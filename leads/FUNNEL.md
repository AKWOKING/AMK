# ENTONNOIR — où le système fuit

> ⚙️ **Généré le 2026-09-24 par `leads/build/views.py` — ne pas modifier à la main.**
> Toute correction se fait dans `leads/build/crm.py` ou `sales/Activity-Log.md`, puis on relance `leads/build/rebuild.sh`.

## La chaîne

| Étape | Nombre | Taux |
|---|---|---|
| Base (leads au fichier) | **163** | — |
| Contactés | **62** | 38.0 % de la base |
| Réponses humaines | **6** | 9.7 % des contactés |
| Réponses automatiques | 1 | — |
| Aperçus produits | **21** | (hors chaîne : souvent produits AVANT contact) |
| Prix posé / en négociation | **3** | 14.3 % des aperçus |
| Clients payants | **0** | — |

## Par source — c'est ici qu'on voit quelle source vaut le travail

| Source | Leads | Contactés | Réponses humaines | Taux de réponse |
|---|---|---|---|---|
| directory | 109 | 55 | **6** | 10.9 % |
| (non renseigné) | 38 | 4 | **0** | 0.0 % |
| google_maps | 2 | 2 | **0** | 0.0 % |
| content_video | 1 | 1 | **0** | 0.0 % |
| walk_in | 1 | 0 | **0** | — |
| pass_vitrine | 4 | 0 | **0** | — |
| onoc_registry | 7 | 0 | **0** | — |
| facebook | 1 | 0 | **0** | — |

## Le diagnostic, en trois lignes

1. **Le volume contacté est le premier goulot** : 101 lead(s) sur 163 n'ont jamais reçu un message (62 % de la base). Aucune amélioration de texte ne compense un lead jamais contacté.
2. **Le taux de réponse humain** est de 9.7 % des contactés — c'est le chiffre à surveiller d'un envoi à l'autre (il se lit avec `SOURCES.md` : quelle liste répond).
3. **La conversion en rendez-vous, elle, ne fuit pas** : 3 des 6 réponses humaines ont donné un rendez-vous ou un prix posé. Le travail n'est donc pas de « mieux closer », il est de **contacter plus**, et de choisir les bonnes listes.

> Règle de lecture : une réponse automatique n'est PAS une réponse. Un aperçu produit n'est pas un prospect chaud — il se compte à part, et `Demo made` ne remplace jamais `reply_type = human`.

