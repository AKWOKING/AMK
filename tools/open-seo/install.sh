#!/usr/bin/env bash
# OpenSEO (every-app/open-seo) — installation sélective épinglée (règles TOOL-SCAN 1–5).
# N'installe QUE les 12 skills markdown du plugin officiel (méthodologie SEO/AEO).
# L'application (pnpm + DataForSEO payant + self-host) reste une décision séparée de King.
set -euo pipefail
PIN="8713d7535f82bf7355313b351004b049d6c9e43c"
SRC="$HOME/.open-seo-src"
SKILLS="$HOME/.agents/skills/open-seo-skills"

rm -rf "$SRC"
git clone -q https://github.com/every-app/open-seo.git "$SRC"
git -C "$SRC" checkout -q "$PIN" 2>/dev/null || {
  echo "ERREUR : pin $PIN absent de l'amont — vérifier avant de changer de pin" >&2
  exit 1
}
HEAD=$(git -C "$SRC" rev-parse HEAD)
[ "$HEAD" = "$PIN" ] || { echo "ERREUR : HEAD $HEAD != pin $PIN" >&2; exit 1; }

rm -rf "$SKILLS"
mkdir -p "$SKILLS"
cp -r "$SRC"/plugins/openseo/skills/* "$SKILLS"/
n=$(ls "$SKILLS" | wc -l | tr -d ' ')
echo "open-seo @ $PIN — $n skills copiés vers $SKILLS"
if [ "$n" -ne 12 ]; then
  echo "ATTENTION : 12 skills attendus au pin, $n présents — vérifier" >&2
  exit 1
fi
echo "OK (application non installée : voir tools/open-seo/README.md)"
