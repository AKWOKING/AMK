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
| Suivi (mensuel) | 30 000 | sauvegardes, mises à jour, 2 posts Google, rapport, 2 h de modifications |
| Croissance (mensuel) | 75 000 | Suivi + 8 pièces sociales, 4 posts Google, pub gérée, revue trimestrielle |
| Montée Présence → Standard | 120 000 | reconstruction, pas une remise |

**Trois contrôles avant d'envoyer une facture** (30 secondes, et ils évitent la mauvaise conversation) :

- [ ] le montant existe **dans cette table**, à la ligne près ;
- [ ] le périmètre écrit sur la facture est **celui de la ligne**, pas un mélange de deux paliers ;
- [ ] l'acompte est **50 %** et la facture suivante ne réclame que le reste (l'outil le calcule déjà).

## 3 · Ce qui reste à décider par King

1. ~~**Le canal d'encaissement** à afficher par défaut~~ — **réglé** : MoMo, Orange Money et les
   coordonnées bancaires figurent déjà sur la facture (King, 23/10). Reste seulement l'ordre d'affichage
   si les trois ne tiennent pas sur une ligne.
2. **La mention fiscale** : ni « conforme DGI » ni « facture normalisée » ne doivent apparaître tant que
   les spécifications ne sont pas publiées ; une phrase honnête est à écrire une fois (proforma + NIU +
   RIB, comme pour DM OPTIQUE) et à réutiliser.
3. **DM OPTIQUE : ne pas y toucher.** 30 000/mois accepté avant la grille, sans périmètre écrit →
   le prix reste, sans augmentation ni réduction. L'écart éventuel se règle **en heures livrées**,
   jamais en réécrivant le contrat. Toute nouvelle facture DM reste à 30 000.

## 3 bis · Ce que la facture porte — vérifié dans le code, le 23/10

**Deuxième correction, et la bonne cette fois.** J'avais d'abord écrit que les coordonnées de paiement
manquaient (faux : King l'a dit), puis que **seule l'échéance** manquait — **faux aussi**. J'ai ouvert le
code le 23/10 (`amk-factures-pwa.zip`, 750 lignes, source copiée dans `ops/amk-factures-pwa/`) :

| Élément | État réel, lu dans le code |
|---|---|
| Numéro annuel continu | ✅ `nextNumber()` — `AMK-2026-001`, séquence par préfixe et par an |
| Date d'émission | ✅ `inv.date` |
| **Date d'échéance** | ✅ `inv.due`, **+14 jours par défaut**, réglable (`dueDays`) |
| **Statut « en retard »** | ✅ `statusOf()` compare `due` à aujourd'hui, badge dans la liste |
| Lignes détaillées, remise, acomptes | ✅ `calc()` : sous-total, remise, payé, solde |
| **Proforma et reçu de paiement** | ✅ `docType:'proforma'`, reçu avec mode de paiement |
| **MoMo · Orange Money · banque · NIU** | ✅ dans les réglages et imprimés sur le PDF |
| Modèles de message (acompte, solde, relance, mensuel) | ✅ `MSG_KINDS` + `suggestKind()` |
| Sauvegarde | ✅ copier-coller du JSON (`copyBackup`) |
| PDF et envoi WhatsApp | ✅ |

**Conclusion honnête : l'outil était déjà complet sur tout ce que j'avais listé.** Deux fois de suite j'ai
affirmé un manque sans ouvrir le fichier — c'est exactement ce que le §0e interdit. La leçon est écrite
dans `ops/amk-factures-pwa/README.md` : **on lit le code avant de dire ce qui manque.**

## 3 ter · Les trois ajouts du 23/10 (et rien d'autre)

| # | Ajout | Pourquoi |
|---|---|---|
| 1 | **`dont X en retard`** sous « À encaisser » | le total dû mélangeait le courant et le retard : on ne voyait pas ce qui est déjà en faute |
| 2 | **`en retard de N jours`** sur la ligne | « Reste 75 000 » ne dit pas depuis quand ; la priorité de relance se lit d'un coup d'œil |
| 3 | **`Enregistrer un fichier`** à côté de « Copier la sauvegarde » | un presse-papiers se perd ; un `.json` daté se range dans les notes |

Aucune refonte, aucune migration de données : les trois lisent des champs qui existaient déjà.

**Procédure de déploiement** (état : source dans `ops/amk-factures-pwa/`, projet Vercel
`amk-factures-pwa-preview` lié à la branche, **preview seulement** ; la production ne bouge que sur le
feu vert de King) :

1. `node --check` sur le script extrait — **fait, OK** ;
2. test fonctionnel sur un téléphone : une facture antidatée doit afficher « en retard de N jours » ;
3. preview d'abord, capture à King, production **après son accord**.

**Où en est le déploiement, le 23/10 (vérifié, pas supposé) :**
- la **source** est dans le dépôt, `ops/amk-factures-pwa/`, commit `54e90f7` ;
- un projet Vercel **`amk-factures-pwa-preview`** (`prj_p0jOq44hpb98NhiYg1ViNzJOXVZw`) a été créé, lié
  au dépôt `AKWOKING/AMK`, racine `ops/amk-factures-pwa` ;
- **l'envoi des fichiers par le connecteur a échoué** (`projectSettings` exigé pour un projet neuf), et un
  déploiement d'essai sans les bons fichiers a été supprimé : rien n'a bougé en production ;
- **le chemin qui reste, et il est propre :** dans Vercel → `amk-factures-pwa-preview` → *Deployments* →
  *Create deployment* → branche `arena/000d42c4-amk`. Le fichier publié est alors celui du dépôt, donc
  exactement celui qui a été vérifié. La production reste sur l'ancienne version tant que King n'a pas dit oui.

## 4 · Ce que l'outil ne fera jamais à notre place

Il ne dit pas si le prix est juste, il ne dit pas si le travail est livré, et il ne remplace pas la
phrase qui compte au client : **« voilà ce que vous avez reçu ce mois-ci »**. C'est le rapport d'une
page (`knowledge/MAINTENANCE-CLIENTS-2026-10-22.md` §4) qui justifie le prélèvement, pas la facture.
Facturer le 1er, envoyer le **récap d'une page + le rapport** le 2 : l'ordre est déjà écrit, il ne
reste qu'à le tenir. Le récap se régénère en deux minutes (`tools/ops/make_recap.py --data …`, gabarit `tools/ops/recap-modele.json`),
ce qui est la seule façon qu'il parte vraiment tous les mois.
