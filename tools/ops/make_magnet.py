#!/usr/bin/env python3
"""L'aimant à prospects AMK — « Le contrôle présence en ligne », une page A4.

    pip install reportlab
    python3 tools/ops/make_magnet.py

Sortie : sales/lead-magnets/CONTROLE-PRESENCE-EN-LIGNE-2026-10-23.pdf

Pourquoi celui-là et pas un e-book (ruling King 23/10 : un opt-in, un seul) :
  - il se lit en 8 minutes et se vérifie sur son propre cabinet ;
  - il révèle un manque que le cabinet ne peut pas combler seul, sans jamais le lui dire ;
  - il ne contient **aucune statistique** : douze points de contrôle, oui/non, et ce que coûte un « non ».
    Aucun chiffre de marché n'entre ici — les sources secondaires sur les lead magnets se contredisent
    (5 % à 42 %), et un chiffre faux dans un aimant contamine la première impression (§1g).

Le mot-clé, le numéro et la phrase de suite sont en pied de page, une seule fois, pour un seul CTA.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "clients/dm-optic/content/month1/w1/assets/fonts"
OUT = ROOT / "sales/lead-magnets/CONTROLE-PRESENCE-EN-LIGNE-2026-10-23.pdf"

NAVY = HexColor("#0B1120")
AMBER = HexColor("#F59E0B")
AMBER_D = HexColor("#B45309")
SLATE = HexColor("#334155")
SLATE_L = HexColor("#94A3B8")
LINE = HexColor("#E2E8F0")
PAPER = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")

W, H = A4
M = 16 * mm

BLOCS = [
    ("A · Être trouvé", "vous existez, mais est-ce qu'on vous trouve ?", [
        ("Votre fiche Google",
         "Cherchez le nom exact du cabinet sur Google. La fiche apparaît-elle à droite, avec photo, horaires et bouton d'appel ?",
         "un patient qui cherche tape le nom, pas votre plaque"),
        ("Le même nom partout",
         "Nom, adresse et téléphone écrits à l'identique sur la fiche Google, la page Facebook et le site.",
         "trois versions = trois fiches = aucune bien classée"),
        ("Votre site est indexé",
         "Tapez site: votredomaine.com sur Google. Les pages du cabinet sortent-elles ?",
         "un site non indexé n'existe que pour ceux qui connaissent l'adresse"),
    ]),
    ("B · Être cru", "le patient compare, il ne vous croit pas sur parole", [
        ("Des photos réelles",
         "La façade, la salle d'examen, les montures : sont-elles vos photos, prises chez vous ?",
         "une image de catalogue se repère en trois secondes"),
        ("Des avis récents",
         "Ouvrez la fiche Google : combien d'avis, et datent-ils des six derniers mois ?",
         "un avis de 2021 ne rassure personne en 2026"),
        ("Des horaires exacts",
         "Les horaires de la fiche Google sont-ils ceux du panneau sur la porte ?",
         "un patient devant une porte fermée ne revient pas"),
    ]),
    ("C · Être joignable", "le trajet entre « je suis intéressé » et « je vous écris »", [
        ("Un numéro cliquable",
         "Sur le site, depuis un téléphone : le numéro lance-t-il l'appel d'un seul geste ?",
         "un numéro en image se recopie à la main, ou pas"),
        ("Un WhatsApp qui écrit d'avance",
         "Le bouton WhatsApp ouvre-t-il la conversation avec un message déjà rédigé ?",
         "un message vide = une conversation qui n'arrive jamais"),
        ("Une réponse le jour même",
         "Qui répond, et en combien de temps ? Écrivez-vous la règle quelque part ?",
         "la première réponse rapide gagne le rendez-vous"),
    ]),
    ("D · Mesurer", "ce qui n'est pas compté ne s'améliore pas", [
        ("Quatre chiffres par mois",
         "Appels depuis la fiche, itinéraires demandés, visites du site, conversations WhatsApp.",
         "sans ces quatre-là, on ne sait pas ce qui marche"),
        ("Une personne responsable",
         "Un nom, pas « l'équipe » : qui regarde ces chiffres le 1er du mois ?",
         "un chiffre que personne ne lit ne change rien"),
        ("Une page de bilan",
         "Un récapitulatif d'une page par mois : publié, obtenu, à faire.",
         "le bilan est ce qui transforme un site en outil"),
    ]),
]


def fonts() -> None:
    pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "ibm-plex-sans-latin-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("HeadB", str(FONTS / "schibsted-grotesk-latin-700-normal.ttf")))
    pdfmetrics.registerFont(TTFont("Head", str(FONTS / "schibsted-grotesk-latin-500-normal.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(FONTS / "ibm-plex-mono-latin-600-normal.ttf")))


def wrap(text: str, font: str, size: float, width: float) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build() -> None:
    fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Le contrôle présence en ligne — 12 points, 8 minutes")
    c.setAuthor("AMK")

    # en-tête
    c.setFillColor(NAVY)
    c.rect(0, H - 42 * mm, W, 42 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(0, H - 42 * mm, W, 2 * mm, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("Mono", 8)
    c.drawString(M, H - 11 * mm, "AMK · DOUALA")
    c.setFont("HeadB", 19)
    c.drawString(M, H - 21 * mm, "Le contrôle présence en ligne")
    c.setFont("Sans", 9.6)
    c.setFillColor(SLATE_L)
    c.drawString(M, H - 28 * mm, "Douze points à vérifier sur votre cabinet — huit minutes, sans inscription.")
    c.setFont("Sans", 8.4)
    c.drawString(M, H - 34.5 * mm,
                 "Cochez « oui » quand c'est vrai aujourd'hui, pas quand c'est prévu. À la fin, comptez : le score s'explique de lui-même.")

    y = H - 50 * mm
    cols_w = (W - 2 * M)
    n = 0
    for titre, sous, items in BLOCS:
        c.setFont("HeadB", 10.6)
        c.setFillColor(NAVY)
        c.drawString(M, y, titre)
        tw = pdfmetrics.stringWidth(titre, "HeadB", 10.6)
        c.setFont("Sans", 8.2)
        c.setFillColor(AMBER_D)
        c.drawString(M + tw + 3 * mm, y, sous)
        y -= 2.2 * mm
        c.setStrokeColor(AMBER)
        c.setLineWidth(1.6)
        c.line(M, y, M + 12 * mm, y)
        y -= 5.4 * mm

        for nom, comment, cout in items:
            n += 1
            # case à cocher
            c.setStrokeColor(SLATE_L)
            c.setLineWidth(0.8)
            c.rect(M, y - 0.6 * mm, 3.2 * mm, 3.2 * mm, stroke=1, fill=0)
            x = M + 6.5 * mm
            c.setFont("Mono", 6.8)
            c.setFillColor(AMBER_D)
            c.drawString(x, y, f"{n:02d}")
            x += 6 * mm
            c.setFont("HeadB", 8.8)
            c.setFillColor(NAVY)
            c.drawString(x, y, nom)
            c.setFont("Sans", 8.1)
            c.setFillColor(SLATE)
            lines = wrap(comment, "Sans", 8.1, cols_w - 12.5 * mm - 34 * mm)
            c.drawString(x + pdfmetrics.stringWidth(nom, "HeadB", 8.8) + 3 * mm, y, lines[0])
            y -= 4.3 * mm
            for extra in lines[1:]:
                c.drawString(x, y, extra)
                y -= 4.0 * mm
            c.setFont("Sans", 7.4)
            c.setFillColor(AMBER_D)
            c.drawString(x, y, "si c'est non : " + cout)
            y -= 6.0 * mm
        y -= 2.4 * mm

    # barème : trois lignes, pour que le score veuille dire quelque chose
    c.setFillColor(PAPER)
    c.roundRect(M, y - 26 * mm, W - 2 * M, 24 * mm, 2.5 * mm, stroke=0, fill=1)
    c.setFont("HeadB", 9.4)
    c.setFillColor(NAVY)
    c.drawString(M + 5 * mm, y - 5.5 * mm, "Comment lire votre score")
    lignes = [
        ("9 à 12", "solide — il reste à mesurer et à publier régulièrement", NAVY),
        ("5 à 8", "la base existe, mais un patient vous perd en route", AMBER_D),
        ("0 à 4", "le cabinet est invisible pour qui ne connaît pas déjà votre adresse", HexColor("#991B1B")),
    ]
    ly = y - 11 * mm
    for score, texte, col in lignes:
        c.setFont("Mono", 8.2)
        c.setFillColor(col)
        c.drawString(M + 5 * mm, ly, score)
        c.setFont("Sans", 8.4)
        c.setFillColor(SLATE)
        c.drawString(M + 22 * mm, ly, texte)
        ly -= 5.4 * mm

    # pied : un seul CTA
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 26 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(0, 26 * mm, W, 1.2 * mm, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("HeadB", 10.5)
    c.drawString(M, 18 * mm, "Vous avez coché moins de huit cases ?")
    c.setFont("Sans", 8.8)
    c.setFillColor(SLATE_L)
    c.drawString(M, 13 * mm,
                 "Écrivez le mot CONTRÔLE au +237 677 78 96 31. On regarde les douze points ensemble, vingt minutes, sans engagement.")
    c.setFont("Mono", 7.4)
    c.setFillColor(AMBER)
    c.drawString(M, 7.4 * mm, "AMK · akwo.king.dev@gmail.com · Douala")
    c.setFont("Sans", 7.2)
    c.setFillColor(SLATE_L)
    c.drawRightString(W - M, 7.4 * mm, "une page · aucun chiffre inventé · vérifiable sur votre propre cabinet")

    c.showPage()
    c.save()
    try:
        print("écrit :", OUT.relative_to(ROOT))
    except ValueError:
        print("écrit :", OUT)


if __name__ == "__main__":
    build()
