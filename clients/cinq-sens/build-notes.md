# CINQ SENS — notes de construction (24/09/2026, soir)

**Client** : RÉFÉRENCE OPTIQUE MÉDICALE CINQ SENS SARL — deux cabinets à Douala, **Akwa** et
**Brazzaville**. Répond « **Ok** » le 24/09 à 17:04 au message du lot 4.
**Aperçu** : `demos/concept-cinqsens-v1.html` ← gabarit `demos/cinqsens-v1.tpl.html` + `demos/build_cinqsens.py`
→ déployable dans `hosting/previews/cinqsens/` (`index.html` + `og.jpg`).
**Contrôle approfondi** : `clients/cinq-sens/dossier.md` · **inspiration** : `clients/cinq-sens/inspiration.md`.

---

## 1 · La consigne, et le Design Read

> King, 24/09 : *« From his picture he seems to be someone flashy so let's make his site in his image »*
> + *« look for inspiration online from the United States preferably »* + *« deep research… then read
> pre-flight documents then amk design documents… build the site then audit it »*.

**Design Read**, écrit avant la première ligne de HTML :

> Reading this as: a mobile-first **shopfront with two doors** for patients across Douala, in a
> **loud-and-generous** language (US eyewear retail energy — KREWE's confidence, DIFF's colour, Warby's
> clarity), leaning toward **a poster: off-black + paper + five hues (the name's own five senses) with
> fuchsia owning every action**, condensed display type (Anton), a **drifting arrivals band**, and the
> cabinet's own landmarks as the map.

**Dials** : VARIANCE **8** · MOTION **6** · DENSITY **5**.

## 2 · Les trois références US, et ce qu'on en a fait (détail dans `inspiration.md`)

| Référence | Ce qu'on prend | Ce qu'on rejette |
|---|---|---|
| **KREWE** (La Nouvelle-Orléans) | la confiance du premier écran : une phrase, une action ; l'arrivage mis en avant | e-commerce, prix, mega-menu, mannequins |
| **Warby Parker** (New York) | les preuves de service en bandeau ; une seule action par écran | quiz, panier, prix en dollars |
| **DIFF Eyewear** (Los Angeles) | la **bande qui défile** ; le nuancier ; l'énergie d'un magasin | « buy 1 get 1 free », urgence commerciale, app mobile |

**Trois directions explorées (§19.3)** : **A · LA BANDE D'ARRIVAGE** (retenue) · B · LE RAYON DE LUMIÈRE
(écartée : trop proche de nos pages DM OPTIC / Cristallin) · C · LE BLOC-NOTES DES CINQ SENS (écartée :
elle range les services dans une grille poétique au lieu de répondre au patient).

**Différenciation (≥ 4 axes)** : architecture « magasin à deux portes » · palette noir + papier + cinq
teintes (rose vif dominant) · typographie **Anton** / Inter Tight / Space Mono · mouvement : une **bande
d'arrivage** inédite dans le dépôt · ton enthousiaste et direct.

## 3 · La provenance de chaque valeur (§18.1) — rien d'inventé

| Sur la page | Source |
|---|---|
| Les deux adresses et leurs repères (Collège King Akwa, snack le Kokotier, immeuble Flore service ; carrefour Brazzaville, immeuble Michelin) | **leurs propres publications** (Blogger, X, LinkedIn) |
| 696 698 136 (WhatsApp + appel) | **leurs publications** + **ligne 118 du registre ONOC du Littoral** |
| 655 163 365 (deuxième ligne, appel seulement) | **leurs publications** |
| Horaires « annoncés » : lun–sam 8h–18h, fériés 8h–15h | **deux annuaires concordants** (Maligah, Mont-Pandi) → écrits comme *annoncés*, **absents du schéma `openingHours`** |
| Les sept services | **leur description YouTube** (2020) + fiche Maligah |
| « Toutes les bourses », « prévenir la cécité », « le meilleur partenaire pour une vision plus nette » | **leur mission**, mot pour mot |
| « L'œil, c'est la lampe du corps… » | **leur phrase**, citée et attribuée (« la phrase du cabinet ») |
| Les trois photos | **générées**, légendées « Photo d'illustration » — le cabinet n'a rien envoyé |
| Adresse, prix, marques, avis, nom du responsable | **jamais écrits** : inconnus ou non publiés |

## 4 · Ce que la page fait, écran par écran

1. **Premier écran** (noir) — le rail des cinq sens en haut de page, le nom, le métier, les deux
   quartiers, une phrase de services réels, **une action principale** (WhatsApp) + un appel, puis trois
   preuves : *deux cabinets · numéro d'urgence · livraison à domicile*.
2. **La bande d'arrivage** — décorative (`aria-hidden`), lentement défilante, coupée par
   `prefers-reduced-motion`. Aucune information n'y vit seule.
3. **Nos services, et ce qu'il faut apporter** — six cartes numérotées, chacune avec son « à apporter »
   et une seule action WhatsApp pour toute la section.
4. **Les arrivages** — trois photos, cinq pastilles de famille, une action (« Demander si un modèle est
   en boutique ») et la phrase qui explique **pourquoi aucune marque n'est nommée**.
5. **Les deux cabinets** (noir) — deux cartes, chacune avec SON repère, les horaires annoncés et **son**
   message WhatsApp (les deux messages sont différents : le patient choisit son cabinet dans le message).
6. **Toutes les bourses** — leur mission, quatre preuves (diplôme, 10 ans, livraison, deux cabinets) et
   leur citation en grand.
7. **Les six questions** — ordonnance, horaires, prix, livraison, prothèses, adresses : les six sont dans
   le schéma `FAQPage`, mot pour mot.
8. **Contact** — deux gestes, puis deux utilitaires discrets (copier le numéro, fiche `.vcf`) ; barre
   d'action fixe en bas sur téléphone.

**Mouvement (budget §9)** : une bande en boucle (décor), une entrée par section au défilement
(IntersectionObserver, **jamais** d'écouteur de défilement), deux retours d'état. Un seul
`@media (prefers-reduced-motion:reduce)` arrête **tout**, bande comprise.

## 5 · Les contrôles (24/09 au soir)

| Contrôle | Résultat |
|---|---|
| `audit_html.py` | **0 constat** sur **254 passages** de texte (desktop et mobile) — il a attrapé le kicker du premier écran à **3,06:1** (gris sur noir), corrigé en `--on-dark-2` |
| `audit_a11y.py --strict` | **0 faute A/AA, 0 avertissement** — il a attrapé l'absence des règles `display:none` des deux langues (le lecteur d'écran aurait lu FR **et** EN) |
| `audit_hero.py` | **0 faute, 0 avertissement** |
| `check_inline_js.py` | **rc 0** — 4 blocs compilés |
| `audit_aeo.py` | ✓ `Optician` + `Place` ×2 + `FAQPage` (6 questions) · `noindex` voulu sur une page de travail |
| `audit_images.py` | 0 faute (0 image comptée : les trois photos sont embarquées en base64 — limite connue) |
| `node tools/qa/test_cinqsens_page.mjs` | **48/48** — dont : chaque adresse WhatsApp statique = le texte français **encodé exactement comme le fera le JavaScript** ; les six questions du schéma **mot pour mot** celles de la page ; aucun prix, **aucune marque**, aucun avis, aucun nom inventé ; les horaires affichés mais **hors du schéma** ; la bande d'arrivage **décorative** et arrêtée par `prefers-reduced-motion` ; le script du `<head>` rejoué **avant** le script principal (la page se rouvre bien dans la langue choisie) |
| Poids | **280 Ko** — trois photos à 900 px, qualité 52, tout embarqué |

**Ce qui n'a PAS été fait, et qu'on dit** : aucune capture d'écran, aucun mockup (le bac n'a **pas de
navigateur**). Le premier écran, la bande, l'œil : c'est King, sur un téléphone, en plein jour.
Règle du portique : *« Not verified on a phone = not sent. »*

## 6 · À faire avant d'envoyer le lien (dans cet ordre)

1. **Déployer** `hosting/previews/cinqsens/` (**le dossier entier** : `index.html` **et** `og.jpg`) —
   projet Vercel séparé, par exemple `cinqsens`.
2. **Recoller l'adresse** : `python3 demos/build_cinqsens.py --url https://<adresse>` puis redéployer —
   `og:url` et `og:image` ne se devinent pas.
3. **Ouvrir sur un téléphone** : FR par défaut, bascule EN, un vrai WhatsApp pré-rempli avec le bon
   numéro (696 698 136), la bande qui défile sans saccade, aucun débordement horizontal, barre du bas
   visible.
4. Envoyer **d'abord la carte du lien**, puis le texte de `sales/Send-CINQ-SENS-2026-09-24.md`.

## 7 · Ce qu'on ne dit pas, et ce qu'on ne fera pas

- **Jamais** « vous n'avez pas de page » : ils ont un blog — **arrêté au 15 octobre 2021**. C'est ça,
  l'angle vrai, et il est daté.
- **Jamais** de prix, de marque, d'avis, d'horaire « officiel », de nom de responsable inventé.
- **Aucune promesse** de classement, de délai, de nombre de patients.
- La prothèse oculaire est un sujet sensible : la page en parle **comme d'un métier du cabinet**, jamais
  comme d'une promesse médicale, et renvoie au dossier médical du patient.

## 8 · Passe 2, la même nuit — ce qui a été ajouté, et une phrase retirée

**Ce qui a été ajouté.** ① Une **lueur** dans le premier écran : les cinq teintes du nom très diluées,
qui dérivent lentement sous le texte (`radial-gradient` × 4, `translate3d` seulement, 30 s). Elle est
`aria-hidden`, `pointer-events:none`, tenue **à l'écart du coin haut-gauche** où vivent le surtitre et le
titre — la lisibilité passe avant l'effet — et le bloc `prefers-reduced-motion` l'arrête. ② Le **rail**
entre en scène : les cinq segments grandissent en cascade (0,65 s), une fois, sous `html.js` seulement.
③ Deux **raccourcis de carte**, avec un message qui n'appartient qu'à eux : « Envoyer la photo de mon
ordonnance » (carte 02) et « Écrire au cabinet, en privé » (carte 05 — aucune donnée clinique dans le
message, le patient garde la main). ④ `sameAs` dans les données structurées : le **blog**, **X** et
**LinkedIn** — trois URL vérifiées le 24/09, et rien d'autre. Le profil X confirme au passage le
« numéro d'urgence » écrit sur la page (il le publie dans sa bio, avec les deux numéros).

**Ce qui a été retiré.** La carte « **Accessoires et petites réparations** » et sa liste
« cordes, étuis, produits d'entretien, vis et plaquettes » : la source ne dit que « **accessoires
d'optique** ». Personne ne nous a dit que le cabinet répare, ni ce qu'il a en rayon. Réécrit en
question — « Vous cherchez une corde, un étui, un produit d'entretien ? Dites-le : on vous répond avec ce
que le cabinet a en boutique » — et « À demander » remplace « À apporter ». **Leçon à garder** : quand on
veut rendre une page vivante, la spécificité inventée est la faute la plus facile à commettre. Ce que la
source ne dit pas, la page le demande.

**Deuxième fois le même piège** : une constante JavaScript utilisée **avant** sa déclaration (`ORD`,
`PROTH`) — les audits ne l'ont pas vue, le test l'a attrapée (`ReferenceError`). Règle : les constantes
partagées se déclarent **en haut** du fichier de test, jamais au milieu.

**Contrôles après la passe 2** : `audit_html` **0 constat** (258 passages) · `a11y --strict` **0/0** ·
`hero` **0/0** · `inline_js` rc 0 · `aeo` ✓ · `test_cinqsens_page.mjs` **53/53** (dont : la lueur est
vide et ne capte pas le clic ; le rail et la lueur ne s'animent que sous `html.js` ; le bloc
`prefers-reduced-motion` arrête **les quatre** mouvements ; `sameAs` ne contient **que** les trois
comptes connus ; le raccourci prothèses ne dit rien de clinique). Poids : **278,7 Ko**, dix liens
WhatsApp, trois photos embarquées.
