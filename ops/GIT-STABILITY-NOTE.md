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
