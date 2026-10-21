# -*- coding: utf-8 -*-
"""DM Optique — TikTok n°1 v2 « 20 minutes d'écran » — moteur de rendu.

1080x1920, 30 fps, 23 s, sans visage, à partir des photos réelles du dépôt.
Rendu PIL image par image -> pipe ffmpeg (imageio-ffmpeg). Aucune retouche de produit :
le fond crème uni des fiches montures est *étendu* (couleur échantillonnée aux bords),
la monture elle-même n'est jamais modifiée.

Usage :
    python3 tools/record/make_dmoptic_tiktok.py --out <fichier.mp4> [--voice <audio>]
    python3 tools/record/make_dmoptic_tiktok.py --preview <dossier>   # 6 PNG de contrôle

Le portique `tools/qa/audit_video_motion.py` doit passer (0 fenêtre figée) avant livraison.
"""
import argparse
import os
import re
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, "hosting", "previews", "dmoptic")
FONTS = os.path.join(ROOT, "clients", "dm-optic", "content", "month1", "w1", "assets", "fonts")

W, H, FPS = 1080, 1920, 30
DUR = 23.0

# --- palette du site (index.html : variables CSS) -------------------------------
BRAND = (26, 63, 134)      # --brand #1A3F86
INK = (12, 21, 36)         # --ink   #0C1524
NIGHT = (10, 18, 32)       # --night #0A1220
PAPER = (238, 241, 245)    # --paper #EEF1F5
EMBER = (224, 112, 58)     # --ember #E0703A
WA = (11, 122, 62)         # --wa    #0B7A3E
CREAM = (250, 248, 242)

F_TITLE = os.path.join(FONTS, "schibsted-grotesk-latin-700-normal.ttf")
F_HEAD = os.path.join(FONTS, "schibsted-grotesk-latin-500-normal.ttf")
F_BODY = os.path.join(FONTS, "ibm-plex-sans-latin-400-normal.ttf")
F_MONO = os.path.join(FONTS, "ibm-plex-mono-latin-600-normal.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# --- plan de montage ------------------------------------------------------------
# (début, fin, type, source, mov) ; mov = (zoom, pan_x) amplitudes sur le plan
BEATS = [
    # (début, fin, type, source, zoom, pan_x, drift_y)
    (0.0, 3.2, "interior", "cabinet-interieur.webp", 0.16, 0.55, -0.40),
    (3.2, 7.0, "product", "montures/monture-f01.webp", 0.14, 0.0, 0.45),
    (7.0, 11.5, "interior", "cabinet-hero-1080.webp", 0.16, -0.55, 0.40),
    (11.5, 15.5, "product", "montures/monture-f24.webp", 0.15, 0.35, -0.45),
    (15.5, 19.5, "product", "montures/monture-h08.webp", 0.14, -0.35, 0.45),
]

# sous-titres (identiques au .srt livré) : (début, fin, texte, taille)
SUBS = [
    (0.0, 3.2, "Vingt minutes d'écran.", 92),
    (3.2, 7.0, "Puis vingt secondes,\nà six mètres.", 84),
    (7.0, 11.5, "Vos yeux passent la journée\nà quarante centimètres.", 72),
    (11.5, 15.5, "Ce n'est pas un traitement.\nC'est une pause.", 78),
    (15.5, 19.5, "Si ça reste flou,\nce n'est plus une question de pause :\nvenez faire mesurer.", 62),
]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def sample_bg(im):
    """Couleur du fond : moyenne des 4 coins (les fiches montures ont un fond uni)."""
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    px = [im.getpixel(p) for p in pts]
    px = [p[:3] for p in px]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))


def master_interior(path, up=1.25, fx=0.5):
    """Photo paysage -> 9:16 par recadrage couvrant (aucune bande floue, aucun étirement).
    fx = ancrage horizontal du recadrage (0 = gauche, 1 = droite) : évite de couper du texte."""
    src = Image.open(path).convert("RGB")
    cw, ch = int(W * up), int(H * up)
    s = max(cw / src.width, ch / src.height)
    big = src.resize((max(int(src.width * s), cw), max(int(src.height * s), ch)), Image.LANCZOS)
    left = int((big.width - cw) * fx)
    top = (big.height - ch) // 2
    out = big.crop((left, top, left + cw, top + ch))
    return out.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=3))


def tight_crop(src, bgcol, pad=0.05):
    """Boîte englobante du produit sur fond uni — cadrage, pas retouche."""
    small = src.resize((src.width // 4, src.height // 4))
    px = small.load()
    w, h = small.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if abs(r - bgcol[0]) + abs(g - bgcol[1]) + abs(b - bgcol[2]) > 44:
                xs.append(x); ys.append(y)
    if not xs:
        return src
    x0, x1 = min(xs) * 4, (max(xs) + 1) * 4
    y0, y1 = min(ys) * 4, (max(ys) + 1) * 4
    mx = int((x1 - x0) * pad); my = int((y1 - y0) * pad)
    return src.crop((max(0, x0 - mx), max(0, y0 - my),
                     min(src.width, x1 + mx), min(src.height, y1 + my)))


def master_product(path, up=1.25):
    """Fiche monture -> carte crème sur fond nuit. Le produit n'est ni retouché ni déformé."""
    src = Image.open(path).convert("RGB")
    bgcol = sample_bg(src)
    prod = tight_crop(src, bgcol)
    cw, ch = int(W * up), int(H * up)

    canvas = Image.new("RGB", (cw, ch), NIGHT)
    # dégradé vertical très doux : le fond n'est jamais plat
    grad = Image.new("L", (1, ch))
    for i in range(ch):
        grad.putpixel((0, i), int(26 * (i / ch)))
    gm = Image.new("RGB", (cw, ch), (18, 34, 62))
    canvas = Image.composite(gm, canvas, grad.resize((cw, ch)))

    card_w = int(cw * 0.84)
    card_h = int(ch * 0.50)
    card_x = (cw - card_w) // 2
    card_y = int(ch * 0.145)

    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((card_x + 10, card_y + 18, card_x + card_w + 10, card_y + card_h + 18),
                         radius=42, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")

    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h), radius=42, fill=bgcol)

    inner_w, inner_h = int(card_w * 0.90), int(card_h * 0.86)
    sc = min(inner_w / prod.width, inner_h / prod.height)
    pw, ph = max(1, int(prod.width * sc)), max(1, int(prod.height * sc))
    prod = prod.resize((pw, ph), Image.LANCZOS)
    prod = prod.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=3))
    canvas.paste(prod, (card_x + (card_w - pw) // 2, card_y + (card_h - ph) // 2))
    return canvas


def reveal(t, start, dur=0.55):
    return ease((t - start) / dur)


def draw_band(draw, alpha):
    """Bandeau permanent en haut, très discret."""
    txt = "DM OPTIQUE · OPTICIEN OPTOMÉTRISTE · BONABÉRI"
    f = font(F_MONO, 27)
    tw = draw.textlength(txt, font=f)
    pad = 26
    x0 = (W - tw) / 2 - pad
    y0 = 74
    box = (x0, y0, x0 + tw + 2 * pad, y0 + 58)
    draw.rounded_rectangle(box, radius=10, fill=(10, 18, 32, int(150 * alpha)))
    draw.text((x0 + pad, y0 + 14), txt, font=f, fill=(250, 248, 242, int(235 * alpha)))


def fit_size(text, path, size, max_w):
    """Réduit la taille jusqu'à ce que la plus longue ligne tienne dans max_w."""
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = font(path, size)
    longest = max(text.split("\n"), key=lambda l: probe.textlength(l, font=f))
    while probe.textlength(longest, font=f) > max_w and size > 34:
        size -= 2
        f = font(path, size)
    return size


def draw_sub(img, text, size, prog):
    """Bandeau bas plein cadre : lisible sur toutes les photos, cohérent avec la marque."""
    prog = ease(prog)
    size = fit_size(text, F_TITLE, size, W - 150)
    f = font(F_TITLE, size)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = text.split("\n")
    lh = int(size * 1.16)
    block_h = lh * len(lines)
    top = int(H * 0.702)
    pad_top, pad_bot = 54, 40
    bar_h = block_h + pad_top + pad_bot

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # glissement d'entrée du bandeau (12 px) — mouvement, jamais de cadre figé
    off = int(14 * (1 - prog))
    a_bar = int(232 * min(1.0, prog * 1.4))
    d.rectangle((0, top + off, W, top + off + bar_h), fill=NIGHT + (a_bar,))
    # filet accent en haut du bandeau, qui grandit
    half = int(W * 0.11 * prog)
    d.rectangle((W // 2 - half, top + off, W // 2 + half, top + off + 7), fill=EMBER + (255,))

    a = int(255 * min(1.0, prog * 1.5))
    y = top + off + pad_top
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=f)
        d.text(((W - tw) / 2, y + i * lh), line, font=f, fill=(255, 255, 255, a))
    return Image.alpha_composite(img.convert("RGBA"), layer)


def end_card(t, t0, t1, K=1.0):
    """Carton final : bleu de marque, logo, horaires, WhatsApp. Mouvement continu."""
    p = (t - t0) / max(0.001, (t1 - t0))
    CW, CH = int(W * K), int(H * K)
    img = Image.new("RGB", (CW, CH), NIGHT)
    d = ImageDraw.Draw(img)
    # halo bleu qui respire lentement (évite toute fenêtre figée)
    cx, cy = CW // 2, int(CH * 0.34)
    r = int(560 * K + 30 * K * p)
    halo = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    for i in range(8, 0, -1):
        rr = int(r * i / 8)
        hd.ellipse((cx - rr, cy - rr, cx + rr, cy + rr),
                   fill=BRAND + (int(9 * (9 - i)),))
    halo = halo.filter(ImageFilter.GaussianBlur(30))
    img = Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB")
    d = ImageDraw.Draw(img)

    # logo, très lent zoom
    logo = Image.open(os.path.join(SITE, "dm-logo.webp")).convert("RGBA")
    lw = int(238 * K * (1 + 0.05 * p))
    logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    img.paste(logo, ((CW - logo.width) // 2, int(CH * 0.235)), logo)
    d = ImageDraw.Draw(img)

    a = ease(min(1.0, (t - t0) / 0.6))
    y = int(CH * 0.455)
    f1 = font(F_HEAD, int(46 * K))
    d.text(((CW - d.textlength("EXAMEN DE VUE", font=f1)) / 2, y), "EXAMEN DE VUE",
           font=f1, fill=PAPER + (int(255 * a),))
    f2 = font(F_TITLE, int(104 * K))
    txt2 = "8h30–13h00"
    d.text(((CW - d.textlength(txt2, font=f2)) / 2, y + int(70 * K)), txt2,
           font=f2, fill=(255, 255, 255, int(255 * a)))
    f3 = font(F_BODY, int(44 * K))
    txt3 = "du lundi au samedi"
    d.text(((CW - d.textlength(txt3, font=f3)) / 2, y + int(196 * K)), txt3,
           font=f3, fill=PAPER + (int(210 * a),))

    # pastille WhatsApp
    a2 = ease(min(1.0, (t - t0 - 0.35) / 0.6))
    py = int(CH * 0.735) + int(14 * K * (1 - a2))
    fw = font(F_TITLE, int(62 * K))
    wtxt = "WhatsApp 656 122 239"
    tw = d.textlength(wtxt, font=fw)
    padx, pady = int(46 * K), int(30 * K)
    d.rounded_rectangle(((CW - tw) / 2 - padx, py, (CW + tw) / 2 + padx, py + int(62 * K) + 2 * pady),
                        radius=int(18 * K), fill=WA + (int(255 * a2),))
    d.text(((CW - tw) / 2, py + pady), wtxt, font=fw, fill=(255, 255, 255, int(255 * a2)))

    f4 = font(F_BODY, int(38 * K))
    txt4 = "Ndobo Mayor · Immeuble West Hotel, 1er étage"
    d.text(((CW - d.textlength(txt4, font=f4)) / 2, int(CH * 0.885)), txt4,
           font=f4, fill=(190, 200, 216, int(230 * a2)))
    return img


def crop_window(big, p, zoom, pan, drift):
    """Fenêtre 1080x1920 qui se déplace dans un master plus grand (mouvement garanti)."""
    z = max(0.0, zoom) * p
    s = 1.0 + z
    cw = int(big.width / s)
    ch = int(big.height / s)
    cw, ch = min(cw, big.width), min(ch, big.height)
    ax, ay = big.width - cw, big.height - ch
    x0 = int(ax * (0.5 + pan * 0.5 * (2 * p - 1)))
    y0 = int(ay * (0.5 + drift * 0.5 * (2 * p - 1)))
    x0 = max(0, min(ax, x0))
    y0 = max(0, min(ay, y0))
    return big.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)


def frame(i):
    t = i / FPS
    if t >= 19.5:
        p = (t - 19.5) / (DUR - 19.5)
        big = end_card(t, 19.5, DUR, K=1.22)
        img = crop_window(big, p, 0.18, 0.0, 0.55)
    else:
        for (b0, b1, kind, src, zoom, pan, drift) in BEATS:
            if b0 <= t < b1:
                p = (t - b0) / (b1 - b0)
                img = crop_window(MASTERS[src], p, zoom, pan, drift)
                break
        else:
            img = Image.new("RGB", (W, H), NIGHT)

    img = img.convert("RGBA")
    for (s0, s1, text, size) in SUBS:
        if s0 <= t < s1:
            img = draw_sub(img, text, size, reveal(t, s0))
            break
    d = ImageDraw.Draw(img)
    draw_band(d, ease(min(1.0, t / 0.5)))
    return img.convert("RGB")


MASTERS = {}
# ancrage du recadrage 9:16 des photos du cabinet (0 = gauche) — évite de couper le poster
FOCUS = {"cabinet-interieur.webp": 0.30, "cabinet-hero-1080.webp": 0.34}


def probe_duration(ffmpeg, path):
    out = subprocess.run([ffmpeg, "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    if not m:
        return 0.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def make_cover():
    """Couverture 1080x1920 : accroche dans le carré central (grille de profil)."""
    img = crop_window(MASTERS["montures/monture-f24.webp"], 0.0, 0.0, 0.0, 0.0).convert("RGBA")
    d = ImageDraw.Draw(img)

    f_top = font(F_MONO, 30)
    t1 = "DM OPTIQUE · BONABÉRI"
    d.text(((W - d.textlength(t1, font=f_top)) / 2, 150), t1, font=f_top, fill=(214, 224, 240, 235))

    y = int(H * 0.675)
    for line, size, gap in (("Vingt minutes", 104, 118), ("d'écran.", 104, 118),
                            ("Puis vingt secondes,", 62, 84), ("à six mètres.", 62, 96)):
        f = font(F_TITLE, size)
        d.text(((W - d.textlength(line, font=f)) / 2, y), line, font=f, fill=(255, 255, 255, 255))
        y += gap

    half = int(W * 0.115)
    d.rectangle((W // 2 - half, y + 4, W // 2 + half, y + 11), fill=EMBER)

    f_bot = font(F_BODY, 34)
    t2 = "Opticien optométriste · WhatsApp 656 122 239"
    d.text(((W - d.textlength(t2, font=f_bot)) / 2, int(H * 0.935)), t2, font=f_bot,
           fill=(186, 198, 218, 230))
    return img.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "clients", "dm-optic", "content",
                                                 "month1", "w1", "tiktok-01-v2.mp4"))
    ap.add_argument("--voice", default=None, help="fichier audio à coller sur la vidéo")
    ap.add_argument("--preview", default=None, help="dossier où écrire 6 PNG de contrôle")
    ap.add_argument("--cover", default=None, help="chemin d'une couverture 1080x1920 (JPG)")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=DUR)
    args = ap.parse_args()

    for (_, _, kind, src, _, _, _) in BEATS:
        path = os.path.join(SITE, src)
        fx = FOCUS.get(src, 0.5)
        MASTERS[src] = master_interior(path, fx=fx) if kind == "interior" else master_product(path)

    if args.cover:
        make_cover().save(args.cover, quality=92, optimize=True)
        print("cover ->", args.cover)
        return 0

    if args.preview:
        os.makedirs(args.preview, exist_ok=True)
        for t in (1.2, 4.5, 9.0, 13.0, 17.0, 21.0):
            frame(int(t * FPS)).save(os.path.join(args.preview, "frame-%05.1fs.png" % t))
        print("preview ->", args.preview)
        return 0

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = args.out + ".silent.mp4"
    cmd = [ffmpeg, "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "pipe:0",
           "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n0, n1 = int(args.start * FPS), int(args.end * FPS)
    for i in range(n0, n1):
        proc.stdin.write(frame(i).tobytes())
        if i % 60 == 0:
            sys.stderr.write("\r%d/%d" % (i - n0, n1 - n0))
    proc.stdin.close()
    proc.wait()
    sys.stderr.write("\n")

    if args.voice:
        # la voix est calée sur la durée du montage : léger ralentissement (<=10 %,
        # inaudible) puis silence de fin. Jamais "-shortest" : il couperait le carton final
        # qui porte le numéro WhatsApp.
        dur_voice = probe_duration(ffmpeg, args.voice)
        tempo = max(0.85, min(1.0, (DUR - 0.6) / max(0.1, dur_voice)))
        cmd2 = [ffmpeg, "-y", "-v", "error", "-i", tmp, "-i", args.voice,
                "-filter_complex", "[1:a]atempo=%.4f,apad[a]" % tempo,
                "-map", "0:v:0", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-t", "%.2f" % DUR,
                "-movflags", "+faststart", args.out]
        subprocess.run(cmd2, check=True)
        os.remove(tmp)
    else:
        os.replace(tmp, args.out)
    print("ok ->", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
