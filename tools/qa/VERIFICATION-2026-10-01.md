# VÉRIFICATION — état réel des contrôles du dépôt (1 Oct 2026)

> **Pourquoi ce fichier existe.** Un bac neuf (clone propre de `main`, commit `c1efdee`) a été monté et
> **tous les contrôles du dépôt ont été exécutés**, pas lus. Ce rapport écrit ce qui est vert, ce qui ne
> tourne pas, et **ce qu'il a fallu installer pour que ça tourne** — parce que trois contrôles sur
> quatorze échouaient pour une raison d'environnement et non de code, et que rien dans le dépôt ne le
> disait au même endroit. Règle appliquée : `AMK-DESIGN-SKILLS.md` §18.3 (« l'état vit dans les
> fichiers ») et §27.5 (« un contrôle automatique ment dans les deux sens — donc on le teste aussi »).
>
> **Ce que ce rapport ne fait PAS :** il ne tranche rien de lui-même. Le §3 a été **résolu sur décision
> explicite de King** le 1/10 (voir le bandeau en tête du §3) ; le §5 reste **écrit, pas
> corrigé** — la maison dit que le jugement reste humain (`leads/build/guard.py`, « ce que cette machine
> NE fait pas »).

---

## 1 · L'environnement : ce qui manque sur un bac neuf (vérifié en l'installant)

Un clone propre ne tourne pas tel quel. Voici **exactement** ce qui a dû être ajouté, et ce qui ne
sert à rien :

| Dépendance | Nécessaire à | État sur bac neuf | Commande qui l'installe |
|---|---|---|---|
| `openpyxl` 3.1.5 | `leads/build/crm.py` (lit `leads_50.xlsx`) | **absent** — le script sort avec `sys.exit("openpyxl manquant…")` | `pip3 install --break-system-packages openpyxl` |
| `Pillow` 12.3.0 | `tools/site/md_to_pdf.py` → `test_md_to_pdf.py` | **absent** — `ModuleNotFoundError: No module named 'PIL'` | `pip3 install --break-system-packages Pillow` |
| `jsdom` (dans `/tmp/amk-video`) | `tools/qa/test_site_a11y_behaviour.mjs` | **absent** — `Cannot find module '/tmp/amk-video/node_modules/jsdom'` | `cd /tmp/amk-video && npm i jsdom` (prérequis déjà écrit dans l'en-tête du test) |
| `puppeteer-core` + `@sparticuz/chromium` | `tools/qa/test_voice_widget.mjs`, `tools/video/*` | **absent** | `bash tools/video/install.sh` (~70 Mo hors dépôt) — **a fonctionné ici**, moteur vérifié (110 images, 3,7 s) |
| `pytest` | — | **inutile** : les 14 tests sont des scripts autonomes (`python3 <fichier>`, rc=1 si échec), pas des tests pytest | — |
| `playwright` | `content/studio/test.py`, `…/source/capture.py` | **paquet pip OK le 1/10**, mais son `install chromium` meurt sur `cdn.playwright.dev` (bloqué) → pointé sur `/tmp/chromium` d'@sparticuz via `AMK_CHROMIUM_EXEC` (§5.3) | `pip3 install --user --break-system-packages playwright` + `bash tools/video/install.sh` |

Deux variables d'environnement ne survivent pas au redémarrage (déjà documenté dans
`tools/video/README.md`, rappelé ici parce que `test_voice_widget.mjs` en dépend) :

```bash
export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib
export FONTCONFIG_PATH=/tmp/amk-video/fonts
```

⚠️ **Les paquets Python non plus — vérifié deux fois le 1/10.** `openpyxl` et `Pillow` installés au
premier tour avaient **disparu** au tour suivant ; `crm.py` est donc ressorti en
`openpyxl manquant` au milieu d'un `rebuild.sh`. Ce n'est pas un défaut du dépôt, c'est le bac — mais
il faut le savoir : **un `rebuild.sh` qui échoue sur `openpyxl manquant` n'annonce pas un CRM cassé.**
Au passage, le garde-fou de `rebuild.sh` a fait exactement son travail : il a nommé l'échec, écrit
« RIEN n'a été écrit » et refusé de laisser lire les vues. Une fois `openpyxl` réinstallé, le même
`rebuild.sh` est passé à **rc=0, zéro marqueur `✗`**, `leads/CRM.csv` inchangé au octet près.

---

## 2 · Les tests : 14 sur 14 verts *(13 à la première passe ; `test.py` rejoint le vert après
l'installation de Playwright, §5.3)*

Les quatorze fichiers de test du dépôt (`find -name 'test_*.py' -o -name 'test_*.mjs' -o -name 'test.py'`)
ont été lancés un par un. **Aucun n'a été réécrit** : ce sont les contrôles du dépôt qui ont jugé, pas
un substitut.

| Contrôle | rc | Ce qu'il a dit |
|---|---|---|
| `tools/qa/test_audit_a11y.py` | 0 | « le contrôle refuse les dix-huit défauts, et il ne mord plus à côté » |
| `tools/qa/test_audit_hero.py` | 0 | « refuse ce qu'il doit refuser (dont les cinq règles du lot [29]) » |
| `tools/qa/test_audit_images.py` | 0 | **17 assertion(s) verte(s), 0 échec(s)** — « mord sur les onze pièges » |
| `tools/qa/test_audit_aeo.py` | 0 | « refuse les quatre pièges du lot [31] et ne mord pas sur les pages saines » |
| `tools/qa/test_md_to_pdf.py` | 0 | **50 assertion(s) passent, 0 échouent** (dont tous les `Send-*`, `RDV-*`, `BUSINESS-CASE*` de `sales/`) |
| `tools/outreach/test_scan_reviews.py` | 0 | **12 assertion(s) verte(s), 0 échec(s)** — « il refuse de mordre là où il n'y a rien » |
| `tools/qa/test_unilabo_page.mjs` | 0 | « Tout est vert. » |
| `tools/qa/test_cavisa_page.mjs` | 0 | « Tout est vert. » |
| `tools/qa/test_cinqsens_page.mjs` | 0 | « ✓ toutes les assertions passent » |
| `tools/qa/test_dmoptic_page.mjs` | 0 | « ✓ toutes les assertions passent » |
| `tools/qa/test_laligne_page.mjs` | 0 | « ✓ toutes les assertions passent » |
| `tools/qa/test_site_a11y_behaviour.mjs` | 0 | « les états d'accessibilité du site sont réels à l'exécution » (20 boutons, aucun sans nom) |
| `tools/qa/test_voice_widget.mjs` | 0 | « ✅ TOUT PASSE » — **dans un vrai Chromium**, mobile 390×844, zéro erreur JS |
| `content/studio/test.py` | **0 depuis le 1/10** | « Interaction checks passed. JS errors: [] » — premier run réel après installation de
Playwright (§5.3) ; à la première passe il était **non lancé** (pas de Playwright). Ajouté ici quand il
est passé au vert. |
| `content/studio/test.py` | **non lancé** | voir §5 |

`test_site_a11y_behaviour.mjs` lit `SITE_FILE`, défaut `/home/user/AMK/site/index.html` : c'est bien la
page du dépôt qui a été exécutée dans jsdom, pas une copie.

---

## 3 · LE VERROU DU CRM ÉTAIT PÉRIMÉ — **RÉSOLU le 1/10 sur décision de King**

> ✅ **RÉSOLU le 1/10/2026.** Le constat qui suit est **conservé tel quel**
> (règle de `PRE-FLIGHT.md` §4 : on annote, on n'efface pas) parce qu'il décrit un état que n'importe
> quel clone antérieur à ce commit reproduira.
>
> **Ce qui a été fait :** `python3 leads/build/guard.py lock` sur décision explicite de King
> (« re-lock the guard »). Le verrou porte maintenant `crm.py = f0ff55f939970e80`, et son champ `why`
> nomme la décision, la date et les preuves — ce champ existe pour ça.
>
> ⚠️ **Il a fallu le rejouer une DEUXIÈME fois le même jour, et c'est une leçon.** La première
> écriture du verrou **n'a pas survécu au redémarrage du bac** : au tour suivant,
> `generators.lock.json` était revenu à sa valeur versionnée (ancienne empreinte, ancien `why`), alors
> que les fichiers **non suivis** (comme ce rapport) avaient survécu. Autrement dit : **une
> modification de fichier suivi, non committée, peut disparaître entre deux tours.** J'avais annoncé
> « le verrou est rejoué, rc=0 » — c'était vrai au moment où je l'ai mesuré, et ce n'était **pas
> durable**. Depuis, le verrou est **committé** sur la branche de session : c'est la seule façon dont
> il tient. À retenir pour tout ce qui doit survivre dans ce dépôt.
>
> **Ce qui a été vérifié après, et c'est ça le vrai contrôle :**
>
> | Contrôle | Avant | Après |
> |---|---|---|
> | `python3 leads/build/guard.py check` | **rc=1**, 5 lignes d'alerte | **rc=0**, silencieux |
> | `bash leads/build/rebuild.sh` **sans** `AMK_GUARD_OK` | **refusait d'écrire** | **rc=0**, zéro marqueur `✗` |
> | `md5 leads/CRM.csv` | `4a1e77f30dd5598eb3e8e78d304eef96` | **identique** — la source n'a pas bougé |
>
> Le mur décrit ci-dessous n'existe plus : la ligne « CRM / pipeline » de la table de routage mène de
> nouveau à un `rebuild.sh` qui tourne. Les 91 fichiers datés que ce rebuild a rafraîchis ont été
> **remis à l'état committé** (`git checkout`), le rafraîchissement de pipeline n'ayant pas été demandé ;
> seul `generators.lock.json` reste modifié.
>
> ⚠️ **Un piège attrapé au passage, à retenir.** Lancé en `bash leads/build/rebuild.sh | head -12`, le
> script affiche **rc=141** — c'est `SIGPIPE` (128+13) causé par `head` qui ferme le tuyau, **pas** un
> échec du builder. C'est mot pour mot l'accident que décrit l'en-tête de `rebuild.sh` (le code de
> retour de `grep` pris pour celui du générateur, 21/09). Le vrai code, obtenu sans tuyau, est **0**.
> **Ne jamais lire le rc d'un générateur au travers d'un `| head` ou `| grep`.**

**Le fait, mesuré (état d'origine, avant résolution).** Sur l'arbre propre (`git status` vide),
`python3 leads/build/guard.py check` sortait **rc=1** :

```
✗ GARDE-FOU : un ou plusieurs GÉNÉRATEURS DU CRM ne correspondent plus au verrou validé
    leads/build/crm.py
        1f5a10770afaac81 → f0ff55f939970e80 · IDENTIQUE à HEAD mais différent du verrou
```

- `generators.lock.json` annonce `crm.py = 1f5a10770afaac81`.
- Le `crm.py` **committé** pèse `f0ff55f939970e80` (sha256 tronqué, recalculé ici).
- `git diff HEAD -- leads/build/` est **vide** : ce n'est la plume de personne, c'est le verrou qui est
  en retard sur le fichier versionné. Les quatre autres générateurs (`views.py`, `records.py`,
  `rebuild.sh`, `guard.py`) correspondent.

**Conséquence concrète :** la ligne « CRM / pipeline » de la table de routage de `PRE-FLIGHT.md` mène à
`leads/build/rebuild.sh`, et ce script **s'arrête avant d'écrire quoi que ce soit**. Quiconque reprend
ce dépôt tombe sur un mur dès la première tâche CRM.

**Ce que ce n'est PAS (vérifié, et c'est rassurant) : une régression de données.** Lancé avec
l'échappatoire assumée du garde-fou (`AMK_GUARD_OK=1 bash leads/build/rebuild.sh`), le générateur
committé reproduit le CSV committé **au octet près** :

| | Avant | Après |
|---|---|---|
| `md5 leads/CRM.csv` | `4a1e77f30dd5598eb3e8e78d304eef96` | `4a1e77f30dd5598eb3e8e78d304eef96` — **identique** |
| Sortie du builder | — | 163 lignes × 52 colonnes · 85 fiches · 5 vues + 1 plan |

91 fichiers ont bougé au passage, **tous générés** : les en-têtes « Généré le 2026-09-27 » devenus
« 2026-10-01 », et — comportement voulu — le **réordonnancement du plan du jour** qui dépend de la date
(`rythme M+2 (message il y a 3 j)` → `7 j`, DM Optique remonté dans « Répondre d'abord »). La source
n'a pas bougé ; seules les vues datées ont bougé. **Tout a été remis à l'état committé** (`git checkout
-- leads/`), l'arbre est redevenu propre : ce rapport ne livre pas un rafraîchissement de pipeline qui
n'a pas été demandé.

**La décision, et comment elle a été prise.** `guard.py` le dit lui-même : *« elle ne
prouve pas que la nouvelle version est meilleure, elle prouve qu'elle est différente de ce qui a été
validé. Le jugement reste humain. »* Le dépôt est un clone **peu profond** (`.git/shallow` présent, 1
commit) : l'historique ne permet pas de dater le verrou par rapport au fichier. Les deux issues étaient :

- si le `crm.py` versionné **est** la version voulue → `python3 leads/build/guard.py lock` ;
- s'il ne l'est **pas** → le verrou a raison d'aboyer et il faut retrouver la bonne version.

**King a tranché la première le 1/10** (« re-lock the guard ») ; le verrou a été rejoué, puis le
contrôle et le rebuild sans échappatoire ont été relancés (tableau en haut de section). Ce qui a
permis de trancher sans risque : le générateur versionné reproduit le CSV versionné au octet près,
donc reverrouiller ne valide pas une version qui aurait perdu de l'état.

---

## 4 · Les portes de livraison, passées sur TOUTES les pages

Les trois contrôles obligatoires de `PRE-FLIGHT.md` §1b (`audit_html.py`, `audit_a11y.py --strict`,
`audit_images.py`) ont été lancés sur les **41 pages** du dépôt (`demos/`, `site/`,
`hosting/previews/*/index.html`).

**27 passaient les trois portes · 14 échouaient** à la première mesure. Après correction des deux
vignettes (§5b, même jour) : **29 passent · 12 échouent.**

> ⚠️ **Correction d'une erreur qui était dans la première version de ce rapport.** J'y écrivais que les
> deux pages `creation-site-web-*` échouaient sur **la même vignette** (`img/clinic.png`). **C'est faux.**
> Relu image par image : la page « clinique » échouait sur `img/clinic.png` (**405 Ko**), la page
> « école » sur **`img/crestwood.png` (626 Ko)** — elle ne référence même pas `clinic.png`. J'avais
> recopié la première ligne sans lire la seconde. Les deux sont corrigées (§5b).

**Les sept fils chauds et la page de l'agence passent tous les trois :**

| Page | html | a11y | images |
|---|---|---|---|
| `demos/concept-dmoptic-v1.html` | ✅ | ✅ | ✅ |
| `demos/concept-cavisa-v1.html` | ✅ | ✅ | ✅ |
| `demos/concept-cinqsens-v1.html` | ✅ | ✅ | ✅ |
| `demos/concept-laligne-v1.html` | ✅ | ✅ | ✅ |
| `demos/concept-unilabo-v2.html` | ✅ | ✅ | ✅ |
| `demos/concept-univers-optique-v2.html` | ✅ | ✅ | ✅ |
| `demos/concept-le-cristallin-v1.html` | ✅ | ✅ | ✅ |
| `site/index.html` | ✅ | ✅ | ✅ |

**Les 14 en échec** (codes de retour `html`/`a11y`/`images`) :

| Page | codes | Nature (lue dans la sortie, pas supposée) |
|---|---|---|
| `site/sample-school.html` | 1/1/0 | 12 constats confirmés (desktop **et** mobile) |
| `site/sample-nursery.html` | 1/1/0 | idem, famille « écoles » d'avant les portes |
| `site/sample-secondary.html` | 1/0/0 | — |
| `site/clinic-bonaberi.html` | 1/0/0 | 2 constats confirmés |
| `site/mitoc.html` | 1/0/0 | — |
| `site/mockup-hero.html` | 1/0/1 | — |
| `site/creation-site-web-clinique-cameroun.html` | 0/0/1 → **0/0/0** | `img/clinic.png` **405 Ko** pour un budget de 400 Ko · **CORRIGÉ §5b → 262 Ko** |
| `site/creation-site-web-ecole-cameroun.html` | 0/0/1 → **0/0/0** | **`img/crestwood.png` 626 Ko** (et non `clinic.png`, voir la correction ci-dessus) · **CORRIGÉ §5b → 347 Ko** |
| `demos/concept-oracare-v2.html` | 1/1/0 | démo du 14/09, antérieure aux portes |
| `demos/concept-oracare-v3.html` | 0/1/0 | — |
| `demos/concept-skye-v1.html` | 1/1/0 | `AUDIT-2026-09-17.md` §2 laissait déjà « 2 libellés à 4,2:1 » |
| `demos/concept-yaks-v1.html` | 1/1/1 | — |
| `hosting/previews/skye/index.html` | 1/1/0 | copie du concept Skye |
| `hosting/previews/yaks/index.html` | 1/1/1 | copie du concept YAKS |

**Lecture honnête :** aucune des pages **en conversation** n'est en faute. Ce qui reste en échec sont des
échantillons « sans nom » et des démos de la première quinzaine de septembre, c'est-à-dire **antérieures**
aux portes — `clients/_uniqueness-registry.md` le dit déjà des écoles (« elles précèdent la porte
d'exploration de direction §19 »). Les deux seules pages **publiques et indexables** qui échouaient
(`creation-site-web-*`) passent désormais les trois portes (§5b) : il ne reste plus aucun écart sur une
page servie au public. À noter : l'écart n'était pas « de 5 Ko » comme je l'avais écrit d'abord — 5 Ko
pour `clinic.png`, **226 Ko** pour `crestwood.png`.

**Les portes plus récentes, sur `site/index.html`** (§22.5, §26, §31) :

| Contrôle | Verdict |
|---|---|
| `audit_hero.py` | ✅ 0 faute, 0 avertissement — « h1 dans le premier écran · premier écran porté par le texte · accordéons natifs » |
| `audit_aeo.py` | ✅ 0 faute, 0 avertissement |
| `audit_page.py` | OK (rc=0), **1 constat non bloquant** : « 27 tailles de texte distinctes — au-delà de 6 sur un site vitrine, la hiérarchie se dissout » |

---

## 5 · Les quatre chemins d'avant le déménagement — **RÉPARÉS le 1/10**

> ✅ **RÉSOLU le 1/10/2026.** Le constat d'origine est conservé plus bas (règle §4 : on annote, on
> n'efface pas). Réparer ces chemins a fait apparaître **deux dérives générateur ↔ artefact** qui
> comptaient plus que les chemins eux-mêmes.

**Les quatre scripts ont été repointés** (`py_compile` OK sur les quatre, plus aucune occurrence des
anciens chemins hors mes commentaires) :

| Script | Ancien chemin | Devenu |
|---|---|---|
| `content/studio/create.py` | `/home/user/website-demo` | `Path(__file__).resolve().parent` |
| `content/studio/test.py` | `/home/user/website-demo` | idem ; les captures de contrôle sortent dans `AMK_STUDIO_WORK` (défaut `/tmp`), pas dans le dépôt |
| `…/source/capture.py` | `/home/user/website-demo` + `/home/user/video4_asset` | `S` = `content/studio` (dans le dépôt) · `P` = `AMK_V04_WORK` (défaut `/tmp/amk-v04`, ~170 captures hors dépôt) |
| `…/source/render.py` | 5 chemins, dont `ffpath.txt` écrit à la main | `FF` = `imageio_ffmpeg.get_ffmpeg_exe()` · polices = `content/assets/fonts` · image d'accroche = `content/assets/host/s1_hook.png` · audio = `…/v04-before-whatsapp/source/` |

### 5.1 · La dérive que la réparation a débusquée : `create.py` faisait **régresser** une correction d'accessibilité

Relancé tel quel, `create.py` réécrivait `after.html` avec des verts **plus clairs** que le fichier
versionné. Le fichier **livré** avait été corrigé à la main pour le contraste, sans que la correction
revienne dans le générateur. Mesuré en WCAG, sur le fond réel de chaque élément :

| Élément | ce que générait `create.py` | le fichier **livré** |
|---|---|---|
| `.brand span` | `#8dba72` **2,23:1 — ÉCHEC** | `#6d9553` 3,46:1 |
| `.eyebrow` | `#51785c` 4,82:1 | `#4b7055` 5,39:1 |
| `.card .number` | `#76a16d` **2,96:1 — ÉCHEC** | `#6b9460` 3,48:1 |
| `.checks li:before` ✓ | `#4d875d` 4,25:1 | `#467c54` **4,92:1 — passe 4,5:1** |

plus une règle `footer p{color:#e3eadd}` qui n'existait **que** dans le fichier livré.

**Le fichier livré gagne, et c'est maintenant celui du générateur** (règle M7 : la source est le
générateur). Preuve, et c'est le seul contrôle qui vaille :

```
md5 committed  after.html : 2f1d8d2ab8d73a5ccaff3f908fffcc5e
python3 content/studio/create.py            → rc=0
md5 regenerated after.html : 2f1d8d2ab8d73a5ccaff3f908fffcc5e   ← identique au octet près
```

Sans ce pliage, **relancer le constructeur aurait effacé silencieusement une correction
d'accessibilité** — exactement la famille d'accident que le garde-fou du CRM (`guard.py`) existe pour
empêcher, mais ici sans aucun garde-fou.

### 5.2 · Seconde dérive : le studio embarquait la **vieille** page

`Website_Demo_Studio.html` versionné embarquait `after.html` en JSON. Vérifié : il contenait
`#8dba72` (l'ancienne teinte) et **pas** la règle `footer p` — alors que le fichier `after.html`
posé à côté portait la version corrigée. **Le studio — l'asset qui sert aux vidéos — était en retard
sur la page qu'il montre.** Régénéré, il embarque désormais la version corrigée, vérifié :

```
#8dba72 (ancienne) : 0   ·  #6d9553 (corrigée) : 1   ·  footer p : 1
le JSON embarqué se parse  ·  embedded after.html == fichier after.html : True
```

### 5.3 · Playwright — installé le 1/10 ; `test.py` et `capture.py` tournent **en vrai**

- **Le CDN de Playwright est bloqué ici** — vérifié, pas supposé : `python3 -m playwright install
  chromium` meurt en `ECONNRESET` sur `cdn.playwright.dev` (c'est le constat que portait déjà
  `tools/video/install.sh` : « les CDN de navigateurs sont bloqués dans la sandbox »). Le paquet pip
  `playwright` s'installe, lui, sans problème.
- **Solution :** pointer Playwright sur le binaire **embarqué** d'`@sparticuz/chromium` (celui de la
  chaîne vidéo, qui ne télécharge rien). `bash tools/video/install.sh` le restaure ;
  `chromium.executablePath()` donne `/tmp/chromium`. Les deux scripts ont gagné une variable
  d'environnement additive `AMK_CHROMIUM_EXEC` : si elle est présente, elle passe en
  `executable_path` (+ `--disable-dev-shm-usage --disable-gpu --no-zygote --single-process`) ; **sans
  elle, comportement inchangé**. C'est la même convention que `AMK_VIDEO_RUNTIME` / `AMK_GUARD_OK`.
- **Vérifié, et c'est le point :** avec `AMK_CHROMIUM_EXEC=/tmp/chromium` + `LD_LIBRARY_PATH` +
  `FONTCONFIG_PATH`, `content/studio/test.py` passe pour la première fois — « Interaction checks
  passed. JS errors: [] », rc=0 — et `capture.py` produit **175 captures** rc=0. J'ai regardé la
  capture du studio rendue par ce vrai Chromium : la coquille AMK, le toggle Before/After, et la page
  « before » avec son débordement horizontal **voulu** — c'est bien le rendu attendu. **Résultat :
  les 14 fichiers de test du dépôt passent tous (14/14).**

### 5.4 · Ce qui reste bloqué, et pourquoi (non masqué)

- **`render.py` ne peut pas aller au bout ici** : `narration.mp3` et `cta.mp3` ne sont **pas dans le
  dépôt** — `.gitignore` exclut `*.mp3` et seule la vidéo 06 est exemptée ; King les garde hors du
  dépôt (règle du 23/09). Le script **s'arrête maintenant proprement** en nommant les deux fichiers
  et leur dossier, au lieu d'un traceback au milieu du rendu — vérifié : rc=1, message explicite.
  C'est aussi ce qui prouve que l'import `imageio_ffmpeg` et la résolution des chemins fonctionnent.
  **La partie Playwright de la chaîne (capture.py) tourne désormais ; seul l'audio manque.**
- **Nouveau, trouvé en route :** `hosting/samples/` est un **instantané périmé** de `site/` — il lui
  manque `creation-site-web-clinique/ecole`, `assets/`, `mockup-hero.html` et les jumeaux `.jpg`, et
  son `index.html` et son `sitemap.xml` diffèrent. Je ne l'ai **pas** régénéré : `build_samples.py` est
  un `copytree` intégral, le relancer aurait amené bien plus que les vignettes. **À trancher.**
  Corollaire : ce `copytree` copie aussi les constructeurs, et `hosting/samples/img/make_og.py`
  (identique au octet près à `site/img/make_og.py`) y calcule `FONTS = hosting/tools/record/fonts` —
  **inexistant**. Un constructeur copié hors de `site/` perd ses chemins relatifs.

**Constat d'origine, conservé :** `content/studio/test.py` ne pouvait pas tourner, pour deux raisons
distinctes — Playwright absent (`CONTENT-PIPELINE.md` §B le savait) **et** un chemin d'avant le
déménagement, `P=Path('/home/user/website-demo')`, vérifié absent. Même défaut dans
`create.py`, `capture.py` et `render.py` ; seul `render.py` était signalé quelque part.

---

## 5b · Les deux vignettes hors budget — **RÉPARÉES le 1/10**

Deux pages **publiques et indexables** échouaient à la porte `audit_images.py` (§4). Correction par un
constructeur, `site/img/process_thumbs.py` (même famille que `process_secondary.py` et
`process_mitoc.py`), parce qu'une obligation sans machine derrière n'est qu'une opinion.

| Vignette | Avant | Après | Page |
|---|---|---|---|
| `site/img/clinic.png` | 1280×800 · **405 Ko** | 800×500 · **262 Ko** | `creation-site-web-clinique-cameroun.html` |
| `site/img/crestwood.png` | 1280×800 · **626 Ko** | 800×500 · **347 Ko** | `creation-site-web-ecole-cameroun.html` |

**Pourquoi 800×500, mesuré et non deviné.** Elles s'affichent en `.proof img{aspect-ratio:16/10;
width:100%}` dans une grille de 3 colonnes sous `.wrap{max-width:1160px}` → **~358 px CSS**, soit
~716 px en 2× DPR : 800 px couvre le retina, les 1280 px ne servaient à rien. Redimensionnement
LANCZOS + **PNG sans perte**, **aucune quantification de palette** (elle ferait tomber crestwood à
144 Ko mais ajoute du dither sur le petit texte). Écart au rendu réel, mesuré à 358 px :
**≤ 0,26/255** en moyenne. 900 px sans perte ne suffisait pas (crestwood restait à 427 Ko).

**Vérifié :**

```
python3 site/img/process_thumbs.py                 → rc=0, les deux sous budget
audit_images.py creation-site-web-clinique-…html    → 0 faute (rc=0)
audit_images.py creation-site-web-ecole-…html       → 0 faute (rc=0)
les trois portes sur les deux pages                 → 0/0/0 PASS
relancer le script                                  → « déjà 800×500 — rien à faire » (idempotent)
site/img/*.png  ==  hosting/samples/img/*.png       → identiques au octet près
```

**Les deux copies ont été écrites** : `hosting/samples/img/` est l'instantané déployable, ne pas
l'écrire aurait fait diverger le bundle et la source en silence.

**Conséquence enchaînée :** `site/img/og-cover.jpg` embarque ces deux vignettes (`make_og.py`), il a
donc été **régénéré** (105 937 → 106 089 o, toujours 1200×630) puis recopié dans
`hosting/samples/img/`. Le constructeur `hosting/build_site_zip.py` tourne toujours (rc=0, 14 fichiers).

**Volontairement non touchées :** `littleoaks.png` (219 Ko) et `nova.png` (232 Ko) passent la porte ;
les réduire n'était pas demandé.

**Ce que ce contrôle ne prouve pas :** la **beauté**. `audit_images.py` le dit lui-même — il porte sur
la structure et la vie privée, jamais sur l'image. Un redimensionnement 1280 → 800 se juge à l'œil, sur
téléphone : c'est le regard de King, pas le mien. Les originaux sont dans git.

---

## 6 · Reproductibilité du constructeur (vérifiée, pas supposée)

Le chemin de production d'un aperçu est `gabarit + build_*.py → concept HTML + bundle`. Testé sur
`demos/build_cavisa.py`, le plus récent :

```
md5 avant  : 3bfbdf82b51e9412c933b8c292fe2b10   demos/concept-cavisa-v1.html
build rc=0 : « les deux copies sont identiques : True » (page 216 Ko + bundle + og.jpg 120 Ko)
md5 après  : 3bfbdf82b51e9412c933b8c292fe2b10   — identique
git status : vide
```

Relancer le constructeur ne change **rien** : la page committée est bien celle que le gabarit produit.
C'est ce qui rend le `§20.7` (coller l'URL réelle dans `og:url`/`og:image` puis **relancer** le
constructeur) sans danger.

---

## 7 · Ce que ce rapport ne prouve pas

- **Aucun goût.** Les portes vérifient structure, contraste, accessibilité, images, hero, AEO. Elles ne
  jugent pas une page — `audit_hero.py` le dit en sortie (« le GOÛT, la hiérarchie visuelle réelle, et
  l'effet d'un regard… demandent un œil »).
- **Aucun déploiement.** Rien n'a été mis en ligne, aucun jeton Vercel ici : le `deploy gate` de
  `hosting/previews/README.md` (« Not verified on a phone = not sent ») reste à faire **par King, sur
  un téléphone**, et le **gel** du Cristallin et d'Univers Optique (23/09) n'a pas été touché — leurs
  fichiers n'ont été ni modifiés ni reconstruits.
- **Aucun envoi.** Aucun message n'a été rédigé ni expédié ; les trois portes de `RESEARCH-STANDARD.md`
  §8b et le contrôle approfondi §8c n'ont donc pas eu à être passés.
- **Le reverrouillage du §3 ne prouve pas que `crm.py` est « meilleur ».** `guard.py` le dit : le verrou
  atteste qu'une version a été **validée par un humain**, pas qu'elle est bonne. Ce qui rend celui-ci sûr
  est mesurable et mesuré : le générateur versionné reproduit le CSV versionné au octet près. Si un état
  de lead venait à manquer, la cause est dans `crm.py` ou `sales/Activity-Log.md` — **pas** dans le
  verrou, qui ne fera plus écran.
- **Rien n'a été régénéré pour de bon.** Le rebuild de vérification a bien tourné, puis les 91 fichiers
  datés ont été remis à l'état committé : les vues du dépôt portent toujours la date du **27/09**. Le
  prochain `rebuild.sh` légitime les rafraîchira, et c'est attendu.
- **`test.py` et `capture.py` tournent désormais en vrai** (§5.3) : 14/14 verts, « Interaction checks
  passed. JS errors: [] », 175 captures, et j'ai **regardé** la capture du studio rendue par le vrai
  Chromium. Mais ce vert dépend de `/tmp/chromium` + `/tmp/amk-video` (le binaire embarqué
  d'@sparticuz), qui **ne survivent pas au redémarrage du bac** : sans relancer
  `bash tools/video/install.sh` et sans `AMK_CHROMIUM_EXEC`, `test.py` retombe en échec. Le vert est
  réel **dans un bac préparé**, pas permanent.
- **`render.py` n'a pas rendu une seule image** (§5.3) : les deux pistes audio ne sont pas dans le
  dépôt. Ce qui est vérifié, c'est qu'il **s'arrête proprement** en les nommant — pas qu'il produit le
  clip.
- **`Website_Demo_Studio.html` a changé, et King ne l'a pas vue.** C'est un asset de 546 Ko, régénéré
  parce que son générateur et sa page source avaient dérivé (§5.2). Le changement visible : la page
  « after » à l'intérieur du studio porte désormais les verts corrigés et la couleur de pied de page.
  C'est cohérent et vérifié, mais **c'est un asset de contenu qui bouge** — `git checkout` le rend.
- **`hosting/samples/` reste périmé** (§5.3) : je n'ai pas relancé `build_samples.py`, qui aurait amené
  beaucoup plus que les vignettes. Le bundle déployable et `site/` divergent toujours.
- **La beauté des vignettes redimensionnées n'est pas jugée** (§5b) : 1280 → 800 px se regarde sur un
  téléphone, pas dans un rapport.
