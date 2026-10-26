#!/usr/bin/env python3
"""Banc de `tools/outreach/scout.py` — le scout et le vérificateur des trois portes.

    python3 tools/outreach/test_scout.py

Chaque refus a son contre-exemple qui passe. La dernière famille est la seule qui compte : sur le **vrai**
CRM du 26/10, le vérificateur doit laisser passer **sept** pistes et pas huit, avec les noms attendus.
"""

from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scout import Piste, lit_crm, scout  # noqa: E402

CAS = []
CHAMPS = ["ID", "School", "City", "Decision maker", "Contacted", "stage", "wa_number",
          "profile_name_seen", "wa_verified", "Website", "Website status", "Notes", "source"]


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn

    return enveloppe


def piste(**kw) -> Piste:
    base = dict(ident="1", nom="Cabinet Test", ville="Douala", numero="699 00 00 00",
                profil="Cabinet Test", contacte=False, stage="prospecting",
                notes="", site="", statut_site="", decideur="Titulaire Test", source="directory")
    base.update(kw)
    return Piste(**base)


def crm_temp(lignes: list[dict]) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
    w = csv.DictWriter(f, fieldnames=CHAMPS)
    w.writeheader()
    for l in lignes:
        w.writerow({k: l.get(k, "") for k in CHAMPS})
    f.close()
    return Path(f.name)


# ── le cas sain ──────────────────────────────────────────────────────────────────────────────────

@cas("3/3 → ENVOI")
def _():
    p = piste(notes="Porte A du 25/10 : PROFIL BUSINESS « Cabinet Test », catalogue")
    assert (p.porte_a, p.porte_b, p.porte_c) == ("pass", "pass", "pass"), (p.porte_a, p.porte_b, p.porte_c)
    assert p.verdict == "ENVOI", p.verdict
    return "A/B/C vertes"


# ── porte A ─────────────────────────────────────────────────────────────────────────────────────

@cas("profil sans nom d'établissement → PAS-D'ENVOI (ligne personnelle)")
def _():
    p = piste(profil="", notes="PROFIL BUSINESS « X »")
    assert p.porte_a == "fail" and p.verdict == "PAS-D'ENVOI", (p.porte_a, p.verdict)
    return "refusé"


@cas("aucun numéro → PAS-D'ENVOI")
def _():
    p = piste(numero="", notes="PROFIL BUSINESS")
    assert p.porte_a == "fail"
    return "refusé"


# ── porte B ─────────────────────────────────────────────────────────────────────────────────────

@cas("profil simple, aucune preuve d'activité → KING-TRANCHE")
def _():
    p = piste(notes="Porte A du 25/10 : profil « Cabinet Test » avec photo.")
    assert p.porte_b == "inconnu" and p.verdict == "KING-TRANCHE", (p.porte_b, p.verdict)
    return "2/3, décision écrite requise"


@cas("site vivant et complet → HORS-CIBLE (§8c règle 6)")
def _():
    p = piste(statut_site="VIVANT", site="cabinet-test.com", notes="")
    assert p.porte_b == "hors-cible" and p.verdict == "HORS-CIBLE", (p.porte_b, p.verdict)
    return "hors cible"


@cas("site vivant mais incomplet → reste dans la cible")
def _():
    p = piste(statut_site="VIVANT mais incomplet", notes="")
    assert p.porte_b == "pass", p.porte_b
    return "accepté"


# ── porte C ────────────────────────────────────────────────────────────────────────────────────

@cas("acheteur « board » → porte C rouge, 2/3")
def _():
    p = piste(notes="PROFIL BUSINESS ; décision board", decideur="")
    assert p.porte_c == "fail" and p.verdict in ("KING-TRANCHE", "JAMAIS"), (p.porte_c, p.verdict)
    assert p.verdict == "KING-TRANCHE"
    return "2/3"


# ── le scout : ce qui entre et ce qui sort ─────────────────────────────────────────────────────

@cas("déjà contacté, disqualifié, parqué, sans numéro → exclus, avec la raison")
def _():
    chemin = crm_temp([
        {"ID": 1, "School": "Jamais touché", "wa_number": "699 00 00 01", "Contacted": "No", "stage": "prospecting"},
        {"ID": 2, "School": "Déjà touché", "wa_number": "699 00 00 02", "Contacted": "Yes", "stage": "prospecting"},
        {"ID": 3, "School": "Disqualifié", "wa_number": "699 00 00 03", "Contacted": "No", "stage": "disqualified"},
        {"ID": 4, "School": "Parqué", "wa_number": "699 00 00 04", "Contacted": "No", "stage": "parked"},
        {"ID": 5, "School": "Sans numéro", "wa_number": "", "Contacted": "No", "stage": "prospecting"},
    ])
    try:
        garde, exclu = scout(lit_crm(chemin))
    finally:
        chemin.unlink(missing_ok=True)
    assert [p.nom for p in garde] == ["Jamais touché"], [p.nom for p in garde]
    assert len(exclu) == 4, exclu
    raisons = {e["raison"] for e in exclu}
    assert raisons == {"déjà contacté", "étape « disqualified »", "étape « parked »", "aucun numéro au CRM"}, raisons
    return "1 retenue, 4 exclues avec raison"


# ── la seule famille qui compte : le vrai CRM ──────────────────────────────────────────────────

@cas("le CRM réel du 26/10 donne exactement sept ENVOI, et ce sont les bons")
def _():
    racine = Path(__file__).resolve().parents[2]
    garde, _ = scout(lit_crm(racine / "leads/CRM.csv"))
    envoi = sorted(p.nom for p in garde if p.verdict == "ENVOI")
    attendu = sorted(["ASS pour RRPHDD", "Bellevue Optique", "Capelli Optique Médicale",
                      "Ets Espace Médical", "Free Optic", "ISEE", "S.O.S Vision"])
    assert envoi == attendu, envoi
    tranche = [p for p in garde if p.verdict == "KING-TRANCHE"]
    assert len(tranche) == 10, len(tranche)
    return f"{len(envoi)} ENVOI · {len(tranche)} à trancher · {len(garde)} retenues"


def main() -> int:
    ko = 0
    for nom, fn in CAS:
        try:
            print(f"  ✓ {nom} — {fn()}")
        except AssertionError as e:
            ko += 1
            print(f"  ✗ {nom} — {e}")
        except Exception as e:  # noqa: BLE001
            ko += 1
            print(f"  ✗ {nom} — {type(e).__name__}: {e}")
    total = len(CAS)
    print(f"\n{'✓' if not ko else '✗'} {total - ko}/{total}")
    return 1 if ko else 0


if __name__ == "__main__":
    raise SystemExit(main())
