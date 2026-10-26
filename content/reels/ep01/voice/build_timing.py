#!/usr/bin/env python3
"""build_timing — mesure la voix, décide des durées, refuse si le réel dépasse le plafond.

Règle (tour 145) : **la voix n'est jamais coupée** ; le beat s'allonge jusqu'à elle. Mais le
plafond de 25 s (`knowledge/STORY-ARC-2026-10-25.md` §3, règle V8) n'est pas négociable : si
l'ensemble ne tient pas, ce script **échoue** en nommant le beat à raccourcir. On coupe le texte,
pas la voix — et jamais l'inverse.

    python3 content/reels/ep01/voice/build_timing.py
"""
from __future__ import annotations

import array
import json
import math
import os
import subprocess
import sys

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
PLAFOND = 25.0
MARGE = 0.30  # respiration après la voix
RMS_MIN = 0.02  # en dessous, le clip est muet : une synthèse « réussie » peut rendre du silence

# durée visée · cime · forme  (la géométrie de l'arc : premier pic à 5,0 s exactement)
# Les durées visées de la v5 sont **mesurées sur la voix nettoyée** (silences retirés), pas rêvées :
# cette voix parle à ~0,45 s/mot, donc 25 s = ~50 mots, pas 65. Total 24,15 s.
PLAN = {
    "hook": (5.0, 70, "contexte"),
    "spike1": (3.46, 92, "contraste"),   # v6 : preuve prononcée, phrase courte
    "release1": (3.19, 58, "relache"),   # v6 : le cadeau (réciprocité) au beat 3
    "spike2": (3.77, 88, "contraste"),   # v6 : le rehook
    "release2": (2.90, 60, "relache"),   # v6 : le mécanisme (autorité par le diagnostic)
    "cta": (4.19, 95, "appel"),          # v6 : le CTA porte sa récompense, mais l'arc plafonne à 4,5 s
}
ORDRE = list(PLAN)

# Le beat SANS voix. Ce n'est pas un trou : c'est le souffle avant la sortie. Il est déclaré ici,
# donc la porte audio le sait — un silence non déclaré, lui, est un défaut.
SOUFFLE: set[str] = set()  # plus aucun beat muet : release2 porte le conseil gratuit


def rms(ff: str, path: str) -> float:
    """Le niveau réel du clip. Un TTS qui rend un fichier de 9 Ko peut rendre du silence."""
    raw = subprocess.run(
        [ff, "-i", path, "-f", "s16le", "-ac", "1", "-ar", "8000", "-"],
        capture_output=True,
    ).stdout
    a = array.array("h")
    a.frombytes(raw)
    if not len(a):
        return 0.0
    return math.sqrt(sum(x * x for x in a) / len(a)) / 32768


def duree(ff: str, path: str) -> float:
    out = subprocess.run([ff, "-i", path], capture_output=True, text=True).stderr
    hms = out.split("Duration:")[1].split(",")[0].strip()
    h, m, s = hms.split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)


def main() -> int:
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    beats, total, muets = [], 0.0, []
    for i, name in enumerate(ORDRE, start=1):
        fichier = next(f for f in sorted(os.listdir(HERE)) if f.startswith(f"b{i}-") and f.endswith(".mp3"))
        chemin = os.path.join(HERE, fichier)
        voix = duree(ff, chemin)
        niveau = rms(ff, chemin)
        cible, cime, forme = PLAN[name]
        souffle = name in SOUFFLE
        if niveau < RMS_MIN and not souffle:
            muets.append(f"{name} ({fichier}, RMS {niveau:.4f})")
        finale = round(cible if souffle else max(cible, voix + MARGE), 2)
        total += finale
        beats.append(
            {
                "name": name,
                "file": None if souffle else fichier,
                "voice": None if souffle else round(voix, 3),
                "rms": None if souffle else round(niveau, 4),
                "breath": souffle,
                "duration": finale,
                "peak": cime,
                "kind": forme,
                "over": round(max(0.0, finale - cible), 2),
            }
        )
        etat = "souffle (sans voix)" if souffle else f"voix {voix:5.2f}s RMS {niveau:.3f}"
        print(f"{name:9} {fichier:16} {etat:26} visé {cible:4.1f}s → {finale:5.2f}s")

    if muets:
        print("\n⛔ PORTE FERMÉE : clip(s) muet(s) — la synthèse a rendu du silence, à régénérer :")
        for m in muets:
            print(f"   · {m}")
        return 1

    print(f"\ntotal {total:.2f}s · plafond {PLAFOND:.0f}s")
    if total > PLAFOND:
        print("\n⛔ PORTE FERMÉE : le réel dépasse le plafond. Raccourcir le TEXTE des beats "
              "les plus lourds (pas la voix) :")
        for b in sorted(beats, key=lambda b: -b["over"])[:3]:
            if b["over"] > 0:
                print(f"   · {b['name']} : {b['over']:.2f}s de trop — « {b['file']} »")
        return 1

    json.dump(
        {
            "_comment": "Durées mesurées sur la voix (build_timing.py). Le beat s'allonge jusqu'à "
                        "la voix ; la voix n'est jamais coupée. Plafond 25 s vérifié à l'écriture.",
            "total": round(total, 2),
            "beats": beats,
        },
        open(os.path.join(HERE, "timing.json"), "w", encoding="utf-8"),
        indent=2,
        ensure_ascii=False,
    )
    print("✅ timing.json écrit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
