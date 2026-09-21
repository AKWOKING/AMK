# Kamaïs Optic

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-09-21. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | kamais-optic-bessengue |
| Type | other |
| Ville | Douala (Bessengue) |
| Langue de contact | FR |
| Étape | qualified |
| WhatsApp | 678 435 460 |
| Numéro vérifié | yes |
| Canal | WhatsApp |
| Contacté | Yes |
| Réponse | No |
| Maquette / site | No |
| Source | directory |
| Détail source | annuaires Bessengue |

## Notes

Envoyé 18/09 19:42, sans maquette.

## Prochaine action

**0 relance(s) sur 3 envoyée(s).** Prochaine relance au rythme M+2 / M+4 / M+7 depuis le dernier message. Jamais deux relances le même jour.

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 4 ligne(s).*

`L44` · | **ven 18/09 19:42** | **Kamaïs Optic** (Bessengue, 678 435 460) | msg 1 — sans maquette | Envoyé | **Non** |
`L112` · | 19:42 | Centre Médical de Bonanjo · Kamaïs Optic |
`L707` · Kamaïs→other, Baird confirmé school). **Les 55 autres restent non vérifiés — je ne devine pas.**
`L761` · | ③ | **org_type : « va ligne par ligne sur les faits écrits dans la ligne. »** | Fait — **mais je n'ai pas trié à la main une par une : j'ai supprimé la cause.** `crm.py` collait `"school"` aux 38 lignes du classeur **sans jamais lire la ligne** ; voilà d'où venaient MITOC « school » et Solidarity « school ». Nouveau `org_type_for()` : l'étiquette n'existe que si un mot **du nom, des Facilities, de l'activité ou des notes** la porte (`lab` → `clinic` → `other` → `school`, dans cet ordre parce qu'« laboratoire d'analyses médicales » n'est pas une clinique). La preuve est écrite dans `Notes` (`org_type=lab prouvé par « laboratoire »`). Les overrides explicites (MITOC, One Stop, JOSS, Kamaïs, Solidarity) gagnent avant. **Résultat : 0 ligne sans étiquette et 0 ligne sans preuve** — contre 145 dont 38 affirmées « school » par défaut. |

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
