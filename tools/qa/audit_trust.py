#!/usr/bin/env python3
"""audit_trust — la porte du jeu de contenu (`knowledge/CONTENT-GAMES-2026-10-25.md`).

Le dépôt produit du contenu pour vendre un service à un acheteur nommable. C'est le **jeu 5**
(construction d'autorité) : on n'est pas payé par la vue, on est payé quand **le bon** spectateur
descend dans l'entonnoir. Cette porte vérifie qu'une pièce sert bien ce jeu-là, avec la formule de
la source — confiance = minutes × pertinence × utilité — et un plancher par rôle.

Ce qu'elle ne fait pas : juger le goût, la typographie, ou la véracité des faits montrés (c'est
`audit_reel.py` et `RESEARCH-STANDARD.md`).

Usage :

    from audit_trust import Piece, audit
    audit(Piece(name="EP01", game=5, role="porte", minutes=23.4/60,
                relevance=5, usefulness=4, on_target="opticien de Douala",
                next_step="écrire APERÇU", goal="conversations"))

    python3 tools/qa/audit_trust.py content/reels/ep01/make_ep01.py   # lit TRUST du module
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── seuils ───────────────────────────────────────────────────────────────────────────────────
# Les planchers viennent de `knowledge/CONTENT-GAMES-2026-10-25.md` §3. Ils sont **notre**
# décision : la source ne donne aucune échelle, elle donne la formule et les trois facteurs.
PLANCHERS = {"porte": 12, "preuve": 24, "autorite": 40, "autorité": 40}
ROLES = set(PLANCHERS)
JEU_AUTORISE = 5
PERTINENCE_MIN = 3
AUTORITE_MIN_TIER = 3          # 1–2 min : sous ce seuil, une « autorité » est une porte déguisée
OBJECTIFS_INTERDITS = {"vues", "views", "reach", "portee", "portée", "impressions", "viralite", "viralité"}
UTILITE_MINCE = 2              # pertinence 5 + utilité ≤ 2 = très ciblé mais creux

# barème des minutes, indexé par palier (voir §3 du document)
PALIERS_MINUTES = [
    (15 / 60, 0, "< 15 s"),
    (30 / 60, 1, "15–30 s"),
    (60 / 60, 2, "30–60 s"),
    (120 / 60, 3, "1–2 min"),
    (300 / 60, 4, "2–5 min"),
]


def palier(minutes: float) -> tuple[int, str]:
    for seuil, tier, label in PALIERS_MINUTES:
        if minutes < seuil:
            return tier, label
    return 5, "≥ 5 min"


@dataclass
class Piece:
    name: str
    game: int
    role: str
    minutes: float
    relevance: int
    usefulness: int
    on_target: str
    next_step: str
    goal: str

    @property
    def tier(self) -> int:
        return palier(self.minutes)[0]

    @property
    def score(self) -> int:
        return self.tier * self.relevance * self.usefulness

    @property
    def plancher(self) -> int | None:
        return PLANCHERS.get(self.role)


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)

    def fail(self, code: str, msg: str):
        self.fails.append(f"[{code}] {msg}")

    def warn(self, code: str, msg: str):
        self.warns.append(f"[{code}] {msg}")

    @property
    def ok(self) -> bool:
        return not self.fails


def audit(p: Piece) -> Verdict:
    v = Verdict()

    # ── le jeu ──────────────────────────────────────────────────────────────────────────────
    if p.game != JEU_AUTORISE:
        v.fail(
            "mauvais-jeu",
            f"jeu {p.game} déclaré ; nous jouons le {JEU_AUTORISE} (autorité). Les jeux 1 et 2 "
            "paient à la vue : « you are the product », et notre produit est le site du client",
        )

    # ── la cible ────────────────────────────────────────────────────────────────────────────
    if not (0 <= p.relevance <= 5):
        v.fail("bareme", f"pertinence {p.relevance} hors barème 0–5")
    elif p.relevance < PERTINENCE_MIN:
        v.fail(
            "hors-cible",
            f"pertinence {p.relevance}/5 : le spectateur ne peut pas acheter. Dans le jeu 5, "
            "la largeur est un piège (« 1 000 vues de la bonne personne »)",
        )
    if not p.on_target.strip():
        v.fail("cible-muette", "aucune cible nommée : on ne peut pas vérifier que le spectateur peut acheter")

    # ── l'objectif ──────────────────────────────────────────────────────────────────────────
    if p.goal.strip().lower() in OBJECTIFS_INTERDITS:
        v.fail(
            "objectif-vues",
            f"objectif « {p.goal} » : c'est le jeu 1. La seule métrique qui décide est la "
            "conversation (playbook §6.1)",
        )

    # ── l'entonnoir ─────────────────────────────────────────────────────────────────────────
    if not p.next_step.strip():
        v.fail(
            "sans-entonnoir",
            "aucune étape suivante : la source exige « high-trust hits **with proper funnels** » ; "
            "une pièce sans sortie ne capture rien",
        )

    # ── l'utilité ───────────────────────────────────────────────────────────────────────────
    if not (0 <= p.usefulness <= 5):
        v.fail("bareme", f"utilité {p.usefulness} hors barème 0–5")
    elif p.usefulness == 0:
        v.fail("inutile", "utilité 0 : le produit des trois facteurs s'annule, la pièce ne construit rien")
    elif p.relevance == 5 and p.usefulness <= UTILITE_MINCE:
        v.warn(
            "mince",
            f"pertinence {p.relevance} mais utilité {p.usefulness} : très ciblé et creux — "
            "ça ne se partage pas et ça ne se retient pas",
        )

    # ── le rôle ─────────────────────────────────────────────────────────────────────────────
    if p.role not in ROLES:
        v.fail("role", f"rôle « {p.role} » inconnu (attendu : {sorted(ROLES)})")
        return v

    if p.role in {"autorite", "autorité"} and p.tier < AUTORITE_MIN_TIER:
        v.fail(
            "trop-court",
            f"rôle autorité à {p.minutes * 60:.0f} s ({palier(p.minutes)[1]}) : une pièce de cette "
            f"durée plafonne à {p.tier * 5 * 5}/125, sous le plancher de 40. Une porte n'est pas "
            "un moteur de confiance",
        )

    if p.score < p.plancher:
        v.fail(
            "score-faible",
            f"score {p.score}/125 ({p.tier} × {p.relevance} × {p.usefulness}) sous le plancher "
            f"« {p.role} » ({p.plancher}). Ce qui manque : "
            + ("des minutes (allonger la pièce) " if p.tier < AUTORITE_MIN_TIER else "")
            + ("de la pertinence " if p.relevance < 4 else "")
            + ("de l'utilité (que repart-il avec ?)" if p.usefulness < 3 else ""),
        )

    return v


# ─────────────────────────────────────────────────────────────── CLI ──────────


def load_piece(path: str) -> Piece:
    spec = importlib.util.spec_from_file_location("piece", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    piece = getattr(mod, "TRUST", None)
    # Pas de `isinstance` : lancé en script, ce fichier est le module « __main__ », alors que la
    # pièce importe `audit_trust` — deux identités pour la même classe, et l'isinstance échoue
    # sur un objet parfaitement valide. On vérifie la forme, pas l'identité du module.
    requis = ("game", "role", "minutes", "relevance", "usefulness", "on_target", "next_step", "goal")
    if piece is None or not all(hasattr(piece, a) for a in requis):
        raise SystemExit(f"✗ {path} : pas de TRUST (Piece) — la pièce ne déclare pas son rôle")
    return piece


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    echecs = 0
    for path in argv:
        p = load_piece(path)
        v = audit(p)
        nom = Path(path).parent.name
        etat = "✓" if v.ok else "✗"
        print(f"{etat} {nom:8} {p.role:8} {p.minutes * 60:5.1f} s · score {p.score:3}/125 "
              f"({p.tier} × {p.relevance} × {p.usefulness}) · plancher {p.plancher}")
        if not v.ok:
            echecs += 1
            for f in v.fails:
                print(f"   ⛔ {f}")
        for w in v.warns:
            print(f"   ⚠ {w}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
