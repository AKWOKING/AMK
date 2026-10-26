# CARTE DU DÉPÔT — ce qui existe, où c'est, et ce qui n'est atteignable par aucun chemin

```text
Généré par tools/graphify/build_full_graph.py — 2026-10-26
Source : graphify-out/graph.json (13244 nœuds, 17115 arêtes)
Aucun LLM, aucune clé : la carte ne lit que les fichiers SUIVIS par git — même commit, même
carte, à l'octet (c'est ce que la CI vérifie à chaque push). Rejouable en ~10 secondes.
```

## 0 · En une page

- **13244 nœuds** — dont 824 documents, 202 scripts, 21 modules, 139 pages HTML, 459 images, 6 vidéos, 40 audios, 41 fichiers de données, 11 PDF.
- **3636 citations entre documents** (2954 en chemin exact, 682 par nom unique)
- **157 arêtes de remplacement** · **1 documents marqués périmés**
- **417 documents que personne ne cite** (atteignables par aucun chemin de lecture)
- **Couverture : 1806 fichiers indexés.** Le seul exclu est cette carte (`ops/REPO-MAP.md`, qui se citerait elle-même) et `graphify-out/` (sortie régénérable). Rien d'autre n'est laissé de côté : ni image, ni audio, ni police, ni PDF, ni archive, ni sous-titre, ni fichier de données.

### Les dossiers du dépôt, par poids — et ce que chacun porte

| Dossier | Fichiers | Ce que c'est |
|---|---|---|
| `hosting/` | 314 | Sites déployés et aperçus |
| `tools/` | 289 | Outils et skills installés |
| `content/` | 223 | Contenu, vidéos, carrousels, scripts |
| `clients/` | 211 | Dossiers clients |
| `leads/` | 185 | CRM machine (CSV, records, vues générées) |
| `design/` | 179 | Design, skills, vendor |
| `sales/` | 143 | Vente, prospection, CRM humain |
| `site/` | 80 | Site AMK |
| `ops/` | 47 | Opérations, portiques, facturation |
| `research/` | 31 | Recherche externe (vidéos, articles) |
| `knowledge/` | 26 | Couche connaissance — les règles de référence |
| `brand/` | 25 | Marque AMK |
| `demos/` | 21 | Maquettes et concepts |
| `tryon-camera/` | 9 | Expérimentation |
| `https___amk-cm.vercel.app_-Performance-on-Search-2026-10-08/` | 7 | — |
| `mockups/` | 5 | Captures et mockups |
| `.github/` | 2 | — |
| `docs/` | 2 | — |

## 1 · La couche connaissance — les 10 documents qui font loi

| Document | Titres | Cité par | Son sujet, dans ses propres mots |
|---|---|---|---|
| `knowledge/PRIX-2026-10-24.md` | 11 | 14× | Le prix du socle et de l'entretien — recherche du 24/10/2026 |
| `knowledge/OUTREACH-MESSAGING-2026-10-22.md` | 8 | 10× | Le message qui accroche un gérant de clinique — motifs tirés de trois comptes, 22/10/2026 |
| `knowledge/IDEA-PIPES-2026-10-25.md` | 12 | 9× | LES SIX TUYAUX À IDÉES — d'où vient une idée, avant de savoir si elle est bonne |
| `knowledge/CONTENT-CREATION-2026-10-22.md` | 39 | 8× | Création de contenu — ce que le dépôt sait faire, au 22/10/2026 |
| `knowledge/CONTENT-GAMES-2026-10-25.md` | 12 | 7× | LES CINQ JEUX DE CONTENU — quel jeu nous jouons, et ce que ça change |
| `knowledge/STORY-ARC-2026-10-25.md` | 7 | 7× | L'ARC MODERNE — comment un réel tient 21 secondes |
| `knowledge/HIGH-TICKET-2026-10-26.md` | 12 | 6× | HIGH-TICKET — ce que le document « High-Ticket Lead Gen Agency » vaut pour AMK, et où il s |
| `knowledge/HOOKS-2026-10-25.md` | 13 | 6× | L'ACCROCHE, L'ÉCHELLE ET LA GRILLE — trois sources du 25/10, et une seule pièce refaite |
| `knowledge/OUTREACH-CAMERON-JEANES-2026-10-26.md` | 8 | 6× | La leçon de Cameron Jeanes — ce qu'un message froid doit demander (26/10/2026) |
| `knowledge/OUTREACH-SELF-MADE-2026-10-26.md` | 7 | 5× | Les 14 méthodes de Self-Made Web Designer — ce qu'on prend, ce qu'on jette (26/10/2026) |
| `knowledge/SALES-5-TACTICS-2026-10-26.md` | 12 | 5× | LES CINQ TACTIQUES DE VENTE — ce qui tient dans 25 secondes, ce qui n'y tient pas |
| `knowledge/AUDIT-LOT-1-HUMANIZER-2026-10-26.md` | 8 | 4× | AUDIT HUMANIZER DU LOT 1 — ce qui sonne écrit, et la seule question qui reste |
| `knowledge/HUMANIZER-EP01-2026-10-26.md` | 5 | 4× | HUMANIZER SUR EP01 — les tics trouvés dans la v5, et ce qu'on en a fait |
| `knowledge/MAINTENANCE-CLIENTS-2026-10-22.md` | 11 | 4× | La routine de maintenance clients — quotidien, hebdomadaire, mensuel |
| `knowledge/ROAST-2026-10-24-PRIX-v2.md` | 8 | 4× | Roast Room — séance du 24/10/2026 · « quel prix pour le socle, et pour l'entretien ? » |
| `knowledge/ROAST-2026-10-26-LOT-1-V5.md` | 9 | 4× | Roast Room — séance du 26/10/2026 · « le patron dirait-il oui, cette fois ? » |
| `knowledge/LANDING-FUNNEL-2026-10-23.md` | 18 | 3× | Le tunnel qui convertit — ce qu'on a appris, ce qu'on applique, ce qu'on refuse |
| `knowledge/ROAST-2026-10-26-EP01-VENTE.md` | 11 | 3× | Roast Room — séance du 26/10/2026 · « le CTA d'EP01 fait-il cliquer, et peut-on le savoir  |
| `knowledge/ROAST-2026-10-26-SCRIPT-EP01.md` | 11 | 3× | Roast Room — séance du 26/10/2026 · « le script d'EP01 est-il bon, ou seulement bien accro |
| `knowledge/HOUSE-KNOWLEDGE-BASE.md` | 16 | 2× | HOUSE KNOWLEDGE BASE — la couche de référence |
| `knowledge/MARKETING-OPTICAL-2026-10-22.md` | 19 | 2× | Marketing de l'optique — ce que le dépôt sait, au 22/10/2026 |
| `knowledge/PREUVE-VAGUE-ET-PERMISSION-2026-10-26.md` | 5 | 2× | La preuve vague, et le droit de ne pas construire d'avance (26/10/2026) |
| `knowledge/VIDEOS-2026-10-23-AUDIT.md` | 10 | 2× | Cinq vidéos, deux images — ce qu'on garde, ce qu'on corrige, ce qu'on jette |
| `knowledge/ROAST-2026-10-23-PRIX.md` | 9 | 1× | Roast Room — séance du 23/10/2026 · « faut-il afficher un prix sur le site AMK ? » |
| `knowledge/ROAST-2026-10-26-LOT-1-V2.md` | 9 | 0× | Roast Room — séance du 26/10/2026 · « ce que Google dit de vous » remplace-t-il « ce que G |
| `knowledge/ROAST-2026-10-26-LOT-5.md` | 10 | 0× | Roast Room — séance du 26/10/2026 · « cinq messages, et King cherche avant d'envoyer : bon |

## 2 · Les 20 documents les plus cités — le squelette réel

C'est ce réseau qui décide de ce qui s'applique à un travail. Si un document que vous écrivez n'y entre pas, personne ne le retrouvera.

| Rang | Document | Cité par | Titres |
|---|---|---|---|
| 1 | `sales/Activity-Log.md` | **200** | 280 |
| 2 | `AMK-DESIGN-SKILLS.md` | **41** | 173 |
| 3 | `PRE-FLIGHT.md` | **37** | 41 |
| 4 | `research/YouTube-Lessons.md` | **30** | 202 |
| 5 | `content/strategy/RULE-CREDENTIAL-CLAIMS.md` | **25** | 11 |
| 6 | `sales/RESEARCH-STANDARD.md` | **23** | 15 |
| 7 | `clients/dm-optic/build-notes.md` | **22** | 98 |
| 8 | `sales/CLIENT-MESSAGING-RULES.md` | **21** | 25 |
| 9 | `sales/MESSAGES-2026-09-23-PERSUASION.md` | **20** | 14 |
| 10 | `clients/_uniqueness-registry.md` | **18** | 1 |
| 11 | `clients/dm-optic/pre-launch-checklist.md` | **18** | 22 |
| 12 | `content/lessons/CONTENT-LESSONS.md` | **18** | 43 |
| 13 | `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md` | **18** | 16 |
| 14 | `hosting/previews/README.md` | **17** | 6 |
| 15 | `sales/PRIX-ET-RECURRENCE-2026-09-24.md` | **17** | 16 |
| 16 | `clients/dm-optic/content-plan-month1.md` | **16** | 18 |
| 17 | `content/scripts/README.md` | **16** | 3 |
| 18 | `ops/TOOL-SCAN.md` | **16** | 44 |
| 19 | `content/strategy/TIKTOK-SEO-CHECKLIST-2026-10.md` | **15** | 14 |
| 20 | `sales/research/2026-W43-techniques.md` | **15** | 27 |

## 3 · ⚠️ Documents encore cités alors qu'ils sont marqués périmés

Ce sont les consignes mortes qu'on risque de réappliquer. Chaque ligne est un correctif à faire.

*Détection lexicale* : un document est marqué périmé quand **son propre texte** le dit (en-tête, titre, ou « ce document / cette version … est périmé »). Un document qui *parle* de choses périmées n'est pas périmé — c'est la correction apportée le 24/10 après que `Activity-Log.md` et `AMK-DESIGN-SKILLS.md` ont été signalés à tort. Reste à vérifier au cas par cas : une ligne du tableau n'est pas une preuve, c'est une piste.

| Document périmé | Encore cité par |
|---|---|
| `sales/Walk-In-Batch-2026-09-15.md` | 1 : `Walk-In-Deep-Dives-2026-09-15.md` |

## 3 bis · Ce que personne ne cite — à relire ou à archiver

417 documents n'ont aucune citation entrante. Un orphelin n'est pas inutile : il est **inatteignable**. Soit il faut le citer là où il sert, soit il faut l'archiver.

- **111 à traiter** · 164 dans `design/vendor/` (imports tiers, normal) · 142 dans `leads/records/` (reliés par le CRM, pas par citation)

- **`tools/`** — 49 : `tools/claude-seo/README.md`, `tools/content/README.md`, `tools/docs/README.md`, `tools/geo-seo-claude/README.md`, `tools/humanizer/README.md`, `tools/marketingskills/README.md` … (+43)
- **`content/`** — 20 : `content/Avatar/_composites/busts-694/MEDIA.md`, `content/README.md`, `content/assets/ASSETS.md`, `content/assets/fonts/MEDIA.md`, `content/pipeline/post01/SENTENCE-TIMING-v5d.md`, `content/pipeline/post01/layers/MEDIA.md` … (+14)
- **`clients/`** — 14 : `clients/dm-optic/brag/MEDIA.md`, `clients/dm-optic/content/month1/c1-render/README.md`, `clients/dm-optic/content/month1/w2/etapes-01-validation-client.md`, `clients/dm-optic/content/month1/w2/etapes-01.md`, `clients/dm-optic/content/month1/w2/facebook-post-enfants.md`, `clients/dm-optic/launch/BILAN-PRODUCTION-2026-10.md` … (+8)
- **`ops/`** — 9 : `ops/BRAINSTORM-LOT-1-V2-2026-10-26.md`, `ops/CHANGELOG-VENDREDI.md`, `ops/CHECKPOINT-MARDI-06-10-20H.md`, `ops/HANDOFF-2026-10-26.md`, `ops/POST-WEDNESDAY-2026-10.md`, `ops/START-NEW-CHAT.md` … (+3)
- **`hosting/`** — 4 : `hosting/previews/dmoptic/montures/MEDIA.md`, `hosting/samples/DEPLOY.md`, `hosting/samples/design-research.md`, `hosting/samples/img/MEDIA.md`
- **`sales/`** — 4 : `sales/AMK-Client-Kickoff-Kit.docx`, `sales/Send-UNIVERS-OPTIQUE-2026-09-21-Soir.md`, `sales/Suivi-CAVISA-2026-10-05.md`, `sales/VAGUE-2026-10-12/VERIFIED-LIST.md`
- **`research/`** — 3 : `research/youtube-lessons/2026-10-11-batch-2/INDEX.md`, `research/youtube-lessons/2026-10-11-batch-3/INDEX.md`, `research/youtube-lessons/2026-10-11-batch-4/INDEX.md`
- **`knowledge/`** — 2 : `knowledge/ROAST-2026-10-26-LOT-1-V2.md`, `knowledge/ROAST-2026-10-26-LOT-5.md`
- **`leads/`** — 2 : `leads/M1-EXTRACTION-REPORT.md`, `leads/SCOUT-2026-10-26.md`
- **`site/`** — 2 : `site/SEO-AUDIT-2026-10-23.md`, `site/img/MEDIA.md`
- **`demos/`** — 1 : `demos/img/MEDIA.md`
- **`design/`** — 1 : `design/README.md`

## 4 · Les communautés du dépôt — les sujets, tels que les documents se relient

12 communautés détectées sur le réseau des citations (propagation d'étiquettes, sans aléa). Chaque bloc est un sujet réel : les documents qui s'y trouvent se citent entre eux.

*Le pivot d'une communauté est le document que **les autres membres du groupe** citent le plus (degré interne) — pas le document le plus cité du dépôt, qui l'est partout.*

**581 documents sur 824 sont dans un sujet.** Les 213 autres ne touchent aucune citation — ni entrante, ni sortante : ce sont eux qui se perdent (voir §3 bis). Un sujet se nomme par ses pivots ; un document hors sujet ne se retrouve pas tout seul.

| # | Docs | Les 3 pivots internes | Ce que le groupe a en propre |
|---|---|---|---|
| 0 | 278 | `AMK-DESIGN-SKILLS.md` · `PRE-FLIGHT.md` · `YouTube-Lessons.md` | `sales/` (33 % du groupe) |
| 1 | 146 | `Activity-Log.md` · `Send-BATCH-2026-09-24-Opticiens-2.md` · `Send-BATCH-2026-09-24-Opticiens.md` | `leads/` (89 % du groupe) |
| 2 | 110 | `pre-launch-checklist.md` · `tiktok-01.md` · `content-plan-month1.md` | `clients/` (52 % du groupe) |
| 3 | 20 | `analyst-common.md` · `context-safety.md` · `report.md` | `tools/` (100 % du groupe) |
| 4 | 5 | `claude-code-tools.md` · `codex-tools.md` · `pi-tools.md` | `tools/` (100 % du groupe) |
| 5 | 4 | `PHOTOSHOOT-FICHE-1PAGE-2026-10.md` · `DEMO-SCRIPT-2026-10-07.md` · `VISIT-RUNSHEET-2026-10-07.md` | `clients/` (100 % du groupe) |
| 6 | 4 | `UNIT-ECONOMICS-2026-10.md` · `CONTENT-UNBLOCK-2026-10-05.md` · `FIRST-CLIENT-PRE-MORTEM.md` | `ops/` (75 % du groupe) |
| 7 | 4 | `root-cause-tracing.md` · `defense-in-depth.md` · `condition-based-waiting.md` | `tools/` (100 % du groupe) |
| 8 | 3 | `builder-check-prompt.md` · `visual-companion.md` | `tools/` (100 % du groupe) |
| 9 | 3 | `implementer-prompt.md` · `task-reviewer-prompt.md` | `tools/` (100 % du groupe) |
| 10 | 2 | `etapes-01-PUBLICATION.md` | `clients/` (100 % du groupe) |
| 11 | 2 | `DESIGN.md` | `design/` (100 % du groupe) |

### Communauté 0 — 278 documents

- `AMK-DESIGN-SKILLS.md` — cité 38× dans le groupe, 41× au total
- `PRE-FLIGHT.md` — cité 29× dans le groupe, 37× au total
- `research/YouTube-Lessons.md` — cité 26× dans le groupe, 30× au total
- `sales/RESEARCH-STANDARD.md` — cité 19× dans le groupe, 23× au total
- `hosting/previews/README.md` — cité 14× dans le groupe, 17× au total
- `sales/PRIX-ET-RECURRENCE-2026-09-24.md` — cité 14× dans le groupe, 17× au total

### Communauté 1 — 146 documents

- `sales/Activity-Log.md` — cité 135× dans le groupe, 200× au total
- `sales/Send-BATCH-2026-09-24-Opticiens-2.md` — cité 7× dans le groupe, 10× au total
- `sales/Send-BATCH-2026-09-24-Opticiens.md` — cité 6× dans le groupe, 7× au total
- `sales/Send-Soir-2026-09-23.md` — cité 3× dans le groupe, 4× au total
- `sales/WAVE-TEMPLATE-CURRENT.md` — cité 3× dans le groupe, 3× au total
- `sales/Reponse-CAVISA-2026-09-24.md` — cité 2× dans le groupe, 2× au total

### Communauté 2 — 110 documents

- `clients/dm-optic/pre-launch-checklist.md` — cité 15× dans le groupe, 18× au total
- `clients/dm-optic/content/month1/w1/tiktok-01.md` — cité 12× dans le groupe, 14× au total
- `clients/dm-optic/content-plan-month1.md` — cité 11× dans le groupe, 16× au total
- `clients/dm-optic/build-notes.md` — cité 11× dans le groupe, 22× au total
- `sales/research/2026-W43-techniques.md` — cité 9× dans le groupe, 15× au total
- `clients/dm-optic/a-completer.md` — cité 8× dans le groupe, 12× au total

### Communauté 3 — 20 documents

- `tools/superpowers/skills/diagnosing-superpowers/prompts/analyst-common.md` — cité 8× dans le groupe, 8× au total
- `tools/superpowers/skills/diagnosing-superpowers/references/context-safety.md` — cité 4× dans le groupe, 4× au total
- `tools/superpowers/skills/diagnosing-superpowers/templates/report.md` — cité 3× dans le groupe, 3× au total
- `tools/superpowers/skills/diagnosing-superpowers/templates/case.md` — cité 2× dans le groupe, 2× au total
- `tools/superpowers/skills/diagnosing-superpowers/templates/issue.md` — cité 2× dans le groupe, 2× au total
- `tools/superpowers/skills/diagnosing-superpowers/references/redaction-policy.md` — cité 2× dans le groupe, 2× au total

### Communauté 4 — 5 documents

- `tools/superpowers/skills/using-superpowers/references/claude-code-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/codex-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/pi-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/antigravity-tools.md` — cité 1× dans le groupe, 1× au total

### Communauté 5 — 4 documents

- `clients/dm-optic/photoshoot/PHOTOSHOOT-FICHE-1PAGE-2026-10.md` — cité 2× dans le groupe, 3× au total
- `clients/dm-optic/onboarding/DEMO-SCRIPT-2026-10-07.md` — cité 2× dans le groupe, 2× au total
- `clients/dm-optic/onboarding/VISIT-RUNSHEET-2026-10-07.md` — cité 1× dans le groupe, 1× au total

### Communauté 6 — 4 documents

- `ops/UNIT-ECONOMICS-2026-10.md` — cité 1× dans le groupe, 1× au total
- `content/pipeline/CONTENT-UNBLOCK-2026-10-05.md` — cité 1× dans le groupe, 1× au total
- `ops/FIRST-CLIENT-PRE-MORTEM.md` — cité 1× dans le groupe, 1× au total

### Communauté 7 — 4 documents

- `tools/superpowers/skills/systematic-debugging/root-cause-tracing.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/systematic-debugging/defense-in-depth.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/systematic-debugging/condition-based-waiting.md` — cité 1× dans le groupe, 1× au total

### Communauté 8 — 3 documents

- `tools/superpowers/skills/brainstorming/builder-check-prompt.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/brainstorming/visual-companion.md` — cité 1× dans le groupe, 1× au total

### Communauté 9 — 3 documents

- `tools/superpowers/skills/subagent-driven-development/implementer-prompt.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/subagent-driven-development/task-reviewer-prompt.md` — cité 1× dans le groupe, 1× au total

## 5 · Le reste du dépôt, par nature

| Nature | Fichiers | Où |
|---|---|---|
| document | 824 | `AGENTS.md`, `AMK-DESIGN-SKILLS.md`, `AMK-SEO-PLAYBOOK.md` |
| image | 459 | `brand/AMK-logo-mono.png`, `brand/AMK-logo-mono.svg`, `brand/AMK-logo-primary.png` |
| script | 202 | `brand/build_fb_assets.py`, `clients/dm-optic/launch/facebook-assets/build_cover.py`, `clients/dm-optic/launch/social/build_frame_cards.py` |
| page | 139 | `brand/AMK-Logo-Kit.html`, `brand/v1-green/AMK-Logo-Kit.html`, `clients/dm-optic/brand/CARTE-SIGNATURE-TABLEAU-VISION.html` |
| données | 41 | `clients/dm-optic/content/month1/w1/spot-02.json`, `clients/dm-optic/content/month1/w1/spot-03.json`, `clients/dm-optic/content/month1/w1/ugc-03.json` |
| audio | 40 | `content/pipeline/post01/vo/v5-sentences/s01.mp3`, `content/pipeline/post01/vo/v5-sentences/s02.mp3`, `content/pipeline/post01/vo/v5-sentences/s03.mp3` |
| autre | 21 | `.gitignore`, `design/vendor/LICENSE-bergside`, `design/vendor/LICENSE-emil` |
| police | 21 | `clients/dm-optic/content/month1/w1/assets/fonts/ibm-plex-mono-latin-600-normal.ttf`, `clients/dm-optic/content/month1/w1/assets/fonts/ibm-plex-sans-latin-400-normal.ttf`, `clients/dm-optic/content/month1/w1/assets/fonts/schibsted-grotesk-latin-500-normal.ttf` |
| code | 21 | `content/pipeline/post01/render.mjs`, `ops/amk-factures-pwa/sw.js`, `ops/amk-factures-pwa/test-calculs.mjs` |
| pdf | 11 | `clients/dm-optic/launch/CARTE-AVIS-2026-10-23.pdf`, `clients/dm-optic/launch/RECAP-MISE-EN-LIGNE-2026-10-23.pdf`, `clients/dm-optic/onboarding/print/AMK-PROFORMA-2026-10-05-DM-OPTIQUE-v2.pdf` |
| texte | 10 | `clients/dm-optic/brag/share-copy.txt`, `clients/dm-optic/launch/LISTE-40-MONTURES-WHATSAPP.txt`, `clients/dm-optic/launch/baseline/README.txt` |
| config | 7 | `.github/workflows/deploy-dmoptic.yml`, `.github/workflows/machine.yml`, `hosting/previews/dmoptic/sitemap.xml` |
| vidéo | 6 | `clients/dm-optic/brag/brag.mp4`, `content/reels/ep01/ep01-v4.mp4`, `content/reels/ep01/ep01-v5.mp4` |
| sous-titre | 3 | `clients/dm-optic/content/month1/w1/tiktok-01-v2.fr.srt`, `clients/dm-optic/content/month1/w1/tiktok-01.fr.srt`, `clients/dm-optic/content/month1/w2/etapes-01.srt` |
| archive | 1 | `dmopticsarl-2026-10-21.zip` |
| symboles extraits (titres de documents + fonctions/classes du code) | 11438 | — |

### Les outils et skills installés — 1 dossier = 1 outil

**Point d'entrée** = ce qu'on exécute ou ce qu'on lit en premier. **Contenu** = ce qu'il y a réellement dans le dossier.

| Outil | Point d'entrée | Contenu | Ce qu'il fait |
|---|---|---|---|
| `agency-agents/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | agency-agents (msitarzewski/agency-agents) — 298 personas d'agents |
| `agent-reach/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | AMK — AGENT REACH (outil installé et vérifié) |
| `awesome-claude-design/` | `install.sh` | 1 shell/CI | — |
| `brag/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | AMK — BRAG (vidéos d'annonce, chaîne installée et vérifiée) |
| `claude-seo/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | claude-seo — l'audit SEO outillé (installé le 23/10/2026, demande King) |
| `content/` | `README.md` | 3 script(s) · 1 doc(s) | tools/content — rendu des carrousels Instagram |
| `deploy/` | — | 1 shell/CI | — |
| `design-md/` | `README.md` `install.sh` | 2 script(s) · 1 doc(s) · 1 shell/CI | design-md — codifier un système de design depuis une page réelle |
| `design-motion-principles/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | design-motion-principles — motion d'interface (installé le 20/10/2026, demande King) |
| `docs/` | `README.md` | 1 script(s) · 1 doc(s) | tools/docs — production documentaire AMK (pile libre) |
| `ecc/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | ECC — skills d'audit/vérification, installation sélective (installé le 20/10/2026, demande King) |
| `facture/` | `SPEC-FACTURATION-AMK-2026-10-22.md` | 1 doc(s) | — |
| `geo-seo-claude/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | geo-seo-claude — l'optimisation pour les réponses IA (installé le 23/10/2026, demande King) |
| `graphify/` | `README.md` `install.sh` | 3 script(s) · 1 doc(s) · 3 shell/CI | Graphify — le graphe du dépôt, pour ne plus écrire sans avoir lu |
| `humanizer/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | humanizer — écrire comme un humain (outil copywriting AMK) |
| `hyperframes/` | `README.md` | 1 doc(s) | hyperframes (heygen-com/hyperframes) — le moteur vidéo d'AMK, auditée sur preuves |
| `hypit/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | hypit — moteur vidéo SVML pour agents (outil AMK) |
| `impeccable/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | Impeccable — détecteur d'anti-patterns UI (installé le 20/10/2026, demande King) |
| `marketingskills/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | marketingskills — 52 skills, **amont** coreyhaines31 (basculé le 23/10/2026, ruling King) |
| `moneyprinter/` | `README.md` `install.sh` | 1 script(s) · 1 doc(s) · 2 shell/CI | MoneyPrinterTurbo — installé pour assembler **nos** plans |
| `open-seo/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | open-seo (every-app/open-seo) — skills SEO/AEO en méthodologie |
| `ops/` | — | 10 script(s) · 8 shell/CI | — |
| `outreach/` | `README-MOCKUP.md` | 16 script(s) · 1 doc(s) | — |
| `photo/` | `README.md` `install.sh` | 1 script(s) · 1 doc(s) · 1 shell/CI | tools/photo — édition photo client, locale, pour le web |
| `pro-design/` | `README.md` `install.sh` `SKILL.md` | 2 doc(s) · 1 shell/CI | pro-design — le skill de construction de pages (installé le 23/10/2026) |
| `qa/` | `AUDIT-2026-09-17.md` | 54 script(s) · 4 doc(s) | — |
| `record/` | `NOTICE.md` | 3 script(s) · 1 doc(s) | — |
| `roast-room/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | roast-room — le conseil d'administration qui débat (installé le 23/10/2026, demande King) |
| `scrapling/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | scrapling — scraping/veille (outil AMK, usage par cibles validées) |
| `seo/` | — | 2 script(s) | — |
| `shots/` | `README.md` | 3 script(s) · 1 doc(s) | AMK shot pipeline — hero capture + laptop/phone mockups |
| `site/` | — | 12 script(s) | — |
| `superpowers/` | `README.md` `install.sh` | 2 script(s) · 71 doc(s) · 5 shell/CI | superpowers — la méthode de développement, en 15 skills |
| `taste-skill/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | taste-skill — direction artistique anti-slop (installé le 20/10/2026, demande King) |
| `ugc/` | `README.md` | 3 script(s) · 1 doc(s) | `tools/ugc` — le moteur UGC |
| `ui-ux-pro-max/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | UI/UX Pro Max — intelligence UI/UX consultable (installé le 20/10/2026, demande King) |
| `video/` | `README.md` `install.sh` | 2 script(s) · 1 doc(s) · 2 shell/CI | AMK — CHAÎNE VIDÉO (outils installés et vérifiés) |

### Un dossier client = une ligne — ce qui existe, et s'il y a un brief

| Client | Fichiers | Documents | Brief ? |
|---|---|---|---|
| `dm-optic/` | 187 | 88 | oui |
| `labiomed/` | 1 | 1 | — |
| `le-cristallin/` | 2 | 2 | — |

### Les vidéos — une pièce par dossier, et ce qu'elle contient

| Pièce | Fichiers | Script | Montage | Statut |
|---|---|---|---|---|
| `v01-instagram-vs-website` | 1 | — | — | POSTED (Instagram, 13 views reported) · TikTok unconfirmed |
| `v02-five-website-answers` | 1 | — | — | POSTED — IG 47 · TikTok 87 (King-reported; observation windows not supplied) |
| `v03-part2-three-reasons` | 1 | — | — | POSTED — IG 41 · TikTok 137 (King-reported; observation windows not supplied) |
| `v04-before-whatsapp` | 4 | — | — | PUBLIÉ sur TikTok le 15/09 à 19:25 — version modifiée par King (34,27 s affichés) — puis … |
| `v05-schools` | 1 | — | — | portique mouvement OK, narration incluse → à valider par King (rien n'est publié sans son … |
| `v06-facebook-no-booking` | 15 | oui (MEDIA.md) | 2 fichier(s) | PRÊTE À PUBLIER (master + voix posée + portique passé) · 38,61 s · 1080×1920 · 30 fps … |
| `v07-stock-invisible` | 2 | — | — | — |
| `v08-preuve-ouverte` | 2 | oui (SCRIPT.md) | — | Stage SCRIPTÉ (23/10/2026) — pas de rendu, pas de publication |

## 6 · Où chercher quoi — la table de routage, vérifiée par le graphe

| Sujet | Les 3 documents qu'il faut ouvrir |
|---|---|
| Écrire un message / relancer | `sales/CLIENT-MESSAGING-RULES.md`, `sales/MESSAGES-2026-09-23-PERSUASION.md`, `sales/AMK-Sales-Playbook-v2.md` |
| Prix, grille, remise | `knowledge/PRIX-2026-10-24.md`, `sales/PRIX-ET-RECURRENCE-2026-09-24.md`, `sales/REVUE-CONTRATS-GRILLE-2026-09-23.md` |
| Contenu, vidéo, script | `sales/SOCIAL-ACQUISITION-PLAYBOOK-2026-10-25.md`, `research/youtube-lessons/2026-10-11-batch-3/video-8-tiktok-beginners-guide.md`, `knowledge/HOOKS-2026-10-25.md` |
| Design, page, tokens | `design/WORKFLOW.md`, `knowledge/LANDING-FUNNEL-2026-10-23.md`, `sales/Playbook-Addendum-3-Conversion-Design-2026-09-15.md` |
| Déploiement, QA, portiques | `tools/qa/AUDIT-LESSONS-2026-10-23.md`, `site/OPTIMISATION-2026-10-22.md`, `knowledge/CONTENT-CREATION-2026-10-22.md` |
| Client DM Optique | `clients/dm-optic/pre-launch-checklist.md`, `clients/dm-optic/dossier.md`, `clients/dm-optic/site/CLIENT-REQUIREMENTS-BRIEF.md` |
| Outils et skills | `tools/agent-reach/README.md`, `tools/pro-design/README.md`, `tools/ecc/README.md` |
| CRM, pipeline, activité | `leads/CRM-AUDIT-AND-PROPOSAL-2026-09-18.md`, `leads/records/univers-optique.md`, `leads/CONTRADICTIONS.md` |

## 7 · Les questions qu'on peut poser au graphe dès maintenant

**Étape 0 de tout tour (ruling King 25/10, 141ᵉ message) : le graphe passe avant `PRE-FLIGHT.md`.**

```bash
bash tools/graphify/preflight.sh "le sujet du tour"          # rejoue + lit CETTE carte + nomme les fichiers
bash tools/graphify/ask.sh "message prospect clinique"      # quelles règles lire avant d'écrire
bash tools/graphify/ask.sh "prix grille remise"               # la couche tarifaire
bash tools/graphify/ask.sh "vidéo script accroche"            # la couche contenu
graphify explain "sales/CLIENT-MESSAGING-RULES.md"
graphify path "sales/LISTE-OPTICIENS-2026-10.md" "knowledge/OUTREACH-MESSAGING-2026-10-22.md"
```

---

*Cette carte est générée : ne pas l'éditer à la main. Elle se régénère avec `python3 tools/graphify/build_full_graph.py`.*
