# CARTE DU DÉPÔT — ce qui existe, où c'est, et ce qui n'est atteignable par aucun chemin

```text
Généré par tools/graphify/build_full_graph.py — 2026-10-24
Source : graphify-out/graph.json (11994 nœuds, 14602 arêtes)
Aucun LLM, aucune clé : la carte ne lit que les fichiers SUIVIS par git — même commit, même
carte, à l'octet (c'est ce que la CI vérifie à chaque push). Rejouable en ~10 secondes.
```

## 0 · En une page

- **11994 nœuds** — dont 766 documents, 165 scripts, 21 modules, 139 pages HTML, 395 images, 8 vidéos, 40 audios, 35 fichiers de données, 11 PDF.
- **2867 citations entre documents** (2280 en chemin exact, 587 par nom unique)
- **121 arêtes de remplacement** · **1 documents marqués périmés**
- **412 documents que personne ne cite** (atteignables par aucun chemin de lecture)
- **Couverture : 1642 fichiers indexés.** Le seul exclu est cette carte (`ops/REPO-MAP.md`, qui se citerait elle-même) et `graphify-out/` (sortie régénérable). Rien d'autre n'est laissé de côté : ni image, ni audio, ni police, ni PDF, ni archive, ni sous-titre, ni fichier de données.

### Les dossiers du dépôt, par poids — et ce que chacun porte

| Dossier | Fichiers | Ce que c'est |
|---|---|---|
| `hosting/` | 312 | Sites déployés et aperçus |
| `tools/` | 254 | Outils et skills installés |
| `clients/` | 193 | Dossiers clients |
| `design/` | 179 | Design, skills, vendor |
| `content/` | 157 | Contenu, vidéos, carrousels, scripts |
| `leads/` | 152 | CRM machine (CSV, records, vues générées) |
| `sales/` | 137 | Vente, prospection, CRM humain |
| `site/` | 79 | Site AMK |
| `research/` | 58 | Recherche externe (vidéos, articles) |
| `ops/` | 34 | Opérations, portiques, facturation |
| `brand/` | 25 | Marque AMK |
| `demos/` | 20 | Maquettes et concepts |
| `knowledge/` | 10 | Couche connaissance — les règles de référence |
| `tryon-camera/` | 9 | Expérimentation |
| `https___amk-cm.vercel.app_-Performance-on-Search-2026-10-08/` | 7 | — |
| `mockups/` | 5 | Captures et mockups |
| `.github/` | 2 | — |

## 1 · La couche connaissance — les 10 documents qui font loi

| Document | Titres | Cité par | Son sujet, dans ses propres mots |
|---|---|---|---|
| `knowledge/PRIX-2026-10-24.md` | 10 | 8× | Le prix du socle et de l'entretien — recherche du 24/10/2026 |
| `knowledge/OUTREACH-MESSAGING-2026-10-22.md` | 8 | 7× | Le message qui accroche un gérant de clinique — motifs tirés de trois comptes, 22/10/2026 |
| `knowledge/CONTENT-CREATION-2026-10-22.md` | 36 | 5× | Création de contenu — ce que le dépôt sait faire, au 22/10/2026 |
| `knowledge/ROAST-2026-10-24-PRIX-v2.md` | 8 | 4× | Roast Room — séance du 24/10/2026 · « quel prix pour le socle, et pour l'entretien ? » |
| `knowledge/MAINTENANCE-CLIENTS-2026-10-22.md` | 11 | 3× | La routine de maintenance clients — quotidien, hebdomadaire, mensuel |
| `knowledge/HOUSE-KNOWLEDGE-BASE.md` | 16 | 2× | HOUSE KNOWLEDGE BASE — la couche de référence |
| `knowledge/LANDING-FUNNEL-2026-10-23.md` | 18 | 2× | Le tunnel qui convertit — ce qu'on a appris, ce qu'on applique, ce qu'on refuse |
| `knowledge/MARKETING-OPTICAL-2026-10-22.md` | 19 | 2× | Marketing de l'optique — ce que le dépôt sait, au 22/10/2026 |
| `knowledge/VIDEOS-2026-10-23-AUDIT.md` | 10 | 2× | Cinq vidéos, deux images — ce qu'on garde, ce qu'on corrige, ce qu'on jette |
| `knowledge/ROAST-2026-10-23-PRIX.md` | 9 | 1× | Roast Room — séance du 23/10/2026 · « faut-il afficher un prix sur le site AMK ? » |

## 2 · Les 20 documents les plus cités — le squelette réel

C'est ce réseau qui décide de ce qui s'applique à un travail. Si un document que vous écrivez n'y entre pas, personne ne le retrouvera.

| Rang | Document | Cité par | Titres |
|---|---|---|---|
| 1 | `sales/Activity-Log.md` | **167** | 240 |
| 2 | `AMK-DESIGN-SKILLS.md` | **39** | 173 |
| 3 | `research/YouTube-Lessons.md` | **31** | 202 |
| 4 | `PRE-FLIGHT.md` | **28** | 40 |
| 5 | `content/strategy/RULE-CREDENTIAL-CLAIMS.md` | **24** | 11 |
| 6 | `sales/RESEARCH-STANDARD.md` | **19** | 15 |
| 7 | `sales/CLIENT-MESSAGING-RULES.md` | **18** | 20 |
| 8 | `sales/MESSAGES-2026-09-23-PERSUASION.md` | **17** | 14 |
| 9 | `sales/PRIX-ET-RECURRENCE-2026-09-24.md` | **17** | 16 |
| 10 | `clients/dm-optic/build-notes.md` | **16** | 89 |
| 11 | `hosting/previews/README.md` | **16** | 6 |
| 12 | `ops/TOOL-SCAN.md` | **16** | 37 |
| 13 | `clients/_uniqueness-registry.md` | **15** | 1 |
| 14 | `clients/dm-optic/content-plan-month1.md` | **15** | 18 |
| 15 | `clients/dm-optic/pre-launch-checklist.md` | **15** | 22 |
| 16 | `content/lessons/CONTENT-LESSONS.md` | **15** | 27 |
| 17 | `content/scripts/README.md` | **15** | 3 |
| 18 | `sales/research/2026-W43-techniques.md` | **15** | 27 |
| 19 | `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md` | **14** | 16 |
| 20 | `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` | **13** | 8 |

## 3 · ⚠️ Documents encore cités alors qu'ils sont marqués périmés

Ce sont les consignes mortes qu'on risque de réappliquer. Chaque ligne est un correctif à faire.

*Détection lexicale* : un document est marqué périmé quand **son propre texte** le dit (en-tête, titre, ou « ce document / cette version … est périmé »). Un document qui *parle* de choses périmées n'est pas périmé — c'est la correction apportée le 24/10 après que `Activity-Log.md` et `AMK-DESIGN-SKILLS.md` ont été signalés à tort. Reste à vérifier au cas par cas : une ligne du tableau n'est pas une preuve, c'est une piste.

| Document périmé | Encore cité par |
|---|---|
| `sales/Walk-In-Batch-2026-09-15.md` | 1 : `Walk-In-Deep-Dives-2026-09-15.md` |

## 3 bis · Ce que personne ne cite — à relire ou à archiver

412 documents n'ont aucune citation entrante. Un orphelin n'est pas inutile : il est **inatteignable**. Soit il faut le citer là où il sert, soit il faut l'archiver.

- **132 à traiter** · 164 dans `design/vendor/` (imports tiers, normal) · 116 dans `leads/records/` (reliés par le CRM, pas par citation)

- **`tools/`** — 50 : `tools/claude-seo/README.md`, `tools/content/README.md`, `tools/docs/README.md`, `tools/geo-seo-claude/README.md`, `tools/graphify/README.md`, `tools/humanizer/README.md` … (+44)
- **`research/`** — 30 : `research/Social-Growth-Synthesis-2026-09-18.md`, `research/youtube-lessons/2026-10-11-batch-1/INDEX.md`, `research/youtube-lessons/2026-10-11-batch-2/INDEX.md`, `research/youtube-lessons/2026-10-11-batch-3/INDEX.md`, `research/youtube-lessons/2026-10-11-batch-4/INDEX.md`, `research/youtube-lessons/2026-10-11-batch-5/INDEX.md` … (+24)
- **`content/`** — 15 : `content/README.md`, `content/assets/ASSETS.md`, `content/pipeline/CONTENT-UNBLOCK-2026-10-05.md`, `content/pipeline/post01/SENTENCE-TIMING-v5d.md`, `content/scripts/v01-instagram-vs-website.md`, `content/scripts/v02-five-website-answers.md` … (+9)
- **`sales/`** — 12 : `sales/AMK-Client-Kickoff-Kit.docx`, `sales/Expansion-Geography-2026-09-18.md`, `sales/PLAN-2026-09-19-21.md`, `sales/PRICING-NEXT-CLIENT-2026-10-22.md`, `sales/Passe-Vitrine-2026-09-23.md`, `sales/Send-Pack-2026-09-18-LOT3.md` … (+6)
- **`clients/`** — 11 : `clients/dm-optic/content/month1/c1-render/README.md`, `clients/dm-optic/content/month1/w2/etapes-01-validation-client.md`, `clients/dm-optic/content/month1/w2/etapes-01.md`, `clients/dm-optic/content/month1/w2/facebook-post-enfants.md`, `clients/dm-optic/launch/BILAN-PRODUCTION-2026-10.md`, `clients/dm-optic/launch/PAIEMENT-SOLDE-ET-RETAINER-2026-10-22.md` … (+5)
- **`ops/`** — 9 : `ops/CHANGELOG-VENDREDI.md`, `ops/CHECKPOINT-MARDI-06-10-20H.md`, `ops/FIRST-CLIENT-PRE-MORTEM.md`, `ops/POST-WEDNESDAY-2026-10.md`, `ops/START-NEW-CHAT.md`, `ops/UNIT-ECONOMICS-2026-10.md` … (+3)
- **`hosting/`** — 2 : `hosting/samples/DEPLOY.md`, `hosting/samples/design-research.md`
- **`design/`** — 1 : `design/README.md`
- **`leads/`** — 1 : `leads/M1-EXTRACTION-REPORT.md`
- **`site/`** — 1 : `site/SEO-AUDIT-2026-10-23.md`

## 4 · Les communautés du dépôt — les sujets, tels que les documents se relient

14 communautés détectées sur le réseau des citations (Louvain, graine fixe). Chaque bloc est un sujet réel : les documents qui s'y trouvent se citent entre eux.

*Le pivot d'une communauté est le document que **les autres membres du groupe** citent le plus (degré interne) — pas le document le plus cité du dépôt, qui l'est partout.*

**517 documents sur 766 sont dans un sujet.** Les 230 autres ne touchent aucune citation — ni entrante, ni sortante : ce sont eux qui se perdent (voir §3 bis). Un sujet se nomme par ses pivots ; un document hors sujet ne se retrouve pas tout seul.

| # | Docs | Les 3 pivots internes | Ce que le groupe a en propre |
|---|---|---|---|
| 0 | 146 | `Activity-Log.md` · `MESSAGES-2026-09-23-PERSUASION.md` · `Send-BATCH-2026-09-24-Opticiens-2.md` | `leads/` (77 % du groupe) |
| 1 | 78 | `PRE-FLIGHT.md` · `TOOL-SCAN.md` · `RESEARCH-STANDARD.md` | `tools/` (33 % du groupe) |
| 2 | 63 | `YouTube-Lessons.md` · `AMK-DESIGN-SKILLS.md` · `FICHE-GOOGLE-PROFILE.md` | `research/` (42 % du groupe) |
| 3 | 63 | `Outreach-Pack-2026-09-14.md` · `Outreach-AFRIQUE-LABO-v1.md` · `KILL-LIST.md` | `sales/` (79 % du groupe) |
| 4 | 60 | `tiktok-01.md` · `pre-launch-checklist.md` · `content-plan-month1.md` | `clients/` (73 % du groupe) |
| 5 | 36 | `CLIENT-MESSAGING-RULES.md` · `a-completer.md` · `RULE-CREDENTIAL-CLAIMS.md` | `clients/` (41 % du groupe) |
| 6 | 24 | `ANALYTICS-LOG.md` · `CONTENT-LESSONS.md` · `2026-09-17-content-handover.md` | `content/` (70 % du groupe) |
| 7 | 20 | `analyst-common.md` · `context-safety.md` · `report.md` | `tools/` (100 % du groupe) |
| 8 | 9 | `claude-code-tools.md` · `codex-tools.md` · `pi-tools.md` | `tools/` (100 % du groupe) |
| 9 | 7 | `PHOTOSHOOT-FICHE-1PAGE-2026-10.md` · `DEMO-SCRIPT-2026-10-07.md` · `VISIT-RUNSHEET-2026-10-07.md` | `clients/` (85 % du groupe) |
| 10 | 4 | `root-cause-tracing.md` · `defense-in-depth.md` · `condition-based-waiting.md` | `tools/` (100 % du groupe) |
| 11 | 3 | `builder-check-prompt.md` · `visual-companion.md` | `tools/` (100 % du groupe) |
| 12 | 2 | `etapes-01-PUBLICATION.md` | `clients/` (100 % du groupe) |
| 13 | 2 | `DESIGN.md` | `design/` (100 % du groupe) |

### Communauté 0 — 146 documents

- `sales/Activity-Log.md` — cité 121× dans le groupe, 167× au total
- `sales/MESSAGES-2026-09-23-PERSUASION.md` — cité 8× dans le groupe, 17× au total
- `sales/Send-BATCH-2026-09-24-Opticiens-2.md` — cité 7× dans le groupe, 10× au total
- `sales/Send-BATCH-2026-09-24-Opticiens.md` — cité 6× dans le groupe, 7× au total
- `sales/PERSUASION-5-NIVEAUX-2026-09-23.md` — cité 5× dans le groupe, 7× au total
- `sales/Send-Soir-2026-09-23.md` — cité 4× dans le groupe, 4× au total

### Communauté 1 — 78 documents

- `PRE-FLIGHT.md` — cité 14× dans le groupe, 28× au total
- `ops/TOOL-SCAN.md` — cité 10× dans le groupe, 16× au total
- `sales/RESEARCH-STANDARD.md` — cité 10× dans le groupe, 19× au total
- `clients/_uniqueness-registry.md` — cité 9× dans le groupe, 15× au total
- `hosting/previews/README.md` — cité 8× dans le groupe, 16× au total
- `clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md` — cité 7× dans le groupe, 11× au total

### Communauté 2 — 63 documents

- `research/YouTube-Lessons.md` — cité 17× dans le groupe, 31× au total
- `AMK-DESIGN-SKILLS.md` — cité 17× dans le groupe, 39× au total
- `sales/FICHE-GOOGLE-PROFILE.md` — cité 10× dans le groupe, 13× au total
- `research/PHOTO-LABO-PIXEL-8A-2026-09-24.md` — cité 10× dans le groupe, 13× au total
- `content/strategy/TIKTOK-SEO-CHECKLIST-2026-10.md` — cité 9× dans le groupe, 13× au total
- `design/WORKFLOW.md` — cité 6× dans le groupe, 10× au total

### Communauté 3 — 63 documents

- `sales/Outreach-Pack-2026-09-14.md` — cité 7× dans le groupe, 9× au total
- `sales/Outreach-AFRIQUE-LABO-v1.md` — cité 6× dans le groupe, 9× au total
- `leads/KILL-LIST.md` — cité 5× dans le groupe, 10× au total
- `sales/Clinic-Batch-2026-09-15.md` — cité 5× dans le groupe, 5× au total
- `sales/AMK-Sales-Playbook-v2.md` — cité 4× dans le groupe, 12× au total
- `sales/Remote-Sweep-1-Douala-2026-09-15.md` — cité 4× dans le groupe, 4× au total

### Communauté 4 — 60 documents

- `clients/dm-optic/content/month1/w1/tiktok-01.md` — cité 10× dans le groupe, 12× au total
- `clients/dm-optic/pre-launch-checklist.md` — cité 8× dans le groupe, 15× au total
- `clients/dm-optic/content-plan-month1.md` — cité 8× dans le groupe, 15× au total
- `content/scripts/README.md` — cité 7× dans le groupe, 15× au total
- `clients/dm-optic/launch/SETUP-FACEBOOK.md` — cité 7× dans le groupe, 10× au total
- `sales/research/2026-W43-techniques.md` — cité 6× dans le groupe, 15× au total

### Communauté 5 — 36 documents

- `sales/CLIENT-MESSAGING-RULES.md` — cité 7× dans le groupe, 18× au total
- `clients/dm-optic/a-completer.md` — cité 7× dans le groupe, 12× au total
- `content/strategy/RULE-CREDENTIAL-CLAIMS.md` — cité 7× dans le groupe, 24× au total
- `clients/dm-optic/site/SPEC-PAGES-v1.md` — cité 6× dans le groupe, 9× au total
- `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` — cité 5× dans le groupe, 13× au total
- `clients/dm-optic/ads/variant-messages.md` — cité 5× dans le groupe, 8× au total

### Communauté 6 — 24 documents

- `content/pipeline/ANALYTICS-LOG.md` — cité 10× dans le groupe, 11× au total
- `content/lessons/CONTENT-LESSONS.md` — cité 6× dans le groupe, 15× au total
- `content/handover/2026-09-17-content-handover.md` — cité 3× dans le groupe, 3× au total
- `content/strategy/POSTING-CALENDAR.md` — cité 3× dans le groupe, 7× au total
- `content/carousels/POST-READY.md` — cité 3× dans le groupe, 6× au total
- `research/HyperFrames-Evaluation-2026-09-19.md` — cité 2× dans le groupe, 4× au total

### Communauté 7 — 20 documents

- `tools/superpowers/skills/diagnosing-superpowers/prompts/analyst-common.md` — cité 8× dans le groupe, 8× au total
- `tools/superpowers/skills/diagnosing-superpowers/references/context-safety.md` — cité 4× dans le groupe, 4× au total
- `tools/superpowers/skills/diagnosing-superpowers/templates/report.md` — cité 3× dans le groupe, 3× au total
- `tools/superpowers/skills/diagnosing-superpowers/templates/case.md` — cité 2× dans le groupe, 2× au total
- `tools/superpowers/skills/diagnosing-superpowers/templates/issue.md` — cité 2× dans le groupe, 2× au total
- `tools/superpowers/skills/diagnosing-superpowers/references/redaction-policy.md` — cité 2× dans le groupe, 2× au total

### Communauté 8 — 9 documents

- `tools/superpowers/skills/using-superpowers/references/claude-code-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/codex-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/pi-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/antigravity-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/hermes-tools.md` — cité 1× dans le groupe, 1× au total
- `tools/superpowers/skills/using-superpowers/references/muse-tools.md` — cité 1× dans le groupe, 1× au total

### Communauté 9 — 7 documents

- `clients/dm-optic/photoshoot/PHOTOSHOOT-FICHE-1PAGE-2026-10.md` — cité 3× dans le groupe, 3× au total
- `clients/dm-optic/onboarding/DEMO-SCRIPT-2026-10-07.md` — cité 2× dans le groupe, 2× au total
- `clients/dm-optic/onboarding/VISIT-RUNSHEET-2026-10-07.md` — cité 1× dans le groupe, 1× au total
- `clients/dm-optic/photoshoot/PHOTOSHOOT-BRIEF-2026-10.md` — cité 1× dans le groupe, 1× au total
- `ops/AUDIT-FICHIERS-2026-10-24.md` — cité 1× dans le groupe, 2× au total
- `clients/dm-optic/photoshoot/RETRAIT-2026-10-24.md` — cité 1× dans le groupe, 1× au total

## 5 · Le reste du dépôt, par nature

| Nature | Fichiers | Où |
|---|---|---|
| document | 766 | `AGENTS.md`, `AMK-DESIGN-SKILLS.md`, `AMK-SEO-PLAYBOOK.md` |
| image | 395 | `brand/AMK-logo-mono.png`, `brand/AMK-logo-mono.svg`, `brand/AMK-logo-primary.png` |
| script | 165 | `brand/build_fb_assets.py`, `clients/dm-optic/launch/facebook-assets/build_cover.py`, `clients/dm-optic/launch/social/build_frame_cards.py` |
| page | 139 | `brand/AMK-Logo-Kit.html`, `brand/v1-green/AMK-Logo-Kit.html`, `clients/dm-optic/brand/CARTE-SIGNATURE-TABLEAU-VISION.html` |
| audio | 40 | `content/pipeline/post01/vo/v5-sentences/s01.mp3`, `content/pipeline/post01/vo/v5-sentences/s02.mp3`, `content/pipeline/post01/vo/v5-sentences/s03.mp3` |
| données | 35 | `clients/dm-optic/content/month1/w1/spot-02.json`, `clients/dm-optic/content/month1/w1/spot-03.json`, `clients/dm-optic/content/month1/w1/ugc-03.json` |
| police | 21 | `clients/dm-optic/content/month1/w1/assets/fonts/ibm-plex-mono-latin-600-normal.ttf`, `clients/dm-optic/content/month1/w1/assets/fonts/ibm-plex-sans-latin-400-normal.ttf`, `clients/dm-optic/content/month1/w1/assets/fonts/schibsted-grotesk-latin-500-normal.ttf` |
| code | 21 | `content/pipeline/post01/render.mjs`, `ops/amk-factures-pwa/sw.js`, `ops/amk-factures-pwa/test-calculs.mjs` |
| autre | 18 | `.gitignore`, `design/vendor/LICENSE-bergside`, `design/vendor/LICENSE-emil` |
| pdf | 11 | `clients/dm-optic/launch/CARTE-AVIS-2026-10-23.pdf`, `clients/dm-optic/launch/RECAP-MISE-EN-LIGNE-2026-10-23.pdf`, `clients/dm-optic/onboarding/print/AMK-PROFORMA-2026-10-05-DM-OPTIQUE-v2.pdf` |
| texte | 10 | `clients/dm-optic/brag/share-copy.txt`, `clients/dm-optic/launch/LISTE-40-MONTURES-WHATSAPP.txt`, `clients/dm-optic/launch/baseline/README.txt` |
| vidéo | 8 | `clients/dm-optic/brag/brag.mp4`, `clients/dm-optic/content/month1/w1/spot-02.mp4`, `clients/dm-optic/content/month1/w1/spot-03.mp4` |
| config | 7 | `.github/workflows/deploy-dmoptic.yml`, `.github/workflows/machine.yml`, `hosting/previews/dmoptic/sitemap.xml` |
| archive | 3 | `amk-factures-pwa-v2.zip`, `amk-factures-pwa.zip`, `dmopticsarl.zip` |
| sous-titre | 3 | `clients/dm-optic/content/month1/w1/tiktok-01-v2.fr.srt`, `clients/dm-optic/content/month1/w1/tiktok-01.fr.srt`, `clients/dm-optic/content/month1/w2/etapes-01.srt` |
| symboles extraits (titres de documents + fonctions/classes du code) | 10352 | — |

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
| `graphify/` | `README.md` `install.sh` | 3 script(s) · 1 doc(s) · 2 shell/CI | Graphify — le graphe du dépôt, pour ne plus écrire sans avoir lu |
| `humanizer/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | humanizer — écrire comme un humain (outil copywriting AMK) |
| `hyperframes/` | `README.md` | 1 doc(s) | hyperframes (heygen-com/hyperframes) — le moteur vidéo d'AMK, auditée sur preuves |
| `hypit/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | hypit — moteur vidéo SVML pour agents (outil AMK) |
| `impeccable/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | Impeccable — détecteur d'anti-patterns UI (installé le 20/10/2026, demande King) |
| `marketingskills/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | marketingskills — 52 skills, **amont** coreyhaines31 (basculé le 23/10/2026, ruling King) |
| `moneyprinter/` | `README.md` `install.sh` | 1 script(s) · 1 doc(s) · 2 shell/CI | MoneyPrinterTurbo — installé pour assembler **nos** plans |
| `open-seo/` | `README.md` `install.sh` | 1 doc(s) · 1 shell/CI | open-seo (every-app/open-seo) — skills SEO/AEO en méthodologie |
| `ops/` | — | 8 script(s) · 5 shell/CI | — |
| `outreach/` | `README-MOCKUP.md` | 4 script(s) · 1 doc(s) | — |
| `photo/` | `README.md` `install.sh` | 1 script(s) · 1 doc(s) · 1 shell/CI | tools/photo — édition photo client, locale, pour le web |
| `pro-design/` | `README.md` `install.sh` `SKILL.md` | 2 doc(s) · 1 shell/CI | pro-design — le skill de construction de pages (installé le 23/10/2026) |
| `qa/` | `AUDIT-2026-09-17.md` | 38 script(s) · 4 doc(s) | — |
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
| `dm-optic/` | 169 | 83 | oui |
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
| `v06-facebook-no-booking` | 14 | — | 2 fichier(s) | PRÊTE À PUBLIER (master + voix posée + portique passé) · 38,61 s · 1080×1920 · 30 fps … |
| `v07-stock-invisible` | 2 | — | — | — |
| `v08-preuve-ouverte` | 2 | oui (SCRIPT.md) | — | Stage SCRIPTÉ (23/10/2026) — pas de rendu, pas de publication |

## 6 · Où chercher quoi — la table de routage, vérifiée par le graphe

| Sujet | Les 3 documents qu'il faut ouvrir |
|---|---|
| Écrire un message / relancer | `sales/CLIENT-MESSAGING-RULES.md`, `sales/MESSAGES-2026-09-23-PERSUASION.md`, `sales/AMK-Sales-Playbook-v2.md` |
| Prix, grille, remise | `sales/PRIX-ET-RECURRENCE-2026-09-24.md`, `knowledge/PRIX-2026-10-24.md`, `sales/REVUE-CONTRATS-GRILLE-2026-09-23.md` |
| Contenu, vidéo, script | `research/youtube-lessons/2026-10-11-batch-3/video-8-tiktok-beginners-guide.md`, `content/pipeline/CONTENT-PIPELINE.md`, `content/strategy/CALENDRIER-4-SEMAINES-2026-10-12.md` |
| Design, page, tokens | `design/WORKFLOW.md`, `knowledge/LANDING-FUNNEL-2026-10-23.md`, `sales/Playbook-Addendum-3-Conversion-Design-2026-09-15.md` |
| Déploiement, QA, portiques | `tools/qa/AUDIT-LESSONS-2026-10-23.md`, `PRE-FLIGHT.md`, `ops/TOOL-SCAN.md` |
| Client DM Optique | `clients/dm-optic/pre-launch-checklist.md`, `clients/dm-optic/dossier.md`, `clients/dm-optic/site/CLIENT-REQUIREMENTS-BRIEF.md` |
| Outils et skills | `tools/agent-reach/README.md`, `tools/pro-design/README.md`, `tools/ecc/README.md` |
| CRM, pipeline, activité | `leads/CRM-AUDIT-AND-PROPOSAL-2026-09-18.md`, `leads/records/univers-optique.md`, `leads/CONTRADICTIONS.md` |

## 7 · Les questions qu'on peut poser au graphe dès maintenant

```bash
bash tools/graphify/ask.sh "message prospect clinique"      # quelles règles lire avant d'écrire
bash tools/graphify/ask.sh "prix grille remise"               # la couche tarifaire
bash tools/graphify/ask.sh "vidéo script accroche"            # la couche contenu
graphify explain "sales/CLIENT-MESSAGING-RULES.md"
graphify path "sales/LISTE-OPTICIENS-2026-10.md" "knowledge/OUTREACH-MESSAGING-2026-10-22.md"
```

---

*Cette carte est générée : ne pas l'éditer à la main. Elle se régénère avec `python3 tools/graphify/build_full_graph.py`.*
