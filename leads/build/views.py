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

STAGE_LABEL = {
    "won": "✅ Client — contrat signé",
    "prospecting": "① Prospection — à qualifier",
    "qualifying": "② Qualifié — en conversation",
    "demo": "③ Aperçu envoyé",
    "closing": "④ Prix posé, en négociation",
    "offer": "④ Offre posée",
    "delivered": "⑤ Livré",
    "lost": "❌ Perdu",
    "parked": "⏸ Parqué",
    "disqualified": "⛔ Écarté",
}
STAGE_ORDER = ["won", "delivered", "closing", "offer", "demo", "qualifying",
               "prospecting", "lost", "parked", "disqualified"]
# ⚠️ CE QUE ÇA A CORRIGÉ (21/09, 23:10) : `closing` n'était NI dans STAGE_ORDER NI dans STAGE_LABEL.
# Le CRM était juste — le tableau de bord, non. Nos DEUX prospects les plus avancés (Le Cristallin,
# Univers Optique : prix posé, aperçu construit) ne figuraient AUCUNE PART dans PIPELINE.md, parce que
# la boucle d'affichage saute silencieusement toute valeur inconnue. Un compteur qui omet le lead le
# plus chaud est pire qu'un compteur absent. D'où l'assertion plus bas : AUCUN stage du CSV ne peut
# rester hors de la vue.

# Décisions humaines qui priment sur les règles automatiques : slug -> (échéance ISO, note)
RELANCE_A_JOUR = {
    "opticien-bali-douala": ("2026-09-25", "2ᵉ message envoyé le 22/09 au soir (créneau fixé par le prospect "
                                        "lui-même). DERNIÈRE touche : vendredi 25/09, puis parked daté"),
    "oracare-buea": ("2026-09-28", "PARKED depuis le message de CLÔTURE du 21/09 17:43 (« last note from me, "
                                    "then I stop ») — ne rien écrire avant lundi 28/09, et ce jour-là un seul "
                                    "message : léger, SANS reproche, justifié par du neuf (les prix et la prise "
                                    "de RDV 24/7 sont sur la page). Nom vérifié : Dr Arnold Nkafu — jamais "
                                    "« Dr Njie », ce prénom n'existe dans aucun fichier"),
    "midas-touch-optic-center-mitoc": ("2026-09-29", "FU2 envoyée le 22/09 au soir (un jour de retard rattrapé). "
                                          "DERNIÈRE touche : 29/09, puis on classe — trois messages maximum"),
    "baird-memorial-college": ("2026-09-21", "FU2 fixée lun 21 (même lot que MITOC)"),
    "labiomed-deido": ("2026-10-01", "A RÉPONDU le 22/09 à 16:41 : « Non pas encore je ne suis pas en place » "
                                      "· « Quand je serai la je vais vous contacter ». Ce n'est ni un oui ni un "
                                      "refus — c'est un REPORT MOTIVÉ (pas encore installé). Réponse envoyée "
                                      "dans l'heure ; on ne le relance plus d'ici le 1ᵉʳ octobre, et ce jour-là "
                                      "sans prix ni question de validation : juste « vous êtes en place ? »"),
    "centre-medical-de-bonanjo": ("2026-09-28", "Page complète envoyée le 22/09 à 13:35 (deux coches) "
                                      "avec le prix posé, puis relance 16:24 (une coche) : « vos 9 services "
                                      "centralisés pour orienter les patients de Google vers votre "
                                      "WhatsApp ». DÉCISION KING 16:30 : prochaine vague — jeudi 24/09, "
                                      "sans reposer le prix, une question de calendrier seulement"),
    # Les deux fils « prix posé » du 21/09 : l'échéance vient de ce qui a été ÉCRIT au client,
    # pas d'un calcul M+2. Univers Optique = l'aperçu promis « d'ici demain ». Le Cristallin =
    # la réponse de King sur le périmètre FB attendue avant d'envoyer, relance 48 h après.
    # 22/09 20:51 : il a répondu — « Je suis vraiment intéressé … Vendredi matin 10h dans mon cabinet. »
    # Comme UNI-LABO, ce n'est plus une relance à calculer, c'est une réunion à préparer.
    "univers-optique": ("2026-09-25", "RENDEZ-VOUS fixé par le prospect — **vendredi 25/09 à 10 h, son "
                                      "cabinet** (Bépanda). Feuille : `sales/RDV-UNIVERS-OPTIQUE-2026-09-25.md`. "
                                      "Prix déjà posé le 21/09 (100 000 FCFA, 50/50) : on ne le re-présente "
                                      "pas, on ne le baisse pas. À sortir de la salle : le « oui », les "
                                      "réponses aux six points que la page demande, l'acompte"),
    # 23/09 09:46 : le prix est PARTI (150 000 FCFA, 75 000 pour démarrer). On attend sa réponse ;
    # s'il ne dit rien, une relance courte le 24/09 — et rien d'autre entre-temps.
    "le-cristallin": ("2026-09-24", "**PRIX POSÉ le 23/09 09:46** : 150 000 FCFA (site bilingue, "
                                     "hébergement 1 an, nom de domaine, assistant WhatsApp), 50 % = 75 000 "
                                     "pour démarrer, solde à la livraison. On attend un oui. S'il ne répond "
                                     "pas : UNE relance courte le 24/09, sans rebaisser le prix et sans "
                                     "reprocher le silence. Cinq écarts à trancher AVANT publication "
                                     "(compte d'assurances FR 18 / EN 17, mur à 19, bloc « 32 ans » en "
                                     "double, horaires vs son flyer, « depuis 2010 ») et le périmètre "
                                     "« hébergement + domaine » à cadrer : son domaine est à lui jusqu'au "
                                     "13/06/2027"),
    # UNI-LABO a DEMANDÉ un rendez-vous : ce n'est plus une relance à calculer.
    "uni-labo-bonamoussadi": ("2026-09-25", "RENDEZ-VOUS demandé par le prospect — vendredi 25/09"),
    # Le calcul M+4 ne voyait pas cette échéance : le compteur de la source disait 1 relance au lieu de 2
    # (FU1 19/09 + FU2 21/09 17:39). Le journal, lui, disait « FU3 mer 23/09 max, palier des 3 messages
    # atteint » depuis le 21/09. Décision humaine inscrite ici le 23/09 — c'est la DERNIÈRE touche.
    "afrique-labo-douala": ("2026-09-23", "**FU3 = DERNIÈRE TOUCHE** (le compteur était faux : FU1 19/09 + FU2 "
                                         "21/09 17:39 = 2, la source disait 1 → l'échéance écrite au journal "
                                         "depuis le 21/09 n'était calculée nulle part). Message prêt : "
                                         "`sales/Send-Soir-2026-09-23.md` §③. Après cet envoi : plus aucune "
                                         "relance, on attend. Vitrine À LUI (`afriqlabo.com`) : l'angle part de "
                                         "ce qu'il a, jamais de ce qui lui manque"),
    "tchaya-optique": ("2026-09-23", "Message 1 parti le 21/09 à 17:47 (une coche, jamais enregistré avant le "
                                     "22/09). Vitrine : deux pages Facebook, dont « TCHAYA OPTIQUE INTERNATIONAL » "
                                     "(2 390 mentions J'aime, opticien depuis 1974). Relance 1/3 : 23/09"),
    "disc-optique-m-dicale": ("2026-09-23", "Message 1 parti le 21/09 à 17:48 (une coche, jamais enregistré avant "
                                           "le 22/09). Vitrine : page Facebook « DISC Optique Médical - DOM » "
                                           "(Bali, rue des manguiers). Relance 1/3 : 23/09"),
    "skye-douala": ("2026-09-29", "Relance 2/3 envoyée le 22/09 au soir (réécrite sans reproche). DERNIÈRE "
                                  "touche : 29/09, puis parked daté"),
    "yaks-douala": ("2026-09-29", "Relance 2/3 envoyée le 22/09 au soir. DERNIÈRE touche : 29/09, puis parked"),
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
    if slug in RELANCE_A_JOUR:
        d, note = RELANCE_A_JOUR[slug]
        return (d, f"fixé : {note}") if d <= today.isoformat() else (None, None)
    if (r.get("stage") or "") != "qualifying":
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
    orphan = sorted(k for k in c if k and k not in STAGE_ORDER)
    if orphan:
        sys.exit(f"✗ stage(s) orphelins {orphan} : présents dans le CSV, absents de STAGE_ORDER — "
                 f"ces leads seraient invisibles dans PIPELINE.md. Ajouter l'étape, pas le lead.")
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
           and (r.get("stage") or "") not in ("parked", "disqualified")
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
        if (r.get("stage") or "") in ("parked", "disqualified"):
            continue
        age = last_send_age_days(r)
        if age < 2:
            continue
        if r.get("slug") in RELANCE_A_JOUR:
            continue          # une date a été fixée : ce n'est pas un lead endormi
        if (r.get("org_type") or "") == "school" and r.get("slug") not in SCHOOLS_KEPT:
            continue          # décision de King 22/09 16:45 : le segment école est écarté
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


# ── DÉCISION DE KING — 22/09/2026, 16:45 : « laisser tomber les écoles » ────────────
# Les 39 écoles sortent des vagues d'envoi et du plan du jour (raison chiffrée dans
# sales/PROFIL-DES-OUI-2026-09-22.md : 2,6 % de réponse contre 11,1 % pour les prospects
# qui paient déjà pour être visibles). Elles restent dans le CRM et dans leurs fiches.
# Deux exceptions NOMMÉES, et elles ne sortent pas d'ici sans une décision :
SCHOOLS_KEPT = {
    "inses-douala":
        "École de nom, mais la même affiche porte « LA CLINIQUE DE L'ESPOIR » : le message va au "
        "cabinet (santé), pas à l'institut — et c'est un numéro vérifié.",
    "st-theresa-international-bilingual-comprehensive-college-sti":
        "Une parole a déjà été donnée : retour promis en OCTOBRE (15/09, « permission de revenir »). "
        "On ne reprend pas un engagement pour appliquer une règle.",
}


def view_daily_plan(rows, date):
    out = ROOT / "leads" / "Daily-Plan.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["# Généré le " + date + " par leads/build/views.py — ne pas modifier à la main"])
        w.writerow(["priorite", "action", "lead", "whatsapp", "ville", "etape", "note"])
        prio = 0
        n_school = 0
        n_kept = 0
        for r in rows:
            # ── DÉCISION DE KING 22/09 16:45 : « laisser tomber les écoles ». Elles ne sont ni
            #    relancées, ni contactées, ni listées ici — mais elles restent dans le CRM et
            #    dans les fiches. Le seul engagement déjà pris à une école (STIBCCOL, retour
            #    promis en octobre) reste dans kills/`RELANCE_A_JOUR` : on ne reprend pas une
            #    parole donnée. Zero école ne disparaît en silence : le compte est imprimé.
            if (r.get("org_type") or "") == "school" and r.get("slug") not in SCHOOLS_KEPT:
                n_school += 1
                continue
            if (r.get("org_type") or "") == "school":
                n_kept += 1
            action, note = "", ""
            if reply_pending(r):
                prio += 1
                action = "RÉPONDRE (règle des 90 s)"
                note = re.sub(r"\s+", " ", str(r.get("Reply", "")))[:110]
            else:
                due, why = due_for_relance(r)
                if due:
                    prio += 1
                    fu = str(r.get("follow_ups_sent") or "0")
                    action = f"Relance {int(fu)+1}/3" if fu.isdigit() else "Relance"
                    note = why or ""
                elif (r.get("stage") or "") == "prospecting" and r.get("wa_verified") == "yes":
                    prio += 1
                    action = "À CONTACTER (numéro vérifié)"
                    note = re.sub(r"\s+", " ", str(r.get("Notes", "")))[:110]
            if action:
                w.writerow([prio, action, r["School"], r.get("wa_number", ""),
                            r.get("City", ""), r.get("stage", ""), note])
    if n_school or n_kept:
        print(f"  école(s) : {n_school} écartée(s) du plan (décision de King 22/09 16:45) · "
              f"{n_kept} gardée(s) par exception écrite (SCHOOLS_KEPT)")
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
