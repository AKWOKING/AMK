# -*- coding: utf-8 -*-
"""Build demos/concept-skye-v1.html — NAMED gift for Cabinet Dentaire The Skye.
Base: concept-oracare-v3.html (same proven dental machinery), rebranded:
- sky-blue palette sampled from their logo (deep #0E63A0 / sky #38BDF8 / ice bg)
- tagline « Souriez à l'infini », FR-first bilingual
- real proof only: 100% recommend (19 FB reviews), 1,196 likes, Dr Djuinne Sandrine (mondocteur)
- WA +237 677 79 69 99, TS- refs, facebook.com/237DentalClinic, Bonamoussadi address
- prices DEMO except consultation 10,000 (published on mondocteur for this cabinet)
"""
import re, base64, io, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
s = (ROOT / "demos" / "concept-oracare-v3.html").read_text(encoding="utf-8")

# ---------- 1. palette: warm cream/teal/gold -> clinical sky blues ----------
color_map = [
    ("#F7F1E8", "#F2F9FE"),  # cream
    ("#FBF7F0", "#FFFFFF"),  # cream2
    ("#EDF3EE", "#E3F3FC"),  # sage tint
    ("#7FA88F", "#2E9BD6"),  # sage deep
    ("#16323A", "#0B4A78"),  # navy (deep brand blue)
    ("#1E4152", "#0E63A0"),  # navy2
    ("#1C2B33", "#102A40"),  # ink
    ("#5C6F78", "#5B7284"),  # slate
    ("#C9A24B", "#0EA5E9"),  # gold -> sky accent
    ("#A9842F", "#0284C7"),  # gold text
    ("rgba(22,50,58,", "rgba(11,74,120,"),
    ("rgba(127,168,143,", "rgba(46,155,214,"),
    ("rgba(201,162,75,", "rgba(14,165,233,"),
    ("rgba(247,241,232,", "rgba(242,249,254,"),
    ("rgba(251,247,240,", "rgba(255,255,255,"),
    ("#0F172A", "#0B4A78"),
]
for a, b in color_map:
    s = s.replace(a, b)

# ---------- 2. global literals ----------
lit = [
    ("OraCare Dental Clinic — Molyko, Buea | Gentle Care · Clear FCFA Prices",
     "Cabinet Dentaire The Skye — Bonamoussadi, Douala | Souriez à l'infini · Tarifs FCFA"),
    ("OraCare Dental Clinic", "Cabinet Dentaire The Skye"),
    ("OraCare", "The Skye"),
    ("237672526686", "237677796999"),
    ("+237 672 52 66 86", "+237 677 79 69 99"),
    ("+237 6 72 52 66 86", "+237 6 77 79 69 99"),
    ("tel:+237672526686", "tel:+237677796999"),
    ("snkafuarnold11@gmail.com", "cabinetheskye@gmail.com"),
    ("facebook.com/p/Oracare237-100075164312902", "facebook.com/237DentalClinic"),
    ("Oracare237-100075164312902", "237DentalClinic"),
    ("St. Pius Hospital, Mayor's Street, Molyko, Buea",
     "Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala"),
    ("St. Pius Hospital, Mayor's Street", "Immeuble Stella & Joyce, Bonamoussadi"),
    ("l'hôpital St. Pius, Mayor's Street", "l'immeuble Stella & Joyce, Bonamoussadi"),
    ("l'hôpital St-Pius, Molyko", "Bonamoussadi, Petit terrain"),
    ("Inside St. Pius Hospital, Molyko", "Immeuble Stella & Joyce, Bonamoussadi"),
    ("À l'hôpital St-Pius, Molyko", "Immeuble Stella & Joyce, Bonamoussadi"),
    ("Molyko, Buea", "Bonamoussadi, Douala"),
    ("Molyko, Buéa", "Bonamoussadi, Douala"),
    ("Molyko", "Bonamoussadi"),
    ("Buea", "Douala"),
    ("Buéa", "Douala"),
    ("Mayor's Street", "Petit terrain"),
    ("OC-", "TS-"),
    ("Dr. A. Nkafu", "Dr Sandrine Djuinne"),
    ("Dr A. Nkafu", "Dre Sandrine Djuinne"),
    ("DENTAL CLINIC · MOLYKO", "CABINET DENTAIRE · BONAMOUSSADI"),
    ("CLINIQUE DENTAIRE · MOLYKO", "CABINET DENTAIRE · BONAMOUSSADI"),
    ("DENTAL CARE — MOLYKO, BUEA", "CABINET DENTAIRE — BONAMOUSSADI, DOUALA"),
    ("SOINS DENTAIRES — MOLYKO, BUEA", "SOINS DENTAIRES — BONAMOUSSADI, DOUALA"),
    # consultation price 5,000 -> 10,000 (published on mondocteur for The Skye)
    # NOTE: consultation only — bare replace("5,000") would corrupt the 15,000 cleaning card
    ("I'm the The Skye assistant", "I'm The Skye's assistant"),
    # sample hours -> directory hours, to confirm
    ("Mon–Sat · 8:00 am – 6:00 pm (sample hours)",
     "Mon–Fri 8:00–17:00 · Sat 8:00–14:00 (to confirm)"),
    ("Lun–Sam · 8h00 – 18h00 (horaires d'exemple)",
     "Lun–Ven 8h–17h · Sam 8h–14h (à confirmer)"),
]
for a, b in lit:
    s = s.replace(a, b)
# exact demo/anchored prices (consultation 10,000 published on mondocteur for The Skye)
s = s.replace('<div class="p-amt">5,000 ', '<div class="p-amt">10,000 ')
s = s.replace('<div class="p-amt">110,000 ', '<div class="p-amt">15,000 ')

# ---------- 3. all data-en / data-fr pairs, overridden by index ----------
ens = re.findall(r'data-en="([^"]*)"', s)
frs = re.findall(r'data-fr="([^"]*)"', s)
assert len(ens) == len(frs) == 155, (len(ens), len(frs))

NEW = {
 # idx: (new EN, new FR)
 0:  ("DENTAL CLINIC · BONAMOUSSADI", "CABINET DENTAIRE · BONAMOUSSADI"),
 1:  ("Prices", "Tarifs"),
 2:  ("Our work", "Nos soins"),
 3:  ("Find us", "Nous trouver"),
 4:  ("Smile results", "Résultats sourire"),
 8:  ("Smile without limits —", "Souriez à l'infini —"),
 9:  ("modern dentistry in Bonamoussadi", "des soins dentaires modernes à Bonamoussadi"),
 10: ("Quality dental care in a modern setting at Immeuble Stella & Joyce, Petit terrain — clear prices in FCFA, appointments by WhatsApp, in French and English.",
      "Des soins dentaires de qualité dans un cadre moderne, immeuble Stella & Joyce, Petit terrain — tarifs clairs en FCFA, rendez-vous par WhatsApp, en français et en anglais."),
 12: ("See our care", "Découvrir nos soins"),
 13: ("Immeuble Stella & Joyce, Bonamoussadi", "Immeuble Stella & Joyce, Bonamoussadi"),
 15: ("💬 Prefer to chat? Our 24/7 assistant answers in French &amp; English",
      "💬 Une question ? Notre assistant 24h/7 répond en français et en anglais"),
 18: ("Many patients hesitate to ask about prices. So we publish them — in plain FCFA. Pay by cash, MTN Mobile Money or Orange Money (to confirm).",
      "Beaucoup de patients hésitent à demander le prix. Nous l'affichons donc — en FCFA, clairement. Espèces, MTN Mobile Money ou Orange Money (à confirmer)."),
 47: ("A bright smile starts here", "Un sourire éclatant commence ici"),
 48: ("Restorations, cosmetic whitening and orthodontics — what our patients ask for most.",
      "Restaurations, blanchiment esthétique et orthodontie — ce que nos patients demandent le plus."),
 49: ("FOLLOW OUR SMILES ON FACEBOOK ↗", "SUIVEZ NOS SOURIRES SUR FACEBOOK ↗"),
 57: ("Nervous? That's normal — « Souriez à l'infini » starts with feeling at ease.",
      "Nerveux ? C'est normal — « souriez à l'infini » commence par être à l'aise."),
 65: ("Your dentist", "Votre dentiste"),
 66: ("Skilled. Gentle. On your side.", "Compétente. Douce. De votre côté."),
 67: ("Our team makes every visit comfortable and stress-free — from your first WhatsApp message to your final check-up, the same people follow your smile.",
      "Notre équipe fait de chaque visite un moment confortable et sans stress — de votre premier message WhatsApp au dernier contrôle, les mêmes personnes suivent votre sourire."),
 69: ("Dr Sandrine Djuinne — Dental Surgeon", "Dre Sandrine Djuinne — Chirurgien-dentiste"),
 70: ("General · Cosmetic · Restorative", "Médecine dentaire · Esthétique · Prothèses"),
 72: ("Inside The Skye, Bonamoussadi", "Au Cabinet The Skye, Bonamoussadi"),
 73: ("Easy to find at Petit terrain — Immeuble Stella & Joyce, with parking nearby.",
      "Facile à trouver à Petit terrain — immeuble Stella & Joyce, avec parking à proximité."),
 81: ("Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala — we'll see you at the reception.",
      "Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala — nous vous attendons à la réception."),
 89: ("“I was afraid of the dentist for years. The team explained every step before they started — and it was painless. I finally smile without thinking about it.”",
      "« J'avais peur du dentiste depuis des années. L'équipe a expliqué chaque étape avant de commencer — et c'était indolore. Je souris enfin sans y penser. »"),
 90: ("— Happy patient (sample review)", "— Patient satisfait (avis d'exemple)"),
 91: ("<b>100% recommended · 19 reviews</b> on our Facebook page — <a style='color:#0284C7;font-weight:800' href='https://www.facebook.com/237DentalClinic/reviews/' target='_blank' rel='noopener'>read every review ↗</a>",
      "<b>100 % de recommandations · 19 avis</b> sur notre page Facebook — <a style='color:#0284C7;font-weight:800' href='https://www.facebook.com/237DentalClinic/reviews/' target='_blank' rel='noopener'>lire tous les avis ↗</a>"),
 97: ("Cash, MTN Mobile Money or Orange Money (to confirm). The price you're quoted before we begin is the price you pay — no surprises at the end.",
      "Espèces, MTN Mobile Money ou Orange Money (à confirmer). Le prix indiqué avant de commencer est le prix payé — sans surprise à la fin."),
 103: ("Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala. Use the Get Directions button above and we'll see you at the reception.",
       "Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala. Utilisez le bouton Itinéraire ci-dessus et nous vous attendons à la réception."),
 136: ("CABINET DENTAIRE · BONAMOUSSADI", "CABINET DENTAIRE · BONAMOUSSADI"),
 137: ("Modern, gentle dental care in Bonamoussadi, Douala — clear FCFA prices, French & English, appointments on WhatsApp.",
       "Des soins dentaires modernes et doux à Bonamoussadi, Douala — tarifs FCFA clairs, français et anglais, rendez-vous sur WhatsApp."),
 140: ("Mon–Fri 8:00–17:00 · Sat 8:00–14:00 (to confirm)",
       "Lun–Ven 8h–17h · Sam 8h–14h (à confirmer)"),
 149: ("© 2026 Cabinet Dentaire The Skye · Bonamoussadi, Douala",
       "© 2026 Cabinet Dentaire The Skye · Bonamoussadi, Douala"),
 152: ("The Skye Assistant", "Assistant The Skye"),
 153: ("Online · 24/7 · answers in seconds (concept demo)",
       "En ligne · 24h/7 · répond en quelques secondes (démo concept)"),
}

def pair_repl(m, counter=[0]):
    i = counter[0]; counter[0] += 1
    en, fr = NEW.get(i, (m.group(2), m.group(3)))
    return f'{m.group(1)}data-en="{en}" data-fr="{fr}"{m.group(4)}>'

s = re.sub(r'(<[^>]*?)data-en="([^"]*)" data-fr="([^"]*)"([^>]*?)>', pair_repl, s)

# ---------- 4. hero chips: real review proof ----------
s = s.replace(
 '📍 <span data-en="Immeuble Stella & Joyce, Bonamoussadi" data-fr="Immeuble Stella & Joyce, Bonamoussadi">',
 '⭐ <span data-en="100% recommended · 19 Facebook reviews" data-fr="100 % recommandent · 19 avis Facebook">')
s = s.replace('<span class="chip">🗣 EN | FR</span>',
              '<span class="chip">📍 <span data-en="Stella & Joyce building, Bonamoussadi" data-fr="Immeuble Stella & Joyce, Bonamoussadi">Immeuble Stella & Joyce, Bonamoussadi</span></span>')

# avatar-stack badge: real follower count
s = s.replace('<span class="more">You?</span>', '<span class="more">1 196 ❤</span>')
s = s.replace('title="Concept placeholder — real patient photos are added only with permission at launch"',
              'title="1 196 mentions J’aime sur Facebook — vos vraies photos patients remplacent ces images au lancement"')

# ---------- 5. logo mark: SVG two-blue tooth with smile-arrow ----------
s = s.replace(
 '<span class="tooth">🦷</span>',
 '<span class="tooth"><svg viewBox="0 0 28 28" width="22" height="22" aria-hidden="true">'
 '<path fill="#fff" d="M14 3.5c-2.6 0-3.9-1-6-1-2.6 0-4 2-4 4.6 0 4.6 1.3 7.2 2 10.3.5 2.3.7 6.1 2.7 6.1 1.9 0 1.7-4.6 2.6-6 .7-1.2 1.4-1.6 2.7-1.6s2 .4 2.7 1.6c.9 1.4.7 6 2.6 6 2 0 2.2-3.8 2.7-6.1.7-3.1 2-5.7 2-10.3 0-2.6-1.4-4.6-4-4.6-2.1 0-3.4 1-6 1z"/>'
 '<path d="M8.5 12.5c2.4 3.1 8.6 3.1 11 0" fill="none" stroke="#38BDF8" stroke-width="1.7" stroke-linecap="round"/>'
 '<path d="M8.5 12.5l-1.6-1.4M19.5 12.5l1.6-1.4" fill="none" stroke="#38BDF8" stroke-width="1.7" stroke-linecap="round"/>'
 '</svg></span>')

# ---------- 6. hero image + reception image -> tailored photos ----------
def b64_jpg(path, width, quality):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

hero_uri = b64_jpg(ROOT / "demos" / "img" / "skye-hero.jpg", 860, 80)
team_uri = b64_jpg(ROOT / "demos" / "img" / "skye-team.jpg", 760, 80)

def replace_img_by_alt(txt, alt, uri):
    pat = re.compile(r'(<img[^>]*src=")data:image/jpeg;base64,[^"]*("[^>]*alt="' + re.escape(alt) + r'")')
    return pat.sub(lambda m: m.group(1) + uri + m.group(2), txt, count=1)

s = replace_img_by_alt(s, "Bright smile — The Skye dental clinic, Bonamoussadi Douala", hero_uri) \
    if 'alt="Bright smile — The Skye' in s else re.sub(
        r'(<img class="hero-img" src=")data:image/jpeg;base64,[^"]*(")',
        lambda m: m.group(1) + hero_uri + m.group(2), s, count=1)
s = re.sub(r'(<img[^>]*src=")data:image/jpeg;base64,[^"]*("[^>]*alt="The Skye reception, Bonamoussadi Douala")',
           lambda m: m.group(1) + team_uri + m.group(2), s, count=1)
# fallback: alt still English-literal pre-rebrand when substitution order ran; do raw mapping
s = re.sub(r'(<img[^>]*src=")data:image/jpeg;base64,[^"]*("[^>]*alt="[^"]*reception[^"]*")',
           lambda m: m.group(1) + team_uri + m.group(2), s, count=1)

# alts for the rest (global replace remaining OraCare alts)
s = s.replace('alt="Bright smile — The Skye dental clinic, Bonamoussadi Douala"',
              'alt="Sourire éclatant — Cabinet Dentaire The Skye, Bonamoussadi Douala"')
s = s.replace('alt="The Skye treatment room"', 'alt="Salle de soins — Cabinet The Skye"')
s = s.replace('alt="Smile after treatment at The Skye"', 'alt="Sourire après traitement — The Skye"')
s = s.replace('alt="Smile before treatment at The Skye"', 'alt="Sourire avant traitement — The Skye"')
s = s.replace('alt="Patient at The Skye"', 'alt="Patient du Cabinet The Skye (photo d’exemple)"')
s = s.replace('alt="Dr Sandrine Djuinne, lead dentist"', 'alt="Dre Sandrine Djuinne, chirurgien-dentiste"')
s = s.replace('alt="Dr Sandrine Djuinne"', 'alt="Dre Sandrine Djuinne"')
s = s.replace('alt="Teeth whitening at The Skye"', 'alt="Blanchiment dentaire — The Skye"')
s = s.replace('alt="Dental implant and restoration"', 'alt="Implant et restauration dentaire"')
s = s.replace('alt="Orthodontics and braces"', 'alt="Orthodontie et bagues dentaires"')
s = s.replace('alt="Dental assistant"', 'alt="Assistant(e) dentaire (photo d’exemple)"')
s = s.replace('alt="Dental hygienist"', 'alt="Hygiéniste dentaire (photo d’exemple)"')
s = s.replace('alt="Smile coach"', 'alt="Accueil et coordination (photo d’exemple)"')
s = s.replace('alt="Modern dental equipment"', 'alt="Équipement dentaire moderne"')
s = s.replace('alt="Happy patient"', 'alt="Patient satisfait (photo d’exemple)"')

# ---------- 7. <head>: title/meta/og/noindex/JSON-LD ----------
s = s.replace('<html lang="en">', '<html lang="fr">')
s = re.sub(r'<title>.*?</title>',
           '<title>Cabinet Dentaire The Skye — Bonamoussadi, Douala | Souriez à l’infini</title>', s)
s = re.sub(r'<meta name="description"[^>]*>',
           '<meta name="description" content="Cabinet dentaire moderne à Bonamoussadi, Douala (immeuble Stella & Joyce) : tarifs en FCFA, rendez-vous WhatsApp en un clic, français et anglais.">', s)
s = s.replace('<meta name="robots" content="noindex,nofollow">', '')  # avoid dup
s = s.replace('<title>', '<meta name="robots" content="noindex,nofollow">\n<title>', 1)
s = re.sub(r'<meta property="og:title"[^>]*>',
           '<meta property="og:title" content="Cabinet Dentaire The Skye — Bonamoussadi, Douala">', s)
s = re.sub(r'<meta property="og:description"[^>]*>',
           '<meta property="og:description" content="Souriez à l’infini : soins de qualité, tarifs FCFA clairs, rendez-vous WhatsApp en un clic.">', s)
s = re.sub(r'<meta property="og:url"[^>]*>', '', s)

jsonld = {
 "@context": "https://schema.org",
 "@graph": [
  {"@type": "Dentist",
   "name": "Cabinet Dentaire The Skye",
   "alternateName": "The Skye Dental Clinic",
   "slogan": "Souriez à l'infini",
   "image": "https://www.facebook.com/237DentalClinic",
   "telephone": "+237677796999",
   "email": "cabinetheskye@gmail.com",
   "priceRange": "$$",
   "address": {"@type": "PostalAddress",
     "streetAddress": "Immeuble Stella & Joyce, Petit terrain, Bonamoussadi",
     "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM"},
   "openingHoursSpecification": [
     {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "08:00", "closes": "17:00"},
     {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "14:00"}],
   "sameAs": ["https://www.facebook.com/237DentalClinic"],
   "dentist": {"@type": "Physician", "name": "Dr Sandrine Djuinne"}},
  {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "Est-ce que ça fait mal ?",
     "acceptedAnswer": {"@type": "Answer", "text": "La première visite est souvent la plus calme. Pour les soins comme les plombages, une anesthésie locale est utilisée, et chaque étape est expliquée avant de commencer."}},
    {"@type": "Question", "name": "Comment payer ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Espèces, MTN Mobile Money ou Orange Money (à confirmer). Le prix annoncé avant le soin est le prix payé, sans surprise."}},
    {"@type": "Question", "name": "Comment prendre rendez-vous ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Par WhatsApp en un clic depuis le site, ou au +237 677 79 69 99. La plupart des rendez-vous sont confirmés le jour même."}},
    {"@type": "Question", "name": "Où se trouve le cabinet ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala."}},
    {"@type": "Question", "name": "Recevez-vous les enfants ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Oui, enfants et adolescents sont reçus en douceur, à leur rythme."}}
  ]}
 ]}
s = s.replace('</head>',
  '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n</head>')

# ---------- 8. top promo/FB bar + sticky mobile RDV bar ----------
TOPBAR = '''<!-- TOP PROMO BAR -->
<div class="topbar"><div class="wrap">
  <span data-en="✨ Quality dental care in a modern setting — Bonamoussadi" data-fr="✨ Des soins dentaires de qualité dans un cadre moderne — Bonamoussadi">✨ Des soins dentaires de qualité dans un cadre moderne — Bonamoussadi</span>
  <a href="https://www.facebook.com/237DentalClinic" target="_blank" rel="noopener" data-en="Follow our promotions on Facebook ↗" data-fr="Suivre nos promotions sur Facebook ↗">Suivre nos promotions sur Facebook ↗</a>
</div></div>
<style>
.topbar{background:var(--navy);color:#EAF6FE;font-size:12.5px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 24px;flex-wrap:wrap}
.topbar a{color:#7DD3FC;font-weight:700;text-decoration:none;white-space:nowrap}
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:90;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-top:1px solid rgba(11,74,120,.14);padding:9px 12px;gap:9px;box-shadow:0 -10px 30px rgba(11,74,120,.14)}
.mbar a{min-height:52px;display:flex;align-items:center;justify-content:center;flex:1;border-radius:12px;font-weight:800;text-decoration:none;font-size:14.5px}
.mbar .m-call{flex:0 0 64px;background:#E3F3FC;color:var(--navy);border:1.5px solid rgba(11,74,120,.2)}
.mbar .m-book{background:var(--navy2);color:#fff}
:where(a,button,input,select,summary):focus-visible{outline:3px solid #38BDF8;outline-offset:2px;border-radius:6px}
@media(max-width:860px){ .mbar{display:flex} body{padding-bottom:78px} }
@media(prefers-reduced-motion:reduce){ *,*::before,*::after{animation:none!important;transition:none!important} .rv{opacity:1;transform:none} }
</style>
<div class="mbar">
  <a class="m-call" href="tel:+237677796999" aria-label="Appeler">📞</a>
  <a class="m-book" href="https://wa.me/237677796999?text=Bonjour%20The%20Skye%20!%20Je%20souhaite%20prendre%20rendez-vous." target="_blank" rel="noopener" data-en="📅 Book on WhatsApp" data-fr="📅 Prendre RDV sur WhatsApp">📅 Prendre RDV sur WhatsApp</a>
</div>
'''
s = s.replace('<body>', '<body>\n' + TOPBAR, 1)

# ---------- 9. bot JS rebrand leftovers ----------
s = s.replace('Monday to Saturday, 8:00 am to 6:00 pm — your real hours replace these at launch',
              'Monday to Friday 8:00–17:00 and Saturday 8:00–14:00 (directory hours — confirmed with you at launch)')
s = s.replace("du lundi au samedi, 8h00 à 18h00 — vos vrais horaires les remplacent au lancement",
              "du lundi au vendredi 8h–17h et le samedi 8h–14h (horaires d'annuaire — confirmés avec vous au lancement)")
s = s.replace("We're at Immeuble Stella & Joyce, Bonamoussadi, Douala — right at the hospital. A Google Maps embed goes on the final site.",
              "We're at Immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala. A Google Maps embed goes on the final site.")
s = s.replace("Nous sommes à Bonamoussadi, Petit terrain, Douala — juste à l'hôpital. Une carte Google Maps intégrée figure sur le site final.",
              "Nous sommes à l'immeuble Stella & Joyce, Petit terrain, Bonamoussadi, Douala. Une carte Google Maps intégrée figure sur le site final.")
s = s.replace('console.log("The Skye booking payload → POST /api/bookings"',
              'console.log("The Skye booking payload → POST /api/bookings"')

# default language: FR for Douala; honor ?lang= + localStorage
s = s.replace(
 "(function(){ var p = new URLSearchParams(location.search).get(\"lang\"); if(p === \"fr\" || p === \"en\"){ setLang(p); } })();",
 "(function(){ var p = new URLSearchParams(location.search).get(\"lang\"); var sv=null; try{sv=localStorage.getItem('skye-lang');}catch(e){}"
 " if(p==='fr'||p==='en'){setLang(p);} else if(sv==='fr'||sv==='en'){setLang(sv);} else { setLang('fr'); } })();")
# persist choice inside setLang
s = s.replace('function setLang(l){\n  document.documentElement.lang = l;',
              "function setLang(l){\n  document.documentElement.lang = l;\n  try{ localStorage.setItem('skye-lang', l); }catch(e){}")
# history URL line references OraCare file names if any
s = s.replace('clinic-bonaberi.html', 'index.html').replace('sample-nursery.html', 'index.html')

# map directions link
s = re.sub(r'https://www\.google\.com/maps/search/\?api=1&query=[^"\\ ]*',
           'https://www.google.com/maps/search/?api=1&query=Cabinet%20Dentaire%20The%20Skye%20Bonamoussadi%20Douala', s)

# ----- language-aware WA prefills (source JS still has English OraCare-era strings) -----
old_wire = ('document.querySelectorAll(".pcard .btn[data-wa]").forEach(function(a){\n'
 '  var s = a.getAttribute("data-wa");\n'
 '  a.href = "https://wa.me/" + OC_WA + "?text=" + encodeURIComponent("Hello The Skye! I\'d like to book: " + s + ".");\n'
 '  a.setAttribute("target","_blank"); a.setAttribute("rel","noopener");\n});')
new_wire = (
 'function waHref(en,fr){ var frOn=document.documentElement.lang==="fr";\n'
 '  return "https://wa.me/" + OC_WA + "?text=" + encodeURIComponent(frOn?fr:en); }\n'
 'function wireWa(){\n'
 '  document.querySelectorAll(".pcard .btn[data-wa]").forEach(function(a){\n'
 '    var card=a.closest(".pcard"), h=card?card.querySelector("h3"):null;\n'
 '    var en=a.getAttribute("data-wa"), fr=h?h.getAttribute("data-fr"):en;\n'
 '    a.href=waHref("Hello! I\\u2019d like to book: "+en+".", "Bonjour The Skye ! Je souhaite r\\u00e9server : "+fr+".");\n'
 '    a.setAttribute("target","_blank"); a.setAttribute("rel","noopener");\n'
 '  });\n'
 '  document.querySelectorAll(".js-genbook").forEach(function(a){\n'
 '    a.href=waHref("Hello! I\\u2019d like to book a visit.","Bonjour The Skye ! Je souhaite prendre rendez-vous.");\n'
 '    a.setAttribute("target","_blank"); a.setAttribute("rel","noopener");\n'
 '  });\n'
 '  var mb=document.getElementById("mbarBook");\n'
 '  if(mb) mb.href=waHref("Hello! I\\u2019d like to book a visit.","Bonjour The Skye ! Je souhaite prendre rendez-vous.");\n'
 '}\n'
 'document.addEventListener("DOMContentLoaded",wireWa);\n'
 'var __skyeSetLang=setLang; setLang=function(l){__skyeSetLang(l); wireWa();};')
assert old_wire in s, "wire block not found"
s = s.replace(old_wire, new_wire)

# generic static "book a visit" anchors -> js hook
s = re.sub(r'<a class="btn btn-dark" href="https://wa\.me/237677796999\?text=[^"]*book%20a%20visit[^"]*"',
           '<a class="btn btn-dark js-genbook" href="#book"', s)
# sticky bar button id
s = s.replace('<a class="m-book" href="https://wa.me/237677796999?text=Bonjour%20The%20Skye%20!%20Je%20souhaite%20prendre%20rendez-vous."',
              '<a class="m-book" id="mbarBook" href="#book"')
# formal "vous" in the unlisted-service FR deep link
s = s.replace("Bonjour%20The Skye%21%20Peux-tu%20me%20donner%20le%20prix%20pour",
              "Bonjour%20The Skye%21%20Pouvez-vous%20m%27indiquer%20le%20prix%20de")

# boot: FR-first (Douala), honor ?lang= + saved choice (must run after bot setLang override)
_init = (
 "};\n"
 "(function(){ var p=new URLSearchParams(location.search).get('lang'),sv=null;"
 "try{sv=localStorage.getItem('skye-lang');}catch(e){}"
 " if(p==='fr'||p==='en'){setLang(p);}else if(sv==='fr'||sv==='en'){setLang(sv);}else{setLang('fr');} })();\n"
 "</script>\n</body>\n</html>")
_tail = "};\n</script>\n</body>\n</html>"
assert s.rstrip("\n").endswith(_tail)
s = s.rstrip("\n")[:-len(_tail)] + (
 "};\n"
 "(function(){ var p=new URLSearchParams(location.search).get('lang'),sv=null;"
 "try{sv=localStorage.getItem('skye-lang');}catch(e){}"
 " if(p==='fr'||p==='en'){setLang(p);}else if(sv==='fr'||sv==='en'){setLang(sv);}else{setLang('fr');} })();\n"
 "</script>\n</body>\n</html>\n")

# footer wordmark lockup uses name "The Skye" + small already says CABINET DENTAIRE; fine.
# write
out = ROOT / "demos" / "concept-skye-v1.html"
out.write_text(s, encoding="utf-8")
print("wrote", out, round(out.stat().st_size/1024), "KB")
