#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""« La monture cherche son nom » — épisode 1 (H08) : le SCRIPT, et l'histoire qui le tient.

Pourquoi ce fichier existe (27/10/2026, tour 196)
-------------------------------------------------
King, après la v2 parlée : *« the video style and idea are good, but I need you to audit and edit the
script also making it more human. Create a story behind the naming of the glasses, if not viewers won't
feel engaged, won't see a reason to participate … ask yourself at each stage: if I was a viewer will I
stop doomscrolling just to name frames? We can create games/competitions behind it or even polls. »*

La v2 disait **quoi faire** (« donnez un nom à cette monture »). Elle ne disait pas **pourquoi ce cadre
mérite un nom**, ni **ce que le spectateur y gagne**. Un code de stock n'est pas une histoire ; « 65
montures sans nom » est un inventaire. Le tour 196 remplace l'inventaire par trois choses vérifiables :

1. **un fait que personne ne remarque** — sur notre site, le nom d'une monture *est* son code de stock.
   C'est vrai, c'est daté, ça se vérifie dans `hosting/previews/dmoptic/montures/` : les 40 fiches en
   ligne s'appellent `H08 · Double pont aviateur noir et doré`, `F24 · …`, `E07 · …`. L'échelle des
   histoires l'appelle **niveau 2, Magician** : « voilà comment ça marche vraiment ».
2. **une raison locale de nommer** — ici, un taxi a un nom, une moto aussi. On ne l'affirme pas comme une
   statistique : on le montre, et le spectateur reconnaît sa ville (`knowledge/HOUSE-KNOWLEDGE-BASE` §8,
   copie « chaude, directe, spécifique »).
3. **un enjeu qui reste** — le nom retenu est écrit sur la fiche de la monture, sur le site. Il ne
   disparaît pas avec la vidéo. C'est la seule récompense qu'on puisse promettre **sans dépenser un
   franc du cabinet et sans promettre un résultat de vue**.

Le jeu en trois manches (ce que King appelait « games/competitions/polls »)
--------------------------------------------------------------------------
| Manche | Où | Ce qu'on demande | Pourquoi c'est le plus petit pas possible |
|---|---|---|---|
| **1 · la proposition** | cette vidéo | **un seul mot**, en commentaire | un mot, pas un texte ; la contrainte en fait un jeu, pas une dissertation |
| **2 · le vote** | J+2, un post court | **1 ou 2**, entre les deux mots les plus proposés | un caractère. Ceux qui ont proposé reviennent défendre leur mot |
| **3 · le nom reste** | épisode 2 | rien : on annonce | le nom est écrit sur la fiche, et celui qui l'a trouvé est crédité **avec son accord** |

Ce qui n'est **pas** promis, et ne le sera pas : une remise, une monture offerte, un délai de livraison,
un résultat de vue. Aucune de ces quatre choses n'est au cabinet, et une promesse qu'on ne tient pas
coûte le compte (`knowledge/CONTENT-CREATION` §6 bis).

Les trois images du film (tour 198)
-----------------------------------
King : *« en plus du script et ce qui apparaît sur l'écran, je veux que tu ajoutes des images »*, avec
trois beats nommés. Le film ne raconte donc plus seulement : il **montre**.

| beat | l'image | sa provenance |
|---|---|---|
| 1 « elle n'a pas de nom » | la monture, macro sur le double pont | photo **réelle** du cabinet (site, H08) |
| 2 « quarante montures, toutes avec un code » | le catalogue du site qui défile, codes H02/H04/H05 lisibles | capture du **vrai site**, 27/10/2026 |
| 4 « elle ira sur un visage » | une personne portant la H08 | **image générée** — l'exception que King a accordée |
| 5 « le nom s'écrit sur sa page » | la fiche H08, posée dans le cadre | capture du **vrai site**, 27/10/2026 |

Ce que l'exception ne couvre pas : aucune autre image générée n'entre dans la série. Le visage n'est pas un
patient, ce n'est pas un portrait du cabinet, et la monture qu'il porte est une **approximation** du H08 —
lunettes à double pont, noir et doré. Le kit le dit au spectateur (§8) ; on ne fait pas passer une image
générée pour une photo du cabinet.

Porte W43 §12b — [x] cas client d'abord · [x] un seul axe · [x] objet réel · [x] preuve citée une fois
                 · [x] sortie honnête · [x] un seul CTA

Portes qui lisent ce fichier
----------------------------
    python3 tools/qa/audit_story.py clients/dm-optic/content/month1/w3/MONTURE-01-SCRIPT.py
    python3 tools/qa/audit_hook.py --text "Votre monture n'a pas de nom. Elle s'appelle H08, comme un colis."
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RACINE / "tools" / "qa"))

from audit_hook import Hook  # noqa: E402
from audit_story import Line, Script  # noqa: E402

# ── l'accroche, telle que la porte la lit (`knowledge/HOOKS-2026-10-25.md`) ─────────────────────
# Niveau 2 (**Magician**) et pas 1 : la phrase ne rapporte pas un état, elle **révèle un mécanisme** —
# le nom qu'on croit être un nom est un code de stock. C'est exactement ce que la fiche du site montre.
HOOK = Hook(
    text="Elle n'a pas de nom. Vous choisissez celui qui reste.",
    level=2,
)

# ── le script, tel qu'il est PRONONCÉ (pas tel qu'il est affiché) ────────────────────────────────
# Durées **mesurées** sur les clips de la voix (`voice-05`, 27/10, tour 197) : la voix ne se comprime
# pas, c'est le montage qui se cale sur elle. 0,28 s de respiration entre deux beats.
#
# Deux choses ont changé au tour 197, et elles viennent de King :
# ① « Votre monture » **n'est pas la leur** — la pièce parle maintenant de « elle », et c'est le
#    spectateur qui est **sujet** de la phrase (« vous choisissez ») : il ne possède rien, il décide ;
# ② le **vote binaire** entre au film (Éclat / Minuit) : un nom à taper vaut mieux qu'une page blanche
#    à remplir, et « ou votre mot » garde la porte ouverte à celui qui a mieux.
SCRIPT = Script(
    piece="monture-01",
    promise="nom",
    proof_on_screen="40 MONTURES · 40 CODES (site DM Optique, 27/10/2026)",
    lines=[
        Line("cas", "Elle n'a pas de nom. Vous choisissez celui qui reste.",
             "cas", 0.00, 3.93),
        Line("lockin", "Sur notre site, quarante montures. Toutes s'appellent par un code.",
             "lockin+preuve", 4.21, 8.97),
        Line("corps", "Celle-ci s'appelle H zéro huit. Deux noms sont sur la table : Éclat ou Minuit.",
             "corps", 9.25, 15.13),
        Line("rehook", "Elle ira sur un visage, tous les jours. Elle mérite mieux qu'un code.",
             "rehook", 15.41, 19.26),
        Line("corps", "Le nom qui gagne s'écrit sur sa page, et il y reste.",
             "corps", 19.54, 22.93),
        Line("sortie", "Écrivez A, B, ou votre mot. On vous montre le nom qui gagne.",
             "sortie", 23.21, 26.10),
    ],
)

if __name__ == "__main__":
    from audit_story import audit

    verdict = audit(SCRIPT)
    for l in SCRIPT.lines:
        print(f"  {l.name:8} {l.duree:5.2f} s · {l.roles} · {l.text}")
    print()
    print("durée déclarée :", SCRIPT.total, "s" if SCRIPT.duree_connue else "s (durées non mesurées)")
    print("✓ script" if verdict.ok else "✗ script")
    for f in verdict.fails:
        print("   ⛔", f)
    for w in verdict.warns:
        print("   ⚠ ", w)
