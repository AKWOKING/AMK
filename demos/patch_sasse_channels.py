# -*- coding: utf-8 -*-
"""Minimal functional patch to King's canonical demos/sjc-sasse-v2.html (14 Sep):
- form routes to email (677 195 500 verified NOT on WhatsApp)
- footer/contact gain landline + email + TikTok
- agency chip dead # -> #top ; reduced-motion block
"""
f = 'demos/sjc-sasse-v2.html'
h = open(f, encoding='utf-8').read()

def rep(old, new, label):
    global h
    c = h.count(old)
    assert c == 1, f"anchor count {c} for: {label}"
    h = h.replace(old, new, 1)

rep('</style>',
"""@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
</style>""", 'reduced motion')

rep('<a class="concept-chip" href="#">Website concept by <b>AMK</b></a>',
    '<a class="concept-chip" href="#top">Website concept by <b>AMK</b></a>', 'chip')

rep('<p class="fc-sub" data-en="Sent on WhatsApp — 60 seconds, no email needed." data-fr="Envoyé sur WhatsApp — 60 secondes, pas d\'e-mail nécessaire.">Sent on WhatsApp — 60 seconds, no email needed.</p>',
    '<p class="fc-sub" data-en="Sent by email: 60 seconds, your mail app opens already filled." data-fr="Envoyé par e-mail : 60 secondes, votre messagerie s’ouvre déjà remplie.">Sent by email: 60 seconds, your mail app opens already filled.</p>',
    'fc-sub')

rep('<div class="fld"><label data-en="Phone (WhatsApp) *" data-fr="Téléphone (WhatsApp) *">Phone (WhatsApp) *</label>',
    '<div class="fld"><label data-en="Your phone *" data-fr="Votre téléphone *">Your phone *</label>',
    'phone label')

rep('<p class="form-small" data-en="Routes to the college\'s WhatsApp number — activate WhatsApp Business and this button becomes your admissions inbox on day one." data-fr="Dirigé vers le numéro WhatsApp du collège — activez WhatsApp Business et ce bouton devient votre boîte d\'admissions dès le premier jour.">Routes to the college\'s WhatsApp number — activate WhatsApp Business and this button becomes your admissions inbox on day one.</p>',
    '<p class="form-small" data-en="Opens an email to sajoscol@gmail.com with your message ready. Admissions also answers calls on 677 195 500 (that mobile is not on WhatsApp); landline 233 322 113." data-fr="Ouvre un e-mail à sajoscol@gmail.com avec votre message prêt. Les admissions répondent aussi au 677 195 500 (ce mobile n’est pas sur WhatsApp) ; ligne fixe 233 322 113.">Opens an email to sajoscol@gmail.com with your message ready. Admissions also answers calls on 677 195 500 (that mobile is not on WhatsApp); landline 233 322 113.</p>',
    'form-small')

rep('<!-- DEMO: routes to the college\'s number. Activate a WhatsApp Business number and this becomes a live admissions inbox -->',
    '<!-- Admissions enquiries route to college email (mobile 677 195 500 is calls-only, King-verified) -->',
    'form comment')

rep("""<p><a href="tel:+237677195500">+237 677 195 500</a></p>
        <div class="map-ph\"""",
"""<p><a href="tel:+237677195500">+237 677 195 500</a> <span data-en="(mobile, calls)" data-fr="(mobile, appels)">(mobile, calls)</span></p>
        <p><a href="tel:+237233322113">+237 233 322 113</a> <span data-en="(landline)" data-fr="(ligne fixe)">(landline)</span></p>
        <p><a href="mailto:sajoscol@gmail.com">sajoscol@gmail.com</a></p>
        <p><a href="https://www.tiktok.com/@saintjosephcollegesasse" target="_blank" rel="noopener">TikTok · SJC – The Republic</a></p>
        <div class="map-ph\"""",
    'footer contacts')

rep('<p data-en="Admissions office — 677 195 500" data-fr="Bureau des admissions — 677 195 500">Admissions office — 677 195 500</p>',
    """<p data-en="Admissions office — 677 195 500" data-fr="Bureau des admissions — 677 195 500">Admissions office — 677 195 500</p>
        <p><a href="mailto:sajoscol@gmail.com">sajoscol@gmail.com</a></p>""",
    'contact col email')

rep('''var WA_NUM = "237677195500"; // the college's number (activate WhatsApp Business to make the form live)
function setLang(l){''',
'''var COLLEGE_EMAIL = "sajoscol@gmail.com"; // admissions office (mobile 677 195 500 is calls-only, King-verified)
function setLang(l){''',
    'js const')

rep('''  var msg = fr
    ? "Bonjour SJC Sasse ! Je souhaite des informations d'admission.\\n\\nParent : " + fn + " " + ln + "\\nTéléphone : " + ph + "\\nClasse d'entrée : " + gr + (q ? "\\nQuestion : " + q : "")
    : "Hello SJC Sasse! I would like admissions information.\\n\\nParent: " + fn + " " + ln + "\\nPhone: " + ph + "\\nClass entering: " + gr + (q ? "\\nQuestion: " + q : "");
  window.open("https://wa.me/" + WA_NUM + "?text=" + encodeURIComponent(msg), "_blank");
  return false;''',
'''  var subj = fr ? "Demande d'informations d'admission 2026/2027 — SJC Sasse" : "Admissions enquiry 2026/27 — SJC Sasse";
  var body = fr
    ? "Bonjour,\\n\\nJe souhaite recevoir les informations d'admission 2026/2027 du Collège Saint-Joseph de Sasse.\\n\\nParent/tuteur : " + fn + " " + ln + "\\nTéléphone : " + ph + "\\nClasse d'entrée : " + gr + (q ? "\\nQuestion : " + q : "") + "\\n"
    : "Good day,\\n\\nI would like to receive the 2026/27 admissions information for St. Joseph's College, Sasse.\\n\\nParent/guardian: " + fn + " " + ln + "\\nPhone: " + ph + "\\nClass entering: " + gr + (q ? "\\nQuestion: " + q : "") + "\\n";
  window.location.href = "mailto:" + COLLEGE_EMAIL + "?subject=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(body);
  return false;''',
    'sendLead')

open(f, 'w', encoding='utf-8').write(h)
print('patched OK')
