/* Bloc repris TEL QUEL de la version précédente — c'est le formulaire, la fiche vivante, le refus expliqué.
   Reproduction :  git show 2d2ffe4:demos/concept-unilabo-v1.html > /tmp/av.html
                   python3 tools/qa/extract_unilabo_js.py /tmp/av.html demos/_unilabo_v2_js_main.js demos/_unilabo_v2_js_form.js
   La refonte n'a pas le droit de toucher à ce contrat : ce sont `tools/qa/test_unilabo_page.mjs`
   (suite 0) et ces deux fichiers qui le garantissent. */
/* Extrait de `demos/concept-unilabo-v1.html` (commit 2d2ffe4), repris SANS MODIFICATION dans la
   refonte v2. La fiche vivante, les consignes déduites des textes du laboratoire, le refus
   expliqué : tout est ici, et `tools/qa/test_unilabo_page.mjs` le rejoue. */
/* ── LA FICHE VIVANTE (23/09, soir) ───────────────────────────────────────────────────────────────
   Le formulaire ne fait pas que composer un message : il ÉCRIT LA FICHE sous les yeux du visiteur, et
   la ligne « Préparation » se déduit des consignes que le laboratoire publie déjà lui-même. Rien n'est
   inventé : chaque phrase de `PREP` résume un panneau de la section « Avant de venir », et l'absence de
   consigne est DITE (« pas de consigne particulière publiée ») au lieu d'être comblée.
   Aucun envoi réseau depuis cette page : on remplit le lien `wa.me` déjà présent dans le HTML, que le
   visiteur ouvre lui-même. Le bloc se protège : une erreur ici ne peut pas casser la langue, les
   puces ni la bande de retour — l'ancre garde son href générique. */
(function(){
  try{
  var form=document.getElementById('rdv'); if(!form) return;
  var go=document.getElementById('rdv-go');
  var said=document.getElementById('rdv-said');
  var NUM='237696139819';
  var GENERIC='https://wa.me/'+NUM+'?text='+encodeURIComponent(
    'Bonjour UNI-LABO, je souhaite prendre rendez-vous.');
  var timer=null;
  function lg(){ return document.documentElement.getAttribute('data-lang')==='en' ? 'en' : 'fr'; }
  function set(id, value, empty){
    var el=document.getElementById(id); if(!el) return;
    el.textContent=value;
    if(empty) el.classList.add('is-empty'); else el.classList.remove('is-empty');
  }
  /* LES CONSIGNES — résumés fidèles des panneaux publiés par le laboratoire */
  var PREP={
    jeun:{fr:"À jeun 8 à 12 h, l'eau est permise",en:"Fasting 8 to 12 h, water allowed"},
    urines:{fr:"Recueil au laboratoire, flacon remis sur place",en:"Collected at the laboratory, container given on site"},
    hormones:{fr:"Souvent le matin, parfois un jour précis du cycle",en:"Often in the morning, sometimes a specific cycle day"},
    enfant:{fr:"Précisez l'âge à l'accueil",en:"Tell us the age at reception"},
    suivi:{fr:"Apportez le résultat précédent",en:"Bring the previous result"},
    ordonnance:{fr:"Apportez l'ordonnance (ou une photo nette)",en:"Bring the prescription (or a clear photo)"},
    autre:{fr:"Nous vous confirmons la consigne par message",en:"We confirm the instruction by message"}
  };
  var ORDER=['jeun','urines','hormones','enfant','suivi','ordonnance','autre'];
  function build(){
    var l=lg();
    var picked=[].slice.call(form.querySelectorAll('input[type=checkbox]:checked'));
    var tests=picked.map(function(c){ return c.getAttribute('data-'+l) || c.value; });
    var nomEl=form.querySelector('#rdv-nom'), noteEl=form.querySelector('#rdv-note');
    var nom=(nomEl && nomEl.value || '').replace(/\s+/g,' ').trim();
    var note=(noteEl && noteEl.value || '').replace(/\s+/g,' ').trim();
    var m=form.querySelector('input[name="moment"]:checked');
    var moment=m ? (m.getAttribute('data-'+l) || m.value) : '';
    var keys=[];
    picked.forEach(function(c){ var p=c.getAttribute('data-prep'); if(p && PREP[p] && keys.indexOf(p)<0) keys.push(p); });
    keys.sort(function(a,b){ return ORDER.indexOf(a)-ORDER.indexOf(b); });
    var prep;
    if(keys.length) prep=keys.slice(0,2).map(function(p){ return PREP[p][l]; }).join(' · ');
    else prep = tests.length
      ? (l==='en' ? 'No particular preparation stated: we confirm by message'
                  : 'Pas de consigne particulière publiée : nous confirmons par message')
      : '';
    var ok = tests.length>0 && nom.length>=2 && moment!=='';
    var L = l==='en'
      ? ['Hello UNI-LABO, I would like to book a visit.','Name: ','Tests: ','Preferred time: ','Preparation: ','Anything else: ','(Sent from your website.)']
      : ['Bonjour UNI-LABO, je souhaite prendre rendez-vous.','Nom : ','Analyses : ','Moment souhaité : ','Préparation : ','Précision : ','(Envoyé depuis votre site.)'];
    var msg=L[0];
    if(nom) msg+='\n'+L[1]+nom;
    if(tests.length) msg+='\n'+L[2]+tests.join(', ');
    if(moment) msg+='\n'+L[3]+moment;
    if(prep) msg+='\n'+L[4]+prep;
    if(note) msg+='\n'+L[5]+note;
    msg+='\n'+L[6];
    return {ok:ok, url:'https://wa.me/'+NUM+'?text='+encodeURIComponent(msg),
            need:{tests:tests.length===0, nom:nom.length<2, moment:moment===''},
            nom:nom, tests:tests, moment:moment, prep:prep, l:l};
  }
  /* LA FICHE — le miroir du formulaire. Elle n'est pas annoncée à chaque case cochée (bavardage) : la
     bande `.rdv-said` parle quand il y a vraiment quelque chose à dire. */
  function paintFiche(r){
    var l=r.l;
    set('fiche-nom', r.nom || '—', !r.nom);
    set('fiche-tests', r.tests.length ? r.tests.join(' · ') : '—', !r.tests.length);
    set('fiche-prep', r.prep || '—', !r.prep);
    set('fiche-moment', r.moment || '—', !r.moment);
    var tag=document.getElementById('fiche-state');
    if(tag){
      tag.textContent = r.ok ? (l==='en'?'ready to send':'prête à envoyer')
                             : (l==='en'?'to fill in':'à compléter');
      if(r.ok) tag.classList.add('is-ready'); else tag.classList.remove('is-ready');
    }
    var foot=document.getElementById('fiche-foot');
    if(foot) foot.textContent = r.ok
      ? (l==='en' ? 'This is exactly what leaves on WhatsApp when you press the button.'
                  : 'C\'est exactement ce qui part sur WhatsApp quand vous appuyez sur le bouton.')
      : (l==='en' ? 'Tick your tests: this sheet fills in as you go, then leaves on WhatsApp.'
                  : 'Cochez vos analyses : cette fiche se remplit sous vos yeux, puis part sur WhatsApp.');
  }
  /* LE REFUS EXPLIQUÉ — le groupe fautif passe en rouge, le champ porte aria-invalid */
  function paintErr(need, on){
    var map={tests:'#rdv-g1', nom:'#rdv-g2', moment:'#rdv-g3'};
    Object.keys(map).forEach(function(k){
      var g=document.querySelector(map[k]); if(!g) return;
      if(on && need && need[k]) g.classList.add('is-err'); else g.classList.remove('is-err');
    });
    var bad = (on && need) ? need : {};
    var n1=document.querySelector('#rdv-nom');
    if(n1) n1.setAttribute('aria-invalid', bad.nom ? 'true' : 'false');
    var rd=form.querySelector('input[name="moment"]');
    if(rd) rd.setAttribute('aria-invalid', bad.moment ? 'true' : 'false');
    var cb=form.querySelector('input[type=checkbox]');
    if(cb) cb.setAttribute('aria-invalid', bad.tests ? 'true' : 'false');
  }
  function hideSaid(){
    if(!said) return;
    said.hidden=true; said.classList.remove('on');
  }
  function refresh(){
    var r=build();
    go.setAttribute('aria-disabled', r.ok ? 'false' : 'true');
    /* incomplet : le lien garde le message générique — un clic droit ne peut pas envoyer un brouillon */
    go.setAttribute('href', r.ok ? r.url : GENERIC);
    paintErr(r.need, false);
    paintFiche(r);
    if(r.ok) hideSaid();
  }
  function announce(text){
    if(!said) return;
    said.hidden=false; said.classList.add('on'); said.textContent=text;
    if(timer) clearTimeout(timer);
    timer=setTimeout(hideSaid, 8000);
  }
  ['input','change'].forEach(function(ev){ form.addEventListener(ev, refresh); });
  refresh();
  /* L'ancre a une URL RÉELLE dans le HTML : sans JavaScript elle ouvre déjà WhatsApp avec le message
     générique. Avec JavaScript elle fait mieux, et si la demande est incomplète elle refuse en disant
     pourquoi — au lieu d'envoyer un message à moitié vide au laboratoire. */
  go.addEventListener('click',function(e){
    var r=build();
    if(r.ok) return;
    e.preventDefault();
    paintErr(r.need, true);
    announce(lg()==='en' ? 'Tick at least one test, write your name and choose a time.'
                         : 'Cochez au moins une analyse, écrivez votre nom et choisissez un moment.');
  });
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var r=build();
    if(r.ok) window.location.href=r.url;
  });
  ['btn-fr','btn-en'].forEach(function(id){
    var b=document.getElementById(id);
    if(b) b.addEventListener('click',function(){ setTimeout(refresh,0); });
  });
  }catch(err){ /* la page reste utilisable : l'ancre garde son href générique */ }
})();
