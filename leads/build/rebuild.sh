#!/usr/bin/env bash
# AMK CRM — reconstruit tout, dans le bon ordre.
#   crm.py     : source  -> leads/CRM.csv
#   records.py : CRM     -> leads/records/<slug>.md
#   views.py   : CRM     -> PIPELINE · KILL-LIST · STALE · SOURCES · Daily-Plan.csv
# Les trois sont idempotents : relancer ne perd rien, ça rafraîchit.
#
# ⚠️ GARDE-FOU AJOUTÉ LE 21/09 APRÈS UNE HEURE PERDUE À CROIRE LE CONTRÔLEUR FOYER.
#   `set -e` ne protège PAS contre ce qui m'est arrivé : je lançais
#       bash leads/build/rebuild.sh 2>&1 | grep -E "..."
#   et le code de retour affiché était celui de `grep` (0 = au moins une ligne trouvée),
#   jamais celui du builder. Résultat : `crm.py` avait échoué en fin de script (une clé hors
#   schéma, « ✗ clé(s) inconnue(s) » — son propre garde-fou, excellent), AUCUN CSV n'avait été
#   écrit, et je relisais le CSV de la fois d'avant en concluant que mes champs étaient « perdus ».
#   Trois lectures de champ coup sur suite, toutes périmées, avant de penser au `mtime`.
#   Depuis : le script annonce lui-même s'il a réussi et à quelle heure le CSV a été écrit.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CRM="$HERE/../../leads/CRM.csv"
fail=0

step() {  # $1 = nom, $2.. = commande
  local name="$1"; shift
  local before after rc out
  before=$(stat -c %Y "$CRM" 2>/dev/null || echo 0)
  out=$("$@" 2>&1); rc=$?
  after=$(stat -c %Y "$CRM" 2>/dev/null || echo 0)
  printf '%s\n' "$out"
  if [ $rc -ne 0 ]; then
    printf '✗ ÉCHEC — %s (code %s). Le CSV que tu liras est celui d%savant : RIEN n\x27a été écrit.\n' \
      "$name" "$rc" "'"
    [ -n "$before" ] && [ "$after" = "$before" ] && \
      printf '  (mtime de leads/CRM.csv toujours : %s)\n' "$(date -d "@$after" '+%H:%M:%S' 2>/dev/null || echo inconnu)"
    fail=1
  fi
  return 0
}

step "crm.py (source → CSV)" python3 "$HERE/crm.py"     || true
step "records.py (CSV → fiches)" python3 "$HERE/records.py" || true
step "views.py (CSV → vues)" python3 "$HERE/views.py"   || true

if [ $fail -ne 0 ]; then
  echo "✗ CRM NON reconstruit — corriger la cause ci-dessus et relancer. Ne PAS lire les vues."
  exit 1
fi
echo "✓ CRM reconstruit — leads/CRM.csv écrit à $(date -r "$CRM" '+%H:%M:%S' 2>/dev/null || echo heure indisponible) · $(date -r "$CRM" '+%Y-%m-%d' 2>/dev/null)"
echo "  toute modification manuelle dans ces fichiers est perdue,"
echo "  ce qui est voulu : la seule source est leads/build/crm.py + sales/Activity-Log.md"
