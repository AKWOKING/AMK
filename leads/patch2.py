#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch build_sheet.py: fix Siantou (site actually up) + move sends to today 09/09."""
src = open("build_sheet.py", encoding="utf-8").read()

# ---------- 1) Siantou LEADS row ----------
old_start = ' ("Complexe Scolaire et Universitaire Siantou", "Yaoundé (Mvog-Mbi/Coron-Biteng, BP 04)", "FR",'
i = src.index(old_start)
end_marker = '  "Site siantou.net UNREACHABLE'
k = src.index(end_marker, i)
k = src.index("),\n", k) + 2
new_lead = (
 ' ("Complexe Scolaire et Universitaire Siantou", "Yaoundé (Mvog-Mbi/Coron-Biteng, BP 04)", "FR",\n'
 '  "facebook.com/INSTITUT SIANTOU (secondaire page: 732 likes)", "siantou-univ.com (+ siantou.net e-service subdomains)", "Good",\n'
 '  "N/V", "~732 (secondaire page)", "Yes (préinscription en ligne active)",\n'
 '  "+237 668 556 755", "Likely same", "Wantou Siantou Lucien (fondateur/président)", "PARKED — do not pitch",\n'
 '  "Strong (\'La Tour des Majors\' amphi, modern campus)", "Yes (secondary + university + technical campuses)",\n'
 '  12, "C",\n'
 '  "CORRECTED 09/09/26 (per King): current site siantou-univ.com is UP and digitally mature — modern WP (2025-26 content), online pre-registration (preinscription.siantou.net), document portal (document.siantou.net), e-learning, WhatsApp widget, 12+ filières BTS→MBA. Old siantou.net homepage down but its subdomains work. PARK per brief (B site); long-term upsell: EN|FR for international filières (HND/MBA)."),\n'
)
src = src[:i] + new_lead + src[k:]

# ---------- 2) TOP5: remove Siantou, renumber, append parked #7 ----------
s_start = src.index(' (3, "Complexe Scolaire et Universitaire Siantou"')
s_end = src.index('FU3 09/19."),\n', s_start) + len('FU3 09/19."),\n')
src = src[:s_start] + src[s_end:]

src = src.replace(' (4, "New Horizon International', ' (3, "New Horizon International')
src = src.replace(' (5, "Collège Catholique Bilingue La Retraite"', ' (4, "Collège Catholique Bilingue La Retraite"')
src = src.replace(' (6, "COMOBIL', ' (5, "COMOBIL')

parked = (
 ' (7, "Complexe Scolaire et Universitaire Siantou", "Yaoundé (Mvog-Mbi)", 12,\n'
 '  "PARKED (corrected 09/09/26 per King): initial intel was wrong — siantou.net homepage is down, but the group\'s CURRENT site siantou-univ.com is up and digitally mature: online pre-registration (preinscription.siantou.net), document request portal (document.siantou.net), e-learning, WhatsApp widget, content current to 2025-26, 12+ filières BTS→MBA.",\n'
 '  "BTS/DUT/university recruitment via online pre-registration; \'l\'école des majors\' branding.",\n'
 '  "Wantou Siantou Lucien (fondateur/président)",\n'
 '  "PARKED — no outreach for a basic website",\n'
 '  "— DO NOT SEND (site re-evaluated as Good) —",\n'
 '  "— DO NOT SEND —",\n'
 '  "N/A", "Long-term upsell only: EN|FR bilingual for international filières (HND/MBA), mobile refresh. Keep warm."),\n'
 ']\n'
)
anchor = '"Send on Messenger 09/10, then call 09/11 if no reply. One contact = whole group."),'
a = src.index(anchor) + len(anchor)
# replace the closing bracket right after
assert src[a:a+2] in ("]\n", "]\r") or src[a:a+3].strip().startswith("]")
src = src[:a] + "\n" + parked + src[a:].lstrip("\n").lstrip("]")

# ---------- 3) Move sends to today, shift follow-ups ----------
repl = [
 ('"Send on WhatsApp 09/10 (morning). If no reply: FU1 09/12, FU2 09/15, FU3 09/19. No walk-in."',
  '"Send TODAY 09/09 (school office hours). FU1 09/11, FU2 09/14, FU3 09/18. No walk-in."'),
 ('"Send on WhatsApp 09/10. FU1 09/12, FU2 09/15, FU3 09/19. No walk-in."',
  '"Send TODAY 09/09 (school office hours). FU1 09/11, FU2 09/14, FU3 09/18. No walk-in."'),
 ('"Send on WhatsApp 09/10. FU1 09/12, FU2 09/15, FU3 09/19."',
  '"Send TODAY 09/09. FU1 09/11, FU2 09/14, FU3 09/18."'),
 ('"Send on Messenger 09/10. FU1 09/12, FU2 09/15, FU3 09/19."',
  '"Send TODAY 09/09 (Messenger). FU1 09/11, FU2 09/14, FU3 09/18."'),
 ('"Send on Messenger 09/10, then call 09/11 if no reply. One contact = whole group."',
  '"Send TODAY 09/09 (Messenger), then call 09/10 evening if no reply. One contact = whole group."'),
]
for old, new in repl:
    if old not in src:
        print("WARN not found:", old[:60])
    src = src.replace(old, new)

open("build_sheet.py", "w", encoding="utf-8").write(src)
print("patched OK")
