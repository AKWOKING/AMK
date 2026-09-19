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
         last_send_state="sent", follow_ups_sent="0",
         notes="Message 1 envoyé 17/09 13:24. FU1 prévue sam 19/09. Concept live : concept-afriquelabo-v1.vercel.app. "
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

    cols = headers + NEW_FIELDS
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
    noslug = [r for r in out if not r.get("slug")]
    if noslug:
        print(f"  ⚠ {len(noslug)} ligne(s) sans slug")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
