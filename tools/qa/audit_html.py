# -*- coding: utf-8 -*-
"""
audit_html.py — AMK pre-delivery audit for single-file concepts.

Two checks, both learned the hard way:
  1. STRUCTURE  tag balance + "is this section nested inside another section?"
     (a dropped </div> made every later section inherit a dark section's white
     text → white-on-white. Balance alone would NOT have caught it: the file
     was balanced, just wrongly nested.)
  2. CONTRAST   WCAG ratio for every text run, computed from the file's own CSS
     (cascade approximated: specificity + order + inline styles + var())
     against the nearest ancestor background, alpha-composited.

Usage:
    python3 tools/qa/audit_html.py demos/concept-opticien-v1.html
    python3 tools/qa/audit_html.py --all          # every demos/concept-*.html + site/*.html

Exit code 1 when anything is flagged, so it can gate a build.
"""
import re, sys, pathlib, itertools
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'area', 'base',
        'col', 'embed', 'param', 'track', 'wbr'}


# ----------------------------------------------------------------- DOM
class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent = tag, attrs, parent
        self.children, self.text = [], []

    @property
    def cls(self):
        return (self.attrs.get('class') or '').split()

    def path(self):
        bits, n = [], self
        while n is not None and n.tag != 'html':
            b = n.tag
            if n.attrs.get('id'):
                b += '#' + n.attrs['id']
            elif n.cls:
                b += '.' + n.cls[0]
            bits.append(b)
            n = n.parent
        return ' > '.join(reversed(bits))


class Dom(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('html', {}, None)
        self.cur = self.root
        self.stack = []
        self.mismatch = []

    def handle_starttag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.stack.append(tag)
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        n = Node(tag, dict(attrs), self.cur)
        self.cur.children.append(n)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag not in self.stack:
            self.mismatch.append(('stray </%s>' % tag, self.cur.path()))
            return
        while self.stack and self.stack[-1] != tag:
            self.mismatch.append(('unclosed <%s>' % self.stack[-1], self.cur.path()))
            self.stack.pop()
            self.cur = self.cur.parent
        self.stack.pop()
        self.cur = self.cur.parent or self.root

    def handle_data(self, data):
        if data.strip() and self.cur.tag not in ('script', 'style'):
            self.cur.text.append(data)


# ----------------------------------------------------------------- CSS
def split_media(css):
    """returns [(media_query_or_'' , inner_css)] — top level + each @media block"""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    blocks, i, out = [], 0, []
    while True:
        m = re.search(r'@media([^{]*)\{', css[i:])
        if not m:
            out.append(('', css[i:]))
            break
        out.append(('', css[i:i + m.start()]))
        j = i + m.end()
        depth, k = 1, j
        while k < len(css) and depth:
            if css[k] == '{':
                depth += 1
            elif css[k] == '}':
                depth -= 1
            k += 1
        out.append(('@media' + m.group(1), css[j:k - 1]))
        i = k
    return out


def parse_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    vars_ = {}
    for m in re.finditer(r':root\s*\{([^}]*)\}', css):
        for d in m.group(1).split(';'):
            if ':' in d:
                k, v = d.split(':', 1)
                vars_[k.strip()] = v.strip()
    rules = []
    for media, chunk in split_media(css):
        for m in re.finditer(r'([^{}@]+)\{([^{}]*)\}', chunk):
            sels = [x.strip() for x in m.group(1).split(',') if x.strip()]
            decls = {}
            for d in m.group(2).split(';'):
                if ':' in d:
                    k, v = d.split(':', 1)
                    decls[k.strip()] = v.strip()
            if decls:
                for sel in sels:
                    # pseudo-elements / interactive states never style the static element
                    if '::' in sel or re.search(r':(hover|focus|active|visited|target|checked|disabled)\b', sel):
                        continue
                    rules.append((sel, decls, len(rules), media))
    return vars_, rules


def resolve(val, vars_):
    if not val:
        return val
    for _ in range(6):
        m = re.search(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)', val)
        if not m:
            break
        val = val.replace(m.group(0), vars_.get(m.group(1), (m.group(2) or '').strip()))
    return val.strip()


def spec(sel):
    return (sel.count('#'), len(re.findall(r'\.[\w-]+', sel)) + len(re.findall(r'\[', sel)),
            len(re.findall(r'(?:^|\s|>)([a-zA-Z][\w-]*)', sel)))


def matches(node, sel):
    """descendant-only matcher — enough for our single-file concepts"""
    parts = [p for p in re.split(r'\s+', sel.strip()) if p and p not in ('>', '+', '~')]
    if not parts:
        return False
    if not match_compound(node, parts[-1]):
        return False
    n = node.parent
    for part in reversed(parts[:-1]):
        while n is not None and not match_compound(n, part):
            n = n.parent
        if n is None:
            return False
        n = n.parent
    return True


def match_compound(node, part):
    if ':' in part and not part.startswith(':'):
        part = part.split(':')[0]
    if part.startswith('.'):
        return part[1:] in node.cls
    if part.startswith('#'):
        return node.attrs.get('id') == part[1:]
    m = re.match(r'([\w-]+)?((?:[.#][\w-]+)*)$', part)
    if not m:
        return False
    tag, rest = m.group(1), m.group(2) or ''
    if tag and node.tag != tag:
        return False
    for cls in re.findall(r'\.([\w-]+)', rest):
        if cls not in node.cls:
            return False
    for i in re.findall(r'#([\w-]+)', rest):
        if node.attrs.get('id') != i:
            return False
    return True


def norm_size(val, node, vars_, rules, cache):
    """clamp()/vw/% → a px value, choosing the smallest (strictest) candidate"""
    val = (val or '').strip()
    if val.startswith('clamp('):
        args = [a.strip() for a in val[6:-1].split(',')]
    else:
        args = [val]
    px = []
    for a in args:
        a = resolve(a, vars_)
        if a.endswith('rem'):
            px.append(float(a[:-3]) * 16)
        elif a.endswith('em') and not a.endswith('rem'):
            par = computed(node.parent, 'font-size', vars_, rules, cache) or '16px'
            par = float(re.sub(r'[^0-9.]', '', str(par)) or 16)
            px.append(float(a[:-2]) * par)
        elif a.endswith('px'):
            px.append(float(a[:-2]))
        elif a.endswith(('vw', 'vh', 'vmin', 'vmax', '%')):
            continue          # viewport-relative: not knowable here, skip the candidate
    return '%gpx' % (min(px) if px else 16)


def context_rules(rules, mode):
    """mode 'base' = no media rules; 'mobile' adds max-width rules; 'desktop' adds min-width"""
    if mode == 'base':
        return [r for r in rules if not r[3]]
    keep = []
    for r in rules:
        media = r[3]
        if not media:
            keep.append(r)
        elif 'max-width' in media and mode == 'mobile':
            keep.append(r)
        elif 'min-width' in media and mode == 'desktop':
            keep.append(r)
    return keep


def computed(node, prop, vars_, rules, cache):
    key = (id(node), prop + '|' + str(len(rules)))
    if key in cache:
        return cache[key]
    if node is None:
        return None
    best = None
    for sel, decls, order, *rest in rules:
        if prop in decls and matches(node, sel):
            s = spec(sel)
            if best is None or (s, order) >= (best[0], best[1]):
                best = (s, order, decls[prop])
    shorthand = None
    if prop in ('font-size', 'font-weight') and best is None:
        for sel, decls, order, *rest in rules:
            if 'font' in decls and matches(node, sel):
                shorthand = decls['font']
                break
    if shorthand is not None:
        val = None
        for t in shorthand.split():
            head = t.split('/')[0]
            if prop == 'font-size' and re.match(r'^[\d.]+(px|rem|em|%)$', head):
                val = head
            elif prop == 'font-weight' and (head in ('bold', 'bolder', 'lighter') or
                                            re.match(r'^[1-9]00$', head)):
                val = head
        if val is None:
            val = computed(node.parent, prop, vars_, rules, cache)
        elif prop == 'font-size' and val.endswith(('rem', 'em')):
            val = norm_size(val, node, vars_, rules, cache)
        cache[key] = val
        return val
    if best is None and node.attrs.get('style'):
        for d in node.attrs['style'].split(';'):
            if ':' in d:
                k, v = d.split(':', 1)
                if k.strip() == prop:
                    best = ((9, 9, 9), 10 ** 6, v.strip())
    if best is not None:
        val = resolve(best[2], vars_)
        if prop == 'font-size':
            val = norm_size(val, node, vars_, rules, cache)
        if prop == 'font-size' and val.endswith('em') and not val.endswith('rem'):
            parent = computed(node.parent, 'font-size', vars_, rules, cache) or 16
            val = '%gpx' % (float(val[:-2]) * (parent / 16 if parent > 4 else 1))
        cache[key] = val
        return val
    if prop in ('color', 'font-size', 'font-weight'):
        val = computed(node.parent, prop, vars_, rules, cache)
        cache[key] = val
        return val
    cache[key] = None
    return None


# ----------------------------------------------------------------- colour
def to_rgba(val, vars_):
    val = resolve(val or '', vars_).lower()
    m = re.match(r'#([0-9a-f]{3,8})$', val)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        if len(h) == 6:
            h += 'ff'
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
    m = re.match(r'rgba?\(([^)]+)\)', val)
    if m:
        p = [x.strip() for x in m.group(1).split(',')]
        try:
            r, g, b = (int(float(x)) for x in p[:3])
            a = int(float(p[3]) * 255) if len(p) > 3 else 255
            return (r, g, b, a)
        except ValueError:
            return None
    named = {'white': (255, 255, 255, 255), 'black': (0, 0, 0, 255),
             'transparent': (0, 0, 0, 0), 'inherit': None}
    return named.get(val)


def over(fg, bg):
    a = fg[3] / 255
    return tuple(round(fg[i] * a + bg[i] * (1 - a)) for i in range(3)) + (255,)


def effective_bg(node, vars_, rules, cache, page=(255, 255, 255, 255)):
    if node is None:
        return page
    for prop in ('background-color', 'background'):
        v = node.attrs.get('style', '') and re.search(r'(?:^|;)\s*%s\s*:\s*([^;]+)' % prop,
                                                      node.attrs['style'])
        v = v.group(1) if v else computed(node, prop, vars_, rules, cache)
        if not v or 'gradient' in v.lower() or 'url(' in v.lower():
            if v and ('gradient' in v.lower() or 'url(' in v.lower()):
                c = re.search(r'(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\))', v)
                if not c:
                    continue
                v = c.group(1)
            else:
                continue
        col = to_rgba(v, vars_)
        if col and col[3] > 0:
            parent = effective_bg(node.parent, vars_, rules, cache, page)
            return over(col, parent[:3])
    return effective_bg(node.parent, vars_, rules, cache, page) if node.parent else page


def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# ----------------------------------------------------------------- checks
def audit(path):
    html = path.read_text(encoding='utf-8')
    problems, info = [], []

    dom = Dom()
    dom.feed(html)
    if dom.mismatch:
        for what, where in dom.mismatch[:6]:
            problems.append(('STRUCTURE', what, where,
                             'tag balance: the browser will invent closers'))

    def walk(n, out):
        for c in n.children:
            out.append(c)
            walk(c, out)
    nodes = []
    walk(dom.root, nodes)
    for n in nodes:
        if n.tag == 'section':
            a = n.parent
            while a is not None and a.tag != 'html':
                if a.tag == 'section':
                    problems.append(('STRUCTURE', 'section nested in section',
                                     '%s  (inside %s)' % (n.path(), a.path()),
                                     'later sections inherit the dark section styles'))
                    break
                a = a.parent
        if n.attrs.get('id'):
            chain = []
            a = n
            while a is not None and a.tag != 'html':
                chain.append(a.tag + ('.' + a.cls[0] if a.cls else ''))
                a = a.parent
            info.append('#%-10s %s' % (n.attrs['id'], ' > '.join(reversed(chain))))

    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
    vars_, all_rules = parse_css(css)
    cache = {}
    return problems, info, nodes, vars_, all_rules, css, page_colour(all_rules, vars_)


def page_colour(rules, vars_):
    base = context_rules(rules, 'base')
    for sel, decls, order, *rest in base:
        if sel == 'body' and ('background' in decls or 'background-color' in decls):
            return to_rgba(decls.get('background-color') or decls['background'], vars_) or (255, 255, 255, 255)
    return (255, 255, 255, 255)


def winning_selector(node, prop, rules):
    best = None
    for sel, decls, order, *rest in rules:
        if prop in decls and matches(node, sel):
            sp = spec(sel)
            if best is None or (sp, order) >= (best[0], best[1]):
                best = (sp, order, sel, decls[prop])
    return ('%s { %s: %s }' % (best[2], prop, best[3])) if best else (
        'inline style' if node.attrs.get('style') else 'inherited from ancestor')


def contrast_pass(nodes, vars_, rules, page, mode):
    cache, findings, checked = {}, [], 0
    for n in nodes:
        if n.tag in ('script', 'style', 'title', 'option') or in_svg(n):
            continue
        txt = ''.join(n.text).strip()
        if not txt or not re.search(r'[0-9A-Za-z\u00C0-\u024F]', txt):
            continue          # emoji / symbols only: coloured glyphs, not type
        fg = to_rgba(computed(n, 'color', vars_, rules, cache) or 'inherit', vars_)
        if fg is None or fg[3] == 0:
            continue
        bg = effective_bg(n, vars_, rules, cache, page[:3])
        composited = over(fg, bg)
        size = computed(n, 'font-size', vars_, rules, cache) or '16px'
        try:
            px = float(re.sub(r'[^0-9.]', '', size) or 16)
        except ValueError:
            px = 16
        weight = computed(n, 'font-weight', vars_, rules, cache) or '400'
        bold = weight in ('bold', 'bolder') or (weight.isdigit() and int(weight) >= 600)
        need = 3.0 if (px >= 24 or (px >= 18.66 and bold)) else 4.5
        r = ratio(composited, bg)
        checked += 1
        if r < need:
            findings.append(('%.2f:1 (need %.1f)' % (r, need),
                             '%s  « %s »' % (n.path(), txt[:60]),
                             'text #%02X%02X%02X on #%02X%02X%02X · %gpx%s · %s' % (
                                 composited[0], composited[1], composited[2],
                                 bg[0], bg[1], bg[2], px, ' bold' if bold else '',
                                 winning_selector(n, 'color', rules))))
    return findings, checked


def in_svg(n):
    a = n
    while a is not None:
        if a.tag == 'svg':
            return True
        a = a.parent
    return False


def walk(n, out):
    for c in n.children:
        out.append(c)
        walk(c, out)


def audit(path):
    html = path.read_text(encoding='utf-8')
    problems, info = [], []
    dom = Dom()
    dom.feed(html)
    for what, where in dom.mismatch[:6]:
        problems.append(('STRUCTURE', what, where, 'tag balance: the browser will invent closers'))
    nodes = []
    walk(dom.root, nodes)
    for n in nodes:
        if n.tag == 'section':
            a = n.parent
            while a is not None and a.tag != 'html':
                if a.tag == 'section':
                    problems.append(('STRUCTURE', 'section nested in section',
                                     '%s  (inside %s)' % (n.path(), a.path()),
                                     'later sections inherit the dark section styles'))
                    break
                a = a.parent
        if n.attrs.get('id'):
            chain, a = [], n
            while a is not None and a.tag != 'html':
                chain.append(a.tag + ('.' + a.cls[0] if a.cls else ''))
                a = a.parent
            info.append('#%-10s %s' % (n.attrs['id'], ' > '.join(reversed(chain))))

    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
    vars_, all_rules = parse_css(css)
    page = page_colour(all_rules, vars_)
    passes = {}
    for mode in ('desktop', 'mobile'):
        passes[mode] = contrast_pass(nodes, vars_, context_rules(all_rules, mode), page, mode)
    return problems, info, passes


def main():
    args = sys.argv[1:]
    if not args or args[0] == '--all':
        files = sorted(pathlib.Path(ROOT / 'demos').glob('concept-*.html')) + \
                sorted(pathlib.Path(ROOT / 'demos').glob('sjc-*.html')) + \
                sorted(pathlib.Path(ROOT / 'site').glob('*.html'))
    else:
        files = [pathlib.Path(a) if pathlib.Path(a).is_absolute() else ROOT / a for a in args]

    total = 0
    for f in files:
        if not f.exists():
            continue
        problems, info, passes = audit(f)
        desk, n1 = passes['desktop']
        mob, n2 = passes['mobile']
        keys = {k[1]: k for k in desk} | {k[1]: k for k in mob}
        both = set(x[1] for x in desk) & set(x[1] for x in mob)
        findings = [('both' if k in both else 'mobile-only',) + keys[k] for k in keys]
        findings.sort(key=lambda x: float(x[1].split(':')[0]))
        flag = 'FAIL' if problems or both else ('warn' if findings else 'ok  ')
        print('\n%s %s — %d text runs (desktop %d / mobile %d), %d findings '
              '(%d confirmed in both contexts)' % (flag, f.relative_to(ROOT), n1, n1, n2,
                                                   len(problems) + len(findings), len(both)))
        for kind, what, where, why in problems:
            print('   [%s] %s\n      %s\n      %s' % (kind, what, where, why))
        for ctx, what, where, why in findings[:14]:
            print('   [%s] %s\n      %s\n      %s' % (ctx, what, where, why))
        if len(findings) > 14:
            print('   … %d more' % (len(findings) - 14))
        total += len(problems) + len(both)
    print('\nTOTAL confirmed findings: %d' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
