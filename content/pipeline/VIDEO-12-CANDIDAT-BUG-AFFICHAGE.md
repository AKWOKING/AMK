# Vidéo 12 (candidate) — « Un bug d'affichage qu'on a mis 2 jours à comprendre »

**Statut :** candidat pipeline (lot vidéo AMK). Titre volontairement sans nom d'outil : il enseigne le
**raisonnement**, pas la technologie. **Règle debout (ci-dessous) : on ne dit jamais « l'IA a fait le
travail » — on dit « on a résolu X ».** Formule : problème → raisonnement → décision → résultat.

## Le bug
Le logo du client, posé dans un cercle du premier écran, **ne s'affichait pas**. Le cercle montrait
uniquement son anneau dégradé ; l'intérieur restait vide. Pourtant la variable CSS existait (DevTools
montrait bien l'URL base64) et le logo s'affichait très bien dans une version précédente.

## Première hypothèse — fausse
« C'est le `background-size: cover` qui rogne la mauvaise zone : le masque circulaire coupe le logo en
deux ou le cache derrière l'anneau. » Testée mentalement et par repro : non. `cover` sur la source ne
retire que les marges claires, jamais le disque du logo. Le logo aurait dû rester visible. Hypothèse
écartée.

## Deuxième hypothèse — la bonne
Le cercle « anneau » était en réalité un **pseudo-élément `::before` rempli d'un dégradé conique plein**
— pas un anneau, un **disque**. Et comme l'élément parent (`position:absolute; z-index:0`) forme un
**contexte d'empilement**, l'ordre de peinture y est : **le fond de l'élément d'abord, puis les enfants à
z-index négatif**. Le `::before` (z-index:-1) se peignait donc **AU-DESSUS** du fond de l'élément — c'est-à-dire
au-dessus du logo. Résultat : un disque dégradé posé sur le logo, qui disparaissait. On voyait « l'anneau »
qui était en fait le bord du disque.

## La méthode du repro minimal
Réduire pour isoler : `background: var(--logo) center/contain no-repeat`, **sans** `border-radius`, **sans**
`overflow`, **sans** `::before` → le logo apparaît (la variable est bonne). Ré-ajouter le `::before` → le
logo disparaît. Le coupable est isolé : c'est le pseudo-élément, pas la variable, pas le rognage.

## Le correctif
Supprimer le `::before`. Poser l'anneau et le logo **sur le même élément** : bordure transparente de 7px +
deux fonds clippés — le logo en `padding-box` (peint au-dessus, à l'intérieur), le dégradé conique en
`border-box` (visible seulement dans la bordure, donc un vrai anneau). Plus aucun problème d'ordre de
peinture : il n'y a plus de pseudo-élément.

## La leçon
Dans un contexte d'empilement, **un enfant à z-index négatif se peint au-dessus du fond de son parent** —
le « derrière » intuitif n'existe que par rapport au *contenu*, pas par rapport au *fond*. Un dégradé qui
doit faire un anneau doit être **creusé** (masque, bordure) ; livré plein, c'est un disque qui mange ce
qu'il devait encadrer. Et la méthode générale : **réduire pour isoler** — enlever une couche à la fois
jusqu'à ce que le symptôme disparaisse, plutôt que de deviner.
