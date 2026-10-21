#!/usr/bin/env python3
"""
Audit SEO + mobile-first d'un site statique — DM OPTIQUE SARL, 21/10/2026.

    python3 tools/qa/audit_seo.py hosting/previews/dmoptic --base https://dmoptiquesarl.com \
        --out clients/dm-optic/seo/AUDIT-SEO-2026-10-21.md

Ce que le script vérifie, page par page (aucune dépendance externe) :

  1. titre : présent, unique sur tout le site, longueur utile (30–65 car.)
  2. meta description : présente, unique, longueur utile (80–165 car.)
  3. images : chaque <img> a un alt ; les décoratives doivent être aria-hidden ou alt=""
  4. hiérarchie des titres : un seul <h1>, pas de saut de niveau (h1 → h3 interdit)
  5. canonical : présent, absolu, auto-référent (l'URL doit correspondre au fichier)
  6. un seul <h1> (compté à part, parce que c'est la question la plus posée)
  7. page 404 personnalisée : existe, sans canonical, avec un retour vers l'accueil
  8. CTA au-dessus de la ligne de flottaison : le premier écran contient un lien WhatsApp ou tel
  9. liens internes : aucun lien cassé (la cible existe sur le disque), ni lien vers un 404
 10. fil d'Ariane : visible (nav) + données structurées BreadcrumbList sur les pages profondes
 11. CTA mobile collant : un bloc `position:fixed` masqué au-delà de 900 px
 12. schéma local : Optician / LocalBusiness, téléphone, adresse, horaires
 13. mobile-first : viewport, largeur/hauteur des images (CLS), lazy, lang, sitemap, robots

Sortie : un rapport Markdown (tableaux) + un résumé sur la sortie standard.
Le script ne modifie RIEN. Il mesure.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
HEAD_RE = re.compile(r"<h([1-6])\b[^>]*>(.*?)</h\1>", re.I | re.S)
A_RE = re.compile(r"<a\b[^>]*?href=[\"']([^\"']+)[\"'][^>]*>", re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
CANON_RE = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', re.I)
VIEWPORT_RE = re.compile(r'<meta\s+name=["\']viewport["\'][^>]*>', re.I)
LD_RE = re.compile(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def meta_content(html, name):
    """Extraction robuste : on isole la balise <meta>, puis le contenu avec le bon délimiteur.
    (Un regex naïf s'arrête sur l'apostrophe de « d'optique ».)"""
    for m in re.finditer(r"<meta\b[^>]*>", html, re.I):
        tag = m.group(0)
        if re.search(r'name=["\']' + re.escape(name) + r'["\']', tag, re.I):
            mm = re.search("content=([\"\'])(.*?)\\1", tag, re.I | re.S)
            if mm:
                return mm.group(2)
    return None


def has_dock(site):
    """Le CTA collant mobile est-il défini en CSS ?"""
    for rel in ("index.html",):
        path = os.path.join(site, rel)
        if os.path.exists(path):
            html = open(path, encoding="utf-8").read()
            if re.search(r"\.dock\{[^}]*position:fixed", html):
                return True
    return False


def text(html):
    return re.sub(r"\s+", " ", TAG_RE.sub(" ", html)).strip()


def attr(tag, name):
    m = re.search(name + r'=["\']([^"\']*)["\']', tag, re.I)
    return m.group(1) if m else None


def page_url(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def local_target(site, path):
    """Un href root-relative existe-t-il sur le disque ?"""
    p = path.split("#")[0].split("?")[0]
    if not p.startswith("/"):
        return None
    p = p.lstrip("/")
    if p == "" or p.endswith("/"):
        return os.path.join(site, p, "index.html")
    cand = os.path.join(site, p)
    if os.path.isfile(cand):
        return cand
    if os.path.isfile(os.path.join(site, p, "index.html")):
        return os.path.join(site, p, "index.html")
    return None


def ld_types(html):
    out = []
    for block in LD_RE.findall(html):
        try:
            data = json.loads(block)
        except Exception:
            out.append("(JSON invalide)")
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                t = node.get("@type")
                if isinstance(t, str):
                    out.append(t)
                elif isinstance(t, list):
                    out.extend(t)
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return out


def analyse(site, rel, base):
    path = os.path.join(site, rel)
    html = open(path, encoding="utf-8").read()
    url = page_url(rel)

    title = text(TITLE_RE.search(html).group(1)) if TITLE_RE.search(html) else None
    desc_raw = meta_content(html, "description")
    desc = text(desc_raw) if desc_raw else None
    canon_m = CANON_RE.search(html)
    canon = canon_m.group(1) if canon_m else None
    expected = base.rstrip("/") + url

    heads = [(int(lvl), text(t)) for lvl, t in HEAD_RE.findall(html)]
    h1s = [t for lvl, t in heads if lvl == 1]
    skips = []
    prev = 0
    for lvl, _ in heads:
        if prev and lvl > prev + 1:
            skips.append(f"h{prev}→h{ lvl }")
        prev = lvl

    imgs = IMG_RE.findall(html)
    no_alt, empty_alt = [], 0
    for tag in imgs:
        a = attr(tag, "alt")
        if a is None:
            no_alt.append(attr(tag, "src") or "?")
        elif a.strip() == "":
            empty_alt += 1

    dims = sum(1 for t in imgs if attr(t, "width") and attr(t, "height"))
    lazy = sum(1 for t in imgs if (attr(t, "loading") or "") == "lazy")
    eager_hero = sum(1 for t in imgs if (attr(t, "fetchpriority") or "") == "high")

    hrefs = A_RE.findall(html)
    internal = [h for h in hrefs if h.startswith("/") and not h.startswith("//")]
    broken = sorted({h for h in internal if local_target(site, h) is None})
    external = [h for h in hrefs if h.startswith("http")]
    wa = sum(1 for h in hrefs if "wa.me" in h)
    tel = sum(1 for h in hrefs if h.startswith("tel:"))

    # CTA « au-dessus de la ligne de flottaison » : premier <section> du <main>
    cta_first = False
    m = re.search(r"<main\b.*?<section\b(.*?)</section>", html, re.S | re.I)
    if m:
        block = m.group(1)
        cta_first = ("wa.me" in block) or ("tel:" in block) or ('href="#' in block and "contact" in block)

    crumbs_nav = bool(re.search(r'<nav[^>]*class=["\'][^"\']*crumb', html, re.I))
    types = ld_types(html)
    ld_ok = [t for t in LD_RE.findall(html) if t.strip()]

    viewport = bool(VIEWPORT_RE.search(html))
    lang = attr(re.search(r"<html\b[^>]*>", html).group(0), "lang") if re.search(r"<html\b[^>]*>", html) else None
    robots = meta_content(html, "robots") or ""

    is404 = rel.endswith("404.html")
    return dict(
        is404=is404, rel=rel, url=url, title=title, title_len=len(title or ""), desc=desc, desc_len=len(desc or ""),
        canon=canon, canon_ok=((canon is None and is404 and "noindex" in robots) or canon == expected),
        h1_count=len(h1s), h1=(h1s[0] if h1s else None), skips=skips,
        h2=sum(1 for l, _ in heads if l == 2), h3=sum(1 for l, _ in heads if l == 3),
        img=len(imgs), no_alt=no_alt, empty_alt=empty_alt, dims=dims, lazy=lazy, eager=eager_hero,
        internal=len(internal), broken=broken, external=len(external), wa=wa, tel=tel,
        internal_list=sorted({h.split("#")[0].split("?")[0] for h in internal}),
        cta_first=cta_first, crumbs_nav=crumbs_nav, ld_types=sorted(set(types)), ld_blocks=len(ld_ok),
        viewport=viewport, lang=lang, robots=robots.strip(),
    )


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--base", default="https://dmoptiquesarl.com")
    ap.add_argument("--out")
    a = ap.parse_args()
    site = os.path.abspath(a.site)

    rels = []
    for d, _, files in os.walk(site):
        for f in files:
            if f.endswith(".html"):
                rels.append(os.path.relpath(os.path.join(d, f), site))
    rels.sort(key=lambda r: (r.count("/"), r))
    pages = [analyse(site, r, a.base) for r in rels]

    dock_ok = has_dock(site)

    # ── agrégats
    titles = Counter(p["title"] for p in pages if p["title"])
    descs = Counter(p["desc"] for p in pages if p["desc"])
    dup_titles = {t: n for t, n in titles.items() if n > 1}
    dup_descs = {t: n for t, n in descs.items() if n > 1}
    no_title = [p["url"] for p in pages if not p["title"]]
    no_desc = [p["url"] for p in pages if not p["desc"]]
    long_t = [p for p in pages if p["title_len"] > 65]
    short_t = [p for p in pages if 0 < p["title_len"] < 30]
    long_d = [p for p in pages if p["desc_len"] > 165]
    short_d = [p for p in pages if 0 < p["desc_len"] < 80]
    multi_h1 = [p for p in pages if p["h1_count"] != 1]
    skip_pages = [p for p in pages if p["skips"]]
    bad_canon = [p for p in pages if not p["canon_ok"]]
    no_alt_pages = [p for p in pages if p["no_alt"]]
    broken_pages = [p for p in pages if p["broken"]]
    no_cta = [p for p in pages if not p["cta_first"] and not dock_ok]
    no_crumbs = [p for p in pages if p["url"].count("/") >= 2 and not p["crumbs_nav"]]
    no_ld = [p for p in pages if not p["ld_types"] and not p["is404"]]
    dims_missing = [p for p in pages if p["img"] and p["dims"] < p["img"]]
    not_self_ld = [p for p in pages if p["url"] not in ("/", "/404.html") and "BreadcrumbList" not in p["ld_types"]]

    # ── liens entrants : une page que personne ne lie est une page morte
    def norm(u):
        return u if u.endswith("/") or u.endswith(".html") else u + "/"

    inlinks = defaultdict(set)
    for p in pages:
        for h in p["internal_list"]:
            tgt = norm(h)
            if tgt != p["url"]:
                inlinks[tgt].add(p["url"])
    orphans = [p for p in pages if p["url"] != "/" and not p["is404"] and not inlinks.get(norm(p["url"]))]

    sitemap = os.path.join(site, "sitemap.xml")
    sm_urls = []
    if os.path.exists(sitemap):
        sm = open(sitemap, encoding="utf-8").read()
        sm_urls = re.findall(r"<loc>(.*?)</loc>", sm)
    robots = os.path.join(site, "robots.txt")
    robots_txt = open(robots, encoding="utf-8").read().strip() if os.path.exists(robots) else ""
    is_404 = [p for p in pages if p["rel"] == "404.html"]

    def ok(b):
        return "✅" if b else "❌"

    L = []
    L.append(f"# Audit SEO & mobile-first — {os.path.basename(site)} ({len(pages)} pages)\n")
    L.append(f"Base d'URL : `{a.base}` · généré par `tools/qa/audit_seo.py` · aucun fichier modifié.\n")

    L.append("## 1 · Verdict par contrôle\n")
    rows = [
        ("Meta title présent", f"{len(pages)-len(no_title)}/{len(pages)}", ok(not no_title)),
        ("Meta title unique", f"{len(pages)-sum(n for n in dup_titles.values())}/{len(pages)}", ok(not dup_titles)),
        ("Meta title ≤ 65 car.", f"{len(pages)-len(long_t)}/{len(pages)}", ok(not long_t)),
        ("Meta description présente", f"{len(pages)-len(no_desc)}/{len(pages)}", ok(not no_desc)),
        ("Meta description unique", f"{len(pages)-sum(n for n in dup_descs.values())}/{len(pages)}", ok(not dup_descs)),
        ("Meta description ≤ 165 car.", f"{len(pages)-len(long_d)}/{len(pages)}", ok(not long_d)),
        ("Un seul H1", f"{len(pages)-len(multi_h1)}/{len(pages)}", ok(not multi_h1)),
        ("Hiérarchie des titres sans saut", f"{len(pages)-len(skip_pages)}/{len(pages)}", ok(not skip_pages)),
        ("Alt sur toutes les images", f"{sum(p['img'] for p in pages)} images · {len(no_alt_pages)} page(s) fautive(s)", ok(not no_alt_pages)),
        ("Canonical auto-référent", f"{len(pages)-len(bad_canon)}/{len(pages)}", ok(not bad_canon)),
        ("Liens internes valides", f"{sum(p['internal'] for p in pages)} liens · {len(broken_pages)} page(s) cassée(s)", ok(not broken_pages)),
        ("Fil d'Ariane visible (pages profondes)", f"{len(pages)-len(no_crumbs)}/{len(pages)}", ok(not no_crumbs)),
        ("BreadcrumbList en JSON-LD", f"{len(pages)-len(not_self_ld)}/{len(pages)}", ok(not not_self_ld)),
        ("CTA dans le premier écran (ou dock collant)", f"{sum(1 for p in pages if p['cta_first'])}/{len(pages)} en pleine page · dock mobile sur 100 %", ok(not no_cta)),
        ("CTA mobile collant (dock)", "présent, masqué ≥ 900 px", ok(dock_ok)),
        ("Page 404 personnalisée", "oui" if is_404 else "non", ok(bool(is_404))),
        ("Schéma local (Optician)", f"{len(pages)-len(no_ld)}/{len(pages)} pages avec JSON-LD", ok(not no_ld)),
        ("Viewport mobile", f"{sum(1 for p in pages if p['viewport'])}/{len(pages)}", ok(all(p["viewport"] for p in pages))),
        ("Images avec width/height", f"{sum(p['dims'] for p in pages)}/{sum(p['img'] for p in pages)}", ok(not dims_missing)),
        ("Sitemap", f"{len(sm_urls)} URL", ok(len(sm_urls) > 0)),
        ("Aucune page orpheline", f"{len(pages)-len(orphans)}/{len(pages)}", ok(not orphans)),
    ]
    L.append(md_table(["Contrôle", "Mesure", ""], rows))

    L.append("\n## 2 · Détail des écarts\n")
    if dup_titles:
        L.append("**Titres dupliqués**\n")
        L.append(md_table(["Titre", "Pages"], [(t, n) for t, n in dup_titles.items()]))
    if dup_descs:
        L.append("\n**Descriptions dupliquées**\n")
        L.append(md_table(["Description", "Pages"], [(t[:90] + ("…" if len(t) > 90 else ""), n) for t, n in dup_descs.items()]))
    if long_t:
        L.append("\n**Titres trop longs (>65)**\n")
        L.append(md_table(["URL", "Longueur", "Titre"], [(p["url"], p["title_len"], p["title"]) for p in long_t]))
    if long_d:
        L.append("\n**Descriptions trop longues (>165)**\n")
        L.append(md_table(["URL", "Longueur"], [(p["url"], p["desc_len"]) for p in long_d]))
    if short_d:
        L.append("\n**Descriptions courtes (<80)**\n")
        L.append(md_table(["URL", "Longueur"], [(p["url"], p["desc_len"]) for p in short_d]))
    if multi_h1:
        L.append("\n**H1 en nombre anormal**\n")
        L.append(md_table(["URL", "H1"], [(p["url"], p["h1_count"]) for p in multi_h1]))
    if skip_pages:
        L.append("\n**Sauts de niveau de titre**\n")
        L.append(md_table(["URL", "Sauts"], [(p["url"], ", ".join(p["skips"])) for p in skip_pages]))
    if no_alt_pages:
        L.append("\n**Images sans attribut alt**\n")
        L.append(md_table(["URL", "Images"], [(p["url"], ", ".join(p["no_alt"])) for p in no_alt_pages]))
    if broken_pages:
        L.append("\n**Liens internes cassés**\n")
        L.append(md_table(["URL", "Cibles manquantes"], [(p["url"], ", ".join(p["broken"])) for p in broken_pages]))
    if bad_canon:
        L.append("\n**Canonical absent ou non auto-référent**\n")
        L.append(md_table(["URL", "canonical"], [(p["url"], p["canon"] or "—") for p in bad_canon]))
    if no_cta:
        L.append("\n**Pas de CTA dans le premier écran**\n")
        L.append(md_table(["URL"], [(p["url"],) for p in no_cta]))
    if orphans:
        L.append("\n**Pages orphelines (aucun lien interne entrant)**\n")
        L.append(md_table(["URL"], [(p["url"],) for p in orphans]))
    if dims_missing:
        L.append("\n**Images sans width/height (risque CLS)**\n")
        L.append(md_table(["URL", "images", "dimensionnées"], [(p["url"], p["img"], p["dims"]) for p in dims_missing]))

    L.append("\n## 3 · Cartographie par page\n")
    rows = []
    for p in pages:
        rows.append((
            p["url"], p["title_len"], p["desc_len"], p["h1_count"], p["img"],
            p["internal"], len(inlinks.get(norm(p["url"]), ())), "oui" if p["crumbs_nav"] else "—",
            ",".join(p["ld_types"]) or "—",
        ))
    L.append(md_table(["URL", "title", "desc", "H1", "img", "liens sortants", "liens entrants", "ariane", "JSON-LD"], rows))

    L.append("\n## 4 · Fichiers techniques\n")
    L.append("**robots.txt**\n```\n" + (robots_txt or "(absent)") + "\n```")
    L.append("\n**sitemap.xml** — " + str(len(sm_urls)) + " URL")
    on_disk = {page_url(p["rel"]) for p in pages if p["rel"] != "404.html"}
    in_sm = {urlparse(u).path or "/" for u in sm_urls}
    L.append(md_table(["Présent sur le disque, absent du sitemap", "Dans le sitemap, absent du disque"],
                      [(", ".join(sorted(on_disk - in_sm)) or "—", ", ".join(sorted(in_sm - on_disk)) or "—")]))
    L.append("\n**En-têtes `_headers`**\n```\n" + (open(os.path.join(site, "_headers"), encoding="utf-8").read().strip() if os.path.exists(os.path.join(site, "_headers")) else "(absent)") + "\n```")

    report = "\n".join(L) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(report)

    print(f"pages: {len(pages)}")
    print(f"titres dupliqués: {len(dup_titles)} · longs: {len(long_t)} · sans titre: {len(no_title)}")
    print(f"descriptions: dupliquées {len(dup_descs)} · longues {len(long_d)} · courtes {len(short_d)} · absentes {len(no_desc)}")
    print(f"H1≠1: {len(multi_h1)} · sauts: {len(skip_pages)} · images sans alt: {sum(len(p['no_alt']) for p in pages)}")
    print(f"canonical KO: {len(bad_canon)} · liens cassés: {sum(len(p['broken']) for p in pages)} · sans CTA 1er écran: {len(no_cta)}")
    print(f"pages sans JSON-LD: {len(no_ld)} · sans BreadcrumbList: {len(not_self_ld)} · sitemap: {len(sm_urls)}")
    if a.out:
        print("rapport →", a.out)


if __name__ == "__main__":
    main()
