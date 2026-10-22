# AMK — BRAG (vidéos d'annonce, chaîne installée et vérifiée)

**Installé et prouvé le 19 Oct 2026**, demande de King (« I want you to be able to use both brag
and agent reach here »). Analyse préalable et verdict au journal : `ops/TOOL-SCAN.md` §19/10 (brag).

**Ce que c'est.** [/brag](https://github.com/latent-spaces/brag) (MIT, épinglé `069432c`) est un
**skill agent** : il inspecte un projet (ou un site via `/brag-slim`), écrit un plan, compose une
vidéo d'annonce de 15–25 s avec [Hyperframes](https://github.com/heygen-com/hyperframes)
(HTML→MP4, Apache-2.0, rendu **local**, aucun frais par rendu) et livre `brag.mp4` + poster
incrusté en frame 0 + `share-copy.txt`. **Problème AMK nommé** : à la livraison d'un site, le
client n'a rien de partageable pour l'annoncer (statut WhatsApp) ; nos démos anonymisées sont des
liens, pas des preuves qui circulent. **Coût : 0 FCFA** (l'hébergé letsbrag.app à 19 $/vidéo est
l'alternative paresseuse — non retenue).

## Ce qui tourne dans cet environnement (vérifié le 19/10, pas supposé)

| Maillon | État |
|---|---|
| Skills `/brag`, `/brag-slim` + 9 skills Hyperframes | ✅ installés (≈ `~/.agents/skills/` et `~/.claude/skills/`, clones épinglés) |
| CLI Hyperframes 0.8.177 (`check`, `snapshot`, `render`) | ✅ doctor : Node 22 ✓ · FFmpeg 7.0.2 ✓ · FFprobe ✓ · Chrome ✓ (télémétrie désactivée) |
| Rendu dans la sandbox | ✅ **prouvé de bout en bout** : vidéo de démonstration complète (ci-dessous) |
| Portique maison `tools/qa/audit_video_motion.py` | ✅ **OK** sur la vidéo de démonstration (après correctif, voir « leçon ») |

**Preuve du 19/10** — un vrai `/brag` sur `hosting/previews/demo/opticien-demo.html` (page
**fictive** MboaCare, aucune donnée client) : plan depuis la copie réelle de la page (« Voir net.
Se voir bien. »), captures de la vraie page sur téléphone, composition verticale 1080×1920,
17 s, H.264 + AAC, 2,1 Mo, rendu en ~35 s, `hyperframes check` passé (contraste 9/9 WCAG AA),
snapshots relus à l'œil (2 défauts corrigés avant rendu : image lazy-load cassée, badge étiré),
poster incrusté en frame 0, portique mouvement OK. Livrables de cette preuve (hors dépôt, règle
médias lourds) : `/home/user/brag-demo-output/` (à régénérer en cas de reset).

**Leçon du 19/10 (portique) :** la première version a été **bloquée par `audit_video_motion`** —
fenêtre 0–2 s « figée » : le hook texte se pose à ~1,4 s et ne bouge plus. Correctif réel : zoom
lent continu sur tout le hook (pas un grain cosmétique). À retenir pour tout brag AMK : **chaque
scène doit bouger pendant toute sa durée** (panoramique sur les captures, zoom lent sur les
cartes texte) — c'est aussi la loi créative du skill (« make it alive »).

## Parades sandbox (pourquoi l'installation n'est pas « npx et prière »)

| Blocage | Parade (dans `install.sh`) |
|---|---|
| CDN Google bloqué → `hyperframes browser ensure` échoue (TLS) | `HYPERFRAMES_BROWSER_PATH` → wrapper sur le Chromium `@sparticuz` de la chaîne vidéo (`/tmp/amk-video`, couches al2023/fonts). Rendu en mode `screenshot` (plus lent que BeginFrame, ~2 s/s de vidéo — acceptable) |
| Les gabarits chargent GSAP depuis `cdn.jsdelivr.net` (bloqué) | **GSAP toujours en local** : copier `gsap.min.js` (npm) dans le projet et `<script src="gsap.min.js">` |
| Pas de `ffmpeg`/`ffprobe` système, pas d'apt/sudo | `ffmpeg` = binaire embarqué imageio-ffmpeg ; `ffprobe` = `@ffprobe-installer/ffprobe` (binaire **dans** le paquet npm). ⚠️ `ffmpeg-static` télécharge au postinstall depuis GitHub : échec ici, ne pas utiliser. ⚠️ Deux `npm install` en parallèle peuvent corrompre le cache (UNABLE_TO_VERIFY_LEAF_SIGNATURE) : installer en séquence |
| Polices nommées sans `@font-face` → lint | piles génériques (`sans-serif`) ou `@font-face` vers un fichier local livré |

## Ce qui NE tourne PAS ici

| Besoin | État |
|---|---|
| Voix off `--voice` (Kokoro) | Non installé (optionnel). Les modèles vivent sur HuggingFace → bloqués ici. Notre VO TikTok reste le pipeline Flow ; la question « narration obligatoire aussi pour le format annonce ? » reste un ruling King en attente |
| Musique embarquée de brag (ende.app) | **INTERDITE en production AMK** tant que la licence n'est pas documentée (TODO dans le README amont + issue #59 ouverte). La preuve du 19/10 utilise un fond **généré par ffmpeg** (nappes d'accords, libre de droits AMK) ; en production : piste générée ou licenciée, analysée par `skills/brag/scripts/analyze_music_cues.py` si on veut la synchro au beat |
| Docker / whisper-cpp / MusicGen | Absents, non requis (transcription et musique générative seulement) |

## Installation (une fois par environnement)

```bash
bash tools/brag/install.sh            # chaîne complète + doctor
bash tools/brag/install.sh --smoke    # + rendu de preuve 10 s dans /tmp/brag-smoke
export PATH="$HOME/.local/bin:$PATH"
export HYPERFRAMES_BROWSER_PATH=/tmp/amk-brag/chrome-wrapper.sh
export HYPERFRAMES_SKIP_SKILLS=1
HF=/tmp/amk-brag/node_modules/.bin/hyperframes
```

## Produire un brag (procédure AMK, par-dessus le skill)

> **Déclenchement — `PRE-FLIGHT.md` §1f② (ruling King 19/10) :** King n'a pas à le demander.
> Dès qu'un site est **fini et prêt à être livré** (portes §1b vertes), l'orchestrateur produit
> d'office un **brouillon** de brag de livraison et le présente avec le livrable.
> Rien n'est publié ni envoyé au client sans validation de King.

1. Lire `~/.agents/skills/brag/SKILL.md` (ou `brag-slim` pour une URL), puis
   `hyperframes-core` (contrat) et `hyperframes-cli` (commandes).
2. Inspection : copie **réelle** du site, couleurs exactes ; captures téléphone après
   défilement lent complet (déclenche le lazy-load — sinon images cassées, vu le 19/10).
3. `brag-plan.md` : hook → reveal → 2–3 highlights → outro, sommes 15–25 s.
4. Composition : GSAP local, une timeline paused, scènes qui bougent en continu.
5. **Portiques, dans l'ordre** : `$HF check` (0 erreur — un lint en erreur éteint les audits
   layout/contraste, les « 0/0 » ne valent rien) → `$HF snapshot --at …` (relu à l'œil, y compris
   mi-transition) → `$HF render` → poster (frame posée, incrustée en frame 0 au ffmpeg) →
   `python3 tools/qa/audit_video_motion.py brag.mp4` doit dire **OK** → lecture sur téléphone.
6. Livrables **hors dépôt** (`/home/user/…` ou `brag-output*/`, ignoré par git) : `brag.mp4`,
   `brag.jpg`, `share-copy.txt`, `brag-plan.md`.

## Règles de production (opposables)

1. **Production = après le test personnel de King** sur une vraie tâche (TOOL-SCAN règle 3).
   Statut 19/10 : chaîne prouvée sur démo fictive, pas encore un livrable client.
2. **Aucune donnée client dans les tests** ; pour un client réel, seuls les éléments publics du
   site livré, et l'étiquette de fiction reste sur toute capture de concept/démo.
3. **Tons** : santé/éducation = `polished` ou `app-store`. Jamais `cinematic`/`yc-parody`/
   `chaotic` pour un cabinet (claims). Aucune affirmation inventée (chiffres, avis) —
   `RULE-CREDENTIAL-CLAIMS` s'applique à la vidéo comme aux pages. Pour DM Optique : pas de
   prix (brief §4), et pas de brag tant que les vraies photos n'ont pas remplacé les illustrations.
4. **Musique** : générée ou licenciée avec preuve écrite ; jamais les pistes embarquées
   tant que l'issue #59 amont est ouverte.
5. **Rien n'est publié sans validation de King** (le skill lui-même reste local ; la
   publication est toujours manuelle).
6. Format distinct du pipeline TikTok VO (Flow) : l'annonce 20 s sert le **statut WhatsApp et
   le partage client** ; elle ne remplace ni le portique mouvement ni la lecture téléphone.
