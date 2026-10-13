# Video 26 — « Comment faire du Motion Design PRO avec Claude Opus 5.5 (guide complet) » — Maxence Tison

URL (vérifiée 12/10 — l'URL du brief `M9Bj4uBMP3A` pointait ailleurs, voir INDEX) :
https://youtu.be/DBQqB8eqpFI · Batch: `research/youtube-lessons/2026-10-12-batch-animation/` · 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: CAPTURÉ PAR CHAPITRES** (chunks 0, 1, 2 sur 4 — couvrent : principe code→vidéo,
méthode 1 prompt, méthode 2 images de marque, méthode 3 vidéo de référence, duel de modèles,
tarifs ; chunk 3 = vente Skool, non tiré) — `https://youtubetotranscript.com/transcript?v=DBQqB8eqpFI`.

- **Producteur :** Maxence Tison (FR, ex-Google/TikTok selon sa propre vidéo ; 600 K followers
  revendiqués). **Vente :** Skool « Génération IA » 87 $/mois, Editing OS (son éditeur à feedback
  frame-par-frame), masterclasses gratuites → funnel complet.
- **Metadata (watch page 12/10) :** upload **2026-10-07** · **23:19** · **88 987 vues** · 2 152
  likes · Education.
- **Evergreen check :** cohérent (modèles cités = génération courante oct. 2026).
- **Biais :** toute la vidéo est une démo de SON système (Editing OS + Skool) ; le duel de modèles
  est fait sur SES briefs, avec le contexte Claude qu'il nourrit depuis des mois (il l'admet
  lui-même comme facteur possible du résultat).

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | « Claude/ChatGPT ne savent pas générer de vidéo ; ils écrivent du code, et le code devient MP4 » (Remotion ou HyperFrames, gratuits) | VERIFIED — c'est exactement notre pipeline POST-01 (render.mjs → MP4) | Recoupe notre évaluation HyperFrames du 19/09 et notre pratique. |
| 2 | « Ce type de vidéo aurait pris des jours et coûté des milliers d'euros » | VENDOR SELF-REPORT (mais corroboré par ses propres captures Malt/Fiverr/agence) | Malt 350–450 €/jour, Fiverr 748–2 000 €/vidéo, agence 4 500–6 000 €/60 s — captures montrées à l'écran, non re-vérifiées ici. |
| 3 | Méthode 2 : à partir de captures d'app (Yuka) + URL du site, un seul passage sort une pub 15–30 s avec VO synchronisée | VENDOR SELF-REPORT (démo vraie, sélection des essais non montrée) | Le principe (assets de marque → vidéo) est transférable ; le « du premier coup » est invérifiable. |
| 4 | Duel : Opus 3.5 > Fable 5.1 > GPT pour le motion | VENDOR SELF-REPORT, single-run, non aveugle | Mais le détail utile est factuel : Fable produit PLUS d'animation et PLUS d'erreurs de design (texte noir sur fond noir, texte coupé à droite) — plus de mouvement ≠ mieux. |
| 5 | « L'argument "impossible de modifier après les retours client" ne tient plus » | VERIFIED pour l'architecture code (la nôtre : HTML + beat table = rééditable) | Notre v1→v4 de POST-01 en est la preuve de première main. |
| 6 | HyperFrames « fait des voix médiocres, robotiques » (d'où Google TTS) | ANECDOTE | Chez nous : voice-00 (generate_speech) a déjà tranché cette question. |

## 3 · TOOL AUDIT — ORCHESTRATEUR D'ABORD

| Outil | Ce qu'il fait | Alternative libre/OSS | Verdict |
|---|---|---|---|
| Remotion | Code React → MP4 | — | REJETÉ (l'orchestrateur fait déjà : render.mjs maison, aucun besoin) |
| HyperFrames (HeyGen) | Code → MP4, skill Claude | — | REJETÉ en adoption (déjà évalué 19/09, non nécessaire) ; **3ᵉ confirmation indépendante** qu'il est l'outil standard du code→vidéo |
| Editing OS (payant, Skool) | Feedback frame-par-frame → régénération | Notre discipline exists : stills de chaque beat + gate motion | REJETÉ — principe absorbé (feedback daté par beat/seconde, pas « c'est moche » global) |
| Google TTS / Flow | VO | generate_speech (voice-00, ruling 12/10) | REJETÉ — équivalent maison déjà adopté |
| Flora, Prompt Motion, What Ships, Pinterest | Inspiration/agrégation | Recherche manuelle ciblée | REJETÉ — le swipe file (Lot [42]) couvre le besoin |
| Claude Opus/Fable, GPT-6 | Le « cerveau » | = l'orchestrateur lui-même | N/A — c'est nous |

**Principes extraits :** (1) trois modes d'entrée selon ce qu'on possède : prompt seul (pas de DA)
/ **images de marque** (DA à respecter) / vidéo de référence (style à reprendre) — AMK est
structurellement en mode 2 ; (2) boucle de feedback frame-par-frame avant de considérer une version
comme finale ; (3) les erreurs de design (contraste, texte coupé, chevauchement) sont LE critère
qui sépare l'amateur du pro — pas la quantité d'animation ; (4) l'architecture code rend le clip
rééditable après retour client — avantage décisif sur la vidéo générée image-par-image.

## 4 · GAP-FILLING

- **Cameroun/WhatsApp :** les tarifs cités (450 €/jour, 4 500 €/60 s) sont FR/US — au Cameroun le
  marché motion est quasi vide : c'est un différenciant de positioning pour les sites clients
  (une section vidéo « faite maison » qu'aucun concurrent local ne livre), pas un tarif à copier.
- **Faceless :** sa méthode ne montre jamais son visage dans les vidéos produites (pubs Yuka,
  Génération IA) — 100 % compatible avec notre ruling.
- **Contre-preuve interne :** son propre duel montre Fable (modèle « supérieur ») produire des
  textes illisibles → la génération sans gate visuel produit du rebut ; notre gate
  (`audit_video_motion.py` + stills par beat) est exactement la pièce qu'il vend (Editing OS).

## 5 · INTEGRATION RECOMMENDATION — MAPPING

- **ADOPT → format (question 1–2 du batch) :** le format AMK est CONFIRMÉ = **2D motion graphics
  code→vidéo** (notre architecture actuelle). Rien à changer au pipeline POST-01→09.
- **ADOPT → gate créatif :** ajouter au contrôle qualité la liste des défauts vus dans son duel :
  texte sur fond de même luminance, texte coupé en bord de cadre, chevauchement texte/image →
  checklist dans la spec POST-01 (déjà partiellement couverte par les stills ; formalisée).
- **ADOPT → méthode de feedback :** notes de retouches datées **par beat/seconde** (« à 10 s, le
  bandeau droite n'est pas lisible ») — format des allers-retours avec King sur les futures
  versions.
- **ADOPT → intelligence marché :** mémo pricing motion (Malt/Fiverr/agence) → utile le jour où
  AMK vend une section vidéo à un client ; rejoint le backlog commercial, pas le contenu TikTok.
- **DO NOT ADOPT :** Editing OS, Skool, Remotion/HyperFrames (besoin déjà couvert), Google TTS.

## 6 · SUMMARY BLOCK

**Core idea.** Le motion design « pro » par LLM n'est pas de la génération vidéo : c'est du code
rendu en MP4, dirigé par une DA et nettoyé par une boucle de feedback frame-par-frame. C'est
littéralement l'architecture que POST-01 utilise déjà — la vidéo valide notre pipeline plus
qu'elle ne nous apprend un outil.

**KEPT.** Confirmation du format code→vidéo ; checklist défauts de design au gate ; feedback
daté par beat ; mémo pricing. **REJECTED.** Tous les outils (couverts par l'orchestrateur) ; le
« premier coup parfait » (single-run non aveugle). **OPEN.** Le mode « vidéo de référence »
(méthode 3) — applicable le jour où King donne une référence de style à imiter.
