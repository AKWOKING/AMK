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
        --out sales/ENVOI-VOLUME-2026-10-27.md
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

NOM_OUVERTURE = [           # désarmement + ce que voit un patient : le nom du profil
    "Bonjour, c'est inattendu : à {q}, sur WhatsApp, « {p} ».",
    "Bonjour, inattendu, je sais : à {q}, WhatsApp affiche « {p} ».",
    "Bonjour, ça surprend : à {q}, votre profil dit « {p} ».",
    "Bonjour, sans doute inattendu : à {q}, votre profil « {p} ».",
    "Bonjour, c'est étrange : à {q}, WhatsApp lit 「{p}」.".replace("「", "«").replace("」", "»"),
    "Bonjour, je sais que c'est inattendu : à {q}, profil {s}.",
    "Bonjour, ça peut surprendre : à {q}, WhatsApp, « {p} ».",
]
NOM_CAUSE = [               # le deuxième fait, ET la cause nommée : un registre, pas le prospect
    "L'Ordre vous inscrit « {s} » : pas à vous.",
    "Le tableau dit « {s} » : pas chez vous.",
    "Deux noms, aucun des deux n'est chez vous.",
    "WhatsApp garde la vitrine, l'Ordre « {s} ».",
    "Votre nom vit chez Google, et Google décide.",
    "Ce registre le nomme « {s} » : jamais à vous.",
    "« {s} » au tableau : rien n'est à vous.",
]
NOM_PREUVE = [              # la preuve sociale, **vague par ruling King 26/10** : le métier et la ville,
                            # jamais le nom du client sans son accord. Un site existe et il tourne.
    "Je fais les sites pour les opticiens de Douala.",
    "Les sites des opticiens de Douala, c'est mon métier.",
    "Chez un opticien de Douala, le site est en ligne.",
    "Je fais les sites pour les opticiens de Douala, avec WhatsApp.",
    "Un opticien de Douala a le sien en ligne.",
    "Je fais les sites pour les opticiens de Douala, horaires compris.",
    "Le site d'un opticien de Douala tourne.",
]
NOM_QUESTION = [            # la question offre le site : elle ne demande plus un diagnostic
    "Dites-moi un mot : lequel en haut du site ?",
    "Un mot suffit : lequel passe en haut du site ?",
    "Répondez par un mot : lequel en haut du site ?",
    "Choisissez un mot : lequel va sur le site ?",
    "Dites-moi un mot : lequel en haut, avec WhatsApp ?",
    "Donnez-moi un mot : lequel pour votre site ?",
    "Sur le site, dites-moi lequel devant ?",
]

OFFRE_OUVERTURE = [         # désarmement + le nom que le patient lit sur le profil ou l'annuaire
    "Bonjour, c'est inattendu : à {q}, profil {s}.",
    "Bonjour, inattendu, je sais : à {q}, l'annuaire dit {s}.",
    "Bonjour, ça surprend : à {q}, votre profil dit {s}.",
    "Bonjour, sans doute inattendu : à {q}, WhatsApp dit {s}.",
    "Bonjour, c'est étrange : à {q}, l'annuaire affiche {s}.",
    "Bonjour, ça peut surprendre : à {q}, Google dit {s}.",
    "Bonjour, je sais que c'est inattendu : profil {s}, à {q}.",
]
OFFRE_CAUSE = [             # la cause nommée : les annuaires, Google, le profil — jamais lui
    "Ce que Google sort n'est pas à vous.",
    "Les annuaires parlent de vous, pas à vous.",
    "Rien de ce qui sort n'est chez vous.",
    "Google vous rend chez les annuaires, pas chez vous.",
    "Ce que le patient lit vient des annuaires.",
    "Votre vitrine tient chez Google, pas chez vous.",
    "Les annuaires recopient votre fiche, sans vous.",
]
OFFRE_PREUVE = [            # {m} = le métier du destinataire : jamais la page d'un opticien à une école
    "J'ai fait le site d'{m} d'ici, il tourne.",
    "Le site d'{m} d'ici est en ligne.",
    "J'ai construit le site d'{m} d'ici, il vit.",
    "Un site d'{m} tourne, avec horaires et numéro.",
    "J'ai fait le site d'{m}, il répond.",
    "Le site d'{m} d'ici répond, jour et nuit.",
    "Celui d'{m} d'ici tourne, avec WhatsApp.",
]
OFFRE_QUESTION = [          # la question offre le site — jamais un rendez-vous, jamais un prix
    "Un mot : je vous envoie le site ?",
    "Dites-moi un mot : voir le site d'{m} ?",
    "Un mot, un seul : je vous montre le site ?",
    "Répondez par un mot : je partage le site ?",
    "Vous voulez le site, et WhatsApp : un mot ?",
    "Montrez-moi un mot : j'envoie le site ?",
    "Je transmets le site ce soir : un mot ?",
]

RESERVOIRS = {"nom": (NOM_OUVERTURE, NOM_CAUSE, NOM_PREUVE, NOM_QUESTION),
              "offre": (OFFRE_OUVERTURE, OFFRE_CAUSE, OFFRE_PREUVE, OFFRE_QUESTION)}

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
    return (court or nom.strip()).replace(".", "")


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


def ecarte(leads: list[Lead], verif: Path) -> tuple[list[Lead], list[Lead]]:
    """Ce que le vérificateur a condamné ne s'écrit pas, même bien.

    Deux verdicts seulement ferment la porte à l'écriture : `JAMAIS` (le numéro ne joint pas WhatsApp —
    écrire là, c'est remplir une journée avec du vide) et `HORS-CIBLE` (le cabinet a déjà un site : lui
    dire qu'il lui en manque un est la faute du 24/09). Les 2/3 et les 1/3 restent dans le lot : leur
    porte A se ferme à l'envoi, en huit secondes, pas à l'écriture.
    """
    import json
    v = {x["num"]: x["verdict"] for x in json.loads(verif.read_text(encoding="utf-8"))}
    garde, ecartes = [], []
    for l in leads:
        (ecartes if v.get(l.numero) in ("JAMAIS", "HORS-CIBLE") else garde).append(l)
    return garde, ecartes


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
            # Deux refus appris à la main, et qui ne se réapprennent pas tout seuls (26/10) :
            #   · `wa_verified=no` — King a ouvert la conversation et WhatsApp a refusé le numéro
            #     (Royal Optic, Win Optic Plus). Écrire là, c'est remplir une journée avec du vide ;
            #   · un site **vivant** — lui proposer un site est la faute d'ISEE (26/10). Cristalys,
            #     LyfyOptic et Gift étaient dans les « composables » alors que leur page existe.
            if g("wa_verified").lower() == "no":
                continue
            enseigne = fold(g("Website") + " " + g("Website status"))
            if "vivant" in enseigne or "declare" in enseigne:
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
    """Les quatre phrases, en base 7 sur le rang : deux messages n'ont jamais la même combinaison.

    Depuis le 26/10 il y a quatre réservoirs (ouverture, cause, preuve, question) : les indices
    deviennent (a, a+b, a+2b, a+3b). Le couple (a, b) se lit dans les deux premiers — donc deux
    messages qui partagent une paire de phrases partageraient aussi le rang, ce qui n'arrive pas.
    C'est ce que la porte vérifie de son côté (§10) : une séquence de douze mots vue trois fois est
    la signature d'un compte qui diffuse.
    """
    n = len(RESERVOIRS[angle][0])
    a, b = rang % n, (rang // n) % n
    return (a, (a + b) % n, (a + 2 * b) % n, (a + 3 * b) % n)


def phrase(lead: Lead, i: int, j: int) -> str:
    return RESERVOIRS[lead.angle][i][j].format(
        q=lead.quartier, p=lead.profil, s=lead.nom,
        m=PAGES.get(lead.metier, ("", "un cabinet"))[1])


def indice_question(idx: tuple[int, ...], angle: str = "nom") -> int:
    """La question suit la même loi que les autres phrases : elle ne peut pas revenir deux fois non plus."""
    n = len(RESERVOIRS[angle][3])
    return (idx[0] + 2 * idx[1]) % n


def compose(lead: Lead, idx: tuple[int, ...]) -> str:
    """Quatre phrases : désarmer, nommer la cause, prouver, offrir (ruling King 26/10)."""
    lignes = [phrase(lead, i, j) for i, j in enumerate(idx)]
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

    Un message = **un rang**. Le rang donne les quatre indices (a, a+b, a+2b, a+3b) : deux messages
    d'un même angle ne partagent donc jamais une paire de phrases. La réparation juge le **lot
    entier** à chaque essai, parce qu'une combinaison propre seule peut heurter un autre message
    par sa charnière — et c'est la charnière que WhatsApp lit comme une signature.
    """
    pris: dict[str, set[int]] = {}
    for rang, lead in enumerate(leads):
        pris.setdefault(lead.angle, set()).add(rang % 49)
        lead.lignes = compose(lead, triple(rang % 49, lead.angle)).splitlines()

    for _ in range(3):
        soucis = juge(leads)
        if not soucis:
            break
        for lead in leads:
            if lead.slug not in soucis:
                continue
            depart = list(lead.lignes)
            libres = [r for r in range(49) if r not in pris[lead.angle]]
            for r in libres[:49]:
                lead.lignes = compose(lead, triple(r, lead.angle)).splitlines()
                if lead.slug not in juge(leads):
                    pris[lead.angle].add(r)
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
    ap.add_argument("--verif", default="",
                    help="VERIF-*.json : ne garder que les pistes à 3/3 (le droit d'écrire, pas le texte)")
    ap.add_argument("--ecarter", default="",
                    help="VERIF-*.json : écarter seulement les numéros morts et les cabinets déjà pourvus "
                         "d'un site ; les 2/3 et les 1/3 restent, avec leur porte A à fermer à l'envoi")
    ap.add_argument("--deja", nargs="*", default=[],
                    help="lots déjà écrits : leurs numéros sortent du calcul")
    a = ap.parse_args()

    fautes = verifie_reservoirs()
    if fautes:
        raise SystemExit("réservoir refusé :\n  " + "\n  ".join(fautes))

    leads = lit_crm(Path(a.crm))
    if a.verif:
        import json
        v = json.loads(Path(a.verif).read_text(encoding="utf-8"))
        permis = {x["num"] for x in v if x.get("verdict") == "ENVOYER"}
        avant = len(leads)
        leads = [l for l in leads if l.numero in permis]
        print(f"Filtre `--verif` : {len(leads)} ligne(s) sur {avant} ont les trois portes (§8b).")
    if a.ecarter:
        avant = len(leads)
        leads, ecartes = ecarte(leads, Path(a.ecarter))
        print(f"Filtre `--ecarter` : {len(ecartes)} ligne(s) sur {avant} écartée(s) — numéro mort "
              f"ou site déjà en ligne : " + ", ".join(l.nom for l in ecartes[:6])
              + ("…" if len(ecartes) > 6 else ""))
    if a.angle:
        leads = [l for l in leads if l.angle == a.angle]
    if a.deja:
        pris: set[str] = set()
        for f in a.deja:
            p = Path(f)
            if p.exists():
                pris |= {numero(m.phone) for m in parse(p)}
        leads = [l for l in leads if l.numero not in pris]

    if not a.verif and not a.ecarter:
        v = RACINE / "leads" / f"VERIF-{a.date or '2026-10-27'}.json"
        if v.exists():
            print(f"⚠ aucun filtre de vérification : `{v.name}` existe et n'est pas lu.")
            print("  Un texte propre n'est pas un droit d'écrire — passer `--ecarter` (ou `--verif`).")

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
