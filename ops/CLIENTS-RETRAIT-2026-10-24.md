# CLIENTS RETIRÉS — 24/10/2026, ruling King

> King, 24/10 : « we have files/folders in clients who aren't our clients — remove all except
> DM, labiomed and cristallin ».

**Ce qui reste dans `clients/` :** `dm-optic/` (326 fichiers), `le-cristallin/` (2), plus deux
éléments partagés qui ne sont pas des dossiers clients et qui restent :
`_uniqueness-registry.md` (registre d'unicité, cité 13×, il sert au design de DM) et
`_mockups/` (bibliothèque de maquettes lue par `tools/outreach/mockup.py`).

**Labiomed n'a pas de dossier dans `clients/`** — il existe comme aperçu
(`hosting/previews/labiomed/`), fiche de lead (`leads/records/labiomed-deido.md`), maquette
(`clients/_mockups/labs/labiomed.jpg`) et réponse envoyée (`sales/Reply-LABIOMED-2026-09-19.md`).
Rien à retirer, rien à garder de plus : le nom était déjà couvert ailleurs.

## Ce qui a été retiré — 14 dossiers, 83 fichiers, 31,0 Mo

| Dossier | Fichiers | Ce que c'était |
|---|---|---|
| `clients/afrique-labo/` | 2 | AFRIQUE LABO — build notes |
| `clients/cavisa/` | 2 | Cavisa Optique — notes de construction |
| `clients/cinq-sens/` | 4 | CINQ SENS — ce qu'il reste à nous envoyer |
| `clients/douala-cliniques/` | 7 | maquettes seules (7 images) |
| `clients/jempo/` | 4 | JEMPO (Deido · Bessengue, Douala) — build notes + three-door gate |
| `clients/k-vision-care/` | 1 | K VISION CARE — dossier de recherche (24/09/2026) |
| `clients/l-opticien/` | 3 | L'OPTICIEN (Bali, Douala) — build notes + three-door gate |
| `clients/la-bethanie/` | 5 | LA BÉTHANIE (Bonabéri, Douala) — build notes + three-door gate |
| `clients/la-ligne/` | 5 | LA LIGNE OPTIC — ce qu'il reste à nous envoyer |
| `clients/nabesk/` | 2 | NABESK Comprehensive College — Bonduma, Buea |
| `clients/saint-bernard/` | 2 | Saint Bernard High School (SBHS) — Garden Park, Molyko, Buea |
| `clients/summerset/` | 2 | Summerset Bilingual College (SMBICOL) — Wokoko, Buea |
| `clients/uni-labo/` | 3 | UNI-LABO — audit de la page, puis plan d'amélioration |
| `clients/univers-optique/` | 41 | UNIVERS OPTIQUE — WEBSITE : CLOSED · 03/10 · never re-pitch |

Aucun de ces dossiers ne portait de contrat signé, de facture ni d'acompte : ce sont des
dossiers de **prospect** — recherche, maquette, notes de construction. DM Optique est le seul
client payant du dépôt ; `le-cristallin` est conservé par ruling.

## Ce qui reste du travail, et où

Rien n'est perdu :

| Ce qu'on cherche | Où c'est encore |
|---|---|
| le contact, le numéro, l'état de la relation | `leads/records/` — 119 fiches, une par cible, toutes les 14 y figurent |
| ce qui a été envoyé, quand, avec quelle réponse | `sales/` — packs d'envoi, `Activity-Log.md`, `Pipeline-Status.md` |
| la maquette montrée au prospect | `hosting/previews/` et `demos/concept-*.html` — inchangés |
| les fichiers eux-mêmes | l'historique git — `git checkout 10c86b64 -- clients/<nom>/` |

## Les designs — ce qui est parti, et ce qui les remplace (2ᵉ passe)

King, 24/10 : « cut the ones belonging to retired prospects and keep `dmoptic`, `labiomed` and
`cristallin` — I used to keep them because I didn't want to repeat the same design twice, but the
uniqueness register solves that problem. »

| Retiré | Fichiers |
|---|---|
| `hosting/previews/` — 15 dossiers (`afriquelabo`, `bonanjo`, `cavisa`, `cinqsens`, `demo`, `demo-clinique`, `laligne`, `mboacare-demo`, `opticien`, `skye`, `unilabo`, `univers`, `univers-note`, `univers-v1`, `yaks`) | 46 |
| `demos/` — 14 pages `concept-*.html`, 2 `univers-optique-site-v2*`, 2 modules de contenu, 15 builders, 4 modules `_unilabo_v2_*`, 3 gabarits `.tpl.html`, 3 scripts d'école | 43 |
| `demos/img/` — les visuels de ces pages | 37 |
| `demos/shots/` — maquettes et captures d'envoi de ces prospects | 14 |
| `demos/shot-*.png` — captures OraCare / La Retraite / SAHISCOL | 15 |
| **Total** | **155** |

**Conservés :** `hosting/previews/dmoptic/`, `labiomed/`, `cristallin/` ; `demos/build_dmoptic.py`,
`build_dmoptic_montures.py`, `dmoptic-v1.tpl.html`, `pack_dmoptic.py`, `build_le_cristallin.py`,
`le_cristallin_content.json`, `concept-dmoptic-v1.html`, `concept-le-cristallin-v1.html`, les 11
visuels de `demos/img/` que ces builders lisent, et `demos/shots/README.md` (la règle de capture).

**Ce qui remplace les fichiers, pour ne pas refaire deux fois le même design :**
`clients/_uniqueness-registry.md`. Ses 16 lignes concernées portent désormais la mention
« fichier retiré du dépôt (24/10), l'empreinte ci-contre est ce qui reste » — archétype de mise en
page, palette, typographie et ton restent lisibles, et **se lisent avant de construire** au lieu de
se comparer après coup à un HTML.

**Mis à jour en conséquence :** `hosting/previews/README.md` (3 aperçus, gel du Cristallin seul),
`demos/shots/README.md` (règle + format, plus d'index mort), `hosting/build_previews.py` (son
`SLUGS` ne contient plus que `cristallin`), `tools/site/fix_details_summary.py` (la ligne
`bonanjo` retirée), `tools/video/anonymise.py` (sortie par défaut déplacée hors de
`hosting/previews/demo/`, qui n'existe plus).

## Ce que le retrait laisse derrière lui

- **Des références historiques** dans `sales/Activity-Log.md` (28), `leads/build/crm.py` (35,
  uniquement dans des notes en texte), `leads/CRM-AUDIT-AND-PROPOSAL-2026-09-18.md` (8). Elles
  décrivent ce qui a été fait : on ne les réécrit pas, ce serait falsifier le journal.
- **Aucun script ne casse** : les cinq `demos/build_*.py` ne lisaient ces dossiers que dans leurs
  docstrings ; leurs images viennent de `demos/img/`. Vérifié par lecture et par `ast.parse`.
- **Les aperçus et les pages canoniques sont partis aussi** (même ruling, deuxième passe du 24/10,
  voir §« Les designs » ci-dessous). Ce qui reste de ces 15 prospects dans le dépôt : les fiches de
  `leads/records/`, les envois de `sales/`, et leurs empreintes de design dans
  `clients/_uniqueness-registry.md`.
---

*Retrait exécuté le 24/10/2026. Pour en ramener un : `git log --oneline -- clients/<nom>/` puis
`git checkout <commit>^ -- clients/<nom>/`.*
