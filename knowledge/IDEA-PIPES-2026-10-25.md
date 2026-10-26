# LES SIX TUYAUX À IDÉES — d'où vient une idée, avant de savoir si elle est bonne

```
Statut    doctrine d'entrée, opposable (porte : tools/qa/audit_ideas.py)
Source    texte transmis par King le 25/10/2026 (« The 6 Idea Pipes ») — auteur NON NOMMÉ, aucune
          URL, aucune date. Suite annoncée par « The 5 Content Games » (même fil) : même provenance,
          donc même usage — tier C, voir §9.
Étend     knowledge/CONTENT-GAMES-2026-10-25.md §3 (le rôle) et §4 (ce que la source ne permet pas)
Relie     knowledge/CONTENT-CREATION-2026-10-22.md §4 bis · content/pipeline/CONTENT-SHORTLIST.md ·
          content/ideas/SHORTLIST-2026-10-25.md · content/reels/ep01/ (EP01)
Écrit     25/10/2026, tour 147
```

---

## 1 · Une idée = trois choses `[SOURCE]`

| Pièce | Définition de la source | Notre traduction |
|---|---|---|
| **Topic** | la sous-catégorie, le sujet | « la fiche Google d'un opticien de Douala » |
| **Seed** | la phrase-tête, une prise de position qui ancre la vidéo | « Votre nom existe. Votre site, non. » |
| **Substance** | les faits, opinions et exemples qui construisent la compréhension | les trois captures Optix du 24/10 |

Et **deux prédicteurs**, plus forts que la qualité du montage : ① le topic est-il **pertinent pour
l'acheteur** ? ② le seed et la substance sont-ils **intéressants ou utiles pour lui** ?

> « The difference between 10K views and 1M views come down to how well you choose, frame, and position
> your video ideas. » `[SOURCE]`

**Ce que ça dit de nous, sans détour** : nous avons passé deux tours à améliorer la **substance** d'une
pièce (le clip muet devenu conseil gratuit) et zéro tour à améliorer le **choix** de l'idée. Ce document
inverse l'ordre — non parce que la substance compte peu, mais parce qu'elle ne peut pas sauver un topic
que l'acheteur n'a pas.

## 2 · Les deux erreurs que la source nomme, et où nous sommes

| L'erreur | La phrase de la source | Chez nous |
|---|---|---|
| confondre **portée** et **cible** | « views from the wrong audience don't turn into leads and sales » | mesuré le 17/09 : 91 % et 86 % de l'audience atteinte a **18–34 ans** quand l'acheteur d'un site à 100 000 FCFA est majoritairement **35–54 ans** (`content/pipeline/ANALYTICS-LOG.md` §L'audience atteinte) |
| croire qu'on est « bon en idées » | « the reason their content flops is because their ideas are just not that interesting » | nous n'avons **aucune** banque d'idées évaluée : `CONTENT-SHORTLIST.md` (17/09) liste 13 vidéos avec audience et douleur, jamais une provenance ni une preuve |

## 3 · Les six tuyaux, dans l'ordre de la source `[SOURCE]`

| # | Tuyau | Ce qu'il demande | Preuve qu'il promet |
|---|---|---|---|
| **1** | **nos propres outliers** | ce qui a déjà marché chez nous — le meilleur tuyau pour refaire | nos vues + notre moyenne de chaîne |
| **2** | **les outliers des concurrents** | 80 % du temps de recherche, 10–15 comptes du même acheteur, 30 jours, triés par vues/moyenne | le score de l'outlier + sa date |
| **3** | **les autres médias** | ce qui marche dans la niche ailleurs (YouTube long, podcasts, newsletters, X) | une métrique, même imparfaite |
| **4** | **l'actualité de la catégorie** | ce qui vient de changer dans la niche | une **date** |
| **5** | **les non-outliers des concurrents** | de bonnes idées mal exécutées | une métrique… et un pari (l'exécution était le défaut) |
| **6** | **les originaux** | ce qui nous intéresse, sans aucune donnée | rien — « highest risk, highest reward » |

La conclusion de la source est explicite : *« most beginners start with #6… the lowest hit rate source.
Start with #2 instead. »*

## 4 · Le remix : 8–10 briques constantes, 1–3 changées

> « The goal is not to copy videos word for word or pixel for pixel (that is corny). The goal is to take
> 8-10 of the lego bricks that have worked, and remix the remaining 1-3. » `[SOURCE]`

**Nos onze briques** — ce que `content/reels/ep01/make_ep01.py` sait déjà tenir :

| # | Brique | Où elle vit dans le code |
|---|---|---|
| 1 | **topic** | `voice.json` / le sujet |
| 2 | **seed** | `voice.json`, beat `hook` |
| 3 | **substance** | les captures et les faits cités |
| 4 | **ouverture** | on entre **dans** l'écran, jamais un carton (`s_hook`) |
| 5 | **arc** | 6 beats, 3 cimes (`BEATS`, `audit_reel.py`) |
| 6 | **hook** | les mots de la première seconde |
| 7 | **mise en page** | crème, trame de points, cartes punissées, un seul accent orange (`reelkit`) |
| 8 | **hôte** | la mascotte, même dessin, en bas |
| 9 | **voix** | `voice-03`, une phrase par beat, durée mesurée |
| 10 | **CTA** | le mot `APERÇU` + le numéro, 3,6 s |
| 11 | **durée** | ≤ 25 s quand c'est une porte (`audit_trust.py`) |

**La difficulté d'EP01, nommée correctement pour la première fois** : EP01 ne changeait pas 3 briques
sur 11 — il n'y avait **pas de bibliothèque** avant lui. Les briques 4 à 11 sont nées avec lui. Autrement
dit : EP01 a payé le **gabarit**, et c'est le seul cadeau qu'un original fait à ceux qui suivent. À partir
de maintenant, une pièce peut tenir **9 constantes** et ne changer que topic + seed + substance : le
risque marginal d'EP02 tombe, sans que le talent augmente.

## 5 · Le processus sur deux semaines, traduit pour un opérateur seul

La source prescrit un outil (Sandcastles) que **nous n'avons pas** et que nous n'allons pas acheter pour
un compte à zéro audience. Le protocole tient sans lui, à la main :

| Étape de la source | Notre version, sans l'outil | Qui |
|---|---|---|
| 1 · watchlist de 10–15 comptes | 10–15 comptes qui servent **le même acheteur** (opticiens, cliniques, laboratoires — Douala, Yaoundé, Bafoussam) sur TikTok, Instagram et Facebook, 10 k–1 M d'abonnés | **King ou l'opérateur, au téléphone** — voir §8, je ne peux pas le faire |
| 2 · valider les topics gagnants | les 50–100 vidéos des 30 derniers jours, triées à la main par vues/moyenne ; noter les **5–7 topics** qui reviennent | opérateur, 45 min |
| 3 · miner des seeds | pour chaque vidéo gagnante : *quelle est la phrase non évidente qui la rend intéressante, et est-ce que j'ai mieux ?* | opérateur + moi |
| 4 · shortlist de 10–20 idées | `content/ideas/SHORTLIST-*.md`, une ligne par idée, **avec le lien de l'outlier** | moi, à partir de ce que l'opérateur rapporte |

**Cadence** : tous les quinze jours (§ la source). Notre semaine a trois rôles (`CONTENT-GAMES` §6) ; la
recherche d'idées est ce qui les alimente — sans elle, les trois rôles se remplissent au tuyau 6, c'est-à-dire
au hasard motivé.

## 6 · EP01 passé au crible — la comparaison, sans indulgence

| Question de la source | Réponse sur EP01 v3 |
|---|---|
| **Le topic est-il pertinent pour l'acheteur ?** | **OUI.** Opticien ou clinique de Douala qui a une fiche et pas de site — c'est exactement notre lead type (`leads/records/`, `PACK-OPTICIEN`) |
| **Le seed est-il intéressant ?** | **OUI, mais faible en tension.** « Votre nom existe. Votre site, non. » est un constat, pas une prise de position contraire : il ne contredit rien que l'opticien croit |
| **La substance est-elle utile ?** | **OUI depuis la v3** : trois choses qui se font sans nous + la seule qui reste à construire. En v2, non : le relâchement était muet |
| **De quel tuyau vient-elle ?** | **6 — original.** Aucun outlier à nous, aucun concurrent étudié, aucune actualité datée. La source appelle ça le tuyau « le plus risqué », et elle dit de ne pas commencer par là |
| **Combien de briques changées ?** | **3 sur 11 — mais 8 des 11 n'existaient pas avant lui.** Donc en pratique : 11/11 nouveaux. C'est un original qui a aussi fabriqué son gabarit |
| **Ce que la donnée dit de son audience** | 91 % / 86 % de 18–34 ans sur nos deux publications : **l'audience atteinte n'est pas l'acheteur**. Un topic pertinent ne garantit pas la bonne personne |

**Ce que la v3 a corrigé** : la substance (utilité 3 → 4, score 15 → 20/125).
**Ce qu'aucune version ne peut corriger** : la **provenance**. Une idée sans donnée reste un pari — même
bien exécutée. Le classement d'EP01 comme **porte** (tour 146) était juste ; il manquait une ligne
au-dessus : *porte dont l'idée n'a jamais été validée*.

**Et ce que ça ne veut pas dire.** Il ne faut pas jeter EP01 : c'est la pièce qui a créé le gabarit et
la seule pièce mesurable du dépôt (156 vues, 18 % de rétention, `ANALYTICS-LOG`). Elle devient
**l'outlier nº 1 du tuyau 1 — dès qu'elle aura dépassé sa propre moyenne**, ce qui n'est pas le cas
aujourd'hui. Un outlier se constate, il ne se déclare pas.

## 7 · Ce que ça change dans le dépôt — la chaîne des trois portes

Une pièce ne se produit plus parce qu'elle est une bonne idée : elle franchit trois portes, dans cet
ordre, et chacune a son outil.

| Ordre | Porte | Question | Outil | Refus type |
|---|---|---|---|---|
| 1 | **idée** | d'où vient-elle, et qu'a-t-on changé ? | `tools/qa/audit_ideas.py` | `pipe-sans-chiffre`, `preuve-manquante`, `trop-de-briques` |
| 1 bis | **accroche** *(ajoutée le 25/10 au soir)* | les quatre mots obligatoires, l'échelle déclarée, ni peur ni promesse | `tools/qa/audit_hook.py` | `mots-manquants`, `peur`, `promesse` |
| 1 ter | **récit** *(ajoutée le 26/10)* | une scène, un lock-in, une preuve **dite**, un rehook, un CTA aligné | `tools/qa/audit_story.py` | `pas-de-cas`, `pas-de-rehook`, `preuve-muette`, `cta-non-aligne` |
| 2 | **rôle** | quel jeu sert-elle, et tient-elle son plancher ? | `tools/qa/audit_trust.py` | `trop-court`, `objectif-vues`, `inutile` |
| 3 | **forme** | l'arc tient-il, et la voix est-elle mesurée ? | `tools/qa/audit_reel.py` + `voice/build_timing.py` | `depart-bas`, `cime-manquante`, `muet` |

Conséquences écrites :

- **`content/ideas/`** existe désormais : c'est là que vivent les lots de recherche, un fichier par
  quinzaine (`SHORTLIST-YYYY-MM-DD.md`), avec le format que la porte lit ;
- **`content/pipeline/CONTENT-SHORTLIST.md`** (17/09) reste **l'inventaire des 13 vidéos approuvées**
  — un addendum la relie à `content/ideas/` : elle dit *quoi produire*, le lot dit *d'où vient l'idée* ;
- **la carte des 36 sujets** (playbook §2) ne bouge pas : elle reste l'inventaire des sujets. Ce qui
  change, c'est qu'un sujet ne devient une pièce qu'avec une **ligne de lot** qui nomme son tuyau ;
- **aucune pièce ne se produit plus en tuyau 6 sans que ce soit écrit noir sur blanc** : la porte
  l'avertit, et l'avertissement se cite dans l'en-tête du tour.

## 8 · Ce que je ne peux pas faire, et qui bloque le tuyau 2

Le tuyau 2 — celui que la source recommande de commencer — demande de **regarder TikTok et Instagram** :
chercher 10–15 comptes, lire des vues, calculer une moyenne. **Je n'ai pas d'accès au web ouvert dans
cette session** (le bac ne sort que vers GitHub, npm et PyPI). Je ne peux donc pas construire la
watchlist, et je ne vais pas l'inventer : une watchlist fabriquée serait pire qu'aucune.

Ce que je peux faire, et que fait ce tour : **écrire le format**, la porte qui le vérifie, et un premier
lot honnête (§ `content/ideas/SHORTLIST-2026-10-25.md`) où les tuyaux 1, 2 et 4 sont **déclarés vides**.
Ce que King (ou l'opérateur) doit faire : 45 minutes au téléphone, trois captures d'écran par topic
gagnant. Le lot suivant se remplit avec ça.

## 9 · Provenance et limites — la même règle que les 5 jeux

- **Tier C** : auteur non nommé, aucune URL, aucune date, aucun chiffre de performance vérifiable. Le
  fil annonce « tomorrow … the 6 Idea Pipes » — ce texte est donc la suite directe de « The 5 Content
  Games », même provenance. Il **fait décider** ; il ne se cite pas dans un post.
- **Ce que la source ne prouve pas** : « 10K vs 1M » est une accroche, pas une mesure. Les six tuyaux
  sont un **classement d'expérience**, sans taux de réussite publié. Le « 80 % du temps de recherche »
  est une consigne de travail, pas une donnée.
- **Ce qu'elle ne dit pas** : combien d'idées il faut tester avant d'en garder une ; ce qu'on fait quand
  la niche est **trop petite pour avoir des outliers** (c'est notre cas : les opticiens de Douala ne
  publient presque pas de vidéos — un tuyau 2 peut être vide même bien exécuté) ; et comment un compte
  à zéro audience juge un outlier sans historique.
- **Ce que ça ne change pas** : aucune règle de preuve. Un seed brillant ne rend pas un chiffre inventé
  acceptable (`RESEARCH-STANDARD.md`). Et **une règle sans porte est un trou** — d'où `audit_ideas.py`.

## 10 · Les nœuds liés

| Nœud | Type | Ce qu'il apporte **ici** | Ce que cette doctrine lui ajoute |
|---|---|---|---|
| `knowledge/CONTENT-GAMES-2026-10-25.md` | knowledge | le jeu (5), la formule de confiance, le barème et ses planchers | la **porte d'entrée** qui manquait : le rôle se choisit après l'idée, pas avant |
| `knowledge/CONTENT-CREATION-2026-10-22.md` | knowledge | §3 ter (les quatre S du hook), §4 bis (le type selon l'objectif) | une entrée au **journal §10** : la source, ce qu'on en prend, ce qu'on écarte |
| `content/pipeline/CONTENT-SHORTLIST.md` | données | les 13 vidéos approuvées le 17/09, audience + douleur + droits | un addendum : *quoi produire* ≠ *d'où vient l'idée* |
| `sales/SOCIAL-ACQUISITION-PLAYBOOK-2026-10-25.md` | document | §2 les 36 sujets et leurs 3 étages | **§5 quinquies** : la mine d'idées avant la carte de sujets |
| `content/pipeline/ANALYTICS-LOG.md` | données | 156 / 121 vues, 18 % / 13 %, audience 18–34 ans à 91 % / 86 % | la preuve que notre tuyau 1 est **vide** et que notre audience n'est pas l'acheteur |
| `content/reels/ep01/make_ep01.py` | pièce | les 11 briques du gabarit, en code | `TRUST` (rôle) reste, et la pièce reçoit sa ligne de lot honnête : tuyau 6 |
| `tools/qa/audit_ideas.py` (+ `test_audit_ideas.py`, **19/19**) | outil | la porte : `Idea`, `audit()`, `parse()` | — (c'est son document de référence) |
| `tools/qa/audit_trust.py` · `tools/qa/audit_reel.py` | outil | les portes 2 et 3 de la chaîne | l'ordre **idée → rôle → forme** est écrit dans `PRE-FLIGHT.md` §1 |
| `PRE-FLIGHT.md` | rulebook | §0c/§1 : la lecture et le routage | la ligne « Contenu vidéo / réel / post publié » reçoit la porte d'idée en tête |
| `sales/Activity-Log.md` | journal | la chronologie | le tour 147 |
| Notion `4024b1d8-9633-814c-8837-dcbc1b7f28b0` | miroir | l'état debout lisible | une section datée |

### 10 bis · Ce qui n'a pas été lu, ou n'a pas pu l'être

- **`research/YouTube-Lessons.md`** n'a pas été relu : si un lot antérieur contredit les six tuyaux, la
  contradiction **n'est pas détectée** par ce tour. À faire au prochain lot de veille.
- **Aucun compte concurrent n'a été regardé** (§8) : les tuyaux 1, 2 et 4 sont déclarés vides sur la foi
  du dépôt, pas sur une absence vérifiée sur les plateformes. C'est une **absence de donnée**, pas une
  preuve d'absence.
- **Les 36 sujets du playbook n'ont pas été reclassés un par un** : ce tour écrit la règle et le format ;
  le reclassement se fera lot par lot, en même temps que la watchlist.
