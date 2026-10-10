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

**v2.3 (08/10/2026, après la réponse du cabinet de 14:58)** — heures mises à jour, formulation rapportée
par King (texte exact du client non transmis) : « Examen de vue : 8h30–13h00 · Autres besoins :
8h30–17h30 » (remplace 8h00–17h30 / consultation 8h30–13h30 du 25/09). Écrites dans les deux langues aux
mêmes endroits (carte d'identité, FAQ visible **et** FAQPage, bloc contact, pied de page). Aucun jour.
Également v2.3 : « Inscrit à l'ONOC » (ruling credentials 08/10) à la place de « depuis 2016 ».

Usage :
  python3 demos/build_dmoptic.py                       # écrit l'aperçu, og.jpg sans adresse
  python3 demos/build_dmoptic.py --url https://…       # remplit og:url / og:image APRÈS déploiement
  python3 demos/build_dmoptic.py --url https://… --logo chemin/logo.png [--logo-mode symbol|full]
      # 10/10 : le logo du cabinet remplace le petit symbole rond (symbol, défaut), ou le symbole ET le
      # texte du nom quand le logo contient déjà le nom (full). Sans --logo, la sortie est inchangée.
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


MARK_RE = re.compile(r'<span class="mark" aria-hidden="true"><svg\b.*?</svg></span>', re.S)
LOGO_CSS = (".brand .logo{height:34px;width:auto;max-width:190px;object-fit:contain;flex:none;mix-blend-mode:multiply}\n"
            ".idtop .logo{height:46px;width:auto;max-width:200px;object-fit:contain;flex:none;mix-blend-mode:multiply}\n"
            "footer.site .logo{background:#fff;border-radius:8px;padding:4px 6px}\n")


def prepare_logo(path, out):
    """Logo du client → PNG 'retaillé' (hauteur max 120 px, marges transparentes ou blanches rognées)."""
    src = pathlib.Path(path)
    if not src.exists():
        sys.exit("logo introuvable : %s" % src)
    subprocess.run(["convert", str(src) + "[0]", "-auto-orient", "-fuzz", "6%", "-trim", "+repage",
                    "-resize", "x120>", "-strip", str(out)], check=True)
    return out


def apply_logo(html, logo_png, mode):
    """Remplace les trois symboles ronds (en-tête, carte d'identité, pied de page) par le logo du client.
    mode « full » : le logo contient déjà le nom → on retire aussi le texte du nom, le logo porte le libellé."""
    uri = "data:image/png;base64," + b64(logo_png)
    alt = "DM OPTIQUE SARL" if mode == "full" else ""
    img = '<img class="logo" src="%s" alt="%s" decoding="async">' % (uri, alt)
    html, n = MARK_RE.subn(lambda m: img, html)
    if n != 3:
        sys.exit("symboles remplacés : %d (attendu 3) — le gabarit a changé" % n)
    if mode == "full":
        html, k = re.subn(r'<span class="brandtxt">DM OPTIQUE <span class="thin">SARL</span></span>', "", html)
        html, j = re.subn(r'<span class="idname">DM OPTIQUE SARL</span>', "", html)
        if k != 2 or j != 1:
            sys.exit("textes du nom retirés : %d + %d (attendu 2 + 1)" % (k, j))
        # les liens « marque » n'ont plus de texte : le nom accessible vient de l'aria-label (l'audit
        # a11y du dépôt ne lit pas l'alt d'une image dans un lien — constaté le 10/10)
        html, q = re.subn(r'<a class="brand" href="#top">', '<a class="brand" href="#top" aria-label="DM OPTIQUE SARL">', html)
        if q != 2:
            sys.exit("liens marque : %d (attendu 2)" % q)
    marker = ".nav{display:none}"
    if html.count(marker) < 1:
        sys.exit("point d'insertion CSS introuvable")
    html = html.replace(marker, LOGO_CSS + marker, 1)
    print("✓ logo du cabinet : %d emplacements (%s)" % (n, mode))
    return html


def draw_og(out, url_label, logo=None):
    """La carte du lien : fond marine, l'anneau, le nom, le numéro. Pas de capture d'écran possible
    dans le bac (aucun navigateur) — donc on la dessine, et elle est vraie."""
    size = "1200x630"
    args = ["convert", "-size", size, "xc:#0A1220"]
    # l'anneau (le motif de la page), en haut à droite
    # v2.2 : l'anneau descend en bas à droite — « DM OPTIQUE SARL » est plus long que « DM OPTIC »
    # et avait besoin de la largeur. Mesuré, pas deviné : à 90 pt, le nom fait 937 px (ImageMagick).
    if logo:
        # le logo du cabinet remplace l'anneau : plaque blanche en bas à droite, logo centré
        args += ["-fill", "#FFFFFF", "-stroke", "none", "-draw", "roundrectangle 820,330 1130,560 20,20"]
    else:
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
    if logo:
        sized = pathlib.Path("/tmp/dmoptic-og-logo.png")
        subprocess.run(["convert", str(logo), "-resize", "270x190>", str(sized)], check=True)
        w, h = [int(x) for x in subprocess.run(["identify", "-format", "%w %h", str(sized)], check=True,
                                               capture_output=True, text=True).stdout.split()]
        x, y = 820 + (310 - w) // 2, 330 + (230 - h) // 2
        subprocess.run(["convert", str(out), str(sized), "-geometry", "+%d+%d" % (x, y), "-composite",
                        "-strip", "-quality", "90", str(out)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="", help="adresse de la page déployée, pour og:url / og:image")
    ap.add_argument("--logo", default="", help="fichier du logo du cabinet (remplace le symbole rond)")
    ap.add_argument("--logo-mode", choices=("symbol", "full"), default="symbol",
                    help="symbol : le texte du nom reste ; full : le logo contient déjà le nom")
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

    logo_png = None
    if opts.logo:
        logo_png = prepare_logo(opts.logo, pathlib.Path("/tmp/dmoptic-logo.png"))
        html = apply_logo(html, logo_png, opts.logo_mode)

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
    draw_og(OUT_OG, opts.url.rstrip("/") if opts.url else "", logo_png)
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
