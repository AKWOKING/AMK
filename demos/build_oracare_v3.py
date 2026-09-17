#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_oracare_v3.py — merge the 24/7 bilingual chat assistant from
concept-oracare-v1.html INTO concept-oracare-v2.html (Odentrics-reference build
with clear FCFA pricing).

Why: King's first OraCare message (14 Sep 2026) promised BOTH "clear FCFA
pricing" AND "1-tap WhatsApp booking 24/7". v2 has pricing but no assistant;
v1 has the assistant but no FCFA figures. v3 delivers both promises.

v2 wiring: booking form selects b-service (idx 7 = emergency after this script),
b-day, b-time; sections #book and #pricing; FAB/port added here.
"""
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
V2 = (ROOT / "concept-oracare-v2.html").read_text(encoding="utf-8")

BOT_CSS = """
/* ===== 24/7 scripted chat assistant (merged from v1, restyled to v2 tokens) ===== */
.hero-chat{display:inline-block;margin-top:14px;font-size:13.5px;font-weight:600;color:var(--navy);text-decoration:underline;text-underline-offset:3px;text-align:left}
.hero-chat:hover{color:var(--gold)}
.bot-fab{position:fixed;right:24px;bottom:24px;z-index:80;width:58px;height:58px;border-radius:50%;background:var(--navy);border:none;cursor:pointer;box-shadow:0 14px 34px rgba(22,50,58,.35);display:flex;align-items:center;justify-content:center;transition:transform .25s cubic-bezier(.16,1,.3,1)}
.bot-fab:hover{transform:translateY(-3px) scale(1.04)}
.bot-fab:active{transform:scale(.97)}
.bot-fab .pulse{position:absolute;top:3px;right:3px;width:13px;height:13px;border-radius:50%;background:var(--sage-d);border:2.5px solid var(--cream);animation:botpulse 2.2s infinite}
@keyframes botpulse{0%{box-shadow:0 0 0 0 rgba(127,168,143,.5)}70%{box-shadow:0 0 0 9px rgba(127,168,143,0)}100%{box-shadow:0 0 0 0 rgba(127,168,143,0)}}
.bot-panel{position:fixed;right:24px;bottom:94px;z-index:80;width:360px;max-width:calc(100vw - 24px);max-height:min(540px,72vh);background:#fff;border-radius:22px;box-shadow:0 30px 80px rgba(22,50,58,.32);display:flex;flex-direction:column;overflow:hidden;opacity:0;transform:translateY(14px) scale(.97);pointer-events:none;transition:opacity .3s,transform .3s cubic-bezier(.16,1,.3,1)}
.bot-panel.open{opacity:1;transform:none;pointer-events:auto}
.bot-head{background:var(--navy);color:#fff;padding:14px 16px;display:flex;align-items:center;gap:11px}
.bot-head .bdot{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;flex:none}
.bot-head b{display:block;font-family:'Outfit',sans-serif;font-size:15px}
.bot-head small{display:block;font-size:11px;color:rgba(255,255,255,.72)}
.bot-close{margin-left:auto;background:none;border:none;color:rgba(255,255,255,.85);font-size:22px;cursor:pointer;line-height:1;padding:4px}
.bot-msgs{flex:1;overflow-y:auto;padding:16px 14px;background:var(--cream);display:flex;flex-direction:column;gap:10px;min-height:210px}
.bm{max-width:84%;padding:11px 14px;border-radius:16px;font-size:13.5px;line-height:1.5;animation:bpop .3s ease}
@keyframes bpop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.bm.bot{background:#fff;border:1px solid rgba(22,50,58,.12);border-bottom-left-radius:6px;align-self:flex-start;color:var(--ink)}
.bm.user{background:var(--navy);color:#fff;border-bottom-right-radius:6px;align-self:flex-end}
.bchips{display:flex;flex-wrap:wrap;gap:7px;align-self:flex-start;max-width:96%}
.bchip{border:1.5px solid rgba(22,50,58,.14);background:#fff;border-radius:99px;padding:8px 13px;font-size:12.5px;font-weight:600;color:var(--navy);cursor:pointer;transition:all .18s;font-family:'Outfit',sans-serif}
.bchip:hover{border-color:var(--sage-d);transform:translateY(-1px);background:var(--sage)}
.bot-input{display:flex;gap:8px;padding:12px;border-top:1px solid rgba(22,50,58,.1);background:#fff}
.bot-input input{flex:1;border:1.5px solid rgba(22,50,58,.14);border-radius:99px;padding:11px 16px;font:500 13.5px 'Inter',sans-serif;background:var(--cream);color:var(--ink)}
.bot-input input:focus{outline:none;border-color:var(--sage-d);box-shadow:0 0 0 4px rgba(127,168,143,.16)}
.bot-input button{width:44px;height:44px;border-radius:50%;border:none;background:var(--gold);cursor:pointer;flex:none;display:flex;align-items:center;justify-content:center;transition:transform .2s}
.bot-input button:hover{transform:scale(1.06)}
@media(max-width:640px){
  .bot-fab{right:14px;bottom:calc(20px + env(safe-area-inset-bottom))}
  .bot-panel{right:12px;left:12px;width:auto;bottom:calc(82px + env(safe-area-inset-bottom));max-height:calc(100dvh - 170px)}
}
@media (prefers-reduced-motion:reduce){.bot-fab .pulse{animation:none}.bm{animation:none}.bot-panel{transition:none}}
"""

HERO_LINK = """      <a class="hero-chat rv" href="#" onclick="botToggle(true);return false;" data-en="💬 Prefer to chat? Our 24/7 assistant answers in English &amp; French" data-fr="💬 Vous préférez discuter ? Notre assistant 24h/7 répond en anglais et en français">💬 Prefer to chat? Our 24/7 assistant answers in English &amp; French</a>
"""

HERO_ANCHOR = '      </div>\n    </div>\n  </div>\n  <span class="spark"'
HERO_REPL = '      </div>\n' + HERO_LINK + '    </div>\n  </div>\n  <span class="spark"'

EMERG_OLD = '          <option data-en="Not sure yet" data-fr="Pas encore sûr">Not sure yet</option>\n        </select>'
EMERG_NEW = ('          <option data-en="Not sure yet" data-fr="Pas encore sûr">Not sure yet</option>\n'
             '          <option data-en="Emergency (same day)" data-fr="Urgence (jour même)">Emergency (same day)</option>\n'
             '        </select>')

BOT_HTML = """<!-- 24/7 CHAT ASSISTANT (scripted demo · verified clinic info only · v3 merge) -->
<button class="bot-fab" onclick="botToggle()" aria-label="Chat with the OraCare assistant">
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#C9A24B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 12.3 4.9 8.38 8.38 0 0 1 0 3.8z"/></svg>
  <span class="pulse"></span>
</button>
<div class="bot-panel" id="bot-panel" role="dialog" aria-label="OraCare chat assistant">
  <div class="bot-head">
    <span class="bdot"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 12.3 4.9 8.38 8.38 0 0 1 0 3.8z"/></svg></span>
    <span><b data-en="OraCare Assistant" data-fr="Assistant OraCare">OraCare Assistant</b><small data-en="Online · 24/7 · answers in seconds (concept demo)" data-fr="En ligne · 24h/7 · répond en quelques secondes (démo concept)">Online · 24/7 · answers in seconds (concept demo)</small></span>
    <button class="bot-close" onclick="botToggle(false)" aria-label="Close">&times;</button>
  </div>
  <div class="bot-msgs" id="bot-msgs"></div>
  <div class="bot-input">
    <input type="text" id="bot-in" data-ph-en="Type your question…" data-ph-fr="Écrivez votre question…" placeholder="Type your question…" onkeydown="if(event.key==='Enter')botSend()">
    <button onclick="botSend()" aria-label="Send"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16323A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/></svg></button>
  </div>
</div>

"""

BOT_JS = r"""
/* ---------- 24/7 CHAT ASSISTANT (scripted · verified info only · merged into v3) ---------- */
var botOpen = false, botInit = false;
function bLang(){ return document.documentElement.lang === "fr" ? "fr" : "en"; }
var CH = {
  hours:{t:{en:"🕐 Opening hours",fr:"🕐 Horaires"}, act:"hours"},
  loc:{t:{en:"📍 Where are you?",fr:"📍 Où êtes-vous ?"}, act:"loc"},
  svc:{t:{en:"🦷 What do you treat?",fr:"🦷 Que soignez-vous ?"}, act:"svc"},
  price:{t:{en:"💰 See prices",fr:"💰 Voir les prix"}, act:"pricing"},
  book:{t:{en:"📅 Book a visit",fr:"📅 Réserver une visite"}, act:"book"},
  emerg:{t:{en:"🚨 Emergency",fr:"🚨 Urgence"}, act:"emerg"},
  call:{t:{en:"📞 Call now",fr:"📞 Appeler"}, act:"call"}
};
var BOT_DEFAULT = [CH.hours, CH.loc, CH.svc, CH.price, CH.book, CH.emerg];
var CH_S1 = {t:{en:"General & preventive",fr:"Général & préventif"}, act:"svc:0"};
var CH_S2 = {t:{en:"Cosmetic (veneers, whitening)",fr:"Esthétique (facettes, blanchiment)"}, act:"svc:3"};
var CH_S3 = {t:{en:"Implants & crowns",fr:"Implants & couronnes"}, act:"svc:4"};
var CH_S4 = {t:{en:"Aligners & braces",fr:"Aligneurs & bagues"}, act:"svc:5"};
var CH_CALL = {t:{en:"📞 Call now",fr:"📞 Appeler"}, act:"call"};
var CH_BOOK = {t:{en:"📅 Open booking",fr:"📅 Ouvrir la réservation"}, act:"book"};
var CH_EMB  = {t:{en:"🚨 Emergency booking",fr:"🚨 Réservation d'urgence"}, act:"emerg"};
var BOT_INTENTS = [
  {re:/emergency|urgent|urgency|urgence|douleur|tooth ?ache|hurts|ache\b|mal aux dents/i,
   r:{en:"For pain or injury we keep same-day emergency slots. The fastest route is a call: +237 672 52 66 86 — or tap emergency booking and we'll call you right away.",
      fr:"Pour la douleur ou un traumatisme, nous gardons des créneaux d'urgence le jour même. Le plus rapide est un appel : +237 672 52 66 86 — ou touchez réservation d'urgence et nous vous rappelons immédiatement."},
   chips:[CH_CALL, CH_EMB]},
  {re:/book|appointment|booking|rendez|rdv|réserver|reserve a visit/i,
   r:{en:"Happy to book you in — about 60 seconds: pick your service, day and time, then your details. We confirm by call or WhatsApp the same day.",
      fr:"Avec plaisir — environ 60 secondes : choisissez le soin, le jour et l'heure, puis vos coordonnées. Nous confirmons par appel ou WhatsApp le jour même."},
   chips:[CH_BOOK]},
  {re:/hour|open|closing|horaire|ouvert|fermé|ferme\b|quand|when (are you|can i)/i,
   r:{en:"Our sample hours on this concept are Monday to Saturday, 8:00 am to 6:00 pm — your real hours replace these at launch. When you book, the team confirms your exact time.",
      fr:"Les horaires d'exemple sur cette maquette sont du lundi au samedi, 8h00 à 18h00 — vos vrais horaires les remplacent au lancement. À la réservation, l'équipe confirme votre heure exacte."},
   chips:[CH_BOOK, CH.loc]},
  {re:/price|cost|how much|expensive|cheap|afford|prix|coût|combien|cher|tarif/i,
   r:{en:"This concept lists clear starting prices in FCFA in the pricing section — and every treatment plan comes with a written quote before we start. Quotes are free at your first visit.",
      fr:"Cette maquette affiche des tarifs de départ clairs en FCFA dans la section tarifs — et chaque plan de soin est accompagné d'un devis écrit avant de commencer. Le devis est gratuit à la première visite."},
   chips:[{t:{en:"💰 See the price list",fr:"💰 Voir les tarifs"},act:"pricing"}, CH_BOOK]},
  {re:/afraid|fear|nervous|anxious|scared|peur|nerv|anxi|effray/i,
   r:{en:"Totally normal — most of our patients feel it. We go at your pace, explain every step before it happens, and you can ask us to pause at any time. Mention it in your booking and we'll set you up for comfort.",
      fr:"Tout à fait normal — la plupart de nos patients le ressentent. Nous avançons à votre rythme, expliquons chaque étape avant qu'elle survienne, et vous pouvez demander une pause à tout moment. Mentionnez-le dans votre réservation et nous préparons tout pour votre confort."},
   chips:[CH_BOOK]},
  {re:/english|french|français|anglais|language|langue|bilingual/i,
   r:{en:"We see patients in English and French — and this assistant follows the site's language. Switch any time with the EN|FR button at the top.",
      fr:"Nous recevons les patients en anglais et en français — et cet assistant suit la langue du site. Changez-la à tout moment avec le bouton EN|FR en haut."},
   chips:[CH_BOOK]},
  {re:/child|kid|baby|teen|enfant|ado|bébé/i,
   r:{en:"Yes — we see children and teens, gently and at their pace. Book a first visit and we prepare a calm, kid-friendly room.",
      fr:"Oui — nous recevons enfants et adolescents, en douceur et à leur rythme. Réservez une première visite et nous préparons une pièce calme et conviviale."},
   chips:[CH_BOOK]},
  {re:/where|address|location|find you|directions|adresse|où|situ|localisation/i,
   r:{en:"We're at St. Pius Hospital, Mayor's Street, Molyko, Buea — right at the hospital. A Google Maps embed goes on the final site.",
      fr:"Nous sommes à l'hôpital St. Pius, Mayor's Street, Molyko, Buéa — juste à l'hôpital. Une carte Google Maps intégrée figure sur le site final."},
   chips:[CH_BOOK, CH_CALL]},
  {re:/service|treat|veneer|whiten|implant|crown|aligner|brace|cleaning|check|soin|facette|blanchiment|couronne|bagues|détartrage|aligneur|traiter/i,
   r:{en:"We cover four areas: (1) General & preventive — check-ups and cleanings · (2) Cosmetic — veneers & whitening · (3) Restorative — implants & crowns · (4) Aligners & braces. Which one can I help with?",
      fr:"Nous couvrons quatre domaines : (1) Général & préventif — contrôles et détartrages · (2) Esthétique — facettes & blanchiment · (3) Prothèse — implants & couronnes · (4) Aligneurs & bagues. Lequel puis-je vous préparer ?"},
   chips:[CH_S1, CH_S2, CH_S3, CH_S4]},
  {re:/phone|number|call|contact|téléphone|numéro|appeler|joindre/i,
   r:{en:"Our line is +237 672 52 66 86 — call or WhatsApp, we answer.",
      fr:"Notre ligne : +237 672 52 66 86 — appelez ou WhatsApp, nous répondons."},
   chips:[CH_CALL, CH_BOOK]},
  {re:/human|agent|real person|docteur|dentiste|humain|quelqu/i,
   r:{en:"Here's a real human — the team is reachable on +237 672 52 66 86 by call or WhatsApp.",
      fr:"Voici un humain — l'équipe est joignable au +237 672 52 66 86 par appel ou WhatsApp."},
   chips:[CH_CALL]},
  {re:/thank|thanks|merci|gratitude/i,
   r:{en:"You're welcome! I'm here 24/7 if anything else comes up. 😊",
      fr:"Avec plaisir ! Je suis là 24h/7 si vous avez autre chose. 😊"},
   chips:null},
  {re:/(hi|hello|hey|good morning|good afternoon|good evening|bonjour|bonsoir|salut|salam)\b/i,
   r:{en:"Hello! 👋 I'm the OraCare assistant — I answer quick questions (hours, location, services, prices, emergencies) or start your booking. What can I do for you?",
      fr:"Bonjour ! 👋 Je suis l'assistant OraCare — je réponds aux questions rapides (horaires, adresse, soins, prix, urgences) ou je lance votre réservation. Que puis-je faire pour vous ?"},
   chips:BOT_DEFAULT}
];
var BOT_FALLBACK = {
  en:"I'm a small assistant, so I know best about: opening hours, our location, our services, the price list, emergencies, and bookings. Try one of those — or reach the team directly on WhatsApp.",
  fr:"Je suis un petit assistant ; je connais donc le mieux : les horaires, notre adresse, nos soins, les tarifs, les urgences et les réservations. Essayez l'un de ceux-ci — ou contactez directement l'équipe sur WhatsApp."
};
function botToggle(force){
  var p = document.getElementById("bot-panel");
  botOpen = (typeof force === "boolean") ? force : !botOpen;
  p.classList.toggle("open", botOpen);
  if(botOpen && !botInit){
    botInit = true;
    botTyping(function(){ botSay(BOT_INTENTS[BOT_INTENTS.length-1].r[bLang()], BOT_DEFAULT); });
  }
  if(botOpen){ setTimeout(function(){ var i=document.getElementById("bot-in"); if(i) i.focus(); }, 320); }
}
function botSay(text, chips, user){
  var box = document.getElementById("bot-msgs");
  var d = document.createElement("div");
  d.className = "bm " + (user ? "user" : "bot");
  d.textContent = text;
  box.appendChild(d);
  if(chips){
    var c = document.createElement("div");
    c.className = "bchips";
    chips.forEach(function(ch){
      var b = document.createElement("button");
      b.className = "bchip";
      b.textContent = ch.t[bLang()];
      b.onclick = function(){ botAct(ch.act); };
      c.appendChild(b);
    });
    box.appendChild(c);
  }
  box.scrollTop = box.scrollHeight;
}
function botTyping(cb){
  var box = document.getElementById("bot-msgs");
  var d = document.createElement("div");
  d.className = "bm bot";
  d.textContent = "…";
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
  setTimeout(function(){ if(d.parentNode) d.parentNode.removeChild(d); cb(); }, 650);
}
/* v2 booking form: b-service select (0 General … 6 Not sure, 7 Emergency added), b-day, b-time; sections #book / #pricing */
function botFillBooking(serviceIdx){
  var sec = document.getElementById("b-service");
  if(sec && typeof serviceIdx === "number" && sec.options[serviceIdx]){ sec.selectedIndex = serviceIdx; }
  document.getElementById("book").scrollIntoView({behavior:"smooth"});
  setTimeout(function(){ var el = document.getElementById("b-name"); if(el){ el.focus(); } }, 750);
}
function botAct(act){
  if(act === "call"){ window.location.href = "tel:+237672526686"; return; }
  if(act === "pricing"){ document.getElementById("pricing").scrollIntoView({behavior:"smooth"}); return; }
  if(act === "book"){ botToggle(false); botFillBooking(null); return; }
  if(act === "emerg"){ botToggle(false); botFillBooking(7); return; }
  if(act.indexOf("svc:") === 0){ botToggle(false); botFillBooking(parseInt(act.split(":")[1], 10)); return; }
  var texts = {
    hours:{en:"What are your opening hours?",fr:"Quels sont vos horaires ?"},
    loc:{en:"Where are you located?",fr:"Où êtes-vous situés ?"},
    svc:{en:"What services do you offer?",fr:"Quels soins proposez-vous ?"},
    pricing:{en:"How much does treatment cost?",fr:"Combien coûtent les soins ?"}
  };
  if(texts[act]){ botSendText(texts[act][bLang()]); }
}
function botSend(){
  var el = document.getElementById("bot-in");
  var v = el.value.trim();
  if(!v) return;
  el.value = "";
  botSendText(v);
}
function botSendText(v){
  botSay(v, null, true);
  var hit = null;
  for(var i = 0; i < BOT_INTENTS.length; i++){ if(BOT_INTENTS[i].re.test(v)){ hit = BOT_INTENTS[i]; break; } }
  botTyping(function(){
    if(hit){ botSay(hit.r[bLang()], hit.chips); }
    else { botSay(BOT_FALLBACK[bLang()], BOT_DEFAULT); }
  });
}
/* keep the bot input placeholder + panel labels synced with the EN|FR toggle */
var __setLangOrig = setLang;
setLang = function(l){
  __setLangOrig(l);
  var bi = document.getElementById("bot-in");
  if(bi){ bi.placeholder = (l === "fr") ? bi.getAttribute("data-ph-fr") : bi.getAttribute("data-ph-en"); }
};
"""

def must_replace(html, old, new, label):
    if old not in html:
        sys.exit(f"FAIL: anchor not found for {label}")
    if html.count(old) > 1:
        sys.exit(f"FAIL: anchor not unique for {label} ({html.count(old)} hits)")
    return html.replace(old, new, 1)

out = V2
out = must_replace(out, "<!DOCTYPE html>",
    "<!DOCTYPE html>\n<!-- OraCare concept v3 (14 Sep 2026): v2 Odentrics-reference build (clear FCFA prices) + 24/7 EN|FR scripted chat assistant merged from v1. -->",
    "doctype marker")
out = must_replace(out, "</style>", BOT_CSS + "</style>", "bot css")
out = must_replace(out, HERO_ANCHOR, HERO_REPL, "hero chat link")
out = must_replace(out, EMERG_OLD, EMERG_NEW, "emergency option")
out = must_replace(out, "<script>", BOT_HTML + "<script>", "bot html")
out = must_replace(out, "</script>", BOT_JS + "</script>", "bot js")

dest = ROOT / "concept-oracare-v3.html"
MOBILE_NAV_CSS = """
/* AMK mobile-first nav pass (16 Sep 2026): EN|FR pill must never clip on phones */
.lang-sw{flex:0 0 auto}
.lang-sw button{min-height:40px}
@media(max-width:1000px){ .concept-badge{display:none} }
@media(max-width:860px){
  .nav-phone,.concept-badge,.logo small,.nav-cta{display:none}
  .lang-sw{margin-left:auto}
  .lang-sw button{min-height:44px;padding:10px 16px;font-size:13px}
  .logo{min-width:0}
}
@media(max-width:620px){
  nav.main .wrap{gap:10px;padding-top:10px;padding-bottom:10px;padding-left:16px;padding-right:16px}
  .lang-sw button{padding:10px 15px}
}
@media(max-width:380px){ .tooth{width:34px;height:34px;border-radius:10px} .logo{font-size:19px} }
"""

out = out.replace("</style>", MOBILE_NAV_CSS + "</style>", 1) if "mobile-first nav pass" not in out else out

A11Y_CSS = """
/* a11y-pass-2026-09-17 — readable small text (audited by tools/qa/audit_html.py).
   Light surfaces get a darker text variant of the accent; mid-tone pills get a
   darker fill under light text; the dark booking block gets a lighter accent. */
.eyebrow b{color:#3F7A1E}
.spark{color:#3F7A1E;opacity:.8}
.t-fb b{color:#3F7A1E}
.faq-item summary .pm{color:#0F6E7B}
.loc-strip a.dir{background:#2C7A22;color:#F0FAF1}
.loc-strip a.dir:hover{background:#25681C}
.step3 .n{background:#146A2C;color:#F0FAF1}
.step3 span{color:rgba(240,250,241,.9)}
.btn-dark{background:linear-gradient(135deg,#2A7A20 0%,#1F6E7A 100%)}
.book .eyebrow b,
.book .eyebrow span b{color:#B6E88F}

.concept-badge{color:#846420}
.f-bottom b{color:#846420}
"""

_i = out.rfind("</style>")
out = out[:_i] + A11Y_CSS + out[_i:]


dest.write_text(out, encoding="utf-8")
print(f"WROTE {dest} ({len(out.encode('utf-8'))} bytes)")
