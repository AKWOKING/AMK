#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM Optique — « La monture cherche son nom », épisode 1 (H08) — moteur de rendu.

1080×1920 · 30 fps · **deux rendus** : muet et parlé (29,53 s) · **film calme** (aucun motion design,
tour 199) · **script final de King** (tour 200) · **sans tournage, sans le médecin** — et, depuis le tour 198, avec **une seule image générée** (un visage portant la monture),
déclarée au kit §8.

Pourquoi cette pièce (27/10/2026, tour 194)
-------------------------------------------
King a demandé laquelle des deux séries d'abonnés peut se faire **sans le docteur et sans visage**.
Réponse : celle-ci, parce que sa matière est **déjà au dépôt** — une photo de monture prise au cabinet
(`hosting/previews/dmoptic/montures/`), la référence que le site publie déjà (H08 · double pont, aviateur,
noir et doré), et la carte crème des fiches produit. Aucun être humain n'entre dans le cadre.

Tour 195 : la voix (King : « add voice »)
-----------------------------------------
Le film n'est plus monté sur un minutage écrit à la main, mais **sur la voix** — parce que la doctrine
interdit de comprimer une accroche pour la faire entrer dans une durée décidée d'avance
(`knowledge/HOOK-FIRST-2026-10-27.md`). `PLAN` porte le texte de chaque beat ; `measure_clips()` mesure
les clips **nettoyés** (silence de tête et de queue retiré) ; `timeline()` en déduit les bornes. La voix
ne bouge jamais, c'est l'image qui se cale.

Les six beats (`--voice-dir`), et le plan qui va avec
------------------------------------------------------
b1  0,00–3,93  « Elle n'a pas de nom. Vous choisissez celui qui reste. »
b2  4,21–8,97  « Sur notre site, quarante montures. Tous s'appellent par un code. »
b3  9,25–15,13  « Celle-ci s'appelle H zéro huit. Deux noms sont sur la table : Éclat ou Minuit. »
b4 15,41–19,26  « Elle ira sur un visage, tous les jours. Elle mérite mieux qu'un code. »
b5 19,54–22,93  « Le nom qui gagne s'écrit sur sa page, et il y reste. »
b6 23,21–26,10  « Écrivez A, B, ou votre mot. On vous montre le nom qui gagne. » → carton final

Le scénario, les rôles et le jeu en trois manches vivent dans
`clients/dm-optic/content/month1/w3/MONTURE-01-SCRIPT.py` — ce fichier-ci ne fait que rendre l'image
et la voix. La porte du récit lit ce script-là, pas celui-ci.

Un beat long se découpe **toujours** en 2–3 plans (`shots`) : un carton unique tenu sur une macro de
6,7 s produit une fenêtre figée que `audit_video_motion` attrape (vécu sur b3 au premier rendu parlé).
La première seconde a deux mouvements à elle seule — une poussée de 0,45 s et les deux lignes du carton
qui arrivent à 0,22 s d'intervalle : c'est la seule fenêtre où le pouce hésite encore.

Tour 198 : les trois images (King, 27/10 : « en plus du script et ce qui apparaît à l'écran, ajoute des images »)
---------------------------------------------------------------------------------------------------------
Trois inserts, un par beat nommé, et **de la matière réelle** partout où c'est possible :

| beat | ce qu'on voit | d'où ça vient |
|---|---|---|
| b2 « quarante montures, toutes avec un code » | **la page du catalogue hommes**, qui défile | capture Chromium du vrai site (`tools/video/capture.mjs --mode full`) |
| b4 « elle ira sur un visage » | une personne portant la H08 | **image générée** (`generate_image`, référence = la photo du cabinet) — l'exception demandée par King |
| b5 « le nom… s'écrit sur sa page » | **la fiche H08** du site, posée dans le cadre | même capture, `fiche_card()` |

Les deux captures sont **coupées avant le raccord** que produit la capture pleine page (le haut de la page
réapparaît une seconde fois) : catalogue 0→8 150 px, fiche 0→2 200 px. Sans cette coupe, le plan montre une
page qui bégaie.

Aucun mouvement n'est figé : chaque plan est une fenêtre qui se déplace dans un master plus grand
(`crop_window`), et les textes arrivent en glissant. C'est la leçon du 23/10 : sur TikTok, la moitié de
l'audience part avant **0:02** (`ANALYSE-POST-1` §7).

Usage
-----
    python3 tools/record/make_dmoptic_monture.py --out clients/dm-optic/content/month1/w3/assets/monture-01.mp4
    python3 tools/record/make_dmoptic_monture.py --voice-dir /tmp/voixF --out /tmp/monture-voix.mp4  # parlé
    python3 tools/record/make_dmoptic_monture.py --preview /tmp/monture-preview   # 6 PNG de contrôle
    python3 tools/record/make_dmoptic_monture.py --cover <chemin.jpg>             # couverture 1080x1920

Portes avant publication : `tools/qa/audit_video_motion.py <fichier>` (aucune fenêtre figée) et
`tools/qa/audit_post_dm.py <kit>.md <fichier>` (le kit de publication).
"""
import argparse
import os
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_dmoptic_tiktok as base  # noqa: E402  (mêmes masters, mêmes polices, même mouvement)

ROOT = base.ROOT
SITE = base.SITE
W, H, FPS = base.W, base.H, base.FPS
DUR = 14.2          # valeur de repli (version muette) ; la version parlée calcule la sienne

# ── LE MODE CALME (King, 27/10, tour 199) ────────────────────────────────────────────────────────
# « remove all the motion design elements, the images move too much ». Le film passe donc en
# **images fixes + coupes franches** : plus de poussée, plus de panoramique, plus de bandeau qui
# glisse, plus de filet qui grandit. Ce qui bouge encore : les coupes (le montage) et l'apparition
# du texte (0,12 s de fondu). `--mouvement` rend l'ancien film, pour comparer.
CALME = True

NIGHT, PAPER, EMBER, BRAND, WA, CREAM = base.NIGHT, base.PAPER, base.EMBER, base.BRAND, base.WA, base.CREAM
F_TITLE, F_HEAD, F_BODY, F_MONO = base.F_TITLE, base.F_HEAD, base.F_BODY, base.F_MONO
font, ease, crop_window = base.font, base.ease, base.crop_window

PHOTO = "montures/monture-h08.webp"

# ── LE PLAN EST PILOTÉ PAR LA VOIX (ajout du 27/10, tour 195) ───────────────────────────────────
# La doctrine maison est explicite : **ce n'est pas le style qui choisit la longueur d'une accroche,
# c'est la place qu'on lui donne** (`HOOKS-2026-10-25` §7 bis) — et la voix ne se comprime pas pour
# entrer dans un montage. Donc : on enregistre, on **mesure**, et le montage se cale sur la mesure.
# Chaque beat = un clip de voix + un plan + ses cartons. Les cartons sont exprimés en **fractions** du
# beat : ils suivent la voix même si elle change de durée à la re-synthèse.
# `shots` = les plans d'un même beat de voix : (fin en fraction du beat, type, zoom, pan, drift).
# Un beat long est TOUJOURS coupé en deux plans. Motif mesuré le 27/10 : un carton unique tenu 6,7 s sur
# une macro de monture donne une fenêtre **figée** à 9-10 s (`audit_video_motion --window 1`) — le gate est
# bloquant, et il a raison : à l'écran, plus rien ne bouge pendant que la voix parle.
PLAN = [
    # ── LE SCRIPT DE KING (27/10, tour 200) — six beats, ses phrases, ses cartons ────────────────
    # b1 · 0–4,8 s · HOOK : « H08, c'est son code, pas un nom. Vous choisissez le surnom qui reste. »
    # La deuxième image n'est pas décorative : c'est le **catalogue du site**, où des montures portent
    # « H04 · Double pont doré », « H05 · … ». « C'est son code » se vérifie à l'écran. On ne dit
    # **aucun nombre** : King a lui-même posé la condition (« use this only if the spoken line about
    # 40 distinct frames is accurate ») et la ligne prononcée ne le dit pas.
    dict(clip="b1",
         shots=[(0.50, "card", 0.10, 0.0, -0.15), (1.00, "page", 0.0, 0.30, 0.30)],
         subs=[(0.00, 0.55, ["H08", "C'EST SON CODE"], 100, 0.690),
               (0.55, 1.00, ["ÉCLAT OU MINUIT ?"], 92, 0.698)]),
    # b2 · SHOW THE FRAME (King, 3–7 s) : « deux ou trois angles du même modèle, avec des coupes
    # rapides ». Trois cadrages du même produit, aucune image d'emprunt, aucune image générée.
    dict(clip="b2",
         shots=[(0.34, "macro", 0.30, 0.0, -0.10), (0.62, "macro", 0.08, 0.0, 0.0),
                (1.00, "page", 0.0, 0.30, 0.30)],
         subs=[(0.00, 0.42, ["REGARDEZ", "SES DÉTAILS"], 94, 0.695),
               (0.42, 1.00, ["40 MONTURES", "40 CODES"], 92, 0.690)]),
    # b3 · VOTE : la monture reste **entière** pendant qu'on décide (King : « keep the frame visible
    # while people decide ») — deux cadrages pleins, jamais la charnière seule.
    dict(clip="b3",
         shots=[(0.50, "vote", 0.0, 0.0, 0.0), (1.00, "vote", 0.0, 0.0, 1.0)],
         subs=[]),
    # b4 · SET THE RULE : le produit réel, aucun essayage (King : « only if you already have an
    # approved, accurate image » — nous n'en avons pas).
    dict(clip="b4",
         shots=[(0.62, "rule", 0.0, 0.0, 0.0), (1.00, "card", 0.24, 0.0, -0.15)],
         subs=[]),
    # b5 · CE QUI RESTE : la vraie fiche, sans laisser croire qu'elle est déjà renommée.
    dict(clip="b5",
         shots=[(0.50, "fiche", 0.0, 0.0, 0.0), (1.00, "fiche", 0.0, 0.28, 0.28)],
         subs=[(0.00, 1.00, ["ET IL RESTE", "SUR SA FICHE"], 94, 0.695)]),
    # b6 · CTA : « Suivez la page », puis le carton final.
    dict(clip="b6",
         shots=[(0.30, "card", 0.30, 0.10, -0.10), (0.60, "card", 0.10, 0.0, 0.0),
                (1.00, "end", 0.0, 0.0, 0.0)],
         subs=[(0.00, 0.42, ["SUIVEZ", "LA PAGE"], 100, 0.695)]),
]
TAIL = 0.9          # queue de respiration après le dernier mot : le carton final se lit
GAP = 0.28          # respiration entre deux beats (silence, pas de coupe sèche)

def macro_master(path, up=1.22, fx=0.5, fy=0.5):
    """La monture agrandie, **sur son propre fond** (la carte crème des fiches produit).

    Ce n'est pas une retouche : on recadre la photo réelle du cabinet au plus près du produit, et on
    l'agrandit. Le fond reste **le sien** — le blanc cassé des fiches — parce que changer ce fond serait
    retoucher le produit, ce que la maison ne fait pas. `fx`/`fy` choisissent la zone que le mouvement
    traversera (0 = gauche/haut, 1 = droite/bas).
    """
    src = Image.open(path).convert("RGB")
    bgcol = base.sample_bg(src)
    prod = base.tight_crop(src, bgcol, pad=0.06)
    cw, ch = int(W * up), int(H * up)
    canvas = Image.new("RGB", (cw, ch), bgcol)
    s = max(cw / prod.width, ch / prod.height)
    pw, ph = max(1, int(prod.width * s)), max(1, int(prod.height * s))
    prod = prod.resize((pw, ph), Image.LANCZOS).filter(
        ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    x0 = int((cw - pw) * fx)
    y0 = int((ch - ph) * fy)
    canvas.paste(prod, (x0, y0))
    return canvas


def end_card(t, t0, t1, K=1.22):
    """Carton final — bleu de marque, logo, la promesse de suite, le numéro. Mouvement continu."""
    p = (t - t0) / max(0.001, (t1 - t0))
    CW, CH = int(W * K), int(H * K)
    img = Image.new("RGB", (CW, CH), NIGHT)
    cx, cy = CW // 2, int(CH * 0.33)
    r = int(560 * K + 34 * K * p)
    halo = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for i in range(8, 0, -1):
        rr = int(r * i / 8)
        hd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=BRAND + (int(9 * (9 - i)),))
    img = Image.alpha_composite(img.convert("RGBA"), halo.filter(ImageFilter.GaussianBlur(30))).convert("RGB")
    d = ImageDraw.Draw(img)

    # le logo est un carré à fond blanc : on le pose sur une pastille crème, jamais en carré blanc nu
    logo = Image.open(os.path.join(SITE, "dm-logo.webp")).convert("RGBA")
    lw = int(206 * K * (1 + 0.05 * p))
    logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    lx, ly = (CW - logo.width) // 2, int(CH * 0.235)
    pad = int(16 * K)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((lx - pad, ly - pad, lx + logo.width + pad, ly + logo.height + pad),
                        radius=int(26 * K), fill=CREAM)
    img.paste(logo, (lx, ly), logo)
    d = ImageDraw.Draw(img)

    a = ease(min(1.0, (t - t0) / 0.55))
    y = int(CH * 0.435)
    f1 = font(F_HEAD, int(36 * K))
    d.text(((CW - d.textlength("RÉSULTAT MARDI", font=f1)) / 2, y), "RÉSULTAT MARDI",
           font=f1, fill=PAPER + (int(235 * a),))
    f2 = font(F_TITLE, int(72 * K))
    t2 = "A, B OU VOTRE SURNOM ?"
    d.text(((CW - d.textlength(t2, font=f2)) / 2, y + int(60 * K)), t2,
           font=f2, fill=(255, 255, 255, int(255 * a)))
    f3 = font(F_BODY, int(40 * K))
    t3 = "Le plus cité s'écrit sur sa fiche"
    d.text(((CW - d.textlength(t3, font=f3)) / 2, y + int(190 * K)), t3,
           font=f3, fill=PAPER + (int(200 * a),))

    a2 = ease(min(1.0, (t - t0 - 0.3) / 0.6))
    py = int(CH * 0.700) + int(14 * K * (1 - a2))
    fw = font(F_TITLE, int(60 * K))
    wtxt = "WhatsApp 656 122 239"
    tw = d.textlength(wtxt, font=fw)
    padx, pady = int(44 * K), int(28 * K)
    d.rounded_rectangle(((CW - tw) / 2 - padx, py, (CW + tw) / 2 + padx, py + int(60 * K) + 2 * pady),
                        radius=int(18 * K), fill=WA + (int(255 * a2),))
    d.text(((CW - tw) / 2, py + pady), wtxt, font=fw, fill=(255, 255, 255, int(255 * a2)))

    f4 = font(F_BODY, int(36 * K))
    t4 = "Ndobo Mayor · Immeuble West Hotel, 1er étage"
    d.text(((CW - d.textlength(t4, font=f4)) / 2, int(CH * 0.855)), t4,
           font=f4, fill=(190, 200, 216, int(225 * a2)))
    return img


def draw_subs(img, t):
    """Les textes à l'écran : arrivée en glissant (18 px), filet accent qui grandit, jamais de cadre figé."""
    for (s0, s1, lines, size, anchor) in SUBS:
        if not (s0 <= t < s1):
            continue
        if CALME:
            prog = min(1.0, (t - s0) / 0.12)
            out = 1.0 if t < s1 - 0.12 else max(0.0, (s1 - t) / 0.12)
        else:
            prog = ease((t - s0) / 0.42)
            out = 1.0 if t < s1 - 0.22 else max(0.0, (s1 - t) / 0.22)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        off = 0 if CALME else int(20 * (1 - prog))
        alpha = int(255 * prog * out)
        lh = int(size * 1.1)
        top = int(H * anchor) + off
        # bandeau derrière le texte : lisible sur la carte crème comme sur le carton marine
        block_h = lh * len(lines)
        pad = int(size * 0.40)
        d.rectangle((0, top - pad, W, top + block_h + int(pad * 0.35)),
                    fill=NIGHT + (int(248 * prog * out),))
        for i, line in enumerate(lines):
            # chaque ligne arrive avec 0,22 s de retard sur la précédente : deux mouvements au lieu d'un
            decal = prog if CALME else min(1.0, max(0.0, (t - s0 - 0.22 * i) / 0.42))
            a_ligne = int(alpha * ease(decal))
            if a_ligne <= 2:
                continue
            y_ligne = top + i * lh + (0 if CALME else int(12 * (1 - ease(decal))))
            f = font(F_TITLE, size)
            tw = d.textlength(line, font=f)
            d.text(((W - tw) / 2, y_ligne), line, font=f, fill=(255, 255, 255, a_ligne))
        half = int(W * 0.12) if CALME else int(W * 0.12 * prog)
        d.rectangle((W // 2 - half, top - int(pad * 0.55), W // 2 + half, top - int(pad * 0.55) + 7),
                    fill=EMBER + (255,))
        return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return img


BEATS = []          # (début, fin, type, zoom, pan, drift) — construits par `timeline()`
SUBS = []           # (début, fin, lignes, taille, ancrage) — idem


def timeline(durations, gap=GAP):
    """Construit BEATS et SUBS à partir des durées **mesurées** des clips de voix.

    Retourne la durée totale du film. Les cartons d'un beat sont placés en fraction de sa durée :
    si la voix change, les cartons suivent — on ne recale jamais la voix sur le montage.
    """
    global BEATS, SUBS, DUR
    BEATS, SUBS = [], []
    t = 0.0
    for i, beat in enumerate(PLAN):
        d = durations[beat["clip"]]
        if i == len(PLAN) - 1:
            d += TAIL          # le carton final a besoin de temps pour se lire
        borne = 0.0
        for (fin, kind, zoom, pan, drift) in beat["shots"]:
            BEATS.append((round(t + borne * d, 3), round(t + fin * d, 3), kind, zoom, pan, drift))
            borne = fin
        for (f0, f1, lignes, taille, ancrage) in beat["subs"]:
            SUBS.append((round(t + f0 * d, 3), round(t + f1 * d, 3), lignes, taille, ancrage))
        t += d + (gap if i < len(PLAN) - 1 else 0.0)
    DUR = round(t, 3)
    return DUR



def _panel(canvas, box, radius, fill):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill)
    return Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")


def vote_card(choix="A"):
    """LE CARTON DE VOTE — la monture en haut, A et B côte à côte en bas.

    C'est le seul plan du film où le spectateur doit **faire quelque chose** : les deux choix sont donc
    écrits en gros, encadrés, au même niveau, et la monture reste **entière** au-dessus (King : « keep
    the frame visible while people decide »). Un vote où l'on ne voit qu'une option n'est pas un vote.
    """
    canvas = Image.new("RGB", (W, H), NIGHT)
    prod = still_crop(MASTERS["card"], 0.0, 0.0, -0.10).crop((140, 380, 940, 1420))
    canvas.paste(prod.resize((760, 988), Image.LANCZOS), ((W - 760) // 2, 96))
    d = ImageDraw.Draw(canvas)
    fa = font(F_TITLE, 58)
    opts = ((64, 528, "A · ÉCLAT", PAPER, NIGHT), (552, 1016, "B · MINUIT", EMBER, (255, 255, 255)))
    if choix == "B":                       # même carton, l'autre option allumée — une coupe, pas un effet
        opts = (opts[0][:3] + (EMBER, (255, 255, 255)),) + (opts[1][:3] + (PAPER, NIGHT),)
    for (x0, x1, txt, bg, fg) in opts:
        canvas = _panel(canvas, (x0, 1090, x1, 1200), 18, bg + (255,))
        d = ImageDraw.Draw(canvas)
        d.text(((x0 + x1 - d.textlength(txt, font=fa)) / 2, 1112), txt, font=fa, fill=fg)
    fb = font(F_BODY, 42)
    t = "ou votre mot, en un seul"
    d.text(((W - d.textlength(t, font=fb)) / 2, 1232), t, font=fb, fill=(214, 224, 240))
    return canvas


def rule_card():
    """LE CARTON DE RÈGLE — quand, et où. Aucune image de produit : c'est une date, pas une vitrine."""
    canvas = Image.new("RGB", (W, H), NIGHT)
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 12), fill=EMBER)
    f1 = font(F_HEAD, 44)
    t1 = "LE SURNOM LE PLUS CITÉ"
    d.text(((W - d.textlength(t1, font=f1)) / 2, 470), t1, font=f1, fill=(190, 200, 216))
    f2 = font(F_TITLE, 132)
    for i, (txt, col) in enumerate(((("RÉSULTAT", (255, 255, 255)), ("MARDI", EMBER)))):
        d.text(((W - d.textlength(txt, font=f2)) / 2, 540 + i * 150), txt, font=f2, fill=col)
    # trois jours, un seul allumé : la date se lit sans être lue
    f3 = font(F_MONO, 34)
    jours = ("LUN", "MAR", "MER")
    bw, gap = 150, 26
    x0 = (W - (3 * bw + 2 * gap)) / 2
    for i, j in enumerate(jours):
        on = (j == "MAR")
        box = (x0 + i * (bw + gap), 900, x0 + i * (bw + gap) + bw, 990)
        canvas = _panel(canvas, box, 14, (EMBER + (255,)) if on else (255, 255, 255, 26))
        d = ImageDraw.Draw(canvas)
        d.text((box[0] + (bw - d.textlength(j, font=f3)) / 2, 926), j, font=f3,
               fill=(255, 255, 255) if on else (150, 162, 182))
    f4 = font(F_BODY, 40)
    t4 = "dans l'épisode 2 · ici même"
    d.text(((W - d.textlength(t4, font=f4)) / 2, 1040), t4, font=f4, fill=(200, 210, 226))
    return canvas


STILLS = {}         # cache des images fixes (mode calme) : un plan = une image, calculée une fois


def still_crop(big, zoom, pan, drift):
    """Un cadrage FIXE dans un master plus grand — l'image ne bouge pas d'un pixel."""
    s_ = 1.0 + max(0.0, zoom)
    cw, ch = int(big.width / s_), int(big.height / s_)
    ax, ay = big.width - cw, big.height - ch
    x0 = max(0, min(ax, int(ax * (0.5 + pan * 0.5))))
    y0 = max(0, min(ay, int(ay * (0.5 + drift * 0.5))))
    return big.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


def still(kind, zoom, pan, drift):
    """L'image d'un plan en mode calme. `pan`/`drift` gardent leur sens : fraction pour une page,
    décalage (−1…1) pour une photo."""
    key = (kind, round(zoom, 3), round(pan, 3), round(drift, 3))
    if key in STILLS:
        return STILLS[key]
    if kind == "end":
        img = still_crop(end_card(DUR, 0.0, DUR), 0.0, 0.0, 0.0)
    elif kind == "vote":
        img = vote_card("B" if drift > 0.5 else "A")
    elif kind == "rule":
        img = rule_card()
    elif kind == "page":
        f = (pan + drift) / 2.0                     # le milieu du défilement prévu
        img = page_window(MASTERS["page"], 0.5, f, f, 0.0)
    elif kind == "fiche":
        f = (pan + drift) / 2.0
        img = fiche_card(0.0, f, f, 0.0)
    else:
        img = still_crop(MASTERS[kind], zoom, pan, drift)
    STILLS[key] = img
    return img


def frame(i):
    t = i / FPS
    image_plan = None
    for (b0, b1, kind, zoom, pan, drift) in BEATS:
        if b0 <= t < b1:
            image_plan = (kind, zoom, pan, drift, 0.0)
            break
        if b0 <= t:
            # dernier plan déjà commencé : c'est lui qu'on tient pendant les respirations
            image_plan = (kind, zoom, pan, drift, 1.0)
    if image_plan is not None and CALME:
        kind, zoom, pan, drift, _ = image_plan
        img = still(kind, zoom, pan, drift)
    elif image_plan is not None:
        kind, zoom, pan, drift, fini = image_plan
        p = 1.0 if fini else (t - b0) / (b1 - b0)
        if kind == "end":
            big = end_card(t, b0, DUR)
        elif kind == "page":
            # `pan` = fraction de départ dans la page, `drift` = fraction d'arrivée
            img = page_window(MASTERS["page"], p, pan, drift, zoom)
            big = None
        elif kind == "fiche":
            img = fiche_card(p, pan, drift, zoom)
            big = None
        else:
            big = MASTERS[kind]
        if big is not None:
            img = crop_window(big, p, zoom, pan, drift)
    else:
        img = Image.new("RGB", (W, H), NIGHT)

    if t < 0.45 and not CALME and image_plan is not None and not image_plan[4]:
        k = 1.10 - 0.10 * ease(t / 0.45)
        w2, h2 = int(W * k), int(H * k)
        img = img.resize((w2, h2), Image.LANCZOS)
        img = img.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))

    img = draw_subs(img, t)
    d = ImageDraw.Draw(img)
    base.draw_band(d, 1.0 if CALME else ease(min(1.0, t / 0.45)))
    return img


MASTERS = {}


ASSETS = os.path.join(ROOT, "clients", "dm-optic", "content", "month1", "w3", "assets")


def build_masters():
    path = os.path.join(SITE, PHOTO)
    MASTERS["card"] = base.master_product(path, up=1.3)
    # la double barre est au centre haut de la monture : on parcourt cette zone
    MASTERS["macro"] = macro_master(path, up=1.22, fx=0.5, fy=0.5)
    # ── la page RÉELLE du catalogue (capture Chromium, 1080×10830) : c'est elle qui prouve le
    #    « toutes s'appellent par un code ». Aucune maquette, aucune reconstruction.
    cat = Image.open(os.path.join(ASSETS, "catalogue-hommes.jpg")).convert("RGB")
    MASTERS["page"] = cat.crop((0, 0, cat.width, 8150))   # 0→8 150 px : avant le raccord de capture
    # ── la fiche H08, capture pleine page : c'est là que le nom gagne s'écrira.
    fic = Image.open(os.path.join(ASSETS, "fiche-h08.jpg")).convert("RGB")
    MASTERS["fiche"] = fic.crop((0, 0, fic.width, 2200))   # 0→2 200 px : avant le raccord de capture
    # ── le visage : image générée (exception demandée par King, 27/10), cadrée plus large que le
    #    cadre pour que le mouvement ait de la matière.
    vis = Image.open(os.path.join(ASSETS, "visage-h08.jpg")).convert("RGB")
    up = 1.34
    s_ = max(W * up / vis.width, H * up / vis.height)
    vis = vis.resize((int(vis.width * s_), int(vis.height * s_)), Image.LANCZOS)
    x0 = max(0, (vis.width - int(W * up)) // 2)
    y0 = max(0, (vis.height - int(H * up)) // 2)
    MASTERS["visage"] = vis.crop((int(x0), y0, int(x0 + W * up), int(y0 + H * up)))


def page_window(big, p, y0f, y1f, zoom=0.0):
    """Défilement vertical d'une page réelle : la fenêtre 1080×1920 descend dans la capture.

    `p` est la progression du beat ; `y0f`/`y1f` les deux **fractions** de la page traversées.
    L'interpolation passe par `ease` : une page qui démarre et s'arrête en douceur, jamais un
    défilement linéaire — c'est la différence entre une capture d'écran et un plan.
    """
    # 55 % d'ease + 45 % de linéaire : une page qui ralentit en fin de plan s'arrête, et un plan qui
    # s'arrête est un plan figé (le gate 1 s l'a mesuré à 22–23 s sur la version précédente).
    e = 0.55 * ease(p) + 0.45 * p
    # le zoom réduit la fenêtre : le bas du cadre se rapproche, comme un léger travelling avant
    k = 1.0 + zoom * e
    cw, ch = int(W / k), int(H / k)
    x0 = (big.width - cw) // 2
    ay = max(0, big.height - ch)
    y0 = int(ay * (y0f + (y1f - y0f) * e))
    return big.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


def fiche_card(p, y0f, y1f, zoom=0.0):
    """La fiche H08 **dans le cadre** : une page tenue à la main, pas une capture plein écran.

    Trois raisons de la poser ainsi plutôt qu'en plein cadre : le bandeau de texte tombe alors sur
    le fond marine (jamais sur le bouton vert de la page), le titre de la fiche reste lisible du
    début à la fin du plan, et la lente poussée du carton ajoute un mouvement qui ne dépend pas du
    défilement. La page, elle, défile **dans** le carton — c'est toujours la vraie page du site.
    """
    CW, CH = 610, 1084                      # même rapport que le cadre (0,5625) : la page reste droite
    inner = page_window(MASTERS["fiche"], p, y0f, y1f, zoom)
    k = 1.0 if CALME else 1.0 + 0.070 * (0.55 * ease(p) + 0.45 * p)
    cw, ch = int(CW * k), int(CH * k)
    card = inner.resize((cw, ch), Image.LANCZOS)
    # le bas du carton se fond dans le marine : la page ne s'arrête pas sur une ligne coupée
    fade = Image.new("L", (cw, ch), 0)
    fd = ImageDraw.Draw(fade)
    for i in range(170):
        fd.rectangle((0, ch - 170 + i, cw, ch - 170 + i + 1), fill=int(255 * (i / 170) ** 1.5))
    fade = ImageChops.invert(fade)
    card = Image.composite(card, Image.new("RGB", (cw, ch), NIGHT), fade)
    canvas = Image.new("RGB", (W, H), NIGHT)
    q = 0.0 if CALME else 0.55 * ease(p) + 0.45 * p
    x, y = (W - cw) // 2 + int(16 * (0.5 - q)), 116 - int((ch - CH) / 2) - int(20 * q)
    # ombre portée douce : le carton se détache du fond sans contour dur
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle((x - 6, y + 10, x + cw + 6, y + ch + 14), radius=30, fill=90)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    canvas = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), canvas, sh)
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=26, fill=255)
    canvas.paste(card, (x, y), mask)
    return canvas


NETS = {}           # clip -> fichier nettoyé (silences de tête et de queue retirés)


def clip_path(dossier, nom):
    for ext in (".wav", ".mp3", ".m4a"):
        p = os.path.join(dossier, nom + ext)
        if os.path.exists(p):
            return p
    raise SystemExit(f"clip manquant : {nom} dans {dossier}")


def measure_clips(dossier):
    """Durée **réelle** de chaque clip, silences de tête et de queue retirés.

    On ne rogne que le silence : aucune syllabe ne disparaît, et la mesure reste honnête. C'est cette
    mesure qui décide de la durée de chaque plan — la voix ne se comprime jamais.
    """
    ffmpeg = base.imageio_ffmpeg.get_ffmpeg_exe()
    out = {}
    for beat in PLAN:
        nom = beat["clip"]
        src = clip_path(dossier, nom)
        net = os.path.join(os.path.dirname(src), nom + ".net.wav")
        # ① tête et queue rognées (aucune syllabe touchée) ;
        # ② les **respirations internes** ramenées à 0,20 s : une voix qui marque 1 s entre deux
        #    phrases fait un film de 33 s là où la même voix, au même débit, en fait 29. C'est du
        #    montage radio, pas de la compression de la voix : le débit ne change pas, les trous si.
        subprocess.run([ffmpeg, "-y", "-v", "error", "-i", src, "-af",
                        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB:detection=peak,"
                        "areverse,"
                        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB:detection=peak,"
                        "areverse,"
                        "silenceremove=start_periods=0:stop_periods=-1:stop_duration=0.42:"
                        "stop_threshold=-45dB:stop_silence=0.20:detection=peak", "-ar", "48000", "-ac", "1", net],
                       check=True)
        r = subprocess.run([ffmpeg, "-i", net], capture_output=True, text=True)
        m = __import__("re").search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
        out[nom] = round(int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)), 3)
        NETS[nom] = net
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "clients", "dm-optic", "content", "month1",
                                                 "w3", "assets", "monture-01-h08.mp4"))
    ap.add_argument("--preview", default=None, help="dossier où écrire 6 PNG de contrôle")
    ap.add_argument("--cover", default=None, help="chemin d'une couverture 1080x1920 (JPG)")
    ap.add_argument("--voice-dir", default=None,
                    help="dossier des clips b1…b5 : la voix décide du montage (durées mesurées)")
    ap.add_argument("--no-voice", action="store_true", help="rendu muet, durées de repli")
    ap.add_argument("--mouvement", action="store_true",
                    help="rétablit l'ancien film animé (zooms, panoramiques, bandeaux qui glissent)")
    args = ap.parse_args()
    global CALME
    if args.mouvement:
        CALME = False
        STILLS.clear()

    build_masters()
    durations = None
    if args.voice_dir:
        durations = measure_clips(args.voice_dir)
        total = timeline(durations)
        print("voix : " + " · ".join(f"{k} {v:.2f}s" for k, v in durations.items())
              + f"  →  film {total:.2f} s")
    else:
        # version muette : durées de repli, un carton ne tient jamais plus de 1,8 s
        # durée de repli = **les durées mesurées** de la voix de référence (voice-06, 27/10) : le
        # montage muet garde les mêmes coupes, donc le même rythme. Une image ne tient jamais plus de
        # 2,4 s, même sans voix.
        repli = {"b1": 4.80, "b2": 6.37, "b3": 3.91, "b4": 3.87, "b5": 4.23, "b6": 4.05}
        timeline(repli) if not args.no_voice else timeline(repli)

    if args.cover:
        img = crop_window(MASTERS["card"], 0.55, 0.0, 0.0, 0.0).convert("RGBA")
        d = ImageDraw.Draw(img)
        f_top = font(F_MONO, 30)
        t1 = "DM OPTIQUE · BONABÉRI"
        d.text(((W - d.textlength(t1, font=f_top)) / 2, 150), t1, font=f_top, fill=(214, 224, 240, 235))
        y = int(H * 0.655)
        for line, size, gap in (("H08, c'est", 96, 108), ("son code.", 96, 124),
                                ("Éclat ou Minuit ?", 58, 84)):
            f = font(F_TITLE, size)
            d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=(255, 255, 255, 255))
            y += gap
        half = int(W * 0.115)
        d.rectangle((W // 2 - half, y + 6, W // 2 + half, y + 13), fill=EMBER)
        f_bot = font(F_BODY, 34)
        t2 = "Opticien optométriste · WhatsApp 656 122 239"
        d.text(((W - d.textlength(t2, font=f_bot)) / 2, int(H * 0.935)), t2, font=f_bot,
               fill=(186, 198, 218, 230))
        img.convert("RGB").save(args.cover, quality=92, optimize=True)
        print("cover ->", args.cover)
        return 0

    if args.preview:
        os.makedirs(args.preview, exist_ok=True)
        pts = [round(DUR * f, 2) for f in (0.04, 0.14, 0.27, 0.42, 0.62, 0.88)]
        for t in pts:
            frame(int(t * FPS)).save(os.path.join(args.preview, "frame-%05.1fs.png" % t))
        print("preview ->", args.preview)
        return 0

    ffmpeg = base.imageio_ffmpeg.get_ffmpeg_exe()
    tmp = args.out + ".silent.mp4"
    cmd = [ffmpeg, "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "pipe:0",
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "23",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        proc.stdin.write(frame(i).tobytes())
        if i % 60 == 0:
            sys.stderr.write("\r%d/%d" % (i, n))
    proc.stdin.close()
    proc.wait()
    sys.stderr.write("\n")

    if durations is None:
        os.replace(tmp, args.out)
        print("ok ->", args.out, "(muet)")
        return 0

    # ── la bande son : les clips bout à bout, avec une respiration entre chacun ──────────────────
    audio = args.out + ".audio.wav"
    entrées, filtres, noms = [], [], []
    for i, beat in enumerate(PLAN):
        entrées += ["-i", NETS.get(beat["clip"]) or clip_path(args.voice_dir, beat["clip"])]
        filtres.append(f"[{i}:a]aresample=48000,apad=pad_dur={GAP if i < len(PLAN) - 1 else TAIL}[a{i}]")
        noms.append(f"[a{i}]")
    chaine = ";".join(filtres) + ";" + "".join(noms) + f"concat=n={len(PLAN)}:v=0:a=1[out]"
    subprocess.run([ffmpeg, "-y", "-v", "error", *entrées, "-filter_complex", chaine,
                    "-map", "[out]", "-ar", "48000", "-ac", "1", audio], check=True)
    subprocess.run([ffmpeg, "-y", "-v", "error", "-i", tmp, "-i", audio,
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
                    args.out], check=True)
    for f in (tmp, audio):
        if os.path.exists(f):
            os.remove(f)
    print("ok ->", args.out, "(parlé)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
