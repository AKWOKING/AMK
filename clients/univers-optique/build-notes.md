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
