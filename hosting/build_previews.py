# -*- coding: utf-8 -*-
"""
build_previews.py — assemble hosting/previews/ from the canonical demo files.

Run after editing any concept:  python3 hosting/build_previews.py
Then deploy the hosting/previews/ folder (README in that folder has the steps).

Named concepts are private previews (shared one-to-one with the lead), so every
copy gets <meta name="robots" content="noindex,nofollow">. The public nameless
templates (site/sample-*.html) are NOT deployed here; they ship with the agency
site.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "hosting" / "previews"

SLUGS = {
    "oracare": ("demos/concept-oracare-v3.html", "OraCare Dental Clinic, Buea — concept"),
    "skye":    ("demos/concept-skye-v1.html",    "Cabinet Dentaire The Skye, Douala — concept"),
    "yaks":    ("demos/concept-yaks-v1.html",    "Cabinet Dentaire YAKS, Logbessou Douala — concept"),
    "sasse":   ("demos/sjc-sasse-v2.html",       "St. Joseph's College, Sasse — concept"),
    "comobil": ("demos/concept-comobil-v1.html", "COMOBIL Les Lauréats, Douala — concept"),
    "sah":     ("demos/concept-sahiscol-v1.html","Saint Ann's High School, Limbe — concept"),
    "afriquelabo": ("demos/concept-afriquelabo-v1.html", "Afrique Labo SARL, Bessengue Douala — concept"),
    "opticien": ("demos/concept-opticien-lopticien.html", "Votre Opticien — concept pour L'Opticien, Bali Douala"),
    "labethanie": ("demos/concept-labethanie-v1.html", "Clinique La Béthanie, Bonabéri Douala — concept"),
    "jempo": ("demos/concept-jempo-v1.html", "J&E Memorial Polyclinic (JEMPO), Deido Douala — concept"),
    # 21/09 soir — LE CRISTALLIN : le premier prospect qui a dit « Ok » à l'aperçu (21/09 17:53).
    # Attention : c'est une REFONTE d'un site qui existe déjà (lecristallinoptique.com), pas un
    # concept « introuvable ». Privé, noindex, partagé un-à-un uniquement (aucun droit public sur
    # le nom du cabinet avant signature + consentement).
    "cristallin": ("demos/concept-le-cristallin-v1.html",
                   "Le Cristallin, opticien à Douala — refonte concept"),
    # 21/09 nuit — UNIVERS OPTIQUE (Bépanda) : dossier de REPRISE, pas une refonte d'un site vivant.
    # Le domaine du cabinet ne répond plus : la copie partagée porte donc le constat + l'aperçu.
    # 22/09 — la direction « GRANDE PHOTO » (v2) devient l'aperçu de travail ; le dossier v1 reste
    # consultable sous /univers-v1/ pour que la comparaison des deux directions soit possible sur place.
    # 22/09 soir — deux fichiers, deux lecteurs. `/univers/` est LA PAGE telle qu'un client la lira
    # (aucun mot de dossier, créneaux calculés à l'ouverture) ; `/univers-note/` y ajoute la note au
    # cabinet — les six constats, le 3,3 sur six avis, le comparatif, les questions à trancher.
    "univers": ("demos/univers-optique-site-v2.html",
                 "Univers Optique, opticien à Bépanda Douala — le site (v3, créneaux calculés)"),
    "univers-note": ("demos/concept-univers-optique-v2.html",
                      "Univers Optique — le site + la note au cabinet (document de travail)"),
    "univers-v1": ("demos/concept-univers-optique-v1.html",
                   "Univers Optique, opticien à Bépanda Douala — dossier v1"),
    # 23/09 — UNI-LABO : le dossier `unilabo/` est la racine du projet Vercel `uni-labo.vercel.app`
    # (déployé par King le 18/09) et porte aussi `og.jpg`. Il n'était PAS dans cette liste, donc il
    # restait sur la version du 18/09 pendant que le fichier canonique évoluait — exactement le genre
    # d'écart qui fait qu'on vérifie une page et qu'on en déploie une autre. Il y est désormais.
    "unilabo": ("demos/concept-unilabo-v1.html",
                "UNI-LABO, laboratoire d'analyses à Bonamoussadi Douala — concept"),
}

NOINDEX = '<meta name="robots" content="noindex,nofollow">'

ROOT_INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AMK · private previews</title>
<style>body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;background:#0F172A;color:#E2E8F0;display:flex;min-height:100dvh;align-items:center;justify-content:center;margin:0;text-align:center;padding:24px}
.box{max-width:460px}h1{font-size:22px;margin:0 0 10px}p{color:#94A3B8;font-size:14.5px;line-height:1.6}</style>
</head><body><div class="box">
<h1>AMK · Web Development &amp; Digital Solutions</h1>
<p>This address hosts private, one-to-one concept previews for the school or clinic they were shared with.<br>Nothing is published here.</p>
</div></body></html>"""

def add_noindex(html: str) -> str:
    if 'name="robots"' in html:
        return html
    m = re.search(r"(<meta[^>]+charset[^>]*>)", html, re.I)
    if m:
        return html[:m.end()] + "\n" + NOINDEX + html[m.end():]
    return NOINDEX + "\n" + html

def main():
    for slug, (src, _label) in SLUGS.items():
        srcp = ROOT / src
        assert srcp.exists(), f"missing source {src}"
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        html = srcp.read_text(encoding="utf-8")
        (d / "index.html").write_text(add_noindex(html), encoding="utf-8")
        print(f"  /{slug}/  <- {src} ({len(html)//1024} KB)")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    print("  /        private marker (no links)")
    print("done ->", OUT)

if __name__ == "__main__":
    main()
