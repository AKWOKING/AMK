# RECHERCHE — OUTILLAGE VIDÉO COMPLET (17 Sep 2026)

**Commande de King :** *« if you need a tool don't be lazy go through github I am sure you will find an opensource tool that will fit our need, do a deep research to find all the tools that you need to create the videos, don't stop until you do »*

**Verdict en une ligne :** la chaîne complète existe en open source et **tourne déjà** pour la partie capture/montage ; seule la **narration** reste bloquée dans cet environnement (modèles hébergés sur HuggingFace, réseau fermé) — elle se produira sur la machine de King avec Piper.

---

## 1 · Ce qui manquait vraiment

Le refus de King sur le correctif (« just a zoom in ») a mis au jour **deux** problèmes, pas un :

1. **Aucune image en mouvement** dans nos sources : nos vidéos étaient des diaporamas (6 à 9 fenêtres de 2 s figées sur 14–17 — `content/lessons/CONTENT-LESSONS.md` §13).
2. **Aucune chaîne outillée** pour en produire : tout était composité à la main en PIL sur des images fixes.

La recherche ci-dessous cible donc quatre besoins : **capture**, **montage**, **voix**, **sous-titres** — plus la **composition programmée** et la **capture depuis un téléphone**.

---

## 2 · Le tableau (données GitHub vérifiées par API le 17 Sep 2026)

| Outil | Étoiles | Licence | Dernier commit | Rôle | Verdict AMK |
|---|---|---|---|---|---|
| **puppeteer/puppeteer** | 95 582 | Apache-2.0 | 2026-09-17 | pilote Chrome/Chromium | ✅ **adopté** (déjà dans le dépôt) |
| **Genymobile/scrcpy** | 149 853 | Apache-2.0 | 2026-09-16 | capture écran Android (USB/Wi-Fi), sans root, H.265 | ✅ **recommandé à King** — capture parfaite depuis son téléphone |
| **OpenCut-app/OpenCut** | 89 682 | MIT | 2026-08-10 | alternative open source à CapCut (montage visuel) | 🟡 utile si King veut monter à la main, pas notre chaîne |
| **openai/whisper** | 109 290 | MIT | 2026-08-31 | transcription/sous-titres | ✅ **référence** (via faster-whisper) |
| **SYSTRAN/faster-whisper** | 25 444 | MIT | 2025-11-19 | Whisper ×4 plus rapide (CTranslate2) | ✅ **adopté** pour les sous-titres — bloqué ici (modèles HF) |
| **rhasspy/piper** | 11 284 | **MIT** | 2025-08-26 | TTS neuronal CPU, 47 langues dont **français** | ✅ **adopté pour la narration** — bloqué ici (voix sur HF) |
| **Zulko/moviepy** | 14 901 | MIT | 2026-08-26 | montage vidéo en Python | 🟡 écarté : FFmpeg direct suffit et reste plus rapide |
| **WyattBlue/auto-editor** | 5 238 | Unlicense | 2026-09-13 | coupe automatique des silences | 🟡 utile plus tard (nettoyage de rushes) |
| **motion-canvas/motion-canvas** | 19 121 | MIT | 2026-07-02 | animation TypeScript (générateurs) | 🟡 gardé en réserve (animations complexes) |
| **midrender/revideo** | 4 047 | MIT | 2026-07-15 | « vidéo par le code », fork de Motion Canvas | 🟡 réserve (ex-`redotvideo/revideo`) |
| **mifi/editly** | 5 504 | MIT | 2025-05-12 | montage déclaratif JSON+FFmpeg | 🟡 réserve |
| **remotion-dev/remotion** | 59 592 | **NOASSERTION (non libre)** | 2026-09-17 | vidéo en React | ❌ **écarté** : licence propriétaire, payante au-delà de 3 employés (source-available, pas FOSS) |

**Lecture :** pour notre cas — capturer une vraie page, composer des cartes sobres, encoder en 9:16 — la pile **Puppeteer + FFmpeg + PIL** est la plus légère et la plus contrôlable. Les frameworks de motion design (Motion Canvas, Revideo, Remotion) seraient utiles pour des animations abstraites ; **nous n'en avons pas besoin**, et Remotion est disqualifié par sa licence.

---

## 3 · Ce que la recherche a permis de débloquer tout de suite

**La capacité était déjà dans le dépôt.** `tools/shots/package.json` déclarait depuis le 14 Sep : `@sparticuz/chromium` + `puppeteer-core`. C'est le paquet qui **embarque un Chromium compilé dans son archive npm** — donc aucun CDN de navigateur à joindre (tous bloqués ici). Le README de `tools/shots` documentait même jusqu'à la compilation manuelle de NSS.

**Ce qui a été construit autour (17 Sep, nuit) :**

| Fichier | Rôle |
|---|---|
| `tools/video/install.sh` | installe la chaîne (~70 Mo dans `/tmp/amk-video`), extrait les couches `al2023`/`fonts`/`swiftshader` (brotli+tar) et **vérifie en capturant une vraie page** |
| `tools/video/capture.mjs` | capture le **défilement réel** d'une page en images JPEG (1080×1920 par défaut, cadence fixe, vitesse lisible, `manifest.json`) |
| `tools/video/compose.py` | hook animé → capture → payoff → carte CTA ; **toutes les cartes ont un mouvement continu** (apparitions, reflets, barres de progression, pastilles qui respirent) |
| `tools/video/anonymise.py` | transforme un concept client en **page de démonstration publiable** (fiction MboaCare) + **contrôle de fuite fort** (numéros, marques, noms de praticiens, adresses) + portique HTML |
| `tools/qa/audit_video_motion.py` | **portique bloquant** : mesure l'écart d'image par fenêtre de 2 s, refuse tout diaporama |

**Problèmes résolus en route (traces utiles) :**
- Chromium ne démarrait pas faute de `libnspr4/libnss3` : les couches `.tar.br` du paquet les fournissent → `LD_LIBRARY_PATH`.
- `@sparticuz/chromium` v153 est **ESM-only** → chargement dynamique dans `capture.mjs` (un `require` échoue).
- `drawtext` **absent** du build FFmpeg fourni → les libellés passent par PIL + `overlay`.
- Le premier montage animé (v04c) **coupait le texte** avec des recadrages 1,3× → règle : pas de recadrage sur une carte composée.

---

## 4 · La narration : le seul vrai blocage restant

| Option | Licence | Qualité | Où ça tourne |
|---|---|---|---|
| **Piper** (voix `fr_FR-siwis-medium` / `fr_FR-upmc-medium`, ~60 Mo) | **MIT** — usage commercial libre | bonne (MOS ≈ 3,5) | machine de King (accès HuggingFace) — `pip install piper-tts` ✅ déjà installé ici |
| **Kokoro** (82 M, Apache-2.0) | Apache-2.0 | très bonne, **anglais** surtout | idem |
| **XTTS v2** (Coqui) | **CPML — non commercial** | excellente (clonage) | ❌ écarté : licence incompatible avec nos prestations payantes |
| **F5-TTS** | CC-BY-NC-4.0 | excellente | ❌ écarté (non commercial) |
| **Coqui TTS** (fork `coqui-tts`) | MPL-2.0 (poids XTTS non libres) | bonne | 🟡 réserve |

**Décision :** **Piper** pour la narration FR (licence MIT, voix commerciale libre), **Kokoro** si nous faisons de l'anglais plus tard. Les deux exigent un accès HuggingFace : à lancer sur la machine de King **ou** dans une session où le réseau le permet.

**Alternative humaine recommandée :** la voix de **King lui-même** pour les vidéos « fondateur ». C'est le différenciateur que personne ne copie — et nos messages d'approche sont déjà signés de son nom. À trancher par lui.

---

## 5 · Ce qui reste à faire

1. **Réseau HuggingFace** (ou machine de King) → narration Piper FR + sous-titres faster-whisper automatiques.
2. **scrcpy** si King veut une capture depuis son téléphone sans compression (la nôtre, par Chromium, donne déjà 1080×1920 propre — le téléphone n'est plus indispensable).
3. **V-05** : script existant, capture prête (bibliothèque de démos), il ne manque que la voix.
4. **Ne pas réintroduire** : Remotion (licence), XTTS/F5-TTS (non commercial), recadrages sur cartes composées, diaporamas.

---

## 6 · Sources

- Recherches web du 17 Sep 2026 : comparatifs « programmatic video » (Revideo/Motion Canvas/Remotion/Editly/VideoFlow), comparatifs TTS locaux (Piper/Coqui/Kokoro/XTTS/F5), outillage sous-titres (Whisper/faster-whisper/whisper.cpp) et capture Android (scrcpy).
- **Données GitHub vérifiées par `gh api` le 17 Sep 2026** (étoiles, licence SPDX, dernier push) — voir tableau §2.
- Constats locaux : tests réseau (pypi/npm/github OK ; HF, CDN navigateurs, objects.githubusercontent bloqués), exécution réelle de Chromium dans cet environnement, mesures du portique mouvement.
