#!/usr/bin/env bash
# session.sh — ouvrir une session de travail en une commande, et savoir en une minute si tout est
# d'aplomb.
#
# Ce qui coûtait du temps avant : une session neuve repartait de zéro (4,5 Go, ~5 min), l'état du
# dépôt se lisait dans trois commandes, et le premier `--check` arrivait souvent après deux fichiers
# touchés. Ici : rien n'est installé si les estampes sont là, l'état tient en six lignes, et le temps
# total est affiché — pas supposé.
#
#   bash tools/ops/session.sh              # le réveil complet
#   bash tools/ops/session.sh --fast       # sans provisioning, sans fetch (déjà fait)
#   bash tools/ops/session.sh --full       # noyau de travail (4 outils) au lieu du noyau de tour
#
# Ce qu'il fait, dans cet ordre :
#   0. `git fetch` — la branche est-elle en retard sur `main` ?
#   1. `provision.sh --core` — graphify + superpowers, saut immédiat si les estampes existent
#   1 bis. `install-hooks.sh` — pose pre-commit et pre-push si ce clone n'en a pas
#   2. `machine.py --check` — les portes dures ; une seule rouge suffit à arrêter la session
#   3. l'état en six lignes : branche, avance/retard, jauge de fusion, carte, orphelins, prochain geste
#
# Il ne modifie rien d'autre que les estampes de provisioning. Aucune écriture dans le dépôt.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 1

CORE="--core"
FETCH=1
while [ $# -gt 0 ]; do
  case "$1" in
    --fast)  FETCH=0 ;;
    --full)  CORE="" ;;
    -h|--help) sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argument inconnu : $1" >&2; exit 2 ;;
  esac
  shift
done

T0=$(date +%s)
msg() { printf '%s\n' "$*"; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ── 0 · le dépôt distant a-t-il bougé ?
if [ "$FETCH" -eq 1 ]; then
  step "0 · le distant"
  if git fetch --quiet origin main 2>/dev/null; then
    main_sha=$(git rev-parse --short origin/main)
    behind=$(git rev-list --count "HEAD..origin/main" 2>/dev/null || echo "?")
    msg "  main = $main_sha · cette branche est $([ "$behind" = "0" ] && echo "à jour" || echo "en retard de $behind commit(s)")"
  else
    msg "  ⚠ distant injoignable — on continue avec ce qu'on a (le cockpit le dira)"
  fi
fi

# ── 1 · le noyau, s'il n'est pas déjà là
step "1 · le noyau"
if [ -n "$CORE" ]; then
  bash tools/ops/provision.sh $CORE 2>&1 | sed 's/^/  /'
else
  msg "  (sauté : --fast)"
fi

# ── 1 bis · les crochets, s'ils ne sont pas posés
step "1 bis · les crochets"
if [ -x "$(git rev-parse --git-path hooks)/pre-commit" ]; then
  msg "  pré-commit et pre-push en place (la CI se joue avant le push)"
else
  bash tools/ops/install-hooks.sh 2>&1 | sed 's/^/  /'
fi

# ── 2 · les portes
step "2 · les portes"
check_out=$(python3 tools/ops/machine.py --check 2>&1)
check_rc=$?
printf '%s\n' "$check_out" | sed 's/^/  /'

# ── 3 · l'état, en six lignes
step "3 · l'état"
branch=$(git branch --show-current)
dirty=$(git status --porcelain | wc -l | tr -d ' ')
commits=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "?")
msgs=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l | tr -d ' ')
map_age=$(python3 - <<'PY' 2>/dev/null || echo "?"
import subprocess, datetime, pathlib
r = subprocess.run(["git", "log", "-1", "--format=%ct", "--", "ops/REPO-MAP.md"], capture_output=True, text=True)
ts = int(r.stdout.strip() or 0)
print(datetime.date.today() - datetime.date.fromtimestamp(ts))
PY
)
# `grep -oh` : sans le -h, le nom de fichier (2026-…) serait capturé comme le premier nombre
orphans=$(grep -oh '\*\*[0-9]* seulement à traiter\*\*' ops/FILE-AUDIT-*.md 2>/dev/null | tail -1 | grep -o '[0-9]*' || echo "?")
msg "  branche      $branch · $commits commit(s) depuis main · $([ "$dirty" = "0" ] && echo "arbre propre" || echo "$dirty fichier(s) modifié(s)")"
msg "  carte        $map_age (rejouée à chaque pré-commit, vérifiée par la CI)"
msg "  orphelins    $orphans à traiter (ops/FILE-AUDIT-*.md § 4 bis)"
msg "  Notion       miroir daté dans ops/MACHINE.md, ligne MIRROR"

printf '\n'
if [ "$check_rc" -eq 0 ]; then
  printf '\033[32m✓ session ouverte en %s s — les portes sont ouvertes\033[0m\n' "$(( $(date +%s) - T0 ))"
else
  printf '\033[31m⛔ session ouverte en %s s — une porte est fermée, voir ci-dessus\033[0m\n' "$(( $(date +%s) - T0 ))"
fi
