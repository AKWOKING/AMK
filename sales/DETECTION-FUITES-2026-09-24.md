# DÉTECTION DES FUITES — lire les avis publics pour trouver **ce qui coûte** au prospect

**24/09/2026 · lot [35]** · deux vidéos envoyées par King, sans texte :
`JLGHhsfzf7g` (« Their Reviews Show How Much Money They're Losing (I Built the Fix) », **Automate AI
Consulting**) et `CsXKAC4iYG4` (« Social Intelligence », audiobook — voir §8, traité à part).

**En trois lignes.** La première vidéo donne une façon de **trouver l'angle d'approche dans les avis
publics** : chercher la plainte **qui se répète**, en déduire la fuite de processus, et arriver avec
*« voici ce que ça vous coûte »* au lieu de *« je fais des sites web »*. C'est exactement ce que notre
dépôt dit depuis le 23/09 (*« which problem are we solving ?»*), mais avec une méthode de recherche en
plus — et deux choses que nous refusons (le prix au pourcentage du chiffre d'affaires, la promesse de
gain chiffré).

---

## 1 · Ce que dit la vidéo, sans l'enjoliver

L'auteur cherche « en direct » un commerce local qui perd de l'argent sans le savoir. Sa méthode : fouiller
**les avis Google publics**. Son cas d'école est une société de gestion immobilière à **4,5 étoiles et 458
avis** — donc « qui va bien » — où **quatre clients** racontent la même chose : *on appelle, personne ne
rappelle*. Il estime la fuite (**2 à 6 affaires/mois, jusqu'à ~58 000 $/an**), puis propose le correctif et
le vend.

**Ce qu'il faut garder, et c'est l'essentiel :**

1. **La répétition est le signal** — une plainte isolée peut être une mauvaise journée ; **trois, quatre,
   cinq** avis distincts sur le même sujet, c'est un **trou dans le parcours**. (Sa règle : au moins 3
   mentions indépendantes.)
2. **Sa « zone de fuite »** : viser les commerces entre **~3,2 et 4,5 étoiles** avec un **vrai volume**
   d'avis — assez de notes pour que la moyenne veuille dire quelque chose, jamais 10 avis (une seule
   mauvaise note écrase tout) ni 5 000 (trois plaintes noyées dans la masse ne prouvent rien).
3. **L'absence de réponse du patron est un fait, pas une opinion** — un commerce qui ne répond à aucun avis
   laisse chaque compliment et chaque reproche « partir dans le silence », et le laisse paraître indifférent.
4. **La formulation qui désarme :** *ce n'est pas vos personnes, c'est un trou dans votre processus.* Sa
   phrase exacte : *« Hey, there's a process issue. It's not your people. It's not a moral failing. »*
5. **« Personne ne m'a jamais demandé mon site web »** — son métier a décollé quand il a su dire **ce que le
   problème coûtait**, pas ce qu'il savait faire. C'est la leçon la plus transférable de la vidéo.
6. **Sa provenance compte** : la vidéo se termine sur l'invitation à rejoindre sa communauté payante. C'est
   un vendeur de méthode — comme les trois blogs d'agences du lot [31]. On prend la méthode, on ne cite pas
   l'auteur devant un client, et **on ne réécrit pas ses chiffres** (58 000 $/an décrit un marché immobilier
   américain, pas un laboratoire de Bonamoussadi).

## 2 · Ce que nous refusons de la vidéo

| Ce qu'il fait | Pourquoi nous ne le ferons pas |
|---|---|
| **Facturer 10 à 20 % du chiffre d'affaires ajouté** (~8 600 $ sur les 58 000 $) | nous ne facturons **jamais** au pourcentage du chiffre d'affaires d'un client, et nous **ne promettons aucun gain chiffré**. Nos prix sont fixes (150 000 la création ; 12 000 ou 30 000/mois l'abonnement) — et « jamais de remise, on ajuste le périmètre » |
| **Estimer la fuite en argent avec ses hypothèses** (2 400 $ de marge par voiture…) | nous ne connaissons ni la marge d'un laboratoire, ni son nombre de patients. Une fuite se **décrit** (« quatre patients écrivent que personne ne décroche »), elle ne se **chiffre pas à leur place** |
| **Démarcher à partir de ce qu'il a trouvé dans les avis** | nous le ferons **en privé, une fois, respectueusement** — jamais en public, jamais en commentant un avis, jamais en citant un nom de client |
| **Promettre de « colmater » toutes les fuites** | certaines plaintes ne sont pas réparables par nous (une analyse erronée, un personnel impoli). On ne vend que ce qu'on sait faire : la prise de contact, la fiche, la page, la régularité |

## 3 · La version Douala — les seuils changent, la règle ne change pas

**Le point qu'il faut dire franchement : notre marché n'a pas 458 avis.** Beaucoup de laboratoires et de
cabinets de Douala en ont **0 à 20**. Le seuil « 40 avis et plus » de la vidéo ne s'applique pas ici.

Ce qu'on adapte, sans se raconter d'histoires :

- **Moins de 5 avis : on ne conclut rien.** Aucun motif ne peut être établi, et on ne présente pas une
  plainte isolée comme un problème du commerce. *(C'est ce que l'outil dit lui-même et refuse de franchir.)*
- **À partir de 5 avis : la règle des 3 mentions tient.** Trois personnes distinctes qui écrivent la même
  chose, ce n'est plus une humeur, c'est un parcours.
- **Ce qui se lit même sans volume :** le patron répond-il aux avis ? Les horaires sont-ils à jour ?
  Y a-t-il un site dans la fiche ? *(Pour Univers Optique : **3,3/5 sur 6 avis**, et un champ « site web »
  vide — ces deux faits suffisent, sans avoir besoin de parler des clients mécontents.)*
- **La règle de lecture reste :** on ne parle **jamais** d'un avis négatif devant quelqu'un d'autre, et on
  ne présente jamais un client mécontent comme une preuve.

## 4 · Les familles de plaintes, et l'offre qui y répond

C'est la table que `tools/outreach/scan_reviews.py` applique au texte qu'on lui colle :

| La plainte qui revient | Ce qu'elle dit de la fuite | Notre offre |
|---|---|---|
| **« personne ne répond / on n'a jamais rappelé »** | le canal d'entrée est ouvert et personne n'est au bout | **C** (entretien) — et la page avec son formulaire qui écrit à 22 h ; **B** (pilote labo) si c'est plus large |
| **« mes résultats étaient en retard / il a fallu revenir »** | le suivi n'est pas tracé | **B** (pilote labo : résultats + encaissements) |
| **« impossible d'avoir un rendez-vous »** | aucune prise de rendez-vous en dehors des heures d'ouverture | **le site** (formulaire de réservation WhatsApp) |
| **« le prix annoncé n'était pas le bon »** | aucun périmètre écrit | **le contrat** (description du projet + exclusions) |
| **« accueil / attente »** | l'expérience commence avant la consultation | **la page + la fiche Google** (horaires, repère d'accès, photos) |
| **« c'était fermé alors que c'est marqué ouvert »** | les horaires affichés sont faux quelque part | **la fiche Google** (et le nettoyage de nos 5 écarts connus) |
| **« résultat erroné »** | problème de qualité — | **hors de notre périmètre** : on ne le vend pas, on ne le promet pas |

## 5 · L'angle d'approche, écrit d'avance (FR)

Ce qu'on dit — **au patron, en privé, une seule fois** :

> Bonjour [nom]. Pour un [métier] à [quartier], un patient qui cherche sur son téléphone tombe sur des avis
> qui parlent de vous — et **trois personnes y racontent la
> même chose** — on les appelle et personne ne rappelle.
> Ce n'est pas une question de personnes, c'est un trou dans le parcours : pendant une consultation, un
> appel qui tombe ne se rattrape pas, alors qu'un message écrit attend votre réponse.
> Je ne propose pas de « corriger vos avis ». Je propose que le patient puisse **écrire et réserver à
> n'importe quelle heure**, et que ça arrive sur le téléphone qui est déjà dans votre poche.
> Je vous la construis d'abord, vous la regardez sur votre téléphone, vous décidez après. Je vous l'envoie ?
> — Akwo King / AMK – Développement Web & Solutions Digitales

**Ce qu'on ne met jamais dans ce message :**

- aucun **nom de client** tiré d'un avis, aucune citation complète ;
- aucune **estimation en francs** de ce que la fuite coûte (on ne connaît pas son volume d'activité) ;
- aucun mot qui juge : « mauvais », « honteux », « vous perdez des clients » ;
- **jamais** la phrase « je peux faire supprimer les avis » (nous ne le pouvons pas, et le dire nous
  discréditerait pour de bon — `FICHE-GOOGLE-PROFILE.md` §5) ;
- aucun envoi à deux questions à la fois.

## 6 · Le protocole des dix minutes, avant de contacter

À faire **avant** les messages froids, pour les prospects qu'on choisit (`leads/Daily-Plan.csv`) :

1. **Ouvrir la fiche Google** du prospect (ou Maps) : note, **nombre d'avis**, et depuis quand ils arrivent.
2. **Copier les avis dans un fichier**, un avis par ligne — **en retirant les noms des clients**.
3. **Passer le fichier au scan** :
   `python3 tools/outreach/scan_reviews.py --niche "laboratoire" avis.txt`
4. **Lire le verdict, et s'y tenir** : « motif répété » → on approche par la fuite ; « mentions isolées » ou
   « pas d'angle » → **on approche autrement** (le travail visible, la fiche, l'aperçu) et on ne parle pas
   des avis.
5. **Noter au CRM** ce qui a été retenu — et **le fait qu'on a lu les avis**, pas leur contenu.
6. **Le fichier d'avis ne vit jamais dans le dépôt.** `/tmp` suffit, et il se supprime après : le scan
   lui-même n'écrit rien, et un avis porte un nom de client.

**Ce que fait l'outil, et ce qu'il ne fait pas :** il **compte ce qui est écrit** dans le texte qu'on lui
donne. Il n'invente rien, il ne note personne, il n'écrit **aucun fichier** (un avis contient un nom, et on
ne stocke pas ça), et il **refuse de parler de motif** en dessous de 3 mentions ou de 5 avis. Douze
assertions le vérifient, dont trois cas négatifs.

## 7 · La mesure du travail, pas la promesse

Nous ne facturons pas un pourcentage : notre modèle récurrent est **12 000 ou 30 000 FCFA/mois**, et il doit
contenir du travail visible chaque mois (`PRIX-ET-RECURRENCE-2026-09-24.md`). La fuite détectée donne un
**angle d'approche** et un **ordre de priorité**, pas un prix.

Et la phrase de la vidéo qui vaut d'être gardée pour nos messages : **personne ne demande un site web ;
tout le monde écoute ce que son problème lui coûte.**

---

## 8 · La deuxième vidéo — « Social Intelligence » (audiobook) : ce qu'on en garde, et ce qu'on ne répète pas

`CsXKAC4iYG4` est un **audiobook narré** (« Audiobook Center », 14,2 K abonnés) sur l'intelligence sociale —
lu, et traité avec la même méfiance que n'importe quelle source qui donne des chiffres sans qu'on puisse les
vérifier.

**Ce qu'on ne répétera jamais** (les citations sont invérifiables, et certaines sont des contresens
classiques) : « **93 % de la communication est non-verbale** » — c'est un détournement de l'étude de
Mehrabian (7 % / 38 % / 55 %), qui ne portait que sur la **transmission d'attitudes et d'émotions** dans
une expérience précise, pas sur la communication en général ; « l'intelligence sociale compte **deux fois
plus** que les compétences techniques » ; « **90 %** des meilleurs contre 20 % des moins bons » ;
« **quatre fois** plus de chances d'atteindre un poste de direction ». Aucune de ces phrases n'est
vérifiable, et notre règle est simple : **un chiffre qu'on ne peut pas montrer ne sort pas de notre
bouche** — surtout devant un client.

**Ce qu'on en garde, et qui sert demain matin :** les **cinq composantes** qu'il énumère font une bonne
liste de contrôle pour une réunion :

| Composante | Traduction pour nos deux rendez-vous |
|---|---|
| **conscience sociale** | lire la pièce avant de parler : qui décide, qui écoute, qui n'est pas là |
| **aisance sociale** | entrer, saluer, laisser le silence faire son travail |
| **cognition sociale** | comprendre la norme de la maison (c'est chez eux, pas chez nous) |
| **souplesse de comportement** | le même contenu pour un opticien et pour une biologiste, **jamais le même ton** |
| **présence sociale** | être celui qui sait de quoi il parle — parce qu'on a **lu** leurs avis, leurs horaires, leur page |

**Et le retournement qui compte pour nous.** Cette vidéo répète que « le non-verbal domine ». C'est peut-être
vrai à une table — **c'est faux dans notre canal principal** : sur WhatsApp, il n'y a **ni visage, ni voix,
ni poignée de main**. Nos mots *sont* notre non-verbal : la ponctuation, la longueur d'une phrase, le fait
de ne pas reposer un prix, de ne pas reprocher un silence. C'est une raison de plus, pas une de moins, de
soigner chaque message — et c'est exactement ce que nos trois ouvertures d'appel et nos variantes de message
essaient de faire.

**Ce qui change à table, en revanche** : les deux réunions de vendredi se jouent en présence. Là, la vidéo
redevient utile sur un point — **écouter plus qu'on ne parle**, et poser les questions du questionnaire
plutôt que de réciter la page.


---

## 9 · Premier cas réel — Univers Optique (24/09) : le scan refuse, et c'est la bonne réponse

Demande de King : lancer le scan sur les avis d'Univers Optique, à trois jours de sa réunion. **Il n'y avait
aucun avis « collé »** — le dépôt n'en garde pas, un avis portant un nom de client. Ce que la fiche laisse lire
publiquement : **3 avis sur 6** (les trois autres sont derrière « Plus d'avis (3) »). Le scan a donc tourné sur
ces trois textes, **noms retirés**, lus depuis l'entrée standard — aucun fichier écrit.

Sortie réelle, mot pour mot :

    SCAN DES AVIS PUBLICS — Univers Optique — 3 avis lisibles sur 6
    3 avis analysé(s). Rien n'est enregistré : ce rapport ne vit que sur ton écran.

    STOP — échantillon trop petit (3 avis, minimum 5 pour conclure quoi que ce soit).
    Avec aussi peu d'avis, une plainte isolée peut venir d'une mauvaise journée. On note le
    fait tel quel, on n'en fait pas un motif, et on n'en parle pas au client comme d'un
    problème systématique.

Les trois disent : deux décrivent le cabinet, un félicite l'accueil. **Aucune plainte**, et ils datent de **8
et 5 ans**. Trois conclusions, dans l'ordre d'importance :

1. **La méthode « fuite » ne mord pas ici, et on ne la force pas.** Pas de plainte répétée → pas de « voici ce
   que ça vous coûte ». La réunion garde son angle (le site, la fiche), et **on n'ouvre pas le sujet des avis**.
2. **Ce que la même lecture a trouvé est plus fort que n'importe quel avis** : la fiche affiche
   « **Revendiquer cet établissement** » — **personne ne la pilote**. C'est le cas ② du §9.3 de
   `FICHE-GOOGLE-PROFILE.md`, et c'est **l'étape zéro** de tout le reste : sans revendication, ni champ site
   sous son contrôle, ni réponse aux avis.
3. **Le piège d'homonyme est réel, et maintenant chiffré** : « Univers Optique » à **Hagondange (Moselle)** —
   9 avis, tous 5/5, un gérant prénommé Cyril, un client qui remercie pour un « disque bleu de stationnement ».
   Rien à voir. Le nom d'un dossier porte toujours sa ville.

**La règle qui ressort :** la répétition est le signal (§1) — mais quand il n'y a pas de répétition, la réponse
honnête est « il n'y a pas de fuite ici », et on se tait sur les avis. Le scan a refusé pour de vrai, sur des
 données réelles : c'est le garde-fou qui a produit le résultat, pas un jugement humain.
