# TOOL SCAN — discipline hebdomadaire (ruling King 06/10)

> **Slot :** dimanche 20h00 WAT, avant le State of Play du lundi. **Append-only** : une entrée par
> semaine, **max 3 outils**. Qualité, pas quantité. Première scan : **dimanche 11/10**.
>
> **Format par outil — quatre lignes :** (a) problème qu'il résout · (b) use case AMK nommé ·
> (c) coût · (d) effort d'adoption + verdict (pursue / skip / hold).

**Règles qui lient la scan (ruling King 06/10) :**

1. **Pas d'outil adopté sans problème nommé.** « pourrait servir » n'est pas un problème → skip.
2. **Gratuit / open source d'abord.** Payant seulement si ROI prouvé et petit (< 20 000 FCFA/mois à
   ce stade).
3. **Aucun outil en production avant que King l'ait utilisé une fois personnellement** sur une vraie
   tâche.
4. **Aucun outil ne touche des données client avant que King ait lu ses conditions** (cliniques et
   opticiens : risque privacy).
5. **Aucun outil n'ajoute de l'état à maintenir sauf s'il retire plus de travail qu'il n'en crée** —
   hosting, config, backup = coût mensuel caché, à compter.

---

## 05/10 — entrée FONDATRICE : Mira (github.com/miracodeai/mira, ruling King : skip)

- **(a) Problème :** relecture automatique de PR code, self-hosted, BYO LLM key.
- **(b) Use case AMK :** second lecteur automatique sur les PR arena→main.
- **(c) Coût :** hosting permanent (webhooks) + tokens LLM par PR ; AMK n'a ni serveur persistant ni
   volume de PR — le sandbox reset à chaque tour.
- **(d) Effort + verdict :** GitHub App + deploy Docker + clé OpenRouter pour un workflow à un humain
   + un agent déjà couvert par le protocole de vérification → **skip**. Triggers de re-review : 2e dev
   humain · repo code client · PR volume. La ruling Mira = template de la scan.

---

## TÂCHE HEBDOMADAIRE NOMMÉE — « Re-scan crédentiels » (ruling King 08/10)

- **Quand :** chaque **dimanche 20h00 WAT**, avec la tool-scan (même créneau, deux tâches distinctes).
- **Quoi :** relancer la grille de `content/strategy/RULE-CREDENTIAL-CLAIMS.md` (commande non filtrée)
  sur **tout le dépôt** ET sur **chaque URL publique d'une page construite par AMK** (liste tenue dans
  `ops/QA-NOTES.md`). Résultat journalisé ici, une ligne par scan : date · périmètre · hits · action.
- **Règle permanente — pages en ligne :** toute URL publique d'une page AMK reçoit le balayage crédentiels
  **contre l'URL servie** (`fetch_page` / lecture de la page en ligne), pas seulement contre le dépôt : la
  page déployée peut être en retard sur le dépôt (cas du 08/10 : `dmoptic-2.vercel.app` servait encore
  « depuis 2016 » alors que le dépôt était corrigé).
- **Gel :** pour les pages gelées (Le Cristallin, Univers Optique — `hosting/previews/README.md`), le re-scan
  **lit et signale seulement** ; aucune modification sans mot de King.
- **Premier scan en ligne (08/10) :** voir `ops/QA-NOTES.md`, table « Balayage des pages publiques ».

- **Liste d'attente du scan du dimanche 11/10 (ruling King 08/10) :** `uni-labo.vercel.app` — tracer « Dr Tientcheu
  Philomène, Biologiste » à une source de dossier (sinon « Notre biologiste ») · 2ᵉ moitié de `uni-labo` et de
  `cavisa` · `amk-cm.vercel.app` + ses pages · relecture en ligne de **`dm-optique-sarl.vercel.app`** (en-tête compris : `og:url`, `og:image`) ;
  `dmoptic-2` est hors périmètre (abandonnée, King 08/10).
- **Ajout 08/10 (revue Search Console) :** export Search Console d'`amk-cm` chaque dimanche 20h00 sous
  `research/gsc/AAAA-MM-JJ/` + une ligne ici (clics · impressions · position · requêtes). Repère du
  08/10 : 1 clic · 1 impression · position 3,0 sur 7 jours. Liste d'attente : rapatrier les pages
  live-only d'`amk-cm` (polyclinic, maternity) avant tout redéploiement.

---

## Journal des scans

| Date | Périmètre | Hits | Action |
|---|---|---|---|
| **11/10** | **Grille crédentiels non filtrée sur le dépôt** (`grep -rIn "2016"` · `"2017"` · regex claims) | 92 lignes « 2016 » · 25 lignes « 2017 » · 160 lignes regex, dont **26 dans du HTML construit** (15 fichiers) | **Aucun hit nouveau.** Les 26 se répartissent en trois classes déjà tranchées : Cristallin « depuis 2010 » (leurs mots, à valider par lui) · Univers « depuis 2009 » sous gel du 23/09 (`univers-note/`, `univers-v1/`, les 4 `concept-univers-*`) · Cinq Sens « diplômés en optique lunetterie » (leurs mots). **Rien modifié.** `hosting/previews/univers/index.html` = 0 occurrence (ruling 08/10 tenu). |
| **11/10** | **Même grille, pages AMK publiques** (`site/`, déployé sur `amk-cm.vercel.app`) | 4 lignes : « Certified & vetted staff », « vetted and certified staff », « Certified science practicals » dans `sample-nursery.html` (3) et `sample-school.html` (1) | **Observation, pas une infraction** : ce sont les maquettes **fictives** (Little Oaks, Nova), pas un claim sur un client réel — donc hors du périmètre de `RULE-CREDENTIAL-CLAIMS.md`. Mais elles sont **publiques et indexables** : à garder à l'œil si un prospect les lit comme une promesse. Aucune modification sans mot de King. |
| **11/10** | **Re-pull ONOC** — `annuaire-des-opticiens-par-region/` (LITTORAL 85–159) + `liste-de-tous-les-opticiens-inscrits-au-tableau/` (complet), via `fetch_page` (`curl` bloqué sur ce domaine : HTTP 000) | **8/8 numéros de la liste d'envoi conformes à l'annuaire** · **4 divergences entre les deux pages ONOC** (FABY, JiredOptic, KamaïsOptic, Centrale) · 1 cas d'entité : le numéro de Bali est publié sous « Optic-Swiss Sarl » | **Aucun numéro corrigé.** Règle écrite dans `sales/LISTE-OPTICIENS-2026-10.md` : l'annuaire gagne, et en cas d'échec de livraison on teste le second numéro avant de classer. **Opener Bali sans aucune mention de l'Ordre.** Détail complet dans ce fichier. |
| **11/10** | **Pages live non balayées** | — | `dm-optique-sarl.vercel.app`, `uni-labo.vercel.app`, `cavisa`, `amk-cm` : **non lus** — `curl` depuis le bac à sable renvoie HTTP 000 (SSL bloqué). Le re-pull ONOC a prouvé que `fetch_page` atteint des domaines que `curl` n'atteint pas : **le balayage des pages live passe par `fetch_page`, pas par `curl`.** À faire avant tout partage d'URL. |

---

## 11/10 — scan hebdomadaire (dimanche 20h00 WAT) · 3 outils, maximum respecté

> Chaque outil part d'un **problème nommé** et daté, tiré du dépôt — pas d'un « pourrait servir »
> (règle 1). Les trois problèmes ci-dessous ont tous été rencontrés **cette semaine**.

### ① Script maison `tools/onoc/pull_registry.py` — **PURSUE (sous condition)**

- **(a) Problème :** les numéros de l'annuaire ONOC sont **transcrits à la main**. Le protocole du 05/10
  existe précisément pour ça (« risque de transposition des 7 numéros »). Le re-pull du **11/10** l'a
  prouvé : **4 divergences** entre les deux pages de l'Ordre (FABY, JiredOptic, KamaïsOptic, Centrale),
  trouvées à l'œil sur ~180 lignes, **et** un cas d'entité (le numéro de Bali publié sous
  « Optic-Swiss Sarl »). Une lecture à la main ne garantit rien.
- **(b) Use case AMK nommé :** la vague opticiens (12→22/10, 10 envois) puis chaque vague suivante ;
  la vérification croisée annuaire ↔ liste des inscrits **avant** tout envoi froid.
- **(c) Coût :** **0 FCFA.** Script maison, aucune dépendance payante, aucune donnée client.
  Précédent au dépôt : `tools/outreach/scan_reviews.py` (+ son test, 12 assertions).
- **(d) Effort + verdict :** faible (2 pages, 1 fois/semaine, sortie = instantané daté sous
  `research/onoc/AAAA-MM-JJ/`, même convention que `research/gsc/`). **PURSUE**, sous deux conditions :
  **règle 3** — King relit la première sortie avant qu'elle serve à un envoi ; **règle 5** — l'instantané
  daté remplace la transcription manuelle, il n'ajoute pas un état à tenir. ⚠️ Ne change rien à la règle :
  **un numéro non re-vérifié ne part pas**, script ou pas.

### ② Meta Business Suite / Messenger — **HOLD**

- **(a) Problème :** **15 des 18 pistes clinique/labo « jamais contactées » sont marquées « NE PAS
  ENVOYER »** (pas sur WhatsApp, numéro erroné, ligne fixe, introuvable) — le réservoir WhatsApp réel
  est de **3**, et ces 3 ont déjà un site (correction de l'orchestrateur, 10/10 17:00). King a tranché
  le 10/10 : **Messenger** pour ces cliniques et labos.
- **(b) Use case AMK nommé :** toucher les cabinets joignables uniquement par Messenger, sans brûler
  la liste WhatsApp.
- **(c) Coût :** 0 FCFA (Page existante `@amkweb`).
- **(d) Effort + verdict :** **HOLD.** La recherche du 10/10 est **contradictoire et datée** : l'aide
  officielle parle de 10 demandes/jour « en cours de déploiement, pas disponible pour toutes les Pages »
  et exige que le destinataire autorise les messages ; des sources tierces de 2024 disent qu'une Page ne
  peut pas écrire à une Page. **Règle 4 : des données client (cabinets) sont en jeu → King lit les
  conditions avant tout usage.** Verdict : vérifier **dans la Page elle-même** avant de bâtir un plan ;
  aucun envoi Messenger tant que la capacité n'est pas constatée.

### ③ Facebook Sharing Debugger (cache Open Graph) — **PURSUE (usage King)**

- **(a) Problème :** le lien DM Optique envoyé le **10/10 11:38** s'est affiché **sans vignette** sur la
  carte d'aperçu, puis **toujours sans vignette** à 12:12 — le client a reçu un lien nu deux fois. Cause
  probable : cache WhatsApp d'un lien déjà partagé avant le correctif. `og.jpg` existe au dépôt
  (1200×630, 75 Ko) et `og:image` est en adresse absolue.
- **(b) Use case AMK nommé :** forcer la re-lecture des balises `og:` avant **chaque** envoi de lien à un
  client — DM Optique d'abord, puis chaque aperçu de site.
- **(c) Coût :** 0 FCFA.
- **(d) Effort + verdict :** nul (une URL à coller). **PURSUE** — c'est exactement un outil de la
  **règle 3** : King l'utilise une fois personnellement sur `dm-optique-sarl.vercel.app`, et le résultat
  (vignette présente ou non) tranche entre « cache » et « fichier ». Aucune donnée client envoyée : l'URL
  est déjà partagée avec le client. À ajouter au protocole d'envoi de lien.

### Rattrapage append-only — ruling absent du journal

- **« Website builder » = SKIP** (ruling cité dans la passation du 11/10, **aucune entrée au journal**).
  Motif rapporté : **pas d'images, pas de direction artistique** — ce qui est précisément l'axe de
  différenciation d'AMK (`AMK-DESIGN-SKILLS.md` §15). Conforme à la règle 1 (pas de problème nommé que
  l'outil résolve mieux que le processus actuel). ⚠️ **[À CONFIRMER — King]** : **quel** builder a été
  évalué (Wix / Framer / Durable / autre) ? Sans le nom, l'entrée n'est pas réutilisable et le sujet
  reviendra. **Mise à jour 12/10 :** journalisation de mémoire faite sur ruling King →
  `research/BUILDER-TEST-KING-2026-10.md` (sortie texte seule confirmée ; nom du builder toujours à
  confirmer). Triggers de re-review : un client demande un site auto-géré · un volume de sites que la
  chaîne actuelle ne suit plus.

## 11/10 (nuit) — audit stack GTM (Lot [40], batch 5)

Règle debout issue de l'audit : **jamais de signaux « sur étagère » ni de stack GTM payant sans
profit qui le justifie** (biais gratuit/open-source). Verdicts : Clay (~800 $/mois ; alt open source
buildingopen/opengtm) **REJETÉ à l'échelle AMK** · Apollo payant **REJETÉ** (free 900 crédits sans
donnée opticiens Cameroun) · Instantly/Smartly **REJETÉS** (volume email ≠ WhatsApp-first) ·
Salesforge + Forges **REJETÉS** (vendor sponsorisé, scaling multi-comptes LinkedIn = risque ToS +
réputation) · HubSpot/Salesforce CRM **REJETÉS** (crm.py maison = source de vérité) ·
**n8n Community Edition (self-host, gratuit) = HOLD** : couche connecteur future si le volume
l'exige, jamais avant · ChatGPT/Gemini free = déjà remplacés par l'orchestrateur
(orchestrator-first confirmé : find → enrich → first-line research → route = crm.py + sweeps).

---

## 19/10 — Agent Reach (installation demandée par King, hors scan hebdomadaire)

> Demande King du 19/10 : « Install https://github.com/Panniantong/Agent-Reach » ; choix tranchés
> par King le même jour : `--system`, **tous les canaux**, dossier `tools/agent-reach/`.
> Détail vérifié canal par canal : `tools/agent-reach/README.md`.

- **(a) Problème :** l'agent ne sait pas lire le web vivant sans réinventer chaque accès —
  sous-titres YouTube pour `research/YouTube-Lessons.md`, canaux discrets des prospects exigés par
  le contrôle approfondi `PRE-FLIGHT.md` §1c (YouTube, X/Instagram, Facebook), pages web rendues
  en HTML brut, RSS/GitHub au cas par cas. Chaque plateforme a sa propre porte (API payante,
  login, anti-bot) et la bonne porte change (l'amont documente une rotation rien qu'en 2026).
- **(b) Use case AMK nommé :** §1c sur les prochaines vagues (cliniques/écoles de Douala vivent
  sur Facebook/Instagram — canaux desktop OpenCLI sur la machine de King) · extraction des leçons
  YouTube par sous-titres `yt-dlp` · lecture de pages (Jina) et recherche (Exa) pour la recherche
  hebdomadaire · GitHub/RSS déjà prouvés le jour même (appels réels).
- **(c) Coût :** **0 FCFA** (MIT, tout l'écosystème est open source ; seul coût possible un jour :
  proxy serveur ~1 $/mois, inutile en local — rien acheté). État à maintenir (règle 5, compté) :
  `~/.agent-reach-venv` (~92 Mo) + `~/.agent-reach/` + `~/.mcporter/`, **hors dépôt** (règle
  upstream : jamais de token dans l'espace de travail) + un ré-épinglage version/commit à chaque
  mise à jour dans `tools/agent-reach/install.sh`.
- **(d) Effort + verdict :** installé le 19/10 (v1.5.0, commit `94f06c1` épinglé) — `doctor` :
  4/16 canaux ✅, mais prouvés **par appels réels** depuis la sandbox : **GitHub + RSS seulement**,
  le reste étant bloqué par l'egress du bac à sable (GitHub/PyPI/npm uniquement) ou en attente
  d'input King (cookies Twitter/Reddit, clé Groq, Chrome desktop pour Facebook/Instagram).
  **PURSUE sous conditions** : règle 3 — King l'essaie sur **sa** machine (la seule où
  YouTube/FB/IG peuvent répondre) sur une vraie tâche avant tout usage production ; règle 4 —
  aucun cookie de compte principal, **aucune donnée ni compte client**, comptes secondaires
  dédiés uniquement (risque de ban documenté par l'amont). Triggers de re-review : premier usage
  King concluant (→ usage libre sur §1c) · un canal qui casse deux fois (→ repli sur la méthode
  manuelle actuelle) · sortie d'une version amont (→ procédure `update.md` + ré-épinglage).

---

## 19/10 (soir) — brag (latent-spaces/brag) : analysé, puis installé et prouvé à la demande de King

> Analyse d'abord (verdict HOLD → test borné), puis King : « I want you to be able to use both
> brag and agent reach here ». Chaîne installée le même soir, preuve de bout en bout sur la démo
> fictive opticien. Détail : `tools/brag/README.md`.

- **(a) Problème :** à la livraison d'un site, le client n'a **rien de partageable** pour
  l'annoncer (statut WhatsApp) ; nos 5 démos anonymisées sont des liens, pas des preuves qui
  circulent. DM Optique est en ligne depuis le 16/10 et le forfait mensuel doit produire du
  contenu dès le départ.
- **(b) Use case AMK nommé :** vidéo d'annonce de ~20 s à **chaque livraison de site** (rituel
  inclus au pack, le client la partage = exposition AMK) + teasers des démos pour l'outreach.
  **Pas un service séparé** à ce stade : aucun client ne le demande seul, et le goulot actuel
  est la clôture du client n°2, pas un format de plus.
- **(c) Coût :** **0 FCFA** (skill MIT + Hyperframes Apache-2.0 en rendu local ; l'hébergé
  letsbrag.app à 19 $/vidéo n'est pas retenu). État à maintenir (compté) : runtime
  `/tmp/amk-brag` + Chromium partagé avec la chaîne vidéo + épinglages (brag `069432c`,
  hyperframes `68b873f`/CLI 0.8.177) dans `tools/brag/install.sh`.
- **(d) Effort + verdict :** **INSTALLÉ + PROUVÉ, production sous conditions.** Le 19/10 :
  doctor Hyperframes au vert dans la sandbox (parades : wrapper Chromium @sparticuz, GSAP
  vendored, ffprobe npm embarqué) et brag complet sur `opticien-demo.html` (fictif) — 17 s,
  1080×1920, check 9/9 contraste, **portique `audit_video_motion` OK** après correctif (hook
  figé 0–2 s → zoom lent continu : chaque scène bouge pendant toute sa durée). Conditions
  debout : **règle 3** — King visionne la preuve et l'essaie avant tout usage client ;
  **musique embarquée interdite** (licence ende.app non documentée, issue amont #59 ; fond
  généré ou licencié à la place) ; tons `polished`/`app-store` seulement pour la santé ;
  DM Optique seulement **après** les vraies photos. Triggers de re-review : première annonce
  client livrée et partagée (→ rituel standard) · licence musique clarifiée en amont ·
  ruling King sur la narration pour ce format (la VO TikTok reste Flow).

---

## 19/10/2026 — Édition photo client locale (détourage IA) : rembg + modèle ISNet (tools/photo/)

- **(a) Problème nommé (19/10) :** King a reçu les photos du client DM (montures + cabinet,
  téléphone) ; elles doivent être nettoyées avant d'entrer sur le site (catalogue `/montures/`
  vide, « Photo d'illustration » ×2 en prod). Service cloud écarté d'office (règle 4 : données
  client chez un tiers = King lit les CGU d'abord) → chaîne **100 % locale**.
- **(b) Choix :** détourage IA ONNX (CPU) + corrections Pillow classiques, encapsulés dans
  `tools/photo/prep.py` (2 modes : `catalogue` = détourage + fond uniforme 4:3 1600×1200, le
  contrat de `build_dmoptic_montures.py` ; `clinique` = niveaux/netteté, **aucun détourage**).
  rembg (MIT) est la voie normale mais ses poids (release assets GitHub) sont bloqués par
  l'egress sandbox → modèle ISNet « medium » reconstruit depuis les chunks du paquet npm
  @imgly/background-removal-node (hôte autorisé), exécuté par onnxruntime. Preuve le 19/10 sur
  image de référence démo (aucune donnée client) : détourage propre d'une monture, 3,8 s/image.
- **(c) Coût : 0 FCFA.** État à maintenir (compté) : `~/.venv-amk` (Pillow + rembg — c'est aussi
  le venv du build site, recréé) + modèle ~88 Mo hors dépôt (`~/.rembg/models/manual/`,
  `*.onnx` ignoré). Licences : rembg MIT, u2net Apache-2.0, paquet IMG.LY à licence propre →
  inférence locale interne seulement, jamais de redistribution des poids.
- **(d) Écartés :** IOPaint/lama-cleaner (dépôt archivé 13/08/2025, PyTorch, effacement d'objets
  = hors contrat « que du vrai ») ; Upscayl/Real-ESRGAN ncnn (GPU Vulkan absent de la sandbox ;
  option machine King seulement si photos trop petites).
- **(e) Verdict : INSTALLÉ + PROUVÉ sur démo ; production = règle 3.** Premier lot réel = test
  personnel de King (il valide chaque sortie avant build/déploiement). Conditions permanentes :
  aucune recoloration/redessin de monture, aucun fond « lieu » inventé, aucun patient
  identifiable sans accord écrit, contrôle visuel de 100 % des sorties. Triggers de re-review :
  premier lot client traité · halo/branche mangée constatés (→ autre modèle ou masque manuel) ·
  besoin d'upscale prouvé (→ test Upscayl sur machine King).

---

## 20/10 — taste-skill (design-taste-frontend) : installé et utilisé une première fois à la demande de King

> Demande King du 20/10 : « install and use this [github.com/Leonxlnx/taste-skill] » avant d'aller plus
> loin. Détail, état vérifié et premier usage : `tools/taste-skill/README.md`.

- **(a) Problème :** les pages générées retombent sur les défauts de catégorie (centré, kicker, cartes
  icônes, dégradés) — le risque « AI-made » que `AMK-DESIGN-SKILLS.md` combat déjà à la main, sans
  portique mesuré ni source de directions extérieure au modèle.
- **(b) Use case AMK nommé :** tout build/revue de page client (protocole d'unicité §2) : tirage de
  direction recherchée (`draw.mjs`), lint anti-slop, inspection navigateur réel et critique sur
  captures — en complément mesuré des lois maison, premier terrain : la revue DM Optique.
- **(c) Coût :** **0 FCFA** (MIT). État à maintenir (règle 5, compté) : clone épinglé `~/.taste-skill`
  (~43 Mo avec exemples) + 2 liens symboliques, **hors dépôt** ; ré-épinglage à chaque mise à jour
  dans `tools/taste-skill/install.sh` ; sorties `.taste-skill/` gitignorées.
- **(d) Effort + verdict :** **INSTALLÉ + premier usage fait, production sous conditions.** Le 20/10 :
  pin `63aba5f`, liens `~/.claude/skills` + `~/.agents/skills`, `draw.mjs` prouvé par appels réels ;
  `lint.mjs` sur l'accueil DM = **43 FAIL / 12 WARN**, quasi tous sur l'identité délibérée (mono,
  filets, 01–06) → le skill sert de défaut aux nouveaux builds, pas de bulldozer sur identité figée.
  `inspect.mjs` **non prouvé** ici (aucun Chrome dans la sandbox ; `CHROME_PATH` possible via la
  chaîne brag). Conditions : **règle 3** — King relit la première application complète avant usage
  production libre ; **règle 4** — requêtes `assets.mjs` génériques seulement, aucune donnée client ;
  conflits avec les verrous maison signalés, jamais tranchés en silence. Règle debout :
  `PRE-FLIGHT.md` §1f④. Triggers de re-review : inspecteur prouvé (Chrome) · première page livrée
  avec le run complet · conflit répété avec `AMK-DESIGN-SKILLS.md`.

---

## 20/10 — design-motion-principles (kylezantos) : installé et utilisé à la demande de King

> Demande King du 20/10 : « install and use [github.com/kylezantos/design-motion-principles] »,
> puis nouvel audit du site. Détail : `tools/design-motion-principles/README.md`.

- **(a) Problème :** nos pages ont du mouvement (révélations, lavis, dock, filtres) sans grille
  de lecture dédiée : durées et boucles décidées au cas par cas, aucun contrôle « ce geste mérite-t-il
  d'être animé, à quelle vitesse, pour quel public ».
- **(b) Use case AMK nommé :** tout audit ou ajout de motion sur page client (premier terrain :
  l'audit combiné DM v2 du 20/10) — pondération par contexte (santé = retenue), porte de
  fréquence, anti-checklist « AI-slop motion », accessibilité du mouvement.
- **(c) Coût :** **0 FCFA** (MIT). État à maintenir (règle 5, compté) : clone épinglé
  `~/.design-motion-principles` (~0,6 Mo, 100 % markdown) + 2 liens, **hors dépôt** ;
  ré-épinglage dans `tools/design-motion-principles/install.sh`.
- **(d) Effort + verdict :** **INSTALLÉ + premier usage fait, production sous conditions.**
  Pin `4a9ca87` ; audit DM : boucles d'ambiance infinies non pausables, révélation uniforme
  620 ms jusque sur le texte statique, skiplink animé en `top` — correctifs consignés, **non
  appliqués** (ce sont des changements de design). Conditions : **règle 3** — King relit ce premier
  audit avant tout correctif motion livré ; les lois maison et verrous client gagnent en cas de
  conflit ; pas de rapport HTML `motion-audits/` sans OK (§4b). Règle debout : `PRE-FLIGHT.md`
  §1f⑤. Triggers de re-review : premier lot motion livré · conflit répété avec taste-skill.

---

## 20/10 — ECC sélectif (affaan-m/ECC) : installé et utilisé à la demande de King

> Demande King du 20/10 : « install and use [github.com/affaan-m/ECC] », puis nouvel audit.
> Détail et périmètre exact : `tools/ecc/README.md`.

- **(a) Problème :** nos audits de livraison reposent sur les seuls portiques maison ; il manque
  une grille externe de readiness/sécurité/SEO/accessibilité et un format de verdict chiffré
  (score à plafonds, preuves nommées) opposable avant un lancement client.
- **(b) Use case AMK nommé :** audit de pré-livraison des sites clients (premier terrain :
  l'audit combiné DM v2 du 20/10) via six skills : `production-audit`, `verification-loop`,
  `security-review`, `accessibility`, `seo`, `click-path-audit`.
- **(c) Coût :** **0 FCFA** (MIT). État à maintenir (règle 5, compté — c'est le plus lourd de nos
  outils) : clone épinglé `~/.ecc` (~113 Mo) + 149 fichiers gérés dans `~/.claude/` (état
  `~/.claude/ecc/install-state.json`) + 6 liens `~/.agents/skills/`, **hors dépôt** ; le harnais
  complet (311 skills, hooks, mémoire, MCP) n'est **pas** installé.
- **(d) Effort + verdict :** **INSTALLÉ (sélectif) + premier usage fait, production sous
  conditions.** Pin `6f1881a` (2.2.3) ; plan `--dry-run` lu avant écriture (149 copies, aucun
  settings modifié, aucun hook enregistré) ; `ecc doctor` OK, `ecc status` healthy ; audit DM :
  **79/100, « launchable with caveats »**. Conditions : **règle 3** — King relit ce premier audit ;
  **règle 4** — aucun scanner externe, aucun envoi de code/données client, `ito`/mémoire/hooks/
  auto-update éteints ; ne jamais empiler le plugin complet sur cette installation sélective
  (avertissement de l'amont). Le harnais complet sur la machine de King = décision séparée,
  après son test personnel. Règle debout : `PRE-FLIGHT.md` §1f⑥. Triggers de re-review :
  premier lancement client audité avec la grille · demande d'un skill ECC hors sélection ·
  conflit avec un portique maison.

---

## 20/10 — UI/UX Pro Max (nextlevelbuilder) : installé et utilisé à la demande de King

> Demande King du 20/10 : « install and use [github.com/nextlevelbuilder/ui-ux-pro-max-skill] ».
> Détail : `tools/ui-ux-pro-max/README.md`.

- **(a) Problème :** nos relectures UX reposent sur nos checklists ; il manque une base
  consultable de règles UX/stiles/typo pour interroger un point précis (« fixed bottom bar »,
  « filter drawer ») avant de corriger.
- **(b) Use case AMK nommé :** audit et build de pages clients — recherche ciblée par domaine
  (`ux`, `typography`, `landing`…) et grille pré-livraison ; premier terrain : l'audit combiné
  DM v2 du 20/10.
- **(c) Coût :** **0 FCFA** (MIT). État à maintenir (règle 5, compté) : clone épinglé
  `~/.ui-ux-pro-max-skill` (~30 Mo) + 2 liens, **hors dépôt** ; recherche = Python stdlib local,
  aucun réseau, aucune donnée client dans les requêtes.
- **(d) Effort + verdict :** **INSTALLÉ + premier usage fait, production sous conditions.** Pin
  `56ea9cf` (2.15.0) ; appels réels (`--domain ux`, `--design-system`) ; sur DM, ses règles
  individuelles ont confirmé nos acquis (reduced-motion, focus, cibles, reflow de chips) et sa
  « design system » générée (Claymorphism/teal) a été **écartée** : nouvelle identité interdite
  par les verrous — l'outil sert de grille, jamais de direction. Conditions : **règle 3** (King
  relit la première application) ; aucune sortie d'outil ne remplace les lois maison.
  Règle debout : `PRE-FLIGHT.md` §1f⑦. Triggers de re-review : premier usage « design system »
  accepté par King sur un nouveau build · divergence répétée avec taste-skill.

---

## 20/10 — Impeccable (pbakaus) : installé et utilisé à la demande de King

> Demande King du 20/10 : « install and use [github.com/pbakaus/impeccable] ». Détail :
  `tools/impeccable/README.md`.

- **(a) Problème :** pas de détecteur déterministe d'anti-patterns UI (texte trop petit,
  padding écrasé, niveaux de titres sautés…) ; ces contrôles se font à l'œil ou en grep ad hoc.
- **(b) Use case AMK nommé :** `impeccable detect` en portique d'audit sur les pages clients ;
  commandes de polish (polish/harden/critique) documentées pour les lots de finition. Premier
  terrain : audit combiné DM v2 du 20/10 (32→31 findings, `skipped-heading` corrigé, le reste
  vérifié comme faux positifs ou identité).
- **(c) Coût :** **0 FCFA** (Apache-2.0). État à maintenir (règle 5, compté — le plus lourd avec
  ECC) : clone épinglé `~/.impeccable-src` (~107 Mo) + lien skill + **moteur binaire 0.1.16**
  (~21 Mo) dans `~/.impeccable/bin/` (obtenu du paquet npm officiel `@impeccable/cli-linux-x64`,
  egress releases GitHub bloqué ici ; l'installeur amont saura le télécharger tout seul sur la
  machine de King), **hors dépôt**.
- **(d) Effort + verdict :** **INSTALLÉ + premier usage fait, production sous conditions.** Pin
  `46b822f`, `engine-probe` OK, `detect --json` exécuté sur 4 pages réelles. Conditions :
  **règle 3** (King relit le premier rapport) ; **pas de hooks Impeccable** (ni `.claude/settings`
  ni hooks projet — activation séparée, décision de King) ; PRODUCT.md/DESIGN.md non créés dans
  le dépôt (§4b) ; chaque finding est **vérifié dans le code** avant correction (leçon du jour :
  28 « cramped-padding » étaient des faux positifs). Règle debout : `PRE-FLIGHT.md` §1f⑧.
  Triggers de re-review : premier lot de polish livré avec ses commandes · mise à jour du moteur ·
  divergence répétée avec les portiques maison.

## 20/10 — OpenSEO (every-app/open-seo) : installé (sélectif) et testé à la demande de King

> Demande King du 20/10 : « install https://github.com/every-app/open-seo.git then test/use on
> the DM optic website ». Détail : `tools/open-seo/README.md`.

- **(a) Problème :** pas d'outil SEO structuré côté agence — audits faits à la main
  (checklist SEO + greps) ; les suites du marché (Semrush/Ahrefs) sont hors budget cible.
- **(b) Use case AMK nommé :** les **12 skills méthodologie** du plugin officiel (`seo-audit`,
  `local-seo`, `keyword-research`, `ai-visibility-audit`…) comme grilles de travail des audits
  SEO/AEO clients, en complément des portiques maison. Premier terrain (20/10) : portion gratuite
  exécutée sur le site DM — verdict dans `clients/dm-optic/build-notes.md` (tout vert sauf
  `llms.txt` absent ; portion live bloquée sur la production F8).
- **(c) Coût :** **0 FCFA en l'état** (MIT ; skills markdown). L'**application** (TanStack +
  worker Cloudflare + **clé DataForSEO payante** par appel + self-host Docker/Cloudflare) n'est
  **pas installée** : trois décisions de King (coût récurrent, compte fournisseur au nom de qui
  l'ouvre, hébergement). État maintenu (règle 5) : le pin de l'installeur, rien d'autre.
- **(d) Effort + verdict :** **INSTALLÉ SÉLECTIF + premier usage fait.** Pin `8713d75`
  (`tools/open-seo/install.sh`, testé de bout en bout : 12/12 skills vers
  `~/.agents/skills/open-seo-skills/`). Conditions : aucune clé API dans le dépôt ; aucune donnée
  client vers DataForSEO sans accord explicite de King (règle 4) ; les portiques maison font foi.
  Re-review : quand King décide du compte DataForSEO/self-host, ou à la mise en production d'un
  site client (Search Console connectable).

## 20/10 — The Agency / agency-agents (msitarzewski) : installé et testé à la demande de King

> Demande King du 20/10 : « install test and use https://github.com/msitarzewski/agency-agents.git ».
> Détail : `tools/agency-agents/README.md`.

- **(a) Problème :** expertises ponctuelles (AEO, finish-gate UI, auditeur a11y, chef de staff…)
  re-dérivées à chaque tâche au lieu d'être des personas écrites, testées et réutilisables.
- **(b) Use case AMK nommé :** 298 personas markdown (19 divisions + strategy) chargées comme
  grilles d'expertise quand une tâche tombe dans leur domaine — en **renfort** de la pile existante
  (taste, DMP, ECC, UIUX, Impeccable), jamais en remplacement des portiques. Premier usage (20/10) :
  persona `marketing-aeo-foundations` + `marketing-seo-specialist` appliquées au site DM (verdict
  build-notes). Doublons assumés et nommés : `testing-accessibility-auditor` ≈ ECC accessibility,
  `design-ui-finish-gate-reviewer` ≈ taste (consultés en plus, décisions inchangées).
- **(c) Coût :** **0 FCFA** (MIT, markdown pur — aucun binaire, aucun runtime). État maintenu
  (règle 5, compté) : un pin + deux dossiers hors dépôt (`~/.agents/agency-agents`,
  fusion non destructive `~/.claude/agents`).
- **(d) Effort + verdict :** **INSTALLÉ + testé + premier usage fait.** Pin `4e3ac3c`
  (`tools/agency-agents/install.sh`, testé de bout en bout : 298/298 avec frontmatter). Conditions :
  un persona n'est pas loi maison — il ne restyle pas une identité figée, ne contourne pas §1b,
  ne décide pas un déploiement ; aucune donnée client dans un prompt de persona (règle 4) ;
  toute sortie client-facing passe la validation de King (règle 3). Re-review : à chaque nouveau
  lot de personas amont jugé utile (changement de pin daté, même procédure).

## 20/10 — OpenHiggsfield (wide-trace/open-higgsfield) : AUDITÉ, NON INSTALLÉ (ordre conditionnel de King : auditer d'abord, installer seulement si utile/vendable)

- **(a) Problème visé :** générer des visuels/vidéos IA (38 modèles : Seedance 2.5, Kling 3,
  Flux, Grok Imagine…) pour le marketing des clients.
- **(b) Ce que c'est réellement :** un studio Next.js 16 (1,6 Mo, pin de lecture `b16a0ef`) qui
  appelle l'API **payante** Higgsfield avec la clé du compte (`id:secret`) + un token **Vercel
  Blob** pour les uploads. L'interface est gratuite ; la génération est facturée à l'appel, chez
  un tiers, depuis un compte à ouvrir.
- **(c) Verdict flux de travail : NON aujourd'hui.** (1) Verrous AMK : « le site ne montre que du
  vrai » — aucun visuel IA sur les sites et supports clients ; visages IA déjà écartés ; le plan
  month-1 DM repose sur les vraies photos. (2) L'origine API est injoignable depuis le bac
  (egress). (3) pnpm + clé payante + Vercel Blob requis pour un test réel.
- **(d) Verdict vente : NON en l'état.** **Aucune LICENCE dans le dépôt** (vérifié sur tout
  l'arbre) : le « free & open-source » du README ne vaut rien juridiquement — all rights
  reserved, impossible de dériver ou de revendre légalement ; dépendance à une API payante au
  nom de qui l'ouvre ; toute utilisation client enverrait des données à un tiers sans accord
  explicite (règle 4) ; en tension avec le positionnement honnêteté de l'agence.
- **(e) Ce qui changerait le verdict :** l'amont ajoute une LICENCE · King ouvre un compte
  Higgsfield et le teste personnellement (règle 3) · un cas d'usage concret validé par lui
  (ex. b-roll abstrait pour pubs — jamais de faux visuels produits ou de faux cabinets).
  Alternative immédiate sans installation : la version hébergée openhiggsfield.ai avec la clé
  de King. Entrée tenue pour le registre (règle 5) — réévaluer si l'un des trois points bouge.

## 20/10 — Hyperframes (heygen-com/hyperframes) : auditée sur preuves — DÉJÀ INSTALLÉE et UTILISÉE en production

> Demande King du 20/10 : « audit and see if this helps in our workflow or if we can sell it as
> an additional service .. then install, test and use ». Détail : `tools/hyperframes/README.md`.

- **(a) Problème :** rendre des vidéos d'annonce depuis du HTML réel, en local, sans frais par
  rendu — c'était le chaînon manquant des livraisons avant le 19/10.
- **(b) Use case AMK nommé :** c'est **déjà le moteur de la chaîne brag (§1f②)**. Preuves :
  19/10 preuve de bout en bout ; **20/10 le brag DM Optique rendu avec** — `check` 0 erreur,
  contraste 10/10 WCAG AA, snapshots relus, `render --quality looks` 20 s en ~58 s, portique
  `audit_video_motion` OK après un blocage corrigé (outro figée).
- **(c) Coût :** **0 FCFA** — Apache-2.0 (vérifiée sur le paquet npm installé), rendu local,
  aucun frais par rendu (l'hébergé du même éditeur facture ~19 $/vidéo). État maintenu (règle 5) :
  installé par `tools/brag/install.sh` (runtime unique, CLI 0.8.177, wrapper Chrome) — **aucun
  second installeur** (leçon ECC).
- **(d) Effort + verdict :** **FLUX : OUI (déjà en production). VENTE : OUI** — l'offre « vidéo
  d'annonce de livraison » (captures réelles, identité client, musique générée/licenciée) est
  défendable ; **tarif = décision de King**. Conditions : que du vrai à l'écran ; piste
  ende.app toujours interdite ; rien d'envoyé sans validation de King. Ruling du même jour :
  le `brag.mp4` DM est **versionné dans le dépôt** sur ordre explicite (exception fichier par
  fichier à la règle « aucun mp4 versionné » ; le `.gitignore` global reste).

## 20/10 — anthropics/skills : AUDITÉ — les skills documentaires sont PROPRIÉTAIRES, non installés ; la capacité est construite en propre (`tools/docs/`)

> Demande King du 20/10 : « audit and see if this helps in our workflow or if we can sell it as
> an additional service .. then install, test and use ». Pin de lecture `dbd4588`.

- **(a) Ce que c'est :** le dépôt officiel des skills Anthropic — 19 skills dont les 4
  documentaires (`docx`, `pdf`, `pptx`, `xlsx`, ceux qui font les capacités « create files » de
  Claude) + des skills génériques (frontend-design, brand-guidelines, webapp-testing,
  skill-creator, mcp-builder…).
- **(b) Verdict licence — le point bloquant :** les 4 documentaires sont **« source-available,
  not open source »** (README §20) avec des restrictions écrites noires sur blanc
  (`skills/xlsx/LICENSE.txt`) : interdiction d'**extraire** les matériaux des Services, d'en
  garder des **copies hors des Services**, d'en faire des **works dérivés**, de les
  **redistribuer**. Notre pattern d'installation (clone + copie + pin hors services) = exactement
  ce qui est interdit. **Non installés — pas de contournement.**
- **(c) Verdict flux/vente sur les Apache-2.0 :** réels open source MAIS recouverts par notre
  pile (frontend-design/brand-guidelines ≈ taste + AMK-DESIGN-SKILLS ; webapp-testing ≈ portiques
  Node) ou hors métier (mcp-builder, claude-api). Non installés (règle 5 — pas d'état maintenu
  sans usage).
- **(d) Ce qui est retenu : LA MÉTHODE, réimplémentée en propre** — méthodologie xlsx
  professionnelle (fonte lisible, zéro erreur de formule, sources citées dans le fichier,
  recalc) appliquée avec `openpyxl` (MIT) dans **`tools/docs/xlsx_build.py`** (notre code, aucun
  matériau amont copié). **Test et usage réels le jour même :** inventaire des 40 montures DM
  Optique — `clients/dm-optic/launch/LISTE-40-MONTURES-2026-10.xlsx` (livrable de confirmation
  client) + version WhatsApp `LISTE-40-MONTURES-WHATSAPP.txt`.
- **(e) Vente : OUI, la capacité** — production documentaire (inventaires, proformas, rapports)
  en service additionnel ; ajouts prévus sur demande : docx (python-docx, MIT), pptx
  (python-pptx, MIT), pdf (reportlab — **vérifier les termes AGPL avant usage client**).
  Conditions : aucune donnée client hors machine (génération locale), sorties relues par King
  (règle 3). Re-review : si Anthropic relicencie les skills documentaires en open source.

## 20/10 — blader/humanizer : AUDITÉ puis INSTALLÉ (MIT ; second passe copywriting, loi maison d'abord)

> Ordre King du 20/10 (« install https://github.com/blader/humanizer ») — l'audit-before-install
> est passé AVANT l'installation (règle debout). Pin de lecture `8c307f3` (16/10/2026, v3.1.0).

- **(a) Ce que c'est :** un skill autonome = un `SKILL.md` de 32 Ko qui réécrit un texte « qui sonne
  IA » en gardant ce qu'il dit, d'après les 26 motifs de « Signs of AI writing » (Wikipédia).
  Zéro dépendance, zéro réseau, zéro hook ; `scripts/validate-package.py` = lint du propre
  packaging amont, stdlib.
- **(b) Licence : MIT** (© 2025 Siqi Chen), lue dans le clone épinglé — installable. Le contraste du
  jour : anthropics/skills doc-skills, propriétaires, NON installés (entrée ci-dessus).
- **(c) Flux : OUI — second passe copywriting** APRÈS la loi maison (§11b AMK-DESIGN-SKILLS,
  YouTube-Lessons [1]–[6], COPY CRAFT GATE, MESSAGES §1). Ne remplace aucune règle : les lois
  maison et la voix du client gagnent (règle 1). Premier usage réel le jour même : bande
  « Assurances » du site DM (texte écrit contre les 5 motifs les plus forts).
- **(d) Vente : indirecte** — outil de qualité interne qui améliore chaque texte vendu ; pas un
  livrable. Ne fait pas passer les détecteurs IA (ni visé, ni promis par l'amont).
- **(e) Installation :** `tools/humanizer/install.sh` — clone épinglé `~/.humanizer`, copie du
  `SKILL.md` (voie documentée par l'amont pour les agents sans Skills CLI) vers
  `~/.agents/skills/humanizer/` + miroir `~/.claude/skills/`. NI `/plugin marketplace`, NI
  `npx skills add` (pas de runtime CLI supplémentaire, règle 5). Preuve par grep du front-matter.

## 20/10 — D4Vinci/Scrapling : AUDITÉ puis INSTALLÉ (BSD-3 ; veille/monitoring, cibles validées une par une)

> Ordre King du 20/10 (« audit then install … if it meets the criteria »). Pin de lecture
> `fd53131` (18/10/2026, v0.5). Détail complet : `tools/scrapling/README.md`.

- **(a) Quoi :** framework Python de scraping adaptatif (parser qui retrouve ses éléments après
  changement du DOM, fetchers statique/navigateur, spiders, robots.txt obey intégré, skill agent
  officiel avec garde anti-injection `--ai-targeted`).
- **(b) Licence : BSD-3-Clause** (© Karim Shoair) — bibliothèque et skill ; `AI_POLICY.md` amont =
  règle de contribution, pas de restriction d'usage.
- **(c) Flux : OUI** — contrôles approfondis §1c sur pages publiques ; **veille concurrentielle
  mensuelle** (nouveau service défendable, tarif = décision King) ; vérifications NAP/annuaires.
- **(d) Règles d'usage :** pages publiques ; **jamais Google/Facebook** (ToS) ; robots.txt + débit
  limité ; aucune donnée client sortante ; **chaque cible = décision nommée**.
- **(e) Installation :** `tools/scrapling/install.sh` — pip `--user` + skill officiel copié vers
  `~/.agents/skills/scrapling/` + miroir. **Preuve par appel réel** : GET github.com → 200, title
  extrait (API v0.5 = `.css('sel::text').get()`). **Limite testée :** fetchers navigateur bloqués
  en sandbox (CDN) → `scrapling install` sur la machine de King pour le plein potentiel.

## 21/10 — firecrawl/firecrawl : AUDITÉ — NON INSTALLÉ (AGPL-3.0 mais pile lourde, besoin déjà couvert)

> Ordre King (« audit and install »). Clone de lecture `12c69db` (20/10/2026, 58 Mo).

- **(a) Quoi :** scraping → markdown « LLM-ready », /extract ; API cloud payante (crédits) OU
  self-host Docker Compose (API + workers + Playwright + **Redis + RabbitMQ + PostgreSQL NuQ +
  FoundationDB**). Licence **AGPL-3.0** (usage interne OK ; copyleft si diffusion en réseau).
- **(b) Verdict flux NON pour nous aujourd'hui :** cloud = compte + clé payants, injoignables du
  bac ; self-host = 5 services + Docker — **Docker ABSENT du bac** (vérifié 21/10) et un état
  maintenu de cette taille pour un besoin couvert par Scrapling (installé 20/10, BSD-3, zéro
  infra, testé) contredit la règle 5. Vente : rien que la veille Scrapling ne fasse déjà.
- **(c) Conditions de réévaluation (les deux à la fois) :** King ouvre un compte cloud testé chez
  lui ET un besoin précis non couvert par Scrapling (ex. extraction LLM de centaines de pages à
  la demande). Sinon on ne revient pas dessus.

## 21/10 — hypit-ai/hypit : AUDITÉ puis INSTALLÉ (Apache-2.0 modifiée — clauses lues ; CLI testé)

> Ordre King (« audit and install »). Clone de lecture `0d36de9` (18/10/2026) ; exécutable npm
> `@hypit/hypit@0.3.1` installé `~/.npm-global` (installeur `tools/hypit/install.sh`).

- **(a) Quoi :** moteur vidéo SVML pour agents (check/plan/pricing/build), rendu Chromium,
  modèles génératifs optionnels payants — captions/motion/visuels code-rendus se compilent sans
  modèle (donc sans coût de service).
- **(b) Licence : Apache-2.0 MODIFIÉE, lue en entier** — **travail pour clients PERMIS** sans
  licence commerciale ; interdits : multi-tenant (2ᵉ workspace hors organisation), revente de
  l'outil, retrait du logo/copyright des rapports ; outputs à nous.
- **(c) Flux : OUI-potentiel — testé :** `hypit --version` → 0.3.1, `--help` → CLI complet.
  **Rendu complet NON testé au bac** (Chromium + charge au build) → premier usage réel = décision
  King (candidat : formats captions/motion, ex. UGC W1) ; Hyperframes reste le moteur brag.
- **(d) Règles debout :** jamais cloner la vidéo réelle d'un créateur pour un client (structure
  inspirée, contenu à nous ; verrous « que du vrai », R2 pas de visages IA, musique générée ou
  licenciée) ; `hypit check` + `hypit pricing` AVANT tout build ; logo amont des rapports
  conservé ; pas de multi-tenant ; portiques vidéo habitude avant envoi client.
- **(e) Détail :** `tools/hypit/README.md`.

---

## 23/10 — quatre outils installés **sur demande de King** (hors scan hebdomadaire)

> Ce n'est pas le scan du dimanche (qui plafonne à 3 outils et part d'un problème nommé) : c'est une
> demande explicite — « audit then install/setup » quatre dépôts. Les quatre sont installés
> **épinglés** dans `tools/<nom>/install.sh`, hors dépôt pour les fichiers, avec README et preuve par
> appel réel. Règles 3 et 5 tenues : rien ne tourne en production sans que King l'ait utilisé, et
> chaque outil remplace du travail (audit, mise en page, second avis) au lieu d'ajouter de l'état.

| Outil | Licence | Installé dans | Verdict | Ce qu'il remplace |
|---|---|---|---|---|
| `AgriciDaniel/claude-seo` v2.5.0 (19 729 ★) | MIT | `~/.claude/skills/seo` + 19 agents, miroir `~/.agents/skills` | **pursue** | la partie « audit SEO large » qu'aucun de nos six scripts ne couvre (E-E-A-T, hreflang, backlinks, rapports) |
| `zubair-trabzada/geo-seo-claude` (11 186 ★) | MIT | `~/.claude/skills/geo` + venv isolé | **pursue** | la lecture « crawlers IA / citabilité / llms.txt » — le trou relevé ce matin sur le site AMK |
| `nateherkai/roast-room` (1 004 ★) | **NOASSERTION** | `~/.claude/skills/roast-room` + agents | **hold** | un second avis structuré sur les décisions chères ; **licence à lire avant tout usage hors maison** → usage interne seulement |
| `mysticaltech/marketingskills` (362 ★) → **remplacé** | MIT | — | **abandonné le 23/10** | fork figé au 10/02/2026, 25 skills. Ruling King du 23/10 : basculer sur l'amont |
| `coreyhaines31/marketingskills` (56 063 ★) | MIT | 52 skills dans `~/.claude/skills`, miroir vérifié 52/52 | **pursue** | procédures (copy, pricing, launch, analytics, `ai-seo`, `schema`, `seo-audit`, `cold-email`) là où nous improvisions. Épinglé `e85f3cb` (22/10/2026) |

**Coût total** : 0 FCFA ; ~1 Go de disque **hors dépôt**, dont deux venvs Python (exclus des
sauvegardes). Aucun service, aucune clé, aucun compte. Chromium n'est installé nulle part (impossible
ici) : les fonctions « page rendue » resteront indisponibles et c'est écrit dans les README.

**Décision prise (King, 23/10/2026)** : `marketingskills` est passé sur l'amont `coreyhaines31`
— **52 skills** au lieu de 25, épinglé `e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b`. Le fork
`mysticaltech` est abandonné. **Piège rencontré** : le clone existant venait du fork ; `git fetch`
ramenait l'ancien historique (`not our ref` sur le pin de l'amont) et la bascule échouait en laissant
les 25 anciens skills. `install.sh` réécrit maintenant l'origine avant de chercher le pin, et vérifie
52 skills au lieu de 25.

## 23/10 — recherche « support de présentation » (montures DM) : `rembg` audité, **non retenu**

> Demande King : « research on github tools that can help you do it then install them » — la recherche
> est *exigée* avant toute installation. Elle a été faite sur l'API GitHub (recherche par étoiles), puis
> l'outil a été **installé pour l'essayer** avant d'être jugé. Le verdict est tombé sur l'essai, pas sur
> la popularité.

| Candidat | Licence | État | Verdict | Pourquoi |
|---|---|---|---|---|
| `danielgatis/rembg` (25 162 ★) | MIT | poussé le 21/10/2026, non archivé | **essayé, non retenu** | le détourage de montures n'est pas son cas |
| `noisyshade/PhotoRoom-Desktop` (8 ★) | MIT | appli de bureau | **écarté d'entrée** | application Electron, pas une bibliothèque : rien à piloter |
| `shubham8kale/Product-photography-AI` (5 ★) | — | Stable Diffusion + rembg | **écarté** | génère un *produit* : on n'invente pas une monture |

**Essai réel de `rembg` 2.0.86** (venv `/tmp/toolenv`, CPU) :

1. `pip install "rembg[cpu]"` passe ; mais les poids `u2net.onnx` se téléchargent depuis
   `release-assets.githubusercontent.com`, **bloqué ici** (TLS, comme la vidéo YouTube — voir les
   culs-de-sac du tour 67). L'outil est donc inutilisable dans cet environnement, même installé.
2. Même si les poids passaient, le modèle est entraîné pour des **sujets opaques sur fond chargé**.
   Les montures DM sont l'inverse : verres transparents, acétate translucide, charnières ressort de la
   couleur du fond. C'est précisément ce qui a déjà fait échouer le détourage maison au tour 66
   (14 fichiers sur 65 amputés).

**Décision** : pas de dépendance ajoutée, pas de modèle à télécharger, **0 FCFA**, et le support est
dessiné par **`tools/site/frame_bench.py`** — déterministe, relisible, réversible, sans réseau. Le
script porte ses propres garde-fous (détourage + contrôle de pièces + repli « planche »), ce qu'un
modèle opaque ne peut pas offrir sur ces photos.

---

## 23/10 — **pro-design** (donné par King, installé) — verdict : **pursue**

- **(a) Problème :** une page construite sans méthode sort « générique » et la revue n'en finit pas.
- **(b) Use case AMK nommé :** toute page neuve ou redesign (site client, landing, page de vente) —
  il impose une raison par section, **un** moment de mouvement, et **deux tours de vérification maximum**.
- **(c) Coût :** nul. Markdown pur, source dans le dépôt (`tools/pro-design/SKILL.md`), install
  `bash tools/pro-design/install.sh`, aucun réseau, aucun abonnement.
- **(d) Effort + verdict :** 0 (déjà lu et installé le 23/10) → **pursue**. Le seul apport qu'aucun autre
  skill ne donne : **la limite explicite de la boucle de polissage.** Borné à ce que les portiques maison
  ne couvrent pas : les portiques §1b restent seuls juges.

---

## 23/10 — **MoneyPrinterTurbo** (`harry0703`, MIT) — verdict : **pursue, borné à l'assemblage**

- **(a) Problème :** nos vidéos se montent à la main (`tools/video/compose.py` fait des cartes et du
  mouvement de capture ; il ne coupe pas des rushes à la durée d'une voix, et il ne rend pas deux
  formats d'un seul coup). Chaque tournage réel demandait un montage manuel.
- **(b) Use case AMK nommé :** « un tournage, deux montages » (§5 quater) — quatre plans tournés au
  téléphone, une voix enregistrée, et deux fichiers 9:16 / 16:9 coupés à la seconde.
- **(c) Coût :** **0 FCFA**, aucun compte, aucune clé. 733 Mo de source + 1,2 Go de venv, **hors du
  dépôt** (`/tmp/amk-moneyprinter`). ffmpeg embarqué, pas de paquet système, pas de sudo.
- **(d) Effort + verdict :** installé, **2 341 tests amont passés / 0 échec**, et un assemblage réel
  produit ici (20,0 s, 1080×1920, 30 i/s) → **pursue**. Borné : `--video-source local` est forcé par
  notre enveloppe ; banque d'images, voix de synthèse et script par modèle sont **refusés** (le décor
  doit exister, le script est le nôtre). Sous-titres : Whisper, modèle téléchargé au premier usage —
  donc pas testé dans la sandbox, et jamais présenté comme testé.
- **Ce que l'outil ne fait pas et qu'on ne lui demande pas :** générer des plans. Un plan inventé ne
  remplace pas un plan tourné.
