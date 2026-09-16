# -*- coding: utf-8 -*-
"""Build demos/concept-yaks-v1.html — NAMED gift for Cabinet Dentaire YAKS.
Base: concept-oracare-v3.html (proven dental machinery), deliberately re-designed
to look like YAKS (not OraCare/Skye):
- leaf-green + teal palette sampled from their own « NOS SPÉCIALITÉS » poster/logo
- rounded family-wellness type (Nunito), pill CTAs, circular medallion tiles
- signature « specialities wheel » section (6 poster specialities + prevention +
  booking hub) replacing the photo-card work section
- tagline « La santé de vos dents, la beauté de votre sourire »
- FR-first bilingual, WA +237 672 70 20 78, Dre Lekane, Logbessou face Collège Soleil
- real proof only: 2 100+ FB likes, 100 % / 5 avis FB; consult 6,000 FCFA (mondocteur)
- mobile-first: 44px targets, language-aware WA prefills, sticky bottom booking <=860px
"""
import re, base64, io, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
s = (ROOT / "demos" / "concept-oracare-v3.html").read_text(encoding="utf-8")

# ---------- 1. palette: cream/sage/teal/gold -> YAKS leaf-green + teal + mint ----------
color_map = [
    ("#F7F1E8", "#F0FAF1"),  # cream -> ice mint
    ("#FBF7F0", "#FFFFFF"),  # cream2 -> white
    ("#EDF3EE", "#E4F6EC"),  # sage tint -> mint
    ("#7FA88F", "#1FB7C8"),  # sage deep -> YAKS teal
    ("#16323A", "#146A2C"),  # deep teal -> forest green (primary dark)
    ("#1E4152", "#0E8A99"),  # navy2 -> deep teal
    ("#1C2B33", "#15301B"),  # ink -> green-ink
    ("#5C6F78", "#5C7565"),  # slate -> green-grey
    ("#C9A24B", "#57A52A"),  # gold -> leaf green
    ("#A9842F", "#3E8E1F"),  # gold text -> deep leaf
    ("rgba(22,50,58,", "rgba(20,106,44,"),
    ("rgba(127,168,143,", "rgba(31,183,200,"),
    ("rgba(201,165,75,", "rgba(87,165,42,"),
    ("rgba(247,241,232,", "rgba(240,250,241,"),
    ("rgba(251,247,240,", "rgba(255,255,255,"),
    ("#0F172A", "#146A2C"),
    ("#7DD3FC", "#BDF3E0"),  # topbar link -> light teal
]
for a, b in color_map:
    s = s.replace(a, b)

# ---------- 2. global literals (longest first) ----------
lit = [
    ("OraCare Dental Clinic — Molyko, Buea | Gentle Care · Clear FCFA Prices",
     "Cabinet Dentaire YAKS — Logbessou, Douala | La santé de vos dents, la beauté de votre sourire"),
    ("OraCare Dental Clinic", "Cabinet Dentaire YAKS"),
    ("OraCare", "YAKS"),
    ("237672526686", "237672702078"),
    ("+237 672 52 66 86", "+237 672 70 20 78"),
    ("+237 6 72 52 66 86", "+237 6 72 70 20 78"),
    ("tel:+237672526686", "tel:+237672702078"),
    ("snkafuarnold11@gmail.com", "cabinetdentaireyaks@gmail.com"),
    ("facebook.com/p/Oracare237-100075164312902", "facebook.com/Yaksdentalclinic"),
    ("Oracare237-100075164312902", "Yaksdentalclinic"),
    ("St. Pius Hospital, Mayor's Street, Molyko, Buea",
     "Immeuble BAO, face au Collège Soleil, Logbessou, Douala"),
    ("St. Pius Hospital, Mayor's Street", "Immeuble BAO, Logbessou"),
    ("l'hôpital St. Pius, Mayor's Street", "l'immeuble BAO, Logbessou"),
    ("l'hôpital St-Pius, Molyko", "Logbessou, face au Collège Soleil"),
    ("Inside St. Pius Hospital, Molyko", "Immeuble BAO, Logbessou"),
    ("À l'hôpital St-Pius, Molyko", "Immeuble BAO, Logbessou"),
    ("Mayor's Street", "face au Collège Soleil"),
    ("Molyko, Buea", "Logbessou, Douala"),
    ("Molyko, Buéa", "Logbessou, Douala"),
    ("Molyko", "Logbessou"),
    ("Buea", "Douala"),
    ("Buéa", "Douala"),
    ("St. Pius", "BAO"),
    ("Dr. A. Nkafu", "Dre Lekane Lolita"),
    ("Dr A. Nkafu", "Dre Lekane Lolita"),
    ("DENTAL CLINIC · MOLYKO", "DENTAL CLINIC · LOGBESSOU"),
    ("CLINIQUE DENTAIRE · MOLYKO", "CABINET DENTAIRE · LOGBESSOU"),
    ("DENTAL CARE — MOLYKO, BUEA", "DENTAL CARE — LOGBESSOU, DOUALA"),
    ("SOINS DENTAIRES — MOLYKO, BUEA", "SOINS DENTAIRES — LOGBESSOU, DOUALA"),
    ("OC-", "YK-"),
    # bot hours -> directory hours, Saturday until 13:00 (to confirm)
    ("Monday to Saturday, 8:00 am to 6:00 pm — your real hours replace these at launch",
     "Monday to Friday, 8:00 am to 5:00 pm and Saturday 8:00 am to 1:00 pm (to confirm)"),
    ("du lundi au samedi, 8h00 à 18h00 — vos vrais horaires les remplacent au lancement",
     "du lundi au vendredi 8h–17h et le samedi 8h–13h (horaires à confirmer au lancement)"),
    ("OraCare booking payload", "YAKS booking payload"),
]
for a, b in lit:
    s = s.replace(a, b)

# consultation price 5,000 -> 6,000 FCFA (published on mondocteur for YAKS);
# exact-tag anchor only (never bare numeric replace)
s = s.replace('<div class="p-amt">5,000 ', '<div class="p-amt">6,000 ')

# ---------- 3. type family: Outfit -> rounded family-friendly Nunito ----------
s = s.replace(
    "family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600;700",
    "family=Nunito:wght@600;700;800;900&family=Inter:wght@400;500;600;700;800")
s = s.replace("'Outfit'", "'Nunito'").replace("Outfit,", "Nunito,").replace("Outfit", "Nunito")

# ---------- 4. all data-en / data-fr pairs, overridden by index ----------
ens = re.findall(r'data-en="([^"]*)"', s)
frs = re.findall(r'data-fr="([^"]*)"', s)
assert len(ens) == len(frs) == 155, (len(ens), len(frs))

NEW = {
 0:  ("DENTAL CLINIC · LOGBESSOU", "CABINET DENTAIRE · LOGBESSOU"),
 2:  ("Specialties", "Spécialités"),
 7:  ("DENTAL CARE — LOGBESSOU, DOUALA", "SOINS DENTAIRES — LOGBESSOU, DOUALA"),
 8:  ("Healthy teeth.", "La santé de vos dents."),
 9:  ("A beautiful smile.", "la beauté de votre sourire."),
 10: ("Gentle family dentistry at Immeuble BAO, Logbessou (facing Collège Soleil): six dental specialities, clear FCFA prices and WhatsApp booking — in French and English.",
      "Des soins dentaires doux pour toute la famille à l'immeuble BAO, Logbessou (face au Collège Soleil) : six spécialités, tarifs clairs en FCFA et rendez-vous WhatsApp, en français et en anglais."),
 12: ("See our care", "Découvrir nos soins"),
 13: ("Immeuble BAO, facing Collège Soleil", "Immeuble BAO, face au Collège Soleil"),
 15: ("💬 Prefer to chat? Our 24/7 assistant answers in French and English",
      "💬 Une question ? Notre assistant 24h/7 répond en français et en anglais"),
 18: ("Many patients hesitate to ask about prices. So we show them in plain FCFA. The consultation is 6,000 FCFA; the other tariffs shown are examples — your real price list replaces them in 24 hours.",
      "Beaucoup de patients hésitent à demander le prix. Nous l'affichons donc en FCFA, clairement. La consultation est à 6 000 FCFA ; les autres tarifs affichés sont des exemples — votre vraie grille les remplace en 24 h."),
 19: ("Concept prices — your real price list goes here in 24h.",
      "Tarifs de concept — votre vraie grille tarifaire est ajoutée en 24 h."),
 21: ("Consultation", "Consultation"),
 27: ("Scaling & cleaning", "Détartrage"),
 30: ("Ultrasonic scaling", "Détartrage aux ultrasons"),
 33: ("Filling (obturation)", "Obturation (plombage)"),
 36: ("Caries treatment", "Soin des caries"),
 39: ("Teeth whitening", "Blanchiment dentaire"),
 42: ("Professional whitening gel", "Gel de blanchiment professionnel"),
 46: ("Specialties", "Spécialités"),
 47: ("Six specialities, one healthy smile", "Six spécialités, un sourire en santé"),
 48: ("Preventive care, scaling, fillings, root canals, prosthetics and whitening — the complete range for the whole family.",
      "Soins préventifs, détartrage, plombages, dévitalisations, prothèses et blanchiment : la gamme complète pour toute la famille."),
 49: ("FOLLOW YAKS ON FACEBOOK ↗", "SUIVRE YAKS SUR FACEBOOK ↗"),
 57: ("Nervous? That's normal — we take the time to explain.",
      "Nerveux ? C'est normal — nous prenons le temps de tout expliquer."),
 60: ("Sterile, for every patient", "Stérile, pour chaque patient"),
 62: ("Every smile is welcome", "Chaque sourire est le bienvenu"),
 63: ("Children, parents and grandparents — the whole family is treated here, without judgment.",
      "Enfants, parents et grands-parents : toute la famille est soignée ici, sans jugement."),
 66: ("Skilled. Gentle. For the whole family.", "Compétente. Douce. Pour toute la famille."),
 67: ("Our team makes every visit comfortable for young and old — from your first WhatsApp message to the follow-up, the same people follow your smile.",
      "Notre équipe rend chaque visite agréable, petits et grands — de votre premier message WhatsApp au contrôle de suivi, les mêmes personnes suivent votre sourire."),
 69: ("Dr Lekane Lolita Ntoweng — Dental Surgeon", "Dre Lekane épse Ntoweng Lolita — Chirurgien-dentiste"),
 70: ("Preventive · Restorative · Prosthetics", "Parodontie · Restauration · Prothèse"),
 72: ("Inside YAKS, Logbessou", "Au Cabinet YAKS, Logbessou"),
 73: ("Easy to find at Immeuble BAO, facing Collège Soleil — Logbessou.",
      "Facile à trouver : immeuble BAO, face au Collège Soleil — Logbessou."),
 81: ("Immeuble BAO, facing Collège Soleil, Logbessou, Douala — we'll see you at reception.",
      "Immeuble BAO, face au Collège Soleil, Logbessou, Douala — nous vous attendons à la réception."),
 87: ("Whitening result shown. Every smile is different — your assessment sets the plan.",
      "Résultat de blanchiment. Chaque sourire est différent — votre bilan définit le plan."),
 89: ("“I was afraid of the dentist for years. Dr Lekane explained every step before starting — and it was painless. Now my whole family comes.”",
      "« J'avais peur du dentiste depuis des années. Dre Lekane a expliqué chaque étape avant de commencer — et c'était indolore. Aujourd'hui, toute ma famille vient. »"),
 90: ("— Happy patient (sample review)", "— Patient satisfait (avis d'exemple)"),
 91: ("<b>100% recommended · 5 reviews</b> on our Facebook page — <a style='color:#0E8A99;font-weight:800' href='https://www.facebook.com/Yaksdentalclinic/reviews/' target='_blank' rel='noopener'>read every review ↗</a>",
      "<b>100 % de recommandations · 5 avis</b> sur notre page Facebook — <a style='color:#0E8A99;font-weight:800' href='https://www.facebook.com/Yaksdentalclinic/reviews/' target='_blank' rel='noopener'>lire tous les avis ↗</a>"),
 97: ("Cash for now; Mobile Money is being confirmed. The price quoted before treatment is the price you pay — no surprises at the end.",
      "Espèces pour le moment ; le Mobile Money est en cours de confirmation. Le prix annoncé avant le soin est le prix payé — sans surprise à la fin."),
 103:("Immeuble BAO, facing Collège Soleil, Logbessou, Douala. Tap Get Directions above and we'll see you at reception.",
      "Immeuble BAO, face au Collège Soleil, Logbessou, Douala. Utilisez le bouton Itinéraire ci-dessus et nous vous attendons à la réception."),
 118:("Consultation", "Consultation"),
 119:("Scaling & cleaning", "Détartrage"),
 120:("Filling", "Obturation"),
 121:("Whitening", "Blanchiment"),
 122:("Prosthetics / dentures", "Prothèse / dentier"),
 123:("Root canal (devitalization)", "Dévitalisation"),
 136:("DENTAL CLINIC · LOGBESSOU", "CABINET DENTAIRE · LOGBESSOU"),
 137:("Gentle family dental care in Logbessou, Douala — six specialities, clear FCFA prices, French & English, appointments on WhatsApp.",
       "Des soins dentaires doux pour toute la famille à Logbessou, Douala — six spécialités, tarifs FCFA clairs, français et anglais, rendez-vous sur WhatsApp."),
 140:("Mon–Fri 8:00–17:00 · Sat 8:00–13:00 (to confirm)",
       "Lun–Ven 8h–17h · Sam 8h–13h (à confirmer)"),
 149:("© 2026 Cabinet Dentaire YAKS · Logbessou, Douala",
       "© 2026 Cabinet Dentaire YAKS · Logbessou, Douala"),
 152:("YAKS Assistant", "Assistant YAKS"),
}

def pair_repl(m, counter=[0]):
    i = counter[0]; counter[0] += 1
    en, fr = NEW.get(i, (m.group(2), m.group(3)))
    return f'{m.group(1)}data-en="{en}" data-fr="{fr}"{m.group(4)}>'

s = re.sub(r'(<[^>]*?)data-en="([^"]*)" data-fr="([^"]*)"([^>]*?)>', pair_repl, s)

# ---------- 5. hero chips: real proof ----------
s = s.replace(
 '📍 <span data-en="Immeuble BAO, facing Collège Soleil" data-fr="Immeuble BAO, face au Collège Soleil">',
 '⭐ <span data-en="100% recommended · 5 Facebook reviews" data-fr="100 % recommandent · 5 avis Facebook">')
s = s.replace('<span class="chip">🗣 EN | FR</span>',
              '<span class="chip">📍 <span data-en="Immeuble BAO, facing Collège Soleil" data-fr="Immeuble BAO, face au Collège Soleil">Immeuble BAO, face au Collège Soleil</span></span>')
s = s.replace('<span class="more">You?</span>', '<span class="more">2 100 ❤</span>')
s = s.replace('title="Concept placeholder — real patient photos are added only with permission at launch"',
              'title="Plus de 2 100 mentions J’aime sur Facebook — vos vraies photos patients remplacent ces images au lancement"')
# hero h1: drop stray tooth emoji between the two lines
s = s.replace('</span> 🦷<br>', '</span><br>')

# ---------- 6. logo mark: gradient green->teal tooth in a white tile ----------
s = s.replace(
 '<span class="tooth">🦷</span>',
 '<span class="tooth"><svg viewBox="0 0 28 28" width="22" height="22" aria-hidden="true">'
 '<defs><linearGradient id="yg" x1="0" y1="0" x2="1" y2="1">'
 '<stop offset="0" stop-color="#57A52A"/><stop offset="1" stop-color="#1FB7C8"/></linearGradient></defs>'
 '<path fill="url(#yg)" d="M14 3.5c-2.6 0-3.9-1-6-1-2.6 0-4 2-4 4.6 0 4.6 1.3 7.2 2 10.3.5 2.3.7 6.1 2.7 6.1 1.9 0 1.7-4.6 2.6-6 .7-1.2 1.4-1.6 2.7-1.6s2 .4 2.7 1.6c.9 1.4.7 6 2.6 6 2 0 2.2-3.8 2.7-6.1.7-3.1 2-5.7 2-10.3 0-2.6-1.4-4.6-4-4.6-2.1 0-3.4 1-6 1z"/>'
 '<path d="M8.5 12.5c2.4 3.1 8.6 3.1 11 0" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/>'
 '</svg></span>')

# ---------- 7. signature section: specialities wheel (replaces 002 WORK photo cards) ----------
def tile(cls, sp, tint, emoji, en, fr, desc_en, desc_fr):
    return (f'<div class="sp-card rv {cls}" style="--sp:{sp};--sptint:{tint}">'
            f'<div class="sp-ic">{emoji}</div>'
            f'<h3 data-en="{en}" data-fr="{fr}">{fr}</h3>'
            f'<p data-en="{desc_en}" data-fr="{desc_fr}">{desc_fr}</p></div>')

TILES = [
 ("sp-a", "#C2185B", "#FCE7F0", "🦷", "Tooth extraction", "Extraction",
  "Quick, gentle and numbed", "Rapide, douce et sous anesthésie"),
 ("sp-b", "#1FB7C8", "#E1F7FA", "🪥", "Professional scaling", "Détartrage",
  "Remove tartar, protect your gums", "Élimine le tartre, protège les gencives"),
 ("sp-c", "#27A9D9", "#E3F4FC", "✨", "Teeth whitening", "Blanchiment dentaire",
  "A brighter smile in one session", "Un sourire plus éclatant en une séance"),
 ("sp-d", "#F0781E", "#FEEADB", "🩺", "Root canal treatment", "Dévitalisation",
  "Save a damaged tooth", "Sauver une dent abîmée"),
 ("sp-e", "#1FB7C8", "#E1F7FA", "🧩", "Fillings (obturations)", "Obturations (plomb)",
  "Tooth-coloured composites", "Composites de la couleur des dents"),
 ("sp-f", "#F5A623", "#FEF3DC", "😁", "Dentures & prosthetics", "Prothèse",
  "Replace and rebuild your smile", "Remplacer et reconstruire le sourire"),
 ("sp-g", "#57A52A", "#E7F5DC", "🧒", "Preventive & family care", "Prévention & famille",
  "Children and adults, check-ups", "Enfants et adultes, bilans réguliers"),
]
cells = ""
area_map = ["sp-a", "sp-b", "sp-c", "sp-d", None, "sp-e", "sp-f", "sp-g", "sp-h"]
built = {}
for (cls, sp, tint, emoji, en, fr, den, dfr) in TILES:
    built[cls] = tile(cls, sp, tint, emoji, en, fr, den, dfr)
cta = ('<a class="sp-card sp-h rv" href="#book" id="wheelCta">'
       '<div class="sp-ic">📅</div>'
       '<h3 data-en="Book on WhatsApp" data-fr="Prendre RDV sur WhatsApp">Prendre RDV sur WhatsApp</h3>'
       '<p data-en="One tap, no waiting on the line" data-fr="Un clic, sans attente au téléphone">'
       'Un clic, sans attente au téléphone</p></a>')
built["sp-h"] = cta
# mobile order: hub first, then a,b,c,e,f,d,g,cta
mobile_order = ["sp-a", "sp-b", "sp-c", "sp-e", "sp-f", "sp-d", "sp-g", "sp-h"]
hub = ('<div class="sp-hub rv" id="spHub">'
       '<span class="sp-hub-tooth"><svg viewBox="0 0 28 28" width="40" height="40" aria-hidden="true">'
       '<path fill="#fff" d="M14 3.5c-2.6 0-3.9-1-6-1-2.6 0-4 2-4 4.6 0 4.6 1.3 7.2 2 10.3.5 2.3.7 6.1 2.7 6.1 1.9 0 1.7-4.6 2.6-6 .7-1.2 1.4-1.6 2.7-1.6s2 .4 2.7 1.6c.9 1.4.7 6 2.6 6 2 0 2.2-3.8 2.7-6.1.7-3.1 2-5.7 2-10.3 0-2.6-1.4-4.6-4-4.6-2.1 0-3.4 1-6 1z"/>'
       '<path d="M8.5 12.5c2.4 3.1 8.6 3.1 11 0" fill="none" stroke="#1FB7C8" stroke-width="1.7" stroke-linecap="round"/></svg></span>'
       '<div><div class="sp-hub-name">CABINET DENTAIRE YAKS</div>'
       '<div class="sp-hub-tag" data-en="Healthy teeth, beautiful smiles for the whole family" '
       'data-fr="La santé de vos dents, la beauté de votre sourire — pour toute la famille">'
       'La santé de vos dents, la beauté de votre sourire — pour toute la famille</div></div></div>')
grid = '<div class="sp-grid">' + hub + "".join(built[k] for k in mobile_order) + '</div>'
WHEEL = ('<!-- 002 SPECIALTIES WHEEL (YAKS signature, from their poster) -->\n'
 '<section class="work spec" id="work">\n  <div class="wrap">\n'
 '    <div class="work-head rv">\n'
 '      <div class="eyebrow"><b>002</b><span data-en="Our specialities" data-fr="Nos spécialités">Nos spécialités</span></div>\n'
 '      <div class="work-head-r">\n'
 '        <h2 data-en="Six specialities, one healthy smile" data-fr="Six spécialités, un sourire en santé">Six spécialités, un sourire en santé</h2>\n'
 '        <div class="work-meta">\n'
 '          <p data-en="Preventive care, scaling, fillings, root canals, prosthetics and whitening — the complete range for the whole family." data-fr="Soins préventifs, détartrage, plombages, dévitalisations, prothèses et blanchiment : la gamme complète pour toute la famille.">Soins préventifs, détartrage, plombages, dévitalisations, prothèses et blanchiment : la gamme complète pour toute la famille.</p>\n'
 '          <a class="badge-round" href="https://www.facebook.com/Yaksdentalclinic" target="_blank" rel="noopener" data-en="FOLLOW YAKS ON FACEBOOK ↗" data-fr="SUIVRE YAKS SUR FACEBOOK ↗">SUIVRE YAKS SUR FACEBOOK ↗</a>\n'
 '        </div>\n      </div>\n    </div>\n'
 + grid + '\n  </div>\n</section>')
s, n = re.subn(r'<!-- 002 WORK -->.*?</section>', lambda m: WHEEL, s, count=1, flags=re.S)
assert n == 1, "002 WORK section not replaced"

# ---------- 8. images ----------
def b64_jpg(path, width, quality):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.read()).decode()

hero_uri = b64_jpg(ROOT / "demos" / "img" / "yaks-hero.jpg", 860, 80)
care_uri = b64_jpg(ROOT / "demos" / "img" / "yaks-care.jpg", 760, 80)
s = re.sub(r'(<img class="hero-img" src=")data:image/jpeg;base64,[^"]*(")',
           lambda m: m.group(1) + hero_uri + m.group(2), s, count=1)
s = re.sub(r'(<img[^>]*src=")data:image/jpeg;base64,[^"]*("[^>]*alt="[^"]*reception[^"]*")',
           lambda m: m.group(1) + care_uri + m.group(2), s, count=1)
# alt cleanups (remaining stock shots stay clearly labelled as examples)
alt_rep = [
    ("Bright smile — YAKS dental clinic, Logbessou Douala", "Sourire éclatant — Cabinet Dentaire YAKS, Logbessou Douala"),
    ("YAKS treatment room", "Salle de soins — Cabinet YAKS"),
    ("Smile after treatment at YAKS", "Sourire après traitement — YAKS"),
    ("Smile before treatment at YAKS", "Sourire avant traitement — YAKS"),
    ("Patient at YAKS", "Patient du Cabinet YAKS (photo d'exemple)"),
    ("Dr Lekane Lolita, lead dentist", "Dre Lekane Lolita, chirurgien-dentiste"),
    ("Dr Lekane Lolita", "Dre Lekane Lolita"),
    ("Teeth whitening at YAKS", "Blanchiment dentaire — YAKS"),
    ("Dental implant and restoration", "Prothèse et restauration dentaire"),
    ("Orthodontics and braces", "Soins dentaires en famille"),
    ("Dental assistant", "Assistant(e) dentaire (photo d'exemple)"),
    ("Dental hygienist", "Hygiéniste dentaire (photo d'exemple)"),
    ("Smile coach", "Accueil et coordination (photo d'exemple)"),
    ("Modern dental equipment", "Équipement dentaire moderne"),
    ("Happy patient", "Patient satisfait (photo d'exemple)"),
    ("YAKS reception, Logbessou Douala", "Accueil et salle de soins — Cabinet YAKS, Logbessou Douala"),
    ("Dre Lekane Lolita, lead dentist", "Dre Lekane Lolita, chirurgien-dentiste"),
]
for a, b in alt_rep:
    s = s.replace(f'alt="{a}"', f'alt="{b}"')

# ---------- 9. head: title/meta/noindex/JSON-LD ----------
s = s.replace('<html lang="en">', '<html lang="fr">')
s = re.sub(r'<title>.*?</title>',
  '<title>Cabinet Dentaire YAKS — Logbessou, Douala | La santé de vos dents, la beauté de votre sourire</title>', s)
s = re.sub(r'<meta name="description"[^>]*>',
  '<meta name="description" content="Cabinet dentaire familial à Logbessou, Douala (immeuble BAO, face au Collège Soleil) : six spécialités, consultation à 6 000 FCFA, rendez-vous WhatsApp en un clic, français et anglais.">', s)
s = s.replace('<meta name="robots" content="noindex,nofollow">', '')
s = s.replace('<title>', '<meta name="robots" content="noindex,nofollow">\n<title>', 1)
s = re.sub(r'<meta property="og:title"[^>]*>',
  '<meta property="og:title" content="Cabinet Dentaire YAKS — Logbessou, Douala">', s)
s = re.sub(r'<meta property="og:description"[^>]*>',
  '<meta property="og:description" content="Six spécialités pour toute la famille, tarifs FCFA clairs, rendez-vous WhatsApp en un clic.">', s)
s = re.sub(r'<meta property="og:url"[^>]*>', '', s)

jsonld = {
 "@context": "https://schema.org",
 "@graph": [
  {"@type": "Dentist",
   "name": "Cabinet Dentaire YAKS",
   "alternateName": "YAKS Dental Clinic",
   "slogan": "La santé de vos dents, la beauté de votre sourire",
   "telephone": "+237672702078",
   "email": "cabinetdentaireyaks@gmail.com",
   "priceRange": "$$",
   "address": {"@type": "PostalAddress",
     "streetAddress": "Immeuble BAO, face au Collège Soleil, Logbessou",
     "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM",
     "postalCode": "BP 1925"},
   "geo": {"@type": "GeoCoordinates", "latitude": 4.0795032, "longitude": 9.7884993},
   "openingHoursSpecification": [
     {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "08:00", "closes": "17:00"},
     {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00"}],
   "sameAs": ["https://www.facebook.com/Yaksdentalclinic"],
   "dentist": {"@type": "Physician", "name": "Dr Lekane épse Ntoweng Lolita"}},
  {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "Est-ce que ça fait mal ?",
     "acceptedAnswer": {"@type": "Answer", "text": "La première visite est souvent la plus calme. Pour les plombages et extractions, une anesthésie locale est utilisée et chaque étape est expliquée avant de commencer."}},
    {"@type": "Question", "name": "Combien coûte la consultation ?",
     "acceptedAnswer": {"@type": "Answer", "text": "La consultation est à 6 000 FCFA (tarif publié sur Mondocteur). Les autres tarifs sont communiqués avant chaque soin, sans surprise."}},
    {"@type": "Question", "name": "Comment prendre rendez-vous ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Par WhatsApp en un clic depuis le site, ou au +237 6 72 70 20 78. La plupart des rendez-vous sont confirmés le jour même."}},
    {"@type": "Question", "name": "Où se trouve le cabinet ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Immeuble BAO, face au Collège Soleil, Logbessou, Douala. Ouvert 6j/7 (horaires à confirmer)."}},
    {"@type": "Question", "name": "Recevez-vous les enfants ?",
     "acceptedAnswer": {"@type": "Answer", "text": "Oui — le cabinet offre une gamme complète de soins pour toute la famille, enfants et adultes, en douceur et sans jugement."}}
  ]}
 ]}
s = s.replace('</head>',
  '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + '</script>\n</head>')

# ---------- 10. top promo/FB bar + sticky mobile RDV bar ----------
TOPBAR = '''<!-- TOP PROMO BAR + STICKY MOBILE BOOKING (YAKS) -->
<div class="topbar"><div class="wrap">
  <span data-en="✨ Six dental specialities for the whole family — Logbessou, facing Collège Soleil" data-fr="✨ Six spécialités dentaires pour toute la famille — Logbessou, face au Collège Soleil">✨ Six spécialités dentaires pour toute la famille — Logbessou, face au Collège Soleil</span>
  <a href="https://www.facebook.com/Yaksdentalclinic" target="_blank" rel="noopener" data-en="Follow us on Facebook ↗" data-fr="Suivez nos actus sur Facebook ↗">Suivez nos actus sur Facebook ↗</a>
</div></div>
<style>
.topbar{background:var(--navy);color:#EAF8EF;font-size:12.5px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:8px 24px;flex-wrap:wrap}
.topbar a{color:#BDF3E0;font-weight:700;text-decoration:none;white-space:nowrap}
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:90;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-top:1px solid rgba(20,106,44,.16);padding:9px 12px;gap:9px;box-shadow:0 -10px 30px rgba(20,106,44,.14)}
.mbar a{min-height:52px;display:flex;align-items:center;justify-content:center;flex:1;border-radius:14px;font-weight:800;text-decoration:none;font-size:14.5px}
.mbar .m-call{flex:0 0 64px;background:#E4F6EC;color:var(--navy);border:1.5px solid rgba(20,106,44,.22)}
.mbar .m-book{background:linear-gradient(135deg,#3E9B2E,#1FB7C8);color:#fff}
:where(a,button,input,select,summary):focus-visible{outline:3px solid #1FB7C8;outline-offset:2px;border-radius:6px}
@media(max-width:860px){ .mbar{display:flex} body{padding-bottom:78px} }
</style>
<div class="mbar">
  <a class="m-call" href="tel:+237672702078" aria-label="Appeler">📞</a>
  <a class="m-book" id="mbarBook" href="#book" target="_blank" rel="noopener" data-en="📅 Book on WhatsApp" data-fr="📅 Prendre RDV sur WhatsApp">📅 Prendre RDV sur WhatsApp</a>
</div>
'''
s = s.replace('<body>', '<body>\n' + TOPBAR, 1)

# ---------- 11. YAKS design layer (mobile-first, distinct from OraCare/Skye) ----------
DESIGN = '''<style>
/* ===== YAKS named-gift design layer — family wellness, mobile-first ===== */
h1,h2,h3,.logo{font-family:'Nunito',sans-serif}
h1{letter-spacing:-.02em;line-height:1.05}
.hero h1{font-size:clamp(32px,6.4vw,58px)}
.hero h1 span:first-child{color:var(--navy)}
.hero h1 span:last-child{color:#0E8A99}
.btn{border-radius:999px}
.btn-dark{background:linear-gradient(135deg,#3E9B2E 0%,#1FB7C8 100%);border:0;box-shadow:0 12px 26px rgba(31,183,200,.28)}
.btn-dark:hover{filter:brightness(1.05)}
.btn-outline{border-radius:999px;border-color:var(--navy)}
.eyebrow b{color:#0E8A99}
.chip{background:#E4F6EC;border-radius:999px}
.hero{overflow:hidden;isolation:isolate}
.hero .wrap{position:relative;z-index:2}
.hero::before{content:"";position:absolute;width:420px;height:420px;border:2px dashed rgba(31,183,200,.32);border-radius:50%;right:-150px;top:-130px;z-index:0}
.hero::after{content:"";position:absolute;width:340px;height:340px;border:2px dashed rgba(87,165,42,.30);border-radius:50%;left:-150px;bottom:-150px;z-index:0}
.hero-img{border-radius:34px;border:7px solid #fff;box-shadow:0 32px 60px rgba(20,106,44,.18)}
.pcard{border-radius:26px;border:0;box-shadow:0 14px 40px rgba(20,106,44,.08);background:linear-gradient(180deg,#fff,#F3FBF5)}
.p-ic{border-radius:50%;background:linear-gradient(135deg,#E4F6EC,#DDF7F1);color:#0E8A99}
.p-amt{color:var(--navy);font-family:'Nunito',sans-serif}
.logo .tooth{background:#fff;box-shadow:inset 0 0 0 2px #57A52A}
/* specialities wheel */
.spec{background:linear-gradient(180deg,#F0FAF1 0%,#ffffff 70%);position:relative;overflow:hidden;isolation:isolate}
.spec::before{content:"";position:absolute;width:620px;height:620px;border:2px dashed rgba(31,183,200,.18);border-radius:50%;left:50%;top:54%;transform:translate(-50%,-50%);pointer-events:none;z-index:-1}
.sp-grid{position:relative;z-index:1;display:grid;grid-template-columns:repeat(2,1fr);gap:13px;margin-top:34px}
.sp-card{background:#fff;border:1px solid rgba(20,106,44,.07);border-radius:22px;padding:20px 12px;text-align:center;text-decoration:none;box-shadow:0 10px 30px rgba(20,106,44,.07);display:flex;flex-direction:column;align-items:center;transition:transform .2s,box-shadow .2s}
.sp-card:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(20,106,44,.13)}
.sp-ic{width:68px;height:68px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;background:var(--sptint);box-shadow:inset 0 0 0 2px var(--sp);margin-bottom:10px;flex:0 0 auto}
.sp-card h3{font-size:15px;font-weight:800;color:var(--navy);line-height:1.2}
.sp-card p{font-size:12px;color:var(--slate);margin-top:6px;line-height:1.35}
.sp-hub{grid-column:1/-1;display:flex;gap:16px;align-items:center;background:linear-gradient(135deg,#146A2C,#0E8A99);color:#fff;border-radius:26px;padding:20px 22px}
.sp-hub-tooth{flex:0 0 auto;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center}
.sp-hub-name{font-family:'Nunito',sans-serif;font-weight:900;letter-spacing:.12em;font-size:15px}
.sp-hub-tag{font-size:13px;opacity:.92;margin-top:4px;line-height:1.4}
a.sp-h{background:linear-gradient(135deg,#3E9B2E,#1FB7C8);border:0;color:#fff;justify-content:center}
a.sp-h h3,a.sp-h p{color:#fff}
a.sp-h .sp-ic{background:rgba(255,255,255,.2);box-shadow:inset 0 0 0 2px rgba(255,255,255,.7)}
.badge-round{border-radius:999px}
@media(min-width:600px){ .sp-grid{grid-template-columns:repeat(3,1fr);gap:18px} }
@media(min-width:980px){
  .sp-grid{grid-template-columns:repeat(3,1fr);grid-template-areas:"a b c" "d hub e" "f g h";align-items:stretch}
  .sp-a{grid-area:a}.sp-b{grid-area:b}.sp-c{grid-area:c}.sp-d{grid-area:d}
  .sp-hub{grid-area:hub;flex-direction:column;text-align:center;justify-content:center;border-radius:50%;aspect-ratio:1/1;padding:24px}
  .sp-e{grid-area:e}.sp-f{grid-area:f}.sp-g{grid-area:g}.sp-h{grid-area:h}
}
@media(max-width:420px){ .sp-ic{width:60px;height:60px;font-size:26px} .sp-card{padding:16px 10px} .sp-card h3{font-size:13.5px} .sp-card p{display:none} }
@media(prefers-reduced-motion:reduce){ .sp-card{transition:none} }
</style>
</head>'''
s = s.replace('</head>', DESIGN, 1)

# ---------- 12. language boot: FR-first, localStorage 'yaks-lang' ----------
s = s.replace(
 "(function(){ var p = new URLSearchParams(location.search).get(\"lang\"); if(p === \"fr\" || p === \"en\"){ setLang(p); } })();",
 "(function(){ var p = new URLSearchParams(location.search).get(\"lang\"); var sv=null; try{sv=localStorage.getItem('yaks-lang');}catch(e){}"
 " if(p==='fr'||p==='en'){setLang(p);} else if(sv==='fr'||sv==='en'){setLang(sv);} else { setLang('fr'); } })();")
s = s.replace('function setLang(l){\n  document.documentElement.lang = l;',
              "function setLang(l){\n  document.documentElement.lang = l;\n  try{ localStorage.setItem('yaks-lang', l); }catch(e){}")
s = s.replace('clinic-bonaberi.html', 'index.html').replace('sample-nursery.html', 'index.html')

# map directions
s = re.sub(r'https://www\.google\.com/maps/search/\?api=1&query=[^"\\ ]*',
           'https://www.google.com/maps/search/?api=1&query=Cabinet%20Dentaire%20YAKS%20Logbessou%20Douala', s)

# ---------- 13. language-aware WA prefills ----------
old_wire = ('document.querySelectorAll(".pcard .btn[data-wa]").forEach(function(a){\n'
 '  var s = a.getAttribute("data-wa");\n'
 '  a.href = "https://wa.me/" + OC_WA + "?text=" + encodeURIComponent("Hello YAKS! I\'d like to book: " + s + ".");\n'
 '  a.setAttribute("target","_blank"); a.setAttribute("rel","noopener");\n});')
new_wire = (
 'function waHref(en,fr){ var frOn=document.documentElement.lang==="fr";\n'
 '  return "https://wa.me/" + OC_WA + "?text=" + encodeURIComponent(frOn?fr:en); }\n'
 'function wireWa(){\n'
 '  document.querySelectorAll(".pcard .btn[data-wa]").forEach(function(a){\n'
 '    var card=a.closest(".pcard"), h=card?card.querySelector("h3"):null;\n'
 '    var en=a.getAttribute("data-wa"), fr=h?h.getAttribute("data-fr"):en;\n'
 '    a.href=waHref("Hello! I\\u2019d like to book: "+en+".", "Bonjour YAKS ! Je souhaite r\\u00e9server : "+fr+".");\n'
 '    a.setAttribute("target","_blank"); a.setAttribute("rel","noopener");\n'
 '  });\n'
 '  document.querySelectorAll(".js-genbook").forEach(function(a){\n'
 '    a.href=waHref("Hello! I\\u2019d like to book a visit.","Bonjour YAKS ! Je souhaite prendre rendez-vous.");\n'
 '    a.setAttribute("target","_blank"); a.setAttribute("rel","noopener");\n'
 '  });\n'
 '  var mb=document.getElementById("mbarBook");\n'
 '  if(mb) mb.href=waHref("Hello! I\\u2019d like to book a visit.","Bonjour YAKS ! Je souhaite prendre rendez-vous.");\n'
 '}\n'
 'document.addEventListener("DOMContentLoaded",wireWa);\n'
 'var __yaksSetLang=setLang; setLang=function(l){__yaksSetLang(l); wireWa();};')
assert old_wire in s, "wire block not found"
s = s.replace(old_wire, new_wire)

# generic static book anchors -> js hook
s = re.sub(r'<a class="btn btn-dark" href="https://wa\.me/237672702078\?text=[^"]*book%20a%20visit[^"]*"',
           '<a class="btn btn-dark js-genbook" href="#book"', s)
# formal "vous" in unlisted-service FR deep link
s = s.replace("Bonjour%20YAKS%21%20Peux-tu%20me%20donner%20le%20prix%20pour",
              "Bonjour%20YAKS%20!%20Pouvez-vous%20m%27indiquer%20le%20prix%20de")

# boot tail: FR-first
_tail = "};\n</script>\n</body>\n</html>"
assert s.rstrip("\n").endswith(_tail)
s = s.rstrip("\n")[:-len(_tail)] + (
 "};\n"
 "(function(){ var p=new URLSearchParams(location.search).get('lang'),sv=null;"
 "try{sv=localStorage.getItem('yaks-lang');}catch(e){}"
 " if(p==='fr'||p==='en'){setLang(p);}else if(sv==='fr'||sv==='en'){setLang(sv);}else{setLang('fr');} })();\n"
 "</script>\n</body>\n</html>\n")

out = ROOT / "demos" / "concept-yaks-v1.html"
out.write_text(s, encoding="utf-8")
print("wrote", out, round(out.stat().st_size / 1024), "KB")
