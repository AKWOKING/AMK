#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit le **miroir anglais /en/** des trois pages réelles du site AMK.

Pourquoi un fichier statique et pas le bouton EN existant : aujourd'hui l'anglais du site n'existe
que dans des attributs `data-en`, réécrits par JavaScript. Google ne l'indexe pas — c'est le P0 de
`site/SEO-AUDIT-2026-10-23.md` §3.1 (0 paire hreflang, 1 clic en 7 jours). Un `hreflang` n'a de
valeur que s'il pointe vers une URL qui **sert vraiment** l'anglais dans son HTML.

Ce que le script fait, page par page :

  1. il prend la page française, et remplace le contenu de chaque élément qui porte `data-en` par
     cette valeur — exactement ce que fait `setLang('en')` dans le navigateur, mais **au moment de
     la construction** ;
  2. il retire les attributs de bascule (`data-en`, `data-fr`, `data-alt-*`, `data-ph-*`) : la page
     ne peut plus repasser en français par accident (une préférence `localStorage` oubliée, par
     exemple) ;
  3. il remplace le sélecteur EN/FR par **deux liens** : la page reste indexable et le visiteur peut
     revenir au français sans JavaScript ;
  4. il réécrit `<html lang>`, le canonical, les `hreflang`, le titre, la description et l'OG ;
  5. il préfixe les chemins relatifs (`img/`, `assets/`, `favicon`) pour la profondeur `/en/`.

Il est **idempotent** : relancé, il réécrit les mêmes fichiers. Les pages françaises, elles, sont
seulement retouchées pour porter les `hreflang` et un lien EN qui pointe vers la vraie page anglaise
(fonction `patch_french`).

Usage :
    python3 tools/site/build_en_pages.py --check     # n'écrit rien, dit ce qui manque
    python3 tools/site/build_en_pages.py             # écrit site/en/*.html et patche les 3 FR
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
EN_DIR = SITE / "en"
BASE = "https://amk-cm.vercel.app"

# les trois pages « réelles » (les pages concepts gardent leur bascule JS)
PAGES = {
    "index.html": {
        "url_fr": f"{BASE}/",
        "url_en": f"{BASE}/en/",
        "title": "Websites for schools and clinics in Cameroon | AMK Douala",
        "description": "Your school or clinic is judged on Google before anyone calls you. Bilingual FR|EN site, WhatsApp bookings, free preview.",
        "og_title": "Websites for schools and clinics in Cameroon | AMK",
        "og_desc": "A site built to be found. Free preview · bilingual FR|EN · live as soon as you approve it.",
    },
    "clinic-bonaberi.html": {
        "url_fr": f"{BASE}/clinic-bonaberi.html",
        "url_en": f"{BASE}/en/clinic-bonaberi.html",
        "title": "Clinic & Lab Website Concept · Bonabéri Medical Centre | AMK",
        "description": "A patient-first clinic concept by AMK: transparent FCFA pricing, same-day laboratory, maternity scans, WhatsApp booking in English and French. Free preview.",
        "og_title": "Clinic & Lab Website Concept · Bonabéri Medical Centre | AMK",
        "og_desc": "A patient-first clinic concept by AMK: pricing, laboratory, maternity scans, WhatsApp booking.",
    },
    "mitoc.html": {
        "url_fr": f"{BASE}/mitoc.html",
        "url_en": f"{BASE}/en/mitoc.html",
        "title": "Midas Touch Optic Center, Molyko Buea · Eye Exams, Lenses & Frames (Website Concept by AMK)",
        "description": "A website concept for Midas Touch Optic Center, Molyko-Malingo, Buea: eye tests and refraction, prescription lenses mounted on site, frame gallery, WhatsApp booking, English and French.",
        "og_title": "Midas Touch Optic Center, Molyko Buea · Website Concept by AMK",
        "og_desc": "Eye tests and refraction, lenses mounted on site, frame gallery, WhatsApp booking, English and French.",
    },
}


# Traductions des chaînes de données structurées (page d'accueil). Le JSON-LD français reste celui du
# site français ; le miroir anglais ne peut pas afficher une FAQ anglaise et déclarer une FAQ
# française — Google lit les deux.
JSONLD_EN = {
    "Création de sites web bilingues FR|EN pour écoles privées, cliniques et laboratoires au Cameroun. Aperçu gratuit, en ligne dès votre validation.":
        "Bilingual EN|FR websites for private schools, clinics and laboratories in Cameroon. Free preview, live as soon as you approve it.",
    "MTN Mobile Money, Orange Money, espèces": "MTN Mobile Money, Orange Money, cash",
    "Création de site web au Cameroun": "Website design in Cameroon",
    "Création de site web": "Website design",
    "Site vitrine bilingue FR|EN pour écoles privées, cliniques et laboratoires au Cameroun.":
        "Bilingual EN|FR website for private schools, clinics and laboratories in Cameroon.",
    "Site web bilingue FR|EN": "Bilingual EN|FR website",
    "Chaque page existe en français et en anglais, pas un widget de traduction.":
        "Every page exists in French and in English, not a translation widget.",
    "Prise de rendez-vous WhatsApp": "WhatsApp booking",
    "Chaque bouton ouvre WhatsApp avec le message déjà rédigé : inscriptions, rendez-vous, questions.":
        "Every button opens WhatsApp with the message already written: enrolment, appointments, questions.",
    "Référencement local": "Local SEO",
    "Structure, mots-clés et données structurées pour être trouvé sur « école à Douala », « laboratoire à Buea ».":
        "Structure, keywords and structured data so you are found for “school in Douala”, “laboratory in Buea”.",
    "Nom de domaine et hébergement": "Domain name and hosting",
    "Domaine au nom du client, hébergement sécurisé, fichiers au client.":
        "Domain in the client's name, secure hosting, files owned by the client.",
}

LANG_CSS = """
/* sélecteur EN/FR en liens : même apparence que les boutons, sans JavaScript */
.lang-sw a,.lang a{display:inline-block;background:none;border:none;color:var(--slate-l);font-weight:700;
  font-size:13px;padding:7px 14px;text-decoration:none;transition:.15s}
.lang-sw a.on{background:var(--amber);color:var(--navy)}
.lang-sw a:focus-visible,.lang a:focus-visible{outline-offset:-2px}
.lang a{display:inline-block;text-decoration:none;font-size:12.5px;font-weight:700;padding:6px 12px}
.lang a.on{background:var(--g800,#14532d);color:#fff}
header#hdr .lang-sw a{color:#6B7584}
header#hdr .lang-sw a.on{color:var(--navy)}
"""


def _fragment(markup: str):
    return BeautifulSoup(markup, "html.parser")


def _swap_to_english(soup: BeautifulSoup) -> int:
    """Remplace le contenu de chaque élément `data-en` par sa version anglaise. Retourne le compte."""
    n = 0
    for el in soup.select("[data-en]"):
        value = el.get("data-en")
        if value is None:
            continue
        el.clear()
        el.append(_fragment(value))
        n += 1
    for el in soup.select("[data-alt-en]"):
        if el.get("data-alt-en"):
            el["alt"] = el["data-alt-en"]
    for el in soup.select("[data-ph-en]"):
        if el.get("data-ph-en"):
            el["placeholder"] = el["data-ph-en"]
    return n


def _drop_switch_attributes(soup: BeautifulSoup) -> None:
    for el in soup.find_all(True):
        for attr in list(el.attrs):
            if attr.startswith("data-en") or attr.startswith("data-fr") or \
               attr.startswith("data-alt") or attr.startswith("data-ph"):
                del el[attr]


def _page_slug(name: str) -> str:
    return "" if name == "index.html" else name


def _rewrite_links(soup: BeautifulSoup, name: str) -> None:
    """Depuis /en/, tout ce qui est relatif doit remonter d'un cran — sauf les trois pages miroir."""
    for el in soup.find_all(True):
        for attr in ("href", "src", "action"):
            v = el.get(attr)
            if not v or v.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:", "/", "//")):
                continue
            if v.endswith(".html"):
                if v in PAGES:
                    continue                       # reste dans /en/
                el[attr] = "../" + v
            elif v in ("favicon.svg", "robots.txt", "llms.txt") or \
                    v.startswith("assets/") or v.startswith("img/"):
                el[attr] = "../" + v


def _strip_lang_switch_js(soup: BeautifulSoup) -> None:
    """Neutralise l'initialisation de langue : sur une page anglaise, elle ne doit rien changer."""
    for script in soup.find_all("script"):
        if not script.string or "amk-lang" not in script.string:
            continue
        txt = script.string
        txt = txt.replace(
            'var q = new URLSearchParams(location.search).get("lang");',
            'var q = null; // page anglaise : la langue est fixée par le HTML')
        txt = txt.replace('if (q === "fr" || q === "en") setLang(q);', 'if (false) {}')
        txt = txt.replace('else if (saved === "fr" || saved === "en") setLang(saved);', '')
        script.string = txt


def _head(soup: BeautifulSoup, meta: dict, name: str) -> None:
    soup.html["lang"] = "en"

    if soup.title:
        soup.title.string = meta["title"]

    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        desc["content"] = meta["description"]

    can = soup.find("link", rel="canonical")
    if can is None:
        can = soup.new_tag("link", rel="canonical")
        soup.head.append(can)
    can["href"] = meta["url_en"]

    # hreflang : le FR reste la version de référence, l'EN est son miroir, x-default = FR
    for old in soup.find_all("link", rel="alternate"):
        if old.get("hreflang"):
            old.decompose()
    for lang, href in (("fr", meta["url_fr"]), ("en", meta["url_en"]), ("x-default", meta["url_fr"])):
        link = soup.new_tag("link", rel="alternate", hreflang=lang, href=href)
        soup.head.append(link)

    for prop, value in (("og:title", meta["og_title"]), ("og:description", meta["og_desc"]),
                        ("og:url", meta["url_en"]), ("og:locale", "en_US")):
        tag = soup.find("meta", attrs={"property": prop})
        if tag is None:
            tag = soup.new_tag("meta", property=prop)
            soup.head.append(tag)
        tag["content"] = value
    tw_title = soup.find("meta", attrs={"name": "twitter:title"})
    if tw_title:
        tw_title["content"] = meta["og_title"]
    tw_desc = soup.find("meta", attrs={"name": "twitter:description"})
    if tw_desc:
        tw_desc["content"] = meta["og_desc"]

    alt = soup.find("meta", attrs={"property": "og:locale:alternate"})
    if alt:
        alt["content"] = "fr_FR"

    # images sociales absolues
    for tag in soup.find_all("meta"):
        v = tag.get("content", "")
        if isinstance(v, str) and v.startswith("../"):
            tag["content"] = v[3:]

    if not soup.find("style", id="en-lang-sw"):
        style = soup.new_tag("style", id="en-lang-sw")
        style.string = LANG_CSS
        soup.head.append(style)


def _lang_switch(soup: BeautifulSoup, name: str) -> None:
    """Deux liens à la place des boutons : retour au français, anglais courant.

    Le site utilise deux conteneurs selon les pages : `.lang-sw` (accueil) et `.lang` (concept
    clinique, concept optique). Les deux sont traités, sinon le miroir anglais d'une page garde un
    bouton qui ne mène nulle part.
    """
    fr_href = "../" + name if name != "index.html" else "../"
    touched = 0
    for selector in (".lang-sw", ".lang"):
        for div in soup.select(selector):
            div.clear()
            a_fr = soup.new_tag("a", href=fr_href, hreflang="fr")
            a_fr.string = "FR"
            a_en = soup.new_tag("a", href=name, hreflang="en", **{"class": "on"})
            a_en["aria-current"] = "page"
            a_en.string = "EN"
            div.append(a_fr)
            div.append(a_en)
            touched += 1
    return touched


def _jsonld_english(soup: BeautifulSoup, name: str) -> None:
    """Traduit les chaînes de données structurées et reconstruit la FAQ depuis le DOM anglais."""
    faq_items = []
    for det in soup.select("#faq details"):
        q = det.find("summary")
        a = det.select_one(".ans")
        if q and a:
            faq_items.append((q.get_text(" ", strip=True), a.get_text(" ", strip=True)))

    for script in soup.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue
        changed = False

        def walk(node):
            nonlocal changed
            if isinstance(node, dict):
                for key, val in list(node.items()):
                    if isinstance(val, str) and val in JSONLD_EN:
                        node[key] = JSONLD_EN[val]
                        changed = True
                    elif key == "inLanguage":
                        node[key] = "en"
                        changed = True
                    else:
                        walk(val)
                if node.get("@type") == "FAQPage" and faq_items:
                    node["mainEntity"] = [
                        {"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in faq_items
                    ]
                    changed = True
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(data)
        if changed:
            script.string = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

def build_one(name: str, meta: dict) -> str:
    src = (SITE / name).read_text(encoding="utf-8")
    soup = BeautifulSoup(src, "html.parser")
    _swap_to_english(soup)
    _strip_lang_switch_js(soup)
    _drop_switch_attributes(soup)
    _rewrite_links(soup, name)
    _head(soup, meta, name)
    _lang_switch(soup, name)
    _jsonld_english(soup, name)
    return "<!DOCTYPE html>\n" + str(soup.html)


def patch_french(name: str, meta: dict) -> bool:
    """Ajoute les hreflang et fait pointer le bouton EN vers la vraie page anglaise."""
    path = SITE / name
    html = path.read_text(encoding="utf-8")
    original = html

    for old in re.findall(r'\s*<link rel="alternate" hreflang="[^"]+" href="[^"]*">', html):
        html = html.replace(old, "")

    block = "".join(
        f'\n<link rel="alternate" hreflang="{lang}" href="{href}">'
        for lang, href in (("fr", meta["url_fr"]), ("en", meta["url_en"]), ("x-default", meta["url_fr"]))
    )
    html = html.replace('<link rel="canonical"', block + '\n<link rel="canonical"', 1)

    # la bascule EN devient un lien vers /en/ (le JS reste pour la bascule FR)
    en_url = "en/" if name == "index.html" else "en/" + name
    html = re.sub(
        r'<button id="btn-en(?:-m)?"[^>]*onclick="setLang\(\'en\'\)"[^>]*>EN</button>',
        f'<a class="lang-a" href="{en_url}" hreflang="en">EN</a>', html)
    # le bouton FR redevient explicite quand on l'a remplacé par un lien : il porte l'état courant
    html = html.replace('<a class="lang-a" href=', '<a class="lang-a" href=')

    if "/* lien de langue EN */" not in html:
        css = ("/* lien de langue EN */\n"
               ".lang-sw .lang-a{display:inline-block;background:none;border:none;color:var(--slate-l);"
               "font-weight:700;font-size:13px;padding:7px 14px;text-decoration:none}\n"
               "header#hdr .lang-sw .lang-a{color:#6B7584}\n"
               ".lang .lang-a{display:inline-block;text-decoration:none;font-size:12.5px;"
               "font-weight:700;padding:6px 12px;color:var(--muted)}\n"
               ".m-actions .lang-a{display:inline-block;padding:6px 12px;text-decoration:none;"
               "color:inherit;font-weight:700}\n")
        html = html.replace("</style>", css + "</style>", 1)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="ne rien écrire, seulement constater")
    args = ap.parse_args()

    EN_DIR.mkdir(exist_ok=True)
    changed = 0
    for name, meta in PAGES.items():
        out = EN_DIR / name
        html = build_one(name, meta)
        if args.check:
            state = "présent" if out.exists() else "absent"
            print(f"  {state:8} site/en/{name}")
            continue
        out.write_text(html, encoding="utf-8")
        changed += 1
        if patch_french(name, meta):
            changed += 1
        print(f"  écrit site/en/{name} (+ hreflang sur site/{name})")
    if not args.check:
        print(f"{changed} fichier(s) touché(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
