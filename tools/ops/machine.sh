#!/usr/bin/env bash
# LA MACHINE — cockpit du dépôt. La carte : ops/MACHINE.md
#   bash tools/ops/machine.sh            # où j'en suis, ce qui est frais, ce qui ne l'est plus
#   bash tools/ops/machine.sh 2          # la fiche de l'étape 2 (lecture)
#   bash tools/ops/machine.sh --who prix # qui tranche ce sujet
#   bash tools/ops/machine.sh --check    # code 1 si une porte dure est fermée
exec python3 "$(dirname "${BASH_SOURCE[0]}")/machine.py" "$@"
