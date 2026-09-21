# -*- coding: utf-8 -*-
"""Bilingual EN|FR printable A4 sheet of AMK walk-in leave-behind cards (8/sheet).
Re-run after dropping a hosted agency URL into SITE_URL to add a website QR."""
import base64, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SITE_URL = ""  # e.g. https://amk-cm.vercel.app — fill once the agency site is hosted

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

logo = b64(ROOT / "brand" / "AMK-logo-square.png")
qr = b64(HERE / "qr-wa-bilingual.png")

site_row = f'<div class="site">🌐 {SITE_URL.replace("https://","")}</div>' if SITE_URL else ""

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
    <div class="en"><b>Bilingual websites for Cameroon&apos;s schools &amp; clinics</b> — admissions, fees &amp; results online; parents reach you by WhatsApp in one tap. Ready in 3–5 days.</div>
    <div class="fr"><b>Sites web bilingues (FR|EN) pour écoles et cliniques</b> — inscriptions, frais et résultats en ligne ; les parents vous joignent sur WhatsApp en un clic. Livrés en 3–5 jours.</div>
    <div class="price">From / À partir de <b>100 000 FCFA</b> · 50/50 payment / paiement</div>
  </div>
  <div class="bottom">
    <img class="qr" src="data:image/png;base64,{qr}" alt="WhatsApp QR">
    <div class="cta">
      <div class="big">Scan to message us on WhatsApp</div>
      <div class="big fr">Scannez pour nous écrire sur WhatsApp</div>
      <div class="num">+237 677 78 96 31</div>
      <div class="ask">Ask for your FREE preview · Demandez votre aperçu GRATUIT</div>
      {site_row}
    </div>
  </div>
</div>"""

html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>AMK walk-in cards — EN|FR</title>
<style>
@page {{ size: A4; margin: 9mm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, 'Segoe UI', Roboto, Arial, sans-serif; color:#10243d; }}
.sheet {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 4mm; }}
.card {{ border: 1.5px solid #0F2A43; border-radius: 3mm; padding: 3.2mm; height: 91mm;
        display: flex; flex-direction: column; justify-content: space-between; page-break-inside: avoid; }}
.top {{ display: flex; align-items: center; gap: 3mm; border-bottom: 1px solid #d7e0ea; padding-bottom: 2mm; }}
.logo {{ width: 14mm; height: 14mm; object-fit: contain; }}
.brand .name {{ font-size: 18pt; font-weight: 800; color: #0F2A43; letter-spacing: 1px; line-height: 1; }}
.brand .tag {{ font-size: 6.6pt; color: #35506b; margin-top: 1mm; }}
.offer {{ padding: 1.6mm 0; }}
.offer .en {{ font-size: 8.2pt; line-height: 1.32; }}
.offer .fr {{ font-size: 8.2pt; line-height: 1.32; margin-top: 1.2mm; color:#1f3b5c; }}
.offer .price {{ font-size: 8pt; text-align:center; margin-top: 1.8mm; color:#0a7a4d; }}
.bottom {{ display: flex; align-items: center; gap: 3mm; border-top: 1px solid #d7e0ea; padding-top: 2mm; }}
.qr {{ width: 26mm; height: 26mm; }}
.cta .big {{ font-size: 7.8pt; font-weight: 800; color: #0F2A43; line-height:1.25; }}
.cta .big.fr {{ color:#1f3b5c; }}
.cta .num {{ font-size: 11pt; font-weight: 800; color: #0a7a4d; margin: 1mm 0; }}
.cta .ask {{ font-size: 7pt; color: #35506b; line-height: 1.3; }}
.cta .site {{ font-size: 7pt; color: #0F2A43; margin-top: 1mm; font-weight: 700; }}
</style></head><body><div class="sheet">{card*8}</div></body></html>"""

(HERE / "walk-in-cards.html").write_text(html, encoding="utf-8")
print("wrote bilingual sales/walkin/walk-in-cards.html (8 cards per A4)")
