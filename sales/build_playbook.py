#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build AMK Sales Process v1.0 playbook (DOCX)."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

GREEN = RGBColor(0x14, 0x35, 0x1F)
GOLD = RGBColor(0x8A, 0x6D, 0x14)
GREY = RGBColor(0x5C, 0x66, 0x60)
RED = RGBColor(0xC0, 0x00, 0x00)

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)

def h1(t):
    p = doc.add_heading(t, level=1)
    for r in p.runs:
        r.font.color.rgb = GREEN
    return p

def h2(t):
    p = doc.add_heading(t, level=2)
    for r in p.runs:
        r.font.color.rgb = GREEN
    return p

def para(t, bold=False, color=None, size=None, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(t)
    r.bold = bold
    r.italic = italic
    if color: r.font.color.rgb = color
    if size: r.font.size = Pt(size)
    return p

def bullets(items):
    for it in items:
        doc.add_paragraph(it, style="List Bullet")

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for i, htxt in enumerate(headers):
        hdr[i].text = ""
        r = hdr[i].paragraphs[0].add_run(htxt)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        from docx.oxml.ns import qn
        shd = hdr[i]._element.get_or_add_tcPr()
        e = shd.makeelement(qn("w:shd"), {qn("w:val"): "clear", qn("w:fill"): "1F3864"})
        shd.append(e)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = str(v)
            for p in cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
    return t

# ---------------- COVER ----------------
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\n\nAMK")
r.bold = True; r.font.size = Pt(40); r.font.color.rgb = GREEN
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Développement web & Solutions Digitales")
r.font.size = Pt(14); r.font.color.rgb = GOLD
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\nSALES PROCESS v1.0\nFive stages · ICP · BANT · MQL → SQL\n\nWebsite products for private schools — Douala · Yaoundé · Buea · Limbe\nPrepared by Tony (Marketing & Sales) for Akwo King — 09/09/2026")
r.font.size = Pt(12); r.font.color.rgb = GREY
doc.add_page_break()

# ---------------- 1. OVERVIEW ----------------
h1("1. The process at a glance")
para("One sales cycle, five stages, run as a flywheel — not a line. Every stage has an ENTRY condition (when work starts) and an EXIT gate (when the lead moves on). A lead that cannot pass a gate is not forced through; it is parked, verified, or archived with a reason. This is what makes the funnel measurable: you always know exactly which stage a lead is in, and where the bottleneck is.", bold=False)
table(
    ["Stage", "Name", "Goal", "Exit gate (to move on)"],
    [
        ["1", "PROSPECTING", "Find & capture qualified schools with full intel", "In CRM with score 0–20 + verified channel"],
        ["2", "QUALIFYING (MQL → SQL)", "Message the right leads; separate 'worth messaging' from 'worth selling to'", "MQL: ICP 5/7 + reachable. SQL: replied + BANT complete (B+A+N+T)"],
        ["3", "DEMO & ENGAGEMENT", "Send the custom homepage concept; create the conversation", "They ask the price / request changes / set a call"],
        ["4", "OFFER & CLOSE", "Turn the conversation into a signed deal", "50% deposit paid (MoMo/bank)"],
        ["5", "DELIVERY, PROOF & GROWTH", "Deliver, collect testimonial, generate referrals", "Case study live + ≥1 referral → back to Stage 1"],
    ])
para("")
h2("Operating principles (from our references)")
bullets([
    "Measure everything — you can't improve what you don't measure. The Daily Tracker is updated the same day, no exceptions (Patrick Dang).",
    "Never sell in discovery. Stage 2–3 conversations are about the school's problem, not our product. Only present what they said they need.",
    "Speed is a multiplier: a reply within minutes/hours beats a polished reply 3 days later; 50% of prospects go with whoever responds first (Hormozi). SLA: any inbound reply answered in <24h, ideally same day.",
    "Permission before demo. We never send a concept unsolicited — we earn the 'send it' first.",
    "The close is just asking for the order. If Stages 2–3 were done right, the prospect already wants to buy — no pressure tactics.",
    "Deliver > close. Delivery quality is what produces the testimonial and the referral that feed Stage 1 with warm leads.",
])

doc.add_page_break()
# ---------------- 2. STAGE 1 ----------------
h1("2. Stage 1 — PROSPECTING")
h2("2.1 Sources (rotate daily)")
bullets([
    "Google Maps — the 13-query EN+FR set per city (private schools / écoles privées / collège privé / lycée privé / bilingual schools…).",
    "Facebook — official pages: activity, followers, admissions posts, phone numbers in page info.",
    "Directories: inovedu.net (ratings, tuition, emails), ecolesaucameroun.com (6,989 schools, diocese status), 237zoom.com, banabam.org (Douala), cameroondebate blog (GCE centre lists).",
    "GCE centre lists (camgceb.org PDFs) — every centre number = a real, examined, active school.",
    "Diocese pages (bueadiocese.org, cesbueadiocese.org) — Catholic schools with phones/emails.",
    "TikTok — SW-region schools run live admissions campaigns there (DSCC, Sasse).",
])
h2("2.2 Data standard (a lead is not 'captured' until it has)")
bullets([
    "Official name + neighborhood/city · Language (FR/EN/Bilingual) · Facebook URL (if any)",
    "Website URL + verified status: A None / B Good / C Outdated / D Broken / E Expired — ALWAYS click the site (fetch it). D/E = GOLD, flag immediately.",
    "Phone (and 2nd number if found) · WhatsApp availability CHECKED (open the number — King's rule: no number goes into the plan unverified) · Email if any",
    "Decision maker: founder / proprietor / director / principal — search '[school] directeur / proprietor / founder'; if unknown, first message asks for them.",
    "Activity signals: last post date, admissions campaign?, events, exam results, tuition range (budget proxy).",
])
h2("2.3 Score & quota")
para("Score every lead 0–20 with the rubric in the co-founder brief (website problem +4/+3/+2, marketing +3/+2/+2, business quality +2×4, digital opportunity +2/+2/+1). Quota: 10 qualified leads/day. 12+ = A+ (research immediately, build demo if obvious). 9–11 = A (contact). 6–8 = B (contact if time). <6 = C (park/verify).")
para("Exclusions (never capture): public schools (no budget), schools <50 students with no branches, closed/absent schools (2+ years of silence).", bold=True)

# ---------------- 3. STAGE 2 ----------------
doc.add_page_break()
h1("3. Stage 2 — QUALIFYING: MQL and SQL (ICP + BANT)")
para("Qualifying happens in TWO gates. Marketing qualifying (MQL) asks: 'Is this the kind of business we win?' Sales qualifying (SQL) asks: 'Is this a live buyer right now?'", bold=True)

h2("3.1 ICP — Ideal Customer Profile ('the ABC Bilingual College')")
table(
    ["Dimension", "Ideal", "Acceptable", "Disqualify"],
    [
        ["Type", "Private nursery/primary/secondary school or school group (multi-campus)", "Single campus, confessional (Catholic/Presbyterian/Baptist) or laïc", "Public school; university (different budget/process)"],
        ["City", "Douala · Yaoundé · Buea · Limbe (bilingual advantage: FR+EN markets)", "Other cities after first 50", "—"],
        ["Size", "≥300 students, or group of campuses", "≥100 students", "<50 students, no branches"],
        ["Tuition (budget proxy)", "≥₣150k/year (mid-up)", "≥₣100k/year", "<₣50k (can't absorb ₣100k)"],
        ["Website", "D Broken / E Expired — HOTTEST (they already valued a site)", "A None (with active socials) / C Outdated", "B Good (park → upsell list)"],
        ["Marketing", "Active FB/TikTok, admissions campaign running, events, results posted", "Occasional posts", "Dead everywhere for 12+ months"],
        ["Language fit", "Any — every AMK site is built EN|FR by standard (bilingual country)", "—", "—"],
        ["Buyer reachable", "Proprietor/director/principal identified OR reachable number", "Head office that connects us", "Only unreachable gatekeepers"],
    ])

h2("3.2 MQL gate — Marketing Qualified Lead")
para("A lead is MQL when it passes 5 of 7 ICP checks AND its channel is verified working. Our 0–20 score already approximates this — score ≥9 with verified channel = MQL.")
table(["#", "MQL check", "Verified by"],
 [
  ["1", "Private school/group in target city", "Directory / Maps"],
  ["2", "≥100 students or multi-campus", "Directory, tuition, GCE lists"],
  ["3", "Tuition ≥₣100k/yr (budget proxy)", "inovedu tuition, publicized fees"],
  ["4", "Website problem A/C/D/E", "We click the site ourselves"],
  ["5", "Active social or admissions activity (≤60 days)", "FB/TikTok last post"],
  ["6", "Decision maker identifiable or reachable", "Search '[school] directeur/proprietor'"],
  ["7", "Professional management signals (group, awards, events)", "Press, diocese, GCE results"],
  ["+", "CHANNEL VERIFIED — WhatsApp opened / FB page live / email exists (mandatory)", "King checks the number"],
 ])
para("MQL action: personalized first message — specific problem → specific message (no-site / broken-site / outdated-site / active-admissions / bilingual variants from the brief). Follow-up cadence: FU1 M+2, FU2 M+4, FU3 M+7 (final, graceful). No reply after FU3 → archive to C with reason. No harassment, no disappearing.", bold=True)

h2("3.3 SQL gate — Sales Qualified Lead (BANT)")
para("A reply alone does NOT make an SQL. The reply must complete BANT. Rule: B + A + N + T all green = SQL → move to Stage 3/4. Any red on A (authority) or N (need) = do NOT make an offer; keep qualifying or park.")
table(
    ["BANT", "What it means for us", "Question to ask (EN)", "Question to ask (FR)"],
    [
        ["B — Budget", "They can absorb ₣100k. Proxies: tuition ≥₣100k, multi-campus, active investment. ₣100k ≈ one student's annual tuition — use that framing, don't open by asking 'what's your budget'.",
         "To propose the right size of project — what does the school usually plan for its communication and admissions for the school year?",
         "Pour que je propose la bonne taille de projet — quel budget l'établissement prévoit habituellement pour sa communication et ses admissions sur l'année ?"],
        ["A — Authority", "We talk to the founder/proprietor/director/principal — never park with a secretary or teacher. If it's not them: get the name AND the number of the person who decides.",
         "For a project like this, are you the one who makes the decision, or should I send the concept to the director/proprietor?",
         "Pour ce type de projet, êtes-vous la personne qui décide, ou dois-je adresser l'aperçu au directeur/à la propriétaire ?"],
        ["N — Need", "Already identified at Stage 1 (no site / broken site / active admissions with nowhere to land). Confirm it in their words — the school must say the problem out loud.",
         "When parents can't find reliable information about the school online, what do they usually do? … And what should the website achieve first — admissions, image, or parent communication?",
         "Quand les parents ne trouvent pas d'informations fiables sur l'école en ligne, que font-ils en général ? … Et la priorité du site : les admissions, l'image, ou la communication avec les parents ?"],
        ["T — Timeline", "Admission season (Sep–Nov) is built-in urgency: 'your campaign is running NOW, parents are searching this week'. Accept ≤6–8 weeks. Later than that → park with a dated re-entry (next admission cycle).",
         "Your 2026/2027 admissions are running right now — would you like the first version live before the end of the admissions period?",
         "Vos admissions 2026/2027 sont en cours — souhaiteriez-vous que la première version soit en ligne avant la fin des inscriptions ?"],
    ])
para("BANT log: for every SQL, write B/A/N/T + one line of evidence in the Notes column. This is what the weekly review reads.", bold=True)

# ---------------- 4. STAGE 3 ----------------
doc.add_page_break()
h1("4. Stage 3 — DEMO & ENGAGEMENT")
bullets([
    "Permission first: the message asks 'would you like me to send the preview?' — the demo goes out only after a yes. (Brief §7–8.)",
    "Build standard: custom single-file homepage, EN|FR toggle, mobile-first, sections = programs · admissions (current campaign) · excellence/results · campus life · contact (WhatsApp button) · footer 'Concept prepared for [school] by AMK'. Template: sjc-sasse-homepage.html. Build time target: ≤24h after the yes.",
    "Show only what they raised: if the pain was 'broken site', lead with the before/after; if it was 'admissions attention leaking', lead with the admissions section. No feature dumping (Patrick Dang: don't introduce anything new in the demo).",
    "Conversation questions (max 3): (1) 'What do you want parents to do first on the site — apply, call, or WhatsApp?' (2) 'Who on your side will give me the school info and photos?' (3) 'If you like the direction, I can have the first version in 3–5 days — is the timing good?'",
    "Exit gate: they ask the price / request changes / name a date for a call or visit. Otherwise → still Stage 3, follow up once at 48h, then park at C.",
])

# ---------------- 5. STAGE 4 ----------------
h1("5. Stage 4 — OFFER & CLOSE")
para("THE OFFER — CONFIRMED BY KING 09/09/26: founding-client price ₣100,000 (first two school projects) — 50% to start (₣50,000), 50% on delivery (₣50,000) — first version ready in 3–5 days from receiving the school's info and materials. Scope: main pages in ENGLISH AND FRENCH (EN|FR is the AMK standard — we are in a bilingual country), WhatsApp integration, domain + hosting setup, mobile optimization. No extra charge for the bilingual content.", bold=True)
para("Sequence after the demo conversation: problem recap → direction confirmation → scope → price with payment split → ask for the deposit. One ask, no pressure: 'Shall we start this week so the first version is live before the end of admissions?'")
h2("Objection handling (FR / EN)")
table(["Objection", "Response"],
 [
  ["« C'est trop cher » / Too expensive",
   "« 100 000 FCFA, c'est moins qu'une année de scolarité d'un seul élève. Et vous investissez déjà dans vos campagnes d'admissions — le site est là où toute cette attention doit atterrir. » / '₣100k is less than one student's annual tuition. You already invest in admissions campaigns — the website is where all that attention lands.'"],
  ["« Facebook suffit déjà » / Facebook is enough",
   "« Facebook touche ceux qui voient déjà vos publications. Le site est trouvé par ceux qui cherchent 'école privée à Douala' — c'est là que se joue la crédibilité. Une école sans site semble plus petite qu'elle n'est. » / 'Facebook reaches people who already see your posts. The website is found by the people who search — that's where credibility is won.'"],
  ["« Le dernier site nous a déçus / il s'est cassé » / Last site broke",
   "« C'est exactement le problème que je corrige : je prends en charge le domaine et l'hébergement correctement, et je vous montre à vérifier le site en 5 secondes depuis n'importe quel téléphone. » / 'That's exactly what I fix — domain and hosting handled properly, and I'll show you how to check it in 5 seconds on any phone.'"],
  ["« Il faut demander au conseil » / Need to ask the board",
   "« Bien sûr. Je peux vous envoyer l'aperçu pour que vous le leur présentiez ? Lequel jour serait bien pour que je revienne vers vous — jeudi ? » / 'Of course — may I send you the preview to present to them? Which day works for me to follow up — Thursday?' (always lock a date)"],
  ["« Qui s'en occupe après ? » / Who maintains it?",
   "« Un mois de support est inclus : ajustements de contenu, correctifs. Ensuite, la mise à jour de contenu est facturée séparément — et je vous forme en 30 minutes pour gérer les bases. » / 'One month of support is included (content tweaks, fixes). After that, content updates are quoted separately — and I train your team in 30 minutes.'"],
  ["« On verra après les résultats » / Let's see after exams",
   "« Très bien. Je vous garde votre place sur la liste des clients fondateurs — elle est limitée à deux projets sur cette période. » / 'Understood — I'll keep your spot on the founding-client list; it's limited to two projects this round.'"],
 ])
para("Exit gate: 50% deposit received (MoMo/bank, receipt saved in Notes). Deal is real only at deposit.", bold=True)

# ---------------- 6. STAGE 5 ----------------
h1("6. Stage 5 — DELIVERY, PROOF & GROWTH")
bullets([
    "Build in 3–5 days with a daily WhatsApp progress update (screenshot of what's new). This is also marketing: the school experiences us working.",
    "Handover checklist: site live on school's domain · WhatsApp button tested from a phone · contact info correct · school admin knows how to change basic text · hosting/domain registered in the school's name where possible.",
    "Collect the 50% balance at handover (not 'next month').",
    "Testimonial: ask within 24h of handover — one video (30s: 'the site is beautiful, parents can now find everything') + one written quote. Script: 'A small video of you in front of the school would help us a lot — parents trust parents and headmasters, not agencies.'",
    "Referral ask (the flywheel): 'You know other school directors in your network — is there someone who would also benefit? I take on two more projects at this founding price this month.' Target: ≥1 referral per client.",
    "Upsell menu: results page (CEP/BEPC/GCE) · e-learning/online registration (see Siantou) · other campuses of the group · hosting/renewal (recurring) · parent info microsite · ongoing bilingual content updates. (EN|FR on the site itself is STANDARD — never an upsell.)",
    "Case study: before/after (old site screenshot vs new), time-to-live, one quote → used in every future Stage 3 message. 'A Douala school saw this' beats 'we make websites'.",
])

# ---------------- 7. METRICS ----------------
doc.add_page_break()
h1("7. Funnel metrics & weekly review")
para("Every Friday (or Sunday), fill the Daily Tracker totals for the week and compare to targets:")
table(
    ["Stage", "KPI", "Target (month 1)", "Bottleneck if low"],
    [
        ["1", "Qualified leads captured/day; MQL rate", "10/day; ≥40% of captured", "Targeting / ICP too loose → tighten queries & exclusions"],
        ["2", "Messages sent; reply rate; MQL→SQL", "20+ sent; 15–25%; ≥25% of replies", "Reply low → message/targeting. SQL low → we're messaging non-buyers (fix ICP/BANT)"],
        ["3", "Demos sent; demo→conversation; →offer request", "Every SQL gets a demo; ≥50%; ≥30%", "Demos low → permission ask too weak. Conversation low → demo not personalized"],
        ["4", "Offers made; offer→deposit", "≥40% of conversations; ≥50% of offers", "Offers low → positioning/need. Deposit low → price/urgency/payment friction"],
        ["5", "On-time delivery; testimonials; referrals", "100%; 100%; ≥1/client", "Anything <100% → delivery process, not sales"],
    ])
para("Diagnosis logic (co-founder §17): 100 messages / 3 replies = outreach problem. 100 / 20 / 0 demos = qualification problem. 20 demos / 0 offers = positioning problem. 8 offers / 3 deposits = 🔥 it works — scale.")
para("Month-1 objective: first ₣100,000 inside 30 days → 2–3 deposits by end of month 1 = ₣200–300k, which ends the founding-price window.")

h1("8. References")
bullets([
    "BANT framework & 16 qualification questions — Salesforce, 'What Is BANT?' (salesforce.com/blog/sales/what-is-bant-lead-generation)",
    "6-step sales process, discovery discipline, referral flywheel — Patrick Dang, 'How To Improve Your Sales Process And Increase Business'",
    "Sales multipliers (respond <60s, first-responder wins 50%, availability hours) — Alex Hormozi, 'The Ultimate Sales Training for 2026'",
    "Co-founder prospecting brief (ICP archetype, scoring rubric, message variants, offer, follow-up system) — 09/09/2026",
])

out = "/home/user/agency/sales/AMK-Sales-Process-v1.docx"
doc.save(out)
print("saved", out)
