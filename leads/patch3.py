#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch 3: King's field-verified WhatsApp checks + alternate contact paths."""
src = open("build_sheet.py", encoding="utf-8").read()

def rep(old, new, count=1):
    global src
    if old not in src:
        print("WARN not found:", old[:70])
        return
    src = src.replace(old, new, count)

# ---------- Sasse LEADS row ----------
rep('"Likely same", "Fr. Njanto Jude (Principal)", "Phone/WhatsApp",',
    '"N/A — 677 195 500 NOT on WhatsApp (King verified 09/09)", "Fr. Njanto Jude (Principal)", "TikTok DM + email + call",')
rep("DEMO BUILT: sjc-sasse-homepage.html.",
    "DEMO BUILT: sjc-sasse-homepage.html. 2012 'Best School in West Africa' + 2013 'Best School in Cameroon' (Fondation Terre d'accueil) — demo material. WhatsApp 677 195 500 NOT available (King 09/09) → TIKTOK DM @SJC - The Republic + email sajoscol@gmail.com + call. Diocesan education line: +237 334 745 678.")

# ---------- SAHISCOL LEADS row ----------
rep('"+237 233 322 551 / +237 682 122 959", "682 122 959 (likely)", "Headmaster (N/V)", "WhatsApp",',
    '"+237 233 322 551 / +237 334 745 678 (diocesan line)", "TRY 334 745 678 on WhatsApp; 682 122 959 is NOT school\'s (King verified 09/09 — wrong profile)", "Headmistress (N/V) — GIRLS\' school", "WhatsApp (new no) + Messenger + landline + email",')
rep("Use broken-website pitch. Close to us (Limbe).",
    "Use broken-website pitch. Close to us (Limbe). DIOCESAN school (Buea Diocese portfolio: 'Saint Ann Girls College Limbe', New Town) — GIRLS' school, adjust demo wording. sahiscol@gmail.com. Published mobile was stale (someone else's number) = further evidence of abandoned digital presence.")

# ---------- NHICHS LEADS row ----------
rep('"+237 677 754 290", "Likely same", "N/V", "WhatsApp",',
    '"+237 677 754 290 / 680 738 111 / 679 246 223", "TRY 680 738 111 or 679 246 223 on WhatsApp; 677 754 290 NOT on WhatsApp (King verified 09/09)", "Director (mehdi@nhiss.org)", "WhatsApp (other no) + Director email + phone",')
rep("GCE grammar+commercial centre; scholarships; info@nhichs.org.",
    "GCE grammar+commercial centre; scholarships; info@nhiss.org (updated). inovedu 4.4/5 (40 reviews, 271 likes); tuition 192k–274k FCFA. Director email = mehdi@nhiss.org (direct line to decision maker).")

# ---------- Deep Dive rows ----------
# 1) Sasse channel + action
rep('"WHATSAPP +237 677 195 500 (text-first); sajoscol@gmail.com",',
    '"TIKTOK DM @SJC - The Republic + EMAIL sajoscol@gmail.com (677 195 500 NOT on WhatsApp — King 09/09); call in evening; diocesan line +237 334 745 678",')
rep('"Send TODAY 09/09 (school office hours). FU1 09/11, FU2 09/14, FU3 09/18. No walk-in."',
    '"TikTok DM + email TODAY 09/09 (same copy, email subject below in chat log); call 677 195 500 in evening if no reply. FU1 09/11, FU2 09/14, FU3 09/18. No walk-in."')
# 2) SAHISCOL channel + action
rep('"WHATSAPP +237 682 122 959 (text-first); info@sahiscol.org",',
    '"TRY 334 745 678 on WhatsApp; MESSENDER (FB page); landline 233 322 551; info@sahiscol.org / sahiscol@gmail.com",')
rep('"Send TODAY 09/09 (school office hours). FU1 09/11, FU2 09/14, FU3 09/18. No walk-in."',
    '"WhatsApp 334 745 678 + Messenger TODAY 09/09; landline if silent. FU1 09/11, FU2 09/14, FU3 09/18. No walk-in. Note: GIRLS\' school — adjust demo wording if built."')
# 3) NHICHS channel + action
rep('"WHATSAPP +237 677 754 290 (text-first); info@nhichs.org",',
    '"TRY 680 738 111 / 679 246 223 on WhatsApp; DIRECTOR EMAIL mehdi@nhiss.org; info@nhiss.org",')
rep('"Send TODAY 09/09. FU1 09/11, FU2 09/14, FU3 09/18."',
    '"WhatsApp 680 738 111 TODAY; if not on WA, email the DIRECTOR (mehdi@nhiss.org) — straight to decision maker. FU1 09/11, FU2 09/14, FU3 09/18."')

open("build_sheet.py", "w", encoding="utf-8").write(src)
print("patch3 OK")
