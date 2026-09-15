# -*- coding: utf-8 -*-
"""Regenerate leads/Daily Ops.csv (invitation-first + clinic-first Tue 15 Sep)."""
import csv, pathlib

rows = []
def r(*cols): rows.append(list(cols))

r("AMK — DAILY OPS  ·  open this tab every morning (10 min)  ·  1-hour reply rule: 09:00–21:00, 7 days", "", "", "", "")
r("", "", "", "", "")
r("TUE 15 SEP — DIGITAL-FIRST, CLINICS FIRST (King: clinics have more potential than schools). Plan = sales/Invitation-First-Replan-2026-09-15.md + sales/Clinic-Batch-2026-09-15.md. STANDING (King): every msg 1 goes WITH its mockup image (demos/shots/*-wa.jpg). DEPLOY GATE: amk-cm.vercel.app/sample-clinic.html + /mitoc.html still 404 and homepage stale — redeploy amk-site.zip before any clinic nameless link is shared (MITOC named link lives separately at mitoc-concept.vercel.app).", "", "", "", "")
r("", "", "", "", "")
r("① KILL LIST — hot leads get daily visible attention", "", "", "", "")
r("Lead", "Why hot", "Next action (TODAY)", "Done?", "Re-check")
r("⭐ Solidarity Clinic & Laboratory (Solidarity Health Foundation, Malingo/Molyko) — CLINIC #1",
  "15/A · 24h not-for-profit clinic+lab+maternity+pharmacy founded 1998 · Google 4.0 stars/54 reviews/21 photos BUT no website/booking ('Add website') · founder Dr Peter Nde Fon DIED 2020, current director unknown (gatekeeper routing) · clinic line 677 61 57 57 IS NOT ON WHATSAPP (King-checked 15 Sep); 691 63 29 41 is Dr Njang's PERSONAL WA - DO NOT TEXT about Solidarity",
  "WHATSAPP BLOCKED on front line: (1) quick WA-check admin 677 61 12 07 (SHF-CIG UN-registry number, unverified) -> if it answers as the clinic, attach demos/shots/mockup-clinic-wa.jpg FIRST then send the §1 nameless msg (live link held until redeploy clears /sample-clinic.html 404); (2) if not, Solidarity moves to WED sealed-envelope sweep addressed to 'the current medical director or the clinic manager', never a personal name; (3) landline never cold-called; 691 63 29 41 Dr Njang personal = HOLD forever on Solidarity.", "☐", "Tue")
r("⭐ Midas Touch Optic Center MITOC (Molyko-Malingo) — CLINIC #2 · AWAITING REPLY",
  "12/B+ · full optician (refract, prescribe, mount lenses) · WA Business 'MITOC' 678 90 89 62, catalogue live, 09:00-18:00 = OWNER-BUYER line · named concept LIVE https://mitoc-concept.vercel.app · mockup demos/shots/mockup-mitoc-wa.jpg held",
  "MSG 1 SENT Tue 08:35 (two ticks). No chase today; FU1 Thu 17 / FU2 Sat 19 / FU3 Tue 22 (OWNER-BUYER only, then stop). On warm yes: mitoc-concept link + walkthrough choice. Do NOT share amk-cm /mitoc.html (404 until redeploy).", "☑", "Thu")
r("OraCare237 (Buea) — CLINIC PILOT",
  "18/20 · msg 1 sent Mon · no reply yet · v3 LIVE https://oracare-concept.vercel.app/",
  "REPLY-WATCH all day (1h rule). Silent → FU1 Wed 16 (pack §7). If he replies: branch sheet pack §1; send live v3 link.", "☐", "daily")
r("SJC Sasse (Buea) — KILL LIST #2 · BOARD-BUYER (Catholic diocesan, King 15 Sep)",
  "16/20 · active TikTok admissions · concept LIVE https://sjc-sasse-concept.vercel.app/",
  "07:45 TikTok DM treated as inbound seed only; no FU chase — bishop/diocesan education office decides. Network-level future play post founder-clients.", "☐", "Tue")
r("Baptist Comp. College Great Soppo — SENT, NOW LOW-PRIORITY",
  "12/B+ · GCE 11708 · no site · SURE WA 679 65 07 07 (King-confirmed, school FB-page line)",
  "MSG 1 SENT ~12:00 Tue (one tick). RECLASSIFIED BOARD-BUYER 15 Sep (King: Baptist mission, principal cannot sign). Inbound only: NO FU chase, NO cold walk-in; if they reply, equip contact to forward to Baptist education office/board.", "☑", "Tue")
r("PCSS Buea — PARKED BEFORE SEND (BOARD-BUYER)",
  "12/B+ · 700 boarders, founded 1993 · no site (deliberate network pattern: no PCC secondary in CM has one) · WA 652 075 229 = business acct, Namondo Elangwe (likely principal, cannot sign)",
  "DO NOT SEND msg 1; Kinang door-opener CANCELLED (no staff end-runs). Future play only: one network-level proposal to PCC Christian Education Secretary AFTER the 30 Sep founder push. Error log RESEARCH-STANDARD #2.", "☑", "Tue")
r("St. Theresa STIBCCOL Molyko — SENT, AWAITING DELIVERY",
  "14/A · ~128 GCE candidates, fees 181-237k · active TikTok @stibccol (to 14 Sep) · personal WA 679 15 10 75 (lay private = likely proprietor)",
  "MSG 1 SENT BY KING ~15:45 Tue (one grey tick so far, no image — mockup rule came after). No chase. If WhatsApp stays silent into Wed, TikTok DM @stibccol = second touch (replan §4). On reply: sample-secondary link + Thu/Fri walkthrough choice.", "☑", "Wed")
r("Baird Memorial Bonduma — GO GRANTED, pack in King's hand",
  "bairdmemorial.com DNS-DEAD re-verified 15 Sep 13:35 (Google indexes the dead pages; never say 'finds nothing') · WA 677 87 53 95 = PERSONAL line, man's photo; their own old site names PROPRIETRESS Madam Mary Forju (never name her, never reference the photo) · 677 78 04 05 discarded",
  "SEND: attach demos/shots/mockup-secondary-wa.jpg FIRST, then replan §4 final text (recipient-neutral: 'proprietor or the principal?'). Pre-tap: open bairdmemorial.com once; swap paragraph 3 only if it loads. Silent → sealed card in Wed Limbe sweep. Check box only once King confirms sent.", "☐", "Tue")
r("NHICHS (Limbe)",
  "11/20 · branded domain expired, technical dept launching · emails rarely opened (King)",
  "TONIGHT optionally WA-check 680 738 111 / 679 246 223. Only if neither lands: midday director email mehdi@nhiss.org (fallback, not counted). Build concept within 24h of any yes.", "☐", "Tue")
r("Summerset (SMBICOL) Wokoko — FLAGSHIP",
  "15/A · ~1,000 students, Principal Tata, publicly slower 2026 enrollment · NO phone online, FB dead since 2015",
  "NO Tuesday email (removed per King). Counted first touch = WED sealed-envelope card drop attn Principal Tata; email reply would be a bonus only.", "☐", "Wed")
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
r("Tue clinics: MITOC SENT 08:35 (two ticks, awaiting; FU1 Thu 17). Solidarity: front line not on WA → check admin 677 61 12 07 (profile must answer as the clinic; attach demos/shots/mockup-clinic-wa.jpg) else Wed sealed card", "MITOC out; Solidarity routing open",
  "Yes → /sample-clinic.html link ONLY after the amk-site.zip redeploy clears its 404 (until then describe the image; MITOC uses mitoc-concept.vercel.app) + clinic invite-choice ('10 minutes with the doctor Thu/Fri morning, or all here on WhatsApp?'); named concept within 24h; answers within 1h.", "Tue", "☐")
r("Tue schools: Baptist SENT→inbound only (BOARD); PCSS PARKED (BOARD); St Theresa SENT 15:45 by King (1 tick); Baird GO — image-first pack ready for King's tap", "St Theresa out; Baird in King's hand",
  "Yes → nameless /sample-secondary.html (LIVE, verified) with bilingual-toggle caption + invite-choice Thu/Fri; for St Theresa (replied after a text-only msg 1) attach mockup-secondary-wa.jpg alongside the link; Baird already has the image, link is next. Named concept within 24h for warm specific requests; answers within 1h.", "Tue", "☐")
r("SJC Sasse", "TikTok DM 07:45 Tue", "Watch TikTok inbox; invite visit only.", "Tue", "☐")
r("Wed card-drop inbound scans", "Cards dropped Wed AM",
  "QR inbound = they initiate → reply within 1h, preview link, then invite-choice.", "Wed", "☐")
r("GBP verification", "UNDER REVIEW", "Keep 677 789 631 reachable; check weekly.", "Wed", "☐")
r("", "", "", "", "☐")
r("", "", "", "", "")
r("③ WED 16 — ASYNC CARD-DROP SWEEP (~1h, NO meetings; invitations only after)", "", "", "", "")
r("· Numberless gates, one boda loop: St Bernard (Garden Park, opp Orange, attn Dr Fomba — VERIFY lay founder vs diocesan at gate before pitching) → Salvation (near CUIB — VERIFY possibly faith-founded governance) → Summerset (Check Point Wokoko opp ENAMEN Pharmacy, attn Principal Tata; LAY, keep) → NABESK (Nabesk junction; LAY, keep) → Baird (Bonduma road; card only because WA stayed silent; LAY). SKIP missionary/diocesan gates: St Sylvester, Bishop Jules (BOARD-BUYER, King 15 Sep).", "", "", "", "")
r("· Sealed envelope 'For: the Principal', handwritten bilingual line on card back (replan §3); capture gate-staff name + any mobile; never wait for the principal.", "", "", "", "")
r("· St Sylvester Muea only if already in Muea; Bishop Jules Bokwaongo folds into an invited Great Soppo trip (do not cold-drop a diocesan college).", "", "", "", "")
r("· Wed PM / Thu / Fri: invited 10-min walkthroughs batched by quarter (Molyko clinics/schools one trip, Wokoko one trip, Great Soppo/Bokwaongo one trip); confirm the decision-maker is present before leaving home.", "", "", "", "")
r("· If silent after Wed sweep: FU follows M+2/M+4/M+7; no second uninvited visit. No email legs counted anywhere (King: rarely opened).", "", "", "", "")
r("", "", "", "", "")
r("④ TONIGHT PREP (Mon, 20 min)", "", "", "", "")
r("· WA-verify: DONE Solidarity 677 61 57 57 NOT on WA (admin 677 61 12 07 still to check, else Wed sealed card); DONE MITOC 678 90 89 62 = ORG Business account MITOC with catalogue, hours 09:00-18:00, bio adds lens accessories + computer/swimming glasses. Named preview LIVE: https://mitoc-concept.vercel.app (send after warm yes). 691 63 29 41 stays Dr Njang personal - hold.", "", "", "", "")
r("· Research accuracy: every prospect dossier now follows sales/RESEARCH-STANDARD.md (source tiers, named-person obituary/collision/current-role checks, number attribution labels, message claim audit). No name from a directory enters a message unverified.", "", "", "", "")
r("· Schools status EOD 15 Sep: St Theresa 679 15 10 75 SENT by King ~15:45 (1 tick; Wed TikTok @stibccol fallback if silent). Baird 677 87 53 95 GO ('proceed') — send image mockup-secondary-wa.jpg + §4 neutral text when King taps; personal line, never name proprietress/photo; pre-tap site check. Baptist 679 65 07 07 SENT, inbound only (BOARD). PCSS 652 075 229 PARKED (BOARD; Kinang cancelled). RULE: missionary/confessional secondaries = BOARD-BUYER like government; principals can't sign; no counted slots, no chases.", "", "", "", "")
r("· REDEPLOY — KING'S ACTION (sandbox Vercel CLI is logged out): upload amk-site.zip contents (repo root, 14 web files; smoke-tested all 200, every internal link resolves) to the EXISTING amk-cm.vercel.app project, NOT a new one. Live audit 15 Sep 13:30: /sample-secondary.html already new build; / stale clinic card + old thumbnail (fixed in bundle); /sample-clinic.html and /mitoc.html 404 (in bundle). Verify after: open /sample-clinic.html ('Healthcare that answers, day or night'), homepage clinic card opens it. No clinic nameless link shared until 404 clears; MITOC named link is the separate mitoc-concept.vercel.app.", "", "", "", "")
r("· MOCKUPS (King standing rule 15 Sep): every msg 1 carries the matching house-style phone+laptop image from demos/shots/ — send the *-wa.jpg copies (1600x900, ~170 KB): mockup-secondary-wa.jpg for colleges, mockup-clinic-wa.jpg for clinics; mockup-mitoc-wa.jpg is NAMED/private. Regenerate any concept via tools/shots/ (see its README).", "", "", "", "")
r("· MITOC named concept READY: site/mitoc.html (Cobalt+Cream sheet C, EN|FR 140 pairs, 9 concept photos, WA booking demo-routed to AMK, ref MIT-XXXX). After warm yes: send link, then offer 10-min shop visit vs all-on-WhatsApp.", "", "", "", "")
r("· Print TWO A4 sheets of bilingual cards sales/walkin/walk-in-cards.html = 16 cards; prepare 6 envelopes (Baird now included if silent).", "", "", "", "")
r("· Read Clinic-Batch-2026-09-15 (Solidarity, MITOC) + Walk-In-Deep-Dives sections for Baptist, PCSS, St Theresa, Baird before sends.", "", "", "", "")
r("", "", "", "", "")
r("⑤ DRILL — 15 min/day (voice memo/friend — never on real leads)", "", "", "", "")
r("Day", "Segment", "", "", "")
r("Tue", "30-SECOND TEXT OPEN: read the clinic msg 1 aloud (MITOC - Solidarity line not on WhatsApp), then a school one; rehearse BOTH invite choices: '10 minutes with the doctor Thu/Fri morning?' and 'after morning classes Thu/Fri?'", "", "", "")
r("Wed", "FLIPS: 'It's expensive' → one missed registration/appointment worth per week? · 'I need to think' → timing or priority?", "", "", "")
r("Thu", "CARDONE + REFERRAL: 'Have you heard enough to decide?' · 'Who do you know that's like you?' (use on invited walkthroughs)", "", "", "")
r("Fri", "Friend plays skeptical principal/doctor — full invited-visit run; rehearse price+pause.", "", "", "")
r("Mon", "PRICE + PAUSE: '…100 000 francs, la moitié pour commencer.' 10 seconds silence.", "", "", "")
r("Sun", "OFF (30 min: pipeline review, schedule FUs, prep top 3 + write Weekly-Report-2026-09-20.md)", "", "", "")
r("", "", "", "", "")
r("⑥ TONIGHT — 5 min", "", "", "", "")
r("· Log every send/reply/scan/invitation in Leads 50 / Daily Tracker same day.", "", "", "", "")
r("· Any 'yes send it' → sample link immediately (schools /sample-secondary.html LIVE; clinics /sample-clinic.html ONLY after King redeploys amk-site.zip — until then send mockup-clinic-wa.jpg + 'the live link is minutes away'); MITOC yes → mitoc-concept.vercel.app. Named concept request → AMK builds within 24h; move to kill list + book time.", "", "", "", "")
r("· Open blockers (MoMo details) chase in weekly plan, not at close time.", "", "", "", "")

out = pathlib.Path("leads/Daily Ops.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerows(rows)
print("wrote", out, len(rows), "rows")
