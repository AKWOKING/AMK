# AMK — CONTENT LESSONS (living playbook)

**Version:** v0.1 · **Created:** 17 Sep 2026 · **Sources absorbed:** King's 17 Sep content brief (authoritative), repo content history (15–16 Sep founding series + TikTok v1), `research/YouTube-Lessons.md` batches 1–3 (relevant slices).
**⛔ PENDING:** the previous content chat's lessons file was not received — merge when re-uploaded; log conflicts, never overwrite.

**Rule:** append a dated entry whenever a video teaches something (hook that worked, frame that landed, mistake to avoid). Version the file; never silently rewrite.

---

## 1 · Brand fingerprint (what "in the image of AMK" means — every video)

- Same **cartoon host**, same **selected voice**, same **navy/teal/amber** palette, same **Montserrat/Poppins** typography, same **educational tone**.
- Vertical **9:16, 1080×1920, 30fps, SAR 1:1, H.264** — verify the output, don't assert it.
- **The host introduces the subject and steps back.** Real website footage does the teaching. **No talking-head-only videos. No avatar reciting a script over generic art.**
- Every important conclusion and every CTA gets its **own clean, high-contrast, mobile-readable frame**. No overlays on the thing being demonstrated — **especially never a WhatsApp button**.
- One message per beat. One question per screen when narration presents a list.

## 2 · Content quality

- **Show real websites** — MboaCare, a shipped site, or a concept preview. The visual is always a real webpage, never rectangles.
- Make the bad example **believable, not a parody**. Label fiction as fiction; label real work as real work.
- **Hooks are questions or specifics, never hype.**
- Payoff frames are clean and memorable: **HARD TO FIND → EASY TO LEAVE · CURIOUS → CONFIDENT · MAKE CONTACT EASY.**
- **Never invent** testimonials, rankings, "verified" conversion stats, or client outcomes. "10 seconds" is a hook, not a threshold.
- **Never claim** a video was posted, a profile was edited, or tracking was installed unless King explicitly said so.

## 3 · Funnel tie-in

- Every video ends with the **DM "PREVIEW" CTA as a separate closing beat**, after the educational payoff. **Video 4 already does this. Earlier videos do not — retrofit only if King asks.**
- Funnel: Views → Profile visits → Website clicks → **PREVIEW DMs** → qualified inquiries → projects.
- **Instagram and TikTok are tracked separately.** Never average them; never declare a cross-platform winner — different videos lead on different platforms.
- Report at **24h / 72h / 7 days**, per platform, with the numbers King actually gave. Never assume, never round up.

## 4 · Sources (a decision, never a default)

Allowed sources, with the reason stated per video:
1. **MboaCare studio** (`content/studio/`) — right when the video teaches a problem in the abstract.
2. **Our own shipped work** — anonymised where the client relationship requires it, credited where it doesn't.
3. **Our concept/preview library** — real prospects, real problems, real fixes we proposed. Much of the best raw material lives here.
4. **Before/after from actual prospects** — only where permission exists or anonymisation is clean.
5. **Build footage** (scroll, tap, load, contact flow) from anything we've shipped.
6. **Client stories/results** — only when verified **and** the client agreed.
7. **The niche itself** — schools and clinics in Cameroon: what their customers struggle with, what they get wrong, what good looks like.

## 5 · Production discipline

- **Unique filename per stage. Never edit in place. Preserve every prior deliverable.**
- **FFmpeg via `imageio_ffmpeg.get_ffmpeg_exe()`** — never a hard-coded path. *(Repo environment: installed 17 Sep; resolved path logged in the pipeline file.)*
- **Small sequential compositing passes** over one giant graph — the sandbox chokes on 7 full-res inputs.
- **Sample browser captures at 15fps, compose at 30fps.** Say so in any technical note.
- **QA every final file:** decode it, check resolution, frame rate, SAR/DAR, duration — report what was actually checked.
- Inspect frames whenever possible. Never claim you can't see.

## 6 · Varied formats, not one repeated video

The variety is the point — sameness kills reach. Rotate across: build timelapse (craft/perception) · concept preview reveal · "how we think about X" authority · answer to a real prospect question · single-frame payoff + CTA. Videos must serve the whole funnel, not cluster at "here's what's wrong with your website".

## 7 · Absorbed from the repo's own content history (15–16 Sep 2026)

- **Silent + captions is deliberate** on the founding series (in-app trending sound added by King post-upload) — keep the master silent, let the platform add music.
- **Mirror every TikTok to YouTube Shorts** with a search-first title (niche + city + "website"); Google AI Overviews cite YouTube. Bio/channel link carries `?src=` attribution.
- **DM keywords per vertical** ("CLINIC" / "SCHOOL" / now "PREVIEW") route the conversation into WhatsApp; replies follow the 09:00–21:00 window.
- **No fake scarcity** — the two founding slots were real; state capacity only when it's true.
- **⚠ Discrepancy to reconcile:** `tiktok/video1-final.mp4` is **25fps** (and carries an audio track); the founding series is **30fps silent**. The fingerprint says 30fps → future masters use 30fps; v1 stays as-is unless re-rendered.
- Never name a real client without consent (standing rule, reinforced by 17 Sep brief).

## 8 · Absorbed from the lesson batches (`research/YouTube-Lessons.md`)

- **Copy law [5]:** visualize / falsify / nobody-else-can-say-it — applies to hooks and on-screen text; 2-second test on frame 1; read aloud; no padded lines.
- **Claim → proof [6]:** every claim in a video carries its artifact on screen (the dead domain, the price, the real page).
- **One quote at a time [6]:** no walls of testimonials — one real verbatim client/patient sentence under the claim it proves.
- **Anti-slop design [10]:** no scroll-jacking, no content-hiding animations, no moving buttons, no emoji icons — applies to any UI shown on camera.
- **Conversion-first [12]:** show hierarchy (biggest = most important), solid high-contrast CTAs, never ghost buttons as the primary action.
- **Direction exploration [13]:** three directions before visual work; explicit avoid-list (purple gradients, AI sparkles, generic 3D).
- **Taste is the moat [14]:** when every feed looks the same, the decisions differentiate.

## 9 · Changelog
- **v0.1 — 17 Sep 2026:** created from King's content brief + repo history + lesson batches 1–3. Previous-chat lessons pending ingestion.
