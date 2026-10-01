# CINQ SENS — ce qu'il reste à nous envoyer

**Document de travail. Il part dans la conversation WhatsApp — il n'est pas sur la page.**
Depuis la v1 de l'aperçu (24/09, soir), la page parle **au patient** : services, arrivages, deux
cabinets, six questions. Tout ce qui suit manque pour qu'elle soit **entièrement vraie**.

| # | Ce qu'on attend du cabinet | Ce que ça change sur la page | État |
|---|---|---|---|
| 1 | **Votre nom, ou celui du responsable** (et la fonction) | La page ne nomme personne aujourd'hui : on n'a trouvé aucun nom publié. Un vrai nom fait tomber une méfiance | à demander |
| 2 | **Les horaires définitifs** (jours, heures, jours fériés) — et par cabinet s'ils diffèrent | Écrits « **horaires annoncés** » (deux annuaires concordent), et volontairement **absents du schéma** tant que vous ne les confirmez pas | à confirmer |
| 3 | **La seconde ligne 655 163 365 est-elle toujours active ?** Et le **694 408 495** (vu sur un seul annuaire) ? | Le 655 est en bouton « appeler » ; le 694 n'apparaît **nulle part** tant qu'il n'est pas confirmé | à confirmer |
| 4 | **Six à dix photos de vos arrivages** — montures homme, femme, solaires, et la vitrine du magasin | Elles remplacent les **trois illustrations** générées. C'est la vitrine de la page : c'est ce que le patient vient voir | à demander |
| 5 | **Deux ou trois photos de chaque cabinet** (extérieur avec le repère visible, intérieur) | Le patient reconnaît le lieu avant d'y aller — et les repères écrits (Kokotier, Flore service, Michelin) deviennent vérifiables à l'œil | à demander |
| 6 | **Les marques de montures que vous vendez** (et si vous voulez qu'elles soient nommées) | Aujourd'hui la page n'écrit **aucune marque** — elle dit « demandez, la réponse arrive sur WhatsApp ». Avec votre liste, on écrit « nous portons… » | à confirmer |
| 7 | **Les moyens de paiement** (espèces, MTN MoMo, Orange Money) | Évite qu'un patient arrive sans pouvoir payer | à confirmer |
| 8 | **Les assurances / mutuelles** prises en charge | Décide le patient assuré, et vous distingue de la concurrence | à confirmer |
| 9 | **Les prix** : voulez-vous afficher quelques repères (« à partir de… ») ? | Aujourd'hui **aucun prix** n'est écrit : la page répond à la question en renvoyant au WhatsApp. Vous restez libres — mais dites-le-nous | à décider |
| 10 | **La livraison à domicile** : quels quartiers, quel délai, quel frais ? | Aujourd'hui la page la mentionne sans promettre ni délai ni frais | à préciser |
| 11 | **Les prothèses oculaires** : qui les réalise, et faut-il un rendez-vous ? | La page en parle comme d'un métier du cabinet. Une phrase de précision ferait tomber beaucoup de questions | à préciser |
| 12 | **Vos horaires du dimanche** et les jours de fermeture exceptionnelle | Une question fréquente de patient | à confirmer |

## Ce qu'on fait dès qu'on reçoit

1. `python3 demos/build_cinqsens.py --url https://<votre adresse>` (les faits entrent dans la page) ;
2. **un seul redéploiement** du dossier chez vous ;
3. on vous renvoie la page, et on vous demande de la relire **sur votre téléphone**, pas sur un
   ordinateur.

## Ce qu'on ne fera jamais, même si on nous le demande

- Écrire une adresse, un horaire, un prix, une marque, une assurance ou un avis **non confirmés** ;
- Reprendre un avis client trouvé ailleurs, ou en fabriquer un ;
- Promettre un classement sur Google, un délai ou un nombre de patients ;
- Publier une photo de personne (patient, client, personnel) sans son accord écrit ;
- Mettre la page sur un domaine **à nous** : le jour venu, le domaine est au nom du cabinet.
