#!/usr/bin/env python3
"""audit_post_dm — la porte du KIT CLIENT : accroche alignée, légende par plateforme, chemin d'entrée.

Pourquoi elle existe (27/10/2026, tour 192)
-------------------------------------------
Deux règles venaient d'être écrites et **aucune n'était vérifiée** :

1. `knowledge/HOOK-FIRST-2026-10-27.md` — l'accroche a **trois composantes** (texte à l'écran, visuel,
   parlé) et elles doivent dire **la même chose** ; le texte arrive avant 3 s. Rien ne le contrôlait :
   `audit_hook` vérifie *une phrase*, pas l'alignement de ce qui est montré avec ce qui est dit.
2. `CONTENT-CREATION` §5 — **le message prérempli est la seule attribution fiable**. Sur les deux pièces
   publiées avant cette date, **aucune** n'avait de `wa.me/…?text=…` : zéro conversation attribuable.

Et les deux portes existantes (`audit_publication`, `audit_platform`) sont écrites pour les pièces **AMK**
(mot-clé `APERÇU`, marque `#AMKweb`, Instagram). Un kit **DM Optique** y échouerait sur des paramètres
qui n'ont rien à voir avec la qualité du post. D'où une porte au profil du client, pas un contournement.

Ce qu'elle refuse
-----------------
- `hook-incomplet` · §1 ne déclare pas les **trois** composantes (texte / visuel / parlé)
- `hook-desaligne` · moins de **deux** nombres communs entre le texte à l'écran et la phrase prononcée
- `hook-tardif` · le texte à l'écran arrive après **3,0 s**
- `sections-manquantes` · pas de légende TikTok (§2) **et** Facebook (§3)
- `accroche-longue` · première ligne de légende > **100 caractères** (Facebook coupe avant « Voir plus »)
- `cta-absent` / `deux-cta` · aucune action, ou plus d'une
- `attribution-faible` · les deux plateformes collent le **même** texte prérempli — donc on ne sait plus
  d'où vient la conversation
- `lien-absent` · pas de `wa.me/237…?text=` prérempli
- `prix-dans-la-legende` · un prix, `FCFA`, `k`
- `promesse` / `allegation-sante` · « garanti », « guérir », « corriger définitivement », « soigne »
- `hashtags-hors-borne` (3–8) · `local-absent` (#Douala/#Bonabéri/#Cameroun) · `marque-absente`
  (#dmoptique) · `mendicite` (#fyp, #pourtoi, « abonnez-vous »)
- `sous-titres-auto` · la §2 ne dit pas « sous-titres manuels » (ruling 11/10)
- `epingle-absent` · pas de commentaire épinglé
- `horaires-absents` · aucune heure de consultation dans le kit — le patient doit savoir quand venir
- `nom-tardif` · la première ligne de la réponse d'accueil ne nomme pas le cabinet
- `compteur-absent` · §5 n'a pas ses colonnes de décision
- `alt-absent` · pas de texte alternatif pour la publication Facebook
- `abonnement-mendicite` · « abonnez-vous », « likez » — demander un abonné n'en produit pas
  (doctrine du 27/10, `LEAD-MAGNETS` §2)
- `serie-sans-boucle` · le kit déclare une **série** et ne promet aucune suite — sans boucle ouverte,
  une série ne fait pas revenir, donc ne fait pas s'abonner

Ce qu'elle avertit
------------------
`variantes-absentes` · moins de **trois** accroches écrites pour la même pièce (`CONTENT-CREATION`
§3 ter : « on teste trois hooks », personne ne l'appliquait) · `legende-longue` (> 700 car.) ·
`accroche-tiktok-longue` (> 60 car.) · `duree-inconnue`.

Usage
-----
    python3 tools/qa/audit_post_dm.py clients/dm-optic/content/month1/w3/KIT-27-10-HOOK.md
    python3 tools/qa/audit_post_dm.py <kit>.md <master>.mp4
"""

from __future__ import annotations

import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_publication import _duree_master  # noqa: E402  (une seule mesure de durée)

HASHTAGS_MIN, HASHTAGS_MAX = 3, 8
ACCROCHE_MAX = 100
ACCROCHE_TIKTOK_MAX = 60
LEGENDE_MAX = 700
HOOK_FIN_MAX = 3.0
MARQUE = "#dmoptique"
LOCAL = ("#douala", "#bonaberi", "#bonabéri", "#cameroun", "#cameroon")
INTERDITS = ("#fyp", "#pourtoi", "#viral", "#follow", "abonnez-vous", "abonnez vous", "likez", "partagez svp")
# Mendier un abonnement ne donne pas d'abonnement — et ça signale un compte qui cherche des vues
# (`CONTENT-CREATION` §5 quater, `TIKTOK-SEO-CHECKLIST` §C). Ce qu'on écrit à la place : une raison de
# revenir, c'est-à-dire une boucle ouverte dont on tient la promesse.
MENDICITE_ABO = ("abonnez-vous", "abonnez vous", "abonne-toi", "abonne toi", "abonnes-toi",
                 "follow me", "suivez-moi", "suivez moi", "likez", "mets un like", "mettre un like")
BOUCLE = ("demain", "la prochaine", "prochain episode", "prochaine video", "episode suivant",
          "la suite", "rendez-vous demain", "dans l'episode")
ACTION = ("ecrivez", "envoyez", "passez", "appelez", "cliquez", "contactez", "demandez", "venez")
PROMESSES = ("garanti", "garantie", "garantis", "promis", "plus de patients", "plus de clients",
             "resultat assure", "vous verrez mieux")
SANTE = ("guerir", "guerit", "soigne", "soignent", "corriger definitivement", "corrige definitivement",
         "retrouver une vue parfaite", "vue parfaite", "traitement")
PRIX = re.compile(r"\b(fcfa|prix|tarif)\b|\d{1,3}\s?k\b|\d{1,3}(\s\d{3})+\s?(fcfa|f)\b", re.I)
HEURE = re.compile(r"\b\d{1,2}\s?h\s?\d{0,2}\b", re.I)
LIEN = re.compile(r"wa\.me/237\d{9}\?text=[^\s)\]|]+", re.I)
RANGE = re.compile(r"(\d+)[,.](\d+)\s*[–\-—]\s*(\d+)[,.](\d+)")

MOTS_NOMBRES = {
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8,
    "neuf": 9, "dix": 10, "douze": 12, "quinze": 15, "vingt": 20, "trente": 30, "quarante": 40,
    "cinquante": 50, "soixante": 60, "quatre-vingt": 80, "cent": 100, "mille": 1000,
}

COLONNES = ("vues", "messages recus", "conversations")


@dataclass
class Verdict:
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)
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


def _code(corps: str) -> list[str]:
    return [m.group(2).strip() for m in re.finditer(r"```([a-zA-Z]*)\n(.*?)```", corps, re.S)]


def _tableau(corps: str) -> str:
    return "\n".join(l for l in corps.splitlines() if l.strip().startswith("|"))


def _lignes_citees(corps: str) -> str:
    return "\n".join(l[1:].strip() for l in corps.splitlines() if l.startswith(">")).strip()


def _hashtags(cap: str) -> list[str]:
    return [h.lower() for h in re.findall(r"#[0-9A-Za-zÀ-ÿ_]+", cap)]


def _nombres(texte: str) -> set[int]:
    """Les nombres d'une ligne, en chiffres **et** en mots — c'est ce qui rend l'alignement mesurable."""
    bas = _plat(texte)
    out = {int(n) for n in re.findall(r"\b\d{1,4}\b", bas)}
    for mot, val in MOTS_NOMBRES.items():
        if re.search(rf"\b{re.escape(mot)}\b", bas):
            out.add(val)
    return out


def _ligne_de(table: str, etiquette: str, garder_temps: bool = False) -> str:
    """Le contenu d'une ligne du tableau §1.

    La colonne des secondes n'est **pas du contenu** : « 0,0–3,0 » ne doit pas compter comme un nombre
    commun entre le texte et la voix — c'est ce qui rendait l'alignement faux-positif au premier essai.
    `garder_temps=True` la remet, pour la seule vérification de la fenêtre d'accroche.
    """
    for ligne in table.splitlines():
        cellules = [c.replace("**", "").strip() for c in ligne.strip().strip("|").split("|")]
        if cellules and _plat(cellules[0]).startswith(etiquette):
            if garder_temps:
                return " | ".join(cellules[1:])
            return " | ".join(c for c in cellules[1:] if not RANGE.fullmatch(c.strip()))
    return ""


def _premiere_ligne(texte: str) -> str:
    for ligne in texte.replace("**", "").splitlines():
        if ligne.strip():
            return ligne.strip()
    return ""


def audit(chemin: str | Path, master: str | Path | None = None) -> Verdict:
    chemin = Path(chemin)
    texte = chemin.read_text(encoding="utf-8")
    sections = _sections(texte)
    v = Verdict()

    # ① l'accroche — trois composantes, alignées, à l'heure
    un = _section(sections, "1")
    table = _tableau(un)
    if not table:
        v.fails.append("[hook-incomplet] §1 n'a pas de tableau : les trois composantes ne sont pas déclarées")
    else:
        t_txt = _ligne_de(table, "texte")
        t_vis = _ligne_de(table, "visuel")
        t_par = _ligne_de(table, "parle")
        manquantes = [n for n, t in (("texte", t_txt), ("visuel", t_vis), ("parlé", t_par)) if not t]
        if manquantes:
            v.fails.append(f"[hook-incomplet] composante(s) absente(s) : {', '.join(manquantes)}")
        muet = "muet" in _plat(t_par) or "aucune voix" in _plat(t_par) or "sans voix" in _plat(t_par)
        if muet:
            # Une pièce muette est un choix, pas un oubli : le texte et le visuel portent tout.
            # On ne peut pas mesurer l'alignement sur une voix qui n'existe pas — on le dit.
            v.warns.append("[piece-muette] la pièce est déclarée muette : vérifier à l'œil, son coupé, "
                           "que le texte suffit seul à comprendre la scène")
        else:
            communs = _nombres(t_txt) & _nombres(t_par)
            if len(communs) < 2:
                v.fails.append(
                    "[hook-desaligne] le texte à l'écran et la phrase prononcée n'ont que "
                    f"{len(communs)} nombre(s) en commun ({sorted(communs) or 'aucun'}) — "
                    "le spectateur reçoit deux messages et part (HOOK-FIRST §1)"
                )
        # la fenêtre du texte à l'écran, indépendante de la voix (vaut aussi pour une pièce muette)
        m = RANGE.search(_ligne_de(table, "texte", garder_temps=True))
        if m:
            fin = float(f"{m.group(3)}.{m.group(4)}")
            if fin > HOOK_FIN_MAX:
                v.fails.append(f"[hook-tardif] le texte à l'écran tient jusqu'à {fin} s "
                               f"(max {HOOK_FIN_MAX} s)")
        else:
            v.fails.append("[hook-tardif] aucune fenêtre de temps déclarée pour le texte à l'écran")
        if len(re.findall(r"^\|\s*(?:variante|écart|rejet)", table, re.I | re.M)) < 3:
            if _plat(un).count("ecartee") + _plat(un).count("ecartees") < 3:
                v.warns.append("[variantes-absentes] moins de trois accroches écrites pour la même pièce "
                               "(CONTENT-CREATION §3 ter)")

    # ② les légendes, une par plateforme
    cap_tt = (_code(_section(sections, "2")) or [""])[0]
    cap_fb = (_code(_section(sections, "3")) or [""])[0]
    if not cap_tt or not cap_fb:
        v.fails.append("[sections-manquantes] il faut une légende TikTok (§2) ET Facebook (§3)")
        return v

    for nom, cap, plafond in (("tiktok", cap_tt, ACCROCHE_TIKTOK_MAX), ("facebook", cap_fb, ACCROCHE_MAX)):
        premiere = next((l for l in cap.splitlines() if l.strip()), "")
        if len(premiere) > ACCROCHE_MAX:
            v.fails.append(f"[accroche-longue] {nom} : première ligne de {len(premiere)} car. "
                           f"(max {ACCROCHE_MAX}) — elle est coupée avant « Voir plus »")
        elif nom == "tiktok" and len(premiere) > plafond:
            v.warns.append(f"[accroche-tiktok-longue] tiktok : {len(premiere)} car. (max conseillé {plafond})")
        if len(cap) > LEGENDE_MAX:
            v.warns.append(f"[legende-longue] {nom} : {len(cap)} car. (max conseillé {LEGENDE_MAX})")
        plat = _plat(cap)
        actions = sorted({a for a in ACTION if a in plat})
        if not actions:
            v.fails.append(f"[cta-absent] {nom} : aucun verbe d'action")
        elif len(actions) > 1:
            v.fails.append(f"[deux-cta] {nom} : {len(actions)} actions ({', '.join(actions)}) — une seule")
        if PRIX.search(cap):
            v.fails.append(f"[prix-dans-la-legende] {nom} : « {PRIX.search(cap).group(0)} »")
        for p in PROMESSES:
            if p in plat:
                v.fails.append(f"[promesse] {nom} : « {p} »")
                break
        for mot in SANTE:
            if mot not in plat:
                continue
            # « ce n'est pas un traitement, c'est une pause » est la limite assumée du cabinet :
            # la négation est permise, l'affirmation jamais.
            niee = re.search(rf"(pas|jamais|aucun[e]?)\s+(un\s+|de\s+|d'\s?)?{re.escape(mot)}", plat)
            if niee:
                continue
            v.fails.append(f"[allegation-sante] {nom} : « {mot} » — verrou client, jamais dans un post")
            break
        tags = _hashtags(cap)
        if not HASHTAGS_MIN <= len(tags) <= HASHTAGS_MAX:
            v.fails.append(f"[hashtags-hors-borne] {nom} : {len(tags)} hashtag(s), attendu "
                           f"{HASHTAGS_MIN}–{HASHTAGS_MAX}")
        if not any(t in LOCAL for t in tags):
            v.fails.append(f"[local-absent] {nom} : ni #Douala ni #Bonabéri ni #Cameroun")
        if MARQUE not in tags:
            v.fails.append(f"[marque-absente] {nom} : {MARQUE} manque")
        for mot in INTERDITS:
            if mot in plat:
                v.fails.append(f"[mendicite] {nom} : « {mot} » — ça ne classe rien")
                break
        if not LIEN.search(cap):
            v.fails.append(f"[lien-absent] {nom} : pas de wa.me/237…?text= prérempli — "
                           "sans texte, la conversation ne dit pas d'où elle vient")

    liens = [m.group(0).lower() for m in LIEN.finditer(cap_tt)] + [m.group(0).lower() for m in LIEN.finditer(cap_fb)]
    if len(liens) >= 2 and liens[0] == liens[1]:
        v.fails.append("[attribution-faible] les deux plateformes collent le MÊME texte prérempli — "
                       "on ne saura pas d'où vient la conversation")

    plat_tt = _plat(_section(sections, "2"))
    if "sous-titre" not in plat_tt or "manuel" not in plat_tt:
        v.fails.append("[sous-titres-auto] §2 ne dit pas « sous-titres manuels » (ruling 11/10)")
    if not re.search(r"commentaire (epingle|épinglé)", plat_tt):
        v.fails.append("[epingle-absent] §2 : pas de commentaire épinglé")
    if "alt" not in _plat(_section(sections, "3")):
        v.fails.append("[alt-absent] §3 : pas de texte alternatif pour la publication Facebook")

    # ② bis · la mécanique d'abonné (doctrine du 27/10, `LEAD-MAGNETS` §2 et §6)
    for nom, cap in (("tiktok", cap_tt), ("facebook", cap_fb)):
        plat_cap = _plat(cap)
        for mot in MENDICITE_ABO:
            if mot in plat_cap:
                v.fails.append(
                    f"[abonnement-mendicite] {nom} : « {mot} » — demander un abonnement ne produit pas "
                    "d'abonné ; c'est une raison de revenir qui en produit un"
                )
                break
    declare_serie = "serie" in _plat(texte) or "episode" in _plat(texte)
    if declare_serie:
        ouvert = any(m in _plat(cap_tt) or m in _plat(cap_fb) or m in _plat(un) for m in BOUCLE)
        if not ouvert:
            v.fails.append(
                "[serie-sans-boucle] le kit déclare une série mais ne promet aucune suite — "
                "sans boucle ouverte, une série ne fait pas revenir, donc ne fait pas s'abonner"
            )

    # ③ le chemin d'entrée et les horaires
    if not HEURE.search(texte):
        v.fails.append("[horaires-absents] aucune heure de consultation dans le kit")

    # ④ la réponse d'accueil
    acc = _lignes_citees(_section(sections, "4"))
    if not acc:
        v.fails.append("[nom-tardif] aucune réponse d'accueil citée dans §4")
    elif "dm optique" not in _plat(_premiere_ligne(acc)):
        v.fails.append("[nom-tardif] la première ligne de la réponse ne nomme pas le cabinet")

    # ⑤ le compteur
    table5 = _plat(_tableau(_section(sections, "5")))
    manquantes = [c for c in COLONNES if c not in table5]
    if manquantes:
        v.fails.append(f"[compteur-absent] colonnes manquantes dans §5 : {', '.join(manquantes)}")

    # ⑥ le master, quand il est fourni
    if master is not None:
        m = Path(master)
        if not m.exists():
            v.warns.append(f"[master-absent] {m} n'existe pas — durée non mesurée")
        else:
            v.duree = _duree_master(m)
            if v.duree is None:
                v.warns.append("[duree-inconnue] aucun ffmpeg — la durée n'a pas été mesurée")

    return v


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    kit = argv[0]
    master = argv[1] if len(argv) > 1 else None
    v = audit(kit, master)
    entete = "kit DM"
    if v.duree is not None:
        entete += f" · master {v.duree} s"
    print(f"{'✓' if v.ok else '✗'} {entete}")
    for w in v.warns:
        print(f"   ⚠ {w}")
    for f in v.fails:
        print(f"   ⛔ {f}")
    return 0 if v.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
