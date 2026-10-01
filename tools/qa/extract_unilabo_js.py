# -*- coding: utf-8 -*-
"""extract_unilabo_js.py — sort les deux blocs <script> d'une page UNI-LABO dans deux fichiers.

    python3 tools/qa/extract_unilabo_js.py <page.html> <sortie_main.js> <sortie_form.js>

Pourquoi cet outil existe : la refonte du 24/09 a réécrit la PAGE de zéro, mais elle n'avait pas le
droit de toucher au COMPORTEMENT (la fiche vivante, l'état d'ouverture, la langue). La façon sûre de ne
pas y toucher n'est pas de recopier à la main — c'est d'extraire le bloc et de l'inclure tel quel.
C'est ce que fait cette commande, et c'est elle qui a produit `demos/_unilabo_v2_js_*.js`.
"""
import io, re, sys

def blocks(path):
    s = io.open(path, encoding="utf-8").read()
    return re.findall(r"<script>(.*?)</script>", s, re.S)

def main():
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(2)
    page, out_main, out_form = sys.argv[1:4]
    b = blocks(page)
    main = [x for x in b if "(function(){" in x][0]
    form = [x for x in b if "LA FICHE VIVANTE" in x][0]
    io.open(out_main, "w", encoding="utf-8").write(main.strip() + "\n")
    io.open(out_form, "w", encoding="utf-8").write(form.strip() + "\n")
    print("%s : %d + %d octets -> %s, %s" % (page, len(main), len(form), out_main, out_form))

if __name__ == "__main__":
    main()
