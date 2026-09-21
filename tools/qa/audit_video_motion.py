#!/usr/bin/env python3
"""AMK — portique « MOUVEMENT » pour les vidéos.

Pourquoi : le master #4 était un diaporama (15 fenêtres sur 20 totalement figées) et personne
ne l'a vu avant publication — les défauts de rythme ne se voient pas en survolant un fichier.
Cet outil mesure, image par image, **où la vidéo ne bouge pas**.

Méthode : échantillonnage à `--fps` (défaut 12), écart moyen |Δ| entre images consécutives,
agrégation par fenêtre de `--window` secondes (défaut 2 s — la fenêtre où TikTok perd le spectateur).
Une fenêtre est **FIGÉE** si son écart maximal reste sous `--thresh` (défaut 1.5/255).
Les écarts > `--cut` (défaut 8) sont comptés comme des **coupes** (changement de scène).

Usage :
    python3 tools/qa/audit_video_motion.py <video.mp4> [--window 2.0] [--fps 12] [--thresh 1.5] [--json]

Sortie : tableau par fenêtre + verdict. Code de sortie 1 si au moins une fenêtre est figée
(le portique est bloquant : une vidéo qui gèle 2 s de suite ne part pas en publication).
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

import imageio_ffmpeg
import numpy as np
from PIL import Image

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def sample_frames(path, fps, workdir, width=270):
    subprocess.run(
        [FFMPEG, "-v", "error", "-i", path,
         "-vf", f"fps={fps},scale={width}:-2",
         "-q:v", "4", os.path.join(workdir, "f%05d.jpg")],
        check=True,
    )
    return sorted(f for f in os.listdir(workdir) if f.endswith(".jpg"))


def load(path):
    return np.asarray(Image.open(path).convert("L"), dtype=np.int16)


def duration(path):
    r = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--window", type=float, default=2.0, help="taille de fenêtre en secondes (défaut 2)")
    ap.add_argument("--fps", type=float, default=12.0, help="images échantillonnées par seconde")
    ap.add_argument("--thresh", type=float, default=1.5, help="sous cet écart maximal, la fenêtre est FIGÉE")
    ap.add_argument("--cut", type=float, default=8.0, help="écart considéré comme une coupe (changement de scène)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.video):
        sys.exit(f"fichier introuvable : {a.video}")

    work = tempfile.mkdtemp(prefix="motion_")
    try:
        files = sample_frames(a.video, a.fps, work)
        if len(files) < 3:
            sys.exit("échantillonnage impossible (vidéo trop courte ?)")
        step = 1.0 / a.fps
        prev = load(os.path.join(work, files[0]))
        deltas = []  # (temps, écart)
        for i, f in enumerate(files[1:], start=1):
            cur = load(os.path.join(work, f))
            deltas.append((i * step, float(np.abs(cur - prev).mean())))
            prev = cur

        dur = duration(a.video)
        n_windows = max(1, int(np.ceil(dur / a.window)))
        rows, frozen = [], []
        for w in range(n_windows):
            lo, hi = w * a.window, (w + 1) * a.window
            # on ne juge que les fenêtres réellement couvertes par la vidéo (>= 60 % de la fenêtre)
            if hi > dur + 1e-6 and (dur - lo) < 0.6 * a.window:
                continue
            vals = [d for t, d in deltas if lo <= t < hi]
            if not vals:
                continue
            mx, avg = max(vals), sum(vals) / len(vals)
            cuts = sum(1 for v in vals if v >= a.cut)
            state = "FIGÉE" if mx < a.thresh else ("mouvement" if mx >= a.cut else "léger")
            rows.append({"window": f"{lo:.0f}-{hi:.0f}s", "max": round(mx, 2),
                         "moy": round(avg, 2), "coupes": cuts, "etat": state})
            if state == "FIGÉE":
                frozen.append(rows[-1]["window"])

        result = {
            "video": a.video,
            "duree_s": round(dur, 2),
            "fenetres": rows,
            "fenetres_figees": frozen,
            "verdict": "BLOQUÉ — diaporama" if frozen else "OK — mouvement présent dans chaque fenêtre",
        }
        if a.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n{os.path.basename(a.video)}  ·  {result['duree_s']} s  ·  fenêtre {a.window:g} s  ·  seuil {a.thresh:g}/255")
            print(f"{'fenêtre':>10} {'max':>7} {'moy':>7} {'coupes':>7}  état")
            for r in rows:
                print(f"{r['window']:>10} {r['max']:>7.2f} {r['moy']:>7.2f} {r['coupes']:>7}  {r['etat']}")
            print(f"\nVERDICT : {result['verdict']}")
            if frozen:
                print(f"fenêtres figées : {', '.join(frozen)}")
        return 1 if frozen else 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
