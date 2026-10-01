# Cavisa Optique — inspiration & Design Read

**Client :** Cavisa Optique · Douala (Cameroun) · titulaire **M. DONGMO Jean René** · WhatsApp **699 95 90 52**
**Demande de King, 24/09 :** *« Cavisa optique said yes for the demo so it's time to build him a website tailored for him and that makes his client want to book »* — inspiration imposée : `https://godly.design/website/superpower/`.
**Date de la lecture :** 24/09/2026 · veille faite en direct (jamais de mémoire), `PRE-FLIGHT.md` §2.

---

## 0 · Ce que la veille a établi sur Cavisa (avant toute ligne de HTML)

| Fait | Source / instrument | Conséquence pour la page |
|---|---|---|
| **Google Maps ne trouve pas « Cavisa Optique Douala »** — la fiche n'existe pas (`Google Maps can't find …`, + « Add a missing place ») | `google.com/maps/search/Cavisa+Optique+Douala`, lu le 24/09 | Le patient qui cherche sur son téléphone ne trouve **rien**, même pas une épingle. La page doit être **le** point d'entrée, et c'est un argument à montrer à M. Dongmo. |
| La seule page au monde portant son nom est **vide** (`opticalconsulting.fr/receptacle/cavisa-optique/`, hébergée chez un cabinet de conseil optique français) | vérifié le 24/09 (lot 1) | Le hook du message d'origine — jamais recopié dans la page : **on ne dit pas au patient que la boutique n'existe pas**. |
| Aucune adresse, aucun horaire vérifiable | registre ONOC + Maps (rien) | **La page n'invente ni adresse ni horaires** : deux lignes « à confirmer » dans un encadré clair, adressées à la boutique. |
| Numéro WhatsApp **vérifié sur l'application par King** (profil « CAVISA OPTIQUE ») | capture du 24/09, 12:10 | C'est le numéro des CTA, avec indicatif +237. C'est le numéro public **si M. Dongmo le valide**. |
| Le « n° 103 » lu dans l'annuaire ONOC est un **numéro de ligne du tableau** (186 lignes), pas un numéro d'inscription | relecture du tableau | **Il ne s'affiche pas** comme numéro d'ordre. Aucun statut administratif n'est commenté dans la page. |

---

## 1 · Référence ① — structure / mise en page (imposée par King)

**`https://godly.design/website/superpower/` → le site réel est `https://superpower.com`** (Health & Fitness ; « 150+ biomarker lab tests/year », HSA/FSA). La page Godly ne porte que les captures (`cdn.godly.design/sites/superpower/{desktop-full,mobile-full,hero-*,pricing-*,cta-*}.png`), le site, lui, se lit live.

**Ce qu'on prend (relevé sur la page réelle, chunk 0) :**
1. **Hero = promesse + réassurance + 2 portes.** H1 court, puce de réassurance (« HSA/FSA eligible »), sous-titre chiffré, **deux CTA** (le grand, puis le « voir ce qu'on teste »).
2. **Rangée de preuves sous les CTA** (4 blocs courts + 3 visages) — la preuve vient *après* la promesse, jamais dedans (§26.1.4).
3. **« How it works » en 4 étapes numérotées**, chacune avec une image : le patient voit le chemin avant de s'engager.
4. **Un encadré de comparaison chiffré** (« What could cost $10,000 is now $349 ») : la réponse à « combien ça va me coûter » posée au milieu de la page, pas dans une FAQ planquée.
5. **FAQ en accordéons** + carrousel d'experts nommés (la crédibilité par les personnes).

**Ce qu'on rejette :** les **chiffres de marque** (150+, 1 000+, 6M+, $349/an, prêt à 0 %) — aucun n'est transposable à un opticien de Douala dont on ne connaît ni les prix ni le volume ; le **bandeau de logos** Stanford/Harvard/Oxford (aucun équivalent, et l'inventer serait un mensonge) ; le **carrousel d'experts** (Cavisa est seul) ; les **avatars** de clients (nous n'avons ni photos ni avis) ; le mot « membership » et la mécanique d'abonnement.

**Transposition, pas copie :** structure promise → preuves → chemin en 4 étapes → réponse au coût → FAQ, **avec 0 chiffre inventé**. L'encadré de comparaison devient **« Aucune surprise avant de vous déplacer »** : ce que le patient saura *avant* de sortir de chez lui.

---

## 2 · Référence ② — contenu / réservation (angle patient qui hésite)

**`https://warbyparker.com/eye-exams`** (lu le 24/09).

**Ce qu'on prend :** le hero posé en **question** (« Need to get your eyes checked? ») juste avant le bouton de réservation ; **« What to expect » en liste** (7 items) qui retire l'anxiété du premier rendez-vous ; la **crédibilité par les personnes** (les optométristes) ; **le bloc paiement/assurance** (« When it comes time to pay ») qui répond au vrai frein ; le **renouvellement sans revenir**.

**Ce qu'on rejette :** les prix ($85, assurance −$140, FSA/HSA) — Cavisa ne publie aucun prix et nous n'en inventons aucun ; le **parcours de réservation en ligne à créneaux** (pas d'agenda vérifié, pas de logiciel) ; le renouvellement par iPhone ; les 7 items de « what to expect » qui décrivent un examen médical **que nous n'avons pas vérifié chez Cavisa**.

**Transposition :** la liste « what to expect » devient **« Ce qu'il faut apporter »** (ordonnance · ancienne monture · une photo si réparation) ; le bloc paiement devient **« Aucune surprise avant de vous déplacer »** ; la question du hero devient la question du patient, avec une porte unique : **WhatsApp**.

---

## 3 · Référence ③ — couleur, typographie, images, ton (le marché réel + le ton chaleureux)

**a) Le marché de Douala, lu en direct — `https://www.cristalysoptic.com`** (opticien vivant, Bonapriso + Bonamoussadi, depuis 2003) : la page se lit comme **une carte de visite** — deux adresses, quatre numéros, deux e-mails, « Trouvez-nous sur Google Map ». Aucun visage, aucune monture, aucune phrase pour donner envie d'entrer. *(Recherche qui a échoué le 24/09 : `lyfyoptic.com` ne se laisse pas lire ; la liste « Best Optometrist Websites » de Colorlib est morte — URL 404. Je ne prétends rien sur ces deux-là.)*

**b) Le ton chaleureux, photo-first — `https://spectaclepdx.com`** (boutique indépendante, Portland) : logo blanc posé sur fond sombre, **photos de vraies personnes** (le personnel, la patiente au comptoir), sections qui donnent *une raison de venir* (« Doctors Who Spend Time With You », « Frame and Lens Expertise »), galerie de photos clients.

**Ce qu'on prend :** les **vraies personnes en photo**, le **fond sombre assumé** où une seule couleur conduit l'œil, et l'idée que la boutique se raconte par ce qu'elle fait de ses mains (essayer, ajuster) — pas par une liste de marques.
**Ce qu'on rejette :** les superlatifs non vérifiables (« industry-leading », « twice as much time », « technology invested »), la galerie de clients (nous n'avons aucun avis Cavisa), la longueur américaine, le catalogue e-commerce.
**Ce que la veille locale justifie :** à Douala, les opticiens en ligne sont **clairs et génériques** (carte de visite). Une **page sombre et chaude**, avec de vrais visages et une porte WhatsApp, ne ressemble à personne — et ce n'est pas une couleur posée au hasard : c'est le comptoir éclairé d'une boutique, vu du trottoir.

---

## 4 · Design Read (écrit avant la première ligne de HTML — `PRE-FLIGHT.md` §2.5)

> **Reading this as:** a local optician's landing page for a Douala patient who needs glasses and hesitates to push the door, with a warm, **night-lit** language (Superpower's promise-first structure transposed, Warby Parker's "what to expect" turned into "what to bring"), leaning toward **Black and Tan** — warm off-black ground `#14100D`, a single amber `#E9A544`, warm ivory `#F7EDE1` — **Instrument Serif** display on **Karla** body, one recurring **lens rim**, and a **WhatsApp-first** booking door. **Zero invented price, zero invented number, zero invented review.**

**Les trois dials (§2) :**

| Dial | Valeur | Pourquoi |
|---|---|---|
| DESIGN_VARIANCE | **5** | Décalage mesuré : hero texte/photo, un panneau-figure qui déborde, une bande de parcours plus claire. Rien d'asymétrique au point de perdre un patient pressé. |
| MOTION_INTENSITY | **4** | Révélations au défilement + états pressés. Aucune chorégraphie : le marché est un téléphone, souvent en 3G. |
| VISUAL_DENSITY | **4** | Une idée par écran, sections larges, une seule couleur d'action. |

**Différenciation, ≥ 4 axes, contre `clients/_uniqueness-registry.md`** (les trois lignes opticien existantes : Univers = dossier administratif papier chaud · Le Cristallin = acuity chart, papier froid, vert · L'Opticien = miroir dessiné, ink-teal/ambre/crème) :

1. **Archétype de mise en page** — *la promenade au comptoir* : la page descend dans la boutique de nuit (hero + panneau-verre → 4 cartes → parcours en 4 étapes sur bande surélevée → ordonnance → encadré « aucune surprise » → carte claire « deux lignes à compléter » → accordéons → la porte WhatsApp). Ni fiche (UNI-LABO), ni dossier (Univers), ni échelle d'acuité (Cristallin), ni miroir (L'Opticien).
2. **Palette** — **Black & Tan** du pool §6.2 : off-black chaud `#14100D` · ambre unique `#E9A544` · ivoire chaud `#F7EDE1` · vert WhatsApp `#0C7F41` réservé aux envois. **Aucune ligne opticien de la registre n'est sombre et chaude** ; famille jamais utilisée dans la registre.
3. **Typographie** — **Instrument Serif** (display, 400 + italique) sur **Karla** (400/500/700). Personne n'utilise ce couple : Univers = Bricolage Grotesque, Cristallin = Archivo, L'Opticien = Fraunces (serif souple, ronde) — ici un serif éditorial à fort contraste, tenu serré.
4. **Traitement des images** — **deux photographies**, chaudes, chacune **encadrée comme un verre** (anneau + halo), légendées « mise en situation ». Pas de charte d'acuité, pas de miroir dessiné, pas de photo de stock aseptisée.
5. **Ton de copie** — la voix du boutiquier, tutoiement interdit, phrases courtes, **aucun chiffre** : pas un prix, pas un délai, pas une note, pas un avis. Là où Superpower chiffre, nous **décrivons le geste** (« on vous dit franchement ce qui va »).

**Le « star of the show » (§23.3) et sa rime :** **le verre** — la photo du hero est encadrée comme un verre de lunettes (anneau ambre + reflet en biais), et un composant de ce verre (l'anneau) revient à trois endroits : la puce du hero, les numéros d'étape, et la carte claire « à compléter ». C'est l'objet du métier, pas une décoration : il dit « ici, on regarde à travers du verre ».

**L'ancrage typographique (§23.4) :** l'en-tête a été choisi **en premier** (Instrument Serif, sur le mot « monture ») ; le corps (Karla) n'a été choisi qu'après.

---

## 5 · Ce que la page ne fait pas, et pourquoi (garde-fous de la veille)

- **Aucun prix, aucun délai, aucune note, aucun avis, aucun nombre.** Rien de ce que Cavisa n'a pas publié.
- **Aucune adresse, aucun horaire inventé** : deux emplacements marqués « à confirmer ».
- **Aucune promesse médicale** : la page ne dit pas que la boutique fait des examens de la vue (non vérifié). Elle traite l'ordonnance, la monture, les verres, la réparation.
- **Aucune mention du statut administratif** ni du numéro de ligne du tableau ONOC.
- **Aucun nom d'un autre opticien**, aucune comparaison avec un concurrent.
- Les deux photos sont **des mises en situation générées** (pas la boutique de Cavisa) : c'est écrit sous chacune, et remplacé par ses vraies photos dès qu'il en fournit.
