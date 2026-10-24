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

---

## 20/10/2026 · Correctifs Classe A appliqués (ruling King) + photo du cabinet au premier écran — redéployé Vercel

- **Ruling King (20/10)** : périmètre = **Classe A uniquement** (les 8 défauts objectifs de la revue
  taste ci-dessus) ; l'identité figée (mono, filets, numérotation, kicker, lavis, ombre de la carte,
  crème) n'est **pas** touchée (Classe B toujours en attente d'un ruling séparé). Choix hero :
  **photo réelle du cabinet au premier écran**, logo géant en anneau retiré, carte d'identité gardée.
  C'est aussi le souhait du client du 10/10 (« C'est mieux la photo du cabinet »), différé à l'époque
  faute de photos.
- **Fait (A1–A8)** : A1 `.v2-main section` en longhands verticaux (le `padding:44px 0` n'écrase plus
  la gouttière `.wrap`) ; A2 `.herologo` supprimé (balise + CSS), plus aucun chevauchement du kicker
  en mobile ; A3 filtres mobiles repliés (bouton « Filtrer » `aria-expanded`/`aria-controls`, panneau
  `.v2-filters-panel`, chips hors panneau, visible sans JS ; « Afficher X montures » masqué ≥780 px) ;
  A4 fiche en deux colonnes ≥980 px (galerie 55 % · faits + CTA à droite) + CTA WhatsApp mobile après
  la première image (`.v2-cta-mobile`, masqué ≥980 px) ; A5 `--fs-sm:1rem`, `--fs-label:.8125rem` ;
  A6 `.rv` porté dans le générateur (cartes, portes, fiche, examen — safeguard mobile : les cartes du
  catalogue restent visibles sans attente de révélation sur téléphone) ; A7 `cabinet-interieur.webp`
  posé sur `/examen-de-vue/` (réelle, sans personne — les scènes avec visages restent exclues) ;
  A8 accueil en vraies photos : F01 (vue), E16 (enfants), H01 (bande services) en `object-fit:contain`
  sur le fond crème du catalogue, enseigne réelle en bande sombre ; **solaire = seule illustration
  restante, légendée** (« Montures photographiées au cabinet. Lunettes de soleil : photo
  d'illustration. »), car aucune monture solaire réelle n'est au catalogue (`frames.json` vérifié).
  Pipeline : `PHOTOS` de `build_dmoptic.py` réduit à `dmoptic-solaires.webp` ; les 4 WebP stock
  devenus sans référence (`dmoptic-lunettes|montures|enfants|mesure.webp`) sont supprimés du dossier
  déployé. Tests ajustés au strict nécessaire : 6 images `data-alt-*`, légende mixte honnête,
  compteurs `v2-card rv`, présence toggle/panneau et `v2-fiche`/`v2-cta-mobile`.
- **Portiques §1b** : builds `--production` + montures OK ; accueil html 0 · a11y `--strict` rc 0
  (1 info « barre fixe ») · images 0 (6 images) · JS 0 · hero 0 ; test Node complet vert (suite 2b
  incluse) ; boucle 48 pages html/a11y/images/js = **48/48 rc 0** partout ; HTTP local 7 routes 200.
- **Revue taste après (même chaîne, avant → après)** : femmes inspect **6 FAIL → 4** (marges mobiles
  0/24 px → 20/21, `edge-text`/`off-centre`/`still-page`/`blank-gap` éteints, premier produit visible
  au premier écran mobile, corps 15,2 → 16 px) ; fiche **5 → 4** (`edge-text` et `empty-middle`
  822 px éteints, CTA visible sans défiler sur desktop comme sur mobile, page 3,1 → 2,1 écrans,
  mouvement 0 → 8 = WARN) ; examen **8 → 5** (0 → 1 photo réelle, média hero 46 %, `focal-point`
  éteint, mouvement 0 → 9 = WARN ; `few-pictures` reste : le plancher du skill est 4 images, une seule
  photo honnête sans visage est utilisable aujourd'hui) ; accueil **10 → 10** en nombre mais pas en
  nature (`small-text`/`body-size` éteints, dégradés mesurés 2 → 1, lint 43 → 41 FAIL ; un
  `covered-text` tablette apparaît à l'échantillonnage : le dock WhatsApp fixe couvre transitoirement
  un titre pendant le défilement — comportement préexistant du dock, hors périmètre Classe A, le
  `padding-bottom` du corps protège la fin de page). Le reste des FAIL = la Classe B, inchangée par
  ruling. Lint après : accueil 41/13 · femmes/fiche 36/23 · examen 40/23 (avant : 43/12 · 38/21 · 42/21).
  Limites dites : inspection sur fichiers locaux (egress Chromium fermé ; `font-fallback` des
  sous-pages = artefacts du serveur local de l'inspecteur, chemins absolus `/fonts/…`) ; le live est
  vérifié par lecture de pages, pas par l'inspecteur.
- **Zip + git + déploiement** : `dmopticsarl.zip` reconstruit (127 entrées, 3 189 187 octets,
  `testzip=None`, 48 `index.html`, 65 WebP de montures). Commit site **`5ac4749`** poussé et vérifié
  (`ls-remote` = HEAD). Déployé d'office (§1f③) sur le projet Vercel de test de King :
  **`dpl_Ctyt42NMev9Y8NGAZxrScuPgHqwu`**, **READY / PROMOTED**, alias `dm-optique-sarl.vercel.app` ;
  vérifié en ligne : accueil (photo du cabinet au hero, F01/E16/H01 réels, légende mixte),
  `/montures/femmes/` (« Filtrer », 24 cartes), fiche F01 (CTA WhatsApp juste après la première
  image), `/examen-de-vue/` (photo réelle de l'intérieur).
- **État / ouverts** : production client inchangée — l'upload Cloudflare reste le geste de King après
  sa validation. Toujours en attente : validation client des 40 + correspondance codes ↔ stock ;
  accord explicite pour les scènes d'examen avec visages ; un lot photo de vraies solaires pour
  retirer la dernière illustration ; Search Console / fiche Google après le déploiement client.
  Pas de brag : le site n'est ni validé par King ni livré au client (§1f② se déclenchera à la livraison).

---

## 20/10/2026 · Photo du cabinet en fond du premier écran (demande client) — redéployé Vercel

- **Demande (pratique, rapportée par King)** : le client demande que la photo du cabinet soit placée
  **en fond de la section hero**, fichier nommé :
  `clients/dm-optic/photoshoot/others/PXL_20261016_131635710.MP.jpg`. Aucun message client direct
  n'est au dépôt pour ce point — consigné comme déclaré par King (règle de confiance). C'est la suite
  directe du souhait client du 10/10 (« C'est mieux la photo du cabinet » au premier écran).
- **Source vérifiée à l'œil** : intérieur réel du cabinet (murs de montures, assise), **aucune
  personne dans la pièce** — les visages visibles sont des affiches murales imprimées. Original
  4365×2887, ~3,0 Mo, avec métadonnées (pointeur GPS présent) : la dérivée publiée est générée par
  `build_dmoptic.py` depuis ce fichier exact (`HERO_BG_SRC` → `cabinet-hero.webp`, 1920×1270,
  226,5 Ko, `-strip` : EXIF vérifié vide après génération).
- **Fait** : la photo devient le fond plein cadre du hero (`.hero-bg`, `object-fit:cover`,
  `fetchpriority=high`, alt FR/EN via `data-alt-*`) sous un voile clair de lisibilité
  (`.hero-scrim`, renforcé sur mobile ; le lavis d'identité `.wash` reste au-dessus). La photo
  encadrée `.herophoto` posée au tour précédent est **retirée** (même image, plus de double emploi) ;
  copie, carte d'identité, couleurs, textes et logo inchangés. Le générateur de sous-pages reprend la
  nouvelle tête : les 48 pages sont reconstruites, sans changement de contenu hors accueil.
- **Portiques §1b** : builds OK ; accueil html 0 · a11y `--strict` rc 0 (1 info « barre fixe ») ·
  images 0 (6 images, fond compris) · JS 0 · hero 0 ; boucle 48 pages html/a11y/images/js = **48/48
  rc 0** ; test Node complet vert (le compte d'images `data-alt-*` reste 6 : le fond remplace la
  photo encadrée) ; HTTP local : accueil, `cabinet-hero.webp`, femmes, examen en 200.
- **Mesure taste après (fichiers locaux)** : accueil **10 FAIL → 9** ; média du premier écran
  **12 % → 75 %** et `focal-point` éteint. Le restant = Classe B inchangée (eyebrow, mono,
  numérotation, micro-labels, lavis, ombre de la carte, filets, boîtes contour) + le `covered-text`
  du dock WhatsApp fixe à l'échantillonnage mobile (préexistant, hors périmètre). Lint source :
  44 FAIL (le voile compte 3 dégradés de plus à la source ; l'inspecteur mesuré ne retient que le
  lavis — le voile neutre sur photo est l'exception prévue par le skill). Captures desktop/mobile
  relues : texte lisible sur le voile, cabinet reconnaissable à droite et en bas du hero.
- **Zip + git + déploiement** : `dmopticsarl.zip` reconstruit (128 entrées, 3 430 100 octets,
  `testzip=None`, 48 `index.html`, `cabinet-hero.webp` inclus). Commit site **`12297ed`** poussé et
  vérifié (`ls-remote` = HEAD). Déployé d'office (§1f③) : **`dpl_HDrZgFEEXcNJ3sH5mBnDpKugErBn`**,
  **READY / PROMOTED**, alias `dm-optique-sarl.vercel.app` ; vérifié en ligne : l'accueil sert
  `cabinet-hero.webp` en première image.
- **État / ouverts** : inchangés — production Cloudflare = geste de King après validation ;
  validation client des 40 + stock, accord visages (scènes d'examen), vraies solaires, Search
  Console / fiche Google après mise en ligne client. Pas de brag (site ni validé ni livré).

---

## 20/10/2026 · Audit combiné post-installation (taste + design-motion-principles + ECC sélectif) — aucun changement de site

- **Commande King** : (1) le fond hero « n'est pas vraiment visible mais c'est OK pour l'instant »
  → constat consigné (F1), **aucune retouche du voile ce tour** ; (2) installer et utiliser
  `kylezantos/design-motion-principles` ; (3) installer et utiliser `affaan-m/ECC` ; (4) refaire
  un audit du site avec les outils installés.
- **Installations faites et prouvées** (détail : `tools/design-motion-principles/README.md`,
  `tools/ecc/README.md`, entrées `ops/TOOL-SCAN.md` du 20/10) : DMP épinglé `4a9ca87`
  (100 % markdown, liens `~/.claude/skills` + `~/.agents/skills`) ; ECC 2.2.3 épinglé `6f1881a`,
  **installation sélective officielle** limitée à six skills d'audit (accessibility,
  production-audit, verification-loop, security-review, seo, click-path-audit — dépendances
  comprises : 149 opérations, doctor OK, status healthy). Harnais complet, hooks runtime, MCP et
  mémoire ECC **non activés** (choix séparé de King sur sa machine, règles TOOL-SCAN 3+5).
- **Méthode / preuves** : taste-skill (mesures navigateur du jour : accueil fond hero 9 FAIL,
  femmes 4, fiche 4, examen 5 — restant = identité Classe B par ruling) ; DMP mode Audit
  (reconnaissance + inventaire motion du gabarit/générateur, checklist + anti-checklist,
  accessibilité) ; ECC (production-audit sur preuves locales, verification-loop, security-review,
  seo, click-path-audit, accessibility). Pondération DMP appliquée et dite : **Jakub primaire**
  (marketing/catalogue livré), **Emil secondaire** (retenue sur CTA/filtres/formulaires, contexte
  santé), **Jhey sélectif** (aucun moment ludique recommandé ici) — à re-pondérer si King le demande.
  Vérification-loop : Build PASS · Types N/A (py_compile OK) · Lint maison PASS (lint taste = FAIL
  d'identité, par ruling) · Tests PASS (Node complet, boucle 48/48 du matin) · Sécurité PASS
  (grep : aucun secret ; surface 100 % statique, ni auth, ni base, ni paiement, ni upload) ·
  Diff : outils + docs seulement ce tour.
- **Verdict production (grille ECC)** : **79/100 — « launchable with caveats »** pour la mise en
  production client (plafond 84 : pas de CI GitHub, chemin critique non testé de bout en bout avec
  le client). Le banc Vercel, lui, est sain : portiques verts, rollback = commits/déploiements
  précédents. **Aucun fichier du site modifié ce tour → pas de redéploiement (§1f③ non déclenché).**

| # | Constat (preuve) | Correctif précis (fichier) | Amélioration durable | Action |
|---|---|---|---|---|
| F1 | **Intention client faiblement perçue** : média hero mesuré 75 %, mais le voile couvre fort à gauche ; le motif le plus visible à droite est le panneau d'affiches (œil en gros plan), pas la profondeur du cabinet. King : « pas vraiment visible, OK pour l'instant ». | Au prochain lot design seulement : rééquilibrer `.hero-scrim` (plus léger à droite/bas) et/ou `object-position` vers le couloir de montures, ou fond plein derrière la copie (`demos/dmoptic-v1.tpl.html`). | Validation visuelle client sur capture téléphone avant Cloudflare, pas sur description. | **King/client décident** ; agent ensuite. |
| F2 | **Boucles d'ambiance infinies non pausables** : `.wash` 26 s et `.band::before` 32 s en `infinite alternate` ; seul `prefers-reduced-motion` les arrête (DMP accessibilité : toute boucle doit pouvoir pauser). | Gabarit : dérive en **une fois** puis repos (ou lavis statique) ; garder le bloc reduced-motion actuel. | Règle motion santé : aucun loop infini d'ambiance sur page patient. | King (le lavis est Classe B) → agent. |
| F3 | **Révélation uniforme** `.rv` 620 ms/14 px sur titres, paragraphes, cartes (anti-checklist : uniform-fade-in + motion-on-mount sur texte statique ; 620 ms > repères Emil 300 / Jakub 500) ; le skiplink anime `top` (layout, déclenché au clavier). | Gabarit : `.rv` ≈ 380 ms/8 px, retirée du texte statique du hero ; skiplink en `transform` ou sans transition. | Budget motion écrit avant build (durées par fréquence). | Agent au prochain lot motion validé par King. |
| F4 | **Bascules instantanées** : panneau filtres mobile, résultats filtrés, contenu FAQ (le chevron tourne en 220 ms) ; à l'inverse la carte d'identité **non interactive** se soulève au survol. | Générateur/gabarit, si King veut le polish : 160–200 ms opacité/translate sur panneau seulement, filtrage gardé instantané ; retirer le lift de `.idcard`. | Porte de fréquence DMP appliquée interaction par interaction. | King choisit ; défaut recommandé = ne presque rien animer de plus. |
| F5 | **Dock fixe vs focus/texte** : taste `covered-text` (tablette puis mobile) + info a11y « barre fixe » — un titre/focus peut passer sous le dock pendant le scroll. | Gabarit : `html{scroll-padding-bottom:96px}` (+ test clavier 390/768 au protocole lecteur d'écran). | Contrôle « focus non masqué » ajouté à la recette d'audit des pages à dock. | Agent au prochain changement de site. |
| F6 | **Dock générique sur les fiches** : le bouton bas « Écrire » ouvre le message rendez-vous d'examen, pas la demande de la monture affichée (le CTA de fiche, lui, est correct). | Générateur : message du dock par type de page (monture sur fiche, catégorie sur catégorie) + assertion Node dédiée. | Click-path tracé jusqu'au message final pour chaque gabarit de CTA. | Agent au prochain lot (conversion, aucun design touché). |
| F7 | **Surface de lancement incomplète** : ni `404.html` ni `_headers` dans la sortie ; en-têtes live non vérifiables depuis la sandbox ; build « production » (canonique + sitemap domaine client, robots Allow) servi tel quel sur le banc Vercel. | Avant Cloudflare : 404 bilingue de marque + `_headers` testé (nosniff, referrer, anti-frame ; CSP seulement après test des inline) ; vérifier les en-têtes en ligne au lancement. | Check « 404 + en-têtes » dans la recette de livraison statique. | Agent prépare, King déploie/valide. |
| F8 | **Preuves de lancement manquantes** : validation client des 40 + stock, domaine client non servi, Search Console/fiche Google à faire, aucun test appareil réel / NVDA-TalkBack / zoom 400 %. | Séquence déjà consignée : validation client → upload Cloudflare par King → Search Console + sitemap + fiche → ligne de base patients/mois. | Pack de preuves pré-lancement (appareil réel + lecteur d'écran) avant tout envoi client. | King/client, puis agent. |

- **Ce qui tient déjà** (à ne pas casser) : `prefers-reduced-motion` complet (états finaux
  préservés, aucun contenu prisonnier d'`opacity:0`) ; transitions de contrôles 120–280 ms avec
  feedback `scale` au `:active` ; transform/opacity partout sauf le `top` du skiplink ; aucun
  pulse/rebond/stagger ; poids maîtrisés (accueil 82 Ko/19,8 Ko gzip, fond hero 226,5 Ko) ;
  aucune donnée client envoyée à un service externe pendant l'audit (preuves locales + live lu).

---

## 20/10/2026 · Correctifs F1–F7 appliqués (ruling King) + UI/UX Pro Max + Impeccable installés — redéployé Vercel

- **Ruling King** : « Deal/correct F1 to F6 implementing all recommended actions » ; installer
  `nextlevelbuilder/ui-ux-pro-max-skill` et `pbakaus/impeccable` ; refaire un audit avec tous les
  outils ; chercher des solutions « even on social media » avec Agent Reach ; implémenter ce qui
  est recommandé, « redesign if necessary ». Rédaction retenue : **correction d'art, pas de
  nouvelle identité** — couleurs, textes, logo, structure de pages et noms inchangés.
- **Recherche (§1f① Agent Reach d'abord, appels réels)** : doctor re-run ; **GitHub OK**
  (repos opticiens relevés), **RSS OK** (releases Impeccable lues), **Exa offline (TLS)**,
  **YouTube TLS-EOF**, **Bilibili network_error**, **Twitter/Reddit non authentifiés**, **Jina
  HTTP 000** → repli natif déclaré. Sources natives citées dans les build-notes : NN/g *Ensure
  High Contrast for Text Over Images* (4,5:1 / 3:1) · Smashing *Designing Accessible Text Over
  Images* (scrim) · W3C WCAG 2.2 SC 2.4.11 *Focus Not Obscured* + MDN `scroll-padding-bottom`
  (scroll-padding = la solution canonique) · Cloudflare Pages docs (`404.html` + `_headers`)
  · fils r/Frontend & r/webdesign (img+object-fit+alt pour un hero accessible ; lisibilité des
  overlays).
- **Installations prouvées** : UI/UX Pro Max pin `56ea9cf` (MIT, recherche Python stdlib locale —
  aucune donnée client dans les requêtes), liens `~/.claude/skills` + `~/.agents/skills`, appels
  réels (`--domain ux`, `--design-system`) ; Impeccable pin `46b822f` (Apache-2.0, skill v0.1.16,
  moteur binaire 0.1.16 obtenu via le paquet npm officiel `@impeccable/cli-linux-x64` — egress
  releases GitHub bloqué — cache `~/.impeccable/bin/0.1.16`, `engine-probe` OK), lien skill.
  Installeurs + README : `tools/ui-ux-pro-max/`, `tools/impeccable/` ; TOOL-SCAN ; PRE-FLIGHT
  §1f⑦/⑧ + §0d.
- **Correctifs appliqués** (gabarit + générateur, portiques verts) :
  **F1** voile hero rééquilibré (gauche protégée .92→.92, droite dégagée .46→.16 ; voile mobile
  allégé ; `object-position:38% 50%` → le couloir de montures visible à droite/bas ; captures
  relues : texte lisible, cabinet reconnaissable) · **F2** lavis `.wash` et `.band::before` en
  une dérive de 2,8 s puis repos (plus de boucle infinie ; reduced-motion inchangé) · **F3**
  `.rv` 620 ms/14 px → **380 ms/8 px** ; kicker/H1/lede du hero **statiques** (apparaissent
  d'emblée) ; skiplink en `transform` (plus d'animation d'une propriété de layout, geste clavier
  instantané) · **F4** panneau filtres mobile animé **180 ms** à l'ouverture seulement (filtrage
  instantané, `prefers-reduced-motion` respecté) ; carte d'identité sans soulèvement au survol
  (ombre gardée) · **F5** `scroll-padding-bottom:96px` sur `html` (SC 2.4.11 : focus jamais sous
  le dock) · **F6** dock WhatsApp **par type de page** : fiche = « je suis intéressé par la
  monture [nom] » (comme le CTA), catégorie = demande catégorie, hub = demande générique
  monture, examen/cabinet/contact inchangés ; assertion Node dédiée · **F7 (bonus 404+headers)**
  `404.html` bilingue noindex (dock, mêmes verrous) + `_headers` prudents (nosniff, referrer,
  DENY, Permissions-Policy) — préparation Cloudflare, CSP reportée (JS inline) · bonus
  cohérence : étapes de l'examen en `h2` (Impeccable : niveau sauté h1→h3).
- **Portiques §1b** : builds OK ; accueil html 0 · a11y `--strict` rc 0 (1 info « barre fixe ») ·
  images 0 · JS 0 · hero 0 ; boucle 48 pages html/a11y/images/js = **48/48 rc 0** ; 404 verte sur
  les 4 contrôles ; test Node complet vert (assertions dock + 404/headers incluses) ; zip
  reconstruit (130 entrées, 3 447 323 o, `testzip=None`).
- **Audit combiné post-correctifs** (tous outils) : taste **accueil 9 FAIL → 9** en nombre mais
  `covered-text` mobile disparu (le dock ne couvre plus le titre du contact dans l'échantillonnage)
  · **Impeccable `detect` 32 → 31** (`skipped-heading` éteint ; restants = 28 « cramped-padding »
  faux positifs du détecteur : nos cartes ont un padding 16–18 px, la photo seule touche le bord —
  vérifié dans le code · 2 « undersized-ui-text » (le « DOUALA » du h1, 8 px calculés, style
  d'affichage du titre approuvé · 1 em-dash advisory, textes figés) · **UI/UX Pro Max** : grille
  UX confirmée (reduced-motion, focus, cibles ≥44 px déjà tenues ; chips à reflow = déjà en
  flex-wrap) ; la « design system » de l'outil (Claymorphism/teal) **écartée** — nouvelle
  identité interdite par les verrous, avis traité comme grille et non comme direction · **ECC**
  : security-review PASS (statique, aucun secret), seo PASS (titres/méta/canonical/JSON-LD
  inchangés), click-path PASS après F6 (chaque CTA mène au bon message) · **DMP** : plus aucune
  boucle infinie, fréquence Emil respectée (CTA/filtres = instantané), Jakub : panneau 180 ms
  subtil. Restes connus et **hors lot par ruling** : Classe B (mono, filets, numérotation…),
  `few-pictures` examen (besoin d'un vrai lot photo), taille h1 (3,6 vw).
- **Git + déploiement** : commit site **`bf9c0ec`** poussé/vérifié → Vercel test
  **`dpl_953Nuy9t59nXNdsXQwiJFn39dG7U` READY/PROMOTED** ; vérifié en ligne : accueil (fond hero
  allégé), fiche F01 (dock « monture F01 » — le CTA bas demande la bonne monture), **404 réelle
  servie** sur une URL inexistante. Zip prêt pour l'upload Cloudflare de King.
- **Redesign complet : non nécessaire** — tous les défauts objectifs de l'audit sont corrigés ;
  ce qui reste est soit l'identité figée (Classe B, ruling séparé), soit du contenu à venir (photos
  solaires, scènes d'examen avec accord). Un redesign remplacerait une identité approuvée par le
  client sans défaut objectif pour la justifier.
- **Reste ouvert** : F8 (validation client 40+stock, Cloudflare, Search Console/fiche Google,
  tests appareil/lecteur) ; production = geste de King après validation.

---

## 20/10/2026 · La photo d'examen réelle entre dans « Nos services » et sur la page Examen (OK client) — redéployé Vercel

**Origine.** King propose la photo `photoshoot/others/PXL_20261016_132758528.MP.jpg` pour la
bande « Nos services » de l'accueil (« what do you think ?? »). Avis rendu avant exécution :
favorable — la bande liste « Examen de la vue » en 01 mais montrait la monture H01, déjà visible
deux fois au-dessus (F01/E16 dans le parcours, H01 juste en dessous) ; la vraie scène d'examen
(autoréfractomètre NIDEK, titulaire en blouse, valise de verres d'essai) apporte une information
nouvelle et crédibilise sans superlatif. Une condition posée : la scène montre **deux visages**
(patiente de profil + assistant) → OK publication requis.

**Ruling King (ask_user).** (1) « OK client déjà acquis » → build + gates + commit + deploy dans
le même cycle ; l'OK visages est verbal, consigné « pratique » (20/10). (2) Périmètre élargi :
la même photo rejoint aussi `/examen-de-vue/` — le constat taste « examen sans image » est clos
sans nouveau shooting.

**Build.** `build_dmoptic.py` : `EXAM_PHOTO_SRC/_NAME/_TARGET` (source client nommée,
`cabinet-examen.webp`, 1920×1200 q76, même `prepare_from` que le hero — recadrage centré,
`-strip` des métadonnées/GPS) + garde « absent du gabarit ». Gabarit : la figure `band-fig`
passe de `monture-h01.webp` (`img-real`, contain) à `cabinet-examen.webp` (cover 16/10 pleine
largeur — la source est 4:3, le recadrage coupe haut/bas et garde les quatre acteurs) ; alt +
`data-alt` FR/EN descriptifs, légende « L'examen de la vue, réalisé au cabinet. » (aucune mention
« Photo d'illustration »). Page examen : figure `v2-photo` insérée entre les 4 étapes et la
liste « À apporter », légende « Un examen de la vue en cours au cabinet : la mesure à
l'autoréfractomètre. » H01 reste au parcours (E14/F01), sur sa fiche et en catégorie hommes.

**Portiques.** py_compile OK ; build production OK (`cabinet-examen.webp` 266,4 Ko) ; boucle
48/48 (html/a11y strict/images/js) ; 404 vert ×4 ; Node vert avec **nouvelle assertion**
(bande `actes` = photo examen + légendes honnêtes, plus de H01 ; compte d'images 6 conservé).
Taste lint statique : **44F/12W avant = 44F/12W après** (`bf9c0ec` comparé) — aucun défaut
ajouté, le restant = Classe B gelée + plancher du skill. Impeccable non relancé ce tour : aucun
CSS/layout changé (échange d'image 1:1), détection précédente déjà consignée.

**Incident sandbox (6ᵉ).** L'environnement est revenu à `b134dd2` avec objets Git perdus et home
effacée. Récupération en mixte jamais dur : `fetch origin` → `git reset --mixed fae12f1` →
`git checkout -- .` → suppression de 4 WebP v1 orphelins non trackés ; réinstallation
taste-skill (§1f, statique). Vérifié : status propre, `ls-remote == HEAD`, zip/photo intacts.

**Git + déploiement.** Commit site **`4bed256`** poussé/vérifié → Vercel test
**`dpl_48wabpiJWTGu6rgCfNUC2aGcpSmm` READY/PROMOTED** ; vérifié en ligne : accueil (bande
« Nos services » sert `cabinet-examen.webp` avec sa légende) et `/examen-de-vue/` (figure sous
les étapes). Zip **131 entrées, 3 720 499 o, testzip OK** — prêt pour l'upload Cloudflare de King.

**Reste ouvert** : F8 (validation client 40+stock, Cloudflare, Search Console/fiche Google,
tests appareil/lecteur) ; Classe B = ruling séparé ; production = geste de King après validation.

---

## 20/10/2026 · Deux outils installés (open-seo, agency-agents) + audit de la photo d'examen + test SEO/AEO — aucun changement de site

**Audit de la photo posée hier (`cabinet-examen.webp`, commit `4bed256`).** 1920×1200, 266,4 Ko,
**EXIF vide** (vérifié `identify -format "%[EXIF:*]"` — aucune sortie), recadrage centré 16/10 qui
tient les quatre acteurs (patiente → autoréfractomètre → praticien → valise de verres d'essai),
légendes honnêtes bilingues. **Flag ouvert :** logos accessoires dans le cadre — NIDEK (gravé sur
l'appareil) et HP (autocollant du portable) — considérés comme équipement contextuel, pas une
revendication commerciale (le verrou « marques » vise les montures *revendiquées*) ; un recadrage
qui les éviterait tuerait la scène. King peut statuer autrement.

**open-seo @ `8713d75` (MIT) — installation sélective.** Les **12 skills markdown** du plugin
officiel vers `~/.agents/skills/open-seo-skills/` (méthodologies `seo-audit`, `local-seo`,
`keyword-research`, `ai-visibility-audit`…). L'**application n'est pas construite** : pnpm absent
du bac, clé **DataForSEO payante** et self-host (Docker/Cloudflare) = décisions de King (coût
récurrent + compte fournisseur). Installeur épinglé `tools/open-seo/install.sh`, **testé de bout
en bout** (12/12 skills, pin vérifié). Entrée TOOL-SCAN.

**agency-agents @ `4e3ac3c` (MIT) — 298 personas.** 19 divisions + strategy copiées vers
`~/.agents/agency-agents/`, **fusion non destructive** vers `~/.claude/agents/` ; frontmatter
vérifié 298/298. Un persona informe, ne décide pas (identité figée, portiques §1b, déploiements
intouchés). Installeur épinglé `tools/agency-agents/install.sh`, **testé de bout en bout**.
Entrée TOOL-SCAN.

**Test SEO/AEO sur le site DM (portion gratuite — faits vérifiés dans `hosting/previews/dmoptic/`).**
✓ robots.txt (Allow + sitemap) · sitemap 48 URL · canonical par page · meta descriptions · OG +
twitter card · 404 noindex + `_headers` prudents · JSON-LD accueil riche (**Optician**,
ContactPoint, PostalAddress, OpeningHoursSpecification, Person, **FAQPage** 6 Q/A) ·
**BreadcrumbList** sur les sous-pages · site statique (vitesse par construction).
**Écart AEO n°1 : `llms.txt` absent** (fichier de découverte pour crawlers IA — checklist premiere
ligne du persona `marketing-aeo-foundations`). Écarts mineurs possibles plus tard : FAQPage
limitée à l'accueil ; fiches sans schema Product (sans prix, offers impossible — choix du client,
sans impact connu sur le trafic local). **Portion payante** (crawl live, positions, backlinks,
Search Console) : bloquée sur la **production** (F8 — Cloudflare = King). Le skill `local-seo`
servira à la fiche Google après mise en ligne.

**Aucun fichier du site modifié → pas de redéploiement (§1f③).**

---

## 20/10/2026 · Propositions implementées : llms.txt en ligne, personas en charge fixe, décisions classées — redéployé Vercel

**P1 — `llms.txt` (écart AEO n°1) : construit, déployé, vérifié en ligne.** Généré à chaque build
par `build_dmoptic_montures.py` (comme `404.html`/`_headers`) : 8 pages-hubs bilingues + 40 fiches
aux **vrais noms accentués de `frames.json`** (pas des slugs — corrigé en cours de build) + 48 liens
exactement, adresse/téléphone/horaires exacts, section Langues. Que du vrai : aucun prix, aucune
marque (NIDEK/HP compris), aucune prétention. **Garde intégré au générateur** : le build échoue si
≠ 48 liens, ou si FCFA/marque apparaît. Portiques : boucle 48/48, 404 ×4, Node verts ; taste
44F/12W inchangé ; zip **132 entrées, 3 722 196 o, testzip OK**. Commit `8cb43bc` → Vercel
`dpl_8pWGChkhjeGJQb9zpQE77mGsisRH` READY/PROMOTED, `/llms.txt` **lu en ligne** (contenu complet).
Fallback assumé : une fiche sans `nom` retomberait sur son slug (URL valide quand même) — le
compte de liens verrouille la structure.

**P2 — DataForSEO / application OpenSEO : décision ENREGISTRÉE = report.** Première mesure
honnête après production = **Search Console** (gratuite, première partie) ; DataForSEO seulement
si un besoin reste non couvert, compte pay-per-call au nom de l'agence, clé jamais dans le dépôt.
Trigger déjà inscrit au TOOL-SCAN.

**P3 — Personas en charge fixe jusqu'à la livraison (validé par l'ordre « implement all ») et
appliquées ce tour :**
- **`marketing-aeo-foundations`** — checklist passée sur le site construit : robots `User-agent: *
  Allow: /` (crawlers IA inclus) ✓ · `llms.txt` ✓ (nouveauté) · sitemap 48 ✓ · contenu FR/EN
  **server-renderé** (les deux langues dans le HTML, lisibles sans JS) ✓ · JSON-LD Optician+FAQ ✓ ·
  pages token-lean ✓. **Verdict : socle AEO vert** — ce qui reste est du contenu à venir (avis
  clients, photos solaires), pas de l'infrastructure.
- **`design-ui-finish-gate-reviewer`** — passe « finish gate » sur accueil + fiche : rien
  d'interchangeable — vraies photos presque partout (une seule illustration honnêtement légendée),
  dock WhatsApp au bon message par type de page, ONOC nommé, adresse/horaires réels, services
  numérotés avec « à apporter ». **Verdict : PASS pour la porte pré-Cloudflare**, deux réserves
  connues : F8 (validation client) et Classe B (identité figée = approuvée, pas un défaut).
- Application honnête : les personas servent de **grilles exécutées par l'orchestrateur** (pas
  d'exécution d'agents séparés dans ce bac).

**P4 — Logos accessoires NIDEK/HP : classé « on garde »** (équipement contextuel, pas une
revendication de marque ; l'alternative tuerait la scène). Validé par l'ordre d'implémentation.

**P5 — Fiche Google : préparation `local-seo` écrite** (portion gratuite) dans
`launch/SETUP-GOOGLE-BUSINESS.md` : champ Services (libellés du site), 3 collections « Produits »,
lien de rendez-vous = wa.me examen, attributs honnêtes, géo-grille reportée avec P2, relais
`llms.txt` noté. L'exécution GBP reste postérieure à la mise en production (jour 1 = claim, déjà
écrit).

**Protocole — §1f⑨ amendé (ordre King)** : tout problème résoluble relevé à l'audit porte sa
**solution long terme** (règle, outil, contrôle structurel), pas seulement le correctif.

**Déploiement : commit site `8cb43bc` → `dpl_8pWGChkhjeGJQb9zpQE77mGsisRH` READY/PROMOTED,
`/llms.txt` vérifié en ligne (§1f③).** Reste : F8 (validation client 40+stock, Cloudflare = King,
Search Console/fiche après mise en ligne) ; Classe B = ruling séparé.

---

## 20/10/2026 · Solutions d'audit implémentées + le site est PRÊT pour Cloudflare (geste de King)

**Solutions long terme (ordre King « implement the solutions proposed in the audit ») :**
- **Classe B → ruling à l'écrit** : la ligne v2 de **`clients/_uniqueness-registry.md`** (en tête)
  porte désormais **« IDENTITÉ FIGÉE APPROUVÉE PAR KING LE 20/10 »** avec l'empreinte complète
  (parcours d'abord, photo réelle partout, crème `#F6EBE0`, marine `#0A1220`, Schibsted + IBM Plex,
  « l'aveu avant la promesse », verrous). Les outils (taste, ECC, personas) consignent les
  dispositifs, ils ne les rejugent plus. La ligne v1 du 24/09 (jamais livrée) reste en historique,
  marquée remplacée.
- **`llms.txt` généralisé au routage** : la ligne « Website build » de PRE-FLIGHT §1 impose
  désormais le fichier de découverte IA généré au build (pattern DM + garde) pour tout site client
  destiné à une production.
- **Runbooks de publication** : deux sections ajoutées à `pre-launch-checklist.md` —
  « La mise en ligne — Cloudflare Pages (pas-à-pas King) » (zip GitHub → Workers & Pages → drag &
  drop → `dmoptiquesarl.pages.dev` → domaine personnalisé → vérifications téléphone → le brag
  §1f② part dès la mise en ligne) et « Search Console + relais » (propriété Domaine TXT, sitemap
  48, inspection + indexation, `llms.txt` contrôlé, fiche GBP pointée). La doc Cloudflare
  Direct Upload a été lue ce jour : drag & drop accepte le zip, limites 1 000 fichiers/25 Mo par
  fichier (nous : 132 fichiers, max ~270 Ko).
- **F8-pack** : la checklist existante EST le rituel (item 10 + sections nouvelles) — rien à
  créer de plus. **Sandbox reverts** : couverts structurellement par §1e (rien à ajouter).
  **Photo solaires réelle** : reste ouvert (attend une photo du cabinet).

**Vérifications « prêt à publier » (exécutées ce jour, sur les fichiers du commit `8cb43bc`) :**
zip `dmopticsarl.zip` 132 fichiers, `testzip` OK ; **0 référence Vercel** dans les HTML ;
canonical/`og:url`/`og:image` = `https://dmoptiquesarl.com` (+ `og.jpg` 75 Ko présent) ;
**0 `noindex`** sur pages et fiches (le 404 garde le sien, voulu) ; aucune ligne « aperçu » ;
`llms.txt` 48 liens. **Aucun fichier du site n'a changé ce tour (docs/registre/checklist) → pas de
redéploiement (§1f③). La publication Cloudflare est le geste de King — le pas-à-pas est prêt.**

---

## 20/10/2026 · King a déployé sur Cloudflare (Workers, upload du zip) — vérifié en ligne par l'orchestrateur

King a déposé le zip sur **Workers & Pages** (projet `dmoptiquesarl`, déploiement `b3ed20c2`
« Manually deployed » Ready) — URL temporaire **`dmoptiquesarl.akwo-king-dev.workers.dev`**
(capture d'écran). Vérifications **en ligne** faites par l'orchestrateur le même jour :
`/llms.txt` ✓ servi intégralement · **404 bilingue servie** sur une URL inexistante (dock au bon
message « passer vous voir », liens relatifs qui suivent l'hôte) · fiche F01 ✓ (multi-angles,
suggestions, WhatsApp à la bonne monture). L'upload Worker sert donc `404.html` et `llms.txt`
correctement — **aucun passage par Pages nécessaire**. Reste côté King : domaine personnalisé
(onglet Domains → + Add Domain → `dmoptiquesarl.com` + `www`), puis vérifications téléphone
(10.5), puis signal à l'orchestrateur → brag §1f②, Search Console (TXT dans la zone), sitemap,
fiche GBP, note finale. À noter : tant que le domaine n'est pas attaché, les partages WhatsApp
depuis l'URL workers.dev arrivent en carte grise (`og:url`/`og:image` pointent déjà vers
`dmoptiquesarl.com` — c'est voulu pour la destination finale) → **envoyer le lien au client
seulement après l'attachement du domaine**.

---

## 20/10/2026 · Le domaine est en ligne (www) — audit production 12/12 vert + brag de livraison produit (§1f②)

**Mise en ligne constatée.** King a attaché **`www.dmoptiquesarl.com`** au déploiement Cloudflare
(projet `dmoptiquesarl`, toujours `b3ed20c2`). **Audit production lu en direct depuis le domaine :
12 ressources, zéro erreur** — accueil ✓ (hero photo, carte, vrais CTA) · catalogue ✓ · catégories
femmes (24 + filtres avec comptes)/hommes (6)/enfants (10) ✓ · fiche F01 ✓ (multi-angles,
WhatsApp à la bonne monture, suggestions) · examen ✓ · le-cabinet ✓ · contact ✓ (Maps, horaires,
paiement) · **404 bilingue sur URL inventée** ✓ · `llms.txt` ✓ · `sitemap.xml` 48 URL ✓.

**Un point ouvert (à King, 2 minutes) : le domaine racine `dmoptiquesarl.com` sans www ne répond
pas depuis le bac** (fetch en échec ; www répond). Or canonical/`og:url`/`sitemap`/`llms.txt`
pointent vers la racine. **Action : Domains → + Add Domain → `dmoptiquesarl.com`** (l'apex se
pose comme le www — la zone est déjà dans le compte), puis vérifier depuis un téléphone. Si la
racine reste morte après ça, on rebascule les canonical sur www (rebuild d'une ligne) — mais
l'apex est la voie propre.

**Brag de livraison produit (§1f②) — `brag.mp4`.** Chaîne réinstallée (home effacée :
`tools/{brag,video}/install.sh`, ffmpeg 7.0.2 via imageio-ffmpeg, ffprobe npm relié — leçon :
`ffprobe` n'est pas `ffmpeg`, l'installeur `@ffprobe-installer` fournit le vrai). Captures
**réelles** du site construit (Chromium local, 1080×1920) : accueil, grille femmes, fiche F01,
examen. Composition Hyperframes 20 s verticale — 5 scènes, identité du site (marine `#0A1220`,
crème `#F6EBE0`, Schibsted + IBM Plex en `@font-face` locaux), chaque scène en mouvement continu
(panoramiques + zooms lents). Musique : **nappe générée ffmpeg** (accord, libre AMK — la piste
ende.app reste interdite). **Portiques dans l'ordre : `check` 0 erreur / 0 warning, contraste
10/10 WCAG AA ; 3 débordements volontaires déclarés `data-layout-allow-overflow` ; snapshots
relus à l'œil (planche 6 frames) ; après 1ᵉʳ rendu, `audit_video_motion` a BLOQUÉ la queue
d'outro (18–20 s figée — la leçon du 19/10 confirmée) → zoom renforcé 1,0→1,15 + dérive,
re-rendu, verdict final OK « mouvement présent dans chaque fenêtre ».** Livrables hors dépôt :
`/home/user/brag-dm/` — `brag.mp4` (20,0 s, 15,3 Mo, 1080×1920, H.264+AAC), `poster.jpg`,
`share-copy.txt`, `brag-plan.md`. **Brouillon : rien n'est envoyé au client sans validation de
King** (lecture téléphone = portique final).

---

## 20/10/2026 (suite) · open-higgsfield audité (non installé) · artefacts du brag dans le dépôt · voie rapide Google décidée

**open-higgsfield — audité, NON installé** (ordre conditionnel de King : auditer d'abord,
installer seulement si utile au flux ou vendable). Ce que c'est : un studio Next.js 16 (1,6 Mo,
`b16a0ef`) qui appelle l'API **payante** Higgsfield (38 modèles — Seedance 2.5, Kling 3, Flux,
Grok Imagine…) avec la clé du compte (`id:secret`) + Vercel Blob pour les uploads. **Verdict
flux : non** — verrous « que du vrai » (aucun visuel IA sur les supports clients, visages IA
écartés, month-1 DM sur les vraies photos), origine API injoignable depuis le bac, pnpm + clé
payante requis. **Verdict vente : non en l'état** — **aucune LICENCE dans tout le dépôt**
(vérifié ; le « free & open-source » du README ne vaut rien juridiquement), dépendance à une API
payante, egress de données client vers un tiers (règle 4). Verdict modifiable si : licence
ajoutée en amont + compte ouvert et testé par King + cas d'usage concret validé. Entrée complète
au TOOL-SCAN.

**Brag : où est la vidéo ?** Le `brag.mp4` (15,3 Mo) reste **hors Git** — règle debout du
19/10 : aucun mp4 versionné (plafond de patch, livrables régénérables) ; il vit dans le bac
(`/home/user/brag-dm/`) et a été présenté dans le visualiseur à King. Les **artefacts légers
entrent dans le dépôt** ce jour : `clients/dm-optic/brag/` — `brag-plan.md`, `share-copy.txt`,
`poster.jpg` (12,5 Ko). Si King statue « versionner le mp4 », c'est un commit — décision
explicite contre la règle.

> **Ruling King du 20/10 (même jour) : le `brag.mp4` EST versionné.** King ne pouvant pas le
> télécharger depuis le bac, il a ordonné « push the video into the repo in the dm optic folder » :
> `clients/dm-optic/brag/brag.mp4` (15,3 Mo, ajouté avec `git add -f` — la règle globale `*.mp4`
> du `.gitignore` reste en place pour tout le reste). Exception fichier par fichier ; le défaut
> pour les futurs brags reste « hors Git ». Détail : `tools/hyperframes/README.md` (section
> « Règle de livraison vidéo »).

**Hyperframes — audit sur preuves (demande King du 20/10).** Déjà installée (chaîne brag, CLI
0.8.177, Apache-2.0 vérifiée sur le paquet npm) et déjà utilisée : c'est le moteur qui a rendu le
brag DM plus tôt dans la journée. Verdict : **flux OUI (en production), vente OUI** — offre
« vidéo d'annonce de livraison » défendable (rendu local 0 FCFA contre ~19 $/vidéo hébergé),
tarif = décision de King. **Aucun second installeur créé** (runtime unique via
`tools/brag/install.sh` — leçon ECC) ; documentation et verdict dans `tools/hyperframes/README.md`
+ entrée TOOL-SCAN dédiée.

**Voie rapide Google (décision King — le client répond lentement, fuseaux différents).** Les
comptes sont créés par l'agence **au nom du cabinet, maintenant, sans lui** : e-mail
`dmoptiquesarl@gmail.com` (secours = King, 2FA, mot de passe JAMAIS dans le dépôt public),
**Search Console** propriété Domaine + TXT dans la zone Cloudflare de King (zéro dépendance
client) puis sitemap + indexation, première mesure = **Cloudflare Web Analytics** (toggle, zéro
build — GA4 = décision séparée), **fiche GBP** créée avec les données déjà préparées — la
vérification SMS vers le 656 122 239 fait de **« transférer le code »** la seule action du
client (asynchrone, 10 s, pas de séance à planifier). Ligne de propriété écrite au client +
« pratique » au log. Section « Voie rapide » ajoutée au `SETUP-GOOGLE-BUSINESS.md`. Rappel
ouvert : l'**apex** `dmoptiquesarl.com` (sans www) reste à attacher (Domains → Add Domain).

## 20/10 — Brag ENVOYÉ ; Google lancé chez King ; anthropics/skills audité (propriétaire, non installé) ; capacité documentaire maison + livrables client

**Message + brag.mp4 ENVOYÉS à M. Domche (15:09, double check ; le client avait répondu « Ok » à
12:35).** §1f② CLOS : le portique final (lecture téléphone) est passé. Le message annonce le
site en ligne + l'ordre des prochaines étapes ; **restes ouverts** : la racine
`dmoptiquesarl.com` (sans www) à attacher (aucune confirmation dans la capture) et le solde
75 000 à la livraison (rappel à la main de King, le message n'en parlait pas — son choix).

**Google — King exécute chez lui (ordre explicite : Google AVANT les comptes sociaux).**
`SETUP-GOOGLE-BUSINESS.md` complété : valeurs exactes de l'écran de création de compte
(`dmoptiquesarl@gmail.com`, prénom « DM OPTIQUE »/« SARL », secours et 2FA sur King, mot de
passe jamais dans le dépôt public) + ordre en 5 étapes : apex d'abord (Add Domain) → Search
Console propriété Domaine + TXT dans la zone Cloudflare → sitemap + indexation → Web Analytics
(toggle) → fiche GBP (SMS 656 122 239, « transférer le code » = seule action client) → ensuite
seulement FB/TikTok.

**anthropics/skills — audité sur ordre conditionnel (« audit and see…then install »), verdict
NON install :** le dépôt mélange skills Apache-2.0 et 4 skills documentaires (docx/pdf/pptx/xlsx)
**« source-available, not open source »** — LICENSE.txt © Anthropic PBC avec interdictions
explicites d'extraction hors Services, copie, works dérivés, redistribution : notre pattern
(clone + copie + pin) est exactement ce qui est interdit. Les skills Apache sont redondants avec
la pile AMK. **Retenu : la méthodologie, réimplémentée en propre** — `tools/docs/xlsx_build.py`
(openpyxl MIT, aucun matériau amont copié) ; **nouvelle règle TOOL-SCAN** : « repo qui se dit
open-source sans LICENSE = propriétaire, non installable » (même leçon qu'open-higgsfield).

**Livrables du jour produits avec la nouvelle capacité (usage réel, pas un toy) :**
`clients/dm-optic/launch/LISTE-40-MONTURES-2026-10.xlsx` (inventaire des 40 montures depuis
frames.json — livrable de confirmation au client) + `LISTE-40-MONTURES-WHATSAPP.txt` (version
à coller dans le fil) + `sales/OFFRE-VIDEO-LIVRAISON-2026-10.md` (fiche du service additionnel
« vidéo d'annonce de livraison » — tarif = décision King).

**Durcissement brag (leçon ffprobe du 20/10) :** `tools/brag/install.sh` lie maintenant
`@ffprobe-installer/linux-x64/ffprobe` → `~/.local/bin/ffprobe` à la fin de l'installation
(imageio-ffmpeg n'embarque que ffmpeg ; sans ffprobe, `hyperframes render` échoue au probe,
exit 8) — testé : `ffprobe -version` OK depuis le symlink.

## 20/10 (soir) — Bande « Assurances acceptées » sur le site ; apex VIVANT en production ; GSC/GBP/Analytics par les captures ; humanizer installé

**Section assurances (ordre King : « affiliated assurances — Belife Insurance, Willis Towers Watson,
Groupe Activa », avec consigne copywriting explicite).** Accueil : nouvelle section claire
`#assurances` entre la bande marine « étapes » et la FAQ — h2 bilingue « Votre assurance, acceptée
au cabinet. », lede qui dit les trois noms + ce qu'il faut apporter (carte d'assuré, ordonnance) +
l'aveu « Ce qui est couvert dépend de votre police », 3 chips **statiques** (consultation UI/UX Pro
Max : valeur en texte, pas cliquable, pas de statut par couleur seule), note de sortie honnête
(« la liste évolue, demandez sur WhatsApp »), CTA WhatsApp « Vérifier ma prise en charge » (lien
dérivé du data-fr, même mécanique que les six actes). `/contact/` et `/le-cabinet/` : entrée
`Assurance` ajoutée au bloc de faits, après `Paiement`. Tokens existants uniquement (identité
figée intouchée) ; `.rv` inchangé (reduced-motion préservé). Copy passée au crible humanizer
(26 motifs « Signs of AI writing » — installé le même jour, premier usage réel).

**Portiques :** audit_html 0 faute ×3 pages · audit_a11y --strict rc=0 ×3 · audit_images 0 ×3 ·
audit_hero (vérifications machine) · check_inline_js 0 · `test_dmoptic_page.mjs` toutes assertions ·
lint taste FAILs **44 = 44** (identité figée documentée ; WARN 12→13 = la bordure 1px des chips,
même famille délibérée) · llms.txt 48 · sitemap 48 · zip `dmopticsarl.zip` 132 fichiers testzip OK
(format exact de l'ancien : `-D`, zéro entrée de répertoire).

**Déploiement §1f③ :** commit `e881fdd` (site) + `29e449b` (humanizer) → Vercel
`dpl_4Za3oJ1UmR8hiS7P2ESuBTUmmUbG` READY/**PROMOTED** (28 s) — lecture live de l'alias production :
section complète en ligne (titre, 3 chips, note, CTA pré-rempli) ✓.

**Production (Cloudflare, geste de King) :** **l'apex `dmoptiquesarl.com` est VIVANT** — lu en
direct : accueil complet + `sitemap.xml` 48 URLs toutes en apex. Le blocage canonical/sitemap de la
semaine est levé. La prod sert encore le zip du matin (`b3ed20c2` @ `8cb43bc`) : **la bande
Assurances n'y est pas encore** — retélécharger `dmopticsarl.zip` (commit `e881fdd`+) et refaire
l'upload Worker (même procédure).

**GSC (capture) :** propriété = **préfixe URL `https://www.dmoptiquesarl.com/`** (pas une propriété
Domaine) ; sitemap `/sitemap.xml` soumis → « Couldn't fetch », 0 page. Diagnostic : (1) état
transitoire fréquent dans les heures qui suivent la soumission ; (2) la sitemap liste des URLs
**apex** alors que la propriété est **www** — Google peut les ignorer (hôte non vérifié) et le
canonical du site est l'apex. **Recommandation : propriété Domaine `dmoptiquesarl.com`** (TXT dans
la zone Cloudflare, le runbook initial) qui couvre apex+www d'un coup ; la propriété www peut rester
comme second jeton. robots.txt = Cloudflare managed (Allow / + ligne Sitemap, Googlebot autorisé).

**GBP (capture) :** Business Profile créé, écran « Customize profile » avec upsell Google Ads —
**conseil : Skip** (aucune dépense pub sans décision King) ; continuer le remplissage (catégories,
horaires, photos, services) puis vérification SMS vers le 656 122 239.

**Web Analytics (captures) :** actives, setup automatique, site `dmoptiquesarl.com` — premières données :
15 pages vues / 10 visites (24 h), chargement 866 ms, INP et CLS verts, **LCP partiellement rouge**
(échantillon minuscule, probablement le hero WebP sur mobile lent) → à relire à J30 avec le SEO, pas
une action immédiate.

**humanizer (ordre King) :** audit-before-install passé — **MIT**, un SKILL.md autonome (26 motifs),
zéro réseau/hook → **INSTALLÉ** (`tools/humanizer/install.sh`, pin `8c307f3`, copie du SKILL.md vers
`~/.agents/skills/` + miroir `~/.claude/skills/`, ni plugin marketplace ni npx skills). Rôle :
**second passe** copywriting APRÈS la loi maison (§11b, COPY CRAFT GATE, MESSAGES §1) ; TOOL-SCAN à
jour ; premier usage réel = la bande Assurances.

**Dépôt :** 8ᵉ wipe du bac détecté (restauration sur la base `b134dd2`, arbre sale) → remède debout
appliqué (`reset --mixed` sur le tip ls-remote + checkout), **zéro perte** (tout était poussé).

## 20/10 (nuit) — Production Cloudflare = bande Assurances EN LIGNE (vérifiée sur l'apex) ; propriété GSC Domaine VÉRIFIÉE ; plan d'indexation

**Upload Cloudflare de King vérifié en direct :** `https://dmoptiquesarl.com/` sert la bande
« Votre assurance, acceptée au cabinet. » (3 chips + note + CTA pré-rempli) et `/contact/` la
ligne `Assurance` — la production tourne sur le contenu `e881fdd`. Site livré et complet.

**GSC :** propriété **Domaine `dmoptiquesarl.com` VÉRIFIÉE** (capture : sélecteur de propriété sur
le domaine, Overview « Processing data » = normal à J0). La sitemap listée est encore celle soumise
sous l'URL www — colonne « Last read » vide = Google ne l'a pas relue. **Plan validé :** (1)
soumettre aussi `https://dmoptiquesarl.com/sitemap.xml` (hôte canonique) dans la propriété
Domaine ; (2) « Demander une indexation » sur 9 URLs seulement — `/`, `/montures/`, les 3 hubs de
catégorie, `/examen-de-vue/`, `/le-cabinet/`, `/contact/`, une fiche témoin (F01) — les 40 autres
fiches arrivent par la sitemap et les liens internes des hubs (quota de demande d'indexation +
zéro gain à les faire une par une) ; (3) lecture de la sitemap attendue sous 24–48 h → statut
« Success / 48 discovered ».

**Dépôt :** 9ᵉ wipe du bac (même restauration base `b134dd2`, mêmes 4 webp orphelins non suivis
réapparus, nettoyés) → remède debout, zéro perte.

## 20/10 (nuit 2) — GSC : 5 indexations demandées puis quota (4 restent pour le 21/10, rappel debout à la checklist) ; Scrapling audité puis installé

**GSC :** King a demandé l'indexation de `/`, `/montures/` et les 3 hubs de catégorie (5 URLs) —
la 6ᵉ tentative (`/examen-de-vue/`) a touché le **quota quotidien** (« Quota exceeded, try again
tomorrow » — normal sur une propriété neuve). **Rappel debout inscrit à la checklist** (section
Search Console) : le 21/10, demander les 4 restantes — examen, cabinet, contact, fiche témoin F01.
La relecture du statut de sitemap (« Success / 48 ») reste au 21/10 aussi.

**Scrapling (ordre King : « audit then install if it meets the criteria ») — verdict : INSTALLÉ.**
BSD-3-Clause (© Karim Shoair) lue dans le clone épinglé `fd53131` (v0.5, 18/10) ; framework de
scraping adaptatif (parser qui retrouve ses éléments après refonte, fetchers statique/navigateur,
spiders, robots.txt obey, skill agent OFFICIEL fourni — garde anti-injection `--ai-targeted`) ;
`AI_POLICY.md` amont = règle de contribution (divulgation IA dans les PR), pas de restriction
d'usage. **Installation :** `tools/scrapling/install.sh` (pip `--user` + skill officiel copié vers
`~/.agents/skills/scrapling/` + miroir `~/.claude/skills/`) — **preuve par appel réel** : GET
`github.com/D4Vinci/Scrapling` → 200, `title` extrait (API v0.5 = `.css('sel::text').get()`).
**Limites testées et documentées :** fetchers navigateur exigent `scrapling install` (CDNs bloqués
depuis le bac) → plein potentiel sur la machine de King ; drapeau robots au niveau spider/session
en 0.5 (pas au one-off get). **Règles d'usage :** pages publiques, jamais Google/Facebook (ToS),
débit limité, aucune donnée client sortante, **chaque cible = décision nommée**. Usage AMK visé :
contrôles approfondis §1c, **veille concurrentielle mensuelle** (service défendable — tarif =
décision King), vérifications NAP. TOOL-SCAN à jour.

## 20/10 (nuit 3) — GBP CRÉÉ (valeurs NAP à aligner) ; prototype de veille Bonabéri livré (3 cibles sélectionnées sous délégation)

**GBP créé** (capture : « You manage this Business Profile », bouton Website). `SETUP-GOOGLE-BUSINESS.md`
+ section « Profil CRÉÉ » : 3 alignements NAP demandés (adresse complète « Ndobo Mayor, Immeuble
West Hotel… » vs « Ndobo Bonaberi » capturé ; +237 656 122 239 vs « 6 56 12 22 39 » ; horaires
lun–sam 8:30–17:30) + complétion (photos/description/services = §Données) + social profiles APRÈS
FB/TikTok + Ads = Skip + code SMS si vérification en attente.

**Prototype de veille accepté et livré : `sales/veille-prototype-bonaberi-2026-10-20.md`.**
Cibles sélectionnées par l'orchestrateur (délégation King, critères : présence Bonabéri + web
public + positionnements distincts) : **Valdoz Optic** (Entrée forêt Bar, 677 61 04 41, 3 villes,
« Meilleur cabinet d'optique au Cameroun 2024 » — Innovation Awards 05/03/2025, pas de site propre
trouvé), **iris — l'Optométriste** (Immeuble MTN Bonabéri, réservation en ligne Setmore sur un
réseau de ~16 points, ABONNEMENT « consultations/examens/rdv gratuits », lun–ven 8–15h sam 8–13h),
**Bronze Eye Care & Optics** (200 m après Royal City, fiche annuaire seule, 0 avis — le concurrent
invisible). Méthode consignée : pages publiques seulement, zéro FB/IG scrapé, sources datées ;
industrialisation = Scrapling chez King. Lecture stratégique honnête : DM déjà devant sur le web ;
à surveiller = réputation Valdoz (→ 5 premiers avis Google DM) + modèle abonnement iris (noté,
jamais copié sans ruling). Offre mensuelle décrite, tarif = décision King.

## 21/10 — Firecrawl audité NON installé ; hypit audité INSTALLÉ (CLI testé) ; message avis Google approuvé ; TikTok démarré (voie email cabinet) ; gabarit de veille debout

**Firecrawl (ordre « audit and install ») — verdict NON INSTALLÉ :** AGPL-3.0 (usage interne OK)
mais cloud payant (compte + clé, injoignables du bac) et self-host = Docker + Redis + RabbitMQ +
PostgreSQL NuQ + FoundationDB + Playwright — Docker absent du bac (vérifié) ; le besoin (veille
mensuelle, pages publiques) est couvert par Scrapling (20/10, zéro infra). Règle 5 : pas d'état
sans usage. Réévaluation seulement si compte cloud testé chez King ET besoin non couvert
(/extract LLM massif). Entrée TOOL-SCAN.

**hypit (ordre « audit and install ») — verdict INSTALLÉ :** moteur vidéo SVML pour agents
(check/plan/pricing/build), Apache-2.0 **modifiée lue en entier** — travail pour clients PERMIS ;
interdits multi-tenant/revente/logo-strip ; outputs à nous. Exécutable npm `@hypit/hypit@0.3.1`
installé (`tools/hypit/install.sh`, `~/.npm-global`) — **testé** : `hypit --version` → 0.3.1 +
CLI complet. Rendu complet NON testé au bac (Chromium au build) → premier usage réel = décision
King ; Hyperframes reste le moteur brag. **Règles debout :** jamais cloner la vidéo réelle d'un
créateur pour un client ; `check` + `pricing` avant tout build ; logo amont conservé ; portiques
habitude. Détail `tools/hypit/README.md` + TOOL-SCAN.

**Message « avis Google » approuvé et rédigé :** `launch/MESSAGE-AVIS-GOOGLE-2026-10.md`
(message WhatsApp à M. Domche + phrase du comptoir + réponses aux objections ; règle : clients
réels seulement, jamais d'avis acheté). Objectif : 5 avis d'ici samedi.

**TikTok démarré (King suit écran par écran) :** voie du 03/10 mise à jour — création avec
l'**email du cabinet** (`dmoptiquesarl@gmail.com`, décision 20/10 étendue aux réseaux), username
`dmoptique.bonaberi`, nom affiché `DM OPTIQUE – Bonabéri`, anniversaire = King, mot de passe dans
son gestionnaire. Section « Création du compte » ajoutée au SETUP-TIKTOK.

**Gabarit de veille debout (approuvé par King, 21/10) :** `sales/VEILLE-GABARIT-MENSUEL.md` —
structure fixe en 6 points (cibles nommées, collecte datée sourcée, comparatif, devant/à
surveiller, actions suggérées, limites), 2 pages max, humanizer.

**GSC rappel du jour (rappelé à King) :** les 4 « Demander une indexation » restantes +
relecture statut sitemap (attendu « Success — 48 »).

**Dépôt :** 10ᵉ wipe du bac (même restauration base `b134dd2` + webp orphelins) → remède debout,
zéro perte.

## 21/10 (2) — TikTok CRÉÉ (capture) ; recherche marketing W43 livrée ; bio : 3 candidats, décision King

**Compte créé par King** (capture) : `DM OPTIQUE SARL` @`dmoptique.bonaberi237`, logo avatar +
story, 0/0/0. Le nom affiché = le nom de la fiche Google (cohérence inter-plateforme — validé
par la recherche §3). Rien publié. **Objection bio de King** : l'ancienne bio (« inscrit à
l'ONOC ») sonnait personnel — fait recoupé : l'ONOC est l'inscription du SARL (#102, 021/2016,
annuaire recoupé en octobre), pas le diplôme de M. Domche ; la bio est réécrite du côté client
quoi qu'il en soit (§12 de la recherche).

**Recherche ordonnée par King (verbatim conservé en tête de fichier), livrée :**
`sales/research/2026-W43-techniques.md` — 11 frameworks étudiés un par un (Purple Cow,
StoryBrand SB7, Cialdini 7, LF8, biais cognitifs, différenciation, USP, preuve sociale/autorité,
branding, psychologie, digital marketing), chacun avec source datée + application DM, puis la
synthèse : **« le client ne veut pas des lunettes »** — il veut voir sa vie normale, être pris
au sérieux, ne pas se faire avoir, protéger ses enfants, être bien vu. 7 décisions en découlent
(avis Google n°1 — message parti ce jour ; USP « le seul à Bonabéri dont vous voyez toutes les
montures avant de vous déplacer » ; client-héros dans chaque vidéo ; angle enfants ; effets
leurre/fausse rareté récusés ; peak-end ; rien ne change à l'identité figée — la recherche la
valide). **La création TikTok reprend après la décision de King sur la bio** (candidats A/B/C
dans le SETUP, recommandation A, 74/70/78 caractères).

## 21/10 (3) — bio B, premier TikTok prêt à tourner, gabarit W43 implémenté

**Bio TikTok — King choisit B** : `Opticien à Bonabéri · examen de vue & montures · WhatsApp 656 122
239` (69 caractères). Raison : le nom affiché `DM OPTIQUE SARL` ne dit pas le métier ; « opticien » est
le mot tapé. Le guide écran par écran est dans `launch/SETUP-TIKTOK.md`. **Le Business Account s'est
révélé impossible** : le parcours de vérification exige un pays, et le Cameroun est absent du sélecteur
(page TikTok « About business verification » : six marchés africains — Algérie, Égypte, Kenya, Maroc,
Nigeria, Afrique du Sud). On reste en compte personnel. **Conflit assumé** avec la checklist SEO TikTok (« lien en bio = le site ») :
le champ Website n'est pas encore disponible pour ce compte → numéro écrit d'abord, site dès que le
champ apparaît.

**Message avis — envoi 21/10 à 09:00**, pas à 2h du matin. Un lien `wa.me/?text=` pré-rempli est dans
le fichier pour que King n'ait qu'à choisir la conversation ; suivi jusqu'à samedi (5 avis), relance
unique vendredi si zéro.

**Premier TikTok — plan validé** (`content/month1/w1/tiktok-01.md`) : 22 s, 56 mots, 5 plans tournés
au cabinet avec un téléphone, **aucune image IA, aucun visage**, une monture réelle (F24 · carrée
écaille). Structure : cas client → miroir → monture réelle + les 40 en ligne → ONOC en preuve (une
fois) → **sortie honnête** + numéro. Le script était le point faible de la V1 du 02/10 : elle ouvrait
sur le certificat du cabinet, ce que la recherche W43 et l'objection de King sur la bio condamnent
tous les deux. **La V1 n'est pas supprimée** : elle reste valable comme UGC IA, avec un renvoi en tête.

**Vérifié en production avant d'écrire « c'est en ligne »** : `https://dmoptiquesarl.com/montures/`
→ 200, 24 femmes + 6 hommes + 10 enfants = **40 montures** ; fiche `f24-carree-ecaille` → 200, 2
photos. Le site dit « une photo ne dit pas tout » → le script dit « vous les voyez avant de vous
déplacer, et vous les essayez au cabinet » : la promesse reste vraie.

**« Implement » de la solution long terme — le gabarit est câblé, pas seulement écrit :**

| Fichier | Ce qui y est |
|---|---|
| `sales/research/2026-W43-techniques.md` §12b | le gabarit (5 beats · 7 interdits · 6 cases) + la table de câblage + la bio B décidée |
| `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md` | règle debout « le gabarit W43 est la porte de tout contenu client » |
| `content/scripts/README.md` | la porte W43 en tête de la convention de script client |
| `content-plan-month1.md` §10 | la porte appliquée au mois 1 + ce qui change vs le plan du 01/10 |
| `posting-calendar.md` | amendement du 21/10 (calendrier réel) + règle 11 au §6 |
| `PRE-FLIGHT.md` §0d + routage | la ligne « gabarit W43 » → fichiers gouvernés ; le routage contenu la nomme |
| `month1/README.md` | `w1/tiktok-01.md` ajouté à la table des fichiers |
| `pre-launch-checklist.md` | suivi TikTok + avis ; item 4 passé 🟠 (compte au nom du cabinet mais mot de passe côté King → transfert à prouver avant livraison) |

## 21/10 (4) — Business Account TikTok : impossible au Cameroun, et ce que ça change

**Constat (captures de King, 21/10).** Le passage en Business Account ouvre *Business registration →
Basic info → Address → Select*. La recherche « Camero » répond « No results found for Camero —
Couldn't find your country? Don't worry, more countries will be available soon. » Le bouton **Next**
reste inactif sans pays. Le formulaire a par ailleurs demandé le site (www.dmoptiquesarl.com) et
« Industry with audience restrictions » — renseignés pour rien : sans pays, la validation est bloquée.

**Vérification à la source.** Page TikTok « About business verification for TikTok accounts »
(consultée le 21/10/2026) : la table des marchés ne compte, pour l'Afrique, que l'Algérie, l'Égypte, le
Kenya, le Maroc, le Nigeria et l'Afrique du Sud. **Le Cameroun n'y figure pas.** Les listes de création
self-serve du Business Center et des comptes publicitaires ne le mentionnent pas davantage.

**Décision.** Compte **personnel**. Ce qu'on ne fait pas : choisir un autre pays (fausse adresse →
risque de suspension, et la région du compte oriente la distribution), soumettre le formulaire avec un
pays inventé, créer un second compte, passer par un VPN. Aucun de ces contournements ne vaut le compte
d'un client.

**Ce que ça change vraiment.** Rien sur la capacité à publier, à être trouvé ou à convertir : la bio B
porte le numéro, le CTA est parlé et le commentaire est épinglé — c'est exactement le repli déjà prévu
par la « contrainte plateforme ». On perd le badge, le champ site cliquable et les exports Business.
**On garde les analytics de base** : TikTok Studio (Profil → ☰ → TikTok Studio → Analytics) — la page
d'aide TikTok précise que les creator tools sont ouverts aux comptes personnels comme aux comptes
business ; repli : « More insights » sous chaque vidéo.

**Nuance honnête.** Nos fichiers de prospection de septembre montrent des opticiens camerounais avec un
badge Business (K Vision Care, Maff, Espace Lunetterie) : ces comptes datent d'avant la vérification
obligatoire. Un compte neuf ne peut pas passer par ce parcours aujourd'hui. Ça ne change pas le plan.

**Corrigé partout** (aucune instruction ne doit continuer à demander un Business Account) :
`launch/SETUP-TIKTOK.md` (section « ⛔ Business Account » + ordre de la suite + optimisation locale),
`content/strategy/TIKTOK-SEO-CHECKLIST-2026-10.md` §A, `posting-calendar.md` (amendement),
`pre-launch-checklist.md` (suivi), `content/month1/w1/tiktok-01.md` (§6 mesure, §8).

## 21/10 (5) — Facebook : la page se prépare, avec une contrainte Meta dit d'avance

**Aucune page n'existe** (recherche du 21/10 : que des homonymes à l'étranger). On part d'une page neuve,
même nom que partout : `DM OPTIQUE SARL`.

**La contrainte Meta, écrite avant le clic.** Une page Facebook ne se crée pas avec un email seul : il
faut un **profil personnel réel** derrière. Un profil au nom du cabinet (« DM Optique SARL » comme
personne) est inauthentique — suspension possible, et **la page tombe avec le profil**. Donc : page créée
depuis le profil de King, immédiatement placée dans un **portefeuille d'entreprise Meta `DM OPTIQUE
SARL`** (c'est le portefeuille qui détient la page), 2FA, AMK en accès personne, **M. Domche
administrateur** dès qu'il a un profil ou à la livraison. C'est la même logique que le compte Google et
TikTok — l'agence opère, le cabinet possède — mais Meta impose un détour par une personne physique.

**Visuels produits et relus aux vrais recadrages** (pas au hasard) :

| Fichier | Contrôle |
|---|---|
| `profile-1024.png` | logo détouré, testé **en cercle** à 200 px et à 64 px — « DM OPTIQUE » reste lisible |
| `cover-1640x624.jpg` | relu en **desktop 820×312** (fichier entier) et en **mobile 2,4:1** (côtés coupés) ; le texte le plus bas s'arrête à 496 px sur 624 |
| `post-01-cabinet-1200.jpg` | photo réelle du cabinet, bandeau marine, adresse/horaires/bouton |

Aucune image IA, aucun visuel générique : la règle « le site ne montre que du vrai » vaut pour la page.
Aucun prix, aucune marque de monture, aucun visage inventé.

**Premier post** écrit sous la porte §12b — il commence par la situation du client (« En fin de journée,
vous éloignez votre téléphone pour lire ? »), pas par l'annonce de notre existence. C'est le même texte
que le TikTok n°1 : une production, deux vitrines, et le même message pré-rempli pour mesurer.

**Rien n'est publié** avant le feu vert de King ; la capture de la page servira de vérification, comme
pour TikTok.

## 21/10 — Meta au Cameroun : la carte avant la page

Demande de King : savoir **ce qui est disponible au Cameroun et ce qui ne l'est pas** avant de créer la
page — « cette information sera aussi nécessaire quand nous publierons et lancerons des publicités ».

**Livré : `launch/META-CAMEROUN-2026-10.md`.** Tableau maître (16 lignes, ✅/⚠️/❌), la partie publicité
en six points, une section « ce que ça change pour la page », une section « ce que ça change pour les
pubs du mois 1 », une règle de revue trimestrielle, et onze sources datées.

**Les cinq constats qui comptent :**

1. **Publier et sponsoriser : oui.** Meta prélève la TVA camerounaise sur les publicités depuis le
   1ᵉʳ octobre 2020 — un compte publicitaire dont le pays de vente est le Cameroun est donc prévu par
   Meta, ce n'est pas un bricolage.
2. **Mais pas en francs CFA.** XAF n'est pas dans la liste des devises acceptées : le compte sera en
   **USD ou EUR**. Le budget se lit en FCFA et se règle en devise.
3. **Et avec une carte, pas du mobile money.** Visa/Mastercard ou PayPal. L'exemple officiel de paiement
   manuel local pour l'Afrique est Orange Money **en Côte d'Ivoire, en XOF** — aucune section Cameroun.
   D'où une ligne de suivi nouvelle : **carte internationale à vérifier avec King avant la semaine 2**.
4. **Le commerce ne s'ouvre pas.** Shops (liste Meta 2026), Meta Pay (liste Afrique sans Cameroun),
   monétisation (Content Monetization : Nigeria et RDC oui, Cameroun non). Pour un cabinet qui ne publie
   pas de prix, **ce n'est pas une perte** — c'est même une protection.
5. **Le badge n'est pas documenté.** Meta Verified : « select regions », sources contradictoires →
   on ne le promet pas, on ne paie pas d'intermédiaire, on vérifie dans l'app si l'occasion se présente.

**Ce que la recherche a changé dans les documents :** `SETUP-FACEBOOK.md` gagne un **§0 bis** (tableau
de disponibilité + les trois conséquences, aucune bloquante) ; `posting-calendar.md` gagne la ligne
« Meta au Cameroun » et **le budget de S2 corrigé** (5 000 FCFA de diffusion ⇒ ≈ 5 963 FCFA débités,
TVA comprise) plus le prérequis carte ; `pre-launch-checklist.md` gagne la même ligne et une alerte 🔴.

**Méthode :** les listes tierces se contredisent (Marketplace, Verified) → **seules les pages Meta font
foi**, et quand Meta ne publie rien, le document dit « non documenté » au lieu de trancher. Un mur n'est
pas une porte qui s'ouvre en insistant : la revue est **trimestrielle**, pas quotidienne.

## 21/10 (6) — La page est en ligne, le texte ne suivait pas la photo

**Ce qui est fait :** la page `DM OPTIQUE SARL` existe (créée par King), catégorie Opticien, bio posée,
logo en photo de profil, 0 follower. Business Suite : `asset_id 1417215104801727`, plan hebdomadaire
2/7 — il reste « Create an ad account », « Publish one story », « Connect Instagram ».

**Le défaut, et il est réel :** le premier post partait avec « *Cette monture est dans notre stock, et
les autres sont sur le site…* » devant **la photo du cabinet**. La phrase vient du script du premier
TikTok, où le plan montre **une** monture (F24) : là, elle est juste. Devant un mur de montures, elle
devient fausse deux fois — on ne sait pas de laquelle on parle, et « les autres sont sur le site »
laisse croire que celle qu'on voit n'y est pas.

**La correction :** le texte passe au pluriel et s'appuie sur ce que la photo prouve —
« *Ce mur, c'est notre stock — pas une image de catalogue. Les montures que vous voyez sur le site sont
ici, dans ce cabinet…* ». La sortie honnête et le CTA ne bougent pas.

**La règle qui reste :** *le texte suit le visuel.* Une photo de cabinet → on parle au pluriel, du
stock, du lieu. Une photo d'une monture → singulier, et **on la nomme**. Les deux versions vivent
côte à côte dans `SETUP-FACEBOOK.md` §6, avec un interdit correspondant au §4 : plus jamais un texte
écrit pour une autre image.

**La carte :** King déclare une carte utilisable → le prérequis publicitaire du mois 1 est levé. Reste
le contrôle du premier débit en devise (banque qui bloque, plafond, frais de change). Le test de
5 000 FCFA est lançable en semaine 2.

**Incident sandbox (12ᵉ wipe) :** le bac est revenu à `b134dd2` alors que le remote était à `5d3b9c7` —
la première lecture de `SETUP-FACEBOOK.md` a donc rendu l'**ancienne** version (5 sections, sans §0 bis
ni §6). Récupération en mixte (`reset --mixed 5d3b9c7`, `checkout -- .`, 4 webp orphelins supprimés),
jamais `--hard` ; arbre propre. **Leçon :** lire HEAD avant de lire un fichier.

## 21/10 (7) — La carte : on prend l'identifiant, on laisse l'usine

King a envoyé l'export **Quick Builder** de Google (Locator Plus) et sa capture : la fiche est bien
punaisée au West Hotel, et le panneau annonce « All locations (1) ».

**Ce que le code dit de lui-même :** `YOUR_API_KEY_HERE` deux fois, `mapId` vide dans la config et
`DEMO_MAP_ID` dans la balise, bandeau « Finish account setup ». Tel quel, il n'affiche rien. Ce n'est pas
un raté : c'est l'écran où Google s'arrête tant que la clé et la facturation n'existent pas.

**Verdict : on n'installe pas.** Un locator sert à chercher **parmi** des lieux — il y en a un. Il
ajouterait une clé à restreindre, un compte de facturation, et un script Google sur un site qui n'en a
aucun. Conditions de réexamen écrites dans `site/maps/PLAN-CARTE-2026-10.md` (clé restreinte par
référent, API Maps JS seule, alerte de budget, `mapId` cohérent, consentement si cookie).

**Ce qu'on garde, et qui vaut plus que le widget :** le **`place_id`**. Il transforme deux liens
approximatifs en deux liens exacts — et il ne demande ni clé, ni facture, ni JavaScript :

| Page | Avant | Après |
|---|---|---|
| Accueil | bouton « Itinéraire » **caché** (`MAP_URL` vide) | **visible**, ouvre l'itinéraire vers la fiche |
| Contact | recherche par **nom** (liste, homonymes possibles) | `query_place_id` — **la** fiche |

**Portiques :** `audit_html` 49/49 · `audit_a11y --strict` rc 0 sur 49 · `check_inline_js` 49/49 ·
`audit_images` 0 · `test_dmoptic_page.mjs` vert · zip `dmopticsarl.zip` reconstruit (132 fichiers,
`testzip` OK).

**Déploiement : non fait ce tour.** Le bac n'a ni jeton Vercel ni projet lié, et `api.vercel.com` sort du
périmètre réseau — je ne prétends pas avoir déployé. Le zip est prêt ; la mise en ligne reste le geste de
King sur Cloudflare, et le banc d'essai Vercel sera redéployé au prochain tour avec les accès.

**Bonus non appliqué :** le `place_id` donne aussi un **lien d'avis direct**
(`search.google.com/local/writereview?placeid=…`). Il est en annexe du message d'avis — **pas dans le
message approuvé**, qui ne bouge pas sans l'accord de King.

## 21/10 (8) — « Est-ce qu'il reste quelque chose ? » : la réponse en une page

King a le site, la page Facebook et TikTok. La question mérite une réponse qui ne mélange pas **ce qui
reste à produire** et **ce qui reste à faire**.

**Rien de neuf à produire pour le contrat.** Le Pack Global (site + mise en place FB/TikTok + gestion
mensuelle) est construit. Ce qui reste, ce sont des **gestes** — et surtout **trois preuves** qui
conditionnent le solde de 75 000 : les comptes au nom du client, le transfert écrit, et le site sur **son**
domaine.

D'où `launch/CHECKLIST-LIVRAISON-2026-10.md` : inventaire de ce qui est livré et prouvable, reste par
propriétaire (AMK 4 · King 8 · cabinet 3), **PV de remise** à remplir, et cinq vérifications de 60 secondes
que King peut faire seul — dont deux qui prouvent que le **dernier zip** est bien en ligne (le bouton
« Itinéraire » qui était caché, et « Ouvrir dans Maps » qui doit ouvrir **la** fiche).

**Un écart signalé, pas corrigé :** la couverture Facebook en ligne n'est **pas** celle du dépôt. King a
posé une bannière de marque — logo en grand, nom, promesse, pastille WhatsApp — là où l'asset du dépôt
montre la **photo réelle du mur de montures**. Les deux défendent des choses différentes : l'une prouve la
marque, l'autre prouve **que le lieu existe**. Comparatif et recommandation (hybride : photo + promesse)
dans la checklist §7 ; décision à King, ce n'est pas bloquant.

**Détail qui compte :** la bannière en ligne annonce « **Réparation** ». C'est cohérent avec les six
services du site, mais **aucun des six n'est confirmé par le cabinet** (item 8 de la checklist). On ne
laisse pas un service affiché sans confirmation.

## 21/10 (9) — Couverture hybride, Vercel rétabli, verdict sur les affiches

### ① La couverture hybride

`facebook-assets/cover-1640x624-hybride.jpg` + `build_cover.py` (relançable). **La photo réelle** du mur de
montures, rendue en « cover » — la première version laissait deux bandes marine en haut et en bas, avec
une arête franche : recadrée en hauteur, fondue sur 420 px, voile à 10 %. Le texte reprend **la phrase du
cabinet** (« Voir mieux, grandir plus loin »), pas une phrase d'agence.

**Trois contrôles automatisés** plutôt qu'un avis à l'œil : texte le plus bas 496/624 ; bord droit du texte
707 px **contre** 738 px pour la photo (aucun chevauchement) ; marge mobile 41 px après le recadrage
2,4:1. Simulations 820×312 et 640×360 relues. C'est la leçon de la cover précédente, partie en trois
itérations : **on mesure, puis on regarde**.

### ② Vercel : le déploiement existait, mais il ne se déclenchait plus

Le projet `dm-optique-sarl` est lié au dépôt avec `rootDirectory: hosting/previews/dmoptic`, mais le
dernier déploiement datait de `29e449b` — quatre commits de retard. Le connecteur Vercel permet de le
relancer explicitement : **`dpl_J2UiUijPC5fSgooYe1k2fGpGwQvc`**, READY / PROMOTED, alias
`dm-optique-sarl.vercel.app`, commit `931d464`. **Règle tenue** : à partir de maintenant, tout changement
du site est déployé **avant** d'être annoncé, et l'état est consigné.

### ③ Les affiches enfants — bonnes, à deux conditions

Reçues en trois versions (deux vertes, une bleue). **Archivées** dans `launch/facebook-assets/posters/`.
Verdict complet dans `content/month1/w1/facebook-post-posters.md`. En résumé :

- **La bonne idée** : la cible (les parents), la saison (la rentrée), et **la même promesse que la
  couverture** — la page commence à avoir une voix.
- **Condition 1 — les montures en médaillon ne sont pas au cabinet.** Comparaison faite avec les 40 réelles :
  **aucune monture verte** au catalogue, et le violet brillant des affiches 1 et 2 ne correspond pas aux
  photos de E14/E15 (violet sombre et mat). Or l'affiche dit « Disponible chez DM Optique ». Un parent
  peut venir demander **cette** monture. Deux sorties : King confirme le stock, ou je remplace les
  médaillons par de vraies montures du cabinet.
- **Condition 2 — les visages sont générés.** Règle R2 + label Meta. Trois options proposées, la
  recommandation étant **A : publier sans le visage** (médaillon + les trois promesses + le titre) — plus
  différenciant, et zéro risque.

**La légende est prête** (815 caractères) : elle commence par la situation de l'enfant, ne nomme aucun
symptôme, oriente vers l'examen, et finit par la sortie honnête de la maison. **Rien n'est publié.**

### ④ États corrigés

- **Pas de `@username`** : King a constaté que la page n'en propose pas. L'adresse reste numérique → **on ne
  l'affiche nulle part** (site, fiche Google). C'était une ligne de ma liste, elle tombe.
- **Horaires ✅**, **bio TikTok ✅**, **1er TikTok programmé le 22/10 à 5h30**.

## 21/10 (10) — « Opticien optométriste » : la demande du client, vérifiée avant d'être appliquée

Le client écrit : « *nous ne sommes pas seulement Opticien mais OPTOMETRISTE également […] relier à
chaque fois les 2* ». Deux réflexes, dans cet ordre : **ne pas appliquer à l'aveugle**, **ne pas
refuser**.

**Vérification** : la loi camerounaise **n° 99/001 du 7 avril 1999**, art. 2, définit l'opticien comme
titulaire *soit* du diplôme d'opticien lunetier, *soit* du **diplôme d'opticien optométriste** ; l'art.
3(2) donne à ce dernier des attributions en plus (formuler et concevoir l'équipement). L'optométrie n'est
donc **pas** une profession séparée au Cameroun — et l'ONOC poursuit l'usurpation de titre. Écrire
« optométriste » seul serait **plus risqué** que d'écrire « opticien » : ce n'est pas un titre protégé.

**Forme retenue : « opticien optométriste ».** Les deux mots du client, dans l'ordre du droit.

**Appliqué — 12 endroits dans le gabarit, 6 dans le constructeur :**

| Où | Avant | Après |
|---|---|---|
| `<title>` | Opticien à Bonabéri, Douala | Opticien optométriste à Bonabéri, Douala (58 car.) |
| og:title / og:description | Opticien… | Opticien optométriste… (144 car.) |
| Kicker du premier écran | Opticien à Douala · inscrit à l'ONOC | Opticien optométriste à Douala · inscrit à l'ONOC |
| Carte d'identité | « Opticien inscrit » / « L'opticien » | « Opticien optométriste » / « Le titulaire » |
| Légende de la carte | Opticien inscrit à l'Ordre… | Opticien optométriste, inscrit à l'Ordre… |
| Alt de la photo d'examen | opticien en blouse blanche | opticien optométriste en blouse blanche |
| Pied de page | Opticien inscrit à l'ONOC | Opticien optométriste inscrit à l'ONOC |
| vCard (`TITLE:`) | Opticien | Opticien optométriste |
| JSON-LD | description sans le titre | description + `jobTitle` sur le fondateur |
| Pages examen / cabinet (4 phrases) | opticien inscrit à l'ONOC | opticien optométriste inscrit à l'ONOC |

**Décision de détail :** la ligne « L'opticien / M. Domche Noumbi » de la carte est devenue
« **Le titulaire** ». Le libellé complet ne tenait pas dans la colonne, et « Le titulaire » ne dit rien de
faux — le titre est écrit juste en dessous, dans la légende, en entier. On préfère un libellé neutre à
un libellé tronqué.

**Portiques :** html **49/49** · a11y `--strict` **rc 0 sur 49** · JS **49/49** · images **0** ·
`test_dmoptic_page.mjs` vert · AEO **0** · hero **0**. Zip **132 fichiers**, `testzip` OK.

**Ce qui reste à réviser côté plateformes** (gestes de King, textes fournis) : bio Facebook (237/255),
bio TikTok (71 car.), catégorie secondaire « Optométriste » sur Facebook et Google, description Google.
**TikTok n° 1** : le montage est déjà tourné — on ne refait pas la vidéo pour un bandeau, le titre complet
passe dans la bio et la légende, qui se modifient au moment de publier.

## 21/10 (11) — le ton client, et trois montures qui parlent d'elles-mêmes

**① Le ton.** King a envoyé la description Google Business qu'il veut voir partout : « *Découvrez la
différence chez DM OPTIQUE SARL…* ». Le ton est juste — invitation, « vous », la famille, le lieu, et
l'ONOC **en dernier**. C'est devenu une règle debout (`content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md`,
section « le ton client »), avec une limite : la chaleur se **prouve**, elle ne se déclare pas. Trois
expressions de sa version sont des superlatifs non vérifiables (« soins d'exception », « les plus hauts
standards », « les meilleures mains ») → deux versions de la description sont au dossier :
A (la sienne, 545 car.) et **B (745 car., recommandée)**, même rythme, promesses vérifiables.

**② La correction d'attribution.** Le « D'accord je vais faire les modifications » du 21/10 est **King**,
pas le client. Corrigé dans `RULE-CREDENTIAL-CLAIMS.md`, `CHECKLIST-LIVRAISON` §8 et l'`Activity-Log`.
Conséquence pratique : **c'est King qui pose les bios** Facebook / TikTok / Google (il a les accès) ;
AMK fournit les chaînes exactes, et on ne renvoie pas la tâche au cabinet.

**③ Les posts en photos réelles.** Les 65 photos du cabinet sont sur un fond (246, 236, 225) qui est
**le chaud de la marque** : la photo peut se fondre dans une carte sans cadre. Nouveau script
`launch/social/build_frame_cards.py` → trois cartes 1080×1350 (F01 ovale dorée · H08 aviateur · E16
enfant), titre en Schibsted Grotesk, preuve en bas à droite (« Opticien optométriste · inscrit à
l'ONOC »), pastille WhatsApp verte. Fichiers : `launch/social/cards/card-0{1,2,3}-*.jpg`, 78–86 Ko.
Légende et commentaire épinglé dans `content/month1/w1/facebook-post-famille.md`.

**④ Le site est sur le domaine.** `dmoptiquesarl.com` (Cloudflare) sert la version « opticien
optométriste » : `title`, kicker, carte, pied de page et **sitemap 48 URL** vérifiés. La preuve n° 3 du
solde est donc remplie. Vercel reste le miroir de contrôle, pas la production.

## 21/10 (12) — le stock n'est plus un chiffre, et Google devient un canal

**① Ruling « aucun chiffre de stock ».** King : « *avoid mentionning the number of frames available
everywhere since this can change at any moment* ». Un compte est vrai un jour et faux le lendemain.
Retiré partout : **le site** (les 3 portes « N montures », la phrase d'intro des catégories, la meta
description, le compteur initial « N montures », le bouton « Afficher N montures »), le partage de
livraison et le dossier. Le **compteur de filtre** reste, mais il compte les fiches **affichées**
(« 12 affichées ») et se calcule à l'affichage — ce n'est pas un stock annoncé. Rebuild 47 pages + 40 fiches,
portiques verts, **zip 132 entrées** régénéré et **déployé**.

**② La description Google : version A.** King a choisi sa version (545 car.), superlatifs compris. Consigné
comme **ruling du titulaire** dans `SETUP-GOOGLE-BUSINESS.md`, avec la version B gardée au dossier comme
substitut immédiat. On ne la « corrige » pas en silence.

**③ Bios posées.** Facebook et TikTok sont à jour avec le titre complet — les deux lignes passent en ✅ dans
le calendrier, la checklist et les deux guides.

**④ Le module Google Posts — vérifié, cadré, planifié.** Recherche complète dans
`launch/GOOGLE-POSTS-2026-10.md`. Ce qui est **prouvé** : Google archive les posts après 6 mois, accepte
une programmation récurrente, et **rejette** un post dont le numéro de téléphone n'est pas rattaché à la
fiche → le numéro passe par le bouton « Call now ». Ce qui est **mesuré** : le test contrôlé de Sterling Sky
(9 semaines, 441 mots-clés) ne trouve **aucun effet de classement** ; Whitespark 2026 (GBP 32 %, avis 20 %)
ne liste pas les posts comme facteur. Donc : **conversion, pas classement**. Quatre posts prêts (S1→S4),
un par semaine, avec photo réelle, un seul bouton et UTM.

**⑤ Le zip devient une commande.** `demos/pack_dmoptic.py` : zip déterministe (entrées triées, dates figées,
`testzip`), refuse de produire un paquet si `index.html`/`sitemap.xml`/`robots.txt`/`llms.txt` manquent.
Deux exécutions donnent le même SHA-256 — on peut donc dire « c'est bien ce build-là qui est en ligne ».

## 21/10 (13) — la ligne de base, écrite avant les résultats

Les 4 posts Google sont **programmés** (27/10 → 17/11), la fiche Yandex est **hors de portée** (le cabinet
ne la contrôle pas → on n'y touche pas, point de veille seulement), et le site **sans chiffres de stock**
est en ligne sur `dmoptiquesarl.com` (vérifié : « Des montures à essayer au cabinet », plus aucun nombre).

Reste le point qui décide de tout : **la ligne de base**. Un guide de 10 minutes est au dossier
(`launch/LIGNE-DE-BASE-GOOGLE-2026-10.md`) : où sont les 9 chiffres, **quelle fenêtre de dates** choisir
(28 jours glissants, arrêtés au dimanche — sinon deux lectures ne sont jamais comparables), le tableau à
remplir, la capture d'écran à garder, et le **carnet du cabinet** (appels / WhatsApp / visites / « comment
nous avez-vous trouvé ? ») qui est la seule façon de relier un post à un patient.

Trois décisions y sont écrites **d'avance** pour ne pas interpréter après coup : premier bilan le **16/11**,
on regarde **appels + itinéraires** avant tout le reste, et **aucune promesse de classement** (Sterling Sky).
Le dossier `launch/baseline/` est créé pour les captures.

**Limite assumée** : le site n'a aucune mesure d'audience. Les liens des posts portent leurs UTM, mais
personne ne peut les lire. Deux options sont posées dans le guide — Cloudflare Web Analytics (gratuit, sans
cookie, une ligne de script à poser) ou rien. Non tranché : c'est un ruling de King, pas une décision
technique.

## 21/10 (14) — audit SEO complet, et la ligne de base est faite

**Ligne de base relevée.** 0 appel, 0 message, 0 itinéraire, 0 clic site, 0 vue de fiche — et **moins de
50 recherches ont affiché la fiche**. C'est le point zéro, et il est sain pour une fiche de quelques jours.
Décision de lecture : au 16/11, on annonce des **chiffres absolus**, jamais des pourcentages calculés sur
zéro.

**Le cahier quotidien est abandonné** (ruling King : « ça sera donner plus de travail à mon client »). Il
est remplacé par **une phrase** au moment du paiement — « comment nous avez-vous trouvé ? » — notée sur le
support que le cabinet utilise déjà, plus **3 chiffres** que King relève le lundi. Un dispositif qu'on
n'arrive pas à tenir ne mesure rien.

**Les cookies : non.** Cloudflare Web Analytics tourne déjà sur le domaine, **sans cookie**, et donne
visites / pages / référents / Core Web Vitals (c'est lui qui a fourni les chiffres de l'audit). Il ne lit
pas les UTM → on attribue par **page d'arrivée** (une par post). GA4 est écarté : bandeau de consentement,
40 Ko de script, base légale à expliquer — disproportionné.

**Audit SEO des 49 pages** (`seo/AUDIT-SEO-2026-10-21.md`, outil `tools/qa/audit_seo.py`) : 20 contrôles,
10 verts complets. **1 096 liens internes, 0 cassé, 0 page orpheline** · **245 images, 245 alt, 245
width/height** · un seul H1 partout · canonical 49/49 · 404 personnalisée servie (testée en ligne).
Trois écarts : **6 fiches montures partagent 2 descriptions** (F10/F11 et H01/H02/H05/H08 — même
catégorie + forme + couleur), **h1 vers h3** sur `/contact/`, `/le-cabinet/` et la 404, et **sitemap sans
`lastmod`**. Deux vrais sujets : **aucune version anglaise indexable** (`<html lang="fr">`, 0 hreflang,
0 URL `/en/`, alors que le texte EN est dans le DOM mais masqué) et **le LCP** — l'élément lent est nommé
par Cloudflare (`cabinet-hero.webp`, 232 Ko, 1920 px, **aucun `srcset` sur les 245 images**), P90 3,2 s,
P99 8,4 s.

**Rien n'a été construit** — l'audit est un constat, avec un ordre d'attaque en 7 lignes en attente de
ruling. Le seul document d'action produit est la liste des **10 URL à indexer aujourd'hui**
(`seo/URLS-INDEXATION-2026-10-21.md`).

## 21/10 (15) — les six correctifs d'audit, et le site existe enfin en anglais

**Le miroir `/en/` est en place : 48 pages.** Jusqu'ici le site était bilingue *à l'écran* seulement :
`<html lang="fr">` partout, aucun `hreflang`, aucune adresse anglaise. Google ne pouvait donc pas servir
une page à « optician Douala » ou « eye test Bonaberi ». Le miroir est fabriqué par le générateur :
même DOM (le contenu bilingue y était déjà), langue inversée, liens réécrits, titres et descriptions
traduits, `hreflang` réciproque. Une fiche = deux adresses, un seul contenu à maintenir.

Les textes anglais des 40 montures vivent dans `clients/dm-optic/site/frames-en.json`, indexés par code.
**Le build refuse de tourner si une monture n'a pas sa traduction** — une page à moitié française sous
`/en/` coûterait plus cher que l'absence de page.

**Le reste des correctifs :** `srcset` sur la photo d'accueil (35 / 86 / 226 Ko selon l'écran, + `preload`
en `imagesrcset`), descriptions de montures rendues uniques par la référence, `lastmod` dans le sitemap
(daté sur la dernière modification réelle), pied de page passé en `h2` (plus aucun saut h1→h3), schéma
`Optician` enrichi (`image`, `logo`, `sameAs` TikTok, `geo`, `hasMap`). `Product` : non fait, comme
recommandé.

**Deux bugs corrigés au passage :** le `preload` de la photo d'accueil était recopié sur les 47 autres
pages (86 Ko inutiles par page visitée), et le bouton FR/EN ne changeait que l'affichage — il change
maintenant d'adresse, ce qui est la seule façon d'avoir deux URL indexables.

**Mesure :** `audit_seo.py` couvre désormais le `hreflang` (cible existante, réciprocité, `lang` du
document). Résultat sur 97 pages : tout à zéro sauf le fil d'Ariane de la 404 (voulu, elle est en
`noindex`). Livraison : zip 182 entrées.

## 21/10 (16) — le kit du premier TikTok

Le script existait, le tournage était fait ; il manquait tout ce qui se colle **autour** de la vidéo.
Trois pièces produites : la **couverture 1080×1920** (`build_frame_cards.py --cover`, la F24 réelle,
l'accroche du script, texte placé dans le carré central pour survivre au recadrage de la grille de
profil), les **sous-titres manuels** (`.srt`, 8 blocs, découpe aux frontières de phrase, jamais l'auto)
et une **fiche de publication** qui dit quoi faire à 5h30, dans l'ordre, avec la légende, le commentaire
épinglé et le message de réponse qui rend la conversation attribuable.

**Un défaut trouvé au passage, à trancher :** la **seconde photo de la fiche F24** montre une monture
translucide multicolore, pas l'écaille à détail doré. La fiche affiche donc deux montures différentes —
c'est la règle « le texte colle à la photo » qui tombe. La vidéo n'est pas concernée (le plan 3a
n'utilise que la bonne photo) ; c'est le site qu'il faut corriger.

## 22/10 (17) — le déploiement manuel est abandonné

**Le vrai problème n'était pas la taille du site.** 183 fichiers, 9 Mo : la limite d'un Worker est de
20 000 fichiers et 25 Mo par fichier. C'est **l'outil d'envoi du tableau de bord** qui plante — il
n'affiche ni progression ni erreur, il annonce 184 fichiers quand il y en a 183, et son propre bandeau
dit qu'il ne gère que HTML/CSS/JS.

Trois fichiers ajoutés au dépôt pour ne plus jamais passer par lui : `wrangler.toml` (quel dossier
publier, quelle page servir en 404), `.github/workflows/deploy-dmoptic.yml` (envoi depuis GitHub) et le
mode d'emploi `launch/DEPLOIEMENT-CLOUDFLARE-2026-10-22.md` (route Workers Builds recommandée, route
GitHub Actions, route terminal). **Fusion dans `main` = site à jour.**

Vérifié dans la documentation Cloudflare : les Workers avec assets **prennent en charge `_redirects` et
`_headers`** (2 000 redirections statiques, 100 règles d'en-têtes) — la redirection www → apex survivra
donc à la nouvelle méthode de publication.

## 22/10 (18) — la branche ne se met pas dans wrangler.toml

King a posé la bonne question : chaque conversation ouvre une branche neuve, donc un réglage
« branche de production » dans Cloudflare devient faux à chaque chat.

**Correction d'une idée fausse (la mienne, en creux) :** `wrangler.toml` **ne porte pas de branche**, et
Cloudflare n'en lit aucune dedans. Y écrire `branch = "arena/…"` aurait l'air d'un réglage et n'en serait
pas un — le genre d'illusion qui coûte une soirée de diagnostic. Le fichier dit seulement **quel dossier
publier** et **quelle page servir en 404**.

La branche se décide à deux endroits : *Settings → Build* dans Cloudflare (à changer chaque chat), ou un
fichier de workflow avec `branches: ['arena/**']` (à ne faire qu'une fois, couvre toutes les branches
présentes et futures). Le modèle est versionné dans `tools/deploy/workflow-deploy-dmoptic.yml` — hors de
`.github/workflows`, parce que l'outil qui pousse ce dépôt n'a pas le droit d'y déposer un workflow
(GitHub réserve ça aux comptes humains). Il se colle en une minute depuis l'interface GitHub.

Mode d'emploi réécrit en entier : `launch/DEPLOIEMENT-CLOUDFLARE-2026-10-22.md` (§0 les chiffres, §1 la
règle de la branche, §3 publier aujourd'hui, §4 le workflow une fois, §5 le rituel par chat).

## 22/10 (19) — le nom du Worker, et le premier build

Le tableau de bord a donné la réponse que je ne pouvais pas deviner : **le Worker s'appelle
`dmoptiquesarl`** (sans tirets), et non `dm-optique-sarl` comme je l'avais supposé. Cloudflare l'a
signalé lui-même — *« Update wrangler.toml in your repo to keep settings consistent »*, avec la ligne
exacte à corriger. Un `name` faux aurait créé un **second** Worker, le domaine restant sur l'ancien :
la panne silencieuse que je redoutais. Corrigé au commit `9f5c26c`, qui déclenche le premier build.

**Workers Builds est branché** : dépôt `AKWOKING/AMK`, production `arena/2fffee3b-amk`, build command
vide, deploy command `npx wrangler deploy`, racine `/`.

**Sur le jeton API :** le modèle **« Edit Cloudflare Workers »** suffit et il est le bon choix — il
contient les trois droits nécessaires (`Workers Scripts: Edit`, `Account Settings: Read`, `Workers
Routes: Edit`). Un jeton personnalisé oblige à les retrouver à la main, et un oubli donne un
« Authentication error » qui ne dit pas lequel manque. Et surtout : **ce jeton n'est pas nécessaire**
tant qu'on reste sur Workers Builds — il ne sert qu'à la publication depuis GitHub Actions.

## 22/10 (20) — `_redirects` a cassé le déploiement ; il est retiré

**Le journal de build a parlé.** Workers Builds fonctionne (clone, `wrangler` 4.151.3, assets téléversés
— 180 déjà en place, `+ /robots.txt`), puis échoue à la création de **version** :

```
Invalid _redirects configuration:
Line 1: Only relative URLs are allowed. [code: 100324]
```

**Mon erreur :** j'ai écrit `https://www.dmoptiquesarl.com/* https://dmoptiquesarl.com/:splat 301` sur la
foi de la documentation « Cloudflare Pages ». Or **Workers n'accepte que des chemins relatifs**, et
surtout **`_redirects` ne compare jamais les hôtes** : une redirection d'hôte ne peut pas s'y écrire,
quelle que soit la syntaxe. Un fichier qui n'aurait jamais pu fonctionner, et qui a bloqué le site trois
déploiements de suite.

**Retiré** du générateur et du dossier publié. Zip : **182 entrées** (sha `a07ad7c2a0c0a30e…`). La
redirection `www` → apex se règle dans la zone (**Rules → Redirect Rules**, modèle « Redirect from WWW to
root ») — ce n'est pas bloquant, le `canonical` pointe déjà l'apex.

**Effet de bord à retenir :** quand la création de version échoue, les assets sont quand même
téléversés, mais **le site en ligne ne bouge pas**. C'est ce qui donnait « le build ne se lance pas »
alors qu'il se lançait très bien.

**Sécurité :** le jeton API a été collé en clair dans la conversation → à rouler immédiatement. Il n'est
de toute façon pas nécessaire à Workers Builds.

## 22/10 (21) — le site publie tout seul, et il est vérifié en ligne

Après retrait de `_redirects`, le build est passé au vert (commit `617eea1`). **Vérifié sur le domaine
public, pas dans le tableau de bord :**

- `/en/` sert la page anglaise (« DM OPTIQUE SARL — Optometrist optician in Douala ») ;
- `/en/montures/femmes/f01-ovale-doree/` sert « F01 · Oval, gold » ;
- `/sitemap.xml` annonce **96 URL** (48 FR + 48 EN) avec `lastmod` ;
- une fiche française affiche les libellés anglais dans le DOM et la section « You may also like ».

Workers Builds est donc branché pour de bon : **envoi sur `arena/2fffee3b-amk` = publication**, sans zip,
sans glisser-déposer, sans écran qui tourne dans le vide.

**Reste, hors du site :** la redirection `www` → apex (zone → Redirect Rules), et la resoumission du
sitemap dans Search Console.

## 22/10 (22) — un « Retry » ne rattrape pas un commit périmé

Le second échec de la journée n'était pas une régression : le bouton **Retry build** rejoue **le commit du
build**, pas le dernier. Celui relancé portait `1dfee35`, c'est-à-dire l'état **d'avant** le retrait de
`_redirects` — donc le même message, `Only relative URLs are allowed`, pour la même raison. Le site en
ligne, lui, était déjà à jour depuis le déploiement de `617eea1` (vérifié : `/en/` en anglais, sitemap à
96 URL). Un build rouge sur un commit ancien n'annule pas un déploiement réussi ; il occupe le badge.

Trois boutons à ne pas confondre, désormais écrits dans le mode d'emploi (§3 quinquies) : **Retry** (le
commit du build), **New deployment** (la tête de branche), et rien (un `push` construit le dernier).

**Jeton API :** décision King — pas de révocation, il reste **local**. Vérifié qu'aucun jeton complet
n'est dans le dépôt (`git log -S` sur le préfixe : rien) ; le fragment de huit caractères qui traînait
dans une note interne a été retiré. `.gitignore` refuse maintenant `.dev.vars`, `.env*`, `*.token`,
`CLOUDFLARE_*` et `.wrangler/`.

## 22/10 (23) — 96 pages découvertes, et la redirection www passe en attente

**Le build est vert** (`Success: Build completed`, version `f3288fc2`, 39 s). Workers Builds publie donc
pour de bon, et les deux hôtes servent la nouvelle version (vérifié sur `www` et sur l'apex).

**Search Console a retourné la situation.** Deux sitemaps soumis, deux résultats :

| Sitemap | Statut | Pages |
|---|---|---|
| `https://www.dmoptiquesarl.com/sitemap.xml` | **Success** | **96** |
| `https://dmoptiquesarl.com/sitemap.xml` | **Couldn't fetch** | 0 |

Google lit donc parfaitement le sitemap **sur `www`**, et échoue sur le **même fichier** en apex. La
découverte est faite : 96 URL, toutes en apex (celles que le site déclare en `canonical`).

**Conséquence directe : la redirection `www` → apex est reportée.** Elle ferait passer Google de
l'adresse qui est lue vers celle qui échoue — l'inverse du but recherché. Ordre à respecter : apex
lisible d'abord, redirection ensuite. Le test qui tranche est « Test live URL » sur l'apex, dans Search
Console ; selon le résultat, soit c'est un état périmé (resoumettre), soit l'apex refuse le robot
(Security → Events).

C'est la deuxième fois aujourd'hui qu'une de mes recommandations doit être retirée devant les faits. La
règle que j'en tire : **ne pas proposer une règle de redirection avant de savoir ce que le robot sait
déjà lire.**

## 22/10 (24) — les deux sitemaps au vert, la redirection repart

**Correction de mon propre diagnostic.** J'avais conclu, sur une capture de 18 h, que l'apex refusait
Googlebot parce que son sitemap restait en *Couldn't fetch* alors que celui de `www` passait. La capture
suivante montre les **deux entrées en Success, 96 pages chacune**. Le refus n'existait pas : c'était un
**état périmé** de la soumission du 21/10, faite avant le déploiement.

Deux fois de suite aujourd'hui, j'ai bâti une recommandation sur une capture unique. La règle : **une
capture, c'est un instantané, pas une mesure** — attendre la seconde lecture avant de conclure à un refus.

**Ce qui en sort, et qui est solide :**

- **96 pages découvertes**, deux fois, sur les deux hôtes. Le sitemap ne bloque plus rien.
- **La redirection `www` → apex est de nouveau la bonne étape** : elle envoie Google d'une adresse lue
  vers une adresse lue. Après elle, on **supprime l'entrée `www`** de Search Console (elle passera au
  rouge, c'est normal) et on garde l'apex.
- **Le sujet suivant n'est plus la découverte mais l'indexation.** *Pages → Indexed* : combien des 96 URL
  sont réellement dans l'index. C'est la seule mesure qui dira si le site existe pour Google.

## 22/10 (25) — redirection www vérifiée, et pourquoi on laisse `www` dans Search Console

**`https://www.dmoptiquesarl.com/` redirige bien vers `https://dmoptiquesarl.com/`.** Constaté par King
dans le navigateur. C'est le dernier maillon technique du déploiement : build vert, site servi, sitemap
découvert, adresse unique.

**L'avertissement Cloudflare était un faux positif**, comme le laissaient penser les IP identiques pour
les deux hôtes. La leçon retient un piège : l'option « Create a new proxied DNS record » proposée dans
cette boîte de dialogue **crée un doublon** au lieu de constater l'existant — elle aurait pu couper `www`.

**Question posée : faut-il retirer l'entrée `www` de Search Console ?** Réponse : **non, pas besoin.** Les
96 pages sont déjà découvertes deux fois, le `canonical` est en apex, et le 301 consolide. L'entrée est
inerte. Si elle passe un jour en erreur (« redirect »), c'est cosmétique et on n'y touche pas — la
supprimer ou la resoumettre n'apporterait rien.

**Le sujet SEO est donc clos côté technique.** Ce qui reste à mesurer n'est plus la découverte, mais
l'**indexation** : *Pages → Indexed* sur les URL apex. À lire dans quelques jours, pas maintenant.

## 22/10 (26) — la recherche qui manquait : la marque, la vente, Warby Parker

Deuxième vague de recherche, et elle a fait plus que compléter : elle a **donné un axe** à tout ce qu'on
avait produit ces trois semaines.

**Joanna Wiebe** (`YNJ18ggqwqM`) pose la distinction qui commande le reste : *célèbre* n'est pas
*intéressant*. McDonald's est célèbre ; In-N-Out est intéressant. Et un écart qui n'est pas crédible
n'est pas un écart — c'est une excentricité. Son test à deux phrases (« je suis différent parce que…
et ça compte pour mes gens parce que… ») élimine les idées décoratives.

**Warby Parker** n'a pas gagné avec un prix bas : ils ont **nommé un ennemi structurel** (les marges de
Luxottica), **supprimé la friction** (cinq montures essayées chez soi), et **changé la catégorie** — des
lunettes sont un accessoire qu'on porte toute la journée, pas un dispositif médical. On copie la posture,
pas le modèle : nous avons un cabinet à Ndobo Mayor et un numéro WhatsApp, pas 120 000 $ et un marché de
150 milliards.

**Ce qui en sort pour DM Optique** — et c'est la pièce qui manquait :

> **L'axe unique : la transparence avant la vente. On montre avant de vendre.**

Tout était déjà là : les 40 montures photographiées, la phrase « si vous voyez bien, ne venez pas »,
l'examen à des horaires dédiés. Ce n'était pas une collection de bons gestes — **c'était un
positionnement qui n'avait pas encore été nommé**. Écrit dans `brand/BRAND-STRATEGY-2026-10-22.md`.

**Décision de King sur le premier post** : option B, on ne publie pas la vidéo déjà tournée en premier —
on ouvre sur la règle **20/20/20**, sans visage, montée à partir des photos du dépôt
(`content/month1/w1/tiktok-01-v2-20-20-20.md`). Le mois sera **entièrement sans visage** : c'est un choix
assumé, documenté comme un coût (la recherche place les visages au premier rang), à réévaluer sur chiffres.

**Le risque, dit à voix haute** : la v1 est tournée, la v2 ne l'est pas. Si le montage n'est pas prêt pour
5h30, on publie la v1 et la v2 part le 27. Manquer la date pour une vidéo non montée serait le pire choix.

## 22/10 (27) — la V2 est montée : 23 s, sans visage, portique vert

**Livré** : `content/month1/w1/tiktok-01-v2.mp4` — 23,00 s, 1080×1920, 30 fps, H.264 + AAC, 4,3 Mo.
Moteur : `tools/record/make_dmoptic_tiktok.py` (reproductible, une commande). Plan écrit avant de
commencer : `MONTAGE-V2-ROADMAP.md`, avec son journal de montage en §7.

**Ce qui n'existait pas ce matin dans le sandbox** : ni ffmpeg, ni PIL, ni police, ni brotli. Quatre
paquets installés (`pillow`, `imageio-ffmpeg`, `numpy`, `fonttools`+`brotli`), polices du site converties
de `woff2` en `ttf` et **versionnées** (`assets/fonts/`), pour que le montage soit rejouable.

**Le portique a servi, et il a bloqué.** Première version : 5 fenêtres figées sur 11 — un diaporama.
Cause : des zooms de 5 % et un carton final immobile. Correction : amplitudes de 14 à 16 %, déplacement
en x **et** en y, carton final rendu à 1,22× puis **recadré en mouvement** (net et vivant à la fois).
Verdict final : **0 fenêtre figée**.

**Deux pièges de plus, à retenir :**

1. **`-shortest` coupe le carton final.** La voix faisait 21,26 s pour un montage de 23 s : la vidéo
   sortait à 21,2 s, sans le numéro WhatsApp. Correction : tempo doux (0,92) + `apad` + `-t 23`.
   **Règle ajoutée au moteur** : la durée du montage est forcée, jamais déduite de l'audio.
2. **Une photo de produit sur fond crème ne se pose pas sur un fond flou.** Ça donne deux zones grises
   mortes. Correction : **carte crème sur fond nuit** — le produit n'est pas retouché, c'est le cadre qui
   change.

**Visages** : King a tranché (22/10) — les visages **du personnel** sont autorisés. Les deux photos du
cabinet n'en contiennent aucun d'exploitable de toute façon (posters et mur de montures).

## 22/10 (28) — « where is post 1 ? » : les vidéos n'étaient ni sur GitHub ni sur le disque

Trois questions de King en une : *« je ne trouve pas ugc-03.mp4 sur github »*, *« où est le post 1 ?? »*,
et la décision de garder le sans-visage avec un tournage mensuel.

**Le diagnostic, et il est gênant.** Les deux vidéos étaient **absentes des deux endroits à la fois** :

1. **Pas sur GitHub** — le `.gitignore` du dépôt exclut `*.mp4` et `*.mp3` depuis le **23/09**, sur ta
   demande (« retire les vidéos précédentes, elles rendent le repo lourd inutilement »). Règle juste, mais
   je n'avais pas dit assez clairement qu'elle implique **invisibilité totale sur GitHub** : aucun `.mp4`
   livré n'apparaîtra jamais dans l'arborescence.
2. **Pas sur le disque non plus** — l'espace de travail a été remis à zéro (18ᵉ épisode du genre) ; comme
   les fichiers étaient **ignorés par git**, aucun `checkout` ne pouvait les ramener. `git ls-files` le
   confirme : seuls 7 vieux mp4 de `content/pipeline` sont suivis.

**Ce qui a été fait, dans l'ordre :**

1. **Récupération du dépôt** — `fetch` puis `reset --mixed origin/arena/2fffee3b-amk` + `checkout -- .`
   (jamais `--hard`), arbre propre, HEAD `e861057`.
2. **Remontage des deux vidéos**, voix comprises (`voice-00`, texte pris dans le `.srt` pour le post 1 et
   dans `ugc-03.md` pour le post 2) : `tiktok-01-v2.mp4` **23,00 s / 4,8 Mo**, `ugc-03.mp4`
   **22,30 s / 6,8 Mo**, **portique OK pour les deux**.
3. **Le correctif de fond** — en deux temps. D'abord la **release GitHub** : elle échoue,
   `uploads.github.com` étant **injoignable depuis l'espace de travail** (testé, code 000 ; `api.github.com`
   et `github.com` répondent, l'envoi de pièces jointes non). Ensuite, et c'est ce qui reste : **dépôt
   direct dans l'arborescence**, par **deux exceptions nommées** dans `.gitignore`, avec le commentaire qui
   explique et qui dit comment revenir en arrière. Coût assumé : **~11,6 Mo**. `VIDEOS.md` donne les chemins
   exacts, les durées, les portiques et les commandes de remontage.

**La leçon à garder** : un fichier ignoré n'est pas « rangé ailleurs », il est **hors de toute
sauvegarde**. Règle debout proposée : *tout livrable binaire déposé en release le jour même, son nom écrit
dans `VIDEOS.md`*. Si King préfère les `.mp4` dans l'arbre, une ligne de `.gitignore` suffit — mais c'est
sa décision, pas la mienne.

**Et la décision de production** : sans-visage conservé, budget mis sur **une demi-journée de tournage par
mois** (14h–18h, 4 blocs, 30–40 clips, 8 posts dont 4 à visage). Plan complet, liste de plans imprimable,
autorisation d'image et circuit rush → post : `content/tournage/PLAN-TOURNAGE-MENSUEL.md`. Aucun
abonnement d'avatar IA, aucune clé Veo achetée.

---

## 23/10/2026 — badge « source préférée sur Google » sur les 97 pages, et déploiement de test

**Ce qui a changé.** Un badge deeplink (`https://www.google.com/preferences/source?q=dmoptiquesarl.com`)
sous la description du pied de page, sur **les 97 pages** (FR + miroir `/en/` + fiches de montures).
Pose par l'outil unique `tools/site/add_social_footer.py` (constante `PREF_DOMAIN`), **idempotent** :
`--check` renvoie « 97 pages · 0 à corriger ». Bilingue par les `.fr-only` / `.en-only` existants.

**Pourquoi le deeplink et pas le bouton JavaScript de Google.** Le bouton officiel charge une iframe
`news.google.com` **à chaque vue de page** ; le site promet une page légère sur un téléphone en 3G. Le
deeplink n'ajoute ni script ni requête tierce. Détail et sources : `site/PREFERRED-SOURCES-2026-10-23.md`.

**Portes (§1b)** : `audit_html` 0 finding sur `index`, `en/index`, `montures/index`, `contact` ;
`audit_a11y --strict` 0 faute / 0 avertissement sur `index` et `en/index`.

**Déploiement de test (§1f③)** : projet `dm-optique-sarl` (`prj_vnTP9SW2lGh2rMqH15oU6S5NZvob`),
déploiement **`dpl_3DnweMavAxXaZAFgRFXp4ZafT9gA`**, commit **`3e32490`**, cible `production`,
état **READY / PROMOTED**, alias `https://dm-optique-sarl.vercel.app`. Piège reconfirmé : `git_source`
attend `repoId` **numérique en chaîne** (`"1370149389"`) ; un `repoId` au format `owner/repo` renvoie
400 « repository can't be found ».

**Non vérifié** : la présence du badge dans la page servie. L'extracteur de texte de `fetch_page`
**supprime le pied de page** (il ne montre pas non plus les liens Facebook/TikTok pourtant en ligne) :
la preuve visuelle reste une capture de King.


---

## 23/10/2026 — 65 photos de montures passées sur un set blanc

**Demande King** : « can you edit/modify the images of the frames in the repo so that they look as the
ones in the attached images ? » (visuels fournisseur : monture sur fond clair continu, cadrée large).

**Trois méthodes ont été essayées, dans cet ordre, et les deux premières ont été jetées après
contrôle image par image** — c'est le détail qui compte pour la suite :

1. **Gain de couleur** par canal pour amener le crème au blanc. Rejeté : il éclaircit aussi le
   produit. Mesuré sur f01 — le doré de la monture passait de `(236,194,117)` à `(255,223,160)`,
   un or devenu pâle. Un client qui commande sur cette photo ne reçoit pas cette couleur.
2. **Détourage** (seuil sur le fond, verres rendus transparents). Rejeté : 14 fichiers sur 65 ont des
   **charnières ressort presque de la couleur du fond** — e07 et e13 sortaient coupées en deux, e17
   sans ses branches —, et sur les montures **percées ou semi-cerclées** (f01, h01, h04) les verres
   *sont* la monture : les rendre transparents effaçait la moitié du produit.
3. **Substitution de couleur** — retenue. Le fond est remplacé pixel par pixel, la monture n'est pas
   touchée. La flèche du filigrane, détachée dans un coin, est effacée ; tout ce qui est dans le
   cadre de la paire reste.

**Ce qui est livré** (`tools/site/restyle_frames.py`) : fond crème → `(250,250,250)`, flèche du
filigrane retirée, recadrage sur la monture à marge constante, pose sur set blanc uni. 65 fichiers,
0 échec, 4,8 → 4,7 Mo, 1600 × 1200, noms inchangés, 0,8 s par image, réversible.

**Ce qui reste visible, et pourquoi** : la **carte d'appui bleutée** du fournisseur est toujours là,
sous la monture. Elle est dans la photo ; l'effacer proprement demande de découper la monture — ce
qu'on refuse, pour les raisons du point 2. Elle disparaîtra le jour où la série sera re-photographiée.

**La vraie réponse reste la re-photo** : table blanche, lumière diffuse, 10 minutes par série. Le
script rejouera alors la même présentation, avec cette fois un détourage possible.

## 23/10/2026 (suite) — le socle : les montures ne flottent plus

**Demande King** : « I see you have changed the background but that won't be quite enough to satisfy
the client, can you generate something (the case or a bench) on which the frames will stand? research
on github tools that can help you do it then install them ».

**Recherche GitHub d'abord** (API, par étoiles), puis essai : `rembg` (25 162 ★, MIT) installé dans un
venv et **écarté** — ses poids se téléchargent sur un hôte bloqué ici, et il est entraîné pour des
sujets opaques, alors que nos montures sont transparentes. Le détail et les deux autres candidats sont
dans `ops/TOOL-SCAN.md`. **Rien n'est donc installé** : le socle est dessiné par un script maison.

**Ce qui est généré** — `tools/site/frame_bench.py` : un **socle en acrylique**, dalle translucide vue
de face, arête claire sur le dessus, chants latéraux, ombre de contact, et le **reflet** de la monture
dans la matière. Pas d'étui : nous n'en avons photographié aucun, on ne montre pas un produit que le
cabinet ne vend pas. La monture, elle, n'est **jamais** redessinée : elle est détourée de sa photo.

**Trois garde-fous, dans l'ordre où ils ont servi** :

1. **charnières ressort** — récupérées par fermeture morphologique (un pixel clair *entouré* de monture
   en fait partie) : e07 et e13, coupées en deux au tour 66, sont entières ;
2. **papier bleu pâle** — la feuille bleutée du fournisseur laissait un ruban clair accroché aux
   charnières (e07, e13). Retiré par une règle de couleur (clair **et** froid, `b - r ≥ 5`) : l'acier et
   l'argent sont neutres, donc épargnés — f59, qui était la victime de la première tentative, reste
   intacte ;
3. **contrôle de pièces + repli** — si le détourage laisse des morceaux séparés, ou si la matière est
   transparente (e17, e27, f06, f25, f25-2, f26, f59-2), la photo n'est **pas** découpée : elle est
   affichée entière, fond ramené au blanc du set, posée sur le socle. Une monture entière sur un socle
   vaut mieux qu'une monture amputée sur un beau fond.

**Résultat** : 65 fichiers, 0 échec, **58 détourés + 7 en planche**, 1600 × 1200, 4,7 → 4,9 Mo, noms
inchangés, `QUALITY=82`, réversible (`git show 3810e3b~1:…`). `dmopticsarl.zip` repacké :
182 entrées, 4 706 Ko. Contrôle : `tools/qa/audit_images.py` — 0 faute sur femmes (24) et hommes (6).

**Ce qui reste imparfait, et il faut le dire au client** : sur f25 et f25-2, le bord de la carte
d'appui du fournisseur reste visible derrière le verre (on ne découpe pas, donc on ne l'efface pas) ;
sur h05 et h08, prises de trois quarts, la monture repose sur son point le plus bas, ce qui la fait
flotter d'un côté. **La vraie réponse reste la re-photo sur le socle** : dix minutes par série, et les
65 photos sortent alors sans détourage du tout.

## 23/10/2026 — la page d'accueil non indexée : un 403 à la dernière visite, et un panneau vide qui est normal

**Ce que la Search Console montre** (captures de King, 23/10) : `/examen-de-vue/` est indexée, avec
« Breadcrumbs : 1 valid item ». `/` ne l'est pas, avec « **Page is not indexed: Blocked due to access
forbidden (403)** », dernier crawl **20 oct. 2026 à 22:21:35**, crawlé comme **Googlebot smartphone**,
« Crawl allowed: Yes », « Page fetch: Failed ». Le **test en direct du 23/10 à 04:17** dit l'inverse :
« URL is available to Google… Page can be indexed ».

**Ce que le dépôt prouve, et qui innocente les fichiers** :

| Vérifié dans `hosting/previews/dmoptic/` | Résultat |
|---|---|
| `robots.txt` | `User-agent: * / Allow: /` — rien de bloqué, sitemap déclaré |
| `sitemap.xml` | **96 URL**, et `https://dmoptiquesarl.com/` en **première** ligne — la découverte n'a jamais manqué |
| `_headers` | sécurité seulement (nosniff, frame, referrer) — aucun `X-Robots-Tag`, aucun blocage |
| `index.html` | pas de `noindex`, canonical correcte, `@graph` avec l'entité `Optician` |

Un 403 n'est donc **pas produit par le site** : il vient de la couche qui le sert (Cloudflare). Il a
duré le temps d'un crawl, quatre jours avant la capture, et il a disparu — le test en direct le prouve.

**Ce qu'il faut faire, dans cet ordre** :

1. **Search Console → URL inspection → `/` → onglet « Google index » → REQUEST INDEXING** (pas le bouton
   du test en direct, qui ne demande rien à l'index). C'est ce qui remet la page dans la file.
2. Si le 403 revient dans 48–72 h : **Cloudflare → Security → Events**, filtrer sur `Path = /` et sur
   les ASN de Google, autour du 20/10 22:21. Chercher une règle WAF, un *rate limit* ou un
   « Under Attack Mode » activé pendant le déploiement. C'est le scénario le plus probable du blocage
   d'une **seule** URL racine alors que les sous-pages passaient.
3. Contrôle indépendant : `curl -A "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P)
   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible;
   Googlebot/2.1; +http://www.google.com/bot.html)" -sI https://dmoptiquesarl.com/` → attendre `200`.

**Pourquoi « Enhancements and experience » est vide sur l'accueil, et pourquoi c'est normal** : le
panneau ne liste que les **types d'items présents et validés** (fil d'Ariane, FAQ, produit…). L'accueil
déclare un `Optician` (LocalBusiness) : il n'y a **pas de fil d'Ariane** sur une racine — un
`BreadcrumbList` d'un seul élément n'est pas un fil d'Ariane. `/examen-de-vue/` en a un à deux niveaux
(Accueil → Examen de vue), d'où la ligne. Deux causes se cumulent ici : la page **n'a jamais été lue**
(403), donc rien n'a pu être validé ; et même une fois indexée, elle n'affichera pas de fil d'Ariane.
**Il n'y a rien à corriger sur la page pour ce panneau.** Si King veut quelque chose dans cette section
sur l'accueil, l'item à ajouter est **`WebSite` + `Organization` avec `logo` et `sameAs`** (les profils
sociaux déjà en pied de page) : c'est ce qui produit les améliorations « logo » et « identité du site ».

## 23/10/2026 — l'audit extérieur : ce qu'il a trouvé, ce que nos portiques ne voyaient pas

Le rapport est archivé tel quel : `clients/dm-optic/audits/AUDIT-EXTERNE-2026-10-23.md` (Chrome headless
1366 et 390 px, axe-core, comparaison au domaine). **Deux P1**, et nos cinq portiques disaient tous
« 0 faute » le même jour. Les deux étaient vrais : aucun des cinq ne regardait une feuille de style, des
en-têtes HTTP ou un fichier absent.

**Vérifié dans le dépôt, constat par constat** (pas de reprise de l'audit sur parole) :

| # | Constat | Vérification locale | État |
|---|---|---|---|
| 1 | Aucune nav sous 980 px | `.nav{display:none}` + `@media (min-width:980px)`, **0 bouton `aria-expanded`** sur 90 pages | **confirmé** |
| 2 | Cache `max-age=0` | `_headers` ne porte **aucune** règle de cache ; 491 images et 7 polices référencées | **confirmé** |
| 3 | Pas de favicon | aucun fichier, aucune balise `<link rel="icon">` sur 97 pages | **confirmé** |
| 4 | Double barre dans le JSON-LD | 4 occurrences, 2 par accueil FR/EN (`//cabinet-hero-1080.webp`, `//dm-logo.webp`) | **confirmé** |
| 5 | HSTS absent | `_headers` = nosniff, referrer, frame, permissions | **confirmé** |
| 6 | `og:image` en WebP | 80 pages sur 97 ; l'aperçu WhatsApp se teste en envoyant un lien, pas ici | à tester |
| 7 | `llms.txt` FR seulement | 49 URL contre 96 au sitemap, **47 anglaises absentes** | **confirmé** |
| 8 | Pas de `Product` | fiches montures : `BreadcrumbList` seul | **confirmé** |
| 9 | Tirets cadratins | 685 — / 654 – | à trancher (voix DM) |
| 10 | Pas de CSP | — | **confirmé** |
| 11 | Fondateur et horaires | à confronter à la source (ONOC), pas au dépôt | à vérifier |
| 12 | Images de partage partagées | 41 images pour 97 pages | **confirmé** |

**Une erreur dans l'audit extérieur**, relevée et corrigée de notre côté : la règle de cache qu'il
propose (`/*.webp`) **ne peut pas fonctionner** sur Cloudflare Pages, où le splat ne vaut qu'en fin de
motif. Appliquée telle quelle, elle aurait laissé le défaut en place. Sur ce site les images vivent dans
`/montures/`, mêlées aux pages : une règle par dossier cacherait aussi du HTML. La voie correcte est une
**Cache Rule** du tableau de bord (extension `webp|jpg|png|woff2`, 7 jours pour les images, 1 an
`immutable` pour les polices), et le HTML reste à `max-age=0, must-revalidate`.

**Ce qui a changé dans nos outils** : `tools/qa/audit_delivery.py` (+ son témoin qui casse douze choses
une par une), branché dans `PRE-FLIGHT.md` §1b. Leçons : `tools/qa/AUDIT-LESSONS-2026-10-23.md`.
**Les défauts du site ne sont pas corrigés dans ce tour** : les P1 demandent du design (bouton de menu,
focus, Échap) et un réglage côté Cloudflare, pas un `sed`. Proposé à King.

---

## 23/10/2026 (soir) — les deux P1 corrigés, et une correction de nos propres conclusions

**Deux erreurs de ce matin, corrigées ici parce qu'elles étaient écrites noir sur blanc** :

1. Le paragraphe ci-dessus présente la **Cache Rule** comme « la voie correcte ». C'est faux pour cet
   hébergement : le site est servi par un **Worker** (`wrangler.toml`, `[assets]`), et la doc Cloudflare
   dit que *« Cache Rules, Cache Page Rules, Page Rules … have no effect on a Worker's cache »*
   (<https://developers.cloudflare.com/workers/cache/>). La bonne porte est `_headers`, que Workers lit
   (<https://developers.cloudflare.com/workers/static-assets/headers/>) et qui fixe le défaut
   `max-age=0`. Détail et règle de secours : `launch/CACHE-2026-10-23.md`.
2. Le portique condamnait `/*.webp` **partout**. Vrai sur Pages (splat en fin seulement), faux sur
   Workers, dont la doc donne justement `/*.jpg` en exemple. `audit_delivery.py` détecte maintenant
   `wrangler.toml` (`uses_workers_assets`) et juge le motif selon l'hôte ; le fichier livré nomme
   quand même les onze fichiers racine, pour rester vrai si le site repasse un jour sur Pages.

**Livré (commit `b68239e`, poussé sur `arena/29c013f1-amk`)** :

| P1 / P2 de l'audit extérieur | Correction | Preuve |
|---|---|---|
| 1 · pas de nav sous 980 px | `<details class="mnav">` + `<summary>` 44 px sur **97 pages**, liens recopiés de la nav (les bascules FR/EN continuent), Échap/clic dehors/`resize` en confort, **rien n'exige JS** | `audit_delivery.py` D1 : 0 page |
| 2 · cache `max-age=0` | `_headers` : polices + logo 1 an `immutable`, montures et images racine 7 j, HTML laissé à `must-revalidate` | `--strict` rc=0 |
| 3 · pas de favicon | `favicon.ico` (16/32/48), `favicon-32.png`, `favicon-192.png`, `apple-touch-icon.png` tirés de `dm-logo.webp` ; 4 `<link>` sur 97 pages | 4 fichiers + 97 pages |
| 4 · `//` dans le JSON-LD | 4 occurrences supprimées (2 accueils) | D4 : 0 |
| 5 · HSTS absent | `Strict-Transport-Security: max-age=31536000; includeSubDomains` | D8 : 0 |
| 6 · `og:image` WebP | **65 cartes JPEG 1200 × 630** (`make_dm_og.py`, photo réelle recadrée) + `og:image:type` | D6 : 0 page en WebP |
| 7 · `llms.txt` FR seul | bloc anglais régénéré depuis les fichiers (`build_dm_llms.py`) : 47 URL | D5 : 0 |
| 8 · pas de `Product` | `Product` ajouté aux **80 fiches**, **sans prix, sans offre, sans marque inventée** (`sku`, `name`, `image`, `description`) | D7 : 0 |
| 10 · pas de CSP | politique conservatrice, aucune ressource hors `self` (vérifié : les 1 102 liens externes sont des `<a>`, aucun script distant) | D8 : 0 |

**Résultat de la porte** : `0 P1 · 0 P2 · 1 P3` (P3 = aperçus partagés entre pages de même famille),
`--strict` **rc=0**. `tools/ops/gate-dm.sh` porte désormais l'étape 4 : `audit_delivery.py --strict`
avant toute livraison client.

**Ce qui n'est toujours pas en ligne** : rien de tout cela. La prod Cloudflare est restée sur le
déploiement du `25e2289`/`3e314fd` parce que Workers Builds publie la branche **`arena/2fffee3b-amk`**,
celle d'une conversation terminée. Le correctif tient en un champ à changer (Settings → Build →
Branch) ou en un `npx wrangler deploy` depuis la racine du dépôt — voir `launch/CACHE-2026-10-23.md` §6.

### 23/10 (nuit) — le déploiement a eu lieu, et il est prouvé

Changer la branche de production **ne déclenche rien** : c'est l'**envoi** qui déclenche. Le premier
envoi après le réglage de King (`e30dadb`) a été publié à 04:48 UTC — trois minutes après sa capture
d'écran, d'où l'impression que « rien ne s'est passé ». Preuve côté public : `llms.txt` sert la section
`## English pages`, écrite dans le même commit que le menu mobile.

Les builds suivants échouent en une seconde sans produire de version : commande de déploiement
`npx wrangler deploy`, qui attend une confirmation avant d'installer wrangler. À remplacer par
`npx --yes wrangler@4.152.0 deploy` — détail et relevé minute par minute dans
`launch/DEPLOIEMENT-CLOUDFLARE-2026-10-22.md` §6.

## 24/10/2026 — les masters vidéo sortent du dépôt

Les cinq vidéos du mois 1 (`tiktok-01-v2`, `ugc-03`, `spot-02`, `spot-03`, `etapes-01`) et leurs
couvertures sont publiées, présentes sur TikTok et Facebook, et King en garde les fichiers sur son
téléphone. Elles sortent du suivi git à sa demande. Ce qui reste dans le dossier : storyboards,
sous-titres, plans de publication et commandes de remontage. Rien n'est détruit — l'historique git
les porte encore — et le `.gitignore` explique les deux décisions successives (22/10 puis 24/10),
pour que la question ne se rouvre pas une troisième fois sans le contexte.
