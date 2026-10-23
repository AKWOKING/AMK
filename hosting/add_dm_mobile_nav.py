#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE — menu de navigation mobile (P1 de l'audit du 23/10) et icônes d'onglet.

    python3 hosting/add_dm_mobile_nav.py --check     # ne touche à rien, dit ce qui manque
    python3 hosting/add_dm_mobile_nav.py             # applique aux 97 pages

**Le défaut** : sous 980 px, `nav.nav{display:none}` et **aucun bouton de menu**. Un visiteur au
téléphone n'avait, pour se déplacer, que le pied de page. C'était le P1 n°1 de l'audit extérieur.

**La solution retenue : `<details>/<summary>`.** Pas de bouton piloté en JavaScript, pas de
`aria-expanded` à tenir à jour : l'élément natif annonce déjà son état (replié/déplié), répond au
clavier (Entrée, Espace), et **fonctionne sans JS**. Le script ajouté n'est qu'un confort : Échap
referme et rend le focus, un clic à l'extérieur referme, un clic sur un lien referme, et au-delà de
980 px le panneau se referme de lui-même.

Les liens sont **copiés tels quels** depuis la nav existante : les bascules FR/EN déjà en place
(`.fr-only` / `.en-only`) continuent de fonctionner dessus sans une ligne de plus.

Ce que le script touche, dans chaque page : un `<details class="mnav">` avant la fermeture du
`.wrap` de l'en-tête, un bloc CSS avant le premier `</style>`, trois `<link>` d'icônes avant `</head>`,
et huit lignes de JS avant `</body>`. Il est **idempotent** : une page déjà traitée est laissée telle
quelle, et `--check` sort en 1 s'il reste une page à traiter.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent / "previews" / "dmoptic"
BRAND = "DM OPTIQUE SARL"

ICONS = """<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
"""

CSS = """/* 23/10 — menu mobile : sous 980 px la nav disparaît, le <details> la remplace (aucun JS requis) */
.mnav{display:none}
@media (max-width:979px){
  .mnav{display:block}
  .mnav>summary{list-style:none;width:44px;height:44px;display:grid;place-items:center;cursor:pointer;
    border:1px solid var(--line);border-radius:12px;background:var(--card)}
  .mnav>summary::-webkit-details-marker{display:none}
  .mnav>summary::before{content:"";width:20px;height:2px;background:var(--ink);
    box-shadow:0 -6px 0 var(--ink),0 6px 0 var(--ink)}
  .mnav[open]>summary{background:var(--brand-tint);border-color:var(--brand)}
  .mnav-panel{position:absolute;left:12px;right:12px;top:calc(100% + 4px);z-index:40;display:flex;
    flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:var(--r);
    box-shadow:0 18px 40px rgba(12,21,36,.18);padding:6px}
  .mnav-panel a{padding:13px 14px;border-radius:10px;text-decoration:none;color:var(--ink);
    font-weight:600;font-size:var(--fs-base)}
  .mnav-panel a+a{border-top:1px solid var(--line-2)}
  .mnav-panel a:focus-visible{outline:3px solid var(--brand);outline-offset:-3px}
}
"""

JS = """<script>
/* 23/10 — confort du menu mobile (le <details> marche déjà sans ce script) */
(function(){
  var d=document.querySelector('.mnav'); if(!d) return;
  function close(focus){ if(!d.open) return; d.open=false; if(focus) d.querySelector('summary').focus(); }
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') close(true); });
  document.addEventListener('click',function(e){ if(d.open && !d.contains(e.target)) close(false); });
  d.addEventListener('click',function(e){ var a=e.target.closest && e.target.closest('a'); if(a) close(false); });
  window.addEventListener('resize',function(){ if(window.innerWidth>=980) close(false); });
})();
</script>
"""


def nav_links(html: str) -> str | None:
    m = re.search(r'<nav class="nav"[^>]*>(.*?)</nav>', html, re.S)
    return m.group(1).strip() if m else None


def patch(html: str) -> tuple[str, list[str]]:
    """Retourne (html patché, liste de ce qui manquait)."""
    missing = []
    if 'class="mnav"' not in html:
        links = nav_links(html)
        if links is None:
            missing.append("nav absente")
        else:
            details = ('<details class="mnav">\n      <summary aria-label="Menu"></summary>\n'
                       '      <nav class="mnav-panel" aria-label="Sections (menu)">\n        '
                       + links + '\n      </nav>\n    </details>\n    ')
            i = html.index("</header>")
            j = html.rindex("</div>", 0, i)          # fermeture du .wrap
            html = html[:j] + details + html[j:]
            missing.append("menu")
    if ".mnav>summary" not in html:
        i = html.index("</style>")
        html = html[:i] + CSS + html[i:]
        missing.append("css")
    if 'rel="icon"' not in html:
        i = html.index("</head>")
        html = html[:i] + ICONS + html[i:]
        missing.append("icônes")
    if "confort du menu mobile" not in html:
        i = html.index("</body>")
        html = html[:i] + JS + html[i:]
        missing.append("js")
    return html, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    pages = sorted(SITE.rglob("*.html"))
    todo = []
    for page in pages:
        html = page.read_text(encoding="utf-8")
        if 'class="mnav"' in html and 'rel="icon"' in html and ".mnav>summary" in html:
            continue
        todo.append(page)
        if not args.check:
            new, missing = patch(html)
            if "nav absente" in missing:
                print(f"  ⚠ {page.relative_to(SITE)} : pas de nav, ignorée")
                continue
            page.write_text(new, encoding="utf-8")

    if args.check:
        print(f"{len(pages)} page(s) · {len(todo)} à traiter")
        for p in todo[:8]:
            print(f"  · {p.relative_to(SITE)}")
        return 1 if todo else 0

    print(f"{len(pages)} page(s) · {len(todo)} traitée(s) · {len(pages) - len(todo)} déjà à jour")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
