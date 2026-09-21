#!/usr/bin/env bash
# AMK CRM — reconstruit tout, dans le bon ordre.
#   crm.py     : source  -> leads/CRM.csv
#   records.py : CRM     -> leads/records/<slug>.md
#   views.py   : CRM     -> PIPELINE · KILL-LIST · STALE · SOURCES · Daily-Plan.csv
# Les trois sont idempotents : relancer ne perd rien, ça rafraîchit.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/crm.py"
python3 "$HERE/records.py"
python3 "$HERE/views.py"
echo "✓ CRM reconstruit — toute modification manuelle dans ces fichiers est perdue,"
echo "  ce qui est voulu : la seule source est leads/build/crm.py + sales/Activity-Log.md"
