# ISEE — la réparation, et ce qu'on dit maintenant (26/10/2026)

```text
ÉTAPE 0   graphe rejoué 26/10 14 h 33 (13 262 nœuds) · §13 · PREUVE-VAGUE · ruling « pas de site »
DÉCLENCHEUR   King, 26/10 16 h : « seems we made a mistake and didn't search well they have a website
              https://iseecameroon.com/ — so what do we tell them now »
PORTE     python3 tools/qa/audit_outreach.py — nouvelle règle 11 (SITE-CHECK), 29/29 cas
PREUVES   iseecameroon.com ouvert le 26/10 (accueil, page-sitemap.xml) · Google « I See Better » ·
          profil WhatsApp Business ISEE · captures de King (26/10)
```

## 0 · Ce qui s'est passé, en clair

À 15 h 15, le premier message du LOT 1 est parti à ISEE avec cette phrase :

> « Le patient a cherché l'un, trouvé l'autre, et **aucune de ces deux vitrines ne lui permet de vous
> joindre directement**. »

**C'est faux.** `iseecameroon.com` existe depuis 2024 : boutique WooCommerce, collections avec prix,
**un bouton WhatsApp sur chaque monture**, une page « Prendre RDV », et les logos de six assureurs.

À 15 h 41, le cabinet a répondu « Bonjour ». À 15 h 45, King a promis une démo sous quelques minutes.
**Rien n'a encore été démenti côté client** : la correction part avant la démo, ou il n'y a plus de
conversation.

**Pourquoi on ne l'a pas vu.** Nous avons cherché « ISEE » et « I See Better » — deux noms. Le site
s'appelle **Isee Cameroun**, et le domaine ne contient ni l'un ni l'autre. Une recherche par nom exact
n'aurait jamais dû suffire : c'est la leçon, et elle est devenue une porte (tools/qa/audit_outreach.py,
règle 11).

## 1 · Le message à envoyer maintenant — tel quel

> Une chose d'abord, et elle est contre moi : j'ai écrit mon premier message avant d'ouvrir votre site.
> iseecameroon.com est en ligne, les collections y sont avec leurs prix, chaque monture a son bouton
> WhatsApp et vos assurances y figurent. Ce que j'ai dit des vitrines qui ne permettent pas de vous
> joindre est faux, je le retire — et la démo que je vous proposais n'a plus de sens.
>
> Ce qui reste vrai est plus petit : le site n'a pas bougé depuis le 14 novembre 2024, et trois noms le
> désignent — ISEE sur WhatsApp, I See Better sur Google, Isee Cameroon sur le site.
>
> Je ne vais pas vous vendre un site que vous avez déjà. Je peux vous envoyer une page, cinq lignes, sur
> ce que je toucherais dans celui-là et ce que je laisserais tel quel : la vitesse sur téléphone, votre
> fiche Google, la dernière mise à jour. Gratuit. Je vous l'envoie ?

**Pourquoi ça peut encore tenir debout.** Trois raisons, dans l'ordre d'importance :

1. **la correction arrive avant la découverte.** Un client qui apprend lui-même qu'on s'est trompé ferme
   la porte ; un client à qui on le dit avant garde la main, et juge la franchise, pas l'erreur ;
2. **elle est vérifiable** : les deux faits qui restent (dernière mise à jour, trois noms) se contrôlent
   en dix secondes, comme le reste de nos messages ;
3. **elle change l'offre au lieu de la répéter** : à un cabinet qui a déjà un site, on ne vend pas un
   site. On vend ce qui manque — et ce qui manque est petit, daté, et vrai.

**Ce que le message ne fait pas, volontairement** : il ne dit pas que le site est mauvais (il est bon),
il ne parle pas de classement Google (personne ne l'a mesuré), il ne promet pas de clients, et il ne
donne aucun prix.

## 2 · La page promise — cinq lignes, mesurables, à remplir en 15 minutes

C'est le livrable. Une page, cinq constats, chacun avec sa preuve et son chiffre. Rien d'autre.

| # | Ce qu'on mesure | Comment, en 15 min | Pourquoi ça compte pour lui |
|---|---|---|---|
| 1 | **Dernière mise à jour du site** | `iseecameroon.com/sitemap_index.xml` → 14/11/2024 pour les pages, 08/07/2024 pour les produits | un site figé depuis deux ans ne dit plus ses prix ni ses nouveautés |
| 2 | **Vitesse sur téléphone** | PageSpeed Insights sur l'accueil, onglet mobile → le score et le temps de chargement | un patient à Deido sur un forfait data abandonne avant la deuxième seconde |
| 3 | **Fiche Google** | chercher « I See Better Douala » sur un téléphone : propriétaire revendiqué ou non, catégories, horaires, photos, lien « Prendre RDV » | c'est là que 80 % des patients le trouvent, avant le site |
| 4 | **Les trois noms** | taper « ISEE », « I See Better », « Isee Cameroun » : est-ce que les trois mènent au même endroit ? | un patient qui hésite appelle le numéro qu'il a déjà sous la main |
| 5 | **Le parcours « Prendre RDV »** | le faire soi-même, sur téléphone, en se chronométrant | s'il faut plus de trois champs, il ne le fait pas |

**Ce qu'on ne met pas dans la page** : des recommandations générales, des captures d'écran sans chiffre,
et tout ce qui ressemble à un audit de 20 pages. Une page qu'il lit debout, entre deux patients.

## 3 · Ce qu'on vend à un cabinet qui a déjà un site

**Pas un site.** Le sien est complet, avec des prix et un bouton WhatsApp par monture : proposer de le
refaire, c'est insulter son travail et perdre la conversation.

**Ce qui reste, et qui est le vrai produit ici — `Suivi`, 30 000 FCFA/mois** (`knowledge/PRIX-2026-10-24.md` §5) :

- mises à jour du site et des prix, sauvegardes vérifiées, surveillance SSL et disponibilité ;
- **deux publications Google par mois** (nouvelle collection, horaires de fête, arrivage) ;
- le **rapport d'une page** — exactement la page du §2, chaque mois ;
- support WhatsApp sous 24 h.

C'est cohérent avec ce que le site est devenu : un magasin figé depuis novembre 2024, alors que les
collections et les arrivages changent, eux, chaque saison. Et c'est le prix déjà tranché pour DM Optique : il ne bouge pas.

**Si et seulement si** il demande un site neuf (refonte, e-commerce plus rapide, réservation en ligne) :
`Présence` 150 000, trois pages. On ne le propose pas le premier.

## 4 · Si la question du prix arrive

> L'aperçu et la page sont gratuits, je ne facture rien avant que vous décidiez. Ce que je fais ensuite,
> c'est le suivi du site et de la fiche : 30 000 par mois, mises à jour, deux publications Google, le
> rapport d'une page, et je réponds sur WhatsApp sous 24 h. Pas d'engagement de durée : vous arrêtez le
> mois où vous voulez.

Si « vous faites un prix ? » : **pas de remise** — on change le périmètre (une publication par mois au
lieu de deux, ou le site sans la fiche).

## 5 · Ce qu'on ne dit pas, même sous pression

| Interdit | Pourquoi |
|---|---|
| « Votre site est mal classé » | nous ne l'avons pas mesuré. On dit ce qu'on a vu : figé depuis le 14/11/2024 |
| « Vous n'avez pas de site » (ou « aucune vitrine ne permet de vous joindre ») | c'est ce qui vient d'arriver. Une phrase comme celle-là exige un SITE-CHECK daté, sinon la porte refuse le message |
| « Je vais vous amener des clients » | promesse de résultat invérifiable (ruling 142) |
| « C'est gratuit et sans engagement » | formule de vendeur, et elle ne dit rien de ce qu'on reçoit |
| Une démo de site neuf | il en a un. Une démo dit « jette ce que tu as » |

## 6 · Ce que cette erreur a coûté, et ce qu'elle a installé

**Coût** : un message faux chez un prospect chaud, qui a répondu « Bonjour » en 26 minutes — le meilleur
signe du lot jusqu'ici. Il est encore réparable ; il ne l'aurait plus été après la démo.

**Installé** : une **porte 11** dans `tools/qa/audit_outreach.py`. Un message qui affirme l'absence de
site doit porter, sous son titre, une ligne :

```text
SITE-CHECK 2026-10-26 · nom exact, nom WhatsApp, variantes, numéro, Google Maps → aucun site
```

Sans cette ligne, ou si elle dit « site trouvé », le message est **bloqué**. 29/29 cas passent, dont
deux nouveaux : l'absence non vérifiée, et le SITE-CHECK qui avoue avoir trouvé un site.

**La leçon du jour, en une phrase** : *on ne dit pas à quelqu'un ce qu'il n'a pas avant d'avoir cherché
par tous ses noms* — et il en a toujours plus d'un.

## 7 · Ce que ce document ne prouve pas

Le site d'ISEE est ouvert et daté ; sa **vitesse**, son **classement** et l'état de sa **fiche Google**
ne sont pas mesurés à cette heure. Les trois chiffres du §2 sont à prendre avant d'envoyer la page. Et
la réparation peut échouer : un cabinet à qui on avoue une erreur peut très bien ne jamais répondre.
