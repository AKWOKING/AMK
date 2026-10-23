#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""raster_svg_path.py — voir un tracé SVG avant de le livrer, avec PIL seul.

Pourquoi ce fichier existe : le bac n'a **ni navigateur, ni cairo, ni rsvg** (`render_svg.py` le dit
depuis le 24/09). Or `tools/qa/render_svg.py` **ne remplit pas les trous** : il dessine chaque
sous-chemin avec `polygon()`, donc le logo Instagram ressort en **carré plein**. Vérifié le 23/10 en
regardant la sortie — c'est ce qui a motivé cet outil.

Ce qu'il fait : échantillonne les segments (`svg.path`), puis remplit par **balayage avec la règle
nonzero** — ce que fait un navigateur. Surdimensionne ×4 et moyenne, ce qui donne un antialiasing.

Limite assumée : segments droits et courbes Bézier uniquement (pas d'arcs `A`), pas de transformations.
Pour un logo Simple Icons, c'est suffisant ; pour autre chose, étendre — pas contourner.

Dépendance non installée d'origine : `pip install --break-system-packages svg.path` (non persistant).

Usage :
    python3 tools/qa/raster_svg_path.py <fichier-svg-ou-.path> <sortie.png> [--size 480]
"""
import argparse
import re

from PIL import Image
from svg.path import parse_path


def subpaths(d, n=48):
    p = parse_path(d)
    subs, cur = [], []
    for seg in p:
        name = seg.__class__.__name__
        if name == "Move":
            if cur:
                subs.append(cur)
            cur = [seg.start]
        elif name == "Close":
            if cur:
                cur.append(cur[0])
                subs.append(cur)
                cur = []
        else:
            if not cur:
                cur = [seg.start]
            cur += [seg.point(i / n) for i in range(1, n + 1)]
    if cur:
        subs.append(cur)
    return subs


def render(d, size=480, vb=24.0, ss=4):
    scale = size / vb
    edges = []
    for sub in subpaths(d):
        pts = [(complex(q).real * scale, complex(q).imag * scale) for q in sub]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            edges.append((x0, y0, x1, y1))
    acc = [0.0] * (size * size)
    for row in range(size * ss):
        y = (row + 0.5) / ss
        xs = []
        for (x0, y0, x1, y1) in edges:
            if y0 == y1:
                continue
            if min(y0, y1) <= y < max(y0, y1):
                t = (y - y0) / (y1 - y0)
                xs.append((x0 + t * (x1 - x0), 1 if y1 > y0 else -1))
        xs.sort()
        wind = 0
        target = row // ss
        for i in range(len(xs) - 1):
            wind += xs[i][1]
            if wind != 0:
                a, b = max(0, int(xs[i][0])), min(size, int(xs[i + 1][0]) + 1)
                for px in range(a, b):
                    acc[target * size + px] += 1
    m = Image.new("L", (size, size))
    m.putdata([min(255, int(255 * v / ss)) for v in acc])
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=480)
    ap.add_argument("--viewbox", type=float, default=24.0)
    args = ap.parse_args()
    raw = open(args.source, encoding="utf-8").read()
    m = re.search(r'd="([^"]+)"', raw)
    d = m.group(1) if m else raw.strip()
    render(d, args.size, args.viewbox).save(args.out)
    print(f"✓ {args.out} ({len(subpaths(d))} sous-chemin(s), règle nonzero)")


if __name__ == "__main__":
    main()
