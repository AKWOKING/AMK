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

Trois gestes, dans l'ordre :
  1. **fond crème → blanc du set** : un gain par canal, mesuré aux quatre coins de la photo, amène le
     crème du fournisseur à `(250,250,250)`. C'est un changement de **température** du fond, pas de
     la monture : ses couleurs, ses reflets et son ombre sont conservés ;
  2. **recadrage** sur la monture, marge constante, centrée dans le cadre ;
  3. **pose** sur un set blanc uni, sans ombre ajoutée : l'ombre réelle de la photo reste, c'est elle
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
QUALITY = 82


def _neutralise(src: Image.Image) -> Image.Image:
    """Amène le fond crème du fournisseur au blanc du set, sans toucher aux couleurs du produit."""
    w, h = src.size
    corners = [src.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    cream = tuple(sum(c[i] for c in corners) / 4 for i in range(3))
    luts = []
    for i in range(3):
        gain = SET_RGB[i] / max(cream[i], 1.0)
        luts.append([min(255, int(v * gain + 0.5)) for v in range(256)])
    return Image.merge("RGB", [src.getchannel(i).point(luts[i]) for i in range(3)])


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
