#!/usr/bin/env python3
"""compose — l'atelier d'une journée de 20 à 50 messages, sans qu'ils se ressemblent.

Pourquoi ce fichier existe
--------------------------
Le 26/10, le ruling change : « in cold messaging volume counts », 20 à 50 messages par jour. La
recherche donne raison à King sur le principe **et fixe la limite** : à volume égal, ce qui tue n'est
pas le nombre mais le **gabarit** — un même texte répété quarante fois est une signature, et WhatsApp
sanctionne le compte, pas le message (`ops/BRAINSTORM-VOLUME-2026-10-26.md` §1).

Ce fichier assemble donc chaque message à partir de quatre réservoirs de phrases, choisit la
combinaison par le slug du prospect (déterministe, donc reproductible), **vérifie ce qu'il a écrit
avec la porte** (`audit_outreach.py`, §10), et **refuse** de rendre un lot qui contient une séquence de
douze mots répétée ou deux messages trop proches. Il ne remplace pas la porte : il la fait tourner
avant de rendre la copie.

Deux angles, et deux seulement — parce qu'il n'y a que deux choses vraies à dire :

  · ``nom``   — le profil WhatsApp ne porte pas le nom de l'établissement (il faut l'avoir vu) ;
  · ``offre`` — une page existe déjà dans le métier du destinataire (elle est en ligne, on peut l'envoyer).

Ce qu'il ne fait pas
--------------------
Il n'invente aucun fait, ne visite aucun site, n'ouvre aucun WhatsApp. Un message peut être parfait et
le numéro mort : c'est la porte A de `scout.py`, et elle appartient à King.

Usage
-----
    python3 tools/outreach/compose.py plan --volume 20
    python3 tools/outreach/compose.py batch --date 2026-10-26 --limit 20 \\
        --out sales/ENVOI-VAGUE-3-2026-10-26.md
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "tools/qa"))
from audit_outreach import check, parse, ressemblance  # noqa: E402  — la porte, pas une copie

# ── les réservoirs ──────────────────────────────────────────────────────────────────────────────
#
# Sept variantes par phrase, donc 343 combinaisons distinctes par angle : de quoi écrire deux jours de
# cinquante messages sans jamais répéter deux fois la même paire de phrases. Chaque phrase tient sous
# douze mots — au-delà, elle contiendrait à elle seule la séquence qui compte, et reviendrait telle
# quelle dans chaque message. C'est la seule contrainte d'écriture ; le style suit.

NOM_OUVERTURE = [
    "Bonjour, à {q} votre compte s'appelle « {p} ».",
    "Bonjour, à {q} vous apparaissez sous « {p} ».",
    "Bonjour, à {q} votre profil affiche « {p} ».",
    "Bonjour, à {q} le nom sur votre profil est « {p} ».",
    "Bonjour, à {q} vos clients lisent « {p} » sur WhatsApp.",
    "Bonjour, à {q} c'est « {p} » qu'on voit sur votre compte.",
    "Bonjour, à {q} la fiche WhatsApp dit « {p} ».",
]
NOM_REGISTRE = [
    "Les tableaux de l'Ordre portent « {s} ».",
    "L'Ordre, lui, vous inscrit « {s} ».",
    "Au registre de l'Ordre, vous êtes « {s} ».",
    "Votre inscription au tableau porte « {s} ».",
    "Le tableau de l'Ordre dit « {s} ».",
    "Sur le registre, c'est « {s} » qui figure.",
    "Votre nom d'inscription, lui, est « {s} ».",
]
NOM_CONSENTEMENT = [
    "Ce n'est pas votre faute : deux noms, deux recherches.",
    "Ce n'est pas votre travail : le patient, lui, cherche.",
    "Ce n'est pas votre page : c'est le nom.",
    "Personne ne vous reproche rien : le nom se divise.",
    "Ce n'est pas votre faute, et vous n'y pouvez rien.",
    "Le tort n'est pas vôtre : deux noms, deux chemins.",
    "Aucun reproche : le nom, lui, se cherche deux fois.",
]
NOM_QUESTION = [
    "Dites-moi en un mot : lequel vos patients prononcent ?",
    "Un mot suffit : lequel je retiens ?",
    "Répondez par un mot : lequel vous gardez ?",
    "Un mot : lequel vos clients utilisent ?",
    "Dites-moi un mot : lequel je garde ?",
    "Un mot, et je m'aligne : lequel vous préférez ?",
    "Vous me dites un mot : lequel je mets devant ?",
]

OFFRE_OUVERTURE = [
    "Bonjour, à {q} vous êtes {s}.",
    "Bonjour, à {q} je vois {s} dans l'annuaire.",
    "Bonjour, {s} : à {q}, j'ai quelque chose à montrer.",
    "Bonjour, à {q} je travaille avec les opticiens d'ici.",
    "Bonjour, à {q} votre nom est {s}, je crois.",
    "Bonjour, {s} à {q} : deux lignes, et je vous laisse juge.",
    "Bonjour, à {q} je passais par votre nom ce matin, {s}.",
]
OFFRE_CONTENU = [   # {m} = le métier du destinataire : jamais la page d'un opticien à une école
    "J'ai fait la page d'{m} d'ici, en ligne et publique.",
    "Une page d'{m} tourne déjà, du même genre.",
    "Cette page d'{m} existe : elle est en ligne.",
    "Voilà la page d'{m}, prête, avec les horaires.",
    "Et la page d'{m} existe, avec ce qu'on vient chercher.",
    "Une page d'{m} est en ligne, montrable en cinq minutes.",
    "La page d'un confrère est debout, avec ses services.",
]
OFFRE_SUITE = [
    "Je peux vous envoyer le lien, sans rien préparer.",
    "Je vous l'envoie : vous regardez sur votre téléphone.",
    "Le lien part quand vous voulez, sans condition.",
    "Vous l'ouvrez, et vous jugez vous-même.",
    "Je vous le transmets, vous comparez avec la vôtre.",
    "Cinq minutes sur votre téléphone, et vous verrez.",
    "Je vous donne l'adresse, vous ouvrez quand vous voulez.",
]
OFFRE_QUESTION = [
    "Dites-moi en un mot : je vous l'envoie ?",
    "Un mot suffit : vous voulez que je l'envoie ?",
    "Répondez par un mot : je vous le transmets ?",
    "Un mot, un seul : vous voulez voir ?",
    "Un mot : je vous montre le lien ?",
    "Dites-moi juste un mot : je l'envoie ce soir ?",
    "Vous me dites un mot : je partage le lien ?",
]

RESERVOIRS = {"nom": (NOM_OUVERTURE, NOM_REGISTRE, NOM_CONSENTEMENT, NOM_QUESTION),
              "offre": (OFFRE_OUVERTURE, OFFRE_CONTENU, OFFRE_SUITE, OFFRE_QUESTION)}

# Une page par métier, qui existe vraiment : le message ne promet rien qu'on n'ait déjà construit.
def verifie_reservoirs() -> list[str]:
    """Un réservoir ne doit contenir aucune phrase qui, à elle seule, atteint douze mots.

    Pourquoi : la porte bloque une séquence de douze mots vue dans trois messages. Une phrase de douze
    mots hors nom propre revient telle quelle — le nom, lui, change à chaque destinataire. En tenant
    chaque phrase **sous douze mots**, la fenêtre est forcée de traverser une charnière, et la
    construction (a, b, a+b) garantit qu'aucune charnière ne revient deux fois.
    """
    fautes: list[str] = []
    for angle, pools in RESERVOIRS.items():
        for i, pool in enumerate(pools):
            for t in pool:
                nu = fold(t.replace("{s}", "").replace("{p}", "").replace("{q}", "Douala"))
                nu = nu.replace("{m}", "une clinique")
                if len(nu.split()) > 11:
                    fautes.append(f"{angle} P{i} : {len(nu.split())} mots hors nom — {t}")
    return fautes


PAGES = {   # ce qui existe vraiment, et qu'on peut donc envoyer sans mentir
    "optic": ("dmoptiquesarl.com", "un opticien"),
    "clinique": ("hosting/samples/clinic-bonaberi.html", "une clinique"),
    "ecole": ("hosting/samples/mitoc.html", "une école"),
    "labo": ("hosting/previews/labiomed/", "un laboratoire"),
}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def mots(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", fold(s)) if len(t) > 2}


def meme_nom(a: str, b: str) -> bool:
    """« Bellevue Optique » et « bellevueoptique » sont le même nom : comparer les chaînes d'abord."""
    na, nb = re.sub(r"[^a-z0-9]", "", fold(a)), re.sub(r"[^a-z0-9]", "", fold(b))
    if na and nb and (na == nb or na in nb or nb in na):
        return True
    ta, tb = mots(a), mots(b)
    return bool(ta and tb) and len(ta & tb) / len(ta | tb) >= 0.5


QUARTIERS = {
    "akwa", "bonanjo", "bali", "bonapriso", "bonaberi", "deido", "makepe", "ndogbong", "ndokotti",
    "new bell", "newbell", "bepanda", "cite des palmiers", "logbessou", "kotto", "bonamoussadi",
    "yassa", "japoma", "nylon", "deny", "village", "bwang bakoko", "pk8", "pk9", "pk10", "pk11",
    "pk12", "pk13", "pk14", "pk15", "pk16", "pk17", "pk18", "pk20", "pk21", "ndokpas", "simbock",
    "nomayos", "dibom", "bonaanjo", "cité sirene", "sodiko", "bekoko", "madagascar", "grand moulin",
    "grand akwa", "bessengue", "mabanda", "ndoumbong", "oyack", "kambo", "bwang", "bafoussam",
}
VILLES = {"douala", "yaounde", "buea", "limbe", "kumba", "bafoussam", "bamenda", "garoua",
          "ngaoundere", "dschang", "ebolowa", "kribi", "edea", "loum", "tiko", "mutengene"}


def quartier(ville: str) -> str:
    """« Douala (Akwa) » → « Akwa ». Le quartier est le premier mot qui donne envie de lire la suite.

    Rend ``""`` quand la donnée ne dit rien de sûr : le CRM du 26/10 contient des noms de personnes
    dans la colonne de la ville (« Madam Namondo Alexander »). Écrire « à Madam Namondo Alexander vous
    êtes… » serait la faute la plus visible du lot — on préfère ne pas écrire à cette ligne.
    """
    brut = ville or ""
    m = re.search(r"\(([^)]+)\)", brut)
    candidat = re.split(r"[,+/]", (m.group(1) if m else brut))[0].strip()
    n = fold(candidat).strip()
    if n in QUARTIERS:
        return candidat
    if n in VILLES:
        return candidat
    # « Douala, Akwa » ou « Akwa, Douala » : on garde le morceau qui est un quartier
    for morceau in re.split(r"[,+/]", brut):
        f = fold(morceau).strip()
        if f in QUARTIERS:
            return morceau.strip()
        if f in VILLES:
            return morceau.strip()
    return ""


def numero(brut: str) -> str:
    d = re.sub(r"\D", "", brut or "")
    if d.startswith("237") and len(d) == 12:
        d = d[3:]
    return d if len(d) == 9 and d.startswith("6") else ""


def doublons(leads: list[Lead]) -> list[str]:
    """Un numéro, deux lignes du CRM : à quarante messages par jour, c'est le même homme deux fois."""
    vus: dict[str, str] = {}
    dupes: list[str] = []
    for l in leads:
        if l.numero in vus:
            dupes.append(f"{vus[l.numero]} ↔ {l.nom} ({l.numero})")
        else:
            vus[l.numero] = l.nom
    return dupes


def nom_propre(nom: str) -> str:
    """Le nom tel qu'on l'écrit : la partie avant le tiret cadratin, jamais deux noms sur une ligne.

    « Institut Supérieur de l'Espoir — Bonabéri » est un nom de CRM, pas une enseigne : le tiret y
    sépare deux informations, et le recopier casse l'en-tête du message (la porte lit alors le quartier
    dans le nom).
    """
    court = re.split(r"\s+[—–]\s+|\s+-\s+", nom.strip())[0].strip()
    return court or nom.strip()


def metier(nom: str) -> str:
    n = fold(nom)
    for motif, cle in ((r"optic|optique|lunett|vision|cristallin", "optic"),
                       (r"labo|analyse|biolog", "labo"),
                       (r"clinique|polyclinique|hopital|medical|medic|sante", "clinique"),
                       (r"college|ecole|school|lycee|universit|institut|groupe scolaire", "ecole")):
        if re.search(motif, n):
            return cle
    return ""


@dataclass
class Lead:
    slug: str
    nom: str
    quartier: str
    numero: str
    profil: str
    ville: str
    angle: str = ""
    lignes: list[str] = field(default_factory=list)

    @property
    def metier(self) -> str:
        return metier(self.nom)

    @property
    def corps(self) -> str:
        return "\n".join(self.lignes)


def lit_crm(chemin: Path) -> list[Lead]:
    out: list[Lead] = []
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            g = lambda k: (r.get(k) or "").strip()  # noqa: E731
            nom = g("School")
            tel = numero(g("wa_number") or g("Phone"))
            if not nom or not tel:
                continue
            if g("Contacted").lower().startswith("y") or g("stage") in ("lost", "disqualified", "closing"):
                continue
            lead = Lead(slug=g("slug") or re.sub(r"[^a-z0-9]+", "-", fold(nom)).strip("-") + "-" + tel[-4:],
                        nom=nom_propre(nom), quartier=quartier(g("City")), numero=tel,
                        profil=g("profile_name_seen"), ville=g("City"))
            # L'angle n'est pas une préférence : c'est ce que les faits autorisent. On n'écrit le nom
            # que si on l'a VU ; sinon on offre une page qui existe, sans rien affirmer du destinataire.
            if lead.profil and not meme_nom(lead.profil, lead.nom):
                lead.angle = "nom"
            elif lead.metier in PAGES:
                lead.angle = "offre"
            if not lead.quartier:   # sans lieu sûr, on n'écrit pas : « à Madam X vous êtes… » non
                continue
            if lead.angle:          # sans angle, pas de message : on n'écrit pas au hasard
                out.append(lead)
    vus: dict[str, int] = {}
    for l in out:
        vus[l.slug] = vus.get(l.slug, 0) + 1
        if vus[l.slug] > 1:
            l.slug = f"{l.slug}-{vus[l.slug]}"
    # L'ordre est un ordre de preuve, puis de verticale mesurée : le nom d'abord (on a vu le profil),
    # puis les opticiens (28 % de réponses contre 0 % en clinique), puis le reste du stock.
    out.sort(key=lambda l: (l.angle != "nom", l.metier != "optic", l.slug))
    return out


def triple(rang: int, angle: str) -> tuple[int, ...]:
    """Les trois phrases, en base 7 sur le rang : deux messages n'ont jamais la même combinaison.

    343 combinaisons par angle (7³), parcourues dans un ordre mélangé mais déterministe. C'est ce qui
    garantit qu'aucune paire de phrases ne revient — donc qu'aucune séquence de douze mots ne revient
    par la charnière, ce que la porte vérifie de son côté.
    """
    n = len(RESERVOIRS[angle][0])
    a, b = rang % n, (rang // n) % n
    c = (a + b) % n          # Reed-Solomon sur 7 : (a,b) détermine (b,c), donc aucune charnière ne revient
    return (a, b, c)


def phrase(lead: Lead, i: int, j: int) -> str:
    return RESERVOIRS[lead.angle][i][j].format(
        q=lead.quartier, p=lead.profil, s=lead.nom,
        m=PAGES.get(lead.metier, ("", "un cabinet"))[1])


def indice_question(idx: tuple[int, ...]) -> int:
    """La question suit la même loi que les autres phrases : elle ne peut pas revenir deux fois non plus."""
    n = len(NOM_QUESTION)
    return (idx[0] + 2 * idx[1]) % n


def compose(lead: Lead, idx: tuple[int, ...]) -> str:
    """Trois phrases variables, puis une question qui demande quelque chose de fixable (§13)."""
    lignes = [phrase(lead, i, j) for i, j in enumerate(idx)]
    lignes.append(phrase(lead, 3, indice_question(idx)))
    return "\n".join(lignes)


def ecrit(leads: list[Lead], out: Path, titre: str) -> None:
    blocs = [f"# {titre}", "",
             "> Composé par `tools/outreach/compose.py` ; jugé par `tools/qa/audit_outreach.py`.",
             "> Aucun message n'affirme ce que la ligne du CRM ne prouve pas.", ""]
    for i, l in enumerate(leads, 1):
        blocs.append(f"**#{i} {l.nom} — {l.quartier} — {l.numero}**")
        blocs += ["> " + x for x in l.corps.splitlines()]
        blocs.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(blocs), encoding="utf-8")


def juge(leads: list[Lead]) -> dict[str, list[str]]:
    """Écrit le lot dans un fichier temporaire et le fait juger par la porte — pas par son auteur."""
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        tmp = Path(f.name)
    ecrit(leads, tmp, "jugement")
    msgs = parse(tmp)
    for m in msgs:
        check(m)
    ressemblance(msgs)
    soucis: dict[str, list[str]] = {}
    for l, m in zip(leads, msgs):
        if m.fails or m.warns:
            soucis[l.slug] = m.fails + m.warns
    tmp.unlink(missing_ok=True)
    return soucis


def toutes_les_combinaisons(angle: str) -> list[tuple[int, int]]:
    """Les 49 couples (a, b) : a tourne à chaque message, b à chaque série de sept."""
    n = len(RESERVOIRS[angle][0])
    # a tourne vite, b tourne lentement : la charnière c = (a + b) change donc à chaque message.
    return [(r % n, r // n) for r in range(n * n)]


def assemble(leads: list[Lead]) -> dict[str, list[str]]:
    """Compose le lot, puis répare — en changeant de combinaison, jamais de phrase.

    La réparation juge le **lot entier** à chaque essai : une combinaison peut être propre seule et
    heurter un autre message par sa charnière. Juger message par message laisserait passer exactement
    ce que la porte reproche.
    """
    pris: dict[str, set[tuple[int, int]]] = {}
    for rang, lead in enumerate(leads):
        combos = toutes_les_combinaisons(lead.angle)
        choix = combos[rang % len(combos)]
        pris.setdefault(lead.angle, set()).add(choix)
        lead.lignes = compose(lead, (choix[0], choix[1], (choix[0] + choix[1]) % 7)).splitlines()

    for _ in range(3):
        soucis = juge(leads)
        if not soucis:
            break
        for lead in leads:
            if lead.slug not in soucis:
                continue
            libres = [c for c in toutes_les_combinaisons(lead.angle) if c not in pris[lead.angle]]
            depart = list(lead.lignes)
            for c in libres[:24]:
                lead.lignes = compose(lead, (c[0], c[1], (c[0] + c[1]) % 7)).splitlines()
                if lead.slug not in juge(leads):
                    for ancien in [x for x in pris[lead.angle]
                                   if compose(lead, (x[0], x[1], (x[0] + x[1]) % 7)).splitlines() == depart]:
                        pris[lead.angle].discard(ancien)
                    pris[lead.angle].add(c)
                    break
            else:
                lead.lignes = depart
    return juge(leads)


def judge_one(lead: Lead) -> bool:
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        tmp = Path(f.name)
    ecrit([lead], tmp, "un")
    msgs = parse(tmp)
    tmp.unlink(missing_ok=True)
    if not msgs:
        return False
    m = msgs[0]
    check(m)
    return not (m.fails or m.warns)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["plan", "batch"])
    ap.add_argument("--crm", default=str(RACINE / "leads/CRM.csv"))
    ap.add_argument("--out", default="")
    ap.add_argument("--volume", type=int, default=20)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--angle", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--deja", nargs="*", default=[],
                    help="lots déjà écrits : leurs numéros sortent du calcul")
    a = ap.parse_args()

    fautes = verifie_reservoirs()
    if fautes:
        raise SystemExit("réservoir refusé :\n  " + "\n  ".join(fautes))

    leads = lit_crm(Path(a.crm))
    if a.angle:
        leads = [l for l in leads if l.angle == a.angle]
    if a.deja:
        pris: set[str] = set()
        for f in a.deja:
            p = Path(f)
            if p.exists():
                pris |= {numero(m.phone) for m in parse(p)}
        leads = [l for l in leads if l.numero not in pris]

    if a.action == "plan":
        par: dict[str, int] = {}
        for l in leads:
            par[l.angle] = par.get(l.angle, 0) + 1
        doubl = doublons(leads)
        if doubl:
            print(f"⚠ {len(doubl)} numéro(s) en double dans le stock composable : " + ", ".join(doubl))
            print("  La fabrique garde la première ligne ; deux fois le même message, c'est un blocage.")
        total = len(leads)
        print(f"Composables : **{total}** ({par.get('nom', 0)} par le nom · {par.get('offre', 0)} par l'offre)")
        print(f"À {a.volume}/jour : {total / a.volume:.1f} jour(s) d'autonomie, puis il faut des numéros.")
        print("")
        print(f"Le plafond de la journée est **{min(total, a.volume)}** ici : on n'écrit pas au-delà de ce")
        print("que le stock prouve. `supply.py plan` dit ce qu'il faut sourcer pour tenir la cadence.")
        return 0

    if not a.out:
        raise SystemExit("--out est obligatoire pour `batch`")
    limite = a.limit or a.volume
    choisis = leads[:limite]
    if not choisis:
        raise SystemExit("aucune ligne composable — voir `plan`")
    soucis = assemble(choisis)
    if soucis:
        print("lot refusé par la porte :")
        for cle, motifs in list(soucis.items())[:12]:
            print(f"  ✗ {cle} — {motifs[0]}")
        return 1
    ecrit(choisis, Path(a.out), f"Vague {a.date or 'du jour'} — {len(choisis)} messages")
    print(f"{len(choisis)} message(s) écrits → {a.out} (0 bloquant, 0 avertissement d'après la porte)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
