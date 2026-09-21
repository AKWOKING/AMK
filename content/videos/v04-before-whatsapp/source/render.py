from PIL import Image,ImageDraw,ImageFont
import numpy as np, subprocess, math, wave, json
from pathlib import Path
P=Path('/home/user/video4_asset'); FF=(P/'ffpath.txt').read_text().strip(); W,H=720,1280; fps=30; rate=1; duration=34.2
fontdir=Path('/home/user/video/assets/fonts')
from functools import lru_cache
@lru_cache(None)
def font(s,b=True):
 f=ImageFont.truetype(str(fontdir/('Montserrat-ExtraBold.ttf' if b else 'Montserrat-Medium.ttf')),s)
 try: f.set_variation_by_axes([800 if b else 500])
 except Exception: pass
 return f
navy='#1B2055'; ink='#172044'; teal='#23C4B1'; gold='#FFB020'; white='#FFFFFF'
base=Image.open('/home/user/video/assets/img/s1_hook.png').convert('RGB').resize((720,1280))
# Website overlays obscure the social profile in the reused opening art.
def text(d,xy,t,s=34,c=white,b=True): d.text(xy,t,font=font(s,b),fill=c)
def center(d,y,t,s=34,c=white):
 f=font(s); box=d.textbbox((0,0),t,font=f); d.text(((W-box[2])/2,y),t,font=f,fill=c)
def box(d,xy,c=white,r=20): d.rounded_rectangle(xy,radius=r,fill=c)
def header(im,n,title):
 d=ImageDraw.Draw(im); text(d,(48,115),f'WEBSITE CHECK   /   {n:02d}',22,teal)
 for i,l in enumerate(title): text(d,(48,174+i*56),l,43)
 return d
def web(d):
 box(d,(42,370,658,1100),'#F6F8FC',26); box(d,(42,370,658,443),'#E4EAF2',20)
 for i in range(3): d.ellipse((62+i*22,397,72+i*22,407),fill=['#F28E88',gold,teal][i])
 text(d,(163,388),'brightcare.example',19,ink,False)
 text(d,(72,469),'BRIGHTCARE',27,ink);text(d,(72,511),'FAMILY CLINIC',15,'#687491')
 text(d,(50,1130),'ILLUSTRATIVE WEBSITE • FICTIONAL BUSINESS',14,'#ACB4D7',False)
def person(d,x,y,c=teal,scale=1):
 r=int(20*scale); d.ellipse((x-r,y-r,x+r,y+r),fill='#B8774F'); box(d,(x-r*1.5,y+r+5,x+r*1.5,y+r*3),c,12)
red='#F27C82'
def lines(d,y,ls,s=32,c=white,gap=46):
 for j,l in enumerate(ls):center(d,y+j*gap,l,s,c)
def browser(d):
 box(d,(42,380,658,1000),'#F6F8FC',26);box(d,(42,380,658,449),'#E4EAF2',22)
 for j in range(3):d.ellipse((63+j*23,406,74+j*23,417),fill=[red,gold,teal][j])
 text(d,(163,397),'your-business.example',19,ink,False)
 text(d,(73,479),'YOUR BUSINESS',25,ink)
def crossed(d,y,label):
 box(d,(72,y,628,y+78),'#F8E7EA',15)
 d.line((92,y+27,114,y+49),fill=red,width=5);d.line((114,y+27,92,y+49),fill=red,width=5)
 text(d,(137,y+23),label,24,ink)
def scene(i,local):
 im=Image.new('RGB',(W,H),navy);d=ImageDraw.Draw(im)
 if i==0:
  im=base.copy();d=ImageDraw.Draw(im)
  box(d,(385,590,649,1140),white,27);text(d,(407,623),'YOUR WEBSITE',18,ink)
  for y in (710,800,890):box(d,(410,y,620,y+48),'#E4EAF2',12)
  box(d,(410,1010,620,1080),teal,14);text(d,(425,1031),'WhatsApp',25,ink)
  text(d,(50,125),'3 MOBILE WEBSITE LEAKS',24,teal)
  lines(d,173,['Losing customers'],43,gap=51)
  box(d,(49,245,671,374),gold,24);lines(d,267,['BEFORE WHATSAPP?'],36,ink)
 elif i==1:
  header(im,1,['Too slow','to load.']);browser(d)
  # Rotating loader within the website.
  angle=int(local*210)%360
  d.arc((290,613,430,753),angle,angle+270,fill=teal,width=12)
  center(d,790,'Still loading…',30,ink)
  box(d,(92,863,608,883),'#DFE4EE',8);box(d,(92,863,92+min(280,int(local*47)),883),teal,8)
  if local>2.4:
   box(d,(94,903,626,972),'#F8E7EA',15);text(d,(124,923),'VISITOR LEFT',28,ink)
  lines(d,1045,['They never even','see your offer.'],31,gap=44)
 elif i==2:
  header(im,2,['Hard to use','on a phone.']);browser(d)
  # Deliberately miniature desktop layout, labelled as the problem.
  for k in range(5):text(d,(73+k*104,548),['HOME','ABOUT','SERVICES','NEWS','CONTACT'][k],10,ink)
  for c in range(3):
   x=76+c*181;box(d,(x,608,x+160,701),'#DAE0EC',5)
   for r in range(7):box(d,(x,721+r*18,x+147-(r%3)*13,726+r*18),'#B9C1D2',2)
  label='Tiny text' if local<3.85 else 'Awkward menus' if local<4.85 else 'Too much zooming'
  box(d,(79,886,641,970),gold,18);center(d,909,label,31,ink)
  # Cursor highlights an unusably small target.
  x=545+int(10*math.sin(local*3));d.ellipse((x-28,530,x+42,588),outline=red,width=4)
  lines(d,1045,['Built for a desktop.', 'Visited on a phone.'],30,gap=44)
 elif i==3:
  header(im,3,['Contact takes','too much work.']);browser(d)
  # Content scrolls inside a clipped viewport until the contact button appears.
  panel=Image.new('RGB',(548,415),'#F6F8FC');pd=ImageDraw.Draw(panel)
  offset=int(min(1,max(0,(local-.5)/3.6))*610)
  for k in range(9):
   y=30+k*94-offset
   pd.rounded_rectangle((4,y,515,y+53),radius=8,fill='#E0E6F0')
  by=910-offset
  pd.rounded_rectangle((8,by,510,by+85),radius=18,fill=teal)
  pd.text((111,by+23),'WhatsApp us',font=font(28),fill=ink)
  im.paste(panel,(77,558));d=ImageDraw.Draw(im)
  d.rounded_rectangle((632,568,639,961),radius=3,fill='#D1D8E5')
  y=575+int(min(local/4,1)*325);box(d,(632,y,639,y+49),ink,3)
  lines(d,1045,['Don’t bury the button','at the bottom.'],30,gap=44)
 elif i==4:
  text(d,(48,133),'BEFORE YOU BUY MORE TRAFFIC',22,teal)
  lines(d,309,['Help the people','already visiting.'],44,gap=62)
  box(d,(61,575,659,805),gold,28)
  lines(d,613,['MAKE CONTACT','EASY.'],47,ink,gap=69)
  center(d,929,'Less friction. A clearer next step.',25)
 else:
  text(d,(48,133),'TRY THIS NOW',25,teal)
  lines(d,286,['Open your website','on your phone.'],41,gap=59)
  # Clean, prominent contact example.
  box(d,(137,475,583,812),white,29);box(d,(274,489,446,502),ink,5)
  text(d,(178,548),'YOUR BUSINESS',24,ink)
  box(d,(169,648,551,742),teal,19);text(d,(206,677),'WhatsApp us',31,ink)
  lines(d,898,['How quickly can you','reach your business?'],32,gap=46)
 for k in range(3):box(d,(48+k*208,103,242+k*208,109),teal if i>k else '#383F74',2)
 return im
oldscene=scene
@lru_cache(maxsize=200)
def shot(name):return Image.open(P/'captures'/name).convert('RGB')
def viewport(im,img):
 d=ImageDraw.Draw(im);box(d,(68,285,652,1150),'#0D1230',22)
 im.paste(img.resize((560,840),Image.Resampling.LANCZOS),(80,300))
 return ImageDraw.Draw(im)
def scene(i,local):
 if i in (0,4):
  im=oldscene(i,local)
  if i==0:im.paste(shot('after_mobile.png').resize((240,510)),(398,608))
  return im
 im=Image.new('RGB',(W,H),navy);d=ImageDraw.Draw(im)
 if i in (1,2,3):
  titles=[['Too slow to load.'],['Hard to use','on a phone.'],['Contact takes','too much work.']]
  text(d,(48,92),f'WEBSITE LEAK {i} / 3',22,teal)
  for j,l in enumerate(titles[i-1]):text(d,(48,142+j*49),l,38)
  if i==1:
   img=shot('before_full.png').copy();dim=Image.new('RGB',img.size,'#F7F8F5');img=Image.blend(img,dim,.93)
   d=viewport(im,img);ang=int(local*230)%360
   d.arc((310,600,410,700),ang,ang+265,fill=teal,width=9)
   center(d,727,'Still loading…',30,ink)
   center(d,800,'SIMULATED DELAY',17,'#647168')
   if local>2.7:box(d,(120,974,600,1060),gold,18);center(d,998,'VISITOR LEFT',32,ink)
  elif i==2:
   if local<1.8:img=shot('before_full.png')
   else:img=shot(f'mobile_{min(93,int(local*15)):03}.png')
   d=viewport(im,img)
   lab='Desktop layout on a phone' if local<2.75 else 'Tiny text. Awkward menus.' if local<4.8 else 'Sideways scrolling.'
   box(d,(83,1001,637,1110),gold,16);center(d,1036,lab,25,ink)
  else:
   idx=min(77,int(local*15));img=shot(f'scroll_{idx:03}.png')
   if local>3.6:
    z=min(1,(local-3.6)/.55);w=int(980-490*z);h=int(1470-735*z);img=img.crop((980-w,1470-h,980,1470))
   d=viewport(im,img)
   if local>3.65:box(d,(107,388,613,466),gold,15);center(d,411,'BURIED IN THE FOOTER',24,ink)
   if local>4.15:
    detail=shot('scroll_077.png').crop((775,1375,975,1470)).resize((520,247),Image.Resampling.LANCZOS)
    im.paste(detail,(100,850));d=ImageDraw.Draw(im)
    d.rounded_rectangle((98,848,622,1099),radius=3,outline=gold,width=3)
  center(d,1170,'MBOACARE · FICTIONAL DEMONSTRATION',14,'#A8B4D0')
 elif i==5:
  text(d,(48,93),'TRY THIS ON YOUR PHONE',23,teal)
  center(d,153,'How quickly can you',34);center(d,199,'reach your business?',34)
  d=viewport(im,shot('after_mobile.png'))
  # Leave the real WhatsApp buttons fully visible.
  center(d,1170,'MBOACARE · IMPROVED DEMO WEBSITE',14,'#A8B4D0')
 else:
  text(d,(48,133),'AMK · SCHOOLS & CLINICS',23,teal)
  center(d,316,'Want a clearer',43);center(d,371,'homepage?',43)
  box(d,(62,502,658,659),gold,25);center(d,544,'DM “PREVIEW”',49,ink)
  center(d,733,'for a free',39);center(d,789,'homepage concept.',38)
  center(d,963,'See what yours could look like.',26)
 return im
starts=[0,4.78,9.78,16.02,21.3,26.5,30.5]
(P/'timeline.json').write_text(json.dumps({'starts':starts,'fps':fps,'duration':duration},indent=2))
cmd=[FF,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','30','-i','-','-vf','scale=1080:1920,setsar=1,fps=30','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','18','-pix_fmt','yuv420p','-r','30',str(P/'step01_browser_edit_30fps.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=open(P/'render.log','w'))
for n in range(round(duration*fps)):
 t=n/fps;i=max(k for k,s in enumerate(starts) if t>=s);loc=t-starts[i];im=scene(i,loc)
 if i and loc<.13:
  shift=int(32*(1-loc/.13)**2);canvas=Image.new('RGB',(W,H),navy);canvas.paste(im,(shift,0));im=canvas
 proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
sr=48000;t=np.arange(int(duration*sr))/sr
mus=sum(np.sin(2*np.pi*f*t)*.012 for f in [130.81,164.81,196,261.63]);mus*=np.minimum(t/1.5,1)*np.minimum((duration-t)/1,1)
with wave.open(str(P/'step02_music.wav'),'w') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mus*32767).astype('int16').tobytes())
g=f'[0:a]apad,atrim=0:{duration}[orig];[1:a]adelay=30500,apad,atrim=0:{duration}[cta];[orig][cta]amix=inputs=2:normalize=0,asplit=2[n][key];[2:a][key]sidechaincompress=threshold=0.015:ratio=5:attack=15:release=300[m];[n][m]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]'
subprocess.run([FF,'-y','-i','/home/user/video4/narration.mp3','-i',str(P/'cta.mp3'),'-i',str(P/'step02_music.wav'),'-filter_complex',g,'-map','[a]','-ar','48000',str(P/'step03_narration_cta_mix.wav')],stderr=open(P/'audio.log','w'),check=True)
subprocess.run([FF,'-y','-i',str(P/'step01_browser_edit_30fps.mp4'),'-i',str(P/'step03_narration_cta_mix.wav'),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart','/home/user/Video_04_Real_Website_PREVIEW.mp4'],stderr=open(P/'mux.log','w'),check=True)
sheet=Image.new('RGB',(960,1280),navy)
for k,(i,t) in enumerate([(0,2),(1,3),(2,3),(3,4.5),(5,2),(6,2)]):sheet.paste(scene(i,t).resize((320,568)),((k%3)*320,(k//3)*640))
sheet.save(P/'review.jpg')
print('Complete:',duration,'seconds, 30 fps')
