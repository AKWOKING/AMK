#!/usr/bin/env bash
# Appeler un skill superpowers — et LAISSER UNE TRACE.
#
#   bash tools/superpowers/use.sh --list
#   bash tools/superpowers/use.sh verification-before-completion
#
# Pourquoi ce script existe : un skill lu ne laisse aucune trace, donc « superpowers est installé et
# utilisé » restait une affirmation invérifiable. Le 24/10, `machine.sh --usage` l'a nommé dans la
# ligne « provisionnés mais muets ». Ce script fait deux choses : il montre le chemin du skill, et il
# écrit une ligne datée dans ~/.amk-provisioned/usage.log. Il n'exécute pas le skill : il n'y a pas de
# moteur à appeler — le skill est un texte de méthode, on le lit et on applique.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1
SKILLS="tools/superpowers/skills"

if [ "${1:-}" = "--list" ]; then
  for d in "$SKILLS"/*/; do echo "  $(basename "$d")"; done
  exit 0
fi
[ $# -ge 1 ] || { echo "usage : bash tools/superpowers/use.sh <skill> | --list" >&2; exit 2; }
name="$1"
[ -f "$SKILLS/$name/SKILL.md" ] || {
  echo "skill inconnu : $name" >&2
  echo "les 15 disponibles :" >&2
  for d in "$SKILLS"/*/; do echo "  $(basename "$d")" >&2; done
  exit 2
}
printf '%s\tsuperpowers\t%s\n' "$(date -Iseconds)" "$name" >> "$HOME/.amk-provisioned/usage.log" 2>/dev/null || true
echo "$SKILLS/$name/SKILL.md"
