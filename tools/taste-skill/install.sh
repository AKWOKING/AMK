#!/usr/bin/env bash
# taste-skill (skill « design-taste-frontend ») — installation reproductible, sandbox ou machine King.
# Amont MIT : https://github.com/Leonxlnx/taste-skill — épinglé le 20/10/2026.
# Rien de l'amont dans le dépôt : clone dans ~/.taste-skill, liens symboliques vers les dossiers skills.
# L'environnement ne survit pas entre sessions : relancer ce script suffit (idempotent, aucun sudo).
set -euo pipefail

PIN="63aba5f43b5056758b15bbe7d683da8c86a7a7ad"
DEST="$HOME/.taste-skill"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin
else
  git clone -q https://github.com/Leonxlnx/taste-skill.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

# Installeur amont : lien symbolique vers ~/.claude/skills/design-taste-frontend
bash "$DEST/install.sh"
# Même lien pour l'agent de cette plateforme (~/.agents/skills, comme agent-reach)
mkdir -p "$HOME/.agents/skills"
ln -sfn "$DEST/skills/taste-skill" "$HOME/.agents/skills/design-taste-frontend"

# Preuve par appel réel (jamais le seul état des liens)
node "$DEST/skills/taste-skill/scripts/draw.mjs" --list sectors >/dev/null
echo "taste-skill OK (pin $PIN)"
echo "skill : $HOME/.agents/skills/design-taste-frontend/SKILL.md"
echo "inspecteur : exige Chrome/Chromium (CHROME_PATH) — absent par défaut dans la sandbox, voir README.md"
