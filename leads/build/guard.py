#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GARDE-FOU ANTI-RETOUR-EN-ARRIÈRE DES GÉNÉRATEURS DU CRM.

Pourquoi ça existe (22/09 00:25, consigné dans sales/Activity-Log.md) : le bac a été restauré depuis
un instantané et a rendu des versions **antérieures** de `crm.py`, `views.py`, `records.py` et
`rebuild.sh` — celles d'avant l'enrichissement `EVENING_2109`. Comme `rebuild.sh` est la SEULE source
de `leads/CRM.csv` et de toutes les vues, le premier run a **réécrit le CRM sans l'état des deux fils
chauds** : `univers-optique` et `le-cristallin` repassés de `closing` à `prospecting`, relance du
22/09 effacée, note vocale du Cristallin envolée. Aucun message, aucun cri — juste un fichier d'état
redevenu muet. Ce qui doit être vrai ne peut pas reposer sur « je ferai attention » : d'où une
empreinte des générateurs, vérifiée AVANT que quiconque régénère le CRM.

Ce que cette machine NE fait pas, et qu'il faut dire : elle ne prouve pas que la nouvelle version est
meilleure, elle prouve qu'elle est **différente de ce qui a été validé**. Le jugement reste humain —
c'est le contrat de la maison : une promesse d'attention n'existe que si un contrôle la porte.

Usage :
    python3 leads/build/guard.py check    # avant de générer ; rc=1 si un générateur a bougé
    python3 leads/build/guard.py lock     # enregistre l'empreinte après un changement voulu
Court-circuit assumé : `AMK_GUARD_OK=1 bash leads/build/rebuild.sh`
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WATCH = ["leads/build/crm.py", "leads/build/views.py", "leads/build/records.py",
         "leads/build/rebuild.sh", "leads/build/guard.py"]
LOCK = HERE / "generators.lock.json"


def digests():
    out = {}
    for rel in WATCH:
        p = ROOT / rel
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.exists() else "ABSENT"
    return out


def touched_in_worktree(rel):
    """True si le fichier est modifié dans l'arbre par rapport à HEAD : un changement VOLONTAIRE, visible."""
    return subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet", "HEAD", "--", rel],
                          capture_output=True).returncode != 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    cur = digests()

    if mode == "lock":
        LOCK.write_text(json.dumps({"digests": cur, "why": "verrou rejoué à la main"},
                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("✓ empreinte des générateurs enregistrée — %d fichiers" % len(cur))
        return 0

    if os.environ.get("AMK_GUARD_OK") == "1":
        print("! garde-fou court-circuité (AMK_GUARD_OK=1) : run assumé, vérifie ce que tu écris")
        return 0

    if not LOCK.exists():
        LOCK.write_text(json.dumps({"digests": cur, "why": "premier run — empreinte initiale"},
                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("· empreinte initiale des générateurs posée (premier run) — rien à signaler")
        return 0

    prev = json.loads(LOCK.read_text(encoding="utf-8")).get("digests", {})
    drift = [k for k in WATCH if prev.get(k) != cur.get(k)]
    if not drift:
        return 0

    print("✗ GARDE-FOU : un ou plusieurs GÉNÉRATEURS DU CRM ne correspondent plus au verrou validé")
    print("  dernier verrou : %s (%s)" % (LOCK.name, prev.get("written", "?")))
    for rel in drift:
        old, new = prev.get(rel, "?"), cur[rel]
        if touched_in_worktree(rel):
            etat = "modifié dans l'arbre — visible dans `git diff HEAD -- %s`, donc peut-être voulu" % rel
        else:
            etat = ("IDENTIQUE à HEAD mais différent du verrou : retour en arrière probable "
                    "(restauration d'instantané, checkout partiel) — PAS ta plume")
        print("    %s\n        %s → %s · %s" % (rel, old, new, etat))
    print("  Ce qui est en jeu : ces fichiers sont la SEULE SOURCE de leads/CRM.csv, des fiches")
    print("  leads/records/*.md et des vues PIPELINE / KILL-LIST / STALE / Daily-Plan. Une version")
    print("  plus ancienne ne casse rien d'apparent : elle RECOMMENCE l'histoire et Perd l'état des")
    print("  leads, silencieusement. C'est exactement l'accident du 22/09, 00:20.")
    print("  À faire, dans l'ordre :")
    print("    1) git diff HEAD -- leads/build/            (lire ce qui a bougé)")
    print("    2) si c'est toi : python3 leads/build/guard.py lock")
    print("       si ce n'est pas toi : git checkout HEAD -- leads/build/")
    print("    3) bash leads/build/rebuild.sh               (régénérer depuis les bons générateurs)")
    print("  Échapper en conscience : AMK_GUARD_OK=1 bash leads/build/rebuild.sh")
    return 1


if __name__ == "__main__":
    sys.exit(main())
