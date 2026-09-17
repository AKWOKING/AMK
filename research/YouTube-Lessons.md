# AMK — YouTube Lessons Log (ingestion register)

**Created:** 17 Sep 2026 · **Protocol owner:** King · **Operator:** AMK

This is the catch-all register for every YouTube link King drops in chat. Links whose lesson belongs in an existing playbook/ops file are folded **there**, not here — but **everything is logged here**, one entry per video, dated, with the verdict (absorbed / alternative / rejected / conflict). Any future chat can see what has been absorbed and what was thrown away, and why.

---

## 0 · How to ingest (method that works in this sandbox)

- The sandbox has **no raw network** (direct `curl`/`getent` fail). Transcripts come through the `fetch_page` tool only.
- **Working path:** `https://youtubetotranscript.com/transcript?v=VIDEO_ID` → full transcript, title, channel (tested 17 Sep 2026).
- If that returns nothing: try `?v=ID&current_language_code=fr` for French captions. If still nothing (members-only, no captions, livestream), **stop and ask King to paste notes — never guess at content.**
- Extract, don't summarize: core claim(s) · AMK-applicable tactics (2–5) · contradictions vs playbook · junk filter · attribution.

## 1 · Where each field folds (keep files in scope)

| Field | Primary target | Versioning |
|---|---|---|
| Sales (prospecting, qualifying, closing, objections, FU, pricing) | `sales/AMK-Sales-Playbook-v2.md` | bump v2.x + changelog line |
| Outreach copy / social / positioning | `sales/Monday-Outreach-Pack.md` + the dated pack in use | date-stamped edit note |
| Design (visual standards, layout, type, color, anti-default) | `AMK-DESIGN-SKILLS.md` §1–§17 | dated entry in the section |
| Build (HTML/CSS/JS, mobile-first, EN\|FR, base64, perf, deploy) | `AMK-DESIGN-SKILLS.md` §build/deploy + `hosting/DEPLOY.md` | dated entry |
| Agency ops (delivery, onboarding, retention, upsell, referrals) | relevant ops/delivery doc (`sales/AMK-Playbook-Addendum-*`) | dated entry |
| Niche intel (schools, clinics, Cameroon/Africa, WhatsApp-first buyers) | `sales/Deep-Dive-Research.md` or the playbook addendum in scope | dated entry |
| Anything that fits nowhere | **this file**, as a dated entry | — |

Cross-link with the weekly techniques register `sales/research/2026-W37-techniques.md` when a video and a technique overlap.

## 2 · Standing bias (every lesson passes this lens or it does not enter)

WhatsApp-first · mobile-first · EN|FR · Cameroon (Kumba/Douala/South-West) · clinics & schools · close one client by 30 Sep · 500 000 FCFA/month by month 6. If a tactic doesn't serve that, it goes in §5 Rejected — named, not silently dropped.

## 3 · Ingestion log (one line per video)

| # | Date | Video / creator | Field | Verdict | Folded into |
|---|---|---|---|---|---|
| — | — | *(first drop pending)* | — | — | — |

## 4 · Entries (full reports)

*(One dated block per video, in the order ingested. Format: Video · Field · Core claims · AMK tactics · Contradictions · Junk filter · Attribution.)*

## 5 · Rejected (named, with reason)

*(Nothing rejected yet.)*

## 6 · Weekly ritual (Mondays, before the outreach pack goes out)

1. Re-read the last 7 days of entries in §3/§4.
2. Surface the **top 3 lessons that should change how we operate this week** — each one must name the file it changes and the concrete move it changes.
3. If a lesson contradicts the playbook: state the conflict and ask King which side wins (unless the video is clearly stronger evidence — then propose the change and wait for the yes).
4. Log the Monday summary at the top of §3 as a dated row so the ritual itself is auditable.
