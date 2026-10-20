#!/usr/bin/env bash
# scrapling — installation reproductible, sandbox ou machine King.
# Amont BSD-3-Clause (© 2024 Karim Shoair) : https://github.com/D4Vinci/Scrapling — épinglé le 20/10/2026
# (audit tools/scrapling/README.md ; verdict : INSTALLÉ — veille/monitoring, usage par cibles validées).
# Rien de l'amont dans le dépôt : clone dans ~/.scrapling, paquet pip --user, skill officiel copié.
# L'environnement ne survit pas entre sessions : relancer ce script suffit (idempotent, aucun sudo).
set -euo pipefail

PIN="fd53131"
DEST="$HOME/.scrapling"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin
else
  git clone -q --depth 1 https://github.com/D4Vinci/Scrapling.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

# Bibliothèque (pypi) — fetchers inclus : curl_cffi (statique) + playwright (navigateur, SANS les
# navigateurs : ils se téléchargent à part, voir la limite dans README.md)
pip install --user --break-system-packages -q "scrapling[fetchers]"

# Skill officiel de l'amont (BSD-3, même auteur) vers les dossiers skills — la copie du dossier
# est la voie prévue par l'amont (agent-skill/Scrapling-Skill)
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
rm -rf "$HOME/.agents/skills/scrapling" "$HOME/.claude/skills/scrapling"
cp -r "$DEST/agent-skill/Scrapling-Skill" "$HOME/.agents/skills/scrapling"
cp -r "$DEST/agent-skill/Scrapling-Skill" "$HOME/.claude/skills/scrapling"

# Preuve par appel réel (jamais le seul état des liens)
python3 -c "import scrapling, importlib.metadata as m; assert m.version('scrapling').startswith('0.'), m.version('scrapling'); print('scrapling', m.version('scrapling'))"
python3 -c "from scrapling.fetchers import Fetcher; print('Fetcher importé')"
echo "scrapling OK (pin $PIN, BSD-3) — skill : $HOME/.agents/skills/scrapling/SKILL.md"
echo "LIMITE sandbox : StealthyFetcher/DynamicFetcher exigent les navigateurs (scrapling install) —"
echo "à faire sur la machine de King (internet complet) ; le bac reste en Fetcher statique."
