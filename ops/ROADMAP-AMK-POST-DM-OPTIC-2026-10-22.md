# Feuille de route AMK après DM Optique — les cinq chantiers, remis dans l'ordre

```
Date     22/10/2026
Contexte DM Optique n'est pas encore « livré » : la vidéo attend la validation du client.
         Cette feuille de route commence donc par ce qui débloque le reste, pas par ce qui est amusant.
Règle    un seul chantier de développement à la fois. Trois clients à servir + deux produits à coder = rien de fini.
```

---

## 0 · L'ordre, et pourquoi c'est celui-là

| # | Chantier | Quand | Pourquoi à ce moment |
|---|---|---|---|
| **A** | **NIU · RCCM · RIB d'AMK** | **cette semaine** | sans ça, aucune facture n'est émise — et les deux chantiers suivants tournent à vide |
| **B** | **Système de facturation** (interne) | semaine 1–2 | il sert **immédiatement** : solde DM Optique, retainer, prochain client |
| **C** | **Routine de maintenance** (document + outil) | semaine 1 | se fait en 2 h, et évite de perdre un client en silence |
| **D** | **Cadence 2 publications/semaine** | dès la 1re validation | c'est de la production, pas du développement : ça n'entre pas en conflit |
| **E** | **Essai virtuel** (finir l'app) | semaine 3–5 | le plus gros morceau, et le seul qui n'a **aucun acheteur identifié** aujourd'hui |

**La règle : B et C avant E.** Un outil de facturation qui marche rapporte de l'argent dès le premier client ; une app d'essayage finie ne rapporte rien tant que personne ne l'a achetée.

---

## 1 · « Un système de facturation web pour AMK » — oui, mais pas celui que tu imagines

### 1.1 Ce que le dépôt savait déjà (et qu'il ne faut pas refaire)

`research/ETUDE-OFFRES-LOGICIEL-2026-09-23.md` a déjà corrigé l'erreur : **vendre un logiciel de gestion au Cameroun est un marché saturé et bon marché.**

| Concurrent local | Prix mensuel | Ce qu'il fait déjà |
|---|---|---|
| **Nkap Control** 🇨🇲 | **gratuit** (20 factures) · 3 000 (Pro) · 10 000 (Max) | TVA 19,25 % automatique, **MTN MoMo + Orange Money intégrés** |
| **zBilling** 🇨🇲 | 10 000 (2 utilisateurs) | ventes, factures, stocks, SMS clients |
| **GesCab** | 6 500 – 12 000 | SYSCOHADA, paie CNPS, **DSF au format DGI** |
| **Duka360** | 11 150 | caisse, stock, facturation, RH |
| **Omamori** 🇨🇲 | 15 000 – 25 000 | gestion + paie camerounaise |

**Conclusion inchangée : ne pas construire un produit de facturation pour le vendre.** On arriverait plus cher, plus tard, avec moins de fonctions.

### 1.2 Ce qui manque vraiment — et qui est à nous

Il n'existe **aucun outil** pour la chose qu'on fait tous les jours : **facturer nos propres prestations**, avec acompte, solde, retainer mensuel, paiement partiel en Mobile Money et relance. Aujourd'hui cette chaîne n'existe pas — et c'est exactement ce qui a rendu la conversation avec DM Optique floue.

**Donc : un outil interne, pas un SaaS.**

| Ce qu'il fait | Pourquoi c'est urgent |
|---|---|
| Devis → proforma → facture → reçu → avoir, avec **numérotation continue** | le solde de 75 000 FCFA doit partir avec une pièce propre |
| **Acompte + solde + paiements partiels** suivis | DM Optique a payé en espèces, sans reçu. On ne refait pas ça |
| Facture récurrente mensuelle (retainer) | 3 clients = 3 factures par mois, à la main aujourd'hui |
| Tableau de bord : encaissé, en attente, en retard | c'est le seul chiffre qui dit si le mois est tenu |
| Mentions légales complètes (NIU, RCCM, TVA ou « TVA non applicable ») | une facture sans NIU n'existe pas fiscalement |

### 1.3 La règle de prudence à écrire dans le code

> **On n'écrit jamais « conforme DGI », ni « facture normalisée », ni « facture électronique ».**

La loi de finances 2026 impose la facturation électronique via des **plateformes agréées**, dont la liste n'est pas publiée. Personne ne peut promettre la conformité aujourd'hui — et notre outil n'est pas agréé.

Ce qu'on peut écrire, en revanche : *« document de facturation — mentions légales camerounaises »*. C'est vrai, c'est vérifiable, et ça ne nous engage pas sur un agrément qui n'existe pas.

**Détail complet : `tools/facture/SPEC-FACTURATION-AMK-2026-10-22.md`.**

---

## 2 · L'essai virtuel — ce que j'ai trouvé dans le dossier

Le dossier `tryon-camera/` existe déjà. **Ce n'est pas un prototype vide : c'est une application finie, mais elle appartient à un autre client.**

| Constat mesuré | Conséquence |
|---|---|
| `V2 Try-On Camera.html` — **3,1 Mo**, un seul fichier | trop lourd pour un forfait de 20 000 FCFA : chaque visite coûte de la data au client |
| dont **3,0 Mo en images base64** (les montures embarquées) | les montures sont dans le HTML : impossible de changer une monture sans reconstruire la page |
| **619 occurrences de « UO »** (Univers Optique) | ce n'est pas un produit AMK : c'est le produit d'un client, prêté |
| MediaPipe tiré de **deux CDN** (jsdelivr + Google Storage), modèle ≈ 10 Mo | premier chargement lourd, et dépendance à deux domaines externes |
| montures avec coordonnées verres (L, R, `dist`) | le format est bon — c'est la brique à garder |
| En ligne sur **Vercel**, sous `uo-essayage-camera` | hébergement au nom d'un client, pas au nôtre |

**Ce que j'en conclus : ce n'est pas « à finir », c'est « à découpler ».** Le moteur est bon ; tout ce qui l'entoure est mono-client.

### Les modifications, par ordre d'importance

1. **Sortir les montures du HTML** → un `frames.json` par client, chargé à la demande. Une monture = ~500 Ko aujourd'hui, compressée en WebP ≈ 80 Ko.
2. **Dé-brander** : le nom, les couleurs, le logo et le message WhatsApp viennent d'un `client.json`, pas du code.
3. **Ramener le premier chargement sous 1,5 Mo** avant la première monture, et annoncer le poids (« ≈ 10 Mo au premier lancement, puis en cache »).
4. **Héberger le modèle nous-mêmes** (Cloudflare R2) : deux CDN tiers = deux façons de tomber en panne.
5. **Ajouter le but commercial** : après la capture, un bouton **« Envoyer cette monture sur WhatsApp »** avec le nom de la monture pré-rempli. Aujourd'hui l'appli télécharge un PNG et s'arrête — elle ne vend rien.
6. **Mesurer** : 4 événements (ouverture caméra, changement de monture, capture, clic WhatsApp). Sans ça, on ne saura pas si l'outil sert.
7. **La mention d'honnêteté** : *« rendu indicatif — l'ajustement réel se fait en boutique »*. Un essayage virtuel qui promet un ajustement parfait fabrique des déceptions, et la déception revient au vendeur.

**Décision à prendre avant de coder : à qui appartient cette app ?** Si c'est pour Univers Optique, on ne peut pas la rebrander pour un autre client sans son accord. Si c'est un actif AMK, il faut que ce soit écrit quelque part. Aujourd'hui, ce n'est écrit nulle part.

**Détail : `tryon-camera/PLAN-V2-AMK-2026-10-22.md`.**

---

## 3 · Publier deux fois par semaine — **deux calendriers distincts** (corrigé le 22/10)

⚠️ **Correction du 22/10** : ce créneau dimanche + lundi concerne **les comptes d'AMK**, pas ceux de DM Optique. Un compte client et notre propre compte n'ont ni le même public ni la même fonction. Le détail des deux calendriers est dans `ops/CADENCE-PUBLICATION-2026-10-22.md`.

| Compte | Jours | Heure | Fonction |
|---|---|---|---|
| **AMK** | dimanche + lundi | 19 h · 13 h | être connu, être cru |
| **DM Optique** | mardi + jeudi | 19 h · 13 h | être vu, être cru |

Ce qui suit explique **pourquoi** les deux jours d'AMK se défendent, et pourquoi ils ne conviennent pas à un opticien.

| Source | TikTok | Facebook |
|---|---|---|
| **Buffer** (7,1 M de vidéos / 14 M de posts) | **dimanche 9 h** = meilleur créneau de la semaine, puis lundi 13 h | jeudi 9 h, mercredi meilleur jour |
| **Sprout Social** (2 Md d'interactions) | mardi–jeudi 14 h–18 h, **dimanche = pire jour** | mardi–mercredi 12 h–20 h, week-end faible |
| **Hootsuite** (1 M de posts) | jeudi matin, samedi midi | 5 h–8 h |

**Traduction pratique :**

- **Dimanche + lundi est un bon choix pour TikTok** (Buffer le confirme), à condition de viser **dimanche matin** et **lundi début d'après-midi**.
- **Pour Facebook, le milieu de semaine est meilleur** — mais la page a 22 vues : on n'a aucune donnée propre, et les études globales ne décrivent pas Bonabéri.
- **Deux jours consécutifs, ce n'est pas une cadence, c'est une rafale.** Ce qui compte n'est pas l'espacement, c'est que **les deux pièces aient des fonctions différentes** : dimanche = l'épisode (la vidéo), lundi = l'utile (le post qui explique, rassure, rappelle).

**Ma recommandation, à tenir 4 semaines sans changer :**

| Jour | Heure | Quoi | Fonction |
|---|---|---|---|
| **Dimanche** (AMK) | 19 h | une pièce de fond : le métier, un cas, une leçon | être connu |
| **Lundi** (AMK) | 13 h | une pièce courte : méthode, chiffre, outil | être cru |
| **Mardi** (DM) | 19 h | la vidéo de la série | être vu |
| **Jeudi** (DM) | 13 h | un post utile : le lieu, un mythe, une question | être cru |

Pourquoi 19 h le dimanche et pas 9 h : les études mesurent l'engagement **des gens qui utilisent l'application**, pas ceux qui vont chez l'opticien. À Bonabéri, un dimanche matin, on est à l'église ou au marché. C'est une hypothèse — et c'est justement pour ça qu'il faut la noter et la vérifier sur 4 semaines.

**La condition qui prime sur tout :** on ne passe pas à deux publications par semaine sans **deux pièces d'avance validées**. Sinon on refait le mois dernier — produire sans publier. Le stock de sécurité n'est pas du confort, c'est la condition de la régularité.

---

## 4 · La routine de maintenance — le document qui manquait

Les repères du secteur, vérifiés :

- **Le rapport mensuel est la norme** : 46 à 58 % des agences rapportent chaque mois, 14 % par semaine. En dessous d'un mois, on ne distingue pas une tendance d'un creux.
- **Le temps de réponse est un KPI** : 73 % des clients attendent une réponse en moins de 24 h, 42 % en moins de 60 min. Un standard réaliste : **60 min en journée pour du grand public, 4 h en B2B, 24 h maximum**.
- **Le rapport doit coûter 4 à 6 % du temps facturé** : chez nous, 1 page + 3 phrases, pas un PDF de 12 pages.
- **La revue trimestrielle augmente la rétention de 22 à 31 points** selon les études d'agences — c'est le rendez-vous qu'on saute toujours, et c'est celui qui garde le client.

**Le détail complet (quotidien, hebdomadaire, mensuel, trimestriel, avec le temps que ça prend) : `knowledge/MAINTENANCE-CLIENTS-2026-10-22.md`.**

Résumé du budget temps pour un retainer à 75 000 : **≈ 11 h/mois**, dont 8 h de production et 3 h d'entretien et de mesure. Si l'entretien dépasse 3 h, ce n'est plus de l'entretien, c'est un projet — et il se facture.

---

## 5 · Ce que j'ajouterais, et que tu n'as pas listé

Par ordre d'impact réel sur ton mois :

1. **Régulariser AMK.** NIU, RCCM, RIB, régime fiscal. Sans ça : pas de facture, pas de virement, pas de client sérieux. C'est le point 0 de tout le reste.
2. **Un contrat d'une page par client**, avec trois clauses qui nous protègent : acompte avant travaux, délai de validation de 5 jours ouvrés, propriété des comptes au client. Le mois de DM Optique s'est perdu sur ces trois lignes absentes.
3. **Un cas DM Optique honnête.** Pas « +300 % » : « voilà ce qui a été construit, voilà l'état de départ, voilà ce qu'on mesure ». Un cas faible raconté honnêtement vend mieux qu'un faux chiffre qui s'écroule à la première question.
4. **Un modèle de proposition en une page** (offre, prix, ce qui n'est pas inclus, délai). Aujourd'hui, chaque devis se réécrit.
5. **Une sauvegarde et une politique de données** : les fichiers clients, les accès, les photos. Une perte de disque ne doit pas coûter un client.
6. **Ne pas construire deux produits à la fois.** Facturation maintenant, essayage ensuite, et seulement si un acheteur est identifié.

---

## 6 · Ce que je ne ferais pas

- **Vendre un logiciel de facturation** au Cameroun : marché à 0–25 000 FCFA/mois, déjà servi, et la réforme 2026 favorise les éditeurs agréés, pas nous.
- **Promettre « conforme DGI »** avant la publication de la liste des plateformes agréées.
- **Ouvrir un troisième chantier de code** avant que les deux premiers soient stables.
- **Passer à 2 publications/semaine sans stock d'avance.**
- **Facturer l'essai virtuel à un client qui ne l'a pas demandé** : c'est un argument de vente, pas une ligne de devis surprise.

---

## 7 · La semaine, en clair

| Jour | Quoi |
|---|---|
| **Aujourd'hui** | envoyer le message des comptes ; relancer le RIB/NIU d'AMK |
| **Demain** | publier le post enfants ; envoyer le solde si la vidéo est validée |
| **Cette semaine** | routine de maintenance écrite (2 h) ; spec de facturation validée |
| **Semaine prochaine** | facturation v1 : devis, facture, paiement, PDF |
| **Ensuite** | 2 publications/semaine tenues 4 semaines, puis lecture des chiffres |
| **Après** | essai virtuel — seulement si un client le demande ou le paie |
