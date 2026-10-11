# Inspiration site — DM OPTIQUE SARL

> **Objet : ce qu'on vole, ce qu'on refuse, et ce qui ne se transpose pas.** Chaque référence est
> réduite à **un** motif transposable, avec sa **provenance** et son **verdict**.
>
> **Deux apports, fusionnés ici :**
> · **01/10/2026** — la compilation de recherche de King (Parties 1 à 3), organisée **par ce qu'on
> vole** et non par site d'origine. C'est la matière principale de ce fichier.
> · **01/10/2026, plus tôt** — la synthèse de six références déjà consignée.
>
> Un **troisième** fichier existe et répond à une autre question : `clients/dm-optic/inspiration.md`
> (24/09) traite du **style** — couleur, typographie, mouvement, composants. Celui-ci traite de
> **l'offre et de l'architecture**. Les deux sont conservés, volontairement séparés.
>
> ⛔ **Rien n'est produit avant approbation du plan de contenu.**

---

## Partie 1 · Ce que la recherche dit de la catégorie

Trois conclusions convergentes, toutes sources confondues (littérature design optique **et** médical).

### 1.1 · L'optique est à l'intersection du clinique et du commerce

**Le constat.** Un dermatologue n'a pas besoin d'une galerie de montures. Un pédiatre ne vend pas de
lunettes de soleil. Un opticien doit faire **les deux** : gagner la confiance médicale **et** montrer
du produit.

**Pourquoi c'est l'insight structurant.** Ce n'est pas une question de style, c'est une question
d'**architecture** : il faut des **pages de service** et des **pages de catalogue**, et elles doivent
cohabiter sans que la navigation devienne illisible. C'est exactement le problème que Muffin Group
nomme (§2.6).

**Conséquence pour DM OPTIQUE.** ⚠️ **Ceci fait bouger ma recommandation d'architecture du 01/10.**
J'avais recommandé « une seule page maintenant, la vitrine en page dédiée plus tard ». La recherche
dit que la **destination** est bien une architecture à deux jambes (soins · produit). Ce qui ne change
pas, c'est le **séquencement** : une page catalogue sans **aucune photo réelle de monture** est une
pièce vide.

**La bonne décomposition** — et c'est la nuance qui compte :

| Ce qui coûte | Ce que c'est | Quand |
|---|---|---|
| **L'architecture de l'information** (navigation en trois parties, ancres) | Une décision de structure — **peu coûteuse**, et c'est elle qui empêche l'encombrement | **Maintenant** |
| **La découpe en pages** (une page par service, une page catalogue) | Six pages × **deux langues** = douze écrans à écrire, relire et maintenir, dans un abonnement à 30 000 FCFA/mois | **Quand les photos existent** |

→ **Adopter la navigation à trois parties dès maintenant, découper en pages à la réception des
photos.** L'architecture est bon marché ; les pages sont chères. Détail dans `brief.md` §2.

### 1.2 · Trois secondes : la fenêtre de décision

**Le constat.** La plupart des sites d'optique se ressemblent : fond bleu, photo générique de quelqu'un
qui porte des lunettes, numéro de téléphone enterré. Les patients sortent. Ceux qui fonctionnent
**installent la confiance vite**, **mènent avec des images fortes du travail réel**, et **pointent vers
une seule action**.

**Conséquence.** Trois exigences pour le premier écran, toutes déjà partiellement tenues par la v2.2 :

1. **Nom + ville + métier** immédiatement — « DM OPTIC, votre opticien à Douala ».
2. **Une preuve, pas une promesse** — l'inscription à l'ONOC.
3. **Une action, pas trois** — le WhatsApp. La v2.2 a déjà réduit de quatre actions à deux.

⚠️ **Point de vigilance sur « images fortes du travail réel ».** Nous n'avons **aucune photo réelle**.
Les deux images actuelles sont des illustrations générées, légendées comme telles. **C'est le point où
la recherche et nos moyens divergent le plus** — et c'est pourquoi les photos sont au portique
(`pre-launch-checklist.md` item 7).

### 1.3 · Le WhatsApp-first est déjà la norme en Afrique de l'Ouest et de l'Est

**Le constat.** Plusieurs sources sur les marchés **sénégalais, nigérian et kényan** décrivent la même
structure : le **mode catalogue** pose un bouton **« Enquire »** sur **chaque produit**, qui ouvre
WhatsApp ; le CTA WhatsApp est **répété à plusieurs points de défilement**. C'est le standard du
commerce mobile-first africain.

**Conséquence.** Ce n'est plus une intuition, c'est un **motif éprouvé** — et c'est déjà la règle du
dossier. Le **raffinement** apporté par la recherche :

> **Chaque fiche produit porte son propre bouton WhatsApp, avec un message pré-rempli nommant cette
> monture précise.** « Bonjour, je suis intéressé par la monture **[nom]** ».

**C'est ce qui transforme la consultation en demande.** Un « contactez-nous » générique ne convertit
pas ; une question déjà écrite, si.

---

## Partie 2 · Les sept références

### 2.1 · Focal — **la correspondance la plus proche**

**Provenance :** Hatchable.

**Ce qu'il fait.** Fond blanc, typographie à l'encre, **un seul teal profond**, et **une échelle de vue
géante qui se réduit** comme signature du site — « personne ne la dépasse sans la voir ». L'examen est
**itemisé en cinq étapes en langage simple**, les **prix sont énoncés** et non cachés, la prise de
rendez-vous est un **bouton SMS pré-rempli**.

| Motif | Verdict | Transposition |
|---|---|---|
| **La signature « échelle de vue »** | ✅ **Prendre** | Un seul moment visuel indiscutablement optique. **Et c'est faisable tout de suite** — voir encadré ci-dessous |
| **L'examen itemisé (5 étapes)** | ✅ **Prendre** | « Voici ce que comprend un examen de vue chez DM Optique ». Répond à la question que tout nouveau patient n'ose pas poser : **« est-ce qu'on va m'expédier ? »** |
| **Les prix énoncés** | ⚠️ **Décision à trancher** | Voir §3.3 — ce n'est pas interdit, mais ça exige des tarifs **confirmés** |
| **La prise de rendez-vous par SMS** | ✅ **Prendre — déjà notre standard** | Un bouton WhatsApp pré-rempli, le numéro partout où il doit être. **Aucun portail, aucun widget, aucune connexion.** Focal prouve que ça marche en optique |
| **La liste d'assurances américaine** (VSP, EyeMed) | ⛔ **Ne pas transposer** | Remplacer par « Nous acceptons les mutuelles suivantes » **si** le cabinet en prend — sinon **omettre**. Question 4.4 du questionnaire |

> **💡 L'échelle de vue ne demande aucune photographie.** C'est de la typographie et du SVG.
> **Conséquence de planification importante** : c'est la **seule signature visuelle produisible dans la
> fenêtre où les photos manquent** — donc avant le lancement, et pour la semaine 1 du plan de contenu.
> C'est le meilleur candidat pour remplacer l'anneau de verre actuel (`.lensring`) si King tranche en
> sa faveur.

> **⚠️ Note bilingue réelle.** L'échelle de vue **française n'est pas identique** à l'anglaise. Le
> visuel fonctionne dans les deux cas, mais **le contenu des lignes diffère**. À traiter comme deux
> jeux, pas un — c'est un cas concret où le bilingue n'est pas une simple traduction.

---

### 2.2 · Warby Parker — **le quiz comme entrée à faible engagement**

**Provenance :** exemples d'optométristes Zarla.

**Ce qu'il fait.** L'accueil mène avec **une seule monture** magnifiquement éclairée, **deux entrées à
faible engagement** (« Start with a quiz » · « Shop eyeglasses »), et une **barre de rassurance** qui
pré-répond à l'ajustement, aux retours et à l'assurance. Le quiz de style **lève la paralysie** du choix
de monture en ligne.

| Motif | Verdict | Transposition |
|---|---|---|
| **Le quiz** | ✅ **Prendre, adapté** | **Pas de quiz numérique** — un **flux WhatsApp** : *« Répondez à 3 questions, on vous envoie 5 montures qui vous correspondent. »* Faible engagement, conversion élevée |
| **La barre de rassurance** | ✅ **Prendre** | Une bande qui pré-répond aux trois inquiétudes réelles : **l'ajustement**, **l'ordonnance**, **le paiement**. C'est peu coûteux et ça répond avant qu'on demande |
| **Le panier e-commerce** | ⛔ **Ne pas transposer** | DM OPTIQUE est une boutique locale : la conversion est **un message WhatsApp ou une visite**, pas un panier |

> ⚠️ **La condition que la recherche pose elle-même.** *« Le quiz ne fonctionne que si l'inventaire
> suffit à matcher. Confirmer la profondeur d'inventaire avec le client lors de la visite. »*
>
> **C'est un risque réel et il était absent de mes documents.** Promettre « 5 montures qui vous
> correspondent » avec trois familles en stock, c'est une promesse qu'on ne peut pas tenir.
> → **Question ajoutée au questionnaire** (§5.7 — profondeur d'inventaire). **Ne pas écrire le quiz
> avant d'avoir la réponse.**

---

### 2.3 · Moscot — **le nommage propriétaire des montures**

**Provenance :** Zarla.

**Ce qu'il fait.** Donne à **chaque monture un nom propriétaire distinctif** — *Plotz, Shtarker,
Billik, Utz* — qui rend le catalogue **appropriable** et mémorable, et transforme les lunettes en
**continuité culturelle**.

**Verdict : ✅ c'est l'idée la plus transposable de toute la recherche.**

**Le problème qu'elle résout, exactement.** Aujourd'hui, les montures de DM OPTIQUE se décrivent en
termes de **marchandise** : « ronde écaille », « acétate noir ». Descriptions que n'importe quel
concurrent peut reprendre.

**La transposition proposée par King — et elle est meilleure que la mienne :**

> Nommer d'après **des villes camerounaises, des figures locales, des noms de famille** — quelque chose
> qui a du sens. Le client ne demande plus « la marron » : il demande **« la Bonabéri »** ou
> **« la Sanaga »**.

**Pourquoi c'est fort, en quatre points :**

1. **Ça coûte 0 FCFA.**
2. **Aucun concurrent ne peut le copier** — le vocabulaire est à lui.
3. **C'est du contenu inépuisable** : chaque nom est une publication, chaque publication une histoire.
4. **Ça remplace ce qu'on n'a pas.** Nous n'avons **aucune marque** à nommer
   (`research/domche-noumbi.md` §6). Le nommage substitue un **vocabulaire possédé** à un
   **portefeuille de marques absent**.

**⚠️ Les trois conditions, à ne pas sauter :**

| Condition | Pourquoi |
|---|---|
| **Les noms viennent du client ou de ses montures réelles** | On n'invente pas un catalogue. Un nom posé sur une monture qu'on n'a pas vue est une invention |
| **Vérifier le sens des noms choisis** | Un nom de figure locale ou de famille peut porter une histoire sensible. **C'est au client de choisir**, pas à nous |
| **Pas de nom à consonance médicale ou curative** | « la Vision », « la Clarté » glisseraient vers l'allégation. Des lieux et des noms, pas des promesses |

→ **Questions ajoutées au questionnaire** (§5.4 révisée, §5.8).

---

### 2.4 · LumeLens — **la découverte par niveaux**

**Provenance :** Dribbble.

**Ce qu'il fait.** Une expérience « Vision-First » avec une **découverte produit à niveaux** :
scrollers « Trending Products » et « Best Selling », conçus pour **réduire la charge cognitive** sur des
catalogues optiques à fort inventaire. La navigation par style de vie utilise la **portraitistique**
pour aider à visualiser les formes (ronde, œil-de-chat, aviateur) en contexte réel.

| Motif | Verdict | Transposition |
|---|---|---|
| **La découverte à niveaux** plutôt qu'une grille plate de 40 montures | ✅ **Prendre le principe** | C'est ce qui fait qu'un catalogue paraît **choisi** au lieu d'être **déversé** |
| **Par forme** (ronde · carrée · œil-de-chat · aviateur) | ✅ **Prendre** | Utilisable dès qu'on a les photos |
| **Par usage** (travail · lecture · conduite · soleil) | ✅ **Prendre** | Déjà retenu |
| **Nouveautés** | ⚠️ **Sous condition** | Suppose un **stock qui tourne**. Non documenté — question au client |
| **Best-sellers / Trending** | ⛔ **Interdit en l'état** | Voir §3.1 — c'est un **classement**, et la règle 4 les interdit. **Mais il existe un chemin légitime** |
| **La portraitistique** | ⚠️ **Sous condition stricte** | Voir §3.2 — conflit direct avec « aucun visage inventé » |

**L'angle de contenu proposé** — *« Les 5 montures les plus demandées ce mois-ci »* — est excellent
**s'il repose sur des données réelles**. Voir §3.1 pour comment les produire nous-mêmes.

---

### 2.5 · Le motif WhatsApp-first africain — **le CTA par produit**

**Provenance :** Kolonell, Dev.to, Contra.

**Ce qu'il fait.** *« Le mode catalogue pose un bouton « Enquire » sur chaque produit, qui ouvre
WhatsApp ou un formulaire. »* WhatsApp comme CTA primaire, **répété à chaque point de rupture**.
*« Construire assez de confiance pour justifier un achat sans magasin physique »* — audience
mobile-first, CTA WhatsApp saillant à plusieurs points de défilement.

**Verdict : ✅ transposer intégralement. C'est le cœur du site.**

**Ce que la recherche confirme, et ce qu'elle affine :**

| | |
|---|---|
| **Confirmé** | C'est déjà le standard AMK, et la recherche établit que c'est **le bon choix pour ce marché** — pas une préférence maison |
| **Affiné** | **Chaque produit a son propre message pré-rempli nommant la monture.** C'est la granularité qui convertit |

**Contrainte technique déjà couverte.** Le texte statique doit être encodé **exactement** comme le fait
le JavaScript — c'est l'une des **38 assertions** du test existant.

**Pourquoi ce motif est le plus important des sept.** Il rend **tout mesurable** : on compte des
conversations, pas des intentions. C'est ce qui rend applicable la règle des 3 000 FCFA par **message**
(`content-plan-month1.md` §5), et c'est ce qui donne à une SARL sous contrôle fiscal un rapport
**vérifiable**.

---

### 2.6 · Muffin Group — **l'architecture hybride clinique / commerce**

**Provenance :** Muffin Group.

**Ce qu'il fait.** **Nomme directement le problème structurel.** Un site d'optométrie a besoin de
**pages de service** pour les examens de vue complets, et de **pages de catégorie** pour les verres
progressifs, photochromiques et les traitements antireflet. *« Beaucoup de contenu à organiser sans que
la navigation donne une impression d'encombrement. »*

**La solution de navigation — ✅ à prendre telle quelle :**

| Niveau supérieur | Contenu |
|---|---|
| **Soins** | Examen de vue · consultation — **le versant clinique** |
| **Montures** | Montures, par catégorie — **le versant commerce** |
| **Verres** | Verres, par type — **le versant produit** |

> **Trois entrées de premier niveau. Tout le reste vit à l'intérieur.**

**Verdict : la structure demandée par King est déjà alignée.** Les six sections demandées se rangent
naturellement sous ces trois entrées :

| Demande de King | Entrée |
|---|---|
| Examen de vue | **Soins** |
| Nos montures | **Montures** |
| Nos verres | **Verres** |
| Accueil · À propos · Contact | service, pas offre |

⚠️ **À noter :** Muffin Group mentionne des **verres progressifs, photochromiques et antireflet**. Ce
sont des **produits de dispositif** — en parler exige de ne faire **aucune allégation de performance**.
On décrit **l'usage** (« pour la conduite », « pour la lecture »), jamais **l'effet** (« réduit la
fatigue », « améliore la vision »).

---

### 2.7 · Minimal.gallery — **le principe de retenue** *(référence ajoutée par la compilation)*

**Provenance :** minimal.gallery.

**Ce qu'il fait.** Ne sélectionne que des designs **minimaux** — beaucoup d'espace blanc, propre et
simple. *« L'art de la simplicité et le pouvoir de la retenue. »*

**Ce qui se transpose : la discipline.** Pour un opticien de quartier, la tentation est de **remplir
chaque pixel**. La recherche dit l'inverse : **fond blanc, une seule couleur d'accent, laisser les
montures être l'héroïne.**

**La version pratique, énoncée par King :** la règle de Focal — **« un seul teal pour gouverner la
palette »**. Chaque couleur dépend d'**une seule variable CSS**. **On change une variable, et tout le
cabinet change d'identité.**

**Pourquoi c'est décisif ici.** C'est exactement ce qui permet de **trancher le conflit de palette**
(§3.4) à coût quasi nul — et c'est cohérent avec le système déjà construit, qui repose **déjà** sur un
accent unique (la braise `#E0703A`) utilisé une seule fois.

---

## Partie 3 · Les conflits — ce qui ne se règle pas tout seul

Cinq points où la recherche et les contraintes du dossier se touchent. **Aucun n'est tranché en
silence.**

### 3.1 · ⛔ « Best-sellers » et « Trending » — interdits en l'état, mais il y a un chemin

**Le conflit.** La règle 4 interdit **tout classement inventé**. « Best-sellers » et « les 5 montures
les plus demandées ce mois-ci » sont des **affirmations de classement**. Or nous n'avons **aucune
donnée de vente** du cabinet.

**Pourquoi je ne l'accepte pas tel quel.** Un classement sans donnée est une invention, et sur un
produit de santé vendu par un cabinet sous contrôle fiscal, une affirmation invérifiable est un risque
— pas un détail de style.

**Le chemin légitime — et il est bon :**

> **Nous pouvons produire la donnée nous-mêmes.** Dès le mois 1, chaque fiche monture porte son propre
> WhatsApp pré-rempli (§2.5). **On peut donc compter les demandes par monture.** À partir du mois 2,
> « les montures les plus demandées » devient un **fait sourcé**, mesuré par nous, et non un classement
> supposé.

**Règle proposée :**

| Formulation | Statut |
|---|---|
| « Best-sellers » | ⛔ Jamais — suppose des ventes qu'on ne connaît pas |
| « Les plus demandées **ce mois-ci** » **avec le comptage WhatsApp derrière** | ✅ Autorisé dès que deux semaines de données existent |
| « Trois montures que nos clients demandent souvent » **sans chiffre** | ⚠️ Seulement si le client l'affirme lui-même |

→ **Action :** ajouter un **comptage des demandes par monture** au rapport mensuel. Ça ne coûte rien,
et ça transforme une invention en mesure.

### 3.2 · ⚠️ La portraitistique — conflit direct avec « aucun visage inventé »

**Le conflit.** LumeLens utilise des **portraits** pour faire visualiser les formes de monture. Notre
règle 7 interdit **tout visage inventé**, et aucune photo de patient ne peut servir **sans accord
écrit**.

**Trois issues :**

| Issue | Verdict |
|---|---|
| **Portraits générés** | ⛔ **Interdit.** Un visage inventé sur un produit de santé est une fabrication |
| **Portraits de vrais clients** | ⚠️ Possible **uniquement avec accord écrit**, et c'est une lourdeur pour un cabinet de quartier |
| **Silhouettes et schémas de forme** | ✅ **Recommandé.** Un diagramme de forme (ronde · carrée · œil-de-chat · aviateur) transmet **exactement le même bénéfice** — visualiser la forme — **sans aucun visage** |

**Recommandation : les schémas de forme.** C'est du SVG, donc **produisible sans photo**, donc
disponible dans la fenêtre actuelle — et zéro risque de consentement ou d'image.

### 3.3 · ⚠️ Les prix énoncés — ⚠️ j'avais sur-contraint ce point

**Ce que j'ai écrit le 01/10 au matin**, dans `brief.md` §6 : *« Aucun prix affiché »* comme règle
absolue.

**C'était trop strict, et je le corrige.** Les contraintes réelles de King sont : **rien d'inventé** et
**jamais de remise**. **Afficher un tarif confirmé par le client n'est ni une invention ni une remise.**
La règle exacte est donc :

> ✅ **Un prix confirmé par le client peut être affiché.**
> ⛔ **Un prix non confirmé, estimé, ou emprunté à un autre, ne peut jamais l'être.**
> ⛔ **Aucune remise, aucun « à partir de » racoleur qui sous-entend une promotion.**

**D'où venait ma sur-contrainte.** La décision du 24/09 (aucun prix affiché, question renvoyée à la
boutique) a été prise **parce qu'aucun tarif n'était confirmé** — c'était une conséquence de
l'ignorance, pas un principe.

**Ce que la recherche apporte.** Focal énonce ses prix, et King note que **c'est un fort mouvement de
confiance** si le client accepte ; sinon, des fourchettes « à partir de ».

**Verdict.** C'est **une décision, pas une violation** — et elle appartient à King. Les tarifs sont
demandés au questionnaire (§4.1–4.2). ⚠️ **Mais une fourchette « à partir de » engage** : elle devient
une attente. À peser dans un quartier sensible au prix, où un « à partir de » mal calibré fait fuir
aussi sûrement qu'un prix absent.

### 3.4 · ✅ La palette — **la recherche tranche le conflit**

**Le conflit que j'avais signalé le 01/10 au matin.** King interdit le **« cliché médical bleu et
blanc »** ; la palette construite est **papier froid + marine profond** (`#1A3F86`, `#2A5CB8`,
`#4E7BD8`) + accent braise (`#E0703A`).

**La compilation le résout, et proprement.** Focal — la référence la plus proche — travaille en
**fond blanc, typographie à l'encre, un seul teal profond**. Et Minimal.gallery donne le mécanisme :
**une seule variable CSS**.

> **Recommandation : remplacer le marine par un teal profond.**

| Critère | Verdict |
|---|---|
| Est-ce le cliché bleu-blanc médical ? | **Non** — le teal n'est pas le bleu clinique, et Focal le prouve en optique |
| Fond blanc + un seul accent ? | **Oui** — conforme à la retenue de Minimal.gallery |
| Éprouvé pour l'optique ? | **Oui** — c'est la palette de la référence n° 1 |
| Échappe au reskin du **Cristallin** (papier froid, étiquettes mono) ? | **Oui** — le teal et l'échelle de vue en distinguent nettement le registre |
| Échappe à la page opticien sombre (**Cavisa**) ? | **Oui** — fond blanc |
| Coût | **Une variable CSS.** Le travail testé 38/38 n'est pas jeté |

**C'est la réponse que je cherchais au tour précédent.** Elle reste **à confirmer par King** — c'est son
œil, sur un téléphone, qui tranche, pas ce document.

### 3.5 · ⚠️ L'échelle de vue contre l'anneau de verre

**Le conflit.** Le premier écran construit porte un **anneau de verre** qui se trace (`.lensring`,
dégradé `#7FA6E8 → #2A5CB8 → #E0703A`, rotation 24 s). Focal propose une **échelle de vue géante qui se
réduit** — « personne ne la dépasse sans la voir ».

| | Anneau de verre *(actuel)* | Échelle de vue *(Focal)* |
|---|---|---|
| Immédiatement optique ? | Moyennement — un anneau est abstrait | **Oui — indiscutable** |
| Coût | déjà construit et testé | à construire — **mais typographie + SVG, aucune photo** |
| Bilingue | indifférent | ⚠️ **deux jeux** : l'échelle FR ≠ l'échelle EN |
| Sert-il le message ? | décor | **il dit le métier** |

**Recommandation : l'échelle de vue**, pour deux raisons — elle est **plus lisible comme signe
optique**, et elle est **produisible maintenant**, sans attendre les photos. À confirmer par King.

---

## Partie 4 · Classement — les sept directions, par applicabilité directe

| # | Référence | Ce qu'on vole | Pourquoi ça convient à DM OPTIQUE |
|---|---|---|---|
| **1** | **Focal** (Hatchable) | Signature « échelle de vue » · examen itemisé · prix énoncés · rendez-vous WhatsApp | **La correspondance la plus proche.** Fond blanc, un accent, confiance médicale + clarté commerciale |
| **2** | **Warby Parker** (Zarla) | Le quiz comme entrée à faible engagement · barre de rassurance | Adapté en WhatsApp : « 3 questions → 5 montures qui vous correspondent ». ⚠️ sous réserve de profondeur d'inventaire |
| **3** | **Moscot** (Zarla) | **Nommage propriétaire** des montures | **Ne coûte rien, rend le catalogue appropriable, nourrit le contenu.** « la Bonabéri », « la Sanaga » |
| **4** | **LumeLens** (Dribbble) | Découverte à niveaux : nouveautés · par forme · par usage | Résout le « mur de montures » — ⚠️ best-sellers écartés (§3.1), portraitistique remplacée (§3.2) |
| **5** | **Motif WhatsApp-first africain** (Kolonell, Dev.to, Contra) | CTA WhatsApp **par produit**, répété aux points de rupture | Déjà le standard AMK. **Raffinement : chaque monture a son message pré-rempli** |
| **6** | **Muffin Group** | Navigation à trois : **Soins · Montures · Verres** | Empêche l'encombrement qui tue les sites d'optique |
| **7** | **Minimal.gallery** | **La retenue** — une variable CSS gouverne la palette | C'est ce qui rend le changement de palette quasi gratuit, et tient la page hors du cliché |

---

## Partie 5 · Ce qu'on évite — explicitement

| À éviter | Pourquoi, d'après la recherche | Comment on vérifie |
|---|---|---|
| **Le cliché médical bleu et blanc** | Tous les concurrents le font. Il signale « clinique générique », pas « l'opticien de confiance de Bonabéri » | ✅ **Résolu par le teal** (§3.4) — à confirmer |
| **Les photos génériques de médecins souriants** | La recherche les qualifie d'**impersonnelles et destructrices de confiance** | Aucun visage généré. **De vraies photos du magasin, des montures réelles, du vrai matériel** |
| **Le panier e-commerce** | Les acheteurs camerounais convertissent sur **WhatsApp**, pas sur un panier. Ne pas construire un tunnel que DM OPTIQUE n'utilisera jamais | Aucun bouton « ajouter », aucune page de paiement |
| **Les slogans génériques** | *« Excellence in Healthcare »* est cité par la recherche comme **tueur de crédibilité** | **Le test de l'échange** : si la phrase tient avec le nom d'un autre cabinet, elle ne dit rien |
| **L'esthétique sombre et luxueuse** | Ça marche pour Warby Parker et les marques de lunetterie mode. **Pas pour une clientèle populaire de Bonabéri.** Chaud, propre, direct | Fond blanc. Mode sombre déjà refusé — un patient lit dehors, en plein jour |

**Le slogan spécifique proposé par King, et il est bon :**

> **« L'opticien enregistré à Bonabéri. Examen de vue sur place. »**

Il passe le test de l'échange : remplaçé par le nom d'un autre cabinet, **il ne tient plus** — il nomme
un lieu précis, un statut vérifiable, et un service rendu sur place. **C'est exactement le registre
qu'il faut.**

⚠️ **Une réserve sur le mot « enregistré ».** Il est juste (inscription ONOC 021/2016) mais il **désigne
implicitement ceux qui ne le sont pas**. La règle 5 interdit de nommer un concurrent — y compris par
implication. **Formulations sûres équivalentes** : « Opticien **inscrit à l'ONOC**, à
Bonabéri » — on affirme **son** statut, on ne qualifie personne d'autre.

---

## Partie 6 · Ce que cette compilation change dans les autres documents

| Document | Changement |
|---|---|
| `website/brief.md` | **Palette** : marine → **teal profond** (§3.4) · **Architecture** : navigation à trois parties maintenant, découpe en pages aux photos (§1.1) · **Prix** : règle corrigée — un tarif **confirmé** peut s'afficher (§3.3) · **Signature** : échelle de vue proposée (§3.5) |
| `content-plan-month1.md` | **Le nommage devient un moteur de contenu** (§2.3) · **« les plus demandées » conditionné au comptage WhatsApp** (§3.1) |
| `onboarding/intake-questionnaire.md` | **Profondeur d'inventaire** ajoutée — condition du quiz (§2.2) · **noms de montures** précisé (§2.3) · **mutuelles** confirmées comme remplaçant de la liste d'assurances (§2.1) |
| `pre-launch-checklist.md` | Inchangé — les photos restent au portique, et la recherche le **renforce** (« lead with strong visuals of the actual work ») |

---

## Partie 7 · En attente de décision

- [ ] **Architecture** — navigation à trois parties maintenant, découpe en pages aux photos ? (§1.1)
- [ ] **Palette** — marine → teal profond ? (§3.4)
- [ ] **Signature du premier écran** — échelle de vue ou anneau de verre ? (§3.5)
- [ ] **Prix** — afficher des tarifs confirmés, des fourchettes « à partir de », ou rien ? (§3.3)
- [ ] **Quiz WhatsApp** — engagé ou non, **selon la profondeur d'inventaire** relevée à la visite (§2.2)
- [ ] **Nommage des montures** — qui choisit les noms, et lesquels ? (§2.3)
- [ ] **Consolidation ou non** avec `clients/dm-optic/inspiration.md` (24/09, le style)
- [ ] **Approbation du plan de contenu**

⛔ **Aucune production avant approbation du plan de contenu.**
