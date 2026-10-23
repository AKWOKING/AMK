#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Donne aux photos de montures DM Optique la **présentation** des visuels du fournisseur.

Ruling King 23/10/2026 : « can you edit/modify the images of the frames in the repo so that they look
as the ones in the attached images ? » — les visuels joints montrent une monture posée sur un fond
clair continu, avec une ombre douce, cadrée large, sur un set blanc.

Ce que l'outil fait — et surtout ce qu'il ne fait pas :
  • il **ne touche pas à la monture** : aucune déformation, aucun redressement, aucun rendu 3D, aucun
    accessoire inventé (pas d'étui ajouté : nous n'avons photographié aucun étui) ;
  • il remplace le fond crème « détouré » par un **set studio** : dégradé blanc cassé, sol légèrement
    plus sombre, ombre portée douce calculée depuis le détourage réel ;
  • il garde le cadrage, la taille (1600 × 1200) et le nom des fichiers.

Pourquoi ce n'est pas une retouche IA image par image : une monture se choisit sur sa **forme**. Un
modèle génératif qui « redresse » une paire en 3/4 la redessine — et le client reçoit autre chose que
ce qu'il essaiera au cabinet. La forme reste donc pixel pour pixel celle du cabinet.

Le détourage est déduit du fond uni d'origine (couleur du coin), avec un seuil et un adoucissement de
1 px pour éviter une découpe en escalier. Les zones très claires *à l'intérieur* de la monture sont
conservées par un **remplissage depuis les bords** : seuls les pixels reliés au bord deviennent du fond.

Usage :
    python3 tools/site/restyle_frames.py --sample 3 --out /tmp/preview   # regarder avant d'appliquer
    python3 tools/site/restyle_frames.py --check                          # état, n'écrit rien
    python3 tools/site/restyle_frames.py                                  # applique aux 65 fichiers
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / "hosting" / "previews" / "dmoptic" / "montures"

SIZE = (1600, 1200)
BG_TOLERANCE = 34      # écart de couleur toléré comme « fond » (0–255, par canal)
LENS_ALPHA = 64        # les verres restent à peine visibles : on voit le set au travers, comme sur
                       # un vrai détourage produit — mais le reflet de la photo ne disparaît pas
EDGE_SOFTEN = 1.0      # px de flou sur le masque : anti-escalier
MARGIN = 0.055         # marge minimale autour de la monture (fraction de la largeur)
QUALITY = 82


def backdrop(w: int, h: int) -> Image.Image:
    """Set studio : mur blanc cassé en haut, sol un peu plus dense, transition douce."""
    img = Image.new("RGB", (w, h), (253, 253, 251))
    d = ImageDraw.Draw(img)
    horizon = int(h * 0.78)
    for y in range(h):
        if y < horizon:
            t = y / max(horizon, 1)
            c = (253 - int(4 * t), 253 - int(4 * t), 251 - int(3 * t))
        else:
            t = (y - horizon) / max(h - horizon, 1)
            c = (249 - int(10 * t), 249 - int(11 * t), 248 - int(12 * t))
        d.line([(0, y), (w, y)], fill=c)
    return img


def cut(frame: Image.Image) -> tuple[Image.Image, Image.Image]:
    """(monture RGBA, masque plein) — fond déduit des quatre coins, verres conservés en transparence.

    1. le fond d'origine est un crème presque uni : on mesure la moyenne des coins et on prend
       l'écart par canal (tolérance `BG_TOLERANCE`) ;
    2. les **trous** intérieurs (verres) sont repérés par remplissage depuis le bord : ce qui n'est
       pas relié au bord n'est pas du fond ;
    3. la monture est opaque, les verres le sont à `LENS_ALPHA` : le set se voit au travers, comme
       sur un détourage produit — mais le reflet photographié reste un peu présent.
    """
    frame = frame.convert("RGB")
    w, h = frame.size
    corners = [frame.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    diff = ImageChops.difference(frame, Image.new("RGB", frame.size, bg)).convert("L")
    solid = diff.point(lambda v: 255 if v > BG_TOLERANCE else 0).filter(ImageFilter.MedianFilter(7))

    solid = _keep_big(solid)

    flood = solid.copy()
    ImageDraw.floodfill(flood, (0, 0), 128, thresh=0)          # 128 = fond extérieur
    filled = flood.point(lambda v: 0 if v == 128 else 255)     # monture + verres

    alpha = filled.point(lambda v: LENS_ALPHA if v else 0)     # verres : translucides
    alpha.paste(255, (0, 0), solid)                            # monture : opaque
    alpha = alpha.filter(ImageFilter.GaussianBlur(EDGE_SOFTEN))

    subject = frame.convert("RGBA")
    subject.putalpha(alpha)
    return subject, filled


def _keep_big(mask: Image.Image, min_frac: float = 0.0025) -> Image.Image:
    """Retire les taches isolées (filigrane, poussière) : seules les taches reliées et assez
    grandes restent. Le calcul se fait sur un masque réduit (÷4) pour rester rapide en pur Python."""
    small = mask.resize((mask.width // 4, mask.height // 4), Image.BOX)
    px = small.load()
    w, h = small.size
    seen = bytearray(w * h)
    keep = Image.new("L", small.size, 0)
    kp = keep.load()
    min_px = int(w * h * min_frac)
    for y in range(h):
        for x in range(w):
            if px[x, y] < 128 or seen[y * w + x]:
                continue
            stack = [(x, y)]
            seen[y * w + x] = 1
            comp = []
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and px[nx, ny] >= 128 and not seen[ny * w + nx]:
                        seen[ny * w + nx] = 1
                        stack.append((nx, ny))
            if len(comp) >= min_px:
                for cx, cy in comp:
                    kp[cx, cy] = 255
    return ImageChops.multiply(mask, keep.resize(mask.size, Image.LANCZOS))


def restyle(path: Path) -> bytes | None:
    src = Image.open(path).convert("RGB")
    subject, mask = cut(src)

    bbox = mask.getbbox()
    if not bbox:
        return None
    sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]

    canvas = backdrop(*SIZE)
    # échelle : la monture occupe le cadre avec une marge constante
    scale = min((SIZE[0] * (1 - 2 * MARGIN)) / sw, (SIZE[1] * (1 - 2 * MARGIN)) / sh, 1.0)
    nw, nh = int(sw * scale), int(sh * scale)
    sub = subject.crop(bbox).resize((nw, nh), Image.LANCZOS)
    x = (SIZE[0] - nw) // 2
    y = int(SIZE[1] * 0.5 - nh / 2)

    # ombre portée : le profil bas de la monture, écrasé et flouté, posé sous elle
    mask_crop = mask.crop(bbox).resize((nw, nh), Image.LANCZOS)
    band = mask_crop.crop((0, max(nh - int(nh * 0.35), 1), nw, nh))
    sh_h = max(int(nh * 0.10), 6)
    sh = band.resize((nw, sh_h), Image.LANCZOS).filter(
        ImageFilter.GaussianBlur(max(int(SIZE[0] * 0.012), 8)))
    shadow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    shadow.paste((48, 45, 40, 70), (x, y + nh - sh_h // 2), sh)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")

    canvas.paste(sub, (x, y), sub)

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
            print(f"  ✗ {p.name} : détourage impossible")
            failed += 1
            continue
        if args.out:
            (args.out / p.name).write_bytes(data)
        else:
            p.write_bytes(data)
        done += 1
    if not args.check:
        print(f"{done} fichier(s) écrit(s), {failed} échec(s), cible = {args.out or FRAMES}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
