#!/usr/bin/env python3
"""La fiche d'un prospect — ce qu'on sait, le numéro, le message, et ce qui reste à chercher.

    python3 tools/outreach/fiche.py cartes --lot sales/ENVOI-VAGUE-2-2026-10-26.md --limite 5
    python3 tools/outreach/fiche.py cartes --lot ... --limite 5 --out sales/LOT-1-2026-10-27.md
    python3 tools/outreach/fiche.py verifie sales/LOT-1-2026-10-27.md

Pourquoi cet outil existe : à la main, on recopie un numéro de travers (mesure du 26/10 : sept lignes
fausses dans `SWEEP-PORTE-B`, toutes recopiées). Ici, le numéro, le nom affiché, le quartier, le décideur
et le message viennent **du CRM et du lot**, jamais d'une frappe. `verifie` fait le chemin inverse : il
relit la fiche livrée et crie si un numéro de la fiche ne correspond pas à ce nom dans le CRM.

Ce que l'outil ne fait pas : il ne cherche rien sur Google ni sur Facebook (aucun réseau ici), il ne
réécrit pas le message, et il ne décide pas quoi envoyer — c'est `plan_jour.py` pour l'ordre, King pour
le fait manquant.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compose  # noqa: E402
from audit_outreach import words  # noqa: E402  — le même compteur que la porte, pas un mien

RACINE = compose.RACINE
CRM = RACINE / "leads" / "CRM.csv"
MAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
# Ce qu'un message ne peut pas affirmer sans preuve : qu'une chose n'existe pas sur le web.
ABSENCE = re.compile(r"ne (connait|connaît|voit|lit|trouve|sort|rend) pas|n'existe pas|ignore|introuvable|invisible")
# « page » à Douala = page Facebook (ruling King 26/10). Le produit s'appelle « le site », avec un usage.
PAGE_SEULE = re.compile(r"\bpages?\b(?!\s+facebook)")


def numero_intl(n: str) -> str:
    """Le format qu'on tape : +237 6XX XX XX XX. Un numéro qu'on copie de travers ne part pas."""
    d = compose.numero(n)
    return f"+237 {d[0]} {d[1:3]} {d[3:5]} {d[5:7]} {d[7:9]}" if d else ""


def lit_crm_detail(chemin: Path = CRM) -> dict[str, dict]:
    """Tout ce que le CRM sait d'un numéro, y compris l'email caché dans les notes."""
    out: dict[str, dict] = {}
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            n = compose.numero(r.get("wa_number") or r.get("Phone") or "")
            if not n:
                continue
            notes = (r.get("Notes") or "").strip()
            mails = MAIL.findall(notes)
            out.setdefault(n, {
                "ordre": (r.get("School") or "").strip(),
                "affiche": (r.get("profile_name_seen") or "").strip(),
                "ville": (r.get("City") or "").strip(),
                "decideur": (r.get("Decision maker") or r.get("contact_name") or "").strip(),
                "role": (r.get("contact_role") or "").strip(),
                "mail": mails[0] if mails else "",
                "notes": notes,
                "verifie": (r.get("wa_verified") or "").strip(),
                "source": (r.get("source_detail") or "").strip(),
                "slug": (r.get("slug") or "").strip(),
            })
    return out


def verdicts(date: str) -> dict[str, dict]:
    p = RACINE / "leads" / f"VERIF-{date}.json"
    if not p.exists():
        return {}
    return {x["num"]: x for x in json.loads(p.read_text(encoding="utf-8"))}


def cartes(lot: Path, limite: int, date: str) -> list[dict]:
    crm = lit_crm_detail()
    verif = verdicts(date)
    out: list[dict] = []
    for m in compose.parse(lot)[:limite]:
        n = compose.numero(m.phone)
        d = crm.get(n, {})
        out.append({
            "num": n, "intl": numero_intl(n), "label": m.label, "quartier": m.quartier,
            "message": m.body, "mots": len(words(m.body)),
            "affiche": d.get("affiche", ""), "ordre": d.get("ordre", ""),
            "decideur": d.get("decideur", ""), "mail": d.get("mail", ""),
            "verdict": verif.get(n, {}).get("verdict", "PAS-ENVOYÉ"),
            "fact": verif.get(n, {}).get("fact", ""),
            "lot": lot.name,
        })
    return out


def rendu(cs: list[dict], titre: str) -> str:
    out = [f"<!-- {titre} — engendré par tools/outreach/fiche.py ; numéros et messages non retapés -->", ""]
    for i, c in enumerate(cs, 1):
        out += [f"### {i}. {c['label']} — {c['quartier']}",
                "",
                f"**Numéro : `{c['intl']}`** · {c['verdict']} · message de {c['mots']} mots",
                "",
                f"- nom affiché sur WhatsApp : **{c['affiche'] or '—'}**",
                f"- nom au tableau de l'Ordre : {c['ordre'] or '—'}",
                f"- décideur au CRM : {c['decideur'] or '—'}",
                f"- email public : {c['mail'] or '—'}",
                f"- preuve de la porte A : {c['fact'] or '—'}",
                "",
                "```text",
                c["message"],
                "```",
                ""]
    return "\n".join(out)


BADGE = re.compile(r"^###\s*\d+\.\s*(?P<nom>.+?)\s*—\s*.+$", re.M)
TEL = re.compile(r"\*\*Numéro : `\+237\s*(?P<num>[\d ]+)`\*\*")
# Le format du lot : **#3 ③ ISEE — Douala — 656 97 80 43**
ENTETE_LOT = re.compile(r"^\*\*#\d+\s+(?P<nom>.+?)\s+—\s+[^—]+\s+—\s+(?P<tel>[\d ]{9,})\*\*$", re.M)


def verifie(chemin: Path) -> list[str]:
    """Chaque carte de la fiche doit porter le numéro que le CRM associe à ce nom. Sinon, on crie."""
    crm = lit_crm_detail()
    par_nom = {}
    for n, d in crm.items():
        for cle in (d["ordre"], d["affiche"]):
            if cle:
                par_nom.setdefault(compose.fold(cle), n)
    fautes: list[str] = []
    texte = chemin.read_text(encoding="utf-8")
    # Les deux formats sont lus : la carte (### 1. Nom — Ville) et le lot (**#1 Nom — Ville — numéro**).
    # Une fiche sans aucune carte n'est pas « valide » : c'est une fiche vide, et une porte qui ne voit
    # rien ne prouve rien.
    lues = 0
    for m in ENTETE_LOT.finditer(texte):
        lues += 1
        nom, n = m.group("nom").strip(), compose.numero(m.group("tel"))
        attendu = par_nom.get(compose.fold(re.sub(r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*", "", nom)))
        if not attendu:
            fautes.append(f"{nom} : ce nom n'existe dans aucune ligne du CRM")
        elif attendu != n:
            fautes.append(f"{nom} : le lot porte {numero_intl(n)}, le CRM dit {numero_intl(attendu)}")
    blocs = BADGE.split(texte)
    # blocs = [avant, nom1, corps1, nom2, corps2, ...]
    for i in range(1, len(blocs) - 1, 2):
        lues += 1
        nom, corps = blocs[i].strip(), blocs[i + 1]
        m = TEL.search(corps)
        if not m:
            fautes.append(f"{nom} : aucun numéro lisible")
            continue
        n = compose.numero(m.group("num"))
        attendu = par_nom.get(compose.fold(nom))
        if not attendu:
            fautes.append(f"{nom} : ce nom n'existe dans aucune ligne du CRM")
        elif attendu != n:
            fautes.append(f"{nom} : la fiche porte {numero_intl(n)}, le CRM dit {numero_intl(attendu)}")
    if not lues:
        fautes.append("aucune carte lue : ni `### N. Nom — Ville` ni `**#N Nom — Ville — numéro**`")
    return fautes


def controle(texte: str) -> tuple[list[str], list[str], int]:
    """Le contrôle d'UN message réécrit à la main — avant de l'envoyer, pas après.

    La porte `audit_outreach` juge un lot au format `**#N Nom — Ville — numéro**`. Quand King ajoute un
    fait trouvé sur Facebook, il réécrit une phrase dans son téléphone : ce mode lui rend le même verdict
    sur un texte collé, sans lui demander de reconstruire un fichier.
    """
    from audit_outreach import Message, check
    m = Message(label="message réécrit", quartier="", phone="", body=texte.strip(), line=0)
    check(m)
    # Le trou du 26/10 : deux messages affirmaient « Google ne vous voit pas » et Google les voyait.
    # Ce n'est pas une porte — c'est un rappel : une affirmation d'absence exige une capture datée.
    plat = compose.fold(m.body)
    if PAGE_SEULE.search(plat):
        m.warns.append("le mot « page » se lit comme une page Facebook à Douala — dire « le site », "
                       "et lui donner un usage (horaires, adresse, bouton WhatsApp)")
    if ABSENCE.search(plat):
        m.warns.append("affirmation d'absence (« Google ne… », « ignore », « n'existe pas ») : elle exige "
                       "une capture datée — sans elle, le prospect la dément en dix secondes")
    return m.fails, m.warns, len(words(m.body))


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="action", required=True)
    c = sub.add_parser("cartes")
    c.add_argument("--lot", required=True)
    c.add_argument("--limite", type=int, default=5)
    c.add_argument("--date", default="")
    c.add_argument("--titre", default="Cartes du lot")
    c.add_argument("--out", default="")
    v = sub.add_parser("verifie")
    v.add_argument("fiche")
    ct = sub.add_parser("controle")
    ct.add_argument("--fichier", default="", help="sinon : le texte arrive sur l'entrée standard")
    a = ap.parse_args()

    if a.action == "cartes":
        cs = cartes(Path(a.lot), a.limite, a.date or "2026-10-27")
        txt = rendu(cs, a.titre)
        if a.out:
            Path(a.out).write_text(txt, encoding="utf-8")
            print(f"{len(cs)} carte(s) → {a.out}")
        else:
            print(txt)
        return 0

    if a.action == "controle":
        texte = (Path(a.fichier).read_text(encoding="utf-8") if a.fichier else sys.stdin.read())
        fails, warns, n = controle(texte)
        for f in fails:
            print(f"  ⛔ {f}")
        for w in warns:
            print(f"  ⚠ {w}")
        etat = "OK" if not fails else f"{len(fails)} bloquant(s)"
        print(f"{etat} · {n} mot(s) · {texte.count('?')} question(s)")
        return 1 if fails else 0

    fautes = verifie(Path(a.fiche))
    if fautes:
        print("⛔ la fiche ne correspond pas au CRM :\n  " + "\n  ".join(fautes))
        return 1
    print("✓ chaque numéro de la fiche est celui que le CRM associe à ce nom")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
