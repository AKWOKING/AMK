# Relevé du 29/10 : ce que les deux écrans disent vraiment

```text
PREUVE      search-console-sitemaps-2026-10-29.png · fiche-google-2026-10-29.png (ce dossier)
SOURCE      captures de King, 29/10, Search Console et résultat de recherche « DM OPTIQUE SARL »
MÉTHODE     on lit ce qui est écrit, on ne complète pas de mémoire. Ce qui n'est pas sur la capture
            reste marqué inconnu.
```

## 1 · Search Console : le sitemap est soumis, et il y en a un de trop

| Sitemap | Soumis le | Dernière lecture | Statut | Pages | Verdict |
|---|---|---|---|---|---|
| `https://dmoptiquesarl.com/sitemap.xml` | 26 oct. | **29 oct.** | Success | **22** | ✅ **c'est celui qu'on garde** |
| `https://www.dmoptiquesarl.com/sitemap.xml` | 21 oct. | 28 oct. | Success | 22 | ⚠️ doublon, à retirer |

**B2 est fait** : le sitemap est soumis dans la propriété **Domaine** (les deux hôtes apparaissent dans
le même panneau, ce qui ne peut arriver que là), il est lu, et il rend exactement les 22 URL du site.
Le compte est juste : 22 URL indexables, 80 fiches montures en `noindex,follow` qui n'ont rien à y faire.

### Pourquoi retirer le doublon www

Le www **redirige déjà vers l'apex en 301**. Vérifié en ligne le 29/10, pas supposé : une requête sur
`https://www.dmoptiquesarl.com/contact/` rend la page de `https://dmoptiquesarl.com/contact/`. La ligne
www du tableau est donc un **reste du 21/10**, quand les deux hôtes servaient encore le site.

Ce que ça coûte de la garder : deux déclarations pour 22 mêmes URL, un rapport qui compte double, et un
jour où quelqu'un lira « 44 pages découvertes » en croyant à un site deux fois plus gros. Ce que ça
coûte de la retirer : rien, **retirer un sitemap ne retire aucune URL de l'index**.

**Le geste** : les trois points verticaux au bout de la ligne www → **Remove sitemap**. Une ligne reste,
celle de l'apex.

> **À ne pas faire** : re-soumettre l'apex tous les jours. Google relit tout seul (il l'a fait le 29/10),
> et les demandes manuelles sont limitées.

## 2 · La fiche : trois cases passent au vert

| # | Point | Ce que l'écran montre | État |
|---|---|---|---|
| C1 | Fiche revendiquée | « **You manage this Business Profile** » + « Profile strength : Complete info » | ✅ **fait** |
| C2 | Nom | « DM OPTIQUE SARL » | ✅ |
| C3 | Adresse | « Ndobo Mayor, Immeuble West Hotel, 1er étage, dernière porte à droite, Bonabéri, Douala » | ✅ **mot pour mot identique au site** |
| C4 | Téléphone | « 6 56 12 22 39 » = 656 122 239 | ✅ |
| C6 | Catégorie | « **Opticien** in Bonabéri » | ✅ **tranché par l'écran**, voir ci-dessous |
| C8 | Avis | « **4,9 ★ 7 Google reviews** » | ✅ **la vélocité marche**, voir §3 |

### C6 · La question de catégorie est tranchée, et ce n'est pas par nous

Le 23/10, la fiche était sans avis et la catégorie n'était écrite nulle part. Le 29/10, l'écran répond :
la catégorie principale affichée est **« Opticien »**, et Google la rend en français sur une recherche
francophone au Cameroun.

Notre checklist disait de ne pas trancher à la place du client, et de regarder le sélecteur. L'écran a
tranché plus vite : **« Opticien » existe dans le sélecteur camerounais et elle est déjà choisie**. On
la garde. Chercher « Optometrist » serait poursuivre un mot que ce sélecteur ne propose peut-être même
pas, sur une fiche qui fonctionne.

**Ce qui reste ouvert, et c'est un bonus, pas une correction** : si le sélecteur propose une catégorie
secondaire du type optométrie ou examen de la vue, l'ajouter **en secondaire** est cohérent avec le
titre « opticien optométriste ». À regarder une fois, sans y passer la soirée. On ne change pas la
principale.

## 3 · Les avis : +3 en six jours

| Date | Avis | Note |
|---|---|---|
| 23/10 | 4 | 5,0 |
| **29/10** | **7** | **4,9** |

Le passage de 5,0 à 4,9 n'est pas un incident : il y a 7 avis, donc **un avis à 4 étoiles suffit** à
faire bouger la moyenne. C'est exactement ce qu'on veut. Une fiche qui reste à 5,0 sur des mois est une
fiche qui ne reçoit plus rien, ou une fiche qui trie ses clients.

**Ce qu'on ne fait pas** : relancer pour remonter à 5,0, demander une note, ou trier qui on sollicite.
La vélocité sur 90 jours pèse plus que la moyenne, et les guidelines du 24/07/2026 nomment explicitement
les avis incités.

**Ce que la carte du comptoir change** : elle rend le geste possible au bon moment, sans que personne
ait à épeler une adresse. Elle a été livrée le 29/10 (`launch/carte-avis-a6.pdf`), en même temps que le
lien sur `/contact/`.

## 4 · Le seul écart trouvé, et il n'est pas dans le site

La fiche dit « **Open · Closes 5pm** » (17h00). Le site dit « Autres besoins : 8h30 – **17h30** ».
Trente minutes d'écart, sur le seul champ qui fait qu'un patient se déplace pour rien.

| Source | Ce qu'elle dit |
|---|---|
| Site `/contact/` et `/en/contact/` | examen 8h30–13h00 · autres besoins 8h30–**17h30** |
| Fiche Google (capture du 29/10) | fermeture à **17h00** |

**On ne corrige pas au hasard.** Les deux valeurs viennent de nous (les horaires du site ont été repris
du cabinet), mais une seule est vraie. Deux sorties, et c'est le cabinet qui choisit :

1. la fiche avait raison, et le site se corrige en deux minutes (deux fichiers, FR et EN) ;
2. le site avait raison, et King corrige les horaires dans la fiche (Modifier le profil → Horaires).

**Tant que ce n'est pas tranché, on ne touche à rien** : changer le site pour coller à une capture ferait
d'un doute une erreur de plus. Une incohérence d'horaires entre le site et la fiche est le genre de
détail qui coûte un déplacement, et Google le lit comme un signal de fiabilité en moins.

## 5 · Une citation tierce qui ne dit pas le même nom

Sous la fiche, une annonce **Yandex** affiche « Cabinet De Soins Oculaires **DM Optometrie** », Littoral,
Wouri, Douala 4e, Rue 4.070. Ce n'est pas notre fiche : c'est un annuaire tiers qui a construit sa page
à partir de données publiques, avec un nom qui n'est pas le nôtre.

**Ce qu'on en fait : rien, pour l'instant.** On ne peut pas éditer Yandex sans y créer un compte, ça
n'apporte aucun patient au Cameroun, et le nom canonique de la fiche et du site est cohérent partout
ailleurs (site, fiche, Facebook « DM Optique SARL | Douala »). À surveiller si un jour quelqu'un tombe
dessus et doute. **À ne pas faire** : créer un compte sur chaque annuaire pour aller corriger un nom,
on ouvrirait un chantier sans fin pour zéro trafic.

## 6 · Où on en est, et ce qui reste

| # | Geste | Qui | Quand |
|---|---|---|---|
| 1 | Retirer le sitemap www en double (3 points → Remove sitemap) | **King** | 2 minutes |
| 2 | Trancher les horaires : 17h00 ou 17h30 ? | **King + cabinet** | avant le 05/11 |
| 3 | Regarder si le sélecteur propose une catégorie secondaire d'optométrie | **King** | à l'occasion |
| 4 | Coller la capture « Pages » de Search Console (indexation) | **King** | **05/11**, cible interne |
| 5 | Carte du comptoir imprimée et posée | **King** | cette semaine |

**Ce que le 29/10 ne prouve pas** : que le site soit indexé. Le sitemap est lu, 22 URL sont découvertes,
ce n'est pas la même chose que 22 URL dans l'index. Le seul chiffre qui le dit est le rapport « Pages »
de Search Console, et il date du 23/10 (4 pages indexées sur 106 URL connues). Prochaine mesure : 05/11.
