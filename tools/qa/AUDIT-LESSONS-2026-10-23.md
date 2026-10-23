# Leçons d'audit — 23/10/2026

> Déclencheur : un audit extérieur de DM Optique (`clients/dm-optic/audits/AUDIT-EXTERNE-2026-10-23.md`,
> Chrome headless à 1366 et 390 px, axe-core WCAG 2 A/AA, comparaison au domaine en ligne) a rendu
> **deux P1** le jour où nos cinq portiques rendaient tous « 0 faute ». Les deux peuvent être vrais :
> ils ne mesuraient pas la même chose. Ce fichier dit **quoi**, **pourquoi on ne l'a pas vu**, et **ce
> qui le mesure maintenant**.

## 1 · Ce que l'audit a trouvé, et ce que nos portiques en disaient

| Constat extérieur | Sév. | Notre portique ce jour-là | Verdict |
|---|---|---|---|
| Aucune navigation sous 980 px : `nav.nav{display:none}`, aucun bouton de menu sur 91 pages | P1 | « 0 faute » — aucun portique ne regarde le CSS responsive | **vrai, et grave** |
| `Cache-Control: public, max-age=0, must-revalidate` sur `.webp` et `.woff2` | P1 | « 0 faute » — aucun portique ne lit `_headers` | **vrai, et grave** |
| Pas de favicon, pas d'`apple-touch-icon` | P2 | « 0 faute » — jamais cherché | **vrai** |
| `https://dmoptiquesarl.com//fichier` dans le JSON-LD (4 occurrences) | P2 | `audit_seo` valide le JSON-LD, pas les URL qu'il contient | **vrai** |
| HSTS absent ; CSP absente | P2/P3 | jamais regardé | **vrai** |
| `og:image` en WebP sur 80 pages | P2 | jamais regardé (WebP = bon format pour la page, douteux pour WhatsApp) | **vrai, à tester** |
| `llms.txt` : 49 URL, aucune anglaise | P2 | `audit_seo` vérifie que le fichier existe, pas qu'il couvre le sitemap | **vrai** |
| Fiches montures sans `Product` | P3 | jamais regardé | **vrai** |
| Em dashes / en dashes (685 / 654) | P3 | hors périmètre | à trancher côté voix DM |
| Double barre, horaires, nom du fondateur | P3 | — | voir §4 |

**Ce que nos portiques disaient vraiment** : `audit_html` (structure et contraste), `audit_a11y`
(critères WCAG), `audit_images` (ratio, poids, GPS), `audit_reveal` (contenu caché par une animation),
`audit_seo` (titre, description, canonical, hreflang, liens, données structurées). Tous mesuraient des
**documents**. Aucun ne mesurait ce qui n'existe pas dans un document : une **feuille de style qui cache
la navigation**, des **en-têtes HTTP**, un **fichier d'icône absent**. C'est la définition d'un angle
mort : le contrôle ne peut pas échouer sur ce qu'il ne regarde pas.

## 2 · Nos deux corrections de méthode

1. **« 0 faute » ne veut rien dire sans le périmètre.** Chaque portique dit désormais ce qu'il couvre ;
   le rapport de livraison dit ce qu'**aucun** portique ne couvre (§5). Un vert ne se lit plus comme
   « le site est bon » mais comme « ces 42 choses-là sont bonnes ».
2. **Un portique doit avoir été vu mordre.** `tools/qa/test_audit_delivery.py` monte un site sain, puis
   casse une chose à la fois (douze pièges) et vérifie que le contrôle la nomme. Le vert du premier cas
   et les douze rouges du suivant sont dans le même test, exécuté à chaque fois.

## 3 · Une erreur **dans l'audit extérieur**, corrigée ici

L'audit propose, pour le cache :

```
/*.webp
  Cache-Control: public, max-age=604800
```

Sur Cloudflare Pages — l'hôte de DM, et l'audit le dit lui-même puisque `_headers` y est honoré — le
splat `*` **ne vaut qu'en fin de motif**, et un motif commence par `/`. `/*.webp` ne matche donc aucun
fichier : la correction aurait été appliquée, le défaut serait resté, et le prochain audit aurait
retrouvé le même P1. `audit_delivery.py` refuse ce motif (`pattern_is_valid`), et propose les deux
voies qui marchent : un dossier d'assets (`/assets/*`) ou une **Cache Rule** du tableau de bord.
Sur Vercel, `vercel.json` accepte une expression de chemin et la même règle y est valide — d'où le
contrôle séparé `_check_vercel`.

## 4 · Ce qui reste à la main, et le restera

- **Le rendu réel** : Chrome headless n'est pas installé ici (téléchargement bloqué). `audit_delivery`
  lit le CSS, il ne calcule pas de layout. Un chevauchement ne se voit qu'à l'écran.
- **axe-core** : nous n'avons pas d'équivalent ; `audit_a11y` couvre 42 critères mécaniques, pas les
  règles de composition d'axe.
- **Un vrai partage WhatsApp** d'un lien produit (l'aperçu WebP se teste en envoyant le lien).
- **Le lecteur d'écran** : `tools/qa/PROTOCOLE-LECTEUR-ECRAN.md` (NVDA, TalkBack), cinq minutes, à la main.
- **Les faits du client** : nom complet du fondateur, horaires réels — un portique ne peut pas savoir
  que « Domche Noumbi » est « DOMCHE NOUMBI Samuel Renaud ». Ça se vérifie à la source (ONOC), et ça
  s'écrit dans `clients/dm-optic/`.

## 5 · La porte de livraison, telle qu'elle tourne

```bash
python3 tools/qa/audit_delivery.py hosting/previews/dmoptic --base https://dmoptiquesarl.com
python3 tools/qa/audit_delivery.py site --base https://amk-cm.vercel.app --strict
python3 tools/qa/test_audit_delivery.py          # le témoin : 12 pièges
```

Huit classes, huit codes : **D1** navigation mobile · **D2** cache des assets (et validité des motifs) ·
**D3** icônes · **D4** URL malformées · **D5** `llms.txt` face au sitemap · **D6** partage social ·
**D7** données structurées (dont **`price` = P1**, règle maison) · **D8** en-têtes de sécurité.

État au 23/10 après branchement :

| Site | P1 | P2 | P3 | Ce que c'est |
|---|---|---|---|---|
| DM Optique (97 pages) | **2** | 7 | 2 | navigation mobile absente ; cache à zéro ; polices ; icônes ; double barre ; llms.txt ; WebP en partage ; `Product` ; HSTS |
| AMK `site/` (15 pages) | **1** | 1 | 2 | deux pages publicitaires (`creation-site-web-*`) sans navigation sous 820 px ; huit pages concepts sans liens de section sous 640–861 px (P2) |

Les deux P1 de DM et le P1 d'AMK sont **antérieurs** à ce fichier : le portique les révèle, il ne les a
pas créés.
