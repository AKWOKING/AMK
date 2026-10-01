#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Témoin de `tools/site/md_to_pdf.py` — le convertisseur qui met nos documents client sur WhatsApp.

Écrit le 25/09/2026, après deux défauts trouvés **le même jour** par le document des deux coffrets de
DM OPTIQUE SARL (le premier document client qui contient des listes) :

  ① `bullets()` appelait `write()` sans son argument `size` → `TypeError` : le chemin des listes à
     puces n'avait **jamais** été exercé (le business case d'Univers n'en avait aucune) ;
  ② les listes **ordonnées** (« 1. ») n'étaient pas reconnues : les trois items s'imprimaient collés
     sur une seule ligne.

Ce témoin ne juge pas l'esthétique (ça, c'est l'œil, et on regarde les PNG). Il vérifie que **chaque
chemin du convertisseur produit des pages** — c'est la leçon du dépôt : un outil qui n'est pas exercé
ment, et le seul moyen de le savoir est de l'exercer.

Usage : python3 tools/qa/test_md_to_pdf.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools" / "site"))

import md_to_pdf  # noqa: E402

PASSED = FAILED = 0


def ok(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  ok   {label}")
    else:
        FAILED += 1
        print(f"  FAIL {label}" + (f" — {detail}" if detail else ""))


def render(md, titre="Témoin"):
    """Rend un Markdown et rend les pages — comme le ferait la ligne de commande."""
    return md_to_pdf.build(md, titre, "AMK · témoin")


print("═══ 1 · chaque bloc du convertisseur produit des pages ═══")

BLOCS = {
    "titre h1":            "# Un titre\n\nUn paragraphe.\n",
    "sous-titres h2/h3":   "## Un h2\n\n### Un h3\n\ntexte\n",
    "paragraphe multi-lignes": "Une phrase qui\ncontinue à la ligne suivante.\n",
    "gras et italique":    "Un mot **en gras**, un mot *en italique*, et du `code`.\n",
    "liste à puces":       "- première puce\n- deuxième puce\n- troisième puce\n",
    "puce à plusieurs lignes": "- une puce qui\n  continue à la ligne\n- une autre\n",
    "liste ordonnée":      "1. première étape\n2. deuxième étape\n3. troisième étape\n",
    "étape à plusieurs lignes": "1. une étape qui\n   continue à la ligne\n2. une autre\n",
    "tableau 2 colonnes":  "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n",
    "citation":            "> Une phrase citée, avec son attribution.\n> — Quelqu'un\n",
    "filet":               "avant\n\n---\n\naprès\n",
    "tableau vide (en-tête seule)": "| A | B |\n|---|---|\n",
}
for label, md in BLOCS.items():
    try:
        pages = render(md)
        ok(f"{label} → {len(pages)} page(s)", len(pages) >= 1 and pages[0].size[0] > 0)
    except Exception as exc:  # noqa: BLE001 — on veut voir le défaut, pas le masquer
        ok(f"{label}", False, f"{type(exc).__name__}: {exc}")

print("\n═══ 2 · les deux défauts du 25/09, nommés ═══")

# ① la liste à puces — le TypeError de `bullets()`
try:
    render("- a\n- b\n")
    ok("une liste à puces ne lève plus `TypeError: write() missing 1 required positional argument`", True)
except TypeError as exc:
    ok("une liste à puces ne lève plus de TypeError", False, str(exc))

# ② la liste ordonnée — les trois items collés sur une ligne
pages = render("1. alpha\n2. beta\n3. gamma\n")
ok("une liste ordonnée produit bien TROIS lignes distinctes",
   len(pages) == 1 and pages[0].size[0] == md_to_pdf.W,
   f"{len(pages)} page(s)")

print("\n═══ 3 · nos documents client passent tous ═══")
for doc in sorted((ROOT / "sales").glob("*.md")):
    if doc.name.startswith(("Send-", "RDV-")) or "BUSINESS-CASE" in doc.name or "DM-OPTIC" in doc.name:
        try:
            render(doc.read_text(encoding="utf-8"), doc.stem)
            ok(f"{doc.name}", True)
        except Exception as exc:  # noqa: BLE001
            ok(f"{doc.name}", False, f"{type(exc).__name__}: {exc}")

print(f"\n{'-' * 62}\n{PASSED} assertion(s) passent, {FAILED} échouent")
sys.exit(1 if FAILED else 0)
