#!/usr/bin/env python3
"""Contrat de prestation AMK — une page A4, deux exemplaires à imprimer.

    pip install reportlab
    python3 tools/ops/make_contrat.py

Sortie : ops/templates/CONTRAT-UNE-PAGE-2026-10.pdf
Source éditable du texte : ops/templates/CONTRAT-UNE-PAGE-2026-10.md

Les champs à remplir sont des lignes de points : le contrat s'imprime puis se remplit à la main, en
visite. C'est volontaire — un PDF « à signer à distance » ne vaut rien ici, le papier reste la preuve.
Le moteur s'arrête si le texte dépasse une page : « une page » est une contrainte, pas un souhait.
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
OUT = ROOT / "ops/templates/CONTRAT-UNE-PAGE-2026-10.pdf"

NAVY = HexColor("#0B1120")
AMBER = HexColor("#F59E0B")
SLATE = HexColor("#475569")
SLATE_L = HexColor("#94A3B8")
LINE = HexColor("#CBD5E1")

W, H = A4
M = 18 * mm
BOTTOM = 16 * mm

CLAUSES = [
    ("1 · Objet",
     "Le prestataire conçoit et met en ligne le site de …………………………………… : …… pages, en français et en "
     "anglais, avec un bouton de contact WhatsApp sur chaque écran. Le site est livré sur le nom de "
     "domaine choisi par le client."),
    ("2 · Ce qui est inclus, ce qui ne l'est pas",
     "Inclus : la conception, la rédaction des textes des pages, l'intégration des photos fournies par le "
     "client, la mise en ligne, deux (2) tours de modifications et trente (30) jours de corrections après "
     "la mise en ligne. Non inclus, sur devis séparé : séance photo professionnelle, publicité en ligne, "
     "achat du nom de domaine et de l'hébergement (au nom du client), rédaction de contenus médicaux "
     "réglementés."),
    ("3 · Prix et échéancier",
     "Total : ……………………… FCFA. 50 % à la signature (……………… FCFA), 50 % à la livraison (……………… FCFA). "
     "Chaque facture est payable sous sept (7) jours. Moyens de paiement : Mobile Money, Orange Money, "
     "virement bancaire — les coordonnées figurent sur la facture."),
    ("4 · Retard de paiement",
     "Tout montant impayé à l'échéance porte intérêt de 1 % par mois, plafonné à 10 % du montant dû. "
     "Passé quinze (15) jours, le prestataire peut suspendre le service après en avoir informé le client "
     "par écrit."),
    ("5 · Validations et délais",
     "Le client renvoie ses remarques sous cinq (5) jours ouvrés après chaque envoi. Passé ce délai, "
     "l'étape est réputée validée et le calendrier continue."),
    ("6 · Propriété",
     "Dès paiement intégral, le nom de domaine, les comptes (Google, Facebook, TikTok), les textes et les "
     "images sont la propriété du client. Le prestataire conserve le droit de citer le site à titre de "
     "référence, sauf refus écrit du client."),
    ("7 · Abonnement mensuel (si souscrit)",
     "…………………… FCFA par mois à partir du ……………………, préavis de quatorze (14) jours de part et d'autre, "
     "prix figé douze (12) mois. Le périmètre mensuel figure en annexe : publications, fiche Google, "
     "entretien du site, récapitulatif d'une page."),
    ("8 · Fin du contrat",
     "Résiliation par écrit, à tout moment, dans le respect du préavis. Les sommes dues au titre du travail "
     "réalisé restent dues. Aucune indemnité au-delà du préavis."),
    ("9 · Photos et droit à l'image",
     "Le client fournit les photos et garantit l'accord des personnes qui y figurent, ainsi que le droit de "
     "les publier sur le site et les réseaux du cabinet. Aucune photo de patient identifiable n'est publiée "
     "sans autorisation écrite."),
    ("10 · Litiges",
     "Droit camerounais. Tribunaux de Douala. Les parties cherchent d'abord une solution amiable écrite."),
]


def fonts() -> None:
    pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "ibm-plex-sans-latin-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("HeadB", str(FONTS / "schibsted-grotesk-latin-700-normal.ttf")))
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
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("AMK — contrat de prestation, une page")
    c.setAuthor("AMK")

    # en-tête
    c.setFillColor(NAVY)
    c.rect(0, H - 26 * mm, W, 26 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(0, H - 26 * mm, W, 1.6 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("HeadB", 15)
    c.drawString(M, H - 13 * mm, "CONTRAT DE PRESTATION")
    c.setFont("Sans", 8.5)
    c.setFillColor(SLATE_L)
    c.drawString(M, H - 18.5 * mm, "Site web, mise en ligne et suivi — deux exemplaires, un pour chaque partie")
    c.setFont("Mono", 8)
    c.setFillColor(AMBER)
    c.drawRightString(W - M, H - 13 * mm, "AMK")

    y = H - 33 * mm

    # parties
    c.setFont("Sans", 8.2)
    c.setFillColor(SLATE)
    c.drawString(M, y, "Prestataire : AMK — Akwo King, Douala · +237 677 78 96 31 · akwo.king.dev@gmail.com")
    y -= 4.6 * mm
    c.drawString(M, y, "NIU : ……………………………")
    y -= 5.4 * mm
    c.drawString(M, y, "Client : ………………………………………………………… représenté par ………………………………………")
    y -= 4.6 * mm
    c.drawString(M, y, "NIU : ……………………………    Adresse : ………………………………………………………………………………………")
    y -= 4 * mm

    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, y, W - M, y)
    y -= 6.5 * mm

    # clauses
    for title, body in CLAUSES:
        c.setFont("HeadB", 9.4)
        c.setFillColor(NAVY)
        c.drawString(M, y, title)
        y -= 4.9 * mm
        c.setFont("Sans", 8.9)
        c.setFillColor(SLATE)
        for line in wrap(body, "Sans", 8.9, W - 2 * M):
            c.drawString(M, y, line)
            y -= 4.5 * mm
        y -= 2.4 * mm

    if y < BOTTOM + 34 * mm:
        raise SystemExit(f"Débordement : {y / mm:.0f} mm restants — raccourcir une clause.")

    # signature : un vrai bloc, séparé du texte, avec de la place pour signer à la main
    y -= 6 * mm
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, y, W - M, y)
    y -= 5.5 * mm
    c.setFont("Sans", 8.6)
    c.setFillColor(SLATE)
    c.drawString(M, y, "Fait à ………………………………………, le ………………………………………, en deux exemplaires.")
    y -= 13 * mm
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.7)
    c.line(M, y, M + 62 * mm, y)
    c.line(W - M - 62 * mm, y, W - M, y)
    c.setFont("Sans", 8)
    c.setFillColor(SLATE_L)
    c.drawString(M, y - 4 * mm, "Le client — nom, date, signature")
    c.drawRightString(W - M, y - 4 * mm, "Le prestataire — nom, date, signature")

    c.setFont("Sans", 6.8)
    c.setFillColor(SLATE_L)
    c.drawCentredString(W / 2, 8 * mm, "Modèle commercial AMK — à faire relire une fois par un juriste camerounais.")

    c.showPage()
    c.save()
    try:
        print("écrit :", OUT.relative_to(ROOT))
    except ValueError:
        print("écrit :", OUT)


if __name__ == "__main__":
    build()
