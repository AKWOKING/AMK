# AFRIQUE LABO — build notes

**Date:** 17 Sep 2026 · **Concept:** `demos/concept-afriquelabo-v1.html` · **Builder:** `demos/build_afriquelabo.py` · **Status:** named gift, unlisted, noindex — for the owner's eyes only.

## 1 · Verified intel (source-tagged)

| Fact | Source | Confidence |
|---|---|---|
| Nom : **Afrique Labo SARL** — laboratoire multidisciplinaire d'analyses de biologie médicale | leur poster WhatsApp | ✅ |
| Adresse : **Feu rouge Bessengue, Immeuble Nkake, au-dessus de Wafacash** (face Total Bessengue) | poster + ancien site indexé + dossier | ✅ |
| Téléphone : **+237 690 54 70 93** | leur profil WhatsApp Business + poster | ✅ |
| WhatsApp Business : compte pro « Afrique labo sarl », **catalogue en usage** (poster, grille tarifaire, photo devanture), statut **« Open 24 hours »**, catégories Medical & health / Education / Beauty | captures King (17/09) | ✅ |
| E-mail publié : **Afrique.labo@gmail.com** | poster | ✅ |
| Ancien e-mail **info@afriqlabo.com** | index Google de l'ancien site | ⚠ mort avec le domaine → à remplacer |
| Tagline : **« Votre santé, notre priorité »** ; valeurs **QUALITÉ · FIABILITÉ · RAPIDITÉ · SANTÉ HOLISTIQUE** | poster + ancien site indexé | ✅ |
| Photo/équipe : **Dr Takala** en blouse (**biologiste médicale**), devanture « A.F.L AFRIQUE LABO » bleu/rouge, paiement **MoneyGram / Orange Money** au seuil | poster + photo devanture (dossier) | ✅ (titre exact à confirmer) |
| Domaines **afriqlabo.com / .net : NXDOMAIN** (16/09, King au téléphone) ; l'index Google montre encore l'ancien site (placeholder **« Your logo »**) | dossier §6 + vérif. 17/09 (fetch échoue) | ✅ — à re-tester par King avant l'envoi |
| Grille tarifaire : ~150 lignes (biochimie, hématologie, sérologie, hormonologie, bactériologie, NFS…) avec codes machine | captures King (17/09) | ✅ (extraits only — cf. §5) |
| Facebook ≈ **5 500+ abonnés**, Google **4,5/5 (2 avis)** | dossier | ✅ |

## 2 · Pain analysis (what the website must kill)
1. **Le domaine est un cimetière.** Un patient qui tape « Afrique Labo Douala » tombe sur une page d'erreur — ou sur un annuaire qui propose un concurrent.
2. **L'ancien site disait « Your logo ».** Même quand il vivait, il ne reflétait pas l'activité réelle (template générique).
3. **Les prix sont invisibles.** Toute la grille vit dans une image WhatsApp et dans un panneau imprimé : impossible de comparer ou de se préparer, donc appels répétés pour un renseignement.
4. **Aucun parcours de prélèvement.** On ne sait pas s'il faut être à jeun, quoi apporter, quand venir pour les hormones, ni comment récupérer les résultats.
5. **Leur catalogue WhatsApp est un actif** — il faut s'appuyer dessus, pas le remplacer.
6. **La preuve locale manque** (24h/24, biologiste, devanture) : rien n'est visible hors Facebook.

## 3 · The solution the concept implements
- **Hero** : promesse concrète + photo réelle du travail + WhatsApp. Prix annoncé comme principe (« tarifs affichés »).
- **Rail 3 étapes** : Ordonnance → Prélèvement → Résultats (le patient sait où il va).
- **Console catalogue** : ~35 tests **extraits de leur propre grille**, recherche live + filtres par famille, prix FCFA, et **un bouton WhatsApp par test** qui ouvre un message pré-rempli (test + prix) — c'est leur catalogue, rendu utilisable.
- **Préparation** : à jeun (8–12 h, eau permise), quoi apporter, hormones = consigne au rendez-vous.
- **Résultats** : retrait sur place / envoi sur demande (WhatsApp e-mail) — **à confirmer avec eux**.
- **Services** : le trio de leur propre poster (analyses médicales · consultation médicale · coaching santé, bien-être & beauté).
- **Preuve** : Dr Takala (biologiste), 24h/24, 5 500+ Facebook, 4,5/5 Google, devanture et accès (repères locaux).
- **FAQ** : 5 questions guichet (à jeun, délais, quoi apporter, mutuelles, comment réserver).
- **FR/EN** complet (toggle mémorisé), mobile-first, WhatsApp-first, une seule page autonome.

## 4 · Three directions explored (§19.3) — and why the winner won
1. **« SAINE VITALITÉ »** (teal/white, soft rounded cards, illustrations) → *rejected*: c'est le look wellness générique des templates, il efface la précision du métier et ressemble aux sites concurrents.
2. **« CHAÎNE DE LABO »** (dark navy, photos plein cadre, chiffres corporate) → *rejected*: trop institutionnel/B2B, mauvais pour un patient au téléphone, et coûteux en données mobiles.
3. **« FEUILLE DE RÉSULTAT »** (retenu) → cyan signal + navy structure, micro-labels monospace, sections numérotées, **le catalogue comme pièce maîtresse**. Distinct de tous nos concepts, adapté au vrai problème (opacité), et il donne de la valeur *immédiatement* même sans paiement.

## 5 · Accuracy discipline (what is NOT claimed)
- Prix : **extraits du catalogue**, marqués « tarifs indicatifs — le tarif est confirmé avant le prélèvement ». Pas de totaux inventés, pas de promos.
- Aucune promesse de délai (« résultats le jour même ») — nous ne pouvons pas la vérifier.
- Pas de logos d'assurances (nous ne connaissons pas leurs conventions) → la question est posée dans le message.
- Pas de faux témoignages, pas de fausses certifications, pas de « N° d'agrément » que nous n'avons pas vérifié.
- Horaires affichés = leur propre statut WhatsApp (« Ouvert 24h/24 ») ; à confirmer (le dossier mentionne aussi 6j/7 07–18h).
- Photos : générées (aucun texte, aucun logo, vérifiées visuellement) — remplacées par leurs vraies photos à la livraison.
- Nom utilisé **avec leur accord implicite de destinataire** (cadeau nommé envoyé à eux seuls, page `noindex`, non listée) — conforme à la règle « pas de nom public sans autorisation ».

## 6 · Open questions for the owner (in the message, one at a time)
1. Les horaires exacts (24h/24 ? 6j/7 07–18h ?) et les urgences.
2. Mutuelles/assurances prises en charge (pour la bande partenaires).
3. Les résultats : retrait sur place seulement, ou envoi WhatsApp/e-mail ?
4. Prélèvement à domicile : proposé ou non.
5. Le titre exact de Dr Takala + accord pour sa photo.
6. Les tarifs : lesquels ont changé depuis la grille photographiée ?
