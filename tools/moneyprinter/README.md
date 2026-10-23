# MoneyPrinterTurbo — installé pour assembler **nos** plans

> Dépôt : `harry0703/MoneyPrinterTurbo` · commit **`f063a2b`** (23/10/2026) · **MIT** · installé le
> 23/10/2026 dans `tools/moneyprinter/`. Rien du dépôt amont n'est copié ici : seul l'installeur est à nous.

## 1 · Ce que c'est, en une phrase

Un outil qui prend **un sujet** et rend une vidéo courte complète : script, voix, sous-titres, musique,
et plans assemblés. Par défaut il va chercher ses plans dans des banques d'images (Pexels, Pixabay) et
fait écrire le script par un modèle (Moonshot, OpenAI…).

## 2 · Ce qu'on en garde, et ce qu'on refuse

| Ce que l'outil sait faire | Décision | Pourquoi |
|---|---|---|
| assembler **nos propres rushes** (`--video-source local`) | ✅ **gardé** | c'est tout ce qu'on lui demande : quatre plans tournés au cabinet, l'audio, la coupe |
| couper à la durée de l'audio, 9:16 **et** 16:9 depuis le même tournage | ✅ **gardé** | c'est la règle « un tournage, deux montages » (§5 quater), sans la faire à la main |
| sous-titres incrustés (Whisper) | ⚠️ **utilisable, pas testé ici** | le modèle se télécharge au premier usage (~150 Mo en `small`, ~3 Go en `large-v3`) — le réseau est fermé dans la sandbox |
| voix automatique (edge-tts) | ❌ **refusé par défaut** | une voix de synthèse sur un sujet de santé sonne faux ; on enregistre la voix au téléphone, 30 secondes |
| plans de banque d'images (Pexels/Pixabay) | ❌ **refusé** | règle du décor réel : le spectateur doit pouvoir pousser la porte qu'il voit |
| script écrit par un modèle | ❌ **refusé** | le script est écrit, relu et validé avant tournage ; `assemble.sh` **exige** `--script` |
| publication automatique vers les réseaux | ❌ **non installé** | King publie lui-même |

## 3 · Installer, assembler

```bash
bash tools/moneyprinter/install.sh                      # ~50 s la première fois, hors du dépôt
bash tools/moneyprinter/assemble.sh \
     --clips /tmp/rushs-55ans --audio /tmp/voix.m4a \
     --script "Vous éloignez votre téléphone pour lire ? …" \
     --out /tmp/55ans --aspect 9:16
```

Sortie : un `.mp4` coupé à la durée de l'audio, dans `--out`. Relancer avec `--aspect 16:9` pour le
deuxième montage.

| Option | Ce qu'elle fait | Réseau ? |
|---|---|---|
| `--subtitles` | **sous-titres sans Whisper** : le script connu est découpé au temps (`srt.py`) puis incrusté par ffmpeg, police du projet | **non** |
| `--whisper` | sous-titres par Whisper (chemin natif de MPT) | oui — modèle au 1er usage |
| `--music none\|random` | musique de fond depuis `resource/songs` (29 titres) | non |

**Ce qui reste hors du dépôt :** la source (733 Mo, dont 198 Mo de polices et de musiques) et le venv
(1,2 Go) vivent dans `/tmp/amk-moneyprinter`, comme Chromium dans `/tmp/amk-video`. Un dépôt n'est pas
un disque dur.

## 4 · Ce que l'installation a réellement prouvé (23/10)

| Étape | Résultat |
|---|---|
| clone épinglé | commit `f063a2b` exact, vérifié par comparaison de SHA |
| dépendances | 25 paquets, ~35 s, 1,2 Go — `moviepy 2.2.1`, `edge-tts`, `faster-whisper`, `streamlit` |
| tests amont | **2 341 passés · 142 ignorés · 0 échec** (307 s) — le code est tenu |
| ffmpeg | embarqué (`ffmpeg 7.0.2`), aucun paquet système, aucun sudo |
| assemblage réel | 4 plans 1080×1920 + un audio de 20 s → **`final-1.mp4` 20,0 s · 1080×1920 · 30 i/s · avec son**, en **38 s** |
| deux formats | 9:16 (1,1 Mo) et 16:9 (562 Ko) depuis le même dossier de rushes |
| ce qui n'a pas pu être testé | voix edge-tts, banques d'images, sous-titres Whisper : **tous demandent le réseau**, fermé ici |

## 5 · Ce qui manquait pour le faire tourner « efficacement », et comment c'est compensé (23/10)

| Ce qui manque à l'outil brut | Pourquoi c'est bloquant | La compensation |
|---|---|---|
| un **script** (il appelle un LLM) | sans clé Moonshot/OpenAI, la tâche échoue à la première étape | `--script` **obligatoire** : le texte est le nôtre, écrit et relu |
| une **voix** (edge-tts, réseau) | voix de synthèse sur un sujet de santé = perte de confiance | voix **enregistrée** au téléphone ; `--custom-audio-file` |
| des **sous-titres** (Whisper ~150 Mo à 3 Go) | modèle à télécharger, et une transcription d'un texte qu'on connaît déjà | `srt.py` : découpage déterministe du script au temps de l'audio, incrusté par ffmpeg — **0 téléchargement** |
| des **plans** (banques d'images, clés payantes) | le décor doit exister | `--video-source local` forcé : nos rushes, copiés dans `storage/local_videos` |
| une **musique** | `bgm_type` par défaut peut chercher ailleurs | `--music` pointe les 29 titres embarqués, ou `none` |
| la **durée** : l'outil boucle si la vidéo est plus courte que l'audio | une boucle se voit | on tourne large (3 s de respiration) ; l'outil le dit dans son journal (`looping clips`) |

**Le résultat mesuré le 23/10 :** 4 plans + 20 s d'audio → 20 s montées en 38 s, puis sous-titres
incrustés en ~5 s. **Aucun appel réseau** sur ce chemin.

**La leçon de l'installation :** le premier essai a échoué — sans `--video-script`, l'outil appelle un
LLM et s'arrête faute de clé. `assemble.sh` refuse donc maintenant de démarrer sans script. Un outil
qui peut appeler un modèle sans qu'on le sache doit être enveloppé, pas utilisé nu.
