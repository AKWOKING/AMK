# -*- coding: utf-8 -*-
"""Rewrite Sasse concept (sjc-sasse-v2.html) with verified boarding facts.
EN strings appear twice (data-en attr + visible text); FR strings once (data-fr attr only).
Every replacement asserts its expected occurrence count before applying."""
import sys

PATH = "sjc-sasse-v2.html"
html = open(PATH, encoding="utf-8").read()

REPL = [
(1,
 '<span class="kicker" data-en="Buea · Diocese of Buea · Since 1939" data-fr="Buea · Diocèse de Buea · Depuis 1939">Buea · Diocese of Buea · Since 1939</span>',
 '<span class="kicker" data-en="Buea · At the foot of Mount Fako · Since 1939" data-fr="Buea · Au pied du mont Fako · Depuis 1939">Buea · At the foot of Mount Fako · Since 1939</span>'),

(1,
 '<span data-en="Excellence in education" data-fr="L\'excellence dans l\'éducation">Excellence in education</span> <em data-en="since 1939." data-fr="depuis 1939.">since 1939.</em>',
 '<span data-en="Cameroon\'s oldest" data-fr="Le plus ancien">Cameroon\'s oldest</span> <em data-en="secondary school." data-fr="collège du Cameroun.">secondary school.</em>'),

(1,
 '<p class="sub" data-en="St. Joseph\'s College, Sasse is a Catholic institution in Buea where academic rigour, Christian values and bilingual education have shaped leaders for nearly nine decades." data-fr="Le Collège Saint-Joseph de Sasse est une institution catholique à Buea où rigueur académique, valeurs chrétiennes et éducation bilingue forment des leaders depuis près de neuf décennies.">St. Joseph\'s College, Sasse is a Catholic institution in Buea where academic rigour, Christian values and bilingual education have shaped leaders for nearly nine decades.</p>',
 '<p class="sub" data-en="A Catholic boarding college at the foot of Mount Fako — the first college in Cameroon\'s English-speaking region, founded by the Mill Hill in 1939, and the oldest secondary school in the country." data-fr="Un collège catholique en pensionnat au pied du mont Fako — le premier collège de la région anglophone du Cameroun, fondé par les Mill Hill en 1939, et le plus ancien collège secondaire du pays.">A Catholic boarding college at the foot of Mount Fako — the first college in Cameroon\'s English-speaking region, founded by the Mill Hill in 1939, and the oldest secondary school in the country.</p>\n       <p style="font-style:italic;color:#C9A227;margin-top:10px;font-size:14.5px" data-en="&ldquo;O Sasse by the Mountain · O Sasse by the Sea&rdquo; — the college anthem" data-fr="&laquo; Ô Sasse près de la montagne · Ô Sasse près de la mer &raquo; — l\'hymne du collège">&ldquo;O Sasse by the Mountain · O Sasse by the Sea&rdquo; — the college anthem</p>'),

(1,
 '<span data-en="Mill Hill tradition · Diocese of Buea" data-fr="Tradition Mill Hill · Diocèse de Buea">Mill Hill tradition · Diocese of Buea</span>',
 '<span data-en="100% GCE pass · 2025 (O &amp; A-Level)" data-fr="100% de réussite GCE · 2025 (O &amp; A-Level)">100% GCE pass · 2025 (O &amp; A-Level)</span>'),

(1,
 '<h3 data-en="Leadership & Co-curricular" data-fr="Leadership & activités">Leadership & Co-curricular</h3>',
 '<h3 data-en="Boarding &amp; Leadership" data-fr="Pensionnat &amp; Leadership">Boarding &amp; Leadership</h3>'),

(1,
 '<p data-en="Debate, sport, service and prefectship — the habits of leaders, practised every day." data-fr="Débat, sport, service et fonctions de direction — les habitudes des leaders, pratiquées chaque jour.">Debate, sport, service and prefectship — the habits of leaders, practised every day.</p>',
 '<p data-en="Eight dormitories, a 1,200-seat chapel, house system and prefectship — the habits of leaders, lived every day on campus." data-fr="Huit dortoirs, une chapelle de 1 200 places, le système de maisons et les fonctions de préfet — les habitudes des leaders, vécues chaque jour sur le campus.">Eight dormitories, a 1,200-seat chapel, house system and prefectship — the habits of leaders, lived every day on campus.</p>'),

(2,
 'The discipline and warmth of the place showed from the first day. My son came home proud.',
 'From his first week in the dorms, the discipline and warmth showed. He comes home for break a different boy — and a proud one.'),
(1,
 'La discipline et la chaleur du lieu se voyaient dès le premier jour. Mon fils est rentré fier.',
 'Dès sa première semaine au dortoir, on voyait la discipline et la chaleur du lieu. Il rentre pour les vacances un autre garçon — et un fier.'),

(2,
 'The O-Level results speak for themselves — but what parents feel is the attention each boy gets.',
 'The O-Level results speak for themselves — but what parents feel is the attention each boy gets, in class and in the dorms.'),
(1,
 'Les résultats du O-Level parlent d\'eux-mêmes — mais ce que les parents ressentent, c\'est l\'attention portée à chaque garçon.',
 'Les résultats du O-Level parlent d\'eux-mêmes — mais ce que les parents ressentent, c\'est l\'attention portée à chaque garçon, en classe comme au dortoir.'),

(2,
 'Walk the campus, sit in a class, meet the teachers and the director. The best way to know a school.',
 'Walk the classrooms, labs, dormitories and the 1,200-seat chapel; sit in a class; meet the teachers and the director. The best way to know a school.'),
(1,
 'Parcourez le campus, assistez à un cours, rencontrez les enseignants et le directeur. La meilleure façon de connaître une école.',
 'Parcourez les classes, les laboratoires, les dortoirs et la chapelle de 1 200 places ; assistez à un cours ; rencontrez les enseignants et le directeur. La meilleure façon de connaître une école.'),

(2, 'Is transport available from Buea town?', 'Is Sasse a boarding school?'),
(1, 'Un transport est-il disponible depuis Buea ?', 'Sasse est-il un pensionnat ?'),
(2,
 'Transport information is available at the admissions office — routes and pickup points are confirmed with families at enrollment.',
 'Yes — Sasse is a boarding college. Eight dormitories house boys from across Cameroon, and families in Buea may also enrol day students. The admissions office explains both options, their fees and the entry dates.'),
(1,
 'Les informations sur le transport sont disponibles au bureau des admissions — les trajets et points de ramassage sont confirmés avec les familles à l\'inscription.',
 'Oui — Sasse est un collège en pensionnat. Huit dortoirs accueillent des garçons venus de tout le Cameroun, et les familles de Buea peuvent aussi inscrire des élèves de jour. Le bureau des admissions explique les deux options, leurs frais et les dates d\'entrée.'),

(2,
 '<b>The campus welcomes families</b> every school day — sit in a class before you decide.',
 '<b>The campus welcomes visiting families</b> — walk the dorms and the chapel, sit in a class before you decide.'),
(1,
 '<b>Le campus accueille les familles</b> chaque jour de classe — assistez à un cours avant de décider.',
 '<b>Le campus accueille les familles en visite</b> — parcourez les dortoirs et la chapelle, assistez à un cours avant de décider.'),
(2, 'admissions, fees, transport, everything.', 'admissions, fees, boarding, everything.'),
(1, 'admissions, frais, transport, tout.', 'admissions, frais, pensionnat, tout.'),

(1,
 '<div class="yr">87</div><p data-en="Years of forming leaders across Cameroon" data-fr="Années à former des leaders à travers le Cameroun">Years of forming leaders across Cameroon</p>',
 '<div class="yr">82</div><p data-en="GCE candidates passed in 2025 — 37 O-Level + 45 A-Level" data-fr="Candidats GCE reçus en 2025 — 37 O-Level + 45 A-Level">GCE candidates passed in 2025 — 37 O-Level + 45 A-Level</p>'),

(1,
 '"slogan": "Excellence in education since 1939"',
 '"slogan": "Cameroon\'s oldest secondary school — a Catholic boarding college since 1939"'),
(1,
 '"award": "Best School in West Africa 2012; Best School in Cameroon 2013"',
 '"award": "Best School in West Africa 2012; Best School in Cameroon 2013; 100% GCE pass 2025 (O & A-Level)"'),

(1,
 "<title>St. Joseph's College Sasse | Best School in West Africa 2012</title>",
 "<title>St. Joseph's College Sasse | Cameroon's Oldest Secondary School · Catholic Boarding College</title>"),

(1,
 '<meta name="description" content="Catholic bilingual college in Buea since 1939. Best School in West Africa 2012 & Cameroon 2013. GCE O-Level & A-Level, faith, character. Call admissions."',
 '<meta name="description" content="St. Joseph\'s College Sasse — Cameroon\'s oldest secondary school (1939). Catholic boarding college at the foot of Mount Fako. 100% GCE pass 2025. Admissions open 2026/2027."'),
]

errors = []
for i, (n, old, new) in enumerate(REPL, 1):
    c = html.count(old)
    if c != n:
        errors.append(f"[{i}] expected {n}, found {c}: {old[:70]}...")
    else:
        html = html.replace(old, new)

if errors:
    print("ABORTED — no file written:")
    for e in errors:
        print(" ", e)
    sys.exit(1)

import re
en = len(re.findall(r'data-en="', html))
fr = len(re.findall(r'data-fr="', html))
open(PATH, "w", encoding="utf-8").write(html)
print(f"OK — all {len(REPL)} edits applied. pairs: {en}/{fr}")
print("remaining 'transport' occurrences:", html.lower().count("transport"))
print("boarding/pensionnat mentions:", html.lower().count("boarding") + html.lower().count("pensionnat"))
