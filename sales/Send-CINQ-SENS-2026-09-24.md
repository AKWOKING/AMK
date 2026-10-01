# CINQ SENS — le message à envoyer après le déploiement (24/09/2026)

**Pour qui :** Référence Optique Médicale Cinq Sens SARL, Douala — **696 698 136** (WhatsApp).
**Pourquoi maintenant :** le cabinet a répondu « **Ok** » à 17:04 au message du lot 4 (« Souhaitez-vous
que je vous envoie le lien pour y jeter un coup d'œil sur votre téléphone ? »). L'aperçu est construit
(`demos/concept-cinqsens-v1.html`).

> ⚠️ **Un mot à ne jamais répéter.** Le message de 16:53 disait *« il n'existait pas encore de page
> officielle réunissant vos deux cabinets »*. C'est faux au sens strict : **leur blog Blogger existe**, il
> mentionne bien les deux cabinets, et sa dernière publication est du **15 octobre 2021**. L'angle vrai,
> daté et vérifiable, est celui ci-dessous : *« le blog s'arrête en octobre 2021 »*. On ne renie pas le
> travail de King — on corrige la phrase, parce qu'un client qui vérifie ne doit pas nous prendre en
> défaut sur un fait.

**AVANT D'ENVOYER — le portique, dans cet ordre :**

1. **Déployer le dossier entier** `hosting/previews/cinqsens/` (`index.html` **et** `og.jpg`) — projet
   Vercel séparé, par exemple `cinqsens` ;
2. `python3 demos/build_cinqsens.py --url https://<adresse>` puis **redéployer** : `og:url` et `og:image`
   ne se devinent pas ;
3. vérifier **sur un téléphone**, en plein jour : FR par défaut, bascule EN qui change tout, un **vrai
   WhatsApp pré-rempli** (le numéro doit être le 696 698 136), la bande d'arrivage qui défile sans
   saccade, la barre du bas visible, aucun débordement horizontal ;
4. la vignette du lien montre bien la carte 1200×630, pas un carré gris.

---

## 1 · Le message (à copier tel quel, après la carte du lien)

```
Votre page est prête : <ADRESSE>

Elle réunit vos deux cabinets, Akwa et Brazzaville, avec vos propres repères
(le Collège King Akwa, le Kokotier, l'immeuble Flore service, l'immeuble Michelin),
vos services avec ce qu'il faut apporter pour chacun, et vos réponses aux six
questions qu'on vous pose le plus souvent. Le patient choisit son cabinet, et le
message WhatsApp part déjà écrit, avec votre numéro d'urgence.

Un mot franc : le blog du cabinet s'arrête en octobre 2021, et un patient qui vous
cherche depuis son téléphone tombe sur des annuaires. Cette page prend le relais.

Il me manque des choses vraies, et je n'en inventerai aucune : les horaires
définitifs, vos marques, vos moyens de paiement, les assurances que vous acceptez —
et surtout des photos. Vos montures, et vos deux cabinets : trois ou quatre photos
prises au téléphone, en plein jour, suffisent. Si vous voulez qu'un nom soit écrit
sur la page, dites-moi lequel.

Ouvrez-la sur votre téléphone et dites-moi ce qui manque ou ce qui est faux.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi ce texte est écrit comme ça** (MESSAGES §1) : il ouvre sur **le fait nouveau pour lui**
(« Votre page est prête »), le nom et le titre passent **à la fin**. Aucun prix, aucun délai, aucune
promesse de classement, aucun reproche — le constat sur le blog est **daté**, donc vérifiable, et suivi
immédiatement de ce que la page fait à la place.

## 2 · Les douze informations qu'on attend (et qu'on ne devinera pas)

Elles vivent dans **`clients/cinq-sens/a-completer.md`**, à recopier si le cabinet demande la liste :
**① le nom du responsable · ② les horaires définitifs · ③ la deuxième ligne (655 163 365) est-elle
active ? · ④ six à dix photos de montures · ⑤ deux ou trois photos par cabinet · ⑥ les marques vendues ·
⑦ les moyens de paiement · ⑧ les assurances · ⑨ veut-il afficher des prix ? · ⑩ livraison : quartiers,
délai, frais · ⑪ prothèses oculaires : qui, et sur rendez-vous ? · ⑫ dimanches et fermetures.**

## 3 · Ce qu'on répond s'il pose une question

- **« Combien ça coûte ? »** → la grille est celle de King, jamais improvisée dans la conversation :
  remonter la question à King avant de donner un chiffre (règle des prix).
- **« Qui a fait ça ? »** → Akwo King / AMK, Douala. Le bandeau de pied de page porte « Aperçu préparé par
  AMK pour Cinq Sens » — c'est assumé.
- **« Pourquoi ces photos ne sont pas les miennes ? »** → parce qu'on ne fabrique pas la vitrine d'un
  opticien : les trois images sont des illustrations, et ses photos prennent leur place le jour même.
- **« Pourquoi il n'y a pas mes marques ? »** → parce qu'on n'en connaît aucune ; on n'écrit que ce qu'il
  vend vraiment. Sa liste, et elles s'affichent.
- **« Le nom du responsable ? »** → la page n'en porte aucun, faute de source : ce sera le premier ajout
  dès qu'il donne le nom.

## 4 · Après l'envoi

- La réponse se traite **dans l'heure** et s'écrit dans `sales/Activity-Log.md` avec l'heure et le mot
  exact (§34.1 : une réponse humaine arrête l'horloge).
- S'il envoie les éléments : `python3 demos/build_cinqsens.py --url <adresse>` → **un seul
  redéploiement** → on lui renvoie la page complétée.
- S'il ne répond pas : **aucune relance-reproche**. Le fil reste ouvert ; la page est à lui.
