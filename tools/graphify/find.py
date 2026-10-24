#!/usr/bin/env python3
"""AMK — `ask.sh` : interroger le graphe du dépôt au lieu de le parcourir à l'œil.

Pourquoi cet outil existe
-------------------------
Le 24/10/2026, deux règles écrites la veille ont été violées en même temps :
`knowledge/OUTREACH-MESSAGING-2026-10-22.md` (à lire avant tout message à un prospect) et
`RESEARCH-STANDARD.md` §10 (qui avait déjà tranché une statistique que j'ai citée comme valide).
Les deux étaient dans le dépôt. Aucune n'a été lue.

Le défaut n'est pas le manque de règles : c'est que **les trouver dépendait de ma mémoire**.
Cet outil rend la recherche mécanique : on lui donne un sujet, il rend les documents classés par
pertinence, avec leurs titres — donc les règles qu'on aurait dû lire, et qu'on peut citer.

Ce qu'il fait, exactement
-------------------------
Il lit `graphify-out/graph.json` (produit par `build_full_graph.py`, local, sans clé d'API) et
compte, pour chaque document :
  · les titres du fichier qui contiennent un des mots cherchés  (signal fort)
  · le nom du fichier lui-même                                 (signal moyen)
  · les liens reçus d'autres documents (degré entrant)          (signal de centralité)
Il n'invente rien : chaque ligne renvoyée est un fichier réel, avec des numéros de ligne réels.

Usage
-----
    bash tools/graphify/install.sh
    python3 tools/graphify/build_full_graph.py
    python3 tools/graphify/find.py "message prospect clinique" --top 8

Sortie : une ligne par document — score, chemin, nombre de titres touchés, extraits.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "graphify-out" / "graph.json"

LAW_NAMES = (
    "RULES", "STANDARD", "PLAYBOOK", "GUIDE", "DECLINAISON", "MESSAGES", "PERSUASION",
    "PRE-FLIGHT", "TOOL-SCAN", "README",
)

STOP = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "ou", "à", "au", "aux", "en", "pour",
    "dans", "sur", "que", "qui", "quoi", "avec", "sans", "par", "ce", "cet", "cette", "il", "elle",
    "on", "nous", "vous", "je", "tu", "se", "sa", "son", "ses", "leur", "the", "a", "of", "to", "in",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s)


def load() -> dict:
    if not GRAPH.exists():
        print(
            "graphify-out/graph.json absent.\n"
            "  bash tools/graphify/install.sh && python3 tools/graphify/build_docs_graph.py",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Cherche les documents du dépôt qui parlent d'un sujet.")
    ap.add_argument("query", nargs="+", help="mots-clés (français ou anglais)")
    ap.add_argument("--top", type=int, default=8, help="nombre de documents affichés (défaut 8)")
    ap.add_argument("--min", type=int, default=1, help="score minimal (défaut 1)")
    args = ap.parse_args()

    words = [w for w in norm(" ".join(args.query)).split() if w and w not in STOP and len(w) > 2]
    if not words:
        print("aucun mot-clé exploitable", file=sys.stderr)
        return 2

    g = load()
    by_file: dict[str, list[dict]] = defaultdict(list)
    for n in g["nodes"]:
        src = n.get("source_file")
        if src:
            by_file[src].append(n)

    # degré entrant : on lit le `source_file` du nœud visé (le graphe complet le porte sur tous
    # les nœuds). L'ancienne version comparait des préfixes et tombait sur un préfixe vide —
    # `.gitignore` sortait « cité 3 055× » et prenait la première place.
    id_to_file = {n["id"]: n["source_file"] for n in g["nodes"] if n.get("source_file")}
    inbound: dict[str, int] = defaultdict(int)
    for e in g.get("edges", []):
        if e.get("relation") in ("references", "mentions", "cites", "supersedes"):
            src = id_to_file.get(e.get("target", ""))
            if src in by_file:
                inbound[src] += 1

    scored = []
    for src, nodes in by_file.items():
        base = norm(Path(src).stem.replace("-", " ").replace("_", " "))
        file_hits = sum(1 for w in words if w in base)
        head_hits, excerpts = 0, []
        for n in nodes:
            if n.get("node_kind") != "heading":
                continue
            label = n.get("label") or ""
            nl = norm(label)
            hit = [w for w in words if w in nl]
            if hit:
                head_hits += 1
                if len(excerpts) < 3:
                    loc = (n.get("source_location") or "").lstrip("L")
                    excerpts.append(f"L{loc} · {label[:96]}")
        # Un journal de 5 000 lignes ne doit pas enterrer une règle de 130 lignes : on divise par la
        # racine de la taille, et on remonte les fichiers qui PORTENT une règle (knowledge/, *RULES*,
        # *STANDARD*, *PLAYBOOK*, *GUIDE*…). Sans ça, `ASK` sur « message prospect » sortait
        # Activity-Log en tête et le fichier de King en 4ᵉ position.
        # Un journal qui touche 32 titres n'est pas plus pertinent qu'une règle qui en touche 2 :
        # on plafonne les titres comptés (6), on divise par la racine de la taille, et on remonte les
        # fichiers qui PORTENT une règle — mais seulement s'ils ont effectivement touché quelque chose.
        total = sum(1 for n in nodes if n.get("node_kind") == "heading") or 1
        if head_hits == 0 and file_hits == 0:
            continue  # aucune trace du sujet dans le fichier : sa centralité ne le rend pas pertinent
        base = min(head_hits, 6) * 3 + file_hits * 2 + min(inbound.get(src, 0), 8)
        score = base / (1 + total / 40) ** 0.5
        # `knowledge/` = la couche qui fait loi (10 documents). Elle est petite, donc elle n'a pas
        # beaucoup de titres : on la remonte franchement — c'est la règle qu'on n'a pas lue le 24/10.
        if src.startswith("knowledge/"):
            score = score * 1.6 + 8
        if any(k in Path(src).name.upper() for k in LAW_NAMES):
            score += 3
        if score >= args.min:
            scored.append((score, src, head_hits, file_hits, inbound.get(src, 0), excerpts))

    scored.sort(key=lambda t: (-t[0], t[1]))
    if not scored:
        print(f"rien pour « {' '.join(words)} » — essayez d'autres mots (ou --min 0)")
        return 4

    print(f"« {' '.join(words)} » — {len(scored)} document(s), les {min(args.top, len(scored))} premiers :\n")
    for score, src, hh, fh, deg, ex in scored[: args.top]:
        print(f"[{score:5.1f}] {src}   (titres {hh} · nom {fh} · cité {deg}×)")
        for e in ex:
            print(f"        {e}")
        print()
    print("→ Ces fichiers se lisent AVANT d'écrire. Ceux qui ne sont pas lus se disent dans l'en-tête pré-vol.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
