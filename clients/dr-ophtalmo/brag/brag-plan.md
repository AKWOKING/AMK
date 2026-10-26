# Brag plan — Dr Ophtalmo (brouillon de livraison, §1f②)

- **Ton :** `polished` (santé — seuls `polished` / `app-store` sont admis) · **Format :** vertical
  1080×1920, 30 fps, H.264 + AAC · **Durée :** 20 s · **Langue :** FR
- **Matière :** **captures réelles du site construit** (`hosting/previews/dr-ophtalmo/` @ `f3f05ee`), prises
  en Chromium à **540 × 1500 @2×** (1080 × 3000 px réels), défilement complet d'abord pour déclencher le
  lazy-load, puis cadrage sur chaque section : hero, lieux, semaine, formulaire. Aucune maquette, aucune
  capture d'un autre site, **aucune personne générée présentée comme le médecin** (les images du site
  portent déjà leurs légendes « image générée »).
- **Couleurs / polices :** celles du site — marine `#07111d`, teal `#76b9b4`, crème `#f6f8fa` ; Newsreader
  + Inter Tight en woff2 **locaux** (aucun appel réseau au rendu). GSAP servi **en local**
  (`gsap.min.js` copié depuis `/tmp/amk-brag`, jamais le CDN).
- **Musique :** nappe **générée par ffmpeg** — accord C–E–G–A (130,81 / 164,81 / 196 / 220 Hz), `aecho`,
  fondu d'entrée 2,2 s et de sortie 2,8 s — ajoutée après rendu (`-c:v copy -c:a aac`). La piste
  embarquée de brag (ende.app) reste **interdite** : licence non documentée (issue #59).

| # | Scène | t | Mouvement continu |
|---|---|---|---|
| 1 | HOOK — « Où consulter ? » / « Un médecin, quatre lieux. » | 0 – 3,6 s | entrée en cascade + échelle 1 → 1,07 et y −70 sur toute la scène |
| 2 | 01 · LE SITE — capture réelle du hero | 3,6 – 8,0 s | panoramique vertical −260 px + échelle 1 → 1,02 |
| 3 | 02 · LA SEMAINE — capture réelle ; la pastille « Horaires à confirmer » **est dans notre carte**, pas posée sur la page | 8,0 – 12,4 s | panoramique −360 px + échelle 1 → 1,02 |
| 4 | 03 · LES LIEUX — les quatre lieux numérotés | 12,4 – 16,8 s | panoramique −240 px + échelle 1 → 1,02 |
| 5 | GÉNÉRIQUE — « Votre vision, / ma priorité. » + 4 villes + « Aperçu privé, non publié. » + AMK | 16,8 – 20 s | échelle 1 → 1,09, y +40 → −96, halo dédié qui monte |

**Fond commun, 20 s sans interruption :** halo qui dérive (x −60 → 190, y −40 → 260), second halo en
contre-sens, troisième halo réservé au générique, grille qui glisse (−300, +400 px) et **fond entier qui
avance vers la caméra** (échelle 1 → 1,085). Rien ne s'immobilise, y compris pendant le générique.

**Ce que la vidéo ne dit pas :** aucun nom de médecin, aucun horaire précis, aucun numéro, aucun prix,
aucun avis, aucune disponibilité en temps réel, aucune inscription à l'Ordre. Elle ne dit pas « voici un
beau site » : elle dit « voici où l'on consulte cette semaine — et tout ce qui reste à confirmer est écrit
dessus ».

**Portiques, dans l'ordre, et ce qu'ils ont donné :**

| Porte | Résultat mesuré |
|---|---|
| `hyperframes check` | **0 erreur**, 19/19 textes en contraste AA · 12 avertissements, tous de la même famille (`nested_structure_needs_subcomposition` : la timeline d'une composition monolithique n'affiche qu'une ligne par élément racine — cosmétique, pas un défaut de rendu). Les `container_overflow` des captures (zoom) sont marqués intentionnels par `data-layout-allow-overflow`. |
| 2 défauts trouvés **à l'œil** sur les captures (`snapshot --at`) et corrigés | ① le panoramique à 1,14 d'échelle **rognage du texte sur les côtés** → échelle ramenée à 1 → 1,02 (11 px par côté, dans la marge de 64 px) ; ② la carte de légende en `rgba(.94)` laissait **traverser le texte du site** → fond opaque `#07111d`, et la pastille « Horaires à confirmer » déplacée **dans** la carte pour qu'on ne la confonde pas avec ce que le site affiche. |
| `hyperframes render --quality looks` | 20,0 s · 600 images · capture `screenshot`, GPU logiciel · ~70 s |
| `audit_video_motion.py` | **OK sur les deux fichiers** — fenêtre la plus faible **18–20 s à 2,12** (elle était **1,39 = FIGÉE** au premier rendu, d'où le troisième halo et le fond qui avance) |
| Lecture des images du film | 5 images relues (1,6 · 6,0 · 10,6 · 14,5 · 18,4 s) : aucun texte rogné, aucune carte qui masque une information qu'elle prétend montrer |

**Livrables — maintenant DANS le dépôt** (exception datée dans `.gitignore`, demande de King
« push the brag video to github ») :

| Fichier | Poids | Rôle |
|---|---|---|
| `clients/dr-ophtalmo/brag/brag.mp4` | **4,1 Mo** (crf 23) | la version qu'on regarde sur GitHub |
| `clients/dr-ophtalmo/brag/brag-whatsapp.mp4` | **2,5 Mo** (crf 27) | la version statut WhatsApp |
| `clients/dr-ophtalmo/brag/poster.jpg` | 67 Ko | affiche, extraite à 18,4 s (**jamais** en `attached_pic` : ça casse la durée) |

Le master non recompressé (14 Mo, AAC 160 kb/s, copie vidéo du rendu) reste **hors dépôt** : il se refait
par un rendu de 70 s. Le projet de composition a été perdu au redémarrage de l'environnement (tout `/tmp`
l'est) et **reconstruit** : les captures sont reproductibles en 10 s par le script de capture, la
composition est décrite ici scène par scène.

**Refaire la vidéo, de zéro :**

```bash
bash tools/video/install.sh && bash tools/brag/install.sh
export HYPERFRAMES_BROWSER_PATH=/tmp/amk-brag/chrome-wrapper.sh HYPERFRAMES_SKIP_SKILLS=1
export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib FONTCONFIG_PATH=/tmp/amk-video/fonts
python3 -m http.server 8080 --bind 0.0.0.0 --directory hosting/previews/dr-ophtalmo &
# captures 540×1500 @2× → composition GSAP locale → check → snapshot → render
# → nappe ffmpeg → mux (-c:v copy -c:a aac) → crf 23 / crf 27 → poster à 18,4 s
python3 tools/qa/audit_video_motion.py clients/dr-ophtalmo/brag/brag.mp4   # doit dire OK
```

**Rien n'est publié, rien n'est envoyé au médecin sans validation de King** (règle brag AMK, §1f②).
Le dépôt public ne rend pas la vidéo publique : elle est dans un dépôt privé, **et** le site qu'elle
montre est en `noindex` + `robots.txt`.
