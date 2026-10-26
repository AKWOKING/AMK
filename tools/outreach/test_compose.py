#!/usr/bin/env python3
"""Banc de la fabrique — `tools/outreach/compose.py`.

    python3 tools/outreach/test_compose.py

Chaque refus a son contre-exemple. Les trois familles qui comptent : la réserve ne peut pas produire
de motif répété, un lot plein passe la porte avec zéro avertissement, et la fabrique refuse ce qu'un
envoi en volume ne pardonne pas — deux fois le même numéro, un fait qui n'existe pas.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "qa"))

import compose as c  # noqa: E402
from audit_outreach import SEQ, _n_grams, check, parse, words  # noqa: E402

RACINE = Path(__file__).resolve().parents[2]
CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def lead(nom="Cabinet Test", numero="699 00 00 01", profil="", stage="prospecting",
         contacte="No", quartier="Akwa", objet="d'un opticien de Douala") -> c.Lead:
    return c.Lead(cle=nom.lower().replace(" ", "-"), nom=nom, quartier=quartier, numero=numero,
                  profil=profil, stage=stage, contacte=contacte, objet=objet)


# ── la réserve ───────────────────────────────────────────────────────────────────────────────────

@cas("la réserve ne peut produire aucun motif répété (longueurs, débuts, fins)")
def _():
    fautes = c.verifie_reserves()
    assert not fautes, fautes
    return "4 phrases, 7 variantes, plafonds tenus"


# ── le lot ───────────────────────────────────────────────────────────────────────────────────────

@cas("un lot plein de 49 messages passe la porte : zéro bloquant, zéro avertissement")
def _():
    import subprocess
    out = Path("/tmp/_banc_compose.md")
    c.write(c.lit_crm(RACINE / "leads/CRM.csv"), out, 49,
            "banc", 0, None)
    r = subprocess.run([sys.executable, str(RACINE / "tools/qa/audit_outreach.py"),
                        str(out), "--strict"], capture_output=True, text=True)
    assert "TOTAL 0 bloquant(s) · 0 avertissement(s)" in r.stdout, r.stdout[-600:]
    return "49/49 propres"


@cas("deux messages ne partagent jamais douze mots, et tous tiennent entre 35 et 55 mots")
def _():
    leads = c.selection(c.lit_crm(RACINE / "leads/CRM.csv"))[:49]
    corps = c.assemble(leads)
    vus = [set() for _ in range(0)]
    grammes = []
    for l in leads:
        body = corps[l.cle]
        n = len(words(body))
        assert 35 <= n <= 55, (l.nom, n)
        g = _n_grams(body, SEQ)
        assert not any(g & autre for autre in grammes), l.nom
        grammes.append(g)
        vus.append(g)
    return f"{len(leads)} messages, aucune séquence partagée"


# ── les refus ────────────────────────────────────────────────────────────────────────────────────

@cas("déjà contacté, disqualifié, sans numéro → hors sélection")
def _():
    leads = [lead("A", contacte="Yes"), lead("B", stage="disqualified"), lead("C", numero="12345"),
             lead("D")]
    garde = c.selection(leads)
    assert [l.nom for l in garde] == ["D"], [l.nom for l in garde]
    return "1 retenu sur 4"


@cas("deux lignes, un seul numéro → la fabrique garde la première et écarte la seconde")
def _():
    leads = [lead("Cabinet Un", "699 00 00 01"), lead("Cabinet Deux", "699 00 00 01")]
    d = c.doublons(leads)
    assert len(d) == 1 and set(d[0][1]) == {"Cabinet Un", "Cabinet Deux"}, d
    return "doublon vu"


@cas("le métier du prospect choisit l'objet de l'offre — une école n'entend pas parler d'opticien")
def _():
    assert c.objet("Blessed Group of Schools") == "d'une école de Douala"
    assert c.objet("Laboratoire Biomedicam") == "d'un laboratoire de Douala"
    assert c.objet("Clinique des Cités") == "d'une clinique de Douala"
    assert c.objet("Capelli Optique Médicale") == "d'un opticien de Douala"
    return "4 métiers, 4 pages"


@cas("le quartier se réduit au premier segment — « Douala (Makepe BM, rue des pavés) » → Makepe BM")
def _():
    assert c.quartier("Douala (Makepe BM, rue des pavés)") == "Makepe BM"
    assert c.quartier("Douala") == "Douala"
    assert c.quartier("Douala (Simbock + Nomayos)") == "Simbock"
    return "3/3"


@cas("deux noms identiques ne déclenchent pas l'angle « nom » — on n'invente pas une contradiction")
def _():
    assert c.meme_nom("Bellevue Optique", "bellevueoptique") is True
    assert lead("Ets Espace Médical", profil="Optic Medical Favour and Joy").angle == "nom"
    return "1 refus, 1 acceptation"


@cas("l'ID du CRM n'est pas une clé : 152 lignes sur 190 n'en ont pas — on identifie par le slug")
def _():
    leads = c.lit_crm(RACINE / "leads/CRM.csv")
    assert len({l.cle for l in leads}) == len(leads), "clés en double"
    assert sum(1 for l in leads if not l.cle) == 0
    return f"{len(leads)} clés distinctes"


@cas("plus de 49 messages d'un coup → refus explicite, pas un lot silencieusement répétitif")
def _():
    try:
        c._assemblages(50)
    except ValueError as e:
        assert "49" in str(e)
        return "refusé"
    raise AssertionError("50 messages acceptés")


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
