# Video 04 — Losing customers before they reach WhatsApp (+ PREVIEW CTA)

**Statut 17 Sep (nuit) : PUBLIÉ sur TikTok le 15/09 à 19:25 — version modifiée par King (34,27 s affichés) — puis mesuré : 156 vues · 6,2 s de lecture moyenne · 18 % de rétention · 4,35 % de visionnage complet · +1 abonné.** Détail : `content/pipeline/ANALYTICS-LOG.md`.
**Instagram + YouTube Shorts : pas encore publiés** → créneaux mer 24 / jeu 25, avec la version **b** ci-dessous.

## Fichiers
| Fichier | Rôle | Specs vérifiées |
|---|---|---|
| `Video_04_Real_Website_PREVIEW.mp4` | master publié sur TikTok (ouverture **figée 4,78 s**) | 34,20 s (audio 34,21) · 1080×1920 · SAR 1:1 · H.264 High · 30 fps · AAC 48 kHz mono |
| **`Video_04b_Animated_Opening.mp4`** | **correctif de l'ouverture** — même script, même voix, même minutage ; le premier beat devient animé (punch 1,2 % en 0,2 s puis push-in lent) | **34,20 s (audio 34,21)** · 1080×1920 · 30 fps · AAC 48 kHz mono · **mouvement 0,0→0,5 s : 0,02 → 13,69** · alignement après la coupe ≤ 0,19/255 vs master |
| `review-opening-avant-apres.mp4` | clip de validation (6 s, sans audio) : 3 s AVANT / 3 s APRÈS | 1080×1920 · 30 fps · 0,93 Mo |

**QA du 17/09 :** décodage FFmpeg OK sur les trois fichiers · images inspectées (b : 0,0 s / 2,4 s / 5,1 s) · **la coupe est au bon endroit** (l'image post-4,78 s est identique au master à ≤ 0,19/255 près).
**Note technique :** `drawtext` **absent** de ce build FFmpeg → les libellés du clip de validation sont posés avec PIL (`overlay`), pas avec drawtext.
**Rappel :** captures navigateur échantillonnées à 15 fps, composées à 30 fps — ne jamais parler de capture native 30 fps.
**Suite :** validation par King → publication IG (mer 24) + Shorts (jeu 25). **Pas de republication TikTok.**
