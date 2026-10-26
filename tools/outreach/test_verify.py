#!/usr/bin/env python3
"""Banc de `verify.py` — les trois portes, et le refus de deviner.

    python3 tools/outreach/test_verify.py

Ce qui est vérifié : une porte ne s'ouvre que sur une preuve datée, une porte fermée le reste, et un
cabinet qui a déjà un site dédié sort de la cible au lieu d'être félicité.
"""

from __future__ import annotations

import csv
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify  # noqa: E402

CAS = []
JOUR = date(2026, 10, 27)
CHAMPS = ["School", "City", "wa_number", "wa_verified", "Contacted", "stage", "Website",
          "Website status", "Last FB post", "Decision maker", "profile_name_seen", "Notes"]


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def crm(lignes: list[dict]) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
    w = csv.DictWriter(f, fieldnames=CHAMPS)
    w.writeheader()
    for l in lignes:
        w.writerow({k: l.get(k, "") for k in CHAMPS})
    f.close()
    return Path(f.name)


def preuve(nom: str, type_: str, texte: str = "", vu: str = "2026-10-25") -> verify.Preuve:
    return verify.Preuve(cle=verify.slug(nom), type=type_, texte=texte or type_, source="test", vu_le=vu)


def optique(**kw) -> dict:
    base = {"School": "Optique Test", "City": "Douala", "wa_number": "699 00 00 01",
            "wa_verified": "yes", "Contacted": "No", "stage": "prospecting",
            "Decision maker": "Titulaire Nommé"}
    base.update(kw)
    return base


def juge(lignes, preuves=()) -> verify.Piste:
    pistes = verify.applique_portes(verify.lit_crm(crm(lignes)), list(preuves), JOUR)
    return pistes[0]


# ── porte A ──────────────────────────────────────────────────────────────────────────────────

@cas("A : le CRM dit que King a vu le profil → la porte est ouverte")
def _():
    p = juge([optique()])
    assert p.a == "pass" and "wa_verified" in p.motifs["a"]
    return "pass"


@cas("A : un numéro vu mort le 25/10 ferme la porte, même si le CRM dit `yes`")
def _():
    p = juge([optique()], [preuve("Optique Test", "mort", "mort")])
    assert p.a == "fail" and p.verdict == "JAMAIS", (p.a, p.verdict)
    return "fail + JAMAIS"


@cas("A : un numéro jamais ouvert reste `inconnu` — il ne devient pas `pass` par politesse")
def _():
    p = juge([optique(wa_verified="unknown")])
    assert p.a == "inconnu" and p.verdict != "ENVOYER"
    return "inconnu"


# ── porte B ──────────────────────────────────────────────────────────────────────────────────

@cas("B : une page Facebook qui a posté il y a six mois ouvre la porte")
def _():
    p = juge([optique()], [preuve("Optique Test", "facebook", "dernier post 2026-04-10")])
    assert p.b == "pass", p.motifs["b"]
    return "pass"


@cas("B : une page dormante depuis 2021 ferme la porte")
def _():
    p = juge([optique()], [preuve("Optique Test", "facebook", "dernier post 2021-04-03", "2021-04-03")])
    assert p.b == "inconnu", p.motifs["b"]          # une preuve trop vieille n'ouvre rien
    p2 = juge([optique(**{"Last FB post": "2021-04-03"})])
    assert p2.b == "fail" and p2.verdict == "JAMAIS", (p2.b, p2.verdict)
    return "inconnu, puis fail via le CRM"


@cas("B : un profil WhatsApp Business « actif » compte, et il est daté")
def _():
    p = juge([optique()], [preuve("Optique Test", "whatsapp_business", "Business « Optique Test »")])
    assert p.b == "pass" and "2026-10-25" in p.motifs["b"]
    return "pass"


@cas("B : un site dédié en ligne met la ligne hors cible (§8c), il n'ouvre pas la porte")
def _():
    p = juge([optique(**{"Website": "optiquetest.com", "Website status": "vivant"})])
    assert p.site_vivant == "optiquetest.com"
    assert p.verdict == "HORS-CIBLE", p.verdict
    return "HORS-CIBLE"


@cas("B : « none found » dans la colonne Website n'est pas un site")
def _():
    p = juge([optique(**{"Website": "None found", "Website status": ""})])
    assert p.site_vivant == ""
    return "pas de site"


# ── porte C ──────────────────────────────────────────────────────────────────────────────────

@cas("C : un titulaire nommé ouvre la porte ; une clinique sans acheteur la ferme")
def _():
    assert juge([optique()]).c == "pass"
    clinique = optique(School="Clinique des Cités", **{"Decision maker": ""})
    p = juge([clinique])
    assert p.c == "fail" and "conseil" in p.motifs["c"]
    return "pass · fail"


# ── le verdict ──────────────────────────────────────────────────────────────────────────────

@cas("3/3 → ENVOYER · 2/3 → KING-TRANCHE · et le manque est nommé")
def _():
    trois = juge([optique()], [preuve("Optique Test", "facebook", "post 2026-05-01")])
    assert trois.verdict == "ENVOYER" and trois.portes == 3
    deux = juge([optique()])
    assert deux.verdict == "KING-TRANCHE" and "B intention" in deux.manque
    return "ENVOYER · KING-TRANCHE (B)"


@cas("la raison affichée est celle de la porte qui manque, pas celle d'une porte franchie")
def _():
    p = juge([optique(wa_verified="unknown", **{"Website": ""})],
             [preuve("Optique Test", "facebook", "post 2026-05-01")])
    assert p.a == "inconnu" and "WhatsApp" in p.raison_manque, p.raison_manque
    return "raison = porte A"


@cas("sur le vrai CRM, sept pistes ont les trois portes et aucune n'est hors cible")
def _():
    preuves = verify.lit_porte_a(verify.RACINE / "sales/PORTE-A-2026-10-25.md")
    pistes = verify.applique_portes(verify.lit_crm(verify.RACINE / "leads/CRM.csv"), preuves, JOUR)
    env = [p.nom for p in pistes if p.verdict == "ENVOYER"]
    assert len(env) == 7, env
    assert not [p for p in pistes if p.verdict == "HORS-CIBLE" and p.verdict == "ENVOYER"]
    assert "ISEE" in env and "Capelli Optique Médicale" in env
    return f"{len(env)} ENVOYER, dont ISEE et Capelli"


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
    print(f"\n{'✓' if not ko else '✗'} {len(CAS) - ko}/{len(CAS)}")
    return 1 if ko else 0


if __name__ == "__main__":
    raise SystemExit(main())
