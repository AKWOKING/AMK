#!/usr/bin/env python3
"""AMK — injection de la couche vocale Tier 0 dans site/index.html (18 Sep 2026).

Protocole §21 (AMK-DESIGN-SKILLS.md) :
  · la voix est une ADDITION — le bouton WhatsApp reste la voie principale
  · clic explicite pour le micro, jamais d'écoute automatique
  · toute réponse est traçable à une ligne de la page
  · repli honnête + WhatsApp quand l'assistant ne sait pas
  · langue = celle du site (fr-FR / en-US)

Idempotent : si le marqueur VX est déjà présent, le script ne réinjecte rien.
Usage : python3 tools/site/patch_voice_widget.py [chemin/index.html]
"""
import re
import sys
import pathlib

TARGET = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site/index.html")
MARK = "<!-- VX:VOICE-LAYER -->"

CSS = """
/* ===== VX voice layer (Tier 0 — scripted answers, browser speech, no backend) ===== */
.vx-fab{position:fixed;right:18px;bottom:18px;z-index:130;display:flex;align-items:center;gap:9px;
  background:var(--amber);color:#0F172A;border:0;border-radius:99px;padding:13px 18px;
  font-family:inherit;font-size:15px;font-weight:800;cursor:pointer;
  box-shadow:0 10px 26px rgba(15,23,42,.28);transition:.15s}
.vx-fab:hover{transform:translateY(-2px)}
.vx-fab svg{width:19px;height:19px;flex:0 0 auto}
.vx-panel{position:fixed;right:18px;bottom:88px;z-index:131;width:min(400px,calc(100vw - 24px));
  max-height:min(74vh,620px);overflow:auto;background:#fff;color:#0F172A;
  border:1px solid var(--border);border-radius:20px;box-shadow:0 24px 60px rgba(15,23,42,.30);padding:16px}
.vx-panel[hidden]{display:none}
.vx-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:6px}
.vx-head strong{font-size:16px;font-weight:800;color:#0F172A}
.vx-x{border:0;background:#F1F5F9;color:#0F172A;width:32px;height:32px;border-radius:50%;
  font-size:15px;cursor:pointer;line-height:1;font-family:inherit}
.vx-note{margin:0 0 12px;font-size:12.5px;line-height:1.45;color:#475569}
.vx-mic{width:100%;display:flex;align-items:center;justify-content:center;gap:10px;background:#0F172A;
  color:#fff;border:0;border-radius:14px;padding:15px 14px;font-family:inherit;font-size:15px;
  font-weight:800;cursor:pointer;transition:.15s}
.vx-mic.on{background:#B91C1C;color:#fff}
.vx-mic:disabled{opacity:.55;cursor:not-allowed}
.vx-mic svg{width:20px;height:20px;flex:0 0 auto}
.vx-chips{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0}
.vx-chip{border:1.5px solid var(--border);background:#F8FAFC;color:#0F172A;border-radius:99px;
  padding:8px 12px;font-family:inherit;font-size:13px;font-weight:700;cursor:pointer;text-align:left}
.vx-chip:hover{border-color:var(--amber);background:var(--amber-t)}
.vx-out{margin-top:12px;border-top:1px solid var(--border);padding-top:12px}
.vx-out[hidden]{display:none}
.vx-you{margin:0 0 8px;font-size:13px;color:#475569;font-style:italic}
.vx-ans{margin:0 0 10px;font-size:14.5px;line-height:1.55;color:#0F172A}
.vx-act{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.vx-act a,.vx-act button{font-family:inherit;font-size:13px;font-weight:700;border-radius:10px;
  padding:10px 13px;border:1.5px solid var(--border);background:#fff;color:#0F172A;
  cursor:pointer;text-decoration:none;line-height:1}
.vx-act a{background:#10B981;border-color:#10B981;color:#04211D}
.vx-consent{margin:12px 0 0;font-size:11.5px;line-height:1.5;color:#64748B}
@media (max-width:760px){
  .vx-fab{bottom:86px;right:12px;padding:12px 16px;font-size:14px}
  .vx-panel{bottom:150px;right:12px;left:12px;width:auto;max-height:min(62vh,520px)}
}
"""

HTML = MARK + """
<button class="vx-fab" id="vx-fab" type="button"
  data-en="Talk to this site" data-fr="Parler à ce site"
  aria-controls="vx-panel" aria-expanded="false">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M5 11a7 7 0 0 0 14 0"/><path d="M12 18v4"/></svg>
  <span data-en="Talk to this site" data-fr="Parler à ce site">Talk to this site</span>
</button>

<div class="vx-panel" id="vx-panel" role="dialog" aria-labelledby="vx-title" hidden>
  <div class="vx-head">
    <strong id="vx-title" data-en="Ask the site a question" data-fr="Posez une question au site">Ask the site a question</strong>
    <button class="vx-x" id="vx-x" type="button" aria-label="Close" data-aria-en="Close" data-aria-fr="Fermer">&#10005;</button>
  </div>
  <p class="vx-note" data-en="Demo — it only answers with what is written on this page." data-fr="Démo — il ne répond qu'avec ce qui est écrit sur cette page.">Demo — it only answers with what is written on this page.</p>

  <button class="vx-mic" id="vx-mic" type="button">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/><path d="M5 11a7 7 0 0 0 14 0"/><path d="M12 18v4"/></svg>
    <span id="vx-mic-label" data-en="Tap to speak" data-fr="Appuyez pour parler">Tap to speak</span>
  </button>

  <div class="vx-chips" id="vx-chips"></div>

  <div class="vx-out" id="vx-out" hidden>
    <p class="vx-you" id="vx-you"></p>
    <p class="vx-ans" id="vx-ans"></p>
    <div class="vx-act">
      <a id="vx-wa" href="#" target="_blank" rel="noopener" data-en="Continue on WhatsApp" data-fr="Continuer sur WhatsApp">Continue on WhatsApp</a>
      <button id="vx-mute" type="button" data-en="Mute voice" data-fr="Couper la voix">Mute voice</button>
    </div>
  </div>

  <p class="vx-consent" data-en="Voice recognition uses your browser's own speech service (Chrome or Edge). Only when you tap the microphone, and only your question is sent to the browser maker. This page itself never records you." data-fr="La reconnaissance vocale utilise le service vocal de votre navigateur (Chrome ou Edge). Seulement quand vous appuyez sur le microphone, et seule votre question est envoyée à l'éditeur du navigateur. Cette page n'enregistre rien.">Voice recognition uses your browser's own speech service (Chrome or Edge). Only when you tap the microphone, and only your question is sent to the browser maker. This page itself never records you.</p>
</div>
"""

JS = """<script>
/* ===== VX voice layer — Tier 0 (scripted answers traced to this page, browser speech) =====
   Regles : le bouton WhatsApp reste la voie principale · micro = clic explicite ·
   aucune reponse inventee · repli honnete · langue = celle du site. */
(function(){
  var WAN = (typeof WA_NUM !== "undefined" && WA_NUM) ? WA_NUM : "237677789631";
  var fab=document.getElementById("vx-fab"), panel=document.getElementById("vx-panel"),
      mic=document.getElementById("vx-mic"), micLabel=document.getElementById("vx-mic-label"),
      chips=document.getElementById("vx-chips"), out=document.getElementById("vx-out"),
      you=document.getElementById("vx-you"), ansEl=document.getElementById("vx-ans"),
      wa=document.getElementById("vx-wa"), muteBtn=document.getElementById("vx-mute");
  if(!fab||!panel) return;

  var SR = window.SpeechRecognition || window.webkitSpeechRecognition || null;
  var rec=null, listening=false, muted=false, current="";

  function lang(){ return document.documentElement.lang === "fr" ? "fr" : "en"; }
  function t(en,fr){ return lang()==="fr" ? fr : en; }
  function norm(s){
    return (s||"").toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"")
      .replace(/[^a-z0-9\\s]/g," ").replace(/\\s+/g," ").trim();
  }

  /* --- Base de connaissances : chaque reponse = une ligne deja presente sur la page --- */
  var FALLBACK = {
    en:"I do not know that one. I only answer with what is written on this page. Send us the question on WhatsApp and Akwo King will answer you directly.",
    fr:"Je ne sais pas repondre a ca. Je ne reponds qu'avec ce qui est ecrit sur cette page. Envoyez la question sur WhatsApp et Akwo King vous repondra directement."
  };
  var KB = [
    { chip:{en:"How much does it cost?", fr:"Combien ca coute ?"},
      k:["prix","combien","coute","cout","tarif","price","cost","how much","fcfa","cher","chere","budget"],
      en:"One price: 100,000 FCFA for the founding package. It is paid 50/50, so 50,000 to start and 50,000 when the site goes live. Nothing hidden.",
      fr:"Un seul prix : 100 000 FCFA pour la formule fondatrice. Ca se paie 50/50, donc 50 000 pour demarrer et 50 000 a la mise en ligne. Rien de cache." },

    { chip:{en:"Is the preview free?", fr:"L'apercu est-il gratuit ?"},
      k:["apercu","preview","gratuit","free","essai","24","paye"],
      en:"The preview is free. Send us the name of your school or clinic on WhatsApp and the preview is on your phone within 24 hours. You pay nothing until you approve it.",
      fr:"L'apercu est gratuit. Envoyez-nous le nom de votre ecole ou clinique sur WhatsApp et l'apercu est dans votre telephone sous 24 heures. Vous ne payez rien avant votre accord." },

    { chip:{en:"How long does it take?", fr:"Combien de temps ca prend ?"},
      k:["delai","temps","duree","jours","long","vite","rapide","live","launch","lancement","quand","prend"],
      en:"Once you approve the preview, the site is live in 3 to 5 days.",
      fr:"Apres votre validation, le site est en ligne en 3 a 5 jours." },

    { chip:{en:"What about after launch?", fr:"Et apres le lancement ?"},
      k:["mensuel","monthly","abonnement","maintenance","suivi","subscription","apres","plus tard","mois"],
      en:"After launch you get one month of free support. After that, if you want us to handle updates, it is 15,000 FCFA per month: hosting managed, two updates a month, and the site stays online and backed up. No contract, you can stop any time, and the domain and files stay yours.",
      fr:"Apres le lancement, vous avez un mois de support gratuit. Ensuite, si vous voulez que nous gerons les mises a jour, c'est 15 000 FCFA par mois : hebergement suivi, deux modifications par mois, et le site reste en ligne et sauvegarde. Sans engagement, vous arretez quand vous voulez, et le domaine et les fichiers restent a vous." },

    { k:["bilingue","bilingual","anglais","francais","english","french","langue","language","deux langues"],
      en:"Bilingual EN|FR is included as standard on every site we build, never an add-on. A school or clinic in Cameroon serves both languages, and your website should too.",
      fr:"Le bilingue EN|FR est inclus en standard sur chaque site, jamais une option. Une ecole ou une clinique au Cameroun sert les deux langues, et votre site devrait aussi." },

    { k:["ecole","school","clinique","clinic","laboratoire","lab","hopital","hospital","sante","qui","travaillez","niche"],
      en:"AMK works with two kinds of institutions: schools and clinics. There is a live clinic concept on this page that you can open right now.",
      fr:"AMK travaille avec deux types d'etablissements : les ecoles et les cliniques. Un concept de clinique est en ligne sur cette page, vous pouvez l'ouvrir maintenant." },

    { k:["inclus","comprend","included","include","contient","offre","package","pack","formule","sections"],
      en:"The founding package includes a one-page bilingual homepage of up to six sections, a WhatsApp button on every screen, domain and secure hosting set up, 30 minutes of staff training, one month of free support, and launch in 3 to 5 days.",
      fr:"La formule fondatrice comprend une page d'accueil bilingue jusqu'a six sections, un bouton WhatsApp sur chaque ecran, la configuration du domaine et de l'hebergement, 30 minutes de formation pour votre personnel, un mois de support gratuit, et la mise en ligne en 3 a 5 jours." },

    { k:["personnel","staff","modifier","update","mettre a jour","changer","equipe","technique","photos","actualites","news"],
      en:"Yes. We design for non-technical staff, train your team in 30 minutes and stay reachable on WhatsApp. News, photos, events: your team handles it.",
      fr:"Oui. Nous concevons pour du personnel non technique, formons votre equipe en 30 minutes et restons joignables sur WhatsApp. Actualites, photos, evenements : votre equipe s'en charge." },

    { k:["google","trouve","found","recherche","search","referencement","seo","visibilite","parents","patients","visible"],
      en:"We build with local search in mind: fast pages, clean structure, both languages, and the words parents and patients really type, like school in Douala or dentist in Buea. We set you up to be found, and your reputation does the rest.",
      fr:"Nous construisons pour la recherche locale : des pages rapides, une structure propre, les deux langues, et les mots que les parents et les patients tapent vraiment, comme ecole a Douala ou dentiste a Buea. On vous met en position d'etre trouve, et votre reputation fait le reste." },

    { k:["domaine","domain","proprietaire","appartient","fichiers","files","own","possedez","enferme"],
      en:"The domain and the files are 100% yours. You are never locked in.",
      fr:"Le domaine et les fichiers vous appartiennent a 100 pour cent. Vous n'etes jamais enferme." },

    { k:["payer","paiement","payment","mobile money","momo","orange","acompte","deposit","especes","virement","cash"],
      en:"Payment is 50/50: half to start, half at launch. Nothing is charged before you approve the preview.",
      fr:"Le paiement se fait 50/50 : la moitie pour demarrer, la moitie au lancement. Rien n'est facture avant votre accord." },

    { k:["pages","plusieurs","multi","growth","grande","grand","huit","eight","lycee","college"],
      en:"If you need more than one page, up to eight pages, we send you a transparent quote before you commit to anything.",
      fr:"Si vous avez besoin de plusieurs pages, jusqu'a huit pages, nous vous envoyons un devis transparent avant tout engagement." },

    { chip:{en:"How do I start?", fr:"Comment commencer ?"},
      k:["commencer","start","comment","contact","whatsapp","numero","appeler","message","ecrire","devis","quote","parler"],
      en:"The simplest way: message us on WhatsApp. Tell us the name of your school or clinic, and your free preview follows within 24 hours.",
      fr:"Le plus simple : ecrivez-nous sur WhatsApp. Donnez-nous le nom de votre ecole ou clinique, et votre apercu gratuit suit dans les 24 heures." }
  ];

  function renderChips(){
    chips.innerHTML = "";
    KB.forEach(function(e){
      if(!e.chip) return;
      var b=document.createElement("button");
      b.type="button"; b.className="vx-chip";
      b.textContent = lang()==="fr" ? e.chip.fr : e.chip.en;
      b.addEventListener("click", function(){ ask(b.textContent, false); });
      chips.appendChild(b);
    });
  }

  function speak(txt){
    if(muted || !("speechSynthesis" in window)) return;
    try{ window.speechSynthesis.cancel(); }catch(e){}
    var u = new SpeechSynthesisUtterance(txt);
    u.lang = lang()==="fr" ? "fr-FR" : "en-US";
    u.rate = 1; u.pitch = 1;
    var vs = window.speechSynthesis.getVoices ? window.speechSynthesis.getVoices() : [];
    var want = lang()==="fr" ? "fr" : "en";
    for(var i=0;i<vs.length;i++){
      if((vs[i].lang||"").toLowerCase().indexOf(want)===0){ u.voice = vs[i]; break; }
    }
    window.speechSynthesis.speak(u);
  }

  function ask(text, spoken){
    var q = norm(text), best=null, score=0;
    KB.forEach(function(e){
      var s=0;
      e.k.forEach(function(kw){ if(q.indexOf(norm(kw))>=0) s += (kw.length>=5 ? 2 : 1); });
      if(s>score){ score=s; best=e; }
    });
    var entry = (score>=2) ? best : FALLBACK;
    var a = entry[lang()];
    current = text;
    you.textContent = "\\u201C" + text + "\\u201D";
    ansEl.textContent = a;
    out.hidden = false;
    wa.href = "https://wa.me/" + WAN + "?text=" + encodeURIComponent(
      t("Hello AMK! I asked the site a question: ","Bonjour AMK ! J'ai pose une question au site : ")
      + "\\u201C" + text + "\\u201D");
    if(!muted) speak(a);
  }

  function setMic(state, err){
    mic.classList.toggle("on", state==="listening");
    if(state==="listening")      micLabel.textContent = t("Listening\\u2026 tap to stop","Ecoute\\u2026 appuyez pour arreter");
    else if(state==="error")     micLabel.textContent = t("Microphone unavailable \\u2014 use the buttons","Micro indisponible \\u2014 utilisez les boutons");
    else                         micLabel.textContent = t("Tap to speak","Appuyez pour parler");
    if(err) console.warn("[VX] speech:", err);
  }

  if(!SR){
    mic.disabled = true;
    micLabel.textContent = t("Voice not supported in this browser \\u2014 use the buttons","Voix non supportee par ce navigateur \\u2014 utilisez les boutons");
  }

  fab.addEventListener("click", function(){
    var open = panel.hidden;
    panel.hidden = !open;
    fab.setAttribute("aria-expanded", String(open));
    if(open){ renderChips(); }
  });
  document.getElementById("vx-x").addEventListener("click", function(){
    panel.hidden = true; fab.setAttribute("aria-expanded","false");
    if("speechSynthesis" in window){ try{ window.speechSynthesis.cancel(); }catch(e){} }
  });
  document.addEventListener("keydown", function(e){
    if(e.key === "Escape" && !panel.hidden){
      panel.hidden = true; fab.setAttribute("aria-expanded","false");
      if("speechSynthesis" in window){ try{ window.speechSynthesis.cancel(); }catch(e){} }
    }
  });

  muteBtn.addEventListener("click", function(){
    muted = !muted;
    muteBtn.textContent = muted ? t("Unmute voice","Remettre la voix") : t("Mute voice","Couper la voix");
    if(muted && "speechSynthesis" in window){ try{ window.speechSynthesis.cancel(); }catch(e){} }
  });

  mic.addEventListener("click", function(){
    if(!SR) return;
    if(listening){ try{ rec.stop(); }catch(e){} return; }
    if(!rec){
      rec = new SR();
      rec.continuous = false;
      rec.interimResults = false;
      rec.maxAlternatives = 1;
      rec.onresult = function(e){
        var txt = e.results[0][0].transcript;
        ask(txt, true);
      };
      rec.onerror = function(e){ setMic("error", e.error || "error"); };
      rec.onend   = function(){ listening=false; setMic("idle"); };
    }
    rec.lang = lang()==="fr" ? "fr-FR" : "en-US";
    try{ rec.start(); listening=true; setMic("listening"); }
    catch(e){ listening=false; setMic("error", e.message); }
  });

  /* la langue du site change -> on retraduit les puces et on relit les libelles */
  new MutationObserver(function(){
    renderChips();
    if(!listening) setMic("idle");
  }).observe(document.documentElement, {attributes:true, attributeFilter:["lang"]});

  renderChips();
})();
</script>
"""


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    if MARK in src:
        print("déjà injecté — rien à faire")
        return 0

    # 1 · CSS
    anchor = "/* reveal */"
    if anchor not in src:
        print("ERREUR : ancre CSS '/* reveal */' introuvable")
        return 1
    src = src.replace(anchor, CSS.strip() + "\n\n" + anchor, 1)

    # 2 · HTML + JS juste avant </body>
    if "</body>" not in src:
        print("ERREUR : </body> introuvable")
        return 1
    src = src.replace("</body>", HTML.strip() + "\n" + JS + "\n</body>", 1)

    # 3 · formule de lancement dans l'offre fondatrice (prix bilingue, carte Starter)
    m = re.search(r'(<li data-en="Live in 3–5 days"[^>]*>[^<]*</li>)', src)
    if m:
        li = (
            '\n          <li data-en="Optional monthly after launch — 15,000 FCFA (hosting managed + 2 updates/month)"'
            ' data-fr="Mensuel optionnel après lancement — 15 000 FCFA (hébergement suivi + 2 modifications/mois)">'
            'Optional monthly after launch — 15,000 FCFA (hosting managed + 2 updates/month)</li>'
        )
        src = src.replace(m.group(1), m.group(1) + li, 1)
    else:
        print("AVERT : ligne 'Live in 3–5 days' introuvable — carte Starter non modifiée")

    # 4 · FAQ « What happens after launch? » — le mensuel passe de vague à chiffré
    new_en = ("One month of free support, hosting managed, and then — if you want us to handle updates — "
              "15,000 FCFA per month: two updates a month, the site stays online and backed up, no contract, "
              "and your domain and files stay 100% yours.")
    new_fr = ("Un mois de support gratuit, l'hébergement suivi, et ensuite — si vous voulez que nous gérons les "
              "mises à jour — 15 000 FCFA par mois : deux modifications par mois, le site reste en ligne et "
              "sauvegardé, sans engagement, et votre domaine et vos fichiers restent à 100 % à vous.")
    if 'What happens after launch?' in src:
        src = re.sub(r'data-en="One month of free support[^"]*"', 'data-en="%s"' % new_en, src)
        src = re.sub(r'data-fr="Un mois de support gratuit[^"]*"', 'data-fr="%s"' % new_fr, src)
    else:
        print("AVERT : FAQ 'What happens after launch?' introuvable")

    # 5 · JSON-LD : même réponse, pour ne pas avoir deux vérités dans le même fichier
    src = re.sub(r'"text":"One month of free support[^"]*"',
                 '"text":"%s"' % new_en.replace('"', "'"), src)

    TARGET.write_text(src, encoding="utf-8")
    print("OK — couche vocale injectée dans %s (%d Ko)" % (TARGET, len(src) // 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
