# AMK Factures — la source vivante de l'outil

```
Origine   amk-factures-pwa.zip à la racine du dépôt (archive de King, 23/10) — laissée intacte
Ce dossier est la SOURCE VIVANTE ; le zip est l'archive d'origine, jamais modifiée
Prod      https://amk-factures-pwa.vercel.app (projet Vercel amk-factures-pwa, non lié à git)
```

## Ce que fait l'outil, vérifié dans le code le 23/10

Numérotation annuelle continue (`AMK-2026-001`) · factures, **proformas**, **reçus de paiement** ·
acomptes et solde dû · **date d'échéance** avec délai réglable (14 jours par défaut) · **statut
« en retard »** et badge dans la liste · modèles de message (acompte, solde, relance, mensuel) ·
PDF et envoi WhatsApp · **MoMo, Orange Money, coordonnées bancaires, NIU** · sauvegarde par copier-coller.

**Autrement dit : l'échéance et les coordonnées de paiement y étaient déjà.** L'analyse du 23/10 qui
disait le contraire était fausse — elle a été corrigée dans `ops/FACTURATION-2026-10-24.md` §3 bis.

## Les trois ajouts du 23/10 (et rien d'autre)

1. **`dont X en retard`** sous « À encaisser » : le total dû ne mélange plus le courant et le retard.
2. **`en retard de N jours`** sur la ligne d'une facture échue, à la place de « Reste ».
3. **`Enregistrer un fichier`** à côté de « Copier la sauvegarde » : un `.json` téléchargeable, parce
   qu'un presse-papiers se perd et qu'un fichier se range.

Différence exacte : voir le commit. Aucune refonte, aucun changement de structure de données : les
trois ajouts lisent les champs qui existaient déjà (`inv.due`, `calc().bal`, `db`).

## Vérifier avant de publier

```bash
node --check <(python3 -c "import re,sys;print(re.search(r'<script>(.*?)</script>',open('index.html').read(),re.S).group(1))")
```

Puis, sur un téléphone : créer une facture antidatée (échéance passée) → la liste doit afficher
« en retard de N jours », et le résumé « dont X en retard ». Si ce n'est pas le cas, on n'a rien gagné.

## Les deux façons de publier

**① Le zip, pour un envoi manuel** — `amk-factures-pwa-v2.zip` à la racine du dépôt (6 fichiers, à plat).
King le télécharge depuis GitHub et le dépose dans Vercel (*Deploy* → *Upload*). C'est la voie qui ne
dépend de personne.

**② Le projet lié au dépôt** — `amk-factures-pwa-preview` (Vercel), racine `ops/amk-factures-pwa` :
chaque envoi sur la branche donne une preview, et la production ne bouge que sur décision.

**Dans les deux cas, vérifier avant :**

```bash
node test-calculs.mjs      # 8 assertions : statut, jours de retard, solde, montant
```

Puis sur un téléphone : une facture antidatée doit afficher « en retard de N jours » et le résumé doit
dire « dont X en retard ». Le service worker passe en cache `v4` — un appareil qui avait l'ancienne
version se met à jour au deuxième chargement.
