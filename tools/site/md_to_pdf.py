#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Markdown → PDF, pour les documents qu'on pose sur la table du client (25/09/2026).

Pourquoi ce script existe : le business case d'Univers Optique doit partir **sur WhatsApp, dans
l'heure qui suit la réunion**, et un `.md` ne s'ouvre pas sur un téléphone. Il fallait un PDF —
et le bac n'a ni pandoc, ni LibreOffice, ni reportlab : **PIL est le seul moteur** (même situation
que pour les planches de contrôle et la vignette des liens). Trente secondes de rendu valent mieux
qu'un fichier que le client ne peut pas ouvrir.

Ce n'est PAS un moteur Markdown complet : il lit exactement ce qu'écrivent nos documents client —
titres (`#`, `##`, `###`), paragraphes, gras `**…**`, italique `*…*`, code `` `…` ``, citations `>`,
filets `---`, listes `- `, et les **tableaux à deux colonnes** (la forme qu'ont tous nos chiffres).

Usage :
  python3 tools/site/md_to_pdf.py sales/BUSINESS-CASE-UNIVERS-OPTIQUE-2026-09-25.md \
      -o sales/BUSINESS-CASE-UNIVERS-OPTIQUE-2026-09-25.pdf \
      --titre "UNIVERS OPTIQUE — business case" --pied "AMK · Akwo King · Douala" --png /tmp/bc
"""
import argparse
import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

# A4 à 160 ppp : 1323 × 1871 px. Le texte fait ~24 px de haut, soit l'équivalent de 11 pt —
# net à l'écran comme à l'impression, et lisible d'un pouce sur un téléphone.
W, H, DPI = 1323, 1871, 160
M = 104                     # marge
COLW = 0.62                 # part de la première colonne des tableaux

# La palette de la page d'Univers Optique, reprise telle quelle : le document et la page se
# ressemblent, donc le client reconnaît la même maison.
PAPER = (251, 246, 236)
INK = (30, 26, 21)
TEXT = (61, 54, 44)
MUTE = (110, 100, 85)
HAIR = (216, 202, 177)
RUST = (169, 76, 35)
PETROL = (18, 48, 63)

FONTS = "/usr/share/fonts/truetype/dejavu/"
NO_SPACE_BEFORE = ".,;:!?»%…"
F_BODY, F_BOLD, F_MONO = "DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSansMono.ttf"
_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS + name, size)
    return _cache[key]


def join_lines(parts):
    """Recolle les lignes d'un paragraphe : un `.md` source est coupé à la main, pas au sens.
    Une ponctuation qui commence une ligne ne prend jamais d'espace devant elle."""
    out = ""
    for part in parts:
        if out and part[:1] not in NO_SPACE_BEFORE:
            out += " "
        out += part
    return out


def spans(text):
    """`**gras**`, `` `code` ``, `*italique*` → une suite de (texte, style)."""
    out, i = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*|`(.+?)`|(?<!\*)\*([^*]+?)\*(?!\*)", text):
        if m.start() > i:
            out.append((text[i:m.start()], ""))
        out.append((m.group(1), "b") if m.group(1) is not None else
                   (m.group(2), "c") if m.group(2) is not None else (m.group(3), "i"))
        i = m.end()
    if i < len(text):
        out.append((text[i:], ""))
    return out or [(text, "")]


def wrap(text, size, width):
    """Découpe une suite de (texte, style) en lignes qui tiennent dans `width`."""
    f, fb, fm = font(F_BODY, size), font(F_BOLD, size), font(F_MONO, size - 3)
    space = f.getlength(" ")
    words = []
    for chunk, style in spans(text):
        for k, w in enumerate(chunk.split(" ")):
            if w != "" or k == 0:
                fnt = fb if style == "b" else fm if style == "c" else f
                words.append((w, fnt, style))
    # Une ponctuation seule est COLLÉE au mot qui la précède — sinon, quand le mot finit pile au
    # bord, le point part seul à la ligne suivante (vu sur la page 3 du business case).
    glued = []
    for w, fnt, style in words:
        if glued and w[:1] in NO_SPACE_BEFORE:
            pw, pfnt, pstyle = glued[-1]
            glued[-1] = (pw + w, pfnt, pstyle)
        else:
            glued.append((w, fnt, style))
    words = glued

    lines, cur, curw = [], [], 0.0
    for w, fnt, style in words:
        wd = fnt.getlength(w)
        gap = 0 if (cur and w[:1] in NO_SPACE_BEFORE) else space
        if cur and curw + gap + wd > width:
            lines.append(cur)
            cur, curw = [(w, fnt, style)], wd
        else:
            curw += (gap if cur else 0) + wd
            cur.append((w, fnt, style))
    if cur:
        lines.append(cur)
    return lines


class Doc:
    """Le document : des pages A4, un curseur, et des blocs qui savent se couper."""

    def __init__(self, title, foot):
        self.title, self.foot = title, foot
        self.pages = []
        self.new_page()

    # ── pages ─────────────────────────────────────────────────────────────────────────────────
    def new_page(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.pages.append(self.img)
        self.y = M
        if self.title:
            self.d.text((M, 46), self.title, font=font(F_BOLD, 19), fill=MUTE)
            self.d.line([(M, 78), (W - M, 78)], fill=HAIR, width=2)

    def ensure(self, h):
        if self.y + h > H - 96:
            self.new_page()

    # ── texte ─────────────────────────────────────────────────────────────────────────────────
    def write(self, lines, size, lead, indent=0, fill=TEXT):
        f = font(F_BODY, size)
        space = f.getlength(" ")
        for line in lines:
            self.ensure(lead)
            x = M + indent
            for i, (w, fnt, style) in enumerate(line):
                col = PETROL if style == "c" else MUTE if style == "i" else fill
                self.d.text((x, self.y), w, font=fnt, fill=col)
                x += fnt.getlength(w)
                if i + 1 < len(line) and line[i + 1][0][:1] not in NO_SPACE_BEFORE:
                    x += space
            self.y += lead

    def para(self, text, size=24, lead=34, gap=16, indent=0, fill=TEXT):
        if text != "":
            self.write(wrap(text, size, W - 2 * M - indent), size, lead, indent, fill)
        self.y += gap

    def rule(self, color=HAIR, weight=2, gap=24):
        self.ensure(gap + 4)
        self.d.line([(M, self.y + gap // 2), (W - M, self.y + gap // 2)], fill=color, width=weight)
        self.y += gap


# ─────────────────────────────── les blocs ───────────────────────────────

def h1(d, t):
    d.ensure(70)
    d.write(wrap(t, 40, W - 2 * M), 40, 50)
    d.y += 6


def h2(d, t):
    d.ensure(96)
    d.y += 12
    d.d.line([(M, d.y), (W - M, d.y)], fill=RUST, width=3)
    d.y += 18
    d.write(wrap(t, 30, W - 2 * M), 30, 42)
    d.y += 14


def h3(d, t):
    d.ensure(46)
    d.write(wrap(t, 24, W - 2 * M), 24, 32)
    d.y += 10


def quote(d, block):
    d.ensure(60)
    top = d.y
    for i, ln in enumerate(block):
        d.write(wrap(ln, 25 if i == 0 else 20, W - 2 * M - 36),
                25 if i == 0 else 20, 35 if i == 0 else 28,
                indent=36, fill=INK if i == 0 else MUTE)
    d.d.line([(M + 10, top + 6), (M + 10, d.y - 24)], fill=RUST, width=4)
    d.y += 20


def bullets(d, items):
    for it in items:
        d.ensure(36)
        d.d.text((M + 4, d.y + 4), "•", font=font(F_BOLD, 22), fill=RUST)
        d.write(wrap(it, 24, W - 2 * M - 36), 34, indent=36)
        d.y += 8


def table(d, rows):
    """Tableau à deux colonnes : en-tête en gras, filets fins, cellules qui se replient."""
    head, body = rows[0], rows[1:]
    if not any(c.strip() for c in head):
        head, body = None, rows
    c1 = int((W - 2 * M) * COLW)
    if head:
        d.ensure(52)
        if head[0].strip():
            d.write(wrap(head[0], 19, c1 - 20), 19, 26, fill=MUTE)
        if len(head) > 1 and head[1].strip():
            y0 = d.y - 26
            d.y = y0
            d.write(wrap(head[1], 19, W - 2 * M - c1 - 20), 19, 26, indent=c1 + 20, fill=MUTE)
        d.d.line([(M, d.y + 2), (W - M, d.y + 2)], fill=HAIR, width=2)
        d.y += 18
    for row in body:
        left, right = (row + ["", ""])[:2]
        lw = wrap(left, 22, c1 - 24) if left.strip() else []
        rw = wrap(right, 19, W - 2 * M - c1 - 20) if right.strip() else []
        hgt = max(len(lw) * 31, len(rw) * 27) + 20
        d.ensure(hgt)
        top = d.y
        if lw:
            d.write(lw, 22, 31)
        yleft = d.y
        if rw:
            d.y = top
            d.write(rw, 19, 27, indent=c1 + 20, fill=MUTE)
        d.y = max(yleft, d.y if rw else top)
        d.d.line([(M, d.y + 2), (W - M, d.y + 2)], fill=HAIR, width=2)
        d.y += 14


# ─────────────────────────────── le document ───────────────────────────────

BLOCK_START = ("#", ">", "|", "- ", "---")


def _is_text(s):
    """Une ligne de continuation de paragraphe : non vide et pas un début de bloc."""
    return bool(s) and not s.startswith(BLOCK_START)


def build(md, title, foot):
    d = Doc(title, foot)
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s == "---":
            d.rule()
        elif s.startswith("### "):
            h3(d, s[4:])
        elif s.startswith("## "):
            h2(d, s[3:])
        elif s.startswith("# "):
            h1(d, s[2:])
        elif s.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            block = [b for b in block if b]
            # Une citation de plusieurs lignes est UN paragraphe : on recolle les retours du
            # fichier source (un `.md` écrit à la main est coupé tous les 90 caractères). Seule
            # l'attribution, qui commence par un tiret cadratin, reste sur sa propre ligne.
            quote(d, [join_lines([b for b in block if not b.startswith("—")])] +
                    [b for b in block if b.startswith("—")])
            continue
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") and c for c in cells):
                    rows.append(cells)
                i += 1
            table(d, rows)
            continue
        elif s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item = [lines[i].strip()[2:]]
                i += 1
                while i < len(lines) and _is_text(lines[i].strip()):
                    item.append(lines[i].strip())
                    i += 1
                items.append(join_lines(item))
            bullets(d, items)
            continue
        else:
            para = [s]
            i += 1
            while i < len(lines) and _is_text(lines[i].strip()):
                para.append(lines[i].strip())
                i += 1
            d.para(join_lines(para), gap=18)
            continue
        i += 1
    # Les pieds de page s'écrivent à la fin : c'est là qu'on connaît le nombre total de pages.
    for n, img in enumerate(d.pages, 1):
        dr = ImageDraw.Draw(img)
        if foot:
            dr.text((M, H - 62), foot, font=font(F_BODY, 18), fill=MUTE)
        num = "%d / %d" % (n, len(d.pages))
        dr.text((W - M - dr.textlength(num, font=font(F_BODY, 18)), H - 62), num,
                font=font(F_BODY, 18), fill=MUTE)
    return d.pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("-o", "--out")
    ap.add_argument("--titre", default="")
    ap.add_argument("--pied", default="")
    ap.add_argument("--png", help="dossier où poser aussi les pages en PNG (contrôle à l'œil)")
    o = ap.parse_args()

    src = pathlib.Path(o.source)
    out = pathlib.Path(o.out) if o.out else src.with_suffix(".pdf")
    pages = build(src.read_text(encoding="utf-8"), o.titre, o.pied)
    pages[0].save(out, "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
    print("✓ %s — %d page(s), %.0f Ko" % (out, len(pages), out.stat().st_size / 1024))
    if o.png:
        d = pathlib.Path(o.png)
        d.mkdir(parents=True, exist_ok=True)
        for k, im in enumerate(pages, 1):
            im.save(d / ("page-%d.png" % k))
        print("✓ %d page(s) en PNG dans %s — à regarder avant d'envoyer" % (len(pages), d))


if __name__ == "__main__":
    main()
