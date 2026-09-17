#!/usr/bin/env python3
"""AMK — montage d'un clip vertical à partir d'une capture réelle.

Assemble : carte HOOK → **capture réelle en mouvement** (frames du `capture.mjs`) →
carte PAYOFF → carte CTA « PREVIEW ». Optionnel : narration (--audio) synchronisée
sur la durée totale.

Pourquoi : nos vidéos étaient des diaporamas (content/lessons/CONTENT-LESSONS.md §13).
Ici la partie centrale est du **mouvement réel capturé**, et le portique
`tools/qa/audit_video_motion.py` doit dire OK avant toute livraison.

Usage :
    python3 tools/video/compose.py --frames /tmp/cap/frames --out /tmp/clip.mp4 --lang fr \
        --eyebrow "3 fuites mobiles" --hook "Votre site perd des clients|AVANT WHATSAPP ?" \
        --payoff "LE CONTACT DOIT ÊTRE FACILE." --label "MboaCare · démonstration fictive"

    python3 tools/video/compose.py ... --audio narration.mp3     # narration optionnelle
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = ROOT / "content/assets/fonts"
W, H, FPS = 1080, 1920, 30

NAVY = (16, 24, 56)
NAVY_D = (10, 16, 40)
TEAL = (35, 196, 177)
AMBER = (255, 176, 32)
WHITE = (255, 255, 255)
CREAM = (250, 249, 245)

F_BOLD = str(FONT_DIR / "Montserrat-Bold.ttf")
F_SEMI = str(FONT_DIR / "Montserrat-SemiBold.ttf")
F_MED = str(FONT_DIR / "Montserrat-Medium.ttf")
_cache = {}


def fnt(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _ease_out(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


def _sheen(img, box, t, period=1.6, alpha=42):
    """Bande claire qui traverse la zone — mouvement continu, visible, jamais un zoom."""
    x0, y0, x1, y1 = box
    phase = (t % period) / period
    cx = x0 - (x1 - x0) * 0.4 + phase * (x1 - x0) * 1.8
    bw = (x1 - x0) * 0.22
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps):
        f = i / steps
        x = cx - bw / 2 + f * bw
        a = int(alpha * (1 - abs(f - 0.5) * 2))
        if a > 0 and x0 - bw < x < x1 + bw:
            d.rectangle([x, y0, x + bw / steps + 1, y1], fill=(255, 255, 255, a))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def _moving_background(img, t, tint=(255, 255, 255), alpha=12, spacing=190, tilt=140, speed=46):
    """Bandes diagonales en dérive + balayage large : mouvement continu de grande surface.
    C'est ce qui fait passer une carte longue au portique (une apparition ne suffit pas)."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    offset = int((t * speed) % spacing)
    for k in range(-2, int(img.width / spacing) + 4):
        x = k * spacing + offset
        dl.polygon([(x, 0), (x + 46, 0), (x + 46 + tilt, img.height), (x + tilt, img.height)],
                   fill=tint + (alpha,))
    img = Image.alpha_composite(img.convert("RGBA"), lay)
    return _sheen(img.convert("RGB"), (0, 0, img.width, img.height), t, period=1.9, alpha=22)


def render_hook(t, dur, eyebrow, hook_lines):
    """Carte d'ouverture ANIMÉE : eyebrow, titre blanc qui monte, **dernière ligne dans le
    bloc ambre**, barre de progression continue + reflet qui balaie le bloc."""
    img = _moving_background(Image.new("RGB", (W, H), NAVY), t)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=TEAL)

    p = _ease_out(t / 0.35)
    if p > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((90, 330 + int(24 * (1 - p))), eyebrow.upper(),
                                 font=fnt(F_SEMI, 40), fill=TEAL + (int(255 * p),))
        img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
        d = ImageDraw.Draw(img)

    title_lines = hook_lines[:-1] if len(hook_lines) > 1 else hook_lines
    amber_line = hook_lines[-1] if len(hook_lines) > 1 else ""

    p = _ease_out((t - 0.15) / 0.6)
    y = 430
    f_h = fnt(F_BOLD, 104)
    for line in title_lines:
        for sub in wrap(d, line, f_h, W - 190):
            if p > 0:
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((90, y + int(40 * (1 - p))), sub, font=f_h, fill=WHITE + (int(255 * p),))
                img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
                d = ImageDraw.Draw(img)
            y += 118
    y += 26

    # bloc ambre : s'ouvre, puis reçoit sa ligne en sombre
    p = _ease_out((t - 0.5) / 0.6)
    if p > 0 and amber_line:
        f_a = fnt(F_BOLD, 78)
        # retour à la ligne, puis on prend TOUTES les lignes (une ligne unique tronquait le texte)
        sub_lines = wrap(d, amber_line.upper(), f_a, W - 300)
        bw = max((d.textlength(l, font=f_a) for l in sub_lines), default=0)
        box_w = min(W - 120, bw + 150)
        box_h = 96 * len(sub_lines) + 84
        x0 = 90
        x1 = x0 + int(box_w * p)
        d.rectangle([x0, y - 10, x1, y - 10 + box_h], fill=AMBER)
        if p >= 0.6:
            q = _ease_out((t - 0.75) / 0.45)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dl2 = ImageDraw.Draw(lay)
            for i, l in enumerate(sub_lines):
                dl2.text((x0 + 60, y + 24 + i * 96), l, font=f_a, fill=NAVY_D + (int(255 * q),))
            img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
            d = ImageDraw.Draw(img)
        if p >= 0.98:
            img = _sheen(img, (x0, y - 10, x0 + box_w, y - 10 + box_h), t, alpha=52)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 16, int(W * min(1.0, t / dur)), H], fill=TEAL)
    return img


def render_payoff(t, dur, text):
    """Carte de payoff ANIMÉE : fond en dérive, bande qui entre, texte qui suit, reflet continu."""
    img = _moving_background(Image.new("RGB", (W, H), NAVY), t)
    d = ImageDraw.Draw(img)
    p = _ease_out(t / 0.45)
    f = fnt(F_BOLD, 96)
    lines = wrap(d, text, f, W - 200)
    block_h = len(lines) * 116
    y0 = (H - block_h) // 2 - 40
    x_off = int(-(W + 400) * (1 - p))
    d.rectangle([60 + x_off, y0 - 70, W - 60 + x_off, y0 + block_h + 40], fill=AMBER)
    q = _ease_out((t - 0.25) / 0.45)
    if q > 0:
        yy = y0
        for line in lines:
            wpx = d.textlength(line, font=f)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).text(((W - wpx) / 2, yy), line, font=f, fill=NAVY_D + (int(255 * q),))
            img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
            d = ImageDraw.Draw(img)
            yy += 116
    if p >= 0.98:
        img = _sheen(img, (60, y0 - 70, W - 60, y0 + block_h + 40), t, period=1.4, alpha=54)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 16, int(W * min(1.0, t / dur)), H], fill=AMBER)
    return img


def render_cta(t, dur, question, keyword="PREVIEW"):
    """Carte CTA ANIMÉE : fond en dérive (bandes diagonales), balayage large, pastille
    qui respire, points qui défilent, barre de progression — aucune seconde figée."""
    img = Image.new("RGB", (W, H), NAVY_D)

    # 1 · bandes diagonales en dérive lente (grande surface, faible contraste)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    spacing, tilt = 190, 140
    offset = int((t * 46) % spacing)
    for k in range(-2, int(W / spacing) + 4):
        x = k * spacing + offset
        dl.polygon([(x, 0), (x + 46, 0), (x + 46 + tilt, H), (x + tilt, H)], fill=(255, 255, 255, 12))
    img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")

    # 2 · balayage large sur toute la carte
    img = _sheen(img, (0, 0, W, H), t, period=1.7, alpha=26)

    d = ImageDraw.Draw(img)
    f_q = fnt(F_MED, 54)
    y = 470
    for line in wrap(d, question, f_q, W - 200):
        wpx = d.textlength(line, font=f_q)
        d.text(((W - wpx) / 2, y), line, font=f_q, fill=CREAM)
        y += 74
    y += 60

    # 3 · pastille : position + contour qui respirent (mouvement visible, pas un zoom)
    f_k = fnt(F_BOLD, 78)
    label = f'DM « {keyword} »'
    wpx = d.textlength(label, font=f_k)
    pad = 46
    breathe = 0.5 + 0.5 * abs(((t * 1.4) % 2) - 1)
    glow = tuple(int(TEAL[i] * (0.5 + 0.5 * breathe)) for i in range(3))
    slide = int(14 * (2 * breathe - 1))
    x0 = (W - wpx) / 2 - pad + slide
    x1 = (W + wpx) / 2 + pad + slide
    d.rounded_rectangle([x0, y, x1, y + 150], radius=75, outline=glow, width=8)
    d.text((x0 + pad, y + 34), label, font=f_k, fill=TEAL)
    y += 250

    f_s = fnt(F_MED, 40)
    for line in ["Aperçu gratuit d'une page d'accueil", "amk-cm.vercel.app"]:
        wpx = d.textlength(line, font=f_s)
        d.text(((W - wpx) / 2, y), line, font=f_s, fill=(190, 200, 220))
        y += 60

    # 4 · points qui défilent (plus gros qu'avant)
    dot_y = y + 34
    for i in range(3):
        phase = ((t * 1.1) - i * 0.16) % 1.0
        r = 14 + int(16 * max(0.0, 1 - abs(phase - 0.5) * 2))
        cx = W / 2 + (i - 1) * 78
        d.ellipse([cx - r, dot_y - r, cx + r, dot_y + r], fill=TEAL)
    d.rectangle([0, H - 16, int(W * min(1.0, t / dur)), H], fill=TEAL)
    return img


def label_bar(img, text):
    """Étiquette de fiction — obligatoire sur toute capture d'écran (règle de contenu)."""
    if not text:
        return img
    d = ImageDraw.Draw(img, "RGBA")
    f = fnt(F_SEMI, 28)
    wpx = d.textlength(text, font=f)
    pad = 24
    # étiquette en BAS de cadre : ne masque jamais l'en-tête de la page capturée
    x, y = (img.width - wpx) / 2 - pad, img.height - 130
    d.rounded_rectangle([x, y, x + wpx + 2 * pad, y + 64], radius=32,
                        fill=(16, 24, 56, 225))
    d.text((x + pad, y + 17), text, font=f, fill=(255, 255, 255))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True, action="append", help="dossier d'images (répétable : A puis B)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="fr", choices=["fr", "en"])
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--hook", required=True, help="lignes séparées par | (2e ligne = bloc ambre)")
    ap.add_argument("--payoff", default="")
    ap.add_argument("--cta", default="")
    ap.add_argument("--keyword", default="PREVIEW")
    ap.add_argument("--label", default="DÉMONSTRATION FICTIVE")
    ap.add_argument("--audio", default="")
    ap.add_argument("--hold-hook", type=float, default=2.3)
    ap.add_argument("--hold-payoff", type=float, default=2.1)
    ap.add_argument("--hold-cta", type=float, default=3.2)
    ap.add_argument("--fps", type=int, default=FPS)
    a = ap.parse_args()

    frames = []
    for d in a.frames:
        part = sorted(Path(d).glob("*.jpg"))
        if len(part) < 5:
            sys.exit(f"✗ pas assez d'images dans {d} (lancer capture.mjs d'abord)")
        frames += part

    hook_parts = a.hook.split("|")
    eyebrow = a.eyebrow or ("3 fuites mobiles" if a.lang == "fr" else "3 mobile leaks")
    cta_q = a.cta or ("Votre site perd des clients avant WhatsApp ?"
                      if a.lang == "fr" else "Losing customers before WhatsApp?")

    n_hook = int(a.hold_hook * a.fps)
    n_pay = int(a.hold_payoff * a.fps) if a.payoff else 0
    n_cta = int(a.hold_cta * a.fps)
    total = n_hook + len(frames) + n_pay + n_cta
    dur = total / a.fps

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-"]
    if a.audio and Path(a.audio).exists():
        cmd += ["-i", a.audio, "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "19",
            "-r", str(a.fps), "-movflags", "+faststart", a.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def emit(img):
        proc.stdin.write(img.convert("RGB").tobytes())

    hd, pd, cd = n_hook / a.fps, n_pay / a.fps, n_cta / a.fps
    for i in range(n_hook):
        emit(render_hook(i / a.fps, hd, eyebrow, hook_parts))
    for p in frames:
        emit(label_bar(Image.open(p).convert("RGB"), a.label))
    if a.payoff:
        for i in range(n_pay):
            emit(render_payoff(i / a.fps, pd, a.payoff))
    for i in range(n_cta):
        emit(render_cta(i / a.fps, cd, cta_q, a.keyword))
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        sys.exit(f"✗ ffmpeg a échoué (rc={rc})")
    size = os.path.getsize(a.out) / 1e6
    print(f"✓ {a.out}  ·  {dur:.1f} s  ·  {total} images  ·  {size:.2f} Mo  "
          f"(hook {a.hold_hook}s + capture {len(frames)/a.fps:.1f}s + payoff {a.hold_payoff}s + CTA {a.hold_cta}s)")


if __name__ == "__main__":
    main()
