#!/usr/bin/env python3
"""audit_outreach — la porte des messages d'approche froide, avant l'envoi.

Pourquoi ce fichier existe
--------------------------
Le 24/10, six messages ont été réécrits puis déclarés « prêts » **sans passer par une seule
vérification mécanique**. Les règles existaient pourtant, éparpillées dans quatre documents :

  sales/CLIENT-MESSAGING-RULES.md §13      la structure en quatre temps, 35–55 mots, une question
  sales/DECLINAISON-9-DECLENCHEURS… §1②    l'attaque déguisée (« rien à vous », « vous perdez »)
  sales/Monday-Outreach-Pack.md §COPY CRAFT le test des trois questions, zéro mot de remplissage
  knowledge/OUTREACH-MESSAGING-2026-10-22   le dédouanement et la preuve sociale minimale

Une règle sans porte est un trou (§109 de la mémoire de session). Ce script est la porte : il lit un
fichier markdown où chaque message est un bloc

    **⑥ Bouda Seidou — Bonanjo — 677 76 03 49**
    > Bonjour Docteur, ce matin…

et rend un verdict par message, avec la règle citée pour chaque manquement.

Ce qu'il ne juge PAS (et qui reste humain)
------------------------------------------
- **la vérité du fait** — il ne sait pas si les quatre annuaires existent ; c'est le §8c
  (`RESEARCH-STANDARD`) et la capture datée qui le prouvent ;
- **les trois portes §8b** (numéro joint sur WhatsApp, intention numérique, type d'acheteur) — elles se
  vérifient à la main, avant l'écriture ;
- **le goût** — un message qui passe les portes peut rester plat.

Usage
-----
    python3 tools/qa/audit_outreach.py sales/ENVOI-LOT-2026-10-26.md
    python3 tools/qa/audit_outreach.py <fichier> --strict   # les avertissements bloquent aussi

Code de sortie : 0 = aucun manquement bloquant, 1 = au moins un.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮"

HEADER = re.compile(
    rf"^\*\*\s*([{CIRCLED}]?\s*[^*]+?)\s+—\s+(.+?)\s+—\s+([\d\s+]+)\s*\*\*"
)

# Attaques déguisées — DECLINAISON §1②. Le message reproche au gérant ce qu'il n'a pas fait.
ATTACKS = [
    "rien à vous",
    "vous perdez",
    "perdez des clients",
    "vous n'avez pas",
    "vous n'avez aucun",
    "vous n'êtes pas sur",
    "vous êtes absent",
    "absent du web",
    "invisible",
    "ne sert à rien",
    "il vous manque",
    "vous manquez",
    "votre site est mauvais",
    "dommage",
]

# Remplissage et mots creux — COPY CRAFT GATE §5.
PADDING = [
    "j'espère que vous allez bien",
    "je me permets de vous contacter",
    "je me permets",
    "solution digitale",
    "solutions digitales",
    "révolutionnaire",
    "passionné",
    "dynamique",
    "leader",
    "excellence",
]

# Dédouanement — CLIENT-MESSAGING-RULES §13 temps 2. Sans lui, le message se lit comme un reproche.
DEDOUANEMENT = [
    "ce n'est pas votre",
    "pas de votre fait",
    "n'est pas en cause",
    "pas vous qui",
    "pas votre travail",
    "pas votre faute",
]

# Sortie sans friction — knowledge/OUTREACH-MESSAGING §3, temps 5.
SORTIE = ["sans moi", "2 minutes", "deux minutes", "sans engagement", "le faire vous-même"]

URL_RE = re.compile(r"https?://|www\.", re.I)
DOMAIN_RE = re.compile(r"\b[\w-]+\.(?:com|cm|site|net|org|shop|business\.site)\b", re.I)
PRICE_RE = re.compile(r"\d[\d\s.,]*\s*(?:fcfa|francs?|f\s*cfa)\b|\b\d[\d\s]*\s*f\b", re.I)
SIGNATURE_RE = re.compile(r"(?:—|-)\s*(?:King|AMK)\b|\bAMK\b", re.I)
PERCENT_RE = re.compile(r"\b\d+\s*%")
BULLET_RE = re.compile(r"^\s*(?:[•·*-]\s+|\d+[.)]\s+)", re.M)
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def words(text: str) -> list[str]:
    """Mots réels : un guillemet seul ou un tiret seul n'est pas un mot."""
    return [w for w in re.split(r"[\s\u00a0]+", text.strip()) if re.search(r"[0-9A-Za-zÀ-ÿ]", w)]


def sentences(text: str) -> int:
    parts = [p for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p.strip()]
    return len(parts)


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


@dataclass
class Message:
    label: str
    quartier: str
    phone: str
    body: str
    line: int
    fails: list[str] = field(default_factory=list)
    warns: list[str] = field(default_factory=list)

    @property
    def n_words(self) -> int:
        return len(words(self.body))

    @property
    def n_questions(self) -> int:
        return self.body.count("?")


def parse(path: Path) -> list[Message]:
    out: list[Message] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = HEADER.match(lines[i].strip())
        if not m:
            i += 1
            continue
        label = m.group(1).strip()
        quartier = m.group(2).strip()
        phone = m.group(3).strip()
        start = i + 1
        body_lines: list[str] = []
        j = i + 1
        while j < len(lines):
            s = lines[j].strip()
            if not s:
                # un blanc ne coupe pas si la ligne suivante est encore une citation
                if j + 1 < len(lines) and lines[j + 1].strip().startswith(">"):
                    j += 1
                    continue
                break
            if s.startswith(">"):
                body_lines.append(s.lstrip("> ").rstrip())
                j += 1
                continue
            if body_lines:  # texte nu après une citation = fin du bloc
                break
            j += 1
        if body_lines:
            out.append(Message(label, quartier, phone, "\n".join(body_lines), start))
        i = j if j > i else i + 1
    return out


def check(msg: Message) -> None:
    body = msg.body
    flat = fold(body)

    # 1 · longueur — CLIENT-MESSAGING-RULES §13 : 35 à 55 mots, trois phrases
    if msg.n_words > 55:
        msg.fails.append(f"{msg.n_words} mots (maximum 55) — §13")
    elif msg.n_words < 30:
        msg.warns.append(f"{msg.n_words} mots (plancher 35) — §13")
    n_sent = sentences(body)
    if n_sent > 4:
        msg.warns.append(f"{n_sent} phrases (la règle dit trois) — §13")

    # 2 · une seule question — §13 interdit
    if msg.n_questions > 1:
        msg.fails.append(f"{msg.n_questions} questions (une seule) — §13")
    if msg.n_questions == 0:
        msg.warns.append("aucune question : rien à quoi répondre — §13 temps 4")

    # 3 · attaque déguisée — DECLINAISON §1②
    for a in ATTACKS:
        if fold(a) in flat:
            msg.fails.append(f"attaque déguisée : « {a} » — DECLINAISON §1②")

    # 4 · remplissage et mots creux — COPY CRAFT §5
    for p in PADDING:
        if fold(p) in flat:
            msg.fails.append(f"mot de remplissage : « {p} » — COPY CRAFT §5")

    # 5 · lien / prix / signature / pourcentage / puces / emoji
    if URL_RE.search(body):
        msg.fails.append("lien cliquable dans un premier message — §13")
    if DOMAIN_RE.search(body):
        msg.warns.append("domaine cité : preuve ou lien déguisé ? à relire — COPY CRAFT §4")
    if PRICE_RE.search(body):
        msg.fails.append("prix dans un premier message — §13")
    if SIGNATURE_RE.search(body):
        msg.fails.append("signature : signe d'envoi en série — §13")
    if PERCENT_RE.search(body):
        msg.fails.append("pourcentage : aucun chiffre de résultat — OUTREACH-MESSAGING §3")
    if BULLET_RE.search(body):
        msg.fails.append("liste à puces : ça se lit comme un rapport — §13")
    if EMOJI_RE.search(body):
        msg.fails.append("emoji — §13")

    # 6 · dédouanement — §13 temps 2
    if not any(fold(d) in flat for d in DEDOUANEMENT):
        msg.warns.append("pas de dédouanement : le fait se lira comme un reproche — §13 temps 2")

    # 7 · sortie sans friction — knowledge §3 temps 5 (avertissement : deux structures coexistent)
    if not any(fold(x) in flat for x in SORTIE):
        msg.warns.append("pas de sortie sans friction — OUTREACH-MESSAGING §3 temps 5")

    # 7 bis · une question à deux branches — le §13 interdit « deux questions » ;
    # « A ou B ? » en est une seule à l'écrit, mais deux réponses à choisir à l'oral.
    for sent in re.split(r"(?<=[.!?])\s+", body):
        if sent.rstrip().endswith("?") and " ou " in fold(sent):
            msg.warns.append("question à deux branches (« X ou Y ? ») — justifier ou simplifier, §13")
            break

    # 8 · le quartier doit apparaître tôt — DECLINAISON §1①, six premiers mots
    q = fold(msg.quartier.split("(")[0].strip())
    first = fold(" ".join(words(body)[:12]))
    if q and q not in first:
        msg.warns.append(f"« {msg.quartier} » absent des 12 premiers mots — DECLINAISON §1①")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--strict", action="store_true", help="les avertissements bloquent aussi")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"fichier introuvable : {path}")
    msgs = parse(path)
    if not msgs:
        raise SystemExit(
            "aucun message reconnu — attendu : **⑥ Nom — Quartier — 677 00 00 00** puis des lignes > "
        )

    total_f = total_w = 0
    print(f"\nPORTE DES MESSAGES FROIDS — {path}  ({len(msgs)} message(s))\n")
    for m in msgs:
        check(m)
        total_f += len(m.fails)
        total_w += len(m.warns)
        verdict = "BLOQUÉ" if m.fails else ("À RELIRE" if m.warns else "OK")
        print(f"{'─' * 78}\n{m.label} · {m.quartier} · {m.phone}")
        print(f"  {m.n_words} mots · {sentences(m.body)} phrases · {m.n_questions} question(s) → {verdict}")
        for f in m.fails:
            print(f"  ✗ {f}")
        for w in m.warns:
            print(f"  · {w}")

    blocking = total_f + (total_w if args.strict else 0)
    print(f"{'─' * 78}")
    print(f"TOTAL {total_f} bloquant(s) · {total_w} avertissement(s) — {'BLOQUÉ' if blocking else 'OK'}")
    print("Rappel : ce script ne prouve pas que le fait est vrai, ni que le numéro joint WhatsApp (§8b).\n")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
