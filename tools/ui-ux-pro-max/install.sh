#!/usr/bin/env bash
# ui-ux-pro-max (skill « ui-ux-pro-max ») — installation reproductible.
# Amont MIT : https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — épinglé le 20/10/2026 (2.15.0).
# Rien de l'amont dans le dépôt : clone dans ~/.ui-ux-pro-max-skill, liens vers les dossiers skills.
# La recherche est un script Python stdlib local (aucun réseau, aucun paquet installé).
set -euo pipefail

PIN="d14efff8ed1faa4187f004f79926f428c8074ec7"
DEST="$HOME/.ui-ux-pro-max-skill"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin "$PIN" || git -C "$DEST" fetch -q origin
else
  git clone -q --filter=blob:none https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

mkdir -p "$HOME/.claude/skills" "$HOME/.agents/skills"
# 23/10 : l'amont ne livre plus un seul skill mais six (design, design-system, brand, ui-styling,
# banner-design, slides). On les lie tous — un skill non lié est un skill qui n'existe pas.
for s in "$DEST"/.claude/skills/*/; do
  name="$(basename "$s")"
  ln -sfn "$s" "$HOME/.claude/skills/$name"
  ln -sfn "$s" "$HOME/.agents/skills/$name"
done

# Preuve par appel réel (recherche locale, hors projet : requête générique)
python3 "$HOME/.agents/skills/ui-ux-pro-max/scripts/search.py" "accessible form validation" --domain ux -n 1 >/dev/null
echo "ui-ux-pro-max OK (pin $PIN)"
echo "skill : $HOME/.agents/skills/ui-ux-pro-max/SKILL.md"
