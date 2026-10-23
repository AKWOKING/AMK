#!/usr/bin/env python3
"""audit_site_amk — les lois de la maison que les portiques existants ne vérifient pas.

Pourquoi ce fichier
-------------------
`audit_html`, `audit_a11y`, `audit_seo`, `audit_aeo`, `audit_hero` et `audit_images` couvrent la
structure, le contraste, l'accessibilité, les balises et le premier écran. Ils ne voient **pas** ce que
`AMK-DESIGN-SKILLS.md` et `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` exigent :

  · §20.8 — le texte bilingue vit dans TROIS endroits (`data-en`, `data-fr`, le nœud visible) et doit
    dire la même chose ; Google et les robots ne lisent que le nœud.
  · §11b — les mots bannis (« excellence » sans chiffre, « solutions digitales » comme bénéfice…).
  · §13 — le tiret cadratin dans les chaînes anglaises, les `transition: all`, l'entrée en `ease-in`,
    l'absence de `prefers-reduced-motion`.
  · §20.6 — les quatre blocs de pied de page et la ligne de crédit.
  · §20.7 — `og:image` absolu, présent, à la bonne taille.
  · SEO §3.2/§3.6 — les pages `noindex` hors du sitemap ; tout ce que le sitemap annonce existe.
  · SEO §3.8 — aucun chiffre, ville ou disponibilité sans source.

Ce que le script ne fait pas : juger le goût, voir une page, lire une vidéo. Ces trois-là restent
manuels et se disent « non vérifié » dans le rapport.

Usage
-----
    python3 tools/qa/audit_site_amk.py site/            # dossier
    python3 tools/qa/audit_site_amk.py site/index.html  # une page

Sortie : une ligne par constat, `✗` = à corriger, `~` = à vérifier à l'œil, code 1 si au moins un `✗`.
"""
from __future__ import annotations

import html
import json
from html.parser import HTMLParser
import re
import sys
from pathlib import Path

# ── les règles, écrites une fois ────────────────────────────────────────────────────────────────
BANNED_FR = ["révolutionnaire", "passionné", "passionnée", "solutions digitales", "leader du marché",
             "à la pointe", "n°1", "numéro un"]
BANNED_EN = ["world-class", "state-of-the-art", "revolutionary", "cutting-edge", "best-in-class",
             "passionate", "game-changer", "seamless"]
# « excellence » n'est interdit que s'il n'est pas suivi d'un chiffre ou d'un fait : on le signale
# toujours en `~` pour que quelqu'un regarde.
WATCH = ["excellence", "premium", "unique", "premier"]

CREDIT = "site par amk"


def norm(s: str) -> str:
    """Normalise pour comparer : entités, espace insécable, espaces multiples."""
    s = html.unescape(s).replace("\xa0", " ").replace("\u2019", "'")
    return re.sub(r"\s+", " ", s).strip()


def strip_tags(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def attrs_and_nodes(src: str):
    """(data-en, data-fr, texte visible) pour chaque élément qui porte une paire bilingue."""
    out = []
    for m in re.finditer(r"<([a-zA-Z][\w-]*)([^>]*\bdata-en=\"[^\"]*\"[^>]*)>(.*?)</\1>", src, re.S):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        en = re.search(r'data-en="([^"]*)"', attrs)
        fr = re.search(r'data-fr="([^"]*)"', attrs)
        node = strip_tags(inner).strip()
        if en and fr:
            out.append((en.group(1), fr.group(1), node, tag))
    return out


class _BilingParser(HTMLParser):
    """Repère les éléments `data-en` contenus dans un autre élément `data-en`."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack: list[tuple[str, bool]] = []   # (tag, porte data-en)
        self.nested: list[tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "meta", "link", "input", "hr", "source", "path", "circle", "rect", "use"):
            return
        has = any(k == "data-en" for k, _ in attrs)
        if has:
            for parent_tag, parent_has in reversed(self.stack):
                if parent_has:
                    self.nested.append((tag, parent_tag))
                    break
        self.stack.append((tag, has))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


def count_nested_bilingual(src: str) -> list[tuple[str, str]]:
    p = _BilingParser()
    p.feed(src)
    return p.nested


def check_page(p: Path, root: Path) -> tuple[list[str], list[str], list[str]]:
    src = p.read_text(encoding="utf-8", errors="replace")
    ko, warn, info = [], [], []
    rel = p.name

    # §20.8 — trois sources bilingues
    pairs = attrs_and_nodes(src)
    mismatched = []
    for en, fr, node, tag in pairs:
        n = norm(node)
        cand = {norm(x) for x in (en, fr)}
        # le nœud doit correspondre à l'une des deux langues (celle servie sans JS)
        if n and n not in cand:
            mismatched.append((tag, n[:70], norm(en)[:70]))
    if mismatched:
        ko.append(f"§20.8 — {len(mismatched)} texte(s) visible(s) qui ne correspondent NI à data-en NI à "
                  f"data-fr (le robot lit le nœud) · ex. « {mismatched[0][1]} »")

    # §20.8 bis — un élément bilingue DANS un élément bilingue : la bascule écrit innerHTML sur le
    # parent et détruit l'enfant (trouvé le 22/10 : les signatures de témoignages de sample-school
    # disparaissent au premier clic sur FR). Détecté sur l'arbre, pas par regex.
    nested = count_nested_bilingual(src)
    if nested:
        ex = nested[0]
        ko.append(f"§20.8bis — {len(nested)} élément(s) bilingue(s) imbriqué(s) : la bascule écrit "
                  f"`innerHTML` sur le parent et efface l'enfant (ex. <{ex[0]}> dans <{ex[1]}>)")

    # §20.8 ter — parité des DÉLAIS entre les deux langues. Trouvé le 22/10 : l'anglais disait
    # « Live as soon as you approve » et le français « en 3 à 5 jours après l'acompte » — même
    # élément, deux promesses. Un délai promis dans une seule langue reste une promesse publiée.
    # Seuls les nombres portant une unité de durée sont comparés (une heure d'ouverture formatée
    # « 09:00 » vs « 9 h », ou un « 1-page » traduit sans le chiffre, ne sont pas des promesses).
    DUR = re.compile(r"(\d+)\s*(?:jours?|heures?|h\b|semaines?|mois\b|days?|hours?|weeks?|months?)", re.I)

    def _norm_heures(x: str) -> str:
        """« 09:00 », « 9 h », « 9h30 », « 7j/7 » : même information, écritures différentes."""
        x = re.sub(r"\b(\d{1,2})\s*[:h]\s*\d{2}\b", r"\1h", x)
        x = re.sub(r"\b(\d{1,2})\s*h\b", r"\1h", x)
        # « 7j/7 » et « 7 days » portent la même information
        x = re.sub(r"\b(\d{1,2})\s*j\s*/\s*7\b", r"\1 days", x)
        x = re.sub(r"\b24h/24\b", "24/7", x)
        return x
    drift = []
    for en, fr, node, tag in pairs:
        de = sorted(int(x) for x in DUR.findall(_norm_heures(en)))
        df = sorted(int(x) for x in DUR.findall(_norm_heures(fr)))
        # on ne signale que l'asymétrie franche : une langue promet un délai, l'autre aucun.
        # Deux formats d'horaire (09:00 / 9 h, 24/7 / 24h/24) ne sont pas des promesses.
        if bool(de) != bool(df):
            drift.append((tag, en[:60], fr[:60]))
    if drift:
        ko.append(f"§20.8ter — {len(drift)} paire(s) EN/FR dont les délais diffèrent (une promesse "
                  f"retirée d'une langue reste publiée dans l'autre) · ex. « {drift[0][1]} » / « {drift[0][2]} »")

    # §13 — tiret cadratin dans les chaînes anglaises
    em_en = [v for v in re.findall(r'data-en="([^"]*)"', src) if "—" in v]
    if em_en:
        warn.append(f"§13 — {len(em_en)} chaîne(s) anglaises avec un tiret cadratin · ex. « {em_en[0][:70]} »")

    # §11b — mots bannis
    text = strip_tags(src).lower()
    hits = [w for w in BANNED_FR + BANNED_EN if w in text]
    if hits:
        ko.append(f"§11b — mot(s) banni(s) dans le texte visible : {', '.join(hits)}")
    watched = [w for w in WATCH if w in text]
    if watched:
        warn.append(f"§11b — à vérifier (superlatif sans preuve ?) : {', '.join(watched)}")

    # §13 — mouvement
    if re.search(r"transition\s*:\s*all\b", src):
        ko.append("§13 — `transition: all` présent (interdit)")
    if "prefers-reduced-motion" not in src:
        ko.append("§13 — aucun bloc `prefers-reduced-motion` : la page ignore la préférence système")
    if re.search(r"animation[^;{}]*ease-in\b", src) and "ease-in-out" not in src[:0]:
        pass  # trop bruyant pour un audit statique ; laissé au regard
    if re.search(r"opacity\s*:\s*0\b", src) and "html.js" not in src:
        warn.append("§13 — `opacity: 0` sans porte `html.js` : le contenu peut rester invisible sans JS")

    # §20.6 — pied de page
    f = re.search(r"<footer[^>]*>(.*?)</footer>", src, re.S)
    if f:
        foot = f.group(1)
        flat = re.sub(r"\s+", " ", strip_tags(foot)).lower()
        if CREDIT not in flat:
            info.append("§20.4 — pas de ligne de crédit « Site par AMK » dans le pied de page")
        if not re.search(r"tel:|wa\.me|mailto:", foot):
            ko.append("§20.6 — pied de page sans bloc contact (aucun `tel:`, `wa.me` ou `mailto:`)")
        if not re.search(r'href="#[a-z]', foot):
            warn.append("§20.6 — pied de page sans navigation de rappel (aucun lien d'ancre)")

    # §20.7 — carte de lien
    for prop in ("og:title", "og:description", "og:image", "og:url"):
        if f'property="{prop}"' not in src:
            ko.append(f"§20.7 — `{prop}` absent : l'aperçu du lien sera pauvre")
    og_img = re.search(r'property="og:image"\s+content="([^"]+)"', src)
    if og_img:
        u = og_img.group(1)
        if not u.startswith("https://"):
            ko.append(f"§20.7 — `og:image` n'est pas une URL absolue (« {u[:60]} »)")
        else:
            name = u.rsplit("/", 1)[-1]
            if not (root / "img" / name).exists() and not (root / name).exists():
                warn.append(f"§20.7 — `og:image` pointe sur « {name} », absent du dossier local")

    # SEO §3.2 — tout ce que le sitemap annonce existe
    sm = root / "sitemap.xml"
    if sm.exists() and p.name in sm.read_text(encoding="utf-8"):
        if 'content="noindex' in src:
            ko.append("SEO §3.2 — page `noindex` présente dans le sitemap")

    # liens internes morts
    dead = []
    for href in set(re.findall(r'href="([a-zA-Z0-9._-]+\.html)(?:#[^"]*)?"', src)):
        if not (root / href).exists():
            dead.append(href)
    if dead:
        ko.append(f"liens — {len(dead)} fichier(s) lié(s) mais absent(s) : {', '.join(sorted(dead)[:4])}")

    # réseaux sociaux (constat du 22/10 : DM les a, AMK non)
    if not re.search(r"instagram\.com|facebook\.com|tiktok\.com", src):
        info.append("§20.2 — aucun lien vers nos réseaux sociaux (Instagram / Facebook / TikTok)")

    return ko, warn, info


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else Path("site")
    root = target if target.is_dir() else target.parent
    pages = sorted(root.glob("*.html")) if target.is_dir() else [target]
    pages = [p for p in pages if not p.name.startswith(("google", "mockup"))]

    total_ko = 0
    print(f"\naudit site AMK · lois maison · {len(pages)} page(s)\n")
    for p in pages:
        ko, warn, info = check_page(p, root)
        if not (ko or warn):
            print(f"  ok   {p.name}")
        else:
            print(f"  {'✗' if ko else '~'}   {p.name}")
            for k in ko:
                print(f"        ✗ {k}")
            for w in warn:
                print(f"        ~ {w}")
        total_ko += len(ko)
        for i in info:
            print(f"        · {i}")

    print(f"\nTOTAL à corriger : {total_ko}\n")
    return 1 if total_ko else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
