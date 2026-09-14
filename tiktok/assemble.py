#!/usr/bin/env python3
"""AMK TikTok assembly — video #1 (reusable for the series).
Inputs: clips/{hook,fb,nova,crest,end}-normal.mp4 + a voiceover mp3.
Output: video1-final.mp4 (1080x1920, 25fps, burned bilingual captions, VO audio).
Timeline auto-fits the voiceover length: end card begins just before the spoken CTA.
"""
import json, re, subprocess, sys, pathlib

FF = __import__("imageio_ffmpeg").get_ffmpeg_exe()
ROOT = pathlib.Path("/home/user/agency/tiktok")

def ff(*args, **kw):
    p = subprocess.run([FF, "-nostdin", "-y", "-loglevel", "error", *args],
                       capture_output=True, text=True, **kw)
    if p.returncode != 0:
        print("FFMPEG FAILED:\n", " ".join(str(a) for a in args[:6]), "\n", p.stderr[-3000:])
        sys.exit(1)
    return p

def duration(path):
    p = subprocess.run([FF, "-nostdin", "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", p.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))

# ---------- parameters (edit per video) ----------
VO = ROOT / "vo-video1-fr.mp3"
CTA_TEXT_FR = "Aperçu gratuit en vingt-quatre heures. Écrivez APERÇU sur WhatsApp."
FULL_FR = ("Les parents cherchent votre école sur Google avant de l'appeler. "
           "Et ce qu'ils trouvent ? Une page Facebook… ou un site qui ressemble à l'école de quelqu'un d'autre. "
           "On construit ça pour votre école — vos couleurs, votre histoire, en deux langues, en trois à cinq jours. "
           + CTA_TEXT_FR)
CTA_RATIO = 1 - len(CTA_TEXT_FR) / len(FULL_FR)  # ~where the CTA is spoken

CAPTIONS = [  # (fr, en, start_frac_or_None, end_frac_or_None) — None = segment boundary
    ("Les parents cherchent votre école sur Google avant de l'appeler.",
     "Parents Google your school before they call it.", 0.004, "hook"),
    ("Et ce qu'ils trouvent ? Une page Facebook…",
     "And what do they find? A Facebook page…", "hook", "fb"),
    ("…ou un site qui ressemble à l'école de quelqu'un d'autre.",
     "…or a site that looks like someone else's school.", "fb", "nova"),
    ("On construit ça pour votre école — vos couleurs, votre histoire,",
     "We build that for your school — your colors, your story,", "nova", "crest_mid"),
    ("en deux langues, en 3 à 5 jours.",
     "in two languages, in 3 to 5 days.", "crest_mid", "crest"),
    ("Aperçu gratuit en 24h — écrivez APERÇU sur WhatsApp.",
     "Free 24h preview — message APERÇU on WhatsApp.", "end_start", "total"),
]

def main():
    seg = {}
    for name in ("hook", "fb", "nova", "crest", "end"):
        seg[name] = duration(ROOT / "clips" / f"{name}-normal.mp4")
    vo_len = duration(VO)
    print("segments:", json.dumps({k: round(v, 2) for k, v in seg.items()}), "vo:", round(vo_len, 2))

    cta_said = 0.3 + vo_len * CTA_RATIO          # 0.3s = audio lead delay
    end_start = max(cta_said - 0.6, seg["crest"] * 0.35 + 8.72)  # crest needs a minimum
    crest_len = end_start - (seg["hook"] + seg["fb"] + seg["nova"])
    total = end_start + seg["end"]
    print(f"cta_said={cta_said:.2f}  end_start={end_start:.2f}  crest_used={crest_len:.2f}  total={total:.2f}")

    # trim crest to used length
    ff("-i", str(ROOT / "clips/crest-normal.mp4"), "-t", f"{crest_len:.3f}",
       "-c", "copy", str(ROOT / "clips/crest-trim.mp4"))
    order = ["hook", "fb", "nova", "crest-trim", "end"]

    # concat (re-encode, uniform)
    ins = " ".join(f"-i {ROOT/'clips'/f'{n}-normal.mp4' if n!='crest-trim' else ROOT/'clips/crest-trim.mp4'}" for n in order)
    ff(*ins.split(), "-filter_complex",
       "[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0,format=yuv420p[v]",
       "-map", "[v]", "-r", "25", "-c:v", "libx264", "-crf", "20",
       "-preset", "medium", str(ROOT / "video1-silent.mp4"))

    # timeline boundaries for captions
    b = {"hook": seg["hook"], "fb": seg["hook"] + seg["fb"], "nova": seg["hook"] + seg["fb"] + seg["nova"],
         "crest": end_start, "crest_mid": (seg["hook"] + seg["fb"] + seg["nova"] + end_start) / 2,
         "end_start": end_start, "total": total}
    def t(x):
        return b[x] if isinstance(x, str) else x
    def ts(sec):
        h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: FR,Arial,60,&H00FFFFFF,&H00FFFFFF,&H000F172A,&H960F172A,-1,0,0,0,100,100,0,0,1,7,0,2,70,70,330,1
Style: EN,Arial,40,&H00D9E2F3,&H00D9E2F3,&H000F172A,&H960F172A,0,0,0,0,100,100,0,0,1,6,0,2,70,70,225,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    for fr, en, s, e in CAPTIONS:
        s, e = t(s), t(e)
        fr_e = fr.replace("{", "\\{").replace("}", "\\}")
        en_e = en.replace("{", "\\{").replace("}", "\\}")
        ass += f"Dialogue: 0,{ts(s)},{ts(e)},FR,,0,0,0,,{fr_e}\n"
        ass += f"Dialogue: 0,{ts(s)},{ts(e)},EN,,0,0,0,,{en_e}\n"
    (ROOT / "captions.ass").write_text(ass)

    # mux VO (0.3s lead) + burn captions
    ff("-i", str(ROOT / "video1-silent.mp4"), "-i", str(VO),
       "-filter_complex",
       f"[1:a]adelay=300|300[a];[0:v]ass={ROOT}/captions.ass[v]",
       "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-crf", "20", "-preset", "medium",
       "-c:a", "aac", "-b:a", "160k", "-shortest",
       str(ROOT / "video1-final.mp4"))
    print("DONE", duration(ROOT / "video1-final.mp4"))

if __name__ == "__main__":
    main()
