# UGC IA — Semaine 4 · « Ce qui protège vos yeux au quotidien »

```
Status: APPROVED (King, 02/10/2026) — prêt pour le producteur   ·  Updated: 2026-10-02
Audience: quelqu'un exposé aux écrans, à la route, à la lecture ou au soleil
Source asset: les types de verres du cabinet — **à confirmer par le client**, §7
Funnel stage: pertinence → éducation → demande de conseil WhatsApp
Expected outcome: un message WhatsApp demandant conseil sur ses verres
Duration target: 20 s   ·   Language: FR master + variante EN (à produire avant publication)
```

**Portes de la maison** (`content/scripts/README.md` + `CONTENT-LESSONS` §10, §12, §10.4) :

- [x] **Accroche 3 s** — question ou fait précis, une seule personne, aucune auto-présentation
- [x] **Résultat plutôt que caractéristiques** — aucune spécification listée
- [x] **« Pourquoi s'y intéresser ? » par beat**
- [x] **Zéro remplissage** — relecture à voix haute faite
- [x] **Clarté en 4 questions** — ci-dessous
- [x] **Un seul CTA clair** — un WhatsApp pré-rempli
- [x] **Aucun tiers nommé** — aucun concurrent, aucune marque
- [ ] **Pré-vol en 3 volets : script → visuels → voix** — *le volet voix reste à faire par le producteur*

**Clarté (les 4 questions) :** quoi → *des verres adaptés aux situations réelles* · pour qui → *écran · route · lecture · soleil* ·
quel résultat → *des yeux moins sollicités* · parcours → *constat → prise de conscience → conseil*.


> **Notre livrable : ce script. La production vidéo est externe (King).**
> Durée cible : **20 s** (règle maison 15–22 s, §12.5) · Vertical **9:16** · **Aucun visage** · **Aucun verre en gros plan.**
>
> ⚠️ **Le sujet le plus réglementé du mois.** Un verre est un **dispositif optique**. Lire §7 — et
> noter que tout gros plan de verre en IA est une **dérogation**.

**Le problème traité.** Quatre situations réelles — écran, conduite, lecture, soleil — où les yeux
travaillent. **Décrites comme des situations, jamais comme des symptômes, et sans aucune performance
promesse.**

---

## 1 · Accroche — trois variantes

| # | Accroche | Format viral copié | Risque |
|---|---|---|---|
| **A** | **« Huit heures d'écran. Vos yeux le sentent. »** | Chiffre concret + ressenti | ✅ **Aucun** — « le sentent » est un ressenti, pas un diagnostic |
| **B** | **« Quatre situations où vos yeux travaillent. »** | Liste annoncée | ✅ **Aucun** — descriptif |
| **C** | **« Le soleil de Douala. Vos yeux le paient. »** | Image locale forte | ⚠️ **« le paient » sous-entend un dommage. À reformuler ou écarter** |

**Recommandation : B** — la plus sûre, et elle structure toute la vidéo (les quatre situations **sont** le
script). **A** est la plus percutante sans risque ; à tester en variante publicitaire.

⛔ **C est écartée.** « Payer » implique un dommage causé — on glisse vers l'allégation.

---

## 2 · Beats

| # | Temps | Ce qu'on voit | Ce qu'on entend |
|---|---|---|---|
| **1** | 0:00–0:02 | **Accroche.** Un écran allumé, de face | L'accroche |
| **2** | 0:02–0:11 | **Quatre situations, quatre plans courts.** L'**écran** · le **volant** · le **livre** · le **soleil** de face | « L'écran. La route. La lecture. Le soleil. Quatre moments où vos yeux travaillent. » |
| **3** | 0:11–0:16 | **Le geste du métier.** Le montage, l'ajustement — les mains, **l'objet** | « Ce que vous en faites change ce qu'il vous faut. Et ça se règle au cabinet. » |
| **4** | 0:16–0:20 | **Payoff.** Les quatre mots alignés : **écran · route · lecture · soleil** + le bouton WhatsApp | « Dites-nous ce que vous en faites. On vous répond. » |

---

## 2b · Contraintes de production — règles dures de la maison

| # | Règle | Source |
|---|---|---|
| 1 | **Première coupe ≤ 1,5 s.** Aucune image immobile à l'ouverture | §12.2 |
| 2 | **Mouvement + voix dès la frame 1** — jamais une ouverture figée | §12.1–12.2 |
| 3 | **La frame 0 est la vignette** : poser la meilleure image en frame 0. Le canal de partage est **WhatsApp**, où la vignette décide du clic | §10.4 |
| 4 | **Lisibilité :** une étiquette reste **≥ 0,8 s** · une phrase **≥ 0,3 s × nombre de mots**. *Fast-in, then hold — jamais fast-in, then gone* | §10.4 |
| 5 | **La narration est dans le fichier livré** — `ffmpeg -i` doit afficher une piste audio. Un son ajouté à la publication n'est pas un substitut | §12.3 |
| 6 | **Musique libre de droits, ou silence + voix.** Jamais un son pris sur une autre publication | §15 (02/10) |
| 7 | **⛔ Ne jamais animer l'élément démontré** | §3.8 / §10.3 |

⚠️ **Volet voix non fait.** La porte de pré-vol maison a trois volets : **script → visuels → voix**.
Le script est approuvé ; **le choix de la voix reste à faire par le producteur**, ré-auditionné avant
le premier rendu (décision de King, §11.2).

⚠️ **L'accroche tient en 2 secondes, pas 3.** §12.1 mesure notre falaise de rétention à **0:02** : tout
ce qui suit la seconde 2 est vu par ~1 spectateur sur 5. Les durées de ce script ont été **ramenées
dans la cible maison 15–22 s** (§12.5) — elles dépassaient.

---

## 3 · Texte à l'écran

| Beat | Texte |
|---|---|
| 1 | L'accroche, mot pour mot |
| 2 | **ÉCRAN** · **ROUTE** · **LECTURE** · **SOLEIL** — un mot par plan |
| 3 | **Ça se règle au cabinet** |
| 4 | **Quel est votre usage ?** · bouton WhatsApp |

⚠️ **Un seul mot par plan.** C'est ce qui rend la vidéo lisible **sans le son** — et la plupart
regardent sans le son.

---

## 4 · Image de payoff

Les quatre usages, en grille sobre :

```
ÉCRAN · ROUTE · LECTURE · SOLEIL

Quel est le vôtre ?
Écrivez-nous — on vous répond.

DM OPTIQUE SARL · Ndobo Mayor, Bonabéri
```

**Pourquoi cette image.** Elle ne vend **aucun produit** : elle pose une **question**. Et une question
appelle un message WhatsApp — ce qui est exactement ce qu'on mesure.

---

## 5 · CTA

| | |
|---|---|
| **À l'écran** | « Dites-nous ce que vous en faites — on vous répond » |
| **WhatsApp pré-rempli (variante A)** | `Bonjour, je passe 8 heures par jour devant un écran` |
| **Variante B** | `Bonjour, j'ai une question sur mes verres` |

⚠️ **La variante A est meilleure** : elle arrive avec un **contexte**, donc la conversation démarre
vraiment. Et elle est **attribuable** — on sait quelle accroche l'a produite.

---

## 6 · Notes de direction

| Point | Instruction |
|---|---|
| **Visages** | ⛔ **Aucun** |
| **Verre en gros plan** | ⛔ **Aucun.** Voir §7 |
| **Ce qu'on montre** | Les **situations** (écran, volant, livre, soleil) et les **mains** au montage. Jamais le produit comme héros |
| **Moment surréel** | ⛔ **Interdit.** Un jeu d'échelle sur un verre affirme une propriété optique. Sur les situations, c'est inutile |
| **Mouvement** | Quatre coupes franches, un seul plan long sur le geste du montage |
| **Lumière** | Les quatre situations ont **quatre lumières différentes** — c'est le récit : chaque usage a sa contrainte |
| **Son** | Voix posée, aucune dramatisation |

---

## 7 · ⛔ Le verre est un dispositif — deux règles absolues

### Règle 1 : aucun verre en gros plan généré par IA

Un rendu IA d'un verre affirme une **propriété optique** qu'aucune prise de vue réelle ne garantit :
reflet, traitement, teinte, épaisseur.

**Exemples concrets du risque :**

| Image générée | Ce qu'elle affirme sans qu'on l'ait dit |
|---|---|
| Un verre sans **aucun** reflet | un **antireflet** qu'on ne peut pas garantir |
| Un verre qui **fonce** au soleil | un **photochromique** qu'on ne vend peut-être pas |
| Une teinte précise | une **catégorie de protection** non vérifiée |

**Sur un produit de santé, une image exagère plus fort qu'une phrase.** C'est pourquoi cette demande est
consignée comme **dérogation** dans `dossier.md` §6 : elle doit être **signalée** et **tranchée par
King**, pas décidée en production.

### Règle 2 : le vocabulaire

| ✅ Autorisé | ⛔ Interdit |
|---|---|
| « **protège** vos yeux » | « **soigne** » · « **guérit** » |
| « adapté à la **conduite** » | « **améliore** la vision » |
| « confortable à la **lecture** » | « **réduit** la fatigue oculaire de X % » |
| « ce que vous en faites **change ce qu'il vous faut** » | « **corrige** votre vue » |
| « **ça se règle** au cabinet » | « vos maux de tête **disparaîtront** » |

**La règle de fond :** on décrit **l'usage**, jamais **l'effet**. « Adapté à la conduite » parle d'une
situation ; « améliore la vision » promet un résultat.

### ⚠️ Les verres techniques — progressifs, photochromiques, antireflet

La recherche (Muffin Group) les cite comme des **pages de catégorie**. Si le client en vend, on peut en
parler — **mais uniquement par l'usage** :

- ✅ « pour ceux qui lisent de près et regardent de loin »
- ⛔ « élimine le besoin de changer de lunettes »

**Question à poser à la visite :** quels types de verres le cabinet propose réellement ? Rien ne
s'écrit avant la réponse.

---

## 8 · Ce qui rend ce script sûr

Il ne nomme **aucun produit**, ne promet **aucun effet**, et se termine par **une question**. Tout son
poids repose sur quatre mots que n'importe qui reconnaît : **écran · route · lecture · soleil**.

C'est aussi le script le plus **réutilisable** en publicité : les quatre situations font **quatre
accroches** naturelles, et donc quatre variantes mesurables séparément.
