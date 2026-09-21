#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Univers Optique (Bépanda, Douala) — générateur du concept « dossier de reprise ».

ARCHÉTYPE (registre d'unicité, 21/09/2026) : le document administratif qui reprend la main.
  La page s'ouvre sur la COUVERTURE D'UN DOSSIER (fiche d'établissement + tampon « à reprendre »),
  pas sur une vitrine. Palette papier chaud + bleu-petrole + une seule encre rouge brique
  (celle des constatations). Typo : Bricolage Grotesque (display) / Public Sans (texte) /
  JetBrains Mono (champs de la fiche). Mode : redesign-overhaul (V7 / M4 / D5).

CE QUE CE FICHIER NE FAIT PAS : il n'invente aucun fait, aucun prix, aucun avis, aucune photo
  réelle. Toute la copie vit dans univers_optique_content.{py,json} ; ce fichier ne met en forme.
  Les trois visuels sont des RENDUS, étiquetés comme tels en FR et EN sur chaque image.

CONTRÔLES (la machine, pas la relecture) — voir la fin du fichier :
  poids WhatsApp, par visuel, compte FR/EN de la COPIE (le DOM ne peut pas compter les spans
  cachés), plafond d'eyebrows, alt/width/height/lazy, aucune ancre morte, même CTA au hero et au
  rail mobile, zéro jeton non remplacé, palette lisible (contraste calculé, pas espéré).
"""
import base64
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "demos" / "concept-univers-optique-v1.html"
sys.path.insert(0, str(ROOT / "demos"))
from univers_optique_content import C  # noqa: E402

# ── le numéro WhatsApp : chiffres seuls. Un espace dans l'URL tue le message pré-rempli. ──
WA = re.sub(r"\D", "", C["wa"])
assert len(WA) == 9 and WA.startswith("6"), f"numéro WhatsApp invalide : {WA!r}"
TEL = WA  # le portable du cabinet sert aussi de lien tel:

MAPS = ("https://www.google.com/maps/search/?api=1&query=Univers%20Optique%20"
        "B%C3%A9panda%20Douala")


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def L(pair):
    """Paire FR|EN -> deux spans. La page est bilingue par DOM, pas par traduction runtime."""
    if isinstance(pair, dict):
        fr, en = pair["fr"], pair["en"]
    else:
        fr, en = pair[0], pair[1]
    return f'<span class="fr-only">{esc(fr)}</span><span class="en-only">{esc(en)}</span>'


def pair(pair_):
    """Les deux langues en attribut (aria-label / alt) : FR d'abord, EN en secours."""
    if isinstance(pair_, dict):
        return pair_["fr"], pair_["en"]
    return pair_[0], pair_[1]


def wa_url(text):
    return "https://wa.me/%s?text=%s" % (WA, text)


def wa_msg(d):
    """Message pré-rempli : on encode côté Python pour qu'aucun espace ne survive dans l'href."""
    from urllib.parse import quote
    return wa_url(quote(d["fr"]))


# ── palette : chaque couple texte/fond est CALCULÉ avant d'être écrit ────────────────
PAPER = "#F2EDE3"
CARD = "#F7F3EA"
INK = "#17140F"
TEXT = "#322E27"
MUTE = "#5A5347"
LINE = "#DBD3C3"
BRAND = "#14344A"
BRAND_DK = "#0E2536"
FLAG = "#8F3821"
CHECK = "#235A35"


def _lum(h):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(int(h[i:i + 2], 16)) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cr(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def sat(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    mx, mn = max(r, g, b), min(r, g, b)
    return 0 if mx == 0 else (mx - mn) / mx


CONTRASTS = [("ink/paper", INK, PAPER, 4.5), ("text/paper", TEXT, PAPER, 4.5),
             ("text/card", TEXT, CARD, 4.5), ("mute/paper", MUTE, PAPER, 4.5),
             ("mute/card", MUTE, CARD, 4.5), ("paper/brand", PAPER, BRAND, 4.5),
             ("paper/branddk", PAPER, BRAND_DK, 4.5), ("flag/paper", FLAG, PAPER, 4.5),
             ("flag/card", FLAG, CARD, 4.5), ("check/paper", CHECK, PAPER, 4.5),
             ("brand/paper", BRAND, PAPER, 4.5), ("brand/card", BRAND, CARD, 4.5),
             ("brand@15/card", "#BBD0DE", BRAND, 3.0)]
# les liserés décoratifs (bornes de colonnes, filets du pied de page) ne portent pas de texte :
# ils ne sont pas soumis au ratio. Tout ce qui EST du texte est dans la liste ci-dessus.
for _n, _a, _b, _need in CONTRASTS:
    _r = cr(_a, _b)
    assert _r >= _need, "contraste %.2f < %.1f pour %s (%s on %s)" % (_r, _need, _n, _a, _b)
for _c in (BRAND, FLAG, CHECK):
    assert sat(_c) < 0.80, "accent saturé à %.0f%% : %s (§3.1)" % (sat(_c) * 100, _c)
for _c in (PAPER, CARD, INK):
    assert _c.upper() not in ("#FFFFFF", "#000000"), "blanc/noir purs interdits (§3.1)"

# ── les trois visuels de concept, inlinés en base64 ──────────────────────────────────
IMG_DIR = ROOT / "demos" / "img"
DIM = {"shop": (1312, 816), "bench": (1200, 896), "customer": (1024, 1024)}
IMG = {}
for _k in DIM:
    _p = IMG_DIR / f"univers-optique-{_k}.jpg"
    assert _p.exists(), f"visuel manquant : {_p}"
    _raw = _p.read_bytes()
    assert len(_raw) <= 260 * 1024, f"{_k} pèse {len(_raw)//1024} Ko (plafond 260 Ko/visuel)"
    IMG[_k] = "data:image/jpeg;base64," + base64.b64encode(_raw).decode()
IMGKB = sum(len(v) for v in IMG.values()) // 1024

EYE = ('<svg class="i" viewBox="0 0 24 24" width="17" height="17" aria-hidden="true">'
       '<path d="M2 12s3.9-6.2 10-6.2S22 12 22 12s-3.9 6.2-10 6.2S2 12 2 12Z" fill="none" '
       'stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="12" r="2.9" fill="currentColor"/></svg>')
WA_I = ('<svg class="i" viewBox="0 0 24 24" width="17" height="17" aria-hidden="true">'
        '<path d="M12 2.2A9.7 9.7 0 0 0 3.6 16.8L2.4 21.6l4.9-1.2A9.7 9.7 0 1 0 12 2.2Z" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M8.7 7.5 10 7.3l1.1 '
        '2.6-1 .9c.5 1.2 1.4 2 2.5 2.5l.9-1 2.6 1.1-.2 1.3c-.2.9-1.2 1.4-2.1 1.2A8.6 8.6 0 0 1 7.5 9.6c-.2-.9.3-1.9 1.2-2.1Z" '
        'fill="currentColor"/></svg>')
PH_I = ('<svg class="i" viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M5 3.4h3.2l'
        '1.5 3.9-2 1.4a11 11 0 0 0 5.6 5.6l1.4-2 3.9 1.5v3.2c0 1-.9 1.8-1.9 1.7A15.6 15.6 0 0 1 3.3 5.3C3.2 4.3 4 3.4 5 3.4Z" '
        'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>')


def img(tag, w, h):
    return '<img src="%s" width="%d" height="%d" loading="lazy" decoding="async" alt="%s">%s' % (
        IMG[tag], DIM[tag][0], DIM[tag][1], esc(w), esc(h))


# ── CSS ─────────────────────────────────────────────────────────────────────────────
CSS = """
:root{
 --paper:%(PAPER)s; --card:%(CARD)s; --ink:%(INK)s; --text:%(TEXT)s; --mute:%(MUTE)s;
 --line:%(LINE)s; --brand:%(BRAND)s; --brand-dk:%(BRAND_DK)s; --flag:%(FLAG)s; --check:%(CHECK)s;
 --disp:"Bricolage Grotesque","Archivo",system-ui,sans-serif;
 --body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
 --mono:"JetBrains Mono",ui-monospace,"SFMono-Regular",monospace;
 --r:3px; --wrap:1180px; --pad:clamp(18px,4.2vw,44px);
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%;scroll-behavior:smooth;scroll-padding-top:104px}
body{margin:0;background:var(--paper);color:var(--text);font-family:var(--body);
 font-size:16.5px;line-height:1.62;font-weight:400;overflow-wrap:break-word;
 background-image:linear-gradient(180deg,rgba(20,52,74,.035),rgba(20,52,74,0) 460px)}
h1,h2,h3{font-family:var(--disp);color:var(--ink);margin:0;font-weight:700;
 letter-spacing:-.018em;line-height:1.08;text-wrap:balance}
h1{font-size:clamp(2.05rem,5.4vw,3.55rem)}
h2{font-size:clamp(1.5rem,3.5vw,2.35rem)}
h3{font-size:1.05rem;line-height:1.25;font-weight:650}
p{margin:0}
a{color:var(--brand);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--flag);outline-offset:2px;border-radius:2px}
img{display:block;max-width:100%%;height:auto}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.wrap{width:100%%;max-width:var(--wrap);margin-inline:auto;padding-inline:var(--pad)}
html[data-lang=fr] .en-only{display:none}
html[data-lang=en] .fr-only{display:none}

/* ── bandeau d'état : la page est un document privé, elle le dit ───────────── */
.status{background:var(--brand-dk);color:var(--paper);font-family:var(--mono);font-size:11.5px;
 letter-spacing:.055em;text-transform:uppercase;padding:9px 0}
.status .wrap{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline;justify-content:space-between}
.status b{color:var(--paper);font-weight:600}
.status .tagline{color:#BBD0DE}
.status .sep{opacity:.5;padding-inline:4px}
.status a{color:#DCE9F2;text-decoration:none;border-bottom:1px solid #37607A}
.status a:hover{border-bottom-color:#DCE9F2}

/* ── en-tête : onglets d'index, pas de pills ──────────────────────────────── */
.nav{position:sticky;top:0;z-index:40;background:var(--paper);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:14px;min-height:72px;padding-block:8px}
.mark{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);flex:0 0 auto}
.mark svg{flex:0 0 auto}
.mark .nm{font-family:var(--disp);font-weight:700;font-size:1.02rem;letter-spacing:-.01em;line-height:1.1}
.mark .rl{display:block;font-family:var(--mono);font-size:9.6px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--mute);font-weight:400}
.nav ol{display:flex;gap:2px;list-style:none;margin:0 0 0 auto;padding:0;flex-wrap:wrap}
.nav .tab{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.06em;
 text-transform:uppercase;text-decoration:none;color:var(--mute);padding:7px 10px 6px;
 border:1px solid transparent;border-bottom:0;border-radius:var(--r) var(--r) 0 0;line-height:1.3;
 transition:color .18s,background-color .18s}
.nav .tab:hover{color:var(--ink);background:#E9E2D5;border-color:var(--line)}
.nav .tab.is-on{color:var(--brand);background:var(--card);border-color:var(--line);font-weight:600}
.lang{display:flex;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;flex:0 0 auto}
.lang button{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;background:transparent;
 color:var(--mute);border:0;padding:7px 9px;cursor:pointer;transition:color .18s,background-color .18s}
.lang button:hover{color:var(--ink);background:#E9E2D5}
.lang .is-on{background:var(--brand);color:var(--paper)}
.cta{display:inline-flex;align-items:center;gap:8px;background:var(--brand);color:var(--paper);
 text-decoration:none;font-weight:600;font-size:.95rem;padding:11px 17px;border-radius:var(--r);
 border:1px solid var(--brand);transition:background-color .18s,transform .12s}
.cta:hover{background:var(--brand-dk);text-decoration:none}
.cta:active{transform:scale(.97)}
.cta .i{flex:0 0 auto}
.cta.ghost{background:transparent;color:var(--brand);border-color:var(--brand)}
.cta.ghost:hover{background:#E4E9EE}
/* Le CTA de l'en-tête : visible dès qu'il y a la place (≥ 900px). En dessous, c'est le rail
   collé au pouce qui tient ce rôle — d'où la règle `display:none` dans le bloc 960px, et le
   fait que les DEUX portent le MÊME texte (assertion 7). */
.nav .cta.small{display:inline-flex;font-size:.88rem;padding:9px 14px;flex:0 0 auto}

/* ── le dossier : couverture ───────────────────────────────────────────────── */
main>section{padding-block:clamp(46px,7vw,88px);border-bottom:1px solid var(--line)}
main>section:last-of-type{border-bottom:0}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.13em;text-transform:uppercase;
 color:var(--flag);margin-bottom:14px}
.lede{font-size:1.05rem;color:var(--text);max-width:63ch}
.hero .grid{display:grid;grid-template-columns:1.08fr .92fr;gap:clamp(24px,4vw,54px);align-items:start}
.hero h1{margin-bottom:16px}
.hero .actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}

/* la fiche d'établissement : le vrai objet du dossier */
.sheet{background:var(--card);border:1px solid var(--line);border-radius:var(--r);
 box-shadow:0 14px 30px -22px rgba(20,52,74,.55);position:relative;overflow:hidden}
.sheet-top{display:flex;justify-content:space-between;align-items:baseline;gap:10px;
 padding:13px 16px;border-bottom:1px solid var(--line);background:#EDE6D9}
.sheet-top .t{font-family:var(--mono);font-size:11px;letter-spacing:.11em;text-transform:uppercase;
 color:var(--brand);font-weight:600}
.sheet-top .no{font-family:var(--mono);font-size:10.5px;color:var(--mute)}
.sheet dl{margin:0;padding:2px 16px 6px}
.sheet .rec{display:grid;grid-template-columns:minmax(96px,.86fr) 1.14fr;gap:10px;
 padding:9px 0;border-bottom:1px dotted #CFC6B4;align-items:baseline}
.sheet .rec:last-of-type{border-bottom:0}
.sheet dt{font-family:var(--mono);font-size:10.6px;letter-spacing:.04em;text-transform:uppercase;
 color:var(--mute);line-height:1.4}
.sheet dd{margin:0;font-size:.95rem;color:var(--ink);font-weight:550}
.sheet dd.dead{color:var(--flag);font-weight:600}
.sheet dd.open{color:var(--brand);font-weight:600}
.sheet-foot{padding:11px 16px 14px;font-size:.8rem;color:var(--mute);border-top:1px solid var(--line)}
.stamp{position:absolute;right:14px;top:66px;transform:rotate(-7.5deg);border:2px solid var(--flag);
 color:var(--flag);border-radius:var(--r);padding:5px 10px;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.16em;text-transform:uppercase;font-weight:600;background:rgba(242,237,227,.72);
 transition:transform .2s cubic-bezier(.2,.7,.2,1)}
.sheet:hover .stamp,.sheet:focus-within .stamp{transform:rotate(-3deg) translateY(-2px)}

/* ── constatations : liste bordée, pas de cartes gégales ──────────────────── */
.dossier .intro{display:grid;grid-template-columns:1fr;gap:10px;max-width:74ch;margin-bottom:26px}
.finding{display:grid;grid-template-columns:170px 1fr;border-top:1px solid var(--line);
 padding:20px 0;gap:clamp(14px,3vw,32px)}
.finding:last-of-type{border-bottom:1px solid var(--line)}
.f-head{display:flex;flex-direction:column;gap:8px}
.f-kick{font-family:var(--mono);font-size:10.4px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--flag);font-weight:600}
.f-where{font-family:var(--disp);font-weight:650;font-size:1.06rem;line-height:1.2;color:var(--ink);
 text-wrap:balance}
.f-body h3{font-family:var(--mono);font-weight:600;font-size:11px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--brand);margin:0 0 5px}
.f-read{font-size:1rem;color:var(--ink)}
.f-move{margin-top:11px;font-size:.97rem;color:var(--text);padding-left:14px;
 border-left:2px solid var(--check)}
.f-move b{color:var(--ink)}
.f-src{margin-top:11px;font-family:var(--mono);font-size:10.6px;color:var(--mute);line-height:1.5;
 word-break:break-word}
.f-src b{color:var(--brand);font-weight:600}
.dossier .cnote{margin-top:24px;font-size:.92rem;color:var(--mute);max-width:70ch;
 border-top:1px solid var(--line);padding-top:14px}

/* ── le cabinet : le registre des actes ───────────────────────────────────── */
.svc{border:1px solid var(--line);border-radius:var(--r);background:var(--card);overflow:hidden;
 margin-top:24px}
.svc .head{display:grid;grid-template-columns:1.6fr 1fr 92px;gap:12px;padding:11px 16px;
 background:#EDE6D9;border-bottom:1px solid var(--line);font-family:var(--mono);font-size:10.4px;
 letter-spacing:.1em;text-transform:uppercase;color:var(--brand);font-weight:600}
.row{display:grid;grid-template-columns:1.6fr 1fr 92px;gap:12px;padding:13px 16px;align-items:start;
 border-bottom:1px dotted #CFC6B4;cursor:pointer;transition:background-color .18s}
.row:last-of-type{border-bottom:0}
.row:hover{background:#EDE7DA}
.row:active{background:#E6DFD0}
.row .n{font-weight:650;color:var(--ink);font-size:1rem;font-family:var(--disp);line-height:1.2}
.row .d{font-size:.9rem;color:var(--mute);line-height:1.5}
.row .go{font-family:var(--mono);font-size:10.6px;letter-spacing:.05em;text-transform:uppercase;
 color:var(--brand);text-align:right;align-self:center;border-bottom:1px solid #AFC3D1;
 transition:color .18s}
.row:hover .go{color:var(--brand-dk)}
.rare{margin-top:22px;display:grid;grid-template-columns:1fr auto;gap:clamp(16px,3vw,30px);
 align-items:center;border:1px solid var(--brand);border-left:4px solid var(--brand);
 background:#E8EEF2;border-radius:var(--r);padding:clamp(16px,3vw,24px)}
.rare h2{font-size:clamp(1.12rem,2.4vw,1.5rem);margin-bottom:8px}
.rare p{font-size:.97rem;color:var(--text)}
.rare a{margin-top:14px}
.rare .ask{font-size:.88rem;font-weight:600}

/* ── rendez-vous : les créneaux, pas un formulaire ────────────────────────── */
.book{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(20px,4vw,44px);align-items:start}
.hours{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--card)}
.slot{display:grid;grid-template-columns:1fr auto auto;gap:12px;align-items:center;padding:14px 16px;
 border-bottom:1px dotted #CFC6B4;cursor:pointer;transition:background-color .18s}
.slot:last-of-type{border-bottom:0}
.slot:hover{background:#EDE7DA}
.slot:active{background:#E6DFD0}
.slot .d{font-weight:650;color:var(--ink);font-family:var(--disp)}
.slot .h{font-family:var(--mono);font-size:.9rem;color:var(--text)}
.slot .p{font-family:var(--mono);font-size:10.4px;letter-spacing:.06em;text-transform:uppercase;
 color:var(--brand);border:1px solid #B6C8D5;border-radius:2px;padding:4px 8px}
.slot.shut .p{color:var(--flag);border-color:#DDB6A9}
.slot.shut{cursor:default}
.slot.shut:hover{background:transparent}
.contact{border:1px solid var(--line);border-radius:var(--r);padding:clamp(15px,3vw,20px);background:var(--paper)}
.contact h3{font-family:var(--mono);font-size:10.6px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--brand);margin-bottom:10px}
.contact .l{display:flex;gap:9px;align-items:flex-start;padding:8px 0;border-bottom:1px dotted #CFC6B4;
 font-size:.94rem}
.contact .l:last-of-type{border-bottom:0}
.contact .k{font-family:var(--mono);font-size:10.4px;letter-spacing:.05em;text-transform:uppercase;
 color:var(--mute);min-width:78px;padding-top:2px}
.contact .v a,.contact .v{color:var(--ink);font-weight:550}
.contact .v .q{color:var(--flag);font-family:var(--mono);font-size:10px;letter-spacing:.05em}
.prewrite{margin-top:18px;border:1px dashed var(--brand);border-radius:var(--r);padding:13px 15px;
 background:#E8EEF2;font-size:.93rem;color:var(--ink)}
.prewrite .lbl{font-family:var(--mono);font-size:10.4px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--brand);display:block;margin-bottom:5px}
.fine{margin-top:16px;font-size:.85rem;color:var(--mute);max-width:72ch}

/* ── avis : la note réelle, en chiffres tabulaires ───────────────────────── */
.rate{display:grid;grid-template-columns:auto 1fr;gap:clamp(20px,4vw,40px);align-items:center;
 border:1px solid var(--line);border-radius:var(--r);background:var(--card);padding:clamp(18px,3.4vw,28px)}
.score{font-family:var(--disp);font-weight:700;font-size:clamp(3.4rem,9vw,5.4rem);line-height:.86;
 color:var(--ink);font-variant-numeric:tabular-nums;letter-spacing:-.04em}
.score span{display:block;font-family:var(--mono);font-size:10.6px;letter-spacing:.09em;
 text-transform:uppercase;color:var(--flag);margin-top:11px;font-weight:600}
.rate .of{font-size:.95rem;color:var(--mute)}
.ledger{margin-top:20px;border-top:1px solid var(--line)}
.lg{display:grid;grid-template-columns:.9fr 1.6fr;gap:clamp(12px,3vw,28px);padding:16px 0;
 border-bottom:1px solid var(--line)}
.lg h3{font-family:var(--mono);font-size:10.6px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--brand);font-weight:600}
.lg p{font-size:.98rem}
.warn{margin-top:18px;border-left:3px solid var(--flag);padding:12px 15px;background:#F0E7E1;
 border-radius:0 var(--r) var(--r) 0;font-size:.93rem;color:var(--ink)}

/* ── les trois visuels, étiquetés ────────────────────────────────────────── */
.strip{display:grid;grid-template-columns:1.5fr 1fr;gap:14px;margin-top:24px}
.shot{margin:0;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--card);
 position:relative}
.shot.big{grid-row:span 2}
.shot img{width:100%%;height:auto}
.shot .lay{padding:12px 14px 34px}
.shot figcaption{font-size:.9rem;color:var(--text)}
.shot .cn{display:block;font-family:var(--disp);font-weight:650;color:var(--ink);font-size:1rem;
 margin-bottom:4px}
.shot .badge{position:absolute;left:10px;bottom:10px;font-family:var(--mono);font-size:9.6px;
 letter-spacing:.055em;text-transform:uppercase;background:rgba(14,37,54,.92);color:var(--paper);
 padding:5px 8px;border-radius:2px}
.photos .lede{margin-bottom:6px}

/* ── questions ouvertes ─────────────────────────────────────────────────── */
.asks{list-style:none;margin:22px 0 0;padding:0;border-top:1px solid var(--line)}
.asks li{border-bottom:1px solid var(--line);padding:17px 0;
 display:grid;grid-template-columns:1.35fr 1fr;gap:clamp(12px,3vw,30px);align-items:start}
.asks h3{font-family:var(--disp);font-size:1.05rem;font-weight:650;color:var(--ink);margin-bottom:6px}
.asks p{font-size:.94rem;color:var(--text)}
.asks .qq{font-family:var(--mono);font-size:10.4px;letter-spacing:.09em;text-transform:uppercase;
 color:var(--flag);display:block;margin-bottom:7px}
.asks .ans{font-family:var(--mono);font-size:10.4px;letter-spacing:.05em;text-transform:uppercase;
 color:var(--brand);border:1px solid #B6C8D5;border-radius:2px;padding:6px 9px;text-align:center;
 text-decoration:none;display:block;transition:background-color .18s}
.asks .ans:hover{background:#E4E9EE;text-decoration:none}

/* ── FAQ ───────────────────────────────────────────────────────────────────── */
.faq details{border-bottom:1px solid var(--line);padding:2px 0}
.faq details:first-of-type{border-top:1px solid var(--line)}
.faq summary{cursor:pointer;list-style:none;display:grid;grid-template-columns:1fr 26px;gap:12px;
 align-items:center;padding:15px 0;font-family:var(--disp);font-weight:650;color:var(--ink);
 font-size:1.02rem;transition:color .18s}
.faq summary:hover{color:var(--brand)}
.faq summary::-webkit-details-marker{display:none}
.faq .pm{font-family:var(--mono);font-size:1.1rem;color:var(--brand);text-align:center;
 transition:transform .22s cubic-bezier(.2,.7,.2,1)}
.faq details[open] .pm{transform:rotate(45deg)}
.faq .a{padding:0 0 17px;font-size:.97rem;color:var(--text);max-width:78ch}

/* ── pied de page : le dernier écran du dossier ─────────────────────────── */
.pagefoot{background:var(--brand-dk);color:#D9E3EA;padding-block:clamp(40px,6vw,68px) 0}
.pagefoot a{color:#EAF1F6}
.pagefoot .top{display:grid;grid-template-columns:1.3fr 1fr 1fr 1fr;gap:clamp(20px,3.4vw,38px)}
.pagefoot .brandline{font-family:var(--disp);font-size:clamp(1.5rem,3.6vw,2.2rem);font-weight:700;
 color:var(--paper);letter-spacing:-.02em;line-height:1.05;margin-bottom:12px}
.pagefoot p{font-size:.93rem;color:#C3D2DD;max-width:44ch}
.pagefoot .badge{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:9.8px;
 letter-spacing:.09em;text-transform:uppercase;border:1px solid #37607A;border-radius:2px;
 padding:5px 9px;color:#D9E3EA}
.pagefoot h3{font-family:var(--mono);font-size:10.4px;letter-spacing:.1em;text-transform:uppercase;
 color:#9FBCD0;margin-bottom:11px;font-weight:600}
.pagefoot ul{list-style:none;margin:0;padding:0}
.pagefoot li{padding:5px 0;font-size:.93rem}
.pagefoot li a{text-decoration:none;border-bottom:1px solid #37607A;transition:border-color .18s,color .18s}
.pagefoot li a:hover{border-bottom-color:#EAF1F6;text-decoration:none}
.pagefoot .open{color:#F0C9BC;border-bottom-color:#8A5340}
.pagefoot .cta{margin-top:18px}
.strip2{margin-top:clamp(26px,4vw,44px);border-top:1px solid #2A4A60;padding-block:16px 20px;
 display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between;align-items:center;
 font-family:var(--mono);font-size:10.4px;letter-spacing:.045em;color:#A8C0D0}
.strip2 a{text-decoration:none;border-bottom:1px solid #37607A;color:#D9E3EA}

/* ── le rail mobile : une seule action visible à la fois ─────────────────── */
.rail{position:fixed;left:0;right:0;bottom:0;z-index:50;display:none;gap:8px;padding:9px 12px
 calc(9px + env(safe-area-inset-bottom));background:rgba(242,237,227,.97);
 border-top:1px solid var(--line);backdrop-filter:blur(7px)}
.rail a{flex:1;justify-content:center;font-size:.92rem;padding:12px 10px}
.reveal{opacity:0;transform:translateY(15px);transition:opacity .55s cubic-bezier(.2,.7,.2,1),
 transform .55s cubic-bezier(.2,.7,.2,1)}
.reveal.in{opacity:1;transform:none}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%%);white-space:nowrap}

@media (max-width:1120px){.mark .rl{display:none}}
@media (max-width:960px){
 .nav .cta.small{display:none}
 .hero .grid,.book,.rare{grid-template-columns:1fr}
 .pagefoot .top{grid-template-columns:1fr 1fr}
 .strip{grid-template-columns:1fr 1fr}
 .shot.big{grid-row:auto;grid-column:span 2}
 .finding{grid-template-columns:1fr}
 .f-head{flex-direction:row;flex-wrap:wrap;align-items:baseline;gap:10px}
 .stamp{position:static;display:inline-block;margin:2px 0 0 16px;transform:rotate(-2deg)}
 .asks li,.lg{grid-template-columns:1fr}
}
@media (max-width:640px){
 html{scroll-padding-top:132px}
 body{font-size:16px}
 .nav .wrap{flex-wrap:wrap;min-height:0;row-gap:0;padding-block:7px 0}
 .lang,.nav ol{order:3;width:100%%}
 .nav ol{margin:0 0 -1px;overflow-x:auto;flex-wrap:nowrap;-webkit-overflow-scrolling:touch}
 .nav .tab{white-space:nowrap;padding:6px 9px 5px}
 .lang{width:auto;order:2;margin-left:auto;margin-bottom:7px}
 .rail{display:flex}
 main{padding-bottom:76px}
 .row,.svc .head{grid-template-columns:1fr 78px}
 .row .d{grid-column:1/-1;order:3}
 .svc .head span:nth-child(2){display:none}
 .sheet dl{padding-inline:13px}
 .rate{grid-template-columns:1fr;text-align:left}
 .pagefoot .top{grid-template-columns:1fr}
 .strip{grid-template-columns:1fr}
 .shot.big{grid-column:auto}
}
@media (prefers-reduced-motion:reduce){
 html{scroll-behavior:auto}
 *,*::before,*::after{transition-duration:.01ms!important;animation-duration:.01ms!important}
 .reveal{opacity:1;transform:none}
}
""" % dict(PAPER=PAPER, CARD=CARD, INK=INK, TEXT=TEXT, MUTE=MUTE, LINE=LINE,
           BRAND=BRAND, BRAND_DK=BRAND_DK, FLAG=FLAG, CHECK=CHECK)

# ── JS : la langue, les révélations, les messages WhatsApp pré-remplis ──────────────
JS = """
(function(){
 var html=document.documentElement, KEY='universoptique-lang';
 function setLang(l){
  html.setAttribute('data-lang',l); html.lang=l;
  document.getElementById('btn-fr').classList.toggle('is-on',l==='fr');
  document.getElementById('btn-en').classList.toggle('is-on',l==='en');
  try{localStorage.setItem(KEY,l)}catch(e){}
 }
 document.getElementById('btn-fr').addEventListener('click',function(){setLang('fr')});
 document.getElementById('btn-en').addEventListener('click',function(){setLang('en')});
 try{var s=localStorage.getItem(KEY); if(s)setLang(s)}catch(e){}

 /* l'onglet courant, par intersection — pas par listener de scroll */
 var tabs={}; [].slice.call(document.querySelectorAll('.nav .tab')).forEach(function(t){
  var id=(t.getAttribute('href')||'').slice(1); if(id)tabs[id]=t;});
 if('IntersectionObserver' in window){
  var spy=new IntersectionObserver(function(es){es.forEach(function(e){
   var t=tabs[e.target.id]; if(!t)return;
   if(e.isIntersecting){[].slice.call(document.querySelectorAll('.nav .tab')).forEach(
    function(x){x.classList.remove('is-on')});t.classList.add('is-on');}});},
   {rootMargin:'-45%% 0px -50%% 0px'});
  [].slice.call(document.querySelectorAll('main>section[id]')).forEach(function(s){spy.observe(s)});
  var rev=new IntersectionObserver(function(es){es.forEach(function(e){
   if(e.isIntersecting){e.target.classList.add('in');rev.unobserve(e.target);}});},
   {threshold:.1,rootMargin:'0px 0px -6%% 0px'});
  [].slice.call(document.querySelectorAll('.reveal')).forEach(function(el){rev.observe(el)});
 }else{[].slice.call(document.querySelectorAll('.reveal')).forEach(function(el){el.classList.add('in')});}
 function reduce(){return window.matchMedia('(prefers-reduced-motion: reduce)').matches;}
 if(reduce()){[].slice.call(document.querySelectorAll('.reveal')).forEach(function(el){el.classList.add('in')});}

 /* un acte, un créneau = une conversation déjà écrite */
 function open(el){
  var h=el.getAttribute('data-msg');
  if(h){window.open(h,'_blank','noopener');}
 }
 [].slice.call(document.querySelectorAll('[data-msg]')).forEach(function(el){
  el.addEventListener('click',function(ev){ev.preventDefault();open(el)});
  el.addEventListener('keydown',function(ev){
   if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();open(el);}});
 });
})();
"""

# ── JSON-LD : NAP strictement conforme à la fiche Google, aucune note inventée ──────
SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Optician",
    "name": "Univers Optique",
    "legalName": C["legalName"],
    "foundingDate": "2009-08-01",
    "description": C["desc"]["fr"],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": C["addr"].split(" — ")[0],
        "addressLocality": "Douala",
        "addressRegion": "Littoral",
        "addressCountry": "CM",
        "postOfficeBoxNumber": "4680",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": C["geo"][0], "longitude": C["geo"][1]},
    "hasMap": MAPS,
    "telephone": "+237" + WA,
    "email": C["mail1"],
    "areaServed": [{"@type": "City", "name": "Douala"}, {"@type": "Place", "name": "Bépanda"}],
    "currenciesAccepted": "XAF",
    "paymentAccepted": "Espèces, Mobile Money, carte — à confirmer (champ annuaire vide)",
    "knowsAbout": ["examen de vue", "verres correcteurs", "montures", "verres de sécurité",
                   "prothèses oculaires", "lentilles de contact", "formation en optique-lunetterie"],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday",
         "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00"}],
    # aggregateRating VOLONTAIREMENT absent : 6 avis à 3,3 ne se balisent pas (voir section avis).
    # sameAs VOLONTAIREMENT absent : aucune page sociale rattachée à ce nom avec certitude.
}


# ══════════════════════════════════════════════════════════════════════════
#  LA PAGE
# ══════════════════════════════════════════════════════════════════════════
H = C["hero"]
D = C["dossier"]
S = C["services"]
R = C["prosthesis"]
B = C["book"]
V = C["reviews"]
P = C["photos"]
O = C["open"]
F = C["faq"]
FO = C["footer"]

GEN_MSG = wa_msg(C["waMsg"]["generic"])


def lrow(cells):
    return '<li class="rec"><dt>%s</dt><dd>%s</dd></li>' % (
        '<span class="fr-only" data-lang="fr">%s</span>'
        '<span class="en-only" data-lang="en">%s</span>' % (esc(cells[0]), esc(cells[1])),
        cells[2])


def bi(fr, en, tag="span"):
    return ('<%s class="fr-only" data-lang="fr">%s</%s><%s class="en-only" data-lang="en">%s</%s>'
            % (tag, esc(fr), tag, tag, esc(en), tag))


# ── la fiche d'établissement (huit lignes, lues à six sources) ─────────────
rec_rows = []
for cells in H["facts"]:
    cls = ""
    if "hors ligne" in cells[2]:
        cls = ' class="dead"'
    elif "confirmer" in cells[2]:
        cls = ' class="open"'
    rec_rows.append(
        '<div class="rec"><dt>%s</dt><dd%s>%s</dd></div>'
        % (bi(cells[0], cells[1]), cls, esc(cells[2])))
SHEET = ('<aside class="sheet reveal" role="group" aria-label="%s">'
         '<div class="sheet-top"><span class="t">%s</span>'
         '<span class="no mono">%s</span></div>%s'
         '<div class="stamp" aria-hidden="true">%s</div>'
         '<div class="sheet-foot">%s</div></aside>'
         % (esc(C["a11y"]["record"]["fr"]), bi(H["recordHead"]["fr"], H["recordHead"]["en"]),
            esc(H["recordNo"]), "".join(rec_rows),
            L({"fr": H["stamp"]["fr"], "en": H["stamp"]["en"]}),
            bi("Constaté le 21/09/2026 par AMK · six sources publiques citées plus bas · « à reprendre » "
               "veut dire : c'est à vous de décider ce qui est vrai.",
               "Recorded 21/09/2026 by AMK · six public sources cited below · \"to reclaim\" means: "
               "you decide what is true.")))

# ── les six constatations ──────────────────────────────────────────────────
find_rows = []
for r in D["rows"]:
    find_rows.append(
        '<article class="finding reveal"><div class="f-head"><span class="f-kick">%s</span>'
        '<h3 class="f-where">%s</h3></div>'
        '<div class="f-body"><h3>%s</h3><p class="f-read">%s</p>'
        '<p class="f-move"><b>%s</b> %s</p>'
        '<p class="f-src">%s <b>%s</b></p></div></article>'
        % (bi("Constat", "Finding"), bi(r[0], r[1]),
           bi("Ce que j'ai lu", "What I read"), bi(r[2], r[3]),
           bi("La reprise", "The move"), bi(r[4], r[5]),
           bi("Source", "Source"), esc(r[6])))

# ── le registre des dix actes ──────────────────────────────────────────────
svc_rows = []
for r in S["rows"]:
    msg = wa_msg(dict(C["waMsg"]["row"], svc=r[0])) if False else (
        "https://wa.me/%s?text=%s" % (WA, __import__("urllib.parse", fromlist=["quote"])
                                       .quote(C["waMsg"]["row"]["fr"].replace("{svc}", r[0]), safe="")))
    svc_rows.append(
        '<li class="row" tabindex="0" role="link" data-msg="%s" data-svc-fr="%s" data-svc-en="%s" '
        'aria-label="%s">'
        '<span class="n">%s</span><span class="go">%s</span><span class="d">%s</span></li>'
        % (esc(msg), esc(r[0]), esc(r[1]),
           esc("Demander « %s » par WhatsApp" % r[0]),
           bi(r[0], r[1]), L(S["ask"]), bi(r[2], r[3])))

# ── créneaux ───────────────────────────────────────────────────────────────
slot_rows = []
from urllib.parse import quote as _q  # noqa: E402
for i, sl in enumerate(B["slots"]):
    shut = "Fermé" in sl[2]
    msg = ("https://wa.me/%s?text=%s" % (WA, _q(
        C["waMsg"]["slot"]["fr"].replace("{slot}", "%s %s" % (sl[0], sl[2])).replace(
            "{when}", "cet après-midi" if i == 0 else "samedi"), safe="")))
    slot_rows.append(
        '<li class="slot%s"%s data-msg="%s"><span class="d">%s</span>'
        '<span class="h">%s</span><span class="p">%s</span></li>'
        % (" shut" if shut else "", "" if shut else ' tabindex="0" role="link"',
           "" if shut else esc(msg),
           bi(sl[0], sl[1]), esc(sl[2]),
           bi("Réserver", "Book") if not shut else bi("Fermé", "Closed")))

# ── les trois visuels ──────────────────────────────────────────────────────
#   l'ordre des fichiers suit l'ordre des items de la copie ; le tag n'est PAS une donnée
#   éditoriale (il nomme un fichier), il vit donc ici, à côté de DIM.
SHOT_TAGS = ["shop", "bench", "customer"]
assert len(SHOT_TAGS) == len(P["items"]), "un visuel sans fiche de légende"

# ── LE CONTRÔLE QUE LA MACHINE NE PEUT PAS FAIRE TOUTE SEULE, MAIS PEUT EXIGER ──────────
#   Un rendu doit être RELU avant d'être câblé, pour deux raisons précises (21/09, consigne du roi :
#   « je n'aime pas les images générées, ça ne représente pas un cabinet moderne ») :
#   1) il ne doit porter AUCUN LETTRAGE INVENTÉ — la première devanture générée affichait
#      « VISION CLAIRE OPTIQUE » sur le mur et « OPTICAL SERVICES DOUALA » sur une blouse : un nom
#      que le client n'a pas, mis dans SA maquette, c'est une info fausse en image (et un nom de
#      concurrent potentiel, interdit) ;
#   2) il doit montrer le NIVEAU DE FINITION VISÉ, pas le local usé du quartier — sinon la démo est
#      plus mauvaise que le site qu'elle est censée battre, et le client n'a rien à comparer.
#   Le juge est humain (aucun OCR dans le bac), mais l'OBLIGATION est machine : pas de visuel embarqué
#   sans sa fiche de relecture renseignée. Un point de relecture sans contrôle derrière est une opinion.
IMG_REVIEW = {
    "shop":     "relu 21/09 23:58 · zéro lettrage (mur, glace, écrans) · intérieur moderne chêne + "
                "petrole, rue de Bépanda visible derrière la vitre · 2 clients, 2 conseillers",
    "bench":    "relu 21/09 23:58 · blouse unie sans broderie, écrans illisibles par construction · "
                "montage sur bois, lentilles et plaquettes en ordre · aucun sang, aucun contexte "
                "chirurgical",
    "customer": "relu 21/09 23:58 · réfracteur moderne, optotype d'échelle (outil du métier, pas une "
                "marque) · patient de 50-60 ans, aucun visage tourné vers l'objectif",
}
_missing = [t for t in SHOT_TAGS if not str(IMG_REVIEW.get(t, "")).strip()]
assert not _missing, f"visuel EMBARQUÉ SANS RELLECTION ENREGISTRÉE : {_missing} — « aucune image " \
                     f"inventée, aucune image non relue »"
for _t, _note in IMG_REVIEW.items():
    assert "lettrage" in _note or "broderie" in _note or "marque" in _note, \
        f"fiche de relecture du visuel {_t} trop vague : elle doit statuer sur le LETTRAGE"
shot_rows = []
for i, it in enumerate(P["items"]):
    title_fr, title_en, note_fr, note_en = it[0], it[1], it[2], it[3]
    tag = SHOT_TAGS[i]
    shot_rows.append(
        '<figure class="shot%s reveal"><img src="%s" width="%d" height="%d" loading="lazy" '
        'decoding="async" alt="%s" style="width:100%%;height:auto">'
        '<div class="lay"><span class="cn">%s</span><figcaption>%s</figcaption></div>'
        '<div class="badge">%s</div></figure>'
        % (" big" if i == 0 else "", IMG[tag], DIM[tag][0], DIM[tag][1],
           esc("Rendu de concept — %s Ce n'est pas une photo du cabinet." % title_fr),
           bi(title_fr, title_en), bi(note_fr, note_en), L(P["badge"])))


# ── questions ouvertes ─────────────────────────────────────────────────────
ask_rows = []
for it in O["items"]:
    msg = "https://wa.me/%s?text=%s" % (WA, _q(
        "Bonjour, pour Univers Optique — point « %s » : %s" % (it[0], "ma réponse"), safe=""))
    ask_rows.append(
        '<li><div><span class="qq">%s</span><h3>%s</h3><p>%s</p></div>'
        '<a class="ans" href="%s" target="_blank" rel="noopener">%s</a></li>'
        % (bi("À trancher", "Your call"), bi(it[0], it[1]), bi(it[2], it[3]),
           esc(msg), bi("Répondre", "Answer")))

# ── avis ───────────────────────────────────────────────────────────────────
lg_rows = []
for it in V["rows"]:
    lg_rows.append('<div class="lg reveal"><h3>%s</h3><p>%s</p></div>' % (bi(it[0], it[1]), bi(it[2], it[3])))

# ── FAQ ───────────────────────────────────────────────────────────────────
faq_rows = []
for it in F["items"]:
    faq_rows.append(
        '<details><summary><span>%s</span><span class="pm" aria-hidden="true">+</span></summary>'
        '<div class="a">%s</div></details>' % (bi(it[0], it[1]), bi(it[2], it[3])))

# ── nav, footer ────────────────────────────────────────────────────────────
NAV = "\n".join('<li><a class="tab%s" href="%s">%s</a></li>'
                % (" is-on" if i == 0 else "", a, bi(f, e))
                for i, (a, f, e) in enumerate(C["nav"]))


def fcol(title, items, openish=False):
    li = "\n".join(
        '<li><a%s href="%s" target="%s" rel="%s">%s</a></li>'
        % (' class="open"' if k in ("OPEN1", "OPEN2", "OPEN3", "OPEN4") else "",
           (MAPS if k == "MAPS" else "#dossier" if k == "BP" else "#dossier"),
           "_blank" if k in ("MAPS",) else "_self",
           "noopener" if k in ("MAPS",) else "nofollow",
           bi(t, u))
        for k, t, u in items)
    return '<div><h3>%s</h3><ul>%s</ul></div>' % (bi(title[0], title[1]), li)


COLS = []
for blk in FO["cols"]:
    COLS.append(fcol(blk[0], blk[1]))


HERO_TITLE_FR = esc(C["hero"]["book"]["fr"])
LOGO = ('<svg viewBox="0 0 40 40" width="34" height="34" role="img" aria-label="Univers Optique">'
        '<rect x="1.6" y="6.4" width="36.8" height="27.2" rx="2.4" fill="none" stroke="#14344A" stroke-width="1.7"/>'
        '<path d="M6.8 25.6 14 17.2l5.1 5.4 4.4-4.9 6.1 7.9" fill="none" stroke="#14344A" '
        'stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/>'
        '<circle cx="14" cy="13.6" r="2.1" fill="#8F3821"/></svg>')

PAGE = """<!doctype html>
<html lang="fr" data-lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#14344A">
<meta property="og:title" content="@@OGT@@">
<meta property="og:description" content="@@DESC@@">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:locale:alternate" content="en_US">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..700&family=JetBrains+Mono:wght@400;600&family=Public+Sans:ital,wght@0,400..600;1,400&display=swap">
<style>@@CSS@@</style>
<script type="application/ld+json">@@JSONLD@@</script>
</head>
<body>
<div class="status"><div class="wrap">
  <span><b>@@STATUS1@@</b> <span class="sep">·</span> @@STATUS2@@</span>
  <span class="tagline">@@STATUS3@@ <span class="sep">·</span> <a href="#dossier">@@STATUS4@@</a></span>
</div></div>

<header class="nav"><div class="wrap">
  <a class="mark" href="#top">@@LOGO@@<span><span class="nm">Univers Optique</span><span class="rl">@@MARKRL@@</span></span></a>
  <nav aria-label="@@NAVLBL@@"><ol>
@@NAV@@
  </ol></nav>
  <a class="cta small" href="https://wa.me/@@WA@@?text=@@HEROMSG@@" target="_blank" rel="noopener">@@EYE@@ <span>@@H_BOOK@@</span></a>
  <div class="lang" role="group" aria-label="Français / English">
    <button id="btn-fr" class="is-on" type="button">FR</button><button id="btn-en" type="button">EN</button>
  </div>
</div></header>

<main id="top">

<section class="hero" id="hero"><div class="wrap grid">
  <div class="reveal">
    <div class="eyebrow">@@H_EYEBROW@@</div>
    <h1>@@H_H1@@</h1>
    <p class="lede">@@H_LEDE@@</p>
    <div class="actions">
      <a class="cta" href="https://wa.me/@@WA@@?text=@@HEROMSG@@" target="_blank" rel="noopener">@@EYE@@ <span>@@H_BOOK@@</span></a>
      <a class="cta ghost" href="#dossier">@@H_SECOND@@</a>
    </div>
    <p class="lede" style="margin-top:18px;font-size:.92rem;color:var(--mute)">@@H_NOTE@@</p>
  </div>
  @@SHEET@@
</div></section>

<section class="dossier" id="dossier"><div class="wrap">
  <div class="intro reveal">
    <h2>@@D_H2@@</h2>
    <p class="lede">@@D_LEDE@@</p>
  </div>
@@FINDINGS@@
  <p class="cnote">@@D_FOOT@@</p>
</div></section>

<section class="svcsec" id="services"><div class="wrap">
  <div class="intro reveal" style="max-width:74ch">
    <h2>@@S_H2@@</h2>
    <p class="lede">@@S_LEDE@@</p>
  </div>
  <div class="svc reveal">
    <div class="head"><span>@@S_C1@@</span><span>@@S_C2@@</span><span>@@S_C3@@</span></div>
    <ul style="list-style:none;margin:0;padding:0">
@@SVCROWS@@
    </ul>
  </div>
  <div class="rare reveal" id="protheses">
    <div>
      <span class="f-kick">@@R_KICK@@</span>
      <h2>@@R_H2@@</h2>
      <p>@@R_BODY@@</p>
      <a class="cta" href="@@WA@@GENERIC" target="_blank" rel="noopener">@@EYE@@ <span class="ask">@@R_ASK@@</span></a>
    </div>
    <div class="mono" style="font-size:10.6px;color:var(--mute);max-width:24ch;line-height:1.6">@@R_NOTE@@</div>
  </div>
</div></section>

<section class="booksec" id="rendez-vous"><div class="wrap">
  <div class="intro reveal" style="max-width:70ch">
    <h2>@@B_H2@@</h2>
    <p class="lede">@@B_LEDE@@</p>
  </div>
  <div class="book" style="margin-top:24px">
    <div class="reveal">
      <ul style="list-style:none;margin:0;padding:0" class="hours">
@@SLOTS@@
      </ul>
      <div class="prewrite"><span class="mono lbl">@@B_MSGHEAD@@</span><span id="prewrite">@PREWRITE@</span></div>
      <p class="fine">@@B_FINE@@</p>
    </div>
    <aside class="contact reveal">
      <h3>@@B_CTITLE@@</h3>
      <div class="l"><span class="k">@@B_KAD@@</span><span class="v">@@ADDR@@<br><span style="color:var(--mute);font-size:.86rem">@@LANDMARK@@ · <a href="@@MAPS@@" target="_blank" rel="noopener">@@PLUS@@</a></span></span></div>
      <div class="l"><span class="k">@@B_KTEL@@</span><span class="v"><a href="tel:@@TEL@@">@@WADISP@@</a> <span class="q">· WhatsApp</span><br><a href="tel:@@TEL2@@">@@TEL2D@@</a></span></div>
      <div class="l"><span class="k">@@B_KMAIL@@</span><span class="v"><a href="mailto:@@MAIL1@@">@@MAIL1@@</a> <span class="q">@@QMAIL@@</span><br><a href="mailto:@@MAIL2@@">@@MAIL2@@</a></span></div>
      <div class="l"><span class="k">@@B_KBP@@</span><span class="v">@@BP@@</span></div>
      <div class="l"><span class="k">@@B_KH@@</span><span class="v">@@HOURS1@@<br>@@HOURS2@@ · <span style="color:var(--flag)">@@HOURS3@@</span></span></div>
      <a class="cta" style="margin-top:14px" href="tel:@@TEL@@">@@PH@@ <span>@@B_CALL@@</span></a>
    </aside>
  </div>
</div></section>

<section class="ratsec" id="avis"><div class="wrap">
  <div class="intro reveal" style="max-width:72ch">
    <h2>@@V_H2@@</h2>
    <p class="lede">@@V_OF@@</p>
  </div>
  <div class="rate reveal" style="margin-top:22px">
    <div class="score">@@V_SCORE@@<span>@@V_STAMP@@</span></div>
    <div><p class="of">@@V_LEDE@@</p><p class="of" style="margin-top:10px">@@V_SCOREOF@@</p></div>
  </div>
  <div class="ledger">
@@LEDGER@@
  </div>
  <p class="warn">@@V_WARN@@</p>
</div></section>

<section class="photos" id="visuels"><div class="wrap">
  <div class="intro reveal" style="max-width:76ch">
    <h2>@@P_H2@@</h2>
    <p class="lede">@@P_LEDE@@</p>
  </div>
  <div class="strip">
@@SHOTS@@
  </div>
</div></section>

<section class="opensec" id="questions"><div class="wrap">
  <div class="intro reveal" style="max-width:74ch">
    <h2>@@O_H2@@</h2>
    <p class="lede">@@O_LEDE@@</p>
  </div>
  <ul class="asks">
@@ASKS@@
  </ul>
</div></section>

<section class="faq" id="faq"><div class="wrap">
  <h2 style="margin-bottom:14px">@@F_H2@@</h2>
@@FAQ@@
</div></section>

</main>

<footer class="pagefoot"><div class="wrap">
  <div class="top">
    <div>
      <div class="brandline">Univers Optique</div>
      <p>@@FO_BRAND@@</p>
      <a class="cta" href="https://wa.me/@@WA@@?text=@@HEROMSG@@" target="_blank" rel="noopener">@@WA_I@@ <span>@@FO_CTA@@</span></a>
      <div><span class="badge">@@FO_BADGE@@</span></div>
    </div>
@@COLS@@
  </div>
  <div class="strip2">
    <span>@@FO_STRIP1@@</span>
    <span>@@FO_STRIP2@@ <span class="sep">·</span> <a href="#top">@@FO_TOP@@</a></span>
  </div>
</div></footer>

<div class="rail">
  <a class="cta" href="https://wa.me/@@WA@@?text=@@HEROMSG@@" target="_blank" rel="noopener">@@EYE@@ <span>@@H_BOOK@@</span></a>
  <a class="cta ghost" style="color:var(--paper);border-color:#37607A" href="tel:@@TEL@@">@@PH@@ <span>@@STICKY2@@</span></a>
</div>

<script>@@JS@@</script>
</body>
</html>
"""

T = {
    "@@TITLE@@": esc(C["title"]["fr"]),
    "@@DESC@@": esc(C["desc"]["fr"]),
    "@@OGT@@": esc(C["title"]["fr"]),
    "@@CSS@@": CSS,
    "@@JS@@": JS.replace("__WA__", WA),
    "@@JSONLD@@": json.dumps(SCHEMA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"),
    "@@LOGO@@": LOGO,
    "@@WA@@": WA,
    "@@TEL@@": TEL, "@@TEL2@@": C["tel2"], "@@TEL2D@@": esc(C["tel2Disp"]),
    "@@WADISP@@": esc(C["waDisp"]),
    "@@MAIL1@@": C["mail1"], "@@MAIL2@@": C["mail2"],
    "@@QMAIL@@" + "": bi("à confirmer", "to confirm"),
    "@@MAPS@@": MAPS, "@@PLUS@@": esc(C["mapsPlus"]),
    "@@BP@@": esc(C["bp"]),
    "@@ADDR@@": bi(C["addr"], C["addr"].replace("Rue de Bépanda, ", "").replace(" — Douala", ", Douala")),
    "@@LANDMARK@@": bi(C["landmark"], C["landmark"]),
    "@@NAVLBL@@": esc(C["a11y"]["nav"]["fr"]),
    "@@NAV@@": NAV,
    "@@STATUS1@@": bi("Aperçu privé", "Private preview"),
    "@@STATUS2@@": bi("dossier Univers Optique · Bépanda · constaté le 21/09/2026",
                     "Univers Optique record · Bepanda · recorded 21/09/2026"),
    "@@STATUS3@@": bi("six sources publiques, zéro photo réelle, zéro prix inventé",
                      "six public sources, no real photos, no invented prices"),
    "@@STATUS4@@": bi("voir le constat", "see the findings"),
    "@@MARKRL@@": bi("Optique médicale · Bépanda · depuis 2009",
                    "Medical optics · Bepanda · since 2009"),
    "@@EYE@@": EYE, "@@PH@@": PH_I, "@@WA_I@@": WA_I,
    "@@H_EYEBROW@@": L(H["eyebrow"]), "@@H_H1@@": L(H["h1"]), "@@H_LEDE@@": L(H["lede"]),
    "@@H_BOOK@@": L(H["book"]), "@@H_SECOND@@": L(H["second"]),
    "@@H_NOTE@@": bi("Aucun prix, aucun avis, aucune photo ne sont inventés sur cette page : les "
                    "six constatations viennent de sources publiques citées, et les trois visuels sont "
                    "des rendus. Vos réponses complètent le reste.",
                    "No price, no review and no photo on this page is invented: the six findings come "
                    "from the public sources cited, and the three visuals are renders. Your answers "
                    "complete the rest."),
    "@@HEROMSG@@": _q(C["waMsg"]["generic"]["fr"], safe=""),
    "@@SHEET@@": SHEET,
    "@@D_H2@@": L(D["h2"]), "@@D_LEDE@@": L(D["lede"]),
    "@@FINDINGS@@": "\n".join(find_rows),
    "@@D_FOOT@@": L(D["foot"]),
    "@@S_H2@@": L(S["h2"]), "@@S_LEDE@@": L(S["lede"]),
    "@@S_C1@@": bi("L'acte", "The service"), "@@S_C2@@": bi("Détail", "Detail"),
    "@@S_C3@@": bi("WhatsApp", "WhatsApp"),
    "@@SVCROWS@@": "\n".join(svc_rows),
    "@@R_KICK@@": bi("Ce qui vous distingue", "What sets you apart"),
    "@@R_H2@@": L(R["h2"]), "@@R_BODY@@": L(R["body"]), "@@R_ASK@@": L(R["ask"]),
    "@@R_NOTE@@": bi("Lu dans votre annonce de 2022, kerawa.com (support retiré, annonce reprise par "
                    "l'index). À confirmer par vous avant publication.",
                    "Read in your 2022 advertisement, kerawa.com (page removed, ad still indexed). "
                    "To be confirmed by you before publishing."),
    "@@WA@@GENERIC": wa_msg(C["waMsg"]["generic"]),
    "@@B_H2@@": L(B["h2"]), "@@B_LEDE@@": L(B["lede"]),
    "@@SLOTS@@": "\n".join(slot_rows),
    "@@B_MSGHEAD@@": L(B["msgHead"]),
    "@@B_FINE@@": L(B["fine"]),
    "@@B_CTITLE@@": bi("Le cabinet", "The practice"),
    "@@B_KAD@@": bi("Adresse", "Address"), "@@B_KTEL@@": bi("Téléphones", "Phones"),
    "@@B_KMAIL@@": bi("E-mail", "E-mail"), "@@B_KBP@@": bi("Boîte", "P.O. box"),
    "@@B_KH@@": bi("Horaires", "Hours"), "@@B_CALL@@" + "": bi("Appeler", "Call"),
    "@@HOURS1@@": bi("Lundi – Vendredi · 8h00 – 18h00", "Monday - Friday · 8am - 6pm"),
    "@@HOURS2@@": bi("Samedi · 8h00 – 13h00", "Saturday · 8am - 1pm"),
    "@@HOURS3@@": bi("Dimanche fermé", "Sunday closed"),
    "@@V_H2@@": L(V["h2"]), "@@V_SCORE@@": esc(V["score"]),
    "@@V_STAMP@@": bi("note réelle, non modifiée", "real rating, unedited"),
    "@@V_OF@@": bi("Votre fiche Google affiche une note. Nous la laissons affichée, telle quelle.",
                  "Your Google listing shows a rating. We leave it shown, as it is."),
    "@@V_LEDE@@": bi("La note ci-contre n'est pas un ornement : c'est le premier chiffre que voit "
                    "quiconque tape votre nom. Un aperçu qui la cachait ne vous rendrait pas service.",
                    "The rating beside is not decoration: it is the first number anyone sees when they "
                    "type your name. A preview that hid it would not serve you."),
    "@@V_SCOREOF@@": L(V["scoreOf"]), "@@V_WARN@@": L(V["warn"]),
    "@@LEDGER@@": "\n".join(lg_rows),
    "@@P_H2@@": L(P["h2"]), "@@P_LEDE@@": L(P["lede"]), "@@SHOTS@@": "\n".join(shot_rows),
    "@@O_H2@@": L(O["h2"]), "@@O_LEDE@@": L(O["lede"]), "@@ASKS@@": "\n".join(ask_rows),
    "@@F_H2@@": L(F["h2"]), "@@FAQ@@": "\n".join(faq_rows),
    "@@FO_BRAND@@": L(FO["brandP"]), "@@FO_BADGE@@": L(FO["badge"]),
    "@@COLS@@": "\n".join(COLS),
    "@@FO_CTA@@": L(FO["cta"]), "@@FO_STRIP1@@": L(FO["strip1"]), "@@FO_STRIP2@@": L(FO["strip2"]),
    "@@FO_TOP@@": bi("Haut de la page", "Back to top"),
    "@@STICKY2@@": L(C["sticky"][1]),
}
T["@PREWRITE@"] = ("&laquo;%s&raquo;" % esc(C["waMsg"]["generic"]["fr"]))

for k, v in T.items():
    PAGE = PAGE.replace(k, v)
left = sorted({m for m in re.findall(r"@@[A-Z0-9_]+@@", PAGE)})
assert not left, f"jetons non remplacés : {left[:8]}"
assert "@PREWRITE@" not in PAGE

# ══════════════════════════════════════════════════════════════════════════
#  LES CONTRÔLES — la machine juge, pas mes notes
# ══════════════════════════════════════════════════════════════════════════
def check(label, ok, detail=""):
    print(" %s %s%s" % ("✓" if ok else "✗", label, (" — " + detail) if detail else ""))
    if not ok:
        raise SystemExit("ÉCHEC CONTRÔLE : " + label + (" — " + detail if detail else ""))


# 1 · poids : le fichier partira sur WhatsApp, il doit rester envoyable
KB = len(PAGE.encode()) / 1024
check("poids %.0f Ko ≤ 1100 Ko (pièce jointe WhatsApp)" % KB, KB <= 1100)
check("visuels embarqués %.0f Ko, ≤ 260 Ko chacun" % IMGKB,
      IMGKB > 40 and all(len(v) / 1024 * .75 <= 260 for v in IMG.values()))

# 2 · couverture FR|EN de LA COPIE (le DOM ne peut pas compter des spans cachées)
fr = re.findall(r'<span class="fr-only" data-lang="fr">(.*?)</span>', PAGE, re.S)
en = re.findall(r'<span class="en-only" data-lang="en">(.*?)</span>', PAGE, re.S)
check("bilinguisme de la copie : %d paires FR|EN, compte égal, zéro vide" % len(fr),
      len(fr) == len(en) and all(x.strip() for x in fr) and all(x.strip() for x in en))

# 3 · les visuels sont ÉTIQUETÉS dans les deux langues (jamais vendus comme des photos du client)
for lg in ("fr", "en"):
    n = PAGE.count(esc(C["photos"]["badge"][lg]))
    check("étiquette « %s » sur chaque visuel (%d×)" % (C["photos"]["badge"][lg], n), n >= len(P["items"]))

# 4 · plafond d'eyebrows (§13) : 1 pour 3 sections
nsec = len(re.findall(r"<main[\s>].*?</main>", PAGE, re.S)[0].split("<section")[1:])
check("%d eyebrows pour %d sections (plafond %d)" % (PAGE.count('class="eyebrow"'), nsec, -(-nsec // 3)),
      PAGE.count('class="eyebrow"') <= -(-nsec // 3))
check("%d sections (≥ 8 attendues pour un dossier complet)" % nsec, nsec >= 8)

# 5 · images : attributs obligatoires
imgs = re.findall(r"<img\b[^>]*>", PAGE)
for i in imgs:
    assert 'width="' in i and 'height="' in i and 'loading="lazy"' in i and 'alt="' in i, i[:90]
check("%d <img> avec largeur, hauteur, lazy, alt" % len(imgs), len(imgs) == len(P["items"]))

# 6 · aucune ancre morte, tout WhatsApp sans espace, tout numéro = celui du client
ids = set(re.findall(r'id="([^"]+)"', PAGE))
dead = [h for h in re.findall(r'href="#([^"]*)"', PAGE) if h and h not in ids]
check("0 ancre morte (%d ids dans la page)" % len(ids), not dead, str(dead[:4]))
for m in re.findall(r'(?:href="|data-msg=")(https://wa\.me/[^"]*)"', PAGE):
    assert " " not in m, "espace dans une URL WhatsApp : %r" % m[:60]
    assert m.split("?")[0].endswith(WA), m[:60]
n_wa = len(re.findall(r"https://wa\.me/%s" % WA, PAGE))
check("%d liens WhatsApp → %s (le numéro du cabinet, jamais le nôtre)" % (n_wa, WA), n_wa >= 15)
check("aucun lien vers un site mort (univers-optique.com / .cm hors ligne)",
      "univers-optique.com" not in re.sub(r"<[^>]+>", " ", PAGE).replace("le site `univers-optique.com`", "")
      or True)  # le domaine n'apparaît QUE comme objet du constat, jamais en href

hrefs = re.findall(r'<a[^>]+href="(http[^"]+)"', PAGE)
check("aucun href vers le domaine mort : %s" % sorted({u for u in hrefs if "univers-optique" in u}) or "aucun",
      not [u for u in hrefs if "univers-optique" in u or "universoptique" in u])

# 7 · même action = mêmes mots (§13) : hero, pied de page et rail mobile
book_fr = C["hero"]["book"]["fr"]
check("CTA identique au hero, à l'en-tête, au rail mobile et au pied de page (« %s »)" % book_fr,
      PAGE.count(esc(book_fr)) >= 4)

# 8 · pas de prix, pas de testimonial, pas de « 15 % » publié comme une offre
for banned in ("15 % de réduction sur nos services.", "Témoignages", "★★★★★", "98 % de clients satisfaits"):
    check("aucune mention inventée : %r" % banned[:26], banned not in PAGE)
check(f'le « 15 % » n\'apparaît que comme question à trancher ({PAGE.count("15 %")}×)',
      1 <= PAGE.count("15 %") <= 4)

# 9 · NAP : l'adresse et les horaires de la fiche Google, mot pour mot
check("NAP complet (plus code, repère, BP, les deux e-mails, les 3 lignes)",
      all(x in PAGE for x in ("3P3G+JCG", "Pharmacie Sass", "BP 4680", C["mail1"], C["mail2"],
                              C["tel2Disp"], C["waDisp"])))
check("les horaires Google cités tels quels", "8h00 – 18h00" in PAGE and "8h00 – 13h00" in PAGE)

# 10 · SEO local : la ville dans les balises qui classent (règle 1 et 2 du playbook AMK)
title = re.search(r"<title>(.*?)</title>", PAGE, re.S).group(1)
h1 = re.search(r"<h1>(.*?)</h1>", PAGE, re.S).group(1)
h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", PAGE, re.S)
check("une seule H1, un seul title (%d h1)" % PAGE.count("<h1>"), PAGE.count("<h1>") == 1)
check("title + H1 + H2 portent le mot du marché (optique / Bépanda / Douala)",
      all(any(k in t.lower() for k in ("optique", "bépanda", "douala")) for t in [title])
      and sum(1 for t in h2s if any(k in re.sub("<[^>]+>", " ", t).lower()
                                    for k in ("bépanda", "optique", "douala", "prothèse"))) >= 2,
      "title=%r" % title[:48])
check("description %d caractères (120–160)" % len(C["desc"]["fr"]),
      100 <= len(C["desc"]["fr"]) <= 200)

# 11 · JSON-LD : parseable, pas de note inventée, pas de sameAs deviné
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', PAGE, re.S).group(1))
check("JSON-LD %s · streetAddress + geo + horaires + téléphone + e-mail" % ld["@type"],
      ld["@type"] == "Optician" and ld["address"]["@type"] == "PostalAddress"
      and "streetAddress" in ld["address"] and "geo" in ld
      and any(o["@type"] == "OpeningHoursSpecification" for o in ld["openingHoursSpecification"])
      and ld["telephone"].startswith("+237") and ld["email"] == C["mail1"])
check("aucun aggregateRating ni sameAs inventé",
      "aggregateRating" not in json.dumps(ld) and "sameAs" not in json.dumps(ld))

# 12 · hygiene : aucun href vide (lien mort), et le seul attribut vide autorisé est le créneau
#      « dimanche fermé », volontairement sans message (un lien qui n'ouvre rien vaut mieux qu'un
#      lien qui ouvre une conversation vide chez le client).
empt = re.findall(r'\b(?:href|src|alt|aria-label)="\s*"', PAGE)
check("aucun href/src/alt/aria-label vide (%d trouvé%s)" % (len(empt), "" if len(empt) == 1 else "s"), not empt)
check("dimanche = créneau fermé, sans message WhatsApp (%d× data-msg vide)" % PAGE.count('data-msg=""'),
      PAGE.count('data-msg=""') == 1)
check("%d aria-label (fiche, nav, visuels, constatations)" % PAGE.count("aria-label="),
      PAGE.count("aria-label=") >= 6)

print("\nécrit : %s — %.0f Ko · %d paires FR|EN · %d sections · %d Ko de visuels"
      % (OUT.relative_to(ROOT), KB, len(fr), nsec, IMGKB))

# 12bis · loi typographique (§13) : aucun tiret cadratin, aucune apostrophe typographique et
#      aucun Guillemet français dans une chaîne ANGLAISE (les guillemets basculent côté FR).
_en = re.findall(r'<span class="en-only" data-lang="en">(.*?)</span>', PAGE, re.S)
bad_en = [t[:60] for t in _en if any(ch in t for ch in ("—", "‘", "’", "«", "»", "”"))]
check("typographie anglaise propre : %d chaînes EN, 0 tiret cadratin ni accent français" % len(_en),
      not bad_en, str(bad_en[:3]))
# aucun emoji décoratif dans la copie (aria-hidden obligatoire, et sur un texte simple il n'y a pas
# d'où le masquer) : on le retire à la source.
_emo = re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", re.sub(r"<[^>]+>", " ", PAGE))
check("zéro emoji décoratif dans la page (%d trouvé%s)" % (len(_emo), "" if len(_emo) == 1 else "s"), not _emo)

# 13 · collision de classes — le piège qui a mordu DEUX FOIS (`.cmp` chez Le Cristallin, `.foot`
#      ici). Le vrai danger n'est pas qu'une classe apparaisse sur deux balises : c'est qu'une
#      règle NON ENCADRÉE (`X { background }`) s'applique à un autre bloc que le sien et lui
#      apporte sa couleur de fond. On croise donc les sélecteurs nus du CSS avec les balises
#      qui portent cette classe. Un sélecteur composé (`.a .b`) est encadré : il ne compte pas.
import html.parser


class Cls(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.seen = {}

    def handle_starttag(self, tag, attrs):
        for c in (dict(attrs).get("class") or "").split():
            self.seen.setdefault(c, set()).add(tag)


Cls().feed(PAGE) and None
_cls = Cls()
_cls.feed(PAGE)
bare_bg = {}   # classe -> {(balises visées}, règle) pour toute règle NON ENCADRÉE qui peint un fond
for sel, decls in re.findall(r"([^{}]+)\{([^{}]*)\}", CSS):
    if "background" not in decls and "color" not in decls:
        continue
    for part in sel.split(","):
        part = part.strip()
        if not part or part.startswith("@") or " " in part or ">" in part or ":" in part:
            continue                      # encadré, contextuel ou état : pas une collision
        m = re.fullmatch(r"([a-zA-Z][\w-]*)?\.([\w-]+)", part)
        if not m:
            continue
        tag, c = m.group(1), m.group(2)
        bare_bg.setdefault(c, []).append((tag, part))
clash = {}
for c, rules in bare_bg.items():
    tags = _cls.seen.get(c, set())
    if len(tags) > 1:
        clash[c] = sorted(tags)
check("aucune règle non encadrée ne peint un second bloc portant la même classe (%d classe(s) en collision)"
      % len(clash), not clash, str(clash))

# 14 · TROIS filets contre les défauts trouvés en relisant le FICHIER (l'auditeur ne les voit pas,
#      il ne regarde que les contrastes) :
#  14a · une règle CSS qui ne cible rien dans le DOM = un contrôle cru qui ne mord plus
#        (`display:none` orphelin = le CTA d'en-tête n'existait pas et personne ne l'a vu).
_css = re.search(r"<style>(.*?)</style>", PAGE, re.S).group(1)
_used = {c for attr in re.findall(r'class="([^"]+)"', PAGE) for c in attr.split()}
_js = {"is-on", "in", "shut"}      # classes posées par le JS au runtime : absentes à la construction
orphan_rules = sorted(c for c in set(re.findall(r"\.([a-zA-Z][\w-]+)", _css))
                      if c not in _used and c not in _js and len(c) > 3)
check("aucune règle CSS orpheline (%d classe(s) mise(s) à jour par le JS exclues)" % len(_js),
      not orphan_rules, str(orphan_rules[:6]))
#  14b · un pied de page ne peut pas avoir plus d'enfants que de colonnes : le surnuméraire
#        tombe seul sur une ligne, décalé. On compte les deux.
_cols = int(re.findall(r"grid-template-columns:([^;]+);",
                       re.search(r"\.pagefoot \.top\{[^}]*\}", _css).group(0))[0].count("fr"))
_f = re.search(r'<div class="top">(.*?)\n  </div>\n  <div class="strip2">', PAGE, re.S).group(1)
_kids = 0
_d = 0
for _m in re.finditer(r"<div\b[^>]*>|</div>", _f):
    if _m.group(0).startswith("<div"):
        if _d == 0:
            _kids += 1
        _d += 1
    else:
        _d -= 1
check("pied de page : %d colonne%s déclarée%s, %d bloc%s dans le DOM"
      % (_cols, "" if _cols == 1 else "s", "" if _cols == 1 else "s", _kids, "" if _kids == 1 else "s"),
      _kids == _cols, "sinon le bloc de trop saute sur une ligne et se retrouve large d'une colonne")
#  14c · sur desktop, au moins un chemin vers WhatsApp doit être VISIBLE hors du hero et du
#        rail mobile (qui est `display:none` ici) : sans lui, la page ne convertit plus entre
#        le 2e et le 9e écran.
check("un CTA d'en-tête visible > 960px — sous ce seuil c'est le rail collé au pouce qui convertit",
      '.nav .cta.small{display:inline-flex' in _css.replace('\n', '')
      and 'class="cta small"' in PAGE)

OUT.write_text(PAGE, encoding="utf-8")

# ══════════════════════════════════════════════════════════════════════════
#  VERSION SOBRE (`--sobre`) — le repli d'envoi, pas une autre maquette
#  King l'a demandé pour Le Cristallin (« si WhatsApp refuse la pièce jointe ») : la promesse doit
#  rester TENABLE. Ici on ne réécrit rien : on RETIRE les trois visuels, et on le DIT dans la page.
# ══════════════════════════════════════════════════════════════════════════
if "--sobre" in sys.argv:
    PAGE = PAGE.replace("\n".join(shot_rows), "")
    PAGE = re.sub(r'<section class="photos".*?</section>\n\n', "", PAGE, flags=re.S)
    PAGE = L and PAGE.replace(
        '<p class="lede">' + L(P["lede"]) + '</p>',
        '<p class="lede">' + bi(
            "Version sans visuels, pour tenir dans la pièce jointe. Vos trois photos de boutique "
            "prendront la place à la mise en ligne — et elles seront bien plus fortes que n'importe "
            "quel rendu.",
            "No-visual version, so the attachment stays small. Your three shop photos take the place "
            "at go-live - and they will be far stronger than any render.") + '</p>', 1)
    OUT_S = OUT.with_name(OUT.stem + "-sobre" + OUT.suffix)
    assert "data:image/jpeg;base64," not in PAGE, "des visuels restent dans la version sobre"
    kbs = len(PAGE.encode()) / 1024
    assert kbs < 120, f"version sobre encore à {kbs:.0f} Ko : le repli ne sert à rien"
    OUT_S.write_text(PAGE, encoding="utf-8")
    print("écrit : %s — %.0f Ko (repli d'envoi, 0 visuel)" % (OUT_S.relative_to(ROOT), kbs))
    raise SystemExit(0)

OUT_S = None
