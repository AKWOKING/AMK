#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE — compléter `llms.txt` avec le miroir anglais.

    python3 hosting/build_dm_llms.py --check    # dit combien d'URL manquent
    python3 hosting/build_dm_llms.py            # réécrit le bloc anglais

Le portique de livraison (D5) compare `llms.txt` au `sitemap.xml` : 47 URL anglaises du plan de site
n'y figuraient pas, donc un agent qui lit `llms.txt` ne voyait que la moitié du site. Le bloc français
est écrit à la main (il porte les précisions « 24 montures femme », les horaires) : ce script n'y touche
pas, il ne régénère que le bloc anglais, à partir des fichiers réels — titre de page, moins la marque.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent / "previews" / "dmoptic"
HOST = "https://dmoptiquesarl.com"
MARK = "## English pages"


def title_of(page: Path) -> str:
    s = page.read_text(encoding="utf-8")
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else page.parent.name
    return re.sub(r"\s+—\s+DM OPTIQUE SARL\s*$", "", t)


def url_of(page: Path) -> str:
    rel = page.relative_to(SITE).parent.as_posix()
    return HOST + "/" + ("" if rel == "." else rel + "/")


def block() -> str:
    pages = sorted((SITE / "en").rglob("index.html"))
    main = [p for p in pages if "montures/" not in p.relative_to(SITE).as_posix()
            or p.relative_to(SITE).as_posix().count("/") <= 2]
    fiches = [p for p in pages if p not in main]
    lines = [MARK, "",
             "Mirror of the French pages, for agents that read English. Each page declares its "
             "alternate in `<link rel=\"alternate\" hreflang=\"en\">`.", "",
             "### Sections", ""]
    lines += [f"- [{title_of(p)}]({url_of(p)})" for p in main]
    lines += ["", f"### Frame pages ({len(fiches)})", ""]
    lines += [f"- [{title_of(p)}]({url_of(p)})" for p in fiches]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    path = SITE / "llms.txt"
    cur = path.read_text(encoding="utf-8")
    head = cur.split(MARK)[0].rstrip("\n")
    new = head + "\n\n" + block()
    if args.check:
        added = len([l for l in new.splitlines() if l.startswith("- ")]) - \
                len([l for l in cur.splitlines() if l.startswith("- ")])
        print(f"llms.txt : {added:+d} entrée(s) par rapport à la version en place")
        return 0 if new.strip() == cur.strip() else 1
    path.write_text(new, encoding="utf-8")
    print(f"llms.txt réécrit · {len(new.splitlines())} lignes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
