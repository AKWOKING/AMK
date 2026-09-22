# VIDEO 06 — « Votre page Facebook ne prend pas de rendez-vous »

**Statut : master monté et VOIX POSÉE · 38,6 s · 1080×1920 · 30 fps** · produit le 22/09/2026 au soir
Langue : **français** · Cible : laboratoires, cliniques, opticiens de Douala · CTA : « écrivez APERÇU »

## Fichiers
| Fichier | Rôle |
|---|---|
| `Video_06_Facebook_No_Booking.mp4` | master avec voix off française (voix choisie par King le 22/09) |
| `build.py` | le moteur : 6 scènes écrites en Python/PIL, rendues image par image |
| `narration/n1…n6.mp3` | les six phrases, telles qu'enregistrées |
| `narration/timeline.json` | **le montage suit la voix** : frontières de scènes mesurées sur les fichiers audio |
| `timeline.json` | scènes + durée du master |
| `../../scripts/v06-facebook-no-booking.md` | le script validé (texte, minutage, ce qui n'est pas dedans) |

## Ce que la vidéo dit (et pourquoi ce sujet)
Sur les leads trouvés pendant la passe du 22/09, **cinq sur six avaient déjà une vitrine** — une page Facebook,
parfois deux — et **aucun** n'avait de quoi prendre un rendez-vous. Huit des huit réponses de la campagne sont
venues de gens qui avaient déjà payé pour être visibles. Le message n'est donc **pas** « vous n'existez pas »
(ce serait faux) mais : *votre page montre, elle ne répond pas*.

Plans : ① la page a tout (photos, horaires, services) — ② ce qui manque : la réponse, avec des points « en
train d'écrire » qui tournent sans jamais aboutir — ③ pendant ce temps, la notification « appel manqué » part
chez le voisin — ④ une page à votre nom : horaires, examens, **rendez-vous sur WhatsApp** — ⑤ « ouvrez votre
page, comptez les questions sans réponse » — ⑥ carte finale orange « Écrivez **« APERÇU »** ».

## Le portique du mouvement est passé
`tools/qa/audit_video_motion.py` → **« OK — mouvement présent dans chaque fenêtre », 0 fenêtre figée.**
C'est la barrière qui avait bloqué #4 et #4b (diaporama) : chaque plan porte trois mouvements — push-in
global (3 % par scène), éléments qui vivent (réactions qui montent, points de saisie, notification, bouton
qui pulse) et **poussière lumineuse en dérive**, présente dans toutes les scènes.

## Trois pièges payés, écrits dans le moteur pour ne plus les repayer
1. **Les Montserrat du dépôt sont des polices VARIABLES** : sans `set_variation_by_axes`, tout sort en Thin.
   Mesuré : 1 042 pixels d'encre à l'axe 100 contre 7 435 à 800, pour le même mot. D'où la fonction
   `font(taille, graisse)` avec l'axe explicite.
2. **PIL ne mélange pas les translucides** : `fill=(255,255,255,30)` écrit un blanc opaque, et
   `convert("RGB")` jette l'alpha. Les étiquettes étaient blanches sur blanc. Corrigé par les helpers
   `veil_*` qui composent vraiment.
3. **Aucun glyphe absent du jeu de caractères** : ♥ ★ ✆ ✓ sortaient en carrés vides. Ils sont maintenant
   **dessinés** (`icon_heart`, `icon_star`, `icon_phone`, `icon_check`).

## Numéros et couleurs
Palette reprise de la série : nuit `#191E53` / `#11164D`, teal `#20C8B4`, ambre `#FCAE1C` (échantillonnés
sur les masters #3 et #4b, pas inventés). Maquette Facebook **fictive et étiquetée « EXEMPLE FICTIF »** — la
règle maison : on ne met jamais la page d'un vrai prospect dans une vidéo.

## Suite
- Publication : **King seul** (règle du calendrier). Créneaux libres : voir `content/strategy/POSTING-CALENDAR.md`.
- Sous-titres incrustés : à faire dans la version de publication (le master en est dépourvu volontairement,
  pour ne pas figer le texte si King veut changer un mot).
- Vidéo 07 : le sujet est déjà choisi par les chiffres du soir (voir `content/pipeline/KEYWORDS-2026-09-22.md`).
