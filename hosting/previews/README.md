# AMK — Client preview hosting (King self-hosts)

This folder is a **drag-and-drop deploy bundle**. Every concept is a single self-contained `index.html` (base64 images, no local assets), so any static host works.

## URLs after deploy (example project name: `amk-previews`)

| Slug | LIVE link | Lead | Canonical source file |
|---|---|---|---|
| **separate Vercel project** | ✅ **https://oracare-concept.vercel.app/** (live 14 Sep, verified v3: prices + assistant) | OraCare237, Buea | `demos/concept-oracare-v3.html` |
| **separate Vercel project** | ✅ **https://sjc-sasse-concept.vercel.app/** (live 14 Sep, verified email-patched build) | SJC Sasse, Buea | `demos/sjc-sasse-v2.html` |
| `/comobil/` (this bundle, when deployed) | `https://amk-previews.vercel.app/comobil/` | COMOBIL — PARKED 14 Sep; deploy only on revival | `demos/concept-comobil-v1.html` |
| `/sah/` (this bundle, when deployed) | `https://amk-previews.vercel.app/sah/` | SAHISCOL — PARKED 14 Sep | `demos/concept-sahiscol-v1.html` |
| `/` | private marker, deliberately no links | — | — |

**Current model (King, 14 Sep):** one Vercel project per named concept, deployed from the canonical HTML (index.html at project root). To push an update: overwrite that project's root index.html with the rebuilt canonical file and redeploy. The `build_previews.py` bundle remains available as a single-project multi-slug alternative for future batches.

All four carry `noindex,nofollow` (private previews, never search-listed). Rebuild after editing any concept:

```bash
python3 hosting/build_previews.py
```

## Hosting priority (14 Sep 2026)

**Deploy today, before anything else:**
1. **`/oracare/`** — the only live conversation; Dr. Nkafu was already promised the preview today. This is v3: FCFA prices **and** the 24/7 assistant (his sent message promised both).
2. **`/sasse/`** — needed for the TikTok DM + email going out today.
3. **`/comobil/`** — have it live before the Messenger "oui" so the link goes back within the hour.
4. **`/sah/`** — deploy after King's phone check of sahiscol.org (do not send the school the link until the check).

**Next, agency-facing (separate project/domain):**
5. The whole **`site/`** folder (agency homepage + the three nameless templates Nova / Little Oaks / Crestwood) → the AMK domain / `amk-cm.vercel.app`. That is public and indexable; do NOT add noindex there.
6. The clinic switcher demo already referenced as `demo-cliniques-cm.vercel.app` — its source is not in the repo; keep that deployment as-is or drop its folder into the repo so v3 can replace its OraCare variant.

**Do not host publicly:** `concept-la-retraite-v1.html` (lead parked; hold), v1/v2 OraCare files (superseded by v3), `sjc-sasse-homepage.html` (v1 draft).

## Option A — Vercel from GitHub (recommended)
1. Push the repo; on vercel.app → **Add New → Project** → import AKWOKING/AMK.
2. Set **Root Directory** = `hosting/previews`, Framework Preset = **Other**, Build Command = none, Output = `public` is not needed (leave defaults).
3. Deploy. Rename the project (Settings → Domains) to something plain like `amk-previews`.
4. Re-deploy is automatic on every push after `python3 hosting/build_previews.py` is run and committed.

## Option B — Vercel CLI (fastest, no Git settings)
```bash
npm i -g vercel
cd hosting/previews
vercel            # preview URL
vercel --prod     # production URL after checking
```

## Option C — Netlify Drop (no account setup friction)
Go to app.netlify.com/drop and drag the **`hosting/previews`** folder. Subfolder links then read `https://<random>.netlify.app/oracare/` (rename the site in site settings).

## Sending rules
- Send the **subfolder link**, never the raw GitHub URL.
- On the client's own domain after close: site goes to a folder/project in THEIR name, domain registered in THEIR name (internal checklist rule).
- Re-shoot `demos/shots/oracare-v3-*` once v3 is live (the existing shot shows v2 without the assistant FAB).
- HTTPS and mobile viewport already work on all these hosts; the links open full-screen on a phone, which is the whole pitch.

— Akwo King / AMK – Web Development & Digital Solutions
