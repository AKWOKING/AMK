#!/usr/bin/env python3
"""Banc du scout et du vérificateur — `tools/outreach/scout.py`.

    python3 tools/outreach/test_scout.py

Chaque refus a son contre-exemple. La dernière famille est la seule qui compte : sur le vrai CRM du
26/10, le vérificateur doit laisser passer **sept** pistes et pas huit, avec les bons noms.
"""

from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import scout  # noqa: E402

CAS = []
CHAMPS = ["ID", "School", "City", "Decision maker", "contact_name", "Contacted", "stage",
          "wa_number", "profile_name_seen", "wa_verified", "Website", "Website status", "Notes",
          "source", "source_detail", "slug"]


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def piste(nom="Cabinet Test", numero="699 00 00 01", profil="Cabinet Test", contact="Titulaire Test",
          stage="prospecting", contacte="No", capture="✅", vu='Business « Cabinet Test »',
          notes="") -> scout.Piste:
    return scout.Piste(slug=nom.lower().replace(" ", "-"), nom=nom, ville="Douala", numero=numero,
                       profil=profil, contact=contact, stage=stage, contacte=contacte,
                       source="directory", detail="", notes=notes, capture=capture, vu=vu,
                       intention="pass" if "business" in vu.lower() else "inconnu",
                       acheteur="pass" if contact else "inconnu")


def crm_temp(lignes: list[dict]) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
    w = csv.DictWriter(f, fieldnames=CHAMPS)
    w.writeheader()
    for l in lignes:
        w.writerow({k: l.get(k, "") for k in CHAMPS})
    f.close()
    return Path(f.name)


# ── les trois portes ────────────────────────────────────────────────────────────────────────────

@cas("3/3 → ENVOYER")
def _():
    p = piste()
    assert (p.porte_a, p.porte_b, p.porte_c) == ("pass", "pass", "pass")
    assert p.verdict == "ENVOYER"
    return "A/B/C vertes"


@cas("profil vu mais aucune preuve numérique datée → KING-TRANCHE (et pas « envoyé »)")
def _():
    p = piste(vu="profil « Cabinet Test »")
    assert p.porte_b == "inconnu" and p.verdict == "KING-TRANCHE", (p.porte_b, p.verdict)
    return "2/3 — King tranche"


@cas("profil sans nom d'établissement → PAS-ENVOYÉ (ligne personnelle)")
def _():
    p = piste(profil="", capture="⚠️", vu="photo de personne")
    assert p.porte_a == "ambigu" and p.verdict != "ENVOYER", (p.porte_a, p.verdict)
    return "on n'écrit pas « votre cabinet »"


@cas("numéro mort dans la capture → JAMAIS")
def _():
    p = piste(capture="⛔")
    assert p.porte_a == "fail" and p.verdict == "JAMAIS"
    return "pas de repli : ni SMS, ni appel"


@cas("aucun décideur nommé → la porte C manque, et le vérificateur dit laquelle")
def _():
    p = piste(contact="")
    assert p.porte_c == "inconnu" and p.verdict == "KING-TRANCHE"
    return "2/3, porte C"


# ── les exclusions du scout ────────────────────────────────────────────────────────────────────

@cas("déjà contactée, disqualifiée, perdue, sans numéro, refus écrit → exclues avec la raison")
def _():
    pistes = [piste("Jamais touchée"), piste("Déjà", contacte="Yes"), piste("Perdue", stage="lost"),
              piste("Disqualifiée", stage="disqualified"), piste("Sans numéro", numero=""),
              piste("Refus", notes="réponse écrite : Non merci")]
    garde, exclues = scout.scout(pistes)
    assert [p.nom for p in garde] == ["Jamais touchée"], [p.nom for p in garde]
    assert len(exclues) == 5
    return f"1 gardée, {len(exclues)} exclues"


@cas("l'ordre du scout est un ordre de preuve : 3/3 avant 2/3 avant 1/3")
def _():
    pistes = [piste("Une seule", profil="", capture="⚠️", vu="photo"),
              piste("Deux", vu="profil simple"),
              piste("Trois")]
    garde, _ = scout.scout(pistes)
    assert [p.nom for p in garde] == ["Trois", "Deux", "Une seule"], [p.nom for p in garde]
    return "3/3 → 2/3 → 1/3"


# ── la seule famille qui compte : le vrai CRM ─────────────────────────────────────────────────

@cas("le CRM réel du 26/10 donne exactement sept ENVOYER, et ce sont les bons")
def _():
    pistes = scout.lit_crm()
    garde, _ = scout.scout(pistes)
    envoi = sorted(p.nom for p in garde if p.verdict == "ENVOYER")
    attendu = sorted(["ASS pour RRPHDD", "Bellevue Optique", "Capelli Optique Médicale",
                      "Ets Espace Médical", "Free Optic", "ISEE", "S.O.S Vision"])
    assert envoi == attendu, envoi
    tranche = [p for p in garde if p.verdict == "KING-TRANCHE"]
    assert len(tranche) == 9, (len(tranche), [p.nom for p in tranche])
    return f"{len(envoi)} ENVOYER · {len(tranche)} à trancher · {len(garde)} gardées"


@cas("les sept ENVOYER portent chacun un fait daté, et deux noms différents du tableau sont vus")
def _():
    garde, _ = scout.scout(scout.lit_crm())
    envoi = [p for p in garde if p.verdict == "ENVOYER"]
    assert all("Business" in p.vu for p in envoi), [p.vu for p in envoi]
    noms = {p.nom for p in envoi}
    assert {"Ets Espace Médical", "ASS pour RRPHDD", "ISEE"} <= noms
    return "7 faits datés, 3 noms divergents"


@cas("le vérificateur signale les cabinets déjà écrits qui ne sont pas à 3/3")
def _():
    conflits = scout.contradictions(scout.lit_crm())
    assert conflits, "aucune contradiction vue — le lot volume devrait en produire"
    assert any("ENVOI-VOLUME" in c or "ENVOI-LOT" in c for c in conflits)
    return f"{len(conflits)} contradictions signalées"


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
