# Vidéo 15 — « How to Be a 1000x GTM Engineer - Only 1 Trick Needed » · Jordan Crawford (Blueprint)

## 1 · SOURCE CAPTURE
- **Transcript :** voie §0, 3 chunks, complet.
- **Producteur :** Jordan Crawford (Blueprint), 4,37 K abonnés — **consultant GTM engineering** ;
  vend des services (« guide pour mes clients actuels »), pas de SaaS propre. Biais : vendre du
  conseil « recherche d'abord », anti-leadgen-agencies.
- **Longueur / date / vues :** ~15–20 min · 24/07/2025 · 8 860 vues.
- **Re-dated evergreen check :** pas de millésime au titre ; contenu « agentic AI » cohérent avec
  2025 ; **pas de mismatch**.

## 2 · CLAIM AUDIT
1. « J'ai construit des centaines de systèmes GTM agentiques » — **VENDOR SELF-REPORT**.
2. « Les plays inventés hors conditions réelles d'achat échouent ; les leadgen agencies churnent » —
   argument/opinion **plausible**, non mesuré ; c'est la thèse du vidéo.
3. Démo : ChatGPT trouve des signaux d'achat publics nichés (dossiers de tribunaux/PACER, newsletters
   de barreaux, snapshots Indeed, avis Google, breadcrumbs tech-stack) — **PARTIELLEMENT DÉMONTRÉ** :
   les sorties de recherche sont réelles, mais le transcript de départ est **fictif** (généré pour la
   démo) → la démo prouve la recherche, pas la chaîne complète.
4. « Invert, always invert » (Munger, via Charlie Munger tribute) — citation, pas une claim factuelle.

## 3 · TOOL AUDIT
| Outil | Coût | Alternative | Verdict |
|---|---|---|---|
| ChatGPT / Gemini (recherche + transcription) | free tiers | **l'orchestrateur** = cet agent de recherche | **ADOPTÉ en équivalent maison** |
| Clay (agent tool) | payant | opengtm | rejeté à l'échelle AMK |
| n8n | CE gratuit | — | réserve future |
- **Orchestrator-first :** le « trick » (interroger les deals gagnés, croiser transcript + signaux
  publics, puis systématiser) est **exactement** un protocole de recherche — le cœur de notre métier
  actuel. **Rien à acheter.**

## 4 · GAP-FILLING
- Absent : comment démarrer **sans** base de clients (nous : 1–2 clients) ; la vidéo suppose 10–30
  deals gagnés à disséquer.
- Contre-preuve : aucune ; c'est la seule vidéo du lot qui **contredit** le « personalization at
  scale » des videos 12–14 (« le job N'EST PAS de personnaliser des emails »).
- **Question critique :** transférable **même à 1 personne / 4 clients/an** : chaque deal gagné (et
  chaque refus documenté) devient la source des signaux. DM Optique = notre premier « closed deal »
  à rétro-ingénierer (qu'est-ce qui a fait dire oui ? la page WhatsApp-ready ? l'approche vérifiée
  ONOC ? le prix founding ?).

## 5 · INTEGRATION RECOMMENDATION
- **Adopté :** **protocole de rétro-ingénierie des deals gagnés** : avant d'inventer un play,
  (1) interviewer King sur chaque deal gagné/perdu (verbatim), (2) croiser avec les données publiques
  observables à l'époque (avis, activité sociale, annuaire), (3) n'automatiser que ce qui est confirmé
  par ≥1 transaction réelle. → destination `sales/RESEARCH-STANDARD.md` (§ nouveau, fichier existant).
- **Adopté :** « ne pas acheter de signaux sur étagère » → cohérent avec notre biais gratuit ; consigné
  dans `ops/TOOL-SCAN.md`.
- **Rejeté :** rien du cœur ; seulement le passage « générer un transcript fictif pour tester » —
  dangereux pour nous (règle : jamais d'affirmation non vérifiée ; un transcript fictif ne doit
  jamais entrer au CRM ni dans un message).
- **Wave / outreach / CRM :** le protocole s'applique **avant** la prochaine vague (après acompte),
  pas à la vague du 12/10 (vérifiée, figée).

## 6 · SUMMARY BLOCK
- **Core idea (2 phrases) :** le vrai job du GTM engineer n'est pas d'inventer des plays mais de
  forcer l'entreprise à regarder ses deals gagnés, d'extraire pourquoi ils ont gagné, puis de
  systématiser cette recherche. Bottom-up (« invert »), jamais top-down.
- **KEPT :** protocole rétro-ingénierie → `sales/RESEARCH-STANDARD.md` ; « pas de signaux sur
  étagère » → `ops/TOOL-SCAN.md`.
- **REJECTED :** transcripts fictifs dans le pipeline ; Clay payant.
- **OPEN QUESTIONS :** qui interviewe-t-on pour les deals **perdus** (COMOBIL, etc.) sans rouvrir le
  fil ? → proposer un format « autopsie interne » non client-facing.
