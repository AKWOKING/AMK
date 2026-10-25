#!/usr/bin/env python3
"""Banc de `audit_ideas.py` — chaque règle a son cas, et le cas sain doit passer.

    python3 tools/qa/test_audit_ideas.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_ideas import Idea, audit, audit_idea, parse  # noqa: E402

CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


def saine(**kw) -> Idea:
    base = dict(
        ident="IDEA-01",
        pipe=2,
        topic="fiche Google d'un opticien",
        seed="Une fiche complète fait rappeler ; une fiche vide fait passer au suivant",
        substance="trois captures datées du 24/10 : horaires, site, premier avis",
        cible="opticien de Douala, 35–54 ans, fiche existante, pas de site",
        preuve="concurrent camerounais A · 41 000 vues pour 3 200 de moyenne (12/10)",
        constantes=["format 6 beats", "arc 3 cimes", "mise en page", "mascotte",
                    "voix", "CTA"],
        changees=["topic", "substance"],
    )
    base.update(kw)
    return Idea(**base)


def codes(verdict):
    return [f.split(" · ")[1].split(" ")[0] for f in verdict.fails]


@cas("une idée saine passe")
def _():
    v = audit_idea(saine(), outliers_valides=3)
    assert v.ok, v.fails
    assert v.warns == [], v.warns


@cas("tuyau hors 1-6 refusé")
def _():
    v = audit_idea(saine(pipe=7), outliers_valides=3)
    assert codes(v) == ["pipe-inconnu"], codes(v)


@cas("tuyau 1 sans chiffre refusé")
def _():
    v = audit_idea(saine(pipe=1, preuve="notre meilleure vidéo, personne ne sait combien"),
                   outliers_valides=1)
    assert "pipe-sans-chiffre" in codes(v), codes(v)


@cas("tuyau 2 avec chiffre accepté")
def _():
    v = audit_idea(saine(pipe=2), outliers_valides=1)
    assert v.ok, v.fails


@cas("tuyau 3 sans chiffre : avertissement, pas refus")
def _():
    v = audit_idea(saine(pipe=3, preuve="le carrousel kallowaymarketing du 23/10 (vues inconnues)"),
                   outliers_valides=0)
    assert v.ok, v.fails
    assert any("preuve-sans-chiffre" in w for w in v.warns), v.warns


@cas("actualité sans date avertie")
def _():
    v = audit_idea(saine(pipe=4, preuve="Google a changé l'affichage des fiches cette semaine"),
                   outliers_valides=0)
    assert v.ok and any("actualité-sans-date" in w for w in v.warns), v.warns


@cas("actualité datée acceptée")
def _():
    v = audit_idea(saine(pipe=4, preuve="relevé du 24/10/2026 : trois champs disparus de l'affichage"),
                   outliers_valides=0)
    assert v.ok and not any("actualité-sans-date" in w for w in v.warns), v.warns


@cas("[NEEDS DATA] dans la preuve : refusé")
def _():
    v = audit_idea(saine(preuve="[NEEDS DATA] : les vues du concurrent"), outliers_valides=0)
    assert "preuve-manquante" in codes(v), codes(v)


@cas("seed trop court refusé")
def _():
    v = audit_idea(saine(seed="Fiche Google"), outliers_valides=0)
    assert "seed-mou" in codes(v), codes(v)


@cas("seed identique au topic refusé")
def _():
    meme = "fiche google d'un opticien"
    v = audit_idea(saine(topic=meme, seed=meme), outliers_valides=0)
    assert "seed=topic" in codes(v), codes(v)


@cas("cible floue refusée")
def _():
    v = audit_idea(saine(cible="tout le monde"), outliers_valides=0)
    assert "cible-mou" in codes(v), codes(v)


@cas("quatre briques changées : refusé")
def _():
    v = audit_idea(saine(changees=["topic", "seed", "substance", "format"]), outliers_valides=3)
    assert "trop-de-briques" in codes(v), codes(v)


@cas("trois briques changées : accepté")
def _():
    v = audit_idea(saine(changees=["topic", "seed", "substance"]), outliers_valides=3)
    assert v.ok, v.fails


@cas("aucune constante : avertissement")
def _():
    v = audit_idea(saine(constantes=["format", "arc"]), outliers_valides=3)
    assert v.ok and any("peu-de-constantes" in w for w in v.warns), v.warns


@cas("original sans outlier : avertissement nommé")
def _():
    v = audit_idea(saine(pipe=6, preuve="aucune donnée : pièce originale (EP01)"), outliers_valides=0)
    assert v.ok, v.fails
    assert any("original-sans-données" in w for w in v.warns), v.warns


@cas("tuyau 5 (non-outlier) : averti, jamais refusé")
def _():
    v = audit_idea(saine(pipe=5, preuve="concurrent B · 900 vues pour 3 000 de moyenne (20/09)"),
                   outliers_valides=1)
    assert v.ok and any("concurrent-sans-perf" in w for w in v.warns), v.warns


@cas("lot sans donnée validée : le lot le dit")
def _():
    lot = [saine(pipe=6, preuve="aucune donnée : original"), saine(ident="IDEA-02", pipe=6,
                                                                   preuve="aucune donnée")]
    v = audit(lot, outliers_valides=0)
    assert any("aucune-idée-validée" in w for w in v.warns), v.warns
    assert any("origine-en-série" in w for w in v.warns), v.warns


@cas("lot vide : refusé")
def _():
    v = audit([], outliers_valides=0)
    assert "lot vide" in " ".join(v.fails), v.fails


@cas("un timecode n'est pas une métrique")
def _():
    v = audit_idea(saine(pipe=3, preuve="BONT, la séquence [≈5:00] — vues inconnues"), outliers_valides=0)
    assert v.ok, v.fails
    assert any("preuve-sans-chiffre" in w for w in v.warns), v.warns


@cas("une section de prose n'est pas une idée")
def _():
    texte = """## IDEA-01 · une idée
- pipe: 6
- topic: fiche Google d'un opticien
- seed: Une fiche vide fait passer au suivant
- substance: trois captures datées
- cible: opticien de Douala, 35–54 ans
- preuve: aucune donnée : original
- briques_constantes: format, arc, mise en page, mascotte, voix, CTA
- briques_changees: topic, seed, substance

## Ce que le lot ne contient pas
- aucune idée validée
"""
    idees, _ = parse(texte)
    assert len(idees) == 1, [i.ident for i in idees]


@cas("lecture markdown : pipe, briques et outliers")
def _():
    texte = """# Lot

outliers_validés: 4

## IDEA-07 · une accroche
- pipe: 2
- topic: fiche Google
- seed: Une fiche complète fait rappeler, une fiche vide fait passer au suivant
- substance: trois captures datées
- cible: opticien de Douala, 35–54 ans
- preuve: concurrent A · 41 000 vues (12/10)
- briques_constantes: format, arc, mise en page, mascotte, voix, CTA
- briques_changees: topic, substance
"""
    idees, outliers = parse(texte)
    assert outliers == 4, outliers
    assert len(idees) == 1 and idees[0].pipe == 2, idees
    assert len(idees[0].constantes) == 6 and idees[0].changees == ["topic", "substance"], idees[0]
    assert audit(idees, outliers).ok


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
