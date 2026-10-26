# Dr Ophtalmo — notes de construction

**26/10/2026** · aperçu `hosting/previews/dr-ophtalmo/` · aucun client payant, rien n'est publié.

## 1 · La décision qui commande tout le reste : l'honnêteté est un composant

Le brief demande à la fois « premium, rassurant, crédible » et « ne rien inventer ». Ces deux exigences se
contredisent dès la deuxième ligne d'une page de médecin : un site de soin vide fait peur. La solution
retenue est un **système d'état visible**, pas une absence :

| État | Rendu | Exemple |
|---|---|---|
| `confirmed` | pastille pleine + mot « Confirmé » | aucun pour l'instant |
| `reported` | pastille atténuée + mot « Communiqué » | les quatre lieux, la spécialité |
| `unknown` | pastille en pointillé + mot « À confirmer » | horaires, adresses exactes, contact |

Trois conséquences heureuses : ① le premier client qui remplit la configuration voit les états changer de
couleur sans qu'on retouche une ligne de CSS ; ② le médecin comprend en regardant sa page ce qu'il lui
reste à envoyer — le site est aussi sa liste de courses (bouton « Informations à publier » dans le pied) ;
③ le doute du visiteur est traité là où il naît, au lieu d'être noyé dans une mention légale.

## 2 · Ce qui n'a pas été fait, volontairement

- **Pas de nom dans le hero.** Le H1 est celui du brief (« VOTRE VISION, MA PRIORITÉ. ») : il tient sans
  nom, donc le jour où le nom arrive il n'y a rien à remanier. Dans le parcours, « Dr [NOM DU MÉDECIN] »
  est affiché entre crochets — c'est laid exprès : un crochet ne se confond pas avec un vrai nom.
- **Pas de cinquième lieu, pas de « et aussi… ».** Quatre lieux, numérotés 01–04. Hôpital Charity n'a
  aucun jour : il affiche « à confirmer » plutôt que de deviner dimanche.
- **Pas de carte dessinée pour Bonabéri.** « Grand Hangar, Bloc 7 » est une information de repère, pas une
  coordonnée ; un plan inventé serait pire qu'aucun plan.
- **Pas de lien de carte** tant qu'aucune destination vérifiée n'existe : le bouton « Ouvrir l'itinéraire »
  n'apparaît que si `mapUrl` est rempli, et la configuration refuse d'avoir un lien sans adresse (test).
- **Pas de prix, pas d'avis, pas de compteur.** Un site de soin n'a rien à vendre dans le premier écran.

## 3 · Décisions techniques

1. **Une seule source de vérité** (`js/config/doctor.js`), et la semaine en est *déduite* (`lib/schedule.js`).
   Ajouter un jour ne touche ni le HTML, ni le CSS, ni le sélecteur, ni le formulaire.
2. **Aucun texte dans le HTML.** Tout passe par `data-i18n` et deux dictionnaires ; un test vérifie que
   FR et EN ont exactement les mêmes clefs, donc une traduction ne peut pas « oublier » un paragraphe.
3. **Le formulaire ne parle à personne.** Pas de `fetch`, pas de backend, pas de cookie. Il compose un
   message, l'affiche, et laisse partir WhatsApp si — et seulement si — un numéro vérifié est configuré.
   Tant qu'il ne l'est pas, le message est copiable et le site explique pourquoi il n'y a pas de bouton.
4. **Le message WhatsApp ne contient que les champs du formulaire**, jamais le champ libre : c'est testé.
   Une demande de rendez-vous n'est pas un dossier médical.
5. **Le repli est un état normal**, pas une erreur : le site est complet sans numéro, sans horaires, sans
   nom — c'est ce qui permet de le montrer aujourd'hui.

## 4 · Images

Trois images générées le 26/10 (`assets/src/*.png`, converties en webp 1440/960/640, ~300 Ko au total) :

1. **Portrait** — une praticienne africaine en blouse, salle de consultation lumineuse. Deux tentatives :
   une première avec un homme en blouse n'allait pas avec la deuxième image, et la deuxième version du
   portrait (femme) ne correspondait pas non plus. La cohérence entre le portrait et la photo d'examen a
   demandé trois générations : la première photo d'examen montrait une praticienne européenne avec un
   patient européen, ce qui aurait juré à côté du portrait. Tout est régénéré pour que ce soit la même
   personne dans les deux images.
2. **Examen** — la même praticienne, patiente assise, lampe à fente.
3. **Équipement** — lampe à fente et fauteuil, sans personne.

**Elles ne sont pas le médecin.** Deux légendes le disent à l'écran ; `isRealPhoto: false` commande la
mention. Le jour où le vrai portrait arrive : remplacer les trois fichiers, l'`alt`, et passer le drapeau.

## 5 · Ce que je n'ai pas pu vérifier

- **Le rendu d'un vrai navigateur.** Aucun Chromium dans l'environnement (bibliothèques NSS absentes, pas
  de réseau vers les dépôts système). J'ai vérifié la structure et le comportement dans un DOM simulé
  (46 assertions) et relu le CSS point de rupture par point de rupture ; **je n'ai pas vu la page**.
  C'est la raison pour laquelle elle est ouverte en aperçu : le contrôle visuel est à faire, pas à croire.
- **Les contrastes mesurés.** Les couples employés sont choisis pour tenir (texte `#f7fafc` sur `#07111d`,
  `#142536` sur `#f6f8fa`, `#76b9b4` sur `#07111d` en accent), mais aucun outil de mesure n'a tourné ici.
- **La taille du texte dans les captures.** Non mesurable sans navigateur.

## 6 · La leçon à garder

*Un site de médecin ne se juge pas à ce qu'il affirme, mais à la manière dont il traite ce qu'il ne sait
pas encore.* Ici, l'inconnu est un état graphique : « Communiqué » / « À confirmer », une phrase qui le dit,
et un bouton qui montre au médecin ce qu'il reste à envoyer. La même mécanique servira au prochain dossier
où le client tarde à envoyer ses informations — c'est-à-dire presque tous.
