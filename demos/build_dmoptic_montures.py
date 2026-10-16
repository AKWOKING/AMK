#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIC — page catalogue /montures (scaffold, 15/10/2026).

Lit `clients/dm-optic/site/frames.json` (une liste vide au 15/10 : aucune monture
n'a encore de nom ni de photo fournis par le client) et écrit
`hosting/previews/dmoptic/montures/index.html`.

Règles appliquées (ruling King 08/10, Option B et SPEC-PAGES-v1 §2 / §6) :
- aucun prix affiché ; aucune image inventée ; aucune carte sans nom fourni par le client ;
- catalogue vide -> état vide « Le catalogue arrive » + CTA WhatsApp, pas de faux stock ;
- barre de recherche et pastilles de filtres cachées tant qu'aucune carte n'existe ;
- la page n'est liée depuis l'accueil qu'à partir du premier vrai lot de montures (non fait).
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "hosting/previews/dmoptic/index.html"
FRAMES = ROOT / "clients/dm-optic/site/frames.json"
OUT = ROOT / "hosting/previews/dmoptic/montures/index.html"
WA = "https://wa.me/237656122239?text="

def wa(msg):
    return WA + quote(msg, safe="")

def esc(s):
    return html.escape(str(s), quote=True)

def main():
    src = SRC.read_text(encoding="utf-8")
    head_end = src.index("</head>") + len("</head>")
    head = src[:head_end]
    head = head.replace("<title>", "<title>", 1)
    head = re.sub(r"<title>.*?</title>", "<title>Toutes nos montures — DM OPTIQUE SARL</title>", head, count=1, flags=re.S)
    # 15/10 — l'adresse vient de l'accueil construit (même source que `--url`), jamais écrite en dur.
    m = re.search(r'<link rel="canonical" href="([^"]+)">', src)
    if m:
        base = m.group(1).rstrip("/") + "/montures/"
        head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % base, head)
        head = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % base, head)
    else:
        # accueil sans adresse (pas encore construit avec --url) : pas de canonique inventée
        head = re.sub(r'<link rel="canonical" href="[^"]*">\n?', '', head)

    header = re.search(r'<header class="site">.*?</header>', src, re.S).group(0)
    footer = re.search(r'<footer class="site">.*?</footer>', src, re.S).group(0)
    # ancres de l'accueil -> retour à l'accueil
    header = re.sub(r'href="#(?!top)([^"]+)"', r'href="/#\1"', header)
    footer = re.sub(r'href="#(?!top)([^"]+)"', r'href="/#\1"', footer)
    header = header.replace('href="#top"', 'href="/"')
    footer = footer.replace('href="#top"', 'href="/"')
    scripts = re.findall(r"<script>/\* ── (?:LES DEUX|LE MOUVEMENT).*?</script>", src, re.S)

    frames = json.loads(FRAMES.read_text(encoding="utf-8"))
    if not frames:
        body_main = f'''<main id="main">
  <section class="wrap" style="padding:72px 0">
    <h1><span class="fr-only" lang="fr">Toutes nos montures</span><span class="en-only" lang="en">All our frames</span></h1>
    <p class="empty" role="status">
      <span class="fr-only" lang="fr">Le catalogue arrive — écrivez-nous, on vous montre les montures en message.</span>
      <span class="en-only" lang="en">The catalogue is coming — write to us and we will show you the frames by message.</span>
    </p>
    <p><a class="btn btn-wa wa" href="{esc(wa('Bonjour DM OPTIQUE SARL, je voudrais voir les montures disponibles.'))}"><span class="fr-only" lang="fr">Écrire sur WhatsApp</span><span class="en-only" lang="en">Write on WhatsApp</span></a></p>
  </section>
</main>'''
    else:
        cards = []
        for f in frames:
            name = f["nom"]
            msg = f"Bonjour DM OPTIQUE SARL, je suis intéressé par la monture « {name} ». Est-elle disponible ?"
            img = f'<img src="{esc(f["photo"])}" alt="{esc(name)}" loading="lazy" width="800" height="600">' if f.get("photo") else ""
            cards.append(f'''<li class="frame">
      {img}
      <h2>{esc(name)}</h2>
      <p>{esc(f.get("phrase", ""))}</p>
      <a class="btn btn-wa wa" href="{esc(wa(msg))}"><span class="fr-only" lang="fr">Demander cette monture</span><span class="en-only" lang="en">Ask about this frame</span></a>
    </li>''')
        body_main = f'''<main id="main">
  <section class="wrap" style="padding:72px 0">
    <h1><span class="fr-only" lang="fr">Toutes nos montures</span><span class="en-only" lang="en">All our frames</span></h1>
    <ul class="frames">
    {chr(10).join(cards)}
    </ul>
  </section>
</main>'''

    page = f'''{head}
<body>
<a class="skiplink" href="#main"><span class="fr-only" lang="fr">Aller au contenu</span><span class="en-only" lang="en">Skip to content</span></a>
<p id="say" class="sr" role="status" aria-live="polite"></p>

{header}

{body_main}

{footer}
{chr(10).join(scripts)}
</body>
</html>
'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"ok: {OUT.relative_to(ROOT)} ({len(frames)} montures)")

if __name__ == "__main__":
    main()
