#!/usr/bin/env python3
"""audit_platform — la porte des LÉGENDES : une légende par plateforme, pas une légende recopiée.

Pourquoi elle existe (26/10/2026, tour 153)
-------------------------------------------
Le 26/10 à 11 h, Facebook partait à midi et King a demandé les légendes TikTok et Instagram **séparément**.
Trois règles écrites s'appliquaient déjà et **aucune n'était vérifiée** : 3–8 hashtags dont un local et un
de marque (`TIKTOK-SEO-CHECKLIST` §C) · sous-titres **manuels**, jamais automatiques (ruling 11/10) ·
**FR à l'écran, EN en légende** sur Instagram (`brand/AMK-PRESENCE` §2, correction 5). Une règle sans
porte est un trou.

Ce qu'elle refuse
-----------------
- `sections-manquantes` · il n'y a pas **deux** sections `## 2` (TikTok) et `## 3` (Instagram) avec légende
- `hashtags-hors-borne` · moins de 3 ou plus de 8 hashtags dans une légende
- `local-absent` · ni `#Douala` ni `#Cameroun` — la géographie de la cible
- `marque-absente` · `#AMKweb` — un seul et toujours le même, pour que la série se retrouve
- `mot-cle-absent` · `APERÇU` — le mot compté dans le CRM
- `prix-dans-la-legende` · un prix, `FCFA`, un `k` (décision du 08/10)
- `mendicite` · `#fyp`, `#pourtoi`, `#viral`, `abonnez-vous`, `likez` — ça ne classe rien, ça signale un
  compte qui cherche des vues (`CONTENT-CREATION` §5 quater)
- `cta-multiple` · plus d'une action demandée dans la légende TikTok
- `sous-titres-auto` · la section TikTok ne dit pas « sous-titres manuels » (ruling 11/10)
- `langue-instagram` · la légende Instagram est en français (règle FR à l'écran / EN en légende)
- `alt-absent` · pas de texte alternatif pour Instagram (accessibilité, `AMK-DESIGN-SKILLS` §27)
- `lieu-absent` · pas de lieu déclaré pour Instagram
- `epingle-absent` · pas de commentaire épinglé pour TikTok

Ce qu'elle avertit
------------------
`coupe-tiktok-manquante` · le master dépasse **16 s** — la grille maison du 23/10 dit 12–16 s sur TikTok
(avertissement, pas refus : une pièce longue peut sortir, mais on doit le savoir) · `duree-inconnue`.

Usage
-----
    python3 tools/qa/audit_platform.py content/reels/ep01/PUBLICATION-TIKTOK-INSTAGRAM-2026-10-26.md \\
                                        content/reels/ep01/ep01-v6.mp4
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_publication import _duree_master  # noqa: E402  (même mesure, une seule implémentation)

HASHTAGS_MIN, HASHTAGS_MAX = 3, 8
TIKTOK_MAX_S = 16.0
ACTION_FR = ("ecrivez", "envoyez", "appelez", "cliquez", "commentez", "inscrivez", "contactez")
LOCAL = ("#douala", "#cameroun", "#cameroon", "#buea", "#yaounde")
MARQUE = "#amkweb"
INTERDITS = ("#fyp", "#pourtoi", "#viral", "#follow", "abonnez-vous", "abonnez vous", "likez",
             "follow for follow", "commentez un emoji", "partagez svp")
STOPWORDS_FR = (" votre ", " vous ", " votre", " ecrivez", " il ", " elle ", " qui ", " dans ",
                " avec ", " votre ", " sa ", " une page", " avant de ")
PRIX = re.compile(r"\b(fcfa|prix|tarif)\b|\d{1,3}\s?k\b|\d{1,3}(\s\d{3})+\s?(fcfa|f)\b", re.I)


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
    tags: dict[str, list[str]] = field(default_factory=dict)
    duree: float | None = None

    @property
    def ok(self) -> bool:
        return not self.fails


def _plat(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def _sections(texte: str) -> list[tuple[str, str]]:
    out, titre, corps = [], "", []
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            if titre:
                out.append((titre, "\n".join(corps)))
            titre, corps = ligne[3:].strip(), []
        elif titre:
            corps.append(ligne)
    if titre:
        out.append((titre, "\n".join(corps)))
    return out


def _section(sections: list[tuple[str, str]], numero: str) -> str:
    for titre, corps in sections:
        if re.match(rf"^{numero}\b", titre):
            return corps
    return ""


def _code(corps: str, langue: str | None = None) -> list[str]:
    blocs = []
    for m in re.finditer(r"```([a-zA-Z]*)\n(.*?)```", corps, re.S):
        if langue is None or m.group(1).lower() == langue:
            blocs.append(m.group(2).strip())
    return blocs


def legende(corps: str) -> str:
    """La première légende = le premier bloc de code non étiqueté `text`... ou le premier tout court."""
    blocs = _code(corps)
    return blocs[0] if blocs else ""


def hashtags(caption: str) -> list[str]:
    return [h.lower() for h in re.findall(r"#[0-9A-Za-zÀ-ÿ_]+", caption)]


def audit(chemin: str | Path, master: str | Path | None = None) -> Verdict:
    chemin = Path(chemin)
    texte = chemin.read_text(encoding="utf-8")
    sections = _sections(texte)
    v = Verdict()

    tt = _section(sections, "2")
    ig = _section(sections, "3")
    cap_tt, cap_ig = legende(tt), legende(ig)
    if not cap_tt or not cap_ig:
        v.fails.append("[sections-manquantes] il faut une légende TikTok (§2) ET une légende Instagram (§3)")
        return v

    v.tags = {"tiktok": hashtags(cap_tt), "instagram": hashtags(cap_ig)}

    for plateforme, cap in (("tiktok", cap_tt), ("instagram", cap_ig)):
        h = v.tags[plateforme]
        if not HASHTAGS_MIN <= len(h) <= HASHTAGS_MAX:
            v.fails.append(
                f"[hashtags-hors-borne] {plateforme} : {len(h)} hashtag(s), attendu "
                f"{HASHTAGS_MIN}–{HASHTAGS_MAX} (`TIKTOK-SEO-CHECKLIST` §C)"
            )
        if not any(t in LOCAL for t in h):
            v.fails.append(f"[local-absent] {plateforme} : ni #Douala ni #Cameroun")
        if MARQUE not in h:
            v.fails.append(f"[marque-absente] {plateforme} : #AMKweb manque")
        if "apercu" not in _plat(cap):
            v.fails.append(f"[mot-cle-absent] {plateforme} : le mot APERÇU n'est pas dans la légende")
        if PRIX.search(cap):
            v.fails.append(f"[prix-dans-la-legende] {plateforme} : « {PRIX.search(cap).group(0)} »")
        plat = _plat(cap)
        for mot in INTERDITS:
            if mot in plat:
                v.fails.append(f"[mendicite] {plateforme} : « {mot} » — ça ne classe rien")
                break

    actions = sorted({a for a in ACTION_FR if a in _plat(cap_tt)})
    if len(actions) > 1:
        v.fails.append(f"[cta-multiple] tiktok : {len(actions)} actions ({', '.join(actions)}) — une seule")

    plat_tt = _plat(tt)
    if "sous-titre" not in plat_tt or "manuel" not in plat_tt:
        v.fails.append(
            "[sous-titres-auto] tiktok : la section ne dit pas « sous-titres manuels » — "
            "l'automatique ne tient pas sur un accent camerounais (ruling 11/10)"
        )
    if not re.search(r"commentaire (epingle|épinglé)", plat_tt):
        v.fails.append("[epingle-absent] tiktok : pas de commentaire épinglé (le numéro doit être écrit)")

    plat_ig = _plat(cap_ig)
    if sum(1 for m in STOPWORDS_FR if m in f" {plat_ig} ") >= 2:
        v.fails.append(
            "[langue-instagram] la légende Instagram est en français — "
            "règle `AMK-PRESENCE` §2 (5) : FR à l'écran, EN en légende"
        )
    if "alt text" not in _plat(ig) and "alt-texte" not in _plat(ig):
        v.fails.append("[alt-absent] instagram : pas de texte alternatif")
    if "lieu" not in _plat(ig):
        v.fails.append("[lieu-absent] instagram : pas de lieu déclaré")

    if master is not None:
        m = Path(master)
        if m.exists():
            v.duree = _duree_master(m)
            if v.duree is None:
                v.warns.append("[duree-inconnue] aucun ffmpeg — la durée n'a pas été mesurée")
            elif v.duree > TIKTOK_MAX_S:
                v.warns.append(
                    f"[coupe-tiktok-manquante] master {v.duree} s > {TIKTOK_MAX_S} s — la grille du 23/10 "
                    f"dit 12–16 s sur TikTok : la coupe est pour la pièce suivante, pas pour celle-ci"
                )

    return v


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    kit = argv[0]
    master = argv[1] if len(argv) > 1 else None
    v = audit(kit, master)
    entete = "plateformes · " + " · ".join(f"{k} {len(t)} hashtags" for k, t in v.tags.items())
    if v.duree is not None:
        entete += f" · master {v.duree} s"
    print(("✓ " if v.ok else "✗ ") + entete)
    for w in v.warns:
        print(f"   ⚠ {w}")
    for f in v.fails:
        print(f"   ⛔ {f}")
    return 0 if v.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
