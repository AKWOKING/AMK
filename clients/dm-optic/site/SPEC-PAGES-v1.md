# DM OPTIQUE — SPEC PAGES v1 (planning pré-dépôt, ruling King 06/10) — révisé 08/10 (réponse client 14:58)

> **RÉVISION 08/10 — réponse du client reçue à 14:58** (suite au jeu de questions de 13:26). Texte
> exact **non transmis** à l'orchestrateur : les points ci-dessous sont ceux que King a rapportés ;
> le verbatim reste à coller (journal : `onboarding/post-deposit-email.md`). Six changements :
> **(1)** aucun prix sur les cartes ni les fiches — CTA WhatsApp seul · **(2)** plus de bandes de prix :
> la rangée 2 = Forme · Matériau · Couleur · **(3)** taxonomie confirmée pour un stock de 400 montures ·
> **(4)** convention de nommage abandonnée : les noms du client, tels quels · **(5)** heures mises à jour ·
> **(6)** stock : `[400 montures — confirmé client 08/10]`.
> **Raison « pas de prix » :** contrainte réglementaire invoquée par le client (ministère de la Santé
> publique, selon King) — statut de la règle : `sales/PACK-OPTICIEN-2026-10.md` § « Fait de marché ».
> Ancienne version de ce fichier : `d1f0360` (historique git).

> Périmètre : **structure + spec uniquement**. Pas de contenu produit, pas de design (palette/typo =
> phase séparée), pas d'assets. Les noms/descriptions des montures viendront du client ; **aucun prix n'est affiché** (ruling 08/10).
> Toute donnée client manquante = **[À CONFIRMER — client]**, jamais inventée.
> Faits tracés au repo : adresse (proforma v2) · WhatsApp 656 122 239 (proforma v2) · heures
> (client, 08/10 14:58, formulation rapportée par King) : examen de vue 8h30–13h00 · autres besoins 8h30–17h30 (**jours NON connus** ; remplace 8h00–17h30 / consultation 8h30–13h30 du 25/09) ·
> inscription ONOC 021/2016, arrêté 0382, titulaire M. Domche Noumbi (registre ONOC, annuaire
> Littoral, ligne 102 — `build-notes.md`). **Aucun diplôme n'est prouvé au repo : aucune mention
> « diplômé » nulle part** (ruling King 08/10 ; règle : `content/strategy/RULE-CREDENTIAL-CLAIMS.md`).
> Photos / domaine / hébergement = **après dépôt** (ruling).

---

## 0 · L'atome — carte produit (schéma ruling, appliqué partout où une carte apparaît)

| Élément | Spec |
|---|---|
| Photo monture | fond uni blanc ou gris clair, même angle pour toutes (cohérence grille) |
| Nom | tel que fourni par le client — aucune convention imposée (§7) |
| Description | 1 ligne : matière, forme, caractère — fournie par le client |
| CTA | bouton « **Commander sur WhatsApp** » |

**Mécanisme CTA (comportement exact, ruling) :** un tap ouvre WhatsApp avec message pré-rempli,
nom injecté depuis la carte, une seule tape, ni formulaire ni e-mail :

> « Bonjour DM Optique, je suis intéressé par la monture [Nom]. Est-elle disponible ? »
>
> *(Le « ([Prix]) » du verbatim ruled est retiré par conséquence du ruling « aucun prix » du 08/10 — lecture de ma part ; dis-le si tu veux garder une autre forme.)*

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

> **RULING KING 08/10 (soir) — *Category pills and search bar hidden until ≥1 frame card exists. Re-enable in the frames-catalog commit.*** Une affordance qui ne fonctionne pas est pire que pas d'affordance : pas de carte monture → ni pills de catégorie, ni barre de recherche, ni filtre. En attendant, le site est un socle : Accueil + Contact + À propos + bouton WhatsApp flottant. **Ceci remplace** la ligne « toujours présente, même catalogue plat » du schéma ci-dessous et le « grille plate + barre de recherche » du mode plat (annotés, non effacés).

```
┌──────────────────────────────┐
│ header + flottant (§1)       │
├──────────────────────────────┤
│ [🔍 Rechercher…]  sticky     │  ~~toujours présente, même catalogue plat~~ → CACHÉE tant qu'aucune carte (ruling 08/10 soir)
├──────────────────────────────┤
│ RANGÉE 1 (si catalogue tagué)│  pills, scroll horizontal, jamais dropdown
│ (Toutes)(Femme)(Homme)       │
│ (Enfant)(Soleil)(Vue)        │
├──────────────────────────────┤
│ RANGÉE 2 (seulement si une   │
│ primaire choisie OU 400+)    │
│ (Ronde)(Carrée)(Œil-de-chat) │
│ (Aviateur)(Ovale)            │
│ Matériau (…) · Couleur (…)   │
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
  rangée 2 = une pill active par groupe (Forme / Matériau / Couleur), combinables en intersection avec la
  rangée 1 ; recherche = filtre par nom (insensible casse/accents) ; grille 2 col, cartes tap
  ≥44 px ; first paint ≤3 s : lots de 12, images lazy.
- **Mode plat (RÈGLE, ruling 08/10) :** catalogue non tagué = grille plate + barre de recherche *(barre cachée tant qu'aucune carte n'existe — ruling 08/10 soir)*,
  **aucun filtre, aucune pill grisée, aucun « bientôt »**. Les filtres s'allument quand les données
  portent les tags (§6) : un commit de données, pas de reconstruction.
- **États vides/erreur :** combinaison sans résultat → état vide ci-dessus (jamais page blanche) ;
  recherche sans résultat → même bloc avec le terme cité.
- **Inventaire :** `[400 montures — confirmé client 08/10]` (la taxonomie §6 est dimensionnée pour 400).
- **[À CONFIRMER — client] :** existence d'un stock enfant/soleil au lancement · valeurs réelles de
  Matériau et de Couleur (issues du tag d'inventaire).

## 3 · FICHE MONTURE `/montures/[nom]`

```
┌──────────────────────────────┐
│ HERO image (fond uni)        │  swipe si 2+ angles [APRÈS DÉPÔT]
├──────────────────────────────┤
│ Nom                          │
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
- **Mobile :** CTA pleine largeur sous la description (pouce) ; accordéon natif sans JS lourd ; similaires
  en scroll horizontal ; first paint ≤3 s (image lazy, texte d'abord).
- **États vides/erreur :** URL inconnue / monture retirée → « Cette monture n'est plus disponible.
  Voici des modèles proches. » + similaires + CTA ; similaires vides → section masquée, pas vide ; catalogue non tagué (§6) → section masquée
  (pas de similarité sans tags).
- **[À CONFIRMER — client] :** champs matière/taille/couleur selon fiche inventaire (Matériau et Couleur = candidats de filtre confirmés 08/10 ; taille selon tag). **Aucun prix sur la fiche.**

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
- **Adresse (fait proforma v2) :** DM OPTIQUE SARL, immeuble West Hotel, 1er étage, dernière porte à droite, Ndobo Mayor, Bonabéri,
  Douala IV. **Heures (client, 08/10 14:58) :** Examen de vue : 8h30–13h00 · Autres besoins : 8h30–17h30.
- **Épingle Maps (post-acompte, ruling 08/10) :** précision = « Immeuble West Hotel, 1er étage, dernière porte à droite ». Une épingle
  seule, au rez-de-chaussée, serait fausse : l'étage et la porte s'écrivent **en texte** juste sous la
  carte et dans le champ adresse (ligne 2) de la fiche Google. *(Un pin n'a pas d'étage ; mise en
  œuvre = ma lecture du ruling.)*
- **Mobile :** click-to-call `tel:` ; Maps = lien externe (pas d'embed lourd) ; carte statique =
  image ≤80 Ko ou simple bloc adresse si plus léger ; tap targets ≥44 px.
- **États erreur :** carte statique indisponible → bloc adresse seul + bouton Maps (dégradation
  propre, jamais page cassée).
- **[À CONFIRMER — client] :** **jours d'ouverture** (heures connues, jours NON) · numéros réseaux
  (placeholders jusqu'au go-live, §9). **Repère : CLOSED 08/10** — King sur place mercredi : le cabinet est à
  « Immeuble West Hotel, 1er étage, dernière porte à droite » ; aucune question client.

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
- **Rangée 2, secondaires (révisé 08/10) :** **Forme** — Ronde · Carrée · Œil-de-chat · Aviateur · Ovale ;
  **Matériau** et **Couleur** — candidats ajoutés, **valeurs issues du tag d'inventaire** (non inventées ici).
  Rangée **conditionnelle : visible quand une primaire est sélectionnée OU que le catalogue compte 400+
  montures** — le stock du client (400) y satisfait : rangée visible d'emblée.
  *Écart signalé :* le ruling du 08/10 matin disait « 20+ » ; le ruling 08/10 (réponse client) dit « 400+ ».
  Appliqué **littéralement (400+)**. À 400 montures les deux seuils donnent le même résultat ; ils ne
  diffèrent que pour un catalogue partiel de 20 à 399 — dis-moi si tu voulais garder 20.
- **Bandes de prix : SUPPRIMÉES (ruling 08/10).** Aucun prix affiché nulle part (cartes, fiches, filtres).
  Le tri par prix de la référence Zenni n'est pas repris.
- **Retirés :** Rectangulaire (recouvre Carrée au niveau de tag habituel : l'un ou l'autre) ·
  Géométrique (trop rare en stock d'opticien : pill à zéro résultat). **Matériau : désormais candidat**
  (v1 conditionnelle au tag d'inventaire ; la mention « hors v1 » du 08/10 matin est levée).
- **Pas de pill à zéro résultat :** une pill de rangée 2 n'est rendue que si ≥1 monture
  porte le tag (calculé sur les données, pas à la main).
- **Mode plat = règle, pas repli :** catalogue non tagué → grille plate + recherche, **sans
  filtres** (ni pills grisées ni « bientôt »). Activation par les données, un commit.
  *Lecture littérale : « sans filtres » inclut la rangée 1 (Femme/Homme/…) — elle dépend aussi
  des tags. Si tu veux la rangée 1 sur un stock partiellement tagué, dis-le.*
- **Références (comparaison réelle) :** formes Warby Parker — cat-eye, square, round, oval,
  rectangle, geometric, aviator ([source](https://www.warbyparker.com/sitemap),
  [source](https://clark.com/save-money/warby-parker-review/)) · filtres Zenni — formes + plein/demi
  cadre (+ tri prix, non repris ici) ([source](https://www.zennioptical.com/b/glasses-for-square-face)).

## 7 · Nommage — convention ABANDONNÉE (ruling King 08/10, réponse client 14:58)

- **Les noms du client, tels quels.** Le client juge ses noms « trop diverses » (fragment rapporté par King) :
  **aucune convention imposée**, aucune suggestion de noms de lieux, aucun renommage. La carte affiche le
  nom fourni.
- **Mécanique (pas un ruling) :** l'URL `/montures/[nom]` est dérivée du nom fourni (slug) ; en cas de
  doublon, suffixe interne — non affiché.
- **Remplace** la section « suggérée, le client nomme » du 08/10 matin (Warby Parker, noms de lieux) :
  version précédente = `d1f0360`.

---

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
| Heures · prix · taille du stock · nommage | **RÉPONDU par le client 08/10 14:58** (verbatim non transmis) : heures données (**jours toujours NON confirmés**) · prix non affichés · stock 400 · noms tels quels — `CLIENT-QUESTIONS-2026-10-08.md` |
| Photos (logo/devanture/équipe) | Annoncées, non demandées (option A) — non couvert par les éléments transmis de la réponse ; **après acompte** |
| Photo hero · photo À propos · bornes exactes par bande · méthode de tag | **Décisions internes, phase build** (ruling) |
| Repère près de l'adresse | **CLOSED (ruling 08/10)** — King sur place mercredi : « Immeuble West Hotel, 1er étage, dernière porte à droite ». Aucune question client. |
| Texte des mentions légales | **Phase build** — rédigé en interne, le client relit à la livraison |
| Comptes réseaux sociaux (footer/contact) | **Phase build** — les conditions confient à AMK la création Facebook + TikTok (`CONDITIONS-D-INTERVENTION` l.11, vérifié) ; ils n'existent pas encore : footer en **placeholders**, activés au go-live |
| Validation du paragraphe À propos | **Phase build** — rédigé en interne, le client approuve à la livraison |
| Champs matière/taille/couleur · filtres Matériau/Couleur | **Phase build, liés au tag d'inventaire** — si le tag se fait (400 montures), les champs et filtres existent ; sinon non |
| « Aucun prix » : base réglementaire | **Déclarée par le client, corroborée en partie, non vérifiée pour l'affichage en ligne** — `sales/PACK-OPTICIEN-2026-10.md` § Fait de marché |

**Questions client : quatre, pas de sixième** (ruling 08/10) — **répondues le 08/10 à 14:58**.
