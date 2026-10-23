#!/usr/bin/env bash
# Porte AMK — avant de publier le site de l'agence ou d'envoyer du trafic sur une page.
#
#   bash tools/ops/gate-amk.sh
#
# Trois questions :
#   1. l'arbre est-il le vrai dépôt ?           (sinon tout ce qu'on lit est faux)
#   2. la page de vente tient-elle debout ?     (structure du tunnel : 11 blocs, source externe du 23/10)
#   2 bis. la livraison tient-elle ?            (navigation mobile des 97 pages, en-têtes, partage)
#   3. le portique se teste-t-il lui-même ?     (sinon un « 0 faute » ne vaut rien)
#
# Les deux pages de niche sont incluses : ce sont elles qui reçoivent le trafic payant, et ce sont
# exactement celles qui échouent aujourd'hui au P1 de navigation mobile.
set -u
cd "$(dirname "$0")/../.." || exit 1
fail=0

echo "── 1. état du dépôt ──"
if ! python3 tools/ops/wake.py --check; then
  echo "  ⛔ STOP. Réparer d'abord :  python3 tools/ops/wake.py"
  echo
  echo "PORTE : BLOQUÉE (arbre périmé)."
  exit 1
fi

echo "── 2. tunnel des pages de vente ──"
for page in site/index.html site/en/index.html site/creation-site-web-ecole-cameroun.html site/creation-site-web-clinique-cameroun.html; do
  out=$(python3 tools/qa/audit_funnel.py "$page" 2>&1)
  printf '  %s → %s\n' "$page" "$(echo "$out" | grep 'TOTAL' | sed 's/^ *//')"
  if echo "$out" | grep -q "\[P1\]"; then
    echo "$out" | grep -E "^  \[P1\]"
    fail=1
  fi
done

echo "── 2 bis. livraison (navigation mobile, en-têtes, partage) ──"
out=$(python3 tools/qa/audit_delivery.py site 2>&1)
printf '  site/ → %s\n' "$(echo "$out" | grep 'TOTAL' | sed 's/^ *//')"
if echo "$out" | grep -q "\[P1\]"; then
  echo "$out" | grep -E "^  \[P1\]" | head -5
  fail=1
fi

echo "── 3. le portique mord-il encore ? ──"
if ! python3 tools/qa/test_audit_funnel.py | tail -1; then
  fail=1
fi

echo
if [ "$fail" -ne 0 ]; then
  echo "PORTE : BLOQUÉE — corriger les P1 ci-dessus avant de publier."
  exit 1
fi
echo "PORTE : OK — on peut publier."
