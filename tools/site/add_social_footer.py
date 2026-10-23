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

# ── source préférée sur Google (23/10/2026) ───────────────────────────────────
# Domaine de la canonique du site (dmoptiquesarl.com), pas le *.vercel.app de test : c'est le
# domaine que le lecteur verra dans ses préférences. Mise en oeuvre = le *deeplink* recommandé par
# Search Central pour les sites sans JavaScript tiers : aucun script news.google.com, aucune iframe.
PREF_DOMAIN = "dmoptiquesarl.com"
PREF_URL = f"https://www.google.com/preferences/source?q={PREF_DOMAIN}"
PREF_STAR = ("M12 2.6l2.9 5.88 6.49.94-4.7 4.58 1.11 6.46L12 17.4l-5.8 3.06 1.11-6.46"
             "-4.7-4.58 6.49-.94z")

PREF_CSS = (
    ".psrc{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-top:14px;"
    "padding:0 14px;border:1px solid rgba(169,184,207,.42);border-radius:999px;"
    "color:var(--on-night-2);font-size:13px;line-height:1.2;text-decoration:none;"
    "box-sizing:border-box;transition:color .18s ease,border-color .18s ease}\n"
    ".psrc:hover,.psrc:focus-visible{color:var(--ember-2);border-color:var(--ember-2);"
    "background:rgba(240,145,96,.08)}\n"
    ".psrc:focus-visible{outline:2px solid var(--ember-2);outline-offset:2px}\n"
    ".psrc svg{display:block;width:14px;height:14px;flex:0 0 auto;fill:var(--ember-2)}\n"
    "@media (prefers-reduced-motion:reduce){.psrc{transition:none}}\n"
)

PREF_BLOCK = (
    f'<a class="psrc" href="{PREF_URL}" target="_blank" rel="noopener">'
    f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{PREF_STAR}"/></svg>'
    '<span class="fr-only" lang="fr">Ajouter DM OPTIQUE comme source préférée sur Google</span>'
    '<span class="en-only" lang="en">Add DM OPTIQUE as a preferred source on Google</span></a>'
)

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

    # 2b · le badge « source préférée » sous la description, dans la colonne de marque.
    # Gardé séparément : les pages déjà équipées du pied social ne repassent pas par l'étape 1.
    if 'class="psrc"' not in html:
        m = re.search(r"(<footer[^>]*>.*?<div class=\"fgrid\">\s*<div>.*?</p>)", html, re.S)
        if m:
            html = html[: m.end(1)] + "\n        " + PREF_BLOCK + html[m.end(1):]
            done.append("badge")
    if ".psrc{" not in html and "footer.site" in html:
        i = html.index("footer.site")
        html = html[:i] + PREF_CSS + html[i:]
        done.append("badge-css")

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
