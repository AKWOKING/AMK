#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige le bug des DEUX <summary> (19/09/2026).

Un `<details>` n'a qu'UN SEUL `<summary>` reconnu comme bouton d'ouverture — le premier.
En mettant `<summary class="fr-only">` puis `<summary class="en-only">`, la version anglaise
cachait le premier et laissait un bouton VIDE. La FAQ anglaise de Labiomed et de Bonanjo
s'affichait donc sans aucune question.

Motif CORRECT (celui de tous nos autres sites, validé et en ligne) :
    <summary><span class="fr-only">…</span><span class="en-only">…</span></summary>

Le script fusionne les paires de <summary> ET les paires de <p> qui les suivent.
Idempotent : le relancer ne casse rien.
"""
import pathlib
import re
import sys

FILES = [
    "hosting/previews/labiomed/index.html",
    "hosting/previews/bonanjo/index.html",
]

# <summary class="fr-only">A</summary> ... <summary class="en-only">B</summary>
SUM = re.compile(
    r'<summary\s+class="fr-only"\s*>(?P<fr>.*?)</summary>\s*'
    r'<summary\s+class="en-only"\s*>(?P<en>.*?)</summary>',
    re.S)

# <p class="fr-only">X</p> ... <p class="en-only">Y</p>   (uniquement à l'intérieur d'un <details>)
PAR = re.compile(
    r'<p\s+class="fr-only"\s*>(?P<fr>.*?)</p>\s*'
    r'<p\s+class="en-only"\s*>(?P<en>.*?)</p>',
    re.S)


def fix(path: pathlib.Path, dry=False) -> int:
    t = path.read_text(encoding="utf-8")
    before = t

    t = SUM.sub(lambda m: (f'<summary><span class="fr-only">{m.group("fr").strip()}</span>'
                           f'<span class="en-only">{m.group("en").strip()}</span></summary>'), t)

    # les <p> : on ne fusionne QUE dans les blocs <details>, pour ne pas toucher au reste
    def fix_details(m):
        inner = PAR.sub(lambda x: (f'<p><span class="fr-only">{x.group("fr").strip()}</span>'
                                   f'<span class="en-only">{x.group("en").strip()}</span></p>'),
                        m.group(0))
        return inner

    t = re.sub(r'<details[^>]*>.*?</details>', fix_details, t, flags=re.S)

    n = 0
    if t != before:
        n = len(SUM.findall(before)) + len(PAR.findall(before))
        if not dry:
            path.write_text(t, encoding="utf-8")
    # contrôle : plus aucun <details> avec plusieurs <summary>
    bad = sum(1 for b in re.findall(r'<details[^>]*>.*?</details>', t, re.S)
              if len(re.findall(r'<summary', b)) > 1)
    print(f"  {'✗' if bad else '✓'} {path}  —  {n} paire(s) fusionnée(s), {bad} details encore cassé(s)")
    return bad


def main() -> int:
    dry = "--dry" in sys.argv
    total = 0
    for f in FILES:
        p = pathlib.Path(f)
        if not p.exists():
            print(f"  ⚠ absent : {f}")
            continue
        total += fix(p, dry)
    print("\n" + ("✗ il reste des details cassés" if total else "✓ toutes les FAQ sont réparées"))
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
