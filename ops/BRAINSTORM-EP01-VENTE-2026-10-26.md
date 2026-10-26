# BRAINSTORM — EP01 : le rendre humain, et lui donner une raison de cliquer

```
Étape 0   graphe rejoué le 26/10 à 00:36 → 12 600 nœuds · 15 971 arêtes (ops/REPO-MAP.md)
          ask « humanizer tics écriture IA phrases robotiques » → 32 documents
          ask « réciprocité rareté preuve sociale autorité Cialdini conversion CTA » → 116 documents
Puis      PRE-FLIGHT.md lu · §0b sans objet · §0c knowledge/ (HOOKS, CONTENT-CREATION, HOUSE §8)
Skill     brainstorming (tracé) · humanizer (pin 8c307f3, 26 motifs « Signs of AI writing »)
Entrées   King : « ça sonne robotique » · « écrivez APERÇU pour faire quoi ? » · les 5 tactiques de vente
But       décider ce qu'on change AVANT de le changer — et dire ce qu'on refuse de changer
```

## 1 · Ce que King a dit, en trois phrases distinctes

1. **« less robotic and more human »** — un problème de **langue**, pas de structure. La v5 est
   correctement ordonnée (porte du récit ✓) et parle comme un panneau de signalisation.
2. **« écrivez APERÇU … to do what ?? »** — un problème de **promesse**. Le CTA nomme l'action et tait
   la récompense. Dans un fil WhatsApp, le message d'accueil explique ; dans une vidéo de 24 s,
   personne ne l'a sous les yeux. **Le CTA doit porter sa propre explication.**
3. **Les cinq tactiques** — un problème de **levier**. Le script constate ; il ne fait rien désirer.

Trois problèmes, trois remèdes différents. Le risque de ce tour est de les mélanger : réécrire « plus
humain » en glissant des tactiques dedans produirait exactement le ton de vendeur qu'on fuit.

## 2 · Ce que le graphe dit qu'on a déjà (et qu'on a sous-utilisé)

| Ce qu'on possède | Où | Pourquoi ça n'a pas servi |
|---|---|---|
| **`humanizer`** (26 motifs, MIT, épinglé) | `tools/humanizer` → `~/.agents/skills/humanizer` | installé le 20/10, jamais passé sur une pièce vidéo |
| **La voix de la copie camerounaise** : « chaude, directe, spécifique — pas polie, pas formelle, pas IA-sonnante » | `HOUSE-KNOWLEDGE-BASE` §8 | appliquée aux messages, pas aux scripts |
| **Erhart B2** (micro-accords, double contrainte) et **B10** (l'offre en une phrase) | `AMK-Sales-Playbook-v2` | playbook de vente, jamais transposé en 25 s |
| **Les trois phrases plates** (risque inversé : « je ne demande rien avant votre accord ») | `MESSAGES-2026-09-23-PERSUASION` §8 | jamais dites à l'écran |
| **Le message d'accueil APERÇU** | `PLAYBOOK` §4.2 | il explique le CTA… **ailleurs que là où le CTA est vu** |

**Le constat** : le dépôt sait déjà faire les trois choses demandées, séparément. Ce qui manque, c'est
un endroit où elles se rencontrent : une **pièce**, pas un document de plus.

## 3 · Les trois approches

### A · Humaniser seulement (la demande littérale, prise au mot)
Passer le script au `humanizer`, garder l'ordre et le CTA.
- **Coût** : 20 min. **Ce que ça prouve** : que le ton peut changer.
- **Le risque** : on garde le défaut que King a signalé en deuxième — un CTA qui ne promet rien. Une
  phrase plus humaine qui ne dit toujours pas ce qu'on obtient reste une phrase qui ne fait pas agir.

### B · Humaniser **puis** armer (les 5 tactiques filtrées), **puis** réécrire le CTA *(recommandée)*
1. `humanizer` d'abord, sur le texte v5, pour tuer les tics (deux-points en série, triades, fragments
   théâtraux, ouvertures parallèles).
2. Les **5 tactiques** passées au crible du format : trois tiennent dans 25 s, deux n'y tiennent pas
   sans mentir (voir `knowledge/SALES-5-TACTICS-2026-10-26.md`).
3. Le **CTA** réécrit pour porter sa récompense : ce qu'on reçoit, et à quelle condition.
- **Coût** : ~1 h 30 avec le rendu. **Ce que ça prouve** : que le ton, le levier et la promesse peuvent
  tenir dans la même phrase.
- **Le risque** : surcharger. Garde-fou : **le texte final ne contient aucun mot que l'opticien
  n'emploierait pas lui-même**, et la porte du récit refuse tout ce qui dépasse 7 beats.

### C · Recommencer le concept (autre angle, autre personnage, autre histoire)
- **Coût** : une demi-journée. **Ce que ça prouve** : qu'on sait repartir de zéro.
- **Le risque, et il est déjà mesuré** : six versions en deux jours, **zéro vue mesurée**. Le problème
  n'est pas le concept, il est dans la langue et dans la clôture. Changer de concept, c'est payer pour
  ne pas répondre à la question posée.

**Recommandation : B.** Et une condition, écrite d'avance : si la v6 n'est pas **audiblement** meilleure
que la v5 dans les trois secondes, on garde la v5 et on publie mardi.

## 4 · Ce que je ne peux pas décider seul

> **Le CTA promet une page. King propose de promettre aussi la fiche Google (« on vous crée votre fiche
> Google »). Laquelle des deux entre dans la vidéo ?**

Ce n'est pas une question de goût : **créer** une fiche Google Business suppose une vérification
(courrier, téléphone, parfois refusée) que nous ne contrôlons pas. Le dépôt ne promet nulle part ce
service, et `MESSAGES` §2 existe précisément parce qu'un lien a déjà promis plus que la page. Trois
options, et je recommande la troisième :

| Option | Ce que le CTA dit | Le risque |
|---|---|---|
| 1 · page seule | « Écrivez APERÇU. Vous voyez votre page avant de payer. » | vrai, mais ne répond pas à « pour faire quoi » au-delà de la page |
| 2 · fiche promise | « Écrivez APERÇU, on vous crée votre fiche Google. » | **promesse non tenue** si la vérification échoue |
| 3 · fiche **regardée** *(recommandée)* | « Écrivez APERÇU. On regarde votre fiche, et je vous montre votre page. » | honnête, et la fiche entre quand même dans la conversation |

La version 3 garde l'idée de King (la fiche est nommée, donc le bénéfice est concret) sans promettre un
résultat que Google décide. **Si King veut la version 2, il tranche** — c'est son nom sur le message.

## 5 · Propositions

| # | Proposition | Coût | Ce qu'elle règle |
|---|---|---|---|
| 1 | `knowledge/SALES-5-TACTICS-2026-10-26.md` : les 5 tactiques, ce qui tient en 25 s, ce qu'on refuse | 30 min | une doctrine réutilisable sur les 8 cases de la grille |
| 2 | La v6 humanisée + armée + CTA qui dit ce qu'on reçoit | 40 min + rendu | les trois reproches de King |
| 3 | Le **Roast Room** sur hooks / CTA / conversion | 30 min | un second avis **avant** de rendre, pas après |
| 4 | La v5 conservée comme filet | 0 | la règle qui a sauvé le tour précédent |
| 5 | Publier mardi, quoi qu'il arrive | 0 | sans donnée, aucune version ne sera jamais « prête » |

## 6 · Audit de ce document

- **Mesuré** : 12 600 nœuds, 32 et 116 documents retrouvés par `ask`, les six textes de la v5 et leurs
  durées (`timing.json`), le pin `8c307f3` du skill humanizer.
- **Jugement** : le classement B > C > A est une opinion. Elle repose sur une hypothèse non vérifiée —
  qu'un CTA qui nomme sa récompense convertit mieux qu'un CTA qui nomme seulement l'action. C'est
  plausible, ce n'est pas mesuré chez nous.
- **Absent** : **aucun taux de conversion réel**. Le dépôt n'a ni vue ni clic ni message compté pour
  EP01. Tout chiffre de conversion produit ce tour serait inventé ; le Roast Room note donc le
  **potentiel** de conversion sur une grille, pas un taux.
