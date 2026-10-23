# -*- coding: utf-8 -*-
"""Visuels de la page Facebook AMK — générés depuis les fichiers de marque, pas à la main.

Trois sorties (hors dépôt de publication, mais versionnées : ce sont des actifs de marque) :

  brand/facebook/profile-1024.png       photo de profil : la marque SEULE, sans le mot « AMK »
                                        (Facebook affiche déjà le nom de la page ; à 40 px,
                                        un motmark devient une tache)
  brand/facebook/cover-1640x624.png     couverture. Tout le contenu tient dans la zone
                                        centrale **820 × 312** : le mobile recadre en ~2:1
                                        et rien d'important ne doit être sur les bords
  brand/facebook/cover-mobile-820x312.png  le recadrage mobile, pour vérification à l'œil

Règles respectées (brand/AMK-PRESENCE-2026-10-22.md §3 et §9.2) :
  • aucun prix, aucun délai promis (pas de « 3–5 jours », pas de « live in ») ;
  • aucune photo de client, aucun site fictif présenté comme un portfolio —
    la couverture est typographique tant qu'il n'y a pas de site livré avec accord ;
  • le slogan banni « Solutions Digitales » (§11b) n'apparaît nulle part.

Usage :  python3 brand/build_fb_assets.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
OUT = HERE / "facebook"
FONTS = HERE.parent / "tools" / "record" / "fonts"
SRC = HERE / "AMK-logo-square.png"

NAVY = (15, 23, 42)
NAVY2 = (30, 41, 59)
AMBER = (245, 158, 11)
AMBER_L = (252, 211, 77)
WHITE = (255, 255, 255)
SLATE = (148, 163, 184)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def centered(d, y, text, f, fill, W):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


def build_profile():
    """1024 × 1024, la marque seule, centrée, sur le navy de la charte."""
    logo = Image.open(SRC).convert("RGBA")
    # la marque (cercle + triangle) occupe le haut du logo carré ; le mot « AMK » est en dessous
    # Boîte englobante mesurée dans le fichier, pas devinée : les pixels ambre de la marque
    # occupent x 166–345, y 100–283. On recadre avec 8 px d'air, et on VÉRIFIE que la boîte est
    # bien carrée — un recadrage raté déforme ou rogne le logo (deux essais perdus le 22/10).
    mark = logo.crop((158, 92, 353, 291))
    assert abs(mark.width - mark.height) <= 12, f"boîte non carrée : {mark.size}"
    scale = 620 / mark.height
    mark = mark.resize((int(mark.width * scale), int(mark.height * scale)), Image.LANCZOS)

    img = Image.new("RGB", (1024, 1024), NAVY)
    # centrage optique : la marque est un triangle dans un cercle, donc plus lourde en bas
    img.paste(mark, ((1024 - mark.width) // 2, (1024 - mark.height) // 2 - 6), mark)
    out = OUT / "profile-1024.png"
    img.save(out, "PNG", optimize=True)

    # contrôle : ce que ça donne à 40 px (le vrai test d'une photo de profil)
    img.resize((40, 40), Image.LANCZOS).resize((160, 160), Image.NEAREST).save(
        OUT / "profile-preview-40px.png")
    return out


def build_cover():
    """1640 × 624 — tout le texte dans la zone centrale 820 × 312, vérifié par calcul."""
    W, H = 1640, 624
    SAFE = (410, 156, 1230, 468)          # zone visible sur téléphone (recadrage ~2:1)
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # deux filets ambre : ils tiennent le cadre même quand le mobile recadre
    d.rectangle((0, 0, W, 6), fill=AMBER)
    d.rectangle((0, H - 6, W, H), fill=AMBER)

    f1 = font("OpenSans-Bold.ttf", 46)     # 755 px de large : tient dans 820
    f2 = font("OpenSans-Regular.ttf", 25)
    f3 = font("OpenSans-Bold.ttf", 22)

    lines = [
        (206, "Sites web pour écoles & cliniques", f1, WHITE),
        (274, "Bilingues FR | EN · pensés pour être trouvés sur Google", f2, AMBER_L),
        (330, "Aperçu gratuit, envoyé sur WhatsApp · Douala, Cameroun", f2, SLATE),
    ]
    drawn = []
    for y, text, f, fill in lines:
        centered(d, y, text, f, fill, W)
        w = d.textlength(text, font=f)
        drawn.append((text, (W - w) / 2, (W + w) / 2, y, ""))

    # petit soulignement ambre sous le titre : la marque, sans bruit
    d.rectangle((W / 2 - 46, 272, W / 2 + 46, 276), fill=AMBER)  # sous la ligne de base du titre

    # pastille d'adresse, centrée
    label = "amk-cm.vercel.app"
    tw = d.textlength(label, font=f3)
    bx0 = (W - tw) / 2 - 22
    d.rounded_rectangle((bx0, 392, bx0 + tw + 44, 442), radius=25, outline=NAVY2, width=2)
    d.text(((W - tw) / 2, 402), label, font=f3, fill=WHITE)
    drawn.append((label, bx0, bx0 + tw + 44, 392, ""))

    # contrôle bloquant : rien ne doit toucher le bord de la zone sûre
    for text, x0, x1, y0, _ in drawn:
        assert SAFE[0] + 8 <= x0 and x1 <= SAFE[2] - 8, f"trop large : {text}"
        assert SAFE[1] + 8 <= y0 and y0 + 52 <= SAFE[3] - 8, f"trop haut/bas : {text}"

    out = OUT / "cover-1640x624.png"
    img.save(out, "PNG", optimize=True)

    # le recadrage mobile : ce que voit un visiteur sur téléphone
    img.crop(SAFE).save(OUT / "cover-mobile-820x312.png")
    return out


def build_square_post():
    """1080 × 1080 — la première pièce d'Instagram (et la couverture d'un TikTok).

    Même grammaire que la couverture : navy, deux filets ambre, titre blanc, sous-titre ambre,
    pastille du domaine. Aucun prix, aucun délai, aucun site fictif.
    """
    S = 1080
    MARGIN = 96                                   # zone sûre : un carré IG garde tout le centre
    img = Image.new("RGB", (S, S), NAVY)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, S, 8), fill=AMBER)
    d.rectangle((0, S - 8, S, S), fill=AMBER)

    f1 = font("OpenSans-Bold.ttf", 78)
    f2 = font("OpenSans-Regular.ttf", 34)
    f3 = font("OpenSans-Bold.ttf", 30)

    drawn = []

    def line(y, text, f, fill):
        centered(d, y, text, f, fill, S)
        w = d.textlength(text, font=f)
        drawn.append((text, (S - w) / 2, (S + w) / 2, y))
        return w

    line(300, "Sites web pour", f1, WHITE)
    w2 = line(396, "écoles & cliniques", f1, WHITE)
    # le soulignement ambre souligne la DEUXIÈME ligne, mesurée, jamais devinée
    d.rectangle((S / 2 - w2 / 2, 500, S / 2 + w2 / 2, 506), fill=AMBER)
    line(540, "Bilingues FR | EN · Douala, Cameroun", f2, AMBER_L)
    line(600, "Aperçu gratuit, envoyé sur WhatsApp", f2, SLATE)

    label = "amk-cm.vercel.app"
    tw = d.textlength(label, font=f3)
    bx0 = (S - tw) / 2 - 26
    d.rounded_rectangle((bx0, 726, bx0 + tw + 52, 786), radius=30, outline=NAVY2, width=3)
    d.text(((S - tw) / 2, 738), label, font=f3, fill=WHITE)
    drawn.append((label, bx0, bx0 + tw + 52, 726))

    for text, x0, x1, y0 in drawn:
        assert MARGIN <= x0 and x1 <= S - MARGIN, f"trop large : {text}"
        assert MARGIN <= y0 and y0 + 80 <= S - MARGIN, f"trop haut/bas : {text}"

    out = OUT / "post-square-1080.png"
    img.save(out, "PNG", optimize=True)
    return out


def build_vertical():
    """1080 × 1920 — la version TikTok / Reels / Stories du carré (§14.7).

    TikTok pose son interface PAR-DESSUS la vidéo : à droite (boutons) et en bas (légende).
    Tout le contenu utile reste donc dans x 72–1008 et y 260–1420, et le nom d'utilisateur
    est placé DANS cette zone — sinon il est caché par les boutons.
    """
    W, H = 1080, 1920
    SAFE = (72, 260, 1008, 1420)
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 8), fill=AMBER)
    d.rectangle((0, H - 8, W, H), fill=AMBER)

    f1 = font("OpenSans-Bold.ttf", 92)
    f2 = font("OpenSans-Regular.ttf", 38)
    f3 = font("OpenSans-Bold.ttf", 34)

    drawn = []

    def line(y, text, f, fill):
        centered(d, y, text, f, fill, W)
        w = d.textlength(text, font=f)
        drawn.append((text, (W - w) / 2, (W + w) / 2, y))
        return w

    line(520, "Sites web pour", f1, WHITE)
    w2 = line(636, "écoles & cliniques", f1, WHITE)
    d.rectangle((W / 2 - w2 / 2, 760, W / 2 + w2 / 2, 768), fill=AMBER)
    line(812, "Bilingues FR | EN · Douala, Cameroun", f2, AMBER_L)
    line(878, "Aperçu gratuit, envoyé sur WhatsApp", f2, SLATE)

    handle = "@amkweb"
    tw = d.textlength(handle, font=f3)
    bx0 = (W - tw) / 2 - 30
    d.rounded_rectangle((bx0, 1040, bx0 + tw + 60, 1108), radius=34, outline=NAVY2, width=3)
    d.text(((W - tw) / 2, 1054), handle, font=f3, fill=WHITE)
    drawn.append((handle, bx0, bx0 + tw + 60, 1040))

    for text, x0, x1, y0 in drawn:
        assert SAFE[0] <= x0 and x1 <= SAFE[2], f"trop large : {text}"
        assert SAFE[1] <= y0 and y0 + 100 <= SAFE[3], f"trop haut/bas : {text}"

    out = OUT / "post-vertical-1080x1920.png"
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for p in (build_profile(), build_cover(), build_square_post(), build_vertical()):
        print("wrote", p, round(p.stat().st_size / 1024), "KB")
