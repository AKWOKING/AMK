#!/usr/bin/env bash
# marketingskills (mysticaltech/marketingskills) — fork MIT de coreyhaines31, épinglé.
# Épinglé 9ee486c2002f3edac53c4481315e5acb6d42f7a1 (10/02/2026) — c'est le dernier commit du fork.
# ⚠ Le dépôt amont (coreyhaines31/marketingskills) est à jour (22/10/2026) et porte 52 skills ;
# ce fork en porte 25. Installer l'amont = changer UPSTREAM/BRANCH ci-dessous, avec l'accord de King.
# Portée : copie des 25 dossiers de skills dans ~/.claude/skills + miroir ~/.agents/skills.
# Aucun script de cycle de vie, aucun sudo, aucun hook.
set -euo pipefail
REPO="https://github.com/mysticaltech/marketingskills.git"
PIN="9ee486c2002f3edac53c4481315e5acb6d42f7a1"
DEST="$HOME/.marketingskills"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin || true
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
test "$n" -ge 25
echo "marketingskills OK (pin $PIN) → $n skills dans ~/.claude/skills + miroir ~/.agents/skills"
