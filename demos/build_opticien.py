#!/usr/bin/env python3
"""
AMK — OPTICAL concept builder (generic / nameless v1)
Direction: « LE MIROIR » — boutique fitting-room: a frame-shape selector as the
signature interaction, an honest quote-builder (no invented prices), warm
editorial tone. Distinct from site/mitoc.html (royal blue + Outfit) and from
the lab concept (cyan/navy + Space Grotesk).

Output: demos/concept-opticien-v1.html  (single file, base64 images, EN|FR)
"""
import base64, io, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path('/home/user/AMK')
WA = "237600000000"          # placeholder — pass --wa 2376XXXXXXXX to bake a real line
OUT_NAME = "concept-opticien-v1.html"
WA_LABEL = '+237 6XX XX XX XX'
if "--wa" in sys.argv:
    WA = sys.argv[sys.argv.index("--wa") + 1]
    WA_LABEL = '+237 ' + WA[3:6] + ' ' + WA[6:8] + ' ' + WA[8:10] + ' ' + WA[10:12]
if "--out" in sys.argv:
    OUT_NAME = sys.argv[sys.argv.index("--out") + 1]
OUT = ROOT / 'demos' / OUT_NAME

def b64(path, width, quality=76):
    im = Image.open(ROOT / path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

IMG_HERO = b64('demos/img/opticien-hero.jpg', 880)
IMG_FRAMES = b64('demos/img/opticien-frames.jpg', 820)
IMG_TRYON = b64('demos/img/opticien-tryon.jpg', 720)

SHAPES = [
    ("Rond", "Round", "rond",
     "Adoucit les visages anguleux (mâchoire marquée, front large).",
     "Softens angular faces (strong jaw, broad forehead)."),
    ("Carré", "Square", "carre",
     "Structure les visages ronds ou ovales, et tient bien sur les nez larges.",
     "Adds structure to round or oval faces and sits well on wider noses."),
    ("Œil de chat", "Cat-eye", "cat",
     "Remonte le regard : idéal si les paupières tombent un peu ou pour un effet élégant.",
     "Lifts the gaze: ideal if the eyelids drop slightly, or for a dressier look."),
    ("Aviateur", "Aviator", "avi",
     "Grand champ de vision, très confortable pour la conduite et les visages allongés.",
     "A wide field of view, very comfortable for driving and longer faces."),
]

LENSES = [
    ("Unifocaux", "Single-vision", "Vision de près ou de loin, une seule distance.",
     "Near or far vision, a single distance."),
    ("Progressifs", "Progressive", "Trois distances en un seul verre, sans ligne visible.",
     "Three distances in one lens, with no visible line."),
    ("Anti-lumière bleue", "Blue-light filter", "Pour les journées devant l'écran.",
     "For long days in front of a screen."),
    ("Photochromiques", "Photochromic", "Verres qui foncent dehors et s'éclaircissent dedans.",
     "Lenses that darken outside and clear indoors."),
]

FAQ = [
    ("Combien de temps prend un contrôle de la vue ?", "How long does an eye check take?",
     "Comptez une quinzaine de minutes, plus le temps de choisir votre monture si vous en prenez une le même jour.",
     "Allow about fifteen minutes, plus the time to choose your frame if you take one the same day."),
    ("Faut-il une ordonnance ?", "Do I need a prescription?",
     "Non pour le contrôle de la vue. Si vous apportez une ordonnance récente, nous montons vos verres directement.",
     "No for the eye check. If you bring a recent prescription, we make your lenses directly from it."),
    ("Combien coûtent les verres ?", "How much do the lenses cost?",
     "Depuis le 1\u1d49\u02b3 juillet 2026, les verres montés ont un prix plafonné au niveau national (référentiel ONOC / ministère de la Santé). Vous recevez un devis écrit avant toute commande : vous connaissez le prix avant de vous engager.",
     "Since 1 July 2026 mounted lenses have a nationally capped price (ONOC / Ministry of Public Health framework). You get a written quote before any order: you know the price before committing."),
    ("Est-ce que vous réparez les lunettes ?", "Do you repair glasses?",
     "Oui : vis, plaquettes, branches tordues, ajustement. Passez avec vos lunettes — dites-nous d'abord sur WhatsApp.",
     "Yes: screws, nose pads, bent arms, adjustments. Come in with your glasses — message us first on WhatsApp."),
    ("J'hésite entre plusieurs montures.", "I'm hesitating between several frames.",
     "Envoyez-nous les photos sur WhatsApp, nous vous conseillons selon la forme de votre visage — puis vous essayez en boutique.",
     "Send us the photos on WhatsApp, we advise you on your face shape — then you try them in the shop."),
    ("Et pour les enfants ?", "What about children?",
     "Nous montons des verres et des montures adaptés aux enfants, avec un ajustement refait après quelques jours.",
     "We fit lenses and frames suited to children, with a re-adjustment a few days later."),
]
FAQ_HTML = "\n".join(f'''<details class="faq">
  <summary><span class="fr-only">{q_fr}</span><span class="en-only">{q_en}</span></summary>
  <p><span class="fr-only">{a_fr}</span><span class="en-only">{a_en}</span></p>
</details>''' for q_fr, q_en, a_fr, a_en in FAQ)

GLYPHS = {
    "rond": '<svg viewBox="0 0 48 32"><circle cx="15" cy="16" r="11"/><circle cx="33" cy="16" r="11"/><path d="M26 16h-4"/></svg>',
    "carre": '<svg viewBox="0 0 48 32"><rect x="4" y="5" width="18" height="22" rx="4"/><rect x="26" y="5" width="18" height="22" rx="4"/><path d="M22 16h4"/></svg>',
    "cat": '<svg viewBox="0 0 48 32"><path d="M4 18c0-6 5-11 11-11 5 0 8 3 9 7l-3 8c-2 4-6 5-9 5-5 0-8-4-8-9Z"/><path d="M44 18c0-6-5-11-11-11-5 0-8 3-9 7l3 8c2 4 6 5 9 5 5 0 8-4 8-9Z"/></svg>',
    "avi": '<svg viewBox="0 0 48 32"><path d="M3 12h18l-4 12c-2 4-5 5-7 5-4 0-7-4-7-9Zm42 0H27l4 12c2 4 5 5 7 5 4 0 7-4 7-9Z"/><path d="M21 12h6"/></svg>',
}
FACE_SVG = """<svg viewBox="0 0 300 340" role="img" aria-label="Visage illustré portant la monture sélectionnée">
  <path d="M40 340c0-44 48-66 110-66s110 22 110 66Z" fill="#0E3B43"/>
  <path d="M118 226h64v44c0 12-16 20-32 20s-32-8-32-20Z" fill="#E4C4A6"/>
  <ellipse cx="66" cy="162" rx="12" ry="20" fill="#EFD2B8"/>
  <ellipse cx="234" cy="162" rx="12" ry="20" fill="#EFD2B8"/>
  <path d="M150 50c46 0 84 38 84 96 0 62-38 112-84 112S66 208 66 146c0-58 38-96 84-96Z" fill="#F2D9C0"/>
  <path d="M150 40c54 0 90 34 90 80 0 7-3 11-8 11-7-22-22-38-46-44-24-6-54-5-78 6-15 7-23 20-27 40-5 0-7-5-7-11 0-46 36-82 76-82Z" fill="#2B2620"/>
  <path d="M96 116q20-10 40-2" stroke="#4A3B2E" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M164 114q20-8 40 2" stroke="#4A3B2E" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse cx="116" cy="152" rx="15" ry="9" fill="#fff"/>
  <ellipse cx="184" cy="152" rx="15" ry="9" fill="#fff"/>
  <circle cx="116" cy="152" r="5.6" fill="#3A2E24"/>
  <circle cx="184" cy="152" r="5.6" fill="#3A2E24"/>
  <path d="M150 156v22q0 8 8 10" stroke="#DFB995" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M128 208q22 16 44 0" stroke="#C08B72" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse cx="100" cy="188" rx="14" ry="8" fill="#EBBFA1" opacity=".5"/>
  <ellipse cx="200" cy="188" rx="14" ry="8" fill="#EBBFA1" opacity=".5"/>
  <path d="M104 236q46 26 92 0" stroke="#D8B48F" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>
  <g stroke="#4A3222" stroke-width="6" fill="none" stroke-linecap="round">
    <g class="frame is-on" data-k="rond">
      <circle cx="116" cy="152" r="33" fill="rgba(190,230,240,.10)"/>
      <circle cx="184" cy="152" r="33" fill="rgba(190,230,240,.10)"/>
      <path d="M147 150h6"/>
      <path d="M83 150 64 152"/><path d="M217 150 236 152"/>
    </g>
    <g class="frame" data-k="carre">
      <rect x="84" y="128" width="64" height="48" rx="10" fill="rgba(190,230,240,.10)"/>
      <rect x="152" y="128" width="64" height="48" rx="10" fill="rgba(190,230,240,.10)"/>
      <path d="M148 146h4"/>
      <path d="M84 146 64 150"/><path d="M216 146 236 150"/>
    </g>
    <g class="frame" data-k="cat">
      <path d="M78 136 Q96 128 124 132 Q146 136 149 152 Q150 172 126 176 Q94 178 80 158 Q76 146 78 136 Z" fill="rgba(190,230,240,.10)"/>
      <path d="M222 136 Q204 128 176 132 Q154 136 151 152 Q150 172 174 176 Q206 178 220 158 Q224 146 222 136 Z" fill="rgba(190,230,240,.10)"/>
      <path d="M147 144h6"/>
      <path d="M80 148 64 152"/><path d="M220 148 236 152"/>
    </g>
    <g class="frame" data-k="avi">
      <path d="M80 136h68v8c0 22-15 38-35 38c-20 0-35-16-35-38v-8Z" fill="rgba(190,230,240,.09)"/>
      <path d="M220 136h-68v8c0 22 15 38 35 38c20 0 35-16 35-38v-8Z" fill="rgba(190,230,240,.09)"/>
      <path d="M82 134h136"/>
      <path d="M148 142h4"/>
      <path d="M82 140 64 146"/><path d="M218 140 236 146"/>
    </g>
  </g>
</svg>"""

SHAPE_HTML = "\n".join(
    f'''<button class="shape tab{" is-on" if i == 0 else ""}" data-shape="{key}" role="tab" aria-selected="{"true" if i == 0 else "false"}">
      <span class="gl" aria-hidden="true">{GLYPHS[key]}</span>
      <span class="nm"><span class="fr-only">{fr}</span><span class="en-only">{en}</span></span>
    </button>''' for i, (fr, en, key, _d_fr, _d_en) in enumerate(SHAPES))

LENS_HTML = "\n".join(
    f'''<label class="len-row">
      <input type="radio" name="lens" value="{fr}" data-en="{en}">
      <span class="len-name"><span class="fr-only">{fr}</span><span class="en-only">{en}</span></span>
      <span class="len-desc"><span class="fr-only">{d_fr}</span><span class="en-only">{d_en}</span></span>
    </label>''' for fr, en, d_fr, d_en in LENSES)

FAQ_HTML = "\n".join(f'''<details class="faq">
  <summary><span class="fr-only">{q_fr}</span><span class="en-only">{q_en}</span></summary>
  <p><span class="fr-only">{a_fr}</span><span class="en-only">{a_en}</span></p>
</details>''' for q_fr, q_en, a_fr, a_en in FAQ)

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Optician",
    "name": "Votre Opticien (demonstration concept)",
    "description": "Concept de site pour opticien : controle de la vue sur rendez-vous, choix de montures, devis verres et reparations par WhatsApp.",
    "telephone": "+237600000000", "address": {"@type": "PostalAddress", "addressLocality": "Douala", "addressCountry": "CM"},
    "openingHours": "Mo-Sa 08:30-18:00", "priceRange": "Sur devis",
}, ensure_ascii=False, indent=2)

CSS = """
:root{
 --ink:#0E3B43; --ink-2:#155763; --amber:#F0A03C; --clay:#C96F4A; --cream:#FBF6EF;
 --paper:#FFFFFF; --mute:#5E7A80; --line:rgba(14,59,67,.14); --wa:#0B7A3E; --r:16px; --max:1120px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--cream);color:var(--ink);
 font:16px/1.62 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3,.display{font-family:Fraunces,"Georgia",serif;font-weight:600;line-height:1.06;margin:0;letter-spacing:-.015em}
h1{font-size:clamp(2.1rem,7.6vw,3.6rem)}
h2{font-size:clamp(1.5rem,4.8vw,2.2rem)}
h3{font-size:1.05rem;font-family:Inter,sans-serif;font-weight:600}
p{margin:.6rem 0 0}
a{color:inherit}
.mono{font-family:Inter;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
.wrap{max-width:var(--max);margin:0 auto;padding:0 18px}
section{padding:54px 0}
.hair{border-top:1px solid var(--line)}
html[data-lang="fr"] .en-only{display:none !important}
html[data-lang="en"] .fr-only{display:none !important}
html[data-lang="en"] .en-only{display:revert !important}
html[data-lang="fr"] .fr-only{display:revert !important}
:is(a,button,label):focus-visible{outline:3px solid var(--amber);outline-offset:2px;border-radius:8px}

.top{background:var(--ink);color:#EAF4F5;font-size:.8rem}
.top .wrap{display:flex;gap:14px;justify-content:space-between;align-items:center;padding:9px 18px;flex-wrap:wrap}
.top a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.35)}
.nav{position:sticky;top:0;z-index:40;background:rgba(251,246,239,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:14px;padding:11px 18px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}
.brand svg{flex:0 0 auto}
.brand b{font-family:Fraunces,serif;font-size:1.06rem;display:block;line-height:1.05}
.brand .sub{display:block;font-size:.66rem;color:var(--mute);letter-spacing:.1em;text-transform:uppercase}
.nav nav{margin-left:auto;display:none;gap:18px;font-size:.9rem}
.nav nav a{text-decoration:none;opacity:.85}
.lang{display:flex;margin-left:auto;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:#fff}
.lang button{border:0;background:transparent;padding:7px 12px;font:600 .78rem Inter;color:var(--mute);cursor:pointer}
.lang button.is-on{background:var(--ink);color:#fff}
.cta{background:var(--wa);color:#fff;text-decoration:none;padding:11px 15px;border-radius:999px;font-weight:600;font-size:.86rem;white-space:nowrap}
.cta.small{display:none}

.hero{padding-top:34px}
.hero-grid{display:grid;gap:26px;align-items:center}
.hero h1 em{font-style:italic;color:var(--clay)}
.lede{font-size:1.05rem;color:#2C4C53;max-width:56ch}
.hero-media{position:relative;border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}
.hero-media img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover}
.tag{position:absolute;left:12px;bottom:12px;background:rgba(14,59,67,.92);color:#fff;padding:7px 11px;border-radius:10px;font-size:.7rem}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 18px;border-radius:12px;text-decoration:none;font-weight:600;border:1px solid transparent;cursor:pointer}
.btn-primary{background:var(--wa);color:#fff}
.btn-alt{background:var(--amber);color:#3A2508}
.btn-ghost{background:#fff;color:var(--ink);border-color:var(--line)}
.btn svg{width:18px;height:18px;fill:currentColor}
.facts{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
.fact{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 13px;font-size:.8rem;color:#2C4C53}
.fact b{color:var(--ink)}

/* shape selector — signature */
.shapes{background:var(--ink);color:#fff}
.shapes h2{color:#fff}
.shapes .mono{color:var(--amber)}
.tabs{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:22px 0 18px}
@media(min-width:700px){.tabs{grid-template-columns:repeat(4,1fr)}}
.shape{display:flex;flex-direction:column;align-items:center;gap:8px;background:rgba(255,255,255,.06);
 border:1px solid rgba(255,255,255,.18);color:#EAF4F5;border-radius:14px;padding:14px 10px;cursor:pointer;font:600 .9rem Inter}
.shape.is-on{background:var(--amber);color:#3A2508;border-color:var(--amber)}
.shape svg{width:46px;height:32px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round}
.shape-panel{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:20px}
.shape-panel h3{color:#fff;font-family:Fraunces,serif;font-size:1.35rem;font-weight:600}
.shape-panel p{color:#CBE0E3}
.who{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}
.who span{background:rgba(240,160,60,.16);border:1px solid rgba(240,160,60,.4);color:#FFDDA8;border-radius:999px;padding:6px 12px;font-size:.78rem}
.mirror-grid{display:grid;gap:22px}
@media(min-width:900px){.mirror-grid{grid-template-columns:290px 1fr;gap:30px;align-items:start}}
.mirror{margin:0;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:16px 16px 12px}
.mirror svg{display:block;width:100%;height:auto}
.mirror figcaption{display:block;margin-top:10px;font-size:.68rem;letter-spacing:.04em;color:#9FBDC3;text-transform:uppercase}
.mirror-grid .tabs{grid-template-columns:repeat(2,1fr);margin-top:0}
.frame{opacity:0;transform:translateY(-12px);transition:opacity .32s ease,transform .32s ease}
.frame.is-on{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.frame{transition:none}}

/* frames wall */
.wall{display:grid;gap:12px;margin-top:20px}
@media(min-width:760px){.wall{grid-template-columns:1.2fr .8fr}}
.shot{border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}
.shot img{display:block;width:100%;height:100%;object-fit:cover}
.stack{display:grid;gap:12px}

/* quote builder */
.quote{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:20px}
.quote .mono{color:var(--clay)}
.len-row{display:grid;grid-template-columns:auto 1fr;gap:8px 12px;align-items:start;padding:12px 0;border-top:1px solid var(--line);cursor:pointer}
.len-row input{margin-top:5px;accent-color:var(--clay)}
.len-name{font-weight:600}
.len-desc{grid-column:2;color:var(--mute);font-size:.86rem;margin-top:-4px}
.field{display:grid;gap:6px;margin-top:14px}
.field label{font-size:.82rem;color:var(--mute);font-weight:600}
.field select,.field input{padding:12px 14px;border-radius:11px;border:1px solid var(--line);font:16px Inter;background:#fff;color:var(--ink)}
.grid2{display:grid;gap:16px}
@media(min-width:860px){.grid2{grid-template-columns:1.05fr .95fr;gap:24px}}

/* services */
.svc{display:grid;gap:14px}
@media(min-width:760px){.svc{grid-template-columns:repeat(3,1fr)}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px}
.card .mono{color:var(--mute)}
.card h3{margin-top:8px;color:var(--ink)}

/* faq / contact / footer */
.faq{background:#fff;border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:2px 16px}
.faq summary{cursor:pointer;padding:14px 0;font-weight:600;list-style:none}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--clay);font-weight:700}
.faq[open] summary::after{content:"–"}
.faq p{margin:0 0 14px;color:#2C4C53}
.contact{background:var(--ink);color:#fff;border-radius:var(--r);padding:22px}
.contact h3{color:#fff}
.contact .mono{color:var(--amber)}
.row{display:flex;gap:12px;padding:11px 0;border-top:1px solid rgba(255,255,255,.15);font-size:.95rem}
.row .k{min-width:92px;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--amber);padding-top:3px}
footer{background:var(--ink);color:#CBE0E3;padding:28px 0 96px;font-size:.86rem}
footer a{color:#fff}
.sticky-wa{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;display:flex;gap:10px}
.sticky-wa a{flex:1;justify-content:center;padding:15px 18px;border-radius:14px;text-decoration:none;font-weight:700;display:flex;align-items:center;gap:9px}
.sticky-wa .w{background:var(--wa);color:#fff;box-shadow:0 8px 22px rgba(11,122,62,.35)}
.sticky-wa .c{background:#fff;color:var(--ink);border:1px solid var(--line)}
.sticky-wa svg{width:18px;height:18px;fill:currentColor}
@media(min-width:900px){.sticky-wa{display:none}footer{padding-bottom:28px}.nav nav{display:flex}.cta.small{display:inline-flex}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
"""

HTML = f"""<!doctype html>
<html lang="fr" data-lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Opticien à Douala — contrôle de la vue, montures et devis par WhatsApp</title>
<meta name="description" content="Concept de site pour opticien : contrôle de la vue sur rendez-vous, choix de la forme de monture, devis verres et réparations par WhatsApp, en français et en anglais.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0E3B43">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{JSONLD}</script>
</head>
<body>

<div class="top"><div class="wrap">
  <span><span class="fr-only">Contrôle de la vue sur rendez-vous · Douala</span><span class="en-only">Eye check by appointment · Douala</span></span>
  <a href="tel:{WA_LABEL}">{WA_LABEL}</a>
</div></div>

<header class="nav"><div class="wrap">
  <a class="brand" href="#top" aria-label="Opticien">
    <svg width="38" height="38" viewBox="0 0 38 38" role="img" aria-hidden="true">
      <rect width="38" height="38" rx="12" fill="#0E3B43"/>
      <g fill="none" stroke="#F0A03C" stroke-width="2.4"><circle cx="13.5" cy="20" r="6.5"/><circle cx="24.5" cy="20" r="6.5"/><path d="M20 20h-2M7 17.5 10 14M31 17.5 28 14"/></g>
    </svg>
    <span><b>Votre Opticien</b><span class="sub"><span class="fr-only">Concept de démonstration · Douala</span><span class="en-only">Demo concept · Douala</span></span></span>
  </a>
  <nav>
    <a href="#formes"><span class="fr-only">Choisir ma forme</span><span class="en-only">Find my shape</span></a>
    <a href="#verres"><span class="fr-only">Verres &amp; devis</span><span class="en-only">Lenses &amp; quote</span></a>
    <a href="#services"><span class="fr-only">Services</span><span class="en-only">Services</span></a>
    <a href="#contact"><span class="fr-only">Venir</span><span class="en-only">Visit</span></a>
  </nav>
  <div class="lang" role="group" aria-label="Langue / Language">
    <button id="btn-fr" class="is-on" type="button">FR</button>
    <button id="btn-en" type="button">EN</button>
  </div>
  <a class="cta small" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20un%20rendez-vous%20pour%20un%20contr%C3%B4le%20de%20la%20vue.">
    <span class="fr-only">Rendez-vous</span><span class="en-only">Book now</span>
  </a>
</div></header>

<main id="top">

<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="mono" style="color:var(--clay)"><span class="fr-only">Opticien · contrôle de la vue · montage</span><span class="en-only">Optician · eye check · lens fitting</span></p>
    <h1><span class="fr-only">Voir net. <em>Se voir bien.</em></span><span class="en-only">See clearly. <em>Look right.</em></span></h1>
    <p class="lede"><span class="fr-only">Contrôle de la vue sur rendez-vous, conseil sur la forme de votre visage, et un devis verres qui arrive sur WhatsApp avant que vous ne vous déplaciez.</span>
      <span class="en-only">An eye check by appointment, advice on your face shape, and a lens quote that reaches you on WhatsApp before you travel.</span></p>
    <div class="actions">
      <a class="btn btn-primary" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20pour%20un%20contr%C3%B4le%20de%20la%20vue.">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
        <span class="fr-only">Prendre rendez-vous</span><span class="en-only">Book an appointment</span>
      </a>
      <a class="btn btn-ghost" href="#formes"><span class="fr-only">Choisir ma forme</span><span class="en-only">Find my shape</span></a>
    </div>
    <div class="facts">
      <span class="fact"><b>15 min</b> <span class="fr-only">contrôle de la vue</span><span class="en-only">eye check</span></span>
      <span class="fact"><b>WA</b> <span class="fr-only">devis avant déplacement</span><span class="en-only">quote before you come</span></span>
      <span class="fact"><b>FR / EN</b></span>
      <span class="fact"><span class="fr-only">Réparation & ajustement</span><span class="en-only">Repairs &amp; adjustments</span></span>
    </div>
  </div>
  <div class="hero-media">
    <img src="{IMG_HERO}" alt="Opticienne testant la vue d'un client avec une monture d'essai">
    <span class="tag mono"><span class="fr-only">Contrôle de la vue en boutique</span><span class="en-only">Eye check in store</span></span>
  </div>
</div></section>

<section id="formes" class="shapes"><div class="wrap">
  <p class="mono"><span class="fr-only">Choisir sa monture</span><span class="en-only">Choosing a frame</span></p>
  <h2><span class="fr-only">Quelle forme pour votre visage ?</span><span class="en-only">Which shape suits your face?</span></h2>
  <p style="color:#CBE0E3;max-width:60ch"><span class="fr-only">Touchez une forme : vous voyez à qui elle va, et vous pouvez la demander directement sur WhatsApp — on vous envoie les modèles disponibles dans cette forme.</span>
    <span class="en-only">Tap a shape: see who it suits, then ask for it straight on WhatsApp — we send you the models available in that shape.</span></p>
  <div class="mirror-grid">
    <figure class="mirror">
      {FACE_SVG}
      <figcaption class="mono"><span class="fr-only">Illustration — l'essayage réel se fait en boutique</span><span class="en-only">Illustration — real try-on happens in store</span></figcaption>
    </figure>
    <div class="mirror-side">
      <div class="tabs" role="tablist" aria-label="Formes de monture">{SHAPE_HTML}</div>
      <div class="shape-panel" id="shapePanel">
        <h3 id="shapeTitle"><span class="fr-only">Rond</span><span class="en-only">Round</span></h3>
        <p id="shapeDesc"><span class="fr-only">Adoucit les visages anguleux (mâchoire marquée, front large).</span><span class="en-only">Softens angular faces (strong jaw, broad forehead).</span></p>
        <div class="who">
          <span class="fr-only">Essayage en boutique</span><span class="en-only">Try-on in store</span>
          <span class="fr-only">Ajustement offert après montage</span><span class="en-only">Free adjustment after fitting</span>
        </div>
        <div class="actions">
          <a class="btn btn-alt" id="shapeCta" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20cherche%20une%20monture%20ronde.">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
            <span class="fr-only">Demander cette forme</span><span class="en-only">Ask for this shape</span>
          </a>
        </div>
      </div>
    </div>
  </div>

<section><div class="wrap">
  <p class="mono" style="color:var(--clay)"><span class="fr-only">La boutique</span><span class="en-only">The shop</span></p>
  <h2><span class="fr-only">Des montures qu'on essaie, pas qu'on devine.</span><span class="en-only">Frames you try, not frames you guess at.</span></h2>
  <div class="wall">
    <div class="shot"><img src="{IMG_FRAMES}" alt="Présentoir de montures colorées dans une boutique d'optique" style="aspect-ratio:16/11"></div>
    <div class="stack">
      <div class="shot"><img src="{IMG_TRYON}" alt="Cliente essayant une monture devant le miroir" style="aspect-ratio:4/5"></div>
      <div class="card">
        <span class="mono"><span class="fr-only">Photos</span><span class="en-only">Photos</span></span>
        <p><span class="fr-only">Les visuels ci-dessus sont des exemples : vos vraies montures, en photos, remplacent ces images en 24 h.</span>
          <span class="en-only">The visuals above are examples: your real frames, in photos, replace them within 24 hours.</span></p>
      </div>
    </div>
  </div>
</div></section>

<section id="verres" class="hair"><div class="wrap">
  <p class="mono" style="color:var(--clay)"><span class="fr-only">Verres &amp; devis</span><span class="en-only">Lenses &amp; quote</span></p>
  <h2><span class="fr-only">Composez votre demande, recevez le prix.</span><span class="en-only">Build your request, get the price.</span></h2>
  <div class="grid2" style="margin-top:22px">
    <div class="quote">
      <span class="mono"><span class="fr-only">1 · type de verres</span><span class="en-only">1 · lens type</span></span>
      <div id="lensList">{LENS_HTML}</div>
      <div class="field">
        <label for="who"><span class="fr-only">2 · pour qui</span><span class="en-only">2 · who is it for</span></label>
        <select id="who">
          <option data-fr="Adulte" data-en="Adult">Adulte / Adult</option>
          <option data-fr="Enfant" data-en="Child">Enfant / Child</option>
          <option data-fr="Senior" data-en="Senior">Senior / Senior</option>
        </select>
      </div>
      <div class="field">
        <label for="kind"><span class="fr-only">3 · usage principal</span><span class="en-only">3 · main use</span></label>
        <select id="kind">
          <option data-fr="Bureau / écran" data-en="Office / screen">Bureau / écran · Office / screen</option>
          <option data-fr="Conduite" data-en="Driving">Conduite · Driving</option>
          <option data-fr="Lecture" data-en="Reading">Lecture · Reading</option>
          <option data-fr="Soleil" data-en="Sun">Soleil · Sun</option>
        </select>
      </div>
      <div class="actions">
        <button class="btn btn-primary" id="quoteBtn" type="button">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
          <span class="fr-only">Envoyer ma demande</span><span class="en-only">Send my request</span>
        </button>
      </div>
      <p class="mono" style="color:var(--mute);margin-top:12px"><span class="fr-only">Aucun prix inventé : votre devis est calculé par l'opticien.</span><span class="en-only">No invented prices: the quote is set by the optician.</span></p>
    </div>
    <div class="card">
      <span class="mono"><span class="fr-only">Bon à savoir</span><span class="en-only">Good to know</span></span>
      <h3><span class="fr-only">Ce qui fait le prix d'une paire</span><span class="en-only">What drives the price of a pair</span></h3>
      <p><span class="fr-only">La correction (simple ou complexe), le type de verre, le traitement (anti-reflet, anti-lumière bleue, photochromique) et la monture. Envoyez votre ordonnance : on vous dit ce dont vous avez réellement besoin, sans sur-vendre.</span>
        <span class="en-only">The correction (simple or complex), the lens type, the coating (anti-reflective, blue-light, photochromic) and the frame. Send your prescription: we tell you what you actually need, without upselling.</span></p>
      <div class="actions">
        <a class="btn btn-ghost" href="https://wa.me/{WA}?text=Bonjour%2C%20j%27envoie%20mon%20ordonnance%20pour%20un%20devis.">
          <span class="fr-only">Envoyer mon ordonnance</span><span class="en-only">Send my prescription</span></a>
      </div>
    </div>
  </div>
</div></section>

<section id="services" class="hair"><div class="wrap">
  <p class="mono" style="color:var(--clay)"><span class="fr-only">Services</span><span class="en-only">Services</span></p>
  <h2><span class="fr-only">Cinq choses qu'un opticien fait pour vous.</span><span class="en-only">Five things an optician does for you.</span></h2>
  <div class="svc" style="margin-top:22px">
    <div class="card"><span class="mono">01</span><h3><span class="fr-only">Contrôle de la vue</span><span class="en-only">Eye check</span></h3>
      <p><span class="fr-only">Sur rendez-vous, en boutique, une quinzaine de minutes.</span><span class="en-only">By appointment, in store, about fifteen minutes.</span></p></div>
    <div class="card"><span class="mono">02</span><h3><span class="fr-only">Montage &amp; ajustement</span><span class="en-only">Fitting &amp; adjustment</span></h3>
      <p><span class="fr-only">Vos verres montés sur mesure, ajustés après quelques jours d'usage.</span><span class="en-only">Your lenses fitted to measure, adjusted after a few days of wear.</span></p></div>
    <div class="card"><span class="mono">03</span><h3><span class="fr-only">Réparation</span><span class="en-only">Repairs</span></h3>
      <p><span class="fr-only">Vis, plaquettes, branches tordues : passez, on regarde sur place.</span><span class="en-only">Screws, nose pads, bent arms: come in, we look at them on the spot.</span></p></div>
    <div class="card"><span class="mono">04</span><h3><span class="fr-only">Lentilles de contact</span><span class="en-only">Contact lenses</span></h3>
      <p><span class="fr-only">Essai et apprentissage de la pose, puis réapprovisionnement.</span><span class="en-only">Trial and insertion training, then refills.</span></p></div>
    <div class="card"><span class="mono">05</span><h3><span class="fr-only">Lunettes de soleil</span><span class="en-only">Sunglasses</span></h3>
      <p><span class="fr-only">Avec ou sans correction — demandez les modèles disponibles.</span><span class="en-only">With or without correction — ask which models are in stock.</span></p></div>
    <div class="card"><span class="mono">06</span><h3><span class="fr-only">Enfants</span><span class="en-only">Children</span></h3>
      <p><span class="fr-only">Montures solides, verres adaptés, ajustement refait après quelques jours.</span><span class="en-only">Sturdy frames, suited lenses, re-adjusted after a few days.</span></p></div>
  </div>
</div></section>

<section class="hair"><div class="wrap">
  <p class="mono" style="color:var(--clay)"><span class="fr-only">Questions fréquentes</span><span class="en-only">Frequently asked</span></p>
  <h2 style="margin-bottom:16px"><span class="fr-only">Ce qu'on nous demande au comptoir.</span><span class="en-only">What people ask at the counter.</span></h2>
{FAQ_HTML}
</div></section>

<section id="contact" class="hair"><div class="wrap">
  <p class="mono" style="color:var(--clay)"><span class="fr-only">Venir</span><span class="en-only">Visit</span></p>
  <h2><span class="fr-only">Une visite, ou juste un message.</span><span class="en-only">A visit, or just a message.</span></h2>
  <div class="contact" style="margin-top:22px;max-width:640px">
    <div class="row"><span class="k">WhatsApp</span><span><a href="https://wa.me/{WA}">{WA_LABEL}</a></span></div>
    <div class="row"><span class="k"><span class="fr-only">Horaires</span><span class="en-only">Hours</span></span><span><span class="fr-only">Lun–Sam · à confirmer avec vos horaires réels</span><span class="en-only">Mon–Sat · to be set to your real hours</span></span></div>
    <div class="row"><span class="k"><span class="fr-only">Adresse</span><span class="en-only">Address</span></span><span><span class="fr-only">Douala — votre adresse et votre repère ici</span><span class="en-only">Douala — your address and landmark here</span></span></div>
    <div class="row"><span class="k"><span class="fr-only">Paiement</span><span class="en-only">Payment</span></span><span><span class="fr-only">Espèces · Mobile Money — à confirmer</span><span class="en-only">Cash · Mobile Money — to be confirmed</span></span></div>
  </div>
</div></section>

</main>

<footer><div class="wrap">
  <p><b>Votre Opticien</b> — <span class="fr-only">concept de démonstration préparé par AMK</span><span class="en-only">demonstration concept prepared by AMK</span><br>
  <span class="fr-only">Tous les textes, horaires, prix et photos sont des emplacements : votre contenu réel les remplace à la mise en ligne.</span>
  <span class="en-only">All text, hours, prices and photos are placeholders: your real content replaces them at launch.</span></p>
</div></footer>

<div class="sticky-wa">
  <a class="w" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20un%20rendez-vous.">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
    <span class="fr-only">WhatsApp</span><span class="en-only">WhatsApp</span>
  </a>
  <a class="c" href="tel:{WA_LABEL}"><span class="fr-only">Appeler</span><span class="en-only">Call</span></a>
</div>

<script>
(function(){{
  var html=document.documentElement, k='opticien-lang';
  function setLang(l){{
    html.setAttribute('data-lang',l); html.lang=l;
    document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
    document.getElementById('btn-en').classList.toggle('is-on',l==='en');
    try{{localStorage.setItem(k,l)}}catch(e){{}}
    var sel=document.getElementById('who');
    [].forEach.call(sel.options,function(o){{o.textContent=o.dataset[l]}});
    var sel2=document.getElementById('kind');
    [].forEach.call(sel2.options,function(o){{o.textContent=(l==='fr'?o.dataset.fr:o.dataset.en)}});
    var qi=document.getElementById('quoteBtn'); if(qi){{}}
    updateShape();
  }}
  document.getElementById('btn-fr').addEventListener('click',function(){{setLang('fr')}});
  document.getElementById('btn-en').addEventListener('click',function(){{setLang('en')}});
  try{{ var saved=localStorage.getItem(k); if(saved) setLang(saved); }}catch(e){{}}

  // shape selector
  var shapes=[{{SHAPES_JS}}];
  var tabs=[].slice.call(document.querySelectorAll('.shape.tab'));
  function updateShape(){{
    var cur=document.querySelector('.shape.tab.is-on'); if(!cur) return;
    var s=shapes.filter(function(x){{return x.key===cur.dataset.shape}})[0]; if(!s) return;
    var l=html.getAttribute('data-lang');
    document.getElementById('shapeTitle').innerHTML='<span class="'+(l==='fr'?'fr-only':'en-only')+'">'+(l==='fr'?s.fr:s.en)+'</span>';
    document.getElementById('shapeDesc').innerHTML='<span class="'+(l==='fr'?'fr-only':'en-only')+'">'+(l==='fr'?s.dfr:s.den)+'</span>';
    var msg=(l==='fr'?'Bonjour, je cherche une monture '+s.fr.toLowerCase()+'.':'Hello, I am looking for a '+s.en.toLowerCase()+' frame.');
    document.getElementById('shapeCta').href='https://wa.me/{WA}?text='+encodeURIComponent(msg);
    var fg=document.querySelectorAll('.mirror .frame');
    [].forEach.call(fg,function(g){{g.classList.toggle('is-on', g.getAttribute('data-k')===s.key)}});
  }}
  tabs.forEach(function(t){{t.addEventListener('click',function(){{
    tabs.forEach(function(x){{x.classList.remove('is-on'); x.setAttribute('aria-selected','false')}});
    t.classList.add('is-on'); t.setAttribute('aria-selected','true'); updateShape();
  }})}});
  updateShape();

  // quote builder -> WhatsApp
  document.getElementById('quoteBtn').addEventListener('click',function(){{
    var l=html.getAttribute('data-lang');
    var lens=document.querySelector('input[name=lens]:checked');
    var lensTxt=lens?(l==='fr'?lens.value:lens.dataset.en):(l==='fr'?'(type de verres à préciser)':'(lens type to confirm)');
    var who=document.getElementById('who'); var whoTxt=who.options[who.selectedIndex].textContent;
    var kind=document.getElementById('kind'); var kindTxt=kind.options[kind.selectedIndex].textContent;
    var msg=(l==='fr'
      ? 'Bonjour, je souhaite un devis :\\n• Verres : '+lensTxt+'\\n• Pour : '+whoTxt+'\\n• Usage : '+kindTxt+'\\n(Je peux envoyer mon ordonnance ici.)'
      : 'Hello, I would like a quote:\\n• Lenses: '+lensTxt+'\\n• For: '+whoTxt+'\\n• Main use: '+kindTxt+'\\n(I can send my prescription here.)');
    window.open('https://wa.me/{WA}?text='+encodeURIComponent(msg),'_blank','noopener');
  }});

  // default lens selection
  var first=document.querySelector('input[name=lens]'); if(first) first.checked=true;
}})();
</script>
</body>
</html>
"""

shapes_js = ",\n".join(
    f'{{key:"{key}",fr:"{fr}",en:"{en}",dfr:"{d_fr.replace(chr(34), chr(39))}",den:"{d_en.replace(chr(34), chr(39))}"}}'
    for fr, en, key, d_fr, d_en in SHAPES)
HTML = HTML.replace("{SHAPES_JS}", shapes_js)
OUT.write_text(HTML, encoding='utf-8')
print(f"OK {OUT} — {OUT.stat().st_size/1024:.0f} KB")
