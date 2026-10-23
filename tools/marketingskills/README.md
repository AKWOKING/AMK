# marketingskills — 52 skills, **amont** coreyhaines31 (basculé le 23/10/2026, ruling King)

Amont : <https://github.com/coreyhaines31/marketingskills> · **MIT** · 56 063 ★ ·
épinglé `e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b` (branche `main`, 22/10/2026) · **52 skills**.

## Historique — pourquoi ce n'est pas le fork

Le 23/10, la demande portait sur `mysticaltech/marketingskills`, un fork de Corey Haines. Il a été
installé (`9ee486c2…`, 25 skills) puis **abandonné le même jour** : le fork n'a pas bougé depuis le
**10 février 2026** et s'arrête à 25 skills, alors que l'amont en porte 52 — dont `ai-seo`,
`cold-email`, `link-building`, `marketing-council`, `directory-submissions`, `lead-magnets`,
`influencer-marketing`, `conversion-tracking`, qui sont exactement des sujets AMK.

> Ruling King (23/10/2026) : « Basculer marketingskills sur l'amont (52 skills au lieu de 25). »

**Ce qu'il a fallu corriger dans le script** : le clone existant venait du fork. `git fetch origin`
ramenait l'ancien historique et le pin de l'amont restait introuvable (`not our ref`). `install.sh`
réécrit donc l'origine (`remote set-url`) avant de chercher le pin. Sans ça, la bascule échoue
silencieusement et laisse les 25 anciens skills en place.

## Ce qui est installé

Les 52 dossiers de `skills/` dans `~/.claude/skills`, miroir `~/.agents/skills` (liens symboliques
vérifiés : 52/52, aucun lien mort). Aucun script de cycle de vie, aucun hook, aucun `npm install`,
aucun sudo. `dist/*.skill` (paquets préconstruits) n'est pas utilisé : on copie les sources, c'est
plus lisible et plus facile à corriger.

## Ce que ça apporte à AMK

Des procédures écrites là où nous improvisions : `copywriting`, `copy-editing`, `content-strategy`,
`email-sequence`, `form-cro`, `pricing`, `launch-strategy`, `analytics`, `ab-testing`, `ai-seo`,
`schema`, `seo-audit`, `programmatic-seo`, `site-architecture`.

Utile en **appui** : nos règles maison (`knowledge/MARKETING-OPTICAL-2026-10-22.md`,
`sales/AMK-Sales-Playbook-v2.md`, gabarit W43) restent supérieures en cas de conflit, et les verrous
client (aucun prix public, aucun délai sans condition, aucun avis inventé, aucune donnée patient) ne
se négocient pas parce qu'un skill propose un modèle.

## Limites

Ce sont des prompts de méthode, pas des données : aucun ne connaît le Cameroun, l'optique, ni nos
marges. Rien n'y est vérifié. Les skills `ads`, `paywalls`, `programmatic-seo` supposent des marchés
et des budgets qui ne sont pas les nôtres — ils se lisent, ils ne s'appliquent pas tels quels.

Réinstallation : `bash tools/marketingskills/install.sh` (idempotent, réécrit l'origine, vérifie 52).
