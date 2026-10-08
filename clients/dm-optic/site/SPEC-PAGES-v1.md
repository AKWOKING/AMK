# DM OPTIQUE — SPEC PAGES v1 (planning pré-dépôt, ruling King 06/10)

> Périmètre : **structure + spec uniquement**. Pas de contenu produit, pas de design (palette/typo =
> phase séparée), pas d'assets. Les noms/descriptions/prix des montures viendront du client.
> Toute donnée client manquante = **[À CONFIRMER — client]**, jamais inventée.
> Faits tracés au repo : adresse (proforma v2) · WhatsApp 656 122 239 (proforma v2) · heures
> 8h00–17h30, consultation 8h30–13h30 (post-deposit-email — **jours NON connus**) · opticien diplômé
> = inscription ONOC 021/2016, arrêté 0382, titulaire M. Domche Noumbi (CRM).
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
cabinet, fait proforma v2). Le bouton flottant global (§contraintes) ouvre le même canal avec un
message court : « Bonjour DM Optique ! » (copy proposée, dans le périmètre headlines/CTA).

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
│  [Commander sur WhatsApp]    │  CTA secondaire WhatsApp (flottant = principal)
├──────────────────────────────┤
│ TRUST BAR : opticien diplômé │  3 items, une ligne chacun
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

- **Copy exacte :** H1 « Votre opticien à Bonabéri, Douala. » · sous-titre « Voyez les montures avant d'entrer. » · trust bar : « Opticien diplômé » (fait ONOC) · « Conseil personnalisé » ·
  « Sur rendez-vous » · étapes : « 1. Parcourez les montures » · « 2. Envoyez un message WhatsApp » ·
  « 3. Passez en boutique, essayez, repartez servi. »
- **Mobile :** hero = 1 image ≤100 Ko lazy, first paint ≤3 s en 3G (image hors first paint si
  nécessaire : texte d'abord) ; carrousel = scroll horizontal natif, pas de dropdown ; tap targets
  ≥44 px (CTA, toggle, cartes) ; FR par défaut, toggle EN visible header (strings EN =
  [À PRODUIRE — phase contenu]).
- **États vides/erreur :** si « à la une » vide (inventaire non chargé) → bloc repli :
  « Le catalogue arrive — écrivez-nous, on vous montre les montures en message. » + CTA WhatsApp.
- **[À CONFIRMER — client] :** photo hero (après dépôt) · libellé réseaux sociaux (comptes à créer
  à l'encaissement) · texte mentions légales.

## 2 · CATALOGUE `/montures`

```
┌──────────────────────────────┐
│ header + flottant (§1)       │
├──────────────────────────────┤
│ [🔍 Rechercher…]  sticky     │  barre sticky sous header
├──────────────────────────────┤
│ (Toutes)(Femme)(Homme)       │  pills horizontales scrollables,
│ (Enfant)(Soleil)(Vue)        │  une seule rangée, jamais dropdown
│ (Forme)(Prix)                │
├──────────────────────────────┤
│ grille 2 col mobile /        │  cartes §0
│ 3–4 col desktop              │
├──────────────────────────────┤
│ ÉTAT VIDE par filtre         │
└──────────────────────────────┘
```

- **Copy exacte :** titre « Toutes nos montures » · état vide : « Aucune monture dans ce filtre
  pour l'instant. Écrivez-nous : on cherche pour vous. » + CTA WhatsApp.
- **Mobile :** pills = scroll horizontal, sélection = une pill active combinable (audience +
  catégorie + forme + prix) ; recherche = filtre par nom, tolérant aux fautes (min. : insensible
  casse/accents) ; grille 2 col, cartes tap ≥44 px ; first paint ≤3 s : pagination par lot de 12,
  images lazy.
- **États vides/erreur :** combinaison sans résultat → état vide ci-dessus (jamais page blanche) ;
  recherche sans résultat → même bloc avec le terme cité.
- **[À CONFIRMER — client] :** valeurs Forme/Prix (§6) selon inventaire tagué ; existence d'un
  stock enfant/soleil au lancement.

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
  Voici des modèles proches. » + similaires + CTA ; similaires vides → section masquée, pas vide.
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
  « Écrire sur WhatsApp » · « Appeler le cabinet ». **Aucun formulaire de contact — un seul
  canal : WhatsApp** (ruling).
- **Adresse (fait proforma v2) :** DM OPTIQUE SARL, immeuble West Hotel, Ndobo Mayor, Bonabéri,
  Douala IV. **Heures (fait repo) :** 8h00–17h30 · consultation 8h30–13h30.
- **Mobile :** click-to-call `tel:` ; Maps = lien externe (pas d'embed lourd) ; carte statique =
  image ≤80 Ko ou simple bloc adresse si plus léger ; tap targets ≥44 px.
- **États erreur :** carte statique indisponible → bloc adresse seul + bouton Maps (dégradation
  propre, jamais page cassée).
- **[À CONFIRMER — client] :** **jours d'ouverture** (heures connues, jours NON) · point de repère
  « en face de… » (déjà demandé : `a-completer.md` n°1 — un repère de plus aide le patient qui arrive en taxi) · numéros réseaux.

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

## 6 · Taxonomie des filtres — PROPOSITION (King tranche)

Pills ruling : Toutes · Femme · Homme · Enfant · Soleil · Vue · Forme · Prix. Valeurs proposées :

- **Forme** (intersection Warby Parker — 7 formes : cat-eye, square, round, oval, rectangle,
  geometric, aviator [2](https://clark.com/save-money/warby-parker-review/), [3](https://www.warbyparker.com/sitemap) — et Zenni : square, cat-eye, round, rectangle, aviator, browline,
  geometric, oval [1](https://www.zennioptical.com/b/glasses-for-round-face), [2](https://www.zennioptical.com/b/glasses-for-square-face)) :
  **Ronde · Carrée · Rectangulaire · Ovale · Œil-de-chat · Aviateur · Géométrique** (browline
  réservé v2, trop spécifique).
- **Prix** : Zenni filtre par prix (tri + bornes) ; Warby par gamme de largeur/matériau. Proposition
  FCFA : **< 25 000 · 25 000–50 000 · 50 000–100 000 · > 100 000** — bornes **[À CONFIRMER —
  client]** (doivent coller à sa grille réelle).
- **Matériau** (acétate/métal chez les deux) : **hors v1** — une dimension de plus = inventaire à
  taguer ; pills ruling n'incluent pas matériau.

⚠️ **Drapeau inventaire :** Forme et Prix supposent un inventaire **tagué** (une ligne par monture :
audience, catégorie, forme, prix). Si le tag n'existe pas à la mise en ligne, les pills Forme/Prix
produiraient des états vides → plan B ruling-compatible : pills visibles mais grises avec état vide
« bientôt », lancement sur Femme/Homme/Enfant/Soleil/Vue seulement. **[À CONFIRMER — client]** :
l'inventaire sera-t-il tagué avant mise en ligne ?

## 7 · Convention de nommage — PROPOSITION (King tranche)

- **Recommandé : lieux courts du Cameroun** — Bonabéri, Akwa, Deido, Wouri, Kribi, Limbe, Ndobo,
  Mabanda… Courts (≤3 syllabes), propres, fierté locale, mémorables au comptoir (« la Kribi vous
  va bien »). Aucun conflit de marque possible.
- **Précédents réels :** Warby Parker nomme ses best-sellers par des noms propres courts —
  Haskell, Durand, Carlton, Percey [1](https://virat.blog/warby-parker-glasses-review/),
  [2](https://www.warbyparker.com/eyeglasses/haskell/crystal) ; Ray-Ban garde des noms de modèle
  (Clubmaster, cité [1](https://virat.blog/warby-parker-glasses-review/)). Le nom propre court se
  dit à voix haute au comptoir, ce qu'un code ne fait pas. (Je n'avance rien sur Zenni : non vérifié.)
- **Repli :** mots français simples (Net, Clair, Doux) si le client préfère ; codes numériques
  (DM-014) seulement en identifiant interne, jamais comme nom affiché.
- **[À CONFIRMER — client] :** liste finale des noms alignée sur l'inventaire réel ; veto du client
  sur tout nom à connotation locale sensible.

---

## 8 · Contraintes transverses (ruling) — rappel par page fait foi ci-dessus

- Pas d'e-commerce, pas de comptes, pas de blog, pas d'essayage virtuel, pas de newsletter.
- Téléphone d'abord ; desktop = adaptation. Tap targets ≥44 px. Aucun dropdown — pills seulement.
  Scrolls horizontaux pour carrousels. Bouton WhatsApp flottant bas-droite **sur chaque page**.
  First paint ≤3 s en 3G. FR par défaut, toggle EN visible au header.
- WhatsApp = seul canal de conversion ; le pré-rempli verbatim (§0) est la seule mécanique CTA
  produit.
