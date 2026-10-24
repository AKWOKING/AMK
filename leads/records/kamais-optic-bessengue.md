# Kamaïs Optic

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-10-24. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | kamais-optic-bessengue |
| Type | other |
| Ville | Douala (Bessengue) |
| Langue de contact | FR |
| Étape | parked |
| WhatsApp | 678 435 460 |
| Numéro vérifié | yes |
| Canal | WhatsApp |
| Contacté | Yes |
| Réponse | No |
| Maquette / site | No |
| Source | directory |
| Détail source | annuaires Bessengue |

## Notes

Envoyé 18/09 19:42, sans maquette. · ⚰️ MORT le 22/09 (lot du 18/09) — jamais ouvert, jamais répondu ; décision de King : on ne réécrit plus, on va vers des prospects frais. Aucune relance programmée.

## Prochaine action

**Aucune.** Parqué. Une action n'est légitime que si King le décide explicitement.

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 15 ligne(s).*

`L44` · | **ven 18/09 19:42** | **Kamaïs Optic** (Bessengue, 678 435 460) | msg 1 — sans maquette | Envoyé | **Non** |
`L112` · | 19:42 | Centre Médical de Bonanjo · Kamaïs Optic |
`L707` · Kamaïs→other, Baird confirmé school). **Les 55 autres restent non vérifiés — je ne devine pas.**
`L761` · | ③ | **org_type : « va ligne par ligne sur les faits écrits dans la ligne. »** | Fait — **mais je n'ai pas trié à la main une par une : j'ai supprimé la cause.** `crm.py` collait `"school"` aux 38 lignes du classeur **sans jamais lire la ligne** ; voilà d'où venaient MITOC « school » et Solidarity « school ». Nouveau `org_type_for()` : l'étiquette n'existe que si un mot **du nom, des Facilities, de l'activité ou des notes** la porte (`lab` → `clinic` → `other` → `school`, dans cet ordre parce qu'« laboratoire d'analyses médicales » n'est pas une clinique). La preuve est écrite dans `Notes` (`org_type=lab prouvé par « laboratoire »`). Les overrides explicites (MITOC, One Stop, JOSS, Kamaïs, Solidarity) gagnent avant. **Résultat : 0 ligne sans étiquette et 0 ligne sans preuve** — contre 145 dont 38 affirmées « school » par défaut. |
`L3899` · 156 lignes du CRM et les 62 leads déjà contactés : **Kamaïs Optic est tombé** (Bessengue — déjà au CRM,
`L5033` · Kamaïs/Bonanjo · Maff/Bonadibong · Faby · JiredOptic · Planète · Centrale) ; Lumumba + Bali hors
`L5046` · (≤30 j) pour les 7** ; seuls existent l'annuaire ONOC (noms propres sourcés) et, pour Kamaïs, une
`L5056` · - **KamaïsOptic :** sur WhatsApp ; **aucun envoi aujourd'hui**. ⚠️ Le CRM porte : envoyé 18/09 19:42,
`L5060` · (« 50m du feu rouge Bessengue ») + numéros 693 927 766 / 678 435 460 : Bessengue retenu comme
`L5072` · contrôlé l'entité ONOC mais PAS l'historique CRM → 3 des 7 n'étaient pas froids (Maff, Kamaïs,
`L5075` · ## lun 12/10 11:47 — PREMIER REFUS DE LA VAGUE (JiredOptic) + KAMAÏS CONFIRMÉ MORT
`L5082` · - **KamaïsOptic :** ruling King 12/10 : « Kamais est mort on ne le relance pas » → la décision du
`L5108` · excluded_already_contacted. Kamaïs : tag excluded_already_contacted.
`L5192` · - **Ruling 2 — décompte (CORRECTION) :** la vague comptait **7 envois à froid** ; **5 sur 7** ont échoué aux gates (Horizon, Faby, Centrale : WhatsApp · Kamaïs, Maff : déjà contactés) ; **2 sur 7** ont passé (JiredOptic a refusé, Planète silence). Lumumba n'est pas à froid (contacté 24/09), traité à part. Le « 5 sur 8 » était une erreur de notre part. `RETRO-VAGUE-2026-10-12.md` §1/§3 corrigés.
`L5668` · 11:47, envoi Planète, tags Maff/Horizon/Kamaïs, RDV Univers Optique du 16/10) et la relance Planète du

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
