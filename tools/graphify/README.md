# Graphify — le graphe du dépôt, pour ne plus écrire sans avoir lu

```text
Statut   : installé, testé et branché le 24/10/2026 (ruling King 24/10).
Source   : https://github.com/Graphify-Labs/graphify — PyPI `graphifyy`, Apache-2.0.
Épinglé  : 0.9.95 (commit amont 92741d1, 23/10/2026).
Coût     : 0 € · 0 clé d'API · 0 donnée sortante.
```

## Pourquoi il est là — la décision du 13/10, et pourquoi elle est inversée

Le 13/10, Graphify a été **rejeté** (`sales/Activity-Log.md`, « décision Graphify »), avec trois
déclencheurs de réévaluation. **Deux viennent de se produire le 24/10** :

1. **Deux incidents « fichier introuvable » en une semaine** — `knowledge/OUTREACH-MESSAGING-2026-10-22.md`
   (à lire avant tout message à un prospect, table §0c ligne 3) et `sales/RESEARCH-STANDARD.md` §10
   (qui avait déjà réfuté une statistique que j'ai citée comme valide). Les deux existaient, indexés,
   et je ne les ai pas lus avant d'écrire.
2. **Le dépôt dépasse très largement les 150 fichiers** de la condition de réévaluation.

**La prémisse du rejet était partiellement fausse** et c'est important : « l'outil exigerait un backend
LLM configuré ». Vrai pour l'extraction **sémantique** (des « concepts »), faux pour ce dont on a
besoin — la **structure**. L'extracteur Markdown de Graphify (`extractors/markdown.py`) est du parsing
ligne à ligne : chaque titre devient un nœud, chaque lien entre deux documents devient une arête,
**sans aucune dépendance LLM**. C'est ce que `build_docs_graph.py` exploite.

## Ce que ça produit, mesuré sur ce dépôt (24/10, après le ruling « rien de côté »)

**Deux graphes, un seul point d'entrée.**

| Outil | Ce qu'il indexe | Chiffres |
|---|---|---|
| `build_docs_graph.py` | documents + code (structure et symboles) | 734 documents, 10 208 nœuds, 7 594 titres, 11 323 arêtes |
| **`build_full_graph.py`** | **tout le dépôt** — chaque fichier devient un nœud, quelle que soit son extension | **1 935 fichiers**, **≈12 100 nœuds**, **≈14 400 arêtes**, **≈2 900 citations**, **13 communautés** sur 515 documents reliés |

`build_full_graph.py` écrit aussi **`ops/REPO-MAP.md`** : la carte lisible, qui répond à « qu'est-ce qui
existe, où, et qu'est-ce que personne ne cite ». Durée : **~10 s**, zéro clé, zéro réseau.

## Ce que le graphe complet ajoute au graphe documentaire

| Question | Réponse dans `ops/REPO-MAP.md` |
|---|---|
| Quels documents font loi ? | §1 — les 10 de `knowledge/`, par citations reçues |
| Quel est le squelette réel du dépôt ? | §2 — les 20 documents les plus cités |
| Quelles consignes mortes risquent d'être réappliquées ? | §3 — « périmé » **et** encore cité |
| Qu'est-ce que personne ne cite ? | §3 bis — les orphelins, séparés en « à traiter » / `design/vendor/` / `leads/records/` |
| Quels sont les sujets du dépôt ? | §4 — communautés Louvain, chacune nommée par ses 3 pivots **internes** |
| Où sont les vidéos, leurs scripts, leurs rendus ? | §5 ter — une pièce par dossier, avec son statut |
| Quels outils sont installés, et par quoi on les lance ? | §5 bis — 1 dossier = 1 outil, point d'entrée + contenu réel |
| Je cherche quoi pour écrire sur X ? | §6 — table de routage, 8 sujets × 3 documents |

## Ce qui est indexé — et ce qui ne l'est pas, volontairement

**Un fichier = un nœud, sans exception d'extension** : `.md`, `.py`, `.mjs`, `.sh`, `.html`, `.jpg`,
`.png`, `.webp`, `.mp4`, `.mp3`, `.srt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.ttf`, `.zip`…
Les non-documents portent `kind` (image, vidéo, audio, police, archive, sous-titre…) et sont comptés
au §5. Ils ne sont pas « lus », ils sont **recensés** : le graphe ne prétend pas comprendre une image,
il garantit qu'**aucune ne manque à l'appel**.

Exclus, et pourquoi :
- `ops/REPO-MAP.md` — la carte **se citerait elle-même** : l'indexer ferait boucler le graphe
  (13 communautés un coup, 9 le suivant) ;
- `graphify-out/` — sortie régénérable (930 fichiers d'exports HTML/SVG) ;
- `.git`, `node_modules`, `__pycache__`, `.venv`, `dist`, `build`, `.cache`.

Vérification faite le 24/10 : **1 935 fichiers indexés sur 1 936 sur le disque**, l'unique écart étant
la carte elle-même. Zéro nœud sans `source_file`.

## Les trois commandes

```bash
bash tools/graphify/install.sh                        # venv jetable /tmp/amk-graphify
python3 tools/graphify/build_docs_graph.py            # code + documents → graphify-out/graph.json
bash tools/graphify/ask.sh "message prospect clinique" --top 8
```

Et les commandes natives, pour explorer :

```bash
graphify explain "CLIENT-MESSAGING-RULES.md"
graphify path "LISTE-OPTICIENS-2026-10.md" "OUTREACH-MESSAGING-2026-10-22.md"
graphify query "règles de relance" --budget 1200
graphify god-nodes --top 15
```

## La commande de l'étape 0 — `preflight.sh`

```bash
bash tools/graphify/preflight.sh "le sujet du tour"   # ruling King 25/10 (141ᵉ message)
```

Rejoue le graphe, lit `ops/REPO-MAP.md` dans l'ordre §0 → §6 → §2 → §3 → §1 → §3 bis, cherche le
sujet, nomme les fichiers à ouvrir et **imprime la ligne d'en-tête à coller avant la ligne
`PRE-FLIGHT.md read`**. `--read` lit la carte sans la reconstruire ; `AMK_GRAPH_LINES` raccourcit
l'affichage. Elle s'exécute **avant** la lecture de `PRE-FLIGHT.md`, jamais après.

## La règle qu'il sert (PRE-FLIGHT §00 pour l'ordre, §0h pour le détail)

**Avant d'écrire un document de vente, un message, un script ou une règle** : `ask.sh` sur le sujet.
La sortie liste des fichiers réels avec leurs numéros de ligne. L'en-tête pré-vol **cite ceux qui ont
été lus et ceux qui ne l'ont pas été** — un fichier listé et non lu se dit.

## Ce que l'outil ne fait pas — et qu'on n'essaiera pas de lui faire dire

- **Aucun « concept » extrait sans LLM.** Une arête `contains` dit « ce titre est dans ce fichier »,
  pas « ce paragraphe parle de X ». Le graphe sert à **trouver**, pas à **conclure**.
- **Pas de réponse automatique.** `ask.sh` classe des documents ; la lecture et le jugement restent
  entiers — c'est même tout l'intérêt.
- **Aucune donnée ne sort.** Pas de clé, pas d'appel réseau à l'exécution (l'installation PyPI, oui).
- **`graphify-out/` n'est pas versionné** : 19 Mo d'artefact, reconstruit en 10 s (`.gitignore`).
  **`ops/REPO-MAP.md`, lui, est versionné** : c'est le livrable lisible, pas l'artefact.
- **La détection « périmé » est lexicale**, pas sémantique : les 40 lignes de `REPO-MAP` §3 sont des
  **pistes** à vérifier, pas des preuves. Un document qui *parle* de choses périmées n'est pas périmé.
- **Les non-documents sont recensés, pas compris** : une image est un nœud avec sa taille et son
  dossier ; le graphe prouve qu'elle existe, pas ce qu'elle montre.

## Fichiers

| Fichier | Rôle |
|---|---|
| `install.sh` | venv jetable + pin 0.9.95 + lien `/usr/local/bin/graphify` |
| `build_docs_graph.py` | passe l'extracteur Markdown sur les 734 documents, fusionne avec le AST de code, clusterise |
| **`build_full_graph.py`** | **l'inventaire complet** : 1 fichier = 1 nœud, citations en backticks → arêtes `cites`, `supersedes` lexical, communautés Louvain maison, génération de `ops/REPO-MAP.md`. Options `--no-map`, `--no-cluster` |
| `find.py` | le moteur de `ask.sh` : score par titres touchés (plafonné à 6), nom de fichier, citations reçues (plafonnées à 8) ; divise par la racine de la taille du fichier, remonte `knowledge/` et les fichiers de règle. Ignore un fichier qui ne touche pas le sujet, quelle que soit sa centralité |
| `ask.sh` | le point d'entrée qu'on tape vraiment |

## Le classement, et pourquoi il est fait comme ça

Premier essai : `ask.sh "message prospect clinique"` sortait `sales/Activity-Log.md` en tête — 32 titres
touchés dans un journal de 5 000 lignes, contre 2 dans une règle de 130 lignes. **Le journal gagnait.**
Trois corrections, mesurées sur ce dépôt :

1. **les titres comptés sont plafonnés à 6** — un fichier qui touche 32 titres est un journal, pas une règle ;
2. **le score est divisé par la racine de la taille** (nombre de titres du fichier) ;
3. **`knowledge/` et les fichiers de règle** (`RULES`, `STANDARD`, `PLAYBOOK`, `GUIDE`, `DECLINAISON`,
   `MESSAGES`, `PERSUASION`) reçoivent une remontée — **seulement s'ils ont touché quelque chose**
   (sinon un fichier sans rapport sortait avec un score artificiel de 6).

4. **le degré entrant est plafonné à 8** et ne compte plus que si le fichier touche le sujet —
   `leads/CRM.csv` sortait premier (« cité 143× ») sur *message prospect clinique*, sans un seul mot du sujet.

Résultat, mesuré le 24/10 :

| Requête | Les 3 premiers, dans l'ordre |
|---|---|
| `message prospect clinique` | `MESSAGES-2026-09-23-PERSUASION.md` · `GUIDE-REPONDRE-AVIS` · **`knowledge/OUTREACH-MESSAGING-2026-10-22.md`** |
| `relance rupture` | `MESSAGES-2026-09-23-PERSUASION.md` §4 — la règle qui interdit la relance sur un message jamais ouvert |
| `prix grille remise` | **`knowledge/PRIX-2026-10-24.md`** · `sales/PRIX-ET-RECURRENCE-2026-09-24.md` · `knowledge/ROAST-2026-10-24-PRIX-v2.md` |

Le document du 24/10 — celui qu'on n'avait pas lu — remonte **3ᵉ** sur la requête qui aurait dû le faire
sortir. C'est le test que l'outil doit passer, et c'est celui qu'il passe.
