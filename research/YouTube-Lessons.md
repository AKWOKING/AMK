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

## 6 · Weekly ritual (Mondays, before the outreach pack goes out)

1. Re-read the last 7 days of entries in §3/§4.
2. Surface the **top 3 lessons that should change how we operate this week** — each one must name the file it changes and the concrete move it changes.
3. If a lesson contradicts the playbook: state the conflict and ask King which side wins (unless the video is clearly stronger evidence — then propose the change and wait for the yes).
4. Log the Monday summary at the top of §3 as a dated row so the ritual itself is auditable.
