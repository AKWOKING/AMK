#!/usr/bin/env python3
"""test_audit_reel — casse la porte de l'arc, un défaut à la fois.

Même convention que `test_audit_outreach.py` : une porte qu'on n'a jamais vue refuser n'est pas
une porte. Chaque cas est un réel volontairement fautif ; le test vérifie que la porte nomme
**la bonne** règle — pas seulement qu'elle refuse.

Usage : python3 tools/qa/test_audit_reel.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_reel import Beat, audit  # noqa: E402

# Un réel sain : départ à 70, secousse à 6,3 s, relâchement, seconde cime, CTA final.
BON = [
    Beat("hook", 0.0, 5.0, 70, "contexte", "Votre nom existe. Votre site, non."),
    Beat("spike1", 5.0, 9.5, 92, "contraste", "Ce que Google réclame", "capture Optix 24/10"),
    Beat("relache", 9.5, 13.0, 58, "relache"),
    Beat("spike2", 13.0, 16.5, 88, "contraste", "Neuf fiches, zéro site", "capture Optix 24/10"),
    Beat("relache2", 16.5, 18.2, 60, "relache"),
    Beat("cta", 18.2, 21.9, 95, "appel", "Écrivez APERÇU"),
]


def cas(nom: str, beats: list[Beat], attendu: str) -> tuple[str, list[Beat], str]:
    return (nom, beats, attendu)


CAS = [
    cas("reel sain", BON, ""),
    cas(
        "ouvert à zéro",
        [Beat("hook", 0.0, 5.0, 30, "contexte"), *BON[1:]],
        "depart-a-zero",
    ),
    cas(
        "contexte trop lent",
        [Beat("hook", 0.0, 8.0, 70, "contexte"), Beat("spike1", 8.0, 12.0, 92, "contraste"),
         Beat("relache", 12.0, 14.0, 55, "relache"), Beat("cta", 14.0, 18.0, 95, "appel")],
        "contexte-lent",
    ),
    cas(
        "secousse trop tôt",
        [Beat("hook", 0.0, 3.0, 70, "contexte"), Beat("spike1", 3.0, 6.0, 92, "contraste"),
         Beat("relache", 6.0, 9.0, 50, "relache"), Beat("spike2", 9.0, 13.0, 88, "contraste"),
         Beat("cta", 13.0, 17.0, 95, "appel")],
        "premier-pic",
    ),
    cas(
        "une seule cime",
        [Beat("hook", 0.0, 6.0, 70, "contexte"), Beat("spike1", 6.0, 12.0, 92, "contraste"),
         Beat("relache", 12.0, 16.0, 55, "relache"), Beat("cta", 16.0, 20.0, 95, "appel")],
        "pics",
    ),
    cas(
        "deux cimes collées",
        [Beat("hook", 0.0, 6.0, 70, "contexte"), Beat("spike1", 6.0, 10.0, 92, "contraste"),
         Beat("spike2", 10.0, 14.0, 90, "contraste"), Beat("relache", 14.0, 16.0, 55, "relache"),
         Beat("cta", 16.0, 20.0, 95, "appel")],
        "sans-relachement",
    ),
    cas(
        "pas de CTA",
        [b if b.name != "cta" else Beat("fin", 18.2, 21.9, 95, "contexte") for b in BON],
        "cta-absent",
    ),
    cas(
        "CTA trop long",
        [*BON[:5], Beat("cta", 18.2, 24.0, 95, "appel")],
        "cta-long",
    ),
    cas(
        "chiffre sans source",
        [Beat("hook", 0.0, 6.0, 70, "contexte"), Beat("spike1", 6.0, 10.0, 92, "chiffre", "+40 % d'appels"),
         Beat("relache", 10.0, 13.0, 55, "relache"), Beat("cta", 13.0, 17.0, 95, "appel")],
        "chiffre-nu",
    ),
    cas(
        "chiffre sans date",
        [Beat("hook", 0.0, 6.0, 70, "contexte"),
         Beat("spike1", 6.0, 10.0, 92, "chiffre", "175-450k", "relevé du marché"),
         Beat("relache", 10.0, 13.0, 55, "relache"), Beat("cta", 13.0, 17.0, 95, "appel")],
        "chiffre-non-date",
    ),
    cas(
        "trou dans la timeline",
        [Beat("hook", 0.0, 5.0, 70, "contexte"), Beat("spike1", 7.0, 10.0, 92, "contraste"),
         Beat("relache", 10.0, 13.0, 55, "relache"), Beat("cta", 13.0, 17.0, 95, "appel")],
        "trou",
    ),
    cas(
        "trop long",
        [*BON[:-1], Beat("cta", 18.2, 28.0, 95, "appel")],
        "duree",
    ),
]


def main() -> int:
    echecs = 0
    for nom, beats, attendu in CAS:
        v = audit(beats)
        if not attendu:
            ok = v.ok and not v.warns
            detail = f"{len(v.fails)} bloquant(s), {len(v.warns)} avertissement(s)"
        else:
            ok = any(attendu in f for f in v.fails)
            detail = f"« {attendu} »" if ok else f"attendu « {attendu} », vu {v.fails}"
        print(f"{'✓' if ok else '✗'} {nom:24} {detail}")
        echecs += 0 if ok else 1

    print(f"\n{len(CAS) - echecs}/{len(CAS)} cas passent")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
