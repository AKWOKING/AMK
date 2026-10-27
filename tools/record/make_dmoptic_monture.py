#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM Optique — « La monture cherche son nom », épisode 1 (H08) — moteur de rendu.

1080×1920 · 30 fps · **deux rendus** : muet (14,20 s) et parlé (19,87 s) · **sans visage, sans tournage,
sans le médecin**.

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

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_dmoptic_tiktok as base  # noqa: E402  (mêmes masters, mêmes polices, même mouvement)

ROOT = base.ROOT
SITE = base.SITE
W, H, FPS = base.W, base.H, base.FPS
DUR = 14.2          # valeur de repli (version muette) ; la version parlée calcule la sienne

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
    # b1 · 3,93 s — LE CONSTAT, ET LE SPECTATEUR COMME SUJET (King, 27/10 : « elle n'est pas à lui »).
    # Trois plans, coupe à 0,94 s : la première seconde ne reste jamais sur une image.
    dict(clip="b1",
         shots=[(0.24, "card", 0.30, 0.90, 0.40), (0.60, "card", 0.26, -0.90, -0.40),
                (1.00, "macro", 0.28, 0.65, -0.45)],
         subs=[(0.00, 0.50, ["ELLE N'A PAS", "DE NOM"], 100, 0.695),
               (0.50, 1.00, ["VOUS CHOISISSEZ"], 88, 0.700)]),
    # b2 · 4,76 s — LA PREUVE, prononcée : « quarante ».
    dict(clip="b2",
         shots=[(0.48, "card", 0.26, -0.60, 0.40), (1.00, "macro", 0.28, 0.60, -0.50)],
         subs=[(0.00, 0.50, ["40 MONTURES"], 110, 0.700),
               (0.50, 1.00, ["40 CODES"], 110, 0.700)]),
    # b3 · 5,88 s — LE CODE, PUIS LES DEUX NOMS. Trois plans pour un beat long.
    dict(clip="b3",
         shots=[(0.32, "card", 0.28, 0.70, -0.45), (0.64, "macro", 0.26, -0.65, 0.50),
                (1.00, "card", 0.24, 0.60, -0.40)],
         # les deux noms restent à l'écran **ensemble** : un vote où l'on ne voit qu'une option
         # à la fois n'est pas un vote, c'est une devinette.
         subs=[(0.00, 0.34, ["H08"], 124, 0.700),
               (0.34, 1.00, ["A · ÉCLAT", "B · MINUIT"], 88, 0.680)]),
    # b4 · 3,85 s — LE REHOOK : ce n'est plus un objet, c'est un visage.
    dict(clip="b4",
         shots=[(0.50, "macro", 0.28, -0.60, 0.50), (1.00, "card", 0.26, 0.60, -0.45)],
         subs=[(0.00, 0.55, ["SUR UN VISAGE", "TOUS LES JOURS"], 86, 0.700),
               (0.55, 1.00, ["ELLE MÉRITE", "MIEUX"], 104, 0.700)]),
    # b5 · 3,39 s — L'ENJEU QUI RESTE.
    dict(clip="b5",
         shots=[(0.55, "card", 0.28, 0.55, -0.40), (1.00, "macro", 0.30, -0.60, 0.50)],
         subs=[(0.00, 1.00, ["LE NOM RESTE", "SUR SA PAGE"], 94, 0.700)]),
    # b6 · 2,89 s + queue — LA SORTIE : A, B, ou un mot. Puis le carton.
    dict(clip="b6",
         shots=[(0.42, "card", 0.30, 0.60, -0.45), (1.00, "end", 0.30, 0.0, 0.55)],
         subs=[(0.00, 0.42, ["A, B", "OU VOTRE MOT"], 100, 0.700)]),
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
    d.text(((CW - d.textlength("MARDI, DANS LA VIDÉO SUIVANTE", font=f1)) / 2, y), "MARDI, DANS LA VIDÉO SUIVANTE",
           font=f1, fill=PAPER + (int(235 * a),))
    f2 = font(F_TITLE, int(84 * K))
    t2 = "LE NOM QUI GAGNE"
    d.text(((CW - d.textlength(t2, font=f2)) / 2, y + int(60 * K)), t2,
           font=f2, fill=(255, 255, 255, int(255 * a)))
    f3 = font(F_BODY, int(40 * K))
    t3 = "écrit sur sa page, sur notre site"
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
        prog = ease((t - s0) / 0.42)
        out = 1.0 if t < s1 - 0.22 else max(0.0, (s1 - t) / 0.22)  # sortie douce en fondu
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        off = int(20 * (1 - prog))
        alpha = int(255 * prog * out)
        lh = int(size * 1.1)
        top = int(H * anchor) + off
        # bandeau derrière le texte : lisible sur la carte crème comme sur le carton marine
        block_h = lh * len(lines)
        pad = int(size * 0.40)
        d.rectangle((0, top - pad, W, top + block_h + int(pad * 0.35)),
                    fill=NIGHT + (int(236 * prog * out),))
        for i, line in enumerate(lines):
            # chaque ligne arrive avec 0,22 s de retard sur la précédente : deux mouvements au lieu d'un
            decal = min(1.0, max(0.0, (t - s0 - 0.22 * i) / 0.42))
            a_ligne = int(alpha * ease(decal))
            if a_ligne <= 2:
                continue
            y_ligne = top + i * lh + int(12 * (1 - ease(decal)))
            f = font(F_TITLE, size)
            tw = d.textlength(line, font=f)
            d.text(((W - tw) / 2, y_ligne), line, font=f, fill=(255, 255, 255, a_ligne))
        half = int(W * 0.12 * prog)
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


def frame(i):
    t = i / FPS
    for (b0, b1, kind, zoom, pan, drift) in BEATS:
        if b0 <= t < b1:
            p = (t - b0) / (b1 - b0)
            if kind == "end":
                big = end_card(t, b0, DUR)
            else:
                big = MASTERS[kind]
            img = crop_window(big, p, zoom, pan, drift)
            break
    else:
        img = Image.new("RGB", (W, H), NIGHT)

    if t < 0.45:
        k = 1.10 - 0.10 * ease(t / 0.45)
        w2, h2 = int(W * k), int(H * k)
        img = img.resize((w2, h2), Image.LANCZOS)
        img = img.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))

    img = draw_subs(img, t)
    d = ImageDraw.Draw(img)
    base.draw_band(d, ease(min(1.0, t / 0.45)))
    return img


MASTERS = {}


def build_masters():
    path = os.path.join(SITE, PHOTO)
    MASTERS["card"] = base.master_product(path, up=1.3)
    # la double barre est au centre haut de la monture : on parcourt cette zone
    MASTERS["macro"] = macro_master(path, up=1.22, fx=0.5, fy=0.5)


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
        subprocess.run([ffmpeg, "-y", "-v", "error", "-i", src, "-af",
                        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB:detection=peak,"
                        "areverse,"
                        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB:detection=peak,"
                        "areverse", "-ar", "48000", "-ac", "1", net], check=True)
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
    args = ap.parse_args()

    build_masters()
    durations = None
    if args.voice_dir:
        durations = measure_clips(args.voice_dir)
        total = timeline(durations)
        print("voix : " + " · ".join(f"{k} {v:.2f}s" for k, v in durations.items())
              + f"  →  film {total:.2f} s")
    else:
        # version muette : durées de repli, un carton ne tient jamais plus de 1,8 s
        repli = {"b1": 3.9, "b2": 4.8, "b3": 5.9, "b4": 3.9, "b5": 3.4, "b6": 2.9}
        timeline(repli) if not args.no_voice else timeline(repli)

    if args.cover:
        img = crop_window(MASTERS["card"], 0.55, 0.0, 0.0, 0.0).convert("RGBA")
        d = ImageDraw.Draw(img)
        f_top = font(F_MONO, 30)
        t1 = "DM OPTIQUE · BONABÉRI"
        d.text(((W - d.textlength(t1, font=f_top)) / 2, 150), t1, font=f_top, fill=(214, 224, 240, 235))
        y = int(H * 0.655)
        for line, size, gap in (("Elle n'a pas", 104, 118), ("de nom.", 104, 132),
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
