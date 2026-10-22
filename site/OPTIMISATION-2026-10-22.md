# AMK — optimisation du site `amk-cm.vercel.app`

```
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
| **3** | **Pas de `hreflang`** | le site est bilingue FR/EN mais Google ne le sait pas : les deux versions peuvent se concurrencer | 20 min |
| **4** | Accueil = **écoles + cliniques seulement** | c'est **voulu** (décision du 08/10 : pas d'opticiens dans le titre tant que DM Optique n'est pas approuvé). Une page **opticiens** se crée après | après DM Optique |
| **5** | **Fiche Google** AMK | impossible à vérifier d'ici — à faire par King sur place | 30 min |
| **6** | Adresse **Gmail** comme contact | contredit la promesse (voir `brand/AMK-PRESENCE-2026-10-22.md` §3) | à décider |

---

## 4 · Le détail qu'on ne voit pas mais qui compte

Le site contient **`img/nova.webp`** et **`og-cover.jpg`** dans ses concepts. Or **`nova` est le nom d'une école fictive** utilisée comme démonstration : c'est bien, et c'est étiqueté. Le risque n'est pas là.

Le risque est ailleurs : **un concept fictif présenté comme un client**. La page dit « noms fictifs, nous ne montrons jamais le site d'un client sans accord écrit » — **cette phrase doit rester**, c'est elle qui protège. Ne jamais la raccourcir au moment de gagner de la place.

---

## 5 · Le plan de déploiement, sans risque

1. **Comparer** le dossier `site/` et `amk-site.zip` (22/10 14:16, 4,0 Mo, 28 fichiers, dont 6 `img/*.webp`) : publier **le plus récent**, pas les deux.
2. **Déployer en prévisualisation** d'abord (`vercel deploy` sans `--prod`) et relire la page sur téléphone.
3. Vérifier les cinq points du §1 **sur l'URL de prévisualisation**, pas dans l'éditeur.
4. Passer en production.
5. **Redemander l'indexation** dans la Search Console, et repasser le partage dans le *Facebook Sharing Debugger* (le cache Open Graph garde l'ancienne image plusieurs jours).

**Ne pas publier depuis un dossier dont on n'est pas sûr** : c'est comme ça qu'on écrase une correction par une version plus ancienne.

---

## 6 · Ce que je ne peux pas faire d'ici

- **Créer la page Facebook** : ça demande un compte connecté dans un navigateur.
- **Vérifier la fiche Google** d'AMK.
- **Voir le site comme un visiteur** : pas de navigateur dans cet environnement, je lis le HTML.

Tout le reste du §2 et du §3 est faisable maintenant, dans le dépôt.
