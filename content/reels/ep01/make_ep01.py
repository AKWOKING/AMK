"""EP 01 — « Votre nom existe. Votre site, non. » · 21 s · 1080×1920

Sujet : carte de contenu du playbook §2, **T2** (TOFU, vidéo 25 s) — « pourquoi votre site
n'apparaît pas quand on cherche votre nom ». Rendu en 5 plans, sans voix, texte incrusté
(sous-titres écrits à la main — ruling King 11/10, jamais d'auto).

Sources des faits montrés à l'écran :
  · « Add business hours » / « Add website » = ce que Google réclame sur la fiche d'Optix,
    capture du 24/10 (sales/PACK-OPTICIEN-2026-10.md, tableau « Ce qu'un patient voit »).
  · « Pas encore d'avis » = « Be the first to review », même capture.
  · Aucun chiffre de résultat, aucun nom de client, aucune promesse de mesure.

    python3 content/reels/ep01/make_ep01.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from reelkit import (  # noqa: E402
    H,
    PALETTE as P,
    Kit,
    Mascot,
    draw_text,
    ease,
    font,
    pill,
    rounded_card,
    text_width,
    W,
)

MARGIN = 90
OUT_DIR = HERE
MASCOT = os.path.join(HERE, "assets", "mascot.png")


def label(d, text, xy=(MARGIN, 200)):
    fnt = font("Montserrat-SemiBold.ttf", 30)
    d.text(xy, text, font=fnt, fill=P["ink_soft"], anchor="la")


def headline(d, lines, y=300, size=120, accent_last=True):
    """Grand titre ; la dernière ligne est en orange (l'accent de la référence)."""
    fnt = font("Montserrat-ExtraBold.ttf", size)
    line_h = int(size * 1.12)
    for i, line in enumerate(lines):
        color = P["orange"] if (accent_last and i == len(lines) - 1) else P["ink"]
        draw_text(d, (MARGIN, y + i * line_h), line, fnt, color)
    return y + len(lines) * line_h


# ────────────────────────────────────────────────────────────── 1 · accroche ──


def s1_hook(kit, img, d, t):
    label(d, "AMK · 01 — OPTICIEN", (MARGIN, 190))
    a = ease(t / 0.6)
    # le titre monte de 30 px à l'apparition
    dy = int((1 - a) * 30)
    fnt_big = font("Montserrat-ExtraBold.ttf", 122)
    lines = [("Votre nom", P["ink"]), ("existe.", P["ink"]),
             ("Votre site,", P["ink"]), ("non.", P["orange"])]
    for i, (line, color) in enumerate(lines):
        draw_text(d, (MARGIN, 330 + i * 138 + dy), line, fnt_big, color)
    if t > 0.8:
        a2 = ease((t - 0.8) / 0.5)
        uy = 330 + 3 * 138 + 128
        d.rectangle((MARGIN + 6, uy, MARGIN + 6 + int(210 * a2), uy + 9), fill=P["orange"])
    kit.mascot.draw(img, 30, 1080, t, height=760)
    if t > 1.4:
        pill(img, (720, 1030), [("cherchez ", P["white"]), ("vous-même", P["orange"])], size=52)


# ──────────────────────────────────────────────── 2 · ce que Google réclame ──


CARDS = [
    ("HORAIRES", "Add business hours"),
    ("SITE WEB", "Add website"),
    ("AVIS", "Pas encore d'avis"),
]


def s2_missing(kit, img, d, t):
    label(d, "LA FICHE DU CABINET", (MARGIN, 190))
    fnt_h = font("Montserrat-ExtraBold.ttf", 84)
    draw_text(d, (MARGIN, 250), "Ce que Google\nréclame :", fnt_h, P["ink"], spacing=10)

    for i, (name, prompt) in enumerate(CARDS):
        appear = ease((t - 0.35 - i * 0.25) / 0.45)
        if appear <= 0:
            continue
        y = 620 + i * 222 + int((1 - appear) * 26)
        x0, x1 = MARGIN, W - MARGIN
        fill = [P["orange_soft"], P["blue_soft"], P["green_soft"]][i]
        rounded_card(img, (x0, y, x1, y + 186), fill, radius=14, pin=P["orange"])
        d.text((x0 + 44, y + 46), name, font=font("Montserrat-SemiBold.ttf", 30), fill=P["ink_soft"])
        d.text((x0 + 44, y + 92), prompt, font=font("Montserrat-Bold.ttf", 56), fill=P["ink"])
        d.text((x1 - 48, y + 140), "—", font=font("Montserrat-ExtraBold.ttf", 80),
               fill=P["orange"], anchor="ra")

    kit.mascot.draw(img, -10, 1250, t, talking=1.0 if t > 1.2 else 0.0, height=560)
    if t > 1.6:
        pill(img, (700, 1360), [("les trois ", P["white"]), ("manquent", P["orange"])], size=50)


# ─────────────────────────────────────────────── 3 · le mur des fiches ──


WALL = [
    "Horaires", "Photos", "Avis", "Adresse",
    "Services", "Langue", "Téléphone", "Itinéraire",
    "Catalogue", "Tarifs", "Équipe", "Rendez-vous",
]


def s3_wall(kit, img, d, t):
    fnt_h = font("Montserrat-ExtraBold.ttf", 78)
    draw_text(d, (MARGIN, 200), "Tout le monde\na une fiche.", fnt_h, P["ink"], spacing=8)
    draw_text(d, (MARGIN, 400), "Cherchez le site.", font("Montserrat-SemiBold.ttf", 46),
              P["ink_soft"])

    cols, rows = 3, 3
    cw, ch = 286, 196
    gap_x, gap_y = 24, 26
    grid_w = cols * cw + (cols - 1) * gap_x
    x0 = (W - grid_w) // 2
    y0 = 540
    tones = [P["cream_light"], P["orange_soft"], P["green_soft"], P["blue_soft"]]
    for idx in range(cols * rows):
        appear = ease((t - 0.15 - idx * 0.07) / 0.34)
        if appear <= 0:
            continue
        r, c = divmod(idx, cols)
        x = x0 + c * (cw + gap_x)
        y = y0 + r * (ch + gap_y) + int((1 - appear) * 18)
        tone = tones[(idx + r) % len(tones)]
        rounded_card(img, (x, y, x + cw, y + ch), tone, radius=8, shadow=5, pin=P["orange"])
        d.text((x + 26, y + 34), "FICHE", font=font("Montserrat-SemiBold.ttf", 22), fill=P["ink_soft"])
        d.text((x + 26, y + 74), WALL[idx], font=font("Montserrat-Bold.ttf", 38), fill=P["ink"])
        d.text((x + cw - 26, y + ch - 30), "0 site", font=font("Montserrat-Bold.ttf", 30),
               fill=P["ink_soft"], anchor="ra")

    kit.mascot.draw(img, 0, 1240, t, talking=1.0, height=580)
    if t > 1.3:
        pill(img, (690, 1340), [("partout ", P["white"]), ("pareil", P["orange"])], size=48)


# ──────────────────────────────────────────────── 4 · ce qui règle les trois ──


def s4_site(kit, img, d, t):
    a = ease(t / 0.55)
    draw_text(d, (MARGIN, 230 + int((1 - a) * 24)), "Ce qui règle\nles trois :",
              font("Montserrat-ExtraBold.ttf", 84), P["ink"], spacing=10)

    appear = ease((t - 0.5) / 0.6)
    if appear > 0:
        y = 690 + int((1 - appear) * 40)
        box = (MARGIN, y, W - MARGIN, y + 520)
        rounded_card(img, box, P["green_soft"], radius=18, pin=P["green"])
        d.text((MARGIN + 48, y + 54), "VOTRE SITE", font=font("Montserrat-SemiBold.ttf", 30),
               fill=P["ink_soft"])
        fnt = font("Montserrat-Bold.ttf", 62)
        for i, line in enumerate(["Horaires", "Adresse", "WhatsApp"]):
            draw_text(d, (MARGIN + 48, y + 120 + i * 96), line, fnt, P["ink"])
        d.text((W - MARGIN - 60, y + 300), "✓", font=font("Montserrat-ExtraBold.ttf", 150),
               fill=P["green"], anchor="mm")
        d.text((MARGIN + 48, y + 440), "visible quand on cherche le cabinet",
               font=font("Montserrat-Medium.ttf", 34), fill=P["ink_soft"])

    kit.mascot.draw(img, 10, 1190, t, talking=1.0 if t > 1.0 else 0.0, height=600)
    if t > 1.1:
        pill(img, (690, 1300), [("un site ", P["white"]), ("à votre nom", P["orange"])], size=46)


# ─────────────────────────────────────────────────────────────────── 5 · CTA ──


def s5_cta(kit, img, d, t):
    label(d, "LE MOT SUFFIT", (MARGIN, 250))
    a = ease(t / 0.55)
    dy = int((1 - a) * 26)
    draw_text(d, (MARGIN, 330 + dy), "Écrivez", font("Montserrat-ExtraBold.ttf", 96), P["ink"])
    fnt = font("Montserrat-ExtraBold.ttf", 172)
    draw_text(d, (MARGIN, 440 + dy), "APERÇU", fnt, P["orange"])
    d.rectangle((MARGIN, 700 + dy, MARGIN + text_width(fnt, "APERÇU"), 716 + dy), fill=P["orange"])
    draw_text(d, (MARGIN, 780 + dy), "sur WhatsApp", font("Montserrat-SemiBold.ttf", 56), P["ink"])
    draw_text(d, (MARGIN, 870 + dy), "677 78 96 31", font("Montserrat-Bold.ttf", 62), P["ink_soft"])

    if t > 0.9:
        b = ease((t - 0.9) / 0.5)
        pill(img, (W // 2, 1050), [("10 minutes", P["white"]), (" cette semaine", P["orange"])],
             size=52, pad=(44, 30))
        if b > 0.99:
            draw_text(d, (MARGIN, 1150), "Réponse le jour même.", font("Montserrat-Medium.ttf", 38),
                      P["ink_soft"])

    kit.mascot.draw(img, 40, 1240, t, talking=1.0 if t > 1.0 else 0.0, height=600)


def build(out: str = os.path.join(OUT_DIR, "ep01-v1.mp4")) -> Kit:
    kit = Kit(mascot=Mascot(MASCOT, height=620))
    kit.scene(4.0, s1_hook)
    kit.scene(5.0, s2_missing)
    kit.scene(4.2, s3_wall)
    kit.scene(4.2, s4_site)
    kit.scene(4.0, s5_cta)
    return kit


if __name__ == "__main__":
    kit = build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT_DIR, "ep01-v1.mp4"))
    path = kit.render(sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT_DIR, "ep01-v1.mp4"))
    print(f"✅ {path} · {kit.total():.1f} s · {W}×{H} · 30 fps")
