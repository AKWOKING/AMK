# Création de contenu — ce que le dépôt sait faire, au 22/10/2026

```
Statut   base de connaissance + mode d'emploi de l'outillage installé le 22/10
Sources  research/youtube-lessons/2026-10-22-eyecare-marketing/SYNTHESE.md
         research/youtube-lessons/2026-10-22-brand-strategy/SYNTHESE.md
         retour d'expérience du montage de la V2 (clients/dm-optic/content/month1/w1/)
Usage    toute production vidéo/sociale commence ici (PRE-FLIGHT §1g)
```

---

## 1 · La chaîne de production, telle qu'elle existe maintenant

```
photos réelles (dépôt)  →  moteur de rendu PIL  →  ffmpeg (imageio-ffmpeg)  →  portique mouvement  →  livraison
                                  ↑                        ↑
                            polices du site        voix (generate_speech)
```

| Maillon | Outil | État |
|---|---|---|
| Rendu des cartons et composition | **Pillow** | installé (13.0.0) |
| Encodage vidéo | **imageio-ffmpeg** (ffmpeg 7.0.2 statique) | installé — `apt` n'a pas accès aux dépôts |
| Polices | Schibsted Grotesk 500/700 + IBM Plex Sans, converties `woff2` → `ttf` par **fontTools + brotli** | dans `clients/dm-optic/content/month1/w1/assets/fonts/` |
| Moteur DM Optique | `tools/record/make_dmoptic_tiktok.py` | écrit le 22/10 |
| Portique qualité | `tools/qa/audit_video_motion.py` | **bloquant** |

**Commande d'installation** (à refaire si le sandbox est neuf) :
```bash
pip install --user --break-system-packages pillow imageio-ffmpeg numpy fonttools brotli
```

---

## 2 · Les règles de fabrication (payées par l'expérience)

1. **Chaque plan doit bouger.** Le portique bloque toute fenêtre de 2 s figée. Un carton « stable 3 s »
   échoue : il faut un zoom lent ou une apparition de texte.
2. **Zoom très lent = 2 à 6 %** sur la durée du plan. Au-delà, ça tremble et ça fait diaporama.
3. **Jamais d'agrandissement au-delà de 1,4×.** Une photo de 1400 px dans du 1920 devient molle.
4. **Produit sur fond uni** : on **échantillonne** la couleur des bords et on l'étend au 9:16. Ce n'est pas
   retoucher la photo, c'est changer le cadre — la monture reste intacte.
5. **Sous-titres incrustés**, jamais les automatiques de la plateforme : ce que le spectateur voit doit
   être exactement ce qu'on a écrit.
6. **Cartons : 0,3 s par mot**, minimum 0,8 s, deux lignes maximum à l'écran (réduire la police, pas le
   texte).
7. **Audio dans le fichier.** Un son ajouté dans l'application ne compte pas : le fichier livré porte la
   voix.
8. **Aucune musique commerciale.** Silence + voix, ou piste libre de droits documentée.
9. **Export** : 1080×1920, 30 fps, H.264, CRF ~20, `+faststart`, audio 128 kb/s. Sous 25 Mo.

---

## 3 · La structure d'un script court (5 temps)

Celle qui traverse toutes les sources et qu'on applique :

| # | Temps | Rôle | Interdit |
|---|---|---|---|
| 1 | **Le cas** | une situation vécue, à la 2ᵉ personne, dans les 3 premières secondes | se présenter, vanter le cabinet |
| 2 | **Le miroir** | ce que ça coûte, sans diagnostic | nommer un symptôme, promettre une guérison |
| 3 | **Le réel** | un objet du cabinet, un seul axe | empiler les arguments |
| 4 | **La preuve** | un fait vérifiable, une fois | « meilleur », « n°1 », « unique » |
| 5 | **La sortie** | un seul CTA + l'honnêteté (« si vous voyez bien, ne venez pas ») | deux CTA, urgence artificielle |

**Longueur** : 21–34 s. **Densité** : 2,5 à 3 mots par seconde lus à voix haute.

---

## 3 bis · Le gabarit en 9 blocs (Kallaway) — et comment il se pose sur nos 5 temps

Sources reçues de King le 23/10 : *Short-Form Storytelling (Writing Guide)* (3 p.) et *100 Viral Hooks*
(BrandIt, 16 p.), tous deux de l'école **Kane Kallaway**. Vérifié au passage : le format et les « 4 S »
sont bien les siens (atelier hooks, `luma.com/sfa-hooks` ; podcast Castmagic 2025 ; analyse build-os 2026).

**Le gabarit, mot pour mot :** Hook (1–2 phrases) → **Lock-in zone** (2–4) → Body block 1 (3–5, avec au
moins une idée contre-intuitive) → **Rehook 1** (1 phrase) → Body block 2 (3–5) → **Rehook 2** (1) →
(option) Body block 3 → (option) Closing → **CTA** (1 phrase, idéalement un **lead magnet aligné**).

**Ce que chaque bloc fait :**

| Bloc | Fonction | Erreur fatale |
|---|---|---|
| Hook | nomme le sujet, pose l'enjeu, en mots simples | se présenter, ou une accroche « jolie » qui ne dit pas le sujet |
| Lock-in | convainc que la suite vaut les 20 prochaines secondes : preuve annoncée, contraste, « boîte magique », objection désarmée | enchaîner sur le corps sans avoir mérité l'attention |
| Body block | une idée non évidente + 2 à 4 phrases qui la défendent | empiler des généralités |
| Rehook | remet le sablier à zéro (contraste, nouvelle curiosité) | une transition plaquée, « mais ce n'est pas tout » |
| CTA | rampe vers de la valeur supplémentaire, mesurable | deux CTA, ou « abonnez-vous » sans contrepartie |

**Deux principes qui changent notre façon d'écrire :**

1. **L'alignement du hook compte plus que le hook.** Ordre d'importance, selon Kallaway : **hook visuel >
   hook écrit (texte à l'écran) > hook parlé**. Nos cartons doivent donc porter l'accroche *écrite*, pas
   seulement la voix.
2. **Le rehook est un besoin physiologique, pas un tic d'écriture.** Selon Kallaway, l'attention moyenne
   sur un short tourne autour de **20 à 25 secondes** — *chiffre de praticien, pas une étude* : on le
   retient comme **hypothèse de travail**, on ne le cite jamais comme une statistique (§1g). Conséquence
   pratique : un rehook au milieu achète une vingtaine de secondes de plus.

**Comment on le pose sur nos 5 temps (§3), sans trahir ni l'un ni l'autre :**

| Nos 5 temps | Blocs Kallaway | Ce qu'on garde de nous |
|---|---|---|
| 1 · Le cas | **Hook** | la situation vécue à la 2ᵉ personne, dans les 3 premières secondes |
| 2 · Le miroir | **Lock-in zone** | ce que ça coûte, sans diagnostic |
| 3 · Le réel | **Body block 1** | un seul objet du cabinet, un seul axe |
| — | **Rehook** | « et ce n'est pas le pire » → amène la preuve |
| 4 · La preuve | **Body block 2** | un fait vérifiable, une fois |
| 5 · La sortie | **CTA** | un seul CTA + l'honnêteté (« si vous voyez bien, ne venez pas ») |

**Les six principes d'écriture qui vont avec** (ils valent plus que le gabarit lui-même) :

1. **Couper le gras** — chaque phrase qui ne fait pas avancer s'enlève.
2. **Le plus court possible** — leur fourchette idéale est 45–90 s ; on ne rallonge jamais pour remplir.
3. **Une logique évidente** — chaque phrase se rattache à la précédente, ou ouvre clairement une nouvelle
   chaîne. Sauter d'une idée à l'autre rend la vidéo illisible.
4. **Annoncer la valeur tôt** — dire pourquoi rester, dès le début, pas à la fin.
5. **Des mots simples** — le mot que le patient emploierait, pas le mot du métier.
6. **La clarté avant l'élégance** — si une formulation est jolie mais moins claire, on garde la claire.

**La seule tension, et elle est réelle :** Kallaway vise **45–90 s** ; nos scripts DM tiennent en
**21–34 s**. On ne rallonge pas pour rentrer dans un gabarit — un short de 30 s qui garde 30 % vaut mieux
qu'un 70 s qui garde 12 %. Le gabarit sert quand **la matière le justifie** (une explication, un
« pourquoi »), pas pour remplir. Règle : **rehook obligatoire dès qu'on dépasse 25 s**.

---

## 3 ter · Les quatre S du hook, et la banque de hooks adaptée

**Les quatre S** (Kallaway) : **S**ujet (le sujet est dit dans la première phrase) · **S**takes (une
raison de rester) · **S**imple (mots de tous les jours) · **S**uperclear (structure limpide, une seule
idée par phrase).

**Banque adaptée** — 15 hooks dérivés de *100 Viral Hooks* (les originaux sont en anglais, à la 2ᵉ
personne, avec des trous). On garde **la structure**, jamais le contenu : un hook copié tel quel sonne
faux et ne parle pas de Bonabéri.

| # | Hook (français, adapté au cabinet) | D'où il vient (structure) |
|---|---|---|
| 1 | « Vous pensez qu'il faut une ordonnance pour changer de monture. En réalité, il n'en faut pas toujours. » | « People think you need X, but in reality you only need Y » |
| 2 | « Ne faites jamais nettoyer vos verres au tee-shirt avant de savoir ces deux choses. » | « Never start X before you understand these N things » |
| 3 | « Arrêtez de plisser les yeux pour lire votre téléphone jusqu'à ce que vous ayez fait ceci. » | « Stop X until you Y » |
| 4 | « Il y a deux façons de choisir une monture. Devinez laquelle vous fait porter la même que tout le monde. » | « A vs B — who do you think gets X? » |
| 5 | « Si quelqu'un vous dit qu'il voit bien, demandez-lui de lire la plaque d'un taxi à dix mètres. » | « If someone says they don't like X, just Y » |
| 6 | « Ça, c'est le moment où la plupart des gens achètent la mauvaise monture. » | « This is exactly what you want to see when… » |
| 7 | « Votre ordonnance date de deux ans ? Voici ce que ça change concrètement. » | « Do you struggle with X? » |
| 8 | « Je suis opticien à Bonabéri, et voici ce que je refuse de vendre. » | « I am X in Y, and this is… » |
| 9 | « Regardez ces deux verres : même correction, même prix. Un seul est sale depuis six mois. » | « Look at these two: same X, the left one… » |
| 10 | « Trois choses que les patients croient normales, et qui ne le sont pas. » | « N things X think are normal, but aren't » |
| 11 | « Le chiffre qui vous coûte le plus cher quand vous commandez des lunettes en ligne. » | « There's one number that will kill you in X » |
| 12 | « Vous avez déjà eu mal à la tête à 16 h sans savoir pourquoi ? C'est peut-être ça. » | « Have you ever noticed that X… » |
| 13 | « Personne ne vous le dira au comptoir : voilà comment on reconnaît une monture trop lourde. » | « No more gatekeeping. These are my N… » |
| 14 | « J'ai payé pour apprendre ça. Je vous le dis en trente secondes. » | « I paid $X to learn this » |
| 15 | « Si vous devez acheter une seule chose cette année pour vos yeux, c'est celle-ci. » | « People only spend money on N things » |

**Trois règles d'usage** (sinon la banque devient un générateur de clickbait) :

- **le hook ne promet rien que la vidéo ne tienne** — un hook qui ment coûte le compte, pas la vue ;
- **aucun hook ne touche aux verrous client** : pas de prix de monture, pas de délai, pas de superlatif,
  pas d'allégation santé (« guérir », « corriger définitivement ») — voir §6 bis ;
- **on teste trois hooks pour la même vidéo**, on garde celui qui retient, et on note le numéro gagnant
  dans le fichier de la semaine.

---

## 4 · Les quatre piliers de contenu (modèle DM Optique, transposable)

| Pilier | Ce que c'est | Preuve mobilisée |
|---|---|---|
| **Le geste utile** | une chose faisable dans les 30 secondes (20/20/20, entretien des verres) | aucune promesse — l'utilité |
| **La monture réelle** | une monture du stock, photographiée au cabinet, nommée | « montrer avant » |
| **La coulisse** | ce qui se passe entre la porte et la sortie | « mesurer, pas deviner » |
| **La sortie honnête** | ce qu'on refuse de faire, à qui on dit non | « dire quand on n'a pas besoin » |

**Rythme** : 2 posts/semaine — un pilier 1 ou 4, un pilier 2 ou 3. C'est ce qui supprime la question
« que poster aujourd'hui ? ».

---

## 4 bis · Choisir le type de contenu selon l'objectif visé

Source reçue le 23/10 : @ameliagonzamonte, *« posting content just because it's going viral is one of the
best ways to never reach your specific goals »*. Le principe est le bon et il manquait : **on choisit le
type de contenu d'après l'objectif, pas d'après la tendance.**

| Objectif réel | Type de contenu qui y mène | Ce que ça donne chez DM |
|---|---|---|
| **être connu comme la référence** (opticien, pas « un opticien ») | prises de position, prédictions, cadre maison, série signée | « ce qu'on refuse de vendre », « pourquoi on mesure avant de vendre » |
| **faire écrire en DM / au WhatsApp** | Q&R, jeu de rôle, réponses aux objections, démonstration | « votre ordonnance date de deux ans », « ma monture glisse » |
| **créer l'urgence de ne pas rester bloqué** | transformations, erreurs qui coûtent, cadre comparatif — **poussée douce, jamais la peur** | « ce que ça coûte d'attendre » (sans dramatiser, sans promesse) |
| **attirer les bons et écarter les mauvais** | prise de position claire sur **pour qui on n'est pas** | « si vous cherchez le moins cher, ce n'est pas ici » |

**Ce que ça interdit :** publier « parce que ça peut devenir viral ». Une vidéo virale qui n'appelle
personne est un feu de paille : elle coûte une journée de production et ne laisse **aucun** avis, aucune
conversation, aucun patient.

**Ce qui relie les quatre lignes :** chacune se termine par **le même** CTA — un seul opt-in, (§5 bis).

**Ce que cette section ne disait pas encore (ajouté le 25/10)** : *quel jeu* on joue. Choisir le type de
contenu selon l'objectif ne suffit pas si l'objectif lui-même est mal nommé — une pièce peut être bien
faite, bien ciblée, et viser la **portée** alors que notre monétisation est **hors plateforme**. Le texte
« The 5 Content Games » (25/10, tier C) le tranche : AMK vend un service → **jeu 5, l'autorité** ; la
formule de confiance est `minutes watchées × pertinence × utilité`, et une pièce courte **plafonne à
25/125**. La doctrine complète — les cinq jeux, le diagnostic en quatre questions, le barème, les quatre
conflits tranchés et la semaine en trois rôles — est dans **`knowledge/CONTENT-GAMES-2026-10-25.md`** ;
sa porte est **`tools/qa/audit_trust.py`**. Le §4 bis reste la règle de *quoi publier* ; le document des
jeux est la règle de *pourquoi*, et de *quel rôle* la pièce tient dans la semaine.

---

## 4 ter · Les six formats de la matrice, outillés pour le cabinet (23/10)

Le §4 bis dit **quel type de contenu pour quel objectif**. Il ne dit pas **comment on le fabrique**
quand on a un téléphone, un cabinet et aucun acteur. C'est ce trou que cette section ferme.
Six formats, une seule règle de fond : **le format ne change jamais ce qu'on a le droit de dire**
(verrous du §6 bis — aucun montant, aucune marque de monture, aucun visage, aucun délai promis).

| Format | Objectif servi | La version DM — concrètement | La preuve qu'il faut avoir | Le piège |
|---|---|---|---|---|
| **La démonstration** | faire écrire (§4 bis, ligne 2) | on filme **le geste** : mesurer une monture, régler un tenon, souffler sur un verre — 8 s, mains seules | le geste a été fait au cabinet cette semaine | filmer un appareil qu'on ne sait pas nommer : ça se voit |
| **La réponse à une objection** | faire écrire | on prend **la phrase exacte** d'un client (« c'est cher », « j'attends l'ordonnance ») et on y répond en 20 s, sans la déformer | la phrase a été **entendue**, pas imaginée | répondre à une objection que personne ne pose : c'est un argumentaire, pas une vidéo |
| **Le jeu de rôle** | faire écrire | deux voix, un seul téléphone tenu à la main : « — Docteur, ma vue a baissé. — Depuis quand ? » — la question qu'on pose vraiment en consultation | le script suit **notre** protocole de questions (§contenu examen) | jouer un patient mécontent : ça invente un problème qui n'existe pas |
| **L'erreur qui coûte** | l'urgence douce | « trois choses qui abîment vos verres sans que vous le sachiez » — on montre, on ne dramatise pas | chaque erreur est **constatée au comptoir** | glisser vers la peur (« vous allez perdre la vue ») : interdit, et faux |
| **La transformation** | l'urgence douce | avant/après **d'un objet**, jamais d'un patient : une monture tordue puis redressée, un verre rayé puis changé | la monture existe, la photo est réelle | montrer un visage, même de dos, même flouté |
| **La prise de position** | attirer les bons, écarter les autres | « on ne vend pas une monture sans l'essayer » · « on dit quand vous n'avez pas besoin de nous » — une phrase, tenue | c'est **notre** pratique, pas une posture | la fausse polarité gratuite (« les autres opticiens sont nuls ») : on parle de nous |

**Ce qu'on garde de la source, mot pour mot :** *« copycats never stand out »*. Traduit en une règle de
fabrication : **si la vidéo pourrait être postée par n'importe quel opticien de Douala, elle ne sort pas.**
Le test tient en une question — *qu'est-ce qui, dans cette vidéo, ne pourrait exister qu'ici ?* Si la
réponse est « rien », on jette le plan, pas la journée.

**Ce qu'on écarte de la source, et pourquoi :** les **prédictions** (« voici ce qui va changer en 2026 »)
supposent une autorité de marché qu'un cabinet de quartier n'a pas — et une prédiction sur la santé est
une promesse déguisée. Les **réactions** (commenter l'actualité) demandent une actualité optique suivie ;
on ne l'a pas. Restent **quatre** formats sur six : démonstration, objection, erreur qui coûte,
prise de position — plus le jeu de rôle, réservé aux semaines où le protocole de questions change.

**Le calendrier qui en découle** (2 posts/semaine, §4) :

| Semaine | Mardi | Vendredi | Objectif travaillé |
|---|---|---|---|
| 1 | démonstration (mesurer une monture) | prise de position (« on ne vend pas sans essayer ») | crédibilité + tri |
| 2 | erreur qui coûte (les verres) | réponse à une objection entendue | urgence douce + conversation |
| 3 | transformation (monture redressée) | « vous demandez, on répond » (§5 sexies) | preuve + série |
| 4 | jeu de rôle (les questions de l'examen) | démonstration (réglage) | conversation |

**La mesure, une seule, à 30 jours :** nombre de conversations WhatsApp ouvertes **après** un post,
comparé au mois précédent. Les vues ne disent rien (§5) ; une démonstration qui n'ouvre aucune
conversation est un plan réussi et une vidéo ratée.

---

## 5 · Ce qui produit un résultat (et ce qui ne le produit pas)

| On mesure | On ne mesure pas |
|---|---|
| conversations WhatsApp avec le message pré-rempli propre à la vidéo | vues |
| avis Google gagnés | likes |
| itinéraires et appels depuis la fiche | abonnés |
| enregistrements et partages (pilier 1) | impressions |

**Le message pré-rempli est la seule attribution fiable** : chaque vidéo a son propre texte
(`wa.me/237…?text=…`), sinon une conversation ne dit pas d'où elle vient. Pas de cookies, pas d'UTM côté
WhatsApp.

---

## 5 bis · Un opt-in, un seul — et où vit le mot-clé (ruling King 23/10)

**Correction d'abord, parce que ma phrase était ambiguë :** « `CONTRÔLE` dans la bio » ne voulait **pas**
dire remplacer la bio par ce mot. La bio garde son texte ; le mot est une **porte**, pas un titre.

**Et l'aimant ne concerne pas les patients de DM.** Il parle aux **opticiens et gérants de cliniques** —
des prospects AMK. Donc :

| Compte | Public | CTA | Mot-clé |
|---|---|---|---|
| **AMK** | opticiens, cliniques, écoles | « commentez **CONTRÔLE** » | `CONTRÔLE` → le contrôle présence en ligne |
| **DM OPTIQUE** | patients du cabinet | « écrivez-nous / passez au cabinet » | **aucun aimant** : un patient veut un rendez-vous, pas un PDF |

**Où placer le mot, dans l'ordre d'efficacité réel** (règle du 23/10 : hook visuel > écrit > parlé) :

1. **à l'écran, dans les dernières secondes de la vidéo** — c'est là que le CTA est vu ;
2. **première ligne de la légende** — c'est ce que le lecteur voit avant « plus » ;
3. **commentaire épinglé**, avec le lien `wa.me/…?text=CONTRÔLE` ;
4. **dernière ligne de la bio** — utile seulement quand quelqu'un visite le profil après la vidéo.

**Commentaire ou message privé ?** Les deux, dans cet ordre : on demande **un commentaire** (il pousse la
vidéo et il est public), puis on répond **en message** avec le PDF. Un commentaire par personne, réponse
manuelle sous quelques heures : à notre volume, aucun outil n'est nécessaire — et l'automatisation de
réponse par mot-clé (ManyChat et compagnie) demande un accès API et un abonnement qu'on n'a pas.

**Et « abonne-toi d'abord, puis écris » ?** Évalué honnêtement :

| Ce que ça donne | Ce que ça coûte |
|---|---|
| des abonnés en plus, et un compte qui paraît vivant | une étape de plus avant la conversation, sur un prospect qui ne nous connaît pas |
| | aucun moyen technique de le vérifier côté TikTok — on ne peut pas conditionner la réponse |
| | pour un commerce local, **un abonné ne vaut pas une conversation WhatsApp** : c'est la conversation qui devient un devis |

**Décision : pas de porte d'abonnement.** Le commentaire suffit à faire vivre la vidéo, et le message fait
le reste. Si les chiffres montrent un jour que les abonnés manquent, on en reparlera avec un test — pas
avant.

## 5 ter · La bibliothèque derrière l'aimant : un seul mot-clé, plusieurs portes

Ruling King 23/10 : *« the lead magnet will be to attract people to our WhatsApp and that's where we
will give them the free resource »*. Donc **l'aimant n'est pas le PDF, c'est la conversation** — le PDF
est ce qu'on donne en échange du numéro. Et la matière existe déjà : la base de connaissance, c'est une
bibliothèque de ressources écrites, pas un dossier d'archives.

**La règle qui évite de tout donner d'un coup :** une seule entrée (mot-clé `CONTRÔLE`), puis **une
ressource par étape** de la conversation. Quatre, pas dix. Chacune répond à une objection précise qu'on
entend au téléphone.

| Étape | La ressource | L'objection qu'elle lève | Elle vient de |
|---|---|---|---|
| 1 · Entrée | **Le contrôle présence en ligne** (12 points) | « je ne sais pas où j'en suis » | `sales/lead-magnets/CONTROLE-PRESENCE-EN-LIGNE-2026-10-23.pdf` |
| 2 · Autorité | **Le calendrier de 12 publications** (quoi publier, quand, et pourquoi ça tient en 2 h/mois) | « je n'ai pas le temps de publier » | `knowledge/CONTENT-CREATION…` §4 + `clients/dm-optic/content/month1/` (le vrai calendrier tenu) |
| 3 · Preuve | **Le récapitulatif d'une page** (le vrai, celui de DM) | « qu'est-ce que je reçois pour 30 000 par mois ? » | `clients/dm-optic/launch/RECAP-MISE-EN-LIGNE-2026-10-23.pdf` (version publique, chiffres conservés) |
| 4 · Qualification | **Le contrat d'une page** | « et si je veux arrêter ? » | `ops/templates/CONTRAT-UNE-PAGE-2026-10.pdf` |

**Ce que l'ordre fait :** l'étape 1 coûte 8 minutes au prospect ; l'étape 2 lui coûte une demi-journée
de lecture ; l'étape 3 prouve qu'on travaille ; l'étape 4 dit qu'on est un prestataire, pas un ami. Un
prospect qui demande l'étape 4 sans avoir lu l'étape 1 est un curieux, pas un client.

**Comment on livre — et pourquoi pas une liste de diffusion.** Relevé le 23/10 (guides WhatsApp
2026, tous alignés sur la politique Meta) :

| Fait de plateforme | Conséquence pour nous |
|---|---|
| Une **liste de diffusion** de l'application gratuite plafonne à **256 contacts** et ne délivre **qu'aux personnes qui ont enregistré notre numéro** | inutilisable pour des prospects : la plupart n'ont pas notre numéro en contact |
| Une **chaîne WhatsApp** n'est pas une diffusion : pas de réponse privée, pas de fichier échangé | ne sert pas à livrer une ressource |
| L'**opt-in est obligatoire** ; les blocages font chuter la qualité du numéro et peuvent le faire restreindre | on ne message jamais un numéro qui n'a pas écrit d'abord |
| Sur l'API payante, la fenêtre de service est de **24 h** après le message du client | on répond dans l'heure, pas le lendemain |

**Donc le seul chemin qui marche ici** : le prospect écrit `CONTRÔLE` → on répond dans la conversation
1:1 avec le PDF → on pose **une** question. Aucune liste, aucun envoi de masse, aucun outil à installer.
C'est aussi la raison pour laquelle l'aimant doit vivre sur nos propres comptes (AMK), pas sur ceux du
cabinet : le numéro qui reçoit le message doit être celui qui peut y répondre.

**Deux règles debout (ruling King 23/10) :**

1. **On mesure l'aimant avant d'en créer un second.** Un seul opt-in = un seul chiffre à lire : combien
   de `CONTRÔLE` reçus, combien de conversations, combien de rendez-vous. Créer un deuxième aimant avant
   d'avoir ces trois nombres, c'est brouiller la seule mesure propre dont on dispose.
2. **45–90 s pour les explications, 20–30 s pour les gestes.** La fourchette Kallaway s'applique quand il
   y a une démonstration à tenir (un « pourquoi », un cadre). Un geste utile qui tient en 20 s ne se
   rallonge pas : un short de 30 s qui retient passe devant un 70 s qui ennuie.

---

## 5 quater · Une vidéo, deux plateformes : un tournage, deux montages (ruling King 23/10)

> *King, 23/10 : « since Facebook and TikTok give different results for the same video, shouldn't we
> create a video adapted for each of them ? and you are right, shares and comments always help the boost
> of a post, so we should make sure our videos push watchers to do so. »*

**Oui — mais pas deux créations.** Ce qui change n'est pas la matière, c'est le montage. Ce qui suit est
mesuré sur la première vidéo de DM Optique (voir `ANALYSE-POST-1`, relevé à 24 h).

### Ce que nos deux tableaux de bord disent, sur le même film

| | Facebook | TikTok | Lecture |
|---|---|---|---|
| Vues | 227 | 80 | Facebook distribue plus large |
| Lecture moyenne | 4 s / 31 = **12 %** | 4,7 s / 18 = **26 %** | **TikTok juge mieux le film** |
| Sortie massive | 0:05 | **0:02** | deux causes différentes |
| Complètes | 2,4 % (à 20 s) | 6,67 % | idem |

**Les deux réseaux ne mesurent pas la même chose :**
- **TikTok note le film.** Le pourcentage de lecture est le seul juge ; une vidéo à 26 % est « bonne mais
  pas assez » pour être poussée. Les deux premières secondes décident du reste.
- **Facebook distribue le film.** Il donne des vues à un film imparfait, puis s'arrête quand les gens
  partent. Le nombre de vues ne dit rien de la qualité ; **le partage, si** — c'est le seul geste qui
  remet la vidéo devant quelqu'un qui ne nous suit pas.

### La grille des deux montages

| | **TikTok** | **Facebook** |
|---|---|---|
| Durée | 12–16 s | 16–22 s |
| Première image | l'action, déjà commencée — jamais un logo, jamais une façade | la même action |
| Texte | 3–5 mots, très gros, **en haut** (le bas est couvert par l'interface) | 3–5 mots + **sous-titres intégrés** |
| Légende | 2 lignes | 6–10 lignes — Facebook se lit |
| Partage | demandé à l'oral, une fois | demandé dans la légende **et** à l'oral |
| Question | réponse en un mot ou un chiffre | la même, en fin de légende |
| Ce qu'on mesure | % de lecture, % de complètes | vues, partages, commentaires |

**La règle de tournage qui rend les deux possibles :** on filme **large et long** — deux fois la durée
prévue, 3 secondes de respiration au début de chaque plan. Un plan tourné à la seconde près ne se
remonte pas pour l'autre réseau.

### Faire partager et commenter — sans mendier

Un « partagez svp » ne marche pas : il demande un effort sans dire à qui. Les quatre mécaniques qui
marchent, dans l'ordre :

| # | Mécanique | Exemple |
|---|---|---|
| 1 | **nommer la personne à qui l'envoyer** | « montrez ça à quelqu'un qui éloigne son téléphone pour lire » |
| 2 | **une question dont la réponse est un mot ou un chiffre** | « depuis quand écartez-vous votre téléphone pour lire ? » |
| 3 | **répondre à chaque commentaire dans l'heure** | une réponse relance la conversation et prévient le suivant |
| 4 | **remercier nommément**, jamais « merci à tous » | « merci Madame, c'est noté pour la monture » |
| 5 | **répondre à une question par une vidéo** (§5 sexies) | « la question de Sandrine » en ouverture |

**Ce qu'on ne fait pas :** demander un like, un abonnement, ou « commentez un emoji ». Ça produit des
commentaires vides, et un commentaire vide n'apprend rien à l'algorithme **ni à nous**.

⚠️ **Ce qui est mesuré et ce qui ne l'est pas.** Les quatre mécaniques ci-dessus reposent sur un
raisonnement (un partage met la vidéo devant un nouvel audience) et sur nos 0 partage constatés — **pas
sur une étude**. On les applique parce qu'elles ne coûtent rien et qu'elles sont vraies ; on ne promet pas
qu'elles doublent la portée. Le seuil du §6 de `ANALYSE-POST-1` le dira en deux vidéos.

---

## 5 quinquies · Le décor doit exister chez le spectateur (ruling King 23/10)

> *King, 23/10, sur une vidéo qui commençait par un journal qu'on éloigne : « plus personne ne lit le
> journal. Regarder le journal à la télé oui, mais acheter et lire un papier journal, je n'en vois même
> pas autour de moi. »*
>
> **Précision du même jour, qui tranche la question : « c'est le journal. »** Le refus portait sur
> **l'objet**, pas sur la cible : la vidéo pour les 45 ans et plus est **gardée**, le décor passe au
> téléphone.

**Ce n'était pas un détail de décor, c'était une erreur de méthode.** Le geste de la presbytie — écarter
les bras pour lire — est juste ; **l'objet était faux**. J'avais pris la mise en scène d'un manuel
occidental sans vérifier qu'elle existe encore ici.

**La règle : tout objet filmé doit avoir été vu dans la journée par quelqu'un de Bonabéri.** Pas « dans
un pays proche », pas « il y a dix ans » : **cette semaine, à Douala.**

| Objet | Verdict |
|---|---|
| un téléphone tenu à bout de bras | ✅ tout le monde le fait, dix fois par jour |
| un écran d'ordinateur à 40 cm | ⚠️ vrai pour les actifs, faux pour la moitié de l'audience mesurée |
| un journal déplié | ⛔ a disparu |
| une carte de visite, un flyer | ⛔ remplacés par le contact WhatsApp |
| un rendez-vous noté dans un agenda papier | ⛔ rare |
| une ordonnance, une monture, l'appareil de mesure | ✅ objets du métier, mais **jamais lisibles** (verrou données patient) |

**Le test des trois secondes, avant de tourner :** montre l'objet à la première personne qui passe dans
la boutique et demande **« tu as vu ça cette semaine ? »** Si la réponse hésite, l'objet sort du plan.

**Corollaire pour l'écriture :** la même règle vaut pour les mots. « Presbytie » ne se dit pas ; « vous
écartez votre téléphone pour lire » se dit. **Un mot que le spectateur n'emploie pas est un objet qu'il
n'a pas vu.**

---

## 5 sexies · « Vous demandez, on répond » — la série qui fait commenter (ruling King 23/10)

> *King, 23/10 : « on peut aussi encourager notre audience à nous poser des questions sur ce qu'ils
> aimeraient savoir, puis on peut leur répondre par une autre vidéo et les taguer. »*
>
> **Validé le 23/10 au soir : « oui, on démarre la série avec la prochaine vidéo. »** Le point de départ est
> `clients/dm-optic/content/month1/w3/presbytie-55ans-SCRIPT.md` (bloc 8 : la demande de question).

**Oui — et c'est la seule mécanique qui produit trois choses à la fois :** des commentaires (qui poussent le
post), **la matière des vidéos suivantes** (on ne devine plus les sujets, ils arrivent tout seuls), et un
lien personnel avec ceux qui ont demandé.

### Le cycle, en quatre gestes

| # | Geste | Où | Quand |
|---|---|---|---|
| 1 | **on demande la question** — à l'écran dans les 2 dernières secondes, et en première ligne de légende : *« quelle question vous pose-t-on le plus souvent sur les yeux ? »* | vidéo + légende | en continu |
| 2 | **on garde la question et le prénom** — capture d'écran, dossier `questions/` | interne | le jour même |
| 3 | **on répond en vidéo** — la question à l'écran au début (*« la question de Sandrine »*), la réponse en 15 s | vidéo suivante | une par semaine |
| 4 | **on tague la personne** dans la légende et le commentaire, **avec son accord** | publication | à la sortie |

### Ce qui rend la série tenable

- **Une question = une vidéo de 15 s.** Aucune ne demande de tournage : le cabinet est le décor, la réponse
  se dit en une prise.
- **On ne répond qu'aux questions qu'on peut traiter sans données patient.** « Pourquoi mes yeux piquent le
  soir ? » oui ; « est-ce que ma correction est bonne ? » non — ça se voit au cabinet, et ça se dit ainsi.
- **Le tag demande l'accord, toujours.** Une personne qui pose une question en commentaire public n'a pas
  donné son nom pour une vidéo. **On demande en message privé ; sans réponse, on anonymise** (« une
  cliente du quartier ») — et on dit pourquoi.

### Ce que ça change dans nos chiffres

| Chiffre | La n°1 | Ce que la série doit produire |
|---|---|---|
| Commentaires | 1 | **≥ 3 par vidéo** — et chacun est une question potentielle |
| Matière pour le mois suivant | on l'inventait | **elle vient de l'audience** |
| Tag / partage | 0 | la personne taguée voit la vidéo **et** la partage souvent |

⚠️ **Ce qui n'est pas prouvé :** je n'ai pas de mesure AMK sur l'effet d'une série « questions ». Ce qui est
sûr, c'est que **répondre à une question nommée produit un commentaire de plus** (la personne répond), et
qu'un commentaire de plus vaut mieux qu'un commentaire inventé.

---

## 6 · Visages, UGC et modèles IA — la position du dépôt

**Rappel des faits** : le client (King) et le docteur ont évoqué la possibilité de **modèles UGC
réalistes / influenceurs IA** si le mois 1 ne donne pas de résultats ; les visages **du personnel** sont
autorisés sur les photos.

### Ce qui est autorisé

- Les **photos réelles** du cabinet et des montures, y compris avec le personnel identifiable (accord du
  client, 22/10).
- Un **avatar IA présentateur** — quelqu'un qui *explique* ce qu'on lui fait dire — **à condition** d'être
  signalé comme généré par IA (voir ci-dessous).
- Les **témoignages réels**, avec autorisation écrite, sans détail de santé.

### Ce qui n'est pas autorisé, et ne le sera pas

| Interdit | Pourquoi |
|---|---|
| Un **faux patient** généré par IA qui dit « j'ai été soigné chez eux » | c'est un **faux témoignage** : tromperie, et dans beaucoup de pays une pratique commerciale illicite. Le gain à court terme coûte la crédibilité entière du cabinet |
| Un **professionnel de santé IA** présenté comme le praticien | même raison, aggravée : c'est un titre réglementé (ONOC) |
| Une **photo de produit** générée ou retouchée | règle de maison : les photos réelles sont la matière première |
| Un contenu IA **non signalé** | les plateformes exigent le signalement des médias synthétiques ; un compte qui se fait prendre perd sa portée |

### Les conditions pratiques, si on va vers l'avatar IA

1. **Étiqueter** : mention « contenu généré par IA » dans la légende, et l'étiquette native de la
   plateforme quand elle existe.
2. **Rôle limité** : présentateur / explicatif. Jamais un patient, jamais un soignant, jamais un
   témoignage.
3. **Aucune promesse médicale** dans la bouche de l'avatar — c'est nous qui parlons.
4. **Cohérence de marque** : même voix, même axe (« on montre avant de vendre »), même typographie.
5. **Le réel reste majoritaire** : au moins un contenu sur deux doit contenir une image réelle du
   cabinet ou d'une monture — sinon le compte devient une chaîne d'avatars et perd ce qui le distingue.
6. **Décision de King avant production**, et mention au dossier client.

### L'outillage vidéo (posé le 22/10)

| Besoin | Outil | Fichier |
|---|---|---|
| monter une vidéo à partir d'un storyboard (photos, produit, cartons, clip, voix) | **`tools/ugc/ugc.py`** | `tools/ugc/README.md` |
| obtenir un **plan d'humain** (qualité Flow), avec un prix vérifié | **Veo 3.1 via l'API Gemini** : 0,05–0,12 $/s en 1080p, 9:16 natif, audio inclus → **0,64 à 0,96 $ le clip de 8 s** | `tools/ugc/providers.py` |
| présentateur nommé, longue durée | HeyGen Avatar V, 29 $/mois | `tools/ugc/providers.py` |
| animer **une seule photo** du cabinet avec une voix | Hedra Character-3, ~20 $/mois | `tools/ugc/providers.py` |
| contrôler qu'une vidéo n'est pas un diaporama | **portique** `tools/qa/audit_video_motion.py` | §1b |

**Trois faits à ne pas réapprendre :**

1. **Google Flow n'a pas d'API.** Le modèle derrière (Veo 3.1) s'achète à la seconde sur l'API Gemini.
2. **Aucun modèle ouvert ne tourne dans le sandbox** : pas de GPU, 3 Go de RAM, HuggingFace bloqué.
3. **`morluto/rea` n'est pas un outil vidéo** : c'est un serveur MCP de rétro-ingénierie de binaires. Le
   détour n'existe pas — comparatif complet et chiffré dans `research/ugc-video/2026-10-22-TOOLCHAIN-UGC.md`.

### La voie préférée — **tranchée le 22/10 par King**

> King, 22/10 : « on garde le sans-visage et on réserve l'argent pour la séance de tournage d'une
> demi-journée par mois ».

| Rang | Voie | État |
|---|---|---|
| **1** | **Photos réelles + cartons + voix** (`tools/ugc/`) | **en production** — UGC-03 livré, portique vert |
| **2** | **Une séance de tournage d'une demi-journée par mois** (14h–18h, 4 blocs, 30–40 clips) | **retenue** — budget réservé, plan écrit : `clients/dm-optic/content/tournage/PLAN-TOURNAGE-MENSUEL.md` |
| 3 | Avatar IA présentateur (HeyGen 29 $/mois) | **écarté pour l'instant** — les données 2026 ne le justifient pas (Kantar : 54ᵉ vs 65ᵉ centile ; retargeting humain +20–25 %) |
| — | Clips Veo (API Gemini, 0,64–0,96 $ le plan de 8 s) | **non acheté** — reste disponible si un jour un plan généré manque ; rien ne bloque sans lui |

**Conséquence opérationnelle** : le sans-visage **teste**, l'humain **convertit**. Ce sont deux rôles, pas
deux niveaux de qualité. Le tournage mensuel ne remplace pas le montage sans visage : il l'alimente en
matière première.

**Outil** : `tools/ugc/ugc.py` — le rush filmé entre comme scène `clip`, entouré du produit réel, des
cartons et de la sortie honnête. Une vidéo brute reste une vidéo de téléphone ; le montage en fait une pub.

---

## 6 bis · Les verrous client qui ne se discutent pas (22/10)

Trois règles sont **plus fortes** que le style. Elles viennent du client ou de King, elles sont écrites
ici pour ne plus être redécouvertes après coup :

| Verrou | Verbatim / source | Ce qu'il interdit |
|---|---|---|
| **Aucun prix public** | client, 10/10/2026 : « Pour le prix des montures c'est interdit de le diffuser car nous sommes régit par le ministère de la Santé Publique. » | un prix affiché, « le prix est en ligne », « avec son prix » en sous-titre, un montant en légende |
| **Aucun cardinal de stock** | King, 21/10 : « avoid mentioning the number of frames available everywhere » | « 40 montures », « 400 modèles » — même quand le nombre est vrai |
| **Aucun superlatif non prouvable** | règle de marque | « le meilleur opticien de Douala », « n°1 », « garanti » |

**Et surtout : ces verrous ont un portique.** `tools/qa/audit_claims.py` les vérifie sur tous les
livrables (storyboards JSON, scripts, légendes, sous-titres) et sort en code 1 au premier manquement.

```bash
python3 tools/qa/audit_claims.py clients/dm-optic/content     # doit afficher VERDICT : OK
```

**Pourquoi cet outil existe** : le 22/10, deux vidéos ont été livrées avec une **somme en francs** affichée
et un **cardinal de stock** — deux affirmations fausses au regard de verrous **déjà écrits**. Une règle sans
contrôle n'est pas une règle, c'est une intention. Désormais, toute production passe par ce portique
**avant** le portique mouvement.

## 7 · La règle de source (posée le 22/10)

> **Une statistique sans source primaire nommée n'entre pas dans une décision client.**

Les pages d'agences qui recyclent des chiffres sans les nommer produisent des stratégies sur du sable. Ce
qui est accepté : l'institution nommée (BrightLocal, Litmus, Stanford, Sprout Social, Omnisend), même si
le chiffre n'a pas été revérifié à la source — auquel cas il est **signalé comme non revérifié**.

---

## 8 · Les portes à franchir avant qu'une vidéo sorte

- [ ] Accroche ≤ 3 s, aucune auto-présentation
- [ ] Un seul axe de marque, une seule preuve
- [ ] Aucune promesse médicale, aucun symptôme nommé
- [ ] Aucun tiers nommé (concurrent, marque de monture ou de verre)
- [ ] Un seul CTA
- [ ] Sous-titres manuels relus
- [ ] **Audio dans le fichier**
- [ ] **Portique mouvement : 0 fenêtre figée**
- [ ] Relu par le client — rien n'est publié sans lui

---

## 9 · Ce que cinq vidéos du 23/10 changent dans la fabrication (lot [46])

> Source : `research/YouTube-Lessons.md` lot [46]. Cinq vidéos lues en transcription (pas vues) :
> Facebook 2026, publicité Meta, trois méthodes Instagram. **Ne s'applique qu'après le ruling de
> publication habituel** : rien ne sort sans validation de King.

### 9.1 · Les cinq gestes adoptés

| # | Geste | Pourquoi (source) | Coût |
|---|---|---|---|
| 1 | **Aucun filigrane** (TikTok/YouTube) sur une vidéo publiée sur Facebook ou Instagram ; export propre | Meta ne promeut que l'**original** et déteste les filigranes (Social Media Examiner, 16/04/2026) | 0 — c'est un réglage d'export |
| 2 | **Accroche de 3 secondes**, avec les **mots-clés prononcés** dedans | 3 s = temps de décision ; Instagram lit l'audio (FrenchStartupper ; HubSpot France) | 0 — le premier temps du gabarit |
| 3 | **Lire la courbe de rétention** après chaque pièce : à quelle seconde on décroche, et ce qu'on disait | la donnée corrige la pièce suivante (FrenchStartupper) | 5 min par pièce |
| 4 | **Légende explicite** : le métier, la ville, l'usage — jamais « ambiance » | Instagram lit la légende pour classer (HubSpot France) | 0 — on écrivait déjà des légendes |
| 5 | **2 hashtags de niche + 2 locaux + 2 tendance**, **géotag systématique**, **alt text** à la publication | visibilité locale et accessibilité (HubSpot France) | 2 min par pièce |

### 9.2 · Ce qui ne change pas

- **Deux pièces par semaine** (dim 19 h, lun 13 h pour AMK ; mar/jeu pour DM). Aucune vidéo ne justifie de
  passer à un post par jour : le seul exemple de réussite cité (FrenchStartupper) a mis **plus d'un an**
  avant le premier déclic.
- **Le gabarit en 5 temps** (W43 §12) reste la porte. L'accroche de 3 s est **le premier des cinq temps**,
  elle ne s'y ajoute pas comme un sixième.
- **Aucun chiffre sans source, aucun délai promis, aucun prix, aucun visage** sans ruling : les vidéos ne
  changent pas les verrous.

### 9.3 · La tension à trancher par King

Trois des cinq vidéos placent **le visage face caméra** en tête des formats qui marchent. Notre §6 ne l'a
pas tranché. Tant que ce n'est pas tranché, la production part sur **ce qui ne montre personne** : écran,
mains, documents, lieux, texte animé. Ce n'est pas un refus — c'est l'attente d'une décision.

---

## 10 · Journal des sources — « lu, adapté, intégré, et où »

> **Pourquoi cette section existe.** King, 23/10 : *« where did you write this "les deux documents lus,
> adaptés, intégrés" ?? you need to write it somewhere so that we don't forget that's what the knowledge
> base is for ».* Sans ce journal, une source lue reste dans un tour de conversation : elle est perdue
> au tour suivant, et le dépôt ne sait pas qu'il la sait. **Toute source reçue entre ici le jour où elle
> est lue**, avec l'endroit exact où elle a atterri — et ce qu'on en a écarté.

| Date | Source | Ce qu'on en a pris | Où ça vit maintenant | Écarté (et pourquoi) |
|---|---|---|---|---|
| 23/10 | **Short-Form Storytelling (Writing Guide)** — Kallaway, PDF 3 p., reçu de King | le gabarit 9 blocs ; les 6 principes d'écriture ; les 6 mécaniques de lock-in ; les 4 S du hook | §3 bis, §3 ter | la fourchette 45–90 s, appliquée aux explications seulement (§5 ter, règle 2) |
| 23/10 | **100 Viral Hooks** — BrandIt, PDF 16 p., 99 hooks, reçu de King | la **structure** des 99 accroches → 15 hooks adaptés au cabinet | §3 ter | les hooks anglais tels quels (ils sonnent faux et ne parlent pas de Bonabéri) |
| 23/10 | Capture **@kallawaymarketing** (schéma du format) | confirmation visuelle de l'ordre des blocs + le « lead magnet aligné » dans le CTA | §3 bis, §5 bis | — |
| 23/10 | Capture **@ameliagonzamonte** (« posting for viral ») | le principe : type de contenu choisi **par objectif** ; l'urgence douce, jamais la peur | §4 bis | les catégories non transposables (thought leadership B2B US) |
| 23/10 (2ᵉ lecture) | **Même capture @ameliagonzamonte**, relue à la demande de King (« read, research, adapt and learn ») | la matrice **format → objectif** descendue au niveau du geste : les 6 formats traduits en tournages possibles avec un téléphone, et le test « qu'est-ce qui ne pourrait exister qu'ici ? » | §4 ter | les **prédictions** (autorité de marché inventée + promesse de santé déguisée) et les **réactions** (pas d'actualité optique suivie) |
| 23/10 | **Deya**, *how to send contracts & invoices* (2022) | les 7 lignes de contrat + l'échelle d'impayé | `sales/AMK-Sales-Playbook-v2.md` Addendum 5 · `sales/REVUE-CONTRATS-GRILLE-2026-09-23.md` | ses outils (Wise, HelloSign, Dubsado, Wave) : inutilisables ici |
| 23/10 | **Adam Erhart**, *Marketing & Sales Strategy for Service Business* (2025) | langage de la ligne d'arrivée · caractéristique → bénéfice · tunnel CASE | `sales/AMK-Sales-Playbook-v2.md` Addendum 5 | son anecdote « agenda rempli en 2 semaines » : cas unique, pas une preuve (§1g) |

**La règle d'écriture de ce journal :** une ligne par source, **le jour où elle est lue**, avec la
section qui la porte. Une source sans ligne ici n'est pas dans le dépôt — même si on s'en souvient.

### 10 bis · La procédure (règle King, 23/10) — le journal s'ouvre **à la réception**, pas à la fin

King, 23/10 : *« Ouvre le journal des sources à chaque nouvelle vidéo ou PDF. »* Ce n'est pas une
recommandation, c'est l'ordre de travail. À chaque fichier reçu — un PDF, une capture, un zip, une vidéo,
une story — la même séquence, dans cet ordre, avant toute autre chose :

| # | Geste | Où ça s'écrit |
|---|---|---|
| 1 | **la ligne existe d'abord** : date, source, « reçu, pas encore lu » | §10, ce tableau |
| 2 | on lit, et on écrit **ce qu'on en prend** et **ce qu'on écarte** | §10, colonnes 3 et 5 |
| 3 | on nomme **la section qui le porte** — si aucune section ne le porte, on en crée une | §10, colonne 4 |
| 4 | ce qui devient une **règle** est écrit au §correspondant, pas seulement au journal | la section ellemême |

**Pourquoi cet ordre.** Une source lue mais non journalisée disparaît au tour suivant ; une source
journalisée mais non atterrie est un décor. La ligne 1, posée avant la lecture, est ce qui empêche les
deux. Depuis le 23/10, le journal couvre **les vidéos et les fichiers de travail aussi**, pas seulement
les textes de méthode : le zip de l'outil de factures a sa ligne, la capture WhatsApp du client a la
sienne.

| 23/10 | **`amk-factures-pwa.zip`** — l'outil de factures de King | l'inventaire réel de l'outil (échéance, proforma, reçu, MoMo/OM/banque, modèles) — et la leçon : **lire le code avant de dire ce qui manque** | `ops/amk-factures-pwa/` · `ops/FACTURATION-2026-10-24.md` §3 bis | ses deux affirmations de ma part sur des manques inexistants : corrigées, pas reprises |
| 23/10 | **Captures Facebook + TikTok du post « lunettes pour enfants »** (poster, 23/10) | le texte de la légende Facebook (structure « accroche → preuve mesurable → adresse ») et la confirmation que le même visuel tourne sur les deux réseaux | §5 quater · `ANALYSE-POST-1` §4 bis | le visuel généré : il reste, mais il ne se refait pas (pas de visage inventé) |
| 23/10 | **Correction King : « plus personne ne lit le journal »** (23/10, à propos de la vidéo n°3) | la règle du décor : tout objet filmé doit avoir été vu cette semaine à Douala — et le remplacement du journal par le téléphone | §5 quinquies | le geste de manuel occidental, pris sans vérification |
| 23/10 | **Ruling King : « vous demandez, on répond »** (23/10) | la série questions → vidéo → tag, avec l'accord obligatoire avant de taguer | §5 sexies | le tag sans accord, écarté pour la même raison qu'un visage sans autorisation |
| 23/10 | **Insights 24 h du reel** (Facebook Business Suite, TikTok Studio) | la preuve que les deux réseaux ne mesurent pas la même chose : 12 % de lecture moyenne sur Facebook contre 26 % sur TikTok pour le même film | §5 quater | la comparaison brute des vues (227 contre 80) : elle ne dit rien de la qualité |
| 23/10 | **Capture WhatsApp DM OPTIQUE** (13h00, message d'avis du client) | le texte exact de sa demande d'avis, ses liens, et l'heure | `clients/dm-optic/launch/SOLDE-75K-2026-10-23.md` §3 bis | la tentation d'y répondre : c'est un message de masse, pas une question |
| **25/10** | **Capture @kallowaymarketing** (7 slides, reçue de King) | l'arc moderne : départ à **70**, secousse entre 5 et 10 s, **trois cimes**, relâchements, CTA en dernière cime | §3 bis (l'ordre des blocs — l'arc en est la version sociale) · `knowledge/STORY-ARC-2026-10-25.md` · `tools/qa/audit_reel.py` | le « 742 jours / 207 clients » de la slide : cas unique, pas une preuve (§1g) — non repris |
| **25/10** | **« The 5 Content Games »** (texte collé par King ; **ni auteur, ni URL, ni date → tier C**) | les 5 jeux et ce que chacun monétise ; le diagnostic en 4 questions ; `confiance = minutes × pertinence × utilité` ; « pure virality is a trap for games 3, 4, 5 » ; la semaine en 3 rôles | `knowledge/CONTENT-GAMES-2026-10-25.md` (9 sections) · §4 bis (le renvoi) · `sales/SOCIAL-ACQUISITION-PLAYBOOK-2026-10-25.md` §5 quater · `tools/qa/audit_trust.py` | les noms de marques cités (AG1, Meta Ray-Ban) comme exemples de jeu 4 : jamais cités dans un post · les « on-target views » : **non mesurables**, on garde le principe, pas le chiffre |

---

## 11 · Reels explainer — le studio `content/reels/` (25/10/2026)

> *Numéroté §7 par erreur le 25/10 : le §7 de ce document est la **règle de source**. Contenu inchangé.*

Un troisième moteur, à côté de `tools/record/make_dmoptic_tiktok.py` : `content/reels/reelkit.py`.
Il rend un réel vertical complet **sans navigateur, sans tournage, sans capture** — fond, cartes,
pastilles et mascotte dessinés à la volée, frames poussées dans le pipe ffmpeg.

| Ce qu'il fait | Comment |
|---|---|
| 1080×1920 · 30 fps · H.264 + AAC | `Kit.render()` puis `mux()` (voix posée par beat, `adelay` + `amix`) |
| style « post-it » (crème, trame, orange) | `_base()`, `rounded_card()`, `pill()` |
| **arc moderne** (départ à 70, 3 cimes, CTA final) | `BEATS` + `tools/qa/audit_reel.py` — voir `knowledge/STORY-ARC-2026-10-25.md` |
| voix | `generate_speech` par beat → `voice/timing.json` → `voice/build_timing.py` (refuse un clip muet) |

**Deux pièges déjà payés**, à ne pas repayer :

1. **Les quatre `Montserrat-*.ttf` du dépôt sont le même fichier variable.** Sans
   `set_variation_by_name`, PIL rend l'instance par défaut, c'est-à-dire **Thin** — tout « ExtraBold »
   sort maigre. `reelkit.font()` demande l'axe. (C'est la même famille de bug que `set_variation_by_axes`
   au §6 de `CONTENT-LESSONS`.)
2. **`✓` n'est pas dans Montserrat** : une coche se dessine (`reelkit.draw_check`).

**Coût mesuré** : 30 s de rendu pour 23 s de vidéo, 2 dépendances (`pillow`, `imageio-ffmpeg`), zéro
`apt`. C'est ce qui rend le format tenable par un opérateur seul, trois fois par semaine.

**Ce que la v3 a changé (25/10, soir)** : EP01 déclare désormais son **jeu** dans le module
(`TRUST = Piece(role="porte", …)`), et `audit_trust.py` la lit — 23,76 s, **20/125**, plancher de porte tenu,
plancher d'autorité (40) hors d'atteinte par construction. Le relâchement muet de `release2` est devenu
**le conseil gratuit** (« Dix minutes, et c'est gratuit. ») : c'est le seul endroit de l'arc où l'on peut
rendre service sans rien vendre, donc le seul où l'**utilité** s'achète. Détail de fabrication :
`content/reels/README.md` §4.
