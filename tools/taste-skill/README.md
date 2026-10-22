# taste-skill — direction artistique anti-slop (installé le 20/10/2026, demande King)

Amont : <https://github.com/Leonxlnx/taste-skill> (MIT) · épinglé `63aba5f43b5056758b15bbe7d683da8c86a7a7ad`.
Le skill s'appelle **`design-taste-frontend`**
(« tasteskill v2 ») : direction artistique distillée d'une étude de 247 sites de galeries.

## Ce que c'est

- `SKILL.md` (530 lignes) : un « run » complet — inventaire du sujet → argument (claims/preuves) →
  tirage d'une direction par script → phrase-idée + « one live thing » → copy deck → construction →
  portique (`lint.mjs` + `inspect.mjs` navigateur réel) → critique sur captures → mouvement → rapport.
- `scripts/draw.mjs` : distribue 3 directions recherchées (composition, type, palette, blueprints de
  sections) depuis une bibliothèque locale ; `--keep palette,type` quand la marque est figée.
- `scripts/inspect.mjs` : ouvre la page en vrai navigateur (1440/768/390), mesure les règles maison
  (titres ≤ 2 lignes, marges égales, aucun vide, contrastes…) et capture des écrans.
- `scripts/assets.mjs` : recherche d'images réelles en collections ouvertes (licences commerciales).
- `references/` : copy, type, couleur, layout, imagery, motion, scenes, critique, tells, research.

## Installation (reproductible)

```bash
bash tools/taste-skill/install.sh
```

Clone épinglé dans `~/.taste-skill`, liens vers `~/.claude/skills/` et `~/.agents/skills/`, preuve par
appel réel (`draw.mjs --list sectors`). Aucun sudo, rien de l'amont dans le dépôt. Les sorties du skill
(`.taste-skill/` à la racine du projet visé) sont ignorées par git.

## État dans cette sandbox (vérifié le 20/10, appels réels)

- ✅ Liens installés ; `draw.mjs --list sectors|roles` répond (Node v22 présent).
- ✅ `lint.mjs` tourne (aucun navigateur requis).
- ✅ `inspect.mjs` **tourne dans la sandbox** (prouvé le 20/10, revue DM v2) : jonction avec la chaîne
  vidéo — `bash tools/video/install.sh` (Chromium @sparticuz) puis wrapper
  `CHROME_PATH=/tmp/amk-video/chrome-wrapper.sh` (exporte `LD_LIBRARY_PATH`/`FONTCONFIG_PATH`, exécute
  `/tmp/chromium`). Mesures + captures 1440/768/390 OK sur **fichiers locaux** ; l'inspection d'une
  **URL live échoue** (egress du Chromium fermé, `ERR_CONNECTION_CLOSED`). Piège : son serveur local
  sert la racine du dépôt — les chemins absolus du site (`/fonts/…`) y font 404 (faux `font-fallback`
  sur les sous-pages DM ; sur Vercel/Cloudflare, racine = le site, tout se charge).
- ⚠️ `assets.mjs` exige le réseau sortant (collections ouvertes) : egress sandbox limité → à considérer
  indisponible ici tant qu'un appel réel ne prouve pas le contraire.

## Premier usage (20/10) — lint sur l'accueil DM Optique

`node …/lint.mjs demos/dmoptic-v1.tpl.html` → **43 FAIL, 12 WARN**. L'essentiel vise l'identité DM
délibérée et approuvée par le client : IBM Plex Mono (3), filets 1px (19), numérotation 01–06 (9),
kicker (2), dégradés du hero (7), ombres de la carte d'identité (3). Lecture : les règles maison du
skill sont un **défaut pour les nouveaux builds**, pas un bulldozer pour une identité figée — l'amont
prévoit d'ailleurs `--allow <règle>` et les commentaires `taste-skill-ignore` pour ce cas. Toute
application à DM Optique qui toucherait ces dispositifs exige un ruling King explicite (conflit avec
« mêmes couleurs, même texte, même logo » et l'approbation client du 25/09).

## Garde-fous AMK

- Les verrous client et `AMK-DESIGN-SKILLS.md` restent la loi maison ; en cas de conflit avec une règle
  du skill, on signale à King au lieu de restyler en silence.
- Aucune donnée client dans `assets.mjs` (requêtes génériques seulement) ; images trouvées = crédits
  obligatoires, jamais présentées comme celles du client (rejoint « le site ne montre que du vrai »).
- Rien n'est publié/envoyé sans validation de King (règle debout) ; premier usage « production » =
  première application relue par King (TOOL-SCAN règle 3).
