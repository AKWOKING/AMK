# -*- coding: utf-8 -*-
"""Build amk-site.zip at repo root — the drag/CLI deploy bundle for the
EXISTING amk-cm.vercel.app project.

Contents = every HTML page in site/ (nameless samples + agency index + the
named mitoc preview), the brand files (favicon/robots/sitemap), and ONLY the
four thumbnails referenced by index.html. The concept pages embed their photos
as base64, so the big concept JPGs are intentionally excluded to keep the
bundle small. Builders and research notes under site/ are not web assets.

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
    "sample-clinic.html",
    "mitoc.html",
]
ROOT_FILES = ["favicon.svg", "robots.txt", "sitemap.xml"]
THUMBS = ["nova.png", "littleoaks.png", "crestwood.png", "clinic.png"]

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
