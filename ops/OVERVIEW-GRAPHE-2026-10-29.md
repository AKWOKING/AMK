# Le graphe, en une page — 29/10/2026

**Ce que c'est.** Un relevé du dépôt tel que `tools/graphify/build_full_graph.py` le voit, pas tel
qu'on s'en souvient. Rejoué ce matin : **14 287 nœuds, 18 826 arêtes, 871 documents**. La carte
complète est `ops/REPO-MAP.md` (régénérée à chaque poussée, vérifiée par la CI) ; ce document-ci est
la vue qu'on garde sous les yeux quand on planifie.

## 1 · La matière

| Type de nœud | Nombre | Ce que c'est |
|---|---|---|
| `heading` | 8 782 | les sections de documents : le grain auquel on cite |
| sans `node_kind` | 4 634 | fichiers, images, assets |
| `page` | 871 | les documents autonomes |

| Type de fichier | Nœuds |
|---|---|
| documents | 10 524 |
| code | 2 450 |
| concepts | 826 |
| rationales (pourquoi) | 487 |

| Relation | Arêtes | Ce qu'elle prouve |
|---|---|---|
| `contains` | 10 545 | la structure (un doc contient une section) |
| **`cites`** | **3 996** | **le chemin de lecture** : qui mène à qui |
| `calls` | 2 087 | le code qui appelle le code |
| `supersedes` | 163 | ce qui remplace quoi (les consignes mortes) |

## 2 · Le poids, par dossier

| Dossier | Fichiers | Rôle |
|---|---|---|
| `hosting/` | 359 | les sites déployés et les aperçus clients |
| `tools/` | 299 | outils et skills installés |
| `clients/` | 256 | les dossiers clients |
| `content/` | 223 | vidéos, carrousels, scripts |
| `leads/` | 189 | le CRM machine |
| `design/` | 180 | design, skills, vendor |
| `sales/` | 153 | vente et prospection |
| `site/` | 80 | **le site AMK** |
| `ops/` | 53 | opérations, portiques, facturation |
| `knowledge/` | 40 | **la couche qui fait loi** |
| `research/` | 31 | recherche externe |

## 3 · Où circule l'information, et où elle s'arrête

**Les douze flux de citation les plus denses** (dossier source → dossier cible) :

```text
leads → leads       129      clients → clients    60      sales → sales     51
tools → tools        32      content → content    20      leads ⇄ sales     36
sales → tools        12      clients → tools      10      research → content 9
ops   → tools         8      ops → ops             8
```

Deux choses à lire dans ce tableau, et une troisième qu'il cache.

1. **Le dépôt se cite surtout lui-même, par dossier.** C'est normal pour des dossiers de travail, et
   c'est un risque : une décision prise dans `clients/` n'atteint `knowledge/` que si quelqu'un
   l'écrit. Les flux croisés existent (`leads ⇄ sales` 36 arêtes, `research → content` 9) mais restent
   minoritaires.
2. **`knowledge/` n'apparaît dans aucun des douze premiers flux.** Les documents qui font loi sont
   cités (`PRIX-2026-10-24.md` 22×, `CONTENT-CREATION-2026-10-22.md` 10×) mais ne citent presque rien :
   la couche connaissance est un puits, pas un carrefour. Ce n'est pas un défaut en soi, c'est une
   raison de plus de passer par `PRE-FLIGHT.md` et `ops/REPO-MAP.md` §6, qui eux routent.
3. **Le plancher est bas.** Les cinq documents les plus cités sont : `sales/Activity-Log.md` (204),
   `leads/CRM.csv` (178), `leads/build/records.py` (149), `leads/build/crm.py` (51),
   `AMK-DESIGN-SKILLS.md` (44). **Le journal et le CRM portent la mémoire du dépôt**, pas la couche
   design. Qui ne lit pas ces deux-là refait le travail de la semaine dernière.

## 4 · Ce qui est inatteignable

**428 documents n'ont aucune citation entrante** (sur 871 pages). Répartition, et ce qu'on en fait :

| Où | Combien | Verdict |
|---|---|---|
| `design/vendor/` | 164 | normal : des imports tiers, lus par un index, pas par citation |
| `leads/records/` | 142 | normal : reliés par le CRM, pas par du texte |
| `tools/` | 49 | **à traiter** : des README d'outils que personne ne cite. Un outil qu'on ne sait pas retrouver est un outil qu'on réinstalle |
| `clients/` | 21 | à citer depuis le dossier client, ou à archiver |
| `content/` | 20 | idem |
| `ops/` | 11 | dont trois brainstormes du 26/10 jamais cités |

**Trois documents sont marqués périmés et encore cités** (dont `sales/Walk-In-Batch-2026-09-15.md`) :
une consigne morte qu'on peut réappliquer sans le savoir.

## 5 · Les skills et les outils, ce qu'il y en a vraiment

**Ce qui est installé dans `tools/` (34 dossiers)** : `qa` (62 scripts de portique), `graphify`,
`video`, `design-md`, `design-motion-principles`, `humanizer`, `roast-room`, `superpowers`, `seo`,
`open-seo`, `geo-seo-claude`, `claude-seo`, `marketingskills`, `ui-ux-pro-max`, `taste-skill`,
`pro-design`, `awesome-claude-design`, `impeccable`, `hyperframes`, `hypit`, `photo`, `shots`,
`record`, `outreach`, `facture`, `deploy`, `site`, `ops`, `content`, `docs`, `brag`, `record`,
`agency-agents`, `agent-reach`, `ecc`, `moneyprinter`, `scrapling`, `ugc`.

**Ce qui est installé hors dépôt, donc perdu à chaque nouveau bac** :
`~/.agents/skills/hallmark` (v2.0.0, la seule). La commande est dans `design/HALLMARK.md` § « Où elle
est installée » ; c'est le seul skill dont l'absence casserait une procédure écrite.

**Ce qui est vendorié dans `design/vendor/`** : 67 familles `bergside-skills` + `emil` + `taste`, avec
un digest machine (`registry-digest.json`).

**Ce qui n'est ni l'un ni l'autre** : `pro-design/`, `awesome-claude-design/`, `taste-skill/` et
`impeccable/` existent en double, une fois à la racine du dépôt et une fois sous `design/vendor/` ou
`tools/`. Ce sont des copies de skills, pas des outils maison : elles ne se mettent pas à jour.

## 6 · Ce que ce relevé change dans la journée

1. **Le graphe dit que la priorité n'est pas le contenu, c'est l'atteignabilité.** 428 orphelins, dont
   49 outils et 11 brainstormes. Avant d'écrire un document de plus, citer ceux qui existent.
2. **Deux documents portent tout** : `sales/Activity-Log.md` et `leads/CRM.csv`. Toute session qui les
   saute repart de zéro, avec l'impression du contraire.
3. **`knowledge/` ne citant presque rien, elle ne se met pas à jour toute seule.** Une décision qui
   n'est pas recopiée dans `knowledge/` ou dans `PRE-FLIGHT.md` reste dans un dossier client, donc
   reste invisible à la session suivante.

> **Piège vérifié en écrivant ce document** : la carte ne lit que les fichiers **suivis** par git.
> Ce fichier, écrit mais pas encore `git add`, valait **zéro nœud** (14 287 avant, 14 287 après).
> Après `git add` : **14 296 nœuds**, dont ses 9 sections. Un document non suivi n'existe pas pour la
> carte, donc pas pour la session suivante.

```bash
# rejouer ce relevé
python3 tools/graphify/build_full_graph.py
python3 tools/graphify/find.py "avis google" --top 5
bash tools/graphify/preflight.sh "sujet du tour"
```
