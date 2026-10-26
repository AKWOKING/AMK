#!/usr/bin/env python3
"""dm_index_surface — la surface d'indexation du site DM OPTIQUE, et sa porte.

Pourquoi ce fichier existe
--------------------------
Le 23/10, Search Console disait : **102 pages non indexées, 4 indexées**, dont 89 en
« Discovered – currently not indexed ». Le site demandait à Google d'indexer **96 URL** alors que
**80 d'entre elles** (40 fiches de montures × FR/EN) ne contiennent qu'un titre, une phrase, trois
photos et quatre lignes de faits. Google a tranché tout seul : il a découvert, il n'est pas venu.

Le 26/10, un 403 est apparu au bord du réseau (8 pages) : c'est un second problème, distinct, qui se
règle dans Cloudflare (`clients/dm-optic/seo/RUNBOOK-403-2026-10-26.md`). Ce script ne le touche pas.

Ce qu'il fait
-------------
1. **`--apply`** : passe les fiches de montures en `noindex,follow` (elles restent en ligne, liées
   depuis les galeries, et restent le lien qu'on envoie sur WhatsApp — elles cessent seulement de
   demander une place dans l'index), puis réécrit `sitemap.xml` avec **les seules pages qui ont du
   contenu** : 8 françaises + 8 anglaises = **16 URL**.
2. **`--check`** : vérifie l'invariant et échoue s'il est rompu. C'est la porte : une règle sans
   contrôle est un trou. Appelée avant chaque publication (`.github/workflows/deploy-dmoptic.yml`).

Ce qu'il ne fait pas
--------------------
- Il **ne supprime aucune page** : l'envoi par WhatsApp continue de fonctionner, à l'identique.
- Il **ne reconstruit pas** le site : le gabarit de l'accueil a changé le 24/10 et une reconstruction
  réécrirait 99 fichiers (design non demandé). Le correctif est appliqué aux fichiers publiés, et la
  fabrique (`demos/build_dmoptic_montures.py`) porte le même interrupteur pour un futur build propre.
- Il **n'invente rien** : la liste des fiches vient de `clients/dm-optic/site/frames.json`, la liste
  des pages cœur est le complément, mesuré sur le disque.

La liste blanche
----------------
`clients/dm-optic/seo/index-whitelist.txt` : un chemin par ligne (`/montures/femmes/f01-.../`).
Une fiche listée là **reste indexable**. On n'y met que ce que Google a **déjà** indexé — on ne
retire jamais du champ ce qu'il a accepté. Le fichier est vide au 26/10 : les 4 URL indexées ne sont
pas connues avant l'extraction Search Console (étape 3 du plan).

Usage
-----
    python3 tools/ops/dm_index_surface.py --apply
    python3 tools/ops/dm_index_surface.py --check     # rc=0 si la surface est celle qu'on a décidée
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SITE = RACINE / "hosting/previews/dmoptic"
FRAMES = RACINE / "clients/dm-optic/site/frames.json"
WHITELIST = RACINE / "clients/dm-optic/seo/index-whitelist.txt"
SITEMAP = SITE / "sitemap.xml"

ROBOTS = '<meta name="robots" content="noindex,follow">'
ORDRE_COEUR = ["/", "/montures/", "/montures/femmes/", "/montures/hommes/", "/montures/enfants/",
               "/examen-de-vue/", "/le-cabinet/", "/contact/"]


def base() -> str:
    """L'hôte canonique, lu dans l'accueil — jamais écrit deux fois."""
    m = re.search(r'<link rel="canonical" href="(https://[^/"]+)/?"',
                  (SITE / "index.html").read_text(encoding="utf-8"))
    if not m:
        sys.exit("accueil sans canonical absolu : impossible de bâtir le sitemap")
    return m.group(1)


def fiches() -> list[str]:
    """Les chemins des fiches de montures, FR et EN, dans l'ordre du fichier de données."""
    frames = json.loads(FRAMES.read_text(encoding="utf-8"))
    out: list[str] = []
    for f in frames:
        p = f"/montures/{f['categorie']}/{f['slug']}/"
        out += [p, "/en" + p]
    return out


def whitelist() -> set[str]:
    if not WHITELIST.exists():
        return set()
    out = set()
    for ligne in WHITELIST.read_text(encoding="utf-8").splitlines():
        l = ligne.split("#", 1)[0].strip()
        if l:
            out.add(l if l.endswith("/") else l + "/")
    return out


def coeur() -> list[str]:
    """Les pages qui ont du contenu : 8 françaises + leurs 8 miroirs anglais."""
    fr = [p for p in ORDRE_COEUR if (SITE / p.strip("/") / "index.html").exists()]
    en = [x for x in ("/en" + p for p in fr) if (SITE / x.strip("/") / "index.html").exists()]
    return fr + en


def fichier(path: str) -> Path:
    return SITE / path.strip("/") / "index.html"


def applique() -> None:
    garde = whitelist()
    a_noindex = [p for p in fiches() if p not in garde]
    changes = 0
    for p in a_noindex:
        f = fichier(p)
        if not f.exists():
            sys.exit(f"fiche absente du disque : {p}")
        html = f.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="noindex', html):
            continue
        if re.search(r'<meta name="robots"[^>]*>', html):
            html = re.sub(r'<meta name="robots"[^>]*>', ROBOTS, html, count=1)
        else:
            html = html.replace("</head>", "  " + ROBOTS + "\n</head>", 1)
        f.write_text(html, encoding="utf-8")
        changes += 1
    print(f"  fiches en noindex,follow : {changes} écrite(s), "
          f"{len(a_noindex) - changes} déjà conforme(s), {len(garde)} en liste blanche")

    # Sitemap : les pages cœur, et rien d'autre. lastmod conservé quand il existait (on ne prétend
    # pas qu'une page a changé quand seul son en-tête robots a bougé).
    ancien = {}
    if SITEMAP.exists():
        for loc, lm in re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>",
                                  SITEMAP.read_text(encoding="utf-8")):
            ancien[loc] = lm
    h = base()
    urls = []
    for p in coeur() + sorted(whitelist()):
        loc = h + p
        lm = ancien.get(loc)
        urls.append(f"  <url><loc>{loc}</loc>" + (f"<lastmod>{lm}</lastmod>" if lm else "") + "</url>")
    SITEMAP.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- Surface d'indexation décidée le 26/10/2026 : les 8 pages qui ont du contenu, et leurs\n"
        "     8 miroirs anglais. Les 80 fiches de montures restent en ligne mais en noindex,follow —\n"
        "     elles servent au lien WhatsApp, pas au référencement. Voir\n"
        "     clients/dm-optic/seo/DIAGNOSTIC-INDEXATION-2026-10-26.md §3.3 et\n"
        "     tools/ops/dm_index_surface.py (porte : --check). -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(u + "\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    print(f"  sitemap : {len(urls)} URL (avant : 96)")


def check() -> list[str]:
    """Les quatre invariants. Chacun nomme le fichier et la règle, jamais « erreur »."""
    pbs: list[str] = []
    garde = whitelist()
    noindex_attendu = 0
    for p in fiches():
        html = fichier(p).read_text(encoding="utf-8")
        est_noindex = bool(re.search(r'<meta name="robots" content="noindex', html))
        if p in garde:
            if est_noindex:
                pbs.append(f"{p} est en liste blanche mais porte noindex — la liste blanche perd")
        elif not est_noindex:
            noindex_attendu += 1
            pbs.append(f"{p} n'est pas en noindex alors que c'est une fiche — la surface dérive")
    for p in coeur():
        html = fichier(p).read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="noindex', html):
            pbs.append(f"{p} est une page cœur et porte noindex — elle sortirait de l'index")

    if not SITEMAP.exists():
        return pbs + ["sitemap.xml absent"]
    texte = SITEMAP.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", texte)
    attendu = {base() + p for p in coeur() + sorted(garde)}
    if len(locs) != len(set(locs)):
        pbs.append(f"sitemap : {len(locs)} URL dont {len(locs) - len(set(locs))} doublon(s)")
    manquantes = attendu - set(locs)
    en_trop = set(locs) - attendu
    if manquantes:
        pbs.append(f"sitemap : {len(manquantes)} page(s) cœur absente(s) — {sorted(manquantes)[:3]}")
    if en_trop:
        pbs.append(f"sitemap : {len(en_trop)} URL qui ne devraient pas y être — {sorted(en_trop)[:3]}")
    if len(locs) > 16 + len(garde) * 1:
        pbs.append(f"sitemap : {len(locs)} URL (plafond décidé : 16 + liste blanche)")
    return pbs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--apply", action="store_true", help="écrire la surface (noindex + sitemap)")
    g.add_argument("--check", action="store_true", help="vérifier la surface (rc=1 si elle dérive)")
    a = ap.parse_args()

    if a.apply:
        print("SURFACE D'INDEXATION — application")
        applique()
        pbs = check()
        print(f"  contrôle après écriture : {'OK' if not pbs else str(len(pbs)) + ' problème(s)'}")
        for p in pbs:
            print("   ✗", p)
        return 1 if pbs else 0

    pbs = check()
    print("SURFACE D'INDEXATION — contrôle")
    print(f"  pages cœur indexables : {len(coeur())} · fiches noindex : "
          f"{len([p for p in fiches() if p not in whitelist()])} · liste blanche : {len(whitelist())}")
    for p in pbs:
        print("  ✗", p)
    print(f"  {'OK' if not pbs else 'DÉRIVE'}")
    return 1 if pbs else 0


if __name__ == "__main__":
    raise SystemExit(main())
