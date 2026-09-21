# -*- coding: utf-8 -*-
"""Named-gift mockup for AFRIQUE LABO SARL — demos/shots/mockup-afriquelabo-wa.jpg (1600x900).
House style adapted to THEIR brand: poster cyan + navy + white, mono micro-labels,
catalogue/price console as the centrepiece (direction « FEUILLE DE RÉSULTAT »)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/user/AMK')
F = ROOT / 'content/assets/fonts'
OUT = ROOT / 'demos/shots/mockup-afriquelabo-wa.jpg'

def mont(s, weight=700):
    f = ImageFont.truetype(str(F / 'Montserrat-ExtraBold.ttf'), s)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f

def os_(s, bold=False):
    name = 'OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf'
    return ImageFont.truetype(str(ROOT / 'tools/record/fonts' / name), s)

CYAN = (18, 180, 214); CYAN_D = (12, 143, 171); CYAN_SOFT = (228, 246, 250)
NAVY = (14, 35, 71); NAVY2 = (21, 52, 100); RED = (225, 29, 46)
PAPER = (247, 250, 252); SOFT = (232, 244, 248); INK = (11, 27, 51)
MUTE = (85, 104, 138); WHITE = (255, 255, 255); LINE = (216, 228, 238)
WA = (11, 122, 62)

W, H = 1920, 1080
img = Image.new('RGB', (W, H), PAPER)
px = img.load()
for y in range(H):
    t = y / H
    r = int(PAPER[0] + (SOFT[0] - PAPER[0]) * t)
    g = int(PAPER[1] + (SOFT[1] - PAPER[1]) * t)
    b = int(PAPER[2] + (SOFT[2] - PAPER[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)
d = ImageDraw.Draw(img)

def rr(box, rad, fill=None, outline=None, w=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=w)

def wa_glyph(x, y, s, col):
    d.ellipse((x, y, x + s, y + s), outline=col, width=max(2, s // 7))
    d.line((x + s * .28, y + s * .62, x + s * .45, y + s * .5), fill=col, width=max(2, s // 8))
    d.line((x + s * .45, y + s * .5, x + s * .62, y + s * .58), fill=col, width=max(2, s // 8))

# ---------------------------------------------------------------- header
d.ellipse((70, 78, 84, 92), fill=CYAN)
d.text((100, 68), "SITE CONCEPT  ·  LABORATOIRE D'ANALYSES  ·  BESSENGUE, DOUALA",
       font=os_(17, True), fill=CYAN_D)
d.text((68, 104), "Afrique Labo SARL", font=mont(58), fill=INK)
d.text((71, 184), "Tarifs affichés  ·  Demande par WhatsApp  ·  Français / English",
       font=os_(23), fill=MUTE)
rr((70, 232, 596, 280), 24, fill=NAVY)
d.text((92, 244), "Concept par AMK — votre site en ligne en 3–5 jours",
       font=os_(16, True), fill=WHITE)

# ---------------------------------------------------------------- laptop
LX, LY, LW, LH = 300, 320, 1180, 700
rr((LX - 22, LY - 14, LX + LW + 22, LY + LH + 26), 20, fill=(10, 24, 48))
rr((LX - 22, LY + LH, LX + LW + 22, LY + LH + 26), 10, fill=(20, 42, 76))
rr((LX, LY, LX + LW, LY + LH), 10, fill=WHITE)
d.rectangle((LX, LY, LX + LW, LY + 40), fill=(240, 246, 250))
for i, c in enumerate([(248, 113, 113), (251, 191, 36), (52, 211, 153)]):
    d.ellipse((LX + 18 + i * 22, LY + 13, LX + 30 + i * 22, LY + 25), fill=c)
rr((LX + 120, LY + 8, LX + 480, LY + 32), 12, fill=WHITE, outline=LINE)
d.text((LX + 136, LY + 10), "concept-afriquelabo-v1.vercel.app", font=os_(12), fill=MUTE)

# top info bar
d.rectangle((LX, LY + 40, LX + LW, LY + 68), fill=NAVY)
d.ellipse((LX + 20, LY + 51, LX + 28, LY + 59), fill=(59, 224, 138))
d.text((LX + 36, LY + 46), "Ouvert 24h/24 · Feu rouge Bessengue, Douala", font=os_(13), fill=(234, 242, 255))
d.text((LX + LW - 150, LY + 46), "690 54 70 93", font=os_(13, True), fill=WHITE)

# nav
ny = LY + 86
rr((LX + 26, ny - 8, LX + 62, ny + 28), 10, fill=NAVY)
d.ellipse((LX + 36, ny + 2, LX + 46, ny + 12), outline=CYAN, width=2)
d.line((LX + 37, ny + 16, LX + 51, ny + 16), fill=CYAN, width=2)
d.text((LX + 70, ny - 4), "AFRIQUE LABO", font=mont(15, 800), fill=NAVY)
d.text((LX + 70, ny + 14), "ANALYSES MÉDICALES · DOUALA", font=os_(9, True), fill=MUTE)
for i, t in enumerate(["Analyses & tarifs", "Préparation", "Résultats", "Accès"]):
    d.text((LX + 300 + i * 108, ny + 4), t, font=os_(12), fill=MUTE)
rr((LX + LW - 250, ny - 4, LX + LW - 180, ny + 26), 14, fill=WHITE, outline=LINE)
d.text((LX + LW - 240, ny + 1), "FR", font=os_(12, True), fill=WHITE if False else NAVY)
d.rectangle((LX + LW - 212, ny - 4, LX + LW - 180, ny + 26), fill=None)
rr((LX + LW - 214, ny - 4, LX + LW - 181, ny + 26), 13, fill=NAVY)
d.text((LX + LW - 205, ny + 1), "EN", font=os_(12), fill=(200, 214, 234))
rr((LX + LW - 168, ny - 6, LX + LW - 26, ny + 28), 16, fill=WA)
d.text((LX + LW - 150, ny - 1), "Demander", font=os_(12, True), fill=WHITE)

# hero copy
hx, hy = LX + 40, LY + 144
d.text((hx, hy), "LABORATOIRE MULTIDISCIPLINAIRE · BESSENGUE, DOUALA", font=os_(10, True), fill=CYAN_D)
d.text((hx, hy + 20), "Vos analyses,", font=mont(36), fill=INK)
d.text((hx, hy + 62), "du prélèvement", font=mont(36), fill=INK)
d.text((hx, hy + 104), "au résultat.", font=mont(36, 800), fill=CYAN_D)
d.multiline_text((hx, hy + 156),
                 "Le tarif est affiché avant de venir, la demande part\nsur WhatsApp, et la préparation est expliquée.\nPlus besoin de venir « demander pour voir ».",
                 font=os_(14), fill=(36, 57, 92), spacing=7)
rr((hx, hy + 222, hx + 196, hy + 262), 20, fill=WA)
wa_glyph(hx + 16, hy + 233, 17, WHITE)
d.text((hx + 42, hy + 231), "Demander une analyse", font=os_(13, True), fill=WHITE)
rr((hx + 210, hy + 222, hx + 350, hy + 262), 20, outline=LINE, w=2)
d.text((hx + 232, hy + 231), "Voir les tarifs", font=os_(13, True), fill=NAVY)
for i, t in enumerate(["24h/24 accueil", "34 tests affichés", "FR / EN"]):
    rr((hx + i * 132, hy + 274, hx + (i + 1) * 128, hy + 304), 16, fill=CYAN_SOFT)
    d.text((hx + i * 132 + 12, hy + 281), t, font=os_(10, True), fill=(7, 90, 110))

# catalogue console (the centrepiece)
cx, cy = hx, hy + 316
rr((cx, cy, cx + 560, cy + 162), 16, fill=WHITE, outline=LINE)
d.text((cx + 18, cy + 9), "CATALOGUE · EXTRAITS 2026", font=os_(10, True), fill=CYAN_D)
rr((cx + 18, cy + 26, cx + 542, cy + 54), 12, fill=(244, 249, 251), outline=LINE)
d.text((cx + 30, cy + 32), "Rechercher :  glycémie, NFS, hépatite…", font=os_(11), fill=MUTE)
for i, t in enumerate(["Tous", "Biochimie", "Hématologie", "Hormonologie"]):
    fill = NAVY if i == 0 else WHITE
    rr((cx + 18 + i * 100, cy + 58, cx + 108 + i * 100, cy + 82), 12, fill=fill,
       outline=None if i == 0 else LINE)
    d.text((cx + 30 + i * 100, cy + 63), t, font=os_(9, True), fill=WHITE if i == 0 else NAVY)
rows = [("Glycémie à jeun", "1 200"), ("Hémogramme complet (NFS)", "6 000"), ("Hépatite B (AgHBs)", "14 850")]
for i, (name, price) in enumerate(rows):
    ry = cy + 84 + i * 24
    d.line((cx + 18, ry, cx + 542, ry), fill=(236, 243, 248))
    d.text((cx + 18, ry + 8), name, font=os_(12), fill=INK)
    d.text((cx + 330, ry + 7), price, font=os_(13, True), fill=NAVY)
    d.text((cx + 384, ry + 9), "FCFA", font=os_(9), fill=MUTE)
    rr((cx + 440, ry + 4, cx + 534, ry + 28), 10, fill=CYAN_SOFT, outline=(191, 233, 242))
    d.text((cx + 452, ry + 8), "Demander →", font=os_(10, True), fill=(7, 90, 110))

# hero photo (right)
hero = Image.open(ROOT / 'demos/img/labo-hero.jpg').convert('RGB')
hw, hh = 372, 470
h2 = hero.resize((hw, hh))
mask = Image.new('L', (hw, hh), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, hw, hh), 24, fill=255)
img.paste(h2, (LX + LW - hw - 40, LY + 116), mask)
rr((LX + LW - hw - 28, LY + 116 + hh - 44, LX + LW - 40, LY + 116 + hh - 12), 12,
   fill=(14, 35, 71))
d.text((LX + LW - hw - 18, LY + 116 + hh - 38), "BIOLOGIE MÉDICALE · DOUALA", font=os_(9, True), fill=WHITE)

# navy stats strip at the bottom of the screen
sy = LY + LH - 64
d.rectangle((LX, sy, LX + LW, LY + LH), fill=NAVY)
for i, (n, l) in enumerate([("24h/24", "accueil annoncé"), ("5 500+", "abonnés Facebook"),
                            ("4,5/5", "avis Google"), ("34", "tests en ligne")]):
    cxp = LX + (i + 0.5) * LW / 4
    w = d.textlength(n, font=mont(22))
    d.text((cxp - w / 2, sy + 8), n, font=mont(22), fill=WHITE)
    w2 = d.textlength(l, font=os_(10))
    d.text((cxp - w2 / 2, sy + 40), l, font=os_(10), fill=(199, 214, 238))

# ---------------------------------------------------------------- phone
PX, PY, PW, PH = 1492, 400, 330, 620
shadow = Image.new('RGBA', (PW + 40, PH + 40), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((20, 10, PW + 20, PH + 30), 40, fill=(12, 30, 58))
img.paste(shadow, (PX - 20, PY - 10), shadow)
rr((PX, PY, PX + PW, PY + PH), 30, fill=WHITE)
rr((PX + PW // 2 - 40, PY + 12, PX + PW // 2 + 40, PY + 30), 9, fill=(12, 28, 54))
# mini top bar
d.rectangle((PX, PY + 40, PX + PW, PY + 62), fill=NAVY)
d.ellipse((PX + 12, PY + 49, PX + 18, PY + 55), fill=(59, 224, 138))
d.text((PX + 24, PY + 45), "Ouvert 24h/24 · Bessengue", font=os_(9), fill=(234, 242, 255))
# mini nav
rr((PX + 16, PY + 72, PX + 40, PY + 96), 8, fill=NAVY)
d.ellipse((PX + 22, PY + 79, PX + 28, PY + 85), outline=CYAN, width=1)
d.text((PX + 46, PY + 74), "AFRIQUE LABO", font=mont(11, 800), fill=NAVY)
rr((PX + PW - 62, PY + 72, PX + PW - 44, PY + 94), 10, fill=NAVY)
d.text((PX + PW - 58, PY + 76), "FR", font=os_(9, True), fill=WHITE)
d.text((PX + PW - 40, PY + 76), "EN", font=os_(9), fill=MUTE)
# hero image
pim = hero.resize((PW - 32, 210))
pmm = Image.new('L', (PW - 32, 210), 0)
ImageDraw.Draw(pmm).rounded_rectangle((0, 0, PW - 32, 210), 16, fill=255)
img.paste(pim, (PX + 16, PY + 108), pmm)
# copy
d.text((PX + 18, PY + 330), "Vos analyses,", font=mont(18), fill=INK)
d.text((PX + 18, PY + 354), "du prélèvement", font=mont(18), fill=INK)
d.text((PX + 18, PY + 378), "au résultat.", font=mont(18, 800), fill=CYAN_D)
rr((PX + 16, PY + 408, PX + PW - 16, PY + 448), 18, fill=WA)
wa_glyph(PX + 30, PY + 418, 16, WHITE)
d.text((PX + 56, PY + 416), "Demander une analyse", font=os_(11, True), fill=WHITE)
# two catalogue rows
for i, (name, price) in enumerate([("Glycémie à jeun", "1 200"), ("Hémogramme (NFS)", "6 000")]):
    ry = PY + 462 + i * 34
    d.line((PX + 16, ry, PX + PW - 16, ry), fill=(236, 243, 248))
    d.text((PX + 16, ry + 9), name, font=os_(11), fill=INK)
    d.text((PX + PW - 96, ry + 8), price, font=os_(12, True), fill=NAVY)
    d.text((PX + PW - 56, ry + 10), "FCFA", font=os_(8), fill=MUTE)
# sticky bar
d.rectangle((PX, PY + PH - 52, PX + PW, PY + PH), fill=WHITE)
rr((PX + 10, PY + PH - 44, PX + 176, PY + PH - 10), 16, fill=WA)
wa_glyph(PX + 22, PY + PH - 38, 14, WHITE)
d.text((PX + 44, PY + PH - 34), "WhatsApp", font=os_(11, True), fill=WHITE)
rr((PX + 186, PY + PH - 44, PX + PW - 10, PY + PH - 10), 16, outline=LINE, w=2)
d.text((PX + 240, PY + PH - 34), "Appeler", font=os_(11, True), fill=NAVY)

# footer note
d.text((624, 246), "Photos d'illustration — vos vraies photos d'équipe et de devanture remplacent celles-ci à la mise en ligne.",
       font=os_(13), fill=MUTE)

img = img.resize((1600, 900), Image.LANCZOS)
img.save(OUT, 'JPEG', quality=86, optimize=True)
print('wrote', OUT, round(OUT.stat().st_size / 1024), 'KB', img.size)
