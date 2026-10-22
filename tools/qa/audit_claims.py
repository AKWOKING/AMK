#!/usr/bin/env python3
"""AMK — portique « AFFIRMATIONS » : refuse une publication qui contredit un verrou client.

Pourquoi cet outil existe
-------------------------
Le 22/10, deux affirmations fausses sont parties dans des vidéos livrées :
  • « le prix est affiché en ligne » — alors que le client l'interdit par écrit
    (« Pour le prix des montures c'est interdit de le diffuser », 10/10/2026) ;
  • « 40 montures » — alors que le ruling du 21/10 interdit de chiffrer le stock.

Ces deux verrous étaient écrits dans le dépôt. Ils n'ont pas été appliqués parce que
rien ne les **vérifiait**. Une règle qui n'a pas de contrôle est une intention.

Ce que fait l'outil : il lit les livrables (storyboards, scripts, légendes, sous-titres)
et échoue si une phrase contredit un verrou documenté. Chaque règle cite le verrou
d'origine pour qu'on puisse le discuter au lieu de contourner.

Usage
-----
    python3 tools/qa/audit_claims.py clients/dm-optic/content
    python3 tools/qa/audit_claims.py --all          # tout le dépôt client
    python3 tools/qa/audit_claims.py fichier.json --json

Sortie : une ligne par infraction (fichier:ligne → extrait → règle → correctif).
Code de sortie 1 s'il existe au moins une infraction.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Extensions auditées : les livrables, pas le code ni les données de build.
EXTS = {".json", ".md", ".txt", ".srt", ".vtt", ".jsx", ".tsx", ".html"}

# Fichiers exclus : ils CITENT les verrous pour les expliquer.
SKIP_NAMES = {"audit_claims.py"}

RULES = [
    {
        "id": "prix-public",
        # la fenêtre est volontairement large : dans un storyboard JSON, « le prix » et
        # « est affiché » vivent sur deux lignes différentes.
        "pattern": re.compile(
            r"(?:(?:prix|tarif)s?\b.{0,120}?\b(?:affich\w*|en ligne|sur le site|public\b|visible\b|en photo))"
            r"|(?:\bavec son prix\b)|(?:\b(?:affich|consultabl)\w*\b.{0,40}?\bprix\b)",
            re.I | re.S),
        "why": "VERROU CLIENT (10/10/2026, verbatim) : « Pour le prix des montures c'est interdit "
               "de le diffuser car nous sommes régit par le ministère de la Santé Publique. » "
               "Aucun prix n'est public, ni sur le site, ni en vidéo, ni en légende.",
        "fix": "Parler de la référence, de l'essai au cabinet, ou de « ce qui fait le prix » — "
               "jamais d'un prix consultable en ligne.",
    },
    {
        "id": "stock-chiffre",
        "pattern": re.compile(r"\b(\d{1,4}|quarante|cinquante|cent)\s+(montures|modèles|paires)\b", re.I),
        "why": "RULING KING (21/10/2026) : « avoid mentioning the number of frames available "
               "everywhere ». Le site a été rebuildé pour retirer ces comptes ; une vidéo qui les "
               "redit contredit la page qu'elle renvoie.",
        "fix": "« des montures », « chaque monture », « celles du cabinet » — sans cardinal.",
    },
    {
        "id": "superlatif",
        # ne vise que les affirmations SUR LE CABINET OU LE PRODUIT, pas les tournures
        # internes (« la meilleure image en frame 0 », « le premier post »).
        "pattern": re.compile(
            r"\b(?:le|la|les)\s+(?:meilleur\w*|n°\s?1|numero\s?1)\s+"
            r"(?:opticien|optique|cabinet|lunettes?|montures?|verres?|magasin|boutique|de douala|du cameroun)\b"
            r"|\b(?:le|la)\s+(?:meilleur\w*)\s+(?:de|du|des)\b"
            r"|\bunique\s+au\s+cameroun\b"
            r"|\b(?:qualité|service|monture|verre|examen|garantie)\s+garantie?s?\b", re.I),
        "exts": {"json", "srt", "vtt", "txt"},
        "why": "Règle de marque : aucun superlatif non prouvable, aucune garantie. Un cabinet ne "
               "peut pas être « le meilleur » sur un critère qu'il ne mesure pas.",
        "fix": "Remplacer par une preuve : photographié, mesuré, inscrit à l'ONOC, essayé sur place.",
    },
    {
        "id": "allegation-medicale",
        # le verbe doit porter sur la vue ou les yeux du patient, pas figurer dans une liste d'interdits
        "pattern": re.compile(
            r"\b(?:guérit|soigne|corrige|améliore|récupère|restaure)\b\s+(?:la\s+|votre\s+|vos\s+)?"
            r"(?:vue|yeux|vision|myopie|presbytie|astigmatisme)\b"
            r"|\bguérit\b|\btraitement\s+(?:de|du|des)\s+(?:la\s+)?(?:myopie|presbytie|cataracte)\b",
            re.I),
        "exts": {"json", "srt", "vtt", "txt"},
        "why": "Aucune allégation médicale : un opticien optométriste mesure et équipe, il ne "
               "soigne pas. C'est aussi la ligne de l'ONOC.",
        "fix": "« mesurer », « équiper », « soulager la fatigue visuelle par une pause » — jamais "
               "« soigner » ni « guérir ».",
    },
]

# Un fichier peut revendiquer une exception explicite, sur la même ligne : claims-ok: raison
ALLOW = re.compile(r"claims-ok\s*:", re.I)
# Une ligne de documentation CITE les interdits pour les expliquer : « … » dans un tableau.
DOC_QUOTE = re.compile(r"«.*»")

# Dossiers où les verrous sont EXPLIQUÉS (on n'y cherche pas d'infraction).
SKIP_DIRS = {"node_modules", ".git", "build-notes.md", "Activity-Log.md",
             "PRE-FLIGHT.md", "knowledge", "onboarding", "dossier.md"}


def iter_files(paths):
    for p in paths:
        p = p if os.path.isabs(p) else os.path.join(ROOT, p)
        if os.path.isfile(p):
            yield p
            continue
        for base, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
            for f in files:
                fp = os.path.join(base, f)
                if os.path.splitext(f)[1].lower() not in EXTS:
                    continue
                if f in SKIP_NAMES:
                    continue
                if any(s in fp for s in SKIP_DIRS):
                    continue
                yield fp


def scan(path: str):
    hits = []
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return hits
    # On cherche sur le texte aplati (les affirmations traversent les lignes d'un JSON),
    # puis on retrouve la ligne d'origine par comptage.
    flat = text.replace("\n", " ")
    line_starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)

    import bisect
    seen = set()
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    for rule in RULES:
        if "exts" in rule and ext not in rule["exts"]:
            continue
        for m in rule["pattern"].finditer(flat):
            snippet = m.group(0).strip()
            # une ligne portant déjà une exception explicite n'est pas signalée
            line_idx = bisect.bisect_right(line_starts, m.start()) - 1
            line_txt = text.splitlines()[line_idx] if line_idx < len(text.splitlines()) else ""
            if ALLOW.search(line_txt):
                continue
            if "|" in line_txt and DOC_QUOTE.search(line_txt):
                continue          # tableau qui énumère les interdits
            # une phrase de conformité (« aucun prix affiché », « pas de prix en ligne ») n'est pas une infraction
            neg = flat[max(0, m.start() - 40):m.start()].lower()
            if re.search(r"aucun\w*\s+(?:de\s+)?$|pas\s+de\s+$|jamais\s+de\s+$|sans\s+$", neg):
                continue
            key = (line_idx, rule["id"], snippet[:40])
            if key in seen:
                continue
            seen.add(key)
            hits.append({"file": os.path.relpath(path, ROOT), "line": line_idx + 1,
                         "rule": rule["id"], "match": snippet[:80],
                         "context": line_txt.strip()[:150],
                         "why": rule["why"], "fix": rule["fix"]})
    hits.sort(key=lambda h: h["line"])
    return hits


def main():
    ap = argparse.ArgumentParser(description="Portique des affirmations client")
    ap.add_argument("paths", nargs="*", default=[])
    ap.add_argument("--all", action="store_true", help="tout clients/ et hosting/")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    paths = a.paths or (["clients", "hosting"] if a.all else ["clients/dm-optic/content"])
    hits = []
    n = 0
    for f in iter_files(paths):
        n += 1
        hits += scan(f)

    if a.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        print(f"\naudit affirmations · {n} fichiers · {len(RULES)} règles")
        if not hits:
            print("  aucune infraction — les verrous client sont respectés")
        for h in hits:
            print(f"\n  {h['file']}:{h['line']}  [{h['rule']}]  « {h['match']} »")
            print(f"    ligne   : {h['context']}")
            print(f"    verrou  : {h['why'][:160]}")
            print(f"    correctif: {h['fix']}")
        print()
        print(f"VERDICT : {'OK' if not hits else f'BLOQUÉ — {len(hits)} affirmation(s) contredite(s)'}")
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
