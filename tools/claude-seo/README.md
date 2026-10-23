# claude-seo — l'audit SEO outillé (installé le 23/10/2026, demande King)

Amont : <https://github.com/AgriciDaniel/claude-seo> · **MIT** · épinglé `219ff485bb016314bb4c15bfc7978df61c668a4f`
(release **v2.5.0**, 22/10/2026) · 19 729 ★ au moment de l'audit.

## Ce que c'est

Un skill Claude Code (`~/.claude/skills/seo`) de 26 sous-skills et 19 sous-agents : SEO technique,
E-E-A-T, schéma, GEO/AEO, « agent readiness » (Lighthouse agentique, WebMCP, `llms.txt`), backlinks,
SEO local, e-commerce, international, Google APIs, rapports PDF/Excel. Trois points d'entrée :
`/seo audit <url>`, `/seo quick <url>`, `/seo report <url>`.

## Ce qui est installé, et ce qui ne l'est pas

- **Installé** : les fichiers du skill + les 19 agents (`~/.claude/agents/seo-*.md`) + un **runtime
  Python isolé** (`~/.claude/skills/seo/.venv`, 3.11) que l'amont crée lui-même, et un miroir
  `~/.agents/skills/seo`.
- **Non installé** : Chromium (téléchargement de ~700 Mo, inutile ici — **aucun navigateur dans la
  sandbox** et l'egress de Chromium est fermé ; les fonctions de page rendue resteront indisponibles).
  `ms-playwright` a été supprimé après l'installation pour ne pas laisser 765 Mo inutiles.
- **Non branché** : aucun hook dans `settings.json` — vérifié, le fichier n'existe pas après
  installation. Les scripts de `hooks/` sont présents mais jamais enregistrés.
- **Extensions de données live** (DataForSEO, Google APIs, Bing, Common Crawl…) : présentes, **sans
  identifiants**. Elles ne fonctionnent qu'après que King a saisi ses clés ; aucune clé n'est demandée
  ici, et aucune donnée client ne sort tant qu'elles sont vides.

## Preuve d'installation (appel réel)

```
$ bash ~/.claude/skills/seo/scripts/claude-seo doctor
Runtime: ready
Install mode: manual
Python: 3.11
Chromium: not installed
```

## Coût et limites

Gratuit. Le seul coût est le disque hors dépôt (~12 Mo de clone, ~1,4 Mo de skill + venv exclu des
sauvegardes). **Limite honnête** : un skill est un **prompt outillé**, pas un verdict — sur nos pages,
les portiques maison (`tools/qa/audit_seo.py`, `audit_html.py`, `audit_a11y.py`) restent la référence,
et leurs résultats ne sont pas remplacés par ceux de l'amont.

Réinstallation : `bash tools/claude-seo/install.sh` (idempotent, sans sudo).
