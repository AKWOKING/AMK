# GIT STABILITY NOTE · 03/10 · pattern récurrent du sandbox

- **Pattern :** le `.git` du sandbox revient par intermittence à un commit de base au cours des longs
  tours (7 fois cette semaine, dont 1 le 03/10 en plein ruling DM).
- **Symptômes :** `views.py` redevient une vieille version ; les ancres de recherche python ne matchent
  plus ; `ls-remote` diverge du `git log` local.
- **Tells :** la sortie de la file RELANCE contredit ce qui vient d'être écrit ; le guard passe mais le
  contenu est périmé (rc=0 ne prouve rien — règle 02/10).
- **Mitigation (appliquée à chaque tour) :** `git ls-remote origin` est la **seule source de vérité** ;
  ne jamais faire confiance au seul état local ; au début du rituel, fetch + reset --hard sur la ref
  distante ; après chaque rebuild, vérifier la sortie de la file ; sauvegarder les écritures du tour
  dans /tmp avant tout reset.
- **Implication mercredi 07/10 :** si un commit pré-visite a rollback pendant la nuit, **re-vérifier
  contre la remote avant de partir pour Bonabéri** — le bundle de démo, les PDF d'impression et la file
  RELANCE doivent être relus depuis `origin/arena/01a0f7ad-amk`, pas depuis le working tree local.
- **05/10 — variante du piège :** le rendu « DATES À VENIR » sautait silencieusement toute entrée
  RELANCE sans ligne CRM (rc=0, file incomplète). Corrigé : fallback sur le slug + commentaire daté
  dans views.py. Vérifier la SORTIE après chaque rebuild reste la règle.

## Silent drops — classe de piège (ruling King 05/10)
*Silent drops: rc=0 outputs can be incomplete. Known instances: dict last-wins overwriting schedule
entries (02/10), prose-not-in-data keep flags (21/09), relance renderer dropping CRM-less slugs
(05/10). Pattern: any generator that joins on CRM rows will silently discard orphans. Before trusting
any generated view, grep for `next((r for r in rows` join sites.*

---

## 22/10/2026 — la cause est identifiée, et le remède est un outil

**Quatrième récidive de la journée** (après le 03/10 et sa série de 7). Cette fois la cause est lue
dans le reflog, plus devinée :

```
471bc84  clone: from https://github.com/AKWOKING/AMK.git
b134dd2  checkout: moving from main to arena/2fffee3b-amk
b134dd2  branch: Created from b134dd2d…
```

Ce n'est pas un « rollback » : **à chaque réapprovisionnement du bac, un clone neuf est créé et la
branche de session est replacée sur le commit de DÉBUT de session.** Tout ce qui a été commité après
n'existe plus en local — alors qu'il est intact sur `origin`. Le worktree, lui, est repeuplé depuis le
snapshot de l'espace de travail : on obtient donc un arbre qui *ressemble* au dépôt, avec un `.git`
qui ne correspond pas.

**Ce que ça a coûté le 22/10 :** deux affirmations fausses dans la même journée.
`frames.json` lu à **0 entrée** et le dossier `hosting/previews/dmoptic/montures/` lu **vide**, alors que
**tout l'inventaire (65 images)** est versionné (vérifié après réparation). Conclusion annoncée à King :
« la semaine 3 est bloquée faute de photos ». Faux. Il a fallu qu'il objecte pour que ce soit vérifié.

**Le remède — `tools/ops/wake.py`** (écrit et testé le 22/10) :

| Geste | Effet |
|---|---|
| `python3 tools/ops/wake.py` | récupère la branche, remet le local sur `origin`, **sauvegarde d'abord** tout travail non commité dans `/tmp/amk-wip-<horodatage>/` |
| `python3 tools/ops/wake.py --check` | ne modifie rien ; sort en **code 1** si l'arbre est périmé |
| `bash tools/ops/gate-dm.sh` | enchaîne l'état, la fraîcheur des rendus et les affirmations — et **s'arrête net** si l'arbre est périmé |

**Test de bout en bout, exécuté :** régression provoquée par `git reset --hard b134dd2` → `--check` sort
en 1 et annonce « en retard de 113 commits » ; `wake.py` restaure, `frames.json` repasse de 0 à 40
entrées, et la modification non commitée est bien retrouvée dans `/tmp/amk-wip-…/changes.patch`.

**Règles qui en découlent, désormais dans `AGENTS.md` :**

1. `wake.py` est le **premier appel de chaque tour**, avant toute lecture ou mesure.
2. **On pousse après chaque lot** : un commit local peut disparaître, un commit poussé non.
3. Un chiffre lu sans `wake.py` dans le même tour **n'est pas un chiffre**.
4. Pour un fait du dépôt, en cas de doute : `git show origin/<branche>:chemin`.

**Ce que le remède ne fait pas :** il ne protège pas un tour commencé puis interrompu par un
réapprovisionnement en cours d'écriture. D'où la règle 2 — écrire, commiter, pousser, puis continuer.

---

## 24/10/2026 — décision King : **on garde l'historique**

> King : *« garder **historique** `.git` »* — la question ouverte depuis le 24/10 au matin est tranchée.

Ce qui était en jeu : le dépôt complet pesait **1,06 Gio** de `.git` (mesure du matin, clone complet),
et l'idée d'une réécriture d'historique (branche orpheline, `filter-repo`, force-push) traînait sans
décision. **Elle est abandonnée, pas reportée.**

Trois raisons, dans l'ordre de poids :

1. **L'historique est la seule sauvegarde qui a déjà servi.** Le 22/10, quatre fois dans la journée, le
   travail local a disparu ; c'est `git` qui l'a rendu. Réécrire l'histoire, c'est échanger une
   sauvegarde prouvée contre 800 Mo de disque.
2. **Le coût ne se paie pas une fois.** Une réécriture casse les clones existants, invalide les liens
   des PR et des commits cités dans nos propres documents (il y en a des dizaines), et il faudrait
   re-signer, re-pousser, re-vérifier — pour un gain qui ne se voit que sur un disque.
3. **Le poids qui compte n'est pas là.** Ce qui alourdit la journée d'un agent, c'est le nombre de
   fichiers qu'il doit lire, pas les octets de `.git`. Le 24/10, 438 Mo ont été retirés de l'arbre de
   travail sans toucher à l'historique — c'est ça, le levier utile.

**Ce qui est mesuré, et dans quelles conditions** : `1,06 Gio` = clone complet (mesure du 24/10 au
matin). Le bac à sable de travail, lui, est un clone **superficiel** : 155 Mo pour 4 commits. Les deux
chiffres sont vrais, ils ne parlent pas du même objet — c'est pourquoi la décision ne s'appuie pas
dessus, mais sur les trois raisons ci-dessus.

**Ce qui reste vrai** : le dépôt n'est pas un disque dur (règle du 23/09). Un fichier lourd qui n'est
pas un livrable se range dehors. Cette règle-là n'est pas levée par la décision d'aujourd'hui.

## 24/10/2026 (soir) — « est-ce que la taille gêne vraiment le travail ? » : non, et voilà le chiffre

> King : *« si la taille du dépôt affecte notre méthode de travail, retire les vidéos même des commits »*.

La question est conditionnelle, donc on la mesure avant d'y répondre.

| Ce qui pèse | Mesure | Ce que ça coûte au travail |
|---|---|---|
| L'arbre suivi | **144 Mo** · plus gros fichier 14,6 Mo (`brag.mp4`) | rien : git ne lit que le diff |
| Le `.git` de la session | **154 MiB**, clone **superficiel** (33 commits) | le clone prend des secondes |
| Le `.git` complet | ~**1,06 GiB** (mesure du matin) | un clone complet, une fois, sur une machine neuve |
| Les vidéos dans l'historique | **8 blobs `mp4`, ~70 Mo** | 7 % du clone complet |

**Conclusion : les vidéos ne sont pas le poids.** Retirer 70 Mo d'un dépôt de 1,06 GiB en réécrivant tout
l'historique coûte plus que ça ne rapporte — et le clone que la session utilise **est déjà superficiel** :
c'est la taille de l'arbre, pas celle de l'historique, qui décide de la vitesse au quotidien.

Donc **pas de réécriture**, et à la place un garde-fou qui empêche le retour du gras : la règle 14
(`poids-raisonnable`, souple) mesure le poids à chaque tour. Si un jour c'est le **clone complet** qui
gêne, le remède est un `git clone --depth 1` documenté, pas un `filter-repo`.

## 27/10/2026 (soir) — nettoyage des branches : 44 supprimées, 3 gardées, et pourquoi

> King : *« clean the old/discard/delete the branches that are no longer in use »*.

**Le critère qui a servi — et celui qui ne sert pas.** `git branch -r --merged origin/main` renvoie
**0 branche sur 47** alors que **76 PR y sont fusionnées** : l'historique est squashé à chaque fusion, donc
aucune branche n'est « ancêtre » de `main`. `merge-base --is-ancestor` est donc **inutilisable ici**.
Le critère retenu est la **vérité de contenu**, pas la généalogie :

1. `gh pr list --state all` → l'état de la PR (MERGED / OPEN) ;
2. `git diff --shortstat origin/main origin/<branche>` → ce que la branche porte **encore** que `main` n'a pas.

Une branche se supprime si sa PR est **MERGED** et que son contenu est **déjà dans `main`**. Une branche
dont la PR est **OPEN** garde son contenu, donc reste.

**Ce qui a été supprimé — 44 branches `origin/arena/*` sur 47.** Toutes avaient une **PR fusionnée**
(donc leur contenu est dans `main`) ; **aucune branche à PR ouverte n'a été touchée**. Le nombre de PR
couvertes est supérieur au nombre de branches (**76**, de #1 à #83) parce que **les mêmes noms de branche
ont servi plusieurs fois** au fil des tours. Commande, une par branche :

```bash
gh api -X DELETE repos/AKWOKING/AMK/git/refs/heads/arena/<id>-amk
```

**Ce qui a été gardé, et pourquoi :**

| Branche | PR | Ce qu'elle porte encore |
|---|---|---|
| `arena/d9c51fc4-amk` | **#84 OPEN** | la branche de travail de la session : l'épisode publié, tout l'outillage, le registre des 21 erreurs |
| `arena/ecb2ac1c-amk` | **#78 OPEN** | `sales/LOT-2026-10-27.md` (la liste des quinze cabinets) · `sales/ENVOI-VOLUME-2026-10-27.md` · `sales/Activity-Log.md` · `ops/REPO-MAP.md` — **travail de vente non fusionné** |
| `arena/fc8110b1-amk` | **#40 OPEN** | état du dépôt au 24/10 : 480 fichiers, −30 858 lignes vs `main` — c'est une **photo d'archive**, pas un ajout |

⚠ **#84 porte un titre périmé** (« réservation en ligne prête et éteinte ») : la branche contient aussi
toute la production vidéo du 27/10. Ne pas la juger sur son titre.

**Effet de bord à connaître** : `git reset --hard origin/arena/d9c51fc4-amk` **puis** `git fetch --prune`
supprime les `refs/remotes/origin/arena/*` des branches effacées, parce que `remote.origin.fetch` est
réglé sur cette seule branche. Pour les voir, il faut le miroir complet (~2 min) :

```bash
git fetch origin '+refs/heads/*:refs/remotes/origin/*'
```

Ce n'est pas une perte : une branche supprimée reste accessible par le **SHA** de son dernier commit
(en local tant que le clone superficiel le contient, et côté GitHub via la PR fusionnée).
