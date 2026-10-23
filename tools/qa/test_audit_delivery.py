#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le témoin de la porte de livraison — le 23/10/2026.

Un portique qui trouve « 0 faute » sans avoir mordu une seule fois ne prouve rien. Nos cinq contrôles
(html, a11y, images, reveal, seo) disaient tous verts le matin où un audit extérieur a trouvé **deux
P1** sur le site DM : pas de navigation sous 980 px, et un cache à zéro sur toutes les images. Ce test
monte un site **sain**, vérifie qu'il passe (aucune P1, aucune P2), puis casse **une chose à la fois**
et vérifie que le portique la nomme.

Pièges joués :
  1. site sain                                                  → 0 P1, 0 P2
  2. nav cachée sous un point de rupture sans bouton de menu    → D1 P1
  3. `/*.webp` dans `_headers` (motif que l'hôte n'applique pas) → D2 P1
  4. aucune règle de cache sur les images                      → D2 P1
  5. cache des polices absent                                  → D2 P2
  6. fichiers d'icônes absents                                 → D3 P2
  7. `https://hote//fichier` dans le JSON-LD                   → D4 P2
  8. URL anglaise du sitemap absente de llms.txt               → D5 P2
  9. `og:image` en WebP sans dimensions                        → D6 P2
 10. `price` dans le JSON-LD                                   → D7 P1
 11. fiche produit sans `Product`                              → D7 P2
 12. HSTS absent                                               → D8 P2
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "audit_delivery.py")

HOST = "https://exemple.test"

HEADERS_OK = """/*
  X-Content-Type-Options: nosniff
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'
  Cache-Control: public, max-age=0, must-revalidate
/assets/*
  Cache-Control: public, max-age=604800
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
"""

NAV_OK = """<nav class="nav" aria-label="Sections"><a href="/montures/">Montures</a> <a href="/contact/">Contact</a></nav>"""
NAV_HIDDEN = """<style>.nav{display:none}@media(min-width:980px){.nav{display:flex}}</style>""" + NAV_OK

HEAD_OK = """<meta name="viewport" content="width=device-width,initial-scale=1">
<style>@font-face{font-family:X;src:url("/fonts/f.woff2") format("woff2")}</style>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:image" content="https://exemple.test/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">"""

HOME_LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Exemple",
 "telephone":"+237 600 000 000","address":{"@type":"PostalAddress","streetAddress":"Rue 1"},
 "sameAs":["https://www.facebook.com/exemple"]}
</script>"""

PRODUCT_LD = """<script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://exemple.test/"}]},
 {"@type":"Product","name":"Monture F01","image":"https://exemple.test/assets/a.webp","sku":"F01"}]}
</script>"""


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def page(title, body, head=HEAD_OK):
    return ("<!doctype html><html lang=\"fr\"><head><meta charset=\"utf-8\"><title>%s</title>%s</head>"
            "<body>%s<img src=\"/assets/a.webp\" width=\"100\" height=\"100\" alt=\"\"></body></html>"
            % (title, head, body))


def build(root):
    write(os.path.join(root, "index.html"), page("Accueil", NAV_OK + HOME_LD))
    write(os.path.join(root, "montures", "femmes", "f01", "index.html"),
          page("F01", NAV_OK + PRODUCT_LD))
    write(os.path.join(root, "contact", "index.html"), page("Contact", NAV_OK))
    write(os.path.join(root, "en", "index.html"), page("Home", NAV_OK + HOME_LD))
    write(os.path.join(root, "og.jpg"), "x")
    for name in ("favicon.ico", "favicon.svg", "apple-touch-icon.png"):
        write(os.path.join(root, "assets", name), "x")
    write(os.path.join(root, "assets", "a.webp"), "x")
    write(os.path.join(root, "fonts", "f.woff2"), "x")
    write(os.path.join(root, "_headers"), HEADERS_OK)
    write(os.path.join(root, "sitemap.xml"),
          "<urlset>%s</urlset>" % "".join("<url><loc>%s%s</loc></url>" % (HOST, p) for p in
                                          ("/", "/montures/femmes/f01/", "/contact/", "/en/")))
    write(os.path.join(root, "llms.txt"),
          "\n".join("%s%s" % (HOST, p) for p in ("/", "/montures/femmes/f01/", "/contact/", "/en/")))
    return root


def run(site, strict=False):
    cmd = [sys.executable, TOOL, site, "--base", HOST]
    if strict:
        cmd.append("--strict")
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


ok = fail = 0


def check(cond, label):
    global ok, fail
    if cond:
        ok += 1
        print("  ✓ " + label)
    else:
        fail += 1
        print("  ✗ " + label)


def has(out, code, sev):
    return ("[%s] %s" % (sev, code)) in out


def main():
    tmp = tempfile.mkdtemp(prefix="delivery-")
    try:
        site = build(os.path.join(tmp, "good"))
        rc, out = run(site)
        check(rc == 0 and "0 P1 · 0 P2" in out, "site sain : 0 P1, 0 P2, rc=0")

        def broken(name, mutate, code, sev, strict_rc=None):
            d = os.path.join(tmp, name)
            shutil.copytree(site, d)
            mutate(d)
            rc, out = run(d, strict=strict_rc is not None)
            check(has(out, code, sev), "%s → %s %s" % (name, code, sev))
            if strict_rc is not None:
                check(rc == strict_rc, "%s → code de sortie %d" % (name, strict_rc))
            return out

        def hide_nav(d):
            write(os.path.join(d, "index.html"), page("Accueil", NAV_HIDDEN + HOME_LD))

        broken("nav-cachee", hide_nav, "D1", "P1", strict_rc=1)

        def bad_pattern(d):
            with open(os.path.join(d, "_headers"), "a", encoding="utf-8") as f:
                f.write("/*.webp\n  Cache-Control: public, max-age=604800\n")

        broken("motif-invalide", bad_pattern, "D2", "P1")

        def no_cache(d):
            write(os.path.join(d, "_headers"), HEADERS_OK.replace(
                "/assets/*\n  Cache-Control: public, max-age=604800\n", ""))

        broken("cache-images-absent", no_cache, "D2", "P1")

        def no_font_cache(d):
            write(os.path.join(d, "_headers"), HEADERS_OK.replace(
                "/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n", ""))

        broken("cache-polices-absent", no_font_cache, "D2", "P2")

        def no_favicon(d):
            for n in ("favicon.ico", "favicon.svg", "apple-touch-icon.png"):
                os.remove(os.path.join(d, "assets", n))

        broken("icones-absentes", no_favicon, "D3", "P2")

        def dbl(d):
            write(os.path.join(d, "index.html"), page(
                "Accueil", NAV_OK + HOME_LD,
                HEAD_OK.replace("https://exemple.test/og.jpg", "https://exemple.test//og.jpg")))

        broken("double-barre", dbl, "D4", "P2", strict_rc=1)

        def llms(d):
            write(os.path.join(d, "llms.txt"), "\n".join(
                "%s%s" % (HOST, p) for p in ("/", "/montures/femmes/f01/", "/contact/")))

        broken("llms-incomplet", llms, "D5", "P2")

        def webp_og(d):
            write(os.path.join(d, "index.html"), page(
                "Accueil", NAV_OK + HOME_LD,
                HEAD_OK.replace("https://exemple.test/og.jpg", "https://exemple.test/assets/a.webp")))

        broken("og-webp", webp_og, "D6", "P2")

        def price(d):
            write(os.path.join(d, "montures", "femmes", "f01", "index.html"), page(
                "F01", NAV_OK + PRODUCT_LD.replace('"sku":"F01"',
                                                   '"sku":"F01","offers":{"@type":"Offer","price":"45000"}')))

        broken("prix-dans-jsonld", price, "D7", "P1", strict_rc=1)

        def no_product(d):
            write(os.path.join(d, "montures", "femmes", "f01", "index.html"),
                  page("F01", NAV_OK + PRODUCT_LD.replace('{"@type":"Product","name":"Monture F01","image":'
                                                          '"https://exemple.test/assets/a.webp","sku":"F01"}', "{}")))

        broken("fiche-sans-product", no_product, "D7", "P2")

        def no_hsts(d):
            write(os.path.join(d, "_headers"),
                  HEADERS_OK.replace("  Strict-Transport-Security: max-age=31536000; includeSubDomains\n", ""))

        broken("sans-hsts", no_hsts, "D8", "P2")

        print("\n%d assertion(s) verte(s), %d échec(s) — la porte de livraison mord sur les douze pièges."
              % (ok, fail))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
