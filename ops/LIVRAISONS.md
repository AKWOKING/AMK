# LIVRAISONS — ce qui a été remis, quand, et où le récupérer

Un livrable est un fichier **figé** remis à quelqu'un : une archive de site, un PDF de devis, un zip
d'application. Il ne sert qu'une fois, et il pèse ensuite dans chaque clone pour toujours. Ce registre
le sort de l'arbre sans le perdre.

**Trois règles, et elles suffisent.**

1. **Un livrable ne rentre pas dans l'arbre.** Il va dans une Release GitHub (`tools/ops/release.sh`),
   qui accepte 2 Go par fichier et ne compte pas dans la taille du dépôt. Le dépôt garde la ligne du
   registre : date, empreinte, lien, et **comment le refabriquer**.
2. **Un livrable qui se refait à l'identique n'a pas besoin d'être gardé du tout.** Il n'est alors pas
   « publié puis supprimé » : il n'a jamais eu besoin d'être là. L'empreinte de contenu ci-dessous dit
   si la refabrication est fidèle.
3. **L'empreinte de contenu n'est pas l'empreinte du zip.** Un zip embarque des dates : deux zips du
   même contenu n'ont pas le même sha256. D'où deux colonnes — le sha256 du fichier remis (pour
   vérifier un téléchargement) et le **digest de contenu** (pour vérifier une refabrication).

## Le registre

| Remis le | Release (tag) | Fichier | Taille | sha256 du fichier | Digest de contenu | Où le refabriquer | État |
|---|---|---|---|---|---|---|---|
| 2026-10-21 | `livraison-dmoptic-2026-10-21` | `dmopticsarl-2026-10-21.zip` | 4,6 Mo | `1d9d0ca6e3b6f5ab` | figé, non reproductible | — (182 entrées ; le site en compte 251 aujourd'hui) | **dans l'arbre, à publier** |
| 2026-10-23 | — | `amk-factures-pwa-v2.zip` | 88 Ko | `b46aac85f5e033b9` | digest `5902f1f5bacbf57a3a461d9845206ce02d7f0125e2514b815bec620e3131ecf6` | `bash tools/ops/pack_factures.sh` | **sorti de l'arbre, refabrication prouvée** |
| 2026-10-23 | — | `amk-factures-pwa.zip` (v1, remplacé 8 h plus tard) | 88 Ko | `7d9241fadaa5f400` | digest `f2490a32bb3ea71d0e5fdac6dc60f182ee6a1f3f93000af4ec44e3f1d7b1e055` | contenu d'origine, non reproductible | **archivé** (`archive/2026-10/`) |

## Ce qui reste à faire, et pourquoi ce n'est pas fait

**L'archive du site DM attend sa Release.** Le fichier est prêt, le commentaire de version est écrit,
et `tools/ops/release.sh` fait tout : publication, puis **aller-retour réel** (retéléchargement du zip
depuis GitHub et comparaison du sha256) avant de dire « publié ».

Il n'a pas pu être publié depuis la session du 24/10 : `uploads.github.com` — l'hôte qui reçoit les
fichiers d'une Release — n'était pas joignable depuis cet environnement, alors qu'`api.github.com`
l'était. Le script refuse maintenant de commencer dans ce cas, avec ce message plutôt qu'un `EOF`.
Sur une machine ordinaire, une commande :

```bash
bash tools/ops/release.sh --tag livraison-dmoptic-2026-10-21 \
     --file dmopticsarl-2026-10-21.zip \
     --title "Site DM Optic — archive livrée le 21/10"
```

Puis `git rm --cached dmopticsarl-2026-10-21.zip` — et la ligne État ci-dessus passe à « publiée ».

## Les deux hôtes de GitHub, à ne plus confondre

`api.github.com` crée la Release (métadonnées, tag, notes). `uploads.github.com` reçoit le **fichier**.
Un environnement peut joindre le premier et pas le second : c'est exactement ce qui s'est passé, et
`gh` le signale par un `EOF` qui ne dit rien. `release.sh` teste l'hôte d'upload avant d'écrire quoi
que ce soit — une Release à moitié faite n'est pas une livraison.
