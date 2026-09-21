# Le Cristallin — inspiration (21 Sep 2026, 18:40)

**Commande de King :** « Le Cristallin a déjà un site (lecristallinoptique.com) — notre but, puisqu'il a eu
la gentillesse de nous répondre, est d'en créer une version moderne. » → **brief = refonte honnète d'un site
vivant**, pas un concept « vous êtes introuvable ». Cela change tout : la douleur n'est pas l'absence,
c'est ce que le site actuel ne fait pas.

## Le portail a été fait : `https://lecristallinoptique.com/` lu EN ENTIER le 21/09 (deux fragments, `hasMore`
false à la fin). Ce qui y est écrit, et rien d'autre, est la seule source de contenu de la maquette.

**Ce que le site actuel possède déjà (et que la maquette doit conserver, pas ré-inventer) :**
- ancienneté : « installé au Cameroun depuis 2010 » + « 24 ans d'expérience » · « personnel qualifié » ·
  « laboratoire high-tech » ;
- trois papiers : ISO 9001:2008 (via Laboratoires SIVO) · autorisation d'exercer MINSANTE · ONOC ;
- onze prestations nommées (examen de vue, orientation ophtalmologique, verres médicaux et spéciaux,
  montures de marque, montage, lentilles de contact, opticien conseil, entretien/réparation, contrôle,
  formation du personnel, bons de prise en charge) ;
- **douze assureurs et mutuelles** (Chanas, Activa ×2, Beneficial General, SAAR, Ascoma, Zénith, Samaritan,
  Mutuelle des Brasseries du Cameroun, Gras Savoye, Alpha, Saham, GMC) ;
- huit partenaires industriels (Essilor, MCT Vision, SIVO, American Optical, Fondation Krys, Luxottica,
  Technidis, Groupe LOGO) ;
- une offre : « kit d'entretien gratuit pour une paire achetée » ;
- un manifeste social (lutte contre la malvoyance et la cécité, urbain et rural) ;
- horaires : « Lundi à Vendredi entre 8h30 et 18h30 ».

**Ce que le site actuel ne fait pas — la douleur réelle, mesurée sur sa propre page :**
1. **Le carousel « Nos Produits » affiche la MÉME liste de montures trois fois de suite** (le bloc
   Stellaire → Lacoste → … → Sorealo est répété trois fois dans le HTML). Même erreur côté « Ils nous font
   confiance » : la liste des douze assureurs est triplée, et « ACTIVA ASSURANCES » apparaît **deux fois avec
   deux logos différents** (`c13.png` puis `c7.jpg`).
2. **Pas de WhatsApp.** Un opticien de Douala dont le seul bouton de contact est un formulaire
   Nom/Email/Objet/Message. Le numéro WhatsApp du cabinet est pourtant sur SON flyer (699 90 55 77) — celui
   par lequel King lui a écrit et par lequel il a répondu.
3. **Le flyer ajoute un samedi 08h30–13h30 que le site ne montre pas**, une adresse différente
   (« Carrefour CTFIC Mballa 2, Bonapriso » vs « Akwa, carrefour Ancien Dalip, face COMECI SA »), deux lignes
   de téléphone supplémentaires et une autre adresse e-mail. Quatre divergences entre ses deux supports.
4. **Aucun prix** (leur choix, légitime : la monture dépend du modèle) et **aucune prise de rendez-vous**.
5. `foundingDate` 2010 et ISO **9001:2008** : la version 2008 de la norme a été remplacée depuis — à
   confirmer sur le certificat courant, pas à « moderniser » par nous.

## Références de direction (3 angles, comme l'exige PRE-FLIGHT §2.3 — prises en ligne, pas de mémoire)

| Angle | Référence | Ce qu'on prend | Ce qu'on refuse |
|---|---|---|---|
| Structure | **Leur propre planche de flyer** (photo reçue sur WhatsApp, 21/09 18:02) : trois bandeaux de texte blanc sur vert, horaires en bloc, liste à puces | La hiérarchie « ce que je fais / quand venir / où » telle qu'ils la pensent déjà sur papier | Le jaune sur photographié, illisible sur téléphone |
| Typo-couleur | **Leur site actuel**, base blanche + logo œil bleu-vert | Le vert du flyer comme SEULE couleur d'accent (identité réelle du client, pas notre goût) | Tout l'empilement de carousels et de logos de marques |
| Motions/tone | **notre propre `concept-afriquelabo-v1`** (console à filets) et `concept-opticien-v1` (cabine d'essayage, Fraunces/ambre) | Le principe « les faits du propriétaire en tableau, pas en cartes » | **leurs deux palettes** : ink-teal + amber + cream et poster-cyan + navy sont déjà pris au registre → direction nouvelle |

**Ce que nous n'avons pas pu faire, écrit comme tel :** `playwright` est absent du bac → **aucune capture
1280×800** (`demos/shots/le-cristallin-concept.png`) et aucune vérification de rendu navigateur ici.
Les contrôles disponibles ont été passés (`audit_html.py` = 0 finding sur 387 runs, desktop et mobile).
La capture et le contrôle visuel restent À FAIRE avant que King envoie la maquette (voir `build-notes.md`).
