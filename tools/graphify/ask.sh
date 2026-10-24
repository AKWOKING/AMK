#!/usr/bin/env bash
# AMK — « quel document du dépôt parle de ça ? » (à lancer AVANT d'écrire)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="${AMK_GRAPHIFY_VENV:-/tmp/amk-graphify}/bin/python"
[ -x "$PY" ] || { echo "graphify absent : bash tools/graphify/install.sh" >&2; exit 2; }
[ -f "$ROOT/graphify-out/graph.json" ] || { echo "graphe absent : python3 tools/graphify/build_docs_graph.py" >&2; exit 2; }
exec "$PY" "$ROOT/tools/graphify/find.py" "$@"
