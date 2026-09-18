#!/usr/bin/env python3
"""AMK — MAQUETTE INSTANTANÉE personnalisée (avant tout build).

Décision de King (18 Sep 2026) : on ne construit plus un site complet avant le « oui »
du prospect. Avant le « oui » → une **maquette légère mais personnalisée** ; le site
complet n'est construit qu'après un accord explicite.

Chaîne : modèle d'accueil à jetons (site/mockup-hero.html)
        → rempli avec les mots du prospect
        → capturé (Chromium)
        → composé en image 1080×1350 prête à envoyer sur WhatsApp.
~2 minutes par prospect, sans réseau.

Règle d'exactitude : ce script n'invente RIEN. Les seuls textes visibles sont ceux
passés en arguments — donc les mots du prospect lui-même (tarifs, horaires,
témoignages restent dehors). La page porte l'étiquette « maquette, pas encore en ligne ».

Usage :
    python3 tools/outreach/mockup.py \\
        --vertical clinique \\
        --name "Cabinet Dentaire YAKS" \\
        --specialty "Cabinet dentaire · Logbessou, Douala" \\
        --color "#0E7A5C" --whatsapp 672702078 \\
        --h1 "Des soins dentaires|sans surprise" \\
        --sub "Urgences, détartrage et blanchiment — rendez-vous confirmé sur WhatsApp." \\
        --svc "Urgences,Détartrage,Blanchiment" \\
        --out clients/_mockups/yaks.jpg

Prérequis : bash tools/video/install.sh
            export LD_LIBRARY_PATH=/tmp/amk-video/al2023/lib FONTCONFIG_PATH=/tmp/amk-video/fonts
"""
import argparse
import base64
import html
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODEL = ROOT / "site/mockup-hero.html"

# Réglages par métier : photo par défaut + libellés d'action neutres (jamais de chiffre).
VERTICALS = {
    "clinique": {
        "photo": "site/assets/mockup-clinique.jpg",
        "cta1": "Prendre rendez-vous", "cta2": "Appeler",
        "bar": "Écrire sur WhatsApp", "bar_sub": "Réponse pendant les heures d'ouverture",
        "badge": "Bilingue EN / FR",
    },
    "college": {
        "photo": "site/assets/mockup-college.jpg",
        "cta1": "Demander une inscription", "cta2": "Appeler",
        "bar": "Écrire sur WhatsApp", "bar_sub": "Admission — dossier et frais",
        "badge": "Bilingue EN / FR",
    },
}


def hex_ok(v):
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", v.strip()))


def lighten(hexcolor, amount=0.30):
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: int(round(c + (255 - c) * amount))  # noqa: E731
    return "#{:02X}{:02X}{:02X}".format(mix(r), mix(g), mix(b))


def initials(name):
    words = [w for w in re.split(r"[\s·,]+", name) if w and w[0].isalnum()]
    return "".join(w[0] for w in words[:2]).upper() or "AM"


def to_data_uri(path):
    ext = pathlib.Path(path).suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
    return f"data:image/{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def fill(a, v):
    """Remplit le modèle à jetons. Aucun texte n'est inventé ici."""
    if not MODEL.exists():
        sys.exit(f"✗ modèle introuvable : {MODEL}")
    page = MODEL.read_text(encoding="utf-8")

    h1a, _, h1b = a.h1.partition("|")
    svcs = [s.strip() for s in a.svc.split(",") if s.strip()]
    if len(svcs) != 3:
        sys.exit("✗ --svc attend exactement 3 activités séparées par des virgules "
                 f"(reçu {len(svcs)})")

    photo = pathlib.Path(a.photo) if a.photo else ROOT / v["photo"]
    if not photo.exists():
        sys.exit(f"✗ photo introuvable : {photo}")

    tokens = {
        "NAME": a.name, "INITIALS": initials(a.name),
        "EYEBROW": a.specialty, "H1_A": h1a, "H1_B": h1b,
        "SUB": a.sub, "CTA1": a.cta1 or v["cta1"], "CTA2": a.cta2 or v["cta2"],
        "PHOTO": to_data_uri(photo), "BADGE": a.badge or v["badge"],
        "S1": svcs[0], "S2": svcs[1], "S3": svcs[2],
        "BAR": a.bar or v["bar"], "BAR_SUB": a.bar_sub or v["bar_sub"],
        "BRAND": a.color, "BRAND_B": lighten(a.color),
    }
    if a.whatsapp:
        digits = re.sub(r"\D", "", a.whatsapp)
        if not digits.startswith("237"):
            digits = "237" + digits.lstrip("0")
        tokens["BAR_SUB"] = f"{a.bar_sub or v['bar_sub']} · +{digits}"

    for k, val in tokens.items():
        page = page.replace("{{" + k + "}}", html.escape(str(val), quote=True)
                            .replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>"))

    left = re.findall(r"\{\{[A-Z_]+\}\}", page)
    if left:
        sys.exit(f"✗ jetons non remplis : {sorted(set(left))}")
    return page


def capture(url, out_dir, width, height, env):
    cmd = ["node", str(ROOT / "tools/video/capture.mjs"), "--url", url,
           "--out", str(out_dir), "--mode", "hero",
           "--width", str(width), "--height", str(height), "--dsf", "1", "--wait", "900"]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("✗ capture impossible — chaîne installée ? (bash tools/video/install.sh)\n"
                 + (r.stderr or r.stdout or "")[-500:])
    p = pathlib.Path(out_dir) / "hero.png"
    if not p.exists():
        sys.exit(f"✗ capture attendue absente : {p}")
    return p


def build_card(a, hero_uri):
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
  *{{box-sizing:border-box;margin:0}}
  body{{width:1080px;height:{a.height}px;background:#0B1020;font-family:Inter,Arial,sans-serif;overflow:hidden}}
  .bg{{position:absolute;inset:0;background:
      radial-gradient(1200px 600px at 12% -8%, {a.color}44, transparent 60%),
      radial-gradient(900px 500px at 92% 8%, #23C4B122, transparent 55%),
      #0B1020}}
  .wrap{{position:relative;padding:54px 64px 0}}
  .top{{display:flex;align-items:center;gap:18px}}
  .dot{{width:26px;height:26px;border-radius:50%;background:{a.color}}}
  .amk{{color:#9FB0D0;font:600 26px/1 Inter,Arial;letter-spacing:.14em}}
  .card{{margin-top:44px;background:#FFFFFF;border-radius:34px;padding:40px 40px 34px;
        box-shadow:0 40px 90px rgba(0,0,0,.55)}}
  .kicker{{color:{a.color};font:700 26px/1 Inter,Arial;letter-spacing:.12em;text-transform:uppercase}}
  h1{{margin:14px 0 8px;color:#0E1430;font:800 62px/1.06 Inter,Arial;letter-spacing:-1px}}
  .sub{{color:#5A6784;font:400 30px/1.35 Inter,Arial}}
  .rule{{height:6px;width:120px;background:{a.color};border-radius:3px;margin:26px 0 0}}
  .shot{{margin:36px 26px 0;display:flex;justify-content:center}}
  .phone{{width:{a.phone_w}px;background:#0B1020;border-radius:52px;padding:16px;
         box-shadow:0 34px 70px rgba(0,0,0,.6)}}
  .screen{{border-radius:38px;overflow:hidden;background:#fff;height:{a.phone_h}px}}
  .screen img{{width:100%;display:block}}
  .tag{{position:relative;margin:22px 26px 0;display:inline-block;color:#FFE3CE;
       background:#9E3F1D;border-radius:999px;padding:12px 24px;font:700 24px Inter,Arial}}
  .foot{{position:absolute;left:64px;right:64px;bottom:44px;display:flex;justify-content:space-between;
        align-items:center;color:#8FA0BF;font:600 26px Inter,Arial}}
  .pill{{color:#0B1020;background:#23C4B1;border-radius:999px;padding:16px 30px;font:800 28px Inter,Arial}}
</style></head><body>
<div class="bg"></div>
<div class="wrap">
  <div class="top"><span class="dot"></span><span class="amk">MAQUETTE AMK · APERÇU NON OFFICIEL</span></div>
  <div class="card">
    <div class="kicker">{html.escape(a.kicker)}</div>
    <h1>{html.escape(a.name)}</h1>
    <div class="sub">{html.escape(a.specialty)}</div>
    <div class="rule"></div>
  </div>
  <div class="shot"><div class="phone"><div class="screen"><img src="{hero_uri}"></div></div></div>
  <div class="tag">MAQUETTE PERSONNALISÉE · PAS LE SITE FINAL</div>
</div>
<div class="foot"><span>{html.escape(a.line)}</span><span class="pill">RÉPONDEZ «&nbsp;OUI&nbsp;»</span></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vertical", required=True, choices=sorted(VERTICALS))
    ap.add_argument("--name", required=True, help="nom du prospect, tel qu'il s'affiche")
    ap.add_argument("--specialty", required=True, help="ex. « Cabinet dentaire · Logbessou, Douala »")
    ap.add_argument("--color", required=True, help="couleur de marque du prospect, #RRGGBB")
    ap.add_argument("--h1", required=True, help="titre, « partie normale|partie accentuée »")
    ap.add_argument("--sub", required=True, help="une phrase, les mots du prospect")
    ap.add_argument("--svc", required=True, help="3 activités séparées par des virgules")
    ap.add_argument("--whatsapp", default="", help="numéro WhatsApp du prospect (optionnel)")
    ap.add_argument("--photo", default="", help="photo de la maquette (défaut : selon le métier)")
    ap.add_argument("--cta1", default="", help="bouton principal")
    ap.add_argument("--cta2", default="", help="bouton secondaire")
    ap.add_argument("--badge", default="", help="pastille sur la photo")
    ap.add_argument("--bar", default="", help="barre du bas")
    ap.add_argument("--bar-sub", dest="bar_sub", default="")
    ap.add_argument("--kicker", default="Aperçu gratuit · 1 page d'accueil")
    ap.add_argument("--line", default="Site bilingue · RDV WhatsApp en un clic")
    ap.add_argument("--out", required=True)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--phone-w", type=int, default=430)
    ap.add_argument("--phone-h", type=int, default=560)
    a = ap.parse_args()

    if not hex_ok(a.color):
        sys.exit(f"✗ --color doit être au format #RRGGBB (reçu : {a.color})")

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path("/tmp/amk-mockup")
    tmp.mkdir(parents=True, exist_ok=True)

    rt = os.environ.get("AMK_VIDEO_RUNTIME", "/tmp/amk-video")
    env = dict(os.environ)
    env.setdefault("LD_LIBRARY_PATH", f"{rt}/al2023/lib")
    env.setdefault("FONTCONFIG_PATH", f"{rt}/fonts")

    page = tmp / "prospect.html"
    page.write_text(fill(a, VERTICALS[a.vertical]), encoding="utf-8")
    hero = capture(page.as_uri(), tmp / "prospect", 540, 1100, env)

    card = tmp / "card.html"
    card.write_text(build_card(a, to_data_uri(hero)), encoding="utf-8")
    shot = capture(card.as_uri(), tmp / "render", 1080, a.height, env)

    from PIL import Image
    img = Image.open(shot).convert("RGB")
    img.save(out, quality=92)
    print(f"✓ maquette : {out}  ({img.size[0]}×{img.size[1]}, "
          f"{round(out.stat().st_size/1024)} Ko)  [{a.vertical} · {a.name}]")


if __name__ == "__main__":
    main()
