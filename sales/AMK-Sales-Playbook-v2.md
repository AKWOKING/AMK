# AMK — Sales Playbook v2.2 (09/12 · updated 17/09)
**Synthesized from 4 videos → optimized for AMK's exact context (WhatsApp-first, schools + clinics, free concept previews, ₦100k 50/50, King's standing rules).**

> **v2.1 changelog (17 Sep 2026 — copywriting batch of 6 videos, see `research/YouTube-Lessons.md`):** added **Part H — the customer-language system** (customer interviews as ingredient harvest; the WhatsApp-default reframe; claim→proof discipline). No existing rule was deleted or overwritten. The copy law itself (Harry Dry's 3 questions, 2-Mississippi, read-aloud) lives in `sales/Monday-Outreach-Pack.md` (cold messages) and `AMK-DESIGN-SKILLS.md` §11b (site copy) — Part H is the sales-specific slice only.
>
> **v2.2 changelog (17 Sep 2026 — sales batch, videos [7] Hormozi 3A and [8] CLOSER):** added **Part I — the 3A reframe** (objection handling with Acknowledge · Associate · Ask, now the house method for written/WhatsApp objections) and **Part J — CLOSER for the WhatsApp era** (clarify→label→pain→vacation→concerns→reinforce, yes/no decision chain, always-ask, reinforce-the-decision sequence, one-taxonomy objection log). Nothing deleted. Two guardrails added: straw men only with **true** references (accuracy law), and the pain cycle is capped inside discovery — it never extends the no-chase FU rule (M+2/+4/+7 then stop).

> **M7 changelog (21 Sep 2026 — CRM migration, King's ruling).** The pipeline now speaks ONE stage vocabulary — `prospect → qualified → presented → closing → won → delivered`, plus `parked` and `lost` — the same five beats as `sales/AMK-5-Stage-Funnel.svg`, with `won`/`lost` added and `delivered` kept separate (paid ≠ delivered, and that seam is where a client dies). Two rules were settled today: **(1) the kill list is DERIVED, never hardcoded** — King confirmed the 19 Sep correction to §A4, and a reply always outranks it (the 90-second rule); **(2) the no-cold-calls rule is now written here as a standing rule** — it had been operating since 14 Sep only as a routing preference (`Contact channel`, `Invitation-First-Replan`). Fields were added to `leads/CRM.csv` (`first_touched`, `stage_since`, `last_reply_received`, `preview_sent`, `proposal_sent`, `price_quoted_fcfa`, `invoice_sent`, `closed_on`, `closed_value_fcfa`, `bamfam_next_action/step`, `health_override`, `gtd_filter`) — see `leads/build/crm.py` header. Nothing in this file was deleted.

> **Addendum (15 Sep evening):** [`AMK-Playbook-Addendum-Outcomes-2026-09-15.md`](AMK-Playbook-Addendum-Outcomes-2026-09-15.md) synthesizes 5 newer AI-agency videos — outcome (not website) framing, the gift-preview validation, Google-Maps no-website prospecting, the optional Care Plan retainer (FCFA/MoMo), monthly reports, and the handoff-video delivery step. Standing rules in this file still override; pricing changes in the addendum are proposals until King approves.

Sources:
1. Alex Hormozi — *Sales Was Hard Until I Understood These 9 Concepts* (51 min) — the ENGINE (opportunity × conversion × consistency)
2. Adam Erhart — *10 Dark Psychology Sales Techniques (Ethically)* (21 min) — the MIND (framing tactics)
3. Natalie Dawson — *$100M Worth of Sales Knowledge in 19 Minutes* (20 min) — the MINDSET (belief, authenticity, the close)
4. Patrick Dang — *8 Dark Psychology Sales Techniques* (19 min) — the CLOSE (pain ladder, price+pause, their words)

**Standing rules that override everything:** no sell in message 1 (goal = "send me the preview") · max 3 FUs · pain statements ONLY from verified facts · never name a specific competitor school/clinic · no fake scarcity (small-city networks poison themselves) · sign AKWO KING · never discount — trade scope/timing, not price.

---

## PART A · THE ENGINE (Hormozi's 3 jobs)

A salesman has 3 jobs: **maximize opportunities → convert the highest % → stay consistent for a long time.**

### A1. Availability is the #1 lever
> "Availability was the strongest predictor of total sales."

- **1-hour reply rule:** answer every WA/Messenger between 09:00–21:00, 7 days (including Sunday — "businesses pay rent on Sundays"). A principal who gets a reply in 40 minutes feels chosen; one who waits 3 days feels like option #6.
- Speed-to-lead is the single biggest conversion lever in our whole funnel. The concept takes hours; the *reply* takes 90 seconds.

### A2. Pull it up
- They say "can we talk Thursday?" → "Actually I have a slot tomorrow at 15:00 — does that work for you?" Same/next-day beats the date they picked. If they can't, book the earliest you can AND fill the freed slot with the next lead.
- Any reply that goes quiet for 24h → one gentle nudge that offers a new time ("I know this is busy — tomorrow 16:00 instead?").

### A3. BAMFAM — Book A Meeting From A Meeting
- **No conversation ends without a scheduled next step.** Not "let me think about it" → silence. Always: "I'll send the preview Tuesday 09:00 — I'll ping you the moment it's out." Both calendars know what happens next.

### A4. The Kill List
- The 2 leads at 18 (COMOBIL, OraCare) + any lead who just said yes → written on a visible "TODAY" list (CRM top rows). They get the extra attention daily until they close or park.

> **⚠️ CORRECTION — 19 Sep 2026 (CRM M2, `leads/CONTRADICTIONS.md` §1).** This line is **wrong as written** and must not be followed literally: **COMOBIL has been `parked` since 14 Sep** (King's decision — the DAILY OPS tab says so itself), so it does not belong on a "TODAY" list. An earlier audit claim that DAILY OPS contradicted `Pipeline-Status` on this was **checked and infirmed** — both files agree.
> **The rule, corrected:** the kill list is **derived** from the CRM, never written in hard: *score ≥ 18 **and** stage ≠ `parked` **and** stage ≠ `disqualified` **and** the lead has not just been contacted.* With the current data that leaves **OraCare** alone, plus anyone who replies. `KILL-LIST.md` will be generated from `leads/CRM.csv` in M6 — this paragraph then becomes the spec for that generator.

### A5. Referrals: "Who do you know?"
> A new rep who asked "who would you like to bring?" outperformed #2 by ~50% — only 1 in 4 refers, but referrals close at 80–90%. CAC effectively halves.

- Ask it **twice**: (1) when handing over the concept, (2) at close. The compliment sandwich:
  - EN: "Before we finish — who do you know that's like you? Another principal, or a clinic owner, who'd benefit from this? A referral from you is the best thing that could happen to my little agency."
  - FR: "Avant de finir — qui connaissez-vous qui est comme vous ? Un autre directeur, ou un propriétaire de clinique, qui en bénéficierait ? Un parrainage venant de vous serait la meilleure chose pour ma petite agence."
- The Diocese of Buea is ONE network. One Sasse win should produce 3 names.

### A6. Prep = 10% of call time, come with solutions
- Before every call: 10 minutes. Re-read that lead's Deep-Dive section. Choose **one personalized opening fact** ("I saw your 100% GCE results — 82 students…" / "Your smile-makeover ad is running right now…").
- "The big guys have reputation; the small guys win through preparation." AMK = the small guy. The Deep-Dive research is the weapon — use it in minute 1 so they feel *known*.

### A7. Listen 2× more than you talk
- Best salespeople (per AI call analysis): listening twice as much as talking.
- **Answer questions with questions.** "What makes you better than the other agency?" → "Good question — what's most important to you: the design, the speed to launch, or the support after?" They believe everything THEY say, nothing you say.
- Ask the discovery trio (schools): "How many registrations did you get last term? / What do parents ask you most on the phone? / When do you open for registration next?" (clinics): "How do new patients find you today? / What do they ask before coming? / Do you keep emergency slots?"

### A8. Know the script like breathing — drill the 30-second open
- 15 minutes a day, daily: the 30-second open + price+pause + the 5 objection flips. With a friend, a family member playing "principal", or voice memo. **Never practice on real leads.**
- One segment at a time (this week: the price+pause only). Three "bangs" in a row clean, then move on.

### A9. Be concise — 5 words when 100 do
- Every WA message ≤ 5 lines (except the concept handover). Long messages get read as homework.

> **M7 soirée (21 Sep 2026, 18:20 — King's screens corrected my read).** Three standing rules added, nothing deleted:
> **(1) A deferral is not a consent.** "je vous reviens" / "Ok" / a 🙏 means *not yet* — never "he agreed,
> send the price and the full page". Bonanjo is the case: page + 100 000 FCFA went out on a "je vous reviens"
> and the thread has been silent 29 h. A follow-up that assumes agreement ("j'attends votre feu vert",
> "comme convenu") is now a **defect in the copy**, not a style choice: ask for an *opinion*, offer an exit.
> **(2) Never count a send the CRM cannot prove — and never un-count one it can.** King's screenshots found
> three messages that had never been registered (OraCare's 14/09 13:04, AFRIQUE LABO's 21/09, Baird's 17/09
> 13:48) and one that looked sent but wasn't (Bely: number not on WhatsApp → **channel incident**, not a
> failed follow-up). **(3) Look up a lead by NUMBER in the generated CSV, never by name in the code.**
> I "discovered" AFRIQUE LABO was missing from the CRM and added a second row for the same laboratory; the
> row already existed as `afrique-labo-douala`. `crm.py` now **fails the build** if one number appears on two
> rows — and that guard immediately caught the 18/09 CEMECES/INSES number swap, which is now fixed by
> *removing* the number from the wrong row rather than by exempting it.

### A10. Consistency system (the 3rd bucket — "do it for a very long time")
- **Lives in the workbook:** `leads/leads_50.xlsx` → **"DAILY OPS" tab** (first tab, opens by default) — Kill List + Reply Queue + this week's drill + tonight's 5 min.
- **Morning (10 min):** open DAILY OPS → check Kill List → check Reply Queue → 15 min drill.
- **Same day:** log every send/reply in `Leads 50` + `Daily Tracker`.
- **Sunday (30 min):** review pipeline, schedule next week's FUs (M+2/M+4/M+7), prep top 3 leads' Deep-Dive pages.

---

## PART B · THE MIND — Erhart's 10 tactics, AMK version

### B1. Latent → Realized → Extreme pain (the 3-year question)
People don't move until staying put feels worse than changing. Use **verified facts only** — our D/E sites ARE the pain, no invention needed.
- **Latent:** "Your Facebook page is doing well, right?" *(they agree — the pain is invisible to them)*
- **Realized:** "When a parent Googles '[school name]', what comes up first?" *(truth: nothing / expired domain / a template with another school's name — SAHISCOL, Retraite, COMOBIL each have their own verified answer)*
- **Extreme (one level only):** "Every open day, some of the parents in the room have already Googled you. Right now the first thing they find is [X]. Next term the question isn't whether they'll search — it's **who they find first**."
- The 3-year question (call, after trust is built): "What do you want this school to look like in 3 years — and what would it take to be the first name parents see?"

### B2. Perceived control — they decide, you choose the path
People resist being sold; they don't resist choosing.
- **Micro-agreements** in every FU: "Can I show you what's been working for other schools in the region?" / "Puis-je vous montrer ce qui a marché pour d'autres écoles de la région ?"
- **Double binds** (both roads lead forward): "Would you rather I send the preview as a link or a short video?" / "Vous préférez l'aperçu en lien ou en petite vidéo ?" · "Shall we start with the homepage, or the full site?"
- **Decision framing, never demand:** "Here's the path I'd take if I were in your shoes — it's totally your call."

### B3. The Pit — share the struggle, not the success
> "The lower the pit, the higher the payoff. No one buys the perfect origin story. They buy the comeback."

AMK's pit (WA Business profile "about" + one line on calls, never a whole paragraph):
- EN: "I started AMK because I kept seeing brilliant schools lose parents to schools that just *looked* bigger — not better, more visible. My first builds were slow and imperfect; every one since has been faster. I tell you that because you'll get the honest person, not a polished pitch."
- FR: "J'ai lancé AMK parce que je voyais des écoles brillantes perdre des parents au profit d'écoles qui semblaient simplement plus grandes — pas meilleures, plus visibles. Mes premiers sites étaient lents et imparfaits ; chacun depuis est plus rapide. Je vous le dis parce que vous aurez la personne honnête, pas un discours poli."

### B4. The Adventurer frame (AMK has no track record — make it the superpower)
- "I'm building something small on purpose: a studio that builds schools first, clinics second. Every build teaches me how Cameroonian parents actually browse, and it goes into the next build. You work with the person — not a call center."
- FR: "Je construis quelque chose de petit exprès : un studio qui construit d'abord les écoles, puis les cliniques. Chaque site m'apprend comment les parents naviguent vraiment, et ça rentre dans le suivant. Vous travaillez avec la personne — pas un call center."

### B5. Throw rocks at the enemy (never a named school — the enemy is the *category*)
- Enemy list (use in pitch, one per conversation): **(1)** the template site with another school's name on it; **(2)** the expired/dead domain that looks like the school died; **(3)** "we have a Facebook page, so we're fine" thinking.
- EN: "Most schools in the region are in one of two places: a Facebook page, or a template site that looks like someone else's school. Parents compare schools on Google now — the ones that show up as *themselves*, with real results, get the calls."
- FR: "La plupart des écoles de la région sont dans l'une des deux situations : une page Facebook, ou un site modèle qui ressemble à l'école de quelqu'un d'autre. Les parents comparent maintenant les écoles sur Google — celles qui s'y montrent vraiment, avec leurs vrais résultats, reçoivent les appels."

### B6. Objection inversion (the flips — see Part E for full EN/FR scripts)
Objections are doors, not walls. Agree → reframe as the reason to act:
- "I can't afford it" → "If more parents finding and registering is the problem — isn't that why we're talking?"
- "I've been burned before" → "And how much longer do you want to keep operating with what's not working?"
- "I'm not ready" → "Waiting rarely makes you more prepared. Action does."

### B7. Future pacing (Polaroid language — paint the scene)
- **School:** "Picture open day. A parent walks in and shows their phone: *'I already saw your site — the results, the dorms, the registration form. I'm registering my brother's child.'* The site sells while you teach."
  - FR: "Imaginez le jour portes ouvertes. Un parent entre et montre son téléphone : « J'ai déjà vu votre site — les résultats, les chambres, le formulaire. J'inscris l'enfant de mon frère. » Le site vend pendant que vous enseignez."
- **Clinic (Oracare):** "Imagine a parent tapping your smile-makeover ad and landing on a page with your name, your clinic at St. Pius, real photos of the room, and a Book button that lands on your WhatsApp. That's what's in the preview — waiting for your real photos."
  - FR: "Imaginez un parent qui touche votre pub 'smile makeover' et atterrit sur une page avec votre nom, votre clinique au St. Pius, de vraies photos de la salle, et un bouton « Réserver » qui atterrit sur votre WhatsApp. C'est ce qui est dans l'aperçu — il n'attend que vos vraies photos."

### B8. Status shift framing (sell identity, not features)
- "This is what the top private schools in Douala are doing this year." / "C'est ce que les meilleures écoles privées de Douala font cette année."
- "This is how principals who take open days seriously get found." / "C'est comme ça que les directeurs sérieux sur la rentrée se font trouver."
- Before/after identity: from *"a school with a Facebook page"* → *"the school that comes up first when parents search."*

### B9. Identity activation
- "If you're the kind of principal who treats open days as the biggest marketing moment of the year — this is for you."
- FR: "Si vous êtes le genre de directeur qui traite les journées portes ouvertes comme le plus grand moment marketing de l'année — c'est pour vous."
- After they say yes, confirm the identity: "That's exactly what schools that grow do — you made the smart move."

### B10. Dangerous simplicity (the one-sentence offer)
- **The spine (everything else is detail):**
  - EN: "I build your school's website — your name, your colors, your photos — so parents who Google you find you first. Preview in 24 hours, live in 3–5 days."
  - FR: "Je construis le site web de votre école — votre nom, vos couleurs, vos photos — pour que les parents qui vous googlent vous trouvent en premier. Aperçu en 24 h, en ligne en 3–5 jours."
- Clinic variant: "…your clinic's website — your name, your services, your photos — so patients who Google you can book in 30 seconds."
- Test: can a student in Form 2 repeat it back? If not, cut more.

---

## PART C · THE CLOSE — Dang's 8, AMK version

### C1. Pain > Pleasure, in that order
Open with verified pain (site status, what Google shows today) → THEN the concept (pleasure). Never lead with features ("6 pages, bilingual, responsive…") — that's what the concept *shows* while they watch it.

### C2. The pain ladder on WhatsApp (ethical version)
Only facts. Sequence across the conversation, never one message:
1. (msg 1 — done in pack) the observation + free preview ask
2. (after they see it) the *realized* pain: "This is what a parent sees today when they Google you: [verified screenshot]."
3. (call) the *extreme* level — one sentence: "Every open day, some parents have already searched. Right now the first result is [X]."
Then stop. Let it sit. Future-pace (B7) is the exit.

### C3. Mirror the negatives, flip to positives (call technique)
- Reflect: "So parents call every morning asking registration hours, and that eats your first two hours?"
- Flip: "That's exactly what the registration section kills — they self-serve, you get the calls that matter."

### C4. Close without negotiating: **price + pause**
> Say the price with confidence, then say nothing. Let them find a way to afford it instead of finding a way to cut it.

- EN: "For the full site — every page you saw, in English and French, live in 3 to 5 days — it's **100,000 francs, half to start**." *(pause. Do not justify, do not smile-apologize, do not add 'but'…)*
- FR: "Pour le site complet — toutes les pages que vous avez vues, en anglais et en français, en ligne en 3 à 5 jours — c'est **100 000 francs, la moitié pour commencer**." *(pause.)*
- If silence stretches: "That includes hosting and the bilingual content — anything I should walk through?"
- **If they push price:** trade scope/timing, NEVER price: "We can start with the homepage this month and add the rest next term — same total, different rhythm."

### C5. Stories > claims (AMK has no client logos yet)
- Until first client: the *process story* is the proof — "Here's how I researched [their school] and found [verified fact]" + the concept itself + the 3-nameless templates.
- **After client #1:** collect testimonial + 2 photos + one number ("registrations in the first month"). Add to Kickoff Checklist as a formal step. Then the story becomes: "Here's where [school] was — broken domain — and here's where they are."

### C6. Their own words against them (timeline pressure — use ONCE, gently)
- They: "This is exactly what I wanted." … then "let's do it next month."
- You: "You said it's exactly what you wanted — so if I start this week, we're live before [open day/term]. What would change between now and then that makes the site less useful?"
- FR: "Vous m'avez dit que c'est exactement ce que vous vouliez — si je commence cette semaine, on est en ligne avant [la rentrée]. Qu'est-ce qui changerait entre maintenant et là que le site serait moins utile ?"

### C7. Obstacle math (commitment through their own numbers)
- "How many calls do you get a day asking about registration?" (say 10) "A site that answers 80% of them — worth 30 minutes of your time this week?"

### C8. The delivery IS the tactic
The "dark" part that's actually legal: **over-deliver.** 3–5 day promise → deliver day 3. They asked for a website → they get the website + WA booking + the chat assistant. In a referral market the size of Buea, delivery is the marketing.

---

## PART D · THE MINDSET — Dawson's 9, AMK version

1. **Get sold on the product.** AMK doesn't sell "websites." AMK sells *being found first* — enrollment visibility for schools, patient flow for clinics. If you can't believe that in a specific school, don't message that school (that's the MQL gate doing its job).
2. **Get sold on you — keep every micro-promise.** Preview in 24h → actually 24h. "I'll ping you Tuesday" → ping Tuesday. Every kept promise raises the next close.
3. **Sell the problem, not the car.** The Buick Century lesson: the parent doesn't want a website; they want to *stop losing registrations to schools that look more serious*. Ask what they're solving, then answer that.
4. **No aggression, just authenticity.** "Their money is in better hands with me" → AMK version: *"The 50/50 means I only win when you win — if parents don't start finding you, you tell me and we keep working."*
5. **No ≠ no — it means "show me, don't tell me."** That's why the free preview exists. Every "no" gets exactly one demo push (the concept link/video), then the FU clock.
6. **You are the bridge.** From "invisible on Google" to "first result." Take the driver's seat: you know where they can go better than they do.
7. **Practice 15 min/day** (see A8) — the skill compounds; the market is small enough that everyone you meet is a future referral.
8. **The Cardone question:** *"Have you heard enough to make a decision?"*
   - EN: "Have you heard enough to make a decision — or is there one thing I can still show you?"
   - FR: "Assez entendu pour décider — ou y a-t-il une chose que je peux encore vous montrer ?"
   - Use at the end of every preview walkthrough. Ask it early, ask it again later. People don't want to hear everything; they want to decide.
9. **Nothing blows the deal.** A typo'd first message, a 2-day delay, one clumsy call — log it, keep the FU cadence, remember people change their minds (open days are the trigger). Confidence survives mistakes; anxiety doesn't.

---

## PART E · THE OBJECTION HANDLER (5 flips, EN + FR)

| # | Objection | The flip |
|---|-----------|----------|
| 1 | **"It's expensive" / "C'est cher"** | EN: "I understand. Quick question: if more parents finding and registering your school is the problem we're solving — isn't that exactly why we're having this conversation? Let's compare: what is one missed registration worth per term?" · FR: "Je comprends. Petite question : si le but c'est que plus de parents vous trouvent et s'inscrivent — n'est-ce pas justement pour ça qu'on en parle ? Faisons le compte : combien vaut une inscription manquée par trimestre ?" |
| 2 | **"I need to think" / "Il faut que je réfléchisse"** | EN: "Of course. Usually when a principal says that, it's one of two things: timing, or the offer doesn't match a priority yet. Which one is it — so I can actually help?" · FR: "Bien sûr. D'habitude, quand un directeur dit ça, c'est l'une des deux choses : le timing, ou l'offre ne correspond pas encore à une priorité. C'est laquelle — comme ça je peux vraiment vous aider ?" *(perceived control + it usually surfaces the real obstacle — then apply Hormozi's three: circumstances / people / self)* |
| 3 | **"We already have a page" / "On a déjà une page Facebook"** | EN: "That's great — and I'm not asking you to replace it. Here's the question: when a parent taps your page, what do they find? A feed with 200 posts — or a page with your name, your results, and a way to register in 30 seconds?" · FR: "C'est bien — et je ne vous demande pas de la remplacer. La question c'est : quand un parent touche votre page, que trouve-t-il ? Un fil avec 200 publications — ou une page avec votre nom, vos résultats, et un moyen de s'inscrire en 30 secondes ?" |
| 4 | **"Send me a price list" / "Envoyez-moi votre grille tarifaire"** | EN: "I don't send a generic price list — I price per school, because every school is different. That's exactly why the preview is free: you see what I'd build for you, then I give you a number for that specific thing." · FR: "J'envoie pas de grille tarifaire générique — je fixe le prix par école, parce que chaque école est différente. C'est justement pour ça que l'aperçu est gratuit : vous voyez ce que je construirais pour vous, puis je vous donne un prix pour cette chose précise." |
| 5 | **"Let's do it next month / at the rentrée" / "Faisons-le le mois prochain / à la rentrée"** | EN: "That works — one thing: every week without the site, parents Google and find [verified X]. Shall I start this week so we're live before [date]?" · FR: "Ça marche — une chose : chaque semaine sans le site, les parents googlent et trouvent [X vérifié]. Je commence cette semaine pour qu'on soit en ligne d'ici [date] ?" |

**Hormozi's zombie check (before the price on every call):** three categories of hidden obstacles — **circumstances** (time/money/fit), **people** (who else must agree — spouse? co-director? bishop?), **self** (their own doubt). Surface them BEFORE the price:
- "Who else does this decision involve — do you consult anyone?"
- "What's the one thing you're worried about happening? Let's just play it out." *(then future-pace the worry into the ground: "Worst case? You've spent half of one term's registration fee… and the site keeps working for 10 years.")*

---

## PART F · THE CALL RUN-SHEET (after they accept the preview)

1. **Prep (10 min):** re-read Deep-Dive section · pick 1 personalized opening fact · note the last 2 things they said on WA.
2. **Open (30 sec, drilled):** "Good morning [name] — thanks for the time. Before I show you anything: I noticed [personalized fact — GCE results / the running ad / the dead domain]. That's what made me reach out. Can I show you something in 10 minutes?" *(micro-agreement = perceived control)*
3. **Show the concept (them scrolling, you mostly listening).** Their questions → answer with questions (A7).
4. **Pain, realized (one verified screenshot):** "This is what a parent sees today when they Google you."
5. **Future-pace (B7)** — the open-day scene / the ad-click scene. Let it land.
6. **Zombie check (Part E):** who else decides? what's the worry? play it out.
7. **Price + pause (C4).** Silence.
8. **"Have you heard enough to make a decision?" (D8).**
9. **If yes → the 50/50:** "Half to start — I'll send the details. You'll get the live site in 3 to 5 days, and I stay with you after launch." *(BAMFAM: agree the exact day you send the MoMo reference.)*
10. **Referral ask (A5):** "Who do you know that's like you…?"
11. **If no → graceful FU schedule** (M+2), log the objection verbatim in CRM.

---

## PART G · DAILY 15-MINUTE DRILL (this week's focus: PRICE + PAUSE)

1. Say the one-sentence offer (B10) out loud — 3 times, 5 seconds each.
2. The price+pause (C4) — say it, then stay silent for 10 full seconds. Record yourself; check you didn't add "but" or an apology.
3. One flip from Part E — say it, then answer your own follow-up.
4. Tomorrow: swap in the 30-second open. Friday: a friend plays "skeptical principal" for 10 minutes.

**Rule:** never practice on real leads. Practice on people who owe you nothing — and never send a drilled line verbatim; the drill makes it *breathe*, not robotic.

---

## PART H · THE CUSTOMER-LANGUAGE SYSTEM (v2.1, 17 Sep — from videos [4] and [6])

**H1 · Never originate the words.** The best copy is quoted, not written. Sources, in order: (1) the client's/prospect's own customers, (2) the prospect's own public words (FB posts, comments, signage, listings), (3) our own swipe file of messages that got replies (`sales/swipe/`).

**H2 · The 6-field ingredient sheet** — the questions for any discovery conversation (onboarding call for a delivered client; qualification for the close):
1. **Struggle** — what was happening before? what was frustrating?
2. **Solutions** — what did you actually use it for / expect it to do?
3. **Hesitations** — what worried you before saying yes? (unspoken here: price, trust, "will he disappear after payment?" — pre-answer in the offer, not the close)
4. **Awareness** — what are you comparing this to? *(expect: another clinic's Facebook page, the phone number on the door, "we already have a page")*
5. **Differentiators** — why choose us over the alternative?
6. **Success** — what does life/business look like after? (business outcome + the emotional one — a lab that no longer makes patients queue for paper results; a school where the parent stops calling the office)
Ask "anything else you'd like to add?" and then **stay silent** — the gold is in the answer to that question.

**H3 · The WhatsApp-default reframe (Alex [6]: "the default is Google Sheets and WhatsApp").** In Cameroon, a clinic/school is not competing with another website — it competes with a Facebook page and a WhatsApp status. Use this in qualification and in the close, verbatim if it fits:
- FR : « Vos patients ne vous comparent pas à un autre laboratoire — ils vous comparent à une page Facebook. »
- EN : "Your patients aren't comparing you to another clinic — they're comparing you to a Facebook page."
This is not a scare line: it's the reason a real site + WhatsApp flow *wins* without any ads.

**H4 · Claim → proof discipline in the demo and the close.** Every bold sentence gets its artifact on the very next screen or breath: the price on their own ad, the deadline, the dead domain, the Google listing, the number of followers. No claim without a pointer. In the walkthrough: "here it is" beats "this is great".

**H5 · One quote at a time.** Never a wall of reviews in a client deliverable or a concept. Bold claim → one real verbatim quote under it → next claim. (Contradicts nothing in v2; sharpens the proof sections.)

**H6 · Testimonial harvest as a delivery step (zero cost over-delivery).** At handover +1 week, ask the client for 3 of their own customers to answer H2's questions (WhatsApp voice notes are fine). Their words go into the site (with consent) and become the next concept's proof. This is the "customer writes your copy" hack [4] applied to our delivery — logged in the client's delivery checklist.

---

## PART I · THE 3A REFRAME — the house method for every objection (v2.2, 17 Sep, from Hormozi [7])

**When to use:** any moment a prospect says anything other than yes — an objection, a stall, a question we're not certain how to answer, a "no" dressed as a statement. Especially written WhatsApp replies, where we have time to think and every word stays on record.

**The three beats (always this order, keep it to 3–4 short lines in writing):**
1. **ACKNOWLEDGE** — say their words back, in their words: « Je comprends : le budget est un vrai sujet. » / "I understand — timing isn't right for you."
2. **ASSOCIATE** — label their question as the behaviour of our best clients: « C'est la question que posent les clients qui prennent ça au sérieux. » / "That's exactly what the ones who end up happy ask first." The label is a mirror they then live up to. Echo it deliberately when we get to the close.
3. **ASK** — ask a question *about their question*, never defend:
   - « Qu'est-ce qui vous ferait dire oui ? » · « Qu'est-ce qui vous ferait dire non ? »
   - « Qu'est-ce qui vous inquiète le plus ? » (use once we're far enough along; early on use « Quel est le point principal ? »)
   - « Sur quoi votre associé serait-il d'accord, et sur quoi pourrait-il bloquer ? »
   - « Vous cherchez surtout X ou Y ? » (safe answer to a question we can't verify — it keeps control and protects the accuracy law)

**The four objections written out (FR/EN-ready, 3–4 lines each):** price · « je vais réfléchir » · « on a déjà une page Facebook » · « je dois en parler à mon associé/épouse » — full scripts in `research/YouTube-Lessons.md` entry [7] §"AMK-applicable tactics" 1.

**Rules that make it safe and ethical (AMK version):**
- **Never disagree with a prospect, ever.** You cannot win a sale by winning an argument. Be smoke: always side-shift to a question.
- **Never invent a third party.** Straw-man stories (a foil who asked the same thing) are allowed **only when true** — a real past client, a real quote from their own reviews, a real story that happened. Otherwise it's a lie and it breaks the accuracy law.
- **Prospects believe what they say, not what we say.** Stop telling them they're a good fit; ask until they say it themselves.
- **Retain childlike curiosity** — in writing that means « Hmm, intéressant… » followed by a real question, never a defensive paragraph.
- **Ban the sentence "Vous avez des questions ?"** — it invites objections and hands over the wheel. Replace with a specific question.

**The label bank (use once per conversation, then echo at the close):** « Ça, c'est une question de quelqu'un qui prend ça au sérieux. » · « C'est la question de nos meilleurs clients. » · « Vous faites bien de vérifier ça. »

---

## PART J · CLOSER FOR THE WHATSAPP ERA (v2.2, 17 Sep, from SaaS Academy [8])

**The framework (every step phrased as a question — statements make people stall, questions get instant answers):**
- **C — Clarify:** « Quel est votre objectif avec ça ? » → « Pourquoi c'est important pour vous ? » → « Dans 12 mois, ça ressemble à quoi si ça marche ? »
- **L — Label the problem:** « Si je comprends bien : vous avez X, Y, et il manque Z. C'est ça ? »
- **O — Overview the pain:** « Qu'est-ce que vous avez déjà essayé ? Pourquoi ça n'a pas marché ? » — recap the pain in their words, **inside discovery only** (never extend into follow-ups; our no-chase rule stands).
- **S — Sell the vacation:** three 30-second proof stories showing the missing link, adapted to our niche: (a) a site that works on a phone, (b) WhatsApp as the booking/results channel, (c) being findable when searched. Most prospects have one or two; we sell the third.
- **E — Explain away concerns.** Only three objection types exist: **price · delay · decision-maker.** Log every objection into one of these three (local addition: trust — « est-ce que vous disparaissez après paiement ? » — mapped to price-visibility and decision-maker, logged separately until we have a fourth confirmed pattern).
- **R — Reinforce the decision:** within the hour of a « oui »: a short voice/video note from King + the personalised confirmation with their business name + the first delivery date. Feet hot, no buyer's remorse, no ghosting.

**Yes/no decision chain (pre-close checklist, one question at a time — three yeses and the close is administrative):**
1. « Le concept vous plaît ? » · 2. « Vous pensez que ça peut vous amener des patients ? » · 3. « Vous avez la première moitié disponible cette semaine ou fin de mois ?

**Always make the ask.** A sale we never asked for is a sale we never made. The 3A reframe (Part I) is what lets us ask repeatedly without burning rapport: ask, reframe, ask again.

**Solo version of the team cadence** (the video's huddle/1-on-1/leaderboard mechanics are for teams — parked in the register, not in the playbook): Friday, re-read the week's best and worst exchange, write one line on each into `sales/swipe/README.md`, and update the objection log. That is our call-recording discipline.

---

## PART K · THE SIGNATURE OFFER — FROM "A WEBSITE" TO A NAMED RESULT (v2.3, 23 Sep, from Nicole & James [24])

**The video's diagnosis, in one line:** *premium prices do not come from how long something takes — they
come from how deeply it changes somebody's business.* Selling **deliverables** ("a 5-section homepage",
"a bilingual site") puts you in the **service trap**: every project is custom, you quote by hand, the
client hears a cost, and you end up positioned as **an extra pair of hands** instead of the person they
call for results.

**The framework — three R, applied to AMK with our own numbers:**

| | What the video says | Ours, verified |
|---|---|---|
| **R — Refine** | pick a niche you like, where you can offer the biggest transformation, **and who can pay** | already done: **schools & clinics**, narrowed to the **vitrine profile** — that profile answers **11,1 %** (3/27) against **2,5 %** (3/118). "Who can pay" is not an assumption for us: it is the **budget step** of the 6-step discovery, asked out loud, never guessed |
| **R — Research** | pains, desires, what keeps them up at night, the one thing | we have the verbatims, in the client's own words: « je suis vraiment intéressé » (Univers Optique), « Ok » (Le Cristallin, on a site he had not paid for). Their night-time worry is not "I want a website" — it is **"est-ce que quelqu'un me trouve et me fait confiance ?"** |
| **R — Reposition** | reframe the same skills around that transformation | the offer is **built already, before a franc is discussed** — "L'aperçu d'abord", the unique mechanism from `DECLINAISON-9-DECLENCHEURS-2026-09-23.md` |

### K.1 The offer, in the client's words (never in ours)

**The transformation we sell, one sentence, plain French, no jargon:**

> **« On vous trouve, on vous fait confiance, on vous écrit sur WhatsApp — et la page est déjà faite avant
> que vous ayez payé un franc. »**

**The three things that actually change for the client** (this is the answer to "what am I buying?", and it
is what the business case measures):
1. **Trouvable** — le nom, le métier, le quartier, les horaires, une réponse chiffrée à la question du prix.
2. **Rassuré avant de venir** — photos réelles, conditions écrites, ce qui se passe après le message.
3. **Un chemin de rendez-vous** — WhatsApp pré-rempli, appel en un tap, aucune inscription.

**The deliverables are the proof, not the pitch.** The 5 sections, the bilingual build, the 3–5 days, the
hosting year: they belong in the *what's included* block, after the outcome.

### K.2 What this changes in what we say (and what stays frozen)

- **The first line of every message is the outcome, not the artefact.** Before: « je crée des sites web
  bilingues ». After: « on vous trouve et on vous écrit — voici la page, elle est déjà faite ».
  (The rewritten message 1 in `MESSAGES-2026-09-23-PERSUASION.md` already does this; this makes it a rule.)
- **Price stays a number attached to the outcome, never to hours.** Our prices are fixed and public in the
  room: **100 000** (Univers Optique, frozen 21/09) and **150 000** (Le Cristallin, sent 23/09). We never
  discount — **if the scope is too big for the budget, the scope shrinks** (that is already the rule; the
  video is the reason to keep it).
- **The business case is the reposition, written down.** `BUSINESS-CASE-*.md` = "here is what changes for
  you, in your numbers" — that is the document a high-paying client signs, not a feature list.
- **We do NOT rename our offer into an "accelerator".** The US version of this framework lives on coined
  product names (« Brand Visibility Accelerator »). Our market reads French, distrusts jargon, and our own
  §11 copy rules ban invented vocabulary. The transformation is named **in their words**, which is what
  actually makes it land.

### K.3 The two traps of this video, closed by name

- **"Who can pay premium prices"** can quietly become *"skip the small ones"*. Ours: every lead gets the
  same message; **budget is a question in discovery, not a filter in sourcing**. Cost of being wrong the
  other way (pitching a school that cannot pay) is one message; the cost of excluding by assumption is a
  dead pipeline.
- **The invented-prestige trap.** A big name with nothing behind it is the exact thing our accuracy law
  bans. The offer is credible for one reason only, and it is checkable: **the page exists before the
  invoice** — UNI-LABO is live, Univers Optique wrote back, Le Cristallin validated a price on a site he
  had not paid for.

### K.4 What was rejected

The course/community funnel, the $30k/month income claims, the "gamify your way to 30K" framing, USD
pricing, the referral-dependency angle (our pipeline is outbound — referrals are a *result* to earn, not
the channel we start from). Rejections logged in `research/YouTube-Lessons.md` §5.

---

## PART L · THE SECOND PRODUCT — WHY THE BACK-OFFICE IS A DIFFERENT BUSINESS (v2.4, 23 Sep, from the ERPNext audit)

**Context:** King sent `github.com/frappe/erpnext`. I read the repo itself (not the marketing pages). Full
audit: **`research/ERPNext-AUDIT-2026-09-23.md`**. The playbook only keeps the selling rules that came out of it.

**L.1 The one thing that must never happen.** ERPNext is free, mature (39.5k ★, stable v16 released 15/09),
and runs on a **server**, not Vercel. It contains the **Cameroonian SYSCOHADA chart of accounts (1,329 coded
accounts)** and **VAT 19.25 %**, straight out of the installer. The temptation is therefore to sell an "ERP" on
Monday. **Do not.** Our 47 leads buy **being found**, at 100–150k FCFA, one time. An ERP buyer is a different
animal: 10–30 staff, several sites, invoicing every day, and a **monthly** budget. **Selling the wrong one to
the wrong man loses the account we already have.**

**L.2 What the audit actually gives us to sell — in order.**

| | Offer | Price (proposal, King validates — never a discount, we adjust scope) | Why it is credible here |
|---|---|---|---|
| **A** | **Caisse + factures + stock** (shop / optician, 3–8 staff) | **250 000 FCFA** + **25 000/month** | Every franc that comes in is recorded, MoMo included, without a spreadsheet |
| **B** | **Dossier + résultats + factures** (lab / clinic, 10–30 staff, via the Marley health app) | **450 000–600 000 FCFA** + **40 000/month** | The only segment that invoices daily and where "quality" is already a purchase motive |
| **C** | **The monthly maintenance contract** | **25 000–40 000/month** | Ten contracts = 250–400k FCFA/month without prospecting. **This is the first credible recurring revenue AMK has ever had.** |

**L.3 The four sentences we are not allowed to say** (each one is a call-back we would deserve):
"Ndou payez en ligne / par Mobile Money" — **no MoMo gateway exists**: we record the MoMo transaction reference
in the accounting instead. · "Ça marche sans internet" — the standard POS needs the network **to load**: we test
the client's connection *before* selling a till. · "Envoyez vos factures par WhatsApp automatiquement" — that
needs a **dedicated number, Meta verification, approved templates and a cost per conversation**: an option for a
big client, a project in itself. · "C'est entièrement en français" — measured: **47 % (ERPNext) / 73 %
(framework)**; translating the fifteen screens that matter **is part of the job**, and can be billed.

**L.4 What we keep even if we never sell one licence.**
① **The business model** — Frappe sells **hosting, backups and updates, every month**, not licences: copy it,
including for the 150k pages (hébergement + retouches, 10–15k/month). ② **The branded PDF** — today our quotes
are plain WhatsApp text; a real PDF with our logo changes how the agency is perceived from the next client on.
③ **"The invoice link that opens in WhatsApp"** — the invoice is hosted, the `wa.me` message carries the link,
the client taps and reads it: no Meta API, no per-message cost, **and it works on the number he already has**.
That one is ours, and it sells to every trade that issues bills. ④ **Licence hygiene**: ERPNext/HRMS/Marley are
GPL-3.0, the framework/Builder are MIT, **CRM/Helpdesk/Books/Insights/Print Designer are AGPL** — a modified
AGPL app served to users over the network owes them its source. **We never promise a closed product built on
AGPL.** And never put "ERPNext" in our company, product or domain name (Frappe's trademark policy), nor in ads.

**L.5 Before any of this is offered to a human being — three decisions belong to King** (listed at the end of
the audit): whether we open the track at all (no / a public demo with invented data / a paid pilot — **never a
free pilot**), **who pays the server and how** (Frappe Cloud or a VPS wants a foreign card; Mobile Money cannot
pay for a VPS), and **which profile the demo shows** (lab or shop — I can only build one).

**L.6 Which problem are we solving — the order, explained (King's question, 23 Sep).** Our problem #1 is not
the client's: **we sell 150,000 once and then work for free.** Every offer was sorted by four questions —
does it fix *our* recurring revenue, can it be sold this week, what does it cost us, does it produce a
reference? The order that falls out is **C (monthly maintenance, sold on deals already on the table: three
clients × 10,000 = 360,000 FCFA/year without prospecting) → D/E (the quote-PDF and invoice-link tooling that
makes a subscription billable) → B (the lab pilot, the only offer whose price holds, and the one that produces
a health reference) → A1 (resell a local SaaS for a commission) → A2 (out-of-standard, only if a distributor
walks in) → F (client-editable site: **destroys the subscription**, premium only, later) → G (e-invoicing:
watch, never promise "DGI-compliant")**. Full reasoning: `sales/ORDRE-DES-OFFRES-2026-09-23.md`. The tunnel,
in one line: **the page opens the door, the subscription pays the bills, the tool is the next trade — in that
order, never the reverse.**
