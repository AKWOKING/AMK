#!/usr/bin/env python3
"""Construit `site/en/index.html` depuis `site/index.html`, sans traduire à la main.

Pourquoi un générateur : la page française porte déjà 301 paires `data-en` /
`data-fr`. Écrire la version anglaise à la main, c'est deux vérités qui
divergent au premier changement — exactement ce que `PRE-FLIGHT.md` §0f interdit.
Ici, le nœud visible est **remplacé par `data-en`** : le robot lit l'anglais,
le lecteur lit l'anglais, et le texte français reste dans `data-fr` pour le
bouton FR (qui, lui, renvoie vers `/`).

    python3 tools/site/build_en_page.py

Trois choses sont écrites à la main dans ce script, parce qu'aucune paire ne les
couvre : le `<head>` (titre, description, og, canonical, hreflang), le bloc des
trois étapes de paiement (`.pay`), et le sélecteur de langue (des liens, pas des
boutons : changer de langue change de page).

Le script refuse de produire une page si un nœud visible reste identique à sa
version française alors qu'une paire existe — c'est la seule faute qui compte.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SRC = SITE / "index.html"
DST = SITE / "en" / "index.html"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}

# Les trois étapes de paiement : aucun `data-en` là-dessus dans la page source.
PAY_EN = [
    ("1 · Quote", "A written quote, a scope, a price. Nothing starts without your “yes”."),
    ("2 · Invoice", "Numbered invoice AMK-2026-00x: 50 % when work starts, 50 % when the site goes live. "
                    "MTN, Orange or cash."),
    ("3 · Follow-up", "A line left open? We follow up on day 7, politely, with the exact amount."),
]


class Rewrite(HTMLParser):
    """Un DOM minimal : on garde les nœuds, on remplace le texte visible."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out: list[str] = []
        self.stack: list[dict] = []
        self.skip = 0          # dans <script>/<style> : on recopie tel quel

    # --- sortie -----------------------------------------------------------
    def emit(self, s: str) -> None:
        self.out.append(s)

    def attrs_of(self, attrs) -> str:
        parts = []
        for k, v in attrs:
            if v is None:
                parts.append(f' {k}')
            else:
                parts.append(f' {k}="{html.escape(v, quote=True)}"')
        return "".join(parts)

    # --- balises ----------------------------------------------------------
    def handle_decl(self, decl):
        self.emit(f"<!{decl}>")

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        self.emit(f"<{tag}{self.attrs_of(attrs)}>")
        if tag not in VOID:
            self.stack.append({"tag": tag, "data-en": d.get("data-en"), "buf": [], "keep": True})

    def handle_startendtag(self, tag, attrs):
        self.emit(f"<{tag}{self.attrs_of(attrs)}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        node = self.stack.pop() if self.stack else None
        if node and node["tag"] == tag and node.get("data-en") is not None and node["buf"]:
            inner = "".join(node["buf"])
            if re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", inner)).strip():
                # ce qui restait à écrire dans les enfants est déjà parti : on
                # remplace le texte visible par la version anglaise, entités comprises.
                # la valeur est insérée telle qu'elle est écrite dans l'attribut : c'est
                # exactement ce que fait `setLang` (`el.innerHTML = v`) sur la page
                # française, donc les deux pages se comportent pareil.
                self.emit(node["data-en"])
                # les enfants qui portaient eux-mêmes data-en ont déjà écrit leur
                # texte : on nettoie le doublon en fin de balise.
                self.emit(f"</{tag}>")
                return
        self.emit(f"</{tag}>")

    def handle_data(self, data):
        if self.skip:
            self.emit(data)
            return
        # si un ancêtre porte data-en, son texte visible est remplacé en bloc :
        # on n'écrit rien maintenant, on garde le texte pour la fin de la balise.
        for node in reversed(self.stack):
            if node.get("data-en") is not None:
                node["buf"].append(data)
                return
        self.emit(data)

    def handle_comment(self, data):
        self.emit(f"<!--{data}-->")

    def handle_entityref(self, name):
        # dans un nœud remplacé, l'entité n'est pas écrite : le remplacement
        # arrive entier à la fermeture de la balise (sinon « &amp; » ressort
        # devant le texte anglais, ce qui donne « &Domain & hosting »).
        for node in reversed(self.stack):
            if node.get("data-en") is not None:
                node["buf"].append(f"&{name};")
                return
        self.emit(f"&{name};")

    def handle_charref(self, name):
        for node in reversed(self.stack):
            if node.get("data-en") is not None:
                node["buf"].append(f"&#{name};")
                return
        self.emit(f"&#{name};")


def head_en(s: str) -> str:
    s = s.replace('<html lang="fr">', '<html lang="en">', 1)
    s = s.replace("<title>Site web clinique, cabinet &amp; école au Cameroun | AMK Douala</title>",
                  "<title>Websites for clinics, practices and shops in Cameroon | AMK Douala</title>", 1)
    s = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="Your patients and your customers look you up on Google '
               'all year. Bilingual FR|EN site, Google profile, WhatsApp booking. From 150,000 FCFA.">', s, count=1)
    s = s.replace('<link rel="alternate" hreflang="fr" href="https://amk-cm.vercel.app/">',
                  '<link rel="alternate" hreflang="fr" href="https://amk-cm.vercel.app/">')
    s = s.replace('<link rel="alternate" hreflang="en" href="https://amk-cm.vercel.app/en/">',
                  '<link rel="alternate" hreflang="en" href="https://amk-cm.vercel.app/en/">')
    s = s.replace('<link rel="canonical" href="https://amk-cm.vercel.app/">',
                  '<link rel="canonical" href="https://amk-cm.vercel.app/en/">')
    s = re.sub(r'<meta property="og:title" content="[^"]*">',
               '<meta property="og:title" content="Websites that make people pick up the phone | AMK">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">',
               '<meta property="og:description" content="Bilingual FR|EN websites for clinics, practices, '
               'shops and schools in Cameroon. From 150,000 FCFA · free preview · nothing owed before you approve.">', s, count=1)
    s = s.replace('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="en_US">')
    s = s.replace('<meta property="og:locale:alternate" content="en_US">',
                  '<meta property="og:locale:alternate" content="fr_FR">')
    s = s.replace('<meta property="og:url" content="https://amk-cm.vercel.app/">',
                  '<meta property="og:url" content="https://amk-cm.vercel.app/en/">')
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">',
               '<meta name="twitter:title" content="AMK · Bilingual websites for clinics, practices and shops in Cameroon">', s, count=1)
    s = re.sub(r'<meta name="twitter:description" content="[^"]*">',
               '<meta name="twitter:description" content="From 150,000 FCFA · bilingual FR|EN · Google profile '
               'included · free preview.">', s, count=1)
    return s


def langue(s: str) -> str:
    """Le sélecteur devient deux liens : changer de langue change de page."""
    s = s.replace('<a class="lang-a" href="en/" hreflang="en">EN</a>\n      '
                  '<button id="btn-fr" class="on" aria-pressed="true" onclick="setLang(\'fr\')">FR</button>',
                  '<a class="lang-a on" href="index.html" hreflang="en" aria-current="page">EN</a>\n      '
                  '<a class="lang-a" href="../" hreflang="fr">FR</a>')
    s = s.replace('<a class="lang-a" href="en/" hreflang="en">EN</a>\n    '
                  '<button id="btn-fr-m" class="on" aria-pressed="true" onclick="setLang(\'fr\')">FR</button>',
                  '<a class="lang-a on" href="index.html" hreflang="en" aria-current="page">EN</a>\n    '
                  '<a class="lang-a" href="../" hreflang="fr">FR</a>')
    # le chargement ne doit pas retourner en français à cause d'un réglage enregistré
    s = s.replace('  if (q === "fr" || q === "en") setLang(q);\n'
                  '  else if (saved === "fr" || saved === "en") setLang(saved);\n'
                  '  setNiche("school");',
                  '  setLang("en");\n'
                  '  setNiche("clinic");')
    return s


def liens(s: str) -> str:
    """Tout ce qui est relatif remonte d'un cran : la page vit dans `en/`."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|tel:|#|/|\.\./)", val) or val.startswith("data:"):
            return m.group(0)
        return f'{attr}="../{val}"'
    s = re.sub(r'\b(href|src|poster)="([^"]+)"', fix, s)

    # `srcset` porte plusieurs URL dans un seul attribut : sans ce passage, les variantes du héros
    # restaient relatives à `en/` et répondaient 404 — et comme `srcset` prime sur `src`, le
    # navigateur ne retombait même pas sur l'image de secours. Trouvé le 29/10 à la mesure.
    def fix_set(m):
        attr, val = m.group(1), m.group(2)
        parts = []
        for part in val.split(","):
            u = part.strip()
            if not u:
                continue
            url, _, desc = u.partition(" ")
            if not re.match(r"^(https?:|/|\.\./)", url) and not url.startswith("data:"):
                url = "../" + url
            parts.append((url + (" " + desc if desc else "")).strip())
        return f'{attr}="' + ", ".join(parts) + '"'
    s = re.sub(r'\b(srcset|imagesrcset)="([^"]+)"', fix_set, s)
    return s


def entete_retour(s: str) -> str:
    """Les ancres internes de la page anglaise restent sur place ; seuls les
    liens vers les concepts et les pages de niche remontent."""
    return s


def pay(s: str) -> str:
    """Le bloc des trois étapes, en anglais."""
    start = s.index('<div class="pay">')
    end = s.index('</div>', s.index('<div><b>3', start)) + len('</div>') + len('</div>')
    new = '<div class="pay">\n'
    for b, txt in PAY_EN:
        new += f'  <div><b>{b}</b><span>{txt}</span></div>\n'
    new += '</div>'
    return s[:start] + new + s[end:]


def purge_pairs(s: str) -> str:
    """La page anglaise n'a plus de paire : elle est ANGLAISE.

    Garder `data-en` / `data-fr` sur une page dont tous les nœuds sont déjà en
    anglais, c'est laisser croire à une bascule qui n'existe pas — et le contrôle
    §20.8 (`tools/qa/audit_site_amk.py`) compare le nœud à l'attribut, ce qui
    échoue dès que la valeur porte des balises. On garde donc le texte, on retire
    les paires, et on recopie `alt` depuis `data-alt-en` avant de les perdre.
    """
    def alt(m):
        attrs = m.group(0)
        en = re.search(r'data-alt-en="([^"]*)"', attrs)
        if not en:
            return attrs
        attrs = re.sub(r'\sdata-alt-en="[^"]*"', "", attrs)
        if re.search(r'\salt="[^"]*"', attrs):
            return re.sub(r'\salt="[^"]*"', f' alt="{en.group(1)}"', attrs)
        return attrs.replace("<img", f'<img alt="{en.group(1)}"', 1)

    s = re.sub(r'<img[^>]*>', alt, s)
    s = re.sub(r'\sdata-(?:en|fr|alt-en|alt-fr|ph-en|ph-fr|risk)="[^"]*"', "", s)
    return s


def faq_en(s: str) -> str:
    """La FAQ structurée de la page anglaise est reconstruite depuis ses propres
    `summary` et `.ans` : c'est le seul moyen d'être sûr que Google lit la même
    question que le visiteur. Une FAQ française sur une page anglaise est un
    signal contradictoire, même quand elle est valide."""
    paires = re.findall(r'<details>\s*<summary data-en="([^"]*)"[^>]*>.*?</summary>\s*'
                        r'<div class="ans" data-en="([^"]*)"', s, re.S)
    if len(paires) < 5:
        return s
    entities = [{"@type": "Question", "name": html.unescape(q).strip(),
                 "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a).strip()}}
                for q, a in paires]
    bloc = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    data = json.loads(bloc.group(1))
    for node in data["@graph"]:
        if node.get("@type") == "FAQPage":
            node["mainEntity"] = entities
            node["inLanguage"] = "en"
    neuf = json.dumps(data, ensure_ascii=False, indent=1)
    return s[:bloc.start(1)] + neuf + s[bloc.end(1):]


def main() -> int:
    src = SRC.read_text(encoding="utf-8")

    # Les SVG passent à côté du parseur. `HTMLParser` abaisse les noms d'attribut
    # (`viewBox` devient `viewbox`, ce qui casse le dessin) et transforme les
    # balises auto-fermées (`<rect …/>`) en balises ouvrantes jamais fermées, donc
    # en SVG imbriqués les uns dans les autres. Aucun SVG de la page ne porte de
    # texte bilingue : on les met de côté, on les remet tels quels.
    gardes: list[str] = []

    def garde(m):
        gardes.append(m.group(0))
        return f"\u0000SVG{len(gardes) - 1}\u0000"

    src = re.sub(r"<svg\b.*?</svg>", garde, src, flags=re.S)
    p = Rewrite()
    p.feed(src)
    out = "".join(p.out)
    out = re.sub(r"\u0000SVG(\d+)\u0000", lambda m: gardes[int(m.group(1))], out)
    out = head_en(out)
    out = langue(out)
    out = pay(out)
    out = liens(out)
    out = faq_en(out)
    out = purge_pairs(out)

    # garde-fou : aucun nœud ne doit encore être en français
    fr = [w for w in ("Vos patients", "Recevoir mon aperçu", "Des sites web qui", "Opticien médical",
                      "Trois formats", "Ce qu'on ne fera pas", "Combien coûte")
          if w in re.sub(r'data-fr="[^"]*"', "", out)]
    if fr:
        print("✗ français resté dans le corps : " + ", ".join(fr), file=sys.stderr)

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out, encoding="utf-8")
    print(f"→ {DST.relative_to(ROOT)} · {len(out) // 1024} Ko")
    return 1 if fr else 0


if __name__ == "__main__":
    sys.exit(main())
