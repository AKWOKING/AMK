#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Témoin de `audit_funnel.py` — une page saine, puis une casse par contrôle.

    python3 tools/qa/test_audit_funnel.py

Chaque cas modifie **une seule chose** dans une page par ailleurs correcte : si le portique cesse de
mordre sur ce cas, c'est lui qui est cassé, pas la page. Même méthode que `test_audit_delivery.py`.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_funnel import check  # noqa: E402

GOOD = """<!doctype html><html lang="fr"><head><style>.hdr{position:sticky;top:0}</style></head>
<body>
<header class="hdr"><a class="btn" href="#contact">Recevoir mon aperçu gratuit</a></header>
<main>
<section class="hero" id="top">
  <h1>Vos parents vous trouvent avant d'appeler</h1>
  <p>Sites bilingues pour écoles et cliniques au Cameroun.</p>
  <a class="btn" href="https://wa.me/237600000000">Écrire sur WhatsApp</a>
</section>
<section id="problem"><h2>Trois façons de perdre des clients</h2><p>Votre page Facebook ne suffit plus.</p></section>
<section id="services"><h2>Ce que nous construisons</h2><p>Un site qui répond à leur question.</p></section>
<section id="work"><h2>Cas client</h2><p>Étude de cas : DM OPTIQUE SARL, site livré, FR + EN.</p></section>
<section id="process"><h2>Comment ça marche</h2><ol><li>Étape 1</li><li>Étape 2</li><li>Étape 3</li></ol></section>
<section id="pricing"><h2>Prix</h2><p>À partir de 150 000 FCFA.</p></section>
<section id="faq"><h2>Questions</h2>
  <details><summary>Combien ?</summary>150 000 FCFA.</details>
  <details><summary>En combien de temps ?</summary>Sept jours.</details>
  <details><summary>Qu'est-ce que je fournis ?</summary>Vos photos et vos textes.</details>
</section>
</main></body></html>
"""


def run(html: str) -> list[tuple[str, str]]:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "index.html"
        p.write_text(html, encoding="utf-8")
        return [(f.code, f.sev) for f in check(p)]


CASES: list[tuple[str, str, str, str]] = [
    ("page saine", GOOD, "", "aucune plainte"),
    ("sans CTA dans le premier écran", GOOD,
     '<a class="btn" href="https://wa.me/237600000000">Écrire sur WhatsApp</a>', "F1 P1"),
    ("sans titre", GOOD, "<h1>Vos parents vous trouvent avant d'appeler</h1>", "F2 P1"),
    ("titre en mots creux", GOOD, "Vos parents vous trouvent avant d'appeler",
     "F2 P2"),
    ("aucune preuve", GOOD,
     '<section id="work"><h2>Cas client</h2><p>Étude de cas : DM OPTIQUE SARL, site livré, FR + EN.</p></section>',
     "F3 P2"),
    ("problème sans solution", GOOD,
     '<section id="services"><h2>Ce que nous construisons</h2><p>Un site qui répond à leur question.</p></section>',
     "F4 P2"),
    ("aucun prix ni devis", GOOD, '<section id="pricing"><h2>Prix</h2><p>À partir de 150 000 FCFA.</p></section>',
     "F6 P2"),
    ("sur devis seulement", GOOD, "À partir de 150 000 FCFA.", "F6 P3"),
    ("sans FAQ", GOOD,
     """<section id="faq"><h2>Questions</h2>
  <details><summary>Combien ?</summary>150 000 FCFA.</details>
  <details><summary>En combien de temps ?</summary>Sept jours.</details>
  <details><summary>Qu'est-ce que je fournis ?</summary>Vos photos et vos textes.</details>
</section>""", "F7 P2"),
    ("sans barre collante", GOOD, ".hdr{position:sticky;top:0}", "F8 P2"),
    ("texte de remplacement", GOOD, "Un site qui répond à leur question.", "F10 P1"),
    ("quatre CTA", GOOD, '<a class="btn" href="https://wa.me/237600000000">Écrire sur WhatsApp</a>',
     "F11 P3"),
]


def main() -> int:
    fails = 0
    for name, base, cut, expect in CASES:
        html = base.replace(cut, "") if cut else base
        if name == "titre en mots creux":
            html = GOOD.replace("Vos parents vous trouvent avant d'appeler", "Une solution digitale moderne")
        if name == "sur devis seulement":
            html = GOOD.replace("150 000 FCFA.", "sur devis, selon votre besoin.")
        if name == "quatre CTA":
            html = GOOD.replace(
                '<a class="btn" href="https://wa.me/237600000000">Écrire sur WhatsApp</a>',
                "".join(f'<a class="cta" href="#c{i}">Action {i}</a>' for i in range(4)))
        if name == "texte de remplacement":
            html = GOOD.replace("Un site qui répond à leur question.", "Lorem ipsum dolor sit amet.")
        if name == "aucun prix ni devis":
            html = GOOD.replace("150 000 FCFA.", "un montant adapté.") \
                       .replace('<section id="pricing"><h2>Prix</h2><p>À partir de un montant adapté.</p></section>', "")
        if name == "sur devis seulement":
            assert "150 000" not in html, "le montant doit avoir disparu pour tester « sur devis »"

        got = run(html)
        if name == "page saine":
            ok = not got
            detail = "aucun constat" if ok else f"constats inattendus : {got}"
        else:
            ok = tuple(expect.split()) in got
            detail = "" if ok else f"attendu {expect}, obtenu {got}"
        print(f"  {'✓' if ok else '✗'} {name}" + (f" → {detail}" if detail else ""))
        fails += 0 if ok else 1

    print(f"\n{len(CASES) - fails} assertion(s) verte(s), {fails} échec(s) — la porte tunnel mord sur "
          f"les onze blocs du tableau.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
