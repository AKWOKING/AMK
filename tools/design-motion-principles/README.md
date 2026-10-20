# design-motion-principles — motion d'interface (installé le 20/10/2026, demande King)

Amont : <https://github.com/kylezantos/design-motion-principles> (MIT) · épinglé
`4a9ca879f24a361f4dca4174fe2da0f67b5ddee3`. Un seul skill, **`design-motion-principles`** :
motion design lu par trois lentilles (Emil Kowalski = retenue/vitesse, Jakub Krehel = polish de
production, Jhey Tompkins = expérimentation), pondérées selon le contexte du projet.

## Ce que c'est

- `SKILL.md` : routeur **Create** (construire des composants animés) / **Audit** (relire le motion
  existant), porte de fréquence (rare/occasionnel/fréquent/clavier), durées par contexte.
- `workflows/audit.md` : reconnaissance → pondération des lentilles → audit complet → rapport
  (HTML avec démos chez l'amont ; ici : consigné dans les build-notes du client, voir garde-fous).
- `references/` : checklist d'audit, anti-checklist « AI-slop motion » (pulsing indicators,
  hover-scale-on-everything, stagger-spam, uniform fade-ins…), accessibilité
  (`prefers-reduced-motion` obligatoire), performance (transform/opacity, `will-change` ciblé),
  cookbook de recettes et les trois philosophies.
- **Aucun code exécutable** : markdown + gabarits HTML de rapport. Rien ne tourne, rien n'appelle
  le réseau (les gabarits de rapport de l'amont chargent des polices Google — non utilisés ici).

## Installation (reproductible)

```bash
bash tools/design-motion-principles/install.sh
```

Clone épinglé dans `~/.design-motion-principles`, liens vers `~/.claude/skills/` et
`~/.agents/skills/`, preuve par lecture des fichiers installés. Aucun sudo, rien de l'amont
dans le dépôt.

## État dans cette sandbox (vérifié le 20/10, appels réels)

- ✅ Clone au pin `4a9ca87`, liens résolus des deux côtés, `SKILL.md` + workflow d'audit +
  références (audit/anti-checklist, Emil, Jakub, accessibilité, performance) lus en entier.
- ✅ Premier usage fait : audit motion de DM Optique v2 (voir ci-dessous).

## Premier usage (20/10) — audit motion DM Optique v2

Pondération appliquée (site santé, catalogue, conversion WhatsApp, public qui vient pour ses
yeux) : **Jakub primaire** (polish de production), **Emil secondaire** (retenue sur les gestes
fréquents : CTA, filtres, formulaires), **Jhey sélectif** (aucun moment ludique recommandé).
Constats principaux (détail + correctifs : `clients/dm-optic/build-notes.md`, audit combiné) :
`prefers-reduced-motion` présent et complet ; contrôles rapides (120–280 ms, feedback `scale`
au `:active`) ; mais lavis d'ambiance en boucle infinie non pausable (26 s/32 s), révélation
`.rv` uniforme de 620 ms jusque sur le texte statique, skiplink qui anime `top` (layout +
déclenché au clavier), survol qui soulève une carte non interactive, et panneaux/FAQ/résultats
qui basculent instantanément (acceptable en fréquence, à polir seulement si King le demande).
**Aucun changement de site ce tour** : audit seulement, les correctifs motion sont des
changements de design → ruling King, puis portiques §1b + redéploiement §1f③.

## Garde-fous AMK

- Les lois maison (`AMK-DESIGN-SKILLS.md`) et les verrous client gagnent en cas de conflit ;
  on signale, on ne restyle pas en silence. Le skill juge le motion, pas l'identité.
- Pas de rapport HTML `motion-audits/` généré dans le dépôt (PRE-FLIGHT §4b : pas de nouveau
  fichier debout sans l'OK de King) ; les findings vivent dans les build-notes du client.
- `prefers-reduced-motion` est non négociable sur nos pages (déjà la règle maison) ;
  aucun motion nouveau sans sa variante réduite.
- Règle debout : `PRE-FLIGHT.md` §1f⑤. Production = première application relue par King
  (TOOL-SCAN règle 3).
