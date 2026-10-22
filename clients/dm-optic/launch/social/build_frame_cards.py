#!/usr/bin/env python3
"""
DM OPTIQUE SARL — cartes sociales à partir des VRAIES photos de montures.

Pourquoi ce script existe
-------------------------
Les 65 photos du cabinet (`hosting/previews/dmoptic/montures/*.webp`) sont photographiées
sur un fond crème (246, 236, 225) qui est presque exactement le chaud de la marque
(#F6EBE0). On peut donc composer une carte 1080x1350 où la photo se fond dans le fond,
sans cadre, sans ombre, sans faux décor : c'est la monture réelle, telle qu'elle est
au cabinet — pas une illustration.

Règle debout respectée : le texte colle à la photo (loi du 21/10 — « une image de stock
ne porte jamais “cette monture” »). Ici la monture EST celle du texte, elle est en stock,
et la légende le dit.

Usage :
    python3 build_frame_cards.py              # 3 cartes 1080x1350 (fil Facebook)
    python3 build_frame_cards.py --vertical   # 3 cartes 1080x1920 (TikTok, mode photo)
Sortie :
    clients/dm-optic/launch/social/cards/card-01-f01.jpg …
    clients/dm-optic/launch/social/cards/vertical/card-01-f01.jpg …
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SITE = os.path.join(ROOT, "hosting", "previews", "dmoptic")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
FONTS = "/tmp/fonts"  # woff2 -> ttf, généré à la volée si absent

W, H = 1080, 1350
BAND = 810                      # 1080 x 810 = le 4:3 exact des photos (1600x1200)
CREAM = (246, 236, 225)
INK = (12, 21, 36)
BRAND = (26, 63, 134)
WA = (11, 122, 62)
MUTED = (92, 84, 74)

CARDS = [
    {
        "frame": "F01",
        "file": "card-01-f01.jpg",
        "title": ["Une monture qu’on", "oublie qu’on porte."],
        "sub": "F01 · Ovale dorée — en stock au cabinet",
    },
    {
        "frame": "H08",
        "file": "card-02-h08.jpg",
        "title": ["De l’allure,", "sans la raideur."],
        "sub": "H08 · Double pont noir et doré — en stock",
    },
    {
        "frame": "E16",
        "file": "card-03-e16.jpg",
        "title": ["À sa taille.", "Solide pour la récré."],
        "sub": "E16 · Carrée bleue, taille enfant — en stock",
    },
]


def ttf(name):
    p = os.path.join(FONTS, name)
    if not os.path.exists(p):
        raise SystemExit(
            f"Police absente : {p}\n"
            "Génère-la : python3 - <<'PY'\nfrom fontTools.ttLib import TTFont\n"
            "TTFont('...woff2').save('/tmp/fonts/....ttf')\nPY"
        )
    return p


def spaced(draw, xy, text, font, fill, tracking=0):
    """Pillow ne sait pas interletter : on avance caractère par caractère."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def spaced_width(draw, text, font, tracking=0):
    return sum(draw.textlength(c, font=font) + tracking for c in text) - tracking


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build(card, frames):
    f = frames[card["frame"]]
    src = os.path.join(SITE, f["photos"][0].lstrip("/"))
    im = Image.open(src).convert("RGB")

    canvas = Image.new("RGB", (W, H), CREAM)
    # bande photo : la photo garde ses proportions (4:3) et son propre fond crème.
    # On la réduit de 6 % et on la centre : le fond de prise de vue (246,236,225) est
    # identique à CREAM, donc la marge est invisible — et aucune branche ne touche le bord.
    scale = 0.94
    pw, ph = int(W * scale), int(BAND * scale)
    canvas.paste(im.resize((pw, ph), Image.LANCZOS), ((W - pw) // 2, (BAND - ph) // 2))
    d = ImageDraw.Draw(canvas)

    kicker = ImageFont.truetype(ttf("ibm-plex-mono-latin-500-normal.ttf"), 21)
    title_f = ImageFont.truetype(ttf("schibsted-grotesk-latin-700-normal.ttf"), 74)
    sub_f = ImageFont.truetype(ttf("ibm-plex-sans-latin-400-normal.ttf"), 32)
    cta_f = ImageFont.truetype(ttf("ibm-plex-sans-latin-600-normal.ttf"), 29)
    micro_f = ImageFont.truetype(ttf("ibm-plex-mono-latin-500-normal.ttf"), 19)

    left = 84
    right_edge = W - 84

    # --- kicker + filet
    spaced(d, (left, 878), "DM OPTIQUE SARL  ·  BONABÉRI", kicker, BRAND, tracking=4.2)
    d.rectangle([left, 922, left + 56, 925], fill=BRAND)

    # --- titre (2 lignes max, contrôlé)
    y = 954
    for line in card["title"]:
        wpx = d.textlength(line, font=title_f)
        assert wpx <= right_edge - left, f"titre trop large ({wpx:.0f}px) : {line}"
        d.text((left, y), line, font=title_f, fill=INK)
        y += 84

    # --- sous-titre
    y += 16
    for line in wrap(d, card["sub"], sub_f, right_edge - left):
        d.text((left, y), line, font=sub_f, fill=MUTED)
        y += 42

    # --- pastille WhatsApp (bas)
    label = "WhatsApp 656 122 239"
    tw = d.textlength(label, font=cta_f)
    pad_x, hgt, rad = 30, 66, 33
    x0, y0 = left, 1214
    d.rounded_rectangle([x0, y0, x0 + tw + pad_x * 2, y0 + hgt], radius=rad, fill=WA)
    d.text((x0 + pad_x, y0 + (hgt - 34) / 2), label, font=cta_f, fill=(255, 255, 255))

    # --- ligne de preuve (bas droite, alignée à droite)
    proof = "Opticien optométriste · inscrit à l’ONOC"
    pw = d.textlength(proof, font=micro_f)
    d.text((right_edge - pw, y0 + 24), proof, font=micro_f, fill=MUTED)

    out = os.path.join(OUT, card["file"])
    canvas.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{os.path.relpath(out, ROOT):60s} {os.path.getsize(out)//1024:4d} Ko  {f['nom']}")
    return out


def build_vertical(card, frames):
    """1080x1920 — mode photo TikTok. Zones sûres : rien au-dessus de y=180 (barre),
    rien sous y=1650 (légende + boutons TikTok)."""
    f = frames[card["frame"]]
    src = os.path.join(SITE, f["photos"][0].lstrip("/"))
    im = Image.open(src).convert("RGB")

    Wv, Hv = 1080, 1920
    canvas = Image.new("RGB", (Wv, Hv), CREAM)
    canvas.paste(im.resize((Wv, BAND), Image.LANCZOS), (0, 300))
    d = ImageDraw.Draw(canvas)

    kicker = ImageFont.truetype(ttf("ibm-plex-mono-latin-500-normal.ttf"), 22)
    title_f = ImageFont.truetype(ttf("schibsted-grotesk-latin-700-normal.ttf"), 78)
    sub_f = ImageFont.truetype(ttf("ibm-plex-sans-latin-400-normal.ttf"), 34)
    cta_f = ImageFont.truetype(ttf("ibm-plex-sans-latin-600-normal.ttf"), 31)
    micro_f = ImageFont.truetype(ttf("ibm-plex-mono-latin-500-normal.ttf"), 20)

    left, right_edge = 84, Wv - 84
    spaced(d, (left, 196), "DM OPTIQUE SARL  ·  BONABÉRI", kicker, BRAND, tracking=4.2)
    d.rectangle([left, 240, left + 56, 243], fill=BRAND)

    y = 1180
    for line in card["title"]:
        wpx = d.textlength(line, font=title_f)
        assert wpx <= right_edge - left, f"titre trop large ({wpx:.0f}px) : {line}"
        d.text((left, y), line, font=title_f, fill=INK)
        y += 88

    y += 14
    for line in wrap(d, card["sub"], sub_f, right_edge - left):
        d.text((left, y), line, font=sub_f, fill=MUTED)
        y += 44

    label = "WhatsApp 656 122 239"
    tw = d.textlength(label, font=cta_f)
    pad_x, hgt = 30, 70
    x0, y0 = left, y + 34
    d.rounded_rectangle([x0, y0, x0 + tw + pad_x * 2, y0 + hgt], radius=hgt // 2, fill=WA)
    d.text((x0 + pad_x, y0 + (hgt - 36) / 2), label, font=cta_f, fill=(255, 255, 255))
    d.text((left, y0 + hgt + 26), "Opticien optométriste · inscrit à l’ONOC", font=micro_f, fill=MUTED)

    out = os.path.join(OUT, "vertical", card["file"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{os.path.relpath(out, ROOT):60s} {os.path.getsize(out)//1024:4d} Ko  {f['nom']}")
    return out


def build_cover(frames):
    """Couverture du 1er TikTok — 1080x1920, F24 en main (photo réelle), accroche du script.
    Zones sûres : la grille de profil de TikTok recadre au CENTRE (1080x1080 autour de y=1920/2),
    donc tout ce qui doit être lu reste entre y=420 et y=1500."""
    f = frames["F24"]
    src = os.path.join(SITE, f["photos"][0].lstrip("/"))
    im = Image.open(src).convert("RGB")
    Wv, Hv = 1080, 1920
    canvas = Image.new("RGB", (Wv, Hv), CREAM)
    # bande photo 4:3 (1080x810) posée à y=300 : la monture occupe le haut du carré central
    canvas.paste(im.resize((1080, 810), Image.LANCZOS), (0, 300))
    d = ImageDraw.Draw(canvas)

    kicker = ImageFont.truetype(ttf("ibm-plex-mono-latin-500-normal.ttf"), 22)
    title_f = ImageFont.truetype(ttf("schibsted-grotesk-latin-700-normal.ttf"), 84)
    sub_f = ImageFont.truetype(ttf("ibm-plex-sans-latin-400-normal.ttf"), 34)
    micro_f = ImageFont.truetype(ttf("ibm-plex-mono-latin-500-normal.ttf"), 20)

    left, right_edge = 84, Wv - 84
    spaced(d, (left, 196), "DM OPTIQUE SARL  ·  BONABÉRI", kicker, BRAND, tracking=4.2)
    d.rectangle([left, 240, left + 56, 243], fill=BRAND)

    y = 1180
    for line in ["Vous éloignez", "votre téléphone", "pour lire ?"]:
        wpx = d.textlength(line, font=title_f)
        assert wpx <= right_edge - left, f"titre trop large ({wpx:.0f}px) : {line}"
        d.text((left, y), line, font=title_f, fill=INK)
        y += 96

    y += 22
    for line in wrap(d, "F24 · carrée écaille — en stock au cabinet", sub_f, right_edge - left):
        d.text((left, y), line, font=sub_f, fill=MUTED)
        y += 44

    d.text((left, 1730), "Opticien optométriste · inscrit à l’ONOC · WhatsApp 656 122 239",
           font=micro_f, fill=MUTED)

    out = os.path.join(OUT, "tiktok-cover-f24.jpg")
    canvas.save(out, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"{os.path.relpath(out, ROOT):60s} {os.path.getsize(out)//1024:4d} Ko  couverture TikTok")
    return out


def main():
    if "--cover" in sys.argv:
        frames = {f["code"]: f for f in json.load(open(os.path.join(ROOT, "clients/dm-optic/site/frames.json"), encoding="utf-8"))}
        build_cover(frames)
        return
    vertical = "--vertical" in sys.argv
    os.makedirs(os.path.join(OUT, "vertical") if vertical else OUT, exist_ok=True)
    frames = {f["code"]: f for f in json.load(open(os.path.join(ROOT, "clients/dm-optic/site/frames.json"), encoding="utf-8"))}
    if not all(c["frame"] in frames for c in CARDS):
        raise SystemExit("monture absente de frames.json")
    for c in CARDS:
        (build_vertical if vertical else build)(c, frames)
    fmt = "1080x1920 (TikTok)" if vertical else "1080x1350 (Facebook)"
    print(f"\n{len(CARDS)} cartes — {fmt}, JPEG progressif.")


if __name__ == "__main__":
    main()
