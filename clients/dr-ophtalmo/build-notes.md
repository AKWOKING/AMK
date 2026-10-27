# Dr Ophtalmo — notes de construction

**26/10/2026** · aperçu `hosting/previews/dr-ophtalmo/` · aucun client payant, rien n'est publié.

## 1 · La décision qui commande tout le reste : l'honnêteté est un composant

Le brief demande à la fois « premium, rassurant, crédible » et « ne rien inventer ». Ces deux exigences se
contredisent dès la deuxième ligne d'une page de médecin : un site de soin vide fait peur. La solution
retenue est un **système d'état visible**, pas une absence :

| État | Rendu | Exemple |
|---|---|---|
| `confirmed` | pastille pleine + mot « Confirmé » | aucun pour l'instant |
| `reported` | pastille atténuée + mot « Communiqué » | les quatre lieux, la spécialité |
| `unknown` | pastille en pointillé + mot « À confirmer » | horaires, adresses exactes, contact |

Trois conséquences heureuses : ① le premier client qui remplit la configuration voit les états changer de
couleur sans qu'on retouche une ligne de CSS ; ② le médecin comprend en regardant sa page ce qu'il lui
reste à envoyer — le site est aussi sa liste de courses (bouton « Informations à publier » dans le pied) ;
③ le doute du visiteur est traité là où il naît, au lieu d'être noyé dans une mention légale.

## 2 · Ce qui n'a pas été fait, volontairement

- **Pas de nom dans le hero.** Le H1 est celui du brief (« VOTRE VISION, MA PRIORITÉ. ») : il tient sans
  nom, donc le jour où le nom arrive il n'y a rien à remanier. Dans le parcours, « Dr [NOM DU MÉDECIN] »
  est affiché entre crochets — c'est laid exprès : un crochet ne se confond pas avec un vrai nom.
- **Pas de cinquième lieu, pas de « et aussi… ».** Quatre lieux, numérotés 01–04. Hôpital Charity n'a
  aucun jour : il affiche « à confirmer » plutôt que de deviner dimanche.
- **Pas de carte dessinée pour Bonabéri.** « Grand Hangar, Bloc 7 » est une information de repère, pas une
  coordonnée ; un plan inventé serait pire qu'aucun plan.
- **Pas de lien de carte** tant qu'aucune destination vérifiée n'existe : le bouton « Ouvrir l'itinéraire »
  n'apparaît que si `mapUrl` est rempli, et la configuration refuse d'avoir un lien sans adresse (test).
- **Pas de prix, pas d'avis, pas de compteur.** Un site de soin n'a rien à vendre dans le premier écran.

## 3 · Décisions techniques

1. **Une seule source de vérité** (`js/config/doctor.js`), et la semaine en est *déduite* (`lib/schedule.js`).
   Ajouter un jour ne touche ni le HTML, ni le CSS, ni le sélecteur, ni le formulaire.
2. **Aucun texte dans le HTML.** Tout passe par `data-i18n` et deux dictionnaires ; un test vérifie que
   FR et EN ont exactement les mêmes clefs, donc une traduction ne peut pas « oublier » un paragraphe.
3. **Le formulaire ne parle à personne.** Pas de `fetch`, pas de backend, pas de cookie. Il compose un
   message, l'affiche, et laisse partir WhatsApp si — et seulement si — un numéro vérifié est configuré.
   Tant qu'il ne l'est pas, le message est copiable et le site explique pourquoi il n'y a pas de bouton.
4. **Le message WhatsApp ne contient que les champs du formulaire**, jamais le champ libre : c'est testé.
   Une demande de rendez-vous n'est pas un dossier médical.
5. **Le repli est un état normal**, pas une erreur : le site est complet sans numéro, sans horaires, sans
   nom — c'est ce qui permet de le montrer aujourd'hui.

## 4 · Images

Trois images générées le 26/10 (`assets/src/*.png`, converties en webp 1440/960/640, ~300 Ko au total) :

1. **Portrait** — une praticienne africaine en blouse, salle de consultation lumineuse. Deux tentatives :
   une première avec un homme en blouse n'allait pas avec la deuxième image, et la deuxième version du
   portrait (femme) ne correspondait pas non plus. La cohérence entre le portrait et la photo d'examen a
   demandé trois générations : la première photo d'examen montrait une praticienne européenne avec un
   patient européen, ce qui aurait juré à côté du portrait. Tout est régénéré pour que ce soit la même
   personne dans les deux images.
2. **Examen** — la même praticienne, patiente assise, lampe à fente.
3. **Équipement** — lampe à fente et fauteuil, sans personne.

**Elles ne sont pas le médecin.** Deux légendes le disent à l'écran ; `isRealPhoto: false` commande la
mention. Le jour où le vrai portrait arrive : remplacer les trois fichiers, l'`alt`, et passer le drapeau.

## 5 · Ce que j'ai vérifié, et dans quoi

**Corrigé le 26/10 au soir (tour 179).** La version du matin disait « je n'ai pas vu la page » : c'était
vrai alors, plus maintenant. `bash tools/video/install.sh` installe un Chromium avec ses bibliothèques
(`/tmp/amk-video`), donc la page a été **mesurée**, pas relue.

| Largeur | Débordement horizontal | Texte < 12 px | Images cassées | Erreurs console |
|---|---|---|---|---|
| 1440 / 1024 / 768 / 390 / 320 px | **0** aux cinq | **0** après correction (10,2 px avant) | 0 | 0 |

- **Typographie** : 42 règles tombaient sous 12 px (`0.6x`/`0.7xrem`) → plancher `0.8rem`. L'échelle est
  maintenant tenue à 320 px comme à 1440 px, et `.heading-lg` passe de 20ch à 30ch (un titre de deux
  lignes au lieu de trois).
- **Focus clavier** : anneau de 2 px → **3 px**, et `:active { scale(.975) }` partout, sous garde
  `prefers-reduced-motion`.
- **En-tête mobile** : 60 px de haut à 320 px (wordmark 41 px, sous-titre masqué) — le CTA du hero reste
  visible au premier écran.
- **Polices** : `document.fonts.status === "loaded"` (aucun FOUT résiduel), et aucune requête hors du
  domaine.
- **EN** : 0 tiret cadratin (5 avant), 0 champ sans étiquette, `aria-pressed` correct sur FR/EN.
- **Partage** : `og:image` était un **WebP** — WhatsApp n'en dessine pas d'aperçu. Remplacé par un JPEG
  **1200 × 630** (`assets/img/og.jpg`, 80 Ko), avec `og:image:type/width/height/alt`.
- **Aperçu privé** : `<meta name="robots" content="noindex, nofollow">`, `robots.txt` en `Disallow: /`,
  `_headers` (HSTS, CSP fermée, cache par type de fichier) et `llms.txt` qui écrit noir sur blanc ce que
  le site affirme et ce qu'il laisse à confirmer.
- **Porte de livraison** : `python3 tools/qa/audit_delivery.py hosting/previews/dr-ophtalmo --strict`
  → **VERT, 0 P1**, 1 P2 et 1 P3 **assumés** : le JSON-LD n'a ni téléphone ni adresse parce que le
  médecin ne les a pas donnés (les inventer serait pire que le silence), et pas de `sameAs` puisqu'il
  n'a pas de profil social connu.
- **Tests** : `node tests/logic.test.mjs` → **40 vérifications** (36 → 40 : noindex, robots.txt,
  `og.jpg` présent avec ses dimensions, en-têtes de sécurité).

**Ce qui reste non vérifié, et le reste à la décision de King :** le rendu sur un vrai téléphone
camerounais en 3G, la lecture de l'aperçu WhatsApp depuis une conversation réelle, et le rendu des
polices sur Android ancien.

## 6 · La leçon à garder

*Un site de médecin ne se juge pas à ce qu'il affirme, mais à la manière dont il traite ce qu'il ne sait
pas encore.* Ici, l'inconnu est un état graphique : « Communiqué » / « À confirmer », une phrase qui le dit,
et un bouton qui montre au médecin ce qu'il reste à envoyer. La même mécanique servira au prochain dossier
où le client tarde à envoyer ses informations — c'est-à-dire presque tous.

## 7 · Le lien, la vidéo, et ce qui attend une décision

**Lien d'aperçu :** `https://dr-ophtalmo-preview.vercel.app` — projet Vercel `dr-ophtalmo-preview`
(racine `hosting/previews/dr-ophtalmo`, source GitHub `AKWOKING/AMK`, production), déploiement
`dpl_4f4QJpE1WMuXDZpxrYECtACToaNY` **READY / PROMOTED** sur le commit `f177b6c`. Vérifié à la lecture
externe : la page se sert, `robots.txt` aussi. `noindex` + `robots.txt` : le site **ne s'indexe pas**.

**Vidéo de lancement** (brag, §1f②) : 20 s, 1080 × 1920, 30 fps, captures réelles du site — plan
complet et portiques dans `clients/dr-ophtalmo/brag/brag-plan.md`. **Dans le dépôt** depuis le 26/10 au
soir (demande de King), sous `clients/dr-ophtalmo/brag/` : `brag.mp4` (4,1 Mo, lecture),
`brag-whatsapp.mp4` (2,5 Mo, statut WhatsApp), `poster.jpg` (67 Ko). Le master de 14 Mo reste dehors.

**Ce qui s'est passé avec le premier envoi :** les vidéos n'existaient que dans `/tmp` et dans
`/home/user/brag-output-dr-ophtalmo/` ; l'environnement a redémarré, **ces chemins n'existaient plus**.
Un livrable annoncé « prêt » n'était plus atteignable. Cette fois les fichiers sont dans le dépôt, avec
la composition décrite scène par scène et les captures reproductibles en 10 s.

**Trois décisions qui ne sont pas les miennes :**

1. **Le nom et le titre** du médecin (« Dr [NOM DU MÉDECIN] » s'affiche entre crochets, exprès).
2. **Les horaires** — la semaine est là, les heures sont « à confirmer ».
3. **Le numéro** de téléphone ou WhatsApp — tant qu'il manque, le formulaire compose un message
   copiable et n'affiche aucun bouton : c'est testé.

Tant que ces trois points ne sont pas tranchés, le site reste un aperçu privé et **la vidéo reste un
brouillon** : rien n'est publié ni envoyé au médecin sans la validation de King.

## 8 · Refonte du premier écran — 27 octobre 2026

**Ce qui a changé, et pourquoi.** Le premier écran était un panneau bleu nuit avec une carte photo de
22 rem posée à droite : la photographie du médecin servait d'illustration, pas de composition. King a
demandé que la photo de la salle d'examen devienne **le fond du hero**, pleine largeur, sous la
navigation. C'est fait.

- **Le cadrage suit la photographie, pas l'inverse.** L'image est déjà composée : zone sombre à gauche,
  médecin à droite, matériel éclairé au fond. Le dégradé navy s'arrête à 74 % de la largeur ; à droite,
  l'image est intacte — ni filtre, ni vignette, ni flou. Le texte ne dépasse jamais 41 % de la largeur,
  donc il ne passe jamais sur le visage.
- **Mise en page mobile décidée pour le mobile.** Sous 900 px, un fond pleine largeur rendrait la moitié
  du texte illisible : la composition est empilée — panneau de texte sur navy, photographie juste
  dessous à son propre cadrage (`object-position: 66% 30%`), les deux boutons empilés sous 480 px.
  Les deux actions sont visibles sans défiler.
- **Deux légendes de provenance supprimées** (ruling King : « Photographie transmise par le médecin,
  26 octobre 2026 » n'est pas nécessaire) et **une troisième remplacée** : le portrait isolé de 22 rem a
  cédé sa place à la photographie du Dr Fogue avec ses confrères, en bande pleine largeur. Légende
  neutre — « Le Dr Fogue avec des confrères, dans un service d'ophtalmologie » —, aucune affiliation
  affirmée : le panneau « Hôpital de Paris » visible sur l'image n'est pas vérifié.
- **Palette réconciliée sans rupture** : le fond passe de `#07111d` à `#071b2a` (le bleu de la photo),
  les surfaces sombres à `#10354c`, les sections claires à `#edf5fa`. Le teal reste le seul accent des
  actions. Aucune autre section n'a été redessinée.
- **Copie** : eyebrow « OPHTALMOLOGIE · CAMEROUN », titre « Votre vision, / ma priorité. », lead du
  brief, CTA « Prendre rendez-vous » (→ `#appointments`) et « Voir les lieux de consultation »
  (→ `#consultations`). En-tête : « Dr Fogue / Ophtalmologue ».
- **Ce qui n'a pas bougé** : navigation, sélecteur FR/EN, parcours de rendez-vous, sections lieux,
  questions fréquentes, pied de page, JSON-LD.

**Deux règles du corpus tranchées explicitement.** `AMK-DESIGN-SKILLS.md` §26.1 interdit « du texte sur
une photographie » ; le brief demande l'inverse. La contradiction est résolue par le dégradé : le texte
se pose sur un aplat navy *issu* de la photo, jamais sur une zone à détail. Et `imagegen-frontend-web`
(« HERO COMPOSITION BIAS ») demande de composer pour l'image : ici, l'image était déjà composée avant
d'arriver — c'est elle qui commande le cadrage.

**Photographies.** Dérivés WebP créés depuis les deux fichiers transmis le 27/10 :
`dr-fogue-hero-room-{640,960,1280}.webp` (16/9, 19/31/43 Ko) et `dr-fogue-equipe-{640,960,1024}.webp`
(4/5, 54/87/95 Ko). `og.jpg` recadré en 1200 × 630 sur la nouvelle photo. Les anciens dérivés
`dr-fogue-hero-*` et `dr-fogue-consultation-*` sont supprimés du dépôt : plus aucune page ne les
appelle.

**Mesures avant déploiement.** Le texte garde **7,3:1 à 9:1** de contraste sur ordinateur (pire cas
mesuré sur 96 × 54 points de la photographie, dégradé compris) et le visage reste entier aux quatre
largeurs testées (1100, 1280, 1440, 1920).
