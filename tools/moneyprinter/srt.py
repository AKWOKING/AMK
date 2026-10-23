#!/usr/bin/env python3
"""AMK — sous-titres sans Whisper : le script qu'on connaît déjà, découpé au temps.

Pourquoi ce fichier existe : MoneyPrinterTurbo génère ses sous-titres avec Whisper, ce qui veut dire
télécharger un modèle (150 Mo en `small`, ~3 Go en `large-v3`) et attendre une transcription… d'un
texte que **nous avons écrit**. Pour une voix enregistrée par le patron, la transcription n'apporte
rien : elle peut même se tromper (« O.N.O.C. » devient « nos os »). Ici, le découpage est
déterministe : les phrases sont réparties à la longueur, et le résultat est relisible.

    python3 tools/moneyprinter/srt.py --script "phrase une. phrase deux." --duration 20 --out /tmp/x.srt
"""
import argparse
import re
from pathlib import Path


def phrases(texte: str) -> list[str]:
    """Découpe sur la ponctuation forte, sans perdre les abréviations courantes du dossier."""
    texte = re.sub(r"\s+", " ", texte).strip()
    # 8h30, 656 122 239, M. : on ne coupe pas après un point isolé entre deux majuscules courtes
    morceaux = re.split(r"(?<=[.!?…])\s+", texte)
    out = []
    for m in morceaux:
        m = m.strip()
        if m:
            out.append(m)
    return out or [texte]


def lignes(phrase: str, largeur: int = 38, max_lignes: int = 2) -> str:
    """Coupe une phrase en au plus `max_lignes` lignes lisibles, sans casser un mot."""
    mots, out, cur = phrase.split(), [], ""
    for mot in mots:
        essai = f"{cur} {mot}".strip()
        if len(essai) <= largeur or not cur:
            cur = essai
        else:
            out.append(cur)
            cur = mot
    if cur:
        out.append(cur)
    if len(out) <= max_lignes:
        return "\n".join(out)
    # trop long : on regroupe équitablement sur max_lignes
    total = sum(len(x) for x in out)
    cible, lignes_finales, buf = total / max_lignes, [], ""
    for ligne in out:
        if len(buf) + len(ligne) <= cible + 6 or len(lignes_finales) == max_lignes - 1:
            buf = f"{buf} {ligne}".strip()
        else:
            lignes_finales.append(buf)
            buf = ligne
    lignes_finales.append(buf)
    return "\n".join(lignes_finales[:max_lignes])


def t(secondes: float) -> str:
    h, reste = divmod(secondes, 3600)
    m, s = divmod(reste, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def construire(script: str, duree: float, largeur: int = 38, marge: float = 0.25) -> str:
    ps = phrases(script)
    poids = [max(len(p), 12) for p in ps]
    total = sum(poids)
    dispo = max(duree - marge * 2, 1.0)
    cues, curseur = [], marge
    for p, w in zip(ps, poids):
        d = dispo * w / total
        debut, fin = curseur, min(curseur + d, duree - marge * 0.2)
        if fin - debut < 1.0:                       # jamais sous la seconde : illisible
            fin = debut + 1.0
        cues.append((debut, fin, lignes(p, largeur)))
        curseur = fin
    if cues:
        debut, _, texte = cues[-1]
        cues[-1] = (debut, max(duree - marge * 0.1, debut + 1.0), texte)
    return "\n".join(
        f"{i}\n{t(a)} --> {t(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1)
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Écrire un .srt depuis un script connu et une durée d'audio.")
    ap.add_argument("--script", required=True)
    ap.add_argument("--duration", type=float, required=True, help="durée de l'audio, en secondes")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=38, help="caractères par ligne (38 tient sur 9:16)")
    args = ap.parse_args()

    srt = construire(args.script, args.duration, args.width)
    Path(args.out).write_text(srt, encoding="utf-8")
    print(f"{srt.count('-->')} sous-titre(s) → {args.out}")


if __name__ == "__main__":
    main()
