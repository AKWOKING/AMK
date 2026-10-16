# Video 17 — "How to Make Viral Motion Graphics With AI With 0$ (Turned it into a Skill)" — Jad M.H | AI Automation

URL: https://youtu.be/zke3bTtvmLo · Batch: `research/youtube-lessons/2026-10-12-batch-6/` · Date: 2026-10-12

## 1 · SOURCE CAPTURE

**Transcript: RETRIEVED IN FULL** (2/2 chunks) — `https://youtubetotranscript.com/transcript?v=zke3bTtvmLo`.

- **Producer:** Jad M.H | AI Automation — 5.38K abonnés. **Même producteur, même jour que la
  vidéo 16** (upload 2026-10-04) : déduplication faite — c'est la vidéo « méthode », 16 est
  l'application carousel. Aucun double comptage.
- **Metadata (watch page, 2026-10-12):** **15:47** · **173 420 vues** · **3 759 likes** · People & Blogs.
- **Vente:** communauté Skool gratuite (même modèle que 16) ; « not sponsored » déclaré.
- **Pipeline démontré (identique à 16):** Claude écrit du code (page web par instant) → navigateur
  headless screenshot chaque frame → FFmpeg assemble le MP4. **16 s à 60 fps = 960 screenshots.**
  Framework : HyperFrames (open source). Musique : ACE-Step 1.5 local (MacBook Air 16 Go, ~11 Go disque).
  SFX : générés **par code** (maths qui sonnent comme un woosh), 375 dans le film final.

## 2 · CLAIM AUDIT

| # | Claim | Verdict | Basis |
|---|---|---|---|
| 1 | « Opus 5.5 sorti le 22/09, mon feed n'est que motion graphics » | CLAIM-VIDÉO, non vérifié en externe | Contexte, pas un décideur pour nous. |
| 2 | « One prompt » viral = en réalité ~10 000 caractères + skills + setup | PLAUSIBLE (cité : tweet d'un ingénieur Claude Code) | Self-report tiers ; mais cohérent avec notre expérience. |
| 3 | « Le prompt est 10 % de la vidéo, le setup 90 % » | OPINION CITÉE (article X, 1,7 M vues) | Framing, pas mesure. |
| 4 | Boucle de critique : screenshot de chaque plan → note 1–10 (histoire, compo, motion, typo, sync) → corriger les 3 pires → recommencer jusqu'à ≥8/10 | VERIFIED IN-DEMO | Méthode démontrée, résultats montrés. |
| 5 | « J'ai payé 1 000 $ pour une vidéo comme ça il y a 1 an » / « 163 appels modèles, 7 h » (tiers) | VENDOR SELF-REPORT | Non audité. |
| 6 | Voix off : modèles vocaux gratuits existent en local | VRAI en général | Non démontré ici (ses 3 vidéos sont sans voix). |
| 7 | Tout à 0 $ hors abonnement Claude | VRAI-hors-abonnement | Comme vidéo 16. |

## 3 · TOOL AUDIT

Même table que vidéo 16 (HyperFrames déjà évalué chez nous le 19/09 ; ACE-Step rejeté pour poids ;
skill Skool rejetée). **Aucun outil nouveau par rapport à 16** — la valeur est méthodologique :

1. **Boucle d'auto-critique notée** (note chiffrée par plan, corriger les pires, itérer jusqu'au
   seuil) — c'est notre discipline QA appliquée au rendu vidéo.
2. **Donner une équipe, pas une tâche** (« directeur, scénariste, animateur, compositeur, sound
   designer, ingénieur render ») + **une histoire** — même famille que nos rôles d'orchestrateur.
3. **Ban des défauts** : interdire explicitement le look par défaut (texte centré, fade-in partout,
   les couleurs/fonts des vidéos précédentes).

## 4 · GAP-FILLING

- Coût temps non quantifié (960 screenshots, 12 versions de chanson) ; « Claude worked 12 hours »
  cité pour un tiers — la méthode n'est pas instantanée.
- Rien sur la lisibilité mobile du texte petit à 60 fps compressé.
- Rien sur le FR (typographie, césures).
- **Application Cameroun :** aucune immédiate — nos posts TikTok sont screen-record + VO, pas du
  motion design. La boucle de critique est la seule pièce directement réutilisable, et elle rejoint
  notre QA existante (`tools/qa/`).

## 5 · INTEGRATION RECOMMENDATION

**ADOPT (1 discipline, backlog):** la boucle d'auto-critique notée (≥8/10 par plan, corriger les 3
pires) → notée dans l'addendum Lot [41] du brief TikTok pour tout futur contenu motion/rendu.
**Confirmation sans adoption:** « le prompt est 10 %, le setup 90 % » = reformulation de notre
règle 05/10 (premise-check) et du protocole §8d — déjà en place.
**DO NOT ADOPT:** voir vidéo 16 (mêmes rejets).

## 6 · SUMMARY BLOCK

**Core idea.** Trois vidéos motion graphics de qualité croissante avec Claude : prompt simple →
chanson originale + SFX locaux → court-métrage dirigé avec boucle de critique notée. La progression
ne vient pas du prompt mais du setup (rôles, histoire, critique itérative, ban des défauts).

**KEPT.** Boucle d'auto-critique notée → backlog motion (addendum Lot [41]).
**REJECTED.** Skill Skool, ACE-Step maintenant, tout changement de pipeline.
**OPEN QUESTIONS.** Aucune bloquante.
