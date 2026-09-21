# -*- coding: utf-8 -*-
"""Named-gift mockup for Cabinet Dentaire YAKS — demos/shots/mockup-yaks-wa.jpg (1600x900).
House style adapted to THEIR brand: leaf-green + teal, mint background, rounded
family-friendly shapes, six-speciality medallions echoed from their poster."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "tools" / "record" / "fonts"
def f(n, s): return ImageFont.truetype(str(F / n), s)

GREEN_D = (20, 106, 44)     # #146A2C
GREEN = (87, 165, 42)       # #57A52A
TEAL_D = (14, 138, 153)     # #0E8A99
TEAL = (31, 183, 200)       # #1FB7C8
INK = (21, 48, 27)
SLATE = (92, 117, 101)
MINT = (240, 250, 241)
MINT2 = (222, 244, 228)
WHITE = (255, 255, 255)
MAGENTA = (194, 24, 91)
ORANGE = (240, 120, 30)
AMBER = (245, 166, 35)
SKY = (39, 169, 217)
RIBBONS = [MAGENTA, TEAL, SKY, TEAL, AMBER, ORANGE]

S = 2
W, H = 1920 * S // 2, 1080 * S // 2
img = Image.new("RGB", (W, H), MINT)
top = Image.new("RGB", (1, H)); top.putdata([MINT])
img = top.resize((W, H))
px = img.load()
for y in range(H):
    t = y / H
    r = int(MINT[0] + (MINT2[0] - MINT[0]) * t)
    g = int(MINT[1] + (MINT2[1] - MINT[1]) * t)
    b = int(MINT[2] + (MINT2[2] - MINT[2]) * t)
    for x in range(0, W, 4):
        for xx in range(x, min(x + 4, W)):
            px[xx, y] = (r, g, b)
d = ImageDraw.Draw(img)

def rr(box, rad, fill=None, outline=None, w=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=w)

def sparkle(cx, cy, r, col):
    d.line((cx - r, cy, cx + r, cy), fill=col, width=3 * S // 2)
    d.line((cx, cy - r, cx, cy + r), fill=col, width=3 * S // 2)
    d.line((cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2), fill=col, width=2 * S // 2)
    d.line((cx - r // 2, cy + r // 2, cx + r // 2, cy - r // 2), fill=col, width=2 * S // 2)

for (cx, cy, r, c) in [(1760, 150, 16, TEAL), (170, 760, 13, GREEN), (1830, 760, 12, TEAL), (120, 180, 10, GREEN)]:
    sparkle(cx * S // 2, cy * S // 2, r * S // 2, c)

# ---- header ----
d.ellipse((70 * S // 2 - 7 * S // 2, 84 * S // 2 - 7 * S // 2, 70 * S // 2 + 7 * S // 2, 84 * S // 2 + 7 * S // 2), fill=GREEN)
d.text((92 * S // 2, 72 * S // 2), "SITE CONCEPT  ·  CABINET DENTAIRE  ·  LOGBESSOU, DOUALA",
       font=f("OpenSans-Bold.ttf", 17 * S // 2), fill=TEAL_D)
d.text((68 * S // 2, 108 * S // 2), "Cabinet Dentaire YAKS", font=f("OpenSans-Bold.ttf", 62 * S // 2), fill=INK)
d.text((71 * S // 2, 196 * S // 2),
       "La santé de vos dents, la beauté de votre sourire  ·  6 spécialités  ·  RDV WhatsApp en un clic",
       font=f("OpenSans-Regular.ttf", 23 * S // 2), fill=SLATE)
rr((70 * S // 2, 244 * S // 2, 580 * S // 2, 292 * S // 2), 24 * S // 2, fill=GREEN_D)
d.text((92 * S // 2, 256 * S // 2), "Concept par AMK — votre site en ligne en 3–5 jours",
       font=f("OpenSans-Bold.ttf", 16 * S // 2), fill=WHITE)

# ---- laptop ----
LX, LY, LW, LH = 300 * S // 2, 320 * S // 2, 1180 * S // 2, 700 * S // 2
rr((LX - 22, LY - 14, LX + LW + 22, LY + LH + 26), 20, fill=(23, 50, 30))
rr((LX - 22, LY + LH, LX + LW + 22, LY + LH + 26), 10, fill=(40, 72, 46))
rr((LX, LY, LX + LW, LY + LH), 10, fill=WHITE)
d.rectangle((LX, LY, LX + LW, LY + 44 * S // 2), fill=(244, 250, 246))
for i, c in enumerate([(248, 113, 113), (251, 191, 36), (52, 211, 153)]):
    d.ellipse((LX + 18 * S // 2 + i * 22 * S // 2, LY + 14 * S // 2, LX + 30 * S // 2 + i * 22 * S // 2, LY + 26 * S // 2), fill=c)
rr((LX + 120 * S // 2, LY + 10 * S // 2, LX + 470 * S // 2, LY + 34 * S // 2), 12 * S // 2, fill=WHITE, outline=(214, 232, 220))
d.text((LX + 136 * S // 2, LY + 12 * S // 2), "concept-yaks-v1.vercel.app", font=f("OpenSans-Regular.ttf", 12 * S // 2), fill=SLATE)
# nav
py = LY + 58 * S // 2
rr((LX + 28 * S // 2, py - 6, LX + 60 * S // 2, py + 26), 9, fill=GREEN)
d.text((LX + 39 * S // 2, py + 1), "Y", font=f("OpenSans-Bold.ttf", 15 * S // 2), fill=WHITE)
d.text((LX + 70 * S // 2, py - 4), "CABINET YAKS", font=f("OpenSans-Bold.ttf", 15 * S // 2), fill=GREEN_D)
for i, t in enumerate(["Spécialités", "Tarifs", "Visite", "Questions"]):
    d.text((LX + 250 * S // 2 + i * 96 * S // 2, py), t, font=f("OpenSans-Regular.ttf", 13 * S // 2), fill=SLATE)
rr((LX + LW - 150 * S // 2, py - 8, LX + LW - 28 * S // 2, py + 26), 17, fill=TEAL_D)
d.text((LX + LW - 138 * S // 2, py - 2), "Prendre RDV", font=f("OpenSans-Bold.ttf", 12 * S // 2), fill=WHITE)
# hero copy
hx, hy = LX + 40 * S // 2, LY + 116 * S // 2
d.text((hx, hy), "CABINET DENTAIRE — LOGBESSOU", font=f("OpenSans-Bold.ttf", 11 * S // 2), fill=TEAL_D)
d.text((hx, hy + 26 * S // 2), "La santé de", font=f("OpenSans-Bold.ttf", 40 * S // 2), fill=INK)
d.text((hx, hy + 70 * S // 2), "vos dents,", font=f("OpenSans-Bold.ttf", 40 * S // 2), fill=GREEN_D)
d.text((hx, hy + 114 * S // 2), "la beauté de", font=f("OpenSans-Bold.ttf", 40 * S // 2), fill=INK)
d.text((hx, hy + 158 * S // 2), "votre sourire.", font=f("OpenSans-Bold.ttf", 40 * S // 2), fill=TEAL_D)
d.multiline_text((hx, hy + 214 * S // 2),
                 "Six spécialités pour toute la famille,\ntarifs FCFA clairs et rendez-vous\nWhatsApp en français et en anglais.",
                 font=f("OpenSans-Regular.ttf", 15 * S // 2), fill=SLATE, spacing=7)
rr((hx, hy + 300 * S // 2, hx + 200 * S // 2, hy + 342 * S // 2), 21, fill=TEAL_D)
d.text((hx + 22 * S // 2, hy + 309 * S // 2), "Prendre rendez-vous", font=f("OpenSans-Bold.ttf", 13 * S // 2), fill=WHITE)
rr((hx + 214 * S // 2, hy + 300 * S // 2, hx + 380 * S // 2, hy + 342 * S // 2), 21, outline=GREEN_D, w=2)
d.text((hx + 232 * S // 2, hy + 309 * S // 2), "Voir les spécialités", font=f("OpenSans-Bold.ttf", 13 * S // 2), fill=GREEN_D)
for i, t in enumerate(["⭐ 100 % · 5 avis", "📍 Immeuble BAO", "💬 WhatsApp"]):
    rr((hx + i * 150 * S // 2, hy + 360 * S // 2, hx + (i + 1) * 148 * S // 2, hy + 392 * S // 2), 16, fill=(228, 246, 236))
    d.text((hx + i * 150 * S // 2 + 12 * S // 2, hy + 366 * S // 2), t, font=f("OpenSans-Bold.ttf", 10 * S // 2), fill=TEAL_D)
# six medallions (poster wheel echo)
my = hy + 430 * S // 2
for i, c in enumerate(RIBBONS):
    cxp = hx + i * 56 * S // 2
    d.ellipse((cxp, my, cxp + 40 * S // 2, my + 40 * S // 2), fill=c, outline=WHITE, width=3)
d.text((hx + 6 * 56 * S // 2 + 6, my + 10 * S // 2), "+ prévention", font=f("OpenSans-Bold.ttf", 12 * S // 2), fill=GREEN_D)
# hero photo
hero = Image.open(ROOT / "demos/img/yaks-hero.jpg").convert("RGB")
hw, hh = 380 * S // 2, 470 * S // 2
h2 = hero.resize((hw, hh))
maska = Image.new("L", (hw, hh), 0)
ImageDraw.Draw(maska).rounded_rectangle((0, 0, hw, hh), 26, fill=255)
img.paste(h2, (LX + LW - hw - 40 * S // 2, LY + 118 * S // 2), maska)
# stats bar gradient
sy = LY + LH - 72 * S // 2
bar = Image.new("RGB", (LW, 72 * S // 2))
bp = bar.load()
BW, BH = bar.size
for x in range(BW):
    t = x / BW
    col = (int(GREEN_D[0] + (TEAL_D[0] - GREEN_D[0]) * t),
           int(GREEN_D[1] + (TEAL_D[1] - GREEN_D[1]) * t),
           int(GREEN_D[2] + (TEAL_D[2] - GREEN_D[2]) * t))
    for y in range(BH):
        bp[x, y] = col
img.paste(bar, (LX, sy))
for i, (n, l) in enumerate([("2 100", "mentions Facebook"), ("100 %", "recommandent"), ("6", "spécialités"), ("6 000 F", "consultation*")]):
    cxp = LX + (i + 0.5) * LW / 4
    d.text((cxp - 40, sy + 10), n, font=f("OpenSans-Bold.ttf", 24 * S // 2), fill=WHITE)
    d.text((cxp - 52, sy + 44), l, font=f("OpenSans-Regular.ttf", 11 * S // 2), fill=(205, 244, 224))

# ---- phone ----
PX, PY, PW, PH = 1430 * S // 2, 400 * S // 2, 330 * S // 2, 620 * S // 2
sh = Image.new("RGBA", (PW + 40, PH + 40), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle((20, 8, PW + 20, PH + 28), 40, fill=(20, 44, 26))
img.paste(sh, (PX - 20, PY - 8), sh)
rr((PX, PY, PX + PW, PY + PH), 30, fill=WHITE)
rr((PX + PW // 2 - 40, PY + 12, PX + PW // 2 + 40, PY + 30), 9, fill=(20, 44, 26))
# phone nav
rr((PX + 18, PY + 44, PX + 46, PY + 72), 8, fill=GREEN)
d.text((PX + 28, PY + 49), "Y", font=f("OpenSans-Bold.ttf", 14 * S // 2), fill=WHITE)
d.text((PX + 54, PY + 48), "YAKS", font=f("OpenSans-Bold.ttf", 13 * S // 2), fill=GREEN_D)
rr((PX + PW - 86, PY + 46, PX + PW - 52, PY + 70), 12, fill=TEAL_D)
d.text((PX + PW - 81, PY + 50), "EN FR", font=f("OpenSans-Bold.ttf", 10 * S // 2), fill=WHITE)
# phone image
pim = hero.resize((PW - 32, 232 * S // 2))
pmm = Image.new("L", (PW - 32, 232 * S // 2), 0)
ImageDraw.Draw(pmm).rounded_rectangle((0, 0, PW - 32, 232 * S // 2), 18, fill=255)
img.paste(pim, (PX + 16, PY + 88), pmm)
d.text((PX + 18, PY + 340), "La santé de vos dents,", font=f("OpenSans-Bold.ttf", 19 * S // 2), fill=GREEN_D)
d.text((PX + 18, PY + 368), "la beauté de votre sourire.", font=f("OpenSans-Bold.ttf", 19 * S // 2), fill=TEAL_D)
d.multiline_text((PX + 18, PY + 402), "6 spécialités pour toute\nla famille, à Logbessou.",
                 font=f("OpenSans-Regular.ttf", 13 * S // 2), fill=SLATE, spacing=4)
# mini medallions
for i, c in enumerate(RIBBONS):
    cxp = PX + 20 + (i % 3) * 62 * S // 2
    cyp = PY + 456 + (i // 3) * 40 * S // 2
    d.ellipse((cxp, cyp, cxp + 30 * S // 2, cyp + 30 * S // 2), fill=c)
rr((PX + 18, PY + 540, PX + PW - 18, PY + 584), 22, fill=TEAL_D)
d.text((PX + 50, PY + 550), "📅  Prendre rendez-vous", font=f("OpenSans-Bold.ttf", 13 * S // 2), fill=WHITE)
# sticky bar
d.rectangle((PX, PY + PH - 56, PX + PW, PY + PH), fill=GREEN_D)
d.text((PX + 24, PY + PH - 38), "💬 WhatsApp 6j/7", font=f("OpenSans-Bold.ttf", 13 * S // 2), fill=WHITE)

img = img.resize((1600, 900), Image.LANCZOS)
out = ROOT / "demos/shots/mockup-yaks-wa.jpg"
img.save(out, "JPEG", quality=86, optimize=True)
print("wrote", out, round(out.stat().st_size / 1024), "KB")
