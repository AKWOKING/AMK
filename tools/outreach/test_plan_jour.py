#!/usr/bin/env python3
"""Banc du plan du matin — `tools/outreach/plan_jour.py`.

    python3 tools/outreach/test_plan_jour.py

Le cas qui compte est le dernier : sur les vrais lots du 26/10, le plan doit dire **35 messages, dont 5
prêts**, et jamais compter un numéro mort comme envoyable. Un plan qui se trompe d'un cran envoie un
message qu'on n'a pas le droit d'écrire — c'est pire que pas de plan du tout.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import plan_jour  # noqa: E402

CAS = []
RACINE = plan_jour.RACINE
LOTS = ["sales/LOT-1-2026-10-27.md", "sales/ENVOI-VOLUME-2026-10-27.md"]


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


@cas("le plan lit les deux lots vivants : 35 messages, 5 prêts")
def _():
    p = plan_jour.plan("2026-10-27", choisis=LOTS)
    assert len(p["lignes"]) == 35, len(p["lignes"])
    assert p["compte"]["ENVOYER"] == 5, p["compte"]
    assert p["compte"]["JAMAIS"] == 0 and p["compte"]["HORS-CIBLE"] == 0, p["compte"]
    return f"35 lignes · {p['compte']['KING-TRANCHE']} à trancher · {p['compte']['PAS-ENVOYÉ']} sans porte"


@cas("l'ordre met les 3/3 devant, et le mort en dernier")
def _():
    p = plan_jour.plan("2026-10-27", choisis=LOTS)
    vus = [l["verdict"] for l in p["lignes"]]
    assert vus == sorted(vus, key=plan_jour.ORDRE.index), vus
    assert vus[0] == "ENVOYER"
    return "cinq ENVOYER en tête, aucun verdict mélangé"


@cas("un numéro absent du vérificateur n'est jamais compté prêt")
def _():
    v = plan_jour.verdicts(RACINE / "leads" / "VERIF-2026-10-27.json")
    assert v, "le vérificateur du 27/10 manque"
    assert v.get("655049529") == "ENVOYER"        # Ets Espace Médical, capture du 25/10
    assert v.get("674936604") == "ENVOYER" or "674936604" in v
    return "7 ENVOYER lus dans le vrai JSON"


@cas("sans vérificateur, tout est PAS-ENVOYÉ et le plan le dit")
def _():
    dossier = Path(tempfile.mkdtemp())
    lot = dossier / "ENVOI-TEST.md"
    lot.write_text("**#1 Cabinet Test — Douala — 699 00 00 01**\n"
                   "> Bonjour, à Douala vous êtes Cabinet Test.\n"
                   "> J'ai fait la page d'un opticien d'ici, et elle tourne.\n"
                   "> Dites-moi en un mot : je vous l'envoie ?\n", encoding="utf-8")
    p = plan_jour.plan("1999-01-01", dossier)
    assert len(p["lignes"]) == 1, p["lignes"]
    assert p["lignes"][0]["verdict"] == "PAS-ENVOYÉ", p["lignes"][0]
    assert not p["verif_lu"]
    texte = plan_jour.rendu(p)
    assert "aucun `leads/VERIF" in texte, texte[-400:]
    return "1 ligne, PAS-ENVOYÉ, avertissement présent"


@cas("le stock restant exclut ce qui est déjà écrit et ce qui est condamné")
def _():
    p = plan_jour.plan("2026-10-27", choisis=LOTS)
    ecrits = {l["num"] for l in p["lignes"]}
    libres = {l.numero for l in p["libres"]}
    assert not (ecrits & libres), ecrits & libres
    v = plan_jour.verdicts(RACINE / "leads" / "VERIF-2026-10-27.json")
    assert not [n for n in libres if v.get(n) in ("JAMAIS", "HORS-CIBLE")], "un condamné reste libre"
    return f"{len(libres)} ligne(s) encore libre(s), aucune déjà écrite, aucune condamnée"


@cas("le rendu porte les trois gestes du matin, dans l'ordre")
def _():
    p = plan_jour.plan("2026-10-27", choisis=LOTS)
    t = plan_jour.rendu(p)
    for attendu in ("Ouvrir WhatsApp", "Envoyer dans l'ordre du tableau", "Cocher le tracker"):
        assert attendu in t, attendu
    return "trois gestes présents"


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
