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

---

## §6 COLOR SYSTEM

### 6.1 Construction
- Max 1 accent. Neutral base (warm or cool, locked). 1-2 secondary tints for section backgrounds.
- Text on accent: WCAG AA 4.5:1 (3:1 for large text). Audit every CTA.
- Shadows tinted to background hue. Consistent light direction across all shadows.

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
- [ ] 0 console errors in headless Chromium (EN, FR, mobile 390)
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

**Heroes:** asymmetric split · editorial manifesto · media-mask · kinetic-type · curtain-reveal · scroll-pinned · image-as-canvas · mini-minimalist.
**Nav:** floating glass pill · magnification dock · mega-menu reveal · contextual radial.
**Layout:** bento (exact cell count) · masonry · split-screen scroll · sticky-stack · chroma grid.
**Cards:** parallax tilt · spotlight border · glass panel (inner refraction) · morphing modal.
**Scroll:** sticky stack · horizontal hijack · zoom parallax · progress path · SVG line-draw.
**Micro:** magnetic button (motion values, never state) · particle-success CTA · skeleton shimmer · directional hover fill · ripple.
**Type:** kinetic marquee (max 1/page) · text-mask reveal · text scramble · circular text path.
**Libraries:** CSS/IO for single-file (AMK standard) · Motion (motion/react) for React UI · GSAP+ScrollTrigger for scrolltelling · never mix GSAP+Motion+rAF in one tree.

---

## SOURCES
- `design/vendor/bergside-skills/` — github.com/bergside/awesome-design-skills (TypeUI), 67 SKILL.md + DESIGN.md pairs, MIT (see `design/vendor/LICENSE-bergside`)
- `design/vendor/taste/skills/` — github.com/Leonxlnx/taste-skill: taste-skill, redesign, output, brandkit, imagegen web/mobile, image-to-code, stitch, soft/minimalist/brutalist, MIT (`design/vendor/LICENSE-taste`)
- `design/vendor/emil/skills/` — github.com/emilkowalski/skills: emil-design-eng, animate, review-animations, improve-animations, find-animation-opportunities, animation-vocabulary, apple-design, prototype, pick-ui-library, MIT (`design/vendor/LICENSE-emil`); condensed for vanilla builds in `design/MOTION.md`
- `design/vendor/registry-digest.json` — machine digest of all 67 bergside token sheets
- AMK playbooks: `design/WORKFLOW.md` (pipeline), `design/STYLE-TOKENS.md` (vertical starters + rotation ledger), `design/MOTION.md` (motion standard)
- In-house references: `sales/Monday-Outreach-Pack.md` (Concept Production Standard), `site/design-research.md` (AMK site research), OraCare v2/v3 (reference-override case studies)
