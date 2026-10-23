#!/usr/bin/env python3
"""AMK — DESIGN.md en une commande, depuis une page du dépôt ou une URL.

L'enveloppe fait trois choses que `extract.mjs` ne peut pas faire seul :
  1. elle règle l'environnement du Chromium embarqué (comme `tools/qa/shot.py`) ;
  2. si on lui donne un dossier ou un fichier, elle **sert le site en HTTP local** — les pages du
     dépôt utilisent des chemins absolus (`/fonts/…`) qui cassent en `file://` ;
  3. elle nomme la marque, sinon le `DESIGN.md` s'appelle « Untitled system ».

    python3 tools/design-md/extract.py hosting/previews/dmoptic --name "DM OPTIQUE SARL"
    python3 tools/design-md/extract.py hosting/previews/dmoptic/index.html --out /tmp/dm-design
"""
import argparse
import contextlib
import os
import socket
import subprocess
import sys
import threading
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
    handler = lambda *a, **k: SimpleHTTPRequestHandler(*a, directory=str(racine), **k)
    srv = ThreadingHTTPServer(("127.0.0.1", port_libre()), handler)
    srv.RequestHandlerClass.log_message = lambda *a, **k: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}"
    finally:
        srv.shutdown()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="dossier, fichier .html, ou URL")
    ap.add_argument("--out", default="/tmp/designmd")
    ap.add_argument("--name", default="")
    args = ap.parse_args()

    cible = Path(args.target)
    if args.target.startswith("http"):
        url = args.target
    else:
        # racine = dossier contenant 404.html, sinon le dossier du fichier
        base = cible if cible.is_dir() else cible.parent
        if not (base / "404.html").exists() and base.parent != base:
            for parent in base.parents:
                if (parent / "404.html").exists():
                    base = parent
                    break
        rel = cible.relative_to(base) if cible != base else Path("index.html")
        with serveur(base) as base_url:
            url = f"{base_url}/{(rel.as_posix() if rel.name != 'index.html' or rel.parent != Path('.') else 'index.html')}"
            return run(url, args)
    return run(url, args)


def run(url: str, args) -> int:
    cmd = ["node", str(ROOT / "tools/design-md/extract.mjs"), url, "--out", args.out]
    if args.name:
        cmd += ["--name", args.name]
    return subprocess.call(cmd, env=env())


if __name__ == "__main__":
    sys.exit(main())
