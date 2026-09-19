# CRM — microtâche M1 terminée : extraire + dédoublonner

**Date :** samedi 19 septembre 2026 · **Livrable :** `leads/CRM.csv` (**54 lignes × 47 colonnes**)
**Script :** `leads/build/crm.py` (relançable à volonté — il reconstruit le CSV depuis la source)
**Périmètre :** M1 seulement. Les fiches `records/`, les vues générées et l'archivage restent M2–M6.

---

## Ce qui a été fait

| Étape | Résultat |
|---|---|
| Extraire | **38** lignes de l'onglet « Leads 50 » + **1** (OraCare237, onglet « Pipeline ») + **15** leads qui n'existaient qu'en prose = **54** |
| Colonnes du classeur | **conservées à l'identique, avec leurs noms** — aucune remplacée |
| Champs ajoutés | **20** (identification, contact, vérité des échanges, site, gestion, dédoublonnage) |
| Dédoublonner | **COMOBIL ↔ GS WAFO** reliés par `same_buyer_as` — **sans supprimer de ligne** |

**Pourquoi un lien au lieu d'une suppression :** l'audit dit à la fois « 54 lignes » et « COMOBIL + GS WAFO → une fiche,
un acheteur ». Les deux ne tiennent ensemble que si la liaison est **un champ**. Une ligne supprimée est une donnée perdue.

## Ce que l'extraction a produit toute seule

- **32 lignes sur 54 ont un mobile exploitable** (`wa_number`), dont **10 déjà vérifiées** sur WhatsApp Business.
- **8 fixes écartés** de `wa_number` : un fixe ne va pas sur WhatsApp — on ne fabrique pas une fausse capacité.
  Le texte d'origine reste **intact** dans la colonne `WhatsApp` du classeur.
- **Étapes dérivées mécaniquement** (`Contacted` → `prospecting` / `qualifying`), vocabulaire de l'onglet
  « Pipeline - 5 Stages » du classeur lui-même + `disqualified` (ajout demandé par l'audit) + `parked`.
  Aucune ligne ne reste sans étape.

## ⚠️ Les deux erreurs que le CRM empêchera désormais

**1 · La liste « ne jamais contacter » n'existait que dans ma mémoire.** Elle est maintenant **dans la donnée** :
- **Solidarity Health Foundation** → `parked`, motif écrit.
- **One Stop Medical Laboratory & Diagnostics (Dr Njang)** → `parked`, motif écrit.
  Celui-là était rangé **comme un prospect normal** dans le classeur. Personne ne l'aurait vu avant l'envoi.

**2 · Les deux numéros écartés à la vérification du 18/09 sont gravés** :
`696 023 696` = « Kingdom Family Int'l » (Finance, pas une école) · `677 647 802` = aucune identité.
`wa_verified = no`, motif dans `disqualification_reason`. **Un numéro dangereux ne peut plus ressortir par accident.**

## Bugs corrigés pendant l'écriture (et pourquoi ils comptent)

Le premier extracteur de numéros a rendu **0 numéro sur 38** — deux fois de suite, pour deux raisons différentes :

1. **Coller deux colonnes avant d'extraire** → les numéros se concaténaient en une suite de 18 chiffres, plus rien ne correspondait.
2. **Ne pas retirer l'indicatif `+237` d'abord** → `+237 233 470 608` matchait à partir du `2` de `237` et rendait
   `237233470` — un numéro qui n'existe pas.

Les deux sont documentés dans la docstring de la fonction. **Un CRM qui rend de faux numéros est pire qu'un CRM vide.**

## Ce qui n'est PAS fait (et qui reste à faire)

| Microtâche | État |
|---|---|
| **M2** — les 11 contradictions du §6 : valeur retenue + valeur écartée, verbatim conservé | à faire |
| **M3** — `records/<slug>.md` pour les 13-15 leads avec un historique réel | à faire |
| **M4** — lier les 8 dossiers `clients/` (dont 5 orphelins) aux lignes | à faire |
| **M5** — compléter les champs des 33 leads en `prospecting` | à faire |
| **M6** — archiver `leads_50.xlsx` + `Daily Ops.csv` + les `patch*.py`, puis générer les vues | à faire |

**Rien n'a été déplacé, archivé ou renommé.** Le classeur est intact, à sa place. `sales/Activity-Log.md` reste
le journal chronologique : le CSV dit *où en est* chaque lead, le journal dit *ce qui s'est passé et quand*.

## Les 5 questions du §10 attendent toujours une réponse de King

1. COMOBIL — kill-list ou parqué ?
2. St. Theresa — `health` forcé à la main (froide en date, chaude en intention) ?
3. Les 12 labos du `Remote-Sweep` §C — réserve ou pipeline ?
4. La Page Facebook AMK — on la crée (25 min, ouvre Messenger et débloque COMOBIL) ?
5. Le parrainage St. Theresa — on le demande maintenant ?
