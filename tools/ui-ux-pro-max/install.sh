#!/usr/bin/env bash
# ui-ux-pro-max (skill « ui-ux-pro-max ») — installation reproductible.
# Amont MIT : https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — épinglé le 20/10/2026 (2.15.0).
# Rien de l'amont dans le dépôt : clone dans ~/.ui-ux-pro-max-skill, liens vers les dossiers skills.
# La recherche est un script Python stdlib local (aucun réseau, aucun paquet installé).
set -euo pipefail

PIN="56ea9cf174ed86786187daa9de0e6247cb0747e4"
DEST="$HOME/.ui-ux-pro-max-skill"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin "$PIN" || git -C "$DEST" fetch -q origin
else
  git clone -q --filter=blob:none https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

mkdir -p "$HOME/.claude/skills" "$HOME/.agents/skills"
ln -sfn "$DEST/.claude/skills/ui-ux-pro-max" "$HOME/.claude/skills/ui-ux-pro-max"
ln -sfn "$DEST/.claude/skills/ui-ux-pro-max" "$HOME/.agents/skills/ui-ux-pro-max"

# Preuve par appel réel (recherche locale, hors projet : requête générique)
python3 "$HOME/.agents/skills/ui-ux-pro-max/scripts/search.py" "accessible form validation" --domain ux -n 1 >/dev/null
echo "ui-ux-pro-max OK (pin $PIN)"
echo "skill : $HOME/.agents/skills/ui-ux-pro-max/SKILL.md"
