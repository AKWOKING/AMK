#!/usr/bin/env bash
# ECC (affaan-m/ECC) — installation SÉLECTIVE et reproductible, sandbox ou machine King.
# Amont MIT : https://github.com/affaan-m/ECC — épinglé le 20/10/2026 (release 2.2.3).
# Portée volontairement étroite : seuls les skills d'audit listés ci-dessous, via l'installeur
# officiel de l'amont (cible claude = ~/.claude). PAS de profil full, PAS de hooks runtime,
# PAS de MCP, PAS de mémoire ECC activée. Le harnais complet (plugin guidé `ecc setup`,
# hooks, 311 skills) reste un choix séparé de King sur sa machine (TOOL-SCAN règles 3+5).
# Rien de l'amont dans le dépôt : clone dans ~/.ecc, état d'installation dans ~/.claude/ecc/.
# L'environnement ne survit pas entre sessions : relancer ce script suffit (idempotent, aucun sudo).
set -euo pipefail

PIN="6f1881aeafa3c48f7b603cc4be4b2e4e70daad59"
DEST="$HOME/.ecc"
SKILLS_CSV="accessibility,production-audit,verification-loop,security-review,seo,click-path-audit"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" fetch -q origin "$PIN" || git -C "$DEST" fetch -q origin
else
  git clone -q --filter=blob:none https://github.com/affaan-m/ECC.git "$DEST"
fi
git -C "$DEST" checkout -q "$PIN"

# Dépendances de production du CLI (sql.js pour le store d'état) — aucun script de cycle de vie.
if [ ! -f "$DEST/node_modules/sql.js/package.json" ]; then
  (cd "$DEST" && npm install --ignore-scripts --no-audit --no-fund --omit=dev >/dev/null)
fi

# Installation sélective officielle (installeur Node de l'amont, depuis le clone épinglé).
TMP_JSON="$(mktemp)"
(cd "$DEST" && node scripts/ecc.js install --target claude --skills "$SKILLS_CSV" --json >"$TMP_JSON")
rm -f "$TMP_JSON"

# Miroir des six skills retenus pour l'agent de cette plateforme (~/.agents/skills).
mkdir -p "$HOME/.agents/skills"
for s in accessibility production-audit verification-loop security-review seo click-path-audit; do
  test -f "$HOME/.claude/skills/$s/SKILL.md"
  ln -sfn "$HOME/.claude/skills/$s" "$HOME/.agents/skills/$s"
done

# Preuves par appels réels : doctor de l'amont + résolution des liens installés.
(cd "$DEST" && node scripts/ecc.js doctor --target claude >/dev/null)
test -f "$HOME/.agents/skills/production-audit/SKILL.md"
echo "ECC (sélectif, 6 skills d'audit) OK (pin $PIN)"
echo "skills : $HOME/.agents/skills/{accessibility,production-audit,verification-loop,security-review,seo,click-path-audit}/SKILL.md"
echo "état amont : $HOME/.claude/ecc/install-state.json (doctor OK)"
