# ECC — skills d'audit/vérification, installation sélective (installé le 20/10/2026, demande King)

Amont : <https://github.com/affaan-m/ECC> (MIT, release 2.2.3) · épinglé
`6f1881aeafa3c48f7b603cc4be4b2e4e70daad59`. ECC est un « agent harness operating system » :
71 agents, 311 skills, hooks, règles, mémoire, MCP, AgentShield. **Ce qui est installé ici n'est
pas le harnais complet** : c'est l'installation sélective officielle de l'amont, limitée à six
skills d'audit, sans runtime de hooks, sans MCP, sans mémoire activée.

## Ce qui est installé (et ce qui ne l'est pas)

- **Six skills retenus** (cible `claude` de l'installeur amont, miroités dans `~/.agents/skills/`) :
  `accessibility` (WCAG 2.2 AA), `production-audit` (readiness sur preuves locales, score
  0–100 à plafonds), `verification-loop` (rapport PASS/FAIL build/types/lint/tests/sécurité/diff),
  `security-review` (checklist OWASP/secrets/CSP), `seo` (technique + on-page),
  `click-path-audit` (l'état final correspond-il à ce que le bouton promet ?).
- L'installeur résout leurs dépendances : 9 modules, **149 opérations de copie, 76 dossiers de
  skills** dans `~/.claude/skills/` (les bundles `workflow-quality` et `security` tirent leurs
  skills voisins). Aucun `settings.json` modifié, aucun hook enregistré : vérifié sur le plan
  `--dry-run` avant installation, puis `ecc doctor` = OK (checked 1, warnings 0, errors 0) et
  `ecc status` = readiness OK / installHealth healthy.
- **Non installé, volontairement** : le plugin guidé complet (`ecc setup`), les profils
  `core`/`full`, le runtime de hooks, la mémoire ECC, les serveurs MCP, l'App GitHub/Pro,
  l'auto-update. L'amont lui-même interdit d'empiler les méthodes d'installation sur un même
  harnais ; le harnais complet est un choix séparé de King sur sa machine (test personnel
  d'abord — TOOL-SCAN règles 3 et 5).

## Installation (reproductible)

```bash
bash tools/ecc/install.sh
```

Clone épinglé dans `~/.ecc` → dépendances de production du CLI (`npm install --ignore-scripts
--omit=dev`, pour `sql.js`) → installeur officiel sélectif → miroirs `~/.agents/skills/` →
preuves par appels réels (`ecc doctor`, lecture des `SKILL.md` installés). Aucun sudo ; rien de
l'amont dans le dépôt, l'état vit dans `~/.claude/ecc/install-state.json` (hors dépôt).

## Premier usage (20/10) — audit combiné DM Optique v2

`ecc consult` (appel réel) a recommandé la capacité sécurité pour notre requête d'audit ; les
six skills ci-dessus ont ensuite servi de grilles à l'audit combiné (détail :
`clients/dm-optic/build-notes.md`). Score **production-audit : 79/100, « launchable with
caveats »** (plafond 84 appliqué : pas de CI GitHub et chemin critique non testé de bout en
bout avec le client). Vérification-loop : Build PASS · Types N/A (py_compile OK) · Lint maison
PASS (le lint taste reste FAIL sur l'identité figée, par ruling) · Tests PASS · Sécurité PASS
(aucun secret, surface statique) · Diff : outils/docs seulement. Blockers de lancement relevés :
validation client des 40 montures + correspondance stock, domaine client pas encore servi
(Cloudflare = geste de King), ni `404.html` ni en-têtes de sécurité d'hôte dans la sortie.

## Garde-fous AMK

- ECC est une **grille de lecture**, jamais la loi : PRE-FLIGHT, les portiques `tools/qa/`
  et les tests du dépôt font foi. Un score ECC ne remplace ni un portique rouge ni l'œil de King.
- Aucun scanner externe, aucun envoi de code ou de données client à un service tiers sans
  l'accord explicite de King (règle 4) ; `ecc ito`, mémoire, hooks et auto-update restent éteints.
- Ne pas empiler : si King installe un jour le plugin complet sur sa machine, ne pas relancer
  cet installeur sélectif sur la même cible (risque de doublons, documenté par l'amont).
- Règle debout : `PRE-FLIGHT.md` §1f⑥. Production = premier audit relu par King (règle 3).
