#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""« Quatre étapes avant la monture » — le premier film où M. Domche parle.

Pourquoi ce fichier existe (29/10/2026, tour 232)
--------------------------------------------------
King, 29/10 : *« Passons à la video de M. Domche, I need a script and a message in this chat to send to
him to ask if he is willing to do it. »*

Trois choses du dépôt décident de ce script, et aucune n'est un goût personnel :

1. **La décision « pas de visage » du mois 1** (`DIRECTION-MARQUE-v2` §10.4) avait une exception écrite,
   et une seule : `content-plan-month1.md` §9 — *« test conditionné à l'accord du client : 2 clips de
   M. Domche (service/processus, 20–34 s verticale) »*. Ce film **est** cette exception. Il ne peut donc
   pas se tourner sur un accord verbal : `launch/AUTORISATION-IMAGE-2026-10-29.md` se signe avant.

2. **L'axe de marque est « l'expertise qui précède la vente »** (`DIRECTION-MARQUE-v2` §5 : A comme
   moteur, B comme preuve, C comme limite). Le film ne montre donc pas une monture : il montre **ce qui
   se passe avant qu'on en parle**. C'est la correction de la v1.0, qui vendait l'inventaire.

3. **Sa propre parole est la meilleure matière** (`onboarding/REPONSES-CLIENT.md`, 15/10 16:54) : il
   décrit l'examen en quatre temps — *anamnèse, bilan optique, acuités visuelles, réfraction* — et il
   écrit « je prends le temps pour chaque étape ». Le script ne traduit pas ça en jargon : il le dit en
   quatre phrases qu'un patient peut répéter.

Ce que le film ne dit pas, et c'est la partie qui compte
--------------------------------------------------------
Aucun prix (verrou client, 10/10) · aucun nombre de montures (ruling King 21/10) · aucune marque de
monture · aucune promesse sur la vue · aucun titre professionnel non prouvé par une pièce (la note de
`REPONSES-CLIENT` est explicite : « Optometriste » ne se publie qu'avec un diplôme) · aucun symptôme
nommé. La seule chose qu'il promet, c'est **le temps qu'il prend** et **une heure de rendez-vous**.

Le chiffre prononcé, et pourquoi celui-là
------------------------------------------
`audit_story` exige une preuve **dite**, pas seulement affichée. Le seul chiffre disponible ici est
**quatre** : les quatre étapes de l'examen, ses mots, vérifiables, et il ne dit rien de la santé de
personne. Un nombre de montures serait un verrou cassé ; un taux de réussite serait une promesse.

Trois coupes, un tournage
-------------------------
Un seul après-midi, une seule prise de parole, quatre pièces :

| Pièce | Où | Durée | Ce qu'elle fait |
|---|---|---|---|
| **le film** (`SCRIPT`) | site, Facebook, WhatsApp | ~67 s | le portrait calme : les quatre étapes, et le refus de vendre |
| **coupe 1** | TikTok | ~19 s | le mécanisme (« quatre étapes avant la monture ») |
| **coupe 2** | Facebook | ~24 s | la sortie honnête (« il m'arrive de dire de ne rien acheter ») |
| **coupe 3** | Reels | ~20 s | ce qu'il demande avant de mesurer (le temps, l'accueil) |

**Ce qui se filme large et long** (`CONTENT-CREATION` §5 quater) : chaque réponse est tournée **deux
fois**, avec **trois secondes de respiration** avant et après. Une réponse tournée à la seconde près ne
se remonte pas pour l'autre réseau.

Portes qui lisent ce fichier
----------------------------
    python3 tools/qa/audit_story.py clients/dm-optic/content/tournage/DOMCHE-01-SCRIPT.py
    python3 clients/dm-optic/content/tournage/DOMCHE-01-SCRIPT.py      # les quatre pièces d'un coup
    python3 tools/qa/audit_claims.py clients/dm-optic/content          # les verrous client
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RACINE / "tools" / "qa"))

from audit_hook import Hook  # noqa: E402
from audit_story import Line, Script  # noqa: E402

# ── l'accroche, telle que la porte la lit (`knowledge/HOOKS-2026-10-25.md`) ─────────────────────
# Niveau 2, **Magician** : la phrase ne rapporte pas un état, elle révèle un mécanisme — ce qui se passe
# avant la monture. Les quatre mots de puissance y sont : sujet (« vous », « je »), action (« montrer »,
# « fais »), objectif (« quatre choses »), contraste (« avant de vous montrer une monture » = on ne vend
# pas d'abord). L'écrit arrive en premier (HOOK-FIRST : écrit > visuel > parlé).
HOOK = Hook(
    text="Je mesure avant de vous montrer une monture. On ne repart pas avec le premier venu.",
    level=2,
)

# ── le film · 67,0 s · 7 beats ───────────────────────────────────────────────────────────────────
# Durées **prévues**, pas mesurées : la voix de M. Domche décidera, et le montage se calera sur elle
# (`voice/timing.json` remplacera ces bornes). Débit visé 2,3 à 2,6 mots/s — il parle lentement, et c'est
# la marque (`DIRECTION-MARQUE-v2` §4 : voix lente, posée, une idée par phrase).
SCRIPT = Script(
    piece="domche-01",
    promise="jour et une heure",
    proof_on_screen="4 ÉTAPES · 8h30–13h00 (horaires du cabinet, /contact/)",
    lines=[
        Line("cas", "Je mesure avant de vous montrer une monture. On ne repart pas avec le premier venu.",
             "cas+lockin", 0.0, 4.8),
        Line("lockin", "La première, c'est vous. Je vous écoute. Ce que vous faites dans la journée. "
                       "Ce qui vous gêne, depuis quand.",
             "lockin", 4.8, 11.5),
        Line("mesure", "Ensuite je mesure. Le bilan, les acuités, la réfraction. Quatre étapes en tout, "
                       "et à la fin je sais ce qu'il vous faut.",
             "corps+preuve", 11.5, 22.5),
        Line("rehook", "Et parfois, la réponse, c'est qu'il ne vous faut rien.",
             "rehook", 22.5, 28.0),
        Line("honnete", "Je vous le dis quand même. Si vous voyez bien, ne venez pas. On peut passer un "
                        "moment ensemble et vous repartez sans rien. Ce n'est pas une perte pour moi.",
             "corps", 28.0, 41.5),
        Line("cabinet", "L'examen se fait le matin, de 8h30 à 13h00. L'après-midi, on regarde les "
                        "montures ensemble, si vous en voulez une. Le cabinet est au premier étage, "
                        "dernière porte à droite.",
             "corps+preuve", 41.5, 55.5),
        Line("sortie", "Si vous éloignez votre téléphone pour lire, écrivez-nous sur WhatsApp. "
                       "On vous propose un jour et une heure, et vous décidez après.",
             "sortie", 55.5, 67.5),
    ],
)

# ── les trois coupes ────────────────────────────────────────────────────────────────────────────
# Elles ne sont pas des résumés du film : chacune prend **un** beat et le pousse. Un résumé de 67 s en
# 16 s ne retient personne ; une seule idée, si.

# Coupe 1 — TikTok · « quatre étapes avant la monture » · 19,1 s
# La grille maison du 23/10 vise 12–16 s sur TikTok (`CONTENT-CREATION` §5 quater). Cette coupe en fait
# 19, et c'est une **déviation déclarée** : M. Domche parle lentement, et couper dans ses phrases pour
# gagner trois secondes lui ferait dire autre chose que ce qu'il dit. On ne remplit pas : on ne coupe pas
# un homme en train d'expliquer son métier.
COUPE_1 = Script(
    piece="domche-01-tiktok",
    promise="jour et une heure",
    lines=[
        Line("cas", "Je mesure avant de vous montrer une monture.",
             "cas+lockin", 0.0, 3.0),
        Line("ecoute", "La première, c'est vous. Je vous écoute.",
             "lockin", 3.2, 5.6),
        Line("mesure", "Ensuite je mesure. Quatre étapes, et à la fin je sais ce qu'il vous faut.",
             "corps+preuve", 5.6, 10.0),
        Line("rehook", "Parfois, la réponse, c'est qu'il ne vous faut rien.",
             "rehook", 10.0, 12.6),
        Line("honnete", "Si vous voyez bien, ne venez pas.",
             "corps", 12.6, 14.8),
        Line("sortie", "Écrivez-nous sur WhatsApp, on vous propose un jour et une heure, "
                       "et vous décidez après.",
             "sortie", 14.8, 19.1),
    ],
)

# Coupe 2 — Facebook · « il m'arrive de dire de ne rien acheter » · 24,0 s
COUPE_2 = Script(
    piece="domche-01-facebook",
    promise="jour et une heure",
    lines=[
        Line("cas", "Il m'arrive de recevoir quelqu'un et de lui dire de ne rien acheter.",
             "cas", 0.0, 5.0),
        Line("lockin", "Ce n'est pas une formule. C'est ce que je fais quand la mesure ne montre rien.",
             "lockin", 5.0, 11.0),
        Line("mesure", "L'examen fait quatre étapes. Si les quatre ne montrent rien, je vous le dis.",
             "corps+preuve", 11.0, 17.5),
        Line("rehook", "Et vous repartez sans rien acheter.",
             "rehook", 17.5, 20.5),
        Line("honnete", "Ce n'est pas une vente perdue pour moi.",
             "corps", 20.5, 23.0),
        Line("sortie", "Si vous éloignez votre téléphone pour lire, écrivez-nous. "
                       "On vous propose un jour et une heure, et vous décidez après.",
             "sortie", 23.0, 29.0),
    ],
)

# Coupe 3 — Reels · « ce que je demande avant de mesurer » · 30,0 s
COUPE_3 = Script(
    piece="domche-01-reels",
    promise="jour et une heure",
    lines=[
        Line("cas", "Avant de mesurer, je vous pose une question qui n'a rien à voir avec les yeux.",
             "cas", 0.0, 4.5),
        Line("lockin", "Je demande ce que vous faites dans la journée. C'est ça qui décide de la "
                       "monture, pas la mode.",
             "lockin", 4.5, 11.0),
        Line("corps", "Un chauffeur et un comptable ne passent pas leur journée devant la même chose.",
             "corps", 11.0, 16.0),
        Line("rehook", "L'examen commence par quatre étapes, et la première, c'est vous qui parlez.",
             "rehook+preuve", 16.0, 21.0),
        Line("corps2", "Après, seulement, on regarde les montures.",
             "corps", 21.0, 24.0),
        Line("sortie", "Écrivez-nous sur WhatsApp, on vous propose un jour et une heure, "
                       "et vous décidez après.",
             "sortie", 24.0, 30.0),
    ],
)

PIECES = [SCRIPT, COUPE_1, COUPE_2, COUPE_3]


if __name__ == "__main__":
    from audit_story import audit

    total_ok = True
    for piece in PIECES:
        verdict = audit(piece)
        print(f"\n── {piece.piece} · {piece.total:.1f} s · {len(piece.lines)} beats")
        for l in piece.lines:
            print(f"   {l.name:9} {l.duree:5.2f} s · {'+'.join(sorted(l.roles)):14} · {l.text}")
        mots = sum(l.mots for l in piece.lines)
        print(f"   débit : {mots / piece.total:.2f} mots/s · {mots} mots")
        if verdict.ok:
            print("   ✓ récit")
        else:
            print("   ✗ récit")
            total_ok = False
        for f in verdict.fails:
            print("      ⛔", f)
        for w in verdict.warns:
            print("      ⚠ ", w)
    sys.exit(0 if total_ok else 1)
