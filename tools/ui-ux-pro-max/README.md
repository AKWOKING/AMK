# UI/UX Pro Max — intelligence UI/UX consultable (installé le 20/10/2026, demande King)

Amont : <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill> (MIT) · épinglé
`56ea9cf174ed86786187daa9de0e6247cb0747e4` (version du plugin amont 2.15.0). Un skill principal
**`ui-ux-pro-max`** (+ skills satellites de l'amont non installés : banner-design, brand,
design-system, design, slides, ui-styling) : base locale interrogeable — 79 styles, 192 palettes,
74 paires de polices, 119 règles UX, icônes, presets GSAP, 22 stacks.

## Ce que c'est

- `scripts/search.py "<query>" --domain ux|typography|landing|icons|gsap|google-fonts…` :
  recherche locale (Python stdlib, **aucun réseau, aucun paquet**) qui renvoie des règles avec
  Do/Don't, exemples de code et sévérité.
- `--design-system` : génère une direction complète (pattern, style, couleurs, typo, effets,
  anti-patterns, checklist pré-livraison). **Voir la limite posée ci-dessous.**

## Installation (reproductible)

```bash
bash tools/ui-ux-pro-max/install.sh
```

Clone épinglé dans `~/.ui-ux-pro-max-skill`, liens vers `~/.claude/skills/` et
`~/.agents/skills/`, preuve par appel réel de `search.py` (requête générique hors projet).
Aucun sudo, rien de l'amont dans le dépôt.

## État dans cette sandbox (vérifié le 20/10, appels réels)

- ✅ Clone au pin `56ea9cf`, liens résolus ; `search.py` répond (`--domain ux`, `--design-system`).
- ✅ Premier usage fait : audit combiné DM v2 — requêtes « hero background image contrast »,
  « fixed bottom bar focus », « mobile filter drawer », « prefers reduced motion infinite
  animation » ; ses règles ont **confirmé nos acquis** (reduced-motion, focus non masqué,
  cibles ≥ 44 px, reflow des chips déjà en flex-wrap) et cadré les correctifs F1–F5.

## Limite posée le 20/10 (verrous client)

Sa commande `--design-system` **propose une identité neuve** (style, palette, typographie —
sur DM elle a sorti « Claymorphism / teal / Varela Round »). Sur un site à identité figée
(« mêmes couleurs, même texte, même logo »), cette sortie est **écartée** : l'outil sert de
grille de lecture, jamais de direction. Une identité neuve ne se choisit qu'avec King
(protocole d'unicité §2, `AMK-DESIGN-SKILLS.md`).

## Garde-fous AMK

- Requêtes **génériques seulement** — aucune donnée client dans une query ni dans une sortie
  persistée (règle 4 TOOL-SCAN ; l'amont l'écrit aussi dans son SKILL.md).
- En cas de conflit avec taste-skill ou `AMK-DESIGN-SKILLS.md`, les lois maison gagnent ;
  on signale à King, on ne tranche pas en silence.
- Règle debout : `PRE-FLIGHT.md` §1f⑦. Production = première application relue par King
  (TOOL-SCAN règle 3).
