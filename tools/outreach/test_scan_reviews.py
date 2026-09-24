#!/usr/bin/env python3
"""Le témoin du scan des avis — lot [35].

Un outil qui trouve 0 constat doit prouver qu'il mord, et un outil qui « trouve un motif » doit prouver
qu'il refuse d'en voir un là où il n'y en a pas. Cinq cas, dont deux négatifs :

  1. trois avis sur douze parlent du téléphone         → motif répété, offre « C », extraits montrés
  2. deux avis seulement sur le même sujet             → mention isolée, JAMAIS un motif
  3. quatre avis, toutes plaintes différentes          → échantillon trop petit : il s'arrête
  4. douze avis sans plainte                           → « pas d'angle fuite », dit franchement
  5. le texte accentué/majuscules/anglais               → les mêmes familles se déclenchent

Et deux règles de la maison vérifiées dans la sortie : il ne promet rien (pas de « faire disparaître »,
aucun pourcentage de chiffre d'affaires) et il rappelle qu'aucun avis ne se commente en public.
"""

import io
import os
import subprocess
import sys
import tempfile

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_reviews.py")
ok = fail = 0


def check(cond, label):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label)


def run(texte):
    tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tmp.write(texte)
    tmp.close()
    r = subprocess.run([sys.executable, TOOL, tmp.name], capture_output=True, text=True)
    os.unlink(tmp.name)
    return r.returncode, r.stdout


AVIS_TELEPHONE = """Excellent accueil et résultats rapides, je recommande.
Les résultats étaient prêts le jour même, personnel très professionnel.
J'ai appelé trois fois personne ne répond, j'ai dû venir sur place.
Prise de sang faite le matin, résultat le soir. Parfait.
Personne ne répond au téléphone, j'ai attendu deux jours pour un renseignement.
Très bon laboratoire, prix corrects.
Le personnel est aimable, rien à dire.
Impossible de joindre le laboratoire par téléphone, le numéro sonne dans le vide.
Résultats toujours à l'heure, je viens depuis des années.
Accueil correct, un peu d'attente le samedi.
Les résultats étaient en retard de deux jours cette fois.
Bon suivi, la biologiste explique bien.
"""

AVIS_DEUX = """Personne ne répond au téléphone, c'est dommage.
Encore une fois pas de réponse au téléphone.
Très satisfait des résultats, rapides et clairs.
Personnel accueillant, je recommande.
Bon laboratoire de quartier.
Résultats conformes, rien à signaler.
"""

AVIS_TROP_PEU = """Fermé alors que c'est marqué ouvert.
Le prix était plus cher que ce qu'on m'avait dit.
Personnel impoli, j'ai attendu longtemps.
Résultat avec une erreur, il a fallu refaire.
"""

AVIS_POSITIFS = """Très bon accueil, résultats dans les temps.
Le personnel est professionnel et à l'écoute.
Je recommande ce laboratoire, prix honnêtes.
Au top, comme d'habitude.
Rapide, propre, efficace.
Merci pour votre disponibilité.
Toujours satisfait depuis des années.
Parfait du début à la fin.
Résultats impeccables.
Bon rapport qualité prix.
Équipe sérieuse et compétente.
Rien à redire, je reviendrai.
"""

AVIS_ANGLAIS = """Nobody answers the phone, I called on Monday and Tuesday.
I called three times, no answer at all.
The phone is never answered, I had to walk in.
Results were ready the same day, great service.
The team is professional and kind.
Best lab in the neighbourhood.
"""


def main():
    # 1 · le motif se voit
    rc, out = run(AVIS_TELEPHONE)
    check(rc == 0 and "MOTIF" in out, "trois avis sur le téléphone : motif répété annoncé")
    check("TÉLÉPHONE SANS RÉPONSE".lower() in out.lower(), "la famille nommée est la bonne")
    check("avis et 12" not in out and "3 avis sur 12" in out, "le compte est exact (3 sur 12)")
    check("(C)" in out or "Offre AMK qui y répond : C" in out, "l'offre qui répond est rattachée")

    # 2 · un fait isolé n'est pas un motif
    rc, out = run(AVIS_DEUX)
    check("MOTIF(S) RÉPÉTÉ(S)" not in out, "deux mentions : AUCUN motif annoncé")
    check("isol" in out.lower(), "deux mentions : présentées comme isolées")

    # 3 · échantillon trop petit = il s'arrête
    rc, out = run(AVIS_TROP_PEU)
    check("STOP" in out and "trop petit" in out, "quatre avis : l'outil refuse de conclure")

    # 4 · pas de fuite : dit franchement
    rc, out = run(AVIS_POSITIFS)
    check("Aucune plainte répétée" in out, "douze avis sans plainte : « pas d'angle fuite »")

    # 5 · l'anglais et la casse
    rc, out = run(AVIS_ANGLAIS)
    check("MOTIF" in out, "avis en anglais : la même famille se déclenche (téléphone)")

    # 6 · les garde-fous sont imprimés
    rc, out = run(AVIS_TELEPHONE)
    check("jamais" in out.lower() and "disparaître" in out.lower(),
          "le rappel « jamais faire disparaître un avis » est imprimé")
    check("pourcentage" in out.lower() or "chiffre d'affaires" in out.lower(),
          "le rappel « aucun chiffre d'affaires promis » est imprimé")

    # 7 · rien n'est écrit sur le disque
    before = set(os.listdir("/tmp"))
    run(AVIS_TELEPHONE)
    after = set(os.listdir("/tmp"))
    check(len(after - before) <= 0, "l'outil n'écrit aucun fichier (aucun avis n'est stocké)")

    print("\n%d assertion(s) verte(s), %d échec(s) — le scan mord, et surtout il refuse de mordre "
          "là où il n'y a rien." % (ok, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
