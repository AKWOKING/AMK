# open-seo (every-app/open-seo) — skills SEO/AEO en méthodologie

**Problème nommé (20/10, demande King) :** pas d'outil SEO structuré côté agence — l'audit SEO
se faisait à la main (checklist `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` + greps).
**Licence :** MIT. **Pin :** `8713d7535f82bf7355313b351004b049d6c9e43c` (main au 20/10).

## Ce qui est installé (sélectif)

Les **12 skills markdown** du plugin officiel (`plugins/openseo/skills/`) copiés vers
`~/.agents/skills/open-seo-skills/` : `seo-audit`, `local-seo`, `keyword-research`,
`keyword-clustering`, `competitive-landscape`, `competitor-analysis`, `link-prospecting`,
`ai-visibility-audit`, `ai-prompt-research`, `seo-coach`, `seo-project-setup`, `seo-report`.

Ils servent de **méthodologie de référence** (workflows de recherche, courtlistage, preuves live)
aux audits SEO/AEO des sites clients, en complément des portiques maison qui font foi (§1f⑥).

## Ce qui n'est PAS installé — et pourquoi

L'**application** OpenSEO (TanStack Start + D1/Postgres + worker Cloudflare) exige : `pnpm`,
une clé **DataForSEO payante** (pay-per-call, compte au nom de qui l'ouvre), et un dépôt
self-hosted (Docker ou Cloudflare). Aucune de ces trois décisions n'est prise : c'est un choix
de King (coût récurrent + compte fournisseur). Le site DM n'ayant pas encore de production ni de
Search Console, la partie « données de crawl/positions » n'a de toute façon rien à mesurer.
**Quand King décide du compte :** `docs/DATAFORSEO_API_KEY.md` du dépôt amont + self-host Cloudflare
(documenté dans le dépôt), jamais de clé dans le dépôt AMK.

## Installation

```bash
bash tools/open-seo/install.sh    # épinglé ; clone + copie des 12 skills, hors dépôt
```

## Première utilisation réelle (20/10, site DM Optique — portion gratuite)

Méthodologie `seo-audit` + persona AEO de agency-agents appliquées aux fichiers construits
(`hosting/previews/dmoptic/`) — résultats dans `clients/dm-optic/build-notes.md` :
robots ✓, sitemap 48 ✓, canonical ✓, Optician+FAQPage ✓ (accueil), BreadcrumbList ✓ (sous-pages),
OG ✓, 404/headers ✓ ; **manque `llms.txt`** (proposition au ruling de King). La portion
« crawl live / positions / Search Console » attend la production (F8).
