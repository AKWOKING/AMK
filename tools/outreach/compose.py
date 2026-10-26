#!/usr/bin/env python3
"""compose — la fabrique des messages froids, quand le volume dépasse la main.

Pourquoi ce fichier existe
--------------------------
Le 26/10, King renverse la cadence : « we can't be sending just 1 message per day, we send between
20-50 ». Le lot du 24/10 était écrit à la main — sept messages, trois heures. À quarante par jour, la
main ne suit pas, et la solution évidente (un gabarit et un prénom) est exactement ce que WhatsApp
sanctionne : **le texte identique répété est la signature d'un compte qui diffuse**.

Ce fichier est donc une fabrique, pas un gabarit :

  1. il **refuse** d'écrire un message dont le fait manque dans le CRM — aucun fait inventé ;
  2. il choisit l'angle que les faits autorisent : *le nom* (deux noms pour un cabinet) ou *l'offre*
     (la page d'un opticien d'ici, en ligne et montrable) — jamais un angle sans preuve ;
  3. il assemble quatre phrases tirées de quatre réserves, puis **vérifie chaque message avec l'aune
     de `audit_outreach`** : longueur, séquence de douze mots, recouvrement — et écarte les
     assemblages qui ne tiennent pas ;
  4. il écrit au format de la porte, pour que `audit_outreach --strict` juge le lot entier.

Pourquoi des phrases courtes
----------------------------
Une phrase fixe de plus de onze mots contient à elle seule une séquence de douze mots : si elle revient
cinq fois dans le lot, le lot est un gabarit. En gardant chaque phrase sous onze mots (neuf pour celles
du milieu), la fenêtre de douze mots traverse forcément deux phrases — et la fabrique s'arrange pour
qu'aucune paire voisine ne se répète. C'est la seule raison d'écrire court ; le style suit.

Ce qu'il ne fait pas
--------------------
Il ne sait pas si le numéro joint WhatsApp (§8b porte A) : c'est `scout.py verify`, avec la capture
datée de King. Il n'envoie rien : le message part de son téléphone, un par un.

Usage
-----
    python3 tools/outreach/compose.py plan --volume 40
    python3 tools/outreach/compose.py write --out sales/ENVOI-VOLUME-2026-10-27.md \\
        --limit 49 --split 20,29 --deja sales/ENVOI-VAGUE-2-2026-10-26.md
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "tools/qa"))
from audit_outreach import SEQ, SHINGLE, _n_grams, words  # noqa: E402  — l'aune du lot

MAX_FIXE = 11       # mots hors nom propre : au-delà, une phrase se répète comme un gabarit
MAX_MILIEU = 9      # une phrase du milieu, plus courte, laisse la fenêtre de douze mots mordre après
TAILLE = 7          # variantes par phrase
MIN_MOTS = 35       # plancher de CLIENT-MESSAGING-RULES §13
JACCARD_MAX = 0.28  # sous le seuil d'alerte de la porte (§10), avec une marge


# ── les réserves ─────────────────────────────────────────────────────────────────────────────────
#
# Le nom de l'établissement apparaît une fois — dans la première phrase. Un message qui le répète
# quatre fois se lit comme un publipostage, et c'est précisément ce que King a refusé le 24/10.

NOM_S1 = [
    "Bonjour, à {q} votre compte professionnel s'appelle « {p} ».",
    "Bonjour, à {q} vous apparaissez sous « {p} » sur WhatsApp.",
    "Bonjour, à {q} votre profil affiche « {p} », et rien de plus.",
    "Bonjour, à {q} le téléphone dit « {p} » quand on vous cherche.",
    "Bonjour, à {q} je lis « {p} » sur votre compte pro.",
    "Bonjour, à {q} vos clients voient « {p} », pas votre enseigne.",
    "Bonjour, à {q} le nom sur votre profil est « {p} » seul.",
]
NOM_S2 = [
    "Au tableau de l'Ordre, vous êtes « {s} ».",
    "L'Ordre, lui, vous inscrit « {s} ».",
    "Le tableau de l'Ordre dit « {s} ».",
    "Votre inscription au tableau porte « {s} ».",
    "Sur le registre de l'Ordre, c'est « {s} ».",
    "Le tableau vous nomme « {s} », pas autrement.",
    "Et l'Ordre vous enregistre sous « {s} ».",
]
NOM_S3 = [   # dédouanement + conséquence, neuf mots au plus, aucun début ni fin ne se répète
    "Ce n'est pas votre travail : le patient cherche.",
    "Deux noms, et ce n'est pas votre faute.",
    "Aucun reproche : ce n'est pas votre page.",
    "Franchement, ce n'est pas votre faute, mais le nom.",
    "Personne ne blâme : ce n'est pas votre cas.",
    "Le nom change, et ce n'est pas votre travail.",
    "Vraiment, ce n'est pas votre travail, c'est le nom.",
]
NOM_Q = [
    "Dites-moi en un mot : lequel vos clients prononcent ?",
    "Un mot suffit : lequel je retiens ?",
    "Répondez par un mot : lequel vous voulez écrire ?",
    "Dites-moi, en un mot : lequel vos patients utilisent ?",
    "Un mot : lequel vous voulez garder ?",
    "Dites-moi juste un mot : lequel vous préférez ?",
    "Vous me dites un mot : lequel je garde ?",
]

# Angle « offre » — rien n'est affirmé sur le prospect, donc rien à dédouaner. On offre un travail qui
# existe déjà : la page d'un opticien de Douala, en ligne (`dmoptiquesarl.com`, client payant).
OFFRE_S1 = [
    "Bonjour, à {q} vous êtes {s}, et je passais par là.",
    "Bonjour, à {q} je vois {s} dans l'annuaire des pros.",
    "Bonjour, {s} : à {q}, j'ai quelque chose à vous montrer.",
    "Bonjour, vous êtes {s} à {q}, si je ne me trompe.",
    "Bonjour, à {q} je travaille pour les opticiens de la ville.",
    "Bonjour, {s} : à {q}, deux minutes de votre temps suffisent.",
    "Bonjour, à {q}, {s} — je passais par votre nom ce matin.",
]
OFFRE_S2 = [   # chaque variante finit autrement après {o} : c'est la charnière qui compte
    "J'ai fait la page {o}.",
    "Cette page {o} tourne.",
    "C'est la page {o}, prête.",
    "Voilà la page {o}, en ligne.",
    "Et la page {o} existe.",
    "Une page {o} tourne aussi.",
    "Cette page {o} est ici.",
]
OFFRE_S3 = [
    "Je peux vous envoyer le lien, sans rien préparer.",
    "Je vous l'envoie : vous regardez sur votre téléphone.",
    "Le lien part quand vous voulez, sans condition.",
    "Vous l'ouvrez sur votre téléphone, et vous jugez.",
    "Cinq minutes sur votre téléphone, et vous verrez.",
    "Je vous le transmets, vous comparez avec la vôtre.",
    "Vous regardez tranquillement, quand vous avez le temps.",
]
OFFRE_Q = [
    "Dites-moi en un mot : je vous l'envoie ?",
    "Un mot suffit : vous voulez que je vous l'envoie ?",
    "Répondez par un mot : je vous le transmets ?",
    "Un mot, un seul : vous voulez voir ?",
    "Un mot : je vous montre le lien ?",
    "Dites-moi juste un mot : je l'envoie ce soir ?",
    "Vous me dites un mot : je vous le partage ?",
]

RESERVES = {"nom": (NOM_S1, NOM_S2, NOM_S3, NOM_Q),
            "offre": (OFFRE_S1, OFFRE_S2, OFFRE_S3, OFFRE_Q)}


# ── les faits, et le refus d'écrire sans eux ─────────────────────────────────────────────────────

def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def tokens(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", fold(s)) if len(t) > 2}


def meme_nom(a: str, b: str) -> bool:
    """Deux libellés désignent-ils le même établissement ? (Jaccard sur les mots utiles.)"""
    na, nb = re.sub(r"[^a-z0-9]", "", fold(a)), re.sub(r"[^a-z0-9]", "", fold(b))
    if na == nb or (na and nb and (na in nb or nb in na)):
        return True          # « Bellevue Optique » et « bellevueoptique » : le même nom, sans espace
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return True
    return len(ta & tb) / len(ta | tb) >= 0.5


OBJETS = [
    (r"optic|optique|lunett", "d'un opticien de Douala"),
    (r"labo|analyse|biolog", "d'un laboratoire de Douala"),
    (r"clinique|polyclinique|centre m|hôpital|hopital|médic|medic", "d'une clinique de Douala"),
    (r"collège|college|école|ecole|school|lycée|lycee|universit", "d'une école de Douala"),
]


def objet(nom: str) -> str:
    """Ce dont on parle dans l'offre. Chaque métier a une page réelle dans le dépôt : un opticien
    (`dmoptiquesarl.com`, client payant), une clinique (`hosting/samples/clinic-bonaberi.html`), une
    école (`hosting/samples/mitoc.html`), un laboratoire (`hosting/previews/labiomed/`). Offrir une
    page de laboratoire à une école serait la faute la plus visible du lot."""
    for motif, phrase in OBJETS:
        if re.search(motif, fold(nom)):
            return phrase
    return "d'un cabinet de Douala"


def quartier(ville: str) -> str:
    """« Douala (Akwa) » → « Akwa » : le quartier est ce qui fait ouvrir le message (§1①)."""
    m = re.search(r"\(([^)]+)\)", ville or "")
    q = m.group(1) if m else (ville or "")
    q = re.split(r"[,+/]", q)[0].strip()
    if not q or q.lower() == "douala" or len(q.split()) > 3:
        return "Douala"
    return q


@dataclass
class Lead:
    cle: str
    nom: str
    quartier: str
    numero: str
    profil: str
    stage: str
    contacte: str
    objet: str = ""

    @property
    def offre(self) -> str:
        return self.objet or objet(self.nom)

    @property
    def angle(self) -> str | None:
        if self.profil and not meme_nom(self.profil, self.nom):
            return "nom"
        if self.nom and self.quartier:
            return "offre"
        return None


def lit_crm(chemin: Path) -> list[Lead]:
    out: list[Lead] = []
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            g = lambda k: (r.get(k) or "").strip()  # noqa: E731
            out.append(Lead(cle=g("slug"), nom=g("School"), quartier=quartier(g("City")),
                            numero=g("wa_number") or g("Phone"),
                            profil=g("profile_name_seen"), stage=g("stage"), contacte=g("Contacted"),
                            objet=objet(g("School"))))
    # L'ID du CRM n'est pas une clé : 152 lignes sur 190 n'en ont pas (constaté le 26/10). On identifie
    # par le slug, et on suffixe les collisions pour que deux messages ne se confondent jamais.
    vus: dict[str, int] = {}
    for l in out:
        base = l.cle or re.sub(r"[^a-z0-9]+", "-", fold(l.nom) + "-" + l.numero).strip("-")
        vus[base] = vus.get(base, 0) + 1
        l.cle = base if vus[base] == 1 else f"{base}-{vus[base]}"
    return out


def joignable(l: Lead) -> bool:
    """Ce qu'il faut pour qu'un message puisse partir : neuf chiffres, et une ligne jamais touchée."""
    if len(re.sub(r"\D", "", l.numero)) != 9:
        return False
    if l.contacte.lower().startswith("y"):
        return False
    return l.stage in ("prospecting", "parked")


def portes(leads: list[Lead]) -> dict[str, int]:
    """Le nombre de portes §8b que la piste franchit — lu par `scout.py`, jamais deviné ici."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import scout
        return {p.numero: p.portes for p in scout.lit_crm()}
    except Exception:  # noqa: BLE001 — sans le vérificateur, on n'ordonne pas, on n'invente pas
        return {}


def selection(leads: list[Lead], angle: str | None = None) -> list[Lead]:
    """L'ordre est un ordre de preuve : les portes franches d'abord, puis les opticiens.

    Un numéro dont King a vu le profil le 25/10 n'a pas le même coût qu'un numéro d'annuaire : le
    premier part sans vérification, le second demande huit secondes avant l'envoi. Mettre les portes
    devant, c'est dire à King où son temps est déjà dépensé.
    """
    optique = re.compile(r"optic|optique|lunett|vision", re.I)
    dispo = [l for l in leads if joignable(l) and l.angle and (angle is None or l.angle == angle)]
    p = portes(dispo)
    dispo.sort(key=lambda l: (-p.get(l.numero, 0), not optique.search(l.nom), l.angle != "nom", l.cle))
    return dispo


def doublons(leads: list[Lead]) -> list[tuple[str, list[str]]]:
    """Deux lignes, un seul numéro : à quarante messages par jour, c'est deux fois le même."""
    par_num: dict[str, list[str]] = {}
    for l in leads:
        par_num.setdefault(re.sub(r"\D", "", l.numero), []).append(l.nom)
    return [(n, noms) for n, noms in par_num.items() if len(noms) > 1]


def verifie_reserves() -> list[str]:
    """La réserve peut-elle produire un lot sans motif répété ? Quatre conditions, vérifiées ici.

    1. une phrase **fixe** de plus de onze mots contient à elle seule une séquence de douze mots ;
    2. une phrase qui suit une autre doit se distinguer dès ses **cinq premiers mots**, sinon la
       charnière « fin de la précédente + début de celle-ci » se répète d'un message à l'autre ;
    3. et finir par cinq mots différents, pour la même raison, côté sortie ;
    4. les phrases du milieu tiennent sous **neuf** mots : c'est ce qui garantit que la fenêtre de
       douze mots mord assez loin dans la phrase suivante pour que sa charnière la distingue.
    """
    fautes: list[str] = []
    for angle, pools in RESERVES.items():
        for pi, pool in enumerate(pools):
            debuts: dict[tuple, int] = {}
            fins: dict[tuple, int] = {}
            dernier = pi == len(pools) - 1
            plafond = MAX_FIXE if (pi == 0 or dernier) else MAX_MILIEU
            for t in pool:
                # même découpage que la porte : la ponctuation compte comme un jeton
                fixe = fold(t.replace("{s}", "").replace("{p}", "").replace("{q}", "")
                             .replace("{o}", "page")).split()
                if len(fixe) > plafond:
                    fautes.append(f"{angle} P{pi} : {len(fixe)} mots (plafond {plafond}) — {t}")
                if pi:
                    debuts[tuple(fixe[:5])] = debuts.get(tuple(fixe[:5]), 0) + 1
                if not dernier:
                    fins[tuple(fixe[-5:])] = fins.get(tuple(fixe[-5:]), 0) + 1
            for cle, n in debuts.items():
                if n > 1:
                    fautes.append(f"{angle} P{pi} : deux phrases commencent par « {' '.join(cle)} »")
            for cle, n in fins.items():
                if n > 1:
                    fautes.append(f"{angle} P{pi} : deux phrases finissent par « {' '.join(cle)} »")
    return fautes


# ── l'assemblage ────────────────────────────────────────────────────────────────────────────────

def _phrases(lead: Lead, idx: tuple[int, ...]) -> list[str]:
    p = RESERVES[lead.angle]  # type: ignore[index]
    return [p[i][j].format(q=lead.quartier, p=lead.profil, s=lead.nom, o=lead.offre)
            for i, j in enumerate(idx)]


def _corps(lead: Lead, idx: tuple[int, ...]) -> str:
    return "\n".join(_phrases(lead, idx))


def _assemblages(n: int) -> list[tuple[int, ...]]:
    """n quadruplets d'indices tels que **deux messages ne partagent jamais deux phrases**.

    Construction : (x, y, x+y, x+2y) modulo 7 — un code de Reed-Solomon sur un corps de sept éléments.
    Toutes les projections sur deux coordonnées y sont distinctes, donc deux messages du lot ont au
    plus une phrase en commun. C'est la seule raison de cette formule ; elle n'a rien de mystique.
    """
    if n > 49:
        raise ValueError("la fabrique plafonne à 49 messages par lot — au-delà, il faut étendre la "
                         "réserve ou faire deux lots d'un jour chacun")
    couples = [(x, y) for x in range(TAILLE) for y in range(TAILLE)]
    couples.sort(key=lambda xy: ((xy[0] * 3 + xy[1] * 5) % 7, xy[1], xy[0]))
    return [(x, y, (x + y) % TAILLE, (x + 2 * y) % TAILLE) for x, y in couples[:n]]


def assemble(leads: list[Lead]) -> dict[str, str]:
    """Place les messages un par un : le premier assemblage qui ne ressemble à aucun autre."""
    dispos = _assemblages(len(leads))
    pris: set[int] = set()
    corps: dict[str, str] = {}
    seqs: list[set[tuple[str, ...]]] = []
    shingles: list[set[tuple[str, ...]]] = []

    for lead in leads:
        choix = None
        for rang, idx in enumerate(dispos):
            if rang in pris:
                continue
            body = _corps(lead, idx)
            if not (MIN_MOTS <= len(words(body)) <= 55):
                continue
            grammes = _n_grams(body, SEQ)
            if any(grammes & autre for autre in seqs):
                continue
            sh = _n_grams(body, SHINGLE)
            if any((sh | autre) and len(sh & autre) / len(sh | autre) >= JACCARD_MAX for autre in shingles):
                continue
            choix = (rang, body, grammes, sh)
            break
        if choix is None:      # aucune place propre : on prend la première libre, la porte jugera
            rang = next(r for r in range(len(dispos)) if r not in pris)
            body = _corps(lead, dispos[rang])
            choix = (rang, body, _n_grams(body, SEQ), _n_grams(body, SHINGLE))
        pris.add(choix[0])
        corps[lead.cle] = choix[1]
        seqs.append(choix[2])
        shingles.append(choix[3])
    return corps


# ── les sorties ─────────────────────────────────────────────────────────────────────────────────

def plan(leads: list[Lead], volume: int) -> str:
    dispo = selection(leads)
    par_angle: dict[str, int] = {}
    for l in dispo:
        par_angle[l.angle] = par_angle.get(l.angle, 0) + 1
    jours = len(dispo) / volume if volume else 0
    return "\n".join([
        f"Stock envoyable : {len(dispo)} messages  (angle « nom » {par_angle.get('nom', 0)}"
        f" · angle « offre » {par_angle.get('offre', 0)})",
        f"À {volume}/jour, le stock tient {jours:.1f} jour(s) — puis il faut de nouvelles lignes.",
        "",
        "Autre contrainte : la porte A (§8b) n'est ouverte que pour les lignes dont King a vu le profil",
        "WhatsApp. Les autres partent quand même, mais leur numéro n'est pas prouvé vivant — 68 % des",
        "numéros d'annuaire l'étaient en septembre (leçon du 19/09).",
        "",
        f"Numéros en double dans le stock : {len(doublons(dispo))} — la fabrique garde la première ligne "
        "et écarte la seconde (deux fois le même message = un blocage).",
    ])


def deja_envoyes(chemin: Path) -> set[str]:
    """Les numéros déjà écrits dans un lot précédent — on ne double jamais un envoi."""
    from audit_outreach import parse
    if not chemin.exists():
        return set()
    return {re.sub(r"\D", "", m.phone) for m in parse(chemin)}


def write(leads: list[Lead], out: Path, limit: int, titre: str, offset: int = 0,
          split: list[int] | None = None) -> int:
    fautes = verifie_reserves()
    if fautes:
        raise SystemExit("réserve refusée :\n  " + "\n  ".join(fautes))
    choisis = selection(leads)[offset:offset + limit]
    if not choisis:
        raise SystemExit("aucune ligne composable — voir `plan`")
    doubl = doublons(choisis)
    if doubl:
        vus: set[str] = set()
        garde = []
        for l in choisis:
            n = re.sub(r"\D", "", l.numero)
            if n in vus:
                continue
            vus.add(n)
            garde.append(l)
        print(f"{len(choisis) - len(garde)} ligne(s) écartée(s) pour numéro en double : "
              + " · ".join(", ".join(v) for _, v in doubl))
        choisis = garde

    corps = assemble(choisis)
    blocs = [f"# {titre}", "",
             "> Généré par `tools/outreach/compose.py` depuis `leads/CRM.csv` (lecture seule).",
             "> Chaque message ne dit que ce que sa ligne prouve. Porte : `audit_outreach.py --strict`.",
             ""]
    jour = 0
    for rang, l in enumerate(choisis, 1):
        if split:
            bornes = [sum(split[:k + 1]) for k in range(len(split))]
            while jour < len(bornes) - 1 and rang > bornes[jour]:
                jour += 1
            if rang == (bornes[jour - 1] + 1 if jour else 1):
                blocs += ["", f"## Jour {jour + 1}", ""]
        blocs.append(f"**#{rang} {l.nom} — {l.quartier} — {l.numero}**")
        blocs += ["> " + x for x in corps[l.cle].splitlines()]
        blocs.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(blocs), encoding="utf-8")
    return len(choisis)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["plan", "write", "check"])
    ap.add_argument("--crm", default=str(RACINE / "leads/CRM.csv"))
    ap.add_argument("--out", default="")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--volume", type=int, default=40)
    ap.add_argument("--angle", choices=["nom", "offre"], default=None)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--deja", default="", help="lot déjà écrit : ses numéros sont exclus")
    ap.add_argument("--split", default="", help="répartition en jours, ex. 20,29")
    args = ap.parse_args()

    if args.action == "check":
        fautes = verifie_reserves()
        print("\n".join(fautes) if fautes else "réserve OK — aucun motif ne peut se répéter")
        return 1 if fautes else 0

    leads = lit_crm(Path(args.crm))
    if args.deja:
        pris = deja_envoyes(Path(args.deja))
        leads = [l for l in leads if re.sub(r"\D", "", l.numero) not in pris]
    if args.angle:
        leads = [l for l in leads if l.angle == args.angle]

    if args.action == "plan":
        print(plan(leads, args.volume))
        return 0
    if not args.out:
        raise SystemExit("--out est obligatoire pour `write`")
    split = [int(x) for x in args.split.split(",") if x.strip()] if args.split else None
    n = write(leads, Path(args.out), args.limit, f"Vague volume — {args.limit} messages",
              args.offset, split)
    print(f"{n} message(s) écrits → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
