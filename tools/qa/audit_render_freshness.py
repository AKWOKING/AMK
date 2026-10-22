#!/usr/bin/env python3
"""audit_render_freshness — le MP4 correspond-il au storyboard qui l'a produit ?

Pourquoi ce portique existe
---------------------------
Le 22/10/2026, `ugc-03.mp4` est parti en revue client avec une carte qui comptait les montures et
annonçait des montants consultables. Le storyboard `ugc-03.json` avait pourtant été nettoyé le matin
même (commit `542ee03`). `audit_claims.py` a répondu « aucune infraction » — à juste titre : **il lit le
storyboard, pas les images.** Le fichier montré était l'ancien rendu.

Deux méthodes ont été essayées et écartées :

* comparer les **mtime** — une checkout Git les égalise, aucune information ;
* comparer les **dates de commit** — les deux fichiers appartiennent au même commit, donc même date.

Ce qui marche : le rendu écrit une **preuve** (`<nom>.render.json`) contenant l'empreinte SHA-256 du
storyboard utilisé. Le portique recalcule l'empreinte actuelle et la compare. Une différence = le
storyboard a changé depuis le rendu = **PÉRIMÉ**. Pas de preuve = **NON TRAÇABLE** : on ne sait pas,
donc on ne publie pas.

Usage
-----
    python3 tools/qa/audit_render_freshness.py            # tout le dépôt
    python3 tools/qa/audit_render_freshness.py <dossier>

Sortie : code 1 si au moins un MP4 est PÉRIMÉ ou NON TRAÇABLE, 0 sinon.
Les MP4 sans storyboard (montages ffmpeg classiques) sont ignorés : ils ne sont pas concernés.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    scope = Path(argv[1]).resolve() if len(argv) > 1 else ROOT
    ok, stale, untraced, skipped = 0, [], [], 0

    for mp4 in sorted(scope.rglob("*.mp4")):
        if ".git" in mp4.parts:
            continue
        storyboard = mp4.with_suffix(".json")
        if not storyboard.exists():
            skipped += 1
            continue

        proof_path = mp4.with_suffix(".render.json")
        if not proof_path.exists():
            untraced.append((mp4, "aucune preuve de rendu"))
            continue

        try:
            proof = json.loads(proof_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            untraced.append((mp4, "preuve de rendu illisible"))
            continue

        if proof.get("storyboard_sha256") != sha256(storyboard):
            stale.append((mp4, "le storyboard a changé depuis le rendu"))
            continue
        ok += 1

    print(f"\naudit fraîcheur des rendus · {ok} à jour · {len(stale)} périmé(s) · "
          f"{len(untraced)} non traçable(s) · {skipped} MP4 sans storyboard")
    for mp4, why in stale:
        print(f"  ✗  {mp4.relative_to(ROOT)} — {why}")
    for mp4, why in untraced:
        print(f"  ?  {mp4.relative_to(ROOT)} — {why}")

    if stale or untraced:
        print("\nVERDICT : BLOQUÉ — re-rendre avant toute publication, puis relire image par image\n")
        return 1
    print("\nVERDICT : OK — chaque MP4 correspond à son storyboard\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
