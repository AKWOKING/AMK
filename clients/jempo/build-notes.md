# JEMPO (Deido · Bessengue, Douala) — build notes + three-door gate

**Date:** 17 Sep 2026 · **Concept:** `demos/concept-jempo-v1.html` (161 KB) · **Builders:** `demos/build_jempo.py` (+ `--wa/--out`) · `demos/build_jempo_mockup.py` · **Mockup:** `demos/shots/mockup-jempo-wa.jpg` (174 KB)
**Direction:** « LA PORTE » — the polyclinic's own front door, opened. **First build under the §20 footer standard.**

## 1 · Three-door pre-send gate (RESEARCH-STANDARD §8b)
| Door | Verdict | Evidence |
|---|---|---|
| **A · Reachability** | ✅ **PASS — King, 17 Sep (screenshot)** | **696 71 06 99** = WhatsApp **Business** account named « **J&E MEMORIAL** », category **Medical & health**, **« Polyclinic »** shown in Contact info. Baked as the single WhatsApp CTA. See `whatsapp-business-2026-09-17.md`. |
| **B · Digital intent** | ✅ PASS | **4 JEMPO practitioners bookable on MonDocteur237** (Dr Marcus Youda ORL — "partenaire prioritaire", Dr Paul Djomaleu diabetes, Dr Angelique Njeumen dermatology, Dr Humphry Neng gynaecology), consultations published, WhatsApp booking, MoMo/Orange Money; complete Maligah listing; **202 WhatsApp clicks** logged via DoualaTour. |
| **C · Buyer type** | ✅ PASS | **Dr Marcus Youda**, ORL — **founder** of JEMPO (Maligah) and the priority partner of the booking platform = named owner-decider. |
**Score 3/3 → built and ready to send.**

## 2 · What the concept answers
Everything about JEMPO online lives **inside someone else's product** (MonDocteur237, Maligah, DoualaTour). A patient searching "ORL Deido" or "dermatologue Douala" lands on the platform, books there, and the clinic owns neither the page, nor the booking, nor the first impression.
**Answers:** a named front door · **la réception** — pick one of four specialty doors and see the practitioner's published days · a WhatsApp message that **names the specialty and the doctor** · the **24h/24 reception** stated as a promise (it was only visible on a directory) · **accès** with the real landmark (face hôtel LEWAT, Vallée Bessengue) · payment + insurance reality · FR|EN · **complete §20 footer**.

## 3 · §20 footer — first application (King's ruling 17 Sep: new builds only)
Drawn in the mockup so it can be seen before deploy. Four blocks + strip:
1. **brand + one line** (who they are, what they do) · 2. **doormat nav** — the page's own sections, labelled · 3. **CTA block = the hero's action** (WhatsApp appointment, same intent) · 4. **contact block** — WhatsApp, two phones, address + landmark, 24/7.
**Strip:** © 2026 + "aperçu préparé par AMK, pas encore en ligne" + **Retour en haut**. Legal is small and quiet; nothing hidden; credit is plain text (no keyword anchor).

## 4 · Uniqueness (registry + §19.3)
Distinct from La Béthanie (built the same day) on **6 axes** — see `inspiration.md` §Uniqueness. Rejected directions: « TABLEAU DE GARDES » (roster-like), « ANNUAIRE CORRIGÉ » (a cleaner copy of the platform), « CENTRE MÉDICAL MODERNE » (the blue/white-coat template that is La Béthanie's and everyone else's territory).

## 5 · Accuracy discipline (what is deliberately NOT on the page)
- **No consultation price.** The platform publishes 15 000 FCFA for Dr Youda; **that is the platform's number, not the clinic's** → it stays out of the page and out of the message.
- **No testimonial, no review score.** The 4.8/5 ratings live on the platform's profiles; we do not import someone else's proof into the clinic's site.
- **Practitioner names, days and hours** come from their own public cards (printed to the line, e.g. "Lun–Ven 08:00–17:30 · Sam 08:00–13:00") and are flagged **on the page** with a discreet note: *"Jours et heures affichés d'après vos fiches publiques — à confirmer avant la mise en ligne."* Same for the **24h/24** reception (Maligah: "Tous les jours 24h/24").
- **No claim about insurances we could not verify** — the page says to send the insurer's name before the visit.
- The hero image is a **generated, unmarked door** (the sign panel left blank on purpose — "*your door — the sign is still blank*" is the visual pitch). No real photo of JEMPO exists in our files; the mockup labels it as our preview.

## 6 · Gates passed before shipping
- `python3 tools/qa/audit_html.py demos/concept-jempo-v1.html` → **0 findings** (203 text runs, desktop + mobile). The audit caught **11 real contrast failures** on the first build (white text on the bright terracotta `#C2542B` in the 24/7 band and the footer CTA, a private-use `–` in the JS arrow, `.btn-line` colour). Fix: **clay fills darkened to `#9E3F1D`** for every white-on-clay surface, colour moved into a class (no inline-style cascade trap), footer anchors given an explicit light colour.
- Structure: **5 sections, none nested**; **6** `wa.me/237696710699` links; zero placeholder numbers; `node --check` on the inline script → OK (one fix: the JS object list had to be an array literal).
- Mockup inspected visually: laptop + phone, footer visible on both.
- Builder is parametrised (`--wa`, `--out`) → the same concept can be rebuilt for another line without touching the file.

## 7 · Open items for King / the client
1. Confirm the four practitioners' **days and hours** (and whether more specialties should appear) before launch.
2. Confirm the **24h/24 reception** claim at the time of handover.
3. Deploy `hosting/previews/jempo/` → share the link only after King's phone QA → then send §2f of the send sheet (image first).
4. Ask, on the first reply: who runs the clinic's Facebook/digital, and whether they want the platform link kept or replaced.
