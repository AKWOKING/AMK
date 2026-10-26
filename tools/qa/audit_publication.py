#!/usr/bin/env python3
"""audit_publication — la porte de la PUBLICATION : ce qui se vérifie avant 12 h, pas après.

Pourquoi elle existe (26/10/2026, tour 152)
-------------------------------------------
King a décidé de publier EP01 v6 **le jour même**, à 12 h. La veille, quatre pièces existaient (le master,
la porte du récit, le CTA, le message d'accueil) et **aucune n'était réunie** : ni légende, ni bouton
prérempli, ni réponse prête, ni compteur. Une publication ne rate pas à cause du montage ; elle rate parce
que le lien n'était pas réglé, que la légende n'avait pas d'accroche dans les deux premières lignes, ou que
personne n'a répondu pendant trois heures.

Les règles ci-dessous étaient **écrites** dispersées dans quatre documents (`PLAYBOOK` §4, `ROAST` §3,
`CLIENT-MESSAGING-RULES` §13, `POSTING-CALENDAR` §E). Une règle sans porte est un trou : voilà la porte.

Ce qu'elle refuse (mesurable, jamais du goût)
---------------------------------------------
- `legende-absente` · le kit n'a pas de légende dans un bloc de code
- `accroche-longue` · la première ligne dépasse **100 caractères** (Facebook coupe avant « Voir plus »)
- `cta-absent` · aucun verbe d'action dans la légende
- `deux-cta` · **plus d'un** verbe d'action — un seul CTA, jamais deux (`PLAYBOOK` §0 ligne 2)
- `mot-cle-absent` · le mot-clé compté (`APERÇU`) n'est pas dans la légende
- `prix-dans-la-legende` · un prix, un « FCFA », un « k » dans un post public (décision du 08/10)
- `promesse` · « garanti », « plus de patients », « vous aurez » — une promesse de résultat
- `nom-tardif` · la réponse d'accueil ne demande pas le nom du cabinet **dans sa première ligne**
  (condition 2 du Roast)
- `delai-absent` · la réponse ne nomme aucune heure de livraison (condition 3 du Roast : le délai se dit
  dans le message, avec une heure)
- `lien-absent` · ni `wa.me` ni numéro WhatsApp dans le kit
- `compteur-absent` · le tableau de mesure n'a pas ses colonnes de décision
- `master-absent` / `master-trop-long` · le master manque, ou dépasse **25 s**

Ce qu'elle avertit
------------------
`delai-flou` · « bientôt », « rapidement », « dans les prochains jours » sans heure · `trop-de-blocs` ·
`legende-longue` (> 700 caractères) · `duree-inconnue` (aucun ffmpeg pour mesurer le master).

Comment on s'en sert
--------------------
    python3 tools/qa/audit_publication.py content/reels/ep01/PUBLICATION-2026-10-26.md \\
                                          content/reels/ep01/ep01-v6.mp4
    # → « ✓ publication · légende 5 blocs · master 23.7 s » et code 0, ou les refus et code 1
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

PLAFOND_MASTER = 25.0          # s — la même borne que `audit_reel`
ACCROCHE_MAX = 100             # caractères visibles avant « Voir plus »
LEGENDE_MAX = 700              # au-delà, personne ne lit

# ── les verbes qui demandent une action : un seul par publication ───────────────────────────────
VERBES_CTA = (
    "ecrivez", "envoyez", "appelez", "cliquez", "commentez", "reservez", "inscrivez",
    "ecrivez-moi", "envoyez-moi", "appelez-moi", "contactez",
)

# ── ce qui n'apparaît JAMAIS dans un post public ────────────────────────────────────────────────
PRIX = re.compile(r"\b(fcfa|prix|tarif)\b|\d+\s*k\b|\d{1,3}\s?000\b", re.I)
PROMESSES = (
    "garanti", "garantie", "garantis", "plus de patients", "plus de clients",
    "vous aurez", "certifie", "certifiee", "assure de", "resultat assure",
)
DELAI_FLOU = ("bientot", "rapidement", "dans les prochains jours", "sous peu", "des que possible")
HEURE = re.compile(r"\b\d{1,2}\s?h(\s?\d{2})?\b", re.I)
CONTACT = re.compile(r"wa\.me/\d{6,}|(\+?237\s?)?6[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}")

COLONNES_REQUISES = ("messages recus", "apercu", "conversations", "apercus envoyes")


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
    blocs: int = 0
    duree: float | None = None

    @property
    def ok(self) -> bool:
        return not self.fails


# ── lecture du kit ──────────────────────────────────────────────────────────────────────────────

def _sans_accent(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def _sections(texte: str) -> list[tuple[str, str]]:
    """Découpe sur les titres `## N · …` — la numérotation du kit est le contrat."""
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


def _blocs_de_code(corps: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", corps, re.S)]


def _lignes_citees(corps: str) -> str:
    """Les lignes en citation `>` — c'est là que vivent les messages à coller."""
    return "\n".join(l[2:].strip() for l in corps.splitlines() if l.startswith(">")).strip()


def legende(texte: str) -> str:
    sections = _sections(texte)
    return (_blocs_de_code(_section(sections, "2")) or [""])[0].strip()


def accueil(texte: str) -> str:
    return _lignes_citees(_section(_sections(texte), "4"))


def _tableau(corps: str) -> str:
    return "\n".join(l for l in corps.splitlines() if l.strip().startswith("|"))


def _premiere_ligne(texte: str) -> str:
    """La **première ligne** du message d'accueil — ce que WhatsApp affiche avant d'ouvrir le fil.

    Le Roast demande le nom du cabinet « dans la première ligne », pas dans la première phrase : une
    salutation et la question peuvent tenir sur la même ligne sans rien coûter (condition 2,
    `ROAST-2026-10-26-EP01-VENTE` §Tour 2).
    """
    plat = re.sub(r"\*\*|>", "", texte)
    for ligne in plat.splitlines():
        if ligne.strip():
            return ligne.strip()
    return ""


def _duree_master(chemin: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        r = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(chemin)],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and r.stdout.strip():
            return round(float(r.stdout.strip()), 2)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        try:  # le paquet imageio-ffmpeg fournit un binaire sans apt (cf. content/reels/README §2)
            import imageio_ffmpeg  # type: ignore

            ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            return None
    r = subprocess.run([ffmpeg, "-i", str(chemin)], capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr)
    if not m:
        return None
    h, mi, se = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return round(h * 3600 + mi * 60 + se, 2)


# ── la porte ────────────────────────────────────────────────────────────────────────────────────

def audit(chemin: str | Path, master: str | Path | None = None) -> Verdict:
    chemin = Path(chemin)
    texte = chemin.read_text(encoding="utf-8")
    v = Verdict()
    sections = _sections(texte)

    # ① la légende
    cap = legende(texte)
    if not cap:
        v.fails.append("[legende-absente] aucun bloc de code dans §2 — il n'y a rien à coller")
        cap = ""
    blocs = [b for b in cap.split("\n\n") if b.strip()]
    v.blocs = len(blocs)
    if cap:
        premiere = next((l for l in cap.splitlines() if l.strip()), "")
        if len(premiere) > ACCROCHE_MAX:
            v.fails.append(
                f"[accroche-longue] la première ligne fait {len(premiere)} caractères "
                f"(max {ACCROCHE_MAX}) — Facebook la coupe avant « Voir plus »"
            )
        if len(cap) > LEGENDE_MAX:
            v.warns.append(f"[legende-longue] {len(cap)} caractères (max conseillé {LEGENDE_MAX})")
        plat = _sans_accent(cap)
        verbes = sorted({x for x in VERBES_CTA if x in plat})
        if not verbes:
            v.fails.append("[cta-absent] aucun verbe d'action — une publication sans CTA ne déplace rien")
        elif len(verbes) > 1:
            v.fails.append(f"[deux-cta] {len(verbes)} actions demandées ({', '.join(verbes)}) — une seule")
        if "apercu" not in plat:
            v.fails.append("[mot-cle-absent] le mot-clé compté (APERÇU) n'est pas dans la légende")
        if PRIX.search(cap):
            v.fails.append(
                f"[prix-dans-la-legende] « {PRIX.search(cap).group(0)} » — un prix ne sort jamais en public "
                "(décision du 08/10, PLAYBOOK §0 ligne 5)"
            )
        for p in PROMESSES:
            if p in plat:
                v.fails.append(f"[promesse] « {p} » — on ne promet pas un résultat qu'on ne compte pas")
                break

    # ② la réponse d'accueil
    acc = accueil(texte)
    if not acc:
        v.fails.append("[nom-tardif] aucune réponse d'accueil citée dans §4")
    else:
        if "nom" not in _sans_accent(_premiere_ligne(acc)):
            v.fails.append(
                "[nom-tardif] la première ligne ne demande pas le nom du cabinet — "
                "condition 2 du ROAST-2026-10-26 (§Tour 2)"
            )
        if not HEURE.search(acc):
            v.fails.append(
                "[delai-absent] aucune heure de livraison — condition 3 du Roast : le délai se dit "
                "dans le message, avec une heure"
            )
        plat = _sans_accent(acc)
        for mot in DELAI_FLOU:
            if mot in plat:
                v.warns.append(f"[delai-flou] « {mot} » — nommer l'heure, pas l'intention")
                break

    # ③ le lien et le compteur
    if not CONTACT.search(texte):
        v.fails.append("[lien-absent] ni wa.me ni numéro WhatsApp — le chemin d'entrée n'existe pas")
    table = _tableau(_section(sections, "5"))
    plat_table = _sans_accent(table)
    manquantes = [c for c in COLONNES_REQUISES if c not in plat_table]
    if manquantes:
        v.fails.append(f"[compteur-absent] colonnes manquantes dans §5 : {', '.join(manquantes)}")

    # ④ le master
    if master is not None:
        m = Path(master)
        if not m.exists():
            v.fails.append(f"[master-absent] {m} n'existe pas")
        else:
            d = _duree_master(m)
            v.duree = d
            if d is None:
                v.warns.append("[duree-inconnue] aucun ffmpeg/ffprobe — la durée n'a pas été mesurée")
            elif d > PLAFOND_MASTER:
                v.fails.append(f"[master-trop-long] {d} s > {PLAFOND_MASTER} s")

    return v


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    kit = argv[0]
    master = argv[1] if len(argv) > 1 else None
    v = audit(kit, master)
    entete = f"publication · {v.blocs} bloc(s) de légende"
    if v.duree is not None:
        entete += f" · master {v.duree} s"
    if v.ok:
        print(f"✓ {entete}")
    else:
        print(f"✗ {entete}")
    for w in v.warns:
        print(f"   ⚠ {w}")
    for f in v.fails:
        print(f"   ⛔ {f}")
    return 0 if v.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
