# On ne dit pas à quelqu'un ce qu'il n'a pas avant d'avoir cherché tous ses noms

**Cas fondateur — ISEE, Douala, 26/10/2026.** Message parti à 15 h 15 : « aucune de ces deux vitrines ne
lui permet de vous joindre directement ». À 16 h, King ouvre `iseecameroon.com` : boutique WooCommerce
vivante depuis 2024, collections avec prix, **bouton WhatsApp sur chaque monture**, page « Prendre RDV »,
six assureurs en logo. Le prospect avait répondu « Bonjour » vingt-six minutes plus tôt.

## 1 · Pourquoi la recherche a échoué

Les deux noms cherchés étaient « ISEE » (tableau de l'Ordre) et « I See Better » (profil WhatsApp).
Le site s'appelle **Isee Cameroun**, et son domaine — `iseecameroon.com` — ne contient ni l'un ni l'autre.

Un cabinet de Douala porte en moyenne **trois à quatre noms** : celui du registre ONOC, celui du profil
WhatsApp, celui de la fiche Google, celui du site. Chercher un seul de ces noms, c'est chercher au
hasard.

## 2 · Les cinq voies obligatoires

Une phrase qui affirme l'absence de site n'est écrite qu'après ces cinq recherches, datées :

1. **nom exact** du registre (ONOC) ;
2. **nom affiché sur WhatsApp** — celui que le patient voit, pas celui du registre ;
3. **variantes** de graphie (« I See Better », « Isee Cameroon », « ISEE ») ;
4. **numéro de téléphone** entre guillemets — il apparaît souvent sur un site qui ne parle pas du nom ;
5. **Google Maps** : la fiche, le champ « Site web », et les photos.

Un seul de ces cinq qui rend un site **annule la phrase**. Le site existe : il n'y a plus rien à vendre
de ce côté-là, et c'est l'offre qui change (voir `sales/REPARATION-ISEE-2026-10-26.md` §3).

## 3 · La porte

`tools/qa/audit_outreach.py`, règle 11. Un message qui contient une affirmation d'absence (`aucun site`,
`pas de site`, `aucune de ces pages`, `ne mène nulle part`, `ne permet pas de vous joindre`…) doit porter
sous son titre :

```text
SITE-CHECK 2026-10-26 · nom exact, nom WhatsApp, variantes, numéro, Google Maps → aucun site
```

- sans ligne datée → **bloqué** ;
- avec une ligne qui dit « site trouvé » → **bloqué** aussi : si la recherche a rendu un site, le message
  ne peut pas dire le contraire.

La porte ne prouve pas que la recherche a eu lieu. Elle prouve qu'on a écrit **où** on a cherché et
**quand** — comme les portes A et B. C'est le maximum qu'un script puisse faire d'une vérification
manuelle ; le reste est la parole de celui qui envoie.

## 4 · Ce que ça change dans la façon d'écrire

Les messages sûrs ne parlent pas de ce qui **manque** au cabinet, mais de ce que le patient **ne trouve
pas là où il cherche** : « l'annuaire affiche 8 h à 18 h 30 mais pas les jours », « la fiche ne montre pas
vos examens de vue ». Ces faits-là se vérifient sur la page qu'on cite, et ils restent vrais même quand
le cabinet a un site ailleurs.

## 5 · L'offre, quand le site existe

Un cabinet avec un site vivant n'achète pas un site. Il achète : la **mise à jour** (le sien est figé
depuis novembre 2024), **l'unité du nom** (trois noms, trois endroits), et la **fiche Google**. C'est le
`Suivi` à 30 000 FCFA/mois (`knowledge/PRIX-2026-10-24.md` §5), pas le `Présence` à 150 000. Proposer le
second à qui a déjà le premier, c'est insulter son travail et perdre la conversation.

## 6 · Ce que ce document ne prouve pas

Que la réparation réussisse : un cabinet à qui on avoue une erreur peut ne jamais répondre. Et il ne
remplace pas la vérification du jour : `iseecameroon.com` sera peut-être mort dans six mois.
