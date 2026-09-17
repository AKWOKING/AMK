# JEMPO — inspiration & Design Read (17 Sep 2026)

## Live references pulled (URLs opened today, not memory)
| # | Reference | Angle | Taken (specifically) | Rejected |
|---|---|---|---|---|
| R1 | **mondocteur237.com** (the platform JEMPO already uses — homepage + the four practitioner cards) | **The UX their patients already learned** | The exact vocabulary and grammar patients in Douala are being trained on: « Dr + nom », specialty, city/quarter, **tarif consultation**, « RDV WhatsApp », « confirmation immédiate », days and hours as a short line per doctor. We keep the *grammar*, we remove the marketplace. | The marketplace frame itself (platform brand dominant, a widget that opens a conversation **on their channel**, the same doctor appearing among 991 others, the price displayed as the platform's own). |
| R2 | **doctolib.fr** | Booking-flow structure at world scale | **Specialty → practitioner → slot** as the single spine of a clinic site, and how a specialty index is written (ORL → « oto-rhino-laryngologie », plus plain-language aliases). The ladder is the lesson; nothing else. | Their consumer-marketplace chrome (search bar over 90 specialties, sitemap of every city, app-store badges) — irrelevant for one polyclinic in Deido. |
| R3 | **mpshahhosp.org** (M.P. Shah Hospital, Nairobi) | Multi-specialty private hospital, East Africa | How a multi-specialty facility presents **"Find a Doctor / Book / Services"** as three equal primary actions, and how accepted insurance and branches are handled as *quiet* trust blocks rather than decoration. | Their ICS/carousel-heavy hero, 217-bed scale, JCI badge wall, news feed, PDF leaflet promos. |
| R4 | **reddingtonhospital.com** (Lagos) | Emergency + 24/7 proof on a private hospital site | The **emergency strip that states the promise plainly** ("24 Hours Services" + the emergency numbers) and keeps a visible phone/address triad near the top. | Counters animated from 0, "Our Clients" bank-logo wall (they have corporate clients; JEMPO does not), blog sections we cannot fill, broken slider. |

**Gaps stated:** no Cameroonian clinic with a well-designed owned site was found — again. R1 and R2 are **product-logic** references (how booking is structured), R3/R4 are **institutional trust** references. The visual direction comes from the client's own physical door (the hero image) and from the palette family we chose for them (espresso/terracotta/sand), not from any of the four.

## Design Read
Dials: **Soft 4/10 · Editorial 4/10 · Dense 5/10** — a reception desk, not a brochure: structured, unmistakably local, no aspiration.
Direction **« LA PORTE »** — the polyclinic's own front door, opened. Espresso `#2A211C` + terracotta `#C2542B` (fills at `#9E3F1D` for AA) + sand `#F7F1E9`; **Archivo** display over **Inter**; a **door-shaped mark** instead of a generic medical cross; and one signature interaction — **la réception**: four specialty doors, each one showing the practitioner's name and their real published days, and a WhatsApp message that names that specialty and that doctor.

## Rejected alternative directions (§19.3)
- **« LE TABLEAU DE GARDES »** (a timetable-first page: a big grid of doctors × days). Rejected: it reads like an internal staff roster; patients arrive with a symptom, not a schedule. The timetable is *inside* the door, not on the wall.
- **« L'ANNUAIRE CORRIGÉ »** (a page that mirrors the MonDocteur237 card, only cleaner). Rejected: it would make us look like a cheaper copy of the platform the client already pays; the whole argument is that the door should be *theirs*.
- **« LE CENTRE MÉDICAL MODERNE »** (blue/navy medical template, white coats, stethoscope photography). Rejected: that is La Béthanie's territory (`clients/la-bethanie/`) and every other clinic in Douala. The brand colour direction had to break from the blue convention while staying credible — terracotta/espresso comes from the client's actual building.

## Uniqueness check
Registry read before building. Nearest rows: **La Béthanie** (royal blue + leaf green, Montserrat + Open Sans, tickable leaflet, hero = their own entrance photo) and **Bonabéri Medical Centre** (forest green + bone, Outfit + Inter, bento + prices). Differentiation from La Béthanie — the build from *this same day*, so the bar is high — on **6 axes**:
1. **layout archetype** — reception/four-doors selector vs leaflet checklist;
2. **palette** — espresso + terracotta on sand vs navy + leaf green on white;
3. **typography** — Archivo + Inter vs Montserrat + Open Sans;
4. **imagery** — a generated, unmarked door (with the *blank sign* as the message) vs their own photographed, signed façade;
5. **interaction** — specialty → practitioner → appointment that **names the doctor in the WhatsApp message** vs tick-list that names the services;
6. **section order** — hero → réception → 24/7 → accès → FAQ → contact vs hero → urgences → gynécologie → chirurgie → trouver → FAQ.
Also distinct from Afrique Labo (catalogue console), optical (mirror), dental trio.
