# BRAINSTORM — LES SUPER-POUVOIRS D'AMK

```
Étape 0   graphe rejoué le 25/10 à 23:39 → 12 496 nœuds · 15 815 arêtes (carte : ops/REPO-MAP.md)
          lue : §0 une page, §1 couche connaissance, §2 les 20 plus cités, §3 périmés, §3 bis orphelins,
          §4 communautés, §6 routage · ask « superpower brainstorm — ce que le dépôt sait faire que
          personne d'autre ne fait, et quelle pièce ensuite » → 161 documents, 6 retenus
Puis      PRE-FLIGHT.md lu · §0b/§0c sans objet (aucun dossier client ouvert ce tour)
Skill     tools/superpowers/skills/brainstorming/SKILL.md (usage tracé dans ~/.amk-provisioned/usage.log)
But       ne rien construire avant d'avoir écrit ce que King veut vraiment — puis proposer, pas livrer au hasard
```

## 1 · Ce que le graphe dit qu'on possède (chiffres de la carte, pas d'impression)

| Ce qu'on a | La mesure | Où c'est |
|---|---|---|
| Un graphe du dépôt, rejouable à l'octet | **12 496 nœuds · 15 815 arêtes**, 786 documents, 183 scripts | `tools/graphify/build_full_graph.py` |
| Un réseau de citations, pas une liste de fichiers | **3 382 citations** (2 732 en chemin exact, 650 par nom unique) | `ops/REPO-MAP.md` §2 |
| Une mémoire qui sert vraiment | `sales/Activity-Log.md` cité **197 fois** — c'est le pivot de la communauté 1 | §2 |
| Des règles **exécutables**, pas des conseils | **4 portes · 71 cas de test** : `audit_ideas` 21, `audit_hook` 23, `audit_trust` 15, `audit_reel` 12 | `tools/qa/` |
| Un rendu vidéo local, sans réseau ni clé | 24 s de master en **~30 s** (28 s mesurées ce tour) | `content/reels/reelkit.py` |
| Une doctrine qui vient de sources nommées et datées | 10 documents dans `knowledge/` ; les sources **tier C/D** sont refusées ou marquées | `knowledge/` + §9 de chaque doc |
| Un plan de contenu qui n'est pas une liste d'envies | la **grille 331** : 9 cases, une dixième après la donnée | `content/ideas/GRID-331-2026-10-25.md` |

**Le super-pouvoir n'est aucun de ces objets pris seul.** C'est la chaîne : *une règle écrite → une porte
qui la refuse → une pièce qui passe la porte → une trace datée de ce qui a été refusé*. Personne à Douala
ne vend un site avec **la liste de ce qu'il a refusé de promettre**. C'est vérifiable, et c'est déjà là.

## 2 · Ce que le graphe dit qu'on n'a pas (et qui bloque)

1. **Les masters disparaissent.** Les `*.mp4` sont gitignorés : le master d'EP01 v4 rendu hier soir
   **n'existait plus** ce matin (constaté, pas supposé). 1,8 Mo de travail évaporés, 30 s à refaire —
   mais **King ne peut pas le regarder** s'il n'est pas devant le bac. Le graphe compte « 3 vidéos »
   suivies : le livrable vidéo, lui, n'est pas suivi du tout.
2. **415 documents que personne ne cite** (109 à traiter : 49 dans `tools/`, 19 dans `content/`, 9 dans
   `ops/`). `ops/UNIT-ECONOMICS-2026-10.md` en est un : l'économie unitaire est écrite et inatteignable.
3. **La communauté contenu (30 documents) ne touche pas la communauté vente.** On sait fabriquer des
   pièces ; on ne sait pas encore relier une pièce à un devis, un devis à un client.
4. **Aucune donnée de performance.** La grille a 9 cases et **zéro chiffre** : la dixième reste ouverte,
   et la porte l'affiche à chaque exécution — c'est honnête, ce n'est pas un plan.
5. **Le tuyau 2 est bloqué par une ressource humaine** : les 45 minutes de watchlist (`IDEA-PIPES` §8).
   Aucun outil ne le débloque ; le dire est plus utile que le simuler.

## 3 · Les trois approches (chacune est un pari différent, pas une variante)

### A · « Les neuf d'abord » — remplir la grille avant tout
Produire les 8 cases restantes, une par jour, dans l'ordre du tableau.
- **Coût** : ~1 h par case (script + portes + rendu), donc 8 jours pleins.
- **Ce que ça prouve** : qu'on tient une cadence sans se répéter.
- **Le risque, et il est sérieux** : **produire sans publier**. Neuf pièces au sol et zéro donnée
  laissent la dixième ouverte — exactement l'état d'aujourd'hui, en plus lourd.

### B · « Le dossier de preuve » — transformer les portes en actif client *(recommandée)*
Chaque pièce (et chaque site livré) repart avec **une page de preuve** : les sources datées, les quatre
portes et leur verdict, **ce qui a été refusé** (urgence, promesse, chiffre inventé), et les mesures.
- **Coût** : faible — les portes tournent déjà, il ne manque que l'écriture du dossier.
- **Ce que ça prouve** : ce que nous vendons n'est pas une opinion. Et ça se démontre **sur EP01 v4 ce
  soir**, pas dans un mois.
- **Pourquoi c'est le super-pouvoir** : c'est le seul actif du dépôt qu'un concurrent ne peut pas copier
  en une soirée — il faudrait qu'il ait aussi ses propres refus, datés.
- **Le risque** : un dossier de preuve sur une pièce que personne n'a vue ne prouve rien. **B ne remplace
  pas la publication, il l'accompagne** — donc B puis A, jamais B au lieu de A.

### C · « Le tuyau 2 d'abord » — débloquer la recherche avant de produire
Ne rien rendre avant d'avoir les 45 minutes de watchlist (les vidéos qui marchent chez d'autres).
- **Coût** : nul pour moi, **entier pour King** (c'est du temps humain, non délégable).
- **Ce que ça prouve** : qu'on ne tire pas de plans sur la comète.
- **Le risque** : c'est un blocage **externe**. En attendant, on ne produit rien — et la grille reste
  à 1/9. C'est déjà le cas depuis ce matin.

**Recommandation : B, appliqué à EP01 v4 tout de suite, puis A en publiant chaque case avec son dossier.**
C part quand King a 45 minutes ; ça ne se planifie pas à sa place.

## 4 · Ce que je ne peux pas décider seul

Le seul point que la demande de King laisse ouvert, et qui change **tout** ce qui sera construit :

> **EP01 v4 part-il mardi 27/10 comme prévu — ou attends-tu que le dossier de preuve soit attaché ?**

- S'il part **mardi** : je construis le dossier de preuve **des huit cases suivantes** d'abord, et la v4
  part avec un dossier rétroactif (les portes tournent, les chiffres existent déjà).
- S'il **attend** : je construis le dossier d'EP01 v4 en premier, et la publication glisse — avec le
  risque connu : une semaine de plus sans donnée, donc une dixième qui reste ouverte.

Deuxième question, plus petite, si King a une minute : **le dossier de preuve est-il pour nous (interne,
pour décider) ou pour le client (livré avec le site) ?** Les deux se défendent ; la version client est un
argument de vente, la version interne est un journal de fabrication. Ce n'est pas le même document.

## 5 · Propositions

| # | Proposition | Coût | Ce qu'elle règle |
|---|---|---|---|
| 1 | **Rendre les masters regardables sans le bac** — `tools/ops/projection.py` sert `content/reels/` en page qui joue les vidéos | fait ce tour | « where is the mp4 » : une URL, pas un chemin |
| 2 | **Corriger le bug d'arguments de `make_ep01.py`** : `--sans-voix` devenait le nom du fichier de sortie | fait ce tour | un master de 1,6 Mo écrit dans un fichier nommé `--sans-voix` |
| 3 | **Écrire le dossier de preuve d'EP01 v4** (générateur, pas texte à la main) | ~1 h | la preuve suit la pièce |
| 4 | **Publier mardi, quoi qu'il arrive**, et saisir la donnée dans `ANALYTICS-LOG` | 10 min | la dixième case existe un jour |
| 5 | **Rapatrier 3 orphelins utiles** (`ops/UNIT-ECONOMICS-2026-10.md`, `content/pipeline/CONTENT-UNBLOCK-2026-10-05.md`, `ops/FIRST-CLIENT-PRE-MORTEM.md`) | 20 min | du savoir déjà écrit qu'aucun chemin n'atteint |

## 6 · Audit de ce document

- **Ce qui est mesuré** : tous les chiffres du §1 viennent de `ops/REPO-MAP.md` régénéré ce tour
  (12 496 nœuds) ou de l'exécution des portes (71 cas). Les deux bugs du §5 sont constatés, pas supposés.
- **Ce qui est une opinion** : le classement du §3. « B est le meilleur pari » n'est pas une mesure,
  c'est un jugement — et il repose sur une hypothèse non vérifiée : **qu'un client de Douala paie mieux
  un fournisseur qui montre ses refus**. Aucune donnée ne le prouve. Le test coûte une pièce.
- **Ce qui manque** : aucune donnée de performance depuis le 25/09. Les seuls chiffres de vues du dépôt
  sont ceux que King a rapportés (IG 47, TikTok 87…) — sans fenêtre d'observation, donc non comparables.
- **Ce que ce document ne fait pas** : il ne remplace pas `writing-plans`. Si King choisit B, le plan
  d'exécution s'écrit ensuite, avec des étapes qu'un exécutant suit sans nous.
