#!/usr/bin/env bash
# The Agency (msitarzewski/agency-agents) — installation épinglée (règles TOOL-SCAN 1–5).
# 298 personas markdown, format natif Claude Code → ~/.agents/agency-agents + ~/.claude/agents
# (fusion non destructive : ce qui existe déjà dans ~/.claude/agents n'est pas supprimé).
set -euo pipefail
PIN="4e3ac3ca6604c75113f52c695dbddcc7af928b46"
SRC="$HOME/.agency-agents-src"
AGENTS="$HOME/.agents/agency-agents"
CC="$HOME/.claude/agents"
DIV="academic design engineering finance game-development gis healthcare marketing paid-media product project-management research sales security spatial-computing specialized support testing strategy"

rm -rf "$SRC"
git clone -q https://github.com/msitarzewski/agency-agents.git "$SRC"
git -C "$SRC" checkout -q "$PIN" 2>/dev/null || {
  echo "ERREUR : pin $PIN absent de l'amont — vérifier avant de changer de pin" >&2
  exit 1
}
HEAD=$(git -C "$SRC" rev-parse HEAD)
[ "$HEAD" = "$PIN" ] || { echo "ERREUR : HEAD $HEAD != pin $PIN" >&2; exit 1; }

rm -rf "$AGENTS"
mkdir -p "$AGENTS" "$CC"
for d in $DIV; do
  if [ -d "$SRC/$d" ]; then cp -r "$SRC/$d" "$AGENTS/"; else
    echo "ATTENTION : division absente au pin : $d" >&2
  fi
done

# Fusion non destructive vers Claude Code (ne rm jamais ~/.claude/agents)
cp -rf "$AGENTS"/. "$CC"/ 2>/dev/null

n=$(find "$AGENTS" -name '*.md' | wc -l | tr -d ' ')
missing=$(grep -rL "^---" "$AGENTS" --include='*.md' | wc -l | tr -d ' ')
echo "agency-agents @ $PIN — $n personas vers $AGENTS + $CC (sans frontmatter : $missing)"
if [ "$n" -ne 298 ] || [ "$missing" -ne 0 ]; then
  echo "ATTENTION : attendu 298 personas / 0 sans frontmatter — vérifier" >&2
  exit 1
fi
echo "OK"
