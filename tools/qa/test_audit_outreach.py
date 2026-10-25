#!/usr/bin/env python3
"""test_audit_outreach — casse la porte une règle à la fois, et vérifie qu'elle le dit.

Convention maison (`tools/qa/test_audit_delivery.py`, `test_audit_a11y.py`) : une porte qu'on n'a
jamais vue refuser n'est pas une porte, c'est un fichier. Chaque cas ci-dessous est un message
volontairement fautif ; le test vérifie que `audit_outreach.check()` nomme **la bonne** règle.

Usage : python3 tools/qa/test_audit_outreach.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_outreach import Message, check  # noqa: E402

BON = (
    "Bonjour Docteur, à Bonanjo ce matin, votre cabinet apparaît sur quatre annuaires, avec quatre "
    "numéros et deux adresses. Ce n'est pas votre travail, c'est cette fiche : un patient appelle un "
    "numéro qui n'est plus le vôtre, et raccroche. Je vous l'envoie ? Deux minutes à lire, vous "
    "décidez après."
)


def msg(body: str, quartier: str = "Bonanjo") -> Message:
    m = Message(label="Test", quartier=quartier, phone="677 00 00 00", body=body, line=1)
    check(m)
    return m


def has(m: Message, needle: str) -> bool:
    return any(needle in x for x in m.fails + m.warns)


CAS: list[tuple[str, str, str, str]] = [
    # (nom, corps, quartier, texte attendu dans le verdict)
    ("message sain", BON, "Bonanjo", ""),
    (
        "trop long",
        BON + " Et je pourrais ajouter que la fiche n'a pas été mise à jour depuis longtemps, ce qui "
        "n'aide personne dans le quartier.",
        "Bonanjo",
        "mots (maximum 55)",
    ),
    (
        "deux questions",
        BON.replace("Je vous l'envoie ?", "Je vous l'envoie ? Ou vous préférez que je passe ?"),
        "Bonanjo",
        "questions (une seule)",
    ),
    (
        "attaque déguisée",
        BON.replace("Ce n'est pas votre travail, c'est cette fiche", "Rien à vous, donc"),
        "Bonanjo",
        "attaque déguisée",
    ),
    (
        "remplissage",
        "J'espère que vous allez bien. " + BON,
        "Bonanjo",
        "mot de remplissage",
    ),
    (
        "prix",
        BON.replace("Deux minutes à lire", "À partir de 150 000 FCFA"),
        "Bonanjo",
        "prix dans un premier message",
    ),
    (
        "lien",
        BON.replace("Deux minutes à lire", "Voyez https://amk.cm"),
        "Bonanjo",
        "lien cliquable",
    ),
    (
        "signature",
        BON.replace("vous décidez après.", "vous décidez après. — King, AMK"),
        "Bonanjo",
        "signature",
    ),
    (
        "pourcentage",
        BON.replace("un patient appelle", "97 % des patients appellent"),
        "Bonanjo",
        "pourcentage",
    ),
    (
        "emoji",
        BON.replace("Deux minutes à lire", "Deux minutes à lire 👍"),
        "Bonanjo",
        "emoji",
    ),
    (
        "puces",
        "• fiche incomplète\n" + BON,
        "Bonanjo",
        "liste à puces",
    ),
    (
        "pas de dédouanement",
        BON.replace("Ce n'est pas votre travail, c'est cette fiche :", "La fiche est incomplète :"),
        "Bonanjo",
        "pas de dédouanement",
    ),
    (
        "pas de sortie sans friction",
        BON.replace("Deux minutes à lire, vous décidez après.", ""),
        "Bonanjo",
        "pas de sortie sans friction",
    ),
    (
        "quartier absent du début",
        BON.replace("à Bonanjo ce matin, ", "ce matin, "),
        "Bonanjo",
        "absent des 12 premiers mots",
    ),
    (
        "faux positif : « ou » ailleurs dans la phrase",
        "Bonjour Docteur, à Bonanjo, votre fiche donne un numéro qui n'existe plus ou qui a changé. "
        "Ce n'est pas votre travail, c'est la fiche : un patient appelle et raccroche. "
        "Je vous l'envoie ? Deux minutes, et vous verrez ce que le patient voit.",
        "Bonanjo",
        "",
    ),
    (
        "question à deux branches",
        BON.replace("Je vous l'envoie ?", "C'est vous qui l'avez retiré, ou personne ne vous a prévenu ?"),
        "Bonanjo",
        "deux branches",
    ),
    (
        "auto-présentation au premier message",
        "Bonjour, c'est King. " + BON,
        "Bonanjo",
        "auto-présentation",
    ),
    (
        "sortie qui ne dit pas ce qu'elle produit",
        BON.replace("Je vous l'envoie ? Deux minutes à lire, vous décidez après.",
                    "Je vous l'envoie ? Un mot suffit."),
        "Bonanjo",
        "sortie seule en fin de message",
    ),
    (
        "faux positif : message tiède, sans bonjour ni présentation",
        "Hier, à Akwa, Google sort un cabinet comptable avant Optix — ce n'est pas votre faute. "
        "Un site à votre nom s'affiche à cette place avec horaires, adresse et WhatsApp ; je complète "
        "votre fiche Google si vous en avez les accès. Dites-moi si vous les avez ? "
        "Un mot suffit : la fiche suit le jour même.",
        "Akwa",
        "",
    ),
    (
        "promesse de mesure impossible",
        "Hier, à Akwa, Google sort un cabinet comptable avant Optix — ce n'est pas votre faute. "
        "Dites-moi combien de patients vous arrivent par Google ? Un chiffre suffit : je le compare à "
        "ce que la fiche laisse filer.",
        "Akwa",
        "promesse de mesure impossible",
    ),
    (
        "question finale décorative",
        "Bonjour Docteur, à Bonanjo ce matin, votre cabinet apparaît sur quatre annuaires. Ce n'est "
        "pas votre travail, c'est la fiche recopiée. Un patient appelle et raccroche. Deux minutes "
        "à lire, ça vous parle ?",
        "Bonanjo",
        "ne demande aucune action",
    ),
]


def main() -> int:
    echecs = 0
    for nom, corps, quartier, attendu in CAS:
        m = msg(corps, quartier)
        if not attendu:
            ok = not m.fails and not m.warns
            detail = f"{len(m.fails)} bloquant(s), {len(m.warns)} avertissement(s)"
        else:
            ok = has(m, attendu)
            detail = f"« {attendu} »" if ok else f"attendu « {attendu} », rien trouvé"
        print(f"{'✓' if ok else '✗'} {nom:32} {detail}")
        echecs += 0 if ok else 1

    print(f"\n{len(CAS) - echecs}/{len(CAS)} cas passent")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
