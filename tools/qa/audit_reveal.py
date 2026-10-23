#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portique du système de révélation au défilement — le bug qui a rendu 142 blocs invisibles.

Deux fois de suite (23/10), la règle de base `html.js .rv{opacity:0}` a été plus **spécifique** que
`.rv.in{opacity:1}` : le JavaScript ajoutait bien la classe, et rien ne s'affichait. Un contrôle de
contraste ne le voit pas, `node --check` non plus, et la page reste blanche **sans une seule erreur en
console**. D'où ce portique.

Ce qu'il vérifie, page par page :
  1. la règle de base porte `:not(.in)` — sinon elle masque l'état révélé (FAUTE) ;
  2. l'état révélé existe (`.rv.in` ou `html.js .rv.in`) — sinon rien ne peut s'afficher (FAUTE) ;
  3. la révélation a un **filet** (repli si pas d'IntersectionObserver, ou un minuteur) — sinon une
     panne de JavaScript laisse la page vide (FAUTE) ;
  4. une règle `@media (scripting:none)` existe — le repli sans JavaScript (AVERTISSEMENT).

Usage :
    python3 tools/qa/audit_reveal.py site/*.html
    python3 tools/qa/audit_reveal.py site/            # tous les .html d'un dossier, sans récursion
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCK = re.compile(r'class="[^"]*\brv\b[^"]*"')


def check(path: Path) -> tuple[list[str], list[str], int]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    blocks = len(BLOCK.findall(html))
    if not blocks:
        return [], [], 0                      # page sans révélation : hors périmètre

    faults, warns = [], []

    base = re.findall(r"html\.js\s+\.rv\s*\{", html)
    good = re.findall(r"html\.js\s+\.rv:not\(\.in\)\s*\{", html)
    if base or not good:
        faults.append("règle de base sans `:not(.in)` → l'état révélé reste invisible")

    if not re.search(r"(html\.js\s+)?\.rv\.in\s*\{", html):
        faults.append("aucune règle `.rv.in` : la classe ajoutée par le JS ne fait rien")

    if "IntersectionObserver" in html:
        # un repli valable : revealAll(), un else qui coche tout, ou un minuteur
        fallback = (
            re.search(r"function\s+revealAll|revealAll\s*\(", html)
            or re.search(r"else\s*\{[^}]*classList\.add\(['\"]in['\"]\)", html, re.S)
        )
        if not fallback:
            faults.append("aucun repli : si l'observateur ne coche pas, les blocs restent invisibles")
        if "setTimeout" not in html:
            warns.append("pas de minuteur de secours : une exception laisse la page bloquée")
    if "scripting:none" not in html:
        warns.append("pas de repli `@media (scripting:none)`")
    return faults, warns, blocks


def main(argv: list[str]) -> int:
    targets: list[Path] = []
    for a in argv or ["site"]:
        p = Path(a)
        targets.extend(sorted(p.glob("*.html")) if p.is_dir() else [p])
    if not targets:
        print("aucune page à contrôler")
        return 2

    total_blocks = errors = warnings = 0
    for t in targets:
        faults, warns, blocks = check(t)
        if not blocks:
            continue
        total_blocks += blocks
        status = "FAIL" if faults else ("warn" if warns else "ok  ")
        print(f"{status} {t} — {blocks} bloc(s) .rv")
        for f in faults:
            print("   ✗ " + f)
        for w in warns:
            print("   ~ " + w)
        errors += len(faults)
        warnings += len(warns)

    print(f"\nTOTAL {total_blocks} bloc(s) · {errors} faute(s) · {warnings} avertissement(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
