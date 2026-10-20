#!/usr/bin/env bash
# impeccable (skill « impeccable », moteur détecteur d'anti-patterns UI) — installation reproductible.
# Amont Apache-2.0 : https://github.com/pbakaus/impeccable — épinglé le 20/10/2026 (skill v0.1.16, engine 0.1.16).
# Rien de l'amont dans le dépôt : clone dans ~/.impeccable-src, lien skill, moteur dans ~/.impeccable/bin/.
# Ici (egress GitHub releases bloqué) le moteur vient du paquet npm OFFICIEL de l'amont
# (@impeccable/cli-linux-x64, même version que ENGINE_VERSION) ; sur la machine de King, le
# lanceur amont sait télécharger le moteur tout seul depuis les releases GitHub signées.
# PAS de hook Impeccable installé (ni settings Claude ni hook projet) : activation séparée, décision de King.
set -euo pipefail

PIN="46b822f7dda9f7dba799a9c7776fdc19b3a93559"
ENGINE_VERSION="0.1.16"
SRC="$HOME/.impeccable-src"
CACHE="$HOME/.impeccable/bin/$ENGINE_VERSION"

if [ -d "$SRC/.git" ]; then
  git -C "$SRC" fetch -q origin "$PIN" || git -C "$SRC" fetch -q origin
else
  git clone -q --filter=blob:none https://github.com/pbakaus/impeccable.git "$SRC"
fi
git -C "$SRC" checkout -q "$PIN"

mkdir -p "$HOME/.claude/skills" "$HOME/.agents/skills"
ln -sfn "$SRC/.agents/skills/impeccable" "$HOME/.agents/skills/impeccable"
ln -sfn "$SRC/.claude/skills/impeccable" "$HOME/.claude/skills/impeccable"

# Moteur : binaire officiel @impeccable/cli-linux-x64 à la version ENGINE_VERSION (npm, registry autorisé).
if [ ! -x "$CACHE/impeccable" ]; then
  TMP="$(mktemp -d)"
  (cd "$TMP" && npm pack "@impeccable/cli-linux-x64@$ENGINE_VERSION" --silent >/dev/null)
  (cd "$TMP" && tar -xzf impeccable-cli-linux-x64-"$ENGINE_VERSION".tgz)
  mkdir -p "$CACHE"
  cp "$TMP/package/bin/impeccable" "$CACHE/impeccable"
  chmod +x "$CACHE/impeccable"
  rm -rf "$TMP"
fi

# Preuves par appels réels : handshake du moteur, puis détection sur un fichier HTML trivial.
"$HOME/.agents/skills/impeccable/scripts/impeccable" engine-probe >/dev/null
TMPHTML="$(mktemp --suffix=.html)"
printf '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>test</title></head><body><h1>Titre</h1><p>Paragraphe de contrôle assez long pour être lu.</p></body></html>' > "$TMPHTML"
"$HOME/.agents/skills/impeccable/scripts/impeccable" detect --quiet "$TMPHTML" >/dev/null 2>&1 || true
rm -f "$TMPHTML"
echo "impeccable OK (pin $PIN, engine $ENGINE_VERSION)"
echo "skill : $HOME/.agents/skills/impeccable/SKILL.md"
echo "moteur : $CACHE/impeccable (engine-probe OK)"
