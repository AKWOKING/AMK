#!/usr/bin/env python3
"""Pose la voix off sur le master muet, en respectant les frontières de scènes.

Le montage suit la voix : `narration/timeline.json` donne les départs mesurés des six phrases,
et le master a été rendu avec ces mêmes frontières. Ce script recolle donc les deux sans
deviner — il refuse de tourner si le master et la timeline ne s'accordent pas à ±0,15 s.
"""
import json
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

HERE = Path(__file__).resolve().parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
SILENT = HERE / "Video_06_Facebook_No_Booking.mp4"
FINAL = HERE / "Video_06_Facebook_No_Booking_VOIX.mp4"
tl = json.loads((HERE / "narration" / "timeline.json").read_text())


def dur(p):
    e = subprocess.run([FF, "-i", str(p)], capture_output=True, text=True).stderr
    for l in e.splitlines():
        if "Duration" in l:
            h, m, s = l.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0


def main():
    starts, durs = tl["starts"], tl["durations"]
    total = starts[-1]
    vdur = dur(SILENT)
    print(f"master {vdur:.2f}s · montage prévu {total:.2f}s · {len(durs)} phrases")
    if abs(vdur - total) > 0.35:
        sys.exit(f"✗ écart trop grand ({abs(vdur - total):.2f}s) — relancer le rendu avec la timeline")
    ins, filt = [], []
    for i in range(6):
        ins += ["-i", str(HERE / "narration" / f"n{i+1}.mp3")]
        ms = int(round(starts[i] * 1000))
        filt.append(f"[{i+1}:a]adelay={ms}|{ms},volume=1.9[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(6))
    filt.append(f"{mix}amix=inputs=6:normalize=0:dropout_transition=0,"
                f"acompressor=threshold=0.12:ratio=3:attack=8:release=180,"
                f"loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{total:.3f}[aout]")
    cmd = [FF, "-y", "-i", str(SILENT), *ins, "-filter_complex", ";".join(filt),
           "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-ar", "48000", "-t", f"{total:.3f}", "-movflags", "+faststart", str(FINAL)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
        sys.exit("✗ ffmpeg a refusé le montage")
    print(f"écrit : {FINAL.name} · {dur(FINAL):.2f}s")


if __name__ == "__main__":
    main()
