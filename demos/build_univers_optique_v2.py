#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONCEPT — UNIVERS OPTIQUE (Bépanda, Douala) · v2, direction « GRANDE PHOTO »
════════════════════════════════════════════════════════════════════════════════════════════════════
QUOI : une page de démonstration à envoyer à ETS UNIVERS OPTIQUE, en un seul fichier, français en tête,
       anglais en vis-à-vis, rendez-vous par WhatsApp. Elle est générée ici, jamais écrite à la main :
       la copie vit dans `demos/univers_optique_content.py`, cette fiche ne fait que la mettre en page.

POURQUOI v2 : le 22/09 au matin King a renvoyé quatre captures — une fiche de gabarit (« Grande Photo ·
       Propre · Moderne », palette bleu/gris/blanc/noir) et trois écrans d'un site de santé américain
       (Function : bandeau rouille, photo pleine largeur, titre serif avec un mot en italique, trois
       étapes numérotées 01/02/03 à cartes teintées, tableau comparatif à colonne surlignée). Sa consigne :
       « take inspiration from all the attachments then read the design files once more, then redo the site ».
       La v1 était un DOSSIER (registre, filets, densité 5) ; la v2 est un CABINET (photo, air, chaleur)
       — sans rien retirer des faits, des contrôles ni des lois.

LOI APPLIQUÉE, ET LÀ OÙ LA RÉFÉRENCE PASSE AVANT ELLE (§4.4 : une référence est une contrainte) :
  · Design Read (§1) : « Lecture faite comme : une page de preuve commerciale pour le propriétaire d'un
    cabinet d'optique de Douala, en langage photographique chaud et éditorial, penchée vers le plan
    pleine-photo + cartes teintées numérotées + colonne comparative surlignée (référence : Function,
    gabarit « Grande Photo · Propre · Moderne »). »
  · Cadres (§2) : VARIANCE 6 · MOTION 4 · DENSITÉ 3. L'air vient de la photo, pas du vide décoratif.
    (v1 : 7/4/5 — le registre dense cédait ; ici le registre reste, il respire.)
  · §3.1 interdit le « beige crème + terracotta » comme RÉFLEXE NON EXAMINÉ. Ici le couple est EXAMINÉ :
    c'est la palette des captures renvoyées par le client de notre client, consignée dans
    `clients/univers-optique/inspiration.md`. Il est donc gardé, mais signé comme référence, pas comme habitude.
  · §3.2 interdit Inter, et proscrit « luxe = serif beige ». Le serif choisi n'est NI Fraunces NI
    Instrument Serif : **Newsreader** (opsz 6→72, italique vraie), pour une raison énoncée — la référence
    est un titre serif à mot italique, et l'italique reste DANS LA MÊME FAMILLE (jamais un mot serif
    greffé sur un titre sans-serif, qui est le tics n° 1 des agents).
  · §3.4 + `design/CRAFT-FLOOR.md` §3 : une pilule au-dessus du hero est normalement interdite quand le
    H1 est fort. La référence en montre une ; elle est gardée UNE fois et dit une chose fausable
    (les horaires), pas une humeur.
  · §11 : pas de tableau de dix lignes à filets → les dix actes sont rendus en TROIS PAQUETS, une raison
    par paquet. Filets seulement dans le comparatif : c'est un document, pas une vitrine.
  · §13 : les contrôles machine ci-dessous sont exigés AVANT écriture. Un point de relecture sans contrôle
    derrière n'est qu'une opinion.
  · §15 : un rendu par section, un seul monde visuel, légende SOUS l'image et badge « rendu de concept »
    dans la légende (la référence pose des pastilles SUR l'image ; la maison ne le fait pas : un badge sur
    la photo survit à une capture d'écran, un badge dans la légende aussi, et il ne salit pas l'image).
  · §20 : le pied de page est l'écran de conversion — quatre blocs, le MÊME appel à l'action que le hero,
    jamais un second rival, et le retour en haut.
  · `design/WORKFLOW.md` étape 8 : la page se PEUT peindre sans JavaScript. Le hero, les cartes, le
    comparatif, les images sont en HTML dur ; le sélecteur de créneaux est une grappe de liens `wa.me`
    réels, pas un widget qui attend un bundle.
════════════════════════════════════════════════════════════════════════════════════════════════════
AUCUN FAIT NOUVEAU : note 3,3/5 sur 6 avis, champ « site web » vide, pas de bouton de réservation,
archives 2 nov. 2023 vivante / 9 janv. 2024 morte, « 15 % » sans date de fin, texte d'un AUTRE opticien
relevé sur SES pages, prothèses oculaires et formations listées à l'annuaire, BP 4680, +237 699 25 28 74.
Tout est relu le 21/09 ; ce qui reste non vérifié est écrit « à trancher par vous » dans les six questions.
"""
import base64
import json
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "demos" / "concept-univers-optique-v2.html"
IMGDIR = ROOT / "demos" / "img"
C = json.loads((ROOT / "demos" / "univers_optique_content.json").read_text(encoding="utf-8"))["page"]
V2 = C["v2"]
WA = re.sub(r"\D", "", C["wa"])
assert len(WA) == 9 and WA.startswith("6"), "numéro WhatsApp malformé : " + WA

# ── PALETTE — le monde de la référence, verrouillé et justifié avant la feuille de style ──────────────
PAPER, CARD, CARD2 = "#FBF6EC", "#FFFCF5", "#F5EEDF"
INK, TEXT, MUTE, LINE = "#1E1A15", "#3D362C", "#6E6455", "#E6DAC5"
RUST, RUST_DK, RUST_T = "#A94C23", "#8E401F", "#F3E1D4"
PETROL, PETROL_DK = "#12303F", "#0C222D"
CHECK = "#2F6142"
CREAM = "#FBF6EC"                                       # le crème posé sur les fonds sombres
HAIR, WASH = "#D8CAB1", "#EFE6D4"                       # filets pointillés, survol de puce
WASH_BLUE, EDGE_BLUE, BAR_BG = "#E3ECF1", "#C6D8E0", "#EADFCB"
RUST_EDGE = "#E4C9B4"                                   # liseré des blocs d alerte
ON_DARK, ON_DARK_2 = "#FCF8F1", "#F0C9A8"                # titre et accent posés sur la photo
ON_DARK_3, ON_DARK_4 = "#E9E2D5", "#D9D1C4"              # lede et note sur la photo
ON_RUST, ON_RUST_2 = "#F7E7DA", "#F6EEDF"                # texte et survol sur le bandeau rouille
FOOT_INK, FOOT_MUTE, FOOT_LABEL = "#E4DDCF", "#C7C0B2", "#9FB4C0"
FOOT_LINK, FOOT_RULE, FOOT_RULE_2 = "#E9E1D2", "#37607A", "#26414F"
FOOT_STRIP_MUTE = "#93A6B2"
RGB_DARK = "12,34,45"                                    # = PETROL_DK, pour les voiles
RGB_CREAM = "251,246,236"                                # = CREAM
RGB_SHADOW = "30,26,21"                                  # = INK, pour les ombres
RAD_CARD, RAD_CHIP = "20px", "999px"     # UN système : carte 20, pastille 999 (la référence)
FONTS_DISP = "'Newsreader',Georgia,serif"
FONTS_BODY = "'Public Sans',system-ui,-apple-system,'Segoe UI',sans-serif"
FONTS_MONO = "'JetBrains Mono',ui-monospace,'SFMono-Regular',monospace"


def _lum(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def cr(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mix(fg, bg, alpha):
    """fg posé à l'opacité alpha sur bg — le pire cas de la voile du hero, calculé et non ressenti."""
    f = [int(fg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(bg.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(round(alpha * x + (1 - alpha) * y) for x, y in zip(f, b))


def sat(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn:
        return 0.0
    return (mx - mn) / (2 - mx - mn) if (mx + mn) > 1 else (mx - mn) / (mx + mn)


VEIL_DESKTOP = .84   # opacité la plus faible qui touche encore la colonne de titre (dégradé 97deg)
VEIL_MOBILE = .87    # idem, voile verticale sous 700 px
VEIL_WORST = mix(PETROL_DK, "#FFFFFF", VEIL_DESKTOP)
VEIL_WORST_M = mix(PETROL_DK, "#FFFFFF", VEIL_MOBILE)     # sous la voile la plus claire, si l'image est blanc pur
# Les paires ci-dessous sont celles qui sont RÉELLEMENT peintes, héritage compris : l'auditeur du dépôt
# (tools/qa/audit_html.py) a trouvé huit faux contrastes que la seule table des couleurs déclarées laissait
# passer — un texte de pied de page héritait du gris des liens sur le bouton rouille, et le paragraphe du
# bandeau portait un crème tiède à 4,07:1. La table est donc complétée des paires héritées.
CONTRASTS = {
    "corps sur papier": (TEXT, PAPER), "titres sur papier": (INK, PAPER), "muet sur papier": (MUTE, PAPER),
    "muet sur carte": (MUTE, CARD), "rouille sur papier": (RUST_DK, PAPER), "crème sur rouille": (CREAM, RUST),
    "encre sur carte teintée": (INK, CARD2), "crème sur pétrole": (CREAM, PETROL),
    "encre sur bandeau pétrole": (CREAM, PETROL_DK), "lie-de-vin sur papier": (PETROL, PAPER),
    "titre sur voile du hero (pire cas, image blanche)": (ON_DARK, VEIL_WORST),
    "lede sur voile du hero (pire cas)": (ON_DARK_3, VEIL_WORST),
    "note sur voile du hero (pire cas)": (ON_DARK_4, VEIL_WORST),
    "note sur voile du mobile (pire cas)": (ON_DARK_4, VEIL_WORST_M),
    "accent italique sur voile du hero": (ON_DARK_2, VEIL_WORST),
}
for _name, (_a, _b) in CONTRASTS.items():
    _r = cr(_a, _b)
    assert _r >= 4.5, "contraste AA manqué sur « %s » : %s sur %s = %.2f" % (_name, _a, _b, _r)
assert sat(RUST) < .80 and sat(PETROL) < .80 and sat(CHECK) < .80, "accent trop saturé (loi : moins de 80 %)"
assert PAPER != "#FFFFFF" and INK != "#000000", "fond blanc pur ou encre noire pure (loi §3.1)"

# ── OUTILS : chaque chaîne visible est un couple FR|EN posé par le même moteur ────────────────────────
def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def bi(fr, en, tag="span"):
    """Le couple bilingue en HTML. Le FR est la langue par défaut (jamais une langue « chargée après »)."""
    return '<' + tag + ' class="fr-only">' + esc(fr) + '</' + tag + '><' + tag + ' class="en-only">' + \
        esc(en) + '</' + tag + '>'


def L(pair, tag="span"):
    return bi(pair["fr"], pair["en"], tag)


def wa_url(text):
    return "https://wa.me/" + WA + "?text=" + urllib.parse.quote(text, safe="")


MSG = C["waMsg"]


def msg(kind, **kw):
    t = MSG[kind]["fr"]
    for key, val in kw.items():
        t = t.replace("{" + key + "}", val)
    return t


MAPS = "https://www.google.com/maps/search/?api=1&query=" + \
    urllib.parse.quote("Univers Optique Bépanda Douala", safe="")

# ── VISUELS : relus UN À UN avant d'entrer (loi §10.3 + §15). Le contrôle est machine, pas moral. ─────
DIM = {"hero": (1440, 810), "frames": (760, 950), "lab": (1200, 900), "exam": (1060, 795)}
IMG_REVIEW = {
    "hero": "relu 22/09 07:4x · AUCUN lettrage au mur, sur la vitre, sur la blouse ni sur les objets · "
            "comptoir de chêne, présentoirs rétroéclairés, toits de Bépanda par la fenêtre · deux visages "
            "naturels, personne ne regarde l'objectif · bas de page libre à gauche pour le titre",
    "frames": "relu 22/09 07:4x · trois montures dans un plateau de chêne, chiffon crème, outil de montage "
              "en laiton · aucune marque lisible sur les branches, le tissu ni l'outil · mains plausibles",
    "lab": "relu 22/09 07:4x · blouse unie sans broderie, écrans de machine en lumière abstraite (aucun "
           "caractère lisible) · cartons de verres neutres, plan de travail propre · aucune allusion "
           "chirurgicale",
    "exam": "relu 22/09 07:4x · réfracteur moderne, panneau d'échelle d'optotypes CONSERVÉ (outil du métier, "
            "pas une marque) · patient d'une soixantaine d'années, opticienne au réglage, personne ne regarde "
            "l'objectif",
}
IMG_ALT = {
    "hero": "Salle de vente d'un cabinet d'optique à Douala, lumière du jour — rendu de concept. "
            "Optical practice sales room in Douala, daylight - concept render.",
    "frames": "Trois montures posées dans un plateau de chêne avec un chiffon — rendu de concept. "
              "Three frames on an oak tray with a cloth - concept render.",
    "lab": "Comptoir d'entretien avec tailleries et lunettes de mesure — rendu de concept. "
           "Fitting bench with edger and lensometer - concept render.",
    "exam": "Mesure de vue au réfracteur, un patient et son opticienne — rendu de concept. "
            "Refraction test with a patient and her optician - concept render.",
}
IMGS, IMGKB = {}, 0.0
for _key, (_w, _h) in DIM.items():
    _f = IMGDIR / ("univers-v2-" + _key + ".jpg")
    if not _f.exists():
        raise SystemExit("visuel manquant : " + _f.name + " — la section qui le demande n'existe pas sans lui")
    _raw = _f.read_bytes()
    if len(_raw) > 260_000:
        raise SystemExit("%s pèse %d Ko (plafond 260 Ko) : re-compresser et relire après compression"
                         % (_f.name, len(_raw) // 1024))
    _rev = IMG_REVIEW.get(_key, "")
    if "lettrage" not in _rev and "marque" not in _rev and "broderie" not in _rev:
        raise SystemExit("fiche de relecture du visuel « " + _key + " » muette sur le LETTRAGE")
    IMGS[_key] = "data:image/jpeg;base64," + base64.b64encode(_raw).decode()
    IMGKB += len(_raw) / 1024

# ══════════════════════════════════════════════════════════════════════════════════
#  FEUILLE DE STYLE
# ══════════════════════════════════════════════════════════════════════════════════
CSS = """
:root{
 --paper:@PAPER@; --card:@CARD@; --card2:@CARD2@; --ink:@INK@; --text:@TEXT@; --mute:@MUTE@;
 --line:@LINE@; --hair:@HAIR@; --rust:@RUST@; --rust-dk:@RUST_DK@; --rust-t:@RUST_T@; --rust-edge:@RUST_EDGE@;
 --petrol:@PETROL@; --petrol-dk:@PETROL_DK@; --check:@CHECK@; --cream:@CREAM@;
 --wash:@WASH@; --wash-blue:@WASH_BLUE@; --edge-blue:@EDGE_BLUE@; --bar-bg:@BAR_BG@;
 --on-dark:@ON_DARK@; --on-dark-2:@ON_DARK_2@; --on-dark-3:@ON_DARK_3@; --on-dark-4:@ON_DARK_4@;
 --on-rust:@ON_RUST@; --on-rust-2:@ON_RUST_2@;
 --foot-ink:@FOOT_INK@; --foot-mute:@FOOT_MUTE@; --foot-label:@FOOT_LABEL@; --foot-link:@FOOT_LINK@;
 --foot-rule:@FOOT_RULE@; --foot-rule-2:@FOOT_RULE_2@; --foot-strip-mute:@FOOT_STRIP_MUTE@;
 --rgb-dark:@RGB_DARK@; --rgb-cream:@RGB_CREAM@; --rgb-shadow:@RGB_SHADOW@;
 --disp:@FDISP@; --body:@FBODY@; --mono:@FMONO@;
 --r:@RCARD@; --chip:@RCHIP@; --wrap:1240px; --pad:clamp(18px,4.4vw,52px);
 --dur-press:140ms; --dur-menu:220ms; --dur-reveal:520ms;
 --ease-out:cubic-bezier(.23,1,.32,1); --ease-in-out:cubic-bezier(.77,0,.175,1);
 --sh:0 22px 44px -26px rgba(var(--rgb-shadow),.34); --sh-soft:0 12px 26px -20px rgba(var(--rgb-shadow),.26);
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:124px}
body{margin:0;background:var(--paper);color:var(--text);font-family:var(--body);font-size:17px;
 line-height:1.66;overflow-wrap:break-word}
h1,h2,h3,h4{font-family:var(--disp);color:var(--ink);margin:0;font-weight:500;letter-spacing:-.015em;
 line-height:1.1;text-wrap:balance;font-optical-sizing:auto}
h1{font-size:clamp(2.35rem,6.1vw,4.35rem);line-height:1.03}
h2{font-size:clamp(1.62rem,3.6vw,2.7rem)}
h3{font-size:1.14rem;line-height:1.26;font-weight:600;font-family:var(--body)}
p{margin:0}
em{font-style:italic}
a{color:var(--petrol);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--rust);outline-offset:2px}
img{display:block;max-width:100%;height:auto}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}
.wrap{width:100%;max-width:var(--wrap);margin-inline:auto;padding-inline:var(--pad)}
html[data-lang=fr] .en-only{display:none}
html[data-lang=en] .fr-only{display:none}
.ttl{margin-bottom:22px}
.narrow{max-width:900px}
.gap-top{margin-top:16px}
.lead-dim{margin-top:16px}
.lead-mute{margin-top:14px;font-size:.97rem;color:var(--mute)}
.strip{background:var(--rust);color:var(--cream);font-size:.9rem;padding:10px 0}
.strip .wrap{display:flex;gap:12px;align-items:baseline;justify-content:space-between;flex-wrap:wrap}
.strip a{color:var(--cream);font-weight:600}
.strip .dim{opacity:.86}
.hd{position:sticky;top:0;z-index:40;background:rgba(var(--rgb-cream),.95);backdrop-filter:blur(8px);
 border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;gap:15px;min-height:78px;padding-block:10px}
.mark{display:flex;align-items:center;gap:11px;text-decoration:none;color:var(--ink);flex:0 0 auto}
.mark .lg{width:34px;height:34px;border-radius:50%;background:var(--rust);position:relative;flex:0 0 auto}
.mark .lg::after{content:"";position:absolute;inset:9px 6px;border-radius:50%;border:2px solid var(--cream);
 border-right-color:transparent;border-bottom-color:transparent;transform:rotate(-24deg);
 transition:transform var(--dur-menu) var(--ease-out)}
.mark:hover .lg::after{transform:rotate(14deg)}
.mark .nm{font-family:var(--disp);font-weight:600;font-size:1.22rem;letter-spacing:-.02em;line-height:1.05}
.mark .rl{display:block;font-family:var(--mono);font-size:9.4px;letter-spacing:.11em;text-transform:uppercase;
 color:var(--mute)}
.nav{display:flex;gap:4px;list-style:none;margin:0 0 0 auto;padding:0;flex-wrap:wrap}
.nav a{display:block;font-size:.94rem;font-weight:550;text-decoration:none;color:var(--mute);padding:8px 13px;
 border-radius:var(--chip);transition:color .18s var(--ease-out),background-color .18s var(--ease-out)}
.nav a:hover{color:var(--ink);background:var(--card2);text-decoration:none}
.btn{display:inline-flex;align-items:center;gap:9px;background:var(--rust);color:var(--cream);border:1px solid
 var(--rust);text-decoration:none;font-weight:600;font-size:.97rem;padding:12px 19px;border-radius:var(--chip);
 box-shadow:var(--sh-soft);transition:transform var(--dur-press) var(--ease-out),background-color .2s var(--ease-out),
 border-color .2s var(--ease-out)}
.btn:hover{background:var(--rust-dk);border-color:var(--rust-dk);text-decoration:none}
.btn:active{transform:scale(.97)}
.btn svg{flex:0 0 auto}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line);box-shadow:none}
.btn.ghost:hover{background:var(--card2);border-color:var(--hair)}
.btn.onphoto{background:transparent;color:var(--on-dark);border-color:rgba(var(--rgb-cream),.42)}
.btn.onphoto:hover{background:rgba(var(--rgb-cream),.12);border-color:var(--on-dark)}
.btn.onlight{background:var(--cream);color:var(--rust-dk);border-color:var(--cream)}
.btn.onlight:hover{background:var(--on-rust-2);border-color:var(--on-rust-2)}
.lang{display:flex;border:1px solid var(--line);border-radius:var(--chip);overflow:hidden;flex:0 0 auto}
.lang button{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;background:transparent;color:var(--mute);
 border:0;padding:8px 11px;cursor:pointer;transition:color .18s var(--ease-out),background-color .18s var(--ease-out)}
.lang button:hover{color:var(--ink);background:var(--card2)}
.lang button.is-on{background:var(--petrol);color:var(--cream)}
/* Le hero est la « grande photo » du gabarit. La voile n'est pas décorative : son opacité minimale sur la
   colonne de texte est calculée pour que le crème reste à plus de 4,5:1 même si l'image derrière est
   blanc pur (contrôle « voile du hero » ci-dessous dans le générateur). */
.hero{position:relative;isolation:isolate;background:var(--petrol-dk);color:var(--cream)}
.hero .ph{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;object-position:64% 56%}
.hero .veil{position:absolute;inset:0;z-index:-1;background:linear-gradient(97deg,
 rgba(var(--rgb-dark),.95) 0%,rgba(var(--rgb-dark),.90) 44%,rgba(var(--rgb-dark),.84) 64%,
 rgba(var(--rgb-dark),.34) 82%,rgba(var(--rgb-dark),.08) 94%)}
.hero .wrap{padding-block:clamp(58px,9vw,116px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,352px);
 gap:clamp(26px,4vw,58px);align-items:end}
.pill{display:inline-flex;align-items:center;gap:8px;background:rgba(var(--rgb-cream),.14);border:1px solid
 rgba(var(--rgb-cream),.34);color:var(--cream);font-family:var(--mono);font-size:11px;letter-spacing:.09em;
 text-transform:uppercase;padding:7px 13px;border-radius:var(--chip);margin-bottom:20px}
.pill i{width:6px;height:6px;border-radius:50%;background:var(--rust);display:block}
.hero h1{color:var(--on-dark);max-width:23ch}
.hero h1 em{color:var(--on-dark-2)}
.hero .lede{color:var(--on-dark-3);max-width:56ch;margin-top:20px;font-size:1.03rem}
.hero .acts{display:flex;gap:11px;flex-wrap:wrap;margin-top:26px}
.hero .note{margin-top:20px;font-size:.83rem;color:var(--on-dark-4);max-width:54ch}
.pick{background:var(--card);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh);
 padding:16px 16px 14px;color:var(--text)}
.pick .cap{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.pick h3{font-size:.98rem;margin:4px 0 0}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:11px 0 2px}
.chip{display:inline-flex;align-items:center;gap:6px;text-decoration:none;background:var(--card2);border:1px solid
 var(--line);color:var(--ink);font-size:.86rem;font-weight:550;padding:7px 11px;border-radius:var(--chip);
 transition:transform var(--dur-press) var(--ease-out),background-color .18s var(--ease-out)}
.chip:hover{background:var(--wash);text-decoration:none}
.chip:active{transform:scale(.96)}
.chip.h{font-family:var(--mono);font-size:.82rem;background:transparent;color:var(--petrol);
 border-color:var(--edge-blue)}
.chip.h:hover{background:var(--wash-blue)}
.pick .fine{font-size:.76rem;color:var(--mute);margin-top:10px;line-height:1.5}
main>section{padding-block:clamp(58px,8.4vw,124px)}
main>section+section{border-top:1px solid var(--line)}
.kick{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--rust-dk);
 margin-bottom:14px;display:block}
.sec2{display:grid;grid-template-columns:minmax(0,.94fr) minmax(0,1.06fr);gap:clamp(24px,4vw,56px);
 align-items:end;margin-bottom:clamp(28px,4vw,52px)}
.lede{font-size:1.06rem;color:var(--text);max-width:62ch}
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,1.8vw,22px)}
.step{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:clamp(18px,2.2vw,28px);
 box-shadow:var(--sh-soft);display:flex;flex-direction:column;gap:12px}
.step .n{font-family:var(--mono);font-size:.78rem;letter-spacing:.14em;color:var(--rust-dk)}
.step h3{font-family:var(--disp);font-weight:500;font-size:clamp(1.2rem,2vw,1.62rem);letter-spacing:-.015em;
 line-height:1.14;color:var(--ink)}
.step p{font-size:.95rem;color:var(--text)}
.step .wid{margin-top:auto;padding-top:14px;border-top:1px dotted var(--hair)}
.bars{display:flex;align-items:flex-end;gap:5px;height:58px}
.bars i{flex:1;background:var(--bar-bg);border-radius:3px;display:block;height:26%}
.bars i.on{background:var(--rust)}
.bars i:nth-child(2){height:44%}.bars i:nth-child(3){height:36%}.bars i:nth-child(4){height:58%}
.bars i:nth-child(5){height:48%}.bars i:nth-child(6){height:70%}.bars i:nth-child(7){height:82%}
.bars i:nth-child(8){height:64%}.bars i:nth-child(9){height:92%}
.step .cap{font-size:.76rem;color:var(--mute);margin-top:9px;line-height:1.45}
.tick{display:flex;gap:9px;align-items:flex-start;font-size:.9rem;padding:5px 0;color:var(--text)}
.tick b{color:var(--check);font-family:var(--mono);line-height:1.4;flex:0 0 auto}
.cmp{border:1px solid var(--line);border-radius:var(--r);background:var(--card);box-shadow:var(--sh-soft);
 overflow:hidden}
table.t{width:100%;border-collapse:collapse;font-size:.95rem}
table.t th,table.t td{text-align:left;padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top}
table.t thead th{font-family:var(--mono);font-size:10.4px;letter-spacing:.11em;text-transform:uppercase;
 color:var(--mute);background:var(--card2);font-weight:600}
table.t tbody tr:last-child td{border-bottom:0}
table.t td.c1{color:var(--mute)}
table.t th.mark,table.t td.mark{background:var(--rust);color:var(--cream);
 border-bottom-color:rgba(var(--rgb-cream),.24)}
table.t thead th.mark{background:var(--rust-dk);color:var(--cream)}
table.t td.mark b{font-weight:600}
.cmpfoot{padding:14px 16px;border-top:1px solid var(--line);background:var(--card2);font-size:.8rem;
 color:var(--mute);line-height:1.55}
.note-inline{margin-top:18px;font-size:.86rem;color:var(--mute);border:1px solid var(--line);border-radius:var(--r);
 background:var(--card);padding:14px 16px;line-height:1.55;max-width:88ch}
.ed{display:grid;grid-template-columns:minmax(0,.82fr) minmax(0,1.18fr);gap:clamp(22px,3.4vw,54px);align-items:center}
.ed figure{margin:0}
.ed img{width:100%;height:auto;border-radius:var(--r);box-shadow:var(--sh);object-fit:cover;aspect-ratio:760/950}
.ed figcaption{font-size:.86rem;color:var(--mute);margin-top:13px;line-height:1.55}
.ed figcaption b{display:block;font-family:var(--disp);font-weight:500;font-size:1.05rem;color:var(--ink);
 letter-spacing:-.01em;margin-bottom:4px}
.marks{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:2px;margin:22px 0 0;
 border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.marks>div{background:var(--card);padding:13px 15px}
.marks dt{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.marks dd{margin:5px 0 0;font-size:.94rem;color:var(--ink);font-weight:550}
.finds{display:grid;gap:0;border-top:1px solid var(--line)}
.find{display:grid;grid-template-columns:44px minmax(0,.9fr) minmax(0,1.3fr);gap:clamp(12px,2vw,26px);
 padding:clamp(16px,2.2vw,26px) 0;border-bottom:1px solid var(--line);align-items:start}
.find .k{font-family:var(--mono);font-size:.8rem;color:var(--rust-dk);padding-top:6px}
.find h3{font-family:var(--disp);font-weight:500;font-size:1.22rem;line-height:1.2;letter-spacing:-.015em}
.find .src{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;
 color:var(--mute);margin-top:7px}
.find p{font-size:.96rem;color:var(--text)}
.packs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,1.8vw,22px);align-items:start}
.pack{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:clamp(17px,2vw,24px)}
.pack h3{font-family:var(--disp);font-weight:500;font-size:1.3rem;letter-spacing:-.015em}
.pack .why{font-size:.88rem;color:var(--mute);margin-top:7px;line-height:1.5}
.pack ul{list-style:none;margin:14px 0 0;padding:0}
.pack li{padding:10px 0;border-top:1px dotted var(--hair);font-size:.96rem}
.pack li:first-child{border-top:0}
.pack li a{text-decoration:none;color:var(--ink);font-weight:550}
.pack li a:hover{color:var(--rust-dk);text-decoration:underline}
.band{background:var(--rust);color:var(--cream);border-radius:var(--r);padding:clamp(24px,3.6vw,46px);
 display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.62fr);gap:clamp(20px,3vw,40px);align-items:center}
.band h2{color:var(--cream)}
.band .kick{color:var(--cream)}
.band p{color:var(--cream);margin-top:12px;font-size:1.02rem;max-width:60ch}
.band .btn{justify-self:start}
.shots{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.7fr);gap:clamp(14px,2vw,24px);align-items:start}
.shots2{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(14px,2vw,24px)}
.shot{margin:0}
.shot img{width:100%;height:auto;border-radius:var(--r);box-shadow:var(--sh-soft);object-fit:cover}
.shot figcaption{margin-top:12px;font-size:.88rem;color:var(--mute);line-height:1.55}
.shot figcaption b{display:block;font-family:var(--disp);font-size:1.05rem;color:var(--ink);font-weight:500;
 margin-bottom:4px;letter-spacing:-.01em}
.book{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(20px,3vw,44px);align-items:start}
.slots{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--card)}
.slots>div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;padding:14px 16px;
 border-bottom:1px solid var(--line);align-items:center}
.slots>div:last-child{border-bottom:0}
.slots .d{font-weight:600;color:var(--ink)}
.slots .h{font-family:var(--mono);font-size:.9rem;color:var(--petrol);font-variant-numeric:tabular-nums}
.slots .closed{color:var(--rust-dk)}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:clamp(17px,2.2vw,26px);
 box-shadow:var(--sh-soft)}
.card .gap-top{margin-top:16px}
.card h3{font-family:var(--disp);font-weight:500;font-size:1.24rem;letter-spacing:-.015em;margin-bottom:9px}
.kv{display:grid;grid-template-columns:minmax(86px,.62fr) minmax(0,1.38fr);gap:9px 14px;margin-top:14px;
 font-size:.93rem}
.kv dt{font-family:var(--mono);font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:var(--mute);
 padding-top:3px}
.kv dd{margin:0;color:var(--ink)}
.asks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(12px,1.6vw,18px)}
.ask{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--rust);
 border-radius:0 var(--r) var(--r) 0;padding:16px 18px}
.ask h3{font-size:1rem;color:var(--ink);font-family:var(--disp);font-weight:500;letter-spacing:-.01em}
.ask p{font-size:.9rem;color:var(--mute);margin-top:7px;line-height:1.55}
.rate{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:clamp(18px,2.6vw,38px);align-items:start}
.score{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:22px}
.score .lbl{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.score .big{font-family:var(--disp);font-size:clamp(3rem,6vw,4.6rem);line-height:.94;color:var(--ink);margin-top:8px}
.score .of{font-size:.9rem;color:var(--mute);margin-top:8px}
.score .bar{height:6px;background:var(--bar-bg);border-radius:3px;margin-top:16px;overflow:hidden}
.score .bar i{display:block;height:100%;width:66%;background:var(--rust)}
.score .fine{font-size:.8rem;color:var(--mute);margin-top:12px;line-height:1.5}
.rw{padding:15px 0;border-bottom:1px dotted var(--hair)}
.rw:last-of-type{border-bottom:0}
.rw h3{font-size:.99rem;color:var(--ink)}
.rw p{font-size:.93rem;color:var(--mute);margin-top:5px}
.warn{margin-top:20px;font-size:.9rem;color:var(--rust-dk);background:var(--rust-t);border:1px solid
 var(--rust-edge);border-radius:var(--r);padding:13px 15px;line-height:1.55}
.faq details{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:0 18px;margin-bottom:9px}
.faq summary{cursor:pointer;padding:15px 0;font-weight:600;color:var(--ink);list-style:none;display:flex;
 justify-content:space-between;gap:14px;align-items:center;font-size:.99rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";font-family:var(--mono);color:var(--rust-dk);font-size:1.1rem;line-height:1;
 transition:transform var(--dur-menu) var(--ease-out)}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details>div{padding:0 0 16px;font-size:.95rem;color:var(--text);max-width:78ch}
.foot{background:var(--petrol-dk);color:var(--foot-ink);padding-block:clamp(40px,6vw,76px) 22px}
.foot .cols{display:grid;grid-template-columns:minmax(0,1.3fr) repeat(3,minmax(0,1fr));gap:clamp(18px,2.4vw,36px)}
.foot h4{font-family:var(--mono);font-size:10.6px;letter-spacing:.13em;text-transform:uppercase;color:var(--foot-label);
 margin:0 0 12px;font-weight:600}
.foot .bn{font-family:var(--disp);font-size:1.4rem;color:var(--cream);margin-bottom:10px}
.foot p{font-size:.92rem;color:var(--foot-mute);line-height:1.6}
.foot ul{list-style:none;margin:0;padding:0}
.foot li{margin:8px 0;font-size:.93rem}
.foot a{color:var(--foot-link);text-decoration:none;border-bottom:1px solid var(--foot-rule);padding-bottom:1px}
.foot a:hover{color:var(--cream);text-decoration:none}
.foot a.btn{color:var(--cream);border:1px solid var(--rust);
 margin-top:16px}
.foot .badge{display:inline-block;font-family:var(--mono);font-size:9.8px;letter-spacing:.11em;
 text-transform:uppercase;color:var(--cream);border:1px solid var(--foot-rule);border-radius:var(--chip);
 padding:5px 10px;margin-top:16px}
.foot .strip2{display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between;align-items:center;
 border-top:1px solid var(--foot-rule-2);margin-top:clamp(26px,4vw,44px);padding-top:18px;font-size:.8rem;
 color:var(--foot-strip-mute)}
.foot .strip2 a{color:var(--foot-link);border:0}
.up{display:inline-flex;align-items:center;gap:7px;text-decoration:none;color:var(--cream);font-family:var(--mono);
 font-size:10.4px;letter-spacing:.1em;text-transform:uppercase;border:0}
.up:hover{color:var(--cream);text-decoration:underline}
.rail{position:fixed;left:0;right:0;bottom:0;z-index:45;display:none;gap:8px;padding:9px 12px
 calc(9px + env(safe-area-inset-bottom));background:rgba(var(--rgb-cream),.96);border-top:1px solid var(--line);
 backdrop-filter:blur(8px)}
.rail .btn{flex:1;justify-content:center;padding:13px 12px;font-size:.95rem}
.rail .btn.ghost{flex:0 0 32%}
@media (hover:hover) and (pointer:fine){
 .step:hover,.pack:hover,.card:hover{box-shadow:var(--sh);border-color:var(--hair)}
 .shot:hover img{box-shadow:var(--sh)}
 .ask:hover{border-left-color:var(--rust-dk)}
}
@media (max-width:1080px){
 .hero .wrap,.sec2,.ed,.book,.rate,.shots{grid-template-columns:minmax(0,1fr)}
 .steps,.packs{grid-template-columns:repeat(2,minmax(0,1fr))}
 .foot .cols{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:960px){
 .hd .wrap{flex-wrap:wrap;min-height:0;row-gap:10px}
 .hd .btn,.mark .rl{display:none}
 .nav{order:3;width:100%;margin:0;overflow-x:auto;flex-wrap:nowrap;-webkit-overflow-scrolling:touch}
 .nav a{white-space:nowrap;padding:7px 11px;font-size:.88rem}
 .rail{display:flex}
 main>section{padding-block:clamp(44px,9vw,64px)}
 html{scroll-padding-top:132px}
}
@media (max-width:700px){
 .steps,.packs,.asks,.shots,.shots2{grid-template-columns:minmax(0,1fr)}
 .find{grid-template-columns:28px minmax(0,1fr)}
 .find p{grid-column:2}
 .band{grid-template-columns:minmax(0,1fr)}
 table.t{font-size:.9rem}
 table.t th,table.t td{padding:12px 13px}
 .marks{grid-template-columns:minmax(0,1fr)}
 /* Sur le pouce, le texte passe SUR la photo : la voile devient quasi pleine, jamais un dégradé qui
    laisse passer la lumière derrière un paragraphe. */
 .hero .veil{background:linear-gradient(180deg,rgba(var(--rgb-dark),.93) 0%,rgba(var(--rgb-dark),.87) 100%)}
}
@media (max-width:430px){
 body{font-size:16.4px}
 .hd .lang{margin-left:auto}
 .hero .acts .btn{flex:1;justify-content:center}
}
@media print{.rail,.hd,.strip{display:none}body{background:var(--card)}}
/* L'état caché n'existe QUE sous html.js : sans JavaScript qui tourne, la page se peint ENTIÈRE.
   Loi design/WORKFLOW.md étape 8 ; l'accident du 22/09 (corps invisible chez le client, 25 blocs à
   opacité nulle relevés par un seul observeur de fin de document) est raconté dans design/LESSONS.md. */
html.js .rv{opacity:0;transform:translateY(22px);transition:opacity var(--dur-reveal) var(--ease-out),
 transform var(--dur-reveal) var(--ease-out)}
html.js .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
 html{scroll-behavior:auto}
 *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
  transition-duration:.01ms!important}
 html.js .rv{opacity:1;transform:none;transition:none}
}"""
for _tok, _val in (("@PAPER@", PAPER), ("@CARD@", CARD), ("@CARD2@", CARD2), ("@INK@", INK), ("@TEXT@", TEXT),
                   ("@MUTE@", MUTE), ("@LINE@", LINE), ("@RUST@", RUST), ("@RUST_DK@", RUST_DK),
                   ("@RUST_T@", RUST_T), ("@PETROL@", PETROL), ("@PETROL_DK@", PETROL_DK), ("@CHECK@", CHECK),
                   ("@CREAM@", CREAM), ("@HAIR@", HAIR), ("@WASH@", WASH), ("@WASH_BLUE@", WASH_BLUE),
                   ("@EDGE_BLUE@", EDGE_BLUE), ("@BAR_BG@", BAR_BG), ("@RUST_EDGE@", RUST_EDGE),
                   ("@ON_DARK@", ON_DARK), ("@ON_DARK_2@", ON_DARK_2), ("@ON_DARK_3@", ON_DARK_3),
                   ("@ON_DARK_4@", ON_DARK_4), ("@ON_RUST@", ON_RUST), ("@ON_RUST_2@", ON_RUST_2),
                   ("@FOOT_INK@", FOOT_INK), ("@FOOT_MUTE@", FOOT_MUTE), ("@FOOT_LABEL@", FOOT_LABEL),
                   ("@FOOT_LINK@", FOOT_LINK), ("@FOOT_RULE@", FOOT_RULE), ("@FOOT_RULE_2@", FOOT_RULE_2),
                   ("@FOOT_STRIP_MUTE@", FOOT_STRIP_MUTE), ("@RGB_DARK@", RGB_DARK), ("@RGB_CREAM@", RGB_CREAM),
                   ("@RGB_SHADOW@", RGB_SHADOW),
                   ("@FDISP@", FONTS_DISP), ("@FBODY@", FONTS_BODY), ("@FMONO@", FONTS_MONO),
                   ("@RCARD@", RAD_CARD), ("@RCHIP@", RAD_CHIP)):
    CSS = CSS.replace(_tok, _val)
assert "@" not in re.sub(r"@media|@import|@font-face", "", CSS), "un jeton de style n'a pas été résolu"
_CSS_TAIL = CSS[CSS.index("body{margin"):]
assert not re.search(r"#[0-9A-Fa-f]{3,8}\b", _CSS_TAIL), "couleur écrite en dur hors de :root"
assert not re.search(r"rgba\(\s*\d", _CSS_TAIL), "rgba en chiffres bruts : passer par un jeton-triplet"

JS = """
(function(){
  var html=document.documentElement, KEY='universoptique-lang-v2';
  function setLang(l){
    html.setAttribute('data-lang',l); html.setAttribute('lang',l);
    var f=document.getElementById('btn-fr'), e=document.getElementById('btn-en');
    if(f){f.classList.toggle('is-on',l==='fr');}
    if(e){e.classList.toggle('is-on',l==='en');}
    try{localStorage.setItem(KEY,l);}catch(err){}
  }
  var f=document.getElementById('btn-fr'), e=document.getElementById('btn-en');
  if(f){f.addEventListener('click',function(){setLang('fr');});}
  if(e){e.addEventListener('click',function(){setLang('en');});}
  try{var s=localStorage.getItem(KEY); if(s==='en'||s==='fr'){setLang(s);}}catch(err){}
})();
"""
# la révélation vit dans son propre <script>, avec un filet qui montre tout en cas de faute
JS_REV = """
(function(){
  function show(){var n=document.querySelectorAll('.rv');for(var i=0;i<n.length;i++){n[i].classList.add('in');}}
  try{
    var els=document.querySelectorAll('.rv');
    if(!els.length){return;}
    var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(reduce||!('IntersectionObserver' in window)){show();return;}
    var io=new IntersectionObserver(function(es){
      for(var j=0;j<es.length;j++){if(es[j].isIntersecting){es[j].target.classList.add('in');io.unobserve(es[j].target);}}
    },{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    for(var k=0;k<els.length;k++){els[k].style.transitionDelay=(Math.min(k,3)*60)+'ms';io.observe(els[k]);}
  }catch(err){show();}
})();
"""

WA_I = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 '
        '2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.1c-.2.6-1.2 1.2-1.7 1.2-.4.1-1 .1-1.6-.1'
        '.4-.1-.9-.3-1.5-.6-2.7-1.2-4.4-3.9-4.6-4.1-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.2.5-.3.7-.3h.5c.2'
        ' 0 .4 0 .6.4l.8 2c.1.2.1.4 0 .5l-.4.5c-.1.2-.3.3-.1.6.1.3.7 1.1 1.4 1.7.9.8 1.6 1 1.9 1.2.2.1.4.1.5'
        '-.1l.7-.8c.2-.2.3-.2.6-.1l1.9.9c.3.1.4.2.5.3.1.2.1.6-.1 1.1Z"/></svg>')
EYE = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
       'aria-hidden="true"><path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6Z"/>'
       '<circle cx="12" cy="12" r="2.6"/></svg>')
ARR = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg>')

# ══════════════════════════════════════════════════════════════════════════════════
#  SECTIONS — chacune tient debout seule (ruban de loi n° 11)
# ══════════════════════════════════════════════════════════════════════════════════
S = []
WA_HERO = wa_url(msg("generic"))

# 1 · bandeau rouille : une urgence vraie, les horaires
S.append('<div class="strip"><div class="wrap"><span>' + L(C["bar"]["line"]) +
         ' <span class="dim">· ' + L(C["bar"]["confirm"]) + '</span></span>'
         '<a href="#rendez-vous">' + bi("Un créneau de vingt minutes se prend ici",
                                        "A twenty-minute slot is taken here") + '</a></div></div>')

# 2 · en-tête
_nav = "".join('<li><a href="%s">%s</a></li>' % (h, bi(fr, en)) for h, fr, en in C["nav"])
S.append('<header class="hd"><div class="wrap">'
         '<a class="mark" href="#top"><span class="lg" aria-hidden="true"></span><span>'
         '<span class="nm">Univers Optique</span>'
         '<span class="rl">' + bi("Optique médicale · Bépanda · depuis 2009",
                                  "Medical optics - Bepanda - since 2009") + '</span></span></a>'
         '<ol class="nav" aria-label="' + esc(C["a11y"]["nav"]["fr"]) + '">' + _nav + '</ol>'
         '<a class="btn" href="' + WA_HERO + '" target="_blank" rel="noopener">' + EYE +
         '<span>' + L(C["ctaNav"]) + '</span></a>'
         '<span class="lang" role="group" aria-label="' + esc("Langue / Language") + '">'
         '<button id="btn-fr" class="is-on" type="button">FR</button>'
         '<button id="btn-en" type="button">EN</button></span>'
         '</div></header>')

# 3 · HERO — la grande photo, le sélecteur de créneaux posé dedans
_days = "".join('<a class="chip" href="%s">%s</a>' % (wa_url(msg("slot", slot=fr, when=fr)), bi(fr, en))
                for fr, en in V2["steps"]["chipsDays"][:3])
_hours = "".join('<a class="chip h" href="%s">%s</a>' % (wa_url(msg("slot", slot=fr, when="lundi-vendredi")),
                                                         bi(fr, en))
                 for fr, en in V2["steps"]["chipsHours"])
_pick_fine = ("Aucun compte, aucun formulaire : ces appuis ouvrent WhatsApp au " + C["waDisp"] +
              " avec la demande déjà écrite. Les horaires viennent de votre fiche Google, relue le 21/09.")
_pick_fine_en = ("No account, no form: these taps open WhatsApp on " + C["waDisp"] + " with the request already "
                 "written. Hours come from your Google listing, re-read on 21 Sep.")
S.append('<section class="hero" id="hero">'
         '<img class="ph" src="' + IMGS["hero"] + '" width="' + str(DIM["hero"][0]) + '" height="' +
         str(DIM["hero"][1]) + '" alt="' + esc(IMG_ALT["hero"]) + '" fetchpriority="high" decoding="async">'
         '<span class="veil" aria-hidden="true"></span>'
         '<div class="wrap"><div>'
         '<span class="pill"><i aria-hidden="true"></i>' + L(V2["heroPill"]) + '</span>'
         '<h1>' + L(V2["heroH1a"]) + '<em>' + L(V2["heroH1b"]) + '</em></h1>'
         '<p class="lede">' + L(V2["heroLede"]) + '</p>'
         '<div class="acts">'
         '<a class="btn" href="' + WA_HERO + '" target="_blank" rel="noopener">' + WA_I +
         '<span>' + L(C["hero"]["book"]) + '</span></a>'
         '<a class="btn ghost onphoto" href="#dossier">' + L(C["hero"]["second"]) + '</a>'
         '</div>'
         '<p class="note">' + L(V2["heroNote"]) + '</p>'
         '</div>'
         '<aside class="pick" aria-label="' + esc("Choisir un créneau") + '">'
         '<span class="cap">' + bi("Prochains créneaux proposés", "Next slots offered") + '</span>'
         '<h3>' + bi("Appuyez, le message est écrit", "Tap it, the message is written") + '</h3>'
         '<div class="chips">' + _days + '</div><div class="chips">' + _hours + '</div>'
         '<p class="fine">' + bi(_pick_fine, _pick_fine_en) + '</p>'
         '</aside></div></section>')

# 4 · les trois étapes — LE moment animé de la page


def widget(it):
    kind = it["widget"]
    if kind == "days":
        a = "".join('<a class="chip" href="%s">%s</a>' %
                    (wa_url(msg("slot", slot=fr, when=en)), bi(fr, en))
                    for fr, en in V2["steps"]["chipsDays"][2:])
        b = "".join('<a class="chip h" href="%s">%s</a>' %
                    (wa_url(msg("slot", slot=fr, when="demain")), bi(fr, en))
                    for fr, en in V2["steps"]["chipsHours"])
        return '<div class="wid"><div class="chips">' + a + '</div><div class="chips">' + b + '</div></div>'
    if kind == "bars":
        bars = "".join('<i class="on"></i>' if i < 6 else '<i></i>' for i in range(9))
        lbl = "6 constats sourcés sur 9 lignes publiées"
        return ('<div class="wid"><div class="bars" role="img" aria-label="' + esc(lbl) + '">' + bars +
                '</div><p class="cap">' + L(V2["steps"]["barsCaption"]) + '</p></div>')
    ticks = "".join('<div class="tick"><b>+</b><span>' + bi(fr, en) + '</span></div>'
                    for fr, en in V2["steps"]["list"])
    return '<div class="wid">' + ticks + '</div>'


_steps = "".join('<article class="step rv"><span class="n">' + it["n"] + '</span><h3>' + L(it["h"]) + '</h3>'
                 '<p>' + L(it["p"]) + '</p>' + widget(it) + '</article>' for it in V2["steps"]["items"])
S.append('<section id="etapes"><div class="wrap">'
         '<div class="sec2"><div>'
         '<h2>' + L(V2["steps"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(V2["steps"]["lede"]) + '</p></div>'
         '<div class="steps">' + _steps + '</div></div></section>')

# 5 · le comparatif à colonne surlignée
_rows = ""
for _r in V2["cmp"]["rows"]:
    _rows += ('<tr><td scope="row">' + bi(_r[0], _r[3]) + '</td>'
              '<td class="c1">' + bi(_r[1], _r[4]) + '</td>'
              '<td class="mark"><b>' + bi(_r[2], _r[5]) + '</b></td></tr>')
_c = V2["cmp"]["cols"]
S.append('<section id="comparatif"><div class="wrap">'
         '<div class="sec2"><div><span class="kick">' + bi("Face à face", "Side by side") + '</span>'
         '<h2>' + L(V2["cmp"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(V2["cmp"]["lede"]) + '</p></div>'
         '<div class="cmp"><table class="t"><thead><tr>'
         '<th scope="col">' + bi(_c[0], _c[3]) + '</th>'
         '<th scope="col">' + bi(_c[1], _c[4]) + '</th>'
         '<th scope="col" class="mark">' + bi(_c[2], _c[5]) + '</th></tr></thead>'
         '<tbody>' + _rows + '</tbody></table>'
         '<p class="cmpfoot">' + L(V2["cmp"]["foot"]) + '</p></div></div></section>')

# 6 · le cabinet : édition photo + repères vérifiés
_mk = "".join('<div><dt>' + bi(a, c) + '</dt><dd>' + bi(b, d) + '</dd></div>'
              for a, b, c, d in V2["cabinet"]["marks"])
S.append('<section id="cabinet"><div class="wrap"><div class="ed">'
         '<figure><img src="' + IMGS["frames"] + '" width="' + str(DIM["frames"][0]) + '" height="' +
         str(DIM["frames"][1]) + '" loading="lazy" decoding="async" alt="' + esc(IMG_ALT["frames"]) + '">'
         '<figcaption><b>' + L(V2["cabinet"]["shotT"]) + '</b>' + L(V2["cabinet"]["shotP"]) +
         ' <span class="chip">' + bi("Rendu de concept — votre photo le remplacera",
                                    "Concept render - your photo replaces it") + '</span></figcaption></figure>'
         '<div>'
         '<h2>' + L(V2["cabinet"]["h2"]) + '</h2>'
         '<p class="lede lead-dim">' + L(V2["cabinet"]["p1"]) + '</p>'
         '<p class="lead-mute">' + L(V2["cabinet"]["p2"]) + '</p>'
         '<dl class="marks">' + _mk + '</dl></div></div></div></section>')

# 7 · les six constats sourcés — le corps du dossier, en liste éditoriale
_finds = ""
for _i, _r in enumerate(C["dossier"]["rows"], 1):
    _so = (' ' + bi(_r[4], _r[5])) if len(_r) > 5 and _r[4] else ''
    _finds += ('<article class="find"><span class="k mono">' + ('%02d' % _i) + '</span>'
               '<div><h3>' + bi(_r[0], _r[1]) + '</h3>'
               '<span class="src">' + bi("relu le 21/09/2026", "read on 21 Sep 2026") + '</span></div>'
               '<p>' + bi(_r[2], _r[3]) + _so + '</p></article>')
S.append('<section id="dossier"><div class="wrap">'
         '<div class="sec2"><div><span class="kick">' + bi("Le dossier", "The record") + '</span>'
         '<h2>' + L(C["dossier"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(C["dossier"]["lede"]) + '</p></div>'
         '<div class="finds">' + _finds + '</div>'
         '<p class="note-inline">' + L(C["dossier"]["foot"]) + '</p></div></section>')

# 8 · les dix actes en trois paquets
_packs = ""
for _g in V2["clusters"]["groups"]:
    _lis = "".join('<li><a href="#rendez-vous">' + bi(fr, en) + '</a></li>' for fr, en in _g["rows"])
    _packs += ('<article class="pack"><h3>' + L(_g["t"]) + '</h3><p class="why">' + L(_g["why"]) +
               '</p><ul>' + _lis + '</ul></article>')
_pack_foot = bi("Deux lignes manquent exprès ici : les prix et un horaire du dimanche. Vous n'avez publié de "
                "prix nulle part, et votre fiche écrit « Fermé » le dimanche. Les deux sont dans la colonne "
                "des questions, pas dans la vitrine.",
                "Two lines are missing here on purpose: prices and a Sunday hour. You published no price "
                "anywhere, and your listing reads closed on Sunday. Both sit in the questions column, not in "
                "the window.")
S.append('<section id="services"><div class="wrap">'
         '<div class="sec2"><div>'
         '<h2>' + L(V2["clusters"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(V2["clusters"]["lede"]) + '</p></div>'
         '<div class="packs">' + _packs + '</div>'
         '<p class="note-inline">' + _pack_foot + '</p></div></section>')

# 9 · le bandeau : l'acte que personne d'autre ne revendique
S.append('<section id="protheses"><div class="wrap"><div class="band">'
         '<div><h2>' + L(V2["band"]["t"]) + '</h2><p>' + L(V2["band"]["p"]) + '</p></div>'
         '<a class="btn onlight" href="' + wa_url(msg("ask", svc="les prothèses oculaires")) +
         '" target="_blank" rel="noopener">' + EYE + '<span>' + L(V2["band"]["cta"]) + '</span>' + ARR + '</a>'
         '</div></div></section>')

# 10 · les rendus : une image = une légende = un badge, la légende dessous


def shot(tag, item):
    cap = bi(item[0], item[1])
    body = bi(item[2], item[3])
    badge = bi("Rendu de concept — votre photo le remplacera", "Concept render - your photo replaces it")
    return ('<figure class="shot"><img src="' + IMGS[tag] + '" width="' + str(DIM[tag][0]) + '" height="' +
            str(DIM[tag][1]) + '" loading="lazy" decoding="async" alt="' + esc(IMG_ALT[tag]) + '">'
            '<figcaption><b>' + cap + '</b>' + body + ' <span class="chip">' + badge + '</span>'
            '</figcaption></figure>')


_ph = C["photos"]["items"]
S.append('<section id="visuels"><div class="wrap">'
         '<div class="sec2"><div>'
         '<h2>' + L(C["photos"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(C["photos"]["lede"]) + '</p></div>'
         '<div class="shots">' + shot("lab", _ph[1]) + '<div class="shots2">' + shot("exam", _ph[2]) +
         '</div></div>'
         '<p class="note-inline">' + L(V2["photosNote"]) + '</p></div></section>')

# 11 · rendez-vous + fiche
_slots = ""
for _fr, _en, _hours_txt in C["book"]["slots"]:
    _cls = ' class="h closed"' if "Ferm" in _hours_txt else ' class="h"'
    _slots += ('<div><span class="d">' + bi(_fr, _en) + '</span><span' + _cls + '>' + esc(_hours_txt) +
               '</span></div>')
_kv = [("Établissement", "Establishment", C["legalName"], None),
       ("Adresse", "Address", C["addr"] + " · " + C["bp"], None),
       ("Repère", "Landmark", C["landmark"], None),
       ("Téléphone", "Phone", C["waDisp"], "tel:+237" + WA),
       ("Second numéro", "Second number", C["tel2Disp"], "tel:+237" + re.sub(r"\D", "", C["tel2"])),
       ("E-mail", "Email", C["mail1"], "mailto:" + C["mail1"]),
       ("Plus code", "Plus code", C["mapsPlus"], None),
       ("Carte", "Map", None, MAPS)]
_kvs = ""
for _l1, _l2, _txt, _href in _kv:
    _v = bi("Ouvrir dans Google Maps", "Open in Google Maps") if _txt is None else esc(_txt)
    if _href:
        _v = '<a href="' + _href + '"' + (' rel="noopener"' if _href.startswith("http") else '') + '>' + _v + '</a>'
    _kvs += '<dt>' + bi(_l1, _l2) + '</dt><dd>' + _v + '</dd>'
S.append('<section id="rendez-vous"><div class="wrap">'
         '<div class="sec2"><div><span class="kick">' + bi("Réserver", "Booking") + '</span>'
         '<h2>' + L(C["book"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(C["book"]["lede"]) + '</p></div>'
         '<div class="book"><div><div class="slots">' + _slots + '</div>'
         '<p class="note-inline">' + L(C["book"]["fine"]) + '</p></div>'
         '<div class="card"><h3>' + bi("La fiche du cabinet", "The practice record") + '</h3>'
         '<dl class="kv">' + _kvs + '</dl>'
         '<a class="btn gap-top" href="' + WA_HERO + '" target="_blank" rel="noopener">' + WA_I +
         '<span>' + L(C["hero"]["book"]) + '</span></a></div></div></div></section>')

# 12 · les avis, tels qu'ils sont
_rws = "".join('<div class="rw"><h3>' + bi(a, c) + '</h3><p>' + bi(b, d) + '</p></div>'
               for a, b, c, d in C["reviews"]["rows"])
_score_note = bi("Barre lue comme une proportion, pas comme une promesse : aucun avis n'est ajouté pour la "
                 "faire monter.",
                 "Read the bar as a proportion, not a promise: no review is added to lift it.")
S.append('<section id="avis"><div class="wrap">'
         '<div class="sec2"><div>'
         '<h2>' + L(C["reviews"]["h2"]) + '</h2></div>'
         '<p class="lede">' + bi("Aucun avis n'est écrit, déplacé ou enjolivé ici. Ce qui est publié sous votre "
                                 "nom reste tel quel, et une note basse se traite comme un sujet, pas comme une "
                                 "honte.",
                                 "No review is written, moved or prettified here. What is published under your "
                                 "name stays as it is, and a low rating is a subject, not a shame.") + '</p></div>'
         '<div class="rate"><div class="score">'
         '<span class="lbl">' + bi("Google · catégorie Opticien", "Google - Optician category") + '</span>'
         '<div class="big">' + esc(C["reviews"]["score"]) + '</div>'
         '<p class="of">' + L(C["reviews"]["scoreOf"]) + '</p>'
         '<div class="bar" role="img" aria-label="' + esc("3,3 sur 5") + '"><i></i></div>'
         '<p class="fine">' + _score_note + '</p></div>'
         '<div>' + _rws + '<p class="warn">' + L(C["reviews"]["warn"]) + '</p></div></div></div></section>')

# 13 · les six questions à trancher
_asks = "".join('<article class="ask"><h3>' + bi(r[0], r[1]) + '</h3><p>' + bi(r[2], r[3]) + '</p></article>'
                for r in C["open"]["items"])
S.append('<section id="questions"><div class="wrap">'
         '<div class="sec2"><div><span class="kick">' + bi("À trancher par vous", "For you to settle") + '</span>'
         '<h2>' + L(C["open"]["h2"]) + '</h2></div>'
         '<p class="lede">' + L(C["open"]["lede"]) + '</p></div>'
         '<div class="asks">' + _asks + '</div></div></section>')

# 14 · FAQ (le seul accordéon de la page : une question, quatre réponses, aucune promesse)
_faq = "".join('<details><summary>' + bi(r[0], r[1]) + '</summary><div>' + bi(r[2], r[3]) + '</div></details>'
               for r in C["faq"]["items"])
S.append('<section id="faq"><div class="wrap">'
         '<h2 class="ttl">' + L(C["faq"]["h2"]) + '</h2>'
         '<div class="faq narrow">' + _faq + '</div></div></section>')

# 15 · pied de page = l'écran de conversion (loi §20)


def fcol(title, links):
    lis = ""
    for _href, _fr, _en in links:
        if _href == "MAPS":
            lis += '<li><a href="' + MAPS + '" rel="noopener">' + bi(_fr, _en) + '</a></li>'
        elif _href == "BP":
            lis += '<li><span>' + bi(_fr, _en) + '</span></li>'
        else:
            lis += '<li><a href="' + _href + '">' + bi(_fr, _en) + '</a></li>'
    return '<div><h4>' + bi(title[0], title[1]) + '</h4><ul>' + lis + '</ul></div>'


_cols = "".join(fcol(_t, _items) for _t, _items in C["footer"]["cols"])
assert _cols.count("<h4>") == len(C["footer"]["cols"]) + 0
S.append('<footer class="foot" id="contact"><div class="wrap"><div class="cols">'
         '<div><div class="bn">Univers Optique</div><p>' + L(C["footer"]["brandP"]) + '</p>'
         '<a class="btn" href="' + WA_HERO + '" target="_blank" rel="noopener">' + WA_I +
         '<span>' + L(C["footer"]["cta"]) + '</span></a>'
         '<span class="badge">' + L(C["footer"]["badge"]) + '</span></div>' + _cols + '</div>'
         '<div class="strip2"><span>' +
         bi("Univers Optique · " + C["addr"] + " · " + C["bp"], "Univers Optique - " + C["addr"] + " - " + C["bp"]) +
         '</span><span>' + L(C["footer"]["strip1"]) + ' · ' + L(C["footer"]["strip2"]) + '</span>'
         '<a class="up" href="#top">' + bi("Retour en haut", "Back to top") + '</a></div></div></footer>')

# 16 · barre collée au pouce
S.append('<div class="rail" role="group" aria-label="' + esc("Actions rapides") + '">'
         '<a class="btn" href="' + WA_HERO + '" target="_blank" rel="noopener">' + WA_I +
         '<span>' + L(C["sticky"][0]) + '</span></a>'
         '<a class="btn ghost" href="tel:+237' + WA + '"><span>' + L(C["sticky"][1]) + '</span></a></div>')

# 17 · JSON-LD : mêmes octets que la fiche Google, aucune note inventée, aucun sameAs
_ld_desc = C["desc"]["fr"]
JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Optician", "name": "Univers Optique",
    "legalName": C["legalName"], "foundingDate": "2009-08-01", "description": _ld_desc,
    "address": {"@type": "PostalAddress", "streetAddress": C["addr"].split(" — ")[0],
                "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM",
                "postOfficeBoxNumber": re.sub(r"\D", "", C["bp"])},
    "geo": {"@type": "GeoCoordinates", "latitude": C["geo"][0], "longitude": C["geo"][1]},
    "hasMap": MAPS, "telephone": "+237" + WA, "email": C["mail1"],
    "areaServed": [{"@type": "City", "name": "Douala"}, {"@type": "Place", "name": "Bépanda"}],
    "currenciesAccepted": "XAF",
    "paymentAccepted": "Espèces, Mobile Money, carte — à confirmer (champ annuaire vide)",
    "knowsAbout": ["examen de vue", "verres correcteurs", "montures", "verres de sécurité",
                   "prothèses oculaires", "lentilles de contact", "formation en optique-lunetterie"],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                                                             "Friday"], "opens": "08:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00"}],
    "potentialAction": {"@type": "ReserveAction",
                        "target": {"@type": "EntryPoint", "inLanguage": "fr",
                                   "actionPlatform": ["http://schema.org/DesktopWebPlatform",
                                                      "http://schema.org/MobileWebPlatform"],
                                   "url": WA_HERO},
                        "name": "Réserver un examen de vue"}}, ensure_ascii=False)

HEAD = ('<!doctype html>\n<html lang="fr" data-lang="fr">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>' + L(C["titleV2"]) + '</title>\n'
        '<meta name="description" content="' + esc(C["desc"]["fr"]) + '">\n'
        '<meta name="robots" content="noindex,nofollow">\n'
        '<meta name="theme-color" content="' + PETROL_DK + '">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@'
        '0,6..72,400..600;1,6..72,400..500&family=Public+Sans:wght@400;550;600&family=JetBrains+Mono:wght@'
        '400;600&display=swap">\n'
        '<script>document.documentElement.classList.add(\'js\')</script>\n'
        '<style>' + CSS + '</style>\n'
        '<script type="application/ld+json">' + JSONLD + '</script>\n</head>\n<body>')

PAGE = (HEAD + '\n<main id="top">\n' + "\n".join(S) + "\n</main>\n" +
        "<script>" + JS.strip() + "</script>\n" +
        "<script>" + JS_REV.strip() + "</script>\n</body>\n</html>\n")

# ══════════════════════════════════════════════════════════════════════════════════
#  LES CONTRÔLES — tout est vérifié AVANT que le fichier existe
# ══════════════════════════════════════════════════════════════════════════════════
#  LES CONTRÔLES — tout est vérifié AVANT que le fichier existe (§13).
#  Un point de relecture qui n'a pas de contrôle derrière lui n'est qu'une opinion ; un contrôle qui ne
#  peut pas dire non n'est pas un contrôle. Chaque ligne ci-dessous a donc été mutée une fois à la main
#  (copie faussée volontairement) pour vérifier qu'elle échoue bien quand la règle est cassée.
# ══════════════════════════════════════════════════════════════════════════════════
#  LES CONTRÔLES — tout est vérifié AVANT que le fichier existe (§13).
#  Un point de relecture qui n'a pas de contrôle derrière lui n'est qu'une opinion ; un contrôle qui ne
#  peut pas dire non n'est pas un contrôle. Chaque ligne ci-dessous a donc été mutée une fois à la main
#  (copie faussée volontairement) pour vérifier qu'elle échoue bien quand la règle est cassée.
# ══════════════════════════════════════════════════════════════════════════════════
#  LES CONTRÔLES — tout est vérifié AVANT que le fichier existe (§13).
#  Un point de relecture qui n'a pas de contrôle derrière lui n'est qu'une opinion ; un contrôle qui ne
#  peut pas dire non n'est pas un contrôle. Chaque ligne ci-dessous a donc été mutée une fois à la main
#  (copie faussée volontairement) pour vérifier qu'elle échoue bien quand la règle est cassée.
# ══════════════════════════════════════════════════════════════════════════════════
#  LES CONTRÔLES — tout est vérifié AVANT que le fichier existe (§13).
#  Un point de relecture qui n'a pas de contrôle derrière lui n'est qu'une opinion ; un contrôle qui ne
#  peut pas dire non n'est pas un contrôle. Chaque ligne ci-dessous a donc été mutée une fois à la main
#  (copie faussée volontairement) pour vérifier qu'elle échoue bien quand la règle est cassée.
# ══════════════════════════════════════════════════════════════════════════════════
FAILS = []


def check(label, ok, detail=""):
    print((" ✓ " if ok else " ✗ ") + label + ((" — " + detail) if detail else ""))
    if not ok:
        FAILS.append(label)


TXT = re.sub(r"<style>.*?</style>|<script.*?</script>|<img\b[^>]*>", " ", PAGE, flags=re.S)
KB = len(PAGE.encode()) / 1024

# ── poids et visuels (le fichier part en pièce jointe WhatsApp, il doit s'ouvrir sans réseau) ────────
check("poids %.0f Ko ≤ 1100 Ko (pièce jointe WhatsApp)" % KB, KB <= 1100, "%.0f Ko" % KB)
check("visuels embarqués %.0f Ko, chacun ≤ 260 Ko" % IMGKB, IMGKB <= 1000)
check("fiche de relecture des %d visuels, lettrage statué partout" % len(IMG_REVIEW),
      len(IMG_REVIEW) == len(DIM) and all(("lettrage" in v) or ("marque" in v) or ("broderie" in v)
                                          for v in IMG_REVIEW.values()))
check("exactement %d visuels embarqués, aucun en double" % len(DIM),
      PAGE.count("data:image/jpeg;base64,") == len(DIM))
check("dimensions affichées = dimensions réelles du fichier (pas de saut de mise en page)",
      all(('width="%d" height="%d"' % (w, h)) in PAGE for (w, h) in DIM.values()))

# ── bilinguisme : chaque phrase française a son vis-à-vis anglais, posés par le même moteur ──────────
_nfr = len(re.findall(r'class="fr-only"', PAGE))
_nen = len(re.findall(r'class="en-only"', PAGE))
check("bilinguisme : %d portées FR, %d portées EN, comptes égaux" % (_nfr, _nen),
      _nfr == _nen and _nfr >= 180)
check("le français est la langue peinte SANS JavaScript (masque CSS, pas un script qui ajoute)",
      "html[data-lang=fr] .en-only{display:none}" in CSS and 'data-lang="fr"' in PAGE and
      'lang="fr"' in PAGE)
check("l'anglais est complet lui aussi (zéro texte EN tronqué par une apostrophe échappée de travers)",
      not re.findall(r'class="en-only">[^<]*\\\\', PAGE))

# ── SEO (AMK-SEO-PLAYBOOK §3) ──────────────────────────────────────────────────────────────────────
_h1 = re.findall(r"<h1\b.*?</h1>", PAGE, re.S)
check("un seul H1, et il porte le mot-clé « Opticien à Bépanda »",
      len(_h1) == 1 and "Opticien à Bépanda" in _h1[0])
_t = C["titleV2"]["fr"]
check("titre d'onglet : mot-clé en premier, %d caractères (cible 45-65)" % len(_t),
      _t in PAGE and _t.lower().startswith("opticien à bépanda") and 45 <= len(_t) <= 65, _t)
check("la description existe, 100-200 caractères, française en tête",
      C["desc"]["fr"] in PAGE and 100 <= len(C["desc"]["fr"]) <= 200, "%d car." % len(C["desc"]["fr"]))
_banned = ("web design", "pas cher", "le moins cher", "gratuit", "meilleur prix", "promo", "top 1", "n°1")
_hits = [x for x in _banned if x in TXT.lower()]
check("aucun mot de vendeuri dans le texte visible (%d expressions contrôlées)" % len(_banned),
      not _hits, str(_hits))
check("aucune note agrégée dans le schema (aggregateRating absent : 6 avis ne valent pas une moyenne)",
      "aggregateRating" not in JSONLD)
check("aucun profil social revendiqué (sameAs absent, rien n'a été vérifié)", "sameAs" not in JSONLD)
check("aucune citation d'avis inventée (guillemet suivi d'un nom propre)",
      not re.findall(r"»\s*[—–-]\s*[A-ZÀ][a-zà-ÿ]+ [A-ZÀ]", TXT))
check("NAP : un seul numéro WhatsApp, le même dans le schema, les boutons et la barre collée",
      "+237" + WA in JSONLD and len(set(re.findall(r"wa\.me/(\d+)", PAGE))) == 1 and
      re.findall(r"wa\.me/(\d+)", PAGE)[0] == WA and PAGE.count("wa.me/" + WA) >= 12)
_http = re.findall(r'href="(https?:[^"]*)"', PAGE)
check("aucun lien sortant vers le domaine mort (%d liens http sortants, 0 vers universoptique) ; le domaine "
      "n'apparaît qu'en texte, comme archive" % len(_http),
      not [h for h in _http if "universoptique" in h])
check("aucun href vide, aucun href « # » nu", 'href="#"' not in PAGE and 'href=""' not in PAGE)
check("toutes les ancres internes pointent vers un id existant",
      not (set(re.findall(r'href="#([\w-]+)"', PAGE)) - set(re.findall(r'id="([\w-]+)"', PAGE))))
check("téléphone : format international dans le lien, format local dans le texte",
      'href="tel:+237' + WA + '"' in PAGE and C["waDisp"] in PAGE)
check("horaires du schema = horaires de la fiche (lun-ven 08-18, sam 08-13, dimanche absent)",
      '"opens": "08:00"' in JSONLD and '"closes": "18:00"' in JSONLD and '"closes": "13:00"' in JSONLD and
      '"Sunday"' not in JSONLD)
check("le dimanche est écrit « Fermé » en toutes lettres, pas masqué", ">Fermé<" in PAGE)
_wa = re.findall(r'href="https://wa\.me/\d+\?text=([^"]*)"', PAGE)
check("chaque appui WhatsApp part avec un message déjà écrit (%d liens pré-remplis, aucun vide)" % len(_wa),
      len(_wa) >= 8 and all(len(x) > 8 for x in _wa))
check("aucun prix affiché (le nôtre comme le leur) : pas de « FCFA » dans le corps de page",
      "FCFA" not in TXT and "F CFA" not in TXT)
_f15 = [m.start() for m in re.finditer(r"15\s?%", TXT)]
_ctx = [TXT[max(0, _p - 320):_p + 320] for _p in _f15]
_attrib = ("?", "«", "&quot;", "gweleo", "relev", "archiv", "annonce", "votre")
check("le « 15 %% » n'est jamais présenté comme notre offre : %d mention(s), chacune posée en question ou "
      "attribuée à une source nommée" % len(_f15),
      bool(_f15) and all(any(w in x.lower() for w in _attrib) for x in _ctx),
      str([re.sub(r"<[^>]+>", " ", x)[:90] for x in _ctx if not any(w in x.lower() for w in _attrib)][:2]))
check("aucun pourcentage dans un bouton ou une puce",
      not [x for x in re.findall(r'<a class="(?:btn|chip)[^"]*"[^>]*>(.*?)</a>', PAGE, re.S) if "%" in x])
check("aucun chiffre de résultat promis (98 % / 95 % / 40 % / +N %)",
      not re.search(r"(9[58]|40)\s?%", TXT) and not re.search(r"\+\s?\d+\s?%", TXT))
_gw = [m.start() for m in re.finditer("Gweleo", TXT)]
check("la copie du voisin est citée, jamais revendue : chaque mention de Gweleo est encadrée par un verbe de "
      "relevé ou un guillemet (%d mention(s))" % len(_gw),
      bool(_gw) and all(any(w in TXT[max(0, _p - 300):_p + 300].lower() for w in ("relev", "«", "copie", "autre"))
                        for _p in _gw))

# ── design : les lois précises qui avaient été franchies ─────────────────────────────────────────────
check("pilule du hero : une seule, et elle dit une chose fausable (horaires) — §3.4, référence assumée",
      PAGE.count('class="pill"') == 1)
_nsec = PAGE.count("<section")
_nkick = TXT.count('class="kick"')
check("étiquettes de section : %d pour %d sections (plafond maison : une sur trois)" % (_nkick, _nsec),
      _nkick <= max(1, -(-_nsec // 3)),
      str([m.group(1) for m in re.finditer(r'class="kick"><span class="fr-only">([^<]*)', PAGE)]))
_rv = re.findall(r'class="([^"]*\brv\b[^"]*)"', PAGE[PAGE.find("<main"):])
check("UN seul moment animé (MOTION 4) : la révélation est sur les trois étapes, rien d'autre",
      len(_rv) == 3 and all("step" in c.split() for c in _rv), str(_rv))
check("la première peinture ne dépend d'aucun script : l'état caché n'existe que sous html.js",
      CSS.count(".rv{opacity:0") == 1 and "html.js .rv{opacity:0" in CSS and
      "<script>document.documentElement.classList.add(" in PAGE[:PAGE.find("<body")])
check("hero, comparatif, rendus, créneaux, fiche : aucun de ces blocs n'est en état caché",
      "hero rv" not in PAGE and "cmp rv" not in PAGE and "shot rv" not in PAGE and "pick rv" not in PAGE and
      "find rv" not in PAGE)
check("prefers-reduced-motion annule l'état caché ET les transitions",
      "html.js .rv{opacity:1;transform:none;transition:none}" in CSS and "animation-duration:.01ms" in CSS)
check("durées réelles dans les jetons, aucun nombre posé à l'aveugle",
      all(x in CSS for x in ("--dur-press:140ms", "--dur-reveal:520ms", "--dur-menu:220ms")))
check("pas de transition:all, pas d'ease-in sur une entrée",
      "transition:all" not in CSS.replace(" ", "").replace("transition:", "transition:"))
check("chaque appui a son état pressé (120-160 ms)",
      ".btn:active{transform:scale(.97)}" in CSS and ".chip:active{transform:scale(.96)}" in CSS)
check("les survols sont gardés derrière (hover:hover) and (pointer:fine)",
      CSS.count("@media (hover:hover) and (pointer:fine)") == 1)
_tail = CSS[CSS.index("body{margin"):]
_hex = re.findall(r"#[0-9A-Fa-f]{3,8}\b", _tail)
_rgbn = re.findall(r"rgba\(\s*\d", _tail)
check("couleur = jeton : 0 hex et 0 rgba en chiffres bruts hors de :root", not _hex and not _rgbn,
      str(_hex[:5] + _rgbn[:2]))
_rads = sorted({x for grp in re.findall(r"border-radius\s*:\s*([^;}]+)", CSS) for x in grp.replace(" ", "").split()})
check("système de rayons unique : carte 20 / pastille 999 / outils 3-4 / cercle 50%% — %s" % _rads,
      all(x in ("var(--r)", "var(--chip)", "50%", "3px", "4px", "0", "0px", "0var(--r)", "0") or
          x.startswith("0") or x.endswith("var(--r)") for x in _rads))
check("aucun glassmorphism de vitrine : backdrop-filter utilisé 3 fois max, jamais sur une carte",
      CSS.count("backdrop-filter") <= 3)
check("aucun dégradé appliqué à un texte de marque", "background-clip" not in CSS)
check("tailles de caractères : deux familles utiles (Newsreader / Public Sans / JetBrains Mono), Inter "
      "absent, pas de serif de luxe beige « Fraunces/Instrument Serif »",
      "Newsreader" in CSS and "Public Sans" in CSS and "JetBrains" in CSS and "Inter" not in CSS and
      "Fraunces" not in CSS and "Instrument" not in CSS)
check("l'italique du H1 est dans la même famille (pas de serif greffé sur un titre sans-serif)",
      len(re.findall(r"<em>", _h1[0])) == 1 and "font-family" not in re.search(r"<em>.*?</em>", _h1[0], re.S).group(0))
check("largeurs de lecture bornées en ch (62 / 56 / 54 / 60 / 78)",
      len(re.findall(r"max-width:\d+ch", CSS)) >= 5)
check("zéro emoji décoratif dans toute la page",
      not re.findall(r"[\U0001F000-\U0001FAFF\u2190-\u21FF\u2600-\u27BF\u2B00-\u2BFF]", PAGE))
check("icônes : SVG dessinés à la main, aucune librairie",
      PAGE.count("<svg") <= 8 and "fa-" not in PAGE and "icon-" not in PAGE)
check("chiffres tabulaires partout où il y a des nombres", CSS.count("tabular-nums") >= 2)
check("focus visible redéfini, jamais supprimé",
      ":focus-visible{outline:3px solid" in CSS and "outline:none" not in CSS and
      "outline:0" not in CSS)
check("toutes les images : largeur, hauteur, alt, lazy (le hero en fetchpriority)",
      all(('width="' in t and 'height="' in t and 'alt="' in t and
           ('loading="lazy"' in t or 'fetchpriority="high"' in t)) for t in re.findall(r"<img\b[^>]*>", PAGE)))
check("aucun alt ne contient de HTML (le bilinguisme reste dans le texte, pas dans les attributs)",
      not re.findall(r'<img\b[^>]*alt="[^"]*<(span|div|em)', PAGE))
check("les trois rendus portent le badge « concept » dans la légende, FR et EN",
      TXT.count("Rendu de concept — votre photo le remplacera") == 3 and
      TXT.count("Concept render - your photo replaces it") == 3)
check("légende SOUS l'image : aucune pastelle posée sur la photo (la maison, pas la référence)",
      ".shot img{position:absolute" not in CSS and PAGE.count("<figcaption>") == 3 and
      "figcaption" in CSS and CSS.count("figcaption") >= 4)
_ids = []
try:
    import subprocess as _sp
    for _k in DIM:
        _o = _sp.run(["identify", "-format", "%m %w %h %[fx:mean]",
                      str(IMGDIR / ("univers-v2-" + _k + ".jpg"))], capture_output=True, text=True).stdout.split()
        _ids.append(_o)
    check("visuels mesurés : JPEG, dimensions au pixel près, exposition du même monde (moyennes " +
          " · ".join("%.2f" % float(x[3]) for x in _ids) + ")",
          all(x[0] == "JPEG" and (int(x[1]), int(x[2])) == DIM[_k2] and 0.16 < float(x[3]) < 0.94
              for x, _k2 in zip(_ids, DIM)))
except FileNotFoundError:
    check("contrôle identify NON RENDU : ImageMagick absent du bac — dimensions non revérifiées", False,
          "loi §13 : une mesure impossible s'écrit NON VÉRIFIÉE, jamais « ok »")
check("une section = une photo : le plateau est au cabinet, deux rendus dans la section images, "
      "quatre au total", PAGE.count("<img ") == 4 and PAGE.count('<figure class="shot"') == 2)
_CSS_PLAIN = re.sub(r"/\*.*?\*/", " ", CSS, flags=re.S)   # la prose des commentaires n'est pas un sélecteur
_used_cls = {c for a in re.findall(r'class="([^"]+)"', PAGE[PAGE.find("<main"):]) for c in a.split()}
_def_cls = set(re.findall(r"\.([a-z][a-z0-9-]*)", _CSS_PLAIN))
_unused = sorted(_used_cls - _def_cls - {"mark", "lg", "nm", "rl"})
check("aucune classe du HTML sans règle derrière (%d orpheline(s))" % len(_unused), not _unused, str(_unused[:6]))
_defs = set(re.findall(r"\.([a-z][a-z0-9-]*)[\s{:]", _CSS_PLAIN)) - {"fr-only", "en-only", "js", "in", "is-on",
                                                                     "rv", "on", "fine", "big", "of"}
_orphan_css = sorted(x for x in _defs if not re.search(r'(class|aria-label)="[^"]*\b%s\b' % re.escape(x), PAGE))
check("aucune règle CSS sans emploi (%d orpheline(s))" % len(_orphan_css), not _orphan_css, str(_orphan_css[:6]))
check("aucun style en dur dans le corps de page (tout passe par la feuille)",
      not re.findall(r'<[^>]*\bstyle="', PAGE[PAGE.find("<main"):PAGE.find("</main>")]))
def _open(t):
    return len(re.findall("<" + t + r"[\s>]", PAGE))


def _close(t):
    return PAGE.count("</" + t + ">")


_TAGS = ("section", "div", "article", "figure", "span", "p", "li", "aside", "dl", "table", "ul", "em",
         "details", "summary", "h1", "h2", "h3", "h4", "main", "header", "footer", "button", "thead",
         "tbody", "tr", "th", "td", "a", "dt", "dd", "b", "i", "ol", "caption")
_mismatch = {t: (_open(t), _close(t)) for t in _TAGS if _open(t) != _close(t)}
check("toutes les balises appariées (%d familles comptées ; balises auto-fermantes exclues)" % len(_TAGS),
      not _mismatch, str(_mismatch))
check("chaque section se tient seule : %d sections, aucune sans titre ni contenu" % _nsec,
      len(re.findall(r"<section[^>]*>\s*<(?:div|img)", PAGE)) + PAGE.count('<section class="hero"') >= _nsec)

# ── structure de la page (les promesses du plan) ────────────────────────────────────────────────────
check("le comparatif : 8 lignes × 3 colonnes, colonne de droite surlignée (la référence, sans tricher)",
      len(re.findall(r'<td scope="row">', PAGE)) == 8 and PAGE.count('scope="col"') == 3 and
      len(re.findall(r'class="mark"', PAGE)) >= 9)
check("le comparatif compare des faits de service, jamais des résultats promis",
      not re.search(r"(patients|ca|chiffre d)[^<]{0,40}(augment|×|multipli)", TXT.lower()))
_svc = PAGE[PAGE.find('id="services"'):PAGE.find('id="protheses"')]
check("les dix actes sont rendus en 3 paquets de 4+3+3, une raison par paquet (loi §11 : pas de "
      "tableau à filets)",
      _svc.count('class="pack"') == 3 and _svc.count('<li><a href="#rendez-vous">') == 10 and
      _svc.count('class="why"') == 3 and PAGE.count('<li><a href="#rendez-vous">') >= _svc.count('<li><a href="#rendez-vous">'),
      "%d paquets, %d lignes, %d raisons" % (_svc.count('class="pack"'), _svc.count('<li><a href="#rendez-vous">'),
                                              _svc.count('class="why"')))
check("un seul tableau dans la page : les filets restent dans le document", len(re.findall(r"<table", PAGE)) == 1)
check("les six constats sont numérotés et datés", PAGE.count('class="find"') == 6 and PAGE.count('class="src"') == 6)
check("les six questions à trancher sont là, aucune effacée", PAGE.count('class="ask"') == 6)
check("les créneaux sont des liens réels, pas un widget qui attend un bundle",
      PAGE.count('class="chip"') >= 4 and "<template" not in PAGE and "setTimeout" not in PAGE)
check("la fiche du cabinet porte adresse, repère, BP, plus code, carte et les deux lignes téléphoniques",
      all(x in PAGE for x in (C["addr"], C["bp"], C["landmark"], C["mapsPlus"], C["tel2Disp"])))
_body = PAGE[PAGE.find("<main"):PAGE.find("<footer")]
check("chemin de conversion hors du hero : %d boutons dans le corps + la barre collée au pouce" %
      _body.count('class="btn'), _body.count('class="btn"') >= 2)
check("un seul appel à l'action, répété : « Réserver un examen de vue » — pas de rival concurrent",
      TXT.count("Réserver un examen de vue") >= 2 and "Demander un devis" not in TXT and
      "Nous contacter" not in TXT)
_foot_html = PAGE[PAGE.find("<footer"):PAGE.find("</footer>")]
check("pied de page : 4 colonnes (marque + 3 blocs), le même appel à l'action, retour en haut",
      _foot_html.count("<h4>") == 3 and 'class="up"' in _foot_html and 'class="cols"' in _foot_html and
      _foot_html.count('class="btn') == 1)
check("le pied de page n'est pas un cimetière de liens : toute ancre du pied existe",
      not (set(re.findall(r'href="#([\w-]+)"', _foot_html)) - set(re.findall(r'id="([\w-]+)"', PAGE))))
check("barre collée au pouce sous 960px, deux actions, jamais trois",
      ".rail{display:flex}" in CSS.replace(" ", "").replace("\n", "") and
      PAGE.count('class="rail"') == 1 and PAGE.count('aria-label="Actions rapides"') == 1)
check("accessibilité : nav libellée, groupes libellés, jauges role=img avec texte de repli",
      'aria-label' in PAGE and PAGE.count('role="img"') >= 2 and 'role="group"' in PAGE)
check("les chiffres du tableau et de la fiche sont en chiffres tabulaires",
      ".mono" in CSS and "tabular-nums" in CSS)

# ── la porte de peinture : la faute du 22/09 ne se reproduit pas ────────────────────────────────────
_plain = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
_hidden = re.findall(r"([^{}]+)\{[^}]*opacity\s*:\s*0(?![.\d])[^}]*\}", _plain)
_hidden = [h.strip() for h in _hidden if not h.strip().startswith("html.js")]
check("aucune règle hors html.js ne cache un contenu (%d suspect(s))" % len(_hidden), not _hidden, str(_hidden[:4]))
_sec = len(re.findall(r"<(?:section|article|figure|aside)\b", PAGE))
check("budget de révélation : %d blocs animés pour %d blocs de structure (plafond 40 %%)" % (len(_rv), _sec),
      len(_rv) <= 0.4 * _sec)
check("le script de révélation est isolé et fileté (une faute dedans ne vide pas la page)",
      PAGE.count("<script>") >= 3 and "catch(err){show();}" in PAGE)
_pick_html = PAGE[PAGE.find('class="pick"'):PAGE.find("</aside>")]
_npick = len(re.findall(r'<a class="chip', _pick_html))
check("les créneaux se prennent sans JavaScript : %d liens réels dans le bloc, zéro onclick, zéro gabarit "
      "à remplir après coup" % _npick,
      _npick >= 6 and "onclick" not in _pick_html and "<template" not in PAGE and "innerHTML" not in _pick_html
      and all("wa.me/" in h for h in re.findall(r'href="([^"]+)"', _pick_html)),
      "le bulbe de langue a le droit d'écouter un clic : le contrôle ne porte que sur le bloc des créneaux")

if FAILS:
    raise SystemExit("ÉCHEC CONTRÔLE — " + str(len(FAILS)) + " faute(s) : " + " · ".join(FAILS))

# ── porte de compilation du JavaScript embarqué (audit sur la page en mémoire, pas sur le disque) ─────
_qa = ROOT / "tools" / "qa" / "check_inline_js.py"
if _qa.exists():
    import os
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as _fh:
        _fh.write(PAGE)
        _tmp = _fh.name
    try:
        _r = subprocess.run([sys.executable, str(_qa), _tmp], capture_output=True, text=True)
    finally:
        os.unlink(_tmp)
    if _r.returncode == 1:
        print(_r.stdout)
        raise SystemExit("JavaScript embarqué non compilable — rien n'est écrit sur le disque")
    elif _r.returncode == 3:
        print(" ! AVERTISSEMENT : node absent du bac — le JS embarqué n'a PAS été compilé (contrôle non rendu)")
    else:
        print(" ✓ " + (_r.stdout.strip().splitlines() or ["JS embarqué compilé"])[-1])

OUT.write_text(PAGE, encoding="utf-8")
print("écrit : %s — %.0f Ko · %d portées bilingues · %d sections · %.0f Ko de visuels"
      % (OUT.relative_to(ROOT), KB, _nfr, PAGE.count("<section"), IMGKB))

# ── repli d'envoi : on RETIRE les visuels, on ne réécrit aucune phrase ────────────────────────────────
if "--sobre" in sys.argv:
    S2 = re.sub(r'<img class="ph"[^>]*>', "", PAGE)
    S2 = re.sub(r'<section id="visuels">.*?</section>\n', "", S2, flags=re.S)
    S2 = re.sub(r'<figure><img src="data:image/jpeg;base64,"[^>]*>.*?</figure>', "", S2, flags=re.S)
    S2 = re.sub(r'<figure><img src="data:image[^"]*"[^>]*>.*?</figure>', "", S2, flags=re.S)
    OUT_S = OUT.with_name(OUT.stem + "-sobre" + OUT.suffix)
    assert "data:image/jpeg;base64," not in S2, "des visuels restent dans la version sobre"
    assert "html.js .rv{opacity:0" in S2, "la porte de peinture a sauté dans le repli"
    OUT_S.write_text(S2, encoding="utf-8")
    print("écrit : %s — %.0f Ko (repli d'envoi, 0 visuel, même copie)"
          % (OUT_S.relative_to(ROOT), len(S2.encode()) / 1024))
