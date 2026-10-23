#!/usr/bin/env python3
"""AMK — shot.py : la porte de design en une commande.

Enveloppe autour de `tools/qa/shot.mjs` : elle règle l'environnement du Chromium embarqué
(les variables ne survivent pas au redémarrage), vérifie que le moteur existe, et rend
le code de sortie de la vérification.

    python3 tools/qa/shot.py hosting/previews/dmoptic/index.html
    python3 tools/qa/shot.py https://example.com --out /tmp/shot --strict

Sans Chromium installé : `bash tools/video/install.sh` (installé une fois par session).
"""
import argparse
import contextlib
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RUNTIME = Path(os.environ.get("AMK_VIDEO_RUNTIME", "/tmp/amk-video"))
ROOT = Path(__file__).resolve().parents[2]


def env() -> dict:
    e = dict(os.environ)
    e["LD_LIBRARY_PATH"] = f"{RUNTIME}/al2023/lib" + ((":" + e["LD_LIBRARY_PATH"]) if e.get("LD_LIBRARY_PATH") else "")
    e["FONTCONFIG_PATH"] = f"{RUNTIME}/fonts"
    return e


def port_libre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@contextlib.contextmanager
def serveur(racine: Path):
    """Sert le dossier du site en HTTP local.

    Pourquoi ce détour : les pages du site utilisent des chemins absolus (`/dm-logo.webp`,
    `/fonts/...`). Ouvertes en `file://`, elles cassent — et l'outil crierait « 4 images cassées »
    sur un site en parfait état. Servi à la racine, tout se résout comme en production.
    """
    handler = lambda *a, **k: SimpleHTTPRequestHandler(*a, directory=str(racine), **k)
    srv = ThreadingHTTPServer(("127.0.0.1", port_libre()), handler)
    srv.RequestHandlerClass.log_message = lambda *a, **k: None
    thread = __import__("threading").Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}"
    finally:
        srv.shutdown()


def moteur_absent() -> bool:
    return not (RUNTIME / "node_modules" / "puppeteer-core").is_dir() or not (RUNTIME / "node_modules" / "@sparticuz" / "chromium").is_dir()


def main() -> int:
    ap = argparse.ArgumentParser(description="Vérification de design dans un vrai navigateur")
    ap.add_argument("cible", help="fichier HTML local ou URL (un fichier local est servi en HTTP à la racine du site)")
    ap.add_argument("--out", default="/tmp/amk-shot", help="dossier des captures")
    ap.add_argument("--strict", action="store_true", help="un P2 suffit à faire échouer")
    a = ap.parse_args()

    if moteur_absent():
        print("✗ Chromium embarqué absent. Lancer : bash tools/video/install.sh", file=sys.stderr)
        return 2
    if shutil.which("node") is None:
        print("✗ node introuvable", file=sys.stderr)
        return 2

    os.makedirs(a.out, exist_ok=True)

    cible = a.cible
    ctx = contextlib.nullcontext()
    if not cible.startswith(("http://", "https://")):
        f = Path(cible).resolve()
        if not f.is_file():
            print(f"✗ fichier introuvable : {cible}", file=sys.stderr)
            return 2
        # Racine = le dossier du site, pas celui de la page.
        # Marqueur fiable : `404.html` à la racine (toutes nos pages statiques en ont une).
        # À défaut, on prend l'ancêtre le plus haut qui contient un index.html, sans sortir du dépôt.
        racine = None
        for parent in f.parents:
            if (parent / ".git").is_dir():
                break
            if (parent / "404.html").is_file():
                racine = parent
            elif racine is None and (parent / "index.html").is_file():
                racine = parent
        if racine is None:
            racine = f.parent
        ctx = serveur(racine)
        base = ctx.__enter__()
        cible = base + "/" + str(f.relative_to(racine)).replace(os.sep, "/")
        print(f"▸ servi à la racine : {racine} → {cible}")

    cmd = ["node", str(ROOT / "tools" / "qa" / "shot.mjs"), "--url", cible, "--out", a.out]
    if a.strict:
        cmd.append("--strict")
    try:
        r = subprocess.run(cmd, env=env())
    finally:
        if ctx is not None:
            ctx.__exit__(None, None, None)
    rap = Path(a.out) / "rapport.json"
    if rap.is_file():
        d = json.loads(rap.read_text())
        print(f"→ {d['verdict']} · {d['totals']['p1']} P1 · {d['totals']['p2']} P2 · {d['totals']['p3']} P3")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
