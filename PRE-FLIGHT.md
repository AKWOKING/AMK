> **Every orchestrator response to King must begin with the §0 pre-flight header. Every King-issued task that passes through the chief of staff will re-state this requirement at the top of the task. Non-compliance = returned message.** *(standing rule, King 08/10, 11th message)*

# AMK — PRE-FLIGHT PROTOCOL (standing rule, King 17 Sep 2026)

## 0 · MANDATORY FIRST READ (standing rule, King 08/10)

> **§0 — MANDATORY FIRST READ.** Before beginning any task, read this document in full. Every task begins with §1e resync, then a §0 pre-flight confirmation in the response header: *"Pre-flight: [task type] → PRE-FLIGHT.md read, [other files loaded]."* A response without this header is incomplete and will be returned.

Structural, not a memory test: the header is the **first line** of every response, so King can see the precondition was met without asking. (Supersedes the looser one-line format below; same discipline, now with the explicit « PRE-FLIGHT.md read » confirmation.)


### 0b · Client dossier first (standing rule, King 08/10, 12th message)

> **§0b — CLIENT DOSSIER FIRST.** Before any ruling on a client's site, document, or message, read the client's full dossier end-to-end. State in the pre-flight header which files were loaded. If a ruling is being made on a client artifact without the dossier loaded, the ruling is incomplete.

Applied: the header lists the files **actually loaded** (and says "partial" / "not read" where that is true) — never the whole folder by assumption.

### 0c · Knowledge docs first (standing rule, King 23/10)

> **§0c — KNOWLEDGE FIRST.** Before any task, list `knowledge/` and read the documents whose scope
> covers the task — the client dossier alone is **not** enough. The pre-flight header names the files
> actually read. A task started without the knowledge layer is incomplete, even when the dossier was
> read end to end.

Application : `knowledge/` est la couche de référence (table ci-dessous) ; une règle qui la contredit
se dit **à voix haute**, et le document est corrigé le jour même — jamais contourné en silence. Une
recherche neuve (vidéo, article, outil) atterrit dans `knowledge/` **avant** d'entrer dans une page
ou un message : sinon elle n'existe pas. For DM Optique, "end to end" means `clients/dm-optic/` including `onboarding/CONDITIONS-D-INTERVENTION-*`, `site/SPEC-PAGES-v1.md`, the build notes (`build-notes.md`), the proforma, and the client's messages as logged in the CRM. **For the DM Optique site, the source of truth is `clients/dm-optic/site/CLIENT-REQUIREMENTS-BRIEF.md`: rulings cite it; a question it cannot answer extends it (its « Journal d'extension »), never a ruling from memory.**
---

**The rule: no task begins without a pre-flight.** Identify the task type → load the lessons for that field from this repo → read them → only then start work. Work that skips the pre-flight is invalid.

**Every task response opens with one line:**
`Pre-flight: [task type] → loaded [folders/files]`
If a folder/file is missing, empty or unreadable → say so in that line and either proceed with a stated gap or stop and ask. Never skip silently.

---

## 0e · Audit de soi : correctif, amélioration, action (ruling King 13/10)

Tout audit qui relève un problème doit contenir trois éléments. Un audit sans correctif proposé est incomplet.

1. **Le correctif** : précis, dit ce qui change dans quel fichier.
2. **L'amélioration** : durable, sous forme de règle, de contrôle ou de changement de modèle, pour que le problème ne revienne pas.
3. **L'action** : qui fait quoi (orchestrateur, King, ou les deux).

**Règle complémentaire (King 13/10) :** les chiffres et états que l'orchestrateur affirme (une date, un compte, l'état d'un fichier ou d'une fiche) sont **vérifiés contre la source avant d'être affirmés**. Ce qui ne peut pas être vérifié est dit comme tel. La confiance n'est pas une vérification.

**Instruction ≠ état :** une règle annoncée n'est pas une règle présente. Avant de la citer, l'orchestrateur vérifie qu'elle figure dans le fichier.

---

## 0f · Le tour se lit avant de répondre : trois couches, dans cet ordre (ruling King 23/10)

> *King 23/10 : « at each turn you go through the preflight doc, the knowledge docs, and other docs
> depending on the task or question ».*

Ce n'est pas une recommandation, c'est **la première chose que fait un tour**. Trois couches, toujours
dans cet ordre, et le compte rendu en tête de réponse dit **ce qui a été lu et ce qui ne l'a pas été** :

| # | Couche | Ce qu'on y cherche | Temps |
|---|---|---|---|
| 1 | **`PRE-FLIGHT.md`** (§0 à §5, en entier) | la règle qui gouverne la tâche, les portiques, les verrous, les rulings en vigueur | 2 min |
| 2 | **`knowledge/`** — les documents dont le périmètre couvre la tâche (§0c + table §1g) | ce que le dépôt sait déjà : sources vérifiées, chiffres, structure, retours d'expérience | 3 min |
| 3 | **Les documents de la tâche** : dossier client (§0b), brief, devis, données, captures, pièces jointes | l'état réel du sujet traité | variable |

**Règle de sortie :** si une couche n'a pas été lue, la réponse le dit et explique pourquoi (fichier
absent, hors périmètre, illisible) — jamais un silence. Une réponse qui invente une règle déjà écrite,
ou qui redécouvre un chiffre déjà sourcé, a sauté la couche 2.

**Et le contrôle qui va avec :** avant d'affirmer *(a)* une règle, *(b)* un chiffre, *(c)* l'état d'un
fichier ou d'un compte, on l'a **lu dans la source**, pas dans sa mémoire du tour précédent (§0e).

---

## 0g · Notion = second cerveau, et sauvegarde lisible (ruling King 23/10)

> *King 23/10 : « everything has to be documented on another note do you have access to notion ?? if yes
> you can use that as your second brain and backup ».* Accès confirmé le 23/10 ; la page existe.

```
Notion      « AMK · second cerveau — miroir du dépôt »
ID          4024b1d8-9633-814c-8837-dcbc1b7f28b0
Parent      Pipeline42 (espace de travail)
URL         https://app.notion.com/p/AMK-second-cerveau-miroir-du-d-p-t-4024b1d89633814c8837dcbc1b7f28b0
```

**La règle de priorité, et elle ne se discute pas : le dépôt fait loi.** Notion est un **miroir** —
lisible depuis un téléphone, et une **sauvegarde** si le dépôt devient inaccessible. Quand les deux se
contredisent, c'est Notion qui est corrigé, le jour même, jamais le dépôt.

**Ce qui se recopie dans Notion** (et seulement ça) :

| Contenu | Fréquence |
|---|---|
| l'**état debout** : branche, PR, commits d'avance, clients récurrents, ce qui est encaissé / dû | à chaque tour qui change un de ces faits |
| les **documents qui font loi** (table sujet → fichier → ce qu'il tranche) | quand un document structurant est créé ou déplacé |
| les **règles debout** en cinq lignes | quand un ruling en ajoute ou en retire une |
| les **prochaines actions** (cases à cocher) | à chaque tour |
| le **journal** daté, une ligne par tour qui change quelque chose | à chaque tour |

**Ce qui ne va pas dans Notion** : les secrets (NIU, RIB, mots de passe, numéros de clients), les
documents client complets, les fichiers binaires. Notion est un **résumé et un index**, pas un dépôt
secondaire : dupliquer un document entier crée deux vérités, et c'est exactement ce que §0f interdit.

**En cas de doute sur l'état d'un fichier**, on lit le dépôt — pas la page Notion, qui peut avoir un tour
de retard.

## 0d · Décision → fichiers touchés (table manuelle, 13/10/2026)

Quand une règle change ou qu'un ruling est donné, cette table dit quels fichiers il faut relire et mettre à jour. Chaque ligne est vérifiée contre le dépôt. Ajouter une ligne à chaque nouvelle règle permanente.

| Règle | Fichiers qu'elle gouverne |
|---|---|
| **Marketing & création de contenu (ruling King 22/10)** | `knowledge/MARKETING-OPTICAL-2026-10-22.md` · `knowledge/CONTENT-CREATION-2026-10-22.md` · `PRE-FLIGHT.md` §1g · `clients/<client>/brand/BRAND-STRATEGY-*.md` · scripts `content/month1/**` · `tools/record/` · portique `tools/qa/audit_video_motion.py` |
| **Notion = miroir + sauvegarde (ruling King 23/10)** | page Notion `4024b1d8-9633-814c-8837-dcbc1b7f28b0` · ce §0g · le journal de la page |
| **Lecture par tour, trois couches (ruling King 23/10)** | `PRE-FLIGHT.md` §0f · §0c · §1g · ce tableau |
| **Contrat d'une page (ruling King 23/10)** | `ops/templates/CONTRAT-UNE-PAGE-2026-10.md` · `.pdf` · `tools/ops/make_contrat.py` · `sales/REVUE-CONTRATS-GRILLE-2026-09-23.md` (addendum 23/10) |
| **Un opt-in, un seul (ruling King 23/10)** | `sales/lead-magnets/CONTROLE-PRESENCE-EN-LIGNE-2026-10-23.pdf` · `tools/ops/make_magnet.py` · `knowledge/CONTENT-CREATION-2026-10-22.md` §5 bis |
| **Knowledge first (ruling King 23/10)** | `knowledge/**` (la couche de référence) · `PRE-FLIGHT.md` §0c · table de routage §1g |
| **Versionnage : fusion sur jalon, ou ≈ 3 000 lignes / 40 fichiers / 6 tours — « 1 000 CHANGES, pas 1 000 commits » (King 23/10, corrigé le 23/10)** | `PRE-FLIGHT.md` §1i · `tools/ops/wake.py` · `tools/ops/gate-amk.sh` |
| **Plafond 5 clients · Présence ≤ 3 pages · grille pour la prochaine signature seulement (King 23–24/10)** | `PRE-FLIGHT.md` §1h · `knowledge/PRIX-2026-10-24.md` §4–§5 · `knowledge/MAINTENANCE-CLIENTS-2026-10-22.md` · `site/index.html` · `site/en/index.html` · `site/creation-site-web-*.html` · `sales/PRIX-ET-RECURRENCE-2026-09-24.md` · `ops/FACTURATION-2026-10-24.md` |
| **Credential rule** (ne jamais revendiquer ce qu'on ne peut pas prouver) | `content/strategy/RULE-CREDENTIAL-CLAIMS.md` · pages client (`clients/*/`, `site/`) · textes de publication (`content/carousels/`, `content/scripts/`) |
| **Caption-split / découpage de légende (ruling King 12/10 : frontières de phrase, jamais de fragment)** | `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md` · section « Règle debout — VO vidéo courte », **AMENDEMENT 2 (découpe des légendes)** (fichier d'origine ; le commit `9294cf2` le contient) · appliquée dans `content/scripts/` et `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` |
| **Wave gate / relances (24 h, 48 h, 7 j, changement de canal)** | `sales/CLIENT-MESSAGING-RULES.md` · `leads/CRM.csv` · `leads/build/crm.py` · `leads/PIPELINE.md` · `sales/Activity-Log.md` |
| **Ruling « relance interdite après report du client » (Labiomed)** | `leads/CRM.csv` · `leads/records/labiomed-deido.md` · `leads/KILL-LIST.md` · `sales/Activity-Log.md` |
| **ICP (clinique / optique, seuil MQL)** | `sales/Deep-Dive-Research.md` · `sales/LeadSourcing-Reset-2026-09-18.md` · `sales/AMK-Sales-Playbook-v2.md` · `sales/LISTE-OPTICIENS-2026-10.md` · listes de vague (`sales/Send-BATCH-*.md`) |
| **3-Ingredient rule (avatar, décor, logo)** | `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` §3 · prompts Flow (§5) · `PRE-FLIGHT.md` §routage vidéo |
| **Règle vidéo : Flow remplace render.mjs, render.mjs = secours** | `PRE-FLIGHT.md` (routage vidéo) · `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` · `content/pipeline/CONTENT-PIPELINE.md` |
| **Orchestrateur : livrables par vidéo (script, prompt Flow, prompt ChatGPT, légende TikTok)** | `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` §2 · `content/pipeline/CONTENT-PIPELINE.md` |
| **Accès Flow / chiffres [NV] : vérifiés par King, pas par l'orchestrateur** | `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` §9 et points ouverts |
| **Publication : rien n'est publié sans validation de King** | `content/strategy/POSTING-CALENDAR.md` · `content/strategy/CALENDRIER-4-SEMAINES-2026-10-12.md` |
| **POST-02 en attente (pas de script avant décision de King)** | `content/pipeline/CONTENT-PIPELINE.md` · `content/strategy/POSTING-CALENDAR.md` · `sales/Activity-Log.md` |
| **Recherche externe = Agent Reach d'abord (ruling King 19/10, §1f①)** | `PRE-FLIGHT.md` §1f + lignes de routage recherche (§1, §1c, §2 étape 3) · `tools/agent-reach/README.md` · skill installé `~/.agents/skills/agent-reach/SKILL.md` (hors dépôt) · sorties de recherche (`research/`, `sales/research/`) |
| **Brag de livraison à chaque site prêt (ruling King 19/10, §1f②)** | `PRE-FLIGHT.md` §1f + §1b · `tools/brag/README.md` · `tools/qa/audit_video_motion.py` (portique) · `clients/<client>/build-notes.md` (chemin du brouillon) · `hosting/previews/README.md` (deploy gate) |
| **Déploiement Vercel DM Optique après chaque changement du site (ruling King 20/10, §1f③)** | `PRE-FLIGHT.md` §1f · `clients/dm-optic/build-notes.md` (id + état du déploiement) · `hosting/previews/dmoptic/` (racine du projet Vercel) · `sales/Activity-Log.md` |
| **Design/build/revue = taste-skill appliqué (ruling King 20/10, §1f④)** | `PRE-FLIGHT.md` §1f + §1b · `tools/taste-skill/README.md` · skill installé `~/.agents/skills/design-taste-frontend/SKILL.md` (hors dépôt) · `AMK-DESIGN-SKILLS.md` (lois maison, gagnent en cas de conflit) · `clients/<client>/build-notes.md` + `inspiration.md` (direction tirée, redraws, scores) |
| **Mouvement d'interface = design-motion-principles appliqué (ruling King 20/10, §1f⑤)** | `PRE-FLIGHT.md` §1f + §1b · `tools/design-motion-principles/README.md` · skill installé `~/.agents/skills/design-motion-principles/SKILL.md` (hors dépôt) · `AMK-DESIGN-SKILLS.md` (lois maison, gagnent en cas de conflit) · `clients/<client>/build-notes.md` (pondération des lentilles, findings motion) |
| **Audit/vérification = skills ECC sélectifs en appui (ruling King 20/10, §1f⑥)** | `PRE-FLIGHT.md` §1f + §1b · `tools/ecc/README.md` · skills installés `~/.agents/skills/{accessibility,production-audit,verification-loop,security-review,seo,click-path-audit}/SKILL.md` (hors dépôt) · `tools/qa/` (les portiques maison font foi) · `clients/<client>/build-notes.md` (score, preuves, blockers) |
| **Recherche UX/UI consultable = UI/UX Pro Max en appui (ruling King 20/10, §1f⑦)** | `PRE-FLIGHT.md` §1f + §1b · `tools/ui-ux-pro-max/README.md` · skill installé `~/.agents/skills/ui-ux-pro-max/SKILL.md` (hors dépôt) · `AMK-DESIGN-SKILLS.md` (lois maison, gagnent en cas de conflit) · `clients/<client>/build-notes.md` (grilles consultées, avis écartés) |
| **Détection d'anti-patterns UI = Impeccable en portique d'appui (ruling King 20/10, §1f⑧)** | `PRE-FLIGHT.md` §1f + §1b · `tools/impeccable/README.md` · skill installé `~/.agents/skills/impeccable/SKILL.md` + moteur `~/.impeccable/bin/` (hors dépôt) · `tools/qa/` (les portiques maison font foi) · `clients/<client>/build-notes.md` (findings vérifiés, faux positifs nommés) |
| **Gabarit W43 = porte de tout contenu client (ruling King 21/10, « implement »)** | `sales/research/2026-W43-techniques.md` **§12 + §12b** (la règle et le gabarit : 5 beats · 7 interdits · 6 cases) · `content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md` (règle debout) · `clients/<client>/content-plan-*.md` et `posting-calendar*.md` (porte de chaque pièce) · `clients/<client>/content/**` (chaque script coche les 6 cases) · `content/scripts/README.md` + `CONTENT-LESSONS` §10/§12 (les portes maison restent supérieures) |
| **Clôture debout : inventaire outils en ouverture + propositions/audit en fin de chaque réponse (ruling King 20/10, §1f⑨)** | `PRE-FLIGHT.md` §0 + §1f⑨ (la règle) · toute réponse de l'orchestrateur (en-tête enrichi + bloc final) · `ops/TOOL-SCAN.md` (l'inventaire consulté) · `clients/<client>/build-notes.md` (audits qui alimentent le bloc) |

Si cette table ne suffit plus à suivre la propagation entre fichiers, c'est le déclencheur pour réévaluer un outil de graphe de connaissances (voir la décision Graphify dans `sales/Activity-Log.md`).

---

## 1 · Routing table (King's fields → the actual files in this repo)

The rule names abstract folders; these are where the lessons actually live. Load **all** relevant rows when a task spans several types.

| Task type | Load these (repo paths) |
|---|---|
| **Marketing / outreach copy** | `research/YouTube-Lessons.md` (entries [1]–[6] copy, [10][13] design-of-copy) · `sales/Monday-Outreach-Pack.md` (**COPY CRAFT GATE** + templates) · `sales/AMK-Sales-Playbook-v2.md` (Parts H, I) · niche: `sales/research/*deep-dive*.md`, `sales/Deep-Dive-Research.md`, `sales/RESEARCH-STANDARD.md` |
| **Trouver l'angle d'un prospect (avis publics)** | `sales/DETECTION-FUITES-2026-09-24.md` (**la méthode, les seuils adaptés à Douala, le message type, les quatre lignes qu'on ne franchit pas**) · `tools/outreach/scan_reviews.py` (+ son test, 12 assertions) · `sales/FICHE-GOOGLE-PROFILE.md` §5 (ce qu'on peut promettre sur les avis, et ce qu'on ne promet jamais) |
| **Écrire ou relire un message avant envoi** | `sales/MESSAGES-2026-09-23-PERSUASION.md` §1 (**la règle de la première ligne : le nom et le titre passent à la fin ; les six premiers mots sont pour lui**) + `sales/PERSUASION-5-NIVEAUX-2026-09-23.md` §5 (la checklist de 5 lignes, 30 secondes) |
| **Prospecting / qualifying** | `sales/APPELS-GOOGLE-MAPS-2026-09-24.md` (les trois ouvertures d'appel, la règle du **mobile avant le fixe**, les quatre fiches joignables seulement par un fixe, les heures d'appel, et la limite sur les avis — lot [26] du 24/09) · `sales/AMK-Sales-Playbook-v2.md` (Parts A, B, D, E, H, J) · `research/YouTube-Lessons.md` [7][8] · **`sales/RESEARCH-STANDARD.md` (incl. §8b three-door pre-send gates — every send, every time)** · niche: `sales/Deep-Dive-Research.md`, `sales/Remote-Sweep-*.md`, `sales/Walk-In-*.md` · state: `sales/Pipeline-Status.md` |
| **Presenting / proposals** | `sales/AMK-Sales-Playbook-v2.md` (Parts C, E, F, I, J) · `sales/Monday-Outreach-Pack.md` · `AMK-DESIGN-SKILLS.md` §11b + §19 · `sales/swipe/README.md` |
| **Découverte / réunion client** | `sales/QUESTIONNAIRE-REUNIONS-2026-09-25.md` (**le questionnaire : personnalisation, autres services, relation — une question ne se pose que si sa réponse change un fichier**) · `sales/RDV-UNIVERS-OPTIQUE-2026-09-25.md` / `sales/RDV-UNILABO-2026-09-25.md` (les six points factuels, l'ordre de la séance) · `sales/FICHE-GOOGLE-PROFILE.md` (la question de la fiche) |
| **Closing / objection handling** | `sales/AMK-Sales-Playbook-v2.md` (Part I = 3A reframe, Part J = CLOSER, Part E = flips, Part C = closes) · `research/YouTube-Lessons.md` [7][8] |
| **Any copywriting** | `research/YouTube-Lessons.md` [1]–[6] (+ [5] Harry Dry = the law) · `sales/Monday-Outreach-Pack.md` COPY CRAFT GATE · `AMK-DESIGN-SKILLS.md` §11 + §11b · `sales/swipe/README.md` · client's own words (FB/comments) per Part H |
| **Visual design (mockups, brand, graphics)** | `AMK-DESIGN-SKILLS.md` (§1–§19: dials, anti-slop §3, locks §4, type §5, colour §6, layout §7, components §8, motion §9, images §10, copy-law §11b, redesign §12, pre-flight §13, style menu §14, image art-direction §15, patterns §17, §19 foundations) · `design/WORKFLOW.md` · `design/STYLE-TOKENS.md` · `design/MOTION.md` · `design/vendor/*` (registries) · `clients/_uniqueness-registry.md` |
| **Website build** | `tools/qa/PROTOCOLE-LECTEUR-ECRAN.md` (**le test à l'oreille, à la main, 5 minutes : NVDA + TalkBack, les annonces attendues sur NOS pages**) · `tools/qa/test_site_a11y_behaviour.mjs` (les états de la page, exécutés dans un DOM) · `research/ACCESSIBILITE-2026-09-24.md` (le rapport du lot [27] : le niveau promis, les quatre choses qu'aucune machine ne vérifie) · **`tools/qa/audit_a11y.py`** (+ `test_audit_a11y.py`) — le contrôle d'ACCESSIBILITÉ, critère par critère, **WCAG 2.2 AA** (le niveau qu'un appel d'offres exige : ni A seul, ni AAA) : images et alts, hiérarchie des titres, étiquettes de champs, zoom non bloqué, clavier, focus visible, lang, noms des boutons · `AMK-DESIGN-SKILLS.md` **§27** (le niveau promis, et les quatre choses qu'aucune machine ne vérifie) · **`tools/qa/audit_hero.py`** (§26 + §29 : la grammaire du premier écran **et** son anatomie — trois questions, deux actions au maximum, la marque nommée) (+ `test_audit_hero.py`) — le contrôle du PREMIER ÉCRAN appris au lot [26] : mots écrits dans le CSS, hero 100vh sans `@media`, animations de mise en page sans `prefers-reduced-motion`, gabarits non remplis · `AMK-DESIGN-SKILLS.md` **§26** (la grammaire du hero) · All of the design row **plus** `AMK-DESIGN-SKILLS.md` §18 (spec-before-build, value provenance, verification ladder) + §19.3 (3-direction exploration) · copywriting row · `design/WORKFLOW.md` stages 1–9 · deploy gate `hosting/previews/README.md` · client context: `sales/research/<client>-deep-dive-*.md` + `clients/<client>/*` · **live inspiration research (step 3 of the uniqueness protocol)** · **`llms.txt` généré au build** (pattern DM : `build_dmoptic_montures.py` — fichier de découverte IA + garde anti-invention/compte de liens ; ruling « implement the solutions », 20/10) pour tout site client destiné à une production |
| **SEO / site public (AMK ou client)** | `content/strategy/SEO-CHECKLIST-CLIENT-SITES-2026-10.md` (**la liste dans l'ordre + ce que Google dit de ne PAS faire**) · `site/SEO-REVIEW-2026-10-08.md` §8 · `tools/seo/bake_default_lang.py` (français/anglais par défaut dans le HTML) · `node tools/qa/test_amkcm_lang.mjs` · `content/strategy/RULE-CREDENTIAL-CLAIMS.md` (affirmations) |
| **Photographie / images livrées** | `research/PHOTO-LABO-PIXEL-8A-2026-09-24.md` (ce que le Pixel 8A sait faire, la séance de 15 min, la lumière d'un laboratoire, la fiche à emporter FR, la vérification de 60 s) · `AMK-DESIGN-SKILLS.md` §25 (une photo = un sens) + §32 · `tools/qa/audit_images.py` (**contrôle**) |
| **Prix / abonnement / récurrence** | `sales/PRIX-ET-RECURRENCE-2026-09-24.md` (**ce qui est tranché, et les 16 questions ouvertes — à lire AVANT toute conversation d'argent**) · `sales/REVUE-CONTRATS-GRILLE-2026-09-23.md` · `sales/ORDRE-DES-OFFRES-2026-09-23.md` |
| **Delivery / handoff** | **`tools/qa/audit_delivery.py`** (+ `test_audit_delivery.py`, leçons `tools/qa/AUDIT-LESSONS-2026-10-23.md`) — la porte qui mesure ce qui n'est pas dans le document (nav mobile, cache, icônes, URL, llms.txt, partage, schéma, en-têtes) · `AMK-DESIGN-SKILLS.md` §13 (pre-flight) + §18.4 (verification ladder) · `hosting/previews/README.md` (deploy gate) · `site/DEPLOY.md` · `sales/AMK-Playbook-Addendum-Outcomes-2026-09-15.md` (handoff video, care plan) · **brag de livraison en brouillon d'office (§1f②, `tools/brag/README.md`)** |
| **Retention / upsell / referrals** | `sales/AMK-Sales-Playbook-v2.md` (A5 referral, F6, Part J reinforce-the-decision) · `sales/AMK-Playbook-Addendum-Outcomes-2026-09-15.md` · `sales/AMK-Playbook-Addendum-4-Marketing-Systems-2026-09-15.md` (monthly report, GBP layer) |
| **Weekly research / veille vidéo** | `research/YouTube-Lessons.md` (le lot du jour ; **lot [46] du 23/10** = Facebook 2026, publicité Meta, méthodes Instagram) · `knowledge/CONTENT-CREATION-2026-10-22.md` **§9** (les cinq gestes de fabrication adoptés) · **lecture vidéo : `fetch_page` sur `youtube.com/watch?v=<id>` (anglophone) ou `youtubetotranscript.com/transcript?v=<id>` (francophone, seule source qui pagine)** — `ops/QA-NOTES.md`, 23/10. Une transcription n'est **pas** un visionnage : l'écrire dans le lot |
| **Weekly research (générique)** | The field being studied → log the output back into that field's lessons: sales/marketing → `sales/research/<YYYY>-W<WW>-techniques.md`; video lessons → `research/YouTube-Lessons.md`; design/build → the relevant `AMK-DESIGN-SKILLS.md` section · **collecte externe via Agent Reach d'abord (§1f①, `tools/agent-reach/README.md`)** |

| **CRM / pipeline** | `leads/build/crm.py` (schéma + énumération des étapes — C'EST LUI LA SOURCE, pas le CSV) · `leads/build/guard.py` + `generators.lock.json` (EMPREINTE des générateurs : `rebuild.sh` refuse d'écrire si un générateur a été remplacé par une version plus ancienne — 22/09 : une restauration d'instantané avait effacé l'état des deux fils chauds du CSV sans un seul message d'erreur) · `leads/CRM.csv` (état) · `sales/Activity-Log.md` (chronologie, append-only) · `sales/AMK-Sales-Playbook-v2.md` (règles debout, §A4 corrigé) · vue live : `leads/PIPELINE.md`, `leads/KILL-LIST.md`, `leads/STALE.md`, `leads/SOURCES.md`, `leads/Daily-Plan.csv` (toutes GÉNÉRÉES) · fiche d'un lead : `leads/records/<slug>.md` · **règle 02/10 (bug OraCare) : avant de remplir `source_detail` d'un lead content, vérifier que le lead a VU la vidéo — jamais déduire l'attribution de « la seule vidéo publiée »** · **règle 02/10 (fil Cavisa) : jamais re-poser la même question — au-delà de 7 jours sans réponse, changer de canal (texte → voix → appel), pas de wording ; un fix interne n'est jamais un prétexte d'outreach** · **règle 02/10 (piège de file, re-datée 03/10) : après édition de RELANCE_A_JOUR ou de toute structure planifiée à clés, vérifier la SORTIE de la file après rebuild — rc=0 n'est pas une preuve** · **règle 03/10 (tous prospects) : aucun travail non demandé sur la démo d'un prospect — sans demande explicite, la démo reste intouchée ; follow-up plain, chaud, court, sans prétexte ni re-ask ; le travail ne reprend que si le prospect demande quelque chose de spécifique** · **protocole 05/10 : premise check (une ligne, vérifiée contre le fil) avant toute sortie client-facing + passe second-reader + log dans ops/INFERENCE-ERRORS.md · **règle 05/10 (#7) : premise check d'un document financier = complétude du bloc émetteur au standard fiscal du client, pas seulement cohérence interne (« que demandera-t-il qui n'est pas là ? »)** |

**Règle d'écriture du CRM (M7, 21 Sep 2026) — « la prose ne suffit pas ».** Une décision qui
doit changer un calcul (`parked`, un score, un `reply_type`) se met **dans le générateur**
(`leads/build/crm.py`), jamais seulement dans un `.md` : COMOBIL était annoncé « parké » dans trois
fichiers et restait `prospect` dans les données, donc la kill list déduite le remettait en tête.
Une correction manuelle dans `CRM.csv` est **perdue** au prochain `leads/build/rebuild.sh` —
c'est voulu. La chronologie, elle, va dans `sales/Activity-Log.md` (une ligne par envoi, une ligne
par réponse) et remonte toute seule dans les fiches et les vues.

**State files to load with almost everything:** `sales/Pipeline-Status.md` (current week), the prospect dossier, `sales/Outreach-Pack-<date>.md` (active pack), session memory.

**Knowledge base (couche de référence, 02/10 — `knowledge/HOUSE-KNOWLEDGE-BASE.md`) :** chaque
pré-vol charge, **en plus du dossier métier**, les sections pertinentes de la base :

| Task type | + knowledge base |
|---|---|
| **Sales / outreach / proposal** | §2, §8 |
| **Content / script / video / caption** | §7, §8 · **DM Optique : `clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md` — à relire avant d'écrire (King 22/10)** · **gabarit W43 : `sales/research/2026-W43-techniques.md` §12/§12b — à cocher avant d'écrire** · **vidéo : `content/strategy/VIDEO-PIPELINE-FLOW-2026-10.md` (pipeline Flow + ChatGPT, remplace `render.mjs` ; `render.mjs` = secours uniquement)** |
| **Marketing / strategy** | §3, §5 |
| **Ads / campaign** | `clients/<slug>/ads/campaign-brief.md` (quand il existe) + §4, §5 |
| **Design / build** | §1 |
| **Delivery / onboarding** | §1, §2 |
| **Orchestration / meta / workflow** | §6 |
| **Ops / workflow / project management** | §9 · `ops/LIFECYCLE.md` · `ops/ONBOARDING.md` · `ops/templates/` |

**Étape de vérification des sources :** avant d'appliquer une section, vérifier que ses sources sont
encore atteignables. 404 ou bloquée → note au change log de la base, et on travaille depuis le contenu
de la section quand même — **les sources servent à vérifier, pas à dépendre**.

---

## 1b · Porte technique obligatoire avant toute livraison (17 Sep 2026)

```
python3 tools/qa/audit_html.py <fichier-construit>      # doit finir sur « TOTAL confirmed findings: 0 »
python3 tools/qa/audit_a11y.py --strict <fichier-construit>   # rc=0 : aucune faute de niveau A ou AA
python3 tools/qa/audit_images.py <fichier-construit>          # 0 faute : ratio annoncé = ratio réel, poids, pas de GPS
python3 tools/qa/audit_reveal.py site/                        # 0 faute : aucune animation ne cache du contenu (ajouté 23/10)
python3 tools/qa/audit_delivery.py <dossier> --base <url>     # 0 P1 : navigation mobile, cache, icônes, URL, llms.txt, partage, schéma, en-têtes (ajouté 23/10)
python3 tools/qa/audit_funnel.py site/index.html             # 0 P1 : premier écran, preuve, problème→solution, étapes, prix, FAQ, barre collante (ajouté 23/10)
bash tools/ops/gate-dm.sh                                     # porte DM complète ; son étape 4 lance audit_delivery.py --strict (livraison client)
bash tools/ops/gate-amk.sh                                    # porte AMK (site propre + deux pages de niche) : tunnel, témoin, état du dépôt
```

`audit_delivery.py` (23/10) ferme les deux angles morts qu'un audit extérieur a trouvés le jour où les
cinq autres portiques rendaient « 0 faute » : **aucune navigation sous 980 px** (le CSS cachait la nav,
aucun bouton de menu) et **`max-age=0` sur toutes les images et polices**. Un portique de documents ne
peut pas voir ce qui n'est pas dans un document — une feuille de style, des en-têtes HTTP, un fichier
d'icône absent. Il valide aussi la **forme** des motifs de `_headers` : sur Cloudflare Pages le splat ne
vaut qu'en fin de motif, donc `/*.webp` ne matche rien (l'audit extérieur proposait exactement cette
règle : elle aurait laissé le défaut en place). Son témoin, `tools/qa/test_audit_delivery.py`, casse
douze choses une par une et vérifie que chacune est nommée. Leçons complètes :
`tools/qa/AUDIT-LESSONS-2026-10-23.md`.

`audit_funnel.py` (23/10) vient d'ailleurs : d'une source **externe**, la vidéo Liam Ottley ×
Arthur du 04/09/2025 et son tableau Figma « funnel-fixer » (`knowledge/LANDING-FUNNEL-2026-10-23.md`).
Il vérifie la **structure** d'une page de vente : CTA dans le premier écran, titre de résultat et
non de technologie, preuve présente (et si elle est un cas client ou seulement une démonstration),
douleur suivie d'une solution, trois étapes, prix ou devis expliqué, FAQ, action toujours à portée,
mots creux interdits, texte de remplacement. Il ne juge pas la **qualité** d'un titre — c'est écrit
dans son en-tête, pour que personne n'attende de lui ce qu'il ne peut pas faire.
Le troisième contrôle est né le 24/09 (lot [32]) avec l'arrivée des **vraies photos** : une photo de
téléphone pèse 3 à 6 Mo et porte la position GPS. Il vérifie la structure et la vie privée — **jamais la
beauté de la photo** (celle-là se juge à l'œil).
Contrôle **structure** (sections imbriquées, équilibre) + **contraste WCAG** de chaque texte (desktop et mobile).
`audit_reveal.py` (23/10) garde la classe de bug qui a rendu **142 blocs invisibles** deux fois de suite :
`html.js .rv{opacity:0}` étant plus **spécifique** que `.rv.in{opacity:1}`, le JavaScript ajoutait bien la
classe et rien ne s'affichait. La règle de base doit porter `:not(.in)`. Motif : un `</div>` perdu en insérant le miroir opticien a rendu du texte blanc sur fond blanc (déclaré par King). Détail : `tools/qa/AUDIT-2026-09-17.md`.

## 1c · Contrôle approfondi — obligatoire sur CHAQUE prospect (King, 24 Sep 2026)

> *« Mais à partir de maintenant fais toujours des contrôles approfondis sur chaque prospect. »*

Six recherches **avant** d'écrire le message : nom exact + ville · le vrai domaine (pas la page
d'accueil du groupe : `.com`, `.cm`, `.shop`, blogspot, Facebook) · les canaux discrets (Blogspot,
WordPress.com, YouTube, X/Instagram, annuaires) · recoupement adresse/horaires/numéros (la source la
plus récente gagne) · **le verdict écrit de chaque affirmation** qu'on s'apprête à faire · si une page
dédiée existe → **écarté**, pas de message. Détail et les deux preuves du 24/09 (Golden Eyes écarté
avant l'envoi ; SkyOptic et Cinq Sens fragilisés après l'envoi) :
`sales/MESSAGES-2026-09-23-PERSUASION.md` §5 et `sales/RESEARCH-STANDARD.md` §8c.

## 1d · Règle QA/grep — chaîne cherchée = ligne source littérale (ruling King 05/10)

Quand on grep un contenu qu'on vient d'insérer, le pattern est la **ligne source littérale,
marqueurs markdown inclus** (`**gras**` compris). Un pattern « propre » sans marqueurs produit un
faux-zéro sur du contenu boldé. Classe tooling, pas inférence ; journal : `ops/QA-NOTES.md`.

## 1e · Resync git = précondition du tour (ruling King 06/10)

Au début de chaque tour, avant toute lecture ou édition : `git fetch origin`, puis vérifier la
précondition ci-dessous. La resync est une **précondition du tour**, pas une réparation après un push
refusé. Trois occurrences → protocole, pas vigilance.

**⛔ Plus de `git reset --hard origin/<branche>` automatique (ruling King 11/10).** L'ancienne ligne
disait « `reset --hard` si local ≠ remote ». Elle est **retirée** : `origin HEAD` pointe sur `main`,
dont l'historique est **disjoint** de la branche de travail (`git merge-base HEAD origin/main` = vide),
donc un `reset --hard origin/HEAD` remplace tout le travail du mois par le seul commit de `main`.
**Nouvelle règle : on ne reset PAS, sauf si (1) l'arbre est propre ET (2) le travail non poussé est
explicitement reconnu comme perdable.** Sinon : `git reset --mixed`, jamais `--hard`.

**Précondition mécanique avant TOUT commit — AMENDÉE (ruling King 11/10 ; remplace la règle d'égalité du 08/10) :**

```
git fetch -q origin
git merge-base --is-ancestor "$(git ls-remote origin refs/heads/<branche> | cut -f1)" HEAD   # rc = 0
```

Le **tip distant doit être un ANCÊTRE de HEAD** (aucune divergence). Vérifié **par commande, dans le
même appel que le commit**, jamais de mémoire. `rc ≠ 0` → **on ne commit pas**, on resynchronise d'abord.

**Pourquoi l'amendement :** l'ancienne précondition (`git log -1 --format=%H` **égal** au tip distant)
est **insatisfaisable après le premier commit local** tant qu'on n'a pas poussé — elle garantissait
elle-même sa propre violation. L'ancêtre est le vrai invariant : il dit « je suis strictement en
avance, personne d'autre n'a écrit ». Constat du 11/10, journalisé dans `ops/INFERENCE-ERRORS.md`.

**Après CHAQUE commit (ruling King 11/10) :** **pousser immédiatement**, puis vérifier
`git ls-remote origin refs/heads/<branche>` **égal au nouveau HEAD**. Un commit non poussé n'existe
que dans le bac à sable — cf. la note du 21/09 (« perdues au 13ᵉ recul du bac, leur push avait échoué »).

Recette éprouvée (avec travail non commité, **jamais** `--hard`) : `git fetch -q origin` → `R=$(git ls-remote origin refs/heads/arena/01a0f7ad-amk | cut -f1)` → `git reset -q --mixed $R` → vérifier `HEAD == R` → `git checkout HEAD -- leads/build/{crm.py,generators.lock.json,records.py,views.py}` si ces quatre fichiers reviennent périmés → `git status --short`. (`origin/<branche>` peut ne pas exister comme ref locale : le tip se lit par `ls-remote`.) Le `reset --hard` de la ligne ci-dessus ne vaut que pour un arbre propre.

## 1f · Outils installés — usage proactif, sans que King ait à les nommer (ruling King 19/10)

> *King 19/10 : « I shouldn't always tell you when to use them… when you need to answer a question or research something you should always use agent reach… when we finish a website and it is ready to be delivered you can use brag. »*

**La règle : King ne nomme jamais l'outil.** Quand la tâche tombe dans l'un des deux cas ci-dessous, l'orchestrateur charge la chaîne, l'utilise, et **le dit dans son en-tête pré-vol** (canal/backend ou livrable produit). L'environnement ne survit pas entre sessions : si l'outil est absent, l'orchestrateur le **réinstalle tout seul** avant de travailler (`bash tools/agent-reach/install.sh --system --channels=all` · `bash tools/brag/install.sh` — installations approuvées le 19/10, hors dépôt, aucun sudo), sans demander.

### ① Recherche ou question qui demande le web vivant → **Agent Reach d'abord**

- **Portée :** toute information extérieure au dépôt — regarder/chercher YouTube, GitHub, le web, un RSS, Bilibili, la recherche Exa, les canaux sociaux quand ils sont configurés. Cas nommés : contrôles approfondis §1c, leçons YouTube (Weekly research), inspiration live (§2 étape 3), vérification d'un fait sur une plateforme, réponse à une question de King qui exige une source externe.
- **Procédure :** exports PATH (voir `tools/agent-reach/README.md`) → `agent-reach doctor --json` (**`active_backend` fait foi**, un ✅ doctor n'est pas une preuve) → lire les sections utiles de `~/.agents/skills/agent-reach/SKILL.md` → appeler **l'outil upstream directement** (`gh`, `yt-dlp`, `bili`, `mcporter`, `curl` Jina, `feedparser`…). Le résultat cité vient d'un **appel réel**, jamais du doctor.
- **Hiérarchie des sources inchangée :** un fait **interne** (client, pipeline, prix) se vérifie dans le dossier du dépôt d'abord (§0b, §0e). Agent Reach est le premier réflexe pour l'**externe**, pas un substitut au dossier.
- **Repli honnête :** canal bloqué par l'egress de la sandbox ou non configuré → le dire dans la réponse, puis basculer sur `web_search`/`fetch_page`. **Jamais** présenter un résultat natif « comme si » Agent Reach avait répondu. Un canal login manquant (cookie compte **dédié**) se signale à King en une ligne ; on continue avec ce qui est atteignable, on ne bloque pas la tâche dessus.

### ② Site fini, prêt à être livré → **brag de livraison produit d'office** (brouillon)

- **Déclencheur :** build terminé **et** portes §1b vertes, page prête à être livrée/déployée. L'orchestrateur produit alors un **brouillon** de vidéo d'annonce verticale ~20 s selon `tools/brag/README.md` (plan · `hyperframes check` 0 erreur · snapshots relus à l'œil · rendu · poster en frame 0 · `audit_video_motion.py` **OK**) et le présente à King **avec** le livrable, chemin consigné dans les build-notes.
- **Garde-fous inchangés :** rien n'est **publié ni envoyé au client** sans validation de King ; site client réel = que du vrai (pas de brag sur des photos d'illustration — briefs § « le site ne montre que du vrai ») ; étiquette de fiction sur concepts/démos ; tons `polished`/`app-store` pour santé/éducation ; musique générée ou licenciée seulement (jamais les pistes embarquées, licence non documentée).
- **Sortie hors dépôt** (`brag-output*/` ou `/home/user/…`, ignorée par git) : aucun mp4 versionné.

### ③ Site DM Optique modifié → **déploiement sur le projet Vercel de test, d'office** (ruling King 20/10)

> *King 20/10 : « deploy the new version on vercel, do this every time you carry out changes to the site ».*

- **Déclencheur :** tout changement du site DM Optique commité **et** poussé (portiques §1b verts) → l'orchestrateur déploie immédiatement ce commit sur le projet Vercel de test de King, sans qu'on le lui demande, et **vérifie en ligne** (état `READY` + lecture d'au moins une page modifiée).
- **Cible :** projet `dm-optique-sarl` (`prj_vnTP9SW2lGh2rMqH15oU6S5NZvob`, équipe `team_EWqUU5nnB2OitkqqnARZ7Qrl`), racine `hosting/previews/dmoptic`, alias `https://dm-optique-sarl.vercel.app`. Le projet n'est pas lié Git (pas d'auto-déploiement) : déclenchement explicite via le connecteur Vercel, source GitHub `arena/2fffee3b-amk`, cible `production` du projet de test. Pièges connus : outils connecteur à recharger chaque tour ; `git_source` = chaîne JSON, pas objet ; `list_deployment_files` renvoie 404 sur ce projet → vérifier par lecture de page.
- **Garde-fous inchangés :** Vercel = banc d'essai de King, pas une livraison client ; la production client (Cloudflare, domaine du cabinet) reste le geste de King après sa validation. L'id, l'état et le commit déployés se consignent dans `clients/dm-optic/build-notes.md` (+ Activity-Log).

### ④ Tâche design / build / revue de page → **taste-skill lu et appliqué** (ruling King 20/10)

> *King 20/10 : « before we go further I want you to install and use this [taste-skill] ».*

- **Portée :** construire, designer, redesigner, restyler ou relire une page publique (le périmètre du skill lui-même). L'orchestrateur réinstalle si absent (`bash tools/taste-skill/install.sh`, épinglé — voir `tools/taste-skill/README.md`), lit `~/.agents/skills/design-taste-frontend/SKILL.md` (+ les `references/` utiles), et **le dit dans son en-tête pré-vol**.
- **Procédure :** nouveau build = le « run » du skill (inventaire du sujet → argument → tirage de direction par `draw.mjs` → phrase-idée → copy deck → construction → portique `lint.mjs`/`inspect.mjs` → critique sur captures → mouvement → rapport honnête : direction tirée, redraws motivés, scores, contrôles **non** exécutés dits comme tels). Revue/restyle = le cas « existing page » du skill (avant/après mesurés). Sorties `.taste-skill/` ignorées par git.
- **Hiérarchie en cas de conflit :** les lois maison (`AMK-DESIGN-SKILLS.md`, protocole d'unicité §2) et les verrous client (identité figée, textes approuvés, « le site ne montre que du vrai ») **gagnent** sur les règles maison du skill. Un conflit se signale à King, jamais un restylage silencieux ; `--allow`/`taste-skill-ignore` seulement avec raison écrite. Aucune donnée client dans les requêtes `assets.mjs`.
- **Inspecteur dans la sandbox (jonction prouvée le 20/10) :** `inspect.mjs` tourne via le Chromium de la chaîne vidéo : `bash tools/video/install.sh` puis `CHROME_PATH=/tmp/amk-video/chrome-wrapper.sh` (recette : `tools/taste-skill/README.md`). Fichiers locaux OK ; URL live impossible (egress Chromium fermé) ; faux `font-fallback` possibles sur chemins absolus (son serveur sert la racine du dépôt). Si la jonction casse, le rapport le dit et seuls `lint.mjs` + les portiques §1b font foi.

### ⑤ Mouvement d'interface (créer ou auditer) → **design-motion-principles lu et appliqué** (ruling King 20/10)

> *King 20/10 : « install and use [kylezantos/design-motion-principles] ».*

- **Portée :** ajouter, modifier ou auditer transitions, animations, états de survol/pression, révélations au scroll, micro-interactions. L'orchestrateur réinstalle si absent (`bash tools/design-motion-principles/install.sh`, épinglé — voir son README), lit `~/.agents/skills/design-motion-principles/SKILL.md` + le workflow du mode (create/audit) + `references/accessibility.md` (obligatoire), et **le dit dans son en-tête pré-vol**.
- **Procédure :** reconnaissance du contexte → **pondération des trois lentilles écrite** (défaut santé/catalogue/conversion : Jakub primaire, Emil secondaire, Jhey sélectif — autre pondération seulement si King la demande) → checklist + anti-checklist → findings dans les build-notes du client (pas de dossier `motion-audits/` sans OK King, §4b). `prefers-reduced-motion` est non négociable ; un changement de motion sur le site DM = changement de site : portiques §1b + déploiement §1f③.
- **Hiérarchie :** lois maison et verrous client gagnent ; un conflit (ex. boucle d'ambiance d'identité) se signale à King, jamais de restylage silencieux.

### ⑥ Audit de production / vérification → **skills ECC sélectifs en appui** (ruling King 20/10)

> *King 20/10 : « install and use [affaan-m/ECC] ».*

- **Portée :** audit de pré-livraison, readiness, sécurité, SEO, accessibilité, parcours de clic, boucle de vérification — **en complément** des portiques maison, jamais à leur place. L'orchestrateur réinstalle si absent (`bash tools/ecc/install.sh`, épinglé — voir son README), lit le ou les `SKILL.md` pertinents parmi les six installés (`accessibility`, `production-audit`, `verification-loop`, `security-review`, `seo`, `click-path-audit`), et **le dit dans son en-tête pré-vol**.
- **Procédure :** preuves locales d'abord (build, portiques, diff, lectures de pages) ; score et blockers au format `production-audit` quand il sert ; findings consignés dans les build-notes du client avec correctif/amélioration/action (§0e).
- **Garde-fous :** installation **sélective seulement** — pas de profil full/core, pas de hooks runtime, pas de MCP, pas de mémoire ECC, pas d'auto-update, pas de scanner externe ni d'envoi de code/données client à un tiers sans l'accord explicite de King (règles TOOL-SCAN 3+4). Le harnais complet sur la machine de King est une décision séparée ; ne jamais empiler deux méthodes d'installation ECC sur la même cible.

### ⑦ Recherche UX/UI ponctuelle → **UI/UX Pro Max interrogé d'abord** (ruling King 20/10)

> *King 20/10 : « install and use [nextlevelbuilder/ui-ux-pro-max-skill] ».*

- **Portée :** avant de corriger ou concevoir un composant, interroger la base locale (`search.py --domain ux|typography|landing|icons|gsap…`, Python stdlib, aucun réseau, aucune donnée client dans les requêtes) — en complément de taste-skill et des lois maison.
- **Limite posée le 20/10 :** sa « design system » générée propose style/couleurs/typo **neuves** — sur un site à identité figée, elle est **écartée** (grille de lecture, pas direction) ; une identité neuve ne se choisit qu'avec King (protocole d'unicité §2).
- Réinstallation : `bash tools/ui-ux-pro-max/install.sh` (épinglé, voir son README). Dit dans l'en-tête pré-vol.

### ⑧ Détection d'anti-patterns UI → **Impeccable `detect` en portique d'appui** (ruling King 20/10)

> *King 20/10 : « install and use [pbakaus/impeccable] ».*

- **Portée :** `impeccable detect --json <pages>` en audit de finition, sur fichiers locaux ou URL ; chaque finding est **vérifié dans le code** avant toute correction (faux positifs nommés, ex. « cramped-padding » sur cartes à photo pleine bordure). Les commandes de polish (`polish`, `harden`, `critique`…) restent des propositions — un changement de site passe par le ruling de King, les portiques §1b et §1f③.
- **Garde-fous :** moteur épinglé (engine v0.1.16 au pin du 20/10) ; **aucun hook Impeccable installé** (activation séparée, décision de King) ; pas de PRODUCT.md/DESIGN.md dans le dépôt sans son OK (§4b) ; re-téléchargement du moteur seulement depuis le canal officiel de l'amont.
- Réinstallation : `bash tools/impeccable/install.sh` (épinglé, voir son README ; sur la machine de King l'installeur amont peut télécharger le moteur lui-même). Dit dans l'en-tête pré-vol.

### ⑨ Chaque tâche de King → PRE-FLIGHT lu en entier, inventaire des outils, propositions + audit en clôture (ruling King 20/10)

> *King 20/10 : « for each message/task I give read all the pre-flight document, go through all the skills and tools available/installed so that you know what to use and when, and at the end of each response write a proposition/recommendations and audit — you can leave it blank if there's nothing. »*

- **Ouverture (renforce §0) :** le document PRE-FLIGHT est **lu en entier** à chaque tâche (aucune section sautée) et l'en-tête pré-vol nomme **l'inventaire des outils/skills examinés pour la tâche** — lesquels sont utilisés, lesquels ne le sont pas, et pourquoi en une ligne (§1f①–⑧ inclus, plus `ops/TOOL-SCAN.md` comme registre). L'objectif est la **connaissance permanente de l'arsenal** : le bon outil au bon moment, sans que King ait à le nommer.
- **Clôture :** chaque réponse se termine par un **bloc debout à deux volets**, présent même vide (« Rien à signaler ») :
  - **Propositions / Recommandations** — étapes suivantes, optimisations du flux de travail, opportunités repérées en cours de route. Ce bloc n'ouvre **aucun droit d'exécution** : une proposition attend le ruling de King (§4b, verrous).
  - **Audit** — auto-audit honnête de la réponse : ce qui a été vérifié contre la source (§0e), ce qui reste incertain ou non testé, les défauts connus laissés ouverts, la conformité aux portiques (§1b/§1f③…). Un audit qui relève un problème porte correctif/amélioration/action (§0e), et **tout problème résoluble porte sa solution long terme** (règle debout, outil, contrôle automatisé — pas seulement le correctif ponctuel) : l'audit d'une réponse prépare celui d'après (ruling King 20/10).
- Le bloc s'applique **à toutes les réponses**, y compris les réponses courtes de consultation — c'est justement là que les propositions coûtent le moins et servent le plus.

### ⑩ La forme exacte de l'inventaire — et pourquoi elle existe (ruling King 23/10)

> *King 23/10 : « each time a decision is taken or a task is given or a question asked, go through all the
> tools and skills available to you then choose the ones suitable for the situation — I had already told
> you this, isn't it written in preflight ? »*

**Oui, c'était écrit — au ⑨ ci-dessus, depuis le 20/10.** Le ⑨ n'était donc pas un manque de règle : c'est
un **manque d'exécution**. Deux réponses du 23/10 n'ont pas porté l'inventaire. Une règle non appliquée
n'existe pas (§0e, « instruction ≠ état ») : le ⑩ lui donne une forme fixe, courte, impossible à oublier.

**Forme obligatoire — trois lignes, en tête de réponse, juste après le pré-vol :**

```
Outil  : [ce que j'utilise, et pourquoi en trois mots]
Écarté : [ce que j'ai examiné et laissé — une raison par outil]
Skill  : [skill chargé, ou « aucun : la tâche n'en appelle pas »]
```

**L'arsenal à passer en revue, chaque fois, dans cet ordre** (registre vivant : `ops/TOOL-SCAN.md`) :

| Famille | Ce que c'est | Déclencheur |
|---|---|---|
| **Connecteurs** | Notion (mémoire, miroir §0g) · Vercel (déploiement) · GitHub (`gh` : PR, issues, contenu) · Google Drive / Agenda | toute écriture de connaissance, tout déploiement, tout geste de dépôt |
| **Recherche** | `web_search` · `fetch_page` · **Agent Reach** (§1f①) | un chiffre à vérifier, une source à ouvrir, une vidéo à transcrire |
| **Skills installés** (§1f④–⑧, hors dépôt) | `design-taste-frontend` · `design-motion-principles` · `ui-ux-pro-max` · `impeccable` · ECC (`accessibility`, `production-audit`, `verification-loop`, `security-review`, `seo`, `click-path-audit`) | page publique, composant, mouvement, audit de livraison |
| **Portiques maison** (§1b) | `tools/ops/gate-amk.sh` · `tools/qa/audit_*.py` · `tools/qa/test_site_a11y_behaviour.mjs` | **avant toute publication** — les portiques maison font foi |
| **Outils média** | `tools/video/` (rendu, sous-titres) · `tools/record/` · `tools/pdf/` | toute pièce vidéo, capture, PDF |
| **Mémoire et journal** | `knowledge/` (§0c) · Notion (§0g) · `§10` journal des sources | **à chaque source nouvelle** — le journal s'ouvre à la réception |

**Deux cas où l'inventaire est court et c'est normal :** une question de conversation sans livrable
(trois lignes, « aucun skill »), et une tâche déjà couverte par le ⑨. **Zéro cas où il est absent.**

## 1g · Marketing, marque et création de contenu (ruling King 22/10)

> *King 22/10 : « make sure you have written everything you just learned in the repo, in preflight too under marketing, content creation and other relevant topics ». *

Toute tâche de **marketing, de marque, de vente optique ou de production de contenu** commence par ces
deux bases de connaissance, **avant** d'écrire une ligne de script ou de lancer un rendu :

| Fichier | Ce qu'il contient | Quand le lire |
|---|---|---|
| **`knowledge/MARKETING-OPTICAL-2026-10-22.md`** | l'ordre des leviers (avis > fiche > site > social), les 3 facteurs de Google, la vente optique (Laramy-K, Anagram), « être expert d'une chose », les chiffres sociaux, la structure de positionnement, **le cas Warby Parker**, les erreurs, le socle Cameroun | toute mission marketing, positionnement, acquisition, SEO local d'un client optique |
| **`knowledge/CONTENT-CREATION-2026-10-22.md`** | la chaîne de production (PIL → ffmpeg → portique), les 9 règles de fabrication, la structure de script en 5 temps, les 4 piliers, ce qui se mesure, **la politique visages / UGC / IA**, la règle de source, les portes avant publication | toute vidéo, tout post, toute production sociale |

**Routage rapide**

| La tâche | D'abord | Ensuite |
|---|---|---|
| positionner une marque, écrire un statement | `knowledge/MARKETING-OPTICAL…` §6 | `clients/<client>/brand/BRAND-STRATEGY-*.md` |
| **créer, réparer ou optimiser une page sociale** (Facebook, Instagram, TikTok) | `brand/AMK-PRESENCE-2026-10-22.md` **§14** (l'audit des trois profils réels : les sept défauts, la copie exacte Instagram/TikTok, la règle des identifiants) + **§13** (identité des trois comptes, fusion de pages, lien page ↔ Instagram) + §12 (les onze champs Facebook) + §10 (protocole captures) · `sales/research/2026-W43-techniques.md` §15 (audience vs communauté, cadence, mesure) | le §3 de PRESENCE uniquement pour les visuels déjà validés — l'arbitrage du nom est au §12.0 ; **une promesse de délai ne va jamais dans une bio sans sa condition** (§14.5) |
| écrire un script court | `knowledge/CONTENT-CREATION…` §3 **puis §3 bis** (gabarit 9 blocs, rehook) et **§3 ter** (4 S + banque de hooks) | le gabarit du mois (`content/month1/…`) |
| choisir **le type de contenu selon l'objectif** (être connu / faire écrire / créer l'urgence / filtrer) | `knowledge/CONTENT-CREATION…` §4 bis | l'objectif du mois, écrit dans le plan |
| poser un **aimant à prospects** (opt-in unique) | `knowledge/CONTENT-CREATION…` §5 bis | `sales/lead-magnets/` + `tools/ops/make_magnet.py` |
| faire signer un **nouveau client** | `ops/templates/CONTRAT-UNE-PAGE-2026-10.md` | `sales/REVUE-CONTRATS-GRILLE…` addendum 23/10 |
| monter une vidéo | `knowledge/CONTENT-CREATION…` §1–2 | `tools/record/` + **portique** `tools/qa/audit_video_motion.py` (§1b) |
| monter une vidéo **UGC** (storyboard, produit, cartons, clip IA, voix) | `tools/ugc/README.md` | `python3 tools/ugc/ugc.py render <spec>.json --qc` |
| obtenir un **plan d'humain** / choisir un générateur, avec un prix | `research/ugc-video/2026-10-22-TOOLCHAIN-UGC.md` | `tools/ugc/providers.py` (Veo 3.1, HeyGen, Hedra, fal) |
| décider d'un contenu avec visage / IA | `knowledge/CONTENT-CREATION…` §6 | ruling de King — jamais de production avant |
| sourcer un chiffre pour un client | `knowledge/MARKETING-OPTICAL…` §9 + `CONTENT-CREATION…` §7 | la source primaire nommée, sinon « non revérifié » |
| **écrire un post, un sous-titre, une légende, un DM** | **`tools/qa/audit_claims.py`** (verrous client : prix, stock, superlatifs, allégations) | `knowledge/CONTENT-CREATION…` §6 bis |
| écrire à un gérant de clinique / opticien (prospection, DM froid) | `knowledge/OUTREACH-MESSAGING-2026-10-22.md` | vérifier la position réelle **avant** d'écrire |

**Deux règles debout issues du 22/10 :**

1. **Aucune statistique sans source primaire nommée n'entre dans une décision client.** Ce qui n'a pas pu
   être revérifié est **écrit comme non revérifié**.
2. **Un contenu qui ne porte aucune preuve de la marque est joli, pas utile.** Les preuves sont listées
   dans `clients/dm-optic/brand/BRAND-STRATEGY-2026-10-22.md` §6 (modèle transposable aux autres clients).

**Ce que ces sections ne remplacent pas** : les portiques §1b (livraison) et le ruling de publication —
**rien n'est publié sans validation de King**.

## 1h · Règles commerciales debout (rulings King, 23–24/10)

Quatre règles, valables jusqu'à ce que King les change — elles ne se rediscutent pas en cours de
devis, et elles ne se « réinterprètent » pas au cas par cas.

| # | Règle | Ce qu'elle interdit en pratique | Où elle s'applique |
|---|---|---|---|
| 1 | **Plafond de 5 clients récurrents** | prendre un 6ᵉ client mensuel sans passer la main ou monter le prix ; empiler des Suivi « pour le volume » | `knowledge/PRIX-2026-10-24.md` §5 · `knowledge/MAINTENANCE-CLIENTS-2026-10-22.md` · `ops/ROADMAP-AMK-POST-DM-OPTIC-2026-10-22.md` |
| 2 | **Présence ne dépasse jamais 3 pages** | glisser 4, 5 ou 6 pages « pour faire plaisir » dans le palier à 150 000 ; appeler « Présence » un site qui est un Standard | `knowledge/PRIX-2026-10-24.md` §4 · `site/index.html` · `site/en/index.html` · pages de niche |
| 3 | **La grille ne vaut que pour la prochaine signature** | appliquer rétroactivement 30 000 ou 75 000 à un contrat accepté avant la grille (cas DM OPTIQUE : figé à 30 000) | `knowledge/PRIX-2026-10-24.md` §5 · `ops/FACTURATION-2026-10-24.md` |
| 4 | **Aucune remise, jamais : on change le périmètre** | baisser un prix pour clore ; offrir une page, un mois, une vidéo « pour compenser » | `sales/PRIX-ET-RECURRENCE-2026-09-24.md` · `sales/AMK-Sales-Playbook-v2.md` |

**Le calcul derrière la règle 1** (à connaître par cœur, il tient en une phrase) : les charges fixes
de King sont de **85 000/mois** ; trois Suivi à 30 000 = 90 000, soit le point d'équilibre exact. Un
4ᵉ et un 5ᵉ client sont les premiers qui paient réellement — au-delà de cinq, la qualité du travail
mensuel (4 h par Suivi, 12 h par Croissance) ne tient plus, et ce sont les livrables qui cassent.

## 1i · Versionnage : quand on fusionne une branche

> **Règle King 23/10, corrigée par lui le 23/10 : « I told you to merge only at a milestone or 1k
> commits, but I meant 1k changes. »** Le seuil porte donc sur **les lignes changées**, pas sur le nombre
> de commits — un tour peut faire 1 commit et 1 200 lignes, ou 12 commits et 40 lignes.
> **Les trois seuils ci-dessous sont validés par King le 23/10** (message du soir, point 5).

Par défaut, chaque tour **pousse** sur la branche de session et **laisse la PR ouverte**. On fusionne
dans `main` quand l'un de ces trois est vrai :

| Déclencheur | Seuil | Comment il se lit |
|---|---|---|
| **Jalon** | une étape finie et utilisable seule | à la main, en une phrase |
| **Volume** | **≈ 3 000 lignes changées** ou **40 fichiers** | `git diff --numstat <base> HEAD \| awk '{a+=$1;d+=$2} END{print a+d}'` |
| **Durée** | **6 tours** sur la même branche | compté dans le journal |

**Pourquoi 3 000 et pas 1 000.** 1 000 lignes se font en un tour dense (le 23/10 : quatre tours ont
dépassé 700 lignes chacun). À 1 000, on fusionnerait tous les deux tours, et `main` deviendrait illisible.
3 000 correspond à ce qu'une relecture humaine peut encore suivre d'un œil, et à ce que nos portiques
savent encore vérifier.

**Ce que « la mémoire » veut dire ici, honnêtement.** La taille de la branche n'abîme pas la mémoire de
l'orchestrateur : il relit ses fichiers à chaque tour, et le dépôt est la source de vérité. Ce qui se
dégrade, c'est **autre chose** :

1. **le résumé de session** — à chaque tour, la conversation est condensée ; ce qui n'est pas écrit dans
   un fichier finit par se perdre. **La défense n'est pas de fusionner, c'est d'écrire.**
2. **la relecture du diff** — au-delà de ~3 000 lignes, plus personne ne relit vraiment, et une erreur
   passe.
3. **le nombre de décisions en vol** — au-delà d'une dizaine de règles annoncées dans un même tour sans
   être écrites, elles se contredisent.

**Le garde-fou anti-hallucination n'est donc pas un compteur, c'est le §0e** : on vérifie un chiffre, une
règle ou un état **contre la source**, jamais contre son souvenir du tour précédent. Le compteur de lignes
protège la relecture, pas la vérité.

**Application :** la PR d'une branche en cours reste ouverte entre deux tours ; on ne la ferme pas « pour
ranger ». Le volume se lit avec `git diff --numstat $(git merge-base HEAD origin/main) HEAD`.

### 1i bis · Avant toute fusion : `fetch`, puis regarder `main` (ruling King 23/10)

> *King, 23/10 : « can you do a git pull or a git fetch before merging ? »*

**Oui, et c'était le vrai défaut du 23/10 :** la PR a été fusionnée sans avoir regardé `main` une seule
fois dans le tour ; GitHub a répondu « head branch is out of date ». Le `fetch` n'est pas une formalité,
c'est ce qui révèle **trois cas** qu'aucune autre commande ne montre :

| Ce que le fetch révèle | Ce qu'on fait |
|---|---|
| `main` a avancé normalement | on **fusionne `main` dans la branche**, on résout, on repousse |
| **`main` a été réécrit** (aucun ancêtre commun) | on **ne force rien** : on dit à King ce qui s'est passé, et on demande avant de toucher à l'histoire du dépôt |
| `main` a bougé ET le diff touche les mêmes fichiers | on relit le diff de `main` **avant** de résoudre, jamais `-X ours` en aveugle |

**La séquence, toujours dans cet ordre :**

```bash
git fetch origin
git log --oneline -3 origin/main            # main a-t-il bougé ?
git merge-base HEAD origin/main || echo "AUCUN ANCETRE — main a été réécrit"
git diff --stat origin/main HEAD | tail -5  # l'écart réel, en fichiers
# puis seulement : fusion locale, push, et fusion de la PR
```

**Ce que le 23/10 a appris concrètement :** `main` porte un commit unique « invoice » (14h34) sans ancêtre
commun avec la branche de session. Mais **son arbre est identique à celui de la base de la branche, plus un
fichier** (`amk-factures-pwa.zip`). Autrement dit : une réécriture **sans perte de contenu** — vérifiable
en une commande (`git diff --stat <base> origin/main`), et c'est cette vérification qui autorise une fusion
sereine, pas la confiance.


## 2 · Uniqueness protocol (every website/design build, before a line of HTML)

1. Load design + copywriting lessons (routing table rows above) and re-read `AMK-DESIGN-SKILLS.md` (dials §2, Design Read §1, anti-default §3/§3.8, pre-flight §13, §19).
2. Load client context — everything we know: brief, niche, what they actually do, who they serve, tone, existing brand assets, intake notes (dossiers in `sales/research/`, `clients/<client>/`).
3. **Go online for live inspiration — never from memory.** At least **3 distinct references from different angles** (structure/layout · colour-typography · imagery/motion/tone), from Awwwards, Godly, Land-book, SiteInspire, Mobbin, Lapa Ninja, Dribbble, or adjacent-market school/clinic sites. For each: **URL · what we take (specifically) · what we reject.**
4. **Check `clients/_uniqueness-registry.md`** and `demos/` — if the direction resembles something we already built, throw it out and re-research.
5. **Write the Design Read line** (dials + inspiration direction + how it ties to this client). No build starts without it.
6. **Differentiate on ≥ 4 axes:** layout · palette · typography · imagery treatment · section order · motion · copy tone. Colours alone = a reskin, not a site.
7. Build per house standard: single-file HTML, base64 images, mobile-first, EN|FR pairs, WhatsApp-first CTAs.
8. Run §13 pre-flight before delivery.

**Web-access fallback:** if live research is impossible (no network / fetch fails), **say so immediately** and propose: King pastes screenshots · work from a curated file · defer the build. Never invent "inspiration" from memory and call it research.

## 3 · Per-client logging (non-negotiable)

- `clients/<client-name>/inspiration.md` — every reference: URL, taken, rejected, plus the Design Read line.
- `clients/<client-name>/build-notes.md` — decisions: dials, why this layout/palette/copy angle.
- `clients/_uniqueness-registry.md` — one line per delivered site: client · niche · dominant fingerprint (layout archetype + palette family + type system + tone).

## 4 · Lesson-update discipline

- A task that teaches something (a tactic that worked, a reference that landed, a copy angle, a design move) → **append a dated entry** to the relevant lessons file the same day, naming the client/task. Don't wait for Monday.
- **Never overwrite a lesson silently** — add, annotate or version (same rule as the playbook).
- **Conflicts:** say so; ask which side wins, unless the newer lesson is clearly stronger for Cameroon clinics/schools — then propose the change and wait for King's yes.
- **Friday report — « Knowledge applied » line (02/10) :** quels domaines de
  `knowledge/HOUSE-KNOWLEDGE-BASE.md` ont servi cette semaine, ce qui a marché, ce qui est à réviser ou à
  tester. Se remplit depuis le change log de la base. **Format standing du rapport** (`content/pipeline/reports/`) :
  mouvement pipeline · cadence contenu · nombres de funnel · appris · ensuite · Knowledge applied ·
  **« Blockers requiring King ruling »** — ce qui est bloqué sur King, pour que rien n'attende en silence.

### 4b · Un fichier debout NOUVEAU exige la confirmation de King (ruling King 11/10)

> **New standing files require King's confirmation before becoming repo law.** Quand un lot de
> recherche produit une checklist ou une règle qui doit atterrir dans un **nouveau** fichier,
> l'orchestrateur **propose l'emplacement** ; King approuve ; ensuite seulement c'est committé
> comme loi. Empêche les standards d'entrer en silence.

Application pratique : une règle qui peut rejoindre un fichier existant **va dans ce fichier**
(exemple du 11/10 : la règle des sous-titres manuels est entrée dans
`content/strategy/CONTENT-STRATEGY-V2-2026-10-05.md`, pas dans un fichier neuf). Un fichier neuf
n'est créé qu'avec le oui de King. Le premier cas d'application : la
`content/strategy/TIKTOK-SEO-CHECKLIST-2026-10.md` du lot [36], créée avant l'existence de cette
règle et **approuvée par King à l'acceptation du lot 1** le 11/10.

## 5 · Standing lens (everything filters through this)

WhatsApp-first · mobile-first · EN|FR · Cameroon (Kumba/Douala/South-West) · clinics & schools · one client closed by 30 Sep · 500 000 FCFA/month by month 6. A lesson that doesn't serve this doesn't get applied.
