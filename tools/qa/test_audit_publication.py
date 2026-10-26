#!/usr/bin/env python3
"""Banc de `audit_publication.py` — la porte de la publication.

    python3 tools/qa/test_audit_publication.py

Chaque refus a son **contre-exemple qui passe**. La dernière famille est la seule qui compte : le kit réel
de ce matin (`content/reels/ep01/PUBLICATION-2026-10-26.md`) passe, et son master est **mesuré** à 23,7 s.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_publication import audit  # noqa: E402

CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn

    return enveloppe


LEGENDE = (
    "Votre patient tape « opticien Akwa ». Il appelle l'autre.\n"
    "\n"
    "Sa fiche a douze avis. La vôtre n'a qu'un nom.\n"
    "\n"
    "Écrivez APERÇU sur WhatsApp : 677 78 96 31. Vous voyez votre page avant de payer."
)

ACCUEIL = (
    "> **Bonjour — vous avez écrit APERÇU, c'est bien ça. Le nom de votre cabinet ?**\n"
    "> (puis) Le quartier, et je regarde ce que Google affiche pour vous.\n"
    "> M4 : « Je vous envoie la page demain à 10 h, ici. »"
)

TABLE = (
    "| Moment | Vues | Messages reçus | dont **APERÇU** | Conversations qualifiées | Aperçus envoyés |\n"
    "|---|---|---|---|---|---|\n"
    "| 12 h | | | | | |"
)


def kit(légende: str | None = None, accueil: str | None = None, contact: str | None = None,
        table: str | None = None) -> str:
    légende = LEGENDE if légende is None else légende
    accueil = ACCUEIL if accueil is None else accueil
    contact = "https://wa.me/237677789631" if contact is None else contact
    table = TABLE if table is None else table
    return (
        "# PUBLICATION — test\n\n"
        "## 1 · Les gestes\n\nRien.\n\n"
        "## 2 · La légende (mot pour mot)\n\n"
        f"```text\n{légende}\n```\n\n"
        "## 3 · Épinglé\n\n> Une précision.\n\n"
        "## 4 · La réponse d'accueil\n\n"
        f"{accueil}\n\n"
        "## 5 · Le compteur\n\n"
        f"{table}\n\n"
        f"Le lien : {contact}\n"
    )


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


# ── le kit sain ─────────────────────────────────────────────────────────────────────────────────

@cas("un kit complet passe")
def _():
    v = _audit(kit())
    assert v.ok, v.fails
    assert v.blocs == 3, v.blocs
    return "3 blocs, 0 refus"


# ── la légende ──────────────────────────────────────────────────────────────────────────────────

@cas("pas de bloc de code → legende-absente")
def _():
    v = _audit(kit().replace("```text", "texte :").replace("```\n\n## 3", "\n## 3"))
    assert "legende-absente" in codes(v), codes(v)
    return "refusé"


@cas("première ligne de 130 caractères → accroche-longue")
def _():
    v = _audit(kit(légende="Votre patient tape opticien Akwa et il appelle l'autre cabinet du quartier, "
                            "celui qui a douze avis et un site.\n\nÉcrivez APERÇU sur WhatsApp : 677 78 96 31."))
    assert "accroche-longue" in codes(v), codes(v)
    return "refusé à 130 caractères"


@cas("première ligne de 99 caractères → passe")
def _():
    ligne = "Votre patient tape opticien Akwa, et il appelle l'autre cabinet du quartier." # 76
    v = _audit(kit(légende=ligne + "\n\nÉcrivez APERÇU sur WhatsApp : 677 78 96 31."))
    assert "accroche-longue" not in codes(v), codes(v)
    return "accepté"


@cas("aucun verbe d'action → cta-absent")
def _():
    v = _audit(kit(légende="Votre patient tape opticien Akwa. APERÇU, c'est le mot du jour."))
    assert "cta-absent" in codes(v), codes(v)
    return "refusé"


@cas("deux actions → deux-cta")
def _():
    v = _audit(kit(légende="Écrivez APERÇU sur WhatsApp : 677 78 96 31. Envoyez aussi le nom du cabinet."))
    assert "deux-cta" in codes(v), codes(v)
    return "refusé"


@cas("sans le mot-clé → mot-cle-absent")
def _():
    v = _audit(kit(légende="Votre patient tape opticien Akwa. Écrivez-moi sur WhatsApp : 677 78 96 31."))
    assert "mot-cle-absent" in codes(v), codes(v)
    return "refusé"


@cas("un prix dans la légende → prix-dans-la-legende")
def _():
    for legende in ("Écrivez APERÇU. Le site coûte 250 000 FCFA.",
                    "Écrivez APERÇU. À partir de 150 k.",
                    "Écrivez APERÇU. Le prix se dit en privé."):
        v = _audit(kit(légende=legende))
        assert "prix-dans-la-legende" in codes(v), (legende, codes(v))
    return "3 formes refusées : FCFA, k, « prix »"


@cas("une promesse de résultat → promesse")
def _():
    v = _audit(kit(légende="Écrivez APERÇU sur WhatsApp : 677 78 96 31. Résultat garanti."))
    assert "promesse" in codes(v), codes(v)
    return "refusé"


# ── la réponse d'accueil ────────────────────────────────────────────────────────────────────────

@cas("le nom du cabinet arrive en deuxième ligne → nom-tardif")
def _():
    v = _audit(kit(accueil="> Bonjour, merci de votre message.\n> Le nom de votre cabinet ?\n> Livraison à 10 h."))
    assert "nom-tardif" in codes(v), codes(v)
    return "refusé"


@cas("le nom et la question sur la même ligne → passe")
def _():
    v = _audit(kit(accueil="> Bonjour — vous avez écrit APERÇU. Le nom du cabinet ?\n> Je vous envoie la page demain à 10 h."))
    assert "nom-tardif" not in codes(v), codes(v)
    return "accepté"


@cas("aucune heure de livraison → delai-absent")
def _():
    v = _audit(kit(accueil="> Bonjour — le nom du cabinet ?\n> Je vous envoie la page dès que possible."))
    assert "delai-absent" in codes(v), codes(v)
    return "refusé"


@cas("« bientôt » avec une heure → averti, pas refusé")
def _():
    v = _audit(kit(accueil="> Bonjour — le nom du cabinet ?\n> Je vous envoie la page bientôt, demain à 10 h."))
    assert v.ok and "delai-flou" in wcodes(v), (v.fails, v.warns)
    return "accepté avec avertissement"


# ── le chemin et le compteur ───────────────────────────────────────────────────────────────────

@cas("ni lien ni numéro → lien-absent")
def _():
    v = _audit(kit(contact="WhatsApp de la page",
                   légende="Écrivez APERÇU sur WhatsApp. Vous voyez votre page avant de payer."))
    assert "lien-absent" in codes(v), codes(v)
    return "refusé"


@cas("le tableau perd sa colonne de décision → compteur-absent")
def _():
    v = _audit(kit(table="| Moment | Vues |\n|---|---|\n| 12 h | |"))
    assert "compteur-absent" in codes(v), codes(v)
    return "refusé"


# ── le master ──────────────────────────────────────────────────────────────────────────────────

@cas("master inexistant → master-absent")
def _():
    v = _audit(kit(), master="/tmp/nexiste-pas-9f3c.mp4")
    assert "master-absent" in codes(v), codes(v)
    return "refusé"


@cas("master de 26 s → master-trop-long")
def _():
    import shutil
    import imageio_ffmpeg  # type: ignore

    ffmpeg = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
    with tempfile.TemporaryDirectory() as d:
        mp4 = Path(d) / "long.mp4"
        subprocess.run([ffmpeg, "-y", "-f", "lavfi", "-i", "color=c=black:s=64x64:r=1:d=26",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(mp4)],
                       capture_output=True, check=True)
        v = _audit(kit(), master=str(mp4))
    assert "master-trop-long" in codes(v), (v.duree, codes(v))
    return f"refusé à {v.duree} s"


# ── la seule famille qui compte : la pièce réelle ─────────────────────────────────────────────

@cas("le kit réel et son master v6 passent, et la durée est mesurée")
def _():
    racine = Path(__file__).resolve().parents[2]
    kit_reel = racine / "content/reels/ep01/PUBLICATION-2026-10-26.md"
    master = racine / "content/reels/ep01/ep01-v6.mp4"
    assert kit_reel.exists(), kit_reel
    v = audit(kit_reel, master)
    assert v.ok, v.fails
    assert v.duree is not None and 23.0 <= v.duree <= 24.0, v.duree
    return f"✓ {v.blocs} blocs · master {v.duree} s"


def main() -> int:
    ko = 0
    for nom, fn in CAS:
        try:
            note = fn()
            print(f"  ✓ {nom} — {note}")
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
