# -*- coding: utf-8 -*-
"""audit_a11y.py — le contrôle d'ACCESSIBILITÉ des pages AMK, critère par critère (WCAG 2.2 niveau AA).

    python3 tools/qa/audit_a11y.py site/*.html demos/concept-*.html      # rapport
    python3 tools/qa/audit_a11y.py --strict pages…                       # rc=1 si un défaut de niveau A ou AA

POURQUOI CET OUTIL, ET POURQUOI MAINTENANT (lot [27], 24/09/2026).
Sources lues ce matin : la spécification W3C **WCAG 2.1** (Recommandation), le **quickref WCAG 2.2**,
les deux guides MDN (*Keyboard accessible*, *Text labels and names*), la vidéo de Silktide (« A c'est
à faire, AA c'est à faire aussi, AAA c'est viser la lune »), et le **cours d'audit en 55 vidéos
d'Accessible Web** — une vidéo par critère de succès, ce qui donne la FORME d'un audit : on passe les
critères un par un, dans l'ordre, et on écrit ce qu'on a vérifié.

Ce que cet outil fait : la part **vérifiable en code**, avec le numéro du critère à côté de chaque
constat — pour qu'une phrase comme « 1.4.4 Resize Text » veuille dire quelque chose dans un rapport.
Ce qu'il ne fait pas, et qui est écrit ici pour ne pas mentir : le contraste (c'est `audit_html.py`),
le rendu réel, l'ordre de tabulation au clavier, la qualité d'un texte alternatif. **Ces quatre-là
demandent un humain** (et King reste l'œil).

Ce qu'on vise : **WCAG 2.2 niveau AA**. Pas AAA (Silktide : « reaching for the stars ») — AAA demande
des choses qu'une page commerciale ne peut pas honorer (langue des signes, 7:1 partout, 44 px partout).
AA, c'est le niveau qu'une loi ou un appel d'offres exige.
"""
import io, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# ── ce que « AA » veut dire pour nous, et ce que cet outil sait vérifier ───────────────────────────
GENERIC_LINK_TEXT = re.compile(
    r"^\s*(ici|cliquez ici|cliquer ici|en savoir plus|lire la suite|plus|détails|détail|voir|"
    r"voir plus|learn more|read more|more|here|click here|details|see more|link)\s*$", re.I)
FILENAME_ALT = re.compile(r"^[\w\-.]+\.(jpe?g|png|gif|webp|svg|avif)$", re.I)
VAGUE_ALT = re.compile(r"^\s*(image|photo|picture|img|logo|banner|illustration)\s*\d*\s*$", re.I)
NO_ZOOM = re.compile(r"(user-scalable\s*=\s*no|maximum-scale\s*=\s*1(\.0)?\b)", re.I)
OUTLINE_KILL = re.compile(r"outline\s*:\s*(none|0)\b", re.I)
# LA RÈGLE QUI TUE LE FOCUS COMPTE-T-ELLE COMME SON REMPLACEMENT ? Non — et c'est le premier bug de
# logique trouvé par le test : `a:focus{outline:none}` satisfaisait « il y a une règle :focus ». Ce qu'on
# cherche, c'est un `outline` NON nul (ou une ombre) sur un état de focus : quelque chose qui SE VOIT.
FOCUS_REPLACEMENT = re.compile(
    r":focus(-visible|-within)?[^{]*\{[^}]*(?:outline\s*:\s*(?!none|0(?:px)?\b)\S|box-shadow\s*:\s*(?!none)\S)",
    re.I)
CLICK_ON_NONINTERACTIVE = re.compile(r"<(div|span|li|section|p)\b[^>]*\bonclick\s*=", re.I)
INFINITE_ANIM = re.compile(r"animation[^;]*\binfinite\b", re.I)
REDUCED_MOTION = re.compile(r"prefers-reduced-motion", re.I)
HOVER_ONLY = re.compile(r":hover\b[^{]*\{[^}]*(display\s*:\s*(block|flex|grid|inline)|visibility\s*:\s*visible)", re.I)
FIXED_BAR = re.compile(r"position\s*:\s*fixed", re.I)
LIVE_REGION = re.compile(r'role\s*=\s*["\'](status|alert)["\']|aria-live\s*=', re.I)
ARIA_INVALID_EMPTY = re.compile(r'aria-(label|labelledby)\s*=\s*["\']\s*["\']', re.I)


def text_of(html):
    """Le texte visible approximatif — pour ne pas confondre un lien vide et un lien qui a un mot."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def accessible_name_of_tag(open_tag, inner=""):
    """Le nom accessible approximatif d'un <a>/<button> : ses attributs PUIS son contenu.

    `open_tag` est la balise ouvrante entière (c'est là que vivent aria-label et title) ; `inner` est ce
    qu'il y a dedans. Les deux comptent : un bouton-icône tient son nom de son aria-label, un bouton de
    texte le tient de son contenu. Les vérifier séparément produit de faux positifs — constaté à la
    première exécution, corrigé ici."""
    for attr in ("aria-label", "title"):
        m = re.search(r'%s\s*=\s*["\']([^"\']+)["\']' % attr, open_tag, re.I)
        if m and m.group(1).strip():
            return m.group(1).strip()
    if re.search(r'aria-labelledby\s*=\s*["\'][^"\']+["\']', open_tag, re.I):
        return "(nommé par aria-labelledby)"
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner)).strip()
    return text


def audit(path):
    html = io.open(path, encoding="utf-8", errors="replace").read()
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', html, re.I):
        if not href.startswith(("http", "//")) and (ROOT / href.lstrip("/")).exists():
            css += "\n" + io.open(ROOT / href.lstrip("/"), encoding="utf-8", errors="replace").read()
    F = []          # constats : (niveau, critère, message)
    OK = []         # ce qui est vérifié et conforme, avec le critère

    def add(level, sc, msg):
        F.append((level, sc, msg))

    def good(sc, msg):
        OK.append((sc, msg))

    # ── 1.1.1 Non-text Content ────────────────────────────────────────────────────────────────────
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    no_alt = [i for i in imgs if not re.search(r"\balt\s*=", i, re.I)]
    bad_alt = [i for i in imgs
               if (m := re.search(r'\balt\s*=\s*["\']([^"\']*)["\']', i, re.I))
               and (FILENAME_ALT.match(m.group(1)) or VAGUE_ALT.match(m.group(1)))]
    if no_alt:
        add("ERR", "1.1.1", "%d image(s) sans attribut alt" % len(no_alt))
    if bad_alt:
        add("ERR", "1.1.1", "%d image(s) dont l'alt est un nom de fichier ou un mot vide (ex. « %s »)"
            % (len(bad_alt), re.search(r'alt\s*=\s*["\']([^"\']*)["\']', bad_alt[0], re.I).group(1)))
    if imgs and not no_alt and not bad_alt:
        good("1.1.1", "les %d images ont un alt qui décrit" % len(imgs))
    # les images décoratives doivent être ignorables : alt="" est la bonne réponse
    svgs = re.findall(r"<svg\b[^>]*>", html, re.I)
    svg_named = [s for s in svgs if re.search(r'role\s*=\s*["\']img["\']', s, re.I)
                 and re.search(r'aria-label(ledby)?\s*=', s, re.I)]
    svg_hidden = [s for s in svgs if re.search(r'aria-hidden\s*=\s*["\']true["\']', s, re.I)]
    if svgs and len(svg_named) + len(svg_hidden) < len(svgs):
        add("WARN", "1.1.1", "%d <svg> sans nom accessible ni aria-hidden (icône décorative ou image ?)"
            % (len(svgs) - len(svg_named) - len(svg_hidden)))
    if ARIA_INVALID_EMPTY.search(html):
        add("ERR", "4.1.2", "un aria-label / aria-labelledby est VIDE — il ne nomme rien")

    # ── 1.3.1 Info and Relationships ──────────────────────────────────────────────────────────────
    levels = [int(m.group(1)) for m in re.finditer(r"<h([1-6])\b", html, re.I)]
    if levels:
        if levels.count(1) != 1:
            add("ERR", "1.3.1", "%d titre(s) de niveau 1 (il en faut exactement un)" % levels.count(1))
        else:
            good("1.3.1", "un seul h1")
        skip = [(a, b) for a, b in zip(levels, levels[1:]) if b - a > 1]
        if skip:
            add("WARN", "1.3.1", "saut de niveau dans les titres : h%d puis h%d" % skip[0])
    else:
        add("ERR", "1.3.1", "aucun titre dans la page")

    inputs = re.findall(r"<(?:input|select|textarea)\b[^>]*>", html, re.I)
    unlabeled = []
    for tag in inputs:
        t = (re.search(r'type\s*=\s*["\']([^"\']+)["\']', tag, re.I) or [None, "text"])[1].lower()
        if t in ("hidden", "submit", "button", "reset", "image"):
            continue
        i = re.search(r'id\s*=\s*["\']([^"\']+)["\']', tag, re.I)
        named = re.search(r'aria-label(ledby)?\s*=\s*["\'][^"\']+["\']', tag, re.I)
        labelled = bool(i) and bool(re.search(r'<label[^>]+for\s*=\s*["\']%s["\']' % re.escape(i.group(1)), html, re.I))
        wrapped = bool(re.search(r"<label[^>]*>(?:(?!</label>).)*" + re.escape(tag[:40]), html, re.S | re.I))
        if not (named or labelled or wrapped):
            unlabeled.append(tag[:80])
    if unlabeled:
        add("ERR", "3.3.2", "%d champ(s) sans étiquette associée (ni <label for>, ni aria-label)" % len(unlabeled))
    elif inputs:
        good("3.3.2", "les %d champs de saisie ont une étiquette" % len(inputs))

    if re.search(r'type\s*=\s*["\'](radio|checkbox)["\']', html, re.I) and "<fieldset" not in html.lower():
        add("WARN", "1.3.1", "des cases/radios sans <fieldset><legend> : le groupe n'est pas nommé")

    # ── 1.3.5 Identify Input Purpose ──────────────────────────────────────────────────────────────
    # 1.3.5 ne vise QUE les champs qui collectent une donnée dont le sens est connu (nom, e-mail,
    # téléphone…). Un champ de texte libre n'a pas d'autocomplete à déclarer : le réclamer serait un
    # faux positif de plus.
    KNOWN = r"(nom|name|prenom|first|last|email|mail|tel|phone|adresse|address|ville|city|cp|zip|societe|company|organisation|organization)"
    need_autocomplete = [t for t in inputs
                         if re.search(r'(id|name)\s*=\s*["\'][^"\']*%s' % KNOWN, t, re.I)
                         and not re.search(r"autocomplete\s*=", t, re.I)]
    if need_autocomplete:
        add("WARN", "1.3.5", "%d champ(s) de saisie sans autocomplete (le navigateur ne peut pas aider)"
            % len(need_autocomplete))

    # ── 1.4.4 Resize Text — le zoom ne doit JAMAIS être bloqué ────────────────────────────────────
    if NO_ZOOM.search(html):
        add("ERR", "1.4.4", "le viewport interdit le zoom (user-scalable=no / maximum-scale)")

    # ── 1.4.10 Reflow — une page doit tenir à 320 px sans défilement horizontal ───────────────────
    fixed_wide = re.findall(r"width\s*:\s*(\d{4,})px", css)
    if fixed_wide and not re.search(r"@media", css, re.I):
        add("WARN", "1.4.10", "des largeurs fixes en pixels (%s px) sans aucune requête média" % fixed_wide[0])

    # ── 2.1.1 Keyboard ────────────────────────────────────────────────────────────────────────────
    if CLICK_ON_NONINTERACTIVE.search(html):
        el = CLICK_ON_NONINTERACTIVE.search(html)
        add("ERR", "2.1.1", "un élément non interactif porte un onclick (inutilisable au clavier) : %s…"
            % el.group(0)[:40])
    positives = re.findall(r'tabindex\s*=\s*["\']([1-9]\d*)["\']', html)
    if positives:
        add("ERR", "2.4.3", "tabindex positif (%s) : l'ordre de tabulation ne suit plus la page"
            % ", ".join(positives[:3]))

    # ── 2.2.2 Pause, Stop, Hide ───────────────────────────────────────────────────────────────────
    if INFINITE_ANIM.search(css) and not REDUCED_MOTION.search(css):
        add("ERR", "2.2.2", "animation infinie sans prefers-reduced-motion : impossible à mettre en pause")

    # ── 2.4.1 Bypass Blocks ───────────────────────────────────────────────────────────────────────
    if re.search(r'<a[^>]+href\s*=\s*["\']#', html, re.I) and re.search(r"skip|aller au contenu|passer", html, re.I):
        good("2.4.1", "un lien d'évitement existe")
    elif "<main" in html.lower() and "<nav" in html.lower():
        add("WARN", "2.4.1", "pas de lien d'évitement (le contenu principal et la navigation existent)")

    # ── 2.4.2 Page Titled ─────────────────────────────────────────────────────────────────────────
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    if not m or len(m.group(1).strip()) < 10:
        add("ERR", "2.4.2", "titre de page absent ou trop court")

    # ── 2.4.4 Link Purpose (In Context) ───────────────────────────────────────────────────────────
    anchors = re.findall(r"<a\b([^>]*)>(.*?)</a>", html, re.S | re.I)
    generic = [inner for _tag, inner in anchors if GENERIC_LINK_TEXT.match(re.sub(r"<[^>]+>", " ", inner))]
    if generic:
        add("WARN", "2.4.4", "%d lien(s) au libellé générique (« %s ») : hors contexte, on ne sait pas où ils mènent"
            % (len(generic), re.sub(r"<[^>]+>", " ", generic[0]).strip()[:20]))
    empty_links = [(tag, inner) for tag, inner in anchors if not accessible_name_of_tag(tag, inner)]
    if empty_links:
        add("ERR", "2.4.4", "%d lien(s) sans AUCUN nom accessible" % len(empty_links))

    # ── 2.4.7 Focus Visible ───────────────────────────────────────────────────────────────────────
    if OUTLINE_KILL.search(css) and not FOCUS_REPLACEMENT.search(css):
        add("ERR", "2.4.7", "outline:none sans remplacement : le focus clavier devient invisible")
    elif FOCUS_REPLACEMENT.search(css):
        good("2.4.7", "un style de focus est défini")

    # ── 2.4.11 Focus Not Obscured (Minimum) — WCAG 2.2 AA ─────────────────────────────────────────
    if FIXED_BAR.search(css):
        add("INFO", "2.4.11", "barre fixe détectée : vérifier à l'œil qu'aucun élément focalisé ne passe dessous")

    # ── 2.5.8 Target Size (Minimum) — WCAG 2.2 AA : 24 × 24 px ────────────────────────────────────
    tiny = []
    for rule in re.findall(r"([^{}]{1,200})\{([^{}]*)\}", css):
        sel, body = rule[0].strip(), rule[1]
        if not re.search(r"(^|[\s,>+~.])(a|button|input|select|textarea|\.btn|\.chip|\.tab|link)", sel, re.I):
            continue
        for v in re.findall(r"min-height\s*:\s*(\d+)px", body):
            if int(v) < 24:
                tiny.append(v)
    if tiny:
        add("WARN", "2.5.8", "une cible mesure moins de 24 px dans le CSS (%s px)" % tiny[0])

    # ── 3.1.1 Language of Page ────────────────────────────────────────────────────────────────────
    lang = re.search(r'<html[^>]*\blang\s*=\s*["\']([^"\']+)["\']', html, re.I)
    if not lang:
        add("ERR", "3.1.1", "pas de lang sur <html> : la synthèse vocale ne sait pas dans quelle langue lire")
    elif not re.match(r"^[a-z]{2}(-[A-Za-z]{2,4})?$", lang.group(1)):
        add("WARN", "3.1.1", "lang peu lisible : « %s »" % lang.group(1))
    else:
        good("3.1.1", "lang=\"%s\"" % lang.group(1))
    # les passages dans l'AUTRE langue doivent être marqués
    if 'class="en-only"' in html or 'class="fr-only"' in html:
        add("INFO", "3.1.2", "page bilingue : les passages de l'autre langue sont-ils marqués par lang= ?")

    # ── 1.4.13 Content on Hover or Focus ──────────────────────────────────────────────────────────
    if HOVER_ONLY.search(css) and not re.search(r":focus(-within)?\b[^{]*\{[^}]*(display|visibility)", css, re.I):
        add("WARN", "1.4.13", "du contenu apparaît au survol sans équivalent au clavier (:focus)")

    # ── 3.3.1 / 3.3.3 Error Identification and Suggestion ─────────────────────────────────────────
    if "<form" in html.lower():
        if LIVE_REGION.search(html):
            good("3.3.1", "une zone vivante annonce les messages")
        else:
            add("WARN", "3.3.1", "un formulaire sans zone vivante (role=status/alert) : l'erreur peut passer inaperçue")

    # ── 4.1.2 Name, Role, Value ───────────────────────────────────────────────────────────────────
    buttons = re.findall(r"<button\b([^>]*)>(.*?)</button>", html, re.S | re.I)
    unnamed = [(t, i) for t, i in buttons if not accessible_name_of_tag(t, i)]
    if unnamed:
        add("ERR", "4.1.2", "%d bouton(s) sans nom accessible (icône seule)" % len(unnamed))
    elif buttons:
        good("4.1.2", "les %d boutons ont un nom" % len(buttons))
    # une icône dans un lien de texte ne doit pas doubler la lecture
    icon_in_named_anchor = 0
    for tag, inner in anchors:
        if "<svg" in inner and not re.search(r'aria-hidden\s*=\s*["\']true["\']', inner, re.I):
            # l'icône n'est un problème que si elle n'est pas déjà couverte par un nom explicite
            if not re.search(r'aria-label(ledby)?\s*=', tag, re.I):
                icon_in_named_anchor += 1
    if icon_in_named_anchor:
        add("WARN", "1.1.1", "%d lien(s) : une icône <svg> non marquée aria-hidden et aucun nom explicite "
                              "sur le lien — le lecteur d'écran annonce « image »" % icon_in_named_anchor)

    return F, OK


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
        F, OK = audit(p)
        errs += sum(1 for l, _, _ in F if l == "ERR")
        warns += sum(1 for l, _, _ in F if l == "WARN")
        head = "✗" if any(l == "ERR" for l, _, _ in F) else ("!" if F else "✓")
        print("%s %s" % (head, path))
        for sc, msg in OK:
            print("     ok   [%s] %s" % (sc, msg))
        for lvl, sc, msg in F:
            print("     %-4s [%s] %s" % (lvl, sc, msg))
    print("\n%d faute(s) de niveau A/AA · %d avertissement(s)" % (errs, warns))
    print("non vérifiable ici, et assumé : contraste (voir audit_html.py), ordre de tabulation réel,\n"
          "rendu à 200 % de zoom, qualité d'un texte alternatif — ces quatre-là demandent un humain.")
    if strict and errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
