# -*- coding: utf-8 -*-
"""Build amk-site.zip at repo root — the drag/CLI deploy bundle for the
EXISTING amk-cm.vercel.app project.

Contents = the LIVE inventory as exported from Vercel on 08/10/2026 (repo
site/ == live): every deployed HTML page, the Google Search Console
verification file (google08d73756faeade69.html, it MUST stay deployed or the
GSC property loses verification), the brand files (favicon/robots/sitemap) and
ONLY the images the pages actually reference (checked 08/10: every local
src/href/og:image resolves). The concept pages embed their photos as base64,
so the big concept JPGs are intentionally excluded. llms.txt (23/10) is the AI-discovery
file: it is served at the root, so it ships with the pages. NOT shipped: builders,
research notes, DEPLOY.md, SEO-REVIEW, mockup-hero.html (unlinked) and
index.html.backup-pre-king24. Before 08/10 this list held 6 pages and would have
dropped four live pages plus the GSC file: never reuse the old list.

Deploy steps + verification: see site/DEPLOY.md.


Sortie NON versionnée (`.gitignore` : `/amk-site*.zip`) : le bundle se régénère en une
commande. Le zip du 23/10 a été retiré du suivi le 24/10 (`ops/AUDIT-FICHIERS-2026-10-24.md` §3).
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
    # miroir anglais du 23/10 (outil : tools/site/build_en_pages.py) — servi sous /en/
    "en/index.html",
    "en/clinic-bonaberi.html",
    "en/mitoc.html",
]
ROOT_FILES = ["favicon.svg", "robots.txt", "sitemap.xml", "llms.txt",
             "google08d73756faeade69.html"]
THUMBS = [
    # WebP (08/10 : 2,28 Mo de PNG -> 0,47 Mo) ; les deux PNG restants servent d'og:image aux pages en noindex
    "nova.webp", "littleoaks.webp", "crestwood.webp", "clinic.webp",
    "sample-polyclinic.webp", "sample-maternity.webp",
    "sample-polyclinic.png", "sample-maternity.png",
    "og-cover.jpg", "og-nova.jpg", "og-littleoaks.jpg", "og-crestwood.jpg",
    "og-clinic-bonaberi.jpg", "og-mitoc.jpg",
]

import posixpath, re

# --- Les assets sont DÉDUITS des pages, plus recopiés à la main -------------------------
# Jusqu'au 29/10 cette liste était figée depuis l'export du 08/10 : elle ne contenait donc ni
# `fonts/*.woff2`, ni `accueil-2026-10-29.css`, ni `img/hero-douala-dusk*.webp`. Un déploiement
# depuis ce zip aurait servi un accueil sans police, sans feuille de style et sans photo — la page
# était juste, le paquet non. On lit maintenant chaque page (et chaque feuille qu'elle charge) et on
# emporte ce qu'elle référence : le zip ne peut plus prendre du retard sur `site/`.
REF_RE = re.compile(r"""(?:href|src|content)\s*=\s*["']([^"']+)["']""", re.I)
# `srcset` / `imagesrcset` portent plusieurs URL séparées par des virgules (« a.webp 860w, b.webp 1600w ») :
# sans cette lecture, la variante 860 px du héros ne partait pas dans le zip.
SRCSET_RE = re.compile(r"""(?:srcset|imagesrcset)\s*=\s*["']([^"']+)["']""", re.I)
CSS_URL_RE = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""", re.I)
ABS_HOSTS = ("https://amk-cm.vercel.app/", "http://amk-cm.vercel.app/")


def _norm(base: str, ref: str) -> str | None:
    """Chemin relatif à `site/`, ou None si la référence ne désigne pas un fichier du dossier."""
    ref = ref.split("#", 1)[0].split("?", 1)[0].strip()
    if not ref or ref.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
        return None
    host = next((h for h in ABS_HOSTS if ref.startswith(h)), None)
    if host:
        ref = ref[len(host):]
        base = ""
    elif ref.startswith(("http://", "https://", "//")):
        return None
    path = posixpath.normpath(posixpath.join(base, ref)) if base else posixpath.normpath(ref)
    if path.startswith(".."):
        return None
    return path


def assets_of(members: list[str]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    queue = list(members)
    while queue:
        rel = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        src = (SITE / rel)
        if src.suffix.lower() not in (".html", ".css"):
            found.append(rel)
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        refs = REF_RE.findall(text) if src.suffix.lower() == ".html" else []
        for group in SRCSET_RE.findall(text):
            refs += [part.strip().split(" ")[0] for part in group.split(",")]
        refs += CSS_URL_RE.findall(text)
        for ref in refs:
            target = _norm(posixpath.dirname(rel), ref)
            if target and (SITE / target).is_file():
                if target not in seen:
                    found.append(target)
                    queue.append(target)
        found.append(rel)
    # ordre stable et dédoublonné, les pages d'abord
    order = {m: i for i, m in enumerate(members)}
    uniq = sorted(set(found), key=lambda m: (order.get(m, 10_000), m))
    return uniq


members = assets_of(PAGES + ROOT_FILES + ["vercel.json"])

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
