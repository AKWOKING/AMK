#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAVISA OPTIQUE — le constructeur de l'aperçu (24/09/2026).

Ce que fait ce script, dans l'ordre :
 1. il prépare les deux photographies (16/10 pour le hero, 4/3 pour la section ordonnance) ;
 2. il les emballe en base64 dans le gabarit `demos/cavisa-v1.tpl.html` ;
 3. il écrit la page d'aperçu (un seul fichier, qui s'ouvre sur n'importe quel téléphone) ;
 4. il en fait la copie déployable dans `hosting/previews/cavisa/`, plus la vignette 1200×630
    (`og.jpg`) que WhatsApp affichera avant d'ouvrir le lien (§20.7).

Rien n'est inventé ici : chaque phrase vient du briefing de King (24/09) et des faits vérifiés
consignés dans `clients/cavisa/inspiration.md`. Aucun prix, aucun délai, aucune note, aucun avis.

Usage : python3 demos/build_cavisa.py
"""
import base64
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEMOS = ROOT / "demos"
IMG = DEMOS / "img"
TPL = DEMOS / "cavisa-v1.tpl.html"
OUT_CONCEPT = DEMOS / "concept-cavisa-v1.html"
PREVIEW = ROOT / "hosting" / "previews" / "cavisa"
OUT_PREVIEW = PREVIEW / "index.html"
OUT_OG = PREVIEW / "og.jpg"

# Les deux photographies : la source, la découpe, le poids visé. Une photo = une signification (§25).
PHOTOS = {
    # jeton              source                découpe exacte      largeur  qualité
    "__IMG_TRYON__": ("cavisa-tryon.jpg", "1080x675+116+0", "960x", "56"),   # le comptoir : on essaie (16:10)
    "__IMG_EXAM__": ("cavisa-exam.jpg", "896x672+208+0", "840x", "56"),      # l'ordonnance : d'où elle vient (4:3)
}


def prepare(name, geometry, width, quality, out):
    """Découpe et allège une photo. La découpe est déjà au bon rapport, le redimensionnement le garde."""
    src = IMG / name
    if not src.exists():
        sys.exit("photo manquante : %s" % src)
    cmd = ["convert", str(src), "-auto-orient", "-crop", geometry, "+repage",
           "-resize", width, "-strip", "-interlace", "Plane", "-quality", quality, str(out)]
    subprocess.run(cmd, check=True)
    return out.stat().st_size


def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def main():
    if not TPL.exists():
        sys.exit("gabarit manquant : %s" % TPL)
    tmp = pathlib.Path("/tmp/cavisa-build")
    tmp.mkdir(parents=True, exist_ok=True)

    html = TPL.read_text(encoding="utf-8")
    for token, (name, geometry, width, quality) in PHOTOS.items():
        if token not in html:
            sys.exit("le gabarit ne porte plus le jeton %s" % token)
        out = tmp / ("%s-%s.jpg" % (name.rsplit(".", 1)[0], width))
        size = prepare(name, geometry, width, quality, out)
        html = html.replace(token, b64(out))
        print("  %-18s %-5s q%-3s %5d Ko  →  base64 %.0f Ko" % (
            name, width, quality, size / 1024, size * 4 / 3 / 1024))

    if "__IMG_" in html:
        sys.exit("un jeton d'image n'a pas été remplacé")

    OUT_CONCEPT.write_text(html, encoding="utf-8")
    PREVIEW.mkdir(parents=True, exist_ok=True)
    OUT_PREVIEW.write_text(html, encoding="utf-8")

    # La vignette du lien WhatsApp : 1200×630, absolue une fois déployée (§20.7).
    subprocess.run(["convert", str(IMG / "cavisa-tryon.jpg"), "-auto-orient",
                    "-resize", "1200x630^", "-gravity", "center", "-extent", "1200x630",
                    "-strip", "-interlace", "Plane", "-quality", "72", str(OUT_OG)], check=True)

    print("\n  page   %s  (%.0f Ko)" % (OUT_CONCEPT.relative_to(ROOT), OUT_CONCEPT.stat().st_size / 1024))
    print("  bundle %s  (%.0f Ko) + og.jpg (%.0f Ko)" % (
        PREVIEW.relative_to(ROOT), OUT_PREVIEW.stat().st_size / 1024, OUT_OG.stat().st_size / 1024))
    print("  les deux copies sont identiques : %s" % (OUT_CONCEPT.read_bytes() == OUT_PREVIEW.read_bytes()))


if __name__ == "__main__":
    main()
