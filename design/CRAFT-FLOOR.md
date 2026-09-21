# CRAFT-FLOOR — design quality floor from the 2026-09-15 skill-library study

**Status:** controlling overlay on the root law (`/AMK-DESIGN-SKILLS.md`) and `design/WORKFLOW.md`. Where this file is stricter than existing rules, this wins; where the root law bans more, the ban wins.
**Sources (studied in full, 15 Sep):**
- **Impeccable** (Paul Bakaus, pbakaus/impeccable) — `.agent/skills/impeccable/SKILL.md` + `reference/{craft-floor,layout,typeset,colorize,animate,audit,critique,polish,harden,adapt}.md` (MIT; not vendored — binary+76 MB; distilled here).
- **Anthropic frontend-design plugin** (`anthropics/claude-code/plugins/frontend-design`, Apache-2.0) — distinctive, non-templated UI direction.
- **UI/UX Pro Max** (nextlevelbuilder/ui-ux-pro-max-skill, MIT) — 119 UX rules; its search DB was run against both our verticals (results logged below).
- These join the vendored libraries in `design/vendor/` (bergside, emil, taste).

---

## 1. Surface modes (name the mode before designing)

Every surface is exactly one mode, named in the builder header comment:

- **Persuade** — visitor decides and acts. **All AMK client sites and named concepts.** Earn attention, remove doubt, one dominant action.
- **Operate** — visitor completes a task (dashboards/admin). None in our current catalogue.
- **Read** — visitor understands (docs/articles).
- **Experience** — portfolio/gallery.

Rule of thumb that matters for us: the client site (patients/parents) is minimal and B2C; the *pitch material aimed at the proprietor/medical director* is allowed to be dense (high-consideration buyers want exhaustive answers — same lesson as the Medidesk 3× case in Addendum #3). Do not strip pitch pages to minimal, and do not bloat client pages.

## 2. The craft floor (mechanical checks on the BUILT result)

Run together in one batched inspection (they share one render), answer with evidence, never intention:

1. **Contrast:** body/placeholder ≥ 4.5:1, large text ≥ 3:1, focus ring ≥ 3:1. On tinted surfaces, derive muted text from the surface hue — never generic grey.
2. **Depth:** every shadow has an offset AND soft blur; a zero-offset coloured halo is decoration and is banned. Tint shadows to the background hue (already in root law §3).
3. **Spacing:** a documented 4 px-based scale (8-only misses useful middle steps). Tight groups, generous separation; more space ABOVE a heading than below it. Proximity first, containers second; nested cards are always wrong.
4. **Type:** body ≥ 16px; prose measure 45–75ch; display ≤ 6rem; headings balanced (`text-wrap:balance`); obvious size/weight steps; real FR+EN copy run at every breakpoint; fix what overflows (FR expands ~15–20% — reserve it).
5. **Motion:** ONE authored moment per surface, not an identical fade-rise on every section. Feedback 100–150 ms; state changes 150–300; entrances ≤ 500–800; exits faster than entrances; ease-out arrivals (`cubic-bezier(.16,1,.3,1)`), never bounce by reflex; animate transform/opacity, never width/height/top/left. Every animation has a `prefers-reduced-motion` path that preserves state feedback (colour/opacity changes may remain; spatial movement goes).
6. **States are deliverables:** hover, active (scale .95–.98, 100–160 ms), focus-visible, disabled, loading, error, empty — plus real content and working controls. Focus ring is visible, branded (clinic emerald / school gold), never removed.
7. **Browser surfaces carry the design** (cheapest "built, not assembled" signal, most skipped by AI): selection colour, focus ring, underline offset; tabular numerals for stats/prices (`font-variant-numeric:tabular-nums`).
8. **Coverage:** every brief requirement findable within seconds; run the real booking/admissions path mouse + keyboard + thumb.
9. **Touch:** ≥ 44px every target (our sticky bar is 52–64px per Addendum #3); no hover-only affordance; body padding clears the fixed bar.
10. **Performance:** hero image eager + compressed (<200 KB target), all other images `loading="lazy" decoding="async"`; one font family, preconnect, metric-compatible fallback; no layout shift (aspect-ratio on media).

## 3. Refuse list (defaults you may use only when the brief earns them)

Borrowed from impeccable's craft floor and Anthropic's anti-template list, reconciled with our market:

| Tell | Standing AMK position |
|---|---|
| ALL-CAPS tracked eyebrow above every heading | The libraries call it the #1 AI tell and impeccable bans eyebrows outright. **AMK compromise:** eyebrows are bilingual section wayfinding on dense pages — keep, but sentence-case, minimal tracking, and within the §13 count. No eyebrow on a hero that already has a strong H1. |
| Single italic/coloured word in a headline | Avoid. Emphasis from weight/size; our H1 `<em>` highlight is allowed once per page (current builds comply). |
| `→` appended to buttons/links | A known templated tell, BUT it is WhatsApp-native vernacular for our users. Allowed on WhatsApp-action buttons only; never on neutral nav links. |
| Emoji as the icon system | Chrome/brand icons MUST be drawn SVG in one consistent stroke (we already replaced video and nav glyphs this way). Emoji may appear INSIDE content as human language (WhatsApp buttons, service tiles) — our audience texts in emoji; this is a documented market exception, not laziness. Never emoji for nav, form controls, or status (status = colour + shape + word). |
| Identical icon+heading+text card grid as page skeleton | Rotate layout families (already root law); service bento allowed once per page, never nested cards. |
| Big-number/small-label/stats/gradient hero metric | Our stats STRIP (not hero) is acceptable: it is proof, with demo labels, and never uses a gradient. |
| Numbered markers 01/02/03 | Only when the content IS a sequence (our 3-step booking qualifies; nothing else). |
| Gradient text, glass-as-decoration, hard offset shadows, mono-as-costume, geometric mask cutouts, "phone in a phone" | Banned (root law already covers most). |
| Fade-and-slide-up on EVERY section (`rv`) | Reduce: only above-the-light key moments; a page where every block animates identically has no authored moment. New named builds cap `.rv` to ≤ 40% of blocks. |
| Warm cream #F4F1EA + terracotta / near-black + acid green / SaaS soft-shadow kit | Never as unexamined defaults (root law §3 extends this). |

## 4. Two-pass design discipline (Anthropic process, now mandatory for named concepts)

1. **Plan pass (in the builder header / lead dossier):** 4–6 named hex tokens; typeface roles; one-sentence layout concept with ASCII wireframe; the one bold element ("spend boldness in one place"); the page's authored motion moment.
2. **Self-critique pass before code:** "would I produce this for ANY clinic/school?" If yes, change the specific part. Subject-matter grounding wins — palette and vernacular come from the client's world (quarters, denomination, speciality), never from a category habit.
3. Build, then critique with evidence: **squint test** (primary → secondary → groups still readable blurred), cognitive-load count (≤ 4 options at any decision point; Miller/Cowan ≤4, not 7), Nielsen heuristics scored 0–4 (most real pages land 20–32/40; be honest), and 2–3 persona walks:
   - **Parent abroad** (phone, slow wifi, one chance before boarding deadline): can they start admission in ≤3 taps?
   - **Anxious first-time patient** (older Android, sunlight): price + WhatsApp reachable from every screen?
   - **Cost-conscious shopper** comparing with a directory listing: is proof one scroll away?
4. Chanel step: before delivery, remove one accessory.

## 5. Vertical grounding decisions logged (UI/UX Pro Max DB runs, 15 Sep)

Ran the tool's design-system recommendation engine against our two verticals:

- **Clinic** → pattern **Hero + Testimonials + CTA** ("social proof before CTA", testimonials with photo/name/role, pause on focus/reduced-motion) — matches Addendum #3's order, now confirmed by the data. Suggested style Neumorphism and cyan palette **rejected**: soft-UI fails contrast at scale and our warm bone/emerald world is already committed and distinctive; fonts suggested Figtree/Noto Sans (healthcare) noted as fallback candidates for a future client with poor-script needs.
- **School** → tool returned Claymorphism + Baloo 2 (kids' app styling). **Rejected deliberately:** our buyer is the PARENT (trust, heritage, GCE, fees), never the pupil; playful children's styling would undermine the sale. Navy/gold institutional language stays. This decision is recorded so the tool never re-litigates it.
- Tool's canonical **pre-delivery checklist** (375px test, no emoji-icons for chrome, visible focus, reduced-motion, ≥44pt targets, safe areas, decorative icons `aria-hidden`, form labels/hints/errors, auto-rotating content must pause) is folded into §2 and root law §13.

## 6. Accessibility additions to root law §13

- `:focus-visible` ring shipped (clinic emerald / school gold), 3px, 2px offset.
- Count-up/visual JS respects `prefers-reduced-motion` by rendering final state immediately (now implemented in both generators).
- Decorative emoji/icons beside visible text: `aria-hidden="true"`; meaningful images carry descriptive alt; hero alt names the real (demo) subject.
- Language toggle sets `<html lang>` (already shipped); FR content must also satisfy contrast/measure checks, not just EN.
- Colour never the only signal (form errors = text + icon + hue; required = label text).
- Auto-rotating content (if ever added, e.g. testimonial carousel): must pause on hover/focus/reduced-motion and expose controls; our current static quote grid is the safer default — keep it.

## 7. Structured data as craft (schema skill, marketingskills repo)

Implemented in both generators 15 Sep as `@graph` JSON-LD:
- Clinic: `MedicalClinic` (address, contactPoint with EN/FR, medicalSpecialty, priceRange) + `FAQPage` mirroring the visible FAQ exactly.
- School: `School` + `FAQPage` likewise.
- Launch replacements commented in source: real address/phone, `openingHours`, `geo`, `sameAs` [Google profile, FB, TikTok, IG].
- **`aggregateRating` only with real, third-party-visible reviews** — never on a concept (accuracy law). Schema must match visible content; validate every build at search.google.com/test/rich-results before handoff.

## 8. Handoff/QA routing

- Planning/new visual world → WORKFLOW.md stages 1–4 + this file §4.
- Before any UI edit → this file §2.
- Final pass → root law §13 + Addendum #3 gates C1–C14 + real Android test (night/sunlight/slow MTN).
- Something looks "fine but generic" → §3 table + Anthropic five-trait list; change the specific default, do not soften it.
