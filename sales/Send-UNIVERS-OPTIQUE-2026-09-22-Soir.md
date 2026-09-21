# Envoi dû DEMAIN MATIN — UNIVERS OPTIQUE (Bépanda) · écrit 21/09 23:20

> **Ce que cette feuille envoie, et dans quel ordre.** Le fil est simple : message 1 parti **lun 21/09 17:50**,
> il répond **17:56 « Combien ça me coûte »**, King chiffre **18:08** et promet **« un aperçu gratuit d'ici
> demain pour que vous puissiez voir concrètement à quoi cela va ressembler »**. Cette phrase est une **date**:
> l'aperçu doit partir **avant 09:00 mardi 22/09**, et pendant la fenêtre promise il passe **devant toute autre
> réponse à écrire** (règle maison : une promesse d'envoi est la tâche, pas une intention).
> Étapes CRM déjà posées **dans le générateur** (`leads/build/crm.py` → `EVENING_2109`) : `stage = closing` ·
> `Follow-up date = 2026-09-22` · et **l'heure d'envoi n'est pas écrite avant que tu me la donnes** — on ne se
> déclare pas un envoi à soi-même.

---

## ① D'ABORD le fichier (l'aperçu, pas un lien à inventer)

`demos/concept-univers-optique-v1.html` — **928 Ko**, un seul fichier, trois visuels de concept inlinés,
FR|EN commutable, s'ouvre dans le navigateur d'un téléphone. Contrôles : `audit_html.py` = **0 finding**
(459 runs de texte, desktop 459 / mobile 459) sur la démo **et** sur `hosting/previews/univers/index.html`,
`diff` démo ↔ aperçu = **0 ligne**, 167 paires FR|EN, 0 ancre morte, 21 liens WhatsApp **vers son numéro à lui**
(699 25 28 74), JSON-LD `Optician` décodé **sans** note ni réseau inventés.

- ⚠️ **Ne pas envoyer `amk-cm.vercel.app/univers/`** : l'aperçu est bâti dans le dépôt, **pas déployé** → 404.
  Tu déploies, tu me donnes l'URL exacte, je la grave — jamais l'inverse.
- **Si ton WhatsApp refuse une pièce jointe de 928 Ko** : la version **sobre est déjà générée**,
  `demos/concept-univers-optique-v1-sobre.html` (**84 Ko**, zéro visuel, audit 0 finding aussi). Elle dit
  elle-même, en FR et EN, que les photos du cabinet prendront la place à la mise en ligne. Régénérer :
  `python3 demos/build_univers_optique.py --sobre`.
- Le fichier **corrige mon message de 17:50 sans le dire au client** : il prétendait « absent du web ».
  C'est faux, et la page le remplace par le constat vrai (section *Le dossier*) : **sa seule page vivante est
  un miroir tenu par un tiers, avec le champ « site web » vide.** On ne publie jamais une correction du
  client ; on lui soumet des faits. Le reproche, si reproche il y a, s'écrit dans nos fichiers, pas dans son
  fil (voir `design/LESSONS.md`, 21/09 19:40 et 23:10).

---

## ② ENSUITE le texte — DEUX VERSIONS, roi, choisis la tienne

### Version A — **on livre la preuve d'abord** (le prix est déjà posé, on ne le répète pas)

```
Bonjour, comme promis hier soir : votre aperçu est prêt, en pièce jointe (ouvrez-le sur votre téléphone).
On n'a pas fait deux recherches. On a lu votre fiche Google (3,3/5, 6 avis, champ « site web » vide), votre annuaire Maligah, et votre ancien site dans les archives — il s'est arrêté en janvier 2024.
Résultat : ce n'est pas que vous êtes absent du web, c'est que votre seule page vivante est celle d'un autre.
Six points sont à trancher par vous avant de publier : ils sont écrits dans la page, section « À trancher ».
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi ces lignes :** la première tient la promesse à l'heure dite ; la deuxième répond à son objection
éventuelle (« une agence de plus ») par le **nombre de sources**, pas par un adjectif ; la troisième
remplace mon erreur du 17:50 par un constat plus fort et vérifiable ; la quatrième lui rend la main — c'est
son dossier, pas notre vitrine. Cinq lignes, une idée par ligne, aucune question fermée.

### Version B — **s'il enchaîne sur le prix ou négocie**

```
Le prix reste celui dit hier : 100 000 FCFA la page complète en français et en anglais, mise en ligne en 3 à 5 jours, 50 000 pour commencer et 50 000 à la mise en ligne. Rien n'est dû avant votre accord écrit.
Pour tenir ce prix, on reprend ce qui existe déjà : vos horaires Google, votre note, vos six questions — pas de shooting, pas de formulaire de rendez-vous, pas de page par quartier.
Si le budget est trop haut, on coupe dans le contenu, jamais dans le prix.
Dites-moi juste « on y va », et je commence par votre fiche Google : c'est elle qui vous amène des clients aujourd'hui.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**La ligne de conduite, gravée :** s'il marchande, on **échange du périmètre ou du délai** (enlever la page
« formations », ne pas faire les six questions en ligne, livrer en 7 jours), on **ne baisse jamais les
100 000 FCFA**. Et **aucune des deux versions ne promet une page Facebook** : nous n'avons trouvé **aucune**
page rattachable à son nom — celle de 508 likes est un homonyme (« Global trade invesment »). S'il en tient
une, on la relie, on ne la crée pas sans qu'il le demande.

---

## ③ CE QUE LA MAQUETTE CONTIENT, ET QUI FAIT LA DIFFÉRENCE

| Bloc | Ce qu'il voit | D'où ça vient |
|---|---|---|
| Couverture « fiche d'établissement » | 8 champs, dont 3 en rouge : site hors ligne, 6 avis à 3,3, page Facebook « à confirmer » | Maligah · Google Maps · DNS du 21/09 |
| **Le dossier — 6 constatations** | chacune en vis-à-vis : *ce que j'ai lu* (avec l'URL et la date) ↔ *la reprise* | fiche Google, homonyme de Moselle, domaine mort, archive du 02/11/2023 (le nom « Gweleo » resté dans son texte, 3 cartes sur la même URL, la bannière « 15 % »), annuaire à champs vides, réseaux introuvables |
| Le cabinet — 10 actes | liste à filets, chaque ligne ouvre un WhatsApp **déjà écrit** | son annonce de 2022 + la dernière copie de son site |
| Prothèses oculaires + verres de sécurité | le poste qu'aucun voisin ne peut disputer | son annonce de 2022 (support retiré, texte indexé) |
| Rendez-vous | ses horaires Google, tapotables ; **aucun formulaire** | fiche Google, identiques à l'annonce 2022 |
| **Vos six avis : 3,3 / 5** | la note affichée, pas cachée, avec ce qui la fait bouger | fiche Google — et **aucun balisage `aggregateRating`** tant que la base est mince |
| Trois visuels | étiquetés « Rendu de concept — votre photo le remplacera », en FR **et** EN | générés, parce qu'il n'a pas de photos exploitables — jamais présentés comme son magasin |
| **Six questions à trancher par lui** | le fixe à deux versions, le « 15 % », l'ordre des trois lignes, le nom du titulaire, l'e-mail unique, l'accès à sa fiche Google | contradictions **entre ses propres supports** : on les lui soumet, on ne les tranche pas |

---

## ④ CE QUE J'AI FAUX À NE PAS REFAIRE

1. J'ai écrit « absent du web » **sans avoir vérifié**. Cinq autres lignes de ce fil sont exactes parce
   qu'elles ont été lues ; celle-là venait d'une impression. Depuis : **une affirmation sur la présence en
   ligne d'un prospect porte une source et une date, ou ne part pas.**
2. J'ai failli construire une « refonte » de son site : il n'y a **rien à moderniser**, le domaine ne répond
   pas. Le bon objet est une **reprise** — d'où l'archétype du dossier, pas de la vitrine.
3. La page **ne montre aucune donnée que je n'aie pas lue** : pas de prix, pas de témoignage, pas d'assureur,
   pas de « 15 % », pas de page Facebook. Et le numéro fixe en deux versions n'est **pas affiché** du tout :
   il est posé comme question.

---

## ⑤ DÈS QU'IL RÉPOND

- **« C'est joli, combien pour tout ? »** → version B. Stage déjà en `closing` ; on ne bouge plus.
- **« J'ai une page Facebook, la voilà »** → on la **relie** (en-tête, *Nous joindre*, `sameAs`), on régénère,
  on re-audit, on renvoie le fichier. Puis on remonte la question de la fiche Google.
- **Il répond aux six questions** → je mets à jour `demos/univers_optique_content.py`, `python3
  demos/univers_optique_content.py && python3 demos/build_univers_optique.py`, et je réécris cette feuille.
  **Le CSV ne se corrige jamais à la main** — il est une sortie, tout ce qu'on y tape meurt au premier
  `rebuild.sh` (c'est exactement comme ça qu'on a perdu l'état de Le Cristallin ce soir, à 22:55).
- **Après l'envoi** : dis-le moi, et je pose dans `crm.py` (`EVENING_2109`) la date et l'heure réelles dans
  `last_send_state` + `Conversation`. **Il n'y a pas de colonne `preview_sent`** — ce serait une colonne
  inventée, donc une donnée qui meurt au premier `rebuild.sh` (c'est exactement comme ça qu'on a perdu
  l'état de Le Cristallin à 22:55). Sans ton mot, rien n'est coché : déclarer un envoi à ta place vaut un
  faux rendez-vous.
