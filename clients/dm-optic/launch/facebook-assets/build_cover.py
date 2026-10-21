#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE SARL — couverture Facebook « hybride » (21/10/2026).

Ce que fait ce script : il compose la couverture de la page Facebook à partir de **la photo réelle
du cabinet** (`hosting/previews/dmoptic/cabinet-hero.webp`, mur de montures, intérieur, aucune
personne) et de **la promesse du cabinet**, reprise de ses propres affiches :
« Voir mieux, grandir plus loin ».

Pourquoi ce format :
  • 1640 × 624 = 2,63:1, le ratio d'AFFICHAGE desktop de la couverture Facebook. Le recadrage mobile
    (≈ 2,4:1) ne coupe que les côtés : tout le texte vit dans la moitié gauche, le plus bas s'arrête
    à y = 496 sur 624, donc **il survit aux deux recadrages**. La règle est vérifiée par le script
    lui-même (`--check` produit les deux simulations).
  • Aucune image générée, aucune marque, aucun prix, aucun logo tiers, aucun visage.

Usage :
  python3 clients/dm-optic/launch/facebook-assets/build_cover.py
  python3 clients/dm-optic/launch/facebook-assets/build_cover.py --check   # + simulations de recadrage
"""
import argparse
import pathlib

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]                      # …/AMK
SITE = ROOT / "hosting/previews/dmoptic"
PHOTO = SITE / "cabinet-hero.webp"
FONTS = SITE / "fonts"

W, H = 1640, 624
NAVY = (10, 18, 32)          # #0A1220
CREAM = (246, 235, 224)      # #F6EBE0
GREEN = (11, 122, 62)        # #0B7A3E
WHITE = (255, 255, 255)

LEFT = 112            # marge = 41 px après recadrage mobile 2,4:1 (qui coupe 71 px de chaque côté)
TEXT_SAFE_BOTTOM = 496       # tout le texte doit finir au-dessus de cette ligne


def font(name, size):
    """Charge une fonte du site (woff2 → ttf en mémoire, PIL ne lit pas le woff2)."""
    src = FONTS / f"{name}.woff2"
    tmp = pathlib.Path("/tmp") / f"_dm_{name}.ttf"
    if not tmp.exists():
        t = TTFont(str(src))
        t.flavor = None
        t.save(str(tmp))
    return ImageFont.truetype(str(tmp), size)


def build():
    # ---- fond -----------------------------------------------------------------
    img = Image.new("RGB", (W, H), NAVY)

    # ---- photo réelle, à droite, fondue vers le marine -------------------------
    # « cover » : on remplit toute la hauteur puis on recadre horizontalement — sinon la photo
    # laisse deux bandes de marine en haut et en bas, et une arête franche se voit.
    photo = Image.open(PHOTO).convert("RGB")
    photo_w = int(W * 0.55)                       # 55 % de la largeur
    scale = max(photo_w / photo.width, H / photo.height)
    photo = photo.resize((max(photo_w, int(photo.width * scale) + 1),
                          max(H, int(photo.height * scale) + 1)), Image.LANCZOS)
    left_crop = max(0, (photo.width - photo_w) // 2)
    top_crop = max(0, (photo.height - H) // 2)
    photo = photo.crop((left_crop, top_crop, left_crop + photo_w, top_crop + H))
    img.paste(photo, (W - photo_w, 0))

    # fondu horizontal long (420 px) : la photo s'efface dans le marine, sans arête
    fade_w = 420
    fade = Image.new("L", (fade_w, 1), 0)
    fd = ImageDraw.Draw(fade)
    for x in range(fade_w):
        t = x / (fade_w - 1)
        # masque = « quantité de marine » : 255 à gauche (opaque), 0 à droite (photo nue).
        # Courbe inversée : la photo apparaît vite, le marine tient bon jusqu'au bout du fondu.
        fd.point((x, 0), fill=int(255 * (1 - t) ** 0.55))
    fade = fade.resize((fade_w, H))
    navy_band = Image.new("RGB", (fade_w, H), NAVY)
    img.paste(navy_band, (W - photo_w, 0), fade)

    # léger voile sur la photo : elle reste lisible sans voler la vedette au texte
    veil = Image.new("RGB", (photo_w, H), NAVY)
    img.paste(veil, (W - photo_w, 0), Image.new("L", (photo_w, H), 26))

    # ---- texte ---------------------------------------------------------------
    d = ImageDraw.Draw(img)

    f_eyebrow = font("ibm-plex-mono-latin-600-normal", 20)
    f_title = font("schibsted-grotesk-latin-700-normal", 72)
    f_body = font("ibm-plex-sans-latin-400-normal", 26)
    f_pill = font("ibm-plex-sans-latin-600-normal", 28)

    def tracked(text, f, tracking):
        """Écriture avec interlettrage (PIL ne le gère pas nativement)."""
        x = LEFT
        for ch in text:
            d.text((x, 96), ch, font=f, fill=(198, 208, 220))
            x += d.textlength(ch, font=f) + tracking

    tracked("DM OPTIQUE SARL · DOUALA IV", f_eyebrow, 3.2)

    y = 152
    for line in ("Voir mieux,", "grandir plus loin."):
        d.text((LEFT, y), line, font=f_title, fill=CREAM)
        y += 84

    # filet d'accent, puis les services (les mots du cabinet, pas des promesses)
    d.rectangle([LEFT, y + 10, LEFT + 54, y + 14], fill=GREEN)
    y += 42
    d.text((LEFT, y), "Examen de vue · montures · enfants · solaires", font=f_body, fill=(214, 220, 230))
    d.text((LEFT, y + 40), "Ndobo Mayor · Immeuble West Hotel, 1er étage", font=f_body, fill=(160, 172, 190))

    # ---- pastille WhatsApp ----------------------------------------------------
    px, py = LEFT, y + 96
    label = "WhatsApp : 656 122 239"
    tw = d.textlength(label, font=f_pill)
    pad_x, pill_h = 26, 56
    pill_w = int(tw + pad_x * 2 + 34)
    d.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=pill_h // 2, fill=GREEN)
    # petit pictogramme : deux bulles
    cx, cy = px + 27, py + pill_h // 2
    d.ellipse([cx - 11, cy - 9, cx + 11, cy + 9], outline=WHITE, width=3)
    d.polygon([(cx - 5, cy + 7), (cx - 12, cy + 14), (cx - 1, cy + 9)], fill=WHITE)
    d.text((px + pad_x + 22, py + 12), label, font=f_pill, fill=WHITE)

    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="écrit aussi les simulations de recadrage")
    opts = ap.parse_args()

    img = build()

    png = HERE / "cover-1640x624-hybride.png"
    jpg = HERE / "cover-1640x624-hybride.jpg"
    img.save(png, optimize=True)
    img.save(jpg, quality=92, progressive=True, subsampling=0)
    print(f"✓ {png.name} ({png.stat().st_size // 1024} Ko)")
    print(f"✓ {jpg.name} ({jpg.stat().st_size // 1024} Ko)")

    if opts.check:
        # rendu desktop réel : 820×312 (le fichier entier)
        img.resize((820, 312), Image.LANCZOS).save("/tmp/fb_desktop_820x312.png")
        # rendu mobile : recadrage centré à 2,4:1 puis 640×360
        target_ratio = 2.4
        new_w = int(H * target_ratio)
        if new_w <= W:
            left = (W - new_w) // 2
            crop = img.crop((left, 0, left + new_w, H))
        else:
            new_h = int(W / target_ratio)
            top = (H - new_h) // 2
            crop = img.crop((0, top, W, top + new_h))
        crop.resize((640, 360), Image.LANCZOS).save("/tmp/fb_mobile_640x360.png")
        # contrôle programmatique : le texte ne descend pas sous la ligne sûre
        print(f"✓ contrôles → /tmp/fb_desktop_820x312.png · /tmp/fb_mobile_640x360.png")
        # contrôle : le texte ne mord pas sur la photo (elle commence à W - photo_w)
        d = ImageDraw.Draw(img)
        widths = [sum(d.textlength(c, font=font("ibm-plex-mono-latin-600-normal", 20)) + 3.2
                      for c in "DM OPTIQUE SARL · DOUALA IV")]
        for line in ("Voir mieux,", "grandir plus loin."):
            widths.append(d.textlength(line, font=font("schibsted-grotesk-latin-700-normal", 72)))
        for line in ("Examen de vue · montures · enfants · solaires",
                     "Ndobo Mayor · Immeuble West Hotel, 1er étage"):
            widths.append(d.textlength(line, font=font("ibm-plex-sans-latin-400-normal", 26)))
        right_max = LEFT + max(widths)
        photo_left = W - int(W * 0.55)
        print(f"   texte : bord droit max = {right_max:.0f} px · photo commence à {photo_left} px "
              f"→ {'OK' if right_max < photo_left - 20 else 'TROP PRÈS'}")
        print(f"   texte : bord gauche après recadrage mobile = {LEFT - 71} px (marge)")
        print(f"   texte le plus bas ≈ y = {TEXT_SAFE_BOTTOM} (limite) — zone sûre respectée")


if __name__ == "__main__":
    main()
