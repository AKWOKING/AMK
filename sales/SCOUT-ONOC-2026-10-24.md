# Scout ONOC du 24/10 — 20 numéros d'opticiens neufs, entrés par le générateur

```text
Source     : https://onocameroun.com/annuaire-des-opticiens-par-region/  (« REGION DU LITTORAL », lignes 85–159)
Relevé     : 24/10/2026, tableau public de l'Ordre
Entrée     : leads/build/crm.py → OPTICIENS_ONOC_2410 → bash leads/build/rebuild.sh
Porte      : python3 leads/build/guard.py check  → rc 0 (empreinte des générateurs re-scellée)
Résultat   : 163 lignes inchangées à l'octet près + 21 ajoutées = 184 lignes dans leads/CRM.csv
État       : 20 mobiles prêts pour la porte A (§8b) · 1 fixe seul, gardé en trace · 0 message écrit
```

---

## 1 · Ce qui a été fait, en une phrase

Les **75 cabinets du Littoral** publiés par l'Ordre ont été recopiés, croisés avec les **61 lignes
opticien déjà au CRM** (nom normalisé *et* numéro), et les **21 cabinets absents** sont entrés dans le
générateur — jamais à la main dans le CSV, qui est écrasé à chaque rebuild.

**Marché couvert après ce scout : 82 lignes opticien au CRM** (dont 7 disqualifiées et 1 perdue),
**80 avec un numéro**, **46 jamais contactées** et jouables. La couverture du tableau du Littoral passe
donc de **54/75 à 75/75 cabinets** (75 − 21 ajoutés = les 54 déjà présents, retrouvés par nom
normalisé *ou* par numéro ; les recoupements douteux sont traités au §3).

---

## 2 · Les 21 cabinets ajoutés

| Ligne ONOC | Cabinet | Numéro publié | Titulaire au tableau |
|---|---|---|---|
| 87 | **Alpha Optic** | 699 57 34 57 | AKINHOLA Abdou Aziz Adewale |
| 88 | **Saoudia Optique** | 696 04 04 13 | Ali MOUSTAPHA Abdou |
| 89 | **Centrale d'Optique Panafricaine Sarl** | 695 29 79 04 | ATONGO Marie Albert |
| 90 | **ISEE** | 656 97 80 43 | AZEUFACK Raissa |
| 105 | **Free Optic** | 679 11 37 60 | FEUKOUO Rigobert |
| 106 | **La Fierté de l'Optique** | 695 17 90 57 | Fierté Clarisse EKEN EKOLLO |
| 108 | **Emeraude Optique Sarl** | 699 90 99 60 | FOGNEMAFOPOKAM Sebastine |
| 111 | **Optimat Vision Sarl** | 699 86 53 46 | KAMDEM KOUAM Serge Versel |
| 114 | **Light Optique** | 677 64 87 90 | KEMAJOU épse NUSHA Singer |
| 124 | **Ets Espace Médical** | 655 04 95 29 | MBIAMI MENVENGUE |
| 125 | **S.O.S Vision** | 699 86 04 63 | MEILO NGASSA Line |
| 134 | **ASS pour RRPHDD** | 675 39 90 23 | NDE Bruno |
| 135 | **Bellevue Optique** | 694 89 26 96 | NDOUNG Erick Georges |
| 138 | **La Fibre Optique** | 694 42 26 40 | NGUEPI Stéphane |
| 139 | **La Lunetterie Médicale El Shadai** | 696 89 64 11 | NGUEGANG DJOMO Richeleau |
| 141 | **Pagrot Optique** | 699 90 46 91 | NGUIFFO épse KAMGA Lyse Esther |
| 155 | **Capelli Optique Médicale** | 675 26 89 81 | TCHOUMBA Annie Nadège |
| 156 | **Optique Pro** | 690 03 48 18 | TEKENG NTEMTSA Sintiche Laury |
| 157 | **World Vision** | 656 03 21 72 | TONGOUANG Serge Bruno |
| 158 | **Maranatha Optics** | 658 16 31 90 | WONDJE Madeleine Florence |
| 86 | **Prism Optique** *(fixe seul)* | 233 42 62 73 | AHMER SHEIKH Ahmer |

Les 20 premiers sont entrés avec `wa_verified="unknown"`, `stage="prospecting"`, `contacted="No"`.
**Aucun n'est dans un lot d'envoi, aucun message n'est écrit pour eux** : la **porte A** (§8b du
`RESEARCH-STANDARD` — le numéro joint sur WhatsApp, profil vu) reste entièrement à passer, et c'est
King seul qui peut la passer.

**Prism Optique est entré sans numéro WhatsApp** (`wa_number=""`, `wa_number_note` rempli) : l'Ordre
ne publie qu'un **fixe** pour ce cabinet. Le mettre dans `wa_number` l'aurait envoyé dans la file
d'envoi, et l'erreur n'aurait été vue qu'au moment de coller le message. Il reste au CRM comme trace
de couverture : un cabinet de l'annuaire qu'on ne peut pas joindre n'est pas un cabinet qu'on ignore.

---

## 3 · Trois pièges rencontrés, et ce qu'on en fait

**① Star Optic publie le numéro de Médina Optic.** Ligne 154, `699 93 93 34` — exactement le numéro
de Médina Optic (ligne 91), déjà au CRM, déjà contacté le 24/09, déjà parké. Le croisement par numéro
l'a écarté automatiquement : **une ligne, pas deux**, et surtout pas un second message à un cabinet
déjà touché sous un autre nom. C'est déjà écrit au CRM sur la ligne de Médina Optic.

**② « Centrale Optique » et « Centrale d'Optique Panafricaine » sont deux cabinets différents.**
La première (ligne 145, ZOBO Jean, 693 96 89 56) est **disqualifiée** depuis le 12/10 : aucun de ses
deux numéros n'est sur WhatsApp. La seconde (ligne 89, ATONGO Marie Albert, 695 29 79 04) est
**neuve**. Deux noms qui se ressemblent, deux titulaires, deux numéros : le second n'hérite pas du
verdict du premier, et le message ne doit jamais citer « Centrale Optique » sans le mot
« Panafricaine ».

**③ Le numéro du tableau n'est pas le numéro de la fiche.** Chez Optix, l'Ordre publie
`681 36 92 33`, la page Facebook `697 72 32 65`, et c'est le second qui a reçu le message. Pour ces
21 cabinets, on ne connaît **que** le numéro de l'Ordre. La porte A tranche.

---

## 4 · Le trou trouvé en chemin — et il était sérieux

En lançant le rebuild, `leads/CRM.csv` est passé de **163 à 162 lignes** et quatre leads sont revenus
de `parked`/`qualifying` à `prospecting`. La cause n'est pas le scout :

> **`leads/build/crm.py` en tête de branche était la version du 10/10, pas celle du 13/10.**
> Le travail du 12/10 (ruling vague : `excluded_no_wa` sur **Faby** et **Centrale Optique**, refus de
> **Jired** le 12/10 11:47, envoi **Planète** du 12/10, tags **Maff** / **Horizon** / **Kamaïs**,
> RDV **Univers Optique** du 16/10) et la relance **Planète** du 13/10 existaient dans les commits
> `9a49aa1` et `71851af` — mais le fichier avait été **remplacé par une version antérieure** dans
> l'arbre, exactement le scénario contre lequel `guard.py` a été écrit le 22/09.
> Le CSV, lui, portait bien l'état du 13/10 : le dépôt avait donc un **générateur en retard sur sa
> propre donnée**, et le premier rebuild allait effacer six semaines de rulings.

**Réparé** : le générateur a été repris depuis `71851af` (la version du 13/10), le bloc scout
ré-ajouté par-dessus, l'empreinte des générateurs re-scellée (`guard.py lock`, puis `check` → rc 0).
**Contrôle après rebuild** : 184 lignes = **163 identiques champ par champ** (les 163 lignes du CSV
d'avant le rebuild, comparées colonne par colonne : 0 différence) + **21 nouvelles**. Rien de perdu,
rien de réécrit.

**La leçon, écrite ici pour ne pas la repayer** : `git log -- leads/build/crm.py` s'arrête au **10/10**
alors que le fichier a été modifié le 12 et le 13. **La date du dernier commit d'un fichier n'est pas
la date de son contenu** — c'est l'empreinte (`guard.py check`) qui dit la vérité, et elle n'a de sens
que si elle est re-scellée après un changement voulu. Le rebuild a désormais un contrôle qui le
précède : `python3 leads/build/guard.py check` (rc 1 si un générateur a bougé sans lock).

---

## 5 · Ce que ce scout ne fait pas

| Ce qui reste | Pourquoi ce n'est pas fait ici | Qui |
|---|---|---|
| **Porte A** sur les 20 numéros (profil WhatsApp vu) | il faut un téléphone qui ouvre WhatsApp et un jugement : le numéro de l'Ordre peut être un fixe, une ligne d'agence ou un numéro partagé | **King**, 20 ouvertures, ~4 min |
| Vérifier s'ils ont déjà un site ou une page Facebook | demande une recherche par cabinet (20 × 2) ; inutile tant que la porte A n'a pas dit qui est joignable | après la porte A |
| Écrire les messages | un message par cabinet, avec son quartier et sa fuite réelle : **pas avant** la porte A et le contrôle du site (règle « pas de site par prospect avant réponse ») | après la porte A |
| Choisir le segment (cold vs re-engage) | tous les 21 sont **cold** : aucun n'a jamais été contacté | — |

**Le prochain geste, un seul** : les cinq messages froids du **lot du 26/10** partent d'abord (ils sont
écrits, passés à la porte, et Optix part avec sa capture). La porte A des 20 numéros se passe
**ensuite**, en une session de 4 minutes, et elle alimente la vague suivante.
