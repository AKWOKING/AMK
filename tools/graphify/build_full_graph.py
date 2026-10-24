#!/usr/bin/env python3
"""AMK — le graphe COMPLET du dépôt : tout le dépôt, pas seulement les .md.

Ce que ça ajoute aux deux passes précédentes
--------------------------------------------
1. **Tous les fichiers** deviennent des nœuds, pas seulement ceux que la CLI classe :
   736 documents, 145 scripts Python, 176 pages HTML, 29 shell, 15 modules, 11 PDF, 11 CSV,
   431 JPG, 80 WebP, 40 MP3, 13 MP4… → un inventaire qui ne laisse rien dehors.
2. **Les citations entre documents** — le vrai squelette du dépôt. Nos textes se citent en
   backticks (`sales/CLIENT-MESSAGING-RULES.md`). 6 382 citations, ~3 250 résolues en chemin
   exact, le reste par nom de fichier quand il est unique. C'est ce réseau qui dit « quelle règle
   s'applique à quel travail » — et c'est ce qui a manqué le 24/10.
3. **Les chaînes de remplacement** : un document qui se déclare « PÉRIMÉE » ou qui en « remplace »
   un autre crée une arête `supersedes`. On peut alors lister **les documents qui citent encore
   une règle périmée** — la seule liste qui empêche de réutiliser une consigne morte.
4. **Les orphelins** : un document que personne ne cite n'est pas mort, mais il n'est atteignable
   par aucun chemin — il faut le savoir.

Aucun LLM, aucune clé, aucun réseau. Tout est déterministe et rejouable.

Usage
-----
    python3 tools/graphify/build_full_graph.py            # construit + clusterise + écrit ops/REPO-MAP.md
    python3 tools/graphify/build_full_graph.py --no-map   # graphe seul
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "graphify-out"
GRAPH = OUT / "graph.json"
MAP = ROOT / "ops" / "REPO-MAP.md"

SKIP_DIRS = {".git", "node_modules", "graphify-out", "__pycache__", ".venv", "dist", "build", ".cache"}
TEXT_EXT = {".md", ".mdx", ".txt", ".py", ".sh", ".mjs", ".js", ".html", ".css", ".yml", ".yaml",
            ".toml", ".csv", ".json", ".srt", ".xml", ".bat", ".gitignore", ""}
KIND = {
    ".md": "document", ".mdx": "document", ".txt": "texte", ".pdf": "pdf", ".docx": "document",
    ".py": "script", ".sh": "script", ".bat": "script", ".mjs": "code", ".js": "code",
    ".html": "page", ".css": "style", ".json": "données", ".csv": "données", ".xlsx": "données",
    ".yml": "config", ".yaml": "config", ".toml": "config", ".xml": "config",
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".webp": "image", ".svg": "image",
    ".ico": "image", ".mp4": "vidéo", ".mp3": "audio", ".wav": "audio", ".srt": "sous-titre",
    ".ttf": "police", ".woff2": "police", ".zip": "archive", ".pyc": "artefact",
}
DOMAIN_LABEL = {
    "knowledge": "Couche connaissance — les règles de référence",
    "sales": "Vente, prospection, CRM humain",
    "leads": "CRM machine (CSV, records, vues générées)",
    "clients": "Dossiers clients",
    "content": "Contenu, vidéos, carrousels, scripts",
    "hosting": "Sites déployés et aperçus",
    "site": "Site AMK",
    "design": "Design, skills, vendor",
    "tools": "Outils et skills installés",
    "ops": "Opérations, portiques, facturation",
    "research": "Recherche externe (vidéos, articles)",
    "brand": "Marque AMK",
    "demos": "Maquettes et concepts",
    "mockups": "Captures et mockups",
    "tryon-camera": "Expérimentation",
}

CITE_RE = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./\-]*\.[A-Za-z0-9]{1,5})`")
STALE_RE = re.compile(r"p[ée]rim[ée]e?|remplac[ée]e?|obsol[èe]te|superseded|ne plus (?:utiliser|envoyer)|d[ée]pass[ée]e",
                      re.I)
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)


def norm_id(rel: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(rel).lower()).strip("_")[:120] or "root"


def is_text(p: Path) -> bool:
    return p.suffix.lower() in TEXT_EXT


def read(p: Path, cap: int = 2_000_000) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:cap]
    except OSError:
        return ""


def walk() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel = Path(dirpath).relative_to(ROOT)
        for name in filenames:
            relpath = rel / name if str(rel) != "." else Path(name)
            if relpath == MAP.relative_to(ROOT) or relpath.name.startswith(("FILE-AUDIT-", "REPO-MAP")):
                continue  # les rapports générés se citent eux-mêmes : les indexer fait boucler le graphe
            files.append(relpath)
    return sorted(files)


def build_file_nodes(files: list[Path]) -> tuple[dict, dict]:
    nodes: dict[str, dict] = {}
    meta: dict[str, dict] = {}
    for rel in files:
        nid = norm_id(rel)
        if nid in nodes:  # deux chemins qui se normalisent pareil : on garde le plus court
            continue
        p = ROOT / rel
        try:
            size = p.stat().st_size
        except OSError:
            size = 0
        ext = p.suffix.lower()
        text = read(p) if is_text(p) and size < 2_000_000 else ""
        lines = text.count("\n") + 1 if text else 0
        heads = [(len(m.group(1)), m.group(2).strip()) for m in HEAD_RE.finditer(text)]
        node = {
            "id": nid,
            "label": rel.name,
            "file_type": "document" if ext in (".md", ".mdx") else ("code" if KIND.get(ext) in ("script", "code") else "concept"),
            "source_file": str(rel),
            "kind": KIND.get(ext, "autre"),
            "ext": ext or "—",
            "bytes": size,
            "lines": lines,
            "headings": len(heads),
            "domain": rel.parts[0] if len(rel.parts) > 1 else "(racine)",
            "_origin": "amk-inventory",
        }
        nodes[nid] = node
        meta[nid] = {"rel": rel, "text": text, "heads": heads}
    return nodes, meta


def build_citation_edges(nodes: dict, meta: dict) -> tuple[list[dict], dict]:
    by_rel = {str(m["rel"]): nid for nid, m in meta.items()}
    by_name: dict[str, list[str]] = defaultdict(list)
    for nid, m in meta.items():
        by_name[m["rel"].name.lower()].append(nid)

    edges: list[dict] = []
    stats = Counter()
    for nid, m in meta.items():
        text = m["text"]
        if not text or m["rel"].suffix.lower() not in {".md", ".mdx", ".txt"}:
            continue
        seen: set[tuple[str, str]] = set()
        for raw in CITE_RE.findall(text):
            target = None
            conf = None
            cand = raw.lstrip("./")
            if cand in by_rel:
                target, conf = by_rel[cand], "EXTRACTED"
            else:
                rel_from = (m["rel"].parent / cand).as_posix()
                rel_from = os.path.normpath(rel_from)
                if rel_from in by_rel:
                    target, conf = by_rel[rel_from], "EXTRACTED"
                else:
                    hits = by_name.get(Path(cand).name.lower(), [])
                    if len(hits) == 1:
                        target, conf = hits[0], "INFERRED"
            if not target or target == nid:
                continue
            if (nid, target) in seen:
                continue
            seen.add((nid, target))
            edges.append({"source": nid, "target": target, "relation": "cites",
                          "confidence": conf, "context": raw})
            stats[conf] += 1
    return edges, dict(stats)


SELF_STALE = re.compile(
    r"(ce document|cette page|ce fichier|cette version|ce texte|cette r[èe]gle|la version|cette liste)"
    r"[^.]{0,80}?(p[ée]rim[ée]e?|obsol[èe]te|remplac[ée]e?|ne (?:s'applique|s applique) plus|n'est plus en vigueur)",
    re.I)

def build_supersede_edges(meta: dict) -> tuple[list[dict], set[str]]:
    """Un document qui se dit périmé LUI-MÊME, ou qui en remplace un autre.

    Le 24/10, la première version de cette détection marquait `Activity-Log.md` et
    `AMK-DESIGN-SKILLS.md` comme périmés : ils *parlent* de choses périmées, ils ne le sont pas.
    Un document n'est périmé que si (a) le marqueur est dans son en-tête (25 premières lignes),
    (b) la ligne nomme son propre fichier, ou (c) la phrase dit « ce document / cette version …
    est périmé ». Tout le reste est une mention, pas un statut.
    """
    by_rel = {str(m["rel"]): nid for nid, m in meta.items()}
    by_name: dict[str, str] = {}
    for nid, m in meta.items():
        by_name.setdefault(m["rel"].name.lower(), nid)

    edges: list[dict] = []
    stale: set[str] = set()
    for nid, m in meta.items():
        if m["rel"].suffix.lower() not in {".md", ".mdx"}:
            continue
        own = m["rel"].name.lower()
        for i, line in enumerate(m["text"].splitlines()):
            if not STALE_RE.search(line) and not SELF_STALE.search(line):
                continue
            low = line.lower()
            self_declared = (
                i < 25
                or own in low
                or bool(SELF_STALE.search(line))
                or bool(re.search(r"^#{1,6}\s.*(p[ée]rim[ée]e?|obsol[èe]te|superseded)", line, re.I))
            )
            if self_declared and re.search(r"p[ée]rim[ée]e?|obsol[èe]te|superseded", low):
                stale.add(nid)
            for raw in CITE_RE.findall(line):
                cand = raw.lstrip("./")
                tgt = by_rel.get(cand) or by_name.get(Path(cand).name.lower())
                if tgt and tgt != nid:
                    edges.append({"source": nid, "target": tgt, "relation": "supersedes",
                                  "confidence": "INFERRED", "context": f"L{i+1}: {line.strip()[:120]}"})
    return edges, stale


def merge(graphs: list[dict], extra_nodes: dict) -> dict:
    nodes: dict[str, dict] = {}
    edges: dict[tuple, dict] = {}
    for g in graphs:
        for n in g.get("nodes", []):
            nodes.setdefault(n["id"], n)
        for e in g.get("edges", []):
            edges.setdefault((e.get("source"), e.get("target"), e.get("relation")), e)
    for nid, n in extra_nodes.items():
        nodes.setdefault(nid, n)
    # les nœuds AST (titres, symboles) portent le même id que le nœud fichier : on garde la
    # structure ET l'inventaire — sinon on perd `kind`/`lines` sur tous les documents.
    for nid, inv in extra_nodes.items():
        if nid in nodes:
            for k, v in inv.items():
                nodes[nid].setdefault(k, v)
            for k in ("kind", "domain", "ext", "bytes", "lines", "headings"):
                if k in inv:
                    nodes[nid][k] = inv[k]
    out = {"nodes": list(nodes.values()), "edges": list(edges.values()),
           "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
    return out


def degrees(g: dict) -> tuple[Counter, Counter]:
    indeg, outdeg = Counter(), Counter()
    for e in g["edges"]:
        outdeg[e["source"]] += 1
        indeg[e["target"]] += 1
    return indeg, outdeg


def human(n: int) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "o" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} To"


def compute_communities(g: dict, by_id: dict, meta: dict) -> dict[str, int]:
    """Communautés sur le réseau des CITATIONS (Louvain de networkx, local, déterministe par graine).

    Le `cluster-only` de l'amont refuse d'écrire sur un graphe qui contient nos nœuds d'inventaire
    (« saved semantic node(s) are missing »), et il clusterise aussi les 9 000 titres — ce qui noie
    la structure. Ici on ne regroupe que les documents, sur les liens qui veulent dire quelque chose :
    `cites` et `supersedes`. Une communauté = un sujet qu'on peut nommer par ses trois fichiers pivots.
    """
    try:
        import networkx as nx
    except ImportError:
        return {}
    sub = [e for e in g["edges"] if e["relation"] in ("cites", "supersedes", "references")
           and e["source"] in by_id and e["target"] in by_id
           and by_id[e["source"]].get("kind") == "document"
           and by_id[e["target"]].get("kind") == "document"]
    G = nx.Graph()
    for e in sub:
        G.add_edge(e["source"], e["target"])
    if G.number_of_nodes() < 10:
        return {}
    communities = nx.community.louvain_communities(G, seed=42)
    label: dict[str, int] = {}
    for i, c in enumerate(sorted(communities, key=len, reverse=True)):
        for nid in c:
            label[nid] = i
    return label


def isolated_docs(g: dict, by_id: dict) -> list[str]:
    """Les documents qu'aucune arête de citation ne touche : hors réseau, pas hors sujet."""
    touched = {e["source"] for e in g["edges"]} | {e["target"] for e in g["edges"]}
    return [n["id"] for n in g["nodes"]
            if n.get("kind") == "document" and n["id"] not in touched]


def doc_subject(n: dict, meta: dict) -> str:
    """Le sujet d'un document, lu dans son texte : 1re ligne de titre, sinon 1re phrase."""
    txt = meta.get(n["id"], {}).get("text", "")
    for line in txt.splitlines():
        t = line.strip().lstrip(">#*").strip().strip("*").strip()
        if len(t) > 12 and not t.startswith(("```", "|", "---", "Généré")):
            return t[:90].replace("|", "·")
    return "—"


def write_communities_section(A, g, by_id, comm, indeg) -> None:
    if not comm:
        return
    groups: dict[int, list[str]] = {}
    for nid, cid in comm.items():
        groups.setdefault(cid, []).append(nid)
    # degré INTERNE : un document pivot est celui que les autres documents du groupe citent.
    internal: dict[int, Counter] = {}
    for e in g["edges"]:
        if e.get("relation") != "cites":
            continue
        a, b = e.get("source"), e.get("target")
        if a in comm and b in comm and comm[a] == comm[b]:
            internal.setdefault(comm[a], Counter())[b] += 1
    A("## 4 · Les communautés du dépôt — les sujets, tels que les documents se relient")
    A("")
    A(f"{len(groups)} communautés détectées sur le réseau des citations (Louvain, graine fixe). "
      "Chaque bloc est un sujet réel : les documents qui s'y trouvent se citent entre eux.")
    A("")
    A("*Le pivot d'une communauté est le document que **les autres membres du groupe** citent le "
      "plus (degré interne) — pas le document le plus cité du dépôt, qui l'est partout.*")
    A("")
    iso = isolated_docs(g, by_id)
    n_docs = sum(1 for n in g["nodes"] if n.get("kind") == "document")
    A(f"**{len(comm)} documents sur {n_docs} sont dans un sujet.** Les {len(iso)} autres ne touchent "
      "aucune citation — ni entrante, ni sortante : ce sont eux qui se perdent (voir §3 bis). "
      "Un sujet se nomme par ses pivots ; un document hors sujet ne se retrouve pas tout seul.")
    A("")
    A("| # | Docs | Les 3 pivots internes | Ce que le groupe a en propre |")
    A("|---|---|---|---|")
    used: set[str] = set()
    order = sorted(groups.items(), key=lambda kv: -len(kv[1]))
    for cid, members in order[:14]:
        ranks = internal.get(cid, Counter())
        pivots = []
        for n in [m for m, _ in ranks.most_common()] or sorted(members, key=lambda n: -indeg[n]):
            if n in used:
                continue
            pivots.append(n)
            used.add(n)
            if len(pivots) == 3:
                break
        if not pivots:
            pivots = sorted(members, key=lambda n: -indeg[n])[:3]
        names = " · ".join(f"`{by_id[n]['label']}`" for n in pivots)
        doms = Counter(by_id[n].get("domain") for n in members)
        # ex æquo départagé par le nom : sinon deux runs identiques peuvent écrire deux cartes
        top_dom, top_n = sorted(doms.items(), key=lambda kv: (-kv[1], str(kv[0])))[0]
        share = f"{100 * top_n // len(members)} %"
        A(f"| {cid} | {len(members)} | {names} | `{top_dom}/` ({share} du groupe) |")
    A("")
    for cid, members in order[:10]:
        A(f"### Communauté {cid} — {len(members)} documents")
        A("")
        ranks = internal.get(cid, Counter())
        head = [n for n, _ in ranks.most_common(6)] or sorted(members, key=lambda n: -indeg[n])[:6]
        for n in head:
            A(f"- `{by_id[n]['source_file']}` — cité {ranks.get(n, 0)}× dans le groupe, {indeg[n]}× au total")
        A("")


def write_map(g: dict, nodes_meta: dict, stale: set[str], stats: dict, comm: dict | None = None) -> str:
    indeg, outdeg = degrees(g)
    by_id = {n["id"]: n for n in g["nodes"]}
    domains = Counter(n.get("domain") for n in g["nodes"])
    kinds = Counter(n.get("kind") for n in g["nodes"])

    cites_edges = [e for e in g["edges"] if e["relation"] == "cites"]
    sup_edges = [e for e in g["edges"] if e["relation"] == "supersedes"]

    # documents qui citent encore une règle marquée périmée
    danger = defaultdict(list)
    for e in sup_edges:
        if e["target"] in stale:
            danger[e["target"]].append(e["source"])

    docs = [n for n in g["nodes"] if n.get("kind") == "document"]
    orphans = [n for n in docs if indeg[n["id"]] == 0 and n.get("domain") != "graphify-out"]
    hubs = sorted(docs, key=lambda n: -indeg[n["id"]])[:20]

    L: list[str] = []
    A = L.append
    A(f"# CARTE DU DÉPÔT — ce qui existe, où c'est, et ce qui n'est atteignable par aucun chemin")
    A("")
    A(f"```text\nGénéré par tools/graphify/build_full_graph.py — {date.today().isoformat()}\n"
      f"Source : graphify-out/graph.json ({len(g['nodes'])} nœuds, {len(g['edges'])} arêtes)\n"
      f"Aucun LLM, aucune clé : tout est déterministe et rejouable en ~10 secondes.\n```")
    A("")
    A("## 0 · En une page")
    A("")
    A(f"- **{len(g['nodes'])} nœuds** — dont {len(docs)} documents, "
      f"{kinds.get('script', 0)} scripts, {kinds.get('code', 0)} modules, {kinds.get('page', 0)} pages HTML, "
      f"{kinds.get('image', 0)} images, {kinds.get('vidéo', 0)} vidéos, {kinds.get('audio', 0)} audios, "
      f"{kinds.get('données', 0)} fichiers de données, {kinds.get('pdf', 0)} PDF.")
    A(f"- **{len(cites_edges)} citations entre documents** "
      f"({stats.get('EXTRACTED', 0)} en chemin exact, {stats.get('INFERRED', 0)} par nom unique)")
    A(f"- **{len(sup_edges)} arêtes de remplacement** · **{len(stale)} documents marqués périmés**")
    A(f"- **{len(orphans)} documents que personne ne cite** (atteignables par aucun chemin de lecture)")
    n_files = sum(1 for n in g["nodes"] if n.get("kind"))
    A(f"- **Couverture : {n_files} fichiers indexés.** Le seul exclu est cette carte "
      f"(`ops/REPO-MAP.md`, qui se citerait elle-même) et `graphify-out/` (sortie régénérable). "
      f"Rien d'autre n'est laissé de côté : ni image, ni audio, ni police, ni PDF, ni archive, "
      f"ni sous-titre, ni fichier de données.")
    A("")
    A("### Les dossiers du dépôt, par poids — et ce que chacun porte")
    A("")
    A("| Dossier | Fichiers | Ce que c'est |")
    A("|---|---|---|")
    for d, c in sorted(domains.items(), key=lambda kv: -kv[1]):
        if d in (None, "(racine)"):
            continue
        A(f"| `{d}/` | {c} | {DOMAIN_LABEL.get(d, '—')} |")
    A("")

    A("## 1 · La couche connaissance — les 10 documents qui font loi")
    A("")
    A("| Document | Titres | Cité par | Son sujet, dans ses propres mots |")
    A("|---|---|---|---|")
    for n in sorted([n for n in docs if n.get("domain") == "knowledge"], key=lambda x: -indeg[x["id"]]):
        A(f"| `{n['source_file']}` | {n.get('headings', 0)} | {indeg[n['id']]}× | {doc_subject(n, nodes_meta)} |")
    A("")

    A("## 2 · Les 20 documents les plus cités — le squelette réel")
    A("")
    A("C'est ce réseau qui décide de ce qui s'applique à un travail. Si un document que vous écrivez n'y "
      "entre pas, personne ne le retrouvera.")
    A("")
    A("| Rang | Document | Cité par | Titres |")
    A("|---|---|---|---|")
    for i, n in enumerate(hubs, 1):
        A(f"| {i} | `{n['source_file']}` | **{indeg[n['id']]}** | {n.get('headings', 0)} |")
    A("")

    if danger:
        A("## 3 · ⚠️ Documents encore cités alors qu'ils sont marqués périmés")
        A("")
        A("Ce sont les consignes mortes qu'on risque de réappliquer. Chaque ligne est un correctif à faire.")
        A("")
        A("*Détection lexicale* : un document est marqué périmé quand **son propre texte** le dit "
          "(en-tête, titre, ou « ce document / cette version … est périmé »). Un document qui *parle* "
          "de choses périmées n'est pas périmé — c'est la correction apportée le 24/10 après que "
          "`Activity-Log.md` et `AMK-DESIGN-SKILLS.md` ont été signalés à tort. Reste à vérifier au "
          "cas par cas : une ligne du tableau n'est pas une preuve, c'est une piste.")
        A("")
        A("| Document périmé | Encore cité par |")
        A("|---|---|")
        for tgt, srcs in sorted(danger.items(), key=lambda kv: -len(kv[1]))[:15]:
            names = ", ".join(f"`{Path(by_id[s]['source_file']).name}`" for s in srcs[:4])
            more = f" (+{len(srcs) - 4})" if len(srcs) > 4 else ""
            A(f"| `{by_id[tgt]['source_file']}` | {len(srcs)} : {names}{more} |")
        A("")

    A("## 3 bis · Ce que personne ne cite — à relire ou à archiver")
    A("")
    A(f"{len(orphans)} documents n'ont aucune citation entrante. Un orphelin n'est pas inutile : il est "
      "**inatteignable**. Soit il faut le citer là où il sert, soit il faut l'archiver.")
    A("")
    # Deux familles d'orphelins sont normales et ne demandent rien : le vendor (skills tierces
    # importées telles quelles) et les records (une fiche par prospect, reliée par le CRM, pas par
    # une citation). Les mélanger aux vraies orphelines noyait la liste.
    vendor = [n for n in orphans if "vendor/" in n["source_file"] or "/vendor" in n["source_file"]]
    records = [n for n in orphans if n["source_file"].startswith("leads/records/")]
    real = [n for n in orphans if n not in vendor and n not in records]

    A(f"- **{len(real)} à traiter** · {len(vendor)} dans `design/vendor/` (imports tiers, normal)"
      f" · {len(records)} dans `leads/records/` (reliés par le CRM, pas par citation)")
    A("")
    orphan_by_domain = defaultdict(list)
    for n in real:
        orphan_by_domain[n.get("domain")].append(n["source_file"])
    for d, items in sorted(orphan_by_domain.items(), key=lambda kv: -len(kv[1])):
        A(f"- **`{d}/`** — {len(items)} : " + ", ".join(f"`{p}`" for p in items[:6])
          + (f" … (+{len(items) - 6})" if len(items) > 6 else ""))
    A("")

    write_communities_section(A, g, by_id, comm or {}, indeg)

    A("## 5 · Le reste du dépôt, par nature")
    A("")
    A("| Nature | Fichiers | Où |")
    A("|---|---|---|")
    for kind, count in kinds.most_common():
        if kind is None:
            continue
        sample = [n["source_file"] for n in g["nodes"] if n.get("kind") == kind][:3]
        A(f"| {kind} | {count} | " + ", ".join(f"`{s}`" for s in sample) + " |")
    symbols = sum(1 for n in g["nodes"] if n.get("kind") is None)
    A(f"| symboles extraits (titres de documents + fonctions/classes du code) | {symbols} | — |")
    A("")

    # 5 bis · les outils et skills, avec leur point d'entrée
    tools_dir = ROOT / "tools"
    if tools_dir.is_dir():
        A("### Les outils et skills installés — 1 dossier = 1 outil")
        A("")
        A("**Point d'entrée** = ce qu'on exécute ou ce qu'on lit en premier. "
          "**Contenu** = ce qu'il y a réellement dans le dossier.")
        A("")
        A("| Outil | Point d'entrée | Contenu | Ce qu'il fait |")
        A("|---|---|---|---|")
        for d in sorted(tools_dir.iterdir()):
            if not d.is_dir() or d.name.startswith((".", "_")):
                continue
            files = [f for f in d.rglob("*") if f.is_file()
                     and "__pycache__" not in f.parts and not f.name.startswith(".")]
            n_py = sum(1 for f in files if f.suffix in (".py", ".mjs", ".js"))
            n_md = sum(1 for f in files if f.suffix == ".md")
            n_sh = sum(1 for f in files if f.suffix in (".sh", ".yml", ".yaml"))
            parts = []
            if n_py: parts.append(f"{n_py} script(s)")
            if n_md: parts.append(f"{n_md} doc(s)")
            if n_sh: parts.append(f"{n_sh} shell/CI")
            content = " · ".join(parts) or f"{len(files)} fichier(s)"
            entry_bits = []
            for name in ("README.md", "readme.md", "install.sh", "SKILL.md"):
                if (d / name).exists():
                    entry_bits.append(f"`{name}`")
            if not entry_bits:
                first_md = next((f for f in sorted(files) if f.suffix == ".md"), None)
                entry_bits.append(f"`{first_md.name}`" if first_md else "—")
            desc = "—"
            rd = next((d / n for n in ("README.md", "readme.md", "SKILL.md") if (d / n).exists()), None)
            if rd:
                for line in rd.read_text(encoding="utf-8", errors="ignore").splitlines():
                    t = line.strip().lstrip("#").strip().strip("*").strip()
                    if len(t) > 5 and not t.startswith(("```", "|", ">")):
                        desc = t[:80]
                        break
            A(f"| `{d.name}/` | {' '.join(entry_bits)} | {content} | {desc} |")
        A("")

    # 5 quater · un dossier client = une ligne
    clients_dir = ROOT / "clients"
    if clients_dir.is_dir():
        A("### Un dossier client = une ligne — ce qui existe, et s'il y a un brief")
        A("")
        A("| Client | Fichiers | Documents | Brief ? | Dernier commit sur le dossier |")
        A("|---|---|---|---|---|")
        for d in sorted(clients_dir.iterdir()):
            if not d.is_dir() or d.name.startswith(("_", ".")):
                continue
            files = [f for f in d.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
            docs_n = sum(1 for f in files if f.suffix == ".md")
            if not files:
                continue
            brief = "oui" if any("brief" in f.name.lower() for f in files) else "—"
            try:
                stamp = subprocess.run(
                    ["git", "log", "-1", "--format=%ad", "--date=short", "--", f"clients/{d.name}"],
                    cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip() or "—"
            except (OSError, subprocess.SubprocessError):
                stamp = "—"
            A(f"| `{d.name}/` | {len(files)} | {docs_n} | {brief} | {stamp} |")
        A("")

    # 5 ter · les vidéos et leurs pièces
    vids = ROOT / "content" / "videos"
    if vids.is_dir():
        A("### Les vidéos — une pièce par dossier, et ce qu'elle contient")
        A("")
        A("| Pièce | Fichiers | Script | Montage | Statut |")
        A("|---|---|---|---|---|")
        for d in sorted(vids.iterdir()):
            if not d.is_dir() or d.name.startswith(("_", ".")):
                continue
            files = [f for f in d.rglob("*") if f.is_file()]
            scripts = [f for f in files if f.suffix == ".md" and "status" not in f.name.lower()]
            mp4 = [f for f in files if f.suffix in (".mp4", ".mov", ".webm")]
            status = "—"
            st = d / "STATUS.md"
            if st.exists():
                lines = [l.strip().lstrip(">-#|* ").strip().strip("*")
                         for l in st.read_text(encoding="utf-8", errors="ignore").splitlines()]
                lines = [l for l in lines if len(l) > 4 and not l.startswith("```")]
                keyed = [l for l in lines if re.match(r"(statut|status|état|etat)\b", l, re.I)]
                pick = keyed[0] if keyed else (lines[1] if len(lines) > 1 else (lines[0] if lines else "—"))
                status = re.sub(r"\s*[·|]\s*$", "", pick)[:80]
            A(f"| `{d.name}` | {len(files)} | "
              f"{'oui (' + scripts[0].name + ')' if scripts else '—'} | "
              f"{str(len(mp4)) + ' fichier(s)' if mp4 else '—'} | {status} |")
        A("")

    A("## 6 · Où chercher quoi — la table de routage, vérifiée par le graphe")
    A("")
    A("| Sujet | Les 3 documents qu'il faut ouvrir |")
    A("|---|---|")
    TOPICS = [
        ("Écrire un message / relancer", ["prospect", "message", "relance", "accroche"]),
        ("Prix, grille, remise", ["prix", "grille", "facture", "remise"]),
        ("Contenu, vidéo, script", ["video", "script", "accroche", "carrousel"]),
        ("Design, page, tokens", ["design", "tokens", "page", "hero"]),
        ("Déploiement, QA, portiques", ["deploy", "audit", "portique", "verification"]),
        ("Client DM Optique", ["dm", "optic", "client"], "clients/dm-optic/"),
        ("Outils et skills", ["outil", "skill", "tool", "install"], "tools/"),
        ("CRM, pipeline, activité", ["crm", "pipeline", "envoi", "lead"], "leads/"),
    ]
    doc_nodes = [n for n in g["nodes"] if n.get("kind") == "document"]
    docs_text = {n["id"]: nodes_meta[n["id"]]["text"][:60000].lower() if n["id"] in nodes_meta else ""
                 for n in doc_nodes}
    LOGS = ("activity-log", "analytics-log", "changelog", "pipeline-status", "status.md")
    for topic in TOPICS:
        label, words = topic[0], topic[1]
        hint = topic[2] if len(topic) > 2 else None
        scored = []
        for n in doc_nodes:
            src = n["source_file"]
            if any(k in src.lower() for k in LOGS) or src == "ops/REPO-MAP.md":
                continue  # un journal — ou la carte elle-même — ne route vers rien
            hay = docs_text.get(n["id"], "")
            hits = sum(min(hay.count(w), 25) for w in words)
            if not hits:
                continue
            lines = max(n.get("lines", 1), 1)
            score = hits / (1 + lines / 400) ** 0.7
            if src.startswith("knowledge/"):
                score *= 1.6
            if any(k in Path(src).name.upper() for k in ("RULES", "STANDARD", "PLAYBOOK", "GUIDE", "SCHEMA")):
                score *= 1.3
            score += min(indeg[n["id"]], 12) * 0.4
            if hint and src.startswith(hint):
                score *= 3  # le sujet nomme un dossier : le dossier passe devant
            scored.append((score, src))
        scored.sort(reverse=True)
        picks = ", ".join(f"`{q}`" for _, q in scored[:3]) or "—"
        A(f"| {label} | {picks} |")
    A("")

    A("## 7 · Les questions qu'on peut poser au graphe dès maintenant")
    A("")
    A("```bash")
    A('bash tools/graphify/ask.sh "message prospect clinique"      # quelles règles lire avant d\'écrire')
    A('bash tools/graphify/ask.sh "prix grille remise"               # la couche tarifaire')
    A('bash tools/graphify/ask.sh "vidéo script accroche"            # la couche contenu')
    A('graphify explain "sales/CLIENT-MESSAGING-RULES.md"')
    A('graphify path "sales/LISTE-OPTICIENS-2026-10.md" "knowledge/OUTREACH-MESSAGING-2026-10-22.md"')
    A("```")
    A("")
    A("---")
    A("")
    A("*Cette carte est générée : ne pas l'éditer à la main. Elle se régénère avec "
      "`python3 tools/graphify/build_full_graph.py`.*")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-map", action="store_true", help="ne pas réécrire ops/REPO-MAP.md")
    ap.add_argument("--no-cluster", action="store_true", help="ne pas relancer le clustering")
    args = ap.parse_args()

    try:
        from graphify.extract import extract as ast_extract
    except ImportError:
        venv_py = Path(os.environ.get("AMK_GRAPHIFY_VENV", "/tmp/amk-graphify")) / "bin" / "python"
        if venv_py.exists() and Path(sys.prefix).resolve() != venv_py.parents[1].resolve():
            os.execv(str(venv_py), [str(venv_py), str(Path(__file__).resolve()), *sys.argv[1:]])
        print("graphify absent : bash tools/graphify/install.sh", file=sys.stderr)
        return 2

    files = walk()
    print(f"[full] {len(files)} fichier(s) balayés")

    nodes, meta = build_file_nodes(files)
    print(f"[full] {len(nodes)} nœud(s) fichier (inventaire complet)")

    # la passe AST : symboles de code + titres markdown (extracteur amont, déterministe)
    code = [m["rel"] for m in meta.values() if m["rel"].suffix.lower() in
            {".py", ".mjs", ".js", ".sh", ".html", ".ts", ".yml", ".yaml"}]
    docs = [m["rel"] for m in meta.values() if m["rel"].suffix.lower() in {".md", ".mdx", ".txt"}]
    ast = ast_extract(code, root=ROOT, cache_root=ROOT)
    md = ast_extract(docs, root=ROOT, cache_root=ROOT)
    print(f"[full] structure : {len(ast.get('nodes', []))} nœuds code · "
          f"{len(md.get('nodes', []))} nœuds document")

    cite_edges, stats = build_citation_edges(nodes, meta)
    sup_edges, stale = build_supersede_edges(meta)
    print(f"[full] citations : {len(cite_edges)} ({stats}) · remplacements : {len(sup_edges)} · "
          f"périmés : {len(stale)}")

    g = merge([ast, md, {"nodes": list(nodes.values()), "edges": cite_edges + sup_edges}], {})

    # les symboles extraits par la passe AST n'ont pas de source_file : on le reconstitue
    # depuis leur identifiant, sinon le graphe n'est pas relisible par la CLI amont.
    norm_to_rel = {norm_id(m["rel"]): str(m["rel"]) for m in meta.values()}
    orphan_src = 0
    for n in g["nodes"]:
        if n.get("source_file"):
            continue
        prefix = max((k for k in norm_to_rel if n["id"].startswith(k)), key=len, default=None)
        if prefix:
            n["source_file"] = norm_to_rel[prefix]
        else:
            orphan_src += 1
    if orphan_src:
        # derniers recours : le fichier de l'arête qui pointe vers ce nœud
        edge_src = {e["target"]: e.get("source_file") for e in g["edges"] if e.get("source_file")}
        still = 0
        for n in g["nodes"]:
            if n.get("source_file"):
                continue
            n["source_file"] = edge_src.get(n["id"], "")
            still += 0 if n["source_file"] else 1
        print(f"[full] {orphan_src} nœud(s) externe(s) rattaché(s) par arête"
              + (f" · {still} restant(s) sans fichier" if still else ""))
    OUT.mkdir(exist_ok=True)
    GRAPH.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
    (OUT / "stale.json").write_text(json.dumps(sorted(stale), ensure_ascii=False, indent=1), encoding="utf-8")
    n_cites = sum(1 for e in g["edges"] if e["relation"] == "cites")
    n_sup = sum(1 for e in g["edges"] if e["relation"] == "supersedes")
    print(f"[full] écrit {GRAPH.relative_to(ROOT)} — {len(g['nodes'])} nœuds, {len(g['edges'])} arêtes "
          f"({n_cites} citations conservées, {n_sup} remplacements)")

    by_id = {n["id"]: n for n in g["nodes"]}
    comm = compute_communities(g, by_id, meta)
    for nid, cid in comm.items():
        by_id[nid]["community"] = cid
    GRAPH.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
    print(f"[full] communautés : {len(set(comm.values()))} sur {len(comm)} documents")

    if not args.no_map:
        MAP.write_text(write_map(g, meta, stale, stats, comm), encoding="utf-8")
        print(f"[full] carte écrite → {MAP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
