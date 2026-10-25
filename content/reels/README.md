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
| `ep01/make_ep01.py` | l'épisode 01 : 5 plans, 21,4 s — le scénario est **dans le code**, lisible et modifiable |
| `ep01/ep01-v1.mp4` | le rendu : 1080×1920, 30 fps, H.264, 1,5 Mo, **21,4 s** |
| `ep01/poster.jpg` | la couverture (frame 2,2 s) pour la vignette |
| `ep01/frames/` | les captures de contrôle (inspection avant diffusion) |
| `ep01/assets/mascot.png` | la mascotte — illustration générée, fond retiré par diffusion |

## 2 · Lancer

```bash
# une seule dépendance graphique, sans apt :
pip install --break-system-packages pillow imageio-ffmpeg   # imageio-ffmpeg fournit le binaire ffmpeg

cd /home/user/AMK
python3 content/reels/ep01/make_ep01.py content/reels/ep01/ep01-v1.mp4   # ≈ 28 s de rendu
```

Si `ffmpeg` est déjà sur le `PATH`, il est utilisé ; sinon `imageio_ffmpeg.get_ffmpeg_exe()`.

## 3 · Le style, en six règles tenues par le code

| # | Règle | Où c'est codé |
|---|---|---|
| 1 | **Un plan = une idée**, 4 à 5 plans, 21 s (la règle maison V8 : ≤ 25 s) | `build()` |
| 2 | Fond **crème + trame de points**, jamais de photo | `Kit._base()` |
| 3 | **Titre noir, dernier mot orange** — un seul accent par écran | `headline()` / `s1_hook` |
| 4 | Cartes type **post-it punaisé**, une couleur par idée, entrée décalée de 0,25 s | `rounded_card()` |
| 5 | **Pastille bicolore** à côté de la mascotte : `cherchez vous-même`, `les trois manquent` | `pill()` |
| 6 | Mascotte **en bas, jamais au-dessus d'un texte** ; elle respire (± 6 px) et s'incline quand elle « parle » | `Mascot.draw()` |

⚠️ **Piège du dépôt, corrigé** : les quatre fichiers `content/assets/fonts/Montserrat-*.ttf` sont **le même
fichier variable** (744 936 octets chacun). Sans `set_variation_by_name`, PIL rend l'instance par défaut —
**Thin**. Le premier rendu sortait donc en maigre alors que le code demandait `ExtraBold`.
`reelkit.font()` demande l'axe ; ne pas le retirer.

## 4 · L'épisode 01 — « Votre nom existe. Votre site, non. »

| Plan | Durée | Ce qui est dit à l'écran | D'où vient le fait |
|---|---|---|---|
| 1 | 4,0 s | « Votre nom existe. Votre site, non. » + « cherchez vous-même » | — (constat, pas de chiffre) |
| 2 | 5,0 s | « Ce que Google réclame : Add business hours · Add website · Pas encore d'avis » | capture de la fiche Optix du **24/10** (`sales/PACK-OPTICIEN-2026-10.md`, tableau « Ce qu'un patient voit ») |
| 3 | 4,2 s | Neuf fiches punaisées, **0 site** partout | même capture — le mur des fiches vides |
| 4 | 4,2 s | « Ce qui règle les trois : votre site — Horaires · Adresse · WhatsApp » | ruling 142 : **le site est le produit** |
| 5 | 4,0 s | « Écrivez **APERÇU** sur WhatsApp · 677 78 96 31 · 10 minutes cette semaine » | playbook §4 : un lien, une action |

**Carte de contenu** : cet épisode est le sujet **T2** du `sales/SOCIAL-ACQUISITION-PLAYBOOK-2026-10-25.md`
§2 (TOFU, vidéo 25 s) — il est donc déjà planifié au **mardi 03/11**, et peut remplacer le carrousel T1 du
27/10 si la production du carrousel prend du retard.

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

## 5 · La file d'attente (mêmes 5 plans, même moteur)

| # | Sujet (playbook §2) | Accroche | État |
|---|---|---|---|
| EP01 | **T2** | « Votre nom existe. Votre site, non. » | ✅ rendu |
| EP02 | **B1** | « Une fiche Google complète, à quoi ça ressemble » — la fiche DM Optique, trois captures | à écrire |
| EP03 | **M5** | « 3 questions avant de payer un site » | à écrire |
| EP04 | **T7** | « Deux accueils, même cabinet » — deux écrans côte à côte | à écrire |
| EP05 | **B5** | « J'ouvre deux aperçus cette semaine » | à écrire |

Un épisode = un fichier `epNN/make_epNN.py` de 150 lignes, cinq fonctions `s1..s5`. Aucun montage, aucune
timeline à maintenir : **le code est le montage**.

## 6 · Porte avant diffusion (§7 du playbook, version vidéo)

- [ ] durée ≤ 25 s et lisible **sans son**
- [ ] un seul accent orange par écran, aucun texte sous 30 px
- [ ] aucun chiffre qui ne soit pas daté et sourcé dans ce README
- [ ] aucun nom de client sans accord écrit
- [ ] le master est inspecté en captures (`frames/`), pas seulement en lecture rapide
- [ ] King publie — l'agent ne publie jamais
