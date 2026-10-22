# Bilan de production — ce qui est publié, ce qui est produit, ce que ça apprend

```
Statut   constat interne, 22/10/2026. DM Optique sert aussi de banc d'essai :
         ce document existe pour chiffrer le prochain client, pas pour se féliciter.
Règle    on ne compte comme livré que ce qui est PUBLIÉ et visible par un client du cabinet.
```

---

## 1 · Le tableau honnête

| | Produit | Publié | Visible par le public |
|---|---|---|---|
| **Site** (48 pages) | ✅ | ✅ | ✅ dmoptiquesarl.com |
| **Fiche Google** | ✅ | ✅ | ✅ créée le 20/10, 4 posts programmés |
| **Page Facebook** | ✅ | ✅ | ✅ 1 post + 1 programmé |
| **TikTok** | ✅ compte | ⬜ | ⬜ **aucune vidéo publiée** |
| **Vidéos** | **5** (4,6 → 14 Mo) | **0** | ⬜ |
| **Carrousels du plan mois 1** | 0 | 0 | ⬜ |
| **Légendes / posts écrits** | 4 | 1 | ✅ partiellement |
| **Recherche + stratégie** | ✅ 4 documents | — | interne |

**Le chiffre qui compte : 5 vidéos produites, 0 publiée.** Tout le reste en découle.

---

## 2 · Pourquoi ce n'est pas un échec, et pourquoi il faut le dire quand même

Le plan promettait **2 publications par semaine**, soit 8 pièces par mois. On en est à 1 post Facebook. Le compte TikTok est ouvert depuis le 21/10 et n'a rien publié.

Trois causes, dans l'ordre de poids :

1. **L'ordre des opérations.** On a produit avant d'avoir un canal. Quatre vidéos ont été montées alors que la page TikTok n'existait pas encore — et qu'aucun mécanisme de validation client n'était en place.
2. **La validation du client.** Rien ne se publie sous son nom sans son accord : c'est une règle juste. Mais elle n'a pas de délai. Demain, une vidéo peut attendre une semaine pour un « c'est bon ».
3. **Les actifs manquants.** Pas de photos des quatre étapes de l'examen, pas de diplômes, pas de photos des montures. Chaque pièce a demandé de contourner un manque — c'est ce qui a produit les visuels générés, donc un travail supplémentaire, donc du temps.

**La leçon n'est pas « produire moins ».** C'est **produire après avoir sécurisé le canal et les actifs**, et **publier au fur et à mesure** au lieu de constituer un stock.

---

## 3 · Ce que ça a coûté, en nature

Pas d'heures inventées ici : ce qui suit est vérifiable dans le dépôt.

| Poste | Réalité mesurée |
|---|---|
| **Rendus vidéo** | 5 fichiers, 4,6 à 14 Mo. Le rendu machine est rapide (~2 min pour 31 s) |
| **Itérations de montage sur la dernière vidéo** | 5 versions avant validation du mouvement (cadrage, lisibilité, carte de fin figée) |
| **Visuels générés** | 5 images générées, dont **1 refaite** (un visage de patient était visible) — 1,5 s de calcul par image de simulation |
| **Recherche** | 4 documents, 2 vidéos de hooks, 1 masterclass, 1 recherche marché, 5 captures client décodées |
| **Corrections de conformité** | 1 audit automatisé (4 règles), 3 passages de correction sur les prix et les cardinaux |
| **Ce qui a bloqué, et qui ne dépendait pas de nous** | NIU du client (promis le 02/10), photos (jamais reçues), validation vidéo (en attente) |

**Le vrai coût n'est pas la production.** C'est **la boucle de décision** : chercher ce qui est autorisé, produire, faire valider, corriger. La machine tourne vite ; ce sont les allers-retours qui prennent le mois.

---

## 4 · Ce qu'on garde, et qui n'est pas facturé deux fois

Le prochain client ne repart pas de zéro. Ces actifs sont réutilisables :

| Actif | Réutilisable ? | Valeur |
|---|---|---|
| `tools/record/make_dmoptic_etapes.py` | oui, en changeant les plans | moteur vidéo avec chronologie de texte découplée |
| `tools/qa/audit_video_motion.py` | oui, tel quel | portique bloquant : plus de diaporama livré |
| `tools/qa/audit_claims.py` | oui, en réécrivant les règles du client | portique des affirmations |
| Méthode de recherche + banque de hooks | oui | le travail déjà payé une fois |
| Simulation de vision sur photos réelles | oui | format viral sans visage ni image générée |
| Le dossier DM Optique lui-même | **non** | chaque client a ses verrous |

---

## 5 · Ce qu'il faut changer pour cadrer et facturer le prochain client

### 5.1 Auditer les actifs **avant** de chiffrer

Le devis doit être précédé d'une liste courte, remplie avec le client :

> photos du lieu · photos des produits · photos du geste · autorisation d'image des personnes ·
> identité visuelle · accès aux comptes · qui valide, et sous quel délai.

Un client sans photos coûte **une à deux fois plus** qu'un client qui en a. Ce n'est pas une intuition : c'est ce qui s'est passé ici.

### 5.2 Facturer le diagnostic, séparément

La recherche (hooks, marché, verrous) a représenté l'essentiel du travail utile de ce mois. Elle doit être une **ligne de devis**, pas un cadeau qui précède la production. Sinon le client croit qu'il paie des vidéos, et compare au prix d'un monteur.

### 5.3 Écrire un délai de validation dans le contrat

> Chaque pièce est soumise ; sans réponse sous **5 jours ouvrés**, elle est réputée refusée et passe à la semaine suivante. Le calendrier glisse, il ne se compense pas.

Sans cette clause, tout retard client devient notre problème de trésorerie.

### 5.4 Vendre une **série**, pas des pièces

Cinq vidéos produites et zéro publiée, c'est le symptôme d'une vente à la pièce. Une série — même format, même ouverture, même demande, un sujet différent par épisode — se produit plus vite, se valide plus vite, et se vend comme un rendez-vous plutôt que comme un fichier.

### 5.5 Séparer installation et abonnement, dans le temps

L'installation (site, fiches, comptes) se livre et se paie **fermé**. Le retainer commence **après**, sur un mois plein. Ici, les deux se sont chevauchés, et c'est ce qui rend la conversation sur l'argent floue.

### 5.6 Le prix, tel qu'il devrait être posé la prochaine fois

| Ligne | Ce qu'elle couvre | Pourquoi elle existe |
|---|---|---|
| **Diagnostic** | marché, verrous, angle, banque de hooks | se paie une fois, sert tout le projet |
| **Installation** | site, fiche, comptes, identité | livrable fini, vérifiable |
| **Série** | production + publication, cadencée | ce qui produit réellement des conversations |
| **Option pub** | budget média, **hors** forfait | sinon la marge fond dès que la pub marche |

Le forfait doit dire **ce qu'il ne comprend pas**. Un forfait qui laisse croire que la pub est incluse se retourne contre nous au premier mois.

---

## 6 · Ce qu'il faut dire au client, et quand

Le rapport du mois 1 ne peut pas être un catalogue de ce qu'on a produit. Il doit dire :

1. **ce qui est en ligne** (vérifiable depuis son téléphone) ;
2. **ce qui est prêt et attend sa validation** (les vidéos) ;
3. **ce qui bloque de son côté** (photos, NIU, réponse vidéo) ;
4. **ce que ça a donné** (22 vues, 2 interactions, 0 abonné — un point de départ, pas un résultat) ;
5. **ce qu'on change** : une publication par semaine, publiée, plutôt que deux dont une reste dans un tiroir.

Le point 5 est le plus important, et c'est celui qu'on serait tenté d'éviter. C'est pourtant le seul qui prouve qu'on mesure — et c'est ce qui justifie le retainer.
