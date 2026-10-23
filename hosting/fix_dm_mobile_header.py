#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE — l'en-tête qui débordait de 21 px au téléphone, et les cartes invisibles.

    python3 hosting/fix_dm_mobile_header.py --check    # ne touche à rien, dit ce qui reste
    python3 hosting/fix_dm_mobile_header.py            # applique à toutes les pages concernées

**Comment ces deux défauts ont été trouvés — et c'est le vrai sujet.** Ils n'ont été vus ni par les
portiques existants, ni par une relecture : ils sont sortis d'une **capture dans un vrai navigateur**
(Chromium + Puppeteer, `tools/qa/shot.py`), à 390 px de large. Les portiques lisent le HTML ; ils ne
mesurent pas une mise en page. C'est l'étape 4 du skill `pro-design`, et elle vient de payer.

**Défaut ① — l'en-tête déborde de 21 px (P1, téléphone).**
À 390 px, `.brand` (blanc-secant, `white-space:nowrap`) + la bascule FR/EN + le bouton de menu (44 px)
ne tiennent pas dans la barre. Le bouton de menu est donc poussé **hors de l'écran de 21 px** : on peut
encore le toucher, mais il est coupé, et la page entière se décale latéralement.
Correctif : sous 430 px, on récupère la place (marges, écart, taille de marque) **sans rien masquer**.

**Défaut ② — quatre cartes de services restaient invisibles (P2, téléphone).**
`.strip` est un carrousel horizontal : les cartes 3 à 6 sont hors écran **à droite**. Or elles portent
la classe de révélation `.rv`, et l'IntersectionObserver ne les voit jamais → elles restent à
`opacity:0`. Le visiteur qui fait défiler le carrousel trouve des cartes vides.
Correctif : la révélation observe aussi **le conteneur** ; quand un carrousel horizontal devient
visible, tous ses `.rv` s'affichent d'un coup.

Idempotent : une page déjà traitée est laissée telle quelle ; `--check` sort en 1 s'il reste du travail.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "previews" / "dmoptic"

MARK_HEADER = "23/10 — en-tête mobile : la marque ne pousse plus le menu hors de l'écran"
MARK_STRIP = "23/10 — carrousel : les cartes hors écran ne restent plus invisibles"

CSS_HEADER = """/* 23/10 — en-tête mobile : la marque ne pousse plus le menu hors de l'écran */
@media (max-width:430px){
  header.site .wrap{gap:10px;padding-left:14px;padding-right:14px}
  header.site .brand{font-size:.96rem;gap:8px;letter-spacing:.04em;min-width:0}
  header.site .brand svg{width:22px;height:22px}
  header.site .langbox{gap:0}
  header.site .langbox button{padding:6px 7px}
  .mnav>summary{width:40px;height:40px}
}
"""

# Le correctif du carrousel remplace la ligne `els.forEach(function(e){io.observe(e)});`
OLD_OBSERVE = "els.forEach(function(e){io.observe(e)});"
NEW_OBSERVE = """els.forEach(function(e){io.observe(e)});
  /* 23/10 — carrousel : les cartes hors écran ne restent plus invisibles
     Un `.rv` placé dans un conteneur qui défile horizontalement n'entre jamais dans le champ de
     l'observateur (il est hors écran à droite) : il restait donc à opacity:0. On observe le
     conteneur, et quand il devient visible toutes ses cartes s'affichent. */
  var strips=[].slice.call(document.querySelectorAll('.rv')).filter(function(e){
    var n=e.parentElement; while(n&&n!==document.body){var cs=getComputedStyle(n);
      if(/auto|scroll/.test(cs.overflowX)) return true; n=n.parentElement;} return false;});
  if(strips.length){var io2=new IntersectionObserver(function(en){
      en.forEach(function(e){ if(e.isIntersecting){
        [].slice.call(e.target.querySelectorAll('.rv')).forEach(function(c){c.classList.add('in')});
        e.target.classList.add('in'); io2.unobserve(e.target);} });},{threshold:.05});
    var boxes=new Set(); strips.forEach(function(e){var n=e.parentElement;
      while(n&&n!==document.body){var cs=getComputedStyle(n);
        if(/auto|scroll/.test(cs.overflowX)){boxes.add(n);break;} n=n.parentElement;}});
    boxes.forEach(function(b){io2.observe(b)});}"""


def pages() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.html"))


def patch(html: str, name: str) -> tuple[str, list[str]]:
    missing: list[str] = []
    if ".mnav" in html and MARK_HEADER not in html and "</style>" in html:
        i = html.index("</style>")
        html = html[:i] + CSS_HEADER + html[i:]
        missing.append(f"{name}:css")
    if OLD_OBSERVE in html and MARK_STRIP not in html:
        html = html.replace(OLD_OBSERVE, NEW_OBSERVE, 1)
        missing.append(f"{name}:carrousel")
    return html, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    todo: list[str] = []
    touched = 0
    for p in pages():
        src = p.read_text(encoding="utf-8", errors="ignore")
        out, missing = patch(src, p.relative_to(ROOT).as_posix())
        if missing:
            todo.extend(missing)
            if not a.check:
                p.write_text(out, encoding="utf-8")
                touched += 1

    if a.check:
        if todo:
            print(f"✗ {len(todo)} correction(s) restante(s) sur {len(set(x.split(':')[0] for x in todo))} page(s)")
            for t in todo[:8]:
                print("   " + t)
            return 1
        print("✓ toutes les pages sont à jour")
        return 0

    print(f"✓ {touched} page(s) corrigée(s)" if touched else "✓ rien à faire (déjà à jour)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
