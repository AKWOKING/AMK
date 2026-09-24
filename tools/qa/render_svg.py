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
import math
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
TOKEN = re.compile(r"([MmLlHhVvCcSsQqAaZz])|(-?\d*\.?\d+(?:e-?\d+)?)")


def flatten(d, steps=18):
    """Rend une liste de polylignes (listes de points) — les courbes échantillonnées."""
    toks = [(m.group(1) or float(m.group(2))) for m in TOKEN.finditer(d or "")]
    out, cur, start, i = [], (0.0, 0.0), (0.0, 0.0), 0
    cmd, last_ctrl = None, None

    def num():
        nonlocal i
        v = toks[i]
        i += 1
        return v

    def is_cmd():
        return isinstance(toks[i], str) if i < len(toks) else False

    while i < len(toks):
        if i >= len(toks):
            break
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
        elif c == "A":
            rx, ry, rot = num(), num(), num()
            laf, sf = num(), num()
            x, y = num(), num()
            end = (cur[0] + x, cur[1] + y) if rel else (x, y)
            pts = [cur] + arc_points(cur, rx, ry, rot, laf, sf, end)
            out.append(pts)
            cur = end
        elif c in ("C", "Q", "S"):
            if c == "S":
                # courbe lisse : le premier point de contrôle est le MIROIR du précédent — c'est ce que
                # dessinent les épaules et les visages de La Ligne Optic.
                x2, y2 = num(), num()
                p2 = (cur[0] + x2, cur[1] + y2) if rel else (x2, y2)
                p1 = (2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur
                x, y = num(), num()
                p3 = (cur[0] + x, cur[1] + y) if rel else (x, y)
                pts = [cur] + [bezier(cur, p1, p2, p3, t / steps) for t in range(1, steps + 1)]
                last_ctrl = p2
            elif c == "C":
                p1, p2 = (num(), num()), (num(), num())
                if rel:
                    p1 = (cur[0] + p1[0], cur[1] + p1[1])
                    p2 = (cur[0] + p2[0], cur[1] + p2[1])
                x, y = num(), num()
                p3 = (cur[0] + x, cur[1] + y) if rel else (x, y)
                pts = [cur] + [bezier(cur, p1, p2, p3, t / steps) for t in range(1, steps + 1)]
                last_ctrl = p2
            else:
                p1 = (num(), num())
                if rel:
                    p1 = (cur[0] + p1[0], cur[1] + p1[1])
                x, y = num(), num()
                p3 = (cur[0] + x, cur[1] + y) if rel else (x, y)
                pts = [cur] + [qbezier(cur, p1, p3, t / steps) for t in range(1, steps + 1)]
                last_ctrl = p1
            out.append(pts)
            cur = pts[-1]
        else:
            last_ctrl = None
            i += 1
    return [p for p in out if len(p) > 1]


def arc_points(p0, rx, ry, phi_deg, laf, sf, p1, steps=20):
    """Un arc SVG (`A`) échantillonné — les verres de monture arrondis de La Ligne Optic en ont besoin :
    sans lui le lexeur tombait sur « index out of range » et la planche de contrôle ne sortait pas."""
    if rx == 0 or ry == 0:
        return [p1]
    phi = math.radians(phi_deg)
    dx2, dy2 = (p0[0] - p1[0]) / 2.0, (p0[1] - p1[1]) / 2.0
    x1p = math.cos(phi) * dx2 + math.sin(phi) * dy2
    y1p = -math.sin(phi) * dx2 + math.cos(phi) * dy2
    rx, ry = abs(rx), abs(ry)
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        k = math.sqrt(lam)
        rx, ry = rx * k, ry * k
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    num_ = max(0.0, (rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2) / den) if den else 0.0
    co = (-1 if laf == sf else 1) * math.sqrt(num_)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx = math.cos(phi) * cxp - math.sin(phi) * cyp + (p0[0] + p1[0]) / 2
    cy = math.sin(phi) * cxp + math.cos(phi) * cyp + (p0[1] + p1[1]) / 2

    def angle(ux, uy, vx, vy):
        n = math.hypot(ux, uy) * math.hypot(vx, vy)
        a = math.acos(max(-1.0, min(1.0, (ux * vx + uy * vy) / n))) if n else 0.0
        return -a if ux * vy - uy * vx < 0 else a

    th1 = angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dth = angle((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sf and dth > 0:
        dth -= 2 * math.pi
    if sf and dth < 0:
        dth += 2 * math.pi
    return [(cx + rx * math.cos(th1 + dth * i / steps) * math.cos(phi)
             - ry * math.sin(th1 + dth * i / steps) * math.sin(phi),
             cy + rx * math.cos(th1 + dth * i / steps) * math.sin(phi)
             + ry * math.sin(th1 + dth * i / steps) * math.cos(phi)) for i in range(1, steps + 1)]


def bezier(p0, p1, p2, p3, t):
    u = 1 - t
    return (u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
            u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1])


def qbezier(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def col(v, default=None):
    """`#abc`, `#aabbcc` et `rgba(r,g,b,a)` — les ombres et les verres teintés s'écrivent en rgba, et
    sans eux la planche de contrôle ne montrerait ni les ombres ni les verres."""
    if not v or v in ("none", "transparent"):
        return None
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)", v)
    if m:
        rgb = tuple(int(float(m.group(i))) for i in (1, 2, 3))
        return rgb + (float(m.group(4)) if m.group(4) else 1.0,)
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


def keep_one_head(svg, keep):
    """Ne garder qu'un seul `<g class="head h-…">` — pour REGARDER un état du dessin.

    Le filtre naïf par expression régulière a été essayé le 24/09 et il a menti : la recherche
    non-gourmande s'arrête au premier `</g>`, qui est celui d'un groupe ENFANT (`<g class="frame">`),
    et le dessin restant était tronqué — on croyait voir un visage sans monture alors que la page était
    juste. On compte donc les groupes, comme un analyseur le ferait.
    """
    start = 0
    while True:
        m = re.search(r'<g class="head (h-[a-z]+)"', svg[start:])
        if not m:
            break
        head_at = start + m.start()
        depth, i = 0, head_at
        while i < len(svg):
            o, c = svg.find("<g", i), svg.find("</g>", i)
            if c < 0:
                break
            if 0 <= o < c:
                depth += 1
                i = o + 2
            else:
                depth -= 1
                i = c + 4
                if depth == 0:
                    break
        block = svg[head_at:i]
        if m.group(1) != keep:
            svg = svg[:head_at] + svg[i:]
            start = head_at
        else:
            start = i
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
        def blend(color):
            """Un rgba est mélangé au papier, comme le ferait le navigateur."""
            if color is None or len(color) == 3:
                return color
            r, g, b, a = color
            return tuple(int(round(c * a + p * (1 - a))) for c, p in zip((r, g, b), (241, 239, 233)))

        stroke, fill = col(st.get("stroke")), blend(col(st.get("fill")))
        w = max(1, int(round(float(st.get("stroke-width", 1)) * scale)))
        if tag == "path":
            polys = flatten((re.search(r'd="([^"]*)"', attr) or [None, ""])[1])
            if fill is not None:            # une forme fermée remplie : une ombre, un verre teinté
                for poly in polys:
                    dr.polygon([(x * scale, y * scale) for x, y in poly], fill=fill)
            for poly in polys:
                pts = [(x * scale, y * scale) for x, y in poly]
                dr.line(pts, fill=stroke, width=w, joint="curve")
                for p in (pts[0], pts[-1]):
                    dr.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=stroke)
        elif tag == "rect":
            x, y, rw, rh = g("x"), g("y"), g("width"), g("height")
            rx = float((re.search(r'rx="([^"]*)"', attr) or [0, 0])[1]) * scale
            if rx:
                dr.rounded_rectangle([x, y, x + rw, y + rh], radius=rx, outline=stroke, width=w, fill=fill)
            else:
                dr.rectangle([x, y, x + rw, y + rh], outline=stroke, width=w, fill=fill)
        elif tag == "ellipse":
            cx, cy, rx, ry = g("cx"), g("cy"), g("rx"), g("ry")
            dr.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=stroke, width=w, fill=fill)
        elif tag == "circle":
            cx, cy = g("cx"), g("cy")
            r = float(re.search(r'r="([^"]*)"', attr).group(1)) * scale
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=stroke, width=w, fill=fill)
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
    ap.add_argument("--only", default="", help="ne garder qu'un groupe `head` (h-ovale, h-carre…) : "
                                               "montre UN état du dessin, pas les cinq calques superposés")
    opts = ap.parse_args()

    html = pathlib.Path(opts.html).read_text(encoding="utf-8")
    rules = css_rules(html)
    svgs = re.findall(r'<svg class="%s"[\s\S]*?</svg>' % re.escape(opts.cls), html)
    if not svgs:
        sys.exit("aucun <svg class=\"%s\"> dans %s" % (opts.cls, opts.html))
    if opts.only:
        svgs = [keep_one_head(sv, opts.only) for sv in svgs]
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
