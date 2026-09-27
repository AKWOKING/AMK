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

1. **Premier écran** — la phrase (`Inscrit depuis 2016. Trouvable depuis aujourd'hui.`), **deux actions
   et pas trois** (WhatsApp, appeler), trois faits alignés (Ordre, ville, titulaire), et **la carte
   d'identité** : n° d'inscription, arrêté, titulaire, numéro. C'est la seule chose que nous possédons
   vraiment du cabinet, et elle est mise en page comme une pièce officielle.
2. **Le constat** (bande marine) — « Le registre de l'Ordre vous connaît depuis 2016. Le web, non. »
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
histoire (« le registre vous connaît depuis 2016, le web non », « voici les six champs qu'il vous
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
| Premier écran | la phrase au cabinet + la carte d'identité | **« DM OPTIC, votre opticien à Douala. »** · surtitre porteur du mot-clé (« Opticien à Douala · inscrit à l'Ordre depuis 2016 ») · une phrase de service, puis **deux gestes** : écrire sur WhatsApp (message pré-rempli), appeler |
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
   Santé* — supprimés. Ce qui reste : « Opticien inscrit à l'Ordre des opticiens du Cameroun depuis
   2016 » (une phrase, dans la carte et le pied de page), et le nom du titulaire dans la carte. **La
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
| Premier écran | les trois faits deviennent **Où (Douala) · Sur WhatsApp (656 122 239) · Opticien inscrit depuis 2016** ; la carte ne garde que **deux lignes** (L'opticien, Où) et son pied dit « Adresse exacte et horaires : demandez-les sur WhatsApp ou au téléphone » |
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
