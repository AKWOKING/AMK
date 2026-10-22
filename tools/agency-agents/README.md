# agency-agents (msitarzewski/agency-agents) — 298 personas d'agents

**Problème nommé (20/10, demande King) :** la couche « expertises ponctuelles » était à construire
à chaque tâche ; le repo amont fournit 298 personas testées par division (design, engineering,
marketing, sales, security, testing, healthcare…), format frontmatter natif Claude Code.
**Licence :** MIT. **Pin :** `4e3ac3ca6604c75113f52c695dbddcc7af928b46` (main au 20/10).

## Ce qui est installé

- `~/.agents/agency-agents/` — les 19 divisions copiées telles quelles (298 `.md`, tous avec
  frontmatter vérifié).
- `~/.claude/agents/` — **fusion non destructive** (copie par-dessus, ne supprime rien d'existant)
  pour la découverte native Claude Code (`/agents`).

Persona « template » ≠ loi maison : un persona ne peut ni restyler une identité figée, ni
contourner les portiques §1b, ni décider un déploiement (§1f③). Il **informe** l'orchestrateur ;
les décisions restent à King. Personas déjà utiles identifiés le 20/10 :
`marketing-aeo-foundations` (checklist AEO — utilisé pour le test DM), `marketing-seo-specialist`,
`testing-accessibility-auditor` et `design-ui-finish-gate-reviewer` (doublent ECC accessibility /
taste — consultés en renfort, jamais en remplacement), `specialized-chief-of-staff` (miroir du rôle
d'orchestrateur).

## Installation

```bash
bash tools/agency-agents/install.sh    # épinglé ; clone + copie, hors dépôt
```

## Règles TOOL-SCAN appliquées

Règle 3 : les personas sont du texte de méthodologie — aucune sortie ne part en production ni au
client sans validation de King. Règle 4 : aucune donnée client dans un prompt de persona
(anonymiser si un cas l'exige). Règle 5 : un seul état maintenu — le pin de cet installeur
(mise à jour = changer le pin ici, jamais `git pull` dans le clone).
