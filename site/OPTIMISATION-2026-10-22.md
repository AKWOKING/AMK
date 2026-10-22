# AMK — optimisation du site `amk-cm.vercel.app`

```
Exécuté  22/10/2026 (soir) — corrections appliquées dans site/, déploiement NON fait (voir §7)
Relevé   22/10/2026, sur le site EN LIGNE (pas sur le dossier local — les deux diffèrent)
Constat  la passe SEO du 08/10/2026 n'a jamais été déployée. Le public voit encore la v01.
Principe ce qui se corrige ici ne coûte rien : que du texte et des attributs.
```

---

## 1 · Les cinq erreurs visibles par un visiteur

| # | Ce qu'on lit en ligne | Pourquoi c'est faux | Correction |
|---|---|---|---|
| 1 | « **En ligne en 3–5 jours** » — **8 occurrences** | on ne l'a pas tenu : DM Optique a pris un mois. C'est l'engagement le plus vérifiable de la page, et c'en est le plus fragile | retirer le chiffre, dire **« un site livré, pas un site promis »**, et laisser la date au devis |
| 2 | « En ligne en **5–7 jours** » (offre Croissance) | même problème, en plus long | idem |
| 3 | **Compteurs à 0** : « 0 langues », « 0 sites concepts », « 0h » | le chiffre s'anime en JS ; si le script ne tourne pas (réseau lent, aperçu Facebook, lecteur d'écran) le visiteur lit **zéro**. Un zéro est pire que pas de compteur | **écrire les chiffres en dur** dans le HTML ; l'animation devient un bonus |
| 4 | « **Quatre** concepts… trois pour les écoles » | **six** sont listés juste en dessous | corriger le cardinal, il se voit à l'œil nu |
| 5 | « Aperçu **24 h** » sur le bouton et dans trois réponses | nous nous sommes donné la règle : build ≤ 15 min, relecture ≤ 1 h. « 24 h » promet plus que ce qu'on veut tenir | « aperçu **le jour même**, sur WhatsApp » |

**Le point 3 est le plus coûteux, et le moins cher à réparer.** Un aperçu de lien Facebook ou WhatsApp affiche souvent la page sans exécuter le JavaScript animé : nos propres partages donnent donc l'image d'une agence à zéro partout.

---

## 2 · Ce qui est déjà bon — ne pas y toucher

Vérifié dans le HTML : `lang="fr"` · titre de 63 caractères · description de 139 caractères · images en **WebP** · **un seul bloc JSON-LD** (pas de doublon) · `og:image` et `og:url` remplis avec le bon domaine · page `mitoc` en `noindex` · 3 liens `wa.me` avec message pré-rempli · formulaire qui **ouvre WhatsApp** sans envoyer de données.

C'est au-dessus de la moyenne locale. Le problème n'est pas la base, c'est **la version en ligne**.

---

## 3 · Ce qui manque, par ordre de rendement

| Priorité | Manque | Effet | Effort |
|---|---|---|---|
| **1** | **Déployer** la version corrigée | tout le reste est théorique sans ça | 10 min |
| **2** | **Aucun lien vers nos réseaux sociaux** dans le pied de page | nos visiteurs ne peuvent pas nous suivre ; on vient d'ajouter ces liens à **97 pages** de DM Optique et pas à la nôtre | 15 min |
| **3** | **L'anglais n'est pas indexable** — pas « il manque des `hreflang` » | ⚠️ **correction du 22/10 : la première rédaction de cette ligne était fausse.** Il n'y a **pas deux URL** FR et EN mais **une seule**, dont le texte anglais vit dans des attributs `data-en` que Google n'exécute pas. Des `hreflang` n'auraient donc rien à déclarer. Conséquence réelle : le site est vu **en français seulement** par les moteurs, alors que les écoles et cliniques du Nord-Ouest et du Sud-Ouest cherchent en anglais. Le vrai correctif est un miroir `/en/` avec de vraies URL (c'est ce qui a été fait pour DM Optique : 48 pages + `hreflang`). **Coût réel : plusieurs heures, pas 20 minutes** | à planifier |
| **4** | Accueil = **écoles + cliniques seulement** | c'est **voulu** (décision du 08/10 : pas d'opticiens dans le titre tant que DM Optique n'est pas approuvé). Une page **opticiens** se crée après | après DM Optique |
| **5** | **Fiche Google** AMK | impossible à vérifier d'ici — à faire par King sur place | 30 min |
| **6** | Adresse **Gmail** comme contact | contredit la promesse (voir `brand/AMK-PRESENCE-2026-10-22.md` §3) | à décider |

---

## 4 · Le détail qu'on ne voit pas mais qui compte

Le site contient **`img/nova.webp`** et **`og-cover.jpg`** dans ses concepts. Or **`nova` est le nom d'une école fictive** utilisée comme démonstration : c'est bien, et c'est étiqueté. Le risque n'est pas là.

Le risque est ailleurs : **un concept fictif présenté comme un client**. La page dit « noms fictifs, nous ne montrons jamais le site d'un client sans accord écrit » — **cette phrase doit rester**, c'est elle qui protège. Ne jamais la raccourcir au moment de gagner de la place.

---

## 7 · Journal d'exécution — 22/10 (soir)

| # | Correction | État |
|---|---|---|
| 1 | Promesse « 3–5 jours » / « 5–7 jours » / « en une semaine » | ✅ **retirée partout** — `index.html`, les deux pages métier, la page concept maternelle, et jusqu'aux `og:`/`twitter:` et au JSON-LD (c'est là que Google la lisait) |
| 2 | Compteurs à 0 (« 0 langues », « 0 sites concepts ») | ✅ **le chiffre est dans le HTML** ; l'animation ne fait plus que le rejouer. Un aperçu de lien ou un lecteur d'écran lit désormais 24 h / 2 langues / 6 concepts |
| 3 | « Quatre concepts » alors que six sont montrés | ✅ **« Six concepts »**, et « trois pour les écoles, **trois** pour les cliniques » (FR et EN) |
| 4 | Carte de statistique qui promettait « 3–5 jours » | ✅ remplacée par **« 100 % — à vous : domaine, fichiers, hébergement »**, vrai et vérifiable sur la page |
| 5 | Réponse FAQ « combien de temps ? » | ✅ réécrite : « Nous ne donnons pas de date avant de connaître le périmètre. L'aperçu est dans votre téléphone sous 24 heures ; la mise en ligne suit vos validations. » |
| 6 | `amk-site.zip` périmé | ✅ reconstruit (`hosting/build_site_zip.py`), 4,0 Mo, cohérent avec `site/` |

**Vérifications passées** : `audit_seo` et `audit_html` verts sur les 4 pages modifiées (sauf
`sample-nursery.html`, qui porte **5 contrastes insuffisants préexistants** — non touchés, c'est un
choix de design de la démo).

**⚠️ Ce qui n'est pas fait : le déploiement.** Voir le §5 ci-dessous — il reste à la main de King.

---

## 5 · Le plan de déploiement, sans risque

1. **Comparer** le dossier `site/` et `amk-site.zip` (22/10 14:16, 4,0 Mo, 28 fichiers, dont 6 `img/*.webp`) : publier **le plus récent**, pas les deux.
2. **Déployer en prévisualisation** d'abord (`vercel deploy` sans `--prod`) et relire la page sur téléphone.
3. Vérifier les cinq points du §1 **sur l'URL de prévisualisation**, pas dans l'éditeur.
4. Passer en production.
5. **Redemander l'indexation** dans la Search Console, et repasser le partage dans le *Facebook Sharing Debugger* (le cache Open Graph garde l'ancienne image plusieurs jours).

**Ne pas publier depuis un dossier dont on n'est pas sûr** : c'est comme ça qu'on écrase une correction par une version plus ancienne.

---

## 6 · Ce que je ne peux pas faire d'ici — vérifié le 22/10 au soir

- **Déployer.** Le connecteur Vercel atteint bien l'équipe (`amk-5d61`) et le projet `dm-optique-sarl`,
  mais **aucun projet `amk-cm` n'est visible** : ni par identifiant, ni par recherche. Je ne peux donc
  pas publier ce que je viens de corriger. **Il reste 2 minutes de travail pour King** (voir §8).
- **Créer ou vérifier la page Facebook** : `facebook.com/amkweb` répond **403** à toute requête
  automatique (Facebook ferme l'accès aux robots), et il n'y a pas de navigateur ici.
- **Vérifier la fiche Google** d'AMK.
- **Voir le site comme un visiteur** : je lis le HTML, je ne le regarde pas.

---

## 8 · Les 2 minutes de King — publier les corrections

Le dossier `site/` est à jour dans le dépôt ; le zip aussi. Au choix :

1. **Si le projet `amk-cm` est relié à GitHub** : fusionner la branche suffit, Vercel redéploie seul.
   Un commit vient de partir — vérifier dans Vercel qu'un déploiement apparaît pour ce projet.
2. **Sinon, à la main** : ouvrir le projet `amk-cm` dans Vercel → *Deployments* → glisser le contenu de
   `site/` (ou le `amk-site.zip` reconstruit) → publier.
3. **Puis, dans l'ordre** : ouvrir `amk-cm.vercel.app` sur téléphone et vérifier les quatre points —
   plus de « 3–5 jours », les compteurs affichent 24 / 2 / 6, « Six concepts », et la FAQ répond sans
   date. Enfin, repasser le lien dans le *Facebook Sharing Debugger* (le cache garde l'ancienne image).

Tout le reste du §2 et du §3 est faisable maintenant, dans le dépôt.
