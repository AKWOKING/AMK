# superpowers — la méthode de développement, en 15 skills

`obra/superpowers` (MIT, Jesse Vincent) : un cadre de skills qui décrit **comment** travailler —
comprendre la demande, écrire un plan, exécuter, déboguer, relire — et non ce qu'il faut écrire.
Installé le 24/10/2026 sur ruling King : *« install https://github.com/obra/superpowers.git —
don't forget to add it as a node and update the graph »*.

```bash
bash tools/superpowers/install.sh          # 15 skills → ~/.claude/skills + miroir ~/.agents/skills
bash tools/superpowers/install.sh --check  # 15/15 attendu
```

**Épinglé : `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`** — branche `main`, 21/10/2026, version
amont 7.0.1. Les skills sont **vendus dans le dépôt** (`skills/`, 668 Ko) : le script ne touche pas
au réseau, ne demande pas `sudo`, et n'écrit que dans `~/.claude/skills` et `~/.agents/skills`.

## Les 15 skills

| Skill | Ce qu'il fait, en une phrase |
|---|---|
| `using-superpowers` | le point d'entrée : quand un skill s'applique, et comment le trouver |
| `brainstorming` | ne rien construire avant d'avoir écrit ce que la personne veut vraiment |
| `writing-plans` | un plan qu'un exécutant peut suivre sans nous |
| `executing-plans` | suivre ce plan, étape par étape, avec les points d'arrêt |
| `subagent-driven-development` | découper l'exécution en sous-agents qui se vérifient |
| `dispatching-parallel-agents` | plusieurs agents en parallèle sans qu'ils se marchent dessus |
| `test-driven-development` | le test d'abord, la preuve ensuite |
| `systematic-debugging` | chercher la cause avant de changer le code |
| `verification-before-completion` | « terminé » se prouve, ça ne se déclare pas |
| `requesting-code-review` | demander la relecture avec assez de contexte pour qu'elle serve |
| `receiving-code-review` | recevoir la critique sans la filtrer |
| `finishing-a-development-branch` | finir une branche : ménage, commit, sortie propre |
| `using-git-worktrees` | travailler à côté sans casser ce qui tourne |
| `diagnosing-superpowers` | quand la méthode elle-même dérape |
| `writing-skills` | écrire un skill qu'un autre agent saura lire |

## Ce qui est vendu, et ce qui n'est pas actif

Vendu : `skills/` (les 15), `hooks/` (source, **inactif**), `LICENSE`, `.claude-plugin/plugin.json`.

Pas actif : le **hook de session** de l'amont (`hooks/session-start`, injecté par le manifeste
plugin) écrirait dans le contexte à chaque démarrage. La convention du dépôt
(`tools/marketingskills/install.sh`) est explicite : **aucun hook, aucun sudo, aucun script de cycle
de vie**. `install.sh --with-hook` existe pour l'activer sciemment un jour — il n'a pas été lancé, et
il sauvegarde `~/.claude/settings.json` avant d'y toucher. Les `scripts/` de packaging amont
(`package-codex-plugin.sh`, `sync-to-codex-plugin.sh`) ne sont pas vendus : ils fabriquent les
greffons des autres harnais, ce n'est pas notre problème.

## Limite dite

Ces skills décrivent un **processus**, pas notre métier : ils ne remplacent aucune règle du dépôt
(structure en quatre temps, §1g, registre d'unicité, gel Cristallin). Ils disent comment travailler,
pas quoi écrire dans un message. Le suivi de l'outil est dans `ops/TOOL-SCAN.md` (entrée du 24/10).
