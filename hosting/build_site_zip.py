# -*- coding: utf-8 -*-
"""Build amk-site.zip at repo root — the drag/CLI deploy bundle for the
EXISTING amk-cm.vercel.app project.

Contents = the LIVE inventory as exported from Vercel on 08/10/2026 (repo
site/ == live): every deployed HTML page, the Google Search Console
verification file (google08d73756faeade69.html, it MUST stay deployed or the
GSC property loses verification), the brand files (favicon/robots/sitemap) and
ONLY the images the pages actually reference (checked 08/10: every local
src/href/og:image resolves). The concept pages embed their photos as base64,
so the big concept JPGs are intentionally excluded. NOT shipped: builders,
research notes, DEPLOY.md, SEO-REVIEW, mockup-hero.html (unlinked) and
index.html.backup-pre-king24. Before 08/10 this list held 6 pages and would have
dropped four live pages plus the GSC file: never reuse the old list.

Deploy steps + verification: see site/DEPLOY.md.
"""
import pathlib, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "amk-site.zip"

PAGES = [
    "index.html",
    "sample-school.html",
    "sample-nursery.html",
    "sample-secondary.html",
    "sample-polyclinic.html",
    "sample-maternity.html",
    "clinic-bonaberi.html",
    "mitoc.html",
    "creation-site-web-ecole-cameroun.html",
    "creation-site-web-clinique-cameroun.html",
]
ROOT_FILES = ["favicon.svg", "robots.txt", "sitemap.xml", "google08d73756faeade69.html"]
THUMBS = [
    # WebP (08/10 : 2,28 Mo de PNG -> 0,47 Mo) ; les deux PNG restants servent d'og:image aux pages en noindex
    "nova.webp", "littleoaks.webp", "crestwood.webp", "clinic.webp",
    "sample-polyclinic.webp", "sample-maternity.webp",
    "sample-polyclinic.png", "sample-maternity.png",
    "og-cover.jpg", "og-nova.jpg", "og-littleoaks.jpg", "og-crestwood.jpg",
    "og-clinic-bonaberi.jpg", "og-mitoc.jpg",
]

members = PAGES + ROOT_FILES + [f"img/{t}" for t in THUMBS]

if OUT.exists():
    OUT.unlink()
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for m in members:
        p = SITE / m
        assert p.exists(), f"missing {p}"
        z.write(p, m)
print(f"wrote {OUT.relative_to(ROOT)} with {len(members)} files")
for m in members:
    print("  ", m)
