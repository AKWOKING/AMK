# archive/ — ce qui n'est plus vivant, mais qui n'est pas mort

Ici vont les documents **atteignables par aucun chemin de lecture** et dont la date est passée :
campagnes terminées, récoltes ponctuelles, plans d'une semaine révolue.

**Deux règles, et elles suffisent.**

1. **On archive, on ne supprime pas.** Un `git mv` vers `archive/AAAA-MM/` garde le document entier,
   son historique et sa date. Rien n'est perdu ; il cesse simplement de peser sur la carte, les audits
   et les portes — `archive/` sort du corpus (voir `SKIP_DIRS` dans `build_full_graph.py` et
   `audit_files.py`).
2. **Un document entre ici avec sa date dans le chemin.** C'est ce qui permet de savoir, dans deux ans,
   de quand il parle. Un document sans date ne peut pas expirer, donc il ne meurt jamais : c'est le
   défaut que le chantier ④ corrige.

**Ce qui n'a rien à faire ici** : une doctrine encore vraie (elle se cite), un dossier client vivant
(`clients/`), un livrable (il va en Release, pas en archive), un gabarit (il se cite depuis la machine).

L'inventaire de ce qui reste à trier est régénéré à chaque audit : `ops/FILE-AUDIT-*.md` § 4 bis.
