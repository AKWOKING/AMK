#!/usr/bin/env python3
"""test_audit_trust — casse la porte du jeu de contenu, un défaut à la fois.

Même convention que `test_audit_outreach.py` et `test_audit_reel.py` : une porte qu'on n'a jamais
vue refuser n'est pas une porte. Chaque cas est une pièce volontairement fautive ; le test vérifie
que la porte nomme **la bonne** règle.

Le cas « EP01 v2 en autorité » est le cas réel du 25/10 : la même pièce est une porte recevable et
une autorité irrecevable. C'est la leçon, encodée.

Usage : python3 tools/qa/test_audit_trust.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_trust import Piece, audit  # noqa: E402


def porte(**kw) -> Piece:
    base = dict(
        name="EP01", game=5, role="porte", minutes=23.4 / 60, relevance=5, usefulness=4,
        on_target="opticien ou clinique de Douala, sans site",
        next_step="écrire APERÇU sur WhatsApp", goal="conversations",
    )
    base.update(kw)
    return Piece(**base)


def autorite(**kw) -> Piece:
    base = dict(
        name="EP02", game=5, role="autorite", minutes=2.5, relevance=5, usefulness=4,
        on_target="opticien de Douala", next_step="demander l'aperçu", goal="conversations",
    )
    base.update(kw)
    return Piece(**base)


CAS: list[tuple[str, Piece, str]] = [
    ("porte EP01 v3 (saine)", porte(), ""),
    ("preuve carrousel 45 s", porte(name="B2", role="preuve", minutes=0.75, usefulness=4), ""),
    ("autorité 2,5 min", autorite(), ""),
    ("jeu 1 : la viralité", porte(game=1), "mauvais-jeu"),
    ("jeu 2 : la célébrité de niche", porte(game=2), "mauvais-jeu"),
    ("hors cible : un tuyau de design", porte(relevance=2), "hors-cible"),
    ("cible non nommée", porte(on_target="  "), "cible-muette"),
    ("objectif vues", porte(goal="vues"), "objectif-vues"),
    ("aucune étape suivante", porte(next_step=""), "sans-entonnoir"),
    ("utilité nulle", porte(usefulness=0), "inutile"),
    ("EP01 v2 déclaré en autorité", autorite(minutes=23.4 / 60, usefulness=3), "trop-court"),
    ("autorité de 40 s", autorite(minutes=40 / 60, usefulness=3, relevance=4), "trop-court"),
    ("autorité creuse (2 min, u=2)", autorite(minutes=2.0, usefulness=2, relevance=4), "score-faible"),
    ("rôle inventé", porte(role="pubs"), "role"),
]

WARNS = [
    ("très ciblé mais creux", porte(minutes=1.5, relevance=5, usefulness=2, role="preuve"), "mince"),
]


def main() -> int:
    echecs = 0
    for nom, piece, attendu in CAS:
        v = audit(piece)
        if not attendu:
            ok = v.ok
            detail = f"score {piece.score}/125, {len(v.fails)} bloquant(s), {len(v.warns)} avert."
        else:
            ok = any(attendu in f for f in v.fails)
            detail = f"« {attendu} »" if ok else f"attendu « {attendu} », vu {v.fails}"
        print(f"{'✓' if ok else '✗'} {nom:34} {detail}")
        echecs += 0 if ok else 1

    for nom, piece, attendu in WARNS:
        v = audit(piece)
        ok = any(attendu in w for w in v.warns)
        print(f"{'✓' if ok else '✗'} {nom:34} « {attendu} »" if ok else f"✗ {nom:34} attendu « {attendu} », vu {v.warns}")
        echecs += 0 if ok else 1

    total = len(CAS) + len(WARNS)
    print(f"\n{total - echecs}/{total} cas passent")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
