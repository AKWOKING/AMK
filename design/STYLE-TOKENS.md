# AMK Style Token Sheets (project starters)

_Before the first line of HTML, lock ONE token sheet (per `AMK-DESIGN-SKILLS.md` §1-§6). The bergside registry (`design/vendor/bergside-skills/<family>/DESIGN.md`, digest `design/vendor/registry-digest.json`) gives the structural language; the hexes below are AMK-curated because registry defaults are placeholder blue/purple and must never ship as-is._

## How a sheet is used
1. Design Read + dials → pick the vertical sheet, then rotate family per the ledger at the bottom.
2. Copy its `:root{}` block into the builder; every component references variables only (no raw hex in components except the sheet itself).
3. Named client build: replace hues with the client's real brand colors, keep the architecture (contrast pairs, tinted shadows, radius scale).
4. Log the family used in this ledger after delivery so the next project rotates.

## Token architecture (every sheet exposes the same names)
`--ink` body text · `--ink-soft` muted · `--surface` page bg · `--surface-2` raised bg · `--line` hairline · `--brand` / `--brand-bright` (hover) / `--brand-tint` (soft bg) · `--on-brand` text on brand · semantic `--ok/--warn/--danger` + tints · `--radius` (12/16/20 scale, ONE system) · tinted `--shadow` · type ramp via `clamp()` · 4/8 spacing scale · Outfit house font unless the brief names another.
Contrast rule: `--on-brand` on `--brand` and `--ink` on `--surface` both pass WCAG AA 4.5:1; large text 3:1. Verify, don't assume.

---

## A. Clinic / laboratory — Forest (IN USE: clinic-bonaberi.html "Bonabéri Medical Centre")
Registry family: `premium` structure + Forest rotation family. Anxiety-defusing, trustworthy, warm-but-clinical.
```css
--ink:#15201C; --ink-soft:#4E6259; --surface:#F6F3EC; --surface-2:#FFFFFF; --line:#E3DDD0;
--brand:#0E7A5C; --brand-bright:#0A6349; --brand-tint:#E5F0EB; --on-brand:#FFFFFF;
--g900:#114333; --g800:#155642; --g700:#1E6B52;      /* deep forest scale, dark sections */
--bone-2:#EFE8D9; --amber:#C9923B; --amber-tint:#F7EDDB; /* single warm accent, sparse */
--danger:#B5342A; --danger-bright:#9E2B22;             /* emergency */
--radius:16px; --radius-lg:20px;
--shadow:0 18px 40px rgba(17,67,51,.12);
```

## B. Clinic / dental warm — Terracotta + Slate (next warm-premium clinic; never the Odentrics cream/navy)
Registry family: `terracotta`/`cafe` structure. Rotation alternative when Forest was last used.
```css
--ink:#2B211C; --ink-soft:#6A5C52; --surface:#FAF6F1; --surface-2:#FFFFFF; --line:#EAE1D6;
--brand:#C56A3C; --brand-bright:#A8562D; --brand-tint:#F8E7DD; --on-brand:#FFFFFF;
--slate:#3E4A52; --slate-tint:#E6EAEC;                  /* cool counterweight, never blue-purple */
--ok:#3E7A4F; --warn:#B97F2C; --danger:#A83A2E;
--radius:18px; --radius-lg:22px;
--shadow:0 18px 40px rgba(62,74,82,.14);
```

## C. Optic / eye center — Cobalt + Cream (IN USE: mitoc.html, 15 Sep 2026)
Registry family: `clean` + `professional` structure. Precision, clarity, lens-like crispness.
```css
--ink:#10202E; --ink-soft:#46596A; --surface:#F7F5EE; --surface-2:#FFFFFF; --line:#E3E6E4;
--brand:#15539E; --brand-bright:#0F3F78; --brand-tint:#E2ECF7; --on-brand:#FFFFFF;
--accent:#E8A33D; --accent-tint:#FAEFD9;               /* single warm pop, sparse */
--ok:#2E7D5B; --warn:#B97F2C; --danger:#B03A2E;
--radius:16px; --radius-lg:20px;
--shadow:0 18px 40px rgba(16,32,46,.13);
```

## D. Secondary school / college — institutional premium
Registry family: `professional`/`premium`. Crest-driven: derive hues from the real crest on named builds; the nameless template rotates deep, credible colors (never the LLM royal-blue/purple default).
```css
--ink:#1A2033; --ink-soft:#51606F; --surface:#FAFAF7; --surface-2:#FFFFFF; --line:#E6E6E0;
--brand:var(--crest-900,#0F2A47); --brand-bright:var(--crest-800,#0A1E34); --brand-tint:#E7EEF5;
--gold:#B08A3E; --gold-tint:#F3EAD7;                   /* honors/results accent, sparse */
--on-brand:#FFFFFF; --ok:#2E7D5B; --warn:#B97F2C; --danger:#B03A2E;
--radius:14px; --radius-lg:18px;
--shadow:0 16px 36px rgba(15,32,55,.12);
```

## E. Nursery / primary — Friendly
Registry family: `friendly`. Rounded, soft, playful but controlled; one desaturated bright pair, no candy rainbow.
```css
--ink:#27302B; --ink-soft:#5C6B60; --surface:#FCFAF5; --surface-2:#FFFFFF; --line:#ECEADF;
--brand:#3E8F6B; --brand-bright:#327557; --brand-tint:#E3F2EA; --on-brand:#FFFFFF;
--sun:#E2A93B; --sun-tint:#FAF0D9; --berry:#C7657A;            /* tiny pops only */
--ok:#3E8F6B; --warn:#C88A2B; --danger:#B0503A;
--radius:20px; --radius-lg:26px;                      /* rounder system, locked page-wide */
--shadow:0 16px 36px rgba(39,48,43,.10);
```
## F. Day school / generic — Clean
Registry family: `clean`. Maximum legality and speed; warm off-white, one trust accent.
```css
--ink:#1E2428; --ink-soft:#5A666E; --surface:#FAFAF8; --surface-2:#FFFFFF; --line:#E7E8E6;
--brand:#1F5E7A; --brand-bright:#17485E; --brand-tint:#E3EEF3; --on-brand:#FFFFFF;
--ok:#2E7D5B; --warn:#B97F2C; --danger:#B03A2E;
--radius:12px; --radius-lg:16px;
--shadow:0 14px 32px rgba(30,36,40,.10);
```

## G. AMK agency — LOCKED (brand, do not rotate)
```css
--ink:#13202A; --surface:#F7F6F2; --brand:#12324A; --amber:#C8932F; /* navy + amber per current site */
```

---

## Rotation ledger (append after every shipped concept)
| Date | Build | Family / sheet | Notes |
|---|---|---|---|
| 2026-09 | OraCare v3 (named) | Odentrics reference: cream/sand + soft navy + gold + sage | reference-driven, exempt from rotation (§4.4) |
| 2026-09 | SJC Sasse v2 (named) | school institutional w/ chapel photo | named brand |
| 2026-09-15 | **sample-secondary.html (Crestwood) REBUILT** | **D, deep navy + cream + gold** | nameless; Cameroon-localized GCE/boarding/FCFA rebuild (replaced US-style template; 8 concept photos, 152 EN/FR pairs) |
| 2026-09 | sample-school.html (Nova) | F, clean teal-blue | nameless |
| 2026-09 | sample-nursery.html (Little Oaks) | E, friendly green | nameless |
| 2026-09 | **clinic-bonaberi.html (BMC, Bonabéri)** | **A, Forest green + bone + amber** | nameless |
| 2026-09-15 | **mitoc.html (Midas Touch Optic Center)** | **C, Cobalt + Cream, amber sparse** | NAMED preview, builder `site/build_sample_mitoc.py`; send only to MITOC; reference attachment drove page-wide eyebrows (law §4.4) |
| Next clinic | must NOT repeat A → **B Terracotta+Slate** (unless client brand dictates) | | |
| Next optic/eye build | must NOT repeat C → Terracotta+Slate or Olive+Brick+Paper adaptation | | |
