#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_laws.py — les six lois de la capture du 28/10, mesurées au lieu d'être récitées.

Les six lois (capture `designs_by_max`, 28/10/2026) : closure, figure-ground, banner blindness,
Parkinson, connectedness, choice overload. Cinq viennent de la perception ou de la psychologie
cognitive, une (banner blindness) de l'eye-tracking. Toutes ont un point commun : **elles décrivent
un défaut qu'on ne voit plus à force de regarder sa propre page**.

Ce que ce script mesure, et ce qu'il ne mesure pas
--------------------------------------------------
Il lit le HTML et le CSS servis. Il ne regarde PAS le rendu : pas de pixel, pas de défilement, pas de
regard. Il attrape donc les défauts **de structure** — un rail sans amorce, un panneau sans voile, une
pastille qui ressemble à un widget, un formulaire qui ne remplit rien, des étapes qui ne sont pas
reliées, une rangée de décisions trop longue. Le reste (l'amorce est-elle assez visible ? le voile
est-il assez sombre ?) se juge sur une capture, et c'est `shot.py` + `audit_palette.py`.

Chaque constat nomme la loi, le sélecteur, et la correction attendue.

Usage
-----
    python3 tools/qa/audit_laws.py --self-test
    python3 tools/qa/audit_laws.py page.html [autre.html …] [--strict]
    python3 tools/qa/audit_laws.py --dir hosting/previews/dmoptic   # tous les .html, sans récursion

Code de sortie : 0 = aucune faute bloquante, 1 = au moins une (ou un avertissement avec --strict).
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Lire une page : CSS et HTML séparés, parce que les deux lois de structure vivent dans le CSS.

TAG = re.compile(r"<([a-zA-Z][\w-]*)([^>]*)>", re.S)
ATTR = re.compile(r"([\w:-]+)\s*=\s*\"([^\"]*)\"")


def read(path) -> tuple[str, str]:
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)      # un commentaire n'est pas un sélecteur
    return text, css


def css_rules(css: str) -> list[tuple[str, str]]:
    """(sélecteur, corps) pour chaque règle. Les at-rules sont aplaties : on garde le sélecteur interne,
    parce que c'est lui qui porte la mesure (une média-requête n'annule pas une largeur de carte)."""
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel, body = m.group(1).strip(), m.group(2)
        if sel.startswith("@"):                     # @media { … } : la règle interne suit
            continue
        out.append((sel, body))
    return out


def tags(html: str):
    for m in TAG.finditer(html):
        attrs = dict(ATTR.findall(m.group(2)))
        yield m.group(1).lower(), attrs, m.start()


# ─────────────────────────────────────────────────────────────────────────────
# L1 · CLOSURE — « la carte suivante doit dépasser »
# Sans amorce, une rangée qui s'arrête net dit « c'est tout ». Avec 20-35 % de la carte suivante,
# le cerveau complète la série tout seul (Gestalt, fermeture) et la main sait qu'il y a une suite.

SCROLLER = re.compile(r"overflow-x\s*:\s*(auto|scroll)")
AUTOCOL = re.compile(r"grid-auto-columns\s*:\s*([\d.]+)\s*(%|px)")
FLEXBASIS = re.compile(r"flex\s*:\s*0\s+0\s+([\d.]+)\s*(%|px)")


def check_closure(css: str, html: str = "") -> dict:
    out = {"law": "L1 closure", "fails": [], "warns": [], "notes": [], "measured": []}
    rules = css_rules(css)
    def used(selector: str) -> bool:
        """Une règle qui ne sert à rien ne mesure rien : on ne juge que le CSS réellement appliqué."""
        if not html:
            return True
        classes = re.findall(r"\.([\w-]+)", selector)
        return any(f'class="{c}"' in html or f" {c}" in html or f'"{c} ' in html
                   for c in classes) if classes else True

    rails = [(s, b) for s, b in rules if SCROLLER.search(b) and used(s)]
    if not rails:
        out["notes"].append("aucun rail horizontal : la loi ne s'applique pas à cette page")
        return out
    for sel, body in rails:
        width = AUTOCOL.search(body) or FLEXBASIS.search(body)
        if not width:
            out["warns"].append(
                f"« {sel} » défile horizontalement sans largeur de carte déclarée — l'amorce n'est "
                f"donc pas garantie (attendu : 65-80 % de la largeur du conteneur)")
            continue
        val, unit = float(width.group(1)), width.group(2)
        if unit == "px":
            out["notes"].append(f"« {sel} » : cartes en {val:g} px — l'amorce dépend de la fenêtre, à vérifier sur capture")
            continue
        peek = 100.0 - val
        out["measured"].append((sel, val, peek))
        out["notes"].append(f"« {sel} » : carte à {val:g} %, amorce de {peek:g} % — dans la bande 8-55 %")
        if peek < 8:
            out["fails"].append(
                f"« {sel} » : carte à {val:g} % du conteneur, amorce de {peek:g} % seulement — la rangée "
                f"s'arrête net et lit comme « c'est tout » (repasser la carte à 65-80 %)")
        elif peek > 55:
            out["warns"].append(
                f"« {sel} » : carte à {val:g} % — amorce de {peek:g} %, deux cartes et demie à l'écran : "
                f"la rangée lit comme une grille bancale plutôt que comme une suite")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# L2 · FIGURE-GROUND — « ce qui est derrière doit reculer »
# Un panneau posé sur la page sans voile laisse l'œil hésiter entre deux plans. Le repère de la
# capture : 17,4:1 avant, 2,5:1 après — autrement dit le fond perd les trois quarts de son contraste.

OVERLAY_SEL = re.compile(r"(dialog|\.mnav-panel|\.panel|\.modal|\.sheet|\.drawer|\[role=[\"']?dialog)")
SCRIM = re.compile(r"(::?before|::?after|\.scrim|\.backdrop|\.overlay|\.veil|\.voile)")
RGBA = re.compile(r"rgba?\(([^)]*)\)")


def alpha_of(body: str) -> float:
    """Le canal alpha, lu correctement : `rgba(10,18,32,.55)` donne .55, pas 18.

    (La version paresseuse de cette expression rendait 18 — le deuxième composant — et déclarait donc
    tous les voiles transparents. Un outil qui se trompe dans le sens du silence est le pire des cas :
    c'est le banc de test qui l'a vu, pas la page.)"""
    for m in RGBA.finditer(body):
        parts = [x.strip() for x in m.group(1).split(",")]
        if len(parts) == 4:
            try:
                return float(parts[3])
            except ValueError:
                return 0.0
    return 0.0


def check_figure_ground(css: str, html: str) -> dict:
    out = {"law": "L2 figure-ground", "fails": [], "warns": [], "notes": [], "measured": []}
    rules = css_rules(css)
    panels = [(s, b) for s, b in rules
              if OVERLAY_SEL.search(s) and re.search(r"(position\s*:\s*(absolute|fixed)|z-index)", b)]
    if not panels:
        out["notes"].append("aucun panneau superposé : la loi ne s'applique pas à cette page")
        return out

    # un voile = une règle qui couvre l'écran (inset/left+right 0) ET assombrit (rgba alpha ≥ .35)
    # Un voile de panneau est un ÉTAT (menu ouvert, dialogue actif), pas un dégradé de photographie.
    # Sans cette distinction, `.hero-scrim` (un voile de lisibilité à 94 %) passait pour le voile du
    # menu et le constat disparaissait — un faux négatif, le plus dangereux des deux.
    STATE = re.compile(r"(\[open\]|\.is-open|:target|\.is-active|aria-expanded)")
    scrims = []
    for sel, body in rules:
        if re.search(r"(linear|radial)-gradient", body):
            continue                                 # voile de photo : il sert la lisibilité, pas la profondeur
        stateful = bool(STATE.search(sel)) or bool(re.search(r"(scrim|backdrop|overlay|veil|voile)", sel, re.I))
        if not stateful:
            continue
        covers = re.search(r"inset\s*:\s*0", body) or (
            re.search(r"left\s*:\s*0", body) and re.search(r"right\s*:\s*0", body))
        alpha = alpha_of(body)
        if "backdrop-filter" in body and "blur" in body:
            alpha = max(alpha, 0.35)                  # un flou franc sépare aussi les plans
        if covers and alpha >= 0.35:
            scrims.append((sel.strip()[:60], alpha))

    for sel, body in panels:
        out["measured"].append(sel)
        if not scrims:
            out["fails"].append(
                f"panneau « {sel} » sans voile : la page derrière reste au même contraste, l'œil ne "
                f"sait pas quel plan est devant (ajouter un fond plein écran rgba(…,.35+) ou un flou)")
            continue
        if not re.search(r"box-shadow|border|background", body):
            out["warns"].append(
                f"panneau « {sel} » : voile présent mais le panneau lui-même ne se détache pas "
                f"(ni ombre, ni bord, ni surface propre)")
    if scrims:
        out["notes"].append("voile(s) : " + ", ".join(f"{s} α={a:g}" for s, a in scrims))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# L3 · BANNER BLINDNESS — « ce qui compte ne doit pas ressembler à une pub »
# Depuis Benway & Lane (1998) et trente ans d'eye-tracking NN/g : l'œil saute ce qui a la FORME d'une
# annonce — rectangle bordé, pastille flottante, encart isolé — même quand le contenu est utile.

AD_CUE = re.compile(r"(^|[-_])(ad|ads|pub|promo|sponsor|annonce|banner|bannerbox|widget)([-_]|$)")
CTALIKE = re.compile(r"(class=\"[^\"]*\bbtn\b|role=\"button\")")


CSS_OF = {"current": ""}


def check_banner(html: str) -> dict:
    out = {"law": "L3 banner blindness", "fails": [], "warns": [], "notes": [], "measured": []}
    if re.search(r"<ins\b|adsbygoogle|data-ad-slot", html):
        out["fails"].append("<ins> ou emplacement publicitaire présent : le contenu voisin devient suspect")

    # 1 · un conteneur étiqueté comme publicité qui porte une action
    for tag, attrs, _ in tags(html):
        cls = attrs.get("class", "")
        if AD_CUE.search(cls) and CTALIKE.search(html[_: _ + 1200]):
            out["fails"].append(
                f"<{tag} class=\"{cls[:50]}\"> porte une action principale : ce conteneur a la forme "
                f"d'une annonce, l'action sera sautée (rentrer le bouton dans une carte de contenu)")

    # 2 · la pastille isolée : la forme se lit dans le CSS (rayon ≥ 24 px + bord), l'usage dans le HTML
    for sel, body in css_rules(CSS_OF.get("current", "")):
        rad = re.search(r"border-radius\s*:\s*(\d+)px", body)
        if not rad or int(rad.group(1)) < 24:
            continue
        if "border" not in body:
            continue
        cls = sel.strip().lstrip(".")
        if not re.fullmatch(r"[\w-]+", cls):
            continue
        for tag, attrs, pos in tags(html):
            if tag != "a" or cls not in attrs.get("class", "").split():
                continue
            before = html[:pos]
            in_nav = before.rfind("<nav") > before.rfind("</nav>")
            in_list = before.rfind("<ul") > before.rfind("</ul>")
            if in_nav or in_list:
                continue
            out["warns"].append(
                f"<a class=\"{cls}\"> : pastille bordée de {rad.group(1)} px, isolée du flux — c'est "
                f"la forme d'un widget publicitaire ; en faire un lien de texte dans la liste voisine "
                f"(même information, même place, autre forme)")
            out["measured"].append(cls)
            break
    if not out["warns"] and not out["fails"]:
        out["notes"].append("aucune forme publicitaire détectée (encart étiqueté, pastille isolée, <ins>)")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# L4 · PARKINSON — « remplir ce qu'on sait déjà »
# Toute tâche gonfle jusqu'à occuper le temps disponible : demander 30 frappes là où 7 suffisent,
# c'est 23 frappes de friction. Autofill : +12 points de complétion (Zuko, 215 formulaires).

FIELD = re.compile(r"<(input|select|textarea)\b([^>]*)>", re.I)
ACTION = re.compile(r"<button\b([^>]*)>(.*?)</button>", re.I | re.S)


def check_parkinson(html: str) -> dict:
    out = {"law": "L4 Parkinson", "fails": [], "warns": [], "notes": [], "measured": []}
    forms = re.findall(r"<form\b[\s\S]*?</form>", html, re.I)
    if not forms:
        out["notes"].append("aucun formulaire : la loi ne s'applique pas à cette page")
        return out
    for n, form in enumerate(forms, 1):
        fields = [(t.lower(), a) for t, a in FIELD.findall(form)]
        if not fields:
            continue
        autofillable = 0
        prefilled = 0
        for tag, a in fields:
            attrs = dict(ATTR.findall(a))
            if tag == "input" and attrs.get("type") in ("hidden", "submit", "button", "checkbox", "radio"):
                continue
            if attrs.get("autocomplete") and attrs["autocomplete"] != "off":
                autofillable += 1
            if attrs.get("value") or "checked" in a or "selected" in a:
                prefilled += 1
        typed = [f for f in fields if not ("type=\"checkbox\"" in f[1] or "type=\"radio\"" in f[1]
                                           or "type=\"hidden\"" in f[1] or "type=\"search\"" in f[1])]
        out["measured"].append((n, len(fields), len(typed), autofillable, prefilled))
        if typed and autofillable == 0 and prefilled == 0:
            out["warns"].append(
                f"formulaire {n} : {len(typed)} champ(s) à saisir, aucun remplissable par le navigateur "
                f"et aucun rempli d'avance — ajouter les attributs `autocomplete` (name, tel, email, "
                f"postal-code) et un défaut là où la réponse est connue")
        # les boutons qui font la même chose
        labels = [re.sub(r"<[^>]+>", "", m.group(2)) for m in ACTION.finditer(form)]
        labels = [re.sub(r"\s+", " ", l).strip().lower() for l in labels if l.strip()]
        synonyms = [("tout afficher", "effacer"), ("show all", "clear")]
        hit = next(((a, b) for a, b in synonyms
                    if any(a in l for l in labels) and any(b in l for l in labels)), None)
        if hit:
            out["warns"].append(
                f"formulaire {n} : deux boutons pour la même intention (« {hit[0]} » et « {hit[1]} ») — "
                f"un seul suffit, l'autre est une décision de plus pour rien")
        if len(labels) > 3:
            out["warns"].append(
                f"formulaire {n} : {len(labels)} boutons dans la barre — au-delà de 3, la rangée "
                f"d'actions elle-même devient un choix à faire")
    if not out["warns"] and not out["fails"]:
        out["notes"].append("champs tous remplissables ou remplis d'avance")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# L5 · CONNECTEDNESS — « les étapes d'un flux doivent se toucher »
# Des éléments reliés visuellement sont perçus comme un ensemble, plus fort que la proximité ou la
# ressemblance. Trois cartes séparées = trois choses ; trois cartes reliées = un parcours.

STEPS = re.compile(r"(^|[-_.])(steps?|flow|timeline|progress|etapes?|parcours)([-_]|$)")
NUM = re.compile(r">\s*(0?[1-9])\s*<")
CONNECTOR = re.compile(r"(::?before|::?after|\.connector|\.rail|\.line\b|\.track)")


def check_connected(css: str, html: str) -> dict:
    out = {"law": "L5 connectedness", "fails": [], "warns": [], "notes": [], "measured": []}
    rules = css_rules(css)
    containers = [(s, b) for s, b in rules if STEPS.search(s) and not s.strip().startswith(("::", ":"))]
    if not containers:
        out["notes"].append("aucun groupe d'étapes déclaré : la loi ne s'applique pas à cette page")
        return out
    seen = set()
    for sel, body in containers:
        base = sel.strip().split()[0].split(",")[0].replace(":hover", "")
        if base in seen:                      # base + média-requête = le même groupe, pas deux constats
            continue
        seen.add(base)
        out["measured"].append(base)
        # le conteneur relie-t-il ses enfants, ou se contente-t-il de les espacer ?
        gap_only = bool(re.search(r"gap\s*:", body)) and not re.search(r"border|::", body)
        stem = base.rstrip("s")                   # `.steps` → `.step` : les enfants s'écrivent au singulier
        child_rules = [(s, b) for s, b in rules
                       if s.strip().startswith(base) or s.strip().split()[0].startswith(stem)]
        has_connector = any(
            CONNECTOR.search(s) or re.search(r"(border-(top|left|bottom)\s*:|box-shadow\s*:)", b)
            for s, b in child_rules)
        cards = any(re.search(r"(background\s*:|border\s*:)", b) for s, b in child_rules
                    if re.search(r"background\s*:", b))
        if gap_only and cards and not has_connector:
            out["warns"].append(
                f"« {base} » : les étapes sont des cartes séparées, rien ne les relie — trois cartes "
                f"lisent comme trois choses, pas comme un parcours (ajouter un filet ou un rail entre "
                f"les numéros, ou supprimer les bordures pour en faire une seule surface)")
        elif has_connector:
            out["notes"].append(f"« {base} » : un élément de liaison existe")
    if not out["warns"] and not out["fails"]:
        out["notes"].append("étapes reliées")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# L6 · CHOICE OVERLOAD — « moins d'options d'abord »
# Jam study (Iyengar & Lepper, 2000) : 24 confitures → 3 % d'achat, 6 → 30 %. La méta-analyse de 2010
# tempère (effet moyen proche de zéro), mais quatre conditions le déclenchent : décision peu
# importante, options peu comparables, préférence floue, pas d'outil de comparaison. Nos catalogues
# sans prix cochent les quatre.

NAV = re.compile(r"<nav\b[\s\S]*?</nav>", re.I)


def check_choice(html: str) -> dict:
    out = {"law": "L6 choice overload", "fails": [], "warns": [], "notes": [], "measured": []}
    for m in NAV.finditer(html):
        block = m.group(0)
        links = len(re.findall(r"<a\b", block))
        if links > 5:
            out["warns"].append(
                f"navigation à {links} entrées — au-delà de 5, la barre redevient une liste à lire "
                f"(regrouper, ou sortir les entrées secondaires du premier niveau)")
        out["measured"].append(("nav", links))

    # contrôles de filtre visibles d'emblée
    panel = re.search(r"class=\"[^\"]*filters?-panel[^\"]*\"[\s\S]*?</div>\s*</form>", html)
    if panel:
        # Ne comptent que les contrôles VISIBLES d'emblée : un dépliant fermé est déjà une réponse à
        # la surcharge (c'est tout l'objet de la correction), le compter comme visible serait absurde.
        flat = re.sub(r"<details\b[\s\S]*?</details>", "", panel.group(0))
        n = len(re.findall(r"<input\b", flat))
        folded = len(re.findall(r"<input\b", panel.group(0))) - n
        out["measured"].append(("filtres", n, "repliés", folded))
        if folded:
            out["notes"].append(f"{folded} contrôle(s) derrière un dépliant : sous la barre des 7 visibles")
        if n > 7:
            out["warns"].append(
                f"panneau de filtres à {n} contrôles — la table de confitures : garder les deux "
                f"familles utiles visibles, replier le reste derrière « Filtrer » avec un compte")

    # fiches affichées d'un coup
    # Un outil de comparaison (filtres, recherche) amortit la surcharge : la méta-analyse de 2010
    # montre que l'effet disparaît quand les options sont comparables. On ne crie donc pas au loup
    # sur un catalogue filtrable… sauf s'il affiche tout d'un coup.
    comparable = bool(re.search(r"(filters?-panel|v2-filters|role=\"search\")", html))
    cards = len(re.findall(r"class=\"[^\"]*\bv2-card\b", html))
    if cards:
        out["measured"].append(("fiches", cards))
        if cards > 12 and not re.search(r"(voir plus|load more|show more|charger plus)", html, re.I):
            if comparable:
                out["notes"].append(
                    f"{cards} fiches affichées, mais un outil de comparaison existe (filtres) : "
                    f"surcharge amortie — surveiller au premier test réel")
            else:
                out["warns"].append(
                    f"{cards} fiches affichées d'un coup sans « voir plus » ni filtre — une galerie "
                    f"est une exploration, pas un choix : garder la première rangée courte et "
                    f"laisser le défilement faire le reste")
    if not out["warns"]:
        out["notes"].append("aucune décision surchargée détectée")
    return out


# ─────────────────────────────────────────────────────────────────────────────

CHECKS = ("closure", "figure", "banner", "parkinson", "connected", "choice")


def audit(path, checks=CHECKS) -> dict:
    html, css = read(path)
    res = {}
    if "closure" in checks:
        res["closure"] = check_closure(css, html)
    if "figure" in checks:
        res["figure"] = check_figure_ground(css, html)
    if "banner" in checks:
        CSS_OF["current"] = css
        res["banner"] = check_banner(html)
    if "parkinson" in checks:
        res["parkinson"] = check_parkinson(html)
    if "connected" in checks:
        res["connected"] = check_connected(css, html)
    if "choice" in checks:
        res["choice"] = check_choice(html)
    return res


MARKS = {"L1 closure": "CLOSURE", "L2 figure-ground": "FIGURE", "L3 banner blindness": "BANNIÈRE",
         "L4 Parkinson": "PARKINSON", "L5 connectedness": "RELIÉ", "L6 choice overload": "CHOIX"}


def report(path, res) -> tuple[int, int]:
    fails = sum(len(r["fails"]) for r in res.values())
    warns = sum(len(r["warns"]) for r in res.values())
    print(f"\n{path} — 6 lois")
    print("─" * 78)
    for key, r in res.items():
        head = f"  {MARKS[r['law']]:<10}"
        if r["fails"]:
            print(f"{head} ✗ {len(r['fails'])} faute(s)")
            for f in r["fails"]:
                print(f"             {f}")
        elif r["warns"]:
            print(f"{head} · {len(r['warns'])} avertissement(s)")
            for w in r["warns"]:
                print(f"             {w}")
        else:
            print(f"{head} ✓ {r['notes'][0] if r['notes'] else 'rien à signaler'}")
        for w in r["warns"] if r["fails"] else []:
            print(f"             ~ {w}")
    return fails, warns


# ─────────────────────────────────────────────────────────────────────────────
# Le banc : chaque loi a son cas sain et son cas cassé. Un portique sans témoin est un portique
# dont on ne sait pas s'il mord.

GOOD = """<!doctype html><html><head><style>
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:74%;gap:14px;overflow-x:auto}
.panel{position:absolute;top:0;left:0;z-index:40;background:#fff;box-shadow:0 18px 40px rgba(0,0,0,.2)}
.veil{position:fixed;inset:0;background:rgba(10,18,32,.55);z-index:30}
.steps{display:grid;gap:14px}
.step{background:#101b2e;border:1px solid #333}
.steps .step::before{content:"";position:absolute;left:-14px;top:40%;width:14px;border-top:1px solid #666}
</style></head><body>
<nav><a>1</a><a>2</a><a>3</a></nav>
<div class="rail"><article>a</article><article>b</article></div>
<div class="veil"></div><div class="panel">menu</div>
<form><input name="email" type="email" autocomplete="email"><button>Envoyer</button></form>
<div class="steps"><div class="step"><span>1</span></div><div class="step"><span>2</span></div></div>
</body></html>"""

BAD = """<!doctype html><html><head><style>
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:100%;overflow-x:auto}
.panel{position:absolute;top:0;left:0;z-index:40;background:#fff}
.steps{display:grid;gap:14px}
.step{background:#101b2e;border:1px solid #333}
.pill{border-radius:999px;border:1px solid #ccc;padding:8px 12px}
</style></head><body>
<nav><a>1</a><a>2</a><a>3</a><a>4</a><a>5</a><a>6</a><a>7</a></nav>
<div class="rail"><article>a</article></div>
<div class="panel">menu</div>
<div class="promo-banner"><a class="btn" href="#">Offre</a></div>
<a class="pill" href="#"><svg></svg>Ajouter comme source</a>
<form><input name="email" type="email"><input name="tel" type="tel">
<button>Tout afficher</button><button>Effacer</button><button>Plus</button><button>Encore</button></form>
<div class="steps"><div class="step"><span>1</span></div><div class="step"><span>2</span></div></div>
</body></html>"""


def self_test() -> int:
    import tempfile

    total = [0]
    passed = [0]

    def check(label, cond):
        total[0] += 1
        passed[0] += bool(cond)
        print(("  ✓ " if cond else "  ✗ ") + label)
        return bool(cond)

    ok = True
    with tempfile.TemporaryDirectory() as d:
        good = pathlib.Path(d) / "good.html"
        bad = pathlib.Path(d) / "bad.html"
        good.write_text(GOOD, encoding="utf-8")
        bad.write_text(BAD, encoding="utf-8")
        g, b = audit(good), audit(bad)
        ok &= check("sain · closure : rail à 74 % passe", not g["closure"]["fails"])
        ok &= check("cassé · closure : rail à 100 % échoue", bool(b["closure"]["fails"]))
        ok &= check("sain · figure-ground : voile à .55 reconnu", not g["figure"]["fails"])
        ok &= check("cassé · figure-ground : panneau sans voile échoue", bool(b["figure"]["fails"]))
        ok &= check("sain · bannière : rien à signaler", not g["banner"]["warns"] and not g["banner"]["fails"])
        ok &= check("cassé · bannière : encart « promo » qui porte un bouton", bool(b["banner"]["fails"]))
        ok &= check("cassé · bannière : pastille isolée avec icône", any("pastille" in w for w in b["banner"]["warns"]))
        ok &= check("sain · Parkinson : autocomplete posé", not g["parkinson"]["warns"])
        ok &= check("cassé · Parkinson : champs nus", bool(b["parkinson"]["warns"]))
        ok &= check("cassé · Parkinson : deux boutons synonymes",
                    any("même intention" in w for w in b["parkinson"]["warns"]))
        ok &= check("cassé · Parkinson : quatre boutons dans la barre",
                    any("4 boutons" in w for w in b["parkinson"]["warns"]))
        ok &= check("sain · relié : liaison présente", not g["connected"]["warns"])
        ok &= check("cassé · relié : cartes séparées sans liaison",
                    any("rien ne les relie" in w for w in b["connected"]["warns"]))
        ok &= check("cassé · choix : nav à 7 entrées", any("7 entrées" in w for w in b["choice"]["warns"]))
        ok &= check("sain · choix : nav à 3 entrées", not g["choice"]["warns"])
        ok &= check("loi non applicable est dite, pas passée sous silence",
                    "ne s'applique pas" in check_closure("body{margin:0}")["notes"][0])
    print(f"\nbanc de test : {passed[0]}/{total[0]}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Les six lois de la capture du 28/10, mesurées")
    ap.add_argument("pages", nargs="*")
    ap.add_argument("--dir", help="tous les .html d'un dossier, sans récursion")
    ap.add_argument("--only", help="une ou plusieurs lois : closure,figure,banner,parkinson,connected,choice")
    ap.add_argument("--strict", action="store_true", help="un avertissement devient bloquant")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    pages = [pathlib.Path(p) for p in a.pages]
    if a.dir:
        pages += sorted(pathlib.Path(a.dir).glob("*.html"))
    if not pages:
        ap.error("donner au moins une page, ou --dir, ou --self-test")

    checks = CHECKS
    if a.only:
        wanted = {p.strip() for p in a.only.split(",")}
        unknown = wanted - set(CHECKS)
        if unknown:
            ap.error(f"loi inconnue : {', '.join(sorted(unknown))}")
        checks = tuple(c for c in CHECKS if c in wanted)

    total_f = total_w = 0
    for p in pages:
        f, w = report(p, audit(p, checks))
        total_f += f
        total_w += w
    print("\n" + "─" * 78)
    verdict = "BLOQUÉ" if total_f or (a.strict and total_w) else "OK"
    print(f"{total_f} faute(s) · {total_w} avertissement(s) — {verdict}")
    print("Rappel : ce script lit la structure, pas le rendu. L'amorce d'un rail, la noirceur d'un "
          "voile et la force d'une liaison se jugent sur une capture (shot.py).")
    return 1 if (total_f or (a.strict and total_w)) else 0


if __name__ == "__main__":
    sys.exit(main())
