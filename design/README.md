# design/ — AMK design skills workspace

The governing law remains **`/AMK-DESIGN-SKILLS.md`** at the repo root (read it first; its §13 pre-flight gates every delivery). This folder holds the upstream skill libraries (vendored, MIT) and the AMK-written playbooks that operationalize them in our vanilla single-file workflow.

## AMK playbooks (read for every build)
| File | Use at stage |
|---|---|
| `WORKFLOW.md` | End-to-end pipeline: research → design read → dials → tokens → copy → images → build → motion → QA → handoff, with a handoff-record template |
| `STYLE-TOKENS.md` | Locked starting `:root` sheets per vertical (clinic/lab, optic, secondary, nursery, day school, agency) + the palette rotation ledger |
| `MOTION.md` | Exact motion tokens, durations, vanilla snippets, the four-question opportunity gate, and the Before/After review table |
| `CRAFT-FLOOR.md` | Quality floor distilled 15 Sep from Impeccable (Bakaus), Anthropic frontend-design, UI/UX Pro Max: surface modes, 10 built-result checks, refuse list with AMK market exceptions, two-pass self-critique (squint/personas), a11y/schema gates, vertical grounding decisions |

## Vendored upstream skills (all MIT, licenses alongside)
- `vendor/bergside-skills/` — **bergside/awesome-design-skills**, 67 design-system families (`<family>/SKILL.md` agent rules + `DESIGN.md` token sheet). Programmatic digest: `vendor/registry-digest.json` (67 parsed token sets).
- `vendor/emil/skills/` — **emilkowalski/skills** (Emil Kowalski, ex Vercel/Linear): `emil-design-eng` (master craft rules), `animate`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `animation-vocabulary`, `apple-design`, `prototype`, `pick-ui-library`, plus `animate-expo`/`write-swift` for native (reference only; AMK builds are web).
- `vendor/taste/skills/` — **Leonxlnx/taste-skill**: `taste-skill` (the anti-slop master the root law derives from), `redesign-skill`, `output-skill`, `brandkit`, `imagegen-frontend-web/mobile`, `image-to-code-skill`, `stitch-skill`, soft/minimalist/brutalist variants.
- Licenses: `vendor/LICENSE-bergside`, `vendor/LICENSE-emil`, `vendor/LICENSE-taste`.

## Updating the vendored set
```bash
# from a machine with network (skills are text; no build step)
# 1. refresh a clone, 2. rsync its skills/ over vendor/<name>-..., 3. regen the digest:
python3 - <<'PY'
import json,re,pathlib,yaml
root=pathlib.Path("vendor/bergside-skills"); out={}
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    e={}; dm=d/"DESIGN.md"
    if dm.exists():
        t=dm.read_text(errors="ignore"); m=re.match(r"^---\n(.*?)\n---",t,re.S)
        if m: e["tokens"]=yaml.safe_load(m.group(1))
    sm=d/"SKILL.md"
    if sm.exists():
        t=sm.read_text(errors="ignore")
        mm=re.search(r"description:\s*(.+)",t)
        if mm: e["description"]=mm.group(1).strip()
    if e: out[d.name]=e
pathlib.Path("vendor/registry-digest.json").write_text(json.dumps(out,indent=1,ensure_ascii=False))
PY
```
Upstream references used when integrating (2026-09-15):
- https://github.com/bergside/awesome-design-skills
- https://github.com/emilkowalski/skills
- https://github.com/Leonxlnx/taste-skill
