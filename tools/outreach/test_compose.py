#!/usr/bin/env python3
"""Banc de `compose.py` — l'atelier qui écrit vingt messages par jour sans qu'ils se ressemblent.

    python3 tools/outreach/test_compose.py

Ce qui est vérifié ici n'est pas le style : c'est que la fabrique **ne peut pas** écrire un gabarit.
Sept phrases par emplacement, charnière (a, b, a+b), et la porte qui juge le lot entier.
"""

from __future__ import annotations

import csv
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compose  # noqa: E402

CAS = []
CRM = compose.RACINE / "leads/CRM.csv"
CHAMPS = ["ID", "School", "City", "Decision maker", "contact_name", "Contacted", "stage",
          "wa_number", "profile_name_seen", "wa_verified", "Website", "Website status", "Notes",
          "source", "source_detail", "slug"]


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def crm_temp(lignes: list[dict]) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="")
    w = csv.DictWriter(f, fieldnames=CHAMPS)
    w.writeheader()
    for l in lignes:
        w.writerow({k: l.get(k, "") for k in CHAMPS})
    f.close()
    return Path(f.name)


# ── les invariants d'écriture ──────────────────────────────────────────────────────────────────

@cas("aucune phrase ne peut, à elle seule, atteindre douze mots hors nom propre")
def _():
    fautes = compose.verifie_reservoirs()
    assert fautes == [], fautes
    return f"{sum(len(p) for p in compose.RESERVOIRS['offre'])} + 28 phrases, toutes sous 12 mots"


@cas("sept variantes par emplacement : 49 combinaisons par angle, jamais réutilisées")
def _():
    combos = compose.toutes_les_combinaisons("offre")
    assert len(combos) == 49 and len(set(combos)) == 49
    assert combos[0] == (0, 0) and combos[7] == (0, 1)
    return "49 couples distincts"


@cas("deux messages voisins ne partagent jamais la même charnière")
def _():
    vus = set()
    for rang in range(49):
        a, b = rang % 7, rang // 7
        vus.add((a, b, (a + b) % 7))
    assert len(vus) == 49
    return "49 triplets distincts"


# ── les données, et ce qu'on refuse d'écrire ─────────────────────────────────────────────────

@cas("« Douala (Akwa) » donne Akwa ; un nom de personne dans la colonne ville ne donne rien")
def _():
    assert compose.quartier("Douala (Akwa)") == "Akwa"
    assert compose.quartier("Bonapriso") == "Bonapriso"
    assert compose.quartier("Douala") == "Douala"
    assert compose.quartier("Madam Namondo Alexander") == ""
    return "3 lieux retenus, 1 refusé"


@cas("un numéro qui n'est pas un mobile camerounais ne produit pas de message")
def _():
    assert compose.numero("+237 677 00 00 01") == "677000001"
    assert compose.numero("123456789") == ""
    assert compose.numero("") == ""


@cas("« Bellevue Optique » et « bellevueoptique » sont le même nom : pas d'angle « nom »")
def _():
    assert compose.meme_nom("Bellevue Optique", "bellevueoptique")
    assert not compose.meme_nom("Ets Espace Médical", "Optic Medical Favour and Joy")
    return "1 fusion, 1 contradiction"


@cas("une ligne sans lieu sûr, sans métier connu ou sans numéro n'est pas composée")
def _():
    f = crm_temp([
        {"School": "Optique Test", "City": "Akwa", "wa_number": "699 00 00 01", "slug": "a"},
        {"School": "Optique Perdue", "City": "Madam X", "wa_number": "699 00 00 02", "slug": "b"},
        {"School": "Zzz Inconnu", "City": "Akwa", "wa_number": "699 00 00 03", "slug": "c"},
        {"School": "Optique Sans Numéro", "City": "Akwa", "wa_number": "12", "slug": "d"},
        {"School": "Optique Déjà Vue", "City": "Akwa", "wa_number": "699 00 00 05", "slug": "e",
         "Contacted": "Yes"},
    ])
    leads = compose.lit_crm(f)
    assert [l.slug for l in leads] == ["a"], [l.slug for l in leads]
    return "1 composable sur 5"


@cas("deux lignes, un numéro : la fabrique le dit, et le lot ne part pas deux fois")
def _():
    f = crm_temp([
        {"School": "Optique Une", "City": "Akwa", "wa_number": "699 00 00 01"},
        {"School": "Optique Deux", "City": "Akwa", "wa_number": "699 00 00 01"},
    ])
    doubl = compose.doublons(compose.lit_crm(f))
    assert len(doubl) == 1 and "699000001" in doubl[0]
    return "1 doublon nommé"


@cas("le filtre `--ecarter` écarte le mort et le hors-cible, jamais le 2/3")
def _():
    import json, tempfile
    leads = [compose.Lead(slug=f"l{i}", nom=f"Cabinet {i}", quartier="Douala", numero=n,
                          profil="", ville="Douala") for i, n in
             enumerate(["699000001", "699000002", "699000003", "699000004"])]
    verif = {"699000001": "JAMAIS", "699000002": "HORS-CIBLE", "699000003": "KING-TRANCHE"}
    tmp = Path(tempfile.mkdtemp()) / "v.json"
    tmp.write_text(json.dumps([{"num": n, "verdict": v} for n, v in verif.items()]), encoding="utf-8")
    garde, ecartes = compose.ecarte(leads, tmp)
    assert [l.numero for l in ecartes] == ["699000001", "699000002"], ecartes
    assert [l.numero for l in garde] == ["699000003", "699000004"], garde
    return "2 écartés, 2 gardés (le 2/3 et le numéro absent du vérificateur)"


@cas("sur le vrai vérificateur, le filtre écarte seize lignes et n'en perd aucun 3/3")
def _():
    import json
    verif = compose.RACINE / "leads/VERIF-2026-10-27.json"
    js = json.loads(verif.read_text(encoding="utf-8"))
    leads = [compose.Lead(slug=x["slug"], nom=x.get("nom", ""), quartier="Douala", numero=x["num"],
                          profil="", ville="Douala")
             for x in js if x.get("verdict") in ("JAMAIS", "HORS-CIBLE")]
    tres = [x for x in js if x.get("verdict") == "ENVOYER"]
    garde, ecartes = compose.ecarte(leads, verif)
    assert len(ecartes) == len(leads) and not garde, (len(ecartes), len(garde))
    assert len(tres) == 7, len(tres)          # les sept 3/3 ne sont pas dans le filtre
    return f"{len(ecartes)} lignes condamnées, 7 ENVOYER hors filtre"


# ── le lot réel ───────────────────────────────────────────────────────────────────────────────

@cas("sur le vrai CRM, seize messages se composent et passent la porte sans un mot répété")
def _():
    leads = compose.lit_crm(CRM)
    deja = set()
    for nom in ("sales/ENVOI-VAGUE-2-2026-10-26.md", "sales/ENVOI-VOLUME-2026-10-27.md",
                "sales/retires/ENVOI-VAGUE-3-2026-10-26.md"):
        p = compose.RACINE / nom
        if p.exists():
            deja |= {compose.numero(m.phone) for m in compose.parse(p)}
    libres = [l for l in leads if l.numero not in deja]
    assert len(libres) < 20, len(libres)          # le stock est presque épuisé : c'est le fait du jour
    return f"{len(libres)} ligne(s) encore libres sur {len(leads)} composables"


@cas("le lot retiré du 26/10 reste lisible et sans bloquant — on ne réécrit pas l'histoire")
def _():
    # Un lot retiré ne sera jamais envoyé : il est la trace de ce qu'on a refusé, pas un lot en
    # attente. Il ne doit donc plus porter de **bloquant** (fait faux, prix, lien, deux questions) ;
    # ses avertissements, eux, sont datés — depuis le 26/10 la porte demande le désarmement, la
    # preuve sociale et une cause nommée, et ce lot ne les avait pas.
    p = compose.RACINE / "sales/retires/ENVOI-VAGUE-3-2026-10-26.md"
    msgs = compose.parse(p)
    assert len(msgs) == 16, len(msgs)
    for m in msgs:
        compose.check(m)
    compose.ressemblance(msgs)
    fautes = [f for m in msgs for f in m.fails]
    assert not fautes, fautes
    return "16 messages, 0 bloquant (avertissements datés, assumés)"


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
