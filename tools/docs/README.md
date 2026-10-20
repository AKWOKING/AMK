# tools/docs — production documentaire AMK (pile libre)

**Né de l'audit du 20/10 (demande King : « audit and see if this helps in our workflow or if we
can sell it as an additional service » sur `anthropics/skills`).** Verdict complet au
`ops/TOOL-SCAN.md` : les skills documentaires amont (docx, pdf, pptx, xlsx) sont **« source-available »**
avec interdiction explicite d'extraction, de copie et de works dérivés hors des Services
Anthropic — ils ne sont **pas installés** ici. Les skills Apache du même dépôt recouvrent notre
pile existante (taste, portiques Node) et n'ajoutent rien — non installés non plus.

**Ce qui est retenu : la méthode, réimplémentée avec une pile libre** — `openpyxl` (MIT) pour
xlsx ; la méthodologie professionnelle est standard (fonte lisible, zéro erreur de formule,
sources citées dans le fichier, gabarits de remplissage documentés).

## Ce qui existe

- **`xlsx_build.py`** — construit un tableau xlsx propre (titre, ligne de source, en-têtes crème
  sur marine, zébrures, colonnes dimensionnées, volet figé) à partir d'un JSON simple.

```bash
python3 tools/docs/xlsx_build.py entree.json sortie.xlsx --title "..." --source "frames.json @ 376b199"
```

## Usage réel (première production, 20/10)

`clients/dm-optic/launch/LISTE-40-MONTURES-2026-10.xlsx` — l'inventaire des 40 montures de
DM Optique (généré depuis `site/frames.json`), livrable de confirmation au client, avec sa
version WhatsApp texte `LISTE-40-MONTURES-WHATSAPP.txt`.

## Ajouts prévus (à la demande)

pdf (reportlab, AGPL-1.1+ côté lib — vérifier les termes avant usage client), docx (python-docx,
MIT), pptx (python-pptx, MIT). **Aucune dépendance n'est installée d'office** — chaque ajout est
une décision nommée (règle 5 TOOL-SCAN). Aucune donnée client ne sort de la machine : tout est
généré localement.
