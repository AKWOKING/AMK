# marketingskills — 25 skills marketing, et un écart à connaître (installé le 23/10/2026, demande King)

Amont demandé : <https://github.com/mysticaltech/marketingskills> (fork de Corey Haines) · **MIT** ·
épinglé `9ee486c2002f3edac53c4481315e5acb6d42f7a1` (10/02/2026) · 362 ★.

## ⚠ L'écart qui compte

Le fork demandé n'a **pas bougé depuis le 10 février 2026** et porte **25 skills**. Le dépôt d'origine
`coreyhaines31/marketingskills` (56 063 ★, MIT, poussé le **22/10/2026**) en porte **52**, dont
`ai-seo`, `cold-email`, `link-building`, `marketing-council`, `directory-submissions`, `lead-magnets`,
`influencer-marketing` — précisément des sujets AMK. **Ce qui est installé aujourd'hui est le fork
demandé, comme demandé.** Basculer sur l'amont = deux lignes dans `install.sh` (`REPO` + `PIN`) et un
ruling de King — je ne l'ai pas fait sans son mot.

## Ce qui est installé

Les 25 dossiers de `skills/` dans `~/.claude/skills`, miroir `~/.agents/skills` (liens symboliques).
Aucun script de cycle de vie, aucun hook, aucun `npm install`, aucun sudo. `dist/*.skill` (paquets
préconstruits) n'est pas utilisé : on copie les sources, c'est plus lisible et plus facile à corriger.

## Ce que ça apporte à AMK

Des procédures écrites là où nous improvisions : `copywriting`, `copy-editing`, `content-strategy`,
`email-sequence`, `form-cro`, `pricing`, `launch-strategy`, `analytics-tracking`, `ab-test-setup`.
Utile en **appui** : nos règles maison (`knowledge/MARKETING-OPTICAL-2026-10-22.md`,
`sales/AMK-Sales-Playbook-v2.md`, gabarit W43) restent supérieures en cas de conflit, et les verrous
client (aucun prix, aucun délai sans condition, aucun avis inventé) ne se négocient pas parce qu'un
skill propose un modèle.

## Limites

Ce sont des prompts de méthode, pas des données : aucun ne connaît le Cameroun, l'optique, ni nos
marges. Rien n'y est vérifié.

Réinstallation : `bash tools/marketingskills/install.sh`.
