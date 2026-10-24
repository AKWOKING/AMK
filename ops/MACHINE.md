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
bash tools/ops/machine.sh --rules      # les 12 règles debout, chacune avec sa porte (§9)
bash tools/ops/provision.sh --list     # les 24 outils : installés cette session, ou pas
bash tools/ops/install-hooks.sh        # pose le crochet pre-push : un push rouge ne part plus
python3 tools/ops/machine.py --ci      # ce que le crochet joue, et ce que la CI jouera
```

Le miroir Notion (PRE-FLIGHT §0g) est **daté ici**, dans une ligne que la machine lit :

```text
MIRROR 2026-10-24 · bbf2a52
```

Tant qu'un fichier de **fait debout** (pré-vol, machine, prix, dossiers clients, journal des ventes)
change après ce commit, la porte `miroir-notion` reste fermée et `--check` échoue. On met Notion à jour,
puis on re-date la ligne.

Une session neuve n'a **ni skills, ni venvs, ni clones** : `bash tools/ops/provision.sh` les refait
depuis les installateurs épinglés du dépôt. C'est l'étape 0 de la machine, pas une option.

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
| **Règles** | `bash tools/ops/machine.sh --rules` | les 7 portes dures du registre §9 | les 2 règles sans porte, dites en clair |
| **Crochet** | `bash tools/ops/install-hooks.sh` (une fois par clone) → `.git/hooks/pre-push` | un push avec un secret ou un chemin mort | la carte rejouée (trop lent pour un crochet) |
| **Usage** | `bash tools/ops/machine.sh --usage` | un outil provisionné qu'aucune trace ne montre appelé | ce qui ne laisse aucune trace : scripts QA lancés à la main, skills lus, recherche web |

**La trace d'usage, et pourquoi elle existe.** Un outil « installé » n'est pas un outil « utilisé » : le
24/10, la panne notée en §8 disait *24 installateurs, 3 outils appelés*. `--usage` lit un journal hors
dépôt (`~/.amk-provisioned/usage.log`) que les outils écrivent eux-mêmes — `machine`, `provision`,
`graphify`, `ask` — et **oppose une trace à chaque phrase « j'ai utilisé l'outil »**. Il ne voit que ce
qui laisse une trace : un script QA lancé à la main, un skill lu, une recherche web n'y figurent pas, donc
ils ne sont jamais comptés à la place de King. Sa sortie la plus utile est la ligne *« provisionnés mais
muets »* : un outil installé que rien n'appelle est un candidat à sortir (invariant 6), pas un acquis.

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

| # | Règle | Fondement | Déclencheur | Porte |
|---|---|---|---|---|
| 1 | Rien ne reste hors commit quand le tour se dit fini | PRE-FLIGHT §1e | fin de tour | `git status --porcelain` vide |
| 2 | Le tour finit poussé ; une branche sans remote n'est pas un travail rendu | §7 invariant 7 | fin de tour | `rev-list @{u}..HEAD` = 0 |
| 3 | La branche se fusionne sur seuil, pas sur humeur | PRE-FLIGHT §1i | chaque sortie | `machine.sh --merge` — 40 fichiers / 3 000 lignes |
| 4 | La carte du dépôt est reconstruite quand un fichier suivi bouge | PRE-FLIGHT §0h | fichier modifié | `REPO-MAP.md` plus récent que tout fichier suivi |
| 5 | Une session neuve rejoue le noyau épinglé avant de travailler | PRE-FLIGHT §1f | début de session | estampes `~/.amk-provisioned` (graphify, superpowers) |
| 6 | Le miroir Notion suit le jour même tout changement d'un fait debout | PRE-FLIGHT §0g | commit sur un fait debout | `git diff MIRROR..HEAD` sur les chemins de §0g |
| 7 | Ni mot de passe, ni clé, ni jeton dans un dépôt public | PRE-FLIGHT §0g | avant chaque push | `git grep` des motifs de secret (code tiers exclu) |
| 8 | Le comptage des fichiers a moins de sept jours | `ops/AUDIT-FICHIERS` | chaque semaine | âge de `ops/FILE-AUDIT-*.md` — ⚠ souple |
| 9 | L'état de reprise a moins de trois jours | `ops/HANDOFF-*.md` | tous les trois jours | âge du dernier handoff — ⚠ souple |
| 10 | Tout `.md` neuf à la racine ou dans `ops/` se déclare avant de devenir loi | PRE-FLIGHT §4b | apparition d'un doc souverain | `git diff --diff-filter=A` — ⚠ souple |
| 11 | Aucune statistique sans source primaire nommée | PRE-FLIGHT §1g | chaque chiffre écrit | ○ **sans porte machine** |
| 12 | Un fichier debout nouveau n'existe qu'avec le oui de King | PRE-FLIGHT §4b | création d'un document souverain | ○ **sans porte machine** |

**Les deux trous, dits franchement.** Les règles 11 et 12 ne peuvent pas être jugées par un code retour :
un script ne sait pas si un chiffre a une source, ni si King a dit oui. Elles restent dans le registre
avec leur marque `○` plutôt que d'être rangées dans un document que personne ne relit. Leur substitut
mécanique est **la forme de la réponse** : un chiffre sans chemin est refusé à la relecture, et un
document souverain neuf est *proposé* dans la réponse avant d'être committé. Si un jour l'une des deux
devient vérifiable, elle passe en porte dure — c'est le seul sens de circulation autorisé.

**Ce que le registre interdit** : ajouter une règle ici sans lui donner de porte, ou de sévérité
explicite. Une règle sans porte est un trou ; un trou caché est une panne.

---

## 10 · Ce qui manque encore, dit franchement

- **L'intégration continue est locale, pas encore côté GitHub** : le crochet `pre-push` bloque un push
  avec un secret ou un chemin cité mort, et il est posé par `install-hooks.sh`. Le workflow qui ferait la
  même chose *dans* GitHub est écrit et testé (`tools/ops/machine.workflow.yml`) mais **la GitHub App de
  l'atelier n'a pas la permission `workflows`** : il doit être copié par King vers
  `.github/workflows/machine.yml`. Tant qu'il ne l'est pas, la porte dépend d'un clone préparé.
- **Le crochet se contourne** : `AMK_SKIP_CI=1 git push` — et il le dit à voix haute. Un garde-fou qui ne
  se contourne pas serait un mur ; un garde-fou muet serait un piège.
- **La fraîcheur du handoff n'est pas automatique** : le cockpit la signale, il ne la répare pas.
- **`provision.sh` dépend du réseau** : sans GitHub ni PyPI, une session neuve n'a que les outils locaux (`tools/qa`, `tools/ops`, `tools/graphify` une fois installé).
- **Notion reste manuel, mais il n'est plus oubliable** : la porte `miroir-notion` compare la ligne
  `MIRROR` aux commits qui touchent un fait debout ; elle dit *qu'il faut y aller*, elle n'y va pas.
- **Les règles 11 et 12 n'ont pas de porte** (voir §9) : elles tiennent par la forme de la réponse.
- **Aucun outil ne juge un document** : `audit_files.py` compte, il ne lit pas. Le jugement reste entier.

*Cette carte se relit quand un outil entre ou sort, quand une porte change, ou quand une panne nouvelle
apparaît. Sinon, elle se lance : `bash tools/ops/machine.sh`.*
