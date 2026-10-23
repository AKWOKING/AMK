#!/usr/bin/env python3
"""Récapitulatif de mise en ligne DM OPTIQUE — raccourci vers le moteur commun.

    python3 tools/ops/make_recap_dm.py                       # octobre 2026, sortie datée
    python3 tools/ops/make_recap_dm.py --data <json> --out <pdf>

Toute la mise en page vit dans `make_recap.py` (le même moteur pour tous les clients) ; ce fichier ne
fixe que les deux chemins de DM OPTIQUE, pour que la commande historique continue de marcher.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from make_recap import main as recap_main

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "clients/dm-optic/launch/recap-2026-10.json"
OUT = ROOT / "clients/dm-optic/launch/RECAP-MISE-EN-LIGNE-2026-10-23.pdf"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Récapitulatif DM OPTIQUE (une page A4)")
    ap.add_argument("--data", type=Path, default=DATA)
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args()
    recap_main(["--data", str(a.data), "--out", str(a.out)])
