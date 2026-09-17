# -*- coding: utf-8 -*-
"""LA BÉTHANIE mockup — demos/shots/mockup-labethanie-wa.jpg (1600x900).
House style: laptop + phone drawn in the concept's own palette and type
(Montserrat + Open Sans, royal blue #0F4C9C / leaf green, real entrance photo).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/user/AMK')
OUT = ROOT / 'demos/shots/mockup-labethanie-wa.jpg'
FONTS = ROOT / 'content/assets/fonts'

def mont(s, weight=700):
    f = ImageFont.truetype(str(FONTS / 'Montserrat-ExtraBold.ttf'), s)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f

def os_(s, bold=False):
    return ImageFont.truetype(str(ROOT / 'tools/record/fonts' / ('OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf')), s)

BLUE = (15, 76, 156); BLUE_D = (10, 44, 94); CYAN = (31, 169, 216)
GREEN = (63, 139, 30); GREEN_D = (46, 107, 20)
INK = (16, 35, 63); MUTE = (81, 103, 129); TINT = (238, 244, 252); MINT = (239, 247, 233)
WHITE = (255, 255, 255); LINE = (219, 228, 240); WA = (11, 122, 62)
PAGE = (244, 248, 253); PAGE2 = (231, 239, 249)

W, H = 1920, 1080
img = Image.new('RGB', (W, H), PAGE)
px = img.load()
for y in range(H):
    t = y / H
    row = tuple(int(PAGE[i] + (PAGE2[i] - PAGE[i]) * t) for i in range(3))
    for x in range(W):
        px[x, y] = row
d = ImageDraw.Draw(img)

def rr(box, rad, fill=None, outline=None, w=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=w)

def wa_glyph(x, y, s, col):
    d.ellipse((x, y, x + s, y + s), outline=col, width=max(2, s // 7))
    d.line((x + s * .28, y + s * .62, x + s * .45, y + s * .5), fill=col, width=max(2, s // 8))
    d.line((x + s * .45, y + s * .5, x + s * .62, y + s * .58), fill=col, width=max(2, s // 8))

def cross_tile(x, y, s):
    rr((x, y, x + s, y + s), max(5, s // 4), fill=BLUE)
    u = s / 40
    d.rectangle((x + 17 * u, y + 7 * u, x + 23 * u, y + 33 * u), fill=WHITE)
    d.rectangle((x + 7 * u, y + 17 * u, x + 33 * u, y + 23 * u), fill=WHITE)
    d.ellipse((x + 27 * u, y + 9 * u, x + 36 * u, y + 17 * u), fill=CYAN)
    d.ellipse((x + 27 * u, y + 25 * u, x + 36 * u, y + 33 * u), fill=GREEN)

def tick(x, y, s, on=True):
    rr((x, y, x + s, y + s), 5, fill=GREEN_D if on else WHITE, outline=None if on else (176, 193, 216), w=2)
    if on:
        d.line((x + s * .24, y + s * .54, x + s * .43, y + s * .72), fill=WHITE, width=max(2, s // 7))
        d.line((x + s * .43, y + s * .72, x + s * .78, y + s * .3), fill=WHITE, width=max(2, s // 7))

# ---------- header
d.ellipse((70, 78, 84, 92), fill=GREEN)
d.text((100, 68), "SITE CONCEPT  ·  CLINIQUE LA BÉTHANIE  ·  BONABÉRI, DOUALA", font=os_(17, True), fill=BLUE_D)
d.text((68, 104), "Clinique La Béthanie", font=mont(56), fill=BLUE_D)
d.text((71, 182), "Gynécologie & maternité  ·  Chirurgie  ·  Ouvert 24h/24, 7j/7  ·  Rue Mpondo (Ancienne Route)", font=os_(22), fill=MUTE)
rr((70, 226, 760, 274), 24, fill=GREEN_D)
d.text((92, 238), "Aperçu préparé par AMK — en ligne en 3–5 jours", font=os_(16, True), fill=WHITE)
d.text((786, 240), "La photo de l'entrée est la vôtre : le reste se complète avec vos clichés.", font=os_(14), fill=MUTE)

# ---------- laptop
LX, LY, LW, LH = 250, 320, 1240, 700
rr((LX - 22, LY - 14, LX + LW + 22, LY + LH + 26), 20, fill=(6, 22, 48))
rr((LX - 22, LY + LH, LX + LW + 22, LY + LH + 26), 10, fill=(12, 34, 70))
rr((LX, LY, LX + LW, LY + LH), 10, fill=WHITE)
d.rectangle((LX, LY, LX + LW, LY + 38), fill=(240, 245, 252))
for i, c in enumerate([(248, 113, 113), (251, 191, 36), (52, 211, 153)]):
    d.ellipse((LX + 18 + i * 22, LY + 12, LX + 30 + i * 22, LY + 24), fill=c)
rr((LX + 110, LY + 7, LX + 520, LY + 31), 12, fill=WHITE, outline=LINE)
d.text((LX + 126, LY + 9), "concept-labethanie-v1.vercel.app", font=os_(12), fill=MUTE)

y = LY + 38
d.rectangle((LX, y, LX + LW, y + 26), fill=BLUE_D)
d.text((LX + 18, y + 4), "Ouvert 24h/24 · 7j/7 — Bonabéri, Rue Mpondo (Ancienne Route)", font=os_(12), fill=(220, 233, 251))
d.text((LX + LW - 160, y + 4), "+237 677 76 07 82", font=os_(12, True), fill=WHITE)

y += 26
d.rectangle((LX, y, LX + LW, y + 56), fill=WHITE)
d.line((LX, y + 56, LX + LW, y + 56), fill=LINE)
cross_tile(LX + 20, y + 10, 36)
d.text((LX + 64, y + 11), "LA BÉTHANIE", font=mont(15), fill=BLUE_D)
d.text((LX + 64, y + 31), "CENTRE MÉDICO-CHIRURGICAL · MATERNITÉ", font=os_(8, True), fill=MUTE)
for i, t in enumerate(["Gynécologie", "Urgences", "Chirurgie", "Nous trouver"]):
    d.text((LX + 420 + i * 118, y + 20), t, font=os_(12), fill=INK)
rr((LX + LW - 232, y + 14, LX + LW - 168, y + 42), 14, fill=BLUE_D)
d.text((LX + LW - 218, y + 19), "FR", font=os_(12, True), fill=WHITE)
d.text((LX + LW - 192, y + 19), "EN", font=os_(12), fill=(150, 170, 200))
rr((LX + LW - 156, y + 13, LX + LW - 20, y + 43), 15, fill=WA)
d.text((LX + LW - 134, y + 18), "Rendez-vous", font=os_(12, True), fill=WHITE)

# hero
hy = y + 56
hx = LX + 26
d.text((hx, hy + 18), "BONABÉRI · RUE MPONDO (ANCIENNE ROUTE) · DOUALA", font=os_(9, True), fill=BLUE)
d.text((hx, hy + 36), "Votre santé intime,", font=mont(31), fill=BLUE_D)
d.text((hx, hy + 74), "notre priorité.", font=mont(31), fill=BLUE)
d.multiline_text((hx, hy + 122),
                 "Gynécologie, suivi de grossesse, maternité et chirurgie — à la Clinique La\n"
                 "Béthanie, à Bonabéri. Un accueil discret, des examens expliqués, et un\n"
                 "rendez-vous que vous pouvez demander sur WhatsApp, en quelques mots.",
                 font=os_(12.5), fill=(44, 66, 98), spacing=7)
rr((hx, hy + 196, hx + 196, hy + 232), 18, fill=WA)
wa_glyph(hx + 14, hy + 206, 16, WHITE)
d.text((hx + 38, hy + 203), "Prendre rendez-vous", font=os_(12, True), fill=WHITE)
rr((hx + 208, hy + 196, hx + 350, hy + 232), 18, outline=LINE, w=2)
d.text((hx + 232, hy + 203), "Nous trouver", font=os_(12, True), fill=BLUE_D)
for i, t in enumerate(["24h/24 · 7j/7 ouvert", "Gynécologie & maternité", "Rue Mpondo, Bonabéri"]):
    rr((hx + i * 168, hy + 246, hx + (i + 1) * 160, hy + 274), 14, fill=TINT, outline=LINE)
    d.text((hx + i * 168 + 11, hy + 252), t, font=os_(9.5, True), fill=(44, 66, 98))

# hero photo (the real entrance)
photo = Image.open(ROOT / 'clients/la-bethanie/entrance Clinique La Béthanie (Bonabéri).jpg').convert('RGB')
pw, ph = 480, 300
cut = photo.width * 0.62
pcrop = photo.crop((int(photo.width - cut), int(photo.height * .04), photo.width, photo.height))
p2 = pcrop.resize((pw, ph))
mask = Image.new('L', (pw, ph), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), 22, fill=255)
img.paste(p2, (LX + LW - pw - 26, hy), mask)
rr((LX + LW - pw - 12, hy + ph - 42, LX + LW - 40, hy + ph - 10), 12, fill=(10, 44, 94, 255))
d.text((LX + LW - pw + 2, hy + ph - 37), "NOTRE ENTRÉE — RUE MPONDO, BONABÉRI", font=os_(8.5, True), fill=WHITE)

# gynéco section with the tickable leaflet
gy = hy + 320
d.line((LX + 26, gy - 8, LX + LW - 26, gy - 8), fill=LINE)
d.text((hx, gy + 6), "SERVICE DE GYNÉCOLOGIE", font=os_(9, True), fill=BLUE)
d.text((hx, gy + 22), "Nos prestations — cochez ce qui vous concerne", font=mont(17), fill=BLUE_D)
card_x, card_y, card_w = hx, gy + 56, 560
rr((card_x, card_y, card_x + card_w, card_y + 168), 12, fill=WHITE, outline=LINE)
d.rectangle((card_x, card_y, card_x + card_w, card_y + 32), fill=BLUE)
d.text((card_x + 14, card_y + 8), "NOS PRESTATIONS", font=os_(10, True), fill=WHITE)
rows = [("Consultations gynécologiques", "Suivi annuel, dépistage, conseils.", True),
        ("Suivi de grossesse", "Échographies, surveillance, préparation…", True),
        ("Dépistage du cancer du col de l'utérus", "Frottis, test HPV.", False)]
for i, (t, s, on) in enumerate(rows):
    ry = card_y + 32 + i * 34
    d.line((card_x + 14, ry, card_x + card_w - 14, ry), fill=LINE)
    tick(card_x + 16, ry + 8, 17, on)
    d.text((card_x + 44, ry + 6), t, font=os_(11.5, True), fill=INK)
    d.text((card_x + 44 + 260, ry + 7), s, font=os_(10), fill=MUTE)
rr((card_x + 14, card_y + 138, card_x + 300, card_y + 166), 14, fill=WA)
wa_glyph(card_x + 26, card_y + 145, 14, WHITE)
d.text((card_x + 48, card_y + 142), "Envoyer ma liste sur WhatsApp", font=os_(11, True), fill=WHITE)

# right side of the section: the "how it goes" panel
px2 = card_x + card_w + 26
rr((px2, card_y, LX + LW - 26, card_y + 168), 12, fill=BLUE_D)
d.text((px2 + 18, card_y + 12), "EN CONFIANCE", font=os_(9, True), fill=(168, 224, 140))
d.text((px2 + 18, card_y + 28), "Une première consultation ?", font=mont(14), fill=WHITE)
for i, t in enumerate(["1. Vous dites ce qui vous amène",
                       "2. Le médecin examine et explique",
                       "3. Vous décidez de la suite"]):
    d.text((px2 + 18, card_y + 58 + i * 30), t, font=os_(12), fill=(232, 241, 251))

# ---------- phone
PX, PY, PW, PH = 1526, 396, 320, 620
shadow = Image.new('RGBA', (PW + 40, PH + 40), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((20, 10, PW + 20, PH + 30), 40, fill=(10, 30, 60, 255))
img.paste(shadow, (PX - 20, PY - 10), shadow)
rr((PX, PY, PX + PW, PY + PH), 30, fill=WHITE)
rr((PX + PW // 2 - 40, PY + 12, PX + PW // 2 + 40, PY + 30), 9, fill=(12, 34, 70))
d.rectangle((PX, PY + 40, PX + PW, PY + 60), fill=BLUE_D)
d.text((PX + 12, PY + 44), "Ouvert 24h/24 · 7j/7", font=os_(9), fill=(220, 233, 251))
cross_tile(PX + 14, PY + 72, 30)
d.text((PX + 52, PY + 74), "LA BÉTHANIE", font=mont(11, 800), fill=BLUE_D)
d.text((PX + 52, PY + 90), "MÉDICO-CHIRURGICAL · MATERNITÉ", font=os_(6.4, True), fill=MUTE)
rr((PX + PW - 60, PY + 74, PX + PW - 42, PY + 94), 10, fill=BLUE_D)
d.text((PX + PW - 56, PY + 77), "FR", font=os_(8, True), fill=WHITE)
d.text((PX + PW - 38, PY + 77), "EN", font=os_(8), fill=(150, 170, 200))
pim = photo.crop((int(photo.width * .34), int(photo.height * .10), photo.width, photo.height)).resize((PW - 32, 150))
pmm = Image.new('L', (PW - 32, 150), 0)
ImageDraw.Draw(pmm).rounded_rectangle((0, 0, PW - 32, 150), 14, fill=255)
img.paste(pim, (PX + 16, PY + 104), pmm)
d.text((PX + 18, PY + 264), "Votre santé intime,", font=mont(19), fill=BLUE_D)
d.text((PX + 18, PY + 290), "notre priorité.", font=mont(19), fill=BLUE)
rr((PX + 16, PY + 322, PX + PW - 16, PY + 356), 16, fill=WA)
wa_glyph(PX + 30, PY + 331, 14, WHITE)
d.text((PX + 54, PY + 329), "Prendre rendez-vous", font=os_(10.5, True), fill=WHITE)
rr((PX + 16, PY + 368, PX + PW - 16, PY + 392), 12, fill=TINT, outline=LINE)
d.text((PX + 26, PY + 372), "24h/24 · 7j/7  ·  Rue Mpondo", font=os_(8.5, True), fill=(44, 66, 98))
d.text((PX + 16, PY + 404), "NOS PRESTATIONS", font=os_(8.5, True), fill=BLUE)
for i, (t, on) in enumerate([("Consultations gynécologiques", True), ("Suivi de grossesse", True),
                             ("Dépistage du col de l'utérus", False), ("Suivi de la ménopause", False)]):
    ry = PY + 422 + i * 30
    d.line((PX + 16, ry, PX + PW - 16, ry), fill=LINE)
    tick(PX + 18, ry + 7, 16, on)
    d.text((PX + 42, ry + 5), t, font=os_(9.5, True) if on else os_(9.5), fill=INK if on else MUTE)
rr((PX + 16, PY + 546, PX + PW - 16, PY + 574), 14, fill=WA)
d.text((PX + 44, PY + 550), "Envoyer ma liste sur WhatsApp", font=os_(9.5, True), fill=WHITE)
d.rectangle((PX, PY + PH - 52, PX + PW, PY + PH), fill=WHITE)
rr((PX + 10, PY + PH - 44, PX + 176, PY + PH - 10), 16, fill=WA)
wa_glyph(PX + 22, PY + PH - 38, 14, WHITE)
d.text((PX + 44, PY + PH - 34), "WhatsApp", font=os_(11, True), fill=WHITE)
rr((PX + 186, PY + PH - 44, PX + PW - 10, PY + PH - 10), 16, outline=LINE, w=2)
d.text((PX + 236, PY + PH - 34), "Appeler", font=os_(11, True), fill=BLUE_D)

img = img.resize((1600, 900), Image.LANCZOS)
img.save(OUT, 'JPEG', quality=86, optimize=True)
print('wrote', OUT, round(OUT.stat().st_size / 1024), 'KB', img.size)
