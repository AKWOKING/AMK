# LA LIGNE OPTIC — le message à envoyer après le déploiement (24/09/2026)

**Pour qui :** La Ligne Optic — **Mme Joungo Line Chantale**, opticienne, Akwa (Douala) — **683 651 108**.
**Pourquoi maintenant :** le cabinet a répondu « **Ok merci beaucoup vyni** » à 21:04 au message du lot 4,
et King a annoncé le lien à 21:35. L'aperçu est construit (`demos/concept-laligne-v1.html`).

> **Le mot juste pour ce fil.** Le message du 15:29 disait : *« Pour un opticien à Akwa, le seul endroit où
> votre nom est écrit noir sur blanc, c'est le tableau de l'Ordre et un patient ne consulte jamais le
> tableau de l'Ordre avant de choisir ses lunettes. »* C'était vrai et vérifiable : nous n'avons trouvé
> aucun site, aucune page sociale, aucun avis. Le message ci-dessous **ne le répète pas** — il passe
> directement à la page, et à ce qu'elle fait pour le patient.

**AVANT D'ENVOYER — le portique, dans cet ordre :**

1. **Déployer le dossier entier** `hosting/previews/laligne/` (`index.html` **et** `og.jpg`) — projet
   Vercel séparé, par exemple `laligne` ;
2. `python3 demos/build_laligne.py --url https://<adresse>` puis **redéployer** ;
3. vérifier **sur un téléphone** : FR par défaut, bascule EN, le dessin qui se trace, **les cinq onglets
   de visage** (ils doivent changer de panneau même sans JavaScript), un WhatsApp pré-rempli au
   **683 651 108**, aucun débordement horizontal ;
4. la carte du lien montre bien la vignette dessinée (1200×630), pas un carré vide.

---

## 1 · Le message (à copier tel quel, après la carte du lien)

```
Votre page est prête : <ADRESSE>

Elle part d'une idée simple, la vôtre : le visage d'abord, la monture ensuite.
Le patient choisit la forme de son visage (ovale, rond, carré, cœur, oblong),
voit la ligne de monture qui va avec — et le message WhatsApp part déjà écrit,
avec la forme qu'il pense avoir. Vous savez à quoi vous répondez avant même
d'ouvrir la conversation.

Elle explique aussi vos quatre gestes dans l'ordre : consultation, réfraction,
visagiste, conseil — et pour chacun, ce que le patient peut vous dire en arrivant.

Un mot franc : je n'ai rien inventé. Je n'ai trouvé aucun horaire, aucune marque,
aucun prix, aucune photo publiée — donc la page ne les écrit pas. Elle dit au
patient pourquoi ils se règlent sur WhatsApp, et elle est entièrement dessinée
(les visages, les montures) plutôt que d'emprunter des photos qui ne seraient pas
les vôtres.

Ce qu'il me manque pour la rendre complète : vos horaires, le repère exact à Akwa,
vos moyens de paiement, vos marques, et quelques photos de vos montures et de votre
boutique prises au téléphone. Envoyez-les et je les mets en ligne.

Ouvrez-la sur votre téléphone et dites-moi ce qui manque ou ce qui est faux.
— Akwo King / AMK – Développement Web & Solutions Digitales
```

**Pourquoi ce texte est écrit comme ça** (MESSAGES §1) : il ouvre sur **le fait nouveau pour elle**
(« Votre page est prête ») puis sur **son** idée ; le nom et le titre passent à la fin. Aucun prix, aucun
délai, aucune promesse de classement, aucun reproche — et la liste de ce qui manque est **courte**, parce
qu'on demande cinq choses, pas douze.

## 2 · Les douze informations qu'on attend (et qu'on ne devinera pas)

Elles vivent dans **`clients/la-ligne/a-completer.md`**, à recopier si le cabinet demande la liste :
**① les horaires · ② le repère exact à Akwa · ③ les moyens de paiement · ④ des photos (montures et
cabinet) · ⑤ les marques vendues · ⑥ veut-elle afficher des prix ? · ⑦ le délai habituel · ⑧ les verres et
options proposés · ⑨ ce qui est réparé sur place · ⑩ une seconde ligne ? · ⑪ une adresse e-mail ? ·
⑫ le nom exact à faire figurer.**

## 3 · Ce qu'on répond si elle pose une question

- **« Combien ça coûte ? »** → la grille est celle de King, jamais improvisée dans la conversation :
  remonter la question à King avant de donner un chiffre.
- **« Qui a fait ça ? »** → Akwo King / AMK, Douala. Le pied de page porte « Aperçu préparé par AMK pour
  La Ligne Optic » — c'est assumé.
- **« Pourquoi il n'y a aucune photo ? »** → parce qu'on ne fabrique pas la vitrine d'un opticien : les
  visages et les montures sont **dessinés**, et ses photos prendront leur place le jour même où elle les
  envoie.
- **« Pourquoi mes horaires n'y sont pas ? »** → parce qu'aucune source ne les donne ; la page dit
  qu'ils sont confirmés dans la conversation, et un mot suffira à les écrire.
- **« C'est quoi ce conseil de visagiste ? »** → c'est **son** service, écrit dans son annuaire ; la page
  en fait un vrai outil, avec cinq formes de visage et la ligne qui va avec.

## 4 · Après l'envoi

- La réponse se traite **dans l'heure** et s'écrit dans `sales/Activity-Log.md` avec l'heure et le mot
  exact (§34.1 : une réponse humaine arrête l'horloge).
- Si elle envoie les éléments : `python3 demos/build_laligne.py --url <adresse>` → **un seul
  redéploiement** → on lui renvoie la page complétée.
- Si elle ne répond pas : **aucune relance-reproche**. Le fil reste ouvert ; la page est à elle.
