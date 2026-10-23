#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pose les montures DM Optique sur un **socle**, comme les visuels du fournisseur.

Ruling King du 23/10/2026, seconde demande : « I see you have changed the background but that won't be
quite enough to satisfy the client, can you generate something (the case or a bench) on which the
frames will stand? »

**Ce qui est généré** : un **socle en acrylique**, dessiné par ce script — pas une image inventée, pas
un objet du commerce. Une dalle translucide vue de face, arête claire sur le dessus, ombre de contact
au sol et **reflet** de la monture dans la matière. C'est de la mise en scène : on ne montre aucun
produit que le cabinet ne vend pas (pas d'étui : nous n'en avons photographié aucun).

**Ce qui n'est pas généré** : la monture. Elle est détourée de la photo d'origine, jamais redessinée,
jamais redressée, jamais complétée.

Le détourage est le point dur, et il a trois garde-fous :

  1. **charnières ressort** — sur certaines montures elles sont presque de la couleur du fond. Elles
     sont récupérées par fermeture morphologique : un pixel clair *entouré* de monture en fait partie
     (e07 et e13 sont entières aujourd'hui, elles sortaient coupées en deux avec un simple seuil) ;
  2. **contrôle de pièces** — si le détourage laisse plusieurs morceaux séparés par plus de 2 % de la
     largeur, la monture est considérée cassée et la photo part en **mode planche** : recadrée, posée
     sur le socle, **sans détourage**. Une monture entière sur un socle vaut mieux qu'une monture
     découpée sur un beau fond ;
  3. **verres** — jamais rendus transparents. Sur une monture percée ou semi-cerclée, les verres
     *sont* la monture.

Usage :
    python3 tools/site/frame_bench.py --sample 3 --out /tmp/preview   # regarder avant d'écrire
    python3 tools/site/frame_bench.py --check
    python3 tools/site/frame_bench.py                                 # les 65 fichiers
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
FRAMES = ROOT / "hosting" / "previews" / "dmoptic" / "montures"

SIZE = (1600, 1200)
SET_RGB = (250, 250, 250)
MARGIN = 0.055
QUALITY = 82
BG_TOLERANCE = 34          # écart au crème mesuré aux coins, en dessous duquel un pixel est du fond
CLOSE_RADIUS = 13          # fermeture morphologique : pont entre deux morceaux qui se touchent presque
PIECE_GAP_FRAC = 0.02      # au-delà de 2 % de la largeur entre deux pièces, la monture est « cassée »
PLAN_CHE: set[str] = {
    # acétate transparent ou cerclage blanc : le matériau et le fond se ressemblent, aucun seuil ne les
    # sépare — le détourage y perce la monture. Ces photos restent entières.
    "monture-e17", "monture-e27", "monture-f06", "monture-f25", "monture-f25-2", "monture-f26", "monture-f59-2",
}
BENCH_H_FRAC = 0.058       # hauteur du socle, en fraction de la hauteur du cadre


# --------------------------------------------------------------------------- détourage

def _keep_big(mask: Image.Image, min_frac: float = 0.0025) -> Image.Image:
    """Retire les poussières et le filigrane : seules les taches reliées et assez grandes restent."""
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


def _components(mask: Image.Image, min_px: int = 600) -> list[list[tuple[int, int]]]:
    """Les taches du masque (sur une image réduite ÷4), les plus grosses d'abord."""
    small = mask.resize((mask.width // 4, mask.height // 4), Image.BOX)
    px = small.load()
    w, h = small.size
    seen = bytearray(w * h)
    out: list[list[tuple[int, int]]] = []
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
            if len(comp) * 16 >= min_px:
                out.append(comp)
    out.sort(key=len, reverse=True)
    return out, (w, h)  # type: ignore[return-value]


def cut(src: Image.Image) -> Image.Image:
    """Masque plein de la monture (contour + verres), charnières claires comprises."""
    img = src.convert("RGB")
    w, h = img.size
    corners = [img.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    diff = ImageChops.difference(img, Image.new("RGB", img.size, bg)).convert("L")
    solid = diff.point(lambda v: 255 if v > BG_TOLERANCE else 0).filter(ImageFilter.MedianFilter(7))
    solid = _keep_big(solid)

    # charnières ressort : pixels clairs et neutres, rattachés par fermeture morphologique
    px = img.load()
    light = Image.new("L", img.size, 0)
    lp = light.load()
    b_r_img = Image.new("L", img.size, 0)
    b_r = b_r_img.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            b_r[x, y] = min(max(b - r, 0), 255)
            if min(r, g, b) >= 190 and max(r, g, b) - min(r, g, b) <= 20:
                lp[x, y] = 255
    closed = ImageChops.lighter(solid, light)
    closed = closed.filter(ImageFilter.MaxFilter(CLOSE_RADIUS)).filter(ImageFilter.MinFilter(CLOSE_RADIUS))
    near = solid.filter(ImageFilter.MaxFilter(17))
    solid = ImageChops.multiply(closed, ImageChops.lighter(solid, near)).filter(ImageFilter.MedianFilter(5))

    # la feuille bleutée sur laquelle certaines montures sont posées laisse un ruban clair qui touche
    # les charnières. On retire d'abord ces pixels « papier bleu pâle » (clairs ET froids : b - r ≥ 5) ;
    # l'acier et l'argent, eux, sont neutres, donc épargnés. Les verres touchés sont rebouchés par le
    # remplissage ci-dessous, qui ne rouvre que le fond relié au coin.
    pale = Image.new("L", img.size, 0)
    pl = pale.load()
    for y in range(0, h):
        for x in range(0, w):
            if lp[x, y] and b_r[x, y] >= 5:
                pl[x, y] = 255
    solid = ImageChops.subtract(solid, pale.filter(ImageFilter.MaxFilter(3)))

    flood = solid.copy()
    ImageDraw.floodfill(flood, (0, 0), 128, thresh=0)
    mask = flood.point(lambda v: 0 if v == 128 else 255)
    return _drop_far_specks(mask)


def is_broken(mask: Image.Image) -> bool:
    """Vrai si le détourage laisse des pièces visiblement séparées : la monture est amputée."""
    comps, (w, h) = _components(mask)
    if len(comps) < 2:
        return False
    gap = PIECE_GAP_FRAC * w
    main = comps[0]
    mx = [p[0] for p in main]
    my = [p[1] for p in main]
    x0, x1 = min(mx) - gap, max(mx) + gap
    y0, y1 = min(my) - gap, max(my) + gap
    return any(not any(x0 <= x <= x1 and y0 <= y <= y1 for x, y in comp) for comp in comps[1:])


def _drop_far_specks(mask: Image.Image, far_frac: float = 0.10, max_frac: float = 0.30) -> Image.Image:
    """Efface les restes du fournisseur **détachés** (la flèche de son filigrane).

    Une pièce de monture — branche, charnière, tenon — est collée au corps principal : ses pixels sont à
    quelques pixels de lui. La flèche du filigrane, elle, flotte à 20 % de la largeur. Une tache est donc
    effacée si elle pèse moins de 30 % de la plus grosse **et** si son pixel le plus proche du corps est
    à plus de 10 % de la largeur. f13-2 en avait une au-dessus du cadre ; le seuil de taille seul ne la
    voyait pas (14,7 % du corps), la distance seule non plus.
    """
    comps, (w, h) = _components(mask)
    if len(comps) < 2:
        return mask
    main = comps[0]
    ref = main[::6] or main
    limit = far_frac * w

    drop = Image.new("L", (w, h), 0)
    dp = drop.load()
    changed = False
    for comp in comps[1:]:
        if len(comp) >= len(main) * max_frac:
            continue
        best = min(min((x - mx) ** 2 + (y - my) ** 2 for mx, my in ref) for x, y in comp[::6])
        if best <= limit ** 2:
            continue
        changed = True
        for x, y in comp:
            dp[x, y] = 255
    if not changed:
        return mask
    small = drop.resize(mask.size, Image.LANCZOS).filter(ImageFilter.MaxFilter(5)).filter(
        ImageFilter.GaussianBlur(2))
    return ImageChops.subtract(mask, small)

# --------------------------------------------------------------------------- décor

def _bench(canvas: Image.Image, cx: int, base_y: int, width: int, height: int) -> Image.Image:
    """Socle en acrylique : dalle translucide, arête claire, ombre de contact."""
    w, h = canvas.size
    top_w, bot_w = width, int(width * 1.04)
    x0t, x1t = cx - top_w // 2, cx + top_w // 2
    x0b, x1b = cx - bot_w // 2, cx + bot_w // 2
    y0, y1 = base_y, base_y + height

    plate = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(plate)
    for i in range(height):
        t = i / max(height - 1, 1)
        xa = int(x0t + (x0b - x0t) * t)
        xb = int(x1t + (x1b - x1t) * t)
        # la dalle s'épaissit vers l'avant : plus dense en bas, presque transparente sur l'arête
        alpha = int(26 + 96 * (t ** 0.5))
        col = (206 + int(20 * (1 - t)), 218 + int(16 * (1 - t)), 232 + int(10 * (1 - t)), alpha)
        d.line([(xa, y0 + i), (xb, y0 + i)], fill=col)
    # arête supérieure (le verre attrape la lumière) et bord avant (il la perd)
    d.line([(x0t, y0), (x1t, y0)], fill=(255, 255, 255, 255), width=4)
    d.line([(x0t, y0 + 2), (x1t, y0 + 2)], fill=(236, 243, 252, 120), width=2)
    d.line([(x0b + 6, y1 - 1), (x1b - 6, y1 - 1)], fill=(158, 172, 190, 210), width=4)
    # chants latéraux : deux traits verticaux qui font lire « bloc » et pas « ligne »
    d.line([(x0t, y0), (x0b, y1)], fill=(196, 208, 224, 150), width=3)
    d.line([(x1t, y0), (x1b, y1)], fill=(196, 208, 224, 150), width=3)
    plate = plate.filter(ImageFilter.GaussianBlur(0.6))

    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((x0b + bot_w * 0.05, y1 - height * 0.25,
                                x1b - bot_w * 0.05, y1 + height * 1.1),
                               fill=(78, 88, 104, 78))
    sh = sh.filter(ImageFilter.GaussianBlur(max(int(width * 0.02), 10)))

    canvas = Image.alpha_composite(canvas.convert("RGBA"), sh)
    return Image.alpha_composite(canvas, plate).convert("RGB")


def _reflection(subject: Image.Image) -> Image.Image:
    """Reflet de la monture dans la dalle : retournée, estompée, fanée vers le bas."""
    refl = subject.transpose(Image.FLIP_TOP_BOTTOM)
    refl = refl.resize((refl.width, int(refl.height * 0.5)), Image.LANCZOS)
    refl.putalpha(refl.split()[3].point(lambda v: int(v * 0.20)))
    refl = refl.filter(ImageFilter.GaussianBlur(4))
    fade = Image.new("L", refl.size, 0)
    fd = ImageDraw.Draw(fade)
    for i in range(refl.size[1]):
        fd.line([(0, i), (refl.size[0], i)], fill=int(255 * (1 - i / refl.size[1]) ** 1.4))
    refl.putalpha(ImageChops.multiply(refl.split()[3], fade))
    return refl


# --------------------------------------------------------------------------- rendu

def render(src: Image.Image, stem: str = "") -> tuple[Image.Image, str]:
    """Rend la photo sur son socle. Retourne (image, mode) où mode ∈ {détouré, planche}."""
    mask = cut(src)
    bbox = mask.getbbox()
    if not bbox:
        raise ValueError("détourage impossible")

    sw, sh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    scale = min(SIZE[0] * (1 - 2 * MARGIN) / sw, SIZE[1] * (1 - 2 * MARGIN) / sh, 1.0)
    nw, nh = int(sw * scale), int(sh * scale)

    canvas = Image.new("RGB", SIZE, SET_RGB)
    x, y = (SIZE[0] - nw) // 2, int(SIZE[1] * 0.44 - nh / 2)
    bench_h = max(int(SIZE[1] * BENCH_H_FRAC), 46)

    if is_broken(mask) or stem in PLAN_CHE:
        # planche : la photo entière, fond crème effacé, posée sur le socle — rien n'est découpé
        flat = _flatten(src)
        pad = int(max(sw, sh) * 0.03)
        box = (max(bbox[0] - pad, 0), max(bbox[1] - pad, 0),
               min(bbox[2] + pad, src.width), min(bbox[3] + pad, src.height))
        crop = flat.crop(box)
        sc = min(SIZE[0] * (1 - 2 * MARGIN) / crop.width, SIZE[1] * (1 - 2 * MARGIN) / crop.height, 1.0)
        plate = crop.resize((int(crop.width * sc), int(crop.height * sc)), Image.LANCZOS)
        px_, py_ = (SIZE[0] - plate.width) // 2, int(SIZE[1] * 0.44 - plate.height / 2)
        # le bas de la monture, pas le bas du cadre : le socle doit toucher la matière
        base = py_ + int((bbox[3] - box[1]) * sc) - int(bench_h * 0.25)
        canvas = _bench(canvas, SIZE[0] // 2, base, int(plate.width * 1.06), bench_h)
        canvas.paste(plate, (px_, py_))
        return canvas, "planche"

    subject = src.convert("RGBA").crop(bbox).resize((nw, nh), Image.LANCZOS)
    subject.putalpha(mask.crop(bbox).resize((nw, nh), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2)))
    base = y + nh - int(nh * 0.02)

    canvas = _bench(canvas, SIZE[0] // 2, base, int(nw * 1.06), bench_h)
    canvas = canvas.convert("RGBA")
    canvas.alpha_composite(_reflection(subject), (x, base + 6))
    canvas.alpha_composite(subject, (x, y))
    return canvas.convert("RGB"), "détouré"


def _flatten(src: Image.Image) -> Image.Image:
    """Fond crème → blanc du set, sans toucher au produit (substitution pixel à pixel)."""
    img = src.convert("RGB")
    w, h = img.size
    corners = [img.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    cream = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    px = img.load()
    for yy in range(h):
        for xx in range(w):
            r, g, b = px[xx, yy]
            d = max(abs(r - cream[0]), abs(g - cream[1]), abs(b - cream[2]))
            if d <= 9:
                px[xx, yy] = SET_RGB
            elif d < 20:
                t = (d - 9) / 11
                px[xx, yy] = (int(SET_RGB[0] + (r - SET_RGB[0]) * t),
                              int(SET_RGB[1] + (g - SET_RGB[1]) * t),
                              int(SET_RGB[2] + (b - SET_RGB[2]) * t))
    return img


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    files = sorted(FRAMES.glob("monture-*.webp"))
    if args.sample:
        files = files[: args.sample]
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    done = failed = 0
    modes = {"détouré": 0, "planche": 0}
    for p in files:
        if args.check:
            print(f"{p.name:34} {p.stat().st_size // 1024} Ko")
            continue
        try:
            out, mode = render(Image.open(p), p.stem)
        except Exception as exc:                                  # noqa: BLE001
            print(f"  ✗ {p.name} : {exc}")
            failed += 1
            continue
        modes[mode] += 1
        tmp = p.with_suffix(".tmp.webp")
        out.save(tmp, "WEBP", quality=QUALITY, method=6)
        data = tmp.read_bytes()
        tmp.unlink()
        (args.out / p.name if args.out else p).write_bytes(data)
        done += 1
    if not args.check:
        print(f"{done} fichier(s) écrit(s), {failed} échec(s) — "
              f"{modes['détouré']} détouré(s), {modes['planche']} en planche")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
