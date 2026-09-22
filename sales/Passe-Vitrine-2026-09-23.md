# LA PASSE « VITRINE » — mercredi 23/09/2026
**Objectif : remplir `Website` et `Facebook` sur les 104 leads santé/optique jamais vérifiés, et sortir de
là la prochaine liste d'envoi.** C'est la seule tâche qui fabrique des prospects frais, et c'est elle qui a
été demandée par King (« I prefer spending time on fresh prospects »).

## Pourquoi cette colonne et pas une autre

Mesuré sur les 145 leads du CRM (`sales/PROFIL-DES-OUI-2026-09-22.md`) :

| | réponses / leads | taux |
|---|---|---|
| lead **avec une vitrine à lui** (domaine ou page FB) | 3/27 | **11,1 %** |
| lead **sans aucune vitrine** | 3/118 | 2,5 % |
| les 33 fils classés morts le 22/09 | **0/33** | **0 %** |
| ville, secteur, soin du message | — | ~0 point d'écart |

Et le trou : la colonne `Website` n'est renseignée que pour **2 des 106** leads santé/optique (Les Cristallin
et Univers, vérifiés à la main). Les 39 écoles, elles, sont auditées 39/39 — c'est d'ailleurs là qu'on a vu le
motif pour la première fois.

## Ce qu'on remplit, exactement

Une seule colonne compte, avec **trois valeurs possibles** :

| `Website` | Ce que ça veut dire | Suite |
|---|---|---|
| `domaine.com — VIVANT` (+ date de lecture) | site en ligne, à refaire ou à réparer | **lead du profil** — priorité 1 |
| `domaine.com — MORT (aucun DNS / dernière copie <date>)` | il a payé, ça ne marche plus | **lead du profil** — priorité 1 (douleur prouvée) |
| `none found` | rien à lui | réserve, pas de premier message |
| *(vide)* | **on n'a pas regardé** | interdit après cette passe |

`Facebook` : même logique, mais seulement `page <nom>` ou `none found` — **jamais** une page homonyme
(l'erreur d'Univers : la page de 508 likes était « Global trade invesment »).

## La recette, 60 à 90 secondes par lead

1. Rechercher `"<nom exact>" <ville>` puis, si rien, `"<nom>" Cameroun`.
2. Noter ce qu'on trouve, **sans l'interpréter** : un domaine (vivant/mort), une page FB au nom de
   l'établissement, une fiche d'annuaire (mondocteur, maligah, ONOC/réseaux de soins), ou rien.
3. Vérifier une seule chose si un domaine apparaît : **la page s'ouvre-t-elle ?** (un domaine mort = le
   fait le plus vendeur de la campagne, cf. Univers).
4. Écrire la valeur dans la source, jamais dans le CSV.
5. **Ne rien déduire de l'absence** : « rien trouvé » se note `none found` et ne s'écrit jamais au prospect
   comme une affirmation (règle du 22/09, apprise trois fois en une journée).

## Le découpage, pour que ça tienne en une matinée

| Lot | Contenu | Durée visée |
|---|---|---|
| 1 | les 20 labos d'analyses jamais vérifiés | ~30 min |
| 2 | les 20 cliniques / centres médicaux | ~30 min |
| 3 | les 20 opticiens | ~30 min |
| 4 | les 20 suivants (mélange) | ~30 min |
| 5 | les 24 restants + relecture du compte | ~35 min |

À la fin de chaque lot : `python3 leads/build/guard.py lock` puis `bash leads/build/rebuild.sh`, et on relit
le plan — **un lot qui ne change pas le plan n'a rien produit**.

## Les critères d'acceptation de la passe

1. **Zéro case vide** dans `Website` sur les 104 (ou `none found` explicite : ce n'est pas un vide, c'est une
   réponse).
2. Un **compte** qui tombe juste : nombre de leads du profil trouvés, nombre de domaines morts, nombre de
   pages FB.
3. La prochaine vague d'envoi est **100 % issue du profil** (vitrine à soi) — c'est le test de falsification
   écrit le 22/09 : ≥ 4 réponses sur 30 = le profil est une loi ; ≤ 2 = c'était une coïncidence de six cas.
4. Aucun score de « lecture » utilisé comme preuve d'intérêt (leçon des 33 morts du 22/09).

## Ce qu'on ne fait plus, à partir de maintenant

- Plus de premier message vers un lead **sans aucune vitrine** : 0/33 le 22/09, 2,5 % sur l'ensemble.
- Plus de message qui **affirme** une absence (« vous n'êtes pas trouvable ») ni une lecture (« vous avez
  ouvert ») : une seule affirmation non vérifiée efface tout le message.
- Plus de secteur « prometteur » sans vitrine : labo 5,9 %, optique 4,5 %, clinique 4,2 % — le secteur ne
  prédit rien, la vitrine prédit.
