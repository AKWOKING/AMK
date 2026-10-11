from playwright.sync_api import sync_playwright
from pathlib import Path
import os
# Chemins corrigés le 1/10/2026 : '/home/user/website-demo' n'existe plus (déménagement du dépôt).
# La page testée vit dans le dépôt (à côté de ce script) ; les captures de contrôle, elles, sont des
# artefacts jetables et sortent hors du dépôt (règle du 23/09 : le dépôt n'est pas un disque dur).
P=Path(__file__).resolve().parent
OUT=Path(os.environ.get('AMK_STUDIO_WORK','/tmp/amk-studio'));OUT.mkdir(parents=True,exist_ok=True)
STUDIO=P/'Website_Demo_Studio.html'
if not STUDIO.exists():
    raise SystemExit('✗ %s introuvable — lance d\'abord : python3 content/studio/create.py' % STUDIO)
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
 b=p.chromium.launch(**_LAUNCH); page=b.new_page(viewport={'width':1350,'height':1050},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(STUDIO.as_uri());page.wait_for_timeout(600)
 page.screenshot(path=str(OUT/'studio-preview.png'))
 f=page.frames[1];assert f.locator('.old').count()==1
 page.locator('#after').click();page.wait_for_timeout(300);f=page.frames[1]
 f.locator('.menu').click();assert f.locator('nav.open').count()==1
 f.locator('.float').click();assert f.locator('.notice').count()==1
 f.locator('.notice button').click();f.evaluate('booking()');assert f.locator('dialog[open]').count()==1
 page.locator('#desktop').click();page.locator('button',has_text='Reset page').click()
 page.screenshot(path=str(OUT/'after-preview.png'))
 print('Interaction checks passed. JS errors:',errors);assert not errors
 b.close()
print('Captures de contrôle écrites dans', OUT)
