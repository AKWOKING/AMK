# AMK — CONTENT PIPELINE

**Updated:** 17 Sep 2026 (v0.2 — previous-chat pack received and ingested)
**Stages:** `scripted → rendered → delivered → approved → posted → measured`
**Rule:** update after every movement. Nothing is marked posted/measured without King's explicit confirmation. King's reported figures are recorded verbatim with their caveats.

---

## A · The content series (previous chat) — authoritative files now in `content/videos/`

| Video | Concept | Master file (location) | Duration (verified) | Stage | Posted? | Measured (King-reported) |
|---|---|---|---|---|---|---|
| **#1** | Instagram is not a substitute for a website | `Instagram_vs_Website_v2.mp4` — **⚠ NOT in repo, re-upload needed** | 40.08 s (handover) | delivered → **accepted by King for posting** | **yes** (IG) | IG **13** · TikTok **not supplied** (post status unconfirmed) |
| **#2** | 5 things your website should tell a customer in 10 seconds | `content/videos/v02-five-website-answers/Video_02_Five_Website_Answers.mp4` | **29.40 s** ✓ | delivered → posted | **yes** | IG **47** · TikTok **87** |
| **#3** | 3 reasons people leave without contacting you (= **series Part 2**) | `content/videos/v03-part2-three-reasons/Video_03_Part_2.mp4` | **34.90 s** ✓ | delivered → posted | **yes** | IG **41** · TikTok **137** |
| **#4** original | Losing customers before they reach WhatsApp | `Video_04_Before_WhatsApp.mp4` — **⚠ not in repo** (superseded) | 30.9 s (handover) | obsolete for posting | no | — |
| **#4** latest | Same script, real website footage + **PREVIEW CTA** | `content/videos/v04-before-whatsapp/Video_04_Real_Website_PREVIEW.mp4` | **34.20 s** ✓ | **delivered → PENDING: not approved, not posted** | **no** | — |

**QA performed this session (17 Sep), reported as checked:** all three files in the repo were decoded with FFmpeg (`imageio_ffmpeg` binary `ffmpeg-linux-x86_64-v7.0.2`) → 1080×1920, SAR 1:1, DAR 9:16, H.264 High, 30 fps, + AAC 48 kHz mono. Frames extracted and **visually inspected**: #4 at 1 s (hook + real site, labelled "FICTIONAL CLINIC"), 10 s (bad-site demo labelled "Deliberately flawed", desktop-layout-on-phone leak), 22 s (MAKE CONTACT EASY payoff), 33 s (DM "PREVIEW" end card) — all correct; #3 at 18 s ("They don't trust you yet", X-list panel); #2 not frame-inspected yet (QA pending, file verified by decode only).

**Performance arithmetic (from King's figures):** #2 IG +262 % vs #1 IG · #3 IG +215 % vs #1 IG · #3 TikTok +57 % vs #2 TikTok. **#2 leads Instagram; #3 leads TikTok** — recorded separately, no cross-platform winner declared.
**Missing for a real read:** observation windows, unique reach, paid/organic split, profile visits, website clicks, PREVIEW DMs, qualified inquiries. Suggested checkpoints: 24 h / 72 h / 7 d per platform.

## B · Production source & assets (from the pack, now in `content/`)

| Asset | Path | Verified | Notes |
|---|---|---|---|
| MboaCare studio | `content/studio/Website_Demo_Studio.html` | 546 KB, title "AMK · Website demonstration studio" ✓ | self-contained (embedded pages + photo) |
| Bad example | `content/studio/before.html` | 268 KB, title "MboaCare \| Before demo" ✓ | deliberately flawed, labelled |
| Good example | `content/studio/after.html` | 270 KB, title "MboaCare \| After demo" ✓ | responsive, WhatsApp-first |
| Reception photo | `content/studio/clinic-reception.jpg` | 196 KB ✓ | AI-generated, fictional clinic |
| Studio build/test | `content/studio/create.py`, `test.py` | ✓ | Playwright test script |
| Host art | `content/assets/host/s1_hook.png` | 1.2 MB ✓ | established cartoon host + phone |
| Fonts | `content/assets/fonts/` (Montserrat ×5 incl. VF, Poppins-SemiBold) | ✓ PIL loads; **variable axis works** (`set_variation_by_axes([800])` / `[500]` needed — default renders Thin) | glyph gaps noted (draw marks manually) |
| #4 recut source | `content/videos/v04-before-whatsapp/source/` — `capture.py`, `render.py`, `timeline.json`, `cta.mp3` (2.98 s), `narration.mp3` (30.43 s) | ✓ | timeline: starts [0, 4.78, 9.78, 16.02, 21.30, 26.50, 30.50], 30 fps, 34.2 s |

**Re-render caveats (do not re-run blindly):** `render.py` hardcodes `/home/user/video4_asset` and reads `ffpath.txt` (not shipped) → **must be re-pointed to `content/…` and `imageio_ffmpeg.get_ffmpeg_exe()`** before any re-render. It composes at 720×1280 and upscales to 1080×1920 (`scale=1080:1920,setsar=1,fps=30`) — browser captures are sampled at **15 fps**, composed at 30 fps; never claim native 30 fps captures. **Playwright is not installed in this sandbox** (`pip install playwright` + `playwright install chromium` + `install-deps chromium` required before captures).

## C · Repo-era content assets (15–16 Sep, earlier effort — separate from the series)

| Asset | Path | Spec (verified) | Status |
|---|---|---|---|
| TikTok v1 final / silent | `tiktok/video1-final.mp4` / `video1-silent.mp4` | 21.66 s / 22.96 s · 1080×1920 · **25 fps** | prepared — posted? unconfirmed |
| Founding series | `sales/social/videos/{clinic,school}-founding-{en,fr}.mp4` (+ covers) | 29.20 s · 1080×1920 · 30 fps · silent | prepared — posted? unconfirmed |
| Clip library, voice tests, metadata packs | `tiktok/clips/*`, `tiktok/vo-*.mp3`, `sales/social/*.md` | — | assets |

## D · Next productions (shortlist — awaiting King's approval)

8 candidates with rationale: `content/pipeline/CONTENT-SHORTLIST.md`.
**Blocking prerequisites:** (1) rights/consent decisions on concepts, (2) voice selection (previous `voice-00` registration is not available in a new chat — re-audition required), (3) Playwright install for captures.

## E · Changelog
- **v0.2 — 17 Sep 2026:** pack received; files migrated into `content/`; real specs + frame QA recorded; performance figures recorded with caveats; Video 4 = pending/not approved/not posted.
- **v0.1 — 17 Sep 2026:** structure created while uploads were missing.
