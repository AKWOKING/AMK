# -*- coding: utf-8 -*-
"""test_audit_aeo.py — la preuve que le portique AEO mord, et qu'il ne mord pas à côté.

    python3 tools/qa/test_audit_aeo.py

Trois pages fautives construites exprès, une page saine, et nos vraies pages :

1. **`noindex` sur une page publique** — la page est parfaite et invisible. C'est le pendant exact du
   piège que la vidéo d'Ahrefs chiffre : 5,9 % des sites bloquent les robots IA sans le savoir.
2. **Un `robots.txt` qui bloque GPTBot** — le cas « hérité d'un ancien modèle », celui qu'on ne voit
   jamais dans ses statistiques puisqu'il n'y a rien à mesurer.
3. **Une page publique sans données structurées** — avertissement, pas faute : une page peut vivre sans
   JSON-LD, elle est simplement moins lisible par une IA.

Et la page saine prouve l'inverse : une page indexable, structurée et pleine de questions ne reçoit
**aucun** constat. C'est ce témoin-là qui empêche l'outil de crier sur tout.
"""
import io
import os
import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import importlib.util

spec = importlib.util.spec_from_file_location("audit_aeo", HERE / "audit_aeo.py")
aeo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aeo)

SAINE = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="robots" content="index,follow">
<title>Laboratoire d'analyses à Bonamoussadi, Douala</title>
<script type="application/ld+json">{"@type":"MedicalLaboratory","name":"UNI-LABO",
"address":{"@type":"PostalAddress","addressLocality":"Douala"}}</script>
<script type="application/ld+json">{"@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"Êtes-vous ouverts le samedi ?","acceptedAnswer":{"@type":"Answer","text":"Oui, de 7h à 13h."}}]}</script>
</head><body><h1>UNI-LABO, Bonamoussadi</h1>
<details><summary>Êtes-vous ouverts le samedi ?</summary><p>Oui, de 7h à 13h.</p></details>
</body></html>"""

INVISIBLE = SAINE.replace('<meta name="robots" content="index,follow">',
                          '<meta name="robots" content="noindex,nofollow">')
# Le premier témoin « sans données structurées » n'en retirait qu'UN bloc : la page gardait son FAQPage,
# l'outil avait raison de ne rien signaler. Un témoin faux ne prouve rien — il faut retirer TOUT le JSON-LD.
import re as _re
NU = _re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", SAINE, flags=_re.S)

tmp = pathlib.Path(tempfile.mkdtemp())
(tmp / "saine.html").write_text(SAINE, encoding="utf-8")
(tmp / "invisible.html").write_text(INVISIBLE, encoding="utf-8")
(tmp / "sans-donnees.html").write_text(NU, encoding="utf-8")
# un dossier « site » à part, avec un robots.txt qui bloque GPTBot
bloc = tmp / "bloque"
bloc.mkdir()
(bloc / "robots.txt").write_text("User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n", encoding="utf-8")
(bloc / "page.html").write_text(SAINE, encoding="utf-8")

fails = []


def check(label, cond, detail=""):
    print("  %s %s%s" % ("ok  " if cond else "FAIL", label,
                         ("  — " + str(detail)) if detail and not cond else ""))
    if not cond:
        fails.append(label)


def run(p):
    return aeo.audit(p)


print("═══ la page saine : aucun constat ═══")
f, g, n, pub = run(tmp / "saine.html")
check("page saine — aucune faute", not [x for x in f if x[0] == "ERR"], f)
check("page saine — aucun avertissement", not [x for x in f if x[0] == "WARN"], f)
check("page saine — l'outil dit aussi ce qui est conforme (robots, JSON-LD, questions)", len(g) >= 2, g)

GABARIT = SAINE.replace("<h1>UNI-LABO, Bonamoussadi</h1>",
                        "<h1>{{NAME}} — Maquette d'accueil</h1><p>{{CITY}} · {{PHONE}}</p>")
(tmp / "gabarit.html").write_text(GABARIT, encoding="utf-8")

print("\n═══ et les quatre fautes qu'il doit refuser ═══")
f2, _, _, _ = run(tmp / "invisible.html")
check("ERR — page publique en noindex (le piège des 5,9 %)", any(x[0] == "ERR" and "noindex" in x[1] for x in f2), f2)

f3, _, _, _ = run(bloc / "page.html")
# Cinquième fois qu'une assertion mord sur une majuscule : le message dit « gptbot », l'assertion
# cherchait « GPTBot ». Une assertion ne doit jamais dépendre de la casse d'un message.
check("ERR — robots.txt qui bloque GPTBot",
      any(x[0] == "ERR" and "gptbot" in x[1].lower() for x in f3), f3)

f4, _, _, _ = run(tmp / "sans-donnees.html")
check("WARN — page publique sans données structurées",
      any(x[0] == "WARN" and "structur" in x[1] for x in f4), f4)

f6, _, _, _ = run(tmp / "gabarit.html")
check("ERR — gabarit à jetons {{...}} laissé indexable (le défaut trouvé chez nous)",
      any(x[0] == "ERR" and "jeton" in x[1] for x in f6), f6)

print("\n═══ et il ne confond pas une page de TRAVAIL avec une page publique ═══")
f5, _, n5, pub5 = run(HERE.parent.parent / "demos/concept-unilabo-v2.html")
check("UNI-LABO (page de travail, noindex voulu) — aucune faute", not [x for x in f5 if x[0] == "ERR"], f5)
check("UNI-LABO — le noindex est annoncé comme VOLONTAIRE, avec le rappel de déploiement",
      any("noindex" in x and "VOULU" in x for x in n5), n5)

print("\n═══ et contre nos pages publiques ═══")
root = HERE.parent.parent
for rel in ("site/index.html", "site/creation-site-web-clinique-cameroun.html",
            "site/creation-site-web-ecole-cameroun.html"):
    p = root / rel
    if p.exists():
        fn, _, _, _ = run(p)
        check("%s — aucune faute" % p.name, not [x for x in fn if x[0] == "ERR"], fn)

print()
if fails:
    print("DES ÉCHECS : " + " · ".join(fails))
    sys.exit(1)
print("Tout est vert — le portique refuse les quatre pièges du lot [31] et ne mord pas sur les pages saines.")
