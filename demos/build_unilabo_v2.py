# -*- coding: utf-8 -*-
"""UNI-LABO v2 — refonte de zéro, ordinateur ET téléphone conçus ensemble.

    python3 demos/build_unilabo_v2.py      →  demos/concept-unilabo-v2.html

POURQUOI CETTE REFONTE (King, 23/09/2026, captures d'anresco.com à l'appui) :
« the page isn't mobile friendly the pictures seem to have spoiled everything redesign the site from
scratch », avec deux inspirations : **anresco.com** et **animate.bio**.

Ce que les deux références ont en commun, et ce qu'on leur prend :
  · ANRESCO — un laboratoire : ses sections sont **portées par ses analyses** (une famille = une image,
    un titre, une phrase), son hero est sombre et **typographique**, ses preuves sont des listes, son
    pied de page est un vrai sommaire. On prend : la section d'analyses en tuiles, le hero sombre,
    la densité maîtrisée, le pied de page. On NE prend PAS : le texte posé sur les photos (illisible
    sur un téléphone en plein soleil), les sept familles (nous en avons quatre), le jaune.
  · ANIMATE.BIO — beaucoup de blanc, un titre énorme, des étiquettes minuscules, des sections qui
    respirent, aucune décoration. On prend : le blanc, l'échelle des titres, le rythme.
  · ET LES TROIS VIDÉOS MOBILES (lot [25], `AMK-DESIGN-SKILLS.md` §24) : le téléphone est conçu
    D'ABORD — une colonne par défaut, tout ce qui est en colonnes ne l'est qu'à partir de 760 px,
    le texte grossit sur petit écran, les boutons font 52-56 px, chaque image a une variante légère.

LA RÈGLE DE CETTE PAGE, tenue de bout en bout : **au plus cinq photographies**, jamais derrière du texte,
chacune **porteuse d'un sens** (les quatre familles d'analyses, plus la préparation à la maison), et
chacune légendée « mise en situation ». Là où la v1 posait une image, la v2 pose une phrase ou une ligne
de fiche. C'est la correction directe de « the pictures seem to have spoiled everything ».
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "demos"))
from _unilabo_v2_content import (LAB, HERO, FICHE, JOURNEY, FAMILIES, PREP, PREP_ALWAYS,
                                 RESULTATS, LIEU, FAQ, FAM_GROUPS, MOMENTS, FOOT)

OUT = os.path.join(ROOT, "demos", "concept-unilabo-v2.html")
JS_MAIN = io.open(os.path.join(ROOT, "demos", "_unilabo_v2_js_main.js"), encoding="utf-8").read()
JS_FORM = io.open(os.path.join(ROOT, "demos", "_unilabo_v2_js_form.js"), encoding="utf-8").read()

def bi(fr, en):
    """Les deux langues, dans les trois endroits qu'exige §20.8 (le nœud visible étant le français)."""
    return '<span class="fr-only">%s</span><span class="en-only">%s</span>' % (fr, en)

def wa(msg_fr, msg_en=None):
    """Un lien WhatsApp à message pré-rempli — le français par défaut, l'anglais si le visiteur l'a choisi."""
    import urllib.parse
    return "%s?text=%s" % (LAB["wa"], urllib.parse.quote(msg_fr))

# ══════════════════════════════════════════════════════════════════════════════════════════════════
# LA FEUILLE DE STYLE — écrite pour le téléphone, étendue au bureau
# ══════════════════════════════════════════════════════════════════════════════════════════════════
CSS = """
:root{
  --paper:#FFFFFF; --soft:#F5F6F8; --ink:#14151A; --ink-2:#2A2C33; --mute:#5A6170;
  --mute-on-ink:#C3C8D2; --line:rgba(20,21,26,.12); --line-2:rgba(20,21,26,.07);
  --signal:#5B21B6; --signal-2:#7C3AED; --tint:#F1ECFE; --wa:#0B7A3E; --err:#B42318;
  --r:18px; --max:1140px; --gut:20px;
  --f-display:"Sora",system-ui,sans-serif; --f-body:"Public Sans",system-ui,-apple-system,sans-serif;
  /* l'échelle : dix pas, pas plus (§13). Le corps grossit sur téléphone (MALEWICZ pt.5). */
  --fs-h1:clamp(2.1rem,8.2vw,4rem);
  --fs-h2:clamp(1.5rem,5.4vw,2.4rem);
  --fs-h3:clamp(1.12rem,3.4vw,1.35rem);
  --fs-lead:clamp(1.02rem,2.7vw,1.2rem);
  --fs-base:1.0625rem; --fs-sm:.94rem; --fs-xs:.85rem; --fs-label:.72rem; --fs-btn:.97rem;
  --ease:cubic-bezier(.23,1,.32,1);
}
@media (min-width:760px){ :root{--fs-base:1rem; --gut:28px} }
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%; scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:var(--fs-base)/1.62 var(--f-body);
  font-variant-numeric:tabular-nums; padding-bottom:76px}
@media (min-width:760px){ body{padding-bottom:0} }
img{max-width:100%;height:auto;display:block}
a{color:inherit}
h1,h2,h3{font-family:var(--f-display);margin:0;text-wrap:balance;letter-spacing:-.02em}
h1{font-size:var(--fs-h1);font-weight:700;line-height:1.04}
h2{font-size:var(--fs-h2);font-weight:700;line-height:1.1}
h3{font-size:var(--fs-h3);font-weight:600;line-height:1.25}
p{margin:.7rem 0 0;text-wrap:pretty}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gut)}
section{padding:52px 0}
@media (min-width:760px){ section{padding:88px 0} }
.hair{border-top:1px solid var(--line)}
.lede{font-size:var(--fs-lead);color:var(--ink-2);max-width:60ch}
.mute{color:var(--mute)}
.kicker{font-family:var(--f-display);font-size:var(--fs-label);font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;color:var(--signal);margin:0 0 12px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
/* ── LES DEUX LANGUES ───────────────────────────────────────────────────────────────────────────────
   Le HTML porte les deux textes (les lecteurs d'écran, Google et le presse-papier voient les deux) ;
   `data-lang` sur <html> décide lequel s'affiche. C'est le JavaScript du laboratoire qui pose
   l'attribut — le même code qu'avant la refonte, donc le même contrat. */
.en-only{display:none}
html[data-lang=en] .fr-only{display:none}
html[data-lang=en] .en-only{display:inline}
/* le focus : un anneau visible partout, jamais retiré (§13) */
:focus-visible{outline:3px solid var(--signal-2);outline-offset:2px;border-radius:6px}
/* les cibles : 48 px au bureau, 52 sur téléphone — la fenêtre 52-64 de MALEWICZ pt.3 */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:52px;padding:0 20px;
  border-radius:999px;border:1.5px solid transparent;font-family:var(--f-display);font-weight:600;
  font-size:var(--fs-btn);text-decoration:none;cursor:pointer;
  transition:background-color .18s var(--ease),color .18s var(--ease),border-color .18s var(--ease),transform .14s var(--ease)}
.btn:active{transform:translateY(1px)}
.btn-primary{background:var(--signal);color:#fff}
.btn-wa{background:var(--wa);color:#fff}
.btn-line{border-color:var(--line);color:var(--ink)}
.btn-ghost{color:#fff;border-color:rgba(255,255,255,.32)}
.btn svg{width:18px;height:18px;fill:currentColor;flex:none}
@media (min-width:760px){ .btn{min-height:48px} }
.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.skip{position:absolute;left:12px;top:-60px;z-index:80;background:var(--ink);color:#fff;padding:12px 16px;
  border-radius:12px;text-decoration:none;transition:top .18s var(--ease)}
.skip:focus{top:12px}

/* ── LA BARRE DU HAUT — une seule ligne, elle ne colle pas (§24.1 bonus) ───────────────────────── */
.topbar{background:var(--ink);color:#fff;font-size:var(--fs-xs)}
.topbar .wrap{display:flex;align-items:center;gap:14px;min-height:46px;flex-wrap:wrap;padding-top:6px;padding-bottom:6px}
.topbar .state{font-weight:600}
.topbar .dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#25D366;margin-right:7px}
.topbar .dot.closed{background:#FBBF24}
.topbar .sep{color:rgba(255,255,255,.35)}
.topbar .lang{margin-left:auto;display:flex;align-items:center;gap:8px}
.topbar .lang button{background:none;border:0;color:var(--mute-on-ink);font:600 var(--fs-xs) var(--f-display);
  min-height:44px;padding:0 6px;cursor:pointer;letter-spacing:.04em}
.topbar .lang button.is-on{color:#fff}
.topbar .lang button.is-on::after{content:"";display:block;height:2px;background:var(--signal-2);margin-top:2px}

/* ── L'EN-TÊTE ───────────────────────────────────────────────────────────────────────────────── */
.head{background:var(--paper);border-bottom:1px solid var(--line)}
.head .wrap{display:flex;align-items:center;gap:16px;min-height:64px}
.brand{display:flex;flex-direction:column;text-decoration:none;line-height:1.1}
.brand b{font-family:var(--f-display);font-weight:700;font-size:1.24rem;letter-spacing:-.01em}
.brand span{font-size:var(--fs-label);color:var(--mute);letter-spacing:.02em}
.head nav{display:none;margin-left:auto;gap:26px;font-size:var(--fs-sm);font-weight:600}
.head nav a{text-decoration:none;color:var(--ink-2)}
.head .btn{margin-left:auto;min-height:46px;padding:0 16px}
@media (min-width:900px){ .head nav{display:flex} .head .btn{margin-left:26px} }

/* ── LE HERO — sombre, typographique, SANS photographie derrière le texte ──────────────────────── */
.hero{background:var(--ink);color:#fff;padding:44px 0 48px}
@media (min-width:760px){ .hero{padding:76px 0 84px} }
.hero-grid{display:grid;gap:34px}
@media (min-width:900px){ .hero-grid{grid-template-columns:1.05fr .95fr;gap:56px;align-items:center} }
.hero .sur{color:#C4B5FD;font-size:var(--fs-xs);font-weight:600;margin:0 0 14px;letter-spacing:.02em}
.hero h1{color:#fff}
.hero .lede{color:var(--mute-on-ink);margin-top:16px}
.hero .who{margin-top:24px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-size:var(--fs-sm);color:var(--mute-on-ink)}
.hero .who b{color:#fff;font-family:var(--f-display)}
/* la fiche : l'objet du laboratoire, en trois états sur la page (ici, l'exemple) */
.fiche{position:relative;color:var(--ink);background:var(--paper);border-radius:var(--r);
  padding:18px 20px 20px 34px;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.fiche::before{content:"";position:absolute;left:16px;top:14px;bottom:14px;width:5px;
  background:repeating-linear-gradient(to bottom,var(--line) 0 2px,transparent 2px 10px)}
.fiche-top{display:flex;align-items:center;gap:10px;margin:0 0 14px;padding-bottom:11px;border-bottom:2px solid var(--ink)}
.fiche-lab{font-family:var(--f-display);font-weight:700;font-size:1.06rem}
.fiche-tag{margin-left:auto;font-size:var(--fs-label);color:var(--mute);background:var(--soft);border-radius:999px;padding:4px 11px}
.fiche-tag.is-ready{background:var(--wa);color:#fff}
.fiche-rows{margin:0;display:grid;gap:11px}
.fiche-rows dt{font-size:var(--fs-label);color:var(--mute);font-weight:600;letter-spacing:.02em}
.fiche-rows dd{margin:2px 0 0;font-size:var(--fs-sm)}
.fiche-rows dd.is-empty{color:var(--mute)}
@media (min-width:560px){ .fiche-rows>div{display:grid;grid-template-columns:118px 1fr;gap:14px} .fiche-rows dd{margin:0} }
.fiche-cap{margin:14px 0 0;padding-top:12px;border-top:1px solid var(--line);font-size:var(--fs-xs);color:var(--signal);font-weight:600}

/* ── LES QUATRE ÉTAPES — des lignes, pas des cartes ───────────────────────────────────────────── */
.steps{counter-reset:s;margin:26px 0 0;padding:0;list-style:none;display:grid;gap:0}
.steps li{counter-increment:s;position:relative;padding:20px 0 20px 46px;border-top:1px solid var(--line)}
.steps li::before{content:counter(s);position:absolute;left:0;top:20px;width:30px;height:30px;border-radius:50%;
  background:var(--tint);color:var(--signal);font:700 var(--fs-sm) var(--f-display);display:grid;place-items:center}
.steps b{font-family:var(--f-display);font-size:var(--fs-h3);font-weight:600;display:block}
.steps p{margin:.35rem 0 0;color:var(--mute);font-size:var(--fs-sm);max-width:62ch}
@media (min-width:860px){ .steps{grid-template-columns:1fr 1fr;column-gap:44px} }

/* ── LES ANALYSES — une tuile par famille : image, titre, liste. Texte SOUS l'image, jamais dessus */
.fams{margin-top:28px;display:grid;gap:28px}
@media (min-width:820px){ .fams{grid-template-columns:1fr 1fr;gap:36px 32px} }
.fam{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--paper)}
.fam img{aspect-ratio:16/10;object-fit:cover;width:100%}
.fam-b{padding:18px}
.fam h3{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.fam .quoi{color:var(--mute);font-size:var(--fs-sm);margin:.3rem 0 0}
.fam ul{margin:14px 0 0;padding:0;list-style:none;display:grid;gap:8px;font-size:var(--fs-sm)}
.fam li{padding-left:16px;position:relative}
.fam li::before{content:"";position:absolute;left:0;top:.62em;width:6px;height:6px;border-radius:50%;background:var(--signal);opacity:.5}
.fam .ask{display:inline-flex;align-items:center;gap:7px;margin-top:16px;font-size:var(--fs-sm);font-weight:600;
  color:var(--signal);text-decoration:none;min-height:44px}
.fam-cap{margin:10px 0 0;font-size:var(--fs-xs);color:var(--mute)}
figure{margin:0}

/* ── LA PRÉPARATION — cinq accordéons, aucun décor ────────────────────────────────────────────── */
.prep{margin-top:24px;border-top:1px solid var(--line)}
.prep details{border-bottom:1px solid var(--line)}
.prep summary{display:flex;align-items:center;gap:12px;min-height:60px;cursor:pointer;list-style:none;
  font-family:var(--f-display);font-size:var(--fs-h3);font-weight:600;padding:6px 0}
.prep summary::-webkit-details-marker{display:none}
.prep summary::after{content:"+";margin-left:auto;font-weight:600;color:var(--signal);font-size:1.25rem;line-height:1}
.prep details[open] summary::after{content:"–"}
.prep .pane{padding:0 0 20px;color:var(--mute);font-size:var(--fs-sm);max-width:70ch}
.prep .pane b{color:var(--ink)}
.prep .always{margin-top:18px;padding:16px 18px;background:var(--soft);border-radius:var(--r);font-size:var(--fs-sm);color:var(--ink-2)}
.prep-media{margin-top:26px}
.prep-media img{aspect-ratio:4/3;object-fit:cover;border-radius:var(--r);width:100%}  /* le ratio du fichier : 1100×825 */
.photo-cap{margin:9px 0 0;font-size:var(--fs-xs);color:var(--mute)}

/* ── LE RENDEZ-VOUS — le formulaire et la fiche vivante ───────────────────────────────────────── */
.rdv-grid{margin-top:26px;display:grid;gap:26px}
@media (min-width:900px){ .rdv-grid{grid-template-columns:1.15fr .85fr;gap:40px;align-items:start} }
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:20px}
@media (min-width:760px){ .card{padding:26px} }
.rdv h3{margin-bottom:4px}
.rdv .hint{font-size:var(--fs-xs);color:var(--mute);margin:10px 0 0}
.rdv fieldset{border:0;margin:0;padding:0;min-width:0}
.rdv legend,.rdv label.grp-t{display:block;font-size:var(--fs-label);font-weight:600;letter-spacing:.02em;
  color:var(--mute);text-transform:uppercase;margin:22px 0 8px;padding:0}
.fams-box{display:grid;gap:10px}
.fams-box>div{border:1px solid var(--line-2);border-radius:14px;padding:12px 14px}
.fams-box b{font-family:var(--f-display);font-size:var(--fs-sm);display:block;margin-bottom:4px}
.chk{display:flex;gap:11px;align-items:flex-start;font-size:var(--fs-sm);line-height:1.4;padding:8px 0;min-height:44px;cursor:pointer}
.chk input{flex:none;width:21px;height:21px;margin:1px 0 0;accent-color:var(--signal)}
.mom{display:grid;gap:2px}
@media (min-width:560px){ .mom{grid-template-columns:1fr 1fr} }
.rdv input[type=text]{width:100%;font:inherit;font-size:var(--fs-base);padding:13px 14px;border:1.5px solid var(--line);
  border-radius:12px;background:var(--paper);color:var(--ink)}
.rdv input[type=text]:focus{border-color:var(--signal);box-shadow:0 0 0 3px var(--tint);outline:none}
.rdv input[aria-invalid=true]{outline:2px solid var(--err);outline-offset:2px}
.rdv .grp.is-err legend,.rdv .grp.is-err label.grp-t,.rdv .grp.is-err>label,.fams-box>div.is-err b{color:var(--err)}
.rdv .send{width:100%;margin-top:22px}
.rdv .send[aria-disabled=true]{opacity:.55;filter:grayscale(.35);cursor:not-allowed}
#rdv-said{margin:12px 0 0;font-size:var(--fs-xs);font-weight:600;color:var(--err)}
#wa-said{position:fixed;left:12px;right:12px;bottom:88px;z-index:60;margin:0;display:none;font-size:var(--fs-xs);
  background:var(--ink);color:#fff;border-radius:14px;padding:13px 15px;box-shadow:0 14px 34px rgba(0,0,0,.28)}
#wa-said.on{display:block}
@media (min-width:760px){ #wa-said{left:auto;right:24px;bottom:24px;max-width:400px} }
.fiche-live .fiche{box-shadow:0 16px 40px rgba(20,21,26,.10);border:1px solid var(--line)}
.bring{margin-top:20px;border-top:1px solid var(--line);padding-top:16px;display:grid;gap:14px}
.bring h4{margin:0;font-family:var(--f-display);font-size:var(--fs-label);text-transform:uppercase;letter-spacing:.02em;color:var(--mute)}
.bring p{margin:.25rem 0 0;font-size:var(--fs-sm)}
.bring a{color:var(--signal);font-weight:600}

/* ── LES RÉSULTATS ───────────────────────────────────────────────────────────────────────────── */
.two{margin-top:26px;display:grid;gap:22px}
@media (min-width:820px){ .two{grid-template-columns:1fr 1fr;gap:32px} }
.panel{border-top:2px solid var(--ink);padding-top:18px}
.panel p{color:var(--mute);font-size:var(--fs-sm)}
.panel .quote{margin-top:14px;padding-left:16px;border-left:3px solid var(--signal);color:var(--ink-2);font-style:italic}

/* ── NOUS TROUVER ────────────────────────────────────────────────────────────────────────────── */
.find{margin-top:26px;display:grid;gap:26px}
@media (min-width:900px){ .find{grid-template-columns:1fr 1fr;gap:40px;align-items:start} }
.rows{margin:0;display:grid;gap:0}
.rows>div{display:grid;grid-template-columns:110px 1fr;gap:14px;padding:13px 0;border-bottom:1px solid var(--line-2)}
.rows dt{font-size:var(--fs-xs);color:var(--mute);font-weight:600}
.rows dd{margin:0;font-size:var(--fs-sm)}
.rows a{color:var(--signal);font-weight:600;text-decoration:none}
.map{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--soft)}
.map svg{display:block;width:100%;height:auto}

/* ── FAQ ─────────────────────────────────────────────────────────────────────────────────────── */
.faq{margin-top:24px;border-top:1px solid var(--line)}
details.faq{border-bottom:1px solid var(--line)}
details.faq summary{display:flex;align-items:center;gap:12px;min-height:60px;cursor:pointer;list-style:none;
  font-family:var(--f-display);font-weight:600;font-size:1.02rem;padding:6px 0}
details.faq summary::-webkit-details-marker{display:none}
details.faq summary::after{content:"+";margin-left:auto;color:var(--signal);font-weight:600;font-size:1.25rem;line-height:1}
details.faq[open] summary::after{content:"–"}
details.faq p{margin:0 0 20px;color:var(--mute);font-size:var(--fs-sm);max-width:72ch}

/* ── LE PIED DE PAGE — quatre blocs et un filet (§20) ─────────────────────────────────────────── */
.foot{background:var(--ink);color:#fff;padding:52px 0 34px;margin-top:0}
.foot a{color:#fff;text-decoration:none}
.foot-grid{display:grid;gap:30px}
@media (min-width:760px){ .foot-grid{grid-template-columns:1.4fr 1fr 1fr} }
.foot h4{margin:0 0 12px;font-family:var(--f-display);font-size:var(--fs-label);letter-spacing:.06em;
  text-transform:uppercase;color:var(--mute-on-ink)}
.foot ul{margin:0;padding:0;list-style:none;display:grid;gap:10px;font-size:var(--fs-sm)}
.foot .pres{color:var(--mute-on-ink);font-size:var(--fs-sm);margin:.6rem 0 0;max-width:44ch}
.foot .strip{margin-top:38px;padding-top:18px;border-top:1px solid rgba(255,255,255,.16);
  display:flex;flex-wrap:wrap;gap:12px 20px;font-size:var(--fs-xs);color:var(--mute-on-ink)}
.foot .strip .to-top{margin-left:auto;font-weight:600}

/* ── LE BANDEAU DU TÉLÉPHONE — une action primaire, une secondaire, une icône ─────────────────── */
.sticky-wa{position:fixed;left:12px;right:12px;bottom:12px;z-index:50;display:grid;
  grid-template-columns:1.3fr 1fr 56px;gap:10px}
.sticky-wa a{display:flex;align-items:center;justify-content:center;gap:8px;min-height:56px;border-radius:16px;
  text-decoration:none;font-family:var(--f-display);font-weight:700;font-size:var(--fs-sm);
  box-shadow:0 12px 28px rgba(0,0,0,.22)}
.sticky-wa .r{background:var(--signal);color:#fff}
.sticky-wa .w{background:var(--wa);color:#fff}
.sticky-wa .c{background:#fff;color:var(--ink)}
.sticky-wa svg{width:20px;height:20px;fill:currentColor}
@media (min-width:760px){ .sticky-wa{display:none} }

@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;
    transition-duration:.01ms !important}
}
@media (hover:hover) and (pointer:fine){
  .btn-primary:hover{background:var(--signal-2)}
  .btn-line:hover{border-color:var(--signal);color:var(--signal)}
  .btn-ghost:hover{border-color:#fff}
  .btn-wa:hover{background:#096633}
  .fam .ask:hover{text-decoration:underline}
  .head nav a:hover{color:var(--signal)}
}
"""

# ══════════════════════════════════════════════════════════════════════════════════════════════════
# LES MORCEAUX
# ══════════════════════════════════════════════════════════════════════════════════════════════════
def img(slug, cls, w, h, alt_fr, alt_en, eager=False, sm_w=None, sizes="92vw"):
    sm = ' srcset="img/%s-sm.jpg %dw, img/%s.jpg %dw" sizes="%s"' % (slug, sm_w, slug, w, sizes) if sm_w else ""
    loading = "" if eager else ' loading="lazy"'
    return ('<img class="%s" src="img/%s.jpg"%s width="%d" height="%d" data-alt-fr="%s" data-alt-en="%s" alt="%s"%s decoding="async">'
            % (cls, slug, sm, w, h, alt_fr, alt_en, alt_fr, loading))

def seo_graph():
    """La schéma dit ce que la page dit : le laboratoire, ses horaires, et les cinq questions visibles."""
    import json
    faq = [{"@type": "Question", "name": q[0],
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", q[2])}} for q in FAQ]
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalLaboratory", "@id": "#uni-labo", "name": LAB["nom"],
         "description": "Laboratoire d'analyses de biologie médicale à Bonamoussadi, Douala.",
         "url": "https://uni-labo.vercel.app/", "telephone": LAB["tel"], "email": LAB["mail"],
         "address": {"@type": "PostalAddress", "streetAddress": "Rue 5N441, Bonamoussadi (Makepe Bloc L)",
                     "addressLocality": "Douala", "addressCountry": "CM"},
         "areaServed": "Douala", "availableLanguage": ["fr", "en"],
         "openingHoursSpecification": [
             {"@type": "OpeningHoursSpecification",
              "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "19:00"},
             {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "07:00", "closes": "13:00"}]},
        {"@type": "FAQPage", "@id": "#faq", "mainEntity": faq}]}
    return json.dumps(g, ensure_ascii=False, separators=(",", ":"))

def map_svg():
    """Le plan dessiné du carrefour : il aide à trouver, il ne prétend pas être une photo."""
    return """<svg viewBox="0 0 460 300" role="img" aria-label="Plan : le laboratoire au carrefour Etoo, Bonamoussadi">
  <rect width="460" height="300" fill="#F5F6F8"/>
  <path d="M0 118h460M186 0v300" stroke="#D8DBE2" stroke-width="26"/>
  <path d="M0 118h460M186 0v300" stroke="#fff" stroke-width="2" stroke-dasharray="9 9"/>
  <text x="14" y="108" font-family="Sora,sans-serif" font-size="11" fill="#5A6170">vers Makepe</text>
  <text x="392" y="108" font-family="Sora,sans-serif" font-size="11" fill="#5A6170" text-anchor="end">vers Bonamoussadi</text>
  <text x="196" y="292" font-family="Sora,sans-serif" font-size="11" fill="#5A6170">vers Bonabéri</text>
  <rect x="30" y="140" width="130" height="120" rx="6" fill="#E7E3F8"/>
  <rect x="216" y="20" width="120" height="72" rx="6" fill="#E7E3F8"/>
  <circle cx="186" cy="118" r="34" fill="#5B21B6" opacity=".14"/>
  <circle cx="186" cy="118" r="9" fill="#5B21B6"/>
  <text x="200" y="112" font-family="Sora,sans-serif" font-size="13" font-weight="700" fill="#5B21B6">UNI-LABO</text>
  <text x="200" y="130" font-family="Public Sans,sans-serif" font-size="11" fill="#5A6170">Rue 5N441</text>
  <text x="40" y="180" font-family="Public Sans,sans-serif" font-size="11" fill="#5A6170">carrefour</text>
  <text x="40" y="196" font-family="Public Sans,sans-serif" font-size="11" fill="#5A6170">Etoo</text>
</svg>"""

def build():
    P = []
    A = P.append
    A('<!DOCTYPE html>')
    A('<html lang="fr" data-lang="fr" class="no-js">')
    A('<head>')
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
    A('<meta name="robots" content="noindex,nofollow">')
    A('<title>UNI-LABO — Laboratoire d\'analyses médicales · Bonamoussadi, Douala</title>')
    A('<meta name="description" content="Laboratoire d\'analyses de biologie médicale à Bonamoussadi, Douala — Carrefour Etoo. '
      'Analyses prescrites par votre médecin, préparation expliquée, prise de rendez-vous sur WhatsApp. Français et anglais.">')
    A('<meta name="theme-color" content="#14151A">')
    A('<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">'
      '<meta property="og:locale:alternate" content="en_US">')
    A('<meta property="og:title" content="UNI-LABO — laboratoire d\'analyses à Bonamoussadi, Douala">')
    A('<meta property="og:description" content="Le résultat juste, du premier coup. Préparation expliquée, '
      'rendez-vous sur WhatsApp, résultats remis au laboratoire.">')
    A('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    A('<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=Public+Sans:wght@400;600;700&display=swap" rel="stylesheet">')
    A('<style>' + CSS + '</style>')
    A('</head>')
    A('<body>')

    # ── la barre du haut ─────────────────────────────────────────────────────────────────────────
    A('<div class="topbar"><div class="wrap">')
    A('<span class="state" id="open-state"></span>')
    A('<span>%s</span>' % bi(LAB["horaires_fr"], LAB["horaires_en"]))
    A('<span>Carrefour Etoo, Bonamoussadi</span>')
    A('<span class="lang">')
    A('<button id="btn-fr" type="button" aria-pressed="true" lang="fr">FR</button>')
    A('<button id="btn-en" type="button" aria-pressed="false" lang="en">EN</button>')
    A('</span></div></div>')

    # ── l'en-tête ───────────────────────────────────────────────────────────────────────────────
    A('<header class="head"><div class="wrap">')
    A('<a class="brand" href="#top"><b>UNI-LABO</b><span>%s</span></a>' % bi(LAB["qualif_fr"], LAB["qualif_en"]))
    # Les deux langues vivent dans le HTML, mais PAS dans un attribut : un aria-label est une chaîne,
    # pas un nœud — y glisser des <span> produisait un `</span>` orphelin (relevé par audit_html).
    A('<nav aria-label="Sections de la page · Page sections">')
    A('<a href="#analyses">%s</a>' % bi("Analyses", "Tests"))
    A('<a href="#preparation">%s</a>' % bi("Préparation", "Preparation"))
    A('<a href="#resultats">%s</a>' % bi("Résultats", "Results"))
    A('<a href="#trouver">%s</a>' % bi("Nous trouver", "Find us"))
    A('<a href="#faq">%s</a>' % bi("Questions", "FAQ"))
    A('</nav>')
    A('<a class="btn btn-primary" href="#rendez-vous">%s</a>' % bi("Prendre RDV", "Book a visit"))
    A('</div></header>')

    A('<main id="top">')
    A('<a class="skip" href="#rendez-vous">%s</a>' % bi("Aller au formulaire", "Go to the form"))

    # ── le hero ─────────────────────────────────────────────────────────────────────────────────
    A('<section class="hero"><div class="wrap hero-grid">')
    A('<div>')
    A('<p class="sur">%s</p>' % bi(HERO["sur_fr"], HERO["sur_en"]))
    A('<h1>%s</h1>' % bi(HERO["h1_fr"], HERO["h1_en"]))
    A('<p class="lede">%s</p>' % bi(HERO["sub_fr"], HERO["sub_en"]))
    A('<p class="who">%s <b>%s</b> · <a href="tel:%s" style="color:#fff">%s</a></p>'
      % (bi("Biologiste", "Biologist"), LAB["biologiste"], LAB["tel"], LAB["tel_wa"]))
    A('<div class="actions">')
    A('<a class="btn btn-primary" href="#rendez-vous">%s</a>' % bi(HERO["cta_fr"], HERO["cta_en"]))
    A('<a class="btn btn-ghost" href="%s" data-wa>%s</a>'
      % (wa("Bonjour UNI-LABO, je souhaite faire une analyse."), bi(HERO["cta2_fr"], HERO["cta2_en"])))
    A('</div></div>')
    # la fiche, exemple : c'est elle la signature, pas une photo
    A('<div class="fiche">')
    A('<p class="fiche-top"><span class="fiche-lab">UNI-LABO</span>'
      '<span class="fiche-tag">%s</span></p>' % bi("Exemple", "Example"))
    A('<dl class="fiche-rows">')
    for dt_fr, dt_en, dd_fr, dd_en in FICHE:
        A('<div><dt>%s</dt><dd>%s</dd></div>' % (bi(dt_fr, dt_en), bi(dd_fr, dd_en)))
    A('</dl>')
    A('<p class="fiche-cap">%s</p>' % bi(
        "Le formulaire remplit cette fiche avec vos analyses, et l'envoie sur WhatsApp.",
        "The form fills this sheet with your tests and sends it on WhatsApp."))
    A('</div></div></section>')

    # ── les quatre étapes ───────────────────────────────────────────────────────────────────────
    A('<section id="parcours" class="wrap">')
    A('<p class="kicker">%s</p>' % bi("Comment ça se passe", "How it works"))
    A('<h2>%s</h2>' % bi("Quatre étapes, aucune surprise.", "Four steps, no surprises."))
    A('<ol class="steps">')
    for i, (b_fr, b_en, p_fr, p_en) in enumerate(JOURNEY, 1):
        A('<li><b>%s</b><p>%s</p></li>' % (bi(b_fr, b_en), bi(p_fr, p_en)))
    A('</ol></section>')

    # ── les analyses ────────────────────────────────────────────────────────────────────────────
    A('<section id="analyses" class="hair"><div class="wrap">')
    A('<h2>%s</h2>' % bi("Ce que nous dosons.", "What we run."))
    A('<p class="lede">%s</p>' % bi(
        "Les analyses prescrites par votre médecin, dans quatre domaines. <b>Aucun tarif n'est affiché ici</b> : "
        "le prix dépend de l'analyse et du réactif — demandez-le sur WhatsApp, la réponse arrive avant que vous vous déplaciez.",
        "The tests your doctor prescribes, across four areas. <b>No prices are shown here</b>: the price depends on the "
        "test and the day's reagent — ask on WhatsApp, the answer comes before you travel."))
    A('<div class="fams">')
    for f in FAMILIES:
        A('<figure class="fam">')
        A(img("unilabo-f-" + f["slug"], "", 800, 500,
              "Photo d'illustration de laboratoire — %s." % re.sub("&amp;", "et", f["fr"]),
              "Laboratory illustration photo — %s." % re.sub("&amp;", "and", f["en"]),
              sm_w=640, sizes="(min-width:820px) 520px, 92vw"))
        A('<figcaption class="fam-b">')
        A('<h3>%s</h3>' % bi(f["fr"], f["en"]))
        A('<p class="quoi">%s</p>' % bi(f["quoi_fr"], f["quoi_en"]))
        A('<ul>')
        for it_fr, it_en in f["items"]:
            A('<li>%s</li>' % bi(it_fr, it_en))
        A('</ul>')
        A('<a class="ask" href="%s" data-wa>%s →</a>'
          % (wa("Bonjour UNI-LABO, je voudrais le tarif de cette analyse : "),
             bi("Demander le tarif", "Ask the price")))
        A('</figcaption></figure>')
    A('</div>')
    A('<p class="photo-cap">%s</p>' % bi(
        "Images de démonstration : la photo définitive sera prise dans votre laboratoire.",
        "Staged images: the final photograph will be taken in your laboratory."))
    A('</div></section>')

    # ── la préparation ──────────────────────────────────────────────────────────────────────────
    A('<section id="preparation" class="hair"><div class="wrap">')
    A('<p class="kicker">%s</p>' % bi("La préparation", "Preparation"))
    A('<h2>%s</h2>' % bi("Une analyse mal préparée, c'est un déplacement pour rien.",
                         "A badly prepared test means a wasted trip."))
    A('<p class="lede">%s</p>' % bi(
        "C'est la seule chose qui se joue AVANT de venir, et c'est celle qui décide si l'analyse est utilisable. "
        "Voici ce que le laboratoire publie, situation par situation.",
        "It is the only thing decided BEFORE you come, and it decides whether the test is usable. "
        "Here is what the laboratory publishes, situation by situation."))
    A('<div class="prep chips" role="group">')
    for t_fr, t_en, d_fr, d_en, anchor in PREP:
        A('<details%s>' % (' id="prep-%s"' % anchor if anchor else ''))
        A('<summary>%s</summary>' % bi(t_fr, t_en))
        A('<div class="pane">%s</div>' % bi(d_fr, d_en))
        A('</details>')
    A('</div>')
    A('<p class="always">%s</p>' % bi(*PREP_ALWAYS))
    A('<figure class="prep-media">')
    A(img("unilabo-preparation", "", 1100, 825,
          "Un homme attend, un verre d'eau et une horloge devant lui, avant une analyse à jeun.",
          "A man waits with a glass of water and a clock in front of him before a fasting test.",
          sm_w=760, sizes="(min-width:760px) 1080px, 92vw"))
    A('<figcaption class="photo-cap">%s</figcaption>' % bi(
        "Mise en situation. La photo définitive sera prise dans votre laboratoire.",
        "Staged image. The final photograph will be taken in your laboratory."))
    A('</figure>')
    A('</div></section>')

    # ── le rendez-vous ──────────────────────────────────────────────────────────────────────────
    A('<section id="rendez-vous" class="hair"><div class="wrap">')
    A('<h2>%s</h2>' % bi("Dites-nous ce que vous venez chercher.", "Tell us what you are coming for."))
    A('<p class="lede">%s</p>' % bi(
        "Cochez vos analyses, écrivez votre nom, choisissez un moment : la fiche se remplit sous vos yeux et part "
        "sur WhatsApp déjà rédigée. <b>Rien n'est enregistré sur ce site</b> — c'est votre téléphone qui envoie.",
        "Tick your tests, write your name, choose a time: the sheet fills in as you go and leaves on WhatsApp already "
        "written. <b>Nothing is stored on this site</b> — your phone sends it."))
    A('<div class="rdv-grid">')
    A(build_form())
    A('<div class="fiche-live">')
    A('<div class="fiche" id="fiche">')
    A('<p class="fiche-top"><span class="fiche-lab">UNI-LABO</span>'
      '<span class="fiche-tag" id="fiche-state">%s</span></p>' % bi("à compléter", "to fill in"))
    A('<dl class="fiche-rows">')
    for dt_fr, dt_en, idn in (("Nom", "Name", "fiche-nom"), ("Analyses", "Tests", "fiche-tests"),
                             ("Préparation", "Preparation", "fiche-prep"), ("Moment", "Time", "fiche-moment")):
        A('<div><dt>%s</dt><dd id="%s" class="is-empty">—</dd></div>' % (bi(dt_fr, dt_en), idn))
    A('</dl>')
    A('<p class="fiche-cap" id="fiche-foot">%s</p>' % bi(
        "Cochez vos analyses : cette fiche se remplit sous vos yeux, puis part sur WhatsApp.",
        "Tick your tests: this sheet fills in as you go, then leaves on WhatsApp."))
    A('</div>')
    A('<div class="bring">')
    A('<div><h4>%s</h4><p>%s</p></div>' % (bi("Où", "Where"), bi(LAB["adresse_fr"], LAB["adresse_en"])))
    A('<div><h4>%s</h4><p>%s</p></div>' % (bi("Quand", "When"), bi(LAB["horaires_fr"], LAB["horaires_en"])))
    A('<div><h4>%s</h4><p>%s</p></div>' % (bi("Quoi apporter", "What to bring"),
      bi("L'ordonnance si vous en avez une, et votre carte de couverture si vous en avez une. Une question ? "
         "<a href=\"tel:%s\">%s</a>" % (LAB["tel"], LAB["tel_wa"]),
         "Your prescription if you have one, and your cover card if you have one. A question? "
         "<a href=\"tel:%s\">%s</a>" % (LAB["tel"], LAB["tel_wa"]))))
    A('</div></div></div></div></section>')

    # ── les résultats ───────────────────────────────────────────────────────────────────────────
    A('<section id="resultats" class="hair"><div class="wrap">')
    A('<h2>%s</h2>' % bi("Où et quand récupérer le résultat.", "Where and when to collect your result."))
    A('<div class="two">')
    A('<div class="panel"><h3>%s</h3><p>%s</p></div>' % (bi(RESULTATS["t_fr"], RESULTATS["t_en"]),
                                                       bi(RESULTATS["p_fr"], RESULTATS["p_en"])))
    A('<div class="panel"><h3>%s</h3><p>%s</p></div>' % (bi(RESULTATS["b_t_fr"], RESULTATS["b_t_en"]),
                                                       bi(RESULTATS["b_p_fr"], RESULTATS["b_p_en"])))
    A('</div>')
    A('<div class="actions"><a class="btn btn-line" href="%s" data-wa>%s</a></div>'
      % (wa("Bonjour Dr Tientcheu, j'ai une question sur une analyse."),
         bi("Poser une question", "Ask a question")))
    A('</div></section>')

    # ── nous trouver ────────────────────────────────────────────────────────────────────────────
    A('<section id="trouver" class="hair"><div class="wrap">')
    A('<h2>%s</h2>' % bi("Carrefour Etoo, Bonamoussadi.", "Carrefour Etoo, Bonamoussadi."))
    A('<div class="find">')
    A('<dl class="rows">')
    for k_fr, k_en, v_fr, v_en in LIEU:
        val = bi(v_fr, v_en)
        if v_fr == "696 13 98 19":
            val = '<a href="tel:%s">%s</a>' % (LAB["tel"], v_fr)
        if v_fr == "233 47 00 68":
            val = '<a href="tel:%s">%s</a>' % (LAB["tel_fixe_intl"], v_fr)
        if "yahoo" in v_fr:
            val = '<a href="mailto:%s">%s</a>' % (LAB["mail"], v_fr)
        A('<div><dt>%s</dt><dd>%s</dd></div>' % (bi(k_fr, k_en), val))
    A('</dl>')
    A('<div><div class="map">%s</div>' % map_svg())
    A('<div class="actions"><a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&query=UNI-LABO+Carrefour+Etoo+Bonamoussadi+Douala" rel="noopener">%s</a></div>'
      % bi("Ouvrir dans Maps", "Open in Maps"))
    A('</div></div></div></section>')

    # ── la FAQ ──────────────────────────────────────────────────────────────────────────────────
    A('<section id="faq" class="hair"><div class="wrap">')
    A('<h2>%s</h2>' % bi("Ce qu'on nous demande au guichet, écrit ici.",
                         "What people ask at the desk, written here."))
    A('<div class="faq">')
    for q_fr, q_en, r_fr, r_en in FAQ:
        A('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (bi(q_fr, q_en), bi(r_fr, r_en)))
    A('</div></div></section>')
    A('</main>')

    # ── le pied de page ─────────────────────────────────────────────────────────────────────────
    A('<footer class="foot"><div class="wrap">')
    A('<div class="foot-grid">')
    A('<div><a class="brand" href="#top" style="color:#fff"><b style="color:#fff">UNI-LABO</b></a>'
      '<p class="pres">%s</p></div>' % bi(FOOT["pres_fr"], FOOT["pres_en"]))
    A('<div><h4>%s</h4><ul>' % bi("Sur cette page", "On this page"))
    for href, l_fr, l_en in (("#analyses", "Nos analyses", "Our tests"),
                             ("#preparation", "Préparation", "Preparation"),
                             ("#rendez-vous", "Prendre rendez-vous", "Book a visit"),
                             ("#resultats", "Résultats", "Results"),
                             ("#trouver", "Nous trouver", "Find us")):
        A('<li><a href="%s">%s</a></li>' % (href, bi(l_fr, l_en)))
    A('</ul></div>')
    A('<div><h4>%s</h4><ul>' % bi("Nous joindre", "Reach us"))
    A('<li><a href="%s" data-wa>%s</a></li>' % (LAB["wa"], bi("WhatsApp " + LAB["tel_wa"], "WhatsApp " + LAB["tel_wa"])))
    A('<li><a href="tel:%s">%s</a></li>' % (LAB["tel"], bi("Appeler " + LAB["tel_wa"], "Call " + LAB["tel_wa"])))
    A('<li><a href="tel:%s">%s</a></li>' % (LAB["tel_fixe_intl"], LAB["tel_fixe"]))
    A('<li><a href="mailto:%s">%s</a></li>' % (LAB["mail"], LAB["mail"]))
    A('<li>%s</li>' % bi(LAB["adresse_fr"], LAB["adresse_en"]))
    A('</ul></div></div>')
    A('<div class="strip"><span>© 2026 UNI-LABO</span><span>%s</span>'
      '<a class="to-top" href="#top">%s</a></div>' % (bi(FOOT["note_fr"], FOOT["note_en"]),
                                                      bi("Haut de page ↑", "Back to top ↑")))
    A('</div></footer>')

    # ── le bandeau du téléphone + la bande de retour ─────────────────────────────────────────────
    A('<p id="wa-said" role="status" aria-live="polite"></p>')
    A('<div class="sticky-wa" data-wa-bar>')
    A('<a class="r" href="#rendez-vous">%s</a>' % bi("Prendre RDV", "Book a visit"))
    A('<a class="w" href="%s" data-wa>%s</a>' % (wa("Bonjour UNI-LABO, je souhaite faire une analyse."),
                                                 bi("WhatsApp", "WhatsApp")))
    A('<a class="c" href="tel:%s" aria-label="Appeler le laboratoire · Call the laboratory" title="Appeler le laboratoire · Call the laboratory">'
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg></a>'
      % LAB["tel"])
    A('</div>')

    # ── les scripts ─────────────────────────────────────────────────────────────────────────────
    A('<script>(function(){document.documentElement.classList.remove("no-js");'
      'try{var l=localStorage.getItem("unilabo-lang");if(l)document.documentElement.setAttribute("data-lang",l);}catch(e){}})();</script>')
    A('<script type="application/ld+json">' + seo_graph() + '</script>')
    A('<script>' + JS_MAIN + '</script>')
    A('<script>/* L état des deux boutons de langue, dit AUSSI aux lecteurs d écran : le JavaScript du '
      'laboratoire marque `.is-on` (visuel), ceci pose `aria-pressed` (annoncé). */'
      '(function(){function s(){var l=document.documentElement.getAttribute("data-lang")==="en"?"en":"fr";'
      'var a=document.getElementById("btn-fr"),b=document.getElementById("btn-en");'
      'if(a)a.setAttribute("aria-pressed",l==="fr"?"true":"false");'
      'if(b)b.setAttribute("aria-pressed",l==="en"?"true":"false");}'
      's();["btn-fr","btn-en"].forEach(function(i){var e=document.getElementById(i);'
      'if(e)e.addEventListener("click",function(){setTimeout(s,0);});});})();</script>')
    A('<script>' + JS_FORM + '</script>')
    A('</body></html>')
    return "\n".join(P) + "\n"


def build_form():
    """Le formulaire — mêmes identifiants que la v1, donc les 23 assertions continuent de le protéger."""
    F = []
    A = F.append
    A('<form class="rdv card" id="rdv" novalidate>')
    A('<h3>%s</h3>' % bi("Votre demande", "Your request"))
    A('<p class="hint" id="rdv-hint">%s</p>' % bi(
        "Vous ne savez pas quoi cocher ? Cochez « Autre » et envoyez la photo de votre ordonnance sur WhatsApp.",
        "Not sure what to tick? Tick “Other” and send a photo of your request on WhatsApp."))
    A('<fieldset class="grp" id="rdv-g1">')
    A('<legend>%s</legend>' % bi("1 · Vos analyses", "1 · Your tests"))
    A('<div class="fams-box">')
    for g_fr, g_en, gprep, items in FAM_GROUPS:
        A('<div>')
        A('<b>%s</b>' % bi(g_fr, g_en))
        for it_fr, it_en, prep in items:
            A('<label class="chk"><input type="checkbox" data-fr="%s" data-en="%s" value="%s"%s>'
              '<span>%s</span></label>'
              % (it_fr, it_en, re.sub("&amp;", "&", it_fr), ' data-prep="%s"' % prep if prep else "",
                 bi(it_fr, it_en)))
        A('</div>')
    A('</div></fieldset>')
    A('<div class="grp" id="rdv-g2">')
    A('<label class="grp-t" for="rdv-nom">%s</label>' % bi("2 · Votre nom", "2 · Your name"))
    A('<input type="text" id="rdv-nom" name="nom" autocomplete="name" aria-describedby="rdv-hint">')
    A('</div>')
    A('<fieldset class="grp" id="rdv-g3">')
    A('<legend>%s</legend>' % bi("3 · Moment souhaité", "3 · Preferred time"))
    A('<div class="mom">')
    for m_fr, m_en in MOMENTS:
        A('<label class="chk"><input type="radio" name="moment" data-fr="%s" data-en="%s" value="%s">'
          '<span>%s</span></label>' % (m_fr, m_en, m_fr, bi(m_fr, m_en)))
    A('</div></fieldset>')
    A('<div class="grp" id="rdv-g4">')
    A('<label class="grp-t" for="rdv-note">%s</label>' % bi("4 · Une précision (facultatif)", "4 · Anything else (optional)"))
    A('<input type="text" id="rdv-note" name="note">')
    A('</div>')
    A('<a class="btn btn-wa send" id="rdv-go" aria-disabled="true" href="%s?text=%s">'
      % (LAB["wa"], "%5Bmessage%5D"))  # remplacé juste après : voir le vrai href ci-dessous
    A('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5.1-4.5-.1-.2-1.2-1.5-1.2-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1.1 2.2 1.4 2.5 1.5.3.1.4.1.6-.1l.9-1c.2-.2.4-.2.6-.1l1.8.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3Z"/></svg>'
      '<span>%s</span></a>' % bi("Ouvrir WhatsApp avec ma demande", "Open WhatsApp with my request"))
    A('<p class="hint">%s</p>' % bi(
        "Le bouton s'active dès que vous avez coché une analyse, écrit votre nom et choisi un moment. Vous relisez le "
        "message avant de l'envoyer. Il part de votre WhatsApp vers celui du laboratoire, qui vous répond pour confirmer l'heure.",
        "The button turns on once you have ticked a test, written your name and chosen a time. You read the message before "
        "sending it. It leaves from your WhatsApp to the laboratory's, which replies to confirm the time."))
    A('<p id="rdv-said" role="status" aria-live="polite" hidden></p>')
    A('</form>')
    html = "\n".join(F)
    import urllib.parse
    generic = "%s?text=%s" % (LAB["wa"], urllib.parse.quote("Bonjour UNI-LABO, je souhaite prendre rendez-vous."))
    return html.replace('href="%s?text=%s"' % (LAB["wa"], "%5Bmessage%5D"), 'href="%s"' % generic)


if __name__ == "__main__":
    html = build()
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("écrit : %s — %d octets" % (OUT, len(html)))
    for probe, label in (('id="rdv-go"', "bouton d'envoi"), ('id="fiche-tests"', "fiche vivante"),
                         ('id="open-state"', "état d'ouverture"), ("srcset=", "variantes d'images"),
                         ('class="fr-only"', "bilingue")):
        print("   %-20s %d" % (label, html.count(probe)))
