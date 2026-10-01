#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA LIGNE OPTIC — le constructeur de l'aperçu (24/09/2026, nuit).

Ce que fait ce script, dans l'ordre :
 1. il écrit **l'adresse WhatsApp de chaque lien à partir de son `data-fr`** — c'est la seule source du
    message, donc l'adresse écrite dans le HTML et celle que le JavaScript fabrique sont identiques au
    caractère près (même jeu de caractères que `encodeURIComponent`) ;
 2. il écrit la page d'aperçu (un seul fichier, qui s'ouvre sur n'importe quel téléphone) ;
 3. il en fait la copie déployable dans `hosting/previews/laligne/` et **dessine** la vignette 1200×630
    (`og.jpg`) que WhatsApp affichera avant d'ouvrir le lien (§20.7).

Les cinq visages sont des **portraits d'illustration**, générés pour la page : le cabinet n'a publié
aucune photo de lui, et on ne fabrique pas la vitrine de quelqu'un d'autre — voir
`clients/la-ligne/dossier.md` §5. Chaque forme est montée DEUX fois, et les deux en base64 : une
grande dans le miroir (720×900), une carrée dans le verre du premier écran (320×320, exactement le
cadrage circulaire du verre). Le premier écran regarde un visage à travers une ligne de vue — c'est la
page entière en un objet. La page dit noir sur blanc, sous le miroir, que ce sont des **images
d'illustration** et non des clients du cabinet. La vignette du lien reprend le même portrait, rond,
dans un anneau laque.

Rien n'est inventé : tout ce que la page affirme vient du contrôle approfondi du 24/09
(`clients/la-ligne/dossier.md`) — le registre de l'Ordre, l'annuaire où le cabinet écrit son adresse et
ses quatre services, et quatre guides américains recoupés pour le conseil de visagiste. Horaires, prix,
marques, photos et moyens de paiement : jamais écrits, ils sont dans `a-completer.md`.

Usage :
  python3 demos/build_laligne.py                        # écrit l'aperçu, og.jpg sans adresse
  python3 demos/build_laligne.py --url https://…        # remplit og:url / og:image APRÈS déploiement
"""
import argparse
import base64
import pathlib
import re
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEMOS = ROOT / "demos"
IMG = DEMOS / "img"
TPL = DEMOS / "laligne-v1.tpl.html"
OUT_CONCEPT = DEMOS / "concept-laligne-v1.html"
PREVIEW = ROOT / "hosting" / "previews" / "laligne"
OUT_PREVIEW = PREVIEW / "index.html"
OUT_OG = PREVIEW / "og.jpg"

WA_BASE = "https://wa.me/237683651108?text="
# Le jeu de caractères que `encodeURIComponent` laisse tel quel. Python, par défaut, échapperait
# `!'()*` — et l'adresse statique ne serait plus égale à celle du JavaScript.
SAFE = "!'()*-._~"

# Les couleurs de la page, reprises telles quelles dans la vignette : craie, graphite, laque.
PAPER, INK, LAQUE, GREY = "#F1EFE9", "#14130F", "#8E2B22", "#5F5A4E"


# ── LES CINQ PORTRAITS D'ILLUSTRATION ────────────────────────────────────────────────────────────────
# Le suffixe est celui des radios de la page (`f-ovale`…), donc une forme = un nom, du gabarit au test.
SHAPES = ["ovale", "rond", "carre", "coeur", "oblong"]

# Le cadrage du verre : le cercle couvre le carré central de 88,9 % × 71,1 % du portrait (4:5), soit
# 640 px dans les deux sens. C'est CE carré que le premier écran affiche, agrandi à 320 px.
LENS_CROP = "88.9x71.1%"


def prepare(name, target, quality, out):
    """Couvre la cible puis recadre AU CENTRE (`resize ^` + `extent`) : aucun décalage écrit en dur."""
    src = IMG / name
    if not src.exists():
        sys.exit("portrait manquant : %s" % src)
    subprocess.run(["convert", str(src), "-auto-orient", "-resize", target + "^",
                    "-gravity", "center", "-extent", target,
                    "-strip", "-interlace", "Plane", "-quality", quality, str(out)], check=True)
    return out.stat().st_size


def prepare_lens(name, out, size=320, quality="64"):
    """Le carré du verre : le centre du portrait, recadré sous le cercle du premier écran.

    Le cercle du gabarit fait 192 unités de diamètre dans une boîte 4:5 : il couvre donc le carré
    central de 88,9 % × 71,1 % de la photo, et rien d'autre. On le prépare ici une fois pour toutes —
    le SVG n'a plus qu'à poser un carré sur un carré."""
    src = IMG / name
    if not src.exists():
        sys.exit("portrait manquant : %s" % src)
    subprocess.run(["convert", str(src), "-auto-orient",
                    "-resize", "720x900^", "-gravity", "center", "-extent", "720x900",
                    "-gravity", "center", "-crop", LENS_CROP, "+repage",
                    "-resize", "%dx%d!" % (size, size),
                    "-strip", "-quality", quality, str(out)], check=True)
    return out.stat().st_size


def b64(path):
    return base64.b64encode(path.read_bytes()).decode("ascii")


def fix_whatsapp(html):
    """Chaque `<a class="… wa …">` reçoit l'adresse dérivée de son propre `data-fr`."""
    def one(m):
        tag = m.group(0)
        fr = re.search(r'data-fr="([^"]*)"', tag)
        if not fr:
            return tag
        href = WA_BASE + urllib.parse.quote(fr.group(1), safe=SAFE)
        return re.sub(r'href="[^"]*"', 'href="%s"' % href, tag, count=1)

    out, n = re.subn(r'<a\b[^>]*\bclass="[^"]*\bwa\b[^"]*"[^>]*>', one, html)
    print("✓ %d liens WhatsApp : adresse dérivée du texte français" % n)
    return out


def round_photo(name, size, out):
    """Un portrait, rond : le carré central, masqué en cercle. Pas de navigateur dans le bac pour
    faire une capture d'écran — alors on monte la vignette à la main, avec la vraie photo."""
    r = size // 2
    subprocess.run(["convert", str(IMG / name), "-auto-orient",
                    "-resize", "%dx%d^" % (size, size), "-gravity", "center",
                    "-extent", "%dx%d" % (size, size),
                    "(", "-size", "%dx%d" % (size, size), "xc:none", "-fill", "white",
                    "-draw", "circle %d,%d %d,4" % (r, r, r), ")",
                    "-alpha", "off", "-compose", "CopyOpacity", "-composite",
                    "-strip", str(out)], check=True)
    return out


def draw_og(out, url_label):
    """La carte du lien : la craie, la ligne du regard, et le visage DANS le verre — le même motif que
    le premier écran de la page. Le portrait est une image d'illustration, comme sur la page."""
    size = "1200x630"
    face = round_photo("laligne-visage-carre.jpg", 256, "/tmp/laligne-og-face.png")
    args = ["convert", "-size", size, "xc:%s" % PAPER,
            # la règle du regard, d'un bord à l'autre — la signature de la page
            "-stroke", GREY, "-strokewidth", "2", "-fill", "none",
            "-draw", "line 0,352 1200,352",
            "-draw", "line 60,344 60,360", "-draw", "line 1140,344 1140,360",
            # le verre : son anneau posé SUR la ligne, et le portrait dedans
            "-stroke", LAQUE, "-strokewidth", "5",
            "-draw", "circle 1000,224 1000,93",
            str(face), "-geometry", "+872+96", "-composite"]
    # les mots
    args += ["-font", "DejaVu-Sans-Bold", "-pointsize", "78", "-fill", INK, "-stroke", "none",
             "-annotate", "+78+250", "LA LIGNE OPTIC",
             "-font", "DejaVu-Sans", "-pointsize", "30", "-fill", LAQUE,
             "-annotate", "+82+300", "Optique & lunetterie · Akwa, Douala",
             "-font", "DejaVu-Sans-Bold", "-pointsize", "36", "-fill", INK,
             "-annotate", "+82+430", "Votre visage d'abord. La monture ensuite.",
             "-font", "DejaVu-Sans", "-pointsize", "28", "-fill", GREY,
             "-annotate", "+82+482", "Consultation · Réfraction · Visagiste · Conseil",
             "-annotate", "+82+524", "Cinq visages, cinq lignes — et le conseil qui va avec",
             "-font", "DejaVu-Sans-Bold", "-pointsize", "38", "-fill", INK,
             "-annotate", "+82+596", "683 651 108"]
    if url_label:
        args += ["-font", "DejaVu-Sans", "-pointsize", "24", "-fill", GREY,
                 "-annotate", "+760+600", url_label]
    args += ["-strip", "-quality", "90", str(out)]
    subprocess.run(args, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="", help="adresse de la page déployée, pour og:url / og:image")
    opts = ap.parse_args()

    html = TPL.read_text(encoding="utf-8")
    html = fix_whatsapp(html)

    # ── les cinq portraits : le grand pour le miroir, le carré pour le verre du premier écran ──────
    tmp = pathlib.Path("/tmp/laligne-img")
    tmp.mkdir(parents=True, exist_ok=True)
    total = 0
    for s in SHAPES:
        name = "laligne-visage-%s.jpg" % s
        big = tmp / ("%s-720.jpg" % s)
        lens = tmp / ("%s-320.jpg" % s)
        total += prepare(name, "720x900", "66", big)
        total += prepare_lens(name, lens)
        html = html.replace("__IMG_FACE_%s__" % s.upper(), b64(big))
        html = html.replace("__IMG_LENS_%s__" % s.upper(), b64(lens))
    print("✓ 5 portraits × 2 tailles, embarqués en base64 (%.0f Ko de JPEG)" % (total / 1024))

    if opts.url:
        url = opts.url.rstrip("/") + "/"
        html = html.replace("__OG_URL__", url).replace("__OG_IMAGE__", url + "og.jpg")
        print("✓ og:url → %s" % url)
    else:
        # Sans adresse connue : on laisse des marqueurs NEUTRES — jamais une adresse devinée.
        html = html.replace("__OG_URL__", "").replace("__OG_IMAGE__", "")
        print("! og:url / og:image laissés vides — relancer avec --url après le déploiement")

    for leftover in ("__IMG_", "__WA__", "__OG_"):
        if leftover in html:
            sys.exit("jeton non remplacé : %s" % leftover)
    unresolved = re.findall(r'href="[^"]*%(?:20)?[^"]*"', html)
    if any("__" in h for h in unresolved):
        sys.exit("adresse non résolue : %s" % unresolved[0])

    OUT_CONCEPT.write_text(html, encoding="utf-8")
    PREVIEW.mkdir(parents=True, exist_ok=True)
    OUT_PREVIEW.write_text(html, encoding="utf-8")
    draw_og(OUT_OG, opts.url.rstrip("/") if opts.url else "")
    print("✓ aperçu    : %s (%.1f Ko)" % (OUT_CONCEPT.relative_to(ROOT), OUT_CONCEPT.stat().st_size / 1024))
    print("✓ déployable: %s" % PREVIEW.relative_to(ROOT))
    print("✓ vignette  : %s (%.1f Ko)" % (OUT_OG.relative_to(ROOT), OUT_OG.stat().st_size / 1024))
    print("\nContrôles à lancer avant d'envoyer le lien :")
    print("  python3 tools/qa/audit_html.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_a11y.py --strict %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_hero.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/check_inline_js.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_aeo.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_images.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  node tools/qa/test_laligne_page.mjs")


if __name__ == "__main__":
    main()
