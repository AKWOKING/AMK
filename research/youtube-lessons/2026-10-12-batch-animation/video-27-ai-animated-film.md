# Video 27 — « How to Make a Professional AI Animated Film » — Curious Refuge

URL (vérifiée 12/10 — c'était l'URL du slot 8 du brief) : https://youtu.be/aVfawxDj6uw ·
Batch: `research/youtube-lessons/2026-10-12-batch-animation/` · 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: INTÉGRAL** (chunks 0–2 sur 4 ; le chunk 3 = queue du site de transcript) —
`https://youtubetotranscript.com/transcript?v=aVfawxDj6uw`.

- **Producteur :** Curious Refuge (école de cinéma IA, 277 K abonnés). **Vente :** cours « AI
  Animation » (model training, voice actors, directing), newsletter, blog → biais formation cinéma.
- **Metadata (watch page 12/10) :** upload **2025-10-28** · **19:42** · **172 032 vues** · 4 511
  likes · Entertainment.
- **Evergreen check :** **PARTIEL** — upload oct. 2025, outils datés (Veo « VO3.1 », Nano Banana,
  Topaz) ; les ÉTAPES du workflow restent valables, les VERSIONS d'outils non. Re-daté : principes
  valables, stack périmé.
- **Biais :** démo sur un film narratif (personnages, dialogues, lip-sync) — très loin d'une vidéo
  TikTok de preuve métier ; le « professionnel » vise le court-métrage, pas le contenu social.

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | « Sora : weird, inconsistent, application not the best for professional projects » (son propre test montré à l'écran) | VERIFIED PAR SA PROPRE DÉMO (« AI fever dream », ses mots) | Recoupe notre journal des rejets : hype d'outil ≠ usage pro. |
| 2 | Cohérence des personnages via image de référence (Nano Banana, 8 refs max, quantity 4, prompting simple d'abord) | MÉTHODE (sa pratique) | La fragilité de la cohérence générative est confirmée par V29 (perte de cohérence scène 8–10). |
| 3 | « ~12 générations avant de trouver LE shot qui m'excite » (Google Veo) | VENDOR SELF-REPORT | Chiffre clé : le rendement réel de la vidéo générée ≈ 1/12 — coût caché du format. |
| 4 | Audio rough cut AVANT l'animation (« beats set in stone », permet le lip-match) | PRINCIPE SOLIDE (pratique d'animation classique) | Exactement notre séquence : beats + VO définis avant render. |
| 5 | Shot list = un tableur (« most professional projects just use a spreadsheet ») | VERIFIED (pratique standard) | Notre beat table dans la spec POST-01 = déjà conforme. |
| 6 | Lip-sync : ADR avec l'acteur plutôt que les outils tiers (« Act 2 and others… not that good ») | OPINION ÉTAYÉE | Sans objet pour nous (pas de personnages) ; note : même l'école de cinéma préfère l'humain. |
| 7 | « Problems with this workflow? Yeah, definitely… the director's eye is the skill » | AVEU HONNÊTE | Confirme : la valeur est dans la direction, pas l'outil. |

## 3 · TOOL AUDIT — ORCHESTRATEUR D'ABORD

| Outil | Ce qu'il fait | Alternative libre/OSS | Verdict |
|---|---|---|---|
| ChatGPT (idées) | Brainstorm scénario | Orchestrateur | REJETÉ (équivalent) — principe gardé : l'humain injecte la créativité |
| Midjourney | Images de base | — | REJETÉ (payant ; pas de besoin : nos visuels sont du code/SVG) |
| Freepik + Nano Banana | Cohérence personnages/scènes par référence | — | REJETÉ (agrégateur payant ; sans objet : pas de personnages) |
| Google Veo/Flow | Image→vidéo animée | — | REJETÉ (payant/crédits ; artéfacts documentés par lui-même : pluie DANS le restaurant, zoom forcé) |
| Topaz Gigapixel / Video AI | Upscale | Rendu natif à la bonne résolution (notre render) | REJETÉ — le code→vidéo n'a PAS besoin d'upscale (résolution déterministe) |
| Tableur (shot list) | Organisation des plans | Beat table POST-01 (markdown) | ÉQUIVALENT DÉJÀ EN PLACE |
| NLE (montage) | Assemblage + coupe autour des artéfacts | ffmpeg (mux) | ÉQUIVALENT DÉJÀ EN PLACE |

**Principes extraits :** (1) **l'histoire d'abord**, l'outil ensuite (« most info online is
marketing fluff ») ; (2) **audio verrouillé avant l'animation** ; (3) **shot list écrite** avant
toute génération ; (4) **storyboard cut** : monter les images fixes AVANT d'animer, pour
réordonner/couper à coût zéro ; (5) le **directeur** (œil du détail) est la compétence réelle ;
(6) proxy d'abord, upscale après (économie) — traduit chez nous : rendu de validation court avant
rendu final (pratique déjà en place : le gate sur clip ≥6 s).

## 4 · GAP-FILLING

- **Faceless :** workflow entièrement sans visage à l'écran (personnages animés) — mais exige
  acteurs vocaux + ADR : incompatible avec notre ruling « pas de voix d'auteur » SAUF notre VO
  voice-00, qui ne porte pas de personnage. Conclusion : le format film narratif n'est pas le
  nôtre ; ses ÉTAPES de discipline (histoire → audio → shot list → storyboard) oui.
- **Cameroun/coût :** le rendement 1/12 (claim 3) × crédits payants × itérations = coût réel
  incompatible avec « pas d'achat sans profit » ; notre code→vidéo a un coût marginal ~0.
- **Contre-preuve :** ses propres artéfacts (pluie en intérieur, zoom non voulu) montrent que la
  vidéo générée image-par-image demande un montage correctif permanent — exactement ce que notre
  architecture déterministe évite.

## 5 · INTEGRATION RECOMMENDATION — MAPPING

- **ADOPT → méthode de production (question 4 du batch) :** ordre imposé pour chaque post :
  histoire/beat table → VO+SFX verrouillés → storyboard cut (stills des beats montés en
  validation) → render final. POST-01 v4 suivait déjà cet ordre ; le formaliser dans la spec.
- **ADOPT → vocabulaire :** « storyboard cut » = notre revue de stills par beat (déjà une
  discipline debout) — renommée et gravée dans la spec comme étape nommée.
- **ADOPT → argument de format (question 6) :** son aveu « problems? yeah, definitely » +
  artéfacts documentés = la preuve que « généré image-par-image » et « généré par code » sont deux
  mondes : le nôtre est déterministe, rééditable, sans upscale.
- **DO NOT ADOPT :** tout le stack payant (Midjourney, Freepik, Veo, Topaz) ; le format film
  narratif avec personnages ; l'ADR.

## 6 · SUMMARY BLOCK

**Core idea.** Une animation « pro » est une discipline de production (histoire → audio verrouillé
→ shot list → storyboard cut → direction), quel que soit l'outil ; la génération image-par-image
coûte ~12 essais par plan et un montage correctif permanent. AMK n'adopte aucune de ses briques
payantes, mais grave sa séquence de production — que notre pipeline suit déjà.

**KEPT.** Séquence histoire→audio→shot list→storyboard cut ; storyboard cut = étape nommée ;
l'œil du directeur comme compétence réelle. **REJECTED.** Tout le stack payant ; le format film ;
Sora/Veo pour nous. **OPEN.** Rien — la vidéo confirme plus qu'elle n'ouvre.
