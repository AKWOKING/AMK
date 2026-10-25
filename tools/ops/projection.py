#!/usr/bin/env python3
"""La salle de projection — regarder les masters depuis le navigateur, sans rien déployer.

Pourquoi cet outil existe (tour 149)
------------------------------------
Les masters `*.mp4` sont **gitignorés** : ils ne voyagent pas avec le dépôt, et ils ne survivent pas
au redémarrage d'un bac (tour 149 : « where is the mp4 video that I can watch » — le fichier rendu la
veille n'était plus là). Ils se **régénèrent** (`make_ep01.py`, ~30 s) mais ne se **transportent** pas.

Cet outil ne résout pas la persistance : il résout la **question**. Il sert `content/reels/` en HTTP
sur `0.0.0.0`, avec une page qui liste tous les masters présents et les joue en `<video>` — donc
regardables depuis un téléphone, sans copier de fichier, sans compte, sans réseau.

    python3 tools/ops/projection.py                 # http://<hôte>:8000/
    python3 tools/ops/projection.py --port 8080
    python3 tools/ops/projection.py --racine content/reels

Ce qu'il ne fait pas : aucun transcodage, aucun envoi, aucune écriture. Il lit et il sert. S'il n'y a
aucun master, la page le dit et rappelle la commande de rendu — au lieu d'afficher une page vide.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
DEFAUT = ROOT / "content" / "reels"
VIDEOS = (".mp4", ".webm", ".mov")


def ffmpeg_exe() -> str | None:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def duree(path: Path) -> float | None:
    """Durée en secondes, lue par ffmpeg (aucune dépendance à ffprobe)."""
    exe = ffmpeg_exe()
    if not exe:
        return None
    try:
        out = subprocess.run(
            [exe, "-i", str(path)], capture_output=True, text=True, timeout=30
        ).stderr
    except Exception:
        return None
    for ligne in out.splitlines():
        if "Duration:" in ligne:
            brut = ligne.split("Duration:")[1].split(",")[0].strip()
            h, m, s = brut.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return None


def masters(racine: Path) -> list[dict]:
    trouves = []
    for p in sorted(racine.rglob("*")):
        if p.suffix.lower() not in VIDEOS or not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        trouves.append(
            {
                "nom": p.name,
                "chemin": rel,
                "octets": p.stat().st_size,
                "mtime": p.stat().st_mtime,
                "duree": duree(p),
                "fils": sum(1 for _ in p.parent.glob("*.mp4")),
            }
        )
    return trouves


def page(racine: Path, liste: list[dict]) -> bytes:
    lignes = []
    for m in liste:
        taille = f"{m['octets'] / 1e6:.1f} Mo"
        duree = f"{m['duree']:.1f} s" if m["duree"] else "durée inconnue"
        lignes.append(
            f"""      <article>
        <h2>{html.escape(m['nom'])}</h2>
        <p class="meta">{html.escape(str(Path(m['chemin']).parent))} · {duree} · {taille}</p>
        <video controls preload="metadata" playsinline src="/{html.escape(m['chemin'])}"></video>
      </article>"""
        )
    if not lignes:
        corps = f"""      <p class="vide">Aucun master dans <code>{html.escape(str(racine))}</code>.
        Les <code>.mp4</code> sont gitignorés : ils ne survivent pas à un redémarrage. Pour en refaire un :
        <code>python3 content/reels/ep01/make_ep01.py</code> (≈ 30 s).</p>"""
    else:
        corps = "\n".join(lignes)

    doc = f"""<!doctype html>
<html lang="fr">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Salle de projection — {len(liste)} master(s)</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#0b0d10; color:#e9edf2;
         font:16px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
  header {{ padding:28px 20px 8px; max-width:1100px; margin:0 auto; }}
  h1 {{ font-size:22px; margin:0 0 6px; letter-spacing:-.01em; }}
  .sous {{ color:#8b96a5; font-size:14px; margin:0; }}
  main {{ max-width:1100px; margin:0 auto; padding:12px 20px 60px;
          display:grid; gap:26px; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); }}
  article {{ background:#12161b; border:1px solid #1e252e; border-radius:14px; overflow:hidden; }}
  h2 {{ font-size:15px; margin:0; padding:14px 16px 2px; font-weight:600; }}
  .meta {{ margin:0; padding:0 16px 12px; color:#8b96a5; font-size:12.5px; }}
  video {{ width:100%; display:block; background:#000; aspect-ratio:9/16; max-height:78vh; }}
  .vide {{ grid-column:1/-1; background:#12161b; border:1px dashed #2a333f; border-radius:14px;
           padding:20px; color:#c3ccd8; }}
  code {{ background:#1b222b; padding:2px 6px; border-radius:5px; font-size:13px; }}
  footer {{ max-width:1100px; margin:0 auto; padding:0 20px 40px; color:#6f7b8a; font-size:12.5px; }}
</style>
<header>
  <h1>Salle de projection</h1>
  <p class="sous">{len(liste)} master(s) dans <code>{html.escape(str(racine))}</code> — rien n'est envoyé nulle part,
     les fichiers sont servis tels quels.</p>
</header>
<main>
{corps}
</main>
<footer>Les <code>.mp4</code> sont gitignorés : cette page est toujours à jour de ce qui existe sur le disque,
  jamais de ce qui a été rendu hier.</footer>
</html>
"""
    return doc.encode("utf-8")


class Salle(SimpleHTTPRequestHandler):
    racine = DEFAUT

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_GET(self):  # noqa: N802
        if urlparse(self.path).path in ("/", "/index.html"):
            corps = page(Salle.racine, masters(Salle.racine))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corps)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(corps)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("· %s\n" % (fmt % args))


def main() -> int:
    ap = argparse.ArgumentParser(description="Sert les masters dans une page qui les joue.")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--hote", default="0.0.0.0")
    ap.add_argument("--racine", default=str(DEFAUT))
    ap.add_argument("--liste", action="store_true", help="liste les masters et sort")
    a = ap.parse_args()

    racine = Path(a.racine).resolve()
    if not racine.is_dir():
        sys.exit(f"racine absente : {racine}")
    Salle.racine = racine

    if a.liste:
        liste = masters(racine)
        print(json.dumps(liste, ensure_ascii=False, indent=2))
        return 0 if liste else 1

    n = len(masters(racine))
    srv = ThreadingHTTPServer((a.hote, a.port), Salle)
    print(f"— salle de projection : http://{a.hote}:{a.port}/ · {n} master(s) · racine {racine}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n— arrêt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
