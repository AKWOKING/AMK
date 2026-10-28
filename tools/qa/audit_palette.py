# -*- coding: utf-8 -*-
"""audit_palette.py — la règle 60-30-10, mesurée au lieu d'être récitée.

    python3 tools/qa/audit_palette.py --sheet design/STYLE-TOKENS.md          # le contrat des jetons
    python3 tools/qa/audit_palette.py --html demos/concept-x.html             # ce que le CSS peint
    python3 tools/qa/audit_palette.py --image shot.png --palette "#F6F3EC=surface,#0E7A5C=brand,#C9923B=accent"
    python3 tools/qa/audit_palette.py --self-test

POURQUOI CET OUTIL (28/10/2026).
`AMK-DESIGN-SKILLS.md` §6.1 dit depuis le 17/09 : « ~60 % de surfaces neutres, ~30 % de couleur de marque,
~10 % d'accent » — et **rien ne le mesurait**. C'est exactement le défaut que le dépôt s'interdit
ailleurs : une règle écrite n'est pas une règle exécutée. Ce script mesure la seule chose que le §6.1
affirme et que personne ne vérifie : **la proportion**.

CE QUE CET OUTIL NE FAIT PAS, ET IL LE DIT :
le contraste. `tools/qa/audit_html.py` le calcule page par page, avec le seuil WCAG en fonction de la
taille (4,5:1, 3:1 au-delà de 24 px). On **réutilise ses fonctions** (`lum`, `ratio`) au lieu d'en écrire
d'autres : deux outils qui mesurent la même chose finissent par se contredire. Ici, le contraste n'est
mesuré que sur une **planche de jetons** (un fichier CSS de variables), pas sur une page construite.

LES TROIS MODES
  --sheet   lit les blocs `:root{}` d'un fichier de jetons, classe chaque variable par rôle d'après son
            nom, vérifie le contrat (surface, ink, brand) et les paires de contraste canoniques.
  --html    compte ce que la feuille de style **peint** : combien de déclarations `background`, `color`,
            `border` utilisent chaque rôle. Ce ne sont pas des pixels, ce sont des intentions — et c'est
            déjà suffisant pour attraper l'accent mis partout, y compris sur le texte courant.
  --image   mesure la **vraie surface** : décode un PNG sans dépendance (zlib seul), rattache chaque
            pixel à la couleur la plus proche de la palette, et rend les pourcentages.

BANDES (et pourquoi ce ne sont pas des chiffres exacts)
La règle vient de la décoration d'intérieur (murs 60 / mobilier 30 / coussins 10), reprise par la
photographie de cinéma et par NN/g pour les interfaces. Aucune source sérieuse ne prétend qu'il faut
61,4 %. On juge donc une **hiérarchie**, pas un camembert :
    dominant (surfaces)  45 – 85 %      en dessous = page chargée, au-dessus = page plate
    secondaire (marque)   5 – 40 %      en dessous = marque absente
    accent               0,7 – 15 %     au-dessus = accent partout donc rien d'accentué
                                        en dessous = accent invisible
Sur une photographie de page, les pixels « autres » (photos, dégradés, images) sont comptés à part :
ils ne font pas partie de la palette et les inclure fausserait la mesure.

Code de sortie : 0 = aucune faute bloquante, 1 = au moins une.
"""
import argparse
import pathlib
import re
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Le contraste appartient à audit_html.py. On le réutilise.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
try:                                             # pragma: no cover - dépend du dépôt
    from audit_html import lum, ratio
except Exception:                                # autonome si le module bouge
    def lum(c):
        def ch(v):
            v = v / 255.0
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g, b = (ch(x) for x in c[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def ratio(a, b):
        la, lb = lum(a), lum(b)
        hi, lo = max(la, lb), min(la, lb)
        return (hi + 0.05) / (lo + 0.05)

# ─────────────────────────────────────────────────────────────────────────────
# Rôles — classés par NOM de variable, jamais par goût.
ROLE_PATTERNS = [
    ("surface", re.compile(r"^--(surface|bg|background|paper|bone|cream|canvas)")),
    ("ink", re.compile(r"^--(ink|text|fg|foreground|body)")),
    ("brand", re.compile(r"^--(brand|primary|crest|g[0-9]{3})")),
    ("accent", re.compile(r"^--(accent|gold|amber|sun|berry|pop|highlight)")),
    ("line", re.compile(r"^--(line|border|rule|hairline)")),
    ("semantic", re.compile(r"^--(ok|warn|danger|error|success)")),
]
HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
CSS_BLOCK = re.compile(r"```css(.*?)```", re.S)
VAR_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")

BANDS = {
    "dominant": (45.0, 85.0),
    "secondary": (5.0, 40.0),
    "accent": (0.7, 15.0),
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def role_of(name):
    n = name.lower()
    for role, rx in ROLE_PATTERNS:
        if rx.match(n):
            return role
    return "other"


# ─────────────────────────────────────────────────────────────────────────────
# MODE 1 — la planche de jetons
def parse_sheets(text):
    """Rend [(titre, {var: hex})] pour chaque bloc ```css d'un fichier de jetons."""
    sheets = []
    for block in CSS_BLOCK.findall(text):
        vars_ = {}
        for name, val in VAR_RE.findall(block):
            m = HEX_RE.search(val)
            if m:
                vars_[name] = "#" + m.group(1)
        if vars_:
            sheets.append(vars_)
    return sheets


def title_before(text, block_marker_count):
    return None


def check_sheet(vars_, label=""):
    """Contrat de rôles + paires de contraste canoniques sur une planche de jetons."""
    out = {"label": label, "fails": [], "warns": [], "roles": {}, "ratios": []}
    for name, hexv in vars_.items():
        out["roles"].setdefault(role_of(name), {})[name] = hexv

    for required in ("surface", "ink", "brand"):
        if required not in out["roles"]:
            out["fails"].append(f"rôle « {required} » absent : un jeton qui ne nomme pas sa surface, "
                                f"son texte et sa marque ne peut pas être audité (§6.1)")

    def pick(role):
        d = out["roles"].get(role, {})
        return next(iter(d.values()), None)

    surface = pick("surface")
    ink = pick("ink")
    brand = pick("brand")
    accent = pick("accent")
    on_brand = vars_.get("--on-brand")

    pairs = [
        ("texte / fond de page", ink, surface, 4.5, "1.4.3 AA"),
        ("texte de marque / fond", brand, surface, 3.0, "1.4.11 AA — graphique"),
        ("texte sur marque", on_brand, brand, 4.5, "1.4.3 AA"),
    ]
    for label_, fg, bg, need, crit in pairs:
        if not fg or not bg:
            continue
        r = ratio(hex_to_rgb(fg), hex_to_rgb(bg))
        ok = r >= need
        out["ratios"].append((label_, fg, bg, round(r, 2), need, crit, ok))
        if not ok:
            out["fails"].append(f"{label_} : {r:.2f}:1 < {need}:1 — {crit}")

    if accent:
        r = ratio(hex_to_rgb(accent), hex_to_rgb(surface)) if surface else 0
        if surface and r < 3.0:
            out["warns"].append(
                f"accent sur surface : {r:.2f}:1 — un accent sous 3:1 ne peut pas porter un libellé "
                f"de bouton (1.4.3) ni une icône (1.4.11)")
    else:
        out["warns"].append("aucun rôle « accent » déclaré : la page n'aura aucun point le plus fort")

    # Un seul accent : §6.1, « max 1 accent ».
    if len(out["roles"].get("accent", {})) > 2:
        out["warns"].append(
            f"{len(out['roles']['accent'])} variables d'accent — §6.1 dit « max 1 accent » ; "
            f"un accent et sa teinte claire passent, trois familles non")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# MODE 2 — ce que le CSS peint
PROP_RE = re.compile(
    r"(background(?:-color)?|color|border(?:-color)?|fill|stroke)\s*:\s*([^;{}]+)")


def check_html(path):
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S)) or text
    counts = {}
    accent_as_text_on_body = []
    for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", styles):
        selector, body = rule.group(1).strip(), rule.group(2)
        if selector.startswith(("--", "@")):
            continue
        for prop, val in PROP_RE.findall(body):
            m = re.search(r"var\(\s*(--[\w-]+)", val) or re.search(r"(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3}))", val)
            if not m:
                continue
            key = m.group(1)
            counts[key] = counts.get(key, 0) + 1
            if prop == "color" and role_of(key) == "accent":
                sel_low = selector.lower()
                if re.search(r"(^|[\s,>+~])(b|body|p|li|td|dd|small|figcaption)\b", sel_low):
                    accent_as_text_on_body.append((selector.strip()[:60], key))

    out = {"fails": [], "warns": [], "counts": counts, "total": sum(counts.values()) or 1}
    for sel, key in accent_as_text_on_body:
        out["fails"].append(
            f"l'accent « {key} » est utilisé comme COULEUR DE TEXTE sur « {sel} » — l'accent met en "
            f"valeur un bouton ou un chiffre, il ne porte jamais le texte courant (§6.1, 1.4.3)")

    shares = {}
    for key, n in counts.items():
        r = role_of(key)
        shares[r] = shares.get(r, 0) + n
    out["shares"] = {k: 100.0 * v / out["total"] for k, v in shares.items()}
    acc = out["shares"].get("accent", 0.0)
    if acc > 30.0:
        out["warns"].append(
            f"l'accent représente {acc:.0f} % des déclarations de peinture — même sans mesurer les "
            f"pixels, c'est le signe qu'il est partout")
    if acc == 0.0 and counts:
        out["warns"].append("aucune déclaration peinte avec l'accent : la page n'a rien à quoi l'œil "
                            "s'accroche")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# MODE 3 — la vraie surface, en pixels (PNG décodé sans dépendance)
def read_png(path):
    """Rend (width, height, [(r,g,b)]) pour un PNG 8 bits RGB / RGBA / gris / palette."""
    data = pathlib.Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("pas un PNG")
    pos, idat = 8, b""
    w = h = depth = ctype = None
    plte = b""
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", chunk[:10])
        elif typ == b"PLTE":
            plte = chunk
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    if depth != 8 or ctype not in (0, 2, 3, 6):
        raise ValueError(f"PNG non géré : profondeur {depth}, type {ctype}")
    channels = {0: 1, 2: 3, 3: 1, 6: 4}[ctype]
    raw = zlib.decompress(idat)
    stride = w * channels
    out, prev = [], bytearray(stride)
    i = 0
    for _ in range(h):
        f = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if f == 1:
            for x in range(channels, stride):
                line[x] = (line[x] + line[x - channels]) & 0xFF
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 0xFF
        elif f == 3:
            for x in range(stride):
                a = line[x - channels] if x >= channels else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 0xFF
        elif f == 4:
            for x in range(stride):
                a = line[x - channels] if x >= channels else 0
                b = prev[x]
                c = prev[x - channels] if x >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 0xFF
        for x in range(w):
            px = line[x * channels:(x + 1) * channels]
            if ctype == 0:
                out.append((px[0], px[0], px[0]))
            elif ctype == 2:
                out.append((px[0], px[1], px[2]))
            elif ctype == 6:
                out.append((px[0], px[1], px[2]))
            else:
                n = px[0] * 3
                out.append((plte[n], plte[n + 1], plte[n + 2]))
        prev = line
    return w, h, out


def snap(pixels, palette, tol=42):
    """Rattache chaque pixel à la couleur la plus proche ; au-delà de `tol`, « autre »."""
    counts = {k: 0 for k in palette}
    counts["autre"] = 0
    for px in pixels:
        best, bd = None, 1e9
        for key, rgb in palette.items():
            d = (px[0] - rgb[0]) ** 2 + (px[1] - rgb[1]) ** 2 + (px[2] - rgb[2]) ** 2
            if d < bd:
                best, bd = key, d
        if bd <= tol * tol:
            counts[best] += 1
        else:
            counts["autre"] += 1
    return counts


def check_image(path, palette_spec, tol=42):
    palette, roles = {}, {}
    for part in palette_spec.split(","):
        part = part.strip()
        if not part:
            continue
        hexv, _, role = part.partition("=")
        key = hexv.strip()
        palette[key] = hex_to_rgb(key)
        roles[key] = (role.strip() or "other").lower()

    w, h, pixels = read_png(path)
    counts = snap(pixels, palette, tol=tol)
    total = float(len(pixels)) or 1.0
    out = {"size": (w, h), "fails": [], "warns": [], "shares": {}, "counts": counts}
    by_role = {}
    for key, n in counts.items():
        if key == "autre":
            continue
        by_role[roles[key]] = by_role.get(roles[key], 0) + n
        out["shares"][key] = 100.0 * n / total
    out["shares"]["autre"] = 100.0 * counts["autre"] / total

    # La photo n'est pas la palette : on mesure les proportions sur les pixels identifiés.
    # On parle la langue de la règle : la surface est le « dominant », la marque le « secondaire ».
    ALIAS = {"surface": "dominant", "dominant": "dominant",
             "brand": "secondary", "secondary": "secondary",
             "accent": "accent"}
    identified = sum(by_role.values()) or 1
    out["roles"] = {}
    for r, n in by_role.items():
        key = ALIAS.get(r, r)
        out["roles"][key] = out["roles"].get(key, 0.0) + 100.0 * n / identified
    if identified / total < 0.25:
        out["warns"].append(
            f"seulement {100*identified/total:.0f} % des pixels se rattachent à la palette : "
            f"la capture est surtout une photo — mesure peu concluante, refaire sur un écran chargé "
            f"sans image de fond")

    # Une seule faute possible côté dominant : TROP PEU (page chargée). Trop de dominant n'est pas une
    # faute, c'est un parti pris (affiche, champ sombre) — mais ça devient une faute si l'accent disparaît,
    # parce qu'alors plus rien ne guide l'œil.
    for role, (lo, hi) in BANDS.items():
        share = out["roles"].get(role, 0.0)
        if share < lo:
            out["fails" if role == "dominant" else "warns"].append(
                f"{role} à {share:.1f} % (bande {lo}–{hi} %)")
        elif share > hi:
            out["fails" if role == "accent" else "warns"].append(
                f"{role} à {share:.1f} % (bande {lo}–{hi} %)")
    if out["roles"].get("dominant", 0) > BANDS["dominant"][1] and out["roles"].get("accent", 0) < 0.7:
        out["fails"].append(
            "dominant > 85 % ET accent < 0,7 % : champ uniforme sans point d'accroche — l'œil ne sait "
            "pas où se poser (c'est le cas d'une affiche quand même ; sur une page, non)")
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Le banc
def make_png(path, w, h, rows):
    """Écrit un PNG RGB 8 bits minimal — pour le banc de test et pour rien d'autre."""
    raw = b"".join(b"\x00" + bytes(v for px in row for v in px) for row in rows)
    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    pathlib.Path(path).write_bytes(png)


def self_test():
    import tempfile
    ok = 0
    total = 0

    def check(label, cond):
        nonlocal ok, total
        total += 1
        if cond:
            ok += 1
        else:
            print(f"  ✗ {label}")

    # 1 · le contraste réutilisé
    check("noir/blanc = 21:1", abs(ratio((0, 0, 0), (255, 255, 255)) - 21.0) < 0.01)
    check("même couleur = 1:1", abs(ratio((10, 20, 30), (10, 20, 30)) - 1.0) < 1e-9)

    # 2 · les rôles se lisent au nom
    check("--surface-2 → surface", role_of("--surface-2") == "surface")
    check("--brand-bright → brand", role_of("--brand-bright") == "brand")
    check("--accent-tint → accent", role_of("--accent-tint") == "accent")
    check("--danger → semantic", role_of("--danger") == "semantic")
    check("--weird → other", role_of("--weird") == "other")

    # 3 · planche de jetons : une bonne, une fautive
    good = {"--surface": "#F6F3EC", "--ink": "#15201C", "--brand": "#0E7A5C",
            "--on-brand": "#FFFFFF", "--accent": "#C9923B"}
    r = check_sheet(good)
    check("planche saine : 0 faute", not r["fails"])
    bad = {"--surface": "#FFFFFF", "--ink": "#EEEEEE"}
    r = check_sheet(bad)
    check("planche sans marque : faute", any("marque" in f or "brand" in f for f in r["fails"]))
    check("planche sans marque : contraste signalé", any("1.4.3" in f for f in r["fails"]))

    # 4 · le CSS : accent sur le texte courant
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "x.html"
        p.write_text("<style>p{color:var(--accent);} .btn{background:var(--accent);}</style>",
                     encoding="utf-8")
        r = check_html(p)
        check("accent sur <p> → faute", any("COULEUR DE TEXTE" in f for f in r["fails"]))
        p.write_text("<style>.btn{background:var(--accent);} h1{color:var(--ink);}</style>",
                     encoding="utf-8")
        r = check_html(p)
        check("accent sur bouton seulement → pas de faute", not r["fails"])

        # 5 · image : 60/30/10 exact, puis accent partout
        surf, brand, acc = (246, 243, 236), (14, 122, 92), (201, 146, 59)
        rows = []
        for y in range(10):
            row = []
            for x in range(10):
                v = x + y * 10
                row.append(surf if v < 60 else (brand if v < 90 else acc))
            rows.append(row)
        img = pathlib.Path(d) / "a.png"
        make_png(img, 10, 10, rows)
        spec = "#F6F3EC=surface,#0E7A5C=brand,#C9923B=accent"
        r = check_image(img, spec)
        check("image 60/30/10 : 0 faute", not r["fails"])
        check("image : dominant ≈ 60", abs(r["roles"]["dominant"] - 60) < 1.5)
        check("image : accent ≈ 10", abs(r["roles"]["accent"] - 10) < 1.5)

        rows = [[acc if (x + y) % 2 else surf for x in range(10)] for y in range(10)]
        img2 = pathlib.Path(d) / "b.png"
        make_png(img2, 10, 10, rows)
        r = check_image(img2, spec)
        check("image 50 % d'accent → faute", any("accent" in f for f in r["fails"]))

        # 6 · une capture surtout photographique est signalée
        rows = [[(100, 60, 20) for _ in range(10)] for _ in range(10)]
        img3 = pathlib.Path(d) / "c.png"
        make_png(img3, 10, 10, rows)
        r = check_image(img3, spec)
        check("photo : avertissement de fiabilité", any("photo" in w for w in r["warns"]))

        # 7 · un champ presque uniforme n'est pas une faute… s'il reste un accent
        rows = [[surf if not (x == 0 and y == 0) else acc for x in range(10)] for y in range(10)]
        img4 = pathlib.Path(d) / "d.png"
        make_png(img4, 10, 10, rows)
        r = check_image(img4, spec)
        check("dominant 99 % + accent 1 % : avertissement, pas faute", not r["fails"])
        rows = [[surf for _ in range(10)] for _ in range(10)]
        img5 = pathlib.Path(d) / "e.png"
        make_png(img5, 10, 10, rows)
        r = check_image(img5, spec)
        check("champ uniforme sans accent : faute", any("accroche" in f for f in r["fails"]))

    print(f"banc de test : {ok}/{total}")
    return 0 if ok == total else 1


# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--sheet", help="fichier de jetons (blocs ```css avec variables)")
    ap.add_argument("--html", help="page construite : ce que le CSS peint")
    ap.add_argument("--image", help="capture PNG de la page")
    ap.add_argument("--palette", default="", help='couleurs attendues : "#hex=role,#hex=role"')
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--strict", action="store_true", help="rc=1 si un avertissement (défaut : fautes seules)")
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    fails = warns = 0
    if a.sheet:
        text = pathlib.Path(a.sheet).read_text(encoding="utf-8", errors="replace")
        sheets = parse_sheets(text)
        if not sheets:
            print("aucun bloc ```css avec des variables — rien à mesurer")
            return 1
        print(f"\nPLANCHE DE JETONS — {a.sheet}  ({len(sheets)} planche(s))\n" + "─" * 78)
        for i, vars_ in enumerate(sheets, 1):
            r = check_sheet(vars_)
            roles = ", ".join(f"{k}:{len(v)}" for k, v in sorted(r["roles"].items()))
            print(f"\nplanche {i} — {len(vars_)} variables · {roles}")
            for label, fg, bg, got, need, crit, ok in r["ratios"]:
                print(f"  {'✓' if ok else '✗'} {label:26s} {got:5.2f}:1 (min {need}) — {crit}")
            for f in r["fails"]:
                print(f"  ✗ {f}")
            for w in r["warns"]:
                print(f"  · {w}")
            fails += len(r["fails"])
            warns += len(r["warns"])

    if a.html:
        r = check_html(a.html)
        print(f"\nCE QUE LE CSS PEINT — {a.html}\n" + "─" * 78)
        print("  déclarations par rôle : " +
              ", ".join(f"{k} {v:.0f} %" for k, v in sorted(r["shares"].items(), key=lambda kv: -kv[1])))
        for f in r["fails"]:
            print(f"  ✗ {f}")
        for w in r["warns"]:
            print(f"  · {w}")
        fails += len(r["fails"])
        warns += len(r["warns"])

    if a.image:
        if not a.palette:
            print("--image exige --palette \"#hex=role,…\" (sinon on ne sait pas à quoi rattacher)")
            return 1
        r = check_image(a.image, a.palette)
        w, h = r["size"]
        print(f"\nSURFACE MESURÉE — {a.image}  ({w}×{h} px)\n" + "─" * 78)
        for k, v in sorted(r["shares"].items(), key=lambda kv: -kv[1]):
            print(f"  {k:9s} {v:6.2f} %")
        print("  — sur les pixels identifiés —")
        for k, v in sorted(r["roles"].items(), key=lambda kv: -kv[1]):
            lo, hi = BANDS.get(k, (0, 100))
            mark = "✓" if lo <= v <= hi else "✗"
            print(f"  {mark} {k:9s} {v:6.2f} %   bande {lo}–{hi} %")
        for f in r["fails"]:
            print(f"  ✗ {f}")
        for w2 in r["warns"]:
            print(f"  · {w2}")
        fails += len(r["fails"])
        warns += len(r["warns"])

    if not any([a.sheet, a.html, a.image, a.self_test]):
        ap.print_help()
        return 0

    print("\n" + "─" * 78)
    print(f"{fails} faute(s) · {warns} avertissement(s) — "
          f"{'BLOQUÉ' if fails or (a.strict and warns) else 'OK'}")
    print("Rappel : ce script mesure la PROPORTION. Le contraste d'une page construite est celui de "
          "audit_html.py ; il ne remplace ni l'œil ni la capture.")
    return 1 if (fails or (a.strict and warns)) else 0


if __name__ == "__main__":
    sys.exit(main())
