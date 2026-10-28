#!/usr/bin/env python3
"""audit_qualification — la porte d'entrée : vérifie qu'un prospect a le droit d'être prospecté.

Pourquoi ce fichier existe
--------------------------
Le 26/10, un message a été écrit à un **ophtalmologue itinérant** comme s'il était un opticien
propriétaire. Il a répondu en cinq minutes : « je ne suis pas opticien patron ». Le 28/10, King a
tranché : « il n'est pas dirigeant (decision taker), il est consultant itinérant… we need a clear
qualification process ».

Les règles existaient — `RESEARCH-STANDARD` §8b (« type d'acheteur »), `MQL` porte M4, le playbook
ICP §1.2 — mais `audit_outreach.py` dit lui-même, dans son en-tête, qu'il **ne les vérifie pas** :
« les trois portes §8b (numéro joint sur WhatsApp, intention numérique, type d'acheteur) — elles se
vérifient à la main, avant l'écriture ». À la main, un nom dans une case suffisait.

Ce script lit `leads/CRM.csv` et applique **ce qui se prouve par les champs**. Le reste reste humain,
et c'est écrit dans le rapport : une porte mécanique attrape l'oubli, pas le mensonge.

Ce qu'il juge (voir `sales/QUALIFICATION-2026-10-28.md`)
--------------------------------------------------------
  Q1 · l'acheteur   `authority` connu et ≠ « sans-autorite », avec `contact_name` + `contact_role`
  Q2 · l'actif      une organisation et une ville renseignées
  Q3 · le métier    aucun code `Q3_hors_icp` sur une ligne encore engagée
  Q4 · le canal     `wa_verified == yes` — ou, à défaut, une preuve d'usage (le lead a répondu)
  Q5 · le manque    pas de site vivant vérifié récemment ; `Q5_site_vivant` ⇒ hors cible

Ce qu'il ne juge pas
--------------------
- **si le métier est dans l'ICP du mois** : c'est le playbook §1.2, et c'est une décision de King ;
- **si la personne dit la vérité sur son rôle** : `authority` est déclaré, pas prouvé ;
- **si le site est vivant** : ça se teste (`SITE-CHECK`), et la date le dit.

Usage
-----
    python3 tools/qa/audit_qualification.py                      # leads/CRM.csv
    python3 tools/qa/audit_qualification.py --strict             # les avertissements bloquent aussi
    python3 tools/qa/audit_qualification.py --engaged            # seulement les fils engagés
    python3 tools/qa/audit_qualification.py --self-test          # 12 cas, aucun fichier requis

Code de sortie : 0 = aucun bloquant, 1 = au moins un. Le vert ne vaut pas qualification (§5 du doc).
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "leads" / "CRM.csv"

# Un fil est « engagé » dès qu'on lui consacre du temps de vente.
ENGAGED = ("qualifying", "demo", "offer", "closing", "delivered")
AUTHORITY_OK = ("proprietaire", "mandate")
AUTHORITY_BAD = ("sans-autorite", "inconnu")
CODES = {
    "Q1_pas_acheteur": "Q1", "Q2_pas_actif": "Q2", "Q3_hors_icp": "Q3",
    "Q4_pas_de_canal": "Q4", "Q5_site_vivant": "Q5", "Q5_fait_non_verifie": "Q5",
}
# Une disqualification est un état final : le code et le stage doivent dire la même chose.
FINAL = ("disqualified", "parked", "lost")


def _v(row: dict, *keys: str) -> str:
    """Première valeur non vide parmi `keys` — le CSV change de casse et d'accent selon les époques."""
    for k in keys:
        val = (row.get(k) or "").strip()
        if val:
            return val
    return ""


def channel_proven(row: dict) -> str:
    """`yes` · `usage` (le lead a répondu ou le message est parti) · `unknown` · `no`."""
    wa = _v(row, "wa_verified").lower()
    if wa == "yes":
        return "yes"
    if (_v(row, "Reply").lower() == "yes" or _v(row, "last_send_state").lower() in ("sent", "lu", "delivered")):
        return "usage"
    if wa in ("no", "non"):
        return "no"
    return "unknown"


def verdict(row: dict) -> tuple[list[str], list[str]]:
    """Rend (fails, warns). Aucune règle ne se contente d'un champ vide : un vide est un « ? »."""
    fails: list[str] = []
    warns: list[str] = []
    stage = _v(row, "stage").lower()
    code = _v(row, "qualification")
    authority = _v(row, "authority").lower()
    engaged = stage in ENGAGED

    # ── cohérence code / stage : un code posé et ignoré est pire qu'une absence de code
    if code in CODES and stage not in FINAL:
        fails.append(f"{code} est posé mais la ligne est en « {stage} » — un motif de "
                     f"disqualification qui ne disqualifie pas est une note, pas un verdict")
    if code == "Q-OK" and engaged:
        if authority not in AUTHORITY_OK:
            fails.append(f"Q-OK déclaré sans autorité d'acheteur (`authority` = "
                         f"{authority or 'vide'}) — Q1 n'est pas prouvée")
    if code == "Q-OK" and not engaged:
        warns.append(f"Q-OK posé hors fil engagé (stage « {stage} ») — à passer en `qualifying` "
                     f"si le message part")

    # ── Q2 · l'actif
    if engaged and not _v(row, "org", "School"):
        fails.append("Q2 : aucune organisation renseignée — il n'y a pas d'actif à équiper")
    if engaged and not _v(row, "city", "City"):
        warns.append("Q2 : aucune ville — le lieu de l'actif n'est pas établi")

    # ── Q1 · l'acheteur (le cas Fogue)
    if engaged:
        if authority in AUTHORITY_BAD:
            fails.append(f"Q1 : `authority` = « {authority} » — on ne vend pas à quelqu'un qui n'a pas "
                         f"l'autorité d'acheter (cas Dr Fogue, 28/10)")
        elif not authority:
            warns.append("Q1 : `authority` vide — le rôle de la personne n'est pas écrit, donc pas "
                         "vérifié. Question à poser : « qui décide de ce qui s'affiche sur le site ? »")
        if not _v(row, "contact_name", "Decision maker"):
            warns.append("Q1 : aucun nom de contact — on ne sait pas à qui on parle")
        if not _v(row, "contact_role"):
            warns.append("Q1 : `contact_role` vide — « un nom dans une case » n'est pas un rôle")

    # ── Q4 · le canal
    if engaged:
        ch = channel_proven(row)
        if ch == "no":
            fails.append("Q4 : numéro testé et absent de WhatsApp — ruling 25/10 : `disqualified`, "
                         "pas de relance, pas d'appel")
        elif ch == "unknown":
            fails.append("Q4 : canal jamais vérifié — ruling 12/10 : sans WhatsApp vérifié, "
                         "le prospect n'entre pas au pipeline")
        elif ch == "usage":
            warns.append("Q4 : `wa_verified` n'est pas `yes` alors que le fil est engagé — la preuve "
                         "est l'usage, le champ doit être régularisé")

    # ── Q5 · le manque
    if _v(row, "site_url") and not _v(row, "site_checked_on"):
        warns.append("Q5 : un `site_url` est enregistré sans date de vérification — on ne sait pas "
                     "s'il est vivant")
    if engaged and code.startswith("Q5_"):
        fails.append(f"Q5 : {code} alors que la ligne est engagée — le manque n'est pas établi")

    return fails, warns


def run(path: pathlib.Path, strict: bool, engaged_only: bool) -> int:
    if not path.exists():
        print(f"✗ {path} introuvable — rien n'a été jugé.")
        return 1
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8-sig")))
    if not rows:
        print(f"✗ {path} est vide — rien n'a été jugé.")
        return 1

    print(f"\nPORTE D'ENTRÉE — {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}  "
          f"({len(rows)} ligne(s))\n")

    n_fail = n_warn = 0
    shown = 0
    engaged_n = 0
    for row in rows:
        fails, warns = verdict(row)
        if not fails and not warns:
            continue
        engaged = _v(row, "stage").lower() in ENGAGED
        if engaged_only and not engaged:
            continue
        for f in fails:
            n_fail += 1
        for w in warns:
            n_warn += 1
        shown += 1
        label = _v(row, "org", "School") or _v(row, "slug") or "(sans nom)"
        stage = _v(row, "stage") or "?"
        if engaged:
            engaged_n += 1
        print(f"{'─' * 78}\n{label} · {_v(row, 'city', 'City') or '?'} · {stage}")
        for f in fails:
            print(f"  ✗ {f}")
        for w in warns:
            print(f"  · {w}")

    blocking = n_fail + (n_warn if strict else 0)
    print(f"{'─' * 78}")
    print(f"{shown} ligne(s) citée(s) dont {engaged_n} fil(s) engagé(s) · "
          f"{n_fail} bloquant(s) · {n_warn} avertissement(s)")
    print(f"→ {'BLOQUÉ' if blocking else 'OK'}"
          f"{' (--strict : les avertissements bloquent)' if strict else ''}")
    print("Rappel : ce script ne juge ni l'ICP du mois, ni la véracité du rôle déclaré, "
          "ni la vie du site.\n")
    return 1 if blocking else 0


# ── les cas de banc : chaque règle a son exemple, et deux « faux positifs » sont testés ────────────
CASES = [
    ("acheteur propriétaire, canal vu, rien à signaler", dict(
        stage="qualifying", authority="proprietaire", contact_name="X", contact_role="gérant",
        org="A", city="Douala", wa_verified="yes"), 0, 0),
    ("Q1 · consultant itinérant (cas Dr Fogue)", dict(
        stage="qualifying", authority="sans-autorite", contact_name="X", contact_role="ophtalmologue",
        org="A", city="Douala", wa_verified="yes"), 1, 0),
    ("Q1 · autorité vide = non vérifiée", dict(
        stage="qualifying", contact_name="X", contact_role="gérant", org="A", city="Douala",
        wa_verified="yes"), 0, 1),
    ("Q4 · jamais vérifié", dict(
        stage="qualifying", authority="proprietaire", contact_name="X", contact_role="gérant",
        org="A", city="Douala"), 1, 0),
    ("Q4 · testé absent de WhatsApp", dict(
        stage="qualifying", authority="proprietaire", contact_name="X", contact_role="gérant",
        org="A", city="Douala", wa_verified="no"), 1, 0),
    ("Q4 · faux positif évité : le fil prouve le canal", dict(
        stage="qualifying", authority="proprietaire", contact_name="X", contact_role="gérant",
        org="A", city="Douala", wa_verified="unknown", Reply="Yes"), 0, 1),
    ("code posé mais stage encore engagé", dict(
        stage="qualifying", authority="proprietaire", contact_name="X", contact_role="gérant",
        org="A", city="Douala", wa_verified="yes", qualification="Q1_pas_acheteur"), 1, 0),
    ("code posé et stage cohérent", dict(
        stage="parked", authority="sans-autorite", contact_name="X", contact_role="ophtalmologue",
        org="A", city="Douala", wa_verified="yes", qualification="Q1_pas_acheteur"), 0, 0),
    ("Q-OK sans autorité", dict(
        stage="qualifying", contact_name="X", contact_role="gérant", org="A", city="Douala",
        wa_verified="yes", qualification="Q-OK"), 1, 1),
    ("Q2 · pas d'organisation", dict(
        stage="qualifying", authority="proprietaire", contact_name="X", contact_role="gérant",
        city="Douala", wa_verified="yes"), 1, 0),
    ("Q5 · site enregistré sans date", dict(
        stage="prospecting", authority="proprietaire", contact_name="X", contact_role="gérant",
        org="A", city="Douala", wa_verified="yes", site_url="https://x.cm"), 0, 1),
    ("ligne froide sans rien : aucun bruit", dict(stage="prospecting", org="A", city="Douala"), 0, 0),
]


def self_test() -> int:
    bad = 0
    print("\nBANC DE LA PORTE D'ENTRÉE\n")
    for label, row, want_f, want_w in CASES:
        f, w = verdict(row)
        ok = len(f) == want_f and len(w) == want_w
        bad += 0 if ok else 1
        print(f"  {'✓' if ok else '✗'} {label}")
        if not ok:
            print(f"     attendu {want_f} bloquant(s) / {want_w} avertissement(s) — "
                  f"obtenu {len(f)} / {len(w)}")
            for x in f + w:
                print(f"       {x}")
    print(f"\n{len(CASES) - bad}/{len(CASES)} cas\n")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="La porte d'entrée : un prospect a-t-il le droit d'être prospecté ?")
    ap.add_argument("csv", nargs="?", default=str(DEFAULT))
    ap.add_argument("--strict", action="store_true", help="les avertissements bloquent aussi")
    ap.add_argument("--engaged", action="store_true", help="ne citer que les fils engagés")
    ap.add_argument("--self-test", action="store_true", help="joue les 12 cas du banc, sans fichier")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    return run(pathlib.Path(args.csv), args.strict, args.engaged)


if __name__ == "__main__":
    sys.exit(main())
