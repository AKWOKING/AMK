# Video 9 — "How to Create AI Motion Graphics in Minutes (FREE Master Prompt)" — ReachMora

URL: https://youtu.be/n50KkoucMpU · Batch: `research/youtube-lessons/2026-10-11-batch-3/` · 2026-10-11

## 1 · SOURCE CAPTURE

**Transcript: RETRIEVED IN FULL** (2/2 chunks; chunk 2 is site boilerplate).
- **Producer:** ReachMora — channel `@ReachMora`. Subscriber count not exposed on the pages fetched
  → **UNVERIFIED** (not guessed).
- **Claimed credentials:** none. Explicitly anti-credential: "My job is to give you the stuff
  internet gurus are trying to sell you as a course."
- **What he is selling: nothing.** The master prompt is given away in a free Google Drive document,
  and he says so pointedly — "No course, no $97 prompt pack, no DM me on Instagram to get access."
  He asks only for likes and subscriptions. **This is the cleanest commercial posture of any video
  in batches 1–3** (contrast video 7, sponsored by the platform it recommends).
- **Length 09:17 · Uploaded 2026-09-30 · Views 130,921 · Likes 4,785 · Category Education**
  (YouTube watch page, 2026-10-11). **Eleven days old — the most current video reviewed in any
  batch.** Not re-dated.
- **Ethics note in his own description, worth quoting:** "The goal isn't to copy another creator's
  finished work… Always make sure you have the appropriate rights or permissions for any reference
  material or assets you use. AI-generated content should also be reviewed before publishing for
  visual errors, unexpected elements, trademarks, copyrighted material, or other issues." That is a
  more responsible framing than most paid courses offer.

**The seven steps:** ① find a style reference on Pinterest and download it · ② Claude analyses the
"visual DNA" (motion, transitions, colours, typography, composition, camera movement, pacing, visual
hierarchy) and emits a prompt for the Omni Flash model · ③ turn that into a **universal master
prompt** · ④ feed it any script (his test script came from ChatGPT) and get per-beat prompts ·
⑤ generate 10-second clips in Google Flow · ⑥ voiceover in ElevenLabs · ⑦ assemble in CapCut
(strip silent gaps, combine with Alt+G, match visuals to narration, export).

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | **"Create professional-looking motion graphics in minutes using AI without spending a single dollar"** | **PARTIALLY FALSE as stated — the free tier is real but capped, and he never says so** | Google Flow's free tier gives **50 credits per day**, and Gemini Omni Flash at 720p costs **7 credits for 4 seconds up to 15 for 10** (https://wink.ai/blog/gemini-omni-flash-review , https://saascrmreview.com/google-flow-review/). That is roughly **3–7 short clips a day**, not unlimited. Worse, Google's own pages **contradict each other on access**: the Flow pricing page shows a no-subscription route with 50 daily credits, while the Get Started page still lists an AI Plus/Pro/Ultra subscription among the requirements (https://saascrmreview.com/google-flow-review/). The video's workflow — many beats, several retries — would burn the daily cap quickly. |
| 2 | "A motion graphic that could take a designer hours or days can be recreated with AI in a few minutes" | VENDOR SELF-REPORT | His own demo, unaudited. Plausible for a short stylised piece. |
| 3 | Claude (free plan) can analyse an uploaded video and extract its visual characteristics into a reusable prompt | VERIFIED IN-DEMO | Shown on screen. Claude's free tier exists; the specific video-upload capability on the free tier was **not independently verified** — noted, not assumed. |
| 4 | The **Omni Flash** model exists and is selectable inside Google Flow | VERIFIED | Model `gemini-omni-1.1-flash`, launched 19 May 2026; selectable in Flow (https://geotoolbox.ai/blog/gemini-omni , https://wink.ai/blog/gemini-omni-flash-review). |
| 5 | A master prompt can break any script into visual beats and keep one visual style across them | VERIFIED IN-DEMO | Demonstrated with a different script from the reference. |
| 6 | ElevenLabs produces the voiceover; CapCut assembles it | Real tools | ElevenLabs' free-tier limits were **not researched** (no decision turns on it). CapCut is free. |
| 7 | Reusable "for your next 50 videos" | VENDOR SELF-REPORT | The workflow logic supports reuse; the quality claim is unaudited. |
| 8 | Paid tiers exist if you need more | Implied, not stated | Google AI Plus **$4.99/mo** (200 credits/mo), Pro **$19.99** (1,000), Ultra **$99.99–$199.99**; API at **$0.10 per second of 720p output** (https://geotoolbox.ai/blog/gemini-omni). **He never mentions that sustained use costs money.** |

**One more fact the video omits that matters to us:** Omni Flash output generated free inside
YouTube Shorts / YouTube Create is capped at 10 seconds, has audio editing disabled, and **carries a
SynthID watermark** (https://www.ai-inspo.com/blogs/video/gemini-omni-flash-pricing). Any free-tier
asset we used would be watermarked.

## 3 · TOOL AUDIT

| Tool | What it does | Cost | **Can the orchestrator do it?** | Verdict |
|---|---|---|---|---|
| **Claude** (analyse a reference, write a reusable style prompt) | Turns a visual reference into a structured style spec | Free tier | **Yes — this is exactly what I do.** Reverse-engineering a reference into a reusable style specification is the same task as our uniqueness protocol's Design Read. | **Not adopted as a tool** — I do the step myself |
| **Google Flow / Omni Flash** | Generates the video clips | Free 50 credits/day; then $4.99–$199.99/mo; API $0.10/sec | **No — I cannot generate video.** This is a genuine capability gap. | **HOLD** — real gap, but see §5: it conflicts with a house rule for client work |
| **ElevenLabs** | Voiceover | Freemium (limits not researched) | **No** — I cannot produce a client-deliverable voice track | **HOLD** — same scope question |
| **CapCut** | Assembly/editing | Free | King edits | **KEEP (free)** if we ever produce video |
| **Pinterest** | Style references | Free | I can research references | **Neutral** — note that PRE-FLIGHT §2 step 3 already names Awwwards, Godly, Land-book, SiteInspire, Mobbin, Lapa Ninja, Dribbble as the inspiration sources; Pinterest is not on that list |
| **ChatGPT** (test script) | Generates a test script | Free tier | **Yes** | Not adopted as a tool |

**Tools that survive: CapCut (free) and Pinterest (free) — and one genuine capability gap (video and
voice generation) placed on HOLD, not adopted.**

## 4 · GAP-FILLING

**What the video should have covered and did not:**
- **The daily credit cap.** The single most important omission: the workflow he demonstrates cannot
  be run at volume on the free tier, and the "without spending a single dollar" framing hides it.
- **The SynthID watermark** on free-tier output.
- **Quality control beyond "watch it once."** His own description says to review for "visual errors,
  unexpected elements, trademarks, copyrighted material" — but the tutorial never shows that review.
- **Rights.** Reverse-engineering another creator's animation into a reusable template sits close to
  the line he himself draws in the description. He flags it; he does not solve it.

**Cameroon / WhatsApp-first / optician application:**
- **For client deliverables: this conflicts with house rules.** `AMK-DESIGN-SKILLS.md` §25 ("one
  photo = one meaning") and §32, plus `research/PHOTO-LABO-PIXEL-8A-2026-09-24.md`, commit us to
  **real photographs** of the actual cabinet, frames and people, and `tools/qa/audit_images.py`
  enforces the structure and privacy side. The DM Optique site captions every image "Photo
  d'illustration" precisely because we do not pass off imagery as the client's reality. **AI-generated
  motion graphics of an optician's shop or frames would misrepresent a healthcare business.**
- **For AMK's own content: genuinely useful.** Explaining what a try-on app does, or how an eye exam
  works, has no real photograph available — that is the honest use case for generated visuals.
- **The reverse-engineering *method* is adoptable without any tool.** "Study a reference until you
  can name its motion, palette, typography, pacing and hierarchy, then write that down as a reusable
  spec" is exactly our uniqueness protocol's Design Read, stated better than we state it.

**Counter-evidence:** the video's premise is that generated visuals can substitute for designed ones.
Our anti-slop rules (`AMK-DESIGN-SKILLS.md` §3.7 fake UI and assets, §3.8 vibe-code tells) exist
because generated visuals read as generated. For a **trust** business — an optician handling eyes —
that reading is a liability, not a style.

## 5 · INTEGRATION RECOMMENDATION

**ADOPT (2 items, both free, into existing files — §4b respected):**
1. **The reverse-engineering method, without the tool.** When studying a reference, name explicitly:
   motion · transitions · palette · typography · composition · camera movement · pacing · visual
   hierarchy — then write it as a reusable spec. This sharpens the **Design Read** step we already
   require. → logged against `AMK-DESIGN-SKILLS.md` §2 (uniqueness protocol) via this batch pointer.
2. **The ethics checklist, adopted in advance.** If AMK ever publishes AI-generated visuals: confirm
   rights to any reference, review every output for visual errors, unexpected elements, trademarks
   and copyrighted material, and **label it**. → logged in
   `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md` as a HOLD-with-conditions rule.

**HOLD (not adopted):** Google Flow / Omni Flash and ElevenLabs. Real capability gaps, but:
- they conflict with the real-photo rule for **client** work;
- the free tier is 50 credits/day with a SynthID watermark, and sustained use costs $4.99–$199.99/mo
  or $0.10/second — a paid line item with no client paying for it yet;
- **Written trigger to revisit:** a concrete AMK-owned content need with no real-footage answer
  (e.g. explaining the try-on app), approved by King.

**DO NOT ADOPT:** AI-generated imagery or video for any **client** deliverable. It contradicts
§25/§32, the phone-photo standard, and the "Photo d'illustration" honesty practice — and for a
business handling people's eyes, a synthetic image of their shop is a misrepresentation risk we
cannot take.

## 6 · SUMMARY BLOCK

**Core idea (2 sentences).** Reverse-engineer a motion-graphics reference with an AI assistant into a
reusable master prompt, then generate clip-by-clip visuals, a voiceover and an edit from any script.
The method is sound and given away free, but "without spending a single dollar" hides a 50-credit
daily cap and a watermark, and the output conflicts with our real-photo rule for client work.

**KEPT.** The reverse-engineering method as a sharpened **Design Read** (name the eight axes, write
the spec) · the AI-visuals ethics checklist adopted in advance as a HOLD-with-conditions rule →
logged against `AMK-DESIGN-SKILLS.md` §2 and `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md`
(pointer: this batch).

**HOLD.** Google Flow / Omni Flash and ElevenLabs — genuine capability gaps, revisited only on the
written trigger above.

**REJECTED.** AI-generated visuals for any client deliverable (contradicts §25/§32, the phone-photo
standard, and the "Photo d'illustration" practice) · the "free, no dollar" framing (capped free
tier, watermarked output, paid tiers unmentioned).

**OPEN QUESTIONS.**
- Does AMK want a stated policy line — "we do not publish synthetic imagery of a client's premises,
  staff or products" — as a selling point rather than a limitation? For a healthcare client it could
  be a differentiator.
- Is there an AMK-owned content need with no real-footage answer that would justify a paid video
  generation line item?
