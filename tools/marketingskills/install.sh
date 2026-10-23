#!/usr/bin/env bash
# marketingskills — AMONT coreyhaines31/marketingskills (MIT), épinglé.
# Ruling King du 23/10/2026 : « Basculer marketingskills sur l'amont (52 skills au lieu de 25) ».
# Épinglé e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b (branche main, 22/10/2026) — 52 skills.
# Historique : le fork mysticaltech/marketingskills (25 skills, figé le 10/02/2026) a été installé le
# 23/10 sur demande, puis abandonné sur ce ruling. Ne pas y revenir sans un nouveau ruling.
# Portée : copie des dossiers de skills dans ~/.claude/skills + miroir ~/.agents/skills.
# Aucun script de cycle de vie, aucun sudo, aucun hook.
set -euo pipefail
REPO="https://github.com/coreyhaines31/marketingskills.git"
PIN="e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b"
DEST="$HOME/.marketingskills"

if [ -d "$DEST/.git" ]; then
  # le clone existant peut venir d'un autre dépôt (le fork de février 2026) : on réécrit l'origine,
  # sinon `git fetch` ramène l'ancien historique et le pin de l'amont reste introuvable
  git -C "$DEST" remote set-url origin "$REPO"
  git -C "$DEST" fetch -q origin '+refs/heads/*:refs/remotes/origin/*'
else
  git clone -q --filter=blob:none "$REPO" "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

mkdir -p "$HOME/.claude/skills" "$HOME/.agents/skills"
n=0
for d in "$DEST"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$HOME/.claude/skills/$name"
  cp -r "$d" "$HOME/.claude/skills/$name"
  ln -sfn "$HOME/.claude/skills/$name" "$HOME/.agents/skills/$name"
  n=$((n+1))
done
test "$n" -ge 52
echo "marketingskills OK — amont coreyhaines31 (pin $PIN) → $n skills dans ~/.claude/skills + miroir ~/.agents/skills"
