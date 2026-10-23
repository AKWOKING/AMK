#!/usr/bin/env python3
"""Récapitulatif mensuel DM OPTIQUE — une page A4, PDF vectoriel.

    pip install reportlab          # + pypdfium2 pour un aperçu PNG (optionnel)
    python3 tools/ops/make_recap_dm.py                          # chiffres d'octobre (défaut)
    python3 tools/ops/make_recap_dm.py --data recap-2026-11.json --out RECAP-2026-11.pdf

Le modèle de données est `clients/dm-optic/launch/recap-2026-10.json` : on le copie, on change les
chiffres et les dates, rien d'autre. Chaque chiffre porte sa date et sa source (règle §1g) : Facebook
Business Suite et TikTok Studio. Aucun prix de monture, aucun visage de patient, aucune promesse de délai.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "clients/dm-optic/content/month1/w1/assets/fonts"
LAUNCH = ROOT / "clients/dm-optic/launch"
OUT = LAUNCH / "RECAP-MISE-EN-LIGNE-2026-10-23.pdf"

DEFAUT = {
    "titre": "Récapitulatif de la mise en ligne",
    "section1": "Ce qui est en ligne aujourd'hui",
    "date_titre": "23 octobre 2026",
    "releve": "23/10/2026 à 08h40",
    "releve_court": "23/10 À 08H40",
    "fb": {"date": "22/10", "views": "210", "viewers": "200", "watch": "4 s",
           "full": "—", "react": "3", "com": "0", "share": "1"},
    "tk": {"date": "22/10 à 14h36", "views": "90", "watch": "6,9 s",
           "full": "4,9 %", "react": "8", "com": "1", "share": "1"},
    "lendemain": "les prochains jours",
}
DATA = DEFAUT

NAVY = HexColor("#0B1120")
NAVY2 = HexColor("#1E293B")
AMBER = HexColor("#F59E0B")
AMBER_D = HexColor("#B45309")
SLATE = HexColor("#475569")
SLATE_L = HexColor("#94A3B8")
LINE = HexColor("#E2E8F0")
PAPER = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")

W, H = A4
M = 16 * mm


def fonts() -> None:
    pdfmetrics.registerFont(TTFont("Sans", str(FONTS / "ibm-plex-sans-latin-400-normal.ttf")))
    pdfmetrics.registerFont(TTFont("SansB", str(FONTS / "schibsted-grotesk-latin-700-normal.ttf")))
    pdfmetrics.registerFont(TTFont("Head", str(FONTS / "schibsted-grotesk-latin-500-normal.ttf")))
    pdfmetrics.registerFont(TTFont("HeadB", str(FONTS / "schibsted-grotesk-latin-700-normal.ttf")))
    pdfmetrics.registerFont(TTFont("Mono", str(FONTS / "ibm-plex-mono-latin-600-normal.ttf")))


def wrap(c: canvas.Canvas, text: str, font: str, size: float, width: float) -> list[str]:
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


def paragraph(c, text, x, y, width, font="Sans", size=9, leading=12.4, color=SLATE) -> float:
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap(c, text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def header(c: canvas.Canvas) -> float:
    c.setFillColor(NAVY)
    c.rect(0, H - 40 * mm, W, 40 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(0, H - 40 * mm, W, 2.2 * mm, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont("HeadB", 20)
    c.drawString(M, H - 17 * mm, "DM OPTIQUE SARL")
    c.setFont("Sans", 9.5)
    c.setFillColor(SLATE_L)
    c.drawString(M, H - 22.5 * mm, "Cabinet d'optique médicale · Ndobo Mayor, Bonabéri, Douala")

    c.setFont("HeadB", 13.5)
    c.setFillColor(WHITE)
    c.drawString(M, H - 32 * mm, DATA["titre"])

    c.setFont("Mono", 8)
    c.setFillColor(AMBER)
    c.drawRightString(W - M, H - 17 * mm, "AMK")
    c.setFillColor(SLATE_L)
    c.setFont("Sans", 8.5)
    c.drawRightString(W - M, H - 22.5 * mm, DATA["date_titre"])
    return H - 40 * mm


def section(c, y, title, kicker=None) -> float:
    if kicker:
        c.setFont("Mono", 7.2)
        c.setFillColor(AMBER_D)
        c.drawString(M, y, kicker.upper())
        y -= 5.4 * mm
    c.setFont("HeadB", 12)
    c.setFillColor(NAVY)
    c.drawString(M, y, title)
    c.setStrokeColor(AMBER)
    c.setLineWidth(2)
    c.line(M, y - 2.4 * mm, M + 14 * mm, y - 2.4 * mm)
    return y - 7.5 * mm


def card(c, x, y, w, h, title, body, tag=None) -> None:
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y - h, w, h, 2.6 * mm, stroke=1, fill=1)
    c.setFillColor(NAVY)
    c.setFont("HeadB", 9.4)
    c.drawString(x + 4 * mm, y - 6.4 * mm, title)
    if tag:
        c.setFont("Mono", 6.6)
        c.setFillColor(AMBER_D)
        c.drawRightString(x + w - 4 * mm, y - 6.4 * mm, tag)
    paragraph(c, body, x + 4 * mm, y - 11.4 * mm, w - 8 * mm, size=8.2, leading=10.8, color=SLATE)


def stat_table(c, y) -> float:
    """Deux colonnes : Facebook · TikTok. Chaque ligne a une seule vérité par colonne."""
    rows = [
        ("Vues", DATA["fb"]["views"], DATA["tk"]["views"]),
        ("Spectateurs uniques", DATA["fb"]["viewers"], "non communiqué"),
        ("Temps de visionnage moyen", DATA["fb"]["watch"], DATA["tk"]["watch"]),
        ("Vidéo regardée en entier", DATA["fb"]["full"], DATA["tk"]["full"]),
        ("Réactions", DATA["fb"]["react"], DATA["tk"]["react"]),
        ("Commentaires", DATA["fb"]["com"], DATA["tk"]["com"]),
        ("Partages", DATA["fb"]["share"], DATA["tk"]["share"]),
    ]
    x0, col2 = M, M + 62 * mm
    head_y = y
    c.setFont("SansB", 7.6)
    c.setFillColor(SLATE_L)
    c.drawString(x0, head_y, "RELEVÉ DU " + DATA["releve_court"])
    c.drawString(col2, head_y, "FACEBOOK")
    c.drawString(col2 + 46 * mm, head_y, "TIKTOK")
    y = head_y - 6 * mm
    for i, (label, fb, tk) in enumerate(rows):
        if i % 2 == 0:
            c.setFillColor(PAPER)
            c.rect(M - 2 * mm, y - 2.4 * mm, W - 2 * M + 4 * mm, 6.5 * mm, stroke=0, fill=1)
        c.setFont("Sans", 8.2)
        c.setFillColor(SLATE)
        c.drawString(x0, y, label)
        c.setFont("Mono", 8.6)
        c.setFillColor(NAVY)
        c.drawString(col2, y, fb)
        c.setFont("Mono", 8.6 if tk != "non communiqué" else 7.2)
        c.setFillColor(NAVY if tk != "non communiqué" else SLATE_L)
        c.drawString(col2 + 46 * mm, y, tk)
        y -= 6.4 * mm
    return y


def build() -> None:
    fonts()
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("DM OPTIQUE SARL — " + DATA["titre"].lower())
    c.setAuthor("AMK")
    c.setSubject("Ce qui est en ligne au 23 octobre 2026")

    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    y = header(c)
    y -= 7 * mm

    # 1 — ce qui est en ligne
    y = section(c, y, DATA["section1"], "01 · la livraison")
    colw = (W - 2 * M - 6 * mm) / 2
    card(c, M, y, colw, 23 * mm, "Le site",
         "dmoptiquesarl.com — 96 pages en français et en anglais, une fiche par monture, "
         "bouton WhatsApp déjà écrit sur chaque écran.", "EN LIGNE")
    card(c, M + colw + 6 * mm, y, colw, 23 * mm, "La fiche Google",
         "Créée au nom du cabinet : adresse avec repère, horaires (examen 8h30–13h00), photos, "
         "itinéraire, bouton d'appel.", "ACTIVE")
    y -= 26.5 * mm
    card(c, M, y, colw, 23 * mm, "La page Facebook",
         f"DM OPTIQUE SARL — première vidéo publiée le {DATA['fb']['date']} : les quatre temps "
         "de l'examen, sur la photo réelle du cabinet.", "PUBLIÉE")
    card(c, M + colw + 6 * mm, y, colw, 23 * mm, "Le compte TikTok",
         f"@dmoptique.bonaberi237 — la même vidéo, publiée le {DATA['tk']['date']}. "
         "Le téléphone du cabinet est dans la bio.", "PUBLIÉ")
    y -= 30 * mm

    # 2 — les chiffres
    y = section(c, y, "Ce que la première vidéo a donné", "02 · les chiffres, sans arrondi flatteur")
    y = stat_table(c, y)
    y -= 2 * mm
    y = paragraph(
        c,
        "Un premier post ne dit pas si la stratégie marche : il dit que la mécanique fonctionne — la vidéo "
        "arrive, elle est vue, et le numéro du cabinet est joignable en un geste. Les chiffres ci-dessus "
        f"viennent des tableaux de bord Facebook et TikTok, relevés le {DATA['releve']} ; ils bougeront "
        f"encore dans {DATA['lendemain']}.",
        M, y - 1 * mm, W - 2 * M, size=8.2, leading=11.2) - 6 * mm

    # 3 — le mois
    y = section(c, y, "Ce qui tourne maintenant", "03 · le forfait mensuel")
    items = [
        ("8 publications par mois", "deux par semaine : une vidéo courte et un carrousel, sur la page et sur TikTok."),
        ("2 publications Google", "la fiche reste vivante — c'est ce qui la fait remonter sur « opticien Bonabéri »."),
        ("Le site entretenu", "sauvegardes, mises à jour, certificat, disponibilité surveillés."),
        ("Un rapport d'une page", "chaque début de mois : ce qui a été publié, ce que ça a donné, ce qui vient."),
    ]
    for title, body in items:
        c.setFillColor(AMBER)
        c.circle(M + 1.2 * mm, y + 1.1 * mm, 1.2 * mm, stroke=0, fill=1)
        c.setFont("SansB", 8.6)
        c.setFillColor(NAVY)
        c.drawString(M + 5 * mm, y, title)
        tw = pdfmetrics.stringWidth(title, "SansB", 8.6)
        c.setFont("Sans", 8.2)
        c.setFillColor(SLATE)
        c.drawString(M + 5 * mm + tw + 2 * mm, y, body)
        y -= 6.4 * mm
    y -= 3 * mm

    # 4 — accès
    y = section(c, y, "Vos accès", "04 · ce qui vous appartient")
    y = paragraph(
        c,
        "Le domaine, la fiche Google et la page Facebook sont au nom du cabinet, sur le compte "
        "dmoptiquesarl@gmail.com. AMK gère au quotidien ; vous gardez la propriété et les identifiants — "
        "si vous changez de prestataire, rien ne part avec nous.",
        M, y, W - 2 * M, size=8.4, leading=11.4) + 2 * mm

    # pied
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 18 * mm, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("HeadB", 9)
    c.drawString(M, 11 * mm, "AMK")
    c.setFont("Sans", 8)
    c.setFillColor(SLATE_L)
    c.drawString(M + 12 * mm, 11 * mm, "sites web bilingues pour cabinets, cliniques et commerces — Douala")
    c.drawRightString(W - M, 11 * mm, "akwo.king.dev@gmail.com · +237 677 78 96 31")
    c.setFont("Mono", 6.6)
    c.drawRightString(W - M, 6 * mm, f"chiffres relevés le {DATA['releve']} · Facebook Business Suite, TikTok Studio")

    c.showPage()
    c.save()
    try:
        rel = OUT.relative_to(ROOT)
    except ValueError:
        rel = OUT
    print("écrit :", rel)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Récapitulatif mensuel DM OPTIQUE (une page A4)")
    ap.add_argument("--data", type=Path, help="JSON des chiffres du mois (défaut : ceux d'octobre)")
    ap.add_argument("--out", type=Path, help="PDF de sortie")
    a = ap.parse_args()
    if a.data:
        DATA = {**DEFAUT, **json.loads(a.data.read_text(encoding="utf-8"))}
    if a.out:
        OUT = a.out if a.out.is_absolute() else ROOT / a.out
    build()
