#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porte « tunnel » — la structure d'une page qui convertit, vérifiée mécaniquement.

    python3 tools/qa/audit_funnel.py site/index.html
    python3 tools/qa/audit_funnel.py site --strict          # échoue aussi sur les P2
    python3 tools/qa/audit_funnel.py site/index.html --json

D'où vient cette grille : `knowledge/LANDING-FUNNEL-2026-10-23.md` (vidéo Liam Ottley × Arthur du
04/09/2025, Figma « funnel-fixer », site wecreatebrand.com). Les onze blocs du tableau sont devenus les
contrôles F1–F11, dans l'ordre où un visiteur les rencontre.

**Ce que ce portique ne fera jamais** : juger si un titre est *bon*. Il vérifie qu'il **existe**, qu'il
tient en une ligne, qu'il ne dit pas que des mots creux, et que l'appel à l'action est là. Le reste est
un œil humain — c'est la leçon d'`AUDIT-LESSONS-2026-10-23.md`, réappliquée ici.

Les classes :

  F1  appel à l'action dans le premier écran            F7  FAQ qui lève les objections
  F2  titre de résultat, pas de technologie             F8  action toujours à portée (barre collante)
  F3  preuve (cas, témoignage, chiffres, logos)         F9  mots creux dans les titres
  F4  problème suivi d'une solution                     F10 texte de remplacement oublié
  F5  trois étapes de démarrage                         F11 un CTA principal, pas cinq
  F6  prix, ou devis expliqué

Aucune dépendance : même analyse par expressions régulières que `audit_delivery.py`, pour rester
lisible sans `beautifulsoup`.
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

# Mots qui décrivent ce que NOUS faisons, pas ce que le visiteur obtient.
BUZZWORDS = (
    "sur mesure", "moderne", "moderne et", "solution digitale", "transformation digitale",
    "innovation", "innovant", "à la pointe", "cutting-edge", "state-of-the-art", "synergie",
    "holistique", "disruptif", "révolutionnaire", "expérience unique", "digitalisation",
    "fort de notre expertise", "leader du marché",
)

# Marqueurs d'un résultat, du point de vue du visiteur.
RESULT_WORDS = (
    "gagn", "économis", "trouv", "client", "patient", "parent", "élève", "visib", "vendre",
    "vend", "réserv", "remplir", "appel", "inscri", "rendez-vous", "convert", "chiffre",
    "augment", "rédui", "doubl", "tripl", "avant que",
)

PROOF_MARKERS = (
    "témoignage", "témoignages", "avis", "cas client", "étude de cas", "ils nous font confiance",
    "preuve", "référence", "note de", "★", "★★★★★", "chiffres", "résultat client",
    # l'anglais compte aussi : depuis le 23/10 les deux pages de la maison sont auditées
    "testimonial", "case study", "trusted by", "review",
)

# Preuve « forte » : un client nommé, une histoire, un résultat. Les démonstrations (concepts, maquettes)
# sont une preuve honnête mais **faible** : elles montrent ce que nous savons faire, pas ce qui est arrivé
# à quelqu'un. Le Figma d'Arthur place l'étude de cas au-dessus du témoignage, et le témoignage au-dessus
# du logo — cette hiérarchie est ici explicite.
CASE_MARKERS = (
    "cas client", "étude de cas", "client réel", "témoignage", "témoignages",
    "ils nous font confiance", "avis vérifié", "avant / après", "avant-après", "référence client",
    "real client", "live client", "client story", "customer story",
)

# Placeholders **sans ambiguïté** seulement. « xxx » a été retiré le 23/10 : il attrapait une référence
# de commande de démonstration (« BMC-XXXX ») et les masques de téléphone (« 6XX XX XX XX »), pas un
# oubli. Un portique qui crie à tort apprend à être ignoré.
PLACEHOLDERS = ("lorem ipsum", "lorem", "todo", "[insérer", "[à compléter", "your text here",
                "texte à remplacer")
# « placeholder » est un mot normal dans une phrase (« chaque nom est un emplacement ») et un défaut
# quand il traîne seul dans une page : P3, pas P1. La nuance a coûté un faux positif le 23/10.
PLACEHOLDER_SOFT = ("placeholder", "à remplacer", "à compléter", "to be filled")


class Finding(NamedTuple):
    code: str
    sev: str
    where: str
    message: str
    fix: str


# --------------------------------------------------------------------------- lecture

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def text_of(fragment: str) -> str:
    # Les images embarquées (`data:...;base64,…`) contiennent des suites de lettres — dont « xxx » —
    # qui n'ont rien à voir avec du texte visible : les retirer AVANT tout comptage (faux positif
    # relevé sur `clinic-bonaberi.html`, où le portique criait au texte de remplacement dans un PNG).
    fragment = re.sub(r"data:[^\s\"')]+", " ", fragment)
    fragment = re.sub(r"<svg\b.*?</svg>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = htmllib.unescape(fragment)
    return re.sub(r"\s+", " ", fragment).strip()


def sections(html: str) -> list[tuple[str, str]]:
    """[(id ou classe, html du bloc)] dans l'ordre du document."""
    out = []
    for m in re.finditer(r"<section\b([^>]*)>(.*?)</section>", html, re.S | re.I):
        attrs, body = m.group(1), m.group(2)
        ident = (re.search(r'id="([^"]+)"', attrs) or [None, ""])[1]
        cls = (re.search(r'class="([^"]+)"', attrs) or [None, ""])[1]
        out.append((ident or cls or "section", body))
    return out


def headings(html: str, level: int = 2) -> list[str]:
    return [text_of(m.group(1)) for m in
            re.finditer(rf"<h{level}\b[^>]*>(.*?)</h{level}>", html, re.S | re.I)]


def ctas(fragment: str) -> list[str]:
    """Libellés des liens/boutons qui ressemblent à un appel à l'action."""
    labels = []
    for m in re.finditer(r"<a\b([^>]*)>(.*?)</a>", fragment, re.S | re.I):
        attrs, inner = m.group(1), m.group(2)
        label = text_of(inner)
        if not label:
            continue
        looks_like_button = re.search(r'class="[^"]*\b(btn|button|cta)\b', attrs, re.I) or \
            re.search(r'href="(?:https?://wa\.me|tel:|#contact|mailto:)', attrs, re.I)
        if looks_like_button:
            labels.append(label)
    return labels


def hero_of(html: str) -> str:
    """Le premier écran : la première `<section>` qui porte hero/top, sinon tout avant le 2ᵉ `<h2>`."""
    for ident, body in sections(html):
        if re.search(r"hero|top|masthead", ident, re.I):
            return body
    parts = re.split(r"<h2\b", html, flags=re.I)
    return parts[0] if parts else html


# --------------------------------------------------------------------------- contrôles

def check(page: Path) -> list[Finding]:
    html = read(page)
    out: list[Finding] = []
    secs = sections(html)
    ids = [s[0] for s in secs]
    plain = text_of(html)
    hero = hero_of(html)
    hero_ctas = ctas(hero)

    # F1 · un appel à l'action dans le premier écran
    if not hero_ctas:
        out.append(Finding("F1", "P1", "premier écran",
                           "aucun bouton d'action dans le premier écran : le visiteur lit, hoche la "
                           "tête, et repart sans savoir quoi faire",
                           "un CTA principal en verbe + bénéfice (« recevoir mon aperçu gratuit »), "
                           "répété dans une barre collante"))

    # F2 · titre de résultat
    h1s = [m.group(1) for m in re.finditer(r"<h1\b[^>]*>(.*?)</h1>", html, re.S | re.I)]
    h1 = text_of(h1s[0]) if h1s else ""
    if not h1:
        out.append(Finding("F2", "P1", "<h1>", "page sans titre principal",
                           "un `<h1>` qui dit ce que le visiteur obtient"))
    else:
        low = h1.lower()
        has_result = any(w in low for w in RESULT_WORDS)
        buzz = [w for w in BUZZWORDS if w in low]
        if len(h1) > 110:
            out.append(Finding("F2", "P3", f"<h1> · {len(h1)} caractères",
                               "titre trop long pour être lu d'un coup d'œil",
                               "viser moins de 70 caractères, le reste en sous-titre"))
        if buzz and not has_result:
            out.append(Finding("F2", "P2", f"<h1> · « {buzz[0]} »",
                               "le titre ne dit que le métier ou la techno, pas le résultat : c'est "
                               "le défaut n° 1 relevé dans les six audits de la vidéo",
                               "formuler le bénéfice (« vos parents vous trouvent avant d'appeler ») "
                               "et garder le mot-clé en sous-titre"))
        elif not has_result:
            out.append(Finding("F2", "P3", "<h1>",
                               "aucun mot de résultat dans le titre (client, trouver, gagner, "
                               "inscrire, appeler…)",
                               "vérifier qu'un visiteur pressé comprend ce qu'il gagne en 5 secondes"))

    # F3 · preuve
    low = plain.lower()
    if not any(m in low for m in PROOF_MARKERS):
        out.append(Finding("F3", "P2", "page",
                           "aucun bloc de preuve repérable : ni cas, ni témoignage, ni chiffre, ni "
                           "référence",
                           "la preuve la plus forte disponible : un site client ouvert au public, "
                           "nommé, avec ce qui a été livré et en combien de temps"))
    elif not any(m in text_of(b).lower() for i, b in secs
                 if re.search(r"work|preuve|cas|client|témoin|avis|résultat|result", i, re.I)
                 for m in CASE_MARKERS):
        out.append(Finding("F3", "P3", "preuve",
                           "la preuve offerte est une démonstration (concepts, maquettes), pas un cas "
                           "client : elle montre notre savoir-faire, pas ce qui est arrivé à quelqu'un",
                           "ajouter le premier client réel, nommé et ouvrable, avec ce qui a été livré "
                           "et en combien de temps — avec son accord écrit"))

    # F4 · problème suivi d'une solution
    prob = next((i for i, s in enumerate(secs) if re.search(r"probl|douleur|pain|erreur", s[0], re.I)), None)
    if prob is not None:
        after = [s[0] for s in secs[prob + 1:]]
        if not any(re.search(r"serv|solut|bénéf|benef|offre|ce que nous", i, re.I) for i in after):
            out.append(Finding("F4", "P2", f"section « {secs[prob][0]} »",
                               "la douleur est posée puis abandonnée : la section suivante ne montre "
                               "aucune solution (le défaut qui a coûté le plus cher dans l'étude de "
                               "cas n° 1)",
                               "coller la solution à la douleur, dans la même section ou juste après"))

    # F5 · trois étapes
    step_words = len(re.findall(r"\b(?:étape|step)\s*\d", plain, re.I)) + \
        len(re.findall(r"<li[^>]*>", " ".join(b for i, b in secs if re.search(r"process|étape|etape|step|comment", i, re.I)), re.I))
    if not any(re.search(r"process|étape|etape|step|comment ça marche|how it works", i, re.I) for i in ids) \
            and step_words < 3:
        out.append(Finding("F5", "P3", "page",
                           "pas de déroulé de démarrage : le visiteur ne sait pas à quoi il s'engage",
                           "trois étapes maximum, de son premier message à la mise en ligne"))

    # F6 · prix
    has_price = re.search(r"\d[\d\s.,]{2,}\s*(?:FCFA|XAF|€|\$|EUR|USD)", plain, re.I)
    price_sec = any(re.search(r"prix|tarif|pricing|offre|devis", i, re.I) for i in ids)
    if not price_sec and not has_price:
        out.append(Finding("F6", "P2", "page",
                           "aucune section de prix ni de devis : le visiteur suppose le pire et part",
                           "un bloc prix (ou un devis expliqué, avec ce qui le fait varier)"))
    elif re.search(r"sur devis", plain, re.I) and not has_price:
        out.append(Finding("F6", "P3", "section prix",
                           "« sur devis » seulement : le doute sur le montant reste entier",
                           "donner un point d'entrée (« à partir de … FCFA ») — le prix est un "
                           "filtre, pas une fuite"))

    # F7 · FAQ
    faq = next((b for i, b in secs if re.search(r"faq|question", i, re.I)), "")
    q = len(re.findall(r"<summary\b|<h3\b", faq, re.I)) if faq else 0
    if not faq:
        out.append(Finding("F7", "P2", "page", "pas de FAQ : les objections (prix, délais, contenu à "
                           "fournir) restent dans la tête du visiteur",
                           "trois à six questions, en tête : combien, en combien de temps, qu'est-ce "
                           "que je dois fournir"))
    elif q < 3:
        out.append(Finding("F7", "P3", f"FAQ · {q} question(s)",
                           "FAQ trop courte pour lever les objections nommées dans l'audit",
                           "au moins trois questions : prix, délai, contenu à fournir"))

    # F8 · action toujours à portée
    sticky = re.search(r"position\s*:\s*(?:sticky|fixed)", html, re.I) or \
        re.search(r'class="[^"]*\b(?:mbar|sticky-cta|bottom-bar)\b', html, re.I)
    if not sticky:
        out.append(Finding("F8", "P2", "page",
                           "aucune action à portée de pouce : il faut remonter pour trouver le bouton",
                           "barre collante en haut (CTA) ou barre basse mobile"))

    # F9 · mots creux dans les titres
    for h in headings(html, 1) + headings(html, 2):
        hit = next((w for w in BUZZWORDS if w in h.lower()), None)
        if hit:
            out.append(Finding("F9", "P2", f"titre · « {h[:60]} »",
                               f"mot creux « {hit} » : le décideur fatigué le lit comme du bruit",
                               "remplacer par un résultat concret ou supprimer"))
            break

    # F10 · texte de remplacement
    for ph in PLACEHOLDERS:
        if ph in low:
            out.append(Finding("F10", "P1", f"« {ph} »",
                               "texte de remplacement oublié dans la page",
                               "écrire le vrai contenu ou retirer le bloc"))
    if not any(ph in low for ph in PLACEHOLDERS):
        for ph in PLACEHOLDER_SOFT:
            if ph in low:
                out.append(Finding("F10", "P3", f"« {ph} »",
                                   "le mot apparaît : soit c'est une phrase, soit c'est un oubli",
                                   "relire le passage ; si c'est un oubli, écrire le vrai contenu"))
                break
            break

    # F11 · un CTA principal
    if len(set(hero_ctas)) > 2:
        out.append(Finding("F11", "P3", f"{len(set(hero_ctas))} CTA dans le premier écran",
                           "trop de choix tue le choix",
                           "un CTA principal, au plus un secondaire discret"))
    return out


# --------------------------------------------------------------------------- sortie

def resolve(target: Path) -> Path:
    if target.is_dir():
        for name in ("index.html",):
            if (target / name).exists():
                return target / name
        raise SystemExit(f"✗ aucun index.html dans {target}")
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description="Porte tunnel : la structure d'une page qui convertit")
    ap.add_argument("target", type=Path)
    ap.add_argument("--strict", action="store_true", help="échouer aussi sur les P2")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    page = resolve(args.target)
    findings = check(page)
    order = {"P1": 0, "P2": 1, "P3": 2}
    findings.sort(key=lambda f: (order[f.sev], f.code))

    if args.json:
        print(json.dumps([f._asdict() for f in findings], ensure_ascii=False, indent=2))
    else:
        print(f"\nPORTE TUNNEL — {page}")
        for f in findings:
            print(f"\n  [{f.sev}] {f.code} · {f.where}\n        {f.message}\n        → {f.fix}")
        counts = {s: sum(1 for f in findings if f.sev == s) for s in ("P1", "P2", "P3")}
        print(f"\n  TOTAL {counts['P1']} P1 · {counts['P2']} P2 · {counts['P3']} P3 — "
              f"{'VERT' if not counts['P1'] else 'ROUGE (P1)'}")

    fail = any(f.sev == "P1" for f in findings)
    if args.strict:
        fail = fail or any(f.sev == "P2" for f in findings)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
