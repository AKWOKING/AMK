# GABARIT DE TÂCHE — Build de site (livrable non récurrent mais gabaritisé)

> `ops/` créé le 02/10 (KB §9, pilier 3). Le site est « le plus gros artefact payé » (King, 02/10) :
> il a droit au même gabarit que les récurrents.

**Déclencheur :** acompte crédité + proforma tamponnée (jamais « promis »).

**Rôles :** orchestrateur = build + QA · King = approbation des affirmations publiques.

**Entrées requises :**
1. Deep-dive client (`sales/research/<client>-deep-dive-*.md` ou dossier `clients/<slug>/`).
2. Numéro WhatsApp **vérifié dans l'app** (jamais un numéro non identifié).
3. Photos RÉELLES seulement — à défaut, illustrations légendées comme telles ; le site ne montre que du vrai.
4. Registre officiel / annuaire datés pour chaque affirmation publique (angle « introuvable » retiré si
   une page vivante existe — leçon Le Cristallin).

**Sous-tâches :**
1. Une page, mobile-first, orientée patient/prospect, bouton WhatsApp, FR d'abord (+ EN si bilingue).
2. Copy : les mots du client ; R1 si santé ; aucun concurrent ; aucune remise ; aucune promesse médicale.
3. `og:url` + `og:image` collés sur l'adresse réelle AVANT tout partage (leçon Cinq Sens 24/09 : carte
   partie sans vignette).
4. QA : `tools/qa/audit_a11y.py` (WCAG 2.2 AA) + `audit_hero.py` + `audit_images.py` + test lecteur-écran
   à l'oreille (`tools/qa/PROTOCOLE-LECTEUR-ECRAN.md`).
5. Deploy gate : `hosting/previews/README.md` — rien en public avant le déclencheur d'acompte.

**Heures estimées :** structure+copy 3 h · build 4 h · QA+corrections 2 h · deploy 0,5 h.

**Spec de sortie :** URL de preview 0.0.0.0-safe · rapport d'audits · fiche de handoff (vidéo + plan de
soin, `AMK-Playbook-Addendum-Outcomes-2026-09-15.md`).

**Exception :** photo réelle manquante à la livraison → le site part SANS la section, pas avec du stock ;
la section attend la séance (échange client fondateur ou ligne 15 000 FCFA — jamais une remise).

**Succès :** audits verts · zéro affirmation sans source datée · bouton WhatsApp vérifié en conditions
réelles · client propriétaire de tout, domaine à son nom (conditions §5).
