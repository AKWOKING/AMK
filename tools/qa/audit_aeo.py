# -*- coding: utf-8 -*-
"""audit_aeo.py — le portique AEO : ce qu'une machine peut vérifier de la visibilité dans les réponses IA.

    python3 tools/qa/audit_aeo.py site/*.html hosting/previews/*/index.html     # rapport
    python3 tools/qa/audit_aeo.py --strict pages…                              # rc=1 si un défaut

POURQUOI CET OUTIL (lot [31], 24/09/2026).
Source principale : la vidéo d'Ahrefs « Learn 80 % of AEO in 19 Minutes » (679 K abonnés, recherche
maison sur 174 000 pages citées dans les AI Overviews et 75 000 marques). Sa règle la plus utile n'est pas
une technique, c'est un avertissement : **5,9 % des sites bloquent GPTBot sans le savoir**, parce qu'ils
héritent d'un `robots.txt` ou d'un Cloudflare configuré par défaut. Un site bloqué ne peut pas être cité —
et personne ne le voit dans ses statistiques, puisqu'il n'y a rien à mesurer.

Ce que cet outil vérifie, et pourquoi seulement ça :

  1. **Aucun robot IA n'est bloqué** (`robots.txt` + `<meta name="robots">`). C'est le seul point
     purement mécanique et entièrement réparable.
  2. **Le `noindex` de nos pages de travail est VOULU, et rappelé à chaque exécution.** Nos onze copies
     hébergées portent `noindex,nofollow` : c'est correct tant qu'elles ne sont pas le site du client, et
     c'est un piège le jour où l'une d'elles devient publique. L'outil distingue `site/` (public) de
     `demos/` et `hosting/previews/` (travail) — et **imprime la liste des pages à débloquer** au lieu de
     compter sur ma mémoire.
  3. **Les données structurées existent** (JSON-LD : `LocalBusiness`, `MedicalLaboratory`, `FAQPage`…).
     Ahrefs appelle ça l'écriture « riche en entités » : AI a besoin de relations nommées, pas d'adjectifs.
  4. **La page porte des questions et des réponses**, pas seulement des affirmations.

Ce que cet outil NE PEUT PAS vérifier, et qui est imprimé à chaque exécution pour ne pas mentir : la
**consensus** (être nommé sur les pages des autres — la corrélation la plus forte avec la visibilité IA,
et ça ne se mesure pas depuis un fichier HTML), la **fraîcheur** réelle, la présence **YouTube**, la
qualité d'écriture (BLUF, phrases déclaratives), et le fait d'être cité ou non par une IA. Ces cinq-là
demandent un travail humain, et nous n'avons ni les données ni le droit de les promettre à un client.
"""
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

# Les robots dont le blocage empêche une citation par un assistant. Liste issue de la vidéo d'Ahrefs
# (GPTBot, OAI-SearchBot, ClaudeBot, Google-Extended) complétée des autres indexeurs IA connus.
AI_BOTS = ["gptbot", "chatgpt-user", "oai-searchbot", "claudebot", "anthropic-ai", "claude-web",
           "perplexitybot", "google-extended", "ccbot", "applebot-extended", "bytespider",
           "meta-externalagent"]
# Ce qui est PUBLIÉ (donc doit être indexable) contre ce qui est du TRAVAIL (donc `noindex` attendu).
# Un seul dossier est public chez nous : `site/`, la vitrine déployée. `demos/`, `hosting/previews/`,
# `hosting/samples/`, `content/studio/` et `sales/walkin/` sont des pages de travail — et une page
# passée depuis l'extérieur du dépôt est traitée comme PUBLIQUE : c'est le cas conservateur, celui qui
# fait mordre les témoins de test et qui n'excuse rien.
PUBLIC_DIRS = ("site",)
WORK_DIRS = ("demos", "hosting/previews", "hosting/samples", "content/studio", "sales/walkin")


def is_public(path):
    """Publique si la page vit dans `site/`, ou si elle vient d'ailleurs que du dépôt."""
    try:
        rel = path.resolve().relative_to(ROOT)
    except ValueError:
        return True                      # fichier étranger : on l'audite comme une page en ligne
    first = rel.parts[0] if rel.parts else ""
    if first in PUBLIC_DIRS:
        return True
    if first in WORK_DIRS:
        return False
    return "/".join(rel.parts[:2]) not in WORK_DIRS


def robots_near(path):
    """Le robots.txt qui s'applique : celui du dossier de la page, sinon celui de la racine du dépôt."""
    for cand in (path.parent / "robots.txt", ROOT / "robots.txt"):
        if cand.exists():
            return cand
    return None


def blocked_bots(text):
    """Les robots IA bloqués par un robots.txt — lecture par groupes `User-agent:` / `Disallow:`."""
    blocked, current, star = set(), [], False
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            if current:
                current, star = [], False
            current.append(value.lower())
        elif key == "disallow" and value:
            for agent in current:
                for bot in AI_BOTS:
                    if agent == bot or bot in agent:
                        blocked.add(bot)
    return sorted(blocked), star


def audit(path):
    html = io.open(path, encoding="utf-8", errors="replace").read()
    findings, notes, good = [], [], []
    public = is_public(path)

    def add(level, msg):
        findings.append((level, msg))

    # ── 1 · les robots IA ─────────────────────────────────────────────────────────────────────────
    rb = robots_near(path)
    if rb:
        blocked, _ = blocked_bots(io.open(rb, encoding="utf-8", errors="replace").read())
        if blocked and public:
            add("ERR", "robots.txt (%s) bloque %d robot(s) IA : %s — un site non exploré ne peut pas être cité"
                % (rb.name, len(blocked), ", ".join(blocked)))
        elif blocked:
            notes.append("robots.txt (%s) bloque %s — page de travail, sans conséquence ici" % (rb.name, ", ".join(blocked)))
        else:
            good.append("robots.txt (%s) : aucun robot IA bloqué" % rb.name)
    else:
        notes.append("pas de robots.txt trouvé près de la page — par défaut, rien n'est bloqué")

    # Un GABARIT indexable : le défaut trouvé chez nous le 24/09 par ce portique. `site/` part en ligne
    # (`hosting/build_site_zip.py` prend tout `site/*.html`), et la page-modèle y portait 18 jetons
    # `{{...}}` sans noindex : un prospect qui la trouvait lisait « {{NAME}} ». Une page livrée qui
    # contient des jetons non remplis ne doit jamais être indexable.
    placeholders = len(re.findall(r"\{\{[A-Z_]{2,}\}\}", html))
    meta = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
    meta_val = (meta.group(1).lower() if meta else "")
    noindex = "noindex" in meta_val
    # Un GABARIT (page-modèle à jetons `{{...}}`) est le seul cas d'une page livrée qui DOIT être en
    # noindex. Il se juge donc dans les deux sens, et c'est la correction que le portique s'est infligée
    # à lui-même le 24/09 : d'abord il a signalé « aucune donnée structurée » sur la page-modèle, puis —
    # après que je lui ai posé un noindex — il l'a accusée d'être invisible. Un gabarit indexable est une
    # faute ; un gabarit visible est une faute aussi.
    gabarit = placeholders > 0 or "mockup" in path.name.lower()
    if public and gabarit and not noindex:
        add("ERR", "gabarit à jetons (%d) laissé indexable : un prospect qui la trouve lit {{NAME}} — "
                   "poser `noindex,nofollow` ou retirer la page du déploiement" % placeholders)
    elif public and gabarit:
        good.append("gabarit correctement non indexable (`noindex,nofollow`) — à ne jamais débloquer")
    elif public and noindex:
        add("ERR", "page publique avec noindex : invisible de Google ET des IA — le débloquer avant déploiement")
    elif public:
        good.append("page publique indexable (%s)" % (meta_val or "index par défaut"))
    elif noindex:
        notes.append("`noindex,nofollow` — VOULU sur une page de travail ; **à retirer le jour où cette page "
                     "devient celle du client** (voir la liste en fin de rapport)")
    else:
        notes.append("page de travail SANS noindex : si elle est déployée en l'état, elle sera indexée")

    # ── 2 · les données structurées ───────────────────────────────────────────────────────────────
    types = sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', html)))
    # Sur un GABARIT, ces deux contrôles n'ont pas de sens : son contenu viendra du client, jetons
    # compris. Les exiger produirait un avertissement à chaque exécution — et un outil qui crie au loup
    # finit par ne plus être lu.
    if not types:
        if public and not gabarit:
            add("WARN", "aucune donnée structurée (JSON-LD) : l'IA n'a pas de relations nommées à lire")
        else:
            notes.append("aucune donnée structurée (%s)" % ("gabarit : normal" if gabarit else "page de travail"))
    else:
        good.append("données structurées : %s" % ", ".join(types))
        if "FAQPage" in types and not ('"Question"' in html and '"Answer"' in html):
            add("WARN", "FAQPage déclaré sans couple Question/Answer : le balisage promet ce que la page ne dit pas")

    # ── 3 · des questions, pas seulement des affirmations ─────────────────────────────────────────
    # (On retire les balises AVANT de chercher le point d'interrogation : nos titres et nos sommaires
    #  bilingues sont pleins de <span>, et un détecteur qui exige le « ? » dans le premier nœud de texte
    #  annoncerait « aucune question » sur une page qui n'est faite que de ça — mesuré sur UNI-LABO.)
    blocks = re.findall(r"<(?:summary|h[23])\b[^>]*>(.*?)</(?:summary|h[23])>", html, re.S | re.I)
    questions = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", b)).strip()
                 for b in blocks if "?" in re.sub(r"<[^>]+>", " ", b)]
    if questions:
        good.append("%d question(s) en titre ou en sommaire (format « atomique », citable hors contexte)"
                    % len(questions))
    elif not gabarit:
        notes.append("aucune question en titre : la page affirme, elle ne répond pas")

    return findings, good, notes, public


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    pages = []
    for a in args:
        p = pathlib.Path(a)
        if p.is_file():
            pages.append(p)
        elif p.is_dir():
            pages += sorted(p.rglob("*.html"))
    if not pages:
        print("usage : python3 tools/qa/audit_aeo.py [--strict] <pages|dossiers>")
        return 2

    errs, warns, to_unlock = [], [], []
    for p in pages:
        findings, good, notes, public = audit(p)
        rel = p.resolve().relative_to(ROOT) if str(p.resolve()).startswith(str(ROOT)) else p
        e = [(l, m) for l, m in findings if l == "ERR"]
        w = [(l, m) for l, m in findings if l == "WARN"]
        errs += [(rel, m) for _, m in e]
        warns += [(rel, m) for _, m in w]
        mark = "✗" if e else ("!" if w else "ok")
        print("%s   %s" % (mark, rel))
        for m in good:
            print("      ✓ %s" % m)
        for l, m in findings:
            print("      %s %s" % (l, m))
        for n in notes:
            print("      · %s" % n)
        _txt = io.open(p, encoding="utf-8", errors="replace").read()
        _gabarit = "mockup" in p.name.lower() or re.search(r"\{\{[A-Z_]{2,}\}\}", _txt)
        if "noindex" in _txt.lower() and not public and not _gabarit:
            to_unlock.append(str(rel))

    print()
    print("── non vérifiable depuis un fichier HTML, et assumé : la CONSENSUS (être nommé sur les pages des")
    print("   autres — la corrélation la plus forte avec la visibilité IA selon l'étude Ahrefs), la")
    print("   FRAÎCHEUR réelle du contenu, la présence YOUTUBE, la qualité d'écriture (BLUF, phrases")
    print("   déclaratives) et le fait d'être cité ou non par une IA. Cinq choses qui demandent du travail")
    print("   humain et des données que nous n'avons pas — donc jamais une promesse dans une offre.")
    if to_unlock:
        print()
        print("── rappel de déploiement : %d page(s) de travail portent noindex et deviendront publiques" % len(to_unlock))
        for rel in to_unlock:
            print("   · %s" % rel)
    print()
    if errs:
        print("%d faute(s) — %s" % (len(errs), " · ".join(m for _, m in errs[:3])))
    if warns:
        print("%d avertissement(s)" % len(warns))
    if not errs and not warns:
        print("Aucune faute, aucun avertissement sur %d page(s)." % len(pages))
    return 1 if (strict and (errs or warns)) else 0


if __name__ == "__main__":
    sys.exit(main())
