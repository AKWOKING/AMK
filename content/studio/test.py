from playwright.sync_api import sync_playwright
from pathlib import Path
P=Path('/home/user/website-demo')
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox']); page=b.new_page(viewport={'width':1350,'height':1050},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((P/'Website_Demo_Studio.html').as_uri());page.wait_for_timeout(600)
 page.screenshot(path=str(P/'studio-preview.png'))
 f=page.frames[1];assert f.locator('.old').count()==1
 page.locator('#after').click();page.wait_for_timeout(300);f=page.frames[1]
 f.locator('.menu').click();assert f.locator('nav.open').count()==1
 f.locator('.float').click();assert f.locator('.notice').count()==1
 f.locator('.notice button').click();f.evaluate('booking()');assert f.locator('dialog[open]').count()==1
 page.locator('#desktop').click();page.locator('button',has_text='Reset page').click()
 page.screenshot(path=str(P/'after-preview.png'))
 print('Interaction checks passed. JS errors:',errors);assert not errors
 b.close()
