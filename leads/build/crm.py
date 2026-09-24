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
         last_send_state="sent", follow_ups_sent="2",
         notes="Message 1 envoyé 17/09 13:24. **FU1 (M+2) ENVOYÉE par King le 19/09** (confirmé par lui : "
               "« I have already sent message de relance »). **FU2 partie le 21/09 à 17:39** (éditée, une "
               "coche), angle résultats WhatsApp. ⚠️ LE COMPTEUR EST RESTÉ À 1 JUSQU'AU 23/09 : le journal "
               "disait 2 (21/09 au soir), la source disait 1 — conséquence réelle, le calcul M+4 croyait "
               "la FU3 pas encore due alors que sa date écrite était le 23/09. Corrigé ici et inscrit au "
               "`RELANCE_A_JOUR` (views.py) le 23/09 : **FU3 = DERNIÈRE TOUCHE, due le 23/09**, le palier "
               "des 3 relances est atteint après elle. "
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
               "C est une seance de CLOTURE, pas un premier contact. PRIX POSE le 23/09 a 13:30 : 150 000 FCFA, "
               "acompte 75 000, la grille tarifaire standard est deja entre leurs mains. "
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


# ── LOT 3 · LES OPTICIENS NEUFS DU 24/09 (source : mont-pandi, catégorie Opticiens) ────────────
# Sept fiches lues le 24/09 dans la catégorie « Opticiens » de l'annuaire communautaire Mont-Pandi.
# Cinq entrent dans le lot 3 ; deux sont ÉCARTÉES le jour même et restent tracées ici.
# ⚠️ Ce sont des numéros d'ANNUAIRE, jamais vérifiés sur WhatsApp : la porte A se vérifie dans
# l'application, par King, AVANT l'envoi (leçon Horizon du 24/09). L'annuaire se trompe parfois —
# il se trompe même trois fois dans ce lot-ci (voir `wa_number_note`).
BATCH_2409_3_NEW = [
    dict(slug="el-roi-optique-medicale", org="El Roï Optique Médicale", city="Douala (Village)",
         org_type="other", language="FR", wa_number="693 127 302", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 678), lue le 24/09",
         contact_name="",
         notes="LOT 3 (préparé le 24/09, PAS ENVOYÉ). Repères publiés par la boutique elle-même : « à 200 m "
               "de la Elf axe lourd, en face du Collège Pozam et à côté de la Pharmacie Saint-Pierre ». "
               "Services publiés : examen de la vue · vente de lunettes · accessoires et réparation · "
               "conseil et orientation. Horaires publiés 08:00→18:00. Second numéro publié : 670 790 215 "
               "(repli). Le message part sur 693 127 302."),
    dict(slug="net-optique-medical", org="Net Optique Médical", city="Douala (Akwa)",
         org_type="other", language="FR", wa_number="675 785 930", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 761), lue le 24/09",
         notes="LOT 3 (préparé le 24/09, PAS ENVOYÉ). Adresse publiée : Akwa, boulevard de la Liberté. "
               "Services publiés : ophtalmologie · lunetterie · optique · horlogerie · conseil. Horaires "
               "publiés 08:00→18:30."),
    dict(slug="royal-optic-bali", org="Royal Optic", city="Douala (Bali)",
         org_type="other", language="FR", wa_number="676 250 409", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 763), lue le 24/09",
         notes="LOT 3 (préparé le 24/09, PAS ENVOYÉ). Se présente comme « Cabinet d'Optique Médicale ». "
               "Repères publiés : « Bali, Alimentation Koumassi, en face Le Phoenix, à côté de la Direction "
               "Générale de Zenith Assurances ». Horaires publiés 08:00→18:30. Second numéro publié : "
               "691 219 986 (repli). Le message part sur 676 250 409."),
    dict(slug="k-vision-care", org="K Vision Care", city="Douala (Bessengue · Ancien 3e · Ndogpassi)",
         org_type="other", language="FR", wa_number="677 077 459", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 672), lue le 24/09",
         notes="LOT 3 (préparé le 24/09, PAS ENVOYÉ). ⚠️ L'ANNONCE SE CONTREDIT : le texte publie "
               "677 077 459, le lien de la même fiche écrit 677 077 159 — un chiffre d'écart. "
               "VERR : 677 077 459 et 3ᵉ numéro 695 865 346, et n'envoyer qu'après avoir vu le nom du "
               "profil à l'écran. Trois magasins publiés : Bessengue (rue de la Réunification) · entre "
               "Ancien 3e et le marché Congo, en face de l'hôpital Congo 2 (en haut à l'étage) · marché "
               "Ndogpassi. Horaires publiés 08:00→18:00."),
    dict(slug="cabinet-optique-la-retine", org="Cabinet d'Optique la Rétine", city="Douala (Akwa)",
         org_type="other", language="FR", wa_number="695 474 364", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 666), lue le 24/09",
         notes="LOT 3 (préparé le 24/09, PAS ENVOYÉ). Repère publié : Akwa, « non loin de l'ancien Cinéma "
               "Étoile ». Horaires publiés 08:00→18:00."),
]

# Deux fiches lues le même jour et ÉCARTÉES — elles restent au dossier pour que personne ne les
# « redécouvre » comme une bonne idée.
BATCH_2409_3_ECARTES = [
    dict(slug="valdoz-optic-douala", org="Valdoz Optic Douala", city="Douala (Akwa)",
         org_type="other", language="FR", wa_number="682 833 319", wa_verified="unknown",
         stage="disqualified", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 676), lue le 24/09",
         disqualification_reason="numéro ambigu — un des numéros publiés est celui d'un lead DÉJÀ contacté",
         notes="⛔ ÉCARTÉ DU LOT 3 (décision du 24/09). La fiche publie « 682833319/682411637 » en texte, mais son lien "
               "WhatsApp pointe sur 682 833 319 / 656 223 863 — et 656 22 38 63 est le numéro de "
               "**Fashion Vision**, déjà contacté le 24/09. Soit les deux boutiques partagent la ligne, "
               "soit l'annuaire a recopié le mauvais numéro. Dans les deux cas, envoyer ici risquerait un "
               "SECOND message à une boutique déjà sollicitée. À trancher par King avant toute reprise : "
               "si Valdoz et Fashion Vision sont la même maison, il n'y a pas deux prospects."),
    dict(slug="jucia-optics", org="Jucia Optics", city="Douala (Akwa)",
         org_type="other", language="FR", wa_number="653 449 349", wa_verified="unknown",
         stage="parked", contacted="No", reply="No", demo="No",
         source="directory", source_detail="Mont-Pandi, catégorie Opticiens (fiche 759), lue le 24/09",
         notes="EN RÉSERVE POUR LE LOT 4 (décision du 24/09), pas écarté : la boutique est crédible (Akwa 1, ancien 3e ; "
               "consultations, examen, lunettes, accessoires, entretien, conseils ; 08:00→18:30), mais "
               "**son numéro se contredit** — le texte publie 653 449 349, le lien écrit 653 449 385. "
               "Deux numéros à vérifier dans l'application avant d'écrire quoi que ce soit."),
]


# ── LE QUATRIÈME LOT — le registre officiel de l'ONOC (Littoral, lignes 85 à 159), 24/09 au soir ──
# Pourquoi cette source : elle a donné **100 % de joignables** au lot 1 (5/5) contre 60 % pour
# l'annuaire communautaire du lot 3, et elle donne **un nom à qui parler** (l'opticien assumant la
# responsabilité civile) en plus du numéro. Les sept sont NEUFS : croisés par nom ET par numéro avec
# les 156 lignes et les 62 leads déjà contactés — **Kamaïs Optic est tombé à ce contrôle** (déjà au
# CRM, contacté puis parqué) et sort du lot.
# ⚠️ Porte A NON vérifiée : elle se vérifie dans l'application, par King, avant l'écriture du message
# (leçon Horizon). D'où `wa_verified="unknown"` sur les sept, y compris là où un annuaire les décrit.
BATCH_2409_4_NEW = [
    dict(slug="cinq-sens-optique-medicale", org="Référence Optique Médicale Cinq Sens",
         city="Douala (Akwa + Brazzaville)", org_type="other", language="FR",
         wa_number="696 698 136", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, annuaire 2024 — Littoral ligne 118 (inscription 115/2021, "
                       "arrêté 1688), lu le 24/09 · fiche Mont-Pandi 671",
         contact_name="KOUGANG GUIFFO Casimir",
         notes="LOT 4 (préparé le 24/09 au soir, RIEN N'EST ENVOYÉ). Titulaire au registre : KOUGANG "
               "GUIFFO Casimir. Deux cabinets, dans ses mots : « Brazzaville entre le Carrefour "
               "Brazzaville et l'Ecole Saint Bruno · Akwa entre le Carrefour Douala Bar et le Carrefour "
               "Singer face Collège King Akwa. Tout sur la vue. » Horaires 08:00→18:00. Autres numéros "
               "publiés : 696 663 139 · 656 036 312. Porte A à vérifier à l'écran. Message : "
               "`sales/Send-BATCH-2026-09-24-Opticiens-4.md` §1."),
    dict(slug="skyoptic-akwa", org="SkyOptic Akwa (ETS Sky Optics)", city="Douala (Akwa)",
         org_type="other", language="FR", wa_number="655 649 803", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, Littoral ligne 119 (inscription 139, arrêté 0484), lu le 24/09 "
                       "· Maligah (ETS SKY OPTICS, Bd de la République, BP 15211) · Ayila'a",
         contact_name="LAMBO Dorice",
         notes="LOT 4 (préparé, PAS ENVOYÉ). Titulaire au registre : LAMBO Dorice. Deux annuaires le "
               "décrivent : Maligah — « ETS SKY OPTICS, Boulevard De La République, Akwa, BP 15211 », "
               "avec un fixe (233 42 75 00) ; Ayila'a — « Sky Optics Akwa, face BENEFICIAL LIFE "
               "INSURANCE », avec un prix affiché par l'annuaire (« à partir de 10 000 XAF »). Porte A "
               "à vérifier. Message : lot 4 §2."),
    dict(slug="lumumba-optique-medicale", org="Lumumba Optique Médicale", city="Douala (Makepe)",
         org_type="other", language="FR", wa_number="670 59 79 96", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, Littoral ligne 144 (inscription 054/2018, arrêté 6677), lu le "
                       "24/09 · deux pages Facebook + une fiche Maps (Voie Makepe Est)",
         contact_name="NZIKANG Armstrong TUAMBI",
         notes="LOT 4 (préparé, PAS ENVOYÉ). Titulaire : NZIKANG Armstrong TUAMBI. Deux pages Facebook "
               "portent son nom : « Lunettes Lumumba » (146 mentions J'aime, 24 personnes y sont "
               "passées, « We are a new optical center ») et « Lumumba Optique Medicale » (« vente des "
               "montures, verres médicaux et solaires »). Une fiche Maps existe (Makepe Est). Porte A à "
               "vérifier. Message : lot 4 §3."),
    dict(slug="win-optic-plus", org="Win Optic Plus", city="Douala", org_type="other", language="FR",
         wa_number="699 12 59 06", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, Littoral ligne 96 (inscription 109/2020, arrêté 0326), lu le "
                       "24/09 · page Facebook « WIN OPTIC PLUS SARL »",
         contact_name="BETCHEM à BETCHEM Jéhaziel",
         notes="LOT 4 (préparé, PAS ENVOYÉ). Titulaire : BETCHEM à BETCHEM Jéhaziel. Une page Facebook "
               "au nom exact existe — elle s'annonce en trois mots : Douala, Cameroon · Optician. "
               "⚠️ Ne jamais écrire « vous n'avez pas de site » : on n'a pas vu de site, ce n'est pas la "
               "même chose. Porte A à vérifier. Message : lot 4 §4."),
    dict(slug="golden-eyes-optic-douala", org="Golden Eyes Optic (Douala)",
         city="Douala (Bonanjo, Atrium Spar)", org_type="other", language="FR",
         wa_number="699 312 588", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, Littoral ligne 101 (inscription 090/2019, arrêté 2622), lu le "
                       "24/09 · site vivant goldeneyesoptic.com (page Contact)",
         contact_name="DJON II Achille Arnaud",
         notes="LOT 4 (préparé, PAS ENVOYÉ). Titulaire au registre : DJON II Achille Arnaud. ⚠️ ILS "
               "ONT UN SITE VIVANT (goldeneyesoptic.com) — donc jamais « vous n'avez pas de site ». Le "
               "site est Yaoundé d'abord (« Notre siège situé à Yaoundé, Nkomkana ») et Douala tient en "
               "une ligne de la page Contact : « Bonanjo au centre commercial l'Atrium Spar, 2e étage ». "
               "Numéros de Douala publiés par le site : 653 23 77 21 / 699 31 25 88 (le second est celui "
               "du registre). Angle : la page de la maison de Douala. Message : lot 4 §5."),
    dict(slug="la-ligne-optic-akwa", org="La Ligne Optic Akwa", city="Douala (Akwa)",
         org_type="other", language="FR", wa_number="683 651 108", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, Littoral ligne 109 (inscription 025/2017, arrêté 0533), lu le "
                       "24/09 — aucune autre trace publique trouvée",
         contact_name="JOUNGO Line Chantale",
         notes="LOT 4 (préparé, PAS ENVOYÉ). Titulaire : JOUNGO Line Chantale. Aucune page, aucun site, "
               "aucune fiche détaillée trouvés : la seule trace publique est le registre. ⚠️ Porte B "
               "FAIBLE (§8b : 2/3) — King décide explicitement. Remplaçant dans l'ordre d'envoi."),
    dict(slug="dm-optique", org="DM Optique", city="Douala", org_type="other", language="FR",
         wa_number="656 122 239", wa_verified="unknown",
         stage="prospecting", contacted="No", reply="No", demo="No",
         source="onoc_registry",
         source_detail="Registre ONOC, Littoral ligne 102 (inscription 021/2016, arrêté 0382), lu le "
                       "24/09 — aucune autre trace publique trouvée",
         contact_name="DOMCHE NOUMBI",
         notes="LOT 4 (préparé, PAS ENVOYÉ). Titulaire : DOMCHE NOUMBI. Aucune page, aucun site "
               "trouvés (24/09). ⚠️ Porte B FAIBLE (§8b : 2/3) — King décide explicitement. "
               "Remplaçant dans l'ordre d'envoi."),
]


def _batch_2409_3_rows():
    return BATCH_2409_3_NEW + BATCH_2409_3_ECARTES


def _batch_2409_4_rows():
    return BATCH_2409_4_NEW


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
    # le dossier de travail RÉEL du lead le plus actif (audit, notes de build, concept) — c'était
    # une vignette de maquette qui était liée ici, et le dossier `clients/uni-labo/` restait orphelin : M4 le refusait, à raison.
    "uni-labo-bonamoussadi": "clients/uni-labo/",
    # le dossier de travail RÉEL de Cavisa (inspiration, notes de build) — il est passé en `demo`
    # le 24/09 à 13:16, quand M. Dongmo a répondu : « Beaucoup de manquement mais c'est appréciable. »
    "cavisa-optique": "clients/cavisa/",
    # le dossier de travail de DM OPTIC — ouvert le 24/09 au soir, quand M. Domche Noumbi a répondu
    # « Ok Envoyé svp... » et que l'aperçu est parti en construction.
    "dm-optique": "clients/dm-optic/",
    # le dossier de travail de CINQ SENS — ouvert le 24/09 au soir, quand le cabinet a répondu « OK »
    # (17:04) au message de 16:53. Contrôle approfondi complet dans `clients/cinq-sens/dossier.md`.
    "cinq-sens-optique-medicale": "clients/cinq-sens/",
    # le dossier de recherche le plus complet de la campagne (RDAP + Wayback + captures de King)
    "k-vision-care": "clients/k-vision-care/",
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
        "stage": "closing",
        "stage_since": "2026-09-23",
        "Follow-up date": "2026-09-25",
        "last_send_state": "delivered",
        "Conversation_extra":
            "22/09 21:15 — LUI : « Présentiel ». · 22/09 21:20 — KING : « D'accord ça marche pour moi ». · "
            "22/09 21:24 — KING propose de se voir À SON LABORATOIRE (Carrefour Etoo) et demande le "
            "créneau : « plutôt disponible en matinée (vers 10h) ou en début d'après-midi (vers 14h30) ? » · "
            "23/09 13:30 — KING : le créneau de 10 h est pris par un autre rendez-vous client, il PROPOSE "
            "DONC 14h30 pour vendredi, joint LA GRILLE TARIFAIRE STANDARD (PDF, 1 page, 52 Ko) et pose LE "
            "PRIX : 150 000 FCFA — « la création de votre site bilingue complet (avec le formulaire de "
            "réservation WhatsApp direct) », 50 % d'acompte au démarrage et 50 % à la livraison finale. · "
            "23/09 21:42 — LUI, mot pour mot : « Bonsoir Mr » puis « 13h c'est bon pour moi » — IL CHOISIT "
            "13H, ni 10 h ni 14h30 (il répond à la place qu'on lui propose, pas à la question du créneau). · "
            "23/09 21:47 — KING accepte dans la minute : « D'accord ! C'est bien noté pour ce vendredi à "
            "13h à votre laboratoire. Bonne soirée et à vendredi ! » → RENDEZ-VOUS CONFIRMÉ PAR LES DEUX "
            "PARTIES, vendredi 25/09 à 13 h, à leur laboratoire (Carrefour Etoo, Bonamoussadi). "
            "Portique d'avant-envoi passé : le profil WhatsApp s'identifie « Uni Labo ».",
        "Notes_extra":
            "Vendredi 13 h : la seule séance de la journée où l'on peut ENCAISSER un acompte de 75 000 FCFA "
            "(Univers Optique, 10 h, c'est 50 000). Ce n'est plus une présentation : le prix est posé depuis "
            "le 23/09 13:30 et la grille tarifaire standard est déjà entre leurs mains — c'est elle qui fait "
            "foi en cas d'écart. à apporter : contrat Standard en deux exemplaires, grille corrigée, et de "
            "quoi montrer le formulaire de réservation. ⚠️ ÉCART À COMBLER, relevé le 23/09 au soir : la "
            "page en ligne (uni-labo.vercel.app, relue ce soir) est bilingue et complète — héros, 4 étapes, "
            "préparation par onglets, 4 familles d'analyses, résultats, FAQ — mais elle N'A AUCUN "
            "FORMULAIRE DE RÉSERVATION : ses 12 liens WhatsApp sont des questions (« demander le tarif »), "
            "pas un formulaire où le patient laisse ses informations. Or le message de 13:30 promet « la "
            "création de votre site bilingue complet (avec le formulaire de réservation WhatsApp direct) » "
            "à 150 000 FCFA. → CORRIGÉ LE 23/09 AU SOIR : LE FORMULAIRE EST CONSTRUIT "
            "(`demos/concept-unilabo-v1.html` + la copie hébergée `hosting/previews/unilabo/index.html`) : "
            "18 cases d'analyses (les 4 familles publiées + « autre / j'ai une ordonnance »), le nom, le "
            "moment souhaité (matin / après-midi / samedi matin / peu importe) et une précision facultative ; "
            "le bouton s'allume quand une analyse est cochée, le nom écrit et le moment choisi, et le "
            "message part DÉJÀ RÉDIGÉ vers leur WhatsApp (wa.me/237696139819). RIEN n'est enregistré sur le "
            "site : c'est le téléphone du patient qui envoie. RESTE UNE ACTION DE KING AVANT VENDREDI : "
            "redéployer le dossier `hosting/previews/unilabo/` sur le projet Vercel `uni-labo.vercel.app` "
            "(glisser-déposer, pas de CLI) — la page en ligne est celle du 18/09 et ne bougera pas seule — "
            "puis ouvrir la page sur son téléphone et le montrer EN DIRECT en séance. Jamais montrer "
            "l'ancienne page en disant que le formulaire est dedans. Détail relevé au passage : la page "
            "porte `noindex,nofollow` (voulu tant qu'elle n'est pas publique) — À RETIRER le jour où c'est "
            "LEUR site sur leur domaine, sinon aucune fiche Google ne sert à rien. "
            "23/09 ~22 h — LA PAGE EST RETRAVAILLÉE APRÈS AUDIT (consigne de King : « put that all into "
            "practice into the unilabo website » : relire les règles, auditer, améliorer). L'audit "
            "(`clients/uni-labo/AUDIT-2026-09-23.md`, 168 l.) et les notes de build "
            "(`clients/uni-labo/build-notes.md`) gardent la trace. Ce que la page porte désormais : une "
            "**fiche de prélèvement** en trois états (l'exemple au hero, la consigne dans « Avant de "
            "venir », et surtout **la fiche VIVANTE du formulaire** — elle se remplit à chaque case cochée "
            "et la ligne « Préparation » se déduit de LEURS propres textes) ; **quatre photos** « mise en "
            "situation » légendées comme §15.bis l'exige ; l'**état d'ouverture réel** calculé à l'heure "
            "de Douala dans la barre du haut (le point n'est plus décoratif) ; **l'erreur du formulaire "
            "expliquée** au lieu d'un bouton éteint sans raison ; `text-wrap:balance`, chiffres "
            "tabulaires, anneau de focus partout, cibles 44 px, `prefers-reduced-motion` ; schéma "
            "`MedicalLaboratory` + `FAQPage` (les 5 questions visibles) ; l'apostrophe du lien « Poser "
            "une question » corrigée (le message arrivait avec `j&#x27;ai`). Vérifié sans navigateur : "
            "portique 0 constat, analyseur HTML 415 textes / 0 constat, 8 blocs JS au compilateur, 0 faute, "
            "et deux harnais Node + faux DOM (formulaire dans 6 états, état d'ouverture sur 5 horloges, "
            "dans les deux langues). ⚠️ LE DOSSIER À DÉPLOYER A CHANGÉ : "
            "`hosting/previews/unilabo/` contient maintenant `index.html` + `og.jpg` + **`img/` "
            "(4 photos)** — glisser LE DOSSIER ENTIER sur Vercel, sinon la page s'affiche avec quatre "
            "cadres vides. La page en ligne reste celle du 18/09 : ni formulaire, ni fiche, ni photos. "
            "23/09 au soir — PASSE MOBILE (trois vidéos de King) + LA VERTICALE LABO (Thomas Digital) appliquées "
            "à la page : texte 16→17 px sur téléphone, boutons 48/52 px et bandeau 56 px, cases à cocher "
            "21 px, bandeau collant ramené à UNE action primaire (Prendre RDV) + WhatsApp + icône d'appel, "
            "dans le hero la fiche passe avant la photo sur téléphone, variantes légères des photos via "
            "srcset (482 Ko → 193 Ko sur un téléphone) et 3 graisses de police économisées, et le "
            "formulaire dit ce qui se passe après l'envoi. Principes : `AMK-DESIGN-SKILLS.md` §24 ; "
            "rapport complet : `research/YouTube-Lessons.md` lot [25]. Les deux harnais de test entrent "
            "au dépôt (`tools/qa/fake_dom.mjs` + `tools/qa/test_unilabo_page.mjs`, 23 assertions). "
            "⚠️ UNE QUESTION À POSER EN SÉANCE, ET ELLE VAUT UN LIVRABLE : « avez-vous une autorisation ou "
            "un agrément du ministère de la Santé, et une inscription à un contrôle de qualité externe ? » "
            "Les signaux de crédibilité sont ce qu'un patient cherche avant d'appeler (§24.4.3) et la "
            "plupart des laboratoires du quartier ne les affichent pas. On n'invente jamais un badge : on "
            "le demande, et si la réponse est oui, il va en haut de la page. Noter la réponse au CRM le "
            "soir même. "
            "24/09, nuit du 23 au 24 (commit `e936a03`, 00:03 à Douala) — LA PAGE A ÉTÉ REPRISE DE ZÉRO. King a regardé l'aperçu mobile et l'a refusé : "
            "« the page isn't mobile friendly the pictures seem to have spoiled everything redesign the "
            "site from scratch » (six captures d'anresco.com en main ; seconde référence : animate.bio). "
            "Nos outils étaient verts et la page était quand même rejetée : huit photographies, dont quatre "
            "en bandeaux, certaines avec du texte posé dessus — nos mesures portaient sur des éléments, son "
            "regard portait sur la composition. Nouvelle page : `demos/concept-unilabo-v2.html` (85 299 o au "
            "lieu de 94 509), hero SANS photo, CINQ photographies (une par famille d'analyses + la "
            "préparation) jamais derrière du texte et légendées « mise en situation », préparation en cinq "
            "accordéons natifs, mobile d'abord pour de vrai (une colonne par défaut, colonnes à partir de "
            "760 px), images recadrées au ratio déclaré : 167 Ko sur un téléphone (193 avant) et 394 Ko sur "
            "ordinateur (676 avant). Le contenu du laboratoire et ses deux blocs de JavaScript sont repris "
            "MOT POUR MOT (extraits par `tools/qa/extract_unilabo_js.py`, identiques au commit 2d2ffe4) : "
            "la refonte change la coquille, jamais le contrat. Vérifié : portique 0 constat (--strict rc=0), "
            "analyseur HTML 385 textes / 0 constat, 6 blocs JS / 0 faute, harnais 42 assertions vertes dont "
            "une suite 0 qui refuse une page ne portant plus le contrat, copie hébergée identique octet à "
            "octet. La règle est écrite en §25 de `AMK-DESIGN-SKILLS.md` : une photographie doit porter une "
            "seule signification ; sinon, on écrit une phrase à sa place. EN SÉANCE : montrer la REFONTE, "
            "jamais l'ancienne page. ACTION DE KING AVANT VENDREDI : redéployer le dossier "
            "`hosting/previews/unilabo/` ENTIER (index.html + og.jpg + img/, dix fichiers) sur le projet "
            "Vercel `uni-labo.vercel.app`. AJOUTÉ DANS LA FOULÉE : les liens WhatsApp statiques portent leurs DEUX "
            "messages et suivent la langue du visiteur, et la classe de bug de la version précédente "
            "(apostrophe encodée deux fois dans les liens de tarif) est fermée par un test.",
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


# ── LE VOCABULAIRE FERMÉ DE `reply_type` ────────────────────────────────────────────────────────
# Ajouté le 24/09 après l'avoir vu presque passer : l'entonnoir (`views.py`) compte les réponses
# humaines par `reply_type == "human"`. Une valeur libre n'est pas comptée, et **personne ne le voit**.
REPLY_TYPES = ("human", "auto", "none", "")


def doublons_de_cle(source: str) -> list:
    """Rend les clés écrites DEUX fois dans un littéral de dict de ce source.

    L'instrument, et pourquoi c'est celui-là : un dict Python **supprime** la clé dupliquée avant qu'on
    puisse la compter — la table assemblée ne dit plus rien. `Counter` sur un dict compte même autre
    chose (il lit les VALEURS comme des effectifs, et plante dès qu'une valeur est un dict : première
    version écrite le 24/09, plantée au premier essai). Le seul endroit où le doublon existe encore,
    c'est **le texte du fichier** — donc on lit le source avec `ast`, on regarde chaque dict assigné à
    un nom, et on compte ses clés constantes.
    """
    import ast
    tree = ast.parse(source)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
        dups = sorted({k for k in keys if keys.count(k) > 1})
        if dups:
            out.append(f"{names[0] if names else '?'} (ligne {node.lineno}) : {dups}")
    return out


def check_tables_sans_doublon() -> None:
    """Refuse une clé présente DEUX fois dans une table d'état.

    Pourquoi ce contrôle existe (24/09, vu en direct) : une entrée `"horizon-optique"` ajoutée à
    `REVISION_2409` alors qu'elle y était déjà — en Python la **dernière** gagne, la mienne mourait en
    silence, le CRM restait en `prospecting`, et rien ne le disait. Le remède n'est pas de faire
    attention : c'est de compter.
    """
    souci = doublons_de_cle(pathlib.Path(__file__).read_text(encoding="utf-8"))
    if souci:
        sys.exit("✗ clé(s) DUPLIQUÉE(S) dans un littéral de table — la seconde écrase la première en "
                 "silence :\n   " + "\n   ".join(souci))


def check_reply_types(out: list) -> None:
    """Refuse toute valeur hors vocabulaire : l'entonnoir se remplit ou se vide en silence, sinon."""
    bad = sorted({str(r.get("reply_type")) for r in out if str(r.get("reply_type") or "") not in REPLY_TYPES})
    if bad:
        sys.exit("✗ reply_type hors vocabulaire %s %s — valeurs admises : %s. Rien n'a été écrit."
                 % (bad, ":", " · ".join(x or "(vide)" for x in REPLY_TYPES)))


def _apply_jour(out: list) -> None:
    """Les relevés, dans l'ordre : 22/09 (soir), 23/09 (matin), 24/09 (le fil Le Cristallin), puis
    24/09 (la fiche Google d'Univers Optique, relue avant la réunion)."""
    _apply_state(out, JOUR_2209, "JOUR_2209")
    _apply_state(out, JOUR_2309, "JOUR_2309")
    _apply_state(out, FIL_2409, "FIL_2409")
    _apply_state(out, FICHE_2409, "FICHE_2409")
    _apply_state(out, GESTE_2409, "GESTE_2409")
    _apply_state(out, BATCH_2409, "BATCH_2409")
    _apply_state(out, ENVOI_2409, "ENVOI_2409")
    _apply_state(out, CORRECTIF_2409, "CORRECTIF_2409")
    _apply_state(out, REPONSE_2409, "REPONSE_2409")
    _apply_state(out, BATCH_2409_2, "BATCH_2409_2")
    _apply_state(out, ENVOI_2409_2, "ENVOI_2409_2")
    _apply_state(out, ENVOI_2409_3, "ENVOI_2409_3")
    _apply_state(out, ENVOI_2409_4, "ENVOI_2409_4")
    _apply_state(out, REPONSE_2409_DM, "REPONSE_2409_DM")
    _apply_state(out, REPONSE_2409_CS, "REPONSE_2409_CS")
    _apply_state(out, ECARTES_2409, "ECARTES_2409")



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
# ── LE 24/09 · LA RÉPONSE DE LE CRISTALLIN — et ce n'est pas une réponse commerciale ──────────
# 10:10 « Bonjour je vais te revenir » · 10:11 « Je suis malade » · 10:13 King répond par la santé,
# sans un mot du projet, sans relance, sans prix. Décision : ON NE RELANCE PAS un malade. Le prochain
# message est un message de santé, lundi 29/09, et le projet attend — le prix reste posé, il n'est ni
# accepté ni refusé. On ne touche à RIEN sur sa page (son « ne change encore rien sans mon ok » du
# 22/09 tient), et les trois compensations (WhatsApp Business, domaine 2027, fiche Google) restent
# parquées jusqu'au dégel.
FIL_2409 = {
    "le-cristallin": {
        "stage": "closing",            # rien n'est refusé : le prix est sur la table, le fil vit
        "stage_since": "2026-09-23",   # l'étape n'a pas bougé — seule l'attente change de nature
        "Follow-up date": "2026-09-29",
        "last_send_state": "delivered",
        "Reply": "24/09 10:10-10:11 — LUI : « Bonjour je vais te revenir » puis « Je suis malade ». "
                 "Ce n'est PAS une réponse commerciale : ni un oui, ni un non, ni une question sur "
                 "les 150 000. Conséquence écrite : aucune relance du projet d'ici lundi 29/09, et "
                 "le message du 29/09 parle de sa santé avant tout.",
        "Conversation_extra":
            "24/09 (capture du fil) — 10:10 LUI : « Bonjour je vais te revenir » · 10:11 LUI : "
            "« Je suis malade » · 10:13 KING, mot pour mot : « Bonjour Monsieur Messoua, Navré "
            "d'apprendre cela. Je vous souhaite un prompt rétablissement ! Prenez tout le temps de "
            "vous reposer, la santé passe avant tout. Le projet attendra votre retour en forme. Bon "
            "courage et à très bientôt ! » → AUCUNE QUESTION, AUCUN PRIX, AUCUNE DATE : la bonne "
            "réponse, et elle est déjà partie. Notre silence tient jusqu'au 29/09.",
        "Notes_extra":
            "État figé À DESSEIN : la page `lecristallin-concept.vercel.app` reste TELLE QUELLE "
            "(gel décidé par King le 23/09 : « on ne touche plus rien »), les trois compensations du "
            "§4 de `REVUE-CONTRATS-GRILLE-2026-09-23.md` (WhatsApp Business, domaine 2027, fiche "
            "Google) restent parquées jusqu'au paiement, et l'abonnement ne se propose QU'À la "
            "livraison payée. Message de santé prêt, à envoyer par King lundi 29/09 : "
            "`sales/Queue-CRISTALLIN-2026-09-29.md`.",
    },
}


# ── LE 24/09 · LA FICHE GOOGLE D'UNIVERS OPTIQUE — revendiquée par personne ─────────────────────
# Relecture publique de la fiche (Maps, place_id ChIJ2VaDG-QNYRARYgzvNnK0kRA) avant la réunion du 25/09
# à 10 h. Ce qui change : « gestionnaire inconnu » n'est plus l'inconnue — la page propose de la
# REVENDIQUER, donc c'est le cas ② du §9.3 de FICHE-GOOGLE-PROFILE.md, une fiche LIBRE. La première étape
# de tout le reste (champ site, réponse aux avis) est donc la revendication, et elle appartient à LUI :
# nous guidons, nous ne la prenons pas à sa place.
# Les avis : 6 · 3,3/5 — trois lisibles (8, 5 et 5 ans ; descriptifs ; aucune plainte ; aucune réponse du
# propriétaire), trois derrière « Plus d'avis ». Les textes d'avis NE SE COPIENT PAS dans le dépôt (ils
# portent des noms) : le scan a tourné sans nom et a REFUSÉ de conclure (3 < 5).
# Piège d'homonyme, chiffré pour ne plus jamais être confondu : « Univers Optique » à HAGONDANGE
# (Moselle) — 9 avis, tous 5/5, gérant « Cyril » (opticien.tel). Jamais le nôtre.
FICHE_2409 = {
    "univers-optique": {
        "Notes_extra":
            "24/09 — FICHE GOOGLE RELUE (Maps, `place_id:ChIJ2VaDG-QNYRARYgzvNnK0kRA`) : la page "
            "publique propose « **Revendiquer cet établissement** » (`business.google.com/create?fp=…) "
            "— la fiche n'est pilotée par personne (cas ② du §9.3 de `FICHE-GOOGLE-PROFILE.md`), donc "
            "« gestionnaire inconnu » est tranché. Champ « site web » toujours vide, 21 photos, "
            "horaires 08:00-18:00 (sam. 08:00-13:00). AVIS : 6 · 3,3/5, **3 lisibles** (8/5/5 ans, "
            "descriptifs, **aucune plainte**, aucune réponse du propriétaire) et 3 derrière « Plus "
            "d'avis (3) » — non lus, jamais cités. Scan lancé SANS LES NOMS sur les trois : **STOP, "
            "échantillon trop petit (3 < 5)** — `DETECTION-FUITES-2026-09-24.md` §9. ONOC (tableau du "
            "Littoral, ligne 94) : n° insc. **93** · arrêté **0346** · BAYANG BIHEN Calvin · Douala "
            "**699 252 874** (le numéro qu'on a déjà). HOMONYME Hagondange (Moselle) : 9 avis 5/5, "
            "gérant « Cyril » — jamais le nôtre.",
    },
}


# ── LE 24/09 · DÉCISION DE KING — la revendication de la fiche d'Univers Optique sera OFFERTE ────────
# « I have decided to help them set up/claim their google business profile for free if they agree. »
# Bornes écrites le même soir : c'est une MISE EN ROUTE, UNE FOIS (séance de revendication + informations
# de base : nom, catégorie, horaires, téléphone), pas une remise sur la page (100 000, 50/50 — le prix ne
# bouge pas d'un franc) et pas un mandat ouvert sur la fiche (compte Google, code/vidéo de vérification,
# réponses aux avis, photos, mensuel : à lui ou payants). Le geste DÉBLOQUE le travail payé, il ne le
# remplace pas — et il révèle le problème suivant : la fiche revendiquée montrera un champ « site » vide.
# Aucune promesse sur la méthode, le délai ou l'acceptation de Google. Séquence : annoncé tôt dans la
# séance, exécuté à la fin (après la prochaine étape datée), et pas exécuté du tout si la réunion refroidit.
GESTE_2409 = {
    "univers-optique": {
        "Notes_extra":
            "24/09 — DÉCISION DE KING : sa fiche Google (libre) se revendique AVEC lui, **offert une fois**, "
            "à la fin de la séance si la suite est datée. Le geste = revendication + nom/catégorie/horaires/"
            "téléphone depuis SES réponses ; **en dehors du geste** : compte Google, code de vérification, "
            "six réponses aux avis, photos, mensuel — aucune promesse sur la méthode, le délai ou "
            "l'acceptation de Google. Ce n'est PAS une remise (page à 100 000, 50/50). Effet miroir "
            "assumé : la fiche revendiquée montrera un champ « site web » vide. Question C2 du "
            "questionnaire réécrite (branche Univers ; mot de passe non demandé là où il n'existe pas).",
    },
}


# ── LE 24/09 (soir) · LE PREMIER LOT D'OUTREACH — préparé, RIEN N'EST ENVOYÉ ─────────────────
# Cinq opticiens de Douala jamais contactés, choisis dans le tableau de l'Ordre relu le 24/09
# (186 cabinets). Les notes ci-dessous existent pour qu'une prochaine séance sache que ce lot a
# été PRÉPARÉ et ne le prépare pas deux fois — et pour qu'aucun « premier message » ne reparte sur
# quelqu'un qu'on a déjà écrit. Le passage en `Contacted` se fait quand King rapporte l'envoi.
BATCH_2409 = {
    "maff-optique": {
        "Notes_extra":
            "24/09 — PREMIER LOT D'OUTREACH (préparé, PAS ENCORE ENVOYÉ) : numéro du tableau de "
            "l'Ordre (699 93 19 56), titulaire public MANFO Hélène. Recherche et message écrits dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "espace-lunetterie": {
        "Notes_extra":
            "24/09 — PREMIER LOT D'OUTREACH (préparé, PAS ENCORE ENVOYÉ) : numéro du tableau de "
            "l'Ordre (677 34 24 62), titulaire public BOUDJEU TCHAKOUNTE Edwige. Recherche et message écrits dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "megaoptic": {
        "Notes_extra":
            "24/09 — PREMIER LOT D'OUTREACH (préparé, PAS ENCORE ENVOYÉ) : numéro du tableau de "
            "l'Ordre (698 82 10 27), titulaire public MVENG ATEBA Zénon. Recherche et message écrits dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "m-dina-optic": {
        "Notes_extra":
            "24/09 — PREMIER LOT D'OUTREACH (préparé, PAS ENCORE ENVOYÉ) : numéro du tableau de "
            "l'Ordre (699 93 93 34), titulaire public BALLA Saïdou. Recherche et message écrits dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "cavisa-optique": {
        "Notes_extra":
            "24/09 — PREMIER LOT D'OUTREACH (préparé, PAS ENCORE ENVOYÉ) : numéro du tableau de "
            "l'Ordre (699 95 90 52), titulaire public DONGMO Jean René. Recherche et message écrits dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
}




# ── LE 24/09 · LE PREMIER LOT EST PARTI (11:56 → 12:10, captures de King) ────────────────────────
# Cinq messages, cinq numéros, cinq profils WhatsApp qui portent bien le nom de la boutique :
# « MAFF optique » (Business Account) · « Espace Lunetterie » (Business Account) · « MEGA Optique » ·
# « MÉDINA OPTIC » · « CAVISA OPTIQUE ». Tous livrés (✓✓). Aucune réponse au relevé du soir.
# Conséquence : la porte A des trois portes (§8b) est FRANCHIE pour les cinq — par King, sur
# l'application, sur des profils qui s'identifient. C'est la seule façon dont cette porte se franchit ;
# aucun raisonnement à distance ne la remplace.
ENVOI_2409 = {
    "maff-optique": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "delivered", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 11:56 — PREMIER LOT, ENVOYÉ par King. Message livré (✓✓). Profil WhatsApp : "
            "« MAFF optique », Business Account. Aucune réponse au relevé du soir ; toute réponse se "
            "traite dans l'heure et s'écrit dans `sales/Activity-Log.md`.",
    },
    "espace-lunetterie": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "delivered", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 12:00 — PREMIER LOT, ENVOYÉ par King. Message livré (✓✓). Profil WhatsApp : "
            "« Espace Lunetterie », Business Account. Aucune réponse au relevé du soir.",
    },
    "megaoptic": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "delivered", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 12:03 — PREMIER LOT, ENVOYÉ par King. Message livré (✓✓). Profil WhatsApp : "
            "« MEGA Optique » (numéro non enregistré dans le téléphone : le nom vient du profil, "
            "donc c'est bien la boutique). Aucune réponse au relevé du soir. Rappel du piège : un "
            "MEGA OPTIC de Limbe existe (Mveng Ateba Lionel, 698 915 192) — si la réponse vient de "
            "Limbe, on s'arrête.",
    },
    "m-dina-optic": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "delivered", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 12:08 — PREMIER LOT, ENVOYÉ par King. Message livré (✓✓). Profil WhatsApp : "
            "« MÉDINA OPTIC ». Aucune réponse au relevé du soir. Rappel : le 699 939 334 est partagé "
            "avec Star Optic dans le tableau de l'Ordre — un « ce n'est pas nous » arrête tout.",
    },
    "cavisa-optique": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "delivered", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 12:10 — PREMIER LOT, ENVOYÉ par King. Message livré (✓✓). Profil WhatsApp : "
            "« CAVISA OPTIQUE ». Aucune réponse au relevé du soir.",
    },
}


# ── LE 24/09 · DEUX CORRECTIFS DE DONNÉES (la file des « jamais contactés » mentait de 2 lignes) ──
# Disc et Tchaya ont REÇU le message 1 le 21/09 (vague opticiens) : ils sont en relance, et leur
# relance est écrite dans `sales/Send-Soir-2026-09-23.md`. Le CRM les portait pourtant
# « Contacted = No, stage = prospecting » — donc le calcul « 60 leads jamais contactés » les comptait
# encore, et un lot suivant aurait pu leur réécrire un PREMIER message.
# C'est la leçon COMOBIL qui revient : une décision qui doit changer un calcul vit ICI, pas dans un .md.
CORRECTIF_2409 = {
    "disc-optique-m-dicale": {
        "Contacted": "Yes", "wa_verified": "yes", "last_send_state": "sent",
        "stage": "qualifying", "stage_since": "2026-09-21",
        "Notes_extra":
            "CORRECTIF du 24/09 : le message 1 est PARTI le 21/09 (vague opticiens). Il est en "
            "RELANCE — relance écrite dans `sales/Send-Soir-2026-09-23.md`, à envoyer par King. Ne "
            "jamais lui réécrire un premier message.",
    },
    "tchaya-optique": {
        "Contacted": "Yes", "wa_verified": "yes", "last_send_state": "sent",
        "stage": "qualifying", "stage_since": "2026-09-21",
        "Notes_extra":
            "CORRECTIF du 24/09 : le message 1 est PARTI le 21/09 (vague opticiens). En RELANCE — "
            "relance écrite dans `sales/Send-Soir-2026-09-23.md`. Boutique de 1974, rue Pau, Akwa : "
            "ne jamais lui réécrire un premier message.",
    },
}


# ── LE 24/09 · DEUXIÈME LOT D'OUTREACH — OPTICIENS (préparé, RIEN N'EST ENVOYÉ) ──────────────────
# Numéro + recherche + premier message : `sales/Send-BATCH-2026-09-24-Opticiens-2.md`.
# Quatre des cinq hooks viennent d'un instrument dont on ne connaissait pas la portée :
# `google.com/maps/search/<nom>` rend la fiche ENTIÈRE — et surtout ce qui lui MANQUE, parce que
# Google énumère ses propres trous (« Ajouter un site Web », « Ajouter des horaires »…) et propose
# « Revendiquer cet établissement » quand la fiche n'est pas revendiquée. Le cinquième hook vient du
# PDF public du réseau de soins WTW / Société Générale (édition 15/09/2026) : il donne, pour chaque
# opticien de Douala, le quartier précis et un numéro — parfois différent de celui du registre.
BATCH_2409_2 = {
    "doyoan-optic": {
        "Website":
            "aucun site — fiche Google soignée (24/09) : 31 photos, 4,2/5 sur 6 avis, tous les "
            "horaires, réponses du propriétaire à chaque avis, et Google propose encore "
            "« Ajouter un site Web »",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT (préparé, PAS ENCORE ENVOYÉ) : numéro du registre de l'Ordre "
            "(653 85 27 49 = le numéro de sa fiche Google). Titulaire public MEZAFO Gildas. "
            "Recherche et message dans `sales/Send-BATCH-2026-09-24-Opticiens-2.md` ; vérifier le "
            "numéro sur WhatsApp avant d'envoyer (wa_verified = unknown).",
    },
    "bely-optique-m-dicale": {
        "Website":
            "aucun site — réseau de soins WTW / Société Générale (édition 15/09/2026) : "
            "« BELY OPTIQUE MEDICALE SARL · OPTIQUE · BONAMOUSSADI, SABLE · +237699895721 »",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT (préparé, PAS ENCORE ENVOYÉ) : numéro du registre (696 85 52 42), "
            "repli 699 89 57 21 (réseau de soins). Titulaire public NGATCHA ZOE Rosalie ; "
            "consultation oculaire déclarée + vente de montures. Recherche et message dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens-2.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "4m-optique-akwa": {
        "Website":
            "aucun site — fiche Google NUE et NON REVENDIQUÉE (24/09 : pas de numéro, pas "
            "d'horaires, pas de photo, « Revendiquer cet établissement ») ; réseau WTW / Société "
            "Générale (15/09/2026) : « 4M OPTIQUE SARL · AKWA, À CÔTÉ DE VISION CONFORT, AXE DOUALA "
            "BERCY · +237699092523 » ; fiche d'entreprise Yoooper : NIU M080900029528Y, "
            "675 01 07 82",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT (préparé, PAS ENCORE ENVOYÉ) : numéro du registre (679 27 06 64), "
            "repli 699 09 25 23 (réseau de soins). Titulaire public KAPTUE TAFFO Virginie. Trois "
            "numéros circulent — ne jamais dire que sa fiche Google n'existe pas : elle existe et "
            "elle est vide. Recherche et message dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens-2.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "horizon-optique": {
        "disqualification_reason": "",
        "Website":
            "aucun site — fiche DoualaTour (24/09) : « HORIZON Optique », Akwa RUE FOCH, opticien "
            "et horlogerie, sans photo, et le numéro n'apparaît qu'après avoir laissé ses propres "
            "coordonnées",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT (préparé, PAS ENCORE ENVOYÉ) : numéro du registre (677 44 74 17). "
            "Titulaire public DJEUMO FEUNOU Siméon. Passe RÉVISÉE le 24/09 : le « aucune vitrine à "
            "lui » du 22/09 était incomplet — une fiche DoualaTour existe (Akwa, rue Foch), donc la "
            "raison de l'écarter tombe. Piège vivant : « horizon eyes clinic » sur Google Maps "
            "(655 05 88 31, ouvert 24h/24) est un AUTRE établissement. Recherche et message dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens-2.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
    "fashion-vision": {
        "Website":
            "aucun site — Instagram @fashionvisiondouala (24/09 : 2 034 abonnés, 207 publications) "
            "+ fiche Mont-Pandi (Bonapriso, rue Afcodi, 08:00-18:00) ; l'e-mail publié sur sa fiche "
            "d'entreprise est amputé : fvisiondouala@oulock.fr",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT (préparé, PAS ENCORE ENVOYÉ) : numéro du registre (656 22 38 63, "
            "aussi publié comme WhatsApp sur sa fiche d'entreprise ; 2e ligne 691 77 76 57). "
            "Titulaire public PUILLE Nicolas. C'est le plus visible des cinq : le message ne lui "
            "apprend pas qu'il existe, il lui montre ce qui manque. Recherche et message dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens-2.md` ; vérifier le numéro sur WhatsApp avant "
            "d'envoyer (wa_verified = unknown).",
    },
}


# ── LE 24/09 · TROIS OPTICIENS ÉCARTÉS — la porte n° 2 de la vague (site vivant) ────────────────
# La vérification de 2 minutes qui évite un message gênant, appliquée au lot de ce soir : on a cherché
# un site AVANT d'écrire, et trois des candidats préparés le 21/09 en ont un.
ECARTES_2409 = {
    "lyfyoptic": {
        "Website":
            "lyfyoptic.com — VIVANT (24/09) : vitrine + boutique, adresse 15086 Akwa Bonadibong et "
            "numéro 699 98 06 66, les DEUX identiques au CRM",
        "disqualification_reason":
            "site vivant (lyfyoptic.com) — hors cible, comme Vision Care Center et Original Optique "
            "(vérification du 24/09)",
        "Notes_extra":
            "24/09 — ÉCARTÉ : le site est bien le sien (même adresse, même numéro, page Facebook "
            "« Lyfy-optic »). Ne pas lui proposer de vitrine.",
    },
    "cristalys-optic": {
        "Website":
            "cristalysoptic.com — VIVANT (24/09) : deux magasins (Bonapriso « Bonadouma Home » et "
            "Bonamoussadi « Super Marché Carrefour »), page Facebook 230 likes ; le site publie "
            "677 69 23 73 / 691 91 64 12 / 676 20 02 80, pas la ligne 690 94 51 50 du registre",
        "disqualification_reason":
            "enseigne avec site vivant (cristalysoptic.com) — hors cible JUSQU'À VÉRIFICATION que la "
            "ligne 690 94 51 50 est bien la même enseigne (vérification du 24/09)",
        "Notes_extra":
            "24/09 — ÉCARTÉ (sous réserve) : enseigne établie depuis 2003, site vivant. Si King "
            "confirme que 690 94 51 50 est une autre boutique du même nom, la raison tient ; sinon "
            "on rouvre.",
    },
    "gift-optical": {
        "Website":
            "giftopticalsarl.com — DÉCLARÉ sur sa propre fiche d'entreprise (Yoooper, « Gift Optical "
            "Sarl », numéro WhatsApp 237675521735, gift.optical@gmail.com) ; le domaine n'a PAS "
            "répondu au test du 24/09 (ni vivant constaté, ni mort constaté)",
        "disqualification_reason":
            "site déclaré sur sa fiche d'entreprise — hors cible TANT QUE King n'a pas tranché "
            "(le domaine est muet au test du 24/09, mais un domaine muet n'est pas un domaine mort)",
        "Notes_extra":
            "24/09 — EN ATTENTE D'ARBITRAGE : la chaîne a des agences à Bertoua et Ngaoundéré (même "
            "source) et un domaine à son nom. À vérifier sur un téléphone avant tout envoi : si le "
            "site est mort, c'est un excellent prospect (hook du lien mort, comme MegaOptic) ; s'il "
            "vit, c'est un écarté de plus.",
    },
}


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


# ── LA RÉVISION DU 24/09 — elle s'applique APRÈS la passe du 22/09, et c'est voulu ───────────────
# La passe « vitrine » du 22/09 avait classé Horizon Optique « aucune vitrine à lui — hors profil
# d'envoi ». Le 24/09, sa fiche DoualaTour a été trouvée (Akwa, rue Foch, opticien + horlogerie) : la
# prémisse tombe, donc la conséquence aussi. Une correction qui doit changer un calcul vit ici, pas
# dans un .md — et elle doit passer APRÈS la passe qu'elle corrige, sinon la passe l'écrase en
# silence (c'est exactement ce qui vient d'arriver : le premier patch a été recouvert).
# ── LE TROISIÈME LOT D'OPTICIENS — 24/09, fin d'après-midi ─────────────────────────────────────
# King a envoyé trois des cinq. Deux portes fermées, et cette fois **elles ont d'autres numéros
# publiés** : Royal Optic (repli 691 219 986) et K Vision Care (deux autres numéros, dont celui du
# lien, qui contredit le texte de l'annonce). Les replis partent au §7 du dossier d'envoi.
# Heures non relevées ; accusés non relevés → `sent`, jamais `delivered`.
ENVOI_2409_3 = {
    "el-roi-optique-medicale": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — TROISIÈME LOT, ENVOYÉ par King (heure et accusé de réception non relevés). "
            "Numéro utilisé : 693 127 302. Repli publié toujours disponible : 670 790 215.",
    },
    "net-optique-medical": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — TROISIÈME LOT, ENVOYÉ par King (heure et accusé de réception non relevés). "
            "Numéro utilisé : 675 785 930. Aucun second numéro publié.",
    },
    "cabinet-optique-la-retine": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — TROISIÈME LOT, ENVOYÉ par King (heure et accusé de réception non relevés). "
            "Numéro utilisé : 695 474 364. Aucun second numéro publié.",
    },
    "royal-optic-bali": {
        "Contacted": "No", "wa_verified": "no", "last_send_state": "not_sent",
        "wa_number_note": "WHATSAPP INDISPONIBLE au 676 250 409 (constaté par King, 24/09). "
                          "REPLI PUBLIÉ : 691 219 986 — à vérifier dans l'application avant d'envoyer.",
        "Notes_extra":
            "24/09 — TROISIÈME LOT : ENVOI IMPOSSIBLE sur le numéro principal. WhatsApp refuse "
            "676 250 409. Contrairement à Horizon, la boutique publie un SECOND numéro : 691 219 986. "
            "Étape suivante : ouvrir ce numéro dans l'application et lire le nom du profil ; si c'est "
            "Royal Optic, envoyer le même message (§7 du dossier d'envoi).",
    },
    "k-vision-care": {
        # ⚠️ LE NUMÉRO CHANGE : 677 077 459 (annuaire, injoignable) → **677 077 159**, celui que King a
        # ouvert dans l'application le 24/09 à 14:14 (profil « K Vision Care », Business Account) et
        # celui que leur PROPRE ancien site publiait dans ses liens WhatsApp. `wa_verified = "yes"` :
        # le numéro est bien à eux. Mais **le chat n'est pas ouvert** — voir `last_send_state`.
        "Contacted": "No", "wa_verified": "yes", "wa_number": "677 077 159",
        "last_send_state": "not_sent",
        "wa_number_note": "⚠️ 695 865 346 N'EST PAS À EUX : Mont-Pandi le publiait comme « repli », mais le "
                          "registre ONOC donne ce numéro-là — à un chiffre près — à **Optimat Vision Sarl** "
                          "(ligne 111 : 699 86 53 46). Quatrième anomalie du même annuaire en deux jours : "
                          "on ne recopie jamais un numéro d'annuaire. "
                          "NUMÉRO CONFIRMÉ : 677 077 159 (profil « K Vision Care », Business Account, "
                          "vu par King le 24/09 14:14 ; même numéro dans les liens de leur propre site). "
                          "⚠️ Le bouton « Message » n'apparaît pas sur la fiche — le chat n'est pas "
                          "ouvert ; les appels vocaux sont proposés. Portes restantes : SMS · appel · "
                          "e-mail kvisioncare05@gmail.com.",
        "site_url": "kvisioncare.com — DOMAINE À EUX, SITE HORS LIGNE (ERR_SSL_PROTOCOL_ERROR)",
        "Notes_extra":
            "24/09 — TROISIÈME LOT : ENVOI IMPOSSIBLE. WhatsApp refuse d'abord 677 077 459 (numéro "
            "d'annuaire) ; King ouvre ensuite 677 077 159 dans l'application : le profil est bien « K "
            "Vision Care », mais le chat n'est pas ouvert (pas de bouton Message, appels vocaux "
            "proposés). ⚠️ **Prospect de premier ordre** : ils ONT un domaine payé jusqu'au 17/08/2027 "
            "(RDAP Verisign : enregistré 17/08/2024 chez Hostinger, renouvelé le 18/08/2026) et un vrai "
            "site WordPress que la Wayback a capturé 14 fois entre le 17/08/2024 et le 12/07/2025 — "
            "aujourd'hui le DNS est sur NS1.DNS-EXPIRED.COM et le site ne s'ouvre plus. Leur ancien site "
            "publiait : montures à partir de 10 000 F, lunettes médicales à partir de 25 000 F, "
            "« nous acceptons toutes les assurances », trois magasins, et le nom du responsable — "
            "**KAKEU Djounessi** (Général Manager / opticien réfractionniste). Dossier complet : "
            "`clients/k-vision-care/dossier.md`. ⚠️ Ne jamais reprendre les faux avis de leur ancien "
            "site (gabarits de thème : 1 860 / 1 630 / 2 100 avis, lorem ipsum, photos de banque "
            "d'images).",
    },
}


# ── LE LOT 4 EST PARTI — les cinq envois de King, 24/09/2026 entre 15:15 et 15:31 ────────────────
# Preuve : `Screenshot_20260924-154540.png` (capture de King). Horaires de la capture :
#   15:15 Cinq Sens · 15:16 SkyOptics · 15:18 Lumumba · 15:29 La Ligne Optic · 15:31 DM Optic.
# Quatre bulles portent ✓✓ (délivré), Lumumba un seul ✓ (parti, pas encore délivré).
# ⚠️ LE CONTRÔLE APPROFONDI A ÉTÉ FAIT APRÈS L'ENVOI — la règle est née le soir même (décision de
# King : « à partir de maintenant fais toujours des contrôles approfondis sur chaque prospect »).
# Résultat : SkyOptic et Cinq Sens ont en réalité des canaux (site, blog) — les affirmations de leurs
# messages sont FRAGILES. Si l'un des deux répond : ne pas répéter la phrase, pivoter sur ce qui
# manque vraiment (horaires à jour, catalogue, bouton WhatsApp). MESSAGES §5, RESEARCH-STANDARD §8c.
ENVOI_2409_4 = {
    "cinq-sens-optique-medicale": {
        "Contacted": "Yes", "stage": "qualifying", "last_send_state": "delivered",
        "Conversation_extra":
            "24/09 — message 1 parti à 15:15 (capture de King : ✓✓). ⚠️ Contrôle approfondi APRÈS "
            "l'envoi : le cabinet a un Blogspot (dernier article 2021), une page Facebook, un compte X "
            "et une vidéo YouTube de 2020 — la phrase « dans les mots de quelqu'un d'autre » est "
            "FRAGILE. Si réponse : ne pas la répéter, pivoter sur les horaires à jour et le catalogue.",
    },
    "skyoptic-akwa": {
        "Contacted": "Yes", "stage": "qualifying", "last_send_state": "delivered",
        "Conversation_extra":
            "24/09 — message 1 parti à 15:16 (capture de King : ✓✓). ⚠️ Contrôle approfondi APRÈS "
            "l'envoi : ETS SKY OPTICS a un SITE VIVANT — `skyoptics.shop` — avec DEUX boutiques (Akwa, "
            "Boulevard de la République face Beneficial · Bonamoussadi, rond-point Maetur face Ola "
            "Energy) et trois numéros (698 18 42 82 · 698 86 46 93 · 653 98 32 09). Le message dit "
            "« un patient ne les voit nulle part » : FAUX. Si réponse : ne pas répéter, pivoter sur ce "
            "qui manque vraiment (horaires, catalogue à jour, bouton WhatsApp).",
    },
    "lumumba-optique-medicale": {
        "Contacted": "Yes", "stage": "qualifying", "last_send_state": "sent",
        "Conversation_extra":
            "24/09 — message 1 parti à 15:18 (capture de King : un seul ✓, pas encore délivré). "
            "Contrôle approfondi : deux pages Facebook confirmées (« Lunettes Lumumba » · « Lumumba "
            "Optique Medicale », 615 mentions J'aime) + une fiche d'annuaire (APIE) qui le situe **en "
            "face Parcours VITA, Bonamoussadi** — PAS Makepe : le message parle de Makepe, à corriger "
            "si réponse. Autre numéro publié : 656 183 349.",
    },
    "la-ligne-optic-akwa": {
        "Contacted": "Yes", "stage": "qualifying", "last_send_state": "delivered",
        "Conversation_extra":
            "24/09 — message 1 parti à 15:29 (capture de King : ✓✓). Contrôle approfondi : fiche "
            "Mont-Pandi (Akwa, Boulevard de la Liberté — consultation, réfraction, visagiste, conseil). "
            "Le message dit « le seul endroit où votre nom est écrit, c'est le tableau de l'Ordre » — "
            "à nuancer si réponse (la fiche annuaire existe, mais elle n'est pas à eux).",
    },
    "dm-optique": {
        "Contacted": "Yes", "stage": "qualifying", "last_send_state": "delivered",
        "Conversation_extra":
            "24/09 — message 1 parti à 15:31 (capture de King : ✓✓). Contrôle approfondi : rien de "
            "solide — une petite annonce de 2019 (« DM optometrie », afribobo, 2 500 F la consultation) "
            "qui n'est peut-être même pas eux. Le message (« on ne vous trouve pas ») tient.",
    },
}


# ── LE DEUXIÈME LOT D'OPTICIENS — 24/09, après-midi ────────────────────────────────────────────
# King a envoyé quatre des cinq messages préparés. Le cinquième est tombé sur une porte fermée :
# **WhatsApp refuse le 677 44 74 17 de Horizon Optique** (« indisponible »). Rien n'est envoyé à
# Horizon, et on ne réessaie pas sur ce numéro : la route de repli (SMS ou appel) est préparée dans
# `sales/Send-BATCH-2026-09-24-Opticiens-2.md` §6.
# Heures : King n'a pas relevé l'heure de chaque envoi (contrairement au lot 1, qui a des captures) ;
# on l'écrit telle quelle plutôt que d'inventer une heure.
# Accusés de réception (✓✓) : non relevés à cette heure → `last_send_state = "sent"`, pas "delivered".
ENVOI_2409_2 = {
    "doyoan-optic": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT, ENVOYÉ par King (heure non relevée). Accusé de réception non relevé "
            "à cette heure. Toute réponse se traite dans l'heure et s'écrit dans `sales/Activity-Log.md`.",
    },
    "bely-optique-m-dicale": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT, ENVOYÉ par King (heure non relevée). Numéro utilisé : le principal "
            "(696 85 52 42) ; le repli 699 89 57 21 n'a pas eu à servir.",
    },
    "4m-optique-akwa": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT, ENVOYÉ par King (heure non relevée). Numéro utilisé : 679 27 06 64 ; "
            "replis disponibles (699 09 25 23 du PDF WTW, 675 01 07 82 de l'annuaire d'entreprises).",
    },
    "fashion-vision": {
        "Contacted": "Yes", "Contact channel": "WhatsApp", "wa_verified": "yes",
        "last_send_state": "sent", "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT, ENVOYÉ par King (heure non relevée). Numéro utilisé : 656 22 38 63.",
    },
    "horizon-optique": {
        # Ni `disqualification_reason` ni `stage` ici : la passe « vitrine » du 22/09 s'exécute APRÈS
        # cette table et réécrirait la raison. Le fait vit dans `wa_number_note` et `Notes_extra`.
        "Contacted": "No", "Contact channel": "WhatsApp indisponible — SMS ou appel à tenter",
        "wa_verified": "no", "last_send_state": "not_sent",
        "wa_number_note": "WHATSAPP INDISPONIBLE au 677 44 74 17 (constaté par King, 24/09) — numéro lu "
                          "dans le registre de l'Ordre ; aucun second numéro trouvé.",
        "Notes_extra":
            "24/09 — DEUXIÈME LOT : ENVOI IMPOSSIBLE. WhatsApp refuse le 677 44 74 17 (« indisponible »). "
            "Aucune autre trace de la boutique : pas de fiche Google, une fiche DoualaTour dont le numéro "
            "se cache derrière un formulaire, et rien dans les annuaires testés ce jour (businesslist 404, "
            "recherche doualatour sans résultat ; les « Horizon Optique » de Dakar, Grenoble, Tanger et "
            "Verny sont des homonymes, écartés). ⚠️ Un numéro sans WhatsApp reste souvent une ligne "
            "valide : la route de repli est un SMS court ou un appel, scripts prêts dans "
            "`sales/Send-BATCH-2026-09-24-Opticiens-2.md` §6. Ne pas réessayer sur WhatsApp sans nouveau numéro.",
    },
}


# ── LA PREMIÈRE RÉPONSE DU LOT 1 — 24/09, 13:16 ────────────────────────────────────────────────
# M. Dongmo a regardé l'aperçu (https://cavisa.vercel.app/) et a écrit, mot pour mot :
# « Beaucoup de manquement mais c'est appréciable. »
# Ce n'est pas un refus : c'est un client qui a ouvert la page, l'a jugée, et demande le reste.
# Ce que la page laisse volontairement vide — son adresse et ses horaires — est exactement ce qu'il
# appelle « manquement ». On ne devine pas sa liste : on la lui demande, avec les quatre points que
# nous savons manquants. La réponse est écrite dans `sales/Reponse-CAVISA-2026-09-24.md`.
REPONSE_2409 = {
    "cavisa-optique": {
        # ⚠️ `reply_type` a un VOCABULAIRE FERMÉ : `human` · `auto` · `none` · vide.
        # `views.py` compte les réponses humaines sur l'égalité stricte `== "human"` : une valeur
        # écrite en prose (« positive — demande de compléments ») laisse la réponse HORS de
        # l'entonnoir, sans erreur et sans avertissement. Attrapé le 24/09 en relisant FUNNEL.md.
        # La nuance vit dans `Conversation`, jamais dans cette case.
        "Contacted": "Yes", "Reply": "Yes", "reply_type": "human",
        "Demo made": "Yes",
        "last_send_state": "replied", "stage": "demo", "stage_since": "2026-09-24",
        "Conversation_extra":
            "24/09 13:09 — King envoie le lien de l'aperçu (https://cavisa.vercel.app/), avec la carte "
            "de lien WhatsApp (titre + description : ils se sont affichés, la vignette non — `og:image` "
            "était encore commenté, corrigé depuis : redéploiement nécessaire). "
            "24/09 13:16 — RÉPONSE DE M. DONGMO, mot pour mot : « Beaucoup de manquement mais c'est "
            "appréciable. » Ni oui, ni non : il a regardé et il veut le reste. Réponse préparée le jour "
            "même (`sales/Reponse-CAVISA-2026-09-24.md`) : remercier, nommer les deux lignes que la "
            "page n'invente pas (adresse exacte, horaires), et lui demander ses quatre compléments "
            "(adresse + repère · horaires · ce qui manque dans nos services, marques et solaires · "
            "2-3 photos de la boutique · décision sur les prix). "
            "⚠️ Le message d'envoi du 13:09 promettait « votre localisation » et « vos services et "
            "horaires » : la page, elle, les affiche « à confirmer » — c'est très probablement ce "
            "qu'il a vu comme manquement. Leçon écrite dans `sales/MESSAGES-2026-09-23-PERSUASION.md` §2.",
    },
}


# ── LA DEUXIÈME RÉPONSE DU LOT 4 — 24/09, 15:54 ─────────────────────────────────────────────────
# M. Domche Noumbi (DM OPTIC) répond au message de 15:31, mot pour mot : « Ok Envoyé svp... »
# C'est un OUI sur le principe : envoyez l'aperçu. Aucune donnée de cabinet en plus — l'adresse et les
# horaires restent introuvables — donc l'aperçu est bâti UNIQUEMENT sur ce qui est vérifié : le registre
# de l'Ordre (inscription 021/2016, arrêté 0382, titulaire M. Domche Noumbi, Douala), le numéro, et le
# fait qu'aucune page publique n'existe. Les six champs manquants sont écrits « à confirmer » SUR la page.
# Le contrôle approfondi (règle de King du 24/09, MESSAGES §5) a été refait AVANT d'écrire — six
# recherches, verdict écrit : rien d'autre n'existe publiquement sur ce cabinet.
REPONSE_2409_DM = {
    "dm-optique": {
        "Contacted": "Yes", "Reply": "Yes", "reply_type": "human",
        "Demo made": "Yes",
        "last_send_state": "replied", "stage": "demo", "stage_since": "2026-09-24",
        # le profil a été vu : c'est sur WhatsApp qu'il a répondu, et la capture de King montre le nom
        # affiché « DM OPTIC ». On ne remplit `wa_verified` que sur une preuve — celle-ci en est une.
        "wa_verified": "yes", "profile_name_seen": "DM OPTIC",
        "value_kept":
            "Le registre de l'Ordre comme seule matière vraie : inscription 021/2016, arrêté 0382, "
            "titulaire M. Domche Noumbi, ville, un numéro — et la carte d'identité du cabinet en premier écran.",
        "value_discarded":
            "Aucune adresse, aucun horaire, aucun prix, aucune marque, aucune photo inventés : six champs "
            "écrits « à confirmer » sur la page, et deux images d'illustration légendées « mise en situation ».",
        "dossier": "clients/dm-optic/",
        "site_url": "https://dmoptic-2.vercel.app", "site_checked_on": "2026-09-24",
        "Conversation_extra":
            "24/09 15:31 — message 1 parti (capture de King : ✓✓). "
            "24/09 15:54 — RÉPONSE DE M. DOMCHE NOUMBI, mot pour mot : « Ok Envoyé svp... » Deux mots : "
            "envoyez-la. Aperçu construit le soir même (demos/concept-dmoptic-v1.html, gabarit + "
            "demos/build_dmoptic.py + hosting/previews/dmoptic/). "
            "CONTRÔLE APPROFONDI AVANT ÉCRITURE (règle du 24/09) : ONOC ligne 102 = seule source du "
            "cabinet ; `dmoptique.com` et `dmoptic.com` existent mais ne servent rien, `dmoptique.cm` / "
            "`dmoptic.cm` inexistants ; aucun Blogspot, WordPress, YouTube, X, Instagram, Facebook ; "
            "aucune fiche d'annuaire ; une annonce afribobo de déc. 2019 (« DM optometrie », 2 500 F, "
            "publiée par un particulier) NON retenue comme fait — elle n'est pas recoupée. Le nom du "
            "titulaire apparaît en mars 2023 dans la liste des opticiens de Douala citée par Echos Santé. "
            "⚠️ Ne jamais écrire d'adresse ni d'horaire pour ce lead tant qu'il ne les a pas donnés. "
            "24/09 17:05 — LE LIEN EST PARTI. Les mots de King sur le fil, mot pour mot : « Le voici ! "
            "Vous pouvez cliquer directement… » (capture à l'appui) — sur https://dmoptic-2.vercel.app/ (King a déployé le dossier "
            "sur un second projet Vercel ; l'ancienne adresse `dmoptic.vercel.app` sert encore la v1). "
            "La page en ligne est bien la v2.1 (vérifiée par lecture du HTML servi le 24/09 au soir) : "
            "services, vitrine des montures, six questions. En attente de son retour — aucune relance.",
    },
}


REPONSE_2409_CS = {
    # ── 24/09, 16:53 → 17:04 — CINQ SENS RÉPOND « OK » AU MESSAGE DU LOT 4 ───────────────────────────
    # Séquence exacte, sur capture de King : 15:15 le message du lot 4 part (✓✓) ; 16:27 le cabinet
    # demande « Bonjour / A qui ai je honneur » ; 16:53 King se présente et propose d'envoyer l'aperçu ;
    # 17:04 « Ok ». Ce n'est ni un rendez-vous ni un prix : c'est un oui pour voir la page.
    # ⚠️ Le message de 16:53 disait « il n'existait pas encore de page officielle réunissant vos deux
    # cabinets ». FAUX au sens strict : leur blog Blogger existe, il mentionne les deux cabinets, et sa
    # dernière publication est du 15/10/2021. Ne JAMAIS répéter cette phrase ; l'angle vrai est
    # « votre blog s'arrête en octobre 2021 ». Le message de livraison est écrit en conséquence.
    "cinq-sens-optique-medicale": {
        "Contacted": "Yes", "Reply": "Yes", "reply_type": "human",
        "Demo made": "Yes",
        "last_send_state": "replied", "stage": "demo", "stage_since": "2026-09-24",
        # le nom affiché à l'écran est tronqué (« Référence Optique M... ») : on écrit ce qu'on a vu
        "wa_verified": "yes",
        "profile_name_seen": "Référence Optique M... (tronqué à l'écran)",
        "value_kept":
            "Ce qu'ils sont déjà : deux cabinets (Akwa et Brazzaville), des repères publiés par eux-mêmes "
            "(Collège King Akwa, snack le Kokotier, immeuble Flore service, carrefour Brazzaville, immeuble "
            "Michelin), sept services réels (examen de la vue, montures homme/femme, solaires, lentilles, "
            "prothèses oculaires, accessoires, livraison à domicile) et leurs propres phrases.",
        "value_discarded":
            "Aucune adresse inventée au-delà de leurs repères, aucun prix, aucune marque, aucun avis, "
            "aucun nom de responsable (inconnu) : les horaires sont écrits « annoncés » et restent hors du "
            "schéma, et les trois photos sont légendées illustrations.",
        "dossier": "clients/cinq-sens/",
        "site_url": "https://cinqsens.vercel.app", "site_checked_on": "2026-09-24",
        "Conversation_extra":
            "24/09 15:15 — lot 4 (✓✓). 16:27 — LUI : « Bonjour / A qui ai je honneur ». 16:53 — King se "
            "présente et propose l'aperçu. 17:04 — LUI : « Ok ». "
            "CONTRÔLE APPROFONDI AVANT ÉCRITURE (règle du 24/09) : blog Blogger vivant mais arrêté au "
            "15/10/2021 ; `cinqsens.cm` ne résout pas ; LinkedIn société (817 abonnés), X, YouTube (2020), "
            "Facebook ; deux annuaires concordants (Maligah, Mont-Pandi) ; 696 698 136 = numéro d'urgence "
            "qu'ils publient partout ET ligne 118 du registre ONOC du Littoral ; seconde ligne 655 163 365 "
            "(leurs publications) ; 694 408 495 (annuaire seul, non utilisé). "
            "⚠️ Ne jamais écrire « vous n'avez pas de page » : ils en ont une — morte depuis 2021. "
            "24/09 17:54 — **LE LIEN EST PARTI** : https://cinqsens.vercel.app/#top. King a déployé le "
            "dossier sur Vercel et écrit son propre message, en gardant l'angle daté (« le blog du cabinet "
            "ne publie plus depuis octobre 2021… les patients qui vous cherchent tombent sur des annuaires "
            "passifs ») et la liste courte de ce qui manque (horaires, marques, paiements et assurances, "
            "trois ou quatre photos, le nom à faire figurer). La page servie a été relue : c'est bien la "
            "**passe 2** (lueur du premier écran, raccourci « envoyer la photo de mon ordonnance », "
            "raccourci prothèses, six services dont « accessoires »). "
            "⚠️ Ce qui manquait au moment de l'envoi : `og:url` et `og:image` étaient VIDES, donc la carte "
            "du lien est partie sans vignette. Recollés sur l'adresse réelle et commités le même soir — "
            "**un seul redéploiement** suffit, et l'aperçu des partages suivants portera l'image. "
            "Aucune relance : la balle est chez lui.",
    },
}


REVISION_2409 = {
    # ── 24/09, 14:17 — LE PREMIER REFUS EXPLICITE DE LA CAMPAGNE ────────────────────────────────
    # Bely Optique Médicale répond, mot pour mot : « Non Merci ». `lost` et non `disqualified` : ils ne
    # sont pas écartés pour données fausses — ils ont dit non. Conséquence voulue : `records.py` ne
    # propose plus AUCUNE action sur ce lead (« Aucune. Lead écarté — motif dans le CRM »).
    # ⚠️ Le marqueur « FIL CLOS » n'est pas décoratif : `views.py` s'en sert pour sortir le lead de la
    # file « ⚡ Répondre d'abord », où il serait resté TOUS LES JOURS (une réponse `human` reste
    # « en attente » tant que rien ne dit le contraire). Voir le commentaire dans `reply_pending`.
    # ── 24/09 — DÉCISION DE KING : ON NE RELANCE PAS CE QUI N'A JAMAIS ÉTÉ OUVERT ────────────────
    # Mot pour mot : « Pas de relance pour Disc, Tchaya et Afrique Labo, ils n'ont ouvert aucun de mes
    # messages sur WhatsApp, c'est un signe clair qu'ils ne sont pas intéressés. »
    # Les trois avaient une échéance DANS `RELANCE_A_JOUR` (views.py) — échéance RETIRÉE le même jour :
    # sans ça, le plan du jour aurait continué à réclamer une relance que King vient d'interdire. C'est
    # le piège COMOBIL à l'envers : la prose dit « stop », la donnée calcule « relance ».
    # ⚠️ `parked` et non `lost` : personne n'a dit non. Un message jamais ouvert n'est pas une preuve
    # de désintérêt — c'est un signal (notifications coupées, ligne d'appoint, téléphone au magasin),
    # et King en a fait une règle de travail (`sales/MESSAGES-2026-09-23-PERSUASION.md` §4).
    # `records.py` n'engage alors AUCUNE action : seule une décision explicite de King peut rouvrir.
    "disc-optique-m-dicale": {
        "stage": "parked", "stage_since": "2026-09-24",
        "disqualification_reason": "message livré mais JAMAIS OUVERT (aucun accusé de lecture) — "
                                   "décision de King, 24/09 : aucune relance",
        "Notes_extra":
            "24/09 — relance 1/3 ANNULÉE avant envoi. Message 1 parti le 21/09 à 17:48, jamais ouvert. "
            "Si la boutique écrit d'elle-même un jour, le fil rouvre — sinon, plus rien.",
    },
    "tchaya-optique": {
        "stage": "parked", "stage_since": "2026-09-24",
        "disqualification_reason": "message livré mais JAMAIS OUVERT (aucun accusé de lecture) — "
                                   "décision de King, 24/09 : aucune relance",
        "Notes_extra":
            "24/09 — relance 1/3 ANNULÉE avant envoi. Message 1 parti le 21/09 à 17:47, jamais ouvert. "
            "Vitrine réelle (deux pages Facebook, opticien depuis 1974) : le dossier reste, la relance "
            "non. Si la boutique écrit d'elle-même, le fil rouvre.",
    },
    "afrique-labo-douala": {
        "stage": "parked", "stage_since": "2026-09-24",
        "disqualification_reason": "messages livrés mais JAMAIS OUVERTS (aucun accusé de lecture) — "
                                   "décision de King, 24/09 : aucune relance",
        "Notes_extra":
            "24/09 — la FU3 préparée (`sales/Send-Soir-2026-09-23.md` §③) NE PARTIRA PAS : annulée "
            "avant envoi. Deux relances avaient déjà été envoyées (FU1 19/09, FU2 21/09) et aucune "
            "n'a été ouverte. C'était la dernière touche prévue ; elle devient la décision écrite : "
            "on s'arrête. Vitrine à lui (`afriqlabo.com`) — le dossier reste tel quel.",
    },
    # ── 24/09 (soir) — LE SMS EST PARTI, ET IL EST PARTI AUTREMENT (récit de King : « message
    #    envoyé à K Vision et Bely »). WhatsApp n'offre pas de bouton « Message » sur cette fiche
    #    Business : c'est le SMS qui a ouvert la porte, au numéro confirmé 677 077 159. On ne marque
    #    PAS `delivered` : un SMS n'a pas d'accusé visible, et personne ne l'a relevé.
    "k-vision-care": {
        "Contacted": "Yes", "Contact channel": "SMS (WhatsApp Business sans bouton « Message »)",
        "wa_verified": "yes", "last_send_state": "sent",
        "stage": "qualifying", "stage_since": "2026-09-24",
        "Notes_extra":
            "24/09 (soir) — **SMS ENVOYÉ par King** au 677 077 159 (récit de King ce soir-là). "
            "Accusé non relevé : un SMS n'affiche pas de ✓✓ → `sent`, pas `delivered`. "
            "⚠️ Si la réponse ne vient pas, la suite naturelle est **l'APPEL** (§9.b du dossier "
            "d'envoi) — **jamais un second SMS identique** — et l'e-mail `kvisioncare05@gmail.com` est "
            "la troisième porte (§9.c). Rien d'automatique : King décide.",
    },
    "bely-optique-m-dicale": {
        "Reply": "Yes", "reply_type": "human", "last_send_state": "replied",
        "stage": "lost", "stage_since": "2026-09-24",
        "disqualification_reason": "refus explicite (« Non Merci », 24/09 14:17) — aucune relance, "
                                   "aucun réessai, aucune question",
        "wa_number_note":
            "⚠️ LE NUMÉRO QUI A REÇU LE MESSAGE N'EST PAS ÉTABLI — la capture de King montre le fil "
            "« BELY OPTIQUE MÉDI… » sans le numéro. Or le 696 85 52 42 n'était PAS sur WhatsApp le "
            "21/09 (vague 1 jamais partie, `Contacted=No`). L'envoi du 24/09 est donc très "
            "probablement passé par le repli 699 89 57 21 — celui que notre message citait. "
            "La fiche le dit au lieu d'affirmer : à confirmer par King.",
        "Conversation_extra":
            "24/09 13:16 — notre message part et il est livré (✓✓). C'était le PREMIER contact réel "
            "de cette boutique : le message du 21/09 n'était jamais parti (696 85 52 42 absent de "
            "WhatsApp). "
            "24/09 14:17 — RÉPONSE, mot pour mot : « Non Merci ». UNE HEURE après notre message. "
            "**Premier refus explicite de la campagne.** Accepté tel quel : la réponse de courtoisie "
            "est écrite (`sales/Reponse-BELY-2026-09-24.md` §① — remercier, se retirer, laisser la "
            "porte ouverte, ne rien redemander) et c'est le SEUL message qui part. "
            "**FIL CLOS** : après lui, plus rien, jamais. Si elle revient d'elle-même, le fil rouvre. "
            "24/09 (soir) — **RÉPONSE DE COURTOISIE ENVOYÉE par King** (récit de King le même soir). "
            "La variante employée n'a pas été précisée — les deux disent la même chose. La politesse "
            "est rendue, le fil reste clos, et l'engagement tient : **plus rien sur ce lead**, sauf si "
            "elle écrit elle-même.",
    },
    "horizon-optique": {
        "Website":
            "aucun site — fiche DoualaTour (24/09) : « HORIZON Optique », Akwa RUE FOCH, opticien "
            "et horlogerie, sans photo, et le numéro n'apparaît qu'après avoir laissé ses propres "
            "coordonnées",
        # 24/09 — DÉCISION DE KING : « on laisse tomber Horizon ». La tentative reste écrite (elle a
        # eu lieu), le prospect sort de la file, et la table est la DERNIÈRE appliquée — donc le seul
        # endroit où la passe « vitrine » du 22/09 ne recouvrira pas la raison.
        "stage": "disqualified", "stage_since": "2026-09-24",
        # ⚠️ dans une TABLE D'ÉTAT les clés sont des NOMS DE COLONNES : `decision` ne serait pas
        # remappé (la normalisation est déjà passée) et ferait REFUSER la construction.
        "Decision maker": "abandonné — King, 24/09",
        "disqualification_reason": "abandonné sur décision de King (24/09) — WhatsApp indisponible au "
                                  "677 44 74 17 et aucune autre trace de la boutique",
        "Notes_extra":
            "24/09 — ABANDONNÉ sur décision de King (« on laisse tomber Horizon, passons à la prochaine "
            "vague »). Le message préparé n'est jamais parti (WhatsApp indisponible) ; la route de repli "
            "(SMS + script d'appel) reste écrite dans `sales/Send-BATCH-2026-09-24-Opticiens-2.md` §6 sans "
            "être exécutée. Aucune relance, aucun réessai : si un numéro ou une fiche apparaît un jour, le "
            "lead repart de `prospecting`.",
    },
    # ── 24/09 (nuit) — LA PORTE A, PREMIERS RÉSULTATS DE KING SUR LE LOT 4 ──────────────────────
    # King a ouvert les numéros dans l'application : c'est la seule vérification qui compte (Horizon).
    "win-optic-plus": {
        "wa_verified": "no",
        "Notes_extra":
            "24/09 (nuit) — PORTE A VÉRIFIÉE PAR KING : 699 12 59 06 N'EST PAS SUR WHATSAPP. "
            "Le lot 4 prévoyait un repli SMS (1 segment) — dans l'ordre d'envoi, La Ligne Optic a pris "
            "sa place. Aucun second numéro publié : ne pas réessayer à l'aveugle (un SMS ou un appel "
            "restent possibles un autre jour, avec un message adapté).",
    },
    "golden-eyes-optic-douala": {
        "stage": "disqualified", "stage_since": "2026-09-24", "wa_verified": "yes",
        "disqualification_reason":
            "A DÉJÀ UN SITE VIVANT DÉDIÉ À DOUALA (opticiendouala.com) — catalogue, services, "
            "prise de rendez-vous WhatsApp sur 699 312 588, dépistage gratuit annoncé, agrément "
            "MINSANTÉ. Hors cible du lot 4 : il n'y a pas de page à construire.",
        "Notes_extra":
            "24/09 (nuit) — recherche approfondie demandée par King (« look deeper into golden eyes »). "
            "Ce qu'on croyait : « leur site parle de Yaoundé, Douala en une ligne ». Ce qui est vrai : "
            "leur filiale de Douala a sa PROPRE page moderne (opticiendouala.com) et son adresse à "
            "jour — Bonapriso, carrefour Hôtel de l'Air, à côté de la BICEC, face Pharmacie de l'Air — "
            "exactement l'affiche « Nouvelle Adresse ! Douala » envoyée par King "
            "(uploads/20260924_152507.jpg). ⚠️ PAS Bonamoussadi : affiche, nouveau site et ancien site "
            "disent tous Bonapriso ; ce sont les annuaires (Maligah) qui sont restés à « Bonanjo, "
            "Atrium, 2e étage ». C'est le prospect le MIEUX équipé de la liste — à revoir un jour avec "
            "un autre angle, jamais avec « il vous manque une page ». wa_verified=yes : profil vu.",
    },
}


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
    # 1e · le lot 3 du 24/09 (opticiens neufs de Mont-Pandi) + les deux fiches écartées.
    for p in _batch_2409_3_rows():
        out.append({"School": p["org"], **p})
    # 1f · le lot 4 du 24/09 au soir (registre ONOC, Littoral) — 7 neufs, porte A à vérifier.
    for p in _batch_2409_4_rows():
        out.append({"School": p["org"], **p})

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
    _apply_state(out, REVISION_2409, "REVISION_2409")
    check_reply_types(out)
    check_tables_sans_doublon()

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
