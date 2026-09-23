# UNI-LABO — notes de construction

**Client :** UNI-LABO, laboratoire d'analyses de biologie médicale — Carrefour Etoo, Bonamoussadi (Makepe
Bloc L), Douala · Rue 5N441 · BP 2592 · 07h–19h (sam. 13h) · WhatsApp 696 13 98 19.
**Fichiers (depuis la refonte du 24/09, 00 h 30) :** `demos/concept-unilabo-v2.html` (canonique, **généré**)
→ `hosting/previews/unilabo/index.html` (+ `og.jpg`, + `img/` : cinq photos et leurs variantes légères) →
**racine du projet Vercel `uni-labo.vercel.app`**.
**État :** page **réécrite de zéro** le 24/09 au petit matin (audit `AUDIT-2026-09-23.md` → **§9**), après le
verdict de King sur la version précédente. Rendez-vous de clôture **vendredi 25/09 à 13 h**, à leur
laboratoire. Prix posé : 150 000 FCFA (acompte 75 000).

**La page ne s'écrit plus à la main — elle se génère.** Trois pièces, et c'est la commande qui compte :

| pièce | rôle |
|---|---|
| `demos/_unilabo_v2_content.py` | **tout le texte**, FR et EN, dans l'ordre de la page. C'est ici qu'on corrige une phrase. |
| `demos/_unilabo_v2_js_main.js` · `_js_form.js` | les **deux blocs de JavaScript**, extraits mot pour mot de la version précédente (contrat inchangé) |
| `demos/_unilabo_v2_js_links.js` | le seul bloc **écrit** pour la refonte : les liens WhatsApp statiques qui prennent la langue du visiteur |
| `demos/build_unilabo_v2.py` | le gabarit et le CSS, mobile d'abord → écrit `demos/concept-unilabo-v2.html` |

```
python3 demos/build_unilabo_v2.py       # écrit la page
python3 hosting/build_previews.py       # écrit la copie hébergée (noindex)
node    tools/qa/test_unilabo_page.mjs  # 38 assertions
```
Toute image ajoutée doit avoir sa variante `-sm.jpg` **et être copiée dans `hosting/previews/unilabo/img/`** —
la copie hébergée porte les fichiers, pas seulement le HTML.

## 1 · La lecture

Un laboratoire ne vend pas des analyses, il vend **la certitude que le prélèvement sera utilisable**.
Tout se joue **avant** l'arrivée : une analyse mal préparée, c'est un déplacement perdu et une piqûre pour
rien. Leur page en ligne le sait déjà (cinq panneaux de préparation) mais le dit **en paragraphes** ; nous
le disons **avec l'objet** : la fiche de prélèvement. Le visiteur est un patient pressé, souvent envoyé par
un médecin, parfois à jeun depuis le matin, qui veut trois choses — suis-je au bon endroit, que dois-je
faire avant, comment je prends rendez-vous. La page répond dans cet ordre.

## 2 · Les molettes (§2)

| VARIANCE | MOTION | DENSITY |
|---|---|---|
| **6** — la fiche est un objet qu'aucun autre site de labo ne porte ; la frise passe en bandeau à quatre colonnes | **3** — un seul mouvement signé (l'appui à 140 ms) et l'état d'ouverture qui se calcule ; aucune entrée animée, rien qui cache du contenu | **7** — beaucoup de matière (préparation, familles, retrait, FAQ), mais portée par des filets et des listes, jamais par six cartes égales |

## 3 · La différence (§19, registre)

| Axe | UNI-LABO | Le voisin le plus proche |
|---|---|---|
| Objet dominant | **la fiche de prélèvement**, en trois états | Afrique Labo : console de tarifs ; Cristallin : échelle d'acuité |
| Palette | papier froid `#F4F5F7` + **un seul violet `#5B21B6`** (+ vert WhatsApp pour les seules actions d'envoi) | Afrique Labo : cyan poster + navy ; OraCare : crème/or |
| Typographie | **Sora** (display) + **Public Sans** (texte) | Afrique Labo : Space Grotesk ; Univers : Bricolage Grotesque |
| Rythme | frise à quatre colonnes sous le hero, puis bandeaux photo + fiches | Afrique Labo : sections numérotées ; Cristallin : lignes décroissantes |
| Signature | **la fiche vivante du formulaire** qui se remplit, et la ligne « Préparation » déduite de leurs propres textes | aucune ailleurs |
| Ton | « voici ce qu'il faut faire avant de venir », tutoiement de guichet → vouvoiement | Afrique Labo : réponses de guichet |

## 4 · Les règles appliquées, et où

- **§15.bis** : quatre photos générées, relues, légendées « Mise en situation… » ; fichiers séparés (§15.6).
  **La préparation a été regénérée le 23/09 sur correction de King** (« no one lives in that type of
  house ») : la première version montrait une maison de village, la version retenue un intérieur de ville
  (carrelage, cuisine à gaz, réfrigérateur, ventilateur sur pied). Le décor doit être celui du patient, pas
  celui qu'on imagine pour lui.
- **§13** : `prefers-reduced-motion`, focus visible sur tout le focusable, cibles 44 px, contraste AA
  (mesuré : encre/papier 16,7 · blanc/violet 8,98 · blanc/vert WhatsApp 5,43).
- **§3.4** : trois étiquettes en casse de phrase au total, aucune numérotée, aucun point d'état décoratif
  (le point de la barre du haut est **calculé** à l'heure de Douala).
- **§20.8** : chaque phrase existe en trois endroits (`data-fr`, `data-en`, le nœud visible) — les
  remplissages du formulaire sont écrits dans les deux langues dans le JavaScript, pas dans le HTML.
- **§21/09** : « un bouton n'existe que s'il a une URL dans le HTML » — l'envoi du formulaire est un `<a
  href>` réel, que le JavaScript enrichit ; incomplet, il garde le message générique.
- **Honesteté** : aucun prix, aucun avis, aucun `aggregateRating`, aucun `sameAs`, aucune photo présentée
  comme la leur, aucune donnée stockée (le message part du téléphone du patient).

## 5 · Ce qui reste, et ce qui n'est pas à nous

1. **Redéploiement** du dossier `hosting/previews/unilabo/` (King — Vercel, glisser-déposer).
2. **Photos définitives** : le jour de la livraison, trois clichés au laboratoire (accueil, paillasse,
   salle de prélèvement) — la page porte déjà les emplacements et les légendes.
3. **`noindex,nofollow`** à retirer le jour où c'est LEUR site sur LEUR domaine.
4. Couleurs, si le client veut les siennes : la famille violette vient de l'aperçu du 18/09, elle n'est pas
   un choix de leur charte.

## 9 · La refonte (24/09, 00 h 30) — pourquoi tout réécrire plutôt que corriger

La passe précédente (§8) avait corrigé vingt détails sur la même page. King a regardé la page et a dit :
*« the pictures seem to have spoiled everything »*. Les deux constats se tiennent : **nos corrections
portaient sur des éléments, la sienne portait sur la composition.** Huit photographies dans une page, quatre
en bandeaux, du texte posé sur certaines : sur un téléphone, cela fait trois écrans de photo et un écran de
contenu — l'inverse de ce que vend un laboratoire, qui vend de la certitude en trois phrases.

La refonte repart donc de la structure, pas des détails :

1. **Le hero n'a plus de photographie.** Un fond encre et un titre : le laboratoire n'a pas de photo qui
   mérite le premier écran, et une image générée à cet endroit serait un mensonge par omission.
2. **Les photographies portent chacune UNE signification** — la famille d'analyses qu'elles illustrent, ou
   la préparation à la maison. Cinq au total, jamais derrière du texte, toujours légendées « mise en
   situation », et suivies de la phrase qui dit la vérité : *la photo définitive sera prise dans votre labo*.
3. **Mobile d'abord, pour de vrai** : la feuille de style écrit la colonne unique, et ce sont les médias
   `min-width` qui ajoutent les colonnes — jamais l'inverse. Une seule échelle typographique, qui **monte**
   sur petit écran (`clamp`), comme l'exige §24.1.
4. **Ce qui portait la page avant reste** : la fiche de prélèvement (trois états : exemple, consigne, fiche
   vivante), l'état d'ouverture calculé, le refus expliqué, la bande de retour, le bilingue.
5. **Le contenu du client est repris mot pour mot**, et le JavaScript aussi : la refonte change la coquille,
   jamais le contrat. `tools/qa/extract_unilabo_js.py` prouve que les deux blocs sont identiques à ceux du
   commit `2d2ffe4`.

Ce que la refonte a coûté, et ce qu'elle a rapporté : la page passe de 94 509 à **84 053 octets**, les images
d'un téléphone de 193 à **167 Ko** (et de 676 à 394 Ko sur ordinateur, parce que les fichiers ont été
recadrés à 1024×640 — le ratio exact que la page déclare, plus de recadrage surprise), et les assertions
passent de 23 à **32** (la nouvelle suite 0 interdit qu'une refonte suive le JavaScript d'un cran de trop).