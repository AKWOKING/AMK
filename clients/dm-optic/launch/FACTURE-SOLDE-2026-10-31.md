# Les deux pièces du 31/10 : la facture soldée et le reçu du solde

```
Objet     75 000 FCFA, le solde de l'installation DM OPTIQUE
Pièces    la facture AMK-2026-001 (soldée) + le reçu AMK-2026-001-R2 en deux exemplaires
Papier    A4, une feuille par pièce, à découper pour le reçu
Généré    python3 tools/facture/make_solde_dm.py
Date      29/10/2026
```

## 1 · Ce qu'il y a dans le dossier

| Fichier | Ce que c'est | Combien d'exemplaires |
|---|---|---|
| `FACTURE-SOLDE-AMK-2026-001.pdf` | la facture **AMK-2026-001**, 150 000 facturés, les deux encaissements, reste 0, tampon **PAYÉ** | 1 pour lui, 1 pour toi |
| `RECU-SOLDE-AMK-2026-001-R2.pdf` | **deux reçus identiques** sur une seule feuille, séparés par un trait de coupe : un « exemplaire client », un « exemplaire AMK » | 1 feuille, à découper |
| `*.png` | les mêmes, en image, pour vérifier sur le téléphone avant d'imprimer, ou si le PDF refuse de s'ouvrir dans WhatsApp | aucun |

Le reçu porte la mention **FACTURE SOLDÉE** et la somme en lettres : « Arrêté le présent reçu à la somme
de soixante-quinze mille (75 000 FCFA) pour le solde de la facture AMK-2026-001. » C'est cette phrase
qui fait foi dans un litige, pas le montant en chiffres.

## 2 · Ce qui reste à remplir à la main, le jour même

Trois choses, et trois seulement :

1. **Le mode de paiement**, sur le reçu : une ligne de points est laissée exprès. On n'écrit « espèces »
   que si c'est des espèces ; MoMo, OM ou virement s'écrivent aussi.
2. **Le tampon et la signature**, dans le cadre en bas du reçu, sur les deux exemplaires.
3. **La date** : les deux pièces sont datées du **31 octobre 2026**. Si l'encaissement tombe un autre
   jour, il faut régénérer (`SOLDE = {...}` en haut du script) : on ne gratte pas une date sur un reçu.

## 3 · L'ordre, samedi

L'argent avant tout le reste, et le papier avant la caméra :

1. il compte les 75 000 ;
2. tu remplis le mode de paiement, tu signes les deux reçus ;
3. tu lui donnes **le reçu client**, tu gardes l'autre, et tu poses la facture soldée à côté : elle
   archive les 150 000 d'un coup, pas seulement le solde du jour ;
4. **après** ça, la caméra. C'est la règle du déroulé (`content/tournage/SAMEDI-31-10-DEROULE.md`) :
   aucun appareil ne sort avant que le reçu soit signé.

## 4 · La saisie dans l'outil, pour que le téléphone dise la même chose que le papier

L'outil (`https://amk-factures-pwa.vercel.app`) vit dans le `localStorage` du téléphone : personne ne peut
le mettre à jour à distance, et c'est normal. Cinq gestes, une fois les 75 000 en poche :

1. ouvrir **AMK-2026-001** dans la liste ;
2. **Ajouter un paiement** ;
3. date **31/10/2026**, montant **75000**, mode de paiement réel ;
4. **Enregistrer** : l'écran doit passer à « Payée » et afficher **0 FCFA** restant ;
5. ouvrir ce paiement → **Reçu** → **Partager PDF** : c'est la sauvegarde du reçu, et elle t'évite de
   dépendre du papier.

Si l'étape 4 n'affiche pas 0, c'est que le deuxième paiement est en trop ou en double : on corrige dans
l'outil avant de quitter le cabinet, pas le lendemain.

## 5 · Ce que les pièces ne disent pas, volontairement

| Absent | Pourquoi | Ce qu'il faudra faire |
|---|---|---|
| **RCCM** | toujours manquant (`ops/ADMIN-FISCAL-AMK-2026-10-22.md` §2). L'outil, lui, imprime par défaut « RC / RCCM : Non applicable (personne physique sous NIU) » : c'est une affirmation que rien ne prouve. Une ligne absente ne se retourne pas contre nous ; une ligne fausse, si | dès que l'extrait est en main : la saisir dans les Réglages, et la ligne s'imprime toute seule sur les pièces suivantes |
| **TVA** | le régime fiscal n'est pas tranché (SPEC-FACTURATION §0). Écrire « TVA non applicable » serait trancher à sa place | trancher le régime, puis ajouter la ligne : 19,25 % ou la mention légale |
| **NIU du client** | `DM.niu` est vide dans l'outil ; le NIU de DM ne s'invente pas | le demander au cabinet, une fois, et le ranger dans sa fiche client |
| **« Conforme DGI », « facture normalisée »** | la loi de finances 2026 impose des plateformes agréées dont la liste n'est pas publiée ; l'outil n'en est pas une | jamais |

Aucun de ces quatre manques n'empêche d'encaisser et de signer : ils rendent la pièce contestable par
l'administration, pas par le client. C'est écrit ici pour que personne ne les découvre dans six mois.

## 6 · Un point à trancher, hors facture

Le dépôt `AKWOKING/AMK` est **public**, et `ops/amk-factures-pwa/index.html` y contient le **NIU d'AMK en
clair** (`DEFAULT_SETTINGS`, l.229). `ops/ADMIN-FISCAL-AMK-2026-10-22.md` §4 dit l'inverse de ce que le
dépôt fait : « jamais dans un dépôt public ». Deux sorties possibles, aucune n'est faite ici parce que ça
touche la PWA en production :

- **vider la valeur par défaut** et saisir le NIU une fois dans les Réglages du téléphone (il est déjà
  enregistré dans le `localStorage` de King, donc rien ne se perd sur son appareil) ;
- ou passer le dépôt en privé, ce qui laisse tout fonctionner mais coupe le déploiement Vercel public.

Le générateur de ces deux pièces porte le NIU parce qu'une facture sans NIU ne vaut rien. C'est le seul
endroit où il apparaît, avec l'outil lui-même.
