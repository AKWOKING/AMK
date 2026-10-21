# -*- coding: utf-8 -*-
"""UGS/AMK — moteur de montage UGC « spec-driven ».

Un storyboard JSON décrit une suite de scènes ; le moteur rend un MP4 1080x1920
avec mouvement continu, sous-titres incrustés, voix et carton de fin — puis passe
le portique `tools/qa/audit_video_motion.py`.

Types de scène
--------------
  photo    une image du dépôt (produit, intérieur, enseigne…) + mouvement
  clip     une vidéo externe (clip IA Veo/HeyGen, ou séquence filmée au cabinet)
  card     un carton typographique (accroche, chiffre, question)
  endcard  le carton de fin de marque (logo, horaires, WhatsApp, adresse)

Chaque scène porte un `sub` (sous-titre incrusté, `\\n` autorisé) — c'est lui que
le spectateur lit sans le son, pas la piste automatique de la plateforme.

Usage
-----
  python3 tools/ugc/ugc.py render spec.json --out video.mp4 [--voice voix.mp3]
                                            [--cover cover.jpg] [--qc]
  python3 tools/ugc/ugc.py check  spec.json          # valide le storyboard
  python3 tools/ugc/ugc.py providers                 # état des fournisseurs
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_FONTS = os.path.join(ROOT, "clients", "dm-optic", "content", "month1", "w1", "assets", "fonts")

W, H, FPS = 1080, 1920, 30
K = 1.20                      # marge de manœuvre pour le recadrage mouvant

PALETTE = {
    "brand": (26, 63, 134),
    "ink": (12, 21, 36),
    "night": (10, 18, 32),
    "paper": (238, 241, 245),
    "ember": (224, 112, 58),
    "wa": (11, 122, 62),
    "cream": (250, 248, 242),
}

FONT_FILES = {
    "title": "schibsted-grotesk-latin-700-normal.ttf",
    "head": "schibsted-grotesk-latin-500-normal.ttf",
    "body": "ibm-plex-sans-latin-400-normal.ttf",
    "mono": "ibm-plex-mono-latin-600-normal.ttf",
}

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


# ─────────────────────────────────────────────────────────────── utilitaires
def ease(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def probe_duration(path: str) -> float:
    out = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    if not m:
        return 0.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


class Fonts:
    def __init__(self, directory: str):
        self.dir = directory
        self.cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    def get(self, role: str, size: int) -> ImageFont.FreeTypeFont:
        key = (role, size)
        if key not in self.cache:
            path = os.path.join(self.dir, FONT_FILES[role])
            self.cache[key] = ImageFont.truetype(path, size)
        return self.cache[key]

    def fit(self, role: str, text: str, size: int, max_w: int, floor: int = 34) -> tuple[ImageFont.FreeTypeFont, int]:
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        while size > floor:
            f = self.get(role, size)
            if max(probe.textlength(l, font=f) for l in text.split("\n")) <= max_w:
                return f, size
            size -= 2
        return self.get(role, floor), floor


def scrim_mask(top: float = 0.62, band: float = 0.93, soft: float = 0.16) -> Image.Image:
    """Masque vertical : la photo reste lisible en haut et en bas, le texte repose sur un fond dense."""
    m = Image.new("L", (1, H))
    for y in range(H):
        t = y / H
        if t < 0.18:
            v = top
        elif t < 0.18 + soft:
            v = top + (band - top) * (t - 0.18) / soft
        elif t < 0.78:
            v = band
        elif t < 0.78 + soft:
            v = band + (top - band) * (t - 0.78) / soft
        else:
            v = top
        m.putpixel((0, y), int(255 * v))
    return m.resize((W, H))


def sample_bg(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    pts = [im.getpixel(p)[:3] for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
    return tuple(sum(c[i] for c in pts) // 4 for i in range(3))


def tight_crop(src: Image.Image, bg: tuple[int, int, int], pad: float = 0.06) -> Image.Image:
    small = src.resize((max(1, src.width // 4), max(1, src.height // 4)))
    px = small.load()
    xs, ys = [], []
    for y in range(small.height):
        for x in range(small.width):
            r, g, b = px[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 44:
                xs.append(x)
                ys.append(y)
    if not xs:
        return src
    x0, x1 = min(xs) * 4, (max(xs) + 1) * 4
    y0, y1 = min(ys) * 4, (max(ys) + 1) * 4
    mx, my = int((x1 - x0) * pad), int((y1 - y0) * pad)
    return src.crop((max(0, x0 - mx), max(0, y0 - my),
                     min(src.width, x1 + mx), min(src.height, y1 + my)))


def crop_window(big: Image.Image, p: float, zoom: float, pan: float, drift: float) -> Image.Image:
    s = 1.0 + max(0.0, zoom) * p
    cw, ch = min(int(big.width / s), big.width), min(int(big.height / s), big.height)
    ax, ay = big.width - cw, big.height - ch
    x0 = max(0, min(ax, int(ax * (0.5 + pan * 0.5 * (2 * p - 1)))))
    y0 = max(0, min(ay, int(ay * (0.5 + drift * 0.5 * (2 * p - 1)))))
    return big.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


# ──────────────────────────────────────────────────────────── masters (1.20×)
def master_flat(src: Image.Image, focus: float = 0.5) -> Image.Image:
    """Photo quelconque -> 9:16 par recadrage couvrant, ancrage `focus` (0 gauche, 1 droite)."""
    cw, ch = int(W * K), int(H * K)
    s = max(cw / src.width, ch / src.height)
    big = src.resize((max(int(src.width * s), cw), max(int(src.height * s), ch)), Image.LANCZOS)
    left = int((big.width - cw) * focus)
    top = (big.height - ch) // 2
    return big.crop((left, top, left + cw, top + ch)).filter(
        ImageFilter.UnsharpMask(radius=2, percent=55, threshold=3))


def master_product(src: Image.Image) -> Image.Image:
    """Fiche produit sur fond uni -> carte crème sur fond nuit. Le produit n'est pas retouché."""
    bg = sample_bg(src)
    prod = tight_crop(src, bg)
    cw, ch = int(W * K), int(H * K)

    grad = Image.new("L", (1, ch))
    for i in range(ch):
        grad.putpixel((0, i), int(26 * (i / ch)))
    canvas = Image.composite(Image.new("RGB", (cw, ch), (18, 34, 62)),
                             Image.new("RGB", (cw, ch), PALETTE["night"]),
                             grad.resize((cw, ch)))

    card_w, card_h = int(cw * 0.84), int(ch * 0.50)
    card_x, card_y = (cw - card_w) // 2, int(ch * 0.145)

    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (card_x + 10, card_y + 18, card_x + card_w + 10, card_y + card_h + 18),
        radius=42, fill=(0, 0, 0, 130))
    canvas = Image.alpha_composite(canvas.convert("RGBA"),
                                   shadow.filter(ImageFilter.GaussianBlur(26))).convert("RGB")

    ImageDraw.Draw(canvas).rounded_rectangle(
        (card_x, card_y, card_x + card_w, card_y + card_h), radius=42, fill=bg)

    inner_w, inner_h = int(card_w * 0.90), int(card_h * 0.86)
    sc = min(inner_w / prod.width, inner_h / prod.height)
    prod = prod.resize((max(1, int(prod.width * sc)), max(1, int(prod.height * sc))), Image.LANCZOS)
    prod = prod.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))
    canvas.paste(prod, (card_x + (card_w - prod.width) // 2, card_y + (card_h - prod.height) // 2))
    return canvas


class ClipSource:
    """Décode un clip externe en flux, boucle si plus court que la scène."""

    def __init__(self, path: str, width: int, height: int):
        self.path, self.w, self.h = path, width, height
        self.frame_bytes = width * height * 3
        self.dur = probe_duration(path)
        self.proc = None
        self._start()

    def _start(self):
        vf = (f"scale={self.w}:{self.h}:force_original_aspect_ratio=increase,"
              f"crop={self.w}:{self.h},fps={FPS}")
        self.proc = subprocess.Popen(
            [FFMPEG, "-v", "error", "-stream_loop", "-1", "-i", self.path,
             "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            stdout=subprocess.PIPE, bufsize=self.frame_bytes * 3)

    def frame(self) -> Image.Image:
        buf = self.proc.stdout.read(self.frame_bytes)
        while len(buf) < self.frame_bytes:          # sécurité : on relance une fois
            self._start()
            buf = self.proc.stdout.read(self.frame_bytes)
        return Image.frombytes("RGB", (self.w, self.h), buf)

    def close(self):
        if self.proc:
            self.proc.kill()


# ─────────────────────────────────────────────────────────────── rendu scènes
def draw_topband(d: ImageDraw.ImageDraw, text: str, alpha: float):
    if not text:
        return
    f = FONTS.get("mono", 27)
    tw = d.textlength(text, font=f)
    pad, y0 = 26, 74
    x0 = (W - tw) / 2 - pad
    d.rounded_rectangle((x0, y0, x0 + tw + 2 * pad, y0 + 58), radius=10,
                        fill=PALETTE["night"] + (int(150 * alpha),))
    d.text((x0 + pad, y0 + 14), text, font=f, fill=(250, 248, 242, int(235 * alpha)))


def draw_sub(img: Image.Image, text: str, size: int, prog: float, top_ratio: float = 0.702) -> Image.Image:
    if not text:
        return img
    prog = ease(prog)
    f, size = FONTS.fit("title", text, size, W - 150)
    lines = text.split("\n")
    lh = int(size * 1.16)
    block_h = lh * len(lines)
    top = int(H * top_ratio)
    bar_h = block_h + 94
    off = int(14 * (1 - prog))
    a_bar = int(232 * min(1.0, prog * 1.4))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle((0, top + off, W, top + off + bar_h), fill=PALETTE["night"] + (a_bar,))
    half = int(W * 0.11 * prog)
    d.rectangle((W // 2 - half, top + off, W // 2 + half, top + off + 7), fill=PALETTE["ember"] + (255,))
    a = int(255 * min(1.0, prog * 1.5))
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=f)
        d.text(((W - tw) / 2, top + off + 54 + i * lh), line, font=f, fill=(255, 255, 255, a))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def render_card(scene: dict, p: float, base: Image.Image | None = None) -> Image.Image:
    bg = PALETTE[scene.get("bg", "night")]
    img = base.convert("RGB") if base is not None else Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    # halo qui respire : le carton ne gèle jamais
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    cy = int(H * 0.40)
    r = int(520 * (1 + 0.05 * p))
    for i in range(8, 0, -1):
        rr = int(r * i / 8)
        hd.ellipse((W // 2 - rr, cy - rr, W // 2 + rr, cy + rr),
                   fill=PALETTE["brand"] + (int(10 * (9 - i)),))
    img = Image.alpha_composite(img.convert("RGBA"),
                                halo.filter(ImageFilter.GaussianBlur(30))).convert("RGB")
    d = ImageDraw.Draw(img)

    headline = scene.get("headline", "")
    if headline:
        f, _ = FONTS.fit("head", headline, 48, W - 200)
        tw = d.textlength(headline, font=f)
        d.text(((W - tw) / 2, int(H * 0.30)), headline, font=f,
               fill=PALETTE["paper"] + (int(255 * ease(p * 3)),))

    big = scene.get("big", "")
    if big:
        f, _ = FONTS.fit("title", big, scene.get("big_size", 120), W - 140)
        tw = d.textlength(big, font=f)
        d.text(((W - tw) / 2, int(H * 0.42)), big, font=f, fill=(255, 255, 255, 255))

    foot = scene.get("foot", "")
    if foot:
        f, _ = FONTS.fit("body", foot, 42, W - 160)
        tw = d.textlength(foot, font=f)
        d.text(((W - tw) / 2, int(H * 0.58)), foot, font=f,
               fill=PALETTE["paper"] + (int(215 * ease(p * 2.5)),))
    return img


def render_endcard(scene: dict, p: float, base: Image.Image | None = None) -> Image.Image:
    logo_path = os.path.join(ROOT, scene.get("logo", "hosting/previews/dmoptic/dm-logo.webp"))
    img = base.convert("RGB") if base is not None else Image.new("RGB", (W, H), PALETTE["night"])
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    cy, r = int(H * 0.34), int(560 + 30 * p)
    for i in range(8, 0, -1):
        rr = int(r * i / 8)
        hd.ellipse((W // 2 - rr, cy - rr, W // 2 + rr, cy + rr),
                   fill=PALETTE["brand"] + (int(9 * (9 - i)),))
    img = Image.alpha_composite(img.convert("RGBA"),
                                halo.filter(ImageFilter.GaussianBlur(30))).convert("RGB")

    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        lw = int(238 * (1 + 0.05 * p))
        logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
        pad, rad = 26, 34
        pw, ph = logo.width + 2 * pad, logo.height + 2 * pad
        plate = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        ImageDraw.Draw(plate).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=rad,
                                                fill=(255, 255, 255, 255))
        mask = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(mask).rounded_rectangle((pad, pad, pad + logo.width, pad + logo.height),
                                               radius=18, fill=255)
        plate.paste(logo, (pad, pad), mask.crop((pad, pad, pad + logo.width, pad + logo.height)))
        lx, ly = (W - pw) // 2, int(H * 0.235)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((lx + 8, ly + 14, lx + pw + 8, ly + ph + 14),
                                             radius=rad, fill=(0, 0, 0, 120))
        img = Image.alpha_composite(img.convert("RGBA"),
                                    sh.filter(ImageFilter.GaussianBlur(18))).convert("RGB")
        img.paste(plate, (lx, ly), plate)

    d = ImageDraw.Draw(img)
    a = ease(min(1.0, p * 4))
    y = int(H * 0.455)
    head = scene.get("headline", "EXAMEN DE VUE")
    f1 = FONTS.get("head", 46)
    d.text(((W - d.textlength(head, font=f1)) / 2, y), head,
           font=f1, fill=PALETTE["paper"] + (int(255 * a),))

    big = scene.get("big", "8h30–13h00")
    f2, _ = FONTS.fit("title", big, 104, W - 120)
    d.text(((W - d.textlength(big, font=f2)) / 2, y + 70), big,
           font=f2, fill=(255, 255, 255, int(255 * a)))

    sub = scene.get("foot", "du lundi au samedi")
    f3 = FONTS.get("body", 44)
    d.text(((W - d.textlength(sub, font=f3)) / 2, y + 196), sub,
           font=f3, fill=PALETTE["paper"] + (int(210 * a),))

    sign = scene.get("sub", "")
    if sign:
        f0, _ = FONTS.fit("head", sign, 44, W - 180)
        d.text(((W - d.textlength(sign, font=f0)) / 2, int(H * 0.592)), sign,
               font=f0, fill=PALETTE["ember"] + (int(240 * a),))

    a2 = ease(min(1.0, max(0.0, p * 4 - 0.6)))
    cta = scene.get("cta", "WhatsApp 656 122 239")
    py = int(H * 0.715) + int(14 * (1 - a2))
    fw, _ = FONTS.fit("title", cta, 62, W - 120)
    tw = d.textlength(cta, font=fw)
    padx, pady, fh = 46, 30, 62
    d.rounded_rectangle(((W - tw) / 2 - padx, py, (W + tw) / 2 + padx, py + fh + 2 * pady),
                        radius=18, fill=PALETTE["wa"] + (int(255 * a2),))
    d.text(((W - tw) / 2, py + pady), cta, font=fw, fill=(255, 255, 255, int(255 * a2)))

    addr = scene.get("address", "Ndobo Mayor · Immeuble West Hotel, 1er étage")
    f4, _ = FONTS.fit("body", addr, 38, W - 120)
    d.text(((W - d.textlength(addr, font=f4)) / 2, int(H * 0.912)), addr,
           font=f4, fill=(190, 200, 216, int(230 * a2)))
    return img


# ─────────────────────────────────────────────────────────────────── moteur
FONTS: Fonts


def build(spec: dict) -> dict:
    """Prépare les masters et retourne le plan de montage (liste de scènes résolues)."""
    scenes = []
    t = 0.0
    for sc in spec["scenes"]:
        kind = sc["type"]
        d = float(sc["dur"])
        entry = {"type": kind, "start": t, "dur": d, "scene": sc}
        if kind == "photo":
            path = os.path.join(ROOT, sc["src"])
            if not os.path.exists(path):
                raise FileNotFoundError(f"photo introuvable : {sc['src']}")
            src = Image.open(path).convert("RGB")
            if sc.get("layout", "flat") == "product":
                entry["master"] = master_product(src)
            else:
                entry["master"] = master_flat(src, float(sc.get("focus", 0.5)))
        elif kind == "clip":
            path = os.path.join(ROOT, sc["src"])
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"clip introuvable : {sc['src']} — c'est la scène à remplacer par un clip IA "
                    f"ou un rush filmé (voir tools/ugc/README.md)")
            entry["clip"] = ClipSource(path, int(W * K), int(H * K))
        elif kind in ("card", "endcard"):
            if sc.get("src"):
                path = os.path.join(ROOT, sc["src"])
                if not os.path.exists(path):
                    raise FileNotFoundError(f"fond introuvable : {sc['src']}")
                bg = master_flat(Image.open(path).convert("RGB"), float(sc.get("focus", 0.5)))
                entry["bgmaster"] = ImageEnhance.Brightness(bg).enhance(float(sc.get("dim", 0.62)))
                entry["scrim"] = scrim_mask(float(sc.get("scrim_top", 0.62)),
                                            float(sc.get("scrim_band", 0.93)))
        else:
            raise ValueError(f"type de scène inconnu : {kind}")
        scenes.append(entry)
        t += d
    return {"scenes": scenes, "total": t}


def scene_at(plan: dict, t: float) -> tuple[dict, float]:
    for sc in plan["scenes"]:
        if sc["start"] <= t < sc["start"] + sc["dur"]:
            return sc, (t - sc["start"]) / sc["dur"]
    return plan["scenes"][-1], 1.0


def render_frame(plan: dict, t: float, topband: str) -> Image.Image:
    sc, p = scene_at(plan, t)
    conf = sc["scene"]
    kind = sc["type"]

    if kind in ("photo", "clip"):
        zoom = float(conf.get("zoom", 0.15))
        pan = float(conf.get("pan", 0.0))
        drift = float(conf.get("drift", 0.45))
        if kind == "photo":
            img = crop_window(sc["master"], p, zoom, pan, drift)
        else:
            img = crop_window(sc["clip"].frame(), p, zoom, pan, drift)
    elif kind in ("card", "endcard"):
        base = None
        if "bgmaster" in sc:
            base = crop_window(sc["bgmaster"], p, float(conf.get("zoom", 0.18)),
                               float(conf.get("pan", 0.0)), float(conf.get("drift", 0.5)))
            base = Image.composite(Image.new("RGB", (W, H), PALETTE["night"]), base, sc["scrim"])
        img = (render_card if kind == "card" else render_endcard)(conf, p, base)
        # grain fixe par image : casse les aplats dégradés (banding H.264) et garde le carton vivant
        g = int(conf.get("grain", 2))
        if g:
            a = np.asarray(img, dtype=np.int16)
            a = a + np.random.randint(-g, g + 1, a.shape[:2], dtype=np.int16)[..., None]
            img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    img = img.convert("RGBA")
    sub = conf.get("sub", "")
    if sub and kind != "endcard":
        img = draw_sub(img, sub, int(conf.get("sub_size", 84)), ease(min(1.0, p * 4)))
    d = ImageDraw.Draw(img)
    draw_topband(d, conf.get("topband", topband), ease(min(1.0, t / 0.5)))
    return img.convert("RGB")


def encode(spec: dict, plan: dict, out: str, voice: str | None):
    total = plan["total"]
    tmp = out + ".silent.mp4"
    cmd = [FFMPEG, "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", str(spec.get("crf", 20)),
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(round(total * FPS))
    topband = spec.get("topband", "")
    for i in range(n):
        proc.stdin.write(render_frame(plan, i / FPS, topband).tobytes())
        if i % 60 == 0:
            sys.stderr.write(f"\r{i}/{n}")
    proc.stdin.close()
    proc.wait()
    sys.stderr.write("\n")

    audio = voice or spec.get("voice")
    if audio:
        audio = audio if os.path.isabs(audio) else os.path.join(ROOT, audio)
        d_voice = probe_duration(audio)
        tempo = max(0.85, min(1.0, (total - 0.6) / max(0.1, d_voice)))
        subprocess.run([FFMPEG, "-y", "-v", "error", "-i", tmp, "-i", audio,
                        "-filter_complex", f"[1:a]atempo={tempo:.4f},apad[a]",
                        "-map", "0:v:0", "-map", "[a]", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "128k", "-t", f"{total:.2f}",
                        "-movflags", "+faststart", out], check=True)
        os.remove(tmp)
    else:
        os.replace(tmp, out)
    return total


def make_cover(plan: dict, out: str, spec: dict):
    """Couverture 1080x1920 : première image non-carton, accroche dans le carré central."""
    cover = spec.get("cover", {})
    if cover.get("src"):
        src = Image.open(os.path.join(ROOT, cover["src"])).convert("RGB")
        img = crop_window(master_flat(src, float(cover.get("focus", 0.5))), 0.0, 0.0, 0.0, 0.0)
        img = img.convert("RGBA")
    else:
        sc = next((s for s in plan["scenes"] if s["type"] == "photo"), plan["scenes"][0])
        if sc["type"] == "photo":
            img = crop_window(sc["master"], 0.0, 0.0, 0.0, 0.0).convert("RGBA")
        else:
            img = Image.new("RGBA", (W, H), PALETTE["night"])
    # voile : lisibilité du texte sans écraser la photo
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    for y in range(H):
        t = y / H
        if t < 0.12:
            a = int(150 * (1 - t / 0.12))
        elif t < 0.50:
            a = 0
        elif t < 0.80:
            a = int(236 * (t - 0.50) / 0.30)
        else:
            a = 236
        vd.line((0, y, W, y), fill=PALETTE["night"] + (a,))
    img = Image.alpha_composite(img, veil)
    d = ImageDraw.Draw(img)
    top = cover.get("top", "")
    if top:
        draw_topband(d, top, 1.0)
    y = int(H * float(cover.get("y", 0.675)))
    for line, size, gap in cover.get("lines", []):
        f, _ = FONTS.fit("title", line, size, W - 140)
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=(255, 255, 255, 255))
        y += gap
    half = int(W * 0.115)
    d.rectangle((W // 2 - half, y + 4, W // 2 + half, y + 11), fill=PALETTE["ember"])
    foot = cover.get("foot", "")
    if foot:
        f, _ = FONTS.fit("body", foot, 34, W - 120)
        d.text(((W - d.textlength(foot, font=f)) / 2, int(H * 0.935)), foot, font=f,
               fill=(186, 198, 218, 230))
    img.convert("RGB").save(out, quality=92, optimize=True)
    print("cover ->", out)


def run_qc(path: str) -> int:
    qc = os.path.join(ROOT, "tools", "qa", "audit_video_motion.py")
    print("\n── portique mouvement ──")
    res = subprocess.run([sys.executable, qc, path], capture_output=True, text=True)
    tail = [l for l in (res.stdout or res.stderr).splitlines() if l.strip()][-6:]
    print("\n".join(tail))
    return res.returncode


# ────────────────────────────────────────────────────────────────────── CLI
def cmd_render(args):
    global FONTS
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    FONTS = Fonts(os.path.join(ROOT, spec.get("fonts", DEFAULT_FONTS)))
    plan = build(spec)
    out = args.out or os.path.join(ROOT, spec.get("out", "out.mp4"))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    total = encode(spec, plan, out, args.voice)
    dur = probe_duration(out)
    size = os.path.getsize(out) / 1e6
    print(f"ok -> {out}\n   {dur:.2f} s · {size:.1f} Mo · {W}x{H} @ {FPS} fps")
    if args.cover:
        make_cover(plan, args.cover, spec)
    for sc in plan["scenes"]:
        if sc["type"] == "clip":
            sc["clip"].close()
    if args.qc:
        return run_qc(out)
    return 0


def cmd_check(args):
    global FONTS
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    FONTS = Fonts(os.path.join(ROOT, spec.get("fonts", DEFAULT_FONTS)))
    total = 0.0
    print(f"{'#':>2}  {'type':<8} {'dur':>6}  {'début':>6}  détail")
    for i, sc in enumerate(spec["scenes"], 1):
        detail = sc.get("src") or sc.get("big") or sc.get("headline") or sc.get("sub", "")
        exists = "" if sc["type"] not in ("photo", "clip") else (
            "✅" if os.path.exists(os.path.join(ROOT, sc["src"])) else "❌ FICHIER ABSENT")
        print(f"{i:>2}  {sc['type']:<8} {float(sc['dur']):>6.1f}  {total:>6.1f}  {str(detail)[:52]:<54}{exists}")
        total += float(sc["dur"])
    print(f"\ntotal {total:.1f} s · {int(total * FPS)} images · "
          f"{'voix : ' + spec.get('voice', '—') if spec.get('voice') else 'sans voix'}")
    return 0 if total > 0 else 1


def cmd_providers(args):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import providers
    providers.print_status()
    return 0


def main():
    ap = argparse.ArgumentParser(description="AMK UGC engine — storyboard JSON -> MP4")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("render")
    p.add_argument("spec")
    p.add_argument("--out")
    p.add_argument("--voice")
    p.add_argument("--cover")
    p.add_argument("--qc", action="store_true")
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("check")
    p.add_argument("spec")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("providers")
    p.set_defaults(func=cmd_providers)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
