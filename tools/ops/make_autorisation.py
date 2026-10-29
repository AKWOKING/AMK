#!/usr/bin/env python3
"""L'autorisation d'image, imprimable et signable — une page A4.

Pourquoi un fichier et pas un paragraphe dans le dossier : le message WhatsApp promet « la petite
autorisation à signer ». Un client qui signe lit ce qu'il signe ; un texte noyé dans un document de
travail ne se signe pas, il se survole.

    python3 tools/ops/make_autorisation.py            # écrit le PDF + un PNG d'aperçu

Ce qui est produit, dans `clients/dm-optic/launch/` :
  AUTORISATION-IMAGE-2026-10-29.pdf    A4, à envoyer sur son téléphone ou à imprimer sur place
  AUTORISATION-IMAGE-2026-10-29.png    aperçu, si le PDF ne passe pas sur WhatsApp

La même règle qu'à la carte du comptoir : aucune phrase qui promette quoi que ce soit en échange de la
signature. L'autorisation ne donne lieu à aucun paiement et n'engage à aucune prestation — c'est écrit,
et c'est ce qui la rend crédible.
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "clients" / "dm-optic" / "launch"
FONTS = ROOT / "clients" / "dm-optic" / "content" / "month1" / "w1" / "assets" / "fonts"

PAPER, INK, INK_2, LINE = "#FFFFFF", "#0C1524", "#43506A", "#C9D2DE"
W, H = 2480, 3508          # A4 à 300 dpi
M = 220


def font(name, size):
    p = FONTS / name
    if not p.exists():
        sys.exit(f"police absente : {p}")
    return ImageFont.truetype(str(p), size)


def wrap(draw, text, fnt, max_w):
    glued = text.replace("\u00a0", "\x00")
    out, cur = [], ""
    for word in glued.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return [l.replace("\x00", " ") for l in out]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    inner = W - 2 * M
    y = M

    f_brand = font("schibsted-grotesk-latin-700-normal.ttf", 46)
    f_h1 = font("schibsted-grotesk-latin-700-normal.ttf", 74)
    f_h2 = font("schibsted-grotesk-latin-700-normal.ttf", 46)
    f_body = font("ibm-plex-sans-latin-400-normal.ttf", 38)
    f_bold = font("schibsted-grotesk-latin-500-normal.ttf", 38)
    f_small = font("ibm-plex-sans-latin-400-normal.ttf", 30)

    d.text((M, y), "DM OPTIQUE SARL", font=f_brand, fill=INK)
    y += 62
    d.text((M, y), "Cabinet d'optique médicale · Ndobo Mayor, Bonabéri, Douala",
           font=f_small, fill=INK_2)
    y += 70
    d.line([(M, y), (W - M, y)], fill=LINE, width=3)
    y += 70

    d.text((M, y), "Autorisation de diffusion", font=f_h1, fill=INK)
    y += 96
    d.text((M, y), "d'image et de voix", font=f_h1, fill=INK)
    y += 110

    lines = [
        ("Je soussigné(e)", None),
        ("…………………………………………………………", None),
        ("né(e) le ……… / ……… / …………… , demeurant à …………………………………………………………,", None),
        ("", None),
        ("autorise DM OPTIQUE SARL, dont le siège est à Bonabéri (Douala IV), à fixer, reproduire et "
         "diffuser mon image et ma voix dans les enregistrements réalisés le ……… / ……… / …………… "
         "au cabinet.", None),
        ("", None),
        ("1 · Où les images peuvent paraître", f_h2),
        ("Les pages du cabinet sur Facebook, TikTok, Instagram et Google, et le site "
         "dmoptiquesarl.com. Nulle part ailleurs.", None),
        ("", None),
        ("2 · Ce qu'elles ne peuvent pas devenir", f_h2),
        ("Aucune utilisation publicitaire payante, aucune revente, aucune cession à un tiers, aucun "
         "montage qui me ferait dire une chose que je n'ai pas dite, aucune association à un "
         "témoignage de patient.", None),
        ("", None),
        ("3 · Combien de temps", f_h2),
        ("Sans limite de durée, pour les contenus publiés, sauf retrait de ma part (point 4).", None),
        ("", None),
        ("4 · Mon retrait", f_h2),
        ("Je peux retirer cet accord par un simple message écrit, à tout moment, sans avoir à me "
         "justifier. Les contenus qui me montrent sont alors retirés sous sept jours des pages "
         "listées au point 1, et les fichiers sources sont supprimés.", None),
        ("", None),
        ("5 · Ce qui ne peut pas arriver", f_h2),
        ("Aucune image de patient n'est prise ni utilisée. Aucun document administratif, aucune "
         "ordonnance, aucun prix, aucune marque de monture n'apparaît dans les contenus où je figure.",
         None),
        ("", None),
        ("6 · Aucune contrepartie", f_h2),
        ("Cette autorisation ne donne lieu à aucun paiement et ne m'engage à aucune prestation. Ce que "
         "je dis dans ces vidéos reste ma parole ; je peux demander à retirer une phrase avant "
         "publication, et elle sort.", None),
        ("", None),
        ("7 · Ce qui sera filmé, en clair", f_h2),
        ("Vous, en train d'expliquer votre travail : sept phrases, une minute en tout, deux prises. "
         "Puis vos mains sur l'appareil de mesure, une monture reposée sur le comptoir, la porte et "
         "l'escalier. Aucun patient. Vous voyez le montage avant publication, et "
         "vous pouvez retirer une phrase.", None),
        ("", None),
        ("Fait à …………………………………… , le ……… / ……… / ……………", None),
        ("", None),
        ("Signature : …………………………………………………", None),
    ]

    for text, style in lines:
        fnt = style or f_body
        if not text:
            y += 26
            continue
        for line in wrap(d, text, fnt, inner):
            d.text((M, y), line, font=fnt, fill=INK if style else INK_2)
            y += 60 if style else 54
        y += 6 if style else 0

    y = H - M - 34
    d.line([(M, y - 26), (W - M, y - 26)], fill=LINE, width=2)
    pied = ("Une fiche par personne filmée. À faire signer avant la première prise. "
            "Un message écrit suffit pour retirer l'accord.")
    for line in wrap(d, pied, f_small, inner):
        d.text((M, y), line, font=f_small, fill=INK_2)
        y += 40

    page.save(OUT / "AUTORISATION-IMAGE-2026-10-29.pdf", "PDF", resolution=300.0)
    page.save(OUT / "AUTORISATION-IMAGE-2026-10-29.png")
    for f in ("AUTORISATION-IMAGE-2026-10-29.pdf", "AUTORISATION-IMAGE-2026-10-29.png"):
        p = OUT / f
        print(f"  clients/dm-optic/launch/{f}  {p.stat().st_size // 1024} Ko")
    return 0


if __name__ == "__main__":
    sys.exit(main())
