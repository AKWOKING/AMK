# AMK site redesign — research + design decision (13 Sep)

## Sources studied (fetched live 13 Sep)
1. **WebFX** (US, B2B web/marketing — our exact category) — conversion machine.
2. **Lusion** (Bristol/UK, Awwwards studio) — design-language reference.
3. **Obys** (London, Awwwards studio) — portfolio/marquee patterns.
4. **Designmodo** (US, design tools) — stats bands, galleries, persona blocks.
- Sidewell.net, unboxed.io, tandemdigital.com: domains dead/parked (skipped — lesson: check liveness before quoting as reference).

## What works (pattern → where we use it)
| Pattern | Source | AMK application |
|---|---|---|
| One-line positioning, no fluff | WebFX, Lusion | Hero: "judged on Google before parents call" / "your next patient is choosing — right now" |
| Repeated CTA ("Get my Free Proposal") | WebFX | "Free 24h preview" in header, hero, mid-page, footer — 4× |
| Metrics band with big numbers | WebFX, Designmodo | 24h · 3–5 days · 2 languages · 4 concepts (animated counters) |
| Before/after comparison | WebFX | "Old-school site vs what we build" table (kept) |
| Work grid with tag chips + hover | Lusion, Obys | Portfolio cards with real screenshots of our 4 concepts, browser-chrome frames |
| Auto-scroll marquee | Obys, Designmodo | ÉCOLES · CLINIQUES · EN|FR · WHATSAPP-FIRST · cities strip |
| Persona/product tabs | Designmodo | **Niche switcher in hero: Écoles / Cliniques** — equal treatment, swaps H1+sub+preview |
| Scroll cue + reveal on scroll | Lusion | "scroll" cue, IntersectionObserver fade-up reveals |
| Confident closing CTA + playful footer | Lusion | "Ready to be found?" footer block, "Built in Cameroon" |
| Social proof | WebFX | We have NO clients yet → honest proof = live concepts (brand truth, kept as differentiator) |

## Design decisions
- **Dual niche, zero competition:** hero niche switcher (schools/clinics) + portfolio split into "For schools" / "For clinics" rows (3 school cards + 1 live clinic card + 1 "your clinic here" CTA ghost card that balances the row AND converts).
- **Mastery signal:** oversized tight typography, navy/amber brand, floating browser-frame previews, real concept screenshots, smooth reveals, counters, marquee — all vanilla HTML/CSS/JS (no framework, loads fast on 3G — which is itself a selling point).
- **Conversion path:** every viewport ends in a CTA; form stays WhatsApp-first (opens WA with pre-written message); micro-trust under hero CTA (no payment until approval / EN|FR standard / 3–5 days).
- **Constraints kept:** EN|FR paired on every string (data-en/data-fr), brand navy #0F172A + amber #F59E0B, clinic accent green #10B981, founding offer ₣100,000 50/50 (2 slots), no fabricated clients, nameless-template rule for all concepts.
