# Playbook Addendum #4 — Marketing Systems (offer, proof engine, loops, local launch)

**Date:** 15 Sep 2026 · **Status:** CONTROLLING for AMK's own marketing and the Growth Care retainer deliverable. Extends Addendum #3 (conversion design). Companion craft standard: `design/CRAFT-FLOOR.md`.
**Source:** Corey Haines' **marketingskills** library (50 skills, MIT), studied 15 Sep. Skills applied: cro, ab-testing, offers, pricing, referrals, marketing-loops, social, video, sms, schema, directory-submissions, customer-research, copywriting, lead-magnets, analytics, marketing-psychology. SaaS-specific skills (paywalls, churn, aso, cold-email, popups, programmatic SEO) reviewed and **rejected as not applicable** — logged so they aren't re-studied.

---

## 1. The founding offer, audited (Value Equation + six-component anatomy)

Value = (Dream outcome × perceived likelihood) / (time delay × effort). Most "lower the price" pressure is really a broken numerator/denominator lever — never answer it with a discount (also: discount-askers churn ~2× and the coupon anchors us cheap; **100 000 FCFA never discounted**, standing law).

| Lever | AMK standing move |
|---|---|
| Dream outcome ↑ | Not "a website" — *the phone rings with admissions/appointments; parents abroad enrol by WhatsApp; you own the patient relationship instead of renting it from a directory* (mondocteur237 lesson). |
| Likelihood ↑ | The named live preview BEFORE payment is the guarantee mechanism: they see their exact site working. Add: 3–5 day delivery promise, handoff training video, EN+FR visibly working, our own live track record page. |
| Time delay ↓ | 3–5 days to live; concept within 24h of a warm yes (already SOP). |
| Effort ↓ | Done-for-you: we write bilingual copy, wire WhatsApp, build the proof/FAQ sections, submit sitemap. Client's only inputs: logo/crest, photos, real prices/hours, Google login for GBP. |

Six-component audit (must all be present when presenting the offer):
1. **Core deliverable** — bilingual mobile-fast site, WhatsApp funnel, proof/FAQ/schema, live in 3–5 days.
2. **Bonus stack** (candidates, each with real cost-to-us, never inflated): GBP claim+verification walkthrough; local citation setup (§4); 30-day post-launch content tweaks; handoff screen-recording; WA Business profile tidy. Propose the exact included set to King — do not promise unilaterally.
3. **Guarantee** — current de-facto: nothing paid until the named preview is approved (50/50 deposit then balance at handoff). This is strong; consider wording it explicitly: *"You approve your site on your phone before the balance."* King to confirm before use.
4. **Scarcity** — ONLY the real 2 founding slots/month, stated with the month. No timers, no "3 people viewing", no expiring discounts (Addendum #3 honesty rule).
5. **Name** — "Founding Client build" is the offer name; keep it.
6. **Price + structure** — 100 000 FCFA, 50/50, round number (round = premium/fluency; charm 99-pricing signals discount value — banned for us).

**Banned vocabulary in all pitches/pages/captions** (course-bro tells that pattern-match to scam): game-changing, revolutionary, disruptive, next-level, 10x, secret, "what they don't want you to know", "limited time" without a real limit, inflated "$X value", unconditional "100% guaranteed". Use specific numbers, named outcomes, real timelines.

## 2. CRO hierarchy and the small-traffic correction to A/B testing

CRO analysis order (impact): value-prop clarity (5-second test) → headline specificity/message-match → CTA copy+placement (verbs + outcome, never "Submit"/"Learn More") → scannability → proof near claims and CTAs → objection handling (FAQ) → friction (fields, taps, load). Addendum #3's page formula already embodies this.

**Critical correction — classical A/B testing is impossible at our clients' traffic; fake tests are worse than none.** Sample sizes needed for a trustworthy test (per variant):

| Baseline conversion | Detect 20% lift | Detect 10% lift |
|---|---|---|
| 1% | 39 000 visits | 150 000 |
| 5% | 7 000 | 27 000 |
| 10% | 3 000 | 12 000 |

A Cameroon SMB site on 40–500 visits/month would need *years* per test — the result would be noise dressed as science. Rule:
- **Below ~1 000 pageviews/month:** no A/B tests. Ship ONE researched best-practice change per iteration (the skills libraries + cross-client evidence), log it in a dated change log with the hypothesis and the source, and watch directional signals (WA message volume the client reports, GSC clicks/impressions, GBP calls).
- **Above ~1 000/month (or Growth Care clients after 2–3 months):** test one variable, pre-commit to sample via Evan Miller's calculator, no peeking, one primary metric + a guardrail.
- **Our own funnel** uses before/after across sends (subject lines/msg-1 variants on fresh prospect batches) — treat as sequential learning with notes, not significance claims.
- This amends Addendum #3 gate C12 (now: *"named change-log entry: change + hypothesis + source; or a real powered test if traffic qualifies"*).

## 3. Measurement without paid tooling

Track for decisions, not vanity. Free stack:
- **Google Search Console** (already in launch checklist) — impressions/clicks/queries; monthly Growth Care report.
- **GA4, two conversions only:** `wa_click` (wa.me taps, with page/section label) and `tel_click`. Install note in kickoff kit; event code snippet lives with the launch checklist.
- **UTM discipline** for every link WE distribute: named concept links get `?src=wa` / `?src=qr-card` / `?src=tiktok-bio`; every client-side link we put in messages carries a source so GSC/GA shows which leg worked. Never UDM a client's organic pages.
- Client-reported leading indicators kept in CRM: WA messages/week ("the phone is ringing"), GBP review count, GBP directional calls.
- No heatmaps/session-recordings/paid SEO tools on 100k budgets (standing rejection reaffirmed; privacy and 3G weight also argue against them).

## 4. Local launch layer — the new launch deliverable (citations, not SaaS directories)

The directory skill's SaaS catalog (Product Hunt etc.) is irrelevant; its Tier-9 *local business* logic is gold and matches what the Douala sweep proved: **directories already route WhatsApp demand** (JOSS MEDI: 292 WA clicks; La Béthanie: 210; YAKS/Skye live entirely on FB). At each client launch:

1. **Google Business Profile: claim or create + verify** (postcard/SMS) — the single highest-value SEO action for a local CM business; owner does the verification step, we do everything else; categories (MedicalClinic/Dentist/Laboratory/School), hours, services, bilingual description, photos, website URL.
2. **NAP lock:** Name/Address/Phone written identically everywhere we touch.
3. **Cameroon citation set (start here, expand by city):** Facebook Page (primary social), TikTok/Instagram where active, DoualaTour/annuaire listings, goafricaonline, africannuaire, plus the directory where the client's type already gets WA clicks (check during research). For Buea: repeat the sweep method to find the local equivalents before launch.
4. **Review flywheel:** at handoff, set up the client's own *"after each happy visit/term, send one WA message with the Google review link"* habit — a pre-written bilingual one-liner they forward. Reviews power the proof strip and local pack ranking; G2-style incentive protocols do NOT apply; never buy or fabricate reviews (accuracy law; Google bans).
5. Directory/citation consistency is a Growth Care monthly check (NAP drift, dead links).

## 5. Growth Care = a set of marketing loops (formalised)

Loop anatomy we hold ourselves to: trigger/cadence matched to signal speed · acts-when condition · self-check before acting · state/dedupe · explicit stop condition · human checkpoint before anything publishes or spends. Cadence reality check: rankings move weekly (never daily); social listening daily; content decay monthly. **"A weekly conversion-rate loop on 40 visitors is measuring noise"** — loops without a real audience get deleted, not automated.

Standing loops (folded into the retainer one-pager and `leads/Daily Ops.csv` rhythms):

| Loop | Cadence | Acts when | Stop/bail |
|---|---|---|---|
| GSC + Bing Webmaster report | Monthly | client site live ≥30 days | client churns |
| GBP/post + review nudge content (drafted for client to post) | Monthly (2 posts/mo) | client has a real update/photo | 2 no-shows in a row → ask, then pause |
| NAP/citation drift scan | Quarterly | listing mismatches found | all consistent → no action run |
| Cluster page (2/term per Addendum #2) | Quarterly | GSC shows the query impression exists | no query signal → don't manufacture |
| Review-rhythm check (client forwarding their one-liner) | Monthly after handoff | new review appears | — |
| AMK: prospects whose competitor/site trigger fires (e.g. St Theresa October site) | logged per lead (FU 14 Oct) | trigger verified true | FU3 silent → stop, per cadence law |

Human checkpoint: AMK never posts as the client and never spends on their accounts (matches King-posts-everything rule).

## 6. Social content system for AMK's own accounts (King posts)

**Five pillars (%), replacing ad-hoc posting:**

| Pillar | % | AMK content |
|---|---|---|
| Education/demo | 30 | screen recordings of the bilingual toggle, one-tap WA booking, Student Corner, fees-on-phone (the 4 founding videos seed this) |
| Proof/results | 25 | "this clinic had 292 WhatsApp clicks from a directory and no site" teardowns; client launches (with consent); before/after Google-name search |
| Behind-the-build | 20 | 3–5 day build timelapses, why no stock photos, FR/QA on a real Android in sunlight |
| King/personal | 15 | Buea builder story, what parents abroad message him, one founder's opinion on local business sites |
| Promotional | ≤10 | founding slots status, one CTA |

Mechanics from the video/social skills:
- 85% of social video is watched muted → burned captions mandatory (our compositor already does this); 9:16; ≤29 s for the founding series; authentic > over-produced on TikTok.
- **Repurpose each pillar asset into atoms:** one site launch → 1 vertical screen recording, 1 "feature in 20s" clip, 1 static mockup post (FB), 1 LinkedIn-style text post for the AMK Page, 3 stories (build moments). Never start from scratch.
- Hooks from the formula bank (first line decides): curiosity ("I was wrong about how parents choose colleges here"), value ("How a Douala clinic takes bookings without a receptionist"), contrarian ("A beautiful website that doesn't ring the phone is a cost, not an asset"), story ("Last week a school told me it was 'already late'…" — St Theresa-style, anonymised).
- Every post ends with exactly ONE action: DM keyword CLINIC/SCHOOL (matches videos), or "comment the quarter" — one CTA rule.
- Frequency sanity over heroics: 4–5 posts/week King can sustain beats 14 then zero. The 4 rendered videos are the month-one bank; schedule EN then FR mirrors and YouTube Shorts.

## 7. WhatsApp prospecting guardrails (SMS skill applied to our one channel)

Text/SMS compliance principles map directly onto WhatsApp Business norms (ban risk replaces TCPA fines):
- One message, one ask, one link (standing ≤5-line law reaffirmed).
- Identity + sign-off in every send (already required).
- Quiet hours 09:00–21:00 recipient-local (already required) — matches the skill's 9–8 carrier norm.
- Image-first MMS msg 1 (our -wa.jpg rule) is the right analog; text-only where image would feel like bulk.
- **No blasts:** every send is personalised, named, research-backed; never paste a shared template across many numbers in a session (WA spam heuristics flag identical text; also our own accuracy/named-gift law). Volume cap stays human-paced; if we ever scale beyond ~15 new conversations/day, that is a WA Business API decision with opt-in flows, not a personal-line hack.
- Honour "not interested" instantly and permanently (our stop cadence already does this); never re-add.
- No automated follow-up software on King's personal line.

## 8. Voice-of-customer at kickoff (copy quality source)

The converting copy lives in the client's head; AI-generic copy underperforms. Kickoff kit must collect verbatim:
1. The **3 questions asked most often on the phone/WhatsApp** (word for word, EN and FR) → these become FAQ and FAQ schema.
2. The exact words patients/parents use when they arrive anxious ("how much?", "do you have bedspace?", "you people dey for WhatsApp?").
3. What clients say when they praise the business (proof quote material, used only with permission).
4. The alternatives families actually chose (doing nothing, the directory, Facebook, travel) → objection content.
Jobs-to-be-done triple for hero copy: functional (book/enrol), emotional (certainty, dignity), social (seen choosing a serious school/clinic).

## 9. Referral loop — installed at every handoff

Trigger moment = launch day / first unsolicited compliment (never at pitch). Mechanism: give the new client a **pre-written WhatsApp message they can forward to one neighbouring business** (one tap, their name attached):
> "My new website was built by Akwo King at AMK — bilingual, parents/patients reach us on WhatsApp directly. He builds only 2 clients a month; if you want an intro, say so and I'll connect you."
Reward (King to confirm shape): double-sided small thank-you (e.g. referrer gets one free extra Growth Care month / free flyer design; referred business gets the same). Referral stats from the skill (16–25% higher LTV, referred clients refer again 2–3×) justify the small cost. Track referral source in CRM. Denominational/board clients are excluded from referral asks; lay-private owners only.

## 10. Psychological map of our existing moves (so we use them deliberately)

| Principle | Where AMK already uses it |
|---|---|
| Reciprocity | Free named preview built before any money; free St Theresa post-launch review |
| Commitment & consistency / foot-in-door | Msg 1 asks only "may I send it?"; every chat ends with a booked next step (BAMFAM) |
| Liking + Unity | Buea-based, bilingual, "one of us"; same-quarter vernacular in FR |
| Authority | Verified facts (camgceb.org marking centres, directory click counts), our own live demo |
| Social proof / bandwagon | Addendum #3 proof strips; directory demand numbers as pitch ammo |
| Loss aversion (honest) | "Parents who Google the name find nothing and enrol elsewhere" — real, stated without exaggeration |
| Anchoring | $500/$5 000/$50 000 website tier walk for Fiverr objections (Addendum #3 §6) |
| Default effect | Offer two walkthrough choices with a default ("WhatsApp now, or 10 minutes Thursday?") |
| Peak-end | The handoff screen-recording + first-month support is the memorable ending; FUs end warm even on rejection |
| Goal-gradient | 3-step booking progress shows steps 1→3; "2 of 2 founding slots this month" |
| Hyperbolic discounting | 3–5 day delivery and same-day previews beat "we'll get to it" competitors |
| Paradox of choice (≤4) | ≤2 hero CTAs, ≤4 nav items, invite gives 2 options not 6 |

Manipulative uses (fake scarcity, countdowns, invented urgency, disguised ads) are permanently out — they pattern-match to the scam aesthetic that destroys trust in exactly our market.

## 11. Rejected skills (reviewed, do not re-litigate)

Cold-email/email sequences (email is never a leg), popups/exit-intent (3G friction + cheap feel), paywalls/signup/onboarding/churn (SaaS only), programmatic SEO at scale (no content farm — Addendum #2), paid ads skills (no paid acquisition phase; revisit post founder-clients if King chooses), co-marketing/events (all-remote phase), ASO (no app), affiliate networks (service business, referral loop suffices), influencer marketing (King's own accounts are the channel).
