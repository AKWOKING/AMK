# DM OPTIC — ce qu'il reste à nous envoyer

**Document de travail. Il part dans la conversation WhatsApp — il n'est plus sur la page.**
Depuis la v2 (24/09 au soir), la page parle **au patient** : elle ne contient plus aucune section
adressée au cabinet. La liste de ce qui manque vit donc ici.

| # | Ce qu'on attend de M. Domche | Ce que ça change sur la page | État |
|---|---|---|---|
| 1 | **Adresse exacte** + le point de repère (« en face de… », « à côté de… ») | La question n° 1 d'un patient ; c'est aussi ce qui alimente un bouton d'itinéraire | à confirmer |
| 2 | **Horaires** : jours et heures d'ouverture | La question n° 2 ; une des cinq questions fréquentes de la page attend cette réponse | à confirmer |
| 3 | **Trois ou quatre photos du cabinet** (téléphone, lumière du jour) | Elles remplacent les deux images d'illustration légendées « mise en situation » | à confirmer |
| 4 | **Moyens de paiement** acceptés (espèces, MTN MoMo, Orange Money) | Évite au patient de venir sans pouvoir payer | à confirmer |
| 5 | **Assurances / mutuelles** prises en charge | Décide le patient assuré, et distingue le cabinet de ses voisins | à confirmer |
| 6 | **Marques de montures** qu'il aime vendre | Donne de la matière à la bande des actes | à confirmer |
| 7 | **La liste des actes** : confirmer ou retirer, parmi les six de la page (examen de la vue · verres sur ordonnance · montures · lunettes de soleil · réparation et entretien · lentilles de contact) | Aujourd'hui la page liste les six actes **types** d'un cabinet d'optique. Un cabinet ne fait pas tout : ce qu'il retire disparaît, ce qu'il ajoute s'écrit | à valider |
| 8 | *(facultatif)* **Une phrase de lui**, ses mots à lui, sur ce qu'il dit à ses patients | La page n'a **aucun avis** (on n'en invente pas) ; une vraie phrase, signée de son nom, vaut mieux que dix citations inventées | à demander |

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
