#!/usr/bin/env bash
# AMK — install HyperFrames (moteur vidéo HTML→MP4) dans le bac à sable.
#
# Pourquoi ce script existe : /tmp est effacé à chaque redémarrage, et HyperFrames
# ne s'installe PAS tout seul ici (deux obstacles testés le 19/09/2026) :
#   1. `onnxruntime-node` (voix Kokoro) télécharge un binaire GPU depuis github.com
#      → « unable to verify the first certificate ». On n'a pas besoin de leur voix
#      (King a tranché : voice-00 de la plateforme) → `--ignore-scripts` suffit.
#   2. Le modèle par défaut charge GSAP depuis cdn.jsdelivr.net → connexion fermée.
#      On vends GSAP localement (et c'est déjà notre règle : aucun appel externe).
#
# Ce que fait ce script :
#   · installe hyperframes (sans scripts), ffprobe (paquet npm) et gsap
#   · écrit /tmp/amk-hf/env.sh, à sourcer avant tout appel hyperframes
#   · vérifie le rendu par un MP4 de test 1080×1920
#
# Usage :  bash tools/video/install_hyperframes.sh
# Ensuite : source /tmp/amk-hf/env.sh && hf render

set -uo pipefail

HF_HOME="${HF_HOME:-/tmp/amk-hf}"
VIDEO_RT="${AMK_VIDEO_RUNTIME:-/tmp/amk-video}"
HF_VERSION="${HF_VERSION:-0.8.50}"

echo "▸ HyperFrames → $HF_HOME"

# 0 · le moteur vidéo AMK doit exister (chromium + ffmpeg viennent de là)
if [ ! -d "$VIDEO_RT/node_modules" ]; then
  echo "▸ moteur AMK absent → installation"
  bash "$(dirname "$0")/install.sh" >/dev/null 2>&1 || {
    echo "✗ install.sh a échoué — lancez-le à la main pour voir l'erreur"; exit 1; }
fi

mkdir -p "$HF_HOME" && cd "$HF_HOME"

# 1 · hyperframes, scripts bloqués (onnxruntime GPU)
echo "▸ npm install hyperframes@$HF_VERSION (--ignore-scripts)…"
npm init -y >/dev/null 2>&1 || true
npm install --ignore-scripts --no-audit --no-fund "hyperframes@$HF_VERSION" >/tmp/hf-npm.log 2>&1 || {
  echo "✗ npm install a échoué :"; tail -15 /tmp/hf-npm.log; exit 1; }

# 2 · ffprobe (paquet npm, binaire statique) — hyperframes en a besoin pour lire les médias
echo "▸ ffprobe…"
npm install --no-audit --no-fund @ffprobe-installer/ffprobe >>/tmp/hf-npm.log 2>&1 || {
  echo "✗ ffprobe a échoué"; exit 1; }

# 3 · GSAP local (le CDN est injoignable ici, et notre règle est zéro appel externe)
echo "▸ gsap (local)…"
npm install --no-audit --no-fund gsap >>/tmp/hf-npm.log 2>&1 || true

CHROME="$(node --input-type=module -e "
import {createRequire} from 'module'; import {pathToFileURL} from 'url';
const require=createRequire('file://$VIDEO_RT/');
const {default:c}=await import(pathToFileURL('$VIDEO_RT/node_modules/@sparticuz/chromium/build/index.js').href);
console.log(await c.executablePath());
" 2>/dev/null)"
FFMPEG="$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null)"
FFPROBE="$HF_HOME/node_modules/@ffprobe-installer/$(node -p "require('@ffprobe-installer/ffprobe').platform + '-' + require('@ffprobe-installer/ffprobe').arch" 2>/dev/null)/ffprobe"

[ -x "$CHROME" ]  || { echo "✗ chromium introuvable ($CHROME)"; exit 1; }
[ -x "$FFMPEG" ]  || { echo "✗ ffmpeg introuvable ($FFMPEG)"; exit 1; }
[ -x "$FFPROBE" ] || FFPROBE="$(find "$HF_HOME/node_modules/@ffprobe-installer" -name ffprobe -type f | head -1)"
[ -x "$FFPROBE" ] || { echo "✗ ffprobe introuvable"; exit 1; }

cat > "$HF_HOME/env.sh" <<EOF
# AMK — environnement HyperFrames (généré le $(date '+%Y-%m-%d %H:%M'))
export HYPERFRAMES_BROWSER_PATH="$CHROME"
export HYPERFRAMES_FFMPEG_PATH="$FFMPEG"
export HYPERFRAMES_FFPROBE_PATH="$FFPROBE"
export HYPERFRAMES_SKIP_SKILLS=1
export LD_LIBRARY_PATH="$VIDEO_RT/al2023/lib"
export FONTCONFIG_PATH="$VIDEO_RT/fonts"
export HF_HOME="$HF_HOME"
hf() { node "$HF_HOME/node_modules/hyperframes/bin/hyperframes.mjs" "\$@"; }
EOF

# shellcheck disable=SC1090
source "$HF_HOME/env.sh"

# 4 · télémétrie coupée (travail client = pas d'envoi d'usage)
hf telemetry disable >/dev/null 2>&1 || true

echo "▸ vérification : rendu d'un MP4 de test 1080×1920…"
TEST="$HF_HOME/selftest"
rm -rf "$TEST" && mkdir -p "$TEST" && cd "$TEST"
hf init selftest --example blank --resolution portrait --non-interactive >/dev/null 2>&1 || {
  echo "✗ init a échoué"; exit 1; }
if [ -f selftest/index.html ]; then
  sed -i 's#https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js#vendor/gsap.min.js#' selftest/index.html 2>/dev/null || true
  mkdir -p selftest/vendor
  cp "$HF_HOME/node_modules/gsap/dist/gsap.min.js" selftest/vendor/ 2>/dev/null || true
  ( cd selftest && hf render >/tmp/hf-render.log 2>&1 )
  MP4="$(find selftest/renders -name '*.mp4' 2>/dev/null | head -1)"
  if [ -n "$MP4" ]; then
    echo "✓ HyperFrames opérationnel — MP4 de test : $TEST/$MP4"
  else
    echo "✗ le rendu a échoué :"; tail -12 /tmp/hf-render.log; exit 1
  fi
else
  echo "✗ init n'a pas créé le projet"; exit 1
fi

cat <<'EOF'

─── HyperFrames prêt ───────────────────────────────────────────────
  source /tmp/amk-hf/env.sh      # à faire dans chaque nouveau shell
  hf doctor                      # état de l'environnement
  hf init monprojet --resolution portrait --non-interactive
  hf render                      # → renders/*.mp4

  ⚠️  RÈGLE : toute librairie chargée par CDN dans un projet hyperframes
      doit être vendue localement (voir GSAP ci-dessus), sinon le rendu est
      bloqué par « sub_timeline_script_failure ».
  ⚠️  Ne pas utiliser la voix Kokoro d'HyperFrames : King a tranché pour
      voice-00 de la plateforme. On garde notre pipeline audio.
────────────────────────────────────────────────────────────────────
EOF
