#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — CRM : générer les tableaux de bord depuis `leads/CRM.csv`

**Reconstruit le 20/09/2026** après le 8e recul du bac à sable (le fichier précédent n'avait pas
été poussé). Toutes les corrections apprises le 19/09 y sont intégrées d'emblée :

  · **la kill list est DÉDUITE, pas écrite en dur** — le playbook §A4 mettait COMOBIL (parké depuis
    le 14/09) sur une liste « aujourd'hui ». Règle : score ≥ 18 ET non parké ET non disqualifié
    ET pas de réponse en attente.
  · **une réponse « déjà traitée » n'est PAS une réponse en attente** — la première version mettait
    St. Theresa en tête de file 4 jours après sa réponse, alors que le fil était planifié pour octobre.
  · **la décision humaine prime sur le calcul** — L'Opticien avait une relance fixée à dimanche ;
    le rythme M+2 le proposait le samedi. Table RELANCE_A_JOUR.
  · **un rendez-vous n'est pas une relance** — UNI-LABO a demandé une réunion : ce n'est plus un
    calcul de rythme, c'est un événement.

Aucune vue ne se modifie à la main (règle de l'audit §8 : un dérivé manuscrit redevient une source
concurrente — c'est exactement ce qui a produit l'onglet DAILY OPS périmé).

Usage :  python3 leads/build/views.py
"""
import csv
import datetime
import pathlib
import re
import sys
import unicodedata
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
CRM = ROOT / "leads" / "CRM.csv"
LOG = ROOT / "sales" / "Activity-Log.md"

GEN = ("> ⚙️ **Généré le {date} par `leads/build/views.py` — ne pas modifier à la main.**\n"
       "> Toute correction se fait dans `leads/build/crm.py` ou `sales/Activity-Log.md`, "
       "puis on relance `leads/build/rebuild.sh`.\n")

# M7 · AVERTISSEMENT D'ÉCRITURE (21/09) — lu à l'envers, c'est la source qui compte :
#   relancer `python3 leads/build/rebuild.sh` REGENERE leads/CRM.csv depuis le classeur +
#   les tables de crm.py. Les lignes VAGUE 1 (opticiens ONOC) y ont été portées dans
#   `OPTICIENS_2109`, donc rien n'est perdu — mais TOUT ajout écrit à la main dans le CSV
#   disparaît au prochain passage. Règle : un nouveau lot = un bloc dans `crm.py` ;
#   une décision = une table dans `crm.py` ; un envoi = une ligne dans `Activity-Log.md`.
# Vocabulaire M7 (21/09/2026) — décision King : le CRM parle maintenant les noms d'étape
# du funnel, plus `won`/`lost` (inexistants avant) + `delivered` (conservé : l'étape 5 du
# funnel — DELIVERY · PROOF · GROWTH — ne peut pas être absorbée par `won` sans perdre la
# distinction « payé » / « livré », qui est exactement là où meurt un client).
#    prospect → qualified → presented → closing → won → delivered        (vivant)
#    parked (réveil possible) · lost (déduit, motif en `disqualification_reason`)
STAGE_LABEL = {
    "prospect": "① Prospect — à qualifier",
    "qualified": "② Qualifié — en conversation",
    "presented": "③ Aperçu envoyé",
    "closing": "④ Offre posée / prix annoncé",
    "won": "⑤ Signé — dépôt reçu",
    "delivered": "⑥ Livré",
    "parked": "⏸ Parqué",
    "lost": "⛔ Perdu / écarté",
}
STAGE_ORDER = ["won", "closing", "presented", "qualified", "prospect", "parked", "lost"]
# Alias historiques — une seule énumération est stockée, les constantes ci-dessous évitent
# qu'un comparateur éparpillé continue à raisonner en ancien vocabulaire.
QUALIFIED, PROSPECT, CLOSED_STAGES = "qualified", "prospect", ("closing", "won")
DEAD = ("parked", "lost")

# Décisions humaines qui priment sur les règles automatiques : slug -> (échéance ISO, note)
RELANCE_A_JOUR = {
    "opticien-bali-douala": ("2026-09-20", "relances fixées dim 20 / mar 22 / ven 25"),
    # OraCare RETIRÉE de cette table le 21/09 : King a envoyé le message de clôture à 17:43 et le
    # fil est parqué. Une date de relance sur un fil fermé est une invitation à se griller.
    "midas-touch-optic-center-mitoc": ("2026-09-21", "FU2 fixée lun 21"),
    "baird-memorial-college": ("2026-09-21", "FU2 fixée lun 21 (même lot que MITOC)"),
    # AFRIQUE LABO : ajoutée le 21/09 quand on a trouvé le lead ABSENT du CRM (il ne vivait que
    # dans sales/Outreach-AFRIQUE-LABO-v1.md). Dates prises dans le §4 corrigé du 18/09 de ce fichier.
    "afrique-labo-sarl": ("2026-09-21", "FU2 (M+4) fixée lun 21 — §4 d'Outreach-AFRIQUE-LABO-v1.md"),
    "labiomed-deido": ("2026-09-21", "M+2 — il a dit « je vous reviens quand je serai disponible » (report poli, pas un non)"),
    # UNI-LABO a DEMANDÉ un rendez-vous : ce n'est plus une relance à calculer.
    "uni-labo-bonamoussadi": ("2026-09-25", "RENDEZ-VOUS demandé par le prospect — vendredi 25/09"),
}


def norm(s) -> str:
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).lower()


def digits(s) -> str:
    d = re.sub(r"\D", "", str(s or ""))
    return d[-9:] if len(d) >= 9 else d


def tokens(name: str) -> set:
    return {norm(w) for w in re.split(r"[^A-Za-zÀ-ÿ0-9']+", str(name or "")) if len(norm(w)) >= 6}


def load():
    if not CRM.exists():
        sys.exit("✗ leads/CRM.csv absent — lancer leads/build/crm.py d'abord")
    return [r for r in csv.DictReader(CRM.open(encoding="utf-8-sig")) if r.get("slug")]


def distinctive(rows) -> set:
    """Un mot ne sert de clé que s'il n'appartient qu'à UN lead.
    (Leçon du 19/09 : une liste noire de mots génériques avait laissé passer « clinic » et
    JOSS MEDI Clinic héritait de la ligne de « Douala clinic ».)"""
    seen = Counter()
    for r in rows:
        for t in tokens(r.get("School", "")):
            seen[t] += 1
    return {t for t, n in seen.items() if n == 1}


def journal_index(rows, dist) -> dict:
    lines = LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []
    idx = {}
    for r in rows:
        keys = []
        n = digits(r.get("wa_number"))
        if len(n) == 9:
            keys.append(n)
        keys += [t for t in tokens(r.get("School", "")) if t in dist]
        last, count = None, 0
        for i, raw in enumerate(lines, 1):
            ln = norm(raw)
            if any((k.isdigit() and k in re.sub(r"\D", "", raw)) or (not k.isdigit() and k in ln) for k in keys):
                count += 1
                last = (i, raw.strip())
        idx[r["slug"]] = (last, count)
    return idx


def last_send_age_days(r) -> int:
    """Âge du dernier message, lu dans les notes (« envoyé 17/09 »). -1 si inconnu."""
    txt = f"{r.get('Notes','')} {r.get('Contacted','')}"
    today = datetime.date.today()
    best = None
    for d, mo in re.findall(r"(\d{2})/(\d{2})", txt):
        try:
            cand = datetime.date(today.year, int(mo), int(d))
        except ValueError:
            continue
        if cand <= today:
            best = max(best, cand) if best else cand
    return (today - best).days if best else -1


def reply_pending(r) -> bool:
    """Une réponse est EN ATTENTE de nous ?

    ⚠️ Correction du 19/09 : la première version traitait toute ligne `Reply = YES` comme
    « répondre dans l'heure » — et mettait donc **St. Theresa** en tête de la file du jour,
    quatre jours après sa réponse, alors que le fil était **planifié pour octobre avec sa
    permission**. **Une mauvaise file du jour est pire que pas de file : elle fait relancer
    un client qui a déjà dit quand revenir.**
    """
    if not str(r.get("Reply", "")).strip().lower().startswith("yes"):
        return False
    if str(r.get("reply_type") or "").strip() == "auto":
        return False          # une réponse automatique n'est pas une réponse humaine
    fd = str(r.get("Follow-up date") or "").strip()
    if fd:
        years = re.findall(r"20\d\d-\d\d-\d\d", fd)
        if any(y > datetime.date.today().isoformat() for y in years):
            return False      # déjà planifié : pas une réponse à traiter maintenant
    conv = str(r.get("Conversation") or "").lower()
    if "parked" in conv or "await" in conv:
        return False
    if r.get("slug") in RELANCE_A_JOUR:
        return False          # une date a été fixée : le fil est organisé
    return True


def due_for_relance(r):
    """(échéance, pourquoi) ou (None, None). La décision humaine prime sur le rythme."""
    today = datetime.date.today()
    slug = r.get("slug", "")
    # Une décision humaine prime sur le rythme — mais PAS sur le palier : `parked`/`lost` ne sont
    # jamais « dus ». Trouvé le 21/09 : OraCare, parqué le soir même par King, ressortait en
    # « Relance 4/3 » dans la file. Une file qui ordonne de relancer un fil fermé fait perdre
    # la seule chose qui compte ici : la crédibilité du prochain message.
    if (r.get("stage") or "") in DEAD:
        return None, None
    if slug in RELANCE_A_JOUR:
        d, note = RELANCE_A_JOUR[slug]
        return (d, f"fixé : {note}") if d <= today.isoformat() else (None, None)
    if (r.get("stage") or "") != QUALIFIED:
        return None, None
    age = last_send_age_days(r)
    if age < 0:
        return None, None
    try:
        n = int(str(r.get("follow_ups_sent") or "0"))
    except ValueError:
        n = 0
    seuil = {0: 2, 1: 4, 2: 7}.get(n)
    if seuil and age >= seuil:
        return today.isoformat(), f"rythme M+{seuil} (message il y a {age} j)"
    return None, None


# ─────────────────────────────── vues ───────────────────────────────

def view_pipeline(rows, idx, date):
    L = ["# PIPELINE — où en est chaque lead\n", GEN.format(date=date)]
    c = Counter(r["stage"] or "(sans étape)" for r in rows)
    L += ["## Compteur\n", "| Étape | Leads |", "|---|---|"]
    for s in STAGE_ORDER + [""]:
        if c.get(s):
            L.append(f"| {STAGE_LABEL.get(s, '(sans étape)')} | **{c[s]}** |")
    L.append(f"| **Total** | **{len(rows)}** |\n")

    contacted = [r for r in rows if r.get("Contacted", "").strip().lower().startswith(("yes", "sent"))]
    human = [r for r in rows if str(r.get("reply_type") or "") == "human"]
    auto = [r for r in rows if str(r.get("reply_type") or "") == "auto"]
    L.append(f"- **Contactés :** {len(contacted)} · **Réponses humaines :** {len(human)}"
             + (f" · **Taux de réponse : {len(human)/len(contacted)*100:.1f} %**" if contacted else ""))
    L.append(f"- **Réponses automatiques (hors PRR) :** {len(auto)}")
    L.append("- **Clients :** 0 · **Revenu :** 0 FCFA\n")

    waiting = [r for r in rows if reply_pending(r)]
    L += ["## ⚡ Répondre d'abord\n"]
    if waiting:
        L += ["| Lead | WhatsApp | Ce qu'il a dit |", "|---|---|---|"]
        for r in waiting:
            L.append(f"| **{r['School']}** | {r.get('wa_number','')} | "
                     f"{re.sub(chr(10),' ',str(r.get('Reply','')))[:80]} |")
        L.append("\n> **Règle des 90 secondes.** Une réponse en attente passe avant tout le reste.\n")
    else:
        L.append("*Rien en attente.*\n")

    for s in STAGE_ORDER:
        group = [r for r in rows if (r.get("stage") or "") == s]
        if not group:
            continue
        L.append(f"## {STAGE_LABEL.get(s, s)} — {len(group)}\n")
        L += ["| Lead | Ville | WhatsApp | Trace au journal |", "|---|---|---|---|"]
        for r in sorted(group, key=lambda x: x["School"]):
            last, _ = idx.get(r["slug"], (None, 0))
            L.append(f"| {r['School']} | {r.get('City','')} | {r.get('wa_number') or '—'} | "
                     f"{'`L%d`' % last[0] if last else '—'} |")
        L.append("")
    return "\n".join(L)


def view_kill_list(rows, date):
    L = ["# KILL LIST — déduite, jamais écrite en dur\n", GEN.format(date=date)]
    L += ["## La règle (corrigée le 19/09)\n",
          "Le playbook §A4 disait « les 2 leads à 18 (COMOBIL, OraCare) ». **C'était faux** : "
          "COMOBIL est parké depuis le 14/09 (`leads/CONTRADICTIONS.md` §1).\n",
          "> **score >= 18 · ET étape non parkée · ET non écartée · ET pas de réponse en attente**\n"]

    def score(r):
        try:
            return int(float(str(r.get("Lead score") or 0)))
        except ValueError:
            return 0

    hot = [r for r in rows if score(r) >= 18
           and (r.get("stage") or "") not in DEAD
           and not reply_pending(r)]

    waiting = [r for r in rows if reply_pending(r)]
    L.append("## ⚡ Répondre d'abord\n")
    if waiting:
        for r in waiting:
            L.append(f"- **{r['School']}** — {r.get('wa_number','')}")
        L.append("\n> **Règle des 90 secondes.**\n")
    else:
        L.append("*Rien en attente.*\n")

    # ⚠️ Correction du 21/09 : cette section listait TOUTES les entrées de RELANCE_A_JOUR,
    # y compris celles dont la date est DÉJÀ PASSÉE — donc une relance due aujourd'hui
    # s'affichait « ne rien faire maintenant ». Contradiction entre deux sections du même
    # fichier généré. On n'affiche ici que les dates FUTURES ; les autres sont dans la file du jour.
    today_iso = datetime.date.today().isoformat()
    future = [(s, d, w) for s, (d, w) in sorted(RELANCE_A_JOUR.items()) if d > today_iso]
    L.append("## 📅 Décisions déjà prises — DATES À VENIR, ne rien faire maintenant\n")
    if future:
        for slug, d, why in future:
            row = next((r for r in rows if r["slug"] == slug), None)
            if row:
                L.append(f"- **{row['School']}** — {d} · {why}")
    else:
        L.append("*Aucune échéance future.*")
    L.append("")
    L.append("> Les échéances **déjà passées** sont dans `Daily-Plan.csv` — c'est la file de travail.\n")

    L.append("## 🎯 Score >= 18 et jouable\n")
    if hot:
        L += ["| Lead | Score | Ville | WhatsApp |", "|---|---|---|---|"]
        for r in sorted(hot, key=lambda x: -score(x)):
            L.append(f"| **{r['School']}** | {score(r)} | {r.get('City','')} | {r.get('wa_number') or '—'} |")
    else:
        L.append("**Aucun.** Le seul lead à 18 est COMOBIL, parké depuis le 14/09. "
                 "**C'est la vérité, pas un manque de prospection.**\n")
    L += ["## Ce qui alimente la liste quand elle est vide\n",
          "1. **Une réponse** — priorité absolue.\n"
          "2. **Un « oui » ou une demande de rendez-vous** → on construit, on pose le prix.\n"
          "3. **Un numéro vérifié** parmi les leads en prospection — c'est le vrai goulot : "
          "sans numéro confirmé, personne n'entre dans la liste.\n"]
    return "\n".join(L)


def view_stale(rows, idx, date):
    L = ["# STALE — ce qui dort\n", GEN.format(date=date),
         "**« Dormir » =** contacté, sans réponse, dernière trace au journal vieille de plus de **2 jours**. "
         "On relance au rythme **M+2 / M+4 / M+7**, jamais deux fois le même jour, **jamais plus de 3**.\n",
         "| Lead | Étape | Âge | Relances | Trace |", "|---|---|---|---|---|"]
    n = 0
    for r in rows:
        if not r.get("Contacted", "").strip().lower().startswith(("yes", "sent")):
            continue
        if str(r.get("Reply", "")).strip().lower().startswith("yes"):
            continue
        if (r.get("stage") or "") in DEAD:
            continue
        age = last_send_age_days(r)
        if age < 2:
            continue
        if r.get("slug") in RELANCE_A_JOUR:
            continue          # une date a été fixée : ce n'est pas un lead endormi
        n += 1
        last, _ = idx.get(r["slug"], (None, 0))
        L.append(f"| {r['School']} | {r.get('stage','')} | {age} j | "
                 f"{r.get('follow_ups_sent') or 0}/3 | {'`L%d`' % last[0] if last else '—'} |")
    if n == 0:
        L.append("| *(aucun)* | | | | |\n")
        L.append("**Aucun lead ne dort.** Tous les envois du 18 et 19/09 ont moins de deux jours — "
                 "**et c'est exactement pour ça que ce fichier est généré : demain, il changera tout seul.**")
    return "\n".join(L)


def view_sources(rows, date):
    L = ["# SOURCES — d'où viennent les leads\n", GEN.format(date=date),
         "| Source | Leads | Ce que ça dit |", "|---|---|---|"]
    NOTE = {
        "(non renseigné)": "**Les 38 lignes du classeur d'origine.** Leur provenance n'a jamais été écrite — trou de données assumé, pas une invention.",
        "directory": "Annuaires professionnels de Douala (pagespratiquescm, maligah, doualazoom, goafricaonline).",
        "google_maps": "Sweep cartographique — dentaires de Bonamoussadi/Logbessou.",
        "facebook": "Page Facebook identifiée comme seul canal vivant.",
        "content_video": "Premier lead de la campagne, venu du contenu.",
        "walk_in": "Affiche relevée sur place par King.",
        "other": "Divers.",
    }
    for s, n in Counter(r.get("source") or "(non renseigné)" for r in rows).most_common():
        L.append(f"| `{s}` | {n} | {NOTE.get(s,'')} |")
    L += ["", "## Ce que ce tableau dit\n",
          "- **Les 38 lignes d'origine n'ont aucune source écrite.** On ne saura jamais si ces écoles ont été "
          "trouvées par Google, Facebook ou bouche-à-oreille. **À partir du 15/09, chaque ligne porte sa source.**",
          "- **`directory` est la première source.** Les annuaires de Douala sont le meilleur gisement — "
          "mais leçon du 19/09 : **sur 19 labos tirés des annuaires, 13 seulement avaient WhatsApp (68 %). "
          "Un annuaire donne un numéro, il ne dit pas si le numéro reçoit WhatsApp.**"]
    return "\n".join(L)


def view_daily_plan(rows, date):
    out = ROOT / "leads" / "Daily-Plan.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["# Généré le " + date + " par leads/build/views.py — ne pas modifier à la main"])
        w.writerow(["priorite", "action", "lead", "whatsapp", "ville", "etape", "note"])
        prio = 0
        lignes = []      # collectées puis triées : sinon la file est dans l'ordre du CRM, pas l'ordre du jour
        for r in rows:
            action, note = "", ""
            if reply_pending(r):
                prio += 1
                action = "RÉPONDRE (règle des 90 s)"
                note = re.sub(r"\s+", " ", str(r.get("Reply", "")))[:110]
            else:
                due, why = due_for_relance(r)
                if due and str(due).startswith("PLANNED:"):
                    lignes.append([90, "PROGRAMMÉE (ne rien faire avant)", r["School"],
                                   r.get("wa_number", ""), r.get("City", ""), r.get("stage", ""),
                                   (why or "")[:130]])
                    continue
                if due:
                    prio += 1
                    fu = str(r.get("follow_ups_sent") or "0")
                    action = f"Relance {int(fu)+1}/3" if fu.isdigit() else "Relance"
                    note = why or ""
                elif (r.get("stage") or "") == PROSPECT and r.get("wa_verified") == "yes":
                    prio += 1
                    action = "À CONTACTER (numéro vérifié)"
                    note = re.sub(r"\s+", " ", str(r.get("Notes", "")))[:110]
            if not action and (r.get("stage") or "") == "closing":
                # TROU TROUVÉ LE 21/09 : Labiomed et UNI-LABO — les DEUX seules affaires à « closing »,
                # soit 200 000 FCFA chiffrés — avaient DISPARU de la file du jour. Cause : une date de
                # relance planifiée annule « répondre » ET « relancer », donc un rendez-vous déjà fixé
                # devient invisible. Or rien ne dort à cette étape : on confirme, ou on perd.
                prio += 1
                rdv = RELANCE_A_JOUR.get(r.get("slug", ""), ("", ""))[0]
                prix = str(r.get("price_quoted_fcfa") or "").strip()
                if rdv and rdv > date:
                    action, quand = "CONFIRMER LE RENDEZ-VOUS (J-1)", f"RDV fixé au {rdv}"
                elif rdv:
                    action, quand = "RENDEZ-VOUS DU JOUR", f"échéance {rdv}"
                else:
                    action, quand = "AFFAIRE À CLOSING — la faire avancer", "aucune date posée"
                note = str(r.get("bamfam_next_action") or "")[:110]
                lignes.append([prio, action, r["School"], r.get("wa_number", ""), r.get("City", ""),
                            "closing", f"{quand} · {('prix ' + prix + ' FCFA · ') if prix.isdigit() else ''}{note}"])
                continue
            if not action and (r.get("stage") or "") == "parked":
                # Un lead parqué doit APPARAÎTRE dans la file, avec la consigne contraire : « ne pas
                # relancer ». Sans cette ligne, la file du jour est une liste d'occasions ratées et
                # un fil parqué disparaît de la mémoire — c'est comme ça qu'on relance un lead mort.
                trig = ""
                notes = str(r.get("Notes") or "")
                if " ⏸ " in notes:
                    trig = notes.rsplit(" ⏸ ", 1)[1]
                trig = trig or str(r.get("bamfam_next_step") or "")
                lignes.append([100, "NE PAS RELANCER (parqué)", r["School"], r.get("wa_number", ""),
                               r.get("City", ""), "parked",
                               f"depuis {r.get('stage_since') or '—'} · {re.sub(chr(10),' ',trig)[:130]}"])
                continue
            if action:
                lignes.append([prio, action, r["School"], r.get("wa_number", ""),
                               r.get("City", ""), r.get("stage", ""), note])
        for row in sorted(lignes, key=lambda x: (x[0], x[2].lower())):
            w.writerow(row)
    return out


def main() -> int:
    rows = load()
    dist = distinctive(rows)
    idx = journal_index(rows, dist)
    date = datetime.date.today().isoformat()

    for name, content in [
        ("PIPELINE.md", view_pipeline(rows, idx, date)),
        ("KILL-LIST.md", view_kill_list(rows, date)),
        ("STALE.md", view_stale(rows, idx, date)),
        ("SOURCES.md", view_sources(rows, date)),
    ]:
        (ROOT / "leads" / name).write_text(content, encoding="utf-8")
    plan = view_daily_plan(rows, date)

    n_act = max(sum(1 for _ in csv.reader(plan.open(encoding="utf-8-sig"))) - 2, 0)
    print(f"✓ 4 vues + 1 plan générés ({date})")
    print("  PIPELINE.md · KILL-LIST.md · STALE.md · SOURCES.md · Daily-Plan.csv")
    print(f"  file du jour : {n_act} action(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
