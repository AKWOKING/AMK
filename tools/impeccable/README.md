# Impeccable — détecteur d'anti-patterns UI (installé le 20/10/2026, demande King)

Amont : <https://github.com/pbakaus/impeccable> (Apache-2.0) · épinglé
`46b822f7dda9f7dba799a9c7776fdc19b3a93559` (skill v0.1.16, moteur engine 0.1.16). 1 skill,
24 commandes de design (audit, critique, polish, harden, animate…) et **61 règles déterministes**
d'anti-patterns UI exécutables sans IA par le moteur binaire.

## Ce que c'est

- `impeccable detect --json <fichiers|dossier|url>` : scan des anti-patterns (texte fonctionnel
  < 11 px, padding écrasé, niveaux de titres sautés, polices galvaudées, easing daté…).
  Sortie JSON (stdout) + texte (stderr) ; rc 0 = rien trouvé, rc 2 = findings.
- Le moteur est un **binaire autonome** (~21 Mo) résolu par le lanceur du skill
  (`scripts/impeccable`, cache `~/.impeccable/bin/<version>/`).
- Les autres commandes (polish, harden, critique, live…) sont **documentées mais non
  activées ici** : ce sont des flux de travail de design qui demandent un cadrage
  (PRODUCT.md/DESIGN.md) et l'accord de King (§4b).

## Installation (reproductible)

```bash
bash tools/impeccable/install.sh
```

Clone épinglé dans `~/.impeccable-src`, lien skill vers `~/.claude/skills/` et
`~/.agents/skills/`, moteur `0.1.16` dans `~/.impeccable/bin/`. Dans cette sandbox l'egress
`github.com/pbakaus/impeccable/releases/download` est bloqué : le moteur vient du **paquet npm
officiel de l'amont** `@impeccable/cli-linux-x64@0.1.16` (registry autorisée ; c'est le même
artefact que l'installeur `npx impeccable install`, dont c'est la dépendance optionnelle
déclarée). Sur la machine de King, le lanceur amont télécharge le moteur depuis les releases
GitHub signées tout seul. Aucun sudo, rien de l'amont dans le dépôt.

## Ce qui n'est PAS installé

- **Aucun hook** Impeccable (ni `~/.claude/settings.json`, ni `.claude/hooks.json` projet,
  ni PostToolUse) : le détecteur ne tourne que quand on l'appelle. L'activer en hook automatique
  = décision séparée de King.
- Pas de `PRODUCT.md` ni de `DESIGN.md` dans le dépôt (fichiers debout → §4b).
- Pas d'installation « provider » complète de l'amont (`npx impeccable install`) sur cette cible :
  elle écraserait/dupliquerait notre lien épinglé (l'amont interdit d'empiler).

## État dans cette sandbox (vérifié le 20/10, appels réels)

- ✅ Clone au pin `46b822f`, `engine-probe` → `impeccable-engine 0.1.16`,
  `detect --json` exécuté sur 4 pages réelles de DM v2 (32 findings avant correctifs, 31 après —
  détail dans `clients/dm-optic/build-notes.md`).
- ⚠️ Leçon du premier usage : **chaque finding est vérifié dans le code avant correction**. Sur DM,
  28 « cramped-padding » étaient des faux positifs (cartes dont la photo seule touche le bord,
  padding réel 16–18 px), et 2 « undersized-ui-text » visaient le « DOUALA » du h1 (8 px calculés,
  choix d'affichage du titre approuvé).

## Garde-fous AMK

- Les portiques maison (`tools/qa/`) font foi ; Impeccable est un portique **d'appui**.
- Moteur épinglé : on ne suit pas les mises à jour automatiquement ; `impeccable update`/
  `check` restent à la main, après re-review (règle 5).
- Aucune donnée client envoyée à un service distant : `detect` local sur fichiers/URL ;
  pas de télémétrie activée (`telemetry off` par défaut chez l'amont, non modifié ici).
- Règle debout : `PRE-FLIGHT.md` §1f⑧. Production = premier rapport relu par King (règle 3).
