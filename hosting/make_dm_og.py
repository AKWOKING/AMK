#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE — cartes de partage JPEG (1200 × 630) pour les fiches montures.

    python3 hosting/make_dm_og.py            # écrit montures/monture-XX.jpg
    python3 hosting/make_dm_og.py --check    # dit combien de cartes manquent

Pourquoi : les 80 fiches déclaraient `og:image` en **WebP**. WhatsApp est le canal de partage réel de
ce cabinet (les fiches sont envoyées d'un client à l'autre), et l'aperçu WebP n'y est pas garanti.
Un JPEG 1200 × 630 est le format que tous les aperçus savent dessiner.

La photo est **la photo du produit**, recadrée en couverture sur un fond `--paper` : rien n'est
redessiné, rien n'est inventé. Le JPEG est écrit à côté du WebP, jamais à sa place.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parent / "previews" / "dmoptic"
DIR = SITE / "montures"
PAPER = (238, 241, 245)
W, H = 1200, 630


def card(src: Path) -> Image.Image:
    im = Image.open(src).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    return im.crop((left, top, left + W, top + H))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    missing = [p for p in sorted(DIR.glob("*.webp")) if not p.with_suffix(".jpg").exists()]
    if args.check:
        print(f"{len(missing)} carte(s) à produire")
        return 1 if missing else 0
    for src in missing:
        out = src.with_suffix(".jpg")
        card(src).save(out, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"{len(missing)} carte(s) écrite(s) · 1200 × 630 · JPEG q82")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
