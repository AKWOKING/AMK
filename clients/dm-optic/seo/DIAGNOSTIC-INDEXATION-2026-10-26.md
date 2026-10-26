# DM OPTIQUE — pourquoi 102 pages ne sont pas indexées (diagnostic du 26/10/2026)

```text
ÉTAPE 0   graphe rejoué 26/10 19 h 21 (13 541 nœuds) · carte lue §0/§6/§2/§3/§1/§3 bis
PRE-FLIGHT  §00, §0, §0b, §0c, §0c bis, §1b (porte technique) · knowledge : MAINTENANCE-CLIENTS
          (décision qui engage un client) · dossier client : CLIENT-REQUIREMENTS-BRIEF (source de
          vérité), DEPLOIEMENT-CLOUDFLARE-2026-10-22, site/SEO-AUDIT-2026-10-23
MÉTHODE   les chiffres de Google d'abord (export fourni), puis nos propres relevés datés, puis les
          hypothèses classées par ce qui les confirmerait. Ce qui n'a pas été mesuré est écrit
          « non mesuré » — jamais estimé.
LIMITE    cet environnement n'ouvre pas de socket vers dmoptiquesarl.com (`curl` : SSL refusé). Les
          pages ont été lues par le proxy de lecture (`fetch_page`), pas par une requête HTTP à nous :
          un code 200 vu par un proxy n'est pas une preuve de ce que Googlebot reçoit.
```

## 1 · Ce que Google dit, au mot près

Export Search Console du **23/10/2026** (`Chart.csv`, `Critical issues.csv`, `Metadata.csv`) :

| Raison | Source | Pages | Ce que ça veut dire |
|---|---|---|---|
| **Blocked due to access forbidden (403)** | **Website** | **8** | le serveur a répondu **403** à Googlebot — ce n'est pas un problème de contenu |
| **Redirect error** | **Website** | **2** | une URL demandée boucle, ou sa chaîne de redirection est invalide |
| Discovered – currently not indexed | Google systems | **89** | Google **connaît** l'URL (sitemap, lien) et n'a pas encore jugé utile de la visiter |
| Crawled – currently not indexed | Google systems | **3** | Google est venu, a lu, et a décidé de ne pas indexer |

Total **102 non indexées / 4 indexées**. Impressions : 0 (19/10), 11 (20/10), 2 (21/10), 1 (22/10),
2 (23/10). **Le site n'a pas de trafic de recherche, et ne peut pas en avoir tant que 102 de ses
106 URL ne sont pas dans l'index.**

Deux e-mails de Search Console, reçus le **26/10 à 12 h 02 et 12 h 03**, annoncent une **raison
nouvelle** : `Blocked due to access forbidden (403)` — puis, onze secondes plus tard, la même raison
**plus** `Redirect error`. Le 403 n'est donc pas ancien : il est apparu entre le 23/10 (photo de
l'export) et le 26/10.

## 2 · Ce que le dépôt et le site disent, mesuré aujourd'hui

| Vérification | Résultat | Où / comment |
|---|---|---|
| `robots.txt` en ligne | `Allow: /` + sitemap déclaré | `fetch_page` 26/10 |
| `sitemap.xml` en ligne | **96 URL** (48 FR + 48 EN), `lastmod` 2026-10-21 partout | `fetch_page` 26/10 |
| Accueil en ligne | servi, contenu complet (FR + EN) | `fetch_page` 26/10 |
| Une fiche monture en ligne | `/montures/femmes/f01-ovale-doree/` servi | `fetch_page` 26/10 |
| `www.dmoptiquesarl.com` | **redirige vers l'apex** `dmoptiquesarl.com` | `fetch_page` 26/10 (URL finale) |
| Sitemap vs disque | **96 URL, 96 fichiers, 0 manquant** | script de recoupement 26/10 |
| Liens internes | **0 cassé** sur les 97 pages | script de recoupement 26/10 |
| Titres dupliqués | **0** | `audit_seo.py` 26/10 |
| `canonical` | apex, partout, 0 anomalie | `audit_seo.py` 26/10 |
| `hreflang` | **48 paires FR/EN réciproques, 0 problème** | `audit_seo.py` 26/10 |
| Référence à `www.` dans le site publié | **0 fichier** | `grep` 26/10 |
| Porte de livraison | **0 P1 · 0 P2 · 1 P3** (images d'aperçu partagées) | `audit_delivery.py --strict` 26/10 |

**Conclusion de cette section : le problème n'est pas dans le HTML.** Un site dont les canonical, les
hreflang, les titres, les liens et le sitemap sont propres ne produit pas un 403 par son contenu. Le
403 est rendu **au bord du réseau**, avant le fichier.

## 3 · Les trois causes, classées, avec ce qui les confirmerait

### 3.1 · Le 403 (8 pages) — cause au bord, pas dans le fichier

Ce qui peut répondre 403 à Googlebot sur un Worker Cloudflare servant des fichiers statiques, par ordre
de fréquence réelle :

| # | Mécanisme | Pourquoi il touche **8** pages et pas 96 | Ce qui le confirmerait |
|---|---|---|---|
| 1 | **WAF / Bot Fight Mode / « Block AI bots »** réglé en *block* | Googlebot est vérifié mais une règle personnalisée (chemin, user-agent, pays) peut ne viser qu'une partie | Cloudflare → **Security → Events** : filtrer sur `bot score` et `403`, regarder l'ASN Google |
| 2 | **Rate limiting** (une règle « plus de N requêtes / minute → block ») | se déclenche en rafale : Google crawle par vagues, 8 pages tombent dans la fenêtre, les autres passent | Security → Events, même filtre ; la règle apparaît nommée |
| 3 | **Cloudflare Access** posé sur un chemin | seul le chemin protégé répond 403, le reste est ouvert | Zero Trust → Access → Applications : une application couvre-t-elle `dmoptiquesarl.com/...` ? |
| 4 | **Redirect Rule www → apex mal formée** | une redirection vers un hôte qui re-renvoie peut rendre 403 pour les URL profondes | Rules → Redirect Rules : la règle utilise-t-elle `concat()` et un `$1` correct ? |
| 5 | Règle de sécurité de zone (« I'm under attack ») | toucherait **tout**, donc improbable ici | Security → Settings → Security Level |

**Ce qu'il faut pour trancher, et que je n'ai pas :** la **liste des 8 URL**. Elle est dans Search
Console, derrière un clic : *Indexing → Pages → « Blocked due to access forbidden (403) » → Exporter*.
Sans elle, on répare à l'aveugle — et une règle WAF élargie « pour être sûr » ouvrirait le site à tout.

### 3.2 · Le Redirect error (2 pages) — deux candidates, une seule vérifiable ici

- **Candidate A — la propriété Search Console est `https://www.dmoptiquesarl.com/`** (c'est l'objet des
  e-mails) alors que le site canonise l'apex et que `www` renvoie 301 vers l'apex. Une URL `www`
  demandée par Google subit une redirection vers un hôte **qui n'est pas celui de la propriété**.
  Deux URL dans ce cas suffisent à produire « Redirect error ».
- **Candidate B — les URL sans barre finale.** Le site sert `/montures/femmes/f01-ovale-doree/` ;
  la variante sans `/` final redirige (comportement normal des assets Workers). Si une des deux URL
  est une variante sans barre, elle apparaît en « Page with redirect », pas en erreur — donc B est
  moins probable que A.

**Ce qui départage :** les 2 URL, et le choix de propriété (apex ou `www`) dans Search Console.

### 3.3 · Les 89 « Discovered » — la vraie cause de fond, et elle est dans la structure

Le site demande à Google d'indexer **96 URL**, dont **80 fiches de montures** (40 FR + 40 EN) qui sont
**quasi identiques** : un titre, une phrase, trois photos, quatre lignes de faits. Les 16 pages qui ont
du contenu réel (accueil, hub, 3 catégories, examen, cabinet, contact, + miroir EN) totalisent
l'essentiel du texte du site.

Sur un domaine de **trois semaines**, sans un seul lien externe, Google répartit un budget de crawl
minuscule. Il a donc : indexé 4 pages, **découvert** 89 URL sans venir, **visité** 3 sans indexer.
Ce n'est pas une erreur à corriger, c'est un **arbitrage de Google** : 80 pages trop proches les unes
des autres ne méritent pas 80 visites.

**Conséquence directe :** tant que le site demandera 96 URL, le rapport restera rouge, même une fois
le 403 réparé. Le 403 et le « Discovered » sont deux problèmes distincts ; les confondre ferait
attendre du premier qu'il règle le second.

## 4 · Un quatrième défaut, trouvé en chemin, et qui n'était pas dans la commande

Le générateur du site n'est **plus reproductible** : rejoué aujourd'hui, il réécrit **99 fichiers**,
parce que le gabarit de l'accueil a changé le **24/10** (dégradé du premier écran, anneau de verre
revenu à la demande du client) et que les 47 autres pages portent encore le CSS du 21/10.

Ce n'est pas la cause du 403, et ce n'est pas dans la commande. C'est noté ici parce que **reconstruire
le site pour corriger l'indexation appliquerait un changement de design non demandé** : les correctifs
d'indexation de ce tour ne passent donc **pas** par une reconstruction complète.

## 5 · Ce que ça coûte, en clair

| Si on ne fait rien | Aujourd'hui | Dans 3 semaines |
|---|---|---|
| Pages indexées | 4 / 106 | 4 / 106 (le 403 n'est pas auto-réparateur) |
| Trafic de recherche | ~0 (11 impressions au meilleur jour) | ~0 |
| Contacts WhatsApp venus de Google | 0 mesurable | 0 mesurable |

Le site a un autre canal qui marche déjà : le lien envoyé à la main sur WhatsApp. L'indexation ne
remplace pas ce canal, elle en ajoute un — mais seulement quand les 16 pages qui comptent sont dans
l'index.

## 6 · Ce qui a été corrigé le 26/10, et ce qui reste à faire

| # | Correctif | Où | État |
|---|---|---|---|
| 1 | **80 fiches de montures en `noindex,follow`** — elles restent en ligne, liées depuis les galeries, et restent le lien qu'on envoie sur WhatsApp | `tools/ops/dm_index_surface.py --apply` | ✅ appliqué |
| 2 | **Sitemap ramené de 96 à 16 URL** (8 FR + 8 EN) | `hosting/previews/dmoptic/sitemap.xml` | ✅ appliqué |
| 3 | **La même politique dans la fabrique** (`INDEX_FICHES`, liste blanche) pour qu'une reconstruction ne défasse pas le correctif | `demos/build_dmoptic_montures.py` | ✅ testé (build rejoué : 16 URL, 40 fiches noindex, miroir EN hérité) |
| 4 | **Une porte qui empêche le retour en arrière** : `D9 · sitemap ↔ noindex` (P1 si le sitemap demande l'index d'une page qui le refuse, P2 si une URL du sitemap n'a pas de fichier) | `tools/qa/audit_delivery.py` + `test_audit_delivery.py` (18 assertions) | ✅ dans la CI (l'étape de porte du déploiement) |
| 5 | **Le 403** (8 pages) et le **Redirect error** (2 pages) | Cloudflare + Search Console | ⏳ **King** — `RUNBOOK-403-2026-10-26.md` |
| 6 | **Dérive de gabarit** : 99 fichiers diffèrent si on rejoue le générateur (CSS du 24/10 non répercuté) | `demos/build_dmoptic_montures.py` | ⏳ à trancher — **non fait ici**, parce qu'une reconstruction appliquerait un changement de design au client |

**Contrôles après correctif** — `audit_delivery.py --strict` : 0 P1 · 0 P2 · 1 P3 (images d'aperçu
partagées, inchangé) · `audit_seo.py` : 97 pages, 0 problème, 48 paires hreflang, sitemap 16 ·
`audit_aeo.py` : aucune faute · `gate-dm.sh` : PORTE OK · `dm_index_surface.py --check` : OK.

**Ce que ce correctif ne fait pas** : il ne rend pas le site visible à lui seul. Il retire ce que
Google refusait (80 pages sans contenu) et répare ce qui le bloquait (16 URL demandées, 403 côté
Cloudflare). La visibilité, elle, dépend de l'autorité du domaine — fiche Google Business Profile
reliée au site, inscription ONOC, page Facebook du cabinet.
