#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — génère les deux pages service (règle 3 du playbook SEO : une page par service).

**Pourquoi ce script existe.** Ces deux pages ont été écrites le 21/09 puis **perdues au 13ᵉ
recul du bac à sable** — leur push avait échoué (jeton GitHub intermittent). Une page qui
n'existe que sous forme de fichier est fragile ; **une page qui se régénère en une commande
ne l'est pas.** Si elles disparaissent encore :

    python3 tools/site/build_service_pages.py

**Contenu, et d'où il vient.** Chaque page cible un métier et une requête :
  · `creation-site-web-ecole-cameroun.html`   → « création de site web pour école au Cameroun »
  · `creation-site-web-clinique-cameroun.html` → « création de site web pour clinique au Cameroun »

**Ce que chaque page porte :** titre + description en français avec la ville · **une seule H1**
portant le mot-clé · 6 cartes de contenu réel · la preuve cliquable · **le prix affiché** ·
la FAQ avec le prix en question n°1 · les quartiers et villes · un lien vers l'autre page.
**Données structurées :** `Service` + `provider` relié par `@id` au `ProfessionalService`
de l'accueil + `Offer` chiffré + `FAQPage` + `BreadcrumbList`.

**Règle de contraste apprise en les écrivant :** le vert vif `#10B981` ne porte JAMAIS de texte
blanc (≈1.8:1). Il est réservé aux **coches**, sur fond sombre. Les boutons prennent le vert
foncé `--green-btn:#0B7A3E`.
"""
import pathlib
import sys

OUT = pathlib.Path("site")

# ── Le pied de page, partagé (NAP identique à la fiche Google — facteur #15 : exactement pareil)
FOOTER = """
<footer>
  <div class="wrap">
    <div class="f-grid">
      <div>
        <div style="display:flex;align-items:center;gap:10px">
          <svg viewBox="0 0 64 64" width="34" height="34" aria-hidden="true">{LOGO}</svg>
          <span style="color:#fff;font-weight:800">AMK</span>
        </div>
        <p class="nap" style="margin-top:14px" data-en="AMK – Web Development &amp; Digital Solutions" data-fr="AMK – Développement Web &amp; Solutions Digitales">AMK – Développement Web &amp; Solutions Digitales</p>
        <p style="margin-top:8px" data-en="Websites for schools, clinics and laboratories in Cameroon. Bilingual, mobile-first, WhatsApp-ready." data-fr="Des sites web pour les écoles, cliniques et laboratoires au Cameroun. Bilingues, mobile d'abord, prêts pour WhatsApp.">Des sites web pour les écoles, cliniques et laboratoires au Cameroun. Bilingues, mobile d'abord, prêts pour WhatsApp.</p>
        <p style="margin-top:12px"><a href="tel:+237677789631" style="display:inline">+237 677 789 631</a> · <a href="mailto:akwo.king.dev@gmail.com" style="display:inline">akwo.king.dev@gmail.com</a></p>
        <p style="margin-top:6px" data-en="Douala, Littoral, Cameroon" data-fr="Douala, Littoral, Cameroun">Douala, Littoral, Cameroun</p>
      </div>
      <div>
        <h5 data-en="Pages" data-fr="Pages">Pages</h5>
        <a href="index.html" data-en="Home" data-fr="Accueil">Accueil</a>
        <a href="creation-site-web-ecole-cameroun.html" data-en="Website for schools" data-fr="Site web pour école">Site web pour école</a>
        <a href="creation-site-web-clinique-cameroun.html" data-en="Website for clinics" data-fr="Site web pour clinique">Site web pour clinique</a>
      </div>
      <div>
        <h5 data-en="See our work" data-fr="Voir notre travail">Voir notre travail</h5>
        {SEE_WORK}
      </div>
    </div>
    <p style="margin-top:30px;font-size:13.5px;color:#94A3B8" data-en="© 2026 AMK – Web Development &amp; Digital Solutions · Douala, Cameroon. Prices in FCFA. Names and figures shown in concept sites are placeholders." data-fr="© 2026 AMK – Développement Web &amp; Solutions Digitales · Douala, Cameroun. Prix en FCFA. Les noms et chiffres des sites concepts sont des exemples.">© 2026 AMK – Développement Web &amp; Solutions Digitales · Douala, Cameroun. Prix en FCFA. Les noms et chiffres des sites concepts sont des exemples.</p>
  </div>
</footer>

<div class="pad-b"></div>
<div class="mbar">
  <a class="b1" href="tel:+237677789631" data-en="Call" data-fr="Appeler">Appeler</a>
  <a class="b2" href="https://wa.me/237677789631?text={WA_PREFILL}">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.4A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1-.4-.1-1-.3-1.8-.7-2.2-1-3.6-3.3-3.7-3.5-.1-.1-.9-1.2-.9-2.3s.6-1.6.8-1.9c.2-.2.4-.3.6-.3h.5c.2 0 .4 0 .5.4l.7 1.7c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.2.3-.1.5.1.2.6 1 1.2 1.6.8.7 1.4.9 1.6 1 .2.1.4.1.5 0l.7-.8c.2-.2.4-.2.6-.1l1.6.8c.3.2.4.3.4.5Z"/></svg>
    <span data-en="Free 24h preview" data-fr="Aperçu gratuit 24h">Aperçu gratuit 24h</span>
  </a>
</div>

<script>
function setLang(l){
  document.documentElement.lang = l;
  document.querySelectorAll("[data-en]").forEach(function(el){
    var v = (l === "fr") ? el.getAttribute("data-fr") : el.getAttribute("data-en");
    if (v !== null && v !== undefined) el.innerHTML = v;
  });
  var bf = document.getElementById("btn-fr"), be = document.getElementById("btn-en");
  if (bf) bf.classList.toggle("on", l === "fr");
  if (be) be.classList.toggle("on", l === "en");
  try{ localStorage.setItem("amk-lang", l); }catch(e){}
}
(function(){
  try{ var s = localStorage.getItem("amk-lang"); if (s) setLang(s); }catch(e){}
})();
</script>
</body>
</html>
"""

LOGO = '<rect width="64" height="64" rx="14" fill="#1E293B"/><circle cx="32" cy="30" r="17" fill="none" stroke="#F59E0B" stroke-width="2.4"/><path d="M32 16v28M32 30L18 44M32 30l14 14" stroke="#FCD34D" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="16" r="3" fill="#F59E0B"/><circle cx="18" cy="44" r="3" fill="#F59E0B"/><circle cx="46" cy="44" r="3" fill="#F59E0B"/>'

# ── Le CSS, partagé par les deux pages (identique au site, pour que rien ne dépayŝe)
CSS = """
:root{
  --navy:#0F172A; --navy2:#1E293B; --navy3:#334155; --navy4:#0B1120;
  --amber:#F59E0B; --amber-l:#FCD34D; --amber-t:#FFFBEB;
  --green:#10B981; --green-btn:#0B7A3E; --green-d:#04211D;
  --bg:#F8FAFC; --white:#fff; --border:#E2E8F0;
  --ink:#0F172A; --slate:#64748B; --slate-l:#94A3B8;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--white);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
section{padding:78px 0;scroll-margin-top:84px}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.kicker{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#B45309;background:var(--amber-t);border:1px solid #FDE68A;padding:6px 14px;border-radius:99px;margin-bottom:18px}
.kicker.on-dark{background:rgba(245,158,11,.16);border-color:rgba(245,158,11,.42);color:var(--amber-l)}
h1{font-size:clamp(30px,5vw,50px);line-height:1.14;letter-spacing:-.02em;font-weight:800}
h2{font-size:clamp(24px,3.4vw,36px);line-height:1.2;letter-spacing:-.02em;font-weight:800}
h3{font-size:19px;font-weight:700;line-height:1.3}
.sub{font-size:17px;color:var(--slate);max-width:680px}
.center{text-align:center}
.center .sub{margin:0 auto}
em{font-style:normal;color:var(--amber)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:15px 26px;border-radius:99px;font-weight:700;font-size:15.5px;border:1.6px solid transparent;cursor:pointer;min-height:52px}
.btn-amber{background:var(--amber);color:#0B1120}
.btn-ghost{background:transparent;color:var(--ink);border-color:var(--border)}
.btn-hero{background:transparent;color:#FFFFFF;border-color:rgba(255,255,255,.42)}
.btn-wa{background:var(--green-btn);color:#fff}
.btn svg{width:19px;height:19px;fill:currentColor;flex:none}
#hdr{position:sticky;top:0;z-index:60;background:rgba(15,23,42,.97);backdrop-filter:blur(10px)}
#hdr .h-in{display:flex;align-items:center;gap:20px;min-height:70px}
#hdr .brand{display:flex;align-items:center;gap:10px}
#hdr .brand svg{width:38px;height:38px;flex:none}
#hdr .brand .t{color:#fff;font-weight:800;font-size:16px;letter-spacing:.02em;display:flex;flex-direction:column;line-height:1.15}
#hdr .brand .t small{font-weight:500;font-size:10.5px;color:#94A3B8;letter-spacing:.03em}
#hdr nav.main{display:none;gap:24px;margin-left:auto}
#hdr nav.main a{color:#CBD5E1;font-size:14.5px;font-weight:500}
#hdr nav.main a:hover{color:#fff}
.lang-sw{display:flex;gap:2px;background:rgba(255,255,255,.1);border-radius:99px;padding:3px;margin-left:auto}
.lang-sw button{border:0;background:transparent;color:#CBD5E1;font:700 12.5px inherit;padding:6px 11px;border-radius:99px;cursor:pointer}
.lang-sw button.on{background:var(--amber);color:#0B1120}
.h-cta{display:none}
@media(min-width:820px){#hdr nav.main{display:flex}.lang-sw{margin-left:0}.h-cta{display:inline-flex;padding:12px 20px;font-size:14.5px}}
.hero{background:linear-gradient(160deg,var(--navy4),var(--navy2));color:#fff;padding:64px 0 86px;position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-140px;top:-140px;width:460px;height:460px;border-radius:50%;background:radial-gradient(circle,rgba(245,158,11,.18),transparent 70%)}
.hero .wrap{position:relative;z-index:2}
.hero h1{color:#fff;max-width:19em;margin-top:6px}
.hero .sub{color:#CBD5E1;margin-top:18px}
.hero .cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.hero .trust{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:24px;font-size:14.5px;color:#94A3B8}
.hero .trust b{color:#fff;font-weight:600}
.facts{background:var(--navy);color:#fff}
.facts .wrap{display:grid;gap:20px;padding:30px 24px}
@media(min-width:760px){.facts .wrap{grid-template-columns:repeat(3,1fr)}}
.facts .n{font-size:27px;font-weight:800;color:var(--amber-l)}
.facts .l{font-size:14.5px;color:#94A3B8;margin-top:4px}
.cards{display:grid;gap:16px;margin-top:34px}
@media(min-width:640px){.cards{grid-template-columns:repeat(2,1fr)}}
@media(min-width:980px){.cards{grid-template-columns:repeat(3,1fr)}}
.card{background:var(--white);border:1px solid var(--border);border-radius:18px;padding:24px}
.card p{color:var(--slate);font-size:15px;margin-top:8px}
.card .fache{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#B45309;margin-bottom:10px}
.proofs{display:grid;gap:18px;margin-top:34px}
@media(min-width:760px){.proofs{grid-template-columns:repeat(3,1fr)}}
.proof{background:var(--white);border:1px solid var(--border);border-radius:18px;overflow:hidden}
.proof img{aspect-ratio:16/10;object-fit:cover;width:100%}
.proof .b{padding:16px 18px}
.proof h3{font-size:16px}
.proof p{color:var(--slate);font-size:14px;margin-top:4px}
.proof a{display:inline-block;margin-top:10px;font-size:14px;font-weight:700;color:#B45309}
.price{background:var(--navy);color:#fff}
.price .box{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:22px;padding:34px;max-width:720px;margin:0 auto;text-align:center}
.price .amount{font-size:clamp(34px,6vw,50px);font-weight:800;color:var(--amber)}
.price .split{color:#CBD5E1;margin-top:6px}
.price ul{list-style:none;text-align:left;max-width:480px;margin:26px auto 0;display:grid;gap:11px}
.price li{position:relative;padding-left:28px;color:#E2E8F0;font-size:15.5px}
.price li::before{content:"✓";position:absolute;left:0;color:var(--green);font-weight:800}
.price .not{color:#94A3B8;font-size:14px;margin-top:20px}
.qa{max-width:820px;margin:36px auto 0}
details{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:17px 20px;margin-top:12px}
summary{cursor:pointer;font-weight:700;font-size:16.5px;list-style:none}
summary::-webkit-details-marker{display:none}
summary::after{content:"＋";float:right;color:var(--slate);font-weight:400}
details[open] summary::after{content:"－"}
details .ans,.ans{color:var(--slate);font-size:15.5px;margin-top:12px;line-height:1.7}
.zones{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.zone{background:var(--bg);border:1px solid var(--border);border-radius:99px;padding:7px 14px;font-size:14px;color:var(--navy3)}
.xnav{background:var(--bg);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.xnav .wrap{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;padding:22px 24px}
.xnav a{font-weight:700;color:#B45309}
footer{background:var(--navy4);color:#94A3B8;font-size:14.5px;padding:52px 0 34px}
footer .f-grid{display:grid;gap:28px;margin-top:26px}
@media(min-width:760px){footer .f-grid{grid-template-columns:2fr 1fr 1fr}}
footer h5{color:#fff;font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}
footer a{display:block;margin-top:8px;color:#CBD5E1}
footer a:hover{color:#fff}
footer .nap{color:#E2E8F0}
.mbar{position:fixed;left:12px;right:12px;bottom:12px;z-index:120;display:flex;gap:10px}
.mbar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;border-radius:14px;padding:15px;font-weight:700;font-size:14.5px;min-height:52px;box-shadow:0 10px 26px rgba(15,23,42,.24)}
.mbar .b1{background:#fff;color:var(--ink);border:1px solid var(--border)}
.mbar .b2{background:var(--amber);color:#0B1120}
.mbar svg{width:17px;height:17px;fill:currentColor}
@media(min-width:760px){.mbar{display:none}}
.pad-b{padding-bottom:88px}
@media(min-width:760px){.pad-b{padding-bottom:0}}
.wasvg{width:19px;height:19px;fill:currentColor;flex:none}
:is(a,button,summary):focus-visible{outline:3px solid var(--amber);outline-offset:2px;border-radius:10px}
"""

WA_PATH = '<path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.4A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1-.4-.1-1-.3-1.8-.7-2.2-1-3.6-3.3-3.7-3.5-.1-.1-.9-1.2-.9-2.3s.6-1.6.8-1.9c.2-.2.4-.3.6-.3h.5c.2 0 .4 0 .5.4l.7 1.7c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.2.3-.1.5.1.2.6 1 1.2 1.6.8.7 1.4.9 1.6 1 .2.1.4.1.5 0l.7-.8c.2-.2.4-.2.6-.1l1.6.8c.3.2.4.3.4.5Z"/>'


def head(title, desc, canonical, og_title, og_desc, schema_blocks):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://amk-cm.vercel.app/{canonical}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#0F172A">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:site_name" content="AMK">
<meta property="og:image" content="https://amk-cm.vercel.app/img/og-cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://amk-cm.vercel.app/{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://amk-cm.vercel.app/img/og-cover.jpg">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
{schema_blocks}
<style>{CSS}</style>
</head>
<body>
<header id="hdr">
  <div class="wrap h-in">
    <a class="brand" href="index.html" aria-label="AMK">
      <svg viewBox="0 0 64 64" aria-hidden="true">{LOGO}</svg>
      <span class="t">AMK<small data-en="Web Development &amp; Digital Solutions" data-fr="Développement Web &amp; Solutions Digitales">Développement Web &amp; Solutions Digitales</small></span>
    </a>
    <nav class="main">
      <a href="index.html" data-en="Home" data-fr="Accueil">Accueil</a>
"""


def hero(kicker_fr, kicker_en, h1_fr, h1_en, sub_fr, sub_en, wa,
         cta1_fr, cta1_en, cta2_fr, cta2_en, t1f, t1e, t2f, t2e, t3f, t3e):
    return f"""<section class="hero" id="top">
  <div class="wrap">
    <div class="center"><span class="kicker" data-en="{kicker_en}" data-fr="{kicker_fr}">{kicker_fr}</span></div>
    <h1 data-en="{h1_en}" data-fr="{h1_fr}">{h1_fr}</h1>
    <p class="sub" data-en="{sub_en}" data-fr="{sub_fr}">{sub_fr}</p>
    <div class="cta-row">
      <a class="btn btn-wa" href="https://wa.me/237677789631?text={wa}">
        <svg class="wasvg" viewBox="0 0 24 24" aria-hidden="true">{WA_PATH}</svg>
        <span data-en="Get my free preview" data-fr="Recevoir mon aperçu gratuit">Recevoir mon aperçu gratuit</span>
      </a>
      <a class="btn btn-hero" href="#proof" data-en="{cta2_en}" data-fr="{cta2_fr}">{cta2_fr}</a>
    </div>
    <div class="trust">
      <span data-en="<b>No payment</b> before you approve" data-fr="<b>Aucun paiement</b> avant votre accord"><b>Aucun paiement</b> avant votre accord</span>
      <span data-en="{t2e}" data-fr="{t2f}">{t2f}</span>
      <span data-en="{t3e}" data-fr="{t3f}">{t3f}</span>
    </div>
  </div>
</section>

<div class="facts">
  <div class="wrap">
    <div><div class="n">24 h</div><div class="l" data-en="for your free homepage preview — no payment, no commitment" data-fr="pour votre aperçu gratuit d'accueil — sans paiement, sans engagement">pour votre aperçu gratuit d'accueil — sans paiement, sans engagement</div></div>
    <div><div class="n" data-en="3–5 days" data-fr="3–5 jours">3–5 jours</div><div class="l" data-en="from your approval to the site being live" data-fr="entre votre validation et la mise en ligne">entre votre validation et la mise en ligne</div></div>
    <div><div class="n" data-en="{t1e}" data-fr="{t1f}">{t1f}</div><div class="l" data-en="{t2e}" data-fr="{t2f}">{t2f}</div></div>
  </div>
</div>
"""


def price_block(items_fr, items_en, wa):
    lis = "\n".join(f'        <li data-en="{en}" data-fr="{fr}">{fr}</li>' for fr, en in zip(items_fr, items_en))
    return f"""
<section class="price">
  <div class="wrap">
    <div class="box">
      <span class="kicker on-dark" data-en="One price, no surprises" data-fr="Un seul prix, sans surprise">Un seul prix, sans surprise</span>
      <div class="amount">100 000 FCFA</div>
      <p class="split" data-en="Or 50/50 — 50,000 FCFA to start, 50,000 FCFA at launch." data-fr="Ou 50/50 — 50 000 FCFA pour commencer, 50 000 FCFA à la mise en ligne.">Ou 50/50 — 50 000 FCFA pour commencer, 50 000 FCFA à la mise en ligne.</p>
      <ul>
{lis}
      </ul>
      <p class="not" data-en="Not included, and said plainly: new pages beyond the first (quoted separately), and writing your content for you. Your domain and files stay 100% yours — always." data-fr="Non inclus, et dit franchement : les pages supplémentaires au-delà de la première (devis séparé), et la rédaction de vos contenus à votre place. Votre domaine et vos fichiers restent à 100 % à vous — toujours.">Non inclus, et dit franchement : les pages supplémentaires au-delà de la première (devis séparé), et la rédaction de vos contenus à votre place. Votre domaine et vos fichiers restent à 100 % à vous — toujours.</p>
      <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:28px">
        <a class="btn btn-amber" href="https://wa.me/237677789631?text={wa}" data-en="Start with the free preview" data-fr="Commencer par l'aperçu gratuit">Commencer par l'aperçu gratuit</a>
      </div>
    </div>
  </div>
</section>
"""


def faq_block(pairs):
    out = ['<section class="faq" id="faq" style="background:var(--bg)">',
           '  <div class="wrap">',
           '    <div class="center"><span class="kicker">FAQ</span>',
           '      <h2 data-en="Asked before, answered honestly" data-fr="Posé avant, répondu honnêtement">Posé avant, répondu honnêtement</h2></div>',
           '    <div class="qa">']
    for fr_q, en_q, fr_a, en_a in pairs:
        out.append(f'      <details><summary data-en="{en_q}" data-fr="{fr_q}">{fr_q}</summary>'
                   f'<div class="ans" data-en="{en_a}" data-fr="{fr_a}">{fr_a}</div></details>')
    out += ['    </div>', '  </div>', '</section>', '']
    return "\n".join(out)


def zones(names):
    return ('    <div class="zones">\n      '
            + "\n      ".join(f'<span class="zone">{n}</span>' for n in names)
            + '\n    </div>')


def schema(json_text):
    return f'<script type="application/ld+json">\n{json_text}\n</script>'


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — ÉCOLE
# ══════════════════════════════════════════════════════════════════════════════
WA_ECOLE = "Bonjour%20AMK%2C%20je%20souhaite%20un%20site%20pour%20mon%20%C3%A9cole."

SERVICE_ECOLE = """{
 "@context": "https://schema.org",
 "@type": "Service",
 "name": "Création de site web pour école au Cameroun",
 "serviceType": "Création de site internet pour établissement scolaire",
 "url": "https://amk-cm.vercel.app/creation-site-web-ecole-cameroun.html",
 "provider": {
  "@type": "ProfessionalService",
  "@id": "https://amk-cm.vercel.app/#amk",
  "name": "AMK – Développement Web & Solutions Digitales",
  "telephone": "+237677789631",
  "email": "akwo.king.dev@gmail.com",
  "priceRange": "100000 FCFA",
  "address": {"@type": "PostalAddress", "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM"}
 },
 "areaServed": [
  {"@type": "City", "name": "Douala"}, {"@type": "City", "name": "Yaoundé"},
  {"@type": "City", "name": "Buea"}, {"@type": "City", "name": "Limbe"},
  {"@type": "City", "name": "Bafoussam"}, {"@type": "City", "name": "Bamenda"}
 ],
 "audience": {"@type": "Audience", "audienceType": "Écoles privées, collèges, lycées et écoles maternelles au Cameroun"},
 "offers": {"@type": "Offer", "price": "100000", "priceCurrency": "XAF",
  "description": "Site bilingue FR|EN d'une page pour école privée, en ligne en 3 à 5 jours. La moitié à la commande, la moitié à la mise en ligne."},
 "availableLanguage": ["fr", "en"]
}"""

FAQ_ECOLE_LD = """{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
  {"@type":"Question","name":"Combien coûte un site web pour une école au Cameroun ?",
   "acceptedAnswer":{"@type":"Answer","text":"100 000 FCFA pour la formule fondatrice — un site bilingue français-anglais complet, en ligne en 3 à 5 jours, avec le domaine, l'hébergement et 30 minutes de formation de votre personnel. La moitié pour commencer, la moitié à la mise en ligne. Rien n'est dû avant votre accord sur l'aperçu gratuit."}},
  {"@type":"Question","name":"Que met-on sur le site d'une école ?",
   "acceptedAnswer":{"@type":"Answer","text":"Ce que les parents cherchent : les classes et les âges, les frais de scolarité en FCFA, la liste des fournitures et de l'uniforme, le calendrier et les dates d'inscription, les résultats aux examens, l'adresse avec un plan, et un bouton WhatsApp sur chaque écran."}},
  {"@type":"Question","name":"Faut-il payer quelque chose avant de voir le résultat ?",
   "acceptedAnswer":{"@type":"Answer","text":"Non. L'aperçu est gratuit et arrive sur votre téléphone sous 24 heures. Vous le regardez avec votre équipe, on corrige, et vous ne payez que si vous validez."}},
  {"@type":"Question","name":"Mon personnel n'est pas technique. Pourra-t-il mettre le site à jour ?",
   "acceptedAnswer":{"@type":"Answer","text":"Oui — c'est prévu pour ça. Nous concevons pour du personnel non technique, nous faisons une formation de 30 minutes et nous restons joignables sur WhatsApp."}},
  {"@type":"Question","name":"Travaillez-vous en dehors de Douala ?",
   "acceptedAnswer":{"@type":"Answer","text":"Oui, entièrement à distance partout au Cameroun : Yaoundé, Buea, Limbé, Bafoussam, Bamenda, Garoua. Tout se passe sur WhatsApp."}}
 ]
}"""

BREADCRUMB_ECOLE = """{
 "@context": "https://schema.org",
 "@type": "BreadcrumbList",
 "itemListElement": [
  {"@type":"ListItem","position":1,"name":"Accueil","item":"https://amk-cm.vercel.app/"},
  {"@type":"ListItem","position":2,"name":"Site web pour école","item":"https://amk-cm.vercel.app/creation-site-web-ecole-cameroun.html"}
 ]
}"""

CARDS_ECOLE = [
 ("1 · Classes", "1 · Classes", "Quelles classes, quels âges", "Which classes, which ages",
  "Maternelle, primaire, secondaire — les âges et les sections que vous ouvrez réellement. Un parent obligé d'appeler pour le savoir appelle l'école suivante.",
  "Nursery, primary, secondary — the ages and the sections you actually open. A parent who has to call to learn this calls the next school instead."),
 ("2 · Frais", "2 · Fees", "Les frais de scolarité en FCFA, bien visibles", "School fees in FCFA, in plain sight",
  "Inscription, scolarité, uniforme, transport — les montants et ce qu'ils couvrent. Des frais cachés vous coûtent les parents sérieux, qui vont se renseigner ailleurs.",
  "Registration, tuition, uniform, transport — the amounts and what they cover. Hidden fees cost you the serious parents, who ask around instead."),
 ("3 · Inscriptions", "3 · Admissions", "Comment s'inscrire, étape par étape", "How to register, step by step",
  "Les dates, les documents à apporter, et un bouton WhatsApp qui s'ouvre avec le message déjà écrit. Rien à imprimer, rien à perdre.",
  "The dates, the documents to bring, and a WhatsApp button that opens with the message already written. Nothing to print, nothing to lose."),
 ("4 · Résultats", "4 · Results", "Vos résultats GCE, sur votre propre page", "Your GCE results, on your own page",
  "Si vos résultats sont bons, ils sont aujourd'hui enterrés dans un PDF publié par le ministère. Ils ont leur place sur la première page de votre propre site, avec l'année.",
  "If your results are good, they are buried today in a PDF the ministry published. They belong on the front of your own site, with the year."),
 ("5 · Adresse", "5 · Location", "Où vous êtes, avec un repère", "Where you are, with a landmark",
  "Un nom et un quartier ne sont pas un itinéraire. Le repère que tout le quartier connaît, plus un lien qui ouvre Google Maps en un clic.",
  "A name and a quarter are not directions. The landmark everyone in the neighbourhood knows, plus a link that opens Google Maps in one tap."),
 ("6 · WhatsApp", "6 · WhatsApp", "Un bouton question sur chaque écran", "A question button on every screen",
  "Les parents ne remplissent pas de formulaires sur un téléphone. Ils envoient un message. Chaque bouton de votre site ouvre WhatsApp, avec leur question déjà commencée.",
  "Parents don't fill in forms on a phone. They send a message. Every button on your site opens WhatsApp, with their question already started."),
]

FAQ_ECOLE = [
 ("Combien coûte un site web pour une école au Cameroun ?", "How much does a school website cost in Cameroon?",
  "100 000 FCFA pour la formule fondatrice — un site bilingue complet, en ligne en 3 à 5 jours, avec le domaine, l'hébergement et 30 minutes de formation de votre personnel. La moitié pour commencer, la moitié à la mise en ligne, et rien du tout avant votre accord sur l'aperçu gratuit. Le domaine et les fichiers restent à 100 % à vous.",
  "100,000 FCFA for the founding package — a complete bilingual site, live in 3–5 days, with domain, hosting and 30 minutes of staff training. Half to start, half at launch, and nothing at all until you approve the free preview. The domain and files stay 100% yours."),
 ("Que met-on sur le site d'une école ?", "What goes on a school website?",
  "Ce que les parents cherchent : les classes et les âges, les frais de scolarité en FCFA, la liste des fournitures et de l'uniforme, le calendrier et les dates d'inscription, les résultats aux examens, l'adresse avec un plan, et un bouton WhatsApp sur chaque écran.",
  "What parents are looking for: the classes and ages, school fees in FCFA, the list of supplies and uniform, the calendar and registration dates, exam results, the address with a map, and a WhatsApp button on every screen."),
 ("Est-ce que je paie quelque chose avant de voir le résultat ?", "Do I pay anything before seeing the result?",
  "Non. L'aperçu est gratuit et arrive dans votre téléphone sous 24 heures. Vous le regardez avec votre équipe, on corrige, et vous ne payez que si vous validez.",
  "No. The preview is free and arrives on your phone within 24 hours. You look at it with your team, we correct it, and you only pay if you approve."),
 ("Mon personnel n'est pas technique. Peut-il mettre le site à jour ?", "My staff aren't technical. Can they update the site?",
  "Oui — c'est conçu pour ça. Nous faisons une formation de 30 minutes et restons joignables sur WhatsApp. Actualités, photos, événements : votre équipe s'en charge.",
  "Yes — that's what it's designed for. We run a 30-minute training and stay reachable on WhatsApp. News, photos, events: your team handles it."),
 ("Travaillez-vous en dehors de Douala ?", "Do you work outside Douala?",
  "Oui — entièrement à distance, partout au Cameroun. Yaoundé, Buea, Limbe, Bafoussam, Bamenda, Garoua. Tout se passe sur WhatsApp : je vous envoie l'aperçu, vous m'envoyez votre logo et vos frais, et on corrige ensemble.",
  "Yes — entirely remotely, anywhere in Cameroon. Yaoundé, Buea, Limbe, Bafoussam, Bamenda, Garoua. Everything happens on WhatsApp: I send the preview, you send your logo and your fees, and we correct together."),
]


def cards_block(cards):
    out = ['    <div class="cards">']
    for fache_fr, fache_en, h_fr, h_en, p_fr, p_en in cards:
        out.append(f'      <div class="card"><span class="fache" data-en="{fache_en}" data-fr="{fache_fr}">{fache_fr}</span>'
                   f'<h3 data-en="{h_en}" data-fr="{h_fr}">{h_fr}</h3>'
                   f'<p data-en="{p_en}" data-fr="{p_fr}">{p_fr}</p></div>')
    out.append('    </div>')
    return "\n".join(out)


def proofs_block(items):
    out = ['    <div class="proofs">']
    for img, alt, h_fr, h_en, p_fr, p_en, href, l_fr, l_en in items:
        out.append(f"""      <div class="proof">
        <img src="{img}" alt="{alt}" loading="lazy" decoding="async">
        <div class="b">
          <h3 data-en="{h_en}" data-fr="{h_fr}">{h_fr}</h3>
          <p data-en="{p_en}" data-fr="{p_fr}">{p_fr}</p>
          <a href="{href}" data-en="{l_en}" data-fr="{l_fr}">{l_fr}</a>
        </div>
      </div>""")
    out.append('    </div>')
    return "\n".join(out)


def build(name, page_html):
    (OUT / name).write_text(page_html, encoding="utf-8")
    return len(page_html)



# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — CLINIQUE & LABORATOIRE
# ══════════════════════════════════════════════════════════════════════════════
WA_CLINIQUE = "Bonjour%20AMK%2C%20je%20souhaite%20un%20site%20pour%20ma%20clinique."

SERVICE_CLINIQUE = """{
 "@context": "https://schema.org",
 "@type": "Service",
 "name": "Création de site web pour clinique et laboratoire au Cameroun",
 "serviceType": "Création de site internet pour établissement de santé",
 "url": "https://amk-cm.vercel.app/creation-site-web-clinique-cameroun.html",
 "provider": {
  "@type": "ProfessionalService",
  "@id": "https://amk-cm.vercel.app/#amk",
  "name": "AMK – Développement Web & Solutions Digitales",
  "telephone": "+237677789631",
  "email": "akwo.king.dev@gmail.com",
  "priceRange": "100000 FCFA",
  "address": {"@type": "PostalAddress", "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM"}
 },
 "areaServed": [
  {"@type": "City", "name": "Douala"}, {"@type": "City", "name": "Yaoundé"},
  {"@type": "City", "name": "Buea"}, {"@type": "City", "name": "Limbe"},
  {"@type": "City", "name": "Bafoussam"}, {"@type": "City", "name": "Bamenda"}
 ],
 "audience": {"@type": "Audience", "audienceType": "Cliniques, cabinets médicaux, laboratoires d'analyses, centres d'imagerie et opticiens au Cameroun"},
 "offers": {"@type": "Offer", "price": "100000", "priceCurrency": "XAF",
  "description": "Site bilingue FR|EN avec prise de rendez-vous sur WhatsApp, en ligne en 3 à 5 jours. La moitié à la commande, la moitié à la mise en ligne."},
 "availableLanguage": ["fr", "en"]
}"""

FAQ_CLINIQUE_LD = """{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
  {"@type":"Question","name":"Combien coûte un site web pour une clinique au Cameroun ?",
   "acceptedAnswer":{"@type":"Answer","text":"100 000 FCFA pour la formule fondatrice — un site bilingue français-anglais complet, en ligne en 3 à 5 jours, avec le domaine, l'hébergement et 30 minutes de formation de votre personnel. Rien n'est dû avant votre accord sur l'aperçu gratuit."}},
  {"@type":"Question","name":"Que met-on sur le site d'une clinique ou d'un laboratoire ?",
   "acceptedAnswer":{"@type":"Answer","text":"Ce que le patient cherche : les services et spécialités réellement disponibles, la préparation des examens (à jeun ou pas, ce qu'il faut apporter), les horaires, l'adresse avec un repère connu du quartier, et un bouton WhatsApp pour prendre rendez-vous sur chaque écran."}},
  {"@type":"Question","name":"Peut-on prendre les rendez-vous sur WhatsApp au lieu du téléphone ?",
   "acceptedAnswer":{"@type":"Answer","text":"Oui, et c'est ce qui fonctionne le mieux au Cameroun : le patient écrit au lieu d'appeler, souvent en dehors des heures d'ouverture, et le message arrive avec sa question déjà rédigée."}},
  {"@type":"Question","name":"Afficher mes tarifs en FCFA, est-ce obligatoire ?",
   "acceptedAnswer":{"@type":"Answer","text":"Non, mais c'est ce qui filtre les appels : un patient qui voit le tarif ne vous appelle que s'il est décidé. Vous décidez ce qui est affiché."}},
  {"@type":"Question","name":"Travaillez-vous avec des laboratoires et des opticiens aussi ?",
   "acceptedAnswer":{"@type":"Answer","text":"Oui. Laboratoires d'analyses, centres d'imagerie, cabinets dentaires et opticiens. Pour un laboratoire, la page la plus utile est celle des examens et de leur préparation."}}
 ]
}"""

BREADCRUMB_CLINIQUE = """{
 "@context": "https://schema.org",
 "@type": "BreadcrumbList",
 "itemListElement": [
  {"@type":"ListItem","position":1,"name":"Accueil","item":"https://amk-cm.vercel.app/"},
  {"@type":"ListItem","position":2,"name":"Site web pour clinique","item":"https://amk-cm.vercel.app/creation-site-web-clinique-cameroun.html"}
 ]
}"""

CARDS_CLINIQUE = [
 ("1 · Services", "1 · Services", "Ce que vous faites vraiment", "What you actually do",
  "Les spécialités et les examens que vous faites réellement — pas la liste de tout ce qu'un hôpital pourrait faire. Un patient qui vient pour un examen que vous ne faites pas ne revient pas.",
  "The specialties and exams you really offer — not a list of everything a hospital could do."),
 ("2 · Préparation", "2 · Preparation", "À jeun ou pas, et quoi apporter", "Fasting or not, and what to bring",
  "La question que vous répondez au téléphone toute la journée. Écrite une fois, elle cesse d'être un appel — et elle évite le patient qui arrive en ayant mangé.",
  "The question you answer on the phone all day. Written once, it stops being a phone call."),
 ("3 · Tarifs", "3 · Fees", "Vos tarifs en FCFA, ou ceux que vous choisissez", "Your fees in FCFA, or the ones you choose",
  "Affichez le tarif de consultation et les examens courants, ou n'affichez rien et dites-le. Ce qui fait perdre un patient, c'est le silence : il imagine le pire et va ailleurs.",
  "Show the consultation fee and the common tests, or show nothing and say so. Silence loses patients."),
 ("4 · Résultats", "4 · Results", "Quand et comment les résultats arrivent", "When and how results come back",
  "Prévenu sur WhatsApp quand c'est prêt, retiré au laboratoire — au lieu de revenir trois fois demander. Dites le délai avant qu'il se déplace.",
  "Told on WhatsApp when it's ready, collected at the lab — instead of coming back three times to ask."),
 ("5 · Adresse", "5 · Location", "Où vous êtes, avec un repère", "Where you are, with a landmark",
  "Sur des axes comme Deido-Bassa, un nom et un quartier ne sont pas un itinéraire. Le repère que tout le monde connaît, plus un lien qui ouvre Maps en un clic.",
  "On roads like Deido-Bassa, a name and a quarter are not directions. The landmark everyone knows."),
 ("6 · WhatsApp", "6 · WhatsApp", "Des rendez-vous sans appel téléphonique", "Appointments without a phone call",
  "Les patients écrivent au lieu d'appeler, souvent en dehors de vos horaires. Chaque bouton ouvre WhatsApp avec leur message déjà écrit.",
  "Patients write instead of calling, often outside your hours. Every button opens WhatsApp with the message written."),
]

FAQ_CLINIQUE = [
 ("Combien coûte un site web pour une clinique au Cameroun ?", "How much does a clinic website cost in Cameroon?",
  "100 000 FCFA pour la formule fondatrice — un site bilingue complet, en ligne en 3 à 5 jours, avec le domaine, l'hébergement et 30 minutes de formation de votre personnel. La moitié pour commencer, la moitié à la mise en ligne, et rien du tout avant votre accord sur l'aperçu gratuit.",
  "100,000 FCFA for the founding package — a complete bilingual site, live in 3–5 days, with domain, hosting and 30 minutes of staff training."),
 ("Les rendez-vous peuvent-ils passer par WhatsApp au lieu du téléphone ?", "Can appointments go through WhatsApp instead of the phone?",
  "Oui, et c'est ce qui marche le mieux au Cameroun : le patient écrit au lieu d'appeler, souvent en dehors de vos heures d'ouverture, et le message arrive avec la question déjà rédigée.",
  "Yes, and it's what works best in Cameroon: the patient writes instead of calling, often outside your hours."),
 ("Suis-je obligé de publier mes tarifs ?", "Do I have to publish my fees?",
  "Non — mais ça filtre vos appels. Un patient qui voit le tarif n'appelle que s'il est décidé, et vous passez moins de temps au téléphone à expliquer les mêmes prix. Vous décidez ce qui est affiché et ce qui est dit en consultation.",
  "No — but it filters your calls. A patient who sees the fee only calls when he's decided."),
 ("Travaillez-vous aussi avec des laboratoires et des opticiens ?", "Do you also work with laboratories and opticians?",
  "Oui. Laboratoires d'analyses, centres d'imagerie, cabinets dentaires et opticiens. Pour un laboratoire, la page la plus utile est celle des examens et de leur préparation — c'est la question qu'on vous pose au téléphone toute la journée.",
  "Yes. Analysis laboratories, imaging centres, dental cabinets and opticians. For a laboratory, the most useful page lists the tests and how to prepare."),
 ("Travaillez-vous en dehors de Douala ?", "Do you work outside Douala?",
  "Oui — entièrement à distance, partout au Cameroun. Yaoundé, Buea, Limbe, Bafoussam, Bamenda, Garoua. Tout se passe sur WhatsApp : je vous envoie l'aperçu, vous m'envoyez votre logo et vos services, et on corrige ensemble.",
  "Yes — entirely remotely, anywhere in Cameroon. Yaoundé, Buea, Limbe, Bafoussam, Bamenda, Garoua."),
]


def build_clinique():
    c = head(
        "Création de site web pour clinique et laboratoire au Cameroun | AMK Douala",
        "Création de site web pour cliniques, cabinets médicaux et laboratoires d'analyses au Cameroun : rendez-vous sur WhatsApp, examens et préparations expliqués, prix en FCFA. 100 000 FCFA, en ligne en 3–5 jours.",
        "creation-site-web-clinique-cameroun.html",
        "Création de site web pour clinique et laboratoire au Cameroun | AMK",
        "Vos patients vous trouvent, voient vos tarifs en FCFA et prennent rendez-vous sur WhatsApp. 100 000 FCFA, live en 3–5 jours.",
        "\n".join([schema(SERVICE_CLINIQUE), schema(FAQ_CLINIQUE_LD), schema(BREADCRUMB_CLINIQUE)]),
    )
    nav = (
        '      <a href="creation-site-web-ecole-cameroun.html" data-en="For schools" data-fr="Pour les écoles">Pour les écoles</a>\n'
        '      <a href="index.html#pricing" data-en="Pricing" data-fr="Tarif">Tarif</a>\n'
        '      <a href="#faq">FAQ</a>\n'
        '    </nav>\n'
        '    <div class="lang-sw">\n'
        '      <button id="btn-fr" class="on" onclick="setLang(\'fr\')">FR</button>\n'
        '      <button id="btn-en" onclick="setLang(\'en\')">EN</button>\n'
        '    </div>\n'
        '    <a href="https://wa.me/237677789631?text=' + WA_CLINIQUE + '" class="btn btn-amber h-cta" data-en="Free 24h preview" data-fr="Aperçu gratuit 24h">Aperçu gratuit 24h</a>\n'
        '  </div>\n'
        '</header>\n\n'
    )
    c += nav
    c += hero(
        "Sites pour cliniques & labos · Cameroun", "Websites for clinics & labs · Cameroon",
        "Un site web pour votre clinique ou laboratoire — pour que les patients vous trouvent avant d'appeler ailleurs.",
        "A website for your clinic or laboratory — so patients find you before they call someone else.",
        "Les rendez-vous sur WhatsApp, vos examens et leur préparation expliqués, vos tarifs en FCFA. En ligne en 3 à 5 jours pour 100 000 FCFA — et l'aperçu gratuit est dans votre téléphone sous 24 heures.",
        "Appointments on WhatsApp, your tests and their preparation explained, your fees in FCFA. Live in 3–5 days for 100,000 FCFA.",
        WA_CLINIQUE,
        "Recevoir mon aperçu gratuit", "Get my free preview",
        "Voir d'abord un vrai site de clinique", "See a real clinic site first",
        "WhatsApp", "WhatsApp",
        "<b>Bilingue</b> FR|EN inclus", "<b>Bilingual</b> EN|FR included",
        "<b>En ligne en 3–5 jours</b>", "<b>Live in 3–5 days</b>",
    )
    c += """
<section>
  <div class="wrap">
    <span class="kicker" data-en="What patients actually look for" data-fr="Ce que les patients cherchent vraiment">Ce que les patients cherchent vraiment</span>
    <h2 data-en="What goes on a clinic or laboratory website" data-fr="Ce qu'on met sur le site d'une clinique ou d'un laboratoire">Ce qu'on met sur le site d'une clinique ou d'un laboratoire</h2>
    <p class="sub" data-en="A patient searching at eleven at night on a phone is not reading a brochure. He wants six answers, fast." data-fr="Un patient qui cherche à onze heures du soir sur son téléphone ne lit pas une brochure. Il veut six réponses, vite.">Un patient qui cherche à onze heures du soir sur son téléphone ne lit pas une brochure. Il veut six réponses, vite.</p>
""" + cards_block(CARDS_CLINIQUE) + """
  </div>
</section>

<section id="proof" style="background:var(--bg)">
  <div class="wrap">
    <span class="kicker" data-en="Proof, honestly" data-fr="Preuve, honnêtement">Preuve, honnêtement</span>
    <h2 data-en="Open a real clinic site right now" data-fr="Ouvrez un vrai site de clinique maintenant">Ouvrez un vrai site de clinique maintenant</h2>
    <p class="sub" data-en="Not screenshots. Complete concept sites, live, that you can open on your phone this minute." data-fr="Pas des captures d'écran. Des sites concepts complets, en ligne, que vous pouvez ouvrir sur votre téléphone à l'instant.">Pas des captures d'écran. Des sites concepts complets, en ligne, que vous pouvez ouvrir sur votre téléphone à l'instant.</p>
""" + proofs_block([
        ("img/clinic.png", "Exemple de site pour clinique et laboratoire — accueil patient",
         "Clinique & laboratoire", "Clinic & laboratory",
         "Tarifs en FCFA bien visibles, six services, labo le jour même, échographies de maternité, ligne d'urgence, rendez-vous sur WhatsApp.",
         "Fees in FCFA in plain sight, six services, same-day lab, maternity scans, emergency line, booking on WhatsApp.",
         "clinic-bonaberi.html", "Ouvrir le site →", "Open the site →"),
        ("img/nova.png", "Exemple de site bilingue — les deux langues à un clic",
         "Bilingue, les deux langues à un clic", "Bilingual, both languages one click apart",
         "Le Cameroun a deux langues officielles et la plupart des sites de cliniques n'en ont qu'une. Le vôtre en aura deux — inclus, jamais en supplément.",
         "Cameroon has two official languages and most clinic sites have one. Yours will have both.",
         "index.html#work", "Voir tous les concepts →", "See all the concepts →"),
    ]) + """
  </div>
</section>
""" + price_block([
        "Une page complète bilingue (français et anglais, à un clic l'un de l'autre)",
        "Vos services, vos tarifs en FCFA, les consignes de préparation, l'adresse et le plan",
        "Des boutons de rendez-vous qui ouvrent WhatsApp avec le message écrit",
        "Le domaine et l'hébergement sécurisé installés pour vous",
        "30 minutes de formation pour votre accueil et un mois de support",
        "Aucune donnée médicale collectée par le site — les informations du patient restent en consultation",
    ], [
        "A complete bilingual page (French and English, one click apart)",
        "Your services, your fees in FCFA, prep instructions, address and map",
        "Appointment buttons that open WhatsApp with the message written",
        "Domain and secure hosting set up for you",
        "30 minutes of training for your front desk and one month of support",
        "No medical data collected by the site — patient information stays in your consultation room",
    ], WA_CLINIQUE) + """
<section>
  <div class="wrap">
    <span class="kicker" data-en="Where we work" data-fr="Où nous travaillons">Où nous travaillons</span>
    <h2 data-en="Clinics and laboratories we build for, city by city" data-fr="Les cliniques et laboratoires pour lesquels nous construisons, ville par ville">Les cliniques et laboratoires pour lesquels nous construisons, ville par ville</h2>
    <p class="sub" data-en="Entirely remote — everything happens on WhatsApp." data-fr="Entièrement à distance — tout se passe sur WhatsApp.">Entièrement à distance — tout se passe sur WhatsApp.</p>
""" + zones(["Douala — Akwa", "Bonapriso", "Bonanjo", "Bonamoussadi", "Bali", "Deido", "Bonabéri",
             "Bessengue", "Makepe", "Logbessou", "Yassa", "Yaoundé", "Bastos", "Mvog-Mbi",
             "Buea — Molyko", "Bonduma", "Limbe", "Bafoussam", "Bamenda", "Garoua"]) + """
  </div>
</section>
""" + faq_block(FAQ_CLINIQUE) + """
<div class="xnav">
  <div class="wrap">
    <span data-en="You run a school or a college?" data-fr="Vous dirigez une école ou un collège ?">Vous dirigez une école ou un collège ?</span>
    <a href="creation-site-web-ecole-cameroun.html" data-en="See the school website page →" data-fr="Voir la page site web pour école →">Voir la page site web pour école →</a>
  </div>
</div>
""" + FOOTER.replace("{LOGO}", LOGO).replace("{WA_PREFILL}", WA_CLINIQUE).replace(
        "{SEE_WORK}",
        '<a href="clinic-bonaberi.html" data-en="Clinic &amp; laboratory" data-fr="Clinique &amp; laboratoire">Clinique &amp; laboratoire</a>\n'
        '        <a href="sample-school.html" data-en="Bilingual academy" data-fr="Académie bilingue">Académie bilingue</a>\n'
        '        <a href="sample-nursery.html" data-en="Nursery &amp; primary" data-fr="Maternelle &amp; primaire">Maternelle &amp; primaire</a>\n'
        '        <a href="sample-secondary.html" data-en="Secondary — GCE" data-fr="Secondaire — GCE">Secondaire — GCE</a>')
    return build("creation-site-web-clinique-cameroun.html", c)


def main() -> int:
    OUT.mkdir(exist_ok=True)
    written = []

    # ───────────────────────── PAGE ÉCOLE ─────────────────────────
    ecole = head(
        "Création de site web pour école au Cameroun — écoles privées | AMK Douala",
        "Création de site web pour écoles privées au Cameroun : page bilingue FR|EN, frais de scolarité en FCFA, inscriptions sur WhatsApp. 100 000 FCFA, en ligne en 3–5 jours. Aperçu gratuit en 24 h.",
        "creation-site-web-ecole-cameroun.html",
        "Création de site web pour école au Cameroun | AMK",
        "Un site bilingue pour votre école : frais en FCFA, inscriptions sur WhatsApp, trouvable sur Google. 100 000 FCFA, live en 3–5 jours.",
        "\n".join([schema(SERVICE_ECOLE), schema(FAQ_ECOLE_LD), schema(BREADCRUMB_ECOLE)]),
    )
    ecole += """      <a href="creation-site-web-clinique-cameroun.html" data-en="For clinics" data-fr="Pour les cliniques">Pour les cliniques</a>
      <a href="index.html#pricing" data-en="Pricing" data-fr="Tarif">Tarif</a>
      <a href="#faq">FAQ</a>
    </nav>
    <div class="lang-sw">
      <button id="btn-fr" class="on" onclick="setLang('fr')">FR</button>
      <button id="btn-en" onclick="setLang('en')">EN</button>
    </div>
    <a href="https://wa.me/237677789631?text=""" + WA_ECOLE + """" class="btn btn-amber h-cta" data-en="Free 24h preview" data-fr="Aperçu gratuit 24h">Aperçu gratuit 24h</a>
  </div>
</header>

"""
    ecole += hero(
        "Site web pour écoles · Cameroun", "Website for schools · Cameroon",
        "Un site web pour votre école — pour que les parents vous trouvent sur Google, pas seulement sur Facebook.",
        "A website for your school — so parents find you on Google, not just on Facebook.",
        "Bilingue FR|EN, les frais de scolarité en FCFA, les inscriptions sur WhatsApp. En ligne en 3 à 5 jours pour 100 000 FCFA — et l'aperçu gratuit est dans votre téléphone sous 24 heures.",
        "Bilingual FR|EN, school fees in FCFA, admissions on WhatsApp. Live in 3–5 days for 100,000 FCFA — and the free preview is on your phone within 24 hours.",
        WA_ECOLE,
        "Recevoir mon aperçu gratuit", "Get my free preview",
        "Voir d'abord un vrai site d'école", "See a real school site first",
        "2 langues", "2 languages",
        "<b>Bilingue</b> FR|EN inclus", "<b>Bilingual</b> EN|FR included",
        "<b>En ligne en 3–5 jours</b>", "<b>Live in 3–5 days</b>",
    )
    ecole += """
<section>
  <div class="wrap">
    <span class="kicker" data-en="What parents actually look for" data-fr="Ce que les parents cherchent vraiment">Ce que les parents cherchent vraiment</span>
    <h2 data-en="What goes on a school website" data-fr="Ce qu'on met sur le site d'une école">Ce qu'on met sur le site d'une école</h2>
    <p class="sub" data-en="Not a brochure. The six things a parent opens your site to find — written so they find them in ten seconds." data-fr="Pas une brochure. Les six choses qu'un parent ouvre votre site pour trouver — écrites pour qu'il les trouve en dix secondes.">Pas une brochure. Les six choses qu'un parent ouvre votre site pour trouver — écrites pour qu'il les trouve en dix secondes.</p>
""" + cards_block(CARDS_ECOLE) + """
  </div>
</section>

<section id="proof" style="background:var(--bg)">
  <div class="wrap">
    <span class="kicker" data-en="Proof, honestly" data-fr="Preuve, honnêtement">Preuve, honnêtement</span>
    <h2 data-en="Open a real school site right now" data-fr="Ouvrez un vrai site d'école maintenant">Ouvrez un vrai site d'école maintenant</h2>
    <p class="sub" data-en="Not screenshots. Three complete concept sites, live, that you can open on your phone this minute. Every name and figure in them is a placeholder we replace with yours in 24 hours." data-fr="Pas des captures d'écran. Trois sites concepts complets, en ligne, que vous pouvez ouvrir sur votre téléphone à l'instant. Tous les noms et chiffres sont des exemples qu'on remplace par les vôtres en 24 heures.">Pas des captures d'écran. Trois sites concepts complets, en ligne, que vous pouvez ouvrir sur votre téléphone à l'instant. Tous les noms et chiffres sont des exemples qu'on remplace par les vôtres en 24 heures.</p>
""" + proofs_block([
        ("img/nova.png", "Exemple de site d'école bilingue — page d'accueil",
         "Académie bilingue", "Bilingual academy",
         "Parcours portes ouvertes, espace parents, onglets de programmes, étapes d'inscription.",
         "Open-house funnel, parent quick hub, curriculum tabs, admissions steps.",
         "sample-school.html", "Ouvrir le site →", "Open the site →"),
        ("img/littleoaks.png", "Exemple de site pour école maternelle et primaire",
         "Maternelle & primaire", "Nursery & primary",
         "Chaleureux, classes par âge et un espace parents qui répond avant l'appel.",
         "Friendly, warm, age-group classrooms and a parent hub that answers before they call.",
         "sample-nursery.html", "Ouvrir le site →", "Open the site →"),
        ("img/crestwood.png", "Exemple de site de collège et lycée avec résultats GCE",
         "Secondaire — GCE O/A Level", "Secondary — GCE O/A Level",
         "Programmes GCE, externat et internat, frais en FCFA, inscriptions sur WhatsApp.",
         "GCE programmes, day and boarding, fees in FCFA, admissions on WhatsApp.",
         "sample-secondary.html", "Ouvrir le site →", "Open the site →"),
    ]) + """
  </div>
</section>
""" + price_block([
        "Une page complète bilingue (français et anglais, à un clic l'un de l'autre)",
        "Les frais en FCFA, les étapes d'inscription, le contact et le plan",
        "Un bouton WhatsApp sur chaque écran",
        "Le domaine et l'hébergement sécurisé installés pour vous",
        "30 minutes de formation de votre personnel et un mois de support gratuit",
        "Rapide en 3G — la majorité de vos parents sont en données mobiles",
    ], [
        "A complete bilingual page (French and English, one click apart)",
        "School fees in FCFA, admissions steps, contact and map",
        "A WhatsApp button on every screen",
        "Domain and secure hosting set up for you",
        "30 minutes of staff training and one month of free support",
        "Fast on 3G — most of your parents are on mobile data",
    ], WA_ECOLE) + """
<section>
  <div class="wrap">
    <span class="kicker" data-en="Where we work" data-fr="Où nous travaillons">Où nous travaillons</span>
    <h2 data-en="Schools we build for, city by city" data-fr="Les écoles pour lesquelles nous construisons, ville par ville">Les écoles pour lesquelles nous construisons, ville par ville</h2>
    <p class="sub" data-en="We work entirely remotely — everything happens on WhatsApp. Your logo and your fees, sent by message; corrections made the same day." data-fr="Nous travaillons entièrement à distance — tout se passe sur WhatsApp. Votre logo et vos frais, envoyés par message ; les corrections faites le jour même.">Nous travaillons entièrement à distance — tout se passe sur WhatsApp. Votre logo et vos frais, envoyés par message ; corrections faites le jour même.</p>
""" + zones(["Douala — Akwa", "Bonapriso", "Bonamoussadi", "Bali", "Deido", "Bonabéri", "Makepe",
             "Bépanda", "Logbessou", "Yaoundé", "Bastos", "Mvog-Mbi", "Ngousso",
             "Buea — Molyko", "Bonduma", "Great Soppo", "Muea", "Limbe — New Town",
             "Bota", "Bafoussam", "Bamenda", "Garoua"]) + """
  </div>
</section>
""" + faq_block(FAQ_ECOLE) + """
<div class="xnav">
  <div class="wrap">
    <span data-en="You run a clinic or a laboratory?" data-fr="Vous dirigez une clinique ou un laboratoire ?">Vous dirigez une clinique ou un laboratoire ?</span>
    <a href="creation-site-web-clinique-cameroun.html" data-en="See the clinic website page →" data-fr="Voir la page site web pour clinique →">Voir la page site web pour clinique →</a>
  </div>
</div>
""" + FOOTER.replace("{LOGO}", LOGO).replace("{WA_PREFILL}", WA_ECOLE).replace("{SEE_WORK}",
    '<a href="sample-school.html" data-en="Bilingual academy" data-fr="Académie bilingue">Académie bilingue</a>\n'
    '        <a href="sample-nursery.html" data-en="Nursery &amp; primary" data-fr="Maternelle &amp; primaire">Maternelle &amp; primaire</a>\n'
    '        <a href="sample-secondary.html" data-en="Secondary — GCE" data-fr="Secondaire — GCE">Secondaire — GCE</a>\n'
    '        <a href="clinic-bonaberi.html" data-en="Clinic &amp; laboratory" data-fr="Clinique &amp; laboratoire">Clinique &amp; laboratoire</a>')
    written.append(("creation-site-web-ecole-cameroun.html", build("creation-site-web-ecole-cameroun.html", ecole)))
    written.append(("creation-site-web-clinique-cameroun.html", build_clinique()))

    for n, size in written:
        print(f"  ✓ {n}  ({size//1024} Ko)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
