#!/usr/bin/env bash
# design-motion-principles (skill « design-motion-principles ») — installation reproductible.
# Amont MIT : https://github.com/kylezantos/design-motion-principles — épinglé le 20/10/2026.
# Rien de l'amont dans le dépôt : clone dans ~/.design-motion-principles, liens vers les dossiers skills.
# Le skill est 100 % markdown + gabarits HTML de rapport : aucun code exécutable, aucun sudo.
# L'environnement ne survit pas entre sessions : relancer ce script suffit (idempotent).
set -euo pipefail

PIN="4a9ca879f24a361f4dca4174fe2da0f67b5ddee3"
DEST="$HOME/.design-motion-principles"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin "$PIN" || git -C "$DEST" fetch -q origin
else
  git clone -q https://github.com/kylezantos/design-motion-principles.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

mkdir -p "$HOME/.claude/skills" "$HOME/.agents/skills"
ln -sfn "$DEST/skills/design-motion-principles" "$HOME/.claude/skills/design-motion-principles"
ln -sfn "$DEST/skills/design-motion-principles" "$HOME/.agents/skills/design-motion-principles"

# Preuve par lecture réelle des fichiers installés (le skill n'a aucun binaire à appeler)
test -f "$HOME/.agents/skills/design-motion-principles/SKILL.md"
grep -q '^name: design-motion-principles' "$HOME/.agents/skills/design-motion-principles/SKILL.md"
test -f "$HOME/.agents/skills/design-motion-principles/workflows/audit.md"
echo "design-motion-principles OK (pin $PIN)"
echo "skill : $HOME/.agents/skills/design-motion-principles/SKILL.md"
