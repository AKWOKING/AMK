# OFFRE — Vidéo d'annonce de livraison (« brag ») · service additionnel AMK

> **Acceptée par King le 20/10** (« I accept all propositions »). Ce fichier décrit le service ;
> **le prix reste une décision de King** — jamais fixé par l'orchestrateur (§prix).

## Le livrable

Une **vidéo verticale 15–25 s (1080×1920)** qui annonce le site/le client à son public —
pour statut WhatsApp, page Facebook, TikTok :

- 5 scènes : accroche → le site en mouvement réel (2–3 captures filmées du site **livré**)
  → adresse + contact final ;
- identité du client (couleurs, polices du site livré) ;
- musique de fond **générée ou licenciée** (jamais de piste non documentée) ;
- livrés ensemble : `brag.mp4` (H.264+AAC) · `poster.jpg` (image de couverture) ·
  `share-copy.txt` (le texte d'accompagnement) · `brag-plan.md` (le plan).

## La chaîne (déjà en production)

`tools/video/capture.mjs` (captures réelles du site) → Hyperframes (rendu local HTML→MP4,
Apache-2.0, **0 FCFA par rendu**) → musique générée ffmpeg → portiques : `hyperframes check`
(0 erreur, contraste WCAG AA) → snapshots relus à l'œil → `tools/qa/audit_video_motion.py`
(mouvement dans chaque fenêtre — référence : brag DM Optique du 20/10, 20 s, produit en ~1 h).

## Ce qui est exclu (toujours)

- Toute statistique ou prétention non prouvable ; tout visage généré par IA ; toute marque non
  confirmée par écrit ; la piste musicale embarquée de l'outil amont (licence non documentée).
- Rien n'est **envoyé ni publié** sans validation de King (lecture téléphone = portique final).

## Prix

**À fixer par King.** Repères de coût interne : ~1 h de production, 0 FCFA d'outillage
(tout est local et libre). La valeur client se juge sur les comparables locaux.
