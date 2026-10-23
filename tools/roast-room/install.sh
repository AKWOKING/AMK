#!/usr/bin/env bash
# roast-room (nateherkai/roast-room) — installation épinglée. Licence « NOASSERTION » à l'amont :
# le fichier LICENSE est un texte maison, pas une licence SPDX reconnue → usage interne seulement,
# rien de distribué, rien de revendu (voir README, règle licence).
# Épinglé e40f40652d5690c4d9f928c4794c673a99f2cd0e (22/10/2026).
# Portée : le skill `roast-room`, ses agents et son lanceur. Pas de dépendance npm (package.json
# n'en déclare aucune), pas de sudo. L'app web locale n'est pas démarrée par ce script.
set -euo pipefail
PIN="e40f40652d5690c4d9f928c4794c673a99f2cd0e"
DEST="$HOME/.roast-room"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin || true
else
  git clone -q --filter=blob:none https://github.com/nateherkai/roast-room.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

mkdir -p "$HOME/.claude/skills" "$HOME/.claude/agents" "$HOME/.agents/skills"
for d in "$DEST"/.claude/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$HOME/.claude/skills/$name"
  cp -r "$d" "$HOME/.claude/skills/$name"
  ln -sfn "$HOME/.claude/skills/$name" "$HOME/.agents/skills/$name"
done
for f in "$DEST"/.claude/agents/*.md; do
  [ -e "$f" ] || continue
  cp -f "$f" "$HOME/.claude/agents/$(basename "$f")"
done

test -f "$HOME/.claude/skills/roast-room/SKILL.md"
node --check "$DEST/app/server.mjs"
echo "roast-room OK (pin $PIN) → ~/.claude/skills/roast-room + agents ; app : $DEST/app/server.mjs"
