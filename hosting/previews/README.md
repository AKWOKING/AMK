# AMK — Client preview hosting (King self-hosts)

## ⛔ GEL — Le Cristallin et Univers Optique (décision de King, 23/09/2026 au soir)

> **« Pour lecristallin et univers on ne touche plus rien jusqu'à ce que les prospects deviennent des
> clients payants. »**

Ce que ça veut dire concrètement dans ce dossier :

1. **Aucune modification** de `demos/concept-le-cristallin-v1.html`, `demos/univers-optique-site-v2.html`,
   des fichiers `concept-univers-optique-v*.html` et de leurs builders. Pas d'ajustement, pas de « petite
   retouche », pas de rebuild.
2. **Ne JAMAIS redéployer le Cristallin depuis ce dépôt.** La page en ligne
   (`lecristallin-concept.vercel.app`, projet Vercel de King) est **en avance sur notre copie** : elle porte
   déjà le slogan dans la barre, les textes d'origine sur les verres et l'adresse Ancien COMECI / ECOTEX,
   et ses liens WhatsApp sont en `wa.me/237699905577` (corrects). Notre copie locale **ne les a pas** :
   un déploiement depuis ce dépôt **écraserait le travail que le client regarde**.
   *Vérifié le 23/09 par lecture de la page en ligne — notre alerte « bouton mort » d'hier concernait
   notre copie locale, pas la page servie.*
3. La règle du client complète la nôtre, mot pour mot (21:58, 22/09) : « Pour le reste ne change encore rien
   puisque j'ai certains modifications que tu as apporté sans mon ok. »
4. **Ce qui reste permis** : les marquer comme clients, encaisser, répondre à leurs messages. **Rien
   d'autre** tant qu'ils n'ont pas payé.
5. Quand ils paient, le dossier de reprise est `clients/<slug>/build-notes.md` — pas ce dossier-ci.


This folder is a **drag-and-drop deploy bundle**. Every concept is a single self-contained `index.html` (base64 images, no local assets), so any static host works.

## URLs after deploy (example project name: `amk-previews`)

| Slug | LIVE link | Lead | Canonical source file |
|---|---|---|---|
| **separate Vercel project** (projets `dmoptic` **et** `dmoptic-2`) | ✅ **LIVE https://dmoptic-2.vercel.app/** — déployé **et envoyé par King le 24/09 à 17:05** ; la **v2.1** est bien celle qui est servie (vérifiée en lisant le HTML servi le même soir). ⚠️ l'ancienne `dmoptic.vercel.app` sert encore la v1 : ne plus la considérer comme l'adresse du client. **v2.1** : la page parle au patient, liste ses services et **montre les montures** (vue · soleil · enfants) ; le registre est sorti du texte visible. ⚠️ **Déployer LE DOSSIER ENTIER** (`index.html` **+** `og.jpg`) : sans la vignette, le lien arrive en carte grise. **Puis** `python3 demos/build_dmoptic.py --url https://<adresse>` et **redéployer** : `og:url`/`og:image` ne se devinent pas (§20.7). 0 capture ni mockup (pas de navigateur dans le bac) : l'œil de King sur un téléphone, en plein jour, avant d'envoyer. | **DM OPTIC** (M. Domche Noumbi), Douala — `demo`, aperçu **en ligne et envoyé**, en attente de son retour | `demos/concept-dmoptic-v1.html` ← gabarit `demos/dmoptic-v1.tpl.html` + `demos/build_dmoptic.py` |
| **separate Vercel project** (projet `cinqsens`) | ✅ **LIVE https://cinqsens.vercel.app/** — déployé **et envoyé par King le 24/09 à 17:54** ; la page servie a été relue : c'est bien la **passe 2**. ⚠️ `og:url`/`og:image` étaient **vides** à l'envoi (carte sans vignette) : recollés sur l'adresse réelle dans le dépôt — **un seul redéploiement** et les partages suivants porteront l'image. **passe 2** : la page parle au patient et prend le cabinet **à son image** (affiche, rail de cinq teintes qui entre en cascade, **lueur dérivante** au premier écran, bande d'arrivage, deux raccourcis de carte). ⚠️ **Déployer LE DOSSIER ENTIER** (`index.html` **+** `og.jpg`) ; **puis** `python3 demos/build_cinqsens.py --url https://<adresse>` et **redéployer** — `og:url`/`og:image` ne se devinent pas (§20.7). ⚠️ **Ne jamais écrire « vous n'avez pas de page »** : leur blog existe, il s'arrête au **15/10/2021**. 0 capture ni mockup (pas de navigateur dans le bac) : l'œil de King sur un téléphone, FR **et** EN, avant d'envoyer. | **CINQ SENS** (R.O.M. Cinq Sens SARL), Douala — Akwa + Brazzaville — `demo`, aperçu construit, cabinet d'accord (« Ok » 17:04), **lien envoyé à 17:54**, en attente de son retour | `demos/concept-cinqsens-v1.html` ← gabarit `demos/cinqsens-v1.tpl.html` + `demos/build_cinqsens.py`, images `demos/img/cinqsens-*.jpg` |
| **separate Vercel project** ou `/cavisa/` | ✅ **LIVE https://cavisa.vercel.app/** (déployé par King le 24/09, envoyé à M. Dongmo à 13:09 — il a répondu à 13:16). ⚠️ **À REDÉPLOYER : dossier ENTIER** (`index.html` + `og.jpg`) — la vignette du lien (`og:image`, remplie le 24/09 avec l'adresse réelle) et les photos 2026 ne sont en ligne qu'après ce redéploiement. **Après déploiement : coller l'adresse dans `og:url`/`og:image` (bloc commenté du gabarit), relancer `python3 demos/build_cavisa.py`, redéployer** — sinon le lien arrive chez Cavisa en carte grise. ⚠️ 0 capture ni mockup (pas de navigateur dans le bac) : `node tools/video/capture.mjs --mode hero` à faire sur la machine de King. | **CAVISA OPTIQUE** (M. Dongmo Jean René), Douala — a accepté la démo le **24/09 à 12:23** ; lien promis par King à 12:16 | `hosting/previews/cavisa/index.html` ← `demos/concept-cavisa-v1.html` (gabarit `demos/cavisa-v1.tpl.html` + `demos/build_cavisa.py`) |
| **separate Vercel project** | 🟡 **à déployer — King** (projet `mboacare-demo`) | **DÉMO MBOACARE** (fictive, publiable) — clinique de démonstration | `hosting/previews/mboacare-demo/index.html` |
| **`/demo/` (bundle)** | 🟡 **à déployer — King** — **bibliothèque de 5 démos publiables** (polyclinique, maternité, dentaire ×2, optique), 0 fuite d'identité, audit 0 | matière première des vidéos | `hosting/previews/demo/*.html` |
| **separate Vercel project** | ✅ **LIVE https://uni-labo.vercel.app** (déployé par King 18/09 22:05). ⚠️ **la page en ligne est encore celle du 18/09 — à redéployer** (revérifié le 24/09 au soir en lisant le HTML servi : il contient encore des phrases qui n'existent QUE dans la v1, p. ex. « La préparation, écrite noir sur blanc ». Le dossier du dépôt, lui, est **la v2 au byte près** : `cmp` le confirme). **Avant le rendez-vous de 13 h, vendredi 25/09.** 24/09 (nuit du 23 au 24 — commit `e936a03`, 00:03) : **la page a été réécrite de zéro** après le verdict de King (« the pictures seem to have spoiled everything ») — mobile d'abord, cinq photographies cantonnées au lieu de huit, plus de texte sur les images, hero sans photo, la fiche de prélèvement comme seul motif. Le contenu du laboratoire et son JavaScript sont repris mot pour mot (42 assertions vertes, `demos/concept-unilabo-v2.html` = 85 299 o). ⚠️ **le dossier `unilabo/` porte un sous-dossier `img/` (dix fichiers : cinq photos + leurs variantes légères) : déployer LE DOSSIER ENTIER, pas seulement `index.html`.** | **UNI-LABO**, Bonamoussadi Douala | `demos/concept-unilabo-v2.html` |
| **separate Vercel project** | ✅ LIVE **https://concept-afriquelabo-v1.vercel.app** (déployé 17/09) | Afrique Labo SARL, Bessengue Douala | `demos/concept-afriquelabo-v1.html` |
| **separate Vercel project** | ✅ LIVE **https://concept-skye.vercel.app/** (King's Vercel project `concept-skye`; re-deploy after each sync of the `skye` folder) | Cabinet Dentaire The Skye, Bonamoussadi Douala | `demos/concept-skye-v1.html` |
| **separate Vercel project** | ✅ LIVE **https://concept-yaks-v1.vercel.app/** (King's Vercel project `concept-yaks-v1`; re-deploy after each sync of the `yaks` folder) | Cabinet Dentaire YAKS, Logbessou Douala | `demos/concept-yaks-v1.html` |
| **`/cristallin/`** (bundle) **ou projet `concept-le-cristallin-v1`** | 🟡 **à déployer — King (21/09 soir)** — **AUCUNE URL N'EXISTE AVANT LE DÉPLOIEMENT : ne pas envoyer `amk-cm.vercel.app/cristallin/` tant que ce n'est pas en ligne, et ne jamais deviner l'URL.** Alternative immédiate sans Vercel : envoyer le fichier lui-même (58 KB, s'ouvre dans le navigateur d'un téléphone). ⚠️ **Écart au deploy-gate assumé et écrit :** (1) capture 1280×800 + mockup non produits ici (`playwright` absent du bac) — À FAIRE sur la machine de King, sinon envoyer le fichier ; (2) **les 12 assureurs ne sont pas confirmés sur la page d'accueil lue** : la page les affiche avec la mention « à faire valider avant publication », donc LA QUESTION EST À POSER, pas à laisser dans le flou ; (3) aucune photo du cabinet : 3 cadres dessinés étiquetés « à remplacer par vos photos ». | **Le Cristallin**, Douala (Akwa / Bonapriso) — **a répondu « Ok » 21/09 17:53** ; refonte de `lecristallinoptique.com`. ⚠️ **23/09 : la page portait un lien WhatsApp MORT** (`wa.me/699905577`, numéro sans indicatif pays — WhatsApp refuse) : corrigé dans la source, **à REDÉPLOYER pour que le bouton fonctionne** ; même correctif pour `tel:` (+ indicatif). Le bac ne peut pas déployer (pas de jeton Vercel) : c'est King. | `hosting/previews/cristallin/index.html` ← `demos/concept-le-cristallin-v1.html` |
| `/` | private marker, deliberately no links | — | — |

**Current model (King, 14 Sep):** one Vercel project per named concept, deployed from the canonical HTML (index.html at project root). To push an update: overwrite that project's root index.html with the rebuilt canonical file and redeploy. The `build_previews.py` bundle remains available as a single-project multi-slug alternative for future batches.

Every preview carries `noindex,nofollow` (private previews, never search-listed). Rebuild the bundle after editing any concept:

```bash
python3 hosting/build_previews.py
```

## Deploying a NEW named concept (recipe used 17 Sep for La Béthanie / JEMPO)

1. `python3 hosting/build_previews.py` → the bundle folder is refreshed (and the standalone HTML is already the canonical file).
2. New Vercel project from the canonical file: put `demos/concept-<client>-v1.html` as **`index.html`** at the project root → deploy → rename the project to `concept-<client>-v1`.
3. Phone QA (deploy-gate list above) **on the live URL**, not the laptop.
4. Send **image first** (`demos/shots/mockup-<client>-wa.jpg`), then the text from the send sheet — never both in one message.
5. **Footers:** every concept built from 17 Sep 2026 comes with the §20 footer standard (4 blocks + strip). Get asked about it? It is `AMK-DESIGN-SKILLS.md` §20.

## Deploy gate (added 17 Sep 2026 — from the engineering batch, `AMK-DESIGN-SKILLS.md` §18.4)

Before any concept URL goes to a prospect, on a **phone** (not the laptop preview):
1. Page boots in **FR** (default), the EN|FR toggle switches the whole page back and forth.
2. **One real WhatsApp prefill opened** from an in-page CTA — correct number, correct French text, correctly URL-encoded.
3. The sticky mobile CTA is visible and tappable; the nav is one line; no horizontal overflow.
4. The prospect's real facts render (name, address, phone) — and every unreal number carries its DEMO label.
5. **Value provenance pass** (`§18.1`): each price/hour/count traced to a source or labelled sample; no orphan values.
6. After any post-deploy fix, re-verify the same items on the live URL — the deployed file, not the local copy.

**Ce que veut dire « sur un téléphone », depuis le 23/09 au soir** (`AMK-DESIGN-SKILLS.md` §24.3.5, d'après
Jesse Showalter) : **la nuit**, **en plein soleil**, sur **Android** et sur **iOS**. C'est trois minutes
de travail qui attrapent ce qu'aucun aperçu de bureau ne montre — et pour un laboratoire dont les patients
consultent dehors, en journée, c'est le seul test qui compte.

**Et deux critères d'œil, à faire une fois la page ouverte** (Flux Academy, §24.2) :
1. regarder **chaque section seule**, à 390 px de large : est-ce qu'elle tiendrait, imprimée, comme une
   affiche ? Si une section n'est qu'un empilement de paragraphes, elle n'est pas finie ;
2. vérifier qu'il n'y a **qu'une seule action principale** par écran (§24.3.1 — s'il n'y a pas de « grand
   cercle », la page a un problème partout).

Not verified on a phone = not sent.

## Hosting priority (14 Sep 2026)

**Deploy today, before anything else:**
1. **`/oracare/`** — the only live conversation; Dr. Nkafu was already promised the preview today. This is v3: FCFA prices **and** the 24/7 assistant (his sent message promised both).
2. **`/sasse/`** — needed for the TikTok DM + email going out today.
3. **`/comobil/`** — have it live before the Messenger "oui" so the link goes back within the hour.
4. **`/sah/`** — deploy after King's phone check of sahiscol.org (do not send the school the link until the check).

**Next, agency-facing (separate project/domain):**
5. The whole **`site/`** folder (agency homepage + the three nameless templates Nova / Little Oaks / Crestwood) → the AMK domain / `amk-cm.vercel.app`. That is public and indexable; do NOT add noindex there.
6. The clinic switcher demo already referenced as `demo-cliniques-cm.vercel.app` — its source is not in the repo; keep that deployment as-is or drop its folder into the repo so v3 can replace its OraCare variant.

**Do not host publicly:** rien de la liste ci-dessus n'est public — chaque aperçu est partagé un-à-un (noindex). Les fichiers des démos retirées le 23/09 (JEMPO, La Béthanie, SJC Sasse, COMOBIL, SAHISCOL, La Retraite, OraCare v1, L'Opticien v1) sont supprimés du dépôt : voir le commit `38b7f06` pour la liste exacte et la commande de restauration.

## Option A — Vercel from GitHub (recommended)
1. Push the repo; on vercel.app → **Add New → Project** → import AKWOKING/AMK.
2. Set **Root Directory** = `hosting/previews`, Framework Preset = **Other**, Build Command = none, Output = `public` is not needed (leave defaults).
3. Deploy. Rename the project (Settings → Domains) to something plain like `amk-previews`.
4. Re-deploy is automatic on every push after `python3 hosting/build_previews.py` is run and committed.

## Option B — Vercel CLI (fastest, no Git settings)
```bash
npm i -g vercel
cd hosting/previews
vercel            # preview URL
vercel --prod     # production URL after checking
```

## Option C — Netlify Drop (no account setup friction)
Go to app.netlify.com/drop and drag the **`hosting/previews`** folder. Subfolder links then read `https://<random>.netlify.app/oracare/` (rename the site in site settings).

## Sending rules
- Send the **subfolder link**, never the raw GitHub URL.
- On the client's own domain after close: site goes to a folder/project in THEIR name, domain registered in THEIR name (internal checklist rule).
- Re-shoot `demos/shots/oracare-v3-*` once v3 is live (the existing shot shows v2 without the assistant FAB).
- HTTPS and mobile viewport already work on all these hosts; the links open full-screen on a phone, which is the whole pitch.

— Akwo King / AMK – Web Development & Digital Solutions

## Nettoyage du 23/09/2026

Les aperçus des prospects **parqués / morts** ont été retirés du dépôt (et de la liste de génération) :
JEMPO, La Béthanie, SJC Sasse, COMOBIL, SAHISCOL, la démo Collège La Retraite, OraCare v1 et la copie
bundle `/oracare/` (le projet Vercel d'OraCare v3 reste en ligne, indépendant), L'Opticien v1.
Les **démos publiables sans identité client** (`/demo/`, `/mboacare-demo/`) sont **gardées** : ce sont les
seules pièces qu'on peut montrer sans le nom d'un client. Tout est récupérable depuis l'historique git.
