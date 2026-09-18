# CRM — audit des fichiers de leads et proposition d'architecture (v2)

**Date :** vendredi 18 septembre 2026 · **Statut : PROPOSITION — rien n'est migré, rien n'est déplacé, aucun fichier n'est renommé.**
**v2 remplace la v1 du même jour** : l'audit a été refait sur les fichiers exacts demandés par King, et il **corrige une affirmation fausse de la v1**.

**Documents lus :** `leads/leads_50.xlsx` (5 onglets) · `leads/Daily Ops.csv` · `leads/build_daily_ops.py` · `leads/build_sheet.py` · `leads/add_walkin_leads.py` · les 8 dossiers `clients/<slug>/` · `PRE-FLIGHT.md` · `sales/AMK-Sales-Playbook-v2.md` · `sales/Outreach-*.md` (7 fichiers) · `sales/Pipeline-Status.md` · `sales/Activity-Log.md` · `sales/Remote-Sweep-1-Douala-2026-09-15.md` · `sales/Clinic-Batch-2026-09-15.md` · `sales/Walk-In-*.md`.

---

## 0 · D'abord, deux corrections de ma part

**① Le champ `Language` n'est pas vide. Il est rempli, pour les 38 leads.**

Répartition réelle : `EN` **15** · `FR/EN` **13** · `FR` **3** · `EN/FR` **3** · `Bilingual EN/FR` **3** · `FR (N/V)` **1**.

La ligne de Summerset dit **EN/FR**, celle de NABESK dit **EN**. **Le CRM avait la réponse, je ne l'ai pas lue.** C'est exactement la même erreur que les fausses réponses d'OraCare et MITOC : **j'ai travaillé de mémoire au lieu de lire le fichier.** Ma v1 proposait d'ajouter un champ `language` — c'est inutile, il existe. (Une amélioration utile reste : normaliser les six variantes d'écriture en trois valeurs `EN` / `FR` / `both`, pour que ce soit filtrable.)

**② `sales/AMK-Sales-Playbook-v2.md` et les packs existent.** Vérifié fichier par fichier — voir §2.

---

## 1 · Combien de leads uniques

| Où vivent les leads | Nombre |
|---|---|
| `leads_50.xlsx` → onglet **« Leads 50 »** | **38** |
| `leads_50.xlsx` → onglet **« Pipeline - 5 Stages »** — contient **OraCare237**, absent de « Leads 50 » | **+1** |
| Pistes présentes **uniquement en prose** (`sales/*.md`, `clients/*/`) | **+15** |
| **Total d'organisations identifiées** | **54** |
| Réserve brute, jamais qualifiée (`Remote-Sweep` §C, labos) | 12 (hors total) |

Les 15 hors classeur : **The Skye · YAKS · AFRIQUE LABO · JOSS MEDI · L'Opticien Bali · La Béthanie · JEMPO/J&E Memorial · Maison Optique · Cabinet Médical CAMERA · Polyclinique LE NID · Wonders Medical · Cabinet Biomédical Adonaï · Malia Labo · QUALITECH · Clinique des Anges.**

**Ce que ce chiffre dit :** le classeur maître ne contient **aucun** des leads engagés de Douala. Il décrit la partie du pipeline qui n'a pas bougé et ignore celle qui a bougé.

---

## 2 · Les fichiers cités existent-ils ?

**Oui — tous.** Réponse sans détour, contenu non inventé :

| Fichier | Existe | Taille |
|---|---|---|
| `leads/leads_50.xlsx` | ✅ | 40 340 o |
| `leads/Daily Ops.csv` | ✅ | 8 019 o |
| `leads/build_daily_ops.py` | ✅ | 9 197 o |
| `leads/build_sheet.py` | ✅ | 36 829 o |
| `leads/add_walkin_leads.py` | ✅ | 6 449 o |
| `PRE-FLIGHT.md` | ✅ | 7 354 o |
| `sales/AMK-Sales-Playbook-v2.md` | ✅ | 33 247 o (v2.2, 17/09) |

**Packs d'outreach présents :** `Outreach-Pack-2026-09-14.md` · `Outreach-Pack-2026-09-16.md` · `Monday-Outreach-Pack.md` · `Outreach-AFRIQUE-LABO-v1.md` · `Outreach-JEMPO-v1.md` · `Outreach-LOpticien-v1.md` · `Outreach-LaBethanie-v1.md` · `Outreach-Pivot-2026-09-18.md`.

⚠️ **Un fichier que personne ne trouvera : il n'existe pas d'`Outreach-Pack-2026-09-18.md`.** Les productions du 18/09 s'appellent `Send-Pack-2026-09-18-1030.md` et `Send-Pack-Douala-Cliniques-2026-09-18.md`. Si un document cite un « pack du 18/09 », c'est une référence morte.

---

## 3 · Champs du classeur et complétude

**26 colonnes :** `ID · School · City · Language · Facebook · Website · Website status · Last FB post · FB followers · Admissions activity · Phone · WhatsApp · Decision maker · Contact channel · Facilities · Multiple branches · Lead score · Priority · Demo made · Contacted · Reply · Conversation · Offer made · Deposit · Sale · Follow-up date · Notes`

### Aucun lead n'a de champ vide — et c'est le problème

**0 case blanche sur les 11 champs clés, pour les 38 lignes.** L'absence est **écrite en toutes lettres** :

| Constat | Nombre |
|---|---|
| `Phone` n'est **pas un numéro** (mais `N/V`, `not listed`, `not published anywhere`) | **16 / 38** |
| `WhatsApp` n'est **pas un numéro** (`N/V (landline)`, `Likely same (mobile)`, `none found`, `verify on walk-in`) | **27 / 38 — 71 %** |

**Seuls 11 leads sur 38 ont un numéro WhatsApp réellement écrit dans le fichier.** C'est l'explication chiffrée du blocage d'aujourd'hui — et c'est un problème de **type de donnée**, pas de rigueur : « pas de numéro » est écrit comme une phrase, donc **ni triable, ni filtrable, ni comptable**. Un `CRM.csv` doit porter `wa_verified = unknown` et une case vide, pas une phrase.

---

## 4 · `clients/<slug>/` → lignes du classeur

| Dossier | Ligne correspondante |
|---|---|
| `clients/nabesk/` | **30 — NABESK** ✅ |
| `clients/saint-bernard/` | **29 — Saint Bernard** ✅ |
| `clients/summerset/` | **28 — Summerset** ✅ |
| `clients/afrique-labo/` | ❌ **aucune ligne** |
| `clients/jempo/` | ❌ **aucune ligne** |
| `clients/l-opticien/` | ❌ **aucune ligne** |
| `clients/la-bethanie/` | ❌ **aucune ligne** |
| `clients/douala-cliniques/` (6 maquettes) | ❌ **aucune ligne** |

**5 dossiers clients sur 8 n'ont aucune ligne dans le classeur.** Ce sont les dossiers qui contiennent le travail réel — concepts, inspirations, notes de build — et ils ne sont référencés nulle part dans le fichier maître.

**Piège de dédoublonnage à signaler :** une simple recherche du mot « NABESK » fait remonter **la ligne 31 (Baird Memorial)**, parce que ses notes disent *« otherwise Wed card drop same road as NABESK »*. Une déduplication par mot-clé produirait une fausse fusion. Le rapprochement devra se faire **sur l'identifiant, jamais sur le texte**.

---

## 5 · `Daily Ops.csv` — leads ou notes opérationnelles ?

**50 lignes, dont 7 vides → 43 lignes utiles.**

| Nature | Nombre | Exemples |
|---|---|---|
| **État de lead** (le seul contenu CRM) | **12** | L7 OraCare · L8 Skye · L9 YAKS · L10 AFRIQUE LABO · L11 JOSS · L13 MITOC · L14 Baird · L15 St. Theresa · L16 Holds & parks · L20 FU OraCare · L23 FU Baird · L24 FU MITOC |
| **Notes opérationnelles** | **18** | En-têtes de section, `Lead / Why hot / Next action / Done?`, cases à cocher |
| **Consignes permanentes** | **6** | L36 file d'attente AMK · L37 règle des mockups · L47 journaliser chaque envoi · L48 que faire sur un « oui » · L49 points bloqués |
| **Exercices d'entraînement** | **4** | L40-L42 drills EN/FR · L44 dimanche off |
| **Créneaux et décisions** | **3** | L29 14:00-14:15 · L30 14:30-16:00 envois FR · L33 sweep annulé |

**Conclusion : 12 lignes sur 43 (28 %) sont de la donnée de lead.** Les 31 autres sont de la logistique. **Le nom du fichier ment** — ce n'est pas une liste de leads, c'est un plan de journée. Votre proposition de le renommer `Daily-Plan.csv` est la bonne, et je propose mieux : **qu'il soit généré depuis le CRM**, sinon il redeviendra faux (il est déjà périmé au 16/09).

---

## 6 · Contradictions à arbitrer

| # | Contradiction | Gravité |
|---|---|---|
| 1 | **La kill list du playbook est inapplicable depuis les fichiers** : elle dit « les deux 18 » = COMOBIL + OraCare. COMOBIL est **parké**, OraCare **n'est pas dans la table des leads** | **Critique** |
| 2 | Le classeur contient **0 des 15 leads engagés de Douala** et liste à leur place des écoles jamais contactées | **Critique** |
| 3 | **5 dossiers `clients/` sur 8 n'ont aucune ligne** dans le classeur | Élevée |
| 4 | **71 % des leads n'ont pas de numéro WhatsApp** exploitable, l'absence étant écrite en prose | Élevée |
| 5 | COMOBIL : **tête de kill list** dans l'onglet DAILY OPS, **parké** dans `Pipeline-Status` | Élevée |
| 6 | Solidarity : « scheduled Tue » au classeur, **parqué** dans `Pipeline-Status` | Élevée |
| 7 | **Ligne 27 (St. Theresa) décalée** : la cellule « Lead score » contient le verbatim de la réponse | Élevée |
| 8 | `Daily Ops.csv` est un **export de l'onglet DAILY OPS** — même contenu, deux formats, périmés au 16/09 | Moyenne |
| 9 | Trois vocabulaires de stage concurrents ; `Pipeline-Status` dit 27 leads, le classeur en a 38 | Moyenne |
| 10 | NABESK : « 83,5 % au O-Level » → en réalité **83,46 % au A-Level 2020** | Moyenne |
| 11 | GS WAFO (#2) fusionné dans COMOBIL (#1) selon `Pipeline-Status`, mais **reste une ligne séparée** avec son score | Faible |

---

## 7 · Schéma proposé — ajusté à ce que l'audit montre

**Toutes les colonnes du classeur sont conservées, à l'identique, avec leurs noms.** Rien n'est remplacé. J'ajoute ce que l'audit démontre manquant — **et je retire une addition de ma v1.**

### ~~`language`~~ — **annulé**
Le champ existe et il est rempli (§0). Rien à ajouter. Seule amélioration : normaliser les 6 variantes.

### Ajouts (9)

| Champ | Type | La preuve qui le justifie |
|---|---|---|
| `slug` | texte | 5 dossiers `clients/` orphelins : il faut une clé qui relie dossier et ligne |
| `org_type` | school / clinic / lab / other | Le classeur est scolaire à 82 % (31/38) ; les cliniques arrivent par la prose et n'ont pas de place |
| `contact_name` · `contact_role` | texte | « Decision maker » contient des phrases entières (`« Principal (capture) »`, `« Dr Njang… (co-owner; also DMO…) »`) |
| `wa_number` | numérique ou vide | **27/38 lignes ont une phrase au lieu d'un numéro** : il faut une colonne triable à côté du texte conservé |
| `wa_verified` | yes / no / unknown | C'est la porte qui a laissé passer « Kingdom Family Int'l » |
| `profile_name_seen` | texte | Le nom vu à la vérification — la donnée qui a révélé l'erreur |
| `reply_type` | human / auto / none | Adonaï envoie un accueil automatique ; il ne doit jamais gonfler le PRR |
| `last_send_state` | sent / delivered / read | « Envoyé » a été écrit comme « répondu » |
| `site_url` + `site_checked_on` | URL + date | QUALITECH et Clinique des Anges : 2 maquettes produites avant de découvrir un site existant |

### Ajouts pour la gestion (7)

`source` · `source_detail` · `added_on` · `qualified_on` · `stage_since` · `follow_ups_sent` · `disqualification_reason`

### Dérivés, jamais saisis (2)

`kill_list` et `health` **se calculent**. C'est le stockage manuel qui a laissé le fichier mentir pendant quatre jours. `health` reste **modifiable à la main** pour les cas comme St. Theresa (froide en date, chaude en intention).

### Valeurs à corriger dans votre schéma

- **`source` :** votre énumération ne couvre pas nos vraies sources. Nous recrutons par **annuaire** (DoualaTour), **Google Maps**, **Facebook**, **TikTok**, **PDF du GCE Board**, **portail**. Proposition : `directory · google_maps · facebook · tiktok · gce_board · walk_in · referral · inbound · content_video · outreach_pack · other`.
- **`stage` :** ajouter **`disqualified`**. Sinon 8 leads sont rangés dans `lost` — faux : ils n'ont jamais été perdus, ils n'ont jamais été jouables.

---

## 8 · Arborescence proposée (chemins réels)

```
leads/
  CRM.csv
  records/
    adonai-douala.md · malia-labo-douala.md · oracare-buea.md
    skye-douala.md · yaks-douala.md · afrique-labo-douala.md
    opticien-bali-douala.md · la-bethanie-bonaberi.md · jempo-deido.md
    mitoc-molyko.md · baird-bonduma.md · st-theresa-molyko.md
    ...                                        ← un fichier par lead avec historique
  PIPELINE.md · KILL-LIST.md · STALE.md · SOURCES.md     ← générés
  reports/WEEKLY-SALES-REPORT-2026-09-18.md              ← généré
  Daily-Plan.csv                                        ← renommé + généré depuis le CRM
  archive/
    leads_50.xlsx · Daily Ops.csv · patch1.py … patch4.py
  build/crm.py
  CRM-AUDIT-AND-PROPOSAL-2026-09-18.md
```

**Deux règles de génération, en tête de chaque vue :** *« Généré le … par `leads/build/crm.py` — ne pas modifier à la main. »* Un fichier dérivé modifié à la main redevient une source concurrente, et c'est précisément ce qui a produit l'onglet DAILY OPS.

**`sales/Activity-Log.md` reste intact** et n'est pas remplacé : c'est le journal chronologique append-only. `CRM.csv` dit *où en est* chaque lead ; `Activity-Log.md` dit *ce qui s'est passé et quand*.

---

## 9 · Migration — ce qui change, ce qui est conservé

| Étape | Ce qui change | Ce qui est préservé |
|---|---|---|
| 1. Extraire | 38 lignes du classeur + 16 hors classeur = **54** | Le classeur original, intact, jusqu'à l'archivage |
| 2. Dédoublonner | COMOBIL + GS WAFO → **une fiche, un acheteur** | Les deux lignes d'origine, archivées |
| 3. Signaler | Les **11 contradictions** du §6, valeur retenue + valeur écartée | Le verbatim d'origine dans `Notes` |
| 4. Fiches | **13-15 `records/<slug>.md`** (leads avec historique réel) | Les dossiers `clients/` : **liés, jamais dupliqués** |
| 5. `CRM.csv` | 54 lignes, colonnes du classeur conservées + 16 champs | Les cases vides là où la donnée n'existe pas — **jamais d'invention** |
| 6. Archiver | `leads_50.xlsx`, `Daily Ops.csv`, 4 scripts `patch*.py` → `leads/archive/` | Rien n'est supprimé ; les scripts marqués SUPERSEDED sont la seule trace de plusieurs corrections |
| 7. Générer | `PIPELINE.md` · `KILL-LIST.md` · `STALE.md` · `SOURCES.md` · `Daily-Plan.csv` | `Activity-Log.md`, `Pipeline-Status.md`, tous les `sales/*.md` |
| 8. Résumé | Compte rendu avant signature | — |

---

## 10 · Réponses à vos questions

**« PRR » — c'est bien Prospect Response Rate ?** Oui, votre définition : *leads ayant répondu au moins une fois ÷ leads contactés*. **Je propose de la durcir : réponses humaines uniquement.** Adonaï a envoyé un message automatique 60 secondes après notre message ; le compter fausserait la seule métrique qui dit la vérité sur notre approche. Et je propose un second indicateur, **`ARR`** — non comme une réponse, mais comme **signal d'équipement digital** : une entreprise qui a configuré un accueil automatique **a déjà adopté le digital**. C'est un bon prospect, pas un mauvais.

**Des leads dans l'historique qui ne sont dans aucun fichier ?** **Oui : 16, dont 15 hors classeur** (§1). Le plus notable : **OraCare237 figure dans l'onglet « Pipeline - 5 Stages » mais pas dans la table des leads** — il a donc disparu de la seule liste que nous filtrons.

**3 autres questions :**
1. **COMOBIL** — le playbook le met en kill list, votre décision du 14/09 l'a parqué faute de canal. Laquelle gagne ? *(Le playbook gagne selon vos propres règles — mais je propose de l'amender : COMOBIL remonte comme **incident de canal**, pas comme tâche quotidienne.)*
2. **St. Theresa** — `health` la dirait `cold` (3 jours), alors qu'elle a donné une permission. Confirmez-vous que `health` reste **modifiable à la main** ?
3. **Les 12 labos** du `Remote-Sweep` §C : au CRM comme `prospect` à qualifier, ou en réserve hors CRM jusqu'à vérification du canal ?

---

## Ce que je ferais différemment — en trois phrases

**Un :** `kill_list` et `health` **se calculent**, ils ne se saisissent pas — c'est le stockage manuel qui a laissé le fichier mentir quatre jours. **Deux :** chaque vue générée porte un en-tête *« ne pas modifier à la main »*, sinon elle redeviendra une source concurrente, comme l'onglet DAILY OPS. **Trois :** la discipline d'écriture doit être **mécanique, pas volontaire** — *si un envoi n'est pas écrit dans `Activity-Log.md` et `CRM.csv` dans la même réponse, il n'a pas eu lieu*. C'est la seule règle qui aurait empêché mon erreur de ce matin — et celle sur `Language`, qui est la même erreur.

---

**Rien n'est migré.** Dites oui et je migre d'un bloc, puis je vous présente le résumé avant signature.
