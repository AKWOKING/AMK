#!/usr/bin/env python3
"""audit_ideas — la porte de l'IDÉE (`knowledge/IDEA-PIPES-2026-10-25.md`).

Le dépôt savait déjà vérifier le **rôle** d'une pièce (`audit_trust.py`) et sa **forme**
(`audit_reel.py`). Il ne vérifiait pas ce qui vient avant les deux : **l'idée**. La source du 25/10
(« The 6 Idea Pipes ») dit que la différence entre 10 000 et 1 000 000 de vues se joue là, et que la
plupart des échecs sont des idées « pas assez intéressantes ou pas assez utiles » — pas des montages.

Une idée est **trois choses** : un *topic*, un *seed* (la phrase-tête, contre-intuitive) et une
*substance* (les faits, exemples, opinions qui la portent). Elle vient d'un des **six tuyaux**, du plus
prouvé au plus risqué (1 nos outliers · 2 ceux des concurrents · 3 les autres médias · 4 l'actualité de
la catégorie · 5 les non-outliers des concurrents · 6 les originaux). Et on **remixe** : on garde 8 à 10
briques constantes, on en change 1 à 3.

Ce que cette porte vérifie, brique par brique :

- le **tuyau** existe, et il porte **la preuve qu'il promet** (un tuyau 1 ou 2 sans chiffre n'est pas un
  outlier, c'est un souvenir ; une actualité sans date n'est pas une actualité) ;
- l'idée a ses **trois parties**, et le seed n'est pas le topic répété ;
- la **cible** est un acheteur nommable, pas « tout le monde » ;
- le **remix** est un remix : ≤ 3 briques changées, ≥ 6 constantes ;
- et un **original** (tuyau 6) est signalé comme tel quand la chaîne n'a encore aucun outlier à elle.

Ce qu'elle ne fait pas : juger si l'idée est *bonne*. Elle vérifie qu'on sait **d'où elle vient** et
**ce qu'on a changé**. Le goût reste humain ; la provenance, non.

Usage :

    from audit_ideas import Idea, audit
    audit([Idea(ident="IDEA-01", pipe=2, topic="fiche Google", seed="…", substance="…",
                cible="opticien de Douala, 35–54 ans", preuve="concurrent A, 41 000 vues (12/10)",
                constantes=["format", "arc", "hook"], changees=["topic"])])

    python3 tools/qa/audit_ideas.py content/ideas/SHORTLIST-2026-10-25.md
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── seuils ───────────────────────────────────────────────────────────────────────────────────
# Les six tuyaux et leur ordre viennent de la source (§3 du document). Le seuil de briques est
# **notre** lecture de sa règle : « hold most of the lego bricks constant, change just 1-2 » — on
# tolère 3, jamais 4.
PIPES = {1, 2, 3, 4, 5, 6}
PIPES_A_CHIFFRE = {1, 2}          # un outlier sans chiffre n'en est pas un
PIPES_A_RISQUE = {5}              # non-outliers : l'idée est bonne, l'exécution a échoué — pari
BRIQUES_CHANGEES_MAX = 3
BRIQUES_CONSTANTES_MIN = 6
SEED_MOTS_MIN = 5
CIBLE_MOTS_MIN = 4
SEED_LONGUEUR_MAX = 200
DATE = re.compile(r"(\d{4}-\d{2}-\d{2})|(\d{2}/\d{2}(/\d{2,4})?)")
# Un timecode (« [≈5:00] ») n'est pas une mesure de performance : la source cite ses fenêtres par
# minute:seconde, et la première version de cette porte comptait « 5:00 » comme un chiffre de vues.
TIMECODE = re.compile(r"\[?[≈~]?\d{1,2}:\d{2}(:\d{2})?\]?")
CHIFFRE = re.compile(r"\d")


def a_une_metrique(texte: str) -> bool:
    """Vrai si le texte porte un **chiffre de performance** — et non une date.

    Première version de cette porte : `re.search(r"\d", preuve)`. Elle comptait « 23/10 » comme un
    chiffre de vues, donc un tuyau 2 sans aucune donnée passait. Les dates sont retirées d'abord ;
    il faut ensuite un nombre d'au moins deux chiffres (156 vues, 41 000, 18 %).
    """
    sans_dates = TIMECODE.sub(" ", DATE.sub(" ", texte))
    return any(len(m) >= 2 for m in re.findall(r"\d+", sans_dates))

CHAMPS = ("topic", "seed", "substance", "cible", "preuve")


@dataclass
class Idea:
    ident: str
    pipe: int
    topic: str = ""
    seed: str = ""
    substance: str = ""
    cible: str = ""
    preuve: str = ""
    constantes: list[str] = field(default_factory=list)
    changees: list[str] = field(default_factory=list)

    @property
    def provenance(self) -> str:
        return {
            1: "nos outliers",
            2: "outliers des concurrents",
            3: "autres médias",
            4: "actualité de la catégorie",
            5: "non-outliers des concurrents",
            6: "original — aucune donnée",
        }.get(self.pipe, "tuyau inconnu")


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.fails


def _mots(texte: str) -> int:
    return len([m for m in re.split(r"\s+", texte.strip()) if m])


def audit_idea(i: Idea, outliers_valides: int = 0) -> Verdict:
    """Verdict pour une idée. `outliers_valides` = ce que la watchlist a réellement produit."""
    v = Verdict()
    nom = i.ident or "(sans nom)"

    if i.pipe not in PIPES:
        v.fails.append(f"{nom} · pipe-inconnu — {i.pipe!r} n'est pas un tuyau (1–6)")
        return v

    manquants = [c for c in CHAMPS if not getattr(i, c).strip()]
    if manquants:
        v.fails.append(f"{nom} · incomplet — il manque {', '.join(manquants)}")
    if "NEEDS DATA" in i.preuve.upper():
        v.fails.append(f"{nom} · preuve-manquante — « [NEEDS DATA] » n'est pas une source : "
                       "l'idée reste en recherche, elle n'entre pas en production")

    if i.seed.strip() and _mots(i.seed) < SEED_MOTS_MIN:
        v.fails.append(f"{nom} · seed-mou — {_mots(i.seed)} mot(s) : un seed est une phrase-tête, "
                       f"pas un intitulé (≥ {SEED_MOTS_MIN} mots)")
    if len(i.seed) > SEED_LONGUEUR_MAX:
        v.fails.append(f"{nom} · seed-long — {len(i.seed)} caractères : ce n'est plus une ligne")
    if i.seed.strip() and i.topic.strip() and \
            i.seed.strip().lower() == i.topic.strip().lower():
        v.fails.append(f"{nom} · seed=topic — le seed doit apporter la prise de position, "
                       "pas répéter le sujet")

    if i.cible.strip() and _mots(i.cible) < CIBLE_MOTS_MIN:
        v.fails.append(f"{nom} · cible-mou — « {i.cible} » ne nomme pas un acheteur "
                       f"(≥ {CIBLE_MOTS_MIN} mots : métier, ville, situation)")

    if i.pipe in PIPES_A_CHIFFRE and not a_une_metrique(i.preuve):
        v.fails.append(f"{nom} · pipe-sans-chiffre — un tuyau {i.pipe} ({i.provenance}) promet des "
                       "données : sans vues ni score d'outlier, ce n'est pas un outlier")
    if i.pipe == 3 and not a_une_metrique(i.preuve):
        v.warns.append(f"{nom} · preuve-sans-chiffre — autre média sans métrique : "
                       "on garde l'idée, on ne la dit pas validée")
    if i.pipe == 4 and not DATE.search(i.preuve):
        v.warns.append(f"{nom} · actualité-sans-date — une news sans date est un souvenir")
    if i.pipe in PIPES_A_RISQUE:
        v.warns.append(f"{nom} · concurrent-sans-perf — tuyau 5 : l'idée est bonne mais "
                       "personne n'a prouvé qu'elle marche ; exécution à surveiller")

    if len(i.changees) > BRIQUES_CHANGEES_MAX:
        v.fails.append(f"{nom} · trop-de-briques — {len(i.changees)} briques changées "
                       f"(max {BRIQUES_CHANGEES_MAX}) : ce n'est plus un remix, c'est un original "
                       "déguisé (tuyau 6)")
    if i.changees == [] and i.constantes:
        v.warns.append(f"{nom} · copie — aucune brique changée : republier n'est pas remixer")
    if i.constantes and len(i.constantes) < BRIQUES_CONSTANTES_MIN:
        v.warns.append(f"{nom} · peu-de-constantes — {len(i.constantes)} constante(s) "
                       f"(recommandé ≥ {BRIQUES_CONSTANTES_MIN}) : le risque monte")
    if i.pipe == 6 and outliers_valides == 0:
        v.warns.append(f"{nom} · original-sans-données — tuyau 6 alors que la chaîne n'a "
                       "aucun outlier : c'est le tuyau le plus risqué, et le plus mal placé "
                       "pour commencer")

    return v


def audit(idees: list[Idea], outliers_valides: int = 0) -> Verdict:
    """Verdict du lot : les idées, plus deux lectures d'ensemble."""
    v = Verdict()
    for i in idees:
        sous = audit_idea(i, outliers_valides)
        v.fails += sous.fails
        v.warns += sous.warns
    if not idees:
        v.fails.append("lot vide — aucune idée : un lot de recherche en produit 10 à 20")
        return v
    validees = [i for i in idees
                if i.pipe in {1, 2} or (i.pipe == 3 and a_une_metrique(i.preuve))]
    if not validees:
        v.warns.append(f"aucune-idée-validée — {len(idees)} idée(s), 0 avec des données : "
                       "le lot est un brouillon de tuyau 6, pas un résultat de recherche")
    originaux = [i for i in idees if i.pipe == 6]
    if len(originaux) > len(idees) / 2:
        v.warns.append(f"origine-en-série — {len(originaux)}/{len(idees)} en tuyau 6 : "
                       "c'est exactement le point de départ que la source décrit comme perdant")
    return v


# ── lecture d'un fichier de lot ──────────────────────────────────────────────────────────────
_LIGNE = re.compile(r"^\s*[-*]\s*([a-z_éèà]+)\s*:\s*(.+?)\s*$", re.I)


def parse(texte: str) -> tuple[list[Idea], int]:
    """Lit un lot markdown : `## IDEA-xx` puis des lignes `- clé: valeur`.

    En-tête facultatif : `outliers_validés: N` (ce que la watchlist a produit).
    """
    idees: list[Idea] = []
    outliers = 0
    courant: Idea | None = None
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            titre = ligne[3:].strip()
            # Seuls les blocs « IDEA-… » sont des idées. Une section de commentaire (« ## Ce que le
            # lot ne contient pas ») n'en est pas une : la première version la comptait comme une
            # idée sans tuyau, et le lot échouait sur sa propre prose.
            if titre.upper().startswith("IDEA"):
                courant = Idea(ident=titre.split("·")[0].strip(), pipe=-1)
                idees.append(courant)
            else:
                courant = None
            continue
        m = _LIGNE.match(ligne)
        if not m:
            if ligne.strip().lower().startswith("outliers_valid"):
                chiffres = re.findall(r"\d+", ligne)
                outliers = int(chiffres[0]) if chiffres else 0
            continue
        cle, valeur = m.group(1).strip().lower(), m.group(2).strip()
        if cle.startswith("outliers"):
            chiffres = re.findall(r"\d+", valeur)
            outliers = int(chiffres[0]) if chiffres else 0
            continue
        if courant is None:
            continue
        if cle in ("pipe", "tuyau"):
            chiffres = re.findall(r"\d+", valeur)
            courant.pipe = int(chiffres[0]) if chiffres else -1
        elif cle in ("briques_constantes", "constantes"):
            courant.constantes = [b.strip() for b in valeur.split(",") if b.strip()]
        elif cle in ("briques_changees", "changees", "changées"):
            courant.changees = [b.strip() for b in valeur.split(",") if b.strip()]
        elif cle in CHAMPS:
            setattr(courant, cle, valeur)
    return idees, outliers


def load(path: str) -> tuple[list[Idea], int]:
    return parse(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    echecs = 0
    for path in argv:
        idees, outliers = load(path)
        v = audit(idees, outliers)
        print(f"{'✓' if v.ok else '✗'} {Path(path).name} · {len(idees)} idée(s) · "
              f"outliers validés : {outliers}")
        for i in idees:
            sous = audit_idea(i, outliers)
            marque = "✓" if sous.ok else "✗"
            print(f"   {marque} {i.ident:8} tuyau {i.pipe} ({i.provenance}) · "
                  f"{len(i.constantes)} constante(s) · {len(i.changees)} changement(s)")
            if not sous.ok:
                echecs += 1
        if v.fails:
            for f in v.fails:
                print(f"   ⛔ {f}")
        for w in v.warns:
            print(f"   ⚠ {w}")
        if not v.ok:
            echecs += 1
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
