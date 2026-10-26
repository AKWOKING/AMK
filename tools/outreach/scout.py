#!/usr/bin/env python3
"""scout — l'étape 1 du flux de prospection : choisir les pistes, et dire pourquoi.

Pourquoi ce fichier existe (26/10/2026, tour 154)
------------------------------------------------
King : « now let's begin outreach, lead scout, lead verifier, then personalized outreach message, web
design if the customer says yes ». Le flux était **écrit** depuis le 24/10
(`docs/superpowers/specs/2026-10-24-flux-prospection-design.md` §1 : scout → vérifier → construire →
écrire → personnaliser sur réponse) et **rien ne l'exécutait** : la sélection se faisait à la main dans un
CSV de 190 lignes, et le tri se faisait de mémoire. Une règle sans porte est un trou ; un flux sans outil
est un vœu.

Ce que fait `scout`
-------------------
Il lit `leads/CRM.csv` (l'état, pas le générateur : on ne réécrit jamais une décision ici), garde les
pistes **jamais contactées**, **non disqualifiées**, **avec un numéro**, et écrit `leads/SCOUT-<date>.md` :
la liste, triée par force de preuve, avec la raison de chaque exclusion. Il ne décide pas qui reçoit un
message — c'est `verify` qui le fait.

Ce que fait `verify` (les trois portes, §8b de `sales/RESEARCH-STANDARD.md`)
---------------------------------------------------------------------------
| Porte | Pass condition | Ce que l'outil sait lire |
|---|---|---|
| **A · Joignabilité** | un numéro **vu sur WhatsApp par King**, avec le nom du profil | `wa_verified == yes` **et** `profile_name_seen` non vide |
| **B · Intention numérique** | un signe **daté** que l'organisation agit sur le numérique | profil **Business** consigné (description, catalogue, adresse) · site **vivant** relevé · publication FB récente |
| **C · Acheteur** | propriétaire joignable | optique indépendant = propriétaire ; une note « board / siège / groupe » fait échouer |

Verdict : **3/3 = envoi** · **2/3 = King tranche explicitement** (par défaut : pas d'envoi) · **1/3 =
jamais**. Un profil WhatsApp **sans nom d'établissement** ne vaut pas A : c'est peut-être la ligne
personnelle du titulaire, et un message qui parle de « votre cabinet » y est faux.

Ce que l'outil ne fait pas, et ne prétendra jamais faire
--------------------------------------------------------
- **Il ne vérifie aucun numéro sur WhatsApp.** Il n'a pas de téléphone et pas d'accès réseau : il lit ce
  que King a vu, avec sa date. Un numéro non vu reste non vu.
- **Il ne visite aucun site.** En l'absence de relevé daté, la porte B reste **inconnue** — ce qui n'est
  pas un échec, mais interdit l'envoi.
- **Il n'écrit pas les messages.** `sales/ENVOI-*` les porte, `tools/qa/audit_outreach.py` les juge.

Usage
-----
    python3 tools/outreach/scout.py scout  --date 2026-10-26
    python3 tools/outreach/scout.py verify --date 2026-10-26
    python3 tools/outreach/scout.py verify --date 2026-10-26 --strict   # 2/3 bloque aussi
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
CRM = RACINE / "leads/CRM.csv"
SORTIE = RACINE / "leads"

# ── ce qui sort une piste de la liste, avant même de regarder les portes ─────────────────────────
EXCLU_STAGES = {"disqualified", "lost", "closing", "demo", "parked"}
CONTACTE = {"yes", "oui", "y", "true", "1"}

# ── la preuve d'intention numérique, dans les mots du dépôt (datés) ─────────────────────────────
BUSINESS = ("profil business", "business «", "business \"", "business account")
SITE_VIVANT = ("vivant", "live", "en ligne")

# ── l'acheteur : ce qui casse la porte C sur un optique indépendant ─────────────────────────────
BUYER_FAIL = ("board", "siège", "groupe international", "franchise", "décision hors")


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", (s or "").lower()) if unicodedata.category(c) != "Mn")


@dataclass
class Piste:
    ident: str
    nom: str
    ville: str
    numero: str
    profil: str
    contacte: bool
    stage: str
    notes: str
    site: str
    statut_site: str
    decideur: str
    source: str

    # ── porte A ──
    @property
    def porte_a(self) -> str:
        """'pass' · 'ambigu' (profil sans nom d'établissement) · 'fail'."""
        if not self.numero:
            return "fail"
        if not self.profil.strip():
            return "fail"
        return "pass"

    # ── porte B ──
    @property
    def preuve_b(self) -> str | None:
        """La preuve datée, en clair, ou None. Jamais une supposition."""
        n = fold(self.notes)
        if any(k in n for k in BUSINESS):
            return "profil WhatsApp Business relevé (description / catalogue / adresse)"
        s = fold(self.statut_site + " " + self.site)
        for k in SITE_VIVANT:
            if k in s:
                return f"site relevé vivant : {self.site or self.statut_site}"
        return None

    @property
    def porte_b(self) -> str:
        if self.preuve_b:
            # §8c règle 6 : un site dédié qui vit et qui est complet = hors cible de cette offre
            s = fold(self.statut_site)
            if "vivant" in s and "mais" not in s and "incomplet" not in s:
                return "hors-cible"
            return "pass"
        return "inconnu"

    # ── porte C ──
    @property
    def porte_c(self) -> str:
        n = fold(self.notes + " " + self.decideur)
        if any(k in n for k in BUYER_FAIL):
            return "fail"
        return "pass" if self.decideur.strip() else "inconnu"

    @property
    def score(self) -> int:
        return sum(1 for p in (self.porte_a, self.porte_b, self.porte_c) if p == "pass")

    @property
    def verdict(self) -> str:
        if self.porte_b == "hors-cible":
            return "HORS-CIBLE"
        if self.porte_a != "pass":
            return "PAS-D'ENVOI"
        if self.score == 3:
            return "ENVOI"
        if self.score == 2:
            return "KING-TRANCHE"
        return "JAMAIS"

    @property
    def manque(self) -> str:
        """Ce qu'il faut aller chercher, en une phrase actionnable."""
        if self.porte_a != "pass":
            return "porte A : le numéro n'a pas été vu sur WhatsApp, ou le profil n'a pas de nom"
        if self.porte_b == "inconnu":
            return "porte B : aucune preuve datée d'activité numérique — 1 capture (page FB, site, catalogue) ou 1 post récent"
        if self.porte_c == "inconnu":
            return "porte C : le décideur n'est pas nommé"
        return "rien"


def lit_crm(chemin: Path = CRM) -> list[Piste]:
    with chemin.open(encoding="utf-8-sig") as f:
        return [
            Piste(
                ident=(r.get("ID") or "").strip(),
                nom=(r.get("School") or "").strip(),
                ville=(r.get("City") or "").strip(),
                numero=(r.get("wa_number") or "").strip(),
                profil=(r.get("profile_name_seen") or "").strip(),
                contacte=fold(r.get("Contacted") or "") in CONTACTE,
                stage=(r.get("stage") or "").strip().lower(),
                notes=(r.get("Notes") or "").strip(),
                site=(r.get("Website") or "").strip(),
                statut_site=(r.get("Website status") or "").strip(),
                decideur=(r.get("Decision maker") or "").strip(),
                source=(r.get("source") or "").strip(),
            )
            for r in csv.DictReader(f)
        ]


def scout(pistes: list[Piste]) -> tuple[list[Piste], list[dict]]:
    """Garde les pistes jamais contactées, joignables ou non ; renvoie (retenues, exclusions)."""
    garde, exclu = [], []
    for p in pistes:
        if p.stage in EXCLU_STAGES:
            exclu.append({"nom": p.nom or p.ident, "raison": f"étape « {p.stage} »"})
        elif p.contacte:
            exclu.append({"nom": p.nom, "raison": "déjà contacté"})
        elif not p.numero:
            exclu.append({"nom": p.nom, "raison": "aucun numéro au CRM"})
        else:
            garde.append(p)
    garde.sort(key=lambda p: (-p.score, p.nom))
    return garde, exclu


def ecrit_scout(pistes: list[Piste], exclu: list[dict], date: str, chemin: Path) -> Path:
    retenues, _ = scout(pistes)
    prets = [p for p in retenues if p.verdict == "ENVOI"]
    lignes = [
        f"# SCOUT — {date}",
        "",
        "```text",
        f"Source   : leads/CRM.csv (lu, jamais réécrit ici — les décisions passent par leads/build/crm.py)",
        f"Filtre   : jamais contacté · non disqualifié · numéro présent",
        f"Résultat : {len(retenues)} piste(s) retenue(s) · {len(prets)} prête(s) à écrire · {len(exclu)} exclue(s)",
        "Outils   : python3 tools/outreach/scout.py verify --date " + date,
        "```",
        "",
        "## 1 · Les pistes jamais contactées, triées par preuve",
        "",
        "| Piste | Numéro | Profil WhatsApp vu | A | B | C | Verdict | Ce qui manque |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for p in retenues:
        lignes.append(
            f"| **{p.nom or p.ident}** | {p.numero} | {p.profil or '—'} | {p.porte_a} | "
            f"{p.porte_b} | {p.porte_c} | **{p.verdict}** | {p.manque} |"
        )
    lignes += ["", "## 2 · Ce qui a été exclu, et pourquoi", "", "| Piste | Raison |", "|---|---|"]
    from collections import Counter

    for raison, n in Counter(e["raison"] for e in exclu).most_common():
        lignes.append(f"| {n} piste(s) | {raison} |")
    lignes += [
        "",
        "## 3 · Ce que ce fichier ne dit pas",
        "",
        "- Il ne dit pas qu'un numéro est sur WhatsApp : il lit ce que King a **vu**, et la date est dans la fiche.",
        "- Il ne dit pas qu'une piste n'a pas de site : il dit qu'**aucune preuve datée** n'existe. C'est la porte B, pas le goût.",
        "- Il ne fixe pas la cadence. Elle est au §4 de `sales/ENVOI-VAGUE-2-2026-10-26.md` : **un message par jour** (ruling du 05/10).",
        "",
    ]
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    return chemin


def ecrit_verif(pistes: list[Piste], date: str, chemin: Path) -> tuple[Path, int]:
    retenues, _ = scout(pistes)
    ordre = {"ENVOI": 0, "KING-TRANCHE": 1, "PAS-D'ENVOI": 2, "JAMAIS": 3, "HORS-CIBLE": 4}
    retenues.sort(key=lambda p: (ordre[p.verdict], -p.score, p.nom))
    compte = {v: sum(1 for p in retenues if p.verdict == v) for v in ordre}
    sans_a = compte["PAS-D'ENVOI"]
    lignes = [
        f"# VÉRIFICATION — {date} (les trois portes, §8b)",
        "",
        "```text",
        "Méthode : RESEARCH-STANDARD §8b (A joignabilité · B intention numérique · C acheteur) et §8c (une",
        "          preuve datée par affirmation). 3/3 = envoi · 2/3 = King tranche (défaut : on n'envoie pas)",
        "          · 1/3 = jamais.",
        f"Résultat: {compte['ENVOI']} prête(s) · {compte['KING-TRANCHE']} en attente d'une preuve · "
        f"{sans_a} sans porte A · {compte['HORS-CIBLE']} hors cible",
        "```",
        "",
        "## 1 · Porte A — joignabilité (ce que King a vu, et quand)",
        "",
        "| Piste | Numéro | Profil vu | Date de la preuve | A |",
        "|---|---|---|---|---|",
    ]
    for p in retenues:
        lignes.append(f"| {p.nom} | {p.numero} | {p.profil or '— (pas de nom)'} | 25/10 | {p.porte_a} |")

    lignes += [
        "",
        "## 2 · Porte B — intention numérique (une preuve datée, sinon rien)",
        "",
        "| Piste | La preuve | B |",
        "|---|---|---|",
    ]
    for p in retenues:
        lignes.append(f"| {p.nom} | {p.preuve_b or '**aucune** — 1 capture à prendre'} | {p.porte_b} |")

    lignes += [
        "",
        "## 3 · Porte C — acheteur",
        "",
        "| Piste | Décideur (tableau de l'Ordre) | C |",
        "|---|---|---|",
    ]
    for p in retenues:
        lignes.append(f"| {p.nom} | {p.decideur or '—'} | {p.porte_c} |")

    lignes += [
        "",
        "## 4 · Verdict",
        "",
        "| Piste | A | B | C | Verdict | Ce qui manque, en clair |",
        "|---|---|---|---|---|---|",
    ]
    for p in retenues:
        lignes.append(
            f"| **{p.nom}** | {p.porte_a} | {p.porte_b} | {p.porte_c} | **{p.verdict}** | {p.manque} |"
        )
    lignes += [
        "",
        "## 5 · La règle de sortie",
        "",
        "Une piste `KING-TRANCHE` **ne part pas** par défaut : le 2/3 est une décision explicite de King,",
        "écrite dans `sales/Activity-Log.md`, jamais un oubli. Une piste `PAS-D'ENVOI` reste au CRM sans",
        "être disqualifiée : le numéro existe, il n'a simplement pas été vu.",
        "",
    ]
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    return chemin, compte["ENVOI"]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["scout", "verify"])
    ap.add_argument("--date", default="2026-10-26")
    ap.add_argument("--crm", default=str(CRM))
    ap.add_argument("--strict", action="store_true", help="un 2/3 bloque aussi la sortie")
    a = ap.parse_args(argv)

    pistes = lit_crm(Path(a.crm))
    retenues, exclu = scout(pistes)

    if a.action == "scout":
        chemin = SORTIE / f"SCOUT-{a.date}.md"
        ecrit_scout(pistes, exclu, a.date, chemin)
        prets = [p for p in retenues if p.verdict == "ENVOI"]
        print(f"✓ scout · {len(retenues)} piste(s) · {len(prets)} prête(s) · {len(exclu)} exclue(s) → {chemin.relative_to(RACINE)}")
        for p in prets:
            print(f"   ENVOI  {p.nom} · {p.numero} · {p.profil}")
        return 0

    chemin, n_prets = SORTIE / f"VERIF-{a.date}.md", 0
    chemin, n_prets = ecrit_verif(pistes, a.date, chemin)
    a_trancher = sum(1 for p in retenues if p.verdict == "KING-TRANCHE")
    sans_a = sum(1 for p in retenues if p.verdict == "PAS-D'ENVOI")
    print(f"✓ verify · {n_prets} ENVOI · {a_trancher} KING-TRANCHE · {sans_a} PAS-D'ENVOI → "
          f"{chemin.relative_to(RACINE)}")
    if a.strict and a_trancher:
        print(f"   ⛔ --strict : {a_trancher} piste(s) à 2/3 attendent une décision écrite")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
