# DM OPTIC — inspiration & Design Read (24/09/2026)

**Le client.** DM Optic (DM OPTIC) — cabinet d'optique médicale à Douala. Titulaire : **M. Domche Noumbi**.
Inscrit au registre ONOC (Littoral, ligne 102) : inscription **021/2016**, arrêté ministériel **0382**,
téléphone **656 122 239**. Il a répondu « **Ok Envoyé svp…** » le 24/09 à 15:54 au message qui proposait
une page.

**Le contrôle approfondi (règle de King, 24/09).** Six recherches avant d'écrire la page — et le résultat
est le sujet même de la page :
1. **nom exact + ville** → « DM Optic »/« DM Optique » Douala : rien d'autre que le registre ;
2. **domaines** → `dmoptique.com` et `dmoptic.com` existent mais ne servent **rien** (réponse vide) ;
   `dmoptique.cm`, `dmoptic.cm`, `dm-optique.cm` : inexistants ;
3. **canaux discrets** → aucun Blogspot, WordPress, YouTube, X, Instagram, Facebook ;
4. **recoupement** → une seule trace : une petite annonce afribobo de **déc. 2019** (« DM optometrie »,
   2 500 F, publiée par un particulier nommé Samuel) — **peut-être pas eux**, non recoupée, donc non
   utilisée comme fait ;
5. **verdict écrit** → « vous n'êtes nulle part » est **vrai** (aucune page, aucun horaire, aucun
   itinéraire) ; en revanche **aucune adresse ni horaire n'a pu être trouvée** → ils ne sont pas
   inventés, ils deviennent des champs « à confirmer » ;
6. **page dédiée ?** → non, donc **pas d'écartement**.
   Point de crédibilité supplémentaire, trouvé en 4 : le nom de **Domche Noumbi** apparaît en
   **mars 2023** dans la liste des opticiens de Douala cités par la presse de la profession
   (*Echos Santé*, article sur l'Ordre national des opticiens) — fait public, daté, attribué.

---

## Les références (angles différents, toutes ouvertes le 24/09/2026)

### 1 · `styles.refero.design` (donnée par King) — l'angle **couleur + typographie**
Bibliothèque de styles réels décrits en une ligne. Trois lignes ont servi de repère :
« **Brex — White concrete, single ember** », « **Vercel — Typeset terminal on white paper** »,
« **teenage engineering — Industrial catalogue under studio light** ».
- **Ce que je prends** : une **surface neutre froide + un seul accent**, et une page **conduite par la
  typographie, les filets et les chiffres** plutôt que par l'image ; le fait de **nommer le style en une
  phrase** avant de coder.
- **Ce que je rejette** : « **Linear — midnight precision instrument** » (le mode sombre ; Cavisa est
  déjà la page opticien sombre, et un patient lit cette page **dehors, en plein jour**) ; les directions
  néon/violet.

### 2 · `motionsites.ai` (donnée par King) — l'angle **mouvement**
Galerie de premiers écrans animés (« hero sections »).
- **Ce que je prends** : **un seul moment d'entrée** dans le premier écran — la carte d'identité du
  cabinet qui se pose, et l'anneau de verre qui se trace (700 ms, une fois) ; les sections ensuite
  apparaissent une par une, sans chorégraphie.
- **Ce que je rejette** : les fonds 3D/canvas, les vidéos de fond (notre marché est en 3G), les
  recettes « AI landing page » (halo + bento + faux compteurs).

### 3 · `ui.aceternity.com` (donnée par King) — l'angle **composants / interaction**
Catalogue de composants (React) avec micro-interactions.
- **Ce que je prends** : deux idées transposées en CSS vanilla — la **carte qui se soulève vers le
  pointeur** (uniquement souris, `(hover:hover) and (pointer:fine)`) et le **bouton magnétique** sur
  l'action principale (dérive de quelques pixels, jamais sur téléphone).
- **Ce que je rejette** : la pile React/Tailwind/`motion` (nous livrons **un seul fichier**),
  les shaders, les nuages, le bento de neuf cases, les marquees.

### 4 · `aceandtate.com` (marché voisin, optique) — l'angle **structure**
- **Ce que je prends** : « **Find a store** » traité comme un bloc de premier rang, et **WhatsApp comme
  vrai canal de contact** (ils publient un `wa.me` dans leur pied de page) ; les services ont leur
  propre entrée de navigation.
- **Ce que je rejette** : la grille e-commerce de montures (nous n'avons **ni catalogue ni prix**, et
  aucune monture n'est à nous), la capture d'e-mail, les pavés de langue.

---

## Design Read (à dire avant la première ligne de HTML)

> **Reading this as:** a one-page shopfront **preview** for a Douala optician that exists off the web,
> for a patient searching from a phone — with a **precise-and-warm** language (an instrument, not an
> advertisement), leaning toward **« la carte »**: the practice's real registration rendered as an
> elegant credential card in the first screen, cool paper + deep navy, **one ember signal** used once
> (on what is missing), Schibsted Grotesk + IBM Plex Sans, mono on registry fields, no invented faces.

**Les trois directions explorées avant de coder (§19.3) et le verdict** — détail dans
`clients/dm-optic/build-notes.md` :
- **A · LA CARTE** (retenue) — le seul actif vérifié du client (son inscription à l'Ordre) devient
  l'objet du premier écran ; l'histoire « introuvable → trouvable » se raconte en une bande sombre.
- **B · L'INSTRUMENT** (écartée) — catalogue technique à la teenage engineering : trop proche du
  registre « mesure » du **Cristallin** (papier froid, étiquettes mono).
- **C · L'ENSEIGNE** (écartée) — bleu de travail + vermillon, typographie d'enseigne peinte : risque
  « vieux commerce », et King a déjà refusé une imagerie d'époque pour Douala.

**Ce qui différencie la page des quatre autres opticiens du dépôt (≥ 4 axes) :** archétype (carte
d'identification + bande « hier / maintenant ») · palette (papier froid + marine profond + un braise,
aucun ambre) · typographie (Schibsted Grotesk / IBM Plex Sans / IBM Plex Mono) · traitement d'image
(aucun visage, deux natures mortes d'instruments, jamais de texte sur la photo) · ton (l'aveu :
« le registre vous connaît, le web non »).

---

## Second passage (24/09, soir) — **comment écrivent les vrais opticiens**

Retour de King : *« on parlait aussi de listé ces services et montré ses montures et lunettes au
patient »* et *« look for optic clinics and shop on the Web to see how they showcase and write on their
sites »*. Trois recherches, et **deux sites lus en entier** — pas des listicles : des boutiques
indépendantes.

**Ce qu'ils font tous, et qu'on a repris :**

| Ce qu'on voit chez eux | Chez nous (v2.1) |
|---|---|
| Un titre qui dit le métier **et** la ville, puis un positionnement en une phrase (« Des lunettes à votre image, tout simplement » — L'Opticien Angers ; « Pour trouver lunettes à son nez, Rennes a son adresse » — Optique BJ) | « DM OPTIC, votre opticien à Douala. », puis « Lunettes de vue, lunettes de soleil, montures pour enfants… » |
| Une section **« Nos services »** qui liste des gestes, pas des produits (examen de la vue · choix de montures · montage · ajustement · réparation — Optique BJ) | « **Nos services, et ce qu'il faut apporter** » : six services, chacun avec la liste de ce qu'on apporte |
| Une **vitrine des montures** par familles, avec une photo et un mot sur chacune (« Lunetterie, opticien visagiste » — Queen Optique ; « Des montures qui ont du caractère » — Optique BJ) | « **Les montures et les lunettes** » : trois familles (vue · soleil · enfants), une photo et un conseil chacune |
| L'**essayage** comme argument, pas comme option | « elles s'essayent au cabinet, sur votre visage, avec quelqu'un qui vous regarde — pas sur un écran » |
| Un conseil qui nomme la **forme du visage** et le **réglage** (Queen Optique : « opticiens visagistes ») | trois conseils : la forme du visage · la largeur et l'appui · ce que vous en faites |
| **Aucun prix affiché**, la question renvoyée à la boutique | sixième question fréquente (« Combien coûte une paire de lunettes ? ») → la réponse utile, pas un tarif inventé |

**Ce qu'ils font et qu'on n'a PAS copié — avec la raison :**

- **Les marques** (Optique BJ nomme six marques françaises, une page chacune ; Optic Duroc « toutes nos
  marques ») : nous n'avons **aucune** liste pour DM OPTIC → la vitrine ne nomme rien, et la page dit
  « Vous cherchez une marque précise ? Demandez-la : la réponse arrive dans la conversation WhatsApp ».
  On n'invente pas un portefeuille de marques.
- **Les avis clients** (Optique BJ : Mathilde T., Jérôme L., Inès M., cinq étoiles) : interdits tant
  qu'ils ne viennent pas de vrais patients. On en a **zéro** → zéro avis sur la page.
- **La promesse de délai** (« votre monture, vos verres, prêtes en 1 heure » — Queen Optique) : elle
  suppose une banque de verres et un atelier de taillage qu'on n'a pas vus. On ne promet pas le délai
  d'un autre.
- **Le rendez-vous en ligne** (Doctolib, formulaires) : le cabinet n'a pas d'agenda en ligne. Les deux
  gestes restent WhatsApp et le téléphone — ceux qu'il utilise vraiment.

**Sources lues** : `queenoptique.com` (Montréal — deux univers, adultes + Kidoptiks) et `optiquebj.com`
(Rennes — trois cartes de services, six marques, avis, accès) ; structures relevées chez
`lopticien-angers.com`, `lopticien-nantes.com`, `monoptique-opticien.com`, `opticduroc.com`,
`lopticien.ca`, `generale-optique.com`, `optoplus.com` ; guides `madebyevoke.com`, `imatrix.com`,
`optifyonline.com`, `webdesignstudio.london`. Tous disent la même chose : **la section montures est le
différenciateur d'un opticien indépendant**, et l'accueil doit porter le nom, la ville, une liste de
services explicite — et un bouton toujours visible.

---

## Troisième passage (20/10/2026) — **les catalogues**, pour l'architecture v2

Commande King : revue design/structure avec les vraies photos. Agent Reach tentée d'abord (§1f① :
doctor OK, `gh` muet, Jina HTTP 000 → repli natif déclaré). Références lues en direct :

### 5 · `warbyparker.com/eyeglasses/women` — l'angle **structure de catalogue**
238 montures ; filtres repliés (« Shop by · Shape · Frame width »), compteur de résultats visible ;
la carte porte **plusieurs coloris en vignettes**, le nom, « Similar frames », « Try on » ; fiche par
monture `/eyeglasses/<modèle>/<coloris>`. Taxonomie formes : cat-eye · square · round · oval ·
rectangle · geometric · aviator (notre §6 en est proche).
- **Pris** : compteurs, similaires sur la fiche, angles/coloris dans la carte, URL par monture.
- **Rejeté** : prix partout, essayage virtuel, panier, quiz — hors périmètre (brief §6).

### 6 · `aceandtate.com/gb/glasses` — l'angle **navigation + imagerie**
Nav de premier niveau : Glasses · Sunglasses · Services · **Eye test** · Stores — l'examen est une
**entrée**, pas une section. 430 montures, filtres Frame shapes / Frame width / Colours ; carte =
**photo à plat + photo portée** ; blocs de campagne **insérés dans la grille**.
- **Pris** : page examen dédiée et liée dès la nav ; deux images par carte (chez nous : deux
  **angles**, pas de visage porté sans accord) ; blocs éditoriaux dans la grille (nos trois conseils).
- **Rejeté** : prix « starting from », bundles/promos, wishlist, comptes.

### 7 · Baymard Institute (Product List & Filtering UX, 2025-26) — l'angle **preuve d'usage**
Listes médiocres = **67–90 % d'abandon**, outillage correct = 17–33 %. Règles reprises dans
`SPEC-PAGES-v1.md` §10.1 : compteurs par option, OU/ET, chips de filtres appliqués, mobile =
bouton collant + panneau + « Afficher X résultats », un filtre pour chaque attribut montré sur la
carte, étiquettes littérales courtes. **Rejeté** : leurs patterns e-commerce (tri prix, dispo,
livraison) — sans objet ici.

### 8 · Google Search Central (documentation officielle) — l'angle **SEO des filtres**
*Managing crawling of faceted navigation URLs* + blog 12/2024 : les facettes créent des espaces
d'URL quasi infinis ; soit les bloquer (robots.txt), soit utiliser des **fragments `#`** que les
moteurs ignorent ; indexer les **listes propres + les fiches**. À notre échelle (~50 pages) le
budget de crawl n'est pas le sujet ; les doublons minces, si.
- **Pris** : filtres JS + fragments (aucune URL paramétrée), canoniques propres, sitemap limité
  aux pages qui comptent. **Rejeté** : toute facette indexable « au cas où ».

**Design Read v2 (à confirmer par le choix de direction)** : la même identité (« cachet & braise »,
Schibsted/Plex, la carte) ; ce qui change = la **profondeur** (catégories, fiches, examen, cabinet)
et la **matière** (vraies photos détourées sur crème chaud, vrais murs du cabinet). Trois directions
de composition écrites dans `SPEC-PAGES-v1.md` §10.3 — D1 continuité, D2 vitrine réelle
(recommandée), D3 parcours. Unicité vérifiée contre le registre : aucune ne rejoue La Ligne
(visages/portraits), Cinq Sens (affiche), Cristallin (mesure) ni l'Instrument écarté en v1.

---

## Quatrième passage (20/10/2026) — **corriger les FAIL de la revue taste**, sans toucher l'identité

Commande King : revue taste de la v2, puis recherche de correctifs. Agent Reach tentée d'abord
(doctor OK, Exa hors-ligne TLS → repli natif déclaré, comme au 3ᵉ passage). Sources lues en direct :

### 9 · Baymard Institute, *Product Page UX 2026* — l'angle **fiche produit**
Benchmark 2026 : 52 % des fiches desktop et 62 % des fiches mobiles des grands sites restent
« médiocres ou pires ». Constante des correctifs qui marchent : **galerie + panneau d'information
avec l'action principale visible sans défiler** (collante sur mobile), spécifications près de
l'action, jamais l'action sous une image d'un écran de haut.
- **Pris** : fiche DM en deux colonnes ≥980 px (galerie · faits + WhatsApp visibles), CTA mobile
  après la première image. C'est le correctif A4 de `build-notes.md`.
- **Rejeté** : prix, avis/étoiles, urgence, variantes achetables — hors verrous (pas de prix,
  pas d'avis inventés, WhatsApp est notre « panier »).

### 10 · NN/g, *Photos as Web Content* (eyetracking) — l'angle **photos réelles vs stock**
Les images purement décoratives sont **ignorées** ; les photos du produit réel et des personnes
réelles sont **scrutées**. « Decorated means ignored. »
- **Pris** : remplacer les images stock de l'accueil (`dmoptic-*.webp`, légendées « Photo
  d'illustration ») par les vraies montures du catalogue et la vraie photo du cabinet (A8) — ça
  rejoint notre verrou « le site ne montre que du vrai ». Exception honnête : la carte « Lunettes
  de soleil » (aucune solaire réelle photographiée à ce jour).
- **Rejeté** : toute photo « d'ambiance » de banque d'images pour combler — c'est exactement ce
  que l'étude dit invisible, et ce que le brief interdit.

### 11 · `aceandtate.com/gb/eye-test` lue en direct — l'angle **page examen**
Vidéo d'ouverture, liste de signes (« It's time for an eye test if: … »), processus raconté en
**4 photos**, FAQ, CTA de réservation répété à chaque section.
- **Pris** : notre page examen (0 image, FAIL `few-pictures`) gagne la photo réelle de la salle/
  du cabinet (A7) ; la liste de signes est un bon dispositif d'auto-reconnaissance — mais c'est
  du **texte nouveau à faire valider** (client/King), pas à copier tel quel.
- **Rejeté** : réservation en ligne, « examen gratuit », prix, promesses — inexistants ou
  interdits chez DM.

### 12 · Consensus corps de texte ≥ 16 px (Google Fonts Knowledge ; revues d'accessibilité 2025-26) — l'angle **lisibilité**
WCAG n'impose pas de minimum, mais la pratique converge : 16 px plancher pour le texte courant,
12–13 px admis pour libellés courts. Chez nous le corps est à 17 px mais les paragraphes de
cartes vivent à 15,2 px et les libellés à ~11,5 px.
- **Pris** : `--fs-sm` → 1rem, `--fs-label` → .8125rem (A5). Argument décisif ici : le public
  d'un opticien est précisément celui qui lit mal le petit texte.
- **Rejeté** : gonfler toute l'échelle — seuls les deux jetons fautifs bougent.

**Design Read (revue)** : l'identité « cachet & braise » n'est pas le problème ; les FAIL se
scindent en défauts objectifs (marges mobiles, CTA enterrés, photos stock, petit texte) —
correctifs ci-dessus, consignés classe A dans `build-notes.md` — et en dispositifs d'identité que
le skill bannit par principe (classe B) : **ruling King avant tout geste**.
