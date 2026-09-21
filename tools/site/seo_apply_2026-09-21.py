#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMK — applique les leçons SEO du 21/09/2026 au site `site/index.html`.

Source des règles : 3 vidéos analysées par King (voir `AMK-DESIGN-SKILLS.md` §22) :
  · Surfer Academy — « How to Rank #1 in Google in 2026: The 3-Step SEO Playbook »
  · Portable Entrepreneur — « Rank #1 in Google Business Profile in 2026 »
  · Steve Hunsaker — « How to Optimize Your Google Business Profile »

**Ce que la recherche concurrentielle a montré (21/09) :** les agences camerounaises
(FeliSitePro, VENEGRE, Jainli, ECS) ciblent **le français** — « création site web cameroun »,
« agence web douala » — et **notre page était 100 % anglaise**. Notre NAP était déjà exact
(facteur #15 satisfait), mais nos titres ne portaient aucun mot-clé du marché.

Idempotent : garde `<!-- AMK:SEO-2026-09-21 -->`.
"""
import pathlib
import re
import sys

P = pathlib.Path("site/index.html")
GUARD = "<!-- AMK:SEO-2026-09-21 -->"


def main() -> int:
    t = P.read_text(encoding="utf-8")
    if GUARD in t:
        print("✓ déjà appliqué — rien à faire")
        return 0
    before = t

    # ── 1 · TITLE : le mot-clé du marché, avant l'accroche ──────────────────────
    old_title = "<title>AMK – Web Design for Schools & Clinics in Cameroon | Free 24h Preview</title>"
    new_title = ("<title>Création de site web pour écoles & cliniques au Cameroun | "
                 "AMK – Douala · Yaoundé · Buea · Limbé</title>")
    assert old_title in t, "title introuvable"
    t = t.replace(old_title, new_title, 1)

    # ── 2 · DESCRIPTION : une raison de cliquer, dans les deux langues ──────────
    old_desc = ('<meta name="description" content="Modern, bilingual (EN|FR), mobile-first websites '
                'for private schools & clinics in Cameroon. Free 24h preview, live in 3–5 days. '
                'Douala · Yaoundé · Buea · Limbe.">')
    new_desc = ('<meta name="description" content="Création de sites web bilingues FR|EN pour écoles privées, '
                'cliniques et laboratoires au Cameroun — Douala, Yaoundé, Buea, Limbé. Prise de rendez-vous sur '
                'WhatsApp, référencement local, aperçu gratuit sous 24 h, en ligne en 3 à 5 jours. '
                'Bilingual websites for schools & clinics in Cameroon.">')
    assert old_desc in t, "description introuvable"
    t = t.replace(old_desc, new_desc, 1)

    # ── 3 · UNE SEULE H1, PORTEUSE DU MOT-CLÉ ; les accroches passent en H2 ────
    #    Avant : DEUX <h1> (une par panneau école/clinique) sans aucun mot-clé.
    #    Après : UNE <h1> avec le terme que le marché tape, et les deux accroches
    #    fortes deviennent des <h2> — elles gardent leur place, sans diluer la H1.
    old_h1 = ('          <h1><span data-en="Your school is being" data-fr="Votre école est">Your school is being</span> '
              '<em data-en="judged on Google" data-fr="jugée sur Google">judged on Google</em> '
              '<span data-en="— before parents call." data-fr="— avant que les parents n\'appellent.">— before parents call.</span></h1>')
    new_h2_school = ('          <h2 class="punch"><span data-en="Your school is being" data-fr="Votre école est">Your school is being</span> '
                     '<em data-en="judged on Google" data-fr="jugée sur Google">judged on Google</em> '
                     '<span data-en="— before parents call." data-fr="— avant que les parents n\'appellent.">— before parents call.</span></h2>')
    assert old_h1 in t, "h1 école introuvable"
    t = t.replace(old_h1, new_h2_school, 1)

    # la H1 unique, insérée juste après le kicker (donc visible en premier, avant le switch)
    kicker_end = ('<span class="kicker" data-en="Web design — schools & clinics · Cameroon" '
                  'data-fr="Développement web — écoles & cliniques · Cameroun">'
                  'Web design — schools & clinics · Cameroon</span>')
    assert kicker_end in t, "kicker introuvable"
    h1 = (kicker_end + "\n      " + GUARD +
          '\n      <h1 class="seo-h1">'
          '<span data-en="Website design for schools and clinics in Cameroon" '
          'data-fr="Création de sites web pour écoles et cliniques au Cameroun">'
          'Création de sites web pour écoles et cliniques au Cameroun</span></h1>')
    t = t.replace(kicker_end, h1, 1)

    # la H1 clinique devient H2 (elle était la 2e <h1>)
    t = re.sub(r"<h1><span data-en=\"Your next patient is\"", '<h2 class="punch"><span data-en="Your next patient is"', t, count=1)
    t = re.sub(r"data-fr=\"— pendant qu'ils cherchent déjà\.\">— and they're searching right now\.</span></h1>",
               'data-fr="— pendant qu\'ils cherchent déjà.">— and they\'re searching right now.</span></h2>', t, count=1)

    # style de la H1 (lisible, pas écrasante : c'est la phrase-clé, pas l'accroche)
    t = t.replace("/* reveal */", """/* AMK:SEO-2026-09-21 — H1 porteuse du mot-clé (règle §22, facteur « mots-clés en H1 ») */
.seo-h1{font-size:clamp(1.05rem,2.6vw,1.45rem);font-weight:600;color:#fff;
  letter-spacing:-.01em;margin:0 0 14px;max-width:34em;line-height:1.35}
h2.punch{margin:0 0 10px}
h2.punch em{font-style:normal;color:#FFC24B}

/* reveal */""", 1)

    P.write_text(t, encoding="utf-8")
    print(f"✓ title, description et H1 appliqués ({len(t)-len(before):+d} caractères)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
