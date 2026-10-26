#!/usr/bin/env python3
"""Banc de `audit_story.py` — la porte du récit : cas, lock-in, preuve dite, rehook, CTA aligné.

    python3 tools/qa/test_audit_story.py

Un banc qui ne teste que des refus ne prouve rien : chaque refus a ici son **contre-exemple qui passe**.
La dernière famille vérifie la seule chose qui compte : **la v4 rendue échoue là où le Roast Room a dit
qu'elle échouait**, et **la v5 passe**. Tout le reste est de la plomberie.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_story import Line, Script, audit  # noqa: E402

CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn

    return enveloppe


def codes(v):
    return [f.split(" ")[0].strip("[]") for f in v.fails]


def wcodes(v):
    return [w.split(" ")[0].strip("[]") for w in v.warns]


def ligne(name, text, role, start, end):
    return Line(name=name, text=text, role=role, start=start, end=end)


# ── la pièce saine : c'est la v5, mot pour mot ───────────────────────────────────────────────────

BIEN = [
    ("hook", "Votre patient tape opticien Akwa. Il appelle celui qui a un site, pas vous.",
     "cas", 0.0, 5.0),
    ("spike1", "Sa fiche a des horaires, un site, douze avis. La vôtre : un nom.",
     "lockin+preuve", 5.0, 9.6),
    ("release1", "Vos horaires et votre fiche : dix minutes, gratuit.",
     "corps", 9.6, 12.4),
    ("spike2", "Ce n'est pas le site qu'il regarde. Il veut venir ce soir.",
     "rehook+corps", 12.4, 16.6),
    ("release2", "Un site répond à vingt-deux heures. Horaires, adresse, WhatsApp.",
     "corps", 16.6, 20.2),
    ("cta", "Écrivez APERÇU sur WhatsApp.", "sortie", 20.2, 23.0),
]


def piece(bornes=None):
    bornes = bornes or BIEN
    return Script(
        piece="test",
        promise="aperçu",
        proof_on_screen="capture Optix 24/10 : un site · 6 photos · 12 avis",
        lines=[ligne(*b) for b in bornes],
    )


@cas("la pièce saine passe (zéro refus)")
def _():
    v = audit(piece())
    assert v.ok, v.fails


@cas("la pièce saine n'a aucun avertissement de structure")
def _():
    v = audit(piece())
    assert not wcodes(v), v.warns


@cas("un rôle multiple est accepté : lockin+preuve sur le même beat")
def _():
    v = audit(piece())
    assert not any("role-inconnu" in c for c in codes(v)), v.fails


# ── les refus, un par règle ──────────────────────────────────────────────────────────────────────


@cas("pas-de-cas : on ouvre sur une consigne")
def _():
    b = list(BIEN)
    b[0] = ("hook", "Tapez votre nom sur Google : il appelle les autres, pas vous.", "lockin", 0.0, 5.0)
    v = audit(piece(b))
    assert "pas-de-cas" in codes(v), v.fails


@cas("pas-de-lockin : rien ne dit pourquoi rester dans les trois premiers beats")
def _():
    b = list(BIEN)
    b[1] = ("spike1", "Sa fiche a des horaires, un site, douze avis. La vôtre : un nom.", "preuve", 5.0, 9.6)
    b[4] = ("release2", "Un site répond à vingt-deux heures.", "corps+lockin", 16.6, 20.2)
    v = audit(piece(b))
    assert "pas-de-lockin" in codes(v), v.fails


@cas("pas-de-rehook : le défaut exact de la v4")
def _():
    b = list(BIEN)
    b[3] = ("spike2", "Ce n'est pas le site qu'il regarde. Il veut venir ce soir.", "corps", 12.4, 16.6)
    v = audit(piece(b))
    assert "pas-de-rehook" in codes(v), v.fails


@cas("rehook-mal-place : un rehook après le CTA ne relance plus rien")
def _():
    b = list(BIEN)
    b[3] = ("spike2", "Ce n'est pas le site qu'il regarde. Il veut venir ce soir.", "corps", 12.4, 16.6)
    b.append(("bonus", "Et ce n'est pas fini.", "rehook", 23.0, 24.0))
    v = audit(piece(b))
    assert "rehook-mal-place" in codes(v) or "sortie-mal-placee" in codes(v), v.fails


@cas("preuve-muette : la capture dit 12 avis, la voix ne dit aucun chiffre")
def _():
    b = list(BIEN)
    b[1] = ("spike1", "Sa fiche a des horaires, un site, des avis. La vôtre : un nom.",
            "lockin+preuve", 5.0, 9.6)
    v = audit(piece(b))
    assert "preuve-muette" in codes(v), v.fails


@cas("preuve-absente : aucun beat ne porte de preuve")
def _():
    b = list(BIEN)
    b[1] = ("spike1", "Sa fiche a des horaires, un site. La vôtre : un nom.", "lockin", 5.0, 9.6)
    v = audit(piece(b))
    assert "preuve-absente" in codes(v), v.fails


@cas("douze avis en toutes lettres compte comme une preuve dite")
def _():
    b = list(BIEN)
    b[1] = ("spike1", "Sa fiche a des horaires, un site, douze avis. La vôtre : un nom.",
            "lockin+preuve", 5.0, 9.6)
    v = audit(piece(b))
    assert "preuve-muette" not in codes(v), v.fails


@cas("cta-non-aligne : le CTA ne prononce pas le mot de la promesse")
def _():
    b = list(BIEN)
    b[5] = ("cta", "Contactez-nous sur WhatsApp.", "sortie", 20.2, 23.0)
    v = audit(piece(b))
    assert "cta-non-aligne" in codes(v), v.fails


@cas("deux-cta : deux beats de sortie")
def _():
    b = list(BIEN)
    b[4] = ("release2", "Écrivez APERÇU aussi.", "sortie", 16.6, 20.2)
    v = audit(piece(b))
    assert "deux-cta" in codes(v), v.fails


@cas("deux-cta déguisé : deux verbes d'action différents")
def _():
    b = list(BIEN)
    b[4] = ("release2", "Appelez-nous à vingt-deux heures.", "corps", 16.6, 20.2)
    v = audit(piece(b))
    assert "deux-cta" in codes(v), v.fails


@cas("sortie-absente : la pièce ne demande rien")
def _():
    b = list(BIEN)
    b[5] = ("cta", "Écrivez APERÇU sur WhatsApp.", "corps", 20.2, 23.0)
    v = audit(piece(b))
    assert "sortie-absente" in codes(v), v.fails


@cas("sortie-mal-placee : un beat après le CTA")
def _():
    b = list(BIEN) + [("post", "Voilà.", "corps", 23.0, 24.0)]
    v = audit(piece(b))
    assert "sortie-mal-placee" in codes(v), v.fails


@cas("liste-sans-axe : quatre arguments empilés dans un beat")
def _():
    b = list(BIEN)
    b[4] = ("release2", "Un site a horaires, adresse, photos, WhatsApp.",
            "corps", 16.6, 20.2)
    v = audit(piece(b))
    assert "liste-sans-axe" in codes(v), v.fails


@cas("urgence : refusée, même dans une pièce par ailleurs bonne")
def _():
    b = list(BIEN)
    b[3] = ("spike2", "C'est la dernière chance. Il veut venir ce soir.", "rehook+corps", 12.4, 16.6)
    v = audit(piece(b))
    assert "urgence" in codes(v), v.fails


@cas("promesse : refusée")
def _():
    b = list(BIEN)
    b[4] = ("release2", "Un site garanti répond à vingt-deux heures.", "corps", 16.6, 20.2)
    v = audit(piece(b))
    assert "promesse" in codes(v), v.fails


@cas("beat-vide et role-inconnu : la déclaration cassée est nommée")
def _():
    b = list(BIEN)
    b[4] = ("release2", "   ", "relance", 16.6, 20.2)
    v = audit(piece(b))
    assert "beat-vide" in codes(v) and "role-inconnu" in codes(v), v.fails


@cas("trop-de-beats : au-delà de sept, ce n'est plus un short")
def _():
    b = list(BIEN) + [("x1", "Encore une idée.", "corps", 23.0, 24.0),
                      ("x2", "Et une autre.", "corps", 24.0, 25.0)]
    v = audit(piece(b))
    assert "trop-de-beats" in codes(v), v.fails


@cas("script-vide : rien à écouter")
def _():
    v = audit(Script(lines=[]))
    assert "script-vide" in codes(v), v.fails


# ── les avertissements ───────────────────────────────────────────────────────────────────────────


@cas("cadeau-tardif : l'offre gratuite à 18 s sur 23")
def _():
    b = list(BIEN)
    b[2] = ("release1", "Vos horaires et votre fiche : deux choses à faire.",
            "corps", 9.6, 12.4)
    b[4] = ("release2", "Un site répond à vingt-deux heures. Dix minutes, gratuit.",
            "corps", 16.6, 20.2)
    v = audit(piece(b))
    assert "cadeau-tardif" in wcodes(v), v.warns


@cas("preuve-tardive : la preuve après les deux tiers")
def _():
    b = list(BIEN)
    b[1] = ("spike1", "Sa fiche a des horaires et un site. La vôtre : un nom.", "lockin", 5.0, 9.6)
    b[4] = ("release2", "Un site répond à vingt-deux heures, douze avis le disent.",
            "corps+preuve", 16.6, 20.2)
    v = audit(piece(b))
    assert "preuve-tardive" in wcodes(v), v.warns


@cas("debit : un texte trop lent pour une voix")
def _():
    b = list(BIEN)
    b[1] = ("spike1", "Douze avis.", "lockin+preuve", 5.0, 9.6)
    b[2] = ("release1", "Dix minutes.", "corps", 9.6, 12.4)
    b[3] = ("spike2", "Ce soir.", "rehook+corps", 12.4, 16.6)
    b[4] = ("release2", "Un site.", "corps", 16.6, 20.2)
    b[5] = ("cta", "Écrivez APERÇU.", "sortie", 20.2, 23.0)
    v = audit(piece(b))
    assert "debit" in wcodes(v), v.warns


# ── le seul test qui compte : la v4 échoue, la v5 passe ─────────────────────────────────────────

V4 = Script(
    piece="ep01-v4",
    promise="aperçu",
    proof_on_screen="capture Optix 24/10 : un site · 6 photos · 12 avis",
    lines=[
        ligne("hook", "Tapez votre nom sur Google : il appelle les autres, pas vous.", "lockin", 0.0, 5.0),
        ligne("spike1", "Google demande trois choses : horaires, site, un avis.", "corps", 5.0, 10.44),
        ligne("release1", "Vous en avez une.", "corps", 10.44, 12.74),
        ligne("spike2", "Un site ne sert pas à avoir un site. Il répond avant l'appel.", "corps", 12.74, 18.06),
        ligne("release2", "Dix minutes. C'est gratuit.", "corps", 18.06, 20.86),
        ligne("cta", "Écrivez APERÇU sur WhatsApp.", "sortie", 20.86, 24.50),
    ],
)


@cas("la v4 rendue le 26/10 : refusée pour l'absence de scène")
def _():
    v = audit(V4)
    assert "pas-de-cas" in codes(v), v.fails


@cas("la v4 : refusée aussi pour l'absence de rehook")
def _():
    v = audit(V4)
    assert "pas-de-rehook" in codes(v), v.fails


@cas("la v4 : refusée pour la preuve muette (la capture dit 12 avis, la voix non)")
def _():
    v = audit(V4)
    assert "preuve-absente" in codes(v) or "preuve-muette" in codes(v), v.fails


@cas("la v4 : le cadeau arrivait à 18 s sur 24,5 — signalé")
def _():
    v = audit(V4)
    assert "cadeau-tardif" in wcodes(v), v.warns


@cas("la v5 : passe les douze vérifications")
def _():
    v = audit(piece())
    assert v.ok, v.fails


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
