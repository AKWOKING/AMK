# AMK — CONTENT ENGINE (CCO + SMM)

**Owner:** AMK (Chief Content Officer & Social Media Manager) · **King:** approval + posting
**Version:** v0.2 · 17 Sep 2026 · previous-chat pack **received and ingested**

Content is a **marketing function**: it attracts inbound leads. Success is the funnel — Views → Profile visits → Website clicks → **PREVIEW DMs** → qualified inquiries → projects — never views alone.

---

## Status of the previous-chat pack (resolved 17 Sep)

All files arrived via `AMK_New_Chat_Starter_Pack/` (git commit `91cae5e`) and were **migrated (git mv, history preserved, no bytes altered)** into the structure below. The now-empty pack folder is gone; provenance is in git history.

| Arrived | Went to |
|---|---|
| `AMK_New_Chat_Handover.md` | `content/handover/2026-09-17-content-handover.md` |
| `Video_02…mp4`, `Video_03_Part_2.mp4`, `Video_04_Real_Website_PREVIEW.mp4` | `content/videos/vNN-…/` |
| `website-demo/*` (studio, before/after, photo, create/test) | `content/studio/` |
| `video/assets/fonts/*`, `video/assets/img/s1_hook.png` | `content/assets/fonts/`, `content/assets/host/` |
| `video4/narration.mp3`, `video4_asset/{capture.py,render.py,timeline.json,cta.mp3}` | `content/videos/v04-before-whatsapp/source/` |

**Still missing (requested):** `Instagram_vs_Website_v2.mp4` (#1, 40.08 s) and `Video_04_Before_WhatsApp.mp4` (original #4, obsolete). Everything else needed to reproduce #4 is present.

---

## Structure

```
content/
├── handover/2026-09-17-content-handover.md   the previous chat's handover (authoritative record)
├── lessons/CONTENT-LESSONS.md                living playbook (v0.2)
├── strategy/CONTENT-STRATEGY.md              audiences · goals · tests · not-doing (v0.2)
├── strategy/POSTING-CALENDAR.md              what goes out when + profile layer (v0.2)
├── scripts/                                  v01–v04 with status headers (+ conventions in README)
├── assets/                                   fonts (Montserrat/Poppins) · host art · ASSETS.md index
├── studio/                                   MboaCare studio: before/after HTML, photo, create.py, test.py
├── videos/                                   v01–v04 folders, each with STATUS.md
└── pipeline/CONTENT-PIPELINE.md              real stages + QA + specs; CONTENT-SHORTLIST.md (V-05…V-12)
```

## Current state in one line each
- **#1, #2, #3 posted** (King-reported: IG 13/47/41 · TikTok —/87/137). **#4 delivered, pending approval, not posted.**
- **#2 leads IG, #3 leads TikTok** — tracked separately, no averaged winner.
- **Blocking prerequisites for the next production:** rights decisions on concepts, a re-selected voice (the previous `voice-00` registration is gone), Playwright install for captures.

## Weekly cadence
Mon: pipeline + calendar + plan vs the sales pack · Wed: mid-week check · Fri: `pipeline/Weekly-Content-Report-YYYY-MM-DD.md`.

## Standing filter
WhatsApp-first · mobile-first · EN|FR · Cameroon · clinics & schools · one client closed by 30 Sep · 500 000 FCFA/month by month 6. Ideas that don't serve this go to the **rejected list**, not the calendar.

**See also:** `PRE-FLIGHT.md` · `research/YouTube-Lessons.md` · `sales/Monday-Outreach-Pack.md` · `AMK-DESIGN-SKILLS.md` · `clients/_uniqueness-registry.md`.
