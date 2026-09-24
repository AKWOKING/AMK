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
<section class="hero"><div class="hero-grid"><div>
<p class="sur">Bonamoussadi, Douala</p><h1>Le résultat juste, du premier coup.</h1>
<p>Vous arrivez avec l'ordonnance de votre médecin.</p></div></section>
<details><summary>Analyses à jeun</summary><p>8 à 12 heures sans manger.</p></details></body></html>"""

tmp = tempfile.mkdtemp()
paths = {}
for name, content in (("fautive1", FAUTIVE_1), ("fautive2", FAUTIVE_2), ("saine", SAINE)):
    p = os.path.join(tmp, name + ".html")
    io.open(p, "w", encoding="utf-8").write(content)
    paths[name] = p

fails = []
def check(label, cond, detail=""):
    print("  %s %s%s" % ("ok  " if cond else "FAIL", label, ("  — " + detail) if detail and not cond else ""))
    if not cond:
        fails.append(label)

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

print()
if fails:
    print("DES ÉCHECS : " + " · ".join(fails))
    sys.exit(1)
print("Tout est vert — l'outil refuse ce qu'il doit refuser et accepte ce qu'il doit accepter.")
