#!/usr/bin/env bash
# AMK — MoneyPrinterTurbo, installé pour ce qu'il sait faire : **assembler nos vrais plans**.
#
# Ce que ce script installe : le dépôt de harry0703 (MIT), épinglé à un commit précis, dans un
# dossier **hors du dépôt** (`/tmp/amk-moneyprinter`, comme Chromium l'est dans `/tmp/amk-video`),
# avec son propre venv. Rien n'est ajouté au dépôt, rien n'est poussé, aucun sudo.
#
# Ce qu'il refuse d'installer : aucune clé d'API, aucun compte, aucune connexion réseau au-delà du
# clone et de PyPI. Le modèle de sous-titres (Whisper) n'est **pas** téléchargé ici — il l'est au
# premier usage, et seulement si on demande des sous-titres.
#
# Usage :
#   bash tools/moneyprinter/install.sh              # installe ou vérifie
#   AMK_MPT_RUNTIME=/data/mpt bash tools/moneyprinter/install.sh   # autre emplacement
set -euo pipefail

PIN="f063a2b95e0f71f60891ac1c7b53add684bc6a46"   # 2026-10-23
RT="${AMK_MPT_RUNTIME:-/tmp/amk-moneyprinter}"
SRC="$RT/src"
VENV="$RT/venv"

echo "▸ MoneyPrinterTurbo → $RT"

# 1 · la source, épinglée. Un `git clone` complet puis un `checkout` du SHA : c'est le seul moyen
#     d'obtenir exactement ce commit, y compris quand il cesse d'être la tête de branche.
if [ ! -d "$SRC/.git" ]; then
  mkdir -p "$RT"
  git clone -q https://github.com/harry0703/MoneyPrinterTurbo.git "$SRC"
fi
git -C "$SRC" fetch -q origin "$PIN" 2>/dev/null || true
git -C "$SRC" checkout -q "$PIN" 2>/dev/null || {
  echo "✗ commit $PIN introuvable — dépôt amont modifié ?"; exit 1; }
HEAD_SHA="$(git -C "$SRC" rev-parse HEAD)"
[ "$HEAD_SHA" = "$PIN" ] || { echo "✗ mauvais commit : $HEAD_SHA"; exit 1; }
echo "  source : ${PIN:0:7} · $(du -sh "$SRC" | cut -f1)"

# 2 · le venv. Python 3.11+ exigé par le projet.
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
fi
if ! "$VENV/bin/python" -c "import moviepy, edge_tts, faster_whisper, streamlit" 2>/dev/null; then
  echo "  dépendances : installation (~35 s, 1,2 Go dans le venv, hors du dépôt)"
  "$VENV/bin/pip" install -q -r "$SRC/requirements.txt"
fi

# 3 · la configuration : celle de l'exemple, avec les seuls réglages qui nous concernent.
if [ ! -f "$SRC/config.toml" ]; then
  cp "$SRC/config.example.toml" "$SRC/config.toml"
fi

# 4 · la vérification. Elle dit trois choses : les modules importent, ffmpeg est embarqué,
#     et la source « local » (nos propres plans) est acceptée par la ligne de commande.
"$VENV/bin/python" - <<'PY'
import sys, imageio_ffmpeg
import moviepy, edge_tts, faster_whisper  # noqa: F401
exe = imageio_ffmpeg.get_ffmpeg_exe()
print("  modules : OK · ffmpeg :", exe.split("/")[-1])
sys.path.insert(0, ".")
PY
"$VENV/bin/python" "$SRC/cli.py" --help >/dev/null && echo "  cli : OK"
grep -q '"local"' "$SRC/cli.py" && echo "  source local : OK (nos plans, pas de banque d'images)"

echo
echo "MoneyPrinterTurbo OK — assembler : bash tools/moneyprinter/assemble.sh --clips <dossier> --audio <fichier>"
echo "  limites connues : sous-titres = Whisper (modèle téléchargé au 1er usage) · voix automatique"
echo "  (edge-tts) et banques d'images (Pexels…) = réseau, non utilisées par notre chaîne."
