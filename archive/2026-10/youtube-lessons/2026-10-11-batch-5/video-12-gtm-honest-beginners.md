# Vidéo 12 — « What is GTM Engineering? (The Honest Beginner's Guide) » · GTM With Deepika

## 1 · SOURCE CAPTURE
- **Transcript :** voie §0 (`youtubetotranscript.com/transcript?v=e_f06ZTb4oA`), 3 chunks, complet.
  Audio **hindi/hinglish**, transcript en devanagari ; métadonnées en anglais.
- **Producteur :** « GTM With Deepika », 324 abonnés, créatrice Inde. Vend : entrée de carrière en
  GTM engineering (audience, commentaires, abonnés ; pas de produit propre annoncé).
- **Longueur / date / vues :** 26 min · 19/06/2026 · 2 100 vues (page YouTube).
- **Re-dated evergreen check :** aucun millésime au titre ; le contenu (« l'IA a tout changé ») est
  cohérent avec 2026 ; **pas de mismatch**. Seule particularité : langue audio ≠ langue des métadonnées.

## 2 · CLAIM AUDIT (seules les claims qui changeraient une décision)
1. « Les reply rates du cold email sont sous 1 % dans la plupart des industries » — **UNVERIFIED**
   (aucune source ; les benchmarks publics varient ~1–10 %). Sert le pitch « l'ancien monde est mort ».
2. « Un SDR coûte 30–80 k$/an ; 5 SDR = 300 k$/an » — **UNVERIFIED** (plausible US junior, non sourcé).
3. « Un GTM engineer fait le travail de 5 SDR » — **UNVERIFIED** (cœur du pitch, jamais mesuré).
4. « 30 % d'une liste de contacts de 6 mois a changé d'entreprise » — **UNVERIFIED** (chiffre vendor-type).
5. « Clay se connecte à des centaines de sources de données » — **VENDOR SELF-REPORT** (marketing Clay).
6. Grilles salaires Inde/US ($6L–$35L INR ; 55–200 k$ US) — **UNVERIFIED** (estimations annoncées telles quelles).

## 3 · TOOL AUDIT
| Outil | Coût | Alternatives gratuites / moins chères | Orchestrator-first ? |
|---|---|---|---|
| Clay | free tier ; payant jusqu'à ~800 $/mois (cité lot task) | **buildingopen/opengtm** (open source) | OUI : find+enrich = sweeps ONOC/avis/fetch_page |
| Apollo | 49–119 $/user/mois ; free 900 crédits/an | free tier ; sinon annuaires locaux (ONOC) | OUI pour la vérif ; Apollo sans donnée opticiens CM |
| Instantly / Smartly | payant (envoi email) | n8n CE self-host + envoi manuel King (WhatsApp d'abord) | OUI : l'envoi reste manuel et personnel (règle maison) |
| Zapier / Make | freemium | **n8n Community Edition** (self-host, gratuit, illimité) | OUI : crm.py + generators = notre connecteur |
- **Premier contrôle :** l'orchestrateur fait déjà find → enrich → write(first line) → route (crm.py).
  Le « GTM engineer » de la vidéo ≈ l'orchestrateur + King. **Rien à acheter.**

## 4 · GAP-FILLING
- Absent : WhatsApp, marchés non-LinkedIn, Afrique ; tout suppose email B2B + données LinkedIn/US.
- Contre-preuve : les reply rates « <1 % » servent à vendre l'automation de volume ; notre règle maison
  (première ligne sur LUI, jamais template) dit l'inverse et c'est elle qui a produit les réponses.
- **Question critique :** pour une agence 1 personne / 4 clients/an au Cameroun, **la MÉTHODE transfère
  (signaux, enrichissement, système, boucle de données), le STACK et l'ÉCONOMIE (remplacer des SDR) non** :
  il n'y a pas d'équipe SDR à remplacer.

## 5 · INTEGRATION RECOMMENDATION
- **Adopté :** (a) le ciblage par **signaux/trigger** (levée de fonds, recrutement, changement de
  direction, switch concurrent) → traduit Cameroun : nouvel avis Google, activité FB/IG, travaux de
  boutique → destination `sales/RESEARCH-STANDARD.md` ; (b) « builder, pas codeur » + projet portfolio
  documenté → idée de post build-in-public TikTok → `AMK-TIKTOK-ESTABLISHMENT-2026-10-12.md`.
- **Rejeté :** stack payant Clay/Instantly/Apollo à l'échelle actuelle (biais gratuit/open-source ;
  aucun profit ne le justifie) ; l'économie « 1 = 5 SDR » comme chiffre de planification.
- **Wave / outreach / CRM :** pas de changement de template ce soir ; le trigger devient la 7ᵉ
  recherche du standard (voir consolidation Lot [40]).

## 6 · SUMMARY BLOCK
- **Core idea (2 phrases) :** le GTM engineer transforme la stratégie commerciale en système automatisé
  (trouver → enrichir → écrire personnel → envoyer → mesurer) ; l'IA a rendu la personnalisation à
  l'échelle possible sans équipe. C'est un rôle de builder, pas de codeur.
- **KEPT :** ciblage par signaux/trigger → `sales/RESEARCH-STANDARD.md` ; « montrer le système » en
  build-in-public → brief TikTok.
- **REJECTED :** stack payant (biais gratuit), économie SDR-remplacement (non applicable, non vérifiée).
- **OPEN QUESTIONS :** le trigger « avis Google » est déjà dans DETECTION-FUITES — le formaliser comme
  « signal » change-t-il quelque chose au scoring, ou seulement au vocabulaire ?
