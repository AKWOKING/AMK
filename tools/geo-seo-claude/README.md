# geo-seo-claude — l'optimisation pour les réponses IA (installé le 23/10/2026, demande King)

Amont : <https://github.com/zubair-trabzada/geo-seo-claude> · **MIT** · épinglé
`989cae01e8ebbc42a9ec798eb9e7cb423f5ec89c` (05/10/2026) · 11 186 ★ au moment de l'audit.

## Ce que c'est

Un skill `geo` (GEO = *Generative Engine Optimization*) : score de **citabilité**, analyse des
**crawlers IA** (GPTBot, ClaudeBot, PerplexityBot…), autorité de marque, schéma, `llms.txt`,
optimisation par plateforme, rapports PDF. Commandes : `/geo audit`, `/geo quick`, `/geo citability`,
`/geo crawlers`, `/geo report`.

## Ce qui est installé

`~/.claude/skills/geo` (SKILL.md, scripts, schéma, gabarits, hooks **non branchés**) + un **venv Python
isolé** fourni par l'amont, + miroir `~/.agents/skills/geo`. Depuis un clone, l'installeur amont prend
la source locale (`SOURCE_DIR="$SCRIPT_DIR"`) : c'est bien le commit épinglé qui est installé, pas `main`.
Aucun sudo. Le venv est dans la liste des dossiers exclus des sauvegardes — il se recrée en ~15 s.

## Preuve d'installation (appel réel)

```
$ ~/.claude/skills/geo/.venv/bin/python \
    ~/.claude/skills/geo/scripts/llmstxt_generator.py --help
{ "url": "…/llms.txt", "exists": false, "format_valid": false, … }   # le script répond
```

## Ce que ça apporte à AMK, concrètement

Les crawlers IA sont nommés et vérifiables ; `llms.txt` est le format que Google **ne** lit pas mais
que les assistants lisent — le site DM en a un depuis le 20/10, **le site AMK n'en a pas** (trou relevé
par l'audit SEO du 23/10, §3.4). Le générateur du skill sert de référence pour l'écrire à la main.

## Limites

Aucune de ces analyses ne mesure un trafic : elles lisent des pages publiques. Le score de citabilité
est une **heuristique de l'amont**, pas une mesure Google — il ne se cite jamais comme un chiffre.

Réinstallation : `bash tools/geo-seo-claude/install.sh`.
