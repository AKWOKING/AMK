# Solidarity Health Foundation (Solidarity Clinic & Laboratory)

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-09-21. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | solidarity-health-foundation-solidarity-clinic-laboratory |
| Type | school |
| Ville | Buea (Untarred Malingo St / Molyko Checkpoint D61, P.O. Box 467; plus code 575J+7M) |
| Langue de contact | Bilingual EN/FR |
| Étape | parked |
| WhatsApp | 677615757 |
| Contact | CURRENT DIRECTOR UNKNOWN publicly (gatekeeper routing). Founder Dr Peter Nde Fon (CEO) DIED 21 Oct 2020 (Cameroon-Info/MMI obits); run by Solidarity Health Foundation CIG, family incl. widow Beatrice Nde Fon plausibly involved (unconfirmed). Current MO: Dr Asoba Anodem (LinkedIn, 2011-present). Dr Njang Mbeng Emmanuel listed on stale medicoor roster but NOT confirmed current (his LinkedIn: DMO Muyuka + co-owner One Stop lab; do not assume) |
| Canal | WA blocked on clinic line -> check SHF-CIG admin 677 61 12 07; else Wed 16 Sep sealed envelope to 'current medical director or clinic manager' |
| Contacté | scheduled Tue |
| Maquette / site | nameless clinic-bonaberi.html (Bonabéri Medical Centre, Douala; Forest palette; was Molyko Medical Centre/sample-clinic.html, renamed by King 15 Sep PM) |

## Pourquoi il est écarté

King : NE JAMAIS contacter Solidarity (677 61 57 57). Base : établissement à acheteur institutionnel — notre règle ne relance pas ce type d'acheteur.

## Contradiction résolue (M2)

- **Ce qui se contredisait :** Le classeur dit « scheduled Tue » ; Pipeline-Status dit « no WhatsApp line » ; King dit : ne jamais contacter.
- **Retenu :** parked, avec le motif de King écrit dans la donnée : jamais de contact, acheteur institutionnel.
- **Écarté :** « scheduled Tue » — la ligne n'a jamais été jouable, et la consigne de King prime sur les deux fichiers.

## Notes

Clinic lead #1, research-standard corrected 15 Sep (see sales/RESEARCH-STANDARD.md error #1). Not-for-profit CIG founded Aug 1998 by late Dr Peter Nde Fon (UB public health chair, obituary verified). GBP 4.0 stars/54 reviews/21 photos/24h, Untarred Malingo St plus code 575J+7M, NO website ('Add website'), medicoor unclaimed+stale (still lists deceased founder), X @SolidarityHeal1 since May 2021. Services: gen med, vaccination, surgery, lab panels, maternity, ultrasound/X-ray; reviews cite cardiologist+pharmacy; Zenithe accredited. Among Buea district top-3 most-solicited facilities (PAMJ 2023, BMRI 2025). Pitch: attach bilingual site+WA booking+same-day lab results to GBP; foundation/grant visibility; claim medicoor; 24h emergency bar. FUs M+2/M+4/M+7. [15 Sep send morning: 677 61 57 57 not registered on WhatsApp per King; voice line only, never cold-call; MITOC now leads Tue 08:35; Solidarity -> admin-line check, else Wed sealed card] | 15 Sep PM RENAME: live concept is /clinic-bonaberi.html (LIVE, partial hand-rename by King; canonical repo build fully renamed to Douala/BMC, redeploys with amk-site.zip). Solidarity (Buea) warm-yes link uses it with placeholder caption; ask King if he wants a Buea/city-neutral variant + matching mockup-clinic image. · 🚫 King : NE JAMAIS contacter Solidarity (677 61 57 57). Base : établissement à acheteur institutionnel — notre règle ne relance pas ce type d'acheteur. | CONTRADICTION RÉSOLUE (M2) — retenu : parked, avec le motif de King écrit dans la donnée : jamais de contact, acheteur institutionnel.

## Prochaine action

**Aucune.** Parqué — King : NE JAMAIS contacter Solidarity (677 61 57 57). Base : établissement à acheteur institutionnel — notre règle ne relance pas ce type d'acheteur.. Une action n'est légitime que si King le décide explicitement.

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 4 ligne(s).*

`L684` · Ce qui N'est PAS stocké, et pourquoi c'est écrit dans le fichier : `kill_list`, `health` (calculés —
`L685` · `health_override` est la seule porte manuelle, tracée), `last_message_sent` (c'est le journal),
`L745` · 4. **Les 5 questions de l'audit du 18/09 §10 sont toujours sans réponse** (COMOBIL · health manuel de St. Theresa · les 12 labos de la réserve · la Page Facebook · le parrainage St. Theresa). Les deux premières ont été tranchées par la migration d'aujourd'hui ; il en reste trois.
`L761` · | ③ | **org_type : « va ligne par ligne sur les faits écrits dans la ligne. »** | Fait — **mais je n'ai pas trié à la main une par une : j'ai supprimé la cause.** `crm.py` collait `"school"` aux 38 lignes du classeur **sans jamais lire la ligne** ; voilà d'où venaient MITOC « school » et Solidarity « school ». Nouveau `org_type_for()` : l'étiquette n'existe que si un mot **du nom, des Facilities, de l'activité ou des notes** la porte (`lab` → `clinic` → `other` → `school`, dans cet ordre parce qu'« laboratoire d'analyses médicales » n'est pas une clinique). La preuve est écrite dans `Notes` (`org_type=lab prouvé par « laboratoire »`). Les overrides explicites (MITOC, One Stop, JOSS, Kamaïs, Solidarity) gagnent avant. **Résultat : 0 ligne sans étiquette et 0 ligne sans preuve** — contre 145 dont 38 affirmées « school » par défaut. |

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
