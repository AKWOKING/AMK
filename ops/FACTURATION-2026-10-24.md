# L'outil de facturation AMK — ce qu'il est, et la règle qui le relie aux prix

```
Outil   https://amk-factures-pwa.vercel.app/     (application web installable, PWA)
Créé    par King, 24/10/2026
Rôle    suivre ce qui est facturé, ce qui est encaissé, et ce qui reste dû
Règle   aucune ligne de facture ne se tape de mémoire : tout montant sort de la grille publique
```

## 1 · Ce que l'écran montre (relevé le 24/10, 07:1x)

| Élément | Valeur lue |
|---|---|
| En-tête | « À encaisser **75 000 FCFA** » |
| Compteur | « 1 facture ouverte · Déjà encaissé **75 000 FCFA** » |
| Filtres | Toutes · En cours · Payées |
| Facture ouverte | **AMK-2026-001** — « Acompte reçu 150 000 FCFA » — DM OPTIQUE SARL · 23 octobre 2026 — « Reste 75 000 FCFA » |

Deux choses sont donc déjà vraies dans l'outil, et elles comptent :

1. **La numérotation est annuelle et continue** (`AMK-2026-001`) — c'est ce qu'un client au régime réel
   demandera un jour, et c'est déjà en place.
2. **L'acompte de 50 % est matérialisé** : 150 000 facturés, 75 000 reçus, 75 000 restants. C'est
   exactement la clause des contrats (« 50 % à la commande, 50 % à la livraison »), et l'écran le
   montre sans qu'on ait à l'expliquer.

## 2 · La règle qui manquait, et qui relie l'outil aux prix

Le dépôt portait **quatre prix mensuels différents** pour la même chose (10 000 / 12 000 / 30 000 /
35 000 — voir `sales/PRIX-ET-RECURRENCE-2026-09-24.md` §2). Un outil de facturation branché sur quatre
prix ne facture pas : il propage la confusion.

Depuis le 24/10, la grille est unique (`knowledge/PRIX-2026-10-24.md`, séance
`ROAST-2026-10-24-PRIX-v2.md`) :

| Ligne de facture | Montant | Ce qui doit être écrit sur la facture |
|---|---|---|
| Présence | 150 000 | jusqu'à 3 pages, fiche Google créée, domaine + hébergement 1ʳᵉ année, formation |
| Standard | 250 000 | jusqu'à 6 pages, fiche Google optimisée, 1 mois de support |
| Catalogue | 450 000 + | jusqu'à 30 références, commandes WhatsApp |
| Suivi (mensuel) | 25 000 | sauvegardes, mises à jour, 2 posts Google, rapport, 2 h de modifications |
| Croissance (mensuel) | 75 000 | Suivi + 8 pièces sociales, 4 posts Google, pub gérée, revue trimestrielle |
| Montée Présence → Standard | 120 000 | reconstruction, pas une remise |

**Trois contrôles avant d'envoyer une facture** (30 secondes, et ils évitent la mauvaise conversation) :

- [ ] le montant existe **dans cette table**, à la ligne près ;
- [ ] le périmètre écrit sur la facture est **celui de la ligne**, pas un mélange de deux paliers ;
- [ ] l'acompte est **50 %** et la facture suivante ne réclame que le reste (l'outil le calcule déjà).

## 3 · Ce qui reste à décider par King

1. **Le canal d'encaissement** à afficher par défaut : MTN 677 78 96 31 ou Orange 692 89 07 47 — l'outil
   n'affiche aujourd'hui que les montants, pas les coordonnées de paiement.
2. **La mention fiscale** : ni « conforme DGI » ni « facture normalisée » ne doivent apparaître tant que
   les spécifications ne sont pas publiées ; une phrase honnête est à écrire une fois (proforma + NIU +
   RIB, comme pour DM OPTIQUE) et à réutiliser.
3. **Le sort de DM OPTIQUE** : il paie 30 000/mois pour un périmètre « Croissance » (75 000). On ne
   réécrit pas un contrat en cours ; au renouvellement, deux issues écrites — 75 000, ou périmètre
   réduit à ce que 30 000 achètent.

## 4 · Ce que l'outil ne fera jamais à notre place

Il ne dit pas si le prix est juste, il ne dit pas si le travail est livré, et il ne remplace pas la
phrase qui compte au client : **« voilà ce que vous avez reçu ce mois-ci »**. C'est le rapport d'une
page (`knowledge/MAINTENANCE-CLIENTS-2026-10-22.md` §4) qui justifie le prélèvement, pas la facture.
Facturer le 1er, envoyer le rapport le 2 : l'ordre est déjà écrit, il ne reste qu'à le tenir.
