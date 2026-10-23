#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Liens sociaux AMK dans le pied de page du site — **derrière les logos**, pas derrière des mots.

Ruling King 23/10/2026 : « add the links of the social media on the website but I do not want you
hidding the links behind words I want it to be behind their respective logos ».

Ce que l'outil fait, et rien de plus :
  1. insère un bloc `.amk-soc` (label + trois pastilles cliquables) dans la **première colonne** du
     pied de page ;
  2. ajoute la feuille de style `.amk-soc` (une seule fois) ;
  3. complète le `sameAs` du JSON-LD (c'est ce que Google lit) ;
  4. est **idempotent** : relancer ne duplique rien.

Pourquoi un outil : douze pages autonomes, chacune avec son CSS. Une retouche à la main laisse
toujours une page sans lien, et un pied de page différent d'une page à l'autre se voit.

⚠️ Deux règles tenues ici, et pas ailleurs :
  • **accessibilité** — le lien n'a pas de texte visible (c'est le logo), donc chaque lien porte un
    `<span>` masqué (`data-en` / `data-fr`) qui donne son nom au lecteur d'écran, et qui **suit la
    langue** de la page comme tout le reste du site ;
  • **provenance des tracés** — les trois `path` viennent de **Simple Icons 15.0.0** (npm,
    `registry.npmjs.org/simple-icons`), publiés sous **CC0 1.0**. Ce sont les logos officiels, pas des
    dessins approximatifs. Ne pas les retoucher : un logo redessiné n'est plus le logo.

Usage :
    python3 tools/site/add_amk_social.py --check     # n'écrit rien, dit l'état de chaque page
    python3 tools/site/add_amk_social.py             # applique
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"

# ── la seule source des adresses ───────────────────────────────────────────────
# Facebook : numéro de page (aucun nom d'utilisateur — ruling du 23/10, on garde le nom long).
# Instagram / TikTok : identifiants déjà en place. Si l'un change, on modifie ICI et on relance.
SOCIAL = [
    ("facebook", "Facebook", "https://www.facebook.com/profile.php?id=61595803408384"),
    ("instagram", "Instagram", "https://www.instagram.com/amkweb.cm"),
    ("tiktok", "TikTok", "https://www.tiktok.com/@amkweb"),
]

# Simple Icons 15.0.0 — CC0 1.0. Tracés officiels, viewBox 0 0 24 24.
PATHS = {
    "facebook": "M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z",
    "instagram": "M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077",
    "tiktok": "M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z",
}

MARKER_CSS = "/* amk-social */"
MARKER_BLOCK = 'class="amk-soc"'
MARKER_PREF = 'class="amk-psrc"'

# ── source préférée sur Google (23/10/2026) ───────────────────────────────────
# Le domaine est celui de la canonique de la page, pas une invention : la fonction n'accepte
# qu'un domaine ou un sous-domaine (doc Search Central, « Feature availability »). Le jour où le
# site passe sur son domaine propre, cette seule ligne change et l'outil est relancé.
PREF_DOMAIN = "amk-cm.vercel.app"
PREF_URL = f"https://www.google.com/preferences/source?q={PREF_DOMAIN}"
# Étoile dessinée par nous (aucun logo Google reproduit) : Simple Icons ne publie pas d'icône
# « source préférée », et imiter le G de Google poserait un problème de marque.
PREF_STAR = ("M12 2.6l2.9 5.88 6.49.94-4.7 4.58 1.11 6.46L12 17.4l-5.8 3.06 1.11-6.46"
             "-4.7-4.58 6.49-.94z")

CSS = MARKER_CSS + """.amk-soc{margin-top:24px}
.amk-soc .amk-soc-lbl{display:block;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#94A3B8;margin:0 0 10px}
.amk-soc .amk-soc-l{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0;padding:0}
.amk-soc a.amk-soc-a{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;width:44px;height:44px;padding:0;margin:0;border-radius:50%;border:1px solid rgba(148,163,184,.45);color:#E2E8F0;background:transparent;line-height:1;text-decoration:none;box-sizing:border-box;transition:color .18s ease,border-color .18s ease,background-color .18s ease}
.amk-soc a.amk-soc-a:hover,.amk-soc a.amk-soc-a:focus-visible{color:#F59E0B;border-color:#F59E0B;background:rgba(245,158,11,.08)}
.amk-soc a.amk-soc-a:focus-visible{outline:2px solid #FCD34D;outline-offset:2px}
.amk-soc a.amk-soc-a svg{display:block;width:18px;height:18px;flex:0 0 auto;fill:currentColor}
.amk-soc .amk-soc-h{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
@media (prefers-reduced-motion:reduce){.amk-soc a.amk-soc-a{transition:none}}
@media (max-width:420px){.amk-soc a.amk-soc-a{width:42px;height:42px}}
"""


def build_block() -> str:
    links = []
    for key, name, url in SOCIAL:
        links.append(
            f'<a class="amk-soc-a" href="{url}" target="_blank" rel="noopener" '
            f'title="{name}">'
            f'<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">'
            f'<path d="{PATHS[key]}"/></svg>'
            f'<span class="amk-soc-h" data-en="AMK on {name}" data-fr="AMK sur {name}">'
            f'AMK sur {name}</span></a>'
        )
    return (
        '<div class="amk-soc">'
        '<span class="amk-soc-lbl" data-en="Follow AMK" data-fr="Suivre AMK">Suivre AMK</span>'
        '<div class="amk-soc-l">' + "".join(links) + "</div></div>"
    )


# Feuille du badge, gardée à part : les pages déjà équipées du bloc social n'ont pas été
# réécrites quand le badge est arrivé (23/10) — le marqueur `.amk-psrc{` dit si la règle est là.
PREF_CSS = """.amk-psrc{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-top:14px;padding:0 14px;border:1px solid rgba(148,163,184,.45);border-radius:999px;color:#E2E8F0;background:transparent;font-size:13px;line-height:1.2;text-decoration:none;box-sizing:border-box;transition:color .18s ease,border-color .18s ease,background-color .18s ease}
.amk-psrc:hover,.amk-psrc:focus-visible{color:#F59E0B;border-color:#F59E0B;background:rgba(245,158,11,.08)}
.amk-psrc:focus-visible{outline:2px solid #FCD34D;outline-offset:2px}
.amk-psrc svg{display:block;width:14px;height:14px;flex:0 0 auto;fill:#FCD34D}
@media (prefers-reduced-motion:reduce){.amk-psrc{transition:none}}
"""


def build_pref() -> str:
    return (
        f'<a class="amk-psrc" href="{PREF_URL}" target="_blank" rel="noopener">'
        f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{PREF_STAR}"/>'
        f'</svg><span data-en="Add AMK as a preferred source on Google" '
        f'data-fr="Ajouter AMK comme source préférée sur Google">'
        f'Ajouter AMK comme source préférée sur Google</span></a>'
    )


def _match_div(html: str, open_idx: int) -> int:
    """Index du `</div>` qui ferme le `<div` ouvert à `open_idx` (comptage de balises)."""
    depth = 0
    token = re.compile(r"<(/?)div\b", re.I)
    for m in token.finditer(html, open_idx):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.start()
    raise ValueError("div non fermé")


def insert_block(html: str) -> str:
    """Dans la première colonne du `.f-grid` du pied de page (ou juste avant `</footer>`)."""
    if MARKER_BLOCK in html:          # idempotence : le bloc est déjà là → on ne pose que le badge
        return insert_pref(html)
    foot = html.find("<footer")
    if foot < 0:
        raise ValueError("pas de pied de page")
    grid = re.compile(r'<div class="[^"]*f-grid[^"]*">').search(html, foot)
    if grid:
        first_col = re.compile(r"<div\b").search(html, grid.end())
        if first_col:
            at = _match_div(html, first_col.start())
            return html[:at] + build_block() + "\n        " + html[at:]
    end = html.find("</footer>", foot)
    return html[:end] + "<div class=\"wrap\">" + build_block() + "</div>\n  " + html[end:]


def insert_pref(html: str) -> str:
    """Pose le badge « source préférée » à la fin du bloc `.amk-soc`, une seule fois."""
    if MARKER_PREF in html:
        return html
    at = html.find(MARKER_BLOCK)
    if at < 0:
        raise ValueError("pas de bloc social pour ancrer le badge")
    # fin du <div class="amk-soc"> : on referme juste avant son </div>
    end = _match_div(html, html.rfind("<div", 0, at))
    return html[:end] + build_pref() + html[end:]


def insert_css(html: str) -> str:
    if MARKER_CSS in html:
        return insert_pref_css(html)
    at = html.find("</style>")
    if at < 0:
        raise ValueError("pas de feuille de style")
    return html[:at] + CSS + html[at:]


def insert_pref_css(html: str) -> str:
    if ".amk-psrc{" in html:
        return html
    at = html.find("</style>")
    if at < 0:
        raise ValueError("pas de feuille de style")
    return html[:at] + PREF_CSS + html[at:]


def update_sameas(html: str) -> str:
    """Ajoute les trois adresses au `sameAs` existant, sans doublon."""
    urls = [u for _, _, u in SOCIAL]

    def repl(m: re.Match) -> str:
        body = m.group(1)
        missing = [u for u in urls if u not in body]
        if not missing:
            return m.group(0)
        add = ",".join(f'\n    "{u}"' for u in missing)
        return '"sameAs": [' + body.rstrip() + "," + add + "\n   ]"

    return re.sub(r'"sameAs"\s*:\s*\[(.*?)\]', repl, html, count=1, flags=re.S)


# Les trois pages RÉELLES d'AMK. Les concepts (`sample-*`, `clinic-bonaberi`, `mitoc`) portent
# l'identité d'un client fictif ou prospect : y poser nos icônes mélangerait deux marques.
TARGETS = [
    "index.html",
    "creation-site-web-ecole-cameroun.html",
    "creation-site-web-clinique-cameroun.html",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="n'écrit rien")
    args = ap.parse_args()

    rc = 0
    for name in TARGETS:
        path = SITE / name
        html = path.read_text(encoding="utf-8")
        state = [
            "logique" if MARKER_CSS in html else "CSS manquant",
            "bloc" if MARKER_BLOCK in html else "bloc manquant",
            "sameAs" if all(u in html for _, _, u in SOCIAL) else "sameAs partiel",
            "source" if MARKER_PREF in html else "badge manquant",
        ]
        print(f"{name:46s} {' · '.join(state)}")
        if args.check:
            continue
        try:
            out = update_sameas(insert_pref(insert_css(insert_block(html))))
        except ValueError as exc:
            print(f"  ✗ {exc}")
            rc = 1
            continue
        if out != html:
            path.write_text(out, encoding="utf-8")
            print("  ✓ écrit")
    return rc


if __name__ == "__main__":
    sys.exit(main())
