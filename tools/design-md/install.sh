#!/usr/bin/env bash
# AMK — design-md-chrome, installé pour son **extracteur**, pas pour son extension.
#
# Amont : https://github.com/bergside/design-md-chrome (MIT), épinglé ci-dessous. Le dépôt n'en garde
# rien : il est cloné dans /tmp, à côté du Chromium de la chaîne vidéo. L'extension elle-même n'est pas
# installée — on réutilise son `content-script.js` et ses générateurs depuis `extract.mjs`.
#
# Usage : bash tools/design-md/install.sh
set -euo pipefail

PIN="8e07614fb18752ab1ee14dd65a8ff93e63c9b13b"     # 23/10/2026
DEST="${AMK_DESIGNMD_SRC:-/tmp/amk-designmd/src}"
RUNTIME="${AMK_VIDEO_RUNTIME:-/tmp/amk-video}"

if [ ! -d "$DEST/.git" ]; then
  mkdir -p "$(dirname "$DEST")"
  git clone -q https://github.com/bergside/design-md-chrome.git "$DEST"
fi
git -C "$DEST" fetch -q origin "$PIN" 2>/dev/null || true
git -C "$DEST" checkout -q "$PIN"
[ "$(git -C "$DEST" rev-parse HEAD)" = "$PIN" ] || { echo "✗ mauvais commit"; exit 1; }

# L'extracteur tourne dans le Chromium embarqué : il doit déjà être installé.
if [ ! -d "$RUNTIME/node_modules/puppeteer-core" ]; then
  echo "✗ Chromium absent — lancer d'abord : bash tools/video/install.sh"; exit 1
fi

for f in content-script.js lib/normalize.mjs lib/generate-design-md.mjs lib/generate-skill-md.mjs lib/validate.mjs; do
  [ -f "$DEST/$f" ] || { echo "✗ fichier amont manquant : $f"; exit 1; }
done

echo "design-md OK — extracteur amont intact (pin ${PIN:0:7})"
echo "  extraire : python3 tools/design-md/extract.py <dossier-ou-url> [--name \"Marque\"]"
