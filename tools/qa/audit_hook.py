#!/usr/bin/env python3
"""audit_hook — la porte de l'**accroche** et de la **grille**, avant production.

Deux sources du 25/10, même fil (`knowledge/HOOKS-2026-10-25.md`) :

- **les 6 mots de puissance** : *subject clarity*, *action*, *objective / state change*, **contrast**
  (« the most important in the entire stack »), et deux mots d'intrigue facultatifs ;
- **la grille 331** : 3 sujets × 3 formats = 9 vidéos, et la **dixième** se décide **après** les neuf,
  sur la combinaison qui a le mieux marché — « the first time you stop guessing » ;
- **l'échelle des histoires** en 5 niveaux (Reporter → Magician → Fortuneteller → Architect →
  Maestro), déclarée par la pièce, parce qu'un niveau 4 dans 24 s est un mensonge de plus.

Ce que la porte fait : elle **compte les mots** avec des lexiques explicites, refuse ce qui manque,
et accepte une **déclaration** quand le lexique se trompe (`declares={"action": "réclamez"}`) — la
machine propose, l'auteur déclare, et la déclaration se voit dans la sortie.

Ce qu'elle ne fait pas : juger si l'accroche est bonne. Elle vérifie qu'elle contient les quatre
pièces que la source dit obligatoires, qu'elle ne vend pas par la peur, et qu'elle ne promet rien.

Usage :

    from audit_hook import Hook, Grid, audit_hook, audit_grid
    audit_hook(Hook(text="Ouvrez votre nom sur Google : il appelle celui qui a un site, pas l'autre.",
                    level=3))
    python3 tools/qa/audit_hook.py content/reels/ep01/make_ep01.py        # lit HOOK
    python3 tools/qa/audit_hook.py --text "…"                             # à la volée
    python3 tools/qa/audit_hook.py --grid content/ideas/GRID-331-2026-10-25.md
"""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── lexiques (explicites, extensibles — et imparfaits, c'est pour ça que `declares` existe) ─────
SUJET = re.compile(
    r"\b(je|j|moi|mon|ma|mes|nous|notre|nos|vous|votre|vos|tu|ton|ta|tes|te|toi|on)\b"
    r"|\bj'", re.I)

ACTION = re.compile(
    r"\b(ouvrez|ouvre|mettez|met|publiez|publie|réclamez|réclame|vérifiez|vérifie|regardez|regarde"
    r"|cherchez|cherche|tapez|tape|écrivez|écris|appelez|appelle|faites|fait|arrêtez|arrête"
    r"|commencez|commence|prenez|prend|corrigez|corrige|construisez|construis|demandez|demande"
    r"|cliquez|clique|testez|teste|mesurez|mesure|comptez|compte|choisissez|choisis|envoyez|envoie"
    r"|dites|dire|lisez|lis|notez|note|ajoutez|ajoute|remplissez|remplis)\b", re.I)

OBJECTIF = re.compile(
    r"\b(pour que|afin de|résultat|devient|deviennent|reste|restent|gagne|gagnent|économise"
    r"|économisent|trouve|trouvent|évite|évitent|repart|repartent|passe au suivant|passent au suivant"
    r"|appelle|appellent|vous appelle|en \d+ (minutes?|secondes?|heures?|jours?)"
    r"|finis|finit)\b", re.I)

CONTRASTE = re.compile(
    r"\b(au lieu de|alors que|mais|sans|pas|jamais|non|contrairement|pendant que|versus|vs|et non)\b",
    re.I)

INTRIGUE = re.compile(
    r"\b(voici|pourquoi|comment|ce que|personne ne|sauf|et c'est|or|seulement|un seul|deux)\b", re.I)

# Ce qu'on refuse par ruling, quelle que soit la performance : la peur et la promesse.
PEUR = re.compile(
    r"\b(urgence|urgent|dépêchez|dépêchez-vous|dernière chance|dernières places|avant qu'il ne soit trop tard"
    r"|catastrophe|danger|panique|emergency|vous allez fermer|vous perdrez tout)\b", re.I)
PROMESSE = re.compile(
    r"\b(garanti|garantie|garantis|assuré|certifié|doublez|triplerez|quadruplez|\+ ?\d+\s?%"
    r"|100 ?%|infaillible|à coup sûr)\b", re.I)

PLAN = re.compile(r"\b(d'abord|en premier|première|deuxième|troisième|ensuite|puis|étape)\b", re.I)

NIVEAUX = {
    1: "Reporter — rapporte ce qui est (un constat)",
    2: "Magician — révèle le mécanisme caché",
    3: "Fortuneteller — annonce ce qui va se passer",
    4: "Architect — donne le plan, dans l'ordre",
    5: "Maestro — orchestre tout, arc et émotion",
}
NIVEAU_PLAN_MIN = 4          # au-dessus de 3, il faut un plan lisible dans le texte
ACTION_MOTS_MAX = 28
HOOK_CARACTERES_MAX = 240


@dataclass
class Hook:
    text: str
    level: int = 1
    declares: dict[str, str] = field(default_factory=dict)


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.fails


def power_words(hook: Hook) -> dict[str, bool]:
    """Les six mots, dans l'ordre de la source. Les deux derniers sont facultatifs."""
    declares = {k.lower() for k in hook.declares}
    return {
        "sujet": bool(SUJET.search(hook.text)) or "sujet" in declares,
        "action": bool(ACTION.search(hook.text)) or "action" in declares,
        "objectif": bool(OBJECTIF.search(hook.text)) or "objectif" in declares,
        "contraste": bool(CONTRASTE.search(hook.text)) or "contraste" in declares,
        "intrigue_1": bool(INTRIGUE.search(hook.text)),
        "intrigue_2": len(re.findall(r"\d", hook.text)) > 0,
    }


def audit_hook(hook: Hook) -> Verdict:
    v = Verdict()
    texte = hook.text.strip()
    mots = power_words(hook)

    if hook.level not in NIVEAUX:
        v.fails.append(f"niveau-inconnu — {hook.level!r} n'est pas un niveau (1–5)")
    if not texte:
        v.fails.append("hook-vide — pas de texte, pas d'accroche")
        return v

    manquants = [m for m in ("sujet", "action", "objectif", "contraste") if not mots[m]]
    if manquants:
        v.fails.append(
            "mots-manquants — il manque : " + ", ".join(manquants)
            + ". Le contraste est le mot le plus important de la pile : il ne se saute pas. "
              "(Sujet = qui ; action = ce qu'il fait ; objectif = ce qu'il obtient ; "
              "contraste = l'état de départ opposé au résultat.)")
    if len(texte.split()) > ACTION_MOTS_MAX:
        v.fails.append(f"trop-long — {len(texte.split())} mots (max {ACTION_MOTS_MAX}) : "
                       "ce n'est plus une accroche, c'est un paragraphe")
    if len(texte) > HOOK_CARACTERES_MAX:
        v.fails.append(f"trop-long — {len(texte)} caractères (max {HOOK_CARACTERES_MAX})")
    if PEUR.search(texte):
        v.fails.append("peur — vendre par la peur est exclu (ruling, `CONTENT-CREATION` §4 bis) : "
                       "« poussée douce, jamais la peur »")
    if PROMESSE.search(texte):
        v.fails.append("promesse — aucun résultat promis, aucun chiffre de performance "
                       "(ruling 142, `RESEARCH-STANDARD.md`)")

    if not (mots["intrigue_1"] or mots["intrigue_2"]):
        v.warns.append("sans-intrigue — les deux mots facultatifs manquent : l'accroche tient, "
                       "elle n'attire pas")
    if hook.level >= NIVEAU_PLAN_MIN and len(PLAN.findall(texte)) < 2:
        v.warns.append(f"niveau-ambitieux — niveau {hook.level} déclaré sans plan lisible "
                       "(« d'abord / ensuite / puis ») : un Architect sans ordre est un Reporter")
    if hook.level == 1:
        v.warns.append("niveau-1 — Reporter : l'échelle commence ici, elle ne s'arrête pas ici")
    if hook.declares:
        v.warns.append("déclaration — " + ", ".join(f"{k}={v_}" for k, v_ in hook.declares.items())
                       + " : la machine ne l'a pas reconnu seule, l'auteur l'affirme")
    return v


# ── la grille 331 ───────────────────────────────────────────────────────────────────────────
@dataclass
class Grid:
    cells: list[dict] = field(default_factory=list)


LIGNE_GRILLE = re.compile(r"^\s*\|(.+)\|\s*$")


def parse_grid(texte: str) -> Grid:
    cells = []
    for ligne in texte.splitlines():
        m = LIGNE_GRILLE.match(ligne)
        if not m:
            continue
        cols = [c.strip() for c in m.group(1).split("|")]
        if not cols or not re.match(r"^\d+$", cols[0]):
            continue
        if set("".join(cols)) <= set("-: "):
            continue
        cells.append({
            "n": int(cols[0]),
            "topic": cols[1] if len(cols) > 1 else "",
            "format": cols[2] if len(cols) > 2 else "",
            "sujet": cols[3] if len(cols) > 3 else "",
            "etat": cols[4] if len(cols) > 4 else "",
        })
    return Grid(cells=cells)


def audit_grid(grid: Grid) -> Verdict:
    v = Verdict()
    neuf = [c for c in grid.cells if 1 <= c["n"] <= 9]
    dix = [c for c in grid.cells if c["n"] == 10]

    if len(neuf) != 9:
        v.fails.append(f"grille-incomplete — {len(neuf)} cellule(s) sur 9 : la grille se remplit "
                       "toute, sinon ce n'est pas trois formats sur trois sujets")
    if not dix:
        v.fails.append("pas-de-10 — la dixième vidéo est manquante : c'est elle qui remplace "
                       "l'intuition par la donnée")
    for c in grid.cells:
        if not c["sujet"] or c["sujet"] in ("—", "-"):
            v.fails.append(f"cellule-sans-sujet — #{c['n']} : aucune accroche ni sujet nommé")

    topics = {c["topic"].lower() for c in neuf if c["topic"]}
    formats = {c["format"].lower() for c in neuf if c["format"]}
    if len(neuf) == 9 and len(topics) != 3:
        v.fails.append(f"trois-sujets — {len(topics)} sujet(s) distinct(s) pour 9 cellules "
                       "(il en faut exactement 3)")
    if len(neuf) == 9 and len(formats) != 3:
        v.fails.append(f"trois-formats — {len(formats)} format(s) distinct(s) pour 9 cellules "
                       "(il en faut exactement 3)")

    combos = [(c["topic"].lower(), c["format"].lower()) for c in neuf]
    for combo in set(combos):
        if combos.count(combo) > 1:
            v.fails.append(f"doublon — {combo[0]} × {combo[1]} apparaît {combos.count(combo)} fois : "
                           "une case vide quelque part")

    if dix:
        c = dix[0]
        vide = lambda x: x.strip() in ("", "—", "-", "–")
        remplie = not (vide(c["topic"]) and vide(c["format"])) \
            and "à décider" not in c["etat"].lower() and "a decider" not in c["etat"].lower()
        if remplie and not re.search(r"\d{2,}", c["etat"]):
            v.fails.append("double-sans-donnée — la dixième est déjà choisie sans aucune mesure : "
                           "elle se décide **après** les neuf, sur la combinaison qui a le mieux "
                           "marché")
        if not remplie:
            v.warns.append("double-ouvert — la dixième reste ouverte : c'est la règle, pas un oubli")
    return v


# ── CLI ─────────────────────────────────────────────────────────────────────────────────────
def load_hook(path: str) -> Hook:
    spec = importlib.util.spec_from_file_location("piece_hook", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["piece_hook"] = mod
    spec.loader.exec_module(mod)
    hook = getattr(mod, "HOOK", None)
    if hook is None or not hasattr(hook, "text"):
        raise SystemExit(f"✗ {path} : pas de HOOK (Hook) — la pièce ne déclare pas son accroche")
    return hook


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    echecs = 0
    if argv[0] == "--text":
        hook = Hook(text=" ".join(argv[1:]), level=1)
        v = audit_hook(hook)
        print(f"{'✓' if v.ok else '✗'} accroche · {len(hook.text.split())} mots · niveau {hook.level}")
        for f in v.fails:
            print(f"   ⛔ {f}")
        for w in v.warns:
            print(f"   ⚠ {w}")
        return 0 if v.ok else 1
    if argv[0] == "--grid":
        grid = parse_grid(Path(argv[1]).read_text(encoding="utf-8"))
        v = audit_grid(grid)
        print(f"{'✓' if v.ok else '✗'} grille · {len(grid.cells)} ligne(s)")
        for f in v.fails:
            print(f"   ⛔ {f}")
        for w in v.warns:
            print(f"   ⚠ {w}")
        return 0 if v.ok else 1
    for path in argv:
        hook = load_hook(path)
        v = audit_hook(hook)
        mots = power_words(hook)
        marques = "".join("✓" if mots[m] else "·" for m in
                          ("sujet", "action", "objectif", "contraste"))
        print(f"{'✓' if v.ok else '✗'} {Path(path).parent.name:8} niveau {hook.level} "
              f"({NIVEAUX.get(hook.level, '?').split(' —')[0]}) · mots {marques} · "
              f"{len(hook.text.split())} mots")
        if not v.ok:
            echecs += 1
        for f in v.fails:
            print(f"   ⛔ {f}")
        for w in v.warns:
            print(f"   ⚠ {w}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
