# Le registre « éditorial clair » — ce que les trois références font, et ce que j'en garde

```
Décision de King, 22/10 : « great videos with great scripts, we can just translate and adapt and use
them — and as you can see there's no appearance of their staff or even the clinic, AI video for one
and for the other it's full of generated images ».
Traduction : arrêter le montage sombre avec bandeau ; produire comme ces trois-là — fond clair,
produit seul, typographie qui porte le propos — mais avec NOS photos et NOS phrases.
Livré : tools/ugc/editorial.py + spot-02.mp4 + spot-03.mp4.
```

---

## 1 · Ce que j'ai pu vérifier des trois vidéos

| Référence | Ce que c'est | Ce que j'en retiens |
|---|---|---|
| `Yd0S9p59eEg` — *How to Create a Promotional Video for an Optician* (That's Great News, 2013 — pour **Grove Opticians**) | 1 min 24, diaporama de montures détourées sur fond blanc, sous-titres en bandeau, pas de visage, pas de cabinet | **le fond clair**, la monture héros plein cadre, le texte court qui accompagne chaque plan |
| `ZkIlvi7bgOM` — *Wilkin's Opticians Social Media Clip #1* | 17 s, une seule phrase de présentation tenue sur des plans de boutique | **un seul message par vidéo**, pas de catalogue |
| `QVPbqkqdkEA` — *OPTICIANS - REAL APPLICATION* | 19 s, **déclaré « Made with AI »** par YouTube, aucun visage réel | ce sont **des images générées** — exactement ce que tu ne veux pas, et la raison pour laquelle on ne copie pas ce modèle-là |

**Ce qui manque dans les deux premières** et qu'on garde : le vrai nom du cabinet, le vrai numero, le vrai
horaire, et la preuve (les montures photographiées au cabinet). Elles vendent une ambiance ; nous vendons un lieu.

## 2 · Ce que j'ai traduit du texte du `Yd0S9p59eEg` (et ce que j'ai jeté)

Le script de Grove dit, en substance : *« nous produisons des vidéos promotionnelles… YouTube est un vrai
levier… chaque vidéo devient un aimant à ventes… »*. **C'est un discours d'agence, pas une pub** : il parle
du métier de vidéaste, pas du client. On ne le traduit pas — on en garde la **forme** (phrases courtes,
une idée par plan), pas le fond.

Le script de Wilkin's — *« depuis près d'un siècle, Wilkins Opticians s'engage à offrir les meilleurs
services visuels… appelez-nous pour prendre rendez-vous »* — donne une chose utile : **la structure en une
seule promesse + un appel**. Chez nous, la promesse est mesurable : *on montre avant de vendre*.

## 3 · Le registre, en six règles

1. **Fond crème 246,235,225** — exactement le fond des fiches produit. La monture n'est pas posée *sur*
   une carte : elle flotte. Aucun cadre visible.
2. **Détourage réel** (chroma doux + ombre portée). Jamais de rectangle blanc autour d'une monture.
3. **Typographie comme sujet** : Schibsted Grotesk très gras, IBM Plex Mono en petites capitales pour les
   références. Pas de sous-titre en bandeau — le texte **est** l'image.
4. **Aucun visage, aucune image générée.** Photos du cabinet uniquement pour prouver le lieu.
5. **Un seul message par spot**, jamais un catalogue.
6. **Aucun plan ne dépasse 1,9 s.** Ce n'est pas du rythme gratuit : c'est la condition pour que le
   portique ne trouve jamais une fenêtre de 2 s figée (voir §5).

## 4 · Les deux spots livrés

| | **spot-02.mp4** | **spot-03.mp4** |
|---|---|---|
| Titre | « Une monture, ça se choisit au millimètre » | « Trois choses qu'on ne fera pas » |
| Durée | **26,70 s** | **28,40 s** |
| Poids | 12,7 Mo | 14,2 Mo |
| Axe | la méthode : photographié, essayé, mesuré | la sortie honnête : ce qu'on refuse de faire |
| Plans | 15 | 15 |
| Voix | `voice-00` (23,42 s ajustée) | `voice-00` (22,66 s) |
| Son | voix + nappe (accords tenus + souffle sur chaque coupe) | idem |
| Portique mouvement | **OK** | **OK** |
| Portique affirmations | **OK** (`audit_claims.py`) | **OK** |
| Storyboard | `spot-02.json` | `spot-03.json` |

**spot-03 est le plus fort des deux, et c'est volontaire.** « On ne vous vendra pas une monture qui ne
vous va pas » est une phrase qu'aucun concurrent de Bonabéri ne peut copier sans la tenir. C'est notre
axe de marque, mis en images.

## 5 · Ce que le portique a appris au moteur (et pourquoi le découpage est court)

Première version : plans de 3 à 4 s. Verdict : **une fenêtre figée**. Diagnostic, mesuré :

- le portique échantillonne à 12 fps puis **réduit à 270 px de large** ;
- à cette taille, un fond crème qui dérive, un grain fin ou un zoom de 4 % produisent un écart
  **inférieur à 1/255** — invisibles pour la mesure, donc « figé » ;
- une monture détourée qui tourne, elle, produit 2 à 12/255 : la mesure la voit.

**Trois corrections, dans l'ordre :**

| Correction | Effet mesuré |
|---|---|
| bande de lumière diagonale traversant le fond + zoom lent de la couche typographique | 0,4 → 1,7/255 |
| grain aléatoire par image (2/255) | ajoute du bruit réel, pas du banding |
| **découpage : aucun plan > 1,9 s** (garde-fou `MAX_PLAN` dans le code) | chaque fenêtre de 2 s contient une coupe |

Le garde-fou est **bloquant** : si un storyboard contient un plan trop long, le moteur refuse de rendre et
dit lequel. C'est la leçon la plus utile de la soirée : à 270 px, un carton crème de 3 s n'existe pas.

## 6 · Reproduire, modifier, décliner

```bash
# les deux spots tels quels
python3 tools/ugc/editorial.py --out clients/dm-optic/content/month1/w1/spot-02.mp4 \
        --voice clients/dm-optic/content/month1/w1/assets/spot-02-voix.mp3

python3 tools/ugc/editorial.py --story clients/dm-optic/content/month1/w1/spot-03.json \
        --out clients/dm-optic/content/month1/w1/spot-03.mp4 \
        --voice clients/dm-optic/content/month1/w1/assets/spot-03-voix.mp3

# puis, toujours
python3 tools/qa/audit_video_motion.py <fichier>     # doit sortir en code 0
```

**Types de scène disponibles** : `type` (carton typographique), `frame` (une monture héros),
`row` (trois montures en planche), `inset` (photo du cabinet dans une carte arrondie),
`dark` (carton nuit), `end` (carton de marque avec logo, horaires, WhatsApp).

**Pour décliner sur un autre client** : changer la palette (`CREAM`, `INK`, `EMBER` en tête de fichier),
les polices dans `assets/fonts/`, et les scènes. Rien n'est codé en dur sur DM Optique sauf le storyboard.

## 6 bis · Correction du 22/10 — aucun prix, et un portique pour l'imposer

King a relevé l'erreur : **les prix ne sont pas publics chez DM Optique**, c'est un verrou du client
depuis le 10/10 (« c'est interdit de le diffuser car nous sommes régit par le ministère de la Santé
Publique »). La v1 de `spot-03` disait « on ne garde pas le prix pour la caisse », la v1 de `spot-02`
« avec son prix », et `ugc-03` allait jusqu'à montrer « le prix affiché ». **Trois livrables à corriger.**

| Corrigé | Avant | Après |
|---|---|---|
| `spot-02` | « Avec son prix. » | « Avec sa référence. » |
| `spot-03` | « 3. On ne garde pas le prix pour la caisse. » | « 3. On ne vous laissera pas choisir sans essayer. » |
| `spot-03` (2ᵉ occurrence) | « Ce prix-là. » | « Sur vous. » |
| `ugc-03` | « 40 montures / le prix affiché / ce prix en photo » | « chaque monture / en photo, au cabinet / ce que vous voyez est au cabinet » |

Et pour que ça ne recommence pas : **`tools/qa/audit_claims.py`**, portique bloquant qui refuse un
livrable contenant un prix consultable, un cardinal de stock, un superlatif non prouvable ou une
allégation médicale. Il tourne sur tout `clients/dm-optic/content` et sort en code 1.

> **La leçon, écrite pour de bon** : le verrou existait dans le dépôt (`onboarding/post-deposit-email.md`,
> `launch/SETUP-FACEBOOK.md` §145, `posting-calendar.md` §297) mais **n'était pas dans les règles de
> rédaction de contenu**. Une règle rangée dans un dossier que personne ne relit n'est pas une règle.

## 7 · Ce qui reste à décider (King)

1. **Laquelle part en premier ?** Ma recommandation : **spot-03** (la sortie honnête) — c'est celle qui
   nous distingue, et elle ne dépend d'aucune promotion.
2. **Format** : 1080×1920, prêt pour TikTok et Reels. Pour Facebook, un carré 1080×1080 serait à produire
   (le texte tomberait autrement) — dis-moi si tu le veux.
3. **La voix** : `voice-00` tient très bien. Ta voix, ou celle d'un agent, rendrait le propos plus crédible
   encore — dix minutes d'enregistrement par mois suffisent.
