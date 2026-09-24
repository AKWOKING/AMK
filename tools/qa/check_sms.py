#!/usr/bin/env python3
"""Compte les SEGMENTS RÉELS d'un SMS — et refuse les caractères qui font tout basculer.

Pourquoi cet outil existe (24/09/2026) : un message de premier contact pour K Vision Care a été
écrit avec des tirets cadratins « — » et annoncé « 291 caractères → 2 segments ». **Faux.** Le tiret
cadratin n'appartient pas à l'alphabet GSM-7 (03.38) : sa présence fait encoder TOUT le message en
UCS-2, où un segment ne fait plus 160 caractères mais **70**. Le même texte passait de 2 à 5 segments
sans qu'aucun compteur de caractères ne le dise — le genre d'instrument qui ment en silence, comme le
`Counter` des clés dupliquées ou le `grep` du rebuild.

USAGE
    python3 tools/qa/check_sms.py "texte du message"
    python3 tools/qa/check_sms.py --file message.txt
    echo "texte" | python3 tools/qa/check_sms.py

SORTIE  0 = GSM-7 (message propre) · 1 = contient un caractère hors GSM-7 (le coût est multiplié).
"""
import sys
import unicodedata

# Table GSM 03.38 — les 128 caractères de base (1 unité) …
GSM7 = (
    "@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
    "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà"
)
# … et la table étendue : codés sur DEUX unités, mais toujours GSM-7.
GSM7_EXT = "^{}\\[~]|€\f"

# Les fautes qui coûtent le plus cher en français, avec leur remplacement ASCII/GSM-7.
PIEGES = {
    "—": " - ", "–": "-", "’": "'", "‘": "'", "“": '"', "”": '"',
    "«": '"', "»": '"', "…": "...", "€": "€", " ": " ", "’": "'",
    "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u", "ë": "e", "ï": "i",
    "œ": "oe", "Œ": "OE", "ÿ": "y", "\u202f": " ", "\u200b": "",
}


def analyse(texte: str) -> dict:
    hors = [(i, c) for i, c in enumerate(texte) if c not in GSM7 and c not in GSM7_EXT]
    if hors:
        unites = len(texte)                      # UCS-2 : 70 unités par segment
        par_segment, seul = 70, 70
    else:
        unites = sum(2 if c in GSM7_EXT else 1 for c in texte)
        par_segment, seul = 153, 160             # GSM-7 : 160 seul, 153 en multipart
    messages = 1 if unites <= seul else -(-unites // par_segment)
    return {"unites": unites, "messages": messages, "hors": hors,
            "encodage": "UCS-2" if hors else "GSM-7", "par_segment": par_segment}


def rapport(texte: str, nom: str = "message") -> int:
    a = analyse(texte)
    print(f"{nom} : {len(texte)} caractères · {a['unites']} unités · {a['encodage']} · "
          f"**{a['messages']} segment(s)** de {a['par_segment']}")
    if a["hors"]:
        vus, liste = set(), []
        for i, c in a["hors"]:
            if c not in vus:
                vus.add(c)
                liste.append(f"« {c} » (U+{ord(c):04X} {unicodedata.name(c, '?')}) position {i} "
                             f"→ remplacer par {PIEGES.get(c, 'un caractère GSM-7')!r}")
        print(f"  ✗ {len(a['hors'])} caractère(s) HORS GSM-7 — tout le message passe en UCS-2 "
              f"(70 unités/segment) :")
        for x in liste[:12]:
            print("    · " + x)
        print("  → corriger ces caractères fait retomber le message à "
              f"{analyse(_nettoyer(texte))['messages']} segment(s).")
        return 1
    print("  ✓ tous les caractères sont dans GSM-7.")
    return 0


def _nettoyer(t: str) -> str:
    for k, v in PIEGES.items():
        t = t.replace(k, v)
    return t


def main(argv: list) -> int:
    if not argv:
        data = sys.stdin.read().strip()
        if not data:
            print(__doc__)
            return 2
        return rapport(data)
    if argv[0] == "--file":
        return rapport(open(argv[1], encoding="utf-8").read().strip(), argv[1])
    return rapport(" ".join(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
