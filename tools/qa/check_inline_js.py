#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CHECK INLINE JS — `python3 tools/qa/check_inline_js.py fichier.html [autre.html ...]`

Pourquoi cet outil existe (22/09, matin) : King a ouvert la maquette d'UNIVERS OPTIQUE et l'a trouvée
« moche et sans image ». En réalité la page se peignait EN-TIÈRE-MENT vide sous l'en-tête, parce que
tout son contenu portait un `opacity:0` relevé par un `IntersectionObserver` — et donc que **le moindre
plantage du JavaScript embarque laisse la page blanche**. En cherchant ce quicould planté, j'ai trouvé
un vrai plantage, déjà parti chez Le Cristallin : le gabarit écrivait

    st.textContent = (l==='fr'? ST_IDLE_FR : ST_IDLE_EN)

et le générateur injectait la phrase **entre guillemets retirés** (`json.dumps(...)[1:-1]`), d'où un
identifiant nu dans le code émis — `ReferenceError` dès la première ligne exécutée, l'IIFE entière
mourait, le sélecteur d'assurance et la bascule FR|EN avec elle. Un auditeur de contrastes ne peut pas
le voir : il ne lit pas le JS. Un compilateur, si.

Ce qu'il fait : il sort chaque bloc `<script>` NON-JSON de la page, l'écrit tel quel dans un fichier
temporaire, et le passe à `node --check`. Il ne corrige rien, il refuse.

Codes de sortie : 0 tout compile · 1 erreur de syntaxe (liste fichier:ligne + message) · 2 fichier
introuvable ou illisible · 3 `node` indisponible dans le bac (le contrôle n'a PAS été rendu — à écrire
dans les notes de livraison, pas à taire).
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)


def attrs_is_json(attr_text: str) -> bool:
    return "application/ld+json" in attr_text or "importmap" in attr_text


def check_file(path: Path, workdir: Path):
    """Retourne une liste de fautes (peut être vide)."""
    html = path.read_text(encoding="utf-8")
    faults = []
    for n, (attr, body) in enumerate(SCRIPT.findall(html), 1):
        if not body.strip():
            continue
        if attrs_is_json(attr):
            faults += jsonld_faults(path, n, body)
            continue
        f = workdir / ("inline_%02d.js" % n)
        f.write_text(body, encoding="utf-8")
        r = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)
        if r.returncode != 0:
            line_no = line_of_script(html, body)
            faults.append("%s · <script> n°%d (ligne %d du fichier) :\n%s"
                          % (path.name, n, line_no, indent(r.stderr.strip()[:900])))
    return faults


def jsonld_faults(path, n, body):
    import json
    out = []
    try:
        json.loads(body)
    except ValueError as e:
        out.append("%s · JSON-LD n°%d illisible : %s" % (path.name, n, e))
    return out


def line_of_script(html, body):
    i = html.find(body.strip()[:80])
    return html.count("\n", 0, i) + 1 if i > 0 else 0


def indent(t):
    return "\n".join("      " + l for l in t.splitlines())


def main(argv):
    files = [Path(a) for a in argv[1:] if not a.startswith("-")]
    if not files:
        print(__doc__)
        return 2
    missing = [str(f) for f in files if not f.exists()]
    if missing:
        print("✗ fichier introuvable : %s" % ", ".join(missing))
        return 2
    if shutil.which("node") is None:
        print("! `node` est absent de ce bac : le JavaScript embarqué N'A PAS été compilé. À écrire "
              "dans les notes de livraison — ne pas déclarer ce contrôle « passé ».")
        return 3
    all_faults = []
    with tempfile.TemporaryDirectory(prefix="amk-js-") as td:
        workdir = Path(td)
        for f in files:
            all_faults += check_file(f, workdir)
    if all_faults:
        print("✗ JAVASCRIPT EMBARQUÉ NON COMPILABLE — la page se présente vidée de son contenu là où le")
        print("  script est requis (reveals, bascule de langue, liens WhatsApp peints au vol) :")
        for x in all_faults:
            print("  · %s" % x)
        print("  Règle : un script qui plante annule TOUT ce qui suit dans le même bloc. Sur nos maquettes,")
        print("  « ça plante » se voit donc comme « la page est vide » — cf. design/WORKFLOW.md §9 (10).")
        return 1
    tot = sum(len(SCRIPT.findall(f.read_text(encoding="utf-8"))) for f in files)
    print("ok   %d fichier(s), %d bloc(s) <script> passés au compilateur (JSON-LL validé à part) — 0 faute"
          % (len(files), tot))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
