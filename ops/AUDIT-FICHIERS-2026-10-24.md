# Audit des fichiers — 24/10/2026

> Ruling King : *« do a complete audit of the files removing those that are outdated or useless »*.
> Ce document dit **ce qui est parti**, **pourquoi**, **comment le récupérer**, et **ce qui reste gros
> sans être mort**. Il ne remplace pas `ops/FILE-AUDIT-2026-10-24.md` (généré par
> `tools/ops/audit_files.py`) : celui-là compte, celui-ci juge.

## 1 · Ce qui a été mesuré

| | Avant | Après | Écart |
|---|---|---|---|
| Fichiers suivis | 1 788 | 1 788 | ±0 (4 retirés, 4 ajoutés : machine + audit) |
| Poids de l'arbre suivi | 626,5 Mo | **560,1 Mo** | **−66,4 Mo** |
| Médias sans nom cité | 232 | 227 | −5 |
| Documents orphelins | 415 | 415 | inchangé (voir §5) |
| `.git` (historique) | 861 Mo → **1,06 Gio** | | **non touché** (voir §6) |

## 2 · La méthode — quatre preuves, pas d'intuition

Un fichier n'a été retiré que s'il satisfaisait **au moins deux** de ces quatre conditions :

1. **La règle du dépôt l'exclut déjà** : `.gitignore` l'ignore explicitement (`*.mp4` sauf cinq vidéos
   livrées nommées, `/amk-site*.zip`), et il est là parce qu'il est plus vieux que la règle.
2. **Le journal dit qu'il devait partir** : une entrée datée de `sales/Activity-Log.md` le déclare
   retiré, régénérable, ou renvoyé hors dépôt.
3. **Aucun document vivant ne le cite**, et aucun script ne le produit ou ne le lit.
4. **Un script le régénère** à l'identique (`hosting/build_site_zip.py`).

Contre-épreuve systématique : un `grep` de nom de fichier **dans les `.md` ne prouve rien** si le
fichier est lu par du code (les visuels de `demos/img/le-cristallin-*.png` sont inlinés en base64 par
`demos/build_le_cristallin.py` — ils sont restés). Et un fichier sans citation peut être une archive
volontaire (les 15 designs retirés le gardent leur empreinte dans `clients/_uniqueness-registry.md`).

## 3 · Retiré aujourd'hui — 4 fichiers, 66,4 Mo

| Fichier | Poids | Pourquoi il part | Récupération |
|---|---|---|---|
| `content/pipeline/POST-01-v4-TIKTOK.mp4` | **58,9 Mo** | artefact de build d'un post du 12–13/10 ; `*.mp4` est ignoré sauf les cinq vidéos **livrées** (`.gitignore`, exception nommée) ; `Activity-Log` ligne 5196 : « le MP4 local de 57 Mo est retiré » | `git show 907742f8:content/pipeline/POST-01-v4-TIKTOK.mp4 > /tmp/v4.mp4` |
| `amk-site.zip` | 5,2 Mo | `.gitignore` : « archives d'export : produites par un script, jamais versionnées » ; régénérable par `python3 hosting/build_site_zip.py` | `git show 907742f8:amk-site.zip > /tmp/amk-site.zip` |
| `content/pipeline/POST-01-BUG-LOGO-2026-10-12.mp4` | 3,8 Mo | MP4 de test d'un bug corrigé ; le document `TIKTOK-POST-01-BUG-LOGO.md` porte désormais la note datée du retrait | idem, `git show 907742f8:…` |
| `content/pipeline/POST-01-v3-TIKTOK-2026-10-13.mp4` | 1,8 Mo | brouillon (v3) remplacé par v4 dans la même semaine | idem |

**Rien n'est perdu.** Les quatre blobs restent dans l'historique : la commande `git show` ci-dessus les
rend à l'octet près. C'est la convention du dépôt depuis le 23/09 (« 71 Mo retirés, récupérables par
git si besoin »).

**Deux documents ont été mis à jour** pour ne pas laisser un pointeur mort : `content/pipeline/TIKTOK-POST-01-BUG-LOGO.md`
(note datée) et `hosting/build_site_zip.py` (dit que sa sortie n'est pas versionnée).

## 4 · Ce qui reste gros — et pourquoi ce n'est pas du gras

| Zone | Poids | Pourquoi ça reste |
|---|---|---|
| `clients/dm-optic/photoshoot/` | **395 Mo**, 168 fichiers | photos brutes du shooting client (PXL_*.jpg, 4–9 Mo pièce). **Origine du travail** : c'est de là que sortent les visuels du mois 1 et 2. Non supprimées — voir §6, la décision vous revient |
| Vidéos `clients/dm-optic/content/` | 52 Mo | **livrables suivis nommément** (exception `.gitignore` du 22/10 après « where is post 1 ?? ») : `spot-02`, `spot-03`, `etapes-01`, `ugc-03`, `tiktok-01-v2`, `brag.mp4` |
| `design/vendor/` | 12 Mo | skills tierces importées (taste, emil), nécessaires à `tools/taste-skill` |
| `hosting/previews/` | 20 Mo | trois sites déployés (`dmoptic`, `cristallin`, `labiomed`) — un aperçu déployé n'est pas une copie morte |
| `site/` + `hosting/samples/` | 19 Mo | le site AMK, et les pages d'exemple utilisées par les audits |
| `content/Avatar/` | 10 Mo | composites de l'avatar de marque, réutilisés par la chaîne vidéo |
| `mockups/` + `tryon-camera/` | 9 Mo | captures et prototypes (essai caméra) |

## 5 · Ce qui n'a **pas** été supprimé, exprès

- **415 documents orphelins** (aucune citation entrante). Ensemble : **1,9 Mo**. Les supprimer ne
  libérerait rien et détruirait la mémoire du dépôt (recherches, RDV, audits de septembre). Un orphelin
  se **cite** ou se **date**, il ne s'efface pas (règle `PRE-FLIGHT` §0h, 24/10).
- **37 documents marqués périmés** par la détection lexicale. Le marquage est une **piste**, pas une
  preuve (`REPO-MAP` §3) : plusieurs sont en réalité des règles vivantes dont l'en-tête parle d'une
  version antérieure. Aucun n'a été retiré sans lecture.
- **`clients/_uniqueness-registry.md`** et `_mockups/` : ce ne sont pas des dossiers clients, ils
  gardent les empreintes des 15 designs retirés le 24/10.
- **`amk-factures-pwa.zip` (v1)** : 0,1 Mo, cité comme archive de version dans `ops/FACTURATION` — le
  gain ne valait pas le pointeur cassé.
- **Proforma v1 et v2** (0,2 Mo chacun) : les deux sont citées dans `post-deposit-email.md`.

## 6 · Ce qui demande votre décision — et ce que je propose

**① Les photos brutes — 395 Mo, dont 286 Mo qu'aucun document ne nomme.** Elles sont dans l'historique :
les retirer de la tête n'allège pas un clone. Trois options :
- **garder** (statut actuel) : coût disque, zéro risque ;
- **garder la sélection** (les images réellement utilisées dans `month1`/`month2`), retirer les autres de
  la tête : ‑300 Mo sur l'arbre, récupérables par git ;
- **sortir tout le shooting** vers un stockage externe (Google Drive) et ne garder que la sélection.

**② L'historique — `.git` = 1,06 Gio.** C'est devenu le vrai poids du dépôt, et il ne se réduit pas par
`git rm` : il faut réécrire l'historique (`git filter-repo`) — opération **destructive, à fenêtre
fermée** (aucune PR ouverte, toutes les sessions arrêtées, sauvegarde complète avant). Je ne l'ai pas
faite. Elle demanderait ~30 min et ramènerait probablement le dépôt sous 250 Mo.

**③ `photoshoot` dans Git ou pas** : la règle du 23/09 dit « le dépôt n'est pas un disque dur » ; les
photos sont la seule exception qui n'a jamais été tranchée.

## 7 · Ce que l'audit a trouvé au passage

- **`tools/scrapling/install.sh` était cassé** : clone `--depth 1` puis `checkout fd53131` — le pin du
  20/10 n'est pas sur la pointe de branche, donc l'installation échouait depuis sa création. Réparé le
  24/10 (clone `--filter=blob:none`, toutes les refs) : `scrapling 0.5` s'installe, le skill est copié.
- **`provision.sh` n'existait pas** : 24 installateurs épinglés, aucune commande pour tous les rejouer.
  Il existe maintenant (`tools/ops/provision.sh`), **24/24 installés le 24/10**, estampes dans
  `~/.amk-provisioned/`.
- **`tools/graphify/ask.sh` exigeait le venv graphify** alors que `find.py` n'utilise que la
  bibliothèque standard, et renvoyait vers un script supprimé (`build_docs_graph.py`). Corrigé.
