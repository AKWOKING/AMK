#!/usr/bin/env python3
"""AMK — construire le graphe des DOCUMENTS du dépôt, sans clé d'API.

Pourquoi ce script existe
-------------------------
`graphify extract` ne traite les documents (Markdown, PDF, images) qu'avec un backend LLM :
sans clé — et nous n'en mettons pas dans le bac à sable — il les **écarte** et n'indexe que le code
(`GRAPHIFY_BACKEND=none` → « skipping LLM work … indexing code only »).

Or 920 des 1 110 fichiers de ce dépôt sont des documents, et c'est là que vivent les règles, les
leçons et les messages. La partie utile pour nous — la **structure** : chaque titre devient un nœud,
chaque lien entre deux documents devient une arête — est déterministe, locale et gratuite
(`graphify.extractors.markdown.extract_markdown`, aucune dépendance LLM, parsing ligne à ligne).

Ce script fait donc la seule chose qui manque : il passe cet extracteur sur tous les documents,
fusionne le résultat avec le graphe de code déjà produit par la CLI, et laisse `graphify cluster-only`
calculer les communautés. Aucune donnée ne sort de la machine.

Usage
-----
    bash tools/graphify/install.sh                 # une fois par session (venv /tmp/amk-graphify)
    python3 tools/graphify/build_docs_graph.py     # graphe complet : code + documents
    /tmp/amk-graphify/bin/graphify query "messages d'approche froide"
    /tmp/amk-graphify/bin/graphify explain "CLIENT-MESSAGING-RULES.md"

Ce qu'on ne fait pas
--------------------
- **Aucun nœud « concept » inventé** : sans LLM, on n'extrait pas de sens, on extrait la structure.
  Une arête `contains` dit « ce titre est dans ce fichier », pas « ce paragraphe parle de X ».
- **Aucun envoi réseau** : ni clé, ni appel, ni télémétrie.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "graphify-out"
GRAPH = OUT / "graph.json"

DOC_EXTS = {".md", ".mdx", ".qmd", ".markdown"}
SKIP_DIRS = {".git", "node_modules", "graphify-out", ".venv", "__pycache__", "dist", "build"}

# Priorité de lecture : les documents de vente et d'opérations d'abord (ceux qu'on cite dans un message),
# le reste ensuite. L'ordre ne change pas le graphe, il change seulement l'ordre de progression affiché.
PRIORITY = ("sales", "ops", "knowledge", "clients")


def collect_docs() -> list[Path]:
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = Path(dirpath).relative_to(ROOT)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if Path(name).suffix.lower() in DOC_EXTS:
                found.append((rel / name))

    def key(p: Path) -> tuple:
        head = p.parts[0] if p.parts else ""
        rank = PRIORITY.index(head) if head in PRIORITY else len(PRIORITY)
        return (rank, str(p))

    return sorted(found, key=key)


def main() -> int:
    try:
        from graphify.extract import extract as ast_extract
    except ImportError:
        # graphify vit dans le venv jetable ; on s'y ré-exécute plutôt que d'exiger un appelant précis.
        venv_py = Path(os.environ.get("AMK_GRAPHIFY_VENV", "/tmp/amk-graphify")) / "bin" / "python"
        if venv_py.exists() and Path(sys.prefix).resolve() != venv_py.parents[1].resolve():
            os.execv(str(venv_py), [str(venv_py), str(Path(__file__).resolve()), *sys.argv[1:]])
        print("graphify absent. Lancez d'abord : bash tools/graphify/install.sh", file=sys.stderr)
        return 2

    docs = collect_docs()
    print(f"[amk-graphify] {len(docs)} document(s) à structurer")

    # 1 · le graphe de code, par la CLI (AST local, gratuit)
    if not GRAPH.exists():
        print("[amk-graphify] graphe de code absent → graphify extract --no-cluster")
        subprocess.run(
            ["graphify", "extract", ".", "--no-cluster"],
            cwd=ROOT,
            env={**os.environ, "GRAPHIFY_BACKEND": "none"},
            check=True,
        )
    code_graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    # 2 · les documents, par l'extracteur déterministe
    result = ast_extract(docs, root=ROOT, cache_root=ROOT)
    doc_nodes = result.get("nodes", [])
    doc_edges = result.get("edges", [])
    print(f"[amk-graphify] documents : {len(doc_nodes)} nœud(s), {len(doc_edges)} arête(s)")

    # 3 · fusion sans doublon (un même id ne peut venir que d'un fichier)
    nodes = {n["id"]: n for n in code_graph.get("nodes", [])}
    before = len(nodes)
    for n in doc_nodes:
        nodes.setdefault(n["id"], n)

    edges = {(e.get("source"), e.get("target"), e.get("relation")): e for e in code_graph.get("edges", [])}
    e_before = len(edges)
    for e in doc_edges:
        edges.setdefault((e.get("source"), e.get("target"), e.get("relation")), e)

    merged = {
        **{k: v for k, v in code_graph.items() if k not in ("nodes", "edges")},
        "nodes": list(nodes.values()),
        "edges": list(edges.values()),
    }
    merged.setdefault("hyperedges", [])
    OUT.mkdir(exist_ok=True)
    GRAPH.write_text(json.dumps(merged, ensure_ascii=False), encoding="utf-8")

    print(
        f"[amk-graphify] fusion : {len(nodes)} nœuds ({len(nodes) - before} docs) · "
        f"{len(edges)} arêtes ({len(edges) - e_before} docs) → {GRAPH.relative_to(ROOT)}"
    )

    # 4 · communautés + rapport, sans LLM (Louvain de networkx, local)
    print("[amk-graphify] cluster-only --no-label --no-viz")
    subprocess.run(
        ["graphify", "cluster-only", ".", "--no-label", "--no-viz"],
        cwd=ROOT,
        env={**os.environ, "GRAPHIFY_BACKEND": "none"},
        check=False,
    )
    print("[amk-graphify] prêt. Exemples :")
    print('  graphify query "règles de message WhatsApp"')
    print('  graphify explain "OUTREACH-REECRITURE-2026-10-24.md"')
    print('  graphify path "LISTE-OPTICIENS-2026-10.md" "CLIENT-MESSAGING-RULES.md"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
