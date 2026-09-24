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
