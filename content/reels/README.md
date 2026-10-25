# REELS — le studio explainer AMK (format « post-it animé »)

> **Réponse à King, 25/10 (tour 144)** : *« I want content like these, can you do it ?? yes or no »* →
> **OUI.** Ce dossier contient le moteur, un épisode complet rendu, et le mode d'emploi. Les trois
> captures de référence (`/tmp/arena-coding-uploads/Screenshot_20261024-*.png`) ne sont pas copiées :
> la grammaire est reprise (fond crème, trame de points, titres noir + accent orange, cartes punaisées
> avec 0 visiteurs, pastille bicolore à côté d'un personnage qui désigne), pas les images.

## 1 · Ce qu'il y a ici

| Fichier | Rôle |
|---|---|
| `reelkit.py` | le moteur : scènes, fond, cartes, pastilles, mascotte, barre de progression, encodage |
| `ep01/make_ep01.py` | l'épisode 01 : **6 beats, arc moderne, 23,4 s** — le scénario est **dans le code**, lisible et modifiable |
| `ep01/ep01-v2.mp4` | **le master courant** : 1080×1920, 30 fps, H.264 + AAC, **23,4 s, avec voix** |
| `ep01/ep01-v2-silent.mp4` | la même image sans son (pour reposer une autre voix sans refaire le rendu) |
| `ep01/ep01-v1.mp4` | la v1 (21,4 s, sans voix, **arc classique**) — conservée comme trace, **ne pas publier** |
| `ep01/voice/` | les 6 clips de voix + `timing.json` (les durées réelles) + `build_timing.py` (la porte audio) |
| `ep01/voice.json` | le texte de la voix, beat par beat |
| `tools/qa/audit_reel.py` | **la porte de l'arc** — refuse un réel mal formé avant le rendu |
| `ep01/poster.jpg` | la couverture (frame 2,2 s) pour la vignette |
| `ep01/frames/` | les captures de contrôle (inspection avant diffusion) |
| `ep01/assets/mascot.png` | la mascotte — illustration générée, fond retiré par diffusion |

## 2 · Lancer

```bash
# deux dépendances seulement, sans apt (le paquet du bac est réinitialisé entre les sessions) :
pip install --break-system-packages pillow imageio-ffmpeg   # imageio-ffmpeg fournit le binaire ffmpeg

cd /home/user/AMK
python3 tools/qa/audit_reel.py content/reels/ep01/make_ep01.py            # ① la porte AVANT le rendu
python3 content/reels/ep01/voice/build_timing.py                          # ② mesurer la voix
python3 content/reels/ep01/make_ep01.py content/reels/ep01/ep01-v2.mp4    # ③ ≈ 30 s de rendu
```

**L'ordre n'est pas décoratif** : la porte lit `BEATS`, construit depuis `voice/timing.json`. Une voix trop
longue fait donc échouer la porte **avant** de brûler un rendu — et `build_timing.py` refuse une synthèse
muette (voir §4).

Si `ffmpeg` est déjà sur le `PATH`, il est utilisé ; sinon `imageio_ffmpeg.get_ffmpeg_exe()`.

## 3 · Le style, en six règles tenues par le code

| # | Règle | Où c'est codé |
|---|---|---|
| 1 | **Un beat = un mouvement de l'arc**, 6 beats, ≤ 25 s (règle V8 + `knowledge/STORY-ARC-2026-10-25.md`) | `build()` / `BEATS` |
| 2 | Fond **crème + trame de points**, jamais de photo | `Kit._base()` |
| 3 | **Titre noir, dernier mot orange** — un seul accent par écran | `headline()` / `s1_hook` |
| 4 | Cartes type **post-it punaisé**, une couleur par idée, entrée décalée de 0,25 s | `rounded_card()` |
| 5 | **Pastille bicolore** à côté de la mascotte : `cherchez vous-même`, `les trois manquent` | `pill()` |
| 6 | Mascotte **en bas, jamais au-dessus d'un texte** ; elle respire (± 6 px) et s'incline quand elle « parle » | `Mascot.draw()` |
| 7 | **L'arc moderne** : départ à 70, secousse entre 5 et 10 s, ≥ 3 cimes, un relâchement entre deux cimes, CTA = dernière cime (`knowledge/STORY-ARC-2026-10-25.md`) | `BEATS` + `tools/qa/audit_reel.py` |
| 8 | **Aucun glyphe hors Montserrat** : `✓` sort une boîte vide → la coche est **dessinée** | `draw_check()` |

⚠️ **Piège du dépôt, corrigé** : les quatre fichiers `content/assets/fonts/Montserrat-*.ttf` sont **le même
fichier variable** (744 936 octets chacun). Sans `set_variation_by_name`, PIL rend l'instance par défaut —
**Thin**. Le premier rendu sortait donc en maigre alors que le code demandait `ExtraBold`.
`reelkit.font()` demande l'axe ; ne pas le retirer.

## 4 · L'épisode 01 — « Votre nom existe. Votre site, non. » (v2, 23,4 s)

| Beat | Durée | La voix dit | L'écran montre | La cime | D'où vient le fait |
|---|---|---|---|---|---|
| **hook** | 0,0–5,0 | « Votre cabinet existe. Votre site, non. » | un champ de recherche « opticien akwa », un résultat sans site, le titre en 4 lignes | 70 | — (constat, aucun chiffre) |
| **spike1** | 5,0–10,1 | « Google demande trois choses : horaires, site, premier avis. » | trois cartes punaisées : `Add business hours` · `Add website` · `Pas encore d'avis` | **92** | capture Optix **24/10** (`PACK-OPTICIEN`) |
| **release1** | 10,1–12,4 | « Vous en avez une. » | le mot « une. » qui s'allume, puis « jamais les trois » | 58 | — |
| **spike2** | 12,4–17,5 | « Un site ne sert pas à avoir un site. Il répond avant l'appel. » | la phrase barrée, puis Horaires · Adresse · WhatsApp avec la coche dessinée | **88** | ruling 142 : le site est le produit |
| **release2** | 17,5–19,0 | *(souffle — pas de voix)* | « Pas de devis. Un aperçu, à votre nom. » + une page qui se dessine | 60 | — |
| **cta** | 19,0–23,4 | « Écrivez APERÇU sur WhatsApp. » | `APERÇU` en grand, le numéro, « 10 minutes cette semaine » | **95** | playbook §4 : un lien, une action |

**Ce qui a changé entre v1 et v2** — et pourquoi :

| | v1 (20:25) | v2 (21:45) |
|---|---|---|
| ouverture | carton de titre, **à zéro** | on est **déjà** dans l'écran de recherche |
| pics | **un seul** (le CTA final) = l'arc classique | **trois** (5,0 s · 12,4 s · 19,0 s) |
| voix | aucune | **6 clips**, une phrase par beat, jamais coupée |
| durée | 21,4 s | 23,4 s (la voix a dicté, pas l'inverse) |
| vérification | aucune | `audit_reel.py` : **6 beats · 3 cimes · 0 bloquant** |

**La voix** : `voice-03` (masculine, registre publicitaire), français, générée le 25/10. Les six clips sont
dans `ep01/voice/`, les durées mesurées dans `timing.json`. **Le beat s'allonge jusqu'à la voix, jamais
l'inverse** — et si le total dépasse 25 s, `build_timing.py` ferme la porte en nommant le beat à
raccourcir.

### Un défaut trouvé en vérifiant, et ce qu'il a appris

Le premier clip de `release2` (« Un aperçu, à votre nom. ») a été **généré sans erreur** — 9 549 octets,
2,33 s — et il est **muet** : RMS 0,003 au lieu de 0,096 pour les cinq autres. Un fichier qui existe n'est
pas un fichier qui parle. `build_timing.py` mesure donc le **niveau** de chaque clip et refuse la synthèse
muette ; `release2` est devenu un **souffle déclaré** (`SOUFFLE = {"release2"}`), c'est-à-dire un silence
**voulu** et non un trou.

### Ce que l'épisode ne fait pas — et c'est volontaire

- **Aucun chiffre de résultat** : pas de « +X % d'appels », pas de « 3× plus de visites ». Le seul chiffre
  est `677 78 96 31`, notre numéro.
- **Aucun nom de client**, aucun nom de concurrent : les neuf fiches sont génériques.
- **Aucune promesse de mesure** (ruling 142) : on ne dit pas ce que la fiche laisse filer, on montre ce
  qu'elle **n'a pas**.
- **Aucune mention d'IA** (ruling King 11/10) : l'épisode ne raconte pas comment il est fait.
- **Pas de voix, pas de visage, pas de sous-titre automatique** : le texte est **écrit** (ruling 11/10).
  La version avec voix demande la présence de King — elle se posera sur le **même master**, sans refaire
  les images.

## 5 · La file d'attente (même arc, même moteur, même voix)

| # | Sujet (playbook §2) | Accroche | État |
|---|---|---|---|
| EP01 | **T2** | « Votre nom existe. Votre site, non. » | ✅ **v2 rendue, voix posée, porte 3 cimes** |
| EP02 | **B1** | « Une fiche Google complète, à quoi ça ressemble » — la fiche DM Optique, trois captures | à écrire |
| EP03 | **M5** | « 3 questions avant de payer un site » | à écrire |
| EP04 | **T7** | « Deux accueils, même cabinet » — deux écrans côte à côte | à écrire |
| EP05 | **B5** | « J'ouvre deux aperçus cette semaine » | à écrire |

Un épisode = un fichier `epNN/make_epNN.py` de 150 lignes, cinq fonctions `s1..s5`. Aucun montage, aucune
timeline à maintenir : **le code est le montage**.

## 6 · Porte avant diffusion (§7 du playbook, version vidéo)

- [ ] `python3 tools/qa/audit_reel.py content/reels/epNN/make_epNN.py` → **✓** (6 règles de l'arc)
- [ ] durée ≤ 25 s et lisible **sans son** (le texte porte l'histoire, la voix la double)
- [ ] un seul accent orange par écran, aucun texte sous 30 px
- [ ] aucun chiffre qui ne soit pas daté et sourcé dans ce README
- [ ] aucun nom de client sans accord écrit
- [ ] le master est inspecté en captures (`frames/`), pas seulement en lecture rapide
- [ ] la voix est **audible là où elle doit l'être** : RMS mesuré par beat (`build_timing.py`)
- [ ] King publie — l'agent ne publie jamais
