# -*- coding: utf-8 -*-
"""Regenerate leads/Daily Ops.csv — Wed 16 Sep (remote-only day; site redeploy
+ Douala clinic sends + evening FR video)."""
import csv, pathlib

rows = []
def r(*cols): rows.append(list(cols))

r("AMK — DAILY OPS  ·  open this tab every morning (10 min)  ·  1-hour reply rule: 09:00–21:00, 7 days", "", "", "", "")
r("", "", "", "", "")
r("WED 16 SEP — REMOTE-ONLY, CLINICS FIRST (no travel/cards/boda — overrides Tue plan §③). Paste-ready texts: sales/Outreach-Pack-2026-09-16.md. Morning: site audit fixes shipped (commit 11dca5e) — King phone-QA + redeploy while TikTok traffic is live; then OraCare FU1 + 4 Douala clinic msg1s (FR, image-first); evening clinic FR video 18:00–20:00. STANDING: msg1 image = demos/shots/mockup-clinic-wa.jpg; ≤5 lines; one ask; ~15 min between new contacts; sign — Akwo King / AMK.", "", "", "", "")
r("", "", "", "", "")
r("① KILL LIST — hot leads get daily visible attention", "", "", "", "")
r("Lead", "Why hot", "Next action (TODAY)", "Done?", "Re-check")
r("⭐ OPPs ON THE SITE UPGRADE — finish redeploy",
  "TikTok post #1 live since 11:45; old live site shows the clipped EN/FR pill; fixes in commit 11dca5e (sticky WA bar, 3-field form, share card)",
  "1) Finish vercel --prod from site/ (or zip drag). 2) Phone smoke 60 s: both EN+FR visible at 360px and FR switches fully · sticky bar opens prefilled WA · form = 3 fields · /clinic-bonaberi.html FR pill + sticky bar · paste link in own WA to see share card. 3) Set TikTok bio = https://amk-cm.vercel.app/?src=tiktok. Details site/DEPLOY.md.", "☐", "now–14:00")
r("⭐ OraCare237 (Buea, dental) — CLINIC PILOT, AWAITING REPLY",
  "18/20 · msg1 Mon, v3 live https://oracare-concept.vercel.app/ · silent 2 days",
  "FU1 TODAY (M+2), text in pack §1 — EN, no image, ~14:00. Replies -> pack 14 Sep §1 branches (file/video/price). Silent -> FU2 Fri 18, FU3 Mon 21 then stop.", "☐", "1h watch all day")
r("⭐ Douala batch 2a · Cabinet Dentaire The Skye (Bonamoussadi)",
  "FB 19 avis / 100% recommandent · no website · 677 79 69 99 (sec. 672 67 65 70)",
  "Verify WA profile = the clinic, then FR msg1 + mockup-clinic-wa.jpg (pack §2a). First of the 4, ~14:30.", "☐", "FU ven 18")
r("⭐ Douala batch 2b · Cabinet dentaire YAKS (Logbessou, immeuble BAO)",
  "2 100+ FB likes, active page, Gmail only · 672 70 20 78",
  "Verify WA profile, then FR msg1 (pack §2b) ≥15 min after 2a.", "☐", "FU ven 18")
r("⭐ Douala batch 2c · AFRIQUE LABO SARL (Bessengue, Tour SGBC)",
  "5 500+ FB likes, multidisciplinaire, pas de site; afriqlabo.com vérifié NON relié à eux · 690 54 70 93 (sec. 699 73 36 25)",
  "Verify WA profile = the lab, then FR msg1 (pack §2c).", "☐", "FU ven 18")
r("Douala batch 2d · JOSS MEDI Clinic (Bonanjo, rue Ivy)",
  "Private since 2009, highest DoualaTour WA activity, no own site · 677 58 42 73 (sec. 674 63 88 88)",
  "GATE: open jossmediclinic.com on phone FIRST — real site = SKIP & tell AMK; dead/parked = send FR msg1 (pack §2d).", "☐", "FU ven 18")
r("TikTok / IG inbound — post #1 live",
  "Bio traffic landing now; ?src=tiktok tags the WA prefill",
  "1h rule all day. First DM = ONLY 'Thank you! Are you a clinic/lab or a school — and which town?' (FR too, pack §4). Log source=TikTok. Comments -> DM only, no price in public.", "☐", "all day")
r("MITOC (Molyko optical) — AWAITING REPLY",
  "Sent Tue 08:35, two ticks, ORG WA Business, owner hours 09–18; named concept ready",
  "No action today (FU1 Thu 17 M+2). AMK to prep Thursday text; warm yes -> mitoc-concept.vercel.app then 10-min visit vs async choice.", "☐", "Thu")
r("Baird Memorial (Bonduma school) — SENT Tue 14:41",
  "Personal WA line 677 87 53 95; bairdmemorial.com DNS-dead",
  "Check delivery ticks/replies only. Silent -> FU1 Thu 17 (M+2), image-first. Never name proprietress/profile photo.", "☐", "Thu")
r("St Theresa STIBCCOL — parked warm WITH permission",
  "Replied twice; follow-up invited; site in the making 'for October'",
  "NOTHING today. FU1 Wed 14 Oct (is site live? free honest review). No chase. Verbatims in CRM row 28.", "☐", "14 Oct")
r("Holds & parks — no sends",
  "",
  "Solidarity 677 61 57 57 never retry · Dr Njang 691 63 29 41 forever HOLD · admin 677 61 12 07 optional profile look only · COMOBIL/SAHISCOL/Retraite parked (review Fri) · Baptist/PCSS/Sasse board-buyers inbound-only; one HQ proposal after 30 Sep.", "☐", "Fri review")
r("", "", "", "", "")
r("② REPLY QUEUE — 1-hour rule · every chat ends with a booked next step (BAMFAM)", "", "", "", "")
r("Lead", "Last activity", "Next step", "Due", "Done?")
r("OraCare", "Mon msg1, silent", "FU1 text pack §1", "Wed", "☐")
r("Douala ×4", "msg1 today", "'oui' -> demo link + 3-line caption pack §3, then qualifying question; silence -> FU ven 18 / dim 20 / mer 23 then stop", "rolling", "☐")
r("TikTok DMs", "post #1", "Niche + town question only; move to WA for preview; CRM source tag", "1h", "☐")
r("Baird", "SENT Tue 14:41", "Ticks check only today", "Wed", "☐")
r("MITOC", "SENT Tue 08:35, two ticks", "FU1", "Thu", "☐")
r("GBP verification", "UNDER REVIEW", "Keep 677 789 631 reachable; check weekly", "Wed", "☐")
r("", "", "", "", "")
r("③ WED 16 — TIME BLOCKS (all remote, WhatsApp + browser only)", "", "", "", "")
r("· 13:35–14:00 Lock the redeploy: finish vercel --prod, run the 60-second phone smoke list (kill-list row 1), update TikTok bio with ?src=tiktok. Live traffic is hitting the OLD build right now — this outranks prospecting.", "", "", "", "")
r("· 14:00–14:15 Send OraCare FU1 (pack §1), then save+verify the 4 Douala contacts' WhatsApp profiles (photo/name must match the business; skip mismatches).", "", "", "", "")
r("· 14:30–16:00 Four FR msg1 sends, image FIRST (mockup-clinic-wa.jpg), ~15 min apart: Skye -> YAKS -> Afrique Labo -> JOSS (gate first). Never identical wording. Log each in Leads 50 immediately.", "", "", "", "")
r("· 16:00–18:00 Reply-watch window; any 'oui' -> demo link within minutes (pack §3); TikTok/IG DMs same. If zero replies, keep phone audible, don't double-send.", "", "", "", "")
r("· 18:00–20:00 Post clinic-founding-FR.mp4 on TikTok (FR caption in founding-post-tiktok-ig.md §A); mirrors: FB Page, WA Status (3 slides), YouTube Shorts with sales/social/youtube-shorts-metadata.md §2. Optionally mirror the EN video to YT/FB now (metadata §1).", "", "", "", "")
r("· CANCELLED: the Wed async card-drop sweep (St Bernard / Salvation / Summerset / NABESK / Baird envelopes) — remote-only standing law replaces it; those gates are not visited. Summerset/NABESK remain unsent remote candidates (no number yet = AMK research task).", "", "", "", "")
r("", "", "", "", "")
r("④ TONIGHT PREP (20 min, after the video posts)", "", "", "", "")
r("· AMK side queued: (a) NAMED-less generic optical concept so L'Opticien Bali (670 27 60 65) + Maison Optique (657 73 70 45) can get mockup-mitoc-style msg1 without leaking MITOC's named preview — target Thu before sends; (b) MITOC FU1 + Baird FU1 texts for Thursday morning; (c) research numbers for La Béthanie (Bonabéri, maternity) + J&E Memorial / Polyclinique de la Gare / CAMERA / Wonders / Clinique des Anges from DoualaTour/Google for Thu–Fri queue.", "", "", "", "")
r("· MOCKUPS rule: mockup-clinic-wa.jpg for every clinic/dental/lab msg1; mockup-secondary-wa.jpg colleges; mockup-mitoc-wa.jpg is NAMED/private — never attached to anyone but MITOC.", "", "", "", "")
r("· Any 'yes build it' named-gift request -> AMK builds within 24h (generator adapt, throwaway Vercel URL, private), per Remote-Sweep-1 §E.", "", "", "", "")
r("", "", "", "", "")
r("⑤ DRILL — 15 min (voice memo/friend — never on real leads)", "", "", "", "")
r("Wed (today)", "FLIPS: 'C'est cher' -> un rendez-vous/une inscription manquée par semaine, ça vaut combien ? · 'Je dois réfléchir' -> question de timing ou de priorité ? Practice in FR — Douala batch is francophone.", "", "", "")
r("Thu", "CARDONE + REFERRAL: 'Have you heard enough to decide?' · 'Who do you know that's like you?'", "", "", "")
r("Fri", "Friend plays skeptical doctor — full async-to-call run; rehearse price+pause in FR.", "", "", "")
r("Sun", "OFF (30 min: pipeline review, Weekly-Report-2026-09-20.md, schedule next week).", "", "", "")
r("", "", "", "", "")
r("⑥ TONIGHT — 5 min", "", "", "", "")
r("· Log every send/reply in Leads 50 / Daily Tracker same day (include WA profile verification result and JOSS domain gate result).", "", "", "", "")
r("· Any 'yes send it' -> https://amk-cm.vercel.app/clinic-bonaberi.html for clinics/dental/labs (post-redeploy carries the upgraded build; placeholder names shown on purpose), image attached first; schools -> /sample-secondary.html; MITOC yes -> mitoc-concept.vercel.app.", "", "", "", "")
r("· Open blockers (MoMo details) chase in weekly plan, not at close time. OraCare FU2 lands Fri 18 if silent.", "", "", "", "")

out = pathlib.Path("leads/Daily Ops.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerows(rows)
print("wrote", out, len(rows), "rows")
