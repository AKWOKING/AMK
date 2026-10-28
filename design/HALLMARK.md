# Hallmark — la compétence de design installée, et ce qu'elle a dit du site DM OPTIQUE

**Ce que c'est.** `nutlope/hallmark` (MIT, **v2.0.0**, 182 fichiers) : une compétence de design pour
agents, qui pose un **plancher de 16 règles** avant de laisser la main au goût, et qui livre un linter,
`sloplint.mjs`, capable de dire lesquelles sont enfreintes. Sa promesse tient en une phrase : « des
interfaces qui ont l'air faites, pas générées ».

**Où elle est installée, et comment la remettre.** L'installation est globale à la machine, donc elle
ne survit pas à un nouveau bac à sable. La commande exacte, celle qui a servi le 28/10 :

```bash
npx -y skills add nutlope/hallmark -g --agent '*' -y    # → ~/.agents/skills/hallmark
npx -y skills list -g                                   # vérifier : hallmark, source nutlope/hallmark
```

Sans `--agent '*' -y`, la commande ouvre un menu interactif et **s'arrête sans rien installer** quand
elle n'a pas de terminal (c'est arrivé au premier essai).

**Pourquoi ce n'est pas vendorié.** `design/vendor/` garde des bibliothèques qu'on relit et qu'on cite.
Celle-ci s'installe et se met à jour toute seule (`npx skills update`), et 5,6 de ses 7,1 Mo sont des
aperçus de thèmes en JPEG. Recopier une version figée dans le dépôt, c'est se condamner à diverger en
silence. On garde donc **la commande, la version et le verdict**, pas la copie.

---

## 1 · Le plancher, en clair

Seize règles, non négociables, dont sept comptent pour nous tous les jours : chaque couleur et chaque
police passe par un jeton déclaré ; jamais `transition: all` ; jamais un mot en italique dans un titre
romain ; `overflow-x: clip` sur `html` et `body` ; `minmax(0, 1fr)` sur une piste de grille qui porte des
images ; `:focus-visible` sur tout ce qui se clique ; et un repli `prefers-reduced-motion` pour chaque
animation. Le reste interdit l'eyebrow, les étiquettes en capitales espacées, les métadonnées liées par
des points médians, le dégradé violet, la carte dans la carte, l'emoji en icône.

**Ce que ça vaut par rapport à nos documents.** `AMK-DESIGN-SKILLS.md` §3 (l'anti-slop) et
`design/CRAFT-FLOOR.md` disent déjà la plupart de ces règles, avec nos seuils. Hallmark apporte deux
choses qu'on n'avait pas : **un linter** qui les vérifie mécaniquement, et la règle 44b (le titre du
premier écran, sa phrase et son action visibles à 1280 x 800 sans défiler).

---

## 2 · Le verbe employé : `audit`, pas `redesign`

La compétence dit elle-même : *« Never use it on an existing design unless the user names Hallmark »*,
et pour un design existant elle prévoit deux verbes, `audit` et `redesign`. **King a nommé Hallmark**,
donc une passe était autorisée. Le choix s'est porté sur `audit`, pour une raison qui n'est pas de
prudence mais de propriété : le design de DM OPTIQUE SARL est **approuvé, mesuré et en ligne**, sa
palette a des chiffres (papier 55,67 %, encre 17,32 %, blanc 9,36 %), et une refonte n'est pas une
décision que prend un outil. Un `redesign` reste possible, sur demande, et ce sera une autre livraison.

```bash
node ~/.agents/skills/hallmark/scripts/sloplint.mjs hosting/previews/dmoptic/index.html
```

## 3 · Ce que le linter a trouvé, et ce qu'on en a fait

| Règle | Ce qu'elle reproche | Nombre | Décision |
|---|---|---|---|
| **34** | pas de `overflow-x: clip` sur `html` et `body` | 1 | **corrigé** |
| **50** | piste de grille en `1.35fr` qui porte des images | 1 | **corrigé** |
| 48 | couleurs écrites en dur hors du bloc de jetons | 38 | **écarté** : ombres, filets et blancs. Les sortir en jetons, c'est refaire le système de couleurs du client, pas corriger une faute |
| 7a | blanc pur `#fff` | 8 | **écarté** : `#FFFFFF` est dans la palette mesurée (9,36 % de la page), c'est la couleur des cartes, pas un oubli |
| 67 | étiquettes en capitales espacées (`.kicker`, `.chip`, `.h-city`) | 8 | **écarté** : c'est la voix du design, la ville en capitales espacées est la signature du premier écran |
| 63 | métadonnées liées par des points médians | 9 | **écarté** : chaînes approuvées par le client (horaires, adresse, moyens de paiement) |
| 19 | un tiret cadratin dans le texte | 1 | **écarté** : il est dans le `<title>`, et les 22 titres du site suivent la même forme. À trancher pour tout le site ou pas du tout |
| 24b | espacements hors échelle de 4 px | 184 REFLEX (les deux pages) | **écarté** : le site est sur un rythme de 2 px, décidé et tenu |
| 20 | pas de tampon Hallmark en tête du CSS | 1 | **sans objet** : le tampon est la trace d'une page construite par Hallmark, pas d'un site qui existait avant |

**Avant / après**, même page, même machine :

| Page | Avant | Après |
|---|---|---|
| Accueil | 67 FAIL · 74 REFLEX · 25 WARN | **65 FAIL** · 74 REFLEX · 25 WARN |
| `/questions/` | 67 FAIL · 110 REFLEX · 11 WARN | **66 FAIL** · 110 REFLEX · 11 WARN |

Deux fautes en moins, **zéro pixel changé**. Les 65 restantes sont des écarts de convention avec un
design qui a ses propres règles, et elles sont écrites plus haut, une par une.

## 4 · Les deux corrections, et pourquoi celles-là

**Règle 34, dans le gabarit** (`demos/dmoptic-v1.tpl.html`) :

```css
html{… ;overflow-x:clip}
body{margin:0;overflow-x:clip;…}
```

`clip` et non `hidden`. `hidden` fait de `<html>` un conteneur de défilement : le `position:sticky`
cesse de fonctionner et la barre fixe se met à décrocher. Le cercle décoratif du premier écran sort du
cadre **par construction** : c'est lui qui poussait la page de côté sur un téléphone.

**Règle 50, même fichier** : `.grid3` et `.fgrid` passent de `1.35fr 1fr 1fr` à
`minmax(0,1.35fr) minmax(0,1fr) minmax(0,1fr)`. Sans le `minmax`, une colonne de grille refuse de
descendre sous la largeur de son contenu : une image large élargit la colonne, et la grille déborde au
lieu de rétrécir.

## 5 · Ce que le linter ne sait pas faire

- **Le rendu réel** : l'étage `--render` demande `puppeteer-core`, absent du bac. On a donc lu le CSS et
  le HTML, pas la page peinte. L'œil reste `tools/qa/shot.py`, qui a tourné vert sur l'accueil après la
  correction.
- **Le goût**, et c'est écrit dans la compétence : elle juge des règles, pas une hiérarchie.
- **Le contenu** : il compte les mots (2 138 sur l'accueil, contre 450 demandés) mais ne sait pas qu'une
  page d'opticien à Douala doit dire ses horaires quatre fois pour être trouvée.

## 6 · Rejouer la mesure

```bash
node ~/.agents/skills/hallmark/scripts/sloplint.mjs hosting/previews/dmoptic/index.html
# attendu : 65 FAIL, 74 REFLEX, 25 WARN — et aucune ligne FAIL 34 ou 50
```

Si le compte remonte, la première chose à lire est la liste des `FAIL 34` et `FAIL 50` : ce sont les
deux seules qui ont été corrigées, donc les deux seules dont le retour est une régression.
