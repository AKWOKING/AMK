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
