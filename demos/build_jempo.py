#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AMK — J&E MEMORIAL POLYCLINIC « JEMPO » (Deido/Bessengue, Douala) — named concept
Direction « LA PORTE » : la porte d'entrée propre. Une porte entrouverte en hero,
puis la « réception » — on choisit la spécialité, on voit le praticien et ses jours
tels qu'ils sont publiés, et le rendez-vous part sur WhatsApp en deux taps.

FIRST BUILD UNDER §20 FOOTER STANDARD (AMK-DESIGN-SKILLS.md, King 17 Sep 2026):
4 blocks (brand+line · doormat nav · CTA = hero action · contact) + strip (© · retour en haut).

Output: demos/concept-jempo-v1.html   (single file, base64 images, FR|EN)
Usage:  python3 demos/build_jempo.py [--wa 2376XXXXXXXX] [--out name.html]
"""
import base64, io, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path('/home/user/AMK')
WA = "237696710699"            # verified WhatsApp Business line (King, 17 Sep 2026)
OUT_NAME = "concept-jempo-v1.html"
WA_LABEL = '+237 696 71 06 99'
if "--wa" in sys.argv:
    WA = sys.argv[sys.argv.index("--wa") + 1]
    WA_LABEL = '+237 ' + WA[3:6] + ' ' + WA[6:8] + ' ' + WA[8:10] + ' ' + WA[10:12]
if "--out" in sys.argv:
    OUT_NAME = sys.argv[sys.argv.index("--out") + 1]
OUT = ROOT / 'demos' / OUT_NAME

PHONE_2 = "670 85 85 42"
PHONE_FIXE = "233 47 87 69"

def b64(path, width, quality=76):
    im = Image.open(ROOT / path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

IMG_HERO = b64('demos/img/jempo-hero.jpg', 1000, 76)

# ---- the four practitioners, as published on their own MonDocteur237 cards
# (name / specialty / days & hours / how the patient should ask for it)
DOCS = [
    ("orl", "ORL", "ENT",
     "Dr Marcus Youda", "Dr Marcus Youda",
     "Lun–Ven 08:00–17:30 · Sam 08:00–13:00",
     "Mon–Fri 08:00–17:30 · Sat 08:00–13:00",
     "Nez qui coule, maux de gorge, otites, audition, sinus…",
     "Runny nose, sore throat, ear infections, hearing, sinuses…",
     "le Dr Marcus Youda (ORL)", "Dr Marcus Youda (ENT)"),
    ("dermato", "Dermatologie", "Dermatology",
     "Dr Angelique Njeumen", "Dr Angelique Njeumen",
     "Lun–Ven 14:00–16:00 · Mer jusqu'à 17:00",
     "Mon–Fri 14:00–16:00 · Wed until 17:00",
     "Peau, boutons, mycoses, plaques, cheveux…",
     "Skin, spots, fungal infections, patches, hair…",
     "le Dr Angelique Njeumen (dermatologue)", "Dr Angelique Njeumen (dermatologist)"),
    ("diabete", "Diabétologie", "Diabetology",
     "Dr Paul Djomaleu", "Dr Paul Djomaleu",
     "Lun–Ven 13:00–15:00",
     "Mon–Fri 13:00–15:00",
     "Suivi du diabète, glycémie, fatigue, soif constante…",
     "Diabetes follow-up, blood sugar, tiredness, constant thirst…",
     "le Dr Paul Djomaleu (diabétologue)", "Dr Paul Djomaleu (diabetologist)"),
    ("gyneco", "Gynécologie", "Gynaecology",
     "Dr Humphry Neng", "Dr Humphry Neng",
     "Lun–Ven 16:00–20:00",
     "Mon–Fri 16:00–20:00",
     "Suivi, infections, douleurs, grossesse, contraception…",
     "Check-ups, infections, pain, pregnancy, contraception…",
     "le Dr Humphry Neng (gynécologue)", "Dr Humphry Neng (gynaecologist)"),
]

DOC_CARDS = "\n".join(f'''      <button class="door tab{' is-on' if i == 0 else ''}" type="button" role="tab" data-k="{k}" aria-selected="{'true' if i == 0 else 'false'}">
        <span class="knob" aria-hidden="true"></span>
        <span class="d-name"><span class="fr-only">{fr}</span><span class="en-only">{en}</span></span>
        <span class="d-doc">{doc_fr}</span>
        <span class="d-hours fr-only">{h_fr}</span>
        <span class="d-hours en-only">{h_en}</span>
      </button>''' for i, (k, fr, en, doc_fr, doc_en, h_fr, h_en, c_fr, c_en, ask_fr, ask_en) in enumerate(DOCS))

FAQ = [
    ("Faut-il une ordonnance pour consulter un spécialiste ?", "Do I need a referral to see a specialist?",
     "Non. Vous pouvez venir directement — dites à l'accueil ou sur WhatsApp quelle consultation vous cherchez, on vous oriente vers le bon praticien.",
     "No. You can come directly — tell the desk or send a WhatsApp message about the consultation you need, and we point you to the right practitioner."),
    ("La polyclinique est-elle ouverte tous les jours ?", "Is the polyclinic open every day?",
     "Oui, l'accueil est ouvert 24h/24, tous les jours. Les consultations des spécialistes se font aux jours et heures affichés ; la nuit et le week-end, appelez d'abord.",
     "Yes, the reception is open 24 hours a day, every day. Specialist consultations run at the days and hours shown; at night and at weekends, call first."),
    ("Où se trouve JEMPO exactement ?", "Where exactly is JEMPO?",
     "1 149 Boulevard de la République, à Deido — Vallée Bessengue, face à l'hôtel LEWAT. Accessible en taxi ou moto-taxi.",
     "1,149 Boulevard de la République, Deido — Vallée Bessengue, opposite the LEWAT hotel. Easy to reach by taxi or moto-taxi."),
    ("Comment payer ? Et l'assurance ?", "How do I pay? And insurance?",
     "Espèces, MTN Mobile Money et Orange Money sont acceptés. Pour une assurance, envoyez le nom de votre assureur sur WhatsApp avant la visite : nous vous confirmons la prise en charge.",
     "Cash, MTN Mobile Money and Orange Money are accepted. For insurance, send your insurer's name on WhatsApp before the visit and we confirm the cover."),
    ("Est-ce que je peux écrire en anglais ?", "Can I write in English?",
     "Oui. La page se lit en français et en anglais, et vos messages WhatsApp sont lus dans les deux langues.",
     "Yes. This page reads in French and English, and your WhatsApp messages are read in both languages."),
]
FAQ_HTML = "\n".join(f'''  <details class="faq">
    <summary><span class="fr-only">{q_fr}</span><span class="en-only">{q_en}</span></summary>
    <p><span class="fr-only">{a_fr}</span><span class="en-only">{a_en}</span></p>
  </details>''' for q_fr, q_en, a_fr, a_en in FAQ)

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "MedicalClinic",
    "name": "J&E Memorial Polyclinic (JEMPO)",
    "description": "Polyclinique à Deido (Vallée Bessengue), Douala : ORL, dermatologie, diabétologie et gynécologie sur rendez-vous, accueil 24h/24. Concept de démonstration préparé par AMK.",
    "telephone": "+237696710699",
    "address": {"@type": "PostalAddress", "streetAddress": "1 149 Boulevard de la République, Deido — Vallée Bessengue",
                "addressLocality": "Douala", "addressCountry": "CM"},
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                  "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                  "opens": "00:00", "closes": "23:59"},
    "medicalSpecialty": ["Otolaryngologic", "Dermatologic", "Gynecologic"],
    "availableLanguage": ["French", "English"],
}, ensure_ascii=False, indent=2)

CSS = """
:root{
 --ink:#2A211C; --ink-2:#4A3A31; --body:#3E312A;
 --clay:#C2542B; --clay-d:#9E3F1D; --clay-l:#E8A87C;
 --sand:#F7F1E9; --sand-2:#EFE5D9; --paper:#fff; --line:rgba(42,33,28,.15);
 --wa:#0B7A3E; --r:16px; --max:1120px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--sand);color:var(--ink);
 font:16px/1.62 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3,.display{font-family:Archivo,-apple-system,"Segoe UI",Arial,sans-serif;font-weight:700;line-height:1.1;margin:0;letter-spacing:-.015em;color:var(--ink)}
h1{font-size:clamp(2rem,7.4vw,3.4rem);font-weight:800;line-height:1.03}
h2{font-size:clamp(1.4rem,4.6vw,2.05rem)}
h3{font-size:1.05rem;font-weight:700}
p{margin:.55rem 0 0}
a{color:var(--clay-d)}
.mono{font-family:Archivo,sans-serif;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--clay-d)}
.wrap{max-width:var(--max);margin:0 auto;padding:0 18px}
section{padding:52px 0}
.hair{border-top:1px solid var(--line)}
html[data-lang="fr"] .en-only{display:none !important}
html[data-lang="en"] .fr-only{display:none !important}
html[data-lang="en"] .en-only{display:revert !important}
html[data-lang="fr"] .fr-only{display:revert !important}
:is(a,button,label,summary):focus-visible{outline:3px solid var(--clay);outline-offset:2px;border-radius:10px}

/* top + nav */
.top{background:var(--ink);color:#EFE5D9;font-size:.8rem}
.top .wrap{display:flex;gap:12px;justify-content:space-between;align-items:center;padding:9px 18px;flex-wrap:wrap}
.top a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4)}
.nav{position:sticky;top:0;z-index:40;background:rgba(247,241,233,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:12px;padding:10px 18px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}
.brand b{font-family:Archivo,sans-serif;font-weight:800;font-size:1.04rem;display:block;line-height:1.05;letter-spacing:-.01em}
.brand .bsub{display:block;font-size:.62rem;color:var(--ink-2);letter-spacing:.1em;text-transform:uppercase;font-weight:600}
.nav nav{margin-left:auto;display:none;gap:16px;font-size:.9rem}
.nav nav a{text-decoration:none;color:var(--ink);opacity:.86}
.lang{display:flex;margin-left:auto;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:#fff}
.lang button{border:0;background:transparent;padding:7px 12px;font:700 .78rem Archivo,sans-serif;color:var(--ink-2);cursor:pointer}
.lang button.is-on{background:var(--ink);color:#fff}
.cta{background:var(--wa);color:#fff;text-decoration:none;padding:11px 15px;border-radius:999px;font-weight:700;font-size:.86rem;white-space:nowrap}
.cta.small{display:none}

/* hero */
.hero{padding-top:30px}
.hero-grid{display:grid;gap:26px;align-items:center}
.hero h1 em{font-style:normal;color:var(--clay)}
.lede{font-size:1.04rem;color:var(--body);max-width:56ch}
.hero-media{position:relative;border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}
.hero-media img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.tag{position:absolute;left:12px;bottom:12px;background:rgba(42,33,28,.9);color:#F7F1E9;padding:7px 11px;border-radius:10px;font-size:.7rem}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 18px;border-radius:12px;text-decoration:none;font-weight:700;border:1px solid transparent;cursor:pointer;font:inherit;font-weight:700}
.btn-primary{background:var(--wa);color:#fff}
.btn-ghost{background:#fff;color:var(--ink);border-color:var(--line)}
.btn-dark{background:var(--ink);color:#F7F1E9}
.btn-line{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}
.btn svg{width:18px;height:18px;fill:currentColor}
.facts{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}
.fact{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 13px;font-size:.8rem;color:var(--body)}
.fact b{color:var(--ink)}

/* la réception — signature */
.reception{background:var(--ink);color:#F2EAE0}
.reception h2{color:#fff}
.reception .mono{color:var(--clay-l)}
.reception .sub{color:#D8CCC0;max-width:64ch}
.doors{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:24px 0 16px}
@media(min-width:760px){.doors{grid-template-columns:repeat(4,1fr)}}
.door{position:relative;display:flex;flex-direction:column;gap:4px;text-align:left;background:rgba(255,255,255,.05);
 border:1px solid rgba(255,255,255,.2);color:#F2EAE0;border-radius:14px;padding:16px 14px 14px;cursor:pointer;font:inherit}
.door .knob{position:absolute;right:13px;top:16px;width:9px;height:9px;border-radius:999px;background:var(--clay-l)}
.door .d-name{font-family:Archivo,sans-serif;font-weight:700;font-size:1rem}
.door .d-doc{font-size:.8rem;color:#CDBFB2}
.door .d-hours{font-size:.74rem;color:#B7A79A;margin-top:2px}
.door.is-on{background:var(--clay-d);border-color:var(--clay-d);color:#fff}
.door.is-on .d-doc{color:#FBE3D4}
.door.is-on .d-hours{color:#F6CFB9}
.door.is-on .knob{background:#fff}
.rec-panel{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:16px;padding:20px}
.rec-panel h3{color:#fff;font-size:1.3rem;font-family:Archivo,sans-serif}
.rec-panel .who{color:#D8CCC0}
.rec-rows{margin-top:12px}
.rec-row{display:flex;gap:12px;padding:10px 0;border-top:1px solid rgba(255,255,255,.14);font-size:.95rem;flex-wrap:wrap}
.rec-row:first-child{border-top:0}
.rec-row .k{min-width:112px;font-family:Archivo,sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--clay-l);padding-top:3px}
.rec-row .v{color:#EFE5D9}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.chips span{background:rgba(232,168,124,.14);border:1px solid rgba(232,168,124,.4);color:#F6CFB9;border-radius:999px;padding:6px 12px;font-size:.78rem}
.rec-cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.btn-clay{background:var(--clay-d);color:#fff}
.small-note{font-size:.78rem;color:#B7A79A;margin-top:12px}

/* 24/7 band */
.band{background:var(--clay-d);color:#FFF1E7}
.band h2{color:#fff}
.band .mono{color:#FFE3CE}
.band p{color:#FFE7D6;max-width:62ch}
.band .actions{margin-top:18px}
.band .btn-on{background:#fff;color:#8F3A1B}
.band .btn-line{background:transparent;color:#fff;border-color:rgba(255,255,255,.55)}

/* access */
.find-grid{display:grid;gap:22px;margin-top:24px}
@media(min-width:900px){.find-grid{grid-template-columns:1.05fr .95fr;gap:28px;align-items:start}}
.info{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:6px 18px}
.irow{display:flex;gap:12px;padding:14px 0;border-top:1px solid var(--line)}
.irow:first-child{border-top:0}
.irow .k{min-width:112px;font-family:Archivo,sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--clay-d);padding-top:3px}
.irow p{margin:0;color:var(--body)}
.mapcard{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:16px}
.mapcard svg{display:block;width:100%;height:auto}
.mapcard .cap{font-size:.78rem;color:var(--ink-2);margin-top:10px}

/* faq + contact + footer (§20 first application) */
.faq{background:#fff;border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:2px 16px}
.faq summary{cursor:pointer;padding:14px 0;font-weight:700;color:var(--ink);list-style:none;font-family:Archivo,sans-serif;font-size:.95rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--clay);font-weight:800}
.faq[open] summary::after{content:"–"}
.faq p{margin:0 0 14px;color:var(--body)}
.contact{background:var(--ink);color:#F2EAE0;border-radius:var(--r);padding:20px;margin-top:22px}
.contact .mono{color:var(--clay-l)}
.contact h3{color:#fff}
.crow{display:flex;gap:12px;padding:12px 0;border-top:1px solid rgba(255,255,255,.16);font-size:.95rem;flex-wrap:wrap}
.crow:first-of-type{border-top:0}
.crow .k{min-width:112px;font-family:Archivo,sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--clay-l);padding-top:3px}
.crow a{color:#fff}

/* §20 FOOTER */
.footer{background:#1E1712;color:#D8CCC0;padding:46px 0 0;font-size:.9rem}
.f-grid{display:grid;gap:26px}
@media(min-width:860px){.f-grid{grid-template-columns:1.35fr .8fr 1fr 1.05fr;gap:30px}}
.f-brand b{font-family:Archivo,sans-serif;font-weight:800;font-size:1.35rem;color:#fff;display:block;letter-spacing:-.01em}
.f-brand .line{color:#B7A79A;margin-top:8px;max-width:34ch}
.f-ttl{font-family:Archivo,sans-serif;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700;color:var(--clay-l);margin-bottom:10px}
.f-col a{display:block;color:#EFE5D9;text-decoration:none;padding:4px 0}
.f-col a:hover{color:#fff;text-decoration:underline}
.footer a{color:#EFE5D9}
.f-cta{background:var(--clay-d);border-radius:14px;padding:16px}
.f-cta p{margin:0 0 12px;color:#FFF1E7;font-size:.88rem}
.f-cta a{display:inline-flex;align-items:center;gap:9px;background:#fff;color:#8F3A1B;text-decoration:none;font-weight:700;padding:11px 14px;border-radius:10px;font-size:.9rem}
.f-cta svg{width:16px;height:16px;fill:currentColor}
.f-contact div{padding:3px 0;color:#EFE5D9}
.f-strip{border-top:1px solid rgba(255,255,255,.14);margin-top:34px;padding:16px 0 96px;font-size:.78rem;color:#A9968A}
.f-strip .wrap{display:flex;gap:12px;justify-content:space-between;flex-wrap:wrap;align-items:center}
.f-strip a{color:#D8CCC0}
footer{background:#1E1712}
.sticky-wa{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;display:flex;gap:10px}
.sticky-wa a{flex:1;justify-content:center;padding:15px 18px;border-radius:14px;text-decoration:none;font-weight:700;display:flex;align-items:center;gap:9px}
.sticky-wa .w{background:var(--wa);color:#fff;box-shadow:0 8px 22px rgba(11,122,62,.35)}
.sticky-wa .c{background:#fff;color:var(--ink);border:1px solid var(--line)}
.sticky-wa svg{width:18px;height:18px;fill:currentColor}
@media(min-width:900px){.sticky-wa{display:none}.f-strip{padding-bottom:16px}.nav nav{display:flex}.cta.small{display:inline-flex}.hero-grid{grid-template-columns:1.02fr .98fr;gap:30px}.lang{margin-left:0}}
.rv{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.rv{opacity:1;transform:none;transition:none}*{animation:none!important}}
"""

HTML = f"""<!doctype html>
<html lang="fr" data-lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>J&amp;E Memorial Polyclinic (JEMPO) — ORL, dermatologie, diabétologie, gynécologie · Deido, Douala</title>
<meta name="description" content="Polyclinique JEMPO à Deido (Vallée Bessengue), Douala : ORL, dermatologie, diabétologie et gynécologie sur rendez-vous, accueil 24h/24. Rendez-vous par WhatsApp, en français et en anglais.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#2A211C">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{JSONLD}</script>
</head>
<body>

<div class="top"><div class="wrap">
  <span><span class="fr-only">Accueil ouvert 24h/24 · 7j/7 — Deido, Vallée Bessengue</span><span class="en-only">Reception open 24/7 — Deido, Vallée Bessengue</span></span>
  <a href="tel:+237696710699">{WA_LABEL}</a>
</div></div>

<header class="nav"><div class="wrap">
  <a class="brand" href="#top" aria-label="J&amp;E Memorial Polyclinic">
    <svg width="40" height="40" viewBox="0 0 40 40" role="img" aria-hidden="true">
      <rect width="40" height="40" rx="11" fill="#2A211C"/>
      <path d="M13 30V20a7 7 0 0 1 14 0v10" fill="none" stroke="#C2542B" stroke-width="3.2" stroke-linecap="round"/>
      <path d="M10 30h20" stroke="#F7F1E9" stroke-width="3.2" stroke-linecap="round"/>
      <circle cx="29.5" cy="24.5" r="2.1" fill="#F7F1E9"/>
    </svg>
    <span><b>JEMPO</b>
    <span class="bsub"><span class="fr-only">J&amp;E Memorial Polyclinic · Deido</span><span class="en-only">J&amp;E Memorial Polyclinic · Deido</span></span></span>
  </a>
  <nav>
    <a href="#reception"><span class="fr-only">Consultations</span><span class="en-only">Consultations</span></a>
    <a href="#acces"><span class="fr-only">Accès</span><span class="en-only">Getting here</span></a>
    <a href="#faq"><span class="fr-only">Questions</span><span class="en-only">Questions</span></a>
    <a href="#contact"><span class="fr-only">Contact</span><span class="en-only">Contact</span></a>
  </nav>
  <div class="lang" role="group" aria-label="Langue / Language">
    <button id="btn-fr" class="is-on" type="button">FR</button>
    <button id="btn-en" type="button">EN</button>
  </div>
  <a class="cta small" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20polyclinique.">
    <span class="fr-only">Rendez-vous</span><span class="en-only">Book now</span>
  </a>
</div></header>

<main id="top">

<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="mono"><span class="fr-only">Deido · Vallée Bessengue — face hôtel LEWAT</span><span class="en-only">Deido · Vallée Bessengue — opposite the LEWAT hotel</span></p>
    <h1><span class="fr-only">Poussez la porte : <em>quatre spécialités, un seul endroit.</em></span><span class="en-only">Come through the door: <em>four specialties, one place.</em></span></h1>
    <p class="lede"><span class="fr-only">ORL, dermatologie, diabétologie, gynécologie — les consultations de spécialistes de JEMPO, leurs jours et leurs heures, et un rendez-vous qui part sur WhatsApp en deux taps.</span>
      <span class="en-only">ENT, dermatology, diabetology, gynaecology — JEMPO's specialist consultations, their days and hours, and an appointment that goes to WhatsApp in two taps.</span></p>
    <div class="actions">
      <a class="btn btn-primary" href="#reception">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v16H4z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 12a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z"/></svg>
        <span class="fr-only">Choisir ma consultation</span><span class="en-only">Choose my consultation</span>
      </a>
      <a class="btn btn-ghost" href="tel:+237696710699"><span class="fr-only">Appeler la clinique</span><span class="en-only">Call the clinic</span></a>
    </div>
    <div class="facts">
      <span class="fact"><b>24h/24</b> <span class="fr-only">accueil, tous les jours</span><span class="en-only">reception, every day</span></span>
      <span class="fact"><span class="fr-only">4 spécialités sur rendez-vous</span><span class="en-only">4 specialties by appointment</span></span>
      <span class="fact"><span class="fr-only">MoMo · Orange Money · espèces</span><span class="en-only">MoMo · Orange Money · cash</span></span>
      <span class="fact"><b>FR</b> / <b>EN</b></span>
    </div>
  </div>
  <div class="hero-media rv">
    <img src="{IMG_HERO}" alt="Entrée de la polyclinique : mur terracotta, porte vitrée entrouverte et enseigne blanche">
    <span class="tag mono"><span class="fr-only">Votre porte — l'enseigne est encore à remplir</span><span class="en-only">Your door — the sign is still blank</span></span>
  </div>
</div></section>

<section class="reception" id="reception"><div class="wrap">
  <p class="mono"><span class="fr-only">La réception</span><span class="en-only">The reception</span></p>
  <h2><span class="fr-only">Vous cherchez quelle consultation ?</span><span class="en-only">Which consultation are you looking for?</span></h2>
  <p class="sub"><span class="fr-only">Choisissez la spécialité : vous voyez le praticien et ses jours publiés, puis votre demande part sur WhatsApp — sans expliquer votre cas à voix haute à l'accueil.</span>
    <span class="en-only">Pick the specialty: you see the practitioner and their published days, then your request goes to WhatsApp — without explaining your case out loud at the desk.</span></p>
  <div class="doors" role="tablist" aria-label="Spécialités">
{DOC_CARDS}
  </div>
  <div class="rec-panel">
    <h3 id="recTitle"><span class="fr-only">ORL</span><span class="en-only">ENT</span></h3>
    <p class="who" id="recWho">Dr Marcus Youda — <span class="fr-only">oto-rhino-laryngologiste</span><span class="en-only">ear, nose and throat specialist</span></p>
    <div class="rec-rows">
      <div class="rec-row"><span class="k"><span class="fr-only">Consultations</span><span class="en-only">Consultation days</span></span><span class="v" id="recHours"><span class="fr-only">Lun–Ven 08:00–17:30 · Sam 08:00–13:00</span><span class="en-only">Mon–Fri 08:00–17:30 · Sat 08:00–13:00</span></span></div>
      <div class="rec-row"><span class="k"><span class="fr-only">Motifs fréquents</span><span class="en-only">Common reasons</span></span><span class="v" id="recWhy"><span class="fr-only">Nez qui coule, maux de gorge, otites, audition, sinus…</span><span class="en-only">Runny nose, sore throat, ear infections, hearing, sinuses…</span></span></div>
    </div>
    <div class="chips">
      <span><span class="fr-only">Présentiel ou téléconsultation</span><span class="en-only">In person or teleconsultation</span></span>
      <span><span class="fr-only">Messages lus en FR et EN</span><span class="en-only">Messages read in FR and EN</span></span>
    </div>
    <div class="rec-cta">
      <a class="btn btn-clay" id="recWa" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20un%20rendez-vous%20avec%20le%20Dr%20Marcus%20Youda%20(ORL).">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
        <span class="fr-only">Demander ce rendez-vous</span><span class="en-only">Request this appointment</span>
      </a>
      <a class="btn btn-line" href="tel:+237696710699"><span class="fr-only">Appeler</span><span class="en-only">Call</span></a>
    </div>
    <p class="small-note"><span class="fr-only">Jours et heures affichés d'après vos fiches publiques — à confirmer avant la mise en ligne. Votre numéro WhatsApp reste {WA_LABEL}.</span>
      <span class="en-only">Days and hours shown from your public listings — to confirm before launch. Your WhatsApp number stays {WA_LABEL}.</span></p>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <p class="mono"><span class="fr-only">Jour et nuit</span><span class="en-only">Day and night</span></p>
  <h2><span class="fr-only">La nuit, la porte ne se ferme pas.</span><span class="en-only">At night, the door stays open.</span></h2>
  <p><span class="fr-only">L'accueil de la polyclinique est ouvert <b>24h/24, tous les jours</b>. Appelez ou écrivez : on vous répond, on vous oriente, et on vous dit s'il faut venir tout de suite ou attendre la consultation du spécialiste.</span>
    <span class="en-only">The polyclinic's reception is open <b>24/7, every day</b>. Call or message us: we answer, we guide you, and we tell you whether to come now or wait for the specialist's consultation.</span></p>
  <div class="actions">
    <a class="btn btn-on" href="tel:+237696710699">{WA_LABEL}</a>
    <a class="btn btn-line" href="https://wa.me/{WA}?text=Bonjour%2C%20c%27est%20urgent%20%E2%80%94%20que%20dois-je%20faire%20%3F">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
      <span class="fr-only">Écrire sur WhatsApp</span><span class="en-only">Message on WhatsApp</span></a>
  </div>
</div></section>

<section id="acces"><div class="wrap">
  <p class="mono"><span class="fr-only">Accès</span><span class="en-only">Getting here</span></p>
  <h2><span class="fr-only">Deido, Vallée Bessengue — face à l'hôtel LEWAT.</span><span class="en-only">Deido, Vallée Bessengue — opposite the LEWAT hotel.</span></h2>
  <div class="find-grid">
    <div>
      <div class="info rv">
        <div class="irow"><span class="k"><span class="fr-only">Adresse</span><span class="en-only">Address</span></span>
          <p><span class="fr-only">1 149 Boulevard de la République, Deido — Douala.</span><span class="en-only">1,149 Boulevard de la République, Deido — Douala.</span></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Repère</span><span class="en-only">Landmark</span></span>
          <p><span class="fr-only">Vallée Bessengue, <b>face à l'hôtel LEWAT</b>. En taxi ou moto-taxi, demandez « JEMPO, Bessengue » : c'est connu dans le quartier.</span>
            <span class="en-only">Vallée Bessengue, <b>opposite the LEWAT hotel</b>. By taxi or moto-taxi, ask for “JEMPO, Bessengue” — people know it in the neighbourhood.</span></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Téléphones</span><span class="en-only">Phones</span></span>
          <p><a href="tel:+237696710699">{WA_LABEL}</a> <span class="fr-only">(WhatsApp)</span><span class="en-only">(WhatsApp)</span> · <a href="tel:+237670858542">+237 {PHONE_2}</a> · <a href="tel:+237233478769">+237 {PHONE_FIXE}</a></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Accueil</span><span class="en-only">Reception</span></span>
          <p><span class="fr-only">Ouvert 24h/24, 7j/7. Consultations spécialisées : voir les jours par praticien ci-dessus.</span><span class="en-only">Open 24/7. Specialist consultations: see each practitioner's days above.</span></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Paiement</span><span class="en-only">Payment</span></span>
          <p><span class="fr-only">Espèces · MTN Mobile Money · Orange Money. Assurance : envoyez le nom de votre assureur avant la visite.</span><span class="en-only">Cash · MTN Mobile Money · Orange Money. Insurance: send your insurer's name before the visit.</span></p></div>
      </div>
    </div>
    <div class="mapcard rv">
      <svg viewBox="0 0 420 300" role="img" aria-label="Plan schématique : JEMPO, 1 149 Boulevard de la République, Deido, face à l'hôtel LEWAT">
        <rect x="0" y="0" width="420" height="300" rx="14" fill="#F7F1E9"/>
        <path d="M0 168h420" stroke="#E7D9C8" stroke-width="48"/>
        <path d="M0 168h420" stroke="#fff" stroke-width="4" stroke-dasharray="16 14"/>
        <path d="M300 168v-120" stroke="#E7D9C8" stroke-width="24"/>
        <path d="M300 168v-120" stroke="#fff" stroke-width="3" stroke-dasharray="10 10"/>
        <circle cx="300" cy="168" r="30" fill="#C2542B" opacity=".14"/>
        <circle cx="300" cy="168" r="9" fill="#C2542B"/>
        <circle cx="300" cy="168" r="3.4" fill="#fff"/>
        <rect x="58" y="118" width="176" height="40" rx="10" fill="#fff" stroke="#E7D9C8"/>
        <text x="72" y="135" font-family="Archivo,Arial" font-size="12.5" font-weight="700" fill="#2A211C">HÔTEL LEWAT</text>
        <text x="72" y="150" font-family="Inter,Arial" font-size="10.5" fill="#4A3A31">face à la clinique</text>
        <rect x="226" y="196" width="168" height="40" rx="10" fill="#2A211C"/>
        <text x="240" y="213" font-family="Archivo,Arial" font-size="12.5" font-weight="700" fill="#fff">JEMPO</text>
        <text x="240" y="228" font-family="Inter,Arial" font-size="10.5" fill="#E8A87C">1 149, Bd de la République</text>
        <text x="14" y="208" font-family="Archivo,Arial" font-size="12" font-weight="700" fill="#2A211C">BOULEVARD DE LA RÉPUBLIQUE</text>
        <text x="308" y="66" font-family="Archivo,Arial" font-size="11" font-weight="700" fill="#2A211C">DEIDO</text>
        <text x="14" y="24" font-family="Inter,Arial" font-size="11" fill="#4A3A31">Douala · Deido / Bessengue</text>
      </svg>
      <p class="cap"><span class="fr-only">Plan schématique, pas à l'échelle : il sert à reconnaître l'endroit, pas à remplacer votre GPS.</span>
        <span class="en-only">Schematic map, not to scale: it helps you recognise the place, it does not replace your GPS.</span></p>
    </div>
  </div>
</div></section>

<section id="faq" class="hair"><div class="wrap">
  <p class="mono"><span class="fr-only">Questions fréquentes</span><span class="en-only">Frequently asked</span></p>
  <h2 style="margin-bottom:14px"><span class="fr-only">Ce qu'on nous demande avant de venir.</span><span class="en-only">What people ask before coming in.</span></h2>
{FAQ_HTML}
  <div class="contact" id="contact">
    <span class="mono"><span class="fr-only">Prendre contact</span><span class="en-only">Get in touch</span></span>
    <h3 style="margin-top:6px"><span class="fr-only">Un message suffit pour commencer.</span><span class="en-only">One message is enough to start.</span></h3>
    <div class="crow"><span class="k">WhatsApp</span><span><a href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20polyclinique.">{WA_LABEL}</a></span></div>
    <div class="crow"><span class="k"><span class="fr-only">Appels</span><span class="en-only">Calls</span></span><span>{PHONE_2} · {PHONE_FIXE}</span></div>
    <div class="crow"><span class="k"><span class="fr-only">Adresse</span><span class="en-only">Address</span></span><span><span class="fr-only">1 149 Boulevard de la République — Deido, Douala</span><span class="en-only">1,149 Boulevard de la République — Deido, Douala</span></span></div>
  </div>
</div></section>

</main>

<footer class="footer">
  <div class="wrap">
    <div class="f-grid">
      <div class="f-brand">
        <b>J&amp;E MEMORIAL POLYCLINIC</b>
        <p class="line"><span class="fr-only">Polyclinique à Deido, Douala : consultations de spécialistes sur rendez-vous, accueil jour et nuit.</span>
          <span class="en-only">Polyclinic in Deido, Douala: specialist consultations by appointment, reception day and night.</span></p>
      </div>
      <div class="f-col">
        <div class="f-ttl"><span class="fr-only">Sur cette page</span><span class="en-only">On this page</span></div>
        <a href="#reception"><span class="fr-only">Consultations</span><span class="en-only">Consultations</span></a>
        <a href="#acces"><span class="fr-only">Accès</span><span class="en-only">Getting here</span></a>
        <a href="#faq"><span class="fr-only">Questions fréquentes</span><span class="en-only">Frequently asked</span></a>
        <a href="#contact"><span class="fr-only">Contact</span><span class="en-only">Contact</span></a>
      </div>
      <div class="f-cta">
        <p><span class="fr-only">Prenez votre rendez-vous : dites-nous la spécialité, on vous répond sur WhatsApp.</span>
          <span class="en-only">Book your appointment: tell us the specialty and we reply on WhatsApp.</span></p>
        <a href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20polyclinique.">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
          <span class="fr-only">Rendez-vous WhatsApp</span><span class="en-only">WhatsApp appointment</span>
        </a>
      </div>
      <div class="f-contact">
        <div class="f-ttl"><span class="fr-only">Nous joindre</span><span class="en-only">Reach us</span></div>
        <div><a href="tel:+237696710699" style="color:#EFE5D9">{WA_LABEL}</a></div>
        <div>{PHONE_2} · {PHONE_FIXE}</div>
        <div><span class="fr-only">1 149 Bd de la République, Deido — face hôtel LEWAT</span><span class="en-only">1,149 Bd de la République, Deido — opposite LEWAT hotel</span></div>
        <div><span class="fr-only">Accueil 24h/24 · 7j/7</span><span class="en-only">Reception 24/7</span></div>
      </div>
    </div>
    <div class="f-strip">
      <span>© 2026 J&amp;E Memorial Polyclinic (JEMPO) — <span class="fr-only">aperçu préparé par AMK, pas encore en ligne</span><span class="en-only">preview prepared by AMK, not online yet</span></span>
      <a href="#top"><span class="fr-only">Retour en haut ↑</span><span class="en-only">Back to top ↑</span></a>
    </div>
  </div>
</footer>

<div class="sticky-wa">
  <a class="w" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20polyclinique.">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
    <span class="fr-only">WhatsApp</span><span class="en-only">WhatsApp</span>
  </a>
  <a class="c" href="tel:+237696710699"><span class="fr-only">Appeler</span><span class="en-only">Call</span></a>
</div>

<script>
__JS__
</script>
</body>
</html>
"""

JS = """
(function(){
  var html=document.documentElement, k='jempo-lang';
  function setLang(l){
    html.setAttribute('data-lang',l); html.lang=l;
    document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
    document.getElementById('btn-en').classList.toggle('is-on',l==='en');
    try{localStorage.setItem(k,l)}catch(e){}
    updateRec();
  }
  document.getElementById('btn-fr').addEventListener('click',function(){setLang('fr')});
  document.getElementById('btn-en').addEventListener('click',function(){setLang('en')});
  try{ var saved=localStorage.getItem(k); if(saved) setLang(saved); }catch(e){}

  // ---- la réception : specialty -> practitioner -> WhatsApp
  var WA='__WA__';
  var DOCS=[__DOCS__];
  var tabs=[].slice.call(document.querySelectorAll('.door.tab'));
  function put(id, fr, en){
    document.getElementById(id).innerHTML='<span class="'+(html.getAttribute('data-lang')==='fr'?'fr-only':'en-only')+'">'+((html.getAttribute('data-lang')==='fr')?fr:en)+'</span>';
  }
  function updateRec(){
    var cur=document.querySelector('.door.tab.is-on'); if(!cur) return;
    var d=DOCS.filter(function(x){return x.k===cur.dataset.k})[0]; if(!d) return;
    var l=html.getAttribute('data-lang')||'fr';
    put('recTitle', d.fr, d.en);
    document.getElementById('recWho').innerHTML=d.doc+' — <span class="'+(l==='fr'?'fr-only':'en-only')+'">'+(l==='fr'?d.who_fr:d.who_en)+'</span>';
    put('recHours', d.h_fr, d.h_en);
    put('recWhy', d.c_fr, d.c_en);
    var msg='Bonjour, je souhaite un rendez-vous avec '+d.ask_fr+'.';
    if(l==='en') msg='Hello, I would like an appointment with '+d.ask_en+'.';
    document.getElementById('recWa').href='https://wa.me/'+WA+'?text='+encodeURIComponent(msg);
  }
  tabs.forEach(function(t){t.addEventListener('click',function(){
    tabs.forEach(function(x){x.classList.remove('is-on'); x.setAttribute('aria-selected','false')});
    t.classList.add('is-on'); t.setAttribute('aria-selected','true'); updateRec();
  })});
  updateRec();

  // gentle reveal (skipped when the visitor prefers reduced motion)
  if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
    },{rootMargin:'0px 0px -8% 0px'});
    [].forEach.call(document.querySelectorAll('.rv'),function(el){io.observe(el)});
  } else {
    [].forEach.call(document.querySelectorAll('.rv'),function(el){el.classList.add('in')});
  }
})();
"""

# who_fr / who_en per specialty (chronic titles)
WHO_FR = ["oto-rhino-laryngologiste", "dermatologue", "diabétologue", "gynécologue"]
WHO_EN = ["ear, nose and throat specialist", "dermatologist", "diabetologist", "gynaecologist"]

docs_js = ",\n".join(
    '{k:"%s",fr:"%s",en:"%s",doc:"%s",who_fr:"%s",who_en:"%s",h_fr:"%s",h_en:"%s",c_fr:"%s",c_en:"%s",ask_fr:"%s",ask_en:"%s"}'
    % (k, fr, en, doc_fr, WHO_FR[i], WHO_EN[i], h_fr, h_en,
       c_fr.replace('"', "'"), c_en.replace('"', "'"),
       ask_fr.replace('"', "'"), ask_en.replace('"', "'"))
    for i, (k, fr, en, doc_fr, doc_en, h_fr, h_en, c_fr, c_en, ask_fr, ask_en) in enumerate(DOCS))
JS = JS.replace("__DOCS__", docs_js).replace("__WA__", WA)

HTML = HTML.replace("__JS__", JS)
OUT.write_text(HTML, encoding='utf-8')
print(f"OK {OUT} — {OUT.stat().st_size/1024:.0f} KB")
