# Ce qui fait dire oui — la comparaison du 26/10, texte reçu contre texte écrit

**Origine.** King envoie le 26/10 un message écrit ailleurs (116 mots, quatre paragraphes) et pose la
question qui vaut mieux qu'un audit : *« à la place d'un opticien, tu ne dirais pas oui ? »*.

**Ce que ça change dans la méthode.** Le fait daté reste la preuve — c'est ce que ce texte n'a pas, et
c'est ce qui le rend jetable. Mais la preuve seule parle de la fiche du prospect, pas de sa journée. Un
cabinet ne se reconnaît pas dans un constat sur son annuaire ; il se reconnaît dans **un patient qui
s'en va**. v6 ajoute ce patient en cinq mots, et ne retire rien.

## 1 · Le verdict de la porte, sur le texte reçu

`tools/qa/audit_outreach.py` : **116 mots, 5 phrases → BLOQUÉ**, quatre motifs (longueur, nombre de
phrases, une phrase sans ancrage, aucune cause nommée). La forme échoue. Le fond gagne deux points, et
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
