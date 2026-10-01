# Brief site — DM OPTIQUE SARL

> **Statut : brief. Rien n'est publié, rien n'est redéployé, tant que l'acompte n'est pas encaissé.**
> Écrit le **01/10/2026**. Ne pas produire avant approbation du plan de contenu (décision de King).
>
> Ce brief **s'ajoute** à un site déjà construit : voir §2 — il y a une **décision d'architecture à
> trancher** avant toute production.

---

## 1 · Objectif du site

**Une seule question à résoudre pour le visiteur : « puis-je venir, et comment ? »**

Ce n'est pas une vitrine de marque. C'est un **comptoir** : quelqu'un cherche un opticien à Douala sur
son téléphone, en plein jour, probablement en 3G, et doit pouvoir **écrire sur WhatsApp en deux
gestes**.

Trois objectifs, dans cet ordre :

1. **Être trouvable** — nom + ville + métier, dès le premier écran et dans la donnée structurée.
2. **Rassurer** — un opticien inscrit, un titulaire nommé. La preuve ne vend pas le travail au patron :
   elle rassure le patient.
3. **Faire écrire** — chaque chemin mène à un WhatsApp pré-rempli.

**Hors périmètre** : boutique en ligne, paiement, prise de rendez-vous en ligne (le cabinet n'a pas
d'agenda), blog, capture d'e-mail.

---

## 2 · ⚠️ Décision d'architecture à trancher

**Ce qui existe déjà** : un site **une seule page** (v2.2, orienté patient), construit, testé
(**38/38** assertions), **non publié**, `noindex`.

| Chemin | Rôle |
|---|---|
| `demos/concept-dmoptic-v1.html` | l'aperçu, un seul fichier (166 Ko) |
| `demos/dmoptic-v1.tpl.html` | gabarit — source unique du texte |
| `demos/build_dmoptic.py` | constructeur (+ vignette du lien) |
| `hosting/previews/dmoptic/` | dossier à déployer (`index.html` + `og.jpg`) |
| `tools/qa/test_dmoptic_page.mjs` | 38 assertions de comportement |

Ses sections actuelles : premier écran · la preuve (« un opticien inscrit, un titulaire nommé ») ·
les six actes avec « À apporter » · le déroulé en trois étapes · cinq questions fréquentes · contact.

**Ce que demande ce brief** : six sections distinctes — **Accueil / Nos montures / Nos verres / Examen
de vue / À propos / Contact**.

**Le conflit.** Ce n'est pas la même architecture. Trois options, **à trancher par King** :

| Option | Ce que c'est | Pour | Contre |
|---|---|---|---|
| **A — Une page, six sections ancrées** | Garder le fichier unique, transformer les six entrées en **ancres** de navigation | Zéro reconstruction. La QA existante tient. Charge minimale en 3G. Un seul fichier à déployer | « Nos montures » et « Nos verres » n'ont pas de profondeur propre |
| **B — Six pages** | Architecture multi-pages réelle | Chaque service a sa page, son titre, son schéma — meilleur pour la recherche | **Reconstruction quasi complète.** La QA 38/38 est à refaire. Six pages à tenir à jour en **deux langues** = douze écrans. Coût de maintenance réel, dans un abonnement à 30 000 FCFA/mois |
| **C — Hybride** | Une page + une page « Nos montures » dédiée (la vitrine est le différenciateur d'un opticien indépendant) | Concentre l'effort là où il rapporte | Deux gabarits à maintenir |

**Recommandation : A, avec C en réserve.** Raison : la recherche du 24/09 a conclu que **la section
montures est le différenciateur d'un opticien indépendant** (`inspiration.md` § « Second passage »).
Mais nous n'avons **aucune photo réelle de monture** aujourd'hui — trois illustrations. Construire six
pages avant d'avoir les photos, c'est construire du vide. **Ordre proposé : A maintenant, basculer la
vitrine en page dédiée (C) dès que les photos réelles existent.**

⚠️ **Écart d'URL à corriger avant tout redéploiement.** `build-notes.md` et `a-completer.md` citent
`https://dmoptic.vercel.app` ; le CRM cite `https://dmoptic-2.vercel.app`. La vignette du lien
(`og:url`, `og:image`) ne peut pas être devinée : il faut recoller la bonne adresse avec
`build_dmoptic.py --url`, puis redéployer **le dossier entier**.

---

## 3 · Structure — les six sections

| # | Section | Ce qu'elle doit faire | Ce qu'elle ne fait pas |
|---|---|---|---|
| 1 | **Accueil** | « DM OPTIC, votre opticien à Douala » · surtitre porteur du mot-clé (« Opticien à Douala · inscrit à l'Ordre depuis 2016 ») · **deux gestes** : WhatsApp, appeler · trois faits (Où · Sur WhatsApp · Inscrit depuis 2016) | Un discours de marque. Une promesse. Un prix |
| 2 | **Nos montures** | La **vitrine**, par familles (vue · soleil · enfants). Une photo, un conseil par famille. **Un WhatsApp pré-rempli par famille** — « Demander si c'est en boutique » | Nommer une marque qu'on n'a pas. Afficher un prix. Une grille e-commerce |
| 3 | **Nos verres** | Expliquer **ce qu'on apporte** et **ce qui se passe** : ordonnance, choix du verre, montage, ajustement. Dire « protège vos yeux », jamais « corrige » | Promettre un traitement, un délai, une performance optique |
| 4 | **Examen de vue** | Le déroulé réel, la durée, **ce qu'il faut apporter**, les **horaires de consultation (8h30–13h30)**. Un WhatsApp pré-rempli « Je souhaite un examen de vue » | Un tarif. Une allégation médicale. Un rendez-vous en ligne |
| 5 | **À propos** | Un opticien inscrit, un **titulaire nommé** (M. Domche Noumbi), l'inscription depuis 2016, la mention presse de mars 2023 **avec sa source** | Un portrait inventé. Une histoire de marque fabriquée. Un classement |
| 6 | **Contact** | Les deux gestes (WhatsApp, appeler) + deux utilitaires discrets : **copier le numéro**, **enregistrer la fiche `.vcf`**. L'adresse et **un repère** | Un formulaire. Une carte si l'adresse n'est pas confirmée |

**Le principe qui tient l'ensemble.** Chaque section se termine par **un geste**, pas par un paragraphe.
Et le geste est toujours le même : écrire sur WhatsApp.

---

## 4 · Bilingue FR | EN

| Règle | Détail |
|---|---|
| **FR par défaut** | Le français est la langue servie à l'ouverture. Aucune page EN seule |
| **EN en bascule complète** | La bascule change **tout** l'écran, pas un bloc. Déjà le comportement de la v2.2 |
| **Pas de pavés de langue** | Pas de texte en deux langues empilé : ça double la longueur et noie le message |
| **Un seul gabarit** | Les deux langues sortent du **même** gabarit — jamais deux fichiers à maintenir séparément |
| **Le WhatsApp pré-rempli suit la langue** | Un visiteur EN écrit un message pré-rempli **en anglais** ; le cabinet répond dans la langue du patient |
| **La donnée structurée reste en FR** | Le schéma (`Optician`, `PostalAddress`, `FAQPage`) porte le français ; c'est la langue de l'entité |

⚠️ **Coût réel à signaler.** Le bilingue **double** le travail d'écriture et de relecture, dans un
abonnement à 30 000 FCFA/mois qui comprend **2 publications par semaine et la maintenance**. Chaque
nouvelle section = deux écrans à écrire et à relire. C'est un argument de plus pour l'option A (§2).

---

## 5 · WhatsApp-first — la règle d'or

**Chaque CTA mène à WhatsApp. Aucun CTA mort.**

| Exigence | Détail technique |
|---|---|
| **Un `wa.me` pré-rempli par action** | Chaque bouton porte son propre message : « Bonjour, je souhaite un examen de vue », « Bonjour, cette monture est-elle en boutique ? » |
| **Un message pré-rempli par famille de montures** | C'est le motif « WhatsApp-first » retenu (`website/inspiration.md`) : le visiteur arrive avec **sa** question déjà écrite |
| **Encodage identique statique / dynamique** | Le texte statique doit être encodé **exactement** comme le fait le JavaScript — c'est déjà une assertion du test (38/38) |
| **Barre d'action fixe en bas d'écran sur téléphone** | Le geste reste atteignable au défilement |
| **Numéro** | **656 122 239** (+237) — vérifié |
| **Jamais** | Un formulaire de contact, une capture d'e-mail, un `mailto:` en CTA principal |

**Pourquoi c'est le bon canal ici, et pas seulement une règle.** À Bonabéri, on écrit sur WhatsApp ; on
ne remplit pas de formulaire (`research/market-analysis.md` §2). Et c'est le **seul** canal mesurable :
on peut compter les conversations, pas les intentions.

---

## 6 · Règles de contenu

| # | Règle | Application |
|---|---|---|
| 1 | **Aucune allégation médicale** | « protège vos yeux » ✅ · « soigne / corrige / guérit » ⛔ |
| 2 | **Aucun témoignage, classement ou résultat inventé** | Zéro avis. Zéro étoile. Zéro « meilleur opticien de… ». Zéro nombre de patients |
| 3 | **Jamais nommer un concurrent** | Ni en bien ni en mal. L'angle ONOC se dit **sur soi** |
| 4 | **Aucune remise** | On échange du périmètre ou du calendrier, jamais du prix |
| 5 | **Rien d'inventé n'entre sur la page** | Adresse, horaire, prix, marque, assurance, photo : **confirmé ou absent**. Les champs manquants sont assumés, pas comblés |
| 6 | **Le prix ne s'affiche pas** | « Combien coûte une paire ? » est une **question de patient** dont la réponse explique ce qui fait le prix — pas un tarif |
| 7 | **Aucun visage fabriqué** | Pas de portrait généré de M. Domche Noumbi. Pas de patient inventé |

**La phrase qui résume la règle 5** (déjà sur la page) :

> « Une page de santé qui invente une adresse ou un horaire coûte un patient, puis la confiance. »

---

## 7 · Direction visuelle — et un conflit à trancher

**Ce qui est déjà décidé** (24/09, direction « **LA CARTE** » retenue sur trois explorées) :

| Élément | Valeur |
|---|---|
| Archétype | La **carte d'identité** : l'inscription réelle du cabinet mise en page comme une pièce officielle |
| Palette | Papier froid + **marine profond** (`#1A3F86`, `#2A5CB8`, `#4E7BD8`) + **un seul accent braise** (`#E0703A`) |
| Typographie | **Schibsted Grotesk** + **IBM Plex Sans** ; **IBM Plex Mono** sur les champs de registre |
| Images | **Aucun visage.** Deux natures mortes d'instruments. Jamais de texte sur la photo |
| Ton | Sobre, précis, chaleureux — un instrument, pas une publicité |
| Mouvement | **Un** moment d'entrée + révélations au défilement. Quatre moments, pas un de plus. Coupé par `prefers-reduced-motion` |
| Mode sombre | **Écarté** — un patient lit cette page dehors, en plein jour |

### ⚠️ Conflit avec la liste « à éviter »

La liste d'évitement du 01/10 interdit le **« cliché médical bleu et blanc »**. Or la palette retenue
est **papier froid + marine profond** — littéralement du bleu sur blanc.

**Ce n'est pas forcément une contradiction, mais il faut le trancher explicitement.** Ce qui sépare un
cliché médical d'une page précise, ce n'est pas la teinte : c'est **l'archétype** (une carte d'identité
officielle ≠ une clinique), **l'absence de visages souriants**, **la typographie** (du mono sur des
champs de registre ≠ une sans-serif générique), et **l'accent unique** utilisé une seule fois.

**Trois issues possibles :**

| Issue | Effet |
|---|---|
| **1 — Assumer le marine** | La direction « LA CARTE » est déjà construite, testée, et son archétype n'est pas médical. On documente pourquoi ce n'est pas le cliché |
| **2 — Réchauffer** | Papier ivoire/sable au lieu du papier froid, marine conservé. S'éloigne du bleu-blanc clinique, garde la sobriété |
| **3 — Changer d'accent** | Remplacer la braise par un accent non médical (vert profond, ocre). Attention : le **Cristallin** occupe déjà le registre « papier froid, étiquettes mono » — ne pas faire un reskin |

**Recommandation : issue 2.** Un papier réchauffé coûte une variable CSS, sort visuellement du
bleu-blanc clinique, et ne jette pas un travail testé 38/38. À confirmer par King — **c'est son œil,
sur un téléphone, qui tranche**, pas ce document.

---

## 8 · Entrées manquantes (bloquantes pour la production)

Reprises de `clients/dm-optic/a-completer.md`. **Aucune ne peut être inventée.**

| # | Manquant | Bloque |
|---|---|---|
| 1 | **Les jours d'ouverture** (les heures sont connues) | La section Examen de vue et le pied de page n'affirment **aucun** jour |
| 2 | **Un repère physique** (« en face de… », « à côté de… ») | La section Contact. À Bonabéri, on arrive en taxi |
| 3 | **3–4 photos du cabinet** (téléphone, lumière du jour) | Les photos d'illustration de la page |
| 4 | **6–8 photos de montures** par famille | **La vitrine entière** — et les carrousels du mois 1 |
| 5 | **Moyens de paiement** (espèces, MTN MoMo, Orange Money) | Évite au patient de venir sans pouvoir payer |
| 6 | **Assurances / mutuelles** | Décide le patient assuré |
| 7 | **Marques de montures vendues** | La vitrine ne nomme **aucune** marque aujourd'hui |
| 8 | **Validation des six actes** | La page liste six services **types**, signalés comme tels. Un cabinet ne fait pas tout |
| 9 | **Une phrase de lui**, ses mots | Vaut mieux que dix citations inventées |
| 10 | **NIU + adresse fiscale** | La **proforma** — donc l'acompte, donc tout |

→ Questions prêtes à poser : **`clients/dm-optic/onboarding/intake-questionnaire.md`**.

---

## 9 · Contraintes techniques

| Contrainte | Détail |
|---|---|
| **Un seul fichier** | Pas de framework, pas de build côté client, pas de React/Tailwind. HTML/CSS/JS vanilla |
| **3G** | Aucune vidéo de fond, aucun canvas 3D, aucun shader. Les images sont compressées |
| **`noindex` jusqu'au lancement** | ⚠️ **Vérifier que c'est toujours le cas** sur tout redéploiement — la règle « rien de public avant l'acompte » en dépend |
| **Mouvement** | `transform` uniquement (aucun `filter`, aucun repaint) · coupé par `prefers-reduced-motion` · jamais allumé sans JavaScript · la page reste lisible si le script plante |
| **Accessibilité** | `audit_a11y.py --strict` : **0 faute A/AA**. Contraste ≥ 5:1 sur le corps de texte |
| **Donnée structurée** | `Optician` · `PostalAddress` · `ContactPoint` · `Person` · `PropertyValue` · `FAQPage` (les cinq questions **mot pour mot** celles de la page) |
| **Le domaine sera à son nom** | Jamais sur un domaine à nous. `dmoptique.cm` / `dmoptic.cm` sont **libres** — à réserver **au nom du client** |
| **Portique** | *« Not verified on a phone = not sent. »* Aucune capture d'écran ne remplace l'œil de King sur un téléphone, en plein jour |

**Note d'outillage.** `build-notes.md` indique « le bac n'a **pas de navigateur** ». **C'est dépassé** :
Playwright est installé et les 14 fichiers de test passent (voir `tools/qa/VERIFICATION-2026-10-01.md`).
Les captures d'écran sont désormais possibles — **mais le portique du téléphone reste** : une capture
dans un bac n'est pas une lecture en plein jour à Bonabéri.
