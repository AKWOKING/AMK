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
- Schémas : `BreadcrumbList` partout, `ItemList` sur hub/catégories, `Product` **sans** `Offer` ni prix
  sur chaque fiche (28/10 : la porte de livraison le demande, le prix reste interdit).
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
import datetime
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "hosting/previews/dmoptic/index.html"
FRAMES = ROOT / "clients/dm-optic/site/frames.json"
# 21/10 — miroir anglais : les fiches ont maintenant leur texte EN dans un fichier à part, indexé par
# code. Le build REFUSE de tourner si une monture n'a pas sa traduction (mieux qu'une page à moitié
# française sous /en/). Ajouter une monture = ajouter une entrée ici.
FRAMES_EN = ROOT / "clients/dm-optic/site/frames-en.json"
OUTDIR = ROOT / "hosting/previews/dmoptic"

# ── Surface d'indexation (26/10/2026) ───────────────────────────────────────────────────────────
# Search Console du 23/10 : 102 pages non indexées, 4 indexées, dont 89 « Discovered » — le site
# demandait 96 URL alors que 80 fiches (40 × FR/EN) n'ont qu'un titre, une phrase et trois photos.
# Décision : les fiches restent EN LIGNE (le lien WhatsApp continue de marcher) mais passent en
# `noindex,follow`, et le sitemap ne garde que les 8 pages qui ont du contenu + leurs 8 miroirs.
# `INDEX_FICHES = True` rouvre tout : c'est le seul endroit à changer, et le sitemap suit.
# La porte qui empêche la dérive : `tools/ops/dm_index_surface.py --check`.
INDEX_FICHES = False
WHITELIST = ROOT / "clients/dm-optic/seo/index-whitelist.txt"
ROBOTS_NOINDEX = '<meta name="robots" content="noindex,follow">'


def liste_blanche() -> set:
    """Les fiches que Google a DÉJÀ indexées : elles restent indexables (voir le fichier)."""
    if not WHITELIST.exists():
        return set()
    out = set()
    for ligne in WHITELIST.read_text(encoding="utf-8").splitlines():
        l = ligne.split("#", 1)[0].strip()
        if l:
            out.add(l if l.endswith("/") else l + "/")
    return out

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
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'

# CACHE — 23/10 —————————————————————————————————————————————
# Cloudflare Pages ne lit un splat `*` qu'en **fin** de motif : `/*.webp` ne matcherait rien
# (leçon de l'audit du 23/10). D'où un bloc par dossier, et un bloc par fichier à la racine.
# La règle équivalente côté tableau de bord est dans clients/dm-optic/launch/CACHE-2026-10-23.md.
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/montures/*
  Cache-Control: public, max-age=604800

/apple-touch-icon.png
  Cache-Control: public, max-age=604800
/cabinet-enseigne.webp
  Cache-Control: public, max-age=604800
/cabinet-examen.webp
  Cache-Control: public, max-age=604800
/cabinet-hero-1080.webp
  Cache-Control: public, max-age=31536000, immutable
/cabinet-hero-640.webp
  Cache-Control: public, max-age=31536000, immutable
/cabinet-hero.webp
  Cache-Control: public, max-age=31536000, immutable
/cabinet-interieur.webp
  Cache-Control: public, max-age=604800
/dm-logo.webp
  Cache-Control: public, max-age=31536000, immutable
/dmoptic-solaires.webp
  Cache-Control: public, max-age=604800
/favicon-192.png
  Cache-Control: public, max-age=604800
/favicon-32.png
  Cache-Control: public, max-age=604800
/favicon.ico
  Cache-Control: public, max-age=604800
/og.jpg
  Cache-Control: public, max-age=604800

# Pas de bloc pour le HTML : Cloudflare Pages le sert déjà en `max-age=0, must-revalidate`.
# Le forcer ici demanderait `/*.html`, un motif que l'hôte n'applique pas (splat en fin seulement).
"""

# 22/10 (soir) — PAS de fichier `_redirects`. Cloudflare Workers n'accepte que des chemins RELATIFS
# dans ce fichier : « Invalid _redirects configuration: Line 1: Only relative URLs are allowed »
# (code 100324), et le déploiement échoue — vérifié dans le journal de build du 22/10.
# Surtout : `_redirects` ne compare que des CHEMINS, jamais des hôtes ; une redirection
# www.dmoptiquesarl.com → dmoptiquesarl.com n'y a donc pas sa place, quelle que soit la syntaxe.
# La redirection www se fait au niveau de la zone : Cloudflare → Rules → Redirect Rules.
# (Le canonical vers l'apex reste la ceinture de sécurité pour les moteurs.)
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
.v2-door h2{margin:0;font-size:1.05rem}  /* 28/10 : 1,15 rem etait la 7e taille de la page (plafond 6, §5) */
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
/* 28/10 · choice overload : la famille repliee. Un depliant natif, aucun JavaScript de plus. */
.v2-more{margin:16px 0 0}
.v2-more>summary{display:inline-flex;align-items:center;gap:8px;cursor:pointer;list-style:none;
  font:500 var(--fs-label)/1.7 var(--f-m);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);
  padding:6px 0;min-height:44px}
.v2-more>summary::-webkit-details-marker{display:none}
.v2-more>summary::after{content:"+";font-size:14px;line-height:1}
.v2-more[open]>summary::after{content:"–"}
.v2-more>summary:focus-visible{outline:2px solid var(--brand);outline-offset:3px;border-radius:4px}
.v2-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* 28/10 · questions : la question en gras, la reponse en dessous. Pas de depliant : un moteur et un
   assistant lisent le texte tel qu'il est servi, et une reponse repliee n'est pas une reponse citee. */
.v2-qa{margin:14px 0 30px;padding:0}
.v2-qa>div{padding:16px 0;border-top:1px solid var(--line)}
.v2-qa>div:first-child{border-top:0}
.v2-qa dt{font-weight:700;color:var(--ink);font-size:var(--fs-base);line-height:1.4}
.v2-qa dd{margin:6px 0 0;color:var(--ink-2);font-size:var(--fs-sm);line-height:1.65;max-width:68ch}
/* 28/10 · closure : la fiche suivante depasse de 22 % — assez pour que l'oeil complete la serie,
   assez peu pour que la fiche lue reste entiere. Le defilement est natif, avec accroche. */
.v2-rail{grid-auto-flow:column;grid-auto-columns:78%;overflow-x:auto;scroll-snap-type:x mandatory;
  scrollbar-width:thin;padding-bottom:8px;margin-right:-16px;padding-right:16px}
.v2-rail>*{scroll-snap-align:start}
@media(min-width:780px){.v2-rail{grid-auto-flow:row;grid-auto-columns:auto;overflow:visible;
  padding-bottom:0;margin-right:0;padding-right:0}}
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
/* 28/10 · connectedness : des cartes separees lisaient comme des sujets distincts. Une seule
   surface, separee par des filets : la liaison dit « et ensuite ». La regle vaut a TOUTES les
   largeurs — en colonne sur telephone, en deux colonnes au-dela de 760 px. */
.v2-steps{counter-reset:v2step;list-style:none;margin:26px 0 0;padding:0;display:grid;gap:0;
  background:var(--card);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden}
.v2-steps li{background:none;padding:18px;border:0;border-radius:0;border-top:1px solid var(--line)}
.v2-steps li:first-child{border-top:0}
@media(min-width:760px){.v2-steps{grid-template-columns:1fr 1fr}
  .v2-steps li{border-left:1px solid var(--line)}
  .v2-steps li:nth-child(odd){border-left:0}
  .v2-steps li:nth-child(-n+2){border-top:0}}
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
  // 21/10 — le miroir /en/ sert la même page avec data-lang="en" : les libellés du filtre suivent.
  var EN=(document.documentElement.getAttribute('data-lang')==='en');
  function L(fr,en){return EN?en:fr;}
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
    count.textContent=n+(n>1?L(' affichées',' shown'):L(' affichée',' shown'));
    /* 28/10 · Parkinson : ce bouton ne montre pas tout, il ferme le panneau et amene a la grille.
       Le libelle dit maintenant ce qu'il fait, et cesse d'etre le jumeau d'Effacer. */
    if(show)show.textContent=L('Voir les montures','See the frames');
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


# ── Miroir anglais ────────────────────────────────────────────────────────────────────────────────
# Le site est bilingue dans le DOM (`fr-only` / `en-only` + data-lang), mais pour Google une page
# n'a qu'une langue : celle de son <html lang>. Depuis le 21/10 chaque page a donc une adresse
# anglaise réelle (/en/…), reliée par hreflang. Le miroir est fabriqué à partir de la page française :
# même DOM, langue inversée, liens internes réécrits, titres et descriptions traduits.

def en_path(path):
    return "/en/" if path == "/" else "/en" + path


def wa(msg):
    return WA + quote(msg, safe="!'()*-._~")


def set_attr(head, attr, key, val):
    pat = rf'(<meta {attr}="{re.escape(key)}" content=")[^"]*(">)'
    if re.search(pat, head):
        return re.sub(pat, lambda m: m.group(1) + esc(val) + m.group(2), head, count=1)
    return head.replace("</head>", f'<meta {attr}="{key}" content="{esc(val)}">\n</head>', 1)


def to_en(page_html, path, title, desc, base, ld_en=()):
    """Page française → page anglaise. Une seule source de vérité : le contenu n'est pas dupliqué.

    Sauf le balisage qui porte du TEXTE : une FAQPage française sur une page anglaise dit à un
    moteur une chose que le visiteur ne peut pas lire. `ld_en` remplace donc ces nœuds par leur
    version anglaise, avant la réécriture des adresses.
    """
    fr_url, en_url = base + path, base + en_path(path)
    head, sep, body = page_html.partition("</head>")
    if not sep:
        raise SystemExit("miroir : </head> introuvable sur " + path)

    head = head.replace('<html lang="fr" data-lang="fr"', '<html lang="en" data-lang="en"', 1)
    head = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", head, count=1, flags=re.S)
    head = set_attr(head, "name", "description", desc)
    head = set_attr(head, "property", "og:title", title)
    head = set_attr(head, "property", "og:description", desc)
    head = set_attr(head, "property", "og:url", en_url)
    head = re.sub(r'<link rel="canonical" href="[^"]*">',
                  '<link rel="canonical" href="%s">' % esc(en_url), head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", head)
    head += (f'<link rel="alternate" hreflang="fr" href="{esc(fr_url)}">\n'
             f'<link rel="alternate" hreflang="en" href="{esc(en_url)}">\n'
             f'<link rel="alternate" hreflang="x-default" href="{esc(fr_url)}">\n')
    head = head.replace('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="en_US">')
    head = head.replace('<meta property="og:locale:alternate" content="en_US">',
                        '<meta property="og:locale:alternate" content="fr_FR">')

    # Langue mémorisée : sur /en/, l'anglais gagne — sinon un visiteur déjà venu en français
    # verrait du français sous une adresse anglaise.
    boot_fr = 'var l=localStorage.getItem("dmoptic-lang");if(l==="en"||l==="fr")h.setAttribute("data-lang",l);'
    boot_en = 'h.setAttribute("data-lang","en");try{localStorage.setItem("dmoptic-lang","en")}catch(e){}'
    if boot_fr not in head and boot_fr not in body:
        raise SystemExit("miroir : script de langue introuvable sur " + path)
    head, body = head.replace(boot_fr, boot_en, 1), body.replace(boot_fr, boot_en, 1)

    # 3. Chemins relatifs : la page anglaise est un dossier plus bas. L'accueil est le seul à pointer
    #    ses fichiers sans « ../ » ; on normalise les deux cas (src, srcset, préchargement, polices CSS).
    def assets(part):
        def urls(val):
            return ", ".join("../" + u if not u.startswith(("/", "http", "../")) else u
                             for u in val.split(", "))
        part = re.sub(r'src="((?:\.\./)+)', lambda m: 'src="../' + m.group(1), part)
        part = re.sub(r'src="(?!\.\./|/|https?:|data:)([^"]+)"', lambda m: 'src="../' + m.group(1) + '"', part)
        part = re.sub(r'(?:image)?srcset="((?:\.\./)+)', lambda m: m.group(0)[:m.group(0).index('="') + 2] + "../" + m.group(1), part)
        part = re.sub(r'((?:image)?srcset)="(?!\.\./|/|https?:)([^"]+)"',
                      lambda m: m.group(1) + '="' + urls(m.group(2)) + '"', part)
        return part
    head, body = assets(head), assets(body)
    head = head.replace("url(fonts/", "url(/fonts/").replace("url(dm-logo.webp)", "url(/dm-logo.webp)")

    # Liens internes : /montures/ → /en/montures/. Les fichiers (une extension dans le chemin) ne
    # bougent pas : les images, polices et la vignette vivent à la racine du domaine.
    def link(m):
        u = m.group(1)
        if not u.startswith("/") or u.startswith("/en/") or u == "/en":
            return m.group(0)
        if "." in u.split("#")[0].split("?")[0]:
            return m.group(0)
        return 'href="/en' + (u if u != "/" else "/") + '"'
    body = re.sub(r'href="([^"]*)"', link, body)
    # 28/10 · le lien de langue du pied de page est un vrai <a> (les boutons FR/EN n'en sont pas) :
    # sans lui, les pages anglaises n'étaient atteignables que par hreflang et sitemap — orphelines
    # pour un crawler. Sur le miroir, il renvoie vers le français, après la réécriture des liens.
    body = body.replace('<a class="flang" href="/en/" hreflang="en" lang="en">English</a>',
                        '<a class="flang" href="/" hreflang="fr" lang="fr">Français</a>')

    # Boutons WhatsApp : le lien statique (sans JavaScript) part avec le message anglais.
    def wa_link(m):
        tag = m.group(0)
        d = re.search(r'data-en="([^"]*)"', tag)
        if not d:
            return tag
        msg = html.unescape(d.group(1))
        return re.sub(r'href="[^"]*"', 'href="' + esc(wa(msg)) + '"', tag, count=1)
    body = re.sub(r'<a\b[^>]*\bclass="[^"]*\bwa\b[^"]*"[^>]*>', wa_link, body)

    # Textes alternatifs : le HTML servi est déjà en anglais (pas besoin d'attendre le JavaScript).
    def alt(m):
        tag = m.group(0)
        v = re.search(r'data-alt-en="([^"]*)"', tag)
        if not v:
            return tag
        return re.sub(r'alt="[^"]*"', 'alt="' + v.group(1) + '"', tag, count=1)
    body = re.sub(r"<img\b[^>]*>", alt, body)

    body = body.replace("Rechercher une monture…", "Search for a frame…")
    body = body.replace("Tout afficher", "Show all")

    # Données structurées : les adresses de page deviennent anglaises, les fichiers restent à la racine.
    # Nœuds qui décrivent LA PAGE (et non l'entreprise) : eux seuls changent d'adresse en /en/.
    # Sans cette liste, l'URL de l'entreprise deviendrait /en/ sur les pages anglaises.
    PAGE_SCOPED = {"BreadcrumbList", "ListItem", "WebPage", "Service", "FAQPage",
                   "Question", "Answer", "Product"}
    by_type = {n.get("@type"): n for n in ld_en}

    def swap_urls(node):
        """Réécrit base/… → base/en/…, récursivement, dans un nœud de page."""
        if isinstance(node, dict):
            return {k: swap_urls(v) for k, v in node.items()}
        if isinstance(node, list):
            return [swap_urls(v) for v in node]
        if isinstance(node, str) and node.startswith(base + "/"):
            return base + "/en" + node[len(base):]
        return node

    def ld(m):
        block = m.group(0)
        inner = re.search(r">(\{.*\})</script>", block, re.S)
        if not inner:
            return block
        doc = json.loads(inner.group(1))
        nodes = doc["@graph"] if "@graph" in doc else [doc]
        out = []
        for n in nodes:
            typ = n.get("@type")
            n = json.loads(json.dumps(by_type[typ])) if typ in by_type else n
            out.append(swap_urls(n) if typ in PAGE_SCOPED else n)
        if out != nodes:
            doc = dict(doc, **{"@graph": out}) if "@graph" in doc else out[0]
            block = ('<script type="application/ld+json">'
                     + json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "</script>")
        return block

    # Les données structurées vivent dans <head> : les traiter aussi dans le corps laissait le
    # balisage anglais pointer sur les adresses françaises (28/10).
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', ld, head, flags=re.S)
    body = re.sub(r'<script type="application/ld\+json">.*?</script>', ld, body, flags=re.S)
    return head + "</head>" + body


# Textes anglais des montures, chargés au démarrage (frames-en.json). Vide = build impossible.
EN = {}


def tr_en(f, field):
    return EN[f["code"]][field]


def frame_msg(f):
    return (f"Bonjour DM OPTIQUE SARL, je suis intéressé par la monture « {f['nom']} ». Est-elle disponible ?",
            f"Hello DM OPTIQUE SARL, I am interested in frame \"{tr_en(f, 'nom')}\". Is it available?")


def card(f, level=2):
    fr_msg, en_msg = frame_msg(f)
    img = (f'<img src="{esc(f["photos"][0])}" alt="{esc(f["nom"])}" '
           f'data-alt-en="{esc(tr_en(f, "nom"))}" loading="lazy" '
           f'width="1600" height="1200">') if f.get("photos") else ""
    return f'''<li class="v2-card rv" data-forme="{esc(slugify(f["forme"]))}" data-couleur="{esc(slugify(f["couleur"]))}" data-name="{esc(f["nom"] + " " + f["forme"] + " " + f["couleur"])}">
    <article>
      {img}
      <div class="v2-body">
        <h{level}><a href="{esc(frame_url(f))}">{B(f["nom"], tr_en(f, "nom"))}</a></h{level}>
        <ul class="v2-tags"><li>{B(f["forme"], tr_en(f, "forme"))}</li><li>{B(f["couleur"], tr_en(f, "couleur"))}</li></ul>
        <p>{B(f["phrase"], tr_en(f, "phrase"))}</p>
        <div class="v2-actions">
          <a class="btn" href="{esc(frame_url(f))}">{B("Voir la fiche", "See the frame")}</a>
          {wa_btn(fr_msg, en_msg, "Demander cette monture", "Ask about this frame")}
        </div>
      </div>
    </article>
  </li>'''


def mini_card(f):
    img = (f'<img src="{esc(f["photos"][0])}" alt="{esc(f["nom"])}" '
           f'data-alt-en="{esc(tr_en(f, "nom"))}" loading="lazy" '
           f'width="1600" height="1200">') if f.get("photos") else ""
    return f'''<li class="v2-card rv">
    <article>
      {img}
      <div class="v2-body">
        <h3><a href="{esc(frame_url(f))}">{B(f["nom"], tr_en(f, "nom"))}</a></h3>
        <ul class="v2-tags"><li>{B(f["forme"], tr_en(f, "forme"))}</li><li>{B(f["couleur"], tr_en(f, "couleur"))}</li></ul>
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
        self.noindex = []        # pages écrites en noindex,follow (26/10) : hors sitemap
        self.pairs = []          # (chemin, titre EN, description EN) — miroir /en/
        self.ld_en = {}          # chemin → nœuds de schéma anglais (28/10)

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
        # Le préchargement de la photo du premier écran ne concerne QUE l'accueil : recopié sur les
        # 47 autres pages, il téléchargeait 86 Ko d'une image que la page n'affiche pas (audit 21/10).
        head = re.sub(r'<link rel="preload" as="image"[^>]*>\n?', "", head)
        head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1, flags=re.S)

        def set_meta(attr, key, val):
            nonlocal head
            pat = rf'(<meta {attr}="{re.escape(key)}" content=")[^"]*(">)'
            if re.search(pat, head):
                head = re.sub(pat, lambda mm: mm.group(1) + esc(val) + mm.group(2), head, count=1)
            else:
                head = head.replace("</head>", f'<meta {attr}="{key}" content="{esc(val)}">\n</head>', 1)

        url = self.abs(path)
        # 21/10 — hreflang calculé PAR PAGE (le gabarit de l'accueil ne connaît que l'accueil).
        head = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", head)
        if self.base and not path.endswith(".html"):
            fr_u, en_u = self.abs(path), self.abs(en_path(path))
            alt = (f'<link rel="alternate" hreflang="fr" href="{esc(fr_u)}">\n'
                   f'<link rel="alternate" hreflang="en" href="{esc(en_u)}">\n'
                   f'<link rel="alternate" hreflang="x-default" href="{esc(fr_u)}">\n')
            head = head.replace("</head>", alt + "</head>", 1)
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
            url_img = self.abs(og_image[0])
            set_meta("property", "og:image", url_img)
            # 28/10 : le type suit l'extension. Un og:image en WebP n'est pas garanti dans WhatsApp,
            # qui est LE canal de ces clients — les fiches repointent donc vers le JPEG 1200×630.
            if url_img.lower().endswith((".jpg", ".jpeg")):
                set_meta("property", "og:image:type", "image/jpeg")
            elif url_img.lower().endswith(".webp"):
                set_meta("property", "og:image:type", "image/webp")
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

    def page(self, path, title, desc, main_html, ld_graph=None, og_image=None, og_wh=None, extra_script="", dock_wa=None,
             en_meta=None, indexable=True, ld_en=None):
        head = self._head(path, title, desc, ld_graph, og_image, og_wh)
        if not indexable:
            # Le miroir anglais est fabriqué à partir de ce fichier : il hérite du noindex, c'est voulu.
            head = head.replace("</head>", ROBOTS_NOINDEX + "\n</head>", 1)
            self.noindex.append(path)
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
        if en_meta:
            self.pairs.append((path, en_meta[0], en_meta[1]))
            if ld_en:
                self.ld_en[path] = ld_en
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

    def product_ld(self, f, url, desc):
        """La fiche monture, déclarée comme un produit — SANS prix et SANS `Offer`.

        Le 22/10, la règle était « jamais Product » : elle datait du temps où l'on craignait qu'un
        schéma produit ne promette un prix. La porte de livraison (`audit_delivery.py`, D7) demande
        aujourd'hui le contraire : `name`, `image`, `description`, `sku` — et toujours aucun prix.
        Ce que Google lit ici, c'est un objet nommé, pas une offre commerciale.
        """
        return {"@type": "Product",
                "name": f["nom"],
                "url": url,
                "image": [self.abs(f"/montures/monture-{f['code'].lower()}.jpg")],
                "description": desc,
                "sku": f["code"],
                "category": "Monture de vue"}

    def itemlist_ld(self, frames):
        return {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f["nom"], "url": self.abs(frame_url(f))}
            for i, f in enumerate(frames)]}


def main():
    src = SRC.read_text(encoding="utf-8")
    site = Site(src)

    # 28/10 · une page de service déclare ce qu'elle rend, et qui le rend. Le `provider` pointe vers
    # l'entité Optician de l'accueil par son @id : Google relie la page à l'établissement, pas à un
    # texte isolé. Aucun prix, aucune offre — rien à vendre en ligne.
    def service_ld(path, name, service_type, desc):
        return {"@type": "Service", "@id": site.abs(path) + "#service", "name": name,
                "serviceType": service_type, "description": desc, "url": site.abs(path),
                "provider": {"@id": site.abs("/") + "#dmoptic"},
                "areaServed": [{"@type": "City", "name": "Douala"},
                               {"@type": "Place", "name": "Bonabéri, Ndobo Mayor"}],
                "availableLanguage": ["fr", "en"]}

    frames = json.loads(FRAMES.read_text(encoding="utf-8"))
    # Traductions : une entrée par code, ni plus ni moins. Un oubli arrête le build.
    EN.update(json.loads(FRAMES_EN.read_text(encoding="utf-8")))
    manquants = [f["code"] for f in frames if f["code"] not in EN]
    orphelins = [c for c in EN if c not in {f["code"] for f in frames}]
    if manquants or orphelins:
        sys.exit("frames-en.json désaccordé — manquants : %s · orphelins : %s" % (manquants, orphelins))
    by_cat = {c: [f for f in frames if f["categorie"] == c] for c in CATS}
    written = []
    # L'accueil est écrit par build_dmoptic.py ; il entre dans le miroir comme les autres pages.
    site.pairs.append(("/", "DM OPTIQUE SARL — Optometrist optician in Douala",
                       "Eye examinations, prescription lenses, frames, repairs. An optometrist optician registered with the ONOC. WhatsApp: the message is already written."))

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
          <p>{B("Des montures à essayer au cabinet.", "Frames to try at the practice.")}</p>
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
        ld_graph=[site.crumb_ld([("Accueil", "/"), ("Montures", "/montures/")]), site.itemlist_ld(frames)], dock_wa=HUB_WA,
        en_meta=("All our frames in Bonaberi — DM OPTIQUE SARL",
                 "Women's, men's and children's frames photographed at DM OPTIQUE SARL in Bonaberi, Douala. Choose one, then ask for it on WhatsApp.")))

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
            # 28/10 · choice overload : 17 cases d'un coup, c'est la table de confitures. La famille
            # la plus courte (la forme) reste visible ; la couleur (jusqu'a 11) passe derriere un
            # depliant natif, avec son compte annonce. Les cases restent dans le DOM : le filtre, le
            # fragment # et les puces actives continuent de fonctionner a l'identique.
            if len(pills) > 7:
                groups.append(f'''<details class="v2-more"><summary>{B(fr_g, en_g)} <span class="v2-n">({len(pills)})</span></summary>
        <fieldset class="v2-group">
          <legend class="v2-sr">{B(fr_g, en_g)}</legend>
          <div class="v2-pills">{chr(10).join(pills)}</div>
        </fieldset>
      </details>''')
            else:
                groups.append(f'''<fieldset class="v2-group">
        <legend>{B(fr_g, en_g)}</legend>
        <div class="v2-pills">{chr(10).join(pills)}</div>
      </fieldset>''')
        fr_msg, en_msg = CAT_WA[c]
        n = len(items)
        cat_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Montures", "Frames"), "/montures/"), (B(fr_l, en_l), None)])}
    <h1>{B(f"Montures {fr_low}", f"{en_l} frames")}</h1>
    <p class="lede">{B("Nos montures, photographiées une par une au cabinet, à essayer sur votre visage. Touchez une fiche pour la voir sous d'autres angles, ou demandez-la directement sur WhatsApp.", "Our frames, photographed one by one at the practice, to try on your face. Open a frame to see other angles, or ask for it directly on WhatsApp.")}</p>
    <form class="v2-filters" role="search">
      <div class="v2-toolbar">
        <label class="v2-search">{B("Rechercher", "Search")}<input class="v2-q" type="search" name="q" placeholder="Rechercher une monture…" autocomplete="off" enterkeyhint="search" autocapitalize="none" spellcheck="false"></label>
        <p class="v2-count" role="status" aria-live="polite">Nos montures</p>
        <button class="btn v2-filter-toggle" type="button" aria-expanded="false" aria-controls="filtres-{c}">{B("Filtrer", "Filter")}</button>
        <button class="btn v2-show" type="button">{B("Voir les montures", "See the frames")}</button>
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
            f"Montures {fr_low} du cabinet DM OPTIQUE SARL à Bonabéri : formes et couleurs visibles, à essayer au cabinet. Demande sur WhatsApp.",
            cat_main,
            ld_graph=[site.crumb_ld([("Accueil", "/"), ("Montures", "/montures/"), (fr_l, f"/montures/{c}/")]),
                      site.itemlist_ld(items)],
            extra_script=FILTER_JS, dock_wa=CAT_WA[c],
            en_meta=(f"{en_l} frames in Bonaberi — DM OPTIQUE SARL",
                     f"{en_l} frames at DM OPTIQUE SARL in Bonaberi: shapes and colours you can see, to try on at the practice. Ask on WhatsApp.")))

        for f in items:
            fr_m, en_m = frame_msg(f)
            figs = []
            for i, p in enumerate(f["photos"]):
                loading = "" if i == 0 else ' loading="lazy"'
                figs.append(f'<figure><img src="{esc(p)}" alt="{esc(f["nom"])}" data-alt-en="{esc(tr_en(f, "nom"))}" width="1600" height="1200"{loading}></figure>')
            if figs:
                figs.insert(1, f'<div class="v2-cta-mobile">{wa_btn(fr_m, en_m, "Commander sur WhatsApp", "Ask on WhatsApp")}</div>')
            sims = [g for g in items if g["code"] != f["code"] and g["forme"] == f["forme"]]
            sims += [g for g in items if g["code"] != f["code"] and g not in sims and g["couleur"] == f["couleur"]]
            sims += [g for g in items if g["code"] != f["code"] and g not in sims]
            sims = sims[:3]
            sim_block = ""
            if sims:
                # 28/10 · closure : trois fiches empilees sur telephone = trois ecrans de plus, et
                # rien ne dit qu'il y en a d'autres. Un rail qui laisse depasser la fiche suivante
                # (78 %) dit « la serie continue » sans un mot. Grille classique des 780 px.
                sim_block = f'''<section class="wrap" aria-labelledby="h-sims">
    <h2 id="h-sims" class="rv">{B("Vous aimerez aussi", "You may also like")}</h2>
    <ul class="v2-grid v2-rail">
      {chr(10).join(mini_card(g) for g in sims)}
    </ul>
  </section>'''
            fiche_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Montures", "Frames"), "/montures/"), (B(fr_l, en_l), f"/montures/{c}/"), (esc(f["nom"]), None)])}
    <h1 class="rv">{B(f["nom"], tr_en(f, "nom"))}</h1>
    <p class="lede rv">{B(f["phrase"], tr_en(f, "phrase"))}</p>
    <div class="v2-fiche">
      <div class="v2-gallery rv">
      {chr(10).join(figs)}
      </div>
      <aside class="v2-fiche-aside rv">
    <dl class="v2-facts">
      <div><dt>{B("Catégorie", "Category")}</dt><dd>{B(fr_l, en_l)}</dd></div>
      <div><dt>{B("Forme", "Shape")}</dt><dd>{B(f["forme"], tr_en(f, "forme"))}</dd></div>
      <div><dt>{B("Couleur dominante", "Main colour")}</dt><dd>{B(f["couleur"], tr_en(f, "couleur"))}</dd></div>
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
            fiche_desc = (f"{f['phrase']} Demandez-la sur WhatsApp au 656 122 239 "
                          f"— référence {f['code']}.")
            written.append(site.page(
                frame_url(f), f"{f['nom']} — DM OPTIQUE SARL",
                # La référence en fin de description : sans elle, deux montures de même forme et même
                # couleur (F10/F11, H01/H02/H05/H08) portaient la MÊME description (audit 21/10).
                fiche_desc,
                fiche_main,
                ld_graph=[site.crumb_ld([("Accueil", "/"), ("Montures", "/montures/"),
                                          (fr_l, f"/montures/{c}/"), (f["nom"], frame_url(f))]),
                          site.product_ld(f, site.abs(frame_url(f)), fiche_desc)],
                # 28/10 : l'aperçu de partage pointe le JPEG 1200×630 (WhatsApp), pas la photo WebP.
                og_image=(f"/montures/monture-{f['code'].lower()}.jpg", f["nom"]), og_wh=(1200, 630),
                dock_wa=(fr_m, en_m),
                indexable=(INDEX_FICHES or frame_url(f) in liste_blanche()),
                en_meta=(f"{tr_en(f, 'nom')} — DM OPTIQUE SARL",
                         f"{tr_en(f, 'phrase')} Ask for it on WhatsApp at 656 122 239 — reference {f['code']}.")))

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
    <p class="lede rv">{B("On mesure ce que votre œil demande, avant de parler de monture. L'examen est réalisé au cabinet par le titulaire, M. Domche Noumbi, opticien optométriste inscrit à l'ONOC.", "We measure what your eye needs, before anyone talks about frames. The examination is done at the practice by the owner, Mr Domche Noumbi, an optometrist optician registered with the ONOC.")}</p>
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
    <h2 class="rv">{B("Ce que cet examen fait, et ce qu'il ne fait pas", "What this examination does, and what it does not")}</h2>
    <dl class="v2-facts rv">
      <div><dt>{B("Il mesure", "It measures")}</dt><dd>{B("ce que chaque œil voit, et la correction que vos verres devront porter. Rien ne touche l'œil.", "what each eye sees, and the correction your lenses will need. Nothing touches the eye.")}</dd></div>
      <div><dt>{B("Il ne traite pas", "It does not treat")}</dt><dd>{B("une douleur, une maladie de l'œil, une baisse brutale de la vue : c'est l'ophtalmologue, le médecin spécialiste. On vous le dit et on vous oriente.", "pain, eye disease or a sudden loss of sight: that is for the ophthalmologist, the medical specialist. We say so and point you to the right place.")}</dd></div>
      <div><dt>{B("Quand revenir", "When to come back")}</dt><dd>{B("repère : tous les deux ans pour un adulte sans problème particulier, chaque année pour un enfant. La fréquence qui vous concerne se décide ici.", "guide: every two years for an adult with no particular problem, every year for a child. The schedule that applies to you is decided here.")} <a href="/questions/">{B("Voir les 22 questions", "See the 22 questions")}</a></dd></div>
    </dl>
  </section>'''
    written.append(site.page(
        "/examen-de-vue/", "Examen de vue à Bonabéri, Douala — DM OPTIQUE SARL",
        "Examen de vue au cabinet DM OPTIQUE SARL à Bonabéri : anamnèse, bilan optique, acuités visuelles et réfraction. Rendez-vous sur WhatsApp.",
        exam_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Examen de vue", "/examen-de-vue/")]),
                             service_ld("/examen-de-vue/", "Examen de vue",
                                        "Examen de la vue et réfraction",
                                        "Anamnèse, bilan optique, acuités visuelles et réfraction au cabinet, à Bonabéri (Douala), par un opticien optométriste inscrit à l'ONOC.")],
        dock_wa=EXAM_WA,
        en_meta=("Eye examination in Bonaberi, Douala — DM OPTIQUE SARL",
                 "Eye examination at DM OPTIQUE SARL in Bonaberi: history, optical assessment, visual acuity and refraction. Book on WhatsApp.")))

    # ── Le cabinet ──────────────────────────────────────────────────────────────
    cabinet_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Le cabinet", "The practice"), None)])}
    <h1>{B("Le cabinet à Bonabéri", "The practice in Bonaberi")}</h1>
    <p class="lede">{B("Cabinet d'optique médicale à Douala. Opticien optométriste inscrit à l'ONOC. Le titulaire, M. Domche Noumbi, reçoit au cabinet : temps consacré à chaque étape, accueil, confort du patient.", "Optical practice in Douala. Optometrist optician registered with the ONOC. The owner, Mr Domche Noumbi, sees you at the practice: time taken at every step, a proper welcome, patient comfort.")}</p>
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
      <div><dt>{B("Le titulaire", "Owner")}</dt><dd>{B("M. Domche Noumbi", "Mr Domche Noumbi")}</dd></div>
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
        "Le cabinet d'optique médicale DM OPTIQUE SARL à Bonabéri, Douala : M. Domche Noumbi, opticien optométriste inscrit à l'ONOC. Photos réelles du cabinet.",
        cabinet_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Le cabinet", "/le-cabinet/")])], dock_wa=VISIT_WA,
        en_meta=("The DM OPTIQUE SARL practice in Bonaberi, Douala",
                 "The DM OPTIQUE SARL optical practice in Bonaberi, Douala: Mr Domche Noumbi, optometrist optician registered with the ONOC. Real photos of the practice.")))

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
        contact_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Contact", "/contact/")])], dock_wa=VISIT_WA,
        en_meta=("Contact and address — DM OPTIQUE SARL, Bonaberi",
                 "DM OPTIQUE SARL, West Hotel building, first floor, Ndobo Mayor, Bonaberi, Douala. WhatsApp and phone: +237 656 122 239. Hours Mon-Sat.")))

    # ── Pages de service (28/10) ──────────────────────────────────────────────────────
    # Pourquoi ces deux pages : le rapport Whitespark 2026 place « une page dédiée par service »
    # en tête des signaux on-page locaux, et notre propre audit du 21/10 avait déjà écrit que quatre
    # services étaient décrits sans page. Ce qu'on n'a PAS fait : une page par quartier ni par variante
    # de requête. Google nomme explicitement les pages ville qui renvoient toutes au même endroit comme
    # du doorways abuse, et la production de pages à l'échelle comme du scaled content abuse.
    # Les faits ici sont ceux déjà publiés (ONOC, adresse, horaires, ordonnance, réparation) : rien
    # d'inventé, aucun délai, aucun prix, aucune marque. À faire valider par le client (a-completer.md #8).

    LENS_WA = ("Bonjour DM OPTIQUE SARL, j'ai une ordonnance et je voudrais des verres correcteurs.",
               "Hello DM OPTIQUE SARL, I have a prescription and I would like prescription lenses.")
    REPAIR_WA = ("Bonjour DM OPTIQUE SARL, ma monture a besoin d'une réparation ou d'un réglage.",
                 "Hello DM OPTIQUE SARL, my frame needs a repair or an adjustment.")

    lens_steps = [
        ("01", "L'ordonnance", "The prescription",
         "On lit l'ordonnance de votre ophtalmologue : la correction de chaque œil, l'écart entre les pupilles, la vision de loin et de près.",
         "We read your ophthalmologist's prescription: the correction for each eye, the distance between your pupils, distance and near vision."),
        ("02", "La monture", "The frame",
         "On choisit la monture qui va porter ces verres : la taille du cercle compte autant que la forme. Une monture trop grande décentre le verre.",
         "We choose the frame that will carry those lenses: the size of the rim matters as much as the shape. A frame that is too big decentres the lens."),
        ("03", "Le montage et l'ajustement", "Fitting and adjustment",
         "Le verre est taillé à la forme du cercle, monté, puis la monture est ajustée sur votre visage. On reprend le réglage si quelque chose appuie.",
         "The lens is cut to the rim, fitted, then the frame is adjusted on your face. We re-adjust if anything presses."),
    ]
    lens_steps_html = chr(10).join(
        f'<li class="rv"><span class="n">{n}</span><h2>{B(fr_t, en_t)}</h2><p>{B(fr_p, en_p)}</p></li>'
        for n, fr_t, en_t, fr_p, en_p in lens_steps)
    lens_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Verres sur ordonnance", "Prescription lenses"), None)])}
    <h1 class="rv">{B("Verres sur ordonnance à Bonabéri", "Prescription lenses in Bonaberi")}</h1>
    <p class="lede rv">{B("Un verre correcteur n'est pas un accessoire : c'est la correction écrite par votre ophtalmologue, taillée à la forme de la monture que vous choisissez. Le montage se fait au cabinet, à Douala.", "A corrective lens is not an accessory: it is the correction your ophthalmologist wrote, cut to the shape of the frame you choose. The fitting is done at the practice, in Douala.")}</p>
    <ol class="v2-steps">
      {lens_steps_html}
    </ol>
    <dl class="v2-facts rv">
      <div><dt>{B("Ce qu'il faut apporter", "What to bring")}</dt><dd>{B("l'ordonnance de votre ophtalmologue, et vos lunettes actuelles si vous en avez", "your ophthalmologist's prescription, and your current glasses if you have any")}</dd></div>
      <div><dt>{B("Le délai", "Lead time")}</dt><dd>{B("il dépend du verre commandé : nous vous le donnons au cabinet, sur votre ordonnance, avant toute commande", "it depends on the lens ordered: we tell you at the practice, on your prescription, before anything is ordered")}</dd></div>
      <div><dt>{B("Où", "Where")}</dt><dd>{B(ADDRESS_FR, ADDRESS_EN)}</dd></div>
      <div><dt>{B("Horaires", "Hours")}</dt><dd>{B(HOURS_FR, HOURS_EN)}</dd></div>
    </dl>
    <div class="actions rv">
      {wa_btn(LENS_WA[0], LENS_WA[1], "Envoyer mon ordonnance sur WhatsApp", "Send my prescription on WhatsApp")}
      <a class="btn" href="{TEL}">{B("Appeler le 656 122 239", "Call 656 122 239")}</a>
    </div>
    <p class="note">{B("Pas d'ordonnance ? L'examen de la vue se fait au cabinet, le matin, sur rendez-vous.", "No prescription? The eye examination is done at the practice, in the morning, by appointment.")} <a href="/examen-de-vue/">{B("Voir le déroulé de l'examen", "See how the examination works")}</a></p>
    <p class="note">{B("Vous cherchez d'abord une monture ?", "Looking for a frame first?")} <a href="/montures/">{B("Les montures du cabinet, par catégorie", "The practice's frames, by category")}</a> {B("· Une monture à réparer plutôt ?", "· A frame to repair instead?")} <a href="/reparation-et-entretien/">{B("Réparation et entretien", "Repairs and adjustments")}</a></p>
  </section>'''
    written.append(site.page(
        "/verres-sur-ordonnance/", "Verres sur ordonnance à Bonabéri, Douala — DM OPTIQUE SARL",
        "Verres correcteurs montés au cabinet DM OPTIQUE SARL à Bonabéri, Douala : lecture de l'ordonnance, choix de la monture, montage et ajustement.",
        lens_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Verres sur ordonnance", "/verres-sur-ordonnance/")]),
                             service_ld("/verres-sur-ordonnance/", "Verres sur ordonnance",
                                        "Montage de verres correcteurs sur ordonnance",
                                        "Lecture de l'ordonnance, choix de la monture, montage et ajustement des verres correcteurs au cabinet, à Bonabéri (Douala).")],
        dock_wa=LENS_WA,
        en_meta=("Prescription lenses in Bonaberi, Douala — DM OPTIQUE SARL",
                 "Prescription lenses fitted at the DM OPTIQUE SARL practice in Bonaberi, Douala: reading the prescription, choosing the frame, fitting and adjustment.")))

    repair_steps = [
        ("01", "La photo, d'abord", "A photo first",
         "Envoyez une photo de la monture sur WhatsApp. La réponse vous dit si c'est réparable, et si le déplacement en vaut la peine.",
         "Send a photo of the frame on WhatsApp. The answer tells you whether it can be repaired, and whether the trip is worth it."),
        ("02", "La monture, ensuite", "The frame, then",
         "Apportez-la au cabinet. On regarde la charnière, les vis, les plaquettes, les branches, et on vous dit ce qui est possible — sans promettre l'impossible.",
         "Bring it to the practice. We look at the hinge, the screws, the nose pads, the temples, and tell you what is possible — without promising the impossible."),
        ("03", "Le réglage", "The adjustment",
         "Une monture qui glisse, qui appuie ou qui penche se régale sur votre visage. C'est souvent ce qui manquait, pas une réparation.",
         "A frame that slips, presses or sits crooked is adjusted on your face. That is often what was missing, not a repair."),
    ]
    repair_steps_html = chr(10).join(
        f'<li class="rv"><span class="n">{n}</span><h2>{B(fr_t, en_t)}</h2><p>{B(fr_p, en_p)}</p></li>'
        for n, fr_t, en_t, fr_p, en_p in repair_steps)
    repair_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Réparation et entretien", "Repairs and adjustments"), None)])}
    <h1 class="rv">{B("Réparation et entretien de lunettes à Bonabéri", "Repairs and adjustments in Bonaberi")}</h1>
    <p class="lede rv">{B("Une vis perdue, une branche tordue, une plaquette usée, une charnière qui force : ça se regarde. Envoyez d'abord une photo — vous saurez si le déplacement sert à quelque chose avant de traverser Douala.", "A lost screw, a bent temple, a worn nose pad, a hinge that grinds: it needs looking at. Send a photo first — you will know whether the trip is worth it before crossing Douala.")}</p>
    <ol class="v2-steps">
      {repair_steps_html}
    </ol>
    <figure class="v2-photo rv">
      <img src="/cabinet-enseigne.webp" alt="{esc("Enseigne Consultation au-dessus de l'entrée du cabinet")}" width="1200" height="901" loading="lazy">
      <figcaption>{B("L'entrée : immeuble West Hotel, 1er étage, dernière porte à droite.", "The entrance: West Hotel building, first floor, last door on the right.")}</figcaption>
    </figure>
    <dl class="v2-facts rv">
      <div><dt>{B("Ce qu'on regarde", "What we look at")}</dt><dd>{B("vis, plaquettes, branches, charnières, monture déformée, verre rayé", "screws, nose pads, temples, hinges, a bent frame, a scratched lens")}</dd></div>
      <div><dt>{B("À apporter", "Bring")}</dt><dd>{B("la monture, et l'ordonnance si les verres doivent être refaits", "the frame, and the prescription if the lenses have to be remade")}</dd></div>
      <div><dt>{B("Où", "Where")}</dt><dd>{B(ADDRESS_FR, ADDRESS_EN)}</dd></div>
      <div><dt>{B("Horaires", "Hours")}</dt><dd>{B(HOURS_FR, HOURS_EN)}</dd></div>
    </dl>
    <div class="actions rv">
      {wa_btn(REPAIR_WA[0], REPAIR_WA[1], "Envoyer une photo sur WhatsApp", "Send a photo on WhatsApp")}
      <a class="btn" href="{TEL}">{B("Appeler le 656 122 239", "Call 656 122 239")}</a>
    </div>
    <p class="note">{B("Une monture cassée n'est pas toujours réparable : une soudure sur certains métaux, ou une charnière intégrée, ne se refait pas. On le dit avant, pas après.", "A broken frame is not always repairable: some metal joints, or an integrated hinge, cannot be redone. We say so before, not after.")}</p>
    <h2 class="rv">{B("Réparer ou remplacer ?", "Repair or replace?")}</h2>
    <p class="rv">{B("Trois cas, et ils couvrent presque tout. Une vis, une plaquette, un réglage : c'est une réparation, et c'est souvent ce qui manquait. Une monture déformée ou une branche tordue : ça se redresse, tant que le métal n'a pas cassé. Une monture cassée net, ou dont la charnière est arrachée : on regarde, et on vous dit franchement si c'est fini — avant que vous payiez quoi que ce soit.", "Three cases, and they cover almost everything. A screw, a nose pad, an adjustment: that is a repair, and it is often what was missing. A bent frame or a twisted temple: it can be straightened, as long as the metal has not snapped. A frame broken clean through, or with a torn-off hinge: we look, and we tell you plainly if it is finished — before you pay anything.")}</p>
    <p class="note">{B("Ce que vous pouvez faire vous-même : resserrer une vis avec un tournevis d'horloger. Le reste, non : une branche se tord à froid et casse, la colle ne tient pas une charnière.", "What you can do yourself: tighten a screw with a watchmaker's screwdriver. The rest, no: a temple bent cold snaps, and glue does not hold a hinge.")} <a href="/questions/">{B("Toutes les questions", "All the questions")}</a></p>
    <p class="note">{B("Besoin de verres neufs ?", "Need new lenses?")} <a href="/verres-sur-ordonnance/">{B("Verres sur ordonnance", "Prescription lenses")}</a> {B("· Envie de changer de monture ?", "· Fancy a new frame?")} <a href="/montures/">{B("Nos montures", "Our frames")}</a></p>
  </section>'''
    written.append(site.page(
        "/reparation-et-entretien/", "Réparation et entretien de lunettes à Bonabéri — DM OPTIQUE SARL",
        "Monture cassée, vis perdue, branches tordues, plaquettes usées : le cabinet à Bonabéri regarde la monture, ou une photo sur WhatsApp avant de vous déplacer.",
        repair_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Réparation et entretien", "/reparation-et-entretien/")]),
                               service_ld("/reparation-et-entretien/", "Réparation et entretien de lunettes",
                                          "Réparation, réglage et entretien de montures",
                                          "Réparation, réglage et entretien de montures au cabinet, à Bonabéri (Douala) : vis, plaquettes, branches, charnières, monture déformée.")],
        dock_wa=REPAIR_WA,
        en_meta=("Repairs and adjustments in Bonaberi, Douala — DM OPTIQUE SARL",
                 "Broken frame, lost screw, bent temples, worn nose pads: bring it to the practice in Bonaberi, or send a photo on WhatsApp before travelling.")))

    # ── Les questions (28/10) ───────────────────────────────────────────────────
    # Pourquoi cette page : les gens ne tapent pas « opticien Bonabéri », ils tapent une QUESTION.
    # Vingt-deux questions réelles, chacune avec sa réponse en première phrase, pour qu'une phrase
    # sorte de la page et tienne debout toute seule (c'est ce qu'un moteur cite, et ce qu'un assistant
    # extrait). Rien d'inventé : ni durée, ni prix, ni marque, ni symptôme. Deux réponses DISENT ce que
    # le cabinet ne fait pas — c'est le signal de confiance le plus rare dans ce marché.
    QA = [
        ("L'examen de la vue", "The eye examination", [
            ("Faut-il une ordonnance pour faire un examen de la vue ?",
             "Do I need a prescription to have an eye examination?",
             "Non. L'examen se fait au cabinet, sans ordonnance, et c'est lui qui détermine la correction. L'ordonnance de votre ophtalmologue n'est nécessaire que pour faire tailler les verres.",
             "No. The examination is done at the practice, without a prescription, and it is the examination that works out the correction. Your ophthalmologist's prescription is only needed to have the lenses made."),
            ("Combien de temps prend un examen de la vue ?",
             "How long does an eye examination take?",
             "Nous ne publions pas de durée : elle dépend de ce qu'il y a à mesurer. Vous demandez sur WhatsApp, la réponse vous dit combien de temps prévoir.",
             "We do not publish a duration: it depends on what has to be measured. Ask on WhatsApp, and the answer tells you how much time to allow."),
            ("Quand faut-il refaire contrôler sa vue ?",
             "How often should I have my eyes checked?",
             "Comme repère : tous les deux ans pour un adulte sans problème particulier, chaque année pour un enfant et pour une personne diabétique. Ce sont les intervalles publiés par le Collège des optométristes britannique ; la fréquence qui vous concerne se décide au cabinet, pas sur cette page.",
             "As a guide: every two years for an adult with no particular problem, every year for a child and for anyone with diabetes. These are the intervals published by the College of Optometrists; the schedule that applies to you is decided at the practice, not on this page."),
            ("L'examen touche-t-il l'œil ?",
             "Does the examination touch the eye?",
             "Non. Ce qui est décrit ici (les questions, les acuités, la réfraction) se mesure sans rien poser sur l'œil. Si un examen plus poussé vous semble nécessaire, on vous le dit et on vous oriente.",
             "No. What is described here (the questions, visual acuity, refraction) is measured without putting anything on the eye. If a more thorough examination seems necessary, we say so and point you to the right place."),
            ("L'examen détecte-t-il les maladies de l'œil ?",
             "Does the examination detect eye disease?",
             "Non, et c'est important à savoir. Ici, on mesure la vue et on détermine la correction : la loi camerounaise dit que l'opticien-optométriste conçoit l'équipement optique qui compense une anomalie de la vision. Une douleur, une maladie de l'œil ou une baisse brutale : c'est l'ophtalmologue, le médecin spécialiste.",
             "No, and that matters. Here we measure sight and work out the correction: Cameroonian law says the optometrist optician designs the optical equipment that compensates for a vision defect. Pain, eye disease or a sudden loss of sight: that is for the ophthalmologist, the medical specialist."),
            ("Faut-il prendre rendez-vous ?",
             "Do I need an appointment?",
             "Écrivez sur WhatsApp avant de venir : on vous dit s'il faut un rendez-vous, et quand passer. L'examen de vue se fait le matin, de 8h30 à 13h00.",
             "Write on WhatsApp before coming: we tell you whether an appointment is needed, and when to come. Eye examinations are in the morning, from 8:30 to 13:00."),
        ]),
        ("Les montures et les verres", "Frames and lenses", [
            ("Comment choisir une monture qui va à mon visage ?",
             "How do I choose a frame that suits my face?",
             "On essaie. La forme du visage guide la forme de la monture, la largeur décide de l'appui sur le nez et derrière les oreilles, et une photo ne dit ni l'un ni l'autre. C'est pour ça que le choix se fait au cabinet, devant un miroir.",
             "You try them on. Face shape guides the shape of the frame, width decides how it sits on the nose and behind the ears, and a photo tells you neither. That is why the choice is made at the practice, in front of a mirror."),
            ("Mes verres correcteurs peuvent-ils aller dans cette monture ?",
             "Can my prescription lenses go into this frame?",
             "Presque toujours, mais la taille du cercle compte : une monture trop grande décentre le verre, et la correction n'est plus la même au centre. On regarde la monture avec votre ordonnance avant de commander.",
             "Almost always, but the size of the rim matters: a frame that is too big decentres the lens, and the correction is no longer the same at the centre. We look at the frame together with your prescription before ordering."),
            ("Les lunettes de soleil peuvent-elles être à ma vue ?",
             "Can sunglasses be made to my prescription?",
             "Oui. Le verre teinté se monte à votre correction, pour conduire ou travailler dehors. Dites ce que vous faites au soleil : la teinte et la catégorie du verre se choisissent là-dessus.",
             "Yes. Tinted lenses can be made to your prescription, for driving or working outdoors. Tell us what you do in the sun: the tint and the lens category are chosen from that."),
            ("Adaptez-vous des lentilles de contact ?",
             "Do you fit contact lenses?",
             "Oui, avec un suivi. Apportez votre ordonnance de lentilles si vous en avez une. Ce n'est pas la solution de tout le monde : on vous dit au cabinet si votre correction s'y prête.",
             "Yes, with follow-up. Bring your contact lens prescription if you have one. It is not right for everyone: we tell you at the practice whether your correction suits it."),
            ("Quelle est la différence entre un opticien, un optométriste et un ophtalmologue ?",
             "What is the difference between an optician, an optometrist and an ophthalmologist?",
             "L'ophtalmologue est le médecin spécialiste de l'œil : il traite les maladies et opère. L'opticien-optométriste mesure la vue et conçoit l'équipement qui la corrige, et c'est le titre que la loi camerounaise donne au diplômé qui a les deux formations, et celui de M. Domche Noumbi, inscrit à l'ONOC sous le numéro 021/2016.",
             "The ophthalmologist is the medical specialist of the eye: they treat disease and operate. The optometrist optician measures sight and designs the equipment that corrects it, and that is the title Cameroonian law gives to the graduate with both trainings, and the one held by Mr Domche Noumbi, registered with the ONOC under number 021/2016."),
            ("Est-ce que vous vendez des marques ?",
             "Do you sell brands?",
             "Nous ne publions aucune liste de marques : une marque annoncée est une marque qu'il faut avoir. Demandez celle que vous cherchez sur WhatsApp, la réponse vous dit si elle est en boutique.",
             "We publish no list of brands: an announced brand is a brand you have to stock. Ask about the one you are looking for on WhatsApp, and the answer tells you whether it is in store."),
        ]),
        ("La réparation", "Repairs", [
            ("Ma monture est cassée : est-ce réparable ?",
             "My frame is broken: can it be repaired?",
             "Souvent, mais pas toujours : certaines soudures et certaines charnières intégrées ne se refont pas. Envoyez une photo sur WhatsApp : la réponse vous dit si c'est réparable, et si le déplacement en vaut la peine.",
             "Often, but not always: some metal joints and some integrated hinges cannot be redone. Send a photo on WhatsApp: the answer tells you whether it can be repaired, and whether the trip is worth it."),
            ("Faut-il réparer ou remplacer ?",
             "Should I repair or replace?",
             "Trois cas. La vis, la plaquette, le réglage : c'est une réparation, et elle règle la plupart des problèmes. La monture déformée ou la branche tordue : ça se redresse, tant que le métal n'a pas cassé. La monture cassée net, ou dont la charnière est arrachée : on regarde, et on vous dit franchement si c'est fini.",
             "Three cases. A screw, a nose pad, an adjustment: that is a repair, and it fixes most problems. A bent frame or twisted temple: it can be straightened, as long as the metal has not snapped. A frame broken clean through, or with a torn-out hinge: we look at it and tell you plainly if it is finished."),
            ("Puis-je la réparer moi-même ?",
             "Can I repair it myself?",
             "Une vis se resserre avec un tournevis d'horloger, et c'est utile à savoir. Le reste, non : une branche se tord à froid et casse, la colle ne tient pas sur une charnière, et une monture forcée se déforme sans revenir. C'est là que le passage au cabinet évite d'aggraver.",
             "A screw can be tightened with a watchmaker's screwdriver, and that is worth knowing. The rest, no: a temple bent cold snaps, glue does not hold a hinge, and a frame forced back goes out of shape for good. That is where coming to the practice stops it getting worse."),
        ]),
        ("Le prix, l'assurance, le paiement", "Price, insurance, payment", [
            ("Combien coûte une paire de lunettes ?",
             "How much do a pair of glasses cost?",
             "Il n'y a pas de prix unique, et nous n'en publions pas : un verre correcteur ne coûte pas la même chose selon la correction, et une monture selon le modèle. Le prix se demande sur WhatsApp, avec votre ordonnance ou la monture qui vous plaît, ou au cabinet.",
             "There is no single price, and we do not publish one: a corrective lens does not cost the same depending on the correction, and a frame depending on the model. You ask for the price on WhatsApp, with your prescription or the frame you like, or at the practice."),
            ("Acceptez-vous mon assurance ?",
             "Do you accept my insurance?",
             "Nous travaillons avec Belife Insurance, Willis Towers Watson et Groupe Activa, et le dossier de prise en charge se monte avec vous. Ce qui est couvert dépend de votre police, pas de nous : apportez votre carte d'assuré et votre ordonnance.",
             "We work with Belife Insurance, Willis Towers Watson and Groupe Activa, and the claim file is put together with you. What is covered depends on your policy, not on us: bring your insurance card and your prescription."),
            ("Et si je n'ai pas d'assurance ?",
             "What if I have no insurance?",
             "Vous payez au cabinet, comme tout le monde : espèces, Mobile Money, ou en plusieurs fois. L'absence d'assurance ne change ni l'examen ni le conseil.",
             "You pay at the practice, like everyone else: cash, Mobile Money, or in instalments. Having no insurance changes neither the examination nor the advice."),
            ("Peut-on payer en plusieurs fois ?",
             "Can I pay in instalments?",
             "Oui, le paiement en plusieurs fois est possible, et la livraison aussi. Les modalités se voient au cabinet, sur le devis, avant la commande.",
             "Yes, payment in instalments is possible, and so is delivery. The terms are agreed at the practice, on the quote, before the order."),
        ]),
        ("Venir au cabinet", "Coming to the practice", [
            ("Où se trouve le cabinet, exactement ?",
             "Where exactly is the practice?",
             "À Bonabéri, quartier Ndobo Mayor, immeuble West Hotel, 1er étage, dernière porte à droite. Le repère est l'enseigne « Consultation » au-dessus de l'entrée.",
             "In Bonaberi, Ndobo Mayor district, West Hotel building, first floor, last door on the right. The landmark is the “Consultation” sign above the entrance."),
            ("Quels sont les horaires ?",
             "What are the opening hours?",
             "Lundi – Samedi. L'examen de vue se fait de 8h30 à 13h00 ; pour les montures, les verres et la réparation, le cabinet est ouvert de 8h30 à 17h30.",
             "Monday – Saturday. Eye examinations run from 8:30 to 13:00; for frames, lenses and repairs the practice is open from 8:30 to 17:30."),
            ("Comment prendre rendez-vous ?",
             "How do I book?",
             "Un message sur WhatsApp, avec ce dont vous avez besoin : vue qui a changé, ordonnance à monter, monture à réparer. Le message part déjà écrit, vous pouvez le modifier avant de l'envoyer. Le téléphone reste possible : 656 122 239.",
             "One WhatsApp message, with what you need: a change in your sight, a prescription to fill, a frame to repair. The message is already written, and you can edit it before sending. The phone still works: 656 122 239."),
        ]),
    ]

    def qa_html():
        parts = []
        for fr_theme, en_theme, items in QA:
            parts.append(f'<h2 class="rv">{B(fr_theme, en_theme)}</h2><dl class="v2-qa">')
            for q_fr, q_en, a_fr, a_en in items:
                parts.append(f'<div class="rv"><dt>{B(q_fr, q_en)}</dt>'
                             f'<dd>{B(a_fr, a_en)}</dd></div>')
            parts.append("</dl>")
        return chr(10).join(parts)

    qa_ld = {"@type": "FAQPage", "@id": site.abs("/questions/") + "#faq",
             "mainEntity": [{"@type": "Question", "name": q_fr,
                             "acceptedAnswer": {"@type": "Answer", "text": a_fr}}
                            for _, _, items in QA for q_fr, _, a_fr, _ in items]}
    n_qa = len(qa_ld["mainEntity"])
    # Le miroir anglais porte le MÊME schéma, dans la langue de sa page : sans ça, /en/questions/
    # déclare 22 questions françaises, et le texte balisé n'est pas celui que le visiteur lit.
    qa_ld_en = {"@type": "FAQPage", "@id": site.abs("/questions/") + "#faq",
                "mainEntity": [{"@type": "Question", "name": q_en,
                                "acceptedAnswer": {"@type": "Answer", "text": a_en}}
                               for _, _, items in QA for _, q_en, _, a_en in items]}

    questions_main = f'''<section class="wrap">
    {site.crumbs([(B("Accueil", "Home"), "/"), (B("Questions", "Questions"), None)])}
    <h1 class="rv">{B("Les questions qu'on nous pose au cabinet", "The questions we are asked at the practice")}</h1>
    <p class="lede rv">{B("Vingt-deux questions, et pour chacune la réponse en première phrase. Si la vôtre n'y est pas, écrivez sur WhatsApp : c'est souvent plus rapide qu'un moteur de recherche.", "Twenty-two questions, each answered in its first sentence. If yours is not here, write on WhatsApp: that is often faster than a search engine.")}</p>
    {qa_html()}
    <div class="actions rv">
      {wa_btn(VISIT_WA[0], VISIT_WA[1], "Poser ma question sur WhatsApp", "Ask my question on WhatsApp")}
      <a class="btn" href="{TEL}">{B("Appeler le 656 122 239", "Call 656 122 239")}</a>
    </div>
    <p class="note">{B("Ce que cette page ne dit pas : ni prix, ni délai, ni marque. Non par discrétion, mais parce qu'aucun des trois ne se résume honnêtement en une phrase valable pour tout le monde.", "What this page does not say: no prices, no lead times, no brands. Not out of discretion, but because none of the three can honestly be summed up in one sentence that holds for everyone.")}</p>
  </section>'''
    written.append(site.page(
        "/questions/", "Questions sur l'examen de vue, les montures et la r\u00e9paration \u2014 DM OPTIQUE SARL",
        "Vingt-deux questions pos\u00e9es au cabinet DM OPTIQUE SARL \u00e0 Bonab\u00e9ri (Douala) : ordonnance, dur\u00e9e, r\u00e9paration, assurances, paiement, adresse.",
        questions_main, ld_graph=[site.crumb_ld([("Accueil", "/"), ("Questions", "/questions/")]), qa_ld],
        dock_wa=VISIT_WA, ld_en=[qa_ld_en],
        en_meta=("Questions about eye examinations, frames and repairs \u2014 DM OPTIQUE SARL",
                 "Twenty-two questions asked at the DM OPTIQUE SARL practice in Bonaberi (Douala): prescription, duration, repairs, insurance, payment, address.")))

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

    # ── Miroir anglais ──────────────────────────────────────────────────────────────────────────
    en_pages = []                      # (chemin EN, titre anglais) — sert aussi à llms.txt
    for path, en_title, en_desc in site.pairs:
        fr_file = OUTDIR / path.strip("/") / "index.html"
        if not fr_file.exists():
            sys.exit("miroir : page française absente — " + str(fr_file))
        page_html = fr_file.read_text(encoding="utf-8")
        target = OUTDIR / en_path(path).strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(to_en(page_html, path, en_title, en_desc, site.base,
                                site.ld_en.get(path, ())), encoding="utf-8")
        en_pages.append((en_path(path), en_title))
    if site.base:
        print(f"  miroir /en/ : {len(site.pairs)} pages")
    else:
        print("! pas de domaine connu : miroir /en/ non écrit")

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
        "/verres-sur-ordonnance/": ("Verres sur ordonnance — ordonnance, monture, montage, ajustement", "Prescription lenses — prescription, frame, fitting, adjustment"),
        "/reparation-et-entretien/": ("Réparation et entretien — vis, plaquettes, branches, réglage", "Repairs and adjustments — screws, nose pads, temples, fitting"),
        "/le-cabinet/": ("Le cabinet — l'équipement et l'adresse", "The practice — equipment and address"),
        "/contact/": ("Contact — adresse, horaires, WhatsApp", "Contact — address, hours, WhatsApp"),
        "/questions/": ("Questions — 22 réponses sur l'examen, les montures, la réparation, l'assurance et le rendez-vous",
                        "Questions — 22 answers on the examination, frames, repairs, insurance and booking"),
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
    # 28/10 : le fichier ne listait que le français. Or les 48 pages anglaises existent, et la porte
    # de livraison (D4) exige que tout ce qui est dans le sitemap soit dans llms.txt. On les liste.
    llms += ["", "## Coordonnées",
             f"- Adresse : {ADDRESS_FR}",
             "- Téléphone et WhatsApp : +237 656 122 239",
             "- Horaires : Lundi–Samedi, 8h30–17h30 · examen de la vue 8h30–13h00",
             "- Langues : français et anglais sur toutes les pages · version anglaise : https://dmoptiquesarl.com/en/", ""]
    if en_pages:
        CORE_EN = ["/en/contact/", "/en/examen-de-vue/", "/en/", "/en/le-cabinet/", "/en/montures/"]
        core = [(u, t) for u, t in en_pages if u in CORE_EN]
        core.sort(key=lambda x: CORE_EN.index(x[0]))
        fiches_en = sorted((u, t) for u, t in en_pages if u not in CORE_EN)
        llms += ["## English pages", "",
                 'Mirror of the French pages, for agents that read English. Each page declares its '
                 'alternate in `<link rel="alternate" hreflang="en">`.', "", "### Sections", ""]
        llms += [f"- [{t}]({site.abs(u)})" for u, t in core]
        llms += ["", f"### Frame pages ({len(fiches_en)})", ""]
        llms += [f"- [{t}]({site.abs(u)})" for u, t in fiches_en]
    llms_txt = chr(10).join(llms)
    n_links = llms_txt.count("](https://dmoptiquesarl.com")
    # 28/10 : le total ne s'écrit plus en dur. Chaque page française écrite est listée une fois,
    # et chaque page anglaise une fois — 48 était un chiffre qui cassait à la première page ajoutée.
    attendu = len(site.paths) + len(en_pages)
    if n_links != attendu or "+237 656 122 239" not in llms_txt or "FCFA" in llms_txt \
            or any(b in llms_txt for b in ("Ray-Ban", "Oakley", "Gucci", "Essilor", "Zeiss", "NIDEK", "HP")):
        sys.exit(f"llms.txt incohérent : {n_links} liens (attendu {attendu}), verrous à vérifier")
    (OUTDIR / "llms.txt").write_text(llms_txt, encoding="utf-8")
    print(f"  llms.txt : {n_links} liens, {len(llms_txt)} caractères")

    # ── Sitemap ─────────────────────────────────────────────────────────────────
    if site.base:
        # lastmod : date de dernière modification réelle des sources de contenu (pas la date du jour,
        # qui serait fausse — Google ignore un lastmod qui ne bouge jamais, ou qui bouge toujours).
        stamps = [FRAMES, FRAMES_EN, ROOT / "demos/dmoptic-v1.tpl.html"]
        lastmod = max(datetime.date.fromtimestamp(t.stat().st_mtime) for t in stamps if t.exists()).isoformat()
        all_paths = [p for p in site.paths if p not in site.noindex] + \
                    [en_path(p) for p, _, _ in site.pairs if p not in site.noindex]
        urls = "".join(f"  <url><loc>{esc(site.abs(p))}</loc><lastmod>{lastmod}</lastmod></url>\n" for p in all_paths)
        (OUTDIR / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
            encoding="utf-8")
    else:
        print("! pas d'adresse canonique dans l'accueil : sitemap non régénéré")

    print(f"ok: {len(written)} pages v2 ({len(frames)} montures) · "
          f"sitemap {len([p for p in site.paths if p not in site.noindex])} URL FR + "
          f"{len([p for p, _, _ in site.pairs if p not in site.noindex])} EN · "
          f"noindex {len(site.noindex)}")


if __name__ == "__main__":
    main()
