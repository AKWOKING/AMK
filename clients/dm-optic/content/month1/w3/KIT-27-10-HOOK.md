# KIT — mardi 27/10 · TikTok 19 h + Facebook 20 h 30 · DM Optique

```
Pièce      tiktok-01-v2 · « 20 minutes d'écran » (23,00 s, 1080×1920, validée par King le 22/10)
Le changement d'aujourd'hui    l'accroche, et elle seule : un carton de 3 s en ouverture, une phrase
                               d'accroche dite par-dessus (facultative ce soir), et une ligne de partage
                               à la fin. Aucune image, aucune voix d'origine, aucun plan n'est refait.
Décision de King à respecter    « okay to post tiktok-01-v2 on tuesday » (22/10) — le film ne change pas.
Règle appliquée                knowledge/HOOK-FIRST-2026-10-27.md (texte > visuel > parlé ·
                               alignement des trois composantes · carton lisible muet)
Porte                          tools/qa/audit_post_dm.py + tools/qa/audit_hook.py
Fait le                        27/10/2026, tour 192
```

> ⚠️ **Ce que je n'ai pas, et qui bloque un envoi sans toi.** Le fichier `tiktok-01-v2.mp4` n'est **pas
> dans le dépôt** (`*.mp4` est ignoré) et **il n'existe pas dans cet environnement**. Le carton ci-dessous
> est livré en image : il s'insère dans CapCut en deux minutes. Si le master est perdu de ton côté aussi,
> **ne publie pas** — le repli est écrit au §6, il ne demande ni tournage ni montage.

---

## 1 · L'accroche — trois composantes, alignées

| Composante | Ce qui est écrit / montré / dit | Secondes |
|---|---|---|
| **texte** | **20 SECONDES / À 6 MÈTRES** en grand, **8 HEURES À 40 CM** en petit au-dessus (le point de départ, en gris) — sur le carton livré | 0,0–3,0 |
| **visuel** | l'intérieur du cabinet (`cabinet-interieur.webp`), zoom arrière très lent — le carton est **posé dessus**, il ne remplace pas l'image | 0,0–3,0 |
| **parlé** | « Vingt minutes d'écran. Puis vingt secondes. À six mètres. » — la voix existante, **inchangée** | 0,0–3,2 |

**Pourquoi ça tient en une seconde, sans son** : trois nombres, deux couleurs. Le gris dit d'où l'on part
(40 cm), le blanc et le pêche disent ce qu'on gagne (20 secondes à 6 mètres). Le contraste **est** le texte
— ce n'est pas une phrase qui décrit le contraste.

**Les deux phrases d'accroche, vérifiées séparément** (la porte ne juge pas un carton tout seul) :

| Accroche | Où | Porte | Verdict |
|---|---|---|---|
| « 8 heures à 40 cm, pas une seconde à 6 mètres. Regardez au loin 20 secondes : vos yeux repartent. » | **prononcée** | `audit_hook` | ✅ **4/4** — sujet, action, objectif, contraste |
| **20 SECONDES / À 6 MÈTRES** (+ *8 heures à 40 cm*) | **à l'écran** | `audit_post_dm` §1 | ✅ trois nombres communs avec la voix, fenêtre 0,0–3,0 s |

Et la phrase que le master prononce réellement — « Vingt minutes d'écran. Puis vingt secondes. À six
mètres. » — **échoue** à `audit_hook` (0 mot sur 4 : ni sujet, ni action, ni contraste). C'est le
diagnostic exact de la pièce du 22/10, et c'est pour ça que l'accroche de la version de ce soir ajoute
**une phrase à dire** au-dessus de l'image : cinq secondes de voix, rien d'autre ne bouge.

**Pourquoi c'est la même chose que la voix** : la voix dit « vingt secondes » et « six mètres » ; le
carton dit « 20 secondes » et « 6 mètres ». Deux nombres communs, aucun mot qui promet autre chose.

**Trois accroches écrites, deux écartées** (règle du 27/10, appliquée pour la première fois) :

| # | Accroche | Verdict |
|---|---|---|
| 1 | **8 HEURES À 40 CM · 20 SECONDES À 6 MÈTRES** | **retenue** — contraste visuel immédiat, aucun mot à comprendre, tient muette |
| 2 | « Vos yeux passent la journée à 40 cm » | **écartée** — un constat sans action ni objectif (`audit_hook` : 2 mots sur 4) |
| 3 | « Regardez au loin 20 secondes toutes les 20 minutes » | **écartée** — l'action est là, mais aucun contraste : c'est une consigne, pas une accroche |

**Ce que le carton ne dit pas** : ni le nom du cabinet, ni « Bonabéri », ni un prix, ni une promesse. La
marque arrive au carton final, quand le spectateur est encore là — pas avant.

---

## 2 · TikTok — 19 h 00

```text
8 heures à 40 cm. 20 secondes à 6 mètres. C'est tout.

Vos yeux travaillent à 40 cm toute la journée. Ils ne sont pas faits pour ça.
Toutes les 20 minutes, regardez au loin 20 secondes — 6 mètres suffisent.

Ce n'est pas un traitement, c'est une pause. Et si ça reste flou, ce n'est plus une question d'écran :
on mesure, on ne devine pas.

📍 Immeuble West Hotel, 1er étage, dernière porte à droite — Ndobo Mayor, Bonabéri
🕗 Examen de vue : lundi à samedi, 8h30–13h00
💬 Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20votre%20vid%C3%A9o%20des%2020%20secondes%20sur%20TikTok.%20Je%20voudrais%20un%20examen%20de%20vue.

#dmoptique #opticienbonaberi #douala #cameroun
```

- **Sous-titres manuels** — jamais l'automatique (ruling 11/10) : le fichier `tiktok-01-v2.fr.srt`
  est déjà écrit, 7 blocs.
- **Commentaire épinglé** :
  > La règle en clair : toutes les 20 minutes, 20 secondes à regarder au loin (6 mètres environ).
  > Une monture vous intéresse ? Envoyez son nom, on vous dit si elle est au cabinet — et on vous envoie
  > sa photo. WhatsApp 656 122 239 · examen de vue 8h30–13h00, du lundi au samedi.
- **Un seul CTA dans la légende** : écrire. La demande de partage est dans la vidéo, pas ici.
- **Le lien porte son texte** : qui écrit arrive avec « j'ai vu votre vidéo des 20 secondes sur TikTok ».
  Aucune pièce publiée avant aujourd'hui ne permettait de savoir d'où venait une conversation.

---

## 3 · Facebook — 20 h 30, le même soir

Le film y passe **aussi** (même fichier), mais la légende fait un autre travail : Facebook se lit.

```text
8 heures à 40 cm. 20 secondes à 6 mètres. C'est tout le principe.

Vos yeux ne sont pas faits pour rester à 40 cm. Ils sont faits pour regarder au loin.

Toutes les 20 minutes : 20 secondes à 6 mètres. Rien à acheter, rien à installer.
Et si ça reste flou après la pause, ce n'est plus une question d'écran : c'est le moment de mesurer.

Montrez cette vidéo à quelqu'un qui passe la journée devant un écran.

📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri
🕗 Examen de vue : 8h30–13h00, du lundi au samedi
💬 Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20j%27ai%20vu%20votre%20publication%20Facebook%20sur%20les%2020%20secondes.

#dmoptique #opticienbonaberi #douala #cameroun
```

- **Alt text** (le film) : *« Vidéo : l'intérieur du cabinet DM Optique à Bonabéri, les montures présentées sur les murs, puis trois montures photographiées une par une. »* — **alt de l'image de repli** : *« Trois montures du cabinet sur fond crème, avec l'accroche “8 heures à 40 cm, 20 secondes à 6 mètres”. »*
- Le texte prérempli **diffère** de celui de TikTok — c'est tout l'intérêt : deux liens, deux provenances.
- Même règle de CTA : un seul geste demandé (**écrire**). La ligne « Montrez cette vidéo à… » n'est pas
  une action demandée au spectateur pour nous, c'est une recommandation familiale — et c'est le seul
  geste qui peut remplacer les 0 partages du 23/10.

---

## 4 · La réponse d'accueil (à coller telle quelle)

> Bonjour, ici **DM Optique**, Ndobo Mayor (Bonabéri) — vous écrivez pour un examen de vue ?
> L'examen se fait le matin, **8h30–13h00**, du lundi au samedi, par Monsieur Domche.
> Deux choses et je vous propose une heure : c'est pour un adulte ou un enfant, et vous portez déjà
> des lunettes ?

*(puis, quand l'heure est choisie — le vrai message qui fait venir)*

> C'est noté pour **jeudi 8h45**. Le cabinet est au 1er étage de l'immeuble West Hotel, dernière porte à
> droite. Vous n'avez rien à apporter ; si vous avez une ancienne ordonnance, prenez-la.
> Le numéro du cabinet : 656 122 239.

Aucun délai promis, aucune disponibilité inventée : on propose une heure, le cabinet confirme.

---

## 5 · Ce qu'on compte, et ce que ça décide

| Moment | Vues | Messages reçus | dont **20 secondes** | Conversations qualifiées | Photos envoyées |
|---|---|---|---|---|---|
| J+1 (28/10) | | | | | |
| J+7 (03/11) | | | | | |

**Trois nombres seulement décident** : combien de messages portent le texte prérempli, combien deviennent
une heure proposée, combien viennent au cabinet. Les vues ne décident rien — le 23/10, 227 vues ont donné
**1 clic et 0 conversation attribuable**.

**Le seuil écrit d'avance** (sinon on expliquera le résultat après coup) : à moins de **5 messages
préremplis** sur l'ensemble des deux plateformes, il n'y a **pas de résultat** — on ne conclut pas, on
passe à la pièce suivante.

---

## 6 · Le montage — deux minutes, dans CapCut

1. Ouvrir `tiktok-01-v2.mp4`.
2. Poser `assets/hook-tt-1080x1920.jpg` **sur la piste principale, à 0,0**, et le tenir **3,0 s**
   (l'image du cabinet passe dessous : le carton est prévu avec un voile sombre à **62 %**, la vidéo se
   voit au travers).
3. **La voix d'accroche** : enregistrer, par-dessus le début, la phrase du tableau §1 — *« 8 heures à
   40 cm, pas une seconde à 6 mètres. Regardez au loin 20 secondes : vos yeux repartent. »* Elle se pose sur
   les **3 premières secondes** et la voix d'origine reprend à 3,2 s. Si l'enregistrement n'est pas possible
   aujourd'hui, **on publie sans** : le carton porte les trois nombres, et c'est lui qui est lu.
4. Vérifier en **coupant le son** : les trois nombres se lisent-ils en une seconde ? Si non, on raccourcit
   le texte, jamais la durée.
5. À la fin, ajouter la ligne de partage **en texte à l'écran** sur les 2 dernières secondes :
   **« Montrez ça à quelqu'un qui passe la journée devant un écran. »** (la voix ne change pas)
6. Exporter 1080×1920 · 30 fps · H.264.

**Le repli, si le master n'existe plus** : publier `assets/post-fb-1080x1350.jpg` sur Facebook (une image,
la même légende) et **ne rien publier sur TikTok** ce soir. Une image juste vaut mieux qu'une vidéo
absente — et une vidéo refaite à la hâte sans la voix validée n'est pas la même pièce.

---

## 7 · Les fichiers de ce kit

| Fichier | Ce que c'est | Usage |
|---|---|---|
| `assets/hook-tt-1080x1920.jpg` | le carton d'accroche, 1080×1920, voile à 78 % | piste principale, 0,0 → 3,0 s |
| `assets/post-fb-1080x1350.jpg` | la carte Facebook, 1080×1350, fond crème des fiches produit | repli, ou publication du soir |

Les deux sont rendus avec les **vraies** polices du cabinet (Schibsted Grotesk 700 / IBM Plex Sans 400),
les **vraies** couleurs du site (`#1A3F86`, `#0A1220`, `#EEF1F5`) et **aucune image générée**.

---

## 8 · Ce qui n'est pas vérifié, et qui doit se dire

- Le master `tiktok-01-v2.mp4` **n'est pas dans cet environnement** : je n'ai mesuré ni sa durée, ni son
  audio, ni ses images. Les 23,00 s et 4,3 Mo viennent du contrôle du 22/10 (§8 de `tiktok-01-v2-20-20-20.md`).
- Les heures (`8h30–13h00`, lundi à samedi) sont celles publiées depuis le 22/10 ; **aucune confirmation
  écrite du cabinet** n'est au dépôt. Si elles ont changé, c'est la légende **et** la fiche Google qui
  changent le même jour.
- Le prénom du praticien n'est pas écrit ici : « Monsieur Domche » vient de `FUNNEL-WHATSAPP` §2.
- **Facebook** : le film de 23 s dépasse la fourchette maison de 16–22 s pour ce réseau (§4 bis de
  `CONTENT-CREATION`). On publie quand même le même master aujourd'hui — découper une deuxième version
  sans le fichier serait un pari, pas un montage.
