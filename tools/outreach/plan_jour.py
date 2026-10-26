#!/usr/bin/env python3
"""Le plan du matin — ce que King envoie aujourd'hui, dans quel ordre, et ce qui manque.

    python3 tools/outreach/plan_jour.py --date 2026-10-27
    python3 tools/outreach/plan_jour.py --date 2026-10-27 --ecrire sales/PLAN-2026-10-27.md

Trois sources, une seule sortie :

1. les **lots écrits** (`sales/ENVOI-*.md`) — le texte est prêt, il ne manque que le droit d'envoyer ;
2. le **verdict** de `verify.py` pour chaque numéro (`leads/VERIF-<date>.json`) : ENVOYER / KING-TRANCHE /
   PAS-ENVOYÉ / JAMAIS / HORS-CIBLE ;
3. le **stock** composable restant, c'est-à-dire ce que la fabrique pourrait encore écrire.

L'ordre n'est pas la préférence : il va du droit le plus établi au plus faible. Un message qu'on n'a pas
le droit d'envoyer ne part pas — même s'il est le mieux écrit du lot. Ce que l'outil ne fait pas : il
n'envoie rien, il n'écrit aucun message, et il ne devine aucune porte. Sans preuve datée, la ligne reste
`PAS-ENVOYÉ` et c'est King qui tranche, en huit secondes, sur son téléphone.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compose  # noqa: E402

RACINE = Path(__file__).resolve().parents[2]
ORDRE = ["ENVOYER", "KING-TRANCHE", "PAS-ENVOYÉ", "JAMAIS", "HORS-CIBLE"]
SANS = "PAS-ENVOYÉ"      # absent du vérificateur = aucune porte franchie, pas « propre »
MARGE = "·"


def lots(dossier: Path) -> list[tuple[str, str, str]]:
    """(fichier, nom, numéro) de tous les messages déjà écrits, lots retirés exclus."""
    out: list[tuple[str, str, str]] = []
    for p in sorted(dossier.glob("ENVOI-*.md")):
        for m in compose.parse(p):
            out.append((p.name, re.sub(r"^#\d+\s*", "", m.label).strip(), compose.numero(m.phone)))
    return out


def verdicts(chemin: Path) -> dict[str, str]:
    if not chemin.exists():
        return {}
    return {x["num"]: x["verdict"] for x in json.loads(chemin.read_text(encoding="utf-8"))}


def plan(date: str, dossier: Path | None = None, choisis: list[str] | None = None) -> dict:
    dossier = dossier or RACINE / "sales"
    ecrits = []
    for nom in (choisis or []):
        p = RACINE / nom if not Path(nom).is_absolute() else Path(nom)
        ecrits += [(p.name, re.sub(r"^#\d+\s*", "", m.label).strip(), compose.numero(m.phone))
                   for m in compose.parse(p)]
    if not choisis:
        ecrits = lots(dossier)
    v = verdicts(RACINE / "leads" / f"VERIF-{date}.json")
    lignes = [{"lot": lot, "nom": nom, "num": num, "verdict": v.get(num, SANS)}
              for lot, nom, num in ecrits]
    lignes.sort(key=lambda l: (ORDRE.index(l["verdict"]), l["lot"], l["nom"]))
    # Le stock : ce que la fabrique pourrait encore écrire, hors lots déjà écrits et hors condamnés.
    restants = compose.lit_crm(compose.RACINE / "leads" / "CRM.csv")
    pris = {l["num"] for l in lignes}
    libres = [l for l in restants if l.numero not in pris
              and v.get(l.numero) not in ("JAMAIS", "HORS-CIBLE")]
    return {"date": date, "lignes": lignes,
            "compte": {k: sum(1 for l in lignes if l["verdict"] == k) for k in ORDRE},
            "libres": libres, "verif_lu": bool(v)}


def rendu(p: dict) -> str:
    c = p["compte"]
    out = [f"# Plan du {p['date']} — {len(p['lignes'])} message(s) écrit(s), "
           f"{c['ENVOYER']} prêt(s) sans décision",
           "",
           "```text",
           f"ENVOYER       {c['ENVOYER']:>3}  les trois portes, contrôle du 25/10 — partent tels quels",
           f"KING-TRANCHE  {c['KING-TRANCHE']:>3}  8 s de WhatsApp, et la ligne se tranche",
           f"PAS-ENVOYÉ    {c['PAS-ENVOYÉ']:>3}  aucune porte franchie : c'est la file de vérification",
           f"JAMAIS        {c['JAMAIS']:>3}  numéro vu mort : la ligne se barre, elle ne se réécrit pas",
           f"HORS-CIBLE    {c['HORS-CIBLE']:>3}  le cabinet a déjà un site : il ne reçoit rien",
           "```",
           "",
           "| # | Verdict | Cabinet | Numéro | Lot |",
           "|---|---|---|---|---|"]
    for i, l in enumerate(p["lignes"], 1):
        out.append(f"| {i} | **{l['verdict']}** | {l['nom']} | {l['num']} | {l['lot']} |")
    out += ["", "## Ce que le jour ne contient pas encore", ""]
    n = len(p["libres"])
    out.append(f"**{n}** ligne(s) composable(s) sans message écrit"
               + (f" : {', '.join(l.nom for l in p['libres'][:8])}"
                  + ("…" if n > 8 else "") if n else " — le stock est épuisé."))
    if not p["verif_lu"]:
        out.append("")
        out.append("⚠ aucun `leads/VERIF-<date>.json` : toutes les lignes sont lues `PAS-ENVOYÉ`, "
                   "et c'est la lecture juste — sans preuve, la porte n'est pas franchie.")
    out += ["", "## Les trois gestes du matin", "",
            "1. **Ouvrir WhatsApp** et passer les `KING-TRANCHE` : huit secondes par numéro, on barre "
            "plutôt que de composer.",
            "2. **Envoyer dans l'ordre du tableau** — les `ENVOYER` d'abord, jamais l'inverse.",
            "3. **Cocher le tracker** le soir (`sales/CAMPAGNE-VOLUME-2026-10-26.md` §5) : envoyé, lu, "
            "répondu, bloqué.", ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--dossier", default="")
    ap.add_argument("--lots", nargs="*", default=[],
                    help="les lots à lire, dans l'ordre d'envoi — par défaut tous les sales/ENVOI-*.md")
    ap.add_argument("--ecrire", default="", help="écrit le plan dans un fichier markdown")
    a = ap.parse_args()
    p = plan(a.date, Path(a.dossier) if a.dossier else None, a.lots)
    texte = rendu(p)
    if a.ecrire:
        Path(a.ecrire).write_text(texte, encoding="utf-8")
        print(f"{len(p['lignes'])} message(s), {p['compte']['ENVOYER']} prêt(s) → {a.ecrire}")
    else:
        print(texte)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
