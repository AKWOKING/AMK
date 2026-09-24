# AMK DESIGN SKILLS LIBRARY

_Consolidated from three MIT-licensed agent skill libraries: `bergside/awesome-design-skills` (TypeUI, 67 design-system families), `Leonxlnx/taste-skill` (anti-slop frontend), and `emilkowalski/skills` (animation/design engineering). Vendored sources live in `design/vendor/` (full family token sheets: `design/vendor/bergside-skills/<family>/`, digest `design/vendor/registry-digest.json`; motion skills: `design/vendor/emil/skills/`; taste skills: `design/vendor/taste/skills/`)._

**How to use:** the build pipeline is `design/WORKFLOW.md` (9 stages). Before building, read §1-§2 below (infer the brief, set dials), lock a token sheet from `design/STYLE-TOKENS.md`, build against §4-§11, run the motion pass (`design/MOTION.md`), run §13 before delivery. For image/comps work, also read §15. This library is an overlay on top of the AMK standing standards (single-file HTML, EN|FR, base64, Concept Production Standard, nameless-template rule, no fabricated facts).

---

## §1 BRIEF INFERENCE — Read the Room First

Most bad AI design comes from jumping to a default aesthetic instead of reading the brief.

**Signals to read, in order:**
1. **Page kind** — landing / portfolio / redesign-preserve / redesign-overhaul / editorial.
2. **Vibe words** the client used — "premium", "calm", "modern", "playful", "trustworthy", or a reference (URL, screenshot, Dribbble shot).
3. **Reference material** — screenshots, links, named brands. A provided reference is a hard constraint (e.g. OraCare v2 = Odentrics reference = faithful reproduction, see §4.4 override).
4. **Audience** — the audience picks the aesthetic, not your taste. Buea/Douala school parents = trust + warmth + clear prices. Clinic patients = anxiety removal + clarity.
5. **Existing brand assets** — logo, colors, fonts, photography. On redesigns these are starting material.
6. **Quiet constraints** — trust-first, local reality (mobile-first, WhatsApp-first), language (EN|FR). These OVERRIDE aesthetic preference.

**Output a one-line Design Read before generating** (say it, don't skip it):
> "Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design family>."

Example: *"Reading this as: local clinic landing for anxious first-time patients, with a warm premium-spoken language (Odentrics reference), leaning toward cream/sand + soft-navy + gold, rounded-2xl, glass nav, WA-first booking."*

**If the brief genuinely diverges, ask exactly ONE question** — never a dump. If context supports confident inference, declare the read and proceed.

**Anti-default discipline — do NOT default to:** AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism everywhere, infinite-loop micro-animations everywhere, Inter + slate-900, beige+brass (see §6.2).

---

## §2 THE THREE DIALS

Set explicitly after the design read. Every layout/motion/density decision is gated by these.

- **DESIGN_VARIANCE** 1-10 (1 = perfect symmetry, 10 = artsy chaos)
- **MOTION_INTENSITY** 1-10 (1 = static, 10 = cinematic)
- **VISUAL_DENSITY** 1-10 (1 = art gallery, 10 = cockpit)

**AMK presets:**

| Project | VARIANCE | MOTION | DENSITY | Why |
|---|---|---|---|---|
| School/clinic concept (conversion) | 6 | 4 | 4 | trust-first + light editorial; motion = reveal + hover only |
| AMK main site (mastery demo) | 7 | 6 | 4 | must demonstrate craft, but audience is small-business owners |
| Premium consumer / DTC | 7-8 | 5-7 | 3-4 | brand language |
| Playful / Awwwards / agency | 9-10 | 8-10 | 3-4 | brief says wild |
| Public-sector / regulated / a11y-critical | 3-4 | 2-3 | 4-5 | constraints override |
| Redesign — preserve | match existing | +1 | match existing | audit first |
| Redesign — overhaul | +2 | +2 | match existing | greenfield visuals, keep IA |

Dial mechanics: variance 1-3 = symmetric grids; 4-7 = offset (overlaps, mixed aspect ratios); 8-10 = asymmetric (masonry, fractional grid units, big empty zones). Motion 1-3 = hover/active only; 4-7 = transitions + scroll reveals; 8-10 = scroll-triggered choreography. Density 1-3 = py-32+ sections; 4-7 = standard; 8-10 = tight, 1px dividers, mono numbers.
**Mobile override:** any asymmetric layout above md MUST collapse to strict single-column below 768px.

---

## §3 ANTI-SLOP: HARD BANS (the tells that read as "AI made this")

### 3.1 Color & surface
- NO pure `#000000` / `#FFFFFF` as page bg/text. Off-black (zinc-950, warm charcoal) and off-white always.
- NO AI-purple/blue glow gradients, neon outer glows, floating blobs with no purpose.
- NO excessive gradient text on large headers.
- NO oversaturated accents (saturation < 80%).
- NO mixing warm and cool grays in one project. One gray family, tinted consistently.
- Generic black drop shadows banned → tint shadows to the background hue.
- NO decorative crosshair/hairline grid lines, version footers (`v1.4.2`), live-stock counters, locale/time/weather strips ("LIS 14:23 · 18°C").

### 3.2 Typography
- **Inter as default is banned** (acceptable only for public-sector/a11y-first briefs). Default pool: **Outfit** (AMK house font), Geist, Cabinet Grotesk, Satoshi, Space Grotesk.
- **Serif discipline:** serif is discouraged as default. Only when brand names a serif OR aesthetic is genuinely editorial/luxury/heritage AND you can say why. BANNED as defaults: Fraunces, Instrument Serif. Rotate serifs across projects if justified.
- **Emphasis:** italic/bold of the SAME font. Never inject a serif word into a sans headline.
- **Italic descender clearance:** italic display words with y/g/j/p/q need line-height ≥ 1.1 + padding-bottom reserve.
- NO oversized screaming H1s (control hierarchy with weight+color, not raw scale); NO all-caps subheaders everywhere; use `text-wrap: balance`/`pretty` to kill orphans.
- Numbers in data contexts: tabular figures (`font-variant-numeric: tabular-nums`) or mono.

### 3.3 Layout
- **NO three equal feature cards** as the default row (use 2-col, asymmetric grid, bento with exact cell count, horizontal scroll).
- NO empty bento cells (N items → exactly N cells; use `grid-auto-flow: dense`; verify spans interlock).
- NO section-layout repetition: a layout family appears at most ONCE per page; 8 sections need ≥ 4 different families.
- **Zigzag cap:** max 2 consecutive left-img/right-text splits.
- **Split-header ban** ("big headline left + tiny explainer floating right") — stack vertically instead, unless the right column carries a real visual/interactive element. (OraCare v2 001 header = reference exception: right column carries avatar stack + CTA, a real element.)
- NO `h-screen` — use `min-h-[100dvh]` (iOS Safari jump).
- NO flexbox percentage math — CSS Grid.
- Container: max-w ~1180-1400px, auto margins.
- Buttons in card groups pinned to card bottom (align CTA line); feature lists start at same Y across columns.
- 1-2px optical adjustments for mathematically-centered-but-optically-off elements (icons in buttons, play circles).

### 3.4 Decoration & labels
- **Eyebrow restraint:** max 1 eyebrow per 3 sections (hero counts as 1). *Exception: when a client-provided reference uses numbered eyebrows on every section (Odentrics), the reference wins — it's an explicit brief instruction, not a default.*
- NO section-number eyebrows (`001 · Capabilities`) as a default; NO `01/4` pagination on tiles; NO "Brand · No. 01" sub-eyebrows; NO version labels in hero (V0.6, BETA) unless it's a launch.
- Middle-dot `·` rationed: max 1 per line in metadata strips.
- NO decorative status dots (only real semantic state, sparingly).
- NO scroll cues ("Scroll ↓", mouse-wheel icons).
- NO pills/labels overlaid on photos (captions go below the image); NO photo-credit captions as decoration ("Field study no. 12"); NO decorative text strips at hero bottom ("BRAND. MOTION. SPATIAL.").
- NO floating top-right sub-text in section headers.
- NO scoring/progress bars with filled background tracks on marketing pages.
- NO generic step labels ("Stage 1/2/3") — the step's own verb-noun is the label.

### 3.5 Em-dash decision (AMK ruling)
The source skill BANS em-dashes everywhere (top production tell in EN). AMK ruling:
- **EN copy:** minimize. Use periods, commas, colons, parentheses. Hyphen `-` for ranges ("3-5 days").
- **FR copy:** the tiret/em-dash is standard French typography — permitted in FR strings (native readers expect it).
- Never use it as a bullet/decoration either language.

### 3.6 Content & data ("Jane Doe" effect)
- NO generic names (John Doe, Sarah Chan), NO generic avatars, NO "Acme/Nexus/SmartFlow/Cloudly" brand slop.
- NO fake-precise numbers unless from real data OR explicitly labeled sample/mock (our concepts: prices/hours/reviews labeled "sample" — keep doing this).
- NO filler verbs: **Elevate, Seamless, Unleash, Next-Gen, Revolutionize, Game-changer, Delve, Transform your day, Tap into, Unlock your potential.** Concrete verbs only.
- NO "In the world of..." openers.
- Active voice. No exclamation marks in success messages. Sentence case for headers (not Title Case).
- **One copy register per page.**

### 3.7 Fake UI & assets
- **NO div-based fake screenshots** (fake dashboards/terminals built from divs) — the #1 LLM tell.
- NO hand-rolled decorative SVGs as default (one simple geometric mark OK).
- NO pure-text "minimalism" — even minimal sites need 2-3 real images.
- NO broken stock links. Use generated images (our standard), then reliable placeholders, then clearly-labeled TODO slots + tell the user.

### 3.8 VIBE-CODE TELLS (added 17 Sep 2026, YC design review [10] — `research/YouTube-Lessons.md`)
*The tells that make a visitor think "this was AI-generated" and quietly discount the business behind it. Every item below is a hard ban unless a written, brand-driven reason exists.*

- **NO scroll-jacking** — never intercept native scroll for animation ("like molasses": you lose your place and the scroll indicator lies). Readable progress beats choreography.
- **NO hover states that hide or de-emphasise** — nav items fading out on hover is the opposite of an invitation. Hover either invites the click (pop / one shade lighter / subtle glow) or reinforces meaning; the browser's own hand cursor is free, so it's enough.
- **NO essential information behind hover** — mobile has no hover. Anything a user needs is visible, tappable, or in the layout.
- **NO moving buttons** — a control that follows the cursor or drifts cannot be clicked reliably and reads as a bug.
- **NO entrance animations that hide content** — fade-ins must never leave a section looking empty (a FAQ caught mid-fade reads as "one lonely question"); content is present in the DOM and painted; never gate it on a timer.
- **NO decorative scroll-following lines / meteors / cursor glows** — if it wouldn't be worth a week of hand-coding, it isn't worth shipping because it was free.
- **NO emoji as UI icons** — standard-icon tells. Inline SVG only (our standing rule).
- **NO mixed type styles in one header block** — logo + kicker + H1 + sub + fourth style = five styles and zero hierarchy; each block has at most: kicker (optional) + H1 + sub.
- **NO fake dashboards** — same ban as §3.7, restated: red/green/blue/purple Google-colour callout cards are a hallmark tell.
- **NO bento card grids as a default** — icon + text ×6 is the standard LLM section; bento allowed only when the content is genuinely modular with exact cell count and interlocking spans (see §3.3), never as the house rhythm.
- **Banned empty claims** — "10x everything", "unlocked", "seamless", giant whitespace substituting for information. A visitor scrolling halfway must be able to say what the business does.
- **Brand palette first, always** — derive colour/type from the client's own logo, signage, or research BEFORE generating layout (YAKS / Labo storefront method). Never accept an AI default palette; "you have to be intentional about ending up in a different place."
- **The editor rule** — every generated element must survive: *"would a designer have chosen this on purpose?"* If it exists only because it was easy, cut it. Just because it's possible doesn't mean it ships.
- **QA everything yourself** — click every control, scroll every section on a phone, in both languages, before delivery (this is the human half of §18's verification ladder).

---

## §4 THE LOCKS (consistency rules)

1. **Color Consistency Lock:** one accent color, used identically across ALL sections. A warm-cream site does not get a blue CTA in section 7.
2. **Palette Rotation:** don't ship the same family twice in a row (see §6.2 banned default + rotation pool).
3. **Shape Consistency Lock:** ONE corner-radius system per page (all-sharp / all-soft 12-16px / all-pill for interactive). Mixed only with a documented rule followed everywhere (e.g. "buttons pill, cards 16, inputs 8").
4. **Page Theme Lock:** ONE theme for the whole page (light/dark). No section flips to inverted mid-scroll. Tints within the same theme family are fine (sage-tinted section on a cream page ✓; a navy section on a cream page is a deliberate block, used max ~2x, e.g. team + booking — keep it intentional, not random).
5. **CTA Intent Lock:** ONE label per intent, page-wide. "Book Your Visit" everywhere it's book intent. Never "Get in touch" + "Contact us" + "Let's talk" coexisting.
6. **One design system per project.** No mixing Material + shadcn + custom.
7. **Icon family lock:** one icon family, one stroke weight. Allowed: Phosphor, HugeIcons, Radix, Tabler. Never hand-roll icon paths. Emoji policy: banned in code/visible text by default; permitted with intent for playful/social-native briefs (AMK concepts use a few — tooth, phone, location — deliberately, consistently).

### §4.4 Reference-Override Rule (AMK addition)
When the client provides an explicit visual reference (screenshot/Dribbble), the reference's patterns — even ones this library would flag (numbered eyebrows, cream+brass palette, photo-pill captions) — are INSTRUCTIONS, not defaults. Reproduce faithfully. Log what was overridden and why (the reference named it). This is what made OraCare v2 correct.

---

## §5 TYPOGRAPHY SYSTEM

- **House pairing:** Outfit (display, weights 500-800) + Inter or Outfit (body 400-600). Outfit is the AMK approved non-default display font; body Inter is acceptable in the AMK single-file stack but prefer Outfit for both when the design allows.
- Display scale: `clamp(36px, 4vw, 54px)` for heroes with 4+ word headlines; `clamp(44px, 6vw, 74px)` only for 3-5 word headlines. **Headline ≤ 2 lines desktop.** If it wraps 3+ at the chosen size, the FONT is wrong, not the copy.
- Eyebrow: 11-12px, uppercase, tracking 0.14-0.2em, semibold.
- Body: 15-16.5px, line-height 1.6, **max width 65ch** (~640px).
- Hierarchy: use Medium(500)/SemiBold(600) between Regular and Bold for subtle steps.
- Negative tracking on large headers (-0.02em), positive on small-caps labels.
- Weight 800/900 for hero display; never extra-bold shouting on everything.
- **Font pairing:** one display face for titles, one body face; the body never carries the personality, it carries the reading. The title face may run tighter (negative tracking at large sizes); body never tighter than -0.01em.
- **Line-height is inverse to size:** small text (captions, labels, meta) needs MORE line-height (1.5-1.7); display can run tight (0.95-1.05) with descender reserve (§3.2). Never one line-height for the whole page.
- **Never centre paragraphs or small text.** Centring is for 1-2-line hero/section statements; body, lists and FAQ answers stay left-aligned.

---

## §6 COLOR SYSTEM

### 6.1 Construction
- Max 1 accent. Neutral base (warm or cool, locked). 1-2 secondary tints for section backgrounds.
- Text on accent: WCAG AA 4.5:1 (3:1 for large text). Audit every CTA.
- Shadows tinted to background hue. Consistent light direction across all shadows.
- **60-30-10 balance:** ~60% neutral surfaces, ~30% brand colour, ~10% accent. The accent is the rarest colour on the page; CTAs and key numbers own the 10%. If the accent is everywhere, nothing is emphasised.
- **Tinted neutrals are derived, not picked:** background tints = the brand/accent hue with saturation and brightness reduced (a contextual tint, never accidental grey).
- **Contrast is checked, not felt:** run every brand/background pair through a contrast checker (Coolors Contrast Checker or equivalent) before shipping: 4.5:1 body, 3:1 large (the §13 promise, verified).
- Skip colour-psychology folklore: legibility first, one personality accent second.

### 6.2 The premium-consumer default BANNED (2nd most-recurring AI tell)
For premium/warm briefs the LLM default is: **cream/beige bg (#f5f1ea family) + brass/clay/oxblood accent (#b08947 family) + espresso text (#1a1714 family).** BANNED as a default reach.
**Rotation pool (pick per project, never repeat consecutively):**
- Cold Luxury: silver-grey + chrome + smoke
- Forest: deep green + bone + amber accent
- Black & Tan: true off-black + warm tan, sharp contrast
- Cobalt + Cream: saturated blue on one neutral
- Terracotta + Slate: warm rust against cool grey
- Olive + Brick + Paper
- Monochrome + single saturated pop (off-white + off-black + electric blue/emerald/hot pink)
- **Odentrics family (cream/sand #F7F1E8 + soft navy #16323A + gold #C9A24B + sage #7FA88F)** — used for OraCare v2 per explicit reference. Next warm-premium project MUST pick a different family.

### 6.3 Muted pastel set (for tags/badges/chips, minimalist directions)
Pale Red #FDEBEC/#9F2F2D · Pale Blue #E1F3FE/#1F6C9F · Pale Green #EDF3EC/#346538 · Pale Yellow #FBF3DB/#956400.

---

## §7 LAYOUT DISCIPLINE (hard rules)

**Foundation method: build order, spacing-first, hierarchy & zoom-out test → §19.**

**Hero:**
- Must fit initial viewport. Headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines, CTAs visible without scroll.
- Top padding cap ≈ 6rem desktop (content must not float halfway down).
- **Max 4 text elements:** (eyebrow OR brand strip) + headline + subtext + CTAs (1 primary + max 1 secondary). NO tagline below CTAs, NO trust micro-strip, NO pricing teaser, NO avatar row inside hero.
- "Trusted by" logo wall goes UNDER the hero, never inside.

**Navigation:**
- ONE line on desktop. Height ≤ 80px (default 64-72px).
- Active state, focus rings, mobile hamburger with morph (lines → X), staggered link reveal in the open menu.

**Sections:**
- Section padding: py 6-10rem at density 3-4 (AMK concepts: 84px ≈ 5.25rem is the floor).
- Vary rhythm: density, image:text ratio, alignment, scale, whitespace, background tint.
- Every multi-column layout declares its <768px fallback in the same block.
- Grid gaps consistent per section; optical bottom padding ≥ top padding.

**Bento:**
- Exact cell count = content count. Rhythm, not repetition. ≥ 2-3 cells with real visual variation (image, tint, pattern) in any multi-cell grid — no all-white-on-white text cards.

---

## §8 COMPONENT FAMILIES

### Buttons
- Pill or max 12px radius (per shape lock). Generous padding (15-16px / 26px).
- **Contrast check mandatory** (no white-on-white, no invisible ghost over photos — use scrim/stroke).
- **Primary is always solid with high contrast.** An outline/ghost treatment is never the primary action on a page: outlined buttons read as invisible and get skipped [12]. Our ghost/tertiary tier stays only as a third choice, when a filled primary exists in the same viewport and the outline passes contrast on its background.
- **No wrap:** label fits one line at desktop; ≤ 3 words for primary CTAs (ideally 1-2); widen the button before constraining it.
- Hover: bg shift + translateY(-2px) + tinted shadow; arrow translates 4px.
- **Active/press:** `scale(0.98)` or `translateY(1px)` — simulate physical push.
- Premium pattern ("button-in-button"): trailing arrow sits in its own small circular chip flush with the button's right edge.
- Ghost/tertiary/text-link as third tier to reduce "always one filled + one ghost" noise.

### Forms
- Label ABOVE input (never placeholder-as-label). Error below input, inline. Helper text present in markup.
- Inputs: 12px radius, 1.5px border (accent on focus + soft ring), 14.5px text.
- Full contrast audit: inputs, placeholders, focus rings, helper/error text vs section bg.
- States: loading (skeleton matching final shape), empty (composed, shows how to fill), error (inline, no `window.alert`).
- AMK conversion pattern (proven in OraCare v2): 4-6 fields max, first-person CTA ("Send my request"), pre-written message preview, ref code (OC-XXXX), JSON payload logged for backend.

### Cards
- Only when elevation communicates real hierarchy; else use border-t/divide-y/whitespace.
- 20-22px radius (AMK standard 22px / reference-driven), 1px border at 8% ink OR tinted shadow — not both heavy.
- Hover: translateY(-6px) + soft tinted shadow (0.1-0.12 alpha).
- **Double-Bezel technique (premium):** outer shell (subtle bg + hairline ring + p-1.5/p-2 + 2rem radius) wrapping inner core (own bg + inset top highlight + radius − 0.375rem). Makes cards read as machined hardware.
- Equal-height card groups: pin CTAs bottom; align list starts.

### FAQ/Accordion
- Boxless: items separated by 1px dividers, sharp +/− toggle (AMK OraCare uses boxed items per Odentrics reference — reference wins).
- Native `<details>/<summary>` is fine for single-file concepts (zero JS, a11y free).

### Avatars / faces
- Real photos; unique per person. B&W strip treatment = grayscale(1) with hover colorize (OraCare v2). Circle, squircle, or rounded-square — don't default to circle-everything.
- Avatar stacks: overlapping, 2.5px ring in section bg color, "N+" counter chip.

---

## §9 MOTION

> Full playbook with copy-paste snippets: `design/MOTION.md` (distilled from `design/vendor/emil/skills/`). Every concept build passes stage 8 (motion gate) of `design/WORKFLOW.md`.

**Gate before animating (four questions, in order):** frequency (100+/day = no animation ever; tens/day = near-invisible; occasional = standard; rare = the delight budget) then purpose (feedback / spatial consistency / state indication / preventing jarring change / explanation; "looks cool" rejected) then speed (UI interactions under 300ms) then function (never move data the user is reading). Cap 5-7 deliberate motion moments per concept page.

**Motion tokens (paste into every `:root`, reference via variables):**
```css
--ease-out:cubic-bezier(.23,1,.32,1);       /* entrances, exits, press, hover */
--ease-in-out:cubic-bezier(.77,0,.175,1);   /* on-screen movement A to B */
--ease-drawer:cubic-bezier(.32,.72,0,1);    /* sheets and bottom bars */
--dur-press:140ms; --dur-pop:170ms; --dur-menu:220ms; --dur-panel:320ms; --dur-reveal:520ms;
```

**Rules:**
- **Motion must be motivated** — one-sentence justification per animation: hierarchy / storytelling / feedback / state transition. "It looked cool" = delete it.
- **Claimed = shown:** if MOTION_INTENSITY > 4, the page actually moves (hero entry, scroll reveals, hover physics). If you can't ship working motion, drop the dial to 3 and ship clean static. Never half-broken motion.
- Animate ONLY `transform` + `opacity`. Never top/left/width/height/margin/padding. Never `transition:all` — list exact properties.
- Easing: entrances/exits use `--ease-out`; on-screen movement/morph uses `--ease-in-out`; hover/color uses `--ease-out`; only loops and progress use linear. **`ease-in` is banned on UI** (it reads as sluggish).
- Durations: press 100-160ms; tooltips 125-200; menus/accordions 150-250; modals/sheets 200-500; scroll reveals/hero 400-700 (one-time marketing only).
- **Every pressable element gets `:active{transform:scale(.97)}`** (range .95-.98) with a 140-160ms transition. No exceptions.
- **Hover transforms are gated** behind `@media (hover:hover) and (pointer:fine)` — touch screens otherwise stick on a hover state.
- Entrances never start from `scale(0)` (nothing real appears from nothing): start at `translateY(18-24px)` or `scale(.92-.97)` plus opacity 0.
- Popovers/menus scale in FROM THEIR TRIGGER (`transform-origin` at the trigger); modals stay centered.
- **`window.addEventListener("scroll", ...)` is BANNED for reveal logic** — use IntersectionObserver (AMK standard `.rv` pattern is compliant), CSS scroll-driven animations, or a library's scroll API. Passive listeners OK for trivial nav-shadow toggles.
- `prefers-reduced-motion: reduce` means gentler, not zero: keep opacity/color transitions that aid comprehension, kill movement/loops/parallax (house block in `design/MOTION.md` §5).
- Marquee: **max ONE per page.** Infinite loops only where the section actively benefits (status, live feel); never every card.
- Stagger: **30-80ms per sibling** (house 60ms: `transition-delay:calc(var(--i)*60ms)`); never block interaction; cap staggered groups near 7 items.
- Rapidly-triggered elements (toggles, language switch, toasts) use CSS **transitions**, which retarget mid-flight, not keyframes, which restart; exits are faster than entrances.

- `backdrop-blur` ONLY on fixed/sticky elements (nav, overlays) — never on scrolling containers.
- Grain/noise overlays ONLY on fixed `pointer-events:none` pseudo-elements.
- Z-index: systemic scale only (nav 50-60, modals above), never 9999 spam.

**AMK proven vanilla patterns (single-file, no deps):**
- `.rv` reveal: IntersectionObserver threshold .12, `opacity:0 translateY(24px) → in`, unobserve after, data-d delay.
- Glass sticky nav: `backdrop-filter: blur(16px)` on sticky element, bg alpha .78 → .94 + shadow on scroll.
- Before/after drag slider: pointer events + `setPointerCapture`, clip wrapper by width%, inner img width = container width (JS-set on resize).
- Hero full-bleed feather: absolute img + dual `mask-image` (left fade + bottom fade, `mask-composite: intersect`).
- Ken Burns: `scale(1) → scale(1.06)` alternate 14s on hero/section photos.
- B&W strip hover colorize: `filter: grayscale(1)` → `grayscale(0)` .45s.
- Carousel (mobile): scroll-snap + arrow `scrollBy` buttons; grid on desktop.

**GSAP canonical patterns (when a real stack is used):** sticky-stack (pin each card, `start: "top top"`, scale 0.92/opacity .55 driven by NEXT card's trigger) and horizontal pan (pin wrapper, `end: "+=${distance}"`, scrub 1). Never mix GSAP + Motion + rAF loops in one tree.

---

## §10 IMAGES & ASSETS (AMK pipeline rules + source)

1. **Generate first.** If an image tool exists, use it for section-specific assets (hero, product shots, textures, portraits) at the correct aspect ratio. Never skip because CSS "feels faster".
2. Prompt discipline (from image-gen skills): art-direct the shot (subject, crop, light, tone, negative space), state "no watermarks, no logos, no text on clothing", name the palette ("cream and sage tones"), specify photorealistic/editorial quality.
3. **Watermark/logo scan (AMK lesson from OraCare v2):** generated and searched images can carry baked-in branding (clinic logos on coats, stock watermarks). READ every image before use; crop/split composites deliberately; re-generate with explicit exclusions when found.
4. Real images for real claims; generated for concept visuals. Photos get object-fit:cover + fixed aspect (4:5 portrait cards, 4:3 facility, 1:1 circles, 16:10 slider).
5. **Continuity rule:** all images in one concept share one brand world — same palette grade, same lighting family, same framing language. A viewer must read them as one site.
6. Captions below images, never pills on top (reference overrides allowed).
7. Social proof: real SVG logos (Simple Icons) or generated SVG marks — no plain-text wordmarks for invented brands. Logo wall = logos only, no category labels under them.
8. Mockup frames (device shots for previews): rounded-rect bezel + base/notch for laptop, rounded-rect + island for phone, blurred soft shadows, branded background (palette gradient + blobs + sparkles), one concept headline block. (OraCare mockup = reference implementation, `demos/shots/oracare-mockup.png`.)

---

## §11 CONTENT DENSITY & COPY SELF-AUDIT

- Default section shape: headline ≤ 8 words + sub ≤ 25 words + 1 visual or CTA. More must earn its place.
- No data-dump sections (20-row tables on a marketing page). Top 3-5 + "view full" link, or a different component.
- **Long lists (>5 items) need a different UI:** 2-col groups, card grid, tabs/accordion, scroll-snap pills, carousel, marquee. Not `<ul>` + divide-y.
- Spec sheets: never a 10-row hairline table. Use 2-col spec cards (name + big value + why-it-matters), scroll-snap pills, grouped clusters (one divider per cluster), or featured-3 + collapse.
- Quotes: **≤ 3 lines.** Cut the rest. Attribution = name + role/location.
- **COPY SELF-AUDIT (mandatory before ship):** re-read every visible string. Flag: grammatically broken, unclear referents, AI-hallucinated wordplay, "LLM trying to sound thoughtful" (fake humility, mock-poetic meta). Rewrite to plain functional sentences. Boring > broken.
- Fake numbers: only real data or explicitly labeled sample (AMK concepts mark prices/hours/reviews as samples — standing rule).

### §11b — SITE COPY LAW (added 17 Sep 2026, from the copywriting batch · see `research/YouTube-Lessons.md`)

**The three questions — apply to every headline, every claim, every section title (Harry Dry, [5]):**
1. **Can I visualize it?** Concrete beats abstract. If the reader can't see it, it isn't there yet. Zoom-in drill: write the abstract claim, then rewrite downward until you reach a concrete object or number.
2. **Can I falsify it?** A true-or-false claim is checkable — "Consultation 6 000 F", "Résultats reçus sur WhatsApp", "2 100 patients suivis". Unfalsifiable slogans ("l'excellence à votre service", "votre santé, notre priorité") are banned from heroes.
3. **Can nobody else say this?** If the clinic next door could paste the headline unchanged on their site, rewrite it. Use the client's own verified facts.

**Tests before ship (in addition to the §13 pre-flight):**
- **2-second test:** hero headline + sub must land in two seconds on a phone. Read it out loud to someone from the niche.
- **Competitor-sign test:** could this hero live on the competitor's site with just a logo swap? → rewrite.
- **Point, don't talk:** every claim sits next to its artifact — real photo, real number, real screenshot, price, hours, the WhatsApp button. Adjectives are not proof.

**Structure rules (from [1][2][4][6]):**
- **Hero names the business in plain language** + what to do (one CTA). Save the clever line for the section headline, never the hero (kicker/eyebrow carries the keyword; the hero carries plain meaning).
- **Claim → proof pairs:** make a bold claim, put the evidence immediately under it. Never a testimonial "wall of love"; drip **one real verbatim quote** at a time under the claim it supports (use the client's/FB's own words — the customer-language rule [4]).
- **Minimum one real verbatim human quote per concept** beside the numeric proof (follower counts / stars are not enough on their own).
- **Awareness split:** hero + first section speaks to someone who has never heard of them; the FAQ/accordion handles the technical buyer's questions (exact services, hours, payment, location).
- **CTA context:** never a bare button/link — the text around it says what they get. Repeat the same action top / middle / end.
- **Benefits translator:** feature → "…ce qui veut dire…" consequence, once each; short sentences; bullets for lists; no data dumps.
- **Banned words (EN/FR):** passion/passionné, révolutionnaire, dynamique, "solutions digitales" (as a benefit), "excellence" as a claim without a number; "best", "world-class", "state-of-the-art" — same rule in both languages.
- **Read-aloud test** on the whole hero + every CTA, in spoken (not translated) French.
- **Hero price anchor (King-approved 17 Sep):** price sits in the hero ONLY when price is the client's differentiator (a real, verified low price — YAKS consult). Otherwise the price moves next to the claim it proves, further down.
- **H1 contract:** the hero answers what it is / who it's for / why care + one CTA, above the fold, in plain words [10]. A landing page is an acquisition channel, not an art piece.

**SEO placement [6]:** long-tail keywords live in the **FAQ accordion** and in **kickers/eyebrows** — never squeezed into the conversion headline. Ticks/inline SVG for lists, not emoji clusters.

---

## §12 REDESIGN PROTOCOL (for AMK site iterations & client rebuilds)

**Detect mode first:** greenfield / redesign-preserve / redesign-overhaul. Ambiguous → ask once: "preserve the existing brand, or start visually from scratch?"

**Audit before touching:** brand tokens (colors, type, radii) · information architecture · content blocks (working vs filler) · patterns to preserve (signature interactions, copy voice) · patterns to retire (slop tells, broken layouts, dead links) · dial reading of the existing site (your starting point) · **SEO baseline (the #1 redesign risk: ranking pages, meta, structured data, slugs).**

**Preservation rules:** don't change IA unless asked; keep slugs/anchors/nav labels stable; brand colors stay brand colors; preserve copy voice unless rewrite requested; never regress a11y wins; never rename tracked elements (buttons/fields/IDs).

**Modernisation levers (priority order, stop when satisfied):**
1. Typography refresh (biggest lift, lowest risk)
2. Spacing & rhythm
3. Color recalibration (desaturate, unify neutrals, keep accent)
4. Motion layer
5. Hero & key-section recomposition
6. Full block replacement (last resort)

**Decision tree:** IA/content/SEO sound → targeted evolution (levers 1-4, ~70% value at ~40% risk). Structural visual debt → full redesign, strict content preservation. Brand itself changing → greenfield.

**Never change silently:** URL structure, primary nav labels, form field names/order, logo/wordmark, legal/consent copy.

---

## §13 AMK PRE-FLIGHT CHECKLIST (run before EVERY delivery)

**Mechanical (script where possible):**
- [ ] Bilingual: `data-en` count == `data-fr` count, and 0 elements with only one of the pair (DOM check)
- [ ] 0 broken images (naturalWidth > 0 on all `<img>`); 0 unresolved template tokens
- [ ] 0 console errors in headless Chromium (EN, FR, mobile 390) — **if the sandbox has no browser, write
      that the item was NOT run; never let an unchecked line read as passed**
- [ ] **First paint without JS:** no `opacity:0` / `visibility:hidden` entrance state outside an `html.js`
      gate set inline in `<head>`; reveal system in its own `<script>` with `try/catch`; hero + headings static
- [ ] **Every inline `<script>` compiles:** `python3 tools/qa/check_inline_js.py <file>` → rc 0 (rc 3 = control
      not rendered, say so)
- [ ] 0px horizontal overflow at 390px
- [ ] All WA/tel/mailto links → correct owner number/address; no dead `#` links
- [ ] Heading ≤ 2 lines desktop; nav 1 line ≤ 80px; hero CTAs visible at 800px height
- [ ] CTA contrast AA; no wrapped CTA labels; one label per intent
- [ ] Eyebrow count ≤ ceil(sections/3) (unless reference-driven)
- [ ] No 3+ consecutive same layout families; no zigzag ×3
- [ ] Em-dash scan: zero in EN strings (hyphen ok); FR permitted
- [ ] No filler verbs, no fake names, no unlabeled fake numbers
- [ ] Watermark/logo scan on every image asset (visual)
- [ ] Motion: IO-based (no scroll listeners), reduced-motion block present, claimed = shown; **0 `transition:all`; 0 entrance `ease-in`; every pressable has `:active` scale .95-.98 at 100-160ms; hover transforms gated by `(hover:hover) and (pointer:fine)`; no entrance from scale(0); UI motion ≤300ms (reveals ≤700ms); stagger 30-80ms; only transform/opacity animated; `design/MOTION.md` §6 sweep run**
- [ ] Shape lock + color lock + theme lock consistent page-wide
- [ ] Mobile collapse explicit per section; test at 390 AND 360 width
- [ ] `:focus-visible` branded 3px ring present on all controls; tab order matches visual order
- [ ] Reduced-motion: CSS block present AND JS honours it (count-ups/animations render final state — check, a CSS block alone fails this)
- [ ] JSON-LD `@graph` valid (Rich Results Test or local JSON parse); FAQ schema mirrors visible FAQs; zero fabricated ratings/hours; launch-only fields commented
- [ ] Decorative icons/emoji `aria-hidden="true"`; meaningful images carry descriptive alt; below-fold media `loading="lazy" decoding="async"`
- [ ] Cognitive load: ≤4 distinct options at any decision point; nav ≤5 top items; one primary action per section (Addendum #3/CRAFT-FLOOR §2)
- [ ] Squint test + 2 persona walks (parent abroad; anxious first-time patient/cost-conscious shopper) recorded in delivery notes
- [ ] C12 honesty: no claimed A/B test below ~1,000 pageviews/month; dated change-log entry instead (Addendum #4 §2)

**AMK standing additions:**
- [ ] Concept badge ("Website concept by AMK") present
- [ ] Sample-data labels on prices/hours/reviews where applicable
- [ ] 1280×800 hero shot captured → `demos/shots/<lead>-concept.png` (Concept Production Standard)
- [ ] Mockup (laptop+phone) captured when sending to a lead
- [ ] Single file, base64 embedded, opens on phone browser
- [ ] File size sanity (concepts ~1MB is acceptable)
- [ ] **Footer gate (§20.6):** 4 blocks + strip, footer CTA = hero action, labels name destinations, credit = brand text only

**If any box cannot be honestly ticked, it is not done. Fix before delivering.**

---

## §14 STYLE MENU (67 registry styles, one-liners + AMK mapping)

_Full specs: `design/vendor/bergside-skills/<slug>/` (SKILL.md + DESIGN.md). Token digest: `design/vendor/registry-digest.json`. AMK-curated per-vertical starter sheets: `design/STYLE-TOKENS.md`._

| Style | Character | AMK use |
|---|---|---|
| **premium** | Apple-like, precise spacing, refined | School/clinic concepts when no reference given |
| **clean** | Simplicity, whitespace, legible | Default fallback for any brief |
| **professional** | Polished, business-ready, structured | School concepts (bilingual, formal) |
| **corporate** | Brand-aligned, structured grids | AMK site sections |
| **refined** | Curated minimal, elegant serif accent | Premium school concepts |
| **minimal** | Stripped-back, whitespace, restrained | Editorial moments |
| **editorial** | Magazine layout, serif, structured | Storytelling sections (About/history) |
| **spacious** | Generous whitespace, consistent padding | Low-density luxury concepts |
| **bento** | Modular card grids, soft spacing | Feature/service showcases |
| **glassmorphism** | Frosted glass, blur, luminous borders | Sticky nav, overlays (used sparingly) |
| **cafe** | Warm tones, soft typography, cozy | Friendly clinic/nursery concepts |
| **terracotta** | Sun-baked clay tones, warm cream, editorial | Warm-premium ALTERNATIVE to Odentrics family |
| **friendly** | Rounded, approachable, whitespace | Nursery/kindergarten concepts |
| **contemporary** | Current-era minimal, bento, dark mode | AMK site refresh |
| **modern** | Editorial serif, minimal palette | Concept variety |
| **dramatic** | High-contrast theatrical, dark | Statement sections |
| **storytelling** | Narrative-driven, visual copy flow | "About the school/clinic" pages |
| **levels** | Conversion-focused, friction-removed | Landing funnels |
| **geometric** | Structured, neutral, precise | Technical/service grids |
| **flat** | 2D, vibrant, clean | Playful secondary palettes |
| **vibrant** | Lively, bold playful type, warm accents | Kids' activities sections |
| **colorful** | High-contrast palettes/gradients | Careful, on-brief only |
| **creative** | Playful, character-driven | Creative-studio leads (rare) |
| **expressive** | Vibrant, personality, bold graphics | Careful |
| **cosmic / futuristic / neon / matrix / pacman / sega / tetris / fantasy / fiction / pacman** | Dark-tech/arcade/game families | NOT for schools/clinics; keep as vocabulary |
| **brutalism / neobrutalism / bold / pulse** | Raw, heavy borders, vivid accents | Portfolio/experimental only |
| **material / ant / stitch / enterprise / roku / codex / claude / shadcn / agentic / lingo** | Real DS clones (Google/Ant/Carbon-adjacent/devtool) | Only if a brief names that system |
| **dithered / riso / sketch / doodle / vintage / retro / skeumorphism / neumorphism / claymorphism / paper / basic / mono / square / sleek / immersive / perspective / geometric / gradient** | Texture/niche families | Vocabulary for variety when a brief is unusual |

**AMK niche defaults:**
- **School (formal, bilingual):** professional or premium + editorial accents; palette rotation from §6.2 (never the previous project's family).
- **Nursery/kindergarten:** friendly + cafe warmth; rounded shapes; friendly photography.
- **Clinic (dental/medical):** premium or clean + trust cues; cream OR forest OR cobalt family (rotate); anxiety-defusing copy sections always.
- **AMK site:** contemporary/premium, navy+amber locked (brand), must demo mastery (bento + motion within MOTION 6).
- **TikTok/graphics:** bold or dramatic; single accent; big type; 1 message per frame.

---

## §15 IMAGE-GENERATION ART DIRECTION (for comps, mockups, reference boards)

**When the deliverable is IMAGES (not code):**

### Website comps
- **ONE image PER section** (never one tall page image). 8-section site = 8 horizontal images (16:9 or 16:10).
- **Hero composition bias:** left-text/right-image is the most overused pattern — not banned, but not the first instinct. Alternatives: centered over full-bleed image (text in lower 40%), bottom-left/right over image, top-left lead, stacked center, image-as-canvas, off-grid editorial, inverted classic, mini-minimalist.
- Hero rules: short powerful headline (5-10 words), concise support text, negative space, no pills/fake stats/badges clutter.
- Section rhythm: mix large art-directed sections with mini minimalist ones; vary density, alignment, image:text ratio, background intensity.
- **Continuity:** one brand world across all frames (palette, type, CTA family, radius language, photo grade, copy tone).
- Creativity escalation: push at least 3 of (composition / typography / scale contrast / hero concept / image treatment / section rhythm / framing / art-directed tension).
- Image-first: images are core material, including full-bleed backgrounds; several sections must meaningfully include imagery.
- **Anti-slop for image prompts:** no purple/blue AI glow, no blob spam, no glassmorphism-without-reason, no gradient headlines, no "luxury = beige serif", no fake-precision KPI columns, no "unleash/elevate/next-gen" copy in the comp, no Acme/NovaCore wordmarks, no identical card rows, no cloned left-text/right-image across sections, no infinity logo strips, no unreadable mosquito logos.

### Mobile screens
- Screen-first: generate app screens, not phone-shaped websites. Respect safe areas (status bar/home indicator regions), real navigation logic (tab bar / bottom sheet), touch-scale type (readable at 1x).
- Enough screens: generate the full flow (onboarding → home → detail), not one pretty screen + filler.
- Multi-screen consistency: one design system across the set (same palette, components, corner language, icon set).
- Mockup framing: subtle premium phone frame with visible bezel; frame serves the content, never dominates; even margins.
- Anti-tells: no purple-blue fintech gradients, no fake chart spam, no cloned screens, no pill/badge overload, no "elevate your life" copy, no device frames dominating.

### Brand kits
- Board = visual argument (what the brand represents / core metaphor / how the logo expresses it / how it scales / why it's ownable).
- Default 3×3 (4:3 or 16:10): Logo cover · Logo construction · Digital application · Brand essence (one tagline) · Color system · Typography · Physical application · Image direction · System detail.
- Rhythm: quiet / functional / emotional / technical / atmospheric / detailed — not every panel equally loud.
- Logo concept methods: monogram+meaning, product action, metaphor fusion, negative space, construction geometry.
- Style DNA: dark charcoal outer canvas or paper, grid presentation, strong gutters, sparse type, one strong accent, texture (halftone/grain) for print feel.

---

## §16 ANTI-LAZINESS (execution discipline, from the taste-skill research)

Research finding: output truncation is a **deliberate RLHF brevity bias, not a decoding failure** — models choose short outputs; multi-part instructions get sections silently dropped; explicit length requirements get undershot. Implications for how WE work:

1. **Full-output enforcement:** partial output = broken output. If the task is N files/sections, deliver all N. BANNED patterns: `// ...`, `// rest of code`, `// TODO`, `// similar to above`, "the rest follows the same pattern", "I'll leave that as an exercise", skeletons when full code was asked.
2. **Scope lock:** read the full request, COUNT distinct deliverables, lock the number, build all of them, cross-check count before responding.
3. **Verification loops:** re-read output against the request (chain-of-verification). For code: run it / render it / assert (our playwright + grep checks ARE this loop — keep running them every delivery).
4. **Chunked execution for long work:** write at full quality up to a clean breakpoint, then `[PAUSED — X of Y complete. Resume from: <section>]`, and resume exactly there with no recap.
5. **Explicit syntax binding:** when a format matters (EN|FR pairs, JSON payload shape, section order), state the exact format in the plan AND assert it mechanically afterward.
6. **Self-grading:** score the deliverable against the pre-flight checklist before presenting; fix, don't apologize.
7. Seasonal note: measured output-length dip around December — irrelevant to us except as a reminder: verify, don't assume.

---

## §17 PATTERN VOCABULARY (names to know & reach for)

**Naming matters (§19.5):** use these exact words when briefing a human or an AI. Precision beats "make it beautiful".

**Heroes:** asymmetric split · editorial manifesto · media-mask · kinetic-type · curtain-reveal · scroll-pinned · image-as-canvas · mini-minimalist.
**Nav:** floating glass pill · magnification dock · mega-menu reveal · contextual radial.
**Layout:** bento (exact cell count) · masonry · split-screen scroll · sticky-stack · chroma grid.
**Cards:** parallax tilt · spotlight border · glass panel (inner refraction) · morphing modal.
**Scroll:** sticky stack · horizontal hijack · zoom parallax · progress path · SVG line-draw.
**Micro:** magnetic button (motion values, never state) · particle-success CTA · skeleton shimmer · directional hover fill · ripple.
**Type:** kinetic marquee (max 1/page) · text-mask reveal · text scramble · circular text path.
**Libraries:** CSS/IO for single-file (AMK standard) · Motion (motion/react) for React UI · GSAP+ScrollTrigger for scrolltelling · never mix GSAP+Motion+rAF in one tree.

---

## §18 SPEC-DRIVEN BUILD & VERIFICATION (added 17 Sep 2026, engineering batch [9] — `research/YouTube-Lessons.md`)

*The rule that makes everything else hold: **AI builds decay by default** — every feature added without discipline makes the next one harder. Discipline is not a better prompt; it's plan → decide → build → verify → debug.*

### 18.1 Plan before build (never a wish)
- Every concept/client build starts from a **one-page spec in the dossier**: who it's for · what's in v1 · what is explicitly OUT · build order · what depends on what. Changing a line in a plan is free; changing a decision already spread across the code is a rewrite (this is our builder-replacement bug class).
- **Scope never touches the stack**: decide *what* we're building first, *how* (fonts, palette derivation, sections) second, so a plan doesn't rot when a detail changes.
- **Value provenance check (mandatory, pre-ship):** for every number, price, hour, count or status a page shows, name the source — research file, real price, or the explicit DEMO/sample label. **Any value with no source is a decision nobody made** → stop, decide, source it or remove it. This is the mechanical trigger for the accuracy law and §3.6's fake-number ban.

### 18.2 Decisions written down, on purpose
- Defaults that hold unless there's a reason: **single file, base64 embedded, no external requests; mobile-first; EN|FR pairs complete; WhatsApp-first CTAs.**
- Every non-obvious design choice gets one line in the build notes with the **honest alternative and why it lost** (e.g. "sticky WA bar — alternative: fixed footer nav, rejected: competes with language toggle").
- **Secrets/keys never in code** (this repo is public).

### 18.3 State lives in files, not in chats
- The build must be reproducible from the repo: builder script + inputs + dossier + QA notes. A future session (or another AI) reads the files and continues — nobody re-explains the project.
- Our context files: `sales/Pipeline-Status.md` (state), the prospect dossiers (decisions), `hosting/previews/README.md` (deploy map), session memory (continuity). **Update them at the moment of the decision, not at the end of the day.**
- Never overwrite human-written notes; add alongside and flag conflicts.

### 18.4 The verification ladder (match effort to risk)
*"It works" is a lie until verified — green checks only prove what we thought to check.*
- **Marketing concepts (reputation risk):** builder greps (leftovers, numbers, URL, phone) · `node --check` on the JS · DOM pair counts · JSON parse · served over HTTP locally · **mobile click-through: every WA / tel / mailto / CTA opened on a real phone (King's phone QA)** · hero shot + mockup captured.
- **Client deliverables (money risk): run all four jobs:**
  1. **Check/verify** — drive the actual flows (book, submit, language toggle, sticky bar), against the spec's criteria, not against the code.
  2. **Test** — what a real caller depends on: correct number reaches a real WhatsApp, form saves/sends, both languages complete.
  3. **Review** — a fresh pass over the built output, by different eyes than the builder (King's phone pass on the live URL counts as the second pair of eyes; never self-approve from the same pass that wrote it).
  4. **Document** — the change log written from the actual diff, not from memory.
- **Deploy gate:** the live URL is verified on a phone (FR boot, one prefill, one CTA) **before** the link goes to a prospect — the YAKS sequence is the standard.

### 18.5 Debug discipline (no pattern-match fixes)
1. **Reproduce reliably first** — a bug you can't reproduce on command is a bug you can't prove you fixed.
2. Narrow to the smallest failing spot.
3. **Form ONE theory, test that one thing.** If wrong, discard the change — no dead edits left in the file.
4. Fix the **cause**, not the symptom; then hunt the same mistake elsewhere.
5. **Add a regression check** that fails without the fix (grep/assert in the QA script) so it can never quietly come back.
6. If the "bug" is a bad decision, say so and redesign — don't patch over it.

---

## §19 DESIGN FOUNDATIONS & DIRECTION EXPLORATION (added 17 Sep 2026, design batch [11][12][13][14] — `research/YouTube-Lessons.md`)

*The four design videos agree on one thing: execution is now cheap, so the differentiator is taste, the decisions. This section is the base layer that produces those decisions.*

### 19.1 Less design, conversion first
- **Design for the visitor, not for yourself, not for the client.** [12] A clean, modern redesign once dropped a client's sales because it was pretty instead of converting. Beauty in service of conversion is the goal.
- **Start from the key functionality, not the chrome.** [11] Don't begin at the header, the nav, or "how many sections do I need". Ask: what is the one thing a visitor must do here? Design that unit first (for many pages: heading + form/CTA + button). If that is all the page needed, ship that.
- **The three conversion jobs** [12]: **clarity** (who we are, what to do next, why care), **scannability** (they scan, they don't read), **motivation** (speak to what makes them say yes).
- **Foundation before furniture** [11]: one spacing scale (values divisible by 4, rem = px/16, CSS variables), 1-2 font choices, two button types (primary/secondary), one accent. The system exists so no value gets re-decided.
- **Spacing-first method** [11]: start generous (e.g. a 40px rhythm), then bring related elements closer, picking from the scale, never nudging pixels by feel. Elements need more space than feels right when you're zoomed into one component; users scan the whole UI first.

### 19.2 Visual hierarchy — the method
- The most important element is the **biggest and boldest**; everything else has its volume turned down [12]. A CTA must be the highest-contrast object in its viewport.
- **Emphasise by de-emphasising** [11]: when the key element still doesn't win, reduce the contrast/weight/size of its competitors instead of inflating the hero further. Start with the smallest change that works; the most elegant pages use one strong contrast, not five loud ones.
- **Zoom-out test** after each section: squint, or zoom to 25%. If the eye doesn't land on the primary element first, fix the hierarchy before adding anything.
- **F-pattern / Z-pattern dogma: retired.** [12] People engage in many patterns; hierarchy, not a mandated reading path, does the work.

### 19.3 Direction exploration (mandatory before any build, 30-45 min)
*From [13], reinforced by [14]: explore directions before building; the winner becomes the token sheet.*
1. **Write the brief line**: audience + the one action + tone.
2. **Produce exactly 3 directions** (no more), each with its own type pairing and accent: e.g. blueprint/technical · editorial/broadsheet · warm/minimal. Never accept the first output; never accept a default palette.
3. **State the avoid-list** (paste into any tool): purple/violet gradients · neon glow · emoji iconography · AI sparkles · overly-rounded "AI" UI · cheap stock 3D renders · content-hiding fade-ins · Instrument Serif (now an AI-slop tell [13], already banned in §3.2).
4. **Judge with §19.2 + the §3.8 tell list**; pick one; then iterate **variants of the winner only** (font pairing, accent, headline tone).
5. **Headlines are outcome-led, not product-led** [13]: "For organic traffic you can actually defend" becomes "Ship SEO work that measurably moves the needle". Same law as the H1 contract (§11b).
6. **Lock the token sheet** (`design/STYLE-TOKENS.md`) from the winner; that sheet is our version of the "design system file" [13].
7. **Then** build the full page from it. Pipeline hook: `design/WORKFLOW.md` stage 3b.

### 19.4 The inspiration process (creativity is a process, not a moment) [11]
- **Know the basics, collect references, work them over in your head, step away, come back, test with others, ship something.**
- Reference sources: real sites in or adjacent to the vertical, Figma community, pattern libraries, and our vendored registries (`design/vendor/*`). Study *why* a layout works (what it does, for whom) before borrowing anything.
- **Don't fall in love with your own work** [11]: show it to someone who will say it is bad, test it on a phone, adjust. Some outputs only teach you what the next one should be. A finished average page teaches more than a perfect plan.

### 19.5 Design vocabulary beats "beautiful" [14]
- "Make it beautiful" is subjective, and the model resolves it to purple gradients. Name the decisions instead: **layout** (hero / feature / onboarding · card / list / bento · full-screen vs framed), **style** (flat, outline, minimalist, glass, soft-depth), **mode** (light/dark), **accent** (one hue, and where it is allowed), **type** (sans/serif/mono · light vs bold personality · pairing), **motion** (fade/slide/scale/blur · sequenced · ease-in-out).
- **Reference-driven work**: point at a real reference (the client's own storefront/logo, a real site, a Figma frame, our vendored registries) and build *from* it; the taste is inherited instead of guessed.
- **The "one ingredient" rule** [14]: a single well-chosen element (a real photo treatment, one geometric mark, a product mock) lifts a page more than ten generic effects. *Our constraint:* single-file, no external requests; any ingredient must be embeddable (CSS/SVG/canvas). External 3D/blob embeds are parked for the AMK main site only.
- **Taste is the moat** [14]: as every site converges on the same blocks, the decisions are the differentiator. Build for the result, not the template.

---

## §20 FOOTERS — THE LAST SCREEN (added 17 Sep 2026, footer batch [18][19] — `research/YouTube-Lessons.md`)

*Two videos, one message: the footer is a **conversion + trust surface**, not a legal dump. Generic advice below is filtered through our rules — mobile-first, single-file, WhatsApp-first, no fabricated proof.*

### 20.1 What a footer is for [18]
- Two jobs only: **doormat navigation** — the last-chance index for what the nav dropped (contact, hours, address, rarely-needed pages) — and a **second chance to convert**: whoever reached the bottom is interested, so give them the action again.
- A footer is **mandatory**. "Too minimal for a footer" costs UX, conversions and SEO signals.

### 20.2 AMK footer anatomy — 4 blocks + strip (every concept)
1. **Brand + line** — logo lockup + **one sentence** (who you are, what you do). [18] says 2–3 paragraphs; too heavy for our single-page mobile builds → one sentence, always present.
2. **Doormat nav** — the page's own sections, labelled with the destination, never "Ressources"/"Infos" [18].
3. **CTA block** — **the same primary action as the hero** (WhatsApp first, phone second). Framer/Figma repeat the hero CTA in the footer [19]; small landing pages benefit most. Never a second, competing action.
4. **Contact block** — address + landmark if we have one, hours, phone(s)/WhatsApp. This is the **E-A-T cluster** [18] and exactly what a patient needs at 22:00.
- **Bottom strip:** copyright · AMK concept/preview disclaimer · privacy note — small, low-contrast (legal *fades*, hierarchy [19]) + a **back-to-top** link [19].
- Mobile order: brand → CTA → contact → nav → strip (action before index). Desktop: 4 columns with column titles so the eye orients instantly [19].

### 20.3 Space & hierarchy [19]
- The footer is a **designed screen**, never leftover: generous negative space, and **one scale contrast** — a large brand/wordmark (or one large element), a medium one (photo/motif), small body/legal type.
- Negative space is the **canvas** where personality goes [19] — but §3 still governs: no decorative versions, no fake live counters, no ghost chrome.
- **Mobile caveat (AMK):** full-viewport footers are a **desktop-only** move; on mobile the footer is bounded (≈ ≤120px of designed content + strip) because scroll cost beats drama.
- Carry the build's **one ingredient** into the footer (the client's real photo, the drawn motif, the letterform) — motif continuity, no new assets [19].

### 20.4 Copy & proof in the footer
- Link labels name the destination, in the client's own vocabulary [18].
- **No fabricated proof.** Awards, press quotes and review rows go in a footer **only if they are real and permissioned** (accuracy law). No proof yet → leave the slot empty; never fill it with decoration.
- **AMK credit line = plain brand text**: "Site par AMK — Développement Web & Solutions Digitales". A keyword anchor ("développeur web Douala") is flagged as black-hat SEO [18]; on client sites the credit stays **text only** until the client agrees to a link.

### 20.5 Bans & parked [18][19]
- **Banned in footers:** hidden/faded anchor text (named black-hat, Google's own guidelines); keyword-anchor backlinks; vague labels ("Resources"); version footers / fake-live strips (§3.1); external widget embeds.
- **Parked:** Instagram/Facebook feed embeds (external request + speed cost; our clients don't post consistently enough to use as proof) · newsletter signup forms (our channel is WhatsApp; no list to manage yet) · full-viewport mobile footer (desktop-only) · mega multi-column footers on 1-page concepts.
- **Contextual footers** (footer varies by page / by condition) [18]: parked until a genuinely multi-page build (school admissions, lab results portal) — note it in the build notes when it's used.

### 20.6 Footer gate (add to §13)
- [ ] 4 blocks present (brand+line · doormat nav · CTA · contact) + bottom strip (© · disclaimer · back-to-top)
- [ ] Footer CTA = the hero's action, not a second offer
- [ ] Every label names its destination; nothing hidden or faded
- [ ] Credit line = brand text only
- [ ] Footer contrast passes the audit gate (§1b) on desktop **and** mobile

### 20.7 The link card — what the prospect sees BEFORE the page (added 18 Sep 2026)

The first thing a prospect sees is **not the page: it is the WhatsApp link preview.** A concept
link with no `og:image` renders as a grey text card — it looks like a forwarded link, not like
work. The UNI-LABO concept (18/09) shipped **without `og:image`** and the preview came out as a
text card. The page was fine; the first impression was weaker than the page deserved.

Every concept link sent on WhatsApp must carry, in `<head>`:
- [ ] `og:title` — the business name + what it does, ≤ 60 chars
- [ ] `og:description` — one line a patient would recognise, ≤ 120 chars
- [ ] **`og:image` — 1200×630, a real screenshot of the built page, absolute URL** (the deploy URL,
      not a relative path: WhatsApp does not resolve relative URLs)
- [ ] `og:type` = `website`, `og:locale` = `fr_FR` (+ `og:locale:alternate` = `en_US` when FR|EN)

`og:image` must be an absolute `https://` URL on the deployed host, so it is added **after** the
first deploy — or the host must be known in advance. Where a project has no image host, use the
concept's hero screenshot from `tools/video/capture.mjs --mode hero` (1080×1620 → crop to 1200×630).

### 20.8 Bilingual text lives in THREE places — patch all three (added 19 Sep 2026)

On every EN|FR build the same sentence exists in **three** places, and they must always agree:

1. `data-en="…"` — what the language toggle writes
2. `data-fr="…"` — what the language toggle writes
3. **the visible text node between the tags** — what the page shows *before* JavaScript runs, and
   **what Google and every LLM crawler actually read.** `fetch_page`, PageSpeed and any no-JS reader
   never call `setLang()`.

**Found on 19 Sep while diagnosing AMK's own site:** the FAQ answer *"What happens after launch?"* had been updated in
`data-en` and `data-fr` but **not in the text node**. The page looked right in a browser and was wrong to every
crawler. It very nearly made me misdiagnose a deployment (I read the stale node on the live site and concluded the
deploy was old — the deploy *was* old, but the same string existed in both versions, so that one string proved nothing).

- [ ] After editing any bilingual string, grep the file for the **old** wording — it must return **zero** hits, in all three places
- [ ] `audit_html.py` counts text runs but does **not** compare the three sources: this check is manual, or a 3-line script

### 15.bis Images: generate FIRST, never ship a text-only page (reinforced 19 Sep 2026)

**King's correction, 19 Sep:** *« why is there no image on their site, look for more inspiration (focus on clinics
of the same type) online joined with our design documentations and give me something with images »*.

**He is right, and our own library already said so twice — §15 point 3 (« NO pure-text minimalism — even minimal
sites need 2-3 real images ») and §15 point 1 (« Generate first. If an image tool exists, use it… Never skip
because CSS "feels faster" »).** The Bonanjo page had zero images because I built it before reading §15, not
because the tools were missing. **A delivered page with no photograph is an unfinished page.**

**What the 2026 healthcare-web research adds (sources: sitebuilderreport, ueni, reallygooddesigns, digitalsilk):**
- **« Clinical-sterile aesthetics lose patients to warm-and-modern ones at the same price point. »** The hero image must be *calming* — a real practitioner portrait or a warm caregiver–patient moment. **Never a stethoscope on white.**
- The hero is seen for about **6 seconds** — it sets the emotional state before a word is read.
- Non-negotiable stack stays: book-now above the fold, click-to-call on mobile, named specialties.
- Neuro clinics specifically win with **clear hero message + organised service sections + a visible consultation CTA**.

**The AMK image recipe (applies to every client page from now on):**
1. **One image per section** — never one tall page image (§15).
2. **Generate first**, at the right aspect ratio (16:10 hero, 4:3 sections), before writing CSS.
3. **Prompt discipline:** art-direct it (subject, crop, light), name the palette, and **explicitly exclude text,
   logos, signage, writing on clothing and watermarks** — then **read every image back** (the OraCare v2 rule).
4. **Continuity:** all images in one page share one light family and one palette grade, so they read as one site.
5. **Honesty:** when the people are models, **say so under the image** — *« Mise en situation. La photo définitive
   sera prise dans votre centre. »* It is also the sentence that invites the client to supply his own photos.
6. **Weight:** never base64 five photographs into a single file. **Separate files load in parallel**; a 750 KB
   base64 page is a slow page on 3G, which is exactly the market we sell to.

### 20.11 A `<details>` has ONE summary — never put a language class on it (added 19 Sep 2026)

**Found by King on 19 Sep, on Labiomed:** *« FAQ (Questions) do not appear in the English version »*.
The accordion rows were **completely blank in English** — and **also on Bonanjo, which was already live.**

**The cause.** I wrote:

```html
<details>
  <summary class="fr-only">Faut-il prendre rendez-vous ?</summary>
  <summary class="en-only">Do I need an appointment?</summary>
  ...
</details>
```

**HTML recognises only the FIRST `<summary>` as the disclosure control.** In English the first one is hidden,
so the control is empty — and the whole FAQ looks broken to an English reader. Every one of my other builds
used the correct pattern, which is why **only the two pages written in the last two days were affected.**

**The correct pattern — the one already shipped and validated everywhere else:**

```html
<details>
  <summary><span class="fr-only">…</span><span class="en-only">…</span></summary>
  <p><span class="fr-only">…</span><span class="en-only">…</span></p>
</details>
```

**The rule, and it generalises past `<details>`:** a language class may only sit on an element whose
**text** is bilingual — **never on an element whose BEHAVIOUR is structural** (`<summary>`, `<option>`,
`<title>`, `<legend>`, `<caption>`). Wrapping a `<span>` is always safe; wrapping the functional element is not.

**Repaired with `tools/site/fix_details_summary.py`** (idempotent, and it re-checks that no `<details>`
has more than one `<summary>`). Both pages verified **in a real browser, in English: 9 questions visible, all opening**.
**No browser test had ever opened the FAQ in the second language — that is the gap that let this through.**

### 20.9 `display:revert !important` beats every other `display` (added 19 Sep 2026)

Our bilingual pattern hides one language with `html[data-lang="fr"] .en-only{display:none !important}` and shows the
other with `display:revert !important`. **`revert` sends the element back to the user-agent default — not to your CSS.**
So a `<small class="fr-only">` that you styled `display:block` becomes **`inline`** again, and the layout breaks
silently in one language only.

**Found on the Bonanjo build (19 Sep):** the site name ran into its subtitle in the header — the `.brand small{display:block}`
rule was being overridden by the language rule.

- **Rule:** never put `fr-only`/`en-only` on an element whose layout depends on `display`. **Wrap it instead** — the
  language class goes on an inner span, the layout stays on the untouched parent.
- Or omit the language class entirely when the string is identical in both languages (a proper noun often is).

### 20.10 `display:revert !important` — the other half of the bilingual trap
See §20.8 for the three places a bilingual string lives; §20.9 is the layout half of the same pattern. Both come from
the same mechanism, and both fail silently in one language only. **Test every build in BOTH languages before shipping.**

**King's ruling, 17 Sep 2026:** the §20 footer standard **applies to every NEW build**. The concepts already built (opticien, afriquelabo, labethanie, yaks, skye, oracare, clinic-bonaberi) **stay exactly as they are — no retrofit.** First build under this rule: the JEMPO concept (next prospect).

---

## §21 TALKING PAGES — VOICE ON AN AMK BUILD (added 18 Sep 2026, build batch [20] — `research/YouTube-Lessons.md`)

**Origin:** Pavlo, *"How I sell Talking Websites to local businesses for 499/mo"* — voice AI embedded in a page that answers questions and books appointments; sold as **recurring revenue**, not as a delivered file. The concept is right and we are already halfway there: **OraCare v1/v3 already ship a scripted assistant** whose answers come only from the page's verified facts.

### 21.1 The rule that governs everything below

**Voice is an addition, never the only way to reach the business.** The primary action of every AMK build stays a plain `wa.me` link — it works on every phone, every browser, costs nothing, and needs no permission. A voice button sits *next to* it. If the voice layer fails, the page is still complete.

### 21.2 What the browser can actually do (verified 18 Sep 2026, not assumed)

| | Speech **out** (synthesis) | Speech **in** (recognition) |
|---|---|---|
| Chrome desktop | Full (33+) | Full (33+) |
| Chrome **Android** | Full | **Partial** — the only mobile browser that works at all |
| Safari / iOS | Full (7+) | Partial (14.5+), inconsistent |
| **Firefox (all platforms)** | Desktop only | **Not supported, ever** |
| Samsung Internet | Full (5.0+) | Via the Chromium engine |

- **Cost: free, no API key** — the browser vendor runs it (Google for Chrome).
- **Recognition requires a network connection** and **sends the audio to that vendor's servers.** Synthesis is local.
- Newer Chrome builds have begun shipping **on-device recognition** (Chrome 139+, reported Aug 2026) — promising, **not verified on our own devices yet**.
- Cloud voice APIs ($0.006–0.024/min, far better accuracy and custom vocabulary) exist for when a client pays for production quality. They need a key + a backend, so they are **not** our default.

**⚠️ The one thing no source can tell us:** accuracy of recognition on **Cameroonian English and French accents**, in a real room, on a real phone, on mobile data. That is an empirical question and it can only be answered by a test on King's own device. **Do not promise a client a voice feature before that test exists.**

### 21.3 The implementation ladder (cheapest first — do not skip a tier)

**Tier 0 — voice on the scripted assistant. Free. No backend. No account. Ships in an hour.**

> ### ✅ BUILT & TESTED — 18 Sep 2026, on our own site (`site/index.html`)
> King ruled: *« on teste sur le site de AMK »* — our own page, so the worst case is a bug found by us.
> **`tools/site/patch_voice_widget.py`** injects the layer (idempotent), **`tools/qa/test_voice_widget.mjs`** verifies it
> headless (**24/24 checks pass**), both committed. `audit_html.py` = **0 findings** with the widget in, desktop and mobile.
>
> What it answers, traced to lines already on the page: price 100,000 FCFA · free preview · 3–5 days · **monthly 15,000 FCFA
> (2 updates/month, no contract, domain stays yours)** · bilingual included · what's in the package · staff can update it ·
> local Google search · ownership · how to start. Anything else → **"I do not know that one"** + WhatsApp.
>
> **Two bugs the test caught that review would have missed:** equal KB scores let a vague question ("et après ?") win over
> the right answer → scoring rewritten (phrase match 4+, word 2+n/4, tie-break on number of hits, threshold 3);
> and "launch/lancement" in the *delay* keywords stole the *after-launch* question → overlap removed.
> **Mobile:** the labelled FAB covered a hero CTA → icon-only 54 px pill above the sticky bar, plus a 3-pulse halo
> (disabled under `prefers-reduced-motion`). The ✕ glyph is an **SVG**, not `&#10005;` — the glyph was missing from the font.
>
> **Still not verified, and stated as such:** microphone accuracy on a Cameroonian accent. That is King's phone test.
> Speech *input* needs Chrome/Edge; the chips and the WhatsApp handoff work in every browser regardless.
We already write the answers (FAQ, preparation rules, hours, directions, price→WhatsApp). A Tier-0 voice layer is: `SpeechRecognition` for the patient's question → match it against the **existing scripted knowledge base** → `speechSynthesis` reads the answer in the site's current language → if the question isn't in the base, it says so honestly and opens WhatsApp. **This is the tier UNI-LABO's "Avant de venir" section is already written for** — "Est-ce que je dois être à jeun ?" is the single most valuable voice question a lab will ever be asked.

**Tier 1 — a real AI answer, small backend. Needs an API key + a serverless function.**
An LLM grounded in the same knowledge base. Cost per conversation is small but real, and it breaks the single-file rule (the page now talks to an endpoint we run). Not before a client is paying.

**Tier 2 — the video's model (Retell / Vapi / ElevenLabs / GoHighLevel-class agent).** USD-billed, per-minute, foreign card required. **Parked, not rejected** — revisit only when a client explicitly pays for that service.

### 21.4 Answers must be traceable to the page

**Every spoken answer must be a line that already exists on that site, written from a verified fact.** No improvisation, no invented services, no invented prices, no invented turnaround times. The video's own demo fails this test — its AI invents "control joints, reinforcements and curing methods" for a company whose real services nobody checked. If a patient asks something the page doesn't answer, the assistant says **"je ne sais pas — demandez au laboratoire"** and hands off to WhatsApp. *An honest "I don't know" builds more trust than a fluent guess — and a wrong answer about a medical test is not a marketing error, it is a safety error.*

### 21.5 The handoff is the conversion, not the booking

In this market nobody fills a calendar. The assistant's job is to end with **WhatsApp open, the patient's own question pre-filled** — the same `wa.me?text=` mechanic we already ship, except the text is now written from what the patient actually said. That is our equivalent of the video's "books the appointment automatically", and it is measurable.

### 21.6 Gate — a voice layer may ship to a client only when all of these are true

- [ ] The plain WhatsApp button is still there, above or beside it, and works without the voice layer
- [ ] **Explicit click to start** the microphone — never autoplay, never listen on page load
- [ ] A visible line saying the voice is a demo/assistant and that speech recognition uses the browser's service (no silent recording)
- [ ] Language follows the site's FR|EN switch; the answer is spoken in the language the question was asked in
- [ ] Every answer traceable to a line on the page (§21.4); unknown → honest fallback → WhatsApp
- [ ] **`audit_html.py` 0 findings** with the voice UI included, desktop **and** mobile
- [ ] Tested on a real Android phone, on mobile data, with an accented question, before any client sees it

### 21.7 What is permanently banned (from this same video)

- **AI-generated photos presented as the real team, the real owner, or real completed work.** Never. Not for a concept, not for a client. The legitimate use of image generation is a mockup **of the site** — never a fabrication **of their reality**.
- Quoting the "2–3 % average website conversion" figure to a prospect — unverifiable here; internal calibration only.
- Exit-intent pop-ups and auto-rotating review widgets as *defaults* on a mobile-first Cameroonian page.

---

## §22 INTERACTION CONTRACT, INVISIBLE TIMELINE, PSYCHOLOGY LAYER — 4 videos (23 Sep 2026)

Folded from four videos King dropped in one go (UX/UI + design psychology). Verdicts, junk filter and
the full log: `research/YouTube-Lessons.md` **Lot [23]**. §22 is the build-side law that came out of them.

**The four, and what each one is for:**

| # | Video | What we took | What we left |
|---|---|---|---|
| 22.a | Amir Moradi — *What I Wish I Knew Before 10 Years in UX (The 3 Levels)* | the three levels; the invisible timeline; "happy path only = dreamer" | career-path advice |
| 22.b | Kole Jain — *Every UI/UX Concept Explained in Under 10 Minutes* | the interaction contract: 4 states per button, a response per interaction, numbers that are checkable | generic tutorial framing |
| 22.c | uxpeak — *The UX Psychology Behind Apps People Can't Stop Using* | 6 principles — the honest half only | dark patterns, streak/guilt mechanics, fake progress |
| 22.d | Self-Made Web Designer — *The Psychology of a PERFECT Website* | 3 friends, mental models, MAYA, chunking, price ladders | nothing structural; the tone is a hook |

### 22.1 The three levels (22.a) — and the one we kept failing

**Surface** — UI is not UX. *"Screens, AI can do. Designing decisions, that is the job."* Our concepts are not
screens: every section has to answer a question the visitor actually has (hours? price? can I trust this?)
before it is allowed to be pretty.

**Timeline** — *the hardest part of delivery is the waiting*. State the state; show the progress; a happy-path-only
build is a dream. **This is where we were failing, and where the worst bug of the quarter was born:** the
Cristallin page carried a WhatsApp link with no country code (`wa.me/699905577`), on a page already in the
client's hands, and **nobody had clicked it**. Two people had "reviewed" the page. A path nobody has walked
is not a design, it is a hope.

**Strategy** — business × technology × psychology; *everything holds except the human*. The other three
principles in this file are the technology; 22.3 is the psychology; the business is the price and the
perimeter (see `sales/`).

### 22.2 The interaction contract (22.b) — non-negotiable per page

1. **Four states per button, always** — default, hover, active, disabled — plus **loading** where the action
   waits on something. Our house set, copied straight from the Cristallin build:
   `.btn{transition:...}` · `.btn:hover{translateY(-1px)}` · `.btn:active{transform:scale(.97)}` ·
   `.btn.is-off{opacity:.55;cursor:not-allowed;pointer-events:none}` · `:focus-visible{outline:3px}`.
2. **Every interaction produces a response.** Not a spinner for show: *words*. Our pattern is the
   **`.said` band** — after a click that leaves the page (WhatsApp, `tel:`), the page says, in the visitor's
   language, **what just opened and what happens next** ("WhatsApp opens with your request already written.
   The practice answers during opening hours."), then hides itself after 6 s. Implemented with
   `role="status" aria-live="polite"` so it is heard, not only seen.
3. **Never a visible control with no effect.** `href="#"`, a dead button, a form with no state — a false
   signifier; the visitor reads the whole page as broken.
4. **Every path out of the page is checkable and complete**: `wa.me/237…` (country code, digits only, no
   spaces), `tel:+237…`. Both are now **blocking** checks in `tools/qa/audit_page.py`.
5. **Numbers from the video that we hold ourselves to**: one type family; ≤6 sizes per page (see the caveat
   in 22.6); icons at line height (24 px); padding ≈ 2× the button height; **shadows at low opacity with a
   large blur — if the shadow is the first thing you notice, it is wrong**; dark mode = card lighter than the
   background, *lower* saturation; overlays carry a gradient under the text so the words stay legible.
6. **State where the user is**: focus rings on every field (`:focus`), an error state that says *why*, and a
   confirmation micro-interaction after an action (the video's "Copied" chip). Our equivalent today is the
   `.said` band; a copy-to-clipboard chip is the next one to build.

### 22.3 The psychology layer (22.c, 22.d) — used honestly, or not at all

The six principles are real, and **every one of them has an honest form and a dishonest form**. We ship the
honest form only; the dishonest ones are named in `research/YouTube-Lessons.md` §5.

| Principle | The dishonest form | Our legitimate form |
|---|---|---|
| **Smart defaults** (70–90 % never change the default) | a pre-ticked paid extra | **the WhatsApp message arrives pre-written** in the visitor's language; the default is the action they already wanted |
| **Goal gradient** (a card with 2 of 10 stamps pre-filled ≈ ×2 completion) | fake progress bars | **the preview is already built** before anything is asked: they start at "almost there", because it is true |
| **Reciprocity** (value before the ask — Cialdini) | "free" behind a signup wall | the concept page itself, sent with **no account, no form, no deposit** |
| **IKEA / endowment** (people value what they helped build) | labour disguised as a game | they choose the 6 points, the photos, the perimeter — the page becomes *theirs* before the invoice |
| **Loss aversion** (a loss weighs ≈2× a gain — Kahneman) | invented lost revenue | **true** losses only: what a client who cannot be found actually loses; never an unverifiable number |
| **Contrast / anchoring** | a fake crossed-out price | our real price ladder and the real alternative (print, ads, the rent of a shop window) |

**Mental models (22.d).** Never be creative with a convention: the navigation goes where navigation goes, the
logo goes home, the phone number is a phone number. Our version: hours in a table, one address only, the
WhatsApp button in the same place on every page. Creativity is spent on the one thing they cannot get
elsewhere — the craft of *their* page.

**MAYA** — *most advanced yet acceptable*: a familiar structure with small surprises. Our surprises are the
micro-interactions (the `.said` line, the chart frame on the Cristallin, the computed slots on Univers),
never the skeleton.

**Chunking (22.d).** 3–4 items maximum per block; a phone number is written in three groups; a list of six
becomes two blocks of three. Applies to footers, hours, prices, FAQ answers.

**Price ladders (22.d).** When two or three options are shown, describe the difference as *"everything below,
plus this"* — never repeat the same list twice. (Our two-tier AMK ladder and the Cristallin's three-option
rule, `sales/DECLINAISON-9-DECLENCHEURS-2026-09-23.md`.)

**The three friends (22.d)** — the visitor decides in three passes: *survival* (is this a real business? is it
safe? can I see it?), then *emotion* (do I like it?), then *reason* (is it worth it?). The first vote is
therefore **safety first, aesthetics last**: name, trade, town, hours, a reachable number and proof of
existence come before the animation budget. It is also why one line of plainly written truth ("we have no
team — you deal with the person who built the page") beats an invented corporate voice.

### 22.4 What actually changed on our three pages (23 Sep 2026)

| Page | Before | After |
|---|---|---|
| **Cristallin** (client-facing, already sent) | `wa.me/699905577` ×3 — **a link that errors**; `tel:` with no country code; no response after a click | `wa.me/237699905577` ×3; `tel:+237…`; `.said` band (`role=status`, `aria-live`, 6 s); the WhatsApp row now says what happens after the click |
| **Univers Optique** (Friday 10:00) | the same fallback sentence printed **twice**, word for word; the live-status line was written for eyes only | two distinct fallback sentences, one per card; `role="status" aria-live="polite"` on the live-status line; **the v1 archive also carried the broken link** — fixed, it is opened in front of the client for the A/B comparison |
| **UNI-LABO** (Friday, hour TBC) | 3 `:hover`, **0 `:active`, 0 transitions**; no response after a click; chips only had a colour state | the full four-state set + transitions; `.said` band inside the sticky bar; `aria-pressed` on the preparation chips |

### 22.5 The gate — `tools/qa/audit_page.py`

Built the same night, for the same reason as the deploy gate (§18.4): the bug was invisible to reading.
Run it **before any page goes to a prospect**:

```bash
python3 tools/qa/audit_page.py demos/concept-*.html hosting/previews/*/index.html   # rc=1 if blocking
```

Blocking: WhatsApp number without country code · no `<h1>` · no `<title>` · a template placeholder left in
the visible text. Output is three-level: **blocking** · **to fix** · **info** (an intentional demo is *info*, never a
blocker). Warnings: no `aria-live`/`role="status"` · no focus state · no "what happens next"
sentence · images without `alt` · >8 text sizes · a sentence printed twice · a field with no error state ·
more than two `href="#"`.

Four false alarms came from writing *the checker itself*, and all four are worth keeping in mind:
it flagged healthy pages as broken because it searched the **raw HTML** (base64 images contain every
character sequence, including "XXX"); it called every sentence duplicated because **our pages are bilingual**
(FR and EN carry the same sentence); it blocked the **publishable demo pages** because their WhatsApp number
is *deliberately* fake and spaced (`wa.me/6 00 00 00 00` — no real number may appear on a fictional clinic);
and it read `OC-XXXX` as a leftover placeholder when it is a **demo reference code**. All four are fixed in
the tool. The lesson is bigger than the tool: *a checker that cries wolf is not read the third time* — every
false positive is paid for by the next real finding that nobody looks at.

### 22.6 Honest limits of this section

- The **"≤6 font sizes"** check reports **25–37** on our pages. It is counting raw CSS declarations, not steps
  of a scale (our type ramp is deliberate). Do not "fix" it mechanically; the rule that binds is *do not add
  new sizes without a reason*.
- **There is no browser in this sandbox** (no chromium available; the download is blocked). So §22 can be
  checked structurally and the pages compile clean, but **looking at the rendered page on a phone remains
  King's step** — the portico is a pre-screen, never a substitute for the deploy gate.
- The psychology principles are used **only** in their honest form. No fake urgency, no fake scarcity, no
  invented reviews, no streaks, no guilt, no progress we did not actually make. A dark pattern that works in
  California destroys the one asset we have in Douala: being the person who tells the truth.

---

## §23 STYLE CHOICE, THE STAR, THE ANCHOR FONT — 2 videos (23 Sep 2026)

Folded from Web Design Lab (*7 Web Design Styles That Make Sites Look Expensive In 2026*) and Self-Made
Web Designer (*6 EASY Tips to 10x Any Site's Design*). Log + rejection list: `research/YouTube-Lessons.md`
**Lot [24]**. §22 said *how a page answers a finger*; §23 says *how a page chooses its look and carries
one idea through*.

### 23.1 Styles are chosen, not invented

*"The designers didn't invent the web design styles either. They just chose the right one."* Seven
transitions, and our arbitration for a Douala clinic/school page (mobile-first, 3G, one page, WhatsApp-first,
and a client who must recognise themselves in it):

| Transition | What it actually is | For us |
|---|---|---|
| Flat → **neoskeuomorphism** | tactile depth back: soft shadows, floating cards, glass nav, **and above all a hover/press state** | **Adopted, lightly** — depth without gloss. It is also the same rule as §22.2: the cheapest "expensive" signal is a response to the finger, not an effect |
| Static → **kinetic typography** | type becomes a visual element (scroll-linked scale/weight) | **Limited.** Our headlines are long and French; body must stay static. Adopted only as the §9 reveal we already run. Never on body copy |
| Template SaaS → **intentional minimalism** | remove the noise, keep the character: 2–3 signature cues, repeated | **Adopted as law** — see 23.3 |
| Rigid grid → **editorial design** | bold type, contrasting scale, breathing room; build the grid, then let **one** element break it | **Adopted for our own site and premium briefs**; a clinic page keeps its grid. "Freedom doesn't mean chaos" |
| Decorative → **story-driven animation** | motion must make you notice, grasp or understand something | **Adopted as a test**, not a style: *does this animation help the visitor? If not, remove it* |
| AI-generated → **human-made** | sketches, process, raw photos, authentic textures — "when perfection becomes cheap, authenticity is the real luxury" | **Already our market position** (§3 anti-slop, and our own photos-in-concepts rule). New: make the *process itself* visible — the same client page shown before/after |
| Safe → **expressive** | pick audience + feeling first, then one strong direction | **Client's call, never ours.** We do not impose expression on a clinic that needs trust |

**The rule that governs all seven, in the video's own words:** *"A trend becomes a problem when it turns
into a recipe."* So we never ask *what is trending*; we ask **what emotion does this business give, and
which style delivers it** — and we write that sentence in the build file before the first block.

### 23.2 The swap test (brand or template?)

Take the page, **swap the logo and the name for a competitor's**, and read it again. If the page still
feels natural, the visual language carries no brand.

Applied to our three live concepts: **Cristallin** passes — the acuity chart is *theirs* (the smallest line
is the specialty). **Univers Optique** passes on structure (computed slots + the six points to decide) but
not on form. **UNI-LABO does not pass**: nothing on it belongs to UNI-LABO alone — this is the page whose
visual language is generic. It is also the page with the least time invested (48 KB, built in one pass).
**Recorded as a gap, not hidden:** the next UNI-LABO-style build starts by naming its signature cue.

### 23.3 Signature cues and the star of the show

Two rules, and they are the same rule at two scales:

- **The star of the show** (SMWD): the one element that makes someone stop — and it must be *connected to
  the story*, not chosen because it looks cool. The video's own method: start from the product's core idea
  ("taking a mess of data and making it feel simple" → the star is an abstract chart). Our version of that
  question, already written into the builds: **what does this practice do that nobody else does?**
- **Visual rhyming**: repeat **a component of the star** (a shape, a colour, a texture, an icon) in 2–3
  other places, so the page feels like one universe. Not the whole element — a component of it.

**Audit of 23 Sep, on our own pages:**

| Page | The star | The rhyme |
|---|---|---|
| Cristallin | the acuity chart in the hero | the `E F P T Z O` row repeats as a graphic device; strong |
| Univers Optique | the computed slot ("the page proposes a real hour") | the counter-hours block repeats on two cards; **was broken** — the two cards printed the same fallback sentence (fixed, §22.4) |
| UNI-LABO | none identified | none — the honest state of the page |
| **Our own site** | the browser-frame preview of a real concept | the frame already repeats (4 concept cards) **but its signature detail — the three coloured dots — appeared once**. Fixed today: the dots now rhyme. |

### 23.4 The anchor font — start from the HEADLINE

The video's tip 1, and the fastest win of the six: **anchor the headline font first**, not the body font —
the headline sets the personality of the page, the body only carries the reading. Then add a second face
that is *different enough* to create contrast (the video's counter-example: Georgia with Times New Roman —
"so close, but very different; it feels unintentional"). Resource named: Fonts In Use.

**Our audited state (23 Sep):**

| Page | Display | Body | Verdict |
|---|---|---|---|
| Univers Optique | Newsreader (serif) | Public Sans | **the reference pairing** — real contrast, a clear voice |
| Cristallin | Archivo | Instrument Sans | **two grotesques**: legible, but the headline brings almost no personality of its own |
| UNI-LABO | Sora (500-700) | Inter | two sans; Sora is distinctive but the pairing is mild |
| **Our own site** | — *(none)* | system stack | **worse than a bad pairing: no choice at all.** Zero of our own house font (§5: Outfit) |

**Fixed today:** `site/index.html` now loads Outfit (400-800, `display=swap`) and sets
`font-family:'Outfit',-apple-system,…` — the exact house pattern our school/clinic pages already use,
identical fallback chain, so a failed font request leaves the page exactly as it was. This was a **drift
from our own written standard**, not a taste opinion: §5 has said "Outfit house font" since the library
was created, and every other page respected it.

**And a check worth keeping:** a page can *declare* a font it never loads — the text then silently falls
back to the device font and nobody notices. That class of bug is now a warning in `tools/qa/audit_page.py`
(with the system-family list corrected, because the first run flagged `"Helvetica Neue"` as missing —
a false alarm of exactly the kind §22.5 warns about).

### 23.5 Depth (tip 4) and hierarchy by opacity (tip 5)

- **Depth** — texture, noise, glass: *"it needs to be subtle; we don't want to compete with the star of the
  show."* Practical, weight-free recipe for our single-file pages: a `feTurbulence` SVG as a data-URI
  (a few hundred bytes, no image file) at 2–4 % opacity, **never** over the star. Our pages have no texture
  today; the recipe is written here so the next build can use it **with eyes on the result** — we will not
  add a visual effect we cannot look at (no browser in this sandbox, §22.6).
- **Hierarchy by opacity** (taken from Material Design as the video reads it): don't print everything at
  100 %. High-emphasis ≈ 87 %, medium ≈ 60 %; headline at 100 %, subheading ≈ 70 %. Our builds express the
  same three levels with named colours (`--ink`, mute, `--line`) instead of alpha — equivalent, *and*
  easier to keep consistent. **Rule: three levels of emphasis, named once in the token block, never ad hoc.**

### 23.6 Push past the first idea (tip 6)

The video's music-production analogy: the best producers make the artist sing the song faster, slower, in
another key — "you can't get to the best version by tweaking the first one". He built **12 versions** of a
single hero element.

Our equivalent already exists and is worth naming as deliberate practice: Univers Optique has **two
complete directions** on disk (v1 sober, v2 big-photo) plus two size-light variants for sending; the
Cristallin has a chart-led direction that was itself a second pass. **Rule: the first version is a draft,
never the deliverable** — and a direction is judged on a real section, not in the abstract.

### 23.7 Honest limits

- Two of the seven styles (kinetic typography, expressive design) are shown on sites whose budget and
  audience are not ours. Adopted as **tests**, not as looks.
- The video's own warning applies to the *human-made* style it recommends: it is already becoming a
  template. Being human-made is our substance, not a filter we apply to photos.
- Nothing in §23 can be verified visually from this sandbox. Fonts, dots and structure are checked in
  code; **the eye check remains King's**, as in §22.6.

---

## §24 MOBILE-FIRST — and the vertical that pays for it (23 Sep 2026, late night — Lot [25])

**Why this section exists.** King dropped three videos about the phone and one page about *laboratory*
websites in the same message. The pairing is the point: **the phone is where our clients' customers
already are** and the lab is the vertical we are selling into this week. Flux Academy's number, kept
because it is the honest one: **~60 % of global web traffic is mobile** (47 % in the USA) — not the
"99 %" the comments claim. In Cameroon the share is higher again, and our buyers live on WhatsApp on
mid-range Androids. Everything below is checked against that phone, not against a laptop preview.

### 24.1 The five mobile mistakes — Malewicz, *The Secret to Mobile Web Conversion*

1. **Cramming the desktop hero into the phone.** Less white space → unclear hierarchy → the brain reads
   the page as "not what I was looking for" and leaves. On mobile the hero carries **one** idea.
2. **Heavy animation in the hero.** "Pretty damaging to your brand, especially on mobile." Our motion
   budget already says this (§22.2, `design/MOTION.md`); this is the same rule from the conversion side.
3. **Targets too small to tap — or too big to trust.** His numbers: buttons **48–52 px on desktop,
   and on mobile above 52 but under 64**. Above that range the button starts to look like an advert and
   the brain skips it ("banner blindness"). *If a social-proof element is too small to read on a phone,
   delete it on the phone — do not shrink it.*
4. **A phone inside a phone.** Never screen-mock a mobile app inside the mobile page: nobody can tell
   what it does, and it reads as inception. **Show the problem being solved, with one simple element.**
5. **Desktop copy, reused.** A smaller screen means **bigger type, not smaller** — simplify the object,
   cut what is not essential, and rewrite the copy for the phone. He also rewrites the CTA for lower
   friction ("see how it works" instead of "try for free") and changes **"click" to "tap"**. Our pages
   say "appuyez" / "press" for exactly this reason — never "cliquez".

**Bonus, and it contradicts a habit of ours:** *avoid sticky elements on mobile.* Do not keep the logo
or the menu pinned while scrolling — use a small scroll-to-top control instead. See §24.6 for the
arbitration we wrote for our WhatsApp bar.

**Form and onboarding (same video).** Fewer fields on the phone; checkboxes **at least 32×32**;
"a form with more than two fields on mobile gets a big conversion drop" — convert first, ask the rest
later. And the technique he is testing: **micro visuals on mobile, full visuals on desktop** — the
mobile hero image usually pushes the headline and button off-screen, so it often earns nothing.

### 24.2 Mobile is its own layout, not a stacked desktop — Flux Academy, 10 live examples

- Stacking desktop columns one under the other **is not responsive, it is a disaster** — mobile gets a
  deliberate one- or two-column rhythm, and the **aspect ratio of every image is chosen for the phone**
  (portrait crops suit full-length human shots; bands become 4:3).
- **Hierarchy is big → medium → small**, and there is exactly **one** largest item per screen.
- **Generous white space still works on a phone** — it is what makes a small screen read as premium.
- **Every panel must be good enough to be a poster.** This is the cheapest quality test we have and it
  goes in the King-eye checklist: look at each section alone at 390 px and ask if you would print it.
- **Nothing essential behind layers of clicks** — "put the work up front".
- Interest is not a luxury: angles, layered cards, a horizontal band still work on a phone. **Mobile is
  not a reason to go plain.**
- A **menu button near the thumb** (bottom) is a common, working pattern — and it is why our sticky bar
  lives at the bottom.

### 24.3 Mobile-first 101 — Jesse Showalter (live)

1. **Distill the offer.** One primary thing per page. His test: screenshot the desktop, circle the ONE
   most important element big, circle the supports small — *if there is no big circle, the page has a
   problem on every screen, and a worse one on the phone.* The hamburger menu exists because showing
   the whole navigation is **not** distilling.
2. **Buttons live under the thumb.** The **rule of thumbs**: the bottom of the screen is comfortable, the
   middle is acceptable, the top is bad. (Safari puts the URL bar at the bottom, Chrome at the top —
   two different statements about what matters.)
3. **Legible type, always.** No display face for body copy, no mixed families, nothing cursive or
   handwritten; **never a thin / light / ultra-light weight on mobile** — it kills legibility. Use a
   family with 7–8 weights available, pick strong ones, adjust letter-spacing when needed. And:
   **never pure black on pure white, or pure white on pure black** — our `--ink #14151A` and the
   off-black policy already satisfy this.
4. **Optimise images and video.** Resizing inside a builder does **not** reduce the file's weight — the
   browser still downloads the big one. **Export a smaller version and let the tags choose it.** When a
   hero image cannot be made light, **ditch it for a brand colour** — a hex value in the CSS loads
   instantly. **Use SVG for logos** (ours are text wordmarks, which weigh nothing at all).
5. **Test on real devices, in the real browsers** — dev-tools device sizes at minimum, and the phone
   itself: *at night, in bright sunlight, on Android and on iOS.* Trust the browser over the builder's
   own preview.

**From his Q&A, three numbers we now use:** design the narrow frame around **360–380 px** (the
"Goldilocks" mid-size phone, not the biggest or the smallest); **~420–450 px is where mobile begins** —
below that: single column, less imagery, primary function highlighted, buttons relocated lower;
and a mobile grid of **4 or 6 columns, never 12** — and "make it till you break it" (Brad Frost) rather
than one breakpoint per device.

### 24.4 The lab / clinic vertical — Thomas Digital, *40 of the Best Lab Websites*

A commercial testing lab is not a generic corporate site, and the same seven principles hold for the
clinics and cabinets we sell to in Douala:

1. **Know the primary audience, and design for it first.** Every lab site serves at least two audiences;
   the site that serves everyone equally serves nobody. *Ours:* the patient sent by a doctor.
2. **Lead with the problem you solve, not the science you do.** The hero's job is a human entry point —
   what problem, who has it, why you are different. Detail lives one click deeper.
3. **Credibility signals belong above the fold** — accreditations, named advisors, published work,
   certifications. For a testing lab that means the real authorisation, named staff, hours, address,
   phone. **Never invented, never borrowed** (§13): what the client has not given us is a *question to
   ask*, not a badge to draw (§24.5).
4. **Navigation must follow how decisions get made** — for a lab: which tests, which samples, what
   turnaround, how to submit. Organised around the customer's decision, never around the internal org
   chart.
5. **Precision over decoration.** The clichés — dark backgrounds with glowing molecules, **generic stock
   photography of people in white coats** — differentiate nobody and mean nothing. What works: clean
   typographic hierarchy, meaningful white space, and **imagery specific to the actual work** (real
   equipment, real facilities, real people). Where original photography does not exist, good scientific
   illustration or clear data visualisation beats stock. Colour is a functional choice, and its only
   test is whether it supports the message.
6. **Technical content needs depth levels** — a plain-language summary at the top, then progressive
   disclosure for the specialist (our `<details>` FAQ and the preparation tabs are exactly this).
7. **For testing labs, the conversion path must be explicit.** Visitors arrive knowing roughly what they
   need and then meet a generic "Contact us", a phone number and a PDF with **no guidance on which to
   use or what happens next**. Saying what information is needed, **what happens after submitting**, and
   what the turnaround looks like reduces friction and raises the quality of enquiries. His sentence,
   kept in English because it is the rule: **"People don't fill out forms when they're uncertain about
   what comes next."**

Any lab/clinic **SEO** work follows from here too: a commercial lab has real, addressable local search
demand (specific tests, service areas) → structured service pages plus local presence
(`AMK-SEO-PLAYBOOK.md`), not generic keyword pages.

### 24.5 What changed on UNI-LABO the same night (23 Sep 2026, `demos/concept-unilabo-v1.html`)

| Lesson | Change, verifiable in the file |
|---|---|
| §24.1.5 — bigger type on mobile | the body copy stopped being hard-coded at `16px` and now takes the scale: **17 px below 760 px**, 16 above |
| §24.1.3 — the button window | `.btn` 44 → **48 px** desktop, **52 px** on mobile; the sticky bar **56 px** (inside 52–64) |
| §24.1 (onboarding) — the checkbox must be seen | 17 → **21 px** under 760 px; the tappable row stays 44 px and remains the real target |
| §24.3.1 + §24.1.1 — one primary | the bar carried three competing labels; it now carries **one primary (Prendre RDV / Book a visit)**, one secondary (WhatsApp) and **a phone icon** with a bilingual `aria-label` |
| §24.2 / §24.1 — the mobile hero | on a phone the **sheet comes before the photograph** in the hero: the object first, the décor after |
| §24.3.4 — weight, not dimensions | every photo ships a light variant chosen by `srcset`/`sizes`: **a phone downloads 193 KB instead of 482 KB**; the font request lost 3 unused weights (8 → 5) |
| §24.4.7 — what happens next | the form now says the message goes **from your WhatsApp to the lab's, which replies to confirm the time** — no invented delay |
| §24.4.5 — specificity over cliché | noted as the first thing to replace with the lab's own photographs; the generated set stays labelled "mise en situation" |

**The lab question this section creates (for Friday, 13 h):** 《 avez-vous une autorisation ou un agrément
du ministère de la Santé, et une inscription à un contrôle de qualité externe ? 》 — §24.4.3 says those
signals belong above the fold; §13 says we may not draw them. So it is a question with a price attached:
a credibility strip is a real deliverable, and it belongs to the client's own facts.

### 24.6 Two conflicts, arbitrated in writing (never silently)

- **"Avoid sticky elements on mobile" (Malewicz) vs our bottom bar.** Arbitration: the rule targets
  **chrome** — logo, menu, navigation pinned while scrolling. Our bar carries the page's single job
  (get in touch) for a market where the phone call and WhatsApp *are* the conversion, and it sits in the
  thumb zone (§24.3.2). **The bar stays. The navigation never sticks** — and the sticky chrome is exactly
  one row, never a header.
- **"More than two fields on mobile loses the conversion" vs a booking that needs three answers.**
  Arbitration: **two of our three required interactions are taps** (a test, a time), and the fourth
  field is optional and says so. The rule that survives is the one we will hold: **never add a fourth
  required field**; if a future form needs one, it converts first and asks later.

### 24.7 Honest limits

- Nothing here was **seen**. No browser exists in this sandbox: the changes above are structural and
  checkable in code (`tools/qa/audit_page.py`, `audit_html.py`, `check_inline_js.py`, and the two suites
  in `tools/qa/test_unilabo_page.mjs`). **The phone check remains King's** — and §24.3.5 now names what
  that check is: night, sunlight, Android, iOS.
- "Each panel must be a poster" is a criterion for a human eye, not an assertion we can make.
- Flux Academy's 10 examples are foreign, image-heavy studios and brands. The **mechanics** transfer
  (columns, ratios, hierarchy, white space); the **décor does not** — our clients are a lab and a
  cabinet in Douala, and §3.7's ban on borrowed imagery stands.
- Malewicz's numbers (48–52 / 52–64 px, 32 px checkboxes, ~420–450 px) come from product landing pages
  and app onboarding. We adopt them as **defaults with a stated reason**, not as measurements of our own
  traffic — we have no traffic yet.

---

## SOURCES
- `design/vendor/bergside-skills/` — github.com/bergside/awesome-design-skills (TypeUI), 67 SKILL.md + DESIGN.md pairs, MIT (see `design/vendor/LICENSE-bergside`)
- `design/vendor/taste/skills/` — github.com/Leonxlnx/taste-skill: taste-skill, redesign, output, brandkit, imagegen web/mobile, image-to-code, stitch, soft/minimalist/brutalist, MIT (`design/vendor/LICENSE-taste`)
- `design/vendor/emil/skills/` — github.com/emilkowalski/skills: emil-design-eng, animate, review-animations, improve-animations, find-animation-opportunities, animation-vocabulary, apple-design, prototype, pick-ui-library, MIT (`design/vendor/LICENSE-emil`); condensed for vanilla builds in `design/MOTION.md`
- `design/vendor/registry-digest.json` — machine digest of all 67 bergside token sheets
- AMK playbooks: `design/WORKFLOW.md` (pipeline), `design/STYLE-TOKENS.md` (vertical starters + rotation ledger), `design/MOTION.md` (motion standard)
- YouTube lesson batches [18][19] (footers, 17 Sep 2026) → this file §20; full log + rejections in `research/YouTube-Lessons.md`
- YouTube lesson batch [20] (talking websites / voice, 18 Sep 2026) → this file **§21**; offer-model decision in `sales/Voice-Offer-Decision-2026-09-18.md`
- YouTube lesson batch [21] (local SEO, 21 Sep 2026) → `AMK-SEO-PLAYBOOK.md`; log in `research/YouTube-Lessons.md` Lot [21]
- YouTube lesson batch [22] (interaction contract / invisible timeline / design psychology, 23 Sep 2026) → this file **§22**; full log + junk filter in `research/YouTube-Lessons.md` Lot [23]; page portico `tools/qa/audit_page.py`
- YouTube lesson batch [24] (design styles / the star / the anchor font, 23 Sep 2026) → this file **§23**; log in `research/YouTube-Lessons.md` Lot [24]; the AEO half of the same batch (Wes McDowell) → `AMK-SEO-PLAYBOOK.md` **§8**
- YouTube lesson batch [25] (mobile conversion / mobile excellence / mobile-first 101, 23 Sep 2026) → this file **§24**; log in `research/YouTube-Lessons.md` Lot [25]; the lab vertical in the same batch is Thomas Digital's *40 of the Best Lab Websites* (thomasdigital.com), a **competitor page** — read for the seven principles, not for its portfolio
- YouTube lesson batch [26] (hero systems, code-alongs, Google Maps prospecting, 24 Sep 2026) → this file **§26**; log in `research/YouTube-Lessons.md` Lot [26]; the machine check that came out of it is `tools/qa/audit_hero.py` + `tools/qa/test_audit_hero.py`; the prospecting half is `sales/APPELS-GOOGLE-MAPS-2026-09-24.md`
- **§25 rebuild of 24 Sep 2026** (not a video batch — King's verdict on the §24 page, with anresco.com and animate.bio as references) → this file **§25**; the page itself is `demos/concept-unilabo-v2.html`, its audit trail is §9 of `clients/uni-labo/AUDIT-2026-09-23.md`, and the contract it must keep is now checked by suite 0 of `tools/qa/test_unilabo_page.mjs`
- **§21 browser-support matrix (checked 18 Sep 2026):** addpipe.com "A Deep Dive into the Web Speech API" (Chrome 139+ on-device recognition, mobile matrix) · vocafuse.com "Web Speech API vs Cloud APIs" (free/no-key, audio sent to vendor servers, cloud at $0.006–0.024/min) · testmuai.com "Speech Synthesis API: Browser Support" (synthesis matrix, Firefox-Android gap). **No source was found for recognition accuracy on Cameroonian accents — that gap is stated in §21.2, not filled by assumption.**
- In-house references: `sales/Monday-Outreach-Pack.md` (Concept Production Standard), `site/design-research.md` (AMK site research), OraCare v2/v3 (reference-override case studies)

---

## §25 PHOTOGRAPHS MUST CARRY ONE MEANING — the UNI-LABO rebuild (24 Sep 2026 — commit `e936a03`, 00:03 à Douala)

**Origin, verbatim.** King looked at the mobile pass of §24 and said: *« the page isn't mobile friendly, the
pictures seem to have spoiled everything, redesign the site from scratch »* — with six screenshots of
**anresco.com** (an American laboratory) and **animate.bio** as the references. The rebuild is in
`demos/concept-unilabo-v2.html`; the audit trail is §9 of `clients/uni-labo/AUDIT-2026-09-23.md`.

**Why this section exists.** §24 was correct on every mobile measurement — 17 px body, 52 px buttons,
193 KB of images, 23 green assertions — and the page was still rejected. The lesson is not "measure more".
It is that **we were editing elements while the client was judging a composition.** Eight photographs in one
page, four of them full-width bands, some with text laid over them, means three screens of photo and one of
content on a phone. Pictures had stopped being evidence and become the page.

### 25.1 The rule

**One photograph, one meaning — and if it carries none, write a sentence instead.** Before an image goes in,
finish this line out loud: *this photograph is here because it shows `______`.* If the blank holds "it looks
professional", "it fills the space", or "the page looked empty without it", the answer is text, a table, or
nothing. On UNI-LABO the count went 8 → **5**, and each survivor names something: biochemistry, haematology,
serology, hormonology, and preparation at home.

### 25.2 Corollaries that decided the rebuild

1. **No text over a photograph, ever.** A photo is a variable surface — a phone in sunlight, a cracked
   screen, a slow connection — and text on it is the first thing to disappear. It was also the one thing the
   reference does that we must not copy for this audience.
2. **The hero may have no image at all.** A dark, typographic hero is a design decision, not a missing
   asset. If no honest photograph exists for the first screen, a generated one at that size is a lie of
   omission.
3. **Every staged image says so, in the caption.** « Mise en situation. La photo définitive sera prise dans
   votre laboratoire. » It is honest, and it is an argument: photography is not in the 150 000.
4. **Cut the files to the ratio the page declares.** UNI-LABO's tiles are declared 16/10 and the files are now
   cropped to exactly 1024×640 — no surprise recrop in the browser, and the phone variant (`-sm`, 640 px)
   plus the full one together weigh less than the old set (167 KB vs 193 KB on a phone; 394 KB vs 676 KB on a
   laptop).
5. **A `<details>` is a mobile control.** Five preparation panels became five native accordions: no chips to
   hunt for, keyboard and screen-reader behaviour included, zero JavaScript. Reach for the element before
   reaching for a script.

### 25.3 "Redesign from scratch" does not mean rewriting the contract

The order was to rebuild the site, and the tested machinery was kept **word for word**: the two JavaScript
blocks were extracted from the previous file (`tools/qa/extract_unilabo_js.py`) rather than retyped, and the
client's own content — four test families, five preparation panels, five questions, access, hours — was
carried over unchanged. The rebuild replaced the shell.

**Then we made the guarantee checkable.** The harness gained a **suite 0** that reads the page's HTML and
refuses a file that no longer carries the contract the JavaScript needs: eighteen ids, the `.chips` class,
`data-fr`/`data-en`/`data-prep` on every checkbox and moment, `data-alt-*` on every image, WhatsApp links
pointing at the laboratory's number, exactly one `h1`, and no link whose text was encoded twice.
42 assertions, green. That is what makes a from-scratch
rebuild safe: the shell can change completely, and the page still cannot go mute.

### 25.3.bis The language of a message is the sender's choice

A bilingual laboratory does not make the visitor bilingual. The rebuilt page gives every static WhatsApp link
its message in **both** languages (`data-fr-text` / `data-en-text`) and a third, written-for-the-rebuild
script swaps it when the page is read in English; the HTML always carries a real, working link (French, the
language of the staff) so the page works with JavaScript off. And the encoding rule from the rejected file is
now enforced by the harness: one apostrophe, encoded once. Its old links carried `d%26%23x27;`, which landed
in WhatsApp as `d&#x27;` in front of the patient.

### 25.4 Mobile-first, stated as a rule for the CSS

Write the **single column as the default** and let `min-width` media queries *add* columns — never the
reverse. One typographic scale that **grows** on small screens (`clamp`), one violet, one accent green
reserved for sending actions. On UNI-LABO the only breakpoints are 560 / 760 / 820 / 900 px, and every one of
them adds layout rather than shrinking it.

### 25.5 Honest limits

No browser exists in this sandbox: the rebuild was verified by the portico (`0 findings`, `--strict` rc=0),
the HTML analyser (385 text runs, 0 findings), the inline-JS compiler (6 blocks, 0 faults), the 42
assertions, and a byte-for-byte comparison of the hosted copy. **King's eye is still the judge** — and this
time it had already spoken once. The next honest step is five real photographs taken in their laboratory, on
their own bench, replacing ours.

---

## §26 THE FIRST SCREEN — and what a code-along really teaches (24 Sep 2026, learning batch [26])

**Origin.** King's morning learning batch: five videos. Three of them carry real speech and are absorbed
below (**26.1–26.4**); two are UI UNIVERSITY code-alongs whose captions contain nothing but music
(verified twice, on YouTube and on the transcript site) — for those, I read **the code in the repositories
their descriptions link to**, which turned out to be the more useful lesson. The full log, with quotes and
the discarded junk, is **Lot [26]** of `research/YouTube-Lessons.md`. The machine check that came out of it
is **`tools/qa/audit_hero.py`** (+ `tools/qa/test_audit_hero.py`).

### 26.1 The grammar of a hero (39 layouts, two videos by Payton Clark Smith)

1. **Text left, image right.** Our reading order is left to right: an image on the left is looked at
   first and the headline loses the race. Reverse only when the image *is* the product.
2. **Never text on a photograph.** Both the video ("old school", "makes websites feel outdated", the
   call to action disappears) and King ("the pictures seem to have spoiled everything") say the same
   thing from two directions. It is a legibility defect, not a matter of taste.
3. **An image cut by the fold is an invitation to scroll.** Make it deliberate: the photo continues past
   the bottom edge, or a line runs from one image into the next.
4. **Social proof belongs *below* the hero**, given room. Inside it, it competes with the headline.
   (And when there is no proof, there is no section: we never fabricate reviews.)
5. **Centre only short text.** Two sentences and it must go back to the left.
6. **No hamburger on desktop.** It hides navigation that fits. One honest exception: a single-purpose
   sales page where you *want* people to stay.
7. **Depth tricks worth reusing**: a column that swallows the nav bar; an image that overhangs its
   column; and above all, **the image space telling a process** rather than showing stock.
8. **A row of figures** (price · turnaround · users · rating) gives a hero substance without a
   photograph. For a laboratory, the honest version we already have: hours, preparation, turnaround
   confirmed on site, languages.

### 26.2 What a code-along teaches (and what it does not)

The two UI UNIVERSITY tutorials produce a spectacular hero and ship code that fails our own checklist.
Read line by line, their repositories contain four defects:

| defect | why it matters | our rule |
|---|---|---|
| `h1::before{content:'The'}` — real words in CSS | invisible to screen readers, to search engines, and to Ctrl+F; **the headline is not in the document** | text lives in the HTML. CSS may draw rules and marks, never words |
| `height:100vh` + a 180 px (or 222 px) headline + **zero `@media`** | perfect on the maker's screen, broken on a phone — the exact complaint King made about our own page | single column by default; columns added by `min-width`; type that grows on small screens (§24, §25.4) |
| `@keyframes` moving `bottom`/`top`, no `prefers-reduced-motion` | animating layout properties burns battery and drops frames; motion-sensitive visitors are ignored | animate `transform`/`opacity`; always honour `prefers-reduced-motion` |
| lorem ipsum and `{{PLACEHOLDER}}` in the shipped HTML | "Jane Doe" effect (§3.6) | no placeholder text in anything a human will open |

**The transferable lesson: the gesture is kept, the code is thrown away.** A tutorial that shows a
beautiful result is not a quality reference. Which is why these four defects are now **detected by a
tool**, not by memory: `python3 tools/qa/audit_hero.py --strict <pages…>` fails on any of them, and
`python3 tools/qa/test_audit_hero.py` reproduces the two faulty tutorials on purpose to prove the check
still bites. (Verified red on both tutorials, green on `site/index.html` and every demo.)

### 26.3 The prospecting lesson, kept where it belongs

Video 26.5 of that lot is about **getting clients from Google Maps**: three targets (no site or
broken site · outdated site · recent negative reviews), the mobile-first ranking, and the honest
observation that the first fifty calls are awkward for everyone and consistency is what separates you.
Two of the three targets we already work better than the video (we audit before we approach). The third
is new to us and lives in `sales/APPELS-GOOGLE-MAPS-2026-09-24.md`, with one rule I refuse to break: we
never promise to remove a review. And its "free website + monthly fee" advice is recorded as a decision
for King, **not** applied: our rule is no discounts, adjust the scope instead.

### 26.4 Honest limits

The hero grammar comes from two videos about other people's websites in other markets. It is vocabulary,
not proof: nothing here says a Cameroonian clinic converts like a US SaaS page. What we adopted is the
part that is structural (reading order, legibility, mobile-first, the fold) and the part that is
mechanical (the four defects above, now automated). **The eye that decides remains King's** — and the
next build it will be applied to is the school in October, on a blank page, not by re-opening a page
that was just approved.

## §27 ACCESSIBILITY — the level we promise, and the four things a machine cannot check (24 Sep 2026, learning batch [27])

**Origin.** King: *« start with accessibility, I guess you will do research online, I'll add what I can
find »*. The batch began with the two sources he sent — a Silktide explainer on the three levels and
**Accessible Web's course of 55 videos, one per success criterion** — and continued into the two
authorities: the **W3C** specification and quick reference, and **MDN**'s guides on keyboard access and
accessible names. Full log with sources: **Lot [27]** of `research/YouTube-Lessons.md`. What came out of
it: this doctrine, a machine check — **`tools/qa/audit_a11y.py`** (+ `tools/qa/test_audit_a11y.py`) — and
**eleven real defects repaired on pages we had already shipped**. A checker that finds nothing on your own
work was not worth writing.

### 27.1 The level we promise is AA, and we say the number out loud

Silktide names the three levels the way a client hears them: **A is "must do", AA is "should do", AAA is
"reaching for the stars"** (sign-language video, 7:1 contrast everywhere, 44 px targets everywhere). AAA
cannot be honoured by a commercial page and no laboratory or school here would pay for it. **AA is the
level a law, a tender or a ministry asks for.** So we state **WCAG 2.2 level AA** — and always
**standard + level**, never the adjective alone. "Our sites are accessible" is a claim; "built to WCAG 2.2
AA, checked criterion by criterion" is a sentence that survives a question.

### 27.2 The shape of an audit: one criterion, one number, at a time

The useful thing in a 55-video course is not any single video, it is its **form**: 55 criteria, each one
tested on its own, in order, and written down. That is how an audit is read, and how it differs from an
opinion. Every line our checker prints therefore carries its number — `[1.1.1]`, `[2.4.7]`, `[3.3.2]` —
and it prints what **passed** as well as what failed. A report that only lists faults cannot be trusted by
the person who has to sign it.

### 27.3 The four principles, mapped to what we actually test

| principle | what it protects | criteria we test in code |
|---|---|---|
| **Perceivable** | seeing and hearing the content | `1.1.1` every image has an alt, and the alt is not a filename ("hero.jpg") or a filler word ("image"); `1.4.4` the viewport never blocks zoom; `1.4.10` no fixed 4-digit width without a media query; `1.4.13` nothing appears on hover only |
| **Operable** | using it without a mouse | `2.1.1` no `onclick` on a non-interactive element; `2.4.3` never a positive `tabindex`; `2.4.7` `outline:none` demands a visible replacement; `2.5.8` targets ≥ 24 px; `2.2.2` no infinite animation without `prefers-reduced-motion` |
| **Understandable** | knowing what is happening | `3.1.1` a `lang` on `<html>` (and the page sets it when the visitor switches language); `3.3.2` every field has a **associated** label — a placeholder is not a label; `3.3.1` a live region announces what happens after a click |
| **Robust** | working with the tools people own | `4.1.2` every button has a name — an icon-only button needs `aria-label`, and text injected by JavaScript counts as no text at all |

Four of these were found **on our own pages**, and they are the kind of thing nobody sees until someone
looks for it: a form whose two labels were sitting next to the fields instead of attached to them; a mobile
menu that did not announce it was open (and that the Escape key could not close); a language switch that
did not say which side was active; a footer jumping from `h2` to `h4`; and ten decorative icons read aloud
as "image" before every link. **And two more were caused by the corrections themselves** — a heading pair
broken by a find-and-replace, and a status region whose `id` did not match the one the JavaScript looked
for, so that a well-meaning accessibility fix silently did nothing at all. The static checker caught the
first, a small DOM-level behaviour test caught the second. *The control caught the corrector, twice.*

### 27.4 The four things a machine cannot check — and who checks them

1. **Contrast.** Already covered elsewhere: `tools/qa/audit_html.py` computes the WCAG ratio of every text
   run from the file's own CSS, in desktop and mobile contexts. Same standard, different tool.
2. **The real tab order.** No script here has a browser. We can prove there is no positive `tabindex` and
   that a focus style exists; that the order *feels* right needs a keyboard and a minute of patience.
3. **200 % zoom / a narrow screen.** The reflow criteria are checkable in CSS, but nothing replaces looking.
4. **The quality of an alt text.** This one we did not leave to a rule. The four family photos on the
   UNI-LABO page carried the alt *"Photo d'illustration de laboratoire — Biochimie"* — which repeats the
   tile text printed right underneath and tells a blind visitor nothing about the picture. **We opened the
   four images and wrote what is actually in them** ("Six blue-capped tubes of yellow liquid in a purple
   rack, with a micropipette lying beside them"). The rule is: describe the photograph, do not repeat the
   label that is already next to it. *(A person still has the last word — the images and their alts are in
   `demos/_unilabo_v2_content.py`, four lines, easy to correct.)*

### 27.5 An automated accessibility test lies in both directions — so it is tested too

Six false positives turned up the first time the checker ran on real pages, and all six were fixed in the
tool rather than tolerated: an icon-only link that *did* carry an `aria-label`; a 19 px icon **inside** a
button (the target is the button, not its glyph); a free-text field with no `autocomplete` (criterion 1.3.5
only concerns data with a known meaning — name, e-mail, phone); a colour change on hover (that is not hidden
content); an icon inside a link that is already named; and **two buttons reported as nameless when the name was
right there** — one in an `aria-label` attribute, one in a visible `<span>`. That last one is the most
instructive of the six: it was written into a report before anyone checked it, and it produced a "fix" that
removed a perfectly good bilingual label and replaced it with a frozen one. **A false positive costs more
than a missed defect, because it makes you change something that was right.** And one false **negative**: `a:focus{outline:none}`
was satisfying our own "there is a focus rule" test — the exact rule that removes the focus ring. Lesson,
now written into `tools/qa/test_audit_a11y.py`: **a checker is only trusted once it has been shown to
refuse a deliberately broken page, to accept a deliberately clean one, and to run without complaint on our
own pages.**

### 27.6 What this is worth commercially, in one honest paragraph

No Cameroonian law obliges a laboratory or a school to be accessible today, so **the reason to do it is not
the law, it is the visitor**. The same work that a blind patient needs — real text instead of text inside an
image, labels attached to fields, a page that survives 200 % zoom, targets big enough for a thumb, text that
reads in bright sun on a cheap screen — is what everyone needs on a 3G phone in Bonamoussadi. It is also the
one visible quality difference between our 150 000 FCFA page and a template, and it costs nothing extra to
keep. For the October school, it becomes an argument: a school that receives parents with disabilities is
not served by a site those parents cannot use.

**What we do NOT claim:** that a page passed "an accessibility audit". We claim what we ran, on which
criteria, and we say which four things still need a human eye. §26 ends on the same note: the eye that
decides remains King's.

## §28 WHAT A SCREEN READER HEARS — the second accessibility batch (24 Sep 2026, learning batch [28])

**Origin.** The day the accessibility report was published, King sent exactly the two things it named as
missing: **a real screen-reader test** and **forms**. Four sources: a full NVDA tutorial, a French article on
accessible forms and error messages (Kortic), an NVDA add-on that imitates TalkBack's per-object sounds, and
a WhatsApp help-centre page. Lot [28] of `research/YouTube-Lessons.md` holds the detail. One of the four
could not be read at all (the WhatsApp page answers **403** to our fetcher, and this sandbox has no
command-line network) — **so it is written down as unread rather than summarised from memory.**

### 28.1 A page can be perfect in code and mute in the ear

The NVDA tutorial does one thing better than any specification: it plays **the same form twice** — once as
the author built it, once as Apple did — and lets you hear the difference. On the faulty form the screen
reader announces *"page blank"* on a page that visibly contains a whole form; the radio buttons are read as
*"personal radio button, one of two"* with **no group name**; the terms checkbox is announced *"blank"*; and
when the form is submitted with a missing field, **no error is announced at all**. Every one of those is a
criterion we already check statically — but here is what they *sound* like, which is the only way to judge
whether a page works for someone who cannot see it. Two batches, two independent roads to the same sentence:
**the machine checks the code, a person checks the ear.** There is no tool that listens for us.

### 28.2 Landmarks: the first thing to break, and the cheapest to fix

The tutorial's very first finding is the worst one, and it is invisible: **no landmark means the screen
reader finds nothing in the middle of the page.** It reads the header, the menu, the footer — and calls the
page blank. Our site's three pages had **no `<main>`** at all. They have one now, and NVDA's `D` key has
somewhere to land. This is also why the skip link matters (`2.4.1`, **level A**, not a nicety): the second
press of a key should not be the only way past a menu.

### 28.3 A group has to say what it is a group of

Nineteen checkboxes for nineteen analyses, each individually perfectly labelled, can still be an
inaccessible form: the reader announces *"Biochemistry, checkbox, not checked, one of nineteen"* and never
says **what the nineteen belong to**. A `<fieldset>` with a real `<legend>` fixes it — UNI-LABO has had
both since the rebuild (`1 · Vos analyses`, `3 · Moment souhaité`), and our checker now refuses a
`fieldset` whose `legend` is empty. The rule: **a label names the field; a legend names the question.**

### 28.4 Errors are part of the interface, not an afterthought (Kortic)

Anthony Ladeuil's article is the best French-language treatment we have found of the part everyone skips.
What we adopted, in his order:

1. **A label, linked and adjacent** — and **the placeholder is not a label**: it disappears as you type,
   and its contrast is usually too low to read. (`1.3.1`, `3.3.2`)
2. **Announce the expected format** — and for dates, never as `jj/mm/aaaa`: a French voice reads that as
   *"gigi barre oblique aime aime barre oblique ah ah ah ah"*. Give a real date. *(This line alone was worth
   the article.)* 
3. **`type` and `autocomplete`** — they bring the right keyboard on a phone and let the browser help instead
   of making a thumb do the work. (`1.3.5`)
4. **`fieldset` + `legend` for groups**, as above.
5. **No CAPTCHA** if it can be avoided (a honeypot instead) — CAPTCHAs are where accessibility goes to die.
6. **Mark the optional fields, not the required ones.** The asterisk is a 1999 habit: it does not vocalise,
   and its meaning has to be explained *before* the form, which nobody does. Our own form had a naked
   asterisk on "School or clinic name" with no explanation anywhere. Now the one optional field says
   *(optional)* and the required one says nothing — which, in a two-field form, is all it needs.
7. **The error summary**: a container that receives focus, one line per error, and — the good part — each
   line is **a button that takes you to the offending field** and marks it `aria-invalid`.

### 28.5 The defect that was in our own form, and it was the exact one described

Our site's form had `if (!biz) return false;`. Click "Get my free preview" with an empty name and **nothing
happens**: no message, no focus, no announcement. That is the tutorial's *"it does not introduce an error
message… only says blank"*, written by me, in production, on the page we send to every prospect. And there
was a nastier corner: a field filled with **spaces** passes the browser's native `required` check, so the
JavaScript was the only safety net — and it stayed silent. Fixed the way both sources describe: the live
region announces what is missing, the field is marked `aria-invalid`, and **focus moves to it**. The
behaviour test now asserts all of it, including the spaces case, because this is exactly the kind of "fix"
that can look right in a diff and do nothing at runtime.

### 28.6 TalkBack is the reader our market actually has

The third source is a small NVDA add-on that reproduces TalkBack's sound per object. The add-on itself is
not what matters — what matters is what it imitates: **on Android, you explore element by element, with a
sound for each object.** Anything not reachable by swiping does not exist. That sentence should sit next to
every design decision we make, because the phone in Bonamoussadi runs Android, and the same work that serves
a blind patient — real text, attached labels, one message per element — is the work that serves everyone on
a 3G connection. Which is why the protocol below ends on the only question that pays our bills: **does the
double tap open WhatsApp?**

### 28.7 The protocol, and its limits

**`tools/qa/PROTOCOLE-LECTEUR-ECRAN.md`** — a 5-minute manual test: what to install, the eight keys that
matter, *what we should hear on our own pages* (with the real counts: 44 headings and 42 links on the site;
"*1 · Vos analyses, group of checkboxes, 1 of 19*" on UNI-LABO), the TalkBack gestures, and where to write
the result. Its §6 states the limits: **neither of us is an experienced screen-reader user** — we test the
mechanics, not the lived experience — and we never test on the client's real page. What we write is what we
heard, on which page, with which version. Same rule as every other measurement in this repo: **a number you
did not take yourself does not enter a report.**

## §29 THE HERO, SECOND PASS — the process, the gaze, and the 90/10 (24 Sep 2026, learning batch [29])

**Origin.** Five videos from King, all about the first screen: three from **Flux Academy** (1.09 M
subscribers — a process video, 21 real layouts, and episode 10 of their web-design course), one from
**Ahmed Alsayad** (conversion blueprint, with a to-do list), one from **Malewicz** (25 years of design,
500 hours of Hotjar recordings). Full log: **lot [29]**. Unusually, this batch **overlaps** the hero batch
already absorbed in §26 — so this section is written as *what the first pass did not have*, not as a
second telling.

### 29.1 What is genuinely new

§26 (Payton Clark Smith, 39 layouts) gave the **grammar**: text left by default, never text on a photo, an
image cut by the fold invites scrolling, social proof belongs below, a hamburger on desktop is a fault.
This batch adds four things that are not in it: **the process that produces a hero**, **the mechanics of
directing an eye**, **the division of labour between the hero and the rest of the page**, and **the
cognitive-load failure**. Two of those are now machine-checked.

### 29.2 The process — and why a grey wireframe fails with real clients (Flux Academy)

Six steps, in this order: **strategy → wireframe → 3 concepts → imagery → design → optimization**.

The strategy step is a conversation with the client, and its questions are the ones we should be asking
anyway: *what are you selling, why did you start this, who are you trying to help, what should people do
on this site*. Flux distils the answers into **one clear value proposition and one action** — before
opening a design tool.

Then the wireframe, and here is the sentence worth keeping: **the wireframe is not pretty and is not
supposed to be.** It is the content, placed, so the client can say *yes, that is what we do* before anyone
argues about colours. And the second sentence, which contradicts the first: clients do not understand
grey boxes. Malewicz calls his answer **type framing** — start with the copy at real size and real
hierarchy, then choose the visual to match the copy, never the other way round. Applied to us: when we
show a laboratory or a school its own hero, the words are already theirs (that is the live sheet), so
what we are really asking is *does this say what you do* — the fastest approval we have ever got.

The step we were skipping: **three rough concepts, sketched with shapes, before any design.** The point is
not decoration, it is to check *whether there is room for the text next to the image* — a hero concept
that only works with the text on top of the photo dies here, on a napkin, instead of after a rebuild. We
already do three directions in the uniqueness protocol (§2 of `PRE-FLIGHT.md`); this makes it three
*drawn* concepts, shown to the client, before the build.

Finally, optimization: *free* ("join for free"), **social proof with a number and faces**, "featured on"
logos, and a **ghost button** for the secondary action so it does not compete with the primary one.

### 29.3 The anatomy, and the charge mentale (Ahmed Alsayad)

The hero carries five elements: **headline, subheading, visual, trust signal, call to action** (primary,
plus optionally a secondary). The purpose is a single sentence repeated in different words by every source
in this batch: *what is this, who is it for, what do I get, why should I care* — answered in the time it
takes someone to decide whether to stay (Flux's **15-second rule**: 80–90 % of visitors leave before that).

The failure mode he names is the one our own pages could fall into: **cognitive overload**, which he
defines precisely as *the visitor is given many options and therefore chooses none*. Its symptoms are all
mechanical: several CTAs, several colours, no clear hierarchy, everything crowded in because "this is the
hero, let's put it all here", and — worse — **hidden CTAs**. His second family of faults is more
instructive because it looks successful: the award-chasing hero. Heavy parallax "looks great when you
showcase it, but it either kills usability or kills performance"; clever headings that are not clear;
background video and 3D. *It wins a prize; it does not get a client.*

So five of his rules became checks in `tools/qa/audit_hero.py`: a hero with **no subheading**, a hero with
**no action at all**, a hero with **more than two actions**, an **icon-only logo**, and a hero locked at
`height:100vh` with nothing (an arrow, a word, the top of the next section) to say that there is
something below.

### 29.4 Directing an eye — three mechanical techniques (Malewicz)

This is the part we cannot check in code and should apply the next time we shoot a photograph or pick
one. All three are concrete:

1. **The gaze principle.** A person looking at the camera puts the attention on their eyes. A person
   looking *towards* the copy or the button makes us follow their gaze to it. On mobile, the same photo
   recropped so the person looks **up** at the CTA puts the reader's eye exactly where we want it —
   and this is why the pivot from phone screenshot to a real photo matters: we can control where a person
   is looking, we cannot control where a screenshot points.
2. **The optical guide.** The right edge of a block of text, if it forms a soft diagonal, is a funnel
   that leads the eye down to whatever is next. A jagged edge is a wall.
3. **CTA colour matching.** Take the colour of the main button, find it in the photograph — *recolour a
   garment to a hue near it*, keep every other garment muted (colour the whole outfit and it reads as a
   uniform). The visual then connects to the action subconsciously instead of by decoration.

The trend he warns against is exactly the one that costs us nothing to avoid: **gradient shapes and
lighting effects instead of people**. "It has nothing to do with amplifying the message… it is just a
distraction." And the image that works is not the prettiest one: it is the one whose person **matches the
target audience** ("it can't be a random image") — King said the same thing on 24/09 about the house in a
generated photo, from the opposite direction.

### 29.5 The 90/10 rule, or why our proof is not in the hero

Malewicz, from 500 hours of session recordings: **the hero does 90 % of the persuasion; the remaining 10 %
is done below it by "clearing doubts"** — social proof, examples, use cases. One confirms a sale only
when the two are added together. This is precisely why §26 already put social proof *below* the hero, and
why our pages are built the way they are: the hero states one thing, and the sections underneath answer
the objections (the live sheet, the results, the five questions). **A hero that tries to carry the proof
as well as the promise is a crowded hero** — the fault in 29.3, arriving from the other direction.

### 29.6 "Do not put your app in the hero" — and why we are the exception

Malewicz's most contrarian rule: a big screenshot of the product in the hero is often *bad*, because the
visitor does not know your product and does not care how it looks. Show a person and the problem being
solved; show one small panel if you must; show the whole interface **further down**.

That is a real trap for us — our concept pages sell *websites*, so their hero could easily be one enormous
screenshot — and we are the exception for the reason §26 already gives: **an image may take the first
glance when the image IS the product.** A screen of the site we built is the product; a dashboard is not,
for someone who has never heard of the dashboard. Worth saying out loud in a meeting, because the two
cases look identical on a moodboard.

### 29.7 What we will not copy: the invented number

Flux builds trust with "Obi-Wan and 4,000 others have already joined" and logos of TV stations. It works.
We have no reviews, no client count and no press — and inventing any of the three is forbidden (and has
been since the first day: no invented price, no invented testimonial). What we have is honest and
checkable: **five real pages anyone can open**, the laboratory's own words, and the fact that the visitor
is looking at their own future site. So "not yet" is written here for the day someone asks why our hero
does not carry a row of numbers.

### 29.8 Honest note: on 24/09 the audit found nothing on our pages

Twelve checks (the five new ones included) run over the six pages we own: **zero findings**. The three
site pages and UNI-LABO already answer who/where, carry a subheading, hold at most two actions in the
hero, show the name next to the icon, and never lock themselves at `100vh` with no way down. That has
never happened before in this repo — five batches in a row each found real defects in our own work. It is
also not a reason to relax: the checks are from sources read the same day, and the next page (the school,
in October) starts from a blank file, where none of this is inherited.

---

## §30 THE DEAD SKIP LINK, AND THE PAGE WE DO NOT OWN (24 Sep 2026, learning batch [30])

King sent four links with no text: **three about the Google Business Profile** (Santrel Media, 1.13M —
the step-by-step install; Ignite Visibility, 64.9K — twenty checkpoints; Zanet Design, 36.2K — a
compilation billed as a masterclass) and **one about accessibility** (Imran Siddiq, Web Squadron, 195K —
a full walkthrough built inside Elementor).

### 30.1 · The skip-link lesson: present is not the same as working

The accessibility video exists because the **European Accessibility Act** now pressures agencies. Imran
does not hand out a checklist; he builds a page and shows the failures. The sharpest one is a failure our
own control could not see:

> He tabs to **“skip to content”**, presses Enter — and **nothing happens**. The link is there, visible,
> in the tab order; its target is not. He demonstrates it across template types: default works, canvas has
> nothing to skip, **full width shows the link and swallows the click**. His words: *“if your header
> template was 50 % of your screen, they'll keep clicking it and they will get very frustrated and they
> will lose trust in your website.”*

That is worse than having no skip link at all, because a keyboard user pays the cost of trusting it. Our
control said *compliant* on any page containing a `href="#"` and the word “skip” somewhere in the file — a
link to nowhere passed. Since lot [30] it checks two things: **the target exists** (`#contenu` must be an
id in the page) and **the link is reachable** (a rule that hides it must have a matching `:focus` rule
that brings it back). Our pages pass on both counts, and the healthy test witness now carries the exact
production pattern (`.skip{position:absolute;left:-9999px}` + `.skip:focus{left:0}`), so the guard rail
locks the real thing instead of an approximation.

Two neighbouring lessons from the same video, both turned into rules:

- **A hidden label is allowed. An empty label is not.** *“If you hide the label … as long as it is
  completed somewhere.”* A form now fails the audit if a `<label>` is empty even when the `for=` is
  correct — the field would be announced with no name.
- **Contrast depends on size.** His colour-picker demo: a pinkish red fails at 16 px, passes at 24 px,
  fails again at 23 px. `audit_html.py` has applied exactly this since we built it — 4.5:1, dropping to
  **3:1 at 24 px or at 18.66 px bold** — and it composites opacity before comparing. The video confirms
  our number; it does not change it. **We deliberately did not add a second contrast check**: two
  instruments measuring the same thing eventually contradict each other, and the honest place for that
  number is the tool that already computes it from the file's own CSS.

### 30.2 · What the video says that does not apply to us

- **The accordion warning.** He shows that tabbing an Elementor accordion jumps from item 1 to the bottom,
  skipping 2 and 3, and that only arrow keys work — so he injects an `sr-only` hint telling screen-reader
  users to use arrows. That is a defect of an ARIA `tablist` pattern implemented as a widget. **Our FAQ is
  ten native `<details><summary>` pairs per page** (five on the école page): every `<summary>` is its own
  tab stop, tabbing moves through them in order, and no hint is owed. Rule kept for the day we build a
  tablist: if we ever do, the hint is mandatory.
- **Videos.** Captions are required, player controls must stay, and a **background video must offer a
  pause** (he links a nine-minute video on how to add one). We produce and embed **no video anywhere**
  (zero `<video>` elements across the pages), so there is no control to write today — a control over
  content we never make is dead code. The rule is written here to be applied the first time a client hands
  us footage.
- **Icon names.** Social icons are ambiguous: does the Facebook icon share *this post*, or open *our
  page*? His answer is `aria-label` when the icon is the only name. Our pages have one, three and two icon
  links, all named — by `aria-label` or by visible text. **Checked, nothing to fix.**

### 30.3 · The instrument lied for the fourth time

My quick script announced “**2 icon links with no name**” on the école page. False: both are named by
their **text** (“Recevoir mon aperçu gratuit”, “Aperçu gratuit 24h”), and the audit tool counts a name as
attribute **or** content — the very lesson of lot [28]. Fourth occurrence of the same family, now with a
rule attached: *a quick script of mine is not an instrument; if it accuses a page, the accusation is
checked against the tool that has witnesses before anything is “fixed”.* Nothing was changed on the page.
Nothing needed to be.

### 30.4 · The Google profile is a page we do not own — and it is the first screen of local search

The three Google Business Profile videos matter to us for one reason: **that profile is where a local
client finds a business, and it is one click away from the page we sell**. Santrel says it plainly — people
on Maps *“almost always go and click on the website link”* — so the profile is the door and our page is
the room. Zanet sharpens it: **70 % of what Google serves a customer no longer goes through the website at
all** (reviews, hours, photos, questions), yet the click that decides everything still lands on the site.

Read as a designer, the profile is just another **first screen**, and the rules of §26/§29 apply to it
unchanged:

| our rule for a page | the same rule on the profile |
|---|---|
| one clear title, real words | the **name** exactly as it is — keyword-stuffing it is both what Google punishes and what we refuse to do for a client |
| no invented claim | true hours, true service area, true category. All three videos warn about people faking a four-hour service radius; Google checks |
| the hero carries the promise, the proof lives below (90/10, §29) | photo + category + hours carry the profile; **the reviews do the “clearing doubts” below** |
| a photo must carry one meaning (§25) | the façade photo is the first thing seen on Maps: real place, real people, real work — and Google Images (“*trade + neighbourhood*”) is an honest way to see what Google rewards, in order to photograph one's own version of it |
| write the words the customer uses | the description (750 characters) is the profile's about-page: services, neighbourhoods, verifiable history |

And two rules of ours that the videos do **not** contain, kept explicitly:

1. **We never script a review.** All three push towards guiding the customer's vocabulary (“ask them to
   mention *fast service*”). We ask for an honest review, we show how to post it, and we stop there.
   Buying one, rewarding one, or writing it for a client is a suspension risk for them and a lie for us.
2. **We never sell a ranking.** Zanet sells SEO consultancy; his own material says Google weighs *“over
   200 factors”*. We can keep a profile clean and complete, and we can say exactly what we changed. We
   cannot promise a position in the top three, so we never put one in an offer.

The operational version — install order, the thirteen suspension traps, the `wa.me` rule for the profile's
WhatsApp chat, and what belongs to the client rather than to us — is in
**`sales/FICHE-GOOGLE-PROFILE.md`**, written the same day.

### 30.5 · What today's reading changed in the repository

- 3 controls hardened in `tools/qa/audit_a11y.py` (dead skip link, unreachable skip link, empty label),
  3 negative witnesses and 3 new assertions (26 in all) — see §30.1.
- 1 invented hour replaced by a commit hour in 6 places (`00 h 30` → *nuit du 23 au 24, commit `e936a03` à
  00:03*), plus the CRM source, rebuilt and re-locked.
- 1 new operational document (`sales/FICHE-GOOGLE-PROFILE.md`), 2 meeting sheets cross-referenced.
- 1 false claim of mine corrected **in writing** rather than deleted: I had written that UNI-LABO had a
  Google listing “found by our Maps sweep”. The CRM line says `source: directory`, and the thumbnail I was
  looking at is our own mock-up. The correction is dated in `sales/FICHE-GOOGLE-PROFILE.md` §1.
- **Nothing changed on the pages themselves.** Four pages audited: 0 fault, 0 warning — before and after.
