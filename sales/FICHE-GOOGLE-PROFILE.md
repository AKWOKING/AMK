# La fiche Google — ce que trois vidéos ont appris, et ce qu'on en fait

**Date** : 24/09/2026 · **Origine** : quatre liens de King, trois sur la fiche Google, un sur l'accessibilité
(→ `AMK-DESIGN-SKILLS.md` §30 pour les règles de design et `tools/qa/audit_a11y.py` pour ce qui est
devenu mécanique).

**Sources lues** — toutes parlantes, lues en entier :

| vidéo | auteur | ce qu'elle est |
|---|---|---|
| `TNrsBxxkjbA` | **Santrel Media** (1,13 M d'abonnés) | l'installation pas à pas, en direct, écran partagé |
| `-k42Q0JTYVc` | **Ignite Visibility** (64,9 K, agence américaine) | 20 points de contrôle énumérés vite, sans démo |
| `53YetCLm1YY` | **Zanet Design** (36,2 K, « 27 ans à aider des petites entreprises ») | une compilation : installation, performance, avis, suspension, classement |
| `h0ekMnui2Hg` | **Imran Siddiq — Web Squadron** (195 K) | l'accessibilité, en démonstration |

Ces trois-là se recoupent largement (l'installation est la même chez les trois). **Ce document ne garde que
ce qu'elles confirment ensemble, plus deux apports qu'une seule donne** — et il marque ce qui reste à
vérifier pour le Cameroun, parce que les trois sont américaines ou britanniques.

---

## 1 · Le fait qui nous concerne directement

Dans la vidéo d'installation, Santrel dit une phrase en passant, et c'est la plus importante du lot — nous
vendons un site :

> « Beaucoup de gens, quand ils naviguent sur Google Maps, cliquent presque toujours sur le lien du site. »

Zanet dit la même chose par l'autre bout : **70 % de ce que Google sert à un client ne passe plus par le
site** (avis, horaires, photos, questions) — mais quand le client décide d'en savoir plus, c'est le lien du
site qu'il ouvre. Les deux moitiés de notre offre se tiennent donc : **le profil est la porte, le site est
la pièce**. Un site sans profil n'est pas trouvé ; un profil dont le champ « site web » est vide envoie le
client… nulle part.

**Et ce cas, nous l'avons déjà dans le pipeline, preuve en main** : la fiche Google d'**Univers Optique**
porte une note (3,3/5, 6 avis) et son champ « site web » est **vide**, pendant que son domaine ne répond
plus depuis janvier 2024 (`leads/records/univers-optique.md`, contradiction M2). Nous le voyons vendredi
25/09 à 10 h — et « a-t-il la main sur sa fiche ? » est déjà l'un des six points à trancher en séance. Ce
document dit quoi faire de sa réponse.

*Note de méthode : j'avais d'abord écrit ici que UNI-LABO avait une fiche Google « trouvée par notre relevé
Maps ». C'est faux — la ligne du CRM dit `source : directory` (Remote-Sweep section C), et la vignette
`07-unilabo.jpg` est notre propre maquette, pas une capture de fiche. Écrit ici plutôt qu'effacé : une
affirmation non prouvée qui disparaît sans trace revient toujours.*

---

## 2 · L'installation, dans l'ordre (le seul passage à refaire une fois par client)

1. **Chercher d'abord sur Google Maps.** Si la fiche existe déjà, on la **revendique** ; on ne crée pas un
   doublon. Les trois vidéos insistent : un doublon est le chemin le plus court vers la suspension.
2. **Un compte Google professionnel** (jamais le compte personnel du gérant) — Santrel et Zanet le disent
   tous les deux.
3. **Type d'établissement** : *commerce local* pour ce que nous faisons (laboratoire, clinique, école) —
   c'est ce qui ouvre les horaires, l'itinéraire, l'affluence. *Zone de service* est pour les métiers qui
   se déplacent. **Ne pas tricher sur la zone** : les trois vidéos décrivent les gens qui déclarent un
   rayon de 3 ou 4 heures pour apparaître partout ; Google vérifie, et c'est une cause de suspension.
4. **La catégorie principale est le plus gros facteur de classement** (Zanet, sans hésiter). Sa méthode,
   utilisable tout de suite : ouvrir Google Maps, regarder **les catégories des concurrents du quartier**.
5. **Le nom réel, rien d'autre.** Pas de mots-clés collés au nom — Google sanctionne et les concurrents
   signalent (Zanet). Pour nous c'est la même règle que partout : on n'écrit pas ce qui n'est pas vrai.
6. **Les horaires vrais.** On classe un peu mieux quand on est ouvert, mais « 24 h/24 » inventé est à la
   fois suspect pour le client et passible de suspension. Nos horaires UNI-LABO sont ceux du laboratoire :
   lun-ven 07h-19h, sam 07h-13h.
7. **La description (750 caractères)** : services, quartiers desservis, et ce qui est **vérifiable**
   (depuis quand, par qui, quelle spécialité). Rien d'inventé — c'est notre règle depuis le premier jour.
8. **Les photos** : le lieu, l'équipe, le travail réel. Au moins cinq ou six au départ ; la photo de façade
   est la première chose vue sur Maps. Zanet donne une astuce de recherche honnête : taper « *métier + son
   quartier* » dans Google Images pour voir **ce que Google met en avant**, et photographier son propre
   équivalent (pas copier la photo).
9. **La « date d'ouverture »** : un champ que presque personne ne remplit et qui parle de l'ancienneté de
   la maison. Gratuit, et il alimente la confiance.
10. **Vérification** : par téléphone, par courrier, ou en vidéo. Le client seul peut la faire (code SMS ou
    vidéo de sa porte) — **c'est la limite de ce que nous pouvons faire à sa place**.

---

## 3 · Le chat : SMS et WhatsApp — le point le plus utile pour nos clients

Zanet documente un détail que nous pouvons vendre sans mentir : Google a retiré son chat, puis l'a remplacé
par **SMS et WhatsApp** dans le profil. Et il donne la règle technique exacte :

- SMS : le numéro de mobile, indicatif pays.
- **WhatsApp : il ne faut PAS saisir le numéro** — il faut coller un **lien `https://wa.me/<numéro sans
  zéro>`**, sinon ça ne marche pas.

Nous produisons déjà exactement ce lien partout (`wa.me/237696139819` pour UNI-LABO). Pour un commerce
camerounais, dont le téléphone à douane est souvent la ligne fixe et dont le vrai canal est WhatsApp,
c'est le complément logique de ce que nos pages font déjà.

---

## 4 · Les treize pièges qui font suspendre une fiche

C'est Zanet qui les énumère ; ils sont surtout des pièges que **nous** pourrions tendre à un client par
excès de zèle :

1. mots-clés dans le nom de l'entreprise · 2. adresse fictive (boîte postale, domicile) · 3. horaires
faux · 4. changements répétés de nom, adresse ou téléphone · 5. secteurs très surveillés (plombiers,
serruriers, avocats — la santé est plus calme) · 6. services qui se recouvrent entre deux fiches ·
7. **deux fiches pour la même entreprise** · 8. site piraté ou malveillant · 9. compte Google au
passé douteux · 10. **le même numéro de téléphone sur plusieurs établissements** · 11. avis payés ou
récompensés · 12. violation des conditions d'un autre produit Google (Ads, annonces locales) ·
13. entreprise en ligne sans service en personne.

À retenir pour nos clients à deux numéros (fixe + WhatsApp, comme UNI-LABO) : le **10** est le piège
réaliste — un seul numéro sur une fiche, l'autre dans le champ prévu. Et le **11** est notre ligne rouge
à nous : voir le §6.

---

## 5 · Ce que Google utilise vraiment dans les avis

Zanet le formule mieux que les deux autres (« percée numéro un ») :

- Google se sert de **ce que les clients écrivent**, pas de ce que le commerçant répond. Écrire ses
  mots-clés dans une réponse ne sert donc à rien — et ça se voit.
- **Un avis frais pèse plus que des mois de travail** sur le reste. La demande doit donc arriver **au
  moment où le client est content, en face**, pas « plus tard par message » (Zanet raconte l'hôtel qui
  demande le téléphone du client et montre l'écran : des centaines d'avis par jour).
- Un avis **avec photo ou vidéo** vaut environ dix fois un avis de texte. Pour un laboratoire, un patient
  ne photographiera pas sa prise de sang — mais il peut photographier l'accueil, et l'équipe peut
  demander l'autorisation, jamais l'imposer.
- **Ne pas répondre à un faux avis** : le signaler. Répondre revient à dire « j'accepte ».
- **Répondre aux vrais, y compris les mauvais** : c'est ce que lisent les clients suivants.

### Notre ligne, qui n'est pas exactement la leur

Les trois vidéos poussent à orienter le vocabulaire de l'avis (« faites-leur dire *service rapide*,
*résultat fiable* »). **Nous ne dictons pas le texte d'un avis.** Nous demandons l'avis, nous montrons
comment faire, et c'est tout : dès qu'on souffle les mots, l'avis devient à moitié le nôtre, et un faux
témoignage est interdit chez nous depuis le premier jour. **Jamais d'avis acheté, jamais de remise en
échange d'un avis, jamais d'avis écrit pour le compte d'un client.** Nous n'avons d'ailleurs pas d'avis
à nous : nous ne demanderons donc jamais à un prospect de nous croire sur parole, seulement d'ouvrir une
page.

---

## 6 · Ce que nous pouvons faire, et ce qui appartient au client

| nous | le client |
|---|---|
| trouver la fiche existante, lister ce qui manque | créer/reprendre son compte Google |
| rédiger la description, les services, les horaires à partir de **ses** informations | donner le code SMS de vérification |
| préparer les photos (cadrage, recadrage, poids) | fournir les photos réelles, autoriser leur usage |
| fabriquer et coller le lien `wa.me` du chat | donner le numéro à publier |
| vérifier que le lien du site pointe vers la page en ligne | retirer le `noindex` le jour du déploiement |
| expliquer comment demander un avis sur place | demander l'avis à ses clients |

Zanet montre aussi où l'on **délègue la gestion** : *trois points → paramètres du profil → personnes et
accès*. Si un client veut que nous tenions sa fiche, cela passe par là, avec son accord explicite.

---

## 7 · Ce que je n'ai pas vérifié, et que je n'écrirai donc pas dans une offre

Ces vidéos sont **américaines et britanniques**. Écrire ces règles dans une proposition serait un
faux témoignage de plus. À vérifier sur une vraie fiche camerounaise avant de promettre quoi que ce soit :

- quelles **méthodes de vérification** existent réellement ici (le courrier de Google à Douala, la vidéo) ;
- si **SMS et WhatsApp** sont proposés dans les profils du pays ;
- quelles **catégories** existent en français pour un laboratoire, une clinique, une école ;
- l'existence et la forme du tableau de **performance** (« donut ») pour un compte non revendiqué.

Et deux choses que nous ne vendons pas, faute de pouvoir les mesurer honnêtement : un **classement
garanti** et du « **référencement local** » comme service à part. Nous savons tenir une fiche propre ; nous
ne savons pas promettre une position dans les trois premiers.

---

## 8 · Application immédiate à notre pipeline

- **Les quatre fiches « ligne fixe seulement »** du relevé Maps (`sales/APPELS-GOOGLE-MAPS-2026-09-24.md`,
  §2) gagnent un second angle : un commerce joignable **uniquement par fixe** est un commerce dont la fiche
  Google est souvent le seul point de contact moderne. C'est un fait à constater **avant** de le dire —
  pas une affirmation à réciter.
- **Vendredi 10 h, Univers Optique** : sa fiche existe, elle est notée, et son champ « site web » est vide.
  S'il a la main dessus, la séquence est : le site en ligne → **puis** le champ rempli → puis les horaires,
  les photos et la réponse aux six avis. S'il ne l'a pas, la première étape devient « revendiquer la
  fiche » (§2, étape 1) — et c'est *lui* qui peut le faire, pas nous.
- **Vendredi 13 h, UNI-LABO** : nous ne savons pas s'ils ont une fiche Google (ligne du CRM : `directory`).
  Donc on **demande**, on ne suppose pas — et si oui, le lien `wa.me` du chat (§3) est la première chose à
  corriger, avant tout le reste.
- **Nos propres pages** : la fiche Google d'AMK, si elle n'existe pas, est la première chose à créer —
  action de King, elle demande son compte Google et sa vérification.
- **En séance vendredi** (UNI-LABO, 13 h) : point **facultatif**, à trancher par King — si le laboratoire a
  une fiche, proposer d'y poser le lien `wa.me` du chat (§3). Ce n'est pas dans le prix de 150 000 FCFA et
  ce n'est pas une remise : c'est la première brique de la suite, si le client veut qu'on aille plus loin.

---

## 9 · Ce que les sources officielles ajoutent (lot [31], 24/09)

Le premier document de cette fiche reposait sur trois vidéos. King a envoyé depuis **la documentation de
Google elle-même** et le guide le plus complet du paquet. Ce qui change, et ce qui ne change pas.

### 9.1 · Les trois facteurs de classement, chez Google

Google ne classe pas une fiche « au mérite ». Trois facteurs, cités depuis son aide officielle :

| facteur | ce que c'est | ce que nous pouvons faire |
|---|---|---|
| **pertinence** | la fiche correspond-elle à ce qui a été cherché | la **catégorie principale** (le signal le plus fort), les services, les produits, la description. C'est notre terrain |
| **distance** | la distance entre le chercheur et le lieu | **rien** — et c'est important : personne ne peut la « tricher », et nous n'essaierons pas |
| **notoriété** | à quel point l'entreprise paraît connue et active | les avis (nombre, note, **fraîcheur**), la régularité des publications, la présence ailleurs sur le web |

La conséquence pratique est un garde-fou : **nous ne promettons jamais la première place**, puisque deux
des trois facteurs ne dépendent pas de nous (la distance) ou dépendent des clients (la notoriété).

### 9.2 · La vérification : cinq méthodes, et ce que la vidéo exige

Les vidéos en donnaient trois ; la réalité en compte cinq : **appel ou SMS**, **e-mail**, **courrier**
(le délai annoncé varie selon les sources : cinq à sept jours ouvrés, ou une à deux semaines),
**enregistrement vidéo**, **appel vidéo en direct**.

Ce que la vérification vidéo exige, pour ne pas faire perdre une heure au client : **une seule prise, non
montée**, qui prouve trois choses — que le lieu existe, que la personne y a bien accès, et que l'activité
est réelle. Le parcours qui marche : l'**enseigne à l'extérieur**, puis l'intérieur (matériel, poste de
travail), puis une preuve d'activité quotidienne (un cahier, un système de rendez-vous, un terminal de
paiement). **Rien de monté, aucun fichier repris dans la galerie du téléphone.** Et trois choses à tenir
**hors du cadre** : les visages, les informations de clients, les documents bancaires.

Conséquence pour nous : quand un client sera vérifié, c'est **lui** qui filme ; notre travail consiste à
lui donner la liste ci-dessus avant qu'il commence.

### 9.3 · Quand la fiche appartient à quelqu'un d'autre

C'est le cas d'Univers Optique (fiche notée, champ site vide, gestionnaire inconnu) et le cas le plus
fréquent sur les fiches anciennes : un ancien employé, une ancienne agence, un compte oublié. La marche à
suivre, documentée :

1. chercher le nom sur Google ou Maps ;
2. si la fiche est **libre** (« Revendiquer cet établissement ») → la revendiquer puis vérifier ;
3. si **quelqu'un la gère** → **demander l'accès** (nom, relation avec l'entreprise, niveau demandé) ;
4. le gestionnaire actuel a **trois jours** pour accepter ou refuser ; **sans réponse**, Google peut
   laisser la fiche être revendiquée, par la procédure indiquée dans l'e-mail de suivi.

Pour la séance de vendredi 10 h, la question posée à Univers Optique reste la même — « avez-vous la main
sur cette fiche ? » — mais elle a maintenant **trois réponses possibles**, et une procédure pour chacune.

### 9.4 · Ce que la documentation officielle ferme

L'API Business Profile existe, mais son accès exige **un compte Google valide, un motif professionnel
valide, un projet Google Cloud et une URL de site d'entreprise valide**. Autrement dit : **il n'y a pas
d'automatisation possible pour nous aujourd'hui.** Tout se fait dans l'interface, avec le compte du
client. Cette phrase remplace la ligne « il faudra peut-être un jour un outil » qui traînait dans ma tête.

### 9.5 · Les petits champs qui rapportent

- **Les attributs** : accessibilité, équipements, identité (entreprise féminine, etc.). Ils servent de
  **filtres** aux clients et donnent une raison de plus de choisir. À remplir une fois, à vérifier ensuite.
- **Les publications** : une par semaine ou par quinzaine suffit ; les liens suivis montrent le trafic
  envoyé.
- **Le tableau de bord** donne cinq chiffres : **recherches, vues, appels, itinéraires, clics vers le
  site**. Le plus utile pour nous est le dernier — c'est la preuve, chiffrée, que la porte de la fiche
  mène bien à la page que nous avons construite.
- **Une entreprise, une fiche.** Les vidéos parlaient de doublons comme d'une cause de suspension ; les
  guides ajoutent la règle complète : plusieurs fiches seulement pour des **adresses distinctes** ou des
  **activités réellement distinctes**, chacune avec ses propres informations. Un doublon volontaire pour
  « occuper le terrain » nuit et fait suspendre.
- **Les fiches ont une date de naissance** : le champ « date d'ouverture » nourrit la notoriété, et
  presque personne ne le remplit.

### 9.6 · Ce qui reste non vérifié (inchangé depuis §7)

Les méthodes de vérification réellement proposées **au Cameroun**, la présence du chat SMS/WhatsApp dans
les fiches du pays, les catégories disponibles en français, et la forme du tableau de performance pour un
compte non revendiqué. **Trois sources américaines et britanniques plus la documentation de Google ne
prouvent toujours rien sur une fiche camerounaise** — la documentation dit ce que le produit sait faire,
pas ce qu'il déploie ici.
