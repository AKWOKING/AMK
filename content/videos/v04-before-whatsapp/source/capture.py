from playwright.sync_api import sync_playwright
from pathlib import Path
P=Path('/home/user/video4_asset');S=Path('/home/user/website-demo');(P/'captures').mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(args=['--no-sandbox']);page=b.new_page(viewport={'width':980,'height':1470},device_scale_factor=1)
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
