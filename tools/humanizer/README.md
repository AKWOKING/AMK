# humanizer — écrire comme un humain (outil copywriting AMK)

**Audit-before-install (règle debout King), 20/10/2026 — verdict : INSTALLÉ (MIT, flux OUI, vente indirecte).**

## Le verdict, en quatre cases

| Question | Réponse |
|---|---|
| **(a) C'est quoi** | Un skill autonome (un `SKILL.md` de 32 Ko, v3.1.0, © Siqi Chen) : réécrit un texte qui « sonne IA » en gardant exactement ce qu'il dit, à partir des 26 motifs de « Signs of AI writing » de Wikipédia (contrastes « not X but Y », chute d'une ligne, triades forcées, tirets partout, inflation, gras décoratif…). Zéro dépendance, zéro réseau, zéro hook : du markdown lu par l'agent. |
| **(b) Flux : OUI** | Le copywriting traverse tout : légendes TikTok, messages clients, texte du site, `share-copy.txt` des brags. Il vient en **second passe** APRÈS la loi maison (§11b + YouTube-Lessons + COPY CRAFT GATE) — jamais à sa place. Premier usage réel le jour même : la bande « Assurances » du site DM (texte passé au crible des 5 motifs les plus forts avant écriture). |
| **(c) Vente : indirecte** | Outil de qualité interne, pas un livrable : il améliore chaque texte vendu (contenu, messages, sites). Ne se vend pas seul. |
| **(d) Licence : MIT** | `LICENSE` MIT (© 2025 Siqi Chen), vérifiée dans le clone épinglé — installable sans réserve. Contraste avec anthropics/skills doc-skills (propriétaires, NON installés — même jour, même règle). |

## Installation

```bash
bash tools/humanizer/install.sh
```

Clone épinglé (`8c307f3`, 16/10/2026) dans `~/.humanizer`, copie du `SKILL.md` vers
`~/.agents/skills/humanizer/` + miroir `~/.claude/skills/humanizer/`. Idempotent, aucun sudo.
L'amont propose `/plugin marketplace add blader/humanizer` (Claude Code) ou `npx skills add` —
**on n'utilise ni l'un ni l'autre** (runtime CLI de plus = état maintenu inutile, règle 5 TOOL-SCAN ;
la copie du SKILL.md est la voie documentée par l'amont même pour les agents inconnus).

## Usage AMK

1. Écrire le texte selon la loi maison (§11b : concret, prouvé, voix du cabinet).
2. Le relire contre les **5 motifs les plus forts** du skill (contraste « not-X-but-Y », chute d'une
   ligne, « vérité profonde », ouverture mise en scène, argument au vent) + les 21 autres au besoin.
3. Hiérarchie inchangée : **lois maison et verrous client gagnent** (règle 1 TOOL-SCAN). La voix
   « l'aveu avant la promesse » et les règles de première ligne (MESSAGES §1) ne se négocient pas.
4. Le skill ne fait pas passer les détecteurs IA et ne le prétend pas (README amont) — ce n'est pas
   le but recherché.
