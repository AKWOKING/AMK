#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_svg.py — rendre un dessin SVG d'une page AMK en PNG, pour pouvoir LE REGARDER.

Pourquoi ce fichier existe : il n'y a **pas de navigateur** dans le bac (voir `design/LESSONS.md`), et
ImageMagick n'a ni `rsvg-convert` ni cairo ; `cairosvg`, `svglib` et le backend `renderPM` de reportlab
échouent tous les trois pour la même raison (aucune bibliothèque de dessin système). Or depuis le 24/09
et la page de **La Ligne Optic**, une page AMK peut être **entièrement dessinée** : ne pas pouvoir
regarder ses propres dessins avant de les livrer serait une faute professionnelle. Ce script supprime la
dépendance : il rastérise **avec PIL**, qui est installé, et il ne connaît que ce que nos pages utilisent.

Ce qu'il fait : extrait un SVG d'un fichier HTML (par son `class` ou son `id`), lit les règles de style
des classes visées dans la feuille de style de la page, aplatit les courbes de Bézier, **surdimensionne
×3 puis réduit** (l'antialiasing de PIL est inexistant, la réduction en fait un), et écrit un PNG.

Ce qu'il ne fait PAS : le CSS d'héritage, les transformations, les dégradés, les polices. Si un jour un
dessin en a besoin, il faudra l'étendre — pas le contourner.

Usage :
  python3 tools/qa/render_svg.py demos/concept-laligne-v1.html --class draw -o /tmp/hero.png
  python3 tools/qa/render_svg.py <html> --class mini --all -o /tmp/minis/     # tous ceux de la page
"""
import argparse
import pathlib
import re
import sys

from PIL import Image, ImageDraw

SS = 3  # facteur de surdimensionnement


# ── le CSS minimal : on lit les règles `selecteur{...}` de la page et on garde ce qui dessine ────────
def css_rules(html):
    """Les règles qui DESSINENT : une entrée par classe, la dernière gagne (comme dans une feuille).

    Deux choses qu'on sait faire, et deux seulement — parce que nos dessins n'utilisent que ça :
    les sélecteurs descendants (`.draw .face` compte pour `.face`) et les variables de `:root`.
    Sans la seconde, tout sortait **blanc sur papier blanc** le 24/09 : `stroke:var(--ink)` ne se
    résout pas tout seul, et la planche de contrôle semblait vide alors que le dessin était juste. """
    css = "".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", html))
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)

    variables = {}
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if sel.strip() == ":root":
            for decl in body.split(";"):
                if ":" in decl:
                    k, v = decl.split(":", 1)
                    variables[k.strip()] = v.strip()

    def resolve(v):
        for _ in range(4):
            m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)", v.strip())
            if not m:
                break
            v = variables.get(m.group(1), m.group(2) or "")
        return v.strip()

    rules = {}
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        props = {}
        for decl in body.split(";"):
            if ":" in decl:
                k, v = decl.split(":", 1)
                props[k.strip()] = resolve(v)
        for s in sel.split(","):
            s = s.strip()
            if ":" in s and not s.startswith(":root"):
                continue
            tokens = [t for t in re.split(r"\s+", s) if t.startswith(".")]
            if not tokens:
                continue
            rules.setdefault(tokens[-1], {}).update(props)   # `.draw .face` → `.face`
    return rules


def style_for(node, rules):
    classes = (re.search(r'class="([^"]*)"', node) or [None, ""])[1].split()
    st = {}
    for c in classes:
        st.update(rules.get("." + c, {}))
    for attr in ("stroke", "fill", "stroke-width", "stroke-dasharray", "stroke-linecap", "stroke-linejoin"):
        m = re.search(r'%s="([^"]*)"' % attr, node)
        if m:
            st[attr] = m.group(1)
    if "style" in node:
        for decl in (re.search(r'style="([^"]*)"', node) or ["", ""])[1].split(";"):
            if ":" in decl:
                k, v = decl.split(":", 1)
                st[k.strip()] = v.strip()
    return st


# ── les chemins : on aplatit tout ce que nos pages utilisent (M L H V C Q Z, en absolu et relatif) ──
TOKEN = re.compile(r"([MmLlHhVvCcQqZz])|(-?\d*\.?\d+(?:e-?\d+)?)")


def flatten(d, steps=18):
    """Rend une liste de polylignes (listes de points) — les courbes échantillonnées."""
    toks = [(m.group(1) or float(m.group(2))) for m in TOKEN.finditer(d or "")]
    out, cur, start, i = [], (0.0, 0.0), (0.0, 0.0), 0
    cmd = None

    def num():
        nonlocal i
        v = toks[i]
        i += 1
        return v

    def is_cmd():
        return isinstance(toks[i], str) if i < len(toks) else False

    while i < len(toks):
        if is_cmd():
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                if cur != start:
                    out.append([cur, start])
                cur = start
                continue
        if cmd is None:
            break
        rel = cmd.islower()
        c = cmd.upper()
        if c == "M":
            x, y = num(), num()
            cur = (cur[0] + x, cur[1] + y) if rel else (x, y)
            start = cur
            out.append([cur])
        elif c == "L":
            x, y = num(), num()
            nxt = (cur[0] + x, cur[1] + y) if rel else (x, y)
            out.append([cur, nxt])
            cur = nxt
        elif c == "H":
            x = num()
            nxt = (cur[0] + x, cur[1]) if rel else (x, cur[1])
            out.append([cur, nxt])
            cur = nxt
        elif c == "V":
            y = num()
            nxt = (cur[0], cur[1] + y) if rel else (cur[0], y)
            out.append([cur, nxt])
            cur = nxt
        elif c in ("C", "Q"):
            if c == "C":
                p1, p2 = (num(), num()), (num(), num())
                if rel:
                    p1 = (cur[0] + p1[0], cur[1] + p1[1])
                    p2 = (cur[0] + p2[0], cur[1] + p2[1])
                x, y = num(), num()
                p3 = (cur[0] + x, cur[1] + y) if rel else (x, y)
                pts = [cur] + [bezier(cur, p1, p2, p3, t / steps) for t in range(1, steps + 1)]
            else:
                p1 = (num(), num())
                if rel:
                    p1 = (cur[0] + p1[0], cur[1] + p1[1])
                x, y = num(), num()
                p3 = (cur[0] + x, cur[1] + y) if rel else (x, y)
                pts = [cur] + [qbezier(cur, p1, p3, t / steps) for t in range(1, steps + 1)]
            out.append(pts)
            cur = pts[-1]
        else:
            i += 1
    return [p for p in out if len(p) > 1]


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
            u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1])


def qbezier(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def col(v, default=None):
    if not v or v in ("none", "transparent"):
        return None
    if v.startswith("#"):
        v = v[1:]
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))
    return default


# ── le dessin ───────────────────────────────────────────────────────────────────────────────────────
def flatten_groups(svg):
    """Un `<g class="stroke frame">` porte le style de ses enfants : on le leur donne.

    Sans ça, les montures de La Ligne Optic sortaient **incolores** — le trait vivait sur le groupe, et
    le rastériseur ne lit que l'élément. Deux passes suffisent pour nos dessins (groupe → groupe → forme).
    """
    for _ in range(2):
        def one(m):
            classes, inner = m.group(1), m.group(2)
            return re.sub(r"<([a-zA-Z]+)([^>]*?)(/?)>",
                          lambda t: ('<%s class="%s"%s%s>' % (t.group(1), classes,
                                     (" " + t.group(2)).rstrip() if "class=" not in t.group(2) else t.group(2),
                                     t.group(3)))
                          if "class=" not in t.group(2) else t.group(0), inner)
        svg = re.sub(r'<g class="([^"]*)"[^>]*>([\s\S]*?)</g>', one, svg)
    return svg


def draw_svg(svg, rules, scale=SS):
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).replace(",", " ").split()]
    W, H = int(vb[2] * scale), int(vb[3] * scale)
    img = Image.new("RGB", (W, H), (241, 239, 233))
    dr = ImageDraw.Draw(img)
    body = flatten_groups(re.sub(r"^<svg[^>]*>|</svg>\s*$", "", svg.strip()))

    for m in re.finditer(r"<(path|rect|ellipse|circle|line)\b([^>]*?)/?>", body):
        tag, node = m.group(1), m.group(0)
        st = style_for(node, rules)
        attr = m.group(2)
        g = lambda k: float((re.search(r'%s="([^"]*)"' % k, attr) or [0, 0])[1]) * scale
        stroke, fill = col(st.get("stroke")), col(st.get("fill"))
        w = max(1, int(round(float(st.get("stroke-width", 1)) * scale)))
        if tag == "path":
            for poly in flatten((re.search(r'd="([^"]*)"', attr) or [None, ""])[1]):
                pts = [(x * scale, y * scale) for x, y in poly]
                dr.line(pts, fill=stroke, width=w, joint="curve")
                for p in (pts[0], pts[-1]):
                    dr.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=stroke)
        elif tag == "rect":
            x, y, rw, rh = g("x"), g("y"), g("width"), g("height")
            rx = float((re.search(r'rx="([^"]*)"', attr) or [0, 0])[1]) * scale
            if rx:
                dr.rounded_rectangle([x, y, x + rw, y + rh], radius=rx, outline=stroke, width=w)
            else:
                dr.rectangle([x, y, x + rw, y + rh], outline=stroke, width=w)
        elif tag == "ellipse":
            cx, cy, rx, ry = g("cx"), g("cy"), g("rx"), g("ry")
            dr.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=stroke, width=w)
        elif tag == "circle":
            cx, cy = g("cx"), g("cy")
            r = float(re.search(r'r="([^"]*)"', attr).group(1)) * scale
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=stroke, width=w)
        elif tag == "line":
            dr.line([g("x1"), g("y1"), g("x2"), g("y2")], fill=stroke, width=w)
    return img.resize((W // scale, H // scale), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--class", dest="cls", required=True, help="la classe du <svg> à rendre")
    ap.add_argument("--all", action="store_true", help="tous ceux de cette classe")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--width", type=int, default=0)
    opts = ap.parse_args()

    html = pathlib.Path(opts.html).read_text(encoding="utf-8")
    rules = css_rules(html)
    svgs = re.findall(r'<svg class="%s"[\s\S]*?</svg>' % re.escape(opts.cls), html)
    if not svgs:
        sys.exit("aucun <svg class=\"%s\"> dans %s" % (opts.cls, opts.html))
    if not opts.all:
        svgs = svgs[:1]
    out = pathlib.Path(opts.out)
    for i, svg in enumerate(svgs):
        img = draw_svg(svg, rules)
        if opts.width and opts.width < img.width:
            img = img.resize((opts.width, int(img.height * opts.width / img.width)), Image.LANCZOS)
        if opts.all:
            out.mkdir(parents=True, exist_ok=True)
            img.save(out / ("%s-%d.png" % (opts.cls, i)))
        else:
            img.save(out)
        print("✓ %s (%dx%d)" % (out if not opts.all else out / ("%s-%d.png" % (opts.cls, i)), img.width, img.height))


if __name__ == "__main__":
    main()
