# Video 28 — « Create UNLIMITED Stickman Animations with AI | 100% FREE Forever » — Jacksons AI

URL (résolue par recherche le 12/10 — l'URL du brief `dgCSN-rnN0E` = vidéo 25 du batch 1, doublon) :
https://youtu.be/XZjag0_TiWc · Batch: `research/youtube-lessons/2026-10-12-batch-animation/` · 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: CAPTURÉ PAR CHAPITRES** (chunks 0, 2, 4 sur 5 — couvrent : pitch + branding +
source-PDF, visual flow + bake-off de modèles, montage CapCut + branding chaîne ; chunks 1 et 3 =
détails intermédiaires script/VO non tirés) — `https://youtubetotranscript.com/transcript?v=XZjag0_TiWc`.

- **Producteur :** Jacksons AI (65,7 K abonnés ; YouTube-automation/faceless channels). **Vente :**
  Skool « automation bootcamp » (payant), prompt packet (« Comment 'Prompt' » = engagement-bait),
  Telegram, affiliation — disclaimer earnings dans la description.
- **Metadata (watch page 12/10) :** upload **2026-05-24** · **29:35** · **399 058 vues** · 13 578
  likes · Howto & Style.
- **Evergreen check :** cohérent ; le bake-off de modèles est daté (mai 2026) — les verdicts
  d'outils périment, la méthode reste.
- **Biais :** économie de chaînes-usines à RPM (monétisation YouTube), pas agence ; la vague de
  démonétisation qu'il mentionne (« protect your channel ») est le contexte réel du format.

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | « That Guy » : 42 vidéos → 217 K abonnés, 15 M vues ; Productive Peter 300 K | UNVERIFIED (stats tiers, non liées) | Sert son pitch ; ne planifie pas dessus. |
| 2 | Les modèles « struggle with creative direction » ; le visual flow (ordre des scènes) doit venir de l'humain | PRINCIPE — recoupe V27 (« director's eye ») | Convergent deux producteurs indépendants : la direction ne se délègue pas. |
| 3 | Bake-off multi-shot : Google Vids meilleur rendu, Flow 2ᵉ (structure multi-shot correcte, ~200 crédits gratuits/jour), Higgsfield bon mais payant (VO+SFX inclus), Quen inutilisable (séquence unique, ratio faux), Gemini moyen | VENDOR SELF-REPORT (test montré à l'écran) | Sans objet pour nous (générateurs rejetés) ; utile comme preuve que le rendement des générateurs gratuits est instable. |
| 4 | « 100% FREE Forever » (titre) | PARTIELLEMENT FALSE — Higgsfield payant testé, Skool payant vendu, « free » = freemium à crédits | Pattern déjà loggé : « free & unlimited = signal d'alarme » (Lot [41]). |
| 5 | Protection démonétisation = consistance + originalité | COHÉRENT avec les politiques YouTube | Non vérifié ici ; sans objet (on ne vise pas le RPM). |
| 6 | Animation de démo « faite en 15 minutes » | VENDOR SELF-REPORT (montage final non chronométré) | Illustre le bas de gamme du format : vite fait, qualité « late for work » (son propre humour). |

## 3 · TOOL AUDIT — ORCHESTRATEUR D'ABORD

| Outil | Ce qu'il fait | Alternative libre/OSS | Verdict |
|---|---|---|---|
| DeepSeek | Chatbot gratuit illimité (scripts) | Orchestrateur | REJETÉ (équivalent) |
| Source-PDF 53 pages (niche) | Contexte injecté au chatbot | Notre repo (DESIGN-SKILLS, brief, Lot [42]) | ÉQUIVALENT DÉJÀ EN PLACE — principe : contexte écrit persistant |
| Google Vids / Flow / Gemini / Quen / Higgsfield | Image→vidéo | — | REJETÉS en bloc (générateurs ; instabilité documentée par son propre bake-off ; crédits/paid) |
| ElevenLabs-class VO (étape script→VO) | Voix off | generate_speech voice-00 | REJETÉ (équivalent adopté) |
| YouTube Audio Library | Musique libre | King ajoute la musique au téléversement (ruling 12/10) | SANS OBJET (mais confirme : musique = bibliothèque de la plateforme) |
| CapCut | Montage | ffmpeg | REJETÉ (équivalent) |
| Canva-class (bannière chaîne) | Branding chaîne | SVG/code maison | REJETÉ (équivalent) |

**Principes extraits :** (1) **contexte écrit persistant** avant toute génération (son PDF 53
pages = notre repo) ; (2) **visual flow humain** : l'ordre des scènes se décide avant, pas par le
modèle ; (3) prompts **par chapitres/segments** plutôt qu'un prompt unique géant (= notre beat
table) ; (4) tester le même prompt sur plusieurs moteurs et garder le meilleur — traduit chez
nous : plusieurs variantes de beat, King tranche (at-bats, Lot [42]).

## 4 · GAP-FILLING

- **Le stickman pour AMK ? (question 5 du batch)** : NON. Le format existe et marche (chaînes-usines
  à RPM), mais : (a) il véhicule un registre « contenu d'usine », à l'opposé du positionnement
  premium artisanal d'AMK ; (b) il vit de la monétisation YouTube et traverse une vague de
  démonétisation (son propre aveu) ; (c) l'audience cible d'AMK (opticiens décideurs 35–55) n'est
  pas le public stickman ; (d) la signature visuelle AMK (dark + vert + terminal) est
  incompatible avec des bonshommes bâtons. **Verdict : curiosité rentable pour d'autres, pas un
  format pour une agence sérieuse — REJETÉ comme format, principes de production retenus.**
- **WhatsApp/Cameroun :** le modèle chaîne-usine suppose du volume quotidien — contraire à notre
  cadence de test et à la règle « pas de contenu sans fait de première main ».
- **Contre-preuve :** son propre bake-off montre 2 moteurs sur 5 « inutilisables/moyens » → le
  rendement des générateurs gratuits est une loterie ; notre code→vidéo est déterministe.

## 5 · INTEGRATION RECOMMENDATION — MAPPING

- **ADOPT → méthode :** prompts segmentés par beat (déjà notre beat table) + visual flow décidé
  par l'humain avant production (déjà : King valide le script en chat, ruling 12/10). Rien de
  nouveau à créer — confirmation.
- **ADOPT → discipline :** le « contexte persistant » est notre repo ; à ne jamais remplacer par
  des prompts jetables (rappel dans le brief, déjà couvert par §0).
- **REJETÉ COMME FORMAT → question 5 :** stickman = non (détail §4). Rejoint le journal des rejets
  avec raison documentée.
- **DO NOT ADOPT :** tous les générateurs ; l'engagement-bait « commentez Prompt » (contraire à
  notre règle captions manuelles/ton sobre) ; l'économie RPM.

## 6 · SUMMARY BLOCK

**Core idea.** Le stickman est un format d'usine rentable dans l'économie RPM, bâti sur des
générateurs gratuits au rendement instable et une direction humaine minimale. Pour AMK c'est un
anti-modèle de positionnement — mais sa discipline (contexte persistant, visual flow humain,
prompts segmentés) confirme notre méthode existante.

**KEPT.** Confirmations de méthode uniquement. **REJECTED.** Le format stickman (positionnement) ;
tous les générateurs ; l'engagement-bait ; le titre « 100% FREE » (freemium avéré).
**OPEN.** Rien.
