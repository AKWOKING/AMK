# AMK — MboaCare demo studio

**Status:** ✅ received 17 Sep 2026 (from `AMK_New_Chat_Starter_Pack/website-demo/`, migrated here unchanged).

## Inventory (verified)
| File | Verified |
|---|---|
| `Website_Demo_Studio.html` | 546 KB · title "AMK · Website demonstration studio" · self-contained (pages + photo embedded, no external requests) |
| `before.html` | 268 KB · title "MboaCare \| Before demo" |
| `after.html` | 270 KB · title "MboaCare \| After demo" |
| `clinic-reception.jpg` | 196 KB · AI-generated, fictional clinic |
| `create.py` | builds all three HTML files + embeds the photo (23 KB) |
| `test.py` | Playwright interaction tests (1 KB) |

**Studio controls:** Before/After · Phone/Desktop · reset · simulated 5-second load · clean recording view.

## What "before" and "after" actually are
- **Before:** plausible dated institutional design — vague "excellence and commitment" copy, fixed 980 px desktop layout, small nav, long management/mission text, WhatsApp only in the footer.
- **After:** specific family-care services + Douala location, responsive, readable type, working mobile menu, demo booking dialog, clear contact/directions, persistent WhatsApp button.

## Honesty constraints (carry into every frame, every caption)
- **Fictional clinic**, sample address/hours — never present as a client.
- Receipt photo is **AI-generated**.
- No real patient testimonials, credentials or clinical outcomes.
- Contact/booking actions are **simulated**; they do not send messages.
- The slow-load is **deliberately simulated**, not a measured fault of a real site.
- EN/FR text exists in the concept, but this is **not** a complete functional bilingual production site — do not overclaim.
- These assets exist for controlled education — **not to shame a real business**.

## Use in the engine
This is **one asset among several** (CONTENT-LESSONS §4): right when a video teaches a problem in the abstract. Real prospect concepts and shipped work are the other sources — always state why the source was chosen.

## Before any re-render
`capture.py` (Playwright) is the way to regenerate captures; install with `pip install playwright && python -m playwright install chromium && python -m playwright install-deps chromium`. Captures must be sampled at **15 fps** and composed at 30 fps.
