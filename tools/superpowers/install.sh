#!/usr/bin/env bash
# superpowers — obra/superpowers (MIT), la méthodologie de développement en 15 skills.
# Ruling King du 24/10/2026 : « install https://github.com/obra/superpowers.git — don't forget to
# add it as a node and update the graph ».
#
# Épinglé : 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b (main, 21/10/2026) · version amont 7.0.1.
# Portée : les 15 dossiers de `skills/` sont DÉJÀ dans le dépôt (`tools/superpowers/skills/`) —
# ce script ne télécharge rien. Il les installe :
#   ~/.claude/skills/<skill>/        (copie, c'est là que le harnais les lit)
#   ~/.agents/skills/<skill>         (lien symbolique, miroir AMK)
# Aucun sudo. Aucun réseau. Rien d'autre n'est modifié sans `--with-hook`.
#
# Usage :
#   bash tools/superpowers/install.sh                 # les 15 skills
#   bash tools/superpowers/install.sh --with-hook     # + injection du contexte au démarrage
#   bash tools/superpowers/install.sh --check         # vérifie sans installer
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE="$HOME/.claude/skills"
AGENTS="$HOME/.agents/skills"
HOOK_SRC="$SRC/hooks"
SETTINGS="$HOME/.claude/settings.json"
EXPECTED=15

WITH_HOOK=0
CHECK=0
for arg in "$@"; do
  case "$arg" in
    --with-hook) WITH_HOOK=1 ;;
    --check)     CHECK=1 ;;
    -h|--help)   sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "argument inconnu : $arg" >&2; exit 2 ;;
  esac
done

[ -d "$SRC/skills" ] || { echo "skills/ absent de $SRC — le dépôt est incomplet" >&2; exit 1; }

n=0
for d in "$SRC"/skills/*/; do
  [ -f "$d/SKILL.md" ] || { echo "SKILL.md manquant dans $d" >&2; exit 1; }
  n=$((n+1))
done
if [ "$n" -lt "$EXPECTED" ]; then
  echo "seulement $n skill(s) dans $SRC/skills (attendu ≥ $EXPECTED)" >&2
  exit 1
fi

if [ "$CHECK" -eq 1 ]; then
  echo "skills vendored : $n (attendu $EXPECTED) ✓"
  installed=0
  for d in "$SRC"/skills/*/; do [ -d "$CLAUDE/$(basename "$d")" ] && installed=$((installed+1)); done
  echo "skills installés dans ~/.claude/skills : $installed / $n"
  exit 0
fi

mkdir -p "$CLAUDE" "$AGENTS"
n=0
for d in "$SRC"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$CLAUDE/$name"
  cp -r "$d" "$CLAUDE/$name"
  ln -sfn "$CLAUDE/$name" "$AGENTS/$name"
  n=$((n+1))
done
echo "superpowers OK — $n skills dans $CLAUDE + miroir $AGENTS"

if [ "$WITH_HOOK" -eq 1 ]; then
  # Le hook SessionStart est ce qui fait entrer la méthode dans le contexte dès l'ouverture.
  # Il est OPTIONNEL : sans lui, les skills restent installés et se déclenchent par leur description.
  # On sauvegarde settings.json avant d'y toucher, et on n'écrase un hook existant que s'il vient d'ici.
  command -v python3 >/dev/null || { echo "--with-hook demande python3 (absent)" >&2; exit 1; }
  [ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak-$(date +%Y%m%d-%H%M%S)"
  python3 - "$SETTINGS" "$HOOK_SRC" <<'PY'
import json, sys
from pathlib import Path
settings = Path(sys.argv[1])
hook_dir = Path(sys.argv[2])
cmd = f'"{hook_dir}/run-hook.cmd" session-start'
data = {}
if settings.exists() and settings.read_text().strip():
    data = json.loads(settings.read_text())
hooks = data.setdefault("hooks", {})
start = hooks.setdefault("SessionStart", [])
mine = [h for h in start if h.get("hooks") and any(cmd == x.get("command") for x in h["hooks"])]
if mine:
    print("hook SessionStart déjà en place — rien à faire")
else:
    start.append({"matcher": "startup|clear|compact",
                  "hooks": [{"type": "command", "command": cmd, "shell": "bash", "async": False}]})
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"hook SessionStart ajouté à {settings}")
PY
fi

echo
echo "Vérifier :  bash tools/superpowers/install.sh --check"
echo "Lire d'abord : tools/superpowers/skills/using-superpowers/SKILL.md"
