#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajoute les liens sociaux au pied de page du site DM Optique (toutes les pages).

Pourquoi cet outil plutôt qu'une retouche à la main : le site compte une soixantaine de
fichiers HTML autonomes (chaque page porte son propre CSS). Une insertion manuelle laisse
forcément des pages sans lien — et un pied de page différent d'une page à l'autre se voit.

Ce que l'outil fait, et rien de plus :
  1. insère un bloc `Facebook · TikTok` dans la barre de bas de page (`div.stripbar`) ;
  2. ajoute la règle CSS `.stripbar .social` si elle manque ;
  3. complète le `sameAs` du schéma JSON-LD (données structurées) — c'est ce que Google lit ;
  4. est **idempotent** : relancer ne duplique rien.

Usage :
    python3 tools/site/add_social_footer.py            # applique
    python3 tools/site/add_social_footer.py --check    # ne modifie rien, liste l'état

⚠️ Une seule source pour les adresses : SOCIAL ci-dessous. Si le lien Facebook change
(numéro de page, ou nom d'utilisateur obtenu plus tard), on modifie ici et on relance.
"""
from __future__ import annotations

import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, "hosting", "previews", "dmoptic")

# ── la seule source des adresses ──────────────────────────────────────────────
SOCIAL = [
    ("Facebook", "https://www.facebook.com/profile.php?id=61595694418153"),
    ("TikTok", "https://www.tiktok.com/@dmoptique.bonaberi237"),
]

CSS = (
    ".stripbar .foot-l{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}\n"
    ".stripbar .foot-l .social{display:flex;gap:18px}\n"
)

BLOCK = (
    '<span class="social">'
    + "".join(
        f'<a href="{url}" target="_blank" rel="noopener">{name}</a>'
        for name, url in SOCIAL
    )
    + "</span>"
)


def pages():
    for base, _dirs, files in os.walk(SITE):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(base, f)


def patch(html: str) -> tuple[str, list[str]]:
    done = []

    # 1 · la barre de bas de page — © et réseaux groupés à gauche, « haut de page » à droite
    if 'class="foot-l"' not in html:
        # on retire un éventuel bloc posé par une version précédente de cet outil
        html = re.sub(r'\s*<span class="social">.*?</span>(?=\s)', "", html, count=1, flags=re.S)
        html = html.replace(".stripbar .social{display:flex;gap:18px}\n", "")
        m = re.search(r'(<div class="stripbar">\s*)(<span>©[^<]*</span>)', html)
        if m:
            pair = f'<span class="foot-l">{m.group(2)}{BLOCK}</span>'
            html = html[: m.start()] + m.group(1) + pair + html[m.end():]
            done.append("stripbar")

    # 2 · la règle CSS (une seule fois par page)
    if ".stripbar .foot-l" not in html and ".stripbar a{" in html:
        i = html.index(".stripbar a{")
        html = html[:i] + CSS + html[i:]
        done.append("css")

    # 3 · les données structurées : sameAs = la liste complète
    urls = [u for _n, u in SOCIAL]
    m = re.search(r'"sameAs":\[(.*?)\]', html, re.S)
    if m:
        have = re.findall(r'"(https?://[^"]+)"', m.group(1))
        missing = [u for u in urls if u not in have]
        if missing:
            new = ", ".join(f'"{u}"' for u in have + missing)
            html = html[: m.start()] + '"sameAs":[' + new + "]" + html[m.end():]
            done.append("sameAs")

    return html, done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    total = changed = 0
    for p in sorted(pages()):
        total += 1
        src = open(p, encoding="utf-8").read()
        out, done = patch(src)
        if done:
            changed += 1
            rel = os.path.relpath(p, SITE)
            print(f"  {rel:<58} {'+'.join(done)}")
            if not a.check:
                open(p, "w", encoding="utf-8").write(out)

    verb = "à corriger" if a.check else "modifiées"
    print(f"\n{total} pages · {changed} {verb}")
    if a.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
