#!/usr/bin/env python3
"""AMK — VIDEO 06 « Votre page Facebook ne prend pas de rendez-vous » · master silencieux.

Rendu image par image (PIL) → tuyau brut vers ffmpeg → MP4 1080×1920, 30 fps.
La voix off est ajoutée après validation du master (voir STATUS.md).

Trois lois, apprises à la dure dans ce dépôt :
  ① MOUVEMENT — chaque plan a au moins trois mouvements simultanés : push-in global, éléments qui
     vivent (réactions, points de saisie, notification, pulsation) et poussière lumineuse qui dérive.
     Le #4 est resté un diaporama figé ; le portique `tools/qa/audit_video_motion.py` est bloquant.
  ② COMPOSITION — PIL ne mélange PAS les couleurs translucides : `fill=(255,255,255,30)` écrit un
     blanc opaque, et `convert("RGB")` jette l'alpha. D'où les helpers `veil_*` ci-dessous, qui
     composent vraiment (c'est ce qui rendait les étiquettes illisibles en blanc sur blanc).
  ③ DÉBORDEMENT — aucun texte ne dépasse du cadre : on mesure, on tronque, et le contenu de la
     maquette Facebook est dessiné dans son propre calque puis collé avec un masque arrondi.
"""
from __future__ import annotations
import json
import math
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ─────────────────────────────────────────────────────────────── réglages
W, H, FPS = 1080, 1920, 30
DUR = 34.0
HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent.parent / "assets"
FONTS = ASSETS / "fonts"
OUT = HERE / "Video_06_Facebook_No_Booking.mp4"

NUIT, NUIT2 = (25, 30, 83), (17, 22, 77)
TEAL, AMBRE = (32, 200, 180), (252, 174, 28)
BLANC, GRIS = (245, 247, 251), (163, 171, 205)
CARTE, ENCRE, BLEU = (247, 249, 252), (22, 28, 74), (37, 99, 235)
VERT, ROUGE = (37, 211, 102), (228, 82, 92)

WEIGHT = {"M": 500, "S": 600, "B": 700, "X": 800}
_FONTS: dict = {}


def font(size: int, weight: str = "M"):
    """Les Montserrat du dépôt sont VARIABLES : sans axe explicite, tout sort en Thin (défaut 100).
    Mesuré : 1 042 pixels d'encre à 100 contre 7 435 à 800 pour le même mot."""
    key = (size, weight)
    if key not in _FONTS:
        f = ImageFont.truetype(str(FONTS / "Montserrat-VF.ttf"), size)
        f.set_variation_by_axes([WEIGHT.get(weight, 500)])
        _FONTS[key] = f
    return _FONTS[key]


SCENES = [0.0, 5.4, 12.2, 18.6, 25.0, 29.4, DUR]

# ─────────────────────────────────────────────────────────────── helpers qui composent VRAIMENT


def veil(dst: Image.Image, fn, alpha: float):
    """Dessine `fn` sur un calque puis le compose avec une vraie transparence."""
    lay = Image.new("RGBA", dst.size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(lay))
    if alpha < 1.0:
        a = lay.getchannel("A").point(lambda v: int(v * alpha))
        lay.putalpha(a)
    dst.alpha_composite(lay)


def veil_rect(im, box, radius, color, alpha):
    veil(im, lambda d: d.rounded_rectangle(box, radius=radius,
                                           fill=color + (255,)), alpha)


def veil_text(im, xy, text, fnt, color, alpha, anchor="la"):
    veil(im, lambda d: d.text(xy, text, font=fnt, fill=color + (255,), anchor=anchor), alpha)


def spaced(d, xy, text, fnt, fill, tracking=4):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + tracking


def fit(text, fnt, maxw, d=None):
    """Tronque proprement pour qu'aucun mot ne sorte du cadre."""
    d = d or ImageDraw.Draw(Image.new("RGB", (10, 10)))
    if d.textlength(text, font=fnt) <= maxw:
        return text
    while text and d.textlength(text + "…", font=fnt) > maxw:
        text = text[:-1]
    return text + "…"


def glow(im, cx, cy, r, color, alpha=70):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), fill=color + (alpha,))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(int(r / 2.0))))


def shadow(im, box, radius, blur=30, alpha=140, dy=18, pad=70):
    """Ombre portée calculée sur une tuile locale, pas sur les 1080×1920 entiers."""
    x0, y0, x1, y1 = (int(v) for v in box)
    w, h = x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((pad, pad + dy, pad + (x1 - x0), pad + (y1 - y0) + dy),
                                          radius=radius, fill=(4, 8, 30, alpha))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)), (x0 - pad, y0 - pad))


# ─── glyphes dessinés (Montserrat n'a ni ♥ ni ★ ni ✆ ni ✓ : ils sortaient en carrés vides)
def icon_heart(d, cx, cy, s, fill):
    r = s * 0.30
    d.ellipse((cx - s * 0.5, cy - s * 0.42, cx - s * 0.5 + 2 * r, cy - s * 0.42 + 2 * r), fill=fill)
    d.ellipse((cx + s * 0.5 - 2 * r, cy - s * 0.42, cx + s * 0.5, cy - s * 0.42 + 2 * r), fill=fill)
    d.polygon([(cx - s * 0.5, cy - s * 0.14), (cx + s * 0.5, cy - s * 0.14), (cx, cy + s * 0.52)],
              fill=fill)


def icon_star(d, cx, cy, s, fill):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = s * 0.52 if k % 2 == 0 else s * 0.22
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def icon_phone(d, cx, cy, s, fill):
    d.rounded_rectangle((cx - s * 0.42, cy - s * 0.5, cx + s * 0.42, cy + s * 0.5),
                        radius=s * 0.22, outline=fill, width=max(3, int(s * 0.10)))
    d.rounded_rectangle((cx - s * 0.16, cy - s * 0.36, cx + s * 0.16, cy - s * 0.20),
                        radius=s * 0.06, fill=fill)


def icon_check(d, cx, cy, s, fill):
    d.line([(cx - s * 0.5, cy + s * 0.05), (cx - s * 0.12, cy + s * 0.42), (cx + s * 0.55, cy - s * 0.38)],
           fill=fill, width=max(4, int(s * 0.20)), joint="curve")


# ─────────────────────────────────────────────────────────────── fond, poussière, barre

BASE: dict = {}


def base_scene(i):
    if i not in BASE:
        im = Image.new("RGBA", (W, H), NUIT + (255,))
        d = ImageDraw.Draw(im)
        for y in range(0, H, 4):
            k = y / H
            d.rectangle((0, y, W, y + 4), fill=(int(NUIT2[0] + (NUIT[0] - NUIT2[0]) * k),
                                              int(NUIT2[1] + (NUIT[1] - NUIT2[1]) * k),
                                              int(NUIT2[2] + (NUIT[2] - NUIT2[2]) * k)))
        for x0, y0, r, col, a in [(250, 380, 340, TEAL, 30), (880, 1500, 430, AMBRE, 24),
                                  (880, 240, 260, TEAL, 20), (140, 1640, 300, AMBRE, 18)]:
            glow(im, x0, y0, r, col, a)
        BASE[i] = im.copy()
    return BASE[i].copy()


DUST = [(0.07, 0.22, 0.13, 9), (0.83, 0.11, 0.09, 6), (0.31, 0.41, 0.11, 7), (0.66, 0.55, 0.07, 5),
        (0.18, 0.72, 0.10, 8), (0.92, 0.63, 0.06, 6), (0.47, 0.87, 0.08, 5), (0.74, 0.93, 0.12, 7),
        (0.06, 0.55, 0.09, 5), (0.55, 0.18, 0.05, 4), (0.38, 0.66, 0.06, 4), (0.88, 0.31, 0.08, 5)]


_SPRITES: dict = {}


def _sprite(r: int, col, alpha: int = 44):
    key = (r, col)
    if key not in _SPRITES:
        d = r * 2
        tile = Image.new("RGBA", (d, d), (0, 0, 0, 0))
        ImageDraw.Draw(tile).ellipse((0, 0, d, d), fill=col + (alpha,))
        _SPRITES[key] = tile.filter(ImageFilter.GaussianBlur(r / 2.0))
    return _SPRITES[key]


def dust(im, t):
    """Poussière lumineuse : la garantie que l'image bouge, quel que soit le plan."""
    for i, (bx, by, sp, r) in enumerate(DUST):
        x = (bx + (t * sp) % 1.0) % 1.0 * W
        y = (by + math.sin(t * 0.4 + i) * 0.02) * H
        rr = int(r * 3.0)
        sp_img = _sprite(rr, TEAL if i % 2 else AMBRE)
        im.alpha_composite(sp_img, (int(x - rr), int(y - rr)))


def top_bar(im, idx, prog):
    def draw(d):
        spaced(d, (64, 74), f"FACEBOOK CHECK  /  0{idx}", font(34, "S"), TEAL + (255,), tracking=4)
    veil(im, draw, 1.0)
    d = ImageDraw.Draw(im)
    x0, x1, y, n, gap = 64, W - 64, 134, 6, 12
    seg = (x1 - x0 - gap * (n - 1)) / n
    for i in range(n):
        a = x0 + i * (seg + gap)
        veil_rect(im, (a, y, a + seg, y + 7), 4, (255, 255, 255), 0.16)
        if i + 1 < idx:
            d.rounded_rectangle((a, y, a + seg, y + 7), radius=4, fill=TEAL)
        elif i + 1 == idx:
            d.rounded_rectangle((a, y, a + max(6, seg * prog), y + 7), radius=4, fill=TEAL)


def head(im, eyebrow, lines, y=200):
    d = ImageDraw.Draw(im)
    spaced(d, (64, y), eyebrow, font(34, "S"), TEAL, tracking=4)
    f = font(78, "X") if max(len(l) for l in lines) < 24 else font(62, "X")
    yy = y + 64
    for l in lines:
        d.text((64, yy), l, font=f, fill=BLANC)
        yy += int(f.size * 1.14)
    return yy


# ─────────────────────────────────────────────────────────────── la maquette « Facebook »
class Page:
    """Page fictive dessinée dans son propre calque : elle ne peut pas déborder du téléphone."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        self.d = ImageDraw.Draw(self.im)
        # échelle typographique : les tailles sont pensées pour une maquette de 760 px de large
        self.k = max(0.68, min(1.0, w / 760.0))
        self.who_fn = self.fn_(22); self.what_fn = self.fn_(26); self.when_fn = self.fn_(20)

    def fn_(self, size):
        return font(max(15, int(round(size * self.k))), "S" if size <= 22 else "M")

    def txt(self, x, y, s, fnt, fill, maxw=None, anchor="la"):
        s = fit(s, fnt, maxw, self.d) if maxw else s
        self.d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)
        return s

    def build(self, t, comments=(), reply_dots=False, counter=None):
        d, w = self.d, self.w
        band = 150
        d.rectangle((0, 0, w, band), fill=(252, 205, 100))
        ay = band - 40
        d.ellipse((20, ay, 20 + 78, ay + 78), fill=TEAL)
        d.text((20 + 26, ay + 14), "M", font=font(36, "S"), fill=(9, 40, 38))
        self.txt(114, ay + 22, "MboaCare", self.fn_(30), ENCRE, maxw=w - 132)
        self.txt(114, ay + 56, "Cabinet médical · Douala", self.fn_(24), (122, 130, 156), maxw=w - 132)
        by = ay + 92
        bw2 = int(150 * self.k)
        d.rounded_rectangle((20, by, 20 + bw2, by + 46), radius=12, fill=BLEU)
        self.txt(20 + int(32 * self.k), by + 8, "Suivre", self.fn_(24), (255, 255, 255))
        d.rounded_rectangle((20 + bw2 + 14, by, 20 + 2 * bw2 + 14, by + 46), radius=12,
                            fill=(229, 233, 241))
        self.txt(20 + bw2 + int(46 * self.k), by + 8, "Message", self.fn_(24), (44, 50, 80))
        py = by + 74
        self.txt(20, py, "Ouvert aujourd'hui · 8h – 18h", self.fn_(25), (60, 68, 100), maxw=w - 40)
        d.rounded_rectangle((20, py + 44, w - 20, py + 44 + 150), radius=14, fill=(230, 235, 245))
        self.txt(44, py + 68, "Photo de la réception", self.fn_(22), (152, 160, 182), maxw=w - 88)
        ry = py + 44 + 176
        n = min(4, int(t * 1.7) + 1)
        for i in range(n):
            cx = 34 + i * 62
            col = [(66, 133, 244), (233, 82, 92), (252, 174, 28), (32, 200, 180)][i]
            d.ellipse((cx, ry, cx + 46, ry + 46), fill=col)
            if i == 0:
                d.text((cx + 9, ry + 9), "+1", font=font(20, "S"), fill=(255, 255, 255))
            elif i == 1:
                icon_heart(d, cx + 23, ry + 24, 30, (255, 255, 255))
            elif i == 2:
                d.text((cx + 18, ry + 8), "!", font=font(22, "B"), fill=(255, 255, 255))
            else:
                icon_star(d, cx + 23, ry + 24, 32, (255, 255, 255))
        v = counter if counter is not None else 1204 + int(t * 9)
        self.txt(34 + n * 62 + 14, ry + 10, f"{v:,}".replace(",", " ") + " vues",
                 self.fn_(25), (126, 134, 160), maxw=w - (34 + n * 62 + 30))
        cy = ry + 78
        for i, (who, what, when) in enumerate(comments):
            if t < 0.9 + i * 0.7:
                continue
            d.ellipse((20, cy, 20 + 42, cy + 42), fill=(208, 216, 230))
            self.txt(74, cy - 2, who, self.who_fn, (92, 100, 126), maxw=w - 130)
            self.txt(74, cy + 30, what, self.what_fn, ENCRE, maxw=w - 90 if not when else w - 200)
            if when:
                self.txt(w - 22, cy + 31, when, self.when_fn, (152, 160, 182), anchor="ra")
            cy += 96
        if reply_dots:
            d.ellipse((74, cy, 74 + 42, cy + 42), fill=(208, 216, 230))
            for k in range(3):
                ph = (t * 2.4 + k * 0.33) % 1.0
                r = 6 + 5 * math.sin(ph * math.pi)
                d.ellipse((136 + k * 30 - r, cy + 21 - r, 136 + k * 30 + r, cy + 21 + r),
                          fill=(150, 158, 180))
            self.txt(136, cy + 38, "réponse en cours…", self.when_fn, (172, 178, 198),
                     maxw=w - 160)
        return self.im


def phone(im, x, y, w, h, page: Image.Image | None = None, radius=54, screen=(240, 243, 249)):
    d = ImageDraw.Draw(im)
    shadow(im, (x, y, x + w, y + h), radius, blur=34, alpha=150, dy=20)
    d.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=(255, 255, 255))
    inner = (x + 14, y + 14, x + w - 14, y + h - 14)
    d.rounded_rectangle(inner, radius=radius - 14, fill=screen)
    d.rounded_rectangle((x + w / 2 - 62, y + 28, x + w / 2 + 62, y + 46), radius=9, fill=(228, 233, 242))
    if page is not None:
        mask = Image.new("L", page.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, page.size[0], page.size[1]),
                                               radius=radius - 20, fill=255)
        im.paste(page, (inner[0] + 6, inner[1] + 6), mask)
    return inner


def fictif(im, x, y, s="EXEMPLE FICTIF"):
    d = ImageDraw.Draw(im)
    tw = d.textlength(s, font=font(24, "S"))
    veil_rect(im, (x, y, x + tw + 30, y + 44), 22, (255, 255, 255), 0.92)
    d = ImageDraw.Draw(im)
    d.text((x + 15, y + 9), s, font=font(24, "S"), fill=(120, 128, 152))


# ─────────────────────────────────────────────────────────────── les six plans


def scene1(im, t):
    head(im, "LE CONSTAT", ["Votre page", "Facebook a tout."])
    d = ImageDraw.Draw(im)
    pw, ph = 396, 792
    page = Page(pw, ph).build(t)
    box = phone(im, 640, 700, 420, 820, page)
    fictif(im, 664, 712)
    for i, (chip, val) in enumerate([("Photos", "vos locaux"), ("Horaires", "8h – 18h"),
                                     ("Services", "ce que vous faites")]):
        if t < 0.6 + i * 0.5:
            continue
        cy = 880 + i * 108
        veil_rect(im, (64, cy, 500, cy + 84), 42, (255, 255, 255), 0.10)
        d.text((100, cy + 12), chip, font=font(34, "S"), fill=BLANC)
        d.text((100, cy + 48), val, font=font(24, "M"), fill=TEAL)
        d.ellipse((452, cy + 34, 476, cy + 58), fill=TEAL)


def scene2(im, t):
    head(im, "CE QUI MANQUE", ["La réponse."])
    page = Page(760, 960).build(t, comments=[("Client", "Vous êtes ouverts maintenant ?", "il y a 2 h"),
                                             ("Cliente", "C'est combien l'échographie ?", "il y a 1 h")],
                                     reply_dots=True)
    phone(im, 158, 640, 772, 1010, page)
    fictif(im, 182, 652)
    d = ImageDraw.Draw(im)
    d.text((64, 1700), "Un patient qui pose une question", font=font(30, "M"), fill=GRIS)
    d.text((64, 1744), "et n'obtient rien ne revient pas :", font=font(30, "M"), fill=GRIS)
    d.text((64, 1788), "il appelle ailleurs.", font=font(30, "S"), fill=BLANC)


def scene3(im, t):
    head(im, "LE PATIENT N'ATTEND PAS", ["Il appelle", "celui d'à côté."])
    page = Page(412, 700).build(min(t, 1.4), comments=[("Client", "Vous êtes ouverts ?", "")])
    phone(im, 56, 780, 440, 800, page)
    fictif(im, 78, 800)
    bx, by = 588, 780
    shadow(im, (bx, by, bx + 420, by + 800), 54, blur=34, alpha=155, dy=20)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((bx, by, bx + 420, by + 800), radius=54, fill=(255, 255, 255))
    d.rounded_rectangle((bx + 14, by + 14, bx + 406, by + 786), radius=40, fill=(241, 244, 250))
    d.rounded_rectangle((bx + 174, by + 30, bx + 246, by + 48), radius=9, fill=(228, 233, 242))
    if t > 0.25:
        shake = 7 * math.sin(t * 24) * max(0.0, 1 - abs(t - 1.0) / 0.7)
        ny = by + 260 + max(0.0, (1.4 - t)) * -160 + shake
        veil_rect(im, (bx + 30, ny, bx + 390, ny + 136), 26, (255, 255, 255), 0.97)
        d = ImageDraw.Draw(im)
        d.ellipse((bx + 54, ny + 32, bx + 54 + 72, ny + 104), fill=ROUGE)
        d = ImageDraw.Draw(im)
        icon_phone(d, bx + 90, ny + 68, 42, (255, 255, 255))
        d.text((bx + 148, ny + 30), "Appel manqué", font=font(32, "S"), fill=(28, 34, 66))
        d.text((bx + 148, ny + 74), "Cabinet d'à côté", font=font(22, "S"), fill=(140, 148, 172))
        d.text((bx + 148, ny + 104), "il y a 1 min", font=font(22, "S"), fill=(140, 148, 172))
    if t > 1.7:
        d.text((bx + 44, by + 560), "Le rendez-vous est", font=font(30, "M"), fill=(150, 158, 180))
        d.text((bx + 44, by + 604), "déjà pris ailleurs.", font=font(34, "S"), fill=(214, 92, 100))


def scene4(im, t):
    head(im, "CE QU'UNE PAGE À VOTRE NOM FAIT", ["Répond aux trois,", "tout de suite."])
    d = ImageDraw.Draw(im)
    x0, y0, w, h = 300, 700, 480, 880
    phone(im, x0, y0, w, h, None)
    x0, y0 = x0 + 20, y0 + 20
    w, h = w - 40, h - 40
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 150), radius=30, fill=TEAL)
    d.ellipse((x0 + 26, y0 + 88, x0 + 26 + 84, y0 + 172), fill=(255, 255, 255))
    d.text((x0 + 50, y0 + 110), "M", font=font(36, "S"), fill=(9, 40, 38))
    d.text((x0 + 130, y0 + 104), "MboaCare", font=font(34, "S"), fill=(240, 255, 252))
    d.text((x0 + 130, y0 + 144), "Laboratoire · Douala", font=font(22, "S"), fill=(226, 250, 246))
    rows = [("Horaires", "Lun – Sam · 8h – 18h"), ("Examens", "Analyses · Écho · Dépistage"),
            ("Résultats", "En ligne, par SMS ou au guichet")]
    ry = y0 + 190
    for i, (k, v) in enumerate(rows):
        if t < 0.4 + i * 0.42:
            continue
        d.rounded_rectangle((x0 + 22, ry, x0 + w - 22, ry + 100), radius=20, fill=(238, 243, 250))
        d.text((x0 + 46, ry + 16), k, font=font(22, "S"), fill=(120, 128, 152))
        d.text((x0 + 46, ry + 48), fit(v, font(26, "M"), w - 110, d), font=font(26, "M"), fill=ENCRE)
        ry += 116
    pulse = 1 + 0.04 * math.sin(t * 5.2)
    bw, bh = 360 * pulse, 94 * pulse
    cx, cy = x0 + w / 2, ry + 78
    shadow(im, (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 48, blur=22, alpha=90, dy=10)
    d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=48, fill=VERT)
    d.text((cx - 108, cy - 15), "Écrire sur WhatsApp", font=font(26, "S"), fill=(8, 48, 26))
    if t > 1.4:
        yy = cy + 96
        veil_rect(im, (x0 + 40, yy, x0 + w - 40, yy + 80), 22, (232, 240, 255), 0.95)
        d = ImageDraw.Draw(im)
        d.ellipse((x0 + 64, yy + 18, x0 + 108, yy + 62), fill=(37, 160, 90))
        icon_check(d, x0 + 86, yy + 40, 32, (255, 255, 255))
        d.text((x0 + 128, yy + 25), "Rendez-vous demandé", font=font(25, "S"), fill=(30, 62, 128))
    d.text((64, 1700), "Horaires, examens, rendez-vous :", font=font(30, "M"), fill=GRIS)
    d.text((64, 1744), "le patient n'a plus à vous chercher", font=font(30, "M"), fill=GRIS)
    d.text((64, 1788), "dans les commentaires.", font=font(30, "S"), fill=BLANC)


def scene5(im, t):
    head(im, "FAITES LE TEST", ["Comptez les questions", "sans réponse."])
    page = Page(540, 820).build(2.0, comments=[("Client", "Vous êtes ouverts ?", "il y a 3 h"),
                                               ("Cliente", "C'est combien ?", "il y a 2 h")],
                                counter=1180 + int(t * 300))
    phone(im, 470, 640, 548, 880, page)
    fictif(im, 492, 652)
    d = ImageDraw.Draw(im)
    veil_rect(im, (64, 1600, 1016, 1810), 34, (255, 255, 255), 0.07)
    d.text((104, 1640), "Ouvrez votre page Facebook.", font=font(36, "S"), fill=BLANC)
    d.text((104, 1704), "Comptez les questions restées sans", font=font(30, "M"), fill=GRIS)
    d.text((104, 1748), "réponse : c'est ce chiffre qui coûte.", font=font(30, "M"), fill=GRIS)


def scene6(im, t):
    d = ImageDraw.Draw(im)
    pulse = 1 + 0.014 * math.sin(t * 3.4)
    bw, bh = 860 * pulse, 300 * pulse
    cx, cy = W / 2, 720
    shadow(im, (cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), 48, blur=44, alpha=130, dy=22)
    d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=48, fill=AMBRE)
    d.text((cx - d.textlength("Écrivez", font=font(36, "S")) / 2, cy - 122), "Écrivez",
           font=font(36, "S"), fill=(76, 48, 2))
    blink = 1.0 if (t % 1.1) < 0.72 else 0.72
    veil_text(im, (cx, cy - 84), "« APERÇU »", font(88, "X"), (26, 22, 40), blink, anchor="ma")
    d = ImageDraw.Draw(im)
    d.text((cx - d.textlength("en message privé", font=font(28, "S")) / 2, cy + 40),
           "en message privé", font=font(28, "S"), fill=(120, 74, 4))
    veil_rect(im, (64, 1150, W - 64, 1470), 36, (255, 255, 255), 0.09)
    for i, l in enumerate(["Aperçu gratuit de la page de votre",
                           "laboratoire, clinique ou cabinet —",
                           "vous la regardez avant de décider."]):
        d.text((W / 2 - d.textlength(l, font=font(34, "M")) / 2, 1205 + i * 66), l,
               font=font(34, "M"), fill=BLANC)
    d.text((64, 1620), "AMK — Développement web · Douala", font=font(36, "S"), fill=TEAL)
    d.text((64, 1678), "amk-cm.vercel.app", font=font(32, "M"), fill=GRIS)
    d.text((64, 1744), "Aperçu d'abord, prix seulement si vous gardez.", font=font(26, "S"), fill=GRIS)


SCENE_FN = [scene1, scene2, scene3, scene4, scene5, scene6]


def frame(t: float) -> Image.Image:
    i = max(k for k, s in enumerate(SCENES) if t >= s)
    local, dur = t - SCENES[i], SCENES[i + 1] - SCENES[i]
    im = base_scene(i)
    dust(im, t)
    SCENE_FN[i](im, local)
    top_bar(im, i + 1, min(1.0, local / dur))
    z = 1.0 + 0.030 * (local / dur)                       # push-in global
    cw, ch = int(W / z), int(H / z)
    ox = int((W - cw) / 2 + 5 * math.sin(t * 0.35))
    oy = int((H - ch) / 2 + 6 * math.cos(t * 0.31))
    return im.convert("RGB").crop((ox, oy, ox + cw, oy + ch)).resize((W, H), Image.BILINEAR)


def load_scenes():
    """Le montage suit la VOIX, pas l'inverse : si narration/timeline.json existe, les frontières de
    scènes sont celles des phrases enregistrées (mesurées), et la durée totale en découle."""
    global SCENES
    f = HERE / "narration" / "timeline.json"
    if f.exists():
        SCENES = json.loads(f.read_text())["starts"]
    return SCENES


def main():
    load_scenes()
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else SCENES[-1]
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    n = int(round(dur * FPS))
    cmd = [ff, "-y", "-f", "rawvideo", "-vcodec", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-vf", "setsar=1,fps=30", "-an",
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for k in range(n):
        p.stdin.write(frame(k / FPS).tobytes())
        if k % 150 == 0:
            print(f"  {k}/{n} · {k / FPS:5.1f}s", flush=True)
    p.stdin.close()
    err = p.stderr.read().decode()[-1200:]
    if p.wait() != 0:
        print(err)
        raise SystemExit("ffmpeg a échoué")
    (HERE / "timeline.json").write_text(json.dumps(
        {"scenes": SCENES, "fps": FPS, "duration": dur, "size": [W, H]}, indent=2))
    print("écrit :", out)


if __name__ == "__main__":
    main()
