# DM OPTIQUE SARL — dossier client

> **État : accord verbal. Rien n'est public — ni site, ni page, ni fiche Google, ni contenu — tant que
> l'acompte n'est pas encaissé.**
>
> Créé le **01/10/2026** (jour de planification ; aucune production).
> Source de vérité commerciale : `leads/build/crm.py` → table `ACCORD_DM_0110` → `leads/CRM.csv`
> (`slug = dm-optique`, étape **`closing`**). Chronologie : `sales/Activity-Log.md` (entrée
> `2026-10-01 · 15:50 → 17:17`). Ce dossier **rassemble** ; il ne remplace ni le CRM ni le journal.

---

## 1 · Identité

| Champ | Valeur | Provenance |
|---|---|---|
| Raison sociale | **DM OPTIQUE SARL** | donnée par le client, 25/09 16:19 |
| Nom d'usage / profil WhatsApp | **DM OPTIC** | vu à l'écran par King (`wa_verified = yes`) |
| Activité | Cabinet d'optique médicale | registre ONOC |
| Titulaire / propriétaire | **M. Domche Noumbi** | registre ONOC, Littoral ligne 102 |
| Adresse | **Immeuble West Hotel, Ndobo Mayor, Bonabéri, Douala IV** | client, 25/09 16:19 (appliqué en v2.2 le 27/09) |
| WhatsApp | **656 122 239** (+237) | registre ONOC + vérifié à l'écran |
| Horaires | Ouverture **8h00** · Fermeture **17h30** · Consultation **8h30–13h30** | client, 25/09 16:19 |
| **Jours d'ouverture** | **INCONNUS** — il a donné les heures, jamais les jours | ⚠️ ouvert, voir `onboarding/intake-questionnaire.md` §2 |
| Langues | **FR prioritaire · EN secondaire** | décision de King |
| Forme juridique | **SARL** — possède un **NIU**, exige une **facture proforma** | client, 01/10 |
| Réglementaire | **ONOC** — Littoral **ligne 102**, inscription **021/2016**, arrêté ministériel **0382** | registre ONOC, lu le 24/09 |

**Contrainte de conformité qui gouverne tout le reste.** Le client est une **SARL sous contrôle
fiscal**. Il exige la traçabilité complète : **virement bancaire** (pas d'espèces), **facture proforma
PDF + RIB + NIU**, **reçus tamponnés**. Ce n'est pas une hésitation commerciale, c'est une exigence
comptable — elle se traite par des **documents**, jamais par un message. C'est ce qui a clos le deal
(01/10 17:08 : « C'est de confiance et rassurant »).

---

## 2 · Le deal

| Poste | Montant | Détail |
|---|---|---|
| **Installation** (one-shot) | **150 000 FCFA** | **75 000** à la signature (acompte) · **75 000** à la livraison |
| **Récurrent** | **30 000 FCFA / mois** | 2 publications/semaine (**1 UGC IA + 1 carrousel**) + maintenance du site |
| — dont budget publicitaire | **5 000 FCFA** | budget d'amorçage **inclus** dans les 30 000, pas en sus |

**Périmètre du Pack Global** : site web + mise en place Facebook/TikTok + gestion mensuelle.

**Statut : accord verbal.** En attente de : **facture proforma** (à émettre), **NIU du client**,
**acompte de 75 000 FCFA**. Aucun de ces trois éléments n'est reçu à l'heure où ce dossier est écrit.
L'étape CRM reste **`closing`** — elle ne passe à `won` qu'à l'encaissement.

**Règle de trésorerie.** ⛔ **Rien ne se livre, rien ne se publie, rien ne se produit avant
l'encaissement de l'acompte.** Aucun travail de production n'est engagé sur la seule foi de l'accord
verbal.

---

## 3 · Décisions de King — verrouillées, à ne pas re-négocier

Ces points sont tranchés. Ils ne sont pas des propositions ouvertes.

1. **Propriété des comptes.** Les comptes **Facebook et TikTok appartiennent au client**. Nous les
   mettons en place, **il les détient**, nous disposons d'un **accès administrateur**. Le jour où le
   contrat s'arrête, les comptes restent les siens. → à écrire **avant** toute création de compte
   (voir `pre-launch-checklist.md` item 4).
2. **UGC IA — nous n'écrivons que le script.** La **production vidéo est externe** (King). Notre
   livrable est **un fichier markdown par vidéo**, contenant : accroche (hook), beats, texte à
   l'écran, image de payoff, CTA, notes de direction. **Nous ne composons pas, ne rendons pas, ne
   posons pas de voix sur l'UGC IA.**
3. **Carrousels / diaporamas — nous produisons de bout en bout.** Montage, voix off, composition,
   rendu, QA, livraison du **MP4 fini**. Format : **vertical 9:16 · 1080×1920 · 30 fps · SAR 1:1 ·
   H.264**.
4. **Rien de public avant l'acompte.** Ni site, ni pages, ni fiche Google Business Profile, ni contenu.
5. **Visite sur site la semaine prochaine — mercredi 07/10 ou jeudi 08/10.** Cible de pré-lancement.
6. **Aujourd'hui (01/10) = planification et recherche.** Aucune production.

---

## 4 · Contraintes permanentes (valables pour tout le dossier)

| # | Contrainte | Application pratique |
|---|---|---|
| 1 | **FR prioritaire, EN secondaire** | Tout livrable client en FR d'abord ; l'EN suit, jamais l'inverse |
| 2 | **Chaque CTA mène à WhatsApp** | Aucun CTA mort : chaque bouton porte un `wa.me` pré-rempli |
| 3 | **Aucune allégation médicale** | « protège vos yeux », **jamais** « soigne », « guérit », « corrige la vue » |
| 4 | **Aucun témoignage, classement ou résultat inventé** | Zéro avis sur tout support tant qu'il ne vient pas d'un vrai patient |
| 5 | **Jamais nommer un concurrent** | Ni en bien ni en mal, ni par comparaison implicite nominative |
| 6 | **Jamais de remise** | On échange du **périmètre** ou du **calendrier**, jamais du prix |
| 7 | **Règle des 3 000 FCFA par message — appliquée, pas suggérée** | Coût par conversation WhatsApp > 3 000 FCFA → **la publicité est coupée**. Voir `content-plan-month1.md` §5 |
| 8 | **Tout le contenu vit dans le dépôt** | Rien dans le chat : chaque livrable est un fichier versionné |
| 9 | **UGC IA de verres/lentilles = dérogation** | Si demandé : **signaler comme dérogation** et noter le risque (voir §6) |

---

## 5 · Historique de contact

Chronologie complète et verbatim dans `sales/Activity-Log.md`. Résumé :

| Date | Événement |
|---|---|
| **24/09** 15:31 | Message du lot 4 envoyé : « je vous construis votre page, d'abord : vous l'ouvrez sur votre téléphone, vous décidez après » |
| **24/09** 15:54 | Réponse : **« Ok Envoyé svp... »** — premier oui |
| **24/09** nuit | Contrôle approfondi (6 recherches) + construction de l'aperçu v1 → v2 → v2.1 |
| **25/09** 16:08 | **« Ce que vous faites est bien »** — la page est approuvée par son destinataire |
| **25/09** 16:17 | Tarif « client fondateur » posé : 100 000 FCFA au lieu de 150 000, 50 000 d'acompte |
| **25/09** 16:19 | « Quelques Modifications » : raison sociale, adresse, horaires |
| **25/09** 16:41–16:57 | Il veut le site relié à TikTok et Facebook ; il bute sur le prix : **« Vous avez parlé de 12.000frs / mois Ici Comment on est sur 30.000frs ??? »** |
| **25/09** 16:59 | « Donnez moi le temps de réfléchir avec mes collaborateurs » |
| **26/09** 19:47 | « Je suis en déplacement imprévu. Nous en discutons lundi » |
| **27/09** | Corrections appliquées (v2.2) ; document `sales/DM-OPTIC-DEUX-COFFRETS-2026-09-27.md` (+ PDF) préparé pour lever la confusion 12 000 / 30 000 |
| **01/10** 15:50 | **« Le pack global semble nous correspondre »** — le client choisit |
| **01/10** 17:08 | **« C'est de confiance et rassurant »** ; puis deux messages supprimés (17:08, 17:09) — contenu inconnu, non deviné |
| **01/10** 17:17 | King précise : les 5 000 FCFA de pub sont **inclus** dans les 30 000 FCFA/mois |

**Ce qui a fait basculer le deal, et ce n'est pas le prix** : la **traçabilité**. Le client est une
SARL sous contrôle fiscal ; ce qui l'a rassuré, c'est la promesse de documents conformes (proforma,
RIB, NIU, reçus tamponnés, virement). Leçon consignée au journal le 01/10.

---

## 6 · Dérogations — registre

Une dérogation est une demande qui sort des décisions verrouillées du §3. Elle n'est pas refusée :
elle est **signalée**, son **risque est écrit**, et King tranche.

| Dérogation | Risque à noter | Statut |
|---|---|---|
| **UGC IA sur les verres / lentilles** | Un rendu IA d'un verre ou d'une lentille affirme une propriété optique qu'aucune prise de vue réelle ne garantit : reflet, traitement, teinte, épaisseur. Sur un produit de santé, une image générée qui exagère un traitement antireflet ou une teinte est une **allégation de fait sur un dispositif**. Risque : promesse non tenue, et exposition réglementaire sur un produit optique. **Recommandé : filmer le vrai verre, ou traiter le sujet par le geste (l'examen, le montage) plutôt que par le produit.** | aucune demande à ce jour |

---

## 7 · Ce qui manque pour avancer

Liste complète et actionnable : `onboarding/intake-questionnaire.md`. Les trois bloquants immédiats :

1. **NIU + adresse fiscale du client** — sans eux, la proforma ne peut pas être émise correctement.
2. **Nos propres identifiants de facturation** (RIB + NIU AMK au nom qui figure sur la proforma) —
   voir « bloquants » dans le rapport : une SARL sous contrôle fiscal ne peut pas régler une facture
   sans émetteur identifiable.
3. **Les photos réelles** — 3–4 photos du cabinet et 6–8 photos de montures. Les trois images de la
   vitrine actuelle sont des **illustrations**. Sans photos réelles : ni site final, ni carrousels.

---

## 8 · Actifs déjà construits (avant l'acompte — non publics)

| Actif | Chemin | État |
|---|---|---|
| Aperçu du site (une page, v2.2, orienté patient) | `demos/concept-dmoptic-v1.html` (166 Ko) | construit, **non publié**, `noindex` |
| Gabarit (source unique du texte) | `demos/dmoptic-v1.tpl.html` | — |
| Constructeur | `demos/build_dmoptic.py` | `--url` à recoller au déploiement |
| Dossier à déployer | `hosting/previews/dmoptic/` (`index.html` + `og.jpg`) | prêt, **non déployé** |
| Tests de comportement | `tools/qa/test_dmoptic_page.mjs` | **38/38** assertions |
| Document des deux coffrets | `sales/DM-OPTIC-DEUX-COFFRETS-2026-09-27.md` (+ `.pdf`) | envoyé / a servi à lever la confusion tarifaire |
| Liste de ce qu'il reste à envoyer | `clients/dm-optic/a-completer.md` | 9 points, dont 2 partiellement satisfaits |
| Notes de construction | `clients/dm-optic/build-notes.md` | 353 lignes, v1 → v2.2 |
| Inspiration & design read (24/09) | `clients/dm-optic/inspiration.md` | jeu de références **antérieur** — voir `website/inspiration.md` |

⚠️ **Écart d'adresse d'aperçu à trancher.** `build-notes.md` et `a-completer.md` citent
`https://dmoptic.vercel.app` ; le CRM (`site_url`) cite `https://dmoptic-2.vercel.app`. Une seule des
deux est réelle. À confirmer avant tout redéploiement — la vignette du lien (`og:url`, `og:image`) ne
peut pas être devinée.
