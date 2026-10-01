# LA LIGNE OPTIC — notes de construction (24/09/2026, nuit)

**Client** : **La Ligne Optic** — opticienne à **Akwa, boulevard de la Liberté**, Douala.
Répond **« Ok merci beaucoup vyni »** à 21:04 au message du lot 4 ; King annonce le lien à 21:35.
**Aperçu** : `demos/concept-laligne-v1.html` ← gabarit `demos/laligne-v1.tpl.html` + `demos/build_laligne.py`
→ déployable dans `hosting/previews/laligne/` (`index.html` + `og.jpg`).
**Contrôle approfondi** : `clients/la-ligne/dossier.md` · **inspiration** : `clients/la-ligne/inspiration.md`.

---

## 1 · Le Design Read, et la décision qui commande tout le reste

> Reading this as: a **drawn page for a face-first practice** — chalk paper, graphite ink, one laque red —
> where **nothing is photographed**, because the practice has never published a photograph and we will not
> fake one. Every image is a line drawing, and the drawing *is* the service (leur mot : **visagiste**).

**Dials** : VARIANCE **6** · MOTION **5** · DENSITY **4** — l'atelier calme, l'exact contraire de la page
Cinq Sens construite la veille (affiche, magasin, cinq couleurs qui crient). C'est assumé et écrit au
registre d'unicité.

## 2 · Ce qui a décidé de la forme de la page

| Fait du contrôle | Conséquence de construction |
|---|---|
| 4 services publiés, et rien d'autre : consultation · réfraction · visagiste · conseil | la section 01 prend **ces quatre mots**, dans cet ordre, et explique chacun au patient |
| « **Visagiste** » est le seul mot qui les distingue | le service devient **une expérience** : cinq formes de visage, cinq lignes de monture, chacune son message WhatsApp |
| **Aucune photo** publiée | la page est **dessinée** (SVG) — et la vignette du lien est un dessin, elle aussi |
| **Aucun horaire**, aucun prix, aucune marque, aucun avis | section 04 : « quatre choses qui se règlent en une réponse » — l'honnêteté devient la preuve |
| Titulaire **JOUNGO Line Chantale**, inscription **025/2017** | nommée **une fois**, en pied de page, avec sa qualité ; le numéro d'inscription reste **dans les données structurées** (règle DM OPTIC) |
| Opticien ≠ ophtalmologue | la FAQ l'écrit : la réfraction est un acte d'opticien, l'examen des yeux reste le travail de l'ophtalmologue |

## 3 · Écran par écran

1. **Le premier écran** — « Votre visage d'abord. La monture ensuite. » À droite, un **dessin qui se
   trace** : la règle du regard, un visage, la monture par-dessus (SVG, `stroke-dashoffset`, 5 traits).
   Trois faits sous le texte : opticienne inscrite depuis 2017 · le conseil de visagiste · Akwa.
2. **Les quatre gestes** — une liste à filets (pas des cartes) : chacun dit ce qu'il veut dire **et ce que
   vous pouvez dire en arrivant**.
3. **Le visage d'abord** — cinq onglets radio (ovale, rond, carré, cœur, oblong), **sans JavaScript** :
   `:checked` fait tout. Chaque panneau : le visage dessiné, la ligne conseillée, l'explication, ce qu'on
   évite, et **son** message WhatsApp (la forme est nommée dans le message — la visagiste sait à quoi elle
   répond). Deux notes ferment la section : c'est du **style**, pas un examen ; la photo **reste dans la
   conversation**.
4. **Comment ça se passe** — quatre temps, de « vous écrivez » à « vous repartez avec la suite claire ».
   Aucun délai promis, aucun prix annoncé.
5. **Quatre choses qui se règlent en une réponse** — tarif, marques, horaires, votre monture actuelle :
   on explique **pourquoi** elles ne sont pas sur la page, et on renvoie au WhatsApp. C'est la bande de
   preuves de Felix Gray, retournée : ici la preuve, c'est de ne rien affirmer qu'on ne sache.
6. **Six questions** (`FAQPage`, mot pour mot) · **deux gestes** (WhatsApp, appel) · copier le numéro ·
   fiche `.vcf` · barre d'action fixe sur téléphone.

## 4 · Mouvement (budget §9)

Trois mouvements, pas un de plus : le **tracé** des dessins du premier écran, les **révélations** au
défilement (IntersectionObserver, **jamais** d'écouteur de défilement), et les transitions d'onglets du
navigateur. Un `@media (prefers-reduced-motion:reduce)` arrête les deux premiers ; sans JavaScript, la
ligne est **entière** et tout le contenu est visible.

## 5 · Les contrôles

| Contrôle | Résultat |
|---|---|
| `audit_html.py` | **0 constat** sur **314 passages** de texte (desktop et mobile) |
| `audit_a11y.py --strict` | **0 faute, 0 avertissement** — il a attrapé un saut de niveau **h2 → h4** en pied de page (corrigé en `h3`) |
| `audit_hero.py` | **0 faute, 0 avertissement** |
| `check_inline_js.py` | **rc 0** — 4 blocs compilés |
| `audit_aeo.py` | ✓ `Optician` + `FAQPage` (6 questions, mot pour mot) · `noindex` voulu |
| `audit_images.py` | 0 faute — 0 image, et c'est le sujet |
| `node tools/qa/test_laligne_page.mjs` | **52/52** |
| Poids | **79 Ko**, douze liens WhatsApp, **zéro image à charger** |

**Trois choses que le test protège et qu'aucun audit ne voit** : la page n'a **pas un seul `<img>`** ;
le numéro d'inscription à l'Ordre n'existe **que** dans les données structurées ; la titulaire est nommée
**une fois par langue** (le premier jet de l'assertion comptait une seule fois pour les deux langues — le
test avait raison, la page aussi).

**Un bug attrapé par le test, pas par les audits** : la région vive annonçait « la page est maintenant en
français » **au moment de passer en anglais** (arguments inversés dans `setLang`). Invisible à l'œil,
invisible aux audits — visible pour un lecteur d'écran.

## 6 · Ce qu'on ne dit pas, et pourquoi

- **Aucun horaire** : aucun annuaire ne les donne. La page dit où les trouver (la conversation).
- **Aucune photo, aucune marque, aucun prix, aucun avis** : rien n'a été publié.
- **Aucun repère de quartier** inventé (« en face de… », « à côté de… ») : nous n'en avons trouvé aucun.
- **Aucun acte médical** attribué au cabinet, jamais.
- **Aucune promesse** de délai, de classement ou de résultat.

## 7 · Avant d'envoyer le lien (dans cet ordre)

1. **Déployer** `hosting/previews/laligne/` — **le dossier entier** (`index.html` **et** `og.jpg`) ;
2. `python3 demos/build_laligne.py --url https://<adresse>` puis **redéployer** : `og:url` et `og:image`
   se remplissent là, pas avant ;
3. **ouvrir sur un téléphone** : FR par défaut, bascule EN, le dessin qui se trace, les cinq onglets qui
   changent de panneau **sans JavaScript**, un vrai WhatsApp pré-rempli (683 651 108), aucun débordement ;
4. envoyer le message de `sales/Send-LA-LIGNE-2026-09-24.md` §1, après la carte du lien.

## 8 · La planche de contrôle — et le seul moyen de regarder nos propres dessins

Une page **dessinée** pose une question nouvelle : comment vérifier un dessin quand le bac n'a **pas de
navigateur** ? ImageMagick n'a ni `rsvg-convert` ni cairo ; `cairosvg`, `svglib` et le backend `renderPM`
de reportlab échouent tous les trois (aucune bibliothèque de dessin système). Réponse : un outil à nous,
**`tools/qa/render_svg.py`**, qui rastérise un SVG de la page **avec PIL**, en surdimensionnant ×3 puis en
réduisant (c'est ce qui remplace l'antialiasing absent).

**Ce qu'il a attrapé, et que rien d'autre n'aurait vu :**

1. **Tout sortait blanc sur papier blanc.** Les traits sont écrits `stroke:var(--ink)` : le rastériseur
   ne résolvait pas les variables. Corrigé dans l'outil — mais le piège est noté, parce qu'il a failli
   faire conclure « le dessin est cassé » alors que la page était juste.
2. **Les montures sortaient incolores.** Le style vivait sur un `<g class="stroke frame">`, et le
   rastériseur ne lisait que l'élément. Corrigé : les classes d'un groupe descendent sur ses enfants.
3. **Le visage « rond » n'était pas rond — il était ovale.** Copié-corrigé de la forme ovale, et
   personne ne l'aurait vu à la lecture du code. Corrigé, et une assertion le protège désormais : **les
   cinq visages doivent être cinq tracés différents**.

La planche est gardée : `clients/la-ligne/dessins-controle.png` — les cinq visages + le premier écran,
côte à côte. C'est la preuve qu'on a regardé avant de livrer, et le seul « œil » dont on dispose dans le
bac. **La règle du portique ne change pas** : *not verified on a phone = not sent* — le dessin est
vérifié ici, le rendu final reste à l'œil de King, sur un téléphone.

**Contrôles après cette passe** : `audit_html` **0 constat** · `a11y --strict` **0/0** ·
`test_laligne_page.mjs` **53/53**.

## 9 · Passe 3 — les trois retours de King, et ce qu'ils ont changé

**Ses mots :** ① *« the first head why is it there »* · ② *« it could be a 2d or better yet 3d avatar head
with the different types of glasses that fit the shape of the head swiping showing the different shapes
and glasses »* · ③ *« I find it too simple, we could put some life in it, with animated gradient colors
for example »*.

### ① Le premier écran ne dessine plus de tête

Il n'y était pas par hasard, mais il n'y avait pas de raison : un visage **sans monture**, dans une page
dont la promesse est qu'une monture se choisit **sur** un visage — la démonstration venait avant l'idée.
Le premier écran montre maintenant **la ligne** : une règle graduée qui traverse l'écran, et un **verre**
( deux cercles concentriques + un réticule ) posé dessus. C'est le nom du cabinet, littéralement — *La
Ligne* — et ça ne raconte plus rien de faux. Les visages sont dans le miroir, **là où ils servent**.

### ② Le miroir : un buste dessiné, cinq formes, on glisse

Les cinq vignettes (une par panneau) sont remplacées par **un seul buste** — épaules, cou, tête, oreilles,
sourcils, yeux, nez, bouche, et **trois calques d'ombres** qui donnent un peu de volume (2D, mais qui
respire) — plus **cinq silhouettes de tête**, chacune avec **sa** monture dessinée dessus. Le fondu entre
deux formes passe par un **voile de 2px de flou** (MOTION §3.6) et une micro-rotation : c'est ce qui
évite l'effet « deux visages superposés ».

**On glisse** : `pointerdown`/`pointerup` (à la souris comme au doigt), **40px de seuil** pour ne pas
changer de forme sur un simple appui, et `touch-action:pan-y` pour que **le défilement vertical reste au
navigateur** (51 % du trafic est sur un téléphone : c'est le geste qu'on ne casse pas). Deux flèches et
cinq pastilles font la même chose, et le changement est **annoncé** dans la région vive, dans la langue de
la page (« Forme du visage : rond. Les lignes conseillées et votre message WhatsApp ont changé plus
bas. »).

**Sans JavaScript, le miroir fonctionne** : ce sont les **pastilles radio** qui commandent, en CSS pur
(`:checked ~ .mirror-wrap .h-…{opacity:1}`). On perd le glissement, pas le contenu — et c'est pour ça que
le visage et les cinq silhouettes sont dans le balisage, pas construits par le script.

### ③ La vie : deux lueurs, et les jetons de mouvement

`design/MOTION.md` relu avant d'écrire (la porte §0 : fréquence · but · vitesse · fonction). Deux ajouts,
pas un de plus — le budget de la maison est de 5 à 7 moments par page, et cette page en compte
**cinq** : le système de révélations (1), le tracé de la ligne du premier écran (2), la **lueur du
premier écran** (3), le **halo du miroir** (4), le **fondu-rotation du miroir** (5).

- **La lueur du premier écran** : quatre dégradés radiaux (laque, terre cuite ×2, graphite), très dilués
  (10-17 % d'opacité), qui dérivent en 34 s. Elle est **derrière** (`z-index:0`) — jamais sous le texte
  de lecture : les têtes de section restent sur la craie nue, et c'est mesuré : `audit_html` repasse
  **0 constat** sur **314 passages** de texte.
- **Le halo du miroir** : un `conic-gradient` flouté (34px) qui tourne en 30 s derrière le buste.
- Les deux sont `aria-hidden`, `pointer-events:none`, animés **seulement sous `html.js`**, et **arrêtés**
  par `prefers-reduced-motion` (avec le tracé et les révélations : quatre arrêts vérifiés par le test).

**Ce qu'on n'a pas fait** : pas de lueur dans la section des réponses ni dans les questions (on y lit des
phrases utiles — MOTION §0.4 : sur ce qu'on lit, le mouvement gêne) ; pas de couleur qui tourne en boucle
fort (le rouge laque reste **rare**) ; pas de 3D réelle (un objet WebGL dans une page d'opticien, c'est
500 Ko et une dépendance qui peut casser sur un téléphone d'Akwa — le buste dessiné donne la même
lecture, pèse 4 Ko, et **fonctionne sans JavaScript**).

### Contrôles après cette passe

`audit_html` **0 constat** (314 passages) · `a11y --strict` **0/0** · `hero` **0/0** · `inline_js` rc 0 ·
`aeo` ✓ · `images` 0/0 · **`test_laligne_page.mjs` 68/68** — dont onze assertions neuves : le premier
écran ne contient **aucune** tête ; la lueur existe **une fois**, non cliquable, animée sous `html.js`
seulement et arrêtée en mouvement réduit ; le miroir a **5 têtes et 5 tracés différents**, chacune avec
sa monture ; le visage affiché est commandé **en CSS pur** ; le seuil de 40px ; les flèches qui font le
tour ; et l'annonce en français puis en anglais.

**`render_svg.py` a dû apprendre trois choses** pour qu'on puisse regarder tout ça (voir §10).

## 10 · L'outil de contrôle a grandi avec le dessin

Le rastériseur écrit la veille (`tools/qa/render_svg.py`) ne savait pas lire les courbes lisses : il a
fallu lui apprendre `S` (« le point de contrôle est le miroir du précédent ») et `A` (les arcs), puis
**remplir les formes fermées** — les ombres du buste et les verres teintés sont en `rgba()`, il fallait
donc aussi résoudre les `rgba` et les **mélanger au papier**, comme le ferait un navigateur.

**Et il a menti une fois.** Pour regarder **un** état du miroir, le premier filtre retirait les autres
têtes par expression régulière — mais la recherche non-gourmande s'arrête au premier `</g>`, qui est celui
d'un groupe **enfant** (`<g class="frame">`). Le dessin restant était tronqué : on croyait voir un visage
**sans monture** alors que la page était juste. Réécrit en **comptant les groupes**, comme un analyseur.
**Leçon** : un outil de contrôle qui peut mentir est plus dangereux que pas d'outil du tout — quand il
contredit la page, c'est lui qu'on vérifie d'abord.

La planche finale est dans `clients/la-ligne/dessins-controle.png` : le premier écran, puis les cinq
visages du miroir, côte à côte.

## 11 · Passe 4 — des visages réels, et un premier écran qui vit (24/09, après 22 h)

Retour de King, sur capture : *« The hero section looks boring, told you I wanted animations, the heads
can we make something more realistic can't you generate heads of those shapes with glasses »*, et
*« Look for inspiration online for this type of clinic »*. Trois choses à réparer : le premier écran,
les visages, et la recherche.

### Les cinq visages sont des PHOTOGRAPHIES

Le §10 se terminait sur un buste **dessiné** — quatre traits, lisible, sans une photographie, fidèle à
« le cabinet n'a publié aucune photo ». King a tranché : **des visages réalistes**. On ne fabrique
toujours pas la vitrine de quelqu'un d'autre — alors les portraits sont des **images d'illustration**
générées pour la page, et **la page le dit elle-même** sous le miroir : « ce ne sont pas des clients du
cabinet, et ce ne sont pas des montures de son stock ». C'est la règle de Cinq Sens (« mise en
situation ») appliquée à un visage : la franchise est écrite dans la page, pas seulement dans le
dossier.

Cinq formes, cinq personnes, et **la monture que la forme appelle** — celle qu'un visagiste
recommanderait, pas un accessoire au hasard :

| Forme | Le visage | La monture |
|---|---|---|
| **ovale** | femme, début trentaine, mâchoire douce | rectangulaire aux coins arrondis, **écaille miel** |
| **rond** | homme, quarantaine, joues pleines, sans angle | rectangulaire anguleuse, **acétate rouge laque** — la couleur de la maison sur un visage |
| **carré** | femme, fin vingtaine, mâchoire droite | **or fin**, ovale étroit, cerclé léger |
| **cœur** | femme, mi-trentaine, menton étroit | **or rose pâle**, petit ovale à cerclage fin, rien de lourd en haut |
| **oblong** | homme, cinquantaine, visage long | **browline graphite**, verres hauts pour couper la longueur |

Nous ne nommons **aucune marque** : les montures sont décrites par leur forme et leur couleur, jamais
par un modèle. Le visage, lui, est centré sur le regard (cercle du verre : le carré central de 88,9 % ×
71,1 % du portrait) — c'est le conseil qui compte, pas la coiffure.

### Le premier écran : un seul objet, et il bouge

Le premier écran n'est plus « un dessin à droite ». C'est **la page entière en un objet** : la ligne du
regard, un verre, et **cinq visages qui passent dedans**, un cadran gradué autour, un pouls qui part du
bord du verre. Autrement dit : *on regarde un visage à travers une ligne de vue* — exactement ce que
promet le titre.

Cinq mouvements, tous derrière la porte `html.js` et **tous arrêtés** en `prefers-reduced-motion`
(le premier visage reste alors affiché, fixe) :

| Mouvement | Durée | Pourquoi (MOTION §0 : un but nommé, sinon on supprime) |
|---|---|---|
| l'onde lumineuse balaie la règle | 9 s, `linear` | **explication** : la règle se lit comme un instrument en marche |
| le cadran gradué tourne | 96 s, `linear` | **explication** : c'est un réglage, pas une décoration |
| le pouls part du verre et se dilue | 3,6 s | **état** : le verre est vivant, et l'œil revient au centre |
| les visages se relaient | 25 s (5 s/visage) | **explication** : cinq formes, une seule place — la thèse de la page |
| la deuxième couche de dégradé tourne | 54 s, `linear` | **ambiance** derrière le texte, jamais dedans |

Le fondu entre deux visages passe par le **pont de flou de 2 px** (MOTION §3.6) — sinon on voit deux
visages l'un sur l'autre. Le réticule à croix a été **retiré du visage** : une croix sur un nez, c'est
une cible ; les repères sont maintenant **sur la ligne**, à la rencontre du verre.

### Le contrôle : 249 Ko de JPEG, et un angle mort refermé

Chaque visage est monté **deux fois** — 720×900 (q 66, ≈ 36 Ko) pour le miroir, et le carré de 320×320
(q 64, ≈ 10 Ko) pour le verre du premier écran. La page passe de 90 982 o à **424,7 Ko** (dont 249 Ko de
JPEG) : c'est le prix de cinq visages réels, et il est tenu (budget 400 Ko par image).

**`audit_images.py` ne voyait pas les images embarquées** : il annonçait « 0 image(s) » sur une page qui
en porte dix. Corrigé le soir même — il décode chaque `data:image/…;base64`, la pèse, lit ses
métadonnées et vérifie le ratio annoncé, exactement comme un fichier. Son témoin est passé de 13 à
**17 assertions** (image embarquée saine, 420 Ko, GPS, ratio menteur).

### Les contrôles de cette passe

`audit_html` **0 constat** (330 passages) · `a11y --strict` **0/0** · `hero` **0/0** · `inline_js` rc 0 ·
`aeo` ✓ · **`images` 0/0 sur 5 images comptées** · **`test_laligne_page.mjs` 77/77** (68 avant).

La planche `dessins-controle.png` a été refaite : le premier écran monté à la main (PIL), puis les cinq
portraits du miroir — parce qu'on ne livre pas un dessin qu'on n'a pas regardé.
