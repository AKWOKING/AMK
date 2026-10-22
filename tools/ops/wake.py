#!/usr/bin/env python3
"""wake — remettre le dépôt au vrai état avant de lire ou d'écrire quoi que ce soit.

Le problème
-----------
Dans cet environnement, le dépôt **n'est pas persistant de façon fiable**. À chaque
réapprovisionnement du bac, un **clone neuf** est créé depuis GitHub et la branche de session est
replacée sur le **commit de début de session** — pas sur son dernier commit poussé. Le reflog le
montre :

    471bc84  clone: from https://github.com/AKWOKING/AMK.git
    b134dd2  checkout: moving from main to arena/2fffee3b-amk
    b134dd2  branch: Created from b134dd2d…

Conséquence observée quatre fois le 22/10/2026 : le travail local disparaît, et surtout **on lit un
arbre périmé en croyant lire le dépôt**. C'est ce qui a produit deux affirmations fausses dans la
même journée (« frames.json est vide », « la semaine 3 est bloquée faute de photos »), alors que les
40 montures et les 65 images étaient versionnées.

Ce que fait ce script
---------------------
1. récupère la branche depuis `origin` ;
2. compare `HEAD` au sommet distant ;
3. si le local est **en retard** : sauvegarde d'abord toute modification non commitée
   (patch + archive des fichiers non suivis, dans `/tmp`), puis `git reset --hard` sur le sommet ;
4. si le local est **en avance** : pousse les commits (le travail ne doit jamais rester local) ;
5. si les deux ont **divergé** : ne touche à rien et explique quoi faire ;
6. affiche un état vérifiable : branche, sommet, nombre de commits, fichiers modifiés.

Usage
-----
    python3 tools/ops/wake.py             # vérifie et répare
    python3 tools/ops/wake.py --check     # ne modifie rien, code 1 si périmé (gardien pour les outils)
    python3 tools/ops/wake.py --branch X  # autre branche

Règle d'usage : **premier appel de chaque tour**, avant toute lecture ou mesure. Un chiffre lu sur
un arbre non vérifié n'est pas un chiffre.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tarfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} a échoué :\n{r.stderr.strip()}")
    return r.stdout.strip()


def ok(*args: str) -> bool:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True).returncode == 0


def current_branch() -> str:
    b = git("rev-parse", "--abbrev-ref", "HEAD")
    return b if b != "HEAD" else ""


def save_wip() -> Path | None:
    """Sauvegarde les changements non commités avant tout reset. Retourne le dossier, ou None."""
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    if not dirty:
        return None
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = Path("/tmp") / f"amk-wip-{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    diff = subprocess.run(["git", "diff", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout
    (out / "changes.patch").write_text(diff, encoding="utf-8")
    untracked = subprocess.run(["git", "ls-files", "-o", "--exclude-standard"], cwd=ROOT,
                               capture_output=True, text=True).stdout.splitlines()
    if untracked:
        with tarfile.open(out / "untracked.tar.gz", "w:gz") as tar:
            for rel in untracked:
                p = ROOT / rel
                if p.exists():
                    tar.add(p, arcname=rel)
    (out / "status.txt").write_text(dirty + "\n", encoding="utf-8")
    return out


def report(branch: str, head: str, tip: str, log_lines: list[str], dirty: list[str]) -> None:
    print(f"\nbranche      {branch}")
    print(f"local        {head[:12]}")
    print(f"origin       {tip[:12]}")
    print(f"commits      {git('rev-list', '--count', f'b134dd2..{head}', check=False) or '?'} depuis la base de session")
    print("5 derniers   " + " | ".join(log_lines))
    print(f"modifiés     {len(dirty)}" + (f" → {', '.join(dirty[:6])}" if dirty else " (arbre propre)"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", default="")
    ap.add_argument("--check", action="store_true", help="ne modifie rien ; code 1 si périmé")
    args = ap.parse_args(argv[1:])

    branch = args.branch or current_branch()
    if not branch:
        print("✗ HEAD détaché — impossible de déterminer la branche. Rien n'est touché.")
        return 1

    subprocess.run(["git", "fetch", "origin", branch, "--quiet"], cwd=ROOT,
                   capture_output=True)
    if not ok("rev-parse", "--verify", f"origin/{branch}"):
        print(f"✗ origin/{branch} introuvable après fetch. Rien n'est touché.")
        return 1

    head = git("rev-parse", "HEAD")
    tip = git("rev-parse", f"origin/{branch}")
    log_lines = git("log", "--oneline", "-5", "--format=%h %s").splitlines()
    dirty = [l[3:] for l in git("status", "--porcelain").splitlines()]

    if head == tip:
        report(branch, head, tip, log_lines, dirty)
        print("\nVERDICT : À JOUR — l'arbre est le vrai dépôt.\n")
        return 0

    if ok("merge-base", "--is-ancestor", head, tip):
        behind = git("rev-list", "--count", f"{head}..{tip}")
        if args.check:
            print(f"\n✗ PÉRIMÉ — le local est en retard de {behind} commit(s) sur origin/{branch}.\n")
            return 1
        wip = save_wip()
        git("reset", "--hard", tip)
        log_lines = git("log", "--oneline", "-5", "--format=%h %s").splitlines()
        report(branch, tip, tip, log_lines, [])
        print(f"\nRÉPARÉ — le local est en retard de {behind} commit(s) : remis sur origin/{branch}.")
        if wip:
            print(f"⚠ des changements non commités ont été mis de côté AVANT le reset : {wip}")
            print("  (changes.patch + untracked.tar.gz — à réappliquer à la main si nécessaire)")
        print()
        return 0

    if ok("merge-base", "--is-ancestor", tip, head):
        ahead = git("rev-list", "--count", f"{tip}..{head}")
        if args.check:
            print(f"\n✗ NON POUSSÉ — {ahead} commit(s) présents en local et absents d'origin/{branch}.\n")
            return 1
        if dirty:
            print(f"⚠ {len(dirty)} fichier(s) modifié(s) non commité(s) — ils ne seront pas poussés.")
        r = subprocess.run(["git", "push", "origin", f"HEAD:{branch}"], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"✗ le push a échoué :\n{r.stderr.strip()}")
            return 1
        report(branch, head, head, log_lines, dirty)
        print(f"\nPOUSSÉ — {ahead} commit(s) n'existaient qu'en local, ils sont maintenant sur origin/{branch}.\n")
        return 0

    print("\n✗ DIVERGÉ — le local et origin ne partagent pas la même histoire. Rien n'est touché.")
    print(f"  local : {head[:12]} · origin : {tip[:12]}")
    print("  À traiter à la main : `git log --oneline --graph --all -20`, puis décider quoi garder.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
