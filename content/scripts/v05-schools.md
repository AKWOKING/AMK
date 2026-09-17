# V-05 — « Un parent cherche votre école » (FR, 24 s)

**Type :** école privée au Cameroun · **Objectif :** DMs « PREVIEW » · **Angle :** le parent cherche sur son téléphone ; ce qu'il trouve décide.
**Source visuelle :** `site/sample-secondary.html` (Crestwood College, **fictif et public**) — aucune autorisation requise.
**Voix :** `voice-00` (ré-auditionnée le 17 Sep 2026 — c'est l'outil de voix de la plateforme d'AMK, celui des vidéos précédentes).

## Structure (24 s)
| Temps | Contenu | Voix |
|---|---|---|
| 0 – 6,5 s | carte hook « Un parent cherche votre école / VOILÀ CE QU'IL TROUVE » | « Un parent cherche votre école sur son téléphone. Voilà ce qu'il trouve. » |
| 6,5 – 16,3 s | **capture réelle** : accueil, programmes, GCE O/A, bilinguisme, frais, admission | « Les classes, les frais, l'internat, l'admission : tout est lisible, en français comme en anglais. La demande d'inscription part sur WhatsApp, déjà rédigée. » |
| 16,3 – 18,8 s | carte payoff « TOUT EST LISIBLE. INSCRIPTION SUR WHATSAPP. » | (respiration) |
| 18,8 – 24 s | carte CTA « DM PREVIEW » + aperçu gratuit | « La même page pour votre école ? Envoyez PREVIEW en message privé. » |

**Étiquette de fiction** sur chaque image capturée : « CRESTWOOD COLLEGE (FICTIF) · DÉMONSTRATION ».

## Reproductibilité (commandes exactes)

### 0 · chaîne vidéo
```bash
bash tools/video/install.sh
export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib FONTCONFIG_PATH=/tmp/amk-video/fonts
```

### 1 · captures réelles (deux plages de la page — elle fait 15 391 px)
```bash
node tools/video/capture.mjs --url file:///home/user/AMK/site/sample-secondary.html \
     --out /tmp/capA --mode scroll --duration 6 --from-frac 0.02 --to-frac 0.17 \
     --max-speed 420 --fps 24 --settle 200

node tools/video/capture.mjs --url file:///home/user/AMK/site/sample-secondary.html \
     --out /tmp/capB --mode scroll --duration 6 --from-frac 0.53 --to-frac 0.66 \
     --max-speed 420 --fps 24 --settle 200
```

### 2 · sélection des images propres (on retire les images vides des révélations au défilement)
```bash
python3 - <<'SEL'
import glob, os, shutil
out = '/tmp/body-frames'
shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
A = sorted(glob.glob('/tmp/capA/frames/*.jpg'))
B = sorted(glob.glob('/tmp/capB/frames/*.jpg'))
for i, p in enumerate(A[20:165] + B[35:125]):
    shutil.copy(p, f'{out}/f{i:05d}.jpg')
print(len(A[20:165] + B[35:125]), 'images de corps')
SEL
```

### 3 · piste de narration (segments déjà générés, dans `narration/`)
```bash
python3 - <<'AUD'
import subprocess, imageio_ffmpeg, os
exe = imageio_ffmpeg.get_ffmpeg_exe()
N = os.path.abspath('content/videos/v05-schools/narration')
def sil(d, p):
    subprocess.run([exe, '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
                    '-t', str(d), '-y', p], check=True)
sil(0.35, '/tmp/s0.mp3'); sil(0.30, '/tmp/s1.mp3')
sil(2.45, '/tmp/s2.mp3'); sil(0.30, '/tmp/s3.mp3')
seq = ['/tmp/s0.mp3', f'{N}/01-hook.mp3', '/tmp/s1.mp3', f'{N}/02-body.mp3',
       '/tmp/s2.mp3', f'{N}/03-cta.mp3', '/tmp/s3.mp3']
open('/tmp/audiolist.txt', 'w').write(''.join(f"file '{p}'\n" for p in seq))
subprocess.run([exe, '-v', 'error', '-f', 'concat', '-safe', '0', '-i', '/tmp/audiolist.txt',
                '-c:a', 'libmp3lame', '-b:a', '192k', '-ar', '44100', '-ac', '1',
                '-y', '/tmp/v05-audio.mp3'], check=True)
print('piste narration prête : 24,16 s')
AUD
```

### 4 · montage
```bash
python3 tools/video/compose.py --frames /tmp/body-frames \
  --out content/videos/v05-schools/Video_05_School_WhatsApp_v1.mp4 --lang fr --fps 24 \
  --eyebrow "ÉCOLES · DÉMONSTRATION RÉELLE" \
  --hook "Un parent cherche votre école|VOILÀ CE QU'IL TROUVE" \
  --payoff "TOUT EST LISIBLE. INSCRIPTION SUR WHATSAPP." \
  --cta "La même page pour votre école ?" --keyword PREVIEW \
  --label "CRESTWOOD COLLEGE (FICTIF) · DÉMONSTRATION" \
  --audio /tmp/v05-audio.mp3 --hold-hook 6.48 --hold-payoff 2.45 --hold-cta 5.28
```

### 5 · portique — OBLIGATOIRE
```bash
python3 tools/qa/audit_video_motion.py content/videos/v05-schools/Video_05_School_WhatsApp_v1.mp4
# attendu : VERDICT : OK — mouvement présent dans chaque fenêtre
```
