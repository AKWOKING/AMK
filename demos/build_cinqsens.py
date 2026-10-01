#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CINQ SENS — le constructeur de l'aperçu (24/09/2026).

Ce que fait ce script, dans l'ordre :
 1. il prépare les trois photographies d'illustration (16/9) et les emballe en base64 dans le gabarit
    `demos/cinqsens-v1.tpl.html` ;
 2. il écrit **l'adresse WhatsApp de chaque lien à partir de son `data-fr`** — c'est la seule source du
    message, donc l'adresse écrite dans le HTML et celle que le JavaScript fabrique sont identiques au
    caractère près (même jeu de caractères que `encodeURIComponent`) ;
 3. il écrit la page d'aperçu (un seul fichier, qui s'ouvre sur n'importe quel téléphone) ;
 4. il en fait la copie déployable dans `hosting/previews/cinqsens/` et dessine la vignette 1200×630
    (`og.jpg`) que WhatsApp affichera avant d'ouvrir le lien (§20.7).

Rien n'est inventé ici. Tout ce que la page affirme vient du contrôle approfondi du 24/09
(`clients/cinq-sens/dossier.md`) : les services écrits par le cabinet, les repères de ses propres
publications, les deux numéros qu'il publie. Les horaires sont ceux de **deux annuaires concordants** —
la page les annonce comme « horaires annoncés » et le schéma ne les porte pas. Marques, prix, photos et
moyens de paiement : jamais inventés.

Usage :
  python3 demos/build_cinqsens.py                       # écrit l'aperçu, og.jpg sans adresse
  python3 demos/build_cinqsens.py --url https://…       # remplit og:url / og:image APRÈS déploiement
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
TPL = DEMOS / "cinqsens-v1.tpl.html"
OUT_CONCEPT = DEMOS / "concept-cinqsens-v1.html"
PREVIEW = ROOT / "hosting" / "previews" / "cinqsens"
OUT_PREVIEW = PREVIEW / "index.html"
OUT_OG = PREVIEW / "og.jpg"

WA_BASE = "https://wa.me/237696698136?text="
# Le jeu de caractères que `encodeURIComponent` laisse tel quel. Python, par défaut, échapperait
# `!'()*` — et l'adresse statique ne serait plus égale à celle du JavaScript.
SAFE = "!'()*-._~"

# Une image = une signification (§25) : l'arrivage, les solaires, la boutique. Trois MISES EN SITUATION —
# le cabinet n'a pas encore envoyé ses photos, et la page le dit sous chaque image.
PHOTOS = {
    "__IMG_ARRIVAGE__": ("cinqsens-arrivage.jpg", "900x563", "52"),   # 16/9 — l'arrivage
    "__IMG_SOLAIRES__": ("cinqsens-solaires.jpg", "900x563", "52"),   # 16/9 — les solaires
    "__IMG_CABINET__":  ("cinqsens-cabinet.jpg",  "900x563", "52"),   # 16/9 — la boutique
}


def prepare(name, target, quality, out):
    """Couvre la cible puis recadre AU CENTRE (`resize ^` + `extent`) : aucun décalage écrit en dur."""
    src = IMG / name
    if not src.exists():
        sys.exit("photo manquante : %s" % src)
    subprocess.run(["convert", str(src), "-auto-orient", "-resize", target + "^",
                    "-gravity", "center", "-extent", target,
                    "-strip", "-interlace", "Plane", "-quality", quality, str(out)], check=True)
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


def draw_og(out, url_label):
    """La carte du lien : noir profond, le rail des cinq sens, le nom, les deux cabinets, le numéro.
    Pas de capture d'écran possible dans le bac (aucun navigateur) — donc on la dessine, et elle est vraie."""
    size = "1200x630"
    args = ["convert", "-size", size, "xc:#0C0C10"]
    # le rail des cinq sens, en haut (la signature de la page)
    colors = ["#FF2E7E", "#2C6BFF", "#FFC531", "#12B886", "#FF6B2C"]
    for i, c in enumerate(colors):
        args += ["-fill", c, "-stroke", "none",
                 "-draw", "rectangle %d,0 %d,14" % (i * 240, (i + 1) * 240)]
    # l'anneau, à droite
    args += ["-fill", "none", "-stroke", "#FF2E7E", "-strokewidth", "14",
             "-draw", "circle 980,330 980,470",
             "-stroke", "#F6F4EF", "-strokewidth", "5",
             "-draw", "circle 980,330 980,395",
             "-stroke", "none", "-fill", "#FF2E7E", "-draw", "circle 980,330 980,341"]
    # les mots
    args += ["-font", "DejaVu-Sans-Bold", "-pointsize", "116", "-fill", "#F6F4EF",
             "-annotate", "+78+296", "CINQ SENS",
             "-font", "DejaVu-Sans", "-pointsize", "34", "-fill", "#FF2E7E",
             "-annotate", "+82+352", "Référence Optique Médicale Cinq Sens",
             "-font", "DejaVu-Sans-Bold", "-pointsize", "38", "-fill", "#F6F4EF",
             "-annotate", "+82+428", "Opticien à Douala · Akwa & Brazzaville",
             "-font", "DejaVu-Sans", "-pointsize", "30", "-fill", "#BEBCC8",
             "-annotate", "+82+482", "Examen de la vue · Montures · Solaires · Lentilles",
             "-annotate", "+82+524", "Prothèses oculaires · Livraison à domicile",
             "-font", "DejaVu-Sans-Bold", "-pointsize", "42", "-fill", "#F6F4EF",
             "-annotate", "+82+592", "696 698 136"]
    if url_label:
        args += ["-font", "DejaVu-Sans", "-pointsize", "24", "-fill", "#BEBCC8",
                 "-annotate", "+700+592", url_label]
    args += ["-strip", "-quality", "90", str(out)]
    subprocess.run(args, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="", help="adresse de la page déployée, pour og:url / og:image")
    opts = ap.parse_args()

    html = TPL.read_text(encoding="utf-8")
    tmp = pathlib.Path("/tmp/cinqsens-img")
    tmp.mkdir(exist_ok=True)
    for token, (name, target, quality) in PHOTOS.items():
        if token not in html:
            sys.exit("jeton absent du gabarit : %s" % token)
        out = tmp / ("%s-%s.jpg" % (name.rsplit(".", 1)[0], target))
        size = prepare(name, target, quality, out)
        html = html.replace(token, b64(out))
        print("  %-24s %s → %5.1f Ko" % (name, target, size / 1024))

    html = fix_whatsapp(html)

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
    print("✓ aperçu   : %s (%.1f Ko)" % (OUT_CONCEPT.relative_to(ROOT), OUT_CONCEPT.stat().st_size / 1024))
    print("✓ déployable: %s" % PREVIEW.relative_to(ROOT))
    print("✓ vignette  : %s (%.1f Ko)" % (OUT_OG.relative_to(ROOT), OUT_OG.stat().st_size / 1024))
    print("\nContrôles à lancer avant d'envoyer le lien :")
    print("  python3 tools/qa/audit_html.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_a11y.py --strict %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_images.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/check_inline_js.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_hero.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  python3 tools/qa/audit_aeo.py %s" % OUT_CONCEPT.relative_to(ROOT))
    print("  node tools/qa/test_cinqsens_page.mjs")


if __name__ == "__main__":
    main()
