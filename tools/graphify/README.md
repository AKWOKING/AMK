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

## Ce que ça produit, mesuré sur ce dépôt

| | |
|---|---|
| documents structurés | **734** fichiers (dont 920 fichiers non-code vus au scan) |
| nœuds | **10 208** · dont **7 594** titres |
| arêtes | **11 323** (dont 7 627 `contains` et `references`) |
| durée | **~10 s** (code en AST + documents en structure + clustering Louvain local) |

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

## La règle qu'il sert (PRE-FLIGHT §0g)

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

## Fichiers

| Fichier | Rôle |
|---|---|
| `install.sh` | venv jetable + pin 0.9.95 + lien `/usr/local/bin/graphify` |
| `build_docs_graph.py` | passe l'extracteur Markdown sur les 734 documents, fusionne avec le AST de code, clusterise |
| `find.py` | le moteur de `ask.sh` : score par titres touchés (plafonné à 6), nom de fichier, citations reçues ; divise par la racine de la taille du fichier et remonte `knowledge/` et les fichiers de règle |
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

Résultat : `ask.sh "relance rupture"` remonte `MESSAGES-2026-09-23-PERSUASION.md` §4 en tête — la règle
qui interdit la relance sur un message jamais ouvert. C'est exactement le document qu'il fallait.
