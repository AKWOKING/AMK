# HUMANIZER SUR EP01 — les tics trouvés dans la v5, et ce qu'on en a fait

```
Outil     blader/humanizer (MIT, pin 8c307f3) → ~/.agents/skills/humanizer/SKILL.md
Méthode   26 motifs « Signs of AI writing » : marquer, réécrire, relire, vérifier les ajouts
Source    King, 26/10 : « the video looks good but I think we can improve the phrasings and the
          script to sound less robotic and more human »
Portée    le TEXTE PRONONCÉ d'EP01 (les six beats), pas les libellés d'écran
Écrit     26/10/2026, tour 151
```

## 1 · Pourquoi la v5 sonnait robotique (et ce n'est pas une impression)

Le skill explique le mécanisme : un modèle écrit **ce qui convient au plus grand nombre**, un humain
écrit **pour une personne**. Chaque défaut ci-dessous est une forme de ce choix par défaut. Sur six
phrases, j'en ai trouvé **cinq motifs forts** — c'est beaucoup pour 50 mots, et c'est cohérent avec ce
que King a entendu.

| # | Motif (skill) | Où, dans la v5 | Pourquoi ça sonne faux à l'oral |
|---|---|---|---|
| §2 | **fragment théâtral / closer d'une ligne** | « Pas vous. » (fin du hook) | à l'écrit, ça frappe ; à l'oral, ça fait une pause de présentateur |
| §6 | **triade forcée** | « Horaires, adresse, WhatsApp. » | trois mots alignés pour faire complet ; personne ne les énumère comme ça |
| §7 | **ouvertures répétées** | « Votre patient… / Il appelle… / Sa fiche… / La vôtre… » | quatre phrases qui démarrent sur le même moule |
| §8+ | **les deux-points comme connecteur universel** | « Sa fiche : un site, douze avis. » · « Horaires et fiche : dix minutes » | c'est de la typographie de panneau, pas de la parole |
| §16 | **langage de vente** | « gratuit » posé seul en fin de phrase | un mot d'annonce, pas une phrase qu'on dit |
| — | **précision écrite** | « l'un des deux », « vingt-deux heures » | on dit « l'autre », « 22 heures » (ou « le soir ») |

**Ce que je n'ai PAS trouvé**, et c'est important : aucune surenchère (§13), aucune autorité empruntée
(§17), aucun tiret cadratin (§8 — le dépôt l'interdit déjà), aucun résidu de chatbot (§22). Le problème
n'était pas l'inflation, c'était **la cadence et la ponctuation**.

## 2 · La réécriture, beat par beat

| Beat | v5 (écrit) | v6 (parlé) | Ce qui a changé |
|---|---|---|---|
| hook | « Votre patient tape opticien Akwa. Il appelle **l'un des deux**. Pas vous. » | « Votre patient tape opticien Akwa. Il appelle **l'autre**, pas vous. » | « l'un des deux » (écrit) → « l'autre » (parlé) ; le fragment devient une apposition, **ce que fait la langue orale** |
| spike1 | « Sa fiche **:** un site, douze avis. La vôtre **:** un nom. » | « Sa fiche a douze avis. La vôtre **n'a qu'**un nom. » | plus de deux-points : deux phrases avec un verbe, comme on parle |
| release1 | « Horaires et fiche **:** dix minutes, gratuit. » | « Les horaires, **ça se change** en dix minutes. **Sans moi.** » | le cadeau devient **une capacité du client**, pas une annonce de prix ; « sans moi » est la générosité, dite en deux mots |
| spike2 | « Ce n'est pas le site. Il veut venir ce soir. » | « Le soir, il veut venir. **Et personne ne répond.** » | le « Not X but Y » disparaît ; la phrase devient une **scène**, pas un contraste |
| release2 | « Un site répond à vingt-deux heures. Horaires, adresse, WhatsApp. » | « Une page avec vos horaires **répond à votre place**. » | la triade tombe ; « à votre place » dit le bénéfice au lieu d'énumérer des champs |
| cta | « Écrivez APERÇU sur WhatsApp. » | « Écrivez APERÇU. **Vous voyez votre page avant de payer.** » | le CTA porte enfin **sa récompense** (voir §4) |

## 3 · Ce que la réécriture n'a pas le droit de faire (et n'a pas fait)

- **Aucun fait ajouté.** « Douze avis » vient de la capture Optix du 24/10 ; « dix minutes » de la
  capture des trois champs ; rien d'autre n'est chiffré.
- **Aucune promesse nouvelle.** Pas de « votre fiche sera créée », pas de classement, pas de délai de
  livraison.
- **Aucune familiarité fabriquée.** On ne dit ni « mon frère » ni « on est ensemble » : la copie
  camerounaise est « chaude, directe, spécifique » (`HOUSE` §8), pas du mimétisme d'accent.

## 4 · Le CTA : ce que King a mis le doigt dessus

> *« when you close with "Écrivez APERÇU sur WhatsApp" they should write that to do what ?? »*

Il a raison, et c'est un défaut de **contrat**, pas de style. « Écrivez APERÇU » décrit **l'action** ;
il ne dit ni ce qu'on **reçoit**, ni ce que ça **coûte**, ni ce qui se passe **après**. Le playbook
répond à ça… dans le message d'accueil WhatsApp (`PLAYBOOK` §4.2), c'est-à-dire **là où le spectateur
n'est pas encore**.

**La correction retenue** : la voix promet **une chose vérifiable** — *vous voyez votre page avant de
payer* — et l'écran porte le détail que la voix n'a pas le temps de dire :

> **ÉCRIVEZ APERÇU** · on regarde votre fiche · vous voyez votre page · vous décidez après

Pourquoi pas « on vous crée votre fiche Google » (la formulation proposée par King) : créer une fiche
Google Business passe par une **vérification que Google contrôle** (courrier, téléphone, parfois
refusée). Promettre la création, c'est promettre un résultat qu'on ne tient pas — et le dépôt a déjà
vécu ça le 24/09 (`MESSAGES` §2 : « beaucoup de manquement », et le client avait raison). On **regarde**
la fiche, on publie les horaires avec lui, on ne promet pas la validation.
**Si King préfère la promesse directe, il tranche** : c'est son nom sur le message, et la ligne est
isolée dans la v6 pour être changée en une minute.
