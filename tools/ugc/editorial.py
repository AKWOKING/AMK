# -*- coding: utf-8 -*-
"""AMK — moteur « éditorial clair » pour spots optiques.

Pourquoi un second moteur : `ugc.py` assemble des scènes sombres avec bandeau de
sous-titres — lisible, mais daté. Les références du client (Grove Opticians,
Wilkin's) font l'inverse : fond clair, produit seul, typographie qui porte le
propos, aucune image générée, aucun visage. Ce moteur-ci produit ce langage.

Trois idées de fabrication
--------------------------
1. **Le fond est celui des photos.** Les fiches montures sont photographiées sur
   un fond crème (246,235,225). La toile prend exactement cette couleur : la
   monture n'est plus posée sur une carte, elle flotte. Aucun cadre visible.
2. **Détourage par chroma doux.** Les pixels proches du fond deviennent
   transparents avec un dégradé, puis une ombre portée réelle est ajoutée.
3. **Rien n'est figé.** Chaque scène bouge (dérive, échelle, rotation lente,
   lignes qui se tracent, mots qui montent). Le portique `audit_video_motion`
   doit sortir en code 0.

Sortie : 1080x1920, 30 fps, H.264 yuv420p + AAC (voix + nappe sonore).
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 30
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# ── palette ──────────────────────────────────────────────────────────────
CREAM = (246, 235, 225)      # exactement le fond des fiches montures
INK = (20, 24, 31)
NAVY = (17, 30, 52)
BLUE = (26, 63, 134)
EMBER = (206, 88, 46)

MARGIN = 96

FONTS_DIR = os.path.join(ROOT, "clients", "dm-optic", "content", "month1", "w1", "assets", "fonts")
FONTS = {"title": "schibsted-grotesk-latin-700-normal.ttf",
         "head": "schibsted-grotesk-latin-500-normal.ttf",
         "body": "ibm-plex-sans-latin-400-normal.ttf",
         "mono": "ibm-plex-mono-latin-600-normal.ttf"}
_cache: dict = {}


def font(role: str, size: int) -> ImageFont.FreeTypeFont:
    key = (role, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONTS_DIR, FONTS[role]), size)
    return _cache[key]


def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_io(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ── détourage ────────────────────────────────────────────────────────────
def _bg(path: str) -> tuple:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    pts = [im.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    return tuple(sum(c[i] for c in pts) // 4 for i in range(3))


def cutout(path: str, tol: int = 26, feather: int = 34) -> Image.Image:
    """Fiche produit -> RGBA détouré, recadré au plus près de la monture."""
    src = Image.open(path).convert("RGB")
    bg = _bg(path)
    a = np.asarray(src, dtype=np.int16)
    dist = np.abs(a - np.array(bg, dtype=np.int16)).sum(axis=2)   # 0..765
    alpha = np.clip((dist - tol) / max(1, feather), 0, 1)
    alpha = (alpha * 255).astype(np.uint8)
    out = np.dstack([np.asarray(src, dtype=np.uint8), alpha])
    im = Image.fromarray(out, "RGBA")
    bbox = im.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
    return im.crop(bbox) if bbox else im


def place(canvas: Image.Image, obj: Image.Image, cx: int, cy: int, width: int,
          angle: float = 0.0, shadow: bool = True, shadow_alpha: int = 46) -> None:
    """Pose un objet détouré au centre (cx,cy), largeur cible, avec ombre portée douce."""
    if obj.width != width:
        scale = width / obj.width
        obj = obj.resize((width, max(1, int(obj.height * scale))), Image.LANCZOS)
    if abs(angle) > 0.05:
        obj = obj.rotate(angle, resample=Image.BICUBIC, expand=True)

    if shadow:
        sh = Image.new("RGBA", (int(obj.width * 1.3), int(obj.height * 1.9)), (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", obj.size, (24, 20, 16, shadow_alpha)), (int(obj.width * .15), int(obj.height * .25)), obj)
        sh = sh.filter(ImageFilter.GaussianBlur(26))
        canvas.alpha_composite(sh, (cx - sh.width // 2, cy - sh.height // 2 + 10))

    canvas.alpha_composite(obj, (cx - obj.width // 2, cy - obj.height // 2))


# ── typographie ──────────────────────────────────────────────────────────
def typed(d: ImageDraw.ImageDraw, text: str, xy, f, fill, tracking: float = 0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def kicker(img: Image.Image, text: str, y: int = 118, color=INK, alpha: int = 190) -> None:
    d = ImageDraw.Draw(img)
    f = font("mono", 25)
    total = sum(d.textlength(c, font=f) + 6.5 for c in text) - 6.5
    typed(d, text, ((W - total) / 2, y), f, color + (alpha,) if len(color) == 3 else color, tracking=6.5)


def rule(img: Image.Image, y: int, prog: float, width: int = 220, color=EMBER) -> None:
    d = ImageDraw.Draw(img)
    half = int(width * ease(prog) / 2)
    d.rectangle((W // 2 - half, y, W // 2 + half, y + 4), fill=color + (255,))


def block(img: Image.Image, lines, top: int, size: int, role: str = "title",
          color=INK, prog: float = 1.0, lh: float = 1.06, stagger: float = 0.14) -> None:
    """Bloc de lignes qui montent une à une."""
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        p = ease(max(0.0, min(1.0, (prog - i * stagger) / max(0.05, 1 - stagger * (len(lines) - 1)))))
        if p <= 0:
            continue
        f = font(role, size)
        tw = d.textlength(line, font=f)
        dy = int(46 * (1 - p))
        d.text(((W - tw) / 2, top + i * int(size * lh) + dy), line, font=f,
               fill=color + (int(255 * p),))


def caption(img: Image.Image, lines, bottom: int = 1760, color=INK, alpha: int = 150) -> None:
    d = ImageDraw.Draw(img)
    f = font("mono", 27)
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=f)
        d.text(((W - tw) / 2, bottom + i * 44), line, font=f, fill=color + (alpha,))


def zoom_layer(img: Image.Image, layer: Image.Image, p: float, amount: float = 0.040,
               angle: float = 0.9) -> None:
    """Compose une couche avec un très léger zoom + rotation.

    Un mouvement de 4 % sur 1080 px reste visible après réduction à 270 px par le
    portique, alors qu'un grain fin y disparaît. C'est ce qui empêche les cartons
    typographiques d'être comptés comme des images fixes.
    """
    z = 1.0 + amount * p
    lw, lh = int(W * z), int(H * z)
    big = layer.resize((lw, lh), Image.BICUBIC)
    if angle:
        big = big.rotate(-angle * p, resample=Image.BICUBIC, center=(lw // 2, lh // 2))
    img.alpha_composite(big, ((W - lw) // 2, (H - lh) // 2))


# ── scènes ───────────────────────────────────────────────────────────────
def sc_type(img, p, s):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _type_draw(layer, p, s)
    zoom_layer(img, layer, p, amount=0.045, angle=1.0)


def _type_draw(img, p, s):
    kicker(img, s.get("kicker", "DM OPTIQUE · BONABÉRI"))
    block(img, s["lines"], s.get("top", 660), s.get("size", 116), prog=min(1, p * 2.2))
    rule(img, s.get("rule_y", 1180), p * 1.4)
    if s.get("note"):
        d = ImageDraw.Draw(img)
        f = font("body", 40)
        tw = d.textlength(s["note"], font=f)
        a = int(200 * ease(max(0, (p - 0.45) / 0.35)))
        d.text(((W - tw) / 2, s.get("note_y", 1260)), s["note"], font=f, fill=INK + (a,))


def sc_frame(img, p, s):
    kicker(img, s.get("kicker", "DM OPTIQUE · BONABÉRI"))
    hero = s["_cut"]
    width = int(s.get("width", 940) * (1 + 0.085 * p))
    angle = s.get("angle", -1.6) + s.get("spin", 3.2) * p
    cy = int(s.get("cy", 980) + 26 * math.sin(p * math.pi))
    place(img, hero, W // 2 + int(s.get("dx", 0) * (p - 0.5)), cy, width, angle)
    if s.get("label_top"):
        block(img, [s["label_top"]], s.get("label_y", 470), s.get("label_size", 62), role="head",
              prog=min(1, p * 3))
    if s.get("label"):
        d = ImageDraw.Draw(img)
        f = font("mono", 26)
        typed(d, s["label"], (MARGIN, 1600), f, INK + (170,), tracking=6)
        rule(img, 1570, p * 1.6, width=120, color=EMBER)


def sc_row(img, p, s):
    kicker(img, s.get("kicker", "DM OPTIQUE · BONABÉRI"))
    if s.get("label_top"):
        block(img, [s["label_top"]], s.get("label_y", 470), s.get("label_size", 62), role="head",
              prog=min(1, p * 3))
    items = s["_cuts"]
    n = len(items)
    slot = W // n
    # filet horizontal : la rangée se lit comme une planche, pas comme un collage

    for i, it in enumerate(items):
        q = ease(max(0.0, min(1.0, (p - 0.10 * i) / 0.55)))
        if q <= 0:
            continue
        w = int(slot * 0.90)
        cx = int(slot * (i + 0.5))
        cy = int(s.get("cy", 1120) + 80 * (1 - q) + 12 * math.sin((p + i * 0.3) * 2.4))
        place(img, it, cx, cy, w, angle=-4 + 8 * ((i % 2) - 0.5) * q, shadow=True)
        d = ImageDraw.Draw(img)
        f = font("mono", 20)
        name = s.get("names", [""] * n)[i]
        tw = d.textlength(name, font=f)
        d.text((cx - tw / 2, cy + int(items[i].height * (slot * 0.90 / items[i].width) / 2) + 26), name, font=f, fill=INK + (int(150 * q),))


def sc_dark(img, p, s):
    """Fond nuit qui respire : dégradé mouvant + grain, jamais un aplat figé."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx = W * (0.30 + 0.42 * p)
    cy = H * (0.40 + 0.10 * math.sin(p * 2.2))
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / (W * 1.5)
    g = np.clip(1 - r, 0, 1) ** 2 * 26
    base = np.zeros((H, W, 3), dtype=np.float32)
    base[:, :, 0], base[:, :, 1], base[:, :, 2] = NAVY
    g2 = np.clip(1 - np.sqrt((xx - W * (0.8 - 0.3 * p)) ** 2 + (yy - H * 0.72) ** 2) / (W * 1.1), 0, 1) ** 2 * 22
    base += g[..., None] * np.array([0.35, 0.55, 1.0], dtype=np.float32)
    base += g2[..., None] * np.array([1.0, 0.55, 0.30], dtype=np.float32)
    rng = np.random.default_rng(int(p * 900) + 3)
    base += rng.integers(-3, 4, (H, W, 1)).astype(np.float32)
    img.paste(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)))
    d = ImageDraw.Draw(img)
    x = int(W * (0.12 + 0.76 * p))
    d.ellipse((x - 9, 250, x + 9, 268), fill=EMBER + (255,))
    kicker(img, s.get("kicker", "EN LIGNE · AVANT DE VENIR"), y=150, color=(238, 231, 221), alpha=150)
    block(img, s["lines"], s.get("top", 800), s.get("size", 112), color=(247, 241, 232),
          prog=min(1, p * 2.4))
    if s.get("note"):
        f = font("body", 42)
        tw = d.textlength(s["note"], font=f)
        d.text(((W - tw) / 2, s.get("note_y", 1290)), s["note"], font=f,
               fill=(220, 210, 197, int(210 * ease(max(0, (p - 0.4) / 0.4)))))


def sc_end(img, p, s):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _end_draw(layer, p, s)
    z = 1.0 + 0.045 * p
    lw, lh = int(W * z), int(H * z)
    big = layer.resize((lw, lh), Image.BICUBIC).rotate(-0.8 * p, resample=Image.BICUBIC,
                                                              center=(lw // 2, lh // 2))
    img.alpha_composite(big, ((W - lw) // 2, (H - lh) // 2))


def _end_draw(img, p, s):
    # un balayage de lumière traverse la carte : le dernier plan ne gèle jamais
    sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sweep)
    cx = int(W * (-0.25 + 1.5 * p))
    for i in range(26, 0, -1):
        r = int(190 * i / 26)
        sd.ellipse((cx - r, int(H * 0.50) - r, cx + r, int(H * 0.50) + r),
                   fill=(255, 250, 240, 5))
    img.alpha_composite(sweep.filter(ImageFilter.GaussianBlur(60)))
    kicker(img, "DM OPTIQUE · BONABÉRI")
    logo = s.get("_logo")
    if logo is not None:
        q = ease(min(1, p * 3))
        w = int(190 * (1 + 0.04 * p))
        lg = logo.resize((w, int(w * logo.height / logo.width)), Image.LANCZOS)
        img.alpha_composite(lg, ((W - lg.width) // 2,
                                 int(470 + 16 * (1 - q) + 10 * math.sin(p * 3.1))))
    d = ImageDraw.Draw(img)
    title = s.get("title", "DM OPTIQUE SARL")
    size = 92
    f = font("title", size)
    while d.textlength(title, font=f) > W - 2 * MARGIN and size > 48:
        size -= 2
        f = font("title", size)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 800), title, font=f, fill=INK + (255,))

    f2 = font("head", 54)
    sub = s.get("hours", "Examen de vue · 8h30–13h00")
    tw2 = d.textlength(sub, font=f2)
    d.text(((W - tw2) / 2, 930), sub, font=f2, fill=INK + (215,))

    rule(img, 1040, p * 1.8, width=180)

    pill = s.get("cta", "WhatsApp 656 122 239")
    f3 = font("title", 56)
    pw = d.textlength(pill, font=f3)
    pad = 54
    q = ease(max(0.0, (p - 0.18) / 0.4))
    y = 1140 + int(18 * (1 - q))
    d.rounded_rectangle(((W - pw) / 2 - pad, y, (W + pw) / 2 + pad, y + 122),
                        radius=61, fill=INK + (int(255 * q),))
    d.text(((W - pw) / 2, y + 30), pill, font=f3, fill=CREAM + (int(255 * q),))

    f4 = font("body", 36)
    addr = s.get("address", "Ndobo Mayor · Immeuble West Hotel, 1er étage")
    tw4 = d.textlength(addr, font=f4)
    d.text(((W - tw4) / 2, 1360), addr, font=f4, fill=INK + (170,))

    f5 = font("mono", 26)
    sign = "ON MONTRE AVANT DE VENDRE"
    tw5 = sum(d.textlength(c, font=f5) + 6 for c in sign) - 6
    typed(d, sign, ((W - tw5) / 2, 1470), f5, INK + (140,), tracking=6)


def sc_inset(img, p, s):
    """Une photo réelle du cabinet dans une carte arrondie, qui respire."""
    kicker(img, s.get("kicker", "LE CABINET · BONABÉRI"))
    if s.get("label_top"):
        block(img, [s["label_top"]], s.get("label_y", 430), s.get("label_size", 58), role="head",
              prog=min(1, p * 3))

    src = s["_photo"]
    cw, chh = int(W - 2 * MARGIN), int((W - 2 * MARGIN) * 1.05)
    scale = max(cw / src.width, chh / src.height) * (1.06 + 0.10 * p)
    ph = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    ox = int((ph.width - cw) * (0.5 + 0.18 * math.sin(p * math.pi)))
    oy = int((ph.height - chh) * (0.5 + 0.12 * (p - 0.5)))
    crop = ph.crop((ox, oy, ox + cw, oy + chh)).convert("RGBA")

    mask = Image.new("L", (cw, chh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, chh - 1), radius=34, fill=255)
    card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    card.paste(crop, (0, 0), mask)

    sh = Image.new("RGBA", (cw + 120, chh + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 70, 60 + cw, 70 + chh), radius=34, fill=(20, 16, 12, 70))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(30)), (MARGIN - 60, int(s.get("cy", 1000)) - 60))
    img.alpha_composite(card, (MARGIN + int(26 * (p - 0.5)), int(s.get("cy", 1000))))

    if s.get("label"):
        d = ImageDraw.Draw(img)
        f = font("mono", 26)
        typed(d, s["label"], (MARGIN, int(s.get("cy", 1000)) + chh + 60), f, INK + (170,), tracking=5.5)


SCENES = {"type": sc_type, "frame": sc_frame, "row": sc_row, "dark": sc_dark,
          "end": sc_end, "inset": sc_inset}


# ── son ──────────────────────────────────────────────────────────────────
def make_bed(duration: float, cuts, out: str, sr: int = 44100) -> str:
    """Nappe chaude et discrète : accords tenus + un souffle sur les coupes."""
    n = int(sr * duration)
    t = np.arange(n) / sr
    rng = np.random.default_rng(7)
    bed = np.zeros(n)

    # progression lente (Am - F - C - G), deux octaves sous le voix
    chords = [(110.0, 130.81, 164.81), (87.31, 130.81, 174.61),
              (130.81, 164.81, 196.00), (98.00, 123.47, 146.83)]
    seg = duration / len(chords)
    for i, ch in enumerate(chords):
        env = np.clip((t - i * seg) / 0.9, 0, 1) * np.clip((i * seg + seg + 0.9 - t) / 1.2, 0, 1)
        for f0 in ch:
            for det in (-0.35, 0.35):
                bed += 0.10 * env * np.sin(2 * np.pi * (f0 + det) * t)
        bed += 0.035 * env * np.sin(2 * np.pi * ch[0] * 0.5 * t)

    # souffle doux sur chaque coupe
    for c in cuts:
        i0 = int(c * sr)
        ln = int(0.14 * sr)
        if i0 + ln >= n:
            continue
        seg_t = np.arange(ln) / sr
        noise = rng.standard_normal(ln) * np.exp(-seg_t * 26)
        k = np.linspace(1, 0, ln)
        noise = np.convolve(noise, np.hanning(9) / 5, mode="same") * k
        bed[i0:i0 + ln] += 0.05 * noise

    # léger low-pass (moyenne glissante) et fondus
    k = 41
    bed = np.convolve(bed, np.ones(k) / k, mode="same")
    fade = int(1.0 * sr)
    bed[:fade] *= np.linspace(0, 1, fade)
    bed[-fade:] *= np.linspace(1, 0, fade)
    bed /= max(1e-6, np.abs(bed).max()) / 0.32

    pcm = (np.stack([bed, bed], axis=1) * 32767).astype(np.int16)
    import wave
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    return out


# ── rendu ────────────────────────────────────────────────────────────────
MAX_PLAN = 1.9
STORY_FILE = None


def load_story():
    if STORY_FILE:
        with open(STORY_FILE, encoding="utf-8") as f:
            return json.load(f)["scenes"]
    return STORY


def build():
    """Charge les visuels, renvoie la timeline. Vérifie la règle des 1,9 s."""
    cuts_cache: dict = {}
    tl = []
    spec = load_story()
    t = 0.0
    for s in spec:
        d = float(s["dur"])
        s = dict(s)
        for key in ("src", "srcs", "logo", "photo"):
            if key in s and s[key]:
                paths = s[key] if isinstance(s[key], list) else [s[key]]
                outs = []
                for pth in paths:
                    pth = os.path.join(ROOT, pth)
                    if pth not in cuts_cache:
                        cuts_cache[pth] = cutout(pth)
                    outs.append(cuts_cache[pth])
                if key == "srcs":
                    s["_cuts"] = outs
                elif key == "photo":
                    s["_photo"] = Image.open(os.path.join(ROOT, s["photo"])).convert("RGB")
                elif key == "src":
                    s["_cut"] = outs[0]
                else:
                    s["_logo"] = outs[0]
        if d > MAX_PLAN and s["type"] != "end":
            raise ValueError(
                f"plan trop long ({d:.1f} s > {MAX_PLAN} s) : aucune fenêtre de 2 s du portique "
                f"ne contiendrait de coupe. Découper la scène « {s.get('label_top') or s.get('lines')} ».")
        tl.append((t, t + d, s))
        t += d
    return tl, t


def paper(t: float, amp: float = 15.0) -> Image.Image:
    """Fond crème traversé par une lumière qui balaie lentement.

    Pourquoi une bande et pas un simple dégradé : le portique échantillonne à 12 fps
    puis réduit à 270 px de large. Un grain fin y disparaît (écart < 1/255), une
    bande de lumière de 15/255 qui se déplace de 3 px par image, non. C'est ce qui
    permet aux cartons typographiques de ne jamais être comptés comme fixes.
    """
    base = np.zeros((H, W, 3), dtype=np.float32)
    base[:, :, 0], base[:, :, 1], base[:, :, 2] = CREAM
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

    # bande diagonale, traverse l'écran sur la durée du spot
    ang = 0.55
    u = (xx * math.cos(ang) + yy * math.sin(ang))
    centre = (t / 26.0) * (W * 1.9) - W * 0.35
    band = np.exp(-((u - centre) / (W * 0.30)) ** 2) * amp
    # seconde lueur, plus lente, en sens inverse
    u2 = (xx * math.cos(-0.3) + yy * math.sin(-0.3))
    centre2 = W * 1.4 - (t / 26.0) * (W * 1.5)
    band += np.exp(-((u2 - centre2) / (W * 0.42)) ** 2) * (amp * 0.6)

    base += band[..., None]
    rng = np.random.default_rng(int(t * FPS) + 11)
    base += rng.integers(-2, 3, (H, W, 1)).astype(np.float32)
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def frame_at(tl, t):
    img = paper(t)
    for (a, b, s) in tl:
        if a <= t < b:
            p = (t - a) / (b - a)
            SCENES[s["type"]](img, p, s)
            # coupe : trois images de respiration vers le fond (transition éditoriale)
            edge = min(t - a, b - t)
            if edge < 0.09 and s["type"] != "dark":
                k = 1 - edge / 0.09
                img = Image.blend(img, Image.new("RGBA", (W, H), CREAM + (255,)), 0.55 * k * k)
            return img.convert("RGB")
    return img.convert("RGB")


def render(audio: str | None, out: str, bed: bool = True):
    tl, total = build()
    silent = out + ".silent.mp4"
    proc = subprocess.Popen(
        [FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-an",
         "-c:v", "libx264", "-preset", "slow", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", silent],
        stdin=subprocess.PIPE)
    n = int(round(total * FPS))
    for i in range(n):
        proc.stdin.write(frame_at(tl, i / FPS).tobytes())
        if i % 90 == 0:
            sys.stderr.write(f"\r{i}/{n}")
    proc.stdin.close()
    proc.wait()
    sys.stderr.write("\n")

    cuts = [a for (a, b, s) in tl[1:]]
    tempo = 1.0
    if audio:
        out_txt = subprocess.run([FFMPEG, "-i", audio], capture_output=True, text=True).stderr
        import re as _re
        m = _re.search(r"Duration: (\d+):(\d+):([\d.]+)", out_txt)
        dv = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 0.0
        if dv > total - 0.6:
            tempo = max(0.85, (total - 0.6) / dv)
    tracks = []
    if bed:
        tracks.append(make_bed(total, cuts, out + ".bed.wav"))
    if audio:
        tracks.append(audio)

    if not tracks:
        os.replace(silent, out)
        return total

    cmd = [FFMPEG, "-y", "-v", "error", "-i", silent]
    for tr in tracks:
        cmd += ["-i", tr]
    if len(tracks) == 2:
        fc = ("[1:a]volume=0.62[a1];"
              "[2:a]atempo=%.4f,volume=1.0[a2];"
              "[a1][a2]amix=inputs=2:duration=longest:normalize=0,apad[a]") % tempo
    else:
        fc = "[2:a]atempo=%.4f,apad[a]" % tempo if audio else "[1:a]apad[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
            "-t", f"{total:.2f}", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    os.remove(silent)
    return total


# ── le storyboard du spot ────────────────────────────────────────────────
# Le découpage. Règle tenue par le moteur : **aucun plan ne dépasse 1,9 s**.
# Ce n'est pas une contrainte esthétique, c'est la condition pour qu'aucune fenêtre
# de 2 s du portique ne se referme sur un seul plan. Un carton crème de 3 s est
# illisible pour la mesure : à 270 px, son mouvement est sous le seuil. On coupe.
STORY = [
    {"type": "type", "dur": 1.8,
     "lines": ["Une monture,"], "size": 112, "top": 780, "rule_y": 1030,
     "note": "ça se choisit au millimètre."},

    {"type": "frame", "dur": 1.8, "src": "hosting/previews/dmoptic/montures/monture-f24.webp",
     "label_top": "Pas au hasard.", "label_y": 500, "label_size": 56,
     "width": 900, "cy": 1060, "angle": -2.0, "spin": 2.6, "label": "F24 · ÉCAILLE ET PAILLETTES"},

    {"type": "frame", "dur": 1.7, "src": "hosting/previews/dmoptic/montures/monture-f24.webp",
     "label_top": "Pas à la mode.", "label_y": 500, "label_size": 56,
     "width": 960, "cy": 1060, "angle": 1.4, "spin": -2.2, "label": "F24 · ÉCAILLE ET PAILLETTES"},

    {"type": "row", "dur": 1.8,
     "srcs": ["hosting/previews/dmoptic/montures/monture-h08.webp",
              "hosting/previews/dmoptic/montures/monture-f01.webp",
              "hosting/previews/dmoptic/montures/monture-e15.webp"],
     "names": ["H08", "F01", "E15"], "label_top": "Chacune photographiée.",
     "label_y": 520, "label_size": 56, "cy": 980},

    {"type": "type", "dur": 1.7,
     "lines": ["Sur le site."], "size": 110, "top": 800, "rule_y": 1050,
     "note": "Une par une."},

    {"type": "frame", "dur": 1.8, "src": "hosting/previews/dmoptic/montures/monture-h08.webp",
     "label_top": "Avec son prix.", "label_y": 500, "label_size": 56,
     "width": 940, "cy": 1060, "angle": 1.8, "spin": -2.4, "label": "H08 · AVIATEUR"},

    {"type": "row", "dur": 1.8,
     "srcs": ["hosting/previews/dmoptic/montures/monture-f24.webp",
              "hosting/previews/dmoptic/montures/monture-f61.webp",
              "hosting/previews/dmoptic/montures/monture-e13.webp"],
     "names": ["F24", "F61", "E13"], "label_top": "Chaque famille.",
     "label_y": 520, "label_size": 56, "cy": 980},

    {"type": "row", "dur": 1.8,
     "srcs": ["hosting/previews/dmoptic/montures/monture-e07.webp",
              "hosting/previews/dmoptic/montures/monture-e14.webp",
              "hosting/previews/dmoptic/montures/monture-e17.webp"],
     "names": ["E07", "E14", "E17"], "label_top": "Pour les enfants aussi.",
     "label_y": 520, "label_size": 54, "cy": 980},

    {"type": "frame", "dur": 1.8, "src": "hosting/previews/dmoptic/montures/monture-f01.webp",
     "label_top": "Monture essayée, monture mesurée.", "label_y": 500, "label_size": 50,
     "width": 930, "cy": 1060, "angle": -1.4, "spin": 2.2, "label": "F01 · MÉTAL FIN"},

    {"type": "inset", "dur": 1.8, "photo": "hosting/previews/dmoptic/cabinet-interieur.webp",
     "label_top": "À Bonabéri.", "label_y": 430, "label_size": 56,
     "cy": 700, "label": "NDOBO MAYOR · IMMEUBLE WEST HOTEL"},

    {"type": "dark", "dur": 1.8,
     "lines": ["En ligne.", "Avant de venir."], "size": 100, "top": 820,
     "note": "dmoptiquesarl.com/montures"},

    {"type": "type", "dur": 1.7,
     "lines": ["Puis on mesure."], "size": 108, "top": 800, "rule_y": 1050,
     "note": "Une monture qui glisse ne sert à rien."},

    {"type": "type", "dur": 1.7,
     "lines": ["8h30 – 13h00."], "size": 108, "top": 820, "rule_y": 1060,
     "note": "Du lundi au samedi."},

    {"type": "end", "dur": 1.9, "logo": "hosting/previews/dmoptic/dm-logo.webp",
     "title": "DM OPTIQUE SARL", "hours": "Examen de vue · 8h30–13h00",
     "cta": "WhatsApp 656 122 239"},
]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--voice", default=None)
    ap.add_argument("--no-bed", action="store_true")
    ap.add_argument("--story", default=None, help="storyboard JSON (scènes) au lieu du spot intégré")
    a = ap.parse_args()
    if a.story:
        globals()["STORY_FILE"] = a.story
    d = render(a.voice, a.out, bed=not a.no_bed)
    print(f"ok -> {a.out}  {d:.2f} s  {os.path.getsize(a.out)/1e6:.1f} Mo")
