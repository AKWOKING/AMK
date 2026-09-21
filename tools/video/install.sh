#!/usr/bin/env bash
# AMK — installation de la chaîne vidéo (Chromium headless + Puppeteer).
#
# Pourquoi ce script : le paquet npm `@sparticuz/chromium` **embarque** un Chromium
# compilé pour Linux x64 dans son archive (pas de téléchargement externe — les CDN
# de navigateurs sont bloqués dans la sandbox). Il fournit aussi les couches
# `al2023.tar.br` (libnss3/libnspr4/libexpat) et `fonts.tar.br` que le système n'a pas.
#
# Usage :  bash tools/video/install.sh
# Effet :  installe dans /tmp/amk-video (hors dépôt, ~70 Mo) et vérifie que le moteur démarre.
set -euo pipefail

# chemin du script AVANT tout cd (sinon les chemins relatifs se cassent)
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RT="${AMK_VIDEO_RUNTIME:-/tmp/amk-video}"
echo "▸ dossier d'exécution : $RT"
mkdir -p "$RT"
cd "$RT"

if [ ! -d node_modules/@sparticuz/chromium ]; then
  echo "▸ npm install (puppeteer-core + @sparticuz/chromium)…"
  npm init -y >/dev/null 2>&1 || true
  npm install --no-audit --no-fund puppeteer-core @sparticuz/chromium >/dev/null
fi

# dépendances Python (peuvent disparaître à chaque redémarrage de l'environnement)
python3 - <<'PYCHK' || pip install --break-system-packages -q brotli Pillow numpy imageio-ffmpeg
import brotli, PIL, numpy, imageio_ffmpeg  # noqa
PYCHK

echo "▸ extraction des couches embarquées (brotli + tar)…"
python3 - "$RT" <<'PY'
import brotli, tarfile, io, os, shutil, sys
rt = sys.argv[1]
pkg = os.path.join(rt, 'node_modules', '@sparticuz', 'chromium', 'bin')
for layer, dest in [('al2023.tar.br', 'al2023'), ('fonts.tar.br', 'fonts'), ('swiftshader.tar.br', 'swiftshader')]:
    src = os.path.join(pkg, layer)
    if not os.path.exists(src):
        print(f"   ⚠ couche absente : {layer}"); continue
    out = os.path.join(rt, dest)
    if os.path.isdir(out) and os.listdir(out):
        print(f"   = {layer} déjà extrait"); continue
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(brotli.decompress(open(src, 'rb').read()))) as t:
        t.extractall(out)
    print(f"   ✓ {layer} → {out}")
# fonts.conf fourni attend /tmp/fonts — on le satisfait
fd = os.path.join(rt, 'fonts', 'fonts')
if os.path.isdir(fd):
    shutil.rmtree('/tmp/fonts', ignore_errors=True)
    shutil.copytree(fd, '/tmp/fonts')
    print("   ✓ polices installées → /tmp/fonts")
PY

echo "▸ vérification du moteur (lancement réel + capture d'une page de test)…"
export LD_LIBRARY_PATH="$RT/al2023/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export FONTCONFIG_PATH="$RT/fonts"
node "$HERE/capture.mjs" --url "data:text/html,<body style='margin:0;background:%23101838;color:%23fff;font:700%2056px%20sans-serif;padding:48px'><div style='color:%2323C4B1;font:600%2026px%20sans-serif;letter-spacing:2px'>AMK%20VIDEO%20ENGINE</div><h1>Moteur%20pr%C3%AAt.</h1><div%20style='height:1400px'></div><p>bas%20de%20page</p></body>" \
  --out "$RT/verify" --mode scroll --duration 3 --wait 300
echo "   ✓ moteur vérifié ($RT/verify)"

cat <<EOF

▸ PRÊT. Avant chaque session (les variables ne survivent pas au redémarrage) :
    export LD_LIBRARY_PATH="$RT/al2023/lib"
    export FONTCONFIG_PATH="$RT/fonts"

  Capture :   node tools/video/capture.mjs --url file:///.../page.html --out /tmp/frames --mode scroll --duration 12
  Montage :   python3 tools/video/compose.py --frames /tmp/frames --out clip.mp4 --lang fr --eyebrow "..." --hook "..."
  Portique :  python3 tools/qa/audit_video_motion.py clip.mp4      # doit dire OK
EOF
