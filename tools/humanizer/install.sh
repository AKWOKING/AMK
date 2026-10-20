#!/usr/bin/env bash
# humanizer — installation reproductible, sandbox ou machine King.
# Amont MIT (© 2025 Siqi Chen) : https://github.com/blader/humanizer — épinglé le 20/10/2026 (audit tools/humanizer/README.md).
# Rien de l'amont dans le dépôt : clone dans ~/.humanizer, COPIE du SKILL.md (MIT) vers les dossiers skills.
# L'environnement ne survit pas entre sessions : relancer ce script suffit (idempotent, aucun sudo).
set -euo pipefail

PIN="8c307f3"
DEST="$HOME/.humanizer"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin
else
  git clone -q https://github.com/blader/humanizer.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

# Le skill = un SKILL.md autonome (amont : « For an agent the Skills CLI does not know,
# copy SKILL.md into its skill folder »). Aucun runtime, aucun hook, aucun réseau.
mkdir -p "$HOME/.agents/skills/humanizer" "$HOME/.claude/skills/humanizer"
cp "$DEST/SKILL.md" "$HOME/.agents/skills/humanizer/SKILL.md"
cp "$DEST/SKILL.md" "$HOME/.claude/skills/humanizer/SKILL.md"

# Preuve par appel réel : le SKILL.md déclare front-matter + version
grep -q "^name: humanizer" "$HOME/.agents/skills/humanizer/SKILL.md"
grep -q 'version: "3' "$HOME/.agents/skills/humanizer/SKILL.md"
echo "humanizer OK (pin $PIN, MIT) — skill : $HOME/.agents/skills/humanizer/SKILL.md"
echo "usage : appeler le skill avec le texte à passer (26 motifs « Signs of AI writing »)"
