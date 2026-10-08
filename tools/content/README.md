# tools/content — rendu des carrousels Instagram

- `render_carousels.py` : lit `content/carousels/carousels.json` (source unique du texte) → `content/carousels/<id>/slide-N.png` (1080×1350) + `content/carousels/POST-READY.md`. Contrôles intégrés : glyphes présents, texte dans le cadre, contraste ≥ 4,5, ≤ 7 slides.
- `capture_sample_mobile.mjs` : capture mobile (390×844, ×2) d'une page de démonstration avec bascule FR. Usage (après `bash tools/video/install.sh`) : `cd /tmp/amk-video && export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib FONTCONFIG_PATH=/tmp/amk-video/fonts && node capture_sample_mobile.mjs file:///…/site/sample-secondary.html /tmp/out.png 390 844` (copier le script dans `/tmp/amk-video` : il importe `puppeteer-core`).
- Les deux captures utilisées sont des pages **fictives et étiquetées** (MboaCare, Crestwood College) : jamais une page de prospect ou de client.
