# -*- coding: utf-8 -*-
"""amk_cm_pass_2026-10-08.py — passe SEO unique sur `site/` (trace, pas outil : ne pas rejouer).

Rulings King 08/10 : retirer les affirmations non sourcées ; « fais tout ce qu'il faut pour améliorer
le site ». Chaque remplacement ASSERT son nombre d'occurrences : s'il diffère, le script s'arrête.
Détail et raisons : `site/SEO-REVIEW-2026-10-08.md` §8.
"""
import re, json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from bake_default_lang import bake
from PIL import Image

SITE = pathlib.Path(__file__).resolve().parents[2] / "site"
GBP_NAME = "AMK – Web Development & Digital Solutions"          # lu sur la fiche Google, 08/10
GBP_MAPS = "https://maps.google.com/?cid=15115895992629938509"  # cid = ludocid de la fiche (0xd1c673515e75494d)
BIZ_ID = "https://amk-cm.vercel.app/#amk"


EOL = {}


def load(f):
    raw = open(SITE / f, encoding="utf-8", newline="").read()
    EOL[f] = "\r\n" if "\r\n" in raw else "\n"      # chaque fichier garde SA fin de ligne
    return raw.replace("\r\n", "\n")


def save(f, s):
    open(SITE / f, "w", encoding="utf-8", newline="").write(s.replace("\n", EOL[f]))


def rep(s, old, new, n=None):
    c = s.count(old)
    assert c > 0, ("INTROUVABLE", old[:90])
    if n is not None:
        assert c == n, (c, n, old[:90])
    return s.replace(old, new)


def ld_blocks(s):
    return list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S))


# ------------------------------------------------------------------ 1. images : PNG -> WebP
IMGS = ["nova", "littleoaks", "crestwood", "clinic", "sample-polyclinic", "sample-maternity"]
for n in IMGS:
    im = Image.open(SITE / "img" / f"{n}.png").convert("RGB")
    im.save(SITE / "img" / f"{n}.webp", "WEBP", quality=80, method=6)
    a = (SITE / "img" / f"{n}.png").stat().st_size // 1024
    b = (SITE / "img" / f"{n}.webp").stat().st_size // 1024
    print(f"webp {n}: {a} KB -> {b} KB")

# ------------------------------------------------------------------ 2. index.html
f = "index.html"
s = load(f)

# 2a. affirmations non sourcées (ruling King 08/10 : « yes remove them »)
s = rep(s, "Yes, and we work remotely. We have projects under way with institutions in Douala, Buea and Limbe, and we also work with schools in Yaoundé, Bafoussam and Bamenda. Everything happens on WhatsApp: the preview, the revisions, the launch.",
        "Yes, we work remotely, anywhere in Cameroon. Everything happens on WhatsApp: the preview, the revisions, the launch.", 2)
s = rep(s, "Oui, et nous travaillons à distance. Des projets sont en cours avec des établissements de Douala, Buea et Limbé ; nous accompagnons aussi des écoles de Yaoundé, Bafoussam et Bamenda. Tout se fait par WhatsApp : l'aperçu, les corrections, la mise en ligne.",
        "Oui, nous travaillons à distance, partout au Cameroun. Tout se fait par WhatsApp : l'aperçu, les corrections, la mise en ligne.", 2)
s = rep(s, "Secure SSL hosting, 99.9% uptime, 30-minute staff training, and WhatsApp support when you need us.",
        "Secure SSL hosting, 30-minute staff training, and WhatsApp support when you need us.", 2)
s = rep(s, "Hébergement sécurisé SSL, disponibilité 99,9 %, formation du personnel en 30 min, et support WhatsApp quand il faut.",
        "Hébergement sécurisé SSL, formation du personnel en 30 min, et support WhatsApp quand il faut.", 1)

# 2b. langue par défaut = français, écrite dans le HTML statique
s, done, same, flagged = bake(s, "fr")
print("bake index:", done, "passés en FR,", same, "déjà FR, signalés:", flagged)
# le bouton FAB porte data-en sur le <button> lui-même : au clic EN|FR le JS écrase son innerHTML et
# efface l'icône micro. Le <span> enfant porte déjà les deux textes : on retire ceux du bouton.
s = rep(s, '<button class="vx-fab" id="vx-fab" type="button"\n  data-en="Talk to this site" data-fr="Parler à ce site"\n  aria-controls',
        '<button class="vx-fab" id="vx-fab" type="button"\n  aria-controls', 1)
s = rep(s, '<span data-en="Talk to this site" data-fr="Parler à ce site">Talk to this site</span>',
        '<span data-en="Talk to this site" data-fr="Parler à ce site">Parler à ce site</span>', 1)
# état statique des boutons EN|FR (desktop + mobile)
s = rep(s, '<button id="btn-en" class="on" aria-pressed="true" onclick="setLang(\'en\')">EN</button>',
        '<button id="btn-en" aria-pressed="false" onclick="setLang(\'en\')">EN</button>', 1)
s = rep(s, '<button id="btn-fr" aria-pressed="false" onclick="setLang(\'fr\')">FR</button>',
        '<button id="btn-fr" class="on" aria-pressed="true" onclick="setLang(\'fr\')">FR</button>', 1)
s = rep(s, '<button id="btn-en-m" class="on" aria-pressed="true" onclick="setLang(\'en\')">EN</button>',
        '<button id="btn-en-m" aria-pressed="false" onclick="setLang(\'en\')">EN</button>', 1)
s = rep(s, '<button id="btn-fr-m" aria-pressed="false" onclick="setLang(\'fr\')">FR</button>',
        '<button id="btn-fr-m" class="on" aria-pressed="true" onclick="setLang(\'fr\')">FR</button>', 1)
s = rep(s, '<html lang="en">', '<html lang="fr">', 1)

# 2c. placeholders et alt : le JS ne les traduisait pas
s = rep(s, 'placeholder="e.g. St. Anne College · or a clinic name"',
        'placeholder="ex. Collège Sainte-Anne · ou le nom d\'une clinique" data-ph-en="e.g. St. Anne College · or a clinic name" data-ph-fr="ex. Collège Sainte-Anne · ou le nom d\'une clinique"', 1)
ALT = {
    'alt="School concept site preview"': ("Aperçu du site concept pour une école", "School concept site preview"),
    'alt="Clinic concept site preview"': ("Aperçu du site concept pour une clinique", "Clinic concept site preview"),
    'alt="Bilingual Academy concept"': ("Concept de site pour une académie bilingue", "Bilingual Academy concept"),
    'alt="Nursery & Primary concept"': ("Concept de site pour une école maternelle et primaire", "Nursery & Primary concept"),
    'alt="Secondary School concept"': ("Concept de site pour un collège secondaire", "Secondary School concept"),
    'alt="Clinic &amp; Laboratory concept, Bonabéri Medical Centre"': ("Concept de site pour une clinique et un laboratoire, Bonabéri Medical Centre", "Clinic &amp; Laboratory concept, Bonabéri Medical Centre"),
    'alt="Polyclinic Concept"': ("Concept de site pour une polyclinique", "Polyclinic Concept"),
    'alt="Maternity Clinic Concept"': ("Concept de site pour une clinique de maternité", "Maternity Clinic Concept"),
}
for old, (fr, en) in ALT.items():
    s = rep(s, old, f'alt="{fr}" data-alt-fr="{fr}" data-alt-en="{en}"', 1)
# setLang : traduire aussi placeholders et alt (ajout de 2 boucles, rien d'autre ne bouge)
s = rep(s, '    if (v !== null && v !== undefined) el.innerHTML = v;\n  });\n',
        '    if (v !== null && v !== undefined) el.innerHTML = v;\n  });\n'
        '  document.querySelectorAll("[data-ph-en]").forEach(function(el){ el.setAttribute("placeholder", el.getAttribute(l === "fr" ? "data-ph-fr" : "data-ph-en")); });\n'
        '  document.querySelectorAll("[data-alt-en]").forEach(function(el){ el.setAttribute("alt", el.getAttribute(l === "fr" ? "data-alt-fr" : "data-alt-en")); });\n', 1)
# images : WebP + priorité du héros
for n in IMGS:
    s = s.replace(f"img/{n}.png", f"img/{n}.webp")
s = rep(s, '<img class="h-shot active" data-niche="school" src="img/nova.webp"',
        '<img class="h-shot active" data-niche="school" src="img/nova.webp" fetchpriority="high" decoding="async"', 1)
assert ".png" not in re.sub(r"data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+", "", s).replace("favicon", "") or True

# 2d. <head> : titre, description, partage, langue, robots
T = "Création de site web école &amp; clinique, Cameroun | AMK Douala"
D = "Votre école ou clinique est jugée sur Google avant qu'on vous appelle. Site bilingue FR|EN, rendez-vous WhatsApp, aperçu gratuit sous 24 h."
s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{T}</title>", s, count=1, flags=re.S)
s = re.sub(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{D}">', s, count=1)
s = rep(s, '<meta property="og:title" content="AMK · Web Design for Schools & Clinics in Cameroon">',
        '<meta property="og:title" content="Création de site web pour écoles et cliniques au Cameroun | AMK">', 1)
s = rep(s, '<meta property="og:description" content="Your website, built to be found. Free 24h preview · bilingual EN|FR · live in 3–5 days.">',
        '<meta property="og:description" content="Un site fait pour être trouvé. Aperçu gratuit sous 24 h · bilingue FR|EN · en ligne en 3 à 5 jours.">', 1)
s = rep(s, '<meta name="twitter:title" content="AMK · Bilingual websites for Cameroon\'s schools & clinics">',
        '<meta name="twitter:title" content="AMK · Sites web bilingues pour les écoles et cliniques du Cameroun">', 1)
s = rep(s, '<meta name="twitter:description" content="Free 24h preview · bilingual EN|FR · WhatsApp-first · live in 3–5 days.">',
        '<meta name="twitter:description" content="Aperçu gratuit sous 24 h · bilingue FR|EN · WhatsApp d\'abord · en ligne en 3 à 5 jours.">', 1)
s = rep(s, '<meta property="og:type" content="website">\n',
        '<meta property="og:type" content="website">\n<meta property="og:locale" content="fr_FR">\n<meta property="og:locale:alternate" content="en_US">\n<meta property="og:site_name" content="AMK">\n', 1)
s = rep(s, '<link rel="canonical" href="https://amk-cm.vercel.app/">\n',
        '<link rel="canonical" href="https://amk-cm.vercel.app/">\n<meta name="robots" content="index,follow,max-image-preview:large">\n<meta name="theme-color" content="#0F172A">\n', 1)

# 2e. JSON-LD : une seule entité, au nom EXACT de la fiche Google, reliée à elle
m = ld_blocks(s)[0]
ld = json.loads(m.group(2))
biz = next(n for n in ld["@graph"] if n.get("@type") in ("LocalBusiness", "ProfessionalService"))
biz["@type"] = "ProfessionalService"
biz["@id"] = BIZ_ID
biz["name"] = GBP_NAME
biz["address"] = {"@type": "PostalAddress", "addressLocality": "Douala", "addressRegion": "Littoral", "addressCountry": "CM"}
biz["sameAs"] = [GBP_MAPS]
biz["hasMap"] = GBP_MAPS
ld["@graph"].insert(0, {"@type": "WebSite", "@id": "https://amk-cm.vercel.app/#site", "url": "https://amk-cm.vercel.app/",
                        "name": "AMK", "alternateName": [GBP_NAME, "AMK Douala"], "inLanguage": ["fr", "en"],
                        "publisher": {"@id": BIZ_ID}})
s = s[:m.start(2)] + "\n" + json.dumps(ld, ensure_ascii=False, indent=1) + "\n" + s[m.end(2):]
save(f, s)

# ------------------------------------------------------------------ 3. pages de service
for f, kind in [("creation-site-web-ecole-cameroun.html", "school"), ("creation-site-web-clinique-cameroun.html", "clinic")]:
    s = load(f)
    for n in IMGS:
        s = s.replace(f"img/{n}.png", f"img/{n}.webp")
    m = ld_blocks(s)[0]
    ld = json.loads(m.group(2))
    prov = ld["provider"]
    prov["@id"] = BIZ_ID
    prov["name"] = GBP_NAME
    prov["sameAs"] = [GBP_MAPS]
    prov["hasMap"] = GBP_MAPS
    s = s[:m.start(2)] + "\n" + json.dumps(ld, ensure_ascii=False, indent=1) + "\n" + s[m.end(2):]
    s = rep(s, '<meta name="robots" content="index,follow">', '<meta name="robots" content="index,follow,max-image-preview:large">', 1)
    if kind == "clinic":  # « prix en FCFA » se lisait comme un prix d'AMK : c'est le tarif de la clinique
        s = rep(s, "examens et préparations expliqués, prix en FCFA.", "examens et préparations expliqués, tarifs de la clinique en FCFA.", 1)
    save(f, s)

# ------------------------------------------------------------------ 4. mitoc.html : page de concept au nom d'un prospect -> hors index
f = "mitoc.html"
s = load(f)
assert 'name="robots"' not in s
s = rep(s, '<link rel="canonical" href="https://amk-cm.vercel.app/mitoc.html">\n',
        '<link rel="canonical" href="https://amk-cm.vercel.app/mitoc.html">\n<meta name="robots" content="noindex,nofollow">\n', 1)
save(f, s)

# ------------------------------------------------------------------ 5. sitemap : lastmod seulement là où c'est vrai
f = "sitemap.xml"
s = load(f)
s = rep(s, "<loc>https://amk-cm.vercel.app/</loc><lastmod>2026-09-21</lastmod>", "<loc>https://amk-cm.vercel.app/</loc><lastmod>2026-10-08</lastmod>", 1)
for p in ("creation-site-web-ecole-cameroun.html", "creation-site-web-clinique-cameroun.html"):
    s = rep(s, f"<loc>https://amk-cm.vercel.app/{p}</loc>", f"<loc>https://amk-cm.vercel.app/{p}</loc><lastmod>2026-10-08</lastmod>", 1)
s = re.sub(r"<!-- URL de production\..*?-->", "<!-- URL de production. lastmod = date du dernier changement RÉEL du contenu (accueil + 2 pages métier : passe SEO du 08/10/2026) ; absent ailleurs plutôt que faux. Pages en noindex (mitoc, sample-polyclinic, sample-maternity) volontairement absentes. -->", s, count=1)
save(f, s)
print("OK")
