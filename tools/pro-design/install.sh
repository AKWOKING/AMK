#!/usr/bin/env bash
# pro-design — installation reproductible, hors réseau.
# La source est DANS le dépôt (tools/pro-design/SKILL.md) : rien à cloner, rien à épingler.
# Le skill est du markdown pur : aucun binaire, aucun sudo, aucun accès réseau.
# L'environnement ne survit pas entre sessions : relancer ce script suffit (idempotent).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/SKILL.md"
[ -f "$SRC" ] || { echo "✗ SKILL.md introuvable à côté du script" >&2; exit 1; }

mkdir -p "$HOME/.agents/skills/pro-design" "$HOME/.claude/skills/pro-design"
cp "$SRC" "$HOME/.agents/skills/pro-design/SKILL.md"
cp "$SRC" "$HOME/.claude/skills/pro-design/SKILL.md"

# Preuve par lecture réelle du fichier installé — pas par confiance.
test -f "$HOME/.agents/skills/pro-design/SKILL.md"
grep -q '^name: pro-design' "$HOME/.agents/skills/pro-design/SKILL.md"
grep -q '^## 4. Verification loop' "$HOME/.agents/skills/pro-design/SKILL.md"
# La chaîne de vérification de design (étape 4 du skill) : on vérifie qu'elle est là,
# sans l'installer — l'installation de Chromium coûte 40 s et c'est `shot.py` qui la réclame.
if [ -d "${AMK_VIDEO_RUNTIME:-/tmp/amk-video}/node_modules/puppeteer-core" ]; then
  echo "  boucle de vérification : PRÊTE (python3 tools/qa/shot.py <page>)"
else
  echo "  boucle de vérification : ABSENTE — lancer \`bash tools/video/install.sh\` (une fois par session)"
fi

echo "pro-design OK — 4 sections + quality floor + hand-off"
echo "skill : $HOME/.agents/skills/pro-design/SKILL.md"
