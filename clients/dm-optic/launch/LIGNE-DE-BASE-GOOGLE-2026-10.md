# La ligne de base Google — comment la relever, et pourquoi maintenant (21/10/2026)

**En une phrase :** la ligne de base, c'est **la photo du point de départ**, prise avant que les
posts ne commencent. Sans elle, dans quatre semaines, personne ne pourra dire si les posts ont
servi à quelque chose — et le cabinet paiera un rapport qu'on ne peut pas prouver.

**À faire avant mardi 27/10** (premier post programmé). Durée : **10 minutes**. Une seule fois.

---

## 1 · Où sont les chiffres

Deux chemins, le même écran :

| Chemin | Étapes |
|---|---|
| **Le plus rapide** | Connecté avec le compte qui gère la fiche → tape `DM OPTIQUE SARL` dans Google → dans le bloc « Your business on Google », clique **« See performance »** |
| Par le tableau de bord | `business.google.com` → sélectionne la fiche **DM OPTIQUE SARL** → menu de gauche → **Performance** |

Tu arrives sur une page avec des courbes et, en haut, un **sélecteur de dates** (7 jours, 28 jours,
mois en cours, personnalisé).

---

## 2 · Quelle période choisir — et c'est le seul point technique

Le sélecteur par défaut (« 28 derniers jours ») **glisse** : si tu le lis un lundi puis le mardi, la
fenêtre a changé. Deux personnes ne verront donc jamais les mêmes chiffres.

**Règle : on choisit une fenêtre personnalisée, et on la note.**

Pour la ligne de base d'aujourd'hui :

> **Du 24 septembre 2026 au 21 octobre 2026** (28 jours)
> → sélecteur de dates → **Personnalisé (Custom)** → ces deux dates → **Appliquer**

À partir de la semaine prochaine, on garde **28 jours** et on décale d'une semaine :

| Relevé | Fenêtre (28 jours) | Quand |
|---|---|---|
| **Ligne de base** | **24/09 → 21/10** | **aujourd'hui, avant le 1ᵉʳ post** |
| Semaine 1 | 28/09 → 25/10 | lundi 26/10, 9h |
| Semaine 2 | 04/10 → 01/11 | lundi 02/11, 9h |
| Semaine 3 | 11/10 → 08/11 | lundi 09/11, 9h |
| Semaine 4 — premier bilan | 18/10 → 15/11 | lundi 16/11, 9h |

**Pourquoi toujours 28 jours :** c'est la fenêtre que Google utilise par défaut, elle lisse les
week-ends, et elle reste comparable d'une semaine à l'autre. Sept jours, c'est trop bruité pour un
cabinet de quartier.

---

## 3 · Les 9 chiffres à relever (et ce qu'ils veulent dire)

Sur la page Performance, les blocs s'appellent, selon la version de l'interface : **Interactions**,
**Recherches**, **Vues**. Note les neuf lignes suivantes, même quand c'est 0.

| # | Ce que tu notes | Libellé à l'écran | Ce que ça mesure vraiment |
|---|---|---|---|
| 1 | **Appels** | Calls | les gens qui tapent sur le bouton d'appel depuis la fiche — **la métrique la plus proche du chiffre d'affaires** |
| 2 | **Messages** | Messages | messages envoyés depuis la fiche (probablement 0 : on travaille par WhatsApp) |
| 3 | **Itinéraires** | Direction requests | les gens qui demandent le chemin vers le cabinet — **la deuxième métrique qui compte** |
| 4 | **Clics vers le site** | Website clicks | les gens qui ouvrent `dmoptiquesarl.com` depuis la fiche — c'est là que les posts agissent |
| 5 | **Vues de la fiche** | Profile views | combien de fois la fiche a été affichée |
| 6 | **Recherches directes** | Direct searches | quelqu'un a tapé « DM OPTIQUE » ou l'adresse |
| 7 | **Recherches découverte** | Discovery searches | quelqu'un a tapé « opticien Bonabéri » et la fiche est sortie → **la métrique de visibilité** |
| 8 | **Recherches de marque** | Branded searches | variantes du nom |
| 9 | **Vues des photos** | Photo views | combien de fois tes photos ont été regardées |

**Ne cherche pas à tout optimiser.** Pour ce cabinet, trois chiffres décident : **appels**,
**itinéraires**, **clic vers le site**. Les six autres expliquent *pourquoi* ces trois-là bougent.

---

## 4 · Où coller les chiffres

Ici, dans ce fichier. Remplace les cases vides, ne réécris pas la structure :

### Ligne de base — 24/09/2026 → 21/10/2026

| Métrique | Valeur | Note |
|---|---|---|
| Appels | `____` | |
| Messages | `____` | |
| Itinéraires | `____` | |
| Clics vers le site | `____` | |
| Vues de la fiche | `____` | |
| Recherches directes | `____` | |
| Recherches découverte | `____` | |
| Recherches de marque | `____` | |
| Vues des photos | `____` | |

### Les trois chiffres « de contexte » à relever en même temps (même écran ou à côté)

| Quoi | Où | Valeur au 21/10 |
|---|---|---|
| Nombre d'avis | fiche → Avis | `____` (objectif : 5 le 24/10) |
| Note moyenne | fiche → Avis | `____` |
| Nombre de photos | fiche → Photos | `____` |
| Nombre de posts publiés | fiche → Posts | **0** (les 4 sont programmés à partir du 27/10) |

> Les avis comptent autant que les posts : si la note ou le nombre d'avis bouge pendant les quatre
> semaines, une hausse des appels ne sera pas attribuable aux posts. C'est pour ça qu'on les note
> **le même jour**.

---

## 5 · Le geste qui rend tout ça crédible : la capture d'écran

Un chiffre recopié se discute ; une capture non.

1. Sur la page Performance, **avant de changer quoi que ce soit** : capture d'écran (les courbes + le
   sélecteur de dates visible, c'est lui qui prouve la fenêtre).
2. Nomme le fichier **`2026-10-21_performance-28j.png`** et dépose-le dans
   `clients/dm-optic/launch/baseline/` (le dossier est créé au premier dépôt).
3. Refais exactement la même capture chaque lundi, même écran, même fenêtre de 28 jours.

**Si un bouton « Télécharger » ou « Exporter » apparaît** en haut de la page Performance : utilise-le,
il sort un CSV jour par jour. C'est encore mieux que la capture — garde les deux.

---

## 6 · Ce que Google ne compte pas — le carnet du cabinet

Google ne voit **que** ce qui se passe sur la fiche. Il ne voit ni les appels passés directement au
656 122 239, ni les messages WhatsApp, ni les gens qui poussent la porte. Or c'est là que se joue le
chiffre d'affaires.

**Une minute par jour, au cabinet, sur un cahier ou une note du téléphone :**

| Jour | Appels reçus | Messages WhatsApp | Visites | « Comment nous avez-vous trouvé ? » (Google / Facebook / on m'a parlé) |
|---|---|---|---|---|
| lundi | | | | |
| mardi | | | | |
| … | | | | |

La question « comment nous avez-vous trouvé ? » est **la seule** façon de relier un post à un
patient. Elle se pose en une seconde, au moment de l'examen, sans avoir l'air d'un sondage.

> Ce carnet, c'est la partie « cabinet » de la ligne de base — celle qui manque aujourd'hui dans le
> dossier de livraison. Elle ne demande aucune compétence technique, juste de la tenir.

---

## 7 · Comment on lira les résultats (et ce qu'on ne dira pas)

**Premier bilan : lundi 16/11**, quatre semaines après le premier post. Règles de lecture, écrites
d'avance pour ne pas interpréter après coup :

1. **On compare des fenêtres de même longueur**, jamais un mois de 31 jours avec un de 28.
2. **On ne conclut pas avant 4 semaines.** Un cabinet de quartier reçoit peu de clics ; sur des
   volumes de 10–30 par mois, une variation de 3 ne veut rien dire.
3. **On regarde appels + itinéraires d'abord.** Si les posts n'ont rien changé là, ils n'ont rien
   changé — et on le dira, quitte à arrêter.
4. **On sépare les causes.** Une hausse des appels pendant une semaine de publication peut venir
   d'un avis reçu, d'un passage, ou du hasard. C'est pour ça qu'on note avis et photos le même jour.
5. **Aucune promesse de classement.** Le test contrôlé de Sterling Sky (9 semaines, 441 mots-clés) ne
   montre aucun effet des posts sur le classement local — on ne vend donc pas ça au cabinet
   (`GOOGLE-POSTS-2026-10.md` §2).

---

## 8 · Vérifications de la journée (2 minutes)

- [ ] La fiche est bien **vérifiée** et le compte qui la gère est le bon.
- [ ] La page Performance s'ouvre (si elle est vide, c'est que la fiche est trop récente : note 0
      partout, ce **sera** la ligne de base).
- [ ] Le sélecteur de dates affiche bien **24/09 → 21/10**.
- [ ] Les 9 chiffres sont recopiés ci-dessus, même à 0.
- [ ] La capture `2026-10-21_performance-28j.png` est prise.
- [ ] Le cahier du cabinet est commencé (une ligne par jour).

---

## 9 · Ce qui manque encore côté site — et qui limite la mesure

Le site **ne contient aucune mesure d'audience** aujourd'hui. Conséquence : les liens des posts
portent bien un marqueur `utm_source=google…`, mais personne ne peut lire le résultat — on saura
combien de personnes **cliquent depuis Google**, pas ce qu'elles font ensuite.

Deux options, à trancher :

| Option | Ce que ça donne | Coût |
|---|---|---|
| **Cloudflare Web Analytics** (recommandé) | pages vues, visiteurs, sources, pays — **sans cookie**, donc pas de bandeau de consentement à ajouter | gratuit ; une ligne de script à poser dans le site + un redéploiement |
| Ne rien ajouter | on reste sur les chiffres Google + le carnet | 0 |

Tant que ce n'est pas tranché, la ligne de base Google ci-dessus **suffit** : c'est elle qui prouve
le travail. L'analytics du site ne ferait qu'ajouter la couche « ce qui se passe après le clic ».
