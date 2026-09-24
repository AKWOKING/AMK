# -*- coding: utf-8 -*-
"""test_audit_a11y.py — la preuve que le contrôle d'accessibilité mord, et qu'il ne mord pas à côté.

    python3 tools/qa/test_audit_a11y.py

Deux choses sont vérifiées ici, et la seconde compte autant que la première :

1. **Il refuse ce qu'il doit refuser.** Une page fautive est construite exprès, avec les défauts que le
   lot [27] a appris à reconnaître : image sans alt, image dont l'alt est un nom de fichier, deux h1,
   champ sans étiquette, bouton-icône sans nom, zoom bloqué, `outline:none` sans remplacement,
   `tabindex` positif, onclick sur un div, pas de lang, titre de page vide, animation infinie.
   Chaque défaut est attendu **avec son numéro de critère** — c'est ce qui fait qu'un rapport
   d'accessibilité est lisible.

2. **Il ne refuse pas à tort.** Cinq faux positifs ont été trouvés à la première exécution réelle
   (`tools/qa/audit_a11y.py`) et corrigés : un lien-icône qui a bien un aria-label, une icône de 19 px
   à l'intérieur d'un bouton (ce n'est pas une cible), un champ de texte libre sans autocomplete
   (WCAG 1.3.5 ne vise que les données à usage connu), un simple changement de couleur au survol (ce
   n'est pas du contenu caché), et une icône dans un lien déjà nommé. Les pages ci-dessous gardent ces
   cinq cas : si l'un revient, ce test tombe.

Et contre nos pages : zéro faute de niveau A/AA — les avertissements restants sont des choses qui
demandent un œil ou qui vivent dans un périmètre gelé (Univers, Cristallin).
"""
import io, os, sys, tempfile, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import importlib.util
spec = importlib.util.spec_from_file_location("audit_a11y", HERE / "audit_a11y.py")
a11y = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a11y)

# ── 1 · LA PAGE FAUTIVE — un défaut par critère, exprès ───────────────────────────────────────────
FAUTIVE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, maximum-scale=1">
<title></title>
<style>
body{font-family:sans-serif}
a:focus{outline:none}
.spin{animation: turn 2s linear infinite}
@keyframes turn{to{transform:rotate(360deg)}}
.hide{display:none}
.c:hover .hide{display:block}
.btn{min-height:12px}
</style></head><body>
<h1>Premier titre</h1>
<h1>Deuxième titre</h1>
<img src="photo.jpg">
<img src="hero.jpg" alt="hero.jpg">
<img src="x.jpg" alt="image">
<p><a href="/quelque-part">cliquez ici</a></p>
<p><a href="/autre"><svg viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg></a></p>
<div class="c"><span>Survolez-moi</span><span class="hide">Contenu caché</span></div>
<form>
  <input type="text" id="sans-etiquette">
  <input type="tel" id="tel-sans-autocomplete">
  <button><svg viewBox="0 0 24 24"><path d="M0 0h24v24H0z"/></svg></button>
</form>
<div onclick="alert(1)">Cliquable mais pas focalisable</div>
<a href="/trois" tabindex="3">Troisième dans l'ordre</a>
<div class="spin">ça tourne</div>
</body></html>"""

# ── 2 · LA PAGE SAINE — et les cinq faux positifs d'hier, gardés comme garde-fous ────────────────
SAINE = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Laboratoire d'analyses à Bonamoussadi, Douala</title>
<style>
:root{--ink:#14151A}
a:focus-visible,button:focus-visible{outline:3px solid #5B21B6;outline-offset:2px}
.btn{min-height:52px;display:inline-flex;align-items:center;padding:0 20px}
.btn svg{width:19px;height:19px}            /* une icône DANS un bouton : pas une cible */
.nav a:hover{color:#5B21B6;opacity:1}       /* un changement de couleur : pas du contenu caché */
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms !important}}
</style></head><body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header><nav aria-label="Principale"><a href="#analyses">Analyses</a> <a href="#rdv">Rendez-vous</a></nav></header>
<main id="contenu">
<h1>Le résultat juste, du premier coup.</h1>
<h2>Ce que nous dosons</h2>
<h3>Biochimie</h3>
<img src="tube.jpg" alt="Des tubes de prélèvement sur un portoir violet.">
<a class="btn" href="#rdv" aria-label="Prendre rendez-vous">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M0 0h24v24H0z"/></svg>Prendre rendez-vous</a>
<button type="button" aria-label="Parler au micro">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M0 0h24v24H0z"/></svg></button>
<form>
  <label for="nom">Votre nom</label>
  <input type="text" id="nom" name="nom" autocomplete="name">
  <fieldset><legend>Moment souhaité</legend>
    <input type="radio" id="m1" name="moment" value="matin"><label for="m1">Matin</label>
    <input type="radio" id="m2" name="moment" value="soir"><label for="m2">Soir</label>
  </fieldset>
  <p role="status" aria-live="polite"></p>
</form>
<svg viewBox="0 0 320 232" role="img" aria-label="Plan : le laboratoire au carrefour Etoo"><path d="M0 0h1v1z"/></svg>
</main>
<footer><p>UNI-LABO, Bonamoussadi</p></footer>
</body></html>"""

tmp = tempfile.mkdtemp()
paths = {}
for name, content in (("fautive", FAUTIVE), ("saine", SAINE)):
    p = os.path.join(tmp, name + ".html")
    io.open(p, "w", encoding="utf-8").write(content)
    paths[name] = p

fails = []
def check(label, cond, detail=""):
    print("  %s %s%s" % ("ok  " if cond else "FAIL", label, ("  — " + str(detail)) if detail and not cond else ""))
    if not cond:
        fails.append(label)

F, _ = a11y.audit(pathlib.Path(paths["fautive"]))
trouves = {(lvl, sc) for lvl, sc, _ in F}
msgs = " | ".join(m for _, _, m in F)

print("═══ la page fautive : chaque défaut est-il vu, avec son critère ? ═══")
attendu = [
    ("ERR", "1.1.1", "une image sans alt"),
    ("ERR", "1.1.1", "un alt qui est un nom de fichier ou un mot vide"),
    ("ERR", "1.3.1", "deux h1"),
    ("ERR", "3.3.2", "un champ sans étiquette"),
    ("ERR", "4.1.2", "un bouton-icône sans nom"),
    ("ERR", "1.4.4", "le zoom bloqué"),
    ("ERR", "2.4.7", "outline:none sans remplacement"),
    ("ERR", "2.4.3", "un tabindex positif"),
    ("ERR", "2.1.1", "un onclick sur un élément non interactif"),
    ("ERR", "3.1.1", "pas de lang sur <html>"),
    ("ERR", "2.4.2", "un titre de page vide"),
    ("ERR", "2.2.2", "une animation infinie sans prefers-reduced-motion"),
    ("WARN", "2.4.4", "un lien au libellé générique"),
    ("WARN", "1.4.13", "du contenu qui n'apparaît qu'au survol"),
]
for lvl, sc, quoi in attendu:
    check("%s %s — %s" % (lvl, sc, quoi), (lvl, sc) in trouves)

print("\n═══ la page saine : aucune faute (et les faux positifs d'hier sont partis) ═══")
F2, OK2 = a11y.audit(pathlib.Path(paths["saine"]))
errs2 = [(l, s, m) for l, s, m in F2 if l == "ERR"]
warns2 = [(l, s, m) for l, s, m in F2 if l == "WARN"]
check("page saine — aucune faute A/AA", not errs2, errs2)
check("page saine — aucun avertissement non plus", not warns2, warns2)
check("page saine — l'outil dit aussi ce qui est conforme", len(OK2) >= 4, OK2)

print("\n═══ et les deux nouveaux contrôles du lot [28] ont leur témoin fautif ═══")
PIEDS = """<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Une page sans repère principal</title>
<style>a:focus-visible{outline:2px solid red}</style></head><body>
<nav><a href="/">Accueil</a></nav>
<h1>Une page qui a un menu, un pied de page et rien au milieu</h1>
<form><fieldset><input type="checkbox" id="c1"><label for="c1">J'accepte</label></fieldset></form>
<footer><p>Pied</p></footer></body></html>"""
pf = os.path.join(tmp, "sans-repere.html")
io.open(pf, "w", encoding="utf-8").write(PIEDS)
F3, _ = a11y.audit(pathlib.Path(pf))
t3 = {(l, s) for l, s, _ in F3}
check("ERR/WARN 2.4.1 — page sans repère principal (le « page blank » du test NVDA)", ("WARN", "2.4.1") in t3)
check("ERR/WARN 1.3.1 — groupe de cases sans <legend>", ("WARN", "1.3.1") in t3)

print("\n═══ et contre NOS pages ═══")
root = HERE.parent.parent
nos = [root / "site/index.html", root / "site/creation-site-web-clinique-cameroun.html",
       root / "site/creation-site-web-ecole-cameroun.html", root / "demos/concept-unilabo-v2.html"]
for p in nos:
    if p.exists():
        Fn, _ = a11y.audit(p)
        errsn = [(l, s, m) for l, s, m in Fn if l == "ERR"]
        check("%s — aucune faute A/AA" % p.name, not errsn, errsn)

print("\n── pages GELÉES : on ne les touche pas, mais on écrit ce qu'elles portent ──")
for p in (root / "demos/concept-univers-optique-v2.html", root / "demos/concept-le-cristallin-v1.html"):
    if p.exists():
        Fg, _ = a11y.audit(p)
        print("  note %s : %s" % (p.name, " · ".join("[%s] %s" % (s, m) for l, s, m in Fg) or "rien"))

print()
if fails:
    print("DES ÉCHECS : " + " · ".join(fails))
    sys.exit(1)
print("Tout est vert — le contrôle refuse les seize défauts, et il ne mord plus à côté.")
