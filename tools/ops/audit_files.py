#!/usr/bin/env python3
"""AMK — l'audit des fichiers : ce qui est mort, ce qui est en double, ce qui coûte cher.

Pourquoi cet outil existe
-------------------------
Le 24/10/2026, King demande « un audit complet des fichiers, en retirant ceux qui sont
périmés ou inutiles ». Un audit à l'œil sur 1 936 fichiers, c'est un pari : on supprime
au feeling, ou on ne supprime rien. Cet outil remplace le feeling par des **preuves**,
et il est rejouable — la prochaine fois, une commande.

Ce qu'il regarde, et ce que ça vaut comme preuve
-----------------------------------------------
| Classe | Preuve | Ce qu'on peut en faire |
|---|---|---|
| CACHE | `__pycache__`, `*.pyc` | supprimable sans réflexion |
| DOUBLON | md5 identique, octet pour octet | une seule copie suffit — **sauf** si les deux sont déployées séparément |
| SANS RÉFÉRENCE | nom de fichier absent de tout le texte du dépôt | piste, pas preuve : une image peut être appelée par un manifeste ou un CSS |
| ORPHELIN | document sans citation entrante (graphe) | à relire, pas à supprimer : il peut être de la connaissance morte *ou* non branchée |
| PÉRIMÉ | le document dit lui-même qu'il est remplacé | à vérifier au cas par cas — la détection est lexicale |
| ARTEFACT | `.zip` reconstruit par un script | vérifier que le script existe encore |
| LOURD | > 5 Mo | ce qui coûte dans le `.git`, et ce qui mériterait de sortir du dépôt |

Ce qu'il ne fait pas
--------------------
Il **ne supprime rien** tout seul, sauf les caches avec `--clean-cache`. Une suppression de
document est une décision de King, pas une heuristique : le dépôt contient des règles qui
valent plus que leur poids en octets.

Usage
-----
    python3 tools/ops/audit_files.py                    # écrit ops/FILE-AUDIT-<date>.md
    python3 tools/ops/audit_files.py --clean-cache      # + retire les __pycache__
    python3 tools/ops/audit_files.py --no-write         # affiche seulement le résumé
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "graphify-out" / "graph.json"

SKIP_DIRS = {".git", "graphify-out", "node_modules", "__pycache__", ".venv", "dist", "archive",
             "build", ".cache", ".next"}

TEXT_EXT = {".md", ".html", ".js", ".mjs", ".py", ".json", ".css", ".yml", ".yaml",
            ".txt", ".sh", ".svg"}

MEDIA_EXT = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".mp3", ".pdf", ".zip",
             ".docx", ".xlsx", ".ttf", ".woff2", ".srt"}

CACHE_NAMES = {".DS_Store", "Thumbs.db"}


def human(n: float) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "o" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} To"


def find_cache() -> list[Path]:
    """Les caches sont dans des dossiers qu'on ne parcourt pas : on les cherche à part."""
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = Path(dirpath).relative_to(ROOT)
        if rel != Path(".") and rel.parts and rel.parts[0] == ".git":
            dirnames[:] = []
            continue
        if rel.name == "__pycache__":
            out.extend(Path(dirpath).relative_to(ROOT) / f for f in filenames)
            dirnames[:] = []
            continue
        out.extend((rel / f) if str(rel) != "." else Path(f)
                   for f in filenames if f in CACHE_NAMES or f.endswith(".pyc"))
    return out


def walk() -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = Path(dirpath).relative_to(ROOT)
        if rel != Path(".") and rel.name in SKIP_DIRS:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            out.append((rel / name) if str(rel) != "." else Path(name))
    return sorted(out)


def build_corpus(files: list[Path]) -> list[tuple[str, str]]:
    corpus = []
    for rel in files:
        p = ROOT / rel
        if p.suffix.lower() not in TEXT_EXT:
            continue
        try:
            if p.stat().st_size > 3_000_000:
                continue
            corpus.append((str(rel), p.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return corpus


def load_graph() -> tuple[dict | None, dict]:
    """(citations entrantes par fichier, documents marqués périmés).

    `None` quand le graphe n'existe pas. C'est le 25/10 qu'on a vu pourquoi : sans
    `graphify-out/graph.json`, l'ancienne version rendait un dictionnaire vide, donc **tous** les
    documents paraissaient orphelins — le rapport annonçait 743 orphelins, 351 « à traiter », et un
    lecteur pressé en aurait archivé 350. Un fichier absent n'est pas une mesure : c'est une panne.
    """
    if not GRAPH.exists():
        return None, {}
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in g["nodes"]}
    # Comme la carte : on ne compte que les arêtes qui visent le NŒUD FICHIER, pas ses titres.
    file_ids = {n["id"]: n["source_file"] for n in g["nodes"] if n.get("kind")}
    inbound: dict[str, int] = defaultdict(int)
    for e in g["edges"]:
        path = file_ids.get(e.get("target", ""))
        if path:
            inbound[path] += 1
    for n in g["nodes"]:
        if n.get("kind") == "document":
            inbound.setdefault(n["source_file"], 0)
    stale = {}
    sp = GRAPH.parent / "stale.json"
    if sp.exists():
        # stale.json contient des identifiants de nœuds, pas des chemins
        for nid in json.loads(sp.read_text(encoding="utf-8")):
            path = by_id.get(nid, {}).get("source_file")
            if path:
                stale[path] = True
    return inbound, stale


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


DOC_DATE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")
DOC_DATE_FR = re.compile(r"(\d{2})/(\d{2})/(20\d{2})")
FAMILLES = {
    "research/": ("récolte ponctuelle", "archiver après synthèse"),
    "sales/Send-": ("envoi daté d'une campagne finie", "archiver"),
    "sales/VAGUE-": ("envoi daté d'une campagne finie", "archiver"),
    "sales/PLAN-2026-09": ("plan de campagne finie", "archiver"),
    "sales/Passe-Vitrine": ("campagne finie", "archiver"),
    "sales/Expansion-Geography": ("étude de septembre", "archiver"),
    "ops/templates/": ("gabarit réutilisable", "citer depuis la machine"),
    "content/videos/": ("état d'une vidéo livrée", "archiver avec le lot du mois"),
}


def doc_date(rel: Path) -> str:
    """La date d'un document : dans son chemin d'abord (le plus fiable), dans son en-tête ensuite.
    Un document sans date ne peut pas expirer — c'est précisément le défaut que le § ④ corrige."""
    m = DOC_DATE.search(str(rel))
    if m:
        return m.group(0)
    try:
        head = "\n".join((ROOT / rel).read_text(encoding="utf-8", errors="ignore").splitlines()[:12])
    except OSError:
        return "sans date"
    m = DOC_DATE.search(head) or DOC_DATE_FR.search(head)
    if not m:
        return "sans date"
    if m.re is DOC_DATE:
        return m.group(0)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"


def verdict(rel: Path) -> str:
    for pre, (_, v) in FAMILLES.items():
        if str(rel).startswith(pre):
            return v
    if rel.name.startswith("README"):
        return "citer (point d'entrée d'un dossier vivant)"
    return "à décider"


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit des fichiers du dépôt.")
    ap.add_argument("--clean-cache", action="store_true", help="supprime les __pycache__ et *.pyc")
    ap.add_argument("--no-write", action="store_true", help="ne pas écrire le rapport")
    args = ap.parse_args()

    files = walk()
    sizes = {}
    for rel in files:
        try:
            sizes[rel] = (ROOT / rel).stat().st_size
        except OSError:
            sizes[rel] = 0

    cache = find_cache()
    if args.clean_cache:
        for p in cache:
            shutil.rmtree(ROOT / p, ignore_errors=True) if (ROOT / p).is_dir() else (ROOT / p).unlink(missing_ok=True)
        for d in {p.parts[0] for p in cache if "__pycache__" in p.parts}:
            for sub in (ROOT / d).rglob("__pycache__"):
                shutil.rmtree(sub, ignore_errors=True)
        print(f"[audit] caches retirés : {len(cache)} fichier(s)")

    corpus = build_corpus(files)
    inbound, stale = load_graph()

    # doublons exacts
    hashes: dict[str, list[Path]] = defaultdict(list)
    for rel in files:
        if "__pycache__" in rel.parts or sizes.get(rel, 0) < 1024:
            continue
        try:
            hashes[md5(ROOT / rel)].append(rel)
        except OSError:
            continue
    dups = {h: ps for h, ps in hashes.items() if len(ps) > 1}

    # références par nom
    refs: dict[str, int] = {}
    for rel in files:
        name = rel.name
        if rel.suffix.lower() not in MEDIA_EXT:
            continue
        refs[str(rel)] = sum(1 for s, t in corpus if s != str(rel) and name in t)

    media = [(str(p), sizes.get(p, 0), refs.get(str(p), 0)) for p in files
             if p.suffix.lower() in MEDIA_EXT and "__pycache__" not in p.parts]
    unreferenced = [(p, s, r) for p, s, r in media if r == 0]

    docs = [p for p in files if p.suffix.lower() == ".md"]
    mesurable = inbound is not None
    orphans = ([p for p in docs if inbound.get(str(p), 0) == 0 and str(p) != "ops/REPO-MAP.md"]
               if mesurable else [])
    stale_docs = [p for p in docs if str(p) in stale or p.as_posix() in stale]

    zips = [p for p in files if p.suffix.lower() == ".zip"]
    heavy = sorted(((p, sizes.get(p, 0)) for p in files), key=lambda kv: -kv[1])[:20]

    total = sum(sizes.values())
    tracked_big = sum(s for p, s in ((p, sizes[p]) for p in files) if s > 5 * 1024 * 1024)

    L: list[str] = []
    A = L.append
    A("# AUDIT DES FICHIERS — ce qui est mort, ce qui est en double, ce qui coûte")
    A("")
    A("```text")
    A(f"Généré par tools/ops/audit_files.py — {date.today().isoformat()}")
    A(f"{len(files)} fichiers · {human(total)} · dont {human(tracked_big)} dans des fichiers > 5 Mo")
    A("Aucune suppression automatique : les décisions sont listées, pas prises.")
    A("```")
    A("")
    A("## 1 · Ce qui se supprime sans réflexion")
    A("")
    A("| Classe | Fichiers | Poids | Action |")
    A("|---|---|---|---|")
    cache_size = sum((ROOT / c).stat().st_size for c in cache if (ROOT / c).is_file())
    A(f"| caches (`__pycache__`, `*.pyc`) | {len(cache)} | {human(cache_size)} | "
      "`python3 tools/ops/audit_files.py --clean-cache` |")
    A("")

    A("## 2 · Doublons exacts — octet pour octet")
    A("")
    def project(path: Path) -> str:
        """Le « projet » d'un fichier : deux niveaux suffisent pour séparer deux déploiements
        (`hosting/previews/dmoptic` et `hosting/previews/demo-clinique` ne sont pas le même)."""
        parts = path.parts
        if len(parts) > 3 and parts[:2] == ("hosting", "previews"):
            return "/".join(parts[:3])   # chaque aperçu déployé est son propre projet
        return "/".join(parts[:2]) if len(parts) > 2 else "/".join(parts)

    same_project, cross_project = [], []
    for h, ps in dups.items():
        (same_project if len({project(p) for p in ps}) == 1 else cross_project).append(sorted(ps, key=str))
    if same_project:
        A("### Doublons dans le **même** projet — ceux qu'on peut retirer")
        A("")
        A("| Copie gardée | Doublon(s) | Taille unitaire |")
        A("|---|---|---|")
        gain = 0
        for ps in sorted(same_project, key=lambda ps: -sizes.get(ps[0], 0)):
            keep, rest = ps[0], ps[1:]
            gain += sizes.get(keep, 0) * len(rest)
            A(f"| `{keep}` | {', '.join('`' + str(r) + '`' for r in rest)} | {human(sizes.get(keep, 0))} |")
        A("")
        A(f"**Gain : {human(gain)}.**")
        A("")
    else:
        A("Aucun doublon à l'intérieur d'un même projet.")
        A("")
    if cross_project:
        A("### Paires source / déploiement — à garder, mais à surveiller")
        A("")
        A(f"{len(cross_project)} groupes. Le concept vit dans `demos/`, la copie déployée dans "
          "`hosting/previews/`. **Ce n'est pas du gras** : supprimer la copie déployée casse un site. "
          "Le risque réel est la **dérive** — deux copies qui divergent sans qu'on le sache.")
        A("")
        A("| Source | Déploiement | Taille |")
        A("|---|---|---|")
        for ps in sorted(cross_project, key=lambda ps: -sizes.get(ps[0], 0))[:20]:
            A(f"| `{ps[0]}` | {', '.join('`' + str(r) + '`' for r in ps[1:])} | {human(sizes.get(ps[0], 0))} |")
        A("")
    else:
        A("Aucun.")
    A("")

    A("## 3 · Médias sans aucune référence par leur nom")
    A("")
    A(f"{len(unreferenced)} fichiers, {human(sum(s for _, s, _ in unreferenced))}. "
      "**Piste, pas preuve** : un manifeste, un CSS ou un `JSON` peut les appeler autrement.")
    A("")
    by_dir: dict[str, list] = defaultdict(lambda: [0, 0, []])
    for p, s, _ in unreferenced:
        d = str(Path(p).parent)
        by_dir[d][0] += 1
        by_dir[d][1] += s
        if len(by_dir[d][2]) < 3:
            by_dir[d][2].append(Path(p).name)
    A("| Dossier | Fichiers | Poids | Exemples |")
    A("|---|---|---|---|")
    for d, (n, s, ex) in sorted(by_dir.items(), key=lambda kv: -kv[1][1])[:20]:
        A(f"| `{d}/` | {n} | {human(s)} | {', '.join(ex)} |")
    A("")
    A("*Les photos de `clients/dm-optic/photoshoot/` ne sont PAS une rafale : c'est le **catalogue "
      "montures** du client — 160 photos, une par monture (156 montures + 4 vues du cabinet), "
      "395 Mo. Elles sont listées parce qu'elles pèsent, pas parce qu'elles sont mortes : "
      "`sales/Activity-Log.md` (19/10) en garde **84 en réserve** pour le lot 2 du catalogue. "
      "Les supprimer effacerait la source d'un livrable à venir. Ce qui se discute ici, c'est de "
      "les sortir de git (stockage externe), pas de les effacer.*")
    A("")

    A("## 4 · Documents")
    A("")
    A(f"- **{len(orphans)} documents sans citation entrante** — à relire ou à archiver (voir `ops/REPO-MAP.md` §3 bis)."
      if mesurable else
      "- **orphelins : NON MESURÉS** — le graphe des citations est absent (`graphify-out/graph.json`). "
      "Sans lui, tout document paraît orphelin : aucun chiffre ne veut dire quoi que ce soit. "
      "Remède : `python3 tools/graphify/build_full_graph.py`, puis rejouer cet audit.")
    A(f"- **{len(stale_docs)} documents marqués périmés par leur propre texte** — détection lexicale, à vérifier un par un.")
    A("")
    A("| Périmé (d'après lui-même) | Cité par |")
    A("|---|---|")
    for p in sorted(stale_docs, key=lambda p: -(inbound or {}).get(str(p), 0))[:15]:
        A(f"| `{p}` | {(inbound or {}).get(str(p), 0)}× |")
    A("")
    A("⚠️ **Ni l'orphelin ni le « périmé » ne se supprime automatiquement.** Le 24/10, "
      "`AMK-DESIGN-SKILLS.md` était signalé « remplacé par Activity-Log » — c'est faux, et une "
      "suppression sur cette base aurait effacé 1 400 lignes de règles de design.")
    A("")

    # 4 bis · les orphelins datés — le chantier ④ de la carte, mesuré à chaque audit.
    # Sans graphe, on ne mesure pas : on le dit. Un fichier absent produisait sinon 743 orphelins
    # « trouvés » et 351 « à traiter » — de quoi archiver 350 documents vivants sur une panne d'outil.
    A("## 4 bis · Les orphelins datés — ce que personne ne cite, et qui ne peut pas expirer")
    A("")
    if not mesurable:
        A("**Non mesurés.** Le graphe des citations est absent (`graphify-out/graph.json`) : sans lui, "
          "tout document paraît orphelin et aucun chiffre ne veut dire quoi que ce soit. Le reste de ce "
          "rapport (poids, doublons, médias) reste valable ; cette section, non.")
        A("")
        A("```bash")
        A("python3 tools/graphify/build_full_graph.py && python3 tools/ops/audit_files.py")
        A("```")
        A("")
    else:
        normales = ("design/vendor/", "leads/records/", "tools/")
        a_traiter = [p for p in orphans if not str(p).startswith(normales)]
        dates = {p: doc_date(p) for p in a_traiter}
        sans_date = [p for p in a_traiter if dates[p] == "sans date"]
        dated = sorted((p for p in a_traiter if dates[p] != "sans date"), key=lambda p: dates[p])
        fam: dict[str, list[Path]] = defaultdict(list)
        for p in a_traiter:
            parts = str(p).split("/")
            fam["/".join(parts[:2]) if len(parts) > 2 else parts[0] + "/"].append(p)

        A(f"**{len(orphans)} orphelins** au total, mais **{len(a_traiter)} seulement à traiter** : les "
          f"autres sont normaux ({len([p for p in orphans if str(p).startswith('design/vendor/')])} imports "
          f"tiers, {len([p for p in orphans if str(p).startswith('leads/records/')])} fiches CRM reliées par "
          f"la base, {len([p for p in orphans if str(p).startswith('tools/')])} README d'outils installés).")
        A("")
        A(f"- **{len(sans_date)} n'ont aucune date**, ni dans leur chemin, ni dans leurs douze premières "
          "lignes : un document sans date ne peut pas expirer, donc il ne meurt jamais.")
        if dated:
            A(f"- Les {len(dated)} autres s'étalent du **{dates[dated[0]]}** au **{dates[dated[-1]]}**.")
        A("")
        A("| Famille | Orphelins | Le plus ancien | Verdict proposé |")
        A("|---|---|---|---|")
        for k, v in sorted(fam.items(), key=lambda kv: -len(kv[1])):
            ds = sorted(dates[p] for p in v if dates[p] != "sans date")
            old = ds[0] if ds else "sans date"
            A(f"| `{k}` | {len(v)} | {old} | {verdict(v[0])} |")
        A("")
        A("*Le verdict est une **proposition**, pas une décision : archiver = `git mv` vers `archive/`, "
          "jamais supprimer. `archive/` sort du corpus (ni carte, ni portes, ni audit) mais reste dans git.*")
        A("")
        if sans_date:
            A("**Les documents sans date** (à dater ou à archiver) :")
            A("")
            for p in sans_date:
                A(f"- `{p}`")
            A("")

    A("## 5 · Archives et artefacts")
    A("")
    if zips:
        A("| Archive | Taille | Fabriquée par | Contenu |")
        A("|---|---|---|---|")
        for p in zips:
            name = p.name
            maker = next((src for src, txt in corpus
                          if src != str(p) and name in txt
                          and (src.endswith(".py") or src.endswith(".sh"))
                          and "zip" in txt), "—")
            try:
                import zipfile
                with zipfile.ZipFile(ROOT / p) as zf:
                    n = len(zf.namelist())
                    newest = max((i.date_time for i in zf.infolist()), default=None)
                when = f"{newest[0]:04d}-{newest[1]:02d}-{newest[2]:02d}" if newest else "?"
                content = f"{n} fichier(s), plus récent {when}"
            except Exception:
                content = "?"
            A(f"| `{p}` | {human(sizes.get(p, 0))} | {'`' + maker + '`' if maker != '—' else '—'} | {content} |")
        A("")

    A("## 6 · Les 20 plus gros fichiers — ce qui pèse dans l'historique")
    A("")
    A("| Fichier | Taille |")
    A("|---|---|")
    for p, s in heavy:
        A(f"| `{p}` | {human(s)} |")
    A("")
    A("⚠️ **Le `.git` ne perd rien quand on supprime un fichier.** Un binaire retiré reste dans "
      "l'historique ; seul un `git filter-repo` (réécriture + force-push) le retire vraiment. "
      "Tant que ce n'est pas fait, supprimer un gros média allège le disque, pas le dépôt.")
    A("")
    A("---")
    A("")
    A(f"*Rejouable : `python3 tools/ops/audit_files.py`. Rapport précédent à comparer : "
      f"{len(files)} fichiers, {human(total)}.*")

    out = ROOT / "ops" / f"FILE-AUDIT-{date.today().isoformat()}.md"
    if not args.no_write:
        out.write_text("\n".join(L) + "\n", encoding="utf-8")
        print(f"[audit] rapport écrit → {out.relative_to(ROOT)}")

    print(f"[audit] {len(files)} fichiers · {human(total)} · "
          f"{len(cache)} cache(s) · {len(dups)} groupe(s) de doublons · "
          f"{len(unreferenced)} média(s) sans référence · "
          f"{len(orphans) if mesurable else '?':>1} orphelin(s) · "
          f"{len(stale_docs)} périmé(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
