#!/usr/bin/env python3
"""machine — le cockpit du dépôt : où j'en suis, ce que je lis, ce que je lance, quand c'est fini.

Ce script ne dit aucune règle métier. Il dit l'ordre (huit étapes), l'état réel (git, graphe,
audit, handoff, outils), et il renvoie au document qui tranche. La carte complète : `ops/MACHINE.md`.

    python3 tools/ops/machine.py                # le cockpit
    python3 tools/ops/machine.py 2              # la fiche de l'étape 2
    python3 tools/ops/machine.py --who prix     # qui tranche ce sujet
    python3 tools/ops/machine.py --check        # code 1 si une porte dure est fermée
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "ops" / "REPO-MAP.md"
STAMPS = Path.home() / ".amk-provisioned"
SKILLS = Path.home() / ".claude" / "skills"

# ─────────────────────────────────────────────────────────── les huit étapes
STAGES = [
    dict(
        id=0, name="Réveil", alias=["reveil", "wake", "arbre"],
        question="L'arbre que je lis est-il le vrai dépôt ?",
        lis=["ops/GIT-STABILITY-NOTE.md (§ du 22/10)"],
        lance=["python3 tools/ops/wake.py", "python3 tools/ops/wake.py --check"],
        produit="un arbre au sommet distant, ou une réparation faite et dite",
        fini="`wake.py --check` sort en code 0.",
        pourquoi="22/10 : quatre fois dans la journée, le travail local a disparu et deux affirmations "
                 "fausses ont été publiées (« le catalogue est vide », « la semaine 3 est bloquée »).",
    ),
    dict(
        id=1, name="Cadrage", alias=["cadrage", "demande", "ruling"],
        question="Que demande King, et qu'est-ce qui est déjà tranché ?",
        lis=["PRE-FLIGHT.md §0 à §5 (couche 1 de §0f)",
             "knowledge/HOUSE-KNOWLEDGE-BASE.md (la couche de référence)",
             "le dossier client s'il y en a un : clients/<slug>/dossier.md"],
        lance=["bash tools/ops/machine.sh --who <sujet>   # qui tranche, avant de discuter"],
        produit="la demande en une phrase + les rulings concernés, cités par chemin",
        fini="la réponse peut nommer le document qui gouverne la demande — ou dire qu'il n'existe pas.",
        pourquoi="une demande appliquée à moitié vient presque toujours d'un ruling non relu. "
                 "Skill `brainstorming` (tools/superpowers) quand la demande est ouverte.",
    ),
    dict(
        id=2, name="Lecture", alias=["lecture", "graphe", "regle"],
        question="Quelle règle gouvernait déjà ce sujet ?",
        lis=["ops/REPO-MAP.md §0 (chiffres) · §6 (routage) · §2 (squelette) · §1 (knowledge) · §3 bis (orphelins)",
             "ops/REPO-MAP.md §3 (périmé mais encore cité = consigne morte)"],
        lance=["bash tools/graphify/install.sh",
               "python3 tools/graphify/build_full_graph.py",
               'bash tools/graphify/ask.sh "message prospect clinique" --top 8'],
        produit="la liste des fichiers LUS et des fichiers LISTÉS NON LUS, en tête de réponse",
        fini="aucune règle citée ne vient de mémoire ; chaque affirmation a un chemin.",
        pourquoi="24/10 : messages d'approche réécrits sans knowledge/OUTREACH-MESSAGING ni "
                 "sales/RESEARCH-STANDARD §10 — deux règles existaient, aucune n'a été lue.",
    ),
    dict(
        id=3, name="Plan", alias=["plan", "ordre", "fichiers"],
        question="Quels fichiers, dans quel ordre, et à quoi je verrai que c'est fini ?",
        lis=["PRE-FLIGHT.md §0d (décision → fichiers touchés)",
             "ops/templates/ (gabarit de tâche par livrable)"],
        lance=["skills writing-plans → executing-plans (tools/superpowers)"],
        produit="3 à 8 lignes, chaque ligne avec sa porte",
        fini="le plan dit ce qui est touché, ce qui ne l'est pas, et ce qui prouvera que c'est fini.",
        pourquoi="13/10 : une refonte partie d'un fichier en a touché douze sans que personne ne l'ait décidé. "
                 "Déclencheur : plus d'un fichier, ou plus d'un commit.",
    ),
    dict(
        id=4, name="Exécution", alias=["execution", "outil", "build"],
        question="Quel outil fait ce travail — et est-il installé, épinglé, jugé ?",
        lis=["ops/TOOL-SCAN.md (le verdict de l'outil, et sa limite dite)",
             "tools/<domaine>/README.md (la façon d'appeler)"],
        lance=["bash tools/ops/provision.sh --list   # ce qui est réellement installé cette session",
               "bash tools/ops/provision.sh --only <outil>   # si absent"],
        produit="les fichiers et les artefacts, plus la commande exacte qui les a produits",
        fini="chaque outil utilisé a une entrée TOOL-SCAN ; aucun outil non jugé n'a tourné.",
        pourquoi="19/10 : un outil exécuté sans jugement, un autre jamais réutilisé alors qu'il était installé.",
    ),
    dict(
        id=5, name="Preuve", alias=["preuve", "porte", "qa", "verification"],
        question="Qu'est-ce qui prouve que c'est fait ?",
        lis=["AGENTS.md §5 (ce que les portiques ne voient pas)",
             "tools/qa/PROTOCOLE-LECTEUR-ECRAN.md (ce qui doit être vu, à la main)"],
        lance=["bash tools/ops/gate-dm.sh [fichier]        # contenu client DM",
               "bash tools/ops/gate-amk.sh                  # pages AMK et pages de niche",
               "python3 tools/qa/audit_claims.py <fichier>  # prix, cardinaux, promesses",
               "python3 tools/qa/audit_delivery.py --strict <dossier>",
               "python3 tools/ops/audit_files.py            # doublons, orphelins, caches"],
        produit="la sortie de la porte, recopiée dans la réponse (jamais « c'est bon » tout seul)",
        fini="un code retour et une ligne de résultat sont cités ; ce qui n'a pas été vérifié est dit.",
        pourquoi="17/09 : une vidéo publiée avec une ouverture figée — le portique existait, il n'a pas été lancé. "
                 "skill verification-before-completion.",
    ),
    dict(
        id=6, name="Mémoire", alias=["memoire", "journal", "log", "notion"],
        question="Où est-ce écrit pour la session qui ne se souvient de rien ?",
        lis=["ops/HANDOFF-<date>.md (le plus récent)",
             "PRE-FLIGHT.md §0g (Notion = miroir, le dépôt fait loi)"],
        lance=["python3 tools/graphify/build_full_graph.py   # si un fichier a été créé",
               "python3 tools/ops/audit_files.py"], 
        produit="1 à 3 lignes datées dans le bon fichier : Activity-Log (envoi), TOOL-SCAN (outil), "
                "registre d'unicité (design), HANDOFF (état), Notion (miroir)",
        fini="un tour futur retrouve le fait sans avoir à demander.",
        pourquoi="18/09 : un résumé annonçait « OraCare et MITOC ont répondu » — c'était faux. "
                 "La mémoire avait remplacé le journal ; sales/Activity-Log.md existe pour ça.",
    ),
    dict(
        id=7, name="Sortie", alias=["sortie", "push", "commit", "git"],
        question="Est-ce poussé ?",
        lis=["PRE-FLIGHT.md §1i (seuils de fusion : 3 000 lignes / 40 fichiers / 6 tours)"],
        lance=["git status --short", "git push origin <branche>", "python3 tools/ops/wake.py --check"],
        produit="un commit poussé, une branche à jour",
        fini="le distant contient le travail ; un clone neuf le verrait.",
        pourquoi="22/10 : un lot fini, jamais poussé, effacé au réapprovisionnement suivant.",
    ),
]

# ─────────────────────────────────────────────── qui tranche quoi (miroir de MACHINE.md §5)
REGISTRY = [
    dict(subject="message à froid, relance, prospection", alias=["message", "relance", "cold", "outreach", "prospect"],
         doc="knowledge/OUTREACH-MESSAGING-2026-10-22.md", rules="gold",
         decides="la structure en quatre temps, le dédouanement, la sortie sans friction",
         not_decides="la liste des cibles (leads/, leads/CRM.csv)",
         gate="tools/qa/audit_claims.py", when="avant tout envoi"),
    dict(subject="chiffre, source, tier de preuve", alias=["chiffre", "stat", "source", "etude", "research"],
         doc="sales/RESEARCH-STANDARD.md §10", rules="gold",
         decides="ce qui est citable, quel tier, ce qui est déjà réfuté",
         not_decides="la formulation",
         gate="— (lecture seule : aucun outil ne juge une source)", when="avant toute statistique citée"),
    dict(subject="prix, offre, récurrence", alias=["prix", "price", "offre", "tarif", "remise", "retainer"],
         doc="knowledge/PRIX-2026-10-24.md", rules="gold",
         decides="le socle, l'entretien, ce qui n'est jamais remisé",
         not_decides="ce que le client acceptera (c'est la conversation)",
         gate="— (aucun montant publié, AGENTS.md §3)", when="avant toute conversation d'argent"),
    dict(subject="marque et contenu DM Optique", alias=["dm", "dmoptic", "direction-marque"],
         doc="clients/dm-optic/brand/DIRECTION-MARQUE-v2-2026-10-22.md", rules="gold",
         decides="A moteur, B preuve, C limite — la direction arrêtée le 22/10",
         not_decides="le site AMK",
         gate="bash tools/ops/gate-dm.sh", when="avant d'écrire une ligne DM"),
    dict(subject="unicité d'un design", alias=["design", "unicite", "mockup", "page", "hero"],
         doc="clients/_uniqueness-registry.md", rules="gold",
         decides="quelle empreinte visuelle est déjà prise (15 designs, 3 clients vivants)",
         not_decides="le goût de King",
         gate="PRE-FLIGHT.md §2 (protocole, avant la première ligne de HTML)", when="avant tout build de page"),
    dict(subject="verrous client : prix, montures, visages, claims", alias=["verrou", "claim", "monture", "visage"],
         doc="AGENTS.md §3", rules="gold",
         decides="les interdits de publication, client par client",
         not_decides="—",
         gate="tools/qa/audit_claims.py", when="avant publication"),
    dict(subject="SEO, AEO, découvrabilité", alias=["seo", "aeo", "google", "llms"],
         doc="AMK-SEO-PLAYBOOK.md", rules="gold",
         decides="la méthode SEO et ce que Google dit de ne pas faire",
         not_decides="le contenu éditorial (contenu = CONTENT-CREATION)",
         gate="tools/qa/audit_seo.py · audit_aeo.py", when="avant déploiement"),
    dict(subject="vidéo, montage, publication", alias=["video", "montage", "mp4", "tiktok"],
         doc="knowledge/VIDEOS-2026-10-23-AUDIT.md", rules="gold",
         decides="ce qu'on garde, ce qu'on corrige, ce qu'on jette",
         not_decides="le rendu final — King le voit sur son téléphone",
         gate="audit_video_motion.py · audit_render_freshness.py", when="avant toute publication"),
    dict(subject="cadence de publication", alias=["cadence", "calendrier", "planning"],
         doc="ops/CADENCE-PUBLICATION-2026-10-22.md", rules="gold",
         decides="quel jour, quel canal, quelle pièce",
         not_decides="le calendrier promis au client",
         gate="—", when="chaque lundi"),
    dict(subject="les cinq phases d'un engagement", alias=["lifcycle", "lifecycle", "engagement", "client"],
         doc="ops/LIFECYCLE.md", rules="gold",
         decides="Intake → Strategy → Production → Review → Delivery, et ce qui ferme chaque phase",
         not_decides="le prix, l'angle, le design (chacun a son document)",
         gate="gate-dm.sh / gate-amk.sh", when="à chaque phase"),
    dict(subject="les outils et les skills", alias=["outil", "tool", "skill", "install"],
         doc="ops/TOOL-SCAN.md", rules="gold",
         decides="ce qui entre, pourquoi, à quel prix, avec quelle limite",
         not_decides="le code de l'outil (on ne le modifie pas)",
         gate="bash tools/ops/provision.sh --list", when="avant d'installer, et à chaque session"),
    dict(subject="la carte du dépôt", alias=["carte", "graphe", "map", "graphify"],
         doc="ops/REPO-MAP.md (généré, jamais édité)", rules="gold",
         decides="ce qui existe, où, et ce que personne ne cite",
         not_decides="la vérité d'une règle — la carte dit où, pas si c'est juste",
         gate="python3 tools/graphify/build_full_graph.py", when="avant d'écrire, et après tout fichier créé"),
    dict(subject="la mémoire des envois et des réponses", alias=["journal", "activity", "envoi", "reponse"],
         doc="sales/Activity-Log.md", rules="gold",
         decides="ce qui a été envoyé, lu, répondu — et ce qui n'a pas été ouvert",
         not_decides="les intentions",
         gate="leads/build/guard.py", when="à chaque envoi, chaque réponse"),
    dict(subject="l'état du travail", alias=["handoff", "etat", "reprise"],
         doc="ops/HANDOFF-<date>.md (le plus récent)", rules="gold",
         decides="où en est le travail, ce qui est décidé, ce qui reste",
         not_decides="—",
         gate="le cockpit affiche son âge (au-delà de 3 jours, il est réécrit)", when="fin de session"),
    dict(subject="git, branches, fusion", alias=["git", "branche", "merge", "pr"],
         doc="PRE-FLIGHT.md §1i", rules="gold",
         decides="quand on fusionne (3 000 lignes / 40 fichiers / 6 tours) et comment",
         not_decides="—",
         gate="python3 tools/ops/wake.py --check", when="à chaque fusion"),
    dict(subject="facturation, contrat, admin fiscal", alias=["facture", "contrat", "fiscal", "niu"],
         doc="ops/FACTURATION-2026-10-24.md", rules="gold",
         decides="les mentions, la numérotation, ce qui est dû",
         not_decides="le prix",
         gate="tools/ops/make_contrat.py · make_recap_dm.py", when="avant tout document financier"),
    dict(subject="la méthode de travail (comment)", alias=["methode", "methode de travail", "plan", "superpowers"],
         doc="tools/superpowers/ (15 skills, using-superpowers en tête)", rules="doc",
         decides="comment travailler : cadrer, planifier, exécuter, relire, vérifier",
         not_decides="nos règles métier — elles sont dans knowledge/ et PRE-FLIGHT",
         gate="—", when="quand la demande est ouverte ou le travail long"),
    dict(subject="le miroir lisible sur téléphone", alias=["notion", "miroir", "backup"],
         doc="PRE-FLIGHT.md §0g (Notion : 4024b1d8-9633-814c-8837-dcbc1b7f28b0)", rules="doc",
         decides="ce qui est recopié, et à quelle fréquence",
         not_decides="RIEN — le dépôt fait loi, Notion est corrigé",
         gate="—", when="quand un fait debout change"),
]

BOLD, DIM, RED, YEL, GRN, CYA, OFF = "\033[1m", "\033[2m", "\033[31m", "\033[33m", "\033[32m", "\033[36m", "\033[0m"
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    BOLD = DIM = RED = YEL = GRN = CYA = OFF = ""


def run(cmd: list[str], timeout: int = 30) -> str:
    try:
        return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def git_state() -> dict:
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "—"
    dirty = run(["git", "status", "--porcelain"])
    ahead = behind = 0
    counts = run(["git", "rev-list", "--left-right", "--count", "@{u}...HEAD"])
    if counts:
        parts = counts.split()
        if len(parts) == 2:
            behind, ahead = int(parts[0]), int(parts[1])
    return dict(branch=branch, dirty=len([l for l in dirty.splitlines() if l.strip()]),
                ahead=ahead, behind=behind)


def newest_source() -> tuple[float, str]:
    """Le fichier suivi le plus récemment modifié, hors sorties régénérables."""
    files = run(["git", "ls-files", "-z"], timeout=60).split("\0")
    # les sorties régénérables ne rendent pas la carte périmée : elles sont des produits, pas des sources
    skip = ("graphify-out/", "ops/REPO-MAP.md", "ops/FILE-AUDIT-", ".git/")
    best, name = 0.0, "—"
    for f in files:
        if not f or f.startswith(skip):
            continue
        try:
            m = (ROOT / f).stat().st_mtime
        except OSError:
            continue
        if m > best:
            best, name = m, f
    for p in ROOT.rglob("*"):
        rel = str(p.relative_to(ROOT))
        if not p.is_file() or ".git" in p.parts or "graphify-out" in p.parts:
            continue
        if rel.startswith(("ops/REPO-MAP.md", "ops/FILE-AUDIT-")):
            continue
        try:
            m = p.stat().st_mtime
        except OSError:
            continue
        if m > best:
            best, name = m, rel
    return best, name


def graph_state() -> dict:
    if not MAP.exists():
        return dict(ok=False, date=None, mtime=0.0, nodes="?", cites="?", orphans="?", stale=True, stale_by=None)
    txt = MAP.read_text(encoding="utf-8", errors="ignore")
    head = txt[:4000]
    nodes = re.search(r"\*\*([\d\s]+) nœuds\*\*", head)
    cites = re.search(r"\*\*([\d\s]+) citations", head)
    orphans = re.search(r"\*\*([\d\s]+) documents que personne ne cite", head)
    m = re.search(r"build_full_graph\.py — (\d{4}-\d{2}-\d{2})", txt)
    mtime = MAP.stat().st_mtime
    newest, newest_file = newest_source()
    stale = newest > mtime + 2
    return dict(ok=True, date=m.group(1) if m else "?", mtime=mtime,
                nodes=(nodes.group(1) if nodes else "?").replace(" ", ""),
                cites=(cites.group(1) if cites else "?").replace(" ", ""),
                orphans=(orphans.group(1) if orphans else "?"),
                stale=stale, stale_by=newest_file if stale else None)


def dated_file(pattern: str) -> tuple[Path | None, int | None]:
    files = sorted(ROOT.glob(pattern))
    if not files:
        return None, None
    f = files[-1]
    m = re.search(r"(\d{4}-\d{2}-\d{2})", f.name)
    if not m:
        age = (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days
        return f, age
    d = date.fromisoformat(m.group(1))
    return f, (date.today() - d).days


def provision_state() -> dict:
    tools = sorted(p.parent.name for p in (ROOT / "tools").glob("*/install.sh"))
    ok = [t for t in tools if (STAMPS / f"{t}.ok").exists()]
    ko = [t for t in tools if (STAMPS / f"{t}.failed").exists()]
    return dict(total=len(tools), ok=ok, ko=ko, missing=[t for t in tools if t not in ok and t not in ko])


def skills_state() -> int:
    try:
        return len([p for p in SKILLS.iterdir() if p.is_dir()])
    except OSError:
        return 0


def cockpit() -> int:
    g = git_state()
    gr = graph_state()
    audit_file, audit_age = dated_file("ops/FILE-AUDIT-*.md")
    handoff_file, handoff_age = dated_file("ops/HANDOFF-*.md")
    prov = provision_state()
    skills = skills_state()
    hard = []

    print(f"{BOLD}LA MACHINE{OFF} — {ROOT.name} · branche {CYA}{g['branch']}{OFF} · {date.today().isoformat()}")
    print(f"{DIM}la carte : ops/MACHINE.md · les 24 outils : bash tools/ops/provision.sh --list{OFF}\n")

    print(f"{BOLD}État{OFF}")
    if g["dirty"]:
        print(f"  {YEL}⚠{OFF}  {g['dirty']} fichier(s) modifié(s) non commité(s)")
    else:
        print(f"  {GRN}✓{OFF}  arbre de travail propre")
    if g["ahead"] or g["behind"]:
        print(f"  {YEL}⚠{OFF}  {g['ahead']} commit(s) d'avance, {g['behind']} de retard sur le distant")
    else:
        print(f"  {GRN}✓{OFF}  branche alignée sur le distant")
    if gr["stale"]:
        print(f"  {RED}⛔{OFF} carte périmée — `{gr['stale_by']}` est plus récent que ops/REPO-MAP.md")
        print(f"     {DIM}→ python3 tools/graphify/build_full_graph.py{OFF}")
        hard.append("carte périmée")
    elif gr["ok"]:
        print(f"  {GRN}✓{OFF}  carte à jour — {gr['nodes']} nœuds, {gr['cites']} citations, "
              f"{gr['orphans']} orphelins ({gr['date']})")
    else:
        print(f"  {RED}⛔{OFF} ops/REPO-MAP.md absent → python3 tools/graphify/build_full_graph.py")
        hard.append("carte absente")
    if audit_age is not None:
        tag = f"{GRN}✓{OFF}" if audit_age <= 7 else f"{YEL}⚠{OFF}"
        print(f"  {tag}  audit des fichiers : {audit_file.name} ({audit_age} j)")
    if handoff_age is not None:
        tag = f"{GRN}✓{OFF}" if handoff_age <= 3 else f"{YEL}⚠{OFF}"
        note = "" if handoff_age <= 3 else " — au-delà de 3 jours, il est réécrit"
        print(f"  {tag}  handoff : {handoff_file.name} ({handoff_age} j){note}")
    if prov["ok"]:
        print(f"  {GRN}✓{OFF}  outils provisionnés : {len(prov['ok'])}/{prov['total']}"
              + (f" · {len(prov['ko'])} en échec" if prov["ko"] else ""))
    else:
        print(f"  {YEL}⚠{OFF}  aucun outil provisionné cette session ({prov['total']} installateurs)")
        print(f"     {DIM}→ bash tools/ops/provision.sh{OFF}")
    print(f"  {GRN}✓{OFF}  skills lisibles : {skills} dans ~/.claude/skills")

    print(f"\n{BOLD}Les huit étapes{OFF} {DIM}(fiche : bash tools/ops/machine.sh <n> · qui tranche : --who <sujet>){OFF}\n")
    for s in STAGES:
        print(f"  {CYA}{s['id']}{OFF}  {s['name']:<10} {DIM}{s['question']}{OFF}")

    print(f"\n{BOLD}Les trois boucles{OFF}")
    print("  tour       0 réveil → 1 cadrage → 2 lecture → 3 plan → 4 exécution → 5 preuve → 6 mémoire → 7 sortie")
    print("  engagement Intake → Strategy → Production → Review → Delivery      (ops/LIFECYCLE.md)")
    print("  actif      entre par un ruling · vit avec un pin · sort par une note datée")

    if hard:
        print(f"\n{RED}PORTE FERMÉE : {', '.join(hard)}{OFF}")
        return 1
    return 0


def card(n: int) -> int:
    s = next((x for x in STAGES if x["id"] == n), None)
    if s is None:
        print(f"étape inconnue : {n} (0 à 7)", file=sys.stderr)
        return 2
    print(f"{BOLD}ÉTAPE {s['id']} · {s['name']}{OFF}")
    print(f"{DIM}{s['question']}{OFF}\n")
    print(f"{BOLD}Lire{OFF}")
    for x in s["lis"]:
        print(f"  · {x}")
    print(f"\n{BOLD}Lancer{OFF}")
    for x in s["lance"]:
        print(f"  $ {x}")
    print(f"\n{BOLD}Produire{OFF}\n  {s['produit']}")
    print(f"\n{BOLD}Fini quand{OFF}\n  {s['fini']}")
    print(f"\n{BOLD}Pourquoi cette étape existe{OFF}\n  {s['pourquoi']}")
    return 0


def who(query: str) -> int:
    q = query.lower().strip()
    scored = []
    for r in REGISTRY:
        hay = (r["subject"] + " " + " ".join(r["alias"])).lower()
        score = sum(1 for w in q.split() if w in hay) + (2 if q in hay else 0)
        if score:
            scored.append((score, r))
    scored.sort(key=lambda t: -t[0])
    if not scored:
        print(f"aucun sujet nommé « {query} » dans la table de propriété (ops/MACHINE.md §5).")
        print(f"→ le sujet est peut-être neuf : bash tools/graphify/ask.sh \"{query}\" --top 8")
        return 1
    for _, r in scored[:3]:
        print(f"{BOLD}{r['subject']}{OFF}")
        print(f"  tranche        {r['doc']}")
        print(f"  décide         {r['decides']}")
        print(f"  ne décide pas  {r['not_decides']}")
        print(f"  vérifié par    {r['gate']}")
        print(f"  intervient     {r['when']}")
        print()
    return 0


def check() -> int:
    gr = graph_state()
    prov = provision_state()
    problems = []
    if not gr["ok"]:
        problems.append("ops/REPO-MAP.md absent")
    elif gr["stale"]:
        problems.append(f"carte périmée ({gr['stale_by']} plus récent)")
    if not prov["ok"]:
        problems.append("aucun outil provisionné cette session → bash tools/ops/provision.sh")
    for p in problems:
        print(f"{RED}⛔{OFF} {p}")
    if problems:
        return 1
    print(f"{GRN}✓{OFF} portes dures ouvertes (carte à jour, outils provisionnés)")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        return cockpit()
    a = argv[0]
    if a in ("-h", "--help"):
        print(__doc__)
        return 0
    if a == "--check":
        return check()
    if a == "--who":
        if len(argv) < 2:
            print("usage : machine.py --who <sujet>", file=sys.stderr)
            return 2
        return who(" ".join(argv[1:]))
    if a == "--json":
        print(json.dumps(dict(
            git=git_state(),
            graph={k: v for k, v in graph_state().items() if k != "stale_by"},
            provision={k: len(v) if isinstance(v, list) else v for k, v in provision_state().items()},
            skills=skills_state(),
        ), ensure_ascii=False, indent=2))
        return 0
    try:
        return card(int(a))
    except ValueError:
        return who(" ".join(argv))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
