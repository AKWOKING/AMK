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
