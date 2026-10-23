#!/usr/bin/env python3
"""Récapitulatif client — une page A4, PDF vectoriel, piloté par un fichier de données.

    pip install reportlab
    python3 tools/ops/make_recap.py --data clients/dm-optic/launch/recap-2026-10.json \
                                    --out  clients/dm-optic/launch/RECAP-MISE-EN-LIGNE-2026-10-23.pdf

Le même moteur sert **tous les clients** : seul le JSON change (identité, blocs, chiffres, dates).
Le modèle de départ est `tools/ops/recap-modele.json` — on le copie, on remplit, on rend.
Chaque chiffre porte sa date et sa source (règle §1g). Aucun prix de monture, aucun visage de patient,
aucune promesse de délai : ces règles vivent dans le contenu, pas dans le gabarit — donc elles se
relisent dans le JSON avant chaque envoi.
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

NAVY = HexColor("#0B1120")
AMBER = HexColor("#F59E0B")
AMBER_D = HexColor("#B45309")
SLATE = HexColor("#475569")
SLATE_L = HexColor("#94A3B8")
LINE = HexColor("#E2E8F0")
PAPER = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")

W, H = A4
M = 16 * mm
BOTTOM = 34 * mm  # sous cette ligne, on déborde sur le pied de page

DEFAUT = {
    "identite": {
        "nom": "NOM DU CLIENT",
        "sous_titre": "Activité · quartier, ville",
        "agence": "AMK",
        "pied_gauche": "sites web bilingues pour cabinets, cliniques et commerces — Douala",
        "pied_droite": "akwo.king.dev@gmail.com · +237 677 78 96 31",
    },
    "titre": "Récapitulatif du mois",
    "date_titre": "",
    "section1": "Ce qui est en ligne",
    "kicker1": "01 · la livraison",
    "section2": "Ce que ça a donné",
    "kicker2": "02 · les chiffres, sans arrondi flatteur",
    "section3": "Ce qui tourne maintenant",
    "kicker3": "03 · le forfait mensuel",
    "section4": "Vos accès",
    "kicker4": "04 · ce qui vous appartient",
    "releve": "",
    "releve_court": "",
    "livraison": [],
    "chiffres": {"colonnes": [], "lignes": [], "note": ""},
    "mensuel": [],
    "acces": {"corps": "", "pied": ""},
}


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


def header(c: canvas.Canvas, d: dict) -> float:
    idt = d["identite"]
    c.setFillColor(NAVY)
    c.rect(0, H - 40 * mm, W, 40 * mm, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.rect(0, H - 40 * mm, W, 2.2 * mm, stroke=0, fill=1)

    c.setFillColor(WHITE)
    c.setFont("HeadB", 20)
    c.drawString(M, H - 17 * mm, idt["nom"])
    c.setFont("Sans", 9.5)
    c.setFillColor(SLATE_L)
    c.drawString(M, H - 22.5 * mm, idt["sous_titre"])

    c.setFont("HeadB", 13.5)
    c.setFillColor(WHITE)
    c.drawString(M, H - 32 * mm, d["titre"])

    c.setFont("Mono", 8)
    c.setFillColor(AMBER)
    c.drawRightString(W - M, H - 17 * mm, idt["agence"])
    c.setFillColor(SLATE_L)
    c.setFont("Sans", 8.5)
    c.drawRightString(W - M, H - 22.5 * mm, d["date_titre"])
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


def stat_table(c, y, ch: dict) -> float:
    """N colonnes, chaque ligne une seule vérité par colonne."""
    cols = ch["colonnes"]
    rows = ch["lignes"]
    x0 = M
    col_x = [M + 62 * mm + i * 46 * mm for i in range(len(cols))]

    c.setFont("SansB", 7.6)
    c.setFillColor(SLATE_L)
    if ch.get("releve"):
        c.drawString(x0, y, "RELEVÉ DU " + ch["releve"])
    for i, name in enumerate(cols):
        c.drawString(col_x[i], y, name.upper())
    y -= 6 * mm

    for i, row in enumerate(rows):
        if i % 2 == 0:
            c.setFillColor(PAPER)
            c.rect(M - 2 * mm, y - 2.4 * mm, W - 2 * M + 4 * mm, 6.5 * mm, stroke=0, fill=1)
        c.setFont("Sans", 8.2)
        c.setFillColor(SLATE)
        c.drawString(x0, y, row[0])
        for j, val in enumerate(row[1:]):
            weak = val in ("—", "non communiqué", "")
            c.setFont("Mono", 7.2 if weak else 8.6)
            c.setFillColor(SLATE_L if weak else NAVY)
            c.drawString(col_x[j], y, val)
        y -= 6.4 * mm
    return y


def build(d: dict, out: Path) -> None:
    fonts()
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle(f"{d['identite']['nom']} — {d['titre'].lower()}")
    c.setAuthor(d["identite"]["agence"])
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    y = header(c, d) - 7 * mm

    # 1 — livraison : 2 colonnes, autant de cartes que de lignes fournies
    y = section(c, y, d["section1"], d["kicker1"])
    colw = (W - 2 * M - 6 * mm) / 2
    cards = d["livraison"]
    for i in range(0, len(cards), 2):
        pair = cards[i:i + 2]
        for j, cd in enumerate(pair):
            card(c, M + j * (colw + 6 * mm), y, colw, 23 * mm, cd["titre"], cd["corps"], cd.get("tag"))
        y -= 26.5 * mm
    y -= 3.5 * mm

    # 2 — chiffres
    ch = d["chiffres"]
    if ch.get("lignes"):
        y = section(c, y, d["section2"], d["kicker2"])
        ch = {**ch, "releve": ch.get("releve") or d["releve_court"]}
        y = stat_table(c, y, ch)
        if ch.get("note"):
            y = paragraph(c, ch["note"], M, y - 1 * mm, W - 2 * M, size=8.2, leading=11.2) - 6 * mm
        else:
            y -= 4 * mm

    # 3 — le mois
    if d["mensuel"]:
        y = section(c, y, d["section3"], d["kicker3"])
        for title, body in d["mensuel"]:
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
    acc = d["acces"]
    if acc.get("corps"):
        y = section(c, y, d["section4"], d["kicker4"])
        y = paragraph(c, acc["corps"], M, y, W - 2 * M, size=8.4, leading=11.4) + 2 * mm

    if y < BOTTOM:
        raise SystemExit(
            f"Débordement : le contenu descend à {y/mm:.0f} mm, la limite est {BOTTOM/mm:.0f} mm. "
            "Raccourcir un bloc du JSON — c'est une page, pas deux."
        )

    # pied
    idt = d["identite"]
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 18 * mm, stroke=0, fill=1)
    c.setFillColor(WHITE)
    c.setFont("HeadB", 9)
    c.drawString(M, 11 * mm, idt["agence"])
    c.setFont("Sans", 8)
    c.setFillColor(SLATE_L)
    c.drawString(M + 12 * mm, 11 * mm, idt["pied_gauche"])
    c.drawRightString(W - M, 11 * mm, idt["pied_droite"])
    if acc.get("pied"):
        c.setFont("Mono", 6.6)
        c.drawRightString(W - M, 6 * mm, acc["pied"])

    c.showPage()
    c.save()
    try:
        print("écrit :", out.relative_to(ROOT))
    except ValueError:
        print("écrit :", out)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Récapitulatif client, une page A4")
    ap.add_argument("--data", type=Path, required=True, help="JSON du récapitulatif")
    ap.add_argument("--out", type=Path, required=True, help="PDF de sortie")
    a = ap.parse_args(argv)
    data = {**DEFAUT, **json.loads(a.data.read_text(encoding="utf-8"))}
    data["identite"] = {**DEFAUT["identite"], **data["identite"]}
    data["chiffres"] = {**DEFAUT["chiffres"], **data["chiffres"]}
    data["acces"] = {**DEFAUT["acces"], **data["acces"]}
    out = a.out if a.out.is_absolute() else ROOT / a.out
    build(data, out)


if __name__ == "__main__":
    main()
