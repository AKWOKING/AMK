# KIT — « La monture cherche son nom », épisode 1 · H08

```
Pièce A      monture-01-h08-voix.mp4 · 19,87 s · 1080×1920 · 30 fps · H.264 + AAC 48 kHz mono
             2,30 Mo · **parlée** (voice-05) — la pièce à publier
Pièce B      monture-01-h08.mp4 · 14,20 s · 1,35 Mo · **muette** — le même film sans voix, gardé au dépôt
Sans visage  ✅ aucun être humain dans le cadre — aucune photo du personnel, aucun patient
Sans tournage ✅ aucune caméra : la monture est une photo **réelle** du cabinet, déjà au dépôt
Sans le docteur ✅ rien à demander au cabinet pour produire ce fichier
Règle        knowledge/HOOK-FIRST-2026-10-27.md (texte > visuel > parlé : les trois disent la même chose) ·
             knowledge/LEAD-MAGNETS-2026-10-27.md (boucle ouverte, conversion par vue) ·
             clients/dm-optic/content/IDEES-ABONNES-2026-10-27.md (IDEA-01)
Rendu par    tools/record/make_dmoptic_monture.py (muet) et `--voice-dir` (parlé) — reproductible
Portes       audit_video_motion : OK aux fenêtres 1 s **et** 2 s · audit_hook : ✓ · audit_post_dm : ✓
Fait le      27/10/2026 — tour 194 (muet) et tour 195 (parlé)
```

> **Ce que ce kit résout.** C'est la seule des deux séries d'abonnés qui ne demande **ni le docteur, ni un
> visage, ni une caméra, ni un tournage**. Tout est déjà au dépôt : une photo de monture prise au cabinet
> et la référence que le site publie. Le film se refait d'une commande, et un épisode coûte **45 s de
> rendu** — pas une demi-journée de plateau. Depuis le 27/10 (tour 195), il **parle** : la voix est une
> voix de synthèse enregistrée beat par beat, jamais un prompt recollé sur un minutage. Rien n'a été
> tourné, et le docteur n'a toujours rien à faire.

---

## 1 · L'accroche — trois composantes, une seule phrase

| Composante | Ce qui est écrit / montré / dit | Secondes |
|---|---|---|
| **texte** | **ELLE N'A PAS DE NOM** (0,0–2,2) puis **H08 · DOUBLE PONT** (2,2–4,0) puis **AU CABINET / À BONABÉRI**, puis **UN QUARTIER · UNE VILLE · UN PRÉNOM** (4,0–9,0) et au carton final **DEMAIN : LA DEUXIÈME** — huit cartons écrits à la main, jamais d'automatique | 0,0–2,2 |
| **visuel** | la monture réelle **en macro**, cadrée sur la double barre ; le cadre glisse en continu **et** la première seconde porte une poussée de 0,45 s | 0,0–2,2 |
| **parlé** | voix de synthèse (`voice-05`) : « **Votre monture n'a pas de nom. Regardez : elle devient la vôtre.** » puis « **H08**, double pont. Elle est au cabinet, à Bonabéri. » puis « **Un** quartier, **une** ville, un prénom : choisissez. » — la voix ne se comprime jamais, le montage se cale sur elle | 0,0–2,2 |

**Pourquoi c'est aligné** : le texte dit « elle n'a pas de nom », l'image montre **l'objet sans étiquette**
— ni marque, ni prix, ni référence à l'écran pendant ces 2 s — et la voix prononce **exactement** la phrase
écrite en légende, au mot près, dès **0,0 s** — c'est cette phrase-là qui a passé `audit_hook`. Trois couches, une phrase. Rien à interpréter.

**Ce que la voix a changé dans le montage.** Le film n'est plus calé sur un minutage écrit à la main : les
cinq blocs sont mesurés (4,23 · 3,72 · 6,70 · 1,99 · 2,12 s) et le plan se cale dessus, avec **0,28 s de
respiration** entre deux blocs. C'est la règle de `HOOK-FIRST` : on ne comprime pas une accroche pour la
faire entrer dans une durée — on allonge l'image de 5,7 s.

**Les accroches, et ce que la porte en a dit** (`audit_hook`, tour 195) :

| # | Accroche | Verdict |
|---|---|---|
| 1 | **« Votre monture n'a pas de nom. Regardez : elle devient la vôtre. »** | **retenue** — 12 mots, **✓ niveau 1**, deux réserves assumées (`sans-intrigue`, `niveau-1`). C'est **mot pour mot** ce que la voix prononce et ce que la légende écrit |
| 2 | « Votre monture n'a pas de nom. Celle-ci devient la vôtre demain. » | **écartée** — `mots-manquants` : il manque l'**action** (« regardez ») ; le contraste ne suffit pas |
| 3 | « Elle n'a pas de nom. C'est vous qui allez lui en donner un. » | **écartée** — `mots-manquants` : pas de sujet possessif, pas d'objectif |
| 4 | « Regardez cette monture… » / « Cette monture n'a pas de nom… » | **écartées** — `mots-manquants` : « regardez » seul ne dit pas à qui l'on parle |
| 5 | **ELLE N'A PAS DE NOM** (le carton seul) | **insuffisant seul** — la porte ne voit pas le carton : c'est la **phrase de légende** qui porte les quatre mots. Le carton reste ce qui est **à l'écran** |

---

## 2 · TikTok — 19 h 00

```text
Votre monture n'a pas de nom. Regardez : elle devient la vôtre.

H08 · double pont, aviateur, noir et doré. Elle est au cabinet, à Bonabéri.
Un quartier, une ville, un prénom : écrivez-le en commentaire. Le cabinet choisit — et demain,
la deuxième arrive avec le nom qu'il aura retenu.

Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20je%20viens%20de%20voir%20la%20monture%20sans%20nom%20sur%20TikTok.%20La%20H08%20est%20au%20cabinet%20%3F
📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri · Examen de vue 8h30–13h00, du lundi au samedi

#dmoptique #opticienbonaberi #douala
```

- **Sous-titres manuels** — 8 cartons écrits à la main, **aucun automatique** (ruling 11/10). La voix ne
  remplace pas les cartons : 85 % des vues arrivent son coupé, et la version muette reste publiable telle
  quelle — c'est le même film, sans la piste audio.
- **Commentaire épinglé** :
  > La règle du jeu : un nom par personne, en commentaire. Un quartier, une ville, un prénom — pas un nom de
  > marque, et rien qui promette quoi que ce soit sur la vue. Le cabinet choisit demain, et le nom retenu
  > s'affichera dans la deuxième.
  > WhatsApp 656 122 239 · examen de vue 8h30–13h00, du lundi au samedi.
- **La boucle est dans la vidéo** (« DEMAIN · LA DEUXIÈME ») **et** dans la légende : c'est la seule chose
  qui peut transformer une vue en abonné.
- **Ce que la voix dit, au mot près** (à ne pas paraphraser dans un commentaire) : « Votre monture n'a pas
  de nom. Regardez : elle devient la vôtre. » / « H08, double pont. Elle est au cabinet, à Bonabéri. » /
  « Un quartier, une ville, un prénom : choisissez. » / « Écrivez son nom. Demain, la deuxième. » /
  « DM Optique, Ndobo Mayor. »

---

## 3 · Facebook — 20 h 30

```text
Votre monture n'a pas de nom. Regardez : elle devient la vôtre.

H08 · double pont, aviateur, noir et doré. Elle est au cabinet, à Bonabéri — photographiée là, pas en studio.
Un quartier, une ville, un prénom : écrivez-le en commentaire. Le cabinet choisit, et demain la deuxième
arrive.

Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20je%20viens%20de%20voir%20la%20monture%20sans%20nom%20sur%20Facebook.%20La%20H08%20est%20au%20cabinet%20%3F
📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri · Examen de vue 8h30–13h00, du lundi au samedi

#dmoptique #opticienbonaberi #douala
```

- **Alt text** : *« Vidéo de 20 secondes, avec voix : une monture noire et dorée à double pont, photographiée
  au cabinet. On entend « votre monture n'a pas de nom », puis la référence H08 et le lieu. À l'écran :
  « elle n'a pas de nom », puis « demain, la deuxième ». »*
- Le texte prérempli **diffère** de celui de TikTok : deux liens, deux provenances.
- Un seul CTA (**écrire**) ; la demande de commentaire est une mécanique de série, pas un second CTA.

---

## 4 · La réponse d'accueil (à coller telle quelle)

> Bonjour, ici **DM Optique**, Ndobo Mayor (Bonabéri) — vous écrivez pour la monture sans nom, la H08 ?
> Elle est au cabinet. L'examen de vue se fait le matin, **8h30–13h00**, du lundi au samedi.
> Vous voulez passer l'essayer, ou vous préférez que je vous envoie deux autres photos ?

*(puis, quand l'heure est choisie)*

> C'est noté pour **jeudi 8h45**. 1er étage de l'immeuble West Hotel, dernière porte à droite.
> Vous n'avez rien à apporter. Le numéro du cabinet : 656 122 239.

---

## 5 · Ce qu'on compte, et ce que ça décide

| Moment | Vues | Messages reçus (préremplis) | Commentaires (noms proposés) | Conversations qualifiées | Abonnés gagnés |
|---|---|---|---|---|---|
| J+1 (28/10) | | | | | |
| J+7 (03/11) | | | | | |

**Quatre nombres décident** : commentaires (un nom est facile à écrire — cible **≥ 5**), abonnés gagnés
(c'est l'objectif de la série), messages préremplis (le cabinet), et **les deux premières secondes** — la
seule chose que l'on compare à la référence du 22/10 (**22 %** de rétention, arrêt à `0:01`, `ANALYSE-POST-1`
§7). Les vues ne décident rien.

**Le seuil, écrit d'avance** : moins de **200 vues** → **pas de résultat**, on ne conclut pas sur la série ;
on conclut sur la première seconde. Moins de **3 commentaires** → le nom n'est pas la bonne mécanique
d'interaction, et on change la mécanique, pas le sujet.

**Ce que la voix doit apporter, et comment on le saura** : rien ne prouve encore qu'une voix change quoi
que ce soit sur nos vues — nous n'en avons jamais publié. La version muette et la version parlée sont donc
**deux pièces séparées**, et si les deux sortent, elles sortent à **des jours différents** : le même film
avec et sans voix, c'est deux fois la même idée, et un compte qui se répète perd plus qu'il ne gagne.

---

## 6 · Les portes, et ce qu'elles ont dit

| Porte | Résultat |
|---|---|
| `tools/qa/audit_video_motion.py` | **OK — fenêtre 1 s** : 0–1 s max **9,08** (2 coupes, 2 mouvements) · 1–2 s 2,75 · 3–4 s 4,30. **OK — fenêtre 2 s** également |
| `tools/qa/audit_post_dm.py` | **✓** — plus d'avertissement `piece-muette`. Deux nombres communs entre le texte et la voix : **1** (« un quartier, une ville ») et **8** (« H08 »). Un ⚠ subsiste, assumé : la première ligne TikTok fait **63 caractères** pour 60 conseillés — c'est la phrase exacte que la voix dit, et la fin de phrase se replie sous « voir plus » |
| `tools/qa/audit_hook.py` | **✓ niveau 1** — « Votre monture n'a pas de nom. Regardez : elle devient la vôtre. » 13 mots. Deux réserves **assumées** : `sans-intrigue` (elle dit tout de suite de quoi il s'agit) et `niveau-1` (vocabulaire simple, voulu) |
| Audio mesuré | premier bloc audible à **0,0 s** · dernier à **19,7 s** · RMS médian **−19,9 dB** · **deux respirations** (1,6–2,3 s après la première phrase, 15,0–15,4 s entre b3 et b4) |
| Visages | **aucun** — vérifié sur les 6 images de contrôle |
| Images IA | **aucune** — la photo est celle du cabinet |
| Prix · marque · promesse | **aucun** — trois verrous tenus |

**Ce que la porte ne savait pas lire (corrigé, banc à 35/35).** Au premier passage, `audit_post_dm` refusait
cette pièce en `hook-desaligne` — *« 1 nombre en commun »* — alors que le texte **et** la voix disent tous
deux « H08 » et « un quartier, une ville ». Cause : l'extracteur ne voyait que `\b\d{1,4}\b`, donc **ni
`H08`** (lettre collée au chiffre), **ni `8h30`**, et il comptait comme du contenu les fenêtres de temps du
tableau. Ce n'était pas une accroche désalignée, c'était une mesure aveugle. La mesure voit maintenant les
références produit et les heures ; **le seuil n'a pas bougé** (≥ 2 nombres communs), et quatre cas ont été
ajoutés au banc — dont un qui vérifie qu'une voix qui ne reprend ni la référence ni le nom est **toujours**
refusée.

**Deux écarts déclarés, pas cachés.**
1. **Le premier jet de légende disait « Regardez : celle-ci devient la vôtre demain »** alors que la voix
   prononce « Regardez : elle devient la vôtre ». La légende a été **réécrite sur la voix** — les trois
   couches disent maintenant la même phrase au mot près. Le « demain » n'a pas disparu du film : il est au
   carton final (**DEMAIN : LA DEUXIÈME**), et c'est là qu'il se voit.
2. Les **horaires** (8h30–13h00) ne sont **pas dits** dans le film : ils sont dans la légende, dans le
   commentaire épinglé et dans la réponse d'accueil. C'est un choix — trois secondes de voix de plus pour
   une information que personne ne retient à l'oral, alors qu'elle se lit. Conséquence : la ligne
   « parlé » ne porte pas d'horaire, et le kit ne prétend pas le contraire.

## 7 · Ce qui est vérifié, et ce qui ne l'est pas

**Vérifié dans cet environnement** (ffprobe + mesure PCM, 27/10) :
- version parlée : **19,87 s** · 1080×1920 · 30 fps · **H.264 + AAC 48 kHz mono** · **2,30 Mo** · première
  syllabe à **0,0 s** · RMS médian **−19,9 dB** ;
- version muette : **14,20 s** · 1,35 Mo · **aucune piste audio** ;
- mouvement **OK** aux fenêtres 1 s et 2 s sur la version parlée (c'est elle qui bouge le plus : la poussée
  d'entrée et le décalage des deux lignes du carton) ;
- 6 images de contrôle relues à l'œil : aucun visage, aucune image générée.

**Non vérifié, et il faut le dire** :
- **la H08 est-elle encore au cabinet ?** Le site la publie (`/montures/hommes/h08-double-pont-aviateur-noir-et-dore/`),
  mais personne ne l'a confirmé cette semaine. Si elle est vendue, l'épisode 1 prend la suivante — le
  moteur accepte n'importe quelle référence, c'est une ligne à changer.
- **« un aviateur, noir et doré »** vient de la fiche du site. C'est la description du dépôt, pas une
  parole du cabinet.
- **8h30–13h00** est l'horaire que le cabinet publie ; il n'a pas été reconfirmé cette semaine.
- Le nom retenu sera **choisi par le cabinet** : rien dans ce kit ne promet qu'un nom proposé sera gardé —
  la légende dit « le cabinet choisit », et c'est volontaire.
- **La voix est une voix de synthèse** (`voice-05`). Elle est propre et posée ; elle n'est pas la voix de
  quelqu'un du cabinet, et le kit ne le laisse pas croire. Si le cabinet veut sa propre voix, il enregistre
  les cinq phrases au téléphone et le moteur reprend le même montage (`--voice-dir`).
