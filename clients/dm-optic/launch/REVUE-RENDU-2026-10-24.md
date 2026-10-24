# Revue de rendu — DM OPTIQUE SARL · 24/10/2026

> **Ce que ce document est.** La page servie sur le banc Vercel a été **rendue pour de vrai**, dans
> Chromium, à 1440 et 390 px, puis mesurée. Ce qui suit ne compare pas du code à une intention : il
> compare **ce qui s'affiche** à ce que la fiche client et les portiques déclarent. Captures :
> `launch/revue-2026-10-24/` (4 images, 313 Ko).

## 0 · Ce qui a été lu avant d'écrire (règle §0f)

| Couche | Lus | Listés, non lus |
|---|---|---|
| Pré-vol | `PRE-FLIGHT.md` §0f, §0h, §0i, §1f③④⑪, §1b | §1g, §2, §5 (hors périmètre d'une revue de rendu) |
| Graphe | `tools/graphify/ask.sh` ×3, `ops/REPO-MAP.md` §1, §2 | §3, §3 bis |
| Skills | `tools/superpowers/skills/requesting-code-review` (gabarit de revue), `tools/pro-design/SKILL.md` §4 (boucle de vérification : 1440 + 390, débordement, texte coupé, contraste, images, erreurs console, focus) | `receiving-code-review`, `verification-before-completion` |
| Connaissance | `knowledge/LANDING-FUNNEL-2026-10-23.md` (§2 structure, §7 hero), `AMK-DESIGN-SKILLS.md` (lois maison) | `MARKETING-OPTICAL`, `HOUSE-KNOWLEDGE-BASE` |
| Tâche | `clients/dm-optic/site/SPEC-PAGES-v1.md` §10.7 (photo de fond du hero), `build-notes.md` (sections 24/10), `hosting/previews/dmoptic/index.html` | `dossier.md`, `PAIEMENT-SOLDE-ET-RETAINER` |

## 1 · Méthode, et pourquoi elle change la réponse

**Chromium headless**, pas Playwright : `bash tools/video/install.sh` (→ `/tmp/amk-video`, paquet npm
`@sparticuz/chromium` + `puppeteer-core`, 13 s, aucun téléchargement externe). `/tmp` ne survit pas
d'une session à l'autre : il se réinstalle à chaque tour. C'est ce qui manquait au tour précédent, où
j'avais écrit « le bac n'a pas de navigateur, impossible de vérifier le rendu » — **c'était faux**, la
route existait déjà depuis le 08/10 (`ops/QA-NOTES.md`, ligne « un navigateur existe »).

Page servie en local (`python3 -m http.server` sur `hosting/previews/dmoptic`, le dossier que Vercel
publie), donc **les fichiers mesurés sont ceux du dépôt**, pas une reconstruction.

## 2 · Les portiques disent zéro faute ; le navigateur dit trois choses

| Porte | Verdict | Ce qu'elle ne peut pas voir |
|---|---|---|
| `audit_a11y.py --strict` | 0 faute A/AA, 0 avertissement | « contraste : non vérifiable ici » — c'est écrit dans sa propre sortie |
| `audit_html.py` | 0 trouvaille, 317 textes | il compose le fond depuis les `background-color` ancêtres ; **une `<img>` de fond et un voile en dégradé ne sont pas des `background-color`** |

D'où l'écart : la revue ci-dessous mesure ce que ces deux-là ne mesurent pas.

## 3 · P1 — l'anneau ne se lit pas comme un cercle

L'anneau est bien là (`animation: spin 24s`, `prefers-reduced-motion` l'arrête : vérifié, `none`).
Le problème est **où il tombe**. Mesures réelles, anneau figé, intersection disque ↔ rectangle :

| Largeur | Diamètre | Part du **titre** traversée | Part de la **carte** sur l'anneau | Anneau visible |
|---|---|---|---|---|
| 390 | 290 | **48 %** | 0 % | 70 % |
| 600 | 290 | **29 %** | 0 % | 70 % |
| 780 | 380 | **39 %** | 0 % | 84 % |
| 900 | 380 | **33 %** | 0 % | 84 % |
| 1024 | 380 | 0 % | **50 %** | 84 % |
| 1280 | 380 | 0 % | **32 %** | 84 % |
| 1440 | 380 | 0 % | **18 %** | 84 % |
| 1680 | 380 | 0 % | 1 % | 84 % |

Il n'y a **aucune largeur où l'anneau est entier et libre** : sous 1024 px il traverse le titre
(jusqu'à 48 % de la boîte du `h1`), à partir de 1024 px la carte blanche en mange jusqu'à la moitié.
Résultat à l'œil : des **arcs isolés** posés sur la photo, qu'on lit comme des rayures, pas comme le
cercle que le client a dessiné. Captures `01-desktop-actuel.jpg` et `02-mobile-actuel.jpg`.

**Proposition (mesurée) : attacher l'anneau à la carte, pas au premier écran.** Le cercle devient le
cadre de la carte d'identité du cabinet — le verre autour de la fiche. Même élément, même dégradé,
même animation : seule l'ancre change (`.lensring` passe dans `.idwrap`, 560 px de diamètre, 440 px
sous 1024).

| Largeur | Titre traversé | Texte (lede) | Lignes « Où / WhatsApp / ONOC » | Boutons | Carte sur l'anneau | Débordement horizontal |
|---|---|---|---|---|---|---|
| 390 | 0 % | 0 % | 0 % | 0 % | 93 % | aucun (`scrollWidth` 390) |
| 768 | 0 % | 0 % | 0 % | 0 % | — | aucun |
| 1024 | 0 % | 0 % | 0 % | 0 % | 99 % | aucun |
| 1440 | 0 % | 0 % | 0 % | 0 % | 97 % | aucun |

Captures `03-desktop-anneau-autour-carte.jpg` et `04-mobile-anneau-autour-carte.jpg`.
**Ce que ça coûte** : sous 1024 px, l'anneau descend avec la carte (il commence à 709 px sur 844 de
haut) — il n'est donc plus dans le tout premier écran du téléphone, il apparaît au premier geste de
défilement. C'est le seul arbitrage de la proposition, et il se tranche à l'œil, pas au chiffre.

## 4 · P2 — le petit texte du premier écran est sous le seuil de contraste

Mesuré sur le fond réel (capture du hero **sans** le texte, puis luminance du fond sous chaque zone) :

| Zone | Taille | Encre | Contraste médian | **Pire pixel** | Seuil AA (texte normal) |
|---|---|---|---|---|---|
| Sur-titre « OPTICIEN OPTOMÉTRISTE À DOUALA… » | 13 px | `--ink-3` #586476 | 4,20 | **3,73** | 4,5 → **échoue** |
| Étiquettes « OÙ / SUR WHATSAPP / OPTICIEN OPTOMÉTRISTE » | 13 px | `--ink-3` #586476 | 4,81 | **4,48** | 4,5 → **limite** |
| Chapeau (lede) | 18,9 px | `--ink-2` #43506A | 5,83 | 5,37 | 4,5 → passe |
| Titre | 52 px | `--ink` #0C1524 | 12,55 | 11,02 | 3,0 → passe |

Sur téléphone c'est pire (fond plus clair) : sur-titre 4,34, étiquettes **3,91**.

**Correctif chiffré** : `--ink-3` de `#586476` à `#46536A` (ou plus simplement `--ink-2`) →
**4,83** au pire pixel, 5,43 au médian. Une seule variable, employée uniquement sur fond clair
(vérifié : 13 usages, tous sur les surfaces claires). Aucun autre changement de la page.

## 5 · P3 — « je peux rendre la photo plus visible » : le chiffre derrière la demande

Le voile du premier écran est un dégradé horizontal de 0,92 (gauche) à 0,16 (droite) de blanc cassé.
Conséquence mesurée : luminance moyenne du fond **0,72 dans la colonne de texte** (où l'on lit)
contre **0,32 dans la bande droite** — la photo est plus de deux fois plus claire là où il y a du
texte, donc effacée là où elle compte le plus, et lisible seulement là où il n'y a rien.

C'est exactement ce que le client appelle « rendre la photo plus visible ». **Le levier n'est pas le
voile global** : le baisser dégrade le contraste déjà limite du §4. Le levier est de **resserrer le
voile sur la colonne de texte** (dégradé plus court, fin de voile vers 52 % au lieu de 76 %) et de
laisser la droite presque nue. À mesurer au tour suivant dans les mêmes conditions.

## 6 · Ce qui va bien, et qui a été vérifié (pas supposé)

- **Focus clavier** : 3 px `solid` #1A3F86 sur les 8 premiers arrêts, lien « Aller au contenu » en
  premier. Visible sur chaque élément.
- **`prefers-reduced-motion`** : animation de l'anneau `none`, et **0 bloc révélé resté caché** sur 40.
- **Menu mobile** (`<details class="mnav">`) : s'ouvre (5 liens, panneau 286 px), se referme avec
  `Échap`. Pas de JS à charger pour l'ouvrir.
- **Aucun débordement horizontal** à 390, 768, 1024, 1440 (`scrollWidth` = largeur de fenêtre).
- **Aucune erreur console**, aucune erreur JS, aucune requête en échec sur `/`, `/en/`, `/contact/`,
  `/montures/`, `/examen-de-vue/`.
- **6 images sur 6** chargées après défilement (les « cassées » du premier relevé étaient les
  `loading="lazy"` hors écran — vérifié, pas supposé).
- **Barre du bas** : `.dock` fixe, 73 px, et `body{padding-bottom:84px}` — le pied de page n'est pas
  recouvert (« Haut de page ↑ » reste à 73 px au-dessus de la barre).
- **Mémoire de langue** : visiter `/en/` puis revenir sur `/` rend la page en anglais (choix stocké).

## 7 · Ce qui n'est pas vérifié ici

1. **Safari / iOS** : rendu Blink seulement. Les `backdrop-filter`, `env(safe-area-inset-bottom)` et
   le `100vh` du hero peuvent différer.
2. **Lecteur d'écran** : `audit_a11y` dit 0 faute de structure ; l'écoute réelle reste à faire
   (`tools/qa/PROTOCOLE-LECTEUR-ECRAN.md`).
3. **Téléphone réel** : capture émulée à 390 px, pas un appareil dans la main de King — et le
   portique « vérifié sur un téléphone, en plein jour » reste entier.
4. **Le déploiement** : `dm-optique-sarl.vercel.app` est construit sur `3a7ca28` ; cette revue porte
   sur les fichiers de `main` (`8e313c7`), identiques pour les pages du site. Aucun changement de
   page n'a été fait pour cette revue, donc **aucun redéploiement**.

## 8 · Ce qui se tranche maintenant

| Question | Proposition | Ce qu'elle coûte |
|---|---|---|
| L'anneau | l'ancrer sur la carte (§3) | 3 lignes de CSS + 1 déplacement de l'élément ; perd sa place au premier écran du téléphone |
| Le petit texte | `--ink-3` → `#46536A` (§4) | 1 variable |
| La photo | resserrer le voile sur la colonne de texte (§5) | 1 dégradé, à remesurer |
| La réponse au client | §5 + §3, dans cet ordre : d'abord « la photo se verra », ensuite « le cercle se lit » | — |

---

## 9 · Le lot appliqué (24/10, soir) — mesure avant / après

Ruling King : « go ». Les trois points du §8 ont été appliqués **ensemble**, puis remesurés dans les
mêmes conditions (Chromium headless, anneau figé par `prefers-reduced-motion`, fond capturé sans texte).
Fichiers touchés : `hosting/previews/dmoptic/index.html`, `…/en/index.html`, `demos/dmoptic-v1.tpl.html`
(le gabarit, pour que le prochain rebuild ne défasse rien). **97 pages** touchées par la seule variable
`--ink-3` ; 3 fichiers par le déplacement de l'anneau et le voile.

### 9.1 · L'anneau — ancré sur la carte

| Largeur | Ø avant | Titre avant | Ø après | Titre | Chapeau | Infos | Boutons | Carte sur l'anneau |
|---|---|---|---|---|---|---|---|---|
| 390 | 290 | **48 %** | 470 | 0 % | 0 % | 0 % | 0 % | 97 % |
| 600 | 290 | 29 % | 440 | 0 % | 0 % | 0 % | 0 % | — |
| 768 | 290 | 23 % | 440 | 0 % | 0 % | 0 % | 0 % | 53 % |
| 1024 | 380 | 0 % | 560 | 0 % | 0 % | 0 % | 0 % | 99 % |
| 1280 | 380 | 0 % | 560 | 0 % | 0 % | 0 % | 0 % | 97 % |
| 1440 | 380 | 0 % (mais carte **18 %**) | 560 | 0 % | 0 % | 0 % | 0 % | 97 % |
| 1680 | 380 | 0 % | 560 | 0 % | 0 % | 0 % | 0 % | 97 % |

Zéro débordement horizontal partout (`scrollWidth` = largeur de fenêtre), zéro erreur console.

**Le trait visible, mesuré au pixel de contour** (deux cercles échantillonnés tous les 2°) : **44–47 %**
du trait est visible hors de la carte à 1024/1280/1440 — contre 0 % du temps où il passait *derrière*
la carte. Autrement dit : le cercle se lit maintenant comme un cercle autour de la fiche, pas comme deux
arcs sur la photo. Sous 1024 px il descend avec la carte (il commence à ~700 px sur 844) : c'est
l'arbitrage annoncé, et il est visible sur `06-mobile-apres.jpg`.

### 9.2 · Le contraste — mesuré sur le fond réel, avant / après

| Zone | Avant 1440 (médian / pire) | Après 1440 | Avant 390 | Après 390 | Seuil |
|---|---|---|---|---|---|
| Sur-titre 13 px | 4,10 / **3,60** | **5,41 / 4,76** | 4,64 / 4,05 | **6,04 / 5,51** | 4,5 |
| Étiquettes 13 px | 4,79 / **4,48** | **6,30 / 5,79** | 4,40 / 4,03 | **5,57 / 5,06** | 4,5 |
| Chapeau 18,9 px | 5,83 / 5,37 | 5,94 / 5,55 | 5,83 / 5,00 | 6,31 / 4,91 | 4,5 |
| Titre 52 px | 12,55 / 11,02 | 12,61 / 11,20 | — | — | 3,0 |

**Tout passe désormais, au pire pixel.** Le gain vient de l'encre (`--ink-3` #586476 → **#46536A**),
pas du voile : c'est dit pour que personne n'attribue à la photo un mérite qui n'est pas le sien.

### 9.3 · La photo — plus visible là où elle est, sans coût de lisibilité

| Zone (1440, hero) | Source | Avant | Après |
|---|---|---|---|
| Colonne de texte | 0,28 | 0,72 | **0,72** (inchangé : c'est la lisibilité) |
| Colonne de la carte | 0,27 | 0,86 | **0,83** |
| **Bande droite** | 0,12 | 0,32 | **0,24** |

Le voile tient la colonne de texte (0,72) et **rend la moitié droite à la photo** : l'écart avec la
source passe de 0,20 à 0,12 en luminance — la photo est 33 % plus présente là où il n'y a pas de texte.
C'est la réponse chiffrée à « je peux rendre la photo plus visible ».

### 9.4 · Ce que le lot n'a pas touché

Rien d'autre : ni la copie, ni les liens WhatsApp, ni le menu, ni le dock, ni les 94 pages intérieures
au-delà de la variable `--ink-3`. Portes après le lot : `test_dmoptic_page.mjs` **62/62**,
`audit_a11y --strict` **0**, `audit_html` **0**, `audit_images` **0** (12 images), `check_inline_js`
**0**, `audit_hero` **0**, `audit_delivery --strict` **VERT** (0 P1, 0 P2, 1 P3 connu). Le garde
`build_dmoptic.py` refuse toujours de reconstruire (`.mnav, .mnav-panel, .psrc`) — c'est voulu.

### 9.5 · Un 4ᵉ point, trouvé en chemin et **pas** corrigé

`tools/qa/audit_reveal.py` signale **4 fautes** sur les deux pages du premier écran : la règle
`html.js .rv{opacity:0}` n'a pas été convertie en `html.js .rv:not(.in)` le 23/10, contrairement à ce
qu'annonçait le commit (les six autres pages l'ont). **Mesuré : identique avant et après ce lot**, et
sans effet visible — `html.js .rv.in` (spécificité 0,3,0) l'emporte sur `html.js .rv` (0,2,0), et le
navigateur montre bien 40 blocs révélés sur 40. Ça reste une porte qui crie pour rien : correctif d'une
ligne par page, à faire sur ton feu vert, pas glissé dans un lot déjà validé.
