#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porte de livraison — ce qu'un audit extérieur a trouvé et que nos portiques ne voyaient pas.

    python3 tools/qa/audit_delivery.py hosting/previews/dmoptic --base https://dmoptiquesarl.com
    python3 tools/qa/audit_delivery.py site --base https://amk-cm.vercel.app
    python3 tools/qa/audit_delivery.py <site> --strict --json

**Pourquoi ce script existe.** Le 23/10/2026, un audit extérieur de DM Optique (Chrome headless,
axe-core, comparaison au domaine en ligne) a rendu un verdict que nos portiques n'auraient jamais pu
rendre : deux P1 — **aucune navigation sous 980 px** et **cache à `max-age=0` sur toutes les images et
polices** — alors que `audit_html`, `audit_a11y`, `audit_images`, `audit_reveal` et `audit_seo`
disaient tous « 0 faute ». Ils avaient raison **sur ce qu'ils mesurent** ; ils ne mesuraient pas ça.
Un portique qui ne peut pas échouer sur ces classes-là ne prouve rien sur elles.

Les huit classes ajoutées ici, toutes mesurables **sans navigateur ni réseau** :

  D1  navigation mobile     — la nav est cachée sous un point de rupture et **aucun bouton de menu**
                              n'existe (`aria-expanded` + `aria-controls`). Un visiteur au téléphone
                              n'a alors que le pied de page. P1.
  D2  cache des assets      — `_headers` ne sert aucune règle de cache pour les images et les polices,
                              ou sert un motif que l'hôte **n'appliquera jamais** (splat ailleurs qu'en
                              fin de motif sur Cloudflare Pages : `/*.webp` ne matche rien). P1.
  D3  favicon               — `favicon.ico`/`favicon.svg`/`apple-touch-icon.png` absents ou pas
                              déclarés : onglet blanc, 404 dans la console. P2.
  D4  URL malformées        — `https://hote//fichier` (double barre après l'hôte) dans les métadonnées
                              ou les données structurées ; `http://` sur notre propre hôte. P2.
  D5  llms.txt              — présent mais incomplet : des URL du sitemap n'y figurent pas (le cas DM :
                              les 47 pages anglaises). P2.
  D6  partage social        — `og:image` en WebP (aperçu incertain dans WhatsApp), sans `og:image:type`
                              ni dimensions. P2/P3.
  D7  données structurées   — page produit sans `Product` ; page d'accueil sans `sameAs` ; et surtout
                              **un `price` dans le JSON-LD = P1** : la maison n'affiche aucun prix public.
  D8  en-têtes de sécurité  — HSTS absent (P2), CSP absente (P3).

Ce que ce script **ne** fait pas, et qui reste à la main : le rendu réel (Chrome), axe-core, un vrai
partage WhatsApp, un passage lecteur d'écran. Il ne remplace pas `audit_a11y` ni `audit_seo` ; il ferme
les trous qu'ils laissaient. Le détail des leçons : `tools/qa/AUDIT-LESSONS-2026-10-23.md`.

Sortie : constats classés P1/P2/P3, une ligne de résumé, `--json` pour la machine, `--strict` pour
échouer aussi sur P2. Code de sortie 1 s'il reste une P1 (`--strict` : une P1 ou une P2).
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path, PurePosixPath
from typing import NamedTuple

# --------------------------------------------------------------------------- outils

LOCAL_TYPES = ("Optician", "LocalBusiness", "Store", "MedicalBusiness", "MedicalClinic", "Dentist",
               "Pharmacy", "HealthAndBeautyBusiness", "ProfessionalService", "Organization", "Corporation")
IMG_EXT = (".webp", ".jpg", ".jpeg", ".png", ".avif", ".gif", ".svg")
FONT_EXT = (".woff2", ".woff", ".ttf", ".otf")
MENU_BTN_RE = re.compile(r"<button\b[^>]*\baria-expanded\s*=[^>]*>", re.I)
LDJSON_RE = re.compile(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', re.I | re.S)
META_RE = re.compile(r"<meta\b[^>]*>", re.I)
NAV_RE = re.compile(r"<nav\b([^>]*)>(.*?)</nav>", re.I | re.S)
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.I)


class Finding(NamedTuple):
    code: str
    sev: str          # P1 | P2 | P3
    where: str
    message: str
    fix: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def pages_of(site: Path) -> list[Path]:
    return sorted(p for p in site.rglob("*.html") if p.is_file())


def url_of(site: Path, page: Path) -> str:
    rel = PurePosixPath(page.relative_to(site).as_posix())
    if rel.name == "index.html":
        parent = str(rel.parent)
        return "/" if parent == "." else f"/{parent}/"
    return f"/{rel}"


def media_blocks(css: str) -> list[tuple[str, str]]:
    """Les blocs `@media` avec leur condition, accolades équilibrées (pas de regex naïve : les blocs
    de media contiennent d'autres accolades, et une regex `[^}]*` s'arrête au premier `}` venu)."""
    out = []
    for m in re.finditer(r"@media[^{]*\{", css):
        i, depth, j = m.end(), 1, m.end()
        while j < len(css) and depth:
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
            j += 1
        out.append((css[m.start():m.end() - 1].strip(), css[i:j - 1]))
    return out


def max_age(cache_control: str) -> int:
    m = re.search(r"max-age\s*=\s*(\d+)", cache_control or "", re.I)
    return int(m.group(1)) if m else -1


# --------------------------------------------------------------------------- D1 navigation

def _nav_class(attrs: str) -> str:
    m = re.search(r'class\s*=\s*["\']([^"\']+)', attrs)
    return m.group(1).split()[0] if m else ""


def _hidden_below(css: str, cls: str) -> int | None:
    """Point de rupture sous lequel `.cls` n'est pas affichée, ou None si elle l'est toujours."""
    if not cls:
        return None
    base = re.search(r"\.%s(?![-\w])\s*\{[^}]*?display\s*:\s*none" % re.escape(cls), css)
    shown_at = None
    for cond, body in media_blocks(css):
        mi = re.search(r"min-width\s*:\s*(\d+)px", cond)
        if mi and re.search(r"\.%s(?![-\w])\s*\{[^}]*?display\s*:\s*(flex|grid|block|inline-flex)" % re.escape(cls), body):
            shown_at = int(mi.group(1))
            break
    if base and shown_at is not None:
        return shown_at
    # variante inverse : affichée par défaut, cachée par une max-width
    for cond, body in media_blocks(css):
        ma = re.search(r"max-width\s*:\s*(\d+)px", cond)
        if ma and re.search(r"\.%s(?![-\w])[^{]*\{[^}]*?display\s*:\s*none" % re.escape(cls), body):
            return int(ma.group(1)) + 1
    return None



VOID = {"br", "img", "input", "meta", "link", "hr", "source"}


def nav_links_state(css: str, inner: str) -> tuple[int, int, set[int]]:
    """Compte les liens de la nav, ceux que le CSS masque (par leur classe **ou celle d'un ancêtre**),
    et les points de rupture rencontrés. Un lien sans classe dans un conteneur caché compte comme caché :
    c'est le cas de DM comme des pages concepts d'AMK."""
    stack: list[str] = []
    total = hidden = 0
    bps: set[int] = set()
    for m in re.finditer(r"<(/?)([a-zA-Z][\w-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>", inner):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if closing:
            if stack:
                stack.pop()
            continue
        cls = re.search(r'class\s*=\s*["\']([^"\']+)', attrs)
        classes = cls.group(1).split() if cls else []
        if tag == "a":
            total += 1
            found = {b for b in (_hidden_below(css, c) for c in classes + stack) if b}
            if found:
                hidden += 1
                bps |= found
        if tag not in VOID and not attrs.rstrip().endswith("/"):
            stack.append(classes[0] if classes else "")
    return total, hidden, bps




def has_menu_control(html: str) -> bool:
    """Un menu peut être un `<button aria-expanded aria-controls>` **ou** une divulgation native
    `<details><summary>` — le portique ne doit pas imposer une implémentation. Le cas DM du 23/10 est
    justement un `<details>` : sans cette branche, la correction aurait été refusée par le contrôle."""
    for b in MENU_BTN_RE.finditer(html):
        if re.search(r"aria-controls\s*=", b.group(0), re.I):
            return True
    for m in re.finditer(r"<details\b[^>]*>(.*?)</details>", html, re.I | re.S):
        body = m.group(1)
        if re.search(r"<summary\b", body, re.I) and len(re.findall(r"<a\b", body, re.I)) >= 2:
            return True
    return False


def check_nav(site: Path, pages: list[Path]) -> list[Finding]:
    """D1 : sous un point de rupture, **tous** les liens de la nav disparaissent-ils sans bouton de menu ?

    Deux sévérités, parce que ce n'est pas la même perte : si la nav cachée mène à des **pages**
    (`/montures/`, `/contact/`), le visiteur n'a plus aucun chemin — P1. Si elle ne fait que sauter dans
    la même page (`#services`), on perd du confort mais pas la navigation — P2.
    """
    pages_site, pages_ancre, bps_all = [], [], set()
    pages = [p for p in pages if p.name != "404.html"] or pages
    for page in pages:
        html = read(page)
        nav = None
        for m in NAV_RE.finditer(html):
            if len(re.findall(r"<a\b", m.group(2))) >= 2:
                nav = m
                break
        if nav is None:
            continue
        css = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", html, re.I | re.S))
        total, hidden, bps = nav_links_state(css, nav.group(2))
        nav_hidden = _hidden_below(css, _nav_class(nav.group(1))) is not None
        if not nav_hidden and (total == 0 or hidden < total):
            continue
        if has_menu_control(html):
            continue
        hrefs = re.findall(r'<a\b[^>]*href\s*=\s*["\']([^"\']+)', nav.group(2), re.I)
        bucket = pages_site if any(not h.startswith("#") for h in hrefs) else pages_ancre
        bucket.append(page)
        bps_all |= (bps | ({_hidden_below(css, _nav_class(nav.group(1))) or 0} - {0}))

    out = []
    bps = "/".join(str(b) for b in sorted(bps_all)) or "le point de rupture"
    if pages_site:
        out.append(Finding(
            "D1", "P1", f"{len(pages_site)} page(s), ex. {url_of(site, pages_site[0])}",
            f"aucune navigation sous {bps} px : tous les liens de la nav sont masqués par le CSS et aucun "
            "bouton de menu (aria-expanded + aria-controls) ne les remplace — au téléphone, il ne reste "
            "que le pied de page",
            "ajouter un bouton de menu (44 px, aria-expanded, aria-controls, focus géré, Échap, piège de "
            "focus) ou garder deux liens visibles (« Montures », « Contact ») sous le point de rupture ; "
            "tester 390, 768 et 1024 px",
        ))
    if pages_ancre:
        out.append(Finding(
            "D1", "P2", f"{len(pages_ancre)} page(s), ex. {url_of(site, pages_ancre[0])}",
            f"sous {bps} px, les liens de section (`#…`) disparaissent sans bouton de menu : le contenu "
            "reste atteignable en défilant, la navigation d'ancre non",
            "soit un bouton de menu, soit une barre de deux ou trois ancres qui reste visible (Services · "
            "Tarifs · Visite)",
        ))
    return out


# --------------------------------------------------------------------------- D2 cache / D8 sécurité

def parse_headers(path: Path) -> list[tuple[str, dict[str, str]]]:
    blocks: list[tuple[str, dict[str, str]]] = []
    cur: tuple[str, dict[str, str]] | None = None
    for line in read(path).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[:1].isspace():
            cur = (line.strip(), {})
            blocks.append(cur)
        elif cur is not None:
            k, _, v = line.strip().partition(":")
            if k:
                cur[1][k.strip().lower()] = v.strip()
    return blocks


def uses_workers_assets(site: Path) -> bool:
    """Le site est-il publié par **Workers static assets** (wrangler) plutôt que Pages ?

    La différence compte : la doc Workers accepte un splat au milieu d'un motif (son exemple est
    `/*.jpg`), la doc Pages ne l'accepte qu'en fin. Un portique qui ignore l'hôte condamne un motif
    valide — c'était le cas de `/*.webp` pour DM OPTIQUE, publié par Workers depuis le 22/10."""
    for d in [site, *site.parents]:
        if (d / "wrangler.toml").exists() or (d / "wrangler.jsonc").exists() or (d / "wrangler.json").exists():
            return True
    return False


def pattern_is_valid(pattern: str, workers: bool = False) -> bool:
    """Cloudflare Pages / Netlify : un splat `*` **uniquement en fin de motif**, un motif de chemin
    commençant par `/`. `/*.webp` ne matche donc aucun fichier — c'est le piège de l'audit du 23/10."""
    if not pattern.startswith("/"):
        return False
    if workers:
        return pattern.count("*") <= 1          # un seul splat, où qu'il soit
    return "*" not in pattern[:-1]


def pattern_matches(pattern: str, path: str) -> bool:
    """Un motif `_headers` : soit le chemin exact, soit un préfixe terminé par `*`, avec `:param`
    pour un segment. C'est la syntaxe Cloudflare Pages / Netlify — le splat n'y vaut qu'en fin."""
    rx = "^" + re.escape(pattern).replace(r"\:", ":").replace(r"\*", ".*")
    rx = re.sub(r":[A-Za-z_]\w*", "[^/]+", rx) + "$"
    try:
        return re.match(rx, path) is not None
    except re.error:
        return False


def _assets(site: Path, pages: list[Path]) -> tuple[set[str], set[str]]:
    """Chemins (relatifs à la racine du site) des images et des polices réellement référencés."""
    imgs: set[str] = set()
    fonts: set[str] = set()
    exts = r"(?:webp|jpe?g|png|avif|gif|svg|webm|mp4|woff2?|ttf|otf)"

    def add(raw: str, base: Path):
        raw = raw.strip().split()[0] if raw.strip() else ""
        if not raw or raw.startswith(("data:", "http:", "https:", "//", "#")):
            return
        raw = raw.split("?")[0].split("#")[0]
        path = PurePosixPath(raw) if raw.startswith("/") else PurePosixPath(
            (base.relative_to(site) / raw).as_posix())
        norm = posixpath.normpath("/" + str(path).lstrip("/"))   # `/contact/../x.webp` → `/x.webp`
        (fonts if re.search(r"\.(woff2?|ttf|otf)$", norm, re.I) else imgs).add(norm)

    for page in pages:
        html = read(page)
        for m in re.finditer(r'(?:src|href)\s*=\s*["\']([^"\']+\.%s)["\']' % exts, html, re.I):
            add(m.group(1), page.parent)
        for m in re.finditer(r'srcset\s*=\s*["\']([^"\']+)["\']', html, re.I):
            for part in m.group(1).split(","):
                if part.strip():
                    add(part, page.parent)
        for m in re.finditer(r'url\(\s*["\']?([^)"\']+\.%s)' % exts, html, re.I):
            add(m.group(1), page.parent)
    for css in site.rglob("*.css"):
        txt = read(css)
        for m in re.finditer(r'url\(\s*["\']?([^)"\']+\.(?:woff2?|ttf|otf))', txt, re.I):
            add(m.group(1), css.parent)
    return imgs, fonts


def check_headers(site: Path, host: str) -> list[Finding]:
    hfile = site / "_headers"
    out: list[Finding] = []
    if not hfile.exists():
        if (site / "vercel.json").exists():
            return _check_vercel(site)
        out.append(Finding("D2", "P3", "_headers", "aucun fichier `_headers` : l'hôte ne reçoit aucune "
                           "règle de cache ni de sécurité depuis le dépôt",
                           "en ajouter un si l'hôte le lit (Cloudflare Pages, Netlify) ; sinon régler "
                           "le cache côté tableau de bord et le prouver par un `curl -I`"))
        return out

    blocks = parse_headers(hfile)
    workers = uses_workers_assets(site)
    bad = [p for p, _ in blocks if not pattern_is_valid(p, workers)]
    if bad:
        out.append(Finding(
            "D2", "P1", f"_headers · {', '.join(bad[:3])}",
            "motif que l'hôte n'appliquera jamais : sur Cloudflare Pages le splat ne vaut qu'en fin de "
            "motif (`/*.webp` ne matche rien — la règle de cache proposée le 23/10 serait restée sans effet)",
            "cibler par dossier (`/assets/*`) ou, pour du cache par extension, passer par une Cache Rule "
            "du tableau de bord ; sur Vercel, `vercel.json` accepte une expression de chemin"))

    imgs, fonts = _assets(site, pages_of(site))

    def uncovered(paths: set[str]) -> list[str]:
        miss = []
        for path in sorted(paths):
            covered = any(pattern_is_valid(pat, workers) and pattern_matches(pat, path)
                          and max_age(h.get("cache-control", "")) > 0 for pat, h in blocks)
            if not covered:
                miss.append(path)
        return miss

    miss_img = uncovered(imgs)
    if miss_img:
        out.append(Finding("D2", "P1", f"{len(miss_img)}/{len(imgs)} image(s), ex. {miss_img[0]}",
                           "aucune règle de cache ne couvre ces images : l'hôte renvoie "
                           "`max-age=0, must-revalidate` (mesuré en ligne) et le navigateur revalide "
                           "chaque photo à chaque visite",
                           "`Cache-Control: public, max-age=604800` sur le dossier des images (7 jours "
                           "tant que les noms ne sont pas hachés, puis 1 an + `immutable`)"))
    miss_font = uncovered(fonts)
    if miss_font:
        out.append(Finding("D2", "P2", f"{len(miss_font)}/{len(fonts)} police(s), ex. {miss_font[0]}",
                           "aucune règle de cache ne couvre ces polices",
                           "`Cache-Control: public, max-age=31536000, immutable`"))

    star = next((h for p, h in blocks if p == "/*"), {})
    html_cc = star.get("cache-control", "")
    if html_cc and max_age(html_cc) > 0 and "revalidate" not in html_cc.lower():
        out.append(Finding("D2", "P1", "_headers · /*", f"le HTML est mis en cache {html_cc} : une page "
                           "corrigée resterait servie",
                           "garder le HTML à `max-age=0, must-revalidate`"))

    if "strict-transport-security" not in star:
        out.append(Finding("D8", "P2", "_headers",
                           "pas de HSTS : le navigateur n'est pas prévenu que le domaine est en HTTPS seul",
                           "`Strict-Transport-Security: max-age=31536000; includeSubDomains` — `preload` "
                           "seulement quand le domaine et tous ses sous-domaines sont HTTPS pour de bon"))
    if "content-security-policy" not in star:
        out.append(Finding("D8", "P3", "_headers", "pas de Content-Security-Policy",
                           "politique conservatrice : `default-src 'self'; img-src 'self' data:; "
                           "script-src 'self' 'unsafe-inline'; frame-ancestors 'none'` (l'inline impose "
                           "'unsafe-inline', la politique borne quand même les origines)"))
    return out


def _check_vercel(site: Path) -> list[Finding]:
    """Vercel : `vercel.json` accepte une expression de chemin, le cache par extension y est possible."""
    try:
        cfg = json.loads(read(site / "vercel.json"))
    except (json.JSONDecodeError, OSError):
        return [Finding("D2", "P3", "vercel.json", "illisible", "vérifier le JSON")]
    out: list[Finding] = []
    rules = cfg.get("headers") or []
    cached = any(max_age(((r.get("headers") or [{}])[0]).get("value", "")) > 0 for r in rules)
    if not cached:
        out.append(Finding("D2", "P1", "vercel.json",
                           "aucune règle de cache pour les assets dans `vercel.json`",
                           'ajouter `{"source": "/(.*)\\.(webp|jpg|png|woff2)", "headers": '
                           '[{"key": "Cache-Control", "value": "public, max-age=604800"}]}`'))
    return out


# --------------------------------------------------------------------------- D3 favicon

def check_favicon(site: Path, pages: list[Path]) -> list[Finding]:
    """Icônes : les fichiers **et** leur déclaration. Les fichiers peuvent vivre n'importe où (le site
    DM les mettrait à la racine, un autre sous `/assets/`) : ce qui compte est que le `<link>` pointe
    sur un fichier qui existe."""
    out: list[Finding] = []
    refs: dict[str, set[str]] = {}
    for page in pages:
        for m in re.finditer(r'<link\b[^>]*rel\s*=\s*["\'](?:shortcut )?icon["\'][^>]*>', read(page), re.I):
            href = re.search(r'href\s*=\s*["\']([^"\']+)', m.group(0))
            if href and not href.group(1).startswith("data:"):
                refs.setdefault((page, href.group(1).split("?")[0]), set()).add(page.name)
        for m in re.finditer(r'<link\b[^>]*rel\s*=\s*["\']apple-touch-icon["\'][^>]*>', read(page), re.I):
            href = re.search(r'href\s*=\s*["\']([^"\']+)', m.group(0))
            if href and not href.group(1).startswith("data:"):
                refs.setdefault((page, href.group(1).split("?")[0]), set()).add(page.name)

    root = {p.name for p in site.iterdir() if p.is_file()}
    if not refs:
        missing = [n for n in ("favicon.ico", "favicon.svg", "apple-touch-icon.png") if n not in root]
        if missing:
            out.append(Finding("D3", "P2", site.name,
                               f"aucune page ne déclare d'icône, et ces fichiers manquent : {', '.join(missing)}",
                               "générer `favicon.svg`, `favicon.ico` et `apple-touch-icon.png` (180 px) depuis "
                               "le logo, et les déclarer dans l'en-tête partagé : l'onglet reste blanc et "
                               "`/favicon.ico` répond 404 tant qu'elles manquent"))
        else:
            out.append(Finding("D3", "P2", f"0/{len(pages)} page(s)",
                               "les fichiers d'icônes existent mais aucune page ne les déclare",
                               "ajouter les trois `<link>` dans l'en-tête partagé"))
        return out

    dead = []
    for (page, href), where in refs.items():
        target = site / href.lstrip("/") if href.startswith("/") else (page.parent / href).resolve()
        if not target.exists():
            dead.append(f"{href} ({len(where)} page(s))")
    if dead:
        out.append(Finding("D3", "P2", ", ".join(dead[:3]),
                           "icône déclarée mais fichier absent",
                           "produire le fichier ou corriger le `href` : le navigateur demande une icône "
                           "qui n'existe pas"))
    return out


# --------------------------------------------------------------------------- D4 URL

def check_urls(site: Path, pages: list[Path], host: str) -> list[Finding]:
    out = []
    if not host:
        return out
    h = re.escape(host)
    dbl = re.compile(r"https?://%s//" % h, re.I)
    plain = re.compile(r"http://%s/" % h, re.I)
    hits = [(p, len(dbl.findall(read(p)))) for p in pages]
    hits = [(p, n) for p, n in hits if n]
    if hits:
        total = sum(n for _, n in hits)
        out.append(Finding("D4", "P2", f"{len(hits)} page(s) · {total} occurrence(s)",
                           f"URL malformée après l'hôte : `https://{host}//fichier` (double barre) — "
                           "le navigateur répare souvent, les validateurs non",
                           "retirer la barre en trop à la source (souvent dans les données structurées)"))
    insecure = [p for p in pages if plain.search(read(p))]
    if insecure:
        out.append(Finding("D4", "P2", f"{len(insecure)} page(s)",
                           f"au moins un `http://{host}/` sur notre propre hôte",
                           "passer en `https://` absolu ou en chemin relatif"))
    return out


# --------------------------------------------------------------------------- D5 llms.txt

def check_llms(site: Path) -> list[Finding]:
    llms, smap = site / "llms.txt", site / "sitemap.xml"
    out = []
    if not llms.exists():
        return [Finding("D5", "P2", "llms.txt", "fichier de découverte IA absent",
                        "le générer au build, avec la liste des pages et un compte vérifié")]
    if not smap.exists():
        return out
    listed = {u.rstrip("/") for u in re.findall(r"https?://[^\s)\]>\"']+", read(llms))}
    locs = {u.rstrip("/") for u in LOC_RE.findall(read(smap))}
    missing = sorted(locs - listed)
    if not missing:
        return out
    en = [u for u in missing if re.search(r"/en(/|$)", u)]
    out.append(Finding(
        "D5", "P2", "llms.txt",
        f"{len(missing)} URL du sitemap absentes de llms.txt, dont {len(en)} anglaises"
        + (f" (ex. {missing[0]})" if missing else ""),
        "lister les deux langues (ou un `llms.txt` par langue + un index) : le fichier est la carte que "
        "lisent les moteurs et assistants"))
    extra = sorted(listed - locs - {"https://schema.org", "https://dmoptiquesarl.com"})
    extra = [u for u in extra if not u.rstrip("/").endswith(".xml")]
    if extra:
        out.append(Finding("D5", "P3", "llms.txt", f"{len(extra)} URL de llms.txt absentes du sitemap",
                           "vérifier qu'elles existent vraiment ; sinon les retirer"))
    return out


# --------------------------------------------------------------------------- D6 partage social

def meta(html: str, key: str) -> str | None:
    for tag in META_RE.findall(html):
        if re.search(r'(?:property|name)\s*=\s*["\']%s["\']' % re.escape(key), tag, re.I):
            m = re.search(r'content\s*=\s*["\']([^"\']*)', tag, re.I)
            return m.group(1) if m else None
    return None


def check_social(site: Path, pages: list[Path]) -> list[Finding]:
    webp, nodim, imgs = 0, 0, set()
    sample = None
    for page in pages:
        html = read(page)
        og = meta(html, "og:image")
        if not og:
            continue
        imgs.add(og)
        if og.lower().split("?")[0].endswith(".webp"):
            webp += 1
            sample = sample or (page, og)
        if not (meta(html, "og:image:width") and meta(html, "og:image:height")):
            nodim += 1
    out = []
    if webp:
        page, og = sample
        out.append(Finding(
            "D6", "P2", f"{webp} page(s), ex. {url_of(site, page)}",
            f"`og:image` en WebP ({og.rsplit('/', 1)[-1]}) : l'aperçu de partage est incertain dans "
            "WhatsApp, le canal principal de ces clients",
            "tester un vrai lien dans une conversation ; si l'aperçu est vide ou mal recadré, produire un "
            "JPEG 1200 × 630 par monture (ou retomber sur `og.jpg`)"))
    if nodim:
        out.append(Finding("D6", "P3", f"{nodim} page(s)",
                           "`og:image` sans `og:image:width`/`height`/`type`",
                           "les déclarer : les aperçus se dessinent avant le téléchargement de l'image"))
    if len(imgs) and len(imgs) < len(pages) // 2:
        out.append(Finding("D6", "P3", f"{len(imgs)} image(s) pour {len(pages)} page(s)",
                           "des pages partagent la même image d'aperçu",
                           "une image par monture rend les liens partagés reconnaissables"))
    return out


# --------------------------------------------------------------------------- D7 données structurées

def ld_blocks(html: str) -> list:
    out, broken = [], 0
    for raw in LDJSON_RE.findall(html):
        try:
            out.append(json.loads(raw))
        except json.JSONDecodeError:
            broken += 1
    return out


def walk(node, acc: list[dict]):
    if isinstance(node, dict):
        acc.append(node)
        for v in node.values():
            walk(v, acc)
    elif isinstance(node, list):
        for v in node:
            walk(v, acc)
    return acc


def check_schema(site: Path, pages: list[Path]) -> list[Finding]:
    out = []
    priced, no_product, home_ok, same_as = [], [], False, False
    product_pages = 0
    for page in pages:
        html = read(page)
        blocks = ld_blocks(html)
        nodes = walk(blocks, [])
        types = {str(n.get("@type")) for n in nodes if isinstance(n, dict)}
        if any({"price", "priceCurrency"} & set(n) for n in nodes if isinstance(n, dict)):
            priced.append(page)
        biz = [n for n in nodes if isinstance(n, dict)
               and str(n.get("@type")) in LOCAL_TYPES]
        if biz:
            if url_of(site, page) == "/":
                b = biz[0]
                home_ok = bool(b.get("telephone") and (b.get("address") or b.get("location")))
            if any(b.get("sameAs") for b in biz):
                same_as = True
        u = url_of(site, page)
        if re.search(r"^/(en/)?montures(?:/[^/]+){2,}/$", u):
            product_pages += 1
            if "Product" not in types:
                no_product.append(page)
    if priced:
        out.append(Finding("D7", "P1", f"{len(priced)} page(s), ex. {url_of(site, priced[0])}",
                           "un prix apparaît dans le JSON-LD : règle maison : aucun prix public",
                           "retirer `price`/`priceCurrency` ; un `Product` sans `Offer` reste valable"))
    if product_pages and no_product:
        out.append(Finding("D7", "P2", f"{len(no_product)}/{product_pages} fiche(s)",
                           "page de monture sans `Product` : seul le fil d'Ariane est déclaré",
                           "ajouter `name`, `image`, `description`, `brand` (celle de la monture, lue sur "
                           "la photo) et `sku` = la référence — **sans prix** et sans `Offer`"))
    if not home_ok:
        out.append(Finding("D7", "P2", "accueil",
                           "entité locale sans téléphone ou sans adresse dans le JSON-LD",
                           "déclarer l'entité `Optician` complète : téléphone, adresse, horaires"))
    if not same_as:
        out.append(Finding("D7", "P3", "accueil",
                           "aucun `sameAs` : les profils sociaux ne sont pas reliés à l'entité, donc les "
                           "améliorations « identité du site » ne peuvent pas se déclencher",
                           "ajouter les URL Facebook / Instagram déjà présentes en pied de page"))
    return out


# --------------------------------------------------------------------------- sortie

def run(site: Path, base: str) -> list[Finding]:
    host = (base or "").split("//", 1)[-1].split("/", 1)[0].replace("www.", "")
    pages = pages_of(site)
    findings: list[Finding] = []
    findings += check_nav(site, pages)
    findings += check_headers(site, host)
    findings += check_favicon(site, pages)
    findings += check_urls(site, pages, host)
    findings += check_llms(site)
    findings += check_social(site, pages)
    findings += check_schema(site, pages)
    order = {"P1": 0, "P2": 1, "P3": 2}
    return sorted(findings, key=lambda f: (order[f.sev], f.code))


def main() -> int:
    ap = argparse.ArgumentParser(description="Porte de livraison (8 classes que les autres portiques ne voient pas)")
    ap.add_argument("site", type=Path)
    ap.add_argument("--base", default="", help="URL du site : sert à reconnaître l'hôte et les URL malformées")
    ap.add_argument("--strict", action="store_true", help="échouer aussi sur les P2")
    ap.add_argument("--json", action="store_true", help="sortie machine")
    args = ap.parse_args()

    if not args.site.is_dir():
        print(f"✗ {args.site} n'est pas un dossier", file=sys.stderr)
        return 2
    findings = run(args.site, args.base)

    if args.json:
        print(json.dumps([f._asdict() for f in findings], ensure_ascii=False, indent=2))
    else:
        print(f"\nPORTE DE LIVRAISON — {args.site}  ({len(pages_of(args.site))} page(s))")
        for f in findings:
            print(f"\n  [{f.sev}] {f.code} · {f.where}\n        {f.message}\n        → {f.fix}")
        counts = {s: sum(1 for f in findings if f.sev == s) for s in ("P1", "P2", "P3")}
        print(f"\n  TOTAL {counts['P1']} P1 · {counts['P2']} P2 · {counts['P3']} P3 — "
              f"{'VERT' if not counts['P1'] else 'ROUGE (P1)'}")

    fail = any(f.sev == "P1" for f in findings)
    if args.strict:
        fail = fail or any(f.sev == "P2" for f in findings)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
