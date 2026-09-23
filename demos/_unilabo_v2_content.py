# -*- coding: utf-8 -*-
"""UNI-LABO — le contenu de la refonte (24/09/2026), séparé du gabarit.

RÈGLE DE CETTE PAGE : aucune phrase n'est inventée ici. Tout ce qui suit est repris de ce que le
laboratoire publie déjà (sa page en ligne du 18/09, sa grille tarifaire, ses messages), et **rien de ce
qui n'existe pas n'est écrit** — pas de prix, pas d'agrément, pas de délai, pas d'avis.

Deux langues, une seule source : chaque entrée porte `fr` et `en`, comme le veut §20.8 (les trois
endroits : `data-fr`, `data-en`, et le nœud visible — ici le nœud visible EST le français, par défaut).
"""

# ── Le laboratoire : ses faits, tels quels ────────────────────────────────────────────────────────
LAB = {
    "nom": "UNI-LABO",
    "qualif_fr": "Laboratoire d'analyses de biologie médicale",
    "qualif_en": "Medical biology laboratory",
    "ville_fr": "Bonamoussadi, Douala — Carrefour Etoo",
    "ville_en": "Bonamoussadi, Douala — Carrefour Etoo",
    "tel_fixe": "233 47 00 68", "tel_wa": "696 13 98 19",
    "wa": "https://wa.me/237696139819", "tel": "+237696139819", "tel_fixe_intl": "+237233470068",
    "mail": "u.labo@yahoo.fr",
    "adresse_fr": "Rue 5N441, Bonamoussadi (Makepe Bloc L) — repère Carrefour Etoo, Douala",
    "adresse_en": "Rue 5N441, Bonamoussadi (Makepe Bloc L) — landmark Carrefour Etoo, Douala",
    "horaires_fr": "Lundi–vendredi 07h–19h · samedi 07h–13h",
    "horaires_en": "Monday–Friday 7am–7pm · Saturday 7am–1pm",
    "biologiste": "Dr Tientcheu Philomène",
}

# ── Hero ─────────────────────────────────────────────────────────────────────────────────────────
HERO = {
    "sur_fr": "Bonamoussadi, Douala · français et anglais",
    "sur_en": "Bonamoussadi, Douala · French and English",
    "h1_fr": "Le résultat juste, du premier coup.",
    "h1_en": "The right result, first time.",
    "sub_fr": "Vous arrivez avec l'ordonnance de votre médecin : nous prélevons, nous analysons, et "
              "vous repartez en sachant quand revenir chercher le résultat.",
    "sub_en": "You come with your doctor's request: we take the sample, run the test, and you leave "
              "knowing when to come back for the result.",
    "cta_fr": "Prendre rendez-vous", "cta_en": "Book a visit",
    "cta2_fr": "Écrire sur WhatsApp", "cta2_en": "Message on WhatsApp",
}

# La fiche — la signature du build : le papier qu'on apporte et qu'on remplit.
FICHE = [
    ("Analyses", "Tests", "Glycémie · Hémogramme complet (NFS)", "Glucose · Complete blood count (CBC)"),
    ("Préparation", "Preparation", "À jeun 8 à 12 h, l'eau est permise", "Fasting 8 to 12 h, water allowed"),
    ("Moment", "Time", "Lundi–vendredi 7h–19h · samedi 7h–13h", "Monday–Friday 7am–7pm · Saturday 7am–1pm"),
]

# ── Les quatre étapes ────────────────────────────────────────────────────────────────────────────
JOURNEY = [
    ("Vous apportez l'ordonnance", "Bring the request",
     "Le papier de votre médecin, ou une photo nette si vous l'avez reçue par téléphone. Votre carte de couverture si vous en avez une.",
     "Your doctor's paper, or a clear photo if it came by phone. Your cover card if you have one."),
    ("Vous préparez l'analyse", "Prepare the test",
     "Certaines analyses demandent d'être à jeun. La consigne dépend de ce qui est prescrit : la fiche ci-dessous vous la donne.",
     "Some tests need fasting. The instruction depends on what is prescribed: the sheet below gives it to you."),
    ("Prélèvement sur place", "Sample taken on site",
     "Au laboratoire, Carrefour Etoo. Nous vous confirmons le délai au moment du dépôt.",
     "At the laboratory, Carrefour Etoo. We confirm the turnaround when you drop off the sample."),
    ("Vous repartez avec le résultat", "You leave with the result",
     "Remis au laboratoire, sur présentation du reçu — et expliqué par la biologiste si vous le souhaitez.",
     "Handed over at the laboratory on presentation of the receipt — and explained by the biologist if you wish."),
]

# ── Les quatre familles d'analyses (contenu publié par le laboratoire, repris mot pour mot) ──────
FAMILIES = [
    dict(slug="biochimie", fr="Biochimie", en="Biochemistry",
         quoi_fr="Sucre, cholestérol, rein, foie.", quoi_en="Sugar, cholesterol, kidney, liver.",
         items=[("Glycémie (à jeun et post-prandiale)", "Glucose (fasting and after meals)"),
                ("Cholestérol total, HDL, LDL, triglycérides", "Total cholesterol, HDL, LDL, triglycerides"),
                ("Créatinine et urée (fonction rénale)", "Creatinine and urea (kidney function)"),
                ("Transaminases (fonction du foie)", "Transaminases (liver function)")]),
    dict(slug="hematologie", fr="Hématologie", en="Haematology",
         quoi_fr="Le sang, compté et observé cellule par cellule.", quoi_en="Blood, counted and observed cell by cell.",
         items=[("Hémogramme complet (NFS)", "Complete blood count (CBC)"),
                ("Groupe sanguin et rhésus", "Blood group and rhesus"),
                ("Vitesse de sédimentation (VS)", "Erythrocyte sedimentation rate (ESR)"),
                ("Comptage des plaquettes", "Platelet count")]),
    dict(slug="serologie", fr="Sérologie &amp; immunologie", en="Serology &amp; immunology",
         quoi_fr="Infections et inflammation : ce que le corps a rencontré.", quoi_en="Infection and inflammation: what the body has met.",
         items=[("Widal (fièvre typhoïde)", "Widal (typhoid fever)"),
                ("Hépatites B et C", "Hepatitis B and C"),
                ("VIH 1 &amp; 2", "HIV 1 &amp; 2"),
                ("CRP (inflammation)", "CRP (inflammation)")]),
    dict(slug="hormonologie", fr="Hormonologie", en="Hormonology",
         quoi_fr="Thyroïde, fertilité, grossesse, suivi.", quoi_en="Thyroid, fertility, pregnancy, follow-up.",
         items=[("TSH, T3, T4 (thyroïde)", "TSH, T3, T4 (thyroid)"),
                ("Bêta-HCG (grossesse)", "Beta-HCG (pregnancy)"),
                ("FSH et LH", "FSH and LH"),
                ("Prolactine", "Prolactin")]),
]

# ── La préparation : les cinq situations que le laboratoire publie déjà ─────────────────────────
PREP = [
    ("Analyses à jeun", "Fasting tests",
     "Glycémie, cholestérol, triglycérides : venez le matin, sans manger depuis 8 à 12 heures. "
     "<b>L'eau est permise</b>, et vos médicaments habituels sont pris normalement, sauf avis contraire de votre médecin.",
     "Glucose, cholesterol, triglycerides: come in the morning, without food for 8 to 12 hours. "
     "<b>Water is allowed</b>, and your usual medication is taken as normal unless your doctor says otherwise.",
     "jeun"),
    ("Analyses d'urines", "Urine tests",
     "<b>Le recueil se fait au laboratoire</b> : nous vous remettons le flacon propre et la consigne au moment du dépôt. "
     "Pour certains examens, on demande la première urine du matin — nous vous le dirons à l'avance.",
     "<b>The sample is collected at the laboratory</b>: we hand you the clean container and the instruction when you arrive. "
     "Some tests need the first urine of the morning — we will tell you in advance.",
     None),
    ("Dosages hormonaux", "Hormone tests",
     "Plusieurs dosages hormonaux <b>se font le matin</b>, et certains dépendent du jour du cycle ou d'un moment précis de la journée. "
     "C'est l'analyse qui commande : demandez-nous la consigne exacte avant de venir, nous vous donnerons la date et l'heure.",
     "Many hormone tests <b>are done in the morning</b>, and some depend on the day of the cycle or a precise time of day. "
     "The test decides: ask us for the exact instruction before coming and we will give you the date and time.",
     None),
    ("Pour un enfant", "For a child",
     "<b>Précisez l'âge à l'accueil</b> : les valeurs normales ne sont pas les mêmes que chez l'adulte. Pour les tout-petits, "
     "venez si possible à deux et dites-le nous à l'avance — nous vous dirons le meilleur moment de la journée.",
     "<b>Mention the age at reception</b>: normal values differ from an adult's. For very young children, come with a second "
     "person if you can and tell us in advance — we will advise the best time of day.",
     None),
    ("Suivi d'un traitement", "Treatment follow-up",
     "<b>Apportez le résultat précédent</b> : la comparaison avec le nouveau est ce qui montre si le traitement agit. "
     "C'est aussi la question que votre médecin posera — autant l'avoir sous la main.",
     "<b>Bring the previous result</b>: comparing it with the new one is what shows whether the treatment is working. "
     "It is also the first question your doctor will ask — worth having it at hand.",
     None),
]

PREP_ALWAYS = ("Dans tous les cas : demandez-nous la consigne avant de venir. Une question sur WhatsApp coûte une minute "
               "et évite un déplacement pour rien.",
               "In every case: ask us before you come. A question on WhatsApp takes a minute and saves you a wasted trip.")

# ── Les résultats ───────────────────────────────────────────────────────────────────────────────
RESULTATS = {
    "t_fr": "Retrait au laboratoire", "t_en": "Collection at the laboratory",
    "p_fr": "Sur présentation du reçu remis au dépôt. Le délai dépend de l'analyse : il est confirmé au moment du prélèvement, "
            "pour que vous sachiez quand revenir. Si quelqu'un vient à votre place, prévenez-nous : nous dirons ce qu'il doit apporter.",
    "p_en": "On presentation of the receipt given at drop-off. The turnaround depends on the test: it is confirmed when the sample "
            "is taken, so you know when to come back. If someone collects it for you, tell us first: we will say what they need to bring.",
    "b_t_fr": "La biologiste", "b_t_en": "The biologist",
    "b_p_fr": "Dr Tientcheu Philomène, biologiste, conduit les analyses et peut vous expliquer un résultat. "
              "« Réaliser les analyses biologiques prescrites par un médecin, afin de confirmer ou d'écarter un diagnostic, "
              "de traiter une maladie ou de suivre un traitement. » C'est la mission du laboratoire, dans ses propres mots.",
    "b_p_en": "Dr Tientcheu Philomène, biologist, runs the tests and can explain a result. "
              "“To run the biological tests a doctor prescribes, in order to confirm or rule out a diagnosis, to treat an illness, "
              "or to follow a treatment.” That is the laboratory's mission, in its own words.",
}

# ── Nous trouver ────────────────────────────────────────────────────────────────────────────────
LIEU = [
    ("Quartier", "Quarter", "Bonamoussadi (Makepe Bloc L), Douala", "Bonamoussadi (Makepe Bloc L), Douala"),
    ("Repère", "Landmark", "Carrefour Etoo", "Carrefour Etoo"),
    ("Rue", "Street", "Rue 5N441 · BP 2592 Douala", "Rue 5N441 · BP 2592 Douala"),
    ("Horaires", "Hours", "Lundi–vendredi 07h–19h · Samedi 07h–13h", "Monday–Friday 7am–7pm · Saturday 7am–1pm"),
    ("WhatsApp", "WhatsApp", "696 13 98 19", "696 13 98 19"),
    ("Fixe", "Landline", "233 47 00 68", "233 47 00 68"),
    ("E-mail", "E-mail", "u.labo@yahoo.fr", "u.labo@yahoo.fr"),
    ("Paiement", "Payment", "Espèces", "Cash"),
    ("Langues", "Languages", "Français · English", "French · English"),
]

# ── FAQ ─────────────────────────────────────────────────────────────────────────────────────────
FAQ = [
    ("Faut-il être à jeun ?", "Do I need to fast?",
     "Pour la glycémie, le cholestérol et les triglycérides : 8 à 12 heures sans manger, l'eau est permise. Pour les autres "
     "analyses, ce n'est pas toujours nécessaire — demandez-nous avant de venir. Si votre médecin a donné une consigne précise, c'est elle qui compte.",
     "For glucose, cholesterol and triglycerides: 8 to 12 hours without food, water is allowed. For other tests it is not always "
     "needed — ask us before coming. If your doctor gave a specific instruction, that one prevails."),
    ("Quand venir pour un dosage hormonal ?", "When should I come for a hormone test?",
     "Souvent le matin, et parfois à un jour précis du cycle. Écrivez-nous le nom de l'analyse : nous vous donnons la date et "
     "l'heure exactes — c'est la seule façon d'éviter un déplacement pour rien.",
     "Often in the morning, and sometimes on a specific day of the cycle. Message us the name of the test: we give you the exact "
     "date and time — the only way to avoid a wasted trip."),
    ("Qu'est-ce que j'apporte ?", "What should I bring?",
     "L'ordonnance de votre médecin (ou sa photo), votre carte de couverture si vous en avez une, et votre ancien résultat s'il "
     "s'agit d'un suivi.",
     "Your doctor's request (or a photo of it), your cover card if you have one, and your previous result if this is a follow-up."),
    ("Combien coûte une analyse ?", "How much does a test cost?",
     "Le tarif dépend de l'analyse et du réactif utilisé. Envoyez-nous le nom de l'analyse (ou l'ordonnance en photo) sur "
     "WhatsApp : nous vous répondons avec le prix avant que vous vous déplaciez.",
     "The price depends on the test and the reagent used. Send us the name of the test (or a photo of the request) on WhatsApp: "
     "we reply with the price before you travel."),
    ("Où se trouve exactement le laboratoire ?", "Where exactly is the laboratory?",
     "À Bonamoussadi, au carrefour Etoo — Rue 5N441 (Makepe Bloc L), Douala. Le plan ci-dessus montre le carrefour : le "
     "laboratoire est indiqué en violet.",
     "In Bonamoussadi, at Carrefour Etoo — Rue 5N441 (Makepe Bloc L), Douala. The sketch above shows the junction: the "
     "laboratory is marked in violet."),
]

# ── Le formulaire : les vingt analyses et les quatre moments, tels quels (ne pas renommer : les tests s'y appuient) ──
FAM_GROUPS = [
    ("Biochimie", "Biochemistry", "jeun", [
        ("Glycémie (à jeun)", "Glucose (fasting)", "jeun"),
        ("Cholestérol &amp; triglycérides", "Cholesterol &amp; triglycerides", "jeun"),
        ("Créatinine et urée", "Creatinine and urea", None),
        ("Transaminases (foie)", "Transaminases (liver)", None)]),
    ("Hématologie", "Haematology", None, [
        ("Hémogramme complet (NFS)", "Complete blood count (CBC)", None),
        ("Groupe sanguin et rhésus", "Blood group and rhesus", None),
        ("Vitesse de sédimentation", "Erythrocyte sedimentation rate", None),
        ("Plaquettes", "Platelets", None)]),
    ("Sérologie &amp; immunologie", "Serology &amp; immunology", None, [
        ("Widal (typhoïde)", "Widal (typhoid)", None),
        ("Hépatites B et C", "Hepatitis B and C", None),
        ("VIH 1 &amp; 2", "HIV 1 &amp; 2", None),
        ("CRP (inflammation)", "CRP (inflammation)", None)]),
    ("Hormonologie", "Hormonology", None, [
        ("TSH, T3, T4 (thyroïde)", "TSH, T3, T4 (thyroid)", "hormones"),
        ("Prolactine", "Prolactin", "hormones"),
        ("Bêta-HCG (grossesse)", "Beta-HCG (pregnancy)", "hormones"),
        ("FSH et LH", "FSH and LH", "hormones")]),
    ("Autre, ou je ne sais pas encore", "Other, or I am not sure yet", None, [
        ("Analyse d'urines", "Urine test", "urines"),
        ("Autre analyse / à préciser", "Another test / to be specified", "autre"),
        ("J'ai une ordonnance, choisissez pour moi", "I have a prescription, advise me", "ordonnance")]),
]
MOMENTS = [("Matin (7h–12h)", "Morning (7am–12pm)"),
           ("Après-midi (12h–16h)", "Afternoon (12pm–4pm)"),
           ("Samedi matin (7h–13h)", "Saturday morning (7am–1pm)"),
           ("Peu importe, le plus tôt possible", "Any time, as soon as possible")]

# ── Pied de page ────────────────────────────────────────────────────────────────────────────────
FOOT = {
    "pres_fr": "Laboratoire d'analyses de biologie médicale à Bonamoussadi, Douala — Carrefour Etoo. "
               "Analyses prescrites par votre médecin, résultats remis au laboratoire.",
    "pres_en": "Medical biology laboratory in Bonamoussadi, Douala — Carrefour Etoo. Tests prescribed by "
               "your doctor, results handed over at the laboratory.",
    "note_fr": "Maquette préparée par AMK pour UNI-LABO — horaires, services et mentions à valider par le laboratoire avant mise en ligne.",
    "note_en": "Mockup prepared by AMK for UNI-LABO: hours, services and wording to be validated by the laboratory before going live.",
}
