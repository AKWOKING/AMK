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
#   --subtitles  sous-titres **sans Whisper** : le script connu est découpé au temps (tools/moneyprinter/srt.py)
#                puis incrusté par ffmpeg. Aucun modèle, aucun réseau, résultat relisible.
#   --whisper    sous-titres par Whisper (MPT natif) : télécharge un modèle au premier usage.
#   --music      musique de fond (resource/songs du projet) ; défaut : aucune.
set -euo pipefail

# Le script change de dossier en cours de route (le projet lit ses rushes dans SON storage) :
# on fige donc les chemins absolus dès la première ligne, sinon `srt.py` devient introuvable.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RT="${AMK_MPT_RUNTIME:-/tmp/amk-moneyprinter}"
SRC="$RT/src"; VENV="$RT/venv"
[ -x "$VENV/bin/python" ] || { echo "✗ pas installé — lancer bash tools/moneyprinter/install.sh"; exit 1; }

CLIPS=""; AUDIO=""; OUT="./out"; ASPECT="9:16"; SUBS=0; WHISPER=0; MUSIC="none"; SUBJECT=""; SCRIPT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --clips) CLIPS="$2"; shift 2;;
    --audio) AUDIO="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --aspect) ASPECT="$2"; shift 2;;
    --subject) SUBJECT="$2"; shift 2;;
    --script) SCRIPT="$2"; shift 2;;
    --subtitles) SUBS=1; shift;;
    --whisper) WHISPER=1; shift;;
    --music) MUSIC="$2"; shift 2;;
    *) echo "✗ option inconnue : $1"; exit 1;;
  esac
done
[ -n "$CLIPS" ] && [ -d "$CLIPS" ] || { echo "✗ --clips doit être un dossier"; exit 1; }
[ -n "$AUDIO" ] && [ -f "$AUDIO" ] || { echo "✗ --audio doit être un fichier"; exit 1; }
CLIPS="$(cd "$CLIPS" && pwd)"; AUDIO="$(cd "$(dirname "$AUDIO")" && pwd)/$(basename "$AUDIO")"
OUT="$(mkdir -p "$OUT" && cd "$OUT" && pwd)"
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
[ "$WHISPER" = "1" ] && SUBTITLE_FLAG="--subtitle-enabled"

echo "▸ plans : $(echo "$LIST" | tr ',' '\n' | wc -l) · audio : $AUDIO · $ASPECT"
cd "$SRC"
"$VENV/bin/python" cli.py \
  --video-subject "${SUBJECT:-DM OPTIQUE}" \
  --video-script "$SCRIPT" \
  --video-source local \
  --video-materials "$LIST" \
  --custom-audio-file "$AUDIO" \
  --bgm-type "${MUSIC}" \
  $SUBTITLE_FLAG \
  --video-aspect "$ASPECT" \
  --video-concat-mode sequential \
  2>&1 | tail -4

# Le résultat est rangé sous storage/tasks/<id>/final-1.mp4 : on le ramène à l'endroit demandé.
LAST="$(ls -t storage/tasks/*/final-1.mp4 2>/dev/null | head -1)"
[ -n "$LAST" ] || { echo "✗ aucun fichier produit"; exit 1; }
DEST="$OUT/$(basename "$(dirname "$LAST")")-$(echo "$ASPECT" | tr ':' 'x').mp4"
cp "$LAST" "$DEST"

# ── Sous-titres sans Whisper ───────────────────────────────────────────────────────────────────
# On connaît le texte : on le découpe au temps (srt.py), puis ffmpeg incruste. La police est celle
# du projet (Be Vietnam Pro, accents français complets), pas une police système.
if [ "$SUBS" = "1" ]; then
  DUR=$("$VENV/bin/python" -c "from moviepy import AudioFileClip; print(round(AudioFileClip('$AUDIO').duration, 3))")
  SRT="$(dirname "$DEST")/$(basename "$DEST" .mp4).srt"
  python3 "$HERE/srt.py" --script "$SCRIPT" --duration "$DUR" --out "$SRT" >/dev/null
  FF=$("$VENV/bin/python" -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
  BURNED="${DEST%.mp4}-soustitre.mp4"
  "$FF" -nostdin -loglevel error -i "$DEST" \
    -vf "subtitles='$SRT':fontsdir='$SRC/resource/fonts':force_style='FontName=Be Vietnam Pro,FontSize=11,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=1.4,Shadow=0,MarginV=90,Alignment=2'" \
    -c:v libx264 -preset veryfast -crf 20 -c:a copy -y "$BURNED"
  mv "$BURNED" "$DEST"
  echo "  sous-titres incrustés : $(grep -c -- '-->' "$SRT") bloc(s)"
fi

echo "→ $DEST ($(du -h "$DEST" | cut -f1))"
