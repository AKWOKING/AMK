#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE — les icônes d'onglet, tirées du logo du cabinet.

    python3 hosting/make_dm_favicons.py

Ruling King du 23/10/2026 : « can the DM optic logo show beside the DM OPTIQUE SARL in the navbar of
the browser ». C'est le favicon. Ce script le fabrique **depuis `dm-logo.webp`**, sans rien redessiner :

  1. le blanc du fond est rendu transparent par remplissage depuis les quatre coins (le sceau est rond :
     l'extérieur disparaît, l'intérieur reste) ;
  2. le sceau est recadré serré, puis remis à carré avec 4 % de marge — un favicon qui touche le bord
     se lit comme une tache ;
  3. le 16 px est un cadrage serré du même dessin (voir `zoomed`) ;
  4. `favicon.ico` porte 16, 32 et 48 px (Windows, onglet, favoris), `favicon-32.png` et
     `favicon-192.png` servent le reste, et `apple-touch-icon.png` (180 px) est posé sur un fond opaque
     — iOS n'accepte pas la transparence, il la remplit de noir.

Le 16 px restera pâteux avec un sceau à texte : c'est une limite du dessin, pas du script. Le « DM »
tient ; « DM OPTIQUE » non. C'est dit dans `clients/dm-optic/build-notes.md`.
"""
from __future__ import annotations

import base64
import io
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SITE = Path(__file__).resolve().parent / "previews" / "dmoptic"
LOGO = SITE / "dm-logo.webp"
PAPER = (238, 241, 245)          # le papier froid du cabinet (--paper)
MARGIN = 0.04


def seal_with_alpha(src: Image.Image, lum: int = 235, feather: float = 0.9) -> Image.Image:
    """Le sceau est **rond** : on découpe un disque, on ne devine pas le fond.

    Deux essais avant celui-ci, tous deux jetés : la diffusion depuis les coins laissait transparent
    tout pixel non atteint (le sceau sortait en filigrane), puis fuyait à l'intérieur du cercle — le
    blanc du sceau devenait transparent et « DM OPTIQUE » disparaissait sur un onglet sombre. Un disque
    découpé sur la boîte du dessin ne fuit pas : le blanc **intérieur** fait partie du logo et reste.
    """
    img = src.convert("RGB")
    w, h = img.size
    px = img.load()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            if min(px[x, y]) < lum:          # le trait du sceau, pas le fond
                xs.append(x)
                ys.append(y)
    if not xs:
        return img.convert("RGBA")
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    r = max(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 1
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def squared(img: Image.Image, size: int, bg: tuple[int, int, int, int] | None = None) -> Image.Image:
    """Recadre serré sur le sceau, puis le pose au centre d'un carré avec marge."""
    bbox = img.split()[3].getbbox() or (0, 0, img.width, img.height)
    inner = img.crop(bbox)
    side = int(max(inner.size) * (1 + 2 * MARGIN))
    canvas = Image.new("RGBA", (side, side), bg or (0, 0, 0, 0))
    canvas.alpha_composite(inner, ((side - inner.width) // 2, (side - inner.height) // 2))
    return canvas.resize((size, size), Image.LANCZOS)


def zoomed(img: Image.Image, size: int) -> Image.Image:
    """Variante 16 px : le **monogramme DM** du sceau, cadré serré — aucun trait redessiné.

    À 16 px, le sceau complet (cercle + « DM » + « DM OPTIQUE » + lunettes) se réduit à une tache
    grise : quatre traits fins se disputent 256 pixels. On garde les lettres, qui sont la masse bleue
    du dessin, et l'onglet redevient lisible ; 32 px et au-delà gardent le sceau entier.
    """
    bbox = img.split()[3].getbbox() or (0, 0, img.width, img.height)
    inner = img.crop(bbox)
    w, h = inner.size
    crop = inner.crop((int(w * 0.12), 0, int(w * 0.88), int(h * 0.55)))
    side = max(crop.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((side - crop.width) // 2, (side - crop.height) // 2))
    return canvas.resize((size, size), Image.LANCZOS)


def main() -> int:
    if not LOGO.exists():
        print(f"✗ {LOGO} absent")
        return 2
    seal = seal_with_alpha(Image.open(LOGO))
    ico_small = zoomed(seal, 16)                       # 16 px : cadrage serré, lisible
    ico_large = [squared(seal, s) for s in (32, 48)]
    ico_large[-1].save(SITE / "favicon.ico", format="ICO",
                       sizes=[(16, 16), (32, 32), (48, 48)],
                       append_images=[ico_small] + ico_large[:-1])
    squared(seal, 32).save(SITE / "favicon-32.png", "PNG", optimize=True)
    squared(seal, 192).save(SITE / "favicon-192.png", "PNG", optimize=True)
    squared(seal, 180, bg=PAPER + (255,)).save(SITE / "apple-touch-icon.png", "PNG", optimize=True)
    for name in ("favicon.ico", "favicon-32.png", "favicon-192.png", "apple-touch-icon.png"):
        p = SITE / name
        print(f"  {name:22} {p.stat().st_size // 1024:>4} Ko")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
