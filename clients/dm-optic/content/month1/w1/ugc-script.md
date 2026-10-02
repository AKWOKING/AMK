# UGC IA — Semaine 1 · « À qui confier vos yeux ? »

```
Status: APPROVED (King, 02/10/2026) — prêt pour le producteur   ·  Updated: 2026-10-02
Audience: un habitant de Bonabéri/Douala qui cherche un opticien et ne sait pas à qui se fier
Source asset: le registre ONOC (Littoral l.102, inscription 021/2016) — le seul actif vérifié du cabinet
Funnel stage: notoriété → confiance → premier message WhatsApp
Expected outcome: un message WhatsApp entrant, attribuable à cette accroche
Duration target: 18 s   ·   Language: FR master + variante EN (à produire avant publication)
```

**Portes de la maison** (`content/scripts/README.md` + `CONTENT-LESSONS` §10, §12, §10.4) :

- [x] **Accroche 3 s** — question ou fait précis, une seule personne, aucune auto-présentation
- [x] **Résultat plutôt que caractéristiques** — aucune spécification listée
- [x] **« Pourquoi s'y intéresser ? » par beat** — voir §2, colonne *pourquoi*
- [x] **Zéro remplissage** — relecture à voix haute faite
- [x] **Clarté en 4 questions** — ci-dessous
- [x] **Un seul CTA clair** — un WhatsApp pré-rempli
- [x] **Aucun tiers nommé** — aucun concurrent, aucune marque
- [ ] **Pré-vol en 3 volets : script → visuels → voix** — *le volet voix reste à faire par le producteur*

**Clarté (les 4 questions) :** quoi → *un opticien inscrit, trouvable* · pour qui → *celui qui cherche un
opticien à Bonabéri* · quel résultat → *savoir à qui écrire* · parcours → *méfiance → preuve → contact*.

> **Notre livrable : ce script. La production vidéo est externe (King).**
> Durée cible : **18 s** (règle maison 15–22 s, §12.5) · Vertical **9:16** · **Aucun visage** ·
> Texte à l'écran minimal.
> ⛔ Aucune allégation médicale · aucun témoignage · aucun concurrent nommé · aucun prix.

**Le problème traité.** Pas un problème de vue : un problème de **confiance**. On ne sait pas à qui
confier ses yeux. C'est le problème réel, et c'est celui que la preuve résout.

---

## 1 · Accroche — trois variantes

| # | Accroche (voix + texte, dès l'image 1) | Format viral copié |
|---|---|---|
| **A** | **« Cet opticien exerce depuis 2016. Personne ne le trouvait. »** | Contradiction — l'écart entre le réel et le visible |
| **B** | **« Dix ans d'expérience. Zéro résultat sur Internet. »** | Tension chiffrée — le contraste en deux nombres |
| **C** | **« Vous ne savez pas à qui confier vos yeux ? »** | Interpellation directe + boucle ouverte |

**Recommandation : A.** C'est la plus forte parce qu'elle est **vraie**, **vérifiable** et
**spécifique** — et elle ouvre une boucle qu'on referme à la fin. B est plus percutante mais plus
froide ; C est la plus sûre et la plus faible.

⚠️ **Variante A et B : ne jamais écrire « introuvable » comme un reproche au client.** Le ton est le
constat, pas la plainte.

---

## 2 · Beats — durée totale **18 s**

| # | Temps | Ce qu'on voit | Ce qu'on entend | Pourquoi s'y intéresser |
|---|---|---|---|---|
| **1** | 0:00–0:02 | **Accroche.** Fond uni, le texte se pose **en mouvement**. Un téléphone à plat, une recherche sans résultat — **le plan bouge dès la frame 1** | L'accroche | *Il se reconnaît : il a déjà cherché, sans succès* |
| **2** | 0:02–0:06 | Une main fait défiler une liste de résultats **vide**. L'écran se fige | « Quand on cherche un opticien, on tombe sur des pages sans adresse, sans horaire, sans nom. » | *On nomme exactement ce qu'il a vécu* |
| **3** | 0:06–0:11 | **La preuve.** Une ligne de registre se met en page comme une pièce officielle : *Ordre des opticiens du Cameroun · inscrit depuis 2016* | « Celui-ci est inscrit à l'Ordre des opticiens du Cameroun. Depuis 2016. » | *C'est vérifiable, donc ce n'est pas une promesse* |
| **4** | 0:11–0:14 | Le nom apparaît : **M. Domche Noumbi**. Puis l'adresse : **Ndobo Mayor, Bonabéri** | « Un titulaire nommé. Une adresse réelle. À Bonabéri. » | *Un visage derrière, et c'est à côté de chez lui* |
| **5** | 0:14–0:18 | **Payoff.** La carte complète se pose. Le bouton WhatsApp apparaît | « Maintenant, vous pouvez lui écrire. » | *L'action est immédiate et sans risque* |

⚠️ **Le beat 1 contient 2 secondes, pas 3.** C'est délibéré : §12.1 mesure notre falaise de rétention à
**0:02** — tout ce qui suit la seconde 2 est vu par ~1 spectateur sur 5. **L'accroche doit donc être
entièrement lue avant 0:02**, et le plan 0:00–0:02 doit contenir un **mouvement réel** + la **voix**.

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
| 7 | **⛔ Ne jamais animer l'élément démontré** — le bouton WhatsApp peut apparaître, il ne doit pas « cliquer » | §3.8 / §10.3 |

⚠️ **Volet voix non fait.** La porte de pré-vol maison a trois volets : **script → visuels → voix**. Le
script est approuvé ; **le choix de la voix reste à faire par le producteur**, et il doit être ré-auditionné
avant le premier rendu (décision de King, §11.2).

---

## 3 · Texte à l'écran (minimal — la règle de Ryan Collins)

| Beat | Texte |
|---|---|
| 1 | L'accroche, mot pour mot |
| 2 | *aucun* — l'image suffit |
| 3 | **Inscrit depuis 2016** |
| 4 | **M. Domche Noumbi · Bonabéri** |
| 5 | **DM OPTIQUE SARL** · bouton WhatsApp |

**Règle : une seule idée par plan.** Pas de texte sur les plans 2 — l'écran vide **est** le message.

---

## 4 · Image de payoff

**La carte d'identité** — le seul actif vérifié du cabinet, mise en page comme une pièce officielle :

```
┌─────────────────────────────────┐
│  DM OPTIQUE SARL                │
│  Opticien · Douala              │
│                                 │
│  Inscrit à l'Ordre depuis 2016  │
│  Titulaire · M. Domche Noumbi   │
│                                 │
│  Ndobo Mayor · Bonabéri         │
│  8h00 – 17h30                   │
└─────────────────────────────────┘
```

⚠️ **N'écrire que ce qui est confirmé.** L'adresse et les heures le sont (données du client, 25/09).
**Les jours d'ouverture ne le sont pas — ne pas les écrire.**

---

## 5 · CTA

| | |
|---|---|
| **À l'écran** | « Écrivez-nous, on vous répond » |
| **WhatsApp pré-rempli (variante A)** | `Bonjour, je cherche un opticien inscrit à Bonabéri` |
| **Variante B** | `Bonjour, je viens de la vidéo « dix ans d'expérience »` |
| **Variante C** | `Bonjour, je cherche un opticien à Bonabéri` |

⚠️ **Un message différent par variante** — sinon le coût par message n'est pas attribuable
(`README.md` §5).

**Le geste en deux temps :** *« Écrivez-nous, on vous répond — et venez essayer au cabinet. »*

---

## 6 · Notes de direction

| Point | Instruction |
|---|---|
| **Visages** | ⛔ **Aucun.** Mains, téléphone, typographie seulement |
| **Plan produit** | ⛔ **Aucune monture** dans cette vidéo — c'est une vidéo de **confiance**, pas de produit |
| **Mouvement** | Un seul travelling fluide sur la carte qui se pose. **Rien d'autre.** Élégant, intentionnel — pas d'effet gratuit |
| **Moment surréel** | **Non.** Cette vidéo gagne par la **sobriété** : une pièce officielle ne se met pas en scène |
| **Palette** | Fond blanc · encre · **un seul accent** (le teal retenu, `website/brief.md` §7) |
| **Typographie** | La même que le site — cohérence entre la pub et la page sur laquelle elle envoie |
| **Son** | Voix seule, ou voix + musique **libre de droits**. ⛔ **Aucun son d'une autre marque** |
| **Étiquette IA** | Si la plateforme l'exige, **l'appliquer**. Ne pas faire passer du généré pour du réel |

**Ce qui rend cette vidéo difficile à copier.** Elle ne montre **rien qu'un concurrent puisse
revendiquer** : un numéro d'inscription, un nom, une adresse. **Le test de l'échange** tient — avec un
autre nom, la vidéo s'effondre.
