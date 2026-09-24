# LA LIGNE OPTIC — ce qu'il reste à nous envoyer

**Document de travail. Il part dans la conversation WhatsApp — il n'est pas sur la page.**
La page est construite et lisible telle quelle : elle dit au patient ce que le cabinet fait, comment ça
se passe, et ce qui ne peut se décider que dans la conversation. Tout ce qui suit la rendrait
**entièrement vraie** — et fera tomber les questions qui reviennent.

| # | Ce qu'on attend du cabinet | Ce que ça change sur la page | État |
|---|---|---|---|
| 1 | **Les horaires** (jours, heures, et ce qui change les jours fériés) | Aujourd'hui la page dit seulement « les horaires du jour vous sont confirmés dans la conversation ». Avec eux, on écrit une ligne claire — et on la met dans les données structurées | à demander |
| 2 | **Le repère exact, à Akwa** (en face de quoi ? à côté de quoi ? après quel carrefour ?) | La page donne le boulevard de la Liberté. Un repère comme ceux des autres cabinets ferait gagner du temps au patient — et il part déjà sur WhatsApp | à demander |
| 3 | **Les moyens de paiement** (espèces, MTN MoMo, Orange Money) | Évite qu'un patient arrive sans pouvoir payer | à confirmer |
| 4 | **Six à dix photos de montures** (vue, solaires) et **deux ou trois du cabinet** | Elles prendraient la place qu'on a laissée vide : la page est **entièrement dessinée** aujourd'hui, par choix — parce qu'aucune photo n'existe. Avec les vôtres, la vitrine devient réelle | à demander |
| 5 | **Les marques que vous vendez**, et si vous voulez qu'elles soient nommées | Aujourd'hui aucune marque n'est écrite, aucune n'a été inventée | à confirmer |
| 6 | **Les prix** : voulez-vous afficher des repères (« à partir de… ») ? | Aujourd'hui la page répond « le prix dépend de vos verres et de votre monture », et renvoie au WhatsApp. Vous restez libres — mais dites-le-nous | à décider |
| 7 | **Le délai habituel** pour une paire (et ce qui se commande) | La page n'annonce aucun délai : « le cabinet vous le confirme ». Une phrase suffirait | à préciser |
| 8 | **Les verres et options proposés** (progressifs, anti-reflet, photochromiques…) | Renforce la partie « conseil », qui est l'un de vos quatre services | à préciser |
| 9 | **Ce qui est réparé sur place** (vis, plaquettes, ajustement, soudure ?) | La page pose la question au patient et promet une réponse — pas une réparation | à préciser |
| 10 | **Une seconde ligne téléphonique**, s'il y en a une | Un seul numéro est publié aujourd'hui : le 683 651 108 | à confirmer |
| 11 | **Une adresse e-mail**, si vous en avez une | Aucune n'apparaît aujourd'hui | à confirmer |
| 12 | **Le nom exact que vous voulez voir** (enseigne, raison sociale complète, « Mme Joungo ») | La page écrit aujourd'hui « La Ligne Optic » et nomme Mme Joungo Line Chantale, opticienne, avec son inscription à l'Ordre (2017) | à confirmer |

## Ce qu'on fait dès qu'on reçoit

1. `python3 demos/build_laligne.py --url https://<votre adresse>` (les faits entrent dans la page) ;
2. **un seul redéploiement** ;
3. on vous renvoie la page, et on vous demande de la relire **sur votre téléphone**, pas sur un
   ordinateur.

## Ce qu'on ne fera jamais, même si on nous le demande

- Écrire un horaire, un prix, une marque, une adresse ou un avis **non confirmés** ;
- Reprendre un avis client trouvé ailleurs, ou en fabriquer un ;
- Promettre un classement sur Google, un délai ou un nombre de patients ;
- Publier une photo de personne (patient, personnel) sans son accord écrit ;
- Attribuer au cabinet un acte médical : l'examen des yeux reste celui de l'ophtalmologue, et la page
  l'écrit déjà ;
- Mettre la page sur un domaine **à nous** : le jour venu, le domaine est au nom du cabinet.
