#!/usr/bin/env python3
"""verify — les trois portes du §8b, appliquées à ce que le CRM prouve, et rien de plus.

Pourquoi ce fichier existe
--------------------------
Le 26/10, un lot de 49 messages écrits par la fabrique passait la porte du texte avec **0 bloquant** —
et contenait **neuf cabinets à 2/3 et un à 1/3**, dont sa première ligne. La leçon n'est pas « écrire
mieux » : c'est que **deux mesures différentes** doivent exister avant l'envoi.

  · la porte du texte (`audit_outreach.py`) dit si le message est propre ;
  · ce fichier dit si l'on a **le droit d'écrire** : A la joignabilité, B l'intention numérique,
    C l'acheteur (`sales/RESEARCH-STANDARD.md` §8b, ruling King du 17/09).

Ce qu'il refuse de faire
------------------------
Deviner. Sans preuve datée, une porte reste `inconnue`, et une piste à 2/3 **ne part pas** : elle
attend une décision écrite de King. Une preuve (« leur page Facebook a posté le 12/09 ») se dépose dans
`leads/PREUVES-<date>.csv` avec sa source et sa date — jamais dans une note floue.

Usage
-----
    python3 tools/outreach/verify.py --date 2026-10-27
    python3 tools/outreach/verify.py --date 2026-10-27 --preuves leads/PREUVES-2026-10-27.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
AN = 365  # une preuve d'intention numérique vaut un an (§8b porte B) — au-delà, l'organisme est dormant


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")


def numero(brut: str) -> str:
    d = re.sub(r"\D", "", brut or "")
    if d.startswith("237") and len(d) == 12:
        d = d[3:]
    return d if len(d) == 9 and d.startswith("6") else ""


def jours(vu_le: str, aujourdhui: date) -> int | None:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return (aujourdhui - datetime.strptime((vu_le or "").strip(), fmt).date()).days
        except ValueError:
            continue
    return None


# ── les preuves déposées ────────────────────────────────────────────────────────────────────────

@dataclass
class Preuve:
    cle: str
    type: str          # site · facebook · catalogue · google · avis
    texte: str
    source: str
    vu_le: str

    def age(self, aujourdhui: date) -> int | None:
        return jours(self.vu_le, aujourdhui)


def lit_preuves(chemin: Path) -> list[Preuve]:
    if not chemin.exists():
        return []
    out: list[Preuve] = []
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            g = lambda k: (r.get(k) or "").strip()  # noqa: E731
            if not g("nom") and not g("slug"):
                continue
            out.append(Preuve(cle=slug(g("slug") or g("nom")), type=fold(g("type")) or "autre",
                              texte=g("preuve"), source=g("source"), vu_le=g("vu_le")))
    return out


def lit_porte_a(chemin: Path) -> list[Preuve]:
    """Les observations du 25/10, converties en preuves datées — pas en légende.

    `sales/PORTE-A-2026-10-25.md` porte vingt-huit lignes : un numéro, une coche, ce que King a vu en
    ouvrant le profil. Trois choses s'en tirent, et rien d'autre :

      · « Business "…" »  → la porte B (§8b : compte business / catalogue actif), datée du 25/10 ;
      · « ⛔ mort »        → la porte A tombe : le numéro ne joint pas WhatsApp ;
      · « ⚠️ »            → rien. Une ligne personnelle sans nom d'établissement n'ouvre aucune porte.
    """
    if not chemin.exists():
        return []
    vu = re.search(r"(\d{4}-\d{2}-\d{2})", chemin.name)
    jour = vu.group(1) if vu else date.today().isoformat()
    out: list[Preuve] = []
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if not ligne.startswith("|"):
            continue
        cols = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cols) < 5 or not re.fullmatch(r"\d+", cols[0]):
            continue
        nom, tel, marque, vu_txt = cols[1], re.sub(r"[^\d]", "", cols[2]), cols[3], cols[4]
        if not numero(tel):
            continue
        if "⛔" in marque:
            out.append(Preuve(cle=slug(nom), type="mort", texte=f"numéro mort ({vu_txt})",
                              source=chemin.name, vu_le=jour))
        elif "business" in fold(vu_txt):
            out.append(Preuve(cle=slug(nom), type="whatsapp_business", texte=vu_txt,
                              source=chemin.name, vu_le=jour))
    return out


# ── les pistes ──────────────────────────────────────────────────────────────────────────────────

# Un domaine qui existe = hors cible pour cette offre (§8c, point 6) : on ne dit jamais « il vous
# manque une page » à quelqu'un qui en a une. Les statuts négatifs du CRM (« none found », « expiré »,
# « aucune page ») sont la seule façon de lire une colonne Website remplie de prose.
DOMAINE = re.compile(r"\b[a-z0-9][a-z0-9-]{1,62}\.(?:com|cm|net|org|shop|online|site|fr|blogspot\.com)\b",
                     re.I)
SITE_MORT = re.compile(r"none|aucun|aucune|expir|mort|park|pas de site|no site|domaine libre|"
                       r"zéro résultat|zero resultat", re.I)

TYPES_A_CONSEIL = re.compile(r"clinique|hopital|polyclinique|institut|groupe scolaire|universit|"
                             r"fondation|centre hospitalier|district|mairie|diocese", re.I)


@dataclass
class Piste:
    cle: str
    nom: str
    ville: str
    num: str
    profil: str
    acheteur: str
    site: str
    statut_site: str
    dernier_post: str
    note: str
    a: str = "inconnu"
    b: str = "inconnu"
    c: str = "inconnu"
    motifs: dict[str, str] = field(default_factory=dict)
    a_mort: str = ""
    preuves: list[Preuve] = field(default_factory=list)

    @property
    def portes(self) -> int:
        return sum(1 for x in (self.a, self.b, self.c) if x == "pass")

    @property
    def site_vivant(self) -> str:
        """Le domaine réel de la ligne, s'il existe et n'est pas marqué mort. Sinon la chaîne vide."""
        texte = f"{self.site} {self.statut_site}".strip()
        if SITE_MORT.search(texte) or not DOMAINE.search(texte):
            return ""
        return DOMAINE.search(texte).group(0)   # type: ignore[union-attr]

    @property
    def verdict(self) -> str:
        if self.site_vivant:
            return "HORS-CIBLE"
        if "fail" in (self.a, self.b, self.c):
            return "JAMAIS"
        if self.portes == 3:
            return "ENVOYER"
        if self.portes == 2:
            return "KING-TRANCHE"
        return "PAS-ENVOYÉ"

    @property
    def manque(self) -> str:
        noms = {"a": "A joignabilité", "b": "B intention numérique", "c": "C acheteur"}
        return ", ".join(noms[k] for k in ("a", "b", "c") if getattr(self, k) != "pass")

    @property
    def raison_manque(self) -> str:
        """La raison de la **première porte qui manque** — pas celle d'une porte déjà franchie."""
        for k in ("a", "b", "c"):
            if getattr(self, k) != "pass":
                return self.motifs.get(k, "")
        return ""


def lit_crm(chemin: Path) -> list[Piste]:
    out: list[Piste] = []
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            g = lambda k: (r.get(k) or "").strip()  # noqa: E731
            if g("Contacted").lower().startswith("y") or g("stage") in ("lost", "disqualified", "demo"):
                continue
            num = numero(g("wa_number") or g("Phone"))
            if not num or not g("School"):
                continue
            out.append(Piste(cle=slug(g("School")) + "-" + num[-4:], nom=g("School"), ville=g("City"),
                             num=num, profil=g("profile_name_seen"), acheteur=g("Decision maker"),
                             site=g("Website"), statut_site=g("Website status"),
                             dernier_post=g("Last FB post"), note=g("Notes"),
                             a="pass" if g("wa_verified").lower() == "yes" else
                               ("fail" if g("wa_verified").lower() == "no" else "inconnu")))
    return out


def applique_portes(pistes: list[Piste], preuves: list[Preuve], aujourdhui: date) -> list[Piste]:
    """A, B, C — chaque porte ne se ferme ou ne s'ouvre que sur une preuve écrite."""
    par_cle: dict[str, list[Preuve]] = {}
    for p in preuves:
        par_cle.setdefault(p.cle, []).append(p)

    for x in pistes:
        # La preuve peut être déposée sous le slug, sous le nom, ou sur les neuf derniers chiffres.
        trouvees = par_cle.get(x.cle, []) or par_cle.get(slug(x.nom), []) or \
            par_cle.get(slug(x.nom) + "-" + x.num[-4:], [])
        x.preuves = trouvees

        for p in trouvees:                      # un numéro vu mort reste mort, quoi qu'en dise le CRM
            if p.type == "mort":
                x.a, x.a_mort = "fail", p.texte

        # A · joignabilité — la seule source qui vaut est le geste de King (profil vu).
        if x.a == "pass":
            x.motifs["a"] = "numéro vu sur WhatsApp (CRM `wa_verified=yes`)"
        elif x.a == "fail":
            x.motifs["a"] = x.a_mort or "`wa_verified=no` — le numéro ne joint pas WhatsApp"
        else:
            x.motifs["a"] = "numéro jamais ouvert sur WhatsApp"

        # B · intention numérique — un site vivant, une page qui a posté il y a moins d'un an, un
        # catalogue. Une preuve déposée l'emporte sur le CRM, qui est souvent vide.
        for p in trouvees:
            age = p.age(aujourdhui)
            if age is None:
                continue
            if p.type in ("facebook", "fb", "instagram", "whatsapp_business") and age <= AN:
                x.b, x.motifs["b"] = "pass", f"page active — {p.texte} ({p.vu_le}, {p.source})"
                break
            if p.type in ("site", "catalogue", "google", "avis") and age <= AN:
                x.b, x.motifs["b"] = "pass", f"{p.type} vivant — {p.texte} ({p.vu_le}, {p.source})"
                break
        if x.b != "pass":
            age_post = jours(x.dernier_post, aujourdhui)
            if x.site and not re.search(r"aucun|expir|mort|park", fold(x.statut_site)):
                x.b, x.motifs["b"] = "pass", f"site en ligne ({x.site})"
            elif age_post is not None and age_post <= AN:
                x.b, x.motifs["b"] = "pass", f"dernier post Facebook il y a {age_post} jours"
            elif age_post is not None:
                x.b, x.motifs["b"] = "fail", f"page dormante — dernier post il y a {age_post} jours"
            else:
                x.motifs["b"] = "aucun signe numérique daté (ni site, ni page suivie)"

        # C · acheteur — un titulaire nommé sur un cabinet de ville, pas un conseil d'administration.
        if x.acheteur:
            x.c, x.motifs["c"] = "pass", f"titulaire nommé — {x.acheteur}"
        elif TYPES_A_CONSEIL.search(x.nom):
            x.c, x.motifs["c"] = "fail", "structure à conseil (clinique, institut, groupe) — acheteur non identifié"
        else:
            x.motifs["c"] = "aucun nom d'acheteur"
    return pistes


# ── le rendu ───────────────────────────────────────────────────────────────────────────────────

def rendu(pistes: list[Piste], jour: date, nb_preuves: int) -> str:
    env = [p for p in pistes if p.verdict == "ENVOYER"]
    tranche = [p for p in pistes if p.verdict == "KING-TRANCHE"]
    jamais = [p for p in pistes if p.verdict in ("JAMAIS", "PAS-ENVOYÉ")]
    hors = [p for p in pistes if p.verdict == "HORS-CIBLE"]
    l = [f"# VÉRIFICATION — trois portes (§8b) · {jour}", "",
         f"```text\nPISTES   {len(pistes)} jamais contactées, numéro valide\n"
         f"PREUVES  {nb_preuves} déposée(s) dans leads/PREUVES-{jour}.csv\n"
         f"VERDICT  {len(env)} ENVOYER · {len(tranche)} KING-TRANCHE · {len(jamais)} pas d'envoi · "
         f"{len(hors)} hors cible\n```", "",
         "> Une porte ne s'ouvre que sur une preuve datée. `inconnu` n'est pas `pass` : une piste à 2/3",
         "> ne part pas, elle attend une décision écrite (ruling 17/09, §8b).", ""]
    if env:
        l += ["## 1 · Les messages qui ont le droit de partir", "",
              "| # | Cabinet | Numéro | A | B | C | Le fait à écrire |", "|---|---|---|---|---|---|---|"]
        for i, p in enumerate(env, 1):
            l.append(f"| {i} | **{p.nom}** | {p.num} | ✅ {p.motifs['a']} | ✅ {p.motifs['b']} "
                     f"| ✅ {p.motifs['c']} | {p.motifs['b']} |")
        l.append("")
    if tranche:
        l += ["## 2 · Ce qui manque pour les faire partir", "",
              "| Cabinet | Numéro | Portes | Ce qui manque, et où le prendre |", "|---|---|---|---|"]
        for p in tranche:
            l.append(f"| {p.nom} | {p.num} | {p.portes}/3 | {p.manque} — {p.raison_manque} |")
        l.append("")
        l += ["**Le geste qui débloque le plus de lignes** : ouvrir la page Facebook ou Google de chaque",
              "cabinet ci-dessus, noter la date du dernier post (ou du dernier avis) dans",
              f"`leads/PREUVES-{jour}.csv`. Une date de moins d'un an ouvre la porte B ; une date plus",
              "ancienne la ferme **définitivement** (organisme dormant, §8b). C'est le seul travail qui",
              "transforme des pistes en messages.", ""]
    if hors:
        l += ["## 3 · Hors cible : ils ont déjà un site dédié (§8c, point 6)", "",
              "| Cabinet | Le domaine |", "|---|---|"]
        for p in hors[:30]:
            l.append(f"| {p.nom} | `{p.site_vivant}` |")
        if len(hors) > 30:
            l.append(f"| … | et {len(hors) - 30} autres |")
        l += ["", "On ne leur écrit jamais « il vous manque une page ». Un autre angle, plus tard, "
              "éventuellement — jamais celui-là.", ""]
    if jamais:
        l += ["## 4 · Ce qu'on n'écrit pas, et pourquoi", "",
              "| Cabinet | Portes | Raison |", "|---|---|---|"]
        for p in jamais[:40]:
            raison = p.motifs.get("a") if p.a == "fail" else (p.motifs.get("b") if p.b == "fail" else p.motifs.get("c"))
            l.append(f"| {p.nom} | {p.portes}/3 | {raison} |")
        if len(jamais) > 40:
            l.append(f"| … | | et {len(jamais) - 40} autres |")
        l.append("")
    l += ["## 5 · Ce que ce fichier ne remplace pas", "",
          "- **La porte A n'est jamais déduite d'un annuaire** : `wa_verified=yes` veut dire que King a vu",
          "  le profil, un jour daté. Un numéro publié par l'Ordre n'est pas un numéro vérifié.",
          "- **La porte B ne s'invente pas** : une page Facebook sans date n'ouvre rien. La date est la preuve.",
          "- **Le §8c reste obligatoire** avant d'écrire un fait sur le prospect : chercher le nom exact +",
          "  la ville, ouvrir le domaine réel, vérifier l'adresse et les horaires. Une affirmation fausse",
          "  coûte le meilleur prospect de la liste.", ""]
    return "\n".join(l)


def ecrit_json(pistes: list[Piste], chemin: Path) -> None:
    chemin.write_text(json.dumps(
        [{"slug": p.cle, "nom": p.nom, "num": p.num, "verdict": p.verdict, "portes": p.portes,
          "fact": p.motifs.get("b", "")} for p in pistes], ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--crm", default=str(RACINE / "leads/CRM.csv"))
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--preuves", default="")
    ap.add_argument("--porte-a", default=str(RACINE / "sales/PORTE-A-2026-10-25.md"),
                    help="les observations du 25/10, converties en preuves datées")
    ap.add_argument("--out", default="")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    jour = date.fromisoformat(a.date)
    chemin_preuves = Path(a.preuves) if a.preuves else RACINE / f"leads/PREUVES-{a.date}.csv"
    preuves = lit_preuves(chemin_preuves)
    porte_a = lit_porte_a(Path(a.porte_a)) if a.porte_a else []
    vues = {(p.cle, p.type) for p in preuves}
    preuves += [p for p in porte_a if (p.cle, p.type) not in vues]
    pistes = applique_portes(lit_crm(Path(a.crm)), preuves, jour)
    pistes.sort(key=lambda p: (-p.portes, p.nom))

    out = Path(a.out) if a.out else RACINE / f"leads/VERIF-{a.date}.md"
    out.write_text(rendu(pistes, jour, len(preuves)), encoding="utf-8")
    j = Path(a.json) if a.json else RACINE / f"leads/VERIF-{a.date}.json"
    ecrit_json(pistes, j)

    env = sum(1 for p in pistes if p.verdict == "ENVOYER")
    tr = sum(1 for p in pistes if p.verdict == "KING-TRANCHE")
    print(f"{env} ENVOYER · {tr} KING-TRANCHE · {len(pistes)} pistes → {out}")
    if not preuves:
        print(f"  ⚠ aucune preuve déposée ({chemin_preuves.name} absent) : la porte B reste `inconnue`,")
        print("    donc presque rien ne part. C'est le comportement voulu, pas un bug.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
