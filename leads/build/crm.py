#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — CRM microtâche M1 : extraire + dédoublonner → leads/CRM.csv

Source : `leads_50.xlsx` (onglet « Leads 50 », 38 lignes) + OraCare237 (onglet
« Pipeline - 5 Stages ») + les 15 leads qui n'existent qu'en prose dans `sales/*.md`
et `clients/*/` — liste établie par `CRM-AUDIT-AND-PROPOSAL-2026-09-18.md` §1.

Règles tenues par ce script :
  · les 27 colonnes du classeur sont conservées **à l'identique, avec leurs noms**
  · on AJOUTE des champs, on ne remplace rien
  · **aucune invention** : un champ vide reste vide. Là où la donnée n'existe pas,
    la cellule est vide — jamais un « N/A » qui se lirait comme une information.
  · le dédoublonnage ne supprime pas de ligne : il relie (`same_buyer_as`).
    Le audit §9 dit « 54 lignes » ET « COMOBIL + GS WAFO → une fiche, un acheteur ».
    Les deux tiennent seulement si la liaison est un champ, pas une suppression.
  · `kill list` et `health` ne sont PAS stockés : ils se calculent (§7).

Usage :  python3 leads/build/crm.py [--csv leads/CRM.csv]
"""
import argparse
import csv
import pathlib
import sys

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl manquant : pip install --break-system-packages openpyxl")

ROOT = pathlib.Path(__file__).resolve().parents[2]
XLSX = ROOT / "leads" / "leads_50.xlsx"

# ── Correspondance nom court → nom EXACT de la colonne du classeur.
#    Leclasseur garde ses noms (espaces compris) ; le code utilise des identifiants lisibles.
#    Sans cette table, un nom approchant était jeté en silence (bug du 19/09, 15 leads touchés).
KEYMAP = {
    "city": "City", "language": "Language", "decision": "Decision maker",
    "contacted": "Contacted", "reply": "Reply", "demo": "Demo made",
    "wa": "WhatsApp", "org": "School",
    "contact_channel": "Contact channel", "notes": "Notes",
}

# ── Nouveaux champs (audit §7). On ajoute, on ne remplace pas. ──────────────────
NEW_FIELDS = [
    # identification
    "slug", "org_type", "stage",
    # contact
    "contact_name", "contact_role", "wa_number", "wa_verified", "profile_name_seen",
    # vérité des échanges
    "reply_type", "last_send_state",
    # site web
    "site_url", "site_checked_on",
    # gestion
    "source", "source_detail", "added_on", "qualified_on", "stage_since",
    "follow_ups_sent", "disqualification_reason",
    # dédoublonnage (M1) — relie les lignes du même acheteur sans en supprimer aucune
    "same_buyer_as",
    # contradictions (M2) — valeur retenue + valeur écartée, verbatim conservé
    "contradiction", "value_kept", "value_discarded",
    # M1-bis : pourquoi un numéro est inutilisable (canal injoignable, numéro erroné…)
    "wa_number_note",
    # M4 : le dossier de travail réel (concept, inspirations, maquette). L'audit §4 : 5 dossiers
    # sur 8 n'avaient AUCUNE ligne — du travail qui existe et que le CRM ignore.
    "dossier",
]

# ── Les 15 leads hors classeur (audit §1), avec les seuls faits sourcés du dépôt ──
#    Aucun numéro, aucune ville, aucun état qui ne soit écrit dans sales/*.md ou clients/*/
PROSE_LEADS = [
    dict(slug="skye-douala", org="Cabinet Dentaire The Skye", city="Douala (Bonamoussadi)",
         org_type="clinic", language="FR/EN", wa_number="677 79 69 99", wa_verified="yes",
         contact_name="", decision="", contact_channel="WhatsApp",
         wa="Oui (profil Business, logo) — vérifié par King 16/09",
         source="google_maps", source_detail="Douala sweep 15/09 — dentaire Bonamoussadi",
         stage="qualifying", contacted="Yes", reply="No",
         demo="Yes", last_send_state="sent", follow_ups_sent="1",
         notes="Message 16/09. Relance M+2 (FU1) partie 18/09 20:22. Concept live : concept-skye.vercel.app"),
    dict(slug="yaks-douala", org="Cabinet Dentaire YAKS", city="Douala (Logbessou)",
         org_type="clinic", language="FR/EN", wa_number="672 70 20 78", wa_verified="yes",
         contact_channel="WhatsApp", source="google_maps",
         source_detail="Douala sweep 15/09 — dentaire Logbessou",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="1",
         notes="Message 16/09. Relance M+2 (FU1) partie 18/09 20:22. Concept live : concept-yaks-v1.vercel.app"),
    dict(slug="afrique-labo-douala", org="Afrique Labo SARL", city="Douala (Bessengue)",
         org_type="lab", language="FR", wa_number="690 54 70 93", wa_verified="yes",
         contact_channel="WhatsApp", source="directory",
         source_detail="maligah/pagespratiques — numéro joignable vérifié",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="1",
         notes="Message 1 envoyé 17/09 13:24. **FU1 (M+2) ENVOYÉE par King le 19/09** (confirmé par lui : "
               "« I have already sent message de relance »). FU2 (M+4) = lundi 21/09, angle résultats WhatsApp. "
               "Concept live : concept-afriquelabo-v1.vercel.app. "
               "Numéros interdits : 699 73 36 25 et 674 46 62 15 (secours seulement si l'invitation vient d'eux)."),
    dict(slug="joss-medi-buea", org="JOSS MEDI Clinic", city="Buea",
         org_type="clinic", language="EN", wa_number="", wa_verified="no",
         contact_channel="Facebook", source="facebook",
         source_detail="292 clics WhatsApp mesurés — signal de demande fort",
         stage="disqualified", contacted="No", reply="No", demo="No", follow_ups_sent="0",
         disqualification_reason="3 portes sur 3 en échec (17/09) : numéro FB 674 84 39 02 non inscrit sur "
                                 "WhatsApp ; dernière publication 24/06/2022 (dormante) ; 11-50 employés depuis 2009 "
                                 "= acheteur collectif. Parqué dormant, pas perdu.",
         notes="NE JAMAIS envoyer. Le 677 58 42 73 du dossier n'a jamais été confirmé sur WhatsApp (correction de King)."),
    dict(slug="opticien-bali-douala", org="L'Opticien Bali SARL", city="Douala (Bali)",
         org_type="other", language="FR", wa_number="670 27 60 65", wa_verified="yes",
         contact_name="", contact_channel="WhatsApp", source="directory",
         source_detail="Douala sweep — 2 039 likes FB, pas de site",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="3/3 portes le 17/09 (compte WhatsApp Business + catalogue + activité du jour ; mono-boutique "
               "= propriétaire). Message envoyé 17/09. Live : amk-cm.vercel.app/opticien/. Relances : dim 20 / mar 22 / ven 25."),
    dict(slug="la-bethanie-bonaberi", org="Clinique La Béthanie", city="Douala (Bonabéri)",
         org_type="clinic", language="FR", wa_number="677 76 07 82", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory",
         source_detail="210 clics WhatsApp mesurés",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="Capture de King : +237 77760782 sans profil Business (aucun nom, aucune catégorie) → ligne "
               "personnelle probable. Envoi maintenu 17/09 avec ligne de repli (§2e/§3b). Live : labethanie-concept.vercel.app"),
    dict(slug="jempo-deido", org="J&E Memorial Polyclinic (JEMPO)", city="Douala (Deido/Bessengue)",
         org_type="clinic", language="FR/EN", wa_number="696 71 06 99", wa_verified="yes",
         profile_name_seen="J&E MEMORIAL — Medical & health, mention « Polyclinic »",
         contact_channel="WhatsApp", source="directory", source_detail="3/3 portes le 17/09",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="Message envoyé 17/09. Premier build sous la règle footer §20. Live : jempo-concept.vercel.app"),
    dict(slug="maison-optique-douala", org="Maison Optique", city="Douala",
         org_type="other", language="FR", wa_number="657 73 70 45", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory",
         source_detail="1 364 likes FB, activité WhatsApp relevée",
         stage="prospecting", contacted="No", reply="No", demo="No", follow_ups_sent="0",
         notes="Qualifié le 17/09 mais JAMAIS contacté. Concept optique générique à faire."),
    dict(slug="camera-akwa", org="Cabinet Médical CAMERA", city="Douala (Akwa)",
         org_type="clinic", language="FR", wa_number="699 90 53 27", wa_verified="yes",
         contact_name="Dr Simo Happy", contact_role="Médecin", contact_channel="WhatsApp",
         source="directory", source_detail="252 clics WhatsApp mesurés (DoualaTour) — le plus fort du lot",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="Envoi 18/09 ~18:30 SANS maquette (vitesse). Maquette disponible : clients/douala-cliniques/01-camera.jpg."),
    dict(slug="le-nid-bessengue", org="Polyclinique de la Gare LE NID", city="Douala (Bessengue)",
         org_type="clinic", language="FR", wa_number="699 987 775", wa_verified="yes",
         contact_name="Dr Ndongo Diye Eitel", contact_role="Médecin", contact_channel="WhatsApp",
         source="directory", source_detail="199 clics WhatsApp mesurés — entrée de la gare Bessengue",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="Envoi 18/09 ~18:30 sans maquette. Maquette : clients/douala-cliniques/02-le-nid.jpg. "
               "NB : le fixe 233 40 09 61 était jugé comme seule ligne fiable avant la vérification du mobile."),
    dict(slug="wonders-bonamoussadi", org="Wonders Medical Foundation", city="Douala (Bonamoussadi)",
         org_type="clinic", language="FR", wa_number="", wa_verified="unknown",
         contact_channel="", source="directory",
         source_detail="302-339 clics WhatsApp — la plus forte activité du lot ; dernière visite connue 12/03/2026",
         stage="prospecting", contacted="No", reply="No", demo="Yes", follow_ups_sent="0",
         notes="Rue 5N180. NUMÉRO INTROUVABLE (masqué derrière « Cliquez ici » sur DoualaTour). Maquette faite "
               "(clients/douala-cliniques/03-wonders.jpg) mais RIEN NE PART sans numéro vérifié. "
               "Signal de demande le plus fort du fichier — vaut l'effort de le retrouver."),
    dict(slug="adonai-douala", org="Cabinet Biomédical Adonaï", city="Douala",
         org_type="lab", language="FR", wa_number="696 53 87 75", wa_verified="yes",
         contact_channel="WhatsApp", source="directory",
         source_detail="profil WhatsApp Business vérifié (capture King)",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="Envoyé 18/09 13:39. ⚠️ reply_type = auto : le cabinet envoie automatiquement « Merci d'avoir "
               "contacté cabiomedadonai » à tout nouveau contact. Ce n'est PAS une réponse et ne compte pas dans le PRR."),
    dict(slug="malia-labo-douala", org="Malia Labo", city="Douala",
         org_type="lab", language="FR", wa_number="694 56 22 44", wa_verified="yes",
         contact_channel="WhatsApp", source="directory",
         source_detail="profil WhatsApp Business vérifié (capture King)",
         stage="qualifying", contacted="Yes", reply="No", demo="Yes",
         last_send_state="sent", follow_ups_sent="0",
         notes="Envoyé 18/09 13:42. Maquette : clients/douala-cliniques/06-malia-labo.jpg"),
    dict(slug="qualitech-douala", org="Laboratoire QUALITECH", city="Douala (Logbessou/Deido)",
         org_type="lab", language="FR", wa_number="690 72 01 84", wa_verified="unknown",
         contact_channel="", source="directory", source_detail="",
         stage="disqualified", contacted="No", reply="No", demo="Yes", follow_ups_sent="0",
         site_url="https://qualitechsarl.org", site_checked_on="2026-09-18",
         disqualification_reason="A DÉJÀ UN SITE VIVANT (qualitechsarl.org). Hors cible. "
                                 "La maquette avait été produite AVANT la vérification — d'où la règle du 18/09 : "
                                 "vérifier l'existence d'un site AVANT de produire.",
         notes="Maquette : clients/douala-cliniques/05-qualitech.jpg — NE PAS ENVOYER."),
    dict(slug="clinique-des-anges-douala", org="Clinique des Anges", city="Douala",
         org_type="clinic", language="FR", wa_number="", wa_verified="unknown",
         contact_channel="", source="directory", source_detail="",
         stage="disqualified", contacted="No", reply="No", demo="No", follow_ups_sent="0",
         site_url="https://angesclinic-dla.cm", site_checked_on="2026-09-18",
         disqualification_reason="A DÉJÀ UN SITE VIVANT (angesclinic-dla.cm). Hors cible.",
         notes="Écartée à la vérification, aucune maquette produite (le contrôle a fonctionné cette fois)."),
]

# ── Les envois du vendredi 18/09 au soir, absents de l'audit du matin (trouvé le 19/09
#    en cherchant la réponse de Bonanjo dans le CRM — elle n'y était pas).
#    Source : `sales/Activity-Log.md`, tableau des envois. Seuls les « Envoyé » sont ici.
SENT_1809 = [
    # ~18:30 — labos et cliniques
    dict(slug="discovery-labs-bassong", org="Discovery Labs", city="Douala (Bassong)", language="FR",
         org_type="lab", wa_number="694 86 13 61", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="Remote-Sweep §C — dans nos fichiers depuis le 15/09",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 ~18:30, sans maquette (vitesse)."),
    dict(slug="uni-labo-bonamoussadi", org="UNI-LABO", city="Douala (Bonamoussadi, Carrefour Etoo)", language="FR/EN",
         org_type="lab", wa_number="696 13 98 19", wa_verified="yes", contact_channel="WhatsApp",
         decision="Dr Tientcheu Philomène (biologiste)", source="directory",
         source_detail="Remote-Sweep §C — Lun-Ven 07h-19h, Sam 07h-13h",
         contacted="Yes", reply="Yes", demo="Yes", last_send_state="sent", follow_ups_sent="0",
         notes="⭐ LE LEAD LE PLUS ENGAGÉ. Envoyé 18:41, il a répondu « Bsr » à 20:57 (2 coches → les deux "
               "messages de 21:47 et 22:05 ne sont PAS lus, last seen 21:04). SITE COMPLET construit et déployé : "
               "https://uni-labo.vercel.app. Contrôle de lecture prévu sam 19/09, M+2 dim 20, M+4 mar 22, M+7 ven 25 → parked."),
    dict(slug="yondja-analyse-douala", org="YONDJA ANALYSE", city="Douala", language="FR",
         org_type="lab", wa_number="696 88 88 23", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="Remote-Sweep §C", contacted="Yes", reply="No", demo="No",
         last_send_state="sent", notes="Envoyé 18/09 ~18:30, sans maquette."),
    dict(slug="laboratoire-du-chateau-bonaberi", org="Laboratoire du Château", city="Douala (Bonabéri)",
         language="FR", org_type="lab", wa_number="676 94 69 93", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="Remote-Sweep §C",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 ~18:30, sans maquette."),
    dict(slug="departement-biologique-akwa", org="Département Biologique", city="Douala (Akwa I)",
         language="FR", org_type="lab", wa_number="699 85 33 52", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="Remote-Sweep §C",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 ~18:30, sans maquette."),
    # ~19:00 — cabinets de Bonapriso/Bali/Akwa
    dict(slug="cabinet-isis-bonapriso", org="Cabinet Médical ISIS", city="Douala (Bonapriso)", language="FR",
         org_type="clinic", wa_number="699 34 93 89", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="pagespratiquescm — cabmed", contacted="Yes", reply="No",
         demo="No", last_send_state="sent", notes="Envoyé 18/09 ~19:00, sans maquette."),
    dict(slug="cabinet-la-cerisaie-bonapriso", org="Cabinet Médical La Cerisaie", city="Douala (Bonapriso)",
         language="FR", org_type="clinic", wa_number="699 95 51 64", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm — cabmed",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 ~19:00, sans maquette."),
    dict(slug="cabinet-idoc-bonapriso", org="Cabinet Médical i'DoC", city="Douala (Bonapriso)", language="FR",
         org_type="clinic", wa_number="699 68 05 88", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="pagespratiquescm — cabmed", contacted="Yes", reply="No",
         demo="No", last_send_state="sent", notes="Envoyé 18/09 ~19:00, sans maquette."),
    dict(slug="centre-des-capucines-bonapriso", org="Centre Médical des Capucines", city="Douala (Bonapriso)",
         language="FR", org_type="clinic", wa_number="699 72 36 93", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm — cabmed",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 ~19:00, sans maquette."),
    dict(slug="cabinet-brulet-epaka-bonapriso", org="Cabinet du Dr Brulet Epaka", city="Douala (Bonapriso)",
         language="FR", org_type="clinic", wa_number="694 77 74 54", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm — cabmed",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 ~19:00, sans maquette."),
    dict(slug="centre-kouam-samuel-bali", org="Centre Médical Kouam Samuel", city="Douala (Bali)", language="FR",
         org_type="clinic", wa_number="677 39 35 31", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="pagespratiquescm — cabmed", contacted="Yes", reply="No",
         demo="No", last_send_state="sent", notes="Envoyé 18/09 ~19:00, sans maquette."),
    dict(slug="das-group-international-akwa", org="DAS Group International", city="Douala (Akwa)", language="FR",
         org_type="other", wa_number="680 100 626", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="annuaires Akwa", contacted="Yes", reply="No", demo="No",
         last_send_state="sent", notes="Envoyé 18/09 ~19:00, sans maquette."),
    # 19:42
    dict(slug="centre-medical-de-bonanjo", org="Centre Médical de Bonanjo", city="Douala (Bonapriso, ancien aéroport)",
         language="FR", org_type="clinic", wa_number="694 57 22 77", wa_verified="yes",
         contact_channel="WhatsApp", decision="Dr Tchaleu B. Clet — NEUROLOGUE",
         source="directory", source_detail="maligah + mondocteur237 (consultation 20 000 FCFA, publique)",
         contacted="Yes", reply="Yes", demo="Yes", last_send_state="sent", follow_ups_sent="0",
         profile_name_seen="Centre Médical de Bonanjo — Bonapriso",
         notes="⭐ A RÉPONDU. Envoyé 18/09 19:42 (2 coches) → « Bjr merci je vous reviens » le 19/09 à 08:44. "
               "Maquette personnalisée envoyée le 19/09 : clients/_mockups/bonanjo.jpg. "
               "FAIT DÉCISIF : le Dr Tchaleu figure déjà sur mondocteur237.com (annuaire de prise de rendez-vous) "
               "→ il cherche déjà des patients en ligne, mais sur la plateforme d'un autre. C'est le profil "
               "« paie déjà pour du trafic » (§21.7), notre meilleur angle. Services publics vérifiés (maligah) : "
               "neurologie, médecine générale, radiologie, chirurgie, gynécologie, pédiatrie, échographie, accouchement."),
    dict(slug="kamais-optic-bessengue", org="Kamaïs Optic", city="Douala (Bessengue)", language="FR",
         org_type="other", wa_number="678 435 460", wa_verified="yes", contact_channel="WhatsApp",
         source="directory", source_detail="annuaires Bessengue", contacted="Yes", reply="No", demo="No",
         last_send_state="sent", notes="Envoyé 18/09 19:42, sans maquette."),
    # 20:02
    dict(slug="cabinet-dentaire-emmanuel-bonamoussadi", org="Cabinet Dentaire Emmanuel",
         city="Douala (Bonamoussadi)", language="FR", org_type="clinic", wa_number="694 42 62 39",
         wa_verified="yes", contact_channel="WhatsApp", source="directory",
         source_detail="pagespratiquescm — dentaire", contacted="Yes", reply="No", demo="No",
         last_send_state="sent", notes="Envoyé 18/09 20:02, sans maquette."),
    dict(slug="clinique-de-luniversite-bassa", org="Clinique de L'université", city="Douala (Bassa)",
         language="FR", org_type="clinic", wa_number="694 36 02 03", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="annuaires Bassa",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 20:02, sans maquette."),
    dict(slug="medi-labo-akwa", org="MEDI LABO", city="Douala (Akwa, 1927 Bld de la République)",
         language="FR", org_type="lab", wa_number="677 81 70 25", wa_verified="yes",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm",
         contacted="Yes", reply="No", demo="No", last_send_state="sent",
         notes="Envoyé 18/09 20:02, sans maquette."),
]

# ── Numéros testés le 18/09 et ÉCARTÉS : la donnée qui évite de refaire le travail.
#    Ce sont les « portes A » du MQL — soit le numéro ne va pas sur WhatsApp, soit il est faux.
NOT_REACHABLE = [
    ("douala-clinic-makepe", "Douala clinic", "Douala (Makepe BM, rue des pavés)", "clinic", "650 34 32 01",
     "pas sur WhatsApp (vérifié par King 18/09)"),
    ("clinique-des-cites-makepe", "Clinique des Cités", "Douala (Makepe, face Cinpharm)", "clinic", "699 22 62 74",
     "pas sur WhatsApp (vérifié par King 18/09)"),
    ("cmodn-makepe", "Centre Médical d'Ophtalmologie de Douala-Nord (CMODN)", "Douala (Makepe)", "clinic",
     "698 00 68 98", "pas sur WhatsApp (vérifié par King 18/09)"),
    ("perseverance-bonaberi", "Centre de Soins Médic-o-La Persévérance", "Douala (Bonabéri)", "clinic",
     "677 69 25 04", "pas sur WhatsApp (vérifié par King 18/09)"),
    ("imagerie-saint-joseph", "Centre d'Imagerie Médicale Saint Joseph", "Douala (Bonamoussadi)", "clinic",
     "690 412 400", "pas sur WhatsApp (vérifié par King 18/09)"),
    ("polyclinique-innova", "Polyclinique Innova", "Douala", "clinic", "674 145 740",
     "numéro indisponible (King, 18/09 19:18)"),
    ("centre-medical-saint-luc", "Centre Médical Saint Luc", "Douala (Rond-point Deido)", "clinic", "699 08 67 11",
     "aucun profil Business à ce numéro"),
    ("le-cigah-bonaberi", "Clinique Traditionnelle Moderne du Dr Lecigah", "Douala (Bonabéri Sodiko)", "clinic",
     "699 96 95 77", "aucun profil Business à ce numéro"),
    ("labo-phanuel-akwa", "LABO-PHANUEL", "Douala (Akwa)", "lab", "243 17 94 71",
     "ligne fixe — pas un mobile"),
    ("cem-eces-bonaberi", "Clinique Médico-Chirurgicale de L'Espoir (CEMECES)", "Douala (Bonabéri Sodiko)",
     "clinic", "674 93 66 04",
     "NUMÉRO ERRONÉ : ce mobile est celui d'INSES, un institut supérieur. Maligah attribuait le numéro de "
     "l'école à la clinique. La vérification d'identité à l'écran a évité un message à la mauvaise personne."),
]


def _not_reachable_rows():
    out = []
    for slug, org, city, kind, num, why in NOT_REACHABLE:
        out.append(dict(slug=slug, org=org, city=city, language="FR", org_type=kind,
                        wa_number=num, wa_verified="no", wa_number_note=why,
                        stage="prospecting", contacted="No", reply="No", demo="No",
                        source="directory", source_detail="annuaire de Douala",
                        disqualification_reason=f"canal injoignable — {why}",
                        notes=f"⛔ NE PAS ENVOYER sur {num} : {why}. Vérifié le 18/09."))
    # INSES porte le numéro « CEMECES » : c'est un prospect À PART (institut supérieur),
    # et le seul cas où un même numéro sert deux organisations.
    out.append(dict(slug="inses-douala", org="INSES — institut supérieur", city="Douala", language="FR/EN",
                    org_type="school", wa_number="674 93 66 04", wa_verified="yes",
                    stage="prospecting", contacted="No", reply="No", demo="No",
                    source="walk_in", source_detail="affiche vue par King 18/09 — BTS · HND · Licence · Master",
                    notes="Piste ouverte : le mobile 674 93 66 04 est bien celui d'INSES (confirmé par capture). "
                          "La même affiche porte « LA CLINIQUE DE L'ESPOIR » → promoteur probablement commun "
                          "école + clinique. Deux offres possibles en une conversation. **Jamais contacté.**"))
    return out


# ── Les 19 laboratoires du pack du 19/09 au soir (`sales/Send-Pack-2026-09-19-LABS.md`).
#    Aucun doublon : les numéros ont été croisés avec les 82 lignes du CRM AVANT d'écrire.
#    `demo` est renseigné seulement pour les 4 qui ont une maquette ce soir.
LABS_1909 = [
    # BATCH A — Akwa / Deido / Bonamoussadi
    dict(slug="labo-meka-bonamoussadi", org="Laboratoire Meka", city="Douala (Bonamoussadi, 241 Rue 5N036)",
         org_type="lab", language="FR", wa_number="699 79 93 35", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm — 2e ligne : 677 70 57 27",
         stage="prospecting", contacted="No", reply="No", demo="Yes",
         dossier="clients/_mockups/labs/meka.jpg",
         notes="BATCH A. Maquette faite (clients/_mockups/labs/meka.jpg). Argument : la liste des examens et "
               "leur préparation — la question posée au téléphone toute la journée. Bonamoussadi est le quartier "
               "où nos cibles dentaires (Skye, YAKS, Emmanuel) sont déjà actives."),
    dict(slug="niva-labo-akwa", org="Niva Labo", city="Douala (Akwa, Av King Akwa — face Meche a meche)",
         org_type="lab", language="FR", wa_number="679 03 13 30", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm / doualazoom",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH A. Argument : Akwa est le quartier le plus concurrentiel de Douala et son voisin immédiat, "
               "Douala Labo, A UN SITE avec espace résultats. Le patient qui compare choisit celui qu'il trouve."),
    dict(slug="flemming-dream-bessengue", org="Flemming Dream Labo",
         city="Douala (Bessenguè, feu rouge, Bld de la République)", org_type="lab", language="FR",
         wa_number="699 81 34 04", wa_verified="unknown", contact_channel="WhatsApp",
         source="directory", source_detail="pagespratiquescm (liste papier — absent des annuaires en ligne)",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH A. N'apparaît dans AUCUN annuaire en ligne. Nom mémorable, trace nulle : "
               "quand un patient tape « Flemming Dream », il ne trouve rien."),
    dict(slug="interlabo-akwa", org="Interlabo", city="Douala (Akwa, 780 Rue E. Betote — R. Pau)",
         org_type="lab", language="FR", wa_number="677 75 54 21", wa_verified="unknown",
         contact_channel="WhatsApp", decision="Dr Fotso Kuaté — biologiste (nom public)",
         source="directory", source_detail="pagespratiquescm",
         stage="prospecting", contacted="No", reply="No", demo="Yes",
         dossier="clients/_mockups/labs/interlabo.jpg",
         notes="BATCH A. Maquette faite. Argument : le nom du biologiste rassure ceux qui le connaissent déjà, "
               "mais un patient qui cherche « laboratoire sérieux à Akwa » ne tombe jamais sur lui."),
    dict(slug="labiomed-deido", org="Labiomed", city="Douala (Deido, 104 Route Deido-Bassa)",
         org_type="lab", language="FR", wa_number="699 98 54 66", wa_verified="unknown",
         contact_channel="WhatsApp", decision="Dr Fomekong Kuate Guy — biologiste (nom public)",
         source="directory", source_detail="pagespratiquescm",
         stage="prospecting", contacted="No", reply="No", demo="Yes",
         dossier="clients/_mockups/labs/labiomed.jpg",
         notes="BATCH A. Maquette faite. Argument : Deido-Bassa est un axe en travaux chroniques — "
               "une page qui explique l'accès supprime des dizaines d'appels par semaine."),
    dict(slug="la-passerelle-deido", org="Labo La Passerelle", city="Douala (Deido, 820 Bld de la Réunification)",
         org_type="lab", language="FR", wa_number="694 71 91 22", wa_verified="unknown",
         contact_channel="WhatsApp", decision="Dr Djanpou — biologiste (nom public)",
         source="directory", source_detail="pagespratiquescm",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH A. Argument : « La Passerelle » est un nom qu'on retient mais qui n'existe pas en ligne, "
               "et le labo communique par une adresse yahoo — jamais de présence propre."),
    dict(slug="biodiagnostics-sable", org="Laboratoire Biodiagnostics", city="Douala (Sable, Rue Deido-Bonanjo)",
         org_type="lab", language="FR", wa_number="699 92 91 98", wa_verified="unknown",
         contact_channel="WhatsApp", decision="Dr Tankoua Jean Alain — biologiste (nom public)",
         source="directory", source_detail="pagespratiquescm",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH A. ⚠️ Un « Laboratoire Biodiagnostic » existe aussi à New-Bell (Rue du Roi Njoya), "
               "probablement le MÊME biologiste : deux adresses, une seule page à faire. "
               "Argument : avec deux adresses, un patient ne sait pas laquelle choisir — rien ne l'explique."),
    # BATCH B — Bonabéri / New-Bell / Akwa / Bali
    dict(slug="diagmed-bonaberi", org="Diagmed", city="Douala (Bonabéri, Rue 4.352 — Route du Lycée)",
         org_type="lab", language="FR", wa_number="698 97 22 03", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory", source_detail="pagespratiquescm — 2e ligne : 675 96 05 98",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH B. Bonabéri = le quartier de La Béthanie, déjà contactée. Argument : résultats annoncés "
               "sur WhatsApp au lieu de faire revenir le patient — la question la plus posée en salle d'attente."),
    dict(slug="aube-labo-akwa", org="Aube Labo", city="Douala (Akwa II)", org_type="lab", language="FR",
         wa_number="693 06 81 84", wa_verified="unknown", contact_channel="WhatsApp",
         source="directory", source_detail="goafricaonline — Akwa II",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH B. Argument : le repère « derrière l'ancien cinéma Le Berlioz » ne parle plus aux moins "
               "de 30 ans — un point Maps cliquable vaut mieux qu'un repère disparu."),
    dict(slug="hyrus-labo-deido", org="Hyrus Labo", city="Douala (Deido, Bld de la République)",
         org_type="lab", language="FR", wa_number="699 76 01 18", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory",
         source_detail="pagespratiquescm + PDF réseau de soins Société Générale",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH B. Argument : sur le boulevard de la République — un emplacement que beaucoup envieraient, "
               "mais qu'on ne trouve pas en ligne."),
    dict(slug="labtag-bali", org="Labtag", city="Douala (Bali, 301 Rue Ngosso Din)", org_type="lab",
         language="FR", wa_number="699 68 30 50", wa_verified="unknown", contact_channel="WhatsApp",
         decision="Dr Tagu J.P. — biologiste (nom public)", source="directory", source_detail="pagespratiquescm",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH B. ⚠️ MÊME ADRESSE ET MÊME NOM que « Dr Jean Pierre Tagu » (699 91 66 16) : "
               "NE PAS ENVOYER AUX DEUX. Envoyer Labtag d'abord, l'autre sert de relance. "
               "Argument : un fax, en 2026, est le signe le plus net d'une présence en ligne jamais construite."),
    dict(slug="sainte-anne-newbell", org="Laboratoire Sainte Anne",
         city="Douala (New-Bell, 152 Av de l'Indépendance)", org_type="lab", language="FR",
         wa_number="675 39 76 65", wa_verified="unknown", contact_channel="WhatsApp",
         decision="Dr Nkanjo Francis — biologiste (nom public)", source="directory",
         source_detail="pagespratiquescm / doualazoom",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH B. New-Bell = l'un des quartiers les plus densément peuplés de Douala et des moins "
               "couverts en ligne. Argument : le patient cherche au dernier moment, sur son téléphone."),
    dict(slug="pasteur-medlas-akwa", org="Ctre d'Analyses Médicales Pasteur Medlas",
         city="Douala (Akwa, Bld de la République)", org_type="lab", language="FR", wa_number="677 45 99 97",
         wa_verified="unknown", contact_channel="WhatsApp", source="directory",
         source_detail="pagespratiquescm", stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH B. Argument : sur le même axe que trois autres laboratoires de ce pack — et celui qui a "
               "un site part avec les patients qui comparent."),
    # BATCH C — Yassa / Deido / New Bell / Bonanjo
    dict(slug="2k-labo-yassa", org="2K Labo", city="Douala (Yassa, à côté de l'institut La Perle)",
         org_type="lab", language="FR", wa_number="670 94 43 03", wa_verified="unknown",
         contact_channel="WhatsApp", source="directory",
         source_detail="mont-pandi.com — horaires publics 07:00–18:00 · 2e ligne : 694 59 10 44",
         stage="prospecting", contacted="No", reply="No", demo="Yes",
         dossier="clients/_mockups/labs/2k-labo.jpg",
         notes="⭐ MEILLEUR PROSPECT DU PACK. Maquette faite. Yassa = quartier jeune et en expansion : "
               "des familles qui arrivent, sans habitude médicale locale, qui cherchent tout sur leur téléphone. "
               "Là où la population est nouvelle, le premier trouvé gagne. Horaires 07:00–18:00."),
    dict(slug="pathcare-deido", org="Pathcare Diagnostics", city="Douala (Deido)", org_type="lab",
         language="FR/EN", wa_number="680 00 88 45", wa_verified="unknown", contact_channel="WhatsApp",
         source="directory", source_detail="goafricaonline",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH C. Nom de marque anglophone SANS AUCUNE présence en ligne au Cameroun. "
               "Argument : le nom anglais est un atout pour la clientèle anglophone de Douala — "
               "rarement servie, et une page FR|EN la sert."),
    dict(slug="biolex-deido", org="Biolex Labo", city="Douala (Deido, Rue Kotto)", org_type="lab",
         language="FR", wa_number="697 78 00 05", wa_verified="unknown", contact_channel="WhatsApp",
         source="directory", source_detail="goafricaonline",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH C. Argument : quand un patient tape « Biolex », il ne trouve rien — "
               "même pas une confirmation que le laboratoire existe."),
    dict(slug="bioscan-newbell", org="Bioscan", city="Douala (New Bell)", org_type="lab", language="FR",
         wa_number="680 06 03 94", wa_verified="unknown", contact_channel="WhatsApp",
         source="directory", source_detail="goafricaonline + PDF réseau de soins Société Générale",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH C. Figure déjà dans des réseaux de soins professionnels — donc les assureurs et les "
               "entreprises le connaissent. Ce qui manque, c'est la page que LE PATIENT trouve."),
    dict(slug="cidm-saint-joseph", org="CIDM St Joseph", city="Douala", org_type="lab", language="FR",
         wa_number="674 30 07 98", wa_verified="unknown", contact_channel="WhatsApp",
         source="directory", source_detail="goafricaonline",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="BATCH C. AUCUNE adresse publique exploitable dans les annuaires — seulement un nom et un "
               "numéro. Un numéro seul est un numéro qu'on n'appelle pas au hasard. "
               "C'est le prospect du pack pour qui une page change le plus de choses."),
]

# ── Envois RÉELS du samedi 19/09 au soir (19:21 → 19:33), relevés sur les captures de King.
#    Les coches sont la vérité : ✓✓ = lu, ✓ = distribué mais PAS lu.
#    « Envoyé » ≠ « lu » ≠ « répondu » — la règle du journal s'applique aussi ici.
ENVOIS_1909_SOIR = {
    "diagmed-bonaberi":            ("lu", "19:21", ""),
    "labtag-bali":                 ("lu", "19:23", ""),
    "sainte-anne-newbell":         ("lu", "19:24", ""),
    "pasteur-medlas-akwa":         ("lu", "19:25", ""),
    "2k-labo-yassa":               ("auto-reponse", "19:26",
                                    "Réponse AUTOMATIQUE : « Merci pour votre message. Nous ne sommes pas "
                                    "disponibles pour l'instant, mais… ». Ce n'est PAS une réponse humaine et "
                                    "ça ne compte pas dans le PRR (leçon Adonaï). Mais le numéro est vivant et "
                                    "surveillé — c'est un signal, pas une porte fermée."),
    "pathcare-deido":              ("envoye", "19:26", "UNE coche — pas encore lu."),
    "cidm-saint-joseph":           ("lu", "19:29", ""),
    "labo-meka-bonamoussadi":      ("envoye", "19:29", "UNE coche — pas encore lu. Maquette déjà prête."),
    "flemming-dream-bessengue":    ("lu", "19:30", ""),
    "interlabo-akwa":              ("envoye", "19:31", "UNE coche — pas encore lu. Maquette déjà prête."),
    "labiomed-deido":              ("lu", "19:32",
                                    "***PREMIER OUI DE LA CAMPAGNE.*** ""19:43 il repond « Oui » (11 min apres notre message). ""20:02 apercu + texte, SANS le prix (choix de King : le prix va avec un lien). ""21:00 lien labiomed.vercel.app + PRIX 100 000 FCFA 50/50 — premier message de la campagne ""avec prix ET preuve cliquable. ""21:16 il repond : « Ok je vous reviens des que je suis disponible ». ""21:22 King : « C'est note, Docteur.. Je reste a votre disposition. » (2 coches). ""21:27 il envoie un emoji 🙏. Derniere visite 21:40 — il a donc LU la reponse de King. ""ETAT : chaud, en attente, PAS de date donnee. Prochaine relance M+2 = lundi 21/09."),
    "la-passerelle-deido":         ("envoye", "19:33",
                                    "Profil SANS NOM (« +237 6 94 71 91 22 ») — King l'a signalé. Une coche. "
                                    "Cohérent avec le reste du dossier : ce labo communique par adresse yahoo "
                                    "et n'a jamais construit de présence en ligne."),
    "biodiagnostics-sable":        ("lu", "19:33", ""),
}

# Numéros essayés et NON joignables sur WhatsApp (King, 19/09 : « the others weren't available »).
# PAR ÉLIMINATION, pas par affirmation : les 5 du pack qu'il n'a pas envoyés (+ le jumeau du Dr Tagu,
# volontairement écarté). À CONFIRMER par King.
# CONFIRMÉ par King le 19/09 : « the others weren't available on whatsapp ».
PAS_SUR_WHATSAPP = {
    "niva-labo-akwa": "CONFIRMÉ 19/09 — pas sur WhatsApp",
    "aube-labo-akwa": "CONFIRMÉ 19/09 — pas sur WhatsApp",
    "hyrus-labo-deido": "CONFIRMÉ 19/09 — pas sur WhatsApp",
    "biolex-deido": "CONFIRMÉ 19/09 — pas sur WhatsApp",
    "bioscan-newbell": "CONFIRMÉ 19/09 — pas sur WhatsApp",
}


# ── DÉCISION DE KING — 19/09/2026, pendant la poussée de volume ────────────────
# « I sent to all the numbers available even those that weren't professional. »
#
# C'est un ÉCART ASSUMÉ à la règle du 18/09 (« le profil WhatsApp doit s'identifier :
# nom + catégorie »). La règle reste la bonne quand on a le temps de vérifier ; en poussée
# de volume, King a choisi d'envoyer à tout numéro joignable plutôt que de perdre le créneau.
#
# Ce que ça change, et ce que ça ne change pas :
#   · ce n'est PAS revenir sur la leçon Kingdom Family (696 023 696 = un cabinet de finances,
#     PAS une école) — cette erreur-là reste interdite, et le numéro reste écarté ;
#   · c'est accepter qu'un message puisse arriver à quelqu'un qui n'est pas le bon
#     interlocuteur, quand le pire cas est un « ce n'est pas moi » et non un message à un inconnu.
#
# Les profils ci-dessous ont été envoyés SANS nom ni catégorie vérifiés. On le note, pour que
# la prochaine personne sache pourquoi ces lignes n'ont pas de `profile_name_seen`.
PROFILS_NON_PROFESSIONNELS = {
    "la-passerelle-deido": "Profil affiché « +237 6 94 71 91 22 » — AUCUN NOM, aucune catégorie. "
                           "King a envoyé quand même (décision de volume du 19/09). "
                           "À surveiller : si la réponse semble venir d'une personne privée, ne pas insister.",
    "interlabo-akwa": "Avatar = la lettre « I », pas de logo d'entreprise. Identité non confirmée à l'écran.",
}


def _apply_envois(out: list) -> None:
    by = {r.get("slug"): r for r in out}
    # un « Oui » est une reponse HUMAINE : on la pose AVANT la boucle generique,
    # sinon le tuple de ENVOIS_1909_SOIR la remettrait a « none ».
    _oui = by.get("labiomed-deido")
    if _oui is not None:
        _oui["Reply"] = "YES 19/09 19:43 - \"Oui\" (verbatim). PREMIER OUI DE LA CAMPAGNE."
        _oui["reply_type"] = "human"
    for slug, (etat, heure, note) in ENVOIS_1909_SOIR.items():
        r = by.get(slug)
        if not r:
            print(f"  ⚠ envoi 19/09 : slug introuvable « {slug} »")
            continue
        # ⚠️ On retire les clés COURTES avant d'écrire : sinon KEYMAP, qui tourne plus loin,
        # réécrase « Contacted = Yes » avec le « contacted = No » d'origine du dictionnaire.
        # Bug attrapé le 19/09 par vérification : les 13 envois du soir n'étaient pas comptés.
        for k in ("contacted", "reply", "demo"):
            r.pop(k, None)
        r["Contacted"] = "Yes"
        r["stage"] = "qualifying"
        r["last_send_state"] = etat
        if not str(r.get("Reply", "")).strip().lower().startswith("yes"):
            r["reply_type"] = "auto" if etat == "auto-reponse" else "none"
        r["follow_ups_sent"] = "0"
        label = {"lu": "lu (2 coches)", "envoye": "distribué, NON lu (1 coche)",
                 "auto-reponse": "réponse AUTOMATIQUE"}[etat]
        r["Notes"] = (f"Envoyé le 19/09 à {heure} — {label}." + (" " + note if note else "") +
                      " | " + str(r.get("Notes") or "")).strip(" |")
    for slug, why in PROFILS_NON_PROFESSIONNELS.items():
        r = by.get(slug)
        if r is not None:
            r["Notes"] = ("⚠️ " + why + " | " + str(r.get("Notes") or "")).strip(" |")

    for slug, why in PAS_SUR_WHATSAPP.items():
        r = by.get(slug)
        if not r:
            print(f"  ⚠ non joignable : slug introuvable « {slug} »")
            continue
        for k in ("contacted", "reply", "demo"):
            r.pop(k, None)
        r["Contacted"] = "No"
        r["wa_verified"] = "no"
        r["wa_number_note"] = why
        r["stage"] = "prospecting"
        r["disqualification_reason"] = f"Canal injoignable — {why}."
        r["Notes"] = ("⛔ " + why + " | " + str(r.get("Notes") or "")).strip(" |")


# Ces deux entrées n'ont PAS été envoyées : ce sont des pièges enregistrés pour ne pas les oublier.
LABS_ECARTES = [
    ("douala-lab-akwa", "Douala Labo", "Douala (Akwa, 37 Av King Akwa)", "699 62 61 21",
     "https://www.douala-labo.com/", "A un site vivant avec espace résultats en ligne."),
    ("labo-drouot-akwa", "Laboratoire Drouot", "Douala (Akwa, 789 Rue Drouot)", "699 09 29 55",
     "https://laboratoire-drouot.com/", "A un site vivant — 20 ans d'expertise affichés."),
    ("kylaya-labo-bali", "Kylaya Labo", "Douala (Bali, 189 Rue des Manguiers)", "696 78 77 78",
     "http://www.kylayalabo.com/", "A un site vivant."),
    ("scientilabo-akwa", "Scientilabo", "Douala (Akwa, Rue Gallieni)", "696 42 34 77",
     "https://scientilabo.com/", "A un site vivant — 8 spécialités, 34 ans d'expérience."),
    ("le-bon-diagnostic-elf", "Le Bon Diagnostic", "Douala (Elf, Axe-Lourd)", "699 95 67 32",
     "https://www.lebondiagnostic.com", "Site référencé dans les annuaires."),
]


def _labs_ecartes_rows():
    out = []
    for slug, org, city, num, site, why in LABS_ECARTES:
        out.append(dict(slug=slug, org=org, city=city, language="FR", org_type="lab",
                        wa_number=num, wa_verified="no", stage="disqualified", contacted="No",
                        reply="No", demo="No", source="directory", source_detail="annuaires de Douala",
                        site_url=site, site_checked_on="2026-09-19",
                        disqualification_reason=f"A DÉJÀ UN SITE VIVANT ({site}). Hors cible — "
                                                "vérifié AVANT toute production (règle 66).",
                        notes=f"⛔ NE PAS ENVOYER. {why} Écarté le 19/09 pendant la préparation du pack LABOS. "
                              "C'est exactement le piège QUALITECH/Clinique des Anges — sauf que cette fois "
                              "la vérification est passée avant la production, pas après."))
    return out


# ── Le lead hors classeur qui vit dans un autre onglet du même fichier ──────────
ORACARE = dict(slug="oracare-buea", org="OraCare Dental Clinic (Oracare237)",
               city="Buea (Molyo)", org_type="clinic", language="EN",
               wa_number="672 52 66 86", wa_verified="yes", contact_channel="WhatsApp",
               source="content_video", source_detail="Premier lead de la campagne — vérifié par King",
               stage="qualifying", contacted="Yes", reply="No", demo="Yes",
               last_send_state="sent", follow_ups_sent="1",
               notes="Message 1 lundi 14/09. FU2 (M+4) prévue dim 20/09. Concept live : oracare-concept.vercel.app "
                     "(v3, prix + assistant). ⚠️ N'a JAMAIS répondu : message non lu attribué à tort le 18/09, corrigé.")


def norm_slug(name: str) -> str:
    import re
    import unicodedata
    s = unicodedata.normalize("NFD", str(name)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-+", "-", s)[:60]


PHONE_SEP = r"[\s.\-]?"


def cm_numbers(txt) -> list:
    """Numéros camerounais (9 chiffres) trouvés dans un texte, indicatif retiré.

    Deux bugs corrigés avant que ça marche (ils sont la raison d'être de cette docstring) :
      1. **Ne jamais coller plusieurs colonnes avant d'extraire** — « 677378542 699901234 »
         devient une seule suite de 18 chiffres et plus rien ne correspond.
      2. **Retirer l'indicatif `+237` AVANT de chercher** — sinon « +237 233 470 608 »
         matche à partir du `2` de `237` et rend « 237233470 », un numéro qui n'existe pas.
    """
    import re
    t = re.sub(r"\+?237" + PHONE_SEP, " ", str(txt or ""))
    out = []
    for m in re.findall(r"(?<!\d)([62](?:" + PHONE_SEP + r"\d){8})(?!\d)", t):
        d = re.sub(r"\D", "", m)
        if len(d) == 9 and d not in out:
            out.append(d)
    return out


# Étapes = celles du classeur lui-même (onglet « Pipeline - 5 Stages ») + `disqualified`
# (ajout demandé par l'audit §7 : 8 leads étaient rangés dans `lost` alors qu'ils n'ont
# jamais été jouables) + `parked` (dormants, ni perdus ni actifs).
# ── NE JAMAIS CONTACTER — décisions de King. Écrit ici ET dans la donnée, parce qu'une
#    consigne qui ne vit que dans une conversation se perd au premier redémarrage.
NEVER_CONTACT = {
    "solidarity": "King : NE JAMAIS contacter Solidarity (677 61 57 57). "
                  "Base : établissement à acheteur institutionnel — notre règle ne relance pas ce type d'acheteur.",
    "nj ang": "King : NE JAMAIS contacter Dr Njang (691 63 29 41).",
    "njang": "King : NE JAMAIS contacter Dr Njang (691 63 29 41).",
}

STAGES = ("prospecting", "qualifying", "demo", "offer", "delivered", "disqualified", "parked")


def stage_for(rec: dict) -> str:
    """Étape déduite des colonnes du classeur. Rien d'inventé : la règle est écrite ici."""
    c = str(rec.get("Contacted") or "").strip().lower()
    if c.startswith("yes"):
        return "qualifying"          # « Message right leads » — onglet Pipeline, étape 2
    if "scheduled" in c:
        return "parked"              # planifié puis jamais parti
    if "parked" in c:
        return "parked"
    if c in ("", "none", "no", "not contacted") or c.startswith("no"):
        return "prospecting"         # « Find & capture qualified… » — étape 1
    return ""


def wa_number_for(rec: dict) -> str:
    """Le numéro WhatsApp exploitable : un **mobile** (6XXXXXXXX).

    Un fixe (2XXXXXXXX) ne va pas sur WhatsApp — on ne le met pas dans `wa_number`
    pour ne pas fabriquer une fausse capacité. Le texte d'origine reste intact
    dans la colonne `WhatsApp` du classeur (jamais écrasé).
    """
    for col in ("WhatsApp", "Phone"):
        for n in cm_numbers(rec.get(col)):
            if n.startswith("6"):
                return n
    return ""


# ── M2 · les contradictions, vérifiées le 19/09 contre les fichiers (voir CONTRADICTIONS.md).
#    Chaque entrée écrit : ce qui se contredisait · ce qu'on retient · ce qu'on écarte.
#    Aucun verbatim n'est supprimé : la colonne d'origine du classeur reste intacte.
CONTRADICTIONS = [
    # (slug, contradiction, retenu, écarté)
    ("comobil-college-moderne-bilingue-les-laureats",
     "Le playbook §A4 code en dur une kill list « les deux 18 » (COMOBIL + OraCare) ; COMOBIL est parké depuis le 14/09. "
     "L'onglet DAILY OPS dit « PARKED 14 Sep (King decision) » — mon audit du 18/09 prétendait le contraire (infirmé).",
     "parked — une kill list doit se DÉDUIRE de l'état réel (score 18 ET non parké ET non disqualifié).",
     "la liste figée du playbook, qui met sur une liste « TODAY » un lead parké depuis cinq jours."),
    ("groupe-scolaire-moderne-bilingue-wafo",
     "Fusionné dans COMOBIL selon Pipeline-Status, mais resté une ligne séparée avec son propre score.",
     "deux lignes LIÉES par same_buyer_as — un seul acheteur (Pierre WAFO), deux établissements.",
     "supprimer une des deux lignes : une ligne supprimée est une donnée perdue, et l'audit disait les deux choses à la fois."),
    ("st-theresa-international-bilingual-comprehensive-college-sti",
     "Mon audit du 18/09 affirmait que la cellule « Lead score » de cette ligne contenait le verbatim de la réponse.",
     "la ligne est CORRECTE : Lead score = 14 (numérique), le verbatim est dans Reply. 0 anomalie sur 38 lignes.",
     "l'affirmation de l'audit — vérifiée et infirmée le 19/09. Aucun changement de donnée."),
    ("solidarity-health-foundation-solidarity-clinic-laboratory",
     "Le classeur dit « scheduled Tue » ; Pipeline-Status dit « no WhatsApp line » ; King dit : ne jamais contacter.",
     "parked, avec le motif de King écrit dans la donnée : jamais de contact, acheteur institutionnel.",
     "« scheduled Tue » — la ligne n'a jamais été jouable, et la consigne de King prime sur les deux fichiers."),
    ("one-stop-medical-laboratory-diagnostics",
     "Rangé COMME UN PROSPECT NORMAL dans le classeur (score attribué, priorité, canal).",
     "parked — King a une règle : ne jamais contacter Dr Njang (691 63 29 41).",
     "le traitement de prospect standard : personne n'aurait vu l'interdiction avant l'envoi."),
    ("nabesk-comprehensive-college",
     "Le classeur annonce « 83,5 % au O-Level 2020 ».",
     "83,46 % au A-Level 2020 — correction déjà journalisée dans Pipeline-Status le 18/09.",
     "« 83,5 % au O-Level » — un chiffre faux dans une accroche commerciale, le pire endroit pour se tromper. "
     "Verbatim conservé : la colonne Facilities du classeur n'est pas modifiée."),
    ("divine-success-comprehensive-college-dscc",
     "Numéro présent au classeur mais jamais vérifié sur WhatsApp ; il s'est révélé être « Kingdom Family Int'l » (Finance).",
     "wa_verified = no, numéro écarté, motif écrit.",
     "le numéro comme numéro d'école : c'est un cabinet de finances, pas un établissement scolaire."),
    ("baptist-high-school-bhs-awae",
     "Numéro présent au classeur, aucune identité affichée sur WhatsApp.",
     "wa_verified = no, numéro écarté.",
     "l'envoi à un numéro non identifié — la règle de King du 18/09 interdit d'écrire sans nom ni catégorie."),
]

# Contradictions structurelles : elles ne visent pas une ligne mais un fichier entier.
STRUCTURAL = [
    ("#2", "Le classeur maître ne contenait aucun des 15 leads engagés de Douala.",
     "Les 15 existent et sont engagés — ils ont maintenant une ligne.",
     "« le classeur suffit pour décrire le pipeline »."),
    ("#3", "5 dossiers clients/ sur 8 n'avaient aucune ligne dans le classeur.",
     "Ces dossiers contiennent le travail réel, donc ils doivent être liés à une ligne.",
     "l'idée que le classeur décrivait le pipeline.",
     "Réparé par M1 (les 4 + les 6 cliniques ont une ligne). M4 doit lier les fiches."),
    ("#4", "L'absence de numéro WhatsApp était écrite en prose, donc intraitable.",
     "32 lignes sur 54 ont un mobile exploitable ; 41 n'en ont pas ; 8 fixes volontairement exclus.",
     "« N/V (landline) » comme contenu de champ.",
     "Une colonne triable (wa_number) ET le texte d'origine intact dans WhatsApp."),
    ("#8", "Daily Ops.csv présenté comme un export de l'onglet DAILY OPS.",
     "C'est un PLAN DE JOURNÉE du 16/09 (12 lignes sur 43 seulement sont de la donnée de lead) — périmé.",
     "« même contenu, deux formats » : le CSV a 50 lignes, l'onglet 36. Mon audit était partiellement faux.",
     "M6 : le renommer Daily-Plan.csv et le GÉNÉRER depuis le CRM, sinon il redeviendra faux."),
    ("#9", "Trois vocabulaires d'étape concurrents ; Pipeline-Status dit 27 leads, le classeur 38, le CRM 54.",
     "Le vocabulaire de l'onglet « Pipeline - 5 Stages » du classeur + disqualified + parked (7 valeurs).",
     "les trois autres vocabulaires.",
     "Réparé par M1 : chaque ligne porte une étape de l'énumération, aucune hors énumération."),
]


# ── M4 · les dossiers de travail, liés à leur ligne.
#    Le rapprochement se fait sur le SLUG, jamais par recherche de texte : l'audit §4 prévenait
#    qu'une recherche du mot « NABESK » remonte la ligne Baird Memorial (« same road as NABESK »),
#    ce qui produirait une fausse fusion.
DOSSIERS = {
    "afrique-labo-douala": "clients/afrique-labo/",
    "jempo-deido": "clients/jempo/",
    "opticien-bali-douala": "clients/l-opticien/",
    "la-bethanie-bonaberi": "clients/la-bethanie/",
    "nabesk-comprehensive-college": "clients/nabesk/",
    "saint-bernard-high-school-sbhs": "clients/saint-bernard/",
    "summerset-bilingual-college-smbicol": "clients/summerset/",
    "camera-akwa": "clients/douala-cliniques/01-camera.jpg",
    "le-nid-bessengue": "clients/douala-cliniques/02-le-nid.jpg",
    "wonders-bonamoussadi": "clients/douala-cliniques/03-wonders.jpg",
    "adonai-douala": "clients/douala-cliniques/04-adonai.jpg",
    "qualitech-douala": "clients/douala-cliniques/05-qualitech.jpg",
    "malia-labo-douala": "clients/douala-cliniques/06-malia-labo.jpg",
    "uni-labo-bonamoussadi": "clients/douala-cliniques/07-unilabo.jpg",
    "centre-medical-de-bonanjo": "clients/_mockups/bonanjo.jpg",
    "2k-labo-yassa": "clients/_mockups/labs/2k-labo.jpg",
    "interlabo-akwa": "clients/_mockups/labs/interlabo.jpg",
    "labiomed-deido": "clients/_mockups/labs/labiomed.jpg",
    "labo-meka-bonamoussadi": "clients/_mockups/labs/meka.jpg",
}

# Dossiers qui n'appartiennent à aucun lead (gabarits de maquette, pas des prospects)
DOSSIERS_HORS_LEAD = {"_mockups"}


def check_dossiers(out: list) -> None:
    """Le vrai livrable de M4 n'est pas la table, c'est le CONTRÔLE :
    chaque dossier de `clients/` doit être référencé, et chaque référence doit exister.
    Une table se périme ; un contrôle qui refuse le silence, non."""
    linked = {r.get("dossier") for r in out if r.get("dossier")}
    base = ROOT / "clients"
    problems = []
    if base.exists():
        for d in sorted(base.iterdir()):
            if not d.is_dir() or d.name in DOSSIERS_HORS_LEAD:
                continue
            if not any((l or "").startswith(f"clients/{d.name}/") for l in linked):
                problems.append(f"dossier non référencé : clients/{d.name}/")
    for l in sorted(linked):
        if l and not (ROOT / l).exists():
            problems.append(f"référence morte : {l}")
    if problems:
        print(f"  ⚠ M4 — {len(problems)} problème(s) :")
        for x in problems:
            print("      ·", x)
    else:
        n = len([d for d in base.iterdir() if d.is_dir() and d.name not in DOSSIERS_HORS_LEAD]) if base.exists() else 0
        print(f"  M4 : {len(linked)} dossier(s)/maquette(s) liés · {n} dossier(s) de travail, tous référencés ✓")


def read_workbook():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["Leads 50"]
    headers = [c.value for c in ws[1]]
    rows = []
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, len(headers) + 1)]
        if not any(v not in (None, "") for v in vals):
            continue
        rows.append(dict(zip(headers, vals)))
    return headers, rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(ROOT / "leads" / "CRM.csv"))
    args = ap.parse_args()

    headers, wb_rows = read_workbook()
    out = []

    # 1 · les 38 lignes du classeur, colonnes à l'identique
    for r in wb_rows:
        rec = {h: r.get(h) for h in headers}
        rec["slug"] = norm_slug(r.get("School", ""))
        rec["org_type"] = "school"
        rec["wa_number"] = wa_number_for(r)
        rec["stage"] = stage_for(r)
        # wa_verified reste vide : personne n'a ouvert ces profils. On ne le devine pas.
        out.append(rec)

    # 1a · la liste « ne jamais contacter » : on la pose AVANT tout le reste
    for rec in out:
        hay = (str(rec.get("School") or "") + " " + str(rec.get("slug") or "") + " " +
               str(rec.get("Decision maker") or "")).lower()
        for key, why in NEVER_CONTACT.items():
            if key in hay:
                rec["stage"] = "parked"
                rec["disqualification_reason"] = why
                rec["Notes"] = (str(rec.get("Notes") or "") + " · 🚫 " + why).strip(" ·")
                break

    # 1b · le numéro qui NE DOIT PAS servir — la leçon du 18/09, gravée dans la donnée
    #      (King : « vérifier nom + catégorie sur WhatsApp avant d'écrire »)
    BAD = {"696023696": ("Kingdom Family Int'l", "Finance — PAS un établissement scolaire"),
           "677647802": ("", "aucune identité affichée — jamais envoyé")}
    for rec in out:
        n = rec.get("wa_number")
        if n in BAD:
            seen, why = BAD[n]
            rec["wa_verified"] = "no"
            rec["profile_name_seen"] = seen
            rec["disqualification_reason"] = f"numéro écarté à la vérification : {why}"
            rec["Notes"] = (str(rec.get("Notes") or "") +
                            f" · ⚠️ NE PAS ENVOYER sur {n} : {why}.").strip(" ·")

    # 2 · OraCare — même fichier, autre onglet
    out.append({"School": ORACARE["org"], **ORACARE})

    # 2b · les envois du 18/09 au soir (absents de l'audit du matin)
    for p in SENT_1809:
        p.setdefault("stage", "qualifying")   # un message parti = étape 2 du pipeline du classeur
        out.append({"School": p["org"], **p})

    # 2c · les numéros testés et écartés — la donnée qui évite de refaire le travail
    for p in _not_reachable_rows():
        out.append({"School": p["org"], **p})

    # 2d · les 19 laboratoires du pack du 19/09 au soir
    for p in LABS_1909:
        out.append({"School": p["org"], **p})

    # 2d-bis · les envois RÉELS du 19/09 au soir (captures de King)
    _apply_envois(out)

    # 2e · les 5 laboratoires ÉCARTÉS pour site vivant — la donnée qui évite de refaire le travail
    for p in _labs_ecartes_rows():
        out.append({"School": p["org"], **p})

    # 3 · les 15 hors classeur
    for p in PROSE_LEADS:
        out.append({"School": p["org"], **p})

    # le nom de colonne du classeur est `School` : on le garde tel quel, comme demandé
    for rec in out:
        rec.pop("org", None)

    # 4 · dédoublonnage SANS suppression : COMOBIL et GS WAFO, un seul acheteur
    wafo = [r for r in out if r.get("School") and ("COMOBIL" in str(r["School"]) or "WAFO" in str(r["School"]))]
    if len(wafo) == 2:
        a, b = wafo
        dec = str(a.get("Decision maker") or "")
        note = ("Même acheteur que la ligne liée — Pierre WAFO (promoteur). "
                "Le classeur liste les deux établissements du même groupe ; "
                "une seule conversation, un seul acheteur (audit §9 étape 2).")
        for rec in (a, b):
            rec["same_buyer_as"] = ""
        a["same_buyer_as"] = norm_slug(b.get("School", ""))
        b["same_buyer_as"] = norm_slug(a.get("School", ""))
        a["Notes"] = (str(a.get("Notes") or "") + " · " + note).strip(" ·")
        b["Notes"] = (str(b.get("Notes") or "") + " · " + note).strip(" ·")

    # 4b · M4 — lier les dossiers de travail
    for rec in out:
        d = DOSSIERS.get(rec.get("slug"))
        if d:
            rec["dossier"] = d

    # 5 · M2 — les contradictions : valeur retenue + valeur écartée, sur la ligne concernée
    by_slug = {r.get("slug"): r for r in out}
    for slug, what, kept, dropped in CONTRADICTIONS:
        rec = by_slug.get(slug)
        if not rec:
            print(f"  ⚠ contradiction M2 : slug introuvable « {slug} »")
            continue
        rec["contradiction"] = what
        rec["value_kept"] = kept
        rec["value_discarded"] = dropped
        rec["Notes"] = (str(rec.get("Notes") or "") +
                        " | CONTRADICTION RÉSOLUE (M2) — retenu : " + kept).strip(" ·")

    # Garde-fou (bug du 19/09) : une clé mal orthographiée était jetée EN SILENCE par
    # DictWriter(extrasaction="ignore") — 15 leads avaient perdu City, Language, Contacted,
    # Reply et Demo made sans qu'aucune ligne ne se plaigne. On refuse désormais de sortir.
    # ⚠️ CORRECTION DE CAUSE (4e occurrence du même bug, 19/09).
    # AVANT : `rec[full] = rec.pop(short)` écrasait SANS CONDITION ce qu'un autre traitement
    # venait d'écrire (`_apply_envois`, `_apply ...`) — les envois du 19/09 et la conversation
    # LABIOMED ont été perdus deux fois de cette façon.
    # MAINTENANT : la forme longue déjà posée GAGNE. On jette seulement le doublon court.
    # Une donnée écrite par un traitement explicite ne peut plus être effacée par une
    # simple table de correspondance.
    for rec in out:
        for short, full in KEYMAP.items():
            if short not in rec:
                continue
            if full in rec and str(rec[full]).strip():
                rec.pop(short)          # la valeur déjà posée gagne
            else:
                rec[full] = rec.pop(short)
        rec.setdefault("School", "")

    cols = headers + NEW_FIELDS
    allowed = set(cols)
    for rec in out:
        unknown = set(rec) - allowed
        if unknown:
            sys.exit(f"✗ clé(s) inconnue(s) {sorted(unknown)} — nom de colonne probablement mal "
                     f"orthographié. Rien n'a été écrit (perte de données évitée).")

    csv_path = pathlib.Path(args.csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for rec in out:
            w.writerow({c: ("" if rec.get(c) is None else rec.get(c)) for c in cols})

    print(f"✓ {csv_path} — {len(out)} lignes × {len(cols)} colonnes")
    print(f"  dont {len(wb_rows)} du classeur « Leads 50 » · 1 d'un autre onglet · {len(PROSE_LEADS)} de la prose")
    src = {}
    for rec in out:
        s = rec.get("source") or "(non renseigné)"
        src[s] = src.get(s, 0) + 1
    print("  sources :", " · ".join(f"{k}={v}" for k, v in sorted(src.items(), key=lambda x: -x[1])))
    types = {}
    for rec in out:
        t = rec.get("org_type") or "(non renseigné)"
        types[t] = types.get(t, 0) + 1
    print("  types   :", " · ".join(f"{k}={v}" for k, v in sorted(types.items(), key=lambda x: -x[1])))
    check_dossiers(out)
    n_con = sum(1 for r in out if r.get("contradiction"))
    print(f"  M2 : {n_con} ligne(s) portent une contradiction résolue ({len(CONTRADICTIONS)} + {len(STRUCTURAL)} structurelles)")
    noslug = [r for r in out if not r.get("slug")]
    if noslug:
        print(f"  ⚠ {len(noslug)} ligne(s) sans slug")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
