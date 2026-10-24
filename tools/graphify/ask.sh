#!/usr/bin/env bash
# AMK — « quel document du dépôt parle de ça ? » (à lancer AVANT d'écrire)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="${AMK_GRAPHIFY_VENV:-/tmp/amk-graphify}/bin/python"
# find.py n'utilise que la bibliothèque standard : le venv n'est pas indispensable pour chercher.
[ -x "$PY" ] || PY="$(command -v python3 || true)"
[ -n "$PY" ] || { echo "python3 introuvable" >&2; exit 2; }
[ -f "$ROOT/graphify-out/graph.json" ] || {
  echo "graphe absent : python3 tools/graphify/build_full_graph.py" >&2; exit 2; }
printf '%s\task\t%s\n' "$(date -Iseconds)" "$(echo "$*" | cut -c1-60)" >> "$HOME/.amk-provisioned/usage.log" 2>/dev/null || true
exec "$PY" "$ROOT/tools/graphify/find.py" "$@"
