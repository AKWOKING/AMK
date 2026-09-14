# -*- coding: utf-8 -*-
"""Regenerate leads/Daily Ops.csv (invitation-first Tue 15 Sep plan)."""
import csv, pathlib

rows = []
def r(*cols): rows.append(list(cols))

r("AMK — DAILY OPS  ·  open this tab every morning (10 min)  ·  1-hour reply rule: 09:00–21:00, 7 days", "", "", "", "")
r("", "", "", "", "")
r("TUE 15 SEP — DIGITAL-FIRST DAY (no campus visits): plan = sales/Invitation-First-Replan-2026-09-15.md; intel per school = Walk-In-Deep-Dives", "", "", "", "")
r("", "", "", "", "")
r("① KILL LIST — hot leads get daily visible attention", "", "", "", "")
r("Lead", "Why hot", "Next action (TODAY)", "Done?", "Re-check")
r("OraCare237 (Buea) — CLINIC PILOT",
  "18/20 · msg 1 sent Mon · no reply yet · v3 LIVE https://oracare-concept.vercel.app/",
  "REPLY-WATCH all day (1h rule). Silent → FU1 Wed 16 (pack §7). If he replies: branch sheet pack §1; send live v3 link.", "☐", "daily")
r("SJC Sasse (Buea) — KILL LIST #2",
  "16/20 · active TikTok admissions · concept LIVE https://sjc-sasse-concept.vercel.app/",
  "07:45: TikTok DM @saintjosephcollegesasse + email sajoscol@gmail.com (pack §3). Visit only if they invite one.", "☐", "Tue")
r("Baptist Comp. College Great Soppo — NEW",
  "12/B+ · GCE 11708 · no site · SURE WA 679 65 07 07 (King-confirmed, school FB-page line)",
  "08:30 WhatsApp msg 1 (replan §4) → yes = nameless sample link + invite-choice (Thu/Fri walkthrough vs WhatsApp). Baptist protocol: principal then education office.", "☐", "Tue")
r("PCSS Buea — NEW",
  "12/B+ · 700 boarders, founded 1993 · no site · SURE WA 652 075 229 (official) + champion teacher Kinang 675 533 321",
  "08:30 WhatsApp msg 1 (replan §4, boarding angle). No steer by noon → Kinang door-opener text. Visit by invitation; Presbyterian education office ratifies.", "☐", "Tue")
r("St. Theresa STIBCCOL Molyko — NEW",
  "14/A · ~128 GCE candidates, fees 181-237k · active TikTok @stibccol (to 14 Sep) · candidate WA 679 15 10 75 (official FB page)",
  "TONIGHT verify 679 15 10 75 on WA (profile check). Tue AM: TikTok DM @stibccol regardless + WhatsApp if confirmed (replan §4).", "☐", "Tue")
r("NHICHS (Limbe)",
  "11/20 · branded domain expired, technical dept launching",
  "Midday: director email mehdi@nhiss.org (pack §4, email-only leg). Build concept within 24h of any yes.", "☐", "Tue")
r("Baird Memorial Bonduma — CONDITIONAL",
  "has weak self-built site bairdmemorial.com (typos) · candidate WA 677 87 53 95 / 677 78 04 05",
  "TONIGHT: open bairdmemorial.com on phone + WA-check both. Dead site + WA yes → 08:35 msg (replan §4). Site works → card only Wed, park as refresh.", "☐", "Tue")
r("Summerset (SUBICOL) Wokoko — FLAGSHIP",
  "15/A · ~1,000 students, Principal Tata, publicly slower 2026 enrollment · NO phone online, FB dead since 2015",
  "09:00 parallel email to smbicol@yahoo.com (replan §4, weak leg). Effective first touch = Wed sealed-envelope card drop addressed to Principal Tata.", "☐", "Wed")
r("Collège de la Retraite (Yaoundé)", "PARKED (elders board + maintained site)", "Off board; revival triggers logged.", "☐", "Q4")
r("COMOBIL / Groupe WAFO (Douala)", "PARKED 14 Sep (King decision) — #1 revival lead",
  "Triggers: FB Page / Douala trip / comobil.com dark / WAFO referral. Concept hosted /comobil/.", "☐", "review Fri")
r("SAHISCOL (Limbe)", "PARKED 14 Sep confirmed",
  "Revival: site outage/expiry, failed admissions push, Limbe/diocese referral.", "☐", "review Fri")
r("", "", "", "☐", "")
r("", "", "", "", "")
r("② REPLY QUEUE — 1-hour rule · every chat ends with a booked next step (BAMFAM)", "", "", "", "")
r("Lead", "Last activity", "Next step", "Due", "Done?")
r("OraCare237", "Mon 14 msg 1 sent; no reply yet", "§1 branches; silence → FU1 Wed 16.", "Wed", "☐")
r("Tue WhatsApp/TikTok schools (Baptist, PCSS, St Theresa)", "Going out 08:30 Tue",
  "Yes → nameless sample link (hosting/samples project) + invite-choice Thu/Fri; named concept within 24h for warm specific requests; questions answered within 1h.", "Tue", "☐")
r("SJC Sasse", "DM + email 07:45 Tue", "Watch TikTok + Gmail; invite visit only.", "Tue", "☐")
r("Wed card-drop inbound scans", "Cards dropped Wed AM",
  "QR inbound = school initiates → reply within 1h, preview link, then invite-choice.", "Wed", "☐")
r("GBP verification", "UNDER REVIEW", "Keep 677 78 96 31 reachable; check weekly.", "Wed", "☐")
r("", "", "", "", "☐")
r("", "", "", "", "")
r("③ WED 16 — ASYNC CARD-DROP SWEEP (~1h, NO meetings; invitations only after)", "", "", "", "")
r("· Numberless gates, one boda loop: St Bernard (Garden Park, opp Orange, attn Dr Fomba) → Salvation (near CUIB) → Summerset (Check Point Wokoko opp ENAMEN Pharmacy, attn Principal Tata) → NABESK (Nabesk junction) → Baird same road only if site dead.", "", "", "", "")
r("· Sealed envelope 'For: the Principal', handwritten bilingual line on card back (replan §3); capture gate-staff name + any mobile; never wait for the principal.", "", "", "", "")
r("· St Sylvester Muea only if already in Muea; Bishop Jules Bokwaongo folds into an invited Great Soppo trip (do not cold-drop a diocesan college).", "", "", "", "")
r("· Wed PM / Thu / Fri: invited 10-min walkthroughs batched by quarter (Molyko/Wokoko one trip, Great Soppo/Bokwaongo one trip); confirm principal present before leaving home.", "", "", "", "")
r("· If silent after Wed sweep: FU follows the email/message M+2 rhythm; no second uninvited visit.", "", "", "", "")
r("", "", "", "", "")
r("④ TONIGHT PREP (Mon, 20 min)", "", "", "", "")
r("· WA-verify profiles: 679 15 10 75 (St Theresa), 677 87 53 95 + 677 78 04 05 (Baird). First three (679 Baptist, 652 PCSS, 675 Kinang) already confirmed.", "", "", "", "")
r("· Open bairdmemorial.com on phone (dead=full pitch, works=light card).", "", "", "", "")
r("· Deploy hosting/samples as its own Vercel project (e.g. amk-web) the same way as the named concepts; send AMK the URLs — cold leads see NAMELESS samples only.", "", "", "", "")
r("· Print TWO A4 sheets of bilingual cards sales/walkin/walk-in-cards.html = 16 cards; prepare 5 envelopes.", "", "", "", "")
r("· Read Walk-In-Deep-Dives sections for Baptist, PCSS, St Theresa before 08:30.", "", "", "", "")
r("", "", "", "", "")
r("⑤ DRILL — 15 min/day (voice memo/friend — never on real leads)", "", "", "", "")
r("Day", "Segment", "", "", "")
r("Tue", "30-SECOND TEXT OPEN: read msg 1 aloud EN; rehearse the invite-choice line: '10 minutes Thursday or Friday after morning classes, or all here on WhatsApp?'", "", "", "")
r("Wed", "FLIPS: 'It's expensive' → one missed registration worth per term? · 'I need to think' → timing or priority?", "", "", "")
r("Thu", "CARDONE + REFERRAL: 'Have you heard enough to decide?' · 'Who do you know that's like you?' (use on invited walkthroughs)", "", "", "")
r("Fri", "Friend plays skeptical principal — full invited-visit run; rehearse price+pause.", "", "", "")
r("Mon", "PRICE + PAUSE: '…100 000 francs, la moitié pour commencer.' 10 seconds silence.", "", "", "")
r("Sun", "OFF (30 min: pipeline review, schedule FUs, prep top 3 + write Weekly-Report-2026-09-20.md)", "", "", "")
r("", "", "", "", "")
r("⑥ TONIGHT — 5 min", "", "", "", "")
r("· Log every send/reply/scan/invitation in Leads 50 / Daily Tracker same day.", "", "", "", "")
r("· Any 'yes send it' → sample link immediately; named concept request → AMK builds within 24h; move to kill list + book time.", "", "", "", "")
r("· Open blockers (MoMo details · clinic demo source folder) chase in weekly plan, not at close time.", "", "", "", "")

out = pathlib.Path("leads/Daily Ops.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerows(rows)
print("wrote", out, len(rows), "rows")
