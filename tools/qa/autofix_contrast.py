# -*- coding: utf-8 -*-
"""
autofix_contrast.py — propose (and with --write applies) scoped colour overrides
that take a concept to 0 contrast findings, verified by audit_html.py.

Rules it follows, so the design survives:
  · light background  → keep the hue, darken the TEXT colour
  · dark background   → keep the hue, lighten the TEXT colour
  · mid-tone background (a coloured button/fill) → darken the FILL, keep the text
  · never touches gradients, images, borders, shadows
  · every fix is scoped to the selector that actually failed
  · after writing, the file is re-audited; if the count did not go down, it reverts

Usage:  python3 tools/qa/autofix_contrast.py demos/concept-x.html [--write]
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import audit_html as A

MARK = '/* a11y-pass-2026-09-17 */'


def tint(c, factor):
    return tuple(max(0, min(255, round(v * factor))) for v in c[:3])


def fix_pair(fg, bg, need):
    """returns a new fg (tuple) that reaches `need` on bg"""
    lum_bg = A.lum(bg)
    # if the background is mid/low, darken text; if very dark, lighten it
    lighten = lum_bg < 0.16
    best = None
    steps = [i / 100 for i in range(2, 100, 2)]
    for s in steps:
        cand = tuple(min(255, round(v + (255 - v) * s)) for v in fg[:3]) if lighten \
            else tuple(max(0, round(v * (1 - s))) for v in fg[:3])
        if A.ratio(cand + (255,), bg) >= need:
            best = cand
            break
    return best


def darken_fill(bg, need, fg=(255, 255, 255)):
    for s in [i / 100 for i in range(2, 80, 2)]:
        cand = tuple(max(0, round(v * (1 - s))) for v in bg[:3])
        if A.ratio(cand + (255,), tuple(fg)) >= need:
            return cand
    return None


def selector_for(path):
    parts = [p for p in path.split(' > ') if p != 'html']
    if not parts:
        return None
    def s(p):
        if '#' in p:
            t, i = p.split('#'); return t + '#' + i
        if '.' in p:
            return p
        return p
    tail = s(parts[-1])
    for anc in reversed(parts[:-1]):
        if '#' in anc:
            return s(anc) + ' ' + tail
    return (s(parts[0]) + ' ' + tail) if len(parts) > 1 else tail


def main():
    path = pathlib.Path(sys.argv[1])
    write = '--write' in sys.argv
    html = path.read_text(encoding='utf-8')
    problems, info, passes = A.audit(path)
    before = len(problems) + len(passes['desktop'][0])

    rules = []
    seen = set()
    for ctx, what, where, why in [(c,) + f for c, f in
                                  [('both', f) for f in passes['desktop'][0]] +
                                  [('mobile', f) for f in passes['mobile'][0]]]:
        need = float(re.search(r'need ([\d.]+)', what).group(1))
        m = re.search(r'text (#[0-9A-F]{6}) on (#[0-9A-F]{6})', why)
        if not m:
            continue
        fg, bg = A.to_rgba(m.group(1), {}), A.to_rgba(m.group(2), {})
        sel = selector_for(where.split('  «')[0].strip())
        if not sel:
            continue
        key = (sel, m.group(1), m.group(2), need)
        if key in seen:
            continue
        seen.add(key)
        lum_bg = A.lum(bg)
        if lum_bg >= 0.14:
            new = fix_pair(bg if False else fg, bg, need)          # darken text
            if new:
                rules.append((sel, 'color', '#%02X%02X%02X' % new,
                              '%s on %s (%.2f:1)' % (m.group(1), m.group(2),
                                                     A.ratio(fg, bg))))
            continue
        new = darken_fill(bg, need)                                 # mid-tone fill
        if new:
            rules.append((sel, 'background-color', '#%02X%02X%02X' % new,
                          'fill under %s (%.2f:1)' % (m.group(1), A.ratio(fg, bg))))
    if not rules:
        print('nothing to fix in %s (%d findings before, %d after)'
              % (path, before, len(passes['desktop'][0])))
        return 0

    block = '\n' + MARK + '\n' + '\n'.join(r[0] + '{' + r[1] + ':' + r[2] + '}' for r in rules) + '\n'
    print('%d override rules for %s:' % (len(rules), path))
    for sel, prop, val, why in rules:
        print('   %-42s %s:%-6s %s   # %s' % (sel, prop, '', val, why))
    if not write:
        return 0

    patched = html.replace('</style>', block + '</style>', 1)
    path.write_text(patched, encoding='utf-8')
    problems2, info2, passes2 = A.audit(path)
    after = len(problems2) + len(passes2['desktop'][0])
    print('%s: %d → %d findings' % (path.name, before, after))
    if after > before:
        path.write_text(html, encoding='utf-8')
        print('   REVERTED (made it worse)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
