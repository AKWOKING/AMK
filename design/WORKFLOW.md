# AMK Build Workflow (site & concept creation pipeline)

_The law: `AMK-DESIGN-SKILLS.md` (repo root). This file is the step-by-step pipeline that applies it, with the vendored skills mapped in. Every site/concept passes through stages 1-9; skipping a stage is allowed only when the brief explicitly removes it (note why in the delivery notes)._

## Stage map
1. Research & verified facts → 2. Design Read → 3. Dials → **3b. Direction exploration (3 directions)** → 4. Family + token sheet → 5. IA & copy (EN|FR) → 6. Image shot-list & generation → 7. Build (single file) → 8. Motion pass → 9. Pre-flight + screenshot QA → handoff.

---

## 1. Research & verified facts (sales feeds design)
- No claim enters a concept without a source: lead dossier (`sales/*Deep-Dives*`, `sales/Clinic-Batch-*.md`) holds verified pain, services, numbers, reviews.
- Pattern examples that change the design:
  - Solidarity: a Google profile WITH 4.0/54 reviews but no website → the concept's job is "attach to the existing reputation", not "make you exist".
  - Baird: dead site → concept implies full replacement.
- Mark every placeholder clearly (nameless template rule; prices/hours/reviews labeled sample/demo).

## 2. Design Read (mandatory one-liner before code)
> "Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <family>."
- Read §1 signals of the root law (page kind, vibe words, references, audience, brand assets, quiet constraints).
- References are hard constraints (Reference-Override Rule §4.4).
- If genuinely ambiguous, ask exactly ONE question; otherwise declare and proceed.

## 3. Dials
Set VARIANCE / MOTION / DENSITY from the root-law §2 presets (school/clinic concept = 6/4/4; agency = 7/6/4; trust-first = 3/2/4-5). Record them in the builder header comment.

## 3b. Direction exploration (mandatory — 30-45 min, root §19.3)
- Write the brief line: audience + the one action + tone.
- Produce **exactly three** distinct directions (blueprint/technical · editorial/broadsheet · warm/minimal, or the three best suited to the vertical), each with its own type pairing and accent. Never accept the first output; never accept a default palette.
- State the avoid-list before generating: purple/violet gradients · neon glow · emoji icons · AI sparkles · overly-rounded "AI" UI · cheap stock 3D · content-hiding fade-ins · Instrument Serif (root §19.3).
- Judge with the zoom-out hierarchy test (§19.2) and the vibe-code tell list (§3.8). Pick one; iterate **variants of the winner only** (font pairing, accent, headline tone).
- Pick the outcome-led headline (root §11b / §19.3.5).
- Only then proceed to stage 4 (token sheet). Record the chosen direction + why in the delivery notes and the ledger.

## 4. Family + token sheet
- Pick a sheet from `design/STYLE-TOKENS.md` by vertical; rotate per the ledger; or pull structure from a bergside family (`design/vendor/bergside-skills/<family>/DESIGN.md` + `design/vendor/registry-digest.json`).
- Lock: colors (1 accent, tinted neutrals), ONE radius system, type ramp (Outfit house), shadow tint, spacing scale.
- Record the chosen family in the ledger at delivery.

## 5. IA & copy (bilingual first)
- Section list BEFORE HTML. Marketing concept default: sticky header (EN|FR toggle) · 24h/trust bar · hero (≤4 text elements) · proof/stats · services bento (exact cell count) · pricing/sample panels · how-it-works (max 3 steps, verb labels) · proof/reviews (only real or labeled sample) · FAQ `<details>` · visit/map · WhatsApp booking · footer + concept badge.
- Write EN and FR together as `data-en`/`data-fr` pairs; build the page so counts can be asserted mechanically (parity test).
- Copy rules: sentence case, active voice, ≤20-word hero subtext, no filler verbs (root §3.6), no em-dashes in EN (hyphens for ranges), one label per CTA intent.
- Conversion plumbing (AMK standard): WhatsApp form payload with ref code (XX-XXXX), `wa.me/<owner number>`, tel links, JSON-LD for the vertical (MedicalClinic/School), demo routing to AMK number until launch.

## 6. Images (art-directed, continuity-locked)
- Shot-list per section (aspect ratio, subject, crop, light, negative space); full rules: root §10 + §15.
- Prompt pack: same world across every image (palette grade, light family, Cameroonian context, no text/watermarks/logos); "no logos, no watermarks, no text on clothing" always.
- **The image must depict the STANDARD we deliver, not the current state of the premises.** The page is a
  comparison piece: the rule is "our demo has to look BETTER than his actual website", and that applies to
  pixels. "Documentary realism" in the brief produces a tired shop and loses the client before he scrolls.
  Ground the local reality OUTSIDE the window (street, light, passers-by), never inside the fit-out.
- **No invented lettering, ever.** Read each render for text on walls, glass, uniforms, screens: a fabricated
  shop name inside a client's mock-up is a false fact in image form — and can spell a competitor's name.
  Re-prompt with "absolutely NO text, no lettering, no logo, no signage"; keep only objects that are tools
  of the trade (a Snellen chart is equipment, a brand plate is not).
- **A caption describes the image it sits under.** If the render changes subject, the caption and alt change in
  the same commit, and say what the client will replace at go-live ("concept render - your photo replaces it").
- Generate → READ each image back (watermark/logo/text scan + "would this hang in a modern Douala practice?")
  → re-generate/crop if dirty → record the read-back in the builder (`IMG_REVIEW` style), because an
  obligation with no machine behind it is an opinion.
- Embed base64 once each (CSS background or `<img>`; never embed the same photo twice), object-fit cover, reserve space (CLS).

## 7. Build (single-file house format)
- One self-contained `.html` in `site/` (concepts) or `demos/` (named previews), generated by a committed `build_*.py` builder so content/translation edits are reproducible.
- Semantic HTML before classes; sections ≥4 layout families across a page; mobile collapse declared per block; check at 390px.
- Components per root §8 (buttons w/ contrast & no-wrap, forms label-above, cards with pinned CTAs, native details, real faces).
- Concept badge + nameless labeling; noindex NOT required on the public sample project (King deploy decision), but never present a nameless template as the client's real business.

## 8. Motion pass (after the page is fully built and correct)
- Run the opportunity gate (`design/MOTION.md` §0): frequency, purpose, speed, function. Expect 5-7 survivors max, list rejects.
- Apply tokens (--ease-out/--ease-in-out/--ease-drawer, durations), `.rv` IO reveal with 60ms stagger, `:active` press scale .97, hover behind `(hover:hover)`, accordions, sheet/bars, tabular counters.
- transform/opacity only; no `transition:all`; no scroll listeners; reduced-motion block.
- **First paint never depends on JavaScript** (root §13; 22/09 lesson): any `opacity:0`/`visibility:hidden`
  entrance state must be scoped under `html.js`, set by an inline `<script>` in `<head>`; the reveal system
  lives in its own `<script>` after the language one, with a `try/catch` that shows everything on failure.
  Hero and section headings do not animate at all: they are what the reader came for.
- Reveal budget: ≤ 40 % of content blocks, ONE authored moment per page (`design/CRAFT-FLOOR.md` §2.5/§3).
- React/Motion/GSAP only in real app stacks (vendored skills cover them); concepts stay vanilla.

## 9. Pre-flight + QA (non-negotiable; the page is not done until all pass)
Root-law §13 matrix, mechanically enforced where possible via a QA script + browser check:
1. `data-en` count == `data-fr` count, zero unpaired; zero EN em-dashes.
2. Builder runs clean; HTML parses; zero unresolved tokens; base64 images deduped.
3. 390px: zero horizontal overflow; header fits one line; hero CTA visible; bottom bar doesn't cover content.
4. All links real (wa.me/tel/mailto/internal), zero `href="#"`.
5. Color/shape/theme locks page-wide; CTA one-label-per-intent; eyebrow count; no AI tells (root §3).
6. Motion: no `transition:all`, press states present, hover media-gated, reduced-motion block, claimed==shown.
7. Lighthouse-minded: LCP image, CLS space reservation, single file size sane (~1MB acceptable).
8. Screenshot QA at 1280×800 + 390×844, EN and FR; capture hero shot to `demos/shots/<name>-concept.png`; mockup when going to a lead.
9. Rebuild `hosting/samples/` (`python3 hosting/build_samples.py`) when `site/` changed; confirm sitemap + index wiring.
10. **First paint without JS** (machine, no browser needed): every hiding rule is `html.js`-gated, the head
   carries the inline `js` setter, and no hero/heading/figure is reveal-gated. Asserted in the builder
   (Univers: checks 15a-e; Cristallin: same block) — an ungated `.rv`/`.reveal` fails the build.
11. **Every inline `<script` compiles**: `python3 tools/qa/check_inline_js.py <file...>` (extracts each block,
   `node --check`, validates JSON-LD separately). `rc=1` → nothing is delivered; `rc=3` (no `node` in the
   sandbox) → the control was NOT rendered and must be written as such in the handoff. Both builders run it
   on the in-memory page before writing, so a broken script never reaches disk.
12. **Send integrity**: a concept goes as a FILE; record `bytes` + `sha256` in the send sheet, and tell the
   reader that a page whose body is missing under the header = a truncated download, ask for the file again.

## Handoff record (delivery notes template)
```
Build: <file> · Builder: <build_*.py> · Design Read: <line> · Dials: V/M/D = x/x/x
Family: <sheet/family + ledger row> · Images: <n, scanned clean> · QA: EN/FR parity <n/n>, 390px clean, console 0, motion gate <kept/rejected list>
Routing: WA <number>, ref prefix <XX-> · Deploy: <url / pending King redeploy>
```

## Skill routing (where to look while working)
| Need | Open |
|---|---|
| Anti-slop rules, locks, pre-flight | `AMK-DESIGN-SKILLS.md` (root) |
| Exact motion values, snippets, review format | `design/MOTION.md` |
| Starting colors/type per vertical | `design/STYLE-TOKENS.md` |
| 67-family structure/tokens | `design/vendor/bergside-skills/<family>/` + `registry-digest.json` |
| Apple-style principles / vocabulary / RN / toasts / animation audits | `design/vendor/emil/skills/*` |
| Full anti-slop long form, block patterns, redesign protocol, brand/logo boards, image-per-section comps | `design/vendor/taste/skills/*` |

## Regarder un dessin sans navigateur (24/09/2026)

Il n'y a **pas de navigateur** dans le bac, et depuis la page de **La Ligne Optic** une page AMK peut
être **entièrement dessinée** (SVG). Ne pas pouvoir regarder ses propres dessins avant de les livrer
serait une faute : `tools/qa/render_svg.py` les rastérise **avec PIL** (le seul moteur disponible),
en surdimensionnant ×3 puis en réduisant pour remplacer l'antialiasing absent.

```
python3 tools/qa/render_svg.py demos/concept-<client>-v1.html --class draw -o /tmp/hero.png --width 420
python3 tools/qa/render_svg.py demos/concept-<client>-v1.html --class mini --all -o /tmp/minis --width 200
```

Il lit les règles de classe de la page — **y compris les variables de `:root`** (sans quoi tout sort
blanc sur blanc) et les **classes posées sur un `<g>`** (sans quoi les groupes sortent incolores). Il ne
fait ni dégradés, ni transformations, ni polices : si un dessin en a besoin, l'étendre, pas le contourner.

## Peser ce qui est embarqué (24/09/2026, soir — La Ligne Optic)

`tools/qa/audit_images.py` ne regardait que les **fichiers** : il ignorait les `data:image/…;base64`. La
page de La Ligne Optic portait **dix images embarquées (249 Ko de JPEG)** et l'outil annonçait
« **0 image(s)** » — un rapport vert sur un contrôle qui n'avait rien regardé. Il décode maintenant
chaque image embarquée, la **pèse** (budget 400 Ko), lit ses **métadonnées** (GPS = ERR) et vérifie le
**ratio annoncé**, exactement comme un fichier. Son témoin : **17 assertions**.

**La règle à retenir** : avant de croire un « 0 constat », vérifier que l'outil **compte** ce qu'il
prétend contrôler. Un contrôle qui ne voit rien et un contrôle qui ne trouve rien se ressemblent.

## Regarder sa propre mise en page sans navigateur (24/09/2026, soir)

Pour la passe 4 du premier écran (un verre, un cadran, un portrait dedans), il n'y a **toujours pas de
navigateur** : la composition a été **remontée à la main en PIL** — mêmes coordonnées que le SVG, mêmes
rayons, la vraie photo — avant d'écrire les nombres dans le gabarit. Deux erreurs vues à l'écran et
corrigées avant tout build : le portrait était **trop petit** dans le verre (192 unités → 224), et le
réticule à croix tombait **sur le nez** (une croix sur un visage, c'est une cible : les repères sont
passés sur la ligne). `clients/la-ligne/dessins-controle.png` garde les deux planches.
