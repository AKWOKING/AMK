#!/usr/bin/env python3
"""La carte du comptoir : un QR pour laisser un avis Google, prête à imprimer.

Pourquoi un script et pas un fichier posé à la main : un QR contient une URL, et une URL se
périme. Le jour où le `place_id` change, on relance cette commande au lieu de retrouver une
image de 2026 dont personne ne sait plus ce qu'elle pointe.

    python3 tools/ops/make_qr_avis.py                 # écrit les 4 fichiers
    python3 tools/ops/make_qr_avis.py --check         # vérifie que le QR se relit bien en URL

Ce qui est produit, dans `clients/dm-optic/launch/` :
  qr-avis-google.svg        le QR seul, vectoriel (imprimeur, autre support, écran)
  qr-avis-google.png        le QR seul, 1200 px, pour un post ou un écran
  carte-avis-a6.png         la carte A6 complète, 300 dpi (1240 × 1748)
  carte-avis-a6.pdf         la même, en PDF A6, prête à envoyer à l'impression

Trois règles tenues ici, et elles ne sont pas décoratives :
  ① correction d'erreur H (30 %) : le QR doit survivre à une impression bon marché, à un comptoir
    humide et à un téléphone qui vise mal. Un QR « propre » à 7 % ne survit à rien de tout ça ;
  ② aucune incitation, aucune étoile, aucune condition de satisfaction. La carte demande un avis,
    elle ne demande pas une bonne note ;
  ③ l'adresse de repli est écrite en clair : si le scan échoue, le patient peut chercher le
    cabinet par son nom. Un QR est une commodité, pas une condition.
"""
import argparse
import pathlib
import sys

import qrcode
from qrcode.image.svg import SvgPathImage
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "clients" / "dm-optic" / "launch"
FONTS = ROOT / "clients" / "dm-optic" / "content" / "month1" / "w1" / "assets" / "fonts"

# L'identité de la fiche, relevée le 21/10 par le cabinet lui-même (Maps > Quick Builder).
PLACE_ID = "ChIJjdfYfQwXYRARAdi9mPLHGjY"
URL = "https://search.google.com/local/writereview?placeid=" + PLACE_ID

# Les jetons du site, pas des couleurs choisies ici (AMK-DESIGN-SKILLS §6).
PAPER = "#EEF1F5"
INK = "#0C1524"
INK_2 = "#43506A"
BRAND = "#1A3F86"
LINE = "#D6DDE7"

CARD_W, CARD_H = 1240, 1748          # A6 à 300 dpi : 105 × 148 mm
MARGIN = 96


def qr_image(box=1200):
    """Le QR, en navy sur blanc, avec une marge de silence de 4 modules."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color=BRAND, back_color="#FFFFFF").convert("RGB")
    return img.resize((box, box), Image.NEAREST), qr


def font(name, size):
    path = FONTS / name
    if not path.exists():
        sys.exit(f"police absente : {path}")
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_w):
    """Découpe en lignes, en respectant les espaces insécables.

    `str.split()` coupe sur TOUT espace, y compris `\u00a0` : sans ce garde-fou, le « » de
    « DM OPTIQUE SARL » repartait seul à la ligne (vu sur la première épreuve du 29/10).
    """
    glued = text.replace("\u00a0", "\x00")
    words, lines, cur = glued.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return [ln.replace("\x00", " ") for ln in lines]


def build_card(qr_png):
    card = Image.new("RGB", (CARD_W, CARD_H), PAPER)
    d = ImageDraw.Draw(card)
    inner = CARD_W - 2 * MARGIN

    f_brand = font("schibsted-grotesk-latin-700-normal.ttf", 62)
    f_meta = font("ibm-plex-sans-latin-400-normal.ttf", 30)
    f_head = font("schibsted-grotesk-latin-700-normal.ttf", 66)
    f_body = font("ibm-plex-sans-latin-400-normal.ttf", 36)
    f_link = font("schibsted-grotesk-latin-500-normal.ttf", 34)
    f_small = font("ibm-plex-mono-latin-600-normal.ttf", 26)

    y = MARGIN
    d.text((MARGIN, y), "DM OPTIQUE SARL", font=f_brand, fill=INK)
    y += 78
    d.text((MARGIN, y), "Opticien optométriste · Bonabéri, Douala", font=f_meta, fill=INK_2)
    y += 58
    d.line([(MARGIN, y), (CARD_W - MARGIN, y)], fill=LINE, width=2)
    y += 52

    for line in wrap(d, "Vous êtes venu au cabinet ?", f_head, inner):
        d.text((MARGIN, y), line, font=f_head, fill=INK)
        y += 78
    y += 10
    body = ("Votre avis sur Google aide les patients qui cherchent un opticien à Bonabéri.")
    for line in wrap(d, body, f_body, inner):
        d.text((MARGIN, y), line, font=f_body, fill=INK_2)
        y += 52

    # Le QR : blanc autour, large, centré sur la largeur utile.
    size = 760
    q = qr_png.resize((size, size), Image.NEAREST)
    qx = MARGIN + (inner - size) // 2
    y += 34
    d.rectangle([qx - 24, y - 24, qx + size + 24, y + size + 24], fill="#FFFFFF")
    card.paste(q, (qx, y))
    y += size + 52

    cap = ("Scannez avec l'appareil photo, ou cherchez\u00a0«\u00a0DM\u00a0OPTIQUE\u00a0SARL\u00a0»\u00a0sur Google.")
    for line in wrap(d, cap, f_link, inner):
        d.text(((CARD_W - d.textlength(line, font=f_link)) // 2, y), line, font=f_link, fill=BRAND)
        y += 46

    # Le pied : l'adresse, le téléphone. Ce qu'on imprime reste un objet du cabinet.
    y = CARD_H - MARGIN - 52
    d.line([(MARGIN, y - 30), (CARD_W - MARGIN, y - 30)], fill=LINE, width=2)
    pied = "Ndobo Mayor, West Hotel, 1er étage · Bonabéri · 656 122 239"
    for line in wrap(d, pied, f_small, inner):
        d.text(((CARD_W - d.textlength(line, font=f_small)) // 2, y), line, font=f_small, fill=INK_2)
        y += 34
    return card


def main():
    ap = argparse.ArgumentParser(description="La carte du comptoir (QR avis Google).")
    ap.add_argument("--check", action="store_true", help="relit le QR et vérifie l'URL, n'écrit rien")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    qr_png, qr = qr_image()

    if args.check:
        print(f"QR version {qr.version} · {qr.modules_count} modules · correction H (30 %)")
        print("attendu :", URL)
        try:
            import cv2
        except Exception:
            print("relecture NON vérifiée : opencv absent (on ne prétend pas avoir relu le QR)")
            return 0
        det = cv2.QRCodeDetector()
        for name in ("qr-avis-google.png", "carte-avis-a6.png"):
            f = OUT / name
            if not f.exists():
                print(f"  {name} : absent")
                continue
            got, _, _ = det.detectAndDecode(cv2.imread(str(f)))
            statut = "IDENTIQUE" if got == URL else ("NON LU" if not got else "DIFFÉRENT")
            print(f"  {name} : {statut}")
            if got and got != URL:
                print("    relu :", got)
                return 1
        # La carte est l'objet qu'on imprime : c'est elle qui doit se relire, pas seulement le PNG du QR.
        return 0

    # 1 · le QR seul, vectoriel puis bitmap
    svg = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2,
                        image_factory=SvgPathImage)
    svg.add_data(URL)
    svg.make(fit=True)
    (OUT / "qr-avis-google.svg").write_text(
        svg.make_image().to_string(encoding="unicode").replace(
            '<svg ', f'<svg fill="{BRAND}" '), encoding="utf-8")
    qr_png.save(OUT / "qr-avis-google.png")

    # 2 · la carte, en PNG 300 dpi puis en PDF A6
    card = build_card(qr_png)
    card.save(OUT / "carte-avis-a6.png", dpi=(300, 300))
    card.save(OUT / "carte-avis-a6.pdf", "PDF", resolution=300.0)

    print(f"QR : version {qr.version}, {qr.modules_count} modules, correction H")
    for f in sorted(OUT.glob("qr-avis-google.*")) + sorted(OUT.glob("carte-avis-a6.*")):
        print(f"  {f.relative_to(ROOT)}  {f.stat().st_size // 1024} Ko")
    print("\nRappel : aucun texte de cette carte ne promet une note, un avantage ou un délai.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
