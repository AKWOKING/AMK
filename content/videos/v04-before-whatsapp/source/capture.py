from playwright.sync_api import sync_playwright
from pathlib import Path
import os
# Chemins corrigés le 1/10/2026 — les deux étaient des chemins d'avant le déménagement du dépôt :
#   S : les pages « before » / « after » vivent maintenant dans le dépôt, content/studio/.
#   P : dossier de travail HORS dépôt (~170 captures en 980×1470) — AMK_V04_WORK, /tmp par défaut.
#       render.py lit CE MÊME dossier : les deux scripts doivent voir la même variable.
ROOT=Path(__file__).resolve().parents[4]
S=ROOT/'content'/'studio'
P=Path(os.environ.get('AMK_V04_WORK','/tmp/amk-v04'));(P/'captures').mkdir(parents=True,exist_ok=True)
for _f in ('before.html','after.html'):
    if not (S/_f).exists():
        raise SystemExit('✗ %s introuvable — lance d\'abord : python3 content/studio/create.py' % (S/_f))
# Lanceur : par défaut Playwright prend son Chromium. Dans un bac où les CDN de navigateurs sont
# bloqués (celui-ci), on pointe sur le binaire embarqué d'@sparticuz/chromium via AMK_CHROMIUM_EXEC
# (obtenir la valeur : tools/video/install.sh puis `chromium.executablePath()`, ex. /tmp/chromium).
# Sans la variable, comportement inchangé.
_EXEC=os.environ.get('AMK_CHROMIUM_EXEC')
_LAUNCH={'args':['--no-sandbox']}
if _EXEC:
    _LAUNCH['executable_path']=_EXEC
    _LAUNCH['args']+=['--disable-dev-shm-usage','--disable-gpu','--no-zygote','--single-process']
with sync_playwright() as p:
 b=p.chromium.launch(**_LAUNCH);page=b.new_page(viewport={'width':980,'height':1470},device_scale_factor=1)
 page.goto((S/'before.html').as_uri());page.screenshot(path=str(P/'captures/before_full.png'))
 # Actual browser page scroll, sampled at 15 fps for final 30 fps edit.
 total=78
 for j in range(total):
  t=j/(total-1);y=page.evaluate('(document.documentElement.scrollHeight-innerHeight)')*min(1,t*1.25)
  page.evaluate('(y)=>scrollTo(0,y)',y)
  if t>.7:page.locator('.footer a').evaluate("e=>{e.style.background='#ffb020';e.style.color='#172044';e.style.padding='8px';e.style.outline='3px solid #ffb020'}")
  page.screenshot(path=str(P/f'captures/scroll_{j:03}.png'))
 # Real mobile clipping + sideways pan on the bad layout.
 page.set_viewport_size({'width':390,'height':585});page.reload();page.evaluate('scrollTo(0,0)')
 for j in range(94):
  t=j/93;x=max(0,min(1,(t-.25)/.5))*590
  page.evaluate('(x)=>scrollTo(x,0)',x)
  page.screenshot(path=str(P/f'captures/mobile_{j:03}.png'))
 page.goto((S/'after.html').as_uri());page.screenshot(path=str(P/'captures/after_mobile.png'))
 page.locator('.float').click();page.screenshot(path=str(P/'captures/after_contact.png'))
 b.close()
print('Real browser captures complete')
