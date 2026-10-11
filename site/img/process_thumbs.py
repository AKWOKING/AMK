# -*- coding: utf-8 -*-
"""Ramener les vignettes PNG de site/img/ sous le budget de livraison de 400 Ko.

POURQUOI CE SCRIPT EXISTE (1/10/2026). `tools/qa/audit_images.py` est une porte de livraison
obligatoire (`PRE-FLIGHT.md` §1b) et refuse toute image pleine au-delà de 400 Ko (`BUDGET_FULL`).
Deux des quatre vignettes des pages PUBLIQUES et indexables la dépassaient :

    site/img/clinic.png     405 Ko  → creation-site-web-clinique-cameroun.html
    site/img/crestwood.png  626 Ko  → creation-site-web-ecole-cameroun.html

`littleoaks.png` (219 Ko) et `nova.png` (232 Ko) passent : elles ne sont volontairement PAS
touchées ici. Une obligation sans machine derrière n'est qu'une opinion — d'où ce script, qui
refait le travail à l'identique et **vérifie le budget avant d'écrire**.

POURQUOI 800×500, mesuré et non deviné.
  · Affichage réel : `.proof img{aspect-ratio:16/10;object-fit:cover;width:100%}` dans une grille
    de 3 colonnes sous `.wrap{max-width:1160px}` → ~358 px CSS de large, soit ~716 px en 2× DPR.
    800 px couvre donc le retina ; les 1280 px d'origine ne servaient à rien.
  · Redimensionnement LANCZOS + PNG **sans perte** (`optimize=True`). **Aucune quantification de
    palette** : elle ferait tomber crestwood à 144 Ko, mais ajoute du dither sur le petit texte.
    L'écart au rendu réel (mesuré à 358 px, la taille affichée) est ≤ 0,26/255 en moyenne —
    invisible, et sans risque de bandes dans les dégradés.
  · 900 px sans perte ne suffisait pas (crestwood restait à 427 Ko). 800 px passe avec de la marge.

PROVENANCE. Ce sont des captures des pages d'exemple elles-mêmes (`sample-clinic`, Crestwood…).
Si une page d'exemple change, re-capturer avec `node tools/video/capture.mjs --mode hero`,
puis relancer ce script. Il n'y a pas de dossier `raw/` : la source est la page, pas un fichier.

DEUX COPIES. `hosting/samples/img/` est un instantané de `site/img/` (posé par
`hosting/build_samples.py`, un `copytree`). Le script écrit **les deux**, pour qu'elles restent
identiques au octet près — sinon le bundle déployable et le dossier source divergent en silence.

APRÈS CE SCRIPT. `site/img/og-cover.jpg` embarque clinic.png ET crestwood.png
(`site/img/make_og.py`) : le régénérer, sinon la carte de partage montre les anciennes vignettes.

Idempotent : une vignette déjà à la largeur cible n'est pas retouchée.
Usage :  python3 site/img/process_thumbs.py
"""
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent          # site/img
ROOT = HERE.parent.parent
# les deux dossiers qui portent les mêmes vignettes (source + instantané déployable)
DIRS = [HERE, ROOT / "hosting" / "samples" / "img"]

TARGET_W = 800
BUDGET = 400 * 1024          # BUDGET_FULL de tools/qa/audit_images.py — ne pas diverger de lui

# (fichier, raison). Seules les vignettes qui échouent à la porte sont listées.
JOBS = [
    ("clinic.png",    "405 Ko — creation-site-web-clinique-cameroun.html (page publique)"),
    ("crestwood.png", "626 Ko — creation-site-web-ecole-cameroun.html (page publique)"),
]

failed = []
for name, why in JOBS:
    src = HERE / name
    if not src.exists():
        failed.append("%s : absent de %s" % (name, HERE))
        continue
    before = src.stat().st_size
    with Image.open(src) as im:
        w, h = im.size
        rgb = im.convert("RGB")
    if w <= TARGET_W:
        print("=  %-14s déjà %d×%d (%d Ko) — rien à faire" % (name, w, h, before // 1024))
        continue
    target_h = round(TARGET_W * h / w)
    out = rgb.resize((TARGET_W, target_h), Image.LANCZOS)
    for d in DIRS:
        if not d.is_dir():
            failed.append("%s : dossier cible absent %s" % (name, d))
            continue
        p = d / name
        out.save(p, "PNG", optimize=True)
        size = p.stat().st_size
        ok = size <= BUDGET
        print("%s  %-14s %d×%d %4d Ko  →  %d×%d %4d Ko   [%s]  ← %s"
              % ("✓" if ok else "✗", name, w, h, before // 1024,
                 TARGET_W, target_h, size // 1024,
                 "sous budget" if ok else "TOUJOURS AU-DESSUS", why))
        print("      écrit : %s" % p.relative_to(ROOT))
        if not ok:
            failed.append("%s : %d Ko > %d Ko même à %d px" % (name, size // 1024, BUDGET // 1024, TARGET_W))

print()
if failed:
    print("✗ ÉCHEC — rien à livrer tant que ces vignettes dépassent le budget :")
    for f in failed:
        print("   ", f)
    sys.exit(1)
print("✓ les %d vignettes sont sous le budget de %d Ko — relancer :"
      % (len(JOBS), BUDGET // 1024))
print("     python3 tools/qa/audit_images.py site/creation-site-web-clinique-cameroun.html")
print("     python3 tools/qa/audit_images.py site/creation-site-web-ecole-cameroun.html")
print("     python3 site/img/make_og.py        # og-cover.jpg embarque ces deux vignettes")
