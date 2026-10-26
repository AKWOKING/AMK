# Brainstorm — 26/10/2026 (tour 154, 12 h 10) · commencer la prospection, aujourd'hui

> ⚠️ **Le même jour, quatre heures plus tard**, King a renversé la cadence : « we can't be sending just
> 1 message per day, we send between 20-50 ». Ce document reste valable pour le **tri** (scout,
> vérificateur, sept pistes à 3/3) ; sa recommandation « un message par jour » est **remplacée** par
> `ops/BRAINSTORM-VOLUME-2026-10-26.md` et `sales/CAMPAGNE-VOLUME-2026-10-26.md`.

```text
Demande   King : « now let's begin outreach, lead scout, lead verifier, then personalized outreach message,
          web design if the customer says yes »
Contexte  la v6 est publiée (TikTok + Instagram + commentaire épinglé). Le lot du 26/10 est presque épuisé :
          Optix (suivi, 25/10) et COMED (26/10) — trois numéros du lot étaient morts.
Méthode   graphify (12 782 nœuds) → preflight.sh → PRE-FLIGHT.md §00 → superpowers/brainstorming
```

## Ce que le dépôt avait déjà tranché (avant toute opinion)

| Fait | Source | Conséquence |
|---|---|---|
| Le flux en cinq étapes existe : **scout → vérifier → construire → écrire → personnaliser sur réponse** | `docs/superpowers/specs/2026-10-24-flux-prospection-design.md` §1 | rien à inventer : il faut l'**exécuter** |
| **Aucun message sans les trois portes** §8b : A joignabilité WhatsApp · B intention numérique · C acheteur | `sales/RESEARCH-STANDARD.md` §8b | 3/3 = envoi · 2/3 = King tranche · 1/3 = jamais |
| **Une preuve datée par affirmation** ; un site dédié qui vit = hors cible | §8c | on n'écrit pas « vous n'avez pas de site » sans l'avoir vérifié |
| **Un message par jour** (le 2/jour a été mis au veto : drapeau spam, liste brûlée en 5 jours) | `sales/LISTE-OPTICIENS-2026-10.md`, ruling 05/10 | sept messages = sept jours |
| **Aucun site par prospect avant sa réponse** ; 15 aperçus construits pour 1 client payant | `flux-prospection` §3 | la page arrive **après** le oui, jamais avant |
| Une seule relance, **à J+7**, et seulement si le message a été lu | `CLIENT-MESSAGING-RULES` §13 (ruling 24/09) | un silence de 48 h ne se relance pas |
| **L'opticien est la verticale** : 28 % de réponses humaines contre 0 % en clinique | `flux-prospection` §2 | on ne rouvre pas le débat aujourd'hui |

## Ce que le vérificateur a trouvé dans le CRM, en le lisant (pas de mémoire)

| Résultat | Nombre | Ce que ça veut dire |
|---|---|---|
| pistes jamais contactées, avec un numéro | **62** | la matière première existe, elle n'était pas triée |
| **3/3 → envoi** | **7** | porte A vue (profil Business, 25/10) + porte B datée + acheteur propriétaire |
| **2/3 → King tranche** | **10** | porte A ✓, porte C ✓, **porte B sans preuve** : il manque une capture |
| **pas de porte A** | **44** | jamais vues sur WhatsApp : elles attendent King, pas un message |

**Les sept** : Ets Espace Médical · ASS pour RRPHDD · ISEE · Bellevue Optique · S.O.S Vision · Free Optic ·
Capelli Optique Médicale.

## Les trois options

| | **A — envoyer les 7, un par jour** | **B — fermer la porte B des 10 d'abord** | **C — changer de verticale pour le test** |
|---|---|---|---|
| Ce qu'on gagne | la seule chose qui produit une réponse : envoyer | 17 pistes au lieu de 7, et un lot homogène | un bras de comparaison propre (cliniques) |
| Ce qu'on perd | 10 pistes attendent | 100 minutes de captures **avant** le premier envoi, et zéro donnée nouvelle ce soir | la seule verticale qui a 28 % de réponse, et le seul client signé |
| Le risque | un lot de 7 sur un marché de 75 | on optimise la liste pendant que le téléphone sonne pour rien | griller 5 cliniques sur une thèse déjà écrite |

## Recommandation : **A**, et **B en parallèle**

**A parce que le goulot n'est pas la liste, c'est le taux de réponse.** 62 pistes jamais contactées et sept
messages envoyés : la contrainte est le **temps de King**, pas le nombre de noms. Envoyer sept messages à
un par jour, c'est sept jours de données — et c'est la seule chose qui nous dira si les trois portes
prédisent quelque chose.

**B en parallèle, pas avant** : les dix captures de la porte B se prennent **pendant** que ① part. Chaque
capture transforme une piste `KING-TRANCHE` en `ENVOI` pour la vague du 06/11, sans jamais retarder celle-ci.

**C refusé aujourd'hui** : la clinique a été testée (0/15 de réponses humaines, p = 0,033) et le bras de
contrôle prévu par la note du 24/10 est devenu mince — sur les six messages du lot du 26/10, **trois
numéros étaient morts**. Rejouer le bras de contrôle demande cinq numéros vivants, pas cinq messages.

## Ce que le « oui » déclenche, et qui est déjà écrit

`sales/REPONSE-OUI-2026-10-26.md` : huit gestes, **3 h de travail réel** dans une fenêtre de 24 h —
récolter les faits avec leur source, réserver le design au registre, construire depuis le gabarit DM,
passer les six portes, étiqueter la fiction, déployer sur **son** projet, et le deploy gate sur **son**
téléphone. La page ne porte jamais son nom en clair, ne promet jamais une fiche Google validée, n'annonce
jamais un prix qu'il n'a pas demandé.

## Ce qui a été construit pour que ce ne soit pas un vœu

| Outil | Ce qu'il fait | Ce qu'il refuse |
|---|---|---|
| `tools/outreach/scout.py scout` | lit le CRM, garde les pistes jamais contactées, écrit `leads/SCOUT-<date>.md` avec la raison de chaque exclusion | il ne réécrit jamais le CRM |
| `tools/outreach/scout.py verify` | applique les trois portes à partir de preuves **datées**, écrit `leads/VERIF-<date>.md` | il ne vérifie **aucun** numéro (pas de téléphone, pas de réseau) et ne visite **aucun** site ; sans preuve, la porte reste inconnue |
| `tools/qa/audit_outreach.py` | juge les sept messages | il ne juge pas la vérité du fait — c'est le §8c |

**Le banc** : `tools/outreach/test_scout.py`, **9/9**, dont la seule famille qui compte — sur le vrai CRM,
sept ENVOI et pas huit, avec les bons noms.
