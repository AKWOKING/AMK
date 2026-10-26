#!/usr/bin/env python3
"""Banc de `supply.py` — les numéros, la liste collée, et le plan qui refuse.

    python3 tools/outreach/test_supply.py

Deux familles : ce qui se normalise (et ce qui doit être refusé), et le plan qui ne doit jamais
promettre plus de messages qu'il n'y a de lignes.
"""

from __future__ import annotations

import csv
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import supply  # noqa: E402

CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def fichier(contenu: str, suffixe: str = ".csv") -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=suffixe, delete=False, encoding="utf-8", newline="")
    f.write(contenu)
    f.close()
    return Path(f.name)


def crm(lignes: list[str]) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
    f.write("ID,School,City,wa_number,Phone\n")
    for i, l in enumerate(lignes):
        nom, _, tel = (l.partition(" — ") + ("", ""))[:3] if " — " in l else (l, "", "")
        f.write(f'{i},"{nom}","Douala","{tel}",""\n')
    f.close()
    return Path(f.name)


# ── les numéros ────────────────────────────────────────────────────────────────────────────────

@cas("un numéro camerounais s'écrit de sept façons et se lit d'une seule")
def _():
    attendu = "699123456"
    for brut in ("699123456", "699 12 34 56", "699-12-34-56", "+237 699 12 34 56",
                 "00237699123456", "237699123456", "(237) 699123456"):
        assert supply.numero(brut) == attendu, (brut, supply.numero(brut))
    return "7 écritures → 1 numéro"


@cas("un numéro qui n'est pas un mobile est refusé, jamais deviné")
def _():
    for brut in ("", "123456789", "69912345", "6991234567", "23769912", "812345678"):
        assert supply.numero(brut) == "", (brut, supply.numero(brut))
    return "6 refus"


@cas("le même numéro avec un préfixe différent est un doublon")
def _():
    assert supply.numero("+237699123456") == supply.numero("00237699123456")


# ── la liste collée ───────────────────────────────────────────────────────────────────────────

@cas("une liste tabulée sans entêtes propres : les colonnes sont reconnues par leur contenu")
def _():
    f = fichier("Cabinet\tTéléphone WhatsApp\tQuartier\n"
                "Optique Alpha\t+237 699 11 22 33\tAkwa\n"
                "Vision Plus\t677 44 55 66\tBonapriso\n")
    lignes, refus = supply.lit_liste(f, "annuaire", "2026-10-26")
    assert not refus, refus
    assert [l.num for l in lignes] == ["699112233", "677445566"]
    assert lignes[0].ville == "Akwa"
    return "2 lignes, 0 refus"


@cas("une ligne sans nom ou sans numéro lisible entre par la porte de sortie")
def _():
    f = fichier("nom,tel\n,\nSans numéro,abc\nOptique Beta,699 77 88 99\n")
    lignes, refus = supply.lit_liste(f, "annuaire", "2026-10-26")
    assert len(lignes) == 1 and len(refus) == 1, (len(lignes), refus)
    return "1 gardée, 1 refus motivé, ligne vide ignorée"


@cas("un fichier collé dont les colonnes ne sont pas reconnaissables ne produit rien")
def _():
    f = fichier("a,b\n1,2\n")
    lignes, refus = supply.lit_liste(f, "annuaire", "2026-10-26")
    assert lignes == [] and refus and "colonnes" in refus[0]
    return "refus explicite"


@cas("un numéro déjà au CRM n'est pas recollé, et le doublon interne est écarté")
def _():
    base = crm(["Optique Déjà Là — 699 11 22 33"])
    f = fichier("nom,tel\n"
                "Optique Déjà Là,699112233\n"
                "Optique Neuve,677 00 00 01\n"
                "Optique Neuve bis,+237677000001\n"
                "Optique Autre,655 00 00 02\n")
    lignes, refus = supply.lit_liste(f, "annuaire", "2026-10-26")
    garde, doubl = supply.dedoublonne(lignes, base)
    assert [l.nom for l in garde] == ["Optique Neuve", "Optique Autre"], [l.nom for l in garde]
    assert len(doubl) == 2, doubl
    return "2 gardées, 2 écartées (CRM + interne)"


@cas("la liste de transit ne porte que les colonnes du CRM, et un slug par ligne")
def _():
    f = fichier("nom,tel,quartier\nOptique Gamma,699 12 12 12,Bali\n")
    lignes, _ = supply.lit_liste(f, "passage", "2026-10-26")
    out = Path(tempfile.mkdtemp()) / "staging.csv"
    supply.ecrit_transit(lignes, out)
    with out.open(encoding="utf-8") as fh:
        r = list(csv.DictReader(fh))
    assert list(r[0].keys()) == supply.ENTETES
    assert r[0]["Phone"] == "699 12 12 12" and r[0]["slug"] == "optique-gamma-1212"
    return "colonnes CRM, slug stable"


# ── extraire d'une page collée ────────────────────────────────────────────────────────────────

PAGE = """Clinique Dentaire Le Sourire (Bonamoussadi)
Cabinet dentaire, ouvert du lundi au samedi
WhatsApp : +237 699 12 34 56
Appeler : 233 42 11 22

OPTIQUE VISION PLUS (Akwa)
Lunetterie et examens de vue
Contactez-nous au 00237 677 88 99 00
Avis 4,6 (38 avis)
"""


@cas("une page collée rend ses mobiles, avec l'enseigne au-dessus et pas le bouton du site")
def _():
    lignes = supply.extrait(PAGE, "facebook", "2026-10-27")
    noms = [(l.nom, l.num) for l in lignes]
    assert noms == [("Clinique Dentaire Le Sourire (Bonamoussadi)", "699123456"),
                    ("OPTIQUE VISION PLUS (Akwa)", "677889900")], noms
    assert lignes[0].ville == "Bonamoussadi", lignes[0].ville
    return "2 mobiles, 2 enseignes, 1 fixe ignoré"


@cas("« WhatsApp : », « Contactez-nous au », « Avis » ne sont jamais pris pour un nom")
def _():
    for l in supply.extrait(PAGE, "facebook", "2026-10-27"):
        assert not re.match(r"(?i)^(whatsapp|contactez|appeler|avis)", l.nom), l.nom
    return "3 pièges évités"


@cas("un fixe (233 …) n'est pas un mobile : il n'entre pas")
def _():
    nums = [l.num for l in supply.extrait(PAGE, "facebook", "2026-10-27")]
    assert "233421122" not in nums
    return "fixe écarté"


@cas("un même numéro collé deux fois n'entre qu'une fois")
def _():
    assert len(supply.extrait("Optique A 699 11 22 33\nOptique B 699 11 22 33", "x", "2026-10-27")) == 1
    return "1 seule ligne"


@cas("une page sans numéro mobile ne produit rien, et le dit")
def _():
    assert supply.extrait("Belle page sans contact\nAucun numéro ici.", "x", "2026-10-27") == []
    return "0 ligne"


# ── le plan ───────────────────────────────────────────────────────────────────────────────────

@cas("un plan qui demande plus que le stock est refusé, avec le nombre manquant")
def _():
    texte, ok = supply.plan([20, 22], date(2026, 10, 27), {"3/3": 2, "2/3": 3, "1/3": 4})
    assert not ok
    assert "**impossible en l'état**" in texte
    return "refus, et le manque est chiffré"


@cas("un plan que le stock tient est accepté, et les preuves fortes partent en premier")
def _():
    texte, ok = supply.plan([10, 6], date(2026, 10, 27), {"3/3": 7, "2/3": 9, "1/3": 4})
    assert ok, texte
    assert "| 2026-10-27 | 10 | 7 | 3 | 0 |" in texte, texte
    return "7 à 3/3 en tête, puis 3 à 2/3"


@cas("le stock réel du 26/10 tient deux journées de 20 et 22, pas une troisième de 40")
def _():
    d = supply.stock()
    assert d == {"3/3": 7, "2/3": 9, "1/3": 61}, d
    _, ok2 = supply.plan([20, 22], date(2026, 10, 27), d)
    _, ok3 = supply.plan([20, 22, 40], date(2026, 10, 27), d)
    assert ok2 and not ok3
    return "20 + 22 tiennent ; 40 de plus ne tiennent pas"


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
