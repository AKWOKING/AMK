#!/usr/bin/env python3
"""Banc de la fiche prospect — `tools/outreach/fiche.py`.

    python3 tools/outreach/test_fiche.py

Trois familles, dans l'ordre du risque :

1. **le numéro** — le format international se déduit, il ne se tape pas ;
2. **la relecture** — `verifie` doit crier quand la fiche et le CRM divergent, et **aussi** quand elle ne
   trouve rien à lire : une porte qui ne voit rien ne prouve rien ;
3. **le contrôle d'un message réécrit** — la phrase trouvée sur Facebook doit pouvoir être vérifiée sans
   reconstruire un lot, y compris le jour où elle a perdu son dédouanement.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fiche  # noqa: E402

CAS = []
RACINE = fiche.RACINE
LOT1 = RACINE / "sales" / "LOT-1-2026-10-27.md"


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn
    return enveloppe


@cas("le numéro s'écrit au format qu'on tape : +237 6 55 04 95 29")
def _():
    assert fiche.numero_intl("655 04 95 29") == "+237 6 55 04 95 29"
    assert fiche.numero_intl("+237 699 86 04 63") == "+237 6 99 86 04 63"
    assert fiche.numero_intl("0123") == ""
    return "trois formats, deux justes, un refusé"


@cas("le CRM rend l'email caché dans les notes, pas une colonne vide")
def _():
    d = fiche.lit_crm_detail()
    assert d["655049529"]["mail"] == "favourjoyopticmedical@gmail.com", d["655049529"]["mail"]
    assert d["656978043"]["mail"] == "iseecameron@gmail.com"
    assert d["675399023"]["mail"] == ""            # ce cabinet n'a pas publié d'email
    return "deux emails retrouvés dans les notes, un absent assumé"


@cas("les cinq cartes du LOT 1 portent le nom affiché et le verdict ENVOYER")
def _():
    cs = fiche.cartes(RACINE / "sales" / "LOT-1-2026-10-27.md", 5, "2026-10-27")
    assert len(cs) == 5, len(cs)
    assert all(c["verdict"] == "ENVOYER" for c in cs), [c["verdict"] for c in cs]
    assert cs[0]["affiche"] == "Optic Medical Favour and Joy", cs[0]["affiche"]
    assert cs[0]["intl"] == "+237 6 55 04 95 29", cs[0]["intl"]
    return f"5 ENVOYER · {cs[0]['label']} → {cs[0]['affiche']}"


@cas("la fiche livrée est relue contre le CRM, et elle passe")
def _():
    fautes = fiche.verifie(LOT1)
    assert not fautes, fautes
    return "5 numéros, aucun écart"


@cas("un numéro interverti dans la fiche est attrapé")
def _():
    faux = Path(tempfile.mkdtemp()) / "faux.md"
    faux.write_text(LOT1.read_text(encoding="utf-8")
                    .replace("— 656 97 80 43**", "— 656 97 80 44**"), encoding="utf-8")
    fautes = fiche.verifie(faux)
    assert fautes, "un numéro faux est passé"
    assert any("ISEE" in f for f in fautes), fautes
    return f"{len(fautes)} écart(s), ISEE nommé"


@cas("une fiche sans aucune carte n'est pas « valide »")
def _():
    vide = Path(tempfile.mkdtemp()) / "vide.md"
    vide.write_text("# Un document qui parle de prospection\n\nRien à lire ici.\n", encoding="utf-8")
    fautes = fiche.verifie(vide)
    assert fautes and "aucune carte lue" in fautes[0], fautes
    return "porte fermée sur une fiche vide"


@cas("le message réécrit avec un fait trouvé passe la porte")
def _():
    texte = ("Bonjour, je sais que c'est inattendu : à PK11 votre compte WhatsApp s'appelle « Optic "
             "Medical Favour and Joy », et le tableau de l'Ordre vous inscrit « Ets Espace Médical ».\n"
             "Deux noms dans deux registres qui ne sont pas à vous : le patient cherche l'un et trouve "
             "l'autre.\n"
             "J'ai fait le site d'un opticien d'ici, il est en ligne.\n"
             "Dites-moi un mot : lequel en haut du site, avec WhatsApp ?")
    fails, warns, n = fiche.controle(texte)
    assert not fails and not warns, (fails, warns)
    assert 35 <= n <= 70, n
    return f"{n} mots, 0/0"


@cas("le même message sans sa cause nommée est refusé en avertissement")
def _():
    texte = ("Bonjour, je sais que c'est inattendu : à PK11 votre compte WhatsApp s'appelle « Optic "
             "Medical Favour and Joy », et le tableau de l'Ordre vous inscrit « Ets Espace Médical ».\n"
             "Votre nom est inscrit deux fois, et c'est bien normal.\n"
             "J'ai fait le site d'un opticien d'ici, il est en ligne.\n"
             "Dites-moi un mot : lequel en haut du site, avec WhatsApp ?")
    fails, warns, n = fiche.controle(texte)
    assert not fails, fails
    assert any("pas de cause nommée" in w for w in warns), warns
    return "avertissement nommé : le fait se lirait comme un reproche"


@cas("une affirmation d'absence est signalée, même quand le texte passe la porte")
def _():
    texte = ("Bonjour, à Douala, « ISEE » au tableau de l'Ordre et « I See Better » sur WhatsApp, "
             "avec une adresse postale et un email.\n"
             "Ce n'est pas votre travail, c'est le nom : tapez « I See Better Douala », Google ne connaît pas.\n"
             "Dites-moi en un mot : lequel des deux vos patients utilisent ?")
    fails, warns, n = fiche.controle(texte)
    assert not fails, fails
    assert any("affirmation d'absence" in w for w in warns), warns
    return f"{n} mots, porte OK, rappel présent"


@cas("« page » est signalé — le produit s'appelle « le site » à Douala")
def _():
    texte = ("Bonjour, à PK11 votre fiche Google est bien tenue : horaires, photos, trois avis.\n"
             "Ce n'est pas votre travail, c'est le web : cette page vous appartient, et le patient y lit tout.\n"
             "Dites-moi un mot : je vous montre le site, avec un bouton WhatsApp ?")
    fails, warns, n = fiche.controle(texte)
    assert not fails, fails
    assert any("page" in w and "Facebook" in w for w in warns), warns
    return f"{n} mots, rappel « page » présent"


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
    print(f"\n{'✓' if not ko else '✗'} {len(CAS) - ko}/{len(CAS)}")
    return 1 if ko else 0


if __name__ == "__main__":
    raise SystemExit(main())
