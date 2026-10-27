# KIT — « La monture cherche son nom », épisode 1 · H08

```
Pièce A      monture-01-h08-voix.mp4 · 28,37 s · 1080×1920 · 30 fps · H.264 + AAC 48 kHz mono
             1,75 Mo · **parlée** (voice-06, 27/10) — la pièce à publier
Pièce B      monture-01-h08.mp4 · 27,10 s · 1,29 Mo · **muette** — le même film, même histoire, sans la voix
Mouvement    ✅ **aucun élément de motion design** — images fixes, coupes franches, texte en fondu de
             0,12 s (King, 27/10 : « the images move too much » → voir §9)
Images       **les trois que King a demandées** — la monture (macro) · le **catalogue du site** qui défile ·
             une personne portant la H08 (**image générée**, déclarée §8) — **plus** la **fiche H08** au beat 5
Visage       ⚠ **un visage, et il est généré** — aucun patient, aucune photo du personnel, aucun tournage
Sans tournage ✅ aucune caméra : la monture est une photo **réelle** du cabinet, déjà au dépôt
Sans le docteur ✅ rien à demander au cabinet pour produire ce fichier
Histoire     sur notre site, **40 montures, 40 codes** — aucune n'a de nom propre
Jeu          **A (Éclat) / B (Minuit) / ou votre mot** — un vote à une lettre, une porte ouverte
Cadence      **mardi** la vidéo (appel) · **vendredi** le carrousel (5 noms, vote) · **mardi** le résultat
Script       content/month1/w3/MONTURE-01-SCRIPT.py — 6 beats, rôles, jeu (lu par `audit_story`)
Rendu par    tools/record/make_dmoptic_monture.py (`--voice-dir` pour la version parlée)
Portes       audit_story ✓ 6 beats, 0 avertissement · audit_hook ✓ · audit_video_motion **--calme OK**
             sur les deux fichiers (tenue max 2,2 s · 28 changements) · audit_post_dm ✓ · banc 35/35
Amendement   brand/DIRECTION-MARQUE-v2 §12 (27/10) — la monture est **le personnage** de cette série
Fait le      27/10/2026 — tours 194 (muet), 195 (voix), 196 (histoire + jeu), 197 (vote A/B + cadence),
             198 (les trois images), 199 (humanizer + roast + film calme)
```

---

## 0 · Les trois scripts proposés par King — ce que la porte en dit

Les trois ont été **passés à la porte du récit** (`audit_story`) et à celle de l'accroche (`audit_hook`),
pas jugés au goût. Verdict : **les trois échouent sur les quatre mêmes points**, et c'est utile — c'est une
lacune de structure, pas de style.

| Point | P1 « Éclat ou Minuit ? » *(écartée en l'état)* | P2 « H08 cherche son surnom » *(écartée en l'état)* | P3 « À Douala, elle mérite un nom » *(écartée en l'état)* |
|---|---|---|---|
| `pas-de-lockin` | ⛔ rien ne dit pourquoi rester | ⛔ idem | ⛔ idem |
| `preuve-absente` | ⛔ aucun fait | ⛔ aucun fait | ⛔ aucun fait |
| `rehook-mal-place` | ⛔ le « return hook » arrive **après** le dernier corps | ⛔ idem | ⛔ idem |
| `cta-non-aligne` | ⛔ le CTA ne prononce pas « nom » | ⛔ idem | ⛔ idem |
| autres | — | — | `liste-sans-axe` (3 exemples dans un beat) |
| `audit_hook` sur l'accroche | ⛔ `mots-manquants` (objectif, contraste) | ⛔ idem | ⛔ `mots-manquants` (sujet, contraste) |

**Ce qui est bon dans les trois, et que la v4 a pris** :

| De | Ce qu'on garde | Pourquoi c'était la bonne idée |
|---|---|---|
| **P1** | **le vote binaire** — deux noms, on tape A ou B | c'est le plus petit pas possible : une lettre. Et ça fait une **question** de la vidéo : le spectateur veut savoir lequel gagne |
| **P1** | **« tu as un meilleur nom ? propose-le »** | la porte ouverte à celui qui a mieux, sans l'obliger à écrire une phrase |
| **P2** | **« c'est son code »** — le mot juste | c'est le fait qui porte l'histoire : un code de colis, pas un nom |
| **P3** | **l'ancrage local** (« à Douala, elle mérite un vrai nom ») | ça situe la scène à Bonabéri, pas dans un studio |
| **P3** | **la date de réponse** | une promesse datée fait revenir ; notre v4 dit « mardi » **au carton final** |
| **P3** | **la cadence** (mardi vidéo / vendredi carrousel / mardi résultat) | c'est **exactement le rythme contractuel** (2 publications/semaine, `posting-calendar.md`) |

**Ce qu'on n'a pas pris, et pourquoi — trois refus argumentés** :

1. **« Suis DM Optique » / « Abonnez-vous »** (P1, P2, P3). ⛔ `audit_post_dm` le refuse code
   `abonnement-mendicite`, et la doctrine du 27/10 dit pourquoi : *demander un abonné n'en produit pas,
   c'est une raison de revenir qui en produit un*. La v4 remplace la demande par **la raison** : on montre
   le nom qui gagne, mardi. Celui qui veut le voir revient — et s'il revient deux fois, il s'abonne.
2. **« Votre monture »** (v2/v3) — King a raison, **elle n'est pas à eux**. La v4 dit « **elle** », et rend
   le spectateur **sujet** de la phrase : « **vous choisissez** celui qui reste ». Il ne possède rien, il
   décide. C'est la différence entre flatter et inviter.
3. **Le « coup de cœur »** (P2). « On choisira notre coup de cœur » = le cabinet garde le dernier mot sur
   un jeu dont il a fixé les règles. Un concours dont le jury peut tout faire n'est pas un concours. La v4
   dit ce qui est décidable et ce qui ne l'est pas : **A ou B l'emporte au nombre de voix ; un mot proposé
   peut l'emporter s'il revient plus que les deux autres ; le cabinet ne tranche qu'en cas d'égalité**.
   Cette règle-là est dans le commentaire épinglé, pas dans la vidéo (on ne met pas un règlement dans 27 s).

**Deux détails de langue** : P1 et P2 tutoient (« tu choisis ») puis vouvoient dans la même pièce
(« c'est vous qui le choisissez »). La v4 **vouvoie partout** — la copie du cabinet s'adresse à des adultes
qui viennent pour un examen de vue, et le mélange s'entend.

---

## 1 · L'accroche — trois composantes, une seule phrase

| Composante | Ce qui est écrit / montré / dit | Secondes |
|---|---|---|
| **texte** | **ELLE N'A PAS DE NOM** (0,0–2,0) puis **VOUS CHOISISSEZ** (2,0–3,9) · **40 MONTURES / 40 CODES** (4,2–9,0) · **H08** puis **A · ÉCLAT / B · MINUIT** ensemble (9,2–15,1) · **SUR UN VISAGE / TOUS LES JOURS** · **LE NOM RESTE / SUR SA PAGE** · **A, B / OU VOTRE MOT** — sept cartons écrits à la main, aucun automatique | 0,0–2,0 |
| **visuel** | la monture **réelle**, entière d'abord, puis macro de la double barre, puis la fiche crème — une coupe à **0,94 s**, jamais une image qui s'installe | 0,0–2,0 |
| **parlé** | voice-05 : « **Elle n'a pas de nom. Vous choisissez celui qui reste.** » puis « Sur notre site, **quarante** montures. Toutes s'appellent par un code. » puis « Celle-ci s'appelle **H08** (*dit : « H, zéro, huit »*). Deux noms sont sur la table : Éclat ou Minuit. » | 0,0–2,0 |

**Les quatre accroches écrites pour cette pièce, et ce que la porte en a dit** :

| # | Accroche | Verdict (`audit_hook`) |
|---|---|---|
| 1 | **« Elle n'a pas de nom. Vous choisissez celui qui reste. »** | **retenue** — 10 mots, 53 car., ✓ |
| 2 | « Cette monture s'appelle H08. Comme un colis. » | **écartée** — `mots-manquants` : ni sujet ni contraste |
| 3 | « Pour H08, tu choisis Éclat ou Minuit ? » (P1) | **écartée** — `mots-manquants` : ni objectif ni contraste |
| 4 | « H08, c'est son code. Son surnom, c'est vous qui le choisissez. » (P2) | **écartée** — `mots-manquants` : ni objectif ni contraste |

**Pourquoi c'est aligné** : le carton dit « elle n'a pas de nom », l'image montre **l'objet sans étiquette**
— ni marque, ni prix, ni référence pendant ces 2 s — et la voix prononce la même phrase, au mot près, dès
**0,0 s**. La première ligne des deux légendes est **exactement** cette phrase (53 caractères).

---

## 2 · TikTok — 19 h 00 (mardi)

```text
Elle n'a pas de nom. Vous choisissez celui qui reste.

Sur notre site, il y a quarante montures. Chacune a un code à la place d'un nom. Celle-là, c'est la H08.
Deux noms sur la table : A, Éclat. B, Minuit. Tapez A ou B. Si vous avez mieux, votre mot.

Vendredi, les cinq mots les plus dits passent au vote. Mardi, le nom gagne et s'écrit sur sa fiche.
La suite ? La monture d'après.

Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20je%20viens%20de%20voir%20la%20monture%20sans%20nom%20sur%20TikTok.%20La%20H08%20est%20au%20cabinet%20%3F
📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri · Examen de vue 8h30–13h00, du lundi au samedi

#dmoptique #opticienbonaberi #douala
```

- **Sous-titres manuels** — sept cartons écrits à la main, aucun automatique (ruling 11/10). La version
  muette est publiable telle quelle : c'est le même film, sans la piste voix.
- **Commentaire épinglé** (il porte le règlement, la vidéo porte l'invitation) :
  > **La règle** : tapez **A** ou **B**, ou écrivez **un seul mot**. Pas une marque, et rien qui promette
  > quoi que ce soit sur la vue.
  > **Comment on tranche** : vendredi, les cinq mots qui reviennent le plus passent au vote ; mardi, celui
  > qui a le plus de voix gagne. Le cabinet ne tranche qu'en cas d'égalité.
  > **Ce que gagne le nom** : il est écrit sur la fiche de la monture, sur notre site — et il y reste.
  > WhatsApp 656 122 239 · examen de vue 8h30–13h00, du lundi au samedi.
- **Ce qu'on ne promet pas** : ni remise, ni monture offerte, ni délai de livraison. Le prix du jeu, c'est
  une lettre.

## 3 · Facebook — 20 h 30 (mardi)

```text
Elle n'a pas de nom. Vous choisissez celui qui reste.

Sur notre site, il y a quarante montures. Chacune a un code à la place d'un nom. Celle-là, c'est la H08.
Deux noms sur la table : A, Éclat. B, Minuit. Tapez A ou B. Si vous avez mieux, votre mot.

Vendredi, les cinq mots les plus dits passent au vote. Mardi, le nom gagne et s'écrit sur sa fiche.
La suite ? La monture d'après.

Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20je%20viens%20de%20voir%20la%20monture%20sans%20nom%20sur%20Facebook.%20La%20H08%20est%20au%20cabinet%20%3F
📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri · Examen de vue 8h30–13h00, du lundi au samedi

#dmoptique #opticienbonaberi #douala
```

- **Alt text** : *« Vidéo de 28 secondes, avec voix. Une monture noire et dorée à double pont, puis la page
  du catalogue du site qui défile — H02, H04, H05, chacune avec son code —, puis une femme qui porte cette
  monture (image générée), puis la fiche H08 sur le site. On entend « elle n'a pas de nom, vous choisissez
  celui qui reste », « quarante montures, toutes avec un code », « Éclat ou Minuit ». À l'écran, les deux
  noms sont proposés côte à côte, A et B, et le carton final dit « le nom qui gagne, mardi ». »*
- Le texte prérempli **diffère** de TikTok : deux liens, deux provenances.
- Un seul CTA (**écrire**) ; le vote est la mécanique du jeu, pas un second CTA.
- **Sondage Facebook** : il ne remplace pas le commentaire, il le **double** (un vote à un clic pour ceux
  qui n'écriront jamais). Les deux résultats se lisent ensemble, jamais l'un sans l'autre.

---

## 4 · La réponse d'accueil (à coller telle quelle)

> Bonjour, ici **DM Optique**, Ndobo Mayor (Bonabéri) — vous écrivez pour la monture sans nom, la H08 ?
> Elle est au cabinet. L'examen de vue se fait le matin, **8h30–13h00**, du lundi au samedi.
> Vous voulez passer l'essayer, ou vous préférez que je vous envoie deux autres photos ?

*(si la personne a voté ou proposé un mot, et seulement alors)*

> Votre mot est noté, il est dans la liste. Vendredi, les cinq qui reviennent le plus passent au vote.
> Si le vôtre gagne, il est écrit sur la fiche de la monture — et on vous demande votre accord avant de
> vous citer.

---

## 5 · Le jeu, et ce qu'on compte

**Les trois temps du jeu** — et chaque temps est aussi l'appel du suivant :

| Jour | Pièce | Ce qu'on demande | Ce que ça produit |
|---|---|---|---|
| **mardi** | vidéo 27 s | **A**, **B**, ou un mot | des commentaires faciles (une lettre) et des propositions (un mot) |
| **vendredi** | carrousel 5 slides | **le vote** entre les cinq mots qui reviennent le plus | ceux qui ont proposé reviennent défendre leur mot ; les autres votent sans écrire |
| **mardi** | vidéo suivante | rien : on **annonce** le nom, on crédite (avec accord), on ouvre **H09** | la boucle se referme et se rouvre dans le même geste |

**Le vendredi — carrousel « les 5 noms en lice »** (une slide = un nom, pas plus de 25 mots) :

| Slide | Contenu |
|---|---|
| 1 | « Cinq noms pour une monture. Un seul reste. » + la monture |
| 2–6 | un nom par slide, dans l'ordre des voix, avec ce que le nom évoque en une phrase — **jamais** « le meilleur » |
| 7 | « Tapez le numéro de votre nom, en commentaire. » + « le résultat mardi » |
| 8 | où · horaires · WhatsApp prérempli |

**Quatre nombres décident** : **votes A/B** (une lettre — le vrai test de friction), **mots proposés**
(cible ≥ 5), **abonnés gagnés** (l'objectif de la série), **messages préremplis** (le cabinet). Les vues ne
décident rien.

**Le seuil, écrit d'avance** : moins de **200 vues** → pas de résultat, on conclut sur la première seconde.
Moins de **10 votes** (A + B + mots) → le vote n'intéresse pas : on change la mécanique, pas le sujet.
**Des mots mais aucun vote** → les gens préfèrent proposer que choisir : on inverse (proposition d'abord).

| Moment | Vues | Votes A/B | Mots proposés | Messages reçus | Conversations | Abonnés |
|---|---|---|---|---|---|
| J+1 | | | | | | |
| J+7 | | | | | | |

---

## 6 · Les portes, et ce qu'elles ont dit

| Porte | Résultat |
|---|---|
| `tools/qa/audit_story.py` | **✓** — 6 beats, 0 avertissement : cas → lock-in+preuve → corps → **rehook** → corps → sortie · débit **~3 mots/s** · preuve à **16 %** de la pièce |
| `tools/qa/audit_hook.py` | **✓** — « Elle n'a pas de nom. Vous choisissez celui qui reste. » 10 mots, **53 caractères** ⚠ `sans-intrigue` + `niveau-1` assumés (comme sur toutes les variantes testées) |
| `tools/qa/audit_video_motion.py` `--calme` | **OK** sur les **deux** fichiers — image la plus longue tenue **2,17 s** (plafond 2,6 s), **28 changements** de plan ou de carton · le mode par défaut (fenêtres 1 s / 2 s) n'est plus la bonne règle pour un film volontairement immobile (voir §9) |
| `tools/qa/audit_post_dm.py` | **✓** sans avertissement — première ligne **53 caractères**, deux nombres communs entre le texte et la voix (**8** pour H08, **40** pour quarante) |
| Audio mesuré | premier bloc **0,0 s** · dernier **26,3 s** · RMS médian **−21,7 dB** · six blocs (3,92 · 4,88 · 6,02 · 3,86 · 3,43 · 2,89 s) + **0,9 s** de queue pour lire le carton final |
| Visages · IA · prix · marque · promesse | **un visage, et il est généré** — les quatre autres verrous tenus ; l'image est déclarée au kit §8, pas au spectateur sous un faux air de photo du cabinet |

---

## 7 · Ce qui est vérifié, et ce qui ne l'est pas

**Vérifié** (ffprobe + PCM + images de contrôle, 27/10) : parlée **28,37 s** · H.264 + AAC 48 kHz mono ·
**1,75 Mo** · muette **27,10 s** · **1,29 Mo** · **film calme** vérifié par `audit_video_motion --calme`
sur les deux fichiers · **un visage, généré** (voir §8) · les deux captures de site sont **coupées avant
le raccord** de la capture pleine page.

**Vérifié pour l'histoire** : **40 fiches en ligne** (10 enfants + 24 femmes + 6 hommes, comptées dans
`hosting/previews/dmoptic/montures/`) · chaque fiche s'appelle par son code (`H08 · Double pont aviateur
noir et doré`) · la monture est la photo réelle du cabinet.

**Décidé, et à dire** : l'amendement `DIRECTION-MARQUE-v2` §12 — la série fait de la monture **le
personnage** et autorise « quarante montures » à l'écran, alors que le §8 et le §10.5 le refusaient. C'est
une instruction de King du 27/10, écrite, datée, bornée à cette série — et **révocable par un mot**.

**Non vérifié, et il faut le dire** :
- **la H08 est-elle encore au cabinet ?** Le site la publie, personne ne l'a confirmée cette semaine.
- **8h30–13h00** : horaire publié par le cabinet, non reconfirmé.
- **La cadence suppose que King publie mardi et vendredi.** « Mardi » est écrit sur le carton final : si la
  vidéo de résultat ne sort pas mardi, c'est la seule promesse du jeu qui tombe.
- **Éclat et Minuit sont nos deux propositions**, pas celles du public. Le cabinet les a choisies ; le
  public peut les battre avec un mot — c'est la règle, elle est écrite dans l'épinglé.
- **Rien ne prouve qu'un vote à une lettre produise plus de commentaires** qu'une demande libre chez nous :
  nous n'avons jamais publié de jeu. Le seuil de 10 votes est une **cible**, pas une prévision.

---

## 8 · Les images — et l'exception qu'elles demandent

King, 27/10 (tour 198) : *« en plus du script et ce qui apparaît sur l'écran, je veux que tu ajoutes des
images »*, avec trois beats nommés. La règle de la maison était simple : **aucune image générée**. Elle est
levée **une fois, pour un seul plan**, et voici ce que ça coûte et ce que ça ne coûte pas.

| Beat | Ce qu'on voit | D'où ça vient | Fichier |
|---|---|---|---|
| 1 · « elle n'a pas de nom » | la monture, macro sur le double pont | photo **réelle** du cabinet, déjà publiée sur le site | `hosting/previews/dmoptic/montures/monture-h08.webp` |
| 2 · « quarante montures, toutes avec un code » | la page **Montures hommes** qui défile ; H02, H04, H05 lisibles | capture Chromium du **vrai site** (27/10/2026), 1080×10 696 | `assets/catalogue-hommes.jpg` (764 Ko) |
| 4 · « elle ira sur un visage » | une femme portant une double pont noire et dorée | **image générée** (référence : la photo du cabinet) | `assets/visage-h08.jpg` (174 Ko, 768×1376) |
| 5 · « le nom… s'écrit sur sa page » | la **fiche H08**, posée dans le cadre, qui défile | capture Chromium de la **vraie fiche** (27/10/2026) | `assets/fiche-h08.jpg` (493 Ko, 1080×8 000) |

**Ce que l'exception couvre, et rien de plus.** Le visage du beat 4 n'est pas un patient, ce n'est pas un
membre du cabinet, et il ne porte pas *exactement* la H08 : c'est une **approximation** — double pont, noir
et doré. Le film ne dit nulle part « voici la H08 portée ». Le jour où le cabinet veut un vrai visage, il
suffit de remplacer `assets/visage-h08.jpg` et de relancer **une** commande :

```bash
python3 tools/record/make_dmoptic_monture.py --voice-dir /tmp/voixI \
        --out clients/dm-optic/content/month1/w3/assets/monture-01-h08-voix.mp4
```

**Ce que l'exception ne couvre pas** — et qui reste interdit : une image générée pour un prix, une monture
en stock, un résultat de vue, ou un « client satisfait ». Le §12 de la direction de marque borne
l'amendement à cette série ; il est révocable par un mot de King.

**Deux détails de fabrication qui se voient à l'écran**

- Les captures pleine page du site contiennent un **raccord** (le haut de la page réapparaît une seconde
  fois, à 8 190 px pour le catalogue, 2 225 px pour la fiche). Les masters sont coupés **avant** : sans
  ça, le plan montre une page qui bégaie. C'est mesuré, pas supposé.
- La fiche du beat 5 est **posée dans le cadre** (648×1 152, ombre douce, bas fondu) et non en plein
  écran : le bandeau de texte tombe alors sur le marine, jamais sur le bouton vert de la page, et le titre
  de la fiche reste lisible du début à la fin du plan.

**Ce qu'on ne sait pas** : si une page du site change, les captures vieillissent — elles sont datées du
27/10/2026 et devront être refaites pour l'épisode 2. Et personne n'a encore mesuré si un insert de page
web retient mieux qu'une macro de produit : nous le saurons au compteur, pas avant.

---

## 9 · Le film calme — et pourquoi la porte du mouvement a changé de règle

King, 27/10 (tour 199) : *« remove all the motion design elements, the images move too much »*. Ce n'est
pas une préférence de goût qu'on discute : c'est une instruction, et elle est écrite dans
`brand/DIRECTION-MARQUE-v2` **§13** (amendement du 27/10, borné à cette série, révocable).

| Ce qui a été enlevé | Ce qui reste |
|---|---|
| poussées avant, panoramiques, dérives dans le cadre | **les coupes** (13 plans pour 6 beats) |
| bandeaux qui glissent de 20 px, lignes qui arrivent en décalé | le texte, en **fondu de 0,12 s** |
| filet accent qui grandit sous le carton | le filet, **fixe**, à sa largeur finale |
| poussée de 8,5 % sur la fiche, glissement du carton | la fiche, **posée**, immobile |
| zoom d'entrée sur les 0,45 premières secondes | rien : la première image est déjà là |

**La porte a suivi, elle n'a pas été contournée.** `audit_video_motion` jugeait « une fenêtre figée =
diaporama ». Sur ce film-ci, à la fenêtre **1 s**, l'ancienne règle **bloque** (9 fenêtres figées : 4-5,
7-8, 12-13, 15-16, 17-18, 19-20, 20-21, 24-25, 27-28 s) ; à 2 s elle passe. Autrement dit : elle mesure le
**mouvement**, pas le **rythme**. Elle est donc complétée, pas désarmée : le mode **`--calme`** juge la **tenue** — *aucune image ne tient plus de 2,6 s
sans un changement* (coupe, carton, texte). C'est ce qui sépare un film calme d'un diaporama, et c'est
mesuré à chaque rendu :

```
monture-01-h08-voix.mp4 · 28,37 s · mode calme · plafond 2,6 s
tenue la plus longue : 2,17 s · 28 changements      → OK
monture-01-h08.mp4      · 27,10 s · mode calme · plafond 2,6 s
tenue la plus longue : 2,08 s · 30 changements      → OK
```

**Pour rallumer le mouvement** (si le calme ne retient personne) : une option, aucun autre fichier à
toucher — `python3 tools/record/make_dmoptic_monture.py --voice-dir /tmp/voixJ --mouvement --out …`

**Ce que le tour a changé dans le texte** : les six phrases sont passées au skill `humanizer` (5 motifs
corrigés — triade, deux-points, trois « Elle » en ouverture, fragment sans verbe, sujet absent) puis à la
**Roast Room** (séance du 27/10, verdict B : humaniser + calmer, garder la structure). Les deux documents
sont au dépôt : `knowledge/HUMANIZER-MONTURE-01-2026-10-27.md` et
`knowledge/ROAST-2026-10-27-MONTURE-01.md`.
