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
  `cavisa` · `amk-cm.vercel.app` + ses pages · relecture en ligne de `dmoptic-2.vercel.app` après le
  redéploiement du 09/10.
- **Ajout 08/10 (revue Search Console) :** export Search Console d'`amk-cm` chaque dimanche 20h00 sous
  `research/gsc/AAAA-MM-JJ/` + une ligne ici (clics · impressions · position · requêtes). Repère du
  08/10 : 1 clic · 1 impression · position 3,0 sur 7 jours. Liste d'attente : rapatrier les pages
  live-only d'`amk-cm` (polyclinic, maternity) avant tout redéploiement.
