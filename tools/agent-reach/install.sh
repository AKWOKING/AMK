#!/usr/bin/env bash
# AMK — installation d'Agent Reach (Panniantong/Agent-Reach, MIT).
#
# Ce que c'est : une couche « capacité internet » pour agents — sélection, installation
# et diagnostic (`doctor`) des outils upstream (yt-dlp, bili-cli, twitter-cli, rdt-cli, mcporter/Exa,
# gh, feedparser…). La lecture elle-même se fait en appelant ces outils directement.
# Voir README.md (même dossier) pour l'état vérifié canal par canal.
#
# Règle upstream (docs/install.md) : les fichiers Agent Reach vivent HORS du dépôt
# (~/.agent-reach-venv, ~/.agent-reach, ~/.mcporter) — jamais de token/cookie versionné.
# Ce script est le seul artefact AMK ; il installe tout dehors, comme tools/video/install.sh.
#
# Usage :
#   bash tools/agent-reach/install.sh                            # sûr : CLI + check lecture seule + doctor
#   bash tools/agent-reach/install.sh --system --channels=all    # complet (approbation King requise)
# Les arguments sont transmis à `agent-reach install --env=auto`. Sans --system, l'installer
# upstream ne modifie rien (mode sûr par défaut).
set -euo pipefail

# ── épinglage (mettre à jour ensemble ; procédure upstream : docs/update.md du dépôt amont)
AGENT_REACH_VERSION="1.5.0"
AGENT_REACH_COMMIT="94f06c1969dfc1834001269d79d3ad0972d9dee6"
ARCHIVE="https://github.com/Panniantong/agent-reach/archive/${AGENT_REACH_COMMIT}.zip"

VENV="${AGENT_REACH_VENV:-$HOME/.agent-reach-venv}"
export NPM_CONFIG_PREFIX="${NPM_CONFIG_PREFIX:-$HOME/.npm-global}"  # npm -g sans sudo
export PATH="$VENV/bin:$HOME/.local/bin:$NPM_CONFIG_PREFIX/bin:$PATH"

echo "▸ environnement d'exécution (hors dépôt) : $VENV"
mkdir -p "$HOME/.local/bin" "$NPM_CONFIG_PREFIX/bin"

if [ ! -x "$VENV/bin/python" ]; then
  echo "▸ création du venv…"
  python3 -m venv "$VENV"
fi

CURRENT="$("$VENV/bin/agent-reach" version 2>/dev/null || true)"
if [ "$CURRENT" != "Agent Reach v${AGENT_REACH_VERSION}" ]; then
  echo "▸ pip install agent-reach ${AGENT_REACH_VERSION} (${AGENT_REACH_COMMIT:0:7}, archive GitHub — PAS le paquet PyPI homonyme)…"
  "$VENV/bin/pip" install -q "$ARCHIVE"
else
  echo "  = agent-reach ${AGENT_REACH_VERSION} déjà installé"
fi

# pipx : les installateurs de canaux upstream (twitter/bili/rdt) en dépendent.
# uv : fournit uvx (backend LinkedIn MCP). imageio-ffmpeg : binaire ffmpeg embarqué —
# même parade que la chaîne vidéo (aucun apt/sudo disponible dans la sandbox).
if [ ! -x "$VENV/bin/pipx" ] || [ ! -x "$VENV/bin/uvx" ]; then
  echo "▸ pip install pipx uv imageio-ffmpeg (dans le venv)…"
  "$VENV/bin/pip" install -q pipx uv imageio-ffmpeg
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  FF="$("$VENV/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
  ln -sf "$FF" "$HOME/.local/bin/ffmpeg"
  echo "  ✓ ffmpeg (embarqué) → ~/.local/bin/ffmpeg"
fi

echo "▸ agent-reach install --env=auto $*"
rc=0
"$VENV/bin/agent-reach" install --env=auto "$@" || rc=$?
if [ "$rc" != "0" ]; then
  # Connu et documenté : _install_xhs_deps retourne False par conception en environnement
  # serveur (guide seul, aucun service géré) → l'installer sort en 1 même si tout le reste
  # a réussi. Le verdict réel se lit dans le doctor ci-dessous, pas dans ce code.
  echo "  ⚠ installer upstream rc=$rc — souvent = un canal en attente d'input manuel (xhs serveur, clé, cookie). Vérification par doctor :"
fi

# LinkedIn : étape manuelle upstream (mcporter + uvx), sans installateur automatique.
if command -v mcporter >/dev/null 2>&1 && ! grep -q '"linkedin"' "$HOME/.mcporter/mcporter.json" 2>/dev/null; then
  echo "▸ configuration LinkedIn MCP (étape manuelle upstream)…"
  mcporter config add linkedin --command uvx --arg mcp-server-linkedin@latest --env UV_HTTP_TIMEOUT=300 --scope home >/dev/null
  echo "  ✓ linkedin ajouté à ~/.mcporter/mcporter.json (login = navigateur, machine de King)"
fi

echo "▸ vérification (versions réelles des binaires)…"
"$VENV/bin/agent-reach" version
for c in yt-dlp bili twitter rdt mcporter ffmpeg; do
  if command -v "$c" >/dev/null 2>&1; then
    printf '   %-10s %s\n' "$c" "$("$c" --version 2>&1 | head -1)"
  else
    printf '   %-10s (absent — normal sans --system/--channels)\n' "$c"
  fi
done

echo "▸ doctor final…"
"$VENV/bin/agent-reach" doctor || true

cat <<EOF

▸ PRÊT. Avant chaque session (les variables ne survivent pas au redémarrage) :
    export PATH="\$HOME/.agent-reach-venv/bin:\$HOME/.local/bin:\$HOME/.npm-global/bin:\$PATH"
    export NPM_CONFIG_PREFIX="\$HOME/.npm-global"

  Santé :       agent-reach doctor            # + --json : active_backend fait foi
  Mode d'emploi agent : ~/.agents/skills/agent-reach/SKILL.md (installé par --system)
  Canaux login (compte DÉDIÉ uniquement, jamais le compte principal ni un compte client) :
                agent-reach configure twitter-cookies   ·   rdt login   ·   agent-reach configure groq-key
  Désinstaller: agent-reach uninstall  (+ rm -rf ~/.agent-reach-venv)
EOF
