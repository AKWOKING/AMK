#!/usr/bin/env bash
# AMK — installation de brag (/brag + /brag-slim, latent-spaces/brag, MIT) et de sa chaîne de rendu.
#
# Ce que c'est : un skill agent qui transforme un projet (ou une URL) en vidéo d'annonce
# de 15–25 s (plan + composition Hyperframes + brag.mp4 + poster + share-copy.txt).
# Voir README.md (même dossier) pour l'état vérifié, les règles de production AMK et les limites.
#
# Tout vit HORS du dépôt : skills dans ~/.agents/skills + ~/.claude/skills, runtime dans
# /tmp/amk-brag, Chromium réutilisé depuis la chaîne vidéo (/tmp/amk-video, tools/video/install.sh).
# Parades sandbox (vérifiées le 19/10) : les CDN navigateurs sont bloqués -> Hyperframes pointe
# sur notre Chromium @sparticuz via HYPERFRAMES_BROWSER_PATH ; GSAP doit être vendored en local
# (jamais de CDN dans une composition) ; ffprobe vient d'un paquet npm qui embarque le binaire.
#
# Usage :
#   bash tools/brag/install.sh            # installe/vérifie toute la chaîne + doctor Hyperframes
#   bash tools/brag/install.sh --smoke    # + rendu de preuve (gabarit 10 s) dans /tmp/brag-smoke
set -euo pipefail

# ── épinglage (mettre à jour ensemble après test)
BRAG_COMMIT="069432cac935ed1895859df201c31436c07fb74e"          # latent-spaces/brag
HYPERFRAMES_COMMIT="68b873f0763361866d09b604d3f132ac47c6cbc5"    # heygen-com/hyperframes (skills)
HYPERFRAMES_NPM="0.8.177"                                        # CLI

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
RT="${AMK_BRAG_RUNTIME:-/tmp/amk-brag}"
VIDEO_RT="${AMK_VIDEO_RUNTIME:-/tmp/amk-video}"
export PATH="$HOME/.local/bin:$HOME/.agent-reach-venv/bin:$HOME/.npm-global/bin:$PATH"
export NPM_CONFIG_PREFIX="${NPM_CONFIG_PREFIX:-$HOME/.npm-global}"
export HYPERFRAMES_BROWSER_PATH="$RT/chrome-wrapper.sh"
export HYPERFRAMES_SKIP_SKILLS=1

echo "▸ runtime brag (hors dépôt) : $RT"
mkdir -p "$RT" "$HOME/.local/bin" "$HOME/.agents/skills" "$HOME/.claude/skills"

# ── ffmpeg (binaire embarqué imageio-ffmpeg — même parade qu'Agent Reach ; aucun apt/sudo)
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "▸ ffmpeg absent -> venv dédié + imageio-ffmpeg…"
  [ -x "$HOME/.brag-venv/bin/python" ] || python3 -m venv "$HOME/.brag-venv"
  "$HOME/.brag-venv/bin/pip" install -q imageio-ffmpeg
  FF="$("$HOME/.brag-venv/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
  ln -sf "$FF" "$HOME/.local/bin/ffmpeg"
fi
echo "  ✓ $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f1-3)"

# ── ffprobe + Hyperframes CLI + GSAP (npm : les binaires sont DANS les paquets, pas de CDN)
cd "$RT"
if [ ! -x node_modules/.bin/hyperframes ] || [ ! -f node_modules/@ffprobe-installer/linux-x64/ffprobe ] || [ ! -f node_modules/gsap/dist/gsap.min.js ]; then
  echo "▸ npm install hyperframes@${HYPERFRAMES_NPM} @ffprobe-installer/ffprobe gsap…"
  [ -f package.json ] || npm init -y >/dev/null 2>&1
  npm install --no-audit --no-fund "hyperframes@${HYPERFRAMES_NPM}" @ffprobe-installer/ffprobe gsap >/dev/null
fi
chmod +x node_modules/@ffprobe-installer/linux-x64/ffprobe
ln -sf "$RT/node_modules/@ffprobe-installer/linux-x64/ffprobe" "$HOME/.local/bin/ffprobe"
echo "  ✓ hyperframes $("$RT/node_modules/.bin/hyperframes" --version) · ffprobe OK · gsap vendoré : $RT/node_modules/gsap/dist/gsap.min.js"

# ── Chromium : celui de la chaîne vidéo AMK (@sparticuz, binaire embarqué dans le paquet npm)
if [ ! -x "$HYPERFRAMES_BROWSER_PATH" ] || ! "$HYPERFRAMES_BROWSER_PATH" --version >/dev/null 2>&1; then
  if [ ! -d "$VIDEO_RT/node_modules/@sparticuz/chromium" ]; then
    echo "▸ runtime vidéo absent -> tools/video/install.sh (Chromium + couches système)…"
    bash "$REPO/tools/video/install.sh" >/dev/null
  fi
  (cd "$VIDEO_RT" && LD_LIBRARY_PATH="$VIDEO_RT/al2023/lib" FONTCONFIG_PATH="$VIDEO_RT/fonts" \
    node -e "import('@sparticuz/chromium').then(async m=>{console.log(await m.default.executablePath())})" >/dev/null)
  cat > "$HYPERFRAMES_BROWSER_PATH" <<EOF
#!/usr/bin/env sh
export LD_LIBRARY_PATH="$VIDEO_RT/al2023/lib\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
export FONTCONFIG_PATH="$VIDEO_RT/fonts"
exec /tmp/chromium "\$@"
EOF
  chmod +x "$HYPERFRAMES_BROWSER_PATH"
fi
echo "  ✓ Chromium : $("$HYPERFRAMES_BROWSER_PATH" --version)"

# ── skills : clones épinglés (sparse : seuls les dossiers skills/ sont récupérés)
clone_sparse () { # url dir commit
  if [ "$(git -C "$2" rev-parse HEAD 2>/dev/null)" != "$3" ]; then
    rm -rf "$2"
    git clone -q --filter=blob:none --no-checkout "$1" "$2"
    git -C "$2" sparse-checkout set skills >/dev/null 2>&1 || true
    git -C "$2" checkout -q "$3"
  fi
}
echo "▸ skills épinglés (brag ${BRAG_COMMIT:0:7} · hyperframes ${HYPERFRAMES_COMMIT:0:7})…"
clone_sparse https://github.com/latent-spaces/brag.git /tmp/brag "$BRAG_COMMIT"
clone_sparse https://github.com/heygen-com/hyperframes.git /tmp/hyperframes "$HYPERFRAMES_COMMIT"
for root in "$HOME/.agents/skills" "$HOME/.claude/skills"; do
  cp -r /tmp/brag/skills/brag "$root/brag"
  cp -r /tmp/brag/skills/brag-slim "$root/brag-slim"
  for s in hyperframes hyperframes-core hyperframes-cli hyperframes-animation hyperframes-creative hyperframes-keyframes hyperframes-audio hyperframes-registry hyperframes-studio; do
    [ -d "/tmp/hyperframes/skills/$s" ] && cp -r "/tmp/hyperframes/skills/$s" "$root/$s"
  done
done
echo "  ✓ $(ls "$HOME/.agents/skills" | wc -l) skills dans ~/.agents/skills · $(ls "$HOME/.claude/skills" | wc -l) dans ~/.claude/skills"

"$RT/node_modules/.bin/hyperframes" telemetry disable >/dev/null 2>&1 || true

echo "▸ doctor Hyperframes (les ✗ optionnels sont attendus : whisper, Kokoro, MusicGen, Docker)…"
"$RT/node_modules/.bin/hyperframes" doctor 2>/dev/null | grep -E "FFmpeg|FFprobe|Chrome|Node|Version" || true

if [ "${1:-}" = "--smoke" ]; then
  echo "▸ rendu de preuve (gabarit 10 s, GSAP local)…"
  cd /tmp && rm -rf brag-smoke
  "$RT/node_modules/.bin/hyperframes" init brag-smoke --example blank --non-interactive --resolution portrait >/dev/null 2>&1
  cp "$RT/node_modules/gsap/dist/gsap.min.js" /tmp/brag-smoke/gsap.min.js
  python3 - <<'PY'
p="/tmp/brag-smoke/index.html"; s=open(p).read()
s=s.replace('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>','<script src="gsap.min.js"></script>')
s=s.replace('font-family: Inter, ui-sans-serif, system-ui, sans-serif;','font-family: sans-serif;')
s=s.replace('// Example: tl.fromTo("#title", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6 }, 0);','tl.fromTo("#title", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6 }, 0);')
open(p,"w").write(s)
PY
  (cd /tmp/brag-smoke && "$RT/node_modules/.bin/hyperframes" check 2>&1 | grep "Check" && "$RT/node_modules/.bin/hyperframes" render)
  ls -la /tmp/brag-smoke/renders/*.mp4
fi

# ── ffprobe (le binaire vient du paquet npm @ffprobe-installer — imageio-ffmpeg n'embarque
#    QUE ffmpeg ; lier les deux dans ~/.local/bin, sinon `render` échoue au probe du rendu,
#    vu le 20/10 : « ffprobe exit with code 8: Unrecognized option 'print_format' »)
FFPROBE_NPM="$RT/node_modules/@ffprobe-installer/linux-x64/ffprobe"
if [ -x "$FFPROBE_NPM" ]; then
  ln -sf "$FFPROBE_NPM" "$HOME/.local/bin/ffprobe"
  echo "  ✓ ffprobe lié depuis le paquet npm : $(ffprobe -version 2>/dev/null | head -1 | cut -d' ' -f1-3)"
else
  echo "  ⚠ ffprobe npm absent de $RT — le rendu hyperframes échouera au probe (leçon 20/10)"
fi

cat <<EOF

▸ PRÊT. Avant chaque session (les variables ne survivent pas au redémarrage) :
    export PATH="\$HOME/.local/bin:\$PATH"
    export HYPERFRAMES_BROWSER_PATH="$RT/chrome-wrapper.sh"
    export HYPERFRAMES_SKIP_SKILLS=1
    HF="$RT/node_modules/.bin/hyperframes"

  Skills :   ~/.agents/skills/{brag,brag-slim,hyperframes*} (+ miroir ~/.claude/skills)
  Composer : lire ~/.agents/skills/brag/SKILL.md, puis hyperframes-core + hyperframes-cli.
  Règles sandbox : GSAP TOUJOURS en local (cp $RT/node_modules/gsap/dist/gsap.min.js dans le
  projet) · AUCUNE musique embarquée de brag (licence ende.app non documentée, issue #59) :
  générer le fond (ffmpeg) ou piste licenciée AMK · tons santé = polished/app-store uniquement.
  Portiques : \$HF check (0 erreur) · \$HF snapshot (relu à l'œil) · rendu ·
              python3 tools/qa/audit_video_motion.py brag.mp4  (doit dire OK) · lecture téléphone.
EOF
