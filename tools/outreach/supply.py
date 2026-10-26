#!/usr/bin/env python3
"""supply — combien de messages on peut envoyer, et avec quoi on les remplit.

Pourquoi ce fichier existe
--------------------------
Le 26/10, King tranche : « in cold messaging volume counts », 20 à 50 par jour. La recherche lui donne
raison sur le principe **et fixe le plafond** (§1 de `ops/BRAINSTORM-VOLUME-2026-10-26.md`). Reste la
question que personne ne pose : **avec quoi ?**

Le stock du CRM tient 1,9 jour à 40/jour. Écrire plus vite ne sert à rien si l'on n'a rien à écrire :
la contrainte n'est pas la plume, c'est **la liste et le fait**. Ce fichier rend cette contrainte
visible avant l'envoi, au lieu de la découvrir le troisième jour.

Deux commandes, et deux refus :

    python3 tools/outreach/supply.py ingest --in /tmp/annuaire.csv --source annuaire --vu 2026-10-26
        colle une liste (annuaire, page Facebook, passage), normalise les numéros, écarte les doublons
        et écrit un **fichier de transit** — jamais le CRM, qui ne s'écrit que par `leads/build/crm.py`.

    python3 tools/outreach/supply.py plan --volume 20,22,36,0,0,40 --start 2026-10-27
        dit, jour par jour, ce qui est écrit, ce qui manque, combien de profils il faut ouvrir, et
        **refuse** un plan que le stock ne peut pas tenir.

Ce qu'il ne fait pas
--------------------
Il n'invente aucun numéro, ne visite aucune page et n'ouvre aucun WhatsApp. Un numéro collé n'est pas
un numéro vérifié : la porte A reste le geste de King, huit secondes par ligne.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Rendements observés, et **pas** des promesses : ce sont des taux de réponse de courriel froid 2026
# (Gangly, 500 messages ; Instantly, moyenne de plateforme 3,43 %), utilisés ici comme ordres de grandeur
# pour comparer deux plans — jamais comme prévision. Voir §1 du brainstorm pour les sources.
TAUX = {
    "3/3": (0.078, 0.112),   # fait daté sur le prospect : 7,8 % mesuré, 11,2 % au mieux (déclencheur réel)
    "2/3": (0.044, 0.078),   # nom + entreprise + rôle : 4,4 % mesuré
    "1/3": (0.021, 0.044),   # prénom seul à gabarit large : 2,1 à 2,6 %
}
ENTETES = ["School", "City", "Phone", "source", "source_detail", "seen_on", "slug"]


# ── les numéros ─────────────────────────────────────────────────────────────────────────────────

def numero(brut: str) -> str:
    """Neuf chiffres, ou rien. « +237 699 12 34 56 », « 00237699123456 », « 699-12-34-56 » → 699123456.

    Un numéro camerounais mobile tient sur neuf chiffres et commence par 6. Tout le reste est refusé
    plutôt que deviné : un numéro faux coûte un message perdu **et** un signalement.
    """
    d = re.sub(r"\D", "", brut or "")
    for prefixe in ("00237", "237"):
        if d.startswith(prefixe) and len(d) == 9 + len(prefixe):
            d = d[len(prefixe):]
            break
    if len(d) == 11 and d.startswith("237"):
        d = d[3:]
    if len(d) != 9 or not d.startswith("6"):
        return ""
    return d


def joli(n: str) -> str:
    return f"{n[:3]} {n[3:5]} {n[5:7]} {n[7:]}" if len(n) == 9 else n


@dataclass
class Ligne:
    nom: str
    ville: str
    num: str
    source: str
    detail: str
    vu_le: str

    @property
    def slug(self) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", self.nom.lower()).strip("-")
        return f"{base}-{self.num[-4:]}"


# ── lire une liste collée ───────────────────────────────────────────────────────────────────────

ALIAS = {
    "nom": ("school", "nom", "name", "etablissement", "établissement", "cabinet", "entreprise",
            "business", "titre"),
    "tel": ("phone", "tel", "téléphone", "telephone", "numero", "numéro", "wa_number", "mobile",
            "contact", "whatsapp"),
    "ville": ("city", "ville", "quartier", "localite", "localité", "adresse", "address"),
}


def _col(entetes: list[str], quoi: str) -> int | None:
    plies = [re.sub(r"[^a-zéèêàç]", "", (e or "").lower()) for e in entetes]
    for i, e in enumerate(plies):
        if e in ALIAS[quoi]:
            return i
    for i, e in enumerate(plies):     # deuxième passe : inclusion, pour « Téléphone WhatsApp »
        if any(a in e for a in ALIAS[quoi]):
            return i
    return None


def lit_liste(chemin: Path, source: str, vu_le: str) -> tuple[list[Ligne], list[str]]:
    """Lit un CSV/TSV collé, sans supposer l'ordre des colonnes. Rend les lignes et les refus."""
    texte = chemin.read_text(encoding="utf-8-sig")
    sep = "\t" if texte.count("\t") > texte.count(",") else \
          ";" if texte.count(";") > texte.count(",") else ","
    lignes = list(csv.reader(texte.splitlines(), delimiter=sep))
    if not lignes:
        return [], ["fichier vide"]
    entetes = lignes[0]
    i_nom, i_tel, i_ville = _col(entetes, "nom"), _col(entetes, "tel"), _col(entetes, "ville")
    if i_nom is None or i_tel is None:
        return [], [f"colonnes non reconnues : {entetes} — il faut au minimum un nom et un numéro"]
    refus: list[str] = []
    out: list[Ligne] = []
    for n, r in enumerate(lignes[1:], 2):
        if not any(c.strip() for c in r):
            continue
        nom = r[i_nom].strip() if i_nom < len(r) else ""
        tel = r[i_tel].strip() if i_tel < len(r) else ""
        ville = r[i_ville].strip() if i_ville is not None and i_ville < len(r) else ""
        if not nom:
            refus.append(f"ligne {n} : pas de nom")
            continue
        num = numero(tel)
        if not num:
            refus.append(f"ligne {n} : numéro illisible « {tel} »")
            continue
        out.append(Ligne(nom=nom, ville=ville, num=num, source=source, detail=tel, vu_le=vu_le))
    return out, refus


def dedoublonne(nouvelles: list[Ligne], crm: Path) -> tuple[list[Ligne], list[str]]:
    """Écarte ce que le CRM connaît déjà — par numéro, jamais par nom (deux cabinets peuvent partager
    un nom, un numéro ne se partage pas)."""
    connus: dict[str, str] = {}
    if crm.exists():
        with crm.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                n = numero(r.get("wa_number") or r.get("Phone") or "")
                if n:
                    connus[n] = (r.get("School") or "").strip()
    vus: dict[str, str] = {}
    garde: list[Ligne] = []
    refus: list[str] = []
    for l in nouvelles:
        if l.num in connus:
            refus.append(f"{l.nom} — {joli(l.num)} déjà au CRM ({connus[l.num]})")
            continue
        if l.num in vus:
            refus.append(f"{l.nom} — {joli(l.num)} en double dans la liste ({vus[l.num]})")
            continue
        vus[l.num] = l.nom
        garde.append(l)
    return garde, refus


def ecrit_transit(lignes: list[Ligne], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ENTETES)
        w.writeheader()
        for l in lignes:
            w.writerow({"School": l.nom, "City": l.ville, "Phone": joli(l.num), "source": l.source,
                        "source_detail": l.detail, "seen_on": l.vu_le, "slug": l.slug})


# ── le plan ─────────────────────────────────────────────────────────────────────────────────────

def stock() -> dict[str, int]:
    """Ce que le vérificateur sait du stock, porte par porte. Aucune ligne n'est comptée deux fois."""
    import scout
    garde, _ = scout.scout(scout.lit_crm())
    out = {"3/3": 0, "2/3": 0, "1/3": 0}
    for p in garde:
        cle = {3: "3/3", 2: "2/3"}.get(p.portes, "1/3")
        out[cle] += 1
    return out


def plan(volumes: list[int], debut: date, dispo: dict[str, int],
         captures_par_jour: int = 0) -> tuple[str, bool]:
    """Le plan jour par jour, et le refus s'il demande plus de faits qu'il n'en existe.

    Les faits ne se fabriquent pas : un message à 3/3 exige un profil ouvert. Le modèle dit donc
    combien de profils il faut ouvrir chaque jour, et si le plan tient avec ce qu'on a.
    """
    lignes = ["| Jour | Envois | Dont 3/3 | Dont 2/3 | Dont 1/3 | Réponses attendues | Reste |",
              "|---|---|---|---|---|---|---|"]
    reste = dict(dispo)
    total = sum(reste.values())
    manque = 0
    for i, v in enumerate(volumes):
        if v <= 0:
            lignes.append(f"| {debut + timedelta(days=i)} | — | — | — | — | — | {total} |")
            continue
        pris = {"3/3": 0, "2/3": 0, "1/3": 0}
        for cle in ("3/3", "2/3", "1/3"):     # les preuves fortes partent d'abord
            prendre = min(v - sum(pris.values()), reste[cle])
            pris[cle] += prendre
            reste[cle] -= prendre
        total -= sum(pris.values())
        trou = v - sum(pris.values())
        manque += trou
        bas = sum(n * TAUX[c][0] for c, n in pris.items())
        haut = sum(n * TAUX[c][1] for c, n in pris.items())
        lignes.append(f"| {debut + timedelta(days=i)} | {v}{' (+' + str(trou) + ' à trouver)' if trou else ''} "
                      f"| {pris['3/3']} | {pris['2/3']} | {pris['1/3']} | {bas:.1f} – {haut:.1f} | {max(total, 0)} |")
        if captures_par_jour:
            reste["2/3"] += captures_par_jour
            total += captures_par_jour
    ok = manque == 0
    verdict = (f"Plan tenable : {sum(v for v in volumes if v > 0)} envois, "
               f"{sum(w for w in [total] if w >= 0)} lignes encore en réserve après le dernier jour."
               if ok else
               f"Plan **impossible en l'état** : {manque} message(s) sans ligne au {debut}. "
               f"Il manque {manque} numéros, ou {manque} profils ouverts à la main.")
    return "\n".join(lignes + [""] + [verdict]), ok


def rendu(volumes: list[int], debut: date, dispo: dict[str, int], captures: int) -> str:
    corps, _ = plan(volumes, debut, dispo, captures)
    taux = sum(TAUX[c][0] * n for c, n in dispo.items()) / max(sum(dispo.values()), 1)
    return "\n".join([
        f"Stock jamais contacté : **{sum(dispo.values())}** lignes "
        f"({dispo['3/3']} à 3/3 · {dispo['2/3']} à 2/3 · {dispo['1/3']} à 1/3).",
        f"Rendement moyen du stock, aux taux de référence : **{taux * 100:.1f} %** de réponses.",
        "",
        corps,
        "",
        "**Comment lire la colonne « réponses attendues »** : ce sont des taux de courriel froid 2026",
        "appliqués à nos propres nombres. Ce n'est pas une prévision — c'est ce qui permet de comparer",
        "« 40 messages à 1/3 » (0,8–1,8 réponse) et « 10 messages à 3/3 » (0,8–1,1 réponse) avant",
        "d'écrire quoi que ce soit. Sur WhatsApp le taux est plus haut et l'échantillon plus petit :",
        "le chiffre qui décide reste **répondu < 48 h**, mesuré, pas estimé.",
    ])


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="action", required=True)

    i = sub.add_parser("ingest", help="coller une liste et la valider")
    i.add_argument("--in", dest="entree", required=True)
    i.add_argument("--out", default="")
    i.add_argument("--source", default="annuaire")
    i.add_argument("--vu", default=date.today().isoformat())
    i.add_argument("--crm", default=str(RACINE / "leads/CRM.csv"))

    p = sub.add_parser("plan", help="ce que la cadence demande, et si le stock le tient")
    p.add_argument("--volume", default="20,22,36")
    p.add_argument("--start", default=date.today().isoformat())
    p.add_argument("--captures", type=int, default=0,
                   help="profils ouverts par jour (chacun transforme une 2/3 en 3/3)")
    p.add_argument("--crm", default=str(RACINE / "leads/CRM.csv"))

    a = ap.parse_args()
    if a.action == "ingest":
        lignes, refus = lit_liste(Path(a.entree), a.source, a.vu)
        garde, doubl = dedoublonne(lignes, Path(a.crm))
        out = Path(a.out) if a.out else RACINE / f"leads/STAGING-{a.vu}.csv"
        if garde:
            ecrit_transit(garde, out)
        print(f"{len(garde)} numéro(s) accepté(s) → {out}")
        for motif in refus + doubl:
            print(f"  ✗ {motif}")
        return 0 if garde else 1

    dispo = stock()
    volumes = [int(x) for x in a.volume.split(",") if x.strip()]
    print(rendu(volumes, date.fromisoformat(a.start), dispo, a.captures))
    _, ok = plan(volumes, date.fromisoformat(a.start), dispo, a.captures)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
