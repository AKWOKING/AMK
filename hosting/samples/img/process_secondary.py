# -*- coding: utf-8 -*-
"""Resize/compress Cameroon secondary-school concept photos."""
from PIL import Image
import pathlib

RAW = pathlib.Path(__file__).resolve().parent / "raw"
OUT = pathlib.Path(__file__).resolve().parent

JOBS = [
    ("sec-hero.jpg",   "sec-hero.jpg",   (760, 950),  70, (0.62, 0.30)),
    ("sec-class.jpg",  "sec-class.jpg", (1200, 760),  68, (0.55, 0.5)),
    ("sec-lab.jpg",    "sec-lab.jpg",    (720, 540),  70, (0.5, 0.45)),
    ("sec-dorm.jpg",   "sec-dorm.jpg",   (780, 585),  70, (0.5, 0.5)),
    ("sec-sports.jpg", "sec-sports.jpg", (720, 540),  70, (0.55, 0.45)),
    ("sec-awards.jpg", "sec-awards.jpg", (780, 585),  70, (0.45, 0.45)),
    ("sec-campus.jpg", "sec-campus.jpg",(1400, 800),  66, (0.5, 0.55)),
    ("sec-lib.jpg",    "sec-lib.jpg",    (720, 540),  70, (0.5, 0.5)),
]

def crop_to(im, box, focal):
    tw, th = box
    w, h = im.size
    scale = max(tw / w, th / h)
    nw, nh = round(w * scale), round(h * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focal
    left = int(round(min(max(fx * nw - tw / 2, 0), nw - tw)))
    top = int(round(min(max(fy * nh - th / 2, 0), nh - th)))
    return im.crop((left, top, left + tw, top + th))

total = 0
for src, dst, box, q, focal in JOBS:
    im = Image.open(RAW / src).convert("RGB")
    im = crop_to(im, box, focal)
    p = OUT / dst
    im.save(p, "JPEG", quality=q, optimize=True, progressive=True)
    kb = p.stat().st_size // 1024
    total += kb
    print(f"{dst:15s} {box[0]}x{box[1]:4d}  {kb} KB")
print("total", total, "KB")
