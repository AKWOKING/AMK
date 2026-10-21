#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM OPTIQUE SARL — générateur des pages v2 (architecture D3 « Le Parcours », ruling King 20/10/2026).

Lit `clients/dm-optic/site/frames.json` (v2 : 40 montures réelles, taguées sur le **visible**
seulement — catégorie, forme, couleur dominante — ruling King 19/10 « pas de noms : numéroter /
nommer par trait visible ») et l'accueil déjà construit (`hosting/previews/dmoptic/index.html`,
même tête, même en-tête, même pied, même barre mobile), puis écrit, dans `hosting/previews/dmoptic/` :

  montures/index.html                    hub catalogue (3 portes + sélection)
  montures/<categorie>/index.html       femmes · hommes · enfants (filtres Forme/Couleur + recherche)
  montures/<categorie>/<slug>/index.html  fiche par monture (galerie d'angles, faits, similaires)
  examen-de-vue/index.html               le déroulé de l'examen (mots du client, brief journal 15/10)
  le-cabinet/index.html                  le cabinet (photos réelles SANS visage — accord en attente)
  contact/index.html                     adresse complète, horaires, appel, WhatsApp, Maps
  sitemap.xml                            régénéré (pages propres seulement)

Règles appliquées :
- **Aucun prix, aucune marque, aucune mesure** (brief §4 ; les mesures ne sont pas fournies → absentes).
- Filtres = JS progressif + **fragments `#`** (jamais d'URL paramétrée indexable — Google, facettes) ;
  compteurs calculés sur les données, aucune pill à zéro résultat (SPEC §6) ; sans JS, grille complète.
- Schémas : `BreadcrumbList` partout, `ItemList` sur hub/catégories ; **jamais** `Product`/`Offer`/`price`.
- Les polices et le logo de la tête de l'accueil sont relatifs (`fonts/…`) : réécrits en absolu
  (`/fonts/…`) pour les pages nichées, sinon elles chargent dans le vide.
- CTA unique par monture : WhatsApp, message avec le nom injecté (SPEC §0), « DM OPTIQUE SARL »
  partout (ruling King 10/10). Les noms/phrases des montures restent en français (limite connue).

Usage : python3 demos/build_dmoptic.py --production && python3 demos/build_dmoptic_montures.py
"""
import html
import json
import re
import shutil
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "hosting/previews/dmoptic/index.html"
FRAMES = ROOT / "clients/dm-optic/site/frames.json"
OUTDIR = ROOT / "hosting/previews/dmoptic"
WA = "https://wa.me/237656122239?text="
TEL = "tel:+237656122239"
ADDRESS_FR = "Ndobo Mayor — Immeuble West Hotel, 1er étage, dernière porte à droite, Bonabéri, Douala"
ADDRESS_EN = "Ndobo Mayor — West Hotel building, first floor, last door on the right, Bonaberi, Douala"
HOURS_FR = "Lundi – Samedi · Examen de vue : 8h30 – 13h00 · Autres besoins : 8h30 – 17h30"
HOURS_EN = "Monday – Saturday · Eye exam: 8:30–13:00 · Other needs: 8:30–17:30"
# place_id obtenu du cabinet lui-même (Google Maps Platform > Quick Builder, capture King 21/10) :
# c'est l'identité canonique de la fiche — le lien ouvre LA fiche, pas une liste de résultats.
PLACE_ID = "ChIJjdfYfQwXYRARAdi9mPLHGjY"
MAPS = ("https://www.google.com/maps/search/?api=1&query=" + quote("DM OPTIQUE SARL")
        + "&query_place_id=" + PLACE_ID)

CATS = {
    "femmes": ("Femmes", "Women", "femmes"),
    "hommes": ("Hommes", "Men", "hommes"),
    "enfants": ("Enfants", "Children", "enfants"),
}
CAT_WA = {
    "femmes": ("Bonjour DM OPTIQUE SARL, je suis intéressé par vos montures pour femmes. Quelles montures avez-vous disponibles ?",
               "Hello DM OPTIQUE SARL, I am interested in your women's frames. Which frames do you have available?"),
    "hommes": ("Bonjour DM OPTIQUE SARL, je suis intéressé par vos montures pour hommes. Quelles montures avez-vous disponibles ?",
               "Hello DM OPTIQUE SARL, I am interested in your men's frames. Which frames do you have available?"),
    "enfants": ("Bonjour DM OPTIQUE SARL, je suis intéressé par vos lunettes pour enfants. Quelles montures avez-vous disponibles ?",
                "Hello DM OPTIQUE SARL, I am interested in your children's glasses. Which frames do you have available?"),
}
EXAM_WA = ("Bonjour DM OPTIQUE SARL, je voudrais prendre un rendez-vous pour un examen de la vue.",
           "Hello DM OPTIQUE SARL, I would like to book an eye examination.")
VISIT_WA = ("Bonjour DM OPTIQUE SARL, je voudrais passer vous voir.",
            "Hello DM OPTIQUE SARL, I would like to come and see you.")
HUB_WA = ("Bonjour DM OPTIQUE SARL, je cherche une monture. Quelles montures avez-vous disponibles ?",
          "Hello DM OPTIQUE SARL, I am looking for a frame. Which frames do you have available?")
# En-têtes hôte prudents pour Cloudflare Pages (le fichier _headers n'est pas servi comme asset).
# Pas de CSP à ce stade : le site est en CSS/JS inline, une politique stricte se teste séparément.
HEADERS = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()
"""

V2_CSS = """
/* ── Pages v2 (D3, 20/10) : même identité, profondeur en plus ── */
.v2-main section{padding-top:44px;padding-bottom:44px}
.v2-crumbs{font:500 var(--fs-xs)/1.7 var(--f-m);color:var(--ink-3);margin:0 0 14px}
.v2-crumbs a{color:var(--brand);text-decoration:none;border-bottom:1px solid transparent}
.v2-crumbs a:hover{border-color:currentColor}
.v2-grid{display:grid;gap:16px;list-style:none;margin:26px 0 0;padding:0}
@media(min-width:640px){.v2-grid{grid-template-columns:1fr 1fr}}
@media(min-width:1024px){.v2-grid{grid-template-columns:1fr 1fr 1fr}}
.v2-card{background:var(--card);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;display:flex}
.v2-card article{display:flex;flex-direction:column;flex:1}
.v2-card img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#F6EBE0;border-bottom:1px solid var(--line)}
.v2-card .v2-body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:8px;flex:1}
.v2-card h2,.v2-card h3{margin:0;font-size:1.05rem}
.v2-card h2 a,.v2-card h3 a{color:var(--ink);text-decoration:none}
.v2-card h2 a:hover,.v2-card h3 a:hover{color:var(--brand)}
.v2-card p{margin:0;color:var(--ink-2);font-size:var(--fs-sm)}
.v2-tags{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0;padding:0}
.v2-tags li{font:500 var(--fs-xs)/1 var(--f-m);color:var(--ink-2);background:var(--card-2);border:1px solid var(--line);border-radius:999px;padding:6px 9px}
.v2-card .v2-actions{margin-top:auto;padding-top:10px;display:grid;gap:8px}
.v2-card .btn{min-height:48px;width:100%}
.v2-card[hidden],.v2-empty[hidden],.v2-chips[hidden]{display:none!important}
.v2-doors{display:grid;gap:16px;margin-top:26px}
@media(min-width:760px){.v2-doors{grid-template-columns:1fr 1fr 1fr}}
.v2-door{background:var(--card);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;text-decoration:none;color:var(--ink);display:flex;flex-direction:column}
.v2-door img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#F6EBE0}
.v2-door .v2-body{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px}
.v2-door h2{margin:0;font-size:1.15rem}
.v2-door p{margin:0;color:var(--ink-2);font-size:var(--fs-sm)}
.v2-door .v2-go{font:600 var(--fs-sm)/1 var(--f-b);color:var(--brand)}
.v2-filters{margin-top:22px}
.v2-toolbar{position:sticky;top:0;z-index:40;display:flex;flex-wrap:wrap;gap:10px;align-items:end;background:var(--paper);padding:12px 0;border-bottom:1px solid var(--line)}
.v2-search{display:flex;flex-direction:column;gap:6px;flex:1 1 220px;font:500 var(--fs-label)/1 var(--f-m);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.v2-search input{min-height:48px;border:1px solid var(--line-strong);border-radius:var(--r);padding:0 14px;font:400 1rem/1 var(--f-b);background:var(--card);color:var(--ink)}
.v2-count{font:600 var(--fs-sm)/48px var(--f-b);color:var(--ink);margin:0}
.v2-filter-toggle{display:none}
@media(max-width:779px){html.js .v2-filter-toggle{display:inline-flex}html.js .v2-filters-panel{display:none}html.js .v2-filters-panel.is-open{display:block}}
@media(min-width:780px){.v2-show{display:none}}
@media(max-width:779px){html.js .v2-filters-panel.is-open{animation:v2-panel-in .18s var(--ease)}}
@keyframes v2-panel-in{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){html.js .v2-filters-panel.is-open{animation:none}}
.v2-toolbar .btn{min-height:48px}
.v2-group{border:0;margin:16px 0 0;padding:0}
.v2-group legend{font:500 var(--fs-label)/1.7 var(--f-m);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);padding:0}
.v2-pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.v2-pill{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 12px;border:1px solid var(--line-strong);border-radius:999px;background:var(--card);color:var(--ink);font:600 var(--fs-sm)/1 var(--f-b);cursor:pointer}
.v2-pill input{width:18px;height:18px;accent-color:var(--brand)}
.v2-pill .v2-n{font:500 var(--fs-xs)/1 var(--f-m);color:var(--ink-3)}
.v2-pill.is-on{background:var(--brand);border-color:var(--brand);color:#fff}
.v2-pill.is-on .v2-n{color:#fff}
.v2-pill:focus-within{outline:3px solid var(--brand);outline-offset:2px}
.v2-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.v2-chip{min-height:40px;border:1px solid var(--brand);border-radius:999px;background:var(--brand-tint);color:var(--brand-2);font:600 var(--fs-sm)/1 var(--f-b);padding:8px 12px;cursor:pointer}
.v2-empty{margin-top:26px;border:1px solid var(--line);border-radius:var(--r-lg);background:var(--card);padding:20px}
.v2-facts{display:grid;gap:0;margin-top:22px;border-top:1px solid var(--line)}
.v2-facts div{display:flex;justify-content:space-between;gap:14px;padding:13px 0;border-bottom:1px solid var(--line)}
.v2-facts dt{font:500 var(--fs-label)/1.7 var(--f-m);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.v2-facts dd{margin:0;font-weight:600;font-size:var(--fs-sm);text-align:right}
.v2-gallery{display:grid;gap:12px;margin-top:22px}
@media(min-width:760px){.v2-gallery{grid-template-columns:1fr 1fr 1fr}.v2-gallery figure:first-child{grid-column:1/-1}}
.v2-gallery figure{margin:0}
.v2-gallery img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#F6EBE0;border:1px solid var(--line);border-radius:var(--r-lg)}
.v2-fiche{display:grid;gap:22px;margin-top:22px;align-items:start}
.v2-fiche .v2-gallery{margin-top:0}
.v2-fiche-aside .v2-facts{margin-top:0}
.v2-cta-mobile{display:none}
@media(max-width:979px){.v2-cta-mobile{display:block}.v2-cta-mobile .btn{width:100%}}
@media(min-width:760px){.v2-cta-mobile{grid-column:1/-1}}
@media(min-width:980px){.v2-fiche{grid-template-columns:55fr 45fr}}
@media(max-width:779px){html.js .v2-card.rv{opacity:1;transform:none;transition:none}}
.v2-photos{display:grid;gap:16px;margin-top:26px}
@media(min-width:760px){.v2-photos{grid-template-columns:1fr 1fr}}
.v2-photos figure{margin:0}
.v2-photos img{display:block;width:100%;height:auto;border-radius:var(--r-lg);border:1px solid var(--line)}
.v2-photos figcaption{margin-top:10px;font:500 var(--fs-xs)/1.6 var(--f-m);color:var(--ink-3)}
.v2-photo{margin:26px 0 0}
.v2-photo img{display:block;width:100%;height:auto;border-radius:var(--r-lg);border:1px solid var(--line)}
.v2-photo figcaption{margin-top:10px;font:500 var(--fs-xs)/1.6 var(--f-m);color:var(--ink-3)}
.v2-steps{counter-reset:v2step;list-style:none;margin:26px 0 0;padding:0;display:grid;gap:14px}
@media(min-width:760px){.v2-steps{grid-template-columns:1fr 1fr}}
.v2-steps li{background:var(--card);border:1px solid var(--line);border-radius:var(--r-lg);padding:18px}
.v2-steps .n{font:500 var(--fs-label)/1 var(--f-m);letter-spacing:.12em;color:var(--brand)}
.v2-steps h2{margin:.5rem 0 0;font-size:var(--fs-h3);line-height:1.25}
.v2-steps p{margin:.45rem 0 0;color:var(--ink-2);font-size:var(--fs-sm)}
"""

FILTER_JS = """<script>/* Filtres du catalogue v2 : OU dans un groupe, ET entre groupes, état en fragment #. */
(function(){try{
  var form=document.querySelector('.v2-filters'); if(!form) return;
  var grid=document.querySelector('.v2-grid');
  var cards=[].slice.call(grid.querySelectorAll('.v2-card'));
  var q=form.querySelector('.v2-q');
  var boxes=[].slice.call(form.querySelectorAll('input[type="checkbox"][data-group]'));
  var count=document.querySelector('.v2-count'), chips=document.querySelector('.v2-chips');
  var empty=document.querySelector('.v2-empty'), reset=form.querySelector('.v2-reset'), show=form.querySelector('.v2-show');
  var toggle=form.querySelector('.v2-filter-toggle'), panel=form.querySelector('.v2-filters-panel');
  function setPanel(open){if(!panel||!toggle)return;panel.classList.toggle('is-open',open);toggle.setAttribute('aria-expanded',open?'true':'false');}
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
  function state(){var st={forme:[],couleur:[],q:norm(q.value).trim()};boxes.forEach(function(b){if(b.checked)st[b.getAttribute('data-group')].push(b.value);});return st;}
  function renderChips(st){
    chips.innerHTML='';
    function chip(label,fn){var b=document.createElement('button');b.type='button';b.className='v2-chip';b.textContent=label+' \\u00d7';b.addEventListener('click',fn);chips.appendChild(b);}
    boxes.forEach(function(b){if(b.checked){chip(b.getAttribute('data-label'),function(){b.checked=false;apply();});}});
    if(st.q){chip('\\u00ab '+q.value.trim()+' \\u00bb',function(){q.value='';apply();});}
    chips.hidden=!chips.children.length;
  }
  function apply(writeHash){
    var st=state(), n=0;
    cards.forEach(function(c){
      var ok=(!st.forme.length||st.forme.indexOf(c.getAttribute('data-forme'))>-1)
           &&(!st.couleur.length||st.couleur.indexOf(c.getAttribute('data-couleur'))>-1)
           &&(!st.q||norm(c.getAttribute('data-name')).indexOf(st.q)>-1);
      c.hidden=!ok; if(ok)n++;
    });
    count.textContent=n+(n>1?' montures':' monture');
    if(show)show.textContent='Afficher '+n+(n>1?' montures':' monture');
    empty.hidden=(n!==0);
    boxes.forEach(function(b){var l=b.closest?b.closest('label'):null; if(l)l.classList.toggle('is-on',b.checked);});
    renderChips(st);
    if(writeHash!==false){
      var p=[];
      if(st.forme.length)p.push('forme='+st.forme.join(','));
      if(st.couleur.length)p.push('couleur='+st.couleur.join(','));
      if(st.q)p.push('q='+encodeURIComponent(q.value.trim()));
      history.replaceState(null,'',p.length?('#'+p.join('&')):(location.pathname+location.search));
    }
  }
  function fromHash(){
    if(!location.hash) return;
    location.hash.slice(1).split('&').forEach(function(pair){
      var kv=pair.split('='); if(kv.length<2) return;
      var k=kv[0], v=decodeURIComponent(kv[1]);
      if(k==='q'){q.value=v; return;}
      v.split(',').forEach(function(val){boxes.forEach(function(b){if(b.getAttribute('data-group')===k&&b.value===val)b.checked=true;});});
    });
  }
  form.addEventListener('input',function(){apply();});
  form.addEventListener('submit',function(e){e.preventDefault();apply();});
  if(reset)reset.addEventListener('click',function(){q.value='';boxes.forEach(function(b){b.checked=false;});apply();});
  if(toggle)toggle.addEventListener('click',function(){setPanel(!(panel&&panel.classList.contains('is-open')));});
  if(show)show.addEventListener('click',function(){setPanel(false);grid.scrollIntoView();});
  fromHash(); apply(false);
}catch(e){}})();
</script>"""


def esc(s):
    return html.escape(str(s), quote=True)


def slugify(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "monture"


def wa(msg):
    return WA + quote(msg, safe="")


def B(fr, en):
    return (f'<span class="fr-only" lang="fr">{esc(fr)}</span>'
            f'<span class="en-only" lang="en">{esc(en)}</span>')


def wa_btn(fr_msg, en_msg, fr_label, en_label, cls="btn btn-wa wa"):
    return (f'<a class="{cls}" data-fr="{esc(fr_msg)}" data-en="{esc(en_msg)}" '
            f'href="{esc(wa(fr_msg))}">{B(fr_label, en_label)}</a>')


def frame_url(f):
    return f"/montures/{f['categorie']}/{f['slug']}/"


def frame_msg(f):
    return (f"Bonjour DM OPTIQUE SARL, je suis intéressé par la monture « {f['nom']} ». Est-elle disponible ?",
            f"Hello DM OPTIQUE SARL, I am interested in frame \"{f['nom']}\". Is it available?")


def card(f, level=2):
    fr_msg, en_msg = frame_msg(f)
    img = (f'<img src="{esc(f["photos"][0])}" alt="{esc(f["nom"])}" loading="lazy" '
           f'width="1600" height="1200">') if f.get("photos") else ""
    return f'''<li class="v2-card rv" data-forme="{esc(slugify(f["forme"]))}" data-couleur="{esc(slugify(f["couleur"]))}" data-name="{esc(f["nom"] + " " + f["forme"] + " " + f["couleur"])}">
    <article>
      {img}
      <div class="v2-body">
        <h{level}><a href="{esc(frame_url(f))}">{esc(f["nom"])}</a></h{level}>
        <ul class="v2-tags"><li>{esc(f["forme"])}</li><li>{esc(f["couleur"])}</li></ul>
        <p>{esc(f["phrase"])}</p>
        <div class="v2-actions">
          <a class="btn" href="{esc(frame_url(f))}">{B("Voir la fiche", "See the frame")}</a>
          {wa_btn(fr_msg, en_msg, "Demander cette monture", "Ask about this frame")}
        </div>
      </div>
    </article>
  </li>'''


def mini_card(f):
    img = (f'<img src="{esc(f["photos"][0])}" alt="{esc(f["nom"])}" loading="lazy" '
           f'width="1600" height="1200">') if f.get("photos") else ""
    return f'''<li class="v2-card rv">
    <article>
      {img}
      <div class="v2-body">
        <h3><a href="{esc(frame_url(f))}">{esc(f["nom"])}</a></h3>
        <ul class="v2-tags"><li>{esc(f["forme"])}</li><li>{esc(f["couleur"])}</li></ul>
        <div class="v2-actions"><a class="btn" href="{esc(frame_url(f))}">{B("Voir la fiche", "See the frame")}</a></div>
      </div>
    </article>
  </li>'''


class Site:
    def __init__(self, src):
        head_end = src.index("</head>") + len("</head>")
        self.head = src[:head_end]
        m = re.search(r'<link rel="canonical" href="([^"]+)">', src)
        self.base = m.group(1).rstrip("/") if m else ""
        self.header = self._chrome(re.search(r'<header class="site">.*?</header>', src, re.S).group(0))
        self.footer = self._chrome(re.search(r'<footer class="site">.*?</footer>', src, re.S).group(0))
        dock = re.search(r'<div class="dock">.*?</div>', src, re.S)
        self.dock = dock.group(0) if dock else ""
        self.scripts = re.findall(r"<script>/\* ── (?:LES DEUX|LE MOUVEMENT).*?</script>", src, re.S)
        self.paths = ["/"]

    @staticmethod
    def _chrome(block):
        block = re.sub(r'href="#(?!top)([^"]+)"', r'href="/#\1"', block)
        return block.replace('href="#top"', 'href="/"')

    def abs(self, path):
        return (self.base + path) if self.base else path

    def _head(self, path, title, desc, ld_graph, og_image, og_wh):
        if len(title) > 65 or len(desc) > 155:
            print(f"! SEO longueur : {path} titre={len(title)} desc={len(desc)}")
        head = self.head
        # Chemins relatifs de l'accueil → absolus (pages nichées).
        head = head.replace("url(fonts/", "url(/fonts/").replace("url(dm-logo.webp)", "url(/dm-logo.webp)")
        head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1, flags=re.S)

        def set_meta(attr, key, val):
            nonlocal head
            pat = rf'(<meta {attr}="{re.escape(key)}" content=")[^"]*(">)'
            if re.search(pat, head):
                head = re.sub(pat, lambda mm: mm.group(1) + esc(val) + mm.group(2), head, count=1)
            else:
                head = head.replace("</head>", f'<meta {attr}="{key}" content="{esc(val)}">\n</head>', 1)

        url = self.abs(path)
        if self.base:
            head = re.sub(r'<link rel="canonical" href="[^"]*">',
                          f'<link rel="canonical" href="{esc(url)}">', head, count=1)
            set_meta("property", "og:url", url)
        else:
            head = re.sub(r'<link rel="canonical" href="[^"]*">\n?', "", head, count=1)
        set_meta("name", "description", desc)
        set_meta("property", "og:title", title)
        set_meta("property", "og:description", desc)
        if og_image:
            set_meta("property", "og:image", self.abs(og_image[0]))
            set_meta("property", "og:image:alt", og_image[1])
            if og_wh:
                set_meta("property", "og:image:width", str(og_wh[0]))
                set_meta("property", "og:image:height", str(og_wh[1]))
        # Le schéma FAQ de l'accueil ne se recopie pas sur les autres pages ; l'entité Optician reste.
        def _filter_ld(m):
            try:
                data = json.loads(m.group(1))
                graph = data.get("@graph")
                if isinstance(graph, list):
                    data["@graph"] = [g for g in graph if g.get("@type") != "FAQPage"]
                    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"
            except Exception:
                pass
            return m.group(0)
        head = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _filter_ld, head, flags=re.S)
        extra = "<style>" + V2_CSS + "</style>\n"
        if ld_graph:
            payload = {"@context": "https://schema.org", "@graph": ld_graph}
            extra += '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + "</script>\n"
        return head.replace("</head>", extra + "</head>", 1)

    def _dock_for(self, dock_wa=None):
        dock = self.dock
        if dock_wa:
            fr_dock, en_dock = dock_wa
            def _dock_link(m):
                tag = m.group(0)
                tag = re.sub(r'data-fr="[^"]*"', f'data-fr="{esc(fr_dock)}"', tag, count=1)
                tag = re.sub(r'data-en="[^"]*"', f'data-en="{esc(en_dock)}"', tag, count=1)
                tag = re.sub(r'href="[^"]*"', f'href="{esc(wa(fr_dock))}"', tag, count=1)
                return tag
            dock = re.sub(r'<a\b[^>]*\bclass="[^"]*\bwa\b[^"]*"[^>]*>', _dock_link, dock, count=1)
        return dock

    def page(self, path, title, desc, main_html, ld_graph=None, og_image=None, og_wh=None, extra_script="", dock_wa=None):
        head = self._head(path, title, desc, ld_graph, og_image, og_wh)
        # Images du corps en relatif (profondeur de la page) : navigateur et `audit_images.py`
        # résolvent depuis le dossier de la page ; canoniques/OG/JSON-LD restent absolus.
        depth = len([p for p in path.split("/") if p])
        main_html = re.sub(r'src="/', 'src="' + "../" * depth, main_html)
        dock = self._dock_for(dock_wa)
        page = f'''{head}
<body>
<a class="skiplink" href="#main">{B("Aller au contenu", "Skip to content")}</a>
<p id="say" class="sr" role="status" aria-live="polite"></p>

{self.header}

<main id="main" class="v2-main">
{main_html}
</main>

{self.footer}
{dock}
{chr(10).join(self.scripts)}
{extra_script}
</body>
</html>
'''
        out = OUTDIR / path.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        self.paths.append(path)
        return out

    def crumbs(self, items):
        parts = []
        for label, url in items:
            parts.append(f'<a href="{esc(url)}">{label}</a>' if url else f'<span aria-current="page">{label}</span>')
        return '<nav class="v2-crumbs" aria-label="Fil d\'Ariane">' + " · ".join(parts) + "</nav>"

    def crumb_ld(self, items):
        return {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": self.abs(url)}
            for i, (name, url) in enumerate(items)]}

    def itemlist_ld(self, frames):
        return {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f["nom"], "url": self.abs(frame_url(f))}
            for i, f in enumerate(frames)]}


def main():
    src = SRC.read_text(encoding="utf-8")
    site = Site(src)
    frames = json.loads(FRAMES.read_text(encoding="utf-8"))
    by_cat = {c: [f for f in frames if f["categorie"] == c] for c in CATS}
    written = []

    # Nettoyage des anciennes pages générées (les images vivent à la racine de /montures/).
    for c in CATS:
        d = OUTDIR / "montures" / c
        if d.exists():
            shutil.rmtree(d)

    # ── Hub /montures/ ──────────────────────────────────────────────────────────
    doors = []
    for c, (fr_l, en_l, _) in CATS.items():
        rep = by_cat[c][0]
        n = len(by_cat[c])
        doors.append(f'''<a class="v2-door rv" href="/montures/{c}/">
        <img src="{esc(rep["photos"][0])}" alt="{esc(rep["nom"])}" loading="lazy" width="1600" height="1200">
        <span class="v2-body">
          <h2>{B(fr_l, en_l)}</h2>
          <p>{B(f"{n} montures à essayer au cabinet.", f"{n} frames to try at the practice.")}</p>
          <span class="v2-go">{B("Voir les montures", "See the frames")} →</span>
        </span>
      </a>''')
    selection = [by_cat["femmes"][0], by_cat["femmes"][5], by_cat["hommes"][0],
                 by_cat["hommes"][2], by_cat["enfants"][2], by_cat["enfants"][4]]
    hub_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Montures", "Frames"), None)])}
    <h1>{B("Toutes nos montures", "All our frames")}</h1>
    <p class="lede">{B("Lunettes de vue, lunettes de soleil, montures pour enfants : elles s'essayent au cabinet, sur votre visage, avec quelqu'un qui vous regarde — pas sur un écran.", "Spectacles, sunglasses, children's frames: you try them on at the practice, on your face, with someone looking at you — not on a screen.")}</p>
    <div class="v2-doors">
      {chr(10).join(doors)}
    </div>
  </section>
  <section class="wrap" aria-labelledby="h-selection">
    <h2 id="h-selection">{B("À essayer au cabinet", "To try at the practice")}</h2>
    <ul class="v2-grid">
      {chr(10).join(card(f, level=3) for f in selection)}
    </ul>
    <div class="advice">
      <div><h3>{B("La forme du visage", "Your face shape")}</h3><p>{B("Rond, ovale, carré, cœur : c'est la forme du visage qui guide la forme de la monture. C'est pour ça qu'on essaie — une photo ne dit pas tout.", "Round, oval, square, heart: your face shape guides the shape of the frame. That is why you try them on — a photo does not tell the whole story.")}</p></div>
      <div><h3>{B("La largeur, et l'appui", "Width and support")}</h3><p>{B("Une monture bien réglée ne glisse pas sur le nez et ne serre pas derrière les oreilles. Demandez le réglage, même sur des lunettes qui ne viennent pas d'ici.", "A well-adjusted frame does not slip down your nose or press behind your ears. Ask for the adjustment, even on glasses that did not come from here.")}</p></div>
      <div><h3>{B("Ce que vous en faites", "What you do with them")}</h3><p>{B("Écran toute la journée, conduite, lecture, sport, soleil : l'usage change le verre, pas seulement la monture. Dites-le en arrivant.", "Screens all day, driving, reading, sport, sun: the use changes the lens, not just the frame. Say so when you arrive.")}</p></div>
    </div>
  </section>'''
    written.append(site.page(
        "/montures/", "Toutes nos montures à Bonabéri — DM OPTIQUE SARL",
        "Montures femmes, hommes et enfants photographiées au cabinet DM OPTIQUE SARL à Bonabéri, Douala. Choisissez, puis demandez-la sur WhatsApp.",
        hub_main,
        ld_graph=[site.crumb_ld([("Accueil", "/"), ("Montures", "/montures/")]), site.itemlist_ld(frames)], dock_wa=HUB_WA))

    # ── Catégories + fiches ─────────────────────────────────────────────────────
    for c, (fr_l, en_l, fr_low) in CATS.items():
        items = by_cat[c]
        groups = []
        for group_key, fr_g, en_g in (("forme", "Forme", "Shape"), ("couleur", "Couleur", "Colour")):
            counts = Counter(f[group_key] for f in items)
            pills = []
            for label, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
                pills.append(
                    f'<label class="v2-pill"><input type="checkbox" data-group="{group_key}" '
                    f'value="{esc(slugify(label))}" data-label="{esc(label)}"> {esc(label)} '
                    f'<span class="v2-n">{n}</span></label>')
            groups.append(f'''<fieldset class="v2-group">
        <legend>{B(fr_g, en_g)}</legend>
        <div class="v2-pills">{chr(10).join(pills)}</div>
      </fieldset>''')
        fr_msg, en_msg = CAT_WA[c]
        n = len(items)
        cat_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Montures", "Frames"), "/montures/"), (B(fr_l, en_l), None)])}
    <h1>{B(f"Montures {fr_low}", f"{en_l} frames")}</h1>
    <p class="lede">{B(f"{n} montures photographiées au cabinet, à essayer sur votre visage. Touchez une fiche pour la voir sous d'autres angles, ou demandez-la directement sur WhatsApp.", f"{n} frames photographed at the practice, to try on your face. Open a frame to see other angles, or ask for it directly on WhatsApp.")}</p>
    <form class="v2-filters" role="search">
      <div class="v2-toolbar">
        <label class="v2-search">{B("Rechercher", "Search")}<input class="v2-q" type="search" name="q" placeholder="Rechercher une monture…" autocomplete="off"></label>
        <p class="v2-count" role="status" aria-live="polite">{n} montures</p>
        <button class="btn v2-filter-toggle" type="button" aria-expanded="false" aria-controls="filtres-{c}">{B("Filtrer", "Filter")}</button>
        <button class="btn v2-show" type="button">Afficher {n} montures</button>
        <button class="btn v2-reset" type="button">{B("Effacer", "Clear")}</button>
      </div>
      <div class="v2-filters-panel" id="filtres-{c}">
      {chr(10).join(groups)}
      </div>
      <div class="v2-chips" hidden></div>
    </form>
    <noscript><p class="note">{B("Les filtres demandent JavaScript ; toutes les montures sont ci-dessous.", "The filters need JavaScript; every frame is listed below.")}</p></noscript>
    <ul class="v2-grid" id="resultats">
      {chr(10).join(card(f, level=2) for f in items)}
    </ul>
    <div class="v2-empty" hidden>
      <p>{B("Aucune monture dans ce filtre pour l'instant. Écrivez-nous : on cherche pour vous.", "No frame in this filter for now. Write to us: we will look for you.")}</p>
      <div class="actions">{wa_btn(fr_msg, en_msg, "Écrire sur WhatsApp", "Write on WhatsApp")}</div>
    </div>
  </section>'''
        written.append(site.page(
            f"/montures/{c}/", f"Montures {fr_low} à Bonabéri — DM OPTIQUE SARL",
            f"{n} montures {fr_low} réelles du cabinet DM OPTIQUE SARL à Bonabéri : formes et couleurs visibles, à essayer au cabinet. Demande sur WhatsApp.",
            cat_main,
            ld_graph=[site.crumb_ld([("Accueil", "/"), ("Montures", "/montures/"), (fr_l, f"/montures/{c}/")]),
                      site.itemlist_ld(items)],
            extra_script=FILTER_JS, dock_wa=CAT_WA[c]))

        for f in items:
            fr_m, en_m = frame_msg(f)
            figs = []
            for i, p in enumerate(f["photos"]):
                loading = "" if i == 0 else ' loading="lazy"'
                figs.append(f'<figure><img src="{esc(p)}" alt="{esc(f["nom"])}" width="1600" height="1200"{loading}></figure>')
            if figs:
                figs.insert(1, f'<div class="v2-cta-mobile">{wa_btn(fr_m, en_m, "Commander sur WhatsApp", "Ask on WhatsApp")}</div>')
            sims = [g for g in items if g["code"] != f["code"] and g["forme"] == f["forme"]]
            sims += [g for g in items if g["code"] != f["code"] and g not in sims and g["couleur"] == f["couleur"]]
            sims += [g for g in items if g["code"] != f["code"] and g not in sims]
            sims = sims[:3]
            sim_block = ""
            if sims:
                sim_block = f'''<section class="wrap" aria-labelledby="h-sims">
    <h2 id="h-sims" class="rv">{B("Vous aimerez aussi", "You may also like")}</h2>
    <ul class="v2-grid">
      {chr(10).join(mini_card(g) for g in sims)}
    </ul>
  </section>'''
            fiche_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Montures", "Frames"), "/montures/"), (B(fr_l, en_l), f"/montures/{c}/"), (esc(f["nom"]), None)])}
    <h1 class="rv">{esc(f["nom"])}</h1>
    <p class="lede rv">{esc(f["phrase"])}</p>
    <div class="v2-fiche">
      <div class="v2-gallery rv">
      {chr(10).join(figs)}
      </div>
      <aside class="v2-fiche-aside rv">
    <dl class="v2-facts">
      <div><dt>{B("Catégorie", "Category")}</dt><dd>{B(fr_l, en_l)}</dd></div>
      <div><dt>{B("Forme", "Shape")}</dt><dd>{esc(f["forme"])}</dd></div>
      <div><dt>{B("Couleur dominante", "Main colour")}</dt><dd>{esc(f["couleur"])}</dd></div>
      <div><dt>{B("Référence à donner au cabinet", "Reference to give the practice")}</dt><dd>{esc(f["code"])}</dd></div>
    </dl>
    <div class="actions">
      {wa_btn(fr_m, en_m, "Commander sur WhatsApp", "Ask on WhatsApp")}
      <a class="btn" href="{TEL}">{B("Appeler le 656 122 239", "Call 656 122 239")}</a>
      <a class="btn" href="/montures/{c}/">{B(f"Toutes les montures {fr_low}", f"All {en_l.lower()} frames")}</a>
    </div>
    <p class="note">{B("Le message part déjà écrit : vous pouvez le modifier, ou tout effacer, avant de l'envoyer. Nous répondons pendant les heures d'ouverture.", "The message is already typed: you can edit it, or delete it, before sending. We reply during opening hours.")}</p>
      </aside>
    </div>
  </section>
  {sim_block}'''
            written.append(site.page(
                frame_url(f), f"{f['nom']} — DM OPTIQUE SARL",
                f"{f['phrase']} Demandez-la sur WhatsApp au 656 122 239.",
                fiche_main,
                ld_graph=[site.crumb_ld([("Accueil", "/"), ("Montures", "/montures/"),
                                          (fr_l, f"/montures/{c}/"), (f["nom"], frame_url(f))])],
                og_image=(f["photos"][0], f["nom"]), og_wh=(1600, 1200), dock_wa=(fr_m, en_m)))

    # ── Examen de vue ───────────────────────────────────────────────────────────
    exam_steps = [
        ("01", "Anamnèse", "History",
         "On commence par ce que vous ressentez et ce que vous portez déjà.",
         "It starts with what you feel and what you already wear."),
        ("02", "Bilan optique", "Optical assessment",
         "Le bilan de départ, avant toute mesure.",
         "The starting assessment, before any measurement."),
        ("03", "Prise des acuités visuelles", "Visual acuity",
         "On mesure ce que chaque œil voit, de loin comme de près.",
         "We measure what each eye sees, far and near."),
        ("04", "Examens de réfraction", "Refraction",
         "On détermine la correction que vos verres devront porter.",
         "We work out the correction your lenses will need."),
    ]
    steps_html = chr(10).join(
        f'<li class="rv"><span class="n">{n}</span><h2>{B(fr_t, en_t)}</h2><p>{B(fr_p, en_p)}</p></li>'
        for n, fr_t, en_t, fr_p, en_p in exam_steps)
    exam_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Examen de vue", "Eye examination"), None)])}
    <h1 class="rv">{B("Examen de vue à Bonabéri", "Eye examination in Bonaberi")}</h1>
    <p class="lede rv">{B("On mesure ce que votre œil demande, avant de parler de monture. L'examen est réalisé au cabinet par le titulaire, M. Domche Noumbi, opticien inscrit à l'ONOC.", "We measure what your eye needs, before anyone talks about frames. The examination is done at the practice by the owner, Mr Domche Noumbi, an optician registered with the ONOC.")}</p>
    <figure class="v2-photo rv">
      <img src="/cabinet-interieur.webp" alt="Intérieur du cabinet DM OPTIQUE SARL à Bonabéri" width="1400" height="926" loading="lazy">
      <figcaption>{B("L'intérieur du cabinet, immeuble West Hotel.", "Inside the practice, West Hotel building.")}</figcaption>
    </figure>
    <ol class="v2-steps">
      {steps_html}
    </ol>
    <figure class="v2-photo rv">
      <img src="/cabinet-examen.webp" alt="Examen de la vue réalisé au cabinet DM OPTIQUE SARL" width="1920" height="1200" loading="lazy">
      <figcaption>{B("Un examen de la vue en cours au cabinet : la mesure à l'autoréfractomètre.", "An eye examination in progress at the practice: the autorefractor measurement.")}</figcaption>
    </figure>
    <dl class="v2-facts rv">
      <div><dt>{B("Horaires de l'examen", "Examination hours")}</dt><dd>{B("Lundi – Samedi · 8h30 – 13h00", "Monday – Saturday · 8:30–13:00")}</dd></div>
      <div><dt>{B("À apporter", "Bring")}</dt><dd>{B("vos anciennes lunettes, si vous en avez", "your current glasses, if you have any")}</dd></div>
      <div><dt>{B("Où", "Where")}</dt><dd>{B(ADDRESS_FR, ADDRESS_EN)}</dd></div>
    </dl>
    <div class="actions rv">
      {wa_btn(EXAM_WA[0], EXAM_WA[1], "Prendre rendez-vous sur WhatsApp", "Book on WhatsApp")}
      <a class="btn" href="{TEL}">{B("Appeler le 656 122 239", "Call 656 122 239")}</a>
    </div>
    <p class="note">{B("Pour des verres correcteurs, apportez l'ordonnance de votre ophtalmologue. Pour des lunettes de soleil, un réglage ou une réparation, non.", "For prescription lenses, bring your ophthalmologist's prescription. For sunglasses, an adjustment or a repair, no.")}</p>
  </section>'''
    written.append(site.page(
        "/examen-de-vue/", "Examen de vue à Bonabéri, Douala — DM OPTIQUE SARL",
        "Examen de vue au cabinet DM OPTIQUE SARL à Bonabéri : anamnèse, bilan optique, acuités visuelles et réfraction. Rendez-vous sur WhatsApp.",
        exam_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Examen de vue", "/examen-de-vue/")])], dock_wa=EXAM_WA))

    # ── Le cabinet ──────────────────────────────────────────────────────────────
    cabinet_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Le cabinet", "The practice"), None)])}
    <h1>{B("Le cabinet à Bonabéri", "The practice in Bonaberi")}</h1>
    <p class="lede">{B("Cabinet d'optique médicale à Douala. Opticien inscrit à l'ONOC. Le titulaire, M. Domche Noumbi, reçoit au cabinet : temps consacré à chaque étape, accueil, confort du patient.", "Optical practice in Douala. Optician registered with the ONOC. The owner, Mr Domche Noumbi, sees you at the practice: time taken at every step, a proper welcome, patient comfort.")}</p>
    <div class="v2-photos">
      <figure>
        <img src="/cabinet-interieur.webp" alt="{esc("Intérieur du cabinet DM OPTIQUE SARL à Bonabéri")}" width="1400" height="926" loading="lazy">
        <figcaption>{B("L'intérieur du cabinet, immeuble West Hotel.", "Inside the practice, West Hotel building.")}</figcaption>
      </figure>
      <figure>
        <img src="/cabinet-enseigne.webp" alt="{esc("Enseigne Consultation au-dessus de l'entrée du cabinet")}" width="1200" height="901" loading="lazy">
        <figcaption>{B("L'entrée : enseigne « Consultation », 1er étage, dernière porte à droite.", "The entrance: “Consultation” sign, first floor, last door on the right.")}</figcaption>
      </figure>
    </div>
    <dl class="v2-facts">
      <div><dt>{B("L'opticien", "The optician")}</dt><dd>{B("M. Domche Noumbi", "Mr Domche Noumbi")}</dd></div>
      <div><dt>{B("Adresse", "Address")}</dt><dd>{B(ADDRESS_FR, ADDRESS_EN)}</dd></div>
      <div><dt>{B("Horaires", "Opening hours")}</dt><dd>{B(HOURS_FR, HOURS_EN)}</dd></div>
      <div><dt>{B("Paiement", "Payment")}</dt><dd>{B("Espèces, Mobile Money, paiement en plusieurs fois · livraison possible", "Cash, Mobile Money, payment in instalments · delivery possible")}</dd></div>
      <div><dt>{B("Assurance", "Insurance")}</dt><dd>{B("Belife Insurance, Willis Towers Watson, Groupe Activa : dossier de prise en charge monté avec vous, selon votre police", "Belife Insurance, Willis Towers Watson, Groupe Activa: claim file built with you, per your policy")}</dd></div>
    </dl>
    <div class="actions">
      <a class="btn" href="/montures/">{B("Voir les montures", "See the frames")}</a>
      {wa_btn(VISIT_WA[0], VISIT_WA[1], "Écrire sur WhatsApp", "Write on WhatsApp")}
    </div>
  </section>'''
    written.append(site.page(
        "/le-cabinet/", "Le cabinet DM OPTIQUE SARL à Bonabéri, Douala",
        "Le cabinet d'optique médicale DM OPTIQUE SARL à Bonabéri, Douala : M. Domche Noumbi, opticien inscrit à l'ONOC. Photos réelles du cabinet.",
        cabinet_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Le cabinet", "/le-cabinet/")])], dock_wa=VISIT_WA))

    # ── Contact ─────────────────────────────────────────────────────────────────
    contact_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), ("Contact", None)])}
    <h1>{B("Venez nous voir à Bonabéri", "Come and see us in Bonaberi")}</h1>
    <p class="lede">{B("Deux gestes suffisent : appeler, ou écrire.", "Two gestures are enough: call, or write.")}</p>
    <div class="actions">
      {wa_btn(VISIT_WA[0], VISIT_WA[1], "Écrire sur WhatsApp", "Write on WhatsApp")}
      <a class="btn" href="{TEL}">{B("Appeler le cabinet", "Call the practice")}</a>
      <a class="btn" href="{esc(MAPS)}" rel="noopener">{B("Ouvrir dans Maps", "Open in Maps")}</a>
    </div>
    <dl class="v2-facts">
      <div><dt>{B("Téléphone & WhatsApp", "Phone & WhatsApp")}</dt><dd>+237 656 122 239</dd></div>
      <div><dt>{B("Adresse", "Address")}</dt><dd>{B(ADDRESS_FR, ADDRESS_EN)}</dd></div>
      <div><dt>{B("Horaires", "Opening hours")}</dt><dd>{B(HOURS_FR, HOURS_EN)}</dd></div>
      <div><dt>{B("Paiement", "Payment")}</dt><dd>{B("Espèces, Mobile Money, paiement en plusieurs fois · livraison possible", "Cash, Mobile Money, payment in instalments · delivery possible")}</dd></div>
      <div><dt>{B("Assurance", "Insurance")}</dt><dd>{B("Belife Insurance, Willis Towers Watson, Groupe Activa : dossier de prise en charge monté avec vous, selon votre police", "Belife Insurance, Willis Towers Watson, Groupe Activa: claim file built with you, per your policy")}</dd></div>
    </dl>
    <figure style="margin:26px 0 0">
      <img src="/cabinet-enseigne.webp" alt="{esc("Enseigne Consultation au-dessus de l'entrée du cabinet")}" width="1200" height="901" loading="lazy" style="display:block;width:100%;height:auto;border-radius:var(--r-lg);border:1px solid var(--line)">
      <figcaption class="note">{B("Repère : l'enseigne « Consultation », immeuble West Hotel — 1er étage, dernière porte à droite.", "Landmark: the “Consultation” sign, West Hotel building — first floor, last door on the right.")}</figcaption>
    </figure>
    <p class="note">{B("Le bouton WhatsApp ouvre la conversation avec le message déjà écrit : vous pouvez le modifier avant de l'envoyer. Nous répondons pendant les heures d'ouverture.", "The WhatsApp button opens the conversation with the message already written. You can edit it before sending. We reply during opening hours.")}</p>
  </section>'''
    written.append(site.page(
        "/contact/", "Contact et adresse — DM OPTIQUE SARL, Bonabéri",
        "DM OPTIQUE SARL, immeuble West Hotel, 1er étage, Ndobo Mayor, Bonabéri, Douala. WhatsApp et téléphone : +237 656 122 239. Horaires lun–sam.",
        contact_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Contact", "/contact/")])], dock_wa=VISIT_WA))

    # ── Page 404 + en-têtes hôte (préparation Cloudflare, F7) ───────────────────
    notfound_main = f'''<section class="wrap">
    <h1>{B("Page introuvable", "Page not found")}</h1>
    <p class="lede">{B("Cette page n'existe pas ou a été déplacée. Le cabinet, lui, est bien à Bonabéri.", "This page does not exist or has moved. The practice is still in Bonaberi.")}</p>
    <div class="actions">
      <a class="btn" href="/">{B("Retour à l'accueil", "Back to home")}</a>
      <a class="btn" href="/montures/">{B("Voir les montures", "See the frames")}</a>
      {wa_btn(VISIT_WA[0], VISIT_WA[1], "Écrire sur WhatsApp", "Write on WhatsApp")}
    </div>
    <p class="note">{B(ADDRESS_FR, ADDRESS_EN)}</p>
  </section>'''
    head404 = site._head("/404.html", "Page introuvable — DM OPTIQUE SARL",
                         "Page introuvable. Retrouvez l'accueil, les montures et le contact du cabinet DM OPTIQUE SARL à Bonabéri.",
                         None, None, None)
    head404 = re.sub(r'<link rel="canonical" href="[^"]*">\n?', "", head404, count=1)
    head404 = head404.replace("</head>", '<meta name="robots" content="noindex,follow">\n</head>', 1)
    page404 = f'''{head404}
<body>
<a class="skiplink" href="#main">{B("Aller au contenu", "Skip to content")}</a>
<p id="say" class="sr" role="status" aria-live="polite"></p>

{site.header}

<main id="main" class="v2-main">
{notfound_main}
</main>

{site.footer}
{site._dock_for(VISIT_WA)}
{chr(10).join(site.scripts)}
</body>
</html>
'''
    (OUTDIR / "404.html").write_text(page404, encoding="utf-8")
    (OUTDIR / "_headers").write_text(HEADERS, encoding="utf-8")

    # ── llms.txt (20/10, proposition validée par King — écart AEO n°1 du test open-seo) ──────────
    # Fichier de découverte pour crawlers IA : que du vrai (services, pages, coordonnées), aucun
    # prix, aucune marque, aucune prétention. Bilingue sur les pages-hubs, fiches en français
    # (chaque page existe FR/EN — dit en clair dans la section Langues).
    LLMS_NAMED = {
        "/": ("Accueil — le cabinet, les services, les montures", "Home — the practice, services, frames"),
        "/montures/": ("Montures — le catalogue complet", "Frames — the full catalogue"),
        "/montures/femmes/": ("Montures femme (24)", "Women's frames (24)"),
        "/montures/enfants/": ("Montures enfants (10)", "Children's frames (10)"),
        "/montures/hommes/": ("Montures homme (6)", "Men's frames (6)"),
        "/examen-de-vue/": ("Examen de la vue — le déroulé, les horaires, ce qu'il faut apporter", "Eye examination — the steps, hours, what to bring"),
        "/le-cabinet/": ("Le cabinet — l'équipement et l'adresse", "The practice — equipment and address"),
        "/contact/": ("Contact — adresse, horaires, WhatsApp", "Contact — address, hours, WhatsApp"),
    }
    llms = ["# DM OPTIQUE SARL", "",
            "> Cabinet d'optique médicale à Bonabéri, Douala (Cameroun), inscrit à l'ONOC. Examen de la vue, verres sur ordonnance, montures femme/homme/enfant, réglage et réparation. Le premier contact passe par WhatsApp : le message arrive déjà écrit.",
            "> Medical optical practice in Bonaberi, Douala (Cameroon), registered with the ONOC (national opticians order). Eye examinations, prescription lenses, frames for women, men and children, adjustment and repair. First contact is WhatsApp: the message arrives pre-written.",
            "", "## Pages", ""]
    fiches = []
    nom_par_slug = {f["slug"]: f["nom"] for f in frames}
    for p in site.paths:
        if p in LLMS_NAMED:
            fr, en = LLMS_NAMED[p]
            llms.append(f"- [{fr}]({site.abs(p)}) — {en}")
        else:
            slug = p.rstrip("/").rsplit("/", 1)[-1]
            fiches.append(f"- [{nom_par_slug.get(slug, slug)}]({site.abs(p)})")
    llms += ["", "## Fiches des montures",
             "Chaque monture photographiée au cabinet a sa page ; chaque page existe en français et en anglais.",
             ""] + fiches
    llms += ["", "## Coordonnées",
             f"- Adresse : {ADDRESS_FR}",
             "- Téléphone et WhatsApp : +237 656 122 239",
             "- Horaires : Lundi–Samedi, 8h30–17h30 · examen de la vue 8h30–13h00",
             "- Langues : français et anglais sur toutes les pages", ""]
    llms_txt = chr(10).join(llms)
    n_links = llms_txt.count("](https://dmoptiquesarl.com")
    if n_links != 48 or "+237 656 122 239" not in llms_txt or "FCFA" in llms_txt \
            or any(b in llms_txt for b in ("Ray-Ban", "Oakley", "Gucci", "Essilor", "Zeiss", "NIDEK", "HP")):
        sys.exit(f"llms.txt incohérent : {n_links} liens (attendu 48), verrous à vérifier")
    (OUTDIR / "llms.txt").write_text(llms_txt, encoding="utf-8")
    print(f"  llms.txt : {n_links} liens, {len(llms_txt)} caractères")

    # ── Sitemap ─────────────────────────────────────────────────────────────────
    if site.base:
        urls = "".join(f"  <url><loc>{esc(site.abs(p))}</loc></url>\n" for p in site.paths)
        (OUTDIR / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
            encoding="utf-8")
    else:
        print("! pas d'adresse canonique dans l'accueil : sitemap non régénéré")

    print(f"ok: {len(written)} pages v2 ({len(frames)} montures) + sitemap ({len(site.paths)} URL)")


if __name__ == "__main__":
    main()
