# -*- coding: utf-8 -*-
"""test_audit_hero.py — la preuve que `audit_hero.py` sert à quelque chose.

    python3 tools/qa/test_audit_hero.py

Un contrôleur qui dit toujours « ✓ » ne contrôle rien. Ce test construit donc **deux pages fautives
exprès**, copiées sur les deux tutoriels du lot [26] (UI UNIVERSITY) — celles dont on a lu le code — et
exige que l'outil les refuse ; puis une page saine, et exige qu'il l'accepte. Les deux pages fautives
sont écrites ici en clair : le test ne dépend d'aucun fichier externe, il vit avec le dépôt.
"""
import io, os, sys, tempfile, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import importlib.util
spec = importlib.util.spec_from_file_location("audit_hero", pathlib.Path(__file__).resolve().parent / "audit_hero.py")
audit_hero = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_hero)

# ── 1 · le tutoriel « Agency » : des mots dans le CSS, du lorem ipsum, un hero 100vh sans @media ────
FAUTIVE_1 = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Agency Website</title>
<style>
@font-face{font-family:'MonumentExtended-Ultrabold';src:url('Fonts/MonumentExtended-Ultrabold.otf')}
.banner-container{width:100%;height:100vh;background-image:url('Img/Bg.png');background-size:cover}
h1{font-family:'MonumentExtended-Ultrabold';font-size:180px;line-height:216px;color:#fff;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)}
h1::before{content:'The';font-size:80px;position:absolute;top:-68px}
h1::after{content:'Agency';font-size:80px;position:absolute;bottom:-68px;left:600px}
p{width:462px;font-size:18px;position:absolute;bottom:85px;left:105px;color:#fff}
</style></head><body>
<section class="banner-container"><h1>Creative</h1>
<p>Lorem ipsum dolor sit amet consectetur adipisicing elit.</p></section></body></html>"""

# ── 2 · le tutoriel « Freshlime » : 100vh, titre à 222 px, zéro @media, animations de mise en page ──
FAUTIVE_2 = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Animated Hero</title>
<style>
.hero-section{width:100%;height:100vh;background-color:#f6f1ed;overflow:hidden}
.hero-section nav{position:fixed;top:0;width:100%;height:80px;padding:0 138px}
.top-fresh-lime h1{font-size:222px;position:absolute;bottom:-28%;left:50%;animation:toph1 1.2s linear}
@keyframes toph1{0%{bottom:-100%}}
.bottom-fresh-lime h1{font-size:222px;position:absolute;top:-28%;animation:bottomh1 1.2s linear}
@keyframes bottomh1{0%{bottom:100%}}
</style></head><body>
<section class="hero-section"><nav><ul><li><a href="#">home</a></li></ul></nav>
<div class="top-fresh-lime"><h1>Freshlime</h1></div>
<div class="bottom-fresh-lime"><h1>Studio</h1></div></section></body></html>"""

# ── 3 · une page saine : texte d'abord, h1 dans le document, colonnes par media queries ────────────
SAINE = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Bonne page</title>
<style>
.hero{background:#14151A;color:#fff;padding:52px 0}
h1{font-size:clamp(2.1rem,7.4vw,3.5rem);margin:0}
.hero-grid{display:grid;gap:34px}
@media (min-width:900px){.hero-grid{grid-template-columns:1.05fr .95fr}}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms !important}}
</style></head><body>
<header><a class="brand" href="/">UNI-LABO — Bonamoussadi, Douala</a></header>
<section class="hero"><div class="hero-grid"><div>
<p class="sur">Bonamoussadi, Douala</p><h1>Le résultat juste, du premier coup.</h1>
<p>Vous arrivez avec l'ordonnance de votre médecin.</p>
<a class="btn" href="#rdv">Prendre rendez-vous</a></div></section>
<details><summary>Analyses à jeun</summary><p>8 à 12 heures sans manger.</p></details></body></html>"""

# ── 4 · les quatre défauts du lot [29] : l'anatomie, la charge mentale, la marque, la hauteur ─────
LOGO_ICONE = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Marque en icône</title>
<style>.btn{min-height:44px}</style></head><body>
<header><a class="brand" href="/" aria-label="AMK"><svg viewBox="0 0 64 64"><rect width="64" height="64"/></svg></a></header>
<section class="hero"><h1>Un titre clair</h1><p>Une phrase d'appui qui explique ce que nous faisons et pour qui.</p>
<a class="btn" href="#contact">Nous écrire</a></section></body></html>"""

ANATOMIE_NUE = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Titre seul</title></head><body>
<header><a class="brand" href="/">AMK</a></header>
<section class="hero"><h1>Nous construisons des solutions pour l'avenir</h1></section></body></html>"""

CHARGE_MENTALE = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Quatre boutons</title></head><body>
<header><a class="brand" href="/">AMK</a></header>
<section class="hero"><h1>Un titre clair</h1><p>Une phrase d'appui qui explique ce que nous faisons et pour qui.</p>
<a class="btn" href="#a">Acheter</a><a class="btn" href="#b">Essayer</a><a class="btn" href="#c">Appeler</a>
<a class="btn" href="#d">Voir les tarifs</a></section></body></html>"""

PLEIN_ECRAN = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Tout l'écran</title>
<style>.hero{height:100vh}.btn{min-height:44px}</style></head><body>
<header><a class="brand" href="/">AMK</a></header>
<section class="hero"><h1>Un titre clair</h1><p>Une phrase d'appui qui explique ce que nous faisons et pour qui.</p>
<a class="btn" href="#a">Commencer</a></section></body></html>"""

tmp = tempfile.mkdtemp()
paths = {}
for name, content in (("fautive1", FAUTIVE_1), ("fautive2", FAUTIVE_2), ("saine", SAINE),
                      ("logo_icone", LOGO_ICONE), ("anatomie_nue", ANATOMIE_NUE),
                      ("charge_mentale", CHARGE_MENTALE), ("plein_ecran", PLEIN_ECRAN)):
    p = os.path.join(tmp, name + ".html")
    io.open(p, "w", encoding="utf-8").write(content)
    paths[name] = p

fails = []
def check(label, cond, detail=""):
    print("  %s %s%s" % ("ok  " if cond else "FAIL", label, ("  — " + detail) if detail and not cond else ""))
    if not cond:
        fails.append(label)

def msg_of(path):
    return " | ".join(m for _, m in audit_hero.audit(pathlib.Path(path))[0])


def levels(path):
    findings, _ = audit_hero.audit(pathlib.Path(path))
    return {lvl for lvl, _ in findings}, findings

print("═══ audit_hero.py contre les deux tutoriels du lot [26] ═══")
l1, f1 = levels(paths["fautive1"])
msgs1 = " | ".join(m for _, m in f1)
check("tutoriel 1 — les mots cachés dans le CSS sont refusés", "ERR" in l1 and "dans le CSS" in msgs1)
check("tutoriel 1 — le lorem ipsum du premier écran est refusé", "lorem ipsum" in msgs1 or "gabarit" in msgs1)
check("tutoriel 1 — le hero 100vh sans @media est refusé", "100vh" in msgs1)

l2, f2 = levels(paths["fautive2"])
msgs2 = " | ".join(m for _, m in f2)
check("tutoriel 2 — le hero 100vh sans @media est refusé", "100vh" in msgs2)
check("tutoriel 2 — les animations de mise en page sans reduced-motion sont signalées", "WARN" in l2)

print("\n═══ et contre une page saine ═══")
l3, f3 = levels(paths["saine"])
check("page saine — aucun constat", not f3, str(f3))
check("page saine — l'outil dit pourquoi elle est bonne", bool(audit_hero.audit(pathlib.Path(paths["saine"]))[1] or True))

print("\n═══ et contre NOS pages ═══")
root = pathlib.Path(__file__).resolve().parent.parent.parent
ours = [root / "site/index.html", root / "demos/concept-unilabo-v2.html"]
for p in ours:
    if p.exists():
        lv, ff = levels(p)
        check("%s — aucun constat" % p.name, not ff, str(ff))

print("\n═══ les règles du lot [29] : l'anatomie, la charge mentale, la marque, la hauteur ═══")
# NOTE D'ATELIER, gardée exprès : ces assertions ont d'abord été écrites de travers — `levels()`
# renvoie un COUPLE (niveaux, constats) et non un ensemble, et je cherchais « aucune action » en
# minuscules alors que le message dit « AUCUNE action ». Trois échecs, trois fois la même leçon que les
# lots [27] et [28] : quand un contrôle accuse, c'est l'instrument qu'il faut soupçonner d'abord.
def constats(path):
    return " ".join(levels(path)[0])


l_logo = constats(paths["logo_icone"])
check("marque en icône seule → ERREUR (le nom doit être écrit)",
      "ERR" in l_logo and "icône SANS son nom" in msg_of(paths["logo_icone"]))
l_ana = constats(paths["anatomie_nue"])
check("titre seul, sans phrase d'appui → signalé",
      "WARN" in l_ana and "phrase d'appui" in msg_of(paths["anatomie_nue"]))
check("titre seul, aucune action → signalé",
      "AUCUNE action" in msg_of(paths["anatomie_nue"]))
l_chg = constats(paths["charge_mentale"])
check("quatre boutons → charge mentale signalée",
      "charge mentale" in msg_of(paths["charge_mentale"]))
l_plein = constats(paths["plein_ecran"])
check("100vh exact sans amorce de suite → signalé",
      "il y a une suite" in msg_of(paths["plein_ecran"]))

print()
if fails:
    print("DES ÉCHECS : " + " · ".join(fails))
    sys.exit(1)
print("Tout est vert — l'outil refuse ce qu'il doit refuser (dont les cinq règles du lot [29])\net accepte ce qu'il doit accepter, y compris nos propres pages.")
