# PORTE B — la feuille de route de 20 minutes (27/10/2026)

```text
MESURE   python3 tools/outreach/verify.py --date 2026-10-27
         → 7 ENVOYER · 19 KING-TRANCHE · 14 hors cible · 17 jamais · 20 sans porte
CE QUE ÇA DIT  la porte A est faite (numéros vus le 25/10), la porte C est faite (titulaire nommé),
         et il manque **une seule chose** sur 19 lignes : une date qui prouve qu'ils agissent en ligne.
CE QUE ÇA VAUT  19 lignes = 19 messages = la journée du 27/10 entière, sans chercher un numéro de plus.
```

## 1 · Pourquoi c'est bloqué, en une phrase

Le §8b exige, pour écrire, **trois preuves** : le numéro joint WhatsApp (**A** — fait le 25/10), l'organisme
**agit encore** en ligne (**B** — manquante), et l'on parle au **titulaire** (**C** — fait, le nom est au
CRM). Sans B, la règle ne dit pas « écris quand même » : elle dit **stationne**. Dix-neuf cabinets sont
stationnés pour une date.

## 2 · Ce que tu fais, cabinet par cabinet (1 minute chacun)

Pour chaque ligne du tableau :

1. Ouvre **Facebook**, tape le **nom exact** du cabinet + `Douala`. (Puis Google, si Facebook ne donne rien.)
2. Regarde **une seule chose** : la **date du dernier post** (ou du dernier avis sur Google).
3. Écris cette date dans `leads/PREUVES-2026-10-27.csv`, colonne `vu_le`, au format `2026-09-12`.

**Trois issues, et trois seulement :**

| Ce que tu vois | `type` | `preuve` | Ce que ça produit |
|---|---|---|---|
| une page qui a posté **il y a moins d'un an** | `facebook` | `dernier post 2026-09-12` | **porte B ouverte** → message autorisé |
| une page qui a posté **il y a plus d'un an** | `facebook` | `dernier post 2021-04-03` | **porte B fermée** → stationné dormant, on n'écrit pas |
| aucune page, aucun avis, rien | `aucun` | `rien trouvé le 27/10` | reste `inconnu` → rien ne part, et c'est noté |

> **Ne devine pas.** Une page « qui existe » sans date ne prouve pas qu'elle vit. C'est la date qui
> ouvre la porte, pas la page.

## 3 · Les 19 lignes, déjà prêtes

| Cabinet | Numéro | Ce qui manque |
|---|---|---|
| Alpha Optic | 699 57 34 57 | B |
| Bishop Jules Peters Memorial College | 683 34 88 56 | B |
| Class-Optic | 691 17 18 17 | B |
| Emeraude Optique Sarl | 699 90 99 60 | B |
| Espace Vision | 677 33 94 24 | B |
| Gift Optical | 673 52 17 35 | B |
| La Fierté de l'Optique | 695 17 90 57 | B |
| La Lunetterie Médicale El Shadai | 696 89 64 11 | B **et** A (ligne personnelle, sans nom d'établissement) |
| Light Optique | 677 64 87 90 | B |
| Lux Optique | 655 04 05 49 | B |
| Maranatha Optics | 658 16 31 90 | B |
| One Stop Medical Laboratory & Diagnostics | 691 63 29 41 | B |
| Optique Pro | 690 03 48 18 | B |
| Pagrot Optique | 699 90 46 91 | B |
| Presbyterian Comprehensive Secondary School (PCSS) Buea | 652 07 52 29 | B |
| Saoudia Optique | 696 04 04 13 | B |
| Solidarity Health Foundation (Solidarity Clinic & Laboratory) | 677 61 57 57 | B |
| St. Joseph's College Sasse (SJC Sasse) | 677 19 55 00 | B |
| World Vision | 656 03 21 72 | B |

*(Tableau engendré depuis `leads/VERIF-2026-10-27.json` — aucun numéro recopié à la main. Le CSV
`leads/PREUVES-2026-10-27.csv` porte les mêmes lignes, avec leur slug.)*

## 4 · Puis, une seule commande

```bash
python3 tools/outreach/verify.py --date 2026-10-27
python3 tools/outreach/compose.py plan --volume 20 --verif leads/VERIF-2026-10-27.json
```

La première relit les preuves et redonne le verdict. La seconde dit combien de messages la fabrique peut
écrire **avec le droit d'écrire** — pas seulement avec un numéro.

## 5 · Ce que ça change

| Aujourd'hui, sans porte B | Après 20 minutes de dates |
|---|---|
| 7 messages autorisés (les sept du 27/10) | jusqu'à **26** |
| plan 20 · 22 · 11 · **0** | plan 20 · 22 · 22 · 20 |
| lundi 30/10 : plus rien à envoyer | la semaine tient sans un numéro de plus |

**Et c'est plus efficace que de chercher de nouveaux numéros.** Un numéro de plus demande A (8 s), B
(1 min) et C (souvent inconnu) ; ici, **A et C sont déjà faits** : il ne reste qu'une date à trouver.

## 6 · Ce qui reste vrai après

- **La porte B n'est pas une formalité.** Un cabinet dont la page n'a pas bougé depuis 2021 est un
  cabinet qui ne décidera rien : lui écrire coûte un message et rapporte zéro (règle du 18/09).
- **Le §8c s'applique toujours** avant d'écrire un fait : nom exact + ville, domaine réel, adresse et
  horaires. Une affirmation fausse coûte le meilleur prospect de la liste — c'est arrivé le 24/09.
- **Une piste à 2/3 ne part jamais par défaut.** Si tu décides d'envoyer quand même, la raison s'écrit
  à côté de la ligne, datée. C'est le ruling du 17/09, il n'a pas changé.
