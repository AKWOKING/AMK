#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DM Optique — « Ce que voit quelqu'un qui n'est jamais venu » (31 s, 9:16).

Pourquoi un moteur séparé de `make_dmoptic_tiktok.py` : ce film applique trois règles
qui n'existaient pas dans les rendus précédents (voir research/HOOKS-ET-VIRALITE-2026-10-21.md §8-B) :

  1. **Une seule idée, tenue.** 8 plans, un par étape — pas 15 affirmations en 27 s.
  2. **Chronologie du texte découplée de celle de l'image.** Le texte reste ≥ 3 s ;
     c'est l'image qui change dessous (zoom lent, résolution du flou, coupe).
  3. **Triple hook aligné.** Le visuel rompt (le flou se résout), le texte nomme,
     la voix ajoute la cause.

Honnêteté d'image : les plans 3 à 6 sont des visuels générés — ils portent la mention
« illustration ». Le plan 1 (le lieu), le plan 2 (l'appareil), le plan 7 (le praticien)
et le plan 8 (la vitrine) sont de vraies photos du cabinet.

Usage :
    python3 tools/record/make_dmoptic_etapes.py --preview /tmp/apercu
    python3 tools/record/make_dmoptic_etapes.py --out film.mp4 [--voice voix.mp3]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, "hosting", "previews", "dmoptic")
ETAPES = os.path.join(ROOT, "clients", "dm-optic", "research", "assets", "etapes")
FONTS = os.path.join(ROOT, "clients", "dm-optic", "content", "month1", "w1", "assets", "fonts")

W, H, FPS = 1080, 1920, 30
DUR = 31.0
UP = 1.28          # marge de recadrage : autorise zoom et panoramique sans bande

BRAND = (26, 63, 134)
INK = (12, 21, 36)
NIGHT = (10, 18, 32)
CREAM = (250, 248, 242)
EMBER = (224, 112, 58)
MUTED = (150, 163, 180)

F_TITLE = os.path.join(FONTS, "schibsted-grotesk-latin-700-normal.ttf")
F_HEAD = os.path.join(FONTS, "schibsted-grotesk-latin-500-normal.ttf")
F_MONO = os.path.join(FONTS, "ibm-plex-mono-latin-600-normal.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ── le film ───────────────────────────────────────────────────────────────────
# (début, fin, source, zoom_final, pan_x, plan)
#   zoom_final : 1.0 = aucun zoom ; 1.07 = le plan s'éloigne / se rapproche de 7 %
#   pan_x      : déplacement horizontal, en fraction de la marge disponible
BEATS = [
    # (début, fin, source, zoom_final, pan_x, plan, ancrage)
    (0.0, 3.4, os.path.join(SITE, "cabinet-interieur.webp"), 1.06, -0.35, "hook", (0.52, 0.50)),
    (3.4, 6.8, os.path.join(SITE, "dmoptic-mesure.webp"), 1.08, 0.30, "cle", (0.50, 0.50)),
    (6.8, 10.4, os.path.join(ETAPES, "01-anamnese.jpg"), 1.09, -0.25, "etape", (0.62, 0.48)),
    (10.4, 14.0, os.path.join(ETAPES, "02-bilan-optique.jpg"), 1.08, 0.25, "etape", (0.45, 0.50)),
    (14.0, 17.6, os.path.join(ETAPES, "03-acuites.jpg"), 1.09, 0.30, "etape", (0.50, 0.50)),
    (17.6, 21.2, os.path.join(ETAPES, "04-refraction.jpg"), 1.08, -0.20, "etape", (0.50, 0.52)),
    (21.2, 25.6, os.path.join(SITE, "cabinet-examen.webp"), 1.08, -0.30, "preuve", (0.80, 0.45)),
    (25.6, 31.0, os.path.join(SITE, "cabinet-enseigne.webp"), 1.05, 0.20, "cta", (0.50, 0.16)),
]

# Texte à l'écran — un plan = une idée. `sub` = la ligne d'appui, plus petite.
TEXTES = {
    "hook": dict(
        lines=["Ce n'est pas", "une photo floue."], place="haut", size=96,
        sub=None, mention="simulation approximative",
    ),
    "cle": dict(
        lines=["Quatre étapes.", "Aucune ne se saute."], place="bas", size=86,
        sub=None, mention=None,
    ),
    "etape": dict(place="bas", size=92, sub_size=42, mention="illustration"),
    "preuve": dict(
        lines=["C'est lui", "qui fait l'examen."], place="bas", size=88,
        sub="Laquintinie · Kumba · Bethesda", sub_size=38, mention=None,
    ),
    "cta": dict(
        lines=["Écrivez-nous", "avant de venir."], place="centre", size=100,
        sub="WhatsApp 656 122 239 · Bonabéri", sub_size=40, mention=None,
    ),
}

# Ce que chaque plan d'étape dit — dans les mots du client (§1 du document)
ETAPES_TXT = {
    2: ("1 · On écoute", "ce que vous n'arrivez plus à voir"),
    3: ("2 · On mesure", "le bilan optique"),
    4: ("3 · On lit", "les acuités, œil par œil"),
    5: ("4 · On réfracte", "la correction qui en sort"),
}


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 2


# ── masters : une fois par plan, pas par image ────────────────────────────────
_MASTERS: dict[str, Image.Image] = {}


def master(path: str) -> Image.Image:
    """Photo -> master 9:16 surdimensionné, étalonnée pour que les visuels générés
    et les vraies photos se ressemblent (même chaleur, même contraste)."""
    if path in _MASTERS:
        return _MASTERS[path]
    src = Image.open(path).convert("RGB")
    cw, ch = int(W * UP), int(H * UP)
    s = max(cw / src.width, ch / src.height)
    big = src.resize((max(int(src.width * s), cw), max(int(src.height * s), ch)), Image.LANCZOS)
    left = (big.width - cw) // 2
    top = (big.height - ch) // 2
    out = big.crop((left, top, left + cw, top + ch))

    # étalonnage commun : léger réchauffement, contraste doux, netteté
    out = ImageEnhance.Color(out).enhance(1.04)
    out = ImageEnhance.Contrast(out).enhance(1.05)
    r, g, b = out.split()
    r = r.point(lambda v: min(255, int(v * 1.02 + 2)))
    b = b.point(lambda v: max(0, int(v * 0.98)))
    out = Image.merge("RGB", (r, g, b))
    out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=45, threshold=3))
    _MASTERS[path] = out
    return out


def plan_frame(beat, t_local):
    a, b, path, zoom_final, pan_x, kind, anchor = beat
    m = master(path)
    span = b - a
    p = ease_out(t_local / span) if span > 0 else 0.0

    zoom = 1.0 + (zoom_final - 1.0) * p
    cw = int(W * UP / zoom)
    ch = int(H * UP / zoom)
    free_x = m.width - cw
    free_y = m.height - ch
    # ancrage : où se trouve le sujet dans la photo (0 = bord, 1 = bord opposé)
    ax, ay = anchor
    x0 = int(free_x * (ax + 0.5 * pan_x * p))
    y0 = int(free_y * ay)
    x0 = max(0, min(free_x, x0))
    y0 = max(0, min(free_y, y0))
    frame = m.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BICUBIC)

    # le hook : le flou se résout — c'est l'interruption (catégorie ②)
    if kind == "hook":
        k = ease_out(min(1.0, t_local / 1.7))
        radius = 17.0 * (1.0 - k)
        if radius > 0.4:
            frame = frame.filter(ImageFilter.GaussianBlur(radius))
        # la mise au point revient par vagues très légères, pas d'un coup
        if 0.9 < t_local < 1.9:
            frame = frame.filter(ImageFilter.GaussianBlur(0.6 * (1 - abs(t_local - 1.4) / 0.5)))
    return frame


# ── texte ─────────────────────────────────────────────────────────────────────
def fit(text, path, size, max_w):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = font(path, size)
    longest = max(text, key=lambda l: probe.textlength(l, font=f))
    while probe.textlength(longest, font=f) > max_w and size > 34:
        size -= 2
        f = font(path, size)
    return size


_SCRIMS: dict[str, Image.Image] = {}


def scrim(img, where, strength=232):
    """Dégradé sombre — lisible sur toutes les photos, sans bandeau plein.
    Calculé une fois, réutilisé sur toutes les images du plan."""
    if where in _SCRIMS:
        return Image.alpha_composite(img.convert("RGBA"), _SCRIMS[where]).convert("RGB")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    hgt = int(H * 0.60)
    if where == "bas":
        rng = range(H - hgt, H)
        for i, y in enumerate(rng):
            k = (i / hgt) ** 1.35
            d.line([(0, y), (W, y)], fill=NIGHT + (int(min(255, strength * 1.08) * k),))
    elif where == "haut":
        for i, y in enumerate(range(0, hgt)):
            k = (1 - i / hgt) ** 1.7
            d.line([(0, y), (W, y)], fill=NIGHT + (int(strength * k),))
    else:
        d.rectangle((0, 0, W, H), fill=NIGHT + (int(strength * 0.92),))
    _SCRIMS[where] = layer
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def reveal(t_local, start=0.0, dur=0.38):
    return ease((t_local - start) / dur)


def draw_text(frame, kind, t_local, idx):
    cfg = TEXTES[kind].copy()
    if kind == "etape":
        head, sub = ETAPES_TXT[idx]
        cfg.update(lines=[head], sub=sub)
    lines = cfg.get("lines") or []
    sub = cfg.get("sub")
    place = cfg["place"]

    frame = scrim(frame, place)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    al = int(255 * reveal(t_local))
    slide = int(18 * (1 - reveal(t_local)))

    size = fit(lines, F_TITLE, cfg["size"], W - 140)
    f = font(F_TITLE, size)
    lh = int(size * 1.12)
    block_h = lh * len(lines)
    sub_h = int(cfg.get("sub_size", 38) * 1.5) if sub else 0

    if place == "bas":
        # bas du bloc calé à 72 % de la hauteur : au-dessus de l'interface TikTok
        top = int(H * 0.68) - sub_h - block_h
    elif place == "haut":
        top = int(H * 0.17)
    else:
        top = (H - block_h - sub_h) // 2 - 40

    for i, line in enumerate(lines):
        x = 72
        d.text((x, top + i * lh + slide), line, font=f, fill=CREAM + (al,))

    if sub:
        sf = font(F_HEAD, cfg.get("sub_size", 38))
        d.text((72, top + block_h + 26 + slide), sub, font=sf, fill=CREAM + (min(255, int(al * 0.86)),))

    # filet de marque sous le bloc — rappelle la charte sans surcharger
    y_rule = top + block_h + (84 if sub else 30)
    d.rectangle((72, y_rule, 72 + 88, y_rule + 6), fill=EMBER + (min(255, int(al * 0.9)),))

    mention = cfg.get("mention")
    if mention:
        mf = font(F_MONO, 24)
        d.text((72, y_rule + 22), mention, font=mf, fill=MUTED + (int(al * 0.80),))

    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")



def cta_card(t_local):
    """Carte de fin : le vrai mot CONSULTATION, entier, en bandeau — puis la demande.
    Une photo panoramique ne tient pas debout en 9:16 ; on la pose au lieu de la rogner."""
    span = BEATS[-1][1] - BEATS[-1][0]
    p = ease_out(t_local / span)

    # fond nuit, dégradé très doux
    bg = Image.new("RGB", (W, H), NIGHT)
    grad = Image.new("L", (1, H))
    for i in range(H):
        grad.putpixel((0, i), int(30 * (i / H) ** 0.8))
    tint = Image.new("RGB", (W, H), (20, 36, 64))
    bg = Image.composite(tint, bg, grad.resize((W, H)))

    # bandeau photo : cadrage 16:9, zoom lent, le mot reste entier
    src = Image.open(os.path.join(SITE, "cabinet-enseigne.webp")).convert("RGB")
    bw, bh = int(W * 1.02), int(W * 0.52)
    z = 1.0 + 0.12 * p
    cw, chh = int(bw / z), int(bh / z)
    s_ = max(cw / src.width, chh / src.height)
    big = src.resize((max(int(src.width * s_), cw), max(int(src.height * s_), chh)), Image.LANCZOS)
    x0 = (big.width - cw) // 2
    y0 = int((big.height - chh) * 0.18)
    band = big.crop((x0, y0, x0 + cw, y0 + chh)).resize((bw, bh), Image.BICUBIC)
    band = band.filter(ImageFilter.UnsharpMask(radius=2, percent=40, threshold=3))

    bx, by = (W - bw) // 2, int(H * 0.375)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (bx + 8, by + 14, bx + bw + 8, by + bh + 14), radius=26, fill=(0, 0, 0, 150))
    bg = Image.alpha_composite(bg.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(22))).convert("RGB")
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), radius=26, fill=255)
    bg.paste(band, (bx, by), mask)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    al = int(255 * reveal(t_local, 0.08))
    slide = int(16 * (1 - reveal(t_local, 0.08)))

    f = font(F_TITLE, 96)
    d.text((72, int(H * 0.175) + slide), "Écrivez-nous", font=f, fill=CREAM + (al,))
    d.text((72, int(H * 0.175) + 108 + slide), "avant de venir.", font=f, fill=CREAM + (al,))
    d.rectangle((72, int(H * 0.175) + 232, 160, int(H * 0.175) + 238), fill=EMBER + (al,))

    f2 = font(F_HEAD, 44)
    d.text((72, by + bh + 58), "WhatsApp 656 122 239", font=f2, fill=CREAM + (al,))
    f3 = font(F_HEAD, 36)
    d.text((72, by + bh + 118), "Bonabéri, Douala · livraison possible", font=f3, fill=MUTED + (al,))
    f4 = font(F_MONO, 26)
    d.text((72, by + bh + 186), "PAIEMENT EN PLUSIEURS FOIS", font=f4, fill=EMBER + (al,))

    card = Image.alpha_composite(bg.convert("RGBA"), layer).convert("RGB")

    # le plan entier avance très lentement : aucun cadre ne reste figé
    zz = 1.0 + 0.055 * p
    cw2, ch2 = int(W / zz), int(H / zz)
    ox, oy = (W - cw2) // 2, int((H - ch2) * 0.55)
    return card.crop((ox, oy, ox + cw2, oy + ch2)).resize((W, H), Image.BICUBIC)

def draw_plate(frame, alpha):
    """Bandeau de marque, discret, présent du début à la fin."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    txt = "DM OPTIQUE · BONABÉRI"
    f = font(F_MONO, 25)
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle((72, 96, 72 + tw + 44, 96 + 54), radius=8,
                        fill=INK + (int(140 * alpha),))
    d.text((94, 110), txt, font=f, fill=CREAM + (int(225 * alpha),))
    return Image.alpha_composite(frame.convert("RGBA"), layer).convert("RGB")


def frame_at(t):
    idx = 0
    for i, b in enumerate(BEATS):
        if b[0] <= t < b[1]:
            idx = i
            break
        if t >= BEATS[-1][1]:
            idx = len(BEATS) - 1
    beat = BEATS[idx]
    tl = t - beat[0]
    if beat[5] == "cta":
        img = cta_card(tl)
    else:
        img = plan_frame(beat, tl)
        img = draw_text(img, beat[5], tl, idx)

    # dernière seconde : on renforce la marque
    alpha = 1.0
    if t > DUR - 1.0:
        alpha = 1.0
    img = draw_plate(img, alpha)
    return img


# ── rendu ─────────────────────────────────────────────────────────────────────
def preview(outdir):
    os.makedirs(outdir, exist_ok=True)
    for i, t in enumerate([0.2, 1.0, 2.5, 5.0, 8.5, 12.0, 15.5, 19.0, 23.0, 28.0, 30.5]):
        p = os.path.join(outdir, f"p{i:02d}-{t:04.1f}s.jpg")
        frame_at(t).save(p, quality=90)
        print(p)


def render(out, voice=None):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    silent = out + ".silent.mp4"
    proc = subprocess.Popen(
        [ffmpeg, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-an",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", silent],
        stdin=subprocess.PIPE,
    )
    n = int(round(DUR * FPS))
    for i in range(n):
        proc.stdin.write(frame_at(i / FPS).tobytes())
        if i % 120 == 0:
            sys.stderr.write(f"\r{i}/{n} images")
    proc.stdin.close()
    proc.wait()
    sys.stderr.write(f"\r{n}/{n} images\n")

    cuts = [b[0] for b in BEATS[1:]]
    tracks = [make_bed(DUR, cuts, out + ".bed.wav")]
    if voice:
        tracks.append(voice)

    cmd = [ffmpeg, "-y", "-v", "error", "-i", silent]
    for tr in tracks:
        cmd += ["-i", tr]
    if voice:
        fc = ("[1:a]volume=0.55[bed];"
              "[2:a]volume=1.0[vo];"
              "[bed][vo]amix=inputs=2:duration=longest:normalize=0,apad[a]")
    else:
        fc = "[1:a]volume=0.55,apad[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v:0", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
            "-t", f"{DUR:.2f}", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    os.remove(silent)
    return out



# ── voix : une phrase par plan, posée à la seconde exacte ────────────────────
# Calé sur la chronologie du texte, pas sur celle de l'image : chaque phrase est
# dite pendant que son carton est à l'écran, jamais avant ni après.
VOIX_OFFSETS = {1: 0.15, 2: 3.55, 3: 6.95, 4: 10.55, 5: 14.15, 6: 17.65, 7: 21.85, 8: 25.85}


def assemble_voice(folder, out, sr=44100, duration=DUR):
    """Assemble les 8 phrases en une seule piste, sans chevauchement."""
    import wave
    n = int(sr * duration)
    track = np.zeros(n, dtype=np.float32)
    for i, off in VOIX_OFFSETS.items():
        path = os.path.join(folder, f"{i:02d}.wav")
        if not os.path.exists(path):
            raise SystemExit(f"voix manquante : {path}")
        with wave.open(path, "rb") as w:
            frames = w.readframes(w.getnframes())
            data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        i0 = int(off * sr)
        i1 = min(n, i0 + len(data))
        track[i0:i1] += data[: i1 - i0]
    peak = float(np.abs(track).max()) or 1.0
    track *= 0.92 / peak
    pcm = (np.stack([track, track], axis=1) * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    return out

def make_bed(duration, cuts, path, sr=44100):
    """Nappe chaude et discrète — même recette que les spots précédents."""
    n = int(sr * duration)
    t = np.arange(n) / sr
    rng = np.random.default_rng(11)
    bed = np.zeros(n)
    chords = [(110.00, 130.81, 164.81), (87.31, 130.81, 174.61),
              (130.81, 164.81, 196.00), (98.00, 123.47, 146.83)]
    seg = duration / len(chords)
    for i, ch in enumerate(chords):
        env = np.clip((t - i * seg) / 1.1, 0, 1) * np.clip((i * seg + seg + 1.1 - t) / 1.4, 0, 1)
        for f0 in ch:
            for det in (-0.3, 0.3):
                bed += 0.085 * env * np.sin(2 * np.pi * (f0 + det) * t)
        bed += 0.03 * env * np.sin(2 * np.pi * ch[0] * 0.5 * t)
    for c in cuts:
        i0 = int(c * sr)
        ln = int(0.13 * sr)
        if i0 + ln >= n:
            continue
        seg_t = np.arange(ln) / sr
        noise = rng.standard_normal(ln) * np.exp(-seg_t * 28)
        noise = np.convolve(noise, np.hanning(9) / 5, mode="same") * np.linspace(1, 0, ln)
        bed[i0:i0 + ln] += 0.045 * noise
    k = 41
    bed = np.convolve(bed, np.ones(k) / k, mode="same")
    fade = int(1.0 * sr)
    bed[:fade] *= np.linspace(0, 1, fade)
    bed[-fade:] *= np.linspace(1, 0, fade)
    bed /= max(1e-6, np.abs(bed).max()) / 0.30
    import wave
    pcm = (np.stack([bed, bed], axis=1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--voice")
    ap.add_argument("--voice-dir", help="dossier des 8 phrases (01.wav … 08.wav)")
    ap.add_argument("--preview")
    a = ap.parse_args()
    if a.preview:
        preview(a.preview)
    elif a.out:
        voice = a.voice
        if a.voice_dir:
            voice = assemble_voice(a.voice_dir, a.out + ".voix.wav")
        render(a.out, voice)
        print("écrit :", a.out)
    else:
        ap.error("--out ou --preview")
