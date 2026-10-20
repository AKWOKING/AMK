# scrapling — scraping/veille (outil AMK, usage par cibles validées)

**Audit-before-install (règle debout King), 20/10/2026 — verdict : INSTALLÉ (BSD-3, flux OUI,
vente : composant d'un service de veille).** Ordre King : « audit then install … if it meets
the criteria ».

## Le verdict, en quatre cases

| Question | Réponse |
|---|---|
| **(a) C'est quoi** | Framework Python v0.5 de scraping « adaptatif » : le parser **mémorise les éléments** et les retrouve quand le DOM change ; fetchers statique (curl_cffi, empreinte TLS navigateur) / navigateur (Playwright, stealth) / spiders concurrents (CrawlSpider, SitemapSpider, ShopifySpider…) ; **conformité robots.txt intégrée** (`robots_txt_obey` — câblé au niveau spider/session en 0.5, pas au one-off `Fetcher.get`) ; skill agent **officiel** fourni par l'amont (`agent-skill/`, BSD-3), avec garde anti-injection (`--ai-targeted` en CLI). Déps cœur : lxml, cssselect, orjson, w3lib. 12 Mo. Pin `fd53131` (18/10/2026). |
| **(b) Licence : BSD-3-Clause** (© 2024 Karim Shoair) — lue dans le clone, bibliothèque ET skill. Installable sans réserve. L'`AI_POLICY.md` amont ne contraint pas l'usage : c'est une règle de divulgation pour les contributions au dépôt amont. |
| **(c) Flux : OUI** — ① contrôles approfondis §1c sur des pages publiques de prospects (parsing robuste + re-visites) ; ② **veille concurrentielle mensuelle** pour nos clients (pages publiques des concurrents : offres affichées, pages nouvelles, changements — le parsing adaptatif survit aux refontes) ; ③ vérification NAP/annuaires. Aucune cible par défaut : chaque cible est validée (règles ci-dessous). |
| **(d) Vente : composant** — « rapport de veille concurrentielle mensuel » devient défendable (tarif = décision King) ; l'outil seul ne se vend pas. |

## Règles d'usage AMK (non négociables)

1. **Pages publiques seulement** ; jamais de contenus derrière login.
2. **Jamais Google / Facebook / Instagram** (ToS) — pour ces plateformes : les API officielles ou Agent Reach, rien d'autre.
3. **robots.txt respecté** (le drapeau existe, on l'active au niveau spider) + débit limité (delais entre requêtes) — un serveur de petite taille ne doit pas souffrir.
4. Aucune donnée client ne part nulle part : l'outil ramène des données, il n'en envoie pas.
5. Chaque nouvelle cible est une décision nommée (règle 5 TOOL-SCAN) — le scraping n'est jamais « lancé pour voir ».

## Installation

```bash
bash tools/scrapling/install.sh
```

Clone épinglé `~/.scrapling`, `pip install --user --break-system-packages "scrapling[fetchers]"`,
skill officiel copié vers `~/.agents/skills/scrapling/` + miroir `~/.claude/skills/scrapling/`.

## Limites (honnêtes, testées le 20/10)

- **Sandbox (egress pypi/github uniquement) :** le fetch statique est **prouvé par appel réel**
  (GET `github.com/D4Vinci/Scrapling` → 200, `title` extrait via `.css('title::text').get()`).
- **StealthyFetcher/DynamicFetcher :** exigent des navigateurs téléchargés par `scrapling install`
  (CDNs bloqués depuis le bac — testé : « Executable doesn't exist at ~/.cache/ms-playwright »).
  **Sur la machine de King** (internet complet) : `scrapling install` une fois, et les fetchers
  navigateur + `solve_cloudflare` deviennent disponibles.
- **API v0.5 :** style parsel — `page.css('sel::text').get()` / `.getall()` ; pas de `css_first`.
  Le skill officiel (`~/.agents/skills/scrapling/SKILL.md`) EST la référence d'usage.
- Paquet installé `--user` (volatile : réinstaller via le script après un wipe du bac).
