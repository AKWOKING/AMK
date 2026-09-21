# AMK — CHAÎNE VIDÉO (outils installés et vérifiés)

**Créé le 17 Sep 2026 (nuit).** Réponse au refus de King sur le correctif « juste un zoom » : la
cause racine n'était pas le montage, c'était que **nous n'avions aucune image en mouvement**.
Cette chaîne produit cette matière première.

## Ce qui tourne dans cet environnement (vérifié, pas supposé)

| Étape | Outil | État |
|---|---|---|
| Navigateur headless | `@sparticuz/chromium` 153 (npm, **embarque le binaire** — les CDN de navigateurs sont bloqués ici) | ✅ démarre, capture en 0,6 s |
| Extraction des couches système | `al2023.tar.br` (libnss3/libnspr4/libexpat) + `fonts.tar.br` fournis par le paquet | ✅ via `bin/brotli` du paquet |
| Pilote | `puppeteer-core` 25 | ✅ |
| Composition / encodage | `imageio-ffmpeg` (FFmpeg 7.0.2) | ✅ |
| Cartes animées | `PIL` + formules de mouvement | ✅ |
| **Portique mouvement** | `tools/qa/audit_video_motion.py` | ✅ bloque les diaporamas |

### Installation (une fois par environnement)
```bash
bash tools/video/install.sh          # ~70 Mo dans /tmp/amk-video, hors dépôt
export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib
export FONTCONFIG_PATH=/tmp/amk-video/fonts
```

### Production d'un clip
```bash
# 1 · capture réelle (défilement d'une page, 1080×1920, images JPEG)
node tools/video/capture.mjs --url file:///…/page.html --out /tmp/cap --mode scroll --duration 12

# 2 · montage (hook animé + capture + payoff + CTA)
python3 tools/video/compose.py --frames /tmp/cap/frames --out clip.mp4 --lang fr \
    --hook "Une vraie page|QUI DÉFILE" --payoff "FINI LES DIAPORAMAS." --label "MBOACARE (FICTIF)"

# 3 · portique — OBLIGATOIRE avant toute livraison
python3 tools/qa/audit_video_motion.py clip.mp4      # doit afficher : OK
```

### Démos publiables (bibliothèque)
```bash
python3 tools/video/anonymise.py --all     # 5 concepts → hosting/previews/demo/*.html
                                           # 0 fuite d'identité + audit HTML 0 anomalie
```
Les pages produites sont **fictives** (MboaCare), sans nom réel, sans vrai numéro, `noindex`,
avec bandeau de démonstration. C'est ce qui rend nos concepts **publiables**.

## Ce qui NE tourne PAS ici (et pourquoi)

| Besoin | Outil | Blocage constaté |
|---|---|---|
| Narration | **Piper** (MIT) | `pip install piper-tts` ✅ mais **les voix sont sur HuggingFace → bloqué** (HF et tous les miroirs testés : 000). À produire sur la machine de King. |
| Sous-titres auto | faster-whisper / whisper.cpp | Modèles sur HF → même blocage |
| Rendus HTML avancés | weasyprint | `libpango-1.0-0` absente, `apt` indisponible |
| Téléchargement de binaires | — | `storage.googleapis.com`, `cdn.playwright.dev`, `objects.githubusercontent.com` bloqués |

## Règle de production (opposable)
1. **Aucune vidéo ne part sans passer** `audit_video_motion.py` → **OK**.
2. La partie centrale est une **capture réelle** (page qui défile) — pas une image fixe animée par un zoom.
3. **Aucun recadrage** sur une carte composée (un zoom de 1,3× coupe le texte — vérifié sur la v04c).
4. **Narration** dans le fichier livré (pas de son tendance ajouté à la publication).
5. Étiquette de fiction sur toute capture d'écran.
