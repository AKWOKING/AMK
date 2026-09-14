#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch 4: add Pipeline-5-Stages sheet; move outreach to Monday; add planned row to tracker."""
src = open("build_sheet.py", encoding="utf-8").read()

def rep(old, new, count=1):
    global src
    if old not in src:
        print("WARN not found:", old[:70])
        return
    src = src.replace(old, new, count)

# ---- Deep Dive next actions -> Monday + relative FUs ----
rep('"TikTok DM + email TODAY 09/09 (same copy, email subject below in chat log); call 677 195 500 in evening if no reply. FU1 09/11, FU2 09/14, FU3 09/18. No walk-in."',
    '"STAGE 2 — TikTok DM + email on MON (outreach starts Monday). FU1 M+2, FU2 M+4, FU3 M+7, then archive. No walk-in unless invited."')
rep('"WhatsApp 334 745 678 + Messenger TODAY 09/09; landline if silent. FU1 09/11, FU2 09/14, FU3 09/18. No walk-in. Note: GIRLS\' school — adjust demo wording if built."',
    '"STAGE 2 — WhatsApp 334 745 678 + Messenger on MON; landline if silent. FU1 M+2, FU2 M+4, FU3 M+7. No walk-in. GIRLS\' school — adjust demo wording if built."')
rep('"WhatsApp 680 738 111 TODAY; if not on WA, email the DIRECTOR (mehdi@nhiss.org) — straight to decision maker. FU1 09/11, FU2 09/14, FU3 09/18."',
    '"STAGE 2 — WhatsApp 680 738 111 on MON; if not on WA, email the DIRECTOR (mehdi@nhiss.org) — straight to decision maker. FU1 M+2, FU2 M+4, FU3 M+7."')
rep('"Send on Messenger 09/10. FU1 09/11, FU2 09/14, FU3 09/18."',
    '"STAGE 2 — Messenger on MON. FU1 M+2, FU2 M+4, FU3 M+7."')
rep('"Send on Messenger 09/10, then call 09/11 if no reply. One contact = whole group."',
    '"STAGE 2 — Messenger on MON, then call THU if no reply. One contact = whole group (5 institutions)."')

# ---- Pipeline sheet code, inserted before save ----
anchor = 'out = "/home/user/agency/leads/leads_50.xlsx"'
pipeline_code = '''
# ---------- Sheet 4: Pipeline - 5 Stages ----------
ws4 = wb.create_sheet("Pipeline - 5 Stages")
for c, htxt in enumerate(["Stage", "Name", "Goal", "Entry", "Exit gate", "Key actions", "SLA / cadence", "KPI target (month 1)"], 1):
    cell = ws4.cell(1, c, htxt)
    cell.font = Font(bold=True, color="FFFFFF"); cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True); cell.border = thin
stages = [
 ("1", "PROSPECTING", "Find & capture qualified schools with full intel", "Any school in target city", "In CRM with 0-20 score + channel VERIFIED (WhatsApp opened)", "Maps 13 queries EN+FR, Facebook, directories (inovedu/ecolesaucameroun/237zoom/banabam), GCE centre lists, diocese pages, TikTok", "10 leads/day; score same day", "MQL rate >=40% of captured"),
 ("2", "QUALIFYING (MQL->SQL)", "Message right leads; separate worth-messaging from worth-selling", "Lead in CRM", "MQL: ICP 5/7 + channel verified. SQL: replied + BANT complete (B+A+N+T, T<=8 weeks)", "Personalized first message (problem-specific variant); BANT conversation; log B/A/N/T + evidence in Notes", "Reply <24h; FU1 M+2, FU2 M+4, FU3 M+7 then archive C", "Reply 15-25%; MQL->SQL >=25% of replies"),
 ("3", "DEMO & ENGAGEMENT", "Send custom homepage concept; create conversation", "SQL (or A+ with obvious opportunity)", "They ask price / request changes / set a call", "Build EN|FR homepage <=24h after the 'yes'; show ONLY their stated problem; 3 conversation questions", "Send within 24h of permission; 1 follow-up at 48h", "Demo->conversation >=50%; ->offer request >=30%"),
 ("4", "OFFER & CLOSE", "Convert conversation into signed deal", "Positive conversation, need confirmed", "50% DEPOSIT PAID (MoMo/bank)", "Founding-client offer: 100,000 FCFA, 50/50, 3-5 days; scope pages+WhatsApp+domain/hosting+mobile; bilingual content = extra; ask for the deposit directly", "Offer within 48h of conversation; close window <=1 week", "Offer->deposit >=50%"),
 ("5", "DELIVERY, PROOF & GROWTH", "Deliver, collect proof, generate next leads", "Deposit paid", "Case study live + >=1 referral -> back to Stage 1", "Build 3-5 days with daily WhatsApp progress; handover checklist; balance 50%; testimonial (video+written); referral ask; upsell menu (EN|FR, results page, e-learning, other campuses, hosting)", "Delivery <=5 days; balance at handover", "On-time 100%; testimonials 100%; >=1 referral/client"),
]
for i, row in enumerate(stages, 2):
    for c, v in enumerate(row, 1):
        cell = ws4.cell(i, c, v)
        cell.alignment = Alignment(vertical="top", wrap_text=True); cell.border = thin
    ws4.cell(i, 1).font = Font(bold=True, size=11, color="C00000")

ws4.cell(8, 1, "CURRENT PIPELINE (as of 09/09/2026)").font = Font(bold=True, size=12)
for c, htxt in enumerate(["ID", "School", "City", "Score", "Priority", "Stage", "Next action"], 1):
    cell = ws4.cell(9, c, htxt)
    cell.font = Font(bold=True, color="FFFFFF"); cell.fill = head_fill
    cell.alignment = Alignment(vertical="center", wrap_text=True); cell.border = thin
pipe = [
 (1, "St. Joseph's College Sasse", "Buea", 16, "A", "2 — outreach MON", "TikTok DM + email; demo READY"),
 (2, "SAHISCOL (Saint Ann Girls College)", "Limbe", 9, "A", "2 — outreach MON", "WhatsApp 334 745 678 + Messenger; broken-site pitch"),
 (3, "NHICHS", "Limbe", 11, "A", "2 — outreach MON", "WhatsApp 680 738 111; else email Director mehdi@nhiss.org"),
 (4, "Collège de la Retraite", "Yaoundé", 17, "A", "2 — outreach MON", "Messenger; digitalization-priority hook"),
 (5, "COMOBIL / Groupe WAFO", "Douala", 18, "A", "2 — outreach MON", "Messenger; broken-domain pitch; 1 contact = 5 schools"),
 (6, "GS WAFO (separate entity)", "Douala", 12, "A", "2 — merged with #5", "Same contact as COMOBIL"),
 (7, "PCSS Buea", "Buea", 10, "B", "2 — backup (week 2)", "Verify headmaster name first"),
 (8, "PCSS Bonamoussadi", "Douala", 9, "B", "2 — backup (week 2)", "FB Messenger; find phone"),
 (9, "Divine Success Comprehensive College", "Douala", 8, "B", "1 — verify", "Verify 3 campuses + real name on Maps, then qualify"),
 (10, "Baptist High School Awae", "Yaoundé", 8, "B", "1 — verify", "Verify FB activity + website absence, then qualify"),
 (11, "NCHS Limbe", "Limbe", 6, "B", "1 — verify", "Find official FB + phone"),
 (12, "Collège de l'Excellence de Limbe", "Limbe", 9, "A", "2 — verify then MON+", "D site (500) confirmed; find phone via Maps/parents, then pitch"),
 (13, "COSBINAL / NAL", "Douala", 10, "C", "PARK", "Good recent site (Didacweb) — upsell list only"),
 (14, "Blessed Group of Schools", "Yaoundé", 12, "C", "PARK", "Good modern site — upsell: bilingual EN|FR, e-learning"),
 (15, "American School of Douala", "Douala", 9, "C", "PARK", "Strong incumbent site — long-term relationship play"),
 (16, "Siantou Group", "Yaoundé", 12, "C", "PARK", "CORRECTED 09/09: siantou-univ.com up + online pre-registration — upsell only"),
 (17, "Le Paradis des Anges", "Douala", 4, "C", "PARK", "Decent Wix site — upsell candidate later"),
 (18, "Rainforest International School", "Yaoundé", 7, "C", "PARK", "Good site — long-term play"),
 (19, "Les Génies (Akwa)", "Douala", 4, "C", "1 — verify", "Verify on Maps before anything"),
 (20, "La Semence (Bonamoussadi)", "Douala", 3, "C", "1 — verify", "Directory only"),
 (21, "Institut Polyvalent Fosso (Akwa)", "Douala", 4, "C", "1 — verify", "Anglo-Saxon section = bilingual angle"),
 (22, "Frankfils Comprehensive College", "Buea", 5, "C", "1 — verify", "GCE 11402; find FB/phone"),
 (23, "Salvation Bilingual HS (Molyko)", "Buea", 5, "C", "1 — verify", "GCE 11412; find FB/phone"),
 (24, "Marthlo Comprehensive Bilingual", "Buea", 5, "C", "1 — verify", "GCE 22037; find FB/phone"),
 (25, "Notre Dame des Apôtres", "Yaoundé", 5, "C", "1 — verify", "Girls' boarding; find contacts"),
 (26, "PGSS Limbe", "Limbe", 4, "C", "1 — verify", "Presbyterian network; find contacts"),
]
for i, row in enumerate(pipe, 10):
    for c, v in enumerate(row, 1):
        cell = ws4.cell(i, c, v)
        cell.alignment = Alignment(vertical="top", wrap_text=True); cell.border = thin
    if "outreach MON" in str(row[5]):
        ws4.cell(i, 6).fill = PatternFill("solid", fgColor="C6EFCE")
    elif row[5] == "PARK":
        ws4.cell(i, 6).fill = PatternFill("solid", fgColor="FFC7CE")
w4 = [6, 34, 12, 7, 9, 22, 52, 30]
for c, w in enumerate(w4, 1):
    ws4.column_dimensions[get_column_letter(c)].width = w

# ---- Daily Tracker: planned Monday row ----
tr_row = None
for r in range(2, ws3.max_row + 1):
    if str(ws3.cell(r, 1).value) == "2026-09-09":
        tr_row = r
        break
nr = (tr_row or 2) + 1
ws3.cell(nr, 1, "Mon (planned)")
ws3.cell(nr, 2, 0)
ws3.cell(nr, 3, 5)
ws3.cell(nr, 11, "Outreach start: 5 first messages (Sasse, SAHISCOL, NHICHS, La Retraite, COMOBIL) — all STAGE 2 per Sales Process v1.0.")
for c in range(1, 12):
    ws3.cell(nr, c).border = thin

'''
i = src.index(anchor)
src = src[:i] + pipeline_code + src[i:]
open("build_sheet.py", "w", encoding="utf-8").write(src)
print("patch4 OK")
