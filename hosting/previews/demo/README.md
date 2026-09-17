# BIBLIOTHÈQUE DE DÉMOS PUBLIABLES (17 Sep 2026)

**Pourquoi :** nos concepts contiennent l'identité de vrais prospects — interdits dans un contenu public sans autorisation écrite (règle de King, 17 Sep). Ces copies sont **fictives** : marque « MboaCare », numéro de démonstration `600 00 00 00`, adresses banalisées, `noindex`, bandeau de démonstration. Elles servent de **matière première filmable** pour les vidéos.

| Fichier | Dérivé de | Ce que la démo démontre |
|---|---|---|
| `jempo-demo.html` | JEMPO (polyclinique, Deido) | accueil polyclinique : 4 spécialités, 24h/24, accès, FAQ |
| `labethanie-demo.html` | La Béthanie (médico-chirurgical, Bonabéri) | maternité + urgences, prestations en liste cochable |
| `oracare-demo.html` | OraCare (dentaire, Buea) | grille de tarifs FCFA + assistant |
| `yaks-demo.html` | YAKS (dentaire, Logbessou) | roue des 6 spécialités, plaquette |
| `opticien-demo.html` | L'Opticien (Bali) | contrôle de la vue, montures, devis WhatsApp |

**Régénérer / vérifier** (après toute modification d'un concept) :
```bash
python3 tools/video/anonymise.py --all      # régénère + contrôle de fuite + audit HTML
```
Le script **échoue** s'il reste un numéro réel, une marque, un nom de praticien ou une adresse identifiante, ou si l'audit HTML relève la moindre anomalie.

**Déploiement (King) :** un projet Vercel, dossier `hosting/previews/demo` → `https://mboacare-demo.vercel.app/<fichier>`. Utile pour filmer au téléphone, **et** pour les captures de la chaîne `tools/video/`.

**À ne jamais faire :** publier une démo en la présentant comme un client réel. Toute capture à l'écran porte l'étiquette « MBOACARE (FICTIF) · DÉMONSTRATION ».


## Déjà en ligne chez King (rappel — ne pas dupliquer inutilement)

| URL | Nature | Usage vidéo |
|---|---|---|
| **https://amk-cm.vercel.app/clinic-bonaberi.html** | maquette clinique + laboratoire (Bonabéri Medical Centre) — **fictive, template** | ✅ matériel vidéo direct |
| **https://amk-cm.vercel.app/sample-nursery.html** | maquette école maternelle/primaire (Little Oaks) — fictive | ✅ |
| **https://amk-cm.vercel.app/sample-school.html** | maquette école bilingue K-12 (Nova) — fictive | ✅ |
| **https://amk-cm.vercel.app/sample-secondary.html** | maquette collège secondaire (Crestwood College) — fictive | ✅ |
| **https://mboa-gamma.vercel.app** | démo MboaCare (clinique, studio « after ») — **déployée par King le 17/09** | ✅ |

Ces cinq pages sont **publiques et fictives** : aucune autorisation à demander, aucune anonymisation à faire. Ce sont elles la matière première par défaut — les démos anonymisées de ce dossier servent quand on veut montrer un **type de site différent** (polyclinique, maternité, optique, dentaire).
