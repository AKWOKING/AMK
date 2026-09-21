# AMK — PRE-FLIGHT PROTOCOL (standing rule, King 17 Sep 2026)

**The rule: no task begins without a pre-flight.** Identify the task type → load the lessons for that field from this repo → read them → only then start work. Work that skips the pre-flight is invalid.

**Every task response opens with one line:**
`Pre-flight: [task type] → loaded [folders/files]`
If a folder/file is missing, empty or unreadable → say so in that line and either proceed with a stated gap or stop and ask. Never skip silently.

---

## 1 · Routing table (King's fields → the actual files in this repo)

The rule names abstract folders; these are where the lessons actually live. Load **all** relevant rows when a task spans several types.

| Task type | Load these (repo paths) |
|---|---|
| **Marketing / outreach copy** | `research/YouTube-Lessons.md` (entries [1]–[6] copy, [10][13] design-of-copy) · `sales/Monday-Outreach-Pack.md` (**COPY CRAFT GATE** + templates) · `sales/AMK-Sales-Playbook-v2.md` (Parts H, I) · niche: `sales/research/*deep-dive*.md`, `sales/Deep-Dive-Research.md`, `sales/RESEARCH-STANDARD.md` |
| **Prospecting / qualifying** | `sales/AMK-Sales-Playbook-v2.md` (Parts A, B, D, E, H, J) · `research/YouTube-Lessons.md` [7][8] · **`sales/RESEARCH-STANDARD.md` (incl. §8b three-door pre-send gates — every send, every time)** · niche: `sales/Deep-Dive-Research.md`, `sales/Remote-Sweep-*.md`, `sales/Walk-In-*.md` · state: `sales/Pipeline-Status.md` |
| **Presenting / proposals** | `sales/AMK-Sales-Playbook-v2.md` (Parts C, E, F, I, J) · `sales/Monday-Outreach-Pack.md` · `AMK-DESIGN-SKILLS.md` §11b + §19 · `sales/swipe/README.md` |
| **Closing / objection handling** | `sales/AMK-Sales-Playbook-v2.md` (Part I = 3A reframe, Part J = CLOSER, Part E = flips, Part C = closes) · `research/YouTube-Lessons.md` [7][8] |
| **Any copywriting** | `research/YouTube-Lessons.md` [1]–[6] (+ [5] Harry Dry = the law) · `sales/Monday-Outreach-Pack.md` COPY CRAFT GATE · `AMK-DESIGN-SKILLS.md` §11 + §11b · `sales/swipe/README.md` · client's own words (FB/comments) per Part H |
| **Visual design (mockups, brand, graphics)** | `AMK-DESIGN-SKILLS.md` (§1–§19: dials, anti-slop §3, locks §4, type §5, colour §6, layout §7, components §8, motion §9, images §10, copy-law §11b, redesign §12, pre-flight §13, style menu §14, image art-direction §15, patterns §17, §19 foundations) · `design/WORKFLOW.md` · `design/STYLE-TOKENS.md` · `design/MOTION.md` · `design/vendor/*` (registries) · `clients/_uniqueness-registry.md` |
| **Website build** | All of the design row **plus** `AMK-DESIGN-SKILLS.md` §18 (spec-before-build, value provenance, verification ladder) + §19.3 (3-direction exploration) · copywriting row · `design/WORKFLOW.md` stages 1–9 · deploy gate `hosting/previews/README.md` · client context: `sales/research/<client>-deep-dive-*.md` + `clients/<client>/*` · **live inspiration research (step 3 of the uniqueness protocol)** |
| **Delivery / handoff** | `AMK-DESIGN-SKILLS.md` §13 (pre-flight) + §18.4 (verification ladder) · `hosting/previews/README.md` (deploy gate) · `site/DEPLOY.md` · `sales/AMK-Playbook-Addendum-Outcomes-2026-09-15.md` (handoff video, care plan) |
| **Retention / upsell / referrals** | `sales/AMK-Sales-Playbook-v2.md` (A5 referral, F6, Part J reinforce-the-decision) · `sales/AMK-Playbook-Addendum-Outcomes-2026-09-15.md` · `sales/AMK-Playbook-Addendum-4-Marketing-Systems-2026-09-15.md` (monthly report, GBP layer) |
| **Weekly research** | The field being studied → log the output back into that field's lessons: sales/marketing → `sales/research/<YYYY>-W<WW>-techniques.md`; video lessons → `research/YouTube-Lessons.md`; design/build → the relevant `AMK-DESIGN-SKILLS.md` section |

| **CRM / pipeline** | `leads/build/crm.py` (schéma + énumération des étapes — C'EST LUI LA SOURCE, pas le CSV) · `leads/CRM.csv` (état) · `sales/Activity-Log.md` (chronologie, append-only) · `sales/AMK-Sales-Playbook-v2.md` (règles debout, §A4 corrigé) · vue live : `leads/PIPELINE.md`, `leads/KILL-LIST.md`, `leads/STALE.md`, `leads/SOURCES.md`, `leads/Daily-Plan.csv` (toutes GÉNÉRÉES) · fiche d'un lead : `leads/records/<slug>.md` |

**Règle d'écriture du CRM (M7, 21 Sep 2026) — « la prose ne suffit pas ».** Une décision qui
doit changer un calcul (`parked`, un score, un `reply_type`) se met **dans le générateur**
(`leads/build/crm.py`), jamais seulement dans un `.md` : COMOBIL était annoncé « parké » dans trois
fichiers et restait `prospect` dans les données, donc la kill list déduite le remettait en tête.
Une correction manuelle dans `CRM.csv` est **perdue** au prochain `leads/build/rebuild.sh` —
c'est voulu. La chronologie, elle, va dans `sales/Activity-Log.md` (une ligne par envoi, une ligne
par réponse) et remonte toute seule dans les fiches et les vues.

**State files to load with almost everything:** `sales/Pipeline-Status.md` (current week), the prospect dossier, `sales/Outreach-Pack-<date>.md` (active pack), session memory.

---

## 1b · Porte technique obligatoire avant toute livraison (17 Sep 2026)

```
python3 tools/qa/audit_html.py <fichier-construit>      # doit finir sur « TOTAL confirmed findings: 0 »
```
Contrôle **structure** (sections imbriquées, équilibre) + **contraste WCAG** de chaque texte (desktop et mobile). Motif : un `</div>` perdu en insérant le miroir opticien a rendu du texte blanc sur fond blanc (déclaré par King). Détail : `tools/qa/AUDIT-2026-09-17.md`.

## 2 · Uniqueness protocol (every website/design build, before a line of HTML)

1. Load design + copywriting lessons (routing table rows above) and re-read `AMK-DESIGN-SKILLS.md` (dials §2, Design Read §1, anti-default §3/§3.8, pre-flight §13, §19).
2. Load client context — everything we know: brief, niche, what they actually do, who they serve, tone, existing brand assets, intake notes (dossiers in `sales/research/`, `clients/<client>/`).
3. **Go online for live inspiration — never from memory.** At least **3 distinct references from different angles** (structure/layout · colour-typography · imagery/motion/tone), from Awwwards, Godly, Land-book, SiteInspire, Mobbin, Lapa Ninja, Dribbble, or adjacent-market school/clinic sites. For each: **URL · what we take (specifically) · what we reject.**
4. **Check `clients/_uniqueness-registry.md`** and `demos/` — if the direction resembles something we already built, throw it out and re-research.
5. **Write the Design Read line** (dials + inspiration direction + how it ties to this client). No build starts without it.
6. **Differentiate on ≥ 4 axes:** layout · palette · typography · imagery treatment · section order · motion · copy tone. Colours alone = a reskin, not a site.
7. Build per house standard: single-file HTML, base64 images, mobile-first, EN|FR pairs, WhatsApp-first CTAs.
8. Run §13 pre-flight before delivery.

**Web-access fallback:** if live research is impossible (no network / fetch fails), **say so immediately** and propose: King pastes screenshots · work from a curated file · defer the build. Never invent "inspiration" from memory and call it research.

## 3 · Per-client logging (non-negotiable)

- `clients/<client-name>/inspiration.md` — every reference: URL, taken, rejected, plus the Design Read line.
- `clients/<client-name>/build-notes.md` — decisions: dials, why this layout/palette/copy angle.
- `clients/_uniqueness-registry.md` — one line per delivered site: client · niche · dominant fingerprint (layout archetype + palette family + type system + tone).

## 4 · Lesson-update discipline

- A task that teaches something (a tactic that worked, a reference that landed, a copy angle, a design move) → **append a dated entry** to the relevant lessons file the same day, naming the client/task. Don't wait for Monday.
- **Never overwrite a lesson silently** — add, annotate or version (same rule as the playbook).
- **Conflicts:** say so; ask which side wins, unless the newer lesson is clearly stronger for Cameroon clinics/schools — then propose the change and wait for King's yes.

## 5 · Standing lens (everything filters through this)

WhatsApp-first · mobile-first · EN|FR · Cameroon (Kumba/Douala/South-West) · clinics & schools · one client closed by 30 Sep · 500 000 FCFA/month by month 6. A lesson that doesn't serve this doesn't get applied.
