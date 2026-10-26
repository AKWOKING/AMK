# Brainstorm — faire indexer le site DM OPTIQUE (26/10/2026)

```text
ÉTAPE 0   graphe rejoué 26/10 19 h 21 (13 541 nœuds) · carte lue §0/§6/§2/§3/§1/§3 bis
ENTRÉE    clients/dm-optic/seo/DIAGNOSTIC-INDEXATION-2026-10-26.md (les preuves, datées)
MÉTHODE   trois approches à part, chiffrées, puis une recommandation et sa condition de fausseté
ÉTAT      proposition — rien n'est publié tant que King n'a pas tranché
```

## 1 · Le problème, en une ligne

Google refuse **8 pages** (403) et ignore **89 pages** qu'il connaît. Le premier défaut est au bord du
réseau ; le second est dans la structure du site : **96 URL demandées, 16 qui ont du contenu**.

## 2 · Trois approches

### A · « Débloquer et attendre » — l'infra seule

On répare le 403 côté Cloudflare (WAF / Bot Fight / Access / redirections), on ne touche pas au site.

- **Coût** : 10 à 20 minutes de King dans son tableau de bord, 0 ligne de code.
- **Résultat attendu** : les 8 pages redeviennent accessibles. Les **89 « Discovered » restent** — ce
  sont deux problèmes différents (diagnostic §3.3).
- **Ce que ça donne dans 3 semaines** : peut-être 8 à 12 pages indexées sur 106, toujours **0** trafic
  utile pour un opticien de Bonabéri qui n'est pas encore connu de Google.
- **Où ça casse** : on règle la serrure et on laisse la pièce vide. La prochaine alerte Search Console
  sera la même, avec un autre mot.
- **Verdict** : nécessaire, **pas suffisant**. C'est l'étape 1 de B, jamais B tout entier.

### B · « Réduire la surface, puis débloquer » — **recommandée**

On décide **quelles pages méritent l'index**, on le dit à Google explicitement, et on répare le 403 en
parallèle.

1. **80 fiches montures (40 FR + 40 EN) passent en `noindex,follow`.** Elles restent en ligne, elles
   restent liées depuis les galeries, elles restent le lien qu'on envoie sur WhatsApp — elles cessent
   seulement de **demander** une place dans l'index. Un titre, une phrase, trois photos : ce n'est pas
   une page que Google doive indexer, et il l'a déjà dit à sa manière (0 fiche indexée sur 40).
2. **Le sitemap passe de 96 à 16 URL** (8 FR + 8 EN) : accueil, hub montures, 3 catégories, examen de
   vue, cabinet, contact, et leurs miroirs anglais.
3. **Le 403 se répare** côté Cloudflare, avec la liste des 8 URL (approche A).
4. **Une porte empêche le retour en arrière** : un contrôle vérifie que le sitemap fait 16 URL, que les
   80 fiches sont en noindex et qu'aucune page cœur ne l'est. Il tourne avant chaque publication.

- **Coût** : 2 heures de build et de contrôle, 10 minutes de King pour le 403.
- **Résultat attendu** : Google ne se voit plus demander 96 URL mais **16**, toutes riches. Le
  « Discovered » cesse de grossir, et les 16 ont une chance réelle d'être visitées et indexées.
- **Ce qu'on perd** : la longue traîne « monture ovale dorée Douala » — qui n'existe pas aujourd'hui
  (0 fiche indexée, 0 impression). On la récupérera quand une fiche aura de quoi se défendre.
- **Ce qu'on ne perd pas** : aucun lien envoyé à un client ne casse. Les fiches répondent toujours.
- **Réversible en une ligne** : la fabrique porte un interrupteur (`INDEX_FICHES`), le retour à 96 URL
  est un `True` et une reconstruction.
- **Où ça casse** : si les 4 pages indexées aujourd'hui sont justement des fiches (on le saura avec la
  liste des URL indexées), on aurait retiré du champ ce qui marchait — à vérifier **avant** de publier.

### C · « Enrichir les 80 fiches » — garder 96 URL et les mériter

On donne à chaque monture un vrai contenu : matière, dimensions, marque, disponibilité, prix, guide de
choix par forme de visage. 80 pages substantielles, un parangon par forme.

- **Coût** : 80 pages × 250 mots, plus des données que **personne n'a** aujourd'hui : la fiche
  `frames.json` ne contient que code, nom, catégorie, forme, couleur, phrase, photos. Matière,
  dimensions, marque et prix **n'ont jamais été fournis** par le cabinet.
- **Ce que la règle interdit** : inventer une matière ou des dimensions (rien d'inventé, jamais). On
  pourrait écrire 150 mots de guide de choix par monture — mais 80 pages au même gabarit, sur un
  domaine sans autorité, c'est exactement le profil que Google classe « contenu de faible valeur ».
- **Résultat attendu** : incertain, et lent (3 à 6 mois).
- **Verdict** : à rouvrir **quand le cabinet donnera les données** et quand les 16 pages seront
  indexées. Pas maintenant, et pas sur 80 pages d'un coup.

## 3 · Comparaison

| | A · débloquer | **B · réduire + débloquer** | C · enrichir les 80 |
|---|---|---|---|
| Temps de King | 10 min | **10 min** | 1 à 2 h (fournir les données) |
| Lignes de code | 0 | **~120 (script + porte + interrupteur)** | ~2 000 (80 pages) |
| URL demandées à Google | 96 | **16** | 96 |
| Pages indexables aujourd'hui | 96 | **16** | 96 |
| Trafic attendu à 3 semaines | ~0 | **> 0, mesurable** | ~0 |
| Risque de contenu inventé | nul | **nul** | **élevé** si les données manquent |
| Réversible | — | **oui, un booléen** | — |

## 4 · Recommandation

**B, avec le point de contrôle suivant avant publication :** vérifier que les **4 pages déjà indexées**
ne sont pas des fiches. Si l'une d'elles en est une, on la garde indexable (liste blanche nominative) —
on ne retire jamais du champ ce que Google a déjà accepté.

**Ce qui rendrait B fausse :** si Search Console montre que les 8 pages en 403 sont les 8 pages cœur
(accueil, hub, catégories, examen, cabinet, contact). Dans ce cas, le vrai problème est un blocage
d'hôte entier, et B ne sert à rien tant que le 403 n'est pas levé — ce qui ne change pas l'ordre des
gestes, seulement l'urgence.

## 5 · Le plan d'exécution

| # | Geste | Qui | Preuve d'acceptation |
|---|---|---|---|
| 1 | Extraire les 8 URL en 403 et les 2 en redirect error | **King** (3 min, clic) | une capture ou un CSV collé dans `clients/dm-optic/seo/` |
| 2 | Passer les 80 fiches en `noindex,follow`, sitemap à 16 URL | moi | `dm_index_surface.py --check` : 16 URL, 80 noindex, 0 page cœur noindex |
| 3 | Contrôler ce que Google a déjà indexé (les 4) | **King** (1 min) | liste des 4 URL indexées |
| 4 | Réparer le 403 (WAF / Access / Redirect Rules) | **King** | Security → Events ne montre plus de 403 pour Googlebot |
| 5 | Demander une réindexation du sitemap | **King** (1 clic) | Search Console → Sitemaps → « 16 découvertes » |
| 6 | Mesurer à J+21 | moi | `Indexed ≥ 12/16` et `impressions > 0` |

**Ce que ce plan ne fait pas** : il ne promet pas la première place, il ne supprime aucune page, il ne
touche ni au design ni aux textes du cabinet, et il ne remplace pas le canal WhatsApp qui amène déjà
les clients.
