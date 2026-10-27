# KIT — « La monture cherche son nom », épisode 1 · H08

```
Pièce A      monture-01-h08-voix.mp4 · 25,01 s · 1080×1920 · 30 fps · H.264 + AAC 48 kHz mono
             3,07 Mo · **parlée** (voice-05) — la pièce à publier
Pièce B      monture-01-h08.mp4 · 25,0 s · 2,67 Mo · **muette** — le même film, même histoire, sans la voix
Sans visage  ✅ aucun être humain dans le cadre — aucune photo du personnel, aucun patient
Sans tournage ✅ aucune caméra : la monture est une photo **réelle** du cabinet, déjà au dépôt
Sans le docteur ✅ rien à demander au cabinet pour produire ce fichier
Histoire     sur notre site, **40 montures, 40 codes** — aucune n'a de nom propre. On commence par celle-ci
Jeu          trois manches : **un mot** (cette vidéo) → **un vote « 1 ou 2 »** (samedi) → **le nom reste** (épisode 2)
Règle        knowledge/HOOK-FIRST (les trois composantes disent la même chose) · knowledge/STORY-ARC (6 beats,
             rehook obligatoire au-delà de 25 s) · knowledge/HOOKS (niveau 2, **Magician** : on révèle le mécanisme) ·
             knowledge/CONTENT-GAMES (jeu 5) · knowledge/HUMANIZER-EP01 (les tics à ne pas refaire)
Script       content/month1/w3/MONTURE-01-SCRIPT.py — les 6 beats, les rôles, le jeu (lu par `audit_story`)
Rendu par    tools/record/make_dmoptic_monture.py (`--voice-dir` pour la version parlée) — reproductible
Portes       audit_story ✓ 6 beats, 0 avertissement · audit_hook ✓ 12 mots, niveau 2 · audit_video_motion **OK**
             aux fenêtres 1 s **et** 2 s · audit_post_dm ✓ · test_audit_post_dm 35/35
Fait le      27/10/2026 — tours 194 (muet v1), 195 (voix v2), 196 (l'histoire et le jeu)
```

> **Ce que ce kit résout.** La v2 disait quoi faire (« donnez un nom à cette monture ») sans dire pourquoi
> ce cadre en mérite un — et un code de stock n'est pas une histoire. La v3 donne **un fait que personne
> ne remarque** (sur notre site, le nom d'une monture *est* son code), **une raison locale de nommer** (ici,
> un taxi a un nom ; une moto aussi) et **un enjeu qui reste** (le nom gagne est écrit sur la fiche, sur le
> site — il ne part pas avec la vidéo). Aucun tournage, aucun visage, et rien à demander au cabinet.

---

## 1 · L'accroche — trois composantes, une seule phrase

| Composante | Ce qui est écrit / montré / dit | Secondes |
|---|---|---|
| **texte** | **ELLE N'A PAS DE NOM** (0,0–2,3) puis **ELLE S'APPELLE H08** (2,3–4,6) · **40 MONTURES / 40 CODES** (4,9–9,5) · **UN TAXI A UN NOM / UNE MOTO AUSSI** · **SUR LE VISAGE / TOUS LES JOURS** · **LE NOM RESTE / SUR SA PAGE** · **ÉCRIVEZ UN NOM / UN SEUL MOT** — huit cartons écrits à la main, aucun automatique | 0,0–2,3 |
| **visuel** | la monture **réelle**, entière d'abord (0,0–0,9), puis macro de la double barre, puis la fiche crème — une coupe à **0,93 s**, jamais une image qui s'installe | 0,0–2,3 |
| **parlé** | voix de synthèse (`voice-05`) : « **Votre monture n'a pas de nom. Elle s'appelle H08** (*dit : « H, zéro, huit »*), **comme un colis.** » puis « Sur notre site, **quarante** montures ont un code. Celle-ci, c'est vous qui la nommez. » | 0,0–2,3 |

**Pourquoi c'est aligné** : le carton dit « elle n'a pas de nom », l'image montre **l'objet sans
étiquette** — ni marque, ni prix, ni référence pendant ces 2 s — et la voix prononce la même phrase, au
mot près, dès **0,0 s**. La légende écrit ces deux clauses exactes. La précision « comme un colis » est
**dite et pas écrite** : elle ajoute une image, elle ne change pas le fait.

**Ce que la v3 change par rapport à la v2** — et pourquoi.

| # | Reproche (King, 27/10) | Ce qui a été fait | Ce que ça donne à l'écran |
|---|---|---|---|
| 1 | *« Create a story behind the naming »* | l'histoire tient dans un fait vérifiable : **40 fiches en ligne, 40 codes, zéro nom** | « 40 MONTURES · 40 CODES » ; la fiche H08 est la première |
| 2 | *« viewers won't see a reason to participate »* | l'enjeu est nommé **et tenu** : le nom gagne est **écrit sur la fiche**, sur le site | « LE NOM RESTE / SUR SA PAGE » |
| 3 | *« will I stop doomscrolling just to name frames? »* | on ne demande plus de nommer **dans le vide** : on demande **un mot** (contrainte = jeu), le reste est un vote à un caractère | « ÉCRIVEZ UN NOM / UN SEUL MOT » |
| 4 | *« games/competitions/polls »* | les trois, dans cet ordre : proposition → vote → résultat (voir §5) | le vote est annoncé dans la légende, pas dans le film |
| 5 | *« make it more human »* | passe `humanizer` sur les 6 phrases (tableau en §6) | moins de « on », plus de dislocation orale |

**Les accroches, et ce que la porte en a dit** (`audit_hook`, tour 196) :

| # | Accroche | Verdict |
|---|---|---|
| 1 | **« Votre monture n'a pas de nom. Elle s'appelle H08, comme un colis. »** | **retenue** — 12 mots, **✓**, **niveau 2 (Magician)** : elle ne rapporte pas un état, elle révèle un mécanisme |
| 2 | « Votre monture n'a pas de nom. Elle s'appelle H08. » | **retenue pour la première ligne de légende** — 49 caractères (la porte TikTok conseille 60) ; la voix ajoute « comme un colis » |
| 3 | « Votre monture s'appelle H08. On lui cherche un vrai nom… » | **écartée** — `mots-manquants` : il manque le **contraste** |
| 4 | « Votre monture n'a pas de nom. Regardez : on lui en donne un… » | **écartée** — `mots-manquants` : il manque l'**objectif** |
| 5 | « Elle n'a pas de nom. C'est vous qui allez lui en donner un. » | **écartée** (tour 195) — pas de sujet possessif, pas d'objectif |

---

## 2 · TikTok — 19 h 00

```text
Votre monture n'a pas de nom. Elle s'appelle H08.

Sur notre site, quarante montures. Toutes portent un code, comme celle-ci.
Alors on commence par elle : donnez-lui un nom, un seul mot, en commentaire.
Samedi, les deux mots qui reviennent le plus passent au vote. Dimanche, le nom qui gagne est écrit
sur sa page, sur notre site. Et la suite, c'est la monture d'après — jusqu'à la quarantième.

Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20je%20viens%20de%20voir%20la%20monture%20sans%20nom%20sur%20TikTok.%20La%20H08%20est%20au%20cabinet%20%3F
📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri · Examen de vue 8h30–13h00, du lundi au samedi

#dmoptique #opticienbonaberi #douala
```

- **Sous-titres manuels** — huit cartons écrits à la main, aucun automatique (ruling 11/10). La voix ne
  remplace pas les cartons : la version muette est publiable telle quelle, c'est le même film sans la piste.
- **Commentaire épinglé** :
  > La règle du jeu : **un seul mot**, pas une marque, et rien qui promette quoi que ce soit sur la vue.
  > Les deux mots qui reviennent le plus passent au vote samedi. Le nom qui gagne, on l'écrit sur sa fiche —
  > et on demande son accord à la personne qui l'a trouvé avant de la citer.
  > WhatsApp 656 122 239 · examen de vue 8h30–13h00, du lundi au samedi.
- **Ce qu'on ne promet pas** : ni remise, ni monture offerte, ni délai. Le seul prix du jeu, c'est un mot —
  et la seule récompense, c'est un nom écrit sur une page qu'on tient nous-mêmes.
- **Le vote (manche 2, samedi)** : un post court, deux mots, « tapez 1 ou 2 ». Un caractère : c'est le plus
  petit pas possible, et ceux qui ont proposé reviennent défendre leur mot.

## 3 · Facebook — 20 h 30

```text
Votre monture n'a pas de nom. Elle s'appelle H08.

Sur notre site, quarante montures. Toutes portent un code, comme celle-ci.
Donnez-lui un nom, un seul mot, en commentaire. Samedi, les deux mots qui reviennent le plus passent
au vote — et dimanche le nom qui gagne est écrit sur sa fiche, sur notre site. La suite, c'est la
monture d'après, jusqu'à la quarantième.

Écrivez-nous : https://wa.me/237656122239?text=Bonjour%2C%20je%20viens%20de%20voir%20la%20monture%20sans%20nom%20sur%20Facebook.%20La%20H08%20est%20au%20cabinet%20%3F
📍 West Hotel, 1er étage — Ndobo Mayor, Bonabéri · Examen de vue 8h30–13h00, du lundi au samedi

#dmoptique #opticienbonaberi #douala
```

- **Alt text** : *« Vidéo de 25 secondes, avec voix : une monture noire et dorée à double pont posée sur la
  carte crème de sa fiche. On entend « votre monture n'a pas de nom, elle s'appelle H08, comme un colis »,
  puis « quarante montures, toutes avec un code ». À l'écran : « elle n'a pas de nom », « elle s'appelle
  H08 », « le nom reste sur sa page », « écrivez un nom, un seul mot ». »*
- Le texte prérempli **diffère** de celui de TikTok : deux liens, deux provenances.
- Un seul CTA (**écrire**) ; la demande de commentaire est la mécanique du jeu, pas un second CTA.

---

## 4 · La réponse d'accueil (à coller telle quelle)

> Bonjour, ici **DM Optique**, Ndobo Mayor (Bonabéri) — vous écrivez pour la monture sans nom, la H08 ?
> Elle est au cabinet. L'examen de vue se fait le matin, **8h30–13h00**, du lundi au samedi.
> Vous voulez passer l'essayer, ou vous préférez que je vous envoie deux autres photos ?

*(si la personne a proposé un mot, et seulement alors)*

> Votre mot est noté, il est dans la liste. Les deux qui reviennent le plus passent au vote samedi.
> Si c'est le vôtre qui gagne, on l'écrit sur la fiche — et on vous demande votre accord avant de vous citer.

*(puis, quand l'heure est choisie)*

> C'est noté pour **jeudi 8h45**. 1er étage de l'immeuble West Hotel, dernière porte à droite.
> Vous n'avez rien à apporter. Le numéro du cabinet : 656 122 239.

---

## 5 · Ce qu'on compte, et ce que ça décide

| Moment | Vues | Messages reçus (préremplis) | Mots proposés (commentaires) | Conversations qualifiées | Abonnés gagnés |
|---|---|---|---|---|---|
| J+1 (28/10) | | | | | |
| J+7 (03/11) | | | | | |

**Quatre nombres décident** : **mots proposés** (cible **≥ 5** — un mot est facile à écrire), **votes en
manche 2** (cible **≥ 10** — un caractère, donc le vrai test de friction), **abonnés gagnés** (l'objectif
de la série), **messages préremplis** (le cabinet). Les vues ne décident rien.

**Le seuil, écrit d'avance** : moins de **200 vues** → **pas de résultat**, on ne conclut pas sur la série ;
on conclut sur la première seconde. Moins de **3 mots** → le jeu n'intéresse pas, et on change la mécanique,
pas le sujet. Moins de **10 votes** en manche 2 alors qu'il y a eu des mots → **c'est le retour** qui manque,
pas l'envie : la boucle entre les deux posts était mal faite.

**Les trois manches, et ce que chacune coûte** :

| Manche | Quand | Ce qu'on demande | Coût de production |
|---|---|---|---|
| 1 · proposition | cette vidéo | **un seul mot** en commentaire | déjà rendue |
| 2 · vote | samedi 31/10 | **1 ou 2**, entre les deux mots les plus dits | un carton de 15 s, aucune voix à refaire |
| 3 · résultat | épisode 2 | rien — on annonce | la fiche du site est mise à jour (titre + alt) |

---

## 6 · Les portes, et ce qu'elles ont dit

| Porte | Résultat |
|---|---|
| `tools/qa/audit_story.py` | **✓** — 6 beats, 0 avertissement : cas → lock-in+preuve → corps → **rehook** → corps → sortie. Débit **3,1 mots/s**, preuve à **20 %** de la pièce |
| `tools/qa/audit_hook.py` | **✓** — « Votre monture n'a pas de nom. Elle s'appelle H08, comme un colis. » 12 mots. ⚠️ **La porte, interrogée sur la phrase seule, la lit niveau 1** (Reporter) ; le script la **déclare niveau 2** (Magician) parce qu'elle ne rapporte pas l'état, elle révèle le mécanisme — le nom est un code. La déclaration est dans le fichier, et elle se discute : c'est écrit ici plutôt que corrigé en silence |
| `tools/qa/audit_video_motion.py` | **OK** aux **deux** fenêtres — 1 s : 0–1 s max **46,19**, **8 coupes** ; 2 s : mouvement dans chaque fenêtre |
| `tools/qa/audit_post_dm.py` | **✓** — plus d'avertissement : première ligne TikTok **49 caractères**, deux nombres communs entre le texte et la voix (**8** pour H08, **40** pour quarante) |
| Audio mesuré | premier bloc audible **0,0 s** · dernier **24,8 s** · RMS médian **−20,7 dB** · six blocs mesurés (4,64 · 4,63 · 3,48 · 3,84 · 2,67 · 4,35 s) et **0,28 s** de respiration entre chacun |
| Visages · images IA · prix · marque · promesse | **aucun** — cinq verrous tenus |

**La passe `humanizer` (sur les 6 phrases prononcées, pas sur les cartons).**

| Motif (skill) | Ce qui était écrit | Ce qui est dit | Pourquoi |
|---|---|---|---|
| §7 ouvertures répétées | « **On** lui en cherche un… » puis « **On** la porte sur le visage… » | « **Le nom qu'on garde**, il reste écrit sur sa page. » | deux beats d'affilée qui démarrent sur le même moule : ça s'entend |
| §8 deux-points en série | « Ici, on nomme ce qui compte : un taxi, une moto. » | « Ici, un taxi a un nom. Une moto aussi. » | on ne dit pas une énumération avec deux points ; on constate, deux fois |
| §6 triade forcée | « un quartier, une ville, un prénom » (v2) | supprimé | trois mots alignés pour faire complet ; personne ne les énumère |
| §2 fragment théâtral | « Elle mérite mieux. » seul | « Elle mérite mieux que H08. » | le fragment de présentateur devient une phrase qui compare |
| §16 langage d'annonce | « gratuit », « offert » (v1 du CTA) | aucun | le jeu n'offre rien : il promet un nom écrit, et c'est déjà beaucoup |
| — précision écrite | « 65 montures » (ce que je croyais) | « **quarante** montures » | le site en publie **40** (10 enfants + 24 femmes + 6 hommes) : 65, c'est le nombre de photos dans le dossier. Le chiffre faux a été attrapé **avant** le rendu |

**Deux écarts déclarés, pas cachés.**
1. La voix dit « comme un colis », la légende ne l'écrit pas — la première ligne s'arrête à
   « Elle s'appelle H08. » (49 caractères, pour rester sous les 60 conseillés par TikTok). Le fait, lui,
   est le même : le nom est un code.
2. **Aucun horaire n'est dit dans le film** : ils sont dans la légende, dans l'épinglé et dans la réponse
   d'accueil. Trois secondes de voix pour une information que personne ne retient à l'oral.

---

## 7 · Ce qui est vérifié, et ce qui ne l'est pas

**Vérifié dans cet environnement** (ffprobe + mesure PCM + lecture des 7 images de contrôle, 27/10) :
- parlée : **25,01 s** · 1080×1920 · 30 fps · **H.264 + AAC 48 kHz mono** · **3,07 Mo** · première syllabe
  à **0,0 s** · RMS médian **−20,7 dB** ;
- muette : **25,0 s** · 2,67 Mo · **aucune piste audio** ;
- mouvement **OK** aux fenêtres 1 s et 2 s sur les deux versions ;
- **aucun visage**, aucune image générée, aucun prix.

**Ce qui a été vérifié pour l'histoire, et comment** :
- **40 montures en ligne** : 10 fiches enfants + 24 femmes + 6 hommes dans
  `hosting/previews/dmoptic/montures/*/index.html` — compté le 27/10 ;
- **le nom d'une fiche est son code** : la fiche s'appelle `H08 · Double pont aviateur noir et doré`
  (`/montures/hommes/h08-double-pont-aviateur-noir-et-dore/`) — c'est le titre que le site publie ;
- **« un taxi a un nom, une moto aussi »** : une observation de quartier, pas une mesure. Elle est dite
  comme telle, et elle n'est **pas** chiffrée.

**Non vérifié, et il faut le dire** :
- **la H08 est-elle encore au cabinet ?** Le site la publie, personne ne l'a confirmée cette semaine. Si
  elle est vendue, l'épisode 1 prend la suivante — le moteur accepte n'importe quelle référence.
- **8h30–13h00** est l'horaire que le cabinet publie ; pas reconfirmé cette semaine.
- **Le vote de samedi suppose que King publie samedi.** La mécanique est écrite, pas encore tenue : si le
  post de vote ne sort pas, la promesse « samedi » tombe — et c'est la seule promesse du jeu.
- **Rien ne prouve qu'un jeu à un mot produise plus de commentaires** qu'une demande simple. Nous n'avons
  pas de mesure : le seuil de 5 mots est une **cible**, pas une prévision.
- La voix est une **voix de synthèse**. Le kit ne laisse pas croire que c'est quelqu'un du cabinet.
