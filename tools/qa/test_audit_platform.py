#!/usr/bin/env python3
"""Banc de `audit_platform.py` — la porte des légendes par plateforme.

    python3 tools/qa/test_audit_platform.py

Chaque refus a son contre-exemple qui passe. La dernière famille vérifie la pièce réelle : le document du
26/10 doit passer, et son master doit être **mesuré**, pas supposé.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_platform import audit  # noqa: E402

CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn

    return enveloppe


CAP_TT = ("Votre patient tape « opticien Akwa ».\n"
          "Écrivez APERÇU sur WhatsApp : 677 78 96 31.\n\n"
          "#Douala #Cameroun #opticien #opticienDouala #lunettesDouala #AMKweb")

CAP_IG = ("Your patient Googles « opticien Akwa ».\n"
          "Write APERÇU on WhatsApp: +237 677 78 96 31.\n\n"
          "#Douala #Cameroon #Optician #Optometry #Eyewear #AMKweb")

TT = f"""### 2.1 La légende

```text
{CAP_TT}
```

### 2.3 Les sous-titres — manuels, jamais automatiques

```text
0,0 – 5,0 s   Votre patient tape opticien Akwa.
```

### 2.5 Le commentaire épinglé

```text
677 78 96 31 — écrivez APERÇU.
```

"""

IG = f"""### 3.2 La légende

```text
{CAP_IG}
```

**Alt text** : un personnage désigne les deux fiches.

| Lieu | Douala |
|---|---|
"""


def doc(tt: str = TT, ig: str = IG) -> str:
    return ("# Test\n\n## 1 · La question\n\nRien.\n\n"
            f"## 2 · TIKTOK\n\n{tt}\n## 3 · INSTAGRAM\n\n{ig}\n")


def _audit(texte: str, master: str | None = None):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(texte)
        chemin = f.name
    try:
        return audit(chemin, master)
    finally:
        Path(chemin).unlink(missing_ok=True)


def codes(v):
    return [f.split("]")[0].strip("[") for f in v.fails]


def wcodes(v):
    return [w.split("]")[0].strip("[") for w in v.warns]


@cas("un document complet passe")
def _():
    v = _audit(doc())
    assert v.ok, v.fails
    assert len(v.tags["tiktok"]) == 6 and len(v.tags["instagram"]) == 6
    return "6 + 6 hashtags"


@cas("une seule section → sections-manquantes")
def _():
    v = _audit("# Test\n\n## 2 · TIKTOK\n\n```text\n" + CAP_TT + "\n```\n")
    assert "sections-manquantes" in codes(v), codes(v)
    return "refusé"


@cas("deux hashtags → hashtags-hors-borne")
def _():
    v = _audit(doc(tt=TT.replace("#Douala #Cameroun #opticien #opticienDouala #lunettesDouala #AMKweb",
                                 "#Douala #AMKweb")))
    assert "hashtags-hors-borne" in codes(v), codes(v)
    return "refusé à 2"


@cas("neuf hashtags → hashtags-hors-borne")
def _():
    trop = "#Douala #Cameroun #opticien #a #b #c #d #AMKweb #extra"
    v = _audit(doc(tt=TT.replace("#Douala #Cameroun #opticien #opticienDouala #lunettesDouala #AMKweb", trop)))
    assert "hashtags-hors-borne" in codes(v), codes(v)
    return "refusé à 9"


@cas("sans ville → local-absent")
def _():
    v = _audit(doc(tt=TT.replace("#Douala #Cameroun ", "")))
    assert "local-absent" in codes(v), codes(v)
    return "refusé"


@cas("sans #AMKweb → marque-absente")
def _():
    v = _audit(doc(ig=IG.replace(" #AMKweb", "")))
    assert "marque-absente" in codes(v), codes(v)
    return "refusé"


@cas("sans APERÇU → mot-cle-absent")
def _():
    v = _audit(doc(tt=TT.replace("Écrivez APERÇU", "Écrivez-nous")))
    assert "mot-cle-absent" in codes(v), codes(v)
    return "refusé"


@cas("un prix → prix-dans-la-legende")
def _():
    v = _audit(doc(tt=TT.replace("677 78 96 31.", "677 78 96 31. 250 000 FCFA.")))
    assert "prix-dans-la-legende" in codes(v), codes(v)
    return "refusé"


@cas("#fyp → mendicite")
def _():
    v = _audit(doc(tt=TT.replace("#Douala", "#fyp #Douala")))
    assert "mendicite" in codes(v), codes(v)
    return "refusé"


@cas("deux actions → cta-multiple")
def _():
    v = _audit(doc(tt=TT.replace("Écrivez APERÇU", "Écrivez APERÇU, puis appelez-moi")))
    assert "cta-multiple" in codes(v), codes(v)
    return "refusé"


@cas("aucune mention de sous-titres manuels → sous-titres-auto")
def _():
    v = _audit(doc(tt=TT.replace("manuels, jamais automatiques", "comme on peut")))
    assert "sous-titres-auto" in codes(v), codes(v)
    return "refusé"


@cas("pas de commentaire épinglé → epingle-absent")
def _():
    tt = TT.split("### 2.5")[0]
    v = _audit(doc(tt=tt))
    assert "epingle-absent" in codes(v), codes(v)
    return "refusé"


@cas("légende Instagram en français → langue-instagram")
def _():
    fr = ("Votre patient tape opticien Akwa. Écrivez APERÇU sur WhatsApp : 677 78 96 31.\n"
          "#Douala #Cameroun #opticien #AMKweb")
    v = _audit(doc(ig=IG.replace(CAP_IG, fr)))
    assert "langue-instagram" in codes(v), codes(v)
    return "refusé"


@cas("sans alt text → alt-absent")
def _():
    v = _audit(doc(ig=IG.replace("**Alt text**", "**Note**")))
    assert "alt-absent" in codes(v), codes(v)
    return "refusé"


@cas("master de 23,7 s → coupe-tiktok-manquante (avertissement, pas refus)")
def _():
    racine = Path(__file__).resolve().parents[2]
    master = racine / "content/reels/ep01/ep01-v6.mp4"
    v = _audit(doc(), str(master))
    assert v.ok, v.fails
    assert "coupe-tiktok-manquante" in wcodes(v), v.warns
    assert v.duree is not None and 23.0 <= v.duree <= 24.0, v.duree
    return f"averti, master {v.duree} s"


@cas("le document réel du 26/10 passe")
def _():
    racine = Path(__file__).resolve().parents[2]
    kit = racine / "content/reels/ep01/PUBLICATION-TIKTOK-INSTAGRAM-2026-10-26.md"
    master = racine / "content/reels/ep01/ep01-v6.mp4"
    v = audit(kit, master)
    assert v.ok, v.fails
    assert len(v.tags["tiktok"]) == 6 and len(v.tags["instagram"]) == 7, v.tags
    assert v.duree is not None, (
        "aucun ffmpeg : `pip install --break-system-packages imageio-ffmpeg` (content/reels/README §2)"
    )
    return f"tiktok {len(v.tags['tiktok'])} · ig {len(v.tags['instagram'])} · master {v.duree} s"


def main() -> int:
    ko = 0
    for nom, fn in CAS:
        try:
            print(f"  ✓ {nom} — {fn()}")
        except AssertionError as e:
            ko += 1
            print(f"  ✗ {nom} — {e}")
        except Exception as e:  # noqa: BLE001
            ko += 1
            print(f"  ✗ {nom} — {type(e).__name__}: {e}")
    total = len(CAS)
    print(f"\n{'✓' if not ko else '✗'} {total - ko}/{total}")
    return 1 if ko else 0


if __name__ == "__main__":
    raise SystemExit(main())
