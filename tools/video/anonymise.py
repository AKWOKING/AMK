#!/usr/bin/env python3
"""AMK — anonymisation d'une page concept en page de DÉMONSTRATION publiable.

Pourquoi : la règle de King (17 Sep) interdit tout nom réel de clinique/école dans un
contenu public sans autorisation écrite — mais nos concepts sont aussi nos meilleures
maquettes. Ce script produit une copie **fictive** (marque, numéros, adresse unique →
fiction MboaCare + numéro de démonstration), **étiquetée comme fiction**, puis la passe
au portique HTML (`tools/qa/audit_html.py`) : 0 anomalie ou échec.

Usage :
    python3 tools/video/anonymise.py --concept jempo --out hosting/previews/demo/jempo-demo.html
    python3 tools/video/anonymise.py --all          # produit la bibliothèque complète
"""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEMO_WA = "237600000000"          # numéro de démonstration : jamais un vrai prospect
DEMO_WA_HUMAN = "600 00 00 00"

# slug → (fichier source, [(motif, remplacement), …], marque fictive affichée)
CONCEPTS = {
    "jempo": ("demos/concept-jempo-v1.html", [
        (r"J&amp;E Memorial Polyclinic \(JEMPO\)", "MboaCare Polyclinic (DEMO)"),
        (r"J&E Memorial Polyclinic \(JEMPO\)", "MboaCare Polyclinic (DEMO)"),
        (r"J&amp;E Memorial Polyclinic", "MboaCare Polyclinic"),
        (r"J&E Memorial Polyclinic", "MboaCare Polyclinic"),
        (r"J&amp;E MEMORIAL POLYCLINIC", "MBOACARE POLYCLINIC"),
        (r"J&E MEMORIAL POLYCLINIC", "MBOACARE POLYCLINIC"),
        (r"J&amp;E", "MboaCare"), (r"J&E", "MboaCare"),
        (r"Polyclinique\s+MboaCare", "MboaCare Polyclinic"), (r"\bPolyclinique\b", "Polyclinic"),
        (r"Vallée Bessengue", "Bonabéri"),
        (r"Dr Marcus Youda", "Dr A. Mbarga"), (r"Dr Angelique Njeumen", "Dr B. Nkoa"),
        (r"Dr Paul Djomaleu", "Dr C. Etoundi"), (r"Dr Humphry Neng", "Dr D. Fotso"),
        (r"J&amp;E Memorial Polyclinic", "MboaCare Polyclinic"),
        (r"J&amp;E MEMORIAL", "MBOACARE POLYCLINIC"),
        (r"\bJEMPO\b", "MboaCare"),
        (r"Vallée Bessengue", "Bonabéri, Douala"),
        (r"face à l'h[oô]tel\s*LEWAT", "à 200 m du marché"),
        (r"[Ff]ace h[oô]tel\s*LEWAT", "à 200 m du marché"), (r"LEWAT", "marché"),
        (r"696\s?71\s?06\s?99", DEMO_WA_HUMAN), (r"670\s?85\s?85\s?42", DEMO_WA_HUMAN),
        (r"233\s?47\s?87\s?69", DEMO_WA_HUMAN), (DEMO_WA, DEMO_WA),
        (r"237696710699", DEMO_WA), (r"237670858542", DEMO_WA), (r"237233478769", DEMO_WA),
    ]),
    "labethanie": ("demos/concept-labethanie-v1.html", [
        (r"Clinique La Béthanie", "Clinique MboaCare (DÉMO)"),
        (r"La Béthanie", "MboaCare"), (r"la Béthanie", "MboaCare"),
        (r"Béthanie", "MboaCare"),
        (r"Rue Mpondo", "Rue des Palmiers"), (r"Mpondo", "des Palmiers"),
        (r"Dr Richard Petieu", "Dr E. Owona"), (r"Richard PETIEU", "E. Owona"),
        (r"677\s?76\s?07\s?82", DEMO_WA_HUMAN), (r"683\s?76\s?74\s?13", DEMO_WA_HUMAN),
        (r"237677760782", DEMO_WA), (r"237683767413", DEMO_WA),
    ]),
    "oracare": ("demos/concept-oracare-v3.html", [
        (r"OraCare Dental Clinic", "MboaCare Dental (DEMO)"),
        (r"OraCare", "MboaCare"),
        (r"snkafuarnold11@gmail\.com", "contact@mboacare-demo.example"),
        (r"https?://(?:www\.)?facebook\.com/p/Oracare237-100075164312902", "#"),
        (r"Oracare237-100075164312902", "mboacare-demo"),
        (r"Molyko, Buea", "Bonabéri, Douala"), (r"\bMolyko\b", "Bonabéri"),
        (r"672\s?52\s?66\s?86", DEMO_WA_HUMAN), (r"237672526686", DEMO_WA),
    ]),
    # NB : yaks portait 2 anomalies de contraste pré-existantes (concept gelé par King — on ne
    # retouche pas le fichier livré) ; elles sont corrigées **dans la copie de démo** ci-dessous.
    "yaks": ("demos/concept-yaks-v1.html", [
        (r"Cabinet Dentaire YAKS", "Cabinet Dentaire MboaCare (DÉMO)"),
        (r"\bYAKS\b", "MboaCare"),
        (r"Logbessou", "Bonamoussadi"),
        (r"cabinetdentaireyaks@gmail\.com", "contact@mboacare-demo.example"),
        (r"cabinetdentaireyaks\.com", "mboacare-demo.example"),
        (r"Dr Lekane épse Ntoweng Lolita", "Dr F. Tchoumi"),
        (r"Dr Lekane Lolita", "Dr F. Tchoumi"), (r"Dr Lekane", "Dr F. Tchoumi"),
        (r"Lekane épse Ntoweng Lolita", "F. Tchoumi"), (r"Ntoweng", "Tchoumi"),
        (r"672\s?70\s?20\s?78", DEMO_WA_HUMAN), (r"6\s?72\s?70\s?20\s?78", DEMO_WA_HUMAN),
        (r"237672702078", DEMO_WA),
        (r"#5C7565", "#597162"),
        (r"\.book \.eyebrow\{color:rgba\(240,250,241,\.6\)\}",
         ".book .eyebrow{color:rgba(240,250,241,.88)}"),
    ]),
    "opticien": ("demos/concept-opticien-lopticien.html", [
        (r"L'Opticien[^<\"']{0,25}", "MboaCare Optique (DÉMO)"),
        (r"670\s?27\s?60\s?65", DEMO_WA_HUMAN), (r"237670276065", DEMO_WA),
    ]),
}

BANNER = ('<div id="amk-demo-banner" style="position:sticky;top:0;z-index:99999;'
          'background:#101838;color:#FFFFFF;font:600 10px/1.3 system-ui,sans-serif;'
          'letter-spacing:.2px;text-align:center;padding:4px 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'
          'DÉMO AMK · page fictive « MboaCare » — démonstration, pas un vrai prestataire</div>')


def anonymise(slug, out_path, keep_banner=True):
    src_rel, rules = CONCEPTS[slug]
    html = (ROOT / src_rel).read_text(encoding="utf-8")
    before = html
    applied = []
    for pat, rep in rules:
        new = re.sub(pat, rep, html)
        if new != html:
            applied.append(pat)
            html = new
    if not applied:
        print(f"  ⚠ {slug} : aucune substitution appliquée — vérifier les motifs")

    # Normalisateur GÉNÉRIQUE : tout numéro camerounais restant (tous formats) → numéro de démo,
    # en conservant le format d'origine pour ne pas casser la mise en page.
    def demo_phone(m):
        raw = m.group(0)
        suffix = DEMO_WA[-9:]          # ← forme à partir du numéro de DÉMO (bug corrigé)
        pretty = f"{suffix[0]} {suffix[1:3]} {suffix[3:5]} {suffix[5:7]} {suffix[7:9]}"
        compact = "237" + suffix
        if "+237" in raw and " " in raw:
            return "+237 " + pretty
        if raw.strip().startswith("+"):
            return "+237" + suffix
        if "237" in raw and " " not in raw:
            return compact
        return pretty if " " in raw else suffix

    html = re.sub(r"\+?237[\s\-]?\d[\d\s\-]{7,15}|\b6\d{2}[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}\b", demo_phone, html)
    # tout identifiant de page Facebook reste une identité : on neutralise le lien
    html = re.sub(r'(https?://[^"\']*facebook\.com/p/[^"\']*)', "#", html)
    html = re.sub(r"https?://(?:www\.)?facebook\.com/[^\"']*", "https://facebook.com/mboacare-demo", html)

    # PASSE FINALE d'identités : insensible à la casse et aux entités HTML
    # (une marque peut survivre en minuscules, en majuscules ou encodée — ex. « B&eacute;thanie »).
    IDENTITY = {
        "j&amp;e": "MboaCare", "j&e": "MboaCare", "jempo": "MboaCare",
        "b&eacute;thanie": "MboaCare", "béthanie": "MboaCare", "bethanie": "MboaCare",
        "oracare": "MboaCare", "yaks": "MboaCare", "lew (at)": "marché",
        "lewat": "marché", "mpondo": "des Palmiers", "bessengue": "Bonabéri",
        "molyko": "Bonabéri", "djuinne": "Tchoumi", "lekane": "Tchoumi",
        "ntoweng": "Tchoumi", "youda": "Mbarga", "njeumen": "Nkoa",
        "djomaleu": "Etoundi", "neng": "Fotso", "petieu": "Owona",
        "sandrine": "Marie", "snkafuarnold": "contact",
        "cabinetdentaireyaks": "mboacare-demo", "100075164312902": "mboacare-demo",
    }
    for bad, good in IDENTITY.items():
        html = re.sub(re.escape(bad), good, html, flags=re.I)

    # étiquette de fiction + noindex + titre préfixé
    html = re.sub(r"<title>", "<title>[DÉMO] ", html, count=1)
    if 'name="robots"' not in html:
        html = re.sub(r"(</title>)", r"\1\n<meta name=\"robots\" content=\"noindex, nofollow\">", html, count=1)
    if keep_banner and "amk-demo-banner" not in html:
        m = re.search(r"<body[^>]*>", html, re.I)
        if m:
            html = html[:m.end()] + "\n" + BANNER + html[m.end():]
        else:
            html = BANNER + html

    out = ROOT / out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    # Contrôle FORT : on ne vérifie pas nos propres motifs (béquille), on cherche
    # dans la sortie (1) tout numéro de téléphone, (2) une liste noire d'identités réelles.
    leak = []
    for m in re.finditer(r"\+?237[\s\-]?[\d\s\-]{6,16}|\b6\d{2}[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}\b", html):
        digits = re.sub(r"\D", "", m.group(0))
        if DEMO_WA not in digits and not digits.endswith(DEMO_WA):
            leak.append("TÉL:" + m.group(0).strip())
    BLACKLIST = ["JEMPO", "J&amp;E", "J&E", "Béthanie", "Bethanie", "OraCare", "Oracare",
                 "YAKS", "LEWAT", "Mpondo", "Bessengue", "Molyko", "Djuinne", "Lekane",
                 "Youda", "Njeumen", "Djomaleu", "Neng", "Petieu", "Ntoweng", "Sandrine",
                 "snkafuarnold", "cabinetdentaireyaks", "100075164312902"]
    for word in BLACKLIST:
        if word.lower() in html.lower():
            leak.append("NOM:" + word)
    leak = sorted(set(leak))
    print(f"  {slug}: {len(applied)}/{len(rules)} règles · {round(len(html)/1024)} KB · fuites: {len(leak)} {leak[:4]}")
    return out, len(leak)


def audit(path):
    r = subprocess.run([sys.executable, str(ROOT / "tools/qa/audit_html.py"), str(path)],
                       capture_output=True, text=True)
    tail = (r.stdout or "").strip().splitlines()[-1] if r.stdout else ""
    ok = r.returncode == 0 and "0 confirmed" in (r.stdout or "")
    print(f"  audit {path.name}: {'✓ 0 anomalie' if ok else '✗ ' + tail}")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept")
    ap.add_argument("--out")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-audit", action="store_true")
    a = ap.parse_args()

    jobs = list(CONCEPTS) if a.all else [a.concept]
    if not a.all and not a.out:
        sys.exit("--out obligatoire (ou --all)")
    failures = 0
    for slug in jobs:
        out = a.out if (not a.all and a.out) else f"hosting/previews/demo/{slug}-demo.html"
        print(f"▸ {slug} → {out}")
        path, leaks = anonymise(slug, out)
        if leaks:
            print("  ✗ identité résiduelle détectée — à corriger"); failures += 1
        if not a.no_audit and not audit(path):
            failures += 1
    sys.exit(1 if failures else 0)
