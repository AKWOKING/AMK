# DM OPTIQUE — SPEC PAGES v1 (planning pré-dépôt, ruling King 06/10)

> Périmètre : **structure + spec uniquement**. Pas de contenu produit, pas de design (palette/typo =
> phase séparée), pas d'assets. Les noms/descriptions/prix des montures viendront du client.
> Toute donnée client manquante = **[À CONFIRMER — client]**, jamais inventée.
> Faits tracés au repo : adresse (proforma v2) · WhatsApp 656 122 239 (proforma v2) · heures
> 8h00–17h30, consultation 8h30–13h30 (post-deposit-email — **jours NON connus**) ·
> inscription ONOC 021/2016, arrêté 0382, titulaire M. Domche Noumbi (registre ONOC, annuaire
> Littoral, ligne 102 — `build-notes.md`). **Aucun diplôme n'est prouvé au repo : aucune mention
> « diplômé » nulle part** (ruling King 08/10 ; règle : `content/strategy/RULE-CREDENTIAL-CLAIMS.md`).
> Photos / domaine / hébergement = **après dépôt** (ruling).

---

## 0 · L'atome — carte produit (schéma ruling, appliqué partout où une carte apparaît)

| Élément | Spec |
|---|---|
| Photo monture | fond uni blanc ou gris clair, même angle pour toutes (cohérence grille) |
| Nom | court, propre, mémorable (convention §7) — fourni par le client |
| Description | 1 ligne : matière, forme, caractère — fournie par le client |
| Prix | en FCFA — fourni par le client |
| CTA | bouton « **Commander sur WhatsApp** » |

**Mécanisme CTA (comportement exact, ruling) :** un tap ouvre WhatsApp avec message pré-rempli,
nom et prix injectés depuis la carte, une seule tape, ni formulaire ni e-mail :

> « Bonjour DM Optique, je suis intéressé par la monture [Nom] ([Prix]). Est-elle disponible ? »

Implémentation : `https://wa.me/237656122239?text=` + message URL-encodé (numéro = WhatsApp du
cabinet, fait proforma v2). Le bouton flottant global (§8) ouvre le même canal avec le **message générique ruled
(08/10)** :

> « Bonjour DM Optique, je vous contacte depuis votre site. »

Ce message générique sert aussi le CTA hero (Home) et le gros bouton WhatsApp (Contact) : aucun
produit en jeu. Le message produit ci-dessus, verbatim ruled, ne porte pas la mention « depuis
votre site » : la source y est implicite (nom de monture) — on ne l'altère pas.

---

## 1 · HOME `/`

```
┌──────────────────────────────┐
│ [LOGO DM]        [FR | EN]   │  header sticky, toggle EN visible
├──────────────────────────────┤
│ HERO : photo unique (vitrine │  1 frame photo [APRÈS DÉPÔT]
│ ou comptoir)                 │
│  H1 : « Votre opticien à      │  headline location-first (copy ci-dessous)
│   Bonabéri, Douala. »         │
│  Sous : « Voyez les montures  │
│   avant d'entrer. »          │
│  [Écrire sur WhatsApp]       │  CTA secondaire WhatsApp (flottant = principal)
├──────────────────────────────┤
│ TRUST BAR : Inscrit à l'ONOC │  3 items, une ligne chacun
│ · conseil personnalisé ·     │
│ sur rendez-vous              │
├──────────────────────────────┤
│ MONTURES À LA UNE : 6–8      │  scroll horizontal sur mobile
│ cartes (§0) ←→ swipe         │  flèches discrètes desktop
├──────────────────────────────┤
│ COMMENT ÇA MARCHE : 1        │  3 pas, numérotés, verticaux mobile
│ parcourir · 2 envoyer        │
│ message · 3 passer en        │
│ boutique                     │
├──────────────────────────────┤
│ FOOTER : adresse · heures ·  │
│ tél · réseaux ·              │
│ mentions légales             │
└──────────────────────────────┘
 (●) bouton WhatsApp flottant, bas-droite, toutes pages
```

- **Copy exacte :** H1 « Votre opticien à Bonabéri, Douala. » · sous-titre « Voyez les montures avant d'entrer. » · trust bar (ruling 08/10) : « Inscrit à l'ONOC » (fait : registre, 021/2016) · « Conseil
  personnalisé » · « Sur rendez-vous » · étapes : « 1. Parcourez les montures » · « 2. Envoyez un message WhatsApp » ·
  « 3. Passez en boutique, essayez, repartez servi. » · CTA hero « Écrire sur WhatsApp » (message
  générique §0 ; « Commander » reste réservé à la carte produit — libellé hero = ma proposition).
- **Mobile :** hero = 1 image ≤100 Ko lazy, first paint ≤3 s en 3G (image hors first paint si
  nécessaire : texte d'abord) ; carrousel = scroll horizontal natif, pas de dropdown ; tap targets
  ≥44 px (CTA, toggle, cartes) ; FR par défaut, toggle EN visible header (strings EN =
  [À PRODUIRE — phase contenu]).
- **États vides/erreur :** si « à la une » vide (inventaire non chargé) → bloc repli :
  « Le catalogue arrive — écrivez-nous, on vous montre les montures en message. » + CTA WhatsApp.
- **[À CONFIRMER — client] :** photo hero (après dépôt) · libellé réseaux sociaux (comptes à créer
  à l'encaissement) · texte mentions légales.

## 2 · CATALOGUE `/montures` (filtres ruled 08/10 — voir §6)

```
┌──────────────────────────────┐
│ header + flottant (§1)       │
├──────────────────────────────┤
│ [🔍 Rechercher…]  sticky     │  toujours présente, même catalogue plat
├──────────────────────────────┤
│ RANGÉE 1 (si catalogue tagué)│  pills, scroll horizontal, jamais dropdown
│ (Toutes)(Femme)(Homme)       │
│ (Enfant)(Soleil)(Vue)        │
├──────────────────────────────┤
│ RANGÉE 2 (seulement si une   │  apparaît : primaire choisie OU ≥20 montures
│ primaire choisie OU ≥20)     │
│ (Ronde)(Carrée)(Œil-de-chat) │
│ (Aviateur)(Ovale) | (prix×4) │
├──────────────────────────────┤
│ grille 2 col mobile /        │  cartes §0
│ 3–4 col desktop              │
├──────────────────────────────┤
│ ÉTAT VIDE                    │
└──────────────────────────────┘
```

- **Copy exacte :** titre « Toutes nos montures » · état vide : « Aucune monture dans ce filtre
  pour l'instant. Écrivez-nous : on cherche pour vous. » + CTA WhatsApp.
- **Mobile :** pills = scroll horizontal ; rangée 1 = une pill active (« Toutes » réinitialise) ;
  rangée 2 = une forme active + une bande de prix active, combinables en intersection avec la
  rangée 1 ; recherche = filtre par nom (insensible casse/accents) ; grille 2 col, cartes tap
  ≥44 px ; first paint ≤3 s : lots de 12, images lazy.
- **Mode plat (RÈGLE, ruling 08/10) :** catalogue non tagué = grille plate + barre de recherche,
  **aucun filtre, aucune pill grisée, aucun « bientôt »**. Les filtres s'allument quand les données
  portent les tags (§6) : un commit de données, pas de reconstruction.
- **États vides/erreur :** combinaison sans résultat → état vide ci-dessus (jamais page blanche) ;
  recherche sans résultat → même bloc avec le terme cité.
- **[À CONFIRMER — client] :** bornes de prix (Q2) · taille du stock (Q3) · existence d'un stock
  enfant/soleil au lancement.

## 3 · FICHE MONTURE `/montures/[nom]`

```
┌──────────────────────────────┐
│ HERO image (fond uni)        │  swipe si 2+ angles [APRÈS DÉPÔT]
├──────────────────────────────┤
│ Nom · Prix FCFA              │
│ description 1 ligne          │
│ [Commander sur WhatsApp]     │  CTA proéminent, pleine largeur mobile
├──────────────────────────────┤
│ matière · forme · taille ·   │  bloc info, 4 lignes
│ couleur                      │
├──────────────────────────────┤
│ accordéon « Détails »        │  fermé par défaut, tap ≥44 px
├──────────────────────────────┤
│ « Vous aimerez aussi » :     │  3–4 cartes §0, scroll horizontal
│ similaires (même forme/      │
│ audience)                    │
└──────────────────────────────┘
```

- **Copy exacte :** CTA « Commander sur WhatsApp » + message pré-rempli verbatim (§0) · accordéon
  « Détails » · section « Vous aimerez aussi ».
- **Mobile :** CTA pleine largeur sous le prix (pouce) ; accordéon natif sans JS lourd ; similaires
  en scroll horizontal ; first paint ≤3 s (image lazy, texte d'abord).
- **États vides/erreur :** URL inconnue / monture retirée → « Cette monture n'est plus disponible.
  Voici des modèles proches. » + similaires + CTA ; similaires vides → section masquée, pas vide ; catalogue non tagué (§6) → section masquée
  (pas de similarité sans tags).
- **[À CONFIRMER — client] :** champs matière/taille/couleur selon fiche inventaire.

## 4 · CONTACT `/contact`

```
┌──────────────────────────────┐
│ Adresse complète             │
│ carte STATIQUE + bouton      │  pas d'iframe par défaut (3G)
│ « Ouvrir dans Maps »         │
├──────────────────────────────┤
│ Horaires (tableau)           │
├──────────────────────────────┤
│ [WhatsApp — gros bouton]     │
│ [Appeler : click-to-call]    │
├──────────────────────────────┤
│ Réseaux : Facebook · TikTok  │
└──────────────────────────────┘
```

- **Copy exacte :** titre « Venez nous voir à Bonabéri » · bouton « Ouvrir dans Maps » ·
  « Écrire sur WhatsApp » · « Appeler le cabinet » (le bouton WhatsApp ouvre le message générique §0). **Aucun formulaire de contact — un seul
  canal : WhatsApp** (ruling).
- **Adresse (fait proforma v2) :** DM OPTIQUE SARL, immeuble West Hotel, Ndobo Mayor, Bonabéri,
  Douala IV. **Heures (fait repo) :** 8h00–17h30 · consultation 8h30–13h30.
- **Mobile :** click-to-call `tel:` ; Maps = lien externe (pas d'embed lourd) ; carte statique =
  image ≤80 Ko ou simple bloc adresse si plus léger ; tap targets ≥44 px.
- **États erreur :** carte statique indisponible → bloc adresse seul + bouton Maps (dégradation
  propre, jamais page cassée).
- **[À CONFIRMER — client] :** **jours d'ouverture** (heures connues, jours NON) · numéros réseaux
  (placeholders jusqu'au go-live, §9). **Repère : CLOSED 08/10** — King sur place mercredi : le cabinet est à
  « Immeuble West Hotel » exactement ; aucune question client.

## 5 · À PROPOS `/a-propos` (optionnel, léger)

```
┌──────────────────────────────┐
│ paragraphe court (3–4        │
│ phrases) + 1 photo           │  photo [APRÈS DÉPÔT]
├──────────────────────────────┤
│ [Voir les montures]          │  1 CTA vers /montures
└──────────────────────────────┘
```

- **Copy exacte :** H1 « À propos de DM Optique » (neutre : aucune formule comparative sans fait au repo) · CTA « Voir les montures ».
- **Fait traçable :** titulaire M. Domche Noumbi, inscrit à l'Ordre (021/2016, arrêté 0382) — une
  phrase, sans enjoliver.
- **Mobile :** une colonne, photo lazy, first paint ≤3 s trivial.
- **États vides :** photo absente au lancement → paragraphe seul (la page reste publiable).
- **[À CONFIRMER — client] :** photo portrait/comptoir · validation du paragraphe par M. Domche.

---

## 6 · Taxonomie des filtres — RULED (King 08/10)

- **Rangée 1, primaires, toujours visibles (catalogue tagué) :** Toutes · Femme · Homme · Enfant ·
  Soleil · Vue.
- **Rangée 2, secondaires :** Ronde · Carrée · Œil-de-chat · Aviateur · Ovale — **n'apparaît que
  quand une primaire est sélectionnée OU que le catalogue compte 20+ montures.**
- **Bandes de prix (proposition par défaut, structure livrée) :** ≤ 20 000 · 20 001–35 000 ·
  35 001–60 000 · > 60 000 FCFA — bornes **[À CONFIRMER — client]** (Q2). *Placement : lecture
  de ma part (non précisée au ruling) — 4 pills en fin de rangée 2, même règle d'apparition, une
  seule bande active.*
- **Retirés :** Rectangulaire (recouvre Carrée au niveau de tag habituel : l'un ou l'autre) ·
  Géométrique (trop rare en stock d'opticien : pill à zéro résultat). **Matériau : hors v1.**
- **Pas de pill à zéro résultat :** une pill de rangée 2 / prix n'est rendue que si ≥1 monture
  porte le tag (calculé sur les données, pas à la main).
- **Mode plat = règle, pas repli :** catalogue non tagué → grille plate + recherche, **sans
  filtres** (ni pills grisées ni « bientôt »). Activation par les données, un commit.
  *Lecture littérale : « sans filtres » inclut la rangée 1 (Femme/Homme/…) — elle dépend aussi
  des tags. Si tu veux la rangée 1 sur un stock partiellement tagué, dis-le.*
- **Références (comparaison réelle) :** formes Warby Parker — cat-eye, square, round, oval,
  rectangle, geometric, aviator ([source](https://www.warbyparker.com/sitemap),
  [source](https://clark.com/save-money/warby-parker-review/)) · filtres Zenni — formes + plein/demi
  cadre + tri prix ([source](https://www.zennioptical.com/b/glasses-for-square-face)).

## 7 · Convention de nommage — RULED (King 08/10) : suggérée, le client nomme

- **Le client nomme ses propres montures** — sa marque, son stock. La convention est une
  **suggestion** livrée dans les questions client (Q5) : noms de lieux courts du Cameroun
  (Bonabéri, Akwa, Deido, Wouri, Kribi…), ≤3 syllabes. Il choisit. **Codes numériques = identifiant
  interne seulement**, jamais affiché.
- **Précédent réel :** Warby Parker nomme ses best-sellers par des noms propres courts — Haskell,
  Durand, Carlton, Percey ([source](https://virat.blog/warby-parker-glasses-review/),
  [source](https://www.warbyparker.com/eyeglasses/haskell/crystal)). Un nom court se dit à voix
  haute au comptoir ; un code non.
- **[À CONFIRMER — client] :** liste finale de noms = celle qu'il choisit (Q5).

## 8 · Contraintes transverses (ruling) — rappel par page fait foi ci-dessus

- Pas d'e-commerce, pas de comptes, pas de blog, pas d'essayage virtuel, pas de newsletter.
- Téléphone d'abord ; desktop = adaptation. Tap targets ≥44 px. Aucun dropdown — pills seulement.
  Scrolls horizontaux pour carrousels. Bouton WhatsApp flottant bas-droite **sur chaque page**.
  First paint ≤3 s en 3G. FR par défaut, toggle EN visible au header.
- WhatsApp = seul canal de conversion ; le pré-rempli verbatim (§0) est la seule mécanique CTA
  produit.

## 9 · Drapeaux — statut après ruling 08/10

| Drapeau | Statut |
|---|---|
| Jours/heures · fourchette de prix · taille du stock · photos (logo/devanture/équipe) · nommage | **Questions client Q1–Q5** — `CLIENT-QUESTIONS-2026-10-08.md` (brouillon, King relit et envoie) |
| Photo hero · photo À propos · bornes exactes par bande · méthode de tag | **Décisions internes, phase build** (ruling) |
| Repère près de l'adresse | **CLOSED (ruling 08/10)** — King sur place mercredi : « Immeuble West Hotel » exactement. Aucune question client. |
| Texte des mentions légales | **Phase build** — rédigé en interne, le client relit à la livraison |
| Comptes réseaux sociaux (footer/contact) | **Phase build** — les conditions confient à AMK la création Facebook + TikTok (`CONDITIONS-D-INTERVENTION` l.11, vérifié) ; ils n'existent pas encore : footer en **placeholders**, activés au go-live |
| Validation du paragraphe À propos | **Phase build** — rédigé en interne, le client approuve à la livraison |
| Champs matière/taille/couleur | **Phase build, liés au tag d'inventaire** — si le tag se fait, les champs existent ; sinon non |

**Questions client : quatre, pas de sixième** (ruling 08/10).
