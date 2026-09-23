/* Bloc repris TEL QUEL de la version précédente — c'est l'état d'ouverture, la langue, la bande de retour.
   Reproduction :  git show 2d2ffe4:demos/concept-unilabo-v1.html > /tmp/av.html
                   python3 tools/qa/extract_unilabo_js.py /tmp/av.html demos/_unilabo_v2_js_main.js demos/_unilabo_v2_js_form.js
   La refonte n'a pas le droit de toucher à ce contrat : ce sont `tools/qa/test_unilabo_page.mjs`
   (suite 0) et ces deux fichiers qui le garantissent. */
/* Extrait de `demos/concept-unilabo-v1.html` (commit 2d2ffe4), repris SANS MODIFICATION dans la
   refonte v2 : c'est ce JavaScript qui est couvert par les 23 assertions de
   `tools/qa/test_unilabo_page.mjs`. Le contrat d'identifiants ne doit pas bouger. */
(function(){
  var html=document.documentElement, k='unilabo-lang';
  function setLang(l){
    html.setAttribute('data-lang',l); html.lang=l;
    document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
    document.getElementById('btn-en').classList.toggle('is-on',l==='en');
    try{localStorage.setItem(k,l)}catch(e){}
  }
  document.getElementById('btn-fr').addEventListener('click',function(){setLang('fr')});
  document.getElementById('btn-en').addEventListener('click',function(){setLang('en')});
  try{ var saved=localStorage.getItem(k); if(saved) setLang(saved); }catch(e){}

  /* ── L'ÉTAT RÉEL DU LABORATOIRE (23/09 soir) ──────────────────────────────────────────────────────
     La barre du haut portait un point vert décoratif à côté des horaires : à 22 h il annonçait donc
     « ouvert » sans rien savoir. §3.4 interdit les points d'état décoratifs ; celui-ci devient un état
     calculé à l'heure de Douala (UTC+1) — et sans JavaScript il ne s'affiche pas du tout : la page
     retombe sur les horaires écrits, qui eux sont toujours vrais. */
  var barState=document.getElementById('open-state');
  function drawOpen(){
    if(!barState) return;
    var l=(html.getAttribute('data-lang')==='en')?'en':'fr';
    var now=new Date();
    var cm=new Date(now.getTime()+(now.getTimezoneOffset()+60)*60000);
    var d=cm.getDay(), h=cm.getHours()+cm.getMinutes()/60;
    var open=false, closes='', opens='';
    if(d>=1&&d<=5){ open=(h>=7&&h<19); closes='19'; opens=(h<7?'today':'tomorrow'); }
    else if(d===6){ open=(h>=7&&h<13); closes='13'; opens=(h<7?'today':'monday'); }
    else { opens='monday'; }
    var word, extra='';
    if(open){
      word=(l==='en' ? 'Open now, until '+(closes==='19'?'7pm':'1pm')
                     : 'Ouvert maintenant, jusqu\'à '+closes+'h');
    }else{
      extra=' closed';
      var when = opens==='today'    ? (l==='en'?'today at 7am':'aujourd\'hui à 7h')
               : opens==='tomorrow' ? (l==='en'?'tomorrow at 7am':'demain à 7h')
               :                      (l==='en'?'Monday at 7am':'lundi à 7h');
      word=(l==='en'?'Closed, we open ':'Fermé, nous rouvrons ')+when;
    }
    barState.innerHTML='<span class="dot'+extra+'"></span><span>'+word+'</span> · ';
  }
  function labelChips(){
    var g=document.querySelector('.chips'); if(!g) return;
    g.setAttribute('aria-label',(html.getAttribute('data-lang')==='en')?'Preparation':'Préparation');
  }
  function labelMedia(){
    [].slice.call(document.querySelectorAll('img[data-alt-fr]')).forEach(function(im){
      im.setAttribute('alt', html.getAttribute('data-lang')==='en'
        ? im.getAttribute('data-alt-en') : im.getAttribute('data-alt-fr'));
    });
  }
  drawOpen(); labelChips(); labelMedia();
  [document.getElementById('btn-fr'),document.getElementById('btn-en')].forEach(function(b){
    if(b) b.addEventListener('click',function(){ drawOpen(); labelChips(); labelMedia(); });
  });

  // preparation chips — one answer at a time, no scrolling required
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  chips.forEach(function(c){
    c.addEventListener('click',function(){
      chips.forEach(function(x){x.classList.remove('is-on')});
      c.classList.add('is-on');
      document.querySelectorAll('.prep-panel').forEach(function(p){p.classList.remove('is-on')});
      var t=document.getElementById('prep-'+c.dataset.prep);
      if(t) t.classList.add('is-on');
      // l'état du choix existe aussi pour qui n'a pas d'yeux dessus (lecteur d'écran)
      chips.forEach(function(x){ x.setAttribute('aria-pressed', x===c ? 'true' : 'false'); });
    });
  });

  /* ── LA RÉPONSE APRÈS LE CLIC (ajouté le 23/09) ────────────────────────────────────────────────────
     Avant ce patch, un clic sur WhatsApp ouvrait un onglet et LA PAGE NE DISAIT RIEN. Sur un téléphone,
     l'onglet prend l'écran, l'utilisateur revient au site : rien n'indique que son message est déjà
     écrit, ni quand le laboratoire répond. C'est le trou que les deux vidéos UX nomment — « chaque
     interaction doit produire une réponse » et « le plus dur de la livraison, c'est l'attente ». */
  var said=document.getElementById('wa-said'), bar=document.querySelector('[data-wa-bar]');
  var saidTimer=null;
  function say(what){
    if(!said) return;
    var l=(document.documentElement.getAttribute('data-lang')==='en') ? 'en' : 'fr';
    var t=(l==='en')
      ? (what==='call' ? "Your phone app opens with the lab number."
                       : "WhatsApp opens with your message already written.")
      : (what==='call' ? "Votre application téléphone s'ouvre avec le numéro du laboratoire."
                       : "WhatsApp s'ouvre avec votre message déjà écrit.");
    t += (l==='en') ? " Opening hours: Mon-Fri 7am-7pm, Sat 7am-1pm."
                    : " Heures d'ouverture : Lun-Ven 7h-19h, Sam 7h-13h.";
    said.textContent=t;
    said.hidden=false; said.classList.add('on');
    if(saidTimer) clearTimeout(saidTimer);
    saidTimer=setTimeout(function(){ said.hidden=true; said.classList.remove('on'); }, 6000);
  }
  [].slice.call(document.querySelectorAll('a[href]')).forEach(function(a){
    var h=a.getAttribute('href')||'';
    if(h.indexOf('https://wa.me/')===0 || h.indexOf('tel:')===0){
      a.addEventListener('click',function(){ say(h.indexOf('tel:')===0 ? 'call' : 'wa'); });
    }
  });
})();
