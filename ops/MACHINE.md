# LA MACHINE — un tour, un engagement, un actif : ce qui intervient, quand, comment, pourquoi

> Créé le 24/10/2026 (ruling King : *« everything … should work like a single machine »*).
> Ce document ne dit **aucune règle métier**. Il dit **l'ordre**, **qui tranche quoi**, **ce qui vérifie**,
> et **où ça s'écrit**. Quand il contredit `PRE-FLIGHT.md` ou un document de `knowledge/`, c'est le
> document qui gagne : la machine est le câblage, pas la loi.

## 0 · Trois commandes, et vous savez où vous êtes

```bash
bash tools/ops/session.sh              # ouvrir une session : fetch · noyau · crochets · portes · état (0,9 s à chaud, 12 s à froid)
bash tools/ops/machine.sh              # le cockpit : l'étape, ce qui est frais, ce qui ne l'est plus
bash tools/ops/machine.sh 2            # la fiche de l'étape 2 (lecture) : quoi lire, quoi lancer, quand c'est fini
bash tools/ops/machine.sh --who prix   # qui tranche le sujet « prix », et ce qui le vérifie
bash tools/ops/machine.sh --merge      # la jauge de fusion : combien de fichiers/lignes depuis main
bash tools/ops/machine.sh --rules      # les 17 règles debout, chacune avec sa porte (§9)
bash tools/ops/provision.sh            # le noyau de travail : 4 outils (les 24 : --all)
bash tools/ops/provision.sh --list     # les 24 outils : installés cette session, ou pas
bash tools/ops/install-hooks.sh        # pose pre-commit (portes + carte) et pre-push (portes) : un rouge ne part plus
python3 tools/ops/machine.py --ci      # ce que le crochet joue, et ce que la CI jouera
bash tools/ops/machine.sh --turns      # le rendement du jour : commits, fichiers, lignes, refus
```

Le miroir Notion (PRE-FLIGHT §0g) est **daté ici**, dans une ligne que la machine lit :

```text
MIRROR 2026-10-26 · 2c5c8e8 · CRM des 15 envois + plan de relance du 28/10
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

> **L'étape 0 porte deux gestes, dans cet ordre : `wake.py` (l'arbre) puis `bash tools/graphify/preflight.sh`
> (le graphe).** Ruling King 25/10, 141ᵉ message : *« use graphify update or read graph, before you read
> pre-flight document »* — le graphe passe **avant** la lecture de `PRE-FLIGHT.md`, donc avant l'étape 1.

Chaque étape a **une question**, **une sortie vérifiable** et **un incident qui l'a créée**. Un tour qui
saute une étape ne plante pas tout de suite : il plante trois tours plus tard, quand plus personne ne
sait pourquoi le chiffre était faux.

| # | Étape | La question | La sortie qui prouve que l'étape est faite | Ce qui intervient |
|---|---|---|---|---|
| 0 | **Réveil + graphe** | *L'arbre que je lis est-il le vrai dépôt — et le graphe reconstruit dessus ?* | `wake.py --check` code 0 **et** la ligne d'étape 0 de `tools/graphify/preflight.sh` (graphe rejoué, carte lue, fichiers nommés) | `tools/ops/wake.py` · `tools/graphify/preflight.sh` · `ops/REPO-MAP.md` · `ops/GIT-STABILITY-NOTE.md` |
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
| 0 Réveil + graphe | Quatre fois dans la même journée, le travail local a disparu et deux affirmations fausses ont été publiées (« le catalogue est vide », « la semaine 3 est bloquée ») — l'arbre lu n'était pas le dépôt. **Complété le 25/10** : le graphe se lit avant `PRE-FLIGHT.md`, sinon la règle se cherche de mémoire (ruling 141) | 22/10 et 25/10 |
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
| **Crochets** | `bash tools/ops/install-hooks.sh` (une fois par clone) → `.git/hooks/pre-commit` et `pre-push` | un commit avec un secret ou un chemin mort ; **et la carte**, reconstruite et ré-ajoutée si elle a changé (5 s) | les rapports lents : `audit_files.py` (7,5 s), `media_inventory.py --check` (9,8 s), `audit_claims.py` — ils restent dans `--check` et la CI |
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

## 7 · Les dix invariants

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

9. **Aucune valeur de la machine dans un artefact suivi.** La carte recopiait `date.today()` dans son
   en-tête : juste sur le poste, faux sur le runner, et l'étape « la carte se rejoue à l'identique » est
   tombée rouge sur un dépôt qui n'avait pas bougé d'un octet. La date vient maintenant du commit
   (`git log -1 --date=short`). Ni heure, ni fuseau, ni nom d'hôte, ni `$HOME` dans un fichier versionné.
10. **Une porte ne s'ouvre jamais sur une absence.** Le 24/10, `fusion-sur-seuil` s'est déclarée satisfaite
   parce que `origin/main` manquait dans le clone : faute de mesure, elle a répondu « rien à signaler »,
   et 544 fichiers ont attendu quatre tours de trop. Une mesure impossible est une panne, pas une
   permission.

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
| Carte rouge alors que rien n'a bougé | la CI échoue sur « la carte se rejoue à l'identique » (exit 1 dans la branche `git diff --quiet`), le même commit est vert sur le poste | première cause trouvée le 24/10 : la **date** venait de l'horloge (corrigée, invariant 9). **Seconde cause, trouvée et corrigée le 25/10** (elle était ouverte au 24/10) : le §4 de la carte classait les documents par `nx.community.louvain_communities(G, seed=42)` — **13 communautés ici, 15 sur le runner, même commit**. Une graine ne fixe pas l'ordre interne d'un graphe : elle ne rend pas un algorithme reproductible. Le remplacement est une propagation d'étiquettes écrite dans le dépôt (tri + égalité tranchée par la plus petite étiquette), et la carte est désormais identique à l'octet sous trois hash/TZ différents. Louvain reste dans le graphe généré (dossier `graphify-out/`, non suivi par git) |

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
| 3 bis | `etape-0-graphe` | Le graphe est rejoué (ou la carte lue) **avant** la lecture de `PRE-FLIGHT.md` | PRE-FLIGHT §00 · rulings 141-142 | début de chaque tour | estampe `~/.amk-provisioned/preflight.stamp` du jour **et** carte écrite au même moment — ⚠ souple (un runner n'a pas d'estampe) |
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
| 16 | `medias-avec-empreinte` | Un dossier qui porte des médias a un inventaire par empreinte, à jour | MACHINE §11 ③ · `tools/ops/media_inventory.py` | chaque commit | nombre de fichiers vs l'inventaire du dossier — ⚠ souple |
| 17 | `crochets-poses` | Les crochets qui jouent la CI avant le push sont posés, et à jour | MACHINE §11 ⑤ · `tools/ops/install-hooks.sh` | chaque `--check` | `pre-commit`/`pre-push` présents et identiques au dépôt — ⚠ souple |
| 18 | `workflow-colle` | Le workflow proposé au dépôt est celui qui tourne vraiment | MACHINE §11 ⑤ · `ops/machine.yml.propose` | chaque `--check` | corps du `.propose` comparé à `.github/workflows/machine.yml` — ⚠ souple |

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

**Le premier pas — fait le 24/10 au soir, en deux temps, et le second vaut mieux que le premier.**

1. **`tools/ops/release.sh`** publie un livrable et ne le déclare publié qu'après un **aller-retour réel** :
   `gh release create`, puis retéléchargement de l'asset et comparaison du sha256 et de la taille. Une
   publication non vérifiée n'est pas une publication. Il refuse aussi de commencer si
   `uploads.github.com` (l'hôte qui reçoit le fichier, distinct d'`api.github.com` qui crée la release)
   n'est pas joignable — le `EOF` de `gh`, sans cette garde, ne dit rien.
2. **`tools/ops/pack_factures.sh`** : le livrable de l'outil de factures (88 Ko) **se refait à
   l'identique** depuis `ops/amk-factures-pwa/`, qui reste versionné. Il est donc sorti de l'arbre — non
   pas publié puis supprimé, mais jamais eu besoin d'être là. L'empreinte de contenu le prouve :
   `5902f1f5…ecf6` avant et après, et le script **échoue** si la source bouge d'un octet (testé).

**Mesuré, sans se raconter d'histoire** : le livrable retiré pèse **88 Ko**, soit 0,06 % d'un arbre de
144 Mo. Ce n'est pas une optimisation de poids — le gros du poids est dans la vidéo et les photos du
catalogue, et ① le plafonne déjà. Le gain de ② est **structurel** : un livrable n'entre plus dans
l'arbre, et chaque livraison devient datée, empreintée et retrouvable sans ambiguïté. L'archive du
site (4,6 Mo) attend sa Release : elle n'est pas reproductible (182 entrées contre 251 aujourd'hui), donc
elle reste dans l'arbre tant qu'elle n'est pas publiée — on ne remplace pas un fichier par une promesse.

**Ce qui bloque, nommé** : depuis l'environnement de session du 24/10, `uploads.github.com` est
injoignable alors qu'`api.github.com` répond. La commande est prête, le commentaire de version est écrit,
le registre `ops/LIVRAISONS.md` dit quoi lancer. Sur une machine ordinaire, une ligne et c'est fait.

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

**Le premier pas — fait le 24/10 au soir.** `tools/ops/media_inventory.py` (0 dépendance) lit
l'empreinte et les dimensions de chaque média suivi, puis écrit un `MEDIA.md` par dossier de plus de
2 Mo. Mesuré : **460 médias suivis, 104 Mo** (72 % de l'arbre), **12 dossiers** inventoriés,
**95 médias que rien ne nomme** (contre 66 estimés — l'estimation était basse), et surtout
**25 empreintes partagées = 27 copies inutiles, 2,6 Mo** que l'œil ne voyait pas :

| Empreinte | Poids | Copies |
|---|---|---|
| `48d3d3160a35` | 232 Ko | `hosting/samples/img/nova.png` **=** `site/img/nova.png` |
| `aaf29f9471cd` | 193 Ko | `hosting/samples/img/mmc-consult.jpg` **=** `site/assets/mockup-clinique.jpg` **=** `site/img/mmc-consult.jpg` |
| `942ff33b65ee` | 212 Ko | `clients/_mockups/labs/labiomed.jpg` **=** `hosting/previews/labiomed/og.jpg` |

Ce que l'outil ne fait pas, et c'est volontaire : il ne supprime ni ne remplace aucune référence. Une
copie qui « ne sert à rien » peut être l'image qu'un HTML déployé appelle par son nom — le dédoublonnage
est une décision, pas une déduction. Ce tour apporte la **preuve** ; la suppression viendra fichier par
fichier, en regardant qui l'appelle.

Deux modes de plus : `--thumbs DIR` écrit les vignettes 800 px **hors du dépôt** (jamais dans git : une
vignette est un cache, pas un livrable), et `--check` compare les empreintes — c'est la version stricte,
la porte 16 se contentant du nombre de fichiers (un sha256 de 104 Mo coûterait 8 s à chaque tour).

**Deux pièges de mesure, trouvés en écrivant l'outil, et tous les deux corrigés :**

1. **Un inventaire qui se cite lui-même.** Le premier comptage a annoncé 67 médias non nommés au lieu de
   95 : les `MEDIA.md` venaient de lister les fichiers, donc chaque média était « cité » — par sa propre
   fiche. Un thermomètre qui se met dans le four. Les inventaires sont désormais exclus du corpus de
   citations ;
2. **« périmé » à cause d'une virgule dans un autre document.** Le nombre de citations figure dans le
   tableau, donc éditer n'importe quel document rendait tous les inventaires « périmés ». `--check`
   compare maintenant une **signature d'empreintes** écrite dans le fichier ; le texte se rafraîchit par
   `--write`, la porte ne juge que les octets.

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

**Le premier pas — fait le 24/10 au soir.** L'inventaire est régénéré à chaque audit (`ops/FILE-AUDIT-*.md`
§ 4 bis) : sur **412 orphelins**, **82 seulement sont à traiter** — les 330 autres sont normaux (164
imports tiers, 116 fiches CRM, 50 README d'outils). Et le défaut apparaît : **29 de ces 82 n'ont aucune
date**, ni dans leur chemin ni dans leur en-tête. Un document sans date ne peut pas expirer.

**Premier lot archivé** : huit documents de septembre (`Send-Pack` ×4, `PLAN-2026-09-19-21`,
`Passe-Vitrine-2026-09-23`, `Expansion-Geography-2026-09-18`, `Social-Growth-Synthesis-2026-09-18`) →
`archive/2026-09/`. Campagnes terminées, zéro citation entrante, rien qui en dépende. `archive/` sort du
corpus (ni carte, ni portes, ni audit) mais reste dans git : on archive, on ne supprime pas.

**Deuxième lot, le même soir — les 29 récoltes YouTube.** Synthétisées avant d'être archivées, comme la
règle le demande : `research/YOUTUBE-SYNTHESE-2026-10-24.md` tient en une page les 33 rapports de vidéo
(11–12/10) — 14 leçons adoptées avec leur destination, 7 refus nommés, 5 questions ouvertes, 2 trous
(v20 sans source vérifiable, v18 doublon de v11). Les 27 fichiers bruts partent dans
`archive/2026-10/youtube-lessons/`, et les cinq pointeurs de `research/YouTube-Lessons.md` suivent —
sinon la synthèse serait exacte et les liens morts.

**Effet mesuré** : 412 → **393 orphelins**, 82 → **63 à traiter**. La plus grosse famille disparaît de
la liste sans qu'un seul fichier soit perdu.

**Reste à décider** : les 15 orphelins de `clients/dm-optic` (à citer depuis le dossier, pas à archiver),
les 7 `STATUS.md` de vidéos (partent avec le lot du mois), les 7 de `ops/` et les **41 documents sans
date** — ceux-là sont le vrai chantier : un document sans date ne peut pas expirer.

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

#### Fait le 25/10 — les trois pièces, avec leurs chiffres

**1 · `pre-commit` (nouveau) — 1 à 5 s.** Il joue `machine.py --ci` (secrets, chemins cités : 0,8 s) puis
reconstruit la carte et **la ré-ajoute au commit si elle a changé** (0,5 à 5 s). C'est la panne la plus
fréquente du dépôt : on touche trois fichiers, on oublie `build_full_graph.py`, la CI tombe rouge.
Mesuré sur un vrai commit : **5,8 s au total**, dont 5 s de carte, et le message « 🗺 carte reconstruite
et ajoutée au commit » — jamais en silence.

Ce qu'il ne joue **pas**, exprès : `audit_files.py` (7,5 s), `media_inventory.py --check` (9,8 s),
`audit_claims.py`. Un crochet de vingt secondes se contourne avec `--no-verify`, et un crochet contourné
ne vérifie plus rien. Ces trois-là restent dans `--check` et dans la CI.

**2 · `session.sh` (nouveau) — 12 s à froid, 0,9 s à chaud.** `git fetch` → noyau (`provision --core`,
saut immédiat si les estampes existent) → crochets posés s'ils manquent → `--check` → l'état en quatre
lignes (branche, commits depuis `main`, âge de la carte, orphelins à traiter) → le temps total affiché.
Mesuré pour de vrai en effaçant le venv et les estampes : **12,1 s** (dont 11 s de `pip install graphify`
épinglé). Contre ~5 min et 4,5 Go avant le 24/10.

**3 · La CI — mesurée avant d'être optimisée, et le remède n'est pas celui que je croyais.** Le
workflow appartient à King : la GitHub App n'a pas la permission `workflows`, donc je fournis
`ops/CI-CACHE.patch`, vérifié par `git apply --check`. **Une commande :**

```bash
git apply ops/CI-CACHE.patch && git commit -am "CI : un run par commit, historique sans blobs, cache pip" && git push
```

Ce que j'ai mesuré le 24/10 avant de le proposer — et qui contredit ce que j'avais annoncé :

| Levier | Ce que ça coûte vraiment | Gain mesuré |
|---|---|---|
| `cache: pip` | `pip download` de **31,8 Mo** : **4,3 s** sans cache, **3,8 s** avec. L'installation elle-même (`pip install`) : 8,6 s sans cache, 8,1 à 9,5 s avec | **≈ 0,5 s** — le cache ne supprime pas le dépaquetage |
| `filter: blob:none` | le dépôt pèse **848 Mo** ; l'historique sans blobs (691 commits) = **1,3 Mo** ; l'arbre de HEAD = **250 Mo** | **≈ 10 s estimés** (848 → 250 Mo à télécharger) |
| un seul run par commit | **12 commits sur 25** jouaient deux fois (push + pull_request) | **la moitié des minutes** |

Le run de `838fba8` fait **37 s** (33 s de job). J'avais annoncé « 40 s → 15 s » : c'était une
extrapolation, pas une mesure. Le cache pip, tel quel, ne tient pas cette promesse. Le vrai poids est
le **clone** — `fetch-depth: 0` télécharge les 848 Mo d'un dépôt dont 600 Mo d'images mortes — et le
**doublon d'exécution**. Le patch fait donc les trois : clone partiel (l'historique reste complet, donc
`merge-base` et la jauge de fusion continuent de fonctionner ; seuls les blobs changent), un push ne
déclenche plus qu'un run (les branches sont couvertes par `pull_request`, `main` par le push d'après
fusion), et deux poussées rapprochées s'annulent au lieu de s'empiler.

**Ce que je ne fais pas** : réécrire l'historique pour retirer les 600 Mo d'images mortes
(`git filter-repo`). Ça marcherait — mais ça change tous les hachages, donc la ligne `MIRROR`, les
références de ce document et les PR ouvertes. À décider par King, pas par un script.

**Si le run suivant ne descend pas sous 30 s, je le dirai** — et alors le levier suivant sera de
mettre le venv installé en cache, pas de re-cacher des roues.

**3 bis · Pourquoi ce patch ne peut pas partir d'ici — et la porte qui remplace le patch oublié.**
Le 24/10, la commande a été exécutée telle quelle : `git apply` a marché, le commit s'est fait, et
GitHub a refusé **le push entier** — `refusing to allow a GitHub App to create or update workflow …
without 'workflows' permission`. Le commit a été annulé, l'arbre est resté propre : rien n'est parti.

Ce n'est pas une limite du bac, c'est une règle de la plateforme. En 2022, la CVE-2022-46258 a permis
de créer des workflows avec le token d'un workflow, donc d'escalader vers les secrets : depuis, aucun
`permissions:` ne peut donner cette portée au `GITHUB_TOKEN`, et une App ne l'obtient que si elle la
demande explicitement.

**Et c'est là que mon conseil était faux.** J'ai proposé à King d'accorder `Workflows: Read and write`
à l'App. Il a ouvert son écran : **« Settings → Developer settings → GitHub Apps » répond « No GitHub
Apps »**. L'App qui pousse appartient à **Arena**, pas à lui — il ne peut ni la voir ni la modifier.
Il n'y a donc pas d'option A. Il reste deux gestes, et un seul est à sa portée sans terminal :
**éditer le fichier depuis l'éditeur GitHub** (le commit est alors signé par son compte, qui a tous les
droits), ou `git apply` en local.

**Le trou que ça laissait** : un patch CI oublié ne se voyait nulle part. Il pouvait pourrir des
semaines dans `ops/` en ayant l'air appliqué. D'où la règle 18, `workflow-colle` (souple) : à chaque
`--check`, `tools/ops/machine.py` compare le **corps** de `ops/machine.yml.propose` à
`.github/workflows/machine.yml`. Mesuré aujourd'hui : **46 lignes de différence** — le patch n'est pas
appliqué, et le système le dit sans qu'on ait à s'en souvenir.

**3 ter · Mesuré après application, le 24/10 à 19 h 25 (commit de King `4485052`).** Le workflow est
collé : 58 lignes, **identique à l'octet** au corps de `ops/machine.yml.propose`, et la règle 18 passe
au vert. Le premier commit a fait tomber la CI — la carte n'était pas reconstruite (7 clés YAML
nouvelles = 7 symboles de plus, 11 786 → 11 793 nœuds) : c'est la panne que le crochet attrape sur le
poste, et que l'éditeur GitHub contourne. Carte reconstruite, CI verte.

**Le gain, tel qu'il est mesuré — pas tel qu'il était annoncé.**

| | Avant (workflow 42 lignes) | Après (workflow 58 lignes) |
|---|---|---|
| Runs par poussée de branche | **2** (push + pull_request) sur **12 commits de 25** | **1** |
| Durée d'un run | 36 s (médiane de 4) | **27–28 s** (2 derniers runs verts) |
| Coût d'une poussée | **72 s** | **27 s** — **−62 %** |
| Verdicts à lire | 2, parfois divergents | **1** |

**Où passent les 25 s du job, décomposées par les trois repères** (`portes-debut`, `portes-fin`,
`carte-fin`, lus dans les annotations faute de logs) : mise en route **2 s** · checkout + setup-python
**7 s** · portes **1 s** · **carte 15 s** · queue **2 s**.

Les 15 s de la carte sont presque entièrement **l'installation de `graphifyy`** : 8–9 s mesurées pour
le `pip install` (31,8 Mo à dépaqueter), contre 3,9 s pour la construction de la carte elle-même. Le
cache pip, lui, ne gagne que ~0,5 s — il évite le téléchargement, pas le dépaquetage. **Le prochain
levier n'est donc pas de cacher des roues, mais le venv installé** (`actions/cache` sur
`/tmp/amk-graphify`) : ~7 s de plus, et une troisième édition du workflow. À décider par King, pas
d'office : chaque édition passe par son navigateur.

**4 · Une panne trouvée en chemin, et corrigée.** Pendant ce tour, `graphify-out/` avait disparu du
bac : `audit_files.py` a alors annoncé **743 orphelins, 351 à traiter** — et un lecteur pressé en aurait
archivé 350. Sans graphe, l'audit rendait un dictionnaire vide, donc *tout* document paraissait orphelin.
Il dit maintenant **« non mesurés »** et donne la commande. C'est la même leçon que la jauge de fusion :
**une mesure impossible n'est pas un zéro.**

**5 · Une deuxième panne trouvée en chemin : l'audit se lisait lui-même.** En rejouant
`audit_files.py` deux fois de suite, le nombre de médias sans référence faisait **63 → 60 → 63**.
Cause : le rapport `ops/FILE-AUDIT-<date>.md` cite les noms des médias qu'il déclare sans référence ;
en entrant dans le corpus, il les référençait lui-même, et chaque exécution réécrivait la liste que la
suivante allait lire. Les rapports d'audit sortent donc du corpus (`is_own_report()`), et trois
exécutions consécutives rendent maintenant le même octet. **Le chiffre corrigé monte : 104 médias sans
référence** au lieu de 60 — les 44 de différence n'étaient cités que par le rapport lui-même. Aucun
n'est supprimé pour autant : c'est une piste, pas une preuve.

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
