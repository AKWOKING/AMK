# AGENTS.md — lire ceci avant tout

Ce dépôt est le bureau d'**AMK** (Douala) : les sites, les contenus et les comptes de nos clients, plus
nos propres outils. Il est lu et écrit par des sessions d'agent qui **ne partagent pas de mémoire**.
Tout ce qui compte doit donc être écrit ici ou dans `ops/`.

---

## 1 · Le rituel de reprise — cinq commandes, dans cet ordre

```bash
cd /home/user/AMK
python3 tools/ops/wake.py          # 0. l'arbre est-il le vrai dépôt ? (répare si besoin) — sans lui, le graphe est faux
bash tools/graphify/preflight.sh "le sujet du tour"   # 0 bis. LE GRAPHE — avant PRE-FLIGHT.md (ruling 141)
bash tools/ops/machine.sh          # 1. où j'en suis : l'étape, ce qui est frais, ce qui ne l'est plus
cat ops/HANDOFF-*.md | tail -60    # 2. où en est le travail, ce qui est décidé, ce qui reste
bash tools/ops/gate-dm.sh          # 3. la porte : état + rendus frais (avant tout contenu DM)
```

**L'étape 0 passe avant tout le reste, y compris avant la lecture de `PRE-FLIGHT.md`** (ruling King
25/10, 141ᵉ message : *« use graphify update or read graph, before you read pre-flight document »*).
Elle rejoue le graphe (~10 s), lit `ops/REPO-MAP.md` dans l'ordre §0 → §6 → §2 → §3 → §1 → §3 bis,
cherche le sujet du tour et **nomme les fichiers à ouvrir**. Sa ligne d'en-tête se colle en tête de
réponse, avant la ligne `PRE-FLIGHT.md read`. Détail et limites de la carte : `PRE-FLIGHT.md` §00 et §0h.

**La machine est dans `ops/MACHINE.md`** : huit étapes, trois boucles, une table « qui tranche quoi ».
Elle ne dit aucune règle métier — elle dit l'ordre, ce qui vérifie, et où ça s'écrit. Une session neuve
n'a ni skills ni venvs : `bash tools/ops/provision.sh` les refait depuis les installateurs épinglés.

**Sans l'étape 1, tout ce que tu lis peut être faux.** Ce n'est pas une précaution théorique : le
22/10/2026, deux affirmations ont été publiées dans la même journée sur la base d'un arbre périmé
(« le catalogue est vide », « la semaine 3 est bloquée faute de photos ») alors que l'inventaire
complet et les 65 images étaient versionnés. Voir `ops/GIT-STABILITY-NOTE.md`, section du 22/10.

---

## 2 · Ce que fait `wake.py`

Dans cet environnement, le dépôt **n'est pas persistant de façon fiable** : à chaque
réapprovisionnement du bac, un **clone neuf** est créé et la branche est replacée sur le commit de
**début de session** — pas sur le dernier commit poussé. `wake.py` compare le local au sommet distant
et le remet dessus ; il sauvegarde d'abord tout travail non commité dans `/tmp/amk-wip-<horodatage>/`.

Conséquences pratiques, non négociables :

| Règle | Pourquoi |
|---|---|
| **Committer et pousser après chaque lot de travail** | un commit local peut disparaître ; un commit poussé, non |
| **Ne jamais citer un chiffre lu sans avoir lancé `wake.py` dans le même tour** | c'est exactement l'erreur du 22/10 |
| **En cas de doute sur un fait du dépôt, lire la version distante** | `git show origin/<branche>:chemin` |

---

## 3 · Les verrous qui ne se discutent pas

Ils viennent du client ou de King, et un outil les vérifie (`tools/qa/audit_claims.py`).

- **Aucun montant publié**, aucune offre, aucun cadeau — les facilités de paiement, oui.
- **Aucun nombre de montures**, nulle part : ni à l'écran, ni en légende, ni dans une description.
- **Aucun visage de patient**, aucune image IA de personne, aucun témoignage inventé.
- **Aucune promesse médicale** (« vous verrez mieux »), aucun symptôme nommé comme diagnostic.
- **Jamais « opticien » seul** : « opticien optométriste » (loi camerounaise 99/001, art. 2).
- Le phrasé du client est une **source**, jamais une légende publiable telle quelle.

---

## 4 · Avant d'écrire un contenu client

Pour **DM Optique**, relire d'abord
`clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md` — direction arrêtée par King le 22/10 :
**A moteur** (on explique), **B preuve** (un geste réel), **C limite** (jamais de diagnostic).
Un contenu qui ne peut pas dire de quel passage du document il vient n'est pas prêt.

Puis la porte en cinq temps : `sales/research/2026-W43-techniques.md` §12b.

---

## 5 · Les portiques, et ce qu'ils ne voient pas

| Outil | Ce qu'il vérifie | Sa limite |
|---|---|---|
| `tools/qa/audit_claims.py <fichier…>` | prix, cardinaux, promesses, superlatifs | il lit le **texte** — pas les images d'une vidéo |
| `tools/qa/audit_render_freshness.py <dossier>` | le MP4 correspond-il à son storyboard (empreinte) | rien pour les montages sans storyboard `.json` |
| `tools/ops/wake.py` | l'arbre est-il le vrai dépôt | — |

**Trois choses qu'aucun outil ne fait ici** : regarder une vidéo, ouvrir un site comme un visiteur,
capturer un écran. Il n'y a ni navigateur ni ffmpeg dans le bac. Ce qui doit être vu se fait relire par
King, sur son téléphone, **avant** publication.

---

## 6 · Où continuer

`ops/MACHINE.md` — l'ordre du travail, les portes, et qui tranche quoi : c'est le câblage de tout le
reste. Puis `ops/HANDOFF-<date>.md` — état, décisions, chantiers ouverts, prochaines actions, questions
en attente. C'est le document à mettre à jour en fin de session, avant tout le reste.
