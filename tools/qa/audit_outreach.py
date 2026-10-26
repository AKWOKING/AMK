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

Depuis le 26/10, il juge aussi **la ressemblance entre les messages du lot** (§10). À sept messages
écrits à la main, deux phrases communes ne sont rien ; à quarante messages par jour, une séquence de
douze mots qui revient est la signature d'un compte qui diffuse — c'est ce que WhatsApp sanctionne,
et c'est le seul risque que la cadence de King ajoute.

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

# Dédouanement — CLIENT-MESSAGING-RULES §13 temps 2, réécrit le 26/10 (ruling King, 152ᵉ message).
#
# Le ruling précédent disait : « ce n'est pas votre travail, c'est X ». King l'a cassé en deux
# questions, et il avait raison : *c'est la faute de qui ?* — la phrase ne répond pas — et *où est
# le problème ?* — elle ne le dit pas non plus. Pire, « ce n'est pas votre travail » renvoie la
# faute à celui qui a rempli la fiche, c'est-à-dire souvent à un employé du prospect.
#
# Le temps 2 doit donc **nommer ce qui retient le patient** (Google, WhatsApp, les annuaires,
# l'absence de site) — un objet, jamais une personne — **et situer le problème** (ce que le patient
# ne peut pas faire). Une absolution seule ne passe plus.
OBSERVATION = ["votre compte", "votre profil", "votre page", "votre site", "votre cabinet",
               "votre fiche", "votre numéro", "vos horaires", "au tableau", "vous apparaissez",
               "apparaît", "apparait", "s'affiche", "au registre", "chez vous"]

# La cause nommée : un objet qui détient l'information et qui n'est pas le prospect.
CAUSE = [
    "pas à vous",
    "n'est à vous",
    "pas chez vous",
    "n'est chez vous",
    "pas de votre fait",
    "pas en cause",
    "chez google",
    "chez whatsapp",
    "chez facebook",
    "c'est google",
    "c'est whatsapp",
    "c'est facebook",
    "annuaire",          # « les annuaires », « deux annuaires », « un annuaire » : la cause est nommée
    "annuaires",
    "vous le louez",
    "ne vous appartient pas",
    "ne vous appartiennent pas",
]

# L'absolution seule — celle que King refuse. Elle n'est plus acceptée comme dédouanement : elle
# doit être suivie, dans la même phrase, par la cause nommée, sinon le message laisse le prospect
# devant deux questions sans réponse (« c'est la faute de qui ? », « où est le problème ? »).
ABSOLUTION_SEULE = [
    "ce n'est pas votre faute",
    "ce n'est pas votre travail",
    "ce n'est pas votre page",
    "ce n'est pas votre organisation",
    "aucun reproche",
    "vous n'y pouvez rien",
]

# Chaque phrase doit nommer l'endroit où le patient lit le prospect, ou le site qui répondrait.
# Ruling King 26/10 : « make sure each line you write in the messages makes the client aware he
# needs a site / a stronger online presence ». Une phrase qui ne nomme ni l'un ni l'autre est une
# phrase qui décrit le décor : elle se supprime ou elle se réécrit.
ANCRAGE = [
    "site", "en ligne", "google", "facebook", "whatsapp", "annuaire", "annuaires", "fiche",
    "profil", "registre", "tableau", "vitrine", "catalogue", "à vous", "chez vous", "votre nom",
]

# Désarmement — mécanisme 1 de Cameron Jeanes (26/10) : la première ligne excuse l'intrusion.
DESARMEMENT = ["inattendu", "surprenant", "surprend", "je sais que c'est", "sans doute", "étrange"]

# Preuve sociale — mécanisme 5. Un site qui existe déjà vaut mieux qu'une promesse : on nomme le
# métier et la ville, jamais un chiffre de résultat. **Ruling King 26/10** : le client n'est pas nommé
# tant qu'on ne lui a pas demandé (« je fais les sites pour les opticiens de Douala »), et la phrase
# reste une preuve d'existence — un site tourne, en ligne — pas un palmarès.
PREUVE = ["j'ai fait", "j'ai construit", "en ligne", "tourne", "un opticien d'ici", "le site d'un",
          "les sites pour les opticiens", "sites pour les opticiens", "site pour un opticien"]

# Verbes d'action — la question finale doit demander quelque chose de FIXABLE.
# Ajouté le 25/10 après le reproche de King le plus utile de la semaine : « what actions do we expect
# from the prospect? » — le message décrivait une capture et ne demandait rien. La porte mesurait la
# forme (mots, phrases, interdits) et laissait passer un message qui ne vendait rien. Ce contrôle ne
# remplace pas le jugement : il attrape le cas où la question finale est décorative.
VERBES_ACTION = ["voulez", "souhaitez", "préférez", "montre", "envoi", "propose", "dites", "dis-moi",
                 "donnez", "appel", "répondez", "regardez", "comparez", "essayez", "passe", "partage",
                 "transmet", "fixe", "choisissez"]

# Auto-présentation — ruling King 25/10 (141ᵉ message) : « on dit bonjour c'est King alors qu'au
# premier message on ne sait pas se présenter ». Une présentation qui ne porte pas la raison du message
# n'est pas une présentation, c'est du remplissage — et devant un prospect déjà tiède (il a reçu un
# message hier, il y a répondu), elle parle à un inconnu qu'il n'est pas.
SELF_INTRO = ["c'est king", "c'est akwo", "je suis king", "je suis akwo", "moi c'est king",
              "akwo king", "king de amk", "king, de amk"]

# Promesse de mesure — ruling King 25/10 (142ᵉ message). Un message ne peut promettre qu'un travail
# qu'on sait faire. La v6 demandait « combien de patients vous arrivent par Google ? » et promettait de
# comparer ce chiffre « à ce que la fiche laisse filer » : le gérant n'a aucun outil de suivi des appels,
# nous n'avons aucun accès à ses appels, donc la comparaison n'existait pas. Fermé ici pour de bon.
MESURE_IMPOSSIBLE = ["ce que la fiche laisse filer", "je le compare à", "combien ça vous coûte",
                     "je mesure vos", "combien de patients vous arrivent par google"]

# Sortie sans friction — knowledge/OUTREACH-MESSAGING §3, temps 5.
SORTIE = ["sans moi", "2 minutes", "deux minutes", "sans engagement", "le faire vous-même",
          "un mot", "une ligne", "un chiffre"]

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

    # 1 · longueur — CLIENT-MESSAGING-RULES §13. Le plafond passe de 55 à 70 mots le 26/10 :
    #     le désarmement et la preuve sociale entrent dans chaque message (ruling King), et chacun
    #     coûte six à dix mots. On monte le plafond d'autant, on ne le supprime pas — au-delà de
    #     quatre phrases, ça redevient le rapport d'incident que le §13 refuse.
    if msg.n_words > 70:
        msg.fails.append(f"{msg.n_words} mots (maximum 70) — §13")
    elif msg.n_words < 30:
        msg.warns.append(f"{msg.n_words} mots (plancher 35) — §13")
    n_sent = sentences(body)
    if n_sent > 4:
        msg.warns.append(f"{n_sent} phrases (la règle dit quatre depuis le 26/10) — §13")

    # 1 bis · chaque phrase vend le besoin — ruling King 26/10. Une phrase qui ne nomme ni
    #     l'endroit où le patient lit le prospect ni le site qui répondrait ne fait pas avancer
    #     la vente : elle décrit le décor.
    for sent in re.split(r"(?<=[.!?])\s+", body.strip()):
        if len(words(sent)) < 3:
            continue
        if not any(fold(a) in fold(sent) for a in ANCRAGE):
            msg.warns.append(
                "une phrase ne nomme ni l'endroit où le patient vous lit ni le site qui "
                f"répondrait — « {sent.strip()[:60]} » — ruling King 26/10")
            break

    # 1 ter · désarmement — mécanisme 1 de Cameron Jeanes. Il se juge sur l'ouverture, et seulement
    #     sur une **première touche froide** : un prospect tiède (il a déjà répondu) ne se désarme pas,
    #     il se rappelle à lui (§13 quater, ruling 141). Le repère est la salutation : elle est de
    #     règle sur un froid, et absente sur un tiède.
    froid = "bonjour" in fold(" ".join(words(body)[:3]))
    if froid and not any(fold(d) in fold(" ".join(words(body)[:12])) for d in DESARMEMENT):
        msg.warns.append(
            "pas de désarmement dans les douze premiers mots — la première ligne excuse "
            "l'intrusion, sinon elle se lit comme un guet-apens (Cameron Jeanes, 26/10)")

    # 1 quater · preuve sociale — mécanisme 5. Elle est nommable : DM Optique est en ligne.
    #     Même périmètre que le désarmement : une première touche froide.
    if froid and not any(fold(x) in flat for x in PREUVE):
        msg.warns.append(
            "aucune preuve sociale : dire le métier et la ville, et qu'un site tourne déjà — "
            "mécanisme 5, ruling King 26/10 (client jamais nommé sans son accord)")

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

    # 5 bis · auto-présentation — ruling 141. Bloque : c'est une règle de méthode, pas de goût.
    for s in SELF_INTRO:
        if s in flat:
            msg.fails.append(f"auto-présentation : « {s} » — la présentation doit porter la raison du "
                             f"message, pas le prénom seul — ruling 141 (25/10)")

    # 5 ter · promesse de mesure impossible — ruling 142.
    for m in MESURE_IMPOSSIBLE:
        if m in flat:
            msg.fails.append(f"promesse de mesure impossible : « {m} » — le prospect n'a pas l'outil, "
                             f"nous n'avons pas l'accès — ruling 142 (25/10)")

    # 6 · la cause nommée — §13 temps 2, réécrit le 26/10. Deux fautes distinctes :
    #     a) le message observe quelque chose chez lui et ne nomme aucune cause ;
    #     b) il absout sans dire qui détient l'information — c'est le défaut que King a nommé.
    if not any(fold(c) in flat for c in CAUSE) and any(fold(o) in flat for o in OBSERVATION):
        msg.warns.append(
            "pas de cause nommée : le fait se lira comme un reproche — dire qui détient "
            "l'information (Google, WhatsApp, les annuaires) — §13 temps 2")
    for sent in re.split(r"(?<=[.!?])\s+", body):
        f_sent = fold(sent)
        if any(fold(a) in f_sent for a in ABSOLUTION_SEULE) and not any(fold(c) in f_sent for c in CAUSE):
            msg.warns.append(
                "absolution qui n'explique rien : « c'est la faute de qui ? » et « où est le "
                "problème ? » restent sans réponse — nommer la cause dans la même phrase "
                "(ruling King 26/10)")
            break

    # 7 · sortie sans friction — knowledge §3 temps 5 (avertissement : deux structures coexistent)
    if not any(fold(x) in flat for x in SORTIE):
        msg.warns.append("pas de sortie sans friction — OUTREACH-MESSAGING §3 temps 5")

    # 7 bis · une question à deux branches — le §13 interdit « deux questions » ;
    # « A ou B ? » en est une seule à l'écrit, mais deux réponses à choisir à l'oral.
    for sent in re.split(r"(?<=[.!?])\s+", body):
        if sent.rstrip().endswith("?") and " ou " in fold(sent):
            msg.warns.append("question à deux branches (« X ou Y ? ») — justifier ou simplifier, §13")
            break

    # 7 ter · une sortie sans friction qui ne dit pas ce qu'elle produit — ruling 141 : « un mot
    #        suffit pour faire quoi ?? ». Une phrase de sortie seule (≤ 4 mots) en fin de message
    #        demande une réponse sans nommer son usage.
    last = [s for s in re.split(r"(?<=[.!?])\s+", body.strip()) if s.strip()]
    if last:
        tail = fold(last[-1])
        if len(words(last[-1])) <= 4 and any(fold(x) in tail for x in SORTIE):
            msg.warns.append("sortie seule en fin de message : elle ne dit pas ce que la réponse "
                             "produit (« un mot suffit » — pour faire quoi ?) — ruling 141 (25/10)")

    # 8 · le quartier doit apparaître tôt — DECLINAISON §1①, six premiers mots
    q = fold(msg.quartier.split("(")[0].strip())
    first = fold(" ".join(words(body)[:12]))
    if q and q not in first:
        msg.warns.append(f"« {msg.quartier} » absent des 12 premiers mots — DECLINAISON §1①")

    # 9 · la question finale doit demander quelque chose — leçon du 25/10 (« what actions do we
    #     expect from the prospect? »). Un message qui passe la forme peut ne rien vendre.
    questions = [s for s in re.split(r"(?<=[.!?])\s+", body) if s.rstrip().endswith("?")]
    if questions:
        qlast = fold(questions[-1])
        if not any(v in qlast for v in VERBES_ACTION):
            msg.warns.append("la question finale ne demande aucune action (ni « voulez », ni « montre », "
                             "ni « dites »…) — elle est décorative, à réécrire")


# ── §10 · la ressemblance — la seule règle que le volume ajoute ─────────────────────────────────
#
# Ajouté le 26/10 quand King est passé de 1 à 20-50 messages par jour. Le risque change de nature :
# un message seul ne peut pas ressembler à lui-même. Quarante messages qui partagent une phrase sont,
# pour WhatsApp, un compte qui diffuse — et la sanction ne vient pas du contenu, elle vient du motif.
#
# Le seuil est calibré sur le lot du 26/10 (sept messages écrits à la main) : Jaccard maximal 0,124,
# une séquence de douze mots partagée par deux messages. Ce lot reste donc propre, et la règle ne
# s'allume qu'au-delà. Une séquence vue dans trois messages est bloquante à partir de là ; deux, dans
# un lot de douze ou plus, est un avertissement ; en dessous de douze messages, deux n'est pas un motif.

SEQ = 12          # longueur de la séquence qui compte pour WhatsApp
SHINGLE = 6       # longueur pour la ressemblance globale
JACCARD_FAIL = 0.45
JACCARD_WARN = 0.30


def _n_grams(t: str, n: int) -> set[tuple[str, ...]]:
    w = fold(t).split()
    return {tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def ressemblance(msgs: list[Message]) -> None:
    from collections import Counter

    seqs = {m.line: _n_grams(m.body, SEQ) for m in msgs}
    vus: Counter = Counter(g for s in seqs.values() for g in s)

    for m in msgs:
        pire = max((vus[g] for g in seqs[m.line]), default=0)
        if pire >= 3:
            m.fails.append(f"une séquence de {SEQ} mots revient dans {pire} messages — signature de "
                           f"diffusion (§10). Changer la phrase, pas le prénom")
        elif pire == 2 and len(msgs) >= 12:
            m.warns.append(f"une séquence de {SEQ} mots est partagée avec un autre message du lot (§10)")

    for i, a in enumerate(msgs):
        for b in msgs[i + 1:]:
            if fold(a.body) == fold(b.body):
                a.fails.append(f"corps identique à « {b.label} » — un seul envoi, pas deux (§10)")
                continue
            sa, sb = _n_grams(a.body, SHINGLE), _n_grams(b.body, SHINGLE)
            if not (sa | sb):
                continue
            j = len(sa & sb) / len(sa | sb)
            if j >= JACCARD_FAIL:
                a.fails.append(f"trop proche de « {b.label} » ({j:.0%} de recouvrement) — (§10)")
            elif j >= JACCARD_WARN:
                a.warns.append(f"proche de « {b.label} » ({j:.0%}) — varier la phrase (§10)")


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
    ressemblance(msgs)
    for m in msgs:
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
