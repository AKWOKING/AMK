# -*- coding: utf-8 -*-
"""audit_hero.py — le contrôle du PREMIER ÉCRAN, appris le 24/09/2026.

    python3 tools/qa/audit_hero.py site/index.html demos/*.html        # rapport
    python3 tools/qa/audit_hero.py --strict pages…                     # rc=1 si un défaut franc

D'où viennent ces règles (lot [26] de `research/YouTube-Lessons.md`) :

  · **Deux tutoriels de code-along** (UI UNIVERSITY) enseignent un HERO spectaculaire et livrent du
    code qui échoue à nos propres règles. Dans les deux dépôts, lus ligne à ligne :
      – `h1::before{content:'The'}` / `::after{content:'Agency'}` : **des mots réels écrits dans une
        pseudo-classe CSS**. Invisibles pour un lecteur d'écran, ignorés par Google, introuvables par
        Ctrl+F — le titre visible n'est pas dans le document. C'est le défaut le plus grave des deux,
        parce qu'il est silencieux.
      – `height:100vh` + un titre à 180 px / 222 px en position absolue + **zéro `@media`** : la page
        est magnifique sur l'écran de celui qui l'a faite et cassée sur un téléphone.
      – Des animations en `@keyframes` sur `bottom` (une propriété de MISE EN PAGE) sans
        `prefers-reduced-motion`.
  · **Deux vidéos de Payton Clark Smith** sur les heros (39 mises en page au total) donnent la
    grammaire : texte à gauche par défaut, image à droite (la gauche se lit en premier) ; une image
    coupée par le pli fait descendre ; centrer seulement avec peu de texte ; **jamais de texte posé
    sur une photo** (« old school », illisible) ; le hamburger sur ordinateur est presque toujours une
    faute : il cache la navigation à quelqu'un qui a la place de la voir.

Ce que cet outil ne fait pas : il ne juge pas le goût. Il refuse ce qui est mécaniquement vérifiable,
et il SIGNALE, sans trancher, ce qui demande un œil (texte sur une photo de fond).
"""
import io, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# une pseudo-classe qui écrit des MOTS ne contient que des lettres, espaces, tirets, apostrophes
WORDY_CONTENT = re.compile(r"::?(?:before|after)\s*\{[^}]*content\s*:\s*['\"]([^'\"]{2,})['\"]", re.I)
CONTENT_PROP = re.compile(r"content\s*:\s*['\"]([^'\"]*)['\"]", re.I)
HAS_JUNK = re.compile(r"^[\s\-\u2022•·|/\\_\.]*$")          # séparateurs : c'est légitime, pas un mot
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}|lorem ipsum|dolor sit amet", re.I)
VH_HERO = re.compile(r"height\s*:\s*100(?:vh|dvh|svh)", re.I)
ABS_BIG_TYPE = re.compile(r"font-size\s*:\s*(1[2-9]\d|2\d\d)px", re.I)
MEDIA = re.compile(r"@media", re.I)
REDUCED = re.compile(r"prefers-reduced-motion", re.I)
KEYFRAMES_ON_LAYOUT = re.compile(
    r"@keyframes\s+[\w-]+\s*\{[^}]*(?:top|bottom|left|right|width|height|margin)\s*:", re.I | re.S)


def css_of(html):
    """Le CSS de la page : ses blocs <style> et ses feuilles liées si elles sont dans le dépôt."""
    parts = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', html, re.I):
        if href.startswith(("http://", "https://", "//")):
            continue
        p = ROOT / href.lstrip("/")
        if p.exists():
            parts.append(io.open(p, encoding="utf-8", errors="replace").read())
    return "\n".join(parts)


def hero_of(html):
    """Le premier écran : la section qui se donne pour telle, sinon le premier <section>."""
    m = re.search(r"<(?:section|header)[^>]*class=[\"'][^\"']*\b(?:hero|banner|top)\b[^\"']*[\"'][^>]*>(.*?)</(?:section|header)>",
                  html, re.S | re.I)
    return m.group(1) if m else ""


def audit(path):
    html = io.open(path, encoding="utf-8", errors="replace").read()
    css = css_of(html)
    hero = hero_of(html)
    findings = []

    # 1 · des mots réels dans le CSS (la faute silencieuse des deux tutoriels)
    words = [w.strip() for w in WORDY_CONTENT.findall(css)]
    real = [w for w in words if not HAS_JUNK.match(w) and not w.startswith("\\")]
    if real:
        findings.append(("ERR", "des mots réels vivent dans le CSS (invisibles au lecteur d'écran, "
                                "à Google et à Ctrl+F) : " + " · ".join(sorted(set(real))[:4])))

    # 2 · des gabarits non remplis, à la racine du fichier livré
    if PLACEHOLDER.search(hero or html[:4000]):
        findings.append(("ERR", "texte de gabarit non rempli dans le premier écran ({{…}} ou lorem ipsum)"))

    # 3 · le hero en 100vh avec un titre géant en pixels et aucune requête média
    if VH_HERO.search(css) and ABS_BIG_TYPE.search(css) and not MEDIA.search(css):
        findings.append(("ERR", "hero en 100vh, titre en pixels fixes, AUCUN @media : bon sur l'écran "
                                "de celui qui l'a fait, cassé sur un téléphone"))

    # 4 · une animation de mise en page (coûteuse) animée sans respect de reduced-motion
    if KEYFRAMES_ON_LAYOUT.search(css) and not REDUCED.search(css):
        findings.append(("WARN", "une animation déplace top/bottom/width (mise en page, coûteuse en "
                                 "batterie) et la page ignore prefers-reduced-motion"))

    # 5 · du texte posé sur une photo : on ne juge pas, on demande l'œil
    if re.search(r"background-image\s*:\s*url\(", css, re.I) and hero and not re.search(r"<img", hero):
        findings.append(("INFO", "le premier écran est un fond photo sans <img> dans le HTML — vérifier "
                                 "à l'œil que le texte reste lisible en plein soleil"))

    # 6 · ce qui est déjà bien, et qu'on veut voir écrit noir sur blanc
    goods = []
    if hero and re.search(r"<h1", hero, re.I):
        goods.append("h1 dans le premier écran")
    if hero and not re.search(r"data-risk|bg-photo", hero):
        goods.append("premier écran porté par le texte")
    if re.search(r"<details", html, re.I):
        goods.append("accordéons natifs")
    good = " · ".join(goods)

    return findings, good


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if not args:
        print(__doc__); sys.exit(2)

    errs = warns = 0
    for path in args:
        p = pathlib.Path(path)
        if not p.exists():
            print("  ? %s — introuvable" % path); continue
        findings, good = audit(p)
        errs += sum(1 for lvl, _ in findings if lvl == "ERR")
        warns += sum(1 for lvl, _ in findings if lvl == "WARN")
        head = "✗" if any(l == "ERR" for l, _ in findings) else ("!" if findings else "✓")
        print("%s %s%s" % (head, path, ("  — " + good) if good else ""))
        for lvl, msg in findings:
            print("     %-4s %s" % (lvl, msg))

    print("\n%d faute(s) franche(s) · %d avertissement(s)" % (errs, warns))
    if strict and errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
