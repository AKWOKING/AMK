#!/usr/bin/env python3
"""
DM OPTIQUE SARL — paquet Cloudflare.

King dépose lui-même le site sur Cloudflare (`dmoptiquesarl.com`). Ce script produit
le seul fichier qu'il téléverse : `dmopticsarl.zip`, à la racine du dépôt.

    python3 demos/pack_dmoptic.py

Ce qu'il fait, dans l'ordre :
  1. vérifie que `hosting/previews/dmoptic/` contient bien les pages attendues
     (`index.html`, `sitemap.xml`, `robots.txt`, `llms.txt`) — pas de zip d'un site vide ;
  2. refait le zip **déterminé** (entrées triées, pas d'entrée de dossier, dates figées) :
     deux packs du même contenu donnent le même fichier ;
  3. relit le zip (`testzip`) et affiche le compte d'entrées, la taille et l'empreinte SHA-256.

Sortie : `dmopticsarl.zip` à la racine · une ligne « zip : N entrées · X Ko · sha256 … ».
"""
import hashlib
import os
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = os.path.join(ROOT, "hosting", "previews", "dmoptic")
OUT = os.path.join(ROOT, "dmopticsarl.zip")
MUST = ["index.html", "sitemap.xml", "robots.txt", "llms.txt", "_headers"]
FIXED_DATE = (2026, 10, 21, 0, 0, 0)


def main():
    missing = [m for m in MUST if not os.path.exists(os.path.join(SITE, m))]
    if missing:
        sys.exit(f"✗ paquet refusé : fichier(s) manquant(s) — {', '.join(missing)}")

    paths = []
    for d, _, files in os.walk(SITE):
        for f in files:
            paths.append(os.path.join(d, f))
    paths.sort()
    if len(paths) < 40:
        sys.exit(f"✗ paquet suspect : {len(paths)} fichiers seulement")

    tmp = OUT + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in paths:
            arc = os.path.relpath(p, SITE).replace(os.sep, "/")
            info = zipfile.ZipInfo(arc, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(p, "rb") as fh:
                z.writestr(info, fh.read())

    with zipfile.ZipFile(tmp) as z:
        bad = z.testzip()
        if bad:
            sys.exit(f"✗ zip corrompu : {bad}")
        n = len(z.namelist())

    os.replace(tmp, OUT)
    h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16]
    ko = os.path.getsize(OUT) // 1024
    print(f"zip : {n} entrées · {ko} Ko · sha256 {h}…")
    print(f"      → {os.path.relpath(OUT, ROOT)}  (à déposer sur Cloudflare)")


if __name__ == "__main__":
    main()
