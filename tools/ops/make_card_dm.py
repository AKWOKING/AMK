#!/usr/bin/env python3
"""Carte « Votre avis nous aide » pour DM OPTIQUE — A4, 4 cartes de 85 × 55 mm à découper.

    pip install reportlab qrcode
    python3 tools/ops/make_card_dm.py

Sortie : clients/dm-optic/launch/CARTE-AVIS-2026-10-23.pdf

Deux QR par carte : l'avis Google et les avis Facebook. Les deux URL sont celles des documents de
lancement (place_id du cabinet, page publiée dans le JSON-LD du site). Un QR se teste avec un
téléphone avant impression — un QR mort sur un comptoir est pire que pas de carte.
"""
from __future__ import annotations

import sys
from pathlib import Path

import io

import qrcode
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "clients/dm-optic/content/month1/w1/assets/fonts"
OUT = ROOT / "clients/dm-optic/launch/CARTE-AVIS-2026-10-23.pdf"

GOOGLE = "https://search.google.com/local/writereview?placeid=ChIJjdfYfQwXYRARAdi9mPLHGjY"
FACEBOOK = "https://www.facebook.com/profile.php?id=61595694418153&sk=reviews"

NAVY = HexColor("#0B1120")
AMBER = HexColor("#F59E0B")
SLATE = HexColor("#475569")
SLATE_L = HexColor("#94A3B8")
LINE = HexColor("#CBD5E1")
WHITE = HexColor("#FFFFFF")

CARD_W, CARD_H = 85 * mm, 55 * mm
W, H = A4
COLS, ROWS = 2, 4
GAP = 6 * mm
MARGIN_X = (W - COLS * CARD_W - (COLS - 1) * GAP) / 2
MARGIN_Y = (H - ROWS * CARD_H - (ROWS - 1) * GAP) / 2


def fonts() -> None:
    pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "ibm-plex-sans-latin-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("HeadB", str(FONTS / "schibsted-grotesk-latin-700-normal.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(FONTS / "ibm-plex-mono-latin-600-normal.ttf")))


_CACHE: dict[str, ImageReader] = {}


def qr_png(url: str, px: int = 800) -> ImageReader:
    """QR en bitmap : un QR vectoriel dessiné module par module finit par fusionner ses modules.

    `border=2` = zone de silence de 2 modules, celle qui manque le plus souvent sur les QR imprimés.
    Vérifié par décodage réel (opencv) sur le PDF rendu — voir le test en fin de fichier.
    """
    if url in _CACHE:
        return _CACHE[url]
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB").resize((px, px))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    _CACHE[url] = ImageReader(buf)
    return _CACHE[url]


def draw_qr(c: canvas.Canvas, url: str, x: float, y: float, size: float) -> None:
    c.drawImage(qr_png(url), x, y, size, size, mask=None)


def card(c: canvas.Canvas, x: float, y: float) -> None:
    """y = coin bas-gauche de la carte. Tout est calé sur des offsets fixes : rien ne se chevauche."""
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.setDash(2, 2)
    c.roundRect(x, y, CARD_W, CARD_H, 2.5 * mm, stroke=1, fill=0)
    c.setDash()

    # bandeau (16,5 mm en haut, filet ambre au ras)
    band_h = 16.5 * mm
    c.setFillColor(NAVY)
    c.roundRect(x, y + CARD_H - band_h, CARD_W, band_h, 2.5 * mm, stroke=0, fill=1)
    c.rect(x, y + CARD_H - band_h, CARD_W, 3 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(x, y + CARD_H - band_h - 0.9 * mm, CARD_W, 0.9 * mm, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont("HeadB", 11.5)
    c.drawString(x + 5 * mm, y + CARD_H - 8.4 * mm, "Votre avis nous aide")
    c.setFont("Sans", 6.8)
    c.setFillColor(SLATE_L)
    c.drawString(x + 5 * mm, y + CARD_H - 13 * mm, "Scannez avec l'appareil photo — 30 secondes")

    # deux QR de 23 mm : 37 modules → 0,62 mm le module, lisible par un téléphone d'entrée de gamme
    qs = 23 * mm
    qy = y + 12 * mm
    gx = x + 5 * mm
    fx = x + CARD_W - 5 * mm - qs
    draw_qr(c, GOOGLE, gx, qy, qs)
    draw_qr(c, FACEBOOK, fx, qy, qs)

    c.setFont("HeadB", 7.4)
    c.setFillColor(NAVY)
    c.drawCentredString(gx + qs / 2, y + 8.4 * mm, "Avis Google")
    c.drawCentredString(fx + qs / 2, y + 8.4 * mm, "Facebook")

    # pied de carte, une seule ligne : identifiant + site
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(x + 5 * mm, y + 6 * mm, x + CARD_W - 5 * mm, y + 6 * mm)
    c.setFont("Mono", 6.6)
    c.setFillColor(NAVY)
    c.drawString(x + 5 * mm, y + 2.7 * mm, "@dmoptique.bonaberi237")
    c.setFont("Sans", 6.4)
    c.setFillColor(SLATE)
    c.drawRightString(x + CARD_W - 5 * mm, y + 2.7 * mm, "dmoptiquesarl.com")


def build() -> None:
    fonts()
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("DM OPTIQUE SARL — carte d'avis (4 par page A4)")
    c.setAuthor("AMK")
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    for r in range(ROWS):
        for col in range(COLS):
            x = MARGIN_X + col * (CARD_W + GAP)
            y = MARGIN_Y + r * (CARD_H + GAP)
            card(c, x, y)

    c.setFont("Sans", 6.5)
    c.setFillColor(SLATE_L)
    c.drawCentredString(W / 2, 5 * mm,
                        "AMK · à imprimer à 100 % (sans « ajuster à la page »), puis découper sur les pointillés")
    c.showPage()
    c.save()
    try:
        print("écrit :", OUT.relative_to(ROOT))
    except ValueError:
        print("écrit :", OUT)


if __name__ == "__main__":
    build()
    sys.exit(0)
