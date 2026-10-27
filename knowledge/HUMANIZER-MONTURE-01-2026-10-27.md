# HUMANIZER SUR « LA MONTURE CHERCHE SON NOM » — les tics des six lignes, et ce qu'on en a fait

```
Outil     blader/humanizer (MIT, pin 8c307f3) → ~/.agents/skills/humanizer/SKILL.md  (installé 27/10)
Méthode   26 motifs « Signs of AI writing » : marquer, réécrire, relire, vérifier les ajouts
Demande   King, 27/10/2026 : « the script needs to go through humanizer and roast room »
Portée    le TEXTE PRONONCÉ des six beats — pas les libellés d'écran, pas le kit
Écrit     27/10/2026, tour 199
```

## 1 · Ce que le skill a trouvé dans la v5 (celle qui est en ligne dans le film v4)

Six phrases, **cinq motifs forts**. Sur 80 mots, c'est beaucoup — et c'est cohérent avec ce que King
entend : ça sonne écrit.

| # | Motif (skill) | Où, dans la v5 | Pourquoi ça sonne faux à l'oral |
|---|---|---|---|
| §6 | **triade forcée** | « Écrivez A, B, ou votre mot. » | trois items alignés pour faire complet ; personne ne les énumère comme ça en parlant |
| §8 | **les deux-points comme connecteur universel** | « Deux noms sont sur la table : Éclat ou Minuit. » | c'est de la typographie de panneau, pas de la parole |
| §7 | **ouvertures répétées** | « **Elle** n'a pas… / **Elle** ira… / **Elle** mérite… » | trois phrases qui démarrent sur le même moule dans six lignes |
| §2 | **fragment théâtral** | « Sur notre site, quarante montures. » | un nom posé sans verbe : ça se lit, ça ne se dit pas |
| §11 | **sujet absent / passif** | « **On** vous montre le nom qui gagne. » | le spectateur est le complément de sa propre récompense |
| — | **précision écrite** | « H zéro huit » / « celui qui reste » | on dit « la H08 » ; « celui qui reste » est une jolie formule, pas une phrase qu'on dit |

**Ce que je n'ai PAS trouvé** : aucune surenchère (§13), aucune autorité empruntée (§17), aucun tiret
cadratin, aucun résidu de chatbot (§22), aucun gras décoratif. Le problème n'était pas l'inflation —
c'était **la ponctuation et le sujet des phrases**.

## 2 · La réécriture, beat par beat

| Beat | v5 (ce qui est dans le film v4) | v6 (parlé) | Ce qui a changé |
|---|---|---|---|
| 1 | « Elle n'a pas de nom. Vous choisissez celui qui reste. » | « Elle n'a pas de nom. **C'est vous qui** choisissez celui qui reste. » | le sujet est **posé** au lieu d'être sous-entendu ; « c'est vous qui » est la tournure orale du français de Douala |
| 2 | « Sur notre site, quarante montures. Toutes s'appellent par un code. » | « Sur notre site, **il y a** quarante montures. **Chacune a un code à la place d'un nom.** » | le fragment prend un verbe ; « s'appeler par un code » (faux) → « un code à la place d'un nom » (vrai, et plus dur) |
| 3 | « Celle-ci s'appelle H zéro huit. Deux noms sont sur la table : Éclat ou Minuit. » | « **Celle-là, c'est la H08. On lui a déjà trouvé deux noms. Éclat, et Minuit.** » | plus de deux-points ; « on » = le cabinet, un humain ; les noms tombent en apposition, comme on les dit |
| 4 | « Elle ira sur un visage, tous les jours. Elle mérite mieux qu'un code. » | « Demain, **quelqu'un la portera du matin au soir**. Elle mérite mieux que H08. » | « tous les jours » (notion) → « du matin au soir » (scène) ; « mieux qu'un code » → « mieux que H08 » (précis) |
| 5 | « Le nom qui gagne s'écrit sur sa page, et il y reste. » | « **Le nom qui gagne reste. Il ne part pas avec la vidéo.** » | la phrase passive devient une promesse qu'on peut tenir, et elle dit **ce que ça change** |
| 6 | « Écrivez A, B, ou votre mot. On vous montre le nom qui gagne. » | « **Écrivez A ou B. Si vous avez mieux, votre mot. Mardi, vous voyez le nom sur sa fiche.** » | la triade tombe ; le spectateur devient **sujet** de sa récompense ; une **date** est donnée |

Trois « Elle » en ouverture → **deux**. Un deux-points → **zéro**. Une triade → **zéro**. Un « on » qui
prend la place du spectateur → **le spectateur**.

## 3 · Ce que la réécriture n'a pas le droit de faire (et n'a pas fait)

- **Aucun fait ajouté.** « quarante montures » est vérifié dans `hosting/previews/dmoptic/montures/` (40
  fiches) ; « H08 », « Éclat », « Minuit », la fiche, le mardi : tout est déjà au dossier. Rien d'autre.
- **Aucune promesse nouvelle.** Le nom s'écrit sur la fiche — c'est fait à la main par le cabinet, c'est
  tenable. Aucune remise, aucun délai de livraison, aucun résultat de vue.
- **Aucune familiarité fabriquée.** Pas de « mon frère », pas de « on est ensemble » : la règle `HOUSE` §8
  (chaude, directe, spécifique) ne s'imite pas par l'accent.
- **Le vouvoiement est homogène** sur les six beats — aucun tutoiement, y compris dans les libellés.

## 4 · Ce qui reste, et qu'on assume

- **« celui qui reste »** est un *closer* (§2). Il reste : c'est le mot **objectif** de l'accroche, celui
  que la porte `audit_hook` exige, et la seule partie de la phrase qui promet quelque chose (« il reste »).
  Le supprimer ferait une accroche qui constate sans rien offrir — refusée par la porte.
- **« Il ne part pas avec la vidéo »** est un contraste (§1). Il reste pour la même raison : c'est **la
  récompense** du jeu, et c'est la seule qu'on puisse tenir sans dépenser un franc.

## 5 · Ce que le skill ne fait pas

Il ne fait pas passer un détecteur d'IA, et l'amont ne le prétend pas. Il enlève les tics d'écriture
automatique ; il ne rend pas un texte camerounais à ma place. Le reste est du métier : la scène, la
preuve, la date.
