#!/usr/bin/env python3
"""audit_deplacement — le verrou du déplacement : ne pas payer la route pour négocier.

Pourquoi ce fichier existe
--------------------------
Le 28/10, King : « Mettons un mécanisme en place pour éviter des pertes de temps et coûts de transport
inutiles. J'ai posé le prix avant de fixer le RDV pour qu'en arrivant sur place on soit sur la même
longueur d'onde, on parle du détail du projet au lieu de négocier encore. »

Le dossier le confirme : le seul rendez-vous qui a converti (DM Optique, 07/10) a eu lieu **après** que
le prix était posé et **avant** l'acompte. Les deux déplacements du 25/09, faits pour convaincre, n'ont
rien signé — et n'ont laissé aucun chiffre sur ce qu'ils ont coûté.

Ce script tient deux choses que rien ne tenait :
  ① le **verrou** — un déplacement prévu passe quatre conditions, ou il est refusé ;
  ② la **mesure** — le coût du transport par rendez-vous, et donc le coût réel d'un client signé.

Ce qu'il ne juge pas
--------------------
- si le prix est le bon (grille : `knowledge/PRIX-2026-10-24.md`) ;
- si le prospect est dans l'ICP du mois (playbook §1.2, décision de King) ;
- si le trajet vaut son prix — ça, seul le compte du mois le dira.

Usage
-----
    python3 tools/qa/audit_deplacement.py                     # leads/DEPLACEMENTS.csv
    python3 tools/qa/audit_deplacement.py --strict            # les avertissements bloquent aussi
    python3 tools/qa/audit_deplacement.py --self-test         # 11 cas, aucun fichier requis

Codes : 0 = aucun bloquant, 1 = au moins un. Un rendez-vous **refusé** n'est pas une perte : c'est une
demi-journée et un plein de carburant restés dans la poche.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "leads" / "DEPLACEMENTS.csv"

AUTHORITY_OK = ("proprietaire", "mandate")
PLANNED = ("prevu", "prevue", "planifie")
CLOSED = ("clos", "clos ", "fait", "termine", "terminé")
ISSUES = ("signe", "signé", "relance", "perdu", "en_attente")
OBJETS_VALIDES = ("specification", "signature", "livraison", "photos")
MAX_MIN = 45


def v(row: dict, key: str) -> str:
    return (row.get(key) or "").strip()


def money(row: dict, key: str) -> float | None:
    raw = v(row, key).replace(" ", "").replace("\u00a0", "").replace(",", ".")
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def verdict(row: dict) -> tuple[list[str], list[str]]:
    """Rend (fails, warns) pour UN déplacement."""
    fails: list[str] = []
    warns: list[str] = []
    statut = v(row, "statut").lower()

    if statut in PLANNED:
        # ── V1 · l'autorité
        auth = v(row, "authority").lower()
        if auth not in AUTHORITY_OK:
            fails.append(f"V1 : `authority` = « {auth or 'vide'} » — un déplacement ne crée pas un "
                         f"dirigeant (cas Dr Fogue, 28/10). Pas de route.")
        # ── V2 · le prix, ET son périmètre, ET l'accord daté
        if not money(row, "prix_annonce"):
            fails.append("V2 : aucun prix annoncé — on arriverait pour négocier, c'est-à-dire pour "
                         "faire sur place le travail qui se fait avant")
        if not v(row, "prix_accepte_le"):
            fails.append("V2 : le prix n'est pas accepté (case `prix_accepte_le` vide) — la date se "
                         "fixe APRÈS l'accord, pas avant")
        if v(row, "perimetre_ecrit").lower() not in ("oui", "y", "yes"):
            fails.append("V2 : le périmètre du prix n'est pas écrit — le client découvrira en séance "
                         "ce qu'il croyait inclus, et c'est là qu'on renégocie")
        # ── V3 · l'objet et la durée
        objet = v(row, "objet").lower()
        if objet not in OBJETS_VALIDES:
            fails.append(f"V3 : objet « {objet or 'vide'} » — un déplacement a un objet de "
                         f"spécification ({', '.join(OBJETS_VALIDES)}), jamais « convaincre »")
        duree = money(row, "duree_min")
        if duree is None:
            warns.append("V3 : durée prévue non écrite — une réunion sans fin devient une réunion")
        elif duree > MAX_MIN:
            warns.append(f"V3 : {int(duree)} min prévues, au-delà du plafond de {MAX_MIN} — "
                         f"au-delà, ce n'est plus une spécification")
        # ── V4 · le coût, connu avant de partir
        if money(row, "cout_transport") is None:
            warns.append("V4 : coût du trajet inconnu AVANT le départ — ce qui n'est pas compté se "
                         "répète")
        # ── l'ICP
        if v(row, "icp").lower() in ("non", "no"):
            fails.append("hors ICP : on ne se déplace pas pour un profil qu'on a décidé de ne pas "
                         "servir (ruling 28/10 : un praticien itinérant n'est pas une cible)")

    elif statut in CLOSED:
        if money(row, "cout_transport") is None:
            warns.append("mesure : coût du transport non renseigné — le rendez-vous est fait, le "
                         "chiffre manque encore (à donner par King, jamais à estimer)")
        issue = v(row, "issue").lower()
        if not issue:
            fails.append("mesure : `issue` vide — un déplacement sans issue écrite n'apprend rien")
        elif issue not in ISSUES:
            warns.append(f"mesure : issue « {issue} » hors vocabulaire ({', '.join(ISSUES)})")
        if v(row, "objet").lower() == "convaincre":
            warns.append("leçon : l'objet était « convaincre » — les deux déplacements de ce type "
                         "du 25/09 n'ont rien signé")

    else:
        warns.append(f"statut « {statut or 'vide'} » inconnu — ni prévu, ni clos : rien n'est jugé")
    return fails, warns


def run(path: pathlib.Path, strict: bool) -> int:
    if not path.exists():
        print(f"✗ {path} introuvable — rien n'a été jugé.")
        return 1
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8-sig")))
    if not rows:
        print(f"✗ {path} est vide — rien n'a été jugé.")
        return 1

    n_fail = n_warn = 0
    print(f"\nVERROU DU DÉPLACEMENT — {path.name}  ({len(rows)} rendez-vous)\n")
    for row in rows:
        fails, warns = verdict(row)
        label = v(row, "prospect") or v(row, "slug") or "?"
        print(f"{'─' * 78}\n{label} · {v(row, 'lieu') or '?'} · {v(row, 'date')} · "
              f"[{v(row, 'statut') or '?'}]")
        if not fails and not warns:
            print("  ✓ verrou vert" if v(row, "statut").lower() in PLANNED else "  ✓ renseigné")
        for f in fails:
            print(f"  ✗ {f}")
        for w in warns:
            print(f"  · {w}")
        n_fail += len(fails)
        n_warn += len(warns)

    # ── la mesure : ce que la route a coûté, et ce qu'elle a rapporté
    clos = [r for r in rows if v(r, "statut").lower() in CLOSED]
    couts = [money(r, "cout_transport") for r in clos]
    connus = [c for c in couts if c is not None]
    signes = [r for r in clos if v(r, "issue").lower() in ("signe", "signé")]
    print(f"{'─' * 78}")
    print(f"rendez-vous clos : {len(clos)} · signés : {len(signes)} · "
          f"transports chiffrés : {len(connus)}/{len(clos)}")
    if connus and len(connus) == len(clos):
        total = sum(connus)
        print(f"coût total des trajets : {total:,.0f} FCFA".replace(",", " "))
        if signes:
            print(f"coût par client signé : {total / len(signes):,.0f} FCFA".replace(",", " ")
                  + f"  ({len(clos)} rendez-vous pour {len(signes)} signature)")
        else:
            print("coût par client signé : aucun signé — le chiffre est le coût à vide")
    else:
        manque = len(clos) - len(connus)
        print(f"⚠ {manque} trajet(s) sans coût : le coût par client signé ne peut pas être calculé. "
              f"Les chiffres se demandent à King — ils ne s'estiment pas.")
    blocking = n_fail + (n_warn if strict else 0)
    print(f"\n{n_fail} bloquant(s) · {n_warn} avertissement(s) → "
          f"{'BLOQUÉ' if blocking else 'OK'}\n")
    return 1 if blocking else 0


CASES = [
    ("prévu, verrou vert", dict(statut="prevu", authority="proprietaire", prix_annonce="150000",
                                prix_accepte_le="2026-10-27", perimetre_ecrit="oui", icp="oui",
                                objet="specification", duree_min="30", cout_transport="4000"), 0, 0),
    ("V1 · consultant itinérant", dict(statut="prevu", authority="sans-autorite",
                                       prix_annonce="150000", prix_accepte_le="2026-10-27",
                                       perimetre_ecrit="oui", icp="oui", objet="specification",
                                       duree_min="30", cout_transport="4000"), 1, 0),
    ("V2 · prix jamais accepté (cas du 25/09)", dict(statut="prevu", authority="proprietaire",
                                                    prix_annonce="100000", perimetre_ecrit="non",
                                                    icp="oui", objet="convaincre", duree_min="45",
                                                    cout_transport="4000"), 3, 0),
    ("V3 · objet « convaincre »", dict(statut="prevu", authority="proprietaire",
                                       prix_annonce="150000", prix_accepte_le="2026-10-27",
                                       perimetre_ecrit="oui", icp="oui", objet="convaincre",
                                       duree_min="30", cout_transport="4000"), 1, 0),
    ("V4 · coût inconnu = avertissement, pas refus", dict(statut="prevu", authority="proprietaire",
                                                          prix_annonce="150000",
                                                          prix_accepte_le="2026-10-27",
                                                          perimetre_ecrit="oui", icp="oui",
                                                          objet="signature", duree_min="30"), 0, 1),
    ("hors ICP : refusé même avec un prix accepté", dict(statut="prevu", authority="proprietaire",
                                                        prix_annonce="150000",
                                                        prix_accepte_le="2026-10-27",
                                                        perimetre_ecrit="oui", icp="non",
                                                        objet="specification", duree_min="20",
                                                        cout_transport="2000"), 1, 0),
    ("clos sans coût : la mesure manque, pas le verrou", dict(statut="clos", issue="perdu",
                                                              objet="convaincre"), 0, 2),
    ("clos sans issue : bloqué", dict(statut="clos", cout_transport="3000"), 1, 0),
    ("clos complet : rien à dire", dict(statut="clos", cout_transport="3000", issue="signe",
                                        objet="specification"), 0, 0),
    ("durée au-delà du plafond", dict(statut="prevu", authority="proprietaire", prix_annonce="150000",
                                      prix_accepte_le="2026-10-27", perimetre_ecrit="oui", icp="oui",
                                      objet="specification", duree_min="90", cout_transport="4000"), 0, 1),
    ("statut inconnu : signalé, pas bloqué", dict(statut=""), 0, 1),
]


def self_test() -> int:
    bad = 0
    print("\nBANC DU VERROU\n")
    for label, row, want_f, want_w in CASES:
        f, w = verdict(row)
        ok = len(f) == want_f and len(w) == want_w
        bad += 0 if ok else 1
        print(f"  {'✓' if ok else '✗'} {label}")
        if not ok:
            print(f"     attendu {want_f}/{want_w} — obtenu {len(f)}/{len(w)}")
            for x in f + w:
                print(f"       {x}")
    print(f"\n{len(CASES) - bad}/{len(CASES)} cas\n")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Le verrou du déplacement et le coût du trajet.")
    ap.add_argument("csv", nargs="?", default=str(DEFAULT))
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    return run(pathlib.Path(args.csv), args.strict)


if __name__ == "__main__":
    sys.exit(main())
