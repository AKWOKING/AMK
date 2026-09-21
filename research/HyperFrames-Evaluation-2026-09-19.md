# Évaluation — `latent-spaces/brag` + HyperFrames · 19 Sep 2026

**Demandé par King :** « can this repo/tool be useful to us in anyway »
**Méthode :** lecture du dépôt **et test réel dans le bac à sable** (règle z : jamais déclarer
impossible avant d'avoir lu et essayé l'outillage). **Résultat : oui — mais pas pour ce que son README vend.**

---

## 1 · Ce que c'est vraiment (deux choses, pas une)

| | `/brag` | **HyperFrames** |
|---|---|---|
| Nature | *skill* pour agents (Claude Code, Codex, opencode…) | moteur de rendu |
| Rôle | écrit l'histoire : angle, ton, storyboard, texte de partage | transforme du **HTML/CSS/JS en vidéo** |
| Licence | **MIT** | **Apache-2.0** |
| Dépendances | Node 22+, FFmpeg, **CLI HyperFrames** | Chrome headless, FFmpeg, FFprobe |
| Entrée | le **code du projet** (pas une URL, pas de capture) | un dossier de composition HTML |
| Sortie | `brag.mp4` + `brag.jpg` + `share-copy.txt` | `renders/*.mp4` |

Le README vend `/brag`. **La valeur pour nous est dans HyperFrames.**

## 2 · Ce que j'ai vérifié en le faisant tourner (pas en le lisant)

**① Il s'installe ici — mais pas tout seul.** Deux obstacles, tous les deux réels et testés :

1. **`onnxruntime-node`** (la voix Kokoro d'HyperFrames) télécharge un binaire GPU depuis
   github.com → **« unable to verify the first certificate »**, échec d'installation.
   **Contournement : `npm install --ignore-scripts`.** On n'a pas besoin de leur voix —
   King a tranché pour `voice-00` de la plateforme.
2. **GSAP chargé depuis `cdn.jsdelivr.net`** dans le modèle par défaut → **connexion fermée**,
   rendu bloqué par `sub_timeline_script_failure`.
   **Contournement : vendre GSAP localement** — ce qui est déjà notre règle (aucun appel externe).

**② Il accepte notre moteur, pas le sien.** Trois variables d'environnement trouvées dans le code :
`HYPERFRAMES_BROWSER_PATH` · `HYPERFRAMES_FFMPEG_PATH` · `HYPERFRAMES_FFPROBE_PATH`.
On lui branche : **le Chromium de `/tmp/amk-video`**, **le FFmpeg d'`imageio-ffmpeg`** (celui
qu'on utilise déjà), et **un ffprobe récupéré par npm** (`@ffprobe-installer/ffprobe`).
→ **Aucun téléchargement de Chrome, aucun compte HeyGen, aucune clé.**

**③ Il rend, et au bon format.** MP4 de test produit et vérifié par `ffprobe` :
**1080×1920 · 30 fps · 300 images · H.264** — exactement notre format de contenu.
Il a aussi décodé et encodé 300/300 images ; le rendu est **image par image** (il demande chaque
frame au projet au lieu de dépendre de la lecture en direct), donc pas d'image perdue.

**④ Notre portique peut l'auditer.** `tools/qa/audit_video_motion.py` lit son MP4 sans modification
(il a correctement déclaré « FIGÉE » sur le modèle *blank*, qui est statique par construction).

**⑤ Script réutilisable :** `tools/video/install_hyperframes.sh` — installé et **validé depuis zéro**
(rend un MP4 de test en ~35 s). Il écrit `/tmp/amk-hf/env.sh` à sourcer.

## 3 · Pourquoi c'est intéressant pour nous — la vraie raison

**Notre faiblesse mesurée, c'est le mouvement.** §13 du `CONTENT-LESSONS` le chiffre :

| Vidéo | Fenêtres de 2 s figées |
|---|---|
| #4 (publiée) | **6 / 17** |
| #2 (publiée) | **8 / 14** |
| #3 (publiée) | **9 / 17** |

Et §12 : la **falaise de rétention est à 0:02** (18 % / 13 %). Nos vidéos sont des diaporamas,
et les diaporamas perdent le spectateur à la deuxième seconde.

**HyperFrames produit exactement ce qui nous manque : du mouvement réel, écrit en CSS/JS,
rendu image par image.** Aujourd'hui `compose.py` brûle du texte sur des captures avec PIL.
C'est le bon outil pour le mauvais niveau : HyperFrames joue dans la catégorie au-dessus
(keyframes, transitions, easing, mouvement vectoriel), et son rendu est **déterministe** —
un plan n'est jamais « presque » comme on l'a dessiné.

## 4 · Ce qui se prend de `/brag` même sans son moteur

Son **§ Creative laws** contient une règle que nous pouvons rendre *mécanique*, et deux micro-techniques :

1. **La lisibilité est un nombre.** « Every line a viewer must read holds long enough to read it —
   **short label ~0,8 s une fois posé ; une phrase ~0,3 s par mot. Fast-in, then hold —
   never fast-in, then gone.** » Nous avons la durée de chaque carte animée dans `compose.py` :
   **cette règle est vérifiable automatiquement**, et nous ne la vérifions pas.
2. **La frame 0 est la vignette.** Ils choisissent la *meilleure* image et la collent en frame 0,
   pour que la vidéo soit belle partout où elle apparaît. Notre partage se fait sur WhatsApp —
   **la vignette décide du clic.** Micro-gain, applicable à toutes les vidéos.
3. **Le patron de 15–25 s :** Hook 2–3 s → Révélation 2–4 s → 2–3 points forts 5–12 s → Chute 2–4 s.
   Notre V-05 fait 23,9 s — dans la cible, mais nous n'avions pas la structure écrite.

## 5 · Ce qui ne se prend PAS, et pourquoi

| Élément | Pourquoi non |
|---|---|
| **Les tons** (`yc-parody`, `chaotic`, `deadpan`, « fake Series A launch ») | Notre audience = propriétaires de cliniques et d'écoles à Douala/Buea. Un ton parodique détruirait la crédibilité qu'on met 5 jours à construire. **`polished` seulement.** |
| **Le principe d'entrée : lire le *code* du projet** | Notre règle 50 est **vraies pages web**. `/brag` fabrique une composition ; nous montrons le site réel. |
| **La voix Kokoro** | King a tranché : `voice-00`. On ne change pas. |
| **La musique et les SFX embarqués** | Nos vidéos portent une **narration** (§12.3) ; leur musique est un habillage de lancement produit. |
| **`publish` vers une URL HeyGen** | Ne pas mettre le travail client chez un tiers. |
| **La télémétrie** | Coupée (`hf telemetry disable`) — travail client, aucun envoi d'usage. |

## 6 · Verdict, en une phrase

> **`/brag` n'est pas notre outil. HyperFrames, en dessous, en est un** — et c'est peut-être la
> réponse à la seule faiblesse que nos propres chiffres ont identifiée : **nos vidéos ne bougent pas.**

**Ce qui est fait :** installation reproductible (`tools/video/install_hyperframes.sh`, testée),
rendu vérifié 1080×1920/30, portique compatible, télémétrie coupée.

**Ce que je propose ensuite, en microtâche (règle 71) :**
1. **Ajouter la porte de lisibilité** à `audit_video_motion.py` (0,8 s / 0,3 s par mot) — petite, mesurable, utile tout de suite.
2. **Un clip d'essai** : une vidéo réelle faite avec HyperFrames (30–40 min), passée au portique mouvement,
   comparée aux fenêtres figées de #2/#3/#4. **Si elle ne bouge pas mieux, on abandonne HyperFrames** —
   et on l'aura su pour le prix d'un essai, pas d'une migration.
3. **Ne rien migrer.** `compose.py` reste le chemin de production jusqu'à ce que l'essai (2) ait convaincu.

## 7 · Sources

- `https://github.com/latent-spaces/brag` — README, `skills/brag/SKILL.md`, licence MIT (via API GitHub)
- `https://hyperframes.heygen.com/introduction` — « turns HTML into video », rendu image par image
- `npm view hyperframes` — v0.8.50, Apache-2.0, dépendances
- **Tests locaux :** `npx hyperframes doctor` · `browser ensure/path` · `init --resolution portrait` ·
  `render` · `capture --help`. MP4 vérifié au `ffprobe` et passé à `audit_video_motion.py`.
