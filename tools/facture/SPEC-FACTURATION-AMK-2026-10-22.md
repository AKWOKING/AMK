# Spécification — système de facturation AMK (usage interne)

```
Statut   spécification, 22/10/2026. Rien n'est codé à ce stade.
But      produire devis, proforma, factures, reçus et avoirs pour AMK — pas vendre un logiciel.
Décision voir ops/ROADMAP-AMK-POST-DM-OPTIC-2026-10-22.md §1 : outil interne, pas SaaS.
```

---

## 0 · Les deux décisions prises avant d'écrire une ligne

**1. Ce n'est pas un produit.** Le marché camerounais de la facturation est servi à **0 à 25 000 FCFA/mois** (Nkap Control, zBilling, GesCab, Omamori, Duka360), avec Mobile Money déjà intégré. On ne concurrence pas ça. On outille **nos propres factures**.

**2. On n'écrit jamais « conforme DGI ».** La loi de finances 2026 impose la facturation électronique via des plateformes agréées dont la liste n'est pas publiée. Notre outil produit des **documents justes** ; il ne prétend pas être un dispositif fiscal agréé.

---

## 1 · Ce qu'un document doit porter (Cameroun)

| Mention | Règle | Où elle vient |
|---|---|---|
| **Raison sociale + forme juridique** | « AMK … » au nom exact du RIB | à figer avant tout |
| **NIU** | **la mention la plus contrôlée** — sans NIU, l'entreprise n'existe pas fiscalement | ✅ **reçu le 22/10 : `P030218642934H`** |
| **RCCM** | numéro d'immatriculation | ⛔ **toujours manquant — bloquant** |
| **Adresse complète** | siège, téléphone, e-mail | partiel |
| **Régime fiscal** | IGS / réel simplifié / réel normal — décide de la TVA | ⛔ à trancher avant toute facture |
| **Identité du client** | nom ou raison sociale, adresse | à saisir |
| **NIU du client** | **obligatoire en B2B** | à demander au client |
| **Numéro séquentiel continu** | par type et par année, sans trou | généré |
| **Date d'émission** + date de prestation | | généré |
| **Désignation, quantité, prix unitaire HT** | | saisi |
| **TVA 19,25 %** ou **« TVA non applicable »** | si l'émetteur n'est pas assujetti, la mention est obligatoire | selon régime |
| **Total HT · TVA · TTC** | | calculé |
| **Échéance et conditions de règlement** | | paramétré |
| **Mention du type** | DEVIS · PROFORMA · **FACTURE** · REÇU · AVOIR | jamais mélangés |

**Trois pièges techniques à ne pas rater :**

1. **Le franc CFA n'a pas de décimales.** On arrondit à l'unité, jamais de « 12 500,00 ». Un centime affiché sur une facture FCFA est le signe d'un outil mal réglé.
2. **Une proforma n'est pas une facture.** Elle ne crée aucune créance et ne porte pas de numéro de la série des factures. Deux séries séparées : `PRO-2026-001`, `FAC-2026-001`.
3. **Un avoir référence toujours la facture d'origine**, et vient en déduction — jamais une facture négative.

**Conservation** : les pièces se gardent selon l'obligation légale (10 ans en pratique OHADA) — donc **export annuel obligatoire**, pas seulement une base de données.

---

## 2 · Le modèle de données (5 tables, pas plus)

```
clients        id · nom · niu · adresse · email · tel · notes
documents      id · type(devis|proforma|facture|recu|avoir) · serie · numero · date
               client_id · objet · total_ht · tva_taux · total_ttc · statut
               (brouillon|envoyé|payé|partiel|retard|annulé) · echeance · parent_id
lignes         document_id · designation · quantite · prix_unitaire
paiements      facture_id · date · montant · moyen(especes|momo|orange|virement) · reference
reglages       raison_sociale · niu · rccm · adresse · rib · regime · tva_taux · logo
```

**Trois règles de gestion qui viennent du terrain :**

- **Paiement partiel autorisé** (acompte de 50 %, solde à la livraison). C'est le cas DM Optique : 75 000 + 75 000.
- **Une facture échue n'est jamais « annulée » pour cacher un retard** : elle passe en `retard`, et l'avoir ne sert qu'à une vraie correction.
- **Numéro consommé = numéro gardé.** Si un document est supprimé, il est marqué `annulé` et le numéro ne se réutilise pas.

---

## 3 · L'architecture — la plus petite qui tient

```
Navigateur (HTML + JS, aucune dépendance)
      │  formulaire, aperçu imprimable
      ▼
Cloudflare Worker  ←  déjà utilisé pour dmoptiquesarl
      │  API JSON, auth par cookie signé
      ▼
D1 (SQLite)  ── export JSON quotidien vers R2  ──  téléchargement local
```

| Choix | Raison |
|---|---|
| **Un seul utilisateur** (toi), pas de multi-tenant | on ne code pas des rôles dont personne n'a besoin |
| **PDF par impression navigateur** (`@media print`) | zéro bibliothèque PDF, zéro serveur de rendu, un rendu net sur tous les appareils |
| **D1 + export R2 quotidien** | la base ne doit jamais être le seul endroit où vivent les factures |
| **Pas de Mobile Money intégré en v1** | les paiements sont **saisis** ; l'intégration viendra si un client l'exige |
| **Hors ligne toléré** | si le Worker tombe, l'aperçu imprimable doit encore fonctionner depuis le brouillon local |

**Authentification** : mot de passe long + cookie signé, ou Cloudflare Access. Pas de compte utilisateur, pas de « mot de passe oublié » — un seul utilisateur, une seule clé.

---

## 4 · Les écrans, dans l'ordre où ils servent

1. **Nouveau document** — client, objet, lignes, TVA, échéance, aperçu immédiat.
2. **Liste** — filtre par statut, total en attente, total en retard. C'est l'écran qu'on ouvre tous les matins.
3. **Fiche client** — historique, NIU, ce qui a été facturé et payé.
4. **Réglages** — raison sociale, NIU, RCCM, RIB, régime, taux de TVA.
5. **Export** — CSV des factures de l'année, JSON de sauvegarde.

**Ce qu'on ne met pas en v1** : stock, catalogue produits, paie, comptabilité, relances automatiques par e-mail, portail client, application mobile. Chacun de ces ajouts double le projet et ne sert à rien tant qu'il n'y a pas trois clients.

---

## 5 · Le plan de travail

| Étape | Contenu | Durée |
|---|---|---|
| **0 · Préalable** | ~~NIU~~ ✅ reçu · **RCCM, RIB et régime fiscal restent bloquants** | **bloquant** |
| 1 | Réglages + clients + calculs + aperçu imprimable | 1 jour |
| 2 | Numérotation, statuts, paiements partiels | 1 jour |
| 3 | Avoir, export, sauvegarde | 0,5 jour |
| 4 | Test sur un vrai cas : facture du solde DM Optique | 0,5 jour |

**Total : 3 jours.** Au-delà, c'est qu'on a ajouté du périmètre — pas qu'on a pris du retard.

---

## 6 · Les tests qui comptent (à écrire avant le code)

| # | Cas | Résultat attendu |
|---|---|---|
| 1 | Facture avec TVA | 100 000 HT → **19 250 de TVA → 119 250 TTC** |
| 2 | Facture sans TVA | mention **« TVA non applicable »**, pas un taux à 0 % |
| 3 | Deux factures le même jour | numéros consécutifs, aucun trou |
| 4 | Document annulé | numéro conservé, statut `annulé`, absent des totaux |
| 5 | Paiement partiel 75 000 sur 150 000 | statut `partiel`, reste 75 000, reçu possible |
| 6 | Avoir sur facture payée | total recalculé, avoir lié à la facture d'origine |
| 7 | Impression A4 et mobile | lisible, pas de colonne coupée |
| 8 | Sauvegarde restaurée | toutes les pièces et tous les numéros |

Le test 1 et le test 5 sont ceux qui cassent en vrai. Les autres sont de la discipline.

---

## 7 · Ce qui reste à décider par toi

1. **Le régime fiscal d'AMK** — détermine toute la colonne TVA. Tant qu'il n'est pas tranché, l'outil ne peut pas produire une facture juste.
2. **Le nom exact qui figurera sur les factures** — doit être identique au RIB, au RCCM et au NIU.
3. **La numérotation** : `FAC-2026-0001` (lisible) ou une série par client. Je recommande une série unique par année — c'est ce qui se contrôle le plus facilement.
4. **Les conditions de règlement par défaut** : 50 % à la commande / 50 % à la livraison pour une installation ; payables d'avance le 1er du mois pour un retainer.

---

## 8 · Ce que cet outil change vraiment

Ce n'est pas de la bureaucratie. Aujourd'hui :

- le solde de 75 000 de DM Optique **n'a pas de pièce** ;
- l'acompte du 13/10 a été payé **en espèces, sans reçu** ;
- le prochain client n'a **aucun document** à recevoir ;
- et le retainer à trois clients se facturera **à la main, chaque mois**, avec le risque d'oublier.

Un outil qui règle ces quatre lignes vaut plus que n'importe quel tableau de bord. C'est le premier actif d'AMK qui ne dépend d'aucun client.
