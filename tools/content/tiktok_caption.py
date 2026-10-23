#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle une légende TikTok avant publication — la grille du guide « TikTok SEO 2026 ».

Source de la grille : `research/YouTube-Lessons.md`, lot [48] (vidéo `MebRpuAdreI`, Angel
Talamantes, 27/01/2026). Ce qui a été retenu de la vidéo, et ce que ce script en fait :

  • **la recherche d'abord** : la vidéo dit de chercher sa catégorie dans TikTok (chercher un mot,
    filtrer 90 jours, lire le terme proposé en haut des vidéos) et d'en tirer 3 piliers. Ce script ne
    fait pas ça à notre place — il vérifie seulement que **chaque légende porte l'un des piliers** ;
  • **des phrases humaines, pas des murs de hashtags** : la vidéo parle de « natural keyword
    stuffing » — les mots-clés dans une phrase, pas en liste. Une légende qui n'est qu'une suite de
    hashtags est refusée ici ;
  • **1 à 4 hashtags spécifiques**, jamais `#viral`, `#fyp`, `#pourtoi` : ils ne veulent rien dire
    hors de TikTok, alors que la vidéo insiste sur le fait que TikTok est aussi lu par Google, Gemini
    et Perplexity ;
  • **la première ligne porte le sujet** (c'est elle qui est coupée dans le fil et reprise en
    recherche).

Ce que le script ajoute, et qui ne vient **pas** de la vidéo : nos verrous client. Aucun prix, aucun
délai sans sa condition, aucun superlatif non prouvé, aucun nombre de clients. Une légende qui les
casse est refusée, même si elle est mieux optimisée.

Usage :
    python3 tools/content/tiktok_caption.py "ma légende complète"
    python3 tools/content/tiktok_caption.py --file brouillon.txt
    python3 tools/content/tiktok_caption.py --pillars      # rappel des trois piliers

Le code de sortie vaut 1 dès qu'une **erreur** est trouvée (un avertissement ne bloque pas).
"""
from __future__ import annotations

import argparse
import re
import sys

# Trois piliers AMK, tirés de nos deux métiers et de la recherche locale (pas inventés par la vidéo).
PILLARS = {
    "school": ("école", "ecole", "school", "inscription", "enrolment", "academy", "académie"),
    "clinic": ("clinique", "clinic", "laboratoire", "laboratory", "cabinet", "santé"),
    "web": ("site web", "site internet", "website", "devis", "quote", "whatsapp"),
}

# Hashtags interdits : génériques, sans sens hors de TikTok.
BANNED_TAGS = {
    "fyp", "foryou", "foryoupage", "pourtoi", "viral", "virale", "trending", "tendance",
    "viralvideo", "fypシ", "explore", "explorer", "tiktok", "tiktokfrance", "pourtoipage",
}

# Nos verrous, en expressions régulières.
PRICE = re.compile(r"\b\d[\d .]{2,}\s*(?:fcfa|francs?|f\b|xaf)", re.I)
GUARANTEE = re.compile(r"\b(garanti(?:e|s|es)?|guaranteed|100\s*%|n°\s*1|numero 1|le meilleur|"
                       r"the best|incroyable|révolutionnaire)\b", re.I)
CLIENT_COUNT = re.compile(r"\b\d+\s*(?:clients?|écoles?|ecoles?|cliniques?|projets?)\b", re.I)
DEADLINE = re.compile(r"\b(?:en|dans|in)\s*(\d+)\s*(?:h|heures?|hours?|jours?|days?)\b", re.I)
CONDITION = re.compile(r"(après validation|apres validation|une fois (?:le|votre) brief|"
                       r"after (?:the )?brief|once (?:the )?brief)", re.I)
CTA = re.compile(r"(whatsapp|wa\.me|écri[sz]|ecri[sz]|message|appelle|appelez|dm\b|"
                 r"comment|write|call|book|réserve|reserve)", re.I)


def has_pillar(text: str) -> str | None:
    low = text.lower()
    for name, words in PILLARS.items():
        if any(w in low for w in words):
            return name
    return None


def check(caption: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    text = caption.strip()
    if not text:
        return ["légende vide"], []

    lines = [ln for ln in text.splitlines() if ln.strip()]
    first = lines[0].strip() if lines else ""
    body = " ".join(lines[1:]) if len(lines) > 1 else text

    # ① hashtags
    tags = re.findall(r"#([\wÀ-ÿ_]+)", text)
    if not tags:
        errors.append("aucun hashtag : la vidéo en demande 1 à 4, spécifiques (ex. #sitewebecole)")
    elif len(tags) > 4:
        errors.append(f"{len(tags)} hashtags : 1 à 4 suffisent, au-delà c'est du remplissage")
    banned = [t for t in tags if t.lower() in BANNED_TAGS]
    if banned:
        errors.append("hashtags génériques à retirer : " + ", ".join("#" + b for b in banned))
    vague = [t for t in tags if len(t) < 4 and t.lower() not in BANNED_TAGS]
    if vague:
        warns.append("hashtags très courts, sans doute trop larges : " + ", ".join("#" + v for v in vague))

    # ② la légende doit être une phrase, pas une liste de hashtags
    prose = re.sub(r"#[\wÀ-ÿ_]+", "", text)
    if len(prose.split()) < 8:
        errors.append("trop peu de texte hors hashtags : écris une phrase, c'est elle qui est lue "
                      "par la recherche")

    # ③ première ligne
    if len(first) > 120:
        warns.append(f"première ligne longue ({len(first)} caractères) : au-delà de ~90 elle est "
                     "coupée dans le fil")

    # ④ pilier
    pillar = has_pillar(text)
    if pillar is None:
        errors.append("aucun pilier reconnu (école / clinique / site web) : la vidéo appelle à "
                      "écrire pour une catégorie précise")
    elif has_pillar(first) is None:
        warns.append(f"le pilier « {pillar} » n'apparaît pas dans la première ligne")

    # ⑤ nos verrous
    if PRICE.search(text):
        errors.append("un prix apparaît : aucun prix public (verrou King)")
    if GUARANTEE.search(text):
        errors.append("superlatif ou garantie non prouvée")
    if CLIENT_COUNT.search(text) and not re.search(r"(concepts?|sites? concepts?)", text, re.I):
        errors.append("nombre de clients / d'écoles / de projets : aucun chiffre de ce genre "
                      "(seuls les six concepts sont annonçables, et ils sont annoncés comme tels)")
    if DEADLINE.search(text) and not CONDITION.search(text):
        errors.append("délai sans sa condition : « 24 h » ne s'écrit qu'avec « après validation du brief »")

    # ⑥ appel à l'action
    if not CTA.search(text):
        warns.append("pas d'appel à l'action (WhatsApp, écrire, commenter)")

    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("caption", nargs="*", help="la légende, entre guillemets")
    ap.add_argument("--file", help="lire la légende depuis un fichier")
    ap.add_argument("--pillars", action="store_true", help="afficher les trois piliers")
    args = ap.parse_args()

    if args.pillars:
        for name, words in PILLARS.items():
            print(f"{name:8} ex. {' / '.join(words[:4])}")
        print("\nHashtags interdits : " + ", ".join("#" + t for t in sorted(BANNED_TAGS)))
        return 0

    text = ""
    if args.file:
        from pathlib import Path
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.caption:
        text = " ".join(args.caption)
    if not text:
        ap.print_help(sys.stderr)
        return 2

    errors, warns = check(text)
    for w in warns:
        print("  ~ " + w)
    for e in errors:
        print("  ✗ " + e)
    if not errors and not warns:
        print("  ok — légende conforme")
    elif not errors:
        print(f"  ok — {len(warns)} avertissement(s), rien de bloquant")
    else:
        print(f"  REFUSÉ — {len(errors)} erreur(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
