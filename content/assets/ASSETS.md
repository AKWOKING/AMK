# AMK — CONTENT ASSETS INDEX

**Purpose:** character art, fonts, voice references, palette, typography — where each actually lives.
**Status 17 Sep 2026:** repo assets indexed ✅ · previous-chat assets (`clinic-reception.jpg`, `s1_hook.png`, studio art) **not received** ⛔.

## Brand & identity (repo, verified present)

| Asset | Path | Use |
|---|---|---|
| Logo kit | `brand/AMK-Logo-Kit.html` · `brand/AMK-logo-primary.{svg,png}` · `-mono` · `-square` | end cards, watermarks, covers |
| Legacy green kit | `brand/v1-green/` (+ `funnel-v1-green.svg`) | archive — do not use in new content |
| Avatar | `brand/avatar-amk.png` | profile pictures, host reference |

## Content palette (from the 17 Sep brief — the fingerprint)
- **Navy / teal / amber.** Exact hexes to be locked into a token file (`content/assets/palette.css` + swatches) once the studio files arrive and the previous chat's chosen values can be reconciled — **do not invent hexes**. Interim: pull from the live concepts' CSS (`demos/concept-*.html` `:root` blocks) where they match navy/teal/amber.

## Typography (fingerprint)
- **Montserrat / Poppins** for on-screen text and captions. Both are Google Fonts — safe for FFmpeg drawtext pipelines and browser captures.
- Repo note: the concepts use Outfit/Inter/Nunito per client brand; the **content** fingerprint is Montserrat/Poppins — do not confuse the two systems.

## Voice (host narration)
- **Selected voice: pending** — the chosen voice from the previous chat was not received (no reference file). Placeholder: `tiktok/vo-video1-fr.mp3` and `tiktok/vo-test-en.mp3` exist in-repo as *earlier* tests — **not confirmed** as the selected voice. ⛔ King to confirm or supply the reference sample.
- Rule: same voice every video; English and French variants must sound like the same character.

## Character art (host)
- ⛔ Not received. Expected: the cartoon host used in the previous chat's videos (referenced by `s1_hook.png`) + any pose/expression set.
- When it lands → `content/assets/host/` with a pose inventory (intro, pointing, shrug, payoff) so scripts can name poses.

## Studio (MboaCare demo)
- ⛔ Not received: `Website_Demo_Studio.html`, `before.html`, `after.html`, `timeline.json`, `clinic-reception.jpg`.
- Destination once received: `content/studio/` (see its README for the full expected inventory + verification steps).

## Screens & captures we can produce today (no dependency on uploads)
- **Our own concepts** (`demos/concept-*.html`, `hosting/previews/`) — yaks, skye, oracare, sasse, comobil, sahiscol, la-retraite, clinic-bonaberi, mitoc, sample-secondary.
- **Build footage**: scroll/tap/load/contact-flow captures from any of the above, at 15fps sampled → 30fps composed.
- **Rule reminder:** anime/credit decisions belong to King; anonymise when consent is absent.

## Changelog
- **17 Sep 2026:** index created; repo assets verified; pending list explicit.
