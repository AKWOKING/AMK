# SETUP GOOGLE BUSINESS PROFILE — DM OPTIQUE SARL · exécutable jour 1

> La fiche GBP est le premier endroit où « trouvable » devient vrai. **La vérification demande le
> téléphone ou l'e-mail du cabinet** : initier PENDANT la visite du 07/10 (le code arrive sur SON
> téléphone, on le remplit ensemble) — c'est l'item « jour 1 » par excellence. Écrit le 03/10.

## Claim & vérification
1. Sur place, `business.google.com` avec un compte Google **au nom du cabinet** (Gmail créé avec lui).
2. Rechercher « DM OPTIQUE » — probablement absent ou fiche fantôme : **créer**, pas revendiquer.
3. Vérification par code SMS/téléphone sur le 656 122 239 (ou carte postale si SMS indisponible — dans ce
   cas la fiche reste en préparation jusqu'au code, sans rien publier de faux).

## Données (vérifiées, datées, zéro invention)
- **Nom :** DM OPTIQUE SARL · **Catégorie principale :** Opticien · secondaire : Lunetterie.
- **Adresse :** Ndobo Mayor, Douala IV (Bonabéri) — **partage de position WhatsApp demandé au client** à
  la visite (leçon Cavisa : c'est lui qui connaît l'emplacement réel).
- **Horaires :** lundi à samedi ; examen de vue 8h30–13h00 ; autres besoins 8h30–17h30 (verbatim client du 08/10, confirmé le 10/10 ; jours confirmés le 15/10 à 23:36).
- **Téléphone/WhatsApp :** 656 122 239 · **site :** l'adresse Vercel post-déploiement (pas avant).
- **Description (750 car. max) :** « Opticien inscrit à l'ONOC.
  Examen de vue, montures homme et femme, solaires et enfants. Écrivez-nous sur WhatsApp, on vous
  répond. » — pas de claim médical, pas de « meilleur », pas de prix.

## Les 10 premières photos (liste de shoot, `photoshoot/`)
1 entrée de cabinet (B1) · 2 salle d'examen (B2) · 3 mains qui ajustent une monture (C1) · 4 monture
tenue à hauteur (C2) · 5 monture face catalogue (A1) · 6 profil branches (A3) · 7 vitrine/salle de vente ·
8 comptoir · 9 façade avec enseigne lisible depuis la chaussée · 10 le titulaire au comptoir (s'il
accepte — sinon remplacer par un détail d'atelier). Légendes factuelles, jamais « notre équipe souriante ».

## Jour 1 vs plus tard
Jour 1 : claim + données + description + heures. Après les photos : les 10. Jamais acheter d'avis, jamais
répondre à un avis avec un claim — remercier, fait.

## Adresse — précision (ruling King 08/10)

**Ligne 2 de l'adresse / complément :** « Immeuble West Hotel, 1er étage, dernière porte à droite » — l'épingle seule ne dit pas l'étage ; un client qui monte au rez-de-chaussée se trompe de porte.

## Préparation local-seo (portion gratuite — méthodologie open-seo `local-seo`, 20/10)

Ce que la portion gratuite de la méthodologie ajoute à ce qui précède (claim, données, description,
photos, avis déjà réglés ci-dessus) :

- **Services (champ GBP)** : Examen de la vue · Verres sur ordonnance · Montures femme · Montures
  homme · Montures enfants · Réglage et réparation — libellés du site, zéro invention.
- **« Produits » (fiches collections GBP)** : trois collections avec photo — Lunettes de vue,
  Lunettes de soleil (photo d'illustration tant que pas de photo réelle), Montures enfants.
  Aucun prix (verrou client).
- **Lien de rendez-vous (bouton GBP)** : le wa.me du cabinet avec le message examen déjà écrit
  (`https://wa.me/237656122239?text=…examen de la vue…`) — même messagerie que le site.
- **Attributs** : seulement ceux vrais (accès à l'étage par escalier — pas de fausse accessibilité).
- **Suivi de positions géo-grille** : portion payante (DataForSEO) → reportée avec la décision
  open-seo ; en attendant, la mesure honnête = Search Console (gratuit, première partie) après
  mise en production.
- **Le relais AEO est prêt** : `llms.txt` à la racine du site (48 liens, coordonnées) — la fiche
  et le site racontent la même chose, en même temps.

## Création du compte Google — valeurs exactes (20/10, King sur l'écran « Create a Google Account »)

| Écran | Valeur |
|---|---|
| First name | **DM OPTIQUE** |
| Surname (optional) | **SARL** (le nom affiché sera « DM Optique SARL ») |
| Birthday | la date de naissance de **King** (le compte est géré par lui) |
| Username | `dmoptiquesarl@gmail.com` (si pris : `dmoptiquesarl237`) |
| Password | **gestionnaire de mots de passe de King** — jamais dans le dépôt (public) |
| Recovery email | l'e-mail personnel de King |
| Recovery phone | le **656 122 239** (SMS cabinet) — sinon le téléphone de King pour la vérification du COMPTE ; la vérification de la FICHE GBP reste sur le 656 122 239 |

Après création : activer la 2FA (recovery sur King), puis l'ordre ci-dessous.

## Ordre des opérations (20/10, décision King : Google AVANT Facebook/TikTok)

1. **Apex d'abord** (2 min) : Workers & Pages → `dmoptiquesarl` → Domains → + Add Domain →
   `dmoptiquesarl.com` — sinon la racine reste morte et le sitemap canonique sera injoignable.
2. **Search Console** (5 min) : avec le compte du cabinet → propriété **Domaine**
   `dmoptiquesarl.com` → copier l'enregistrement **TXT** `google-site-verification=…` → le coller
   dans Cloudflare (le domaine → DNS → Add record, Type TXT, Name `@`) → Verify →
   soumettre `https://dmoptiquesarl.com/sitemap.xml` → Inspection d'URL + « Demander une
   indexation » sur `/`, `/montures/`, `/examen-de-vue/` et une fiche.
3. **Mesure** (2 min) : Cloudflare Web Analytics (toggle) — GA4 plus tard = décision séparée.
4. **Fiche GBP** (20 min) : `business.google.com` avec le compte du cabinet → tout est préparé
   ci-dessus (nom, catégories, adresse, horaires, téléphone, site, description, photos,
   services, lien wa.me) → vérification **SMS vers +237 656 122 239** → **la seule action de
   M. Domche : transférer le code** (déjà demandé dans le fil WhatsApp, asynchrone).
5. **Ensuite seulement** : comptes Facebook et TikTok au nom du cabinet (item du message client).

## Voie rapide (20/10, décision King) — les comptes Google, créés par l'agence, au nom du cabinet

Le client est difficile à joindre (fuseau différent, réponses lentes) : on crée les comptes
**maintenant, sans lui**, en respectant la règle « comptes au nom du client » — le compte est au
nom du cabinet, AMK le gère dans l'abonnement mensuel, et la ligne de propriété part par écrit.

1. **E-mail du cabinet (5 min, sans le client)** : créer `dmoptiquesarl@gmail.com` — nom affiché
   « DM OPTIQUE SARL » ; e-mail de secours = celui de King ; téléphone de secours = celui de
   King ; 2FA activée. **Le mot de passe ne va JAMAIS dans le dépôt (public)** : il vit dans le
   gestionnaire de King. Ligne écrite au client : « on vous crée et on gère vos comptes Google
   (e-mail, fiche, Search Console) — l'e-mail est à votre nom, AMK le gère dans l'abonnement » ;
   consigné « pratique » à l'Activity-Log.
2. **Search Console (5 min, sans le client)** : propriété **Domaine** `dmoptiquesarl.com` avec
   ce compte → enregistrement TXT dans la zone Cloudflare (déjà dans le compte de King) →
   soumettre `sitemap.xml` (48 URL) → demander l'indexation de `/`, `/montures/`,
   `/examen-de-vue/` + une fiche. **Zéro dépendance client.**
3. **Analytics** : première mesure = **Cloudflare Web Analytics** (toggle dans le dashboard,
   zéro changement de site). GA4 plus tard = décision séparée (un build avec le snippet, portiques
   + déploiement §1f③).
4. **Fiche GBP (20 min, sans le client)** : créer la fiche avec le compte du cabinet — tout est
   déjà préparé ci-dessus (nom, catégories, adresse, horaires, téléphone, site
   `www.dmoptiquesarl.com`, description, photos, services, lien wa.me). À la vérification,
   choisir **SMS vers +237 656 122 239** : **la seule action du client = transférer le code**
   (« quand un code Google arrive par SMS sur le 656 122 239, envoyez-le nous ») — asynchrone,
   10 secondes, aucune séance à planifier. Repli : carte postale.
5. **Ce que le client garde** : la propriété des comptes, le téléphone (vérification, puis
   récupération secondaire une fois son accord écrit reçu), la parole dans les réponses aux avis.

## Profil CRÉÉ (20/10 soir, capture) — les valeurs à aligner avant le mot « terminé »

La fiche apparaît sur Google (« DM OPTIQUE SARL — Optician in Bonabéri — You manage this Business
Profile », bouton Website présent). Trois choses à vérifier/corriger dans « Edit profile » :

1. **Adresse** : la capture montre « Ndobo Bonaberi, Douala ». Valeur exacte à aligner sur le site
   (cohérence NAP = règle locale-seo) : **Ndobo Mayor, Immeuble West Hotel, 1er étage, dernière
   porte à droite, Bonabéri, Douala**.
2. **Téléphone** : la capture montre « 6 56 12 22 39 » (espacé, sans indicatif). Valeur exacte :
   **+237 656 122 239** (identique au site et au wa.me).
3. **Horaires** : poster **lun–sam 8:30–17:30** (la fiche Google ne gère pas deux créneaux par
   besoin) — la nuance « examen 8:30–13:00 » vit déjà dans la description et sur le site.
   La capture montre « Opens 8:30 am Wed » : vérifier que tous les jours sont bien saisis.

Puis compléter le profil (les cartes de l'écran d'accueil) :
- **Photos** : la liste des 10 premières est au-dessus (§Les 10 premières photos).
- **Description + services + catégories** : tout est prêt dans §Données.
- **« Add social profiles »** : **faisable depuis le 21/10** — le TikTok `@dmoptique.bonaberi237` existe
  et la page Facebook `DM OPTIQUE SARL` aussi ; **attendre le `@username` de la page** pour poser une
  URL propre (jamais un lien vers un identifiant numérique).
- **« Create ad »** : Skip — aucune dépense publicitaire sans décision King.
- **Vérification** : si un bandeau « pending verification » reste visible, faire passer le code SMS
  (656 122 239) à M. Domche.
