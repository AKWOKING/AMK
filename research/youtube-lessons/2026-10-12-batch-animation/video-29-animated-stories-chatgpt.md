# Video 29 — « How to Create Full Animated Stories Using ChatGPT Images » — Emmanuel Crown

URL (résolue par recherche le 12/10 — l'URL du brief `aVfawxDj6uw` = la vidéo Curious Refuge) :
https://youtu.be/9yvQTR2siPM · Batch: `research/youtube-lessons/2026-10-12-batch-animation/` · 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: CAPTURÉ PAR CHAPITRES** (chunks 0, 1 sur 3 — couvrent : chaîne de production
complète, GPT « animation script builder », cohérence ChatGPT images, Kling 1.6 vs 2.0, ElevenLabs,
lip-sync Kling/Runway ; chunk 2 = montage CapCut, non tiré) —
`https://youtubetotranscript.com/transcript?v=9yvQTR2siPM`.

- **Producteur :** Emmanuel Crown (283 K abonnés revendiqués par King ; la vidéo elle-même :
  1 299 171 vues). **Vente :** affiliés (ElevenLabs, Kling, CapCut dans la description), membership
  chaîne, son GPT gratuit (funnel).
- **Metadata (watch page 12/10) :** upload **2025-04-24** · **16:50** · **1 299 171 vues** ·
  49 171 likes · Education.
- **Evergreen check :** **PÉRIMÉ en partie** — avr. 2025 ; il dit lui-même que les GPTs n'ont pas
  le nouveau modèle d'images (workaround décrit) ; Kling 1.6/2.0, Runway Gen 4 = versions datées.
  Re-daté : la STRUCTURE (script→personnages→shot list→prompts→animation→VO→lip-sync) reste,
  le stack non.
- **Biais :** chaque outil de la chaîne est un lien affilié ; le « free » du titre précédent
  (part one) est un freemium à crédits.

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | Chaîne de production : script → character design → shot list → text-to-image prompt → image-to-video prompt → dialogue exact (→TTS) | MÉTHODE SOLIDE — c'est la même chaîne que V27 et que notre beat table | Convergence de trois producteurs indépendants (27, 29, nous). |
| 2 | Cohérence des personnages : la mémoire du chat suffit… jusqu'à la scène 8–10, puis re-upload de l'image de référence | AVEU — la cohérence générative est FRAGILE | Preuve directe pour la question 6 : le généré image-par-image se dégrade ; le code est déterministe. |
| 3 | Kling 1.6 suffit pour la plupart des shots ; 2.0 seulement pour le mouvement rapide (crédits) | VENDOR SELF-REPORT (test montré) | Économie de crédits = coût réel du format, confirmé. |
| 4 | Lip-sync : Kling « not the best », Runway Act One « ultimate… when it works », 125 crédits à vie | VENDOR SELF-REPORT | Sans objet (pas de personnages) ; le « when it works » confirme l'instabilité. |
| 5 | Son GPT « animation script builder » produit tous les prompts d'un coup | VENDOR (outil gratuit = funnel) | Principe retenu : un générateur de prompts structuré par scène — notre spec POST-01 fait déjà ça à la main, avec faits réels. |
| 6 | « Consistent characters and scenes across board » (titre/intro) | CONTREDIT PAR SON PROPRE WORKAROUND (claim 2) | Écart titre/réalité — pattern loggé. |

## 3 · TOOL AUDIT — ORCHESTRATEUR D'ABORD

| Outil | Ce qu'il fait | Alternative libre/OSS | Verdict |
|---|---|---|---|
| ChatGPT + son GPT | Script + prompts structurés | Orchestrateur + spec POST-01 | REJETÉ (équivalent ; et nos scripts viennent de faits réels, ruling debug-in-public) |
| ChatGPT images (GPT-4o images) | Visuels cohérents en mémoire de chat | — | REJETÉ (nos visuels = SVG/HTML déterministes ; pas de personnages) |
| Kling 1.6/2.0 | Image→vidéo, lip-sync | — | REJETÉ (crédits ; artéfacts ; instabilité avouée) |
| Runway Gen 4 / Act One | Animation + lip-sync « naturel » | — | REJETÉ (125 crédits à vie ; « when it works ») |
| ElevenLabs | VO | generate_speech voice-00 (ruling 12/10) | REJETÉ (équivalent adopté ; lien affilié de toute façon) |
| CapCut | Montage | ffmpeg | REJETÉ (équivalent) |

**Principes extraits :** (1) la chaîne script→shot list→prompts segmentés est le standard du
métier (3ᵉ confirmation du batch) ; (2) **la cohérence est le point de rupture** de tout pipeline
image-par-image — le nôtre (mêmes composants HTML/SVG rejoués) n'a pas ce problème par
construction ; (3) l'économie de crédits pilote les choix (1.6 vs 2.0) — chez nous le coût marginal
d'un rendu est ~0 ; (4) un prompt « building block » à éditer, jamais un prompt cru — recoupe V27.

## 4 · GAP-FILLING

- **Faceless :** personnages 3D cartoon + VO = pas de visage humain, compatible en théorie ; mais
  le format « histoire animée » est du divertissement, pas de la preuve métier — hors de notre
  brief de contenu (piliers = craft/debug/secteur).
- **Cameroun :** le stack entier est à crédits payants en USD — barrière directe avec « pas
  d'achat sans profit » ; notre stack est à coût marginal nul.
- **Contre-preuve :** le workaround de cohérence (re-upload scène 8–10) et le « when it works »
  d'Act One sont les meilleurs arguments du batch POUR notre architecture générée-par-code
  (question 6) : déterminisme vs loterie.

## 5 · INTEGRATION RECOMMENDATION — MAPPING

- **ADOPT → question 6 (AI vs generated) :** ses aveux (cohérence qui lâche, lip-sync « when it
  works », crédits) documentent pourquoi AMK dit « généré par notre propre système » et jamais
  « l'IA fait le travail » : notre chaîne est du code déterministe dirigé à la main, pas une
  génération probabiliste retouchée. Traduction éditoriale dans le brief.
- **ADOPT → confirmation question 4 :** la chaîne de production standard (script → plans → audio →
  animation → montage) est la nôtre ; aucune étape à ajouter.
- **DO NOT ADOPT :** tout le stack (affilié, crédits, instable) ; le format histoire animée ;
  le GPT-funnel.

## 6 · SUMMARY BLOCK

**Core idea.** Une histoire animée « complète » par ChatGPT+Kling est une chaîne de prompts
structurés dont le point de rupture est la cohérence (perdue vers la scène 8–10) et le coût en
crédits. Pour AMK, cette vidéo est surtout la meilleure preuve par l'absurde que le généré-par-code
déterministe est le bon choix de format.

**KEPT.** Confirmation de la chaîne de production ; l'argument de cohérence pour la question 6.
**REJECTED.** Tout le stack affilié ; le format histoire animée ; le GPT-funnel.
**OPEN.** Rien.
