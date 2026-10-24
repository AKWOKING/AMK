# LA MACHINE — un tour, un engagement, un actif : ce qui intervient, quand, comment, pourquoi

> Créé le 24/10/2026 (ruling King : *« everything … should work like a single machine »*).
> Ce document ne dit **aucune règle métier**. Il dit **l'ordre**, **qui tranche quoi**, **ce qui vérifie**,
> et **où ça s'écrit**. Quand il contredit `PRE-FLIGHT.md` ou un document de `knowledge/`, c'est le
> document qui gagne : la machine est le câblage, pas la loi.

## 0 · Trois commandes, et vous savez où vous êtes

```bash
bash tools/ops/machine.sh              # le cockpit : l'étape, ce qui est frais, ce qui ne l'est plus
bash tools/ops/machine.sh 2            # la fiche de l'étape 2 (lecture) : quoi lire, quoi lancer, quand c'est fini
bash tools/ops/machine.sh --who prix   # qui tranche le sujet « prix », et ce qui le vérifie
bash tools/ops/machine.sh --merge      # la jauge de fusion : combien de fichiers/lignes depuis main
bash tools/ops/machine.sh --rules      # les 15 règles debout, chacune avec sa porte (§9)
bash tools/ops/provision.sh            # le noyau de travail : 4 outils (les 24 : --all)
bash tools/ops/provision.sh --list     # les 24 outils : installés cette session, ou pas
bash tools/ops/install-hooks.sh        # pose le crochet pre-push : un push rouge ne part plus
python3 tools/ops/machine.py --ci      # ce que le crochet joue, et ce que la CI jouera
bash tools/ops/machine.sh --turns      # le rendement du jour : commits, fichiers, lignes, refus
```

Le miroir Notion (PRE-FLIGHT §0g) est **daté ici**, dans une ligne que la machine lit :

```text
MIRROR 2026-10-24 · fc235b9
```

Tant qu'un fichier de **fait debout** (pré-vol, machine, prix, dossiers clients, journal des ventes)
change après ce commit, la porte `miroir-notion` reste fermée et `--check` échoue. On met Notion à jour,
puis on re-date la ligne.

Une session neuve n'a **ni skills, ni venvs, ni clones** : `bash tools/ops/provision.sh` refait le
**noyau de travail** — `graphify`, `superpowers`, `photo`, `video` — depuis les installateurs épinglés
du dépôt. C'est l'étape 0 de la machine, pas une option. Depuis l'étude du 24/10, les vingt autres
outils ne sont plus installés par défaut : `--only <nom>` quand une tâche les demande, `--all` pour
retrouver l'ancien comportement (`ops/TOOL-SCAN.md` § 24/10).

---

## 1 · Le schéma

```text
                    ┌──────────────────────────────────────────────┐
   BOUCLE 1         │ LE TOUR (minutes → une session)              │
   (aujourd'hui)    │ 0 réveil → 1 cadrage → 2 lecture → 3 plan    │
                    │ → 4 exécution → 5 preuve → 6 mémoire → 7 sortie │
                    └───────────────┬──────────────────────────────┘
                                    │ chaque livrable alimente
                    ┌───────────────▼──────────────────────────────┐
   BOUCLE 2         │ L'ENGAGEMENT (semaines → un client)          │
   (par client)     │ Intake → Strategy → Production → Review      │
                    │ → Delivery            (ops/LIFECYCLE.md)     │
                    └───────────────┬──────────────────────────────┘
                                    │ chaque règle et chaque outil
                    ┌───────────────▼──────────────────────────────┐
   BOUCLE 3         │ L'ACTIF (mois → un doc, un outil, une règle) │
   (ce qui reste)   │ entre par un ruling · vit avec un pin et une │
                    │ date · sort avec une note datée              │
                    └──────────────────────────────────────────────┘
```

Les trois boucles tournent sur **le même dépôt** et **les mêmes portes**. Ce qui change est l'horizon :
le tour décide d'un fichier, l'engagement décide d'un client, l'actif décide de ce qui sera encore vrai
dans trois mois.

---

## 2 · Boucle 1 — le tour, en huit étapes

Chaque étape a **une question**, **une sortie vérifiable** et **un incident qui l'a créée**. Un tour qui
saute une étape ne plante pas tout de suite : il plante trois tours plus tard, quand plus personne ne
sait pourquoi le chiffre était faux.

| # | Étape | La question | La sortie qui prouve que l'étape est faite | Ce qui intervient |
|---|---|---|---|---|
| 0 | **Réveil** | *L'arbre que je lis est-il le vrai dépôt ?* | `wake.py --check` passe (code 0) | `tools/ops/wake.py` · `ops/GIT-STABILITY-NOTE.md` |
| 1 | **Cadrage** | *Que demande King, et qu'est-ce qui est déjà tranché ?* | la demande en une phrase + les rulings cités **par chemin** | `PRE-FLIGHT.md` §0–§5 · `knowledge/` couche 2 · skill `brainstorming` si la demande est ouverte |
| 2 | **Lecture** | *Quelle règle gouvernait déjà ce sujet ?* | la liste des fichiers **lus** et **listés non lus**, en tête de réponse | `ops/REPO-MAP.md` §0 §6 §2 §1 §3 bis · `tools/graphify/ask.sh` |
| 3 | **Plan** | *Quels fichiers, dans quel ordre, et à quoi je verrai que c'est fini ?* | 3 à 8 lignes, chaque ligne avec sa porte | skills `writing-plans` / `executing-plans` · `PRE-FLIGHT.md` §0d · `ops/templates/` |
| 4 | **Exécution** | *Quel outil fait ce travail — et est-il installé, épinglé, jugé ?* | la commande lancée + son code retour | `provision.sh` · `tools/<domaine>/` · `ops/TOOL-SCAN.md` |
| 5 | **Preuve** | *Qu'est-ce qui prouve que c'est fait ?* | la sortie de la porte, recopiée dans la réponse | `gate-dm.sh` · `gate-amk.sh` · `tools/qa/*` · skill `verification-before-completion` |
| 6 | **Mémoire** | *Où est-ce écrit pour la session qui ne se souvient de rien ?* | 1 à 3 lignes datées dans le bon fichier | `sales/Activity-Log.md` · `ops/TOOL-SCAN.md` · `clients/_uniqueness-registry.md` · `ops/HANDOFF-*` · Notion (miroir) |
| 7 | **Sortie** | *Est-ce poussé — et est-ce que la branche doit être fusionnée ?* | `git push` fait, branche à jour, **jauge de fusion lue** | `git` · `PRE-FLIGHT.md` §1i (jalon · 3 000 lignes · 40 fichiers · 6 tours) · `bash tools/ops/machine.sh --merge` · `wake.py --check` |

### Pourquoi ces huit-là, et pas d'autres

| Étape | L'incident qui l'a rendue obligatoire | Date |
|---|---|---|
| 0 Réveil | Quatre fois dans la même journée, le travail local a disparu et deux affirmations fausses ont été publiées (« le catalogue est vide », « la semaine 3 est bloquée ») — l'arbre lu n'était pas le dépôt | 22/10 |
| 1 Cadrage | Un ruling de King appliqué à moitié, faute d'avoir relu ce qui était déjà tranché | continu |
| 2 Lecture | Messages d'approche entièrement réécrits sans `OUTREACH-MESSAGING` ni `RESEARCH-STANDARD` §10 — deux règles existaient, aucune n'a été lue | 24/10 |
| 3 Plan | Une refonte partie d'un seul fichier et qui en a touché douze sans que personne ne l'ait décidé | 13/10 |
| 4 Exécution | Un outil exécuté sans jugement préalable, et un autre jamais réutilisé alors qu'il était installé | 19/10 |
| 5 Preuve | Une vidéo publiée avec une ouverture figée : le portique existait, il n'a pas été lancé | 17/09 |
| 6 Mémoire | Un résumé annonçant « OraCare et MITOC ont répondu » alors que c'était faux : la mémoire avait remplacé le journal | 18/09 |
| 7 Sortie | Un lot de travail fini, jamais poussé, effacé au réapprovisionnement suivant | 22/10 |

---

## 3 · Boucle 2 — l'engagement, et ce que la machine y ajoute

`ops/LIFECYCLE.md` nomme les cinq phases et ne change pas. La machine ajoute **ce que chaque phase
produit** et **la porte qui la ferme** — sans quoi « on est en Production » est une déclaration.

| Phase (`LIFECYCLE`) | Le fichier qui la ferme | La porte | Ce que la machine exige en plus |
|---|---|---|---|
| **1 Intake** | accord + calendrier écrits | `sales/RESEARCH-STANDARD.md` §8b (trois portes) | étape 2 du tour : la règle existante est lue **avant** le premier message |
| **2 Strategy** | angle daté + ligne au registre d'unicité | `clients/_uniqueness-registry.md` | un angle sans empreinte n'entre pas en Production |
| **3 Production** | le livrable + son gabarit (`ops/templates/`) | `gate-dm.sh` (rendus frais) | étape 4 : aucun outil non jugé dans `TOOL-SCAN` |
| **4 Review** | retour client dans un seul fil | relecture interne **avant** l'envoi | étape 5 : on cite ce qui a été vérifié, pas ce qu'on croit |
| **5 Delivery** | site/vidéo en ligne + plan de soin | `gate-amk.sh` / `gate-dm.sh` · `audit_delivery.py --strict` · `PROTOCOLE-LECTEUR-ECRAN.md` | étape 6 : le journal et le handoff sont écrits le jour même |

**La règle de passage** : une phase qui ne s'applique pas s'écrit dans le dossier client. On ne la saute
pas en silence (`LIFECYCLE`, dernière ligne).

---

## 4 · Boucle 3 — l'actif : comment un outil, un doc ou une règle entre, vit et sort

C'est la boucle qui manquait, et c'est celle qui fait la différence entre un dépôt qui grossit et un
dépôt qui reste utilisable.

| Moment | Ce qu'on fait | Ce qui le prouve | Exemple récent |
|---|---|---|---|
| **Entrée** | fiche `ops/TOOL-SCAN.md` en six points : (a) problème, (b) cas d'usage AMK nommé, (c) coût, (d) effort + verdict, (e) ce qui n'est pas installé, (f) limite dite | le verdict est écrit, pas sous-entendu | `superpowers`, 24/10 — verdict *pursue*, hooks non activés, raison écrite |
| **Vie** | installateur épinglé sous `tools/<nom>/install.sh` + estampes `provision.sh` + nœud dans `ops/REPO-MAP.md` | `provision.sh --list` dit « installé », le graphe le nomme | 24 outils épinglés, 1 installateur par outil |
| **Sortie** | retrait **daté**, note dans `ops/`, documents qui le citaient mis à jour, empreinte gardée si c'était un design | la note existe et `grep` ne trouve plus d'appel vivant | `clients/` (15 dossiers, 155 fichiers) et `tools/video/anonymise.py`, 24/10 |

**Un skill s'appelle, il ne se cite pas** : `bash tools/superpowers/use.sh <skill>` affiche le skill et
laisse une trace datée. Sans cette ligne, « je m'en suis servi » est exactement le genre d'affirmation que
la machine a été construite pour ne pas croire.

**La loi de l'actif** : un actif sans date est un actif qu'on ne saura pas périmer. Un document mort qui
reste cité est plus dangereux qu'un document absent — il a l'air vivant.

---

## 5 · Qui tranche quoi — la table de propriété

**Un sujet = un document souverain.** Deux documents qui tranchent le même sujet = un conflit à résoudre
le jour même, pas au tour suivant. Cette table ne dit *quoi* lire pour une tâche (c'est
`PRE-FLIGHT.md` §1, la table de routage) : elle dit **qui a le dernier mot**, **ce qui le vérifie** et
**quand il intervient**.

| Sujet | Qui tranche | Ce qu'il ne tranche pas | Ce qui le vérifie (code) | Quand il intervient |
|---|---|---|---|---|
| Le message à froid, la relance | `knowledge/OUTREACH-MESSAGING-2026-10-22.md` | la liste des cibles (`leads/`) | `tools/qa/audit_claims.py` | avant tout envoi |
| Le chiffre, la source, le tier | `sales/RESEARCH-STANDARD.md` §10 | la formulation | — (lecture seule : aucun outil ne juge une source) | avant toute statistique citée |
| Le prix, l'offre, la récurrence | `knowledge/PRIX-2026-10-24.md` + `ROAST-2026-10-24-PRIX-v2.md` | la remise (interdite) | — | avant toute conversation d'argent |
| La marque et le contenu DM | `clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md` | le site AMK | `gate-dm.sh` | avant d'écrire une ligne DM |
| L'unicité d'un design | `clients/_uniqueness-registry.md` + `PRE-FLIGHT.md` §2 | le goût de King | — (le registre est la mémoire, pas la preuve) | avant la première ligne de HTML |
| Les verrous client (claims) | `AGENTS.md` §3 | — | `tools/qa/audit_claims.py` | avant publication |
| Le SEO d'un site | `AMK-SEO-PLAYBOOK.md` + `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` | le contenu éditorial | `audit_seo.py`, `audit_aeo.py` | avant déploiement |
| La vidéo, le montage, la publication | `knowledge/VIDEOS-2026-10-23-AUDIT.md` + `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` | le rendu final (King le voit sur son téléphone) | `audit_video_motion.py`, `audit_render_freshness.py` | avant toute publication |
| La cadence de publication | `ops/CADENCE-PUBLICATION-2026-10-22.md` | le calendrier client | — | chaque lundi |
| Les cinq phases d'un engagement | `ops/LIFECYCLE.md` | le prix, l'angle, le design | `gate-dm.sh` / `gate-amk.sh` | à chaque phase |
| Les outils et les skills | `ops/TOOL-SCAN.md` | le code de l'outil (on ne le modifie pas) | `tools/ops/provision.sh --list` | avant d'installer, et à chaque session |
| La carte du dépôt | `ops/REPO-MAP.md` (**généré**, jamais édité) | la vérité des règles | `tools/graphify/build_full_graph.py` | avant d'écrire, et après tout fichier créé |
| La mémoire des envois | `sales/Activity-Log.md` (append-only) | les intentions | `leads/build/guard.py` | à chaque envoi, chaque réponse |
| L'état du travail | `ops/HANDOFF-<date>.md` (le plus récent) | — | `wake.py` | fin de session |
| Git, branches, fusion | `PRE-FLIGHT.md` §1i + `ops/GIT-STABILITY-NOTE.md` | — | `wake.py --check` | à chaque fusion |
| La facturation, l'admin fiscal | `ops/FACTURATION-2026-10-24.md` + `ops/ADMIN-FISCAL-AMK-2026-10-22.md` | le prix | `tools/ops/make_contrat.py`, `make_recap_dm.py` | avant tout document financier |
| La méthode de travail (comment) | `tools/superpowers/` (15 skills, `using-superpowers` en tête) | nos règles métier | — | quand la demande est ouverte ou le travail long |
| Le miroir lisible (téléphone) | `PRE-FLIGHT.md` §0g — **le dépôt fait loi, Notion est corrigé** | le dépôt | — | quand un fait debout change |

---

## 6 · Les portes — ce que le code vérifie, et ce qu'il ne verra jamais

Une porte est un **code retour**, pas une impression. Si elle n'a pas été lancée, l'étape 5 n'a pas eu lieu.

| Porte | Commande | Ce qu'elle attrape | Ce qu'elle ne voit pas |
|---|---|---|---|
| Arbre vrai | `python3 tools/ops/wake.py --check` | local périmé, travail non poussé | rien au-delà de git |
| DM | `bash tools/ops/gate-dm.sh [fichier]` | rendus périmés, prix, cardinaux, promesses, livraison | une image, une vidéo, un ton |
| AMK | `bash tools/ops/gate-amk.sh` | tunnel des pages de vente, livraison des 97 pages | le contenu des pages |
| Claims | `tools/qa/audit_claims.py <fichier>` | montants, nombres de montures, superlatifs | le sens de la phrase |
| Fraîcheur | `tools/qa/audit_render_freshness.py <dossier>` | MP4 plus vieux que son storyboard | les montages sans storyboard |
| Livraison | `tools/qa/audit_delivery.py --strict <dossier>` | nav mobile, cache, icônes, partage, schéma, en-têtes | l'expérience réelle |
| Accessibilité | `tools/qa/audit_a11y.py <page>` | WCAG 2.2 AA, critère par critère | quatre choses écrites dans `AMK-DESIGN-SKILLS.md` §27 |
| Dépôt | `python3 tools/ops/audit_files.py` | doublons, orphelins, fichiers périmés, caches | la qualité d'un document |
| Provision | `bash tools/ops/provision.sh --list` | outil absent de la session | la version réellement utilisée |
| **Règles** | `bash tools/ops/machine.sh --rules` | les portes dures du registre §9, et toute règle du code qui manquerait au tableau | les règles souples et le trou, dits en clair |
| **Crochet** | `bash tools/ops/install-hooks.sh` (une fois par clone) → `.git/hooks/pre-push` | un push avec un secret ou un chemin mort | la carte rejouée (trop lent pour un crochet) |
| **CI GitHub** | `.github/workflows/machine.yml` — à chaque push et PR | secret, chemin mort, carte non reproductible | la valeur du travail, et tout ce qui demande un jugement |
| **Sources** | `python3 tools/qa/audit_claims.py --sources .` | un pourcentage affirmé sans appui dans **tout le dépôt** (765 documents), sur une fenêtre de 3 lignes avant et 3 après | la qualité de la source ; un chiffre copié d'une étude ancienne reste « sourcé » |
| **Rendement** | `bash tools/ops/machine.sh --turns` | le volume du jour (commits, fichiers, lignes) et le nombre de refus | la valeur du travail : un gros commit peut être du déchet |
| **Usage** | `bash tools/ops/machine.sh --usage` | un outil provisionné qu'aucune trace ne montre appelé | ce qui ne laisse aucune trace : scripts QA lancés à la main, skills lus, recherche web |

**La trace d'usage, et pourquoi elle existe.** Un outil « installé » n'est pas un outil « utilisé » : le
24/10, la panne notée en §8 disait *24 installateurs, 3 outils appelés*. `--usage` lit un journal hors
dépôt (`~/.amk-provisioned/usage.log`) que les outils écrivent eux-mêmes — `machine`, `provision`,
`graphify`, `ask` — et **oppose une trace à chaque phrase « j'ai utilisé l'outil »**. Il ne voit que ce
qui laisse une trace : un script QA lancé à la main, un skill lu, une recherche web n'y figurent pas, donc
ils ne sont jamais comptés à la place de King. Sa sortie la plus utile est la ligne *« muets alors qu'une trace était possible »* : un outil
installé que rien n'appelle est un candidat à sortir (invariant 6), pas un acquis. Depuis le
24/10, le compteur sépare deux silences qui n'ont rien à voir : **muet mesurable** (un CLI qui
pouvait tracer) et **sans trace possible** (15 skills en markdown, que cet agent ne charge pas —
leur silence ne dit rien de leur utilité). L'étude qui les juge, outil par outil et sur une tâche
nommée, est dans `ops/TOOL-SCAN.md` (§ 24/10/2026).

**Une seule copie du workflow.** Il vit dans `.github/workflows/machine.yml` et nulle part ailleurs :
la version « à copier par King » a été supprimée le 24/10 dès que la vraie a existé. Deux copies d'une
même porte finissent toujours par diverger, et c'est la plus vieille qui gagne.

**Ce qu'aucune porte ne fait ici** : regarder une vidéo, ouvrir un site comme un visiteur, capturer un
écran. Ce qui doit être vu se fait relire par King, **avant** publication (`AGENTS.md` §5).

---

## 7 · Les sept invariants

1. **Un seul arbre vrai.** Tout ce qui est lu ou mesuré vient d'un dépôt remis au sommet distant dans le même tour.
2. **Une seule vérité par sujet.** La table §5 est exhaustive : un sujet sans souverain est un sujet qui va se contredire.
3. **Rien n'est « fait » sans sortie de commande.** Une affirmation sans code retour est une intention.
4. **Tout ce qui compte est dans le dépôt.** Ni en mémoire, ni seulement dans Notion, ni dans une conversation.
5. **Chaque actif a une date et un propriétaire.** Un doc sans date ne se périme pas ; il pourrit.
6. **Un outil entre par un ruling, reste par un pin, sort par une note datée.** Jamais par oubli.
7. **Le tour finit poussé.** Un commit local n'existe pas pour la session suivante.
8. **La branche se fusionne sur seuil, pas sur humeur.** Jalon, ou 3 000 lignes, ou 40 fichiers, ou 6 tours
   (`PRE-FLIGHT.md` §1i). Le seuil n'est pas une mémoire : `bash tools/ops/machine.sh` l'affiche, et
   `--check` échoue tant qu'il est dépassé. Trou constaté le 24/10 : **22 commits, 544 fichiers, 59 722
   lignes** sur la même branche sans fusion — la règle existait, rien ne la rappelait.

---

## 8 · Les pannes connues, et leur parade

| Panne | Signe | Parade |
|---|---|---|
| Arbre périmé | deux chiffres qui se contredisent dans la même réponse | étape 0, toujours, même pour « juste lire » |
| Mémoire qui remplace le journal | « ils ont répondu » sans ligne dans `Activity-Log` | étape 6 avant toute affirmation sur un prospect |
| Règle recréée de zéro | un document neuf qui dit ce qu'un ancien disait déjà | étape 2 : `ask.sh` + `REPO-MAP` §3 bis |
| Outil installé, jamais utilisé | 24 installateurs, 3 outils appelés | `machine.sh --usage` : trace datée par outil ; les muets sont nommés |
| Carte qui se cite elle-même | le graphe change à chaque reconstruction sans qu'un fichier bouge | `REPO-MAP.md` est exclu de son propre index |
| Session neuve sans skills | l'agent « ne trouve pas » un skill installé la veille | `provision.sh`, au début de chaque session |
| Handoff qui vieillit | un état de travail de trois jours présenté comme actuel | le cockpit affiche son âge ; au-delà de 3 jours, il est réécrit |
| Branche qui ne fusionne jamais | 22 commits et 59 722 lignes sur la même branche, `main` figé depuis trois jours | la jauge de fusion du cockpit, et `machine.sh --merge` pour la séquence `fetch` → diff → PR |

---

---

## 9 · Les règles et leurs portes — le registre

> Ruling King, 24/10 : *« il faut mettre en place des règles pour que tu n'oublies plus »*. Une règle
> écrite dans un document et rappelée par la mémoire de l'agent **ne tient pas** : elle se perd au
> troisième tour. Ici, chaque règle porte **le document qui la fonde**, **ce qui la déclenche** et **la
> commande qui la vérifie**. `bash tools/ops/machine.sh --rules` les imprime toutes ; `--check` échoue
> dès qu'une porte dure est fermée.

| # | id | Règle | Fondement | Déclencheur | Porte |
|---|---|---|---|---|---|
| 1 | `arbre-propre` | Rien ne reste hors commit quand le tour se dit fini | PRE-FLIGHT §1e | fin de tour | `git status --porcelain` vide |
| 2 | `tour-pousse` | Le tour finit poussé ; une branche sans remote n'est pas un travail rendu | §7 invariant 7 | fin de tour | `rev-list @{u}..HEAD` = 0 |
| 3 | `fusion-sur-seuil` | La branche se fusionne sur seuil, pas sur humeur | PRE-FLIGHT §1i | chaque sortie | `machine.sh --merge` — 40 fichiers / 3 000 lignes / 6 tours |
| 4 | `carte-fraiche` | La carte du dépôt est reconstruite quand un fichier suivi bouge | PRE-FLIGHT §0h | fichier modifié | `REPO-MAP.md` plus récent que toute source (le cockpit exempté, voir plus bas) |
| 5 | `outils-provisionnes` | Une session neuve rejoue le noyau épinglé avant de travailler | PRE-FLIGHT §1f | début de session | estampes `~/.amk-provisioned` (graphify, superpowers) |
| 6 | `miroir-notion` | Le miroir Notion suit le jour même tout changement d'un fait debout | PRE-FLIGHT §0g | commit sur un fait debout | `git diff MIRROR..HEAD` sur les chemins de §0g |
| 7 | `aucun-secret` | Ni mot de passe, ni clé, ni jeton dans un dépôt public | PRE-FLIGHT §0g | avant chaque push | `git grep` des motifs de secret (code tiers exclu) |
| 8 | `docs-existants` | Tout chemin cité par les tableaux de la machine existe encore | MACHINE §5 · §6 · §9 | chaque modification de la carte | chaque chemin cité résolu sur le disque |
| 9 | `audit-frais` | Le comptage des fichiers a moins de sept jours | `ops/FILE-AUDIT-*.md` | chaque semaine | âge de l'audit — ⚠ souple |
| 10 | `handoff-frais` | L'état de reprise a moins de trois jours | `ops/HANDOFF-*.md` | tous les trois jours | âge du dernier handoff — ⚠ souple |
| 11 | `document-neuf` | Tout `.md` neuf à la racine ou dans `ops/` se déclare avant de devenir loi | PRE-FLIGHT §4b | apparition d'un doc souverain | `git diff --diff-filter=A` — ⚠ souple |
| 12 | `stat-sourcee` | Aucune statistique sans source primaire nommée | PRE-FLIGHT §1g | chaque chiffre écrit | `audit_claims.py --sources .` — tout le dépôt, ⚠ souple (porte faible), visible à chaque `--check` |
| 13 | `registre-complet` | Aucune règle du code ne peut disparaître de ce tableau sans faire échouer la porte | ce § | chaque `--check` | chaque id connu de `machine.py` présent ci-dessus |
| 14 | `poids-raisonnable` | Le poids suivi reste sous 160 Mo et aucun fichier ne dépasse 15 Mo sans décision | règle du 23/09 « le dépôt n'est pas un disque dur » | chaque commit | `git ls-files` pesé — ⚠ souple |
| 15 | `fichier-neuf-avec-king` | Un fichier debout nouveau n'existe qu'avec le oui de King | PRE-FLIGHT §4b | création d'un document souverain | ○ **sans porte machine** |

**Pourquoi la 13 existe.** Le 24/10 au soir, ce tableau listait douze règles quand le code en appliquait
treize : `docs-existants` avait été ajoutée dans `machine.py` et **pas ici**. Une règle écrite à un seul
endroit est une règle à moitié tenue — l'agent lit le code, King lit le tableau, et les deux ne parlent
pas du même dépôt. La porte 13 compare les deux listes et échoue à la première divergence.

**Pourquoi le cockpit est exempté de la porte 4.** `ops/MACHINE.md` porte la ligne `MIRROR`, réécrite à la
fin de chaque tour, après la reconstruction de la carte. La compter rendrait la porte rouge **par
construction**, à chaque tour. Une porte toujours rouge n'est pas une règle : c'est du bruit qu'on apprend
à ignorer. Le cockpit reste un nœud de la carte ; seuls ses changements ne la déclenchent pas.

**Une porte faible, et un trou qui reste.** La règle 12 (`stat-sourcee`) n'a pas de porte *forte* : aucun script ne sait
si une source est bonne. Elle a une porte **faible**, et c'est déjà autre chose que rien :
`audit_claims.py --sources` liste les lignes qui affirment un pourcentage **sans lien, sans chemin, sans
« selon », sans « non revérifié », sans calcul, sans « invérifiable »**. Sa précision est choisie : elle
lisait `knowledge/` le matin du 24/10 (7 lignes sur 126 documents), elle lit **tout le dépôt** le soir
(765 documents) et ramène **0 ligne**. Quatre lignes sont tombées au passage, pas 185 : un 53 % recopié
d'un blog sans lien, un 90 % de commerces sans étude, un 14,7 % qui était un calcul (10 ÷ 68, désormais
dit comme tel), un 20–30 % qui était un objectif stratégique et non une mesure. Sa fenêtre de lecture est
de **3 lignes avant, 3 après** : une source posée sous son chiffre compte autant qu'au-dessus.
Elle est **souple** : elle signale, elle ne bloque pas, parce qu'un script ne doit jamais arrêter une
publication sur une intuition — mais `--check` l'affiche désormais à chaque tour, parce qu'une alerte
qu'on ne voit jamais est une règle morte en trois tours.

La règle 15 (`fichier-neuf-avec-king` — **un fichier debout neuf exige le oui de King**) reste sans porte : personne ne peut
vérifier un accord qui n'a pas laissé de trace. Son substitut est **la forme de la réponse** — le fichier
est *proposé* avec son emplacement avant d'être committé. Si un jour l'une des deux devient vérifiable,
elle monte en porte dure ; c'est le seul sens de circulation autorisé.

**Ce que le registre interdit** : ajouter une règle ici sans lui donner de porte, ou de sévérité
explicite. Une règle sans porte est un trou ; un trou caché est une panne.

---

## 10 · Ce qui manque encore, dit franchement

- **L'intégration continue est en place depuis le 24/10** : `.github/workflows/machine.yml` (posé par
  King — la GitHub App de l'atelier n'a pas la permission `workflows`, donc **toute évolution de ce
  fichier passe par lui**) lance `machine.py --ci` puis reconstruit la carte et échoue si elle change.
  Trois rouges de suite le jour de sa mise en route, trois causes réelles : la carte lisait le disque au
  lieu du dépôt, puis l'historique git au lieu de l'arbre, puis elle accusait un fichier périmé quand il
  manquait seulement une dépendance (`graphify`, désormais installée épinglée par le script lui-même).
  C'est exactement ce qu'on attendait d'elle : elle a trouvé trois choses que la relecture n'avait pas vues.
- **Le crochet local reste** (`install-hooks.sh`) : il attrape un secret ou un chemin mort avant même que
  le push parte, et il se contourne bruyamment (`AMK_SKIP_CI=1`).
- **Le crochet se contourne** : `AMK_SKIP_CI=1 git push` — et il le dit à voix haute. Un garde-fou qui ne
  se contourne pas serait un mur ; un garde-fou muet serait un piège.
- **La fraîcheur du handoff n'est pas automatique** : le cockpit la signale, il ne la répare pas.
- **`provision.sh` dépend du réseau** : sans GitHub ni PyPI, une session neuve n'a que les outils locaux (`tools/qa`, `tools/ops`, `tools/graphify` une fois installé).
- **Notion reste manuel, mais il n'est plus oubliable** : la porte `miroir-notion` compare la ligne
  `MIRROR` aux commits qui touchent un fait debout ; elle dit *qu'il faut y aller*, elle n'y va pas.
- **La règle 15 n'a pas de porte** (voir §9) : elle tient par la forme de la réponse. La règle 12 a une
  porte faible, souple, qui nomme les lignes fautives sans jamais bloquer.
- **Le tableau §9 peut mentir par omission** : c'est désormais la porte 13 qui le dit (`registre-complet`).
  Elle a été écrite le jour où le tableau annonçait douze règles quand le code en appliquait treize.
- **Aucun outil ne juge un document** : `audit_files.py` compte, il ne lit pas. Le jugement reste entier.
- **La session pèse plus lourd que le dépôt** : mesuré le 24/10, les 24 outils installés occupent
  ~4,5 Go (`/tmp` + `~`) contre 165 Mo pour le dépôt. Rien de tout cela n'est dans Git, et tout
  disparaît avec la session — le coût n'est pas le disque, c'est **cinq minutes de réinstallation
  et vingt occasions de panne par session**. C'est ainsi que la CI est tombée trois fois le 24/10.

## 11 · Cinq chantiers pour que ça tienne dans la durée (recherche du 24/10)

> King : *« donne-moi cinq façons de nettoyer et d'optimiser ce dépôt, et de rendre notre méthode plus
> efficace sur le long terme »*. Les cinq sont classées par **levier**, pas par facilité. Chacune dit ce
> qu'elle règle, ce qu'elle coûte, et le premier pas qui ne demande aucune décision.

**Ce que la mesure dit ce soir** avant de proposer quoi que ce soit : 1 638 fichiers suivis, **144 Mo**
dans l'arbre, plus gros fichier **14,6 Mo** (`clients/dm-optic/brag/brag.mp4`) ; `.git` **154 MiB** en
clone superficiel et ~**1,06 GiB** en clone complet ; **765 documents** `.md` dont **412 que personne ne
cite** ; 406 médias suivis dont **66 jamais nommés** (5,9 Mo) ; CI **32–40 s** par push et **trois rouges
en une journée** ; provisioning **4,5 Go et ~5 min** avant le changement de ce soir.

### ① Un plafond de poids, pas une purge

**Le problème.** Le dépôt grossit par accrétion : chaque livraison, chaque rendu, chaque export entre par
la racine et n'en ressort jamais. Une purge annuelle ne règle rien : elle remet le compteur à zéro une
fois, puis le dépôt regrossit.

**Le mécanisme.** Un seuil **mesuré à chaque tour** — c'est la règle 14, posée aujourd'hui : **160 Mo**
suivis, **15 Mo** par fichier au maximum. Souple : elle avertit, elle ne bloque pas. Le geste pour
redescendre est toujours le même : sortir les livrables (②), pas compresser des originaux.

**Le gain.** Aujourd'hui 141 Mo / 14,6 Mo : sous le seuil, mais à 88 %. Le seuil est là pour être **vu**
avant d'être franchi, pas après.

**Le coût.** Zéro : la règle existe et tourne en 200 ms.

**Le premier pas.** Déjà fait. La suite, quand on approchera de 150 Mo : baisser le plafond par fichier à
8 Mo et exiger une ligne de justification dans ce document pour toute exception.

### ② Les livrables sortent de l'arbre : une Release par livraison

**Le problème.** Un zip de livraison dans le dépôt ne sert qu'une fois — le jour où on le téléverse — et
pèse ensuite pour toujours. Preuve de ce soir : l'archive du 21/10 (182 entrées) ne correspond plus au
site (251 entrées). Un livrable figé dans l'arbre **ment** dès que la source bouge.

**Le mécanisme.** Une **Release GitHub par livraison** : `dmoptic-v2-2026-11`, asset zip, notes de
version dans la release. Le dépôt garde trois lignes dans `build-notes.md` (date, empreinte, lien) et
refait le zip à la demande par `python3 demos/pack_dmoptic.py`. Les releases acceptent 2 Go par fichier
et ne comptent **pas** dans la taille du dépôt.

**Le gain.** L'arbre cesse de grandir avec les livraisons ; chaque livraison devient datée et retrouvable
sans ambiguïté ; le clone reste petit.

**Le coût.** 10 minutes par livraison, une fois, avec `gh release create`.

**Le premier pas.** Fait à moitié ce soir : l'archive existante est renommée `dmopticsarl-2026-10-21.zip`
pour porter sa date, et `/dmopticsarl*.zip` est ignoré pour que le zip du jour n'entre plus. La prochaine
livraison part en release.

### ③ Les médias par empreinte, pas par octets

**Le problème.** 406 médias suivis, dont 66 que **rien** ne nomme (5,9 Mo) : ils sont là, personne ne les
appelle, et la carte les compte. À l'inverse, les 395 Mo de photos brutes du shooting vivent hors du
dépôt — et rien dans le dépôt ne dit **lesquelles** existent, ni où.

**Le mécanisme.** Un `MEDIA.md` par dossier client : nom du fichier, **sha256**, dimensions, poids, **où
il vit** (disque de King, Drive, téléphone), et une vignette 800 px suivie à sa place. On garde la
traçabilité, pas les octets. Les 66 médias non nommés sont soit cités quelque part, soit sortis.

**Le gain.** Retrouver un original devient possible sans le stocker ; la carte cesse de compter des
fichiers que personne n'utilise ; les 395 Mo restent dehors **sans être perdus**.

**Le coût.** 30 minutes par dossier client, une fois. Un script de 40 lignes pour générer les sha256 et
les vignettes.

**Le premier pas.** Le refaire pour `clients/dm-optic/photoshoot` (23 Mo ici, 395 Mo chez King) : c'est le
seul dossier où l'écart entre ce qu'on a et ce qu'on croit avoir est déjà prouvé.

### ④ Décroissance documentaire : 765 documents, 412 orphelins

**Le problème.** Plus de la moitié des documents du dépôt ne sont **cités par aucun autre** (412 sur 765).
Un document orphelin n'est pas inutile : il est **inatteignable** — donc il ne contredit personne, ne se
relit jamais, et vieillit en silence. C'est exactement le mécanisme qui a produit les 37 « périmés » et
les quatre statistiques fausses de ce week-end.

**Le mécanisme.** Chaque document porte en tête deux lignes : **propriétaire** et **date de péremption**
(90 jours pour une recherche, 365 pour une doctrine). À l'échéance, il part dans `archive/` — **hors de la
carte et hors des portes**, jamais supprimé. Et un document souverain doit être cité par l'index, sinon
la porte 13 le dit.

**Le gain.** Lire, cartographier et auditer coûte proportionnellement au nombre de documents vivants. Passer
de 765 à ~250 vivants divise par trois le bruit de la carte, des audits et de mes relectures — et rend les
portes plus précises, parce qu'elles cessent de crier sur des brouillons de septembre.

**Le coût.** Un tri de deux heures, puis zéro entretien : la péremption fait le travail.

**Le premier pas.** Aucune décision nécessaire : générer la liste des 412 orphelins avec leur date et leur
dernière citation, et la proposer en une page. C'est le prochain chantier que je proposerais.

### ⑤ Les contrôles en amont, et une session qui démarre en une minute

**Le problème.** Aujourd'hui, trois choses coûtent du temps **après** le travail : la CI rougit après le
push (trois fois le 24/10), la carte se reconstruit après coup, et une session neuve repart de zéro
(4,5 Go et ~5 min). Ce sont des allers-retours, pas du travail.

**Le mécanisme.** (a) Le **pre-commit** joue ce que la CI joue (carte reproductible, chemins cités,
sources), pour que le rouge arrive avant le push et non après ; (b) **cache des dépendances** dans le
workflow (le venv `graphify` épinglé est identique à chaque run : 40 s → ~15 s) ; (c) provisioning par
défaut réduit au noyau — **fait ce soir** : 4 outils au lieu de 24, ~1 min au lieu de 5.

**Le gain.** Mesurable : trois rouges évités = trois allers-retours de 5 minutes ; 25 s par run de CI ;
4 minutes par session.

**Le coût.** Une heure pour le pre-commit, 15 minutes pour le cache (côté King : le workflow est à lui
seul, la GitHub App n'a pas la permission `workflows`).

**Le premier pas.** Fait : le provisioning ne rejoue plus que le noyau. Reste le cache CI (à demander à
King) et le pre-commit.

---

**Ce que je ne recommande pas**, et pourquoi :

- **Réécrire l'historique pour retirer les vidéos.** Mesuré : 8 blobs `mp4` pèsent ~70 Mo, soit **~7 %**
  d'un clone complet (~1,06 GiB). En échange, **tous** les SHA changent — les 33 commits cités dans nos
  documents, les PR #13 à #17, les lignes `MIRROR` — et GitHub garde de toute façon les objets atteignables
  par les PR. On paierait une rupture pour 70 Mo sur 1 060.
- **Supprimer les documents périmés.** Le 24/10, une suppression fondée sur « périmé » aurait effacé
  1 400 lignes de règles de design. On archive, on ne supprime pas.
- **Un outil de plus pour ranger.** Le rangement est un geste hebdomadaire, pas un logiciel : trois outils
  de plus seraient trois endroits de plus où chercher.

*Cette carte se relit quand un outil entre ou sort, quand une porte change, ou quand une panne nouvelle
apparaît. Sinon, elle se lance : `bash tools/ops/machine.sh`.*
