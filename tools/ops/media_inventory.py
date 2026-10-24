#!/usr/bin/env python3
"""media_inventory.py — les médias par empreinte, pas par nom.

Le problème, mesuré le 24/10 : 460 médias suivis, 104 Mo sur un arbre de 144 Mo. On les retrouve par
nom (« B1-entree-cabinet.png »), donc un fichier renommé est un fichier perdu, deux copies sont deux
inconnues, et 66 d'entre eux ne sont nommés par aucun document.

Ce que fait cet outil : il calcule l'empreinte (sha256) et les dimensions de chaque média suivi, puis
écrit un `MEDIA.md` par dossier. Trois choses deviennent alors visibles :

1. **les doublons exacts** — même empreinte = même fichier. Un seul est l'original, les autres sont des
   copies à remplacer par une référence ;
2. **les orphelins** — un média que nul document ne nomme. Il existe, mais rien ne mène à lui ;
3. **ce qui vit hors du dépôt** — un fichier dont l'original est ailleurs (téléphone, disque) le dit,
   au lieu de laisser croire que le dépôt est complet.

    python3 tools/ops/media_inventory.py                # écrit les MEDIA.md
    python3 tools/ops/media_inventory.py --check        # sort 1 si un MEDIA.md est périmé
    python3 tools/ops/media_inventory.py --doublons     # ne montre que les empreintes partagées
    python3 tools/ops/media_inventory.py --thumbs DIR   # vignettes 800 px dans DIR (jamais dans git)

Aucune dépendance : les dimensions se lisent dans l'en-tête du fichier (PNG, JPEG, WebP, GIF).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import struct
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                           check=True).stdout.strip())
MARK = "<!-- généré par tools/ops/media_inventory.py — ne pas éditer à la main -->"
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MEDIA_EXT = IMAGE_EXT | {".svg", ".mp4", ".mov", ".webm", ".mp3", ".wav", ".ttf", ".otf", ".pdf"}
# en dessous de ce poids, un dossier n'a pas besoin d'un inventaire : la question ne se pose pas
SEUIL_DOSSIER_MO = 2.0
SEUIL_TABLE_MO = 0.3


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
    return [f for f in out.split("\0") if f]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dimensions(path: Path) -> tuple[int, int] | None:
    """Largeur × hauteur lues dans l'en-tête, sans bibliothèque d'image."""
    try:
        with path.open("rb") as fh:
            head = fh.read(32)
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                w, h = struct.unpack(">II", head[16:24])
                return w, h
            if head[:6] in (b"GIF87a", b"GIF89a"):
                w, h = struct.unpack("<HH", head[6:10])
                return w, h
            if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
                fh.seek(12)
                chunk = fh.read(16)
                if chunk[:4] == b"VP8X":
                    w = int.from_bytes(chunk[8:11], "little") + 1
                    h = int.from_bytes(chunk[11:14], "little") + 1
                    return w, h
                if chunk[:4] == b"VP8 ":
                    fh.seek(26)
                    w, h = struct.unpack("<HH", fh.read(4))
                    return w & 0x3FFF, h & 0x3FFF
                if chunk[:4] == b"VP8L":
                    b = chunk[9:13]
                    bits = int.from_bytes(b, "little")
                    return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
            if head[:2] == b"\xff\xd8":  # JPEG : on marche les segments jusqu'à un SOFn
                fh.seek(2)
                while True:
                    b = fh.read(1)
                    if not b:
                        return None
                    if b != b"\xff":
                        continue
                    marker = fh.read(1)
                    while marker == b"\xff":
                        marker = fh.read(1)
                    if not marker:
                        return None
                    if marker[0] in (0xD8, 0xD9) or 0xD0 <= marker[0] <= 0xD7:
                        continue
                    seg = fh.read(2)
                    if len(seg) < 2:
                        return None
                    length = struct.unpack(">H", seg)[0]
                    if marker[0] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                                     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        data = fh.read(5)
                        h, w = struct.unpack(">HH", data[1:5])
                        return w, h
                    fh.seek(length - 2, os.SEEK_CUR)
    except (OSError, struct.error):
        return None
    return None


def human(n: float) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if n < 1024 or unit == "Go":
            return f"{n:.0f} {unit}" if unit == "o" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} Go"


def corpus_texts(files: list[str]) -> list[tuple[str, str]]:
    out = []
    for f in files:
        if os.path.splitext(f)[1].lower() not in (".md", ".py", ".sh", ".json", ".html", ".yml", ".yaml", ".txt"):
            continue
        try:
            out.append((f, (ROOT / f).read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return out


def scan() -> tuple[dict, dict]:
    files = tracked()
    media = [f for f in files if os.path.splitext(f)[1].lower() in MEDIA_EXT]
    texts = corpus_texts(files)
    rows = {}
    for f in media:
        p = ROOT / f
        try:
            st = p.stat()
        except OSError:
            continue
        name = os.path.basename(f)
        cited = sum(1 for src, txt in texts if src != f and name in txt)
        rows[f] = dict(size=st.st_size, sha=sha256(p), dims=dimensions(p), cited=cited,
                       ext=os.path.splitext(f)[1].lower())
    return rows, {f: t for f, t in texts}


def render(dirname: str, rows: dict, hashes: dict[str, list[str]]) -> str:
    paths = sorted(p for p in rows if os.path.dirname(p) == dirname)
    total = sum(rows[p]["size"] for p in paths)
    L = [MARK, "", f"# MÉDIAS — `{dirname}/`", ""]
    L.append(f"**{len(paths)} fichier(s) · {human(total)}.** Empreinte = identité du fichier : deux "
             "fichiers de même empreinte sont le même fichier, quelle que soit leur adresse.")
    L.append("")
    dups = {p: hashes[rows[p]["sha"]] for p in paths if len(hashes[rows[p]["sha"]]) > 1}
    sans = [p for p in paths if rows[p]["cited"] == 0]
    # « Où vit l'original » : quand un registre de retrait existe dans le dossier, il le dit, et
    # l'inventaire renvoie à lui au lieu de laisser croire que le dépôt est complet.
    dossier = ROOT / dirname
    retraits = sorted(dossier.glob("RETRAIT-*.md")) if dossier.is_dir() else []
    if retraits:
        L.append(f"**Origine** : les fichiers retirés de git sont inscrits dans "
                 f"`{retraits[0].name}` — l'original vit hors du dépôt, sa ligne dit où.")
        L.append("")
    L.append(f"- **{len(dups)} fichier(s) en double** (même empreinte qu'un autre média du dépôt)")
    L.append(f"- **{len(sans)} média(s) que nul document ne nomme**")
    L.append("")
    # Dans un dossier de 130 fichiers, lister tout noie ; ne lister que les gros ne dit rien.
    # On liste donc TOUT ce qui dépasse le seuil, PLUS les 20 plus gros — jamais une table vide.
    gros = {p for p in paths if rows[p]["size"] >= SEUIL_TABLE_MO * 1048576}
    plus_lourds = set(sorted(paths, key=lambda p: -rows[p]["size"])[:20])
    montres = sorted(gros | plus_lourds)
    L.append("| Fichier | Dimensions | Poids | Empreinte | Citations |")
    L.append("|---|---|---|---|---|")
    for p in montres:
        r = rows[p]
        d = f'{r["dims"][0]}×{r["dims"][1]}' if r["dims"] else "—"
        L.append(f'| `{os.path.basename(p)}` | {d} | {human(r["size"])} | `{r["sha"][:12]}` | '
                 f'{r["cited"] or "**0**"} |')
    if len(paths) > len(montres):
        L.append("")
        L.append(f"*{len(paths) - len(montres)} fichier(s) de moins de "
                 f"{int(SEUIL_TABLE_MO * 1024)} Ko et hors des 20 plus lourds ne sont pas listés : "
                 "l'empreinte complète se recalcule en une commande.*")
    if dups:
        L.append("")
        L.append("## Empreintes partagées — un seul original, les autres sont des copies")
        L.append("")
        seen = set()
        for p, group in dups.items():
            key = rows[p]["sha"]
            if key in seen:
                continue
            seen.add(key)
            L.append(f"- `{rows[p]['sha'][:12]}` — {len(group)} copies : " +
                     ", ".join(f"`{os.path.relpath(g, dirname)}`" if os.path.dirname(g) == dirname
                               else f"`{g}`" for g in group))
    if sans:
        L.append("")
        L.append("## Ce que rien ne nomme")
        L.append("")
        L.append("Un média non nommé n'est pas inutile : il est inatteignable. Soit on le cite là où il "
                 "sert, soit il n'a rien à faire ici.")
        L.append("")
        for p in sorted(sans, key=lambda p: -rows[p]["size"])[:15]:
            L.append(f"- `{os.path.basename(p)}` — {human(rows[p]['size'])}")
        if len(sans) > 15:
            L.append(f"- … et {len(sans) - 15} autre(s)")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventaire des médias par empreinte.")
    ap.add_argument("--check", action="store_true", help="sort 1 si un MEDIA.md ne correspond plus")
    ap.add_argument("--doublons", action="store_true", help="n'affiche que les empreintes partagées")
    ap.add_argument("--thumbs", metavar="DIR", help="écrit des vignettes 800 px dans DIR (hors git)")
    ap.add_argument("--write", action="store_true", help="écrit les MEDIA.md")
    args = ap.parse_args()

    rows, _ = scan()
    hashes: dict[str, list[str]] = defaultdict(list)
    for p, r in rows.items():
        hashes[r["sha"]].append(p)
    hashes = dict(hashes)
    groups = {k: sorted(v) for k, v in hashes.items() if len(v) > 1}

    by_dir: dict[str, list[str]] = defaultdict(list)
    for p in rows:
        by_dir[os.path.dirname(p)].append(p)

    if args.doublons:
        poids = sum(rows[g[0]]["size"] * (len(g) - 1) for g in groups.values())
        print(f"{len(groups)} empreinte(s) partagée(s) · {sum(len(g) - 1 for g in groups.values())} "
              f"copie(s) inutile(s) · {human(poids)} récupérables")
        for g in sorted(groups.values(), key=lambda g: -rows[g[0]]["size"]):
            print(f"\n  {rows[g[0]]['sha'][:12]}  {human(rows[g[0]]['size'])} × {len(g)}")
            for p in g:
                print(f"    {p}")
        return 0

    if args.thumbs:
        out = Path(args.thumbs)
        out.mkdir(parents=True, exist_ok=True)
        done = skip = 0
        for p, r in rows.items():
            if r["ext"] not in IMAGE_EXT:
                continue
            dest = out / (Path(p).stem + ".jpg")
            if dest.exists():
                skip += 1
                continue
            if subprocess.run(["convert", str(ROOT / p) + "[0]", "-resize", "800x800>",
                               "-quality", "82", str(dest)], capture_output=True).returncode == 0:
                done += 1
        print(f"vignettes : {done} écrite(s) · {skip} déjà là · dans {out} (hors dépôt)")
        return 0

    cibles = sorted(d for d, ps in by_dir.items()
                    if sum(rows[p]["size"] for p in ps) >= SEUIL_DOSSIER_MO * 1048576)
    stale = []
    for d in cibles:
        target = ROOT / d / "MEDIA.md"
        content = render(d, rows, hashes)
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        if old != content:
            stale.append(d)
            if args.write and not args.check:
                target.write_text(content, encoding="utf-8")

    poids_dup = sum(rows[g[0]]["size"] * (len(g) - 1) for g in groups.values())
    sans = [p for p, r in rows.items() if r["cited"] == 0]
    print(f"{len(rows)} médias suivis · {human(sum(r['size'] for r in rows.values()))} · "
          f"{len(cibles)} dossier(s) au-dessus de {int(SEUIL_DOSSIER_MO)} Mo · "
          f"{len(groups)} empreinte(s) partagée(s) ({human(poids_dup)} en copies) · "
          f"{len(sans)} média(s) que rien ne nomme")

    if args.check:
        if stale:
            for d in stale:
                print(f"  ⛔ {d}/MEDIA.md — périmé (médias ajoutés, retirés ou renommés depuis)")
            print("     → python3 tools/ops/media_inventory.py --write")
            return 1
        print(f"  ✓ les {len(cibles)} inventaires sont à jour")
        return 0

    if not args.write:
        for d in stale:
            print(f"  · {d}/MEDIA.md — à écrire ou à rafraîchir")
    return 0


if __name__ == "__main__":
    sys.exit(main())
