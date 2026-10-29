#!/usr/bin/env python3
"""Les deux pièces du 31/10 pour DM OPTIQUE : la facture soldée et le reçu du solde.

Pourquoi un générateur et pas une capture de l'outil : `ops/amk-factures-pwa/` est une PWA dont les
données vivent dans le `localStorage` du téléphone de King. Elle ne se pilote pas à distance, et ce
dépôt n'a pas de navigateur pour l'imprimer. Ce script reprend donc **les données et la mise en page
de l'outil** (mêmes chiffres, mêmes blocs, même palette) et sort un A4 propre à 300 dpi.

    python3 tools/facture/make_solde_dm.py

Ce qui est produit, dans `clients/dm-optic/launch/` :

  FACTURE-SOLDE-AMK-2026-001.pdf   la facture, soldée, à archiver côté client
  RECU-SOLDE-AMK-2026-001-R2.pdf   le reçu du solde, en 2 exemplaires sur une seule feuille (à découper)
  *.png                            aperçus, si le PDF ne passe pas sur WhatsApp

Trois choses que ce script ne fait volontairement PAS :

1. **Il n'écrit aucun RCCM.** L'outil imprime `RC / RCCM : Non applicable (personne physique sous
   NIU)` par défaut ; c'est une affirmation que rien dans le dossier ne prouve (`ops/ADMIN-FISCAL-
   AMK-2026-10-22.md` §2 dit l'inverse : le RCCM est une mention obligatoire, toujours manquante).
   Tant qu'il manque, la ligne est absente : une ligne absente ne se retourne pas contre nous, une
   ligne fausse si.
2. **Il n'écrit ni « conforme DGI », ni « facture normalisée », ni taux de TVA.** Le régime fiscal
   d'AMK n'est pas tranché (SPEC-FACTURATION §0 et §5). La ligne TVA s'ajoutera le jour où il l'est.
3. **Il n'invente pas le NIU du client.** `DM.niu` est vide dans l'outil ; il reste vide ici.

Les montants : 150 000 facturés, 75 000 reçus le 13/10 (espèces), 75 000 reçus le 31/10, reste 0.
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "clients" / "dm-optic" / "launch"
FONTS = ROOT / "clients" / "dm-optic" / "content" / "month1" / "w1" / "assets" / "fonts"

PAPER, INK, INK_2, LINE, ACCENT = "#FFFFFF", "#0F172A", "#56627A", "#DCE2EC", "#B45309"
NAVY, GOLD, GOLD_DARK, OK = "#0F172A", "#FCD34D", "#D08A0B", "#166534"
SOFT, GREY = "#F4F6FA", "#9AA6BB"
W, H = 2480, 3508              # A4 à 300 dpi
M = 240                        # marge

DEVIS = 150000
ACOMPTE = {"date": "13 octobre 2026", "amount": 75000, "method": "espèces"}
SOLDE = {"date": "31 octobre 2026", "amount": 75000}
FACTURE_NO = "AMK-2026-001"
FACTURE_DATE = "23 octobre 2026"
FACTURE_DUE = "6 novembre 2026"
RECU_NO = FACTURE_NO + "-R2"
EN_LETTRES = "soixante-quinze mille"
EMETTEUR = {
    "legal": "Akwo Makembe King Guerschon",
    "name": "AMK Web & Digital Solutions",
    "addr": "Deido, Douala (Cameroun)",
    "phone": "+237 677 78 96 31",
    "email": "akwo.king.dev@gmail.com",
    "web": "amk-cm.vercel.app",
    "niu": "P030218642934H",
    "momo": "677 78 96 31",
    "om": "692 89 07 47",
    "bank": "Afriland First Bank",
    "holder": "AKWO MAKEMBE KING",
    "acc": "00069-00000097794-90",
}
CLIENT = {
    "name": "DM OPTIQUE SARL",
    "contact": "M. Domche Noumbi",
    "addr": "Immeuble West Hotel, Ndobo Mayor",
    "addr2": "Bonabéri, Douala IV",
    "phone": "656 12 22 39",
}
LIGNES = [
    ("Création du site vitrine bilingue (français + anglais)", 1, 100000),
    ("Configuration Facebook et TikTok (comptes au nom du cabinet, "
     "CTA WhatsApp, premier contenu)", 1, 50000),
]
NOTE = ("Acompte de 75 000 FCFA reçu le 13/10/2026 (espèces). Solde de 75 000 FCFA reçu le "
        "31/10/2026. Site, fiche Google, pages Facebook et TikTok en ligne.")


def money(n):
    return f"{n:,}".replace(",", " ") + " FCFA"


def font(name, size):
    p = FONTS / name
    if not p.exists():
        sys.exit(f"police absente : {p}")
    return ImageFont.truetype(str(p), size)


def wrap(draw, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def logo(img, x, y, side):
    """La marque de l'outil, redessinée : carré nuit, cercle ambre, triangle ouvert, trois points."""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + side, y + side], radius=int(side * 0.20), fill=NAVY)
    c = side / 2
    r = side * 0.31
    d.ellipse([x + c - r, y + c - r, x + c + r, y + c + r], outline=GOLD_DARK, width=max(2, side // 30))
    tri = [(x + c, y + c - r * 0.92), (x + c - r * 0.80, y + c + r * 0.60),
           (x + c + r * 0.80, y + c + r * 0.60)]
    d.line(tri + [tri[0]], fill=GOLD, width=max(3, side // 12), joint="curve")
    dot = max(2, side // 18)
    for px, py in tri:
        d.ellipse([px - dot, py - dot, px + dot, py + dot], fill="#F59E0B")


def stamp(img, xy, text, size, angle=9, pad=34, weight=10):
    """Le tampon, posé sur un calque : il se superpose sans effacer ce qu'il recouvre."""
    f = font("schibsted-grotesk-latin-700-normal.ttf", size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bw = int(tmp.textlength(text, font=f)) + 2 * pad
    bh = int(size * 1.55)
    box = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    db = ImageDraw.Draw(box)
    db.rounded_rectangle([weight // 2, weight // 2, bw - weight // 2 - 1, bh - weight // 2 - 1],
                         radius=14, outline=OK + "FF", width=weight)
    db.text((pad, int(size * 0.22)), text, font=f, fill=OK + "FF")
    box = box.rotate(angle, expand=True, resample=Image.BICUBIC)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    layer.alpha_composite(box, (int(xy[0]), int(xy[1])))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def dotted(d, x1, x2, y, fill=GREY, step=22, dash=10, width=3):
    x = x1
    while x < x2:
        d.line([(x, y), (min(x + dash, x2), y)], fill=fill, width=width)
        x += step


# ------------------------------------------------------------------------------------------------
def page_facture(g=1.0):
    """g étire les respirations verticales pour remplir la page ; le contenu, lui, ne bouge pas."""
    gap = lambda v: int(v * g)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_disp = font("schibsted-grotesk-latin-700-normal.ttf", 96)
    f_h1 = font("schibsted-grotesk-latin-700-normal.ttf", 88)
    f_h2 = font("schibsted-grotesk-latin-700-normal.ttf", 50)
    f_body = font("ibm-plex-sans-latin-400-normal.ttf", 36)
    f_bold = font("schibsted-grotesk-latin-500-normal.ttf", 36)
    f_lbl = font("ibm-plex-sans-latin-400-normal.ttf", 27)
    f_small = font("ibm-plex-sans-latin-400-normal.ttf", 31)
    inner = W - 2 * M

    # en-tête
    side = 210
    logo(img, M, M, side)
    d.text((M + side + 46, M + 8), "AMK", font=f_disp, fill=INK)
    d.text((M + side + 50, M + 128), EMETTEUR["name"], font=f_small, fill=INK_2)
    d.text((M + side + 50, M + 174), "Web & digital · Douala", font=f_small, fill=INK_2)

    xr = W - M
    for txt, fnt, fill, dy in [("FACTURE", f_h1, INK, 0),
                               (f"N° {FACTURE_NO}", f_h2, INK, 112),
                               (f"Date : {FACTURE_DATE}", f_small, INK_2, 188),
                               (f"Échéance : {FACTURE_DUE}", f_small, INK_2, 234)]:
        d.text((xr - d.textlength(txt, font=fnt), M + dy), txt, font=fnt, fill=fill)

    y = M + side + gap(80)
    d.rectangle([M, y, W - M, y + 8], fill=ACCENT)
    y += gap(96)

    # parties
    col = (inner - 140) // 2
    d.text((M, y), "ÉMETTEUR", font=f_lbl, fill=INK_2)
    d.text((M + col + 140, y), "FACTURÉ À", font=f_lbl, fill=INK_2)
    y += 60
    y0 = y
    left = [EMETTEUR["legal"], EMETTEUR["name"], EMETTEUR["addr"], EMETTEUR["phone"],
            EMETTEUR["email"], EMETTEUR["web"], f"NIU : {EMETTEUR['niu']}"]
    right = [CLIENT["name"], CLIENT["contact"], CLIENT["addr"], CLIENT["addr2"],
             f"Tél. : {CLIENT['phone']}"]
    for rows, x in ((left, M), (right, M + col + 140)):
        yy = y0
        for i, txt in enumerate(rows):
            bold = i == 0
            for line in wrap(d, txt, f_bold if bold else f_body, col):
                d.text((x, yy), line, font=f_bold if bold else f_body,
                       fill=INK if bold else INK_2)
                yy += 52
    y = max(y0 + 52 * len(left), y0 + 52 * len(right)) + gap(56)

    # objet
    d.text((M, y), "OBJET", font=f_lbl, fill=INK_2)
    d.text((M + 150, y - 10), "Création du site vitrine et ouverture des comptes sociaux du cabinet",
           font=f_body, fill=INK)
    y += gap(96)

    # tableau des prestations
    d.rounded_rectangle([M, y, W - M, y + 74], radius=6, fill=SOFT)
    for cx, txt, al in [(M + 24, "Désignation", "l"), (M + inner - 740, "Qté", "r"),
                        (M + inner - 450, "P.U.", "r"), (M + inner - 24, "Montant", "r")]:
        s = txt.upper()
        x = cx if al == "l" else cx - d.textlength(s, font=f_lbl)
        d.text((x, y + 22), s, font=f_lbl, fill=INK_2)
    y += 74
    for desc, qty, price in LIGNES:
        lines = wrap(d, desc, f_body, inner - 820)
        h = 36 + 52 * len(lines)
        d.line([(M, y), (W - M, y)], fill=LINE, width=2)
        yy = y + 36
        for line in lines:
            d.text((M + 24, yy), line, font=f_body, fill=INK)
            yy += 52
        for cx, txt, fnt in [(M + inner - 740, str(qty), f_body),
                             (M + inner - 450, money(price), f_body)]:
            d.text((cx - d.textlength(txt, font=fnt), y + 40), txt, font=fnt, fill=INK)
        amt = money(qty * price)
        d.text((M + inner - 24 - d.textlength(amt, font=f_bold), y + 40), amt,
               font=f_bold, fill=INK)
        y += h
    d.line([(M, y), (W - M, y)], fill=INK, width=3)

    # totaux
    y += gap(54)
    x_lbl = W - M - 960
    for lbl, val in [("Total facture", money(DEVIS)),
                     (f"Acompte reçu le {ACOMPTE['date']}", "− " + money(ACOMPTE["amount"])),
                     (f"Solde reçu le {SOLDE['date']}", "− " + money(SOLDE["amount"]))]:
        d.text((x_lbl, y), lbl, font=f_body, fill=INK_2)
        d.text((W - M - d.textlength(val, font=f_body), y), val, font=f_body, fill=INK)
        y += 60
    y += 16
    d.rounded_rectangle([x_lbl - 34, y, W - M, y + 112], radius=8, fill=SOFT)
    d.text((x_lbl, y + 30), "Reste à payer", font=f_h2, fill=INK)
    v = money(0)
    d.text((W - M - 24 - d.textlength(v, font=f_h2), y + 30), v, font=f_h2, fill=OK)
    y += 112 + gap(86)

    # journal des encaissements
    d.rounded_rectangle([M, y, W - M, y + 68], radius=6, fill=SOFT)
    d.text((M + 24, y + 21), "PAIEMENTS REÇUS", font=f_lbl, fill=INK_2)
    y += 68
    for i, (date, obj, amount) in enumerate([(ACOMPTE["date"], "Acompte à la commande",
                                             ACOMPTE["amount"]),
                                            (SOLDE["date"], "Solde à la livraison",
                                             SOLDE["amount"])]):
        if i:
            d.line([(M, y), (W - M, y)], fill=LINE, width=2)
        d.text((M + 24, y + 26), date, font=f_body, fill=INK)
        d.text((M + 620, y + 26), obj, font=f_body, fill=INK_2)
        v = money(amount)
        d.text((W - M - 24 - d.textlength(v, font=f_bold), y + 26), v, font=f_bold, fill=INK)
        y += 78
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    y += gap(92)

    # règlement (gauche) + signature (droite)
    d.text((M, y), "RÈGLEMENT", font=f_lbl, fill=INK_2)
    yy = y + 54
    for row in [f"MTN MoMo : {EMETTEUR['momo']}", f"Orange Money : {EMETTEUR['om']}",
                f"{EMETTEUR['bank']} · Compte {EMETTEUR['acc']}",
                f"Titulaire : {EMETTEUR['holder']}"]:
        d.text((M, yy), row, font=f_body, fill=INK_2)
        yy += 54
    yy += 40
    for line in wrap(d, NOTE, f_small, inner - 880):
        d.text((M, yy), line, font=f_small, fill=INK_2)
        yy += 44

    bx, by, bw, bh = W - M - 640, y, 640, 300
    d.rectangle([bx, by, bx + bw, by + bh], outline=LINE, width=3)
    s = "Cachet et signature"
    d.text((bx + (bw - d.textlength(s, font=f_lbl)) / 2, by + bh - 62), s, font=f_lbl, fill=INK_2)
    img = stamp(img, (bx + 96, by + 6), "PAYÉ", 120, pad=44)
    d = ImageDraw.Draw(img)
    bottom = max(yy, by + bh)

    # pied
    foot = (f"{EMETTEUR['name']} · {EMETTEUR['phone']} · {EMETTEUR['email']} · "
            f"NIU {EMETTEUR['niu']}")
    d.line([(M, H - M - 70), (W - M, H - M - 70)], fill=LINE, width=2)
    d.text(((W - d.textlength(foot, font=f_small)) / 2, H - M - 42), foot,
           font=f_small, fill=INK_2)
    return img, bottom


# ------------------------------------------------------------------------------------------------
def receipt_block(img, top, height, copy_label, s=1.0):
    """Un reçu complet dans une bande de hauteur `height` ; `s` étire les respirations."""
    gap = lambda v: int(v * s)
    d = ImageDraw.Draw(img)
    f_disp = font("schibsted-grotesk-latin-700-normal.ttf", 66)
    f_h = font("schibsted-grotesk-latin-700-normal.ttf", 58)
    f_big = font("schibsted-grotesk-latin-700-normal.ttf", 64)
    f_body = font("ibm-plex-sans-latin-400-normal.ttf", 32)
    f_bold = font("schibsted-grotesk-latin-500-normal.ttf", 32)
    f_lbl = font("ibm-plex-sans-latin-400-normal.ttf", 24)
    f_small = font("ibm-plex-sans-latin-400-normal.ttf", 28)
    inner = W - 2 * M
    y = top

    side = 140
    logo(img, M, y, side)
    d.text((M + side + 34, y + 4), "AMK", font=f_disp, fill=INK)
    d.text((M + side + 36, y + 88), EMETTEUR["name"], font=f_small, fill=INK_2)
    xr = W - M
    for txt, fnt, fill, dy in [("REÇU DE PAIEMENT", f_h, INK, 0),
                               (f"N° {RECU_NO}", f_bold, INK, 78),
                               (f"Date : {SOLDE['date']}", f_small, INK_2, 124)]:
        d.text((xr - d.textlength(txt, font=fnt), y - 4 + dy), txt, font=fnt, fill=fill)
    y += side + 46
    d.rectangle([M, y, W - M, y + 6], fill=ACCENT)
    y += gap(58)

    col = (inner - 110) // 2
    d.text((M, y), "ÉMETTEUR", font=f_lbl, fill=INK_2)
    d.text((M + col + 110, y), "REÇU DE", font=f_lbl, fill=INK_2)
    y += 46
    y0 = y
    for rows, x in (([EMETTEUR["legal"], EMETTEUR["name"], EMETTEUR["phone"],
                      f"NIU : {EMETTEUR['niu']}"], M),
                    ([CLIENT["name"], CLIENT["contact"], CLIENT["addr"], CLIENT["phone"]],
                     M + col + 110)):
        yy = y0
        for i, txt in enumerate(rows):
            bold = i == 0
            for line in wrap(d, txt, f_bold if bold else f_body, col):
                d.text((x, yy), line, font=f_bold if bold else f_body,
                       fill=INK if bold else INK_2)
                yy += 50
    y = y0 + 50 * 4 + gap(50)

    rows = [("Somme reçue", money(SOLDE["amount"]), "big"),
            ("Mode de paiement", None, "dots"),
            ("Facture", FACTURE_NO, None),
            ("Total de la facture", money(DEVIS), None),
            ("Reste à payer après ce paiement", money(0), None)]
    for i, (lbl, val, kind) in enumerate(rows):
        if i:
            d.line([(M, y - 8), (W - M, y - 8)], fill=LINE, width=2)
        d.text((M + 6, y + 12), lbl, font=f_bold if kind == "big" else f_body,
               fill=INK if kind == "big" else INK_2)
        if kind == "dots":
            dotted(d, W - M - 520, W - M - 8, y + 36)
            y += 80
            continue
        fv = f_big if kind == "big" else f_body
        d.text((W - M - 8 - d.textlength(val, font=fv), y + (0 if kind == "big" else 12)),
               val, font=fv, fill=INK if kind == "big" else INK_2)
        y += gap(96) if kind == "big" else gap(74)
    d.line([(M, y - 8), (W - M, y - 8)], fill=INK, width=3)
    y += gap(54)

    d.text((M, y), f"Arrêté le présent reçu à la somme de {EN_LETTRES} "
                   f"({money(SOLDE['amount'])}) pour le solde de la facture {FACTURE_NO}.",
           font=f_small, fill=INK_2)
    y += gap(104)

    bx, by, bw, bh = M, y, 600, 300
    d.rectangle([bx, by, bx + bw, by + bh], outline=LINE, width=3)
    s = "Cachet et signature"
    d.text((bx + (bw - d.textlength(s, font=f_lbl)) / 2, by + bh - 54), s, font=f_lbl, fill=INK_2)
    img = stamp(Image.fromarray if False else img, (bx + 70, by + 4), "FACTURE SOLDÉE", 46,
                angle=6, pad=28, weight=8)
    d = ImageDraw.Draw(img)

    # étiquette d'exemplaire + pied, posés en bas de la bande
    d.text((W - M - d.textlength(copy_label, font=f_lbl), top + height - 46),
           copy_label.upper(), font=f_lbl, fill=GREY)
    foot = f"{EMETTEUR['name']} · {EMETTEUR['phone']} · Merci de votre confiance."
    d.text((M, top + height - 42), foot, font=f_small, fill=INK_2)
    return img, by + bh


def page_recus():
    img = Image.new("RGB", (W, H), PAPER)
    gap = 170
    height = (H - 2 * M - gap) // 2
    target = M + height - 96
    _, b1 = receipt_block(Image.new("RGB", (W, H), PAPER), M, height, "", 1.0)
    _, b0 = receipt_block(Image.new("RGB", (W, H), PAPER), M, height, "", 0.0)
    s = max(0.5, 1.0 + (target - b1) / (b1 - b0)) if b1 > b0 else 1.0
    for i, lab in enumerate(("Exemplaire client", "Exemplaire AMK")):
        img, bot = receipt_block(img, M + i * (height + gap), height, lab, s)
    print(f"reçus : étirement s={s:.2f} · bloc à {bot} px, bas de bande à {M + height}")
    d = ImageDraw.Draw(img)
    yc = M + height + gap // 2
    dotted(d, M, W - M, yc, step=46, dash=26)
    s = "découper ici"
    f = font("ibm-plex-sans-latin-400-normal.ttf", 24)
    tw = d.textlength(s, font=f)
    d.rectangle([(W - tw) / 2 - 16, yc - 16, (W + tw) / 2 + 16, yc + 22], fill=PAPER)
    d.text(((W - tw) / 2, yc - 14), s, font=f, fill=GREY)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # deux passes : la seconde étire les respirations pour que le bloc signature tombe
    # à 120 px au-dessus du pied de page, sans jamais déplacer un chiffre.
    target = H - M - 190
    _, b1 = page_facture(1.0)
    _, b0 = page_facture(0.0)
    slack = b1 - b0
    g = 1.0 + max(0.0, (target - b1)) / slack if slack else 1.0
    facture, bottom = page_facture(g)
    recus = page_recus()

    pdf_f = OUT / "FACTURE-SOLDE-AMK-2026-001.pdf"
    pdf_r = OUT / "RECU-SOLDE-AMK-2026-001-R2.pdf"
    facture.save(pdf_f, "PDF", resolution=300.0, quality=95)
    recus.save(pdf_r, "PDF", resolution=300.0, quality=95)
    facture.save(OUT / "FACTURE-SOLDE-AMK-2026-001.png", "PNG", optimize=True)
    recus.save(OUT / "RECU-SOLDE-AMK-2026-001-R2.png", "PNG", optimize=True)
    print(f"étirement g={g:.2f} · contenu à {bottom} px sur {H}")
    for p in (pdf_f, pdf_r):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
