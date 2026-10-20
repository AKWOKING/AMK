# DM OPTIC — notes de construction (24/09/2026, nuit)

**Ce que c'est.** L'aperçu construit après la réponse de M. Domche Noumbi : « **Ok Envoyé svp...** »
(15:54). Le message du lot 4 lui proposait « je vous construis votre page, d'abord : vous l'ouvrez sur
votre téléphone, vous décidez après » (15:31). Il a dit oui ; voici la page.

**Fichiers.**
| Rôle | Chemin |
|---|---|
| Gabarit (source unique du texte) | `demos/dmoptic-v1.tpl.html` |
| Constructeur (+ vignette du lien) | `demos/build_dmoptic.py` |
| Aperçu, un seul fichier | `demos/concept-dmoptic-v1.html` (166 Ko) |
| Dossier à déployer | `hosting/previews/dmoptic/` (`index.html` + `og.jpg`) |
| Test de comportement (25 assertions) | `tools/qa/test_dmoptic_page.mjs` (`node tools/qa/test_dmoptic_page.mjs`) |
| Images d'illustration | `demos/img/dmoptic-lunettes.jpg`, `demos/img/dmoptic-mesure.jpg` |

---

## 1 · Le Design Read, les trois directions, et le choix

**Design Read** (dit avant la première ligne, §1) : *a one-page shopfront preview for a Douala optician
that exists off the web, for a patient searching from a phone — precise-and-warm language (an
instrument, not an advertisement), leaning toward « la carte » : the practice's real registration as an
elegant credential card in the first screen.*

**Dials (§2) : VARIANCE 6 · MOTION 4 · DENSITY 5.** Variance 6 = une mise en page asymétrique mais
tenue (texte à gauche, carte à droite en 980 px+, tout en une colonne en dessous) ; motion 4 = une
entrée dans le premier écran + les révélations de section, rien d'autre ; densité 5 = la page porte des
champs et des étiquettes (mono), pas seulement de la prose.

**Les trois directions explorées (§19.3), et pourquoi deux sont tombées :**
- **A · LA CARTE** — le seul actif vérifié du cabinet (son inscription à l'Ordre) devient l'objet du
  premier écran. L'absence (« hier : aucun résultat ») et la présence (« maintenant : la fiche ») se
  répondent dans une bande sombre. **Retenue.**
- **B · L'INSTRUMENT** — catalogue technique à la *teenage engineering* (papier blanc, filets, mono
  partout). **Écartée** : trop près du registre « mesure » du **Cristallin** (papier froid, étiquettes
  mono) ; deux pages opticien qui mesurent la même chose, c'est une reskin (§19.3 point 4).
- **C · L'ENSEIGNE** — bleu de travail + vermillon, typographie d'enseigne peinte. **Écartée** : le
  risque « vieux commerce » est réel pour un cabinet de santé, et King a déjà refusé une imagerie
  d'époque pour Douala (« Douala est beaucoup plus moderne »).

**Références** (URL · pris · rejeté) : `clients/dm-optic/inspiration.md`.
**Le test de l'échange (§23.2)** : si l'on remplace « DM OPTIC » par le nom d'un autre cabinet, la page
ne tient plus — la carte d'identité du premier écran porte **son** n° d'inscription, **son** titulaire,
**son** numéro, et la bande « hier » parle d'un cabinet précis qui n'existait pas sur le web.

---

## 2 · La provenance de chaque valeur (§18.1) — rien d'inventé

| Ce qui est affiché | D'où ça vient |
|---|---|
| Nom « DM OPTIC » / « DM Optique » | nom affiché sur WhatsApp (capture de King, 15:54) + registre ONOC ligne 102 |
| Inscription **021/2016**, arrêté **0382**, titulaire **M. Domche Noumbi** | registre ONOC, annuaire par région, ligne 102 (Littoral) |
| Douala, Littoral | même ligne du registre |
| **656 122 239** (+237) | même ligne ; vérifié à l'écran par King (la porte A) |
| « Son nom apparaît en mars 2023 dans la liste des opticiens de Douala citée par la presse » | *Echos Santé*, article sur l'Ordre national des opticiens du Cameroun |
| « Aucun site, aucune page, aucune fiche » | **contrôle approfondi du 24/09** : `dmoptique.com` et `dmoptic.com` existent mais ne servent **rien**, `dmoptique.cm`/`dmoptic.cm` inexistants, aucun Blogspot / WordPress / YouTube / X / Instagram / Facebook, aucune fiche d'annuaire |
| Adresse · horaires · paiement · assurances · marques · photos | **inconnus** → écrits « **à confirmer** » sur la page, deux fois (section *Pour le cabinet* et bloc contact) |
| Les six actes (examen de la vue, verres, montures, solaires, lentilles, entretien) | liste **type** d'un cabinet d'optique, signalée comme telle sous la bande : « Liste type d'un cabinet d'optique — à valider avec vous » |
| Les deux photographies | **générées**, légendées « **Mise en situation : la photo définitive sera prise dans votre cabinet** » (§25.2 point 3). Aucun visage : on ne fabrique pas le portrait de M. Domche Noumbi |

**Une annonce écartée volontairement** : afribobo, déc. 2019, « DM optometrie », 2 500 F — publiée par
un particulier, non recoupée avec le cabinet. Elle n'apparaît nulle part dans la page (§18.1 : une
valeur sans source n'entre pas dans une page de santé).

---

## 3 · Ce que la page fait, écran par écran

1. **Premier écran** — la phrase (`Inscrit à l'ONOC. Trouvable depuis aujourd'hui.`), **deux actions
   et pas trois** (WhatsApp, appeler), trois faits alignés (Ordre, ville, titulaire), et **la carte
   d'identité** : n° d'inscription, arrêté, titulaire, numéro. C'est la seule chose que nous possédons
   vraiment du cabinet, et elle est mise en page comme une pièce officielle.
2. **Le constat** (bande marine) — « Le registre de l'Ordre vous connaît. Le web, non. »
   Deux panneaux : **hier** (un encadré en pointillé braise, « aucun résultat », les trois questions
   sans réponse) et **maintenant** (la fiche vivante). Vérification datée en bas de bande.
3. **Les actes** — une bande **glissante** (six cartes, défilement horizontal à magnétisme sur
   téléphone, trois colonnes sur ordinateur), numérotées 01→06 en mono. Une image, une seule
   signification : l'objet qu'on vient chercher.
4. **Le titulaire** — un nom, une inscription, une source datée (presse professionnelle) ; en face, la
   photographie de l'instrument qui mesure.
5. **La note au cabinet** — les **six champs manquants**, chacun avec sa pastille « à confirmer », et la
   phrase qui explique pourquoi on n'invente pas : « Une page de santé qui invente une adresse ou un
   horaire coûte un patient, puis la confiance. »
6. **Contact** — deux actions, puis deux **utilitaires** discrets : copier le numéro, **enregistrer la
   fiche contact (.vcf)**. Le pied de page suit la norme §20.2 (4 blocs + bandeau, action = celle du
   premier écran, crédit en texte).

**Mouvement (budget respecté)** : une entrée dans le premier écran (la carte qui se pose, l'anneau qui
se trace en 950 ms) + les révélations au défilement (IntersectionObserver, jamais d'écouteur de
défilement) + deux retours d'état (le bandeau `#say` après WhatsApp/appel, l'annonce « Numéro copié »).
Quatre moments, pas un de plus.

---

## 4 · Les contrôles, et ce qu'ils ont attrapé

| Contrôle | Résultat | Ce qu'il a corrigé |
|---|---|---|
| `audit_html.py` | **0 constat** (237 passages de texte, bureau et mobile) | 13 textes en `#6C7890` à **3,92:1** sur le papier → passés à `#586476` (**5,30:1**) ; le mot-symbole du pied de page restait à l'encre foncée sur le marine |
| `audit_a11y.py --strict` | **0 faute A/AA, 0 avertissement** | 4 anneaux SVG sans `aria-hidden` |
| `audit_hero.py` | **0 faute, 0 avertissement** | la marque de l'en-tête était lue « icône sans nom » → le nom écrit passe **avant** le dessin ; 4 actions dans le premier écran → les deux utilitaires descendent dans le bloc contact |
| `check_inline_js.py` | **rc 0**, 4 blocs compilés | — |
| `audit_images.py` | 0 faute (aveugle aux `data:` — limite connue, les images sont embarquées en base64) | — |
| `node tools/qa/test_dmoptic_page.mjs` | **25/25** | marqueur `scriptAfter` ambigu corrigé (le mot « LE MOUVEMENT » vit aussi dans une règle CSS) ; presse-papier et fiche contact protégés pour un DOM sans `Blob` ni téléchargement |

**Ce qui n'a PAS été fait, et qu'on dit** : aucune capture d'écran, aucun mockup (le bac n'a **pas de
navigateur**). Le premier écran, la mise en page et l'œil restent à King, sur un téléphone — c'est la
règle du portique de déploiement : *« Not verified on a phone = not sent. »*

---

## 5 · À faire avant d'envoyer le lien (dans cet ordre)

1. **Déployer** `hosting/previews/dmoptic/` (**le dossier entier** : `index.html` **et** `og.jpg`) —
   projet Vercel séparé, par exemple `dmoptic`. Sans `og.jpg` à côté, le lien redevient une carte grise.
2. **Recoller l'adresse** : `python3 demos/build_dmoptic.py --url https://<adresse>` puis **redéployer le
   dossier** — la vignette du lien (`og:url`, `og:image`) ne peut pas être devinée (§20.7).
3. **Ouvrir le lien sur un téléphone**, en plein jour : FR par défaut, la bascule EN qui change tout,
   **un vrai WhatsApp pré-rempli** qui s'ouvre, la barre du bas visible, aucun débordement horizontal.
4. **Envoyer d'abord la carte du lien**, puis le texte de `sales/Send-DM-OPTIC-2026-09-24.md` —
   jamais les deux dans un même message.

## 6 · Ce qu'on ne dit pas, et ce qu'on ne fera pas

- **Jamais** d'adresse, d'horaire, de prix, de marque, de photo inventés : les six champs sont marqués
  « à confirmer » **sur la page**, et c'est cet aveu qui déclenche la réponse.
- **Jamais** « il vous manque une page » à un prospect (règle du 24/09) — ici la page existe, elle est à
  lui.
- **Aucune promesse** de classement, de délai, de nombre de patients.
- Les deux images sont des **mises en situation** : dès qu'il envoie ses photos, elles prennent leur
  place (c'est écrit sur la page, sous les deux images).

---

# 7 · v2 — le virage patient, et les dégradés animés (24/09, après la v1)

## 7.1 La phrase de King, et ce qu'elle a déplacé

> *« the demo seems to speak more to the prospect, but it's supposed to speak to the patient »*

King a raison, et la faute était de conception, pas de style : la v1 racontait **au cabinet** sa propre
histoire (« le registre vous connaît, le web non », « voici les six champs qu'il vous
manque »). Un patient qui tombe sur cette page apprend que l'opticien n'avait pas de page — il
n'apprend pas **quoi apporter, ni comment prendre rendez-vous**. La v2 part de la seule question qui
compte : *« puis-je venir, et comment ? »*

**Règle retenue, valable pour tous les cabinets de santé :** la preuve (registre, inscription, presse)
ne disparaît pas, elle **change de rôle** — elle ne vend plus le travail au patron, elle **rassure le
patient** (« un opticien inscrit, un titulaire nommé »). Le texte qui s'adresse au propriétaire ne vit
plus sur la page : il vit dans `clients/dm-optic/a-completer.md`, un document qui part dans la
conversation WhatsApp.

## 7.2 Ce qui a changé sur la page, section par section

| Section | v1 (écartée) | v2 (en ligne après redéploiement) |
|---|---|---|
| Premier écran | la phrase au cabinet + la carte d'identité | **« DM OPTIC, votre opticien à Douala. »** · surtitre porteur du mot-clé (« Opticien à Douala · inscrit à l'ONOC ») · une phrase de service, puis **deux gestes** : écrire sur WhatsApp (message pré-rempli), appeler |
| Les actes | six cartes, une image | six actes **avec « À apporter »** sur chacun (ordonnance, ancienne monture…) — c'est ce qui manquait au patient |
| Le déroulé | absent | **trois étapes** : WhatsApp → la réponse → la visite |
| La preuve | « le registre vous connaît, le web non » | **« Un opticien inscrit, un titulaire nommé »** : n° 021/2016, arrêté 0382, M. Domche Noumbi, *Echos Santé* mars 2023 |
| Les questions | absent | **cinq questions fréquentes** de patient : où · faut-il une ordonnance · une monture cassée · les horaires · le prix — les cinq sont dans le schéma `FAQPage`, **mot pour mot** |
| Contact | deux utilitaires | deux gestes, puis **copier le numéro** et **enregistrer la fiche .vcf** ; barre d'action fixe en bas d'écran sur téléphone |
| Note au cabinet | six champs « à confirmer » **sur la page** | **sortie de la page** → `clients/dm-optic/a-completer.md` (huit points, dont la validation des actes et une phrase de lui) |

**Ce qu'on n'a pas inventé** (inchangé, et c'est le cœur du dossier) : aucune adresse, aucun horaire,
aucun prix, aucune marque, aucune assurance, **aucun avis**. Le prix est traité comme une question de
patient (« combien coûte une paire ») dont la réponse renvoie au cabinet — pas comme un tarif affiché.

## 7.3 Les dégradés animés du premier écran (la demande de King)

Trois couches, **transform uniquement** (aucun `filter`, aucun repaint), toutes coupées par
`prefers-reduced-motion` et jamais allumées sans JavaScript :

| Couche | Ce que c'est | Mouvement |
|---|---|---|
| `.wash` | trois `radial-gradient` (cachet `#1A3F86` 20 % · braise `#E0703A` 12 % · bleu clair `#4E7BD8` 15 %) | `drift` **26 s** ease-in-out alternate — translation + échelle ±3 % |
| `.lensring` | anneau SVG, dégradé linéaire `#7FA6E8 → #2A5CB8 → #E0703A`, deux cercles | `spin` **24 s** linéaire — la rotation d'un verre |
| `.band::before` | le même lavis, sur la bande sombre | `drift` **32 s** |

Budget de mouvement toujours respecté : **un** moment d'entrée (la carte qui se pose, l'anneau qui se
trace en 950 ms), les révélations au défilement (IntersectionObserver, jamais d'écouteur de défilement),
deux retours d'état. Les dégradés sont **du décor** : ils vivent sous le contenu, en `z-index: 0`,
`pointer-events: none`, et ne portent aucune information.

## 7.4 Les contrôles du 24/09 au soir (après réécriture)

| Contrôle | Résultat |
|---|---|
| `audit_html.py` | **0 constat** sur **229 passages de texte** (bureau et mobile) |
| `audit_a11y.py --strict` | **0 faute A/AA, 0 avertissement** |
| `audit_hero.py` | **0 faute, 0 avertissement** |
| `check_inline_js.py` | **rc 0** — 4 blocs `<script>` compilés |
| `audit_images.py` | 0 faute (0 image comptée : les deux photos sont embarquées en base64 — limite connue de l'outil) |
| `audit_aeo.py` | ✓ schéma complet (`Optician`, `PostalAddress`, `ContactPoint`, `Person`, `PropertyValue`, `FAQPage` + 5 `Question`) · `noindex` voulu sur une page de travail |
| `node tools/qa/test_dmoptic_page.mjs` | **38/38** — dont : chaque adresse WhatsApp statique = le texte français **encodé exactement comme le fera le JavaScript**, les 5 questions du schéma **mot pour mot** celles de la page, le bloc `prefers-reduced-motion` qui arrête **aussi** `.wash` et `.lensring`, et la page qui reste lisible si le script de mouvement plante |

**Toujours pas fait, et qu'on dit** : aucune capture d'écran, aucun mockup — le bac n'a **pas de
navigateur**. Le premier écran, les dégradés en vrai, l'œil : c'est King, sur un téléphone. Règle du
portique : *« Not verified on a phone = not sent. »*

## 7.5 Après le redéploiement

`hosting/previews/dmoptic/` (**le dossier entier**, `index.html` + `og.jpg`) → `--url
https://dmoptic.vercel.app` déjà recollée dans le fichier construit (`og:url`, `og:image`) → puis le
message de `sales/Send-DM-OPTIC-2026-09-24.md` §1. **Un seul redéploiement.**

---

# 8 · v2.1 — « listez ces services, montrez ses montures » (24/09, soir)

## 8.1 Le retour de King, et ce qu'il déplace

> *« on parlait aussi de listé ces services et montré ses montures et lunettes au patient »*
> *« je ne pense pas que tout les détails de lui dans l'ordre sois nécessaire »*
> *« look for optic clinics and shop on the Web to see how they showcase and write on their sites »*

Trois conséquences, dans cet ordre :

1. une **section vitrine** — « Les montures et les lunettes » : trois familles, une photo, un conseil
   chacune, et une seule action (« Demander si c'est en boutique ») ;
2. le **registre sort du texte visible** : n° 021/2016, arrêté 0382, « Littoral, ligne 102 », *Echos
   Santé* — supprimés. Ce qui reste : « Opticien inscrit à l'ONOC » (une phrase, dans la carte et le pied de page), et le nom du titulaire dans la carte. **La
   donnée structurée garde l'identifiant 021/2016** : la machine peut vérifier l'entité, le patient n'a
   pas à lire un arrêté ministériel ;
3. **recherche avant écriture** (règle du dépôt) : trois recherches, deux sites d'opticiens lus en
   entier — `queenoptique.com` (Montréal) et `optiquebj.com` (Rennes) —, motifs consignés dans
   `inspiration.md` § « Second passage ». Ce qu'on a copié : la liste de services explicite, la vitrine
   par familles, l'essayage comme argument, les trois conseils (visage · appui · usage), le prix jamais
   affiché. Ce qu'on n'a **pas** copié : les marques (on n'en a aucune), les avis (on n'en a aucun), la
   promesse de délai (« en 1 heure »), le rendez-vous en ligne (le cabinet n'a pas d'agenda).

## 8.2 Ce que la page porte de neuf

| | |
|---|---|
| Premier écran | les trois faits deviennent **Où (Douala) · Sur WhatsApp (656 122 239) · Opticien inscrit à l'ONOC** ; la carte ne garde que **deux lignes** (L'opticien, Où) et son pied dit « Adresse exacte et horaires : demandez-les sur WhatsApp ou au téléphone » |
| Services | « **Nos services**, et ce qu'il faut apporter » (six services, chacun avec « À apporter ») |
| Vitrine (neuve) | « **Les montures et les lunettes** » : lunettes de vue · lunettes de soleil · enfants — une photo, un conseil d'essayage et un « À demander » par famille ; trois conseils du choix ; **une seule action** (« avez-vous cette monture en boutique : ») ; **aucune marque, aucun prix** |
| Comment ça se passe | la photo de l'instrument de mesure y entre — la bande sombre s'ouvre sur une image |
| Questions | **six** (ajout : « Peut-on essayer plusieurs montures avant de choisir ? »), les six dans le schéma `FAQPage`, mot pour mot |
| Légendes | les cinq photos disent « **Photo d'illustration** » — plus de « mise en situation : la photo définitive sera prise dans votre cabinet », qui parlait au patron |
| Poids | **328 Ko** — cinq images embarquées, 900 px de large, qualité 50 (contre 170 Ko en v1, deux images) |

## 8.3 Les contrôles de la v2.1

| Contrôle | Résultat |
|---|---|
| `audit_html.py` | **0 constat** — 258 passages de texte (desktop et mobile) |
| `audit_a11y.py --strict` | **0 faute A/AA, 0 avertissement** |
| `audit_hero.py` | **0 faute, 0 avertissement** |
| `check_inline_js.py` | **rc 0** — 4 blocs compilés |
| `audit_aeo.py` | ✓ `Optician` + `FAQPage` · **6 questions** atomiques · `noindex` voulu |
| `test_dmoptic_page.mjs` | **45/45** — trois assertions neuves : la vitrine montre trois familles (photo + titre) ; elle ne nomme **aucune marque** et n'affiche **aucun prix** ; les numéros du registre ne sont plus dans le **texte visible** alors que l'identifiant reste dans les **données structurées** |

**Assumé** : les photos de la vitrine sont des illustrations — le cabinet n'a pas encore envoyé les
siennes. La demande est dans `clients/dm-optic/a-completer.md` (six à huit photos par famille) et le
message qui part avec le lien la porte. Le jour où elles arrivent, elles remplacent les trois.

**Toujours pas fait, et qu'on dit** : aucune capture d'écran, aucun mockup (le bac n'a pas de
navigateur). Le premier écran, les dégradés en vrai, la vitrine : c'est King, sur un téléphone.

---

# 9 · v2.2 — le cabinet donne ses propres faits (25/09 ; appliqué le 27/09)

## 9.1 La source, mot pour mot

Le 25/09 à 16:19, M. Domche Noumbi a écrit — c'est la première fois de la campagne qu'un prospect
**corrige** une page au lieu de la commenter, et la première fois que ce cabinet donne des faits :

> Quelques Modifications :
> - DM OPTIQUE SARL
> - DOUALA/ BONABERI/ NDOBO MAYOR- IMMEUBLE WEST HOTEL
> - HORAIRES : Ouverture 8h00 / Fermeture 17h30 · CONSULTATION : 8H30-13H30

Trois minutes plus tôt (16:08) il avait écrit « **Ce que vous faites est bien** » : la page est
**approuvée par son destinataire**. Ces deux messages sont la matière de la v2.2 — rien d'autre n'a
été écrit dessus.

## 9.2 Ce que « appliquer » veut dire ici — onze endroits, 44 écritures

Le nom, l'adresse et les horaires ne sont pas un paragraphe : ce sont des **valeurs** répétées dans
toute la page, et une seule oubliée se voit tout de suite (une vignette qui dit « DM OPTIC », un
`.vcf` qui enregistre l'ancien nom, une réponse Google qui dit « à confirmer »).

| # | Où | Avant | Après |
|---|---|---|---|
| 1 | `<title>` (onglet) | Opticien à Douala — DM OPTIC… | … — **DM OPTIQUE SARL**… |
| 2 | `og:title` (vignette du lien) | DM OPTIC — opticien… | **DM OPTIQUE SARL**… |
| 3 | `og:image:alt` | DM OPTIC — cabinet… | **DM OPTIQUE SARL** — cabinet… |
| 4-5 | mot-symbole (en-tête **et** pied) | `DM OPTIC` | `DM OPTIQUE` + **SARL** en léger |
| 6-7 | titre du premier écran (FR/EN) | DM OPTIC, votre opticien… | **DM OPTIQUE SARL**, votre opticien… |
| 8 | carte d'identité | DM OPTIC | **DM OPTIQUE SARL** |
| 9 | pied de page | © 2026 DM OPTIC | © 2026 **DM OPTIQUE SARL** |
| 10-21 | **les six messages WhatsApp** ×2 langues | « Bonjour DM OPTIC, » | « Bonjour **DM OPTIQUE SARL**, » |
| 22-23 | `<dd>` du « Où » : premier écran + carte | Douala, Littoral | **Bonabéri, Ndobo Mayor** / **Ndobo Mayor — immeuble West Hotel, Bonabéri, Douala** |
| 24 | pied de la carte d'identité | « Adresse exacte et horaires : demandez-les… » | **« Ouverture 8h00 – 17h30 · Consultation 8h30 – 13h30 »** |
| 25-26 | note sous le bouton (FR/EN) | Le cabinet est à Douala, Littoral | Le cabinet est à **Bonabéri, Ndobo Mayor** (Douala) |
| 27-28 | bloc contact : Adresse, Horaires | `à confirmer` / `à confirmer` | l'adresse et les horaires **écrits** |
| 29-30 | pied de page : adresse, horaires | Douala, Littoral — Cameroun / « à demander au cabinet » | l'adresse + les horaires **écrits** |
| 31-32 | réponses FAQ « Où ? » et « horaires ? » (visibles) | « la localisation vous est envoyée… » / « dès que le cabinet nous les confirme » | l'adresse / **8h00–17h30, consultation 8h30–13h30** |
| 33-37 | **fiche contact `.vcf`** | nom, organisme, adresse = Douala | **DM OPTIQUE SARL**, adresse Ndobo Mayor, + les deux annonces de la région vive |
| 38-41 | **données structurées** : `name`, `PostalAddress`, les **deux réponses** du `FAQPage` | Douala seul / réponses d'attente | nom, `streetAddress` + `addressRegion`, réponses **identiques aux visibles** |
| 42 | bandeau d'aperçu | « …adresse, horaires et photos à valider… » | « **vos corrections du 25/09 sont en place** ; les photos de vos montures remplaceront les illustrations » |
| 43 | le bouton du bloc contact | « …je voudrais passer vous voir. **Quels sont vos horaires ?** » | « …je voudrais passer vous voir. » |
| 44 | la vignette `og.jpg` | nom 104 pt, anneau en haut à droite | nom **90 pt**, anneau reculé (**mesuré** avant, pas deviné) |

## 9.3 La question qu'on ne pose plus, et celle qu'on pose

Le bouton du bloc contact **demandait** « Quels sont vos horaires ? » — c'était juste tant que la
page ne les connaissait pas. Elle les connaît : la question a été **retirée** (garder un bouton qui
demande une information déjà écrite trois écrans plus haut, c'est apprendre au patient que la page ne
sait pas ce qu'elle affiche). La question fréquente « Quels sont les horaires d'ouverture ? » **garde
sa place** dans le schéma `FAQPage` — elle y **répond**.

**Ce qui manque encore, et qu'on ne devinera pas** : **les jours**. Il a donné des heures, pas des
jours (« 8h00 / 17h30 »). La page n'affirme donc **aucun** jour d'ouverture — ni dans le texte, ni
dans le schéma (le test refuse `openingHours`, et c'est bien). La demande est dans le message du
28/09 : *« lundi au samedi ? fermé le dimanche ? »*.

## 9.4 Les contrôles de la v2.2

| Contrôle | Résultat |
|---|---|
| `audit_html.py` | **0 constat** — 258 passages de texte (desktop 258 / mobile 258) |
| `audit_a11y.py --strict` | **0 faute A/AA, 0 avertissement** |
| `audit_images.py` | 0 faute, 0 avertissement sur 5 images |
| `check_inline_js.py` | **rc 0** — 4 blocs compilés |
| `audit_hero.py` | **0 faute, 0 avertissement** |
| `audit_aeo.py` | ✓ `Optician` + `FAQPage` · 6 questions · `noindex` voulu |
| `test_dmoptic_page.mjs` | **45/45** (le test a été mis à jour : les six messages portent le nouveau nom, et le bouton du bloc contact ne demande plus les horaires) |
| équilibre bilingue | **118 `.fr-only` / 118 `.en-only`** — chaque ajout existe dans les deux langues |
| recherche du nom | « DM OPTIC » sans le UE : **0** dans tout le fichier (y compris les scripts) |
| `og:url` / `og:image` | recollés sur `https://dmoptic-2.vercel.app/` **après** le rebuild (`--url`), puis relus dans le HTML écrit |

**Assumé** : les photos de la vitrine restent des **illustrations**. C'est la seule chose qui empêche
la page d'être entièrement la sienne, et elle est demandée en clair (5 à 10 modèles, depuis son
téléphone ou son catalogue WhatsApp Business).

**Toujours pas fait, et qu'on dit** : aucune capture d'écran (pas de navigateur dans le bac). Le
premier écran, la vignette et la bascule FR/EN se regardent sur un téléphone, en plein jour — et
**avant** que le lien reparte.

## 9.5 Le dépôt du moteur

`demos/build_dmoptic.py` a reçu la v2.2 : le docstring porte le message du client mot pour mot (la
provenance), et la vignette a été **remesurée** — « DM OPTIQUE SARL » à 90 pt fait **937 px** (mesuré
avec ImageMagick avant d'écrire), l'anneau a reculé à `circle 1058,452` pour ne plus frôler le « L ».
Un défaut vu à l'œil sur la première sortie, corrigé, revérifié à l'œil.

## v2.3 — 08/10/2026 (réponse du cabinet 14:58 + ruling credentials)

- **Heures** (formulation rapportée par King ; verbatim client non transmis) : « Examen de vue : 8h30–13h00 ·
  Autres besoins : 8h30–17h30 » remplacent « Ouverture 8h00–17h30 · Consultation 8h30–13h30 » (25/09) aux
  six endroits de la page, FAQ visible et FAQPage comprises. **Jours : toujours inconnus.** Reconstruit par
  `python3 demos/build_dmoptic.py --url https://dmoptic-2.vercel.app/` (historique ; **depuis le 08/10 : `--url https://dm-optique-sarl.vercel.app/`**, seule adresse valable — King) ; gate §1b : audit_html 0, a11y OK,
  images 0 faute ; test page : toutes les assertions passent.
- **Ancien état en ligne :** v2.1 (« DM OPTIC », adresse/horaires « à confirmer », « depuis 2016 ») — le
  redéploiement du 09/10 publie d'un coup v2.2 (SARL, adresse, étage/porte) + v2.3.
- **Pas de prix sur la page** (déjà le cas) ; spec : `site/SPEC-PAGES-v1.md` révisé.
- ⚠️ **Heures périmées ailleurs (NON modifiées, hors périmètre) :** `content/month1/carousels.md` l.41, 50, 72, 82 ·
  `content/month1/w2/ugc-script.md` l.63, 97, 99, 114 · **slides C1 baked (PNG) si elles portent les heures** ·
  `a-completer.md` · carte signature PDF/PNG (périmée, acceptable tant que non réutilisée). À aligner avant
  tout usage.

---

## 11/10 · Logo hero — décisions (rulings King, après le fix masque+anneau)

- **Taille hero +35 % :** mobile 210→**285px**, desktop 300→**405px** (template `demos/dmoptic-v1.tpl.html`
  + preview `hosting/previews/dmoptic/index.html`). Garde right-anchored, `pointer-events:none`,
  `aria-hidden`. **Non déployé** — King revoit sur téléphone puis déploie.
- **SVG auto-tracé REJETÉ pour le hero.** `logo/dm-optique-logo.svg` est un tracé automatique (vtracer)
  du raster — « PAS le fichier vectoriel d'origine : dégradés et ombres approchés par aplats ». Il
  rendrait le dégradé en bandes plates. On garde le **PNG masqué en cercle + anneau dégradé**.
  Le **PDF d'origine** (`website/LOGO DM.pdf`, pièce jointe King 11/10) reste la **source autorisée**
  si un vrai vectoriel propre est un jour nécessaire (V2) — pas extrait maintenant.
- **Logo en filigrane derrière le contenu du hero — PARKED (pas maintenant).** Client médical : le
  hero doit rassurer et clarifier, pas exprimer la marque ; un filigrane concurrencerait la lisibilité
  du H1. À ré-étudier **après encaissement de l'acompte**, en V2.
- **SUIVI (accepté, non urgent) :** appliquer le **même masque circulaire** aux assets dérivés
  (`og.jpg`, favicon) dans `build_dmoptic.py` au prochain passage de build — à poser avec le travail
  de catalogue **post-acompte**.

---

## EN ATTENTE (ruling King, 11/10 — post-acompte, avec le travail de catalogue) : masque circulaire sur `og.jpg`
Le `og.jpg` déployé a été généré **avant** le correctif du masque : la carte de prévisualisation
WhatsApp/lien montre encore le logo carré « collé », pas le cercle propre. À refaire dans
`build_dmoptic.py` (même masque circulaire que `.herologo`). **Pas urgent ce soir** — le fil DM Optique
est clos ; importe pour (1) tout envoi futur de l'URL DM Optique (référence/portfolio) et (2) la page
opticiens (quand construite), dont l'og:image portera chaque message de vague avec lien.
(Note : le fichier nommé par le ruling, `site/BUILD-NOTES.md`, n'existe pas ; consigné ici, le vrai
build-notes du dépôt.)

---

## 20/10/2026 · Plan d'architecture v2 écrit — choix de direction en attente (King)

- Recherche catalogue faite (Agent Reach tentée, bloquée egress → natif déclaré) : Baymard,
  Google (facettes), Warby Parker et Ace & Tate lus en direct → `inspiration.md` (3e passage).
- Plan complet : `site/SPEC-PAGES-v1.md` **§10** — architecture 9 URLs types (hub, 3 catégories,
  fiches, examen, cabinet, contact), `frames.json` v2 tagué **visible seulement** (forme/couleur),
  filtres à compteurs en fragments (SEO), ~40 montures curées, 3 directions de composition dans
  l'identité actuelle. Recommandation : **D2 « La Vitrine réelle » + page examen de D3**.
- État : **aucun build v2 commencé**. Prochain geste = choix King (D1/D2/D3), puis données →
  générateurs → portiques → Vercel → déploiement Cloudflare par King.

---

## 20/10/2026 · Build v2 D3 construit au dépôt — portiques verts, non déployé

- **Direction retenue par King : D3 « Le Parcours ».** Accueil : nouvelle section `#parcours`
  (« par où commencer ? ») après le hero, vitrine `#montures` remontée avant les services ; nav en-tête/pied
  vers `/examen-de-vue/`, `/montures/`, `/le-cabinet/`, `/contact/`. Textes/couleurs/logo inchangés.
- **Générateur** `demos/build_dmoptic_montures.py` réécrit en multi-pages : hub catalogue, 3 catégories,
  40 fiches avec galeries d'angles + similaires, `/examen-de-vue/`, `/le-cabinet/`, `/contact/`, sitemap 48 URL.
  Correctifs QA intégrés : bloc similaires en section sœur (pas imbriquée), `src` d'images relatifs à la
  profondeur (résolution navigateur + `audit_images.py`), polices/logo de tête réécrits en absolu pour pages nichées.
- **Données** : 40 montures (F24 · E10 · H6), 65 WebP (~1,9 Mo), 16 fiches multi-angles ; taggage visible
  seulement ; F11 corrigée « Hexagonale argentée ». Photos cabinet publiées au dépôt : intérieur + enseigne
  uniquement (aucun visage ; scènes d'examen en attente d'accord).
- **Contrôles** : `python3 demos/build_dmoptic.py --production` + `python3 demos/build_dmoptic_montures.py` ;
  portiques accueil verts ; boucle 48 pages html/a11y/images/js verte ; `node tools/qa/test_dmoptic_page.mjs` vert
  (suite 2b : 40 montures, 3 catégories, fiche F01). Aperçu HTTP local : routes clés en 200.
- **État** : construit et zippé au dépôt (`dmopticsarl.zip`, racine) pour validation King. **Non déployé** sur
  Cloudflare ; pas de nouvel envoi Vercel ce tour. Bloquants de fin : validation client des 40 + correspondance
  codes ↔ stock, accord visages pour les scènes d'examen, Search Console/fiche Google après déploiement.

---

## 20/10/2026 · v2 déployée sur Vercel test + règle « déployer à chaque changement »

- **Ruling King (20/10)** : déployer la nouvelle version sur Vercel, et le faire **à chaque changement du site**.
  Règle permanente inscrite : `PRE-FLIGHT.md` §1f③ (+ ligne §0d).
- **Déploiement v2 fait** : commit `3d3ab9a` → déploiement `dpl_HUqFyrLTsqZGTxEwUS8tQpQTb5Hd`, **READY / PROMOTED**
  (~70 s), alias `dm-optique-sarl.vercel.app` (+ alias branche). Vérifié en ligne : accueil (section
  `#parcours`), `/montures/femmes/` (24 cartes + filtres), `/examen-de-vue/` (4 étapes).
- **Portée** : Vercel reste le banc d'essai de King. La production client sur Cloudflare (upload du zip par King,
  après validation) n'a pas changé ; `dmoptiquesarl.com` toujours non vérifié en direct.

---

## 20/10/2026 · Revue taste-skill de la v2 (demande King) — mesurée, aucun code du site touché

**Chaîne** : skill `design-taste-frontend` (§1f④), cas « existing page » : `lint.mjs` sur les 8 types de
pages construites + **`inspect.mjs` en vrai navigateur (1440/768/390)** — débloqué ce jour :
Chromium de la chaîne vidéo (`bash tools/video/install.sh`, @sparticuz) via
`CHROME_PATH=/tmp/amk-video/chrome-wrapper.sh`. Captures relues à l'œil (accueil, femmes, fiche F01,
examen). Sorties dans `.taste-skill/before-*` (ignorées par git). Limites dites : l'inspecteur local
sert la racine du dépôt → polices/logo des sous-pages (chemins absolus `/fonts/…`, `/dm-logo.webp`)
en 404 dans SES captures (rendu de repli) ; sur Vercel (racine = `dmoptic/`) ils se chargent.
L'inspection de l'URL live est impossible d'ici (egress Chromium fermé). Les mesures de mise en
page restent valables.

**Comptes** — lint : accueil 43 FAIL/12 WARN · examen 42/21 · hub, 3 catégories, fiche, cabinet,
contact 38/21-22 (l'essentiel vient du CSS de coquille partagé, répété sur les 48 pages).
inspect : accueil 10 FAIL/6 WARN · femmes 6/8 · fiche 5/8 · examen 8/5.

**Critique (format du skill) — accueil**
```
ROUND 1 (before)
Seen in one second: le nom en grand, le bouton WhatsApp vert, le logo en anneau.
Idea (one sentence): la carte d'inscription à l'ONOC devient la preuve du hero ; le parcours
  « par où commencer » route par intention.
Live thing: le message WhatsApp pré-écrit par intention (+ filtres du catalogue).
Layout words: hero=split · parcours=index 3 col · montures=trio cartes+bande · services=grille 6 ·
  bande=étapes+photo · faq=accordéon · contact=faits.
Scores bruts (juré): design 7 · usability 8 · creativity 7 · content 7 → 7,3.
Caps applied: FAIL inspect présents → overall ≤ 6,0 (règle du skill). Plafond identitaire, pas un
  jugement client : les dispositifs plafonnants (mono, filets, numérotation, dégradé, ombre) sont
  l'identité approuvée (voir classe B).
```
Femme/fiche/examen (bruts) : femmes 6,5/6/5,5/7 · fiche 6/6/5,5/6,5 · examen 6/7,5/5,5/7 — tous
plafonnés 6,0 par la même règle. **Top 3 problèmes** : ① marges mobiles des sous-pages (A1) ;
② l'accueil montre encore des photos d'illustration alors que le catalogue réel existe (A8) ;
③ les deux pages qui convertissent enterrent l'action (filtres mobiles A3, CTA de fiche A4).

### Classe A — défauts objectifs (correctifs recherchés ; aucun ne touche l'identité)

| # | Défaut mesuré | Correctif (fichier) | Source |
|---|---|---|---|
| A1 | **Texte à 0 px du bord sur les 47 sous-pages** (<1120 px) : `.v2-main section{padding:44px 0}` (`demos/build_dmoptic_montures.py:72`, spécificité 0-1-1) écrase le `padding:0 var(--gut)` de `.wrap` (0-1-0). Desktop masqué par `margin:auto`. | `padding:44px var(--gut)` (ou longhands verticaux) dans le bloc CSS v2 du générateur ; preuve = `edge-text` 0 à la ré-inspection. | inspect `edge-text`/`off-centre` |
| A2 | **Hero mobile : le logo-anneau couvre le kicker** (« INSCRIT À L'ONOC » partiellement masqué, capture 390). | Sous 780 px : réduire/descendre `.herologo` ou réserver la place (padding droit du bloc titre). `demos/dmoptic-v1.tpl.html`. | critique passe 13 (collisions) |
| A3 | **Catalogue mobile : aucun produit au premier écran** — 17 pills dépliées + barre collante ; compteur rogné à droite. Sur desktop, le compte « 24 montures » est dit 3 fois. | Mobile : filtres repliés derrière un déclencheur + bouton « Afficher X montures » (déjà présent) ; desktop : retirer le bouton « Afficher » redondant, garder compteurs+pills. Générateur (bloc filtres). | Baymard mobile filtering (déjà consigné 20/10) |
| A4 | **Fiche desktop : CTA WhatsApp sous le pli**, image pleine largeur ~840 px de haut, rangée de faits avec **822 px de vide au milieu** (`empty-middle`). | ≥980 px : deux colonnes (galerie ~55 % · faits + CTA à droite, CTA visible sans défiler) ; mobile : CTA après la première image. Générateur (fiche). | Baymard PDP 2026 (CTA au-dessus du pli) |
| A5 | Texte courant mesuré **15,2 px** (`--fs-sm:.95rem` porte les paragraphes de cartes), `--fs-label:.72rem` ≈ 11,5 px → 6 blocs < 13 px (accueil). Le corps (`--fs-base` 17 px) est sain. | `--fs-sm:1rem`, `--fs-label:.8125rem` ; re-portiques §1b + ré-inspection. Gabarit + générateur (jetons partagés). | Consensus 16 px (Google Knowledge ; revues accessibilité) — d'autant plus pour un public qui vient pour ses yeux |
| A6 | **Sous-pages immobiles** : 0 élément en mouvement (`still-page`) — le générateur n'embarque pas la couche d'apparition de l'accueil. | Porter le système `.rv` de l'accueil (transform/opacity, `prefers-reduced-motion`) dans la coquille du générateur. | skill étape 9 |
| A7 | **Page examen : 0 image** (`few-pictures`). | Y poser `cabinet-interieur.webp` (réelle, sans personne, déjà au dépôt). Les scènes d'examen avec visages restent exclues sans accord explicite. | Ace & Tate eye-test (processus en photos) ; verrou « réel » |
| A8 | **Accueil : 3 légendes « Photo(s) d'illustration »** + images stock (`dmoptic-*.webp` : cartes montures, bande, monture d'essai) alors que 65 WebP réelles existent — contredit « le site ne montre que du vrai » (brief §"réel") et la loi imagerie du skill. | Cartes « Lunettes de vue » et « Enfants » → vraies montures du catalogue ; bande sombre → photo réelle du cabinet. **« Lunettes de soleil » : aucune monture solaire réelle au catalogue** (`frames.json` vérifié) → garder l'illustration légendée pour cette seule carte, ou carte sans photo, ou lot photo solaires à demander au client. Choix King. | NN/g « Photos as Web Content » (le décoratif est ignoré, le produit réel est scruté) |

### Classe B — règles du skill contre identité figée (ruling King requis ; options recherchées)

| Dispositif | Mesure | Options (de « on garde » à « on aligne ») |
|---|---|---|
| **Mono (IBM Plex Mono)** | FAIL lint 3 · 21 % du texte accueil, **34 % fiche** | ① `--allow mono` motivé (identité « registre de l'Ordre » approuvée) · ② **mono réservée aux données** (téléphone, horaires, codes F01…), libellés en Plex Sans — fait aussi tomber font-count (3→2 visages perçus) et la plupart des micro-labels · ③ suppression (texte + `tabular-nums`, déjà actif sur `body`). |
| **Micro-labels capitales espacées + kicker hero** | 16 (accueil) · eyebrow FAIL | Le seul dispositif que les données du skill condamnent aussi (16 % des tops vs 57 % des faibles). ① garder · ② retirer le seul kicker du hero (l'info « inscrit à l'ONOC » est déjà dite 3 fois au premier écran) · ③ libellés en casse phrase 13 px (rejoint A5). |
| **Numérotation 01–06 / 01–04** | 9 accueil · 4 examen | À scinder : examen + « trois étapes » = **séquences vraies** → balisage `<ol>` (le skill l'admet) ; services 01–06 = ordre arbitraire → décoratifs, retirables sans perte d'info. |
| **Filets 1 px / boîtes contour** | 35 filets mesurés accueil · 24 boîtes femmes | ① garder · ② **garder les rangées réglées là où elles sont le métaphore-registre** (carte, faits) et passer le reste en écarts de ton/espace (FAQ, contours de cartes catalogue : le fond crème de la photo suffit à définir la surface). |
| **Dégradés** | lavis animé du hero + anneau conique du logo | Anneau = traitement du logo client décidé le 11/10 → `--allow gradient` motivé pour lui. Lavis `.wash` : aplati possible (champ plat) sans toucher ni couleur ni texte — au choix. |
| **Ombre de la carte + survol qui soulève** | 1 ombre au repos | La carte est « l'objet » du hero : `--allow shadow` motivé pour elle seule ; le soulèvement au survol est retirable à coût nul. |
| **Fond crème #F6EBE0 du catalogue** | WARN `palette-cream` (fiche, femmes mobile) | Choix King (ton chaud de marque) ; le skill vise crème jaune + terracotta — notre braise #E0703A s'en approche. Changer = retraiter 65 WebP. À garder sauf ruling contraire. |
| **Tirets cadratins** | 23 accueil · 33 femmes | Textes approuvés intouchés ; les chaînes **générées** (`Femme — forme ovale…` ×40 fiches) peuvent passer en virgules/points lors d'une future passe copie validée. |
| **Point focal du hero** | plus grand corps 52 px = 3,6 vw (médiane des tops du skill : 8,4 vw) ; média hero 12 % | Sans changer le texte : monter `--fs-h1` (plafond 3,25 rem → ~4 rem). Et/ou **photo du cabinet au premier écran — c'était le souhait du client le 10/10** (« C'est mieux la photo du cabinet »), différé faute de photos ; `cabinet-interieur.webp` existe maintenant. Retirerait du même coup le logo géant (le nom/logo apparaît 3 fois au premier écran) et le vide du bas de hero (~40 % du pli desktop). **Changement de composition → ruling King.** |

### Classe C — au-delà du lint (critique sur captures)

- **Répétition de composition** : grille de cartes ×3 sur l'accueil (parcours, montures, services) —
  passe 9 « sameness ». Si B évolue, varier une des trois (liste réglée pour les services, par ex.).
- **Bande défilante des services** (mobile) signalée `side-scroll` : intentionnelle (snap + fondu),
  mais lue « coupée » par beaucoup de visiteurs ; alternative = 2 colonnes dès 768 px.
- **10 tailles de police** sur l'accueil (12→52) : resserrer vers ~6 quand on touchera aux jetons (A5).
- **Aucune vidéo** (WARN partout) : aucun clip honnête n'existe ; le verrou « réel » interdit le
  stock. À mettre au brief du prochain lot photo : un plan cabinet de 5 s. Absence défendue d'ici là.
- Fiches multi-angles (16) : images empilées pleine largeur ; un sélecteur d'angles (vignettes)
  raccourcirait la page — à grouper avec A4 si King retient ce lot.

**Recherche du jour** (Agent Reach tentée d'abord, Exa hors-ligne → repli natif déclaré) :
Baymard *Product Page UX 2026* · NN/g *Photos as Web Content* · page Eye Test d'Ace & Tate lue en
direct · consensus corps ≥ 16 px — détail et pris/rejeté : `inspiration.md`, 4ᵉ passage.

**État** : revue + recherche consignées, **aucun fichier du site modifié** (donc pas de redéploiement
Vercel — §1f③ ne se déclenche pas). En attente du ruling King sur le périmètre (A seul / A + B-lite /
alignement large) avant tout correctif.
