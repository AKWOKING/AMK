# Envoi à faire CE SOIR — LE CRISTALLIN · réécrit 21/09 19:40 (après la transcription de la vocale)

> ⚠️ **Ce fichier remplace la version de 19:15.** La version de 19:15 parlait de « la dette du lien promis » et
> posait quatre confirmations. **La transcription de King change la nature du fil** : la note vocale de 18:01
> n'était pas une demande technique, c'était une information (**il a déjà un site ET une page Facebook**) suivie
> d'**une question d'achat** : **« est-ce que vous voulez m'en créer une autre ? »**. On n'est plus en train de
> livrer un aperçu, on est en train de **répondre à une demande de prestation**. Étapes CRM : `presented` →
> **`closing`** (`closing = 3`).

---

## ① D'ABORD le fichier (l'aperçu, pas un lien à inventer)

`hosting/previews/cristallin/index.html` — **59 KB**, un seul fichier, s'ouvre dans le navigateur d'un téléphone,
FR|EN commutable. Contrôle final : `audit_html.py` = **0 finding** (389 runs, desktop 389 / mobile 389) ·
172 FR / 172 EN · diff démo ↔ aperçu = 0 ligne.

⚠️ **Ne pas envoyer `amk-cm.vercel.app/cristallin/`** : le dossier est bâti dans le dépôt, **pas déployé** → 404.
Je ne devine jamais une URL de preview (c'est `yaks-concept` qui a brûlé comme ça). Si tu préfères le lien :
déploie, donne-moi l'URL exacte, je la grave. Capture mockup impossible ici (`playwright` absent) : le fichier suffit.

---

## ② ENSUITE le texte — DEUX VERSIONS, roi, choisis la tienne

### Version A — **sans prix** (si tu ne confirmation pas encore le périmètre)

```
Merci pour la note vocale, Monsieur Messoue — c'est noté pour la page Facebook.
Je vous joins l'aperçu de la version modernisée de votre site : l'examen de la vue se réserve par WhatsApp, chaque ligne du tableau d'acuité ouvre la conversation.
Oui, on peut vous créer une page Facebook propre et la relier au site — donnez-moi juste le lien de la page actuelle.
Deux choses à me confirmer avant publication : le samedi (votre flyer l'annonce, votre site ne le montre pas) et la liste de vos assureurs.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

### Version B — **avec prix** (il a posé la question, donc le prix peut sortir d'un message 1 — règle consommée)

```
Merci pour la note vocale, Monsieur Messoue — c'est noté pour la page Facebook.
Je vous joins l'aperçu de la version modernisée de votre site : réservation par WhatsApp, lisible sur téléphone.
Pour la page Facebook : oui, on la crée et on la relie au site.
Les deux postes : refonte du site 100 000 FCFA · page Facebook (création + relecture mensuelle) 50 000 FCFA · paiement 50 % au démarrage.
Dites-moi lequel vous voulez en premier — je commence par celui-là.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi le prix est maintenant légitime :** la règle « jamais de prix dans un message 1 » protège le premier
contact. Ici message 1 envoyé (17:51) · lu et répondu (17:53) · aperçu annoncé (17:57) · **c'est LUI qui demande
si on lui crée un support**. Précédent dans le portefeuille : AFRIQUE LABO et Bonanjo ont eu 100 000 FCFA dans le
fil, **sans remise**. ⚠️ **Décision à toi avant d'envoyer B** : est-ce qu'AMK **fait** la création/gestion de page
Facebook, et à quel tarif ? Je ne chiffre pas un service que tu n'as pas validé — si tu dis non, on envoie A et
la page Facebook reste une porte ouverte (« je vous mets en relation »), pas une promesse.

**Ce qui est vérifié dans ces lignes :** le flyer reçu et remercié · la page Facebook (paroles de lui, 18:01) ·
le samedi **sur le flyer** (8h30–13h30, lu sur l'image à l'écran) · la liste des 12 assureurs **jamais confirmée
sur sa page d'accueil** → donc à valider par lui, pas affirmée par nous.

**Ce qui a été RETIRÉ de la maquette ce soir, et pourquoi :** j'avais écrit que son flyer donnait une **adresse
différente** (Bonapriso / CTFIC Mballa 2) du site (Akwa / FODEC). Sur l'image visible à l'écran, le flyer porte
**lui aussi Akwa / FODEC / COMECI** : l'écart est peut-être de mon côté. La page ne l'affirme plus — elle
**demande** : « si une deuxième adresse existe, écrivez-la moi, je ne mets qu'une adresse validée par vous ».
Jamais je ne laisse une correction d'inventaire devenir une correction du client.

## ③ DANS LA MAQUETTE, ce qui vient de changer (19:40)

- **Ligne « Votre page Facebook »** dans le bloc *Nous joindre* : elle est **nommée, pas liée** — son URL nous est
  inconnue, un lien deviné enverrait chez un homonyme. Dès qu'il donne le lien, il entre ici + dans `sameAs` du JSON-LD.
- `addrFlag` réécrit (question, pas accusation) · `hoursFlag` réécrit (« un seul des deux peut être publié »).
- Contrôles rejoués après édition : **0 finding**, 172 FR / 172 EN, 0 jeton survivant, 0 `<a>` sans `href`,
  `wa.me/699905577` (chiffres seuls), rail mobile = même libellé que le hero.

## ④ CE QUE J'AI FAUX À NE PAS REFAIRE

- Le message de **17:57** était : « Parfait ! Je prépare votre aperçu sur-mesure et je vous transmets le lien très
  rapidement. A très vite ! » — **je n'ai jamais écrit « je vous envoie le fichier »** : ne pas lui reprocher une
  promesse qu'il n'a pas reçue, et ne pas inventer la sienne.
- **18:07 : « You deleted this message »** — King a retiré un texte avant de renvoyer celui de 18:13. Je note le
  fait, je n'en conclus rien.
- `last_send_state = read` : deux coches **grises** sur le 18:13 à l'écran de 19:40. Pas de bleues = pas de
  lecture affirmée.

## ⑤ DÈS QU'IL RÉPOND

1. lien de la page FB + « vas-y » → **V2** : je câble le `sameAs`, la ligne FB, la ou les adresses validées, les
   assureurs confirmés, le samedi tranché → page prête à publier, et devis signé (50 % à la signature).
2. « seulement le site » → la page FB sort du périmètre, prix = 100 000 FCFA seul, rien d'autre à négocier.
3. « seulement la page FB » → poser le prix du poste seul **en retirant du périmètre**, jamais en cassant 100 000.
4. silence → FU1 mercredi 23/09, **une** ligne : « Vous avez pu jeter un œil à l'aperçu, Monsieur Messoue ? ».
   FU2 vendredi 25 · FU3 mardi 29 · puis parked. Jamais une deuxième relance le même soir.

⚠️ **Ce que je n'ai pas dans ce bac :** le fichier de la vocale et la résolution suffisante du flyer — je travaille
sur la transcription de King et sur l'image visible à l'écran. Le « last seen today at 18:06 » de son profil veut
dire qu'il est sur WhatsApp plusieurs fois par jour : **la fenêtre est ouverte ce soir**, avant 21:00 pour ne pas
décrocher sur une question qu'il a posée lui-même.
