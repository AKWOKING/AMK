# Vidéo 13 — « Ultimate Guide to GTM Engineering for 2026 » · Salesforge (sponsorisé)

## 1 · SOURCE CAPTURE
- **Transcript :** voie §0, 2 chunks utiles (le corps finit dans le chunk 1 ; chunk 2 = boilerplate).
- **Producteur :** **Salesforge** (4,17 K abonnés) — **VIDÉO SPONSORISÉE PAR LE VENDOR** dont elle vante
  le stack. Vend : Salesforge + LeadsForge + MailForge/Infraforge + PrimeForge.
- **Longueur / date / vues :** ~20 min · 17/04/2026 · 3 400 vues.
- **Re-dated evergreen check :** « for 2026 » au titre = année d'upload ; cohérent ; **pas de mismatch**.

## 2 · CLAIM AUDIT
1. « Un GTM engineer égale la production d'une équipe SDR entière » — **VENDOR SELF-REPORT**.
2. « 5–6 reps sur ce système = pipeline d'une équipe de 50 » — **VENDOR SELF-REPORT**, zéro preuve.
3. « Clay = 150 sources » (vidéo 12 disait « des centaines ») — **VENDOR-RELAYÉ**, incohérence mineure.
4. « Salesforge : 500+ meetings/mois » via **comptes LinkedIn de toute l'équipe** (support, growth,
   sales) — **VENDOR SELF-REPORT** + tactique à risque ToS LinkedIn (automation multi-comptes personnels).
5. « 50+ signaux par prospect » pour l'IA d'outbound — **VENDOR**.
6. « L'outbound devient fiable et scalable » — opinion vendor, **UNVERIFIED**.

## 3 · TOOL AUDIT
| Outil | Coût | Alternative | Verdict |
|---|---|---|---|
| Salesforge (+Leads/Mail/Infra/Prime-Forge) | payant (free trial mis en avant) | n/a — modèle volume email+LinkedIn | **REJETÉ** : vendor, volume, spam-adjacent |
| Clay | voir vidéo 12 | opengtm (open source) | rejeté à l'échelle AMK |
| n8n / Make | n8n CE **gratuit** self-host | — | **gardé en réserve** (couche connecteur future) |
- **Orchestrator-first :** le « système » décrit (liste → enrich → séquence → inbox unifiée) existe déjà
  en version maison : LISTE vérifiée ONOC → crm.py → envoi manuel King → Activity-Log. **Rien à acheter.**

## 4 · GAP-FILLING
- Absent : WhatsApp, Cameroon, opticiens ; le « personalization » vendor = email généré IA à partir de
  LinkedIn — l'opposé de notre première-ligne-écrite-à-la-main qui a produit des réponses.
- Contre-preuve : l'automation multi-comptes LinkedIn viole les politiques LinkedIn (bans documentés) ;
  le vendor la présente comme un avantage (« unlimited LinkedIn senders »).
- **Question critique :** idem vidéo 12 — la discipline transfère, le stack non. Ici le stack est en plus
  **contraire à nos règles** (confiance d'abord, jamais de volume impersonnel).

## 5 · INTEGRATION RECOMMENDATION
- **Adopté :** le découpage **3 couches d'outbound** comme vocabulaire de revue : (1) IA/volume →
  rejeté ; (2) **intent-based** = nos signaux/trigger (vidéo 12) ; (3) **inbound-led outbound** = nos
  relances chaudes et prospects ayant vu notre contenu (règle 02/10 OraCare : vérifier qu'il a VU).
  → noté dans la consolidation Lot [40], pas de fichier neuf.
- **Rejeté :** tout le stack Salesforge ; le scaling horizontal LinkedIn ; « unlimited mailboxes ».
- **Wave / outreach / CRM :** inchangés ; la couche « inbound-led » confirme la règle existante
  (prospect ayant vu la vidéo = attribution vérifiée, jamais déduite).

## 6 · SUMMARY BLOCK
- **Core idea (2 phrases) :** le GTM engineer 2026 traite tout le TAM avec des systèmes (données Clay,
  3 couches d'outbound, triggers live) plutôt que des SDR. La vidéo est un tunnel de vente Salesforge
  déguisé en guide.
- **KEPT :** vocabulaire 3 couches (intent / inbound-led) pour nos revues ; n8n CE en réserve gratuite.
- **REJECTED :** stack Salesforge, scaling multi-comptes LinkedIn, metrics vendor (500 meetings, 1=équipe).
- **OPEN QUESTIONS :** aucune bloquante — le vendor-conflict suffit à classer les chiffres.
