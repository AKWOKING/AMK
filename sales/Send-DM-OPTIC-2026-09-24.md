# DM OPTIC — le message à envoyer après le redéploiement (v2.1 : patient + vitrine des montures)

**Pour qui :** M. Domche Noumbi, DM OPTIC, Douala — **656 122 239** (WhatsApp).
**Où :** ⚠️ **l'adresse réellement envoyée par King le 24/09 à 17:05 est https://dmoptic-2.vercel.app/**
(second projet Vercel ; l'ancienne `dmoptic.vercel.app` sert encore la v1). La page en ligne est bien la
**v2.1** — vérifié en lisant le HTML servi le 24/09 au soir (services, vitrine des montures, six
questions). `og:url` / `og:image` ont été recollés sur cette adresse le même soir.

**Ce que King a dit le 24/09, et ce qu'on en a fait** : *« the demo seems to speak more to the prospect,
but it's supposed to speak to the patient »* → la page a été **réécrite de zéro, patient d'abord**
(titres, actes, questions fréquentes, contact), et le hero a reçu ses **deux dégradés animés** (§7 des
notes). Puis : *« on parlait aussi de listé ces services et montré ses montures et lunettes au patient »*
et *« je ne pense pas que tout les détails de lui dans l'ordre soit nécessaire »* → **v2.1** : une
**vitrine des montures** (vue · soleil · enfants), « Nos services », et **le registre sorti du texte
visible** (§8 des notes).

> **Attention, ne pas se tromper de destinataire :** la **page** parle au **patient**. Le **message
> WhatsApp ci-dessous**, lui, s'adresse bien à **M. Domche** — c'est lui qui le reçoit. Les deux règles
> ne se contredisent pas ; elles ne visent pas la même personne.

**AVANT D'ENVOYER — le portique, dans cet ordre :**

1. King **redéploie le dossier entier** `hosting/previews/dmoptic/` (`index.html` **et** `og.jpg`) ;
2. vérifier que le lien s'ouvre **sur un téléphone**, en plein jour : FR par défaut, la bascule EN qui
   change tout le texte, un **vrai WhatsApp pré-rempli**, aucun débordement horizontal ;
3. la vignette du lien doit montrer la carte 1200×630, pas un carré gris.

---

## 1 · Le message (à copier tel quel, après la carte du lien)

```
La page est retravaillée, à la même adresse : https://dmoptic.vercel.app/

Deux choses ont changé. D'abord, elle ne parle plus au cabinet : elle parle à vos
patients — vos services, ce qu'il faut apporter, comment ça se passe, et vos réponses
aux six questions qu'on vous pose tous les jours. Ensuite, elle montre maintenant les
montures et les lunettes : lunettes de vue, lunettes de soleil, enfants, avec un mot
sur chacune et un bouton pour vous demander si vous avez un modèle.

J'ai retiré les détails administratifs (numéro d'inscription, arrêté ministériel) :
ils ne servent pas un patient.

Il me manque encore neuf choses vraies, et je n'en inventerai aucune. Les premières,
ce sont des photos : trois ou quatre du cabinet, et six à huit de vos montures, par
famille. Puis l'adresse exacte, les horaires, les moyens de paiement, les assurances
que vous acceptez, les marques que vous vendez, et la liste de vos services à valider.
Envoyez-moi ce que vous avez — le reste s'affiche le jour même.

Ouvrez-la sur votre téléphone et dites-moi ce qui manque ou ce qui est faux.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi ce texte est écrit comme ça** (MESSAGES §1) : il commence par **le fait nouveau pour lui**
(« La page est retravaillée »), nom et titre **à la fin**. Aucun prix, aucun délai, aucune promesse de
classement, aucun reproche sur ce qui manque — la liste des huit informations est une **invitation**,
pas un constat de faute.

---

## 2 · Les neuf informations qu'on attend (et qu'on ne devinera pas)

Elles vivent dans **`clients/dm-optic/a-completer.md`**, qui est le document à recopier si M. Domche
demande la liste. En résumé : **① adresse exacte + point de repère · ② horaires · ③ trois ou quatre photos du
cabinet · ④ six à huit photos de ses montures (vue · soleil · enfants) · ⑤ moyens de paiement ·
⑥ assurances/mutuelles · ⑦ marques de montures vendues · ⑧ validation des six services listés sur la
page · ⑨ une phrase de lui, ses mots, sur ce qu'il dit à ses patients.**

Une fois reçues : `python3 demos/build_dmoptic.py --url https://dmoptic.vercel.app` (les faits entrent
dans la page), **un seul redéploiement**, et on lui renvoie la page complétée.

---

## 3 · Ce qu'on répond s'il pose une question

- **« Combien ça coûte ? »** → la grille est celle de King, jamais improvisée dans la conversation :
  remonter la question à King avant de donner un chiffre (règle des prix).
- **« Qui a fait ça ? »** → Akwo King / AMK, Douala. Le bandeau de pied de page porte « Aperçu préparé
  par AMK pour DM OPTIC » — c'est assumé.
- **« Pourquoi il n'y a pas mes photos ? »** → parce qu'on ne fabrique pas un cabinet : les deux images
  sont des **mises en situation**, et ses photos prennent leur place.
- **« Il n'y a pas d'avis de patients. »** → exact, et c'est volontaire : on n'invente pas un avis ; un
  vrai avis, ou une phrase de lui, vaut mieux que dix citations fabriquées.

## 4 · Après l'envoi

- La réponse se traite **dans l'heure** et s'écrit dans `sales/Activity-Log.md` avec l'heure et le mot
  exact (§34.1 : une réponse humaine arrête l'horloge).
- **Un seul redéploiement par étape**, jamais en rafale.
- S'il ne répond pas : **aucune relance-reproche**. Le fil reste ouvert ; la page est à lui.

---

## 5 · Le texte du premier envoi (v1) — conservé pour mémoire, NE PAS RÉUTILISER

La v1 s'adressait au cabinet (« votre inscription à l'Ordre », « ces six informations sont marquées à
confirmer sur la page ») : c'est exactement ce que King a écarté. Gardé ici pour que personne ne le
reprenne :

> Votre cabinet a maintenant sa page : <ADRESSE> — Elle ne dit que ce qui est vrai aujourd'hui : votre
> inscription à l'Ordre depuis 2016 (n° 021/2016, arrêté 0382), le titulaire M. Domche Noumbi, votre
> numéro — et le fait qu'un patient qui vous cherchait depuis son téléphone ne trouvait rien. Je n'ai
> inventé ni adresse, ni horaires, ni photos : ces six informations sont marquées « à confirmer » sur la
> page […]
