# AMK Motion Standard (vanilla HTML/CSS/JS edition)

_Distilled from `design/vendor/emil/skills/` (Emil Kowalski's animation skills, MIT) and the taste-skill motion rules. These are exact values, not approximations: copy them into every build. React/Motion/GSAP guidance lives in the vendored skills; AMK concepts are single-file vanilla, so this file is the house adaptation._

## 0. The gate (run before adding ANY motion)

Every animation survives all four questions, in order. If it fails one, delete it.

1. **Frequency** — how often is it seen?
   - 100+ times/day (core nav, language toggle that users hit repeatedly): **no animation, ever**.
   - Tens/day (hover states, list rows): near-imperceptible only.
   - Occasional (modals, FAQ accordions, booking confirmation): standard animation.
   - Rare/first-time (hero entry, success/celebration): this is the entire delight budget.
2. **Purpose** — name exactly one: feedback · spatial consistency · state indication · preventing a jarring change · explanation (marketing). "It looks cool" is rejected.
3. **Speed** — fits the duration table below (UI under 300ms; marketing reveals may run 400-700ms).
4. **Function** — on data the user is reading/acting on (price tables, lab panels, opening hours), motion hinders. Leave it still.

Cap: at most 5-7 deliberate motion moments per concept page. The reveal system counts as one. When in doubt, no animation.

## 1. Motion tokens (paste into `:root` of every build)

```css
:root{
  --ease-out:cubic-bezier(.23,1,.32,1);        /* entrances, exits, press, hovers */
  --ease-in-out:cubic-bezier(.77,0,.175,1);    /* on-screen movement/morphs (A to B) */
  --ease-drawer:cubic-bezier(.32,.72,0,1);     /* sheets, drawers, bottom bars */
  --dur-press:140ms;   /* button/tile press feedback */
  --dur-pop:170ms;     /* tooltips, small popovers */
  --dur-menu:220ms;    /* dropdowns, selects, accordions */
  --dur-panel:320ms;   /* modals, drawers, mobile nav */
  --dur-reveal:520ms;  /* marketing scroll reveals (max ~700) */
}
```

- **Never use `ease-in` on UI.** It delays the exact moment the user watches.
- Built-in `ease`/`ease-out` keywords are too weak; use the tokens.
- Constant motion (marquee, progress) is the only place for `linear`.
- Hover/color transitions may use plain `ease` (the token --ease-out still reads better in house style; standardize on it).

## 2. Duration table (hard budget)

| Element | Duration |
| --- | --- |
| Press feedback | 100-160ms (house 140) |
| Tooltips, small popovers | 125-200ms |
| Dropdowns, selects, accordions | 150-250ms |
| Modals, drawers, mobile menu | 200-500ms |
| Scroll reveals, hero entry, counters | 400-700ms (marketing, one-time) |
| Marquee / progress / ambient | linear, looped |

UI interactions stay under 300ms. A 180ms menu feels faster than a 400ms menu at identical load cost.

## 3. House snippets (vanilla, no dependencies)

### 3.1 Press feedback (every pressable element, no exceptions)
```css
.btn,.tile,.link-cta{transition:transform var(--dur-press) var(--ease-out),background .2s var(--ease-out),box-shadow .2s var(--ease-out)}
.btn:active{transform:scale(.97)}          /* .95-.98; subtle, physical */
```
Gate hover behind pointer capability (touch screens otherwise fire hover on tap and get stuck):
```css
@media (hover:hover) and (pointer:fine){
  .btn:hover{transform:translateY(-2px)}
}
```

### 3.2 Scroll reveal (the AMK `.rv` standard, values aligned)
```css
.rv{opacity:0;transform:translateY(22px);transition:opacity var(--dur-reveal) var(--ease-out),transform var(--dur-reveal) var(--ease-out)}
.rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  .rv{opacity:1;transform:none;transition:none}
}
```
```js
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}})},{threshold:.12});
document.querySelectorAll(".rv").forEach(function(el){io.observe(el);});
```
- Reveal starts from `translateY` + opacity, never from `scale(0)`. Nothing in the real world appears from nothing; any scale-in starts at **0.92-0.97**.
- **Stagger 30-80ms** between sibling items (house: 60ms). Above ~120ms the page feels slow; stagger is decorative and must never block interaction.
- Use `once` semantics (unobserve), threshold ~.12-.3.

### 3.3 Accordion (FAQ `<details>`)
```css
.faq details{transition:grid-template-rows var(--dur-menu) var(--ease-in-out)}
.faq summary::after{transition:transform var(--dur-menu) var(--ease-out)}
.faq details[open] summary::after{transform:rotate(45deg)}
```
(If animating height: the modern zero-JS pattern is `grid-template-rows:0fr → 1fr`; never animate `height` with JS on main thread.)

### 3.4 Bottom sheet / mobile CTA bar
Slides from its own edge using percentage translate, `--ease-drawer`, 280-360ms:
```css
.sheet{transform:translateY(100%);transition:transform var(--dur-panel) var(--ease-drawer)}
.sheet.open{transform:translateY(0)}
```

### 3.5 Origin-aware menus
Popover/dropdown scales in from its trigger, not from center (modals ARE exempt: they stay centered):
```css
.menu[hidden=false]{transform-origin:var(--origin,top right)}
.menu{transform:scale(.96);opacity:0;transition:transform var(--dur-menu) var(--ease-out),opacity var(--dur-menu) var(--ease-out)}
.menu.open{transform:scale(1);opacity:1}
```

### 3.6 Crossfade that looks wrong = add a blur bridge
When two states swap (language toggle on big headlines, image swap), a 2px blur during the crossfade hides the "two objects overlapping" artifact:
```css
.swap{transition:filter .2s var(--ease-out),opacity .2s var(--ease-out)}
.swap.swapping{filter:blur(2px);opacity:.6}
```
Never exceed `blur(20px)` (Safari cost); use 2-4px.

### 3.7 Counters
Number tickers use `font-variant-numeric:tabular-nums` so digits do not jitter; ease-out over 1000-1400ms, triggered once via IntersectionObserver (our clinic template's pattern is canonical).

## 4. Performance rules
- Animate ONLY `transform` and `opacity`. Never `top/left/width/height/margin/padding` (layout+paint+composite jank).
- Never write `transition:all`. List exact properties.
- No `window.addEventListener("scroll", ...)` for reveals/parallax. IntersectionObserver, CSS `animation-timeline: scroll()` (progressive enhancement), or a library's scroll API only.
- CSS transitions retarget mid-flight; `@keyframes` restart from zero. Anything triggered rapidly (toasts, toggles, language switch) uses **transitions**, not keyframes.
- Predetermined one-shot motion can also use WAAPI (`el.animate([...],{duration,easing,fill:"forwards"})`): JS control, GPU performance.
- `will-change:transform` only on elements that actually animate, never as a blanket rule.
- Grain/noise only on `position:fixed;pointer-events:none` overlays; `backdrop-filter` only on sticky/fixed surfaces.

## 5. Reduced motion (mandatory)
- Every motion above MOTION_INTENSITY 3 honors `prefers-reduced-motion:reduce`.
- Reduced means **gentler, not zero**: keep opacity/color transitions that aid comprehension; remove movement, position changes, parallax, loops and scroll hijack. House block:
```css
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
  .rv{opacity:1;transform:none}
}
```

## 6. Reviewing motion (deliverable format + checklist)

When auditing a page's motion, present findings as a Before/After table (one row per issue):

| Before | After | Why |
| --- | --- | --- |
| `transition:all .3s` | `transition:transform .22s var(--ease-out),opacity .22s var(--ease-out)` | exact properties; off-GPU nothing |
| reveal from `transform:scale(0)` | `translateY(22px);opacity:0` (or scale .95) | nothing appears from nothing |
| `ease-in` on menu | `--ease-out` | ease-in reads as sluggish |
| hover lift on `.btn` | wrap in `@media (hover:hover)` | touch gets stuck hover states |
| 400ms dropdown | 220ms | UI budget is <300ms |
| all cards reveal together | stagger 60ms per sibling | cascade, capped at ~7 items |
| same speed in/out | enter 320ms, exit 180ms | system response snaps |
| keyframe slideIn on toast | transition on a state class | rapid triggers retarget smoothly |
| parallax via scroll listener | IO / CSS scroll-timeline | frame budgets |

Mechanical sweep before delivery:
- grep `transition:\s*all` → zero.
- grep `ease-in` (as entrance) → zero; `linear` only on loops.
- every `.btn`/tile has `:active` press feedback.
- every hover transform lives behind `(hover:hover) and (pointer:fine)`.
- every entrance has a reduced-motion fallback; reveal duration ≤ 700ms; UI ≤ 300ms.
- nothing animates `width/height/top/left/margin/padding`.
- stagger delays 30-80ms; reveal `.rv` count staggered in groups, not 30 items at 200ms each.
- test one pass at 4x slowdown (DevTools Animations panel): do multi-property transitions stay in sync?

## 7. What NOT to animate (rejected list, keep this discipline)
- Language toggle buttons (repeated dozens of times per session): instant swap, optionally a 150ms opacity-only crossfade on page content.
- Sticky nav height/shadow on every scroll frame: one class flip with a 200ms transition, no rAF.
- Price/price-list rows, opening-hours tables, lab panel data: still.
- Section backgrounds as users scroll (constant repaint).
- Anything the user is actively reading.

_Source skills (vendored, MIT): `design/vendor/emil/skills/emil-design-eng/SKILL.md`, `.../animate/`, `.../review-animations/STANDARDS.md`, `.../improve-animations/AUDIT.md`, `.../find-animation-opportunities/SKILL.md`, `.../animation-vocabulary/SKILL.md`, `.../apple-design/SKILL.md`._
