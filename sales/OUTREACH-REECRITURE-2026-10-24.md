# Réécriture de l'approche froide — 24/10/2026 (v2, après lecture du dépôt)

```text
Statut   : remplace la v1 de ce matin (périmée) ET les textes du 23/10.
Portée   : toute première touche froide (WhatsApp), cliniques et opticiens.
Méthode  : le dépôt d'abord (graphify), la recherche ensuite, l'écriture en dernier.
```

---

## 0 · Ce que mes deux erreurs ont coûté — et la règle qui en sort

Le 24/10 au matin, j'ai livré une réécriture complète **sans avoir lu deux documents qui étaient dans
le dépôt** :

| Document | Ce qu'il contenait | Ce que j'ai fait à la place |
|---|---|---|
| `knowledge/OUTREACH-MESSAGING-2026-10-22.md` (à lire « avant tout message à un opticien, un gérant de clinique, un prospect » — table §0c du PRE-FLIGHT, ligne 3) | le motif en 4 temps d'un DM qui accroche, **écrit par King deux jours plus tôt**, avec le dédouanement et la sortie sans friction | j'ai réinventé une structure en 3 lignes, sans le dédouanement |
| `sales/RESEARCH-STANDARD.md` §10 (13/10) | la **réfutation déjà faite** du cadrage de perte « ×2 » (O'Keefe & Jensen, 165 études, N = 50 780, r = .016) | j'ai cité « +19 % de cadrage de perte » d'un blog comme si c'était acquis |

**La faute n'est pas d'avoir mal cherché : c'est d'avoir cherché à la main.** Les deux fichiers
existaient, étaient indexés dans le PRE-FLIGHT, et je ne les ai pas ouverts.

**Ce qui change à partir d'aujourd'hui** (règle `PRE-FLIGHT.md` §0h, déplacée en §00 le 25/10 : le graphe passe avant la pré-vol) : avant d'écrire
un document de vente ou un message, on lance `bash tools/graphify/ask.sh "<sujet>"`. La sortie liste
les documents à lire ; l'en-tête pré-vol **cite ceux qui ont été lus et ceux qui ne l'ont pas été**.
L'outil est local, gratuit, sans clé d'API : `tools/graphify/` (README là-bas).

---

## 1 · Ce que tes deux captures prouvent

**Fashion Vision, 24/09, 13:36, deux coches, jamais ouvert.** Et une correction que je te dois :
j'ai écrit le 23/10 qu'aucun des cinq n'avait été contacté. **Faux** — le dépôt le disait
(`Send-BATCH-2026-09-24-Opticiens-2.md` : « ✔ PARTI LE 24/09 — Doyoan, Bely, 4M Optique Akwa et
Fashion Vision »). Deuxième erreur du même type : une affirmation non vérifiée dans le dépôt.

**Original Optique, 24/10 11:52.** Trois faits dans une image : la fiche dit **« Open until 2:00 PM »**,
le message automatique répond **« nous ne sommes pas disponibles »**, et le site de la fiche ne répond
pas (HTTP 500, vérifié le 23/10). **C'est la meilleure preuve de fuite trouvée à Douala** : le cabinet
dit « je suis ouvert » puis « je ne suis pas là ». Un patient qui écrit reçoit une contradiction et
appelle ailleurs.

---

## 2 · Pourquoi mes messages ne pouvaient pas marcher

Diagnostic ligne par ligne.

| Ce que j'ai écrit (23/10) | Ce que le docteur lit | Ce qui cloche |
|---|---|---|
| « je n'ai trouvé que des annuaires, avec deux adresses différentes » | « D'accord. Et alors ? » | **constat, pas conséquence** |
| « rien à vous, ni horaires ni photos » | « C'est un reproche ? » | **attaque déguisée** — interdite depuis le 23/09 (`DECLINAISON-9-DECLENCHEURS` §1②) |
| « Vous êtes bien à l'immeuble Neuilly II aujourd'hui ? » | « Il veut quoi ? » | **une devinette** sur son adresse, pas un problème |
| « Vous n'avez jamais eu de site, ou… ? » | | **deux questions**, ton d'enquête |

**Les trois fautes, nommées :**
1. **Je décrivais un état, pas une perte en cours.** Un état ne fait rien faire.
2. **Je demandais au docteur de relier lui-même le constat à son chiffre.** Il ne le fera pas : douze
   patients dans la salle d'attente, six mots lus, message effacé.
3. **Je parlais de son site, pas de son patient.** Le cabinet ne veut pas un site ; il veut que la
   personne qui a mal entre chez lui plutôt que chez le voisin.

---

## 3 · La recherche — et la correction du dépôt

**Ce que le dépôt avait déjà tranché, et que je dois respecter** (`sales/RESEARCH-STANDARD.md` §10) :

| Affirmation | Verdict du dépôt (13/10) | Ce que je fais |
|---|---|---|
| « le cadrage de perte gagne ×2 » | **REJETÉ pour un message de persuasion.** O'Keefe & Jensen, 165 études, N = 50 780 : aucune différence fiable (r = .016). Le « ×2 » de Kahneman & Tversky décrit des **choix**, pas un effet mesuré sur un taux de réponse | je garde le cadrage de perte comme **hypothèse à tester**, je ne le cite plus comme acquis |
| « 97 % vérifient en ligne » | **Tier B, mais américain** (BrightLocal 2026, panel US) | jamais cité à un prospect de Douala |
| « 76 % des recherches “near me” visitent dans la journée » | **Tier C, US, de seconde main** | pas utilisé |
| chiffres Cameroun (Facebook 6,8 M, WhatsApp 9–10 M estimés) | Tier C, tiers | utilisables seulement avec la mention « estimation » |

**Ce que j'ai lu ailleurs ce matin, et qui n'a pas le même statut :**

| Source | Ce qu'elle dit | Statut |
|---|---|---|
| méta-analyse 2024 citée par un blog d'agence | « cadrage de perte +19 % en contexte pro » | **source secondaire, non vérifiée** — et contredite par notre §10 : je ne m'en sers pas |
| étude de benchmarks 2025 (thedigitalbloom) | accroches **temporelles** 10,01 % contre accroches **problème** 4,39 % (2,3×) | Tier C, un seul agrégateur — **hypothèse**, pas règle |
| blogs d'outreach (datalane, howtofounder) | une seule demande ; deux demandes divisent le taux de réponse | cohérent avec notre règle « une seule question » — **on garde** |
| sbl.so, firstsales.io, tuco.ai | WhatsApp : 90–98 % de lecture, 3–10 % de réponse à froid, 15–20 % avec personnalisation lourde | Tier C, plusieurs sources convergentes. **Notre 6,5 % historique est dans la norme** |
| sequenzy, overloop, mailshake | le message de rupture est la touche au meilleur taux de réponse (10–15 %) | Tier C, revendeurs. **Actionnable** : une seule relance, à J+7 |

**Ce qu'aucune source ne dit, et qu'on n'inventera pas :** combien un cabinet de Douala perd de
patients. Ni son volume, ni son panier. **Une fuite se décrit, elle ne se chiffre pas à sa place**
(`DETECTION-FUITES` §2).

---

## 4 · La structure retenue — celle de King (22/10), resserrée

Le document du 22/10 décompose le motif en **quatre temps** et le transpose en DM :

1. **le fait daté et vérifié** (« ce matin, j'ai cherché… ») ;
2. **le dédouanement** (« ce n'est pas votre qualité ») ;
3. **la cause nommée** (« c'est votre fiche ») ;
4. **la sortie sans friction** (« ça prend 2 minutes, et vous pouvez le faire sans moi »).

Je garde les quatre temps et j'y ajoute **ce que tu m'as demandé ce matin** : le **patient en train de
se perdre**, au présent, entre le dédouanement et la sortie. Et je resserre à **trois phrases / 55 mots
maximum** — la règle WhatsApp du 02/10 (« laissez l'IA et parlons normalement ») n'a jamais été levée.

| Temps | Rôle | Contrainte |
|---|---|---|
| **1 · le fait** | vrai sur lui, **daté**, vérifiable en 10 s | 12 mots · un chiffre ou un nom propre · aucun adjectif |
| **2 · le dédouanement + la cause** | « ce n'est pas votre travail, c'est X » | une clause, pas un paragraphe |
| **3 · le patient** | ce qu'il **fait** à cause de ça, au présent | une scène, pas un concept |
| **4 · la question** | une seule, fermée, un mot suffit | ni rendez-vous, ni lien, ni prix |

**Interdits inchangés :** prix · lien au premier message · signature · puces · emojis ·
« vous perdez des clients » · deux questions · un chiffre sur son activité.

---

## 5 · Les messages à envoyer aujourd'hui — 6, un seul numéro

### 5.1 · Les cinq cliniques sans aucune présence

**⑥ Bouda Seidou — Bonanjo — 677 76 03 49**
> Bonjour Docteur, ce matin, votre cabinet apparaît sur quatre annuaires, avec quatre numéros et deux
> adresses.
> Ce n'est pas votre travail qui est en cause, c'est cette fiche : un patient qui cherche un dentiste à
> Bonanjo appelle un numéro que vous n'utilisez peut-être plus, et raccroche.
> Je vous montre ce qu'il voit ?

**⑦ Le Sourire — Bali — 698 00 78 08**
> Bonjour Docteur, je n'ai trouvé votre cabinet qu'à deux endroits : l'annuaire de l'association des
> chirurgiens-dentistes, et les Pages Jaunes.
> Rien à vous, donc — et un patient qui cherche un dentiste à Bali appelle celui qui a une page.
> Je vous montre ce qu'il voit ?

**⑧ IVY — Bonanjo — 697 945 251**
> Bonjour Docteur, sur DoualaTour, votre cabinet de la rue Ivy est classé « ORL et dentiste », avec deux
> numéros et aucune page à lui.
> Le classement n'est pas de votre fait, mais un patient qui cherche un dentiste lit « ORL » et passe au
> suivant.
> Je vous envoie la fiche telle qu'il la lit ?

**⑨ COMED — Bonapriso — 699 915 652**
> Bonjour Docteur, le COMED soigne à Bonapriso depuis 1993, et en ligne il n'y a qu'une ligne
> d'annuaire : un numéro fixe, sans horaires.
> Votre réputation n'est pas en cause, c'est la page qui la porte qui manque — un patient qui cherche un
> ophtalmologue un samedi appelle celui qui affiche ses horaires.
> Je vous montre ce qu'il voit ?

**⑩ CMO Jolinom — Deido — 677 466 425**
> Bonjour Docteur, votre centre est enregistré chez trois assureurs avec deux numéros différents et,
> pour seule adresse, « derrière la pharmacie de la Bourse ».
> Un patient avec une ordonnance appelle le numéro que son assureur lui donne — pas forcément le vôtre.
> Lequel des deux est le bon aujourd'hui ?

### 5.2 · L'exception — le site cassé

**③ Optix — Akwa — 697 72 32 65**
> Bonjour, votre lien optix-sarl.business.site ouvre une page « introuvable » : Google a fermé ce service
> en 2024, sans prévenir les cabinets qui l'utilisaient.
> Ce n'est pas vous qui l'avez cassé, mais quelqu'un qui clique aujourd'hui ne sait plus si vous êtes
> encore ouvert.
> Vous l'avez laissé tomber exprès, ou personne ne vous a prévenu ?

*(La question est double **par nécessité** : deux passés proposés, pas deux actions. La réponse choisit
tout l'angle de la suite.)*

### 5.3 · La relance — **lundi 26/10**, pas avant

Le message d'aujourd'hui a produit une réponse **automatique**, pas humaine : la fenêtre du §7 ne
démarre pas. Ce texte part jeudi si rien d'humain n'est arrivé.

**② Original Optique — 678 92 29 73**
> Bonjour, sur votre compte, deux choses se contredisent : la fiche affiche « ouvert », et le message
> automatique répond « nous ne sommes pas disponibles ».
> Un patient qui écrit à 14 h reçoit une réponse qui dit le contraire de ce qu'il voit.
> Je vous envoie les deux captures côte à côte ?

### 5.4 · Le gabarit de rupture — J+7, une seule fois, **et seulement si le message a été ouvert**

**Condition dure, trouvée dans le dépôt et pas dans ma tête** (`sales/MESSAGES-2026-09-23-PERSUASION.md` §4,
décision de King du 24/09, mot pour mot : *« Pas de relance pour Disc, Tchaya et Afrique Labo, ils n'ont
ouvert aucun de mes messages sur WhatsApp, c'est un signe clair qu'ils ne sont pas intéressés. »*) :

- **deux coches bleues** = lu → une relance de rupture est possible, à J+7, **une seule fois** ;
- **coches grises** = livré, jamais ouvert → **on ne relance pas.** Statut `parked`, raison datée, et
  le fil ne rouvre que si **le cabinet écrit de lui-même**. `parked`, jamais `lost` : personne n'a dit
  non, et une ligne d'appoint qui ne lit pas WhatsApp n'est pas un refus.

> Bonjour Docteur, je clos le sujet de mon côté pour ne pas encombrer votre téléphone.
> Si un jour quelqu'un vous dit « je vous ai cherché sur internet et je ne vous ai pas trouvé », c'est
> de ça que je parlais.
> Bonne continuation.

---

## 6 · Ce qui ne part pas aujourd'hui

| Prospect | Décision | Motif |
|---|---|---|
| **Fashion Vision** | **parqué, définitivement** | message du 24/09 **livré, jamais ouvert** (deux coches grises) → la règle du 24/09 s'applique : **aucune relance**, ni à J+7 ni à J+30. `parked`, raison datée ; le fil ne rouvre que si le cabinet écrit. Ma proposition d'hier (« revient dans 30 jours ») **contredisait une décision de King** |
| **SOS Vision** | parqué | Facebook récent, ni IG ni site : profil de ta thèse — on le **mesure**, on ne mise pas dessus |
| **House of Lunettes** | parqué | page Facebook éducative, aucun site. Même raison |
| **Original Optique** | relance J+2 | réponse automatique reçue aujourd'hui |

**Ce qui manque avant l'envoi, et que je ne peux pas faire d'ici :** vérifier lequel des deux mobiles
ouvre WhatsApp pour Bouda Seidou, Le Sourire, IVY et Jolinom (leçon du 10/10 : 15 pistes sur 18 sont
tombées là).

---

## 7 · Le test, corrigé

**Ta thèse :** ceux qui ont des réseaux sociaux ne voient pas l'utilité d'un site ; ceux qui n'ont rien
sont plus proches de dire oui.

**Ce que le lot teste réellement :** cinq cabinets sans **rien**, jamais contactés. Aucun n'a de compte :
si l'un répond, ta thèse tient au moins sur l'accès.

**Ce qui manque pour conclure :** un bras de comparaison propre. Fashion Vision a été contacté il y a un
mois avec un autre texte ; Original Optique a reçu le message du jour. On peut donc dire **« chez ceux
qui ont des réseaux, deux premières touches, deux silences »** — un fait, pas encore une preuve.

**Mesures gardées :** envoyé / livré / lu / répondu < 48 h / répondu positif / bloqué.

---

## 8 · Sources

**Internes (les plus importantes — elles ont déjà statué) :**
- `knowledge/OUTREACH-MESSAGING-2026-10-22.md` — le motif en 4 temps, le dédouanement, la sortie sans
  friction. **C'est la base de la structure §4.**
- `sales/RESEARCH-STANDARD.md` §10 — cadrage de perte rejeté (O'Keefe & Jensen, r = .016), 97 % et
  « near me » classés US/Tier C.
- `sales/DECLINAISON-9-DECLENCHEURS-2026-09-23.md` §1② — l'attaque déguisée et le cas INSES.
- `sales/DETECTION-FUITES-2026-09-24.md` §2 — une fuite se décrit, ne se chiffre pas.
- `sales/Monday-Outreach-Pack.md` — COPY CRAFT GATE : visualisable / falsifiable / personne d'autre ne
  peut l'écrire.
- `sales/CLIENT-MESSAGING-RULES.md` §1 (ton), §7 (fenêtre), §13 (structure froide).

**Externes (Tier C, hypothèses) :** thedigitalbloom (accroches temporelles 2,3×), datalane et
howtofounder (une seule demande), sbl.so et firstsales.io (WhatsApp froid 3–10 %, 15–20 % avec
personnalisation), sequenzy et overloop (message de rupture). **Aucune n'est citée à un prospect.**

---

## 9 · Comment ce document a été écrit (et ce qui changera au prochain)

```
1. bash tools/graphify/install.sh
2. python3 tools/graphify/build_docs_graph.py            → 10 208 nœuds, 734 documents
3. bash tools/graphify/ask.sh "DM froid accroche gérant" → knowledge/OUTREACH-MESSAGING (oublié ce matin)
4. bash tools/graphify/ask.sh "attaque déguisée perte aversion" → DECLINAISON §1② + AUDIT-SEO
5. lecture de RESEARCH-STANDARD §10                      → le chiffre que j'allais citer est rejeté
6. écriture
```

**Ce que l'étape 3 a changé, concrètement :** la structure est passée de « fait / patient / question »
à « **fait daté / dédouanement / patient / question** ». Le dédouanement n'est pas une politesse :
c'est ce qui empêche le message d'être lu comme un reproche — et c'est écrit chez nous depuis le 22/10.
