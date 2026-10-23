#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Donne aux photos de montures DM Optique la **présentation** des visuels du fournisseur.

Ruling King 23/10/2026 : « can you edit/modify the images of the frames in the repo so that they look
as the ones in the attached images ? » — les visuels joints montrent une monture sur un **fond clair
continu**, cadrée large, sans décor.

Ce que l'outil fait — et ce qu'il ne fait pas :
  • il **ne redessine pas la monture** : ni déformation, ni redressement en 3/4, ni rendu 3D, ni
    image générée, ni accessoire inventé (pas d'étui : nous n'avons photographié aucun étui) ;
  • il ne l'isole pas non plus de son support. Voir « pourquoi pas de détourage » plus bas ;
  • il garde la taille (1600 × 1200) et le nom des fichiers : aucune page HTML à retoucher.

Quatre gestes, dans l'ordre :
  1. **fond crème → blanc du set** par **substitution de couleur** : un pixel qui s'écarte du crème
     mesuré aux quatre coins de moins de `BG_SOLID` devient `(250,250,250)` ; au-delà de `BG_EDGE`
     il n'est pas touché du tout (monture, verres, ombre). Un gain par canal a été essayé d'abord :
     il éclaircissait aussi le produit — le doré de f01 passait de (236,194,117) à (255,223,160) ;
  2. **restes du fournisseur retirés** : la flèche du filigrane, dans un coin, est détachée de la
     monture — elle est effacée ; tout ce qui est dans le cadre de la paire reste ;
  3. **recadrage** sur la monture, marge constante, centrée ;
  4. **pose** sur un set blanc uni, sans ombre ajoutée : l'ombre réelle de la photo reste, c'est elle
     qui fait tenir une monture claire sur un fond clair.

Pourquoi pas de détourage — mesuré sur les 65 fichiers :

  • les **charnières ressort** de plusieurs montures sont presque de la couleur du fond (écart < 25
    par canal). Un seuil de détourage les emporte : la paire apparaît **coupée en deux** (e07, e13)
    ou amputée de ses branches (e17). 14 fichiers sur 65 sont dans ce cas ;
  • les **verres** vont du très clair au bleuté, et sur une monture **percée** ou **semi-cerclée**
    (f01, h01, h04), les verres *sont* la monture : les rendre transparents efface le produit ;
  • un détourage réussi sur 43 photos et raté sur 22 donne une page où **une monture sur trois est
    cassée**. Sur une page qui doit inspirer confiance, c'est pire que le fond crème de départ.

La **carte d'appui** bleutée sur laquelle les montures sont photographiées est conservée : elle est
dans la photo, discrète, et l'effacer proprement demanderait de découper la monture — exactement ce
qu'on refuse. Elle disparaîtra d'elle-même le jour où la série sera re-photographiée sur fond blanc.

La vraie réponse pour des visuels « produit » nets reste donc une **re-photo sur fond blanc uni**
(10 minutes par série). L'outil est réversible (`git checkout` des 65 fichiers) et rejouera la même
présentation sur des photos propres.

Usage :
    python3 tools/site/restyle_frames.py --sample 3 --out /tmp/preview   # regarder avant d'écrire
    python3 tools/site/restyle_frames.py --check                          # état, n'écrit rien
    python3 tools/site/restyle_frames.py                                  # applique aux 65 fichiers
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / "hosting" / "previews" / "dmoptic" / "montures"

SIZE = (1600, 1200)
SET_RGB = (250, 250, 250)   # blanc du set, celui des visuels du fournisseur
MARGIN = 0.055              # marge autour de la monture (fraction du cadre)
CROP_PAD = 0.02             # air ajouté autour de la monture avant recadrage
BG_SOLID = 9                # écart au crème en dessous duquel un pixel EST le fond
BG_EDGE = 20                # écart au-dessus duquel un pixel n'est plus touché du tout
QUALITY = 82


def _neutralise(src: Image.Image) -> Image.Image:
    """Remplace **le fond crème** par le blanc du set, pixel par pixel, sans toucher au produit.

    C'est une substitution de couleur, pas un virage : un pixel qui s'écarte du crème mesuré aux
    quatre coins de moins de `BG_SOLID` est du fond — il devient blanc. Un pixel qui s'en écarte de
    plus de `BG_EDGE` est la monture, son ombre, sa carte d'appui — il **n'est pas modifié**. Entre
    les deux, un dégradé doux évite la découpe en escalier.

    Ce que ça change par rapport à un gain par canal (essayé le 23/10) : le gain éclaircissait aussi
    la monture — le doré de f01 passait de (236,194,117) à (255,223,160), un or devenu pâle, donc un
    produit qui ne ressemble plus tout à fait à celui du présentoir. Ici le doré reste le doré.
    """
    img = src.convert("RGB")
    w, h = img.size
    corners = [img.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    cream = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    px = img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            d = max(abs(r - cream[0]), abs(g - cream[1]), abs(b - cream[2]))
            if d <= BG_SOLID:
                px[x, y] = SET_RGB
            elif d < BG_EDGE:
                t = (d - BG_SOLID) / (BG_EDGE - BG_SOLID)     # 0 = fond, 1 = produit
                px[x, y] = (
                    int(SET_RGB[0] + (r - SET_RGB[0]) * t),
                    int(SET_RGB[1] + (g - SET_RGB[1]) * t),
                    int(SET_RGB[2] + (b - SET_RGB[2]) * t),
                )
    return img


def _drop_specks(img: Image.Image, gap_frac: float = 0.02, min_ratio: float = 0.06) -> Image.Image:
    """Efface les **restes du fournisseur** détachés de la monture (la flèche du filigrane).

    Tout ce qui diffère du set est découpé en taches. La plus grosse est la monture. Une tache est
    effacée si elle pèse moins de `min_ratio` de la monture **et** si elle tombe en dehors de sa
    boîte élargie : c'est ce qui distingue un reste qui flotte dans un coin (flèche du filigrane) d'un
    détail de la monture (une branche, une vis, un reflet), toujours dans le cadre de la paire.
    """
    w, h = img.size
    small = img.resize((w // 4, h // 4), Image.BOX)
    px = small.load()
    sw, sh = small.size

    vis = Image.new("L", (sw, sh), 0)
    vp = vis.load()
    for y in range(sh):
        for x in range(sw):
            r, g, b = px[x, y]
            if max(abs(r - SET_RGB[0]), abs(g - SET_RGB[1]), abs(b - SET_RGB[2])) > 12:
                vp[x, y] = 255

    seen = bytearray(sw * sh)
    comps: list[list[tuple[int, int]]] = []
    for y in range(sh):
        for x in range(sw):
            if not vp[x, y] or seen[y * sw + x]:
                continue
            stack = [(x, y)]
            seen[y * sw + x] = 1
            comp = []
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < sw and 0 <= ny < sh and vp[nx, ny] and not seen[ny * sw + nx]:
                        seen[ny * sw + nx] = 1
                        stack.append((nx, ny))
            comps.append(comp)

    if len(comps) < 2:
        return img
    comps.sort(key=len, reverse=True)

    # boîte de la monture, élargie de `gap` pixels : ce qui est dedans est « proche » et reste
    gap = max(int(sw * gap_frac), 2)
    mx = [p[0] for p in comps[0]]
    my = [p[1] for p in comps[0]]
    x0, x1 = min(mx) - gap, max(mx) + gap
    y0, y1 = min(my) - gap, max(my) + gap

    drop = Image.new("L", (sw, sh), 0)
    dp = drop.load()
    changed = False
    for comp in comps[1:]:
        if len(comp) >= len(comps[0]) * min_ratio:
            continue
        if any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in comp):
            continue
        changed = True
        for x, y in comp:
            dp[x, y] = 255

    if not changed:
        return img
    mask = drop.resize(img.size, Image.LANCZOS).filter(ImageFilter.MaxFilter(5)).filter(
        ImageFilter.GaussianBlur(3))
    return Image.composite(Image.new("RGB", img.size, SET_RGB), img, mask)

def restyle(path: Path) -> bytes | None:
    """Neutralise le fond, recadre sur la monture, pose sur le set. Ne découpe rien."""
    src = Image.open(path).convert("RGB")
    flat = _neutralise(src)

    bg = Image.new("RGB", flat.size, SET_RGB)
    diff = ImageChops.difference(flat, bg).convert("L")
    bbox = diff.point(lambda v: 255 if v > 8 else 0).filter(ImageFilter.MedianFilter(9)).getbbox()
    if not bbox:
        return None

    side = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
    pad = int(side * CROP_PAD)
    box = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
           min(bbox[2] + pad, flat.width), min(bbox[3] + pad, flat.height))
    flat = _drop_specks(flat)
    crop = flat.crop(box)
    cw, ch = crop.size

    scale = min((SIZE[0] * (1 - 2 * MARGIN)) / cw, (SIZE[1] * (1 - 2 * MARGIN)) / ch, 1.0)
    nw, nh = int(cw * scale), int(ch * scale)

    canvas = Image.new("RGB", SIZE, SET_RGB)
    canvas.paste(crop.resize((nw, nh), Image.LANCZOS), ((SIZE[0] - nw) // 2, (SIZE[1] - nh) // 2))

    out = path.with_suffix(".tmp.webp")
    canvas.save(out, "WEBP", quality=QUALITY, method=6)
    data = out.read_bytes()
    out.unlink()
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="ne traite que N fichiers")
    ap.add_argument("--out", type=Path, default=None, help="écrit les essais dans ce dossier")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    files = sorted(FRAMES.glob("monture-*.webp"))
    if args.sample:
        files = files[: args.sample]
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    done = failed = 0
    for p in files:
        if args.check:
            print(f"{p.name:34} {p.stat().st_size // 1024} Ko")
            continue
        data = restyle(p)
        if data is None:
            print(f"  ✗ {p.name} : recadrage impossible")
            failed += 1
            continue
        (args.out / p.name if args.out else p).write_bytes(data)
        done += 1
    if not args.check:
        print(f"{done} fichier(s) écrit(s), {failed} échec(s), cible = {args.out or FRAMES}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
