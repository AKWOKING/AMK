#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIC — le constructeur de l'aperçu (24/09/2026).

Ce que fait ce script, dans l'ordre :
 1. il prépare les cinq photographies d'illustration (quatre en 16/10 — services, vitrine des montures —
    et une en 4/3 pour l'examen de la vue) et les emballe en base64 dans le gabarit
    `demos/dmoptic-v1.tpl.html` ;
 2. il écrit **l'adresse WhatsApp de chaque lien à partir de son `data-fr`** — c'est la seule source du
    message, donc l'adresse écrite dans le HTML et celle que le JavaScript fabrique sont identiques au
    caractère près (même jeu de caractères que `encodeURIComponent`) ;
 3. il écrit la page d'aperçu (un seul fichier, qui s'ouvre sur n'importe quel téléphone) ;
 4. il en fait la copie déployable dans `hosting/previews/dmoptic/` et dessine la vignette 1200×630
    (`og.jpg`) que WhatsApp affichera avant d'ouvrir le lien (§20.7).

Rien n'est inventé ici. Les faits du cabinet viennent de deux endroits, et de deux seulement :
le registre de l'Ordre (inscription 021/2016, arrêté 0382, titulaire M. Domche Noumbi, Douala) et **le
message du cabinet lui-même**. Depuis la v2.1, les détails de registre ne sont PLUS écrits sur la page
(ils restent dans les données structurées) : le patient n'en a pas besoin.

**v2.2 (25/09/2026, après-midi)** — M. Domche Noumbi a envoyé « Quelques Modifications » à 16:19 :

    • DM OPTIQUE SARL
    • DOUALA/ BONABERI/ NDOBO MAYOR- IMMEUBLE WEST HOTEL
    • HORAIRES : Ouverture 8h00 / Fermeture 17h30 · CONSULTATION : 8H30-13H30

Les trois sont écrits tels quels, dans les deux langues, à **onze endroits** de la page (titre, mot-
symbole, premier écran, carte d'identité, les six messages WhatsApp, bloc contact, réponses des
questions — visibles **et** dans le schéma FAQPage, mot pour mot —, fiche .vcf, pied de page, schéma
`PostalAddress`). Le nom du fichier .vcf suit. **Ce qu'on n'écrit toujours pas** : les jours
d'ouverture (il ne les a pas donnés), les prix, les marques. Les cinq photos restent des mises en
situation, légendées « Photo d'illustration ».

Usage :
  python3 demos/build_dmoptic.py                       # écrit l'aperçu, og.jpg sans adresse
  python3 demos/build_dmoptic.py --url https://…       # remplit og:url / og:image APRÈS déploiement
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
TPL = DEMOS / "dmoptic-v1.tpl.html"
OUT_CONCEPT = DEMOS / "concept-dmoptic-v1.html"
PREVIEW = ROOT / "hosting" / "previews" / "dmoptic"
OUT_PREVIEW = PREVIEW / "index.html"
OUT_OG = PREVIEW / "og.jpg"

WA_BASE = "https://wa.me/237656122239?text="
# Le jeu de caractères que `encodeURIComponent` laisse tel quel. Python, par défaut, échapperait
# `!'()*` — et l'adresse statique ne serait plus égale à celle du JavaScript (l'écart qui a déjà
# coûté un contrôle le 24/09).
SAFE = "!'()*-._~"

# Une image = une signification (§25) : l'objet qu'on vient chercher, la vitrine des montures (trois
# familles), et l'instrument qui mesure. Cinq images, toutes des MISES EN SITUATION — aucune photo du
# cabinet n'existe encore, et la page le dit (« Photos d'illustration »).
PHOTOS = {
    "__IMG_LUNETTES__": ("dmoptic-lunettes.jpg", "900x563", "50"),   # 16/10 — les services
    "__IMG_MONTURES__": ("dmoptic-montures.jpg", "900x563", "50"),   # 16/10 — la vitrine : lunettes de vue
    "__IMG_SOLAIRES__": ("dmoptic-solaires.jpg", "900x563", "50"),   # 16/10 — la vitrine : solaires
    "__IMG_ENFANTS__":  ("dmoptic-enfants.jpg", "900x563", "50"),   # 16/10 — la vitrine : enfants
    "__IMG_MESURE__":   ("dmoptic-mesure.jpg",  "900x675", "50"),   # 4/3  — l'examen de la vue (bande)
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
    """La carte du lien : fond marine, l'anneau, le nom, le numéro. Pas de capture d'écran possible
    dans le bac (aucun navigateur) — donc on la dessine, et elle est vraie."""
    size = "1200x630"
    args = ["convert", "-size", size, "xc:#0A1220"]
    # l'anneau (le motif de la page), en haut à droite
    # v2.2 : l'anneau descend en bas à droite — « DM OPTIQUE SARL » est plus long que « DM OPTIC »
    # et avait besoin de la largeur. Mesuré, pas deviné : à 90 pt, le nom fait 937 px (ImageMagick).
    args += ["-fill", "none", "-stroke", "#2A5CB8", "-strokewidth", "16",
             "-draw", "circle 1058,452 1058,574",
             "-stroke", "#4E7BD4", "-strokewidth", "7",
             "-draw", "circle 1058,452 1058,501",
             "-stroke", "#E0703A", "-strokewidth", "12", "-draw",
             "path 'M 988,402 A 90 90 0 0 1 1058,362'"]
    # les mots
    args += ["-stroke", "none", "-font", "DejaVu-Sans-Bold", "-pointsize", "90",
             "-fill", "#FFFFFF", "-annotate", "+82+300", "DM OPTIQUE SARL",
             "-font", "DejaVu-Sans", "-pointsize", "33", "-fill", "#A9B8CF",
             "-annotate", "+86+372", "Cabinet d'optique médicale · Bonabéri",
             "-font", "DejaVu-Sans-Bold", "-pointsize", "46", "-fill", "#FFFFFF",
             "-annotate", "+86+455", "656 122 239",
             "-font", "DejaVu-Sans", "-pointsize", "31", "-fill", "#E0703A",
             "-annotate", "+86+522", "Inscrit à l'ONOC"]
    if url_label:
        args += ["-font", "DejaVu-Sans", "-pointsize", "26", "-fill", "#6C7890",
                 "-annotate", "+86+580", url_label]
    args += ["-strip", "-quality", "90", str(out)]
    subprocess.run(args, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="", help="adresse de la page déployée, pour og:url / og:image")
    opts = ap.parse_args()

    html = TPL.read_text(encoding="utf-8")
    tmp = pathlib.Path("/tmp/dmoptic-img")
    tmp.mkdir(exist_ok=True)
    for token, (name, target, quality) in PHOTOS.items():
        token = token.strip()
        if token not in html:
            sys.exit("jeton absent du gabarit : %s" % token)
        out = tmp / ("%s-%s.jpg" % (name.rsplit(".", 1)[0], target))
        size = prepare(name, target, quality, out)
        html = html.replace(token, b64(out))
        print("  %-22s %s → %5.1f Ko" % (name, target, size / 1024))

    html = fix_whatsapp(html)

    if opts.url:
        url = opts.url.rstrip("/") + "/"
        html = html.replace("__OG_URL__", url).replace("__OG_IMAGE__", url + "og.jpg")
        print("✓ og:url → %s" % url)
    else:
        # Sans adresse connue : on laisse des marqueurs NEUTRES et un commentaire d'avertissement —
        # jamais une adresse devinée (une URL morte coûte plus qu'une heure d'attente).
        html = html.replace("__OG_URL__", "").replace("__OG_IMAGE__", "")
        print("! og:url / og:image laissés vides — relancer avec --url après le déploiement")

    for leftover in ("__IMG_", "__WA__"):
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
    print("  node tools/qa/test_dmoptic_page.mjs")


if __name__ == "__main__":
    main()
