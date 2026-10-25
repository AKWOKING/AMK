#!/usr/bin/env python3
"""audit_reel — la porte de l'arc moderne (`knowledge/STORY-ARC-2026-10-25.md`).

Une règle sans porte est un trou (ruling 109). Ce module vérifie la **forme** d'un réel avant
rendu : départ à 70, secousse entre 5 et 10 s, au moins trois cimes, un relâchement entre deux
cimes, CTA dans les quatre dernières secondes, chaque chiffre sourcé et daté.

Ce qu'il ne fait pas : juger le goût, la typographie ou la pertinence du sujet.

Usage :

    from audit_reel import Beat, audit
    problemes = audit(BEATS, duration=21.5)

    python3 tools/qa/audit_reel.py content/reels/ep01/make_ep01.py   # lit BEATS + DURATION
"""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Seuils, tous tirés de knowledge/STORY-ARC-2026-10-25.md (source : carrousel kallowaymarketing 23/10)
DEPART_MIN = 65          # slide 3 : « It starts at 70 out of 100 »
CONTEXTE_MAX = 5.0       # slide 3 : « the first 5 seconds need to establish rapid context »
PREMIER_PIC_MIN = 5.0    # slide 4 : « in the next 5-10 seconds »
PREMIER_PIC_MAX = 10.0
PIC_MIN = 85             # « spike the viewer to 90 » — on tolère 85
CREUX_MAX = 70           # un relâchement doit vraiment descendre
PICS_MIN = 3             # §3 règle 4 : décision maison, pas une citation de la source
CTA_FENETRE = 4.5        # §3 règle 5 : le CTA occupe les 4 dernières secondes
DUREE_MAX = 25.0         # règle V8 du dépôt
BEAT_MIN = 1.5           # en dessous, le texte n'est pas lisible
FORMES = {"contraste", "contraire", "chiffre", "appel", "contexte", "relache"}


@dataclass
class Beat:
    name: str
    start: float
    end: float
    peak: int
    kind: str | None = None
    fact: str | None = None
    source: str | None = None

    @property
    def duree(self) -> float:
        return round(self.end - self.start, 3)

    @property
    def is_pic(self) -> bool:
        return self.peak >= PIC_MIN


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


DATE = re.compile(r"\b(\d{2}/\d{2}/?\d{0,4}|20\d{2})\b")


def audit(beats: list[Beat], duration: float | None = None) -> Verdict:
    v = Verdict()
    if not beats:
        v.fail("vide", "aucun beat : rien à vérifier, donc rien à rendre")
        return v

    duration = duration or beats[-1].end

    # ── géométrie ───────────────────────────────────────────────────────────
    if abs(beats[0].start) > 1e-6:
        v.fail("depart", f"le premier beat commence à {beats[0].start:.1f} s, pas à 0")
    for a, b in zip(beats, beats[1:]):
        if b.start > a.end + 1e-6:
            v.fail("trou", f"{a.end:.1f} s → {b.start:.1f} s : trou sans image")
        if b.start < a.end - 1e-6:
            v.fail("chevauchement", f"{a.name} et {b.name} se chevauchent")
    for b in beats:
        if b.duree < BEAT_MIN:
            v.fail("court", f"{b.name} dure {b.duree:.1f} s (< {BEAT_MIN} s) : illisible")
        if b.kind and b.kind not in FORMES:
            v.fail("forme", f"{b.name} : forme « {b.kind} » inconnue (attendu : {sorted(FORMES)})")

    if duration > DUREE_MAX:
        v.fail("duree", f"{duration:.1f} s > {DUREE_MAX:.0f} s (règle V8)")

    # ── origine : jamais à zéro ─────────────────────────────────────────────
    premier = beats[0]
    if premier.peak < DEPART_MIN:
        v.fail(
            "depart-a-zero",
            f"ouverture à {premier.peak}/100 (< {DEPART_MIN}) : on démarre à zéro "
            "(slide 3 : « It doesn't start at zero »)",
        )
    if premier.kind == "contexte" and premier.duree > CONTEXTE_MAX:
        v.fail(
            "contexte-lent",
            f"le contexte dure {premier.duree:.1f} s (> {CONTEXTE_MAX:.0f} s) : "
            "la slide 3 exige un contexte rapide",
        )

    # ── la secousse : entre 5 et 10 s ───────────────────────────────────────
    pics = [b for b in beats if b.is_pic]
    if not pics:
        v.fail("aucun-pic", f"aucune cime ≥ {PIC_MIN}/100 : un réel plat ne retient personne")
    else:
        p1 = pics[0]
        if not (PREMIER_PIC_MIN <= p1.start <= PREMIER_PIC_MAX):
            v.fail(
                "premier-pic",
                f"première cime à {p1.start:.1f} s ; la slide 4 la veut entre "
                f"{PREMIER_PIC_MIN:.0f} et {PREMIER_PIC_MAX:.0f} s",
            )

    # ── l'empilement des cimes et les relâchements ──────────────────────────
    if len(pics) < PICS_MIN:
        v.fail("pics", f"{len(pics)} cime(s) ; notre plancher est {PICS_MIN} (slide 6 : "
                       "« stacking mini peaks »)")

    for a, b in zip(pics, pics[1:]):
        between = [x for x in beats if a.end <= x.start and x.end <= b.start]
        if not any(x.peak <= CREUX_MAX for x in between):
            v.fail(
                "sans-relachement",
                f"{a.name} → {b.name} : aucune descente sous {CREUX_MAX}/100 — "
                "« peak, release, peak » (slide 5)",
            )

    # ── le CTA est la dernière cime, pas le climax du milieu ───────────────
    dernier = beats[-1]
    if dernier.kind != "appel":
        v.fail("cta-absent", "le dernier beat n'est pas un appel : il n'y a pas de CTA")
    if dernier.duree > CTA_FENETRE:
        v.fail(
            "cta-long",
            f"le CTA dure {dernier.duree:.1f} s (> {CTA_FENETRE:.1f}) : il doit tenir "
            "dans les dernières secondes, pas occuper le reel",
        )
    if not dernier.is_pic:
        v.fail("cta-plat", f"le CTA culmine à {dernier.peak}/100 : une sortie doit être une cime")

    # ── les faits : sourcés et datés ────────────────────────────────────────
    for b in beats:
        if b.kind == "chiffre":
            if not b.fact:
                v.fail("chiffre-muet", f"{b.name} : forme « chiffre » sans fait")
            if not b.source:
                v.fail("chiffre-nu", f"{b.name} : un chiffre sans source est interdit")
            elif not DATE.search(b.source):
                v.fail("chiffre-non-date", f"{b.name} : source « {b.source} » sans date")
        if b.fact and b.kind in {"contraste", "contraire"} and not b.source:
            v.warn("fait-sans-source", f"{b.name} : le fait « {b.fact} » n'a pas de source nommée")

    return v


# ─────────────────────────────────────────────────────────────── CLI ──────────


def load_module(path: str):
    spec = importlib.util.spec_from_file_location("episode", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    echecs = 0
    for path in argv:
        mod = load_module(path)
        beats = getattr(mod, "BEATS", None)
        if beats is None:
            print(f"✗ {path} : pas de BEATS — l'épisode ne déclare pas sa forme")
            echecs += 1
            continue
        duration = getattr(mod, "DURATION", None) or beats[-1].end
        v = audit(beats, duration)
        nom = Path(path).parent.name
        if v.ok:
            pics = sum(1 for b in beats if b.is_pic)
            print(f"✓ {nom:8} {duration:.1f} s · {len(beats)} beats · {pics} cimes")
            for w in v.warns:
                print(f"   ⚠ {w}")
        else:
            echecs += 1
            print(f"✗ {nom} : PORTE FERMÉE")
            for f in v.fails:
                print(f"   ⛔ {f}")
            for w in v.warns:
                print(f"   ⚠ {w}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
