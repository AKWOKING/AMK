#!/usr/bin/env python3
"""audit_story — la porte du RÉCIT : la règle qui n'était vérifiée par rien.

Pourquoi elle existe (26/10/2026, tour 150)
-------------------------------------------
Le dépôt savait déjà écrire un script : les **5 temps** (`CONTENT-CREATION` §3), le squelette
**Kallaway** (§3 bis : hook → lock-in → corps → rehook → corps → CTA aligné), la couche copie
(`HOUSE-KNOWLEDGE-BASE` §8), l'accroche et sa porte (`audit_hook`). Mais **aucune porte ne vérifiait la
structure**. C'est pour ça qu'EP01 v4 a passé quatre portes vertes avec un défaut que le Roast Room a
trouvé en dix secondes : **pas de scène, pas de rehook, preuve montrée mais jamais dite, cadeau enterré
à 21 s**. Une règle sans porte est un trou ; voilà la porte.

Ce qu'elle refuse (mesurable, jamais du goût)
---------------------------------------------
- `pas-de-cas` · le premier beat n'est pas une situation vécue
- `pas-de-lockin` · rien n'annonce, dans les trois premiers beats, pourquoi rester
- `pas-de-rehook` · aucun beat ne relance **entre** le corps et la sortie
- `preuve-muette` · une preuve existe à l'écran mais **aucun chiffre n'est prononcé**
- `preuve-absente` · pas de beat de preuve du tout
- `cta-non-aligne` · le CTA ne prononce pas le mot de la promesse
- `deux-cta` · plus d'un beat de sortie
- `liste-sans-axe` · quatre arguments empilés dans un même beat (`a, b, c, d`)
- `urgence` · champ lexical de la peur ou de la promesse (même lexique qu'`audit_hook`)
- `beat-vide` · un beat sans texte
- `sortie-absente` · le dernier beat n'est pas la sortie
- `trop-de-beats` · plus de 7 beats (au-delà, ce n'est plus un short)

Ce qu'elle avertit
------------------
`pas-de-miroir` · `preuve-tardive` · `cadeau-tardif` (l'offre gratuite arrive après 70 % de la pièce —
le défaut exact de la v4) · `debit` (hors 2,5–3,5 mots/s) · `hook-long` (> 5,0 s).

Comment une pièce se déclare
----------------------------
    from audit_story import Line, Script

    SCRIPT = Script(
        lines=[Line("hook", "…", "cas"), Line("spike1", "…", "preuve"), …],
        promise="aperçu",
    )
    # puis, dans le module : SCRIPT.piece = "ep01"

    python3 tools/qa/audit_story.py content/reels/ep01/make_ep01.py
"""

from __future__ import annotations

import importlib.util
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── rôle d'un beat ───────────────────────────────────────────────────────────────────────────────
ROLES = {
    "cas",      # la situation vécue, à la 2ᵉ personne — temps 1
    "lockin",   # pourquoi rester les vingt prochaines secondes — lock-in zone
    "corps",    # une idée, défendue — temps 3
    "rehook",   # remet le sablier à zéro — le beat qui manquait à la v4
    "preuve",   # un fait vérifiable, prononcé — temps 4
    "sortie",   # un seul CTA — temps 5
}

MAX_BEATS = 7
CONTEXTE_MAX = 5.0
CADEAU_MAX = 0.70      # l'offre gratuite ne doit pas arriver après 70 % de la pièce
PREUVE_MAX = 0.65      # la preuve doit être dite avant les deux tiers
DEBIT = (2.0, 4.2)     # mots par seconde, tolérance large (la doctrine vise 2,5–3,5)

# ── lexiques ─────────────────────────────────────────────────────────────────────────────────────
# Un chiffre prononcé : les chiffres, et les nombres écrits en toutes lettres (le français les préfère
# à l'oral). « douze avis » est une preuve ; « des avis » n'en est pas une.
# « un » et « une » sont des **articles** en français, pas des preuves : « un site » ne dit rien.
# Ils sont retirés exprès — la première version de cette porte comptait « un site » comme un chiffre,
# et donc laissait passer « sa fiche a des horaires, un site, des avis » sans preuve prononcée.
NOMBRES = (
    "deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|"
    "vingt|trente|quarante|cinquante|soixante|cent|mille|zéro|zero"
)
CHIFFRE = re.compile(rf"\b(\d+|[0-9]+\s?h|[0-9]+\s?%|{NOMBRES})\b", re.I)

# Ce qui dit « restez » : le contraste, la conséquence, l'annonce de la valeur (Kallaway, principe 4).
LOCKIN = re.compile(
    r"\b(pas vous|mais|avant|après|voici|voilà|regardez|la différence|pendant ce temps|"
    r"ce que|le problème|sauf que|et c'est là)\b",
    re.I,
)

# La sortie : un verbe, un canal. Deux verbes différents = deux CTA (la règle du dépôt).
VERBES_CTA = re.compile(r"\b(écrivez|ecrivez|appelez|cliquez|envoyez|réservez|reservez|commandez|"
                        r"demandez|inscrivez|commentez|partagez|abonnez)\b", re.I)

# Le refus, repris d'`audit_hook` : ni peur, ni promesse. Recopié exprès (une porte ne dépend pas d'une
# autre) — si le lexique change là-bas, le banc de test ici le montre.
PEUR = re.compile(
    r"\b(urgence|urgent|derni[eè]re chance|catastrophe|danger|risque de perdre|vous allez perdre|"
    r"avant qu'il ne soit trop tard|avant qu'il soit trop tard|menace|panique|effondrement)\b",
    re.I,
)
PROMESSE = re.compile(
    r"\b(garanti|garantie|garantis|certain|à coup sûr|100\s?%|doublez|triplez|"
    r"devenez riche|explosez|sans effort|miracle)\b",
    re.I,
)

# Le cadeau : ce qui est offert gratuitement, et qui doit arriver tôt.
CADEAU = re.compile(r"\b(gratuit|gratuite|gratis|dix minutes|10 minutes|sans payer|sans rien payer)\b", re.I)


@dataclass
class Line:
    """Un beat du script, tel qu'il est **prononcé** (pas tel qu'il est affiché).

    `role` accepte **plusieurs fonctions** : « lockin+preuve » veut dire que la même phrase retient
    (elle montre ce qu'il a vu) *et* prouve (elle prononce « douze avis »). C'est la réalité d'un beat
    de 4 secondes : exiger une fonction par phrase fabrique des scripts hachés.
    """

    name: str
    text: str
    role: str | set[str]
    start: float = 0.0
    end: float = 0.0

    @property
    def roles(self) -> set[str]:
        if isinstance(self.role, set):
            return self.role
        return {r.strip() for r in str(self.role).split("+") if r.strip()}

    @property
    def duree(self) -> float:
        return round(self.end - self.start, 3) if self.end > self.start else 0.0

    @property
    def mots(self) -> int:
        return len([m for m in re.split(r"\s+", self.text.strip()) if m])


@dataclass
class Script:
    lines: list[Line]
    promise: str = ""          # le mot que le CTA doit reprendre (« aperçu »)
    piece: str = ""
    # ce qui est **montré** mais pas dit : la capture, l'écran, le chiffre visuel. Si une preuve
    # existe à l'écran et qu'aucun beat ne prononce de chiffre, la porte refuse (`preuve-muette`).
    proof_on_screen: str = ""

    @property
    def total(self) -> float:
        return round(sum(l.duree for l in self.lines), 3)

    @property
    def duree_connue(self) -> bool:
        return all(l.duree > 0 for l in self.lines)


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.fails

    def fail(self, code: str, msg: str | None = None):
        self.fails.append(f"[{code}] {msg}" if msg else code)

    def warn(self, code: str, msg: str | None = None):
        self.warns.append(f"[{code}] {msg}" if msg else code)


# ── l'audit ──────────────────────────────────────────────────────────────────────────────────────


def audit(script: Script) -> Verdict:
    v = Verdict()
    lines = script.lines

    if not lines:
        v.fails.append("[script-vide] aucun beat : il n'y a rien à écouter")
        return v

    for l in lines:
        for r in l.roles:
            if r not in ROLES:
                v.fails.append(f"[role-inconnu] {l.name} : « {r} » n'est pas un rôle "
                               f"({', '.join(sorted(ROLES))})")
        if not l.text.strip():
            v.fails.append(f"[beat-vide] {l.name} : aucun texte prononcé")

    if len(lines) > MAX_BEATS:
        v.fails.append(f"[trop-de-beats] {len(lines)} beats > {MAX_BEATS} : au-delà, ce n'est plus un short")

    # 1 · le cas, en premier — temps 1 de la doctrine
    if "cas" not in lines[0].roles:
        v.fails.append(
            f"[pas-de-cas] le premier beat est « {'+'.join(sorted(lines[0].roles))} » : la doctrine ouvre sur une "
            "situation vécue, pas sur une consigne (`CONTENT-CREATION` §3, temps 1)"
        )

    # 2 · le lock-in, dans les trois premiers beats
    if not any("lockin" in l.roles for l in lines[:3]):
        v.fails.append(
            "[pas-de-lockin] rien n'annonce, dans les trois premiers beats, pourquoi rester "
            "(§3 bis : sans lock-in, le corps n'est jamais écouté)"
        )

    # 3 · la preuve, prononcée
    preuves = [l for l in lines if "preuve" in l.roles]
    if not preuves:
        v.fails.append("[preuve-absente] aucun beat de preuve : la pièce affirme sans fait (§3, temps 4)")
    else:
        dites = [l for l in preuves if CHIFFRE.search(l.text)]
        if not dites:
            detail = f" (à l'écran : « {script.proof_on_screen} »)" if script.proof_on_screen else ""
            v.fails.append(
                f"[preuve-muette] la preuve n'est pas prononcée{detail} : un fait qu'on ne dit pas "
                "n'existe pas pour qui écoute au volant (§3, temps 4)"
            )
        if script.duree_connue and preuves:
            debut = min(l.start for l in preuves)
            if debut > script.total * PREUVE_MAX:
                v.warn(
                    f"[preuve-tardive] la preuve arrive à {debut:.1f} s sur {script.total:.1f} s "
                    f"(après {PREUVE_MAX:.0%} de la pièce)"
                )

    # 4 · le rehook, entre le corps et la sortie
    corps = [i for i, l in enumerate(lines) if "corps" in l.roles]
    rehooks = [i for i, l in enumerate(lines) if "rehook" in l.roles]
    sorties = [i for i, l in enumerate(lines) if "sortie" in l.roles]
    if not rehooks:
        v.fails.append(
            "[pas-de-rehook] aucun beat ne relance : c'est le défaut exact de la v4 — l'attention "
            "tombe au milieu et rien ne la remonte (§3 bis)"
        )
    elif corps:
        # Le rehook vit **entre** deux blocs de corps : au moins un corps avant lui, au moins un après,
        # et avant la sortie. C'est la forme du squelette Kallaway (body1 → rehook → body2) ; un rehook
        # collé après le CTA ne relance plus rien.
        borne = max(sorties) if sorties else len(lines)
        bon = any(
            any(c < i for c in corps) and any(c > i for c in corps) and i < borne
            for i in rehooks
        )
        if not bon:
            v.fails.append(
                "[rehook-mal-place] le rehook doit venir entre deux blocs de corps, avant la sortie "
                f"(corps {[c + 1 for c in corps]}, rehook {[r + 1 for r in rehooks]}, "
                f"sortie {[s + 1 for s in sorties] or 'aucune'})"
            )

    # 5 · la sortie, une seule, et alignée sur la promesse
    if not sorties:
        v.fails.append("[sortie-absente] aucun beat de sortie : la pièce ne demande rien (§3, temps 5)")
    elif len(sorties) > 1:
        v.fails.append(f"[deux-cta] {len(sorties)} beats de sortie : deux CTA, c'est zéro CTA")
    else:
        if sorties[-1] != len(lines) - 1:
            v.fails.append(f"[sortie-mal-placee] la sortie est le beat {sorties[-1] + 1}, "
                           f"pas le dernier ({len(lines)})")
        if script.promise:
            texte = lines[sorties[-1]].text.lower()
            if script.promise.lower() not in texte:
                v.fails.append(
                    f"[cta-non-aligne] le CTA ne prononce pas « {script.promise} » : le *lead magnet* "
                    "doit correspondre à ce que la vidéo promet (`VIDEOS-2026-10-23-AUDIT` §6)"
                )

    # 6 · la liste empilée : quatre arguments dans un seul beat
    for l in lines:
        if l.text.count(",") >= 3 and "preuve" not in l.roles:
            v.fails.append(
                f"[liste-sans-axe] {l.name} empile {l.text.count(',') + 1} éléments : la doctrine "
                "veut « un objet, un seul axe » (§3, temps 3)"
            )

    # 7 · ni peur, ni promesse
    for l in lines:
        if PEUR.search(l.text):
            v.fails.append(f"[urgence] {l.name} : « {PEUR.search(l.text).group(0)} » — l'urgence "
                           "fabriquée est exclue (ruling 25/10)")
        if PROMESSE.search(l.text):
            v.fails.append(f"[promesse] {l.name} : « {PROMESSE.search(l.text).group(0)} » — aucune "
                           "promesse de résultat")

    # 8 · le miroir (avertissement : on peut s'en passer, à condition de le savoir)
    if not any("corps" in l.roles for l in lines) and not any("preuve" in l.roles for l in lines):
        v.warn("[pas-de-miroir] aucun beat ne dit ce que ça coûte (temps 2)")

    # 9 · le cadeau enterré — le défaut mesuré de la v4
    if script.duree_connue:
        cadeaux = [l for l in lines if CADEAU.search(l.text)]
        if cadeaux:
            premier = min(l.start for l in cadeaux)
            if premier > script.total * CADEAU_MAX:
                v.warn(
                    f"[cadeau-tardif] l'offre gratuite arrive à {premier:.1f} s sur {script.total:.1f} s "
                    f"(après {CADEAU_MAX:.0%}) : c'est le meilleur argument, il se dit tôt"
                )
        # 10 · le débit
        mots = sum(l.mots for l in lines)
        debit = mots / script.total if script.total else 0
        if not (DEBIT[0] <= debit <= DEBIT[1]):
            v.warn(f"[debit] {debit:.1f} mots/s (attendu {DEBIT[0]}–{DEBIT[1]}) : ce n'est plus la "
                   "vitesse d'une voix, c'est une lecture")

    # 11 · le hook ne doit pas manger le contexte (5 s)
    if script.duree_connue and lines[0].duree > CONTEXTE_MAX:
        v.warn(f"[hook-long] {lines[0].duree:.1f} s > {CONTEXTE_MAX:.0f} s de contexte")

    # 12 · deux verbes de CTA différents = deux CTA déguisés
    verbes = {m.lower() for l in lines for m in VERBES_CTA.findall(l.text)}
    if len(verbes) > 1:
        v.fails.append(f"[deux-cta] {len(verbes)} verbes d'action différents : {', '.join(sorted(verbes))}")

    return v


# ── lecture d'un module de pièce ─────────────────────────────────────────────────────────────────


def load_script(path: str) -> Script:
    """Importe le module et cherche `SCRIPT`. Les durées viennent de `SCRIPT.lines` si elles sont
    posées, sinon du `timing.json` voisin (c'est la voix qui décide, pas le plan)."""
    p = Path(path).resolve()
    spec = importlib.util.spec_from_file_location(f"piece_{p.stem}", p)
    if spec is None or spec.loader is None:
        raise SystemExit(f"module illisible : {p}")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(p.parent))
    sys.path.insert(0, str(p.parent.parent.parent / "tools" / "qa"))
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
    except SystemExit as e:  # un module qui sort tout seul (argparse) : on le dit
        raise SystemExit(f"[load] le module a quitté : {e}")
    script = getattr(mod, "SCRIPT", None)
    if script is None:
        raise SystemExit(f"{p.name} ne déclare pas SCRIPT — la pièce n'est pas lisible par la porte")
    if not script.piece:
        script.piece = p.stem.replace("make_", "")

    if not script.duree_connue:
        timing = p.parent / "voice" / "timing.json"
        if timing.exists():
            import json

            t = json.load(open(timing, encoding="utf-8"))
            par_nom = {b["name"]: b for b in t.get("beats", [])}
            # `timing.json` ne stocke pas les bornes : il stocke des **durées**. On les cumule dans
            # l'ordre du fichier — c'est l'ordre des beats, et c'est ce que le mux utilise.
            curseur = 0.0
            for l in script.lines:
                b = par_nom.get(l.name)
                if not b:
                    continue
                duree = float(b.get("duration") or b.get("voice") or 0)
                l.start, l.end = round(curseur, 3), round(curseur + duree, 3)
                curseur += duree
    return script


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    total_ko = 0
    for arg in argv:
        script = load_script(arg)
        v = audit(script)
        entete = f"{script.piece or Path(arg).stem}"
        if script.duree_connue:
            entete += f" · {script.total:.1f} s · {len(script.lines)} beats"
        else:
            entete += f" · {len(script.lines)} beats (durées inconnues : timing.json absent)"
        if v.ok:
            print(f"✓ {entete}")
        else:
            total_ko += 1
            print(f"✗ {entete}")
        for w in v.warns:
            print(f"   ⚠ {w}")
        for f in v.fails:
            print(f"   ⛔ {f}")
    return 1 if total_ko else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
