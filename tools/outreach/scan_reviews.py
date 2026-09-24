#!/usr/bin/env python3
"""AMK — SCAN DES AVIS PUBLICS : trouver le motif qui se répète (lot [35], 24/09/2026).

Pourquoi cet outil existe. Une méthode lue le 24/09 (vidéo « leak finder ») : chercher, dans les avis
publics d'un commerce, **la plainte qui revient** — et s'en servir comme angle d'approche, parce qu'un
patron à qui on dit *« trois patients écrivent que personne ne répond au téléphone »* écoute autrement
qu'un patron à qui on dit *« je fais des sites web »*.

Ce que l'outil fait, et rien d'autre : il **compte ce qui est écrit**. On lui colle le texte des avis
(copié à la main depuis Google Maps) ; il repère les familles de plaintes et dit combien d'avis
distincts en parlent. **Il n'invente rien, il ne note personne, il n'écrit aucun fichier** : la sortie
s'affiche et disparaît — c'est volontaire, un avis contient un nom de client, et nous ne stockons pas
ça.

Ce qu'il refuse de faire :
  · **appeler « motif » un fait isolé** — il faut au moins 3 avis distincts (règle de la vidéo : la
    répétition est le signal, l'incident unique n'en est pas un) ;
  · conclure quand l'échantillon est minuscule (moins de 5 avis) : il le dit, et il s'arrête ;
  · employer le vocabulaire du jugement (« mauvais », « honteux ») : le rapport parle de **fuite de
    processus**, jamais de personnes — c'est la formulation de la vidéo, et c'est aussi la nôtre.

Usage :
    python3 tools/outreach/scan_reviews.py avis.txt                # un fichier, un avis par ligne
    python3 tools/outreach/scan_reviews.py --niche "laboratoire" avis.txt
    cat avis.txt | python3 tools/outreach/scan_reviews.py -        # depuis l'entrée standard

Rappel de la maison (FICHE-GOOGLE-PROFILE.md §5) : **jamais d'avis acheté, jamais de texte dicté, jamais
de promesse de faire disparaître un avis.** Cet outil sert à écouter, pas à manipuler.
"""

import re
import sys

# ── Les familles de plaintes, écrites pour un laboratoire / un opticien / une clinique du Cameroun.
#    Deux leçons ont façonné cette table, toutes deux attrapées par le témoin le jour même :
#      ① on normalise le TEXTE (accents, casse) — donc les motifs doivent l'être aussi, sinon
#         « personne ne répond » ne trouve jamais « personne ne repond » ;
#      ② un mot seul attrape son contraire : « résultats impeccables » contient « résultat ». Les
#         motifs sont donc des PHRASES de plainte, jamais des mots isolés — un faux positif coûte
#         plus cher qu'un défaut manqué, et accuser un commerce à tort est pire qu'un silence.
#    Chaque famille porte l'offre AMK qui répond à la fuite (A1/A2/B/C… voir `ORDRE-DES-OFFRES`).
FAMILLES = [
    ("téléphone sans réponse", "C (entretien) ou B (pilote labo)",
     ["personne ne repond", "personne ne repond", "pas de reponse", "aucune reponse", "sans reponse",
      "ne repond pas", "ne decroche pas", "ne decroche jamais", "jamais repondu", "jamais de reponse",
      "injoignable", "ligne occupee", "sonne dans le vide", "no answer", "nobody answers",
      "no one answers", "never answered", "never called back", "didnt pick up", "did not pick up",
      "phone is never answered", "hard to reach"]),
    ("résultat en retard ou introuvable", "B (pilote labo) ou site",
     ["resultat en retard", "resultats en retard", "resultat pas pret", "resultats pas prets",
      "attendre le resultat", "attendre les resultats", "attendre mon resultat", "revenir chercher",
      "revenu chercher", "revenue chercher", "resultat introuvable", "resultats introuvables",
      "resultats perdus", "je reviens pour", "deuxieme deplacement", "results not ready",
      "results were late", "come back for my results", "waiting for my results"]),
    ("rendez-vous impossible à obtenir", "site (formulaire de réservation)",
     ["pas de rendez-vous", "pas de rendez vous", "impossible d'avoir un rendez", "aucun creneau",
      "pas de creneau", "no slots", "no appointment available", "couldnt book", "could not book"]),
    ("prix annoncé faux ou changeant", "contrat (périmètre écrit)",
     ["plus cher que", "prix annonce", "pas le meme prix", "facture double", "surfacture",
      "frais supplementaires", "prix different", "more expensive than quoted", "overcharged",
      "hidden fee", "different price"]),
    ("accueil / attente sur place", "accueil (page + fiche Google)",
     ["mal recu", "personnel impoli", "accueil desagreable", "attendu longtemps", "attente interminable",
      "bouscule", "rude staff", "waited a long time", "unwelcoming"]),
    ("horaires faux ou porte fermée", "fiche Google",
     ["marque ouvert", "etait ferme", "porte fermee", "horaires pas a jour", "closed when",
      "hours are wrong", "said it was open"]),
    ("résultat / analyse erroné", "qualité (jamais promis par nous)",
     ["resultat errone", "resultat faux", "resultat incorrect", "echantillon melange",
      "analyse erronee", "wrong result", "incorrect result", "sample mixed up"]),
    ("message WhatsApp sans suite", "C (entretien) ou B",
     ["pas de suite", "sans suite", "jamais rappele", "message sans reponse", "whatsapp sans reponse",
      "no reply to my message", "never followed up", "no follow up"]),
]

MIN_AVIS = 5        # en dessous, aucun motif ne peut être conclu
MIN_MENTIONS = 3    # nombre d'avis distincts pour parler de répétition


def normalise(s: str) -> str:
    s = s.lower()
    for a, b in (("’", "'"), ("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("î", "i"), ("ô", "o"),
                 ("û", "u"), ("ç", "c"), ("œ", "oe")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


def avis_depuis(texte: str):
    """Un avis par ligne non vide. Un avis peut aussi être séparé par une ligne de tirets."""
    lignes = []
    for bloc in re.split(r"\n\s*[-–—=]{3,}\s*\n", texte):
        for ligne in bloc.split("\n"):
            ligne = ligne.strip()
            if len(ligne) > 3:
                lignes.append(ligne)
    return lignes


def scan(avis, niche=""):
    resultats = []
    for nom, offre, mots in FAMILLES:
        touches = []
        for i, a in enumerate(avis):
            n = normalise(a)
            if any(m in n for m in mots):
                touches.append(i)
        if touches:
            resultats.append((nom, offre, touches))
    resultats.sort(key=lambda r: -len(r[2]))
    return resultats


def rapport(avis, resultats, niche=""):
    L = []
    titre = "SCAN DES AVIS PUBLICS" + ((" — " + niche) if niche else "")
    L.append(titre)
    L.append("=" * len(titre))
    L.append("%d avis analysé(s). Rien n'est enregistré : ce rapport ne vit que sur ton écran."
             % len(avis))
    L.append("")
    if len(avis) < MIN_AVIS:
        L.append("STOP — échantillon trop petit (%d avis, minimum %d pour conclure quoi que ce soit)."
                 % (len(avis), MIN_AVIS))
        L.append("Avec aussi peu d'avis, une plainte isolée peut venir d'une mauvaise journée. On note le")
        L.append("fait tel quel, on n'en fait pas un motif, et on n'en parle pas au client comme d'un")
        L.append("problème systématique.")
        return "\n".join(L)

    if not resultats:
        L.append("Aucune plainte répétée dans le texte fourni. Ce n'est pas un échec : ça veut dire")
        L.append("qu'il n'y a pas d'angle « fuite » ici — on approchera ce prospect autrement, ou pas.")
        return "\n".join(L)

    motif = [r for r in resultats if len(r[2]) >= MIN_MENTIONS]
    isole = [r for r in resultats if len(r[2]) < MIN_MENTIONS]

    if motif:
        L.append("MOTIF(S) RÉPÉTÉ(S) — %d avis distincts minimum :" % MIN_MENTIONS)
        for nom, offre, t in motif:
            L.append("")
            L.append("  ▸ %s — %d avis sur %d (%d %%)"
                     % (nom, len(t), len(avis), round(100 * len(t) / len(avis))))
            L.append("    Offre AMK qui y répond : %s" % offre)
            L.append("    À dire au client, sans juger : « plusieurs avis parlent de %s — ce n'est pas"
                     % nom)
            L.append("    un problème de personnes, c'est un trou dans le parcours. »")
            for i in t[:3]:
                L.append("      · avis %d : « %s »" % (i + 1, avis[i][:110]))
    else:
        L.append("Aucun motif répété : les plaintes relevées sont isolées (moins de %d avis sur le même"
                 % MIN_MENTIONS)
        L.append("sujet). On ne les présente JAMAIS comme un problème du commerce.")

    if isole:
        L.append("")
        L.append("Mentions isolées (à ne pas présenter comme un motif) :")
        for nom, offre, t in isole:
            L.append("  · %s — %d avis" % (nom, len(t)))

    L.append("")
    L.append("── Rappels qui ne bougent pas ──")
    L.append("· Jamais en public : on parle au patron ou à personne. Un avis se lit, il ne se commente pas.")
    L.append("· Jamais un nom de client, jamais un avis cité en entier devant quelqu'un d'autre.")
    L.append("· On ne promet JAMAIS de faire disparaître un avis (FICHE-GOOGLE-PROFILE.md §5).")
    L.append("· On ne promet aucun chiffre de chiffre d'affaires gagné : la fuite se décrit, elle ne")
    L.append("  se vend pas au pourcentage.")
    return "\n".join(L)


def main(argv):
    niche = ""
    args = list(argv)
    if "--niche" in args:
        i = args.index("--niche")
        niche = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__.strip().splitlines()[-6].strip())
        return 2
    src = args[0]
    if src == "-":
        texte = sys.stdin.read()
    else:
        try:
            texte = open(src, encoding="utf-8").read()
        except OSError as e:
            print("fichier illisible : %s" % e)
            return 1
    avis = avis_depuis(texte)
    print(rapport(avis, scan(avis, niche), niche))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
