# AMK shot pipeline — hero capture + laptop/phone mockups

Produces the house-style 1920×1080 concept mockup (eyebrow dot, title, tagline,
"Concept by AMK" pill chip, laptop with overlapping phone, gold sparkles)
modelled on `demos/shots/oracare-mockup.png`, plus raw 1280×800 desktop and
390×844 (DSF 2) mobile hero shots. Standard documented in
`demos/shots/README.md` and `AMK-DESIGN-SKILLS.md` §13.

- `lib.js` — `launch()` (puppeteer-core + `@sparticuz/chromium`),
  `captureHero(browser, fileURL, name, outdir)`, `composeMockup(browser, cfg, outPath)`.
- `run.js` — job list for the current concepts (`sample-secondary.html`,
  `mitoc.html`, `sample-clinic.html`). Add a job per concept; colours/eyebrow/
  title/tagline per concept live there.
- `woff2ttf.js` — zero-dependency WOFF1→TTF decoder (zlib inflate + sfnt
  rebuild), used to install a system emoji font for headless.

## Install

```bash
cd tools/shots
npm install
node woff2ttf.js node_modules/@fontsource/noto-color-emoji/files ~/.fonts   # emoji in headless
```

### Minimal Linux without NSS/NSPR (e.g. locked-down sandbox)

`@sparticuz/chromium` needs libnss3/libnspr4. If apt is unavailable, build them:

```bash
git clone --depth 1 https://github.com/mozilla/nspr.git /tmp/nssbuild/nspr
git clone --depth 1 https://github.com/mozilla/nss.git  /tmp/nssbuild/nss
pip install ninja
git clone https://github.com/nodejs/gyp-next.git /tmp/gyp-next && pip install /tmp/gyp-next
cd /tmp/nssbuild/nss && bash build.sh --nspr --disable-tests --gcc -j 4
# a late signtool failure on missing zlib.h is harmless — the needed .so files
# (libnss3, libnssutil3, libnspr4, libplc4, libplds4, libsmime3, libssl3,
#  libsoftokn3, libfreebl3, libsqlite3) finish first under dist/Debug/lib
export LD_LIBRARY_PATH="/tmp/nssbuild/dist/Debug/lib:$LD_LIBRARY_PATH"
```

## Run

```bash
node run.js                 # all jobs
node run.js secondary       # one job  -> out/mockup-secondary.png
```

Promote a composed mockup to the committed deliverables folder when it accompanies a send,
and make the WhatsApp-send JPEG (1600 long edge, ~160-180 KB, avoids WA recompression mush):

```bash
cp out/mockup-secondary.png ../../demos/shots/
python3 - <<'EOF'
from PIL import Image
for name in ["secondary","clinic","mitoc"]:
    im = Image.open(f"../../demos/shots/mockup-{name}.png").convert("RGB")
    im.resize((1600, 900), Image.LANCZOS).save(
        f"../../demos/shots/mockup-{name}-wa.jpg", quality=88, optimize=True, progressive=True)
EOF
```

## Notes / gotchas

- Headless Chromium has **no emoji font** — without the `~/.fonts` step the
  graduation cap / phone / WhatsApp glyphs render as tofu boxes. Real phones
  render them natively; this only affects screenshots.
- `@fontsource/outfit` woff2 files are loaded into the composition page via
  `file://` `@font-face` (Google Fonts is unreachable in the sandbox); do not
  switch the composer back to a remote stylesheet.
- Desktop viewport is 1280×860 clipped to 1280×800; mobile 390×844 DSF2;
  `.demobar` is hidden at capture time.
- Mockup frame geometry matches `oracare-mockup.png`: laptop screen at
  x276/y256 (inner screen 1096×700), shelf to y1033, phone 297×589 overlapping
  the laptop's right edge at x1406/y366.
- Never screenshot named content into public/nameless assets; named previews
  follow the isolation rules (e.g. `mitoc.html` mockup stays private to that
  prospect).
