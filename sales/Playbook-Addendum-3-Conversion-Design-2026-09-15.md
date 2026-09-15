# Playbook Addendum #3 — Conversion Design Standard (client websites)

**Date:** 15 Sep 2026 · **Status:** CONTROLLING STANDARD for every AMK build (clinic, school, nursery, future verticals) · **Supersedes:** nothing; extends the delivery checklist and Addendum #2 (SEO)
**Sources (King's study tour, 15 Sep, all watched/read in full with transcripts):**
1. Flux Academy — *How To Increase Conversions With Design* (11:07) — focus, flow, trust, attention, friction, scarcity, speed.
2. Flux Academy — *$500 vs $5,000 vs $50,000 Websites* (10:16) — price is set by the problem solved and the process, not the visuals.
3. Malewicz/Hype4 — *Why Beautiful Websites Don't Convert* (12:57) — clarity beats aesthetics; social proof forms; load time; gaze; CTA practice.
4. Malewicz — *How websites convert into sales?* (10:05) — hero header formula: kicker → headline → clarifying line → CTA → key visual; gaze direction.
5. Malewicz — *How We 3X'd This Website's Conversion* (10:50) — **medical-startup case study (hospitals/clinics)**; high-consideration buyers want MORE information, segmented by niche.
6. HubSpot Marketing — *Build The PERFECT Homepage* (07:47) — orient instantly, prioritise one conversion, lanes by buyer, sticky CTA, cut friction, A/B test.
7. Sagapixel (healthcare marketing) — *5 Proven Ways to Increase Your Website Conversion Rate* (05:19) — formula: right-place+CTA → proof → services/story → objections → alternative CTA; sticky mobile button gave **+37% leads from month one**; secondary hero CTA to results/gallery; link reviews to third-party source; FAQ wins Google + LLM rankings.
8. Malewicz — *The Secret to Mobile Web Conversion* (10:57) — >90% of traffic is mobile; mobile is its own design; tap targets 52–64px; big type; no parallax/animations; ≤2 fields before conversion; sticky action bar (not sticky logo/nav); test on real phones.

---

## 1. The one formula every client homepage follows

All eight sources converge on the same ordered page. This is now AMK's build spec, top to bottom:

1. **Hero — "am I in the right place?" (answer in 4–5 seconds)**
   - eyebrow/kicker: *what they are + locality* ("Private clinic & laboratory · Bonamoussadi, Douala" / etc.)
   - headline: the **outcome the visitor came for**, in their words — not the business's praise of itself. Clinic = be seen today / know the price / reach us on WhatsApp. School = fees visible, admissions in one tap, GCE results online, boarding parent contact.
   - one clarifying sub-line that kills the top 2–3 doubts (price? language? speed? location?).
   - **TWO buttons only:** primary = the money action (Book/Enrol on WhatsApp); secondary = the low-commitment proof action (See prices / See GCE results / Services). No more than two.
   - key visual that supports the headline. **Gaze rule:** any face in the hero looks *toward the CTA*, never off-screen. No stock beauty shots disconnected from the copy.
   - one micro-proof chip is allowed in the hero (rating + count, or "replies in minutes").
2. **Proof strip immediately after the hero** — ratings/numbers so early visitors don't have to scroll to trust. See §3.
3. **Services / programmes, segmented by the visitor** — clinics: tile per patient type (maternity, dental, paediatrics, lab…) each with its own Book deep-link; schools: one lane per buyer (day parents, boarding/abroad parents, GCE candidates → Student Corner). If a visitor doesn't see their own problem listed, they leave (Medidesk 3× lesson).
4. **How it works** — 3 steps max; the last step is "we continue on WhatsApp."
5. **Price / fees** — transparent FCFA. Our differentiator; never buried.
6. **Objections → FAQ** — every question the buyer checks before acting (payment, insurance, walk-ins, languages, boarding visits, results timing). FAQ is also the LLM/Google voice-search surface (Addendum #2): write questions literally as asked.
7. **Final conversion band** — big WhatsApp action, then the **alternative CTA** (§5) for the not-ready.
8. **Sticky mobile action bar** on every screen (already shipped in our generators).

**Focus law (Flux/Unbounce data):** the average page has 4.39 links per decision area; converting pages have fewer. One primary action per screen. Kill decorative links.

## 2. Mobile is the build — desktop is the variant

>90% of Cameroon visitors are on Android phones over 3G/Edge. Our templates already mobile-first; these are now hard gates:

- Primary CTA tap target **min-height 52px, max 64px** on mobile (desktop 48–52); full-width in the sticky bar; never small icon-only buttons for the main action. Tiny social-proof icons that can't be read are removed on mobile.
- **Sticky bottom action bar = WhatsApp (primary) + Call (secondary)**. Sticky *logo/menu* is forbidden (wastes the thumb zone); a scroll-to-top control is all that may join the bar.
- Mobile type gets **bigger, not smaller**; rewrite the mobile copy shorter. Say **"tap"**, never "click".
- No parallax, scroll-hijack, entrance animations, or video on mobile hero (they slow 3G and distract; Malewicz: animations are where mobile conversions die). IntersectionObserver fade-ins are allowed only above-the-fold-light and GPU-cheap (our current `rv` usage passes; do not add more).
- No "phone inside a phone" / app-in-app visuals; show the problem being solved, not a screenshot of a screen.
- Forms: **max 2 fields before the action**; our booking forms compose a pre-filled WhatsApp message and submit nothing to a server — keep it that way. Capture name + number, everything else optional.
- Micro-visuals: mobile hero = headline + button first; the big image drops below or becomes a small supporting chip; the next section clears doubt.
- **Handoff test on King's real Android:** open at night, in daylight/sunlight, on slow MTN data; both EN and FR; every button thumb-reachable. Record the result in the delivery checklist. PageSpeed Insights mobile pass: LCP under ~2.5s simulated-fast-3G; compress every JPG (our mock images already ship resized — keep under ~200 KB each), keep the single font family with system fallback (already Outfit + preconnect).

## 3. Social proof — what we are allowed to use (accuracy law applies)

Nobody wants to be first. Proof priority for a small Cameroon business:

1. **Third-party reviews with an outbound link to the real source** — Google Business Profile first, then their Facebook ratings. Never paste cherry-picked review text without linking where it lives. Demo templates must clearly mark `demo values`; at launch the client's real rating/review count goes in, or the block is removed. **Never invent reviews, ratings, patient counts or testimonials** (standing accuracy law).
2. **Sheer numbers that are true:** years operating, services under one roof, languages, opening days, students per class range — every figure verified at kickoff, marked demo until then.
3. **Credentials & institutions:** GCE Board marking-centre status (verify camgceb.org), medical council/order registration, denominational affiliation where the client documents it.
4. **Logos of partners/institutions only with permission.**
5. Faces: team/proprietor photo builds the "serious people behind it" trust — use where the client gives one; gaze-to-CTA rule applies.
6. Directory demand is **pitch ammo, not site content**: e.g. "292 WhatsApp clicks from your DoualaTour listing" goes in King's outreach, never on the client's site.

Shipped in generators this date: a marked-demo **proof section** (rating chip + 3 quote slots with a "read all reviews on Google" outbound placeholder) right after the stats band, for both clinics and schools (schools' proof = GCE results link to camgceb.org + parent quote slots).

## 4. Objections and density — two different audiences, two rules

- **Client sites serve B2C visitors (patients/parents): goldfish rule** — subtract everything that doesn't aid the decision. Clarity first, then proof.
- **High-consideration BUYERS (proprietors, medical directors deciding on AMK) want exhaustive answers** — the Medidesk 3× case: expensive, risky, niche decisions convert MORE when the page answers every question and lets each niche find itself. Applied to us: named concept links, AMK's own pages and the kickoff kit stay information-rich, bilingual, with per-vertical and per-city specificity. Do not strip the pitch pages to minimal.
- FAQ blocks serve both: objection-killer on client sites, and they win LLM/Google citation (Sagapixel explicitly; already in Addendum #2's keyword map).

## 5. The alternative CTA (new required element)

Every final band offers a low-commitment path for visitors not ready to book/enrol:
- Clinic: **"Follow us" → their Facebook/Instagram/TikTok** (health tips, opening updates), or "Save our number".
- School: **"Follow admissions on TikTok/Facebook"** (dovetails King's inbound strategy — the client's social becomes their own admissions funnel, and our TikTok/IG traffic loop).
Placeholders ship marked `#`/demo and are replaced at launch with the client's real pages, or removed if they have none — never linked to AMK's accounts on a client site.

## 6. Scarcity, urgency and price — the honest version

- Scarcity/urgency convert only when **real and true**. AMK's only scarcity: the **2 founding slots per month at 100 000 FCFA** — said plainly, with the date. No countdown timers, no expiring-discount banners (the price is never discounted; standing law), no fake "3 people viewing now".
- On client sites: honest urgency only ("Walk-ins today until 6pm" / "Admissions close 12 Sep" with a real date the client supplies).
- **Pricing confidence (Flux tier video):** the gap between a $500 site and a $5 000 site is not looks — it is strategy, conversion copy, proof architecture, mobile engineering, SEO and iteration; the $50 000 tier exists because one extra deal pays for it. Our founding offer delivers the *middle-tier process* (strategy, bilingual conversion build, proof/FAQ, WhatsApp funnel, launch SEO from Addendum #2, handoff video) at a Cameroon-accessible price; **the price is justified in outcomes** (admissions calls, booked appointments, owning vs renting the patient relationship — mondocteur237/Directory lesson), never in pages or hours. Use when a prospect compares us to a Fiverr/Wix quote: "a template checks the box 'we have a website'; this is built to make the phone ring — here is the section-by-section difference" (walk the formula in §1).
- Ladder after founding: Growth Care already includes GSC reporting; add **CRO iteration** as a stated benefit (A/B test hero headline/button label from real WA-click data — HubSpot's test→test→test loop).

## 7. Copy rules

- Hero/FAQ copy comes from **the client's own mouth at kickoff** (Malewicz: the converting copy is in the founder's head; AI-generic copy underperforms). Kickoff kit questions now explicitly collect: the three things patients/parents ask most on the phone, and the exact words they use.
- Every claim specific and verifiable; "best", "leading", "No.1" banned unless the client holds proof (then still prefer the proof itself).
- Bilingual copy is written, not translated-from-English afterthought; FR button label "Tap", not "Cliquez".

## 8. QA gate added to every build (append to Internal Delivery Checklist)

| # | Gate | Pass condition |
|---|------|----------------|
| C1 | 5-second hero test | a stranger can say what/who/where + next tap within 5s, EN and FR |
| C2 | Two CTAs max in hero; one primary per section | visual count |
| C3 | Proof strip present | links to live Google/FB source OR removed; every number verified, demo tags gone |
| C4 | Sticky mobile bar | WA primary + call secondary, ≥52px targets, present on scroll everywhere |
| C5 | Mobile real-device test | King's Android, night + sunlight, slow MTN, EN+FR |
| C6 | Speed | PageSpeed Insights mobile run saved; hero images <200 KB; no render-blocking extras |
| C7 | FAQ ≥4 real objections | phone-question sourced; questions phrased as searched |
| C8 | Alternative CTA | real social URLs or block removed |
| C9 | Friction | forms ≤2 required fields; no clicks "click"; tap labels on mobile |
| C10 | Gaze/faces | any face looks toward the primary CTA |
| C11 | Scarcity honesty | only real dates/slots; no timers/fake counters |
| C12 | A/B plan | one post-launch test named in handoff (button label or hero line) for Growth Care clients |

## 9. Implementation log (15 Sep)

- **Already in generators before this study** (validated, keep): sticky bottom mobile WA/call bar, dual hero CTAs, stats/sheer-numbers band with demo tags, per-audience service tiles, transparent FCFA pricing, FAQ `<details>`, bilingual data-EN/data-FR toggle with `?lang=`, WhatsApp-composed booking (no server form), IntersectionObserver reveal + count-up, schema.org School/Clinic JSON-LD.
- **Added this date to `site/build_sample_clinic.py` and `site/build_sample_secondary.py`:** proof section (third-party-linked rating + quote slots, demo-marked); alternative-CTA follow strip in the final band; sticky-bar buttons min-height 52px on mobile.
- **Backlog (next natural deploy, do not hot-deploy tonight):** regenerate named `mitoc-concept` and any live named concept with the same two blocks; replace demo social/Google URLs at each client's launch; add PageSpeed screenshot to the kickoff kit; real-device C5 test by King at handoff; Growth Care CRO test naming in the retainer one-pager.
