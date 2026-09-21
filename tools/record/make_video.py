# -*- coding: utf-8 -*-
"""AMK founding-clients TikTok/IG video builder.

Renders 1080x1920 (9:16), 30 fps, silent MP4s with PIL frames piped to a
static ffmpeg binary (imageio-ffmpeg). No headless browser is available in
the sandbox (Chromium download hosts blocked), so this composites the REAL
AMK mockup artwork (demos/shots/mockup-*-wa.jpg) with designed motion:
listing-card hook -> mockup reveal -> feature lines -> bilingual/3G phone
pan -> WhatsApp conversation -> founding-clients CTA.

Usage:
  python3 tools/record/make_video.py [clinic|school|all] [en|fr|all]
Output: sales/social/videos/<kind>-founding-<lang>.mp4
Silent by design: King adds trending TikTok/IG sound in-app; captions
carry every message. Re-run after changing copy/assets.
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(ROOT, "sales", "social", "videos")
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
W, H, FPS = 1080, 1920, 30

NAVY = (15, 42, 71)
NAVY_D = (8, 24, 44)
TEAL = (14, 122, 92)
GOLD = (201, 146, 59)
CREAM = (250, 248, 242)
WHITE = (255, 255, 255, 255)
GREY = (120, 132, 146)
DARK = (26, 32, 51)
RED = (212, 66, 66)
GREEN = (37, 171, 96)
LIGHT_GREY = (238, 240, 243)

def _font(size, bold=False, italic=False):
    name = "OpenSans-Bold.ttf" if bold else ("OpenSans-Italic.ttf" if italic else "OpenSans-Regular.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

class FontCache(dict):
    def __init__(self, bold): super().__init__(); self.bold = bold
    def __missing__(self, s):
        f = _font(s, self.bold); self[s] = f; return f
F, FB = FontCache(False), FontCache(True)

def ease(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w: cur = trial
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def rr(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def star_points(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(n * 2):
        a = -math.pi / 2 + i * math.pi / n
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def base(color=CREAM): return Image.new("RGB", (W, H), color)

def amk_lockup(d, x, y, color=(255, 255, 255), scale=1.0):
    s = scale
    rr(d, [x, y, x + int(64*s), y + int(64*s)], int(12*s), fill=GOLD)
    d.text((x + int(17*s), y + int(6*s)), "A", font=FB[int(40*s)], fill=NAVY_D)
    d.text((x + int(80*s), y + int(2*s)), "AMK", font=FB[int(34*s)], fill=color)
    d.text((x + int(80*s), y + int(38*s)), "Web Development & Digital Solutions",
           font=F[int(18*s)], fill=color)

def caption_band(img, text, lang):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    bh = 300
    od.rectangle([0, H - bh, W, H], fill=(8, 20, 36, 200))
    img = img.convert("RGBA"); img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    lines = wrap(d, text, FB[52], W - 120)
    y = H - bh + 54
    for ln in lines[:3]:
        d.text((60, y), ln, font=FB[52], fill=WHITE); y += 74
    return img.convert("RGB")

MOCK_FULL_CACHE = {}
def mock_image(path):
    if path not in MOCK_FULL_CACHE:
        im = Image.open(path).convert("RGB")
        MOCK_FULL_CACHE[path] = im.crop((0, 208, im.width, min(880, im.height)))
    return MOCK_FULL_CACHE[path]

def contain(src, w, h, zoom=1.0, bg=(255, 255, 255), cx=0.5):
    iw, ih = src.size
    s = min(w / iw, h / ih) * zoom
    nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
    im = src.resize((nw, nh), Image.LANCZOS)
    panel = Image.new("RGB", (w, h), bg)
    if nw <= w:
        panel.paste(im, ((w - nw) // 2, (h - nh) // 2)); return panel
    ox = max(0, min(int((nw - w) * cx), nw - w))
    panel.paste(im.crop((ox, 0, ox + w, nh)), (0, (h - nh) // 2))
    return panel

# ---------- glyph icons ----------
def icon_nav(cd, cx, cy, col=NAVY):
    cd.ellipse([cx-23, cy-23, cx+23, cy+23], fill=col)
    cd.polygon([(cx-9, cy+10), (cx+11, cy-11), (cx+1, cy+2)], fill=WHITE)

def icon_phone(cd, cx, cy, col=NAVY):
    cd.ellipse([cx-23, cy-23, cx+23, cy+23], fill=col)
    cd.polygon([(cx-11, cy-5), (cx-6, cy-13), (cx+2, cy-6), (cx+10, cy+2),
                (cx+5, cy+11), (cx-4, cy+9), (cx-12, cy+2)], fill=WHITE)

def icon_web(cd, cx, cy, col=GREY):
    cd.ellipse([cx-21, cy-21, cx+21, cy+21], outline=col, width=4)
    cd.ellipse([cx-10, cy-21, cx+10, cy+21], outline=col, width=3)
    cd.line([cx-20, cy, cx+20, cy], fill=col, width=3)
    cd.line([cx-26, cy+24, cx+26, cy-24], fill=RED, width=7)

def wa_phone(od, cx, cy, r, bg, fg):
    od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fg)
    od.polygon([(cx-r*0.45, cy+r*0.12), (cx-r*0.22, cy-r*0.05), (cx+r*0.12, cy+r*0.28),
                (cx+r*0.48, cy+r*0.62), (cx+r*0.26, cy+r*1.0), (cx-r*0.14, cy+r*0.9),
                (cx-r*0.5, cy+r*0.6)], fill=bg)

# ---------- scenes ----------
def scene_maps(p, lang, C):
    img = base(NAVY); d = ImageDraw.Draw(img)
    t = ease(p / 0.9)
    for i, ln in enumerate(wrap(d, C["hook"][0 if lang == "en" else 1], FB[64], W - 140)):
        d.text((70, 130 + i * 80), ln, font=FB[64], fill=WHITE)
    cw, ch = 900, 760
    cy0 = 470
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    rr(cd, [0, 0, cw, ch], 36, fill=WHITE)
    cd.ellipse([48, 48, 104, 104], fill=(220, 233, 245))
    cd.polygon(star_points(76, 76, 26, 11), fill=GOLD)
    cd.text((132, 46), C["card_name"], font=FB[38], fill=DARK)
    cd.text((132, 102), C["card_sub"][0 if lang == "en" else 1], font=F[30], fill=GREY)
    for i in range(5): cd.polygon(star_points(72 + i*52, 190, 21, 9), fill=GOLD)
    cd.text((70 + 5*52 + 18, 164), C["card_rating"], font=FB[32], fill=DARK)
    cd.text((70, 236), C["card_open"][0 if lang == "en" else 1], font=F[30], fill=TEAL)
    cd.line([60, 300, cw-60, 300], fill=LIGHT_GREY, width=3)
    actions = C["card_actions"][0 if lang == "en" else 1]
    xs = [110, 110 + cw//3, 110 + 2*cw//3]
    for i, lab in enumerate(actions):
        icx = xs[i] + 8
        if i == 0: icon_nav(cd, icx, 360)
        elif i == 1: icon_phone(cd, icx, 360)
        else: icon_web(cd, icx, 360)
        tw = cd.textlength(lab, font=F[28])
        cd.text((icx - tw/2, 400), lab, font=F[28], fill=GREY if i == 2 else NAVY)
    a = ease((p - 0.42) / 0.4)
    if a > 0:
        bw, by = 320, 500; bx = (cw - bw)//2
        rr(cd, [bx, by, bx+bw, by+84], 42, fill=(212, 66, 66, int(255*a)))
        bt = ("NO WEBSITE", "AUCUN SITE")
        tw = cd.textlength(bt[0 if lang == "en" else 1], font=FB[36])
        cd.text((bx + (bw-tw)/2, by+18), bt[0 if lang=="en" else 1], font=FB[36], fill=WHITE)
        for i, ln in enumerate(wrap(cd, C["hook_sub"][0 if lang=="en" else 1], F[30], cw-140)):
            cd.text((70, 628 + i*40), ln, font=F[30], fill=GREY)
    if t < 1: card.putalpha(card.getchannel("A").point(lambda v: int(v*t)))
    img.paste(card, ((W-cw)//2, cy0), card)
    return img

def scene_mock(p, lang, C, caption, focus=0.5, zoom_end=1.05, tint=NAVY, bg=(238, 241, 235)):
    img = base(tint)
    z = max(1.0, zoom_end - 0.05) + 0.05 * ease(p)
    m = contain(mock_image(C["mock"]), 1000, 640, zoom=z, bg=bg, cx=focus)
    sh = Image.new("RGBA", (1040, 680), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([0, 0, 1040, 680], radius=28, fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    img.paste(sh, (22, 548), sh)
    card = Image.new("RGBA", (1040, 680), WHITE); card.paste(m, (20, 20))
    img.paste(card, (20, 530), card)
    d = ImageDraw.Draw(img)
    amk_lockup(d, 64, 130, color=(220, 230, 240))
    d.line([64, 230, 280, 230], fill=GOLD, width=5)
    d.text((64, 280), C["reveal_head"][0 if lang=="en" else 1], font=FB[56], fill=WHITE)
    return caption_band(img, caption[0 if lang=="en" else 1], lang)

def scene_features(p, lang, C):
    img = base(NAVY_D); d = ImageDraw.Draw(img)
    title = C["feat_title"][0 if lang=="en" else 1]
    y = 220
    for ln in wrap(d, title, FB[52], W-140):
        d.text((70, y), ln, font=FB[52], fill=WHITE); y += 72
    items = C["features"][0 if lang=="en" else 1]
    iy = 520
    for i, it in enumerate(items):
        a = ease((p - i*0.16) / 0.32)
        if a <= 0: continue
        bw, x0 = 900, (W-900)//2
        card = Image.new("RGBA", (bw, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        rr(cd, [0, 0, bw, 150], 24, fill=(255, 255, 255, int(255*a)))
        cd.ellipse([34, 39, 106, 111], fill=TEAL + (255,))
        cd.line([54, 78, 72, 96], fill=WHITE, width=8)
        cd.line([72, 96, 104, 58], fill=WHITE, width=8)
        lns = wrap(cd, it, FB[36], 720)
        ty = 75 - 22*(len(lns)-1)
        for ln in lns: cd.text((132, ty), ln, font=FB[36], fill=DARK); ty += 50
        img.paste(card, (x0, iy), card); iy += 190
    a = ease((p - 0.6) / 0.3)
    if a > 0:
        bh, y0 = 110, 1180
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        txt = C["feat_button"][0 if lang=="en" else 1]
        tw = od.textlength(txt, font=FB[40])
        bw = max(600, int(tw) + 150)
        pulse = 1 + 0.04 * math.sin(p * 2 * math.pi * 3)
        bw2, bh2 = int(bw*pulse), int(bh*pulse)
        x0p = (W-bw2)//2
        rr(od, [x0p, y0-8, x0p+bw2, y0+bh2-8], 55, fill=GREEN + (int(255*a),))
        grp = 42 + 18 + tw
        gx = (W - grp) / 2
        wa_phone(od, int(gx + 21), y0+47, 21, GREEN + (int(255*a),), (255, 255, 255, int(255*a)))
        od.text((gx + 60, y0+30), txt, font=FB[40], fill=(255,255,255,int(255*a)))
        img = img.convert("RGBA"); img.alpha_composite(ov); img = img.convert("RGB")
    return img

def scene_chat(p, lang, C):
    img = base((235, 239, 236)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 170], fill=GREEN)
    d.ellipse([50, 46, 122, 118], fill=(200, 224, 210))
    d.text((74, 58), C["chat_avatar"], font=FB[44], fill=GREEN)
    d.text((146, 44), C["chat_title"][0 if lang=="en" else 1], font=FB[32], fill=WHITE)
    d.text((146, 96), "online", font=F[28], fill=(210, 240, 222))
    def bubble(y, text, mine=False, ap=0.0):
        a = ease(ap)
        if a <= 0: return y
        lns = wrap(d, text, F[36], 620)
        bw = max(d.textlength(ln, font=F[36]) for ln in lns) + 56
        bh = len(lns)*48 + 40
        x0 = W - 60 - bw if mine else 60
        col = (213, 245, 227) if mine else (255, 255, 255)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        rr(od, [x0, y, x0+bw, y+bh], 26, fill=col + (int(255*a),))
        ty = y + 20
        for ln in lns:
            od.text((x0+28, ty), ln, font=F[36], fill=DARK + (int(255*a),)); ty += 48
        out = img.convert("RGBA"); out.alpha_composite(ov); img.paste(out.convert("RGB"))
        return y + bh + 34
    msgs = C["chat"][0 if lang=="en" else 1]
    y2 = 260
    for i, (mine, txt) in enumerate(msgs):
        y2 = bubble(y2, txt, mine, (p - 0.05 - i*0.24) / 0.3)
    return caption_band(img, C["chat_caption"][0 if lang=="en" else 1], lang)

def scene_cta(p, lang, C):
    img = base(NAVY_D); d = ImageDraw.Draw(img)
    amk_lockup(d, (W-360)//2, 220, color=WHITE, scale=1.4)
    d.line([W//2-90, 360, W//2+90, 360], fill=GOLD, width=6)
    y = 470
    for ln in wrap(d, C["cta_head"][0 if lang=="en" else 1], FB[60], W-120):
        tw = d.textlength(ln, font=FB[60]); d.text(((W-tw)/2, y), ln, font=FB[60], fill=GOLD); y += 84
    y += 30
    for i, b in enumerate(C["cta_bullets"][0 if lang=="en" else 1]):
        ba = ease((p - 0.22 - i*0.12) / 0.3)
        if ba <= 0: y += 150; continue
        d.ellipse([92, y+8, 132, y+48], fill=TEAL)
        d.line([102, y+29, 113, y+40], fill=WHITE, width=5)
        d.line([113, y+40, 126, y+18], fill=WHITE, width=5)
        lns = wrap(d, b, FB[36], W-240)
        for j, ln in enumerate(lns): d.text((156, y+j*48), ln, font=FB[36], fill=WHITE)
        y += 52*len(lns) + 60
    pa = ease((p - 0.7) / 0.3)
    if pa > 0:
        bw, bh, y0 = 460, 116, 1430
        ov = Image.new("RGBA", (W, H), (0,0,0,0)); od = ImageDraw.Draw(ov)
        rr(od, [(W-bw)//2, y0, (W+bw)//2, y0+bh], 58, fill=(255,255,255,int(255*pa)))
        t1 = 'DM  "%s"' % C["keyword"]
        tw = od.textlength(t1, font=FB[48])
        od.text(((W-tw)/2, y0+28), t1, font=FB[48], fill=NAVY_D + (int(255*pa),))
        img = img.convert("RGBA"); img.alpha_composite(ov); img = img.convert("RGB"); d = ImageDraw.Draw(img)
        foot = C["cta_foot"][0 if lang=="en" else 1]
        tw = d.textlength(foot, font=F[32]); d.text(((W-tw)/2, 1610), foot, font=F[32], fill=(180,196,214))
        tw = d.textlength("amk-cm.vercel.app", font=FB[32]); d.text(((W-tw)/2, 1670), "amk-cm.vercel.app", font=FB[32], fill=GOLD)
    return img

# ---------- configs ----------
CLINIC = {
    "mock": os.path.join(ROOT, "demos", "shots", "mockup-clinic-wa.jpg"),
    "hook": ("A clinic with 53 Google reviews…", "Un cabinet avec 53 avis Google…"),
    "hook_sub": ("…and no website for patients to open.", "…et aucun site web à ouvrir pour les patients."),
    "card_name": "Excellence Medical Clinic",
    "card_sub": ("Clinic · Laboratory · Douala", "Cabinet · Laboratoire · Douala"),
    "card_rating": "4.7 (53)",
    "card_open": ("Open · Closes 18:00", "Ouvert · Ferme à 18 h"),
    "card_actions": (["Directions", "Call", "Website"], ["Itinéraire", "Appeler", "Site web"]),
    "reveal_head": ("What patients should find instead:", "Ce que les patients devraient trouver :"),
    "cap1": ("So I built what their patients actually look for.", "J'ai construit ce que leurs patients cherchent vraiment."),
    "feat_title": ("Everything patients need, on the phone:", "Tout ce qu'il faut aux patients, sur le téléphone :"),
    "features": (["Transparent FCFA prices & service list", "Same-day laboratory results", "WhatsApp appointments in one tap"],
                 ["Prix FCFA et prestations affichés", "Résultats de laboratoire le jour même", "Rendez-vous WhatsApp en un clic"]),
    "feat_button": ("Book on WhatsApp", "Prendre RDV sur WhatsApp"),
    "cap2": ("Bilingual EN | FR — fast on any 3G phone.", "Bilingue EN | FR — rapide sur n'importe quel téléphone en 3G."),
    "chat_avatar": "C",
    "chat_title": ("New patient", "Nouveau patient"),
    "chat": ([(False, "Hello! Do you have an appointment slot today?"),
              (True, "Yes — 14:30 is free. Tap to book, we'll confirm here. ✓"),
              (False, "Perfect, booking it. Thank you!")],
             [(False, "Bonjour ! Une place de rendez-vous aujourd'hui ?"),
              (True, "Oui — 14 h 30 est libre. Cliquez pour réserver."),
              (False, "Parfait, je réserve. Merci !")]),
    "chat_caption": ("Bookings arrive on WhatsApp — zero missed calls.",
                     "Les rendez-vous arrivent sur WhatsApp — zéro appel manqué."),
    "cta_head": ("Only 2 founding clients this month.", "Seulement 2 clients fondateurs ce mois-ci."),
    "cta_bullets": (["Your bilingual website preview is built first — free",
                     "You pay 100 000 F only if you keep it",
                     "Clinics & labs · live in 3–5 days"],
                    ["Votre aperçu de site bilingue est construit d'abord — gratuit",
                     "Vous payez 100 000 F seulement si vous le gardez",
                     "Cliniques & laboratoires · en ligne en 3–5 jours"]),
    "cta_foot": ("WhatsApp +237 677 78 96 31  ·  link in bio", "WhatsApp +237 677 78 96 31  ·  lien dans la bio"),
    "keyword": "CLINIC",
}
SCHOOL = {
    "mock": os.path.join(ROOT, "demos", "shots", "mockup-secondary-wa.jpg"),
    "hook": ("A boarding college parents abroad Google…", "Un internat que les parents de la diaspora cherchent…"),
    "hook_sub": ("…with no official website to show them.", "…sans site officiel à leur montrer."),
    "card_name": "Bright Future Bilingual College",
    "card_sub": ("Secondary · Boarding · Buea", "Secondaire · Internat · Buéa"),
    "card_rating": "4.6 (38)",
    "card_open": ("Admissions open · Forms 1–5", "Inscriptions ouvertes · Formes 1–5"),
    "card_actions": (["Directions", "Call", "Website"], ["Itinéraire", "Appeler", "Site web"]),
    "reveal_head": ("What parents should find instead:", "Ce que les parents devraient trouver :"),
    "cap1": ("So I built what parents actually look for.", "J'ai construit ce que les parents cherchent vraiment."),
    "feat_title": ("Everything a parent checks before paying:", "Tout ce qu'un parent vérifie avant de payer :"),
    "features": (["Transparent FCFA fees & boarding packages", "GCE results & Student Corner online", "Admissions on WhatsApp, EN | FR"],
                 ["Frais FCFA et forfaits internat affichés", "Résultats GCE & Espace Élèves en ligne", "Inscriptions sur WhatsApp, EN | FR"]),
    "feat_button": ("Start admission", "Demander une inscription"),
    "cap2": ("GCE results & admissions — bilingual, 3G-fast.", "Résultats GCE & inscriptions — bilingue, rapide en 3G."),
    "chat_avatar": "P",
    "chat_title": ("Parent", "Parent"),
    "chat": ([(False, "Hello! Do you still have Form One boarding places?"),
              (True, "Yes — send the child's name and class here; we book the placement assessment."),
              (False, "Thank you, sending it now!")],
             [(False, "Bonjour ! Reste-t-il des places en internat en Form One ?"),
              (True, "Oui — envoyez le nom et la classe de l'enfant ici ; nous réservons le test."),
              (False, "Merci, j'envoie tout de suite !")]),
    "chat_caption": ("Admissions on WhatsApp — for parents at home or abroad.",
                     "Les inscriptions sur WhatsApp — au pays comme à l'étranger."),
    "cta_head": ("Only 2 founding clients this month.", "Seulement 2 clients fondateurs ce mois-ci."),
    "cta_bullets": (["Your bilingual college website preview is built first — free",
                     "You pay 100 000 F only if you keep it",
                     "Lay-private colleges · live in 3–5 days"],
                    ["L'aperçu bilingue du site de votre collège est construit d'abord — gratuit",
                     "Vous payez 100 000 F seulement si vous le gardez",
                     "Collèges privés laïcs · en ligne en 3–5 jours"]),
    "cta_foot": ("WhatsApp +237 677 78 96 31  ·  link in bio", "WhatsApp +237 677 78 96 31  ·  lien dans la bio"),
    "keyword": "SCHOOL",
}
CONFIGS = {"clinic": CLINIC, "school": SCHOOL}

def build_scenes(C):
    return [
        (0.0, 4.2, lambda p, l: scene_maps(p, l, C)),
        (4.2, 10.0, lambda p, l: scene_mock(p, l, C, C["cap1"], focus=0.5, zoom_end=1.0, tint=NAVY, bg=(234, 238, 232))),
        (10.0, 15.2, lambda p, l: scene_features(p, l, C)),
        (15.2, 19.8, lambda p, l: scene_mock(p, l, C, C["cap2"], focus=0.86, zoom_end=1.55, tint=NAVY_D, bg=(234, 238, 232))),
        (19.8, 24.6, lambda p, l: scene_chat(p, l, C)),
        (24.6, 29.2, lambda p, l: scene_cta(p, l, C)),
    ]

def render_frame(t, lang, scenes, dur):
    for i, (s, e, fn) in enumerate(scenes):
        if t < e or i == len(scenes) - 1:
            p = max(0.0, min(1.0, (t - s) / (e - s)))
            img = fn(p, lang)
            if t - s < 0.18:
                img = Image.blend(base(NAVY_D), img, (t - s) / 0.18)
            elif e - t < 0.18 and i != len(scenes) - 1:
                img = Image.blend(base(NAVY_D), img, (e - t) / 0.18)
            return img

def make(kind, lang):
    import imageio_ffmpeg
    C = CONFIGS[kind]; scenes = build_scenes(C); dur = scenes[-1][1]
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, "%s-founding-%s.mp4" % (kind, lang))
    cmd = [ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-profile:v", "high",
           "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", out]
    n = int(dur * FPS)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(n):
        proc.stdin.write(render_frame(i / FPS, lang, scenes, dur).tobytes())
    proc.stdin.close(); rc = proc.wait()
    print(("OK " if rc == 0 else "FAIL rc=%d " % rc) + out + (" %.1f MB" % (os.path.getsize(out)/1e6) if rc == 0 else ""))
    return rc

if __name__ == "__main__":
    kinds = ["clinic", "school"] if (len(sys.argv) < 2 or sys.argv[1] == "all") else [sys.argv[1]]
    langarg = sys.argv[2] if len(sys.argv) > 2 else "all"
    langs = ["en", "fr"] if langarg == "all" else [langarg]
    for k in kinds:
        for l in langs: make(k, l)
