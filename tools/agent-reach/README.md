# AMK — AGENT REACH (outil installé et vérifié)

**Installé le 19 Oct 2026**, demande de King (« Install https://github.com/Panniantong/Agent-Reach » ;
choix tranchés par King : `--system` + **tous les canaux** + ce dossier). Entrée au journal :
`ops/TOOL-SCAN.md` §19/10.

**Ce que c'est.** [Agent Reach](https://github.com/Panniantong/Agent-Reach) (MIT, v**1.5.0**, commit
épinglé `94f06c1`) est une *couche capacité* : il choisit, installe et diagnostique (`agent-reach
doctor`) les outils upstream par plateforme — yt-dlp, gh, feedparser, bili-cli, twitter-cli,
rdt-cli, mcporter/Exa, OpenCLI… La lecture se fait ensuite **en appelant ces outils directement** ;
Agent Reach n'est pas un wrapper. **Problème AMK nommé** (règle 1 de la tool-scan) : les contrôles
approfondis par prospect (`PRE-FLIGHT.md` §1c : vrais canaux YouTube/X/Instagram/Facebook), les
leçons YouTube (`research/YouTube-Lessons.md`), la lecture web/RSS — aujourd'hui réinventés outil
par outil. **Coût : 0 FCFA** (tout est open source ; seul coût possible un jour : un proxy serveur
~1 $/mois, inutile en local — **rien acheté**).

## Ce qui tourne dans cet environnement (vérifié, pas supposé)

Installation : `bash tools/agent-reach/install.sh --system --channels=all`, le 19/10, **hors dépôt**
(`~/.agent-reach-venv`, `~/.agent-reach`, `~/.mcporter`, skill `~/.agents/skills/agent-reach/`) —
règle upstream : jamais de fichier/token Agent Reach dans l'espace de travail.

| Canal | Outil (version constatée) | État vérifié le 19/10 |
|---|---|---|
| GitHub | `gh` (système) | ✅ **appel réel OK** — `gh repo view Panniantong/Agent-Reach` → 99 526 ★, MIT (le doctor dit `[!]` par prudence : il ne lance pas `gh auth status`) |
| RSS/Atom | `feedparser` 6.0.14 | ✅ **appel réel OK** — `releases.atom` du dépôt amont parsé, 7 entrées |
| YouTube | `yt-dlp` 2026.08.19 + `--js-runtimes node` | ⚠️ installé + configuré (doctor ✅) — **trafic YouTube bloqué ici** (voir ci-dessous) |
| Web (Jina Reader) | `curl https://r.jina.ai/…` | ⚠️ doctor ✅ mais **curl réel = HTTP 000 ici** — le doctor sonde l'installation, pas le réseau |
| Bilibili | `bili` 0.6.2 (pipx) | ⚠️ installé (doctor ✅, backend `bili-cli`) — appel réel : `network_error` vers api.bilibili.com |
| Recherche web | `mcporter` 0.9.0 + Exa MCP | ⚠️ configuré (`~/.mcporter`) — serveur Exa **offline d'ici** (TLS coupé) |
| Twitter/X | `twitter` 0.8.5 (pipx) | ⏳ installé — `twitter status` → `not_authenticated` propre. Attente : cookies d'un **compte dédié**, fournis par King |
| Reddit | `rdt` 0.4.2 (pipx, source GitHub épinglée) | ⏳ installé — `authenticated: false`. Reddit n'a **aucune** voie sans login (amont) |
| LinkedIn | MCP `uvx mcp-server-linkedin` | ⏳ configuré dans mcporter — premier login = navigateur visible, machine de King |
| Xiaoyuzhou (podcasts) | `transcribe.sh` + `ffmpeg` 7.0.2 (embarqué imageio-ffmpeg → `~/.local/bin`) | ⏳ installé — attente clé Groq gratuite (`agent-reach configure groq-key`) |
| Xueqiu | (cookie seul, rien à installer) | ⏳ `agent-reach configure --from-browser chrome --platform xueqiu`, si un jour utile |
| Skill agent | `~/.agents/skills/agent-reach/SKILL.md` + references | ✅ installé — **à lire avant d'utiliser les canaux** |

**Doctor au 19/10 : 4/16 ✅** (youtube, rss, web, bilibili) — à lire avec la colonne ci-dessus :
d'ici, seuls **GitHub et RSS sont prouvés de bout en bout**.

## Ce qui NE tourne PAS ici (et pourquoi)

| Besoin | Blocage constaté |
|---|---|
| Trafic plateformes (YouTube, Jina, Bilibili, Exa, V2EX…) | La sandbox ne laisse sortir que GitHub/PyPI/npm : HTTP 000 / TLS EOF partout ailleurs (même limite que `tools/video/README.md`). **Sur la machine de King, ces canaux doivent répondre** — c'est là qu'ils se prouvent. |
| OpenCLI → Facebook, Instagram, Reddit-desktop, sous-titres Bilibili | Exige un Chrome de bureau avec session vivante. L'installer upstream **saute** ces canaux quand il détecte un serveur (notre cas). Sur la machine de King : `install.sh --system --channels=opencli,facebook,instagram`, puis ajouter l'extension Chrome OpenCLI (seul geste manuel) et `opencli doctor`. |
| Boss直聘 | Desktop uniquement (Chrome dédié + login manuel de King) — sauté ici, et faible pertinence AMK. |
| Xiaohongshu (serveur) | Guide seul : binaire `xiaohongshu-mcp` à poser dans `~/.agent-reach/tools/` + cookies via Cookie-Editor. ⚠️ Il fait sortir l'installer en **code 1 même quand tout le reste réussit** (retour `False` par conception) — ne pas confondre avec un échec ; le doctor fait foi. |
| `agent-reach check-update` | Échoue d'ici (réseau) — la mise à jour se vérifie sur GitHub. |

## Installation (une fois par environnement)

```bash
bash tools/agent-reach/install.sh                          # sûr : CLI + check lecture seule + doctor
bash tools/agent-reach/install.sh --system --channels=all  # complet (ce qui a été fait le 19/10)
export PATH="$HOME/.agent-reach-venv/bin:$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
export NPM_CONFIG_PREFIX="$HOME/.npm-global"
```

Windows (machine de King, si applicable — extrait du guide upstream) :
```powershell
py -3 -m venv $env:USERPROFILE\.agent-reach-venv
$env:USERPROFILE\.agent-reach-venv\Scripts\Activate.ps1
python -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto --system --channels=all
agent-reach doctor
```

## Usage (l'agent appelle les outils upstream directement)

```bash
agent-reach doctor                      # TOUJOURS d'abord ; --json → active_backend par canal
gh repo view owner/repo                 # GitHub
yt-dlp --write-auto-subs --skip-download <URL YouTube>   # sous-titres (leçons vidéo)
curl -s "https://r.jina.ai/<URL>"       # lire une page web en texte propre
mcporter call exa.web_search_exa query="…" numResults=5 # recherche sémantique
bili search "…" --type video            # Bilibili (sans login)
# après cookies King (compte dédié) : les variables doivent être exportées dans le même shell
export TWITTER_AUTH_TOKEN="…" TWITTER_CT0="…"; twitter search "…" -n 10
# desktop King uniquement :
opencli facebook search "…" -f yaml · opencli instagram user <nom> -f yaml · opencli reddit search "…" -f yaml
```
Référence complète des commandes par plateforme : `~/.agents/skills/agent-reach/SKILL.md`
(+ `references/{search,social,video,web,dev,career,finance}.md`).

## Règles de production (opposables — alignées `ops/TOOL-SCAN.md`)

1. **Pas en production tant que King ne l'a pas utilisé une fois personnellement** sur une vraie
   tâche (règle 3). Statut au 19/10 : *installé et diagnostiqué*, pas encore *validé*.
2. **Aucune donnée client, aucun compte client** (règle 4). Cookies/login : **compte secondaire
   dédié uniquement** — risque de ban documenté par l'amont sur les usages cookie/API.
3. **Tokens et cookies vivent uniquement dans `~/.agent-reach/`** (amont : fichier en 600), jamais
   dans le dépôt, jamais dans un message versionné. Vérifié dans le code upstream : l'installation
   **ne lit jamais** les cookies du navigateur — chaque `configure` est un geste explicite de King.
4. **Doctor ≠ preuve de bout en bout.** Un ✅ doctor = binaire + config sondés. Avant de promettre
   un canal sur un prospect, faire **un appel réel** (leçon du 19/10 : doctor ✅ web/bilibili,
   appels réels morts dans la sandbox).
5. **Mise à jour** = procédure upstream (`docs/update.md`), puis ré-épingler version + commit dans
   `install.sh` et rafraîchir ce tableau. Désinstallation : `agent-reach uninstall` (garde-fou :
   `--dry-run` d'abord), puis `rm -rf ~/.agent-reach-venv`.
