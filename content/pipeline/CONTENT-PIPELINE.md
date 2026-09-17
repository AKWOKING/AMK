# AMK — CONTENT PIPELINE

**Updated:** 17 Sep 2026 · **Stages:** `scripted → rendered → delivered → approved → posted → measured`
**Rule:** update after every movement. Nothing is marked posted or measured without King's explicit confirmation.

**Environment note:** FFmpeg resolved via `imageio_ffmpeg.get_ffmpeg_exe()` →
`/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2` (installed 17 Sep). Capture→compose rule: sample browser at 15fps, compose at 30fps.

---

## A · Videos from the previous content chat — **FILES NOT RECEIVED**

| Video | File | Stage | Posted? | Measured? | Notes |
|---|---|---|---|---|---|
| #1 | (unknown — not received) | **unknown** | **unconfirmed** | no | King to confirm what it is, where it went |
| #2 | (unknown — not received) | **unknown** | **unconfirmed** | no | — |
| #3 | (unknown — not received) | **unknown** | **unconfirmed** | no | — |
| **#4** | `Video_04_Real_Website_PREVIEW.mp4` | **rendered → delivered** | **NOT POSTED** | no | **Pending King's approval.** Not approved, not posted. First video carrying the PREVIEW closing beat. |

**Performance data #1–#3:** none available (no files, no numbers supplied). Nothing assumed, nothing rounded.
**Required to unblock:** re-upload of the 7 files (`Website_Demo_Studio.html`, `before.html`, `after.html`, `clinic-reception.jpg`, `s1_hook.png`, `timeline.json`, `AMK_New_Chat_Handover.md`) + the video files.

## B · Assets that ARE accessible (repo, 15–16 Sep) — verified this session

| Asset | Path | Spec (verified via ffmpeg) | Stage | Posted? |
|---|---|---|---|---|
| TikTok v1 final | `tiktok/video1-final.mp4` | 21.66s · 1080×1920 · SAR 1:1 · 25fps · H.264 + AAC | rendered | unconfirmed |
| TikTok v1 silent | `tiktok/video1-silent.mp4` | 22.96s · 1080×1920 · 25fps | rendered | unconfirmed |
| Crestwood scroll capture | `tiktok/crestwood-scroll-1080x1920.mp4` | 15.24s · 1080×1920 · 30fps-ish source | capture | — |
| Clinic founding EN/FR | `sales/social/videos/clinic-founding-en.mp4` / `-fr.mp4` | 29.20s · 1080×1920 · **30fps** · silent | rendered + covers (`-cover.jpg`) | unconfirmed |
| School founding EN/FR | `sales/social/videos/school-founding-en.mp4` / `-fr.mp4` | 29.20s · 1080×1920 · **30fps** · silent | rendered + covers | unconfirmed |
| Clip library | `tiktok/clips/*.mp4` (hook-a/b, crest, fb, nova, end) | short clips | assets | — |
| Voice tests | `tiktok/vo-test-en.mp3`, `tiktok/vo-video1-fr.mp3` | audio | assets | — |
| Metadata | `sales/social/youtube-shorts-metadata.md` · `sales/social/founding-post-tiktok-ig.md` | paste-ready titles/captions/hashtags | — | — |
| Frame stills | `tiktok/f1.png`, `f2.png`, `f3.png`, `frame-*.png` | QA frames | — | — |
| Brand assets | `brand/` (logo kit, mono/primary/square SVG+PNG, avatar) | — | assets | — |
| Concept library (source material) | `demos/concept-*.html` ×10 · `hosting/previews/*` | live concepts: yaks, skye, oracare, sasse | deliverables | — |

**Fingerprint discrepancies to reconcile:** v1 is 25fps (rule: 30fps) and carries audio (founding masters are silent by design). Decision needed: leave v1 as an archive piece, or re-render. Default: leave it; new masters are 30fps.

## C · Next productions (candidates — awaiting King's approval of the shortlist)

| Candidate | Format | Source | Funnel stage | Status |
|---|---|---|---|---|
| V-01 clinic "dead domain → live site" | before/after, 20–25s | real NXDOMAIN case (anonymised) + our concept | BOFU | proposed |
| V-02 school "what parents search before calling" | reveal, 20–25s | school concept (anonymised/new design) | TOFU/MOFU | proposed |
| V-03 build timelapse | craft, 15–20s | our build process + site scroll | perception/authority | proposed |
| V-04 authority "what a Cameroonian clinic site must have in 2026" | checklist, 25–30s | MboaCare + our concepts | MOFU | proposed |
| V-05 objection: "un site, c'est cher ?" | talking + proof frames | our offer + real numbers | BOFU | proposed |
| V-06 WhatsApp-first education | demo, 20s | our concepts' WA flows | MOFU | proposed |
| V-07 real prospect question | answer, 15–20s | actual DMs | authority | proposed |
| V-08 single-frame payoff + CTA | 8–10s | best-performing visual to date | BOFU | proposed |

*Full format with audience/pain/source/funnel/outcome + rationale: see the shortlist in `content/pipeline/` (to be written once King approves the direction).*

## D · Changelog
- **17 Sep 2026:** created. Section A pending re-upload; Section B verified with ffmpeg on real files; Section C awaiting approval. Video 4 recorded as **not approved / not posted**.
