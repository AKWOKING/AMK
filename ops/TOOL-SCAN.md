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

## 05/10 — entrée template : Mira (github.com/miracodeai/mira, ruling King : skip)

- **(a) Problème :** relecture automatique de PR code, self-hosted, BYO LLM key.
- **(b) Use case AMK :** second lecteur automatique sur les PR arena→main.
- **(c) Coût :** hosting permanent (webhooks) + tokens LLM par PR ; AMK n'a ni serveur persistant ni
   volume de PR — le sandbox reset à chaque tour.
- **(d) Effort + verdict :** GitHub App + deploy Docker + clé OpenRouter pour un workflow à un humain
   + un agent déjà couvert par le protocole de vérification → **skip**. Triggers de re-review : 2e dev
   humain · repo code client · PR volume. La ruling Mira = template de la scan.
