# Video 16 — "New VIRAL Carousels With Motion Graphics 0$ Turned It Into a Skill (COPY ME)" — Jad M.H | AI Automation

URL: https://youtu.be/hZ_w1d0uYT4 · Batch: `research/youtube-lessons/2026-10-12-batch-6/` · Date: 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: RETRIEVED IN FULL** (2/2 chunks) — `https://youtubetotranscript.com/transcript?v=hZ_w1d0uYT4`.

- **Producer:** Jad M.H | AI Automation — **5.38K subscribers** (transcript page).
- **Metadata (YouTube watch page, 2026-10-12):** uploaded **2026-10-04** · **10:51** · **82 539 vues** ·
  **1 995 likes** · catégorie People & Blogs.
- **What he is selling:** rien de payant — une **communauté Skool gratuite** (`skool.com/nextphase-5790`)
  qui livre la « skill ». Il déclare explicitement : « not sponsored, nobody paid me, I don't make a
  single dollar from the skill ». Le modèle est la construction d'audience (free skill → communauté).
- **Outils cités (description):** HyperFrames (`github.com/heygen-com/hyperframes`, open source),
  FFmpeg, ACE-Step 1.5 (`github.com/ACE-Step/ACE-Step-1.5`, musique locale, ~11 Go de disque).
  Format carousel : **1080×1350**, 1 MP4 par slide.
- **Cross-ref interne:** HyperFrames = exactement le moteur évalué et installé dans notre sandbox le
  19/09 (`research/HyperFrames-Evaluation-2026-09-19.md`, licence Apache-2.0, contournements
  `--ignore-scripts` + GSAP local documentés). La vidéo confirme un usage de production du même moteur.
- **Cross-ref vidéo 17:** même producteur, même jour d'upload, même stack. La vidéo 17 est la vidéo
  « méthode » (3 vidéos motion graphics) ; celle-ci en est l'application carousel. Les leçons ne sont
  comptées qu'une fois (voir vidéo 17 pour le détail méthode).

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | « animation, musique, sons = 0 $ » | VRAI-hors-abonnement | Il admet lui-même (vidéo 17) que l'abonnement Claude existe ; le 0 $ porte sur musique/SFX/animation (modèles locaux, pas d'API). |
| 2 | Instagram accepte des vidéos dans les carrousels | VERIFIED | Fonctionnalité réelle d'Instagram (slides vidéo en boucle). |
| 3 | « personne n'a fait de carousel 100 % motion » | VENDOR SELF-REPORT | Non vérifiable ; sa recherche YouTube n'est pas une preuve. |
| 4 | 120 BPM, chaque slide = nombre entier de mesures → boucle sans saut | VERIFIED IN-DEMO | Méthode démontrée, cohérente (boucle Instagram). |
| 5 | Les modèles vidéo IA « font fondre le texte », coûtent des crédits | PLAUSIBLE / cohérent | Même constat que le lot [39] (vidéo 11) sur les générateurs vidéo. |
| 6 | HyperFrames gratuit open source | VERIFIED | Évalué par nous le 19/09 (Apache-2.0). |
| 7 | ACE-Step 1.5 tourne sur un MacBook Air de base | VERIFIED IN-DEMO | Démontré ; ~11 Go de disque (description). |

## 3 · TOOL AUDIT

**Première question — l'orchestrateur peut-il déjà le faire ?** Oui, partiellement : HyperFrames est
**déjà installé et testé dans notre sandbox** (évaluation 19/09 : HTML/CSS/JS → MP4). Ce que la vidéo
ajoute n'est pas un outil mais une **méthode de composition** (rythme 120 BPM, mesures entières,
couches séparées, ban des défauts).

| Outil | Coût | Verdict |
|---|---|---|
| HyperFrames | Gratuit (Apache-2.0) | **DÉJÀ ÉVALUÉ** — cross-ref 19/09 ; pas de nouvelle adoption nécessaire. |
| ACE-Step 1.5 (musique locale) | Gratuit mais ~11 Go + GPU utile | **REJETÉ pour l'instant** — lourd pour le besoin actuel (posts TikTok sans musique sous la VO). |
| La « skill » Skool de Jad | Gratuit via communauté | **REJETÉE** — c'est un jeu de prompts qu'on peut écrire nous-mêmes ; passer par Skool n'ajoute rien. |

## 4 · GAP-FILLING

- **Coût de calcul absent :** un render 60 fps = des centaines de screenshots (960 pour 16 s, chiffre
  de la vidéo 17) ; la vidéo ne dit jamais combien de temps ça prend sur une machine modeste.
- **Typographie FR absente :** aucun mot sur les césures/accents français — pertinent pour nous.
- **Audio autoplay :** rien sur le comportement son coupé par défaut selon l'app/device.
- **Application Cameroun :** le format « carousel animé » est transposable à Instagram pour AMK
  (contenu build-in-public) — mais le pipeline POST-01→09 est figé (pas de changement à mi-parcours) ;
  c'est un **backlog**, pas un changement.

## 5 · INTEGRATION RECOMMENDATION

**ADOPT (discipline, backlog — addendum Lot [41] du brief TikTok) :**
1. Quand un post motion verra le jour : **120 BPM + slides en mesures entières** (boucle propre).
2. **Ban des défauts** dans tout prompt visuel (interdire explicitement les couleurs/fonts/effets par
   défaut, texte centré qui fade in) — rejoint notre protocole d'unicité.
**DO NOT ADOPT:** la skill Skool ; ACE-Step maintenant ; toute modification du pipeline en cours.

## 6 · SUMMARY BLOCK

**Core idea.** Un carousel Instagram où chaque slide est une mini-vidéo motion design synchronisée
sur une musique générée localement — Claude écrit le code (HyperFrames + FFmpeg), aucun modèle vidéo
payant. La vraie valeur est la méthode (rythme, boucles, couches, ban des défauts), pas l'outil.

**KEPT.** Discipline loop/rythme + ban des défauts → backlog motion (addendum Lot [41]).
**REJECTED.** Skill Skool, ACE-Step (poids), tout changement de pipeline.
**OPEN QUESTIONS.** Temps de render réel dans notre sandbox pour un slide 1080×1350 (non mesuré).
