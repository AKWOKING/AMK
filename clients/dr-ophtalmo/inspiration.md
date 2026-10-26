# Dr Ophtalmo (médecin itinérant) — inspirations, et ce qui n'a pas pu être fait

**Date du build :** 26/10/2026 · **Aperçu :** `hosting/previews/dr-ophtalmo/`

## Design Read (ligne obligatoire, PRE-FLIGHT §2.5)

> *« Je lis ceci comme : une page professionnelle de médecin pour des patients anxieux qui ne savent pas
> où se rendre, dans une langue premium-calme de soin (bleu de minuit, blanc chaud, un seul teal), avec
> une grande typographie éditoriale à gauche et un portrait à droite — variance 6, mouvement 3,
> densité 4. »*

**Dials :** DESIGN_VARIANCE **6** (asymétrie de grille, pas de cartes égales) · MOTION_INTENSITY **3**
(apparitions sobres uniquement, tout est lisible sans animation) · VISUAL_DENSITY **4** (deux blocs denses
assumés : la fiche professionnelle et le formulaire).

## ⛔ La recherche en ligne n'a pas pu être faite — et je ne l'invente pas

`PRE-FLIGHT.md` §2.3 exige **trois références vivantes minimum** (structure, couleur-typographie,
image-mouvement), prises en ligne et jamais de mémoire, avec pour chacune : URL · ce qu'on prend · ce qu'on
rejette. Dans cet environnement, seuls `github.com`, `registry.npmjs.org` et `pypi.org` sont joignables :
Awwwards, Godly, Land-book, SiteInspire, Mobbin, Lapa Ninja et Dribbble sont **inaccessibles**. La règle
prévoit ce cas : *le dire tout de suite, ne pas fabriquer des références de mémoire.*

**Ce qui a servi à la place, et qui est vérifiable :**

| Référence réelle | Ce qu'on en prend | Ce qu'on rejette |
|---|---|---|
| **Les deux captures WhatsApp** envoyées par King le 26/10 (médecin : « je ne suis pas opticien patron », « je suis ophtalmologue », puis sa semaine : Mbouda lundi-mardi, Bafoussam mercredi-jeudi, Africa Médical vendredi-samedi, rendez-vous à Hôpital Charity) | **Tout le contenu factuel du site** : c'est la seule source des quatre lieux et des jours. Le ton « Docteur » de la conversation rappelle qu'on parle à un médecin, pas à un commerce. | Le ton commercial de la conversation WhatsApp (relances, « 100 % sur-mesure »), qui n'a rien à faire sur une page de soin. |
| **La prescription du brief** (palette, échelle typographique, trois sections, hero à trois lignes, jeton par jeton) | La colonne vertébrale visuelle : elle est assez précise pour tenir sans référence externe. | Rien : c'est une contrainte, pas une inspiration. |
| **`clients/_uniqueness-registry.md`** — lignes DM Optique (marine + crème + mono, « l'aveu avant la promesse »), Le Cristallin (papier froid + vert, « mesure plutôt que séduction »), JEMPO (quatre portes, terracotta) | La **différenciation** : ce build ne reprend ni la carte d'identité DM, ni l'échelle d'acuité du Cristallin, ni les quatre portes de JEMPO. Ni mono, ni terracotta, ni crème. | Le vocabulaire « aveu avant la promesse » des opticiens : ici la promesse n'est pas commerciale, elle est logistique (« où, quel jour »). |

**Différenciation sur cinq axes** (règle §2.6, minimum quatre) : ① mise en page — éditorial 12 colonnes
avec portrait en 4:4.7 et rail de lieux numérotés 01–04, aucune grille de cartes égales ; ② palette —
bleu de minuit + blanc chaud + **un seul** teal qui n'agit que sur l'action et l'état ; ③ typographie —
Newsreader 300 (serif éditorial) en display + Inter Tight en texte, aucun mono, contrairement aux trois
builds opticiens ; ④ imagerie — trois photographies générées, recadrage éditorial, légende honnête sous
chacune ; ⑤ ton — « voici où je consulte, et ce que je ne peux pas encore confirmer », pas de vente.

## Ce qu'il faudrait pour finir la règle d'inspiration

Trois URL, collées par King (ou un accord pour travailler sans) : une page de santé éditoriale, un site de
praticien indépendant, et une référence de mouvement sobre. Elles serviraient au **prochain** passage, pas
à celui-ci : le build actuel tient sur la prescription du brief, et le refaire sur trois références
tardives coûterait plus qu'il ne rapporterait.
