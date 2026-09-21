# LA BÉTHANIE (Bonabéri, Douala) — build notes + three-door gate

**Date:** 17 Sep 2026 · **Concept:** `demos/concept-labethanie-v1.html` · **Builder:** `demos/build_labethanie.py` · **Mockup:** `demos/shots/mockup-labethanie-wa.jpg` (191 KB)
**Direction:** « LA CONSULTATION » — their gynaecology flyer, made live, with the patient's discretion as the design value.

## 1 · Three-door pre-send gate (RESEARCH-STANDARD §8b)
| Door | Verdict | Evidence |
|---|---|---|
| **A · Reachability** | ✅ **PASS — King 17 Sep 2026** | King confirmed **677 76 07 82** is on WhatsApp (screenshot « +237 77760782 » = same line, old 8-digit format). Baked into the concept as the single WhatsApp CTA. |
| **B · Digital intent** | ✅ PASS | 210 WhatsApp clicks recorded through DoualaTour; active in health directories (Medicoor, Maligah, ASCOMA network) — patients already look for them by phone. No own website found. |
| **C · Buyer type** | ✅ PASS | Private clinic led by **Dr Richard Petieu** (surgeon) — named owner-decideer, no board. |
**Score 3/3 → build and send.**

## 2 · Sources used (all verified this session)
- **Their gynaecology flyer** (King's upload, `clients/la-bethanie/Clinique La Béthanie (Bonabéri).jpg`): « Service de gynécologie », « Votre santé intime, notre priorité », the six prestations **copied word-for-word**, phones **683 76 74 13 / 699 73 15 48**, « Bonabéri – Rue Mpondo (Ancienne Route), Douala », « Ouvert 24H/24 · 7J/7 ».
- **Their entrance photo** (King's upload, `entrance … .jpg`): yellow building, dark-green fence, white « LA BETHANIE — Centre Médico-Chirurgical, Maternité » sign, Tél. **677 76 07 82 / 683 … 74 13**. → used as the hero image *and* the wayfinding description (« bâtiment jaune derrière une grille verte »), because a real photo of their gate is worth more than any stock clinic.
- **Their entrance sign, « NOS SPÉCIALITÉS » block** (zoomed 6×): legible lines include *gynécologie-obstétrique*, *médecine générale*, *chirurgie générale*. Other lines are too blurred to read with certainty → **not used** in the page.

## 3 · What the concept contains
Hero (real photo + « Votre santé intime, notre priorité ») · **Urgences 24h/24 · 7j/7** band with call + WhatsApp · **Service de gynécologie**: the flyer's six prestations as a **tickable leaflet** whose checked items compose one discreet WhatsApp message (nothing is stored on the page) · panel « Une première consultation, comment ça se passe ? » (3 steps) · **Chirurgie** (centre médico-chirurgical: consultation, interventions programmées, suivi) · **Nous trouver** (Rue Mpondo/Ancienne Route, landmark from the photo, schematic map, the sign photo) · FAQ (5) · contact + sticky WhatsApp/call bar · FR|EN · noindex.

## 4 · Uniqueness (registry check)
**6 axes differ** from `site/clinic-bonaberi.html` (the nearest row): layout archetype (care leaflet + path vs bento services + price table), palette (royal blue `#0F4C9C` + leaf green `#3F8B1E` vs forest green + bone + amber), type (Montserrat + Open Sans vs Outfit + Inter), imagery (their real photo vs illustrated placeholders), interaction (tickable prestations → WhatsApp message vs quote cards), tone (intimate/discreet, **no prices at all** vs price-forward). Registry row added.

## 5 · Accuracy discipline (what is deliberately NOT on the page)
- **No prices** — none were ever published for their acts; inventing them would be the one fatal claim.
- **No laboratory claim** — the labo was in the earlier draft plan, but no source confirms they run one → dropped.
- **No testimonial, no patient name, no "X patients"** — patient confidentiality + no permission.
- **No English-service claim** — the *site* is bilingual; the FAQ says to mention your language when getting in touch instead of promising bilingual staff.
- **Phones:** the sign reads « 677 76 07 82 / 683 …t 74 13 » and the flyer reads « 683 76 74 13 / 699 73 15 48 » → page shows `677 76 07 82` as the WhatsApp line (verified) and both flyer mobiles as call numbers. *To confirm with the clinic.*
- **« Direction : Dr Richard Petieu, chirurgien »** comes from public directories (ASCOMA 2021, Maligah, Medicoor). Flagged here: **confirm before any public use**; wording already kept minimal.
- Footer states plainly that this is an AMK preview, not their live site.

## 6 · Gates passed before shipping
- `python3 tools/qa/audit_html.py demos/concept-labethanie-v1.html` → **0 findings** (222 text runs, desktop + mobile). The audit caught a *real* bug on the way: the brand subtitle reused the class `.tag` (the hero caption's `position:absolute` dark chip) — renamed `.bsub`.
- Structure: 6 sections, none nested; `node --check` on the inline script → OK; **6** `wa.me/237677760782` links; zero placeholder numbers.
- Mockup: `demos/shots/mockup-labethanie-wa.jpg` 1600×900, laptop + phone, drawn in the concept's own palette/type with the real photo; inspected.

## 7 · Open items for King / the client
1. Confirm which number should be **the** WhatsApp (677 76 07 82 assumed) and whether **683 76 74 13 / 699 73 15 48** are still live.
2. Confirm the surgery list and whether « Dr Richard Petieu » should be named on the page.
3. Deploy `hosting/previews/` → **/labethanie/** → phone QA → send image-first (send sheet).
