# Deploying the AMK site + nameless samples (`amk-cm.vercel.app`)

The public agency site and the **nameless** samples live in **one existing
Vercel project: `amk-cm`**. Never create a new project for them — the links
shared with prospects (below) are promises about that domain.

`amk-site.zip` (repo root) is a ready snapshot of this folder's deployable
files: the 6 HTML pages, `favicon.svg`, `robots.txt`, `sitemap.xml` and the
four `img/*.png` thumbnails (13 files). The big concept pages embed their
photos as base64, so they need no other assets. Rebuild it deterministically
with `python3 hosting/build_site_zip.py`; smoke-test by unzipping and serving
locally (every page 200, every internal link resolves).

## Live state (audit 15 Sep 14:45)

- `/sample-secondary.html` — LIVE, Cameroon Crestwood build.
- `/clinic-bonaberi.html` — **LIVE from King's manual rename** of the clinic
  concept (Bonabéri Medical Centre, Douala), but that upload is a **partial
  rename**: hero eyebrow still reads "Buea", and nav brand / footer / WhatsApp
  greeting / booking reference still say Molyko / MMC. The canonical
  `clinic-bonaberi.html` in this folder is fully renamed (10 brand points, BMC
  refs, Douala) and replaces that upload on the next deploy.
- `/` (homepage) — STALE: still shows the dead external
  `demo-cliniques-cm.vercel.app` "live demo" card (Concept 04) alongside a
  Bonabéri card; current `index.html` has one clinic card pointing inside the
  project and the regenerated `img/clinic.png` + `img/crestwood.png`.
- `/sample-clinic.html` — removed; **404 is correct now** (renamed to
  `/clinic-bonaberi.html`; do not relink the old URL).
- `/mitoc.html` — 404 here; the named MITOC preview is served from the
  separate throwaway project https://mitoc-concept.vercel.app. Deploying it
  here too is optional and it must stay out of the public sitemap.

Redeploy `amk-site.zip` to make the live clinic page fully consistent and to
clean the homepage; until then the live clinic link opens (eyebrow mismatch
noted) and is usable, but send it with the concept caption that calls every
name a placeholder.

## Option A — Vercel CLI (fastest, matches how the named projects went up)

From a logged-in machine:

```bash
npm i -g vercel
cd site
vercel login                 # one time, King's account
vercel link                  # choose the EXISTING project: amk-cm
vercel --prod --yes          # deploys this folder to amk-cm.vercel.app
```

## Option B — Git integration (push-to-deploy)

1. vercel.app → open project **amk-cm** → Settings → Git → connect
   `AKWOKING/AMK`, Root Directory = `site`, Framework Preset = Other,
   no build command.
2. After that, every push redeploys automatically.

## Option C — Recreate from the zip in the dashboard

Vercel dashboards cannot ingest a zip into an *existing* project; if CLI/Git is
unavailable, Netlify Drop (app.netlify.com/drop) only creates a **new** URL, so
do not use it for `amk-cm` — ask AMK to run Option A instead.

## Verify after every deploy

1. `/clinic-bonaberi.html` opens with the hero "Healthcare that answers, day or
   night" (Bonabéri Medical Centre).
2. The homepage clinic card opens `/clinic-bonaberi.html` inside the project.
3. `/sample-secondary.html` still shows the Crestwood Cameroon build.
4. The four cards' thumbnails render (`/img/nova.png`, `littleoaks.png`,
   `crestwood.png`, `clinic.png`).

## Rebuilding the bundle after site edits

```bash
python3 site/img/process_secondary.py      # if secondary photos changed
python3 site/build_sample_secondary.py     # sample-secondary.html
python3 hosting/build_samples.py           # mirror site/ -> hosting/samples/
python3 hosting/build_site_zip.py          # rebuild amk-site.zip (13 files)
```

The nameless pages are public/indexable; `mitoc.html` is a private named
preview and stays absent from `sitemap.xml`.

— Akwo King / AMK – Web Development & Digital Solutions
