#!/usr/bin/env bash
# hypit — installation reproductible, sandbox ou machine King.
# Amont Apache-2.0 modifiée (© Hypit.AI) : https://github.com/hypit-ai/hypit — audité le 21/10/2026
# (tools/hypit/README.md ; verdict : INSTALLÉ — clauses lues, travail client permis, interdits
# multi-tenant/revente/logo-strip). L'exécutable = paquet npm officiel @hypit/hypit (bin: hypit).
set -euo pipefail

PIN_VERSION="0.3.1"
export PATH="$HOME/.npm-global/bin:$PATH"
mkdir -p "$HOME/.npm-global"

npm install -g --prefix "$HOME/.npm-global" "@hypit/hypit@$PIN_VERSION"

# Preuve par appel réel (jamais le seul état des fichiers)
V="$(hypit --version)"
[ "$V" = "$PIN_VERSION" ] || { echo "version inattendue : $V" >&2; exit 1; }
echo "hypit OK (v$V) — CLI : $HOME/.npm-global/bin/hypit"
echo "Règles : hypit check + hypit pricing AVANT tout build ; jamais la vidéo réelle d'un créateur"
echo "pour un client ; logo/copyright amont des rapports conservés ; portiques vidéo habitude."
