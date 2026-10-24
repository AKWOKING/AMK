# Le cercle du premier écran — décision de placement (24/10/2026)

> **Ce document est une courte note de conception**, écrite selon `tools/superpowers/skills/brainstorming`
> (« a small change → a short one: what you already covered together, written down »). Il tranche une
> question posée par King : *« la carte transparente, ou changer la position du cercle ? »*

## 1 · Ce qui est demandé, et pourquoi

Le client a écrit, capture à l'appui : *« Il y avait un cercle à peu près comme ce que j'ai dessiné.
C'était très bien. »* Le cercle n'est pas une décoration parmi d'autres : c'est **la seule pièce
graphique qui soit à lui**. Le reste de la page est du travail d'AMK sur ses photos et ses horaires.

King a déjà répondu au client en deux branches : *« 1. Je peux rendre la photo plus visible — 2. Je peux
retirer la photo et mettre le fond blanc qui avait le dessin. »* La question de ce soir est en aval :
puisque le cercle est là mais que la carte le mange, faut-il **rendre la carte transparente** ou
**déplacer le cercle** ?

## 2 · Ce qu'on voulait tous les deux, et ce que la mesure en dit

Les deux réponses ont été rendues et mesurées (Chromium, 1440 / 1280 / 1024 / 390). La mesure qui
compte n'est pas la géométrie du trait mais **l'encre réellement visible** : le dégradé `#sheen` va de
l'opacité 0 à 0,55 puis 0,38 puis 0 — un arc « géométriquement dehors » peut être transparent.

| Approche | Encre visible 1440 | Encre visible 1024 | Collisions titre / chapeau / boutons | Coût |
|---|---|---|---|---|
| **A** livré ce soir (autour de la carte) | 55 % | 61 % | 0 / 0 / 0 | — |
| **C** carte en verre 88 % + flou | 74 % | 63 % | 0 / 3 % / 2 % (**6 / 8 / 1 %** à 1024) | la fiche devient translucide |
| **D** cercle décalé sur le coin haut-droit | **75–79 %** | **48 %** (620 px) | **0 / 0 / 0** | rien |
| **F** retirer la photo, fond blanc, cercle à sa place d'origine | **21 %** | — | 0 / 0 / 0 | la photo du cabinet disparaît |

Deux résultats ont changé la décision :

1. **Le verre ne coûte presque rien au texte** (petit texte 7,37:1 contre 7,76:1, mesuré sur le fond
   réel de la carte) — mais il laisse **21 % de l'encre sous la carte** et, à 1024 px, le cercle
   commence à traverser le titre. Il rend surtout translucide **la seule pièce qui porte les faits**
   (nom du titulaire, adresse, horaires) : c'est l'objet de confiance du premier écran.
2. **La branche 2 offerte au client est un piège.** Sur fond papier, le cercle devient *moins* visible,
   pas plus : **21 % d'encre visible** contre 55 % aujourd'hui. Les deux extrémités du dégradé sont à
   l'opacité 0 et le bleu clair disparaît sur le blanc. Retirer la photo ne rendrait pas son cercle au
   client ; ça lui donnerait une page plus vide avec un cercle plus pâle.

## 3 · Les approches écartées, et pourquoi

- **B — agrandir le cercle à 760 px sans le déplacer.** Meilleur chiffre brut (77 % géométrique) mais il
  traverse le titre (10–19 %), le chapeau (15–21 %) et les boutons (12–14 %). C'est exactement le défaut
  corrigé le même soir.
- **H — donner au cercle son propre fond (disque papier derrière la carte).** 75 % d'encre, mais le
  disque lave la légende sous la carte et fabrique un projecteur. Rejeté à l'œil.
- **C + D ensemble.** Deux changements dans le même geste, et le verre n'achète que 0 à 4 points d'encre
  quand D est en place. Si le client veut une carte plus légère un jour, c'est une décision séparée.

## 4 · Décision

**D. Le cercle ne bouge pas de pièce, il bouge de place : il s'ancre sur le coin haut-droit de la carte
d'identité, qui reste opaque.**

Réglages mesurés, par palier :

| Largeur | Diamètre | Ancrage | Encre visible | Collisions |
|---|---|---|---|---|
| < 1024 (mobile, tablette) | 470 px (inchangé) | centré sur la carte (inchangé) | 33 % | 0 |
| 1024 – 1199 | 620 px | `right:-34% ; top:-16%` | 48 % | 0 |
| ≥ 1200 | 700 px | `right:-34% ; top:-16%` | 67 % (1280) · **79 % (1440 et plus)** | 0 |

## 5 · Ce qui reste au constructeur, et ce que je ne fais pas

- Un seul arbitrage à tenir : **ne pas toucher au dégradé ni à la durée**. Le cercle reste `#sheen`,
  `spin 24 s`, coupé par `prefers-reduced-motion`.
- **Hors périmètre, à ne pas promettre** : la force du trait lui-même. À 33 % d'encre sur téléphone, le
  cercle est encore discret ; le rendre plus présent demanderait d'épaissir le trait ou de relever les
  arrêts d'opacité — donc de **changer le dessin**, ce qui est une décision du client (son croquis a du
  bleu, du vert et du rouge ; le cercle n'a jamais eu de vert).
- **À dire au client** : la branche 2 (« retirer la photo ») ne rendrait pas le cercle plus visible. Le
  chiffre est là pour que la conversation ne s'engage pas sur une fausse promesse.
