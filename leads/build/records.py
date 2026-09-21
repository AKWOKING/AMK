#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — CRM microtâche M3 : générer `leads/records/<slug>.md`

**Pourquoi ils sont générés et non écrits à la main.** L'audit §9 demandait « 13-15 fiches » ;
il y en a **39** avec un historique réel, et ce nombre grandit chaque jour. Une fiche écrite à la
main redevient fausse en trois envois — c'est exactement ce qui est arrivé à `Daily Ops.csv`.
Générer la fiche depuis le CRM **et** le journal garantit qu'elle dit toujours la vérité du jour.

**Ce que la fiche contient :**
  · l'identité et l'état, **lus dans `leads/CRM.csv`** (jamais ressaisis)
  · l'historique : **les lignes de `sales/Activity-Log.md` qui citent ce lead** (le journal reste
    la source de vérité chronologique, append-only, il n'est pas recopié — il est cité)
  · la prochaine action, déduite des règles de relance
  · une section libre en bas, pour ce qu'un humain veut ajouter à la main

⚠️ **Ce fichier est GÉNÉRÉ.** Toute modification manuelle est perdue au prochain passage.
Ce qu'on veut garder à la main se met dans `sales/Activity-Log.md`, et remonte ici tout seul.

Usage :  python3 leads/build/records.py
"""
import csv
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
CRM = ROOT / "leads" / "CRM.csv"
LOG = ROOT / "sales" / "Activity-Log.md"
OUT = ROOT / "leads" / "records"

GEN_NOTE = ("> ⚙️ **Fiche générée** par `leads/build/records.py` le {date}. "
            "Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, "
            "et remontent ici au passage suivant.\n")

# Ce qui, dans une ligne du journal, désigne un lead sans ambiguïté possible.
def norm_txt(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).lower()


def digits(s) -> str:
    d = re.sub(r"\D", "", str(s or ""))
    # un numéro camerounais stocké « 694 57 22 77 » → 694572277 ; avec indicatif → 9 derniers
    return d[-9:] if len(d) >= 9 else d


def name_tokens(name: str) -> set:
    """Mots d'un nom de lead qui POURRAIENT servir de clé (≥6 lettres)."""
    return {norm_txt(w) for w in re.split(r"[^A-Za-zÀ-ÿ0-9']+", str(name or ""))
            if len(norm_txt(w)) >= 6}


def distinctive_tokens(all_names: list) -> set:
    """**Le cœur de la justesse de ce générateur.**

    Une liste noire de mots génériques ne marche pas : j'avais écrit « clinique » et oublié
    « clinic » — et JOSS MEDI Clinic a hérité de la ligne de « Douala clinic » (fausse
    attribution, trouvée et corrigée le 19/09). On ne tient pas une liste de mots interdits :
    on regarde le corpus.

    **Règle : un mot ne peut servir de clé que s'il n'apparaît que dans le nom d'UN SEUL lead.**
    « clinic », « centre », « medical », « douala » apparaissent dans plusieurs noms → écartés
    automatiquement. « bonanjo » ou « unilabo » n'apparaissent qu'une fois → utilisables.
    """
    seen = {}
    for nm in all_names:
        for tok in name_tokens(nm):
            seen[tok] = seen.get(tok, 0) + 1
    return {tok for tok, n in seen.items() if n == 1}


def lead_keys(rec: dict, distinctive: set) -> list:
    """Motifs qui, dans le journal, ne peuvent désigner que ce lead."""
    keys = []
    num = digits(rec.get("wa_number"))
    if len(num) == 9:
        keys.append(("num", num))
    for tok in name_tokens(str(rec.get("School") or "")):
        if tok in distinctive:
            keys.append(("name", tok))
    return keys


def journal_lines() -> list:
    if not LOG.exists():
        return []
    out = []
    for i, line in enumerate(LOG.read_text(encoding="utf-8").splitlines(), 1):
        n = norm_txt(line)
        if any(n.strip() for _ in [0]):
            out.append((i, line, n))
    return out


def matches_for(rec: dict, lines: list, distinctive: set) -> list:
    """Lignes du journal qui citent CE lead. Le numéro est la preuve la plus forte ;
    un mot du nom ne compte que s'il n'appartient qu'à ce lead (voir distinctive_tokens)."""
    keys = lead_keys(rec, distinctive)
    if not keys:
        return []
    hits = []
    for i, raw, n in lines:
        hit = False
        for kind, k in keys:
            if kind == "num" and k in re.sub(r"\D", "", raw) and len(k) == 9:
                hit = True
                break
            if kind == "name" and k in n:
                hit = True
                break
        if hit:
            hits.append((i, raw))
    return hits


def next_action(rec: dict) -> str:
    """Déduite des règles de relance. Rien n'est inventé : si la règle ne s'applique pas, on le dit."""
    stage = rec.get("stage", "")
    if stage in ("lost", "disqualified"):
        return "**Aucune.** Lead écarté — " + (rec.get("disqualification_reason") or "motif dans le CRM")
    if stage == "parked":
        return ("**Aucune.** Parqué"
                + (" — " + rec["disqualification_reason"] if rec.get("disqualification_reason") else "")
                + ". Une action n'est légitime que si King le décide explicitement.")
    if stage in ("prospect", "prospecting"):
        return "**Prospecter** : vérifier l'identité du numéro sur WhatsApp avant d'écrire (nom + catégorie)."
    if rec.get("Reply", "").strip().lower().startswith("yes"):
        return ("**Répondre dans l'heure.** Une réponse humaine est en attente : c'est la priorité absolue "
                "(règle des 90 secondes).")
    fu = rec.get("follow_ups_sent", "0") or "0"
    try:
        n_fu = int(str(fu).strip() or 0)
    except ValueError:
        n_fu = 0
    if n_fu >= 3:
        return "**Arrêt.** 3 relances envoyées — plafond atteint, le lead passe `parked`."
    return (f"**{n_fu} relance(s) sur 3 envoyée(s).** Prochaine relance au rythme M+2 / M+4 / M+7 "
            f"depuis le dernier message. Jamais deux relances le même jour.")


def render(rec: dict, hits: list, today: str) -> str:
    slug = rec["slug"]
    name = rec.get("School") or slug
    L = []
    L.append(f"# {name}\n")
    L.append(GEN_NOTE.format(date=today))
    L.append("## État (lu dans `leads/CRM.csv`)\n")
    L.append("| Champ | Valeur |")
    L.append("|---|---|")
    for label, key in [
        ("Slug", "slug"), ("Type", "org_type"), ("Ville", "City"), ("Langue de contact", "Language"),
        ("Étape", "stage"), ("WhatsApp", "wa_number"), ("Numéro vérifié", "wa_verified"),
        ("Profil vu", "profile_name_seen"), ("Contact", "Decision maker"),
        ("Canal", "Contact channel"), ("Contacté", "Contacted"), ("Réponse", "Reply"),
        ("Maquette / site", "Demo made"), ("Relances envoyées", "follow_ups_sent"),
        ("Source", "source"), ("Détail source", "source_detail"),
        ("Site vérifié le", "site_checked_on"),
    ]:
        v = str(rec.get(key) or "").strip()
        if v:
            L.append(f"| {label} | {v} |")
    if rec.get("site_url"):
        L.append(f"| Site existant | {rec['site_url']} |")
    if rec.get("wa_number_note"):
        L.append(f"| Numéro inutilisable | {rec['wa_number_note']} |")
    L.append("")

    if rec.get("disqualification_reason"):
        L.append("## Pourquoi il est écarté\n")
        L.append(str(rec["disqualification_reason"]) + "\n")

    if rec.get("contradiction"):
        L.append("## Contradiction résolue (M2)\n")
        L.append(f"- **Ce qui se contredisait :** {rec['contradiction']}")
        if rec.get("value_kept"):
            L.append(f"- **Retenu :** {rec['value_kept']}")
        if rec.get("value_discarded"):
            L.append(f"- **Écarté :** {rec['value_discarded']}")
        L.append("")

    if rec.get("Notes"):
        L.append("## Notes\n")
        L.append(str(rec["Notes"]).strip() + "\n")

    L.append("## Prochaine action\n")
    L.append(next_action(rec) + "\n")

    L.append("## Historique — lignes du journal qui citent ce lead\n")
    if hits:
        L.append(f"*Source : `sales/Activity-Log.md` — citation, jamais recopie. {len(hits)} ligne(s).*\n")
        for i, raw in hits:
            L.append(f"`L{i}` · {raw.strip()}")
        L.append("")
    else:
        L.append("*Aucune ligne du journal ne cite encore ce lead. S'il a été contacté, "
                 "c'est que l'envoi n'a pas été loggé — **à corriger dans `Activity-Log.md`**.*\n")

    L.append("---\n")
    L.append("## À la main (facultatif)\n")
    L.append("*Ce que tu écris ici est perdu au prochain passage du générateur. "
             "Pour garder une information, mets-la dans `sales/Activity-Log.md`.*\n")
    return "\n".join(L)


def main() -> int:
    if not CRM.exists():
        sys.exit(f"✗ {CRM} absent — lancer d'abord leads/build/crm.py")
    rows = list(csv.DictReader(CRM.open(encoding="utf-8-sig")))
    lines = journal_lines()
    distinctive = distinctive_tokens([r.get("School", "") for r in rows])
    OUT.mkdir(parents=True, exist_ok=True)

    import datetime
    today = datetime.date.today().isoformat()

    written, no_hist, by_stage = 0, [], {}
    for rec in rows:
        if not rec.get("slug"):
            continue
        # on ne crée une fiche que pour un lead avec un historique réel
        real = (rec.get("Contacted", "").strip().lower().startswith(("yes", "sent"))
                or rec.get("wa_verified") == "yes"
                or rec.get("stage") in ("qualified", "qualifying", "presented", "closing", "parked", "lost", "disqualified"))
        if not real:
            continue
        hits = matches_for(rec, lines, distinctive)
        if not hits and not rec.get("Notes"):
            no_hist.append(rec["slug"])
        path = OUT / f"{rec['slug']}.md"
        path.write_text(render(rec, hits, today), encoding="utf-8")
        written += 1
        by_stage[rec.get("stage", "")] = by_stage.get(rec.get("stage", ""), 0) + 1

    # on nettoie les fiches dont le slug n'existe plus dans le CRM
    known = {r["slug"] for r in rows}
    removed = []
    for old in OUT.glob("*.md"):
        if old.stem not in known:
            old.unlink()
            removed.append(old.name)

    print(f"✓ {written} fiches écrites dans leads/records/")
    print("  par étape :", " · ".join(f"{k or '(vide)'}={v}" for k, v in sorted(by_stage.items())))
    print(f"  citations du journal trouvées : {sum(1 for r in rows if matches_for(r, lines, distinctive))} lead(s)")
    print(f"  mots distinctifs utilisables : {len(distinctive)}")
    if no_hist:
        print(f"  ⚠ {len(no_hist)} fiche(s) sans citation du journal : {', '.join(no_hist[:6])}"
              + (" …" if len(no_hist) > 6 else ""))
    if removed:
        print(f"  {len(removed)} fiche(s) orpheline(s) supprimée(s) : {', '.join(removed[:5])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
