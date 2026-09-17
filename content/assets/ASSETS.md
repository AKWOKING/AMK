# AMK — CONTENT ASSETS INDEX

**Updated:** 17 Sep 2026 (v0.2 — pack received, all assets in `content/`)

## Character / host art
| Asset | Path | Verified |
|---|---|---|
| Established cartoon host + phone | `content/assets/host/s1_hook.png` | ✅ 1.2 MB · used in #1 (and #4's opening art) |
⚠ Pose inventory (intro / pointing / payoff) beyond this single frame is **not available** — request more from King if a video needs them.

## Typography (fingerprint)
| Asset | Path | Verified |
|---|---|---|
| Montserrat Medium / SemiBold / Bold / ExtraBold / VF | `content/assets/fonts/Montserrat-*.ttf` | ✅ PIL loads; **variable fonts render Thin by default** — call `set_variation_by_axes([800])` (bold) / `[500]` (regular); verified working |
| Poppins SemiBold | `content/assets/fonts/Poppins-SemiBold.ttf` | ✅ |
⚠ Known glyph gaps (check marks, arrows) in some weights → draw simple marks with PIL lines instead.

## Palette (fingerprint — locked)
`navy #1B2055` · `ink #172044` · `teal #23C4B1` · `gold #FFB020` · `white #FFFFFF` — as used in `content/videos/v04-before-whatsapp/source/render.py` and confirmed in inspected frames.
⚠ Note: the AMK **brand** folder uses a different green-family kit (`brand/v1-green/` = archive). Content fingerprint is the navy/teal/amber above.

## Voice (narration)
| Asset | Path | Use |
|---|---|---|
| #4 narration | `content/videos/v04-before-whatsapp/source/narration.mp3` | 30.43 s · 44.1 kHz mono · **best available voice reference** |
| #4 CTA line | `content/videos/v04-before-whatsapp/source/cta.mp3` | 2.98 s — "DM preview for a free homepage concept" |
| Earlier tests (repo) | `tiktok/vo-video1-fr.mp3`, `tiktok/vo-test-en.mp3` | not confirmed as the selected voice |

⚠ **The previous chat's registered voice (`voice-00`) does not carry into a new chat.** For any new narration King must re-select a voice (audition) — existing MP3s are the reference to match. **Do not narrate #5+ until this is done.**

## Studio (MboaCare — the abstract-principle asset)
`content/studio/` — see its README for the honesty constraints. Studio, before/after HTML, reception photo, create.py, test.py all present and verified.
