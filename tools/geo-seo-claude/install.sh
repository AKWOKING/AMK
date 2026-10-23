#!/usr/bin/env bash
# geo-seo-claude (zubair-trabzada/geo-seo-claude) — installation épinglée, MIT.
# Épinglé 989cae01e8ebbc42a9ec798eb9e7cb423f5ec89c (05/10/2026, dernier commit amont).
# Portée : skill `geo` + agents dans ~/.claude, environnement Python isolé (venv) fourni par
# l'amont, miroir ~/.agents/skills/geo. Aucun sudo, aucun hook branché dans settings.json.
set -euo pipefail
PIN="989cae01e8ebbc42a9ec798eb9e7cb423f5ec89c"
DEST="$HOME/.geo-seo-claude"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin || true
else
  git clone -q --filter=blob:none https://github.com/zubair-trabzada/geo-seo-claude.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

# Depuis un clone, l'installeur amont prend la source locale (SOURCE_DIR="$SCRIPT_DIR") :
# il installe exactement le commit épinglé, pas `main`.
bash "$DEST/install.sh" --yes 2>&1 | tail -5 || bash "$DEST/install.sh"

mkdir -p "$HOME/.agents/skills"
test -f "$HOME/.claude/skills/geo/SKILL.md"
ln -sfn "$HOME/.claude/skills/geo" "$HOME/.agents/skills/geo"
test -f "$HOME/.agents/skills/geo/SKILL.md"
echo "geo-seo-claude OK (pin $PIN) → ~/.claude/skills/geo + ~/.agents/skills/geo"
