#!/usr/bin/env python3
"""test_audit_outreach — casse la porte une règle à la fois, et vérifie qu'elle le dit.

Convention maison (`tools/qa/test_audit_delivery.py`, `test_audit_a11y.py`) : une porte qu'on n'a
jamais vue refuser n'est pas une porte, c'est un fichier. Chaque cas ci-dessous est un message
volontairement fautif ; le test vérifie que `audit_outreach.check()` nomme **la bonne** règle.

Depuis le 26/10 (ruling King), trois règles de plus : le **désarmement** en ouverture, la **preuve
sociale**, et une **cause nommée** qui remplace l'absolution seule (« ce n'est pas votre faute »).
Le plafond passe aussi de 55 à 70 mots — le désarmement et la preuve coûtent quatorze mots à eux deux.

Usage : python3 tools/qa/test_audit_outreach.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_outreach import Message, check  # noqa: E402

BON = (
    "Bonjour, je sais que c'est inattendu : à Bonanjo votre fiche Google est tenue, horaires et avis, "
    "et rien n'est à vous. Le patient tape votre nom, tombe sur quatre annuaires qui recopient votre "
    "description, et rien à ouvrir qui vienne de vous. J'ai fait le site d'un opticien d'ici, il est "
    "en ligne. Dites-moi un mot : je vous montre le site, avec vos horaires ?"
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
        "n'aide personne dans le quartier, ni le samedi matin quand le patient hésite encore.",
        "Bonanjo",
        "mots (maximum 70)",
    ),
    (
        "deux questions",
        BON.replace("Dites-moi un mot : je vous montre le site, avec vos horaires ?",
                    "Je vous montre le site ? Ou vous préférez que je passe ?"),
        "Bonanjo",
        "questions (une seule)",
    ),
    (
        "attaque déguisée",
        BON.replace("et rien n'est à vous", "Rien à vous, donc"),
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
        BON.replace("avec vos horaires ?", "à partir de 150 000 FCFA ?"),
        "Bonanjo",
        "prix dans un premier message",
    ),
    (
        "lien",
        BON.replace("il est en ligne", "voyez https://amk.cm"),
        "Bonanjo",
        "lien cliquable",
    ),
    (
        "signature",
        BON.replace("avec vos horaires ?", "avec vos horaires ? — King, AMK"),
        "Bonanjo",
        "signature",
    ),
    (
        "pourcentage",
        BON.replace("Le patient tape", "97 % des patients tapent"),
        "Bonanjo",
        "pourcentage",
    ),
    (
        "emoji",
        BON.replace("avec vos horaires ?", "avec vos horaires 👍 ?"),
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
        "pas de cause nommée",
        BON.replace("tombe sur quatre annuaires qui recopient votre description",
                    "tombe sur des résumés qui recopient votre description")
        .replace("et rien n'est à vous", "et c'est bien tenu"),
        "Bonanjo",
        "pas de cause nommée",
    ),
    (
        "absolution qui n'explique rien",
        BON.replace("et rien n'est à vous", "et ce n'est pas votre faute"),
        "Bonanjo",
        "absolution qui n'explique rien",
    ),
    (
        "pas de désarmement",
        BON.replace("Bonjour, je sais que c'est inattendu : ", "Bonjour, "),
        "Bonanjo",
        "pas de désarmement",
    ),
    (
        "aucune preuve sociale",
        BON.replace("J'ai fait le site d'un opticien d'ici, il est en ligne. ", ""),
        "Bonanjo",
        "aucune preuve sociale",
    ),
    (
        "une phrase qui ne vend rien",
        BON.replace("J'ai fait le site", "Nous travaillons avec soin. J'ai fait le site"),
        "Bonanjo",
        "ne nomme ni l'endroit",
    ),
    (
        "pas de sortie sans friction",
        BON.replace("Dites-moi un mot : je vous montre le site, avec vos horaires ?",
                    "Qu'en pensez-vous ?"),
        "Bonanjo",
        "pas de sortie sans friction",
    ),
    (
        "quartier absent du début",
        BON.replace("à Bonanjo votre fiche", "votre fiche"),
        "Bonanjo",
        "absent des 12 premiers mots",
    ),
    (
        "faux positif : « ou » ailleurs dans la phrase",
        "Bonjour, je sais que c'est inattendu : à Bonanjo, votre fiche donne un numéro qui n'existe "
        "plus ou qui a changé. Ce n'est pas votre travail, c'est la fiche : un patient appelle et "
        "raccroche. J'ai fait le site d'un opticien d'ici, il est en ligne ; dites-moi un mot, je "
        "vous montres les horaires ?",
        "Bonanjo",
        "absolution qui n'explique rien",
    ),
    (
        "question à deux branches",
        BON.replace("Dites-moi un mot : je vous montre le site, avec vos horaires ?",
                    "C'est vous qui l'avez retiré, ou personne ne vous a prévenu ?"),
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
        BON.replace("Dites-moi un mot : je vous montre le site, avec vos horaires ?",
                    "Je vous montre le site ? Un mot suffit."),
        "Bonanjo",
        "sortie seule en fin de message",
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
        "Bonjour, je sais que c'est inattendu : à Bonanjo votre fiche Google apparaît sur quatre "
        "annuaires. Ce n'est pas votre travail, c'est la fiche recopiée. J'ai fait le site d'un "
        "opticien d'ici, il est en ligne. Deux minutes à lire, ça vous parle ?",
        "Bonanjo",
        "ne demande aucune action",
    ),
    (
        "faux positif : message tiède, sans bonjour (le désarmement n'a pas à y être)",
        "Hier, à Akwa, Google sort un cabinet comptable avant Optix — la place est chez lui, pas "
        "chez vous. Un site à votre nom prend cette place, avec horaires et WhatsApp ; je complète "
        "aussi votre fiche Google si vous en avez les accès. Dites-moi un mot : vous les avez, "
        "pour la fiche ?",
        "Akwa",
        "",
    ),
]


def main() -> int:
    echecs = 0
    for nom, corps, quartier, attendu in CAS:
        m = msg(corps, quartier)
        if not attendu:
            ok = not m.fails and not m.warns
            detail = f"{len(m.fails)} bloquant(s), {len(m.warns)} avertissement(s)"
            if not ok:
                detail += " — " + "; ".join((m.fails + m.warns)[:2])
        else:
            ok = has(m, attendu)
            detail = f"« {attendu} »" if ok else f"attendu « {attendu} », rien trouvé"
        print(f"{'✓' if ok else '✗'} {nom:44} {detail}")
        echecs += 0 if ok else 1

    print(f"\n{len(CAS) - echecs}/{len(CAS)} cas passent")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
