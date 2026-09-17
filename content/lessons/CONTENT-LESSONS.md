# AMK — CONTENT LESSONS (living playbook)

**Version v0.2** · 17 Sep 2026 · sources: `content/handover/2026-09-17-content-handover.md` (previous chat, authoritative), King's 17 Sep brief, repo content history, `research/YouTube-Lessons.md` batches 1–3.
**Rule:** append dated entries; never silently rewrite. Conflicts get logged and go to King.

---

## 1 · Brand fingerprint (every video, no exceptions)
- Same **cartoon host**, same **selected voice**, same **navy `#1B2055` / teal `#23C4B1` / amber `#FFB020`** palette, same **Montserrat/Poppins** typography, same **educational tone**.
- Vertical **9:16, 1080×1920, 30 fps, SAR 1:1, H.264** — *verify by decoding the output, never assert.*
- **Host introduces → real website footage teaches.** Never a talking head; never an avatar reciting a script over generic art.
- **One message per beat · one question per screen** when narration lists items.
- Every conclusion and every CTA gets **its own clean, high-contrast, mobile-readable frame**.
- **No overlays on the thing being demonstrated** — a caption once covered the good site's WhatsApp buttons; it was fixed and **must not be reintroduced**.

## 2 · Content quality (hard rules)
- **Show real webpages**, never rectangles masquerading as sites (King's explicit criticism of earlier videos).
- **Bad examples: believable, not parody** — and **labelled**. MboaCare carries "FICTIONAL CLINIC · Deliberately flawed website demonstration" on every capture.
- **Label fiction as fiction, real as real.** Concept sites are **not** client case studies.
- **Hooks are questions or specifics, never hype.** "10 seconds" is a hook, **not** a measured threshold — never turn it into a statistic.
- Payoff frames stay clean: **HARD TO FIND → EASY TO LEAVE · CURIOUS → CONFIDENT · MAKE CONTACT EASY.**
- **Never invent** testimonials, rankings, conversion stats, client outcomes, or completion claims.
- **Never claim a post, a profile edit, or tracking installation happened unless King says so.** Bio/pinned/link advice is *recommendation only*.

## 3 · Funnel & measurement
- Funnel: **Views → Profile visits → Website clicks → PREVIEW DMs → qualified inquiries → projects.**
- Every video ends with the **DM "PREVIEW" closing beat, separate from the educational payoff**. Latest #4 has it; #1–#3 do **not** — **retrofit only if King asks** (and #1's file isn't in the repo).
- **Track IG and TikTok separately. Never average. Never declare a cross-platform winner.**
- Report **24 h / 72 h / 7 d, per platform, only with King's numbers** — never assume, never round up.
- **Views ≠ unique reach.** A bio tap ≠ a loaded session. A WhatsApp click ≠ an inquiry. **A UTM tag = attribution only if analytics actually collect it.**
- Suggested first reply to a PREVIEW DM: ask for **name of school/clinic, town, current website link**. No automation exists.

## 4 · Sources (a stated decision, never a default)
MboaCare (abstract principle) · our own shipped work · **our concept/preview library** (real prospects, real problems, real fixes) · before/after pairs with permission or clean anonymisation · build footage · verified client stories with consent · the niche itself (schools/clinics in Cameroon). State why the source fits the video.

## 5 · Production discipline
- **Unique filename per stage, never edit in place, preserve every prior deliverable.**
- **FFmpeg via `imageio_ffmpeg.get_ffmpeg_exe()`** — never a hard-coded path (packages moved after env resets).
- **Small sequential compositing passes** — a 7-input full-res graph once exhausted the sandbox.
- **Browser captures at 15 fps → compose at 30 fps**; say so in any technical note.
- **QA every final file:** decode, resolution, fps, SAR/DAR, duration — report what was checked.
- **Inspect frames when images are available. Never claim you can't see.**

## 6 · Technical failure log (do not repeat)
| Failure | Fix that worked |
|---|---|
| Wrong loop variable in output filenames → only last clip kept (was wrongly blamed on cleanup) | inspect code before inventing environmental explanations |
| Input and output both `tmpcap.mp4` | unique paths per step; FFmpeg cannot edit in place |
| Mixed/default frame rates | set input & output rates explicitly, `fps=30`, `-r 30`, `setsar=1`; verify output |
| Multiline Bash filter → array instead of one filter string | Python arg list or one correctly quoted filter string |
| "ExtraBold" variable fonts rendered **Thin** | `set_variation_by_axes([800])` bold / `[500]` regular, with fallback (verified working 17 Sep) |
| Font lacked check/arrow glyphs → missing boxes | draw simple marks with PIL lines/vector |
| Playwright Chromium missing system libs | `python -m playwright install-deps chromium` |
| `imageio_ffmpeg` absent after env change | `pip install imageio-ffmpeg`; resolve path at runtime |

## 7 · Evidence from the series so far (King-reported views)
| Platform | #1 | #2 | #3 |
|---|---:|---:|---:|
| Instagram | 13 | **47** | 41 |
| TikTok | not supplied | 87 | **137** |
- **Actionable, specific education beats generic** (#2/#3 vs #1) — direction, not proof.
- **#2 (list/educational) leads IG; #3 (pain-led) leads TikTok.** Test that split, don't average it.
- **⚠ Qualified by the handover:** earlier confident advice about fixed posting windows, minimum weekly cadence, engagement-weight hierarchies and prescribed hashtag counts is **unverified** — treat as hypotheses, never as facts.
- **Duration discipline:** 40.38 s was once called "inside a 35–40 s brief" — it wasn't. Report exact duration; ask before exceeding a cap.
- #1's **SOCIAL MEDIA → ATTENTION / WEBSITE → TRUST → ACTION** mapping was **not prominent enough** — diagrams that matter need their own clean frame (same lesson as #4's CTA frame).

## 8 · Absorbed from the lesson batches (`research/YouTube-Lessons.md`)
- Copy law [5]: visualize / falsify / nobody-else-can-say-it; 2-second test on frame 1; read aloud.
- Claim → proof [6]: every claim carries its artifact on screen; one quote at a time, never a wall.
- Anti-slop [10]: no scroll-jacking, no content-hiding animation, no moving buttons, no emoji icons — applies to any UI on camera.
- Conversion-first [12]: hierarchy (biggest = most important), solid high-contrast CTAs, never ghost buttons as primary.
- Direction exploration [13]: three directions before visual work; explicit avoid-list.
- Taste is the moat [14]: the decisions differentiate when everyone's feed looks the same.

## 10 · Video-marketing lessons (batch #4, 17 Sep 2026 — `research/YouTube-Lessons.md` [15]–[17])

### 10.1 · From Nate Woodbury ("How To Make A Marketing Video For My Business")
- **Two asset classes, don't mix them:** the *educational short-form series* (reach, mirrored to Shorts) vs the **flagship promo** (60–90 s, unlisted on YouTube, embedded on the site + used in proposals). A promo is not expected to go viral; it converts people who already arrived. → production candidate **V-13**.
- **Outcome-over-features gate:** in every script, features may be a minority of beats — the outcome must carry the majority ("features don't sell; the outcome does").
- **Clarity gate before render (4 questions):** what we do · who we help · which outcome · the emotional journey start→middle→end.
- **Testimonials = soundbites**, 5–10 s, placed under the claim they prove — only with consent (ties to [6]).
- **Polish is our pipeline:** §19 three directions + §13 pre-flight + QA — no external production.

### 10.2 · From Brooklyn Social ("How To Make High Converting Videos For Your Business")
- **3-second hook gate (written):** line 1 is a question or a specific aimed at **one person** (a clinic owner, a school proprietor) — never a self-intro, never "today we're going to talk about".
- **"Why should someone care?"** — required per beat before a script is approved.
- **Zero-fluff pass:** read aloud, delete filler (reinforces copy law [5]).
- **Every video carries one clear CTA** — independent confirmation of the PREVIEW closing-beat mandate.
- **Our "lighting/audio" equivalents:** contrast/legibility checked on a phone-sized canvas; music ducked under narration.
- ❌ Rejected: get-the-team-on-camera (no talking heads — BTS becomes build footage: screens, hands, craft), the 78 % Sprout Social stat (unverifiable here), the algorithm/lighting claim (unverified).

### 10.3 · From Digital Canva Mastery (Canva explainer tutorial)
- **Adopted (micro):** element **pop-in** for labels/numbers, and **match-and-move** when the same element grows/moves between beats — implemented in our own PIL/FFmpeg renderer. **Constraint: never animate the demonstrated UI** (no moving buttons — §3.8 anti-slop); titles/labels only.
- **Three-component pre-flight** formalised in the script header: script → visuals → voice.
- ❌ Rejected: the Canva/ChatGPT/ElevenLabs template stack — it cannot show **real websites** (our hard requirement) and produces the generic look King banned. Our pipeline already does script→visuals→voice with the real pages.

## 11 · King's decisions (17 Sep 2026) — binding
1. **No real clinic/school name in any content without the owner's written permission.** Default: **anonymise** (blur/rename logos, addresses, unique details); the live *named* concepts (YAKS, Skye, OraCare, MITOC) are unlisted and shared only with their prospect — **no public content may show or link them**.
2. **Voice:** King agrees we **re-audition a voice before video #5** (the previous `voice-00` registration does not carry over). Existing MP3s are the reference.
3. **#1 master** (`Instagram_vs_Website_v2.mp4`) is **not re-uploaded**; its TikTok status is recorded as **not posted**.
4. **Founding videos (repo, 15 Sep):** King confirms **only one of the four was posted — `clinic-founding-en.mp4` on TikTok**; the other three are unposted assets → integrated in the calendar (§A2).
5. **Strategy + calendar + shortlist: APPROVED.** **Video #4 is approved** — the remaining action is **posting** (King), first slot Tue 23 Sep TikTok / Wed 24 Sep IG, or earlier if King posts it with the outreach push.

## 9 · Changelog
- **v0.3 — 17 Sep 2026:** batch-4 video-marketing lessons absorbed (§10.1–10.3) + King's binding decisions (§11) + script gates formalised in `content/scripts/README.md`.
- **v0.2 — 17 Sep 2026:** handover absorbed — fingerprint hexes, hard rules, production discipline, full technical failure log, evidence table, qualified earlier advice.
- **v0.1 — 17 Sep 2026:** created from King's brief + repo history + lesson batches.
