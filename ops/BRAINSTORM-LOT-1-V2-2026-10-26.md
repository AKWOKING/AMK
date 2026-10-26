# BRAINSTORM — les deux captures ont démenti les deux meilleurs messages (26/10/2026)

```text
Étape 0  graphe rejoué 26/10 12 h (13 087 nœuds) · PRE-FLIGHT lu §0 · §8b · §8c · §13
Entrée   les cinq captures de King : Google (AI Overview + Maps) sur ①, Google + le site de
         Facebook sur ②
Sortie   deux messages réécrits, une règle de vérification ajoutée, un risque de voisinage nommé
```

## 1 · Ce que le pré-vol disait, et ce que les captures disent

| Ce que je croyais | Ce que la capture prouve | Conséquence |
|---|---|---|
| ① Google ne relie pas « Ets Espace Médical » et « Optic Medical Favour and Joy » | l'AI Overview écrit « **also known as** Ets Espace Médical » | le fait est faux : message réécrit |
| ① le cabinet n'a aucune présence numérique tenue | fiche Google : **4,0, 3 avis, photos, horaires** | l'angle « vous n'existez pas » est mort aussi |
| ② « Ambassador Vision » ne sort pas sur Google | LeFish 17/10, DoualaTour ×2, Cameroon Business Directory, Maligah, **Facebook 355 abonnés** | le fait est faux : message réécrit |
| ② un seul numéro public | **trois** numéros différents (699 86 02 02 · 696 21 41 20 · 675 39 90 23), plus un ancien fixe | **le fait de remplacement était dans la capture** |

**Ce que ça coûte, chiffré** : deux messages sur cinq refaits après coup, une demi-heure de travail, et
surtout — si on n'avait pas cherché, **deux messages partis sur un fait faux, vers deux cabinets qui
tiennent leur fiche**. Ce n'est pas une perte, c'est exactement ce que la recherche devait acheter.

## 2 · La décision qui reste à prendre : trois façons de remplacer l'angle mort

| | **A · garder l'angle du nom, « en plus doux »** | **B · basculer sur « ce que le web dit de vous »** | **C · parquer les deux, envoyer ③④⑤ d'abord** |
|---|---|---|---|
| Ce qu'on gagne | rien de neuf, mais on ne perd pas la demi-heure | deux faits vrais, datés, rejouables | zéro risque, et trois messages partent |
| Ce qu'on perd | la crédibilité : le prospect peut vérifier en 10 s | il faut que le fait soit **certain** | ① et ② sont les mieux documentés du CRM (3/3) : on met les meilleurs de côté |
| Le risque | une réponse « essayez, ça marche » = conversation morte | un fait mal choisi = la même chose | la recherche devient une raison de ne pas envoyer |

**Ce que la recherche du 26/10 a déjà coûté en crédibilité** : rien, parce que rien n'est parti. C'est le
seul avantage d'écrire avant d'envoyer.

## 3 · La règle que ces deux cas écrivent, et qui vaut pour tout le stock

> **Un message qui affirme « Google ne vous voit pas » se vérifie AVANT l'envoi, pas après.**
> Sur quatre angles de nom testés ce matin, **deux étaient faux** — et les deux étaient les plus
> convaincants à l'écrit.

Ce n'est pas une précaution de style, c'est une règle de mesure : nous n'avons **aucun** outil qui
interroge Google (le réseau de cet environnement s'arrête à GitHub, npm et PyPI), donc toute affirmation
sur ce que Google montre repose sur une capture de King, datée. Sans capture, la phrase ne s'écrit pas.

**Corollaire pour la fabrique** : `compose.py` ne produit que deux angles — « le nom » (quand le profil
WhatsApp diffère du nom de l'Ordre) et « l'offre » (une page du métier). Les deux angles « nom » du lot
volume reposent sur la même hypothèse, et elle vient d'être démentie deux fois. **Le filtre `--ecarter`
ne protège pas de ça** : il écarte le mort et le hors-cible, pas le fait faux.

## 4 · Le fait de remplacement — la règle qui l'a choisi

Trois candidats pour ②, un seul retenu :

| Candidat | Vrai ? | Rejouable par le prospect ? | Actionnable en un mot ? | Retenu |
|---|---|---|---|---|
| l'adresse diverge (Bali vs Akwa, BP 1301 vs 12810) | oui | oui | non — et c'est peut-être un déménagement, donc leur fait | **non** |
| 355 abonnés Facebook, page active | oui | oui | non — c'est un compliment | **non** |
| **trois numéros publics différents** | oui, trois captures | oui | **oui** : « lequel sonne ? » | **oui** |

**Le critère qui tranche** : le fait doit produire une réponse **d'un mot** qui nous apprenne quelque
chose que nous ne savons pas. « Lequel sonne encore ce soir ? » nous dit quelle ligne est vivante —
c'est-à-dire si le 675 39 90 23 est une ligne de travail ou un vieux compte.

## 5 · Ce que le brainstorm a trouvé sans le chercher — les deux voisins

**AMBASSADOR Vision** : « Bali, côté Hôtel Serena ». **bellevueoptique** : « Bali, Serena Hôtel, rue des
pavés ». Deux de nos cinq prospects sont dans le même bloc.

| Le risque | La règle |
|---|---|
| deux messages qui se ressemblent à deux voisins = signature de diffusion | angles différents (numéros pour ②, adresse pour ④) et **un jour d'écart** |
| citer l'un à l'autre pour faire du social proof | **jamais** : c'est une preuve fabriquée (§8c) |
| l'un répond mal, l'autre le sait avant nous | l'écart d'un jour est aussi un écran |

## 6 · Décision

1. **① et ② sont réécrits** (53 et 54 mots, 0/0), avec les faits de la capture du 26/10, et la v1 reste
   dans le fichier avec sa raison de refus — on ne supprime pas un fait faux, on le date.
2. **③④⑤ ne bougent pas**, mais passent à la même vérification : leurs trois requêtes sont dans le
   fichier, et six phrases de rechange sont déjà écrites et contrôlées.
3. **La règle du §3 entre dans le lot**, pas dans une note : « un message qui affirme que Google ne voit
   pas se vérifie avant l'envoi ».
4. **Les voisins** : un jour d'écart, deux angles, et aucune mention croisée.
5. **Chaque trouvaille devient une preuve** : `leads/RECHERCHE-LOT-1-2026-10-26.csv`, six lignes
   (type, preuve, source, date, ce que ça change). Sans trace, une recherche est une recherche qu'on
   refera.

## 7 · Ce qui reste ouvert

- **③④⑤ ne sont pas vérifiés** : le même démenti peut les attendre, et il coûtera une rechange, pas une
  réécriture — les phrases sont déjà écrites.
- **Le numéro de ② n'est publié nulle part ailleurs.** Ce n'est pas un arrêt (le profil WhatsApp est bien
  à eux, vu le 25/10), mais si la réponse est « ce n'est pas notre numéro », la ligne se barre.
- **Aucun taux n'est mesuré sur WhatsApp** : les 4,4 % et 7,8 % viennent de 500 courriels de 2026. Le
  seul chiffre qui décidera est `répondu < 48 h`, et il vaut **0**.
