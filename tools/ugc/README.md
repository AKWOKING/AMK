# `tools/ugc` — le moteur UGC

```
storyboard JSON  ->  ugc.py  ->  MP4 1080x1920 (mouvement + sous-titres + voix + carton)  ->  portique
```

Trois fichiers, aucun service externe obligatoire :

| Fichier | Rôle |
|---|---|
| `ugc.py` | moteur « nuit » : scènes, mouvement, sous-titres incrustés, cartons, couverture, portique |
| `editorial.py` | moteur « éditorial clair » : fond crème des fiches produit, détourage réel, typographie sujet — le registre des références client (voir `clients/dm-optic/content/month1/w1/SPOT-DIRECTION.md`) |
| `providers.py` | les fournisseurs de **clips IA** (Veo, HeyGen, Hedra, fal) : devis, appel, refus propre sans clé |
| `README.md` | ce document |

Décision et comparatif de prix : **`research/ugc-video/2026-10-22-TOOLCHAIN-UGC.md`**.

---

## 1 · Pourquoi ce moteur existe

Les plateformes d'avatar (HeyGen, Arcads, Creatify) vendent **le plan** — un humain qui parle. Elles ne
vendent pas **la pub** : ni le produit réel, ni la preuve, ni la sortie honnête, ni le carton, ni la
mesure. Une vidéo UGC qui convertit, c'est 60 % d'assemblage.

Ce moteur prend le plan généré (ou filmé) comme **une scène parmi d'autres** et assemble autour de lui
ce qui rend le contenu crédible et mesurable — avec les photos réelles du client, sa voix, son WhatsApp.

## 1 bis · Deux moteurs, deux registres

| | `ugc.py` | `editorial.py` |
|---|---|---|
| Fond | nuit dégradé | **crème 246,235,225** (le fond des fiches montures) |
| Produit | carte crème sur fond nuit | **détouré**, flottant, ombre portée réelle |
| Texte | bandeau de sous-titres | **typographie comme sujet** |
| Rythme | plans de 3 à 4 s | **aucun plan > 1,9 s** (garde-fou bloquant) |
| Son | voix seule | voix + nappe générée (accords tenus, souffle sur les coupes) |
| Usage | UGC explicatif, cartons de marque | **spots publicitaires**, déclinés d'une référence |

Le second est né d'un retour client : *« I don't like the videos »* — le registre sombre ne ressemblait
pas aux vidéos de référence. Les deux restent disponibles ; le registre clair est le défaut pour un spot.

## 2 · Les quatre types de scène

```jsonc
{"type": "photo",   "src": "...webp", "dur": 3.4, "focus": 0.5, "zoom": 0.16, "pan": -0.55, "drift": 0.45,
                    "sub": "Choisir des lunettes,\nça commence par mesurer."}

{"type": "clip",    "src": "clip-veo.mp4", "dur": 4.0, "zoom": 0.14, "drift": 0.4,
                    "sub": "…"}                       // clip IA ou rush filmé, bouclé si trop court

{"type": "card",    "src": "...webp", "dur": 3.4, "headline": "Sur le site, avant de venir",
                    "big": "40 montures", "foot": "photographiées · prix affichés"}

{"type": "endcard", "src": "...webp", "headline": "EXAMEN DE VUE", "big": "8h30–13h00",
                    "foot": "du lundi au samedi", "cta": "WhatsApp 656 122 239",
                    "sub": "On montre avant de vendre."}
```

**Clés utiles**

| Clé | Effet | Valeur sûre |
|---|---|---|
| `layout` | `product` : la fiche produit est posée sur une carte crème, fond nuit (le produit n'est pas retouché) | `flat` par défaut |
| `zoom` | amplitude du recadrage mouvant (0 = figé) | **0,14–0,18** photo · **0,55** carton |
| `pan` / `drift` | sens du glissement horizontal / vertical, −1 à +1 | ±0,45 |
| `focus` | cadrage horizontal de la photo (0 gauche, 1 droite) | 0,3–0,5 |
| `scrim_top` / `scrim_band` | voile nuit sur le fond d'un carton : hors bande / dans la bande de texte | 0,30 / 0,88 |
| `grain` | dither aléatoire par image — casse le banding H.264 **et** garde le carton vivant | 2 |
| `sub` | sous-titre incrusté (`\n` pour deux lignes) — c'est lui qu'on lit sans le son | — |
| `voice` | piste voix du storyboard ; ajustée par `atempo` pour tenir dans la durée | — |

> **Mouvement : ne pas descendre sous `zoom` 0,14.** Le portique (§5) refuse une fenêtre de 2 s dont
> l'écart maximal entre images reste sous 1,5/255. Un carton « stable » est impossible : c'est le fond
> photographique qui bouge derrière, pas le texte.

## 3 · Usage

```bash
# vérifier un storyboard (fichiers présents, durées, total)
python3 tools/ugc/ugc.py check clients/dm-optic/content/month1/w1/ugc-03.json

# rendre
python3 tools/ugc/ugc.py render clients/dm-optic/content/month1/w1/ugc-03.json \
        --out clients/dm-optic/content/month1/w1/ugc-03.mp4 \
        --cover clients/dm-optic/content/month1/w1/ugc-03-cover.jpg --qc

# état des fournisseurs de clips + devis
python3 tools/ugc/providers.py
python3 tools/ugc/providers.py quote 8
```

`--qc` lance `tools/qa/audit_video_motion.py` et **rend le code de sortie du portique** : un rendu qui
gèle en sortie 1.

## 4 · Ajouter un plan IA

```python
from providers import generate_veo, generate_heygen
generate_veo("Un opticien, plan poitrine, téléphone à la main, lumière de fin d'après-midi, "
             "il parle à la caméra, style UGC vertical", "shots/plan-01.mp4",
             tier="fast", res="1080p", seconds=8)          # ~0,96 $
generate_heygen(script, avatar_id, voice_id, "shots/presentateur.mp4")   # 29 $/mois
```

Puis dans le storyboard : `{"type": "clip", "src": "shots/plan-01.mp4", "dur": 4.0}`.

**Sans clé, ces fonctions lèvent une erreur explicite** — elles ne renvoient jamais un faux succès.

## 4 bis · Les deux portiques, dans l'ordre

```bash
python3 tools/qa/audit_claims.py clients/dm-optic/content          # 1. les affirmations
python3 tools/qa/audit_video_motion.py <fichier>.mp4               # 2. le mouvement
python3 tools/ugc/editorial.py --story <storyboard>.json --out …   # 3. le rendu
python3 tools/qa/audit_video_motion.py <fichier>.mp4               # 4. re-contrôle
```

Le premier vérifie qu'aucune phrase ne contredit un **verrou client** (prix publics, cardinal de stock,
superlatif, allégation médicale). Le second vérifie qu'aucune fenêtre de 2 s ne gèle.

**Règle de rythme du registre éditorial** : `MAX_PLAN = 1,9 s` dans `editorial.py`. Le moteur **refuse**
un storyboard dont un plan dépasse cette durée et nomme la scène — parce qu'à 270 px (la largeur
d'échantillonnage du portique), un carton crème de 3 s est mesuré comme figé.

## 5 · Le portique, en une ligne

`python3 tools/qa/audit_video_motion.py <fichier>` — échantillonne à 12 fps, mesure l'écart entre
images, agrège par fenêtres de 2 s. Une fenêtre dont l'écart maximal reste sous **1,5/255** est
**FIGÉE** ; le portique sort en **code 1** et la vidéo ne part pas.

## 6 · Ce que ce moteur ne fait pas

- **Il ne génère pas de visage.** Aucun modèle de génération n'est embarqué : le plan vient d'une API
  (`providers.py`) ou d'un tournage.
- **Il ne tourne pas de modèle ouvert.** Ce sandbox a 2 cœurs, 3 Go de RAM, aucun GPU, et
  `huggingface.co` est bloqué : Wan, MuseTalk, InfiniteTalk, LatentSync sont hors de portée ici.
- **Il ne publie pas.** La publication reste une décision humaine (verrou §4b).
