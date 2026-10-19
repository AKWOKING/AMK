#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK photo prep — préparer des photos client RÉELLES pour un site, en local.

Deux modes, et rien d'autre :
  --mode catalogue : détourage IA (ISNet/u2net via ONNX, local) + fond propre
                     uniforme, ratio 4:3 (contrat catalogue DM 800x600 affiché,
                     export 1600x1200). Aucune couleur de monture n'est
                     retouchée, aucune forme n'est redessinée.
  --mode clinique  : AUCUN détourage. Rotation EXIF, niveaux doux, netteté
                     légère, redimensionnement. La pièce reste la pièce.

Règles (voir README.md) : rien ne part dans un cloud ; aucun visage IA ;
aucun objet n'est effacé/inventé ; le modèle ONNX vit hors dépôt
(~/.rembg/models/manual/), jamais commité.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageEnhance, ImageOps

MODELS = [
    ("imgly-medium.onnx", "isnet"),
    ("imgly-small.onnx", "isnet"),
    ("u2net.onnx", "u2net"),
]


def find_model(explicit):
    if explicit:
        p = Path(explicit).expanduser()
        kind = "u2net" if "u2net" in p.name else "isnet"
        return p, kind
    base = Path.home() / ".rembg" / "models" / "manual"
    for name, kind in MODELS:
        p = base / name
        if p.exists():
            return p, kind
    u2 = Path.home() / ".rembg" / "models" / "u2net" / "u2net.onnx"
    if u2.exists():
        return u2, "u2net"
    sys.exit("Aucun modèle ONNX trouvé — lance d'abord : bash tools/photo/install.sh")


def mask_of(img_rgb, session, kind):
    name = session.get_inputs()[0].name
    size = session.get_inputs()[0].shape[2] or (1024 if kind == "isnet" else 320)
    x = img_rgb.resize((size, size), Image.LANCZOS)
    a = np.asarray(x).astype(np.float32) / 255.0
    if kind == "isnet":          # ISNet : [-1, 1]
        a = (a - 0.5) / 0.5
    else:                        # u2net : normalisation ImageNet
        a = (a - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
    a = np.transpose(a, (2, 0, 1))[None].astype(np.float32)
    out_name = session.get_outputs()[0].name
    m = session.run([out_name], {name: a})[0][0, 0].astype(np.float32)
    m = (m - m.min()) / max(m.max() - m.min(), 1e-6)
    return Image.fromarray((m * 255).astype(np.uint8)).resize(img_rgb.size, Image.LANCZOS)


def do_catalogue(src, outdir, session, kind, bg):
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    mask = mask_of(img, session, kind)
    fg = float((np.asarray(mask) > 40).mean())
    cut = img.convert("RGBA")
    cut.putalpha(mask)
    cut.save(outdir / f"{src.stem}-cutout.png")

    bbox = mask.point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bbox:
        print(f"  ⚠️ {src.name}: sujet non détecté — vérifie la photo à la main.")
        return
    crop = cut.crop(bbox)
    W, H = 1600, 1200
    crop.thumbnail((int(W * 0.88), int(H * 0.82)), Image.LANCZOS)
    canvas = Image.new("RGBA", (W, H), bg + (255,))
    canvas.alpha_composite(crop, ((W - crop.width) // 2, (H - crop.height) // 2))
    out = outdir / f"{src.stem}-catalogue.jpg"
    canvas.convert("RGB").save(out, quality=90)
    warn = " ⚠️ fg suspect, contrôle visuel requis" if fg < 0.02 or fg > 0.98 else ""
    print(f"  ✅ {src.name} -> {out.name} (sujet {fg*100:.1f} % de l'image){warn}")


def do_clinique(src, outdir):
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Color(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.08)
    img.thumbnail((1920, 1920), Image.LANCZOS)
    out = outdir / f"{src.stem}-web.jpg"
    img.save(out, quality=88)
    print(f"  ✅ {src.name} -> {out.name} (corrections classiques, aucun détourage)")


def main():
    ap = argparse.ArgumentParser(description="Prépare des photos client réelles pour le web (local, IA détourage seulement).")
    ap.add_argument("inputs", nargs="+", help="Fichier(s) ou dossier d'images")
    ap.add_argument("-o", "--outdir", required=True)
    ap.add_argument("--mode", choices=["catalogue", "clinique"], default="catalogue")
    ap.add_argument("--bg", default="FFFFFF", help="Fond catalogue, hex sans # (défaut blanc)")
    ap.add_argument("--model", default=None, help="Chemin ONNX explicite (sinon PHOTO_MODEL / défaut)")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    files = []
    for i in args.inputs:
        p = Path(i)
        files += sorted(p.glob("*")) if p.is_dir() else [p]
    files = [f for f in files if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    if not files:
        sys.exit("Aucune image trouvée.")

    session = kind = None
    if args.mode == "catalogue":
        import os
        model_path, kind = find_model(args.model or os.environ.get("PHOTO_MODEL"))
        session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
        print(f"Modèle : {model_path.name} ({kind}, CPU)")
    bg = tuple(int(args.bg[i:i + 2], 16) for i in (0, 2, 4))
    for f in files:
        (do_catalogue(f, outdir, session, kind, bg) if args.mode == "catalogue"
         else do_clinique(f, outdir))
    print("Terminé. Contrôle chaque sortie à l'œil avant toute publication (règle maison).")


if __name__ == "__main__":
    main()
