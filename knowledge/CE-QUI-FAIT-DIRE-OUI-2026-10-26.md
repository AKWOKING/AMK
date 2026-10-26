# Ce qui fait dire oui — la comparaison du 26/10, texte reçu contre texte écrit

**Origine.** King envoie le 26/10 un message écrit ailleurs (quatre paragraphes) et pose la
question qui vaut mieux qu'un audit : *« à la place d'un opticien, tu ne dirais pas oui ? »*.

**Ce que ça change dans la méthode.** Le fait daté reste la preuve — c'est ce que ce texte n'a pas, et
c'est ce qui le rend jetable. Mais la preuve seule parle de la fiche du prospect, pas de sa journée. Un
cabinet ne se reconnaît pas dans un constat sur son annuaire ; il se reconnaît dans **un patient qui
s'en va**. v6 ajoute ce patient en cinq mots, et ne retire rien.

## 1 · Le verdict de la porte, sur le texte reçu

`tools/qa/audit_outreach.py` : **72 mots, 5 phrases → BLOQUÉ**, quatre motifs (longueur, nombre de
phrases, une phrase sans ancrage, aucune cause nommée, question finale sans verbe d'action). La forme échoue. Le fond gagne deux points, et
ce sont ceux que nos cinq n'avaient pas.

## 2 · Les deux points gagnés

| Le point | Pourquoi il marche | Pourquoi il ne suffit pas |
|---|---|---|
| **Il vend ce que le patient perd**, pas ce qui manque à la fiche | on comprend le manque à gagner sans avoir à admettre un défaut | il ne dit **où** le patient lit le cabinet : le décor remplace le fait |
| **L'aperçu est nommé par son contenu** (« avec vos horaires ») | le gratuit devient un objet qu'on peut se figurer | « je vous ai **préparé** » est un fait, pas une offre |

## 3 · Ce qu'on a pris

- **Un comportement, pas une impression.** « il appelle l'annuaire », « il ne sait pas », « le patient
  repart », « resté seul avec sa question », « il hésite ». Un comportement se vérifie ; une impression
  se conteste.
- **Le contenu du site en objets** : le plan, les jours et les fêtes, les examens et les montures, les
  assurances et les garanties, le nom et les horaires. C'est le « tout voir d'un coup » du texte reçu,
  mais vérifiable ligne à ligne.
- **L'adoucissement.** Sur ④, « fiche unverified, sans un seul avis » sort du message : la question datée
  du 30/06/2024 reste. La faute est à la fiche, pas au patron.

## 4 · Ce qu'on n'a pas pris

| Refusé | Raison |
|---|---|
| « vrai site web » | « vrai » insinue que ce qu'il a déjà est faux. On ne vend pas en niant l'existant. |
| « en un clin d'œil », « sans engagement » | clichés de vendeur ; la porte les traite comme du remplissage. |
| « transformer ces recherches en clients directs » | promesse de résultat invérifiable — ruling 142. |
| « catalogue », « praticien » | un opticien vend des montures et fait des examens ; ces mots-là se lisent comme une lettre d'assurance. |

## 5 · La ligne laissée de côté, et pourquoi

**« Je vous ai préparé un aperçu personnalisé avec vos horaires. »** C'est le meilleur mot du texte reçu :
il change une offre en livraison. Il n'a pas été écrit parce qu'**aucun aperçu n'existait** au moment
d'écrire. Trois façons de le rendre vrai, consignées dans `sales/LOT-2-2026-10-27.md` §8 : une maquette
par prospect (10–15 min), une maquette par quartier (3 maquettes), ou rien — on garde « un mot et je
l'envoie ? ». Avis donné : la deuxième, et pour le LOT 3 seulement, pour ne pas changer la promesse au
milieu d'une mesure.

## 6 · La règle ajoutée

> Un message froid nomme **un fait daté** (la preuve), **l'endroit où le patient le lit** (l'ancrage), et
> **ce que ce patient fait ensuite** (le comportement). Le fait sans le comportement est un audit ; le
> comportement sans le fait est un tract.

La porte le mesure déjà pour l'ancrage et la cause ; le comportement, lui, se juge à la lecture — il n'y
a pas de porte pour ça, et c'est dit ici pour que personne ne croie qu'il y en a une.

## 7 · Ce que ce document ne prouve pas

Aucun taux. Le texte reçu n'a jamais été envoyé par nous, et les cinq de v6 ne sont pas partis au moment
d'écrire. La seule mesure qui tranchera est `réponses < 48 h` sur `sales/CAMPAGNE-VOLUME-2026-10-26.md` §5.

## 5 · Le compte était faux, et il est corrigé (26/10, soir)

Ce document a d'abord annoncé **116 mots**. Recompté sur le texte verbatim, avec l'outil qui fait foi :
**72 mots**. Les 116 venaient d'un compte à la main, jamais revérifié — exactement ce que ce dépôt
s'interdit ailleurs : *aucune statistique sans source*. Un chiffre faux dans un document de méthode est
plus coûteux qu'un chiffre absent, parce qu'il circule ensuite dans le lot, dans la PR et dans la note.
Corrigé ici et dans les quatre endroits qui le reprenaient (`sales/LOT-2-2026-10-27.md`,
`knowledge/DEUX-TEXTES-RECUS-2026-10-26.md`, `sales/Activity-Log.md`).

## 6 · L'ordre, qui est la seule chose vraiment transposable

Un message froid se lit dans cet ordre, sinon il se referme :

1. **Le monde du prospect** — où son patient cherche vraiment, aujourd'hui, sans qu'on le lui reproche ;
2. **la perte, côté patient** — ce qu'il rate, jamais ce qu'il fait mal ;
3. **le fait daté et sourcé** — la preuve qu'on a regardé *ce* cabinet et pas un modèle ;
4. **la permission** — une seule question, une seule action.

C'est l'ordre du texte reçu, sauf qu'il lui manque les étapes 3 et 4 (aucun fait daté, et sa question
finale ne demande aucune action). Nous avions les étapes 3 et 4 et pas la 1 : nos cinq messages de
l'après-midi ouvraient sur un défaut du cabinet.

**L'essai, mesuré, sur le seul lot qui n'est pas parti — ① Free Optic :**

Avant (v9, 68 mots, 0 bloquant — mais il ouvre sur le défaut) :

> Bonjour, inattendu : à Akwa, votre page Facebook annonce un site à votre nom, et le lien ne répond pas —
> deux essais aujourd'hui. / Le patient qui vous trouve là clique, tombe sur une page vide, et rappelle
> l'annuaire. / Je fais les sites pour les opticiens de Douala : horaires, montures et un bouton qui écrit
> vraiment. / L'aperçu du site ne coûte rien, votre adresse dessus : un mot et je l'envoie ?

Après (v10, **65 mots, 0 bloquant, 0 avertissement** — même fait, même source, ordre inversé) :

> Bonjour, inattendu : à Akwa, on cherche votre nom sur son téléphone.
> Votre page Facebook annonce un site à votre nom, et le lien ne répond pas : il clique, tombe sur une page
> vide et rappelle l'annuaire.
> Je fais les sites pour les opticiens de Douala, horaires et montures au même endroit.
> L'aperçu du site ne coûte rien, votre adresse dessus : un mot et je l'envoie ?

Seule la première phrase change de sujet : l'endroit où le patient le cherche, au lieu de ce qui manque au
cabinet. Le défaut arrive en deuxième, adossé à un fait vérifiable, et il devient une perte de patient au
lieu d'un reproche.

## 7 · Ce que ce document ne prouve pas

Rien, commercialement. Un texte reçu, zéro mesure de réponse. Ce qui est mesuré ici, c'est la **forme** —
mots, phrases, ordre, ancrage — et un écart de compte corrigé. Ce qui ne l'est pas : qu'un ordre inversé
fasse répondre davantage. Seul un lot qui part avec les deux ordres, compté à J+7, le dira.
