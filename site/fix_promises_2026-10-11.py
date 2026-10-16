#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ruling King 11/10/2026 — trois promesses du site AMK corrigées, PARTOUT où elles portent.

  1. Délai de mise en ligne (3–5 j / 3 à 5 j / 5–7 j)  → complété par « après l'acompte »
  2. Aperçu 24h                                        → « après validation du brief » sur les
                                                         promesses ; le délai DISPARAÎT des libellés
                                                         courts (boutons, barre collante, messages
                                                         WhatsApp pré-remplis)
  3. « 1 mois de support gratuit »                     → SUPPRIMÉ, sans remplacement (aucune ligne
                                                         de la grille tarifaire ne le porte)

Deux gardes-fous :
  · « 24h/24 » (horaires d'ouverture des cliniques) n'est JAMAIS touché.
  · Les .backup ne sont pas des sources : signalés, pas réécrits.

Usage :  python3 site/fix_promises_2026-10-11.py [--check]
         --check = compter sans écrire. La porte de vérification tourne sur le contenu APRÈS
         transformation dans les deux cas.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent

TARGETS = [
    "index.html",
    "creation-site-web-ecole-cameroun.html",
    "creation-site-web-clinique-cameroun.html",
    "clinic-bonaberi.html",
    "sample-school.html",
    "sample-nursery.html",
    "sample-secondary.html",
    "sample-polyclinic.html",
    "sample-maternity.html",
    "mitoc.html",
]

# ── 1. DÉLAI : complément « après l'acompte » / « after the deposit » ───────────────────
DELAY = [
    (r"3[–\-]5 jours(?!\s*après l'acompte)", "3–5 jours après l'acompte"),
    (r"3 à 5 jours(?!\s*après l'acompte)", "3 à 5 jours après l'acompte"),
    (r"3[–\-]5 days(?!\s*after the deposit)", "3–5 days after the deposit"),
    (r"3 to 5 days(?!\s*after the deposit)", "3 to 5 days after the deposit"),
    (r"5[–\-]7 jours(?!\s*après l'acompte)", "5–7 jours après l'acompte"),
    (r"5[–\-]7 days(?!\s*after the deposit)", "5–7 days after the deposit"),
]

# ── 2a. APERÇU : le délai disparaît des libellés courts ─────────────────────────────────
LABELS = [
    (r"(Recevoir mon aperçu gratuit)\s*24\s?h", r"\1"),
    (r"([Aa]perçu gratuit)(?:\s*(?:sous|en|de|dans))?\s*24\s?(?:h\b|heures)", r"\1"),
    (r"(aperçu gratuit)\s*24h", r"\1"),
    (r"(votre apercu gratuit)\s*sous 24 heures", r"\1"),
    (r"(mon aperçu GRATUIT de site web)\s*sous 24h", r"\1"),
    (r"(mon APERÇU GRATUIT de site web)\s*sous 24h", r"\1"),
    (r"(my FREE)\s*24h\s*(website preview)", r"\1 \2"),
    (r"(your FREE website preview)\s*within 24h", r"\1"),
    (r"(Get my free)\s*24h\s*(preview)", r"\1 \2"),
    (r"([Ff]ree)\s*24h\s*(preview)", r"\1 \2"),
    (r"(aperçu gratuit de)\s*24h", r"\1"),
]

# ── 2b. APERÇU : les promesses restantes reçoivent le complément ────────────────────────
# Garde-fou : « 24h/24 » (horaires) est exclu par le lookahead négatif.
QUALIFY = [
    (r"24 heures(?!\s*(?:après|after))(?!\s*/\s*24)", "24 heures après validation du brief"),
    (r"24\s?h(?!/24)(?!\s*(?:après|after))(?![\w/])", "24h après validation du brief"),
    (r"within 24 hours(?!\s*(?:after|of brief))(?!\s*/\s*24)", "within 24 hours of brief sign-off"),
    (r"in 24 hours(?!\s*(?:after|of brief))(?!\s*/\s*24)", "in 24 hours after brief sign-off"),
]

# ── 3. SUPPORT GRATUIT : phrases effacées, sans remplacement ───────────────────────────
SUPPORT = [
    r"Un mois de support gratuit,?\s*",
    r"un mois de support gratuit,?\s*",
    r"\+?\s*1 mois de support gratuit",
    r"\bet un mois de support gratuit",
    r"One month of free support,?\s*",
    r"A month of free support,?\s*",
    r"hosting managed, and then,?\s*",
    r"\+?\s*1 month free support",
    r"\band one month of free support",
    r"99\.9% uptime hosting,?\s*",
    r"99\.9% uptime,?\s*",
    r"et votre lancement devient notre prochaine étude de cas\.?",
    r"and your launch becomes our next case study\.?",
]


# Pré-passe : la promesse est effacée ET la phrase reste grammaticale (le connecteur est réparé,
# aucune offre n'est substituée — « do not replace » porte sur l'offre, pas sur la grammaire).
SENTENCE_REPAIR = [
    (r"Apres le lancement, vous avez un mois de support gratuit\.\s*Ensuite,\s*", "Apres le lancement, "),
    (r"Un mois de support gratuit, l'hébergement suivi, et ensuite,\s*", "L'hébergement est suivi, et ensuite, "),
    (r"Un mois de support gratuit,\s*", ""),
    (r"After launch you get one month of free support\.\s*After that,\s*", "After launch, "),
    (r"[Oo]ne month of free support,\s*", ""),
    (r"One month of free support, hosting managed, and then,\s*", "Hosting is managed, and then, "),
]

# ── Porte de vérification ───────────────────────────────────────────────────────────────
RESIDUE = {
    "3–5 jours sans « après l'acompte »": r"3[–\-]5 jours(?!\s*après l'acompte)",
    "3 à 5 jours sans « après l'acompte »": r"3 à 5 jours(?!\s*après l'acompte)",
    "5–7 jours sans « après l'acompte »": r"5[–\-]7 jours(?!\s*après l'acompte)",
    "3–5 days sans « after the deposit »": r"3[–\-]5 days(?!\s*after the deposit)",
    "5–7 days sans « after the deposit »": r"5[–\-]7 days(?!\s*after the deposit)",
    "24h/24 heures lié à l'aperçu, non conditionné":
        r"(?:aperçu|preview|apercu)[^<]{0,30}?24\s?(?:h\b|heures)(?!\s*(?:après|after|of brief))",
    "« support gratuit » (doit être 0)": r"[Ss]upport gratuit",
    "« free support » (doit être 0)": r"free support",
    "« 99.9% uptime » (doit être 0)": r"99\.9% uptime",
}


def transform(text):
    n = 0
    for pat, rep in SENTENCE_REPAIR + DELAY + LABELS + QUALIFY:
        text, k = re.subn(pat, rep, text)
        n += k
    for pat in SUPPORT:
        text, k = re.subn(pat, "", text)
        n += k
    return text, n


def main():
    check = "--check" in sys.argv
    total = 0
    results = {}
    for name in TARGETS:
        path = ROOT / name
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated, n = transform(original)
        results[name] = updated
        if n:
            total += n
            print(f"{name:45s} {n:3d} remplacement(s)")
            if not check:
                path.write_text(updated, encoding="utf-8")
    print(f"\n{'[CHECK — rien écrit] ' if check else ''}TOTAL : {total} remplacement(s)")

    print("\n=== PORTE DE VÉRIFICATION (contenu APRÈS transformation) ===")
    clean = True
    for name, body in results.items():
        for label, pat in RESIDUE.items():
            hits = re.findall(pat, body)
            if hits:
                clean = False
                print(f"   ⚠️  {name}: {len(hits)} × {label}")
                for h in re.finditer(pat, body):
                    ctx = body[max(0, h.start() - 70):h.end() + 30].replace("\n", " ")
                    print(f"        …{ctx}…")
                    break
    print("   ✅ zéro reste" if clean else "   ❌ des restes — voir ci-dessus")

    print("\n=== Sauvegardes présentes dans le dossier déployé (non réécrites) ===")
    stale = re.compile(r"15 000 FCFA|99\.9% uptime|support gratuit")
    for p in sorted(ROOT.glob("*.backup*")):
        hits = len(stale.findall(p.read_text(encoding="utf-8")))
        print(f"   {p.name} — {hits} mention(s) périmée(s) encore présente(s)")


if __name__ == "__main__":
    main()
