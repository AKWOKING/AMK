"""reelkit — moteur de reels explainer AMK (format vertical 1080x1920).

Un seul fichier, aucune dépendance graphique lourde : PIL + un ffmpeg quelconque
(`imageio-ffmpeg` en fournit un binaire, voir `content/reels/README.md`).

Le style est celui du brief King du 25/10 (captures du 24/10) : fond crème, trame de
points, grands titres Montserrat, cartes type post-it punaisées, pastille de légende
bicolore en bas à droite, mascotte qui désigne, barre de progression fine.

Tout est dessiné à la volée : pas de fichiers intermédiaires, pas de captures. Les frames
partent directement dans le pipe ffmpeg — un reel de 25 s se rend en une vingtaine de
secondes.

    from reelkit import Kit, ease, PALETTE
    kit = Kit(mascot="assets/mascot.png")
    kit.scene(3.0, title_scene("..."))
    kit.render("out.mp4")
"""

from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30

FONTS = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
)

PALETTE = {
    "cream": (245, 237, 225),
    "cream_light": (255, 248, 238),
    "dot": (228, 216, 200),
    "ink": (25, 21, 18),
    "ink_soft": (60, 52, 46),
    "orange": (196, 68, 27),
    "orange_soft": (251, 227, 217),
    "green": (46, 107, 79),
    "green_soft": (223, 237, 228),
    "blue_soft": (223, 234, 243),
    "sand": (232, 219, 200),
    "white": (255, 255, 255),
    "shadow": (0, 0, 0, 26),
}

_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

# Les quatre fichiers Montserrat-Bold/SemiBold/ExtraBold/Medium du dépôt sont **le même
# fichier variable** (Montserrat-VF, 744 936 octets chacun) : sans `set_variation_by_name`,
# PIL rend l'instance par défaut, c'est-à-dire **Thin**. Tout texte « gras » sortait donc
# maigre. On demande l'axe explicitement, et on retombe sur l'instance statique si le
# fichier n'est pas variable (Poppins, lui, l'est vraiment).
_WEIGHT = {
    "Thin": b"Thin", "ExtraLight": b"ExtraLight", "Light": b"Light",
    "Regular": b"Regular", "Medium": b"Medium", "SemiBold": b"SemiBold",
    "Bold": b"Bold", "ExtraBold": b"ExtraBold", "Black": b"Black",
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    key = (name, size)
    if key not in _font_cache:
        path = os.path.join(FONTS, name)
        if not os.path.exists(path):
            # nom sans fichier correspondant (ex. Montserrat-Black) : on prend le VF
            path = os.path.join(FONTS, "Montserrat-VF.ttf")
        fnt = ImageFont.truetype(path, size)
        wanted = name.split("-")[1].split(".")[0] if "-" in name else ""
        variation = _WEIGHT.get(wanted) or _WEIGHT.get("Regular")
        try:
            fnt.set_variation_by_name(variation)
        except Exception:
            pass  # police statique : son instance est déjà la bonne
        _font_cache[key] = fnt
    return _font_cache[key]


def ease(t: float) -> float:
    """ease-out cubic — l'entrée des éléments, jamais linéaire."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


# ─────────────────────────────────────────────────────────────── primitives ──


def draw_text(
    d: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill,
    anchor: str = "la",
    spacing: int = 8,
):
    """Texte multi-lignes (séparateur \\n) avec interligne réglable."""
    x, y = xy
    line_h = fnt.size + spacing
    for i, line in enumerate(text.split("\n")):
        d.text((x, y + i * line_h), line, font=fnt, fill=fill, anchor=anchor)


def text_width(fnt: ImageFont.FreeTypeFont, text: str) -> int:
    return int(fnt.getlength(text))


def dot_grid(d: ImageDraw.ImageDraw, step: int = 48, radius: int = 2, color=None):
    color = color or PALETTE["dot"]
    for y in range(0, H, step):
        for x in range(0, W, step):
            d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def rounded_card(img: Image.Image, box, fill, radius=10, shadow=8, pin=None):
    """Carte post-it : ombre portée + rectangle arrondi + punaise optionnelle."""
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = box
    if shadow:
        d.rounded_rectangle(
            (x0 + shadow, y0 + shadow, x1 + shadow, y1 + shadow),
            radius=radius,
            fill=PALETTE["shadow"],
        )
    d.rounded_rectangle(box, radius=radius, fill=fill)
    if pin:
        cx = (x0 + x1) // 2
        d.ellipse((cx - 9, y0 - 7, cx + 9, y0 + 11), fill=pin)
    return d


def pill(
    img: Image.Image,
    center: tuple[int, int],
    runs: list[tuple[str, tuple[int, int, int]]],
    fnt_name: str = "Montserrat-Bold.ttf",
    size: int = 58,
    pad: tuple[int, int] = (38, 26),
    bg=PALETTE["ink"],
    radius: int = 18,
) -> tuple[int, int]:
    """Pastille de légende bicolore — le marqueur de style de la référence."""
    fnt = font(fnt_name, size)
    d = ImageDraw.Draw(img, "RGBA")
    widths = [text_width(fnt, t) for t, _ in runs]
    total = sum(widths) + pad[0] * 2
    h = size + pad[1] * 2
    cx, cy = center
    box = (cx - total // 2, cy - h // 2, cx + total // 2, cy + h // 2)
    d.rounded_rectangle(
        (box[0] + 10, box[1] + 12, box[2] + 10, box[3] + 12), radius=radius, fill=(0, 0, 0, 40)
    )
    d.rounded_rectangle(box, radius=radius, fill=bg)
    x = box[0] + pad[0]
    for (text, color), w in zip(runs, widths):
        d.text((x, cy), text, font=fnt, fill=color, anchor="lm")
        x += w
    return box[2], box[3]


def progress_bar(img: Image.Image, p: float, y: int = 1742, color=None):
    d = ImageDraw.Draw(img, "RGBA")
    color = color or PALETTE["orange"]
    d.rectangle((60, y, W - 60, y + 4), fill=(60, 40, 30, 40))
    d.rectangle((60, y, 60 + int((W - 120) * clamp01(p)), y + 4), fill=color)


def cut_background(img: Image.Image, tol: int = 26) -> Image.Image:
    """Retire le fond uni d'une illustration générée (crème) par diffusion depuis les bords.

    Une découpe par couleur globale mangerait le visage ; une diffusion depuis les quatre
    coins ne mange que l'extérieur, et s'arrête sur les traits noirs du dessin.
    """
    from collections import deque

    img = img.copy()
    px = img.load()
    w, h = img.size
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    base = tuple(sum(c[i] for c in corners) // len(corners) for i in range(3))

    def near(c):
        return all(abs(c[i] - base[i]) <= tol for i in range(3))

    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        q.extend([(0, y), (w - 1, y)])
    while q:
        x, y = q.popleft()
        if not (0 <= x < w and 0 <= y < h):
            continue
        idx = y * w + x
        if seen[idx]:
            continue
        c = px[x, y]
        if not near(c):
            continue
        seen[idx] = 1
        px[x, y] = (c[0], c[1], c[2], 0)
        q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return img


# ─────────────────────────────────────────────────────────────────── mascotte ──


class Mascot:
    """La mascotte AMK. Trois poses tenues par une seule image : immobile, inclinée,
    et bureau (elle « pointe » du doigt — c'est le placement bas-gauche de la référence)."""

    def __init__(self, path: str | None, height: int = 620, tol: int = 26):
        self.source = None
        self._cache: dict[int, Image.Image] = {}
        if path and os.path.exists(path):
            src = Image.open(path).convert("RGBA")
            src = cut_background(src, tol=tol)
            self.source = src.crop(src.getbbox())
        self.img = self._sized(height)

    def _sized(self, height: int) -> Image.Image | None:
        if self.source is None:
            return None
        if height not in self._cache:
            ratio = height / self.source.height
            self._cache[height] = self.source.resize(
                (int(self.source.width * ratio), height), Image.LANCZOS
            )
        return self._cache[height]

    def draw(self, img, x, y, t, talking: float = 0.0, height: int | None = None):
        pose = self._sized(height) if height else self.img
        if pose is None:
            return
        bob = math.sin(t * 2.2) * 6
        if talking > 0:
            # micro-inclinaison : la mascotte « parle » sans changer de dessin
            angle = math.sin(t * 6.0) * 1.4 * talking
            pose = pose.rotate(angle, resample=Image.BICUBIC, expand=False)
        img.paste(pose, (int(x), int(y + bob)), pose)


# ───────────────────────────────────────────────────────────────────── scènes ──
#
# Une scène = une durée + une fonction (kit, img, draw, t_local, t_global) -> None.
# `t_local` va de 0 à la durée ; `kit.progress` donne l'avancement global.


@dataclass
class Kit:
    mascot: Mascot | None = None
    scenes: list[tuple[float, Callable]] = field(default_factory=list)

    def scene(self, duration: float, fn: Callable):
        self.scenes.append((duration, fn))
        return self

    # ── fond commun ──
    def _base(self) -> Image.Image:
        img = Image.new("RGB", (W, H), PALETTE["cream"])
        d = ImageDraw.Draw(img, "RGBA")
        dot_grid(d)
        return img

    def total(self) -> float:
        return sum(d for d, _ in self.scenes)

    def frame(self, global_t: float) -> Image.Image:
        elapsed = 0.0
        scene_fn = self.scenes[-1][1]
        local = 0.0
        for dur, fn in self.scenes:
            if global_t < elapsed + dur:
                scene_fn, local = fn, global_t - elapsed
                break
            elapsed += dur
        img = self._base()
        d = ImageDraw.Draw(img, "RGBA")
        scene_fn(self, img, d, local)
        progress_bar(img, global_t / self.total())
        return img

    def render(self, out: str, codec_args: list[str] | None = None) -> str:
        ffmpeg = find_ffmpeg()
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        total_frames = int(round(self.total() * FPS))
        args = [
            ffmpeg, "-y", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        ]
        args += codec_args or []
        proc = subprocess.Popen(args + [out], stdin=subprocess.PIPE)
        assert proc.stdin
        for i in range(total_frames):
            proc.stdin.write(self.frame(i / FPS).tobytes())
        proc.stdin.close()
        if proc.wait() != 0:
            raise RuntimeError("ffmpeg a échoué")
        return out

    def still(self, at: float, out: str, scale: float = 0.5) -> str:
        img = self.frame(at)
        if scale != 1.0:
            img = img.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
        img.save(out)
        return out


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit(
            "ffmpeg introuvable. `pip install imageio-ffmpeg` (aucun apt requis) "
            "ou exporter FFMPEG=/chemin/vers/ffmpeg."
        )
