# Univers Optique — notes de build (21 Sep 2026, 22:40)

## Fichier
- `demos/build_univers_optique.py` — le gabarit. **Zéro phrase dans le générateur.**
- `demos/univers_optique_content.py` → **`demos/univers_optique_content.json`** — toute la copie FR|EN,
  plus le dictionnaire `SOURCES` (les six adresses lues, datées). Le `.py` est la source, le `.json` est
  généré par `python3 demos/univers_optique_content.py` : on ne touche jamais au JSON à la main.
- sortie : `demos/concept-univers-optique-v1.html` (**927 Ko**, 3 visuels base64) + copie
  `hosting/previews/univers/index.html` (slug `univers` ajouté à `hosting/build_previews.py`).
- visuels : `demos/img/univers-optique-{shop,bench,customer}.jpg` (241 / 196 / 194 Ko après
  `convert -colorspace sRGB -strip -interlace Plane -quality 74-80`).

## Design Read (§1) et dials (§2)
> « Lecture : un dossier de reprise pour les habitants de Bépanda qui cherchent un opticien ET pour les
> RH et mutuelles qui achètent des verres de sécurité — dans la langue administrative du document
> (fiche, constat, à trancher), penché vers un dossier d'affaires plutôt qu'une vitrine. »

Mode détecté (§12) : **greenfield sur archive** — le site antérieur est mort, il n'y a ni charte ni IA à
préserver ; tout le contenu vient de ce que le client a lui-même publié. Zéro question posée à King : le
screenshot du fil WhatsApp répondait à l'essentiel (loi §1 : une question maximum, et seulement si elle
bloque).

VARIANCE **7** · MOTION **4** · DENSITY **5** (un dossier doit montrer qu'il a lu ; la densité est
ici un argument, pas un accident). Preset maison de base « School/clinic conversion » (6/4/4), poussé
d'un cran sur variance et densité parce que la promesse du message était « on a tout lu ».

## Direction : « LE DOSSIER DE REPRISE »
La page s'ouvre sur sa **couverture** : une fiche d'établissement (huit champs, chacun rattaché à sa
source) et un tampon rouge « à reprendre ». Le visiteur ne découvre pas un opticien, il **ouvre un
dossier le concernant**. Ensuite : six constatations en vis-à-vis — *ce que j'ai lu* (avec l'URL et la
date) en regard de *la reprise* (ce qu'on écrit à la place) — puis le **registre des dix actes** (liste
à filets, pas trois cartes), les créneaux, sa vraie note de 3,3, les rendus, et les six questions qu'il
doit trancher lui-même.

**Différenciation sur 6 axes (minimum 4 exigé par PRE-FLIGHT §2.6) :**
| Axe | Univers Optique | Ce que ça écarte au registre |
|---|---|---|
| Archétype | **dossier administratif / fiche d'établissement + tampon** | Le Cristallin = planche d'acuité ; L'Opticien = cabine d'essayage ; JEMPO = front-desk ; Afrique Labo = console d'analyses |
| Ouverture | la **couverture d'un document** (colonne de champs + tampon incliné), pas un hero vitrine | tous les autres builds, qui ouvrent sur headline + CTA centrés ou latéraux |
| Palette | papier chaud `#F2EDE3` / encre `#17140F` / bleu-petrole `#14344A` / **une seule encre rouge brique `#8F3821`** | Le Cristallin vert-sapin `#0D5A41`, La Béthanie teal-médical, Skye blues éditoriaux, YAKS lime, SAHISCOL prune, Sasse navy, OraCare crème |
| Typographie | **Bricolage Grotesque** (display) / **Public Sans** (texte) / **JetBrains Mono** (champs, dates, plus code) | Cristallin Archivo + Instrument Sans + Space Mono ; aucun build n'avait Bricolage |
| Structure de preuve | **vis-à-vis « ce que j'ai lu » ↔ « la reprise »**, avec URL + date sous chaque constatation | comparatif 8 lignes du Cristallin (qui comparait un site vivant) ; ici on compare **ses sources entre elles** |
| Angle | **reprendre la main sur ce qui existe déjà** (« ce n'est pas que vous êtes absent : votre seule page vivante est celle d'un autre ») | « moderniser ce qui vit » (Cristallin), « être trouvé » (generic L'Opticien) |

**§3.1 respecté, et vérifié :** pas de grille de réticule décorative, pas de ligne de version, pas de
compteur live, pas de bandeau météo/locale ; gris **chauds uniquement** (une seule famille) ; accents sous
80 % de saturation (assertion dans le builder) ; aucun blanc ni noir purs.

## Choix de contenu, et pourquoi
- **La note de 3,3 est affichée, pas cachée.** Un aperçu qui gomme le chiffre que tout le monde voit ne
  rend pas service au client, il le flatte. Elle est encadrée de ce qui la fait bouger (répondre aux six
  avis, un mot au comptoir, le chemin pour en laisser d'autres) — sans promettre de remontée chiffrée.
- **Aucun `aggregateRating`, aucun `sameAs`.** Baliser 6 avis à 3,3 = une étoile pâle en SERP ; lier la
  page Facebook de 508 likes = s'attribuer le compte d'un autre. La page **dit** ces absences (§13
  « honesty ») au lieu de les masquer.
- **Les six questions ouvertes sont une section publique**, pas une note interne : le fixe à deux versions,
  le « 15 % » retiré, l'ordre des trois lignes, le nom du titulaire, l'unique e-mail, l'accès Google.
  Une divergence entre deux supports du client s'interroge, ne se corrige pas.
- **Créneaux = WhatsApp pré-rempli**, aucune prise de rendez-vous technique promise. Un seul message de
  départ par intention (`row` / `ask` / `slot` / `generic`), la même étiquette d'action partout.
- **SEO local (playbook AMK, règles 1, 2, 4)** : le titre porte `Univers Optique Bépanda — opticien à
  Douala` ; un seul `<h1>` ; deux `<h2>` nomment Bépanda / Douala / optique / prothèses ; le NAP de la page
  est mot pour mot celui de la fiche Google (horaires, plus code, repère) — la règle des correspondances
  exactes, et le client n'a pas encore de site pour la casser.

## Contrôles passés
- `python3 tools/qa/audit_html.py demos/concept-univers-optique-v1.html` → **`ok … 0 findings`,
  `TOTAL confirmed findings: 0`** (457 runs de texte, desktop et mobile).
- même audit sur la copie `hosting/previews/univers/index.html` → **0 findings** ; `diff` demo/preview =
  **0 ligne** ; `:4173/univers/` → **200**.
- assertions du générateur (elles échouent bruyamment, elles ne sont pas décoratives) : poids 927 Ko ≤ 1100 Ko
  · 840 Ko de visuels, ≤ 260 Ko chacun · **167 paires FR|EN, comptes égaux, aucune vide** · badge de rendu
  3× en FR et 3× en EN · 1 eyebrow pour 8 sections (plafond 3) · 3 `<img>` avec width/height/lazy/alt ·
  0 ancre morte sur 13 ids · **21 liens WhatsApp → 699252874, sans un seul espace dans l'URL** · aucun href
  vers le domaine mort · CTA identique au hero, au rail mobile et au pied de page · aucun prix, aucun
  témoignage, aucune étoile inventée · NAP complet · une seule H1 · JSON-LD `Optician` parseable avec
  `PostalAddress`, geo, `OpeningHoursSpecification`, **sans aggregateRating ni sameAs** · typographie
  anglaise sans tiret cadratin ni accent (167 chaînes vérifiées) · zéro emoji décoratif.
- **Contrôle de la collision de classes** (nouvelle assertion, née de deux accidents) : croise les règles
  CSS *non encadrées* qui peignent un fond avec les balises portant cette classe. **Muté une fois pour
  vérifier qu'il mord** : en redonnant à un `<div>` la classe du pied de page, il sort
  `✗ … {'pagefoot': ['div','footer']}` et le build s'arrête. Un point de relecture sans machine derrière
  est une opinion.

## Ce que ce build a cassé en route (à ne pas refaire)
1. **Trois chevrons en trop dans la copie.** En réécrivant un bloc `photos` d'un trait, j'ai fermé le dictionnaire un cran trop tôt (` }` au lieu de ` },`) : Python déclarait l'erreur **six lignes plus loin**, sur `"photos": {`. Trois réparations successives ont chacune ajouté un chevron ou une virgule avant que je relise le fichier lui-même. **Leçon : après une réécriture de bloc, on `ast.parse` le fichier et on répare la ligne que l'interpréteur montre, pas celle que je crois voir.**
2. **Collision `.foot`** : la note de fin du dossier et le pied de page portaient la même classe ;
   l'auditeur a calculé le fond sombre du pied sous un paragraphe gris clair (2,07:1). Renommé
   `.pagefoot` / `.cnote`. Deuxième collision du même genre en une soirée (`.cmp` chez Le Cristallin).
3. **Le champ `data-msg=""` du dimanche fermé** a failli être « corrigé » par un faux message : un créneau
   fermé n'ouvre aucune conversation. L'assertion a été rendue précise (`href/src/alt/aria-label` vides =
   interdit ; `data-msg=""` = exactement 1, celui du dimanche).
4. **Un `émoji ⚠️`** dans un paragraphe → retiré à la source, puis verrouillé par une assertion.
5. **Le « 15 % de réduction » est apparu dans la copie du constat** ; s'il avait été repris comme une
   offre, la page aurait publié une promotion que personne n'a confirmée. La borne d'assertion
   (`1 ≤ compte ≤ 4`) existe pour que ce chiffre ne puisse rester que comme question.

## Reste à faire, et c'est court
- **Envoyer le fichier** (jamais un lien deviné) : feuille `sales/Send-UNIVERS-OPTIQUE-2026-09-22-Soir.md`,
  promise « d'ici demain » par King à 18:08 → due avant 09:00 mardi 22/09. Si WhatsApp refuse la pièce
  jointe de 927 Ko, la version de repli est la copie sobre de 58 Ko, déjà prévue au Cristallin — **pas**
  un lien Vercel (rien n'est déployé).
- Faire trancher les six questions par le propriétaire ; sans le fixe et l'e-mail uniques, la page ne
  sort pas en ligne.
- Récupérer l'accès à la fiche Google AVANT la mise en ligne (c'est écrit dans la page, section questions).
- Remplacer les trois rendus par ses photos.
---

# V1-bis — 21/09 · 23:55 · « try again » → repasse qualité sur le FICHIER, pas sur l'auditeur

Roi : « *try again* ». Plutôt que de recommencer le concept au jugé, j'ai relu **le fichier généré**
(ce que l'œil ne peut pas voir sans navigateur, `playwright` absent du bac) avec trois contrôles
aveugles : balisage équilibré, classes utilisées ↔ règles CSS, enfants ↔ colonnes des grilles.

## Deux défauts réels, trouvés et corrigés

1. **Le pied de page avait 5 blocs pour 4 colonnes.** Le CTA, cinquième enfant d'une grille déclarée
   `1.3fr 1fr 1fr 1fr`, **tombait seul sur une deuxième ligne, large d'une colonne** — un bloc d'action
   décalé tout en bas de la dernière écran. §20 dit que le pied de page est une surface de conversion,
   pas un dépotoir : le CTA est **rentré dans la colonne de marque** (4 blocs = 4 colonnes).
2. **Aucun CTA dans l'en-tête.** La règle `.cta.small{display:none}` que j'avais écrite était
   **orpheline** : elle ne ciblait rien, parce que je n'avais jamais posé le bouton dans le `<header>`.
   Combiné au fait que le rail mobile est `display:none` sur desktop, **un visiteur d'ordinateur n'avait
   plus aucun moyen de réserver entre le hero et le pied de page** — huit écrans sans porte de sortie.
   Corrigé : CTA d'en-tête visible > 960px (le rail reprend la main en dessous), avec **le même texte**
   que le hero (l'assertion 7 est passée de ≥3 à ≥4 occurrences). Et `@media (max-width:1120px)` retire
   la ligne de statut de la marque pour que marque + onglets + CTA + bascule FR|EN tiennent sans
   débordement entre 961 et 1120px.

## Trois filets mécaniques ajoutés (les mêmes défauts ne peuvent plus repasser inaperçus)

| # | Ce qu'il vérifie | Preuve qu'il mord |
|---|---|---|
| 14a | **aucune règle CSS orpheline** (toute classe stylée existe dans le DOM ; `is-on`/`in`/`shut` exclues, posées par le JS) | mutation `.orphantest` ajoutée → `✗ … ['orphantest']`, `rc=1` |
| 14b | **enfants directs du pied de page = colonnes déclarées** (le fichier est parsé, pas compté à l'œil) | cinquième `<div>` réinjecté → `✗ 4 colonnes déclarées, 5 blocs dans le DOM`, `rc=1` |
| 14c | **un chemin WhatsApp visible subsiste hors hero et hors rail** sur desktop | vérifie la règle ET la présence de `class="cta small"` |

**Ce que ça dit de notre porte de sortie habituelle :** `audit_html.py` est **excellent sur les
contrastes** et **aveugle à la géométrie** — ses 459 runs de texte sont passés « 0 finding » avec un
pied de page cassé et une page sans CTA sur desktop. Un fichier peut être conforme et moche. D'où la
règle : **après l'auditeur, on repasse trois contrôles structurels sur le fichier généré** (équilibre
des balises · classes orphelines · enfants ↔ colonnes), et on écrit ces contrôles dans le générateur.

**État après correction :** 950 Ko · 459 runs de texte · **`audit_html.py` 0 finding** sur la démo, sur
la version sobre (84 Ko, 437 runs) et sur `hosting/previews/univers/index.html` · `diff` démo ↔ aperçu =
**0 ligne** · `:4173/univers/` et `:4173/cristallin/` = **200**. Le fichier de Le Cristallin n'a pas bougé (484 runs, 0 finding).

**Reste à vérifier à l'œil, quand un navigateur sera disponible dans le bac** (pas de `playwright` ici,
je ne le prétends pas) : la densité du registre des dix actes sous 700px et la ligne de tampon sur la
fiche d'établissement entre 600 et 700px.

---

## V1-ter — 21/09 23:59 · **le roi refuse les images : « ça ne représente pas une clinique moderne »**

**Verdict tel que reçu :** « *je n'aime pas les images generer, ca ne represente pas une clinique moderne* ».
Ce n'est pas un goût à discuter, c'est un **défaut de cadrage de ma part** : j'avais demandé des rendus
« documentaires, réalistes, éclairage du jour, quartier de Bépanda » et le modèle m'a obéi — en montrant la
devanture fatiguée d'un commerce du coin. Or la règle du roi est **comparative** : « *our demo has to look
BETTER than his actual website so that he can compare* ». Un rendu qui montre un local usé **fait perdre la
démo avant même qu'on l'ouvre** : le client n'a rien à envier, il se dit « ils montrent mon magasin en pire ».

**Ce que le brief dit maintenant (à réutiliser pour tout commerce) :** intérieur de pratique **indépendante
mais contemporaine** — chêne clair + menuiserie bleu-pétrole mat, **présentoirs rétroéclairés**, long comptoir
vitré, **un réfracteur et une tailluse moderne**, plantes, sol stratifié/terrazzo, lumière équatoriale vive,
personnel en chemise repassée ou uniforme propre. **Négatifs explicites, écrits dans le prompt :** pas de
peinture qui pèle, pas d'encombrement, pas de néon, pas de halo bleu/violet « IA », pas de verre dépoli
décoratif, pas de surimpression de texte. Le réalisme douala est gardé **par le dehors** : rue visible derrière
la vitrine, palmier, bodaboda, façade en face — pas par la dégradation de l'intérieur.

**Deuxième défaut trouvé en relisant mes propres rendus (à retenir avant de câbler quoi que ce soit) :** le
premier lot générait **du lettrage inventé** — « VISION CLAIRE OPTIQUE » peint sur un mur, « OPTICAL SERVICES
DOUALA » brodé sur une blouse. Sur la maquette d'un client réel, un nom inventé dans l'image est (a) une
**information fausse**, (b) potentiellement le **nom d'un concurrent**, que nous n'écrivons nulle part publiquement.
Les deux images ont été **redemandées avec « absolutely NO text, NO lettering, NO logo, NO signage »** et
relues une à une avant câblage. Le troisième rendu (examen de vue) gardait un **optotype** : conservé, parce
qu'un panneau d'échelle est un outil du métier, pas une marque. Chez Le Cristallin, la vitre portait du texte
miroité sans sens → régénérée aussi.

**Troisième point, automatique :** une **légende doit décrire son image**. « *La devanture, en journée … avec
l'enseigne lisible depuis la chaussée* » ne collait plus à un rendu d'intérieur → renommé « **La salle de vente,
en journée** » chez les deux clients, et la légende assume maintenant ce que l'image montre **et** ce qui sera
remplacé à la livraison (« cette image part, la vôtre arrive, devanture comprise »).

**Contrôle ajouté au générateur** (`demos/build_univers_optique.py`, `IMG_REVIEW`) : le juge reste humain (pas
d'OCR dans le bac) mais **l'obligation est machine** — tout visuel embarqué doit avoir sa **fiche de relecture
renseignée**, qui statue explicitement sur le lettrage ; sinon `rc=1`. Muté une fois (fiche vidée → build
refusé), puis rétabli.

**État après V1-ter :** démo **722 Ko** (633 Ko de visuels, ≤260 Ko chacun : 193 / 128 / 154) · repli sobre
**84 Ko** · `audit_html.py` **0 finding** sur la démo, le repli et l'aperçu · `diff` démo ↔ aperçu **0 ligne** ·
**:4173/univers/** et **:4173/cristallin/** = **200**. Le fichier de Le Cristallin passe de 592 à **605 Ko**
(484 runs, 0 finding, `diff` 0) pour la même raison d'image. Toujours **aucun navigateur** dans le bac : les
densités sous 700px et la ligne de tampon entre 600 et 700px restent **non vérifiées à l'œil**, et le roi doit
valider les visuels **avant** l'envoi.

---

## V2 — 22/09 08:3x · « moche et sans image » : la page ne se peignait pas (deux défauts, dont un chez Le Cristallin)

**Capture du roi, 08:0x :** en-tête peint, corps entièrement blanc, fichier ouvert depuis `Downloads/RES/`.
Verdict reçu comme un goût ; c'était une **panne**. Diagnostic mené sur le fichier généré, sans navigateur
(il n'y en a pas dans le bac, et `playwright` ne s'y installe pas : le contrôle ne pouvait donc pas être
visuel — il est devenu **statique et machine**, ce qui est plus durable).

**Défaut 1 — un cache-contenu hérité du gabarit de la maison.** `design/MOTION.md` §3.2 enseigne
`.rv{opacity:0}` sans porte, et `build_univers_optique.py` l'avait recopié sous le nom `.reveal`, posé sur
**25 blocs dont le hero**, relevé par un `IntersectionObserver` en fin de document. Sans exécution du JS —
coupée, rognée par un envoi, aperçu inerte — la page est blanche. `audit_html.py` ne peut pas le voir : il
mesure des contrastes sur des portées de texte, pas la visibilité.
**Correction :** l'état caché n'existe plus que sous **`html.js`** (classe posée par un `<script>` inline dans
le `<head>`) ; la révélation vit dans **son propre `<script>`** avec un `try/catch` qui appelle `show()` ;
le hero, les titres de section, les registres, les images et la barre collée ne s'animent plus du tout —
budget ramené à **6 blocs sur 19 (31 %)**, sous le plafond de 40 % que pose `design/CRAFT-FLOOR.md` §3.
Cinq contrôles écrits dans le générateur (`première peinture sans JS`, `classe js posée dans le <head>`,
`budget mouvement`, `UN seul moment écrit` — familles animées = `['finding']` —, `prefers-reduced-motion`
annule l'état caché). Muté : une règle `.thead{opacity:0}` non gardée injectée dans le gabarit → `rc=1`
(refusée d'abord par le contrôle de CSS orpheline, ce qui prouve les deux filets).

**Défaut 2 — et c'est le plus grave : la même famille de panne chez LE CRISTALLIN, déjà partie chez le client.**
En cherchant ce qui pouvait faire taire le JS d'Univers, j'ai compilé les deux pages : le `<script>` de
Le Cristallin contient un **SyntaxError** depuis dimanche. Quatre phrases de statut (selecteur d'assurance)
étaient injectées via `json.dumps(...)[1:-1]` — les **guillemets retirés** — donc lues par le moteur comme des
identifiants nus : `Unexpected identifier 'une'`. Une faute dans un bloc annule **tout** ce qui suit dans ce
bloc : bascule FR|EN, sélecteur, messages WhatsApp construits à la volée, reveals. **Corrigé à la source**
(`json.dumps` garde ses guillemets et son échappement), plus `try{paint()}catch(e){}` autour des peintures,
plus la révélation isolée dans son propre script. Nouvelle porte pour les deux générateurs :
`tools/qa/check_inline_js.py` compile chaque `<script>` embarqué (via `node --check`) **sur la page en mémoire,
avant écriture** — un fichier fautif n'atteint plus le disque ; `rc=3` (bac sans node) est affiché comme
contrôle **non rendu**, jamais comme un succès. Muté : le `[1:-1]` remis en place → `rc=1`, et md5 du fichier
sur disque **inchangé** (rien n'a été écrit).

**Ce que ça change pour l'envoi :** le fichier que King a téléchargé hier soir est périmé des deux côtés — il
faut lui redonner la version d'aujourd'hui, et la feuille d'envoi porte désormais **octets + sha256** pour que
« page vide sous l'en-tête » se lise comme un téléchargement tronqué et non comme un site moche. Univers
**740 056 octets** (sha256 `719f8b60283184b6…`), repli sobre **86 954** (`1ff52ae6be71dc4d…`), Le Cristallin
**620 492** (`625ce76a78f9b341…`).

**Reste non vérifié, et cela reste écrit :** aucun navigateur dans le bac → pas de capture 1280×800 ni
390×844, pas de console lue en conditions réelles, densités sous 700 px non vues à l'œil. Ce qui est vérifié à
la place : les deux pages compilent (20 blocs `<script>`, 0 faute), 0 finding de contraste sur les cinq
fichiers, `diff` démo ↔ aperçu = 0 ligne, `:4173/univers/` et `:4173/cristallin/` = 200, et — le point du
jour — **le contenu ne dépend plus de JavaScript pour être peint**.


---

## 22/09/2026 · V2 — « take inspiration from all the attachments, read the design files once more, then
## redo the site » (message de King, 22/09 au matin, quatre captures à l'appui)

**Ce qui a été refusé, et pourquoi.** La v1 était juste sur le fond (faits sourcés, six questions, NAP
exact) et fausse sur le registre : un DOSSIER dense à filets, ouvert sur une carte d'état, sans photo.
Les captures renvoyées disaient autre chose : une fiche de gabarit « Grande Photo · Propre · Moderne »
et trois écrans d'un site de santé américain (Function) — bandeau rouille, photo pleine largeur, titre
serif avec un mot en italique, trois étapes 01/02/03 à cartes teintées, tableau comparatif à colonne
surlignée. Le fichier `inspi.txt` annoncé n'était PAS sur le disque dans ce bac (seules les quatre
images ont été lues) — consigné ici pour que l'absence soit un fait, pas un oubli.

**La loi a été relue avant de toucher au code** (§2 dials, §3.1/§3.2 bans, §10 images, §11/§11b, §13
contrôles, §15 visuels, §20 footer), et deux sections de `design/` ont été réintégrées au lieu de rester
au niveau racine : `CRAFT-FLOOR.md` §3 (la pilule) et §11 (pas de tableau de dix lignes).

**Direction retenue (Design Read §1, écrit dans l'en-tête du générateur)** : cabinet photographique chaud
et éditorial, VARIANCE 6 · MOTION 4 · DENSITÉ 3 — l'air vient de la photo, pas du vide.

**Overrides de loi, assumés et nommés (§4.4 : une référence est une contrainte, pas une permission)** :
1. `crème + terracotta` — interdit comme RÉFLEXE, gardé comme DEMANDE : c'est la palette exacte des
   captures. Consigné au registre de rotation, ligne du 22/09.
2. `pilule au-dessus du H1` — interdite en régime serif (§3.4), gardée UNE fois parce que la référence en
   porte une ; elle dit une chose fausable (horaires), pas une humeur.
3. `Newsreader` plutôt qu'un sans-serif : la référence est un titre serif à mot italique. Ni Fraunces ni
   Instrument Serif (§3.2) ; l'italique reste dans la même famille, jamais greffé.
4. Légendes et badges : la référence pose des pastilles SUR la photo ; la maison les met DANS la légende
   (§10.6 + §15). Le badge « rendu de concept » survit ainsi à une capture d'écran.

**Deux pannes trouvées PAR LES CONTRÔLES, pas par l'œil (à retenir) :**
· un `<div>` ouvert devant la pastille du pied de page n'était jamais refermé — 94 ouvrantes, 93
  fermantes. Le contrôle d'appariement des balises l'a dit, la relecture non.
· `audit_html.py` a sorti **8 contrastes cassés** que la table des paires déclarées du générateur laissait
  passer, parce que ces textes-là étaient des couleurs **héritées** (le bouton du pied héritait du gris des
  liens sur fond rouille ; le paragraphe du bandeau portait un crème tiède à 4,07:1). Réparés à la source :
  la rouille passe de `#B4552B` à `#A94C23` (crème dessus : 4,59 → 5,21, une marge au lieu d'un fil) et la
  table de contrastes du générateur a été complétée des paires héritées. Règle à retenir : **contrôler les
  paires réellement peintes, pas les paires déclarées.**

**Faits et copie : inchangés.** 6 constats sourcés, 6 questions à trancher, 8 lignes de face-à-face,
10 actes (en trois paquets — la v2 de midi n'en montrait que 8, le compte a été remis à dix), note 3,3/5
sur 6 avis telle quelle, aucune offre « 15 % » affirmée, aucun prix, aucun témoignage, même NAP
(+237 699 25 28 74 · BP 4680 · rue de Bépanda), mêmes horaires, `noindex,nofollow`.

**Visuels (loi §10.3 + §15, `design/WORKFLOW.md` étape 6)** : quatre rendus d'un seul monde (chêne, crème,
terracotta, lumière de fin de journée, toits de Bépanda par la fenêtre), générés, **compressés à la taille
d'affichage exacte, relus un à un**, puis câblés. Verdicts de relecture stockés dans `IMG_REVIEW` du
générateur et **exigés par la machine** : pas de fiche → pas de build. Aucun lettrage, aucun logo, aucune
broderie ; l'échelle d'optotypes est conservée (outil du métier, pas une marque). Le négatif demandé en
bas à gauche du hero ne s'est PAS matérialisé → le titre est posé sur une **voile calculée** (opacité
minimale 0,84 sur la colonne de texte, contrastes vérifiés au pire cas « image blanche », desktop et
mobile).

**Contrôles : 74 lignes, 0 faute, puis huit mutations refusées** (`rc=1`, md5 du livrable inchangé) —
retrancher l'état caché du JavaScript, voler le hero à la révélation, écrire une couleur en dur, couper
l'anglais, casser le JS, truquer les dimensions, casser une ancre, gonfler le poids. Le fichier de test
de mutation vit hors dépôt (`/home/user/mutation_test_v2.py`) : c'est une preuve d'hier, pas un produit.

**Deux rollbacks du bac en plein tour** (un entre le build et la relève des tailles, un pendant les
tests de mutation) : `.git` re-cloné à `74542ab`, `leads/build/guard.py`, `generators.lock.json` et les
sorties HTML effacés. Récupéré comme la loi le dit : `git fetch` → `reset --mixed FETCH_HEAD` (HEAD revenu
à `951b752`) → `git checkout HEAD -- leads/build/` → `pip install openpyxl` → `guard.py check` rc=0 →
`rebuild.sh` rc=0 (61 fiches) → re-build des pages. Un script idempotent de reprise a été laissé à
`/home/user/recover_v2.py` pour ce cas précis.

**État vérifié après coup** : `concept-univers-optique-v2.html` **734 727 octets** (sha256 `ca52d3c5f6cc
b7ec…`) · repli sobre **81 565 octets** (`6a07f2c4aee18b77…`) · 470 portées de texte audité, **0 constat**
· 4 blocs `<script>` compilés, 0 faute · `diff` démo ↔ `hosting/previews/univers/index.html` = **0
ligne** · `/univers/` pointe sur la v2, `/univers-v1/` garde le dossier pour la comparaison.
**Aucun envoi fait par mes soins.** Aucun navigateur dans ce bac : pas de capture 1280×800 / 390×844 ni
de console lue en réel — c'est écrit, pas caché (§13 : une mesure impossible s'écrit NON VÉRIFIÉE).
## 22/09 · 2ᵉ passe (soir) — « are they dynamique ?? » : le créneau devient calculé, la copie redevient patiente

**Ce que le roi a dit, mot pour mot.** « I love the designs of V2 they're beutiful, but.. » — puis deux
points : « le créneau : are they dynamique??, do they auto update ? I hope they do if not they're useless »
et « the things written on the site shows like we trying to tell what is and what was before the site, but
that's not the objective of the site, the objectif of the site is so clients find, him his services,
increase trust and they book easily ». Le visuel reste ; deux choses cassent.

**Le défaut était réel, pas une impression.** Le module de copie portait `v2.steps.chipsDays` : cinq dates
écrites à la main (« Mar 22 sept » … « Sam 26 sept ») et quatre heures figées (8h30, 10h00, 14h30, 16h00).
Dès le 23, la page affirmait faux ; dès le 27, elle proposait un dimanche. La promesse « les créneaux se
prennent sans JavaScript » était vraie côté liens, fausse côté dates.

**Ce que la machine garantit maintenant.**
- `C["hours"]` (getDay() → minutes d’ouverture et de fermeture, `None` le dimanche) est LA source unique :
  le tableau publié, le `openingHoursSpecification` du JSON-LD et le moteur lisent le même objet. Une heure
  affichée qui contredit la grille fait échouer la construction.
- Le moteur embarqué : `new Date()` nu (un contrôle refuse `new Date(2026,…)` et toute date ISO dans le
  script), cinq journées encore réservables, dimanche jamais proposé, une journée entamée n’est proposée que
  s’il reste deux heures de comptoir, l’heure tombe dans [ouverture, fermeture − 60 min] arrondie à la
  demi-heure, et chaque pastille est UN lien `wa.me` réel avec le message déjà écrit.
- Aucun fichier public ne contient de date absolue : un contrôle balaie le `<main>` publié et refuse
  `jj/mm/aaaa`, « 22 sept », « septembre 22 ». Le contrôle a été muté, et il a mordu.
- Sans script : le socle de créneaux porte `hidden` (il disparaît, il ne reste pas vide) et la ligne de
  repli est vérifiée HORS de tout conteneur caché par un parseur de proximité — un repli avalé par le bloc
  qu’il est censé remplacer n’est plus un repli.
- `univers_optique_content.json` est devenu un artefact périmable : si le module de copie est plus récent,
  le constructeur le régénère avant de le lire. Quatre mutations avaient traversé la construction
  exactement pour cette raison — on ne construit plus sur la copie d’hier.

**La faute découverte en chemin, plus grave que ce qui était demandé.** `wa_url()` fabriquait
`https://wa.me/699252874` : le numéro à neuf chiffres, sans indicatif. L’API WhatsApp exige le format
E.164 — depuis le premier fichier (v1 et v2, donc l’envoi de ce matin), chaque appel à l’action ouvrait
« numéro invalide ». `WA_INTL = "237" + WA` est désormais la seule forme embarquée, le moteur reçoit la
même, et un contrôle refuse toute URL qui ne matche pas `wa.me/237XXXXXXXXX`. Ce qui reste non vérifié ici :
le clic réel depuis un téléphone (aucun navigateur dans ce bac) — à faire une fois, par King, avant l’envoi.

**La copie sépare les deux lecteurs, elle ne touche aucun fait.** Le bloc `C["site"]` (34 clés) porte la
page publique : pilule, titre, promesse, trois repères, les trois pas du client, les dix actes en trois
paquets avec une raison dite AU client, « ce qu’il faut apporter » et la phrase qui manque rarement — nous
ne posons pas de diagnostic médical —, l’adresse et le repère, les prothèses dites aux personnes qui les
cherchent, le rendez-vous, quatre questions de comptoir, le pied de page. Les six constats, la note de 3,3
sur six avis, le comparatif, les six questions à trancher et la liste des photos manquantes ne disparaissent
pas : ils vivent dans une « note au cabinet » (`C["brief"]`) absente du fichier publié, et un contrôle
refuse que le vocabulaire du dossier (3,3 · votre fiche · à trancher · annuaire · domaine · hors ligne ·
à confirmer) passe dans le `<main>` public.

**Preuves.** 92 contrôles, 0 faute · 10/10 mutations refusées (faute nommée, fichiers livrés intacts, md5
comparé) · moteur rejoué dans node sur six instants figés : mardi 14h30 (le jour même est proposé à 15h30),
mardi 17h45 (le jour même saute), samedi 11h00 (le prochain lundi), dimanche 10h00 (« ferme · rouvre lundi
8h00 »), lundi 28 décembre (bascule de mois et d’année : 31 déc. puis 1ᵉʳ janv.), et mardi en anglais —
étiquettes, URL, message et état du comptoir vérifiés à chaque fois · `audit_html` 0 finding sur les trois
fichiers · `check_inline_js` 5 blocs, 0 faute · `diff` démo ↔ aperçu = 0 ligne sur `/univers/`,
`/univers-note/`, `/univers-v1/`.

**Les fichiers.** `demos/univers-optique-site-v2.html` 718 514 o (le site, ce que lit un client) ·
`demos/univers-optique-site-v2-sobre.html` 66 676 o (repli d’envoi, 0 visuel, même copie) ·
`demos/concept-univers-optique-v2.html` 755 254 o (le site + la note au cabinet, document de travail).
