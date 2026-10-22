# AMK — notre propre présence : état réel et plan

```
Date     22/10/2026
Constat  on passe le mois à construire la présence des autres. La nôtre est en retard d'un cran —
         et c'est elle qui vend les suivants.
Règle    mêmes règles que pour un client : pas de prix public, pas de délai promis, pas de preuve inventée.
```

---

## 1 · Ce qui existe vraiment (vérifié dans le dépôt et en ligne)

| Canal | État | Détail |
|---|---|---|
| **Instagram** | ✅ existe — `@amkweb.cm` | 6 abonnés · 5 posts · 122 vues/30 j (relevé 08/10) · **anglais seul** |
| **Facebook** | ⚠️ **une page `@amkweb` semble déjà exister** | citée dans `ops/TOOL-SCAN.md` comme « Page existante ». **À vérifier avant d'en créer une autre** |
| **TikTok** | ✅ existe | vidéos v01–v04 (septembre) · audience 18–34 ans à 86–91 %, Cameroun ≈ 99 % |
| **Site** | ✅ en ligne | `amk-cm.vercel.app` — audit séparé : `site/OPTIMISATION-2026-10-22.md` |
| **Threads** | ❓ lien `alex_aiproductlab` dans la bio IG | aucune trace au dépôt : voulu ou résiduel ? |

**À vérifier en premier, 5 minutes :** ouvrir `facebook.com/amkweb`. Si la page existe, **on ne la recrée pas** — on la finit (nom, bio, bouton, liens, couverture). Créer une deuxième page pour la même activité, c'est se couper en deux aux yeux de Facebook et de Google.

---

## 2 · Les sept corrections d'Instagram (relevées le 08/10, toujours valables)

| # | Constat | Pourquoi c'est grave | Correction |
|---|---|---|---|
| 1 | « **100 000 F** » affiché sur un post | Règle du 08/10 : **aucun prix public** | retirer (11 vues : le coût du retrait est nul) |
| 2 | « Only **2 founding clients this month** » | daté de septembre, donc périmé en octobre | supprimer ou remplacer |
| 3 | « **live in 3–5 days** » | délai non tenu — le mois de DM Optique le prouve | retirer (voir aussi le site, même défaut) |
| 4 | Bio « **24h** homepage preview » | promesse plus large que le processus réel | « aperçu sous 24 h ouvrées, envoyé sur WhatsApp » |
| 5 | **Anglais seul** alors que la cible lit français | les concurrents locaux publient en français | **FR à l'écran, EN en légende** |
| 6 | Posts « ce qui ne va pas avec les sites » | V2 du 05/10 : plus de contenu *product-led* | passer aux quatre piliers (§4) |
| 7 | Lien Threads `alex_aiproductlab` | profil qui ne nous appartient pas visiblement | vérifier, sinon retirer |

---

## 3 · La page Facebook — le kit de finition

Si la page n'existe pas, on la crée avec exactement ces valeurs. Si elle existe, on remplace ce qui diffère.

| Champ | Valeur à mettre |
|---|---|
| **Nom** | `AMK · Sites web pour écoles & cliniques` |
| **Catégorie** | Agence de marketing / Concepteur de sites web |
| **Bio (155 car.)** | `Sites web bilingues FR\|EN pour écoles, cliniques et opticiens au Cameroun. Aperçu gratuit sur WhatsApp. Basés à Douala.` |
| **Bouton** | **Envoyer un message WhatsApp** → `wa.me/237677789631` + message pré-rempli |
| **Site** | `https://amk-cm.vercel.app` |
| **Photo** | logo AMK sur fond plein (lisible en 40 px) |
| **Couverture** | une **vraie** capture d'un site livré, avec mention du client **seulement s'il a donné son accord** |
| **Horaires** | réels, sept jours — une page sans horaires paraît abandonnée |

> **⚠️ Arbitrage du 22/10 (tour 56) :** la recherche sur les règles de nommage de Meta recommande le nom
> court **`AMK`** plutôt que le nom long de ce tableau — voir **§9.2**. Le reste des champs ci-dessus tient.

**⚠️ Le détail qui compte :** le site affiche aujourd'hui **`akwo.king.dev@gmail.com`**. Pour une agence qui vend de la présence web, une adresse Gmail personnelle est le premier signe qui contredit la promesse. Une adresse sur le domaine (`contact@…`) vaut mieux que n'importe quel argument.

---

## 3bis · Vérifier la page en 60 secondes (fait le 22/10 : impossible d'ici)

**Ce que j'ai essayé, et ce que ça a donné :** ouvrir `facebook.com/amkweb` par requête automatique →
**HTTP 403**. Facebook ferme l'accès aux robots ; sans navigateur, la vérification est impossible depuis
le bac. Le dépôt contient pourtant une trace : `ops/TOOL-SCAN.md` parle, le 10/10, d'une « **Page
existante `@amkweb`** » — c'est une note interne, pas une preuve. **On ne sait donc pas, ce soir, si la
page existe.** La question se tranche en une minute, sur un téléphone :

1. Ouvrir `facebook.com/amkweb` dans un navigateur, **sans être connecté**.
2. Trois issues possibles :

| Ce que tu vois | Ce que ça veut dire | Ce qu'on fait |
|---|---|---|
| La page AMK, avec ses anciens posts | **elle existe** | on ne crée rien. On la finit : §3 ci-dessus, champ par champ. Si tu es le propriétaire, vérifier aussi que le nom d'utilisateur `@amkweb` est bien le sien |
| « Cette page n'est pas disponible » | le nom d'utilisateur est **libre** ou appartenait à une page supprimée | on crée la page (§3), et on prend `@amkweb` si Facebook le propose |
| La page d'une **autre** entreprise | le nom est **pris** | on crée avec un autre identifiant (`@amkcm`, `@amk.douala`) — **jamais** en imitant celui d'un autre |

**Piège à connaître** : une page Facebook exige un **profil personnel réel** pour être créée (pas un
e-mail seul), et un profil au nom de l'entreprise fait tomber la page. C'est déjà écrit pour DM Optique
dans `clients/dm-optic/launch/SETUP-FACEBOOK.md` §1 — la même règle s'applique ici : création depuis le
profil de King, page placée dans un portefeuille Meta `AMK`, 2FA activée.

**Ce qu'on ne fait pas** : créer une deuxième page « pour voir ». Deux pages pour la même activité, c'est
se couper en deux aux yeux de Facebook et de Google — et c'est plus difficile à réparer qu'à éviter.

---

## 4 · Les quatre piliers de contenu AMK

Ce que nous avons et que personne n'a ici : **des sites réels, ouverts dans un téléphone**, et un mois de méthode documentée.

| Pilier | Ce que ça dit | Exemple de pièce |
|---|---|---|
| **1 · La preuve ouverte** | « ouvrez, c'est en ligne » | la page d'un site livré, filmée au doigt, en 20 s |
| **2 · Le test que le lecteur peut faire** | « écrivez à votre page, chronométrez » | le test du message sans réponse |
| **3 · Le métier, sans jargon** | ce qu'est un site utile, en une idée | « un site n'est pas une brochure, c'est une réponse » |
| **4 · Les coulisses de la méthode** | comment on travaille, ce qu'on refuse | « pourquoi on ne promet pas de délai » |

**Ce qu'on ne fait plus** : expliquer ce qui ne va pas chez les autres. Ça marche une fois et ça vieillit mal.

---

## 5 · Huit pièces prêtes à écrire (dimanche / lundi)

| # | Jour | Pilier | Titre | Angle |
|---|---|---|---|---|
| 1 | dim | 1 | **« Ouvrez. C'est en ligne. »** | un site livré, filmé du pouce, sans commentaire |
| 2 | lun | 2 | **« Chronométrez votre page. »** | le test du message sans réponse, 30 s |
| 3 | dim | 3 | **« Un site ne se juge pas à son design. »** | il se juge à la question qu'il répond |
| 4 | lun | 4 | **« Pourquoi je ne promets pas de date. »** | l'honnêteté comme argument, pas comme excuse |
| 5 | dim | 1 | **« Ce que voit un client avant d'appeler. »** | le parcours réel : Google → site → WhatsApp |
| 6 | lun | 2 | **« Votre site sur un téléphone en 3G, à 20 h. »** | le test du vrai terrain |
| 7 | dim | 3 | **« Bilingue, ça veut dire deux pages. »** | pas un bouton de traduction |
| 8 | lun | 4 | **« Ce qu'on ne met pas sur un site d'école. »** | le refus qui rassure |

**Les trois carrousels déjà rendus** (`content/carousels/POST-READY.md` : `c01`, `c02`, `c03`) servent de **stock d'avance** — ils sont prêts, il ne manque que la publication. On les place en semaine 1 et 2, pas en plus : **ils remplacent, ils ne s'ajoutent pas.**

---

## 6 · La cadence, et ce qu'elle remplace

| Jour | Heure | Quoi |
|---|---|---|
| **Dimanche** | 19 h | une pièce de fond (pilier 1 ou 3) |
| **Lundi** | 13 h | une pièce courte (pilier 2 ou 4) |

**Conflit à trancher :** le calendrier du 08/10 prévoyait **mardi/jeudi 19:25 (carrousels) + samedi (Reel)**. On ne peut pas tenir les deux. Je propose de **remplacer** l'ancien calendrier par celui-ci — il est plus simple, il tient sans réunion, et il repose sur ce qu'on sait produire seul.

**Ce qu'il faut avant de commencer :** deux pièces d'avance. On les a déjà (les trois carrousels). Donc **la semaine 1 peut démarrer tout de suite.**

---

## 7 · La mesure

Quatre chiffres, les mêmes que pour un client :

1. messages WhatsApp reçus et **qualifiés** (« aperçu », nom de l'établissement) ;
2. abonnés gagnés — pas le total, le **delta** ;
3. vues à 3 s sur les vidéos ;
4. contacts ayant enregistré le numéro.

**Ce qui ne compte pas** : les likes, la portée, le nombre de posts. Un compte de 6 abonnés qui reçoit deux messages qualifiés par semaine vaut mieux qu'un compte de 500 qui n'en reçoit aucun.

---

## 8 · L'ordre des opérations

1. **Vérifier** si la page Facebook `@amkweb` existe (5 min).
2. **Nettoyer Instagram** : les sept points du §2 (30 min).
3. **Finir la page Facebook** : bio, bouton WhatsApp, liens, photo (30 min).
4. **Ajouter nos liens sur notre site** — le même oubli qu'on vient de corriger chez DM Optique (30 min).
5. **Publier la première pièce** dimanche 19 h.
6. **Tenir quatre semaines** sans changer les jours.

Rien de tout ça ne demande de production nouvelle : **tout est déjà écrit ou rendu.**

---

## 9 · La page Facebook : la procédure (22/10, tour 56) — 40 minutes, écran par écran

> **Origine.** King (22/10) : « creating ourselves a facebook page, research on how we can best do it so as
> to optimise it, I'll send screenshots as we go ahead just let me know when you are ready ».
> **État de la recherche :** faite le 22/10 sur les sources listées au §11. Ce qui n'a pas pu être vérifié
> d'ici (la page `@amkweb`, la fiche Google) est dit tel quel.
>
> **Pourquoi Facebook d'abord, et pas Instagram.** Au Cameroun (NapoleonCat, 09/2026) : **≈6,84 M
> d'utilisateurs Facebook** (21,9 % de la population) contre **≈637 000 sur Instagram** — dix fois moins.
> StatCounter (09/2026) donne **85,5 % de part du social mobile** à Facebook. Notre cible (directeur
> d'école, gérant de clinique, opticien) est sur Facebook ; sur Instagram, il n'y est pas.

### 9.0 · Avant de toucher à quoi que ce soit (5 minutes)

| # | Prérequis | Pourquoi | État |
|---|---|---|---|
| 1 | **Un profil personnel Facebook** (le tien) | Meta **exige** un profil humain pour administrer une page — c'est technique, pas une préférence | à confirmer |
| 2 | **Double authentification activée** sur ce profil | une page perdue = tout l'historique perdu ; le seul vrai risque de l'opération | à faire |
| 3 | **Le numéro `677 789 631`** sous la main (WhatsApp Business) | c'est le bouton de la page ; il doit être joignable | ✅ |
| 4 | **Logo carré 1024 × 1024 px** | `brand/AMK-logo-square.png` existe — vérifier qu'il reste lisible à 40 px | ✅ fichier |
| 5 | **Une capture d'un site livré** pour la couverture | « le site ne montre que du vrai » : pas d'image d'illustration achetée | ⏳ |
| 6 | **`contact@` sur le domaine** (ou au minimum l'adresse Gmail assumée) | §3 : une adresse Gmail perso contredit la promesse | ⏳ |

### 9.1 · La question qui décide de tout : une page, un profil, ou les deux ?

La recherche du 22/10 est claire sur un point que la plupart des guides ratent : **ce sont deux actifs
différents, pas deux versions du même.**

| | **Page AMK** | **Profil de King en mode pro** |
|---|---|---|
| Ce que c'est | l'**entreprise** : preuve, offres, avis, horaires | **toi** : la voix, le parcours, les leçons |
| Ce que ça sert | convertir un prospect qui vérifie (« c'est qui ces gens ? ») | créer l'audience : les gens suivent une personne, pas une agence |
| Portée organique | faible, sauf vidéo | **plus forte** : un profil parle à des amis et à leurs amis |
| Ce que le public peut faire | suivre, recommander, écrire | suivre (mode pro rend le profil public), commenter |
| Risque | aucun (c'est fait pour ça) | **confidentialité** : le mode pro rend le profil public par défaut |
| Rôles | plusieurs admins possibles | un seul propriétaire |

**Décision recommandée : les deux, avec deux rôles séparés.**
1. **La page AMK** = la vitrine qu'on envoie dans un message de prospection (« voilà ce qu'on fait »).
2. **Ton profil en mode pro** = la communauté (point 2 de ta demande) : les réalités, les chiffres, les
   erreurs, les arbitrages. Les gens s'abonnent à une personne qui traverse ce qu'ils traversent.
3. **DM Optique** garde la sienne : commerce local, montures, patients. Trois pages, trois métiers —
   mais **une seule voix** : la tienne.

⚠️ **Le mode pro rend le profil public.** Tes anciens posts gardent leur audience d'origine ; les
nouveaux sont publics par défaut. À décider en connaissance de cause, pas par défaut.

### 9.2 · Création de la page — les valeurs exactes

Aller directement à **`facebook.com/pages/create`** (plus court que le menu).

| Étape | Ce que Meta demande | Ce qu'on met | Pourquoi |
|---|---|---|---|
| 1 | Type | **Public Page** → *Business or Brand* | une « Community Page » ne peut pas être fusionnée avec une entreprise |
| 2 | **Nom** | ⚠️ **voir l'arbitrage ci-dessous** | c'est le champ le plus difficile à changer |
| 3 | **Catégorie principale** | **Concepteur de sites web** (*Web designer*) | décrit ce qu'on vend, pas ce qu'on est |
| 4 | Catégories secondaires | *Marketing agency*, *Website designer*… | 3 maximum ; Meta permet d'en ajouter après |
| 5 | **Bio (255 car.)** | `Sites web bilingues FR`\|`EN pour écoles, cliniques et opticiens au Cameroun. Aperçu gratuit sur WhatsApp, sous 24 h. Douala.` | le mot-clé + la promesse tenable |
| 6 | **Photo de profil** | `AMK-logo-square.png` (1024²) | lisible en 40 px, pas de texte fin |
| 7 | **Couverture** | 1640 × 624 px, zone utile centrée 820 × 312 | le mobile recadre : rien d'important sur les bords |
| 8 | **Adresse** | Douala, Cameroun *(pas l'adresse exacte si tu travailles de chez toi : quartier suffit)* | **obligatoire pour activer les Recommandations** |
| 9 | **Horaires** | les vrais, sept jours | une page sans horaires paraît abandonnée |
| 10 | **Site** | `https://amk-cm.vercel.app` | + la fiche Google quand elle existera |

**⚠️ L'arbitrage sur le nom.** Le §3 de ce document proposait `AMK · Sites web pour écoles & cliniques`.
La recherche du 22/10 dit l'inverse : Meta refuse les noms qui ressemblent à un slogan, et un refus de
nom bloque la page plusieurs jours. **Recommandation : nom = `AMK`**, et les mots-clés vont dans la
catégorie, la bio et les publications. Si tu préfères le nom long, on le tente — mais on le tente **en
connaissance du risque**, et on ne crée pas de deuxième page en cas de refus : on renomme.

### 9.3 · Les réglages qui font la différence (10 minutes, après la création)

| Réglage | Où | Ce qu'on met |
|---|---|---|
| **Nom d'utilisateur** | Paramètres → Page → Nom d'utilisateur | `@amkweb` **s'il est libre ou s'il est déjà à nous** ; sinon `@amk.cm` / `@amkcm` |
| **Recommandations** | Paramètres → Confidentialité → Publications et étiquetage | **ACTIVER**. Sans ça, aucun avis n'apparaît — et une page neuve a besoin de ses 5 premiers |
| **Messagerie** | Boîte de réception → Réponses automatiques | message d'accueil **FR + EN**, réponse d'absence « nous répondons sous 24 h ouvrées » |
| **Modèles et onglets** | Modifier → Modèles et onglets | modèle **Service** ; onglets Avis, Photos, À propos visibles |
| **Rôles** | Tableau de bord pro → Accès à la page | **deux admins** (toi + un compte de secours) ; jamais un seul |
| **Meta Business Suite** | business.facebook.com | crée le **portefeuille** : planification, stats, futures pubs |
| **Lier WhatsApp** | Paramètres → WhatsApp | `wa.me/237677789631` avec message pré-rempli |
| **Bouton d'action** | Modifier → Bouton | **« Envoyer un message WhatsApp »** — pas « Appeler » : on écrit, on n'appelle pas |
| **Traductions** | Publication → Rédiger dans plusieurs langues | FR principal, EN secondaire, quand l'option apparaît |

### 9.4 · Les dix premiers posts (deux par semaine, pas plus)

Rien à produire : **tout existe déjà** (§5). Chaque post porte **un pilier** et **une preuve** — la règle
du 22/10 (§1g, règle 2) : un contenu sans preuve est joli, pas utile.

| # | Pilier | Le post | La preuve qu'il porte |
|---|---|---|---|
| 1 | Présentation | « On fait des sites pour les écoles et cliniques du Cameroun. Voilà à quoi ressemble le nôtre. » + lien | le site lui-même, 3 pages |
| 2 | Le geste utile | « Comment savoir si votre site est lisible sur un téléphone » — 3 captures réelles | nos pages, pas des maquettes |
| 3 | La preuve | un site concept ouvert en direct, une capture, le lien | `sample-school`, `clinic-bonaberi` |
| 4 | Le coulisse | comment on écrit une page d'école : la question qu'on pose au directeur d'abord | méthode, pas outil |
| 5 | La sortie honnête | « Si votre page Facebook vous suffit, ne payez pas un site. » | cohérence avec le site |
| 6 | Le geste utile | ce qu'un parent cherche sur le site d'une école en 10 secondes | les 3 infos des pages métier |
| 7 | La preuve | capture de l'audit du 22/10 : « voilà ce qu'on corrige avant de livrer » | `site/OPTIMISATION-2026-10-22.md` §9 |
| 8 | Le coulisse | combien de temps prend vraiment un site (sans promettre de délai : ce qu'on a mesuré) | nos commits |
| 9 | La sortie honnête | « Vous n'avez pas besoin de publicité payante pour commencer » | la fiche Google d'abord |
| 10 | La demande | « Dites-moi votre métier en commentaire, je vous dis quelle page ouvrir en premier » | conversation, pas un formulaire |

**Cadence** : dimanche 19 h + lundi 19 h (le §6), quatre semaines sans changer les jours. Adam Blakey
(22/10) : *« si tu ne peux faire que trois bonnes vidéos par semaine, fais trois, pas cinq moyennes »*.

### 9.5 · Ce qu'on ne fait pas sur cette page (et pourquoi)

| Interdit | Raison |
|---|---|
| Acheter des abonnés | détruit le taux d'engagement, et Meta le détecte |
| Demander un avis en échange d'une remise | interdit par la politique de Meta : l'avis est supprimé, parfois la note avec |
| Publier un prix | verrou maison (aucun tarif sur nos canaux) |
| Promettre un délai de livraison | le mois de DM Optique l'a prouvé |
| Republier une vidéo TikTok avec son filigrane | Meta rétrograde le contenu recyclé |
| « Commentez pour recevoir le PDF » | Meta a historiquement rétrogradé le *engagement bait* — une question honnête marche mieux |

### 9.6 · Ce qu'on mesure à 30 jours (et ce qu'on ne conclut pas avant)

| Chiffre | Seuil de décision | Ce qu'on en fait |
|---|---|---|
| **Messages WhatsApp qualifiés** (« aperçu », nom de l'établissement) | **≥ 3 en 30 jours** | c'est le seul chiffre qui paie |
| Abonnés (delta) | pas un objectif | on le note, on ne le vise pas |
| Vues à 3 s sur les vidéos | ≥ 50 % | sinon le problème est l'accroche, pas la portée |
| Partages | ≥ 1 par post utile | le partage est le seul signal qui amène des non-abonnés |
| Recommandations (avis) | **≥ 5** pour que la note s'affiche | on les demande après un livrable, jamais avant |

**Ce qu'on ne conclut pas** : un compte neuf tourne **30 à 50 % sous les moyennes publiées** pendant
ses 90 premiers jours (benchmarks 2026). Juger à 30 jours, décider à 90.

---

## 10 · Protocole captures d'écran (ce que j'attends, dans l'ordre)

Envoie **une capture par étape**, nommée comme ci-dessous — je vérifie chaque écran avant que tu passes au
suivant, et je te dis « continue » ou « corrige ce champ ».

| # | Fichier | Ce que je vérifie dessus |
|---|---|---|
| 0 | `00-page-existante.png` | `facebook.com/amkweb` : la page est-elle à nous, à quelqu'un d'autre, ou inexistante ? **(à faire avant tout le reste)** |
| 1 | `01-creation-nom.png` | le nom exact, la catégorie, le type de page |
| 2 | `02-bio.png` | les 255 caractères, les deux langues, pas de prix, pas de délai |
| 3 | `03-photo-couverture.png` | lisibilité en petit, rien de coupé sur les bords |
| 4 | `04-coordonnees.png` | adresse (pour les Recommandations), téléphone, site, horaires |
| 5 | `05-bouton.png` | bouton WhatsApp + message pré-rempli |
| 6 | `06-recommandations.png` | l'interrupteur **activé** |
| 7 | `07-acces.png` | deux admins, rôles corrects |
| 8 | `08-parametres-langue.png` | langue de la page, pays, restrictions d'âge |
| 9 | `09-premier-post.png` | avant publication : le texte, l'image, le premier commentaire |
| 10 | `10-statistiques.png` | à J+7 : portée, abonnés, clics — pour la première mesure |

**Ce que je ne peux pas vérifier d'une capture** : le rendu réel sur un autre téléphone, le comportement
du bouton WhatsApp (il dépend de l'app installée), et l'existence d'un doublon de page. Ces trois-là se
vérifient à la main, en cinq minutes.

---

## 11 · Sources (lues le 22/10/2026)

- **Création et réglages** : `facebook.com/pages/create` · Hootsuite, *How to create a Facebook Business
  Page* (02/10/2026) · Meta, *Turn pro mode on or off for your Facebook profile* (`facebook.com/help/2978174759158711`)
  · Meta Business Help, *How to turn on pro mode* (`facebook.com/business/help/545581016154662`).
- **Recommandations** : Meta, *How Page review count and recommendation score are determined* (cité par
  cloutly.com, 09/2026) · wisernotify.com (01/10/2026) · reviewgen.ai (17/06/2026).
- **Audience Cameroun** : NapoleonCat, *Facebook users in Cameroon* (09/2026 : 6 844 400 ; 21,9 %) et
  *Social media users in Cameroon* (08/2026 : Instagram 637 100, Messenger 6 900 000, LinkedIn 1 805 000)
  · StatCounter, *Mobile social media stats Cameroon* (09/2026 : Facebook 85,5 %).
- **Monétisation — le fait qui change la stratégie** : le programme *Facebook Content Monetization* n'est
  **pas** ouvert au Cameroun (tamtamugc.com, vérifié 08/2026 ; lilachbullock.com, 17/10/2026, qui cite la
  liste de pays Meta). **Conséquence : on ne construit pas cette page pour être payé par Meta.**
- **Comparaisons internationales** : Socialinsider / iqfluence (08/2026 : 4,40 % d'engagement pour les
  comptes de 1 000 à 5 000 abonnés) · growth-onomics.com (23/08/2026) · improvado.io (28/08/2026 :
  30–50 % sous les moyennes pendant les 90 premiers jours).
- **Non vérifié d'ici** : l'existence réelle de `facebook.com/amkweb` (403 pour tout robot), la fiche
  Google d'AMK, et le nom exact qu'elles portent aujourd'hui.
