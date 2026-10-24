#!/usr/bin/env bash
# Pose les crochets git du dépôt (aujourd'hui : pre-push). Idempotent, réversible.
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
  rm -f "$HOOKS/pre-push"
  echo "crochet pre-push retiré"
  exit 0
fi
cp tools/ops/hooks/pre-push "$HOOKS/pre-push"
chmod +x "$HOOKS/pre-push"
echo "crochet posé : $HOOKS/pre-push → python3 tools/ops/machine.py --ci"
