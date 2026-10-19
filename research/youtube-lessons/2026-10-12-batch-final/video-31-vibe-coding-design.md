# Video 31 — « How to Vibe Code a Designer-Level Website in 28 Minutes » — The Next Wave × Meng To

URL (vérifiée 12/10 — l'URL du brief `Fo3lreTdy0g` = la vidéo Mark Ai Guy) :
https://youtu.be/UNqRlRz80Ss · Batch: `research/youtube-lessons/2026-10-12-batch-final/` · 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: CAPTURÉ PAR CHAPITRES** (watch page chunk 0 + chunk 1 sur 4 — couvrent : problème du
design générique, vocabulaire de design complet (layout, styling, couleurs, ombres, typo,
pairing) ; chunks 2–3 = hero/démo Aura, non tirés) —
`https://youtubetotranscript.com/transcript?v=UNqRlRz80Ss`.

- **Producteur :** The Next Wave (podcast HubSpot ; Nathan Lands) × **Meng To** (fondateur
  Design+Code, créateur d'Aura ; « 10 000+ prompts » revendiqués). **Vente :** Aura (son produit),
  guide HubSpot (sponsor), Design+Code → biais démo de son prompt-builder.
- **Metadata (watch page 12/10) :** upload **2025-07-29** · **28:10** · **13 627 vues** · 304
  likes · Science & Technology. (King citait 37,1 K abonnés — cohérent avec la taille de chaîne.)
- **Evergreen check :** PARTIEL — juil. 2025 ; tendances citées (liquid glass, skeuomorphisme
  moderne, fonts Instrument/Geist) datées, mais la MÉTHODE (vocabulaire précis > adjectifs) est
  intemporelle. Re-daté : méthode valable, catalogue d'exemples à rafraîchir.
- **Biais :** toute la démo passe par Aura (payant pour le prompt complet — il l'admet à l'oral).

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | « Les sites vibe-codés se ressemblent tous » car « beautiful » est subjectif → l'LLM sort le générique entraîné (dégradé violet, bold font) | PRINCIPE FORT, vérifiable par l'expérience | Recoupe notre pratique : les specs vagues donnent du générique. |
| 2 | Solution = **vocabulaire de design précis** : layout (hero/card/list/bento/browser-frame), styling (flat/outline/minimalist/glass/iOS/material), accent color, fond = accent désaturé, ombres (none/small/large/« beautiful shadow » sans border), typo (sans/serif/mono/rounded ; pairing serif-titre + sans-corps ; graisse du heading = personnalité ; tracking resserré sur les grands titres) | MÉTHODE OPÉRATIONNELLE | C'est exactement ce que fait notre DESIGN-SKILLS — validation externe de notre standard. |
| 3 | « Single-file HTML/CSS design simplicity » (chap. 05:32) | PRINCIPE — conforme à notre standard maison single-file | Validation externe. |
| 4 | Spline = 3D communautaire gratuit/remixable pour « l'ingrédient qui dé-générise » | VENDOR (mais outil réellement freemium) | Sans objet immédiat (pas de 3D dans POST-01→09) ; noté backlog. |
| 5 | Le prompt-builder complet d'Aura nécessite un compte pro | AVEU (payant) | REJETÉ : notre prompt-engineering vit dans DESIGN-SKILLS, gratuit et maison. |
| 6 | Skuomorphisme « de retour » via liquid glass | TENDANCE DATÉE | Ni adoptée ni rejetée : AMK suit son design system, pas les modes (ruling Lot [43]). |

## 3 · TOOL AUDIT — ORCHESTRATEUR D'ABORD

| Outil | Ce qu'il fait | Alternative | Verdict |
|---|---|---|---|
| Aura (+ prompt builder) | Site builder avec vocabulaire de design intégré | DESIGN-SKILLS + orchestrateur | REJETÉ — notre équivalent existe déjà ; principe absorbé |
| Lovable / V0 | Génération de sites « template-like » | Orchestrateur | REJETÉ (c'est le problème qu'il décrit, pas la solution) |
| Cursor | Éditeur IA | = l'orchestrateur | N/A |
| Spline | Assets 3D communautaires | — | BACKLOG (si un jour une section 3D sur site client) |
| Unicorn Studio | Effets web | Code/CSS | REJETÉ (effet possible en CSS, standard maison) |

**Principes extraits :** (1) **ne jamais prompter avec des adjectifs** (« beautiful »), toujours
avec des tokens de design nommés ; (2) **l'accent color différencie** — sinon c'est violet par
défaut (chez nous : vert AMK, déjà ruling) ; (3) **le fond = accent désaturé** (règle de
construction, pas un choix au hasard) ; (4) **graisse du heading = personnalité** ; tracking
resserré sur grands titres ; (5) **pairing : serif en titre, sans en corps** (lisibilité) ;
(6) **un ingrédient signature** (son blob Spline) suffit à sortir du générique — pas besoin d'en
faire partout.

## 4 · GAP-FILLING

- **Application AMK (question 3 du batch) :** ces règles s'appliquent à **notre propre site** et
  aux sites clients — pas au pipeline vidéo (frozen). Notre DESIGN-SKILLS couvre déjà le
  vocabulaire ; cette vidéo fournit la **checklist de prompt** manquante : quand l'orchestrateur
  génère une page, la spec doit nommer layout/styling/accent/ombre/typo/pairing au lieu
  d'adjectifs.
- **Cameroun :** les sites génériques « template Bootstrap » sont exactement ce que les opticiens
  achètent aujourd'hui (concurrence locale) — notre différenciant se formule avec SON vocabulaire :
  « un ingrédient signature + typo choisie + accent maîtrisé ».
- **Contre-preuve :** sa démo passe par un outil payant pour prouver une méthode gratuite — la
  méthode se suffit à elle-même (il le dit : « you can just write them manually »).

## 5 · INTEGRATION RECOMMENDATION

- **ADOPT → DESIGN-SKILLS (fichier existant, addendum avec pointeur) :** checklist de spec design
  en 6 tokens (layout / styling / accent+fond désaturé / ombres / typo+graisse+tracking /
  pairing) — à utiliser dans toute spec de page générée (notre site, sites clients).
- **ADOPT → argumentaire commercial :** « pourquoi les sites IA se ressemblent » = objection
  prête à l'emploi face aux opticiens qui comparent avec un site à 50 000 FCFA.
- **BACKLOG :** Spline (3D gratuit) si besoin futur ; « ingrédient signature » comme concept de
  différenciation par site client.
- **DO NOT ADOPT :** Aura/Lovable/V0 ; suivre les tendances (liquid glass) au lieu du design
  system ; le format podcast (28 min) comme modèle de contenu.

## 6 · SUMMARY BLOCK

**Core idea.** Le design « niveau designer » par IA ne vient pas de l'outil mais du vocabulaire :
remplacer les adjectifs par des tokens de design précis (layout, styling, couleur, ombre, typo,
pairing) suffit à sortir du générique violet. Notre DESIGN-SKILLS faisait déjà ce pari — il gagne
une checklist de spec en 6 tokens.

**KEPT.** Checklist 6 tokens → DESIGN-SKILLS ; argumentaire anti-site-générique ; ingrédient
signature (backlog). **REJECTED.** Aura/Lovable/V0 ; suivre les modes. **OPEN.** Spline en
backlog 3D.
