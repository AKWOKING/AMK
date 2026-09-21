#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AMK — CLINIQUE LA BÉTHANIE (Bonabéri, Douala) — named concept builder
Direction « LA CONSULTATION » : la page vit comme leur dépliant gynécologie —
bleu royal + vert feuille (leurs couleurs), Montserrat + Open Sans (leur
typographie d'affiche), la vraie photo de l'entrée, et la liste des six
prestations du dépliant devient une liste à cocher qui part sur WhatsApp.

Output: demos/concept-labethanie-v1.html   (single file, base64 images, FR|EN)
Usage:  python3 demos/build_labethanie.py [--wa 2376XXXXXXXX] [--out name.html]
"""
import base64, io, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path('/home/user/AMK')
WA = "237677760782"           # verified WhatsApp line (King, 17 Sep 2026)
OUT_NAME = "concept-labethanie-v1.html"
WA_LABEL = '+237 677 76 07 82'
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

IMG_HERO = b64('clients/la-bethanie/entrance Clinique La Béthanie (Bonabéri).jpg', 900, 72)
IMG_SIGN = b64('clients/la-bethanie/entrance Clinique La Béthanie (Bonabéri).jpg', 720, 76)

PHONE_1 = "683 76 74 13"
PHONE_2 = "699 73 15 48"

# ---- the flyer's six prestations, verbatim (FR) + EN
PRESTATIONS = [
    ("Consultations gynécologiques", "Gynaecology consultations",
     "Suivi annuel, dépistage, conseils.", "Annual check-up, screening, advice."),
    ("Suivi de grossesse", "Pregnancy follow-up",
     "Échographies, surveillance, préparation à l'accouchement.",
     "Ultrasounds, monitoring, birth preparation."),
    ("Prise en charge des troubles gynécologiques", "Care for gynaecological problems",
     "Infections, douleurs, cycles irréguliers…", "Infections, pain, irregular cycles…"),
    ("Dépistage du cancer du col de l'utérus", "Cervical cancer screening",
     "Frottis, test HPV.", "Smear test, HPV test."),
    ("Conseils et planification familiale", "Advice and family planning",
     "Contraception, suivi.", "Contraception, follow-up."),
    ("Suivi de la ménopause", "Menopause follow-up",
     "Accompagnement et conseils.", "Support and advice."),
]

CHIR = [
    ("Consultation chirurgicale", "Surgical consultation",
     "Examen, explication de l'intervention, questions avant de décider.",
     "Examination, explanation of the operation, questions before you decide."),
    ("Interventions programmées", "Scheduled surgery",
     "Les opérations sont planifiées avec vous et expliquées à l'avance.",
     "Operations are planned with you and explained beforehand."),
    ("Suivi après l'opération", "Follow-up after surgery",
     "Contrôles et consignes de récupération après l'intervention.",
     "Check-ups and recovery instructions after the operation."),
]

FAQ = [
    ("Quels sont vos horaires ?", "What are your opening hours?",
     "La clinique est ouverte 24h/24 et 7j/7, toute l'année.",
     "The clinic is open 24 hours a day, 7 days a week, all year round."),
    ("Faut-il prendre rendez-vous ?", "Do I need an appointment?",
     "Pour une consultation, écrivez-nous ou appelez : nous vous donnons un créneau pour vous éviter l'attente. Les urgences sont reçues à toute heure.",
     "For a consultation, message or call us: we give you a slot so you do not wait. Emergencies are seen at any hour."),
    ("Où se trouve exactement la clinique ?", "Where exactly is the clinic?",
     "À Bonabéri, Rue Mpondo, sur l'Ancienne Route — un bâtiment jaune derrière une grille verte, sous l'enseigne « La Béthanie ».",
     "In Bonabéri, Rue Mpondo, on the Ancienne Route — a yellow building behind a green fence, under the “La Béthanie” sign."),
    ("Et si je ne sais pas quel service consulter ?", "What if I don't know which service to see?",
     "Écrivez en quelques mots ce qui vous gêne, sur WhatsApp. On vous oriente vers la bonne consultation, sans long questionnaire.",
     "Write a few words about what is bothering you, on WhatsApp. We point you to the right consultation, with no long questionnaire."),
    ("Le site est-il en anglais ?", "Is the website available in English?",
     "Oui : la page se lit en français et en anglais. Pour l'accueil, indiquez votre langue au moment de prendre contact.",
     "Yes: this page reads in French and English. For the reception, mention your language when you get in touch."),
]

PREST_HTML = "\n".join(f'''    <label class="p-row">
      <input type="checkbox" class="p-check" data-fr="{t_fr}" data-en="{t_en}">
      <span><b><span class="fr-only">{t_fr}</span><span class="en-only">{t_en}</span></b>
      <span class="sub"><span class="fr-only">{s_fr}</span><span class="en-only">{s_en}</span></span></span>
    </label>''' for t_fr, t_en, s_fr, s_en in PRESTATIONS)

CHIR_HTML = "\n".join(f'''    <div class="card"><span class="mono">{n:02d}</span>
      <h3><span class="fr-only">{t_fr}</span><span class="en-only">{t_en}</span></h3>
      <p><span class="fr-only">{s_fr}</span><span class="en-only">{s_en}</span></p></div>''' for n, (t_fr, t_en, s_fr, s_en) in enumerate(CHIR, 1))

FAQ_HTML = "\n".join(f'''  <details class="faq">
    <summary><span class="fr-only">{q_fr}</span><span class="en-only">{q_en}</span></summary>
    <p><span class="fr-only">{a_fr}</span><span class="en-only">{a_en}</span></p>
  </details>''' for q_fr, q_en, a_fr, a_en in FAQ)

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "MedicalClinic",
    "name": "Clinique La Béthanie — Centre Médico-Chirurgical · Maternité",
    "description": "Centre médico-chirurgical et maternité à Bonabéri, Douala : gynécologie, suivi de grossesse, chirurgie. Ouvert 24h/24, 7j/7. Concept de démonstration préparé par AMK.",
    "telephone": "+237677760782",
    "address": {"@type": "PostalAddress", "streetAddress": "Rue Mpondo, Ancienne Route",
                "addressLocality": "Bonabéri, Douala", "addressCountry": "CM"},
    "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                  "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                  "opens": "00:00", "closes": "23:59"},
    "medicalSpecialty": ["Obstetric", "Gynecologic", "Surgical"],
    "availableLanguage": ["French", "English"],
}, ensure_ascii=False, indent=2)

CSS = """
:root{
 --blue:#0F4C9C; --blue-d:#0A2C5E; --blue-l:#2E7BD6; --cyan:#1FA9D8;
 --green:#3F8B1E; --green-d:#2E6B14; --mint:#EFF7E9;
 --ink:#10233F; --mute:#516781; --line:rgba(16,35,63,.13);
 --tint:#EEF4FC; --paper:#fff; --wa:#0B7A3E; --r:16px; --max:1120px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);
 font:16px/1.62 "Open Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
 -webkit-font-smoothing:antialiased}
h1,h2,h3,.display{font-family:Montserrat,-apple-system,"Segoe UI",Arial,sans-serif;font-weight:700;line-height:1.14;margin:0;letter-spacing:-.012em;color:var(--ink)}
h1{font-size:clamp(1.95rem,7vw,3.15rem);font-weight:800;line-height:1.08}
h2{font-size:clamp(1.4rem,4.6vw,2.05rem)}
h3{font-size:1.02rem;font-weight:700}
p{margin:.55rem 0 0}
a{color:var(--blue-d)}
ul{margin:.5rem 0 0;padding-left:1.1rem}
li{margin:.25rem 0}
.mono{font-family:Montserrat,sans-serif;font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;font-weight:700;color:var(--blue-d)}
.wrap{max-width:var(--max);margin:0 auto;padding:0 18px}
section{padding:52px 0}
.hair{border-top:1px solid var(--line)}
.sub{display:block;color:var(--mute);font-size:.88rem;font-weight:400;margin-top:2px;line-height:1.5}
html[data-lang="fr"] .en-only{display:none !important}
html[data-lang="en"] .fr-only{display:none !important}
html[data-lang="en"] .en-only{display:revert !important}
html[data-lang="fr"] .fr-only{display:revert !important}
:is(a,button,label,summary):focus-visible{outline:3px solid var(--cyan);outline-offset:2px;border-radius:10px}

/* top bar + nav */
.top{background:var(--blue-d);color:#DCE9FB;font-size:.8rem}
.top .wrap{display:flex;gap:12px;justify-content:space-between;align-items:center;padding:9px 18px;flex-wrap:wrap}
.top a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.4)}
.nav{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.96);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:12px;padding:10px 18px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}
.brand b{font-family:Montserrat,sans-serif;font-weight:800;font-size:1.02rem;display:block;line-height:1.06;letter-spacing:.02em;color:var(--blue-d)}
.brand .bsub{display:block;font-size:.62rem;color:var(--mute);letter-spacing:.09em;text-transform:uppercase;font-weight:600}
.nav nav{margin-left:auto;display:none;gap:17px;font-size:.9rem}
.nav nav a{text-decoration:none;color:var(--ink);opacity:.88}
.lang{display:flex;margin-left:auto;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:#fff}
.lang button{border:0;background:transparent;padding:7px 12px;font:700 .78rem Montserrat,sans-serif;color:var(--mute);cursor:pointer}
.lang button.is-on{background:var(--blue-d);color:#fff}
.cta{background:var(--wa);color:#fff;text-decoration:none;padding:11px 15px;border-radius:999px;font-weight:700;font-size:.86rem;white-space:nowrap}
.cta.small{display:none}

/* hero */
.hero{padding-top:30px}
.hero-grid{display:grid;gap:26px;align-items:center}
.hero h1 em{font-style:normal;color:var(--blue)}
.lede{font-size:1.04rem;color:#2C4262;max-width:56ch}
.hero-media{position:relative;border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}
.hero-media img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.tag{position:absolute;left:12px;bottom:12px;background:rgba(10,44,94,.93);color:#fff;padding:7px 11px;border-radius:10px;font-size:.7rem}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 18px;border-radius:12px;text-decoration:none;font-weight:700;border:1px solid transparent;cursor:pointer;font-family:inherit;font-size:.95rem}
.btn-primary{background:var(--wa);color:#fff}
.btn-blue{background:var(--blue);color:#fff}
.btn-ghost{background:#fff;color:var(--blue-d);border-color:var(--line)}
.btn svg{width:18px;height:18px;fill:currentColor}
.facts{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}
.fact{background:var(--tint);border:1px solid var(--line);border-radius:999px;padding:8px 13px;font-size:.8rem;color:#2C4262}
.fact b{color:var(--blue-d)}

/* urgences band */
.urg{background:var(--blue-d);color:#E8F1FB}
.urg h2{color:#fff}
.urg .mono{color:#A8E08C}
.urg p{color:#D6E5FA;max-width:62ch}
.urg .actions{margin-top:20px}
.urg .btn-on-dark{background:#fff;color:var(--blue-d)}
.urg-chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
.urg-chips span{background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:8px 13px;font-size:.8rem;color:#EAF3FE}

/* gynécologie */
.gyn-grid{display:grid;gap:22px;margin-top:24px}
@media(min-width:900px){.gyn-grid{grid-template-columns:1.15fr .85fr;gap:28px;align-items:start}}
.ordo{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:0 14px 34px rgba(15,76,156,.07)}
.ordo-head{background:var(--blue);color:#fff;padding:15px 18px}
.ordo-head .mono{color:#CFE2FA}
.ordo-head h3{color:#fff;font-size:1.1rem;margin-top:2px}
.ordo-body{padding:6px 18px 18px}
.p-row{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start;padding:14px 0;border-top:1px solid var(--line);cursor:pointer}
.p-row:first-child{border-top:0}
.p-row input{width:22px;height:22px;margin-top:2px;accent-color:var(--green-d);cursor:pointer}
.p-row b{font-weight:700;color:var(--ink)}
.ordo-send{border-top:1px solid var(--line);padding:16px 18px 18px;background:var(--mint)}
.ordo-send .note{color:#3D5A33;font-size:.82rem;margin-top:10px}
.side{display:grid;gap:16px}
.panel{background:var(--tint);border:1px solid var(--line);border-radius:var(--r);padding:18px}
.panel.blue{background:var(--blue);color:#EAF2FE}
.panel.blue h3{color:#fff}
.panel.blue .mono{color:#CFE2FA}
.panel.blue .step b{color:#fff}
.steps{margin:12px 0 0;padding:0;list-style:none;counter-reset:s}
.step{display:grid;grid-template-columns:auto 1fr;gap:11px;padding:10px 0;border-top:1px solid var(--line)}
.step:first-child{border-top:0}
.step .n{width:26px;height:26px;border-radius:999px;background:var(--blue);color:#fff;font:700 .78rem Montserrat,sans-serif;display:flex;align-items:center;justify-content:center}
.panel.blue .step{border-top-color:rgba(255,255,255,.22)}
.panel.blue .step .n{background:#fff;color:var(--blue-d)}
.step p{margin:2px 0 0;font-size:.92rem}

/* chirurgie */
.svc{display:grid;gap:14px;margin-top:22px}
@media(min-width:760px){.svc{grid-template-columns:repeat(3,1fr)}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px;color:var(--ink)}
.card .mono{color:var(--mute)}
.card h3{margin-top:8px}
.card p{color:#2C4262}
.dir{display:flex;gap:12px;align-items:center;background:var(--tint);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;margin-top:18px}
.dir .dot{width:40px;height:40px;border-radius:999px;background:var(--blue-d);color:#fff;font:800 .95rem Montserrat,sans-serif;display:flex;align-items:center;justify-content:center;flex:0 0 auto}
.dir p{margin:0;font-size:.92rem;color:#2C4262}

/* trouver */
.find-grid{display:grid;gap:22px;margin-top:24px}
@media(min-width:900px){.find-grid{grid-template-columns:1.05fr .95fr;gap:28px;align-items:start}}
.info{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:6px 18px}
.irow{display:flex;gap:12px;padding:14px 0;border-top:1px solid var(--line)}
.irow:first-child{border-top:0}
.irow .k{min-width:104px;font-family:Montserrat,sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--blue-d);padding-top:3px}
.irow p{margin:0;color:#2C4262}
.mapcard{background:var(--tint);border:1px solid var(--line);border-radius:var(--r);padding:16px}
.mapcard svg{display:block;width:100%;height:auto}
.mapcard .cap{font-size:.78rem;color:var(--mute);margin-top:10px}
.shot{border-radius:var(--r);overflow:hidden;border:1px solid var(--line);margin-top:16px}
.shot img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;object-position:78% 46%}

/* faq + contact + footer */
.faq{background:#fff;border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:2px 16px}
.faq summary{cursor:pointer;padding:14px 0;font-weight:700;color:var(--ink);list-style:none;font-family:Montserrat,sans-serif;font-size:.95rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--blue);font-weight:800}
.faq[open] summary::after{content:"–"}
.faq p{margin:0 0 14px;color:#2C4262}
.contact{background:var(--blue-d);color:#E8F1FB;border-radius:var(--r);padding:20px;margin-top:22px}
.contact .mono{color:#A8E08C}
.contact h3{color:#fff}
.crow{display:flex;gap:12px;padding:12px 0;border-top:1px solid rgba(255,255,255,.18);font-size:.95rem;flex-wrap:wrap}
.crow:first-of-type{border-top:0}
.crow .k{min-width:104px;font-family:Montserrat,sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:#A8E08C;padding-top:3px}
.crow a{color:#fff}
footer{background:var(--blue-d);color:#C9DCF6;padding:26px 0 96px;font-size:.86rem}
footer a{color:#fff}
footer .who{font-family:Montserrat,sans-serif;font-weight:800;color:#fff;letter-spacing:.02em}
.sticky-wa{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;display:flex;gap:10px}
.sticky-wa a{flex:1;justify-content:center;padding:15px 18px;border-radius:14px;text-decoration:none;font-weight:700;display:flex;align-items:center;gap:9px;font-size:.95rem}
.sticky-wa .w{background:var(--wa);color:#fff;box-shadow:0 8px 22px rgba(11,122,62,.35)}
.sticky-wa .c{background:#fff;color:var(--blue-d);border:1px solid var(--line)}
.sticky-wa svg{width:18px;height:18px;fill:currentColor}
@media(min-width:900px){.sticky-wa{display:none}footer{padding-bottom:28px}.nav nav{display:flex}.cta.small{display:inline-flex}.hero-grid{grid-template-columns:1.02fr .98fr;gap:30px}.lang{margin-left:0}}
.rv{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.rv{opacity:1;transform:none;transition:none}*{animation:none!important}}
"""

HTML = f"""<!doctype html>
<html lang="fr" data-lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clinique La Béthanie — Centre Médico-Chirurgical · Maternité, Bonabéri (Douala)</title>
<meta name="description" content="Clinique La Béthanie à Bonabéri, Douala : gynécologie, suivi de grossesse, maternité et chirurgie. Ouvert 24h/24, 7j/7 — Rue Mpondo, Ancienne Route. Rendez-vous sur WhatsApp.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0A2C5E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{JSONLD}</script>
</head>
<body>

<div class="top"><div class="wrap">
  <span><span class="fr-only">Ouvert 24h/24 · 7j/7 — Bonabéri, Rue Mpondo (Ancienne Route)</span><span class="en-only">Open 24/7 — Bonabéri, Rue Mpondo (Ancienne Route)</span></span>
  <a href="tel:+237677760782">{WA_LABEL}</a>
</div></div>

<header class="nav"><div class="wrap">
  <a class="brand" href="#top" aria-label="Clinique La Béthanie">
    <svg width="40" height="40" viewBox="0 0 40 40" role="img" aria-hidden="true">
      <rect width="40" height="40" rx="12" fill="#0F4C9C"/>
      <path d="M17 7h6v10h10v6H23v10h-6V23H7V17h10Z" fill="#fff"/>
      <path d="M29 11c3.4.6 5.6 2.9 6 6.4-3.6.2-5.8-2-6.6-5.2Z" fill="#1FA9D8"/>
      <path d="M31 30c-2.6-1.4-3.8-3.6-3.4-6.4 2.8.2 4.6 2 5 4.8Z" fill="#3F8B1E"/>
    </svg>
    <span><b>LA BÉTHANIE</b>
    <span class="bsub"><span class="fr-only">Centre médico-chirurgical · Maternité</span><span class="en-only">Medical &amp; surgical centre · Maternity</span></span></span>
  </a>
  <nav>
    <a href="#gyneco"><span class="fr-only">Gynécologie</span><span class="en-only">Gynaecology</span></a>
    <a href="#urgences"><span class="fr-only">Urgences</span><span class="en-only">Emergency</span></a>
    <a href="#chirurgie"><span class="fr-only">Chirurgie</span><span class="en-only">Surgery</span></a>
    <a href="#trouver"><span class="fr-only">Nous trouver</span><span class="en-only">Find us</span></a>
  </nav>
  <div class="lang" role="group" aria-label="Langue / Language">
    <button id="btn-fr" class="is-on" type="button">FR</button>
    <button id="btn-en" type="button">EN</button>
  </div>
  <a class="cta small" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20clinique.">
    <span class="fr-only">Rendez-vous</span><span class="en-only">Book now</span>
  </a>
</div></header>

<main id="top">

<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="mono" style="color:var(--blue)"><span class="fr-only">Bonabéri · Rue Mpondo (Ancienne Route) · Douala</span><span class="en-only">Bonabéri · Rue Mpondo (Ancienne Route) · Douala</span></p>
    <h1><span class="fr-only">Votre santé intime, <em>notre priorité.</em></span><span class="en-only">Your intimate health, <em>our priority.</em></span></h1>
    <p class="lede"><span class="fr-only">Gynécologie, suivi de grossesse, maternité et chirurgie — à la Clinique La Béthanie, à Bonabéri. Un accueil discret, des examens expliqués, et un rendez-vous que vous pouvez demander sur WhatsApp, en quelques mots.</span>
      <span class="en-only">Gynaecology, pregnancy follow-up, maternity and surgery — at Clinique La Béthanie in Bonabéri. A discreet reception, examinations explained, and an appointment you can request on WhatsApp in a few words.</span></p>
    <div class="actions">
      <a class="btn btn-primary" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20clinique.">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
        <span class="fr-only">Prendre rendez-vous</span><span class="en-only">Book an appointment</span>
      </a>
      <a class="btn btn-ghost" href="#trouver"><span class="fr-only">Nous trouver</span><span class="en-only">Find us</span></a>
    </div>
    <div class="facts">
      <span class="fact"><b>24h/24 · 7j/7</b> <span class="fr-only">ouvert</span><span class="en-only">open</span></span>
      <span class="fact"><span class="fr-only">Gynécologie &amp; maternité</span><span class="en-only">Gynaecology &amp; maternity</span></span>
      <span class="fact"><span class="fr-only">Rue Mpondo, Bonabéri</span><span class="en-only">Rue Mpondo, Bonabéri</span></span>
      <span class="fact"><b>FR</b> / <b>EN</b></span>
    </div>
  </div>
  <div class="hero-media rv">
    <img src="{IMG_HERO}" alt="Entrée de la Clinique La Béthanie à Bonabéri : bâtiment jaune, grille verte et enseigne blanche sur l'Ancienne Route">
    <span class="tag mono"><span class="fr-only">Notre entrée — Rue Mpondo, Bonabéri</span><span class="en-only">Our entrance — Rue Mpondo, Bonabéri</span></span>
  </div>
</div></section>

<section class="urg" id="urgences"><div class="wrap">
  <p class="mono"><span class="fr-only">Urgences &amp; accueil de nuit</span><span class="en-only">Emergency &amp; night reception</span></p>
  <h2><span class="fr-only">Une urgence n'attend pas l'ouverture.</span><span class="en-only">An emergency does not wait for opening hours.</span></h2>
  <p><span class="fr-only">La clinique est ouverte <b>24h/24 et 7j/7</b>. Appelez ou écrivez : on vous répond, on vous oriente, et on vous dit où venir — de jour comme de nuit, week-ends et jours fériés compris.</span>
    <span class="en-only">The clinic is open <b>24 hours a day, 7 days a week</b>. Call or message us: we answer, we point you the right way, and we tell you where to come — day or night, weekends and public holidays included.</span></p>
  <div class="actions">
    <a class="btn btn-on-dark" href="tel:+237677760782">
      <span class="fr-only">Appeler la clinique</span><span class="en-only">Call the clinic</span></a>
    <a class="btn btn-primary" href="https://wa.me/{WA}?text=Bonjour%2C%20j%27ai%20une%20urgence%20et%20je%20souhaite%20savoir%20o%C3%B9%20venir.">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
      <span class="fr-only">Écrire sur WhatsApp</span><span class="en-only">Message on WhatsApp</span></a>
  </div>
  <div class="urg-chips">
    <span><span class="fr-only">Ouvert jour et nuit</span><span class="en-only">Open day and night</span></span>
    <span><span class="fr-only">Bonabéri, Rue Mpondo</span><span class="en-only">Bonabéri, Rue Mpondo</span></span>
    <span>{WA_LABEL} · {PHONE_1} · {PHONE_2}</span>
  </div>
</div></section>

<section id="gyneco"><div class="wrap">
  <p class="mono"><span class="fr-only">Service de gynécologie</span><span class="en-only">Gynaecology department</span></p>
  <h2><span class="fr-only">Un accompagnement à chaque étape de votre santé féminine.</span><span class="en-only">Support at every stage of your women's health.</span></h2>
  <p class="lede"><span class="fr-only">Un accompagnement bienveillant et professionnel — de la consultation annuelle au suivi de grossesse, jusqu'après la ménopause. Cochez ce qui vous concerne : votre demande part sur WhatsApp, sans avoir à tout expliquer à voix haute.</span>
    <span class="en-only">Kind, professional support — from the annual consultation and pregnancy follow-up through to after the menopause. Tick what concerns you: your request goes to WhatsApp, without having to explain everything out loud.</span></p>

  <div class="gyn-grid">
    <div class="ordo rv">
      <div class="ordo-head">
        <span class="mono"><span class="fr-only">Dépliant du service</span><span class="en-only">Department leaflet</span></span>
        <h3><span class="fr-only">Nos prestations</span><span class="en-only">Our services</span></h3>
      </div>
      <div class="ordo-body">
{PREST_HTML}
      </div>
      <div class="ordo-send">
        <button class="btn btn-primary" id="sendList" type="button">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
          <span class="fr-only">Envoyer ma liste sur WhatsApp</span><span class="en-only">Send my list on WhatsApp</span>
        </button>
        <p class="note"><span class="fr-only">Votre liste n'est enregistrée nulle part sur ce site : elle part uniquement dans votre message WhatsApp, que vous pouvez relire avant l'envoi.</span>
          <span class="en-only">Your list is not stored anywhere on this site: it only goes into your WhatsApp message, which you can read again before sending.</span></p>
      </div>
    </div>

    <div class="side">
      <div class="panel blue rv">
        <span class="mono"><span class="fr-only">En confiance</span><span class="en-only">With confidence</span></span>
        <h3><span class="fr-only">Une première consultation, comment ça se passe ?</span><span class="en-only">A first consultation: how does it go?</span></h3>
        <ol class="steps">
          <li class="step"><span class="n">1</span><span><b><span class="fr-only">Vous dites ce qui vous amène</span><span class="en-only">You say what brings you in</span></b><p><span class="fr-only">En quelques mots, au téléphone ou sur WhatsApp.</span><span class="en-only">In a few words, by phone or on WhatsApp.</span></p></span></li>
          <li class="step"><span class="n">2</span><span><b><span class="fr-only">Le médecin vous examine et explique</span><span class="en-only">The doctor examines and explains</span></b><p><span class="fr-only">Ce qu'il observe, ce qu'il propose, et pourquoi.</span><span class="en-only">What they see, what they suggest, and why.</span></p></span></li>
          <li class="step"><span class="n">3</span><span><b><span class="fr-only">Vous décidez de la suite</span><span class="en-only">You decide what comes next</span></b><p><span class="fr-only">Examens, traitement ou suivi : rien ne se fait sans votre accord.</span><span class="en-only">Tests, treatment or follow-up: nothing happens without your agreement.</span></p></span></li>
        </ol>
        <div class="actions">
          <a class="btn btn-on-dark" style="background:#fff;color:#0A2C5E" href="https://wa.me/{WA}?text=Bonjour%2C%20j%27ai%20une%20question%20avant%20de%20prendre%20rendez-vous.">
            <span class="fr-only">Poser une question</span><span class="en-only">Ask a question</span></a>
        </div>
      </div>
      <div class="panel rv">
        <span class="mono"><span class="fr-only">Bon à savoir</span><span class="en-only">Good to know</span></span>
        <p style="margin-top:8px"><span class="fr-only">Le dépistage du col de l'utérus se fait même sans symptôme, et la planification familiale se discute sans jugement : ce sont deux consultations comme les autres.</span>
          <span class="en-only">Cervical screening is done even with no symptoms, and family planning is discussed without judgement: both are ordinary consultations.</span></p>
      </div>
    </div>
  </div>
</div></section>

<section id="chirurgie" class="hair"><div class="wrap">
  <p class="mono"><span class="fr-only">Centre médico-chirurgical</span><span class="en-only">Medical &amp; surgical centre</span></p>
  <h2><span class="fr-only">La clinique n'est pas seulement une maternité.</span><span class="en-only">The clinic is more than a maternity ward.</span></h2>
  <p class="lede"><span class="fr-only">La Béthanie est un centre médico-chirurgical : à côté de la gynécologie et de la maternité, elle reçoit les patients pour une consultation chirurgicale et les interventions programmées, avec un suivi après l'opération.</span>
    <span class="en-only">La Béthanie is a medical and surgical centre: alongside gynaecology and maternity, it receives patients for a surgical consultation and scheduled operations, with follow-up after surgery.</span></p>
  <div class="svc rv">
{CHIR_HTML}
  </div>
  <div class="dir">
    <span class="dot">RP</span>
    <p><span class="fr-only"><b>Direction : Dr Richard Petieu, chirurgien.</b> Les interventions sont réalisées sur place, au bloc de la clinique.</span>
      <span class="en-only"><b>Led by Dr Richard Petieu, surgeon.</b> Operations are performed on site, in the clinic's theatre.</span></p>
  </div>
</div></section>

<section id="trouver" class="hair"><div class="wrap">
  <p class="mono"><span class="fr-only">Nous trouver</span><span class="en-only">Find us</span></p>
  <h2><span class="fr-only">Bonabéri, Rue Mpondo — sur l'Ancienne Route.</span><span class="en-only">Bonabéri, Rue Mpondo — on the Ancienne Route.</span></h2>
  <div class="find-grid">
    <div>
      <div class="info rv">
        <div class="irow"><span class="k"><span class="fr-only">Adresse</span><span class="en-only">Address</span></span>
          <p><span class="fr-only">Bonabéri — Rue Mpondo (Ancienne Route), Douala.</span><span class="en-only">Bonabéri — Rue Mpondo (Ancienne Route), Douala.</span></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Repère</span><span class="en-only">Landmark</span></span>
          <p><span class="fr-only">Un bâtiment jaune derrière une grille verte, sous l'enseigne blanche « La Béthanie ». L'entrée se fait au portail, sur la rue.</span>
            <span class="en-only">A yellow building behind a green fence, under the white “La Béthanie” sign. The entrance is at the gate, on the street.</span></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Téléphone</span><span class="en-only">Phone</span></span>
          <p><a href="tel:+237677760782">{WA_LABEL}</a> <span class="fr-only">(WhatsApp)</span><span class="en-only">(WhatsApp)</span> · <a href="tel:+237683767413">+237 {PHONE_1}</a> · <a href="tel:+237699731548">+237 {PHONE_2}</a></p></div>
        <div class="irow"><span class="k"><span class="fr-only">Horaires</span><span class="en-only">Hours</span></span>
          <p><span class="fr-only">Ouvert 24h/24 et 7j/7 — accueil de jour comme de nuit.</span><span class="en-only">Open 24/7 — reception day and night.</span></p></div>
      </div>
      <div class="shot rv">
        <img src="{IMG_SIGN}" alt="Enseigne blanche « La Béthanie » à l'entrée, sur la grille verte du bâtiment jaune">
      </div>
    </div>
    <div class="mapcard rv">
      <svg viewBox="0 0 420 300" role="img" aria-label="Plan schématique : la clinique se trouve Rue Mpondo, sur l'Ancienne Route Bonabéri">
        <rect x="0" y="0" width="420" height="300" rx="14" fill="#E7EFFA"/>
        <path d="M0 196h420" stroke="#C6D5EA" stroke-width="46"/>
        <path d="M0 196h420" stroke="#fff" stroke-width="4" stroke-dasharray="16 14"/>
        <path d="M232 196v-96" stroke="#C6D5EA" stroke-width="26"/>
        <path d="M232 196v-96" stroke="#fff" stroke-width="3" stroke-dasharray="10 10"/>
        <circle cx="232" cy="196" r="30" fill="#0F4C9C" opacity=".12"/>
        <circle cx="232" cy="196" r="9" fill="#0F4C9C"/>
        <circle cx="232" cy="196" r="3.4" fill="#fff"/>
        <rect x="250" y="146" width="150" height="42" rx="10" fill="#fff" stroke="#C6D5EA"/>
        <text x="264" y="164" font-family="Montserrat,Arial" font-size="12.5" font-weight="700" fill="#0A2C5E">LA BÉTHANIE</text>
        <text x="264" y="179" font-family="Open Sans,Arial" font-size="10.5" fill="#516781">Rue Mpondo · grille verte</text>
        <text x="14" y="238" font-family="Montserrat,Arial" font-size="12" font-weight="700" fill="#0A2C5E">ANCIENNE ROUTE BONABÉRI</text>
        <text x="150" y="86" font-family="Montserrat,Arial" font-size="12" font-weight="700" fill="#0A2C5E">RUE MPONDO</text>
        <text x="14" y="24" font-family="Open Sans,Arial" font-size="11" fill="#516781">Douala · Bonabéri</text>
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
  <div class="contact">
    <span class="mono"><span class="fr-only">Prendre contact</span><span class="en-only">Get in touch</span></span>
    <h3 style="margin-top:6px"><span class="fr-only">Un message suffit pour commencer.</span><span class="en-only">One message is enough to start.</span></h3>
    <div class="crow"><span class="k">WhatsApp</span><span><a href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20clinique.">{WA_LABEL}</a></span></div>
    <div class="crow"><span class="k"><span class="fr-only">Appels</span><span class="en-only">Calls</span></span><span>{PHONE_1} · {PHONE_2}</span></div>
    <div class="crow"><span class="k"><span class="fr-only">Adresse</span><span class="en-only">Address</span></span><span><span class="fr-only">Rue Mpondo, Ancienne Route — Bonabéri, Douala</span><span class="en-only">Rue Mpondo, Ancienne Route — Bonabéri, Douala</span></span></div>
    <div class="crow"><span class="k"><span class="fr-only">Horaires</span><span class="en-only">Hours</span></span><span><span class="fr-only">24h/24 · 7j/7</span><span class="en-only">24/7</span></span></div>
  </div>
</div></section>

</main>

<footer><div class="wrap">
  <p><span class="who">CLINIQUE LA BÉTHANIE</span> — <span class="fr-only">Centre médico-chirurgical · Maternité, Bonabéri (Douala)</span><span class="en-only">Medical &amp; surgical centre · Maternity, Bonabéri (Douala)</span><br>
  <span class="fr-only">Aperçu préparé par AMK : cette page n'est pas encore en ligne. Vos photos, votre liste de services et vos corrections remplacent ce qui doit l'être avant la mise en ligne.</span>
  <span class="en-only">Preview prepared by AMK: this page is not online yet. Your photos, your service list and your corrections replace whatever needs to before launch.</span></p>
</div></footer>

<div class="sticky-wa">
  <a class="w" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20souhaite%20prendre%20rendez-vous%20%C3%A0%20la%20clinique.">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
    <span class="fr-only">WhatsApp</span><span class="en-only">WhatsApp</span>
  </a>
  <a class="c" href="tel:+237677760782"><span class="fr-only">Appeler</span><span class="en-only">Call</span></a>
</div>

<script>
__JS__
</script>
</body>
</html>
"""

JS = """
(function(){
  var html=document.documentElement, k='labethanie-lang';
  function setLang(l){
    html.setAttribute('data-lang',l); html.lang=l;
    document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
    document.getElementById('btn-en').classList.toggle('is-on',l==='en');
    try{localStorage.setItem(k,l)}catch(e){}
  }
  document.getElementById('btn-fr').addEventListener('click',function(){setLang('fr')});
  document.getElementById('btn-en').addEventListener('click',function(){setLang('en')});
  try{ var saved=localStorage.getItem(k); if(saved) setLang(saved); }catch(e){}

  // the leaflet checklist -> one discreet WhatsApp message
  var WA='__WA__';
  function checkedLabels(){
    var l=html.getAttribute('data-lang')||'fr';
    var out=[];
    [].forEach.call(document.querySelectorAll('.p-check'),function(c){
      if(c.checked) out.push(l==='fr'?c.getAttribute('data-fr'):c.getAttribute('data-en'));
    });
    return out;
  }
  document.getElementById('sendList').addEventListener('click',function(){
    var l=html.getAttribute('data-lang')||'fr';
    var items=checkedLabels();
    var msg;
    if(items.length){
      msg=(l==='fr'?'Bonjour, je souhaite un rendez-vous pour :\\n• ':'Hello, I would like an appointment for:\\n• ')
          + items.join('\\n• ')
          + (l==='fr'?'\\nMerci de me dire quand venir.':'\\nPlease let me know when to come.');
    } else {
      msg=(l==='fr'
        ? 'Bonjour, je souhaite prendre rendez-vous pour une consultation de gynécologie.'
        : 'Hello, I would like to book a gynaecology consultation.');
    }
    window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(msg),'_blank','noopener');
  });

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
""".replace("__WA__", WA)

HTML = HTML.replace("__JS__", JS)
OUT.write_text(HTML, encoding='utf-8')
print(f"OK {OUT} — {OUT.stat().st_size/1024:.0f} KB")
