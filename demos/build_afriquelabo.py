#!/usr/bin/env python3
"""
AMK — AFRIQUE LABO concept builder (named gift v1)
Direction: « FEUILLE DE RÉSULTAT » — lab-report anatomy: mono micro-labels,
numbered sections, hairline rules + a searchable test/price console.

Output: demos/concept-afriquelabo-v1.html  (single file, base64 images, FR|EN)
Sources of truth: clients/afrique-labo/build-notes.md + inspiration.md
"""
import base64, io, json
from pathlib import Path
from PIL import Image

ROOT = Path('/home/user/AMK')
OUT = ROOT / 'demos/concept-afriquelabo-v1.html'
WA = '237690547093'

# ---------------------------------------------------------------- images
def b64(path, width, quality=78):
    im = Image.open(ROOT / path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

IMG_HERO = b64('demos/img/labo-hero.jpg', 900, 76)
IMG_SAMPLES = b64('demos/img/labo-samples.jpg', 760, 74)
IMG_RECEPTION = b64('demos/img/labo-reception.jpg', 760, 74)

# ---------------------------------------------------------------- catalogue
# Extracts from THEIR OWN printed/WhatsApp grid (17 Sep 2026). Indicative.
TESTS = [
    # (fr, en, category, price)
    ("Glycémie à jeun", "Fasting blood glucose", "bio", 1200),
    ("Créatinine", "Creatinine", "bio", 3000),
    ("Acide urique", "Uric acid", "bio", 3000),
    ("Urée", "Urea", "bio", 3000),
    ("Triglycérides", "Triglycerides", "bio", 4000),
    ("Cholestérol total", "Total cholesterol", "bio", 4500),
    ("Albumine", "Albumin", "bio", 4500),
    ("Amylase", "Amylase", "bio", 4500),
    ("Bilirubine totale", "Total bilirubin", "bio", 4500),
    ("Calcium", "Calcium", "bio", 6000),
    ("Cholestérol HDL", "HDL cholesterol", "bio", 6000),
    ("Cholestérol LDL", "LDL cholesterol", "bio", 6000),
    ("Lipides totaux", "Total lipids", "bio", 6000),
    ("Hémoglobine glyquée (HbA1c)", "Glycated haemoglobin (HbA1c)", "bio", 12250),
    ("Protéines totales", "Total protein", "bio", 15000),

    ("Hémogramme complet (NFS)", "Complete blood count (CBC)", "hem", 6000),
    ("Groupe sanguin + rhésus", "Blood group + rhesus", "hem", 6000),

    ("CRP (inflammation)", "CRP (inflammation)", "ser", 6250),
    ("Widal (typhoïde)", "Widal (typhoid)", "ser", 7540),
    ("VIH 1 & 2", "HIV 1 & 2", "ser", 11700),
    ("Hépatite B (AgHBs)", "Hepatitis B (HBsAg)", "ser", 14850),
    ("Hépatite C", "Hepatitis C", "ser", 14850),
    ("Toxoplasmose IgG", "Toxoplasmosis IgG", "ser", 14850),
    ("Rubéole IgG", "Rubella IgG", "ser", 14850),
    ("Helicobacter pylori", "Helicobacter pylori", "ser", 28600),

    ("Bêta HCG (grossesse)", "Beta HCG (pregnancy)", "hor", 5200),
    ("FSH", "FSH", "hor", 23400),
    ("LH", "LH", "hor", 23400),
    ("Prolactine", "Prolactin", "hor", 23400),
    ("T3", "T3", "hor", 23400),
    ("T4", "T4", "hor", 23400),
    ("Progestérone", "Progesterone", "hor", 26000),
    ("Testostérone", "Testosterone", "hor", 26000),

    ("ECBU (culture d'urines)", "Urine culture (ECBU)", "bac", 11400),
]
CATS = [("all", "Tous", "All"), ("bio", "Biochimie", "Biochemistry"),
        ("hem", "Hématologie", "Haematology"), ("ser", "Sérologie & immunologie", "Serology & immunology"),
        ("hor", "Hormonologie", "Hormonology"), ("bac", "Bactériologie", "Bacteriology")]

def fmt(p):
    return f"{p:,}".replace(",", " ")

rows = []
for fr, en, cat, price in TESTS:
    rows.append(f'''<li class="t-row" data-cat="{cat}" data-fr="{fr.lower()}" data-en="{en.lower()}">
        <span class="t-name"><span class="fr-only">{fr}</span><span class="en-only">{en}</span></span>
        <span class="t-price">{fmt(price)} <small>FCFA</small></span>
        <button class="t-btn" data-test-fr="{fr}" data-test-en="{en}" data-price="{fmt(price)}" aria-label="Demander par WhatsApp">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
          <span class="fr-only">Demander</span><span class="en-only">Request</span>
        </button>
      </li>''')
CATALOGUE_ROWS = "\n".join(rows)

CAT_CHIPS = "\n".join(
    f'<button class="chip{" is-on" if key == "all" else ""}" data-cat="{key}">'
    f'<span class="fr-only">{fr}</span><span class="en-only">{en}</span></button>'
    for key, fr, en in CATS)

FAQ = [
    ("Faut-il être à jeun ?", "Do I need to fast?",
     "Pour la glycémie, le cholestérol et les triglycérides : 8 à 12 heures sans manger, l'eau est permise. Si votre ordonnance demande autre chose, suivez-la.",
     "For glucose, cholesterol and triglycerides: 8 to 12 hours without food, water is allowed. If your prescription says otherwise, follow it."),
    ("Quand venir pour les dosages hormonaux ?", "When should I come for hormone tests?",
     "Le matin, et demandez-nous la consigne exacte lors de la prise de rendez-vous (l'heure et le moment du cycle comptent pour plusieurs tests).",
     "In the morning, and ask us for the exact instruction when booking (time of day and cycle timing matter for several tests)."),
    ("Qu'est-ce que j'apporte ?", "What should I bring?",
     "L'ordonnance, votre carte de couverture (mutuelle/assurance) et, si vous êtes suivi, un ancien résultat. Pour les enfants, précisez l'âge à l'accueil.",
     "Your prescription, your cover card (insurance) and, if you are being followed up, a previous result. For children, mention the age at reception."),
    ("Comment réserver ou poser une question ?", "How do I book or ask a question?",
     "Par WhatsApp au 690 54 70 93 : envoyez le nom de l'analyse, nous vous donnons le tarif et le moment pour venir.",
     "On WhatsApp at 690 54 70 93: send the name of the test, we reply with the price and the best time to come."),
    ("Où se trouve exactement le laboratoire ?", "Where exactly is the laboratory?",
     "Feu rouge Bessengue — Immeuble Nkake, au-dessus de Wafacash, face Total, Douala.",
     "Bessengue roundabout — Immeuble Nkake, above Wafacash, opposite Total, Douala."),
]

FAQ_HTML = "\n".join(f'''<details class="faq">
  <summary><span class="fr-only">{q_fr}</span><span class="en-only">{q_en}</span></summary>
  <p><span class="fr-only">{a_fr}</span><span class="en-only">{a_en}</span></p>
</details>''' for q_fr, q_en, a_fr, a_en in FAQ)

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "DiagnosticLab",
    "name": "Afrique Labo SARL",
    "description": "Laboratoire multidisciplinaire d'analyses de biologie médicale à Bessengue, Douala. Tarifs affichés, demande par WhatsApp.",
    "telephone": "+237690547093", "email": "Afrique.labo@gmail.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Feu rouge Bessengue, Immeuble Nkake, au-dessus de Wafacash",
                "addressLocality": "Douala", "addressCountry": "CM"},
    "openingHours": "Mo-Su 00:00-24:00", "priceRange": "1000-30000 FCFA",
    "medicalSpecialty": "Pathology",
}, ensure_ascii=False, indent=2)

CSS = """
:root{
 --cyan:#12B4D6; --cyan-d:#0C8FAB; --cyan-soft:#E4F6FA; --navy:#0E2347; --navy-2:#153464;
 --red:#E11D2E; --paper:#F7FAFC; --ink:#0B1B33; --mute:#55688A; --line:rgba(14,35,71,.14);
 --wa:#0B7A3E; --r:14px; --max:1120px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);
 font:16px/1.6 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
 -webkit-font-smoothing:antialiased}
h1,h2,h3,.display{font-family:"Space Grotesk","Inter",sans-serif;line-height:1.08;margin:0;letter-spacing:-.02em}
h1{font-size:clamp(2.05rem,7.4vw,3.5rem);font-weight:700}
h2{font-size:clamp(1.5rem,4.6vw,2.15rem);font-weight:700}
h3{font-size:1.06rem;font-weight:600;letter-spacing:0}
p{margin:.6rem 0 0}
a{color:inherit}
.mono{font-family:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.72rem;
 letter-spacing:.14em;text-transform:uppercase}
.wrap{max-width:var(--max);margin:0 auto;padding:0 18px}
section{padding:52px 0}
.hair{border-top:1px solid var(--line)}
/* language visibility — revert keeps each element's native display (inline for
   spans, block for paragraphs) so no rule can leak the wrong language */
html[data-lang="fr"] .en-only{display:none !important}
html[data-lang="en"] .fr-only{display:none !important}
html[data-lang="en"] .en-only{display:revert !important}
html[data-lang="fr"] .fr-only{display:revert !important}
:is(a,button):focus-visible{outline:3px solid var(--cyan);outline-offset:2px;border-radius:6px}

/* top bar */
.bar{background:var(--navy);color:#EAF2FF;font-size:.8rem}
.bar .wrap{display:flex;gap:14px;justify-content:space-between;align-items:center;padding:9px 18px;flex-wrap:wrap}
.bar a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.35)}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#3BE08A;margin-right:6px;vertical-align:1px}

/* nav */
.nav{position:sticky;top:0;z-index:40;background:rgba(247,250,252,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:14px;padding:11px 18px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}
.brand svg{flex:0 0 auto}
.brand b{font-family:"Space Grotesk",sans-serif;font-size:1.02rem;letter-spacing:-.01em;display:block;line-height:1.05}
.brand .sub{display:block;font-size:.68rem;color:var(--mute);letter-spacing:.06em;text-transform:uppercase}
.nav nav{margin-left:auto;display:none;gap:18px;font-size:.9rem}
.nav nav a{text-decoration:none;color:var(--navy);opacity:.85}
.nav nav a:hover{opacity:1}
.lang{display:flex;margin-left:auto;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:#fff}
.lang button{border:0;background:transparent;padding:7px 12px;font:600 .78rem Inter;color:var(--mute);cursor:pointer}
.lang button.is-on{background:var(--navy);color:#fff}
.cta{background:var(--wa);color:#fff;text-decoration:none;padding:10px 14px;border-radius:999px;font-weight:600;font-size:.86rem;white-space:nowrap}
.cta.small{display:none}

/* hero */
.hero{padding-top:34px}
.eyebrow{color:var(--cyan-d);font-weight:600}
.hero h1 em{font-style:normal;color:var(--cyan-d)}
.lede{font-size:1.06rem;color:#24395C;max-width:56ch}
.hero-grid{display:grid;gap:26px;align-items:center}
.hero-media{position:relative;border-radius:var(--r);overflow:hidden;border:1px solid var(--line);background:#fff}
.hero-media img{display:block;width:100%;height:100%;object-fit:cover;aspect-ratio:4/5}
.hero-media .tag{position:absolute;left:12px;bottom:12px;background:rgba(14,35,71,.9);color:#fff;padding:7px 11px;border-radius:10px;font-size:.72rem}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 18px;border-radius:12px;text-decoration:none;font-weight:600;border:1px solid transparent;cursor:pointer}
.btn-primary{background:var(--wa);color:#fff}
.btn-ghost{background:#fff;color:var(--navy);border-color:var(--line)}
.btn svg{width:18px;height:18px;fill:currentColor}
.facts{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
.fact{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 13px;font-size:.8rem;color:#24395C}
.fact b{font-family:"Space Grotesk";color:var(--navy)}

/* steps */
.steps{background:var(--navy);color:#fff}
.steps h2{color:#fff}
.steps .mono{color:#7FD9EA}
.step{border-top:1px solid rgba(255,255,255,.18);padding:18px 0;display:grid;gap:6px}
.step .n{font-family:"JetBrains Mono";color:var(--cyan);font-size:.8rem}
.step h3{color:#fff}
.step p{color:#C7D6EE;font-size:.95rem;margin:0}
.grid3{display:grid;gap:0}
@media(min-width:860px){.grid3{grid-template-columns:repeat(3,1fr);gap:26px}.step{border-top:0;border-left:1px solid rgba(255,255,255,.18);padding:0 0 0 20px}}

/* catalogue */
.cat-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.search{position:sticky;top:58px;z-index:20;background:var(--paper);padding:14px 0 10px}
.search input{width:100%;padding:14px 16px;border-radius:12px;border:1px solid var(--line);font:16px Inter;background:#fff}
.search input:focus{outline:none;border-color:var(--cyan);box-shadow:0 0 0 4px var(--cyan-soft)}
.chips{display:flex;gap:8px;overflow-x:auto;padding:10px 0 4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{border:1px solid var(--line);background:#fff;color:var(--navy);padding:9px 13px;border-radius:999px;font:600 .82rem Inter;cursor:pointer;white-space:nowrap}
.chip.is-on{background:var(--navy);color:#fff;border-color:var(--navy)}
.t-list{list-style:none;margin:8px 0 0;padding:0;border-top:1px solid var(--line)}
.t-row{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:center;padding:13px 2px;border-bottom:1px solid var(--line)}
.t-name{font-weight:500}
.t-price{font-family:"JetBrains Mono";font-size:.92rem;color:var(--navy);white-space:nowrap}
.t-price small{font-size:.66rem;color:var(--mute)}
.t-btn{grid-column:1 / -1;justify-self:start;display:inline-flex;align-items:center;gap:7px;background:var(--cyan-soft);color:#075A6E;border:1px solid #BFE9F2;border-radius:10px;padding:8px 12px;font:600 .8rem Inter;cursor:pointer}
.t-btn svg{width:15px;height:15px;fill:#075A6E}
.t-btn:hover{background:#D3EFF6}
.note{font-size:.82rem;color:var(--mute);margin-top:12px}
@media(min-width:760px){
 .t-row{grid-template-columns:1fr auto auto;gap:18px}
 .t-btn{grid-column:auto;justify-self:end}
}

/* prep */
.cards{display:grid;gap:14px}
@media(min-width:760px){.cards{grid-template-columns:repeat(3,1fr)}}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:18px}
.card .mono{color:var(--cyan-d)}
.card h3{margin-top:8px;color:var(--navy)}
.pill{display:inline-block;background:var(--cyan-soft);color:#075A6E;border-radius:999px;padding:4px 10px;font:600 .72rem Inter;margin-top:10px}

/* results */
.split{display:grid;gap:16px}
@media(min-width:820px){.split{grid-template-columns:1.1fr .9fr;gap:26px;align-items:center}}
.shot{border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}
.shot img{display:block;width:100%;height:auto}
ul.ticks{list-style:none;padding:0;margin:12px 0 0}
ul.ticks li{position:relative;padding-left:26px;margin:9px 0;color:#24395C}
ul.ticks li::before{content:"";position:absolute;left:0;top:.45em;width:14px;height:8px;border-left:2.5px solid var(--cyan-d);border-bottom:2.5px solid var(--cyan-d);transform:rotate(-45deg)}

/* services */
.svc{display:grid;gap:14px}
@media(min-width:760px){.svc{grid-template-columns:repeat(3,1fr)}}
.svc .card{border-top:3px solid var(--cyan)}
.svc .mono{color:var(--mute)}

/* proof */
.proof{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.stats{display:flex;gap:24px;flex-wrap:wrap;margin-top:16px}
.stat b{font-family:"Space Grotesk";font-size:1.7rem;color:var(--navy);display:block;line-height:1}
.stat span{font-size:.82rem;color:var(--mute)}
.who{display:flex;gap:14px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:14px;margin-top:18px}
.who .av{width:52px;height:52px;border-radius:50%;background:var(--cyan);color:#04303C;display:grid;place-items:center;font:700 1.1rem "Space Grotesk";flex:0 0 auto}
.who b{display:block;font-family:"Space Grotesk";color:var(--navy)}
.who span{font-size:.88rem;color:var(--mute)}

/* contact */
.contact-grid{display:grid;gap:20px}
@media(min-width:860px){.contact-grid{grid-template-columns:1fr 1fr}}
.contact-box{background:var(--navy);color:#fff;border-radius:var(--r);padding:22px}
.contact-box h3{color:#fff}
.contact-box .mono{color:#7FD9EA}
.contact-box a{color:#fff}
.row{display:flex;gap:12px;padding:11px 0;border-top:1px solid rgba(255,255,255,.15);font-size:.95rem}
.row .k{font-family:"JetBrains Mono";font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:#7FD9EA;min-width:88px;padding-top:3px}

/* faq */
.faq{background:#fff;border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:2px 16px}
.faq summary{cursor:pointer;padding:14px 0;font-weight:600;color:var(--navy);list-style:none}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";float:right;color:var(--cyan-d);font-weight:700}
.faq[open] summary::after{content:"–"}
.faq p{margin:0 0 14px;color:#24395C}

/* footer + sticky */
footer{background:var(--navy);color:#C7D6EE;padding:28px 0 96px;font-size:.86rem}
footer a{color:#fff}
.sticky-wa{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;display:flex;gap:10px}
.sticky-wa a{flex:1;justify-content:center;padding:15px 18px;border-radius:14px;text-decoration:none;font-weight:700;display:flex;align-items:center;gap:9px}
.sticky-wa .w{background:var(--wa);color:#fff;box-shadow:0 8px 22px rgba(11,122,62,.35)}
.sticky-wa .c{background:#fff;color:var(--navy);border:1px solid var(--line)}
.sticky-wa svg{width:18px;height:18px;fill:currentColor}
@media(min-width:900px){.sticky-wa{display:none}footer{padding-bottom:28px}.nav nav{display:flex}.cta.small{display:inline-flex}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
"""

HTML = f"""<!doctype html>
<html lang="fr" data-lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Afrique Labo SARL — Laboratoire d'analyses médicales à Bessengue, Douala</title>
<meta name="description" content="Laboratoire multidisciplinaire d'analyses de biologie médicale à Bessengue, Douala. Tarifs affichés, demande par WhatsApp, préparation au prélèvement et résultats.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0E2347">
<meta property="og:title" content="Afrique Labo SARL — Analyses médicales à Douala">
<meta property="og:description" content="Tarifs affichés, demande par WhatsApp, préparation claire. Feu rouge Bessengue, Douala.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{JSONLD}</script>
</head>
<body>

<div class="bar"><div class="wrap">
  <span><span class="dot"></span><span class="fr-only">Ouvert 24h/24 · Feu rouge Bessengue, Douala</span><span class="en-only">Open 24/7 · Bessengue roundabout, Douala</span></span>
  <a href="tel:+{WA}">690 54 70 93</a>
</div></div>

<header class="nav"><div class="wrap">
  <a class="brand" href="#top" aria-label="Afrique Labo">
    <svg width="38" height="38" viewBox="0 0 38 38" role="img" aria-hidden="true">
      <rect width="38" height="38" rx="11" fill="#0E2347"/>
      <path d="M19 8c-4.9 0-8.9 4-8.9 8.9 0 2.2.8 4.2 2.1 5.7l-.9 6.4h15.4l-.9-6.4c1.3-1.5 2.1-3.5 2.1-5.7C27.9 12 23.9 8 19 8Zm0 2.6a6.3 6.3 0 0 1 6.3 6.3c0 1.5-.5 2.9-1.4 4l-9.8 0a6.2 6.2 0 0 1-1.4-4A6.3 6.3 0 0 1 19 10.6Z" fill="#12B4D6"/>
      <path d="M15.6 17.4h6.8M17.4 15.2v4.4" stroke="#0E2347" stroke-width="1.6" stroke-linecap="round"/>
    </svg>
    <span><b>AFRIQUE LABO</b><span class="sub"><span class="fr-only">Analyses médicales · Douala</span><span class="en-only">Medical laboratory · Douala</span></span></span>
  </a>
  <nav>
    <a href="#catalogue"><span class="fr-only">Analyses &amp; tarifs</span><span class="en-only">Tests &amp; prices</span></a>
    <a href="#preparation"><span class="fr-only">Préparation</span><span class="en-only">Preparation</span></a>
    <a href="#resultats"><span class="fr-only">Résultats</span><span class="en-only">Results</span></a>
    <a href="#contact"><span class="fr-only">Accès</span><span class="en-only">Visit us</span></a>
  </nav>
  <div class="lang" role="group" aria-label="Langue / Language">
    <button id="btn-fr" class="is-on" type="button">FR</button>
    <button id="btn-en" type="button">EN</button>
  </div>
  <a class="cta small" href="https://wa.me/{WA}?text=Bonjour%20Afrique%20Labo%2C%20je%20souhaite%20des%20informations.">
    <span class="fr-only">Demander</span><span class="en-only">Ask us</span>
  </a>
</div></header>

<main id="top">

<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="mono eyebrow"><span class="fr-only">Laboratoire multidisciplinaire · Bessengue, Douala</span><span class="en-only">Multidisciplinary laboratory · Bessengue, Douala</span></p>
    <h1><span class="fr-only">Vos analyses, <em>du prélèvement au résultat.</em></span><span class="en-only">Your tests, <em>from sample to result.</em></span></h1>
    <p class="lede"><span class="fr-only">Le tarif est affiché avant de venir, la demande part sur WhatsApp, et la préparation est expliquée noir sur blanc. Vous ne venez plus « demander pour voir ».</span>
      <span class="en-only">The price is shown before you come, the request goes out on WhatsApp, and the preparation rules are written out. You no longer come just to “ask and see”.</span></p>
    <div class="actions">
      <a class="btn btn-primary" href="https://wa.me/{WA}?text=Bonjour%20Afrique%20Labo%2C%20je%20souhaite%20faire%20une%20analyse.%20Je%20regarde%20laquelle%20ici%20%3A">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
        <span class="fr-only">Demander une analyse</span><span class="en-only">Request a test</span>
      </a>
      <a class="btn btn-ghost" href="#catalogue"><span class="fr-only">Voir les tarifs</span><span class="en-only">See the prices</span></a>
    </div>
    <div class="facts">
      <span class="fact"><b>24h/24</b> <span class="fr-only">accueil</span><span class="en-only">open</span></span>
      <span class="fact"><b>{len(TESTS)}</b> <span class="fr-only">tests affichés</span><span class="en-only">tests listed</span></span>
      <span class="fact"><b>FR / EN</b></span>
      <span class="fact"><b>Bessengue</b> <span class="fr-only">au-dessus de Wafacash</span><span class="en-only">above Wafacash</span></span>
    </div>
  </div>
  <div class="hero-media">
    <img src="{IMG_HERO}" alt="Biologiste médicale au microscope dans un laboratoire moderne">
    <span class="tag mono"><span class="fr-only">Biologie médicale · Douala</span><span class="en-only">Medical biology · Douala</span></span>
  </div>
</div></section>

<section class="steps"><div class="wrap">
  <p class="mono"><span class="fr-only">Le parcours, sans zone d'ombre</span><span class="en-only">The path, with nothing hidden</span></p>
  <h2><span class="fr-only">Trois étapes, et vous savez où vous allez.</span><span class="en-only">Three steps, and you know where you're going.</span></h2>
  <div class="grid3" style="margin-top:26px">
    <div class="step"><span class="n">01</span><h3><span class="fr-only">L'ordonnance</span><span class="en-only">The prescription</span></h3>
      <p><span class="fr-only">Envoyez le nom des analyses sur WhatsApp : tarif, préparation et meilleur moment vous reviennent dans la conversation.</span><span class="en-only">Send the test names on WhatsApp: price, preparation and best time come back in the same conversation.</span></p></div>
    <div class="step"><span class="n">02</span><h3><span class="fr-only">Le prélèvement</span><span class="en-only">The sample</span></h3>
      <p><span class="fr-only">Vous venez à Bessengue, au-dessus de Wafacash. À jeun si l'analyse l'exige — l'eau reste permise.</span><span class="en-only">You come to Bessengue, above Wafacash. Fasting if the test requires it — water is allowed.</span></p></div>
    <div class="step"><span class="n">03</span><h3><span class="fr-only">Le résultat</span><span class="en-only">The result</span></h3>
      <p><span class="fr-only">Retrait sur place, et demandez le mode d'envoi au guichet : nous confirmons ce qui est possible pour votre dossier.</span><span class="en-only">Collection on site — ask at the desk about sending: we confirm what is possible for your file.</span></p></div>
  </div>
</div></section>

<section id="catalogue"><div class="wrap">
  <div class="cat-head">
    <div>
      <p class="mono" style="color:var(--cyan-d)"><span class="fr-only">Catalogue · extraits 2026</span><span class="en-only">Catalogue · 2026 extracts</span></p>
      <h2><span class="fr-only">Cherchez votre analyse. Le prix est là.</span><span class="en-only">Find your test. The price is right there.</span></h2>
    </div>
    <p class="note" style="margin:0"><span class="fr-only">Tarifs indicatifs, confirmés avant le prélèvement.</span><span class="en-only">Indicative prices, confirmed before sampling.</span></p>
  </div>

  <div class="search">
    <input id="q" type="search" placeholder="Rechercher : glycémie, NFS, hépatite…" aria-label="Rechercher une analyse">
    <div class="chips" role="group" aria-label="Familles d'analyses">{CAT_CHIPS}</div>
  </div>

  <ul class="t-list" id="list">
{CATALOGUE_ROWS}
  </ul>
  <p class="note" id="count"></p>
  <p class="note"><span class="fr-only">La grille complète (plus de 100 lignes : bilans, sérologies, marqueurs) est envoyée sur WhatsApp avec votre tarif confirmé.</span>
    <span class="en-only">The full grid (100+ lines: panels, serologies, markers) is sent on WhatsApp with your confirmed price.</span></p>
</div></section>

<section id="preparation" class="hair"><div class="wrap">
  <p class="mono" style="color:var(--cyan-d)"><span class="fr-only">Préparation</span><span class="en-only">Preparation</span></p>
  <h2><span class="fr-only">Bien préparé, c'est un résultat de plus.</span><span class="en-only">Well prepared means one less retest.</span></h2>
  <div class="cards" style="margin-top:22px">
    <div class="card"><span class="mono">01 · <span class="fr-only">à jeun</span><span class="en-only">fasting</span></span>
      <h3><span class="fr-only">À jeun, quand c'est demandé</span><span class="en-only">Fasting, when required</span></h3>
      <p><span class="fr-only">Glycémie, cholestérol, triglycérides : 8 à 12 heures sans manger. L'eau est permise, le café non.</span><span class="en-only">Glucose, cholesterol, triglycerides: 8–12 hours without food. Water is fine, coffee is not.</span></p>
      <span class="pill"><span class="fr-only">si votre ordonnance le précise</span><span class="en-only">if your prescription says so</span></span></div>
    <div class="card"><span class="mono">02 · <span class="fr-only">à apporter</span><span class="en-only">to bring</span></span>
      <h3><span class="fr-only">Ordonnance et couverture</span><span class="en-only">Prescription and cover</span></h3>
      <p><span class="fr-only">L'ordonnance, votre carte de mutuelle ou d'assurance, et un ancien résultat si vous êtes suivi.</span><span class="en-only">The prescription, your insurance card, and a previous result if you are being followed up.</span></p></div>
    <div class="card"><span class="mono">03 · <span class="fr-only">hormones</span><span class="en-only">hormones</span></span>
      <h3><span class="fr-only">Le bon moment compte</span><span class="en-only">Timing matters</span></h3>
      <p><span class="fr-only">Pour les dosages hormonaux, venez le matin et demandez la consigne exacte au rendez-vous (heure, cycle).</span><span class="en-only">For hormone tests, come in the morning and ask for the exact instruction when booking (time, cycle).</span></p></div>
  </div>
</div></section>

<section id="resultats" class="hair"><div class="wrap split">
  <div>
    <p class="mono" style="color:var(--cyan-d)"><span class="fr-only">Résultats &amp; suivi</span><span class="en-only">Results &amp; follow-up</span></p>
    <h2><span class="fr-only">Un résultat utile, pas juste un chiffre.</span><span class="en-only">A useful result, not just a number.</span></h2>
    <ul class="ticks">
      <li><span class="fr-only"><b>Retrait sur place</b> à Bessengue, muni du reçu de prélèvement.</span><span class="en-only"><b>Collection on site</b> in Bessengue, with your sampling receipt.</span></li>
      <li><span class="fr-only"><b>Envoi sur demande</b> : nous confirmons au guichet ce qui est possible (WhatsApp ou e-mail) pour votre dossier.</span><span class="en-only"><b>Sending on request</b>: we confirm at the desk what is possible (WhatsApp or e-mail) for your file.</span></li>
      <li><span class="fr-only"><b>Urgences</b> : signalez-la au guichet à votre arrivée, elle est traitée en priorité.</span><span class="en-only"><b>Emergencies</b>: tell the desk on arrival, they are handled first.</span></li>
      <li><span class="fr-only"><b>Biologiste</b> disponible pour expliquer un résultat qui vous inquiète.</span><span class="en-only"><b>A biologist</b> is available to explain a result that worries you.</span></li>
    </ul>
    <div class="actions">
      <a class="btn btn-ghost" href="https://wa.me/{WA}?text=Bonjour%20Afrique%20Labo%2C%20j%27ai%20une%20question%20sur%20un%20r%C3%A9sultat.">
        <span class="fr-only">Poser une question</span><span class="en-only">Ask a question</span></a>
    </div>
  </div>
  <div class="shot"><img src="{IMG_SAMPLES}" alt="Tubes de prélèvement sanguin dans un laboratoire d'analyses"></div>
</div></section>

<section class="hair"><div class="wrap">
  <p class="mono" style="color:var(--cyan-d)"><span class="fr-only">Sur place</span><span class="en-only">On site</span></p>
  <h2><span class="fr-only">Trois services sous le même toit.</span><span class="en-only">Three services under one roof.</span></h2>
  <div class="svc" style="margin-top:22px">
    <div class="card"><span class="mono">01</span><h3><span class="fr-only">Analyses médicales</span><span class="en-only">Medical tests</span></h3>
      <p><span class="fr-only">Biochimie, hématologie, sérologie, hormonologie, bactériologie — plus de 100 lignes de catalogue.</span><span class="en-only">Biochemistry, haematology, serology, hormonology, bacteriology — 100+ catalogue lines.</span></p></div>
    <div class="card"><span class="mono">02</span><h3><span class="fr-only">Consultation médicale</span><span class="en-only">Medical consultation</span></h3>
      <p><span class="fr-only">Un médecin sur place pour lire vos résultats dans la foulée et décider de la suite.</span><span class="en-only">A doctor on site to read your results straight away and decide the next step.</span></p></div>
    <div class="card"><span class="mono">03</span><h3><span class="fr-only">Coaching santé, bien-être &amp; beauté</span><span class="en-only">Health, wellness &amp; beauty coaching</span></h3>
      <p><span class="fr-only">Accompagnement pour agir sur les causes : alimentation, suivi, prévention.</span><span class="en-only">Support to act on the causes: nutrition, follow-up, prevention.</span></p></div>
  </div>
</div></section>

<section class="proof"><div class="wrap split">
  <div>
    <p class="mono" style="color:var(--mute)"><span class="fr-only">Confiance</span><span class="en-only">Trust</span></p>
    <h2><span class="fr-only">Un laboratoire connu de ses patients.</span><span class="en-only">A laboratory its patients already know.</span></h2>
    <div class="stats">
      <div class="stat"><b>24h/24</b><span><span class="fr-only">accueil annoncé</span><span class="en-only">stated opening</span></span></div>
      <div class="stat"><b>5 500+</b><span><span class="fr-only">abonnés Facebook</span><span class="en-only">Facebook followers</span></span></div>
      <div class="stat"><b>4,5/5</b><span><span class="fr-only">avis Google</span><span class="en-only">Google rating</span></span></div>
    </div>
    <div class="who">
      <span class="av">DT</span>
      <span><b>Dr Takala</b><span class="fr-only">Biologiste médicale — direction du laboratoire</span><span class="en-only">Medical biologist — laboratory direction</span></span>
    </div>
    <p class="note"><span class="fr-only">Photo d'illustration : les vraies photos de votre équipe et de la devanture remplacent celles-ci à la mise en ligne.</span>
      <span class="en-only">Illustrative photo: your real team and storefront photos replace these at launch.</span></p>
  </div>
  <div class="shot"><img src="{IMG_RECEPTION}" alt="Accueil d'un laboratoire moderne à Douala"></div>
</div></section>

<section id="contact" class="hair"><div class="wrap">
  <p class="mono" style="color:var(--cyan-d)"><span class="fr-only">Accès &amp; contact</span><span class="en-only">Visit &amp; contact</span></p>
  <h2><span class="fr-only">Vous êtes à deux minutes du feu rouge.</span><span class="en-only">You are two minutes from the roundabout.</span></h2>
  <div class="contact-grid" style="margin-top:22px">
    <div class="contact-box">
      <h3 class="mono" style="letter-spacing:.14em"><span class="fr-only">Nous joindre</span><span class="en-only">Reach us</span></h3>
      <div class="row"><span class="k">WhatsApp</span><span><a href="https://wa.me/{WA}">690 54 70 93</a></span></div>
      <div class="row"><span class="k"><span class="fr-only">Téléphone</span><span class="en-only">Phone</span></span><span><a href="tel:+{WA}">690 54 70 93</a></span></div>
      <div class="row"><span class="k">E-mail</span><span><a href="mailto:Afrique.labo@gmail.com">Afrique.labo@gmail.com</a></span></div>
      <div class="row"><span class="k"><span class="fr-only">Horaires</span><span class="en-only">Hours</span></span><span><span class="fr-only">Ouvert 24h/24</span><span class="en-only">Open 24/7</span></span></div>
      <div class="row"><span class="k"><span class="fr-only">Paiement</span><span class="en-only">Payment</span></span><span><span class="fr-only">Espèces · Orange Money · MoneyGram</span><span class="en-only">Cash · Orange Money · MoneyGram</span></span></div>
    </div>
    <div class="card">
      <span class="mono" style="color:var(--cyan-d)"><span class="fr-only">Adresse</span><span class="en-only">Address</span></span>
      <h3><span class="fr-only">Feu rouge Bessengue</span><span class="en-only">Bessengue roundabout</span></h3>
      <p><span class="fr-only">Immeuble Nkake, au-dessus de Wafacash, face Total — Douala, Cameroun.</span><span class="en-only">Immeuble Nkake, above Wafacash, opposite Total — Douala, Cameroon.</span></p>
      <div class="actions">
        <a class="btn btn-ghost" href="https://www.google.com/maps/search/Afrique+Labo+Bessengue+Douala" target="_blank" rel="noopener">
          <span class="fr-only">Ouvrir dans Maps</span><span class="en-only">Open in Maps</span></a>
        <a class="btn btn-primary" href="https://wa.me/{WA}?text=Bonjour%2C%20je%20viens%20au%20laboratoire.%20Vous%20%C3%AAtes%20ouverts%20maintenant%20%3F">
          <span class="fr-only">Je viens maintenant</span><span class="en-only">I'm coming now</span></a>
      </div>
      <p class="note"><span class="fr-only">Repère simple : feu rouge de Bessengue, au-dessus du comptoir Wafacash.</span><span class="en-only">Simple landmark: Bessengue roundabout, above the Wafacash counter.</span></p>
    </div>
  </div>
</div></section>

<section class="hair"><div class="wrap">
  <p class="mono" style="color:var(--cyan-d)"><span class="fr-only">Questions fréquentes</span><span class="en-only">Frequently asked</span></p>
  <h2 style="margin-bottom:16px"><span class="fr-only">Ce qu'on vous demande au guichet, écrit ici.</span><span class="en-only">What people ask at the desk, written here.</span></h2>
{FAQ_HTML}
</div></section>

</main>

<footer><div class="wrap">
  <p><b>AFRIQUE LABO SARL</b> — <span class="fr-only">Laboratoire multidisciplinaire d'analyses de biologie médicale</span><span class="en-only">Multidisciplinary medical biology laboratory</span><br>
  <span class="fr-only">Feu rouge Bessengue, Immeuble Nkake (au-dessus de Wafacash), Douala · 690 54 70 93</span><span class="en-only">Bessengue roundabout, Immeuble Nkake (above Wafacash), Douala · 690 54 70 93</span></p>
  <p style="opacity:.75"><span class="fr-only">Maquette préparée par AMK pour Afrique Labo SARL — contenu et tarifs à valider par le laboratoire.</span><span class="en-only">Mockup prepared by AMK for Afrique Labo SARL — content and prices to be validated by the laboratory.</span></p>
</div></footer>

<div class="sticky-wa">
  <a class="w" href="https://wa.me/{WA}?text=Bonjour%20Afrique%20Labo%2C%20je%20souhaite%20faire%20une%20analyse.">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1a11 11 0 0 1-5.6-4.9c-.4-.7-.6-1.4-.5-2 .1-.6.6-1.4 1.1-1.7.3-.2.7-.2.9.2l.8 1.4c.1.3.1.5-.1.8l-.4.5c-.2.2-.2.4-.1.6.4.8 1.5 2 2.4 2.4.2.1.4.1.6-.1l.5-.5c.2-.2.5-.3.8-.1l1.4.8c.4.2.4.6.2.9Z"/></svg>
    <span class="fr-only">WhatsApp</span><span class="en-only">WhatsApp</span>
  </a>
  <a class="c" href="tel:+{WA}"><span class="fr-only">Appeler</span><span class="en-only">Call</span></a>
</div>

<script>
(function(){{
  var html=document.documentElement, k='labo-lang';
  function setLang(l){{
    html.setAttribute('data-lang',l); html.lang=l;
    document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
    document.getElementById('btn-en').classList.toggle('is-on',l==='en');
    try{{localStorage.setItem(k,l)}}catch(e){{}}
    var qi=document.getElementById('q');
    if(qi) qi.placeholder = (l==='fr') ? 'Rechercher : glycémie, NFS, hépatite…' : 'Search: glucose, CBC, hepatitis…';
    document.querySelectorAll('.t-btn').forEach(function(b){{
      b.title = (l==='fr' ? 'Demander : ' : 'Request: ') + (l==='fr'?b.dataset.testFr:b.dataset.testEn) + ' — ' + b.dataset.price + ' FCFA';
    }});
    filter();
  }}
  document.getElementById('btn-fr').addEventListener('click',function(){{setLang('fr')}});
  document.getElementById('btn-en').addEventListener('click',function(){{setLang('en')}});
  try{{ var saved=localStorage.getItem(k); if(saved) setLang(saved); }}catch(e){{}}

  // WhatsApp deep link per test, language-aware
  var num='{WA}';
  document.querySelectorAll('.t-btn').forEach(function(b){{
    b.addEventListener('click',function(){{
      var l=html.getAttribute('data-lang');
      var name = l==='fr'?b.dataset.testFr:b.dataset.testEn;
      var msg = l==='fr'
        ? 'Bonjour Afrique Labo, je souhaite faire cette analyse : ' + name + ' (' + b.dataset.price + ' FCFA vu sur votre site). Quand puis-je passer ?'
        : 'Hello Afrique Labo, I would like to do this test: ' + name + ' (' + b.dataset.price + ' FCFA from your website). When can I come?';
      window.open('https://wa.me/'+num+'?text='+encodeURIComponent(msg),'_blank','noopener');
    }});
  }});

  // catalogue search + filter
  var q=document.getElementById('q'), rows=[].slice.call(document.querySelectorAll('.t-row')),
      chips=[].slice.call(document.querySelectorAll('.chip')), count=document.getElementById('count'), cat='all';
  function filter(){{
    var term=(q.value||'').trim().toLowerCase(), l=html.getAttribute('data-lang'), visible=0;
    rows.forEach(function(r){{
      var hay=(l==='fr'?r.dataset.fr:r.dataset.en)+' '+(l==='fr'?r.dataset.en:r.dataset.fr);
      var ok=(cat==='all'||r.dataset.cat===cat)&&(!term||hay.indexOf(term)>-1);
      r.style.display=ok?'':'none'; if(ok)visible++;
    }});
    count.textContent = l==='fr' ? visible+' analyse(s) affichée(s)' : visible+' test(s) shown';
  }}
  q.addEventListener('input',filter);
  chips.forEach(function(c){{c.addEventListener('click',function(){{
    chips.forEach(function(x){{x.classList.remove('is-on')}}); c.classList.add('is-on');
    cat=c.dataset.cat; filter();
  }})}});
  filter();
}})();
</script>
</body>
</html>
"""

OUT.write_text(HTML, encoding='utf-8')
kb = OUT.stat().st_size / 1024
print(f"OK {OUT} — {kb:.0f} KB · tests: {len(TESTS)} · img hero {len(IMG_HERO)//1024}KB samples {len(IMG_SAMPLES)//1024}KB reception {len(IMG_RECEPTION)//1024}KB")
