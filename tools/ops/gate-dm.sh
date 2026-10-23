#!/usr/bin/env bash
# Porte unique avant d'écrire ou de publier du contenu DM Optique.
#
#   bash tools/ops/gate-dm.sh                        # contrôle l'état + les nouveaux rendus
#   bash tools/ops/gate-dm.sh chemin/vers/fichier.md # + contrôle des affirmations de ce fichier
#
# Quatre questions, dans cet ordre :
#   1. l'arbre est-il le vrai dépôt ?      (sinon tout ce qu'on lit est faux)
#   2. les rendus sont-ils frais ?          (un MP4 plus vieux que son storyboard est interdit)
#   3. les affirmations tiennent-elles ?    (prix, nombre de montures, promesses)
#   4. le site livré tient-il debout ?      (menu mobile, cache, icônes, partage, schéma, en-têtes)
#
# L'étape 4 est `--strict` : c'est une livraison **client**, un P2 est un défaut, pas une note.
set -u
cd "$(dirname "$0")/../.." || exit 1
fail=0

echo "── 1. état du dépôt ──"
if ! python3 tools/ops/wake.py --check; then
  echo "  ⛔ STOP. Réparer d'abord :  python3 tools/ops/wake.py"
  echo
  echo "PORTE : BLOQUÉE (arbre périmé) — lire ou mesurer ici donnerait des chiffres faux."
  exit 1
fi

echo "── 2. fraîcheur des rendus ──"
fresh_out=$(python3 tools/qa/audit_render_freshness.py clients/dm-optic 2>&1)
echo "$fresh_out" | grep -E "audit fraîcheur|✗|VERDICT"
if echo "$fresh_out" | grep -q "PÉRIMÉ\|BLOQUÉ"; then
  # un rendu périmé bloque ; un rendu non traçable est signalé (fichiers antérieurs à la preuve)
  if echo "$fresh_out" | grep -q "✗"; then fail=1; fi
  if echo "$fresh_out" | grep -q "? "; then
    echo "  ⚠ rendu(s) sans preuve ci-dessus : ne pas publier sans relecture image par image."
  fi
fi

if [ "$#" -gt 0 ]; then
  echo "── 3. affirmations : $* ──"
  if ! python3 tools/qa/audit_claims.py "$@" 2>&1 | grep -qE "VERDICT : OK"; then
    python3 tools/qa/audit_claims.py "$@" 2>&1 | grep -E "^\s+\S+\.md:|VERDICT"
    fail=1
  else
    echo "  aucune infraction"
  fi
fi

echo "── 4. porte de livraison (client → --strict) ──"
delivery_log=$(mktemp)
if python3 tools/qa/audit_delivery.py hosting/previews/dmoptic \
     --base https://dmoptiquesarl.com --strict >"$delivery_log" 2>&1; then
  grep -E "TOTAL" "$delivery_log" | sed 's/^  /  /'
else
  echo "  ⛔ le site livré a un défaut P1/P2 :"
  grep -E "^  \[P[12]\]" "$delivery_log"
  grep -E "TOTAL" "$delivery_log"
  fail=1
fi
rm -f "$delivery_log"

echo
if [ "$fail" -ne 0 ]; then
  echo "PORTE : BLOQUÉE — corriger avant d'écrire ou de publier."
  exit 1
fi
echo "PORTE : OK — on peut travailler."
