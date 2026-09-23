#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — portique de PAGE (pas de vidéo). Contrôle automatique d'une page avant qu'un client la voie.

Raison d'être, écrite le 23/09/2026 après une trouvaille en pleine nuit :
    La page du Cristallin, **envoyée à un client** et relue par nous deux fois, portait des liens
    WhatsApp du type `wa.me/699905577` — **sans l'indicatif pays**. WhatsApp refuse un numéro qui n'est
    pas au format international : le bouton qui est le cœur de la page ouvre une erreur.
    Nos deux autres pages (Univers, UNI-LABO) utilisent `237…`. **Personne ne l'avait vu**, parce que
    personne n'avait cliqué. C'est la leçon de la vidéo UX : *« si tu ne dessines que le chemin heureux,
    tu n'es pas un designer, tu es un rêveur »*. Un lien qu'on n'a jamais ouvert n'est pas vérifié.

Ce portique applique les règles apprises dans les quatre vidéos UX/UI du 23/09/2026
(voir `AMK-DESIGN-SKILLS.md` §22) :

  · le CHEMIN — tout lien qui fait sortir de la page doit être vérifiable et complet
                (wa.me international, tel: avec indicatif)
  · la RÉPONSE — toute action de l'utilisateur doit produire une réponse visible
                (`:hover`, `:active`, `:focus-visible`, et un retour après clic)
  · le CHEMIN SUIVANT — dire ce qui se passe APRÈS le clic (« la ligne de temps invisible »)
  · la FORME — une seule H1, alt sur les images, pas de gabarit resté en place,
                pas de bloc dupliqué, pas plus de six tailles de texte
  · les ÉTATS — les champs d'un formulaire ont un état de focus (et d'erreur s'il y a validation)

Usage :
    python3 tools/qa/audit_page.py demos/concept-le-cristallin-v1.html
    python3 tools/qa/audit_page.py demos/*.html hosting/previews/*/index.html
    python3 tools/qa/audit_page.py --strict demos/concept-unilabo-v1.html   # rc=1 si erreur bloquante

Sortie : une ligne par page, puis le détail des constats. **rc=1 si une erreur bloquante** (ce qui casse
la page pour un visiteur), rc=0 sinon. Les avertissements ne bloquent pas — mais ils se lisent.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

# ── ce qui casse une page pour un vrai visiteur : BLOQUANT
BLOCKING = "bloquant"
WARN = "à corriger"

WA_RE = re.compile(r'wa\.me/(\d+)')
TEL_RE = re.compile(r'href="tel:([^"]+)"')
IMG_RE = re.compile(r'<img\b[^>]*>', re.I)
H1_RE = re.compile(r'<h1\b', re.I)
FONTSIZE_RE = re.compile(r'font-size\s*:\s*([0-9.]+)(px|rem|em)')
PLACEHOLDERS = ("Premier texte", "Deuxième texte", "Deuxieme texte", "lorem ipsum", "Lorem ipsum",
                "Texte ici", "Votre texte", "TODO", "à remplacer ici", "[insérer", "XXX", "{{")


def text_of(html: str) -> str:
    """Le texte visible, approximé.

    ⚠️ DEUX PIÈGES PAYÉS EN ÉCRIVANT CETTE FONCTION (23/09) :
      ① les images en base64 et les scripts contiennent n'importe quelle suite de caractères — dont
         « XXX ». La première version cherchait les textes de gabarit dans le HTML BRUT et criait
         « gabarit resté en place » sur trois pages saines. **Un contrôle qui crie au loup ne sera
         pas lu la troisième fois** : les textes de gabarit se cherchent donc dans le TEXTE VISIBLE.
      ② nos pages sont bilingues : la même phrase existe en français ET en anglais. Comparé brut,
         le détecteur de doublons signalait chaque phrase comme « imprimée deux fois ». On retire
         donc les blocs de l'autre langue AVANT de comparer."""
    h = re.sub(r'<script\b.*?</script>', ' ', html, flags=re.S | re.I)
    h = re.sub(r'<style\b.*?</style>', ' ', h, flags=re.S | re.I)
    # une seule langue à la fois (nos pages portent .fr-only / .en-only)
    if 'en-only' in h and 'fr-only' in h:
        h = re.sub(r'<span[^>]*class="[^"]*en-only[^"]*"[^>]*>.*?</span>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', h)


def audit(path: str) -> tuple[list[tuple[str, str, str]], int]:
    html = open(path, encoding="utf-8", errors="replace").read()
    txt = text_of(html)
    findings: list[tuple[str, str, str]] = []

    # ① LE CHEMIN — liens sortants
    #    Les pages de DÉMONSTRATION (MboaCare, la bibliothèque publiable) portent un numéro factice
    #    volontairement espacé — « wa.me/6 00 00 00 00 » — pour qu'aucun vrai numéro n'apparaisse et que
    #    chacun voie que ce n'est pas un prestataire réel. Ce n'est pas un bug, c'est une décision : on le
    #    dit, on ne le bloque pas. Le repère est mécanique — un espace à l'intérieur de l'URL : un vrai
    #    numéro n'en contient jamais.
    demo_links = re.findall(r'wa\.me/[^"\s]*\s', html)
    bad_wa = sorted({n for n in WA_RE.findall(html) if len(n) < 11})
    if bad_wa and demo_links:
        findings.append(("info", f"page de démonstration : numéro WhatsApp factice assumé ({len(demo_links)} liens)",
                         "aucune action — la page est une fiction déclarée, sans numéro réel."))
        bad_wa = []
    if bad_wa:
        findings.append((BLOCKING, f"WhatsApp sans indicatif pays : {', '.join('wa.me/' + n for n in bad_wa)}",
                         "WhatsApp refuse un numéro non international. Écrire 237 + les 9 chiffres "
                         "(ex. wa.me/237699905577)."))
    if not WA_RE.findall(html) and "wa.me" not in html:
        findings.append((WARN, "aucun lien WhatsApp trouvé",
                         "si la page a un CTA WhatsApp, il doit exister aussi sans JavaScript."))
    for num in sorted(set(TEL_RE.findall(html))):
        if not num.startswith("+"):
            findings.append((WARN, f"lien téléphone sans indicatif : tel:{num}",
                             "un visiteur hors Cameroun ne peut pas appeler. Écrire tel:+237…"))
    # ni javascript: ni href="#" pour un bouton qui doit agir
    n_dead = html.count('href="#"')
    if n_dead > 2:
        findings.append((WARN, str(n_dead) + " liens `href=\"#\"`",
                         "un lien qui ne mène nulle part est un signifiant faux — le cerveau du visiteur "
                         "classe la page comme « cassée »."))

    # ② LA RÉPONSE — états et retour après action
    has_hover = ":hover" in html
    has_press = ":active" in html or ":focus-visible" in html
    has_focus = ":focus" in html
    if not (has_hover and has_press):
        findings.append((WARN, "états de bouton incomplets",
                         "prévoir au minimum survol + appui (ou focus clavier) : sans retour visuel, "
                         "l'utilisateur appuie deux fois."))
    if not has_focus:
        findings.append((WARN, "aucun état de focus", "les champs et les liens doivent montrer où est le clavier."))
    if "aria-live" not in html and "role=\"status\"" not in html:
        findings.append((WARN, "aucune zone de retour annoncée (aria-live / role=status)",
                         "après un clic qui ouvre WhatsApp ou envoie un formulaire, la page ne dit rien : "
                         "c'est le trou de « la ligne de temps invisible »."))

    # ③ LE CHEMIN SUIVANT — dire ce qui se passe après
    next_words = ("s'ouvre", "souvre", "se passe", "vous répond", "on vous", "nous répondons", "réponse",
                  "confirm", "48 h", "24 h", "dans l'heure", "récapitul", "prochaines étapes")
    if not any(w in txt.lower() for w in (x.lower() for x in next_words)):
        findings.append((WARN, "la page ne dit pas ce qui se passe après le clic",
                         "ajouter une phrase du type « votre message s'ouvre déjà écrit ; le cabinet "
                         "répond pendant les heures d'ouverture »."))

    # ④ LA FORME
    n_h1 = len(H1_RE.findall(html))
    if n_h1 == 0:
        findings.append((BLOCKING, "aucune balise h1", "un titre principal manquant coûte aussi le SEO local."))
    elif n_h1 > 1:
        findings.append((WARN, f"{n_h1} balises h1", "une seule H1 par page (règle SEO déjà écrite)."))
    if "<title>" not in html:
        findings.append((BLOCKING, "pas de <title>", "le titre est ce que Google et l'onglet affichent."))
    no_alt = [t for t in IMG_RE.findall(html) if "alt=" not in t.lower()]
    if no_alt:
        findings.append((WARN, f"{len(no_alt)} image(s) sans alt", "l'alt est lu par Google et par les lecteurs d'écran."))
    for ph in PLACEHOLDERS:
        if ph not in txt:
            continue
        # Deuxième faux positif payé le 23/09 : « OC-XXXX » n'est pas un gabarit resté en place, c'est
        # un CODE DE RÉFÉRENCE de démonstration (la plaque d'immatriculation de la demande, montrée en
        # exemple). On ne bloque donc que si le marqueur n'est pas précédé d'un préfixe de code.
        if ph == "XXX" and re.search(r"[A-Z]{2,4}-XXXX", txt):
            continue
        findings.append((BLOCKING, f"texte de gabarit resté en place : « {ph} »",
                         "c'est la première chose qu'un client voit — LyfyOptic l'a payé."))
        break
    sizes = {v for v, _u in FONTSIZE_RE.findall(html)}
    if len(sizes) > 8:
        findings.append((WARN, f"{len(sizes)} tailles de texte distinctes",
                         "au-delà de 6 sur un site vitrine, la hiérarchie se dissout (repère : 6 max)."))

    # ⑤ LES BLOCS DUPLIQUÉS — la faute relevée sur la page du Cristallin
    cands = [s.strip() for s in re.split(r'(?<=[.!?])\s+', txt) if len(s.strip()) > 70]
    dups = [s for s, n in Counter(cands).items() if n > 1]
    if dups:
        extrait = dups[0][:70].replace("\n", " ")
        findings.append((WARN, f"{len(dups)} phrase(s) imprimée(s) deux fois — ex. « {extrait}… »",
                         "un bloc dupliqué fait douter de tout le reste (déjà relevé sur le Cristallin : "
                         "le mur « 32 ans d'expérience » en double)."))

    # ⑥ FORMULAIRE — états d'erreur s'il y a des champs
    n_inputs = len(re.findall(r'<input\b|<textarea\b|<select\b', html, re.I))
    if n_inputs and not re.search(r'\.(error|invalid|erreur)|aria-invalid', html, re.I):
        findings.append((WARN, f"{n_inputs} champ(s) sans état d'erreur repérable",
                         "un champ qui refuse sans dire pourquoi fait abandonner le formulaire."))

    return findings, (1 if any(f[0] == BLOCKING for f in findings) else 0)


# ni commentaire de docstring ni rien : la fonction ci-dessus renvoie (constats, code) ; le code ne
# regarde QUE les constats bloquants. Une information (démo assumée) ne bloque pas un envoi.


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="+")
    ap.add_argument("--strict", action="store_true", help="les avertissements deviennent bloquants")
    args = ap.parse_args()

    worst = 0
    for path in args.pages:
        try:
            findings, rc = audit(path)
        except FileNotFoundError:
            print(f"✗ {path} — fichier introuvable")
            worst = 1
            continue
        n_block = sum(1 for f in findings if f[0] == BLOCKING)
        print(f"\n=== {path} — {len(findings)} constat(s), dont {n_block} bloquant(s)")
        for level, what, why in findings:
            print(f"  [{level}] {what}")
            print(f"      → {why}")
        if not findings:
            print("  OK — rien à signaler")
        rc = 1 if (n_block or (args.strict and findings)) else 0
        worst = max(worst, rc)

    print("\n" + ("VERDICT : au moins une page à corriger avant de la montrer à un client."
                  if worst else "VERDICT : OK — les pages passées sont propres."))
    return worst


if __name__ == "__main__":
    sys.exit(main())
