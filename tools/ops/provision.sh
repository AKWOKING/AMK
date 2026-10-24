#!/usr/bin/env bash
# provision — remettre une session neuve en état de marche, en une commande.
#
# Le problème : le bac repart d'un clone neuf, donc `~/.claude/skills`, les venvs et les clones
# d'outils ont disparu — mais le dépôt, lui, a tout ce qu'il faut pour les refaire. Ce script
# rejoue les 24 installateurs épinglés de `tools/*/install.sh`, dans l'ordre alphabétique, et
# laisse une **estampe** par outil (`~/.amk-provisioned/<outil>`) : c'est ce qui permet de dire
# « installé cette session » au lieu de le supposer.
#
#   bash tools/ops/provision.sh --list                # l'état, sans rien installer
#   bash tools/ops/provision.sh                       # installe ce qui manque (24 outils)
#   bash tools/ops/provision.sh --core                # le minimum d'un tour : graphify + superpowers
#   bash tools/ops/provision.sh --only graphify,superpowers
#   bash tools/ops/provision.sh --force               # rejoue tout, même ce qui est estampillé
#   bash tools/ops/provision.sh --failures            # ne rejoue que ce qui a échoué
#
# Aucun sudo. Aucun secret. Chaque installateur est épinglé dans son propre fichier — ce script
# ne décide de rien, il exécute et il rapporte.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

STAMPS="$HOME/.amk-provisioned"
ONLY=""
FORCE=0
LIST=0
FAILED_ONLY=0
TIMEOUT="${AMK_PROVISION_TIMEOUT:-300}"

while [ $# -gt 0 ]; do
  case "$1" in
    --list)      LIST=1 ;;
    --force)     FORCE=1 ;;
    --failures)  FAILED_ONLY=1 ;;
    --core)      ONLY="graphify,superpowers" ;;   # réveil + lecture + méthode : ~1 min
    --only)      shift; ONLY="${1:-}" ;;
    --only=*)    ONLY="${1#--only=}" ;;
    --timeout)   shift; TIMEOUT="${1:-300}" ;;
    -h|--help)   sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argument inconnu : $1" >&2; exit 2 ;;
  esac
  shift
done

mkdir -p "$STAMPS"

tools=()
for f in tools/*/install.sh; do tools+=("$(basename "$(dirname "$f")")"); done

keep=()
if [ -n "$ONLY" ]; then
  IFS=',' read -r -a wanted <<< "$ONLY"
  for t in "${tools[@]}"; do
    for w in "${wanted[@]}"; do [ "$t" = "$w" ] && keep+=("$t") && break; done
  done
  tools=("${keep[@]}")
fi
if [ "$FAILED_ONLY" -eq 1 ]; then
  keep=()
  for t in "${tools[@]}"; do [ -f "$STAMPS/$t.failed" ] && keep+=("$t"); done
  tools=("${keep[@]}")
fi

if [ "${#tools[@]}" -eq 0 ]; then
  echo "aucun outil à traiter" >&2
  exit 1
fi

stamp_ok() { [ -f "$STAMPS/$1.ok" ]; }
stamp_line() {
  [ -f "$STAMPS/$1.ok" ] && head -1 "$STAMPS/$1.ok" || echo "—"
}

if [ "$LIST" -eq 1 ]; then
  printf '%-28s %-14s %s\n' "OUTIL" "ÉTAT" "PREUVE"
  ok=0; ko=0; no=0
  for t in "${tools[@]}"; do
    if stamp_ok "$t"; then
      printf '%-28s %-14s %s\n' "$t" "installé" "$(stamp_line "$t")"; ok=$((ok+1))
    elif [ -f "$STAMPS/$t.failed" ]; then
      printf '%-28s %-14s %s\n' "$t" "ÉCHEC" "$(head -1 "$STAMPS/$t.failed")"; ko=$((ko+1))
    else
      printf '%-28s %-14s %s\n' "$t" "non joué" "—"; no=$((no+1))
    fi
  done
  echo
  echo "$ok installé(s) · $ko en échec · $no non joué(s) — estampes dans $STAMPS"
  exit 0
fi

echo "── provision : ${#tools[@]} outil(s), délai ${TIMEOUT} s par outil ──"
ok=0; ko=0; skip=0; failed=""
for t in "${tools[@]}"; do
  if stamp_ok "$t" && [ "$FORCE" -eq 0 ]; then
    printf '  %-28s déjà provisionné (%s)\n' "$t" "$(stamp_line "$t")"
    skip=$((skip+1)); continue
  fi
  printf '  %-28s ' "$t"
  log="$(mktemp)"
  t0=$(date +%s)
  if timeout --kill-after=30 "$TIMEOUT" bash "tools/$t/install.sh" >"$log" 2>&1; then
    pin="$(grep -m1 -E '^[A-Z_]*(PIN|COMMIT|VERSION)[A-Z_]*=' "tools/$t/install.sh" \
           | sed -E 's/^[A-Z_]+=?//; s/"//g; s/^ +//' | cut -c1-12)"
    printf '%s  installé  %ss  pin=%s\n' "✅" "$(( $(date +%s) - t0 ))" "${pin:-—}"
    echo "$(date -Iseconds) pin=${pin:-—}" > "$STAMPS/$t.ok"
    rm -f "$STAMPS/$t.failed"
    ok=$((ok+1))
  else
    code=$?
    reason="$(tail -2 "$log" | tr '\n' ' ' | cut -c1-120)"
    [ "$code" -eq 124 ] && reason="délai dépassé (${TIMEOUT} s)"
    printf '%s  ÉCHEC (%s) %s\n' "⛔" "$code" "$reason"
    echo "$(date -Iseconds) code=$code $reason" > "$STAMPS/$t.failed"
    rm -f "$STAMPS/$t.ok"
    ko=$((ko+1)); failed="$failed $t"
  fi
  rm -f "$log"
done

echo
echo "$ok installé(s) · $skip déjà là · $ko en échec · estampes dans $STAMPS"
[ -n "$failed" ] && echo "rejouer les échecs : bash tools/ops/provision.sh --failures"
exit 0
