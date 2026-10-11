#!/usr/bin/env python3
"""Rend les carrousels Instagram de @amkweb.cm (1080x1350) depuis content/carousels/carousels.json.

Source unique du texte = le JSON. Sorties : content/carousels/<id>/slide-N.png + content/carousels/POST-READY.md.
Contrôles bloquants : glyphes présents dans la police, texte dans le cadre (taille minimale), contraste >= 4,5,
7 slides maximum, un seul appel à l'action par dernière slide.
Palette = empreinte de marque (CONTENT-LESSONS §1) : marine / turquoise / ambre, Montserrat.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CAR = os.path.join(ROOT, 'content', 'carousels')
FONTS = os.path.join(ROOT, 'content', 'assets', 'fonts')
HOST = os.path.join(ROOT, 'content', 'assets', 'host', 's1_hook.png')

W, H, M = 1080, 1350, 84
BG = (28, 34, 92)          # = fond de l'illustration de l'hôte (pas de couture)
WHITE = (255, 255, 255)
SOFT = (214, 218, 240)     # texte secondaire
TEAL = (35, 196, 177)
AMBER = (255, 176, 32)
NAVY_INK = (20, 24, 64)

XB, BD, SB, MD = 'Montserrat-ExtraBold.ttf', 'Montserrat-Bold.ttf', 'Montserrat-SemiBold.ttf', 'Montserrat-Medium.ttf'
WEIGHT = {XB: 800, BD: 700, SB: 600, MD: 500}

def F(name, size):
    """Les 'static' sont des variables dont l'axe par défaut est Thin (CONTENT-LESSONS §6) : fixer le poids."""
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    f.set_variation_by_axes([WEIGHT[name]])
    return f

def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

PAIRS = {'blanc/fond': (WHITE, BG), 'secondaire/fond': (SOFT, BG), 'ambre/fond': (AMBER, BG),
         'turquoise/fond': (TEAL, BG), 'encre/ambre (bouton)': (NAVY_INK, AMBER), 'encre/turquoise': (NAVY_INK, TEAL)}
for k, (a, b) in PAIRS.items():
    assert contrast(a, b) >= 4.5, f'contraste insuffisant {k}: {contrast(a, b):.2f}'

_probe = {}
def has_glyph(fontname, ch):
    key = fontname
    if key not in _probe:
        f = F(fontname, 60)
        _probe[key] = (f, f.getmask('\ue000').getbbox(), f.getmask('\ue000'))
    f, _, miss = _probe[key]
    if ch.isspace():
        return True
    m = f.getmask(ch)
    return bytes(m) != bytes(miss) or m.size != miss.size

def check_glyphs(text, fontname, where):
    for ch in set(re.sub(r'[*\n]', '', text)):
        if not has_glyph(fontname, ch):
            raise SystemExit(f'glyphe absent {ch!r} ({hex(ord(ch))}) dans {fontname} — {where}')

NB = {' ?': '\u00a0?', ' :': '\u00a0:', ' !': '\u00a0!', ' »': '\u00a0»', '« ': '«\u00a0'}

def tokens(text):
    """'*mot*.' -> lignes ; chaque mot = liste de tronçons [(texte, surligné)] (la ponctuation collée reste collée).
    Espaces insécables français avant ? : ! » et après « (elles ne coupent pas la ligne)."""
    for k, v in NB.items():
        text = text.replace(k, v)
    out = []
    for para in text.split('\n'):
        words, cur, hl = [], [], False
        buf = ''
        def flush():
            nonlocal buf
            if buf:
                cur.append((buf.replace('\u00a0', ' '), hl)); buf = ''
        for ch in para:
            if ch == '*':
                flush(); hl = not hl
            elif ch == ' ':
                flush()
                if cur:
                    words.append(cur); cur = []
            else:
                buf += ch
        flush()
        if cur:
            words.append(cur)
        out.append(words)
    return out

def wlen(font, word):
    return sum(font.getlength(t) for t, _ in word)

def layout(text, fontname, size, maxw):
    font = F(fontname, size)
    sp = font.getlength(' ')
    lines = []
    for para in tokens(text):
        cur, curw = [], 0
        for w in para:
            wl = wlen(font, w)
            add = wl if not cur else sp + wl
            if cur and curw + add > maxw:
                lines.append(cur); cur, curw = [w], wl
            else:
                cur.append(w); curw += add
        if cur:
            lines.append(cur)
    return font, lines

def line_w(font, ln):
    return sum(wlen(font, w) for w in ln) + font.getlength(' ') * (len(ln) - 1)

def fit(text, fontname, start, minsize, maxw, maxh, lh=1.14):
    s = start
    while s >= minsize:
        font, lines = layout(text, fontname, s, maxw)
        widest = max(line_w(font, ln) for ln in lines)
        if len(lines) * s * lh <= maxh and widest <= maxw:
            # équilibrer : plus petite largeur qui garde le même nombre de lignes (pas de mot orphelin)
            n, best = len(lines), lines
            for mw in range(int(maxw) - 8, int(maxw * 0.45), -8):
                f2, l2 = layout(text, fontname, s, mw)
                if len(l2) != n or max(line_w(f2, ln) for ln in l2) > mw:
                    break
                best = l2
            return font, best, s, lh
        s -= 2
    raise SystemExit(f'texte trop long pour le cadre ({maxw}x{maxh}) : {text[:60]!r}')

def draw_lines(d, font, lines, x, y, size, lh, color, hl=AMBER, align='left', w=None):
    sp = font.getlength(' ')
    for ln in lines:
        cx = x if align == 'left' else x + (w - line_w(font, ln)) / 2
        for word in ln:
            for t, h in word:
                d.text((cx, y), t, font=font, fill=hl if h else color)
                cx += font.getlength(t)
            cx += sp
        y += size * lh
    return y

def block(d, text, fontname, start, minsize, x, y, maxw, maxh, color, align='left', lh=1.14, dry=False):
    check_glyphs(text, fontname, text[:40])
    font, lines, s, lh = fit(text, fontname, start, minsize, maxw, maxh, lh)
    if dry:
        return y + len(lines) * s * lh, s
    end = draw_lines(d, font, lines, x, y, s, lh, color, align=align, w=maxw)
    return end, s

def pill(d, x, y, text, fill=None, outline=None, ink=WHITE, size=28):
    check_glyphs(text, BD, text)
    f = F(BD, size)
    tw = f.getlength(text)
    h = size + 30
    box = (x, y, x + tw + 56, y + h)
    d.rounded_rectangle(box, radius=h // 2, fill=fill, outline=outline, width=3 if outline else 0)
    d.text((x + 28, y + 14), text, font=f, fill=ink)
    return box

def arrow(d, x, y, color, s=26):
    d.line((x, y, x + s * 1.6, y), fill=color, width=6)
    d.line((x + s * 1.6 - s * .6, y - s * .6, x + s * 1.6, y), fill=color, width=6)
    d.line((x + s * 1.6 - s * .6, y + s * .6, x + s * 1.6, y), fill=color, width=6)

def footer(d, handle, i, n):
    check_glyphs(handle, SB, 'handle')
    d.text((M, 1262), handle, font=F(SB, 32), fill=SOFT)
    r, gap = 9, 30
    x0 = W - M - (n - 1) * gap - 2 * r
    for k in range(n):
        cx = x0 + k * gap + r
        if k == i:
            d.ellipse((cx - r, 1286 - r, cx + r, 1286 + r), fill=AMBER)
        else:
            d.ellipse((cx - r, 1286 - r, cx + r, 1286 + r), outline=SOFT, width=3)

def top_row(d, s, i, n):
    if s.get('label'):
        pill(d, M, 76, s['label'], outline=TEAL, ink=TEAL)
    d.text((W - M - F(BD, 30).getlength(f'{i + 1}/{n}'), 90), f'{i + 1}/{n}', font=F(BD, 30), fill=SOFT)

def canvas():
    im = Image.new('RGB', (W, H), BG)
    return im, ImageDraw.Draw(im)

def host_cover(im):
    host = Image.open(HOST).convert('RGB').crop((0, 560, 768, 1376))     # épaules + téléphone
    sc = 0.68
    host = host.resize((int(host.width * sc), int(host.height * sc)), Image.LANCZOS)
    hw, hh = host.size
    mask = Image.new('L', host.size, 255)
    md = ImageDraw.Draw(mask)
    f = 110
    for k in range(f):
        v = int(255 * k / f)
        md.line((0, k, hw, k), fill=min(v, 255))                       # haut
        md.line((0, hh - 1 - k, hw, hh - 1 - k), fill=v)              # bas
        md.line((k, 0, k, hh), fill=v)                                 # gauche
    from PIL import ImageChops
    m2 = Image.new('L', host.size, 255); d2 = ImageDraw.Draw(m2)
    for k in range(f):
        d2.line((0, k, hw, k), fill=int(255 * k / f)); d2.line((0, hh - 1 - k, hw, hh - 1 - k), fill=int(255 * k / f)); d2.line((k, 0, k, hh), fill=int(255 * k / f))
    mask = m2
    im.paste(host, (W - hw + 30, 1262 - hh), mask)

def render_cover(s, i, n, handle):
    im, d = canvas(); host_cover(im); d = ImageDraw.Draw(im)
    pill(d, M, 84, s['tag'], fill=AMBER, ink=NAVY_INK)
    end, _ = block(d, s['title'], XB, 104, 70, M, 180, W - 2 * M, 380, WHITE)
    if s.get('title2'):
        end, _ = block(d, s['title2'], XB, 66, 52, M, end + 18, W - 2 * M, 190, WHITE)
    sy = min(end + 30, 720)
    check_glyphs(s['sub'], SB, 'sub')
    d.text((M, sy), s['sub'], font=F(SB, 40), fill=TEAL)
    arrow(d, M, sy + 90, AMBER)
    footer(d, handle, i, n)
    return im

def render_text(s, i, n, handle):
    im, d = canvas(); top_row(d, s, i, n)
    TX, BX = 104, 60
    # mesure à blanc pour centrer le bloc (un message par slide : il doit occuper l'écran)
    badge = 170 if s.get('num') else 0
    e1, _ = block(d, s['title'], XB, TX, 64, M, 0, W - 2 * M, 420, WHITE, dry=True)
    e2, _ = block(d, s['body'], MD, BX, 44, M, e1 + 52, W - 2 * M, 700, SOFT, dry=True)
    total = badge + e2
    y = 150 + max(0, (1100 - total) * 0.46)
    if s.get('num'):
        d.ellipse((M, y, M + 120, y + 120), fill=AMBER)
        f = F(XB, 76); tw = f.getlength(s['num'])
        d.text((M + 60 - tw / 2, y + 12), s['num'], font=f, fill=NAVY_INK)
        y += 170
    end, _ = block(d, s['title'], XB, TX, 64, M, y, W - 2 * M, 420, WHITE)
    block(d, s['body'], MD, BX, 44, M, end + 52, W - 2 * M, 700, SOFT)
    footer(d, handle, i, n)
    return im

def render_chat(s, i, n, handle):
    im, d = canvas(); top_row(d, s, i, n)
    end, _ = block(d, s['title'], XB, 96, 64, M, 230, W - 2 * M, 200, WHITE)
    y = end + 60
    f = F(SB, 50)
    for b in s['bubbles']:
        check_glyphs(b, SB, b)
        tw = f.getlength(b); bw = tw + 90
        x1 = W - M; x0 = x1 - bw
        d.rounded_rectangle((x0, y, x1, y + 120), radius=44, fill=TEAL)
        d.text((x0 + 45, y + 30), b, font=f, fill=NAVY_INK)
        y += 150
    y += 30
    block(d, s['note'], MD, 52, 40, M, y, W - 2 * M, 1190 - y, SOFT)
    footer(d, handle, i, n)
    return im

def render_shot(s, i, n, handle):
    im, d = canvas(); top_row(d, s, i, n)
    y = 190
    if s.get('num'):
        d.ellipse((M, y - 6, M + 84, y + 78), fill=AMBER)
        f = F(XB, 54); tw = f.getlength(s['num'])
        d.text((M + 42 - tw / 2, y + 6), s['num'], font=f, fill=NAVY_INK)
        tx = M + 116
    else:
        tx = M
    end, _ = block(d, s['title'], XB, 70, 54, tx, y, W - M - tx, 170, WHITE)
    shot = Image.open(os.path.join(CAR, s['image'])).convert('RGB')
    ch = 690
    cw = int(shot.width * ch / shot.height)
    shot = shot.resize((cw, ch), Image.LANCZOS)
    cx, cy = (W - cw) // 2, 410
    d.rounded_rectangle((cx - 10, cy - 10, cx + cw + 10, cy + ch + 10), radius=44, fill=SOFT)
    m = Image.new('L', (cw, ch), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=36, fill=255)
    im.paste(shot, (cx, cy), m)
    block(d, s['caption'], MD, 32, 28, M, cy + ch + 32, W - 2 * M, 1250 - (cy + ch + 32), SOFT, align='center')
    footer(d, handle, i, n)
    return im

def render_cta(s, i, n, handle):
    im, d = canvas(); top_row(d, s, i, n)
    end, _ = block(d, s['title'], XB, 92, 60, M, 230, W - 2 * M, 420, WHITE)
    by = max(end + 60, 640)
    f = F(XB, 46)
    check_glyphs(s['button'], XB, 'bouton')
    bw = W - 2 * M
    while f.getlength(s['button']) + 100 > bw:
        f = F(XB, f.size - 2)
    d.rounded_rectangle((M, by, M + bw, by + 150), radius=75, fill=AMBER)
    tw = f.getlength(s['button'])
    d.text((M + (bw - tw) / 2, by + 75 - f.size * 0.62), s['button'], font=f, fill=NAVY_INK)
    block(d, s['sub'], MD, 46, 38, M, by + 200, W - 2 * M, 1220 - (by + 200), SOFT)
    footer(d, handle, i, n)
    return im

R = {'cover': render_cover, 'text': render_text, 'chat': render_chat, 'shot': render_shot, 'cta': render_cta}

def main():
    spec = json.load(open(os.path.join(CAR, 'carousels.json'), encoding='utf-8'))
    handle = spec['handle']
    md = ['# Carrousels prêts à poster — @amkweb.cm', '',
          '> Généré par `tools/content/render_carousels.py` depuis `content/carousels/carousels.json` (source unique). **Ne pas éditer ce fichier à la main.**',
          '> Publication : King seul. Rien n\'est marqué publié tant que King ne le confirme pas.', '']
    for c in spec['carousels']:
        n = len(c['slides'])
        assert n <= 7, f"{c['id']} : {n} slides (max 7)"
        assert c['slides'][0]['kind'] == 'cover' and c['slides'][-1]['kind'] == 'cta', c['id']
        assert sum(1 for s in c['slides'] if s['kind'] == 'cta') == 1, c['id']
        out = os.path.join(CAR, c['id']); os.makedirs(out, exist_ok=True)
        for i, s in enumerate(c['slides']):
            im = R[s['kind']](s, i, n, handle)
            im.save(os.path.join(out, f'slide-{i + 1}.png'), optimize=True)
        print(f"✓ {c['id']} : {n} slides")
        md += [f"## {c['id']} · {c['calendar']}", '',
               f"**Cible :** {c['audience']} · **Objectif :** {c['objective']} · **Lecture :** {c['reading']}", '',
               f"**Fichiers :** `content/carousels/{c['id']}/slide-1.png` … `slide-{n}.png` (1080×1350, dans l'ordre)", '',
               '| # | Slide | Texte (dans l\'image) | Texte alternatif (Instagram → Options avancées) |', '|---|---|---|---|']
        for i, s in enumerate(c['slides']):
            shown = ' / '.join(x for x in [s.get('tag'), s.get('label'), s.get('num'), s['title'], s.get('title2'), s.get('body'), ' / '.join(s.get('bubbles', [])),
                                          s.get('note'), s.get('button'), s.get('sub'), s.get('caption')] if x)
            shown = shown.replace('*', '').replace('\n', ' · ').replace('|', '/')
            md.append(f"| {i + 1} | {s['kind']} | {shown} | {s['alt'].replace('|', '/')} |")
        md += ['', '**Légende (copier-coller) :**', '', '```', c['caption_fr'], '', c['hashtags'], '```', '']
    open(os.path.join(CAR, 'POST-READY.md'), 'w', encoding='utf-8').write('\n'.join(md))
    print('✓ POST-READY.md')

if __name__ == '__main__':
    main()
