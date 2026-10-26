# BRAINSTORM — 26/10/2026 (tour 155) · commencer la prospection, aujourd'hui

```text
Étape 0  graphe rejoué 26/10 10:42 (12 856 nœuds) · carte lue §0/§6/§2/§3
Demande  King : « now let's begin outreach, lead scout, lead verifier, then personalized outreach
         message, web design if the customer says yes » — et, plus tard le même jour, « we send
         between 20-50 ».
Méthode  preflight.sh → PRE-FLIGHT.md §00 → superpowers/brainstorming
```

## 1 · Ce que le dépôt avait déjà tranché

| Fait | Source | Conséquence |
|---|---|---|
| Le flux en cinq étapes existe : scout → vérifier → construire → écrire → personnaliser sur réponse | `docs/superpowers/specs/2026-10-24-flux-prospection-design.md` §1 | rien à inventer : il faut l'**exécuter** |
| **Aucun message sans les trois portes** §8b : A joignabilité WhatsApp · B intention numérique · C acheteur | `sales/RESEARCH-STANDARD.md` §8b | 3/3 = envoi · 2/3 = King tranche · 1/3 = jamais |
| **Une preuve datée par affirmation** ; un site dédié qui vit = hors cible | §8c | on n'écrit pas « vous n'avez pas de site » sans l'avoir vérifié |
| L'**opticien** est la verticale : 28 % de réponses humaines contre 0 % en clinique | `flux-prospection` §2 | on ne rouvre pas le débat aujourd'hui |
| **Aucun site par prospect avant sa réponse** ; 15 aperçus construits pour 1 client payant, retirés | `flux-prospection` §3 | la page arrive **après** le oui |
| Une seule relance, à J+7, et seulement sur message lu | `CLIENT-MESSAGING-RULES` §13 | un silence de 48 h ne se relance pas |

## 2 · Ce que le scout et le vérificateur ont trouvé dans le CRM, en le lisant

| Résultat | Nombre | Ce que ça veut dire |
|---|---|---|
| lignes jamais touchées, gardées par le scout | **77** (113 exclues avec leur raison) | la matière première existe ; elle n'était pas triée |
| dont profil ouvert sur WhatsApp le 25/10 | **17** ✅ (+ 2 ⚠️, 0 ⛔) | la porte A est un geste de la veille, pas d'aujourd'hui |
| **3/3 → on écrit** | **7** | porte A vue + porte B datée + acheteur nommé |
| 2/3 → King tranche | **9** | porte B sans preuve : il manque une capture |
| 1/3 → on n'écrit pas à l'aveugle | **61** | jamais vues sur WhatsApp : elles attendent King, pas un message |

**Le fait qui a décidé de la journée** : ces 17 lignes dont le numéro avait été **vu sur WhatsApp le
25/10** existaient depuis la veille. Le lot du matin (49 messages fabriqués) en utilisait deux. Le
goulot n'était pas la vérification — c'était de ne pas regarder la colonne.

**Et le second fait, plus dur** : les 49 messages fabriqués le matin contenaient **neuf** cabinets à
2/3 et **un** à 1/3, sans le dire. Le vérificateur le dit maintenant (`leads/VERIF-2026-10-26.md` §5),
et le lot a été refait sur 42 lignes avec les sept 3/3 sortis et écrits à la main.

## 3 · Les trois options

| | **A — envoyer les 7 en tête du palier de 20** | **B — fermer la porte B des 10 d'abord** | **C — changer de verticale pour le test** |
|---|---|---|---|
| Ce qu'on gagne | la seule chose qui produit une réponse : envoyer | 17 pistes au lieu de 7, lot homogène | un bras de comparaison propre |
| Ce qu'on perd | 10 pistes attendent | 100 minutes de captures **avant** le premier envoi, zéro donnée ce soir | la seule verticale à 28 %, et le seul client signé |
| Le risque | un lot de 7 sur un marché de 75 | on optimise pendant que le téléphone sonne pour rien | griller 5 cliniques sur une thèse déjà écrite |

## 4 · Recommandation : **A**, et **B en parallèle**

**A parce que le goulot n'est pas la liste, c'est le taux de réponse.** 77 pistes jamais contactées et
sept messages prouvés : la contrainte est le **temps de King**, pas le nombre de noms. Les sept partent
le 27/10, d'affilée, en tête de la journée de 20 — un jour de données, pas sept.

**B en parallèle, pas avant** : les neuf captures de la porte B se prennent **pendant** que ① part.
Chaque capture transforme une piste `KING-TRANCHE` en `ENVOYER` pour la vague suivante.

**C refusé aujourd'hui** : la clinique a été testée (0/15 de réponses humaines) et le bras de contrôle
du 24/10 s'est aminci tout seul — sur les six messages du lot du 26/10, **trois numéros étaient morts**.

## 5 · Ce que le « oui » déclenche, et qui est écrit

`sales/REPONSE-OUI-2026-10-26.md` : la page du prospect en **24 h**, en huit gestes, avec les portiques
du §1b et la revue de King. Aucun site n'est construit avant la réponse (spec du 24/10 §3).

## 6 · Ce qui a été construit pour que ce ne soit pas un vœu

| Outil | Ce qu'il fait | Ce qu'il refuse |
|---|---|---|
| `tools/outreach/scout.py scout` | lit le CRM, garde les lignes jamais touchées, écrit la raison de chaque exclusion | il ne réécrit jamais le CRM |
| `tools/outreach/scout.py verify` | applique les trois portes à partir des **captures datées** | il ne visite aucun site et n'appelle aucun numéro : sans preuve, la porte reste `inconnue` |
| `tools/outreach/compose.py` | écrit les messages à volume (42 ici) | il refuse un lot qui contient un motif répété |
| `tools/qa/audit_outreach.py` | juge chaque message et **le lot** (§10) | il ne juge pas la vérité du fait — c'est le §8c |

**Bancs** : `test_scout.py` (9 cas) et `test_compose.py` (10 cas), dont la famille qui compte — sur le
vrai CRM, **sept ENVOYER et pas huit**, avec les bons noms.
