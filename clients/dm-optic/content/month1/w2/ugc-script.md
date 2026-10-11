# UGC IA — Semaine 2 · « Ce qui se passe pendant un examen de vue »

```
Status: APPROVED (King, 02/10/2026) — prêt pour le producteur   ·  Updated: 2026-10-02
Audience: quelqu'un qui n'a jamais passé d'examen de vue, ou qui pense que ce n'est pas pour lui
Source asset: le cabinet et ses instruments (photos W2) · le protocole d'examen, décrit sans diagnostic
Funnel stage: confiance → compréhension → demande de rendez-vous WhatsApp
Expected outcome: un message WhatsApp demandant un examen
Duration target: 22 s   ·   Language: FR master · variante EN différée (King 02/10), non bloquante
```

**Portes de la maison** (`content/scripts/README.md` + `CONTENT-LESSONS` §10, §12, §10.4) :

- [x] **Accroche 3 s** — question ou fait précis, une seule personne, aucune auto-présentation
- [x] **Résultat plutôt que caractéristiques** — aucune spécification listée
- [x] **« Pourquoi s'y intéresser ? » par beat**
- [x] **Zéro remplissage** — relecture à voix haute faite
- [x] **Clarté en 4 questions** — ci-dessous
- [x] **Un seul CTA clair** — un WhatsApp pré-rempli
- [x] **Aucun tiers nommé** — aucun concurrent, aucune marque
- [x] **Pré-vol en 3 volets : script → visuels → voix** — *voix de la maison (voice-00), même voix que le moteur de contenu AMK (King 02/10)*

**Clarté (les 4 questions) :** quoi → *un examen de vue, concret* · pour qui → *celui qui n'a jamais osé* ·
quel résultat → *savoir ce qui l'attend, sans surprise* · parcours → *appréhension → familiarité → rendez-vous*.


> **Notre livrable : ce script. La production vidéo est externe (King).**
> Durée cible : **22 s** (règle maison 15–22 s, §12.5) · Vertical **9:16** · **Aucun visage** · Texte à l'écran minimal.
>
> ⚠️ **C'est le script le plus exposé du mois.** Il traite de symptômes ressentis. Lire §7 avant
> toute production.

**Le problème traité.** La fatigue des yeux en fin de journée — **décrite comme une situation vécue,
jamais comme un diagnostic**. Et la peur silencieuse derrière : **« est-ce qu'on va m'expédier ? »**

---

## 1 · Accroche — trois variantes

| # | Accroche | Format viral copié | Risque |
|---|---|---|---|
| **A** | **« Vous plissez les yeux en fin de journée ? »** | Interpellation sur un geste que tout le monde reconnaît | ✅ **Aucun** — décrit un comportement, pas une cause |
| **B** | **« Trois signes que vos yeux fatiguent. »** | Liste annoncée | ⚠️ **Faible** — « signes » flirte avec le symptôme. Ne pas aller plus loin |
| **C** | **« Vos yeux fatiguent. Ce n'est peut-être pas seulement l'écran. »** | Contradiction + boucle ouverte | ⛔ **Élevé** — **« ce n'est peut-être pas seulement l'écran » sous-entend une cause médicale. À écarter** |

**Recommandation : A.** C'est la seule qui soit **à la fois percutante et sans risque** : elle décrit un
**geste** que le spectateur reconnaît, sans rien affirmer sur sa cause ni sur son traitement.

⛔ **La variante C est écartée volontairement**, alors qu'elle est la plus efficace en théorie. C'est le
prix de la règle : **sur un produit de santé, on perd une bonne accroche plutôt que de prendre une
allégation.**

---

## 2 · Beats

| # | Temps | Ce qu'on voit | Ce qu'on entend |
|---|---|---|---|
| **1** | 0:00–0:02 | **Accroche.** Un écran lumineux dans la pénombre, une main qui se rapproche | L'accroche |
| **2** | 0:02–0:07 | Trois situations, trois plans courts : **un écran** · **un volant** · **un livre rapproché** | « L'écran. La route. Le livre qu'on rapproche. » |
| **3** | 0:07–0:13 | **L'examen, démystifié.** L'instrument, la salle, le geste — **ce qui se passe vraiment** | « Un examen de vue, ce n'est pas une formalité. On prend le temps de regarder comment vous voyez. » |
| **4** | 0:13–0:18 | **Ce qu'il faut apporter.** Trois objets se posent : une ordonnance · une ancienne monture · un carnet | « Apportez votre ordonnance si vous en avez une, votre ancienne monture, et vos questions. » |
| **5** | 0:18–0:22 | **Payoff.** Les horaires de consultation + le bouton WhatsApp | « La consultation se tient de 8h30 à 13h30. Écrivez-nous avant de venir. » |

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

✅ **Voix tranchée (King 02/10).** La narration porte la **voix de la maison (voice-00)** — la même
que le moteur de contenu AMK (`CONTENT-LESSONS` §11.2). **Plus d'audition à prévoir.**
**Variante EN différée, non bloquante** : le FR part en production d'abord ; l'EN suivra en seconde ligne.

⚠️ **L'accroche tient en 2 secondes, pas 3.** §12.1 mesure notre falaise de rétention à **0:02** : tout
ce qui suit la seconde 2 est vu par ~1 spectateur sur 5. Les durées de ce script ont été **ramenées
dans la cible maison 15–22 s** (§12.5) — elles dépassaient.

---

## 3 · Texte à l'écran

| Beat | Texte |
|---|---|
| 1 | L'accroche, mot pour mot |
| 2 | *aucun* |
| 3 | **Ce qui se passe, vraiment** |
| 4 | **1 · L'ordonnance** · **2 · L'ancienne monture** · **3 · Vos questions** |
| 5 | **Consultation 8h30 – 13h30** · bouton WhatsApp |

⚠️ **Les horaires de consultation (8h30–13h30) sont confirmés** par le client (25/09).
⛔ **Les JOURS ne le sont pas** — ne pas écrire « du lundi au samedi » ni aucun jour.

---

## 4 · Image de payoff

Une **carte « quoi apporter »**, trois lignes, sobre :

```
AVANT DE VENIR
1 · Votre ordonnance, si vous en avez une
2 · Votre ancienne monture
3 · Vos questions

Consultation · 8h30 – 13h30
DM OPTIQUE SARL · Ndobo Mayor, Bonabéri
```

**Pourquoi cette image fonctionne.** Elle répond à la vraie peur — **« est-ce qu'on va m'expédier ? »** —
en montrant une liste préparée. Une liste préparée **est** la preuve qu'on prend le temps.

---

## 5 · CTA

| | |
|---|---|
| **À l'écran** | « Écrivez-nous avant de venir — on vous dit quoi apporter » |
| **WhatsApp pré-rempli (variante A)** | `Bonjour, je souhaite un examen de vue` |
| **Variante B** | `Bonjour, je viens de la vidéo « trois signes » — je souhaite un examen` |

---

## 6 · Notes de direction

| Point | Instruction |
|---|---|
| **Visages** | ⛔ **Aucun.** Mains, objets, point de vue subjectif (l'écran vu de face, le volant vu du conducteur) |
| **Plan produit** | ⛔ **Aucune monture sur un visage.** L'ancienne monture apparaît **posée**, comme un objet |
| **Mouvement** | Trois coupes franches sur les trois situations, puis un travelling lent sur la salle |
| **Moment surréel** | ⛔ **Interdit ici.** On est dans le **soin** : le surréel discréditerait le sérieux |
| **Lumière** | La pénombre du beat 1 contraste avec la lumière franche du beat 3 — **c'est le récit visuel** : de la fatigue à la clarté |
| **Son** | Voix calme, posée. **Jamais** de musique dramatique — ce n'est pas une urgence |

---

## 7 · ⛔ La ligne rouge médicale — à lire avant de produire

La demande créative portait sur **« squinting, headaches »**. **Les maux de tête sont le point le plus
dangereux du mois.**

| ✅ Ce que le script dit | ⛔ Ce qu'il ne dit **jamais** |
|---|---|
| « Vous **plissez les yeux** en fin de journée ? » — un **geste** observable | « Vos **maux de tête** viennent de vos yeux » — un **diagnostic** |
| « Vos yeux **fatiguent** » — un **ressenti** | « Des lunettes **font disparaître** les maux de tête » — une **thérapie** |
| « Un examen permet de **savoir où vous en êtes** » | « Un examen **corrige** votre vision » |

**Pourquoi on tient cette ligne.** Le cabinet est **inscrit à l'Ordre** et c'est une **SARL sous
contrôle fiscal**. Une allégation thérapeutique dans une publicité engage **le cabinet**, pas seulement
nous — et c'est exactement le type d'affirmation qu'un contrôle relève.

**Le mot « maux de tête » n'apparaît donc dans aucun script du mois 1.** Si King veut l'utiliser, c'est
une **dérogation** à signaler et à trancher — `dossier.md` §6.

**La substitution qui garde l'efficacité :** au lieu de nommer le symptôme, **montrer le geste**. Tout le
monde reconnaît « plisser les yeux » ; personne ne peut y voir un diagnostic.
