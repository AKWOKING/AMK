#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — schéma enrichi, GÉNÉRÉ depuis la page (21/09/2026).

**Pourquoi généré.** Le `FAQPage` du schéma était écrit à la main à côté de la FAQ visible.
Le 19/09, la FAQ a changé (prix du mensuel) et seul le HTML a été corrigé — le schéma est resté
en arrière jusqu'à ce qu'on le voie. **Deux copies d'une même vérité divergent toujours.**
Ici, le schéma est **extrait de la FAQ réellement affichée**, donc il ne peut plus mentir.

Ajoute aussi ce que les agences camerounaises concurrentes déclarent et pas nous
(FeliSitePro, VENEGRE) : `priceRange`, les `Service` avec leurs `Offer`, `knowsLanguage`,
et la liste complète des villes desservies.

Usage :  python3 tools/site/seo_schema_2026-09-21.py
"""
import json
import pathlib
import re
import sys

P = pathlib.Path("site/index.html")

SERVICES = [
    ("Création de site web", "Website design", "Site vitrine bilingue FR|EN pour écoles privées, cliniques et laboratoires au Cameroun."),
    ("Site web bilingue FR|EN", "Bilingual EN|FR website", "Chaque page existe en français et en anglais — pas un widget de traduction."),
    ("Prise de rendez-vous WhatsApp", "WhatsApp booking", "Chaque bouton ouvre WhatsApp avec le message déjà rédigé : inscriptions, rendez-vous, questions."),
    ("Référencement local", "Local SEO", "Structure, mots-clés et données structurées pour être trouvé sur « école à Douala », « laboratoire à Buea »."),
    ("Nom de domaine et hébergement", "Domain and hosting", "Domaine au nom du client, hébergement sécurisé, fichiers au client."),
]

CITIES = ["Douala", "Yaoundé", "Buea", "Limbe", "Bafoussam", "Bamenda"]


def extract_faq(t: str):
    """Lit la FAQ RÉELLEMENT affichée et en fait le schéma. Source unique de vérité.

    ⚠️ Les `data-en` / `data-fr` sont sur les <summary> et les <p> : on prend le FRANÇAIS
    pour la réponse (le marché cherche en français) et on garde l'anglais quand il n'y a
    pas de paire."""
    out = []
    for block in re.findall(r"<details[^>]*>(.*?)</details>", t, re.S):
        qs = re.findall(r"<summary[^>]*data-fr=\"([^\"]+)\"", block)
        if not qs:
            qs = re.findall(r"<summary[^>]*>(.*?)</summary>", block, re.S)
        # ⚠️ La FAQ du site met la réponse dans <div class="ans"> ; mes 3 ajouts utilisaient <p>.
        # Un extracteur qui ne connaît qu'UN motif ne lit que la moitié de la page
        # (3 questions sur 10 la première fois). On accepte les deux, et on préfère data-fr.
        ps = re.findall(r'<(?:p|div)[^>]*data-fr="([^"]+)"', block)
        if not ps:
            ps = re.findall(r"<(?:p|div)[^>]*>(.*?)</(?:p|div)>", block, re.S)
        if not qs or not ps:
            continue
        q = re.sub(r"<[^>]+>", "", qs[0]).replace("&nbsp;", " ").strip()
        a = re.sub(r"<[^>]+>", "", ps[0]).replace("&nbsp;", " ").strip()
        if q and a:
            out.append({"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}})
    return out


def main() -> int:
    t = P.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not m:
        sys.exit("✗ bloc JSON-LD introuvable")
    data = json.loads(m.group(1))

    faq = extract_faq(t)
    print(f"  FAQ lue dans la page : {len(faq)} question(s)")

    graph = [n for n in data.get("@graph", []) if n.get("@type") != "FAQPage"]

    for n in graph:
        if n.get("@type") == "LocalBusiness":
            n["name"] = "AMK – Web Development & Digital Solutions"   # NAP EXACT (facteur #15)
            n["priceRange"] = "100000 FCFA"
            n["currenciesAccepted"] = "XAF"
            n["paymentAccepted"] = "MTN Mobile Money, Orange Money, espèces"
            n["knowsLanguage"] = ["fr", "en"]
            n["areaServed"] = [{"@type": "City", "name": c} for c in CITIES]
            n["description"] = ("Création de sites web bilingues FR|EN pour écoles privées, cliniques "
                                "et laboratoires au Cameroun. Aperçu gratuit sous 24 h, en ligne en 3 à 5 jours.")
            n["hasOfferCatalog"] = {
                "@type": "OfferCatalog",
                "name": "Création de site web au Cameroun",
                "itemListElement": [
                    {"@type": "Offer",
                     "name": fr_name,
                     "description": desc,
                     "price": "100000",
                     "priceCurrency": "XAF",
                     "availability": "https://schema.org/InStock",
                     "areaServed": "Cameroun",
                     "itemOffered": {"@type": "Service", "name": fr_name, "alternateName": en_name}}
                    for fr_name, en_name, desc in SERVICES
                ],
            }

    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": faq})

    new = json.dumps({"@context": "https://schema.org", "@graph": graph},
                     ensure_ascii=False, indent=1)
    t = t[:m.start(1)] + "\n" + new + "\n" + t[m.end(1):]
    P.write_text(t, encoding="utf-8")

    # contrôle : le schéma se relit-il ?
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    d = json.loads(blocks[0])
    types = [n.get("@type") for n in d.get("@graph", [])]
    has_faq = any(n.get("@type") == "FAQPage" for n in d.get("@graph", []))
    print(f"✓ schéma régénéré · @graph = {types}")
    print(f"  FAQPage : {len(faq)} questions · OfferCatalog : {len(SERVICES)} services")
    print("  JSON valide : oui")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
