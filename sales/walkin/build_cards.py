# -*- coding: utf-8 -*-
"""Build a printable A4 sheet of AMK walk-in leave-behind cards (9 cards).
Re-run after dropping a hosted agency URL into SITE_URL below to add a second QR."""
import base64, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SITE_URL = ""  # e.g. https://amk-cm.vercel.app — fill once agency site is hosted

def b64(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

logo = b64(HERE.parent.parent / "brand" / "AMK-logo-square.png")
qr_en = b64(HERE / "qr-wa-en.png")
qr_fr = b64(HERE / "qr-wa-fr.png")

site_block = ""
if SITE_URL:
    site_block = f'<div class="site">🌐 {SITE_URL.replace("https://","")}</div>'

card = f"""
<div class="card">
  <div class="top">
    <img class="logo" src="data:image/png;base64,{logo}" alt="AMK">
    <div class="brand">
      <div class="name">AMK</div>
      <div class="tag">Web Development &amp; Digital Solutions</div>
    </div>
  </div>
  <div class="offer">
    <div class="line1">Sites web bilingues (FR|EN) pour écoles &amp; cliniques</div>
    <div class="line2">Bilingual websites for schools &amp; clinics · livraison 3–5 jours</div>
    <div class="price">À partir de 100 000 FCFA · paiement 50/50</div>
  </div>
  <div class="bottom">
    <img class="qr" src="data:image/png;base64,{qr_en}" alt="WhatsApp QR">
    <div class="cta">
      <div class="big">Scannez → WhatsApp</div>
      <div class="num">+237 677 78 96 31</div>
      <div class="ask">Demandez votre aperçu gratuit · Ask for your free preview</div>
      {site_block}
    </div>
  </div>
</div>"""

html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>AMK walk-in cards</title>
<style>
@page {{ size: A4; margin: 10mm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif; }}
.sheet {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }}
.card {{ border: 1.5px solid #0F2A43; border-radius: 3mm; padding: 3mm; height: 88mm;
        display: flex; flex-direction: column; justify-content: space-between; page-break-inside: avoid; }}
.top {{ display: flex; align-items: center; gap: 2.5mm; border-bottom: 1px solid #d7e0ea; padding-bottom: 2mm; }}
.logo {{ width: 13mm; height: 13mm; object-fit: contain; }}
.brand .name {{ font-size: 17pt; font-weight: 800; color: #0F2A43; letter-spacing: 1px; line-height: 1; }}
.brand .tag {{ font-size: 6.2pt; color: #35506b; margin-top: 1mm; }}
.offer {{ text-align: center; padding: 1.5mm 0; }}
.offer .line1 {{ font-size: 7.6pt; font-weight: 700; color: #0F2A43; }}
.offer .line2 {{ font-size: 6.6pt; color: #35506b; margin-top: 0.8mm; }}
.offer .price {{ font-size: 7.2pt; font-weight: 700; color: #0a7a4d; margin-top: 1.2mm; }}
.bottom {{ display: flex; align-items: center; gap: 2.5mm; border-top: 1px solid #d7e0ea; padding-top: 2mm; }}
.qr {{ width: 22mm; height: 22mm; }}
.cta .big {{ font-size: 8pt; font-weight: 800; color: #0F2A43; }}
.cta .num {{ font-size: 9pt; font-weight: 800; color: #0a7a4d; margin: 0.8mm 0; }}
.cta .ask {{ font-size: 6pt; color: #35506b; line-height: 1.3; }}
.cta .site {{ font-size: 6.4pt; color: #0F2A43; margin-top: 1mm; font-weight: 700; }}
@media print {{ .sheet {{ gap: 3mm; }} }}
</style></head><body><div class="sheet">{card*9}</div></body></html>"""

(HERE / "walk-in-cards.html").write_text(html, encoding="utf-8")
print("wrote sales/walkin/walk-in-cards.html")
