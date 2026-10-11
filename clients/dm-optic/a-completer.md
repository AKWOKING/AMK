# DM OPTIC — ce qu'il reste à nous envoyer

**Document de travail. Il part dans la conversation WhatsApp — il n'est plus sur la page.**
Depuis la v2.1 (24/09 au soir), la page parle **au patient** : six services listés, une vitrine de
montures, et plus aucun détail administratif du titulaire. La liste de ce qui manque vit donc ici.

*Mis à jour le **27/09/2026** (v2.2) : ses « Quelques Modifications » du 25/09 sont appliquées — le
nom, l'adresse et les **heures** sont écrits sur la page. Les lignes 1 et 2 sont donc en partie
satisfaites : il reste **les jours**, **un point de repère**, et les **photos** (les trois images de la
vitrine sont encore des illustrations).*

| # | Ce qu'on attend de M. Domche | Ce que ça change sur la page | État |
|---|---|---|---|
| 1 | **Un point de repère** en plus de l'adresse (« en face de… », « à côté de… ») — l'adresse est donnée depuis le 25/09 : **Ndobo Mayor, immeuble West Hotel, Bonabéri** | Elle est écrite sur la page, dans le schéma Google et dans la fiche contact depuis la v2.2. Un repère de plus vaut mieux qu'un plus code pour un patient qui arrive en taxi | **adresse ✓ · repère CLOSED 08/10** (King sur place : Immeuble West Hotel, 1er étage, dernière porte à droite) |
| 2 | **Les JOURS d'ouverture** — il a donné les heures le 25/09 (« Ouverture 8h00 / Fermeture 17h30 · CONSULTATION 8H30-13H30 »), **pas les jours** | Ils sont écrits sur la page depuis la v2.2 ; il ne manque que « lundi au samedi ? fermé le dimanche ? » — la page n'affirme **aucun** jour tant qu'on ne l'a pas | **heures ✓ · jours à demander** |
| 3 | **Trois ou quatre photos du cabinet** (téléphone, lumière du jour) | Elles remplacent les photos d'illustration de la page | à confirmer |
| 4 | **Six à huit photos de vos montures et de vos lunettes** — par famille : vue, soleil, enfants (posées, ou la vitrine du magasin) | C'est la **vitrine** de la page : aujourd'hui elle montre trois illustrations. Les vraies montures du cabinet prennent leur place, et le patient voit ce que vous vendez **avant** de venir | à demander |
| 5 | **Moyens de paiement** acceptés (espèces, MTN MoMo, Orange Money) | Évite au patient de venir sans pouvoir payer | à confirmer |
| 6 | **Assurances / mutuelles** prises en charge | Décide le patient assuré, et distingue le cabinet de ses voisins | à confirmer |
| 7 | **Marques de montures** que vous vendez | La page ne nomme aujourd'hui **aucune marque** (on n'en invente aucune). Avec votre liste, on peut écrire « nous portons… » ; sans elle, la vitrine renvoie la question au WhatsApp | à confirmer |
| 8 | **La liste des services** : confirmer ou retirer, parmi les six de la page (examen de la vue · verres sur ordonnance · montures · lunettes de soleil · réparation et entretien · lentilles de contact) | Aujourd'hui la page liste les six services **types** d'un cabinet d'optique. Un cabinet ne fait pas tout : ce qu'on retire disparaît, ce qu'on ajoute s'écrit | à valider |
| 9 | *(facultatif)* **Une phrase de vous**, vos mots, sur ce que vous dites à vos patients | La page n'a **aucun avis** (on n'en invente pas) ; une vraie phrase, signée de votre nom, vaut mieux que dix citations inventées | à demander |

## Ce qu'on fait dès qu'on reçoit

1. `python3 demos/build_dmoptic.py --url https://dmoptic.vercel.app` (les faits entrent dans le gabarit,
   l'adresse reste la même) ;
2. **un seul redéploiement** du dossier `hosting/previews/dmoptic/` chez lui ;
3. on lui renvoie la page, et on lui demande de la relire **sur son téléphone**, pas sur un ordinateur.

## Ce qu'on ne fera jamais, même s'il le demande

- Écrire une adresse, un horaire, un prix, une marque ou une assurance **non confirmés** (une page de
  santé qui invente une adresse coûte un patient, puis la confiance) ;
- Reprendre un **avis** ou un **témoignage** trouvé ailleurs, ou en fabriquer un ;
- Promettre un **classement** sur Google ou un nombre de patients ;
- Mettre en ligne la page sur un domaine **à nous** : le jour venu, le domaine est à son nom.
