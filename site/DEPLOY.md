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

## Live state to fix (audit 15 Sep 13:30)

- `/sample-secondary.html` — LIVE, already the Cameroon Crestwood build.
- `/` (homepage) — STALE: clinic card still pointed at the dead external
  `demo-cliniques-cm.vercel.app` and showed an old US-template crestwood
  thumbnail (both fixed in the current files + zip).
- `/sample-clinic.html` — **404** (page exists locally, not deployed).
- `/mitoc.html` — **404**; that named preview normally goes via the separate
  throwaway project https://mitoc-concept.vercel.app — deploying it here too is
  fine but it must stay out of the public sitemap.

Do not share the `/sample-clinic.html` link with anyone until its 404 clears.

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

1. `/sample-clinic.html` opens with the hero "Healthcare that answers, day or
   night" (Molyko Medical Centre).
2. The homepage clinic card opens `/sample-clinic.html` inside the project.
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
