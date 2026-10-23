#!/usr/bin/env bash
# AMK — assembler une vidéo à partir de NOS plans, avec MoneyPrinterTurbo.
#
# Ce qu'on lui donne : les rushes tournés au cabinet (un dossier de .mp4 verticaux), et l'audio
# (voix enregistrée au téléphone, ou voix edge-tts si on en a une). Ce qu'il rend : le montage
# 9:16 et 16:9, coupé à la durée de l'audio, sans banque d'images et sans visage inventé.
#
# Ce que ce script ne fait PAS : générer des plans. `--video-source local` est forcé — la banque
# Pexels et les générateurs payants restent hors de notre chaîne (règle : le décor doit exister).
#
# Usage :
#   bash tools/moneyprinter/assemble.sh --clips /tmp/rushs-55ans --audio /tmp/voix.m4a \
#        --out /tmp/55ans --aspect 9:16 [--subtitles] [--subject "Presbytie"]
#
#   --subtitles  demande Whisper : le modèle (~150 Mo en `small`) se télécharge au premier usage.
set -euo pipefail

RT="${AMK_MPT_RUNTIME:-/tmp/amk-moneyprinter}"
SRC="$RT/src"; VENV="$RT/venv"
[ -x "$VENV/bin/python" ] || { echo "✗ pas installé — lancer bash tools/moneyprinter/install.sh"; exit 1; }

CLIPS=""; AUDIO=""; OUT="./out"; ASPECT="9:16"; SUBS=0; SUBJECT=""; SCRIPT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --clips) CLIPS="$2"; shift 2;;
    --audio) AUDIO="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --aspect) ASPECT="$2"; shift 2;;
    --subject) SUBJECT="$2"; shift 2;;
    --script) SCRIPT="$2"; shift 2;;
    --subtitles) SUBS=1; shift;;
    *) echo "✗ option inconnue : $1"; exit 1;;
  esac
done
[ -n "$CLIPS" ] && [ -d "$CLIPS" ] || { echo "✗ --clips doit être un dossier"; exit 1; }
[ -n "$AUDIO" ] && [ -f "$AUDIO" ] || { echo "✗ --audio doit être un fichier"; exit 1; }
# Le script est le nôtre : il est écrit à la main, relu, et jamais produit par un modèle.
# Sans lui, l'outil appelle un service LLM (Moonshot/OpenAI) — ce que notre chaîne ne fait pas.
[ -n "$SCRIPT" ] || { echo "✗ --script \"<texte dit dans la vidéo>\" est obligatoire"; exit 1; }
mkdir -p "$OUT"

# Les rushes sont copiés dans le dossier que le projet surveille : il ne lit pas ailleurs.
mkdir -p "$SRC/storage/local_videos"
LIST=""
for f in "$CLIPS"/*.mp4 "$CLIPS"/*.mov "$CLIPS"/*.MP4; do
  [ -f "$f" ] || continue
  cp "$f" "$SRC/storage/local_videos/"
  LIST="${LIST:+$LIST,}$SRC/storage/local_videos/$(basename "$f")"
done
[ -n "$LIST" ] || { echo "✗ aucun rush .mp4/.mov dans $CLIPS"; exit 1; }

SUBTITLE_FLAG="--no-subtitle-enabled"
[ "$SUBS" = "1" ] && SUBTITLE_FLAG="--subtitle-enabled"

echo "▸ plans : $(echo "$LIST" | tr ',' '\n' | wc -l) · audio : $AUDIO · $ASPECT"
cd "$SRC"
"$VENV/bin/python" cli.py \
  --video-subject "${SUBJECT:-DM OPTIQUE}" \
  --video-script "$SCRIPT" \
  --video-source local \
  --video-materials "$LIST" \
  --custom-audio-file "$AUDIO" \
  --bgm-type none \
  $SUBTITLE_FLAG \
  --video-aspect "$ASPECT" \
  --video-concat-mode sequential \
  2>&1 | tail -4

# Le résultat est rangé sous storage/tasks/<id>/final-1.mp4 : on le ramène à l'endroit demandé.
LAST="$(ls -t storage/tasks/*/final-1.mp4 2>/dev/null | head -1)"
[ -n "$LAST" ] || { echo "✗ aucun fichier produit"; exit 1; }
DEST="$OUT/$(basename "$(dirname "$LAST")")-$(echo "$ASPECT" | tr ':' 'x').mp4"
cp "$LAST" "$DEST"
echo "→ $DEST ($(du -h "$DEST" | cut -f1))"
