# L'ACCROCHE D'ABORD — les trois composantes, l'alignement, et le tunnel qui les suit

```
Statut    doctrine de fabrication, opposable (portes : tools/qa/audit_hook.py + tools/qa/audit_post_dm.py)
Source    texte transmis par King le 27/10/2026 (mail « hooks + buyer activation flow ») — auteur NON
          NOMMÉ, aucune URL, aucune date, produit vendu en fin de texte. Tier C : voir §7.
Étend     knowledge/HOOKS-2026-10-25.md (les six mots de puissance, l'échelle, la grille 331)
Relie     knowledge/CONTENT-CREATION-2026-10-22.md §3 ter · §5 bis (un opt-in, un seul) ·
          clients/dm-optic/FUNNEL-WHATSAPP-2026-10-23.md · clients/dm-optic/content/month1/w2/ANALYSE-POST-1
Écrit     27/10/2026, tour 192
```

---

## 1 · Ce que le texte dit, et pourquoi ça tient

Une seule idée porte tout le reste : **la deuxième seconde est le seul endroit où une vidéo se perd pour
de bon.** Si le spectateur part à 4 s, les 55 suivantes valent un écran noir. Donc l'accroche n'est pas
une ligne d'introduction : c'est **le titre, le résumé et l'argument**, réunis dans les trois premières
secondes.

| # | Composante | Ce que c'est | Rang de la source | Ce que ça remplace chez nous |
|---|---|---|---|---|
| 1 | **texte à l'écran** | les mots qu'on lit | **1** | le carton d'ouverture « titre de la marque » |
| 2 | **visuel** | ce qui bouge dans le cadre | **2** | le plan large de façade ou de logo |
| 3 | **parlé** | ce que la voix dit | **3** | la phrase d'introduction que personne n'entend |

> « 85 % des vidéos courtes sont regardées sans son » `[SOURCE — non vérifié]`. **Ce qu'on en garde** :
> une pièce doit rester compréhensible **muette**. Ce qu'on n'en fait pas : citer le 85 % comme un fait
> mesuré — aucune source primaire n'est fournie, et le dépôt ne publie pas un chiffre qu'il n'a pas lu.

**Les deux exigences**, et c'est là que le texte est le plus utile :

1. **clarté immédiate** — dans la première phrase, on sait de quoi parle la vidéo, donc si elle est pour
   nous. Langage simple, phrases courtes, une seule idée.
2. **boucle de curiosité** — *curiosité = contraste*. L'écart entre ce que le spectateur croit et ce qu'on
   s'apprête à lui montrer. Plus l'écart est grand, plus il reste.

**L'alignement maximal** : les trois composantes doivent dire **la même chose**. Le texte dit une chose,
le visuel en montre une autre, la voix ajoute une troisième → le spectateur doute une demi-seconde et
part. Le texte cite deux vidéos du même auteur, même production : **14 M vues** alignée, **40 K vues**
désalignée. `[SOURCE — chiffres non vérifiables]` On retient le mécanisme, pas les chiffres.

**Le temps** : 30–40 % du temps de fabrication sur l'accroche. Chez nous, aujourd'hui : **0 %**. C'est
le seul chiffre du texte qui soit une critique directe de notre façon de travailler — et il est vérifiable
dans nos propres fichiers (l'accroche s'écrit en dernier, dans le tableau du script).

---

## 2 · Ce que le dépôt disait déjà — et la seule ligne à corriger

Depuis le 25/10, `HOOKS-2026-10-25.md` dit **ce qui doit se trouver dans la phrase** : sujet, action,
objectif, **contraste** (le plus important), + deux mots d'intrigue facultatifs. La porte
`tools/qa/audit_hook.py` les compte. Le texte du 27/10 ne remplace pas ça : il dit **où** ça se passe
(à l'écran, pas seulement dans la voix) et **avec quoi** (le visuel doit dire la même chose).

⚠️ **Une ligne du dépôt devient fausse.** `ANALYSE-POST-1-2026-10-23.md` §4 écrivait : *« règle du 23/10 :
visuel > écrit > parlé »*. Le texte du 27/10 tranche l'inverse : **écrit > visuel > parlé**. Les deux
s'accordent sur un point, et c'est le seul qui compte pour nous : **le parlé est dernier**. La ligne est
corrigée là où elle s'applique — pas réécrite dans l'historique : une analyse datée reste une analyse
datée, une doctrine se corrige.

**Conséquence pratique immédiate** : un carton qui n'est pas **lisible en une seconde, sans son**, n'est
pas un texte d'accroche. Sur nos pièces existantes, le carton d'ouverture de `tiktok-01-v2` est
« Vingt minutes d'écran. » — un **constat**, sans action ni objectif. Il informe, il ne retient pas.

---

## 3 · La troisième pièce : l'alignement, désormais vérifiée

Les six mots de puissance vérifient **une** phrase. Rien ne vérifiait que le texte, le visuel et le parlé
disent la même chose. C'est le trou que le texte du 27/10 nomme, et il se ferme :

**`tools/qa/audit_post_dm.py`** exige, dans le kit de publication, une section **§1** qui déclare les
**trois composantes** de l'accroche :

```text
| Composante | Ce qui est écrit / montré / dit | Secondes |
| texte      | 8 HEURES À 40 CM · 20 SECONDES À 6 MÈTRES | 0,0–3,0 |
| visuel     | intérieur du cabinet, zoom arrière très lent | 0,0–3,0 |
| parlé      | « Vingt minutes d'écran. Puis vingt secondes. À six mètres. » | 0,0–3,2 |
```

La porte refuse `hook-incomplet` (une des trois manque), `hook-desaligne` (le texte à l'écran ne contient
aucun des nombres de la phrase prononcée) et `hook-tardif` (le texte arrive après 3 s). Le banc :
`tools/qa/test_audit_post_dm.py`.

Ce que la porte **ne fait pas** : juger si l'accroche est bonne. Elle vérifie qu'il y en a une, qu'elle
est complète, alignée, et qu'elle arrive à temps.

---

## 4 · La seconde moitié du texte : le tunnel — et ce qui ne s'applique pas

Le texte décrit un flux d'activation :

```text
vidéo → CTA commentaire → DM automatique « mot » → aimant → page → e-mail → livraison → séquence → vente
```

**Ce qui s'applique tel quel** : le principe. *« Les réseaux sociaux ne servent pas à vendre, ils servent
à accumuler de la confiance et à capturer un contact. »* C'est exactement ce que le dépôt a écrit le
23/10 (`CONTENT-CREATION` §5 bis : un opt-in, un seul) et ce que `CONTENT-GAMES` §2 dit autrement (jeu 5,
monétisation **hors plateforme**).

**Ce qui ne s'applique pas — et pourquoi, en trois lignes :**

| Pièce du flux | Chez AMK | Chez DM Optique |
|---|---|---|
| **e-mail capturé** | ✅ applicable : c'est notre liste | ⛔ **il n'y en a pas** — un patient de quartier ne donne pas d'e-mail pour des lunettes. Le contact durable, ici, c'est **le numéro WhatsApp** (`FUNNEL-WHATSAPP` §3) |
| **DM automatique par mot-clé (ManyChat)** | ⛔ **non** : accès API + abonnement, et le dépôt a tranché le 23/10 — réponse **manuelle** sous quelques heures, aucun outil | ⛔ idem |
| **page d'atterrissage + formulaire** | ⛔ le site existe ; refaire une page pour un aimant, c'est du travail hors contrat | ⛔ idem : le site, la fiche Google et le fil WhatsApp font ce travail |
| **aimant (7 types)** | ✅ applicable : `CONTRÔLE`, l'étape 1 de la bibliothèque | ✅ **transposé** : l'aimant n'est pas un PDF, c'est **la monture** — « envoyez son nom, on vous dit si elle est au cabinet et on vous envoie sa photo ». Les 65 photos existent déjà |
| **mesure : conversions par vue** | ✅ c'est déjà notre règle (`CONTENT-CREATION` §5) : les conversations WhatsApp, jamais les vues | ✅ idem, avec **un texte prérempli par pièce** — c'est notre seule attribution |

**La ligne qui reste, et qu'on ne franchit pas** : `CONTENT-CREATION` §5 bis — *le patient de DM veut un
rendez-vous, pas un PDF*. On garde donc la mécanique (une porte, un mot, une livraison en conversation)
et on refuse la forme (liste de diffusion, séquence d'e-mails, aimant documentaire). Un aimant qui
demande une adresse e-mail à un patient de Bonabéri coûte une conversation et ne rend rien.

**Le seul chiffre à lire** : conversations ouvertes **par pièce**, rapportées aux vues de la pièce. Une
vidéo à 5 000 vues et 50 conversations vaut mieux qu'une vidéo à 50 000 vues et 5 conversations. Chez DM,
on en est à **0 conversation attribuée** — parce qu'aucune pièce publiée n'avait de texte prérempli propre.

---

## 5 · Le désaccord qu'on assume, et le chiffre qu'on refuse

- **« Le texte est plus important que la voix »** : on l'applique. Mais un texte d'accroche qui **promet**
  ce que la vidéo ne tient pas coûte le compte, pas la vue. Les verrous client passent avant la doctrine :
  aucun prix, aucun diagnostic, aucune promesse, aucun visage de patient (`CONTENT-CREATION` §6 bis).
- **Le texte pousse à l'urgence et à la promesse** (« the biggest gap », « stop doing X »). Chez nous,
  `audit_hook` refuse le champ lexical de la peur et de la promesse, et ça ne change pas.
- **Les chiffres du texte** (14 M / 40 K, 85 % sans son, 30–40 % du temps) ne sont pas vérifiables et ne
  sortent **jamais** dans un livrable client. Ce qui sort, c'est le mécanisme et la méthode.

---

## 6 · Ce que ça change dès aujourd'hui

1. **Le kit de publication porte une §1 d'alignement** — trois composantes, trois lignes, avant la
   légende. C'est la première chose qu'on écrit, pas la dernière.
2. **Trois variantes d'accroche** par pièce, une retenue, notée dans le fichier de la semaine
   (`CONTENT-CREATION` §3 ter le demandait déjà ; personne ne l'appliquait).
3. **Le carton d'ouverture ne porte plus le nom du cabinet** : il porte le contraste. La marque arrive à
   la fin, quand le spectateur est encore là.
4. **Une demande de partage, une seule**, à l'endroit où l'information devient utile — la donnée du 23/10
   dit **0 partage sur les deux réseaux**, et c'est le trou le plus cher.
5. **Un texte WhatsApp prérempli par pièce** (`wa.me/237…?text=…`), sinon une conversation ne dit pas
   d'où elle vient. Aucune pièce publiée avant le 27/10 n'en avait.

Application immédiate : `clients/dm-optic/content/month1/w3/KIT-27-10-HOOK.md`.

---

## 7 · Provenance, et ce que la source ne dit pas

- **Auteur non nommé, aucune URL, aucune date.** Le texte se termine par une offre payante (« Short Form
  Academy ») : c'est un texte de vente, pas une étude. Tier C, comme les captures du 25/10.
- **Aucun chiffre de la source n'est repris dans un livrable client.** Les deux exemples de vues (14 M /
  40 K) et le « 85 % sans son » restent dans ce document, étiquetés non vérifiés.
- **Ce que la source ne dit pas** : combien de variantes tester à budget nul ; comment un compte de
  200 abonnés juge une accroche ; ce que vaut l'alignement sur une audience de 65 ans qui lit surtout les
  sous-titres. Le dépôt n'a **aucune donnée** là-dessus — et ne fera pas semblant.
- **Ce qui reste vrai sans elle** : nos propres mesures du 23/10 (sortie à 0:02 sur TikTok, 0:05 sur
  Facebook, 12 % de lecture moyenne, 0 partage). Elles suffisent à justifier le travail sur l'accroche.

## 8 · Les nœuds liés

| Nœud | Ce qu'il apporte **ici** | Ce que ce document lui ajoute |
|---|---|---|
| `knowledge/HOOKS-2026-10-25.md` | les 6 mots de puissance, l'échelle, la grille 331 | **l'alignement** : les mots doivent être à l'écran, pas seulement dans la voix |
| `knowledge/CONTENT-CREATION-2026-10-22.md` | §3 ter (banque de hooks), §5 bis (un opt-in), §6 bis (verrous) | la §1 d'alignement dans chaque kit, et la correction « écrit > visuel > parlé » |
| `knowledge/CONTENT-GAMES-2026-10-25.md` | jeu 5, monétisation hors plateforme | le mécanisme du tunnel, refusé dans sa forme e-mail |
| `knowledge/IDEA-PIPES-2026-10-25.md` | le remix : 8–10 briques constantes, 1–3 changées | la méthode de recherche d'accroches : **partir des outliers, remixer la structure** |
| `clients/dm-optic/FUNNEL-WHATSAPP-2026-10-23.md` | les huit étages réels | l'étage 3 (le premier message) devient **mesurable** : un texte prérempli par pièce |
| `clients/dm-optic/content/month1/w2/ANALYSE-POST-1-2026-10-23.md` | les chiffres du 23/10 : 0:02, 0:05, 0 partage | l'ordre des composantes corrigé, et le partage demandé |
| `tools/qa/audit_hook.py` | la porte de l'accroche | rien — elle reste la porte des mots |
| `tools/qa/audit_post_dm.py` + `test_audit_post_dm.py` | *(créés ce tour)* | la porte de l'**alignement** et du kit client |
