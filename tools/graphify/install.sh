#!/usr/bin/env bash
# AMK — graphify, installé depuis PyPI dans un venv jetable (/tmp ne persiste pas).
# Épinglé : graphifyy 0.9.95 (dépôt Graphify-Labs/graphify, commit 92741d1 du 23/10/2026, Apache-2.0).
set -euo pipefail
VENV="${AMK_GRAPHIFY_VENV:-/tmp/amk-graphify}"
PIN="0.9.95"

if [ -x "$VENV/bin/graphify" ] && "$VENV/bin/graphify" --version 2>/dev/null | grep -q "$PIN"; then
  echo "graphify $PIN déjà installé → $VENV"
else
  rm -rf "$VENV"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip
  "$VENV/bin/pip" install --quiet "graphifyy==$PIN"
  echo "graphify $PIN installé → $VENV"
fi

# Le CLI n'est pas dans le PATH de la session : on le rend appelable par son nom.
if [ ! -e /usr/local/bin/graphify ] && [ -w /usr/local/bin ]; then
  ln -sf "$VENV/bin/graphify" /usr/local/bin/graphify && echo "lien /usr/local/bin/graphify posé"
fi

echo "vérification :"
"$VENV/bin/graphify" --version
echo
echo "Aucune clé d'API n'est demandée ni utilisée : les documents sont structurés localement"
echo "(titres + liens entre fichiers), le code par AST tree-sitter. Rien ne sort de la machine."
