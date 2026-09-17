# AMK — Uniqueness Registry

**Purpose:** the anti-repetition ledger. One line per delivered/built site: client · niche · dominant fingerprint (layout archetype + palette family + type system + tone). **Before any new build**, read this file — if the intended direction resembles a row below, throw it out and re-research (see `PRE-FLIGHT.md` §2.4).

**Rule:** newest row on top. Backfilled rows are marked; verify the live file before reusing a fingerprint.

| Date | Client / file | Niche | Layout archetype | Palette family | Type system | Tone / angle |
|---|---|---|---|---|---|---|
| 16 Sep 2026 | Cabinet Dentaire YAKS — `demos/concept-yaks-v1.html` | Dental, Logbessou (Douala) | Hero + **specialities wheel** (circular grid), proof stats band, services bento | Green `#57A52A` + teal `#1FB7C8`/`#0E8A99` on light | **Nunito** display + Inter body | Family/care ("la santé de vos dents, la beauté de votre sourire") |
| 16 Sep 2026 | Cabinet Dentaire The Skye — `demos/concept-skye-v1.html` | Dental, Bonamoussadi (Douala) | Editorial hero + services list, FR-first | **Logo blues** (their brand), light neutrals | Outfit + Inter | Aspirational ("Souriez à l'infini") |
| 14 Sep 2026 | OraCare Dental Clinic — `demos/concept-oracare-v3.html` | Dental, Molyko (Buea) | Bento-heavy, price cards, photo-forward hero | **Odentrics family** cream/sand `#F7F1E8` + navy `#16323A` + gold `#C9A24B` + sage `#7FA88F` | Outfit + Inter | Price clarity + 24/7 booking, EN-first demo |
| 14 Sep 2026 | SJC Sasse — `demos/sjc-sasse-v2.html` | Secondary school, Buea | Institutional hero + admissions flow | Navy `#0F2456` / `#17357F` | System sans + **Georgia serif** | Heritage/trust, admission-first |
| (backfill) | SAHISCOL — `demos/concept-sahiscol-v1.html` | School | Institutional layout | Deep purple `#4A2050` / `#38173D` | System sans + Georgia serif | — |
| (backfill) | La Retraite — `demos/concept-la-retraite-v1.html` | School | Institutional layout | Blue `#16337E` / `#0F2456` | System sans + Georgia serif | — |
| (backfill) | COMOBIL — `demos/concept-comobil-v1.html` | Transport | — (parked 14 Sep) | — | Outfit + Inter | — |
| (backfill) | Bonabéri Medical Centre — `site/clinic-bonaberi.html` | Clinic sample (nameless) | Maternity/lab layout | **Forest** `#0E7A5C` + bone `#F6F3EC` + amber | Outfit + Inter | Care/urgency balance |

**Notes**
- School rows (Sasse, SAHISCOL, La Retraite) currently share one fingerprint family (navy/purple/blue + serif + institutional layout) — they predate the §19 direction-exploration gate. **The next school build must differentiate on ≥ 4 axes or adopt a new family.**
- Dental rows (OraCare, Skye, YAKS) are already differentiated on palette + type + layout — YAKS (wheel), Skye (editorial blues), OraCare (bento/cream).
- New clients get `clients/<client-name>/inspiration.md` + `build-notes.md` from their first build (see `PRE-FLIGHT.md` §3).
