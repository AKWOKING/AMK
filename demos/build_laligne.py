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

**Il n'y a aucune photographie à préparer** : la page de La Ligne Optic est entièrement **dessinée**
(SVG). Le cabinet n'a publié aucune photo, et on ne fabrique pas la vitrine de quelqu'un d'autre — voir
`clients/la-ligne/dossier.md` §5. La vignette elle-même est un dessin, fait ici avec ImageMagick.

Rien n'est inventé : tout ce que la page affirme vient du contrôle approfondi du 24/09
(`clients/la-ligne/dossier.md`) — le registre de l'Ordre, l'annuaire où le cabinet écrit son adresse et
ses quatre services, et quatre guides américains recoupés pour le conseil de visagiste. Horaires, prix,
marques, photos et moyens de paiement : jamais écrits, ils sont dans `a-completer.md`.

Usage :
  python3 demos/build_laligne.py                        # écrit l'aperçu, og.jpg sans adresse
  python3 demos/build_laligne.py --url https://…        # remplit og:url / og:image APRÈS déploiement
"""
import argparse
import pathlib
import re
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEMOS = ROOT / "demos"
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
    """La carte du lien : la craie, la ligne du regard, un visage et une monture DESSINÉS — et pas une
    photographie, parce qu'il n'y en a pas. Pas de capture d'écran possible dans le bac (aucun
    navigateur) : on la dessine, et elle est vraie."""
    size = "1200x630"
    args = ["convert", "-size", size, "xc:%s" % PAPER,
            # la règle du regard, d'un bord à l'autre — la signature de la page
            "-stroke", GREY, "-strokewidth", "2", "-fill", "none",
            "-draw", "line 0,352 1200,352",
            "-draw", "line 60,344 60,360", "-draw", "line 1140,344 1140,360",
            # le visage, à droite
            "-stroke", INK, "-strokewidth", "5",
            "-draw", "ellipse 930,300 108,150 0,360",
            "-stroke", GREY, "-strokewidth", "3",
            "-draw", "path 'M 862,214 C 848,214 838,222 832,232'",
            "-draw", "path 'M 998,214 C 1012,214 1022,222 1028,232'",
            # la monture, par-dessus la ligne
            "-stroke", LAQUE, "-strokewidth", "8",
            "-draw", "roundrectangle 852,330 926,384 12,12",
            "-draw", "roundrectangle 934,330 1008,384 12,12",
            "-stroke", LAQUE, "-strokewidth", "6",
            "-draw", "path 'M 926,340 q 16,-9 8,0'",
            "-draw", "line 852,338 812,324", "-draw", "line 1008,338 1048,324"]
    # les mots
    args += ["-font", "DejaVu-Sans-Bold", "-pointsize", "92", "-fill", INK, "-stroke", "none",
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
