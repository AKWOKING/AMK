# UNIVERS OPTIQUE — le pivot : « pas un site, un outil d'essayage »

**Écrit le 25/09/2026** (retour de King après le rendez-vous de 10 h). Ce document ne remplace pas
`sales/RDV-UNIVERS-OPTIQUE-2026-09-25.md` : il note **la nouvelle demande**, dit **ce qui est faisable et
comment**, et liste **ce qu'on doit encore demander** avant d'écrire une ligne de code.

---

## 1 · Ce qu'il a dit, mot pour mot (tel que King le rapporte)

> « ils ne veulent pas d'un site mais quelque chose de différent. Leur problème : **quand un client vient,
> ils passent énormément de temps à essayer toutes les montures disponibles**. Ils veulent une solution qui
> leur fasse gagner du temps. **Il a suggéré une application** (web / mobile / desktop) où il peut **téléverser
> toutes les montures qu'il a en stock** et **retirer celles qui ne sont plus disponibles**, et où **quand un
> client vient pour une monture, il prend une photo du client, et le client peut faire défiler les photos de
> lui-même avec les différentes montures disponibles**. Il choisit ensuite sur ce qu'il voit. »

**Traduction en une phrase** : il ne veut pas qu'on lui *raconte* son cabinet sur une page — il veut qu'on lui
**retire une douleur qu'il vit tous les jours**. Et il a raison : c'est un vrai problème, il est chiffrable, et
il est **le même dans les cinquante autres boutiques d'optique de Douala**.

---

## 2 · Ce qui est faisable — et la preuve

**Verdict : oui, c'est faisable, et beaucoup plus vite qu'il ne l'imagine.** Pas besoin d'application à
installer : **une page web** privée, qui s'ouvre sur le téléphone du comptoir ou sur son ordinateur, se met en
favori, et fonctionne **sans installer quoi que ce soit**. Aucun magasin d'applications, aucune mise à jour à
faire à la main.

**La preuve est faite ce soir** — la planche `clients/univers-optique/essai-maquette.png` : une photo frontale
(prise au téléphone), et **trois montures posées dessus**, à la bonne échelle, sur les yeux, avec un léger voile
de verre pour que la monture ne « flotte » pas. Ce n'est pas un montage fait main : c'est le résultat du
**même procédé que celui que la page fera toute seule** — mesurer le visage sur la photo, mesurer la monture sur
sa photo produit, décaler de l'échelle, découper le fond, poser.

Le principe, en cinq étapes, pour qu'il puisse le vérifier avec nous :

| | L'étape | Pourquoi ça marche |
|---|---|---|
| 1 | **Il photographie une monture** (sur un fond clair, de face, une fois) | une monture, en photo produit, c'est une image **très simple** : deux verres, une monture, presque rien qui bouge |
| 2 | **Le logiciel la détoure et la mesure** (ouverture des verres, largeur totale) | c'est automatique et il corrige d'un geste si besoin (le pont, la largeur) |
| 3 | **On photographie le client** de face, au comptoir, une fois | deux secondes, sans matériel : c'est la photo qu'il a déjà l'habitude de prendre pour ses dossiers |
| 4 | **La page pose les montures sur cette photo** | elle **cherche le visage** (les yeux, la largeur aux tempes) et **ajuste l'échelle de chaque monture** en conséquence |
| 5 | **Le client fait défiler** à droite et à gauche, **met ses trois préférées de côté**, et repart avec sa sélection | c'est le geste qu'il fait déjà avec les vraies montures — sauf qu'ici, il en voit **cent en deux minutes** au lieu de vingt en un quart d'heure |

**Ce que ça change concrètement pour eux** : le temps d'essayage passe de **20-30 minutes à 3-5 minutes**, le
client voit **tout son stock, pas les huit montures du présentoir**, et le vendeur reste assis — la boutique ne
se transforme plus en gymnastique.

### Les faiblesses du procédé, dites avant de commencer (parce qu'il les verra)

- **Les branches n'apparaissent presque pas** derrière l'oreille : on ne les dessine pas, on les suggère. C'est
  exactement ce que font les outils de Warby Parker et de Zenni quand on n'est pas parfaitement de face.
- **S'il a une frange ou un gros chignon**, le contour des oreilles manque — on ajuste, on ne promet pas.
- **Une monture photographiée de biais** ou sur un fond sombre se pose mal. D'où **la fiche de prise de vue**
  (une page, avec un repère à imprimer) qu'on lui laissera.
- **La photo du client doit être frontale.** Face à la vitre, lumière du jour : dans une boutique, ça se fait
  en deux secondes — mais il faut lui dire **comment** (la fiche le dit aussi).
- **Ce n'est pas de la 3D.** On ne verra pas la monture bouger quand il tourne la tête. **Ça viendra en option**,
  après, si le stock est bien photographié — pas avant, pour ne pas promettre ce qui déçoit.

---

## 3 · La question qu'il n'a pas posée, et qui est la vraie : **où sont les montures ?**

Il croit que sa douleur est « le client essaie longtemps ». **La moitié de son temps est ailleurs** : chercher
la monture dans le tiroir, la ressortir, la remettre, compter la plaque. Un outil qui montre les montures sur un
visage mais **ne dit pas où elles sont rangées** lui fait gagner la moitié du temps seulement.

**Donc la version qui gagne vraiment tient en deux gestes de plus :**

1. **Un numéro d'emplacement** collé sur chaque présentoir (« R1-04 ») et **une étiquette** discrète par monture.
2. Quand le client en voit une qui lui plaît, l'écran affiche **« présentoir R1, case 04 »** — le vendeur tend
   la main sans chercher.

Ça, c'est **dix minutes de travail** dans l'outil, et c'est ce qui transforme « un gadget sympa » en **outil de
comptoir**. Il faut le lui proposer — en le lui demandant, pas en le lui imposant (voir §6, question 3).

---

## 4 · La photo du client : deux façons, et une recommandation

| | **① Au comptoir** *(recommandé)* | **② Sur son propre téléphone** |
|---|---|---|
| Qui prend la photo | le vendeur, avec l'appareil du comptoir | le patient, dans l'outil, avec son téléphone |
| Le client voit la photo | sur l'écran du comptoir ou du vendeur | sur son propre écran |
| Le résultat lui reste | non — mais on peut le lui envoyer | oui, il repart avec |
| La qualité de la photo | maîtrisée (même mur, même lumière, même distance) | variable |
| Ce que ça vaut | **le geste de comptoir**, celui qui remplace l'essayage | **le lien qu'on envoie** — le client montre à sa famille avant de décider |

**Recommandation : les deux, mais pas en même temps.** On construit **le comptoir** d'abord (c'est ça qui lui
fait gagner du temps), et **le lien à envoyer** ensuite — c'est le même moteur, plus une adresse à ouvrir. Le
deuxième est d'ailleurs celui qui rapporte le plus au bout d'un mois : un client qui part avec sa sélection
**revient avec la décision de sa famille déjà prise**.

---

## 5 · Ce qu'on construit, en deux temps

### V1 — le prototype qu'il peut toucher (2 à 3 jours de travail, pas de dépendance à installer)

- **Sa boutique** : liste des montures, ajout / retrait (**« cette monture est vendue » en un geste** — c'est
  exactement ce qu'il a demandé), avec **photos prises par lui** depuis son téléphone.
- **La cabine d'essayage** : photo du client → détection du visage → défilement des montures (glissement au
  doigt, comme sur la page de La Ligne) → **trois favorites** → partage.
- **Un écran de fin** : « vos trois montures » + l'emplacement en rayon (§3 si il le veut).
- **Tout fonctionne hors ligne** (le comptoir n'a pas besoin de réseau) et **aucune photo ne quitte son
  téléphone** — c'est une phrase à dire, et une vraie raison d'achat.

### V2 — ce qui se vend ensuite (et ce n'est pas la même somme)

- les **étiquettes et les emplacements** (le vrai gain de temps),
- le **lien client** (le patient repart avec sa sélection),
- le **dépouillement mensuel** : quelles formes partent, quelles montures dorment depuis six mois — **le
  premier chiffre qu'il n'a jamais eu sur son propre stock**.

---

## 6 · Ce qu'il faut lui demander (les réponses changent le travail)

1. **Sur quoi ça tourne au comptoir ?** Android, tablette, ou l'ordinateur de la caisse ? *(Ça change la mise
   en page et la façon de tourner la page.)* — et **a-t-il du réseau au comptoir** ?
2. **Combien de montures en rayon, et combien il en tourne par mois ?** *(Cent ou cinq cents, ce n'est pas le
   même outil — et c'est le chiffre qui donne le prix.)*
3. **Veut-il la version « où est rangée chaque monture » ?** *(Dix minutes de plus dans l'outil, la moitié du
   temps gagné.)*
4. **La photo du client : au comptoir, ou sur son téléphone à lui ?** *(Voir §4 — on construit les deux, mais
   l'un après l'autre.)*
5. **Est-ce qu'il accepte de photographier cinq montures cette semaine**, pour qu'on lui revienne avec **un
   vrai prototype sur ses propres montures** ? *(C'est la demande qui engage : cinq photos, dix minutes, et à la
   fin il voit son stock à l'écran.)*

---

## 7 · Le prix, la vraie question — et elle n'appartient qu'à King

**Ce qu'il faut dire sans détour : l'outil n'est pas le site.** Le site est posé à **100 000 FCFA** (21/09, et
il ne bouge pas). L'outil d'essayage est **un autre métier** : il y a une saisie de stock, des photos, un
algorithme, et surtout **une économie quotidienne** — il ne se vend pas au prix d'une page.

Trois façons de le poser, à trancher avant de le lui proposer :

- **① L'outil est le produit principal** — prix plus élevé, mis en place, et **un abonnement** (les montures
  changent tous les mois : c'est un outil vivant). Le site devient une **ligne séparée**, à re-proposer plus tard.
- **② L'outil est le pied dans la porte** — mis au prix d'une page, en échange de quoi Univers est **le client
  pilote** : ses montures servent de vitrine, et on peut montrer l'outil aux autres opticiens de Douala.
- **③ On ne le vend pas tout de suite** — le prototype d'abord, gratuit et privé, et le prix se pose quand il a
  vu la bête tourner sur son propre stock.

**Le piège à éviter** : résoudre gratuitement le problème payant. Le prototype est un **livrable de
démonstration**, sur **cinq** montures ; **son stock entier, ses étiquettes et son suivi de vente, c'est le
travail qu'on vend** (règle Hormozi, `sales/PLAN-2026-09-24-25.md` §4).

**Et une certitude, qui vaut d'être dite** : les dix-huit autres opticiens de la campagne ont le même problème.
Si l'outil tient pour Univers, **il se revend tel quel** — c'est le premier objet de ce dépôt qui soit un
**produit** et pas une prestation.

---

## 8 · Ce que ce pivot ne dit PAS — et qu'il ne faut pas lire de travers

- **Il n'a pas dit que le site était mauvais.** Il a dit qu'il **ne voulait pas d'un site *maintenant***, parce
  qu'il a une douleur plus concrète. La page reste **la maison** de l'outil (c'est là qu'on met un lien « essayez
  chez vous »), mais on ne le pousse pas aujourd'hui : on l'a déjà payée de son attention une fois.
- **Il n'a rien signé.** Les 50 000 d'acompte n'ont pas été pris : c'est un rendez-vous qui a changé de sujet,
  pas un client perdu. Le CRM doit dire **exactement ça**, sans embellir.
- **Aucune promesse n'a été lâchée sur place** : ni délai, ni prix, ni « ça se fait en trois jours ». Le
  prototype a une date **parce qu'on l'aura tenue**, pas parce qu'on l'a annoncée.

---

*Écrit par AMK le 25/09/2026 — la planche (`essai-maquette.png`) est la preuve technique montrée à King ; elle
n'est pas destinée au client.*
