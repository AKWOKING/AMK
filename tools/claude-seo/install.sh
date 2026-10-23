#!/usr/bin/env bash
# claude-seo (AgriciDaniel/claude-seo) — installation épinglée, MIT, sandbox ou machine King.
# Épinglé sur la release v2.5.0 = 219ff485bb016314bb4c15bfc7978df61c668a4f (22/10/2026).
# Portée : le skill `seo` et ses 19 sous-agents dans ~/.claude, + miroir ~/.agents/skills/seo.
# Aucun sudo. Aucun hook enregistré dans settings.json (les fichiers hooks/ sont copiés, pas branchés).
set -euo pipefail
PIN="219ff485bb016314bb4c15bfc7978df61c668a4f"
TAG="v2.5.0"
DEST="$HOME/.claude-seo"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin || true
else
  git clone -q --filter=blob:none https://github.com/AgriciDaniel/claude-seo.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

# L'installeur amont épingle lui-même un tag ; on lui donne celui du pin, jamais `main`.
CLAUDE_SEO_TAG="$TAG" bash "$DEST/install.sh"

# Miroir pour l'agent de cette plateforme.
mkdir -p "$HOME/.agents/skills"
test -f "$HOME/.claude/skills/seo/SKILL.md"
ln -sfn "$HOME/.claude/skills/seo" "$HOME/.agents/skills/seo"
test -f "$HOME/.agents/skills/seo/SKILL.md"
echo "claude-seo OK (pin $PIN) → ~/.claude/skills/seo + ~/.agents/skills/seo"
