# -*- coding: utf-8 -*-
"""JEMPO mockup — demos/shots/mockup-jempo-wa.jpg (1600x900).
Laptop + phone in the concept's own palette (espresso #2A211C / terracotta / sand),
real generated entrance photo, and — first build under the §20 rule — the FOOTER is
drawn visible on both screens (4 blocks + strip).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/home/user/AMK')
OUT = ROOT / 'demos/shots/mockup-jempo-wa.jpg'
FONTS = ROOT / 'content/assets/fonts'

def mont(s, weight=800):
    f = ImageFont.truetype(str(FONTS / 'Montserrat-ExtraBold.ttf'), s)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f

def os_(s, bold=False):
    return ImageFont.truetype(str(ROOT / 'tools/record/fonts' / ('OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf')), s)

INK = (42, 33, 28); INK2 = (74, 58, 49)
CLAY = (194, 84, 43); CLAY_D = (158, 63, 29); CLAY_L = (232, 168, 124)
SAND = (247, 241, 233); SAND2 = (238, 229, 217); WHITE = (255, 255, 255)
MUTE = (120, 104, 94); LINE = (226, 214, 200); WA = (11, 122, 62)
FOOT = (30, 23, 18)

W, H = 1920, 1080
img = Image.new('RGB', (W, H), SAND)
px = img.load()
for y in range(H):
    t = y / H
    row = tuple(int(SAND[i] + (SAND2[i] - SAND[i]) * t) for i in range(3))
    for x in range(W):
        px[x, y] = row
d = ImageDraw.Draw(img)

def rr(box, rad, fill=None, outline=None, w=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=w)

def wa_glyph(x, y, s, col):
    d.ellipse((x, y, x + s, y + s), outline=col, width=max(2, s // 7))
    d.line((x + s * .28, y + s * .62, x + s * .45, y + s * .5), fill=col, width=max(2, s // 8))
    d.line((x + s * .45, y + s * .5, x + s * .62, y + s * .58), fill=col, width=max(2, s // 8))

def door_icon(x, y, s, col, wd=3):
    d.arc((x, y + s * .35, x + s * .8, y + s * 1.35), 180, 360, fill=col, width=wd)
    d.line((x - s * .14, y + s * .85, x + s * .94, y + s * .85), fill=col, width=wd)
    d.ellipse((x + s * .58, y + s * .52, x + s * .66, y + s * .60), fill=col)

# ---------- header
d.ellipse((70, 78, 84, 92), fill=CLAY)
d.text((100, 68), "SITE CONCEPT  ·  J&E MEMORIAL POLYCLINIC (JEMPO)  ·  DEIDO, DOUALA", font=os_(17, True), fill=CLAY_D)
d.text((68, 104), "JEMPO", font=mont(58), fill=INK)
d.text((71, 186), "La porte d'entrée propre de la polyclinique — ORL · dermatologie · diabétologie · gynécologie", font=os_(22), fill=MUTE)
rr((70, 230, 800, 278), 24, fill=CLAY_D)
d.text((92, 242), "Aperçu préparé par AMK — en ligne en 3–5 jours", font=os_(16, True), fill=(255, 241, 231))
d.text((822, 244), "Premier aperçu construit avec le footer complet (§20).", font=os_(14), fill=MUTE)

# ---------- laptop
LX, LY, LW, LH = 250, 318, 1240, 706
rr((LX - 22, LY - 14, LX + LW + 22, LY + LH + 26), 20, fill=(24, 17, 13))
rr((LX - 22, LY + LH, LX + LW + 22, LY + LH + 26), 10, fill=(48, 37, 30))
rr((LX, LY, LX + LW, LY + LH), 10, fill=WHITE)
d.rectangle((LX, LY, LX + LW, LY + 36), fill=(238, 231, 221))
for i, c in enumerate([(248, 113, 113), (251, 191, 36), (52, 211, 153)]):
    d.ellipse((LX + 18 + i * 22, LY + 11, LX + 30 + i * 22, LY + 23), fill=c)
rr((LX + 110, LY + 6, LX + 520, LY + 30), 12, fill=WHITE, outline=LINE)
d.text((LX + 126, LY + 8), "concept-jempo-v1.vercel.app", font=os_(12), fill=MUTE)

y = LY + 36
d.rectangle((LX, y, LX + LW, y + 24), fill=INK)
d.text((LX + 18, y + 3), "Accueil ouvert 24h/24 · 7j/7 — Deido, Vallée Bessengue", font=os_(11), fill=(239, 229, 217))
d.text((LX + LW - 150, y + 3), "+237 696 71 06 99", font=os_(11, True), fill=WHITE)

y += 24
d.rectangle((LX, y, LX + LW, y + 52), fill=WHITE)
d.line((LX, y + 52, LX + LW, y + 52), fill=LINE)
door_icon(LX + 22, y + 12, 30, CLAY)
d.text((LX + 62, y + 10), "JEMPO", font=mont(14), fill=INK)
d.text((LX + 62, y + 28), "J&E MEMORIAL POLYCLINIC · DEIDO", font=os_(7.5, True), fill=MUTE)
for i, t in enumerate(["Consultations", "Accès", "Questions", "Contact"]):
    d.text((LX + 430 + i * 118, y + 18), t, font=os_(12), fill=INK)
rr((LX + LW - 232, y + 12, LX + LW - 168, y + 40), 14, fill=INK)
d.text((LX + LW - 218, y + 17), "FR", font=os_(12, True), fill=WHITE)
d.text((LX + LW - 192, y + 17), "EN", font=os_(12), fill=(160, 140, 128))
rr((LX + LW - 156, y + 11, LX + LW - 20, y + 41), 15, fill=WA)
d.text((LX + LW - 132, y + 16), "Rendez-vous", font=os_(12, True), fill=WHITE)

# hero row
hy = y + 52
hx = LX + 26
d.text((hx, hy + 14), "DEIDO · VALLÉE BESSENGUE — FACE HÔTEL LEWAT", font=os_(9, True), fill=CLAY_D)
d.text((hx, hy + 32), "Poussez la porte :", font=mont(28), fill=INK)
d.text((hx, hy + 68), "quatre spécialités, un seul endroit.", font=mont(28), fill=CLAY_D)
d.multiline_text((hx, hy + 112),
                 "ORL, dermatologie, diabétologie, gynécologie — les consultations de\n"
                 "spécialistes de JEMPO, leurs jours et leurs heures, et un rendez-vous\n"
                 "qui part sur WhatsApp en deux taps.",
                 font=os_(12), fill=(62, 49, 42), spacing=6)
rr((hx, hy + 176, hx + 200, hy + 210), 16, fill=WA)
wa_glyph(hx + 14, hy + 185, 15, WHITE)
d.text((hx + 36, hy + 183), "Choisir ma consultation", font=os_(11, True), fill=WHITE)
rr((hx + 212, hy + 176, hx + 330, hy + 210), 16, outline=LINE, w=2)
d.text((hx + 232, hy + 183), "Appeler la clinique", font=os_(11, True), fill=INK)
for i, t in enumerate(["24h/24 accueil", "4 spécialités", "MoMo · OM · espèces", "FR / EN"]):
    rr((hx + i * 152, hy + 222, hx + (i + 1) * 144, hy + 248), 13, fill=SAND, outline=LINE)
    d.text((hx + i * 152 + 10, hy + 228), t, font=os_(9), fill=(62, 49, 42))

photo = Image.open(ROOT / 'demos/img/jempo-hero.jpg').convert('RGB')
pw, ph = 470, 268
p2 = photo.resize((pw, ph))
mask = Image.new('L', (pw, ph), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), 20, fill=255)
img.paste(p2, (LX + LW - pw - 26, hy + 12), mask)
rr((LX + LW - pw - 12, hy + 12 + ph - 40, LX + LW - 38, hy + 12 + ph - 8), 12, fill=INK)
d.text((LX + LW - pw + 2, hy + 12 + ph - 35), "VOTRE PORTE — L'ENSEIGNE EST À REMPLIR", font=os_(8, True), fill=(247, 241, 233))

# reception strip
ry = hy + 268
d.rectangle((LX, ry, LX + LW, ry + 214), fill=INK)
d.text((hx, ry + 12), "LA RÉCEPTION", font=os_(9, True), fill=CLAY_L)
d.text((hx, ry + 26), "Vous cherchez quelle consultation ?", font=mont(15), fill=WHITE)
doors = [("ORL", "Dr Marcus Youda", True), ("Dermatologie", "Dr A. Njeumen", False),
         ("Diabétologie", "Dr Paul Djomaleu", False), ("Gynécologie", "Dr Humphry Neng", False)]
for i, (t, doc, on) in enumerate(doors):
    x = hx + i * 190
    rr((x, ry + 56, x + 180, ry + 128), 12, fill=CLAY_D if on else (60, 49, 42), outline=None if on else (86, 71, 61), w=2)
    d.ellipse((x + 158, ry + 66, x + 167, ry + 75), fill=WHITE if on else CLAY_L)
    d.text((x + 12, ry + 66), t, font=os_(11, True), fill=WHITE)
    d.text((x + 12, ry + 82), doc, font=os_(9.5), fill=(251, 227, 212) if on else (205, 191, 178))
    d.text((x + 12, ry + 100), "Lun–Ven 08:00–17:30" if i == 0 else ("Lun–Ven 14:00–16:00" if i == 1 else ("Lun–Ven 13:00–15:00" if i == 2 else "Lun–Ven 16:00–20:00")),
           font=os_(8), fill=(246, 207, 185) if on else (183, 167, 154))
# selected panel
pxx = hx + 4 * 190 + 8
rr((pxx, ry + 56, LX + LW - 26, ry + 200), 12, fill=(58, 47, 40), outline=(86, 71, 61), w=2)
d.text((pxx + 16, ry + 66), "ORL", font=mont(12), fill=WHITE)
d.text((pxx + 16, ry + 86), "Dr Marcus Youda — oto-rhino-laryngologiste", font=os_(10), fill=(216, 204, 192))
d.line((pxx + 16, ry + 104, LX + LW - 42, ry + 104), fill=(86, 71, 61))
d.text((pxx + 16, ry + 112), "CONSULTATIONS", font=os_(8, True), fill=CLAY_L)
d.text((pxx + 130, ry + 112), "Lun–Ven 08:00–17:30 · Sam 08:00–13:00", font=os_(10), fill=(239, 229, 217))
d.line((pxx + 16, ry + 132, LX + LW - 42, ry + 132), fill=(86, 71, 61))
d.text((pxx + 16, ry + 140), "MOTIFS FRÉQUENTS", font=os_(8, True), fill=CLAY_L)
d.text((pxx + 130, ry + 140), "Nez, gorge, otites, audition…", font=os_(10), fill=(239, 229, 217))
rr((pxx + 16, ry + 162, pxx + 216, ry + 192), 12, fill=CLAY_D)
wa_glyph(pxx + 28, ry + 171, 14, WHITE)
d.text((pxx + 50, ry + 169), "Demander ce rendez-vous", font=os_(10, True), fill=WHITE)
d.text((pxx + 232, ry + 170), "ou appeler la clinique", font=os_(10), fill=(200, 186, 174))

# ---------- footer (first §20 build — drawn, 4 blocks + strip)
fy = ry + 214
d.rectangle((LX, fy, LX + LW, fy + 148), fill=FOOT)
d.text((hx, fy + 14), "J&E MEMORIAL POLYCLINIC", font=mont(13), fill=WHITE)
d.text((hx, fy + 34), "Polyclinique à Deido, Douala : consultations", font=os_(9), fill=(183, 167, 154))
d.text((hx, fy + 47), "de spécialistes sur rendez-vous, accueil 24/7.", font=os_(9), fill=(183, 167, 154))
d.text((hx + 330, fy + 14), "SUR CETTE PAGE", font=os_(8, True), fill=CLAY_L)
for i, t in enumerate(["Consultations", "Accès", "Questions fréquentes", "Contact"]):
    d.text((hx + 330, fy + 30 + i * 15), t, font=os_(9), fill=(239, 229, 217))
rr((hx + 520, fy + 14, hx + 780, fy + 96), 12, fill=CLAY_D)
d.text((hx + 536, fy + 24), "Prenez rendez-vous : dites-nous la", font=os_(9), fill=(255, 241, 231))
d.text((hx + 536, fy + 37), "spécialité, on répond sur WhatsApp.", font=os_(9), fill=(255, 241, 231))
rr((hx + 536, fy + 56, hx + 700, fy + 84), 10, fill=WHITE)
wa_glyph(hx + 546, fy + 63, 14, CLAY_D)
d.text((hx + 566, fy + 62), "Rendez-vous WhatsApp", font=os_(9, True), fill=CLAY_D)
d.text((hx + 800, fy + 14), "NOUS JOINDRE", font=os_(8, True), fill=CLAY_L)
d.text((hx + 800, fy + 30), "+237 696 71 06 99", font=os_(9, True), fill=(239, 229, 217))
d.text((hx + 800, fy + 43), "670 85 85 42 · 233 47 87 69", font=os_(9), fill=(239, 229, 217))
d.text((hx + 800, fy + 56), "1 149 Bd de la République, Deido", font=os_(9), fill=(239, 229, 217))
d.text((hx + 800, fy + 69), "face hôtel LEWAT · 24h/24", font=os_(9), fill=(239, 229, 217))
d.line((hx, fy + 108, LX + LW - 26, fy + 108), fill=(70, 57, 48))
d.text((hx, fy + 118), "© 2026 J&E Memorial Polyclinic (JEMPO) — aperçu préparé par AMK, pas encore en ligne", font=os_(8), fill=(169, 150, 138))
d.text((LX + LW - 130, fy + 118), "Retour en haut ↑", font=os_(8), fill=(216, 204, 192))

# ---------- phone
PX, PY, PW, PH = 1524, 392, 322, 624
shadow = Image.new('RGBA', (PW + 40, PH + 40), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle((20, 10, PW + 20, PH + 30), 40, fill=(24, 17, 13, 255))
img.paste(shadow, (PX - 20, PY - 10), shadow)
rr((PX, PY, PX + PW, PY + PH), 28, fill=WHITE)
rr((PX + PW // 2 - 38, PY + 11, PX + PW // 2 + 38, PY + 28), 9, fill=(30, 23, 18))
d.rectangle((PX, PY + 38, PX + PW, PY + 56), fill=INK)
d.text((PX + 12, PY + 41), "Accueil 24h/24 · 7j/7", font=os_(8), fill=(239, 229, 217))
door_icon(PX + 14, PY + 66, 24, CLAY)
d.text((PX + 46, PY + 68), "JEMPO", font=mont(11), fill=INK)
d.text((PX + 46, PY + 82), "J&E MEMORIAL POLYCLINIC", font=os_(6), fill=MUTE)
rr((PX + PW - 58, PY + 68, PX + PW - 42, PY + 86), 9, fill=INK)
d.text((PX + PW - 55, PY + 71), "FR", font=os_(7.5, True), fill=WHITE)
d.text((PX + PW - 38, PY + 71), "EN", font=os_(7.5), fill=(160, 140, 128))
pim = photo.resize((PW - 32, 118))
pmm = Image.new('L', (PW - 32, 118), 0)
ImageDraw.Draw(pmm).rounded_rectangle((0, 0, PW - 32, 118), 14, fill=255)
img.paste(pim, (PX + 16, PY + 96), pmm)
d.text((PX + 18, PY + 226), "Poussez la porte :", font=mont(16), fill=INK)
d.text((PX + 18, PY + 248), "quatre spécialités.", font=mont(16), fill=CLAY_D)
d.text((PX + 18, PY + 274), "LA RÉCEPTION", font=os_(7.5, True), fill=CLAY_D)
for i, (t, on) in enumerate([("ORL", True), ("Dermatologie", False), ("Diabétologie", False), ("Gynécologie", False)]):
    x = PX + 16 + (i % 2) * 150
    y2 = PY + 288 + (i // 2) * 40
    rr((x, y2, x + 142, y2 + 34), 9, fill=CLAY_D if on else WHITE, outline=None if on else LINE, w=2)
    d.text((x + 10, y2 + 6), t, font=os_(9.5, True), fill=WHITE if on else INK)
    d.text((x + 10, y2 + 19), "8h–17h30" if on else "14h–16h" if i == 1 else "13h–15h" if i == 2 else "16h–20h",
           font=os_(7.5), fill=(251, 227, 212) if on else MUTE)
rr((PX + 16, PY + 372, PX + PW - 16, PY + 448), 10, fill=(247, 241, 233), outline=LINE)
d.text((PX + 26, PY + 380), "Dr Marcus Youda — ORL", font=os_(9.5, True), fill=INK)
d.text((PX + 26, PY + 396), "Lun–Ven 08:00–17:30 · Sam 08:00–13:00", font=os_(8), fill=(62, 49, 42))
d.text((PX + 26, PY + 410), "Nez, gorge, otites, audition…", font=os_(8), fill=(62, 49, 42))
rr((PX + 26, PY + 424, PX + PW - 26, PY + 444), 10, fill=CLAY_D)
d.text((PX + 78, PY + 427), "Demander ce rendez-vous", font=os_(8.5, True), fill=WHITE)
rr((PX + 16, PY + 458, PX + PW - 16, PY + 490), 12, fill=WA)
wa_glyph(PX + 28, PY + 466, 14, WHITE)
d.text((PX + 50, PY + 464), "Rendez-vous WhatsApp", font=os_(9.5, True), fill=WHITE)
# compact footer on the phone
d.rectangle((PX, PY + 498, PX + PW, PY + PH - 46), fill=FOOT)
d.text((PX + 14, PY + 506), "J&E MEMORIAL POLYCLINIC", font=mont(9), fill=WHITE)
d.text((PX + 14, PY + 520), "Deido, Douala · accueil 24h/24", font=os_(7.5), fill=(183, 167, 154))
d.text((PX + 14, PY + 533), "+237 696 71 06 99", font=os_(7.5, True), fill=(239, 229, 217))
rr((PX + 14, PY + 546, PX + PW - 14, PY + 570), 9, fill=CLAY_D)
d.text((PX + 60, PY + 549), "Prendre rendez-vous", font=os_(8.5, True), fill=WHITE)
d.text((PX + 14, PY + 574), "© 2026 — aperçu AMK", font=os_(7), fill=(169, 150, 138))
d.text((PX + PW - 90, PY + 574), "Haut ↑", font=os_(7), fill=(216, 204, 192))
d.rectangle((PX, PY + PH - 46, PX + PW, PY + PH), fill=WHITE)
rr((PX + 10, PY + PH - 40, PX + 176, PY + PH - 8), 14, fill=WA)
wa_glyph(PX + 22, PY + PH - 34, 14, WHITE)
d.text((PX + 44, PY + PH - 30), "WhatsApp", font=os_(11, True), fill=WHITE)
rr((PX + 186, PY + PH - 40, PX + PW - 10, PY + PH - 8), 14, outline=LINE, w=2)
d.text((PX + 236, PY + PH - 30), "Appeler", font=os_(11, True), fill=INK)

img = img.resize((1600, 900), Image.LANCZOS)
img.save(OUT, 'JPEG', quality=86, optimize=True)
print('wrote', OUT, round(OUT.stat().st_size / 1024), 'KB', img.size)
