"""EP 01 — « Ouvrez votre nom sur Google. » · v4 · accroche à quatre mots + échelle 3 + grille 331

v1 (25/10, 20:25) : 5 plans, ouverture sur un carton de titre, une seule montée (le CTA final).
C'était **l'arc classique** que `knowledge/STORY-ARC-2026-10-25.md` rejette (slide 2).
v2 applique la doctrine : départ à 70, secousse entre 5 et 10 s, **trois cimes**, relâchements,
CTA en dernière cime — et une **voix** posée sur le master.
v3 (25/10, 21:55) applique la formule de confiance du jeu 5 (`knowledge/CONTENT-GAMES-2026-10-25.md`) :
le souffle muet de `release2` devient **le conseil gratuit** — le spectateur repart avec ce qu'il
peut faire sans nous, et avec ce qui reste à construire. Utilité 3 → 4, porte recevable, autorité
toujours irrecevable (23 s ne peut pas valoir 40/125).

v4 (**25/10, 23:30**) applique les trois sources du soir (`knowledge/HOOKS-2026-10-25.md`) :
① l'accroche passe aux **quatre mots obligatoires** — *sujet* (« votre »), *action* (« Tapez »),
*objectif* (« il appelle »), *contraste* (« pas vous ») : la v3 n'avait ni action ni
objectif, un spectateur ne pouvait rien y faire ; ② l'échelle est déclarée **niveau 3
(Fortuneteller)** — annoncer ce qui va se passer — parce qu'un niveau 4 (le plan dans l'ordre) est
un mensonge dans 24 s ; ③ la pièce prend sa case dans la **grille 331** : *fiche Google × scénario*,
case 3 sur 9 (`content/ideas/GRID-331-2026-10-25.md`).

    python3 content/reels/ep01/make_ep01.py            # rendu + voix si voice/timing.json existe
    python3 tools/qa/audit_reel.py content/reels/ep01/make_ep01.py   # la porte, avant le rendu

Faits montrés : capture de la fiche Optix du **24/10** (`sales/PACK-OPTICIEN-2026-10.md`,
tableau « Ce qu'un patient voit ») — « Add business hours », « Add website », « Be the first to review ».
Aucun chiffre de résultat, aucun nom de client, aucune promesse de mesure (ruling 142).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "tools", "qa"))

from reelkit import (  # noqa: E402
    H,
    PALETTE as P,
    W,
    Kit,
    Mascot,
    draw_text,
    ease,
    find_ffmpeg,
    font,
    draw_check,
    pill,
    rounded_card,
    text_width,
)

MARGIN = 90
MASCOT = os.path.join(HERE, "assets", "mascot.png")
TIMING = os.path.join(HERE, "voice", "timing.json")

# Le plan par défaut, si la voix n'a pas encore été générée (v2 pré-voix).
DEFAULT = [
    ("hook", 5.5, 70, "contexte", None),
    ("spike1", 5.4, 92, "contraste", "capture Optix 24/10"),
    ("release1", 2.3, 58, "relache", None),
    ("spike2", 5.0, 88, "contraste", "capture Optix 24/10"),
    ("release2", 2.4, 60, "relache", None),
    ("cta", 3.6, 95, "appel", None),
]


def load_plan():
    """Lit les durées mesurées sur la voix ; retombe sur le plan par défaut."""
    if os.path.exists(TIMING):
        data = json.load(open(TIMING, encoding="utf-8"))
        plan = []
        for beat in data["beats"]:
            base = next(b for b in DEFAULT if b[0] == beat["name"])
            plan.append((beat["name"], float(beat["duration"]), base[2], base[3], base[4]))
        return plan
    return DEFAULT


PLAN = load_plan()

# ── la forme déclarée à la porte (`tools/qa/audit_reel.py`) ─────────────────────
BEAT_FACTS = {
    "hook": None,
    "spike1": "Add business hours · Add website · Be the first to review",
    "spike2": "neuf fiches, zéro site",
}


def build_beats():
    from audit_reel import Beat

    beats, t = [], 0.0
    for name, dur, peak, kind, source in PLAN:
        beats.append(
            Beat(
                name=name,
                start=round(t, 3),
                end=round(t + dur, 3),
                peak=peak,
                kind=kind,
                fact=BEAT_FACTS.get(name),
                source=source,
            )
        )
        t += dur
    return beats


BEATS = build_beats()
DURATION = round(sum(p[1] for p in PLAN), 3)

# ── le jeu auquel la pièce appartient (`knowledge/CONTENT-GAMES-2026-10-25.md`, §8) ─────────
# EP01 est une **porte** : courte par construction, elle fait entrer, elle ne construit pas la
# confiance. Déclarée « autorité », la même pièce échoue (`trop-court`) — c'est la leçon du 25/10.
from audit_hook import Hook  # noqa: E402
from audit_trust import Piece  # noqa: E402

# ── l'accroche, telle que la porte la lit (`knowledge/HOOKS-2026-10-25.md`) ───────────────────
# Les quatre mots obligatoires, un par clause. Le contraste est **le dernier**, il ferme l'accroche :
# « pas celui qui n'en a pas ». Aucun chiffre de résultat, aucune promesse, aucune urgence.
HOOK = Hook(
    text=(
        "Tapez votre nom sur Google : "
        "il appelle ceux qui ont un site, pas vous."
    ),
    level=3,   # Fortuneteller : on annonce ce que fait le patient. Niveau 4 = le plan, plus tard.
)

TRUST = Piece(
    name="EP01",
    game=5,
    role="porte",
    minutes=DURATION / 60,
    relevance=5,
    usefulness=4,      # v3 : le spectateur repart avec ce qu'il peut faire gratuitement, et ce qui reste
    on_target="opticien ou clinique de Douala, fiche Google existante, pas de site",
    next_step="écrire APERÇU sur WhatsApp (wa.me/237677789631)",
    goal="conversations",
)


# ───────────────────────────────────────────────────────────── primitives ────


def label(d, text, xy=(MARGIN, 190)):
    d.text(xy, text, font=font("Montserrat-SemiBold.ttf", 30), fill=P["ink_soft"], anchor="la")


def punch(img, t, at, strength=0.16, span=0.45):
    """La secousse : un voile sombre qui tombe et repart en 0,45 s. Marque la cime."""
    if t < at - 0.02 or t > at + span:
        return
    k = (t - at) / span
    alpha = int(255 * strength * (1 - k) ** 1.5)
    if alpha > 0:
        img.paste((14, 10, 8), (0, 0, W, H), None) if False else None
        overlay = img.copy()
        from PIL import ImageDraw

        d = ImageDraw.Draw(overlay, "RGBA")
        d.rectangle((0, 0, W, H), fill=(16, 11, 8, alpha))
        img.paste(overlay, (0, 0))


def search_bar(d, y, query, y2=None):
    """Le champ de recherche — l'histoire commence dans l'écran du spectateur."""
    rounded_card(d._image if hasattr(d, "_image") else None, (MARGIN, y, W - MARGIN, y + 108), P["white"], radius=54) if False else None
    d.rounded_rectangle((MARGIN, y, W - MARGIN, y + 108), radius=54, fill=P["white"],
                        outline=(214, 200, 184), width=3)
    d.ellipse((MARGIN + 40, y + 38, MARGIN + 68, y + 66), outline=P["ink_soft"], width=4)
    d.line((MARGIN + 62, y + 62, MARGIN + 78, y + 78), fill=P["ink_soft"], width=4)
    d.text((MARGIN + 104, y + 54), query, font=font("Montserrat-Medium.ttf", 44),
           fill=P["ink"], anchor="lm")


# ─────────────────────────────────────────────────── beat 1 · contexte (70) ──


def s_hook(kit, img, d, t, dur):
    """Deux résultats, un seul a un site : le contraste de l'accroche est **montré**.

    v3 ouvrait sur un seul résultat (« Aucun site · pas d'horaires ») et un constat. Ici le spectateur
    voit la comparaison que l'accroche nomme — celui qu'on appelle, celui qu'on saute — donc la vidéo
    ne décrit plus un problème, elle montre un choix.
    """
    label(d, "GOOGLE · DOUALA")
    search_bar(d, 250, "opticien akwa")

    resultats = [
        ("Optique Akwa", "un site · 6 photos · 12 avis", True),
        ("Optique …", "aucun site · pas d'horaires", False),
    ]
    for i, (nom, detail, bon) in enumerate(resultats):
        a = ease((t - 0.35 - i * 0.22) / 0.5)
        if a <= 0:
            continue
        y = 400 + i * 172 + int((1 - a) * 22)
        rounded_card(img, (MARGIN, y, W - MARGIN, y + 148), P["cream_light"], radius=16, shadow=6)
        d.text((MARGIN + 40, y + 32), nom, font=font("Montserrat-Bold.ttf", 44), fill=P["ink"])
        d.text((MARGIN + 40, y + 92), detail, font=font("Montserrat-Medium.ttf", 30),
               fill=P["green"] if bon else P["orange"])
        cx, cy = W - MARGIN - 70, y + 74
        if bon:
            draw_check(d, (cx - 26, cy), 52, P["green"], width=9)
        else:   # la croix se dessine : `✗` n'existe pas plus que `✓` dans Montserrat
            d.line([(cx - 26, cy - 26), (cx + 26, cy + 26)], fill=P["orange"], width=9)
            d.line([(cx + 26, cy - 26), (cx - 26, cy + 26)], fill=P["orange"], width=9)

    fnt = font("Montserrat-ExtraBold.ttf", 92)
    lignes = [
        ("Tapez votre nom", P["ink"]),
        ("sur Google.", P["ink"]),
        ("Il appelle ceux", P["ink"]),
        ("qui ont un site.", P["orange"]),
    ]
    for i, (ligne, couleur) in enumerate(lignes):
        a = ease((t - 0.7 - i * 0.16) / 0.5)
        if a <= 0:
            continue
        draw_text(d, (MARGIN, 764 + i * 104 + int((1 - a) * 22)), ligne, fnt, couleur)

    if t > 2.2:
        draw_text(d, (MARGIN, 1210), "Pas vous.", font("Montserrat-Bold.ttf", 56),
                  P["ink_soft"] if a > 0.5 else P["ink_soft"])
    kit.mascot.draw(img, 30, 1270, t, height=600)


# ─────────────────────────────────────────────────── beat 2 · secousse (92) ──


CARDS = [("HORAIRES", "Add business hours"), ("SITE WEB", "Add website"), ("AVIS", "Pas encore d'avis")]


def s_spike1(kit, img, d, t, dur):
    punch(img, t, 0.0)
    label(d, "LA FICHE DU CABINET")
    draw_text(d, (MARGIN, 250), "Google demande\ntrois choses.", font("Montserrat-ExtraBold.ttf", 78),
              P["ink"], spacing=8)
    for i, (name, prompt) in enumerate(CARDS):
        appear = ease((t - 0.2 - i * 0.2) / 0.4)
        if appear <= 0:
            continue
        y = 600 + i * 214 + int((1 - appear) * 26)
        fill = [P["orange_soft"], P["blue_soft"], P["green_soft"]][i]
        rounded_card(img, (MARGIN, y, W - MARGIN, y + 180), fill, radius=14, pin=P["orange"])
        d.text((MARGIN + 44, y + 44), name, font=font("Montserrat-SemiBold.ttf", 30), fill=P["ink_soft"])
        d.text((MARGIN + 44, y + 88), prompt, font=font("Montserrat-Bold.ttf", 54), fill=P["ink"])
    kit.mascot.draw(img, -10, 1270, t, talking=1.0, height=560)
    if t > 0.9:
        pill(img, (700, 1380), [("trois ", P["white"]), ("choses", P["orange"])], size=50)


# ─────────────────────────────────────────────────── beat 3 · relâche (58) ──


def s_release1(kit, img, d, t, dur):
    draw_text(d, (MARGIN, 520), "Vous en avez", font("Montserrat-ExtraBold.ttf", 92), P["ink"])
    a = ease((t - 0.4) / 0.6)
    word = "une."
    fnt = font("Montserrat-ExtraBold.ttf", 150)
    draw_text(d, (MARGIN, 640), word, fnt, P["orange"] if a > 0.35 else P["sand"])
    if a > 0.5:
        draw_text(d, (MARGIN, 900), "Jamais les trois.", font("Montserrat-Medium.ttf", 48), P["ink_soft"])
    kit.mascot.draw(img, 20, 1080, t, height=740)


# ─────────────────────────────────────────────────── beat 4 · secousse (88) ──


def s_spike2(kit, img, d, t, dur):
    punch(img, t, 0.0, strength=0.14)
    label(d, "CE QUE FAIT UN SITE")
    draw_text(d, (MARGIN, 250), "Un site ne sert pas", font("Montserrat-ExtraBold.ttf", 66), P["ink"])
    fnt = font("Montserrat-ExtraBold.ttf", 66)
    draw_text(d, (MARGIN, 336), "à « avoir un site ».", fnt, P["orange"])
    # le trait sous la phrase qu'on retire (pas de rature sur les glyphes : illisible)
    d.rectangle((MARGIN + 4, 336 + 72, MARGIN + text_width(fnt, "à « avoir un site »."), 336 + 80),
                fill=P["orange"])

    if t > 0.5:
        a = ease((t - 0.5) / 0.5)
        y = 520 + int((1 - a) * 30)
        rounded_card(img, (MARGIN, y, W - MARGIN, y + 350), P["green_soft"], radius=18, pin=P["green"])
        d.text((MARGIN + 48, y + 46), "IL RÉPOND AVANT L'APPEL", font=font("Montserrat-SemiBold.ttf", 28),
               fill=P["ink_soft"])
        for i, line in enumerate(["Horaires", "Adresse", "WhatsApp"]):
            draw_text(d, (MARGIN + 48, y + 104 + i * 88), line, font("Montserrat-Bold.ttf", 58), P["ink"])
        draw_check(d, (W - MARGIN - 90, y + 210), 92, P["green"], width=14)
    kit.mascot.draw(img, 0, 1270, t, talking=1.0, height=560)


# ─────────────────────────────────────────────────── beat 5 · relâche (60) ──


def s_release2(kit, img, d, t, dur):
    """Le conseil gratuit — la pièce doit laisser quelque chose d'appliquable (utilité, jeu 5).

    Ce qui est vrai, et que la pièce peut donc montrer : les horaires se publient en dix minutes,
    la fiche se réclame, l'avis ne se fabrique pas — il vient d'un patient. Le site, lui, se
    construit : c'est le seul des trois qui soit notre travail.
    """
    label(d, "CE QUI EST DÉJÀ GRATUIT")
    draw_text(d, (MARGIN, 250), "Deux se font", font("Montserrat-ExtraBold.ttf", 72), P["ink"])
    draw_text(d, (MARGIN, 330), "sans personne.", font("Montserrat-ExtraBold.ttf", 72), P["orange"])

    rows = [
        ("Horaires", "10 minutes, vous-même", True),
        ("Votre fiche", "à réclamer", True),
        ("L'avis", "un patient l'écrit", False),
    ]
    for i, (titre, detail, coche) in enumerate(rows):
        a = ease((t - 0.15 - i * 0.15) / 0.35)
        if a <= 0:
            continue
        y = 520 + i * 150 + int((1 - a) * 18)
        d.rounded_rectangle((MARGIN, y, W - MARGIN, y + 122), radius=12, fill=P["cream_light"])
        d.text((MARGIN + 36, y + 30), titre, font=font("Montserrat-Bold.ttf", 44), fill=P["ink"])
        d.text((MARGIN + 36, y + 80), detail, font=font("Montserrat-Medium.ttf", 28), fill=P["ink_soft"])
        if coche:
            draw_check(d, (W - MARGIN - 70, y + 61), 52, P["green"], width=10)
        else:
            d.line([(W - MARGIN - 96, y + 61), (W - MARGIN - 44, y + 61)], fill=P["orange"], width=8)

    draw_text(d, (MARGIN, 1020), "Le site, c'est le seul qui se construise.",
              font("Montserrat-SemiBold.ttf", 40), P["ink_soft"])
    kit.mascot.draw(img, 40, 1120, t, talking=1.0, height=620)


# ────────────────────────────────────────────────────── beat 6 · CTA (95) ──


def s_cta(kit, img, d, t, dur):
    punch(img, t, 0.0, strength=0.12, span=0.35)
    label(d, "LE MOT SUFFIT", (MARGIN, 240))
    draw_text(d, (MARGIN, 320), "Écrivez", font("Montserrat-ExtraBold.ttf", 88), P["ink"])
    fnt = font("Montserrat-ExtraBold.ttf", 156)
    draw_text(d, (MARGIN, 420), "APERÇU", fnt, P["orange"])
    d.rectangle((MARGIN, 660, MARGIN + text_width(fnt, "APERÇU"), 674), fill=P["orange"])
    draw_text(d, (MARGIN, 730), "sur WhatsApp", font("Montserrat-SemiBold.ttf", 52), P["ink"])
    draw_text(d, (MARGIN, 810), "677 78 96 31", font("Montserrat-Bold.ttf", 58), P["ink_soft"])
    if t > 0.5:
        pill(img, (W // 2, 960), [("10 minutes", P["white"]), (" cette semaine", P["orange"])],
             size=48, pad=(40, 26))
        draw_text(d, (MARGIN, 1040), "Réponse le jour même.", font("Montserrat-Medium.ttf", 36), P["ink_soft"])
    kit.mascot.draw(img, 40, 1140, t, talking=1.0, height=620)


SCENES = {
    "hook": s_hook,
    "spike1": s_spike1,
    "release1": s_release1,
    "spike2": s_spike2,
    "release2": s_release2,
    "cta": s_cta,
}


def build() -> Kit:
    """Chaque scène reçoit sa durée : la voix décide du temps, pas l'inverse."""
    kit = Kit(mascot=Mascot(MASCOT, height=620))
    for name, dur, _, _, _ in PLAN:
        fn = SCENES[name]
        kit.scene(dur, lambda k, i, d, t, _fn=fn, _dur=dur: _fn(k, i, d, t, _dur))
    return kit


# ─────────────────────────────────────────────────────────────── audio ───────


def mux(video: str, out: str) -> str:
    """Pose la voix sur le master : chaque clip démarre à son beat, le reste est du silence."""
    ffmpeg = find_ffmpeg()
    timing = json.load(open(TIMING, encoding="utf-8"))
    starts, t = [], 0.0
    for name, dur, *_ in PLAN:
        starts.append(t)
        t += dur
    clips = [b for b in timing["beats"] if b.get("file")]
    if not clips:
        raise SystemExit("aucun clip de voix : lancer d'abord la génération (voir README §7)")

    args = [ffmpeg, "-y", "-loglevel", "error", "-i", video]
    for b in clips:
        args += ["-i", os.path.join(HERE, "voice", b["file"])]
    filters, labels = [], []
    for i, b in enumerate(clips):
        idx = next(j for j, (n, *_rest) in enumerate(PLAN) if n == b["name"])
        delay = int(starts[idx] * 1000)
        filters.append(f"[{i + 1}:a]adelay={delay}|{delay},volume=1.0[a{i}]")
        labels.append(f"[a{i}]")
    filters.append(
        f"{''.join(labels)}amix=inputs={len(clips)}:normalize=0:dropout_transition=0,"
        f"apad,atrim=0:{DURATION},afade=t=out:st={DURATION - 0.4}:d=0.4[aout]"
    )
    args += [
        "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out,
    ]
    subprocess.run(args, check=True)
    return out


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ep01-v4.mp4")
    with_voice = "--sans-voix" not in sys.argv
    kit = build()
    silent = os.path.join(HERE, "ep01-v4-silent.mp4")
    kit.render(silent)
    print(f"✅ image : {silent} · {DURATION:.1f} s")
    if with_voice and os.path.exists(TIMING):
        mux(silent, out)
        print(f"✅ master : {out} · {DURATION:.1f} s · voix posée")
    else:
        os.replace(silent, out)
        print(f"⚠️  master sans voix (timing absent) : {out}")
