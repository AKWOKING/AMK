# `clients/` — ce qu'un dossier client est, et ce qu'il n'est pas

**Trois clients, trois dossiers.** Un dossier client se crée quand quelqu'un a **accepté un devis**, pas
avant. Un prospect vit dans `leads/`, une maquette dans `clients/_mockups/` ou `hosting/previews/`.

| Dossier | Nature | Ce qu'il contient |
|---|---|---|
| `dm-optic/` | **client payant** (production `dmoptiquesarl.com`) | brief, marque, site, contenu mois 1–2, photos, facturation |
| `le-cristallin/` | **client, gelé depuis le 23/09** | build notes ; l'aperçu reste `hosting/previews/cristallin/` |
| `labiomed/` | **prospect chaud, en report motivé** | un point d'entrée (`dossier.md`) ; le fil vit dans `leads/records/labiomed-deido.md` |

**Deux éléments partagés, qui ne sont pas des dossiers clients :**

- `_uniqueness-registry.md` — le registre d'unicité : une empreinte de design par projet, pour ne jamais
  répéter une mise en page. Il sert **avant** la première ligne de HTML (`PRE-FLIGHT.md` §2).
- `_mockups/` — la bibliothèque de maquettes, lue par `tools/outreach/mockup.py` et les builders.

**Ce qui a été retiré le 24/10/2026 :** 14 dossiers qui n'étaient pas des clients (83 fichiers,
31,0 Mo). Le registre du retrait, dossier par dossier, est `ops/CLIENTS-RETRAIT-2026-10-24.md` ; les
fichiers restent dans l'historique (`git log --oneline -- clients/<nom>/`).

**La règle qui décide de l'emplacement d'une pièce :** le dossier client porte ce qui est **au client** ;
`leads/` porte l'**état commercial** ; `hosting/previews/` porte ce qui est **déployé** ; `knowledge/`
porte ce qui **fait loi**. Une même pièce ne vit qu'à un seul endroit.
