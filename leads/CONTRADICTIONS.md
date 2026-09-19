# CRM — microtâche M2 : les 11 contradictions, vérifiées une par une

**Date :** samedi 19 septembre 2026 · **Livrable :** ce fichier + 3 champs dans `leads/CRM.csv`
**Règle appliquée :** *valeur retenue + valeur écartée, verbatim conservé*. **Rien n'est supprimé, rien n'est réécrit** —
une contradiction signalée garde toujours les deux versions, pour qu'on puisse revenir sur la décision.

---

## ⚠️ D'abord : trois contradictions de mon propre audit du 18/09 étaient fausses

Je ne les ai pas recopiées — je les ai **vérifiées contre les fichiers**. C'est tout l'intérêt de M2.

| # | Ce que mon audit affirmait | Verdict |
|---|---|---|
| **5** | « COMOBIL : tête de kill list dans DAILY OPS, parké dans Pipeline-Status » | ❌ **FAUX.** L'onglet DAILY OPS écrit noir sur blanc « **COMOBIL / Groupe WAFO (Douala) - PARKED 14 Sep (King decision)** ». Les deux fichiers disent la même chose. |
| **7** | « Ligne St. Theresa décalée : la cellule *Lead score* contient le verbatim de la réponse » | ❌ **FAUX.** La colonne `Lead score` ne contient **que des nombres** — 0 anomalie sur 38 lignes. Le verbatim est dans `Reply`, à sa place. |
| **8** | « `Daily Ops.csv` est un export de l'onglet DAILY OPS — même contenu, deux formats » | ⚠️ **PARTIELLEMENT FAUX.** Le CSV a **50 lignes**, l'onglet **36**. L'en-tête est identique, les contenus **ne se superposent pas**. La **péremption** (16/09) est confirmée, la « duplication » non. |

**Ce que ça m'apprend, et qui est la vraie leçon de M2 :** un audit est une hypothèse, pas un fait.
Mes trois erreurs venaient d'un raisonnement sur la structure des fichiers sans ouvrir les cellules.
**Le contrôle a coûté dix minutes et a évité de figer trois fausses vérités dans le CRM.**

---

## Les 11, vérifiées

### 1 · La kill list du playbook code en dur deux leads dont un est parké — **CONFIRMÉE**
**Fichier :** `sales/AMK-Sales-Playbook-v2.md` §A4 — texte exact : *« The 2 leads at 18 (COMOBIL, OraCare) + any lead
who just said yes → written on a visible "TODAY" list »*.
**Retenu :** une kill list doit **se déduire de l'état réel** (score 18 **et** non parké **et** non disqualifié).
**Écarté :** la liste figée « COMOBIL, OraCare » — COMOBIL est parké depuis le 14/09, il n'a rien à faire sur une liste « TODAY ».
`∅` **Correction appliquée :** une ligne datée sous §A4 renvoie ici.

### 2 · Le classeur maître ne contenait aucun des 15 leads engagés de Douala — **CONFIRMÉE**
**Retenu :** les 15 existent, ils sont engagés, ils comptent. **Écarté :** « le classeur suffit ».
**Réparé par M1 :** les 15 ont maintenant une ligne dans `CRM.csv` (`source = directory · google_maps · facebook`).

### 3 · 5 dossiers `clients/` sur 8 n'avaient aucune ligne — **CONFIRMÉE**
`afrique-labo` · `jempo` · `l-opticien` · `la-bethanie` · `douala-cliniques` (6 maquettes).
**Retenu :** ces dossiers contiennent le travail réel — donc ils doivent être liés.
**Écarté :** l'idée que le classeur décrit le pipeline. **Réparé par M1** (les 4 + les 6 cliniques ont une ligne).
**Reste pour M4 :** créer les fiches `records/<slug>.md` et vérifier que **les 8** dossiers sont liés.

### 4 · L'absence de numéro WhatsApp était écrite en prose, donc intraitable — **CORRIGÉE**
Mon audit disait 27/38 en prose. **Le chiffre exact après extraction :** **32 lignes sur 54 ont un mobile
exploitable**, **41 n'en ont pas** (76 %). Les **8 fixes** sont volontairement exclus de `wa_number`.
**Retenu :** une colonne triable (`wa_number`) **et** le texte d'origine intact dans `WhatsApp`.
**Écarté :** « N/V (landline) » comme contenu de champ.

### 5 · COMOBIL — **INFIRMÉE** (voir plus haut). Aucun conflit : les deux fichiers disent *parké*.

### 6 · Solidarity : « scheduled Tue » au classeur, jamais travaillé — **CONFIRMÉE**
**Retenu :** `parked`. **Écarté :** « scheduled Tue ».
**La raison retenue est plus forte que celle de mon audit :** ce n'est pas seulement une question de ligne manquante —
**King a une règle : ne jamais contacter Solidarity.** Elle est maintenant **dans la donnée**, pas dans une mémoire.
*Note :* `Pipeline-Status` donne un motif différent (« no WhatsApp line »). Les deux mènent au même état, et le motif de King prime.

### 7 · St. Theresa — **INFIRMÉE** (voir plus haut). La ligne est correcte.

### 8 · `Daily Ops.csv` périmé au 16/09 — **CONFIRMÉE sur la péremption**, infirmed sur la duplication.
**Retenu :** le fichier est un **plan de journée du 16/09**, pas une liste de leads (12 lignes sur 43 sont de la donnée de lead).
**Écarté :** « c'est la même chose que l'onglet ». **À faire en M6 :** le renommer `Daily-Plan.csv` **et le générer depuis le CRM**.

### 9 · Trois vocabulaires d'étape, et deux comptes différents du pipeline — **CONFIRMÉE**
`Pipeline-Status` dit **« Pipeline at a glance (27 leads) »** ; le classeur en a **38** ; le CRM en a **54**.
**Retenu :** le vocabulaire de l'onglet **« Pipeline - 5 Stages »** du classeur lui-même + `disqualified` + `parked` (7 valeurs).
**Écarté :** les trois autres vocabulaires. **Réparé par M1** : chaque ligne a une étape de l'énumération, aucune hors énumération.

### 10 · NABESK : « 83,5 % au O-Level » — **CONFIRMÉE**
**Retenu :** **83,46 % au A-Level 2020** (correction déjà journalisée dans `Pipeline-Status`).
**Écarté :** « 83,5 % au O-Level 2020 » — un chiffre faux **dans une accroche commerciale**, donc le pire endroit pour se tromper.
**Verbatim conservé dans `Notes`** (la colonne `Facilities` du classeur n'est pas modifiée).

### 11 · GS WAFO fusionné dans COMOBIL mais ligne séparée — **CONFIRMÉE**
**Retenu :** **deux lignes liées** (`same_buyer_as`), pas une fusion. **Écarté :** supprimer une des deux.
Raison : une ligne supprimée est une donnée perdue, et l'audit lui-même disait les deux choses à la fois (« 54 lignes » **et** « une fiche »).

---

## Bilan pour King

**6 confirmées · 3 fausses à mon sujet · 1 corrigée · 1 confirmée-mais-déjà-réparée.**

Les deux qui comptaient le plus :
1. **La kill list du playbook est fausse** — elle met sur une liste « TODAY » un lead parké depuis cinq jours. Corrigé.
2. **Les deux règles « ne jamais contacter » (Solidarity, Dr Njang) ne vivaient que dans des conversations.** Elles sont maintenant dans les données.

**Ce qui reste pour M3–M6 :** les fiches `records/`, la liaison des 8 dossiers, le remplissage des 33 lignes en `prospecting`,
l'archivage — puis la génération des vues (`PIPELINE.md`, `KILL-LIST.md`, `STALE.md`, `SOURCES.md`, `Daily-Plan.csv`).
**Une microtâche à la fois.**

## Les 5 questions du §10 attendent toujours une réponse de King
COMOBIL (kill-list ou parqué) · St. Theresa (`health` forcé à la main) · les 12 labos de la réserve · la Page Facebook ·
le parrainage St. Theresa.
