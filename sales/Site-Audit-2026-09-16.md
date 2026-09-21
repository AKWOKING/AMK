# AMK site audit — 16 Sep 2026 (TikTok post 1 live, bio link active)

**Scope:** `site/` (live at https://amk-cm.vercel.app — homepage `index.html` + 4 concept pages). Static cascade audit + content/conversion review against Addendum #3 (conversion), Addendum #4 (measurement/loops), CRAFT-FLOOR (design floor). No browser engine in sandbox; layout findings computed from flex math and flagged for one real-device confirmation.

## Findings (11)

### P0 — broken/visibility, traffic is landing now

1. **Mobile EN/FR switch shows only EN (King-reported, root-caused).** Homepage header at ≤640px: `nav.main` and the CTA are hidden but the desktop `.lang-sw` pill stays with `flex-shrink:1` + `overflow:hidden`; the brand block (logo + uppercase tagline) eats the row on narrow widths, the pill shrinks to ~one button and FR is clipped. Same latent failure on the **clinic concept header** (Book button + logo + pill ≈ 420px at 360px viewport); school concept barely fits with placeholder names but will clip with long real college names.
   - **Fix design:** pill gets `flex:none`; buttons `white-space:nowrap`; on mobile the brand tagline `small` hides and the hamburger carries `margin-left:auto`; clinic concept header drops its Book button ≤640 (the sticky bottom bar already carries the action — matches the school template). Real-device check at 360 + 414 after deploy.

2. **Homepage never received last night's a11y upgrades** (concept pages did): no `:focus-visible` rings anywhere; count-up JS ignores `prefers-reduced-motion`. Fix: branded amber focus rings; render final stat values immediately under reduced motion.

### P1 — conversion (cold TikTok traffic arriving today)

3. **No persistent mobile CTA on the homepage.** Every concept page has the sticky WhatsApp bottom bar; the agency landing page — the one TikTok traffic hits — doesn't. Fix: mobile-only sticky bar, primary "Free preview — WhatsApp" (wa.me prefilled, source-aware), secondary "See concepts" (`#work`).

4. **Lead form asks 5 things before WhatsApp opens** (institution*, town, name, phone, current site). Standard = ≤2 fields before the action. Fix: institution name* + school/clinic chips (synced with the hero niche toggle) + WhatsApp number; everything else asked in the WA chat that opens prefilled.

5. **No social share card (`og:image` / Twitter card).** Links shared on WhatsApp/FB/TikTok unfurl blank. Fix: compose a branded 1200×630 share image (Pillow, navy/amber, bilingual line, concept thumbnails), add og/twitter meta + og:url.

### P2 — craft, SEO, measurement

6. **Thin schema:** only LocalBusiness; the 7 visible FAQs aren't mirrored as FAQPage JSON-LD. Fix: `@graph` LocalBusiness + FAQPage (same discipline shipped on concepts); `sameAs` array left commented until King provides the real TikTok/IG/FB URLs.
7. **Price glyph "₣" is obscure/wrong** for Cameroon — replace with "100 000 FCFA" (trust lives in the pricing section).
8. **Language choice doesn't persist** across pages or return visits. Fix: `localStorage.amk-lang` set/read on homepage + concepts, homepage honors `?lang=fr`; FR choice follows the visitor into concept pages.
9. **Source measurement:** bio links should carry `?src=tiktok` / `?src=ig`; the form and sticky WA links append "(from TikTok)" to the prefilled message — Addendum #4 §3, zero paid tooling.
10. **Small a11y nits:** hamburger ~36px target (→44), drawer × missing aria-label, niche tabs missing aria-selected/arrow keys, marquee only pauses on hover (also pause on focus/reduced-motion; motion CSS already kills it).
11. **Deploy drift:** the live clinic concept is the older partial-rename build without the proof/follow sections, 52px tap targets, focus rings or FAQ schema. Any redeploy today ships all of it. Zip is already rebuilt; needs King's Vercel CLI deploy (or connect Git per DEPLOY.md option B).

## Batch plan (brainstorm)

- **Batch A — emergency (now, mechanical, zero content risk):** #1 switch, #2 focus/reduced-motion, #7 FCFA, #6 schema, #10 nits, #11 redeploy. Unblocks the live bio link.
- **Batch B — conversion (same pass, tested before deploy):** #3 sticky bar, #4 form trim, #5 og:image, #9 src attribution.
- **Batch C — next natural iteration:** #8 language persistence cross-page (touches all 3 generators + concept links), then King connects Git push-to-deploy so this class of drift stops recurring.

QA after edits: local static server, King opens the sandbox preview ON HIS PHONE (360/414, EN+FR, reduced-motion), screenshots header/bar/form; then Vercel deploy + Rich Results Test of the JSON-LD.
