# Rapport de veille — les opticiens de Bonabéri (prototype, 20/10/2026)

> **Prototype du service « veille concurrentielle mensuelle »** — accepté par King le 20/10
> (« you will have to search and select the 3 opticians yourself »). Périmètre : les opticiens du
> quartier de DM Optique (Bonabéri, Douala), **pages publiques seulement**, sources citées.
> Ce prototype sert à montrer le produit en vente. **Le tarif reste une décision de King.**

## Comment ce rapport a été fait (méthode, honnête)

- **Cibles sélectionnées** le 20/10 par l'orchestrateur (délégation King) : présence physique à
  Bonabéri + présence web publique vérifiable + trois positionnements différents (réputation,
  réseau/abonnement, invisible en ligne).
- **Collecte du jour** : recherche web + lecture des pages publiques (annuaires, page de
  réservation, presse). **Conformité** : aucune page Facebook/Instagram scrapée (ToS), aucun
  contenu derrière login, sources datées ci-dessous.
- **Industrialisation** : la chaîne Scrapling (installée le même jour, `tools/scrapling/`) reprend
  cette collecte en automatique chaque mois — sur la machine de King (internet complet). Le bac de
  l'orchestrateur reste limité en sortie réseau ; ce prototype a été fait avec les outils du jour,
  à la main.

## Les trois cibles de Bonabéri

| | **Valdoz Optic** | **iris — l'Optométriste** | **Bronze Eye Care & Optics** |
|---|---|---|---|
| **Adresse publique** | Entrée forêt Bar (Nouvelle Route / Route Nationale 3), Bonabéri | **Immeuble MTN, 4 étages**, Bonabéri (point de consultation) | ~200 m après le Royal City Night Club, Bonabéri |
| **Téléphone public** | +237 677 61 04 41 | via la page de réservation | non publié sur l'annuaire lu |
| **Horaires publiés** | non trouvés | **lun–ven 8:00–15:00, sam 8:00–13:00** | non trouvés |
| **Présence web** | annuaires + presse (pas de site propre trouvé) | **page de réservation en ligne** (Setmore, 16 points du réseau) | une fiche d'annuaire (4 photos, 0 avis) |
| **Positionnement** | lunetterie depuis ~28 ans, 3 villes (Yaoundé Kennedy, Akwa Foch, Bonabéri) | **réseau + abonnement** (« consultations, examens et rdv gratuits » aux abonnés) | soins visuels généralistes (vue, solaires, lentilles) |
| **Signaux de réputation** | **« Meilleur cabinet d'optique au Cameroun 2024 »** (Innovation Awards, remis le 05/03/2025) | 5.0 (2 avis) sur la page de réservation | 0 avis, aucune preuve de vie récente |
| **Offre visible** | lunettes personnalisées, montage, entretien, examens (« à partir de 5 000 XAF » *selon l'annuaire Ayilaa — chiffre non officiel*) | abonnement (prix non publié), réservation en ligne par point de consultation | examen, adaptation, montures modernes |

### Sources (lues le 20/10/2026)
- Valdoz : ayilaa.com (fiche n° 12667) · innovationafric.net (article du 10/03/2025 sur le prix) · yandex.com/maps + docteur.go.yo.fr (adresses, téléphone).
- iris : cno.setmore.com (page de réservation officielle du réseau — horaires, points, modèle d'abonnement).
- Bronze : ayilaa.com (fiche n° 9485).

## Le voisinage élargi (contexte, autres quartiers — une ligne chacun)

Golden Eyes (Bonapriso) : site propre, examen de vue gratuit en avant, tous les réseaux. Maison
Optique (Bali) : site propre soigné. Free Optic (centre) : campagne « examen gratuit pour les
enfants de 2 à 9 ans » sur sa page publique. Tchaya (Akwa) : depuis 1974, met en avant des marques
internationales. Lumel (Ancien 3ᵉ) : horaires publiés clairement. **Aucun n'est à Bonabéri** — le
quartier de DM n'a pas d'opticien avec un vrai site web.

## Où DM est déjà devant — et ce qu'il faut surveiller (honnête)

**Devant, dès aujourd'hui :** DM a un site complet de 48 pages bilingues avec ses vraies photos,
une fiche Google en ligne, des horaires détaillés par besoin, ses assurances affichées et un
bouton WhatsApp sur chaque monture. Aucun des trois voisins n'affiche tout cela — Bronze et Valdoz
n'ont même pas de site propre trouvé.

**À surveiller :**
1. **Valdoz** : la réputation (prix national 2024, « coûts accessibles » revendiqués dans la
   presse) — c'est l'adversaire de l'image, pas du web. DM répond par les avis Google : demander
   poliment les 5 premiers avis clients est l'action la plus rentable du mois.
2. **iris** : l'abonnement et la réservation en ligne sont des idées commerciales fortes (horaires
   étroits, 8:00–15:00). S'en inspirer exige une décision de King — on ne copie pas, on note.
3. **Bronze** : rien à signaler ce mois — c'est le cas d'école du concurrent invisible.

## Ce que le client achète (l'offre mensuelle, à tarifer par King)

Chaque mois, le même rapport en 2 pages : ce qui a changé chez ses concurrents directs (offres
affichées, horaires, nouveautés, avis), ce qui bouge dans le quartier, et les deux ou trois actions
que ça suggère pour le sien. Les données viennent des pages publiques, la chaîne est automatisée
(Scrapling), et rien de faux n'y entre : chaque ligne porte sa source et sa date.

## Limites de ce prototype (dites telles quelles)

- Les annuaires peuvent être vieux — l'annuaire DoualaTour cité dans la recherche date de 2022 et
  a été écarté comme source principale.
- Les offres des concurrents vivent surtout sur Facebook : la veille les voit passer en mention
  (recherche), jamais en scraping — la règle ToS ne bouge pas.
- Prix et abonnements : rien n'est publié proprement chez les trois cibles ; ce rapport ne devine
  pas ce qu'il n'a pas lu.
