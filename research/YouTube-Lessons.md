# AMK — YouTube Lessons Log (ingestion register)

**Created:** 17 Sep 2026 · **Protocol owner:** King · **Operator:** AMK

This is the catch-all register for every YouTube link King drops in chat. Links whose lesson belongs in an existing playbook/ops file are folded **there**, not here — but **everything is logged here**, one entry per video, dated, with the verdict (absorbed / alternative / rejected / conflict). Any future chat can see what has been absorbed and what was thrown away, and why.

---

## 0 · How to ingest (method that works in this sandbox)

- The sandbox has **no raw network** (direct `curl`/`getent` fail). Transcripts come through the `fetch_page` tool only.
- **Working path:** `https://youtubetotranscript.com/transcript?v=VIDEO_ID` → full transcript, title, channel (tested 17 Sep 2026).
- If that returns nothing: try `?v=ID&current_language_code=fr` for French captions. If still nothing (members-only, no captions, livestream), **stop and ask King to paste notes — never guess at content.**
- Extract, don't summarize: core claim(s) · AMK-applicable tactics (2–5) · contradictions vs playbook · junk filter · attribution.

## 1 · Where each field folds (keep files in scope)

| Field | Primary target | Versioning |
|---|---|---|
| Sales (prospecting, qualifying, closing, objections, FU, pricing) | `sales/AMK-Sales-Playbook-v2.md` | bump v2.x + changelog line |
| Outreach copy / social / positioning | `sales/Monday-Outreach-Pack.md` + the dated pack in use | date-stamped edit note |
| Design (visual standards, layout, type, color, anti-default) | `AMK-DESIGN-SKILLS.md` §1–§17 | dated entry in the section |
| Build (HTML/CSS/JS, mobile-first, EN\|FR, base64, perf, deploy) | `AMK-DESIGN-SKILLS.md` §build/deploy + `hosting/DEPLOY.md` | dated entry |
| Agency ops (delivery, onboarding, retention, upsell, referrals) | relevant ops/delivery doc (`sales/AMK-Playbook-Addendum-*`) | dated entry |
| Niche intel (schools, clinics, Cameroon/Africa, WhatsApp-first buyers) | `sales/Deep-Dive-Research.md` or the playbook addendum in scope | dated entry |
| Content / social (video marketing, platform craft, posting, hooks, CTAs) | `content/lessons/CONTENT-LESSONS.md` + `content/strategy/CONTENT-STRATEGY.md` / `POSTING-CALENDAR.md` | version bump (v0.x) + changelog line |
| Anything that fits nowhere | **this file**, as a dated entry | — |

Cross-link with the weekly techniques register `sales/research/2026-W37-techniques.md` when a video and a technique overlap.

## 2 · Standing bias (every lesson passes this lens or it does not enter)

WhatsApp-first · mobile-first · EN|FR · Cameroon (Kumba/Douala/South-West) · clinics & schools · close one client by 30 Sep · 500 000 FCFA/month by month 6. If a tactic doesn't serve that, it goes in §5 Rejected — named, not silently dropped.

## 3 · Ingestion log (one line per video)

| # | Date | Video / creator | Field | Verdict | Folded into |
|---|---|---|---|---|---|
| 1 | 17 Sep 2026 | FREE Website Copywriting Course — Jesse Forrest | Marketing / Build | Absorbed | `sales/Monday-Outreach-Pack.md` (copy gate) · `AMK-DESIGN-SKILLS.md` §11 |
| 2 | 17 Sep 2026 | How To Write Killer Copy That CONVERTS — Trent Kennelly | Marketing | Absorbed (alternatives) | `research/YouTube-Lessons.md` §4 · `AMK-DESIGN-SKILLS.md` §11 |
| 3 | 17 Sep 2026 | Copywriting for Beginners — Adam Erhart | Marketing | Absorbed (practice drills) | `AMK-DESIGN-SKILLS.md` §11 · `sales/Monday-Outreach-Pack.md` |
| 4 | 17 Sep 2026 | How to Write Irresistible Website Copy — Graham Cochrane | Marketing / Niche | Absorbed (customer-language rule) | `sales/AMK-Sales-Playbook-v2.md` → v2.1 Part H · `sales/Monday-Outreach-Pack.md` |
| 5 | 17 Sep 2026 | Learn Copywriting in 76 Minutes — Harry Dry (David Perell) | Marketing / Sales | **Absorbed — new copy law** | `sales/Monday-Outreach-Pack.md` (COPY CRAFT GATE) · `AMK-DESIGN-SKILLS.md` §11 · playbook v2.1 |
| 6 | 17 Sep 2026 | 14 Years of Copywriting Knowledge in 1 Hour — Alex Nafia-Holland (Relume) | Marketing / Niche | Absorbed | `AMK-DESIGN-SKILLS.md` §11 · playbook v2.1 Part H · `sales/Deep-Dive-Research.md` (WhatsApp-default line) |
| 7 | 17 Sep 2026 | After Closing 4000+ Sales… — Alex Hormozi | Sales / Objections | Absorbed (new reframe system) | `sales/AMK-Sales-Playbook-v2.md` → **v2.2 Part I** |
| 8 | 17 Sep 2026 | The Secret To Alex Hormozi's Sales Success — SaaS Academy | Sales / Ops | Partly absorbed; team sections rejected | playbook v2.2 **Part J** |
| 9 | 17 Sep 2026 | The Engineering Skill AI Won't Replace — JavaScript Mastery | Build / Engineering | Absorbed | `AMK-DESIGN-SKILLS.md` **§18** · `hosting/previews/README.md` (deploy gate) |
| 10 | 17 Sep 2026 | Design Experts Review Vibe Coded Websites — Y Combinator (Raphael Schaad) | Design | Absorbed (anti-slop ban list) | `AMK-DESIGN-SKILLS.md` **§3.8** |
| 11 | 17 Sep 2026 | The Easy Way to Design Top Tier Websites — Sajid | Design | Absorbed | `AMK-DESIGN-SKILLS.md` **§19.1/§19.2/§19.4** · `design/WORKFLOW.md` stage 3b |
| 12 | 17 Sep 2026 | Give Me 7 Minutes & Your Web Design Skills Will Take Off — Self-Made Web Designer | Design / Conversion | Absorbed | §19.1/§19.2 · §6 (60-30-10) · §5 (line-height, centring) · §8 (ghost rule) |
| 13 | 17 Sep 2026 | Still Vibe Coding AI Slop? (Genspark) — Build Great Products | Design / Build | Absorbed | §19.3 · §3.8 avoid-list · `design/WORKFLOW.md` 3b |
| 14 | 17 Sep 2026 | How to Vibe Code a Designer-Level Website — The Next Wave (Munk Toad) | Design | Absorbed | §19.5 · §5 (pairing) · §6 (background derivation) · §17 cross-ref |
| 15 | 17 Sep 2026 | How To Make A Marketing Video For My Business — Nate Woodbury | Content / Marketing (video) | Absorbed (promo asset + script gates) | `content/lessons/CONTENT-LESSONS.md` **§10.1** · `content/scripts/README.md` (gates) · `content/pipeline/CONTENT-SHORTLIST.md` **V-13** |
| 16 | 17 Sep 2026 | How To Make High Converting Videos For Your Business — Brooklyn Social | Content / Marketing (video) | Absorbed (hook/CTA discipline); on-camera-team rejected | `content/lessons/CONTENT-LESSONS.md` **§10.2** |
| 17 | 17 Sep 2026 | How to Create Free 2D Animated Explainer Videos … using Canva — Digital Canva Mastery | Content / Production | Mostly rejected; 2 micro-techniques adopted | `content/lessons/CONTENT-LESSONS.md` **§10.3** |
| 18 | 17 Sep 2026 | Everything About: Footers In Web Design — The Website Architect | Design / Build (footers) | Absorbed (anatomy + SEO rules; A/B stats rejected) | `AMK-DESIGN-SKILLS.md` **§20 · §13** |
| 19 | 17 Sep 2026 | Website Footer Design Inspiration (Best practices) — Flux Academy | Design (footers) | Absorbed (footer as designed screen; mobile caveat) | `AMK-DESIGN-SKILLS.md` **§20** |
| 20 | 18 Sep 2026 | How I sell "Talking Websites" to local businesses for 499/mo — Pavlo | Build (voice) / Sales (offer model) | **Absorbed with a hard limit** — voice layer yes, SaaS stack no; recurring model **pending King** | `AMK-DESIGN-SKILLS.md` **§21** · `sales/Voice-Offer-Decision-2026-09-18.md` |
| 21 | 23 Sep 2026 | Sales system — Will Barron (`youtu.be/5swDtQFyIws`) | Sales / Close | Absorbed (6 pieces + 6-step discovery) | `sales/SYSTEME-DE-VENTE-AMK-2026-09-23.md` · `sales/RDV-*.md` |
| 22 | 23 Sep 2026 | The 5 levels of persuasion — Joanna Wiebe (`youtu.be/cT82oNk49ks`) | Sales / Copy | Absorbed — audit of **our own** messages, 5 rewrites | `sales/PERSUASION-5-NIVEAUX-2026-09-23.md` · `sales/MESSAGES-2026-09-23-PERSUASION.md` |
| 23 | 23 Sep 2026 | Words That SELL — Joanna Wiebe (`youtu.be/7gjtI1rnds4`) | Sales / Copy | Absorbed (9 triggers declined to our real messages) | `sales/DECLINAISON-9-DECLENCHEURS-2026-09-23.md` · MESSAGES §8 |
| 24 | 23 Sep 2026 | What I Wish I Knew Before 10 Years in UX (The 3 Levels) — Amir Moradi (`youtu.be/gr0Val2QSbM`) | Design / UX | Absorbed (the invisible timeline) | `AMK-DESIGN-SKILLS.md` **§22.1** |
| 25 | 23 Sep 2026 | Every UI/UX Concept Explained in Under 10 Minutes — Kole Jain (`youtu.be/EcbgbKtOELY`) | Design / Build | **Absorbed — the four states + the response** | `AMK-DESIGN-SKILLS.md` **§22.2** · `tools/qa/audit_page.py` |
| 26 | 23 Sep 2026 | The UX Psychology Behind Apps People Can't Stop Using — uxpeak (`youtu.be/2TlIg3VokY8`) | Design / Psychology | Absorbed, **honest half only** | `AMK-DESIGN-SKILLS.md` **§22.3** |
| 27 | 23 Sep 2026 | The Psychology of a PERFECT Website — Self-Made Web Designer (`youtu.be/d-IaU9qcDGg`) | Design / Psychology | Absorbed (3 friends, mental models, MAYA, chunking, ladders) | `AMK-DESIGN-SKILLS.md` **§22.3/§22.4** |
| 28 | 23 Sep 2026 | Your Website Won't Matter in 2027. Prepare Now. — Wes McDowell (`youtu.be/VXGDHZIGf40`) | Strategy / Search (AEO) | Absorbed as analysis; **a decision for King** (content freeze stands) | `AMK-SEO-PLAYBOOK.md` **§8** |
| 29 | 23 Sep 2026 | How to Attract HIGH PAYING Clients (Stop Selling Services) — Nicole & James (`youtu.be/Y_sPva_30XA`) | Sales / Offer | Absorbed (3 R + the service trap); coined product names rejected | `sales/AMK-Sales-Playbook-v2.md` **PART K** |
| 30 | 23 Sep 2026 | 7 Web Design Styles That Make Sites Look Expensive In 2026 — Web Design Lab (`youtu.be/Fog8WpdTnYU`) | Design / Style | Absorbed as tests, not looks; kinetic + expressive restricted | `AMK-DESIGN-SKILLS.md` **§23.1–23.3** |
| 31 | 23 Sep 2026 | 6 EASY Tips to 10x Any Site's Design — Self-Made Web Designer (`youtu.be/pbhLsV-Dyho`) | Design / Craft | **Absorbed — and it found a real drift on our own site** | `AMK-DESIGN-SKILLS.md` **§23.3–23.6** |
| 32 | 23 Sep 2026 | The Secret to Mobile Web Conversion — Malewicz (`youtu.be/q8yUIbRiNRc`) | Design / Conversion (mobile) | **Absorbed** — 5 fautes + la fenêtre du bouton (52-64 px) + le poids des images | `AMK-DESIGN-SKILLS.md` **§24.1** · `demos/concept-unilabo-v1.html` |
| 33 | 23 Sep 2026 | This is what mobile web design excellence looks like — Flux Academy (`youtu.be/1r4GHOd2THM`) | Design (mobile) | **Absorbed** — mobile n'est pas un bureau empilé ; « chaque panneau doit être une affiche » | `AMK-DESIGN-SKILLS.md` **§24.2** |
| 34 | 23 Sep 2026 | Mobile Design 101: How to Design for Mobile First — Jesse Showalter (`youtu.be/q6qA_609UOE`, direct) | Design / Build (mobile) | **Absorbed** — distiller, la règle du pouce, la légibilité, le POIDS | `AMK-DESIGN-SKILLS.md` **§24.3** · `tools/qa/test_unilabo_page.mjs` |
| 35 | 23 Sep 2026 | 40 of the Best Lab Websites — Thomas Digital (`thomasdigital.com/industry/lab-website-design`) | **Verticale** (labo / clinique) + concurrence | **Absorbed** — 7 principes ; **et une question à poser au client** (agrément) | `AMK-DESIGN-SKILLS.md` **§24.4** · `clients/uni-labo/AUDIT-2026-09-23.md` §9 |


## 4 · Entries (full reports)

### [1] 17 Sep 2026 · Jesse Forrest — "FREE Website Copywriting Course (Full Tutorial)"
**Link:** https://youtu.be/e3rcytD5Z_g · **Field:** Marketing / Build · **Length:** long-form course

**Core claims**
1. Website copy = engaging + persuading to act; audience research precedes all writing (client questions + a Reddit-mining research pass).
2. 10 practical rules: 1–2 long-tail keywords per page (title, meta ≤150 chars, body ~once/200 words); a headline must answer the 3 silent questions (what is this / what can I do here / is this what I want); 80% of viewing time is above the fold → headline + subhead + CTA there; 70% skim → headings, short paragraphs, bullets, short sentences; real photos beat stock; PAS (problem–agitate–solution); benefits over features ("…which means…"); "$5 words → 5-cent words"; CTAs use 3–5 action verbs + urgency, repeated top/middle/bottom; testimonials in a **before–during–after** structure.

**AMK-applicable tactics**
1. **"Which means" translator** in every concept section: feature → consequence (clinic: "Résultats par WhatsApp" → "le patient n'a plus à revenir chercher son papier").
2. **Testimonial template** for delivered sites: before–during–after, collected by interview (see [4]).
3. **Above-the-fold audit** of every concept: does the first screen (mobile!) say what it is, what to do, and one CTA?
4. **CTA ladder**: same action repeated top, middle, bottom of the concept page — not one button in the hero.

**Contradictions:** none with our playbook; reinforces the existing ≤8-word headline + ≤25-word sub rule (§11).

**Junk filter:** "hire a copywriter / become a freelance copywriter on Upwork" framing (we are the vendor); 2018 above-the-fold study is dated — kept directionally, mobile-first anyway; Perplexity-on-Reddit research is US-angled — our equivalent is the prospect's own FB page + comments.

---

### [2] 17 Sep 2026 · Trent Kennelly — "How To Write Killer Copy That CONVERTS! (Copywriting For Websites 101)"
**Link:** https://youtu.be/L9gb9L-b9tM · **Field:** Marketing · **Length:** ~15 min

**Core claims**
1. Frame the page **before** writing: full-width header (headline ≤2 lines, ≤50% width) → subhead → CTA; full-width text block; "dancing columns" (alternating image/text); 3-column row (value props or testimonials); final full-width pitch row.
2. Two copy modes: **toward pleasure** vs **away from pain** — pick one deliberately per page.
3. A headline does two jobs in one sentence: communicate the core message + make them care. Asana: "Work on big ideas without the busy work." WeightWatchers: "Weight loss and wellness designed for you."
4. CTA needs **context text around the button** — a naked "Buy now" converts nothing.
5. Emotionally charged words (secret, instant, reliable); ban worn buzzwords (passion, revolutionary, dynamic).

**AMK-applicable tactics**
1. **Away-from-pain is our house mode** (dead domain, patient who finds nothing) — keep it, but note the alternates: one "toward pleasure" line per message (the future state) to close the loop.
2. **CTA context** rule: our "Répondez juste « oui »" + the mockup offer is exactly this — never send a bare link.
3. **Buzzword ban list (bilingual)** for concept + outreach copy: passion/passionné, revolutionary/révolutionnaire, dynamic/dynamique, "solutions digitales" as a selling point (keep only in the signature).
4. **Page frame template** = the sequence our concept builder should default to; verify each concept has the full-width text block AND the closing pitch row.

**Contradictions:** our concepts sometimes open with a proof strip before the pain section; Alex [6] says pains first, Trent says frame first — no conflict, but sequence: proof above fold is fine when it's the prospect's own real numbers.

**Junk filter:** Reddit/Amazon review mining (low local yield); "wall-of-love" 3-column testimonials (contradicted by [6] — one at a time wins); word-doc wireframing is fine but we already build live.

---

### [3] 17 Sep 2026 · Adam Erhart — "Copywriting for Beginners: The Ultimate 2026 Guide to Writing Words That Sell"
**Link:** https://youtu.be/YSFvTTa7_Pw · **Field:** Marketing · **Length:** ~25 min

**Core claims**
1. Copywriting = *words that make people act*; not poetry, not cleverness — clarity + usefulness.
2. Two workhorse frameworks: **AIDA** (attention–interest–desire–action) and **PAS**; "nobody buys a drill, they buy the hole"; benefits > features.
3. "Write like you talk" — read it out loud; if it sounds robotic, rewrite.
4. **Practice system:** read copy like a copywriter (reverse-engineer why it works); write daily (10 headline variants, rewrite a cereal box as dog-treat copy); hand-copy great ads; build a **swipe file**; read the few right books (Ogilvy, Cashvertising, Cialdini).

**AMK-applicable tactics**
1. **AMK swipe file starts now** — folder `sales/swipe/` for winning local copy: our own sent messages that got replies, prospect FB phrasing, competitor clinic ads, the Harry Dry classics from [5] (falsifiable lines). Every concept and message that gets a reply gets logged there with the result.
2. **Daily rep in the existing 15-min drill** (Part G): write 5 headline variants for one real prospect (2 min) — swaps into the current drill without adding time.
3. **Read-aloud test** added to the pre-send gate for every cold message and every concept hero.
4. "Sell the hole": for each offer, write the outcome line first (results received without travel / parents register online without a phone call), then the feature.

**Contradictions:** none.

**Junk filter:** the freelance-platform money path (Upwork/Fiverr), the free HighLevel funnel pitch, book recommendations (US direct-response canon) — dropped; keep only the drills.

---

### [4] 17 Sep 2026 · Graham Cochrane — "How to Write Irresistible Website Copy (from a copywriting pro)"
**Link:** https://youtu.be/1IAa97uPMBI · **Field:** Marketing / Niche · **Length:** ~15 min

**Core claims**
1. **You don't originate copy — customers write it for you.** Interview 3–4 recent clients with 4 questions: (a) what problems did you have before? (b) what was working together like / what did you appreciate? (c) what would you say to someone considering this? (d) *"anything else you'd like to add?"* — question (d) is where the gold is.
2. Their exact words become your headline — the reader feels "how did they know that?"
3. Read the headline out loud to a stranger; if they don't get it, rewrite — cute fails (the florist who "turns creation into beauty" sells nothing).
4. Social proof changes price tolerance (~31% willing to pay more for great reviews) — reviews must echo the brand story and appear **wherever a purchase decision happens**, not on a single portfolio page.

**AMK-applicable tactics**
1. **Testimonial harvest** becomes a numbered step in delivery: at handover (or 1 week after launch) ask the client's own 3–5 customers these 4 questions — voice notes on WhatsApp are enough — and put their verbatim words into the site.
2. Put this in the **USD‑0 upsell**: "I'll come back in 2 weeks and collect 3 patient testimonials for the site" — over-delivery, zero cost, feeds the next concept's proof.
3. **Cold-message version:** use the prospect's own public words (FB comments, reviews) instead of our adjectives — same mind-reading effect, no interview needed.
4. **Headline litmus** (read aloud to someone who knows the niche) → pre-send gate for every hero.

**Contradictions:** our current concept proof = follower counts + Google stars, mostly numbers; the video says specific human words outperform generic numbers. **Action:** concepts must carry at least one real verbatim quote (from their FB) beside the numbers. Not a conflict, an upgrade — applied.

**Junk filter:** the "attract and repel guide" lead magnet, the 31% stat as a *pitch* number (US survey, internal calibration only — never quote to a Douala clinic).

---

### [5] 17 Sep 2026 · Harry Dry (David Perell channel) — "Learn Copywriting in 76 Minutes"
**Link:** https://youtu.be/TUMjnmfsPeM · **Field:** Marketing / Sales · **Length:** ~76 min — the strongest input of the batch

**Core claims**
1. **The three-question law** — every sentence must pass: **Can I visualize it? Can I falsify it? Can nobody else say this?** Three nos = rubbish; three yeses = onto something.
   - *Visualize:* concrete beats abstract (you remember "charging pitbull", not "better way"). If you can't see it, it isn't there yet. Zoom-in drill: abstract at top of the page, keep rewriting down until you hit a concrete object (recover fitness → couch to 5K).
   - *Falsify:* a true-or-false sentence puts your head on the chopping block — ears prick up. "He reads on the tube" beats "he's intelligent". **Don't talk, only point** (point at the graph, the castle, the speedometer) — get off the adjective trail.
   - *Nobody else can say it:* "Never write an ad a competitor can sign." Differentiation is a copy act (Volvo speedometer jab; New Balance: "worn by supermodels in London and dads in Ohio"; the Premier League striker who outsold Beckham by becoming "the Secret Footballer").
2. **One Mississippi, two Mississippi**: if the idea doesn't land in 2 seconds, it's wrong. And judge in reality, not in Photoshop — look at the ad surrounded by 7 others.
3. **Before writing: current attitude → desired attitude** (Henley); two telephone poles, you string the wire. Three pieces: (1) who you're talking to (Snapchat's $7M Super Bowl ad to a 39-year-old audience), (2) you must have something to say (a real belief), (3) say it well.
4. Great ads lose elements, not add them (The Economist: no logo, no image — the headline *is* the ad).

**AMK-applicable tactics — this becomes our copy law**
1. **Pre-send gate (cold messages):** run all three questions + the 2-Mississippi test on lines 1–2 of every cold message. Line 1 is what shows in the WhatsApp preview — it must be visualizable and falsifiable. Our current openers already do this ("afriqlabo.com est référencé sur Google — mais le domaine ne s'ouvre plus") — formalized and made mandatory.
2. **Concept hero headlines:** kill every abstract hero ("Votre santé, notre priorité", "l'excellence au service de…"). Replace with the prospect's own falsifiable fact (YAKS: 6 000 F consult → "Consultation à 6 000 F, résultats en ligne" beats any slogan). Applied to AMK-DESIGN-SKILLS §11.
3. **Point, don't talk:** every claim in a concept or message gets an artifact — the screenshot, the price, the count, the map. "Réservez vite" → "répondez « oui »".
4. **Competitor-sign test** on every headline of every concept: if the clinic next door could paste it on their site unchanged, rewrite it.
5. **Enemy positioning** (never a named competitor — standing rule): our enemy is already "the template site with another business's name" [see playbook]; Harry's framing validates it — make the enemy concrete in copy ("un site modèle avec le nom d'une autre clinique").

**Contradictions:** our existing sign-off line "AMK – Développement Web & Solutions Digitales" and some soft closers ("sans engagement", "une minute") are non-falsifiable padding — the video would cut them. **Recommendation:** keep signature + the one-minute reassurance (Cameroon trust economics: a stranger asking for a reply needs the no-risk frame), but ban them from line 1, ban a second padding line anywhere. King decides if we keep "sans engagement" (I recommend keep — it lowers the ask, works locally).

**Junk filter:** none meaningful — the ad archaeology is UK/US but the rules transfer 1:1. Note the YouTube title says "2025/2026" variously; content is evergreen.

---

### [6] 17 Sep 2026 · Alex Nafia-Holland (Relume channel) — "14 Years of Copywriting Knowledge in 1 Hour"
**Link:** https://youtu.be/LzpWg1JQz9s · **Field:** Marketing / Niche · **Length:** ~60 min

**Core claims**
1. **Cooking analogy**: ingredients (customer intelligence) → process (frameworks) → presentation (words). Most copy/AI tools only do presentation; smart ones do frameworks; almost nobody does ingredients.
2. **Ingredients = 6 fields from customer interviews** (Jennifer Havis model): *struggle* (pains), *solutions* (actual use cases), *hesitations* (worries), *awareness levels* (what they compare you to), *differentiators* (why they chose you), *success* (business + emotional outcomes — "get your weekends back" beats ROI). Interview 10–15 customers, framed as "product feedback", no bribes.
3. **The default competitor for most people is Google Sheets and WhatsApp** — plus "no product at all", who must be convinced to pay for the first time.
4. **Homepage ≠ sales page.** A homepage explains the product and walks through the experience; it does not hard-sell — visitors arrive at every stage of the journey. Ads point to dedicated sales pages.
5. **They are comparing you to 5–10 products simultaneously** — write as if the reader has 10 tabs open; the pain section's job is to close the other tabs. Problem 1 = for non-users; problems 2–3 = for users of a bad alternative.
6. **Testimonials: no wall of love.** Drop one at a time; best sequence = make a bold claim, back it with a quote. **Golden rule: if the headline could be pasted onto a competitor's page, it's a bad headline.**
7. **SEO where it belongs:** FAQs (long-tail keywords, shameless, in accordions) + kickers/eyebrows (small text above a headline, styled to carry the keyword while the headline carries the value). Never compromise the conversion narrative for keywords. Also: ticks convert better than custom emoji icons.

**AMK-applicable tactics**
1. **The WhatsApp-default line is our strongest strategic reframe:** in Cameroon, a clinic's real competition online is a Facebook page and a WhatsApp status — not another website. Use in qualification and in the close: *"Vos patients ne vous comparent pas à un autre laboratoire — ils vous comparent à une page Facebook."* (Folded into playbook v2.1 Part H; the Labo/JOSS messages already embody it.)
2. **Claim → proof pairs** in concepts: each bold claim gets the prospect's own real number or a verbatim comment immediately underneath (not a testimonial carousel).
3. **Ingredient harvest for delivered clients:** the 6-field interview (struggle/solutions/hesitations/awareness/differentiators/success) becomes the onboarding call script — 3–5 of the client's own customers, voice notes OK. This is the paid-work version of [4].
4. **Kicker/eyebrow + FAQ accordion** as the SEO add-on we can sell later (client's GBP + FAQ long-tails) — zero design cost, real ranking surface.
5. **Awareness split in concepts:** hero speaks to the low-awareness majority (what it is, plainly); the FAQ/section 2 handles the high-awareness buyer's technical questions (exact services, hours, payment).

**Contradictions:** #6 says homepages shouldn't hard-sell; our concepts deliberately anchor price + RDV above the fold (working for our market — the "appointment now" culture). **Resolution proposed:** keep the above-fold RDV CTA (mobile-first, WhatsApp culture) but move *price* proof out of the hero when it isn't the prospect's differentiator — price belongs with the claim it proves. Not applied yet: queued for the next concept build; King to confirm.

**Junk filter:** Webflow-specific build steps, logo-row advice ("don't use Apple/Microsoft — use smaller brands") is B2B SaaS; our equivalent = the prospect's own real logos/partners — and the "use ChatGPT to rank keywords" step (we do it manually). Both dropped as process detail, kept as principles.

---

### [7] 17 Sep 2026 · Alex Hormozi — "After Closing 4000+ Sales, I Discovered a New Method to Close Deals Faster"
**Link:** https://youtu.be/RVbvhPGFi6E · **Field:** Sales / Objections · **Length:** ~35 min

**Core claims**
1. **Reframing = the 1–3 sentences you say after a prospect says anything but yes**, to raise the odds that your next sentence lands. **The 3A framework:**
   - **Acknowledge** — say their words back ("so you're curious about our certifications"). Two jobs: shows listening, and buys you 2–3 seconds to think.
   - **Associate** — label the question as the behaviour of your best customers ("that's a question our best clients ask; it means you're making a serious, rational decision"). The label becomes something they then live up to; bring it back at the close.
   - **Ask (attack the frame)** — ask a question *about their question*: "which certifications were you looking for specifically?", "what would it take to say yes?", "what are you most afraid of?", "what would make this a no?"
2. **The person asking questions controls the conversation.** Beginners answer questions and hand the prospect the role of judge/jury/executioner over an answer they never specified. "Do you have any questions?" is the worst question in sales — you're inviting objections and handing over the wheel.
3. **Prospects believe almost nothing you say and almost everything they say.** Don't tell them they're a good fit — breadcrumb them with questions until *they* say it.
4. **Five rules:** (1) breadcrumb, don't assert; (2) **never disagree with a prospect** — you can never win a sale by winning an argument (be "smoke": un-punchable, always side-shifting); (3) **tell them what their question means** (the associate step, zoomed in: "clients who shift to us usually already have an advisor — it means you'll be up the learning curve"); (4) **use straw men for tough truths** — a third-party foil (a person earlier today, a past customer, the prospect's own authority) so the harsh truth isn't aimed at them; (5) **retain childlike curiosity** ("huh… that's interesting, can I ask more about that?") with smile and tone doing the work.
5. **Ethical frame:** state the facts, tell the truth — and if the prospect is qualified, you have an obligation to keep asking until they make a decision. "You don't close sales by being right; you close by making the prospect right."

**AMK-applicable tactics**
1. **The 3A script for our four objections** (text/WhatsApp-adapted, short sentences because it's typed):
   - *"C'est trop cher"* → Acknowledge: « Je comprends — c'est un vrai budget. » Associate: « C'est la question que posent les clients qui comparent sérieusement. » Ask: « Qu'est-ce qui vous ferait dire que ça vaut le prix : plus de patients qui réservent, ou moins d'appels au secrétariat ? »
   - *"Je vais réfléchir"* → « Bien sûr. Pour réfléchir utilement : quels sont les deux points que vous voulez trancher ? » / « Qu'est-ce qui vous ferait dire non ? »
   - *"On a déjà une page Facebook"* → Associate: « C'est exactement ce que nous disent nos meilleurs clients au départ — la page marche, mais elle ne prend pas les rendez-vous la nuit. » Ask: « Combien de patients vous écrivent le dimanche, sans réponse ? »
   - *"Je dois en parler à mon associé/épouse"* → Acknowledge + Associate (« c'est la réaction des gens sérieux ») + Ask: « Sur quoi pensez-vous qu'il/elle serait d'accord, et quel point pourrait le/la bloquer ? » (name the parts — they'll tell you the real objection).
2. **Never answer a question we're not sure of** — instead: « Bonne question. Avant que je réponde : vous cherchez surtout X ou Y ? » This is safe in writing, keeps control, and prevents us from inventing a fact (accuracy law).
3. **Ban the sentence "Vous avez des questions ?"** in every call/FU — replace with a specific question ("Qu'est-ce qui vous ferait dire oui ?").
4. **The label bank:** « Ça, c'est une question de quelqu'un qui prend ça au sérieux. » / « C'est la question de nos meilleurs clients. » Use once per conversation, and echo the label at the close (« comme quelqu'un qui veut faire le bon choix pour ses patients… »).

**Contradictions — flagged and resolved:** the **straw-man device invites fabricated third parties** ("someone earlier today asked the same"), which collides with our accuracy law. **Rule adopted:** straw men are allowed **only with true references** — a real past client, a real quote from the prospect's own reviews, a real story that happened. Never invent a person. (Logged as an AMK amendment, not a silent edit.)

**Junk filter:** the acquisition.com upsell interludes; "seducing/hard-truth" language framed for phone/Vegas close culture — softened for a WhatsApp-first, reputation-driven Douala market where the network is small.

---

### [8] 17 Sep 2026 · SaaS Academy — "The Secret To Alex Hormozi's Sales Success"
**Link:** https://youtu.be/ZIJAuw64nY4 · **Field:** Sales / Ops · **Length:** ~25 min (conference talk)

**Core claims**
1. **The CLOSER framework** — every step must be phrased as a **question**, never a statement (prospects can answer questions instantly; statements force them to think and stall):
   - **C — Clarify** why they're here: "What's your goal? Why is that important to you? What would 12 months from now look like if this worked?"
   - **L — Label** the problem: "So what I'm hearing is you've done X, Y, Z and the missing piece is… Is that right?"
   - **O — Overview the pain** (the pain cycle, repeat until they have nothing left, then recap).
   - **S — Sell the vacation** — three 30-second stories illustrating the missing link (e.g., fitness = training + nutrition + accountability). "You were missing one of these three."
   - **E — Explain away their concerns** — only three objection types exist: **price, stall, decision-maker**. For the decision-maker: lean on past agreements ("your partner already knows you're dealing with this"). Walk them through a **yes/no decision chain**: Do you like us? Do you like the product? Do you believe it can help? Do you have access to the money?
   - **R — Reinforce the decision** — immediately after the yes: founder video, personalised confirmation, card/T-shirt — make their feet hot so they don't back out.
2. **Always make the ask.** "You can never make a sale you never ask for." Closers ask the most times — and reframing (video [7]) is what lets you ask repeatedly without burning rapport.
3. **Team management (the second half):** record every call; daily huddles to share testimonials; weekly 1:1 reviewing best/worst/average calls; cut the bottom 10% regularly (claimed +30% productivity); leaderboard + 6-week team competitions (3-person teams, ~25% of a month's pay per prize).

**AMK-applicable tactics**
1. **The yes/no decision chain becomes our pre-close checklist** in WhatsApp form, asked one at a time: « Le concept vous plaît ? » → « Vous pensez que ça peut vous amener des patients ? » → « Vous avez la première moitié disponible maintenant ou fin de mois ? » Three yeses = the close is administrative, not a leap.
2. **"Sell the vacation" → our three-part missing link** for clinics/schools: (a) a site that works on the phone, (b) WhatsApp as the intake/booking channel, (c) being findable when searched. Most have one or two; the offer is the third. Three 30-second stories as proof (a real clinic, a real school, the prospect's own numbers).
3. **Reinforce-the-decision sequence** (fits our existing handoff video): on « oui », within the hour: a short voice/video note from King, the personalised confirmation with their business name, and the first deliverable date. This is the anti-buyer's-remorse step we were doing informally — now it's a rule.
4. **One objection taxonomy only: price / delay / decision-maker.** Simplify the CRM objection log to these three; everything else gets mapped to one of them. (Real Cameroon additions found in practice: trust (« est-ce que vous disparaissez après paiement ? ») → map to price-visibility and decision-maker; note as a 4th local variant, kept separate from the framework.)
5. **Weekly self-review (solo version of the 1:1):** Friday, re-read the week's best/worst exchange and write one line each in `sales/swipe/` — the solo operator's version of the call-review cadence.

**Contradictions:** "cut the bottom 10%" and leaderboards are team mechanics — irrelevant to a solo operation today; kept in the register as future hires playbook, not in the playbook itself. The deep pain-cycle "until they have nothing left" conflicts with our **no-chase rule** (M+2/+4/+7 then stop) — our rule (King's standing instruction) wins; the pain cycle is capped at the discovery conversation, never the follow-up sequence.

**Junk filter:** Vegas/Bahamas incentive economics; "kid trying to write with a permanent marker while closing her credit card" war stories; the sales-team management half (record/Gong, comms cadence, comp) — parked for when AMK has people.

---

### [9] 17 Sep 2026 · JavaScript Mastery — "The Engineering Skill AI Won't Replace" (AI Can Build Your App. It Can't Engineer It.)
**Link:** https://youtu.be/Vok_nReMFaU · **Field:** Build / Engineering · **Length:** ~15 min

**Core claims**
1. **AI builds decay by default.** Every feature added without engineering discipline makes the next one harder: missing pieces, silent breakage, duplicated logic, regressions — "nothing is holding the project together." That is an engineering problem, not a prompting problem.
2. **Give it a plan, not a wish.** Requirements before code: what's in v1, what's explicitly out, in what order, what depends on what. Changing a line in a plan is free; changing a decision already spread across the codebase is a rewrite.
3. **Name the provenance of every value.** For each total, date, status a feature must show or compute, write down where it comes from. **Any value with no source is a decision nobody made** — and the correct move is to stop and decide, not to invent.
4. **Decisions must be explicit and in writing** — recommended option + the honest alternative with the reason it lost; secrets never in code; defaults that hold: monolith first, relational DB, paginate every list, rate-limit public endpoints.
5. **State lives in files, not in chats.** Context files (stack, commands, conventions) keep every new session from guessing and drifting into three styles; they must be lean, per-area in a monorepo, never overwrite human-written docs, and be re-synced against what the repo actually shows.
6. **"It works" is a lie until verified.** Green tests only prove what the AI thought to test. Four separate verification jobs: **check/verify** (drive the real feature, click the flow, against the plan's criteria), **test** (what a caller relies on), **review** (read the diff on a different model than the one that wrote it), **document** (changelog from the actual diff, not from memory). Match effort to risk: a prototype self-checks; a payment system runs all four.
7. **Debugging with discipline:** reproduce reliably → narrow to the smallest failing spot → **form one theory and test that one thing** → if wrong, throw the change away → fix the cause, not the symptom → write a test that fails without the fix → hunt the same mistake elsewhere. If the bug is a bad decision rather than a coding error, say so and redesign instead of patching.

**AMK-applicable tactics — folded into `AMK-DESIGN-SKILLS.md` §18**
1. **Concept spec before build (one page, in the dossier):** who it's for, what's in v1, what's explicitly out, order. Our `build_yaks.py` already worked this way implicitly; now every concept starts with the spec written down.
2. **Value provenance pass (pre-ship):** every number/price/hours/stat in a concept traced to a source — research file, real price, or the explicit DEMO label. Anything untraceable is either sourced or removed. Direct reinforcement of the accuracy law and the fake-number rules.
3. **Verification ladder, matched to risk:** concepts (marketing surface, reputation risk) = static checks + greps + mobile click-through on King's phone; **client deliverables (money risk) = all four jobs**: drive every flow, test the WA/tel/mailto links, review the built HTML (fresh pass, different eyes/model than the builder), document the diff.
4. **Regression checks that persist:** every bug fixed adds a grep/test to the QA script so it cannot quietly come back (we did this with the OraCare/YAKS leftover greps — now it's the rule).
5. **Context files:** our equivalents already exist (`sales/Pipeline-Status.md`, dossiers, READMEs, session memory) — the discipline added is: update the file at the moment of the decision, not at the end of the day.

**Contradictions:** none. The "stop and ask a human when a value has no source" mechanic is exactly what the accuracy law already demands; this gives it a mechanical trigger.

**Junk filter:** the Agentic Engineering course launch (Sept 22) and skill names (scope/architect/develop/audit/sync/check/test/review/debug); tools specifics (Claude MD conventions). Kept only the workflow principles — our stack is Python builders + single-file HTML, not agentic app scaffolding, so the folder mechanics don't transfer.

---

### [10] 17 Sep 2026 · Y Combinator (with Raphael Schaad) — "Design Experts Review Vibe Coded Websites"
**Link:** https://youtu.be/DNSXlBmukck · **Field:** Design · **Length:** ~45 min

**Core claims**
1. **The AI-design tells are now a credibility tax.** Purple gradients everywhere, animation for animation's sake, decorative lines following the scroll, cursor-chasing buttons, meteors, fade-ins — "if it looks like a bunch of other things I've seen, customers assume you vibe-coded the product too."
2. **Specific failures found in the review:** hover effects that make nav items *fade out* (opposite of invitation); hover-locked essential information (no hover on mobile → undiscoverable); scroll-jacking ("like molasses", you lose your place, scroll indicator fails); fade-ins that leave sections seemingly empty (an FAQ caught mid-fade looks like one lonely question); 4–5 mixed type styles in the hero adding vertical space without hierarchy; buttons that move (can't be clicked); emoji/standard-icon tells; blurry assets; low-contrast light text; "10x everything" empty claims with enormous whitespace; fake dashboards with the classic red/green/blue/purple Google-colour callouts; bento boxes as a non-original default.
3. **The counter-patterns:** hover should *invite* the click (pop, one shade lighter, subtle glow, cursor hand is already free); a hover that reinforces meaning is the good kind; **the H1 answers what it is, who it's for, why care + a CTA above the fold**; start from **your own brand palette** and feed that in, instead of accepting what the model spits out; **you are the editor** of every suggestion — "just because it's easy doesn't mean it's worth doing"; QA everything yourself; a landing page is a **customer acquisition channel**, not the product.

**AMK-applicable tactics — folded into `AMK-DESIGN-SKILLS.md` §3.8**
1. **New hard bans:** scroll-jacking, hover that hides/de-emphasises, essential info behind hover, moving buttons, entrance animations that hide content, decorative scroll-following lines, emoji as icons, mixed type styles in one header block.
2. **Brand-palette-first is now the build order:** derive the palette/type from the client's own logo/signage/research *before* generating any layout (YAKS and the Labo storefront work already do this — now it's the documented first step) — never accept a default palette.
3. **The editor rule:** every generated element must survive "would a designer have chosen this on purpose?" — if it exists only because it was easy, it's cut. This formalises what our anti-slop §3 already does; the YC list becomes the concrete examples.
4. **Hover audit** added to the pre-flight: every hover state either invites a click or reinforces meaning; zero hover states that hide information; every hover-revealed element also reachable without hover (mobile has none).

**Contradictions:** our §17 pattern vocabulary *lists* bento as a layout pattern; the video calls bento (3×2 icon-text grids) a non-original default. **Resolution:** bento stays allowed when the content is genuinely modular (exact cell count, interlocking spans — already required in §3.3), but the "icon + text ×6" bento card grid is banned as a section default. Logged, King can veto.

**Junk filter:** none — the claims are design fundamentals with concrete evidence from live sites. The YC-startup context (fundraising pages) doesn't change the rules for clinics/schools; if anything they matter more, because our clients compete on trust.

---

### [11] 17 Sep 2026 · Sajid — "The Easy Way to Design Top Tier Websites"
**Link:** https://youtu.be/qyomWr_C_jA · **Field:** Design · **Length:** ~12 min

**Core claims**
1. **Creativity is a process, not a moment** — connect existing ideas; nobody designs from a blank slate.
2. **Rule 1: good design is as little design as possible.** Don't start at the header / the section count / the button styles — start from the page's **key functionality** (for many sites: heading + input + button). Chances are that's all it needed.
3. **Rule 2: similarity & proximity** (Gestalt) — group with shape/size/colour/spacing; the page must be understood as a whole within seconds (scannable).
4. **Rule 3: elements need more spacing than you think** — start generous, then bring related elements closer.
5. **Rule 4: use a design system** — spacing values divisible by 4, rem units (px/16), all as CSS variables; ~1 font + type scale; a dark and light for text/background plus two for personality; **no science in colour psychology**; avoid centred paragraphs; line-height inverse to font size; two button types (primary/secondary).
6. **Rule 5: hierarchy is everything** — emphasise with size/weight/colour but start small; often you must **de-emphasise competing elements** instead; finish by zooming out to test whether the key element wins.
7. Exceptions/additions: depth via colour + shadows (shadows can replace borders), accent colour to highlight, subtle gradients over flat fills, cards for bland content.
8. The **process**: know the basics → collect inspiration (top sites, Figma community) → work the ideas over in your head → **step away** (new ideas arrive on return; if they don't, you're stressed or short on sleep) → don't fall in love with your design (test with friends, then users) → ship something.

**AMK-applicable tactics — folded into §19.1, §19.2, §19.4 + WORKFLOW stage 3b**
1. Build order for every concept: **key functionality first** (e.g. heading + WhatsApp CTA block), then outward. Kills the "design the header for an hour" trap.
2. **Spacing-first method** with the 4-divisible scale (our token sheets already use 4/8) — start generous, reduce with intent.
3. **Zoom-out test** in the pre-flight: at 25%, the primary element must win.
4. The 5-step inspiration process, with "step away" now legitimate: when a direction stalls, park it and return — it's part of the process, not procrastination.

**Contradictions:** none; it sharpens what §2 (dials), §6 (colour), §7 (layout) already require.

**Junk filter:** the Mobbin sponsorship segment (the pattern library is useful but paid — we already have the vendored registries, keep those); the "read these books" list (already in our sources culture).

---

### [12] 17 Sep 2026 · Self-Made Web Designer — "Give Me 7 Minutes & Your Web Design Skills Will Take Off"
**Link:** https://youtu.be/1NTKwpAVcHg · **Field:** Design / Conversion · **Length:** ~9 min

**Core claims**
1. **The F-pattern is bogus** — outdated designer folklore; forcing attention along a path makes people miss content. Use **visual hierarchy**: most important = biggest + boldest; turn the volume down on everything else; CTAs need high contrast (the main job is the click).
2. **Stop using ghost buttons** — outline-only buttons are invisible and don't get clicked (with a caveat that our third-tier ghost usage is deliberate).
3. **Colour:** brand-matched palette; accessibility first — check contrast (Coolors Contrast Checker); **60-30-10** (60% dominant neutrals, 30% brand, 10% accent for CTAs).
4. **Typography roles:** H1 biggest/most prominent (what the page is about), H2s divide the page and guide attention, body text stays readable (never decorative).
5. **Good design without conversion is useless to clients** — the cautionary story: a beautiful relaunch that dropped sales. Conversion = **clarity + scannability + motivation**, and **design for the audience — not yourself, not the client**.
6. Keep learning: "AI won't take all jobs — it will take lazy ones."

**AMK-applicable tactics — folded into §19.1, §19.2, §6, §5, §8**
1. **Conversion-first law** written into §19.1 with the anti-story (pretty ≠ paid).
2. **60-30-10** added to §6.1 — with our "one accent" rule this now quantifies how rare the accent must be.
3. **Ghost rule refined** in §8: primary is always solid; ghost lives only as a third tier beside a filled primary, contrast-checked.
4. **Line-height inverse to size** and **no centred paragraphs** added to §5.
5. Persona walks (already in §13 pre-flight) now explicitly mean **audience, not client or self** — matters when a client asks for a look their patients won't use.

**Contradictions — one, flagged and resolved:** §8 allowed a ghost/tertiary tier; this video says stop ghost buttons. **Resolution:** the primary action is never outline-only (adopted); tertiary ghost stays because our design system uses it sparingly next to filled primaries and our contrast rule already forbids invisible ones. King can veto the tertiary tier.

**Junk filter:** the funnel/community pitch; nothing else.

---

### [13] 17 Sep 2026 · Build Great Products — "Still Vibe Coding AI Slop? Here's How to Create Actually Beautiful Websites with AI (Genspark)"
**Link:** https://youtu.be/ced7C5d7p08 · **Field:** Design / Build · **Length:** ~22 min

**Core claims**
1. **AI slop = whatever the agent reaches for by default**: either purple/blue gradients with glow, or the "Claude" beige/brown/orange family — plus generic sans and over-rounded UI.
2. **What the vibe-coded look signals to customers:** you didn't spend effort → you may not be trustworthy → the product is amateur → "why should I care?". And AI copy tends to be **wordy copy about the product** instead of messaging the customer actually cares about.
3. **Design is a growth lever, not decoration** — his example product made $25k/month while looking bad; better design unlocks more of the same demand.
4. **The fix is a process:** explore **3 design directions** *before* building, specifying audience, aesthetic references, an explicit **avoid-list**, colour direction, type direction, hero approach, data-viz prominence, and scope (hero + one supporting section, not the whole site). Then iterate variants of the winning direction (fonts, accents), rewrite headlines **outcome-led**, build the full page, and extract a **design-system file** to reuse everywhere.
5. Outcome-led example: "For organic traffic you can actually defend" → **"Ship SEO work that measurably moves the needle."**

**AMK-applicable tactics — folded into §19.3 + WORKFLOW stage 3b**
1. **Three-direction rule** is now a pipeline gate: no concept build starts without three explored directions and a locked winner.
2. The **avoid-list** is written into §19.3 for reuse in any generation prompt (fits our §3.8 bans).
3. **Outcome-led headlines** reinforce the H1 contract (§11b) — for clinics/schools: "Des rendez-vous qui n'attendent pas le lundi" beats "Site web pour clinique".
4. The **design-system file** maps to our `design/STYLE-TOKENS.md` + builder `:root` block — already our practice; now explicit that the *winner* seeds it.

**Contradictions:** none.

**Junk filter:** Genspark itself and the AI-video feature (tool marketing); the Product Studio course pitch; "download this HTML" workflows tied to their platform. Principles kept, tool dropped.

---

### [14] 17 Sep 2026 · The Next Wave — "How to Vibe Code a Designer-Level Website in 28 Minutes" (with Munk Toad)
**Link:** https://youtu.be/UNqRlRz80Ss · **Field:** Design · **Length:** ~30 min

**Core claims**
1. Every AI site looks the same because prompts lack **design vocabulary**; "beautiful" is subjective and resolves to purple gradients. Precision works: **hero / feature / onboarding**, card / list / bento, framing (full-screen vs framed), styling (flat / outline / minimalist / glass / iOS-like), mode (light/dark), **accent colour**, background = accent hue with **reduced saturation + brightness**, border, shadow family, typography (sans/serif/mono/condensed/rounded/handwritten), **font pairing** (display + body), sizing, weight personality (light = refined, bold = forceful), tightened tracking on big titles, animation (fade/slide/scale/blur; sequenced word-by-word; ease-in-out).
2. **The recipe metaphor:** a template is instant ramen (always decent); cooking with the right ingredients is better but needs the recipe. **One good ingredient** (a 3D/blob asset via Spline, an animated asset via Unicorn Studio, a strong reference) lifts a design 10x.
3. **Reference-driven prompting:** attach an image, a Figma frame, or an HTML reference and say "create a website based on this" — the model inherits embedded taste rather than guessing.
4. In the AI era **taste is the differentiator** — the more apps exist, the more sameness, so design is what makes one stand out. "Fewer McDonald's."

**AMK-applicable tactics — folded into §19.5 + §5 pairing + §6 derivation**
1. **Vocabulary-first briefs:** our design-read one-liner (WORKFLOW stage 2) now gets the §19.5 word list for precision — human or AI, the same words.
2. **Font pairing** rule added to §5 (display + body; body carries the reading, never the personality).
3. **Background derivation rule** added to §6 (tints = accent hue, saturation/brightness reduced) — matches our token sheets but now stated as the derivation principle.
4. **The "one ingredient"** rule: allowed only if embeddable (single-file, no external requests) — external 3D/animated embeds parked for the AMK main site.
5. **Instrument Serif flagged** by this creator as an AI-slop signal (we already banned it as a default in §3.2) — our ban stands.

**Contradictions:** none material. His "dark mode often needs no accent" is a preference; our §6 (one accent, 60-30-10) still governs.

**Junk filter:** Aura (his template product) and its prompt-builder as a tool; v0/Lovable/Bolt/Cursor workflow specifics; Tailwind-specific colour cross-matching; the book/QR-code promos.


### [15] 17 Sep 2026 · Nate Woodbury — "How To Make A Marketing Video For My Business"

**Link:** https://youtu.be/y5iegw6wlAg · **Field:** Content / Marketing (video) · **Length:** ~12 min

**Core claims**
1. A promo/marketing video must be **short** (audiences know they are being sold to and guard their attention) and **easy to follow** — simple storyline, show don't tell, get feedback before shipping.
2. **Outcomes beat features**: "the features aren't going to sell it — what's the outcome/benefit? How is their life going to change?" Features get mentioned quickly; the majority of the video is the outcome.
3. Use **customers and their results**, and **testimonials as soundbites** — find the 5–10 s moments, never play the whole interview.
4. **Script, refine, polish** promo videos (do not just hit record); the flagship asset deserves disproportionate effort (his own example: months on one 5-min video).
5. A **promo video belongs on your website / landing page** (hosted unlisted), not fed to YouTube hoping for virality. The viral path is *other*, search-driven "leaf" videos that build the relationship first — his **3-video formula**: relationship video #1 → #2 → then people choose to watch the promo.
6. **Paying to push a promo = paying to annoy** — people skip ads; you buy low-quality leads that cost more to filter than they return.

**AMK-applicable tactics**
- **T-15a — Build the flagship promo asset.** One 60–90 s bilingual AMK promo/explainer (what we do, who we serve, outcome, PREVIEW CTA), hosted unlisted, embedded on `amk-cm.vercel.app` and reused in proposals. It is a *different asset class* from the short-form series — see conflicts. → candidate **V-13**.
- **T-15b — Outcome-over-features gate** in every script header: features may be a minority of the beats; the outcome must carry the majority. (#2–#4 already pass; now it is written.)
- **T-15c — Clarity gate before render:** (1) does it say what we do, (2) who we help, (3) which outcome, (4) what emotional journey it takes the viewer start→middle→end?
- **T-15d — Testimonials as soundbites** once we have consent: 5–10 s verbatim under the claim it proves (ties to [6]'s one-quote rule).
- **T-15e — Polish = our pipeline**, not hiring out: §19 three-direction work + §13 pre-flight + QA, aimed hardest at the flagship asset.

**Contradictions**
- "Promo videos don't belong on YouTube" **vs** our TikTok→Shorts mirroring strategy. **Not a true conflict:** his split is *leaf/search videos* (YouTube-native, relationship) vs *promo* (landing-page asset). Resolution: mirroring continues for the educational series; the future flagship promo gets unlisted hosting + site embed. No King ruling required.

**Junk filter:** the videographer-hiring advice and the 4-months-per-5-min scale (AMK is the producer); his course/upsell mentions.

---

### [16] 17 Sep 2026 · Brooklyn Social — "How To Make High Converting Videos For Your Business"

**Link:** https://youtu.be/_znL3ofhkFE · **Field:** Content / Marketing (video) · **Length:** ~5 min

**Core claims**
1. **First 3 seconds decide**: a question or a bold statement; never "hey guys, today we're going to talk about…"; speak to **one person**, not an audience.
2. **Understand the audience** — their pains, and always answer "why should someone care about this?"
3. **Get right to the point** — no filler, no rambling; busy people swipe.
4. **Always a clear CTA** — direct the viewer somewhere.
5. **Lighting and audio are not optional** (window light, tripod, clip-on mic); claims bad lighting stops the algorithm pushing (unverified — see rejected).

**AMK-applicable tactics**
- **T-16a — 3-second hook gate (written):** line 1 of every script = a question or a specific, aimed at **one** person (a clinic owner, a school proprietor) — never a self-introduction. Our #2–#4 hooks already pass; the gate now exists in the script template.
- **T-16b — "Why should someone care?" line** required per beat before a script is approved.
- **T-16c — Zero-fluff pass:** read aloud, delete filler — reinforces copy law [5].
- **T-16d — Clear CTA in every video** — this independently confirms the PREVIEW closing-beat mandate.
- **T-16e — Our version of "good lighting/audio":** frame contrast/readability checked on a phone-sized canvas + music ducked under narration (handover §6). We never shoot live video; the transfer is legibility + clean mix.

**Contradictions**
- "Get your team and your face on camera / share behind the scenes" **vs** our **no talking-head** fingerprint. **Adaptation, not adoption:** behind-the-scenes becomes *build footage* — screens, hands, craft, scroll/tap/load (our V-10 format). The host + real websites remain the fingerprint.

**Junk filter:** the agency pitch, the free checklist, "book a call"; the **78 % (Sprout Social)** stat — US, unverifiable in our market, and we never quote unverifiable stats (accuracy law); the algorithm-punishes-bad-lighting claim.

---

### [17] 17 Sep 2026 · Digital Canva Mastery — "How to Create Free 2D Animated Explainer Videos for Your Business using Canva"

**Link:** https://youtu.be/QsQhaatwSnU · **Field:** Content / Production · **Length:** ~4 min

**Core claims / method**
- Three components: **script → animation → voice-over**. Their stack: ChatGPT (script) → Canva (animated elements, "filter: animated only" to save time) → ElevenLabs (voice) → "pop" entrance animation + "match & move" transition between beats → manual element motion → brand name/CTA → export MP4.

**AMK-applicable tactics (only two, both micro)**
- **T-17a — Element entrance/transition vocabulary** for our own PIL/FFmpeg renderer: **pop-in** for labels/numbers, **match-and-move** for the same element growing/moving between beats (keeps visual continuity). **Constraint:** never animate the demonstrated UI itself (anti-slop §3.8 — no moving buttons while being explained). Titles/labels only.
- **T-17b — Three-component pre-flight** (script → visuals → voice) formalised in the script header, matching our existing pipeline.

**Verdict:** the tool stack is **rejected** — template animation cannot show **real websites** (our hard requirement), it produces exactly the generic look King banned, and our house pipeline already does script→visuals→voice with the real pages. Only the two micro-techniques above are absorbed.

**Junk filter:** the ChatGPT/Canva/ElevenLabs workflow as a method for AMK; the agency-ad framing; "free" tooling claims.

---

### [18] 17 Sep 2026 · The Website Architect — "Everything About: Footers In Web Design"
**Link:** https://youtu.be/T5BACF2goFU · **Field:** Design / Build (footers) · **Length:** ~13 min

**Core claims**
1. Footers have **two uses**: a last resort to find content that is not in the primary navigation (contact, careers, rarely-used pages) and a **second chance to convert** the user. Every website needs one; skipping it ("we're too trendy") damages UX, conversions and SEO.
2. **Three types**: normal (identical site-wide) · **infinite-scroll / mini** footers (placed in the sidebar because a feed never ends, e.g. LinkedIn) · **contextual** (content changes by page or by signed-in state, e.g. Medium).
3. Design depends on site size: for small/medium businesses he uses a **4-column layout + bottom strip** — (1) logo + 2–3 sentence company blurb (the "too long, didn't read" of the business); (2) links: primary nav **plus the pages that didn't make it** — the term is **doormat navigation** (first thing you see on arrival, last thing when you leave); (3) more **CTAs** (services/products) because footer readers are interested; (4) **contact info** (email, location, phone, socials) — a standard ~80% of sites follow.
4. Making footers more useful: **clearer link labels** (not "Resources" → "Blog"/"Articles", citing NN Group on vague labelling) · **3–6 awards** for credibility, modest in size (overdoing it looks like compensating) · an Instagram feed **only** if the account genuinely posts well (adds complexity + speed cost; FB/Twitter feeds look outdated) · a **newsletter signup**, which users now expect in footers.
5. **Evidence he cites**: SuperOffice added CTAs to the footer → **+50%** conversions on the goals placed there; Smart Insights / **Radley London (2012)** swapped a one-line footer for a "mega footer" with product categories → **+24% sales** — with his own caveats (the footer may have been above the fold; results vary with homepage height; and Radley later **reverted** to the old footer).
6. **SEO**: footer internal links raise CTR (an SEO factor); the footer is a prime **E-A-T** location (phone, physical location, email, socials, awards, contact/support, privacy); footer weight differs by page (contextual footers make the homepage footer worth another look). **Black-hat warnings**: hidden/faded anchor text (Google's own guidelines name it) and agency credit links — a **keyword anchor** ("web design toronto") is penalisable, a **plain brand credit** ("Website designed by X") is fine; if your company name looks like a keyword, don't link back at all. Closing rule: common sense — if it feels unnatural or manipulative, don't.

**AMK-applicable tactics — folded into §20 (+ §13 gate)**
1. **Footer anatomy adopted for every concept**: brand+line · doormat nav · CTA · contact, plus strip. The 2–3 paragraph blurb is trimmed to **one sentence** (mobile cost).
2. **Doormat nav** = the concept's own section anchors, labelled with the destination; "Ressources"-style labels banned.
3. **Footer CTA = the hero's action** (WhatsApp), never a new offer.
4. **Contact cluster in the footer** (address + landmark + hours + phone) — serves both E-A-T and the real patient at 22:00.
5. **Credit-line rule**: brand text only, never a keyword anchor; text-only on client sites until they agree to a link.
6. **Bans added**: hidden/faded anchors, vague labels, version/fake-live strips.

**Contradictions:** the +50% / +24% figures are single-source, one is from 2012, the creator himself flags the caveats and the company reverted → **not quotable** under our accuracy law (kept as internal calibration only, rejected as pitch material in §5). Instagram/Facebook feeds and newsletter signups conflict with the single-file/no-external-request rule and with WhatsApp-first → parked in §20.5.

**Junk filter:** Pinterest as "the best" footer-inspiration source (our inspiration process is live refs + vendored registries, §19.4); the A/B numbers as marketing ammunition; feed widgets; the affiliate-tool plug at the end.

**Attribution:** The Website Architect (73.1K subs) — footer anatomy, doormat navigation, E-A-T and the credit-link SEO ruling.

---

### [19] 17 Sep 2026 · Flux Academy — "Website Footer Design Inspiration (Best practices in 2024)"
**Link:** https://youtu.be/Dt04HR1lN5Y · **Field:** Design (footers) · **Length:** ~12 min

**Core claims**
1. The footer is the **last thing a user sees** — the split second where they decide whether to close the tab. A copyright line + privacy link "misses a golden opportunity".
2. **Use the full viewport as the canvas** — "it's not a printed brochure", extra depth costs nothing; **generous negative space**; every viewport should look like something you could print and hang.
3. **Repeat the hero's primary CTA in the footer** (Framer, Figma): the same "get started" button, in its own column, with negative space making it the most prominent item; credibility (awards/reviews) sits beside or just above it.
4. **Repeat/expand navigation with large type**: at the bottom the visitor's question is "where do I go next?" — big nav titles encourage exploring more pages (Figma's huge sitemap; a card-wallet store's four typographic columns with clear titles).
5. **Scale contrast + hierarchy**: a huge wordmark or tagline, a medium element (photo/motif), small body links; legal/copyright **fades into the background**.
6. **Micro-delight**: hover/underline-wipe easing and small interactions keep the visitor a split second longer; a **back-to-top** link is useful. Teenage Engineering carries the product's photographic motif into the footer as a literal canvas — motif continuity as the closing statement.

**AMK-applicable tactics — folded into §20.3/§20.4**
1. Footer treated as a **designed screen** with **one scale contrast** (large brand line, bounded on mobile per AMK caveat).
2. **Hero CTA repeated** in the footer (WhatsApp) — now part of the anatomy; legal stays small.
3. **Back-to-top link** adopted for every build.
4. **Column titles** in the desktop 4-column version (orientation).
5. **Motif continuity**: reuse the build's one ingredient in the footer (La Béthanie's real photo, the lab's console, the optician's mirror) instead of adding new assets.

**Contradictions:** the full-viewport footer conflicts with mobile-first → resolved as a **desktop-only** move (mobile footer bounded). Awards/testimonial rows in the footer conflict with the accuracy law → real + permissioned only.

**Junk filter:** the showcase sites as copy targets (we take principles, not layouts); newsletter-for-agency-lead-gen framing; the "you can be generous with depth" line read as permission to pad — our §20.3 caps it on mobile.

**Attribution:** Flux Academy (1.09M subs) — footer as last-screen conversion surface, CTA repetition, scale hierarchy, motif continuity.

---

### [20] 18 Sep 2026 · Pavlo — "How I sell "Talking Websites" to local businesses for 499/mo (FULL Guide 2026)"
*(titre affiché dans la recherche : « Beginners Guide to Building And Selling Talking Websites in 2026 »)*
**Link:** https://youtu.be/sZbv-HbOIDg · **Field:** Build (voice) / Sales (modèle d'offre) · **Length:** non mesurée (transcript en 11 segments)

**Core claims**
1. **A "talking website" = a voice AI embedded in the page.** The visitor clicks a button and *talks* to the site in-browser — no phone call, no download, no leaving the page, works after hours. The AI answers (hours, services, rough price), asks follow-ups, and **books the appointment** straight into a calendar, writing the contact + transcript to a back end.
2. **The money is recurring, and that is the real product.** Setup fee $1 000–6 000 (or $2–4 000 where he leads), then **$500/month**. His claim: a "10/10 static site" cannot command what a "5/10 talking site" can, because the talking site is billed as a service that produces bookings, not as a file that was delivered. For an existing site: paste one snippet, no rebuild.
3. **The pain he sells against:** the average site converts ~2–3 %, so ~97 of 100 visitors leave doing nothing; contact forms are long; nobody answers at 9 p.m.; the visitor calls a competitor who *does* have a system. "I paid for traffic and got nothing" is the owner's real complaint.
4. **Who to target:** high call volume + high revenue per transaction (roofer, cosmetic surgeon, chiropractor) — **and above all businesses already spending on ads.** He finds them with the **Google Ads Transparency Center** and the **Facebook Ads Library**: if an owner already pays for traffic, they already believe in paying for acquisition and are maximally ready to pay for conversion.
5. **Sales move:** don't argue — **run side by side.** Keep their campaign, build a landing page, compare appointments. "If I get you 41 people instead of 40, is $500 worth it?" Free install offered as the wedge.
6. **"12 components of a $10 000 website":** clear value proposition above the fold · multiple contact methods · strong specific CTAs (not "Contact us today") · real high-quality visuals incl. a photo of the owner · reviews/social proof kept fresh · trust signals (years, certifications, payment) · one page per service + per location for SEO · a personal About page (why the founder started) · mobile-first · FAQ · **booking/scheduling right after the enquiry** · bonus: video + exit-intent pop-up.
7. **His stack:** `gofreetrial.com` (GoHighLevel) — knowledge base built by crawling the client's site, a rich-text FAQ field, an AI agent, one snippet to install on any site. WhatsApp integration exists for non-US markets.

**AMK-applicable tactics — folded into §21**
1. **The voice layer as an *addition* to our scripted assistant, never a replacement for WhatsApp.** We already ship a scripted chat assistant (OraCare v1/v3). Voice is a second input/output on the same knowledge base we already write.
2. **The assistant's job is the handoff, not the booking.** In Cameroon the booking channel is WhatsApp, not a calendar. Our equivalent of "books the appointment" = **the conversation ends by opening WhatsApp with the patient's actual question pre-filled** — the same mechanic as our existing `wa.me?text=` links, but now the text is written by what the patient said.
3. **The knowledge base is the site itself.** We already build the FAQ and the preparation rules from verified facts. That content *is* the assistant's brain — no crawler, no new document. Method: every answer must be traceable to a line already on the page.
4. **"Businesses already spending on ads" = a new sourcing signal we have never used** (Google Ads Transparency Center + Facebook Ads Library, free, public). Our sourcing so far = directory presence + measured WhatsApp click traffic. An owner paying for traffic is strictly warmer than an owner merely listed. **This tactic stands on its own even if voice is never built.**
5. **"Run it side by side" is the least-argument sale we have.** We already build concepts for free before a yes. The missing half: **measure and show the before/after** (WhatsApp clicks, calls) — which turns a concept into a demonstration instead of a gift.

**Contradictions**
| Video says | Our standing rule | Resolution |
|---|---|---|
| $500/mo recurring | **Rule 43: 100 000 FCFA one-off, 50/50, never a discount** | **NOT adopted. King's ruling required** → `sales/Voice-Offer-Decision-2026-09-18.md` |
| "Use AI to get you real photos" of the owner / of completed work | **Accuracy law + no invented proof** | **Rejected outright.** Generating a fake photo of a real clinic's team is fabrication. We may never do it. |
| "Average website converts at 2–3 %" as a pitch number | Never quote a stat we cannot verify | Internal calibration only, never spoken to a prospect |
| Calendar booking as the conversion event | WhatsApp-first market | Adapted: the handoff *is* the conversion |
| $97–297/mo US SaaS platform | No USD card, no recurring infra budget, single-file rule | Tier 3 only, and only if a client pays for it explicitly |

**Junk filter**
- The GoHighLevel affiliate funnel: "rated the number one course", `laptopceo.com`, a Zoom onboarding call, "copy everything with a click" — a course sale, not a method.
- "No one is doing it yet" / "the best part is you can do this without a portfolio" — scarcity framing, unverifiable.
- Fabricated proof in the demo (the AI improvising "we use control joints, reinforcements and curing methods" for a company whose real services are unknown).
- Exit-intent pop-ups and auto-rotating review widgets — US desktop habits; on a 390px Cameroonian phone they cost more than they earn.
- The straw-man "old website from 2005 ranked number one" comparison — the point survives (ranking ≠ conversion) but the theatre doesn't travel.

**Attribution:** Pavlo (YouTube, ~130 K subs) — voice as a site capability, recurring-revenue framing, the "already spending on ads" prospecting signal, and the "12 components of a $10 000 website" checklist.

---

## 5 · Rejected (named, with reason)

| Item | Source | Why rejected |
|---|---|---|
| Freelance-platform money path (Upwork/Fiverr, "get paid to write copy") | [3] | Not our business — AMK sells built sites + concepts, not copywriting gigs. |
| Lead-magnet funnels (HighLevel free trial, "attract and repel guide") | [3][4] | US funnel-marketing mechanics; our acquisition is direct WhatsApp outreach + inbound TikTok. |
| US survey stat "31% pay more for reviews" as a *pitch* number | [4] | Not quotable to a Douala clinic; kept only as internal calibration. |
| Reddit / Amazon-reviews audience mining | [1][2] | Low local yield for Cameroon SMB; replaced by the prospect's own FB page + comments (already our practice). |
| "Wall of love" testimonial walls (3-column testimonial row) | [2] | Directly contradicted by [6]: one testimonial at a time, under the claim it proves. [6] wins — closer to our claim+proof structure. |
| Webflow-specific build steps; logo-row "don't use Apple" advice | [6] | Tool- and B2B-SaaS-specific; our equivalent is the prospect's own real partners/FB proof. |
| Custom emoji icons vs plain ticks | [6] | Marginal A/B claim, no local test; not worth a design rule. *(Kept as a note only — ticks are also lighter, but our concepts use inline SVG icons, which is a different thing.)* |
| Sales-team management half (recorded calls/Gong, daily huddles, cut-the-bottom-10%, leaderboards, Vegas incentives) | [8] | Solo operator — no team to manage. **Parked as the future-hires playbook**, not deleted: revisit at first hire. |
| "Pain cycle until they have nothing left" beyond discovery | [8] | Conflicts with King's no-chase rule (M+2/+4/+7 then stop). Our rule wins; pain work stays inside discovery. |
| Fabricated straw-man foils ("someone earlier today asked the same") | [7] | Direct conflict with the accuracy law. Adopted only with **true** references — real client, real quote, real story. |
| Agentic Engineering course pitch + skill/tool names (Sept 22 launch) | [9] | Course upsell; our stack is Python builders + single-file HTML, not agentic app scaffolding. Principles kept, tooling dropped. |
| Genspark / Aura / v0 / Lovable / Bolt workflows, model picks, Tailwind cross-matching | [13][14] | Tool-specific; AMK builds single-file HTML with committed Python builders. Principles (3 directions, avoid-list, vocabulary, design-system file) kept. |
| External Spline 3D / Unicorn Studio embeds | [14] | Break the single-file, no-external-request rule; parked for the AMK main site only. |
| Mobbin (paid pattern library) | [11] | Principle kept (reference libraries); we already have vendored registries + Figma community. No new paid tool. |
| Launch-video auto-generation, course/community promos | [13] | Upsells; our launch content is made deliberately (see `sales/social/`). |
| "Beautiful shadow" / skeuomorphic revival | [14] | Not adopted as default; our shadow rules (§6.1, §8) stay. Noted as a vocabulary item only. |
| Ghost-button absolute ban | [12] | Softened to our precise rule: never the primary action; tertiary ghost allowed beside a filled primary, contrast-checked (§8). Flagged for King's veto. |
| Canva + ChatGPT + ElevenLabs template-explainers | [17] | Cannot show real websites (our hard requirement); generic template look is the banned "generic art"; house pipeline (PIL/FFmpeg + real captures + selected voice) is better for the niche. Only pop-in / match-and-move kept. |
| "78 % prefer learning about a product or service through video" (Sprout Social, US) | [16] | Unverifiable for Cameroon; we never quote stats we cannot verify (accuracy law). |
| "The algorithm won't push videos with bad lighting" | [16] | Unverified algorithm claim; platform claims only from current platform guidance or our own account insights. |
| Hiring an external promo team / months per 5-minute video | [15] | Wrong scale — AMK produces in-house; our "polish" is §19 directions + §13 pre-flight + QA. |
| "Get your team / faces on camera" as a rule | [16] | Conflicts with the no-talking-head fingerprint; kept only as build-footage BTS (screens, hands, craft), never faces-by-rule. |
| Footer A/B numbers as pitch material (+50% SuperOffice, +24% Radley London 2012) | [18] | Single-source, one from 2012; the creator flags the caveats and the company later reverted. Our accuracy law bans unverifiable stats → internal calibration only, never quoted to a prospect. |
| Instagram / Facebook feed embeds in the footer | [18] | External requests + page-speed cost, breaks the single-file rule; our clients don't post consistently enough for it to count as proof. |
| Newsletter signup in the footer | [18][19] | No list to manage and our channel is WhatsApp; newsletter-first framing is a Western agency habit. Parked until a client asks for email capture. |
| Pinterest as the primary footer-inspiration source | [18] | Moodboard, not research; our process is live references + vendored registries (§19.4 / PRE-FLIGHT §2.3). |
| Awards row / press-quote row as a default footer element | [18][19] | Adopted only with real, permissioned proof; the default is to leave the slot empty. |
| AI-generated "photos" of the business owner / of real completed work | [20] | Fabrication of proof about a real client — banned by the accuracy law, no exception. The legitimate version: **generate a mockup of *this site*, never of *their reality*.** |
| GoHighLevel / `gofreetrial.com` as our delivery stack | [20] | USD-billed recurring SaaS ($97–297/mo), needs a foreign card, breaks the single-file rule; nothing it does that we need is impossible in a serverless function we control. Parked, not deleted — revisit if a client pays for it. |
| "No one is doing it yet" / no-portfolio-needed scarcity framing | [20] | Unverifiable and irrelevant to a Douala lab that has never heard of a talking website either way. |
| Exit-intent pop-up + auto-rotating review widget as defaults | [20] | Desktop/ads-driven behaviour; on a mobile-first Cameroonian page the pop-up interrupts the one action we want (WhatsApp). Kept only as a client-paid extra. |
| "Average website converts at 2–3 %" quoted to a prospect | [20] | Unverifiable for Cameroon; internal calibration only (same ruling as [16][18]). |
| Full-viewport footer on mobile | [19] | Scroll cost beats drama on a 390px screen → desktop-only (§20.3). |
| Hidden/faded anchor text and keyword-anchor agency credit | [18] | Named as black-hat (Google's own guidelines) → banned outright in §20.5. Credit lines are brand text only. |
| AEO percentages quoted to a prospect (43 %, 1 in 4, 30 % of AI answers, 1.3 bn clicks) | [28] | Single-source US self-reported data; our accuracy law bans unverifiable stats. **Internal calibration only.** |
| "You will be recommended by ChatGPT" (as a promise to a client or on our site) | [28] | We control neither the models nor their answers. The honest version: *the page answers the questions people ask before calling* (SEO playbook §8.5). |
| "A website is useless now / will be dead in 2027" | [28] | The video's own thesis is that the website's job *changes* (it closes the deal); we do not sell fear with a date on it — same rule as "no invented deadline" (Cristallin 22/09). |
| Coined offer names ("Brand Visibility Accelerator", "Launch Copy Lab") | [29] | US course-market naming; our market reads plain French and §11 bans invented vocabulary. The transformation is named in the client's words. |
| The course/community funnel, $30k-a-month claims, "gamify to 30K" | [29] | Upsells and income claims; nothing transferable to a Douala outbound pipeline. |
| Kinetic typography as a look, expressive/brutalist direction as a default | [30] | Long French headlines at 3G on a mid-range Android: type that moves costs readability. Kept as a test (does it help notice/grasp/understand?), never as a house style. |
| Spline / Unicorn Studio 3D scenes, "12 versions" of a hero as a weekly habit | [30] | External embeds break the single-file rule; and our build budget is one pass + one revision, not twelve — the *principle* (first version is a draft) is what we keep. |
| "Handmade/human-made" as a photo filter or a moodboard | [30] | Already at risk of becoming the next template (the video says so itself). Ours is substance: real photos of the real practice, or nothing. |

## 6 · Weekly ritual (Mondays, before the outreach pack goes out)

1. Re-read the last 7 days of entries in §3/§4.
2. Surface the **top 3 lessons that should change how we operate this week** — each one must name the file it changes and the concrete move it changes.
3. If a lesson contradicts the playbook: state the conflict and ask King which side wins (unless the video is clearly stronger evidence — then propose the change and wait for the yes).
4. Log the Monday summary at the top of §3 as a dated row so the ritual itself is auditable.

---

## Lot [21] · SEO et classement local — 3 vidéos (King, 21/09/2026)

**Analyse complète : `AMK-SEO-PLAYBOOK.md`.** Ce qui suit est le résumé du lot ; les règles de
construction vivent dans le playbook, pas ici.

| # | Vidéo | Chaîne | Ce qu'elle apporte |
|---|---|---|---|
| 21.1 | *How to Rank #1 in Google in 2026: The 3-Step SEO Playbook* | Surfer Academy | la méthode : intention de recherche · format · E-E-A-T · autorité thématique |
| 21.2 | *Rank #1 in Google Business Profile in 2026 (GBP Ranking Factors Explained)* | Portable Entrepreneur | les facteurs de classement local, chiffrés (rapport Whitespark 2026, ~50 experts) |
| 21.3 | *How to Optimize Your Google Business Profile to Outrank 99% of Local Businesses* | Steve Hunsaker | l'expérience terrain : fréquence, avis avec photos, sections produits/services |

### Affirmations centrales retenues

- **Signaux de profil Google 32 % · avis ~20 % · on-page ~15 %** → le profil et les avis font **plus de la moitié** du classement local. *On peaufinait le HTML pendant que la fiche était vide.*
- **Une seule H1, qui porte le mot-clé** (facteur #20 : mots-clés dans les H1/H2 ; #17 : dans le title).
- **Une page dédiée par service** (facteur #19) — c'est là qu'on est en retard sur VENEGRE.
- **Le NAP doit correspondre EXACTEMENT** (facteur #15). Chez nous : déjà bon.
- **La fréquence bat les pics** — pour les avis comme pour les publications.
- **L'expérience (« le second E » de E-E-A-T) est le facteur le plus lourdement pondéré** — photos originales, captures, documentation pas-à-pas, **études de cas avec des chiffres**.
- **Google ne récompense aucun nombre de mots.** La bonne question : *« qu'est-ce que quelqu'un qui tape ça doit savoir, et est-ce que j'ai tout couvert ? »*
- **L'avis automatique n'est pas une preuve de qualité** : une photo dans un avis est difficile à falsifier (géolocalisation), donc Google la remonte.

### 2 tactiques AMK retenues immédiatement

1. **Notre dépôt EST notre preuve d'expérience.** 45 messages, 4 réponses, un site livré, des captures réelles,
   des erreurs assumées — **aucune agence camerounaise ne publie ça.** On publie des études de cas **anonymisées**
   (règle 11) avec de vrais chiffres.
2. **Réécrire nos propres balises avant de vendre du SEO à qui que ce soit.** Notre titre était 100 % anglais
   alors que le marché tape en français. **Fait le 21/09.**

### Contradictions avec nos fichiers

- **Aucune contradiction avec nos règles existantes.** Mais une **tension** : `AMK-DESIGN-SKILLS.md` privilégie
  la sobriété et la conversion ; le SEO demande du contenu et du volume (une page par service, par ville).
  **Arbitrage : une page qui n'a rien à dire ne se crée pas.** On ne fera pas 6 pages de ville vides.
- **Nuance sur les « avis » :** les vidéos insistent sur la collecte d'avis. **Nous n'avons aucun client.** On ne
  peut pas fabriquer d'avis — **c'est interdit et c'est exactement ce que nos propres cibles subissent.**
  Règle : **on demande un avis à notre premier client, avec une photo, et pas avant.**

### Déchets écartés

- Les promotions de leurs propres formations/groupes payants (Home Service Accelerator Pro, Surfer).
- Le contexte métier : plomberie à Houston, décorations de Noël à Scottsdale, SaaS B2B. **Les facteurs de fond
  sont transférables, les tactiques non.** Aucun de ces intervenants n'a jamais fait de SEO à Douala.
- Les « pourcentages » présentés comme des poids officiels : c'est une **enquête d'opinion** auprès de ~50 experts.

---

## Lot [22] · Vente — 3 vidéos (King, 23/09/2026)

Analyse complète et application : **`sales/SYSTEME-DE-VENTE-AMK-2026-09-23.md`**,
**`sales/PERSUASION-5-NIVEAUX-2026-09-23.md`**, **`sales/DECLINAISON-9-DECLENCHEURS-2026-09-23.md`**.
Ce qui suit n'est qu'un repère : les règles vivent dans les fichiers `sales/`, pas ici.

| # | Vidéo | Chaîne | Ce qu'elle apporte |
|---|---|---|---|
| 22.1 | *Sales system* (`youtu.be/5swDtQFyIws`) | Will Barron | les 6 pièces d'un système de vente, une découverte en 6 pas (douleur → déclencheur → futur → ROI rugueux → budget → étape datée), le rythme hebdomadaire |
| 22.2 | *5 niveaux de persuasion* (`youtu.be/cT82oNk49ks`) | Joanna Wiebe | ne pas parler de soi (6 s) · biais · identité et « money words » · les péages · l'histoire = le client en héros |
| 22.3 | *Words That SELL* (`youtu.be/7gjtI1rnds4`) | Joanna Wiebe | 9 déclencheurs par étage du tunnel : cadrage, identité, fluidité / mécanisme unique, typiquement atypique, ennuyeux par dessein / 3 options, compromis transparents, une grosse preuve |

**Ce qui a changé chez nous le jour même :** message 1 réécrit (« je la construis d'abord, vous décidez
après ») · règle **une seule question OU trois choix — jamais les deux** (jamais 2 options) · les
compromis transparents posés dans `MESSAGES-2026-09-23-PERSUASION.md` §8, **à valider par King** ·
notre mécanisme unique nommé : **« L'aperçu d'abord »**.

**Déchets écartés :** les promotions de leurs formations ; le vocabulaire SaaS/US (le « wall of love », les
séquences automatisées) ; tout chiffre de marché non vérifiable localement.

---

## Lot [23] · UX/UI et psychologie du design — 4 vidéos (King, 23/09/2026)

Règles de construction : **`AMK-DESIGN-SKILLS.md` §22**. Portique de contrôle : **`tools/qa/audit_page.py`**.

| # | Vidéo | Chaîne | Ce qu'elle apporte |
|---|---|---|---|
| 23.1 | *What I Wish I Knew Before 10 Years in UX (The 3 Levels)* | Amir Moradi | les trois niveaux (surface · **la ligne de temps invisible** · stratégie) ; « un chemin heureux sans échec, c'est un rêve » |
| 23.2 | *Every UI/UX Concept Explained in Under 10 Minutes* | Kole Jain | affordances, hiérarchie, grilles, typo, couleur, ombres, **4 états du bouton**, **chaque interaction a une réponse**, micro-interactions, overlays lisibles |
| 23.3 | *The UX Psychology Behind Apps People Can't Stop Using* | uxpeak | 6 principes : défauts intelligents · gradient d'objectif · réciprocité · effet IKEA · aversion à la perte · contraste |
| 23.4 | *The Psychology of a PERFECT Website* | Self-Made Web Designer | les 3 amis (survie → émotion → raison) · modèles mentaux · MAYA · chunking · paliers de prix |

### Ce que le lot a mis en évidence, et que nous avons payé

**Un lien WhatsApp sans indicatif pays vivait dans une page déjà envoyée à un client** (`wa.me/699905577`
au lieu de `wa.me/237699905577`) : le bouton central du Cristallin ouvrait une erreur. Deux relectures
humaines ne l'avaient pas vu, **parce que personne n'avait cliqué**. Le même défaut dormait dans les
archives v1 d'Univers Optique — la copie que King ouvre devant le client vendredi pour comparer les deux
directions. C'est le principe 23.2 appliqué à nous-mêmes : *une page sans réponse après le clic est une page
qui n'a pas de chemin.* Les trois pages corrigées, les trois pages passées au portique : voir §22.4.

### Affirmations centrales retenues

- **Quatre états par bouton** (repos, survol, appui, inactif) + un état d'attente quand l'action attend
  quelque chose. Un bouton sans état d'appui ne répond pas au doigt.
- **Chaque interaction produit une réponse** — pas un spinner décoratif : des mots qui disent ce qui vient
  de se passer et ce qui suit.
- **Les défauts intelligents et la réciprocité sont notre modèle économique**, pas un tour de passe-passe :
  l'aperçu est construit **avant** qu'on demande quoi que ce soit, et le message WhatsApp part **déjà écrit**.
- **Jamais créatif sur les conventions** (modèles mentaux) : navigation, logo, horaires, adresse, numéro.
- **MAYA** : structure prévisible + une ou deux surprises (les micro-interactions), jamais la charpente.
- **Chunking** : 3 à 4 éléments par bloc, un numéro de téléphone en trois groupes.
- **Le premier vote est la survie** : nom, métier, ville, horaires, un numéro qui répond — avant l'esthétique.

### Contradictions avec nos fichiers

- **Aucune contradiction de fond** avec `AMK-DESIGN-SKILLS.md` ; le lot **arme** des règles qui étaient
  implicites (les états, la réponse, la ligne de temps).
- **Tension réglée par l'éthique :** les six principes psychologiques ont tous une forme honnête et une
  forme malhonnête. La forme malhonnête (fausse urgence, fausse rareté, faux progrès, avis inventés, séries
  et culpabilité) est **bannie** — elle contredit la loi d'exactitude et détruirait le seul actif qu'on a :
  être celui qui dit la vérité. Les formes honnêtes sont dans §22.3.

### Déchets écartés

- Le conseil de carrière des quatre vidéos (portfolios, salaires, freelance).
- Les exemples d'apps grand public (Duolingo, cartes de fidélité, applications à notifications) : le
  mécanisme est transférable, la mécanique non — un laboratoire d'analyses à Douala ne relance personne
  par notification.
- Les chiffres cités comme preuves de marché (l'étude des confitures, 70–90 % de défauts inchangés) : gardés
  comme **calibration interne**, jamais cités à un prospect — même règle que [16] et [18].
- Les gabarits de sites « parfaits » montrés en exemple : on ne copie pas un gabarit, on applique des règles.

---

## Lot [24] · Stratégie, offre et style — 4 vidéos (King, 23/09/2026)

Règles de construction : `AMK-DESIGN-SKILLS.md` **§23** (style, étoile, police d'ancrage) ·
`AMK-SEO-PLAYBOOK.md` **§8** (AEO) · `sales/AMK-Sales-Playbook-v2.md` **PART K** (offre signature).

| # | Vidéo | Chaîne | Ce qu'elle apporte |
|---|---|---|---|
| 24.1 | *Your Website Won't Matter in 2027. Prepare Now.* | Wes McDowell | la thèse AEO : l'IA comme premier vendeur, YouTube comme source la plus citée, le site réduit à la dernière étape |
| 24.2 | *How to Attract HIGH PAYING Clients (Stop Selling Services)* | Nicole & James | le piège du service, les trois R (affiner · rechercher · repositionner), vendre une transformation |
| 24.3 | *7 Web Design Styles That Make Sites Look Expensive In 2026* | Web Design Lab | sept choix de style, le test du logo, l'anti-recette |
| 24.4 | *6 EASY Tips to 10x Any Site's Design* | Self-Made Web Designer | police d'ancrage, étoile du spectacle, rime visuelle, profondeur, hiérarchie par opacité, dépasser la première idée |

### Ce que ce lot a trouvé dans notre propre travail

**24.4 a mis le doigt sur une dérive contre notre propre règle.** Le §5 de nos design skills dit « Outfit,
police maison », et nos pages écoles/cliniques la chargent bien. **Notre propre site ne déclarait AUCUNE
police** : titres en police de téléphone. La page qui sert de portfolio était celle qui suivait le moins
notre standard. **Corrigé le jour même** (Outfit 400-800, même chaîne de repli : si la police ne se charge
pas, la page est identique à avant).

**Et un demi-motif.** Le cadre de navigateur du hero se répétait déjà sur les quatre cartes de concepts,
mais ses **trois pastilles rouge/ambre/vert** n'apparaissaient qu'une fois. Une rime qui s'arrête à la
silhouette ne rime qu'à moitié : les pastilles sont maintenant dans les quatre cartes.

**24.1 touche une décision de King — et il faut le dire sans arrondir.** Sa décision du 23/09 (geler la
production de contenu) repose sur une mesure de **trafic humain** (5 vidéos → 602 vues → 0 message). La
vidéo affirme que le mécanisme est ailleurs : les modèles lisent une vidéo **le jour de sa publication**,
sans rapport avec les vues. Donc **notre expérience ne réfute pas la thèse — elle ne l'a jamais testée**.
Mais **elle ne la prouve pas non plus**, et le gel reste la décision par défaut : la seule action gratuite
recommandée est un **relevé AEO** (poser la question du prix à trois assistants, noter qui est cité,
recommencer dans 30 jours). Détail et options : `AMK-SEO-PLAYBOOK.md` §8.3.

**24.3 et 24.2 ont chacun une limite écrite.** Les deux styles les plus spectaculaires (typo cinétique,
design expressif) sont retenus comme **tests**, pas comme looks : nos titres sont longs, en français, lus
sur un Android d'entrée de gamme. Et l'offre signature ne devient **pas** un nom inventé à l'américaine :
la transformation se nomme dans les mots du client, sinon elle ne dit rien.

### Affirmations centrales retenues

- **Le site change de métier** : il ferme la décision au lieu de la créer. Une page qui « ne gêne pas »
  bat une page qui impressionne.
- **Vendre un résultat, pas un livrable** : les cinq sections et le bilingue sont des preuves, pas
  l'argument. Le prix s'accroche au résultat, jamais aux heures.
- **Les styles se choisissent, ils ne s'inventent pas** ; et **une tendance devient un problème quand elle
  devient une recette**.
- **L'étoile du spectacle** : un élément, relié à l'histoire de la maison, pas choisi parce que c'est joli ;
  puis on en répète un **composant** ailleurs (rime visuelle).
- **La police d'ancrage se choisit sur le TITRE d'abord**, et le second choix doit contraster franchement.
- **Hiérarchie par niveaux d'emphase** (100 / ~87 / ~60) plutôt que tout au même poids.
- **Dépasser la première idée** : la première version est un brouillon, jamais le livrable.

### Contradictions avec nos fichiers

- **Avec la décision contenu du 23/09** : voir ci-dessus — nuance de méthode, décision inchangée, à King.
- **Avec notre §11 (copie)** : l'offre signature américaine pousse à des noms inventés. Notre règle gagne.
- **Avec §22.6 (honnêteté sur nos limites)** : la vidéo 24.4 suppose de *voir* les variations ; dans ce
  bac, il n'y a pas de navigateur. Les corrections faites cette nuit sont **structurelles et vérifiables
  en code** (police chargée, rythme, pastilles) — **le regard reste celui de King**.

### Déchets écartés

- Les formations, communautés et offres payantes des quatre chaînes ; les chiffres de revenus personnels.
- Les exemples de sites étrangers (parfum, café, mode) : les mécanismes sont transférables, les décors non.
- Les pourcentages AEO cités comme des faits établis (voir §5 du présent fichier).

---

## Lot [25] · MOBILE-FIRST + LA VERTICALE LABO — 3 vidéos + 1 page (King, 23/09/2026, tard)

**Pourquoi ce lot compte plus que les précédents.** Trois des quatre sources parlent du **téléphone**, qui
est l'écran de nos clients et de leurs clients (Flux Academy : ~60 % du trafic mondial est mobile, et
c'est plus au Cameroun). La quatrième parle de **laboratoires** — la verticale dans laquelle on vend
vendredi. Les leçons sont donc allées directement dans la page en cours, pas dans un tiroir.

### 1 · Malewicz — *The Secret to Mobile Web Conversion* (`youtu.be/q8yUIbRiNRc`)

**Cinq fautes communes, plus un bonus, plus l'atterrissage des formulaires.**

① **Entasser le hero du bureau dans le téléphone** : moins d'espace blanc, hiérarchie illisible, le
cerveau se dit « ce n'est pas ce que je cherche » et part. ② **De l'animation lourde dans le hero** :
« pretty damaging to your brand, especially on mobile ». ③ **Des cibles trop petites — ou trop grosses** :
sur bureau 48-52 px ; **sur mobile au-dessus de 52 et en dessous de 64**, sinon on rate sa cible ou on
déclenche la **cécité aux bannières** ; un élément de preuve sociale illisible sur téléphone se
**supprime**, il ne se rétrécit pas. ④ **Un téléphone dans un téléphone** (« inception ») : montrer le
problème résolu par un élément simple. ⑤ **La copie du bureau recopiée** : sur petit écran, **le texte
grossit**, il ne rétrécit pas ; on réécrit la copie pour le téléphone, on change « click » en « tap »,
et on baisse la friction du bouton.

**Bonus, qui contredit une habitude à nous :** *éviter les éléments collants sur mobile* — ni logo ni menu
épinglés pendant le défilement ; un petit bouton « retour en haut » suffit. **Formulaires :** moins de
champs, **cases à cocher d'au moins 32×32**, et « plus de deux champs sur mobile = grosse chute de
conversion » : convertir d'abord, demander le reste ensuite. **Et sa technique en test : micro-visuels sur
mobile, visuels pleins sur bureau** — l'image de hero chasse le titre et le bouton hors de l'écran, donc
elle ne gagne souvent rien.

### 2 · Flux Academy — *This is what mobile web design excellence looks like* (`youtu.be/1r4GHOd2THM`)

Dix exemples vivants. **Empiler les colonnes du bureau n'est pas du responsive, c'est un désastre** :
le mobile a son propre rythme (une ou deux colonnes) et **chaque image a un rapport choisi pour le
téléphone** (le portrait convient aux personnes, un bandeau devient 4:3). La **hiérarchie est
grand → moyen → petit** avec un seul élément dominant par écran ; **l'espace blanc reste possible sur
mobile** et c'est ce qui fait « premium » ; **chaque panneau doit pouvoir être une affiche** ; rien
d'essentiel derrière des clics ; **le mobile n'est pas une raison de faire plat** (angles, cartes
superposées, bandeau horizontal fonctionnent) ; et un **bouton de menu près du pouce**, en bas.

### 3 · Jesse Showalter — *Mobile Design 101* (`youtu.be/q6qA_609UOE`, direct)

**Cinq points :** ① **distiller l'offre** — un seul élément principal par page (son test : faire un grand
cercle sur l'élément le plus important du bureau ; s'il n'y a pas de grand cercle, la page a un problème
partout) ; le menu hamburger existe parce que tout montrer, ce n'est pas distiller. ② **Les boutons vivent
sous le pouce** (la « règle du pouce » : bas confortable, milieu acceptable, haut mauvais). ③ **Typographie
lisible** : pas de police display pour le texte, pas de famille mixée, rien de cursif, **jamais de graisse
thin/light sur mobile**, et **jamais de noir pur sur blanc pur** (nos jetons y répondent déjà). ④
**Optimiser images et vidéo** : redimensionner dans un constructeur ne réduit pas le **poids du fichier** —
exporter une variante légère et laisser les balises choisir ; si l'image de hero ne peut pas être allégée,
**la remplacer par une couleur de marque** (une valeur hexadécimale en CSS) ; **logo en SVG**. ⑤ **Tester
sur de vrais appareils**, dans les vrais navigateurs, « at night, in bright sunlight, Android and iOS ».

**Et trois nombres utilisés désormais :** dessiner la trame mobile vers **360-380 px** ; **420-450 px est
la frontière du mobile** (sous laquelle : une colonne, moins d'images, fonction principale en avant,
boutons plus bas) ; une grille mobile de **4 ou 6 colonnes, jamais 12** — et « make it till you break it »
plutôt qu'un point de rupture par appareil.

### 4 · Thomas Digital — *40 of the Best Lab Websites* (`thomasdigital.com/industry/lab-website-design`)

**Sept principes, dont quatre nous concernent directement :** ① connaître **l'audience primaire** (un site
de laboratoire sert au moins deux publics ; servir tout le monde également, c'est ne servir personne —
le nôtre : le patient envoyé par son médecin) ; ② **mener avec le problème résolu, pas avec la science** ;
③ **les signaux de crédibilité vont au-dessus de la ligne de flottaison** (agréments, personnes nommées,
travaux publiés) — pour nous : l'autorisation réelle, le personnel nommé, horaires, adresse, téléphone,
**jamais inventés ni empruntés** ; ④ **la navigation suit la décision du client**, pas l'organigramme ;
⑤ **précision plutôt que décoration** — les clichés (fond sombre et molécules lumineuses, **photos de
personnes en blouse blanche**) ne différencient personne ; ce qui marche est **spécifique au travail réel**
(appareils, locaux, personnes réelles) ; ⑥ **plusieurs niveaux de profondeur** technique ; ⑦ **pour un
laboratoire d'analyses, le chemin de conversion doit être explicite** : ce qu'il faut fournir, **ce qui se
passe après l'envoi**, les délais — sa phrase : *« People don't fill out forms when they're uncertain about
what comes next. »*

**Ce que ce n'est pas.** Cette page est celle d'un **concurrent** (agence de San Francisco) : elle se lit
pour ses principes et pour son angle commercial (« request a free mockup », l'aveu de ce qu'un site de
labo doit faire). Ses exemples — biotech, capital-risque, publications — ne sont pas notre marché :
**les mécanismes transfèrent, les décors non.** Ses délais (six à dix semaines) ne sont pas les nôtres,
et son « WordPress » n'est pas notre méthode de livraison.

### Ce que le lot a changé, tout de suite

Sur `demos/concept-unilabo-v1.html`, la nuit même — détail et preuves en **§24.5** de
`AMK-DESIGN-SKILLS.md` : texte de 16 → **17 px sur téléphone** ; boutons **48 px** bureau / **52 px**
mobile et **56 px** pour le bandeau ; cases à cocher 17 → **21 px** ; le bandeau collant ramené à **une
action primaire** + WhatsApp + une icône d'appel ; dans le hero, **la fiche passe avant la photo** sur
téléphone ; **variantes légères des photos (482 Ko → 193 Ko sur un téléphone)** et trois graisses de
police économisées ; et le formulaire dit désormais **ce qui se passe après l'envoi**. Enfin, les deux
harnais de test qui vivaient dans `/tmp` (et qu'un rembobinage du bac a effacés) sont entrés au dépôt :
`tools/qa/fake_dom.mjs` + `tools/qa/test_unilabo_page.mjs`, **23 assertions**, exécutables par
`node tools/qa/test_unilabo_page.mjs`.

### Déchets écartés

- Les chiffres de revenus, formations et communautés payantes des trois chaînes ; le « 99 % de mobile »
  que les commentateurs répètent (Flux Academy donne le vrai chiffre, ~60 %) ; les statistiques de
  pourcentage sans source.
- Les exemples de sites étrangers (parfum, robinetterie, danse, architectes) : les mécanismes sont
  gardés, les décors non (§3.7 : pas d'image empruntée).
- La tirade « l'IA va remplacer les designers juniors » : vraie sur le fond (elle vise la production),
  mais ce n'est pas une leçon de design, et elle ne change aucune de nos décisions.
- La page de Thomas Digital comme **argument de vente** : on ne cite pas un concurrent devant un prospect.

---

## Lot [26] · LE PREMIER ÉCRAN, ET LA PROSPECTION PAR GOOGLE MAPS — 5 vidéos (King, 24/09/2026, au matin)

Règles de construction : **`AMK-DESIGN-SKILLS.md` §26**. Contrôle : **`tools/qa/audit_hero.py`**
(+ `tools/qa/test_audit_hero.py`, qui vérifie que ce contrôle refuse bien ce qu'il doit refuser).
Prospection : **`sales/APPELS-GOOGLE-MAPS-2026-09-24.md`**.

| # | Vidéo | Chaîne | Ce qu'elle apporte |
|---|---|---|---|
| 26.1 | *Mastering Landing Page UI Design: Tips, Tricks, and Best Practices* (`iDzt8VWqjEg`, 7:41, 2023) | UI UNIVERSITY | **AUCUNE PAROLE** — sous-titres de musique seulement (vérifié deux fois : YouTube et le site de transcription). Tutoriel de code-along : on lit le code, pas la vidéo. Voir 26.6. |
| 26.2 | *How To Make Animated Website Design Using HTML And CSS Step By Step* (`nbBQCeOCMmQ`, 14:44, 2024) | UI UNIVERSITY | **AUCUNE PAROLE** non plus. L'idée retenue (deux moitiés de titre qui glissent l'une vers l'autre, image qui monte en place) ; l'implémentation est fautive. Voir 26.6. |
| 26.3 | *18 Hero Section Designs You Can Steal* (`kJb6BZwqCGM`) | Payton Clark Smith | trois familles (fiables / centrées / fantasques), **l'image à gauche vole le premier regard**, et le verdict qui compte : **texte posé sur une photo = « old school », ça fait daté et le bouton devient invisible** |
| 26.4 | *21 Brand New Hero Sections You Must Copy* (`z5yvZW8Ep-E`) | Payton Clark Smith | 16 mises en page : colonne qui **avale la barre de navigation**, image qui **déborde de sa colonne** (profondeur), **image coupée par le pli** (fait descendre), preuve sociale **descendue du hero** pour la laisser respirer, **hamburger sur ordinateur = presque toujours une faute**, ligne qui guide l'œil, rangée de **chiffres-clés** (prix · délai · nombre d'usagers · note) |
| 26.5 | *How I Get Easy Web Design Clients From Google Maps* (`LxweAVqlFMM`) | Payton Clark Smith | **les trois cibles** (pas de site / site cassé · site daté · avis récents négatifs) · le mobile avant le fixe (**on joint le patron, pas la secrétaire**) · l'ouverture simple qui n'est pas un pitch · **les 50 à 100 premiers appels sont mauvais pour tout le monde** · « ton avantage, ce n'est plus de savoir construire, c'est ta distribution et tes gens » |

### 26.3–26.4 · La grammaire du premier écran (39 mises en page, deux vidéos)

Ce qu'on **garde**, et qui devient la règle de nos heros :

1. **Texte d'abord, à gauche ; l'image à droite.** Si l'image passe à gauche, c'est la première chose
   qu'on regarde et le titre perd la course. Une seule exception : quand l'image *est* le produit.
2. **Jamais de texte posé sur une photographie** — la vidéo le classe « old school », et c'est aussi ce
   que King a refusé la nuit dernière. Les deux verdicts se rejoignent : ce n'est pas un goût, c'est un
   défaut de lisibilité, et le bouton est le premier à disparaître.
3. **Image coupée par le pli = une invitation à descendre.** Nous l'avons déjà sur la photo de
   préparation d'UNI-LABO (4/3, coupée par le bas de la section). À refaire exprès, pas par hasard.
4. **La preuve sociale descend du hero.** Elle y étouffe le titre et se lit mal ; juste en dessous, elle
   respire. (UNI-LABO n'a **aucun avis** : on n'en fabrique pas — cette règle attend le jour où il y en
   aura.)
5. **Centrer seulement quand le texte est court** ; dès deux phrases, on repasse à gauche. Le centrage
   s'effondre avec la longueur.
6. **Le hamburger sur ordinateur cache ce qu'on a la place de montrer.** Une exception honnête : une
   page de vente unique où l'on veut retenir le visiteur.
7. **La profondeur** (colonne qui avale la barre, image qui déborde de sa colonne, image qui raconte un
   **processus** au lieu d'être un stock) : ce sont les techniques à ressortir pour la **prochaine**
   construction (l'école d'octobre, la clinique suivante), pas à empiler sur une page qui marche.
8. **La rangée de chiffres** (prix · délai · usagers · note) donne de la matière au premier écran sans
   photographie. Sur un labo, l'équivalent honnête que nous avons déjà : horaires, préparation,
   délai confirmé sur place, langues.

### 26.5 · La prospection par Google Maps — ce qui manquait

Nous faisions déjà deux des trois cibles (site absent ou cassé ; site daté) **mieux que la vidéo** :
nous auditons avant d'approcher, nous arrivons avec un constat. La troisième — **les avis récents
négatifs** — nous ne l'avions jamais essayée. Elle vaut une ligne d'offre, avec une limite tenue : on ne
promet **jamais** de faire disparaître un avis (c'est faux, et contraire aux règles de Google). Ce qu'on
peut honnêtement vendre : une demande d'avis après une visite réussie, la correction de la cause
invoquée, et une réponse publique posée. Détail et phrases en `sales/APPELS-GOOGLE-MAPS-2026-09-24.md`.

**Le mobile avant le fixe.** Sur 149 fiches du CRM, **22 portent un numéro** — 18 mobiles, 4 fixes. Le
plan du jour n'appelle que des mobiles : la règle était déjà respectée dans les faits, elle est
maintenant écrite. Et pour les quatre lignes fixes, le travail n'est pas d'appeler : c'est de **trouver
le mobile** (Maps, Facebook), parce que notre canal est WhatsApp.

### 26.6 · Ce qu'un tutoriel de code-along enseigne vraiment (les deux vidéos muettes)

Les deux vidéos d'UI UNIVERSITY n'ont pas de parole : leurs sous-titres automatiques ne contiennent que
la musique. Leur valeur est donc dans **leur code**, que j'ai lu ligne à ligne dans les deux dépôts
cités par leurs descriptions (`JeeJu-Coding/agency`, `uiuniversity/animated-hero-section`). Verdict :

- **`h1::before{content:'The'}` / `::after{content:'Agency'}`** — le titre visible est écrit **dans le
  CSS**. Invisible pour un lecteur d'écran, ignoré par Google, introuvable au Ctrl+F. C'est la faute la
  plus grave des deux dépôts, parce qu'elle ne se voit pas.
- **`height:100vh` + un titre à 180 px (ou 222 px) en position absolue + zéro `@media`.** Magnifique sur
  l'écran de celui qui l'a fait, cassé sur un téléphone — exactement le reproche que King m'a fait.
- **Des `@keyframes` qui déplacent `bottom`** (une propriété de mise en page) sans
  `prefers-reduced-motion`.
- **Du lorem ipsum** et un `{{PLACEHOLDER}}` dans le HTML livré.

La leçon utile n'est donc pas « voici comment on fait un hero » : c'est **le geste se garde, le code se
jette**, et un tutoriel qui montre un beau résultat n'est pas une référence de qualité. Ces quatre
défauts sont désormais **détectés automatiquement** par `tools/qa/audit_hero.py` — dont le test
`test_audit_hero.py` les reproduit exprès pour prouver qu'il les attrape.

### Déchets écartés

- **L'offre « site gratuit + abonnement mensuel »** recommandée par 26.5 pour ouvrir une porte : elle
  suppose de baisser le prix, et notre règle est de ne jamais remiser — on ajuste le périmètre. Notée
  comme décision pour King (un étalement du paiement n'est pas une remise), pas appliquée.
- **L'outil payant de la vidéo** (uglisitescraper) : il fait ce que nous faisons déjà à la main sur
  Maps, et il est orienté États-Unis.
- Les pourcentages de conversion et les montants (30 000 $ en dix jours) : non vérifiables ici, et pas
  nécessaires — c'est la régularité qui compte, pas le chiffre.
- Les 39 mises en page **comme modèles à copier** : ce sont des idées de composition. Aucune image, aucune
  marque, aucun gabarit n'est repris (même règle que §3.7).

### Ce qu'on pourrait apprendre ensuite — proposé le 24/09, à choisir par King

Chaque ligne nomme **le manque réel** qu'elle comble, pas un sujet qui a l'air utile. Avant d'enregistrer
une source, je la lis (et si c'est une vidéo, je vérifie qu'elle a une vraie parole — le lot [26] a montré
que deux vidéos sur cinq n'en avaient aucune).

| priorité | sujet | le manque que ça comble | sources (à lire avant d'enregistrer) |
|---|---|---|---|
| 1 **(choisie, faite — lot [27])** | **L'accessibilité (WCAG) sur nos pages** | le lot [26] a trouvé des mots écrits dans le CSS, invisibles aux lecteurs d'écran. Nos clients sont des **institutions** (écoles, labos) : l'accessibilité y est un argument de sérieux, pas une mode | W3C WAI (référence officielle) · web.dev (Learn Accessibility) · les rapports de l'auditeur `tools/qa/audit_page.py` |
| 2 | **Google Business Profile à fond** (fiche établissement, avis, photos, horaires) | c'est la troisième cible du lot [26] (les avis) et la première chose qu'un patient ou un parent voit. Aujourd'hui on l'évoque, on ne le vend pas | documentation officielle Google Business Profile · `AMK-SEO-PLAYBOOK.md` §8 en regard |
| 3 | **WhatsApp Business pour un commerce** (catalogue, messages d'accueil, réponses rapides, étiquettes) | nous vendons « formulaire WhatsApp » ; si le client n'a pas configuré son WhatsApp Business, l'expérience s'arrête à l'envoi | WhatsApp Business — aide officielle (faq.whatsapp.com) · tutoriels de commerçants |
| 4 | **Photographier un labo/un cabinet avec un téléphone** | la photo n'est pas comprise dans les 150 000 et nous allons devoir la prendre nous-mêmes, dans leur lumière, sans mentir | à chercher et vérifier (éclairage naturel, plans serrés, arrière-plan) — je proposerai trois candidats lus d'avance |
| 5 | **Prix et récurrence** (comment vendre un abonnement sans remiser) | une décision est ouverte : l'échelonnement du paiement au prix plein, ou le site compris dans 12 mois d'abonnement (§5 de `sales/APPELS-GOOGLE-MAPS-2026-09-24.md`) | études de cas d'agences, hors marchés US si possible — à filtrer sévèrement |
| 6 | **Le français d'ici** (écrire pour un commerçant de Douala) | nos textes sont propres mais parfois « traduits » ; les clients parlent un français plus direct | à construire **nous-mêmes** : relire nos 20 meilleurs messages et extraire nos propres règles, avec les mots des clients (le journal en est plein) |

---

## Lot [27] · ACCESSIBILITÉ (WCAG) — 2 sources de King + les documents officiels (King, 24/09/2026)

**Déclencheur.** King : *« start with accessibility, I guess you will do research online, I'll add what I
can find »*. Il a envoyé deux sources ; le reste, je suis allé le chercher aux endroits qui font foi (W3C,
MDN) plutôt que chez ceux qui vendent un service. C'était la priorité n° 1 de la liste « apprendre
ensuite » écrite la veille dans ce même fichier.

### Les sources lues, et ce que chacune a apporté

| source | ce qu'elle apporte réellement | ce qu'on en garde |
|---|---|---|
| **Silktide**, *WCAG explained* (`youtu.be/5H1JGdqLrWo`, 1:50) | la façon dont un client entend les niveaux : **A = « must do », AA = « should do », AAA = « reaching for the stars »** | le vocabulaire. On annonce **WCAG 2.2 niveau AA** : un standard **et** un niveau, jamais l'adjectif seul |
| **Accessible Web**, *Manual WCAG Auditing Tutorial* (playlist `PLqQI0lmiVs1jhQQNAprIPCjFUYVBB7tY8`, **55 vidéos**) | une vidéo par **critère de succès**, intitulée *« Testing X.Y.Z… »* ; la playlist couvre WCAG 2.2 (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 4.1.2, 4.1.3) | **la forme d'un audit** : on passe les critères un par un, dans l'ordre, et on écrit ce qu'on a vérifié. Leur outil RAMP et les rappels d'extension sont écartés (marketing) |
| **W3C**, `TR/WCAG21` + `WAI/WCAG22/quickref` | les critères eux-mêmes, leur numéro, leurs techniques ; la 2.2 est la plus récente (2.1 et 2.0 restent valides) | la numérotation est la langue commune — c'est elle qui rend un rapport vérifiable |
| **MDN**, *Understanding WCAG* + *Keyboard accessible* + *Text labels and names* | les 4 principes **POUR** ; « un élément focusable doit être interactif » ; **jamais `tabindex` positif** ; un clic doit avoir un équivalent clavier ; un `<title>` est obligatoire ; un dialogue a un nom | les règles de terrain, plus lisibles que la spécification pour décider vite |

### Ce que l'audit a trouvé SUR NOS PAGES (et qui a été réparé)

Un contrôle d'accessibilité qui ne trouve rien sur ce qu'on a déjà livré ne valait pas la peine d'être écrit.
Onze défauts, sur quatre pages, dont trois invisibles à l'œil :

1. **Deux champs du formulaire du site dont l'étiquette n'était pas attachée** au champ (un `<label>`
   voisin, sans `for=`) : un lecteur d'écran annonçait « champ de texte » sans dire lequel (WCAG 3.3.2).
2. Le formulaire écrit maintenant sa réponse après le clic, avec un rattrapage si le
   navigateur bloque la fenêtre (WCAG 3.3.1 : la leçon d'UX du lot [22], côté accessibilité).
4. **Des sauts de niveau dans les titres** : `h2` → `h4` et `h2`→`h5` sur le site, `h2`→`h4` au pied de page
   d'UNI-LABO. La hiérarchie est la carte du document pour qui navigue de titre en titre (WCAG 1.3.1).
5. **Dix icônes décoratives non marquées** `aria-hidden` : le lecteur d'écran annonçait « image » sans rien
   dire avant chaque lien (WCAG 1.1.1).
6. **Un menu mobile qui ne disait pas qu'il s'ouvrait** : pas d'`aria-expanded`, et la touche Échap ne le
   fermait pas. Les boutons de langue ne disaient pas lequel était actif (`aria-pressed`).
7. **Les quatre photos de familles d'UNI-LABO** portaient un alt qui répétait le texte déjà imprimé sous la
   photo (« Photo d'illustration de laboratoire — Biochimie »). **On a ouvert les images** et écrit ce
   qu'elles montrent : six tubes à bouchon bleu dans un portoir violet avec une micropipette ; un frottis
   sanguin ; une pipette sur une plaque à puits violets ; un automate à bras mécanique au-dessus d'un
   carrousel de tubes.

### Ce que ça a produit, et ce que ça ne prouve pas

- **Le contrôle `tools/qa/audit_a11y.py`** (WCAG 2.2 AA), testé par `tools/qa/test_audit_a11y.py` : douze
  défauts attendus sur une page fautive, zéro alerte sur une page saine, et il **dit aussi ce qui est
  conforme**. Les pages AMK et UNI-LABO sortent à **0 faute A/AA**. La doctrine est en **§27**.
- **Ce que ça ne prouve pas** : le contraste (couvert par `audit_html.py`), l'ordre de tabulation réel, le
  rendu à 200 %, et la qualité d'un alt — les quatre demandent un œil. On l'écrit dans le rapport, on ne le
  cache pas.
- **Une leçon d'outillage** : le premier jet de mon contrôle a produit **cinq faux positifs** (et un faux
  négatif : `a:focus{outline:none}` satisfaisait son propre test « une règle de focus existe »). Corrigés
  dans l'outil, jamais tolérés. C'est la même leçon qu'au lot [26] avec les deux vidéos muettes : **vérifier
  l'instrument avant de croire la mesure.**

---

## Lot [28] · LE LECTEUR D'ÉCRAN ET LES FORMULAIRES — 4 sources de King (24/09/2026, dans la journée)

Suite directe du lot [27] : King a envoyé exactement les deux angles que le rapport d'accessibilité
signalait comme manquants — **le test réel au lecteur d'écran** et **les formulaires**. Quatre sources,
dont une qui n'a pas pu être lue (dit plus bas, sans détour).

| source | ce qu'elle apporte | ce qu'on en garde |
|---|---|---|
| **`youtu.be/aAh1PFsgcBY`** — *NVDA Screen Reader Tutorial: How to Use It for Accessibility Testing* (Software Testing 101, 18,5 k abonnés, lu en entier) | le mode d'emploi du test à l'oreille, et **la comparaison la plus utile qui soit** : le même formulaire chez eux (fautif) puis chez Apple (irréprochable) | les touches (**D** repères, **H** titres, **K** liens, **F** champs, **NVDA+Tab** où suis-je), l'astuce des **trois couleurs** (bleu = focus, rouge = lecture, jaune = revue) qui rend le test possible pour quelqu'un qui voit, et le vocabulaire des pannes |
| **`kortic.com`** — *Formulaires et messages d'erreurs accessibles* (Anthony Ladeuil, FR, licence CC BY-NC-SA) | tout l'article porte sur ce que personne ne fait : **gérer les erreurs de saisie** | étiquette liée et à proximité · format annoncé · **le placeholder n'est pas une étiquette** · `type` + `autocomplete` · `fieldset`/`legend` pour les groupes · pas de CAPTCHA (un honeypot à la place) · **marquer les champs FACULTATIFS plutôt que d'astérisquer les obligatoires** · et le patron complet du **résumé d'erreurs** : un conteneur focalisé, une liste où chaque erreur est un **bouton qui amène au champ** et le marque `aria-invalid` |
| **`github.com/videvelopers/TalkBack-Sound-effect-for-NVDA-`** | un module NVDA (Python, MIT, 2023) qui imite les sons de TalkBack : **un son par objet** quand on se déplace | l'idée qui compte n'est pas le module, c'est ce qu'il imite : **sur Android, on explore élément par élément**. Ce qui n'est pas atteignable au balayage n'existe pas — et c'est le téléphone que nos clients ont |
| **`faq.whatsapp.com/3614672068767202`** | ❓ **PAGE NON LUE** | voir ci-dessous |

### La source qui n'a pas pu être lue — et pourquoi je l'écris

Le lien du centre d'aide WhatsApp (plateforme Android, locale fr_FR) **répond 403** à notre outil de fetch,
et le bac à sable n'a **aucun réseau en ligne de commande** (vérifié : `curl` répond `000` même pour
`example.com`). Quatre tentatives : URL d'origine, sans paramètres, en `fr_FR`, en `en_US`. **Je n'ai pas
lu cette page, je ne vais donc pas résumer ce qu'elle dit.** Ce qu'on peut affirmer sans l'avoir lue : WhatsApp
fonctionne avec TalkBack et VoiceOver (c'est documenté par des sources tierces, et Android Accessibility Suite
le décrit). **Si King veut que son contenu entre dans le dossier, il suffit de coller le texte ici** — et il
sera intégré comme les autres.

### Ce que ces sources ont fait changer dans le code, le jour même

Quatre vrais défauts trouvés sur nos pages, tous invisibles à l'œil :

1. **Les trois pages du site n'avaient AUCUN repère `<main>`.** C'est le tout premier constat du tutoriel :
   sans repère principal, le lecteur annonce l'en-tête, le menu, le pied de page… et **« page blank »** au
   milieu. Corrigé : `<main id="contenu">` + `main{display:block}`.
2. **Deux de ces pages n'avaient pas de lien d'évitement** (« Aller au contenu ») — le critère **2.4.1, qui
   est de niveau A**. Corrigé : le lien est en première position dans le `<body>`, donc au premier `Tab`.
3. **Le formulaire du site échouait en SILENCE** : `if (!biz) return false;` — un clic sur « Recevoir mon
   aperçu » sans nom ne produisait **rien** : pas de message, pas de focus, aucune annonce. C'est
   exactement le défaut que le tutoriel NVDA décrit (« *it does not introduce an error message… only says
   blank* ») et que tout l'article de Kortic traite. Et il y avait un cas vicieux : un champ rempli
   d'**espaces** passait la validation native du navigateur (`required`), donc le JavaScript était le seul
   filet — et il ne disait rien. Corrigé : la zone vivante **annonce** ce qui manque, le champ est marqué
   `aria-invalid`, et **le focus y est amené**.
4. **L'astérisque des champs obligatoires** (« Nom de l'école ou de la clinique \* ») n'était expliqué **nulle
   part** — or un astérisque ne se vocalise pas et sa signification doit être donnée *avant* le formulaire.
   Appliqué la règle de Kortic : on ne marque plus l'obligatoire, on marque le **facultatif** (« Votre numéro
   WhatsApp (facultatif) »).

Deux contrôles neufs dans l'outil, nés de la même phrase :

- **2.4.1 — les repères** : sans `<main>`, la page est signalée (« la navigation au lecteur d'écran annonce
  l'en-tête, le menu, le pied de page, et rien au milieu ») ;
- **1.3.1 — les groupes nommés** : un `<fieldset>` **sans `<legend>`** ne nomme rien ; le lecteur annonce
  alors des cases isolées (« *personal radio button, one of two* ») sans dire de quoi il s'agit.

Et un contrôle qui passe d'avertissement à vérification : **3.1.2** regarde maintenant **comment** la page
bilingue cache l'autre langue. `display:none` la retire de l'arbre d'accessibilité ; `opacity:0` ou
`visibility:hidden` la laissent dedans — le lecteur annonce alors **les deux langues à la suite**. Sur
UNI-LABO c'est `display:none` ✅, sur le site une seule langue est dans le document à la fois ✅.

### Le livrable qui manquait

**`tools/qa/PROTOCOLE-LECTEUR-ECRAN.md`** — le test à l'oreille, en 5 minutes, fait par un humain : quoi
installer (NVDA gratuit, TalkBack préinstallé), les **huit touches** qui comptent, **ce qu'on doit entendre
sur nos pages** (avec les vrais chiffres : 44 titres et 42 liens sur le site, « *1 · Vos analyses, groupe de
cases à cocher, 1 sur 19* » sur UNI-LABO), les gestes TalkBack sur Android — et la question qui compte pour
nous : **le double tap ouvre-t-il WhatsApp ?** — plus trois limites écrites noir sur blanc (nous ne sommes pas
des utilisateurs expérimentés de lecteur d'écran ; on ne teste jamais sur la vraie page du client ; le
protocole complète l'audit automatique, il ne le remplace pas).

### Ce que le lot [28] confirme du lot [27]

Les deux lots se rejoignent sur un point, par deux chemins indépendants : **une page peut être parfaite dans
le code et muette à l'oreille.** Le lot [27] l'avait trouvé en lisant les critères ; le lot [28] le montre en
comparant un formulaire fautif et un formulaire Apple. C'est la raison d'être du protocole manuel : il n'y a
pas d'outil qui entende à notre place.

---

## Lot [29] · LE PREMIER ÉCRAN, DEUXIÈME PASSE — le processus, le regard, et la règle des 90/10 (24/09/2026)

Cinq vidéos de King, toutes sur le premier écran. **Trois viennent de Flux Academy** (1,09 M d'abonnés) :
un processus complet, 21 mises en page réelles décortiquées, et l'épisode 10 de leur cours gratuit. Les deux
autres : **Ahmed Alsayad** (plan de conversion + liste de contrôle) et **Malewicz** (25 ans de métier,
500 heures d'enregistrements de sessions).

**Ce lot recoupe le lot [26]** (Payton Clark Smith, 39 heros) — je le dis parce que c'est vrai, et parce que
répéter une leçon en la faisant passer pour neuve est une façon de grossir un journal. Le lot [26] avait
donné la **grammaire** (texte à gauche, jamais de texte sur une photo, image coupée par le pli, preuve
sociale en dessous, pas de hamburger sur ordinateur). Celui-ci ajoute quatre choses qui n'y étaient pas :
**le processus qui fabrique un premier écran**, **la mécanique pour diriger un œil**, **le partage du
travail entre le haut de page et le reste**, et **l'échec par surcharge mentale**. Deux de ces apports sont
maintenant vérifiés par la machine.

### Ce que chaque source apporte

| source | l'apport | ce qu'on en garde |
|---|---|---|
| **Flux Academy — le processus** (`LJbkLdtEW00`) | six étapes, dans l'ordre : **stratégie → maquette → 3 concepts → imagerie → design → optimisation** | les questions de la séance de stratégie (ce que vous vendez, pourquoi vous avez commencé, qui vous aidez, que doivent faire les gens) réduites à **une promesse et une action** ; **la maquette n'est pas jolie et ne doit pas l'être** ; **trois concepts dessinés à la main avant tout design**, pour vérifier qu'il y a la place du texte à côté de l'image ; à l'optimisation : le mot « gratuit », la preuve sociale, le **bouton fantôme** pour l'action secondaire |
| **Flux Academy — 21 mises en page** (`Kg2ioQMjtIA`) | 21 heros de vrais sites, expliqués | on ne veut pas **une rangée d'éléments moyens** : quelque chose de très grand, quelque chose de très petit, le contraste fait l'échelle ; l'image peut passer **sous** le titre (intégration, pas « posée à droite ») ; le haut de page **compact**, dont on voit l'amorce de la section suivante ; le concept qui porte (la carte d'embarquement de Runway) ; et le « **hero sans hero** » quand la marque est connue et le contenu change (MoMA, un journal) |
| **Flux Academy — épisode 10** (`flAcHu-squc`) | **la règle des 15 secondes** (80 à 90 % partent avant) et les trois questions : *qu'est-ce que c'est / que faites-vous / qu'est-ce que j'y gagne* | un logo **en icône seule ne répond pas à « où suis-je »** : le nom doit être écrit ; une police d'affichage va bien à 60 px et devient illisible à 16 px (deux polices, ou deux graisses) ; le sous-titre fait la même largeur que le titre, sans mot orphelin ; l'image se choisit pour **la place qu'elle laisse au texte** (un fond chargé est un mauvais choix), quitte à recadrer et à étendre le ciel |
| **Ahmed Alsayad — le plan** (`gNWOBI67XnQ`) | l'anatomie et les deux familles de fautes | l'anatomie : **titre, sous-titre, visuel, signal de confiance, action** ; la faute n° 1 est la **surcharge mentale** — « beaucoup d'options, donc aucune choisie » : plusieurs boutons, plusieurs couleurs, pas de hiérarchie, tout entassé, et pire, des **actions cachées** ; la faute n° 2 est le site primé qui ne convertit pas (parallaxe lourde : « ça tue l'usage ou la performance » ; titres « malins » mais obscurs) ; et sa liste de contrôle finit sur **mobile** et **chargement rapide** (webp, lottie plutôt que mp4) |
| **Malewicz — le regard** (`nWbBZPjev_0`) | trois techniques mécaniques et une règle de partage | **principe du regard** : une personne qui regarde l'objectif met l'attention sur ses yeux, une personne qui regarde le bouton nous y conduit — et sur téléphone on recadre la même photo pour qu'elle **lève les yeux vers l'action** ; **guide optique** : le bord droit d'un texte qui descend en biais est un entonnoir vers la suite ; **accord de couleur** : recolorer **un** vêtement d'une teinte proche du bouton principal (tout recolorer donne un uniforme) ; et la règle **90/10** : le haut de page fait 90 % de la persuasion, **les 10 % restants se font en dessous** (« clearing doubts ») |

### Les quatre règles nouvelles dans `tools/qa/audit_hero.py`

Cinq contrôles, tous nés de phrases précises, tous vérifiés par des témoins fautifs construits exprès
(`tools/qa/test_audit_hero.py`, cinq assertions de plus) :

1. **un premier écran sans phrase d'appui** → avertissement (le titre doit porter seul le quoi, le pour qui
   et le pourquoi : c'est beaucoup pour une ligne) ;
2. **un premier écran sans aucune action** → avertissement (« le visiteur comprend où il est et ne peut rien
   faire ») ;
3. **plus de deux actions** dans le premier écran → avertissement de **charge mentale** ;
4. **une marque en icône sans son nom écrit** → **faute franche** (la règle des 15 secondes) ;
5. **`height:100vh` exact sans rien** (flèche, mot, amorce de section) → avertissement : le visiteur ne
   descend pas.

Un trou a été bouché au passage : quand l'outil **ne trouve pas** de premier écran à analyser, il le dit
maintenant (`INFO`), au lieu de laisser cinq règles se taire en silence — un contrôle muet ressemble à un
contrôle satisfait.

### Le résultat honnête, et il est inhabituel

**Les six pages passent les douze contrôles sans un seul constat.** C'est la première fois depuis le début
de ces lots : cinq lots d'affilée avaient trouvé de vrais défauts dans notre propre travail. Les pages
répondent déjà aux trois questions, portent une phrase d'appui, tiennent en deux actions, montrent leur nom
à côté de l'icône et ne s'enferment pas dans un écran plein. **Ce n'est pas une raison de se relâcher** :
ces règles viennent de sources lues aujourd'hui, et la prochaine page — l'école, en octobre — part d'un
fichier blanc, où rien de tout cela n'est hérité.

### La lecture à l'œil — ce qu'aucun contrôle ne pouvait voir

Les cinq règles ci-dessus sont mécaniques. La **règle des 15 secondes**, elle, se juge en lisant le premier
écran comme quelqu'un qui ne connaît ni l'entreprise ni le quartier. Je l'ai faite, et voilà ce qu'elle
donne :

- **UNI-LABO** répond aux trois questions avant la première ligne du titre, parce que sa marque porte le
  métier : « **UNI-LABO — Laboratoire d'analyses de biologie médicale** », puis le lieu (« Bonamoussadi,
  Douala »), puis la promesse (« Le résultat juste, du premier coup »), puis ce qui se passe concrètement
  (« vous arrivez avec l'ordonnance… vous repartez en sachant quand revenir »). *« Où suis-je », « que
  faites-vous », « qu'est-ce que j'y gagne » : les trois sont là.* Le nom du biologiste et le numéro
  suivent — la confiance est nommée, pas suggérée.
- **Le site AMK** répond aussi aux trois, avec une nuance : **l'accroche et le titre disent la même chose**
  (« Développement web — écoles & cliniques · Cameroun » puis « Création de sites web pour écoles et
  cliniques au Cameroun »). Or l'accroche est une place précieuse : chez Malewicz elle sert à **planter la
  preuve** avant le titre ; chez Flux, à donner le contexte. Aujourd'hui elle répète.

  **Je ne l'ai pas changée.** C'est une décision de positionnement, pas un défaut mécanique : notre propre
  page n'est pas dans la réunion de vendredi, je n'ai aucune donnée qui dise qu'une version fait mieux, et
  la règle de la maison est de ne pas rouvrir une page qu'on vient de livrer sur un avis personnel. **La
  question est posée à King**, avec deux pistes honnêtes et vérifiables : y mettre le **lieu**
  (« Douala · Yaoundé · Buea · Limbé », qui est déjà dans le titre de la page) ou y mettre un **fait
  vérifiable** (« 5 sites en ligne qu'on peut ouvrir »). Rien d'inventé dans les deux cas — et rien
  d'appliqué sans son accord.

### Et une troisième fois, l'instrument avait tort

Mes cinq assertions ont d'abord produit **trois échecs** sur des témoins que l'outil refusait
correctement : `levels()` renvoie un **couple** (niveaux, constats) et non un ensemble, et je cherchais
« aucune action » en minuscules quand le message dit « AUCUNE action ». Trois fois la même leçon que les
lots [27] et [28] — **quand un contrôle accuse, c'est l'instrument qu'il faut soupçonner d'abord** — et
elle est écrite dans le test, à l'endroit exact où je me suis trompé.

### Ce qu'on n'a pas copié

Flux construit la confiance avec « Obi-Wan et 4 000 autres nous ont déjà rejoints », Malewicz avec une
rangée de chiffres. Nous n'avons ni avis, ni nombre de clients, ni presse — **et en inventer un est
interdit depuis le premier jour**. Ce qu'on a est vérifiable : cinq pages réelles que n'importe qui peut
ouvrir, les mots du laboratoire, et le fait que le visiteur regarde son propre futur site. Écrit ici pour
le jour où la question viendra.

---

## Lot [30] · LA FICHE GOOGLE, ET LE LIEN D'ÉVITEMENT MORT — 4 vidéos (24/09/2026, quatrième lot du jour)

Quatre liens sans texte. Trois sur la **fiche Google** — Santrel Media (1,13 M d'abonnés, l'installation
pas à pas), Ignite Visibility (64,9 K, vingt points de contrôle), Zanet Design (36,2 K, une compilation
présentée comme une masterclass) — et une sur l'**accessibilité** : Imran Siddiq, Web Squadron (195 K),
une démonstration complète dans Elementor. Toutes parlantes, lues en entier (la première a demandé deux
tentatives : YouTube bloque les sites de transcription par intermittence).

**Ce que le lot [26] avait déjà dit, et que je ne revends pas** : la prospection par Google Maps, le
mobile avant la ligne fixe, les trois cibles, les ouvertures d'appel. Le lot [26] avait établi *où
trouver* les prospects ; celui-ci établit **quoi faire de leur fiche Google** — un sujet neuf.

### Ce que chaque source apporte

| source | l'apport | ce qu'on en garde |
|---|---|---|
| **Santrel Media** — l'installation | le pas-à-pas filmé, écran partagé | on **cherche d'abord sur Maps** : si la fiche existe, on la REVENDIQUE, on ne crée pas de doublon ; un compte Google professionnel, pas le personnel ; les services et produits remplis « sans lésiner » ; la description (750 caractères, quelques centaines au minimum) ; au moins cinq ou six photos, et les clients en ajouteront ensuite ; **la vérification** par téléphone, courrier ou vidéo — c'est le client seul qui peut la faire ; et cette phrase qui nous concerne : « les gens cliquent presque toujours sur le lien du site » |
| **Ignite Visibility** — 20 points | une liste récitée vite, utile comme inventaire | le **NAP** (nom, adresse, téléphone) identique partout sur le web ; des **avis réguliers** ; les **horaires** qui commandent la visibilité ; la **FAQ** sur la fiche **et** sur la page ; une URL qui contient la ville et le service ; la carte du site qui renvoie à la fiche et l'inverse ; les **images locales** ; le texte alternatif **dans la fiche et dans le HTML** ; 3 à 5 **vidéos courtes** ; un appel à l'action dans le texte ; le **schéma `LocalBusiness`** sur la page d'arrivée ; les publications régulières pour que la fiche reste vivante ; et la conclusion : « traitez votre fiche comme son propre site web » |
| **Zanet Design** — la masterclass | le plus long, et le seul qui parle de **suspension** et de **couleurs de performance** | la **catégorie principale est le plus gros facteur** (et sa méthode : regarder celles des concurrents du quartier) ; le nom réel, jamais de mots-clés collés ; **les 13 pièges de suspension** ; le **chat** rouvert (SMS et WhatsApp — avec un **lien `wa.me`**, pas un numéro, sinon ça ne marche pas) ; le champ « **date d'ouverture** » que presque personne ne remplit ; la **vérification** ; « personnes et accès » pour déléguer la gestion ; le **cercle de couleur** des statistiques (mobile, ordinateur, Maps) pour savoir comment SES clients le trouvent ; et sur les avis : **Google n'utilise que ce que les clients écrivent**, pas ce que le commerçant répond — un avis frais pèse plus que des mois de travail, et un avis avec photo vaut dix avis de texte |
| **Imran Siddiq** — l'accessibilité | une démonstration, pas une liste | le **lien d'évitement mort** (voir ci-dessous) ; une **étiquette masquée est permise, une étiquette vide non** ; le **contraste dépend de la taille** (16 px échoue, 24 px passe, 23 px échoue encore) ; l'accordéon n'est pas tabulable — **mais notre FAQ est en `<details>` natif**, donc concernée par rien ; les vidéos ont besoin de sous-titres et d'un bouton pause ; et la règle d'or de l'`aria-label` : **seulement quand l'icône est le seul nom** |

### Ce que j'ai fait de vérifiable — et ce que j'ai refusé de faire

**Ajouté** : deux contrôles durcis dans `tools/qa/audit_a11y.py` — un lien d'évitement dont **la cible
n'existe pas** est une faute, un lien d'évitement **caché pour toujours** aussi, et une **étiquette vide**
aussi. Trois témoins fautifs neufs, deux assertions de plus, et le témoin sain qui verrouille le motif
réel de nos pages (`.skip{left:-9999px}` + `.skip:focus{left:0}`). Nos quatre pages passent : elles ne
mentaient donc pas, mais **notre contrôle, lui, ne le savait pas** — il acceptait n'importe quel lien vers
nulle part.

**Refusé, exprès** : un second contrôle de contraste. `audit_html.py` calcule déjà les ratios depuis le CSS
du fichier, avec la nuance de taille (4,5:1, puis **3:1 au-delà de 24 px ou 18,66 px gras**) et la
composition des transparences. La vidéo **confirme** notre règle, elle ne la change pas ; deux outils qui
mesurent la même chose finissent par se contredire.

**Écarté, parce que ça ne nous concerne pas** : l'accordéon d'Elementor (notre FAQ est du `<details>`
natif, tabulable normalement — aucun texte caché n'est dû), et les sous-titres vidéo (nous n'embarquons
aucune vidéo : zéro élément `<video>` sur les six pages ; la règle est écrite en §30.2 pour le jour où un
client nous donnera des images).

### Les deux corrections que ce lot m'a values

1. **Ma quatrième erreur d'instrument.** Un script rapide a annoncé « 2 liens-icônes sans nom » sur la
   page école : faux, tous deux sont nommés par leur **texte**, et l'outil d'audit compte le nom comme
   attribut **ou** contenu depuis le lot [28]. Rien corrigé sur la page, et la règle est écrite.
2. **Une affirmation que j'avais écrite sans preuve.** J'avais rédigé, dans le nouveau document, que
   UNI-LABO avait une fiche Google « trouvée par notre relevé Maps ». La ligne du CRM dit
   `source : directory`, et la vignette que je regardais (`clients/douala-cliniques/07-unilabo.jpg`) est
   **notre propre maquette**. Corrigé dans le document, avec la correction datée : le cas prouvé du
   pipeline, c'est **Univers Optique** — fiche Google notée 3,3/5, **champ « site web » vide**, domaine
   mort depuis janvier 2024, et rendez-vous vendredi 10 h où la question est déjà posée.

### Le verdict d'absorption

**Absorbé** : les 20 points d'Ignite Visibility (inventaire), l'ordre d'installation de Santrel, la
catégorie et les pièges de Zanet, la règle du `wa.me`, et les trois règles d'Imran devenues des contrôles.
**Retenu avec réserve** : les conseils d'avis des trois vidéos — nous ne dictons pas le vocabulaire d'un
avis, nous ne l'achetons pas, nous ne l'échangeons pas contre un prix (voir §30.4, point 1).
**Écarté** : le vocabulaire de vente des trois chaînes américaines (le « donut », les outils payants cités
— Local Falcon, GMB Everywhere, Answer Socrates, Lo — que nous ne pouvons ni acheter ni vérifier depuis
Douala), et leurs promesses de classement.

**Ce qui reste non vérifié, et donc jamais écrit dans une offre** : les méthodes de vérification
réellement disponibles au Cameroun, la présence du chat SMS/WhatsApp dans les profils du pays, les
catégories disponibles en français. Trois sources américaines et britanniques ne prouvent rien sur une
fiche camerounaise.

**Le désaccord méthodologique à noter :** pour 5 et 6, les sources utiles ne sont pas des vidéos YouTube.
Le lot [26] a montré le plafond de ce format (deux vidéos sur cinq muettes, et les autres vendent une
communauté payante). Les meilleures sources sont les documents officiels (Google, WhatsApp, W3C) et
**nos propres archives** — le journal contient 79 citations de leads, c'est notre meilleur manuel de
langue.

