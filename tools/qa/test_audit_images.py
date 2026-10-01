#!/usr/bin/env python3
"""Le témoin du contrôle des images — lot [32].

Un outil qui trouve 0 constat doit prouver qu'il mord. Ce test fabrique de vraies structures JPEG et
PNG dans /tmp (sans dépendance : ni Pillow, ni ImageMagick), monte une page saine, puis casse une
chose à la fois et vérifie que l'outil la nomme :

  1. page saine, dimensions annoncées = dimensions réelles          → aucune faute
  2. ratio annoncé différent du ratio réel                          → ERR (le navigateur recadrerait)
  3. taille absolue fausse, ratio juste (800×500 pour 1024×640)     → WARN, et rc=1 en --strict
  4. métadonnées GPS (position de prise de vue)                     → ERR
  5. autres métadonnées EXIF (appareil, horodatage)                 → WARN
  6. photo de téléphone non traitée (420 Ko)                        → ERR
  7. fichier annoncé par la page et absent                          → ERR
  8. srcset qui annonce « 800w » pour un fichier de 1024 px         → WARN
  9. variante -sm orpheline, et variante -sm plus lourde que l'original → ERR (mode dossier)

Règle de la maison, écrite ici parce qu'elle s'y est déjà cassée cinq fois : **une assertion ne
compare jamais une chaîne sensible à la casse** — on compare en minuscules.
"""

import base64
import os
import struct
import subprocess
import sys
import tempfile

TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_images.py")
ok = fail = 0


def check(cond, label):
    global ok, fail
    if cond:
        ok += 1
        print("  ok   " + label)
    else:
        fail += 1
        print("  FAIL " + label)


# ─────────────────────────── fabrique d'images (structure seule, pas de pixels) ───────────────────────────

def exif_segment(kind):
    """kind: 'none' | 'plain' | 'gps' — un vrai segment APP1/Exif, minimal mais conforme à la structure."""
    if kind == "none":
        return b""          # aucun segment APP1 : « sans métadonnées » doit vouloir dire sans métadonnées
    entries = []
    if kind == "gps":
        entries.append(struct.pack("<HHI", 0x8825, 4, 1) + struct.pack("<I", 0))
    if kind == "plain":
        entries.append(struct.pack("<HHI", 0x0112, 3, 1) + struct.pack("<I", 1))
    ifd = struct.pack("<H", len(entries)) + b"".join(entries) + struct.pack("<I", 0)
    tiff = b"II" + struct.pack("<HI", 42, 8) + ifd
    payload = b"Exif\x00\x00" + tiff
    return b"\xff\xe1" + struct.pack(">H", len(payload) + 2) + payload


def jpeg(width, height, exif="none", pad=0):
    sof = (b"\xff\xc0" + struct.pack(">H", 11) + b"\x08" +
           struct.pack(">HH", height, width) + b"\x01\x01\x11\x00")
    data = b"\xff\xd8" + exif_segment(exif) + sof + b"\xff\xd9"
    return data + b"\x00" * pad


def png(width, height):
    ihdr = struct.pack(">II", width, height) + b"\x08\x02\x00\x00\x00"
    return (b"\x89PNG\r\n\x1a\n" + struct.pack(">I", len(ihdr)) + b"IHDR" + ihdr + b"\x00\x00\x00\x00" +
            struct.pack(">I", 0) + b"IEND" + b"\x00\x00\x00\x00")


def write(path, data):
    with open(path, "wb") as fh:
        fh.write(data)


def write_html(path, body):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def run(*args):
    r = subprocess.run([sys.executable, TOOL] + list(args), capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).lower()


def main():
    tmp = tempfile.mkdtemp(prefix="amk-img-")

    # 1 · page saine
    write(os.path.join(tmp, "saine.jpg"), jpeg(1024, 640))
    write(os.path.join(tmp, "saine-sm.jpg"), jpeg(640, 400))
    write_html(os.path.join(tmp, "page-saine.html"),
          '<img src="saine.jpg" srcset="saine-sm.jpg 640w, saine.jpg 1024w" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "page-saine.html"))
    check(rc == 0 and "aucune faute" in out, "page saine : rc=0, aucun constat")

    # 2 · ratio annoncé faux → ERR
    write_html(os.path.join(tmp, "ratio.html"), '<img src="saine.jpg" width="1024" height="512">')
    rc, out = run(os.path.join(tmp, "ratio.html"))
    check(rc == 1 and "ratio annoncé" in out, "ratio différent : ERR (recadrage par le navigateur)")

    # 3 · taille absolue fausse, ratio juste → WARN (rc=0), puis rc=1 en --strict
    write_html(os.path.join(tmp, "absolu.html"), '<img src="saine.jpg" width="800" height="500">')
    rc, out = run(os.path.join(tmp, "absolu.html"))
    check(rc == 0 and "annonce 800x500" in out, "dimensions absolues fausses : WARN, rc=0")
    rc, out = run("--strict", os.path.join(tmp, "absolu.html"))
    check(rc == 1, "--strict : le même avertissement ferme la porte (rc=1)")

    # 4 · GPS → ERR puis 5 · EXIF simple → WARN
    write(os.path.join(tmp, "gps.jpg"), jpeg(1024, 640, exif="gps"))
    write_html(os.path.join(tmp, "gps.html"), '<img src="gps.jpg" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "gps.html"))
    check(rc == 1 and "gps" in out, "métadonnées GPS : ERR (vie privée)")
    write(os.path.join(tmp, "exif.jpg"), jpeg(1024, 640, exif="plain"))
    write_html(os.path.join(tmp, "exif.html"), '<img src="exif.jpg" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "exif.html"))
    check(rc == 0 and "exif" in out, "EXIF sans GPS : WARN, pas une faute")

    # 6 · photo de téléphone non traitée → ERR
    write(os.path.join(tmp, "lourde.jpg"), jpeg(1024, 640, pad=420 * 1024))
    write_html(os.path.join(tmp, "lourde.html"), '<img src="lourde.jpg" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "lourde.html"))
    check(rc == 1 and "budget" in out, "photo de 420 Ko : ERR (budget 400 Ko)")

    # 7 · fichier absent → ERR
    write_html(os.path.join(tmp, "absent.html"), '<img src="jamais-livree.jpg" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "absent.html"))
    check(rc == 1 and "introuvable" in out, "fichier absent : ERR")

    # 8 · srcset menteur → WARN
    write_html(os.path.join(tmp, "srcset.html"),
          '<img src="saine.jpg" srcset="saine.jpg 800w" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "srcset.html"))
    check(rc == 0 and "srcset annonce" in out, "srcset menteur : WARN")

    # 9 · mode dossier : orpheline, et -sm plus lourde que l'original
    folder = os.path.join(tmp, "dossier")
    os.makedirs(folder)
    write(os.path.join(folder, "orpheline-sm.jpg"), jpeg(640, 400))
    write(os.path.join(folder, "pese.jpg"), jpeg(1024, 640, pad=60 * 1024))
    write(os.path.join(folder, "pese-sm.jpg"), jpeg(640, 400, pad=150 * 1024))
    write(os.path.join(folder, "paire.jpg"), jpeg(1024, 640))
    write(os.path.join(folder, "paire-sm.jpg"), jpeg(640, 400))
    rc, out = run("--dir", folder)
    check("orpheline" in out and "sans fichier plein" in out, "dossier : variante -sm orpheline = ERR")
    check("plus large" in out or "plus lourde" in out, "dossier : -sm plus lourde que l'original = ERR")
    check(rc == 1, "dossier fautif : rc=1")

    # 10 · PNG lu lui aussi
    write(os.path.join(tmp, "nette.png"), png(1024, 640))
    write_html(os.path.join(tmp, "png.html"), '<img src="nette.png" width="1024" height="640">')
    rc, out = run(os.path.join(tmp, "png.html"))
    check(rc == 0, "PNG correct : rc=0 (les deux formats sont lus)")

    # 11 · image EMBARQUÉE en base64 — elle échappait au contrôle jusqu'au 24/09 (La Ligne Optic :
    # dix images embarquées, et l'outil annonçait « 0 image(s) »)
    def b64(data):
        return base64.b64encode(data).decode("ascii")

    write_html(os.path.join(tmp, "b64-saine.html"),
               '<img src="data:image/jpeg;base64,%s" width="1024" height="640">' % b64(jpeg(1024, 640)))
    rc, out = run(os.path.join(tmp, "b64-saine.html"))
    check(rc == 0 and "1 image(s)" in out, "base64 saine : comptée (1 image), aucun constat")
    write_html(os.path.join(tmp, "b64-lourde.html"),
               '<img src="data:image/jpeg;base64,%s" width="1024" height="640">'
               % b64(jpeg(1024, 640, pad=420 * 1024)))
    rc, out = run(os.path.join(tmp, "b64-lourde.html"))
    check(rc == 1 and "budget" in out, "base64 de 420 Ko : ERR (budget 400 Ko)")
    write_html(os.path.join(tmp, "b64-gps.html"),
               '<img src="data:image/jpeg;base64,%s" width="1024" height="640">'
               % b64(jpeg(1024, 640, exif="gps")))
    rc, out = run(os.path.join(tmp, "b64-gps.html"))
    check(rc == 1 and "gps" in out, "base64 avec GPS : ERR (vie privée)")
    write_html(os.path.join(tmp, "b64-ratio.html"),
               '<img src="data:image/jpeg;base64,%s" width="1024" height="512">' % b64(jpeg(1024, 640)))
    rc, out = run(os.path.join(tmp, "b64-ratio.html"))
    check(rc == 1 and "ratio annoncé" in out, "base64 : ratio annoncé faux = ERR")

    print("\n%d assertion(s) verte(s), %d échec(s) — le contrôle des images mord sur les onze pièges."
          % (ok, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
