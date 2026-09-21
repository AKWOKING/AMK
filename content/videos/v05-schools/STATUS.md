# V-05 — « Un parent cherche votre école » (FR) · **PREMIÈRE VIDÉO AVEC NARRATION**

**Produite le 17 Sep 2026 (nuit).** Statut : **portique mouvement OK**, narration incluse → **à valider par King** (rien n'est publié sans son accord).

**Deux versions, les deux validées par le portique mouvement :**
| Fichier | Langue | Durée | Taille | Destination |
|---|---|---|---|---|
| `Video_05_School_WhatsApp_v1.mp4` | **FR** (narration française) | 23,9 s | 3,69 Mo | **TikTok** (créneau 18:00–20:00) |
| `Video_05_School_WhatsApp_EN.mp4` | **EN** (narration anglaise) | 22,1 s | 3,53 Mo | **Instagram Reels** (créneau 12:00–14:00) |

1080×1920 · 24 fps · H.264 High · AAC 44,1 kHz mono · **narration dans le fichier** (aucun son à ajouter à la publication).

## Ce qu'elle corrige, par rapport à tout ce qui a été publié jusqu'ici
1. **La page est réellement filmée** — vraie capture d'écran de `site/sample-secondary.html` (Crestwood College, maquette **fictive et publique**, déjà en ligne sur `amk-cm.vercel.app`) : plus de diaporama.
2. **Narration complète** (`voice-00`, ré-auditionnée ce soir — c'est l'outil de voix de la plateforme, celui des vidéos précédentes).
3. **Aucun texte tronqué** — une version précédente coupait « VOILÀ CE QU'IL TROUVE » ; corrigé (retour à la ligne des cartes).
4. **Mouvement vérifié partout** : `tools/qa/audit_video_motion.py` → **OK**, aucune fenêtre de 2 s figée.

## Structure (24 s)
| Temps | Contenu | Narration |
|---|---|---|
| 0 – 6,5 s | hook animé « Un parent cherche votre école / VOILÀ CE QU'IL TROUVE » | « Un parent cherche votre école sur son téléphone. Voilà ce qu'il trouve. » |
| 6,5 – 16,3 s | **capture réelle** : accueil, programmes, GCE O/A, bilinguisme, frais, admission | « Les classes, les frais, l'internat, l'admission : tout est lisible, en français comme en anglais. La demande d'inscription part sur WhatsApp, déjà rédigée. » |
| 16,3 – 18,8 s | payoff « TOUT EST LISIBLE. INSCRIPTION SUR WHATSAPP. » | (respiration) |
| 18,8 – 24 s | carte CTA « DM PREVIEW » | « La même page pour votre école ? Envoyez PREVIEW en message privé. » |

**Étiquette de fiction** sur chaque image capturée : « CRESTWOOD COLLEGE (FICTIF) · DÉMONSTRATION » (règle de King : aucun nom réel sans autorisation écrite).

**Sources :** captures `/tmp/capA` + `/tmp/capB` (recapturables) · narration `narration/01-hook.mp3`, `02-body.mp3`, `03-cta.mp3` · commandes exactes dans `content/scripts/v05-schools.md`.

**Suite :** validation de King → **ven 18 à 18:00–20:00 (TikTok FR)** puis **sam 19 à 12:00–14:00 (Reels IG EN)**. Rien n'est publié sans son accord.
