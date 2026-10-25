# Le Bon Diagnostic

> ⚙️ **Fiche générée** par `leads/build/records.py` le 2026-10-25. Ne pas modifier à la main — les corrections vont dans `sales/Activity-Log.md`, et remontent ici au passage suivant.

## État (lu dans `leads/CRM.csv`)

| Champ | Valeur |
|---|---|
| Slug | le-bon-diagnostic-elf |
| Type | lab |
| Ville | Douala (Elf, Axe-Lourd) |
| Langue de contact | FR |
| Étape | disqualified |
| WhatsApp | 699 95 67 32 |
| Numéro vérifié | no |
| Contacté | No |
| Réponse | No |
| Maquette / site | No |
| Source | directory |
| Détail source | annuaires de Douala |
| Site vérifié le | 2026-09-19 |
| Site existant | https://www.lebondiagnostic.com |

## Pourquoi il est écarté

A DÉJÀ UN SITE VIVANT (https://www.lebondiagnostic.com). Hors cible — vérifié AVANT toute production (règle 66).

## Notes

⛔ NE PAS ENVOYER. Site référencé dans les annuaires. Écarté le 19/09 pendant la préparation du pack LABOS. C'est exactement le piège QUALITECH/Clinique des Anges — sauf que cette fois la vérification est passée avant la production, pas après.

## Prochaine action

**Aucune.** Lead écarté — A DÉJÀ UN SITE VIVANT (https://www.lebondiagnostic.com). Hors cible — vérifié AVANT toute production (règle 66).

## Historique — lignes du journal qui citent ce lead

*Source : `sales/Activity-Log.md` — citation, jamais recopie. 4 ligne(s).*

`L1320` · « Diagnostic en deux temps » et « OPTICAL SERVICES DOUALA » dans le journal, j'ai fait **fuitér ces
`L1321` · lignes vers les fiches de deux AUTRES leads** (`le-bon-diagnostic-elf`, `gift-optical`) — le générateur
`L5410` · - 22/10/2026 · **DM Optique — diagnostic du 403 sitemap corrigé + redirection www→apex** : la capture Cloudflare (*Bot traffic 0/1 running*, 0,91 % mitigé) **écarte la protection anti-robots** ; 403 = 1 seule instance → resoumettre et attendre 24 h ; `www` et apex servent tous deux le site → ajout d'un `_redirects` **301 www → apex** au build (effet au prochain zip) ; recommandation d'une **propriété de domaine** Search Console (couvre les deux hôtes). `URLS-INDEXATION` §8 réécrit, zip 183 entrées.
`L5419` · - 22/10/2026 · **DM Optique — « où est le post 1 ? » : les vidéos étaient invisibles sur GitHub ET perdues du disque ; reconstruites et publiées en release** : diagnostic à deux volets — ⑴ le `.gitignore` exclut `*.mp4`/`*.mp3` depuis le **23/09** (règle de King : « le repo n'est pas un disque dur »), donc **aucun livrable vidéo n'apparaît jamais sur GitHub** ; ⑵ l'espace de travail a été remis à zéro (**18ᵉ épisode**), et comme les fichiers étaient ignorés, aucun `checkout` ne pouvait les ramener — `git ls-files` ne montre que 7 vieux mp4. **Récupération** : `fetch` + `reset --mixed origin/arena/2fffee3b-amk` + `checkout -- .` (jamais `--hard`), HEAD `e861057`. **Remontage des deux vidéos** avec la voix `voice-00` régénérée (texte pris dans le `.srt` et dans `ugc-03.md`) : `tiktok-01-v2.mp4` **23,00 s / 4,8 Mo** et `ugc-03.mp4` **22,30 s / 6,8 Mo**, **portique OK pour les deux**. **Correctif de fond** : dépôt des fichiers en **release GitHub `dm-optique-videos-2026-10-22`** (téléchargeable, permanent, zéro poids dans l'arbre) + index `content/month1/w1/VIDEOS.md` (où, quoi, comment reproduire) + renvoi depuis `tiktok-01-PUBLICATION.md`. **Décision King appliquée** : sans-visage conservé, **aucun abonnement d'avatar IA, aucune clé Veo** — budget réservé à **une demi-journée de tournage par mois**, plan opérationnel écrit (`content/tournage/PLAN-TOURNAGE-MENSUEL.md` : déroulé 14h–18h, 4 blocs, liste de plans imprimable avec phrases mot pour mot, matériel, autorisation d'image, nommage, circuit rush → `tools/ugc` → portique → release, calendrier). Knowledge mis à jour : `CONTENT-CREATION` §6 (voie tranchée) et `research/ugc-video` §7.

---

## À la main (facultatif)

*Ce que tu écris ici est perdu au prochain passage du générateur. Pour garder une information, mets-la dans `sales/Activity-Log.md`.*
