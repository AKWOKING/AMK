#!/usr/bin/env bash
# AMK — ÉTAPE 0 : LE GRAPHE, AVANT TOUT LE RESTE (ruling King 25/10, 141ᵉ message).
#
#   « new standing rule : use graphify update or read graph, before you read pre-flight document »
#
# Cette commande s'exécute **avant** de lire PRE-FLIGHT.md. Elle ne remplace pas la pré-vol :
# elle la précède. Ce qu'elle fait, dans l'ordre, et rien d'autre :
#   ① rejoue le graphe du dépôt (~10 s, local, 0 clé, 0 réseau) — sauf `--read` ;
#   ② lit la carte `ops/REPO-MAP.md` dans l'ordre obligatoire §0 → §6 → §2 → §3 → §1 → §3 bis ;
#   ③ cherche le sujet du tour dans le graphe (`find.py`) et nomme les fichiers à lire ;
#   ④ imprime la ligne à coller dans l'en-tête pré-vol — un graphe « interrogé » sans nom de
#      fichier ne prouve rien.
#
# Usage :
#   bash tools/graphify/preflight.sh "message prospect opticien"
#   bash tools/graphify/preflight.sh                       # graphe seul, sans recherche
#   bash tools/graphify/preflight.sh --read "prix"          # ne reconstruit pas, lit la carte
#   AMK_GRAPH_LINES=20 bash tools/graphify/preflight.sh     # coupe chaque section plus court
#
# Code de sortie : 0 = carte lue et ligne d'en-tête imprimée · 1 = graphe absent et `--read`.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAP="$ROOT/ops/REPO-MAP.md"
GRAPH="$ROOT/graphify-out/graph.json"
LINES="${AMK_GRAPH_LINES:-14}"

READ_ONLY=0
ARGS=()
for a in "$@"; do
  case "$a" in
    --read|--no-build) READ_ONLY=1 ;;
    *) ARGS+=("$a") ;;
  esac
done
TOPIC="${ARGS[*]:-}"

say() { printf '%s\n' "$*"; }
rule() { printf '%s\n' "$(printf '─%.0s' $(seq 1 78))"; }

say ""
say "ÉTAPE 0 · LE GRAPHE — avant PRE-FLIGHT.md (ruling King 25/10, 141ᵉ message)"
rule

# ① — le graphe
if [ "$READ_ONLY" -eq 1 ]; then
  [ -f "$GRAPH" ] && [ -f "$MAP" ] || {
    say "✗ --read demandé mais le graphe ou la carte manque : relancer sans --read."; exit 1; }
  say "① carte existante conservée (--read) : $(date -r "$MAP" '+%Y-%m-%d %H:%M')"
else
  if [ ! -x "${AMK_GRAPHIFY_VENV:-/tmp/amk-graphify}/bin/graphify" ]; then
    say "① graphify absent du bac → installation (une fois par session)"
    bash "$ROOT/tools/graphify/install.sh" >/dev/null 2>&1 || say "  ⚠ installation incomplète — find.py reste utilisable (stdlib seule)"
  fi
  say "① reconstruction du graphe (~10 s)…"
  python3 "$ROOT/tools/graphify/build_full_graph.py" 2>&1 | grep -E '^\[full\] (structure|citations|communautés|carte)' | sed 's/^/   /' || true
fi

[ -f "$MAP" ] || { say "✗ carte absente : python3 tools/graphify/build_full_graph.py"; exit 1; }

# ① bis — l'estampe : une étape 0 qui ne laisse pas de trace ne peut pas être vérifiée (ruling 142).
STAMP_DIR="${HOME}/.amk-provisioned"
mkdir -p "$STAMP_DIR" 2>/dev/null || true
MODE="rebuild"; [ "$READ_ONLY" -eq 1 ] && MODE="read"
printf '%s\t%s\t%s\t%s\n' "$(date -Iseconds)" "$MODE" \
  "$(grep -m1 -o '[0-9]* nœuds' "$MAP" 2>/dev/null | cut -d' ' -f1)" "${TOPIC:-—}" \
  >> "$STAMP_DIR/preflight.stamp" 2>/dev/null || true
tail -n 200 "$STAMP_DIR/preflight.stamp" > "$STAMP_DIR/preflight.stamp.tmp" 2>/dev/null \
  && mv "$STAMP_DIR/preflight.stamp.tmp" "$STAMP_DIR/preflight.stamp" 2>/dev/null || true

# ② — la carte, dans l'ordre obligatoire
say ""
say "② la carte, dans cet ordre : §0 → §6 → §2 → §3 → §1 → §3 bis"
python3 - "$MAP" "$LINES" <<'PY'
import re, sys
from pathlib import Path

path, cap = Path(sys.argv[1]), int(sys.argv[2])
text = path.read_text(encoding="utf-8").splitlines()

ORDER = [
    ("0",     "combien de fichiers, combien d'orphelins — et le chiffre qui a bougé"),
    ("6",     "le sujet du tour est-il dans la table de routage ?"),
    ("2",     "les documents qui font le squelette"),
    ("3",     "les documents périmés mais encore cités — consignes mortes"),
    ("1",     "la couche knowledge/ : ce qui fait loi, et combien de fois c'est cité"),
    ("3 bis", "ce que je vais créer existe-t-il déjà, sans être cité ?"),
]

def section(key):
    head = None
    for i, line in enumerate(text):
        m = re.match(r"^#{2,4}\s+(\d+(?:\s*bis)?)\s*[·.]", line.strip())
        if m and m.group(1).strip() == key:
            head = i
            level = line.strip().split()[0].count("#")
            break
    if head is None:
        return None
    out = [text[head]]
    for line in text[head + 1:]:
        if re.match(r"^#{2,4}\s", line.strip()) and line.strip().split()[0].count("#") <= level:
            break
        out.append(line)
    return out

missing = []
for key, why in ORDER:
    block = section(key)
    print(f"\n§{key} — {why}")
    if block is None:
        missing.append(key)
        print(f"   ⚠ section absente de la carte (structure changée ?)")
        continue
    body = [l for l in block[1:] if l.strip()]
    for line in body[:cap]:
        print("   " + line[:160])
    if len(body) > cap:
        print(f"   … {len(body) - cap} ligne(s) de plus → ops/REPO-MAP.md §{key}")
if missing:
    print(f"\n⚠ sections manquantes : {', '.join('§' + m for m in missing)}")
PY

# ③ — le sujet du tour
if [ -n "$TOPIC" ]; then
  say ""
  say "③ recherche dans le graphe : « $TOPIC »"
  bash "$ROOT/tools/graphify/ask.sh" "$TOPIC" --top 6 2>/dev/null | sed 's/^/   /' || say "   ⚠ recherche indisponible (graphe à reconstruire)"
else
  say ""
  say "③ pas de sujet fourni — relancer avec un sujet : bash tools/graphify/preflight.sh \"…\""
fi

# ④ — la ligne d'en-tête
NODES="$(grep -m1 -o '[0-9]* nœuds' "$MAP" | head -1 || true)"
STAMP="$(date '+%d/%m %H:%M')"
say ""
rule
say "④ À COLLER DANS L'EN-TÊTE PRÉ-VOL (avant la ligne PRE-FLIGHT.md) :"
if [ "$READ_ONLY" -eq 1 ]; then
  say "   Étape 0 : carte lue SANS reconstruction ($STAMP, ${NODES:-nœuds ?}) · §0/§6/§2/§3/§1/§3 bis · ask « ${TOPIC:-—} »"
else
  say "   Étape 0 : graphe rejoué $STAMP (${NODES:-nœuds ?}) · carte lue §0/§6/§2/§3/§1/§3 bis · ask « ${TOPIC:-—} »"
fi
say ""
say "   Puis seulement : PRE-FLIGHT.md lu, §0b dossier client, §0c knowledge/."
say ""
