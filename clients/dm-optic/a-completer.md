# DM OPTIC — ce qu'il reste à nous envoyer

**Document de travail. Il part dans la conversation WhatsApp — il n'est plus sur la page.**
Depuis la v2.1 (24/09 au soir), la page parle **au patient** : six services listés, une vitrine de
montures, et plus aucun détail administratif du titulaire. La liste de ce qui manque vit donc ici.

| # | Ce qu'on attend de M. Domche | Ce que ça change sur la page | État |
|---|---|---|---|
| 1 | **Adresse exacte** + le point de repère (« en face de… », « à côté de… ») | La question n° 1 d'un patient ; c'est aussi ce qui alimente un bouton d'itinéraire | à confirmer |
| 2 | **Horaires** : jours et heures d'ouverture | La question n° 2 ; une des **six** questions fréquentes attend cette réponse | à confirmer |
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
