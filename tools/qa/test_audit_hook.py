#!/usr/bin/env python3
"""Banc de `audit_hook.py` — les six mots, l'échelle, la grille.

    python3 tools/qa/test_audit_hook.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_hook import Grid, Hook, audit_grid, audit_hook, parse_grid, power_words  # noqa: E402

CAS = []

# Une accroche qui a les quatre mots obligatoires : « Ouvrez… deux cabinets apparaissent… appelle
# celui qui a un site, pas celui qui n'en a pas. »
BONNE = ("Ouvrez votre nom sur Google. Deux cabinets apparaissent : le patient appelle "
         "celui qui a un site, pas celui qui n'en a pas.")


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def codes(v):
    return [f.split(" ")[0] for f in v.fails]


def grille(rangées):
    return Grid(cells=[{"n": n, "topic": t, "format": f, "sujet": s, "etat": e}
                       for n, t, f, s, e in rangées])


def grille_saine():
    sujets = ["fiche", "site", "prix"]
    formats = ["classement", "cas", "scénario"]
    rangées = [(i + 1, sujets[i // 3], formats[i % 3], f"pièce {i + 1}", "à écrire")
               for i in range(9)]
    rangées.append((10, "—", "—", "à décider après les neuf", "ouvert — aucune donnée au 25/10"))
    return grille(rangées)


# ── les six mots ───────────────────────────────────────────────────────────────────────────────
@cas("une accroche complète passe")
def _():
    v = audit_hook(Hook(text=BONNE, level=3))
    assert v.ok, v.fails


@cas("les quatre mots sont détectés")
def _():
    m = power_words(Hook(text=BONNE))
    assert all(m[k] for k in ("sujet", "action", "objectif", "contraste")), m


@cas("sans contraste, refusé — le mot le plus important")
def _():
    v = audit_hook(Hook(text="Ouvrez votre nom sur Google et regardez ce que le patient trouve."))
    assert "mots-manquants" in codes(v), v.fails
    assert any("contraste" in f for f in v.fails), v.fails


@cas("sans objectif, refusé")
def _():
    v = audit_hook(Hook(text="Ouvrez votre nom sur Google, pas celui du voisin."))
    assert "mots-manquants" in codes(v), v.fails


@cas("l'ancienne accroche d'EP01 est refusée (action + objectif manquants)")
def _():
    v = audit_hook(Hook(text="Votre cabinet existe. Votre site, non.", level=1))
    assert not v.ok
    assert "action" in v.fails[-1] or "action" in v.fails[0], v.fails


@cas("une action déclarée à la main sauve le mot — et se voit")
def _():
    v = audit_hook(Hook(text="Votre fiche, en dix minutes, et le patient vous appelle — pas le voisin.",
                        declares={"action": "réclamez"}))
    assert v.ok, v.fails
    assert any("déclaration" in w for w in v.warns), v.warns


@cas("trop longue, refusée")
def _():
    texte = BONNE + " " + " ".join(["et"] * 12)
    v = audit_hook(Hook(text=texte))
    assert "trop-long" in codes(v), v.fails


@cas("vendre par la peur, refusé")
def _():
    v = audit_hook(Hook(text="Ouvrez votre nom maintenant : c'est la dernière chance avant la catastrophe."))
    assert "peur" in codes(v), v.fails


@cas("une promesse de résultat, refusée")
def _():
    v = audit_hook(Hook(text="Ouvrez votre nom : +40 % d'appels garantis, pas comme avant."))
    assert "promesse" in codes(v), v.fails


@cas("niveau hors échelle, refusé")
def _():
    v = audit_hook(Hook(text=BONNE, level=9))
    assert "niveau-inconnu" in codes(v), v.fails


@cas("niveau 4 sans plan lisible : averti")
def _():
    v = audit_hook(Hook(text=BONNE, level=4))
    assert v.ok and any("niveau-ambitieux" in w for w in v.warns), v.warns


@cas("niveau 4 avec un plan lisible : pas d'avertissement")
def _():
    texte = "D'abord vos horaires, ensuite la fiche, puis un site : le patient appelle celui qui a tout."
    v = audit_hook(Hook(text=texte, level=4))
    assert not any("niveau-ambitieux" in w for w in v.warns), v.warns


@cas("niveau 1 (Reporter) : signalé comme point de départ")
def _():
    v = audit_hook(Hook(text=BONNE, level=1))
    assert any("niveau-1" in w for w in v.warns), v.warns


@cas("sans intrigue : averti, jamais refusé")
def _():
    v = audit_hook(Hook(text="Ouvrez votre nom : le patient appelle celui qui a un site, pas l'autre.",
                        level=2))
    assert v.ok and any("sans-intrigue" in w for w in v.warns), v.warns


@cas("accroche vide : refusée")
def _():
    v = audit_hook(Hook(text="   "))
    assert "hook-vide" in codes(v), v.fails


# ── la grille 331 ──────────────────────────────────────────────────────────────────────────────
@cas("une grille 3×3 + une dixième ouverte passe")
def _():
    v = audit_grid(grille_saine())
    assert v.ok, v.fails
    assert any("double-ouvert" in w for w in v.warns), v.warns


@cas("huit cellules : incomplète")
def _():
    g = grille_saine()
    g.cells = [c for c in g.cells if c["n"] != 5]
    v = audit_grid(g)
    assert "grille-incomplete" in codes(v), v.fails


@cas("deux formats seulement : refusé")
def _():
    g = grille_saine()
    for c in g.cells:
        if c["n"] in (2, 5, 8):
            c["format"] = "classement"
    v = audit_grid(g)
    assert any(c.startswith("trois-formats") or c.startswith("doublon") for c in codes(v)), v.fails


@cas("quatre sujets : refusé")
def _():
    g = grille_saine()
    g.cells[0]["topic"] = "quatrième sujet"
    v = audit_grid(g)
    assert "trois-sujets" in codes(v), v.fails


@cas("une cellule sans sujet : refusée")
def _():
    g = grille_saine()
    g.cells[3]["sujet"] = "—"
    v = audit_grid(g)
    assert "cellule-sans-sujet" in codes(v), v.fails


@cas("dixième choisie sans donnée : refusée")
def _():
    g = grille_saine()
    g.cells[-1] = {"n": 10, "topic": "fiche", "format": "classement",
                   "sujet": "on refait la même", "etat": "choisie"}
    v = audit_grid(g)
    assert "double-sans-donnée" in codes(v), v.fails


@cas("dixième absente : refusée")
def _():
    g = grille_saine()
    g.cells = [c for c in g.cells if c["n"] != 10]
    v = audit_grid(g)
    assert "pas-de-10" in codes(v), v.fails


@cas("lecture markdown : 9 cellules + la dixième")
def _():
    texte = """| # | sujet | format | pièce | état |
|---|---|---|---|---|
| 1 | fiche | classement | pièce 1 | à écrire |
| 2 | fiche | cas | pièce 2 | à écrire |
| 3 | fiche | scénario | pièce 3 | produite |
| 4 | site | classement | pièce 4 | à écrire |
| 5 | site | cas | pièce 5 | à écrire |
| 6 | site | scénario | pièce 6 | à écrire |
| 7 | prix | classement | pièce 7 | à écrire |
| 8 | prix | cas | pièce 8 | à écrire |
| 9 | prix | scénario | pièce 9 | brouillon |
| 10 | — | — | à décider après les neuf (aucune donnée au 25/10) | ouvert |
"""
    g = parse_grid(texte)
    assert len(g.cells) == 10, g.cells
    assert audit_grid(g).ok, audit_grid(g).fails


def main() -> int:
    echecs = 0
    for nom, fn in CAS:
        try:
            fn()
            print(f"  ✓ {nom}")
        except AssertionError as exc:
            echecs += 1
            print(f"  ✗ {nom} → {exc}")
    total = len(CAS)
    print(f"\n{total - echecs}/{total} cas passent")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
