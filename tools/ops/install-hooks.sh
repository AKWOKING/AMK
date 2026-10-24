#!/usr/bin/env bash
# Pose les crochets git du dépôt — pre-commit et pre-push. Idempotent, réversible.
#
#   bash tools/ops/install-hooks.sh          # pose / met à jour
#   bash tools/ops/install-hooks.sh --remove # retire
#
# Pourquoi un script et pas un `.git/hooks` versionné : git n'exécute jamais un crochet qui vit dans
# l'arbre de travail. Le crochet doit donc être écrit dans `.git/hooks` à chaque clone neuf — c'est
# exactement ce que fait `provision.sh` pour les outils, appliqué aux portes.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1
HOOKS="$(git rev-parse --git-path hooks)"
mkdir -p "$HOOKS"
if [ "${1:-}" = "--remove" ]; then
  rm -f "$HOOKS/pre-push" "$HOOKS/pre-commit"
  echo "crochets pre-commit et pre-push retirés"
  exit 0
fi
for h in pre-commit pre-push; do
  cp "tools/ops/hooks/$h" "$HOOKS/$h"
  chmod +x "$HOOKS/$h"
done
echo "crochets posés dans $HOOKS :"
echo "  pre-commit → machine.py --ci + carte reconstruite et ré-ajoutée si elle a changé"
echo "  pre-push   → machine.py --ci"
