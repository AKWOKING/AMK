# -*- coding: utf-8 -*-
"""Rebrand Sasse concept: green/gold -> blue/black/white (verified uniform colors).
Embeds chapel photo (base64) into hero video frame. New demo crest in school colors."""
import sys, re, base64

PATH = "sjc-sasse-v2.html"
html = open(PATH, encoding="utf-8").read()
B64 = open("_b64.txt", encoding="utf-8").read().strip()

def rep(n, old, new):
    global html
    c = html.count(old)
    if c != n:
        print(f"FAIL [{n} vs {c}]: {old[:80]}...")
        sys.exit(1)
    html = html.replace(old, new)

# 1. ROOT PALETTE (green/gold -> navy/royal/white)
rep(1,
""":root{
  --brand:#14351F; --brand2:#1D4A2B; --brand3:#2A5A38;
  --gold:#C9A227; --gold-l:#E8D48B; --gold-t:#FDF9EC;
  --bg:#FAF7F0; --white:#FFFFFF; --border:#E5DED0;
  --ink:#1C2420; --slate:#5C6660; --slate-l:#8A958E;
}""",
""":root{
  --brand:#0F2456; --brand2:#17357F; --brand3:#2E4E9E;
  --gold:#2E4E9E; --gold-l:#BFD0F5; --gold-t:#EEF3FC;
  --bg:#F6F8FC; --white:#FFFFFF; --border:#DCE3F0;
  --ink:#131A2A; --slate:#54606F; --slate-l:#8C97A8;
}""")

# 2. DEMO CREST v2 (both header + footer are identical) — royal shield, black outline, white cross & book
rep(1,
'<svg viewBox="0 0 48 48"><path d="M24 3l17 6v13c0 10.5-7 18-17 23C14 40 7 32.5 7 22V9l17-6z" fill="#14351F" stroke="#C9A227" stroke-width="2"/><path d="M24 10v14M18 16h12" stroke="#C9A227" stroke-width="3" stroke-linecap="round"/><path d="M14 32c4-2.5 7.5-2.5 10 0 2.5-2.5 6-2.5 10 0v7c-4-2.5-7.5-2.5-10 0-2.5-2.5-6-2.5-10 0v-7z" fill="#FAF7F0"/><path d="M24 32v7" stroke="#14351F" stroke-width="1.3"/></svg>',
'<svg viewBox="0 0 48 48"><path d="M24 3l17 6v13c0 10.5-7 18-17 23C14 40 7 32.5 7 22V9l17-6z" fill="#17357F" stroke="#131A2A" stroke-width="2"/><path d="M24 10v14M18 16h12" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/><path d="M14 32c4-2.5 7.5-2.5 10 0 2.5-2.5 6-2.5 10 0v7c-4-2.5-7.5-2.5-10 0-2.5-2.5-6-2.5-10 0v-7z" fill="#FFFFFF"/><path d="M24 32v7" stroke="#17357F" stroke-width="1.3"/></svg>')

# 3. HERO VIDEO FRAME -> real chapel photo (base64, self-contained file)
rep(1,
'''<div class="video-inner">
          <div class="play"></div>
          <span class="video-cap" data-en="Video loop — campus life, classrooms, sport and chapel (add footage)" data-fr="Boucle vidéo — vie du campus, classes, sport et chapelle (ajouter des images)">Video loop — campus life, classrooms, sport and chapel (add footage)</span>
        </div>''',
'''<div class="video-inner">
          <img src="data:image/jpeg;base64,''' + B64 + '''" alt="Chapel service at Sasse" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
          <div style="position:absolute;left:0;right:0;bottom:0;padding:34px 14px 12px;background:linear-gradient(transparent,rgba(10,26,60,.92))"><span class="video-cap" data-en="Chapel service at Sasse — your 10–15 photos take this place at kickoff" data-fr="Office de chapelle à Sasse — vos 10–15 photos prendront cette place à la réunion de lancement" style="color:#fff;display:block">Chapel service at Sasse — your 10–15 photos take this place at kickoff</span></div>
        </div>''')

# 4. white text on royal CTA (blue button must not carry dark text)
rep(1, '.btn-gold{background:var(--gold);color:var(--brand)}',
        '.btn-gold{background:var(--gold);color:#fff}')
rep(1, 'border-radius:50%;background:var(--gold);color:var(--brand)',
        'border-radius:50%;background:var(--gold);color:#fff')

# 5. anthem tagline on dark navy hero -> pale blue
rep(1, 'color:#C9A227;margin-top:10px', 'color:#BFD0F5;margin-top:10px')

# 6. GLOBAL HEX REMAP (must all exist; replace every occurrence)
GLB = [
 ("#cfe0d3", "#C7D4F5"), ("#Cfe0d3", "#C7D4F5"),
 ("#E8D48B", "#BFD0F5"), ("#7A5C00", "#17357F"), ("#C9A227", "#2E4E9E"),
 ("#14351F", "#0F2456"), ("#1D4A2B", "#17357F"),
 ("#FAF7F0", "#F6F8FC"), ("#D9C98A", "#C7D4F5"), ("#E8F0EA", "#E3EAF8"),
 ("#0F2417", "#0A1A3C"), ("#9DB5A4", "#93A3C4"), ("#7E9A89", "#7E93BC"),
 ("rgba(201,162,39,.14)", "rgba(255,255,255,.12)"),
 ("rgba(201,162,39,.45)", "rgba(255,255,255,.35)"),
 ("rgba(201,162,39,.2)", "rgba(46,78,158,.3)"),
]
for old, new in GLB:
    c = html.count(old)
    if c == 0:
        print(f"NOTE: {old} not present — skipped")
        continue
    html = html.replace(old, new)
    print(f"  {old} -> {new}  (x{c})")

open(PATH, "w", encoding="utf-8").write(html)
en = len(re.findall(r'data-en="', html)); fr = len(re.findall(r'data-fr="', html))
STALE = ["#14351F", "#1D4A2B", "#2A5A38", "#C9A227", "#7A5C00", "#E8D48B",
         "#FDF9EC", "#cfe0d3", "#Cfe0d3", "#FAF7F0", "#E5DED0", "#1C2420",
         "#5C6660", "#8A958E", "#0F2417", "#9DB5A4", "#7E9A89", "#E8F0EA", "#D9C98A"]
left = [s for s in STALE if s in html]
print(f"DONE — pairs {en}/{fr} · file {len(html)//1024}KB · stale greens left: {left or 'none'}")
