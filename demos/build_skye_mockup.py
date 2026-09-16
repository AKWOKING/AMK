# -*- coding: utf-8 -*-
"""Named-gift mockup for The Skye — demos/shots/mockup-skye-wa.jpg (1600x900).
House style: eyebrow dot, title, tagline, concept pill, laptop + phone, sparkles;
brand palette from their logo (deep blue + sky blue, ice background)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "tools" / "record" / "fonts"
def f(n,s): return ImageFont.truetype(str(F/n), s)

NAVY=(11,74,120); BLUE=(14,165,233); BLUE_D=(2,132,199); SKY=(56,189,248)
INK=(16,42,64); SLATE=(91,114,132); ICE=(233,245,253); ICE2=(218,238,250)
WHITE=(255,255,255); GOLD=(245,158,11)

S=2
W,H=1920*S//2,1080*S//2
img=Image.new("RGB",(W,H),ICE)
# vertical gradient
top=Image.new("RGB",(1,H)); top.putdata([ICE])
img=top.resize((W,H))
px=img.load()
for y in range(H):
    t=y/H
    r=int(ICE[0]+(ICE2[0]-ICE[0])*t); g=int(ICE[1]+(ICE2[1]-ICE[1])*t); b=int(ICE[2]+(ICE2[2]-ICE[2])*t)
    for x in range(0,W,4):
        for xx in range(x,min(x+4,W)): px[xx,y]=(r,g,b)
d=ImageDraw.Draw(img)

def rr(box,rad,fill=None,outline=None,w=1): d.rounded_rectangle(box,radius=rad,fill=fill,outline=outline,width=w)
def sparkle(cx,cy,r,col):
    d.line((cx-r,cy,cx+r,cy),fill=col,width=3*S//2)
    d.line((cx,cy-r,cx,cy+r),fill=col,width=3*S//2)
    d.line((cx-r//2,cy-r//2,cx+r//2,cy+r//2),fill=col,width=2*S//2)
    d.line((cx-r//2,cy+r//2,cx+r//2,cy-r//2),fill=col,width=2*S//2)

for (cx,cy,r,c) in [(1760,150,16,SKY),(170,760,13,SKY),(1830,760,12,BLUE),(120,180,10,BLUE)]:
    sparkle(cx*S//2,cy*S//2,r*S//2,c+(0,) if len(c)==3 else c)

# ---- header text ----
d.ellipse((70*S//2-7*S//2,84*S//2-7*S//2,70*S//2+7*S//2,84*S//2+7*S//2),fill=BLUE)
d.text((92*S//2,72*S//2),"SITE CONCEPT  ·  CABINET DENTAIRE  ·  BONAMOUSSADI, DOUALA",
       font=f("OpenSans-Bold.ttf",17*S//2),fill=BLUE_D)
d.text((68*S//2,108*S//2),"Cabinet Dentaire The Skye",font=f("OpenSans-Bold.ttf",62*S//2),fill=INK)
d.text((71*S//2,196*S//2),"Souriez à l'infini  ·  tarifs en FCFA  ·  rendez-vous WhatsApp en un clic",
       font=f("OpenSans-Regular.ttf",24*S//2),fill=SLATE)
rr((70*S//2,244*S//2,560*S//2,292*S//2),24*S//2,fill=NAVY)
d.text((92*S//2,256*S//2),"Concept par AMK — votre site en ligne en 3–5 jours",
       font=f("OpenSans-Bold.ttf",16*S//2),fill=WHITE)

# ---- laptop ----
LX,LY,LW,LH=300*S//2,320*S//2,1180*S//2,700*S//2
rr((LX-22,LY-14,LX+LW+22,LY+LH+26),20,fill=(23,37,54))           # lid
rr((LX-22,LY+LH,LX+LW+22,LY+LH+26),10,fill=(37,55,75))           # base hint
rr((LX,LY,LX+LW,LY+LH),10,fill=WHITE)                            # screen
# browser chrome
d.rectangle((LX,LY,LX+LW,LY+44*S//2),fill=(244,248,252))
for i,c in enumerate([(248,113,113),(251,191,36),(52,211,153)]):
    d.ellipse((LX+18*S//2+i*22*S//2,LY+14*S//2,LX+30*S//2+i*22*S//2,LY+26*S//2),fill=c)
rr((LX+120*S//2,LY+10*S//2,LX+470*S//2,LY+34*S//2),12,fill=WHITE,outline=(214,226,236))
d.text((LX+136*S//2,LY+12*S//2),"theskye-dental.vercel.app (concept)",font=f("OpenSans-Regular.ttf",12*S//2),fill=SLATE)
# page nav
py=LY+58*S//2
d.rounded_rectangle((LX+28*S//2,py-6,LX+60*S//2,py+26),radius=9,fill=NAVY)
# tiny tooth glyph
d.ellipse((LX+36*S//2,py,LX+52*S//2,py+16),fill=WHITE)
d.text((LX+70*S//2,py-4),"THE SKYE",font=f("OpenSans-Bold.ttf",15*S//2),fill=NAVY)
for i,t in enumerate(["Soins","Tarifs","Visite","Questions"]):
    d.text((LX+250*S//2+i*92*S//2,py),t,font=f("OpenSans-Regular.ttf",13*S//2),fill=SLATE)
rr((LX+LW-150*S//2,py-8,LX+LW-28*S//2,py+26),12,fill=NAVY)
d.text((LX+LW-138*S//2,py-2),"Prendre RDV",font=f("OpenSans-Bold.ttf",12*S//2),fill=WHITE)
# hero copy
hx=LX+40*S//2; hy=LY+120*S//2
d.text((hx,hy),("CABINET DENTAIRE — BONAMOUSSADI"),font=f("OpenSans-Bold.ttf",11*S//2),fill=BLUE_D)
d.text((hx,hy+26*S//2),"Souriez",font=f("OpenSans-Bold.ttf",46*S//2),fill=INK)
d.text((hx,hy+76*S//2),"à l'infini.",font=f("OpenSans-Bold.ttf",46*S//2),fill=BLUE_D)
d.multiline_text((hx,hy+140*S//2),
    "Des soins de qualité dans un cadre\nmoderne, à Bonamoussadi — tarifs\nclairs en FCFA et rendez-vous par\nWhatsApp, en français et en anglais.",
    font=f("OpenSans-Regular.ttf",15*S//2),fill=SLATE,spacing=8)
rr((hx,hy+250*S//2,hx+190*S//2,hy+292*S//2),12,fill=NAVY)
d.text((hx+20*S//2,hy+259*S//2),"Prendre rendez-vous",font=f("OpenSans-Bold.ttf",13*S//2),fill=WHITE)
rr((hx+205*S//2,hy+250*S//2,hx+360*S//2,hy+292*S//2),12,outline=NAVY,w=2)
d.text((hx+225*S//2,hy+259*S//2),"Voir les soins",font=f("OpenSans-Bold.ttf",13*S//2),fill=NAVY)
for i,t in enumerate(["⭐ 100 % · 19 avis","📍 Stella & Joyce","💬 WhatsApp"]):
    rr((hx+i*150*S//2,hy+320*S//2,hx+(i+1)*148*S//2,hy+352*S//2),16,fill=(227,243,252))
    d.text((hx+i*150*S//2+12*S//2,hy+326*S//2),t,font=f("OpenSans-Bold.ttf",10*S//2),fill=BLUE_D)
# hero photo
hero=Image.open(ROOT/"demos/img/skye-hero.jpg").convert("RGB")
hw,hh=380*S//2,470*S//2
h2=hero.resize((hw,hh))
mask=Image.new("L",(hw,hh),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,hw,hh),18,fill=255)
img.paste(h2,(LX+LW-hw-40*S//2,LY+118*S//2),mask)
# stats bar
sy=LY+LH-72*S//2
d.rectangle((LX,sy,LX+LW,LY+LH),fill=NAVY)
for i,(n,l) in enumerate([("100%","recommandent"),("19","avis Facebook"),("2","langues FR | EN"),("10 000 F","consultation*")]):
    cx=LX+(i+0.5)*LW/4
    d.text((cx-40,sy+10),n,font=f("OpenSans-Bold.ttf",24*S//2),fill=WHITE)
    d.text((cx-44,sy+44),l,font=f("OpenSans-Regular.ttf",11*S//2),fill=(173,216,240))

# ---- phone (overlap right) ----
PX,PY,PW,PH=1430*S//2,400*S//2,330*S//2,620*S//2
sh=Image.new("RGBA",(PW+40,PH+40),(0,0,0,0)); sd=ImageDraw.Draw(sh)
sd.rounded_rectangle((20,8,PW+20,PH+28),40,fill=(20,34,50))
img.paste(sh,(PX-20,PY-8),sh)
rr((PX,PY,PX+PW,PY+PH),30,fill=WHITE)
rr((PX+PW//2-40,PY+12,PX+PW//2+40,PY+30),9,fill=(20,34,50))
# phone nav
d.rounded_rectangle((PX+18,PY+44,PX+46,PY+72),radius=8,fill=NAVY)
d.ellipse((PX+25,PY+50,PX+39,PY+64),fill=WHITE)
d.text((PX+54,PY+48),"THE SKYE",font=f("OpenSans-Bold.ttf",13*S//2),fill=NAVY)
rr((PX+PW-86,PY+46,PX+PW-52,PY+70),12,fill=NAVY)
d.text((PX+PW-80,PY+50),"EN FR",font=f("OpenSans-Bold.ttf",10*S//2),fill=WHITE)
# phone image
pim=hero.resize((PW-32,250*S//2))
pm=Image.new("L",(PW-32,250*S//2),0); ImageDraw.Draw(pm).rounded_rectangle((0,0,PW-32,250*S//2),14,fill=255)
img.paste(pim,(PX+16,PY+92),pm)
d.text((PX+18,PY+360),"Souriez à l'infini.",font=f("OpenSans-Bold.ttf",22*S//2),fill=INK)
d.multiline_text((PX+18,PY+396),"Tarifs FCFA clairs et\nrendez-vous WhatsApp.",
                 font=f("OpenSans-Regular.ttf",13*S//2),fill=SLATE,spacing=4)
rr((PX+18,PY+460,PX+PW-18,PY+504),12,fill=NAVY)
d.text((PX+44,PY+470),"📅  Prendre rendez-vous",font=f("OpenSans-Bold.ttf",13*S//2),fill=WHITE)
# sticky bar
d.rectangle((PX,PY+PH-58,PX+PW,PY+PH),fill=BLUE_D)
d.text((PX+24,PY+PH-40),"💬 WhatsApp 24h/24",font=f("OpenSans-Bold.ttf",13*S//2),fill=WHITE)

img=img.resize((1600,900),Image.LANCZOS)
out=ROOT/"demos/shots/mockup-skye-wa.jpg"
img.save(out,"JPEG",quality=86,optimize=True)
print("wrote",out,round(out.stat().st_size/1024),"KB")
