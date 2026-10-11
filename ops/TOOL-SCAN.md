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
  reviendra. Triggers de re-review : un client demande un site auto-géré · un volume de sites que la
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
