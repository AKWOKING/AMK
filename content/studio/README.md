# AMK — MboaCare Demo Studio

**Status 17 Sep 2026: ⛔ the studio files were not received.** This folder is the destination; nothing here is invented.

## Expected inventory (King's 17 Sep brief)

| File | Purpose |
|---|---|
| `Website_Demo_Studio.html` | the studio itself — the demo environment used to stage website shots |
| `before.html` | the "bad example" page (deliberately believable, not a parody) |
| `after.html` | the "good example" page (real AMK quality) |
| `clinic-reception.jpg` | photo asset used inside the demo (hero/feel frame) |
| `s1_hook.png` | frame/reference from Video 1's hook (also used as character-art reference) |
| `timeline.json` | the render/edit timeline definition — needed to reproduce the previous chat's renders |

## On arrival — do this (then log in `content/pipeline/CONTENT-PIPELINE.md`)

1. **Verify each file opens** (open the HTML files locally, decode the images, parse the JSON) — report what was checked.
2. **Reconcile fingerprints** — palette hexes + fonts + host art against `content/assets/ASSETS.md`; log any conflict, overwrite nothing.
3. **Capture the studio at 15fps** (per the production rule) for any re-render; compose at 30fps.
4. **Diff `before.html`/`after.html` against our live concepts** — if the "bad example" resembles a real prospect's site, anonymise further (accuracy law: label fiction as fiction).
5. **Note the provenance of `timeline.json`** — which video it belongs to (likely #1) so previous deliverables stay reproducible and untouched (never edit in place).

## Constraints
- The studio is **one asset among several** (`content/lessons/CONTENT-LESSONS.md` §4): right when a video teaches a problem in the abstract. Not the default for every video.
