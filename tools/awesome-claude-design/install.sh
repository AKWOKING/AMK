#!/usr/bin/env bash
# AMK — awesome-claude-design (VoltAgent, MIT) : un **catalogue**, pas un outil.
#
# Le dépôt ne contient qu'un README qui renvoie vers 68 fichiers `DESIGN.md` hébergés ailleurs.
# Il n'y a donc rien à exécuter : on installe l'index pour pouvoir le consulter hors ligne, et on
# dit clairement ce qu'il ne donne pas (les 68 fichiers ne sont pas dans le dépôt, et ne sont pas
# téléchargeables depuis la sandbox). Pour produire un DESIGN.md, l'outil maison est
# `tools/design-md/` — il travaille sur une page réelle, pas sur une inspiration.
set -euo pipefail

PIN="8f746b5bbb69cc7544fa850c126a71f754091951"     # 23/10/2026
DEST="$HOME/.awesome-claude-design"
SKILL="$HOME/.agents/skills/awesome-claude-design"

[ -d "$DEST/.git" ] || git clone -q https://github.com/VoltAgent/awesome-claude-design.git "$DEST"
git -C "$DEST" fetch -q origin "$PIN" 2>/dev/null || true
git -C "$DEST" checkout -q "$PIN"

mkdir -p "$SKILL"
cp "$DEST/README.md" "$SKILL/README.md"
cat > "$SKILL/SKILL.md" <<'MD'
---
name: awesome-claude-design
description: Catalogue de 68 systèmes de design (DESIGN.md) — index de références, pas un outil exécutable.
---

# awesome-claude-design — comment s'en servir ici

**Ce que c'est :** un index de styles de `DESIGN.md` (VoltAgent). Utile pour **nommer une direction**
(« épuré éditorial », « brutaliste suisse », « chaleureux artisanal ») avant de dessiner.

**Ce qu'il ne fait pas :** il ne contient **aucun** des 68 fichiers, seulement les liens. Sans réseau,
on ne peut pas les ouvrir.

**La règle maison qui gagne :** une référence ne s'applique jamais telle quelle à un client. On prend
la **direction** (rythme, contraste, famille typographique), jamais la palette ni la copie. Pour
**codifier** un système qui existe déjà — le nôtre ou celui d'un site — utiliser
`python3 tools/design-md/extract.py <page>` (`tools/design-md/README.md`), qui lit la vraie page.
MD
echo "awesome-claude-design OK (index seul, ${PIN:0:7})"
