# -*- coding: utf-8 -*-
"""Resize/compress MITOC concept photos for embedding. One-time art pipeline."""
from PIL import Image
import pathlib

RAW = pathlib.Path(__file__).resolve().parent / "raw"
OUT = pathlib.Path(__file__).resolve().parent

# (source, target, box (w,h), quality, center-crop focal x/y)
JOBS = [
    ("mit-hero.jpg",    "mit-hero.jpg",   (760, 950), 70, (0.55, 0.32)),
    ("mit-exam.jpg",    "mit-exam.jpg",   (760, 570), 70, (0.55, 0.45)),
    ("mit-wall.jpg",    "mit-wall.jpg",  (1200, 760), 68, (0.5, 0.55)),
    ("mit-craft.jpg",   "mit-craft.jpg",  (760, 570), 70, (0.62, 0.5)),
    ("mit-fit.jpg",     "mit-fit.jpg",    (820, 615), 70, (0.5, 0.42)),
    ("mit-flatlay.jpg", "mit-flatlay.jpg",(560, 700), 70, (0.5, 0.5)),
    ("mit-f1.jpg",      "mit-f1.jpg",     (520, 520), 72, (0.5, 0.52)),
    ("mit-f2.jpg",      "mit-f2.jpg",     (520, 520), 72, (0.5, 0.5)),
    ("mit-f3.jpg",      "mit-f3.jpg",     (520, 520), 72, (0.5, 0.5)),
]

def crop_to(im, box, focal):
    tw, th = box
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = round(w * scale), round(h * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focal
    left = int(round(min(max((fx * nw) - tw / 2, 0), nw - tw)))
    top = int(round(min(max((fy * nh) - th / 2, 0), nh - th)))
    return im.crop((left, top, left + tw, top + th))

total = 0
for src, dst, box, q, focal in JOBS:
    im = Image.open(RAW / src).convert("RGB")
    im = crop_to(im, box, focal)
    p = OUT / dst
    im.save(p, "JPEG", quality=q, optimize=True, progressive=True)
    kb = p.stat().st_size // 1024
    total += kb
    print(f"{dst:16s} {box[0]}x{box[1]:4d}  {kb} KB")
print("total", total, "KB")
