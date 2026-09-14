# AMK — Deep-Dive Research (2026-09-12)
**Method:** every send-list school re-verified against live sources, 12 Sep 2026. Facts below are quoted from cited sources; anything still unverified is marked **VERIFY**.

---

## 1 · SJC SASSE (Buea) — the concept school
**Identity:** St. Joseph's College, Sasse ("Sasse College") — Catholic, **all-boys boarding college** (Forms 1–7, O & A-Level).

**Verified facts**
- **Cameroon's oldest secondary school**; first college in the English-speaking region — opened **1 Feb 1939** by Mill Hill (Society of the Holy Apostles), Diocese of Buea. [sobadallas.org/our-alma-mater; MMI News]
- **Boarding: 8 dormitories** (started as 2 dorms for 75 boys); enrolment **800+**. At the foot of **Mount Fako** (tallest mountain in W. Africa); **1,200-seat chapel**; 3 science labs (chem/phys/bio) + computer lab + library. [sobadallas]
- **2025 GCE: 100% pass — 37/37 O-Level (lowest 8 papers), 45/45 A-Level (lowest 3 papers).** [MMI News, Aug 2025]
- Awards: Best School in West Africa **2012**; Best School in Cameroon **2013** (diocesan page); **"Best College in Cameroon" 2014** — Fondation Terre d'Accueil. [sobadallas]
- Alumni = **Sasse Old Boys (SOBANS)**; chapters incl. SOBA America; "leaders in all walks of life — politics, health, clergy, engineering, legal, accounting". [sobadallas]
- Their own TikTok **@saintjosephcollegesasse** ("SJC – The Republic") self-describes: *"Best boarding school in Cameroon · Oldest school in Cameroon · Catholic colleges · Single sex"*. [TikTok]
- Anthem: *"O Sasse by the Mountain! O Sasse by the Sea!"* · College song: *"In the hollow of his hand"* (St. Joseph). [sobadallas]
- Suffered attacks in early Anglophone-crisis years; strong bounce-back (the 2025 100%). **Conversation context only — do NOT put on the website.** [MMI News]
- Contacts: **677 195 500** (admissions mobile — NOT on WhatsApp, per King) · 233 322 113 (landline) · P.O. Box 44, Sasse, Buea · email sajoscol@gmail.com

**Web presence (checked 12 Sep):** no school-owned site (social = TikTok). Old diocesan listing (cesbueadiocese.org/sajocol — the page with the testimonials) is **down**; diocese's new site has an empty Education section (colleges gallery returns 500).

**Impact:** `demos/sjc-sasse-v2.html` rewritten 12 Sep — boarding, all-boys, oldest secondary school, 100% 2025 GCE, 8 dorms, 1,200-seat chapel, anthem tagline, "Is Sasse a boarding school?" FAQ, boarding-framed parent quotes. 123/123 EN|FR pairs.
**Brand (King-verified 12 Sep):** school colors = **blue / black / white** (uniform: blue vest, white shirt, black trousers — photo from their alumni chapel service). Concept re-skinned: navy #0F2456 hero/footer, royal #2E4E9E CTAs/accents, white; demo crest v2 = royal shield, black outline, white cross + book (placeholder, in their colors). Real chapel photo embedded base64 in hero (file self-contained, 373KB).
**Still placeholders before send:** crest, photos, class sizes (18:1 / 20:1 / 16:1 are demo values), quotes, and the 2012/2013/2014 award citations (diocesan page down — confirm with school).

---

## 2 · SAHISCOL (Limbe)
**Identity:** Saint Ann's High School Limbe (site title) / Saint Ann Girls College (diocesan listing) — New Town, Limbe; Diocese of Buea. **VERIFY at talk:** girls-only vs mixed (diocese says girls; site copy says "every student").

**Verified facts**
- **sahiscol.org is LIVE** — but it's an unedited "Schola School" template: placeholder staff names (*"Mr. John Smith, Head of Mathematics", "Ms. Emily Johnson, Discipline Mistress", "Mrs. Sarah Thompson"*), generic lorem copy, "00+" counters. Sections: **Commercial (Marketing, Accounting) + Grammar (Arts & Sciences)**. Hours 7:30–15:30, Sun closed.
- Contacts: **233 322 551** (landline, matches pack) · info@sahiscol.org · diocesan line +237 334 745 678 · sahiscol@gmail.com
- Old diocesan page (cesbuea.org/sahiscol, 2016, now down): principal's merit culture — *"no child left behind… but no room for mediocrity… the cream of students with 15+ average and passed in all papers usually have a special outing with the academic deans."*
- Boarding: **unknown** → ask at kickoff.

**Premise check:** old "site broken (502)" is **stale** — site is live but low quality. Message rewritten around the placeholder-names angle (proves we actually looked).
**⚠ 12 Sep, late:** sahiscol.org returned **404 from the sandbox** (LiteSpeed) while search index + fetcher still show the template content fresh — possibly IP/UA blocking, or the site is flaky. **King to verify from phone before sending; the pack carries a dead-site variant of message 2.**
**Concept (12 Sep):** `demos/concept-sahiscol-v1.html` — plum #4A2050 / gold #C9962E / cream, **EN default**, 122/122 pairs. Their own tagline as H1 ("Beyond the classroom, talents are unleashed."), the principal's verified "no room for mediocrity" line as the standard, Dean's-Desk culture card, 2-streams tabs, Mon–Sat hours, landline 233 322 551 everywhere. **GENDER-NEUTRAL wording ("Catholic school")** — if they're still girls-only, it still reads fine; if mixed, nothing to fix. **Form WA_NUM = AMK demo number** (school's WhatsApp unknown) — swap at kickoff. No photo (their site unreachable from sandbox) — placeholder frame captioned "your 10–15 photos".

---

## 3 · NHICHS (Limbe)
**Identity:** **New Horizon International Comprehensive High School** — private, created **2004** (started as primary), Limbe.

**Verified facts (their own site nhiss.org)**
- Pre-nursery → senior secondary. GCE center numbers for **Grammar + Commercial** streams.
- **NO boarding** — FAQ: *"Do you have a boarding section? Unfortunately we don't."* (concept must stay day-school framed)
- **100% Common Entrance** (primary) — stated twice on their site; GCE O & A-Level: "minimum 80%" / ">75%" (their own numbers conflict — use "100% Common Entrance" + "strong GCE pass rate", or quote with the school)
- **30+ scholarships granted every year**; 5,000+ graduates; 20+ learning pathways; 19+ years
- **Inspired by the principles of the Bahá'í Faith**; weekly multi-faith devotions; **Junior Youth Program** (JYP)
- **New technical department launching** — engineering, ICT, industrial sciences, entrepreneurship ("Building the Future of Technical Education in Limbe")
- Equipped science labs; music club
- inovedu listing: 4.4/5 (40 reviews); tuition 192,823–274,372 FCFA/yr (reference only — never quote fees in outreach)

**Premise check:** nhichs.org **still parked** (Namecheap auction page) ✓ · nhiss.org live but **no results, no admissions, no fees pages** ✓.
**Message:** keep expired-domain angle; add technical-department hook + full name.

---

## 4 · COLLÈGE DE LA RETRAITE (Yaoundé)
**Identity:** Collège Catholique Bilingue La Retraite — Archdiocese of Yaoundé; "établissement privé polyvalent, confessionnel catholique"; Ave Konrad Adenauer, B.P. 159 Yaoundé; (+237) 2 43 58 86 54.

**Verified facts**
- Founded **1950** by the Sisters of the Holy Spirit as *Collège du Saint-Esprit* (girls only); **1960**: run by the **Sœurs de la Retraite** → renamed; now co-educational (*"deux sexes, de toute obédience religieuse, à condition qu'elles acceptent et respectent sa catholicité"*). [laretraitecatholicbilingualcollege.org]
- Motto: **"Régina Mundi Ora Pro Nobis"** + **"Discipline – Étude – Charité"**
- Principal **Père Clément Nkodo Manga transferred to F.X. Vogt on 3 Aug 2026** (their news) → **decision-maker in flux this term; confirm who signs off before sending a concept.**
- Active site: **Semaine des Lauréats 2026** (17–21 Aug), 2026 GCE/OBC results banners, "Retour aux sources 2026", careers day; e-learning portal (elearning.collegedelaretraite.org); FB "Live Retraite" (facebook.com/colegedelaretraite)
- 2022: donated 25 computers + 50 MS Office licenses; 2021: Bâtiment Mgr Jean Mbarga inaugurated; multimedia library
- 2024 (lebledparle): principal's crackdown on teachers selling exam papers; school ran exams with same-day online results

**Premise check:** "site outdated" was **partly stale** — the .org site is active (Aug 2026 news) but old-style Joomla, heavy, broken thumbnail links, and the well-known domain **collegedelaretraite.com is DEAD** (two fetch failures — King to confirm from phone). Message rewritten: dead .com + phone-unfriendly live site; reference Semaine des Lauréats.
**Boarding:** nothing found → assume day; confirm at kickoff.
**NEW (12 Sep, from their Semaine des Lauréats poster):** school **mobile 693 240 047** (use as primary in concept) · event program 17 Aug Journée sportive / 19 Aug White Festival / 21 Aug Cérémonie des Lauréats · **current brand = royal blue #16337E + amber #E39A2D + cream** (2026 poster) — concept palette matches it.
**Concept (12 Sep):** `demos/concept-la-retraite-v1.html` — royal/amber/cream, **FR default**, 126/126 pairs, poster embedded base64 (self-contained 158KB file). H1 = their own copy ("Former l'homme, selon le plan de Dieu"), both mottoes, 1950/1960/76/2026 distinction stats, same-day-results fact, e-learning + multimedia library cards, 693 240 047 everywhere, form routes to their mobile.
**DECISION (13 Sep, King): ⏸️ PARKED.** School board likely mostly elders 50+ → risk-averse buyers; site is internally maintained (news current) → "l'ancien fait le travail"; cosmetic flaws (Irish number, dead menu) fixable in-house → repair angle loses punch; long committee cycle. Re-scored for close probability: ~12/20. **Revival triggers:** (1) 2–3 months later with 1–2 client proofs · (2) new principal (Abbé Messi Mbarga) pushes the 2026–27 "digitalisation" priority publicly · (3) inbound. **If revived, lead with CONVERSION, not repair:** 1 500 candidats au concours 2026, no admission flow, not mobile-first.

**UPDATE (13 Sep — King supplied the real URL + re-verified):** live site confirmed at **laretraitecatholicbilingualcollege.org** (collegedelaretraite.com still dead). New verified facts: news current through **4 Aug 2026** (Lauréats program 17–21, principal transition); **2026 concours banners** (T = strong); stats **3 000 élèves inscrits / 1 500 candidats / +99% de réussite**; **e-learning portal in production** (elearning.collegedelaretraite.org) — they already invest in digital. **New pitch angle (site alive but decaying):** nearly ALL nav/footer menu items link to `#` (dead) · Agenda = "No events" · **footer "Talk to us" shows 085 888 5555 (tel:+35385888555) — an IRISH number left in the template** · 2021 necrology on the homepage. **Signatory resolved: Abbé Alexandre Messi Mbarga (principal since Aug 2026).** Contact verified on site: **contact@collegedelaretraite.org** · landline (+237) 2 43 58 86 54 (= 233 588 654) · BP 159 Yaoundé. Channel: Messenger-first, no cold calls (King rule). Pack §4 message rewritten (compliment the current news first, then the dated-shell angle).

---

## 5 · COMOBIL – LES LAURÉATS (Douala)
**Identity:** **Collège Moderne Bilingue Les Lauréats (COMOBIL)** — created **1999, décret N°J1/7/MINEDUC**; school complex: **Général + Technique + Anglo-saxon (English) section**; Bonamoussadi (rond-point du marché), B.P. 6081 Douala.

**Verified facts**
- Motto (FB): **"Discipline – Travail – Succès"**
- **Boarding ("pension") included in fees** — 6e → Tle, pension comprise: **170,000–240,000 FCFA**. [banabam.org listing]
- Equipment: centre de documentation, salle multimédia, labo de langue, labo scientifique, infirmerie
- Sister school: **Collège La Maturité** (same WAFO group); patron association *"L'Enfance Joyeuse du Cameroun"* (Pierre WAFO, president); annual "Excellence Académique" awards
- Contacts: **233 470 608** (Pierre WAFO ✓ pack) · comobil@yahoo.fr · comobi.laureats@yahoo.fr · FB page 100064111147236

**Premise check:** comobil.com = **parked ad-redirect page** (not the school) ✓ — "site inaccessible" premise holds; their FB "website" field points at that dead domain (extra hook).
**Message:** sharpened — mention the three sections + dead official address.

---

## CLINIC PIPELINE (new 12 Sep — King: "we also talked about working with clinics")
**⚠ Framework gap:** the ICP in `AMK-Sales-Process-v1.docx` is school-only (checks 1–3 say "school/tuition"). Clinic ICP = adapted 7 checks (below). Recommend a clinic ICP + clinic message variants before scaling the segment.

### Oracare237 — OraCare Dental Clinic, Buea (researched 12 Sep, from King's ad sighting)
**Verified facts**
- FB page **Oracare237** (id 100075164312902) — "Dentist & Dental Office", **Molyko, Buea**
- "Located in Mayor's Street, Buea **at St. Pius Hospital**" — physically co-located with the hospital
- Tagline: "Your smile is our priority" · services posted: **smile makeover, braces** (high-ticket aesthetic)
- Phone **+237 6 72 52 66 86** (mobile) · email **snkafuarnold11@gmail.com** (owner-operator — decision maker reachable directly)
- **280 likes · 5 talking about this · 1 review · "not yet rated"** · recent video post ("Smile makeover, braces")
- **Running paid ads** (King saw the ad) = active budget + active marketing
- **No website found** — oracare237.com / oracarebuea.com don't resolve; no directory/GBP/IG listings for the Buea clinic (all other "OraCare" results are US/Dubai/Maldives/Ethiopia)

**MQL gate (adapted clinic ICP): 6/7 → MQL**
1. Private business in target city — ✅ Molyko, Buea
2. Real operation (scale proxy) — ✅ physical clinic in a hospital
3. Budget proxy — ✅ paid ads + high-ticket aesthetic services
4. Website problem D/E — ✅ **no website at all (gold)**
5. Active social/marketing ≤60d — ✅ fresh posts + live ad campaign
6. Decision maker reachable — ✅ owner's email + mobile public
7. Professional management signals — ⚠️ partial (single clinic, 1 review)
+ CHANNEL: FB live ✅ · mobile **for King to verify on WA** (standing rule)

**Score: 18/20 → A+** (website +4 · marketing +3 · business quality 6/8 · digital opportunity +5: no site +2, ad spend to convert +2, EN/FR market +1)
**SQL? NOT YET — by definition:** no contact, no reply, BANT unconfirmed. Pre-read: B 🟢 (ad budget) · A 🟢 (owner answers himself — better than a school committee) · N 🟢 (ads landing on a 1-review FB page; braces patients Google first) · T 🟡 (no visible trigger; live ad campaign = soft trigger). **Becomes SQL on reply + BANT complete** → then free concept, same as schools (dental-clinic concept = new template #4, navy/teal or clinical blue/white — build on demand).

**First message (EN — Buea is English-medium; permission-first, no sell in msg 1):**
> Good morning, my name is Akwo King, founder of AMK – Web Development & Digital Solutions, Cameroon. I came across Oracare237's recent ad for smile makeovers — and patients who see ads like that usually check the clinic on Google before they call, but right now the ad leads to a Facebook page instead of a website. We're preparing free homepage concepts for a few clinics in Buea — your colours, your services, in English and French, no cost, no obligation. May I send you a first look?
> — Akwo King · AMK – Web Development & Digital Solutions

**AD PROOF (13 Sep — King screenshot, `sales/evidence/oracare-ad-pricing-ask-2026-09-12.jpeg`):** live video ad (clinic interior) with public engagement — "They are soo good" (2d) + "Wow cool if prices were listed for the different services it would be great 👍" (17h, Mado Ayamba via FB). **BANT pre-read now: B🟢 · A🟢 · N🟢 (public pricing demand under their own ad) · T🟢 (ad live + unmet question).** Use AFTER preview permission only: "Under one of your recent ads, a parent was asking for prices per service — the services section of this page answers exactly that." Never send the screenshot in msg 1.

**Next steps (updated 09/12):** ✅ King verified 672 52 66 86 on WhatsApp → send with the Monday batch (separate segment, clinic pilot) → reply = run BANT from the process doc → concept **BUILT**: `demos/concept-oracare-v1.html` (template #4, 145 pairs, EN default; cream/sand + soft navy + sage + soft gold; Smile Assessment, before/after drag slider, 3-step booking form posting a structured JSON payload + WhatsApp routing to the clinic's own number with ref code, **24/7 scripted chat assistant** — 13 intents, EN|FR, verified info only, funnels to booking/call; upgrade path to real AI = paid add-on).

## Cross-cutting
- **Boarding status per school:** Sasse = boarding (8 dorms) · COMOBIL = pension included · NHICHS = explicitly none · Retraite = day (unconfirmed) · SAHISCOL = unknown → **always ask "jour ou pension ?" in kickoff before finalising any concept.**
- Diocesan web presence is fragile (Sasse page down, SAHISCOL page thin, new colleges gallery 500) — landing Sasse makes the Diocese of Buea a likely referral source.
- King's number +237 677 789 631 is wired in all demo/concept files (Sasse file keeps the SCHOOL's 677 195 500 as its admissions number — correct as-is).
- Sources that died during research (re-fetch if needed): cesbueadiocese.org/sajocol (down) · cesbuea.org/sahiscol (down) · new.bueadiocese.org colleges gallery (500) · banabam.org (down, snippet captured).
