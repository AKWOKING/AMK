# -*- coding: utf-8 -*-
"""Generic OPTICAL mockup — demos/shots/mockup-opticien-wa.jpg (1600x900).
House style, no real name: 'Votre Opticien' + Demo label. Palette ink teal +
amber + clay on cream, matching demos/concept-opticien-v1.html (direction « LE MIROIR »)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/user/AMK')
OUT = ROOT / 'demos/shots/mockup-opticien-wa.jpg'
FONTS = ROOT / 'content/assets/fonts'

def mont(s, weight=700):
    f = ImageFont.truetype(str(FONTS / 'Montserrat-ExtraBold.ttf'), s)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f
def os_(s, bold=False):
    return ImageFont.truetype(str(ROOT / 'tools/record/fonts' / ('OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf')), s)

INK = (14, 59, 67); INK2 = (21, 87, 99); AMBER = (240, 160, 60); CLAY = (201, 111, 74)
CREAM = (251, 246, 239); CREAM2 = (244, 236, 225); WHITE = (255, 255, 255)
MUTE = (94, 122, 128); LINE = (222, 229, 228); WA = (11, 122, 62)

W, H = 1920, 1080
img = Image.new('RGB', (W, H), CREAM)
px = img.load()
for y in range(H):
    t = y / H
    px_row = (int(CREAM[0] + (CREAM2[0] - CREAM[0]) * t),
              int(CREAM[1] + (CREAM2[1] - CREAM[1]) * t),
              int(CREAM[2] + (CREAM2[2] - CREAM[2]) * t))
    for x in range(W):
        px[x, y] = px_row
d = ImageDraw.Draw(img)

def rr(box, rad, fill=None, outline=None, w=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=w)

def wa_glyph(x, y, s, col):
    d.ellipse((x, y, x + s, y + s), outline=col, width=max(2, s // 7))
    d.line((x + s * .28, y + s * .62, x + s * .45, y + s * .5), fill=col, width=max(2, s // 8))
    d.line((x + s * .45, y + s * .5, x + s * .62, y + s * .58), fill=col, width=max(2, s // 8))

def glasses(cx, cy, s, col, wd=4):
    r = s // 2
    d.ellipse((cx - r - s // 2, cy - r, cx + r - s // 2, cy + r), outline=col, width=wd)
    d.ellipse((cx + s // 2 - r, cy - r, cx + s // 2 + r, cy + r), outline=col, width=wd)
    d.line((cx - r * .2, cy, cx + r * .2, cy), fill=col, width=wd)
    d.line((cx - s // 2 - r, cy - r // 2, cx - s // 2 - r - 10, cy - r // 2 - 10), fill=col, width=wd)

# header
d.ellipse((70, 78, 84, 92), fill=AMBER)
d.text((100, 68), "SITE CONCEPT  ·  OPTICIEN  ·  DOUALA", font=os_(17, True), fill=CLAY)
d.text((68, 104), "Votre Opticien", font=mont(58), fill=INK)
d.text((71, 186), "Contrôle de la vue  ·  Choix de la monture  ·  Devis WhatsApp", font=os_(23), fill=MUTE)
rr((70, 232, 700, 280), 24, fill=INK)
d.text((92, 244), "Concept par AMK — votre site en ligne en 3–5 jours", font=os_(16, True), fill=WHITE)
d.text((724, 246), "Photos d'illustration — vos vraies montures remplacent ces images.", font=os_(13), fill=MUTE)

# ---------------- laptop
LX, LY, LW, LH = 300, 320, 1180, 700
rr((LX - 22, LY - 14, LX + LW + 22, LY + LH + 26), 20, fill=(9, 38, 44))
rr((LX - 22, LY + LH, LX + LW + 22, LY + LH + 26), 10, fill=(16, 60, 68))
rr((LX, LY, LX + LW, LY + LH), 10, fill=WHITE)
d.rectangle((LX, LY, LX + LW, LY + 40), fill=(240, 246, 245))
for i, c in enumerate([(248, 113, 113), (251, 191, 36), (52, 211, 153)]):
    d.ellipse((LX + 18 + i * 22, LY + 13, LX + 30 + i * 22, LY + 25), fill=c)
rr((LX + 120, LY + 8, LX + 500, LY + 32), 12, fill=WHITE, outline=LINE)
d.text((LX + 136, LY + 10), "concept-opticien-v1.vercel.app", font=os_(12), fill=MUTE)

# info bar
d.rectangle((LX, LY + 40, LX + LW, LY + 68), fill=INK)
d.text((LX + 20, LY + 46), "Contrôle de la vue sur rendez-vous  ·  Douala", font=os_(13), fill=(234, 244, 245))
d.text((LX + LW - 170, LY + 46), "+237 6XX XX XX XX", font=os_(13, True), fill=WHITE)

# nav
ny = LY + 88
glasses(LX + 44, ny + 4, 20, AMBER, 3)
d.text((LX + 80, ny - 6), "VOTRE OPTICIEN", font=mont(15, 800), fill=INK)
d.text((LX + 80, ny + 12), "CONCEPT DE DÉMONSTRATION", font=os_(8, True), fill=MUTE)
for i, t in enumerate(["Choisir ma forme", "Verres & devis", "Services", "Venir"]):
    d.text((LX + 320 + i * 116, ny + 2), t, font=os_(12), fill=MUTE)
rr((LX + LW - 250, ny - 6, LX + LW - 186, ny + 24), 13, fill=INK)
d.text((LX + LW - 236, ny - 1), "FR", font=os_(12, True), fill=WHITE)
d.text((LX + LW - 210, ny - 1), "EN", font=os_(12), fill=(120, 150, 155))
rr((LX + LW - 174, ny - 8, LX + LW - 26, ny + 26), 17, fill=WA)
d.text((LX + LW - 150, ny - 3), "Rendez-vous", font=os_(12, True), fill=WHITE)

# hero copy
hx, hy = LX + 40, LY + 148
d.text((hx, hy), "OPTICIEN · CONTRÔLE DE LA VUE · MONTAGE", font=os_(10, True), fill=CLAY)
d.text((hx, hy + 22), "Voir net.", font=mont(40), fill=INK)
d.text((hx, hy + 68), "Se voir bien.", font=mont(40), fill=CLAY)
d.multiline_text((hx, hy + 124),
                 "Contrôle de la vue sur rendez-vous, conseil sur la\nforme de votre visage, et un devis verres qui arrive\nsur WhatsApp avant que vous ne vous déplaciez.",
                 font=os_(14), fill=(44, 76, 83), spacing=7)
rr((hx, hy + 210, hx + 210, hy + 250), 20, fill=WA)
wa_glyph(hx + 16, hy + 221, 17, WHITE)
d.text((hx + 42, hy + 219), "Prendre rendez-vous", font=os_(13, True), fill=WHITE)
rr((hx + 224, hy + 210, hx + 396, hy + 250), 20, outline=LINE, w=2)
d.text((hx + 246, hy + 219), "Choisir ma forme", font=os_(13, True), fill=INK)
for i, t in enumerate(["15 min · contrôle", "Devis avant déplacement", "FR / EN"]):
    rr((hx + i * 168, hy + 264, hx + (i + 1) * 164, hy + 294), 15, fill=(238, 244, 243))
    d.text((hx + i * 168 + 12, hy + 271), t, font=os_(10, True), fill=INK2)

# shape selector block (signature) — the drawn mirror, as on the site
sy = hy + 300
SH_H = 232
d.rectangle((hx, sy, hx + 560, sy + SH_H), fill=INK)
d.text((hx + 18, sy + 12), "QUELLE FORME POUR VOTRE VISAGE ?", font=os_(10, True), fill=AMBER)

SKIN = (242, 217, 192); SKIN2 = (228, 196, 166); HAIR = (43, 38, 32)
BROW = (74, 59, 46); FRAME = (74, 50, 34)

def mirror_face(cx, cy, k=0.62):
    """Drawn head + selected (round) frame — same geometry as the site's SVG."""
    def S(v): return int(round(v * k))
    d.ellipse((cx - S(70), cy - S(96), cx + S(70), cy + S(40)), fill=HAIR)          # hair dome
    d.ellipse((cx - S(14), cy + S(74), cx + S(14), cy + S(130)), fill=SKIN2)        # neck
    for sx in (-1, 1):                                                              # ears
        ex = cx + sx * S(84)
        d.ellipse((ex - S(11), cy - S(21), ex + S(11), cy + S(21)), fill=SKIN2)
    d.ellipse((cx - S(84), cy - S(102), cx + S(84), cy + S(102)), fill=SKIN)        # face
    d.ellipse((cx - S(66), cy - S(99), cx + S(70), cy - S(20)), fill=SKIN)          # carve forehead
    d.arc((cx - S(60), cy - S(70), cx - S(6), cy - S(30)), 200, 340, fill=BROW, width=2)
    d.arc((cx + S(6), cy - S(70), cx + S(60), cy - S(30)), 200, 340, fill=BROW, width=2)
    for sx in (-1, 1):
        ex = cx + sx * S(34)
        d.ellipse((ex - S(15), cy - S(9), ex + S(15), cy + S(9)), fill=(255, 255, 255))
        d.ellipse((ex - S(6), cy - S(6), ex + S(6), cy + S(6)), fill=(58, 46, 36))
    d.line((cx, cy + S(4), cx + S(8), cy + S(32)), fill=SKIN2, width=2)
    d.arc((cx - S(22), cy + S(30), cx + S(22), cy + S(62)), 20, 160, fill=(192, 139, 114), width=2)
    for sx in (-1, 1):                                                              # round frame
        ex = cx + sx * S(34)
        d.ellipse((ex - S(33), cy - S(33), ex + S(33), cy + S(33)), outline=FRAME, width=3)
    d.line((cx - S(1), cy, cx + S(1), cy), fill=FRAME, width=3)
    d.line((cx - S(67), cy, cx - S(84), cy + S(2)), fill=FRAME, width=3)
    d.line((cx + S(67), cy, cx + S(84), cy + S(2)), fill=FRAME, width=3)

mirror_face(hx + 118, sy + 104)
d.text((hx + 18, sy + SH_H - 22), "Illustration — l'essayage réel se fait en boutique", font=os_(9), fill=(159, 189, 195))

labels = ["Rond", "Carré", "Œil de chat", "Aviateur"]
for i, t in enumerate(labels):
    x = hx + 250 + (i % 2) * 156
    y = sy + 34 + (i // 2) * 56
    on = (i == 0)
    rr((x, y, x + 148, y + 48), 10, fill=AMBER if on else None,
       outline=None if on else (70, 110, 116), w=2)
    col = (58, 37, 8) if on else (234, 244, 245)
    glasses(x + 30, y + 24, 20, col, 2)
    d.text((x + 56, y + 16), t, font=os_(11, True), fill=col)
d.text((hx + 250, sy + SH_H - 46), "Rond — adoucit les visages anguleux.", font=os_(11), fill=(203, 224, 227))
d.text((hx + 250, sy + SH_H - 28), "Essayage en boutique · ajustement offert", font=os_(10), fill=(159, 189, 195))

# hero photo right
hero = Image.open(ROOT / 'demos/img/opticien-hero.jpg').convert('RGB')
hw, hh = 372, 470
h2 = hero.resize((hw, hh))
mask = Image.new('L', (hw, hh), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, hw, hh), 24, fill=255)
img.paste(h2, (LX + LW - hw - 40, LY + 118), mask)
rr((LX + LW - hw - 28, LY + 118 + hh - 44, LX + LW - 40, LY + 118 + hh - 12), 12, fill=INK)
d.text((LX + LW - hw - 18, LY + 118 + hh - 38), "CONTRÔLE DE LA VUE EN BOUTIQUE", font=os_(9, True), fill=WHITE)

# quote console under the photo (right column)
qx, qy = LX + LW - hw - 40, LY + 118 + hh + 16
rr((qx, qy, qx + hw, qy + 132), 16, fill=WHITE, outline=LINE)
d.text((qx + 14, qy + 10), "COMPOSEZ VOTRE DEVIS", font=os_(10, True), fill=CLAY)
for i, (t, v) in enumerate([("Verres", "Progressifs"), ("Pour", "Adulte"), ("Usage", "Bureau")]):
    ry = qy + 32 + i * 26
    d.line((qx + 14, ry, qx + hw - 14, ry), fill=(236, 242, 241))
    d.text((qx + 14, ry + 6), t, font=os_(11), fill=MUTE)
    d.text((qx + 84, ry + 6), v, font=os_(11, True), fill=INK)
rr((qx + 14, qy + 112 - 6, qx + hw - 14, qy + 132 - 2), 12, fill=WA)
d.text((qx + 96, qy + 111), "Envoyer ma demande", font=os_(11, True), fill=WHITE)

# ---------------- phone
PX, PY, PW, PH = 1492, 400, 330, 620
shadow = Image.new('RGBA', (PW + 40, PH + 40), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((20, 10, PW + 20, PH + 30), 40, fill=(10, 44, 50))
img.paste(shadow, (PX - 20, PY - 10), shadow)
rr((PX, PY, PX + PW, PY + PH), 30, fill=WHITE)
rr((PX + PW // 2 - 40, PY + 12, PX + PW // 2 + 40, PY + 30), 9, fill=(10, 40, 46))
d.rectangle((PX, PY + 40, PX + PW, PY + 62), fill=INK)
d.text((PX + 12, PY + 45), "Contrôle de la vue · Douala", font=os_(9), fill=(234, 244, 245))
glasses(PX + 26, PY + 84, 18, AMBER, 2)
d.text((PX + 54, PY + 76), "VOTRE OPTICIEN", font=mont(11, 800), fill=INK)
rr((PX + PW - 62, PY + 74, PX + PW - 44, PY + 96), 10, fill=INK)
d.text((PX + PW - 58, PY + 78), "FR", font=os_(9, True), fill=WHITE)
d.text((PX + PW - 40, PY + 78), "EN", font=os_(9), fill=MUTE)
pim = hero.resize((PW - 32, 190))
pmm = Image.new('L', (PW - 32, 190), 0)
ImageDraw.Draw(pmm).rounded_rectangle((0, 0, PW - 32, 190), 16, fill=255)
img.paste(pim, (PX + 16, PY + 108), pmm)
d.text((PX + 18, PY + 312), "Voir net.", font=mont(22), fill=INK)
d.text((PX + 18, PY + 342), "Se voir bien.", font=mont(22), fill=CLAY)
rr((PX + 16, PY + 380, PX + PW - 16, PY + 420), 18, fill=WA)
wa_glyph(PX + 30, PY + 390, 16, WHITE)
d.text((PX + 56, PY + 388), "Prendre rendez-vous", font=os_(11, True), fill=WHITE)
# shape chips 2x2
for i, t in enumerate(["Rond", "Carré", "Œil de chat", "Aviateur"]):
    x = PX + 16 + (i % 2) * 152
    y = PY + 432 + (i // 2) * 46
    on = i == 0
    rr((x, y, x + 144, y + 38), 10, fill=AMBER if on else WHITE, outline=None if on else LINE, w=2)
    glasses(x + 24, y + 19, 18, (58, 37, 8) if on else INK, 2)
    d.text((x + 46, y + 12), t, font=os_(10, True), fill=(58, 37, 8) if on else INK)
d.rectangle((PX, PY + PH - 52, PX + PW, PY + PH), fill=WHITE)
rr((PX + 10, PY + PH - 44, PX + 176, PY + PH - 10), 16, fill=WA)
wa_glyph(PX + 22, PY + PH - 38, 14, WHITE)
d.text((PX + 44, PY + PH - 34), "WhatsApp", font=os_(11, True), fill=WHITE)
rr((PX + 186, PY + PH - 44, PX + PW - 10, PY + PH - 10), 16, outline=LINE, w=2)
d.text((PX + 232, PY + PH - 34), "Appeler", font=os_(11, True), fill=INK)

img = img.resize((1600, 900), Image.LANCZOS)
img.save(OUT, 'JPEG', quality=86, optimize=True)
print('wrote', OUT, round(OUT.stat().st_size / 1024), 'KB', img.size)
