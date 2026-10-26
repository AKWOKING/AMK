#!/usr/bin/env python3
"""scout — trouver les pistes, puis les vérifier, avant d'écrire une seule ligne.

Pourquoi ce fichier existe
--------------------------
Le 26/10, King : « now let's begin outreach, lead scout, lead verifier, then personalized outreach
message, web design if the customer says yes ». Le dépôt avait les règles (`RESEARCH-STANDARD` §8b,
trois portes) et aucun outil : la sélection se faisait à la main, et **elle oubliait des lignes
entières**. Ce matin, 17 opticiens dont le numéro avait été vu sur WhatsApp le 25/10 attendaient,
jamais contactés, pendant qu'on écrivait à d'autres.

Deux commandes, deux fichiers, un seul principe : **on n'invente rien**.

  scout   lit le CRM, garde les lignes jamais touchées et joignables, écrit `leads/SCOUT-<date>.md`
          avec la raison de chaque exclusion. Il ne classe pas par opinion : il trie par ce que la
          ligne prouve.

  verify  applique les trois portes du §8b et rend un verdict par piste :
            A · joignabilité  — le numéro joint WhatsApp, le profil a été VU (capture datée)
            B · intention numérique — un signe daté que le cabinet agit en ligne (§8b porte B)
            C · acheteur — un décideur est nommé, et ce n'est pas un siège
          3 portes = on écrit · 2 portes = King tranche (par défaut : on n'écrit pas) · 1 = jamais.

Ce qu'il ne fait pas — et qui reste humain
------------------------------------------
Il ne visite **aucun** site et n'appelle **aucun** numéro : cet environnement n'a pas de réseau vers
les domaines, et un outil qui prétendrait vérifier mentirait. La porte A se lit dans la capture que
King a faite (`sales/PORTE-A-2026-10-25.md`) ; la porte B se lit dans la même capture, parce qu'un
profil WhatsApp Business avec catalogue et horaires **est** un signe daté d'activité numérique.

Usage
-----
    python3 tools/outreach/scout.py scout  --date 2026-10-26
    python3 tools/outreach/scout.py verify --date 2026-10-26
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
PORTE_A = RACINE / "sales/PORTE-A-2026-10-25.md"
CRM = RACINE / "leads/CRM.csv"
NEUF = re.compile(r"\D")


# ── les données ─────────────────────────────────────────────────────────────────────────────────

@dataclass
class Piste:
    slug: str
    nom: str
    ville: str
    numero: str
    profil: str
    contact: str
    stage: str
    contacte: str
    source: str
    detail: str
    notes: str
    # porte A, lue dans la capture datée
    capture: str = ""        # ✅ · ⚠️ · ⛔ · ""
    vu: str = ""             # ce que montre l'écran, mot pour mot
    # portes B et C
    intention: str = "inconnu"
    acheteur: str = "inconnu"

    @property
    def porte_a(self) -> str:
        if not self.numero or len(NEUF.sub("", self.numero)) != 9:
            return "fail"
        if self.capture == "⛔":
            return "fail"
        if self.capture == "✅" and self.profil:
            return "pass"
        return "ambigu"

    @property
    def porte_b(self) -> str:
        return self.intention

    @property
    def porte_c(self) -> str:
        return self.acheteur

    @property
    def portes(self) -> int:
        return sum(1 for p in (self.porte_a, self.porte_b, self.porte_c) if p == "pass")

    @property
    def verdict(self) -> str:
        if self.porte_a == "fail":
            return "JAMAIS"
        if self.portes == 3:
            return "ENVOYER"
        if self.portes == 2:
            return "KING-TRANCHE"
        return "PAS-ENVOYÉ"


def _lignes_tableau(texte: str) -> list[list[str]]:
    """Les tableaux markdown du document, cellules nettoyées. Le document est la source datée."""
    out = []
    for ligne in texte.splitlines():
        s = ligne.strip()
        if not s.startswith("|") or set(s) <= set("|-: "):
            continue
        cellules = [c.strip().strip("*").strip() for c in s.strip("|").split("|")]
        out.append(cellules)
    return out


def lit_porte_a(chemin: Path = PORTE_A) -> dict[str, dict]:
    """Numéro (chiffres) → ce que la capture du 25/10 montre. Le seul endroit où A et B sont prouvés."""
    if not chemin.exists():
        return {}
    vu: dict[str, dict] = {}
    for c in _lignes_tableau(chemin.read_text(encoding="utf-8")):
        if len(c) < 4:
            continue
        numero = next((x for x in c[:4] if len(NEUF.sub("", x)) == 9), "")
        if not numero:
            continue
        etat = next((x for x in c[:5] if x in ("✅", "⚠️", "⛔")), "")
        desc = c[4] if len(c) > 4 else ""
        vu[NEUF.sub("", numero)] = {"nom": c[1], "etat": etat, "vu": desc}
    return vu


def lit_crm(chemin: Path = CRM) -> list[Piste]:
    capture = lit_porte_a()
    out: list[Piste] = []
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            g = lambda k: (r.get(k) or "").strip()  # noqa: E731
            numero = g("wa_number") or g("Phone")
            c = capture.get(NEUF.sub("", numero), {})
            p = Piste(slug=g("slug"), nom=g("School"), ville=g("City"), numero=numero,
                      profil=g("profile_name_seen"), contact=g("contact_name") or g("Decision maker"),
                      stage=g("stage"), contacte=g("Contacted"), source=g("source"),
                      detail=g("source_detail"), notes=g("Notes"),
                      capture=c.get("etat", ""), vu=c.get("vu", ""))
            # B · un profil Business avec catalogue ET horaires est un signe daté (25/10).
            p.intention = "pass" if re.search(r"business", p.vu, re.I) else "inconnu"
            # C · un titulaire nommé, pas un siège. « Sarl » seul ne dit rien du décideur.
            siege = re.search(r"board|siège|siege|groupe|franchise|holding", p.notes, re.I)
            p.acheteur = "pass" if (p.contact and not siege) else "inconnu"
            out.append(p)
    return out


# ── scout ───────────────────────────────────────────────────────────────────────────────────────

def exclue(p: Piste) -> str:
    """Pourquoi une ligne ne peut pas recevoir de message aujourd'hui. Vide = elle peut."""
    if p.stage in ("disqualified",):
        return "disqualifiée au CRM"
    if p.stage in ("lost",):
        return "perdue (refus ou silence clos)"
    if p.stage in ("demo", "closing"):
        return "déjà en négociation : on n'ajoute pas un message froid"
    if p.contacte.lower().startswith("y"):
        return "déjà contactée"
    if len(NEUF.sub("", p.numero)) != 9:
        return "aucun numéro à neuf chiffres"
    if re.search(r"\bnon merci\b|refus", p.notes, re.I):
        return "refus écrit — on ne recontacte jamais"
    return ""


def scout(pistes: list[Piste]) -> tuple[list[Piste], list[tuple[Piste, str]]]:
    garde, exclues = [], []
    for p in pistes:
        r = exclue(p)
        (exclues.append((p, r)) if r else garde.append(p))
    # L'ordre est un ordre de preuve, pas de préférence : ce qui est vérifié d'abord.
    garde.sort(key=lambda p: (-p.portes, p.nom.lower()))
    return garde, exclues


def rendu_scout(garde: list[Piste], exclues: list[tuple[Piste, str]], date: str) -> str:
    par_verdict: dict[str, int] = {}
    for p in garde:
        par_verdict[p.verdict] = par_verdict.get(p.verdict, 0) + 1
    lignes = [
        f"# SCOUT — {date}",
        "",
        "> Généré par `tools/outreach/scout.py scout` depuis `leads/CRM.csv` (lecture seule).",
        "> Il ne visite aucun site, n'appelle aucun numéro : il lit ce que King a déjà vu.",
        "",
        f"**{len(garde)} pistes joignables · {len(exclues)} exclues**",
        "",
        "| Verdict | Combien |",
        "|---|---|",
    ]
    for v in ("ENVOYER", "KING-TRANCHE", "PAS-ENVOYÉ", "JAMAIS"):
        if par_verdict.get(v):
            lignes.append(f"| {v} | {par_verdict[v]} |")
    lignes += ["", "## 1 · Les pistes, dans l'ordre de la preuve", "",
               "| # | Établissement | Numéro | Profil vu le 25/10 | Portes | Verdict | Source |",
               "|---|---|---|---|---|---|---|"]
    for i, p in enumerate(garde, 1):
        lignes.append(f"| {i} | {p.nom} | {p.numero} | {p.profil or '—'} | {p.portes}/3 | "
                      f"**{p.verdict}** | {p.detail or p.source} |")
    lignes += ["", "## 2 · Les exclusions, et leur raison", "",
               "| Établissement | Raison |", "|---|---|"]
    compte: dict[str, int] = {}
    for p, r in exclues:
        compte[r] = compte.get(r, 0) + 1
    for r, n in sorted(compte.items(), key=lambda kv: -kv[1]):
        lignes.append(f"| {n} ligne(s) | {r} |")
    lignes += ["", "## 3 · Ce que le scout ne sait pas", "",
               "Il ne sait pas si un numéro **joint WhatsApp** : c'est la capture du 25/10, et ce qui "
               "n'y est pas reste inconnu (jamais « mort » par défaut). Il ne sait pas si un cabinet "
               "a un site : `Aucun site vérifié` veut dire **non vérifié**, pas « pas de site ».",
               ""]
    return "\n".join(lignes)


# ── verify ─────────────────────────────────────────────────────────────────────────────────────

def contradictions(pistes: list[Piste]) -> list[str]:
    """Les cabinets déjà écrits dans un lot, et que le vérificateur ne classe pas 3/3.

    C'est la seule chose que cet outil peut dire contre un document déjà signé — et il doit la dire :
    deux artefacts du dépôt qui se contredisent valent mieux qu'un seul qui se trompe en silence.
    """
    sys.path.insert(0, str(RACINE / "tools/qa"))
    from audit_outreach import parse

    ecrits: dict[str, str] = {}
    for doc in sorted((RACINE / "sales").glob("ENVOI-*.md")):
        if not doc.exists():
            continue
        for m in parse(doc):
            ecrits[NEUF.sub("", m.phone)] = f"{doc.name} — « {m.label} »"
    out = []
    for p in pistes:
        n = NEUF.sub("", p.numero)
        if n in ecrits and p.verdict != "ENVOYER":
            out.append(f"**{p.nom}** ({p.numero}) figure dans `{ecrits[n]}` mais le vérificateur le "
                       f"classe **{p.verdict}** ({p.portes}/3) : {p.porte_a=} {p.porte_b=} {p.porte_c=}"
                       .replace("p.porte_a=", "A ").replace("p.porte_b=", "· B ")
                       .replace("p.porte_c=", "· C "))
    return out


def rendu_verif(pistes: list[Piste], date: str) -> str:
    groupes = {"ENVOYER": [], "KING-TRANCHE": [], "PAS-ENVOYÉ": [], "JAMAIS": []}
    for p in pistes:
        groupes[p.verdict].append(p)
    lignes = [
        f"# VÉRIFICATION DES PORTES — {date}",
        "",
        "> Généré par `tools/outreach/scout.py verify`. Les trois portes du §8b, appliquées à ce que",
        "> le dépôt prouve — pas à ce qu'on suppose.",
        "",
        "```text",
        "A · joignabilité        le numéro joint WhatsApp, le profil a été VU et porte un nom d'établissement",
        "B · intention numérique un signe DATÉ d'activité en ligne (profil Business, site vivant, page active)",
        "C · acheteur            un décideur est nommé, et ce n'est pas un siège",
        "3 portes → on écrit · 2 → King tranche (par défaut on n'écrit pas) · 1 → jamais",
        "```",
        "",
    ]
    titres = {
        "ENVOYER": "## 1 · Les 3/3 — le message peut partir",
        "KING-TRANCHE": "## 2 · Les 2/3 — une porte manque, et voici laquelle",
        "PAS-ENVOYÉ": "## 3 · Une seule porte — on n'écrit pas",
        "JAMAIS": "## 4 · Aucune porte — mort, disqualifié, ou numéro invalide",
    }
    for cle in ("ENVOYER", "KING-TRANCHE", "PAS-ENVOYÉ", "JAMAIS"):
        g = groupes[cle]
        if not g:
            continue
        lignes += [titres[cle], ""]
        if cle == "ENVOYER":
            lignes += ["| # | Établissement | Numéro | Le fait à écrire (daté) |", "|---|---|---|---|"]
            for i, p in enumerate(g, 1):
                fait = p.vu or f"profil « {p.profil} » vu le 25/10"
                lignes.append(f"| {i} | **{p.nom}** | {p.numero} | {fait} |")
        elif cle == "KING-TRANCHE":
            lignes += ["| Établissement | Numéro | Ce qui manque | Comment le fermer |",
                       "|---|---|---|---|"]
            for p in g:
                manque = "la porte B : aucune preuve datée d'activité en ligne"
                remede = "une capture (page Facebook, site, catalogue) ou le profil Business"
                if p.porte_b == "pass" and p.porte_c != "pass":
                    manque, remede = "la porte C : aucun décideur nommé", "le nom du titulaire (Ordre, page)"
                lignes.append(f"| {p.nom} | {p.numero} | {manque} | {remede} |")
        else:
            lignes += ["| Établissement | Numéro | Ce qu'on a vu |", "|---|---|---|"]
            for p in g:
                lignes.append(f"| {p.nom} | {p.numero or '—'} | {p.vu or p.capture or 'numéro invalide'} |")
        lignes.append("")
    conflits = contradictions(pistes)
    if conflits:
        lignes += ["## 5 · Les contradictions avec les lots déjà écrits", ""]
        lignes += [f"- {c}" for c in conflits]
        lignes += [""]
    lignes += [
        "## 6 · La règle de sortie",
        "",
        "Une piste à 2/3 **ne part pas par défaut** : c'est King qui tranche, et s'il tranche pour "
        "l'envoi, il l'écrit ici avec sa date. Une piste dont le profil n'a **pas** été vu n'est pas "
        "« morte » : elle est **inconnue**, et le ruling du 25/10 interdit le repli (ni SMS, ni appel).",
        "",
    ]
    return "\n".join(lignes)


def main() -> int:
    global PORTE_A
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["scout", "verify"])
    ap.add_argument("--date", default="")
    ap.add_argument("--crm", default=str(CRM))
    ap.add_argument("--porte-a", default=str(PORTE_A))
    args = ap.parse_args()

    PORTE_A = Path(args.porte_a)
    date = args.date or "2026-10-26"
    pistes = lit_crm(Path(args.crm))
    garde, exclues = scout(pistes)
    if args.action == "scout":
        chemin = RACINE / f"leads/SCOUT-{date}.md"
        chemin.write_text(rendu_scout(garde, exclues, date), encoding="utf-8")
        print(f"{len(garde)} pistes · {len(exclues)} exclues → {chemin.relative_to(RACINE)}")
        return 0
    chemin = RACINE / f"leads/VERIF-{date}.md"
    chemin.write_text(rendu_verif(garde, date), encoding="utf-8")
    envoi = sum(1 for p in garde if p.verdict == "ENVOYER")
    tranche = sum(1 for p in garde if p.verdict == "KING-TRANCHE")
    print(f"{envoi} ENVOYER · {tranche} KING-TRANCHE → {chemin.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
