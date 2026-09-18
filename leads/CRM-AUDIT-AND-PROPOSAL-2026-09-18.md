# CRM — audit du fichier de leads et proposition d'architecture

**Date :** vendredi 18 septembre 2026 · **Statut : PROPOSITION — rien n'est migré, rien n'est déplacé.**
**Documents lus :** `leads/leads_50.xlsx` (5 feuilles) · `leads/Daily Ops.csv` · `leads/*.py` (12 scripts) · `sales/AMK-Sales-Playbook-v2.md` · `sales/Pipeline-Status.md` · `sales/Activity-Log.md` · `sales/MQL-Qualification-2026-09-18.md` · `sales/Clinic-Batch-2026-09-15.md` · `sales/Remote-Sweep-1-Douala-2026-09-15.md` · `sales/Walk-In-*.md` · `sales/Outreach-Pack-*.md` · `sales/Send-*.md` · `clients/*/`.

---

## 1 · Combien de leads existent aujourd'hui

| Où | Nombre | Nature |
|---|---|---|
| `leads_50.xlsx` → onglet **« Leads 50 »** | **38** | Le seul tableau structuré. Malgré son nom, 38 lignes. |
| `leads_50.xlsx` → onglet DAILY OPS | — | Tableau de bord du jour, pas une liste de leads |
| `leads_50.xlsx` → onglets *Deep Dive*, *Daily Tracker*, *Pipeline - 5 Stages* | — | Vues et rapports, alimentés à la main |
| `leads/Daily Ops.csv` | — | **Export de l'onglet DAILY OPS** — même contenu, autre format |
| `sales/*.md` | **14 leads suivis hors fichier** | Tous les leads cliniques/optiques de Douala |
| `sales/Remote-Sweep-1-Douala` §C | **12 labos** | Réservoir brut, jamais qualifié |

### Le chiffre qui compte

**38 leads dans le fichier maître + 14 leads suivis uniquement dans des documents Markdown = 52 organisations identifiées**, plus 12 labos en réserve.

**Et le problème structurel est là :** les 14 leads absents du fichier — OraCare, The Skye, YAKS, L'Opticien, La Béthanie, JEMPO, AFRIQUE LABO, JOSS MEDI, Maison Optique, CAMERA, LE NID, Wonders Medical, Adonaï, Malia Labo — **sont exactement ceux que nous avons contactés.** Le fichier maître ne contient aucun des leads engagés de Douala. Il contient des écoles que nous n'avons jamais jointes.

Autrement dit : **le fichier maître décrit la partie du pipeline qui n'a pas bougé, et ignore celle qui a bougé.**

---

## 2 · Champs actuellement suivis

Onglet « Leads 50 » — **26 champs :**

`ID · School · City · Language · Facebook · Website · Website status · Last FB post · FB followers · Admissions activity · Phone · WhatsApp · Decision maker · Contact channel · Facilities · Multiple branches · Lead score · Priority · Demo made · Contacted · Reply · Conversation · Offer made · Deposit · Sale · Follow-up date · Notes`

`Daily Ops.csv` : aucune colonne exploitable — un tableau de bord mis en forme, **7 numéros de téléphone sur 50 lignes**.

---

## 3 · Champs manquants mais nécessaires

Sept manques, chacun payé par une erreur déjà commise cette semaine :

| Champ manquant | L'erreur qu'il aurait évitée |
|---|---|
| **`language`** *(existe mais jamais rempli — voir §4)* | Les 3 maquettes en français pour Buea, région anglophone |
| **`whatsapp_verified`** + `whatsapp_verified_on` + `profile_name_seen` | 696 023 696 = « Kingdom Family Int'l » (une entreprise de finances) · 677 647 802 sans photo de profil |
| **`reply_type`** (human / auto / none) | La réponse automatique d'Adonaï aurait pu être comptée comme une réponse |
| **`last_send_state`** (sent / delivered / read) | « Envoyé » écrit comme « répondu » — mon erreur du 18/09 |
| **`site_url`** + `site_checked_on` | QUALITECH et Clinique des Anges : deux maquettes produites **avant** de découvrir qu'un site existe |
| **`disqualified`** (valeur de stage) + `disqualification_reason` | 8 leads aujourd'hui sans case où vivre : Summerset, Saint Bernard, NABESK, Divine Success, Awae (aucun canal), ICHS (litige), QUALITECH, Clinique des Anges (site existant) |
| **`added_on`** | La métrique hebdomadaire « nouveaux leads » est incalculable sans elle |

**Manquent aussi, demandés par votre schéma et absents du fichier actuel :** `source`, `source_detail`, `first_touched`, `stage_since`, `last_message_sent`, `last_reply_received`, `follow_ups_sent`, `preview_sent`, `preview_asset`, `proposal_sent`, `price_quoted_fcfa`, `invoice_sent`, `closed_on`, `closed_value_fcfa`, `health`.

**Le fichier actuel ne contient aucun champ de suivi temporel.** `Contacted`, `Reply`, `Follow-up date` sont les seuls, et ils sont renseignés à la main, en texte libre, sans date normalisée.

---

## 4 · Recouvrement, contradictions et doublons

### ① Les deux fichiers ne se recouvrent pas — ils se contredisent

`Daily Ops.csv` **est un export de l'onglet DAILY OPS** du même classeur. Ce n'est pas une seconde source : c'est la même source en double, et les deux sont **périmées au 16/09**.

### ② Contradictions relevées (11)

| # | Contradiction | Gravité |
|---|---|---|
| 1 | `Pipeline-Status.md` annonce **27 leads** ; le classeur en contient **38** | Moyenne |
| 2 | Le classeur **ne contient aucun des 14 leads engagés de Douala** — il liste des écoles jamais contactées à la place | **Critique** |
| 3 | La liste de mort du playbook est « les deux 18 » (COMOBIL, OraCare) — mais **COMOBIL est parqué** et **OraCare n'est pas dans le fichier**. La règle est inapplicable depuis les fichiers | **Critique** |
| 4 | Onglet DAILY OPS : COMOBIL en **tête de kill list** ; `Pipeline-Status` : COMOBIL **parqué** | Élevée |
| 5 | Solidarity : le classeur dit « **scheduled Tue** » ; `Pipeline-Status` dit **WA bloqué → parqué** | Élevée |
| 6 | Ligne St. Theresa : **colonnes décalées** — la cellule « Lead score » contient le texte de la réponse, pas un score | Élevée |
| 7 | Colonne `Language` présente mais **peu ou pas remplie** — la donnée qui manquait pour Buea | Élevée |
| 8 | `Contacted` vide pour L'Opticien, La Béthanie, JEMPO, AFRIQUE LABO — **parce que ces lignes n'existent pas** | Élevée |
| 9 | **Trois vocabulaires de stage** : classeur 1-5 + « PARK » · `Pipeline-Status` « parked-warm-with-permission », « BOARD-BUYER », « INBOUND » | Moyenne |
| 10 | NABESK : « 83,5 % au O-Level » → en réalité **83,46 % au A-Level 2020** | Moyenne (exactitude) |
| 11 | GS WAFO (#2) fusionné dans COMOBIL (#1) selon `Pipeline-Status`, mais **reste une ligne séparée** avec son propre score | Faible |

### ③ Doublons

- **Fichiers :** `Daily Ops.csv` ↔ onglet DAILY OPS (même contenu, deux formats).
- **Leads :** COMOBIL ↔ GS WAFO (même promoteur, même contact, 5 institutions) — **un seul acheteur, deux lignes**.
- **Scripts :** 12 scripts `patch*.py` dans `leads/` — quatre sont marqués *SUPERSEDED* dans leur propre en-tête et refusent de s'exécuter. **Ces scripts sont la seule trace de plusieurs corrections** : s'ils partent, l'histoire part avec eux.

---

## 5 · Engagés, froids, morts

**11 leads engagés** (un message au moins est parti) · **0 lead mort** (personne n'a dit non) · **1 lead parké-warm** (St. Theresa, permission de revenir en octobre).

| Classe | Nombre | Qui |
|---|---|---|
| **Engagé — en attente de réponse** | **11** | OraCare · MITOC · Baptist Comprehensive · Baird Memorial · The Skye · YAKS · AFRIQUE LABO · L'Opticien · La Béthanie · JEMPO · Adonaï · Malia |
| **Engagé — réponse obtenue** | **1** | St. Theresa (parkée-warm, retour en octobre) |
| **Qualifié, jamais contacté** | **3** | Cabinet Médical CAMERA · Polyclinique LE NID · Wonders Medical Foundation (Wonders sans numéro vérifié) |
| **À vérifier (canal non confirmé)** | **12** | Les écoles de Douala/Buea sans numéro confirmé |
| **Disqualifié** | **8** | Summerset, Saint Bernard, NABESK, Divine Success, BHS Awae (aucun canal) · ICHS (litige) · QUALITECH, Clinique des Anges (site existant) |
| **Parké** | **5** | COMOBIL/WAFO · SAHISCOL · La Retraite · JOSS MEDI · Solidarity |
| **Réserve non qualifiée** | **12** | Labos du `Remote-Sweep` §C |

> **Note :** après vérification, **OraCare et MITOC n'ont répondu ni l'un ni l'autre.** Les deux messages n'ont même pas été lus. La seule réponse humaine de toute la campagne reste St. Theresa.

---

## 6 · Schéma proposé — et ce que je changerais

Votre schéma est bon. **Je propose 8 ajouts et 2 retraits**, chacun justifié par un fait, pas par une préférence.

### Ajouts

| Champ | Type | Pourquoi |
|---|---|---|
| `language` | `EN` / `FR` / `both` | **Obligatoire.** La langue se déduit de la région : Sud-Ouest et Nord-Ouest = EN ; Littoral et Centre = FR. C'est ce champ qui aurait empêché les maquettes françaises pour Buea. |
| `whatsapp_verified` | `yes` / `no` / `unknown` | Porte d'entrée : un numéro non vérifié ne s'envoie pas. |
| `profile_name_seen` | texte | Le nom affiché à la vérification — c'est ce qui a révélé « Kingdom Family Int'l ». |
| `reply_type` | `human` / `auto` / `none` | Adonaï envoie un message d'accueil automatique. Il ne doit jamais gonfler le PRR. |
| `last_send_state` | `sent` / `delivered` / `read` | « Envoyé ≠ lu ≠ répondu » devient une donnée, plus une consigne. |
| `site_url` + `site_checked_on` | URL + date | Deux maquettes produites avant de découvrir un site existant. On vérifie **avant** de produire. |
| `disqualification_reason` | texte | 8 leads disqualifiés n'ont aujourd'hui aucune case où exister. |
| `mockup_path` | chemin | Un aperçu et une maquette ne sont pas la même chose : la maquette existe souvent sans qu'aucun lien n'ait été envoyé. |

### Retraits

| Champ | Pourquoi |
|---|---|
| `kill_list` (stocké) | **À dériver, pas à stocker.** La règle est « les deux 18 + tout nouveau oui ». Stocké à la main, il dérive — c'est exactement ce qui est arrivé à l'onglet DAILY OPS. `KILL-LIST.md` le recalcule à chaque génération. |
| `health` (stocké) | **À dériver par défaut** : aucun mouvement depuis 7 jours = `cold`, 21 jours = `dead`. Le champ reste **modifiable à la main** pour les cas particuliers (St. Theresa est froide en date mais chaude en intention). |

### Ajouts dans les valeurs, pas dans les colonnes

**`source` — votre énumération ne couvre pas nos vraies sources.** Nous recrutons par annuaire (DoualaTour), Google Maps, Facebook, TikTok, PDF du GCE Board, et portails. Proposition :

`directory` · `google_maps` · `facebook` · `tiktok` · `gce_board` · `walk_in` · `referral` · `inbound` · `outreach_pack` · `content_video` · `other`

**`stage` — ajouter `disqualified`** à votre énumération. Sinon 8 leads sont rangés dans `lost`, ce qui est faux : ils n'ont jamais été perdus, ils n'ont jamais été jouables.

---

## 7 · Structure de dossiers proposée

```
leads/
  CRM.csv                        ← l'index, une ligne par lead
  records/
    adonai-douala.md
    malia-labo-douala.md
    oracare-buea.md
    st-theresa-molyko.md
    ...                          ← un fichier par lead ayant un historique
  PIPELINE.md                    ← généré
  KILL-LIST.md                   ← généré, quotidien
  STALE.md                       ← généré, hebdomadaire
  SOURCES.md                     ← généré
  reports/
    WEEKLY-SALES-REPORT-2026-09-18.md
  archive/
    leads_50.xlsx
    Daily Ops.csv
    patch1.py … patch4.py        ← les scripts marqués SUPERSEDED
  build/
    crm.py                       ← extraction, dédoublonnage, génération des vues
  CRM-AUDIT-AND-PROPOSAL-2026-09-18.md   ← ce fichier
```

**Deux points importants :**

- **`sales/Activity-Log.md` reste** tel quel. C'est le journal chronologique — l'append-only — et il précède le CRM. Il ne sera pas remplacé : `CRM.csv` dit où en est chaque lead, `Activity-Log.md` dit ce qui s'est passé et quand. Le registre et le journal, pas l'un ou l'autre.
- **`leads/archive/`** reçoit les originaux, jamais la corbeille. Rien n'est supprimé.

---

## 8 · Plan de migration (à exécuter après votre accord)

1. **Extraire** les 38 leads de l'onglet « Leads 50 » et les 14 leads des documents `sales/`.
2. **Dédoublonner** — COMOBIL/WAFO à fusionner en une fiche, un acheteur.
3. **Signaler** les 11 contradictions du §4 avec la valeur retenue et la valeur écartée, pour arbitrage.
4. **Créer un `records/<slug>.md`** pour chaque lead ayant un historique réel — soit **15 fiches** (11 engagés + St. Theresa + 3 suivis).
5. **Construire `CRM.csv`** : 52 lignes, valeurs déduites là où la donnée existe, **cases vides là où elle n'existe pas** — jamais d'invention.
6. **Archiver** `leads_50.xlsx`, `Daily Ops.csv` et les 4 scripts périmés vers `leads/archive/`.
7. **Générer** les premières vues : `PIPELINE.md`, `KILL-LIST.md`, `STALE.md`, `SOURCES.md`.
8. **Vous montrer le résumé** avant de considérer la migration terminée.

**Ce qui change :** un seul fichier maître, daté, triable ; les vues ne se modifient plus à la main ; chaque lead a son histoire.
**Ce qui est préservé :** les originaux archivés, `Activity-Log.md` intact, tous les dossiers `clients/`, et l'historique des 12 scripts `patch`.

---

## 9 · Métriques — et la réponse sur le PRR

Vos 12 métriques sont calculables depuis le schéma proposé, **à deux exceptions près** : « nouveaux leads » exige `added_on` (ajouté), et « temps moyen avant première réponse » exige des dates horodatées, pas « mardi ».

**Sur le PRR :** votre définition est la bonne — *leads ayant répondu au moins une fois ÷ leads contactés*. **Je propose de la durcir** : **les réponses automatiques sont exclues**. Adonaï a envoyé un message d'accueil machine 60 secondes après notre message ; le compter comme une réponse fausserait la seule métrique qui dit la vérité sur notre approche.

**Et je propose un second indicateur, `ARR` (taux de réponse automatique)** — non pas comme une réponse, mais comme un **signal d'achat** : une entreprise qui a configuré un message d'accueil automatique est déjà équipée en digital. C'est un bon prospect, pas un mauvais. Adonaï en est la preuve.

**Deux métriques à ajouter**, parce qu'elles manquent et qu'elles nous concernent directement :

- **`PRR` par source** — il répond à votre question « quelle source produit le meilleur taux de qualification ». Aujourd'hui on ne peut pas y répondre.
- **Délai moyen avant première réponse** — mesure la règle des 90 secondes, qui est notre argument de vente et notre faiblesse opérationnelle actuelle.

---

## 10 · Questions avant de construire

1. **PRR** — voulez-vous ma version durcie (réponses humaines uniquement) ou la version simple (toute réponse) ? Et garde-t-on `ARR` comme indicateur d'équipement digital ?
2. **Y a-t-il des leads dans l'historique de conversation qui ne sont dans aucun fichier ?** **Oui — j'en ai trouvé 14** (§1). Le classeur n'en contient aucun. *Est-ce qu'il vous arrive d'avoir approché quelqu'un que je n'ai jamais vu, hors WhatsApp existant ?* Dans ce cas, dites-le moi et je l'intègre.
3. **COMOBIL** — la règle du playbook dit qu'il est l'un des deux 18 de la kill list ; votre décision du 14/09 l'a parqué faute de canal. **Laquelle gagne ?** Je propose : il reste dans la kill list **comme incident de canal** — c'est-à-dire qu'on le remonte à chaque fois qu'une Page Facebook AMK est évoquée, pas chaque matin.
4. **St. Theresa** — `health` la dirait `cold` (3 jours sans mouvement) alors qu'elle a donné une permission. Confirmez-vous que `health` reste **modifiable à la main** pour ce genre de cas ?
5. **Les 12 labos en réserve** (`Remote-Sweep` §C) : ils entrent au CRM comme `prospect` à qualifier, ou restent hors CRM jusqu'à vérification du canal ?

---

## Ce que je ferais différemment de votre plan — en un paragraphe

Votre architecture est la bonne et je ne propose **aucun changement de fond** : un index, des fiches, des vues dérivées. Mes trois ajustements tiennent en une phrase chacun. **Un :** les vues dérivées doivent porter un en-tête *généré le … — ne pas modifier à la main*, sinon elles finiront comme l'onglet DAILY OPS. **Deux :** `health` et `kill_list` se calculent, ils ne se stockent pas — c'est précisément le stockage manuel qui a laissé le fichier mentir pendant quatre jours. **Trois :** la discipline d'écriture doit être mécanique, pas volontaire : **si un envoi n'est pas dans `Activity-Log.md` et dans `CRM.csv` dans la même réponse, il n'a pas eu lieu.** C'est la seule règle qui aurait empêché mon erreur de ce matin.
