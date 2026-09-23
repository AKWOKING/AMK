# Ctre d'Analyses Médicales Pasteur Medlas

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-09-23. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | pasteur-medlas-akwa |
| Type | lab |
| Ville | Douala (Akwa, Bld de la République) |
| Langue de contact | FR |
| Étape | parked |
| WhatsApp | 677 45 99 97 |
| Numéro vérifié | unknown |
| Canal | WhatsApp |
| Contacté | Yes |
| Relances envoyées | 0 |
| Source | directory |
| Détail source | pagespratiquescm |

## Notes

Envoyé le 19/09 à 19:25 — lu (2 coches). · ⚰️ MORT le 22/09 (lot du 19/09) — jamais ouvert, jamais répondu ; décision de King : on ne réécrit plus, on va vers des prospects frais. Aucune relance programmée.

## Prochaine action

**Aucune.** Parqué. Une action n'est légitime que si King le décide explicitement.

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 1 ligne(s).*

`L761` · | ③ | **org_type : « va ligne par ligne sur les faits écrits dans la ligne. »** | Fait — **mais je n'ai pas trié à la main une par une : j'ai supprimé la cause.** `crm.py` collait `"school"` aux 38 lignes du classeur **sans jamais lire la ligne** ; voilà d'où venaient MITOC « school » et Solidarity « school ». Nouveau `org_type_for()` : l'étiquette n'existe que si un mot **du nom, des Facilities, de l'activité ou des notes** la porte (`lab` → `clinic` → `other` → `school`, dans cet ordre parce qu'« laboratoire d'analyses médicales » n'est pas une clinique). La preuve est écrite dans `Notes` (`org_type=lab prouvé par « laboratoire »`). Les overrides explicites (MITOC, One Stop, JOSS, Kamaïs, Solidarity) gagnent avant. **Résultat : 0 ligne sans étiquette et 0 ligne sans preuve** — contre 145 dont 38 affirmées « school » par défaut. |

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
