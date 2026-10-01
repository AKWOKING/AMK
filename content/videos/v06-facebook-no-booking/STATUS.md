# VIDEO 06 — « Votre page Facebook ne prend pas de rendez-vous »

**Statut : PRÊTE À PUBLIER (master + voix posée + portique passé)** · 38,61 s · 1080×1920 · 30 fps · 4,1 Mo
Produite le 22/09/2026 au soir · Langue : **français** · Cible : laboratoires, cliniques, opticiens de Douala
CTA : « écrivez **APERÇU** » · **Publication : King seul** (règle du calendrier).

## Fichiers
| Fichier | Rôle |
|---|---|
| `Video_06_Facebook_No_Booking_VOIX.mp4` | **le livrable** (4,1 Mo) : master + voix off française (voix choisie par King le 22/09) |
| `Video_06_Facebook_No_Booking.mp4` | le même master, muet (3,3 Mo) — si King préfère poser sa propre voix ou un son tendance |
| `build.py` | le moteur : 6 scènes écrites en Python/PIL, rendues image par image puis montées par ffmpeg |
| `narration/n1…n6.mp3` | les six phrases, telles qu'enregistrées (4,60 / 8,02 / 7,21 / 7,08 / 3,92 / 5,88 s) |
| `narration/timeline.json` | **le montage suit la voix** : frontières de scènes mesurées sur les fichiers audio |
| `mux_voice.py` | pose la voix sur le master (garde-fou : refuse si l'écart montage/voix dépasse 0,35 s) |
| `timeline.json` | scènes + durée du master |
| `apercus/planche-v06.jpg` | planche de contrôle (6 images clés, une par plan) pour relecture rapide |
| `../../scripts/v06-facebook-no-booking.md` | le script validé (texte, minutage, ce qui n'est pas dedans) |

Départs de scènes : **[0 / 4,85 / 13,12 / 20,58 / 27,91 / 32,08]** — mesurés sur la voix, pas estimés.

## Ce que la vidéo dit (et pourquoi ce sujet)
Sur les leads trouvés pendant la passe du 22/09, **cinq sur six avaient déjà une vitrine** — une page Facebook,
parfois deux — et **aucun** n'avait de quoi prendre un rendez-vous. Le message n'est donc **pas** « vous
n'existez pas » (ce serait faux, et c'est écrit noir sur blanc dans le pipeline) mais : *votre page montre,
elle ne répond pas*.

Plans : ① la page a tout (photos, horaires, services) — ② ce qui manque : la réponse, avec des points « en
train d'écrire » qui tournent sans jamais aboutir — ③ pendant ce temps, la notification « appel manqué » part
chez le voisin — ④ une page à votre nom : horaires, examens, **rendez-vous sur WhatsApp** — ⑤ « ouvrez votre
page, comptez les questions sans réponse » — ⑥ carte finale orange « Écrivez **« APERÇU »** » + signature
AMK — Développement web · Douala.

## Contrôles passés (mesurés, pas déclarés)
- **Mouvement** : `tools/qa/audit_video_motion.py Video_06_Facebook_No_Booking_VOIX.mp4` → **« OK — mouvement
  présent dans chaque fenêtre », 0 fenêtre figée** (fenêtres de 2 s, fps de contrôle 12, seuil 1,5/255).
  C'est la barrière qui avait bloqué #4 et #4b en diaporama.
- **Son** : mesure `ebur128` sur la version finale → **-15,9 LUFS intégrés, crête réelle -1,5 dBFS** (cible
  -16 / -1,5 ; mono 48 kHz, 182 kb/s). Normalisé par `loudnorm`, pas réglé à l'oreille.
- **Cadres** : relecture image par image après rendu — **deux débordements trouvés et corrigés** (voir
  ci-dessous), puis re-rendu complet et re-vérifié.
- **Débit de rendu** : **0,27 s/image**, rendu complet en ~5 min (contre 0,50 s/image mesuré au `cProfile`)
  — le push-in de 3 % est désormais fait par `zoompan` dans ffmpeg, plus par un recadrage/redimensionnement
  des deux millions de pixels en Python.

## Ce que la relecture image par image a appris (deux pièges, tous les deux payés)
1. **Rien ne dépasse du cadre, et ça se MESURE.** La taille du titre du plan 05 était choisie sur le **nombre
   de caractères** (`< 24`), pas sur la largeur réelle des glyphes : il ne tenait qu'à 99 % de la largeur
   disponible — à un mot près, c'était « Comptez les questio… » coupé au bord droit. Corrigé par `fit_font()`
   et un `head()` qui **mesure chaque ligne et rétracte la taille** jusqu'à ce qu'elle tienne (plan 05 : 78 →
   62 ; les autres plans ne bougent pas). Le nombre de caractères n'est pas une mesure, c'est une intuition
   déguisée. Les textes de la carte du plan 03 sont mesurés de la même façon.
2. **Changer la toile invalide TOUTES les coordonnées.** Pour rendre plus vite, le rendu interne était passé
   de 1080×1920 à 900×1600 : chaque texte de bas de plan (plans 02, 04, 05) est tombé hors cadre d'un coup,
   et la signature finale avec lui — sans que le portique du mouvement, qui ne regarde que le mouvement, ne
   voie quoi que ce soit. Toile rétablie à **1080×1920** (la vitesse vient du `zoompan` ffmpeg, pas d'une
   toile plus petite), puis **re-rendu complet et relecture d'une image par plan** : `apercus/planche-v06.jpg`.
   Loi : après tout changement de moteur ou de toile, on ré-extrait des images et on les regarde.

## Trois pièges payés, écrits dans le moteur pour ne plus les repayer
1. **Les Montserrat du dépôt sont des polices VARIABLES** : sans `set_variation_by_axes`, tout sort en Thin.
   Mesuré : 1 042 pixels d'encre à l'axe 100 contre 7 435 à 800, pour le même mot.
2. **PIL ne mélange pas les translucides** : `fill=(255,255,255,30)` écrit un blanc opaque, et
   `convert("RGB")` jette l'alpha. Les étiquettes étaient blanches sur blanc. Corrigé par les helpers `veil_*`.
3. **Aucun glyphe absent du jeu de caractères** : ♥ ★ ✆ ✓ sortaient en carrés vides. Ils sont maintenant
   **dessinés** (`icon_heart`, `icon_star`, `icon_phone`, `icon_check`).

## Numéros et couleurs
Palette reprise de la série : nuit `#191E53` / `#11164D`, teal `#20C8B4`, ambre `#FCAE1C` (échantillonnés sur
les masters #3 et #4b, pas inventés). Maquette Facebook **fictive et étiquetée « EXEMPLE FICTIF »** — règle
maison : on ne met jamais la page d'un vrai prospect dans une vidéo, et aucun nom de concurrent à l'écran.

## Ce qui n'est PAS dans la vidéo (et pourquoi)
- **Aucun prix**, aucune durée promise, aucun témoignage : rien qui puisse être démenti plus tard.
- **Aucune école** : les 36 écoles ont été écartées le 22/09, la vidéo ne parle qu'aux labos, cliniques et
  opticiens — c'est le profil qui répond (11,1 % contre 2,5 %).
- **Aucune capture de prospect réel** : tout est dessiné, donc aucune autorisation à demander.

## Suite
- **Publication = King.** Créneaux libres : `content/strategy/POSTING-CALENDAR.md`.
- Sous-titres incrustés : à faire dans la version de publication si King le veut (le master en est dépourvu
  volontairement, pour ne pas figer le texte si un mot change).
- Vidéo 07 : sujet déjà choisi par les chiffres du soir → `content/pipeline/KEYWORDS-2026-09-22.md`.
- Après publication : relever vues / réponses dans `content/pipeline/ANALYTICS-LOG.md`.
