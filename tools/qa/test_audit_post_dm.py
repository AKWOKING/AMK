#!/usr/bin/env python3
"""Banc de `audit_post_dm.py` — la porte du kit client (profil DM Optique).

    python3 tools/qa/test_audit_post_dm.py

Chaque refus a son **contre-exemple qui passe**. La dernière famille est la seule qui compte vraiment :
le kit réel du 27/10 (`clients/dm-optic/content/month1/w3/KIT-27-10-HOOK.md`) passe sans un
avertissement.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_post_dm import _nombres, audit  # noqa: E402

CAS = []


def cas(nom):
    def enveloppe(fn):
        CAS.append((nom, fn))
        return fn

    return enveloppe


HOOK = (
    "| Composante | Ce qui est écrit / montré / dit | Secondes |\n"
    "|---|---|---|\n"
    "| **texte** | **8 HEURES À 40 CM · 20 SECONDES À 6 MÈTRES** | 0,0–3,0 |\n"
    "| **visuel** | l'intérieur du cabinet, zoom arrière lent | 0,0–3,0 |\n"
    "| **parlé** | « Vingt minutes d'écran. Puis vingt secondes. À six mètres. » | 0,0–3,2 |\n\n"
    "Trois accroches écrites : ① retenue · ② écartée · ③ écartée — deux écartées.\n"
)

LIEN_TT = "https://wa.me/237656122239?text=Bonjour%2C%20vu%20la%20video%20TikTok"
LIEN_FB = "https://wa.me/237656122239?text=Bonjour%2C%20vu%20la%20publication%20Facebook"

CAP_TT = (
    "8 heures à 40 cm. 20 secondes à 6 mètres. C'est tout.\n\n"
    "Écrivez-nous : " + LIEN_TT + "\n\n#dmoptique #opticienbonaberi #douala"
)
CAP_FB = (
    "8 heures à 40 cm. 20 secondes à 6 mètres.\n\n"
    "Écrivez-nous : " + LIEN_FB + "\n\n#dmoptique #opticienbonaberi #douala"
)

TT_SECTION = (
    "Sous-titres manuels. Commentaire épinglé : WhatsApp 656 122 239, examen 8h30–13h00.\n\n"
    "```text\n" + CAP_TT + "\n```\n"
)
FB_SECTION = (
    "Alt text : « Intérieur du cabinet DM Optique à Bonabéri. »\n\n"
    "```text\n" + CAP_FB + "\n```\n"
)
ACCUEIL = (
    "> Bonjour, ici **DM Optique**, Ndobo Mayor — vous écrivez pour un examen de vue ?\n"
    "> L'examen se fait le matin, 8h30–13h00.\n"
)
TABLE = (
    "| Moment | Vues | Messages reçus | Conversations qualifiées |\n|---|---|---|---|\n| J+1 | | | |\n"
)


def kit(hook: str | None = None, tt: str | None = None, fb: str | None = None,
        accueil: str | None = None, table: str | None = None) -> str:
    return (
        "# KIT — test\n\n"
        "## 1 · L'accroche\n\n" + (HOOK if hook is None else hook) + "\n"
        "## 2 · TikTok\n\n" + (TT_SECTION if tt is None else tt) + "\n"
        "## 3 · Facebook\n\n" + (FB_SECTION if fb is None else fb) + "\n"
        "## 4 · La réponse d'accueil\n\n" + (ACCUEIL if accueil is None else accueil) + "\n"
        "## 5 · Ce qu'on compte\n\n" + (TABLE if table is None else table) + "\n"
    )


def _audit(texte: str):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(texte)
        chemin = f.name
    try:
        return audit(chemin)
    finally:
        Path(chemin).unlink(missing_ok=True)


def _refus(nom_cas: str, motif: str, texte: str):
    v = _audit(texte)
    assert not v.ok, f"{nom_cas} : aurait dû échouer"
    assert any(motif in f for f in v.fails), f"{nom_cas} : {motif} attendu, reçu {v.fails}"


# ── ① le kit de référence passe ─────────────────────────────────────────────────────────────────
@cas("le kit de référence passe, sans avertissement")
def _():
    v = _audit(kit())
    assert v.ok, v.fails
    assert not v.warns, v.warns


@cas("le kit réel du 27/10 passe")
def _():
    chemin = (Path(__file__).resolve().parents[2]
              / "clients/dm-optic/content/month1/w3/KIT-27-10-HOOK.md")
    v = audit(chemin)
    assert v.ok, v.fails
    assert not v.warns, v.warns


# ── ② l'accroche : trois composantes, alignées, à l'heure ───────────────────────────────────────
@cas("une composante manquante est refusée")
def _():
    hook = HOOK.replace("| **visuel** | l'intérieur du cabinet, zoom arrière lent | 0,0–3,0 |\n", "")
    _refus("hook incomplet", "[hook-incomplet]", kit(hook=hook))


@cas("un texte qui ne partage pas les nombres de la voix est refusé")
def _():
    hook = HOOK.replace("**8 HEURES À 40 CM · 20 SECONDES À 6 MÈTRES**", "**LA RÈGLE DES ÉCRANS**")
    _refus("désaligné", "[hook-desaligne]", kit(hook=hook))


@cas("un texte à l'écran qui arrive après 3 s est refusé")
def _():
    hook = HOOK.replace("| 0,0–3,0 |", "| 0,0–5,0 |", 1)
    _refus("hook tardif", "[hook-tardif]", kit(hook=hook))


@cas("moins de trois accroches écrites avertit")
def _():
    hook = HOOK.replace("Trois accroches écrites : ① retenue · ② écartée · ③ écartée — deux écartées.\n", "")
    v = _audit(kit(hook=hook))
    assert v.ok and any("variantes-absentes" in w for w in v.warns), v.warns


# ── ③ les légendes ───────────────────────────────────────────────────────────────────────────────
@cas("une seule légende est refusée")
def _():
    _refus("section manquante", "[sections-manquantes]", kit(fb=""))


@cas("une accroche de plus de 100 caractères est refusée")
def _():
    longue = ("8 heures à 40 cm et 20 secondes à 6 mètres, voilà toute la règle des écrans et elle est simple "
              "à retenir pour vous.\n\n")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n"
          + longue + "Écrivez-nous : " + LIEN_TT + "\n\n#dmoptique #douala #cameroun\n```\n")
    _refus("accroche longue", "[accroche-longue]", kit(tt=tt))


@cas("deux actions dans la même légende sont refusées")
def _():
    cap = (CAP_TT.replace("Écrivez-nous", "Écrivez-nous ou appelez-nous")
           .replace("Ecrivez-nous", "Écrivez-nous ou appelez-nous"))
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("deux CTA", "[deux-cta]", kit(tt=tt))


@cas("une légende sans action est refusée")
def _():
    cap = CAP_TT.replace("Écrivez-nous : ", "")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("CTA absent", "[cta-absent]", kit(tt=tt))


@cas("le même lien collé sur les deux plateformes est refusé")
def _():
    cap_fb = CAP_FB.replace(LIEN_FB, LIEN_TT)
    fb = ("Alt text : « cabinet ». \n\n```text\n" + cap_fb + "\n```\n")
    _refus("attribution faible", "[attribution-faible]", kit(fb=fb))


@cas("un lien sans texte prérempli est refusé")
def _():
    cap = CAP_TT.replace(LIEN_TT, "https://wa.me/237656122239")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("lien absent", "[lien-absent]", kit(tt=tt))


# ── ④ les verrous client ────────────────────────────────────────────────────────────────────────
@cas("un prix dans la légende est refusé")
def _():
    cap = CAP_TT.replace("C'est tout.", "C'est tout. Monture à 45 000 FCFA.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("prix", "[prix-dans-la-legende]", kit(tt=tt))


@cas("une promesse est refusée")
def _():
    cap = CAP_TT.replace("C'est tout.", "C'est tout. Résultat garanti.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("promesse", "[promesse]", kit(tt=tt))


@cas("une allégation santé affirmée est refusée")
def _():
    cap = CAP_TT.replace("C'est tout.", "C'est tout. On corrige définitivement la vue.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("allégation santé", "[allegation-sante]", kit(tt=tt))


@cas("la négation « ce n'est pas un traitement » est permise")
def _():
    cap = CAP_TT.replace("C'est tout.", "C'est tout. Ce n'est pas un traitement, c'est une pause.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    v = _audit(kit(tt=tt))
    assert v.ok, v.fails


# ── ⑤ les hashtags ──────────────────────────────────────────────────────────────────────────────
@cas("un hashtag local manquant est refusé")
def _():
    cap = CAP_TT.replace("#douala", "#lunettes")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("local absent", "[local-absent]", kit(tt=tt))


@cas("la marque manquante est refusée")
def _():
    cap = CAP_TT.replace("#dmoptique", "#opticien")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("marque absente", "[marque-absente]", kit(tt=tt))


@cas("deux hashtags seulement sont refusés")
def _():
    cap = CAP_TT.replace(" #opticienbonaberi #douala", "")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("hashtags hors borne", "[hashtags-hors-borne]", kit(tt=tt))


@cas("la mendicité de vues est refusée")
def _():
    cap = CAP_TT + " #fyp"
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("mendicité", "[mendicite]", kit(tt=tt))


# ── ⑥ la forme du kit ───────────────────────────────────────────────────────────────────────────
@cas("des sous-titres automatiques sont refusés")
def _():
    tt = ("Sous-titres automatiques. Commentaire épinglé.\n\n```text\n" + CAP_TT + "\n```\n")
    _refus("sous-titres auto", "[sous-titres-auto]", kit(tt=tt))


@cas("un commentaire épinglé manquant est refusé")
def _():
    tt = ("Sous-titres manuels.\n\n```text\n" + CAP_TT + "\n```\n")
    _refus("épinglé absent", "[epingle-absent]", kit(tt=tt))


@cas("un texte alternatif manquant est refusé")
def _():
    fb = "```text\n" + CAP_FB + "\n```\n"
    _refus("alt absent", "[alt-absent]", kit(fb=fb))


@cas("aucune heure de consultation est refusée")
def _():
    _refus("horaires absents", "[horaires-absents]",
           kit(accueil=ACCUEIL.replace("8h30–13h00", "le matin")).replace("8h30–13h00", "le matin"))


@cas("une réponse qui ne nomme pas le cabinet est refusée")
def _():
    _refus("nom tardif", "[nom-tardif]",
           kit(accueil="> Bonjour, vous écrivez pour un examen ?\n> Le matin, 8h30–13h00.\n"))


@cas("un compteur sans colonnes de décision est refusé")
def _():
    _refus("compteur absent", "[compteur-absent]", kit(table="| Moment | Vues |\n|---|---|\n| J+1 | |\n"))


# ── ⑦ la pièce muette ───────────────────────────────────────────────────────────────────────────
@cas("une pièce déclarée muette passe, et le dit")
def _():
    hook = HOOK.replace("| **parlé** | « Vingt minutes d'écran. Puis vingt secondes. À six mètres. » | 0,0–3,2 |",
                        "| **parlé** | **aucune voix** — pièce muette : le texte porte tout | 0,0–3,0 |")
    v = _audit(kit(hook=hook))
    assert v.ok, v.fails
    assert any("piece-muette" in w for w in v.warns), v.warns


# ── ⑧ la mécanique d'abonné (doctrine du 27/10) ─────────────────────────────────────────────────
@cas("demander un abonnement est refusé")
def _():
    cap = CAP_TT.replace("C'est tout.", "C'est tout. Abonnez-vous pour la suite.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("mendicité d'abonnement", "[abonnement-mendicite]", kit(tt=tt))


@cas("une série déclarée sans boucle ouverte est refusée")
def _():
    texte = kit().replace("# KIT — test", "# KIT — série « la monture »")
    _refus("série sans boucle", "[serie-sans-boucle]", texte)


@cas("une série qui promet la suite passe")
def _():
    texte = kit().replace("# KIT — test", "# KIT — série « la monture »")
    cap_tt = CAP_TT.replace("C'est tout.", "C'est tout. Demain : la deuxième monture.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap_tt + "\n```\n")
    v = _audit(kit(tt=tt).replace("# KIT — test", "# KIT — série « la monture »"))
    assert v.ok, v.fails


@cas("un épisode numéroté sans suite promise est refusé")
def _():
    # le refus porte sur la série déclarée, pas sur le mot « épisode » employé seul dans un titre
    cap = CAP_TT.replace("C'est tout.", "C'est tout l'épisode 1.")
    tt = ("Sous-titres manuels. Commentaire épinglé.\n\n```text\n" + cap + "\n```\n")
    _refus("épisode sans boucle", "[serie-sans-boucle]", kit(tt=tt))


# ── ⑨ l'alignement texte / voix, y compris les écritures qui collent la lettre au chiffre ────────
HOOK_H08 = (
    "| Composante | Ce qui est écrit / montré / dit | Secondes |\n"
    "|---|---|---|\n"
    "| **texte** | **ELLE N'A PAS DE NOM** (0,0–2,2) · **H08 · DOUBLE PONT** · **UN QUARTIER / UNE VILLE** | 0,0–2,2 |\n"
    "| **visuel** | la monture en macro, cadre en mouvement | 0,0–2,2 |\n"
    "| **parlé** | « Votre monture n'a pas de nom. » puis « H08, double pont. » puis « Un quartier, une ville. » | 0,0–2,2 |\n\n"
    "Trois accroches écrites : ① retenue · ② écartée · ③ écartée — deux écartées.\n"
)


@cas("une référence produit et une heure sont des nombres, pas du décor")
def _():
    assert _nombres("H08 · double pont") == {8}, _nombres("H08 · double pont")
    assert {8, 30, 13} <= _nombres("examen 8h30–13h00"), _nombres("examen 8h30–13h00")


@cas("une fenêtre de temps ne compte pas comme un nombre commun")
def _():
    assert _nombres("0,0–2,2 puis 4,0–9,0") == set(), _nombres("0,0–2,2 puis 4,0–9,0")


@cas("texte et voix qui disent tous deux H08 et « un quartier » : alignés")
def _():
    v = _audit(kit(hook=HOOK_H08))
    assert v.ok, v.fails


@cas("une voix qui ne reprend ni la référence ni le nom : refusée")
def _():
    hook = HOOK_H08.replace(
        "| **parlé** | « Votre monture n'a pas de nom. » puis « H08, double pont. » puis « Un quartier, une ville. » | 0,0–2,2 |",
        "| **parlé** | « Elle n'a pas encore de nom. » puis « C'est vous qui choisirez. » | 0,0–2,2 |",
    )
    _refus("voix désalignée", "[hook-desaligne]", kit(hook=hook))


def main() -> int:
    ko = 0
    for nom, fn in CAS:
        try:
            fn()
            print(f"✓ {nom}")
        except AssertionError as e:
            ko += 1
            print(f"✗ {nom} — {e}")
    print(f"\n{len(CAS) - ko}/{len(CAS)} cas passés")
    return 1 if ko else 0


if __name__ == "__main__":
    raise SystemExit(main())
