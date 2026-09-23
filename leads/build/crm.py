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
    dict(slug="uni-labo-bonamoussadi", org="UNI-LABO",
         city="Douala (Bonamoussadi, Carrefour Etoo)", language="FR/EN",
         org_type="lab", wa_number="696 13 98 19", wa_verified="yes",
         contact_channel="WhatsApp", source="directory",
         source_detail="Remote-Sweep section C - Lun-Ven 07h-19h, Sam 07h-13h",
         contacted="Yes", reply="YES 19/09 20:20 - demande de RENDEZ-VOUS",
         demo="Yes", last_send_state="sent", follow_ups_sent="0",
         stage="offer", reply_type="human",
         notes="DEMANDE DE RENDEZ-VOUS - LE PLUS FORT SIGNAL DE LA CAMPAGNE. "
               "Le 19/09 a 20:20, UNI-LABO a ecrit, mot pour mot : « Bsr. Peut on prendre un rendez vous "
               "pour vendredi pour que vous nous presentez vos services? » "
               "Ce n est plus « je vous reviens » : c est une INVITATION. Premier prospect de la "
               "campagne qui demande a nous voir. RENDEZ-VOUS = VENDREDI 25/09. "
               "ATTENTION : LE SITE EST DEJA CONSTRUIT ET EN LIGNE (https://uni-labo.vercel.app) - "
               "la presentation des services se fera donc sur LEUR PROPRE site, ouvert sur un telephone. "
               "C est une seance de CLOTURE, pas un premier contact. Prix a poser : 100 000 FCFA, 50/50. "
               "Ce qui rend ce lead unique : il avait ecrit « Bsr » le 18/09 a 20:57, nous avons envoye "
               "le lien a 21:47 puis 22:05, et il est revenu DE LUI-MEME 24 h plus tard. "
               "Message 1 envoye le 18/09 a 18:41 (2 coches)."),
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
    out.append(dict(slug="inses-douala", org="INSES — Institut Supérieur de l'Espoir", city="Douala (Bonabéri)",
                    language="FR/EN", org_type="school", wa_number="674 93 66 04", wa_verified="yes",
                    stage="parked", contacted="No", reply="No", demo="No",
                    Website="univ-inses.com — VIVANT et moderne (Next.js bilingue FR/EN, page /inscription), lu le 22/09",
                    source="walk_in", source_detail="affiche vue par King 18/09 — BTS · HND · Licence · Master",
                    notes="JAMAIS contacté, et le 22/09 le premier message préparé a été RETIRÉ avant envoi : King a "
                          "montré `univ-inses.com` — site Next.js bilingue (programmes, /inscription, /contact), "
                          "Douala-Bonabéri, partenaire CEMECES (Clinique Médico-chirurgicale de l'Espoir) ; fiche "
                          "WhatsApp Business « Insés » (Education · University, catalogue CQP Aide-soignant / BTS) "
                          "portant le MÊME numéro 674 93 66 04. Le message préparé disait « quand un parent cherche "
                          "INSES Douala il trouve une affiche, pas une page » : FAUX. C'est un lead du profil « a déjà "
                          "une vitrine à lui » — le meilleur profil de la campagne — pas un premier contact. Défauts "
                          "relevés sur le site, à exploiter si on y revient : /images/formations/default.jpg illustre "
                          "cinq des six filières, et « Diététique et Nutrition » apparaît deux fois avec deux durées "
                          "contradictoires (2 ans / 3 ans). PARKED : les écoles sont hors périmètre (décision King)."))
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



# ── VAGUE 1 OPTICIENS du 21/09 — source : annuaire officiel de l'ONOC (Ordre National des
#    Opticiens du Cameroun) + Maligah. 38 neufs, 0 doublon avec les 82 lignes deja contactees.
#    2 ecartes pour site vivant (Vision Care Center, Original Optique) : voir OPT_ECARTES.
OPTICIENS_2109 = [
    dict(slug="m-dina-optic", org="Médina Optic", city="Douala", org_type="other", language="FR",
         wa_number="699 93 93 34", wa_verified="unknown",
         contact_channel="WhatsApp", decision="BALLA Saïdou", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BALLA Saïdou. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="lux-optique", org="Lux Optique", city="Douala", org_type="other", language="FR",
         wa_number="655 04 05 49", wa_verified="unknown",
         contact_channel="WhatsApp", decision="BATJOM BA BOOH Michel", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BATJOM BA BOOH Michel. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="dumbu-lunetterie", org="Dumbu Lunetterie", city="Douala", org_type="other", language="FR",
         wa_number="690 11 43 23", wa_verified="unknown",
         contact_channel="WhatsApp", decision="", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="univers-optique", org="Univers Optique", city="Douala", org_type="other", language="FR",
         wa_number="699 25 28 74", wa_verified="yes",
         contact_channel="WhatsApp", decision="BAYANG BIHEN Calvin", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah + Google Maps + Wayback + kerawa (2022)",
         stage="closing", contacted="Yes", reply="Yes", demo="Yes",
         reply_type="human", last_send_state="delivered",
         site_url="", site_checked_on="2026-09-21",
         Website="univers-optique.com — HORS LIGNE (aucun enregistrement DNS, vérifié 21/09 ; dernière copie Wayback vivante 02/11/2023, répertoire Apache vide au 09/01/2024)",
         **{"Website status": "AUCUN site à moderniser : le domaine est MORT. Le cabinet existe en ligne "
            "ailleurs — fiche Google (3,3/5 · 6 avis · champ site VIDÉ · aucun réseau relié), annuaire "
            "Maligah à champs vides, annonce kerawa retirée. C'EST UNE REPRISE, PAS UNE REFONTE. "
            "Dernière page vivante = WordPress avec le nom d'un autre opticien (« Gweleo ») dans le texte, "
            "3 cartes pointant vers la même URL, et une bannière « 15 % » sans offre derrière."},
         **{"Follow-up date": "2026-09-22", "Conversation": "Message 1 lun 21/09 17:50 (variante C) · "
            "17:56 il répond « Combien ça me coûte » (2e question de prix de la campagne) · 18:08 King : "
            "100 000 FCFA la page complète FR|EN, mise en ligne 3 à 5 jours, 50 000 pour commencer + 50 000 "
            "à la mise en ligne, rien dû avant accord, aperçu gratuit promis « d'ici demain » · AUCUN prix "
            "n'est écrit sur la maquette, et aucun ne sera publié sur SA page sans son accord."},
         **{"Last FB post": "aucune page Facebook rattachable à ce nom trouvée (21/09) — la page « Univers Optique · 508 likes · Global trade invesment » est un HOMONYME, métier différent : NE PAS REVENDIQUER, NE PAS LIER."},
         **{"FB followers": "—"},
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BAYANG BIHEN Calvin (raison sociale annuaire : ETS UNIVERS OPTIQUE). "
               "Deuxième ligne 674 59 93 02 ; fixe publié en DEUX VERSIONS contradictoires par SES propres supports "
               "(« +237 33 18 33 08 » / « 243 18 33 08 ») → posé comme QUESTION sur la page, jamais tranché par nous. "
               "Adresse Google : rue de Bépanda omnisports, plus code 3P3G+JCG, entre pharmacie Sass et Express Union, BP 4680. "
               "Créé le 01/08/2009 (annonce kerawa, support retiré). E-mails publics : universoptique@yahoo.fr + universoptique.uo@gmail.com. "
               "Raretés réelles à vendre : PROTHÈSES OCULAIRES, verres de sécurité en atelier, FORMATIONS. "
               "Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="lyfyoptic", org="LyfyOptic", city="Douala", org_type="other", language="FR",
         wa_number="699 98 06 66", wa_verified="unknown",
         contact_channel="WhatsApp", decision="BELL MBENOUN Dominique", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BELL MBENOUN Dominique. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="espace-vision", org="Espace Vision", city="Douala", org_type="other", language="FR",
         wa_number="677 33 94 24", wa_verified="unknown",
         contact_channel="WhatsApp", decision="BIYOUMA Théodore", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BIYOUMA Théodore. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="espace-lunetterie", org="Espace Lunetterie", city="Douala", org_type="other", language="FR",
         wa_number="677 34 24 62", wa_verified="unknown",
         contact_channel="WhatsApp", decision="BOUDJEU TCHAKOUNTE Edwige", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BOUDJEU TCHAKOUNTE Edwige. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="faby-optique", org="Faby Optique", city="Douala", org_type="other", language="FR",
         wa_number="692 08 00 55", wa_verified="unknown",
         contact_channel="WhatsApp", decision="BOUDZAP ZOYEM Hermine", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : BOUDZAP ZOYEM Hermine. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="horizon-optique", org="Horizon Optique", city="Douala", org_type="other", language="FR",
         wa_number="677 44 74 17", wa_verified="unknown",
         contact_channel="WhatsApp", decision="DJEUMO FEUNOU Siméon", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : DJEUMO FEUNOU Siméon. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="cavisa-optique", org="Cavisa Optique", city="Douala", org_type="other", language="FR",
         wa_number="699 95 90 52", wa_verified="unknown",
         contact_channel="WhatsApp", decision="DONGMO Jean René", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : DONGMO Jean René. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="l-opticien-sarl", org="L'Opticien SARL", city="Douala", org_type="other", language="FR",
         wa_number="694 33 65 82", wa_verified="unknown",
         contact_channel="WhatsApp", decision="DOUALLA Karen Sophie", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : DOUALLA Karen Sophie. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="class-optic", org="Class-Optic", city="Douala", org_type="other", language="FR",
         wa_number="691 17 18 17", wa_verified="unknown",
         contact_channel="WhatsApp", decision="KAMGANG NGOUNOU Jean Roméo", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : KAMGANG NGOUNOU Jean Roméo. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="4m-optique-akwa", org="4M Optique Akwa", city="Douala", org_type="other", language="FR",
         wa_number="679 27 06 64", wa_verified="unknown",
         contact_channel="WhatsApp", decision="KAPTUE TAFFO Virginie", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : KAPTUE TAFFO Virginie. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="gr-ce-vision", org="Grâce Vision", city="Douala", org_type="other", language="FR",
         wa_number="691 39 28 78", wa_verified="unknown",
         contact_channel="WhatsApp", decision="", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="gilles-andr-vision", org="Gilles-André Vision", city="Douala", org_type="other", language="FR",
         wa_number="699 88 31 78", wa_verified="unknown",
         contact_channel="WhatsApp", decision="KONTCHOU FOUENGO Justine Flore", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : KONTCHOU FOUENGO Justine Flore. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="jiredoptic-med", org="JiredOptic Med", city="Douala", org_type="other", language="FR",
         wa_number="696 26 50 31", wa_verified="unknown",
         contact_channel="WhatsApp", decision="LIPOTH Pierrette", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : LIPOTH Pierrette. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="plan-te-optique", org="Planète Optique", city="Douala", org_type="other", language="FR",
         wa_number="699 85 58 35", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MAKONGO Jean Dury", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MAKONGO Jean Dury. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="maff-optique", org="Maff Optique", city="Douala", org_type="other", language="FR",
         wa_number="699 93 19 56", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MANFO Hélène", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MANFO Hélène. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="le-cristallin", org="Le Cristallin", city="Douala", org_type="other", language="FR",
         wa_number="699 90 55 77", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MESSOUE LONTE Serge Nazaire", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MESSOUE LONTE Serge Nazaire. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="doyoan-optic", org="Doyoan Optic", city="Douala", org_type="other", language="FR",
         wa_number="653 85 27 49", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MEZAFO Gildas", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MEZAFO Gildas. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="london-vision", org="London Vision", city="Douala", org_type="other", language="FR",
         wa_number="696 76 81 16", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MINANKO Pascal", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MINANKO Pascal. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="africa-optic", org="Africa Optic", city="Douala", org_type="other", language="FR",
         wa_number="691 28 02 37", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MINTEU NZONGA Eric Aimé", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MINTEU NZONGA Eric Aimé. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="cristalys-optic", org="Cristalys Optic", city="Douala", org_type="other", language="FR",
         wa_number="690 94 51 50", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MPEGNA Pascal Bertrand", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MPEGNA Pascal Bertrand. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="megaoptic", org="MegaOptic", city="Douala", org_type="other", language="FR",
         wa_number="698 82 10 27", wa_verified="unknown",
         contact_channel="WhatsApp", decision="MVENG ATEBA Zénon", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : MVENG ATEBA Zénon. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="disc-optique-m-dicale", org="Disc Optique Médicale", city="Douala", org_type="other", language="FR",
         wa_number="677 53 35 68", wa_verified="unknown",
         contact_channel="WhatsApp", decision="NANKAP TCHIPTCHOUA Jean Calvin", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : NANKAP TCHIPTCHOUA Jean Calvin. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="bely-optique-m-dicale", org="Bely Optique Médicale", city="Douala", org_type="other", language="FR",
         wa_number="696 85 52 42", wa_verified="unknown",
         contact_channel="WhatsApp", decision="NGATCHA ZOE Rosalie", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : NGATCHA ZOE Rosalie. (2e : 651 61 32 17 — consultation oculaire) Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="isalyd-corporation", org="Isalyd Corporation", city="Douala", org_type="other", language="FR",
         wa_number="694 85 87 46", wa_verified="unknown",
         contact_channel="WhatsApp", decision="NGANKEU Christelle", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : NGANKEU Christelle. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="gift-optical", org="Gift Optical", city="Douala", org_type="other", language="FR",
         wa_number="673 52 17 35", wa_verified="unknown",
         contact_channel="WhatsApp", decision="NGUIFFEU TETNE NGASTING Aristide", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : NGUIFFEU TETNE NGASTING Aristide. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="optic-laser-m-dical", org="Optic Laser Médical", city="Douala", org_type="other", language="FR",
         wa_number="677 82 74 34", wa_verified="unknown",
         contact_channel="WhatsApp", decision="NJUMSSA François", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : NJUMSSA François. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="mel-s-optic", org="Mel's Optic", city="Douala", org_type="other", language="FR",
         wa_number="690 98 85 18", wa_verified="unknown",
         contact_channel="WhatsApp", decision="NTOLO Marie Luise", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : NTOLO Marie Luise. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="fashion-vision", org="Fashion Vision", city="Douala", org_type="other", language="FR",
         wa_number="656 22 38 63", wa_verified="unknown",
         contact_channel="WhatsApp", decision="PUILLE Nicolas", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : PUILLE Nicolas. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="omb-optique", org="OMB Optique", city="Douala", org_type="other", language="FR",
         wa_number="699 77 02 34", wa_verified="unknown",
         contact_channel="WhatsApp", decision="SAMEYO Elie", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : SAMEYO Elie. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="caprice-optique", org="Caprice Optique", city="Douala", org_type="other", language="FR",
         wa_number="675 06 16 23", wa_verified="unknown",
         contact_channel="WhatsApp", decision="SEGUE Benezer", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : SEGUE Benezer. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="le-samaritain-optique", org="Le Samaritain Optique", city="Douala", org_type="other", language="FR",
         wa_number="670 19 74 51", wa_verified="unknown",
         contact_channel="WhatsApp", decision="TASING KAYEH Isaac", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : TASING KAYEH Isaac. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="opticplus", org="OpticPlus", city="Douala", org_type="other", language="FR",
         wa_number="699 37 91 50", wa_verified="unknown",
         contact_channel="WhatsApp", decision="TATSAEDONG Alain Michel", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : TATSAEDONG Alain Michel. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="express-optic", org="Express Optic", city="Douala", org_type="other", language="FR",
         wa_number="675 77 61 25", wa_verified="unknown",
         contact_channel="WhatsApp", decision="TAVEA Frédéric Marie", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : TAVEA Frédéric Marie. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="mouscou-optique-m-dicale", org="Mouscou Optique Médicale", city="Douala", org_type="other", language="FR",
         wa_number="696 65 41 64", wa_verified="unknown",
         contact_channel="WhatsApp", decision="TATSINKOU NGUTE Justin", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : TATSINKOU NGUTE Justin. Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
    dict(slug="tchaya-optique", org="Tchaya Optique", city="Douala", org_type="other", language="FR",
         wa_number="696 79 01 73", wa_verified="unknown",
         contact_channel="WhatsApp", decision="TCHAYA PITCHA'A Yannick — depuis 1974", source="directory",
         source_detail="Annuaire officiel ONOC + Maligah",
         stage="prospecting", contacted="No", reply="No", demo="No",
         notes="VAGUE 1 OPTICIENS (21/09). Titulaire public : TCHAYA PITCHA'A Yannick — depuis 1974. (2e : 699 98 87 24) Probleme : etre dans la listanuaire de l'Ordre (150+ noms) n'est pas etre trouve, et un patient ne peut voir aucune monture avant de venir."),
]

OPT_ECARTES = [
    ("vision-care-center", "Vision Care Center", "Douala (Akwa, rue Ernest Betote)", "698 55 80 34",
     "https://visioncarecentreoptique.com/", "A un site vivant."),
    ("original-optique-douala", "Original Optique", "Douala (Carrefour Dika)", "659 09 71 50",
     "https://originaloptique-douala.com/", "A un site vivant."),
]

def _opt_rows():
    out = []
    for slug, org, city, num, site, why in OPT_ECARTES:
        out.append(dict(slug=slug, org=org, city=city, language="FR", org_type="other",
                        wa_number=num, wa_verified="no", stage="disqualified", contacted="No",
                        reply="No", demo="No", source="directory", source_detail="Annuaire ONOC",
                        site_url=site, site_checked_on="2026-09-21",
                        disqualification_reason=f"A DEJA UN SITE VIVANT ({site}). Hors cible - verifie AVANT toute production.",
                        notes=f"NE PAS ENVOYER. {why} Ecarte le 21/09 pendant la preparation de la vague opticiens."))
    return out

# ── Le lead hors classeur qui vit dans un autre onglet du même fichier ──────────
ORACARE = dict(slug="oracare-buea", org="OraCare Dental Clinic (Oracare237)",
               city="Buea (Molyo)", org_type="clinic", language="EN",
               wa_number="672 52 66 86", wa_verified="yes", contact_channel="WhatsApp",
               source="content_video", source_detail="Premier lead de la campagne — vérifié par King",
               stage="parked", contacted="Yes", reply="No", demo="Yes",
               last_send_state="sent", follow_ups_sent="1",
               notes="Message 1 lundi 14/09. Concept live : oracare-concept.vercel.app (v3, prix + assistant). "
                     "⚠️ N'a JAMAIS répondu : message non lu attribué à tort le 18/09, corrigé. 21/09 17:43 — "
                     "message de CLÔTURE envoyé (« last note from me, then I stop ») : le lead est PARKED, et "
                     "cette phrase est classée « à ne plus jamais écrire » (Enregistrements-2026-09-21-SOIR.md). "
                     "22/09 — un brouillon de relance a été refusé par King : il appelait le dentiste « Dr Njie » "
                     "alors que son nom est ARNOLD NKAFU (fichiers du 14/09), et il reprochait son silence un jour "
                     "après avoir promis de se taire. UN SEUL message reste permis, lundi 28/09 : léger, sans "
                     "reproche, justifié par du NEUF (les prix et la prise de RDV 24/7 sont sur la page).")


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
    ("le-cristallin",
     "Ma note d'annuaire (21/09) affirmait « Aucun site trouvé » et j'ai écrit le message 1 dessus. Son "
     "propre flyer, lu plus tard, portait l'adresse du cabinet.",
     "lecristallinoptique.com est EN LIGNE et a été lu EN ENTIER le 21/09 (roi : « Le cristallin a déjà un "
     "site »), et IL A AUSSI UNE PAGE FACEBOOK — dite par lui dans sa note vocale de 18:01, absente de ma "
     "fiche : je n'avais pas cherché là où il me pointait.",
     "l'argument « introuvable » retiré de la ligne ; le lead passe en REFONTE + création/reprise de page FB "
     "(sa demande, 18:01) ; les claims non contrôlés sont rétrogradés en QUESTIONS posées sur la page : les "
     "12 assureurs (jamais vus sur la page d'accueil) et « 24 ans d'expérience »."),
    ("univers-optique",
     "Mon message 1 du 21/09 17:50 affirmait « absent du web » et « deux recherches ne suffisent pas à le trouver ». "
     "La fouille du même soir prouve le contraire : fiche Google notée (3,3/5 · 6 avis), domaine enregistré (mort), "
     "fiche annuaire à son nom légal, annonce datée de 2009 encore indexée.",
     "le constat exact, plus fort et vérifiable : « votre seule page vivante est celle d'un autre » — son site ne "
     "répond plus depuis janvier 2024, et le champ « site web » de sa fiche Google est vide.",
     "l'angle « introuvable », déjà retiré chez Le Cristallin pour la même raison. Une affirmation sur la présence "
     "en ligne d'un prospect doit venir d'une source LUE, datée — pas d'une impression de recherche."),
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
    "le-cristallin": "clients/le-cristallin/",
    "univers-optique": "clients/univers-optique/",
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


# ══════════════════════════════════════════════════════════════════════════
# ÉTAT DES FILS CHAUDS — 21/09 au soir
# ══════════════════════════════════════════════════════════════════════════
# **Pourquoi ce bloc existe.** À 22:55, `bash leads/build/rebuild.sh` a EFFACÉ l'état de Le Cristallin
# (`closing`, la page FB à 515, la date de relance, le verbatim de la vocale) : ces valeurs avaient été
# écrites DANS `leads/CRM.csv` sans être écrites dans `leads/build/crm.py`. Le CSV est une SORTIE : tout
# ce qu'on y tape à la main meurt au prochain passage, et meurt SILENCIEUSEMENT. Cinquième occurrence du
# même piège dans ce dépôt (après `Daily Ops.csv`, KEYMAP, les deux graphies, le lien Vercel).
# Loi gravée ici : **un fait d'échange — qui a répondu, quoi, à quelle heure, avec quelle URL lue — n'a
# pas le droit de vivre ailleurs que dans un générateur.**
#
# **Ce qu'on y met** : uniquement ce qui ne se déduit pas (verbatims, horodatages, URL lues, chiffre lu
# avec sa date, promesse faite au client). **Ce qu'on n'y met pas** : kill list, health, dernier message
# envoyé, résumé des notes, existence d'un aperçu — tout ça se DÉDUIT (`demo` + `dossier`).
#
# **Trois garde-fous machine, et ils ont mordu tout de suite (c'est leur preuve)** : un slug inconnu fait
# échouer le build ; une clé qui n'est pas une colonne canonique fait échouer le build ; l'application
# arrive APRÈS toutes les fusions, donc rien ne peut écraser un fait d'échange. `bamfam_*`, `Last FB post`,
# `FB followers`, `preview_sent` et `first_touched` ne sont PAS des colonnes : y fourrer un fait, c'est
# l'écrire à l'encre effaçable. Le fait va dans `Notes`, `Conversation` ou `Reply`.
EVENING_2109 = {
    "le-cristallin": {
        "stage": "closing",
        "Contacted": "Yes",
        "Reply": "YES lun 21/09 17:53 « Ok » (2 min) puis 18:01 note VOCALE : il a un site ET une page "
                 "Facebook, et il DEMANDE si on veut bien lui en créer une autre = signal d'achat.",
        "Conversation": "VERBATIM de la vocale (retranscrit par King, 21/09 19:40) : « bonsoir j'ai un site "
                        "web et une addresse Facebook , bon je ne sais pas si vous avez consulter mon site web "
                        "ou quoi vous voulez seulement cree une autre ». Il a aussi ENVOYÉ l'URL de sa page : "
                        "https://www.facebook.com/lecristallinoptique/ (lien de partage, 18:01). "
                        "18:06 : « last seen today at 18:06 » — il est sur WhatsApp plusieurs fois par jour, la "
                        "fenêtre de réponse est réelle, pas théorique.",
        "reply_type": "human",
        "last_send_state": "read",
        "Demo made": "Yes",
        "Facebook": "https://www.facebook.com/lecristallinoptique/",
        "Website status": "VIVANT et consultable le 21/09 (lu EN ENTIER) — mais sans WhatsApp ni prise de "
                          "rendez-vous, carrousels dupliqués ×3, horaires contredits par son propre flyer. "
                          "C'EST UNE REFONTE, PAS UNE CRÉATION.",
        "Decision maker": "MESSOUE LONTE Serge Nazaire — ASCOMA écrit « MESSOUA » : DEUX graphies connues, à "
                          "caler sur sa pièce d'identité, jamais tranchées par nous",
        "Follow-up date": "2026-09-23",
        "Notes_extra": "FB : 515 likes · 44 en parlent · 98 y étaient (lus le 21/09 dans des annuaires "
                       "publics, affichés sans enjoliver sur la maquette) · avis Google : 3 avis, note 3,0. "
                       "ENVOI : envoyer LE FICHIER `demos/concept-le-cristallin-v1.html` (592 Ko, ≤ budget "
                       "WhatsApp 1 100 Ko), PAS un lien — `amk-cm.vercel.app/cristallin/` répond 404 tant que "
                       "rien n'est déployé. BLOQUÉ par UNE réponse de King : est-ce qu'AMK reprend la page "
                       "Facebook du cabinet, et à 50 000 FCFA ? Réponse « A » (page seule) ou « B » (page + FB) "
                       "→ le message part. Feuille prête : `sales/Send-LE-CRISTALLIN-2026-09-21-Soir.md` "
                       "(A sans prix / B : refonte 100 000 FCFA + reprise page FB 50 000 FCFA, 50/50, rien dû "
                       "avant accord). S'il marchande : on ajuste le PÉRIMÈTRE, on ne baisse jamais les "
                       "100 000 FCFA. ADRESSE CLOSE à trois sources (site + flyer + annuaire ASCOMA) : Akwa, "
                       "boulevard de la République, carrefour TIF, face ancien COMECI · 242 65 12 65 / "
                       "699 90 55 77 / 679 63 20 12 · contact@lecristallinoptique.com. MON « Bonapriso / CTFIC "
                       "Mballa 2 » d'hier soir ne figurait dans AUCUNE des trois : retiré. La maquette ne "
                       "corrige plus, elle DEMANDE s'il existe un second local.",
    },
    "univers-optique": {
        "stage": "closing",
        "Contacted": "Yes",
        "Reply": "Yes — lun 21/09 17:56 : « Combien ça me coûte » (2ᵉ question de prix de la campagne).",
        "Conversation": "17:50 message 1 (variante C) · 17:56 IL DEMANDE LE PRIX · 18:08 King répond : "
                        "100 000 FCFA la page complète FR|EN en 3-5 jours, 50 000 pour commencer + 50 000 à la "
                        "mise en ligne, rien dû avant accord, APERÇU GRATUIT PROMIS « d'ici demain » → la "
                        "promesse fait de l'envoi la PREMIÈRE tâche de la soirée, avant toute autre réponse.",
        "reply_type": "human",
        "last_send_state": "delivered",
        "Demo made": "Yes",
        "Follow-up date": "2026-09-22",
        "Notes_extra": "ENVOI DÛ : **la V2** `demos/concept-univers-optique-v2.html` (718 Ko / 734 727 octets, sha256 ca52d3c5f6ccb7ec…) — la v1 `concept-univers-optique-v1.html` (740 056 octets, sha256 719f8b60283184b6…) est gardée pour la comparaison des deux directions et NE part plus ; aperçu promis « d'ici "
                       "demain ») AVANT 09:00 mardi 22/09, et en repartant du fichier DU 22/09 : la version du 21 au soir "
                       "ne peignait son contenu que si le JavaScript s'exécutait (défaut trouvé par King, corrigé "
                       "à la source ; loi consignée design/LESSONS.md du 22/09). Repli si WhatsApp refuse la "
                       "pièce jointe : la "
                       "version sobre sans visuels, JAMAIS un lien non déployé. Feuille : "
                       "`sales/Send-UNIVERS-OPTIQUE-2026-09-22-Matin.md` (la Soir reste archive : elle décrit la v1). Ne PAS répéter « absent du web » "
                       "(faux — voir la contradiction M2 de cette ligne) ; la page pose SIX questions qu'il "
                       "doit trancher avant publication (fixe publié en deux versions, offre « 15 % », ordre "
                       "des trois lignes, nom du titulaire, e-mail unique, accès à sa fiche Google). "
                       "AUCUNE page Facebook rattachable à ce nom (21/09) : celle de 508 likes est un homonyme "
                       "(« Global trade invesment ») — ni revendiquée ni liée. Récupérer l'ACCÈS à sa fiche "
                       "Google PRIME sur la mise en ligne : c'est son premier visiteur, et le champ « site "
                       "web » y est vide.",
    },
}


# ── JOUR 22/09 · le fil LE CRISTALLIN, relevé sur les captures de King (15:30) et la page en ligne.
#    Pourquoi le stage REDESCEND de « closing » à « demo » : « closing » veut dire prix posé, en
#    négociation. Le prix n'a jamais été posé avec lui — la proposition A/B (100 000 / +50 000 Facebook)
#    a été rédigée ICI le 21/09 au soir et n'a JAMAIS été envoyée. Ce qui est vrai, c'est qu'un aperçu
#    est en ligne et qu'il le travaille avec nous : « demo ». Faire semblant d'être plus avancé que le
#    client ne rapporte rien et coûte la seule chose qui vaut : la vérité du tableau.
JOUR_2209 = {
    "le-cristallin": {
        "stage": "demo",
        "stage_since": "2026-09-22",
        "Follow-up date": "2026-09-23",
        "Contacted": "Yes",
        "Demo made": "Yes",
        "last_send_state": "delivered",
        "site_checked_on": "2026-09-22",
        "Website": "lecristallinoptique.com",
        "Reply": "OUI, et le fil est NOURRI par lui : 22/09 13:50 « Bonjour pour les assurances » + six "
                 "noms, 13:55 vocale de 31 s. Il rectifie nos orthographes (ROYAL ONYX, EXCA), il réclame "
                 "des ajouts (lunettes de sécurité OFFSHORE/ONSHORE, solaires, natation), il compte avec "
                 "nous. Ce n'est plus un « je vous reviens » : il édite sa propre page par messages.",
        "reply_type": "human",
        "Contact channel": "WhatsApp",
        "Conversation_extra":
            "21/09 20:10 le concept est envoyé (lien Vercel) · 20:33 « Ok » puis 20:49 VOCAL 1:00 · "
            "21:13 « J'ai pas bien compris où est l'assistant pour faire des modifications » — IL CROIT "
            "QUE L'ASSISTANT EST UN OUTIL OÙ LUI MODIFIE LA PAGE · 21:13 « Pour les sociétés : CAMRAIL, "
            "SOCAPALM, SAFACAM, P.A.D. » · 21:13 douze assurances (G.M.C. ASCOMA CAMEROUN, CHANAS S.A., "
            "SANHLAM, PASS24, A.G.C., ZENITHE, WILLIS TOWERS WATSON, G.G.A., EXCCA, ROYAL ONYX, ACTIVA, "
            "OLEA) · 21:13 trois de plus (SAAR, ALPHA, L.D.A.) · 21:13 « 32 Ans d'expérience. » · "
            "21:26 « Il faut mettre LUNETTES DE SÉCURITÉ ET DE PROTECTION OFFSHORE/ ONSHORE » · 21:29 "
            "« Lunettes solaires », « Lunettes de Natation » · 21:34 son deuxième numéro : 679632012 · "
            "21:35 carte de contact « B B Joe Mtn » · 21:47 King : deux numéros intégrés (679 63 20 12 et "
            "681 49 45 89) clicables vers WhatsApp, 699 90 55 77 garde la priorité RDV · 21:50 « On va "
            "continuer Demain » · 22/09 13:50 six assurances de plus (SUNU, A.F.G, ROYAL ONYX rectif, "
            "EXCA rectif, LES MUTUELLES RÉUNIES S.A., SAMARITAN) · 14:43 King « je vais les ajouter » · "
            "15:08 King : wall de logos + demande des logos officiels, photos et vidéos. Le prix, l'hébergement et la demande des accès LWS ne se posent QU'À LA FIN, quand il dira « on publie » : pendant l'aperçu, toute modification demandée est faite sans facture et sans compter. Ne jamais écrire « c'est fini » ni « à valider sous 48 h » — une urgence que nous n'avons pas créée se facture mal.",
        "Notes_extra":
            "PAGE EN LIGNE (relue 22/09, ?v=7) : https://lecristallin-concept.vercel.app/?v=7 — bandeau "
            "« Aperçu de site par AMK — pas encore le site officiel » et widget « Réponses du site · "
            "réservation vers WhatsApp · DÉMO » : ces deux mentions tombent à la publication. QUATRE "
            "CORRECTIONS À FAIRE, toutes vérifiables : (1) le mur des assurances compte « 17 » en "
            "double-countant G.M.C. et Ascoma Cameroun (UNE seule société dans son message) et en "
            "omettant SAAR, ALPHA et L.D.A. — le compte réel de ce qu'il a donné est 19 distinctes "
            "(15 hier + 4 aujourd'hui, dont deux rectifications d'orthographe) ; (2) le bloc « Grandes "
            "entreprises & sociétés / 32 ans d'expérience » est imprimé DEUX FOIS, le second sans les "
            "quatre badges ; (3) HORAIRES : la page publie « Lun-Ven 8h30–18h30 · Sam 8h30–13h30 » alors "
            "que SON FLYER (envoyé 21/09 18:02) dit 09h30–19h30 et 09h30–13h30 — une heure d'écart sur "
            "toute la journée, à lui confirmer avant la publication, c'est le champ le plus consulté "
            "d'un site d'opticien ; (4) « depuis 2010 » (16 ans) cohabite avec « 32 ans d'expérience » "
            "et avec le « 24 ans » de son site actuel — trois chiffres, une phrase à écrire avec lui. "
            "LOGOS : il n'est PAS besoin de les attendre, son site actuel les sert déjà — "
            "http://lecristallinoptique.com/img/clients/c9.jpg (SAAR), c3.jpg (GRAS SAVOYE), c4.jpg "
            "(ALPHA), c5.jpg (SAHAM), c1.jpg (MUTUELLES DES BRASSERIES), c8.jpg (BENEFICIAL GENERAL), "
            "c11.jpg (ZENITHE), c12.jpg (SAMARITAN), c13.jpg + c7.jpg (ACTIVA — doublon chez lui aussi), "
            "c14.png (ASCOMA), c6.png (CHANAS). Quatre de ces noms n'ont jamais été cités dans la "
            "conversation (SAHAM, GRAS SAVOYE, MUTUELLES DES BRASSERIES, BENEFICIAL GENERAL) : à lui "
            "demander s'il les revendique encore, sinon le mur affiche des partenaires qu'il n'a pas "
            "validés. ASSOCIATION ATTENDUE : il a demandé où était l'assistant pour modifier la page — "
            "ce n'est pas un éditeur (il répond aux visiteurs à partir des infos du cabinet) ; s'il veut "
            "s'éditer lui-même, c'est un chantier à part, donc un prix à part. PAIEMENT : jamais abordé "
            "avec lui (rappel : la proposition A/B n'a pas été envoyée). HÉBERGEMENT + DOMAINE : rien "
            "d'acheté, rien à facturer — domaine payé jusqu'au 13/06/2027 (LWS, IANA 1630), hébergement "
            "LWS déjà en place (ns1/ns2.lws-hosting.net), donc la route sûre est de POSER le fichier sur "
            "SON hébergement sans toucher au DNS : son adresse contact@lecristallinoptique.com vit sur ce "
            "domaine et une bascule de nameservers l'emporterait. Ce qui se facture : la construction et "
            "la mise en ligne (forfeit annoncé 100 000 FCFA, 50/50), l'option page Facebook (+50 000), "
            "et une ligne de maintenance s'il en veut — le seul récurrent honnête, l'infra restant chez "
            "lui.",
        "Website status":
            "VIVANT et consultable (relu EN ENTIER le 22/09) : domaine enregistré le 13/06/2018, expire le "
            "13/06/2027, registrar LWS (Ligne Web Services, IANA 1630), nameservers ns1/ns2.lws-hosting.net "
            "+ ns3/ns4.lwsdns.com → mutualisé LWS, gestionnaire de fichiers/FTP disponibles, donc le "
            "nouveau fichier s'y remplace sans rien acheter. Défauts relevés sur SA page actuelle : toutes "
            "ses images sont appelées en http:// absolu (mixed content bloqué dès qu'une page est servie en "
            "https), le mur « Ils nous font confiance » est répété trois fois dans le même carrousel, "
            "ACTIVAASSURANCES y figure deux fois, et le texte est collé sans espaces (« bonsde prise en "
            "charge », « porte feuille », « ou quoi »). C'EST UNE REFONTE, PAS UNE CRÉATION.",
    },
    "univers-optique": {
        "last_send_state": "sent",
        # 22/09 20:51 — IL A RÉPONDU, et il demande la réunion. Ce n'est plus une relance à
        # calculer : l'échéance devient le jour du rendez-vous (vendredi 25/09, 10 h, son cabinet).
        "Follow-up date": "2026-09-25",
        "site_url": "https://univers-optique-concept.vercel.app",
        "Conversation_extra":
            "22/09 14:35 — le message d'aperçu est PARTI, avec la carte du lien `univers-optique-concept"
            ".vercel.app` : « Bonjour Monsieur Bayang. Comme promis, voici l'aperçu, fait pour Univers "
            "Optique », les deux parties annoncées (la page des patients : examen, montage, réparation, "
            "prothèses, horaires, Bépanda, RDV WhatsApp, FR+EN ; et la « Note au cabinet — à ne pas "
            "publier » : le diagnostic, les six avis Google 3,3/5, ce que le web dit aujourd'hui, le nom "
            "ambigu, l'ancien site hors ligne, la fiche pro à moitié remplie), et la promesse que cette "
            "seconde partie disparaît à la publication. UNE SEULE coche à 15:53 : distribué pas encore lu. "
            "Le prix n'a PAS été répété : il est posé depuis le 21/09 18:08 (100 000 FCFA, 50/50, rien dû "
            "avant accord), et l'aperçu gratuit avait été promis la veille. "
            "22/09 20:51 — IL RÉPOND, mot pour mot : « Je suis vraiment intéressé, il faudrait qu'on se "
            "voie pour discuter. Vendredi matin 10h dans mon cabinet. Bonne nuit ». C'est le DEUXIÈME "
            "prospect de la campagne à demander une réunion de lui-même (après UNI-LABO), et le premier "
            "à fixer une HEURE sans qu'on la demande. L'aperçu a donc été lu et jugé : la question n'est "
            "plus « est-ce que ça vous parle », c'est « combien, quand, et avec quoi ».",
        "Notes_extra":
            "RENDEZ-VOUS VENDREDI 25/09 À 10 h, DANS SON CABINET (rue de Bépanda omnisports, entre "
            "pharmacie Sass et Express Union) — fixé par lui, à son heure. Feuille de préparation : "
            "`sales/RDV-UNIVERS-OPTIQUE-2026-09-25.md`. Ce qu'il faut sortir de la salle, dans l'ordre : "
            "① le « oui » (il a déjà dit « vraiment intéressé » — la réunion sert à lever les six points "
            "à trancher, pas à re-vendre) ; ② les RÉPONSES aux six points que la page lui pose "
            "elle-même (préfixe du fixe, bannière 15 %, ordre de ses trois lignes, nom du titulaire, "
            "l'e-mail qu'il lit vraiment, accès à sa fiche Google) — ce sont deux minutes chacun et "
            "c'est ce qui rend la page publiable ; ③ l'acompte 50 000 FCFA (MoMo, manuel). "
            "Le prix est DÉJÀ posé depuis le 21/09 (100 000 FCFA la page FR|EN, 50/50, rien dû avant "
            "accord) : on ne le re-présente pas et on ne le baisse pas. "
            "LA PAGE PUBLIÉE CONTIENT LA NOTE AU CABINET, en bas, étiquetée « à ne pas publier » — choix "
            "assumé par King pour la discussion, différent du découpage en deux fichiers préparé ici. Les "
            "deux tiennent : si le client demande à ne voir que la page patient, on envoie "
            "`demos/univers-optique-site-v2.html` (718 514 o, sha `ec91063b…`, note retirée par "
            "construction — un contrôle refuse le vocabulaire du dossier dans la page publique), à envoyer "
            "dans la minute s'il demande à ne voir que la page patient. AUCUNE relance d'ici vendredi : un "
            "prospect qui a donné jour et heure n'est plus relancé, il est attendu.",
    },
    # ── LES QUATRE ENVOIS DU SOIR DU 22/09 (relevé de King à 17:31 : « MITOC, L'Opticien, Yaks, Skye »).
    "midas-touch-optic-center-mitoc": {
        "last_send_state": "sent", "Follow-up date": "2026-09-29", "follow_ups_sent": "2",
        "Notes_extra": "22/09 (soir) — relance envoyée par King (FU2, due le 21/09) : sa fiche Facebook trouve "
                       "son public mais l'examen de vue ne se réserve nulle part ; une page avec les montures, "
                       "les prix en FCFA, les horaires, le bassin étudiant de Molyko et un bouton WhatsApp. "
                       "Prochaine et DERNIÈRE touche : 29/09, puis on classe.",
    },
    "opticien-bali-douala": {
        "last_send_state": "sent", "Follow-up date": "2026-09-25", "follow_ups_sent": "2",
        "Notes_extra": "22/09 (soir) — deuxième message envoyé par King, sur le créneau que le prospect avait "
                       "lui-même fixé (« dim 20 / mar 22 / ven 25 »). Prochaine touche : vendredi 25/09, et ce "
                       "sera la dernière (trois messages maximum, puis parked daté).",
    },
    "skye-douala": {
        "last_send_state": "sent", "Follow-up date": "2026-09-29", "follow_ups_sent": "2",
        "Notes_extra": "22/09 (soir) — relance 2/3 réécrite SANS reproche et envoyée par King : une question sur "
                       "LEUR contenu (les horaires et les soins affichés sont-ils justes ?), jamais sur leur "
                       "silence. Prochaine et DERNIÈRE touche : 29/09, puis parked daté.",
    },
    "yaks-douala": {
        "last_send_state": "sent", "Follow-up date": "2026-09-29", "follow_ups_sent": "2",
        "Notes_extra": "22/09 (soir) — relance 2/3 envoyée par King, même réécriture : « qu'est-ce qui manque "
                       "ou qu'est-ce qui est faux sur la page ? ». Prochaine et DERNIÈRE touche : 29/09.",
    },

    # ── DÉCISION DE KING, 22/09 16:30 — « Labiomed et Bonanjo relancer prochaine vague ».
    #    Les deux messages du 16:22 et 16:24 sont donc partis (une coche chacun) : ils glissent
    #    d'une vague, ils ne sont pas perdus, et on ne réécrit pas aujourd'hui par-dessus un
    #    message distribué il y a quelques minutes — même règle que pour les quatre « distribués
    #    non lus » du lot du 19/09.
    "labiomed-deido": {
        "last_send_state": "sent",
        "Follow-up date": "2026-10-01",
        "site_url": "https://labiomed.vercel.app",
        "Conversation_extra":
            "22/09 16:22 — relance ENVOYÉE par King : la carte du lien `labiomed.vercel.app` titrée "
            "« LABIOMED — Analyses médicales à Deido-Bassa, Douala », le texte « Je sais que votre emploi "
            "du temps au laboratoire est très chargé. Je fais un suivi des projets de la semaine : la "
            "maquette de votre site est toujours active et prête ici », la phrase « Tout est configuré "
            "(vos horaires, vos examens et la prise de rendez-vous directe sur votre WhatsApp) » et la "
            "question fermée « Souhaitez-vous qu'on valide le lancement cette semaine ? ». Rappel du fil : "
            "« Ok je vous reviens des que je suis disponible » le 19/09 21:16, emoji 🙏 à 21:27, dernière "
            "visite 21:40 — il avait donc LU la réponse de King. DÉCISION KING 16:30 : prochaine vague. "
            "PUIS, 22/09 16:41, IL A RÉPONDU à la relance de 16:22, en trois messages : « Bjr » · « Non pas "
            "encore je ne suis pas en place » · « Quand je serai la je vais vous contacter ». Ce n'est ni un "
            "oui ni un refus : il n'est pas encore installé. Réponse de King dans l'heure (§0 de "
            "sales/Send-Vague-2026-09-22-16h45.md), 17:14 — réponse de King, SON texte, pas le brouillon du §0 : « C'est très clair, Docteur. Merci pour "
            "la précision ! » · « La maquette reste active et accessible à tout moment. J'attends de vos "
            "nouvelles dès que vous serez de retour / disponible ! » — DEUX coches, il l'a lue. AUCUNE DATE "
            "n'a été promise au client : le 1ᵉʳ octobre est une échéance INTERNE, pas un engagement.",
        "Notes_extra":
            "CORRECTION DU 22/09 16:41 — le mot « premier OUI DE LA CAMPAGNE » était trop fort : son « Oui » du "
            "19/09 acceptait un APERÇU, et son « je vous reviens quand je serai disponible » était un report. "
            "Sa phrase d'aujourd'hui le confirme : « pas encore, je ne suis pas en place ». On le classe donc "
            "en REPORT MOTIVÉ, pas en oui commercial — c'est la même leçon que le « Oui » de courtoisie : un "
            "accord sur un fichier n'est pas un accord sur un prix. "
            "Ce message du 16:22 ne contient PAS le prix (le prix du fil reste 100 000 FCFA, 50/50). "
            "À la prochaine vague, ne pas répéter le 16:22 : une seule ligne, et le prix avec le lien à "
            "l'accord. Ne jamais compter ce fil comme « quatre jours de silence » — il a reçu quelque "
            "chose aujourd'hui.",
    },
    "centre-medical-de-bonanjo": {
        "last_send_state": "sent",
        "Follow-up date": "2026-09-28",
        "site_url": "https://bonanjo.vercel.app",
        "Conversation_extra":
            "22/09 13:35 — King avait envoyé (DEUX coches) la page complète avec le lien "
            "`bonanjo.vercel.app` : « Comme promis, votre aperçu — et comme vous m'avez répondu, j'ai fait "
            "la page entière plutôt qu'un simple écran », les neuf services en une phrase (neurologie, "
            "médecine générale, radiologie, échographie, gynécologie, pédiatrie, chirurgie, accouchement), "
            "le rendez-vous qui se confirme sur WhatsApp « au lieu de passer par un annuaire », le prix "
            "posé (100 000 FCFA — 50 000 pour commencer, 50 000 à la mise en ligne, rien dû avant accord) "
            "et « Si quelque chose est inexact — un horaire, un service, une adresse — dites-le moi et je "
            "corrige tout de suite. Un “oui” suffit. » Puis 16:24 — relance ENVOYÉE : la carte du lien, "
            "« Je sais que la gestion du Centre Médical vous prend énormément de temps… votre aperçu est "
            "toujours fonctionnel et prêt à être déployé ici », « vos 9 services y sont centralisés pour "
            "orienter immédiatement les patients de Google vers votre WhatsApp », et la question fermée "
            "« Avez-vous eu un moment pour regarder, ou souhaitez-vous que je réajuste quelques détails "
            "avant d'officialiser la mise en ligne ? ». Son dernier mot à lui, verbatim : « Bjr merci je "
            "vous reviens » (19/09 08:44). DÉCISION KING 16:30 : "
            "prochaine vague. PUIS un message de plus est parti dans la soirée du 22/09 (texte non relevé — "
            "King l'a écrit lui-même) : la relance prévue pour jeudi est CONSOMMÉE, on ne double pas. "
            "Prochaine touche : lundi 28/09, ou avant s'il répond.",
        "Notes_extra":
            "Le prix est DÉJÀ posé (13:35, et rappelé dans le fil du 19/09) : à la prochaine vague on ne "
            "le répète pas, on ne repose qu'une question de calendrier. Le fait décisif du dossier reste "
            "l'annuaire `mondocteur237.com` (honoraires publics) — il paie déjà, ailleurs, pour être "
            "trouvé.",
    },
}


# ── LE RELEVÉ DU 23/09/2026 (matin) ────────────────────────────────────────────
# Le Cristallin : King a mis le PRIX sur la table. C'était la règle posée le 22/09 à 15:53
# (« prix, hébergement et logins LWS seulement à la fin, après son accord ») — la fin est
# arrivée : l'aperçu est validé sur le fond, le client demande des ajustements depuis trois
# jours, et on ne continue pas à travailler gratuitement sans savoir s'il a le budget.
# ⚠️ CE QUE LE MESSAGE DIT ET NE DIT PAS : il annonce 150 000 FCFA « bilingue, hébergement
# 1 an, nom de domaine et assistant WhatsApp » — il ne parle NI de la page Facebook (l'option
# +50 000 jamais posée), NI du fait que son domaine est déjà à lui jusqu'au 13/06/2027 et que
# son hébergement LWS existe. À cadrer avant de facturer quoi que ce soit d'autre.
JOUR_2309 = {
    "univers-optique": {
        "stage": "closing",
        "stage_since": "2026-09-22",
        "Follow-up date": "2026-09-25",
        "Conversation_extra":
            "22/09 20:51 — LUI : « Je suis vraiment intéressé, il faudrait qu'on se voit pour en discuter. "
            "Vendredi matin 10h dans mon cabinet. Bonne nuit » · 22/09 21:22 — KING confirme : « c'est bien "
            "noté pour ce vendredi à 10h dans votre cabinet ». · 23/09 au soir — GEL DÉCIDÉ PAR KING : plus "
            "aucune modification de la page ni du dossier tant qu'il n'a pas payé. La page à montrer est "
            "celle déjà en ligne ; on n'en reconstruit aucune.",
        "Notes_extra":
            "Prix posé le 21/09 (100 000 FCFA, 50/50) et jamais rebaissé. La préparation de la réunion est "
            "faite (`sales/RDV-UNIVERS-OPTIQUE-2026-09-25.md` + le business case d'une page, à envoyer dans "
            "l'heure qui suit) : elle ne demande plus aucun travail sur le site.",
    },
    "uni-labo-bonamoussadi": {
        "stage": "offer",
        "stage_since": "2026-09-23",
        "Follow-up date": "2026-09-25",
        "last_send_state": "delivered",
        "Conversation_extra":
            "22/09 21:15 — LUI : « Présentiel ». · 22/09 21:20 — KING : « D'accord ça marche pour moi ». · "
            "22/09 21:24 — KING propose de se voir À SON LABORATOIRE (Carrefour Etoo) et demande le "
            "créneau : « plutôt disponible en matinée (vers 10h) ou en début d'après-midi (vers 14h30) ? » · "
            "23/09 13:30 — KING : le créneau de 10 h est pris par un autre rendez-vous client, il PROPOSE "
            "DONC 14h30 pour vendredi, joint LA GRILLE TARIFAIRE STANDARD (PDF) et pose LE PRIX : "
            "150 000 FCFA — « la création de votre site bilingue complet (avec le formulaire de "
            "réservation WhatsApp direct) », 50 % d'acompte au démarrage et 50 % à la livraison. Il "
            "demande une confirmation pour bloquer le créneau. EN ATTENTE DE SA RÉPONSE : rien d'autre "
            "ne se prépare tant qu'il n'a pas dit oui à 14h30.",
        "Notes_extra":
            "LE SEUL DOSSIER SUR LEQUEL ON TRAVAILLE ENCORE VENDREDI : les deux autres (Le Cristallin, "
            "Univers Optique) sont GELÉS jusqu'au paiement (décision de King du 23/09 au soir : « on ne "
            "touche plus rien jusqu'à ce que les prospects deviennent des clients payants »). Prix posé : "
            "150 000 FCFA (même tarif de référence que celui envoyé au Cristallin), acompte 75 000. La "
            "grille tarifaire standard a été jointe en PDF : c'est elle qui fait foi si un écart apparaît "
            "entre le message et le PDF.",
    },
    "le-cristallin": {
        "stage": "closing",
        "stage_since": "2026-09-23",
        "Follow-up date": "2026-09-24",
        "last_send_state": "delivered",
        "Conversation_extra":
            "22/09 22:23 — LUI, mot pour mot : « Pour le reste ne change encore rien puisque j'ai "
            "certaines modifications que tu va apporter sans mon ok » : il annonce d'autres "
            "modifications et demande de ne rien figer. · "
            "23/09 09:46 — KING ENVOIE LES TROIS AJUSTEMENTS DEMANDÉS (slogan dans la barre de "
            "navigation, ses textes d'origine sur les verres conservés, adresse corrigée « Ancien "
            "COMECI / ECOTEX »), le lien de vérification `lecristallin-concept.vercel.app/?v=10`, "
            "puis LE PRIX POUR LA PREMIÈRE FOIS ÉCRIT : 150 000 FCFA — « création du site web "
            "officiel (bilingue, hébergement 1 an, nom de domaine et assistant WhatsApp) », "
            "acompte de démarrage 50 % = 75 000 FCFA, solde à la livraison et mise en ligne "
            "(3 à 5 jours), et il demande l'accord du client pour transmettre les informations de "
            "règlement Mobile Money. AUCUNE RÉPONSE DE LUI à l'heure de ce relevé : on attend un "
            "oui, un non ou une question — et on n'écrit plus rien d'autre entre-temps. · "
            "PRÉCISION APPORTÉE PAR LA CAPTURE DU FIL (23/09 au soir) : à 21:58 le 22/09 il a "
            "écrit « Pour le reste ne change encore rien puisque j'ai certains modifications "
            "que tu as apporté sans mon ok » ; King a répondu « D'accord » à 22:07 ; le client "
            "a mis « Vu » à 22:23. Sa demande est donc DÉJÀ une règle : rien ne se modifie sans "
            "son accord. · NOM DU CLIENT, lu dans le message de King du 23/09 09:46 : "
            "**Monsieur Messoua**. · GEL DÉCIDÉ PAR KING LE 23/09 AU SOIR : plus aucune "
            "modification de la page ni du dossier tant qu'il n'a pas payé. IMPORTANT : la page "
            "EN LIGNE est en AVANCE sur notre copie du dépôt (slogan dans la barre, textes "
            "d'origine sur les verres, adresse « Ancien COMECI / ECOTEX », liens WhatsApp en "
            "wa.me/237699905577 donc corrects) — NE JAMAIS la redéployer depuis ce dépôt, on "
            "écraserait ce que le client regarde.",
        "Notes_extra":
            "À TRANCHER AVANT PUBLICATION — cinq écarts relevés en relisant la page en ligne "
            "(?v=10, 23/09), tous vérifiables : ① la FAQ annonce « 18 assurances » en français et "
            "« 17 » en anglais, sur la même page ; ② le mur « Ils nous font confiance » en affiche "
            "19 ; ③ le bloc « Grandes entreprises & sociétés · 32 ans d'expérience » est TOUJOURS "
            "imprimé DEUX FOIS (défaut relevé le 22/09, non corrigé) ; ④ les horaires publiés "
            "(lun–ven 8h30–18h30, sam 8h30–13h30) contredisent son propre flyer (09h30–19h30, "
            "09h30–13h30) — c'est à LUI de trancher ; ⑤ « depuis 2010 » (16 ans) cohabite avec "
            "« 32 ans d'expérience » ; ⑥ POINT DE FORME : la page parle de « données structurées (le balisage "
            "`aggregateRating`) » en clair, face client — du jargon de développeur sur la page d'un opticien, "
            "à traduire en français simple au prochain passage (table des péages, "
            "`sales/PERSUASION-5-NIVEAUX-2026-09-23.md` §2). PÉRIMÈTRE DU PRIX, à cadrer : le message de 150 000 FCFA ne "
            "mentionne PAS la page Facebook (l'option +50 000 reste non posée) ; « hébergement 1 an "
            "+ nom de domaine » doit être cadré puisqu'il POSSÈDE déjà son domaine jusqu'au "
            "13/06/2027 et son hébergement LWS (ns1/ns2.lws-hosting.net) — on pose le fichier sur "
            "SON hébergement sans toucher au DNS, sinon son adresse "
            "contact@lecristallinoptique.com tombe. Mise en ligne annoncée 3 à 5 jours après "
            "l'acompte. Tant qu'il n'a pas dit oui, on ne touche ni au DNS, ni aux accès LWS, ni "
            "à l'ancien site.",
    },
}


def _apply_evening(out: list) -> None:
    by = {r.get("slug"): r for r in out}
    missing = [k for k in EVENING_2109 if k not in by]
    if missing:
        sys.exit(f"✗ EVENING_2109 : slug(s) introuvable(s) {missing} — une table d'état qui ne trouve "
                 f"pas sa ligne est une table menteuse. Rien n'a été écrit.")
    for slug, patch in EVENING_2109.items():
        r = by[slug]
        extra = patch.pop("Notes_extra", "")
        for k, v in patch.items():
            r[k] = v
        if extra:
            r["Notes"] = (str(r.get("Notes") or "") + " · " + extra).strip(" ·")
        r["stage_since"] = "2026-09-21"
        r["follow_ups_sent"] = r.get("follow_ups_sent") or "0"



def _apply_state(out: list, table: dict, name: str) -> None:
    """Applique une table d'état au relevé : elle ÉCRASE les champs scalaires qu'elle cite (elle est
    plus récente que tout le monde) et APPEND les deux champs de récit (`Conversation_extra`,
    `Notes_extra`) — un fil de conversation ne se remplace pas, il se continue. Un slug introuvable
    fait REFUSER la construction : une table d'état qui ne trouve pas sa ligne est une table
    menteuse.

    ⚠️ On travaille sur une COPIE de l'entrée. L'ancienne version faisait `patch.pop("…_extra")`
    DIRECTEMENT dans la table du module : le deuxième passage dans le même processus trouvait la
    table vidée de ses récits et les perdait en silence. Invisible tant qu'on ne lance le script
    qu'une fois — donc invisible jusqu'au jour où un rebuild enchaîne deux passes."""
    by = {r.get("slug"): r for r in out}
    missing = [k for k in table if k not in by]
    if missing:
        sys.exit(f"✗ {name} : slug(s) introuvable(s) {missing} — rien n'a été écrit.")
    for slug, entry in table.items():
        patch = dict(entry)
        r = by[slug]
        for key in ("Conversation_extra", "Notes_extra"):
            extra = patch.pop(key, "")
            if extra:
                base = key.replace("_extra", "")
                r[base] = (str(r.get(base) or "") + " · " + extra).strip(" ·")
        for k, v in patch.items():
            r[k] = v


def _apply_jour(out: list) -> None:
    """Les deux relevés, dans l'ordre : 22/09 (soir) puis 23/09 (matin)."""
    _apply_state(out, JOUR_2209, "JOUR_2209")
    _apply_state(out, JOUR_2309, "JOUR_2309")



# ── DÉCISION DE KING — 22/09/2026, 16:45 ──────────────────────────────────────
# « je pense qu'on devrais laisser tomber les ecoles »
#
# Conséquence : les 39 écoles sortent des vagues d'envoi et du plan du jour. Ce n'est pas
# un effacement de données — elles restent dans le CRM, avec leur audit, et l'histoire du
# seul établissement scolaire qui a répondu (STIBCCOL, Buea, qui a demandé qu'on revienne
# en octobre) est gardée telle quelle. La raison de fond est chiffrée le même jour dans
# sales/PROFIL-DES-OUI-2026-09-22.md : les écoles répondent 2,6 % du temps, contre 11,1 %
# pour les prospects qui ont déjà payé pour être visibles quelque part. On ne prospecte
# plus ce segment ; on ne l'efface pas non plus.
WORKBOOK_TYPE_EXCEPTIONS = {
    # slug : type réel (le classeur les avait mis en « school » par défaut)
    "midas-touch-optic-center-mitoc": "other",   # opticien de Molyko (Buea)
}


# ── LES MORTS DU 22/09 · décision de King, 17:55 ────────────────────────────────────────────────
# « §1 and §2 weren't even open … I prefer spending time on fresh prospects, classify all those as
#   dead, if there is any we hosted a demo for let me know so that we delete it. »
#
# DEUX LEÇONS GRAVÉES ICI, parce qu'elles ont coûté 33 fils :
#   ① « lu » n'est PAS une preuve d'intérêt. Notre attribution de lecture du lot du 19/09 était
#      fausse — King l'a constaté sur son téléphone. C'est l'erreur OraCare (« message non lu
#      attribué à tort le 18/09 ») qui revient en volume : quand la donnée de lecture n'est pas
#      certaine, on ne la présente pas au prospect, et on ne la compte pas dans la stratégie.
#   ② Un message qui DIT « vous avez ouvert mon message » repose sur cette donnée-là. Plus jamais.
#      Un message ne se justifie que par ce qui est vérifiable et utile au lead.
#
# Ces lignes passent en `parked` SANS date : elles sortent du plan, et il n'existe aucun chemin
# qui les y remette (ni Follow-up date, ni RELANCE_A_JOUR). « Dated parked » = réécriture un jour
# si un fait nouveau apparaît ; ici, pas de fait, pas de date.
DEAD_2209 = {
    "flemming-dream-bessengue": "lot du 19/09",
    "biodiagnostics-sable": "lot du 19/09",
    "diagmed-bonaberi": "lot du 19/09",
    "labtag-bali": "lot du 19/09",
    "sainte-anne-newbell": "lot du 19/09",
    "pasteur-medlas-akwa": "lot du 19/09",
    "cidm-saint-joseph": "lot du 19/09",
    "malia-labo-douala": "lot du 19/09",
    "adonai-douala": "lot du 19/09",
    "labo-meka-bonamoussadi": "lot du 19/09",
    "interlabo-akwa": "lot du 19/09",
    "la-passerelle-deido": "lot du 19/09",
    "pathcare-deido": "lot du 19/09",
    "2k-labo-yassa": "lot du 19/09 (réponse automatique)",
    "discovery-labs-bassong": "lot du 18/09",
    "yondja-analyse-douala": "lot du 18/09",
    "laboratoire-du-chateau-bonaberi": "lot du 18/09",
    "departement-biologique-akwa": "lot du 18/09",
    "cabinet-isis-bonapriso": "lot du 18/09",
    "cabinet-la-cerisaie-bonapriso": "lot du 18/09",
    "cabinet-idoc-bonapriso": "lot du 18/09",
    "centre-des-capucines-bonapriso": "lot du 18/09",
    "cabinet-brulet-epaka-bonapriso": "lot du 18/09",
    "centre-kouam-samuel-bali": "lot du 18/09",
    "das-group-international-akwa": "lot du 18/09",
    "cabinet-dentaire-emmanuel-bonamoussadi": "lot du 18/09",
    "clinique-de-luniversite-bassa": "lot du 18/09",
    "medi-labo-akwa": "lot du 18/09",
    "kamais-optic-bessengue": "lot du 18/09",
    "la-bethanie-bonaberi": "lot du 18/09",
    "jempo-deido": "lot du 18/09",
    "camera-akwa": "lot du 18/09",
    "le-nid-bessengue": "lot du 18/09",
}


def _apply_dead(out: list) -> None:
    """Un seul endroit qui tue, un seul endroit qui réveille."""
    by = {r.get("slug"): r for r in out}
    for slug, why in DEAD_2209.items():
        r = by.get(slug)
        if r is None:
            continue
        r["stage"] = "parked"
        r["Follow-up date"] = ""
        r["Notes"] = (str(r.get("Notes") or "") +
                      f" · ⚰️ MORT le 22/09 ({why}) — jamais ouvert, jamais répondu ; décision de King : "
                      "on ne réécrit plus, on va vers des prospects frais. Aucune relance programmée.").strip(" ·")


# ── LA PASSE « VITRINE » DU 22/09 AU SOIR · 24 leads santé/optique lus un par un ───────────────
# King, 17:56 : « why tomorrow, time is 17:56, we can send one last batch … then move to content
# creation ». La passe a donc été faite ce soir, et elle a produit deux choses :
#   ① 5 leads JAMAIS contactés qui ont une vitrine À EUX (Facebook) → le dernier lot de la soirée ;
#   ② 19 leads vérifiés SANS aucune vitrine → notés `none found`, ils ne seront pas démarchés.
# Le critère est celui qui a coûté la soirée : vitrine à soi = 11,1 % de réponse ; sans = 2,5 %,
# et 0/33 sur les fils classés morts aujourd'hui.
FICHE_2209 = {
    "niva-labo-akwa": (
        'none found (aucun domaine — vérifié 22/09)',
        'facebook.com/people/Laboratoire-Danalyses-Médicales-Niva-Labo/61554339904742/',
        'Vitrine : page Facebook au nom du laboratoire (Akwa, rue King, face Vision Confort). Rien à lui côté domaine.',
    ),
    "aube-labo-akwa": (
        'none found (aucun domaine — vérifié 22/09)',
        'facebook.com/Aubelabo/',
        "Vitrine : page Facebook ACTIVE (dépistage IST, prélèvement à domicile, carrefour Montagne Manga Bell, Bali). ⚠️ Le numéro affiché sur la page est 6 95 75 36 91 ; celui du CRM (693 06 81 84) vient de l'annuaire — vérifier l'identité WhatsApp avant d'écrire.",
    ),
    "hyrus-labo-deido": (
        'none found (aucun domaine — vérifié 22/09)',
        'facebook.com/HYRUS-LABO-1716532941949127/ + facebook.com/p/HYRUS-LABO-100043399675037/ (DEUX pages)',
        "Vitrine : DEUX pages Facebook (999 et 778 mentions J'aime) + fiche Google 5,0/5 (5 avis) + Maligah. « examens à prix réduits » est leur positionnement affiché.",
    ),
    "megaoptic": (
        'none found (aucun domaine — vérifié 22/09)',
        'facebook.com/Mega Optic/',
        'Vitrine : page Facebook MegaOptic, avec une vidéo qui liste les ASSURANCES avec lesquelles ils travaillent (angle identique au Cristallin : ils parlent déjà assurances à leur audience).',
    ),
    "polyclinique-innova": (
        'none found (aucun domaine — vérifié 22/09)',
        'facebook.com/polycliniqueinnova/',
        "Vitrine : page Facebook active (Akwa, immeuble ancien Marlboro / près pharmacie de la Trinité ; ouvert 7j/7 24h/24 ; deux sites Douala + Yaoundé ; membre du réseau CAMERHO). Les horaires et les contacts vivent dans les POSTS, pas dans une page trouvable. Numéros publiés sur la page : 693 14 31 78 / 690 14 71 12 ; celui du CRM (674 145 740) vient de l'annuaire — vérifier l'identité WhatsApp avant d'écrire.",
    ),
    "m-dina-optic": (
        'none found (22/09 : aucune page, aucun domaine — seulement une entrée de carte)',
        '',
        '',
    ),
    "lux-optique": (
        'none found (22/09)',
        '',
        '',
    ),
    "dumbu-lunetterie": (
        'none found (22/09)',
        '',
        '',
    ),
    "class-optic": (
        'none found (22/09 : zéro résultat, même hors Douala)',
        '',
        '',
    ),
    "horizon-optique": (
        'none found (22/09 — un compte Instagram homonyme à 33 abonnés, 0 post, numéro étranger : PAS eux)',
        '',
        '',
    ),
    "plan-te-optique": (
        'none found (22/09 — les pages « Planète Optique » trouvées sont Tébessa, Yaoundé et Libreville : homonymes)',
        '',
        '',
    ),
    "bioscan-newbell": (
        'bioscanlabo.com — VIVANT (WordPress/OceanWP, monté en 2025) : services, galerie, blog, widget WhatsApp',
        '',
        "⚠️ DEUX FAITS VÉRIFIÉS le 22/09 sur son propre site : ① l'adresse de contact est écrite "
        "`bioscanlabo@g.mail.com` — un domaine « g.mail.com » qui n'existe pas, donc les messages envoyés là "
        "ne partent nulle part ; ② les chiffres se contredisent (« +5 ans d'expertise » vs « +100 patients "
        "pris en charge chaque année »). Téléphone du site 680 060 394 = numéro du CRM. RAPPEL 19/09 : "
        "numéro noté « PAS SUR WHATSAPP » → écrire par un autre canal, ou vérifier le profil avant.",
    ),
    "biolex-deido": (
        'none found (22/09)',
        '',
        '',
    ),
    "clinique-des-cites-makepe": (
        'none found (22/09 — fiche Maligah + carte ; aucun site, aucune page)',
        '',
        '',
    ),
    "centre-medical-saint-luc": (
        'none found (22/09)',
        '',
        '',
    ),
    "wonders-bonamoussadi": (
        'none found (22/09)',
        '',
        '',
    ),
    "imagerie-saint-joseph": (
        'none found (22/09)',
        '',
        '',
    ),
    "labo-phanuel-akwa": (
        'none found (22/09 : zéro résultat)',
        '',
        '',
    ),
    "tchaya-optique": (
        'none found (22/09)',
        'facebook.com/T.OPTIQUE/ (+ une seconde page, cabinet depuis 1974)',
        "DÉJÀ CONTACTÉ : message 1 parti le 21/09 à 17:47 (une coche), jamais enregistré dans le CRM — corrigé le 22/09. Vitrine : deux pages Facebook, dont « TCHAYA OPTIQUE INTERNATIONAL » (2 390 mentions J'aime, depuis 1974).",
    ),
    "disc-optique-m-dicale": (
        'none found (22/09)',
        'facebook.com/people/DISC-Optique-Médical-DOM/100088156174066/',
        'DÉJÀ CONTACTÉ : message 1 parti le 21/09 à 17:48 (une coche), jamais enregistré — corrigé le 22/09. Vitrine : page Facebook « DISC Optique Médical - DOM » (Bali, rue des manguiers).',
    ),
    # ── Deuxième passe du 22/09 au soir : on ne garde ici QUE les leads que la première passe n'avait
    #    pas vus. Les autres (bioscan, biolex, horizon-optique, clinique-des-cites, imagerie-saint-joseph,
    #    labo-phanuel) sont déjà dans la table ci-dessus — deux entrées pour une même clé dans un dict,
    #    c'est la seconde qui gagne EN SILENCE. Le garde-fou ne voit pas ce piège ; la relecture, si.
    "afrique-labo-douala": (
        'afriqlabo.com — VIVANT (site du laboratoire, Bessengué feu rouge, même numéro 690 54 70 93 '
        'que notre fiche) — VU LE 22/09 PENDANT LA PASSE « MOTS-CLÉS »',
        '',
        "⚠️ CORRECTION : la fiche le donnait sans site, et un concept lui a même été construit et déployé. "
        "Afrique Labo a une vitrine À LUI → profil « a déjà une vitrine », donc plus jamais « vous n'existez "
        "pas ». Site simple (valeurs, contact) sans prise de rendez-vous. Le concept déployé peut encore "
        "servir, mais l'angle change : partir de ce qu'il a déjà, pas de ce qui lui manque.",
    ),
    "lyfyoptic": (
        'lyfyoptic.com — VIVANT, mais GABARIT NON TERMINÉ : les titres « Premier texte » et « Deuxième texte » '
        'sont restés sur la page d\'accueil (lu le 22/09)',
        '',
        "Vitrine : site à eux. Le numéro du site (699 98 06 66) est celui du CRM. Adresse publiée : "
        "15086 Akwa-Bonadibong. « Assistance 24/24, 7j/7 » est leur argument — et rien sur la page ne permet "
        "de prendre un rendez-vous.",
    ),
    "cmodn-makepe": (
        'none found',
        'facebook.com/profile.php?id=100063463571676 (page au nom du centre)',
        "Vitrine : la page Facebook, PAS de site (« Site internet : - » chez maligah, « no website » chez "
        "africabizinfo). Numéro 698 00 68 98 confirmé par deux annuaires. Profil : il entretient déjà une "
        "vitrine qui ne lui appartient pas.",
    ),
    "espace-vision": (
        'none found (22/09 : aucune page, aucun domaine — registre ONOC n° 030 + une fiche businesslist)',
        '',
        "Registre ONOC : BIYOUMA Théodore, 677 33 94 24. Hors profil d\'envoi pour l\'instant.",
    ),
    "clinique-saint-luc": (
        'none found (22/09 : trois fiches d\'annuaire — maligah, hospitalby, medpages — aucune vitrine)',
        '',
        '',
    ),
    "faby-optique": ('none found (22/09 : aucun résultat sur son nom exact)', '', ''),
}



def _sites_rows():
    """Les prospects TROUVÉS par la deuxième passe : ils ne figuraient pas dans le CRM."""
    return [
        dict(slug="scientilabo-akwa", org="ScientiLabo", city="Douala (Akwa, 1749 rue Gallieni)",
             org_type="lab", language="FR", wa_number="696 423 477", wa_verified="unknown",
             contact_channel="WhatsApp", stage="prospecting", contacted="No", reply="No", demo="No",
             source="pass_vitrine", source_detail="2ᵉ passe du 22/09 (site à eux)",
             Website="scientilabo.com — VIVANT et fourni (34 ans, ISO 15189, RDV en ligne, résultats en ligne)",
             notes="Vitrine à lui → profil. Agréé n°25 du Ministère de la Santé, 34 ans d'existence, analyse "
                   "des eaux et toxicologie en plus de la biologie ; TROIS adresses e-mail différentes sur le "
                   "site (scientisom@yahoo.fr, scientilabo@gmail.com, contact@scientilabo.com) et deux numéros "
                   "(696 423 477 / 680 934 010). Présent dans le réseau de soins AssurTous."),
        dict(slug="kylaya-labo-bali", org="KYLAYA LABO", city="Douala (Bali, 189 rue des Manguiers)",
             org_type="lab", language="FR", wa_number="696 78 77 78", wa_verified="unknown",
             contact_channel="WhatsApp", stage="prospecting", contacted="No", reply="No", demo="No",
             source="pass_vitrine", source_detail="2ᵉ passe du 22/09 (site à eux)",
             Website="kylayalabo.com — VIVANT (analyses, RDV en ligne, espaces résultats patients ET médecins)",
             notes="Vitrine à lui → profil. Site sérieux et complet : biochimie (≈70 analyses), marqueurs "
                   "tumoraux, biologie moléculaire, prélèvements à domicile, résultats en ligne. Également "
                   "dans le réseau de soins AssurTous."),
        dict(slug="biomedicam-bonapriso", org="Laboratoire Biomedicam", city="Douala (Bonapriso)",
             org_type="lab", language="FR/EN", wa_number="699 00 32 07", wa_verified="unknown",
             contact_channel="WhatsApp", stage="prospecting", contacted="No", reply="No", demo="No",
             source="pass_vitrine", source_detail="2ᵉ passe du 22/09 (site à eux)",
             Website="biomedicam.com — VIVANT, bilingue FR/EN (labo ouvert depuis le 2 janvier 1990)",
             Facebook="facebook.com/biomedicam",
             notes="Vitrine à lui (site + page FB) → profil. Histoire vérifiable et forte : premier bébé "
                   "éprouvette de la sous-région (14 avril 1998), biologie de la reproduction, tests ADN, "
                   "biologie vétérinaire ; dirigeant Dr Christian Pany, 1058 avenue Paul Soppo-Priso."),
        dict(slug="optic-laser-medical-akwa", org="Optic Laser Medical", city="Douala (Akwa, bd de la République)",
             org_type="other", language="FR", wa_number="", wa_verified="unknown",
             contact_channel="", stage="prospecting", contacted="No", reply="No", demo="No",
             source="pass_vitrine", source_detail="2ᵉ passe du 22/09 (site à eux)",
             Website="opticlasermedical.com — VIVANT (SARL fondée par M. Njumssa François)",
             notes="⏸ PAS ENCORE ENVOYABLE : aucune coordonnée relevée sur la page publique. Le numéro est la "
                   "première chose à trouver avant tout message."),
    ]


def _apply_fiche(out: list) -> None:
    by = {r.get("slug"): r for r in out}
    for slug, (site, fb, note) in FICHE_2209.items():
        r = by.get(slug)
        if r is None:
            continue
        r["Website"] = site
        if fb:
            r["Facebook"] = fb
        if note:
            r["Notes"] = (str(r.get("Notes") or "") + " · " + note).strip(" ·")
        if site.startswith("none found") and not fb:
            r["disqualification_reason"] = "aucune vitrine à lui (passe du 22/09) — hors profil d'envoi"


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
        # Le classeur d'origine est un lot d'écoles : « school » est le type PAR DÉFAUT, pas une
        # lecture. Deux exceptions nommées, sinon on écrase une réalité (MITOC, 22/09 : la fiche dit
        # « we refract, prescribe n mount lenses » — c'est un opticien, pas une école).
        rec["org_type"] = WORKBOOK_TYPE_EXCEPTIONS.get(rec["slug"], "school")
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

    # 1c · les prospects TROUVÉS par la passe « vitrine » du 22/09 (ils n'étaient pas dans le CRM).
    #      Ils passent AVANT la normalisation des clés : ils arrivent en forme courte, comme les autres.
    for p in _sites_rows():
        out.append({"School": p["org"], **p})

    # 2d · les 19 laboratoires du pack du 19/09 au soir
    for p in LABS_1909:
        out.append({"School": p["org"], **p})

    # 2d-bis · les envois RÉELS du 19/09 au soir (captures de King)
    _apply_envois(out)

    # 2e · les 5 laboratoires ÉCARTÉS pour site vivant — la donnée qui évite de refaire le travail
    for p in _labs_ecartes_rows():
        out.append({"School": p["org"], **p})

    # 2f · la vague 1 opticiens (21/09)
    for p in OPTICIENS_2109:
        out.append({"School": p["org"], **p})
    for p in _opt_rows():
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

    # 2g · l'état des fils chauds du 21/09, appliqué EN DERNIER des fusions. Avant, il se faisait
    #      écraser ; après KEYMAP il ne pourrait plus rien poser. C'est LA place : rien, après,
    #      ne réécrit un fait d'échange.
    _apply_evening(out)
    _apply_jour(out)
    _apply_dead(out)
    _apply_fiche(out)

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
