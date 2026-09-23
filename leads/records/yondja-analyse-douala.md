# YONDJA ANALYSE

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-09-23. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | yondja-analyse-douala |
| Type | lab |
| Ville | Douala |
| Langue de contact | FR |
| Étape | parked |
| WhatsApp | 696 88 88 23 |
| Numéro vérifié | yes |
| Canal | WhatsApp |
| Contacté | Yes |
| Réponse | No |
| Maquette / site | No |
| Source | directory |
| Détail source | Remote-Sweep §C |

## Notes

Envoyé 18/09 ~18:30, sans maquette. · ⚰️ MORT le 22/09 (lot du 18/09) — jamais ouvert, jamais répondu ; décision de King : on ne réécrit plus, on va vers des prospects frais. Aucune relance programmée.

## Prochaine action

**Aucune.** Parqué. Une action n'est légitime que si King le décide explicitement.

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 11 ligne(s).*

`L30` · | **ven 18/09 ~18:30** | **YONDJA ANALYSE** (696 88 88 23) | msg 1 — **sans maquette** | Envoyé | **Non** |
`L110` · | ~18:30 | Discovery Labs · UNI-LABO · YONDJA ANALYSE · Laboratoire du Château · Département Biologique · CAMERA · LE NID |
`L150` · | **22:05** | King | « Bonsoir. Akwo King, AMK — Douala. Vous m'avez écrit ce soir, alors je vous réponds avec l'aperçu plutôt qu'avec un discours. **https://uni-labo.vercel.app** Il est fait pour UNI-LABO : vrais horaires, préparation des examens, itinéraire Carrefour Etoo, en français et en anglais. Dites-moi si les horaires et la liste des analyses sont exacts — je corrige tout de suite. Un « oui » suffit. — Akwo King / AMK » | Envoyé ✓✓ |
`L541` · ### ② SEO — les 3 vidéos analysées, et notre propre site réparé
`L761` · | ③ | **org_type : « va ligne par ligne sur les faits écrits dans la ligne. »** | Fait — **mais je n'ai pas trié à la main une par une : j'ai supprimé la cause.** `crm.py` collait `"school"` aux 38 lignes du classeur **sans jamais lire la ligne** ; voilà d'où venaient MITOC « school » et Solidarity « school ». Nouveau `org_type_for()` : l'étiquette n'existe que si un mot **du nom, des Facilities, de l'activité ou des notes** la porte (`lab` → `clinic` → `other` → `school`, dans cet ordre parce qu'« laboratoire d'analyses médicales » n'est pas une clinique). La preuve est écrite dans `Notes` (`org_type=lab prouvé par « laboratoire »`). Les overrides explicites (MITOC, One Stop, JOSS, Kamaïs, Solidarity) gagnent avant. **Résultat : 0 ligne sans étiquette et 0 ligne sans preuve** — contre 145 dont 38 affirmées « school » par défaut. |
`L1324` · strict perdrait 56 citations **légitimes** sur 295 (`Bonanjo`, `Yondja`, `Cerisaie`…). Limite consignée en
`L2453` · suivi), 4 familles d'analyses, résultats, adresse, FAQ. **Mais zéro formulaire** : ses 12 liens WhatsApp sont
`L2484` · plus « Autre analyse » et « J'ai une ordonnance — conseillez-moi » ;
`L2487` · - **un bouton WhatsApp éteint tant que la demande est incomplète**, qui s'allume quand une analyse est
`L2489` · `Bonjour UNI-LABO, je souhaite prendre rendez-vous. / Nom : … / Analyses : … / Moment souhaité : …` ;
`L2496` · sur les deux états d'erreur : bouton éteint et groupes fautifs marqués quand il manque une analyse, un nom ou

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
