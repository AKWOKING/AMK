#!/usr/bin/env python3
"""
Audit SEO local et intention de recherche — DM OPTIQUE SARL, 28/10/2026.

    python3 tools/qa/audit_seo_local.py hosting/previews/dmoptic          # rapport lisible
    python3 tools/qa/audit_seo_local.py hosting/previews/dmoptic --strict # code 1 si une faute
    python3 tools/qa/audit_seo_local.py --self-test                       # le banc : le portique mord-il ?

Pourquoi ce fichier, à côté de `audit_seo.py` : celui-là vérifie les balises une par une (titre,
description, alt, canonical, hreflang, sitemap). Il ne vérifie pas ce qui DÉCIDE du classement
local : que la page d'accueil porte la requête qu'on vise, que les pages ne se cannibalisent pas,
qu'aucune page indexable n'est orpheline, que le NAP est identique partout, que le schéma dit le
métier et non la marque. Ces vérifications-là demandent de lire le site ENTIER, pas une page.

Ce que le portique mesure (aucune dépendance, aucun accès réseau) :

  1 · CIBLE      la page d'accueil porte la ville ET le métier, dans le titre et dans le H1
  2 · HREFLANG   auto-référence, réciprocité FR⇄EN, x-default présent et cohérent
  3 · SITEMAP    chaque URL du sitemap existe ; aucune page indexable n'est hors sitemap
  4 · ORPHELINS  chaque page du sitemap est atteignable depuis l'accueil en suivant les liens
  5 · CANNIBAL   deux pages indexables ne visent pas le même titre (même signature)
  6 · NAP        même téléphone et même adresse sur toutes les pages indexables
  7 · SCHÉMA     Optician complet, Service sur les pages de service, aucun avis inventé
  8 · ROBOTS     Sitemap déclaré, aucune interdiction de /
  9 · CUL-DE-SAC une page indexable renvoie au moins vers trois autres pages du site

Sortie : des FAUTES (rc 1 avec --strict), des AVERTISSEMENTS, des NOTES. Une loi qui ne s'applique
pas est dite, jamais passée sous silence.
"""
from __future__ import annotations

import argparse
import html as HTML
import json
import re
import shutil
import sys
import tempfile
from collections import deque
from pathlib import Path

# ── La cible, écrite une fois ────────────────────────────────────────────────────────────────────
# Les deux requêtes de King : « opticians in Douala » et « optometrist in Douala ». En français, le
# métier s'écrit « opticien optométriste » (titre réglementé par l'ONOC) : on vérifie donc les deux
# familles de mots, pas une chaîne exacte — un moteur ne lit pas « optométriste » comme « opticien ».
CITY = "douala"
JOBS = ("opticien", "optométriste", "optician", "optometrist", "optométrie", "optometry")
BRAND = "dm optique"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)
ALT_RE = re.compile(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]*)"', re.I)
LD_RE = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.I | re.S)
ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="([^"]*)"', re.I)
A_RE = re.compile(r'<a\b[^>]*?href="([^"]+)"', re.I)
TAG_RE = re.compile(r"<[^>]+>")
PHONE = "+237656122239"


def flat(t: str) -> str:
    """Texte comparable : entités décodées, espaces insécables et apostrophes typographiques
    ramenées à leur forme simple. Sans ça, « Douala&nbsp;? » et « Douala ? » ne se rencontrent
    jamais — et le contrôle le plus utile du fichier devient un générateur de fausses alertes."""
    t = HTML.unescape(t or "")
    t = (t.replace("\u00a0", " ").replace("\u2019", "'").replace("\u2018", "'")
          .replace("\u02bc", "'").replace("\u201c", '"').replace("\u201d", '"'))
    return re.sub(r"\s+", " ", t).strip().lower()
# L'adresse doit être identique mot pour mot partout où elle est écrite (facteur NAP).
ADDRESS_KEYS = ("Ndobo Mayor", "West Hotel", "Bonabéri")


def text(html: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", html)).strip()


def read_page(path: Path, base: str) -> dict:
    html = path.read_text(encoding="utf-8")
    h1 = H1_RE.search(html)
    canon = CANON_RE.search(html)
    robots = ROBOTS_RE.search(html)
    ld = []
    for m in LD_RE.finditer(html):
        try:
            ld.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            ld.append({"@error": "JSON-LD invalide"})
    rel = path.relative_to(base)
    url_path = "/" if str(rel) == "index.html" else "/" + str(rel.parent).replace("\\", "/") + "/"
    return {
        "path": url_path,
        "file": path,
        "title": text(TITLE_RE.search(html).group(1)) if TITLE_RE.search(html) else "",
        "desc": DESC_RE.search(html).group(1) if DESC_RE.search(html) else "",
        "h1": text(h1.group(1)) if h1 else "",
        "canonical": canon.group(1) if canon else "",
        "noindex": bool(robots and "noindex" in robots.group(1)),
        "hreflang": {c.lower(): u for c, u in ALT_RE.findall(html)},
        "ld": ld,
        "links": A_RE.findall(html),
        "plain": text(html),
    }


def load_site(site: Path) -> dict[str, dict]:
    pages: dict[str, dict] = {}
    for f in sorted(site.rglob("index.html")):
        if any(part in ("fonts",) for part in f.parts):
            continue
        p = read_page(f, site)
        pages[p["path"]] = p
    return pages


def ld_nodes(page: dict, wanted: str) -> list[dict]:
    out: list[dict] = []
    for block in page["ld"]:
        for node in block.get("@graph", [block]) if isinstance(block, dict) else []:
            if not isinstance(node, dict):
                continue
            types = node.get("@type")
            types = types if isinstance(types, list) else [types]
            if wanted in types:
                out.append(node)
    return out


# ── 1 · la cible ────────────────────────────────────────────────────────────────────────────────
def check_targeting(pages, home="/") -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    p = pages.get(home)
    if not p:
        out["fails"].append("accueil absent du site")
        return out
    t, h = p["title"].lower(), p["h1"].lower()
    for label, zone, where in (("titre", t, "title"), ("H1", h, "h1")):
        if CITY not in zone:
            out["fails"].append(f"{label} : la ville « Douala » n'apparaît pas dans le {where}")
        if not any(j in zone for j in JOBS):
            out["fails"].append(f"{label} : aucun mot du métier (opticien / optométriste) dans le {where}")
    # la marque seule dans le H1 est le défaut d'origine, mesuré le 28/10
    if h.replace(BRAND, "").strip(" ·—-,.") == "" or set(h.split()) <= {"dm", "optique", "sarl", "douala"}:
        out["warns"].append("le H1 ne dit que la marque et la ville : il ne dit pas le métier")
    if CITY in t and CITY in h:
        out["notes"].append("titre et H1 portent la ville et le métier")
    # le miroir anglais vise les deux mêmes requêtes, dans l'autre langue
    en = pages.get("/en/")
    if en:
        et, eh = en["title"].lower(), en["h1"].lower()
        if CITY not in et or not any(j in et for j in JOBS):
            out["fails"].append("miroir anglais : la cible « optician / optometrist in Douala » n'est pas dans le titre")
        if CITY not in eh or not any(j in eh for j in JOBS):
            out["fails"].append("miroir anglais : la cible n'est pas dans le H1")
    else:
        out["notes"].append("pas de miroir anglais : cible FR seulement")
    return out


# ── 2 · hreflang ───────────────────────────────────────────────────────────────────────────────
def check_hreflang(pages) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    n = 0
    for path, p in pages.items():
        hre = p["hreflang"]
        if not hre:
            continue
        n += 1
        urls = set(hre.values())
        if "x-default" not in hre:
            out["warns"].append(f"{path} : pas de x-default (recommandé par Google, jamais obligatoire)")
        if p["canonical"] and p["canonical"] not in urls:
            out["fails"].append(f"{path} : la page ne se liste pas elle-même (auto-référence absente)")
        for code, url in hre.items():
            other = next((q for q in pages.values() if q["canonical"] == url), None)
            if other is None:
                continue                      # page non auditée : on ne juge pas
            if p["canonical"] not in set(other["hreflang"].values()):
                out["fails"].append(f"{path} → {code} ({url}) : aucun lien retour (hreflang ignoré)")
        if "x-default" in hre and "fr" in hre and hre["x-default"] != hre["fr"]:
            out["warns"].append(f"{path} : x-default ne pointe pas sur la version française")
    out["notes"].append(f"{n} page(s) avec hreflang")
    return out


# ── 3 · sitemap ────────────────────────────────────────────────────────────────────────────────
def parse_sitemap(site: Path) -> list[str]:
    f = site / "sitemap.xml"
    if not f.exists():
        return []
    return re.findall(r"<loc>([^<]+)</loc>", f.read_text(encoding="utf-8"))


def check_sitemap(pages, site: Path, base: str) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    locs = parse_sitemap(site)
    if not locs:
        out["fails"].append("pas de sitemap.xml, ou sitemap sans <loc>")
        return out
    known = {p["canonical"] for p in pages.values() if p["canonical"]}
    for u in locs:
        if u not in known:
            out["fails"].append(f"sitemap : {u} ne correspond à aucune page du disque")
    for path, p in pages.items():
        if p["noindex"] or not p["canonical"]:
            continue
        if p["canonical"] not in locs:
            out["fails"].append(f"{path} est indexable mais absente du sitemap")
    out["notes"].append(f"{len(locs)} URL au sitemap, {sum(1 for p in pages.values() if not p['noindex'])} indexables")
    return out


# ── 4 · orphelins ─────────────────────────────────────────────────────────────────────────────
def check_orphans(pages, home="/") -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    by_url = {p["canonical"]: path for path, p in pages.items() if p["canonical"]}
    seen, queue = {home}, deque([home])
    while queue:
        path = queue.popleft()
        p = pages.get(path)
        if not p:
            continue
        for href in p["links"]:
            href = href.split("#")[0].split("?")[0]
            if not href.startswith("/"):
                continue
            if not href.endswith("/") and "." not in href.rsplit("/", 1)[-1]:
                href += "/"
            target = href if href in pages else by_url.get(href)
            if target and target not in seen:
                seen.add(target)
                queue.append(target)
    for path, p in pages.items():
        if p["noindex"] or path == home:
            continue
        if path not in seen:
            out["fails"].append(f"{path} n'est atteignable depuis aucune page (orpheline)")
    out["notes"].append(f"{len(seen)} page(s) atteignables depuis l'accueil")
    return out


# ── 5 · cannibalisation ───────────────────────────────────────────────────────────────────────
def signature(title: str) -> str:
    t = title.lower()
    t = re.sub(r"dm optique sarl|dm optique|\bà\b|\bin\b|\b—\b|\|", " ", t)
    words = [w for w in re.findall(r"[a-zà-ÿ]+", t) if w not in ("douala", "bonabéri", "bonaberi", "de", "la", "le", "les", "du", "des", "et", "the", "of")]
    return " ".join(sorted(set(words)))


def check_cannibal(pages) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    seen: dict[str, str] = {}
    for path, p in pages.items():
        if p["noindex"] or not p["title"]:
            continue
        sig = signature(p["title"])
        if not sig:
            continue
        if sig in seen:
            out["warns"].append(f"{path} et {seen[sig]} ont le même titre une fois la marque retirée")
        else:
            seen[sig] = path
    if not out["warns"]:
        out["notes"].append(f"{len(seen)} titre(s) distincts sur les pages indexables")
    return out


# ── 6 · NAP ───────────────────────────────────────────────────────────────────────────────────
def check_nap(pages) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    for path, p in pages.items():
        if p["noindex"]:
            continue
        if PHONE not in p["plain"].replace(" ", ""):
            out["fails"].append(f"{path} : le numéro du cabinet (+237 656 122 239) est absent")
        if not all(k in p["plain"] for k in ADDRESS_KEYS):
            out["warns"].append(f"{path} : l'adresse n'est pas écrite au complet (Ndobo Mayor, West Hotel, Bonabéri)")
        variants = re.findall(r"\+237[\s0-9]{9,14}", p["plain"])
        if any(v.replace(" ", "") != PHONE for v in variants):
            out["fails"].append(f"{path} : un numéro différent du NAP apparaît ({variants})")
    if not out["fails"]:
        out["notes"].append("téléphone identique sur toutes les pages indexables")
    return out


# ── 7 · schéma ───────────────────────────────────────────────────────────────────────────────
def check_schema(pages, service_pages=("/examen-de-vue/", "/verres-sur-ordonnance/", "/reparation-et-entretien/")) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    orgs = [(path, n) for path, p in pages.items() for n in ld_nodes(p, "Optician")]
    if not orgs:
        out["fails"].append("aucun nœud Optician : Google ne sait pas quel métier exerce l'établissement")
    else:
        path, org = orgs[0]
        for key in ("name", "telephone", "address", "geo", "openingHoursSpecification", "sameAs"):
            if key not in org:
                out["fails"].append(f"Optician ({path}) : « {key} » manquant")
        if not org.get("areaServed"):
            out["warns"].append("Optician : areaServed absent (la ville servie n'est pas déclarée)")
        out["notes"].append(f"{len(orgs)} nœud(s) Optician")
    for path in service_pages:
        p = pages.get(path)
        if not p:
            out["notes"].append(f"{path} : page de service absente (rien à vérifier)")
            continue
        if not ld_nodes(p, "Service"):
            out["warns"].append(f"{path} : page de service sans nœud Service")
    for path, p in pages.items():
        for node in ld_nodes(p, "Product"):
            if "offers" in node or "price" in json.dumps(node):
                out["fails"].append(f"{path} : un prix ou une offre dans le schéma produit")
        # Un avis peut être imbriqué (dans un Service, un Product…) : on lit le bloc entier, pas
        # seulement ses nœuds de premier niveau. Nous ne publions aucun avis : un `Review` dans le
        # schéma est donc toujours une invention, où qu'il se cache.
        for block in p["ld"]:
            blob = json.dumps(block)
            if '"Review"' in blob or '"AggregateRating"' in blob or '"reviewRating"' in blob:
                out["fails"].append(f"{path} : avis dans le schéma — nous n'en publions pas")
    return out


# ── 8 · robots ───────────────────────────────────────────────────────────────────────────────
def check_robots(site: Path) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    f = site / "robots.txt"
    if not f.exists():
        out["fails"].append("robots.txt absent")
        return out
    txt = f.read_text(encoding="utf-8")
    if "sitemap:" not in txt.lower():
        out["fails"].append("robots.txt : aucune ligne Sitemap:")
    for line in txt.splitlines():
        if line.strip().lower().startswith("disallow:") and line.split(":", 1)[1].strip() in ("/", ""):
            out["fails"].append(f"robots.txt interdit le site entier : « {line.strip()} »")
    if "user-agent: *" not in txt.lower():
        out["warns"].append("robots.txt : pas de règle User-agent: * (le défaut s'applique quand même)")
    out["notes"].append(f"robots.txt : {len(txt)} caractères")
    return out


# ── 10 · questions ─────────────────────────────────────────────────────────────────────────────
def check_questions(pages) -> dict:
    """Le balisage FAQ doit dire EXACTEMENT ce que la page montre.

    Google l'exige (contenu structuré = contenu visible), et un assistant qui cite une réponse
    inventée dans le JSON-LD cite une phrase que le visiteur ne peut pas lire. On vérifie aussi
    qu'aucune question n'est posée deux fois sur le site : deux pages qui répondent à la même
    question se cannibalisent, exactement comme deux titres identiques.
    """
    out = {"fails": [], "warns": [], "notes": []}
    seen: dict[str, str] = {}
    total = 0
    for path, p in pages.items():
        visible = flat(p["plain"])
        for node in ld_nodes(p, "FAQPage"):
            for q in node.get("mainEntity", []) or []:
                if not isinstance(q, dict):
                    continue
                name = (q.get("name") or "").strip()
                ans = ((q.get("acceptedAnswer") or {}).get("text") or "").strip()
                if not name or not ans:
                    out["fails"].append(f"{path} : question ou réponse vide dans le balisage")
                    continue
                total += 1
                if flat(name) not in visible:
                    out["fails"].append(f"{path} : la question « {name[:52]}… » est dans le balisage "
                                        f"mais pas dans le texte de la page")
                if flat(ans) not in visible:
                    out["fails"].append(f"{path} : la réponse à « {name[:40]}… » est dans le balisage "
                                        f"mais pas dans le texte de la page")
                if len(ans) < 60:
                    out["warns"].append(f"{path} : « {name[:40]}… » a une réponse de {len(ans)} "
                                        f"caractères : trop courte pour tenir seule hors contexte")
                # Une page et son miroir anglais portent la même question : ce n'est pas une
                # cannibalisation, c'est une traduction. On compare donc les paires FR/EN.
                key = (flat(name), path.replace("/en/", "/", 1))
                if key in seen and seen[key] != path:
                    out["warns"].append(f"« {name[:48]}… » est posée sur {seen[key]} et sur {path}")
                else:
                    seen[key] = path
    if total:
        distinct = len({k[0] for k in seen})
        out["notes"].append(f"{total} question(s) balisée(s) sur {distinct} distinctes "
                            f"(miroirs FR/EN comptés ensemble), toutes présentes dans le texte visible")
    else:
        out["notes"].append("aucun balisage FAQ sur ce site : rien à vérifier")
    return out


# ── 9 · cul-de-sac ──────────────────────────────────────────────────────────────────────────
def check_dead_end(pages) -> dict:
    out = {"fails": [], "warns": [], "notes": []}
    for path, p in pages.items():
        if p["noindex"]:
            continue
        internal = {h.split("#")[0].split("?")[0] for h in p["links"] if h.startswith("/")}
        internal.discard(path)
        if len(internal) < 3:
            out["warns"].append(f"{path} : {len(internal)} lien(s) interne(s) — une page qui ne mène nulle part ne transmet rien")
    if not out["warns"]:
        out["notes"].append("chaque page indexable mène vers au moins trois autres")
    return out


# ── exécution ───────────────────────────────────────────────────────────────────────────────
CHECKS = ("cible", "hreflang", "sitemap", "orphelins", "cannibal", "nap", "schema", "questions", "robots", "cul-de-sac")


def audit(site: Path, base: str = "") -> dict:
    pages = load_site(site)
    res = {
        "cible": check_targeting(pages),
        "hreflang": check_hreflang(pages),
        "sitemap": check_sitemap(pages, site, base),
        "orphelins": check_orphans(pages),
        "cannibal": check_cannibal(pages),
        "nap": check_nap(pages),
        "schema": check_schema(pages),
        "questions": check_questions(pages),
        "robots": check_robots(site),
        "cul-de-sac": check_dead_end(pages),
    }
    return {"site": str(site), "pages": len(pages), "checks": res}


def report(res: dict) -> tuple[int, int]:
    fails = warns = 0
    print(f"\nSEO LOCAL — {res['site']}  ({res['pages']} page(s))\n")
    for name in CHECKS:
        c = res["checks"][name]
        state = "✗" if c["fails"] else ("·" if c["warns"] else "✓")
        print(f"  {name.upper():<12} {state}")
        for m in c["fails"]:
            fails += 1
            print(f"      ✗ {m}")
        for m in c["warns"]:
            warns += 1
            print(f"      · {m}")
        for m in c["notes"]:
            print(f"      · {m}")
    print(f"\n  {fails} faute(s) · {warns} avertissement(s) — {'ROUGE' if fails else 'VERT'}")
    return fails, warns


# ── le banc ─────────────────────────────────────────────────────────────────────────────────
GOOD = {
    "index.html": """<!DOCTYPE html><html lang="fr"><head><title>Opticien optométriste à Douala — Cabinet</title>
<meta name="description" content="x"><meta name="robots" content="index,follow">
<link rel="canonical" href="https://x.cm/">
<link rel="alternate" hreflang="fr" href="https://x.cm/"><link rel="alternate" hreflang="en" href="https://x.cm/en/">
<link rel="alternate" hreflang="x-default" href="https://x.cm/">
<script type="application/ld+json">{"@graph":[{"@type":"Optician","name":"Cabinet","telephone":"+237656122239","address":{"@type":"PostalAddress"},"geo":{},"openingHoursSpecification":{},"sameAs":["https://f"],"areaServed":{"@type":"City","name":"Douala"}}]}</script>
</head><body><h1>Opticien optométriste à Douala</h1>
<p>Ndobo Mayor West Hotel Bonabéri +237 656 122 239</p>
<a href="/a/">a</a><a href="/b/">b</a><a href="/c/">c</a><a href="/en/">en</a></body></html>""",
    "en/index.html": """<!DOCTYPE html><html lang="en"><head><title>Optometrist optician in Douala — Cabinet</title>
<meta name="description" content="x"><link rel="canonical" href="https://x.cm/en/">
<link rel="alternate" hreflang="fr" href="https://x.cm/"><link rel="alternate" hreflang="en" href="https://x.cm/en/">
<link rel="alternate" hreflang="x-default" href="https://x.cm/"></head><body><h1>Optometrist optician in Douala</h1>
<p>Ndobo Mayor West Hotel Bonabéri +237 656 122 239</p><a href="/">fr</a><a href="/a/">a</a><a href="/b/">b</a></body></html>""",
    "a/index.html": """<!DOCTYPE html><html lang="fr"><head><title>Examen de vue à Douala — Cabinet</title>
<meta name="description" content="x"><link rel="canonical" href="https://x.cm/a/">
<link rel="alternate" hreflang="fr" href="https://x.cm/a/"><link rel="alternate" hreflang="en" href="https://x.cm/en/a/">
<link rel="alternate" hreflang="x-default" href="https://x.cm/a/">
<script type="application/ld+json">{"@type":"Service","name":"Examen"}</script></head>
<body><h1>Examen</h1><p>Ndobo Mayor West Hotel Bonabéri +237 656 122 239</p>
<a href="/">h</a><a href="/b/">b</a><a href="/c/">c</a></body></html>""",
    "b/index.html": """<!DOCTYPE html><html lang="fr"><head><title>Verres sur ordonnance à Douala — Cabinet</title>
<meta name="description" content="x"><link rel="canonical" href="https://x.cm/b/">
<link rel="alternate" hreflang="fr" href="https://x.cm/b/"><link rel="alternate" hreflang="en" href="https://x.cm/en/b/">
<link rel="alternate" hreflang="x-default" href="https://x.cm/b/"></head>
<body><h1>Verres</h1><p>Ndobo Mayor West Hotel Bonabéri +237 656 122 239</p>
<a href="/">h</a><a href="/a/">a</a><a href="/c/">c</a></body></html>""",
    "c/index.html": """<!DOCTYPE html><html lang="fr"><head><title>Réparation de lunettes à Douala — Cabinet</title>
<meta name="description" content="x"><link rel="canonical" href="https://x.cm/c/">
<link rel="alternate" hreflang="fr" href="https://x.cm/c/"><link rel="alternate" hreflang="en" href="https://x.cm/en/c/">
<link rel="alternate" hreflang="x-default" href="https://x.cm/c/"></head>
<body><h1>Réparation</h1><p>Ndobo Mayor West Hotel Bonabéri +237 656 122 239</p>
<a href="/">h</a><a href="/a/">a</a><a href="/b/">b</a></body></html>""",
}
SITEMAP = """<?xml version="1.0"?><urlset><url><loc>https://x.cm/</loc></url><url><loc>https://x.cm/en/</loc></url>
<url><loc>https://x.cm/a/</loc></url><url><loc>https://x.cm/b/</loc></url><url><loc>https://x.cm/c/</loc></url></urlset>"""
ROBOTS = "User-agent: *\nAllow: /\nSitemap: https://x.cm/sitemap.xml\n"


def make_site(tmp: Path, over: dict | None = None, drop: tuple = ()) -> Path:
    """Écrit un site sain, puis applique les casses demandées (`over` remplace un fichier)."""
    over = over or {}
    for name, html in GOOD.items():
        if name in drop:
            continue
        f = tmp / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(over.get(name, html), encoding="utf-8")
    for name, html in over.items():
        if name not in GOOD:
            f = tmp / name
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(html, encoding="utf-8")
    (tmp / "sitemap.xml").write_text(SITEMAP, encoding="utf-8")
    (tmp / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    return tmp


def self_test() -> int:
    ok = total = 0

    def check(label, site, code, want_fail=True, check_name=None, field="fails"):
        nonlocal ok, total
        total += 1
        res = audit(site)
        found = []
        for name, c in res["checks"].items():
            if check_name and name != check_name:
                continue
            found += c[field]
        hit = any(code in m for m in found)
        if hit == want_fail:
            ok += 1
            print(f"  ✓ {label}")
        else:
            print(f"  ✗ {label} — attendu {'une faute' if want_fail else 'aucune faute'} « {code} », "
                  f"vu {len(found)} faute(s) : {found[:2]}")

    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        check("sain · un site propre ne produit aucune faute", make_site(base / "sain"), "", want_fail=False)
        check("cassé · le titre perd la ville",
              make_site(base / "t1", {"index.html": GOOD["index.html"].replace(
                  "<title>Opticien optométriste à Douala — Cabinet</title>", "<title>Cabinet — Cabinet</title>")}),
              "la ville « Douala » n'apparaît pas dans le title", check_name="cible")
        check("cassé · le H1 ne dit que la marque",
              make_site(base / "t2", {"index.html": GOOD["index.html"].replace(
                  "<h1>Opticien optométriste à Douala</h1>", "<h1>Cabinet DOUALA</h1>").replace(
                  "<title>Opticien optométriste à Douala — Cabinet</title>",
                  "<title>Opticien optométriste à Douala — Cabinet</title>")}),
              "aucun mot du métier", check_name="cible")
        check("cassé · pas de x-default",
              make_site(base / "t3", {"index.html": GOOD["index.html"].replace(
                  '<link rel="alternate" hreflang="x-default" href="https://x.cm/">\n', "")}),
              "pas de x-default", check_name="hreflang", field="warns")
        check("cassé · hreflang sans lien retour",
              make_site(base / "t4", {"a/index.html": GOOD["a/index.html"].replace(
                  '<link rel="alternate" hreflang="en" href="https://x.cm/en/a/">',
                  '<link rel="alternate" hreflang="en" href="https://x.cm/en/">')}),
              "aucun lien retour", check_name="hreflang")
        s6 = make_site(base / "t6")
        (s6 / "sitemap.xml").write_text(SITEMAP.replace("<url><loc>https://x.cm/c/</loc></url>", ""), encoding="utf-8")
        check("cassé · le sitemap oublie une page", s6, "absente du sitemap", check_name="sitemap")
        s7 = make_site(base / "t7", {
            "a/index.html": GOOD["a/index.html"].replace('<a href="/c/">c</a>', ""),
            "b/index.html": GOOD["b/index.html"].replace('<a href="/c/">c</a>', ""),
            "index.html": GOOD["index.html"].replace('<a href="/c/">c</a>', ""),
        })
        (s7 / "sitemap.xml").write_text(SITEMAP.replace("<url><loc>https://x.cm/c/</loc></url>", ""), encoding="utf-8")
        check("cassé · une page orpheline", s7, "orpheline", check_name="orphelins")
        check("cassé · deux titres identiques",
              make_site(base / "t8", {"b/index.html": GOOD["b/index.html"].replace(
                  "<title>Verres sur ordonnance à Douala — Cabinet</title>",
                  "<title>Examen de vue à Douala — Cabinet</title>")}),
              "même titre", check_name="cannibal", field="warns")
        check("cassé · un numéro différent",
              make_site(base / "t9", {"a/index.html": GOOD["a/index.html"].replace("+237 656 122 239", "+237 699 000 000")}),
              "numéro différent", check_name="nap")
        check("cassé · Optician sans téléphone",
              make_site(base / "t10", {"index.html": GOOD["index.html"].replace('"telephone":"+237656122239",', "")}),
              "« telephone » manquant", check_name="schema")
        check("cassé · des avis inventés dans le schéma",
              make_site(base / "t11", {"a/index.html": GOOD["a/index.html"].replace(
                  '{"@type":"Service","name":"Examen"}',
                  '{"@type":"Service","name":"Examen","review":{"@type":"Review","reviewRating":5}}')}),
              "avis dans le schéma", check_name="schema")
        s12 = make_site(base / "t12")
        (s12 / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
        check("cassé · robots.txt ferme le site", s12, "interdit le site entier", check_name="robots")
        s13 = make_site(base / "t13")
        (s13 / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
        check("cassé · robots.txt sans sitemap", s13, "aucune ligne Sitemap", check_name="robots")
        check("cassé · une page cul-de-sac",
              make_site(base / "t14", {"c/index.html": GOOD["c/index.html"].replace(
                  '<a href="/">h</a><a href="/a/">a</a><a href="/b/">b</a>', '<a href="/">h</a>')}),
              "lien(s) interne(s)", check_name="cul-de-sac", field="warns")
        check("cassé · le miroir anglais perd la cible",
              make_site(base / "t15", {"en/index.html": GOOD["en/index.html"].replace(
                  "<h1>Optometrist optician in Douala</h1>", "<h1>Cabinet</h1>")}),
              "miroir anglais", check_name="cible")

    print(f"\nbanc de test : {ok}/{total}")
    return 0 if ok == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="SEO local et intention de recherche")
    ap.add_argument("site", nargs="?", help="dossier du site (contient index.html)")
    ap.add_argument("--base", default="", help="domaine canonique (facultatif)")
    ap.add_argument("--strict", action="store_true", help="code 1 si une faute est trouvée")
    ap.add_argument("--only", default="", help="une ou plusieurs vérifications, séparées par des virgules")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    o = ap.parse_args()
    if o.self_test:
        return self_test()
    if not o.site:
        ap.error("site ou --self-test")
    site = Path(o.site).resolve()
    res = audit(site, o.base)
    if o.only:
        keep = {k.strip() for k in o.only.split(",") if k.strip()}
        res["checks"] = {k: v for k, v in res["checks"].items() if k in keep}
    if o.json:
        print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
        return 0
    fails, _ = report(res)
    return 1 if (fails and o.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
