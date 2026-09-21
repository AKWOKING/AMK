# -*- coding: utf-8 -*-
"""Build site/img/og-cover.jpg — 1200x630 social share card (WhatsApp/FB/Twitter/LinkedIn)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).parent
FONTS = HERE.parent.parent / "tools" / "record" / "fonts"
W, H = 1200, 630

NAVY = (15, 23, 42)
NAVY2 = (30, 41, 59)
NAVY3 = (51, 65, 85)
AMBER = (245, 158, 11)
AMBER_L = (252, 211, 77)
WHITE = (255, 255, 255)
SLATE = (148, 163, 184)

def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)

img = Image.new("RGB", (W, H), NAVY)
glow = Image.new("RGB", (W, H), NAVY)
ImageDraw.Draw(glow).ellipse((650, -350, 1500, 500), fill=(30, 27, 18))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.blend(img, glow, 0.55)
d = ImageDraw.Draw(img)

# --- mark ---
cx, cy, r = 90, 92, 34
d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=AMBER, width=3)
d.line((cx, cy-r*0.82, cx, cy+r*0.65), fill=AMBER_L, width=4)
d.line((cx, cy, cx-r*0.82, cy+r*0.82), fill=AMBER_L, width=4)
d.line((cx, cy, cx+r*0.82, cy+r*0.82), fill=AMBER_L, width=4)
for (dx, dy) in ((0, -r*0.82), (-r*0.82, r*0.82), (r*0.82, r*0.82)):
    d.ellipse((cx+dx-4, cy+dy-4, cx+dx+4, cy+dy+4), fill=AMBER)
d.text((140, 64), "AMK", font=font("OpenSans-Bold.ttf", 40), fill=WHITE)
d.text((141, 112), "WEB DEVELOPMENT & DIGITAL SOLUTIONS", font=font("OpenSans-Bold.ttf", 15), fill=SLATE)

# --- headline (left column ends x=700) ---
LX = 66
f_h = font("OpenSans-Bold.ttf", 52)
d.text((LX, 200), "Bilingual websites", font=f_h, fill=WHITE)
d.text((LX, 266), "for Cameroon schools", font=f_h, fill=AMBER_L)
d.text((LX, 332), "& clinics.", font=f_h, fill=AMBER_L)
d.text((LX+2, 404), "Sites web bilingues — écoles & cliniques", font=font("OpenSans-Regular.ttf", 24), fill=SLATE)

# --- value chips (two rows, confined to the left column) ---
f_chip = font("OpenSans-Bold.ttf", 20)
def chip(x, y, text):
    tw = d.textlength(text, font=f_chip)
    d.rounded_rectangle((x, y, x+tw+36, y+42), radius=21, outline=NAVY3, width=2, fill=NAVY2)
    d.text((x+18, y+9), text, font=f_chip, fill=AMBER_L)
    return tw+36
w1 = chip(LX, 452, "Free 24h preview · Aperçu gratuit")
chip(LX+w1+12, 452, "EN | FR")
chip(LX, 504, "WhatsApp-first · live in 3–5 days")

d.text((LX, 566), "amk-cm.vercel.app", font=font("OpenSans-Bold.ttf", 23), fill=WHITE)

# --- two concept browser frames (right side, clear of text column) ---
def browser_shot(src, box, radius=10):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0-10, y0-30, x1+10, y1+10), radius=radius+5, fill=NAVY2, outline=NAVY3, width=1)
    d.ellipse((x0+8, y0-22, x0+18, y0-12), fill=(248,113,113))
    d.ellipse((x0+26, y0-22, x0+36, y0-12), fill=(251,191,36))
    d.ellipse((x0+44, y0-22, x0+54, y0-12), fill=(52,211,153))
    im = Image.open(HERE/src).resize((x1-x0, y1-y0))
    mask = Image.new("L", (x1-x0, y1-y0), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,x1-x0,y1-y0), radius=radius, fill=255)
    img.paste(im, (x0, y0), mask)

# paste happens on img; d must redraw after? frames are right column only, no overlap with text
browser_shot("clinic.png", (770, 128, 1152, 366))
browser_shot("crestwood.png", (726, 330, 1152, 592))

out = HERE / "og-cover.jpg"
img.save(out, "JPEG", quality=86, optimize=True)
print("wrote", out, round(out.stat().st_size/1024), "KB")
