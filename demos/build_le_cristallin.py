#!/usr/bin/env python3
"""
AMK — LE CRISTALLIN · concept builder (v1) — « PLANCHE D'ACUITÉ »

Le prospect a RÉPONDU (« Ok », 21/09 17:53) et a envoyé son flyer + une note vocale. Il a déjà un site
(lecristallinoptique.com, vérifié en ligne le 21/09). Ceci n'est donc PAS un concept « vous êtes
introuvable » : c'est une MODERNISATION du site qu'il possède, avec SES faits, pris sur son site et son flyer.

AUCUN prix inventé (le sien n'en affiche pas) · AUCUN avis inventé · AUCUNE photo volée aux marques :
les trois cadres photo sont dessinés en SVG et étiquetés « à remplacer par vos photos ».

LOI MAISON : toute la copie vit dans `demos/le_cristallin_content.json` (FR|EN par paire), et le gabarit
ci-dessous ne contient que des jetons. Un run FR existe toujours pour chaque run EN — la règle §13.

Direction (voir clients/le-cristallin/build-notes.md) :
  VARIANCE 6 · MOTION 4 · DENSITY 4  ·  single file  ·  mobile-first  ·  WhatsApp-first  ·  FR|EN

Sortie : demos/concept-le-cristallin-v1.html   (aucune dépendance : ni PIL, ni réseau)
"""
import json, re, urllib.parse
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "demos" / "concept-le-cristallin-v1.html"
C = json.loads((ROOT / "demos" / "le_cristallin_content.json").read_text(encoding="utf-8"))
# ⚠️ Le jeton @@WA@@ atterrit dans un href : un numéro écrit « 699 90 55 77 » (avec ses espaces,
#   comme le publie le flyer) y casse l'URL APRÈS l'espace — le lien s'ouvre sur wa.me/699 et le
#   message pré-rempli disparaît. Le numéro CANONIQUE est donc les chiffres seuls ; l'affichage,
#   lui, garde les espaces (c'est ce que lit un humain). Les deux viennent du même champ JSON.
WA = re.sub(r"\D", "", C["wa"])
assert len(WA) == 9 and WA.startswith("6"), f"numéro WhatsApp invalide : {WA!r}"


def L(pair, index=0):
    """Une paire FR|EN -> deux spans. `pair` = [fr, en] ou {fr:, en:}."""
    if isinstance(pair, dict):
        fr, en = pair["fr"], pair["en"]
    else:
        fr, en = pair[0], pair[1]
    return f'<span class="fr-only">{fr}</span><span class="en-only">{en}</span>'


def T(pair, index=0):
    """Texte brut pour un attribut (aria-label, title) : la version FR, l'EN reste en data-."""
    return pair["fr"] if isinstance(pair, dict) else pair[0]


# ─────────────────────────────────────────────── planche d'acuité (hero)
chart_rows = []
for g, fr_t, en_t, fr_d, en_d in C["chart"]:
    chart_rows.append(
        f'''      <a class="row" href="#contact" data-svc-fr="{fr_t}" data-svc-en="{en_t}">
        <span class="g" aria-hidden="true">{g}</span>
        <span class="t"><b>{L([fr_t, en_t])}</b><em>{L([fr_d, en_d])}</em></span>
        <span class="v">{L(C["book"])}</span>
      </a>''')
CHART_ROWS = "\n".join(chart_rows)

# ─────────────────────────────────────────────── tableau des services
svc_rows = []
for fr_t, en_t, fr_d, en_d, who in C["services"]["rows"]:
    wf, we = C["services"]["who"][who]
    svc_rows.append(
        f'''      <div class="srow">
        <span><b>{L([fr_t, en_t])}</b><small>{L([fr_d, en_d])}</small></span>
        <span class="who">{L([wf, we])}</span>
        <a class="ask" href="#contact" data-svc-fr="{fr_t}" data-svc-en="{en_t}">{L(C["services"]["ask"])}</a>
      </div>''')
SVC_ROWS = "\n".join(svc_rows)

# ─────────────────────────────────────────────── les trois portes (asymétriques)
doors = []
for k, hfr, hen, pfr, pen, gfr, gen, href in C["doors"]["items"]:
    doors.append(
        f'''      <a class="door reveal" href="{href}">
        <span class="k">{k}</span>
        <h3>{L([hfr, hen])}</h3>
        <p>{L([pfr, pen])}</p>
        <span class="go">{L([gfr, gen])}<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11h10.2l-4.1-4.1L11.6 5 20 13.4 11.6 21.8l-1.5-1.9 4.1-4.1H4z"/></svg></span>
      </a>''')
DOORS = "\n".join(doors)

# ─────────────────────────────────────────────── preuves
tiles = []
for mono, big, pfr, pen, nfr, nen in C["proof"]["tiles"]:
    note = ""
    if nfr:
        note = f'<p class="note">{L([nfr, nen])}</p>'
    tiles.append(
        f'''      <div class="tile reveal">
        <span class="mono">{mono}</span>
        <b>{big}</b>
        <p>{L([pfr, pen])}</p>
        {note}
      </div>''')
TILES = "\n".join(tiles)

# les partenaires sont rendus en BANDEAU TEXTE, pas en logos : aucun visuel de marque volé,
# et rien à faire payer en droits. Le propriétaire posera ses propres logos s'il le souhaite.

# ─────────────────────────────────────────────── cadres photo dessinés
ART = {
    "store": '<svg viewBox="0 0 120 60" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 52h108M14 52V22l14-12 14 12v30M42 30h14v10H42zM64 52V28l16-8 16 8v24M70 38h10v8H70z"/></svg>',
    "lab": '<svg viewBox="0 0 120 60" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="34" cy="34" r="15"/><circle cx="86" cy="34" r="15"/><path d="M49 34h22M19 27 8 22M101 27l11-5M34 19v-9M86 19v-9"/></svg>',
    "face": '<svg viewBox="0 0 120 60" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><ellipse cx="60" cy="30" rx="30" ry="21"/><path d="M30 26c8-6 18-8 30-8s22 2 30 8"/><circle cx="50" cy="30" r="4"/><circle cx="70" cy="30" r="4"/></svg>',
}
frames = []
for hfr, hen, cfr, cen, kind in C["photos"]["items"]:
    frames.append(
        f'''      <figure class="ph reveal">
        <div class="art">{ART[kind]}</div>
        <figcaption><b>{L([hfr, hen])}</b> · {L([cfr, cen])}</figcaption>
      </figure>''')
FRAMES = "\n".join(frames)

# ─────────────────────────────────────────────── FAQ
faqs = []
for i, (qfr, qen, afr, aen) in enumerate(C["offerfaq"]["faq"]):
    op = " open" if i == 0 else ""
    faqs.append(
        f'''      <details{op}>
        <summary>{L([qfr, qen])}<span class="pm" aria-hidden="true">+</span></summary>
        <p>{L([afr, aen])}</p>
      </details>''')
FAQS = "\n".join(faqs)

# ─────────────────────────────────────────────── assureurs
INS_OPTS = "\n".join(f'        <option value="{i}">{n}</option>'
                     for i, n in enumerate(C.get("insurers", []), 1))
INS_LIST = "\n".join(f"<li>{n}</li>" for n in C.get("insurers", []))
INS_JS = json.dumps(C.get("insurers", []), ensure_ascii=False)

PARTNER_NAMES = " · ".join(n for n, c in C.get("partners", []))

# ─────────────────────────────────────────────── horaires
hours_rows = "\n".join(
    f'        <tr><td>{L([hf, he])}</td><td>{L([vfr, ven])}</td></tr>'
    for hf, he, vfr, ven in C["contact"]["hours"])

# ─────────────────────────────────────────────── nav + footer
NAV = "\n".join(f'      <a href="{h}">{L([fr, en])}</a>' for h, fr, en in C["nav"])


def fcol(block):
    # Un bloc du pied de page. La liste « avant de publier » est grisée : consigne de travail
    # pour le propriétaire, pas un menu client.
    head, links = block
    li = "\n".join('        <li><a href="%s">%s</a></li>' % (h, L([fr, en])) for h, fr, en in links)
    cls = ' class="fine"' if "publier" in head["fr"] else ""
    parts = ['      <div>', '        <h4>' + L(head) + '</h4>', '        <ul' + cls + '>', li,
              '        </ul>', '      </div>']
    return "\n".join(parts)


FOOT_COLS = "\n".join(fcol(b) for b in C["footer"]["cols"])

FACTS = "\n".join(
    f'      <span class="fact"><b>{f[0]}</b> {L([f[1], f[2]])}</span>' if f[0] != "Laboratoire"
    else f'      <span class="fact"><b>{L([f[0], f[2]])}</b> {L([f[1], f[3]])}</span>'
    for f in C["hero"]["facts"])

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@graph": [{
        "@type": "Optician", "@id": "https://lecristallinoptique.com/#org",
        "name": "Le Cristallin", "url": "https://lecristallinoptique.com/",
        "email": C["mail"], "telephone": "+237 699 90 55 77", "foundingDate": "2010",
        "areaServed": "Douala, Cameroun", "memberOf":
        "Ordre National des Opticiens-Lunetiers du Cameroun (ONOC)",
        "address": {"@type": "PostalAddress",
                    "streetAddress": "Akwa, carrefour Ancien Dalip, à côté de l'immeuble FODEC, face COMECI SA",
                    "addressLocality": "Douala", "postalCode": "BP 566", "addressCountry": "CM"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "08:30", "closes": "18:30"}],
        "hasMap": "https://www.google.com/maps/search/?api=1&query=Le+Cristallin+optique+Douala",
        "sameAs": ["https://lecristallinoptique.com/"]}]},
    ensure_ascii=False, indent=1)

WA_HERO = ("https://wa.me/" + WA + "?text=" +
           json.loads(json.dumps(C["waMsg"]["row"]["fr"])).replace("{svc}", "un examen de vue").replace(" ", "%20"))

# ────────────────────────────────────────────────────────────────── CSS
CSS = """
:root{
 --paper:#EFF2F1;--card:#FFFFFF;--ink:#101E19;--txt:#1B2A24;--mute:#586A62;--line:#D5DDD8;
 --lineS:#E4EAE6;--deep:#0D5A41;--deepD:#0A4634;--bright:#7FE0BC;--dark:#0B1613;--tint:#E2EDE6;
 --max:1220px;--r:14px;
 --disp:"Archivo","Helvetica Neue",Arial,sans-serif;
 --body:"Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
 --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--txt);font-family:var(--body);font-size:1rem;
 line-height:1.56;text-rendering:optimizeLegibility}
img,svg{max-width:100%}
h1,h2,h3,h4{font-family:var(--disp);color:var(--ink);margin:0;letter-spacing:-.022em;line-height:1.06;
 text-wrap:balance}
h1{font-size:clamp(2.05rem,6.4vw,3.5rem);font-weight:700}
h2{font-size:clamp(1.5rem,3.7vw,2.15rem);font-weight:650}
h3{font-size:1.14rem;font-weight:620;letter-spacing:-.01em}
h4{font-size:1rem;font-weight:620}
p{margin:0 0 .9em}
.lede{font-size:1.05rem;color:var(--txt);max-width:54ch}
.mono{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase}
.wrap{max-width:var(--max);margin:0 auto;padding:0 18px}
section{padding:54px 0}
a{color:var(--deep)}
.eyebrow{color:var(--deep);font-weight:600;font-size:.76rem;letter-spacing:.11em;text-transform:uppercase;
 margin-bottom:12px}
.hair{border-top:1px solid var(--line)}
html[data-lang=fr] .en-only{display:none!important}
html[data-lang=en] .fr-only{display:none!important}
html[data-lang=en] .en-only{display:revert!important}
html[data-lang=fr] .fr-only{display:revert!important}
:is(a,button,select,summary):focus-visible{outline:3px solid var(--deep);outline-offset:2px;border-radius:8px}
::selection{background:var(--bright);color:var(--ink)}
.bar{background:var(--dark);color:#D7E4DC;font-size:.8rem}
.bar .wrap{display:flex;gap:14px;justify-content:space-between;align-items:center;padding:9px 18px;
 flex-wrap:wrap}
.bar b{color:#fff;font-weight:600}
.bar a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.34)}
.bar a:hover{border-color:var(--bright)}
.bar .sep{color:#8FA79C}
.bar .warn{color:var(--bright)}
.dotlive{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--bright);
 margin-right:7px;vertical-align:1px}
.nav{position:sticky;top:0;z-index:40;background:rgba(239,242,241,.93);backdrop-filter:blur(10px);
 border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:14px;padding:11px 18px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}
.brand svg{flex:0 0 auto;display:block}
.brand b{font-family:var(--disp);font-size:1.04rem;letter-spacing:-.015em;color:var(--ink);display:block;
 line-height:1.05;font-weight:700}
.brand .sub{display:block;font-size:.67rem;color:var(--mute);letter-spacing:.07em;text-transform:uppercase;
 font-family:var(--mono)}
.nav nav{margin-left:auto;display:none;gap:20px;font-size:.9rem}
.nav nav a{text-decoration:none;color:var(--txt);opacity:.9}
.lang{display:flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:var(--card);
 margin-left:auto}
.nav nav+.lang{margin-left:0}
.lang button{border:0;background:transparent;padding:7px 12px;font:600 .78rem/1 var(--body);color:var(--mute);
 cursor:pointer;transition:background .16s ease,color .16s ease}
.lang button:active{transform:scale(.97)}
.lang button.is-on{background:var(--deep);color:#fff}
.cta{background:var(--deep);color:#fff;text-decoration:none;padding:10px 15px;border-radius:999px;
 font-weight:600;font-size:.86rem;white-space:nowrap;display:inline-flex;align-items:center;gap:8px;
 transition:background .16s ease,transform .12s ease}
.cta:hover{background:var(--deepD)}
.cta:active{transform:scale(.97)}
.cta svg{width:16px;height:16px;fill:currentColor}
.cta.small{display:none}
.hero{padding:38px 0 46px;background:linear-gradient(180deg,var(--card) 0%,var(--paper) 78%)}
.hero .grid{display:grid;gap:26px;align-items:start}
.chart{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.chart-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:13px 16px;
 border-bottom:1px solid var(--line);background:var(--tint)}
.chart-top .mono{color:var(--deep)}
.chart-top .acuity{font-family:var(--disp);font-weight:700;color:var(--ink);font-size:.92rem;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:center;padding:13px 16px;
 border-bottom:1px solid var(--lineS);text-decoration:none;color:inherit;transition:background .18s ease}
.row:last-of-type{border-bottom:0}
.row .g{font-family:var(--disp);font-weight:700;color:var(--ink);letter-spacing:.06em;line-height:1;
 font-variant-numeric:tabular-nums;white-space:nowrap}
.row:nth-of-type(1) .g{font-size:2.3rem}
.row:nth-of-type(2) .g{font-size:1.75rem}
.row:nth-of-type(3) .g{font-size:1.4rem}
.row:nth-of-type(4) .g{font-size:1.16rem}
.row:nth-of-type(5) .g{font-size:1rem;color:var(--mute)}
.row .t{font-size:.94rem;color:var(--txt)}
.row .t b{font-weight:620;font-family:var(--disp)}
.row .t em{display:block;font-style:normal;font-size:.78rem;color:var(--mute);margin-top:2px}
.row .v{font-family:var(--mono);font-size:.68rem;color:var(--deep);border:1px solid var(--line);
 border-radius:999px;padding:4px 8px;white-space:nowrap;transition:background .18s ease,color .18s ease}
.row-foot{padding:12px 16px;border-top:1px solid var(--line);font-size:.78rem;color:var(--mute)}
.h1hl{color:var(--deep)}
.actions{display:flex;gap:11px;flex-wrap:wrap;margin-top:20px}
.btn{display:inline-flex;align-items:center;gap:9px;padding:13px 18px;border-radius:12px;text-decoration:none;
 font-weight:620;border:1px solid transparent;cursor:pointer;font-size:.94rem;
 transition:background .16s ease,color .16s ease,transform .12s ease,border-color .16s ease}
.btn svg{width:18px;height:18px;fill:currentColor}
.btn:active{transform:scale(.97)}
.btn-primary{background:var(--deep);color:#fff}
.btn-primary:hover{background:var(--deepD)}
.btn-ghost{background:var(--card);color:var(--ink);border-color:var(--line)}
.btn-ghost:hover{border-color:var(--deep);color:var(--deep)}
.facts{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}
.fact{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 13px;font-size:.8rem;
 color:var(--txt)}
.fact b{font-family:var(--disp);color:var(--ink);font-variant-numeric:tabular-nums}
.doors{display:grid;gap:14px}
.door{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px 18px;
 text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:8px;
 transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.door .k{font-family:var(--mono);font-size:.68rem;color:var(--deep);letter-spacing:.12em}
.door h3{margin:0}
.door p{font-size:.9rem;color:var(--mute);margin:0}
.door .go{margin-top:auto;font-weight:620;font-size:.88rem;color:var(--deep);display:flex;align-items:center;
 gap:7px}
.door .go svg{width:14px;height:14px;fill:currentColor;transition:transform .2s ease}
.svc{border:1px solid var(--line);border-radius:var(--r);background:var(--card);overflow:hidden}
.svc .h,.srow{display:grid;grid-template-columns:1.6fr 1.05fr auto;gap:16px;align-items:center;
 padding:12px 16px}
.svc .h{background:var(--tint);border-bottom:1px solid var(--line)}
.svc .h span{font-family:var(--mono);font-size:.67rem;letter-spacing:.11em;text-transform:uppercase;
 color:var(--deep)}
.srow{border-bottom:1px solid var(--lineS);transition:background .18s ease}
.srow:last-child{border-bottom:0}
.srow b{font-family:var(--disp);font-weight:620;color:var(--ink);font-size:.98rem;display:block}
.srow small{display:block;color:var(--mute);font-size:.83rem;margin-top:3px}
.srow .who{font-size:.76rem;color:var(--txt);background:var(--tint);border-radius:999px;padding:5px 10px;
 display:inline-block;justify-self:start}
.srow .ask{font-size:.82rem;font-weight:600;color:var(--deep);text-decoration:none;white-space:nowrap;
 border-bottom:1px solid transparent;transition:border-color .16s ease}
.cover{display:grid;gap:22px;align-items:start}
.picker{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px}
.picker label{display:block;font-family:var(--mono);font-size:.68rem;letter-spacing:.11em;
 text-transform:uppercase;color:var(--deep);margin-bottom:8px}
.picker select{width:100%;font:1rem var(--body);color:var(--ink);background:var(--paper);
 border:1px solid var(--line);border-radius:10px;padding:12px 34px 12px 13px;margin-bottom:13px;
 -webkit-appearance:none;appearance:none;background-image:linear-gradient(45deg,transparent 49%,#0D5A41 50%),
 linear-gradient(-45deg,transparent 49%,#0D5A41 50%);background-size:9px 9px;
 background-position:right 15px center;background-repeat:no-repeat}
.picker .state{font-size:.9rem;color:var(--txt);margin-bottom:13px;min-height:2.7em}
.picker .state b{color:var(--ink)}
.fine{font-size:.79rem;color:var(--mute);margin:12px 0 0}
.listcard{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px}
.listcard .k{font-family:var(--mono);font-size:.67rem;letter-spacing:.11em;text-transform:uppercase;
 color:var(--deep)}
.listcard ul{margin:10px 0 0;padding:0;list-style:none;columns:2;column-gap:26px}
.listcard li{break-inside:avoid;font-size:.9rem;padding:6px 0;border-bottom:1px solid var(--lineS);
 color:var(--txt)}
.listcard li:last-child,.listcard li:nth-last-child(2){border-bottom:0}
.quote{font-size:.86rem;color:var(--mute);margin-top:14px;border-left:2px solid var(--deep);padding-left:12px}
.proof{background:var(--dark);color:#D7E4DC;padding:52px 0}
.proof h2,.proof h3{color:#fff}
.proof .lede{color:#BFD2C8}
.proof .eyebrow,.proof .eyebrow .fr-only,.proof .eyebrow .en-only{color:var(--bright)}
.proof .tile .mono,.proof .band b{color:var(--bright)}
.tiles{display:grid;gap:14px;margin-top:24px}
.tile{border:1px solid rgba(127,224,188,.22);border-radius:var(--r);padding:18px;background:rgba(255,255,255,.03)}
.tile .mono{color:var(--bright);display:block;margin-bottom:8px}
.tile b{font-family:var(--disp);color:#fff;font-size:1.5rem;display:block;letter-spacing:-.02em;
 font-variant-numeric:tabular-nums}
.tile p{font-size:.88rem;margin:8px 0 0;color:#BFD2C8}
.tile .note{font-size:.76rem;color:#9FB6AB;margin-top:9px}
.band{margin-top:22px;font-size:.86rem;color:#9FB6AB}
.band b{color:#fff;font-weight:600}
.frames{display:grid;gap:14px;margin-top:20px}
.ph{border:1px dashed var(--line);border-radius:var(--r);background:var(--card);overflow:hidden;margin:0}
.ph .art{aspect-ratio:16/10;display:grid;place-items:center;
 background:repeating-linear-gradient(135deg,#F3F7F5 0 12px,#EEF3F0 12px 24px)}
.ph .art svg{width:58%;height:auto;color:var(--deep);opacity:.6}
.ph figcaption{padding:12px 14px;border-top:1px solid var(--lineS);font-size:.83rem;color:var(--mute)}
.ph figcaption b{color:var(--ink);font-weight:620}
.two{display:grid;gap:16px}
.offer{background:var(--tint);border:1px solid var(--line);border-radius:var(--r);padding:22px}
.offer h3{margin-bottom:8px}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:0 16px}
details+details{margin-top:9px}
summary{cursor:pointer;padding:14px 0;font:620 .95rem/1.3 var(--disp);color:var(--ink);list-style:none;
 display:flex;justify-content:space-between;gap:14px;align-items:center}
summary::-webkit-details-marker{display:none}
summary .pm{font-family:var(--mono);color:var(--deep);font-size:1.05rem;flex:0 0 auto;transition:transform .2s ease}
details[open] summary .pm{transform:rotate(45deg)}
details p{font-size:.9rem;color:var(--txt);margin:0 0 15px;max-width:70ch}
.info{display:grid;gap:14px;margin-top:20px}
.icard{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:20px}
.icard h3{margin-bottom:10px}
.icard table{width:100%;border-collapse:collapse;font-size:.92rem}
.icard td{padding:7px 0;border-bottom:1px solid var(--lineS);vertical-align:top;color:var(--txt)}
.icard tr:last-child td{border-bottom:0}
.icard td:last-child{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink);
 font-family:var(--disp);font-weight:600}
.icard a{text-decoration:none;border-bottom:1px solid var(--line)}
.icard a:hover{border-color:var(--deep)}
.flag{display:inline-block;font-size:.76rem;background:var(--tint);color:var(--deep);border-radius:999px;
 padding:5px 10px;margin-top:10px}
footer{background:var(--dark);color:#C6D7CD;padding:38px 0 96px;font-size:.88rem}
footer h4{color:#fff;margin-bottom:11px}
footer a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.28)}
footer ul{list-style:none;margin:0;padding:0}
footer li{padding:4px 0}
footer .cols{display:grid;gap:24px}
footer ul.fine li{font-size:.84rem;color:#9FB6AB}
footer ul.fine a{color:#C6D7CD}
.strip{margin-top:28px;padding-top:16px;border-top:1px solid rgba(255,255,255,.14);display:flex;gap:12px;
 justify-content:space-between;flex-wrap:wrap;font-size:.78rem;color:#9FB6AB}
.badge{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--bright);
 border:1px solid rgba(127,224,188,.3);border-radius:999px;padding:5px 10px;display:inline-block;margin-top:6px}
.sticky-wa{position:fixed;inset:auto 0 0 0;z-index:50;display:flex;gap:9px;padding:10px 12px;
 background:rgba(11,22,19,.95);backdrop-filter:blur(8px)}
.sticky-wa a{flex:1;text-align:center;text-decoration:none;font-weight:620;font-size:.9rem;padding:12px;
 border-radius:11px}
.sticky-wa .p{background:var(--bright);color:var(--ink)}
.sticky-wa .c{border:1px solid rgba(255,255,255,.3);color:#fff}
.reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s cubic-bezier(.2,.7,.2,1)}
.reveal.in{opacity:1;transform:none}
@media(min-width:720px){.hero .grid{grid-template-columns:1fr 1fr;gap:34px}}
@media(min-width:900px){
 .doors{grid-template-columns:1.15fr 1fr}
 .door:nth-child(3){grid-column:1/-1;flex-direction:row;align-items:center;gap:26px}
 .door:nth-child(3) .go{margin-top:0;margin-left:auto}
 .door:nth-child(3) p{max-width:64ch}
 .tiles{grid-template-columns:1.25fr 1fr 1fr;align-items:end}
 .frames{grid-template-columns:1.4fr 1fr 1fr}
 .two{grid-template-columns:1fr 1.25fr;align-items:start}
 .cover{grid-template-columns:1fr 1fr}
 .info{grid-template-columns:1fr 1.1fr 1.1fr}
 footer .cols{grid-template-columns:1.4fr 1fr 1fr 1.15fr}
 footer{padding-bottom:34px}
 .sticky-wa{display:none}
 .nav nav{display:flex}
 .cta.small{display:inline-flex}}
@media(hover:hover) and (pointer:fine){
 .row:hover{background:var(--tint)}
 .row:hover .v{background:var(--deep);color:#fff;border-color:var(--deep)}
 .door:hover{border-color:var(--deep);transform:translateY(-2px);box-shadow:0 6px 22px rgba(16,30,25,.07)}
 .door:hover .go svg{transform:translateX(3px)}
 .srow:hover{background:#F6FAF7}
 .srow .ask:hover{border-color:var(--deep)}
 .nav nav a:hover{color:var(--deep);opacity:1}}
@media(max-width:719px){
 .svc .h{display:none}
 .srow{grid-template-columns:1fr;gap:7px;padding:15px 16px}
 .listcard ul{columns:1}
 .row{grid-template-columns:auto 1fr;gap:12px}
 .row .v{grid-column:2;justify-self:start}}
@media (prefers-reduced-motion:reduce){
 html{scroll-behavior:auto}
 *{transition:none!important;animation:none!important}
 .reveal{opacity:1;transform:none}}
"""

JS = """
(function(){
  var html=document.documentElement, KEY='cristallin-lang', WA='__WA__';
  var MSG=__WAJS__;
  function lang(){return html.getAttribute('data-lang')||'fr';}
  function setLang(l){
    html.setAttribute('data-lang',l); html.lang=l;
    document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
    document.getElementById('btn-en').classList.toggle('is-on',l==='en');
    try{localStorage.setItem(KEY,l)}catch(e){}
    paint();
    paintHero();
  }
  document.getElementById('btn-fr').addEventListener('click',function(){setLang('fr')});
  document.getElementById('btn-en').addEventListener('click',function(){setLang('en')});
  try{var s=localStorage.getItem(KEY); if(s)setLang(s);}catch(e){}

  function msg(kind,svc){
    var l=lang(), t=MSG[kind][l];
    return 'https://wa.me/'+WA+'?text='+encodeURIComponent(t.replace('{svc}',svc).replace('{n}',svc));
  }
  [].slice.call(document.querySelectorAll('.row')).forEach(function(r){
    r.addEventListener('click',function(ev){
      ev.preventDefault();
      var svc=lang()==='fr'?r.dataset.svcFr:r.dataset.svcEn;
      window.open(msg('row',svc),'_blank','noopener');
    });
  });
  [].slice.call(document.querySelectorAll('.ask')).forEach(function(a){
    a.addEventListener('click',function(ev){
      ev.preventDefault();
      var svc=lang()==='fr'?a.dataset.svcFr:a.dataset.svcEn;
      window.open(msg('ask',svc),'_blank','noopener');
    });
  });

  var links=[document.getElementById('wa-hero'), document.getElementById('wa-sticky')].filter(Boolean);
  function paintHero(){ links.forEach(function(a){ a.href = msg('generic'); }); }
  var ins=document.getElementById('ins'), st=document.getElementById('ins-state'),
      go=document.getElementById('ins-go'), NAMES=__NAMES__;
  function paint(){
    if(!ins||!st) return;
    var l=lang(), i=ins.value;
    if(!i){ st.textContent = (l==='fr'? ST_IDLE_FR : ST_IDLE_EN); return; }
    var n=NAMES[+i-1];
    st.innerHTML = '<b>'+n+'</b>' + (l==='fr'? ST_ON_FR : ST_ON_EN);
    go.href = msg('ins', n);
  }
  if(ins) ins.addEventListener('change',paint);
  if(go) go.addEventListener('click',function(ev){ if(!ins.value){ev.preventDefault();ins.focus();} });
  paint();
  paintHero();

  var els=[].slice.call(document.querySelectorAll('.reveal'));
  if(!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches){
    els.forEach(function(e){e.classList.add('in')});
  }else{
    var io=new IntersectionObserver(function(en){
      en.forEach(function(x){ if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);} });
    },{rootMargin:'0px 0px -8% 0px',threshold:.12});
    els.forEach(function(e,i){ e.style.transitionDelay=(Math.min(i,4)*45)+'ms'; io.observe(e); });
  }
})();
""".replace("__WA__", WA).replace("__WAJS__", json.dumps(C["waMsg"], ensure_ascii=False)) \
   .replace("__NAMES__", INS_JS) \
   .replace("ST_IDLE_FR", json.dumps(C["cover"]["idle"]["fr"], ensure_ascii=False)[1:-1]).encode().decode() \
   .replace("ST_IDLE_EN", json.dumps(C["cover"]["idle"]["en"], ensure_ascii=False)[1:-1]) \
   .replace("ST_ON_FR", json.dumps(C["cover"]["on"]["fr"], ensure_ascii=False)[1:-1]) \
   .replace("ST_ON_EN", json.dumps(C["cover"]["on"]["en"], ensure_ascii=False)[1:-1])

EYE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3'
       'A10 10 0 1 0 12 2Z"/></svg>')

PAGE = """<!doctype html>
<html lang="fr" data-lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0B1613">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>@@CSS@@</style>
<script type="application/ld+json">@@JSONLD@@</script>
</head>
<body>
<div class="bar"><div class="wrap">
  <span><span class="dotlive" aria-hidden="true"></span><b>@@BAR_H1@@</b> 8h30 – 18h30
    <span class="sep">·</span> <b>@@BAR_H2@@</b> 8h30 – 13h30 <span class="warn">@@BAR_OK@@</span></span>
  <span>@@BAR_ADDR@@ <span class="sep">·</span> <a href="tel:@@TELF@@">@@TELDISP@@</a></span>
</div></div>

<header class="nav"><div class="wrap">
  <a class="brand" href="#top">
    <svg width="30" height="30" viewBox="0 0 40 40" role="img" aria-label="Le Cristallin">
      <circle cx="20" cy="20" r="18.4" fill="none" stroke="#0D5A41" stroke-width="1.6"/>
      <path d="M5.6 20C9 13.4 14 10.2 20 10.2S31 13.4 34.4 20C31 26.6 26 29.8 20 29.8S9 26.6 5.6 20Z"
            fill="none" stroke="#0D5A41" stroke-width="1.6"/>
      <circle cx="20" cy="20" r="5.1" fill="#0D5A41"/><circle cx="18.1" cy="18.1" r="1.5" fill="#EFF2F1"/>
    </svg>
    <span><b>Le Cristallin</b><span class="sub">@@BRANDSUB@@</span></span>
  </a>
  <nav aria-label="@@NAVLBL@@">
@@NAV@@
  </nav>
  <div class="lang" role="group" aria-label="Français / English">
    <button id="btn-fr" class="is-on" type="button">FR</button><button id="btn-en" type="button">EN</button>
  </div>
  <a class="cta small" href="#contact">@@EYE@@ <span>@@CTANAV@@</span></a>
</div></header>

<main id="top">
<section class="hero" id="hero"><div class="wrap grid">
  <div class="reveal">
    <div class="eyebrow">@@H_EYEBROW@@</div>
    <h1>@@H_H1@@</h1>
    <p class="lede" style="margin-top:14px">@@H_LEDE@@</p>
    <div class="actions">
      <a class="btn btn-primary" id="wa-hero" target="_blank" rel="noopener" href="https://wa.me/@@WA@@?text=@@HEROMSG@@">@@EYE@@ <span>@@H_BOOK@@</span></a>
      <a class="btn btn-ghost" href="#couverture">@@H_INS@@</a>
    </div>
    <div class="facts">
@@FACTS@@
    </div>
  </div>
  <div class="chart reveal" role="group" aria-label="@@CHARTLBL@@">
    <div class="chart-top">
      <span class="mono">@@CHARTTOP@@</span>
      <span class="acuity">@@ACUITY@@ 20/20</span>
    </div>
@@CHART@@
    <p class="row-foot">@@CHARTFOOT@@</p>
  </div>
</div></section>

<section id="portes"><div class="wrap">
  <h2>@@D_H2@@</h2>
  <div class="doors" style="margin-top:22px">
@@DOORS@@
  </div>
</div></section>

<section id="services" class="hair"><div class="wrap">
  <h2>@@S_H2@@</h2>
  <p class="lede" style="margin:12px 0 20px">@@S_LEDE@@</p>
  <div class="svc reveal">
    <div class="h"><span>@@S_H1@@</span><span>@@S_H2b@@</span><span>@@S_H3@@</span></div>
@@SVC@@
  </div>
</div></section>

<section id="couverture" class="hair" style="background:var(--card)"><div class="wrap">
  <div class="eyebrow">@@C_EYEBROW@@</div>
  <h2>@@C_H2@@</h2>
  <div class="cover" style="margin-top:20px">
    <div class="picker reveal">
      <label for="ins">@@C_LABEL@@</label>
      <select id="ins">
        <option value="">@@C_NONE@@</option>
@@INSOPTS@@
      </select>
      <p class="state" id="ins-state"></p>
      <a class="btn btn-primary" id="ins-go" href="#contact" style="width:100%;justify-content:center">
        @@EYE@@ <span>@@C_GO@@</span></a>
      <p class="fine">@@C_FINE@@</p>
    </div>
    <div class="listcard reveal">
      <span class="k">@@C_TRUST@@</span>
      <ul>
@@INSLIST@@
      </ul>
      <p class="quote">@@C_QUOTE@@</p>
    </div>
  </div>
</div></section>

<section class="proof" id="preuves"><div class="wrap">
  <h2>@@P_H2@@</h2>
  <p class="lede" style="margin-top:12px">@@P_LEDE@@</p>
  <div class="tiles">
@@TILES@@
  </div>
  <p class="band">@@P_LAB@@</p>
  <p class="band"><b>@@P_PARTNER@@</b> ::@@PARTNERS@@::</p>
</div></section>

<section id="visuels"><div class="wrap">
  <div class="eyebrow">@@V_EYEBROW@@</div>
  <h2>@@V_H2@@</h2>
  <p class="lede" style="margin:12px 0 0">@@V_LEDE@@</p>
  <div class="frames">
@@FRAMES@@
  </div>
</div></section>

<section class="hair"><div class="wrap two">
  <div class="offer reveal">
    <h3>@@O_H@@</h3>
    <p style="margin:10px 0 0;font-size:.92rem">@@O_P@@</p>
    <p class="fine">@@O_FLAG@@</p>
  </div>
  <div class="reveal">
@@FAQS@@
  </div>
</div></section>

<section id="contact" class="hair"><div class="wrap">
  <h2>@@K_H2@@</h2>
  <div class="info">
    <div class="icard reveal">
      <h3>@@K_HOURS@@</h3>
      <table><tbody>
@@HOURS@@
      </tbody></table>
      <span class="flag">@@K_HFLAG@@</span>
    </div>
    <div class="icard reveal">
      <h3>@@K_WHERE@@</h3>
      <p style="font-size:.94rem;margin:0">@@K_ADDR@@</p>
      <p style="font-size:.88rem;margin:10px 0 0;color:var(--mute)">@@K_ADDRF@@</p>
      <a class="btn btn-ghost" style="margin-top:14px"
         href="https://www.google.com/maps/search/?api=1&amp;query=Le+Cristallin+optique+Douala"
         target="_blank" rel="noopener">@@K_MAPS@@</a>
    </div>
    <div class="icard reveal">
      <h3>@@K_REACH@@</h3>
      <table><tbody>
        <tr><td>WhatsApp @@K_FAST@@</td><td><a href="https://wa.me/@@WA@@">@@WADISP@@</a></td></tr>
        <tr><td>@@K_TEL@@</td><td><a href="tel:@@TELF@@">@@TELDISP@@</a></td></tr>
        <tr><td>@@K_TEL@@</td><td><a href="tel:@@TEL2@@">@@TEL2DISP@@</a></td></tr>
        <tr><td>@@K_MAIL@@</td><td><a href="mailto:@@MAIL@@">@@MAIL@@</a></td></tr>
        <tr><td>@@K_SITE@@</td><td><a href="https://lecristallinoptique.com/" rel="noopener">lecristallinoptique.com</a></td></tr>
      </tbody></table>
      <p class="fine">@@K_NFLAG@@</p>
    </div>
  </div>
</div></section>
</main>

<footer><div class="wrap">
  <div class="cols">
      <div>
        <h4>Le Cristallin</h4>
        <p style="max-width:34ch">@@F_P@@</p>
        <span class="badge">@@F_BADGE@@</span>
      </div>
@@FCOLS@@
  </div>
  <div class="strip">
    <span>@@F_S1@@ · <a href="https://lecristallinoptique.com/" rel="noopener">lecristallinoptique.com</a></span>
    <span>@@F_S2@@</span>
  </div>
</div></footer>

<div class="sticky-wa">
  <a class="p" id="wa-sticky" target="_blank" rel="noopener" href="https://wa.me/@@WA@@?text=@@HEROMSG@@">@@F_WA@@</a>
  <a class="c" href="tel:@@TELF@@">@@F_CALL@@</a>
</div>
<script>@@JS@@</script>
</body>
</html>
"""

h = C["hero"]
# le surlignage final de la lede : on remplace la fin de phrase par un <b> dans CHAQUE langue
def hl(pair, tail_fr, tail_en):
    a = pair["fr"].rsplit(tail_fr, 1)
    b = pair["en"].rsplit(tail_en, 1)
    fr = a[0] + '<b class="h1hl">' + tail_fr + '</b>'
    en = b[0] + '<b class="h1hl">' + tail_en + '</b>'
    return L({"fr": fr, "en": en})

cv = C["cover"]
pr = C["proof"]
ph = C["photos"]
of = C["offerfaq"]
kt = C["contact"]
ft = C["footer"]
sv = C["services"]
dd = C["doors"]

REPL = {
    "TITLE": C["title"]["fr"], "DESC": C["desc"]["fr"], "BRANDSUB": L(C["brandSub"]),
    "BAR_H1": L(C["bar"]["hours1"]), "BAR_H2": L(C["bar"]["hours2"]),
    "BAR_OK": L(C["bar"]["confirm"]), "BAR_ADDR": L(C["bar"]["addr"]),
    "TELF": C["telFixe"], "TELDISP": "(+237) 242 65 12 65",
    "TEL2": C["tel2"], "TEL2DISP": "679 63 20 12", "MAIL": C["mail"],
    "WA": WA, "WADISP": C["wa"], "EYE": EYE, "NAVLBL": T(C["a11y"]["nav"]), "NAV": NAV,
    "CTANAV": L(C["ctaNav"]),
    # le lien est réel DÈS LE HTML (pas seulement posé par le JS) : même texte que le message
    # générique du sélecteur de langue, encodé ici pour ne jamais diverger du JSON.
    "HEROMSG": urllib.parse.quote(C["waMsg"]["generic"]["fr"]),
    "H_EYEBROW": L(h["eyebrow"]), "H_H1": L(h["h1"]),
    "H_LEDE": hl(h["lede"], h["h1hl"]["fr"], h["h1hl"]["en"]),
    "H_BOOK": L(h["book"]), "H_INS": L(h["insured"]), "FACTS": FACTS,
    "CHARTLBL": T(C["a11y"]["chart"]), "CHARTTOP": L(h["chartTop"]), "ACUITY": L(h["acuity"]),
    "CHART": CHART_ROWS, "CHARTFOOT": L(h["chartFoot"]),
    "D_EYEBROW": L(dd["eyebrow"]), "D_H2": L(dd["h2"]), "DOORS": DOORS,
    "S_EYEBROW": L(sv["eyebrow"]), "S_H2": L(sv["h2"]), "S_LEDE": L(sv["lede"]),
    "S_H1": L(sv["head"][0]), "S_H2b": L(sv["head"][1]), "S_H3": L(sv["head"][2]), "SVC": SVC_ROWS,
    "C_EYEBROW": L(cv["eyebrow"]), "C_H2": L(cv["h2"]), "C_LABEL": L(cv["label"]),
    "C_NONE": L(cv["none"]), "INSOPTS": INS_OPTS, "C_GO": L(cv["go"]), "C_FINE": L(cv["fine"]),
    "C_TRUST": L(cv["trust"]), "INSLIST": INS_LIST, "C_QUOTE": L(cv["quote"]),
    "P_EYEBROW": L(pr["eyebrow"]), "P_H2": L(pr["h2"]), "P_LEDE": L(pr["lede"]), "TILES": TILES,
    "P_LAB": L(pr["lab"]), "P_PARTNER": L(pr["partner"]), "PARTNERS": PARTNER_NAMES,
    "V_EYEBROW": L(ph["eyebrow"]), "V_H2": L(ph["h2"]), "V_LEDE": L(ph["lede"]), "FRAMES": FRAMES,
    "O_H": L(of["offerH"]), "O_P": L(of["offerP"]), "O_FLAG": L(of["offerFlag"]), "FAQS": FAQS,
    "K_EYEBROW": L(kt["eyebrow"]), "K_H2": L(kt["h2"]), "K_HOURS": L(kt["hoursH"]),
    "HOURS": hours_rows, "K_HFLAG": L(kt["hoursFlag"]), "K_WHERE": L(kt["whereH"]),
    "K_ADDR": L(kt["addr"]), "K_ADDRF": L(kt["addrFlag"]), "K_MAPS": L(kt["maps"]),
    "K_REACH": L(kt["reachH"]), "K_FAST": L(kt["fastest"]), "K_TEL": L(kt["phone"]),
    "K_MAIL": L(kt["email"]), "K_SITE": L(kt["site"]), "K_NFLAG": L(kt["numFlag"]),
    "F_P": L(ft["brandP"]), "F_BADGE": L(ft["badge"]), "FCOLS": FOOT_COLS,
    "F_S1": L(ft["strip1"]), "F_S2": L(ft["strip2"]), "F_WA": L(ft["cta"]),
    "F_CALL": L(C["sticky"][1]), "CSS": CSS, "JS": JS, "JSONLD": JSONLD,
}
# la lede du hero est une phrase unique : on garde le texte FR/EN entier, sans découpage hasardeux
PAGE = PAGE.replace('<p class="lede" style="margin-top:14px">@@H_LEDE@@</p>',
                    '<p class="lede" style="margin-top:14px">' + REPL["H_LEDE"] + '</p>')
REPL.pop("H_LEDE")
for k, v in REPL.items():
    PAGE = PAGE.replace("@@" + k + "@@", str(v))

left = [t for t in set(PAGE.split()) if t.startswith("@@") and t.endswith("@@")]
assert not left, f"jetons non remplacés : {left}"

n_fr = PAGE.count('class="fr-only"')
n_en = PAGE.count('class="en-only"')
if n_fr != n_en:
    raise SystemExit(f"✗ déséquilibre des paires de langue : {n_fr} FR / {n_en} EN — rien n'est écrit")

n_fr = PAGE.count('class="fr-only"')
n_en = PAGE.count('class="en-only"')
# ── RÈGLE MÉCANIQUE (21/09, loi maison §2 « 1 eyebrow par 3 sections max ») ──────────
#   audit_html.py compte les eyebrows mais ne sort PAS en finding : si on laisse 7 eyebrows
#   sur 8 sections, le contrôle dit « 0 finding » et la page sort monotone. La règle vit donc
#   dans le générateur, pas dans l'espoir d'un lecture humaine.
_nsec = PAGE.count("<section")
_neyb = PAGE.count('class="eyebrow"')
assert _neyb <= -(-_nsec // 3), f"{_neyb} eyebrows pour {_nsec} sections — plafond ceil(n/3) = {-(-_nsec // 3)}"
_nohref = re.findall(r'<a(?![^>]*href=)[^>]*>', PAGE)
assert not _nohref, f"ancre sans href (bouton mort si le JS ne charge pas) : {_nohref[:2]}"
assert "https://wa.me/ " not in PAGE, "espace dans une URL WhatsApp en dur"
for _m in re.findall(r'href="(https://wa\\.me/[^"]*)"', PAGE):
    assert " " not in _m, f"espace dans une URL WhatsApp : {_m!r} — le lien meurt après le préfixe"

# ── RÈGLE MÉCANIQUE (21/09) : MÊME ACTION = MÊS MOTS, vérifiée par la machine ──────────
#   §13 demande que le CTA mobile collant porte LE MÊME texte que le CTA du hero (un utilisateur
#   qui descend la page ne doit pas croire qu'il change de destination). C'était noté « ✓ » dans
#   mes notes alors que hero disait « Réserver un examen de vue » et le rail « Réserver sur
#   WhatsApp ». Un point de relecture qui n'est pas une assertion est une opinion.
_lab = lambda k: [t for t in re.findall(r'id="%s".*?<span[^>]*>([^<]+)</span>' % k, PAGE, re.S)]
_h, _s = _lab("wa-hero"), _lab("wa-sticky")
assert _h and _s and _h[0] == _s[0], f"CTA hero {_h[:1]} ≠ CTA du rail mobile {_s[:1]}"
_fr = [t for t in re.findall(r'class="fr-only">([^<]+)<', PAGE)]
assert _fr == [t for t in _fr], "jetons FR vides dans la page"

OUT.write_text(PAGE, encoding="utf-8")

print(f"OK {OUT} — {OUT.stat().st_size/1024:.0f} KB · runs FR {n_fr} / EN {n_en} · "
      f"planche {len(C['chart'])} lignes · services {len(sv['rows'])} · assureurs {len(C['insurers'])}")
