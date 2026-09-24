#!/usr/bin/env python3
"""Le contrôle des photographies livrées — lot [32], 24/09/2026.

Pourquoi cet outil existe : à partir du 25/09 les photos d'UNI-LABO ne seront plus des images
générées mais **des photographies prises dans leur laboratoire au Pixel 8A de King**. Une photo de
téléphone pèse 3 à 6 Mo, porte l'heure, le modèle de l'appareil et souvent **la position GPS** — trois
choses qu'on ne publie pas. Et une photo livrée au mauvais format casse la page (saut de mise en page)
ou repart dans le zip de déploiement à 4 Mo.

Ce que l'outil vérifie, et rien d'autre :
  1. le fichier existe, et c'est bien un JPEG ou un PNG (pas un PDF renommé) ;
  2. **le ratio annoncé par la page = le ratio réel du fichier** (sinon la photo est recadrée par le
     navigateur, exactement ce que §25.2④ interdit) ; un écart de taille absolue est un WARN, pas une
     faute : le ratio tient, mais l'annonce est fausse et pourrira au prochain recadrage ;
  3. les descripteurs `srcset` (`640w`, `800w`…) correspondent à la largeur réelle ;
  4. le poids : budget **400 Ko** pour une image pleine, **200 Ko** pour une variante `-sm`
     (une photo de téléphone non traitée = ERR) ;
  5. **métadonnées EXIF** : GPS présent = ERR (on ne publie pas l'endroit d'où la photo a été prise,
     ni le numéro de série de l'appareil) ; EXIF quelconque = WARN (à nettoyer avant publication) ;
  6. en mode dossier : une variante `-sm` orpheline (sans fichier plein) = ERR, et une variante `-sm`
     plus large ou plus lourde que son original = ERR.

Ce que l'outil ne fait PAS : décoder les pixels. Il ne juge ni la netteté, ni le cadrage, ni la
lumière — « la qualité d'une photo se juge à l'œil », et l'alt text se juge à la lecture (§27). Un
fichier accepté ici peut être une photo très laide.

Usage :
    python3 tools/qa/audit_images.py [--strict] <pages .html ...>            # lit les <img> des pages
    python3 tools/qa/audit_images.py --dir <dossier> [--dir <dossier> ...]   # lit un dossier d'images
`--strict` : rc=1 dès une faute OU un avertissement (porte technique).
"""

import os
import re
import struct
import sys

BUDGET_FULL = 400 * 1024      # une image pleine ne dépasse pas 400 Ko
BUDGET_SM = 200 * 1024        # une variante téléphone ne dépasse pas 200 Ko
RATIO_TOL = 0.01              # 1 % de tolérance sur le ratio annoncé


# ─────────────────────────────── lecture des en-têtes, sans dépendance ───────────────────────────────

def jpeg_info(data):
    """(largeur, hauteur, exif, gps) d'un JPEG, lus dans les segments. None si ce n'est pas un JPEG."""
    if data[:2] != b"\xff\xd8":
        return None
    i, n = 2, len(data)
    w = h = None
    exif = gps = False
    while i < n - 3:
        if data[i] != 0xFF:
            i += 1
            continue
        m = data[i + 1]
        if m == 0xFF:                      # octet de remplissage
            i += 1
            continue
        if m == 0xD9:                      # fin d'image
            break
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        ln = struct.unpack(">H", data[i + 2:i + 4])[0]
        seg = data[i + 4:i + 2 + ln]
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC) and len(seg) >= 5:
            h, w = struct.unpack(">HH", seg[1:5])
        elif m == 0xE1 and seg.startswith(b"Exif\x00\x00"):
            exif = True
            t = seg[6:]
            endian = "little" if t[:2] == b"II" else ("big" if t[:2] == b"MM" else None)
            if endian and len(t) >= 8:
                off = int.from_bytes(t[4:8], endian)
                if 0 < off and off + 2 <= len(t):
                    cnt = int.from_bytes(t[off:off + 2], endian)
                    for k in range(cnt):
                        e = off + 2 + 12 * k
                        if e + 12 > len(t):
                            break
                        if int.from_bytes(t[e:e + 2], endian) == 0x8825:   # GPSInfo IFD
                            gps = True
        i += 2 + ln
    return (w, h, exif, gps) if w else None


def png_info(data):
    """(largeur, hauteur, exif, gps) d'un PNG : dimensions dans IHDR, métadonnées dans eXIf."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w = h = None
    if data[12:16] == b"IHDR":
        w, h = struct.unpack(">II", data[16:24])
    exif = b"eXIf" in data[:4096]
    gps = False
    if exif:
        j = data.find(b"eXIf")
        chunk = data[j:j + 4096]
        if b"Exif\x00\x00" in chunk:
            t = chunk[chunk.find(b"Exif\x00\x00") + 6:]
            endian = "little" if t[:2] == b"II" else "big"
            if len(t) >= 8:
                off = int.from_bytes(t[4:8], endian)
                if 0 < off and off + 2 <= len(t):
                    cnt = int.from_bytes(t[off:off + 2], endian)
                    for k in range(cnt):
                        e = off + 2 + 12 * k
                        if e + 12 > len(t):
                            break
                        if int.from_bytes(t[e:e + 2], endian) == 0x8825:
                            gps = True
    return (w, h, exif, gps) if w else None


def image_info(path):
    """Lis un fichier : (largeur, hauteur, exif, gps, poids) ou None."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    if not data:
        return None
    return jpeg_info(data) or png_info(data)


# ─────────────────────────────── vérifications ───────────────────────────────

def check_file(path, label, findings, full=True):
    """Vérifie un fichier. `full=False` pour une variante -sm (budget plus serré)."""
    if not os.path.exists(path):
        findings.append(("ERR", label, "fichier introuvable (%s)" % path))
        return None
    size = os.path.getsize(path)
    info = image_info(path)
    if info is None:
        findings.append(("ERR", label, "ce n'est pas un JPEG ni un PNG lisible (%d o)" % size))
        return None
    facts = {"path": path, "w": info[0], "h": info[1], "exif": info[2], "gps": info[3],
             "size": size}
    w, h, exif, gps = facts["w"], facts["h"], facts["exif"], facts["gps"]
    budget = BUDGET_FULL if full else BUDGET_SM
    if size > budget:
        findings.append(("ERR", label, "%d Ko pour un budget de %d Ko — à réduire avant livraison"
                         % (size / 1024, budget / 1024)))
    if gps:
        findings.append(("ERR", label, "métadonnées GPS présentes — on ne publie pas l'endroit où la "
                                       "photo a été prise (nettoyer avant le déploiement)"))
    elif exif:
        findings.append(("WARN", label, "métadonnées EXIF présentes (appareil, horodatage) — à nettoyer"))
    return facts


def audit_page(page, findings, strict=False):
    try:
        html = open(page, encoding="utf-8").read()
    except OSError:
        findings.append(("ERR", page, "page illisible"))
        return 0
    folder = os.path.dirname(page)
    n = 0
    for tag in re.findall(r"<img\b[^>]*>", html, re.S):
        attrs = dict(re.findall(r'([\w:-]+)\s*=\s*"([^"]*)"', tag))
        src = attrs.get("src", "")
        if not src or src.startswith(("http", "data:")):
            continue
        n += 1
        label = "%s → %s" % (page, src)
        path = os.path.join(folder, src)
        info = check_file(path, label, findings, full=not src.endswith("-sm.jpg"))
        if not info:
            continue
        w, h = info["w"], info["h"]
        # ratio annoncé / ratio réel
        dw, dh = attrs.get("width"), attrs.get("height")
        if dw and dh and dw.isdigit() and dh.isdigit():
            dw, dh = int(dw), int(dh)
            if abs(dw / dh - w / h) / (w / h) > RATIO_TOL:
                findings.append(("ERR", label, "ratio annoncé %dx%d (%s) ≠ ratio réel %dx%d (%s) — "
                                               "le navigateur va recadrer la photo"
                                 % (dw, dh, round(dw / dh, 2), w, h, round(w / h, 2))))
            elif (dw, dh) != (w, h):
                findings.append(("WARN", label, "la page annonce %dx%d, le fichier fait %dx%d — même "
                                                "ratio, mais l'annonce est fausse" % (dw, dh, w, h)))
        # descripteurs srcset
        for cand in (attrs.get("srcset") or "").split(","):
            bits = cand.split()
            if len(bits) == 2 and bits[1].endswith("w") and bits[1][:-1].isdigit():
                declared = int(bits[1][:-1])
                cand_path = os.path.join(folder, bits[0])
                ci = image_info(cand_path)
                if ci and ci[0] != declared:
                    findings.append(("WARN", label, "srcset annonce %dw pour %s qui fait %dpx de large"
                                     % (declared, bits[0], ci[0])))
    return n


def audit_dir(folder, findings):
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        findings.append(("ERR", folder, "dossier illisible"))
        return 0
    n = 0
    for name in names:
        if not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        n += 1
        path = os.path.join(folder, name)
        info = check_file(path, name, findings, full=not name.endswith("-sm.jpg"))
        if info and name.endswith("-sm.jpg"):
            full = path[:-7] + ".jpg"
            if not os.path.exists(full):
                findings.append(("ERR", name, "variante -sm sans fichier plein — orpheline"))
            else:
                fi = image_info(full)
                if fi:
                    lourde = os.path.getsize(path) > os.path.getsize(full)
                    if info["w"] > fi[0] or lourde:
                        findings.append(("ERR", name, "variante -sm plus large (%d px contre %d px) ou plus "
                                                      "lourde (%d Ko contre %d Ko) que son original"
                                         % (info["w"], fi[0], os.path.getsize(path) / 1024,
                                            os.path.getsize(full) / 1024)))
    return n


def main(argv):
    strict = "--strict" in argv
    args = [a for a in argv if a != "--strict"]
    if not args:
        print(__doc__.strip().splitlines()[-4].strip())
        return 2
    findings, pages, dirs = [], [], []
    i = 0
    while i < len(args):
        if args[i] == "--dir":
            i += 1
            dirs.append(args[i])
        else:
            pages.append(args[i])
        i += 1
    n = 0
    for page in pages:
        n += audit_page(page, findings)
    for folder in dirs:
        n += audit_dir(folder, findings)

    # Un même fichier cité deux fois dans une page ne doit pas produire deux fois le même constat :
    # un rapport qui se répète se lit mal, et on finit par le survoler.
    seen, unique = set(), []
    for f in findings:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    findings = unique
    order = {"ERR": 0, "WARN": 1}
    findings.sort(key=lambda f: order.get(f[0], 2))
    for level, label, msg in findings:
        print("%-4s %s\n     %s" % (level, label, msg))
    errs = sum(1 for f in findings if f[0] == "ERR")
    warns = sum(1 for f in findings if f[0] == "WARN")
    if not findings:
        print("Aucune faute, aucun avertissement sur %d image(s)." % n)
    else:
        print("\n%d faute(s), %d avertissement(s) sur %d image(s) — "
              "le contrôle porte sur la structure et la vie privée, jamais sur la beauté de la photo."
              % (errs, warns, n))
    return 1 if (errs or (strict and warns)) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
