# La routine de maintenance clients — quotidien, hebdomadaire, mensuel

```
Date     22/10/2026
Pour qui tout client en retainer (aujourd'hui DM Optique ; **5 clients maximum, dont 2 Croissance** — ruling King 23/10)
Principe ce qui n'est pas dans cette liste ne se fait pas ; ce qui dépasse le budget temps se facture.
```

---

## 0 · Les repères du secteur (relevés, pas inventés)

| Constat | Chiffre | Source |
|---|---|---|
| Les agences rapportent **au mois** | 46 à 58 % des agences ; 14 % par semaine | Databox (241 agences), AgencyAnalytics (494 pros, 2026) |
| Les clients attendent une réponse **sous 24 h** | **73 %** ; 42 % attendent moins de 60 min | Sprout Social Index 2025-2026 |
| Un standard réaliste de réponse | **60 min** grand public · **4 h** B2B · **24 h maximum** | plusieurs benchmarks 2026 |
| Le rapport doit coûter **4 à 6 % du temps facturé** | au-delà, on sur-documente | benchmarks d'agences |
| La revue trimestrielle augmente la rétention de **22 à 31 points** | chez les agences qui la tiennent | Promethean Research |

**Traduction pour nous** : un rapport mensuel d'**une page**, pas un PDF de douze. Et une réponse le jour même, parce que c'est le seul KPI que le client voit de ses yeux.

---

## 1 · Le budget temps d'un retainer à 75 000 FCFA

| Bloc | Temps / mois | Ce que ça couvre |
|---|---|---|
| Production | **8 h** | 4 vidéos + 4 posts + publication |
| Entretien & veille | **2 h** | cette routine |
| Mesure & rapport | **1 h** | chiffres + une page |
| **Total** | **≈ 11 h** | soit ≈ 6 800 FCFA/h |

Si l'entretien dépasse 2 h, ce n'est plus de l'entretien : c'est un projet. On le dit, on le chiffre, on ne l'absorbe pas.

---

## 2 · Chaque jour — 10 minutes, pas plus

| # | Quoi | Pourquoi |
|---|---|---|
| 1 | **Répondre aux commentaires et messages** (WhatsApp, Facebook, TikTok) | 42 % des personnes qui **contactent une marque sur les réseaux sociaux** attendent une réponse dans l'heure (Edison Research / *The Social Habit*, 2012, via Convince & Convert ; base : 690 personnes ayant contacté une marque sur 3 000+ interrogés). Étude **ancienne et américaine** : ordre de grandeur, pas une mesure camerounaise. La règle tient sans le chiffre : une question sans réponse est un client parti |
| 2 | **Signaler, pas répondre à sa place** : prix, disponibilité, conseil médical → on renvoie au cabinet | on n'engage pas le client sur ce qu'on ne sait pas |
| 3 | **Vérifier que le lien du jour fonctionne** (page, bouton WhatsApp, formulaire) | un bouton mort coûte plus qu'une publication manquée |
| 4 | **Noter toute question nouvelle** dans un fichier | trois fois la même question = un contenu à faire |

**Ce qu'on ne fait pas chaque jour** : regarder les vues, changer le calendrier, retoucher une vidéo. C'est du bruit, et ça donne l'illusion de travailler.

---

## 3 · Chaque semaine — 30 à 45 minutes, un jour fixe

| # | Quoi | Détail |
|---|---|---|
| 1 | **Publier** aux créneaux décidés (dimanche 19 h, lundi 13 h) | la régularité avant la perfection |
| 2 | **Contrôler les pièces en attente de validation** | relance unique, jamais deux fois la même question |
| 3 | **Relever les 4 chiffres** : vues à 3 s · rétention à 10 s · conversations WhatsApp ouvertes · contacts ayant enregistré le numéro | 5 minutes, pas une réunion |
| 4 | **Vérifier le site** : page en ligne, lien WhatsApp, fiche Google, vitesse | une panne silencieuse est la pire |
| 5 | **Préparer la semaine suivante** : 2 pièces scriptées, 1 tournée d'avance | c'est ce qui empêche le mois de dérailler |

**Le test de la semaine** : si on n'a pas publié, les quatre chiffres sont vides. Le reste est de la préparation.

---

## 4 · Chaque mois — 1 h 30, dans la première semaine

**L'ordre du mois, en trois dates (ruling King 23/10) :** facture le **1er** · récap d'une page et
rapport le **2** · la conversation qui va avec dans la foulée. Le récap est un **PDF d'une page**
(`tools/ops/make_recap.py --data …`, le même moteur pour tous les clients), régénéré depuis un fichier de chiffres
(`clients/dm-optic/launch/recap-2026-10.json` à copier) : mêmes blocs chaque mois, seuls les chiffres
et les dates changent. Un client qui reçoit la même page, avec de nouveaux chiffres, comprend en
trois secondes qu'il paie pour quelque chose qui tourne.

Le rapport tient sur **une page**, dans cet ordre :

| Section | Contenu | Longueur |
|---|---|---|
| **Ce qui a été publié** | nombre, dates, liens | 3 lignes |
| **Ce que ça a donné** | les 4 chiffres, comparés au mois précédent | 1 tableau |
| **Ce qui a marché / ce qui n'a pas marché** | une hypothèse par ligne, pas une excuse | 4 lignes |
| **Ce qui attend le client** | photos, validations, informations | liste courte |
| **Ce qu'on fait le mois prochain** | 3 priorités, pas 10 | 3 lignes |

**Trois règles de rapport :**

- **jamais plus de 7 chiffres** — au-delà, personne ne retient ;
- **toujours un point faible assumé** — un rapport sans problème n'est pas cru ;
- **toujours une demande précise au client** — un rapport qui ne demande rien ne fait pas avancer le dossier.

Et le réflexe qui sauve : **facturer le retainer le 1er, envoyer le rapport le 2**. L'argent d'abord, la preuve ensuite — l'inverse donne l'impression qu'on quémande.

---

## 5 · Chaque trimestre — 1 h, en visio ou en boutique

| # | Quoi |
|---|---|
| 1 | Les chiffres du trimestre, pas du mois |
| 2 | Ce qu'on garde, ce qu'on arrête, ce qu'on essaie |
| 3 | Le budget du trimestre suivant (publicité incluse ou non) |
| 4 | La question qui compte : **« qu'est-ce qui vous a coûté des clients ce trimestre ? »** |

C'est le rendez-vous qu'on saute toujours. C'est aussi celui qui fait rester les clients un an de plus.

---

## 6 · Le calendrier réel, sur une année

| Quand | Quoi | Pourquoi |
|---|---|---|
| **Janvier** | rapport annuel, réajustement du forfait, reçu des pièces | nouvelle année = nouvelle numérotation |
| **Chaque mois** | rapport + facture | voir §4 |
| **Chaque trimestre** | revue | voir §5 |
| **Juin** | sauvegarde complète des actifs clients (photos, vidéos sources, accès) | un disque perdu ne doit pas coûter un client |
| **Décembre** | bilan + proposition pour l'année suivante | on ne renégocie pas en janvier dans l'urgence |

---

## 7 · La panne : ce qu'on fait dans les 2 heures

| Situation | Réflexe |
|---|---|
| Le site ne répond plus | vérifier l'hébergement, restaurer la dernière version connue, prévenir le client **avant** qu'il ne le découvre |
| Le lien WhatsApp est cassé | corriger sur le site, les pages, la fiche Google, le pied de page |
| Un contenu publié contient une erreur | **corriger publiquement** dans l'heure, pas en douce : supprimer sans expliquer se voit |
| Un accès client est perdu | ne jamais détenir le seul jeu d'accès — c'est la règle de propriété du dossier |
| Le client publie lui-même une chose fausse | le dire en privé, proposer une correction, ne jamais corriger à sa place sans accord |

---

## 8 · Ce que cette routine vaut, et ce qu'elle coûte

Pour un client à **75 000 FCFA/mois**, 11 h de travail : la routine n'est pas un supplément de service, c'est **ce qui justifie le prix**. Un client qui ne reçoit qu'un fichier par mois finit par se demander pourquoi il paie.

Pour **cinq clients** (3 Suivi à 4 h + 2 Croissance à 12 h) : **36 h/mois** de maintenance et de
production récurrente — soit un tiers du temps utile. C'est le plafond retenu par King le 23/10 :
au-delà, il faut embaucher ou automatiser, et **un troisième Croissance ne rentre pas** dans le mois.
(L'ancienne note disait trois clients à 33 h : elle datait du prix de 25 000, où trois Suivi ne
couvraient même pas les charges fixes de 85 000.)

---

## 9 · La première semaine, concrètement

- [ ] écrire les deux créneaux dans un calendrier partagé
- [ ] créer le fichier « questions récurrentes » de chaque client
- [ ] mettre en place les 4 chiffres dans un tableau unique
- [ ] préparer le modèle de rapport d'une page
- [ ] fixer la date du rapport mensuel (2 du mois) et de la facture (1er)
- [ ] noter dans le contrat : délai de validation 5 jours ouvrés, propriété des comptes au client, acompte avant travaux
