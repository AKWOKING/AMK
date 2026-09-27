# UNI-LABO — « elle n'était pas vraiment intéressée par le site » : ce qu'elle a décrit, et ce qu'on ne sait pas

**Écrit le 27/09/2026**, d'après ce que King rapporte du rendez-vous du 25/09 à 13 h.
**État : analyse. Aucun code, aucun prix, aucune promesse, aucun message préparé.** Ce document existe pour
qu'on ne se lance pas dans la mauvaise chose — c'est exactement ce qu'il vient d'arriver avec le site.

---

## 1 · Ce que King rapporte, mot pour mot

> « unilabo also told us she wasn't really interested in the website she said she thought we had more to
> offer , she told us about the software they use ... in brief it's a software that enables them reduce
> errors in lab results; when one of the lab technicians finish the analysis and obtains the results, he
> types all the details into the software once that is done and save only a select few superiors can access
> the results through a code they have , once they input the code and see the results they crosscheck and
> verify that there is no error then they validate the results before sending it to the secretariat where it
> is then printed and sealed »

---

## 2 · Lecture : ce qu'elle a décrit est une **chaîne**, et elle a quatre temps

Sa description est précise — et ce n'est pas une demande, c'est **un état des lieux**. Les quatre temps,
tels qu'elle les a donnés :

| # | Qui | Ce qui se passe | Ce que ça protège |
|---|---|---|---|
| ① | **le technicien** | il termine l'analyse, obtient les résultats, **et les saisit** dans le logiciel, puis enregistre | la traçabilité de l'entrée |
| ② | **quelques supérieurs** | ils accèdent aux résultats **par un code**, qu'eux seuls ont | la confidentialité — le technicien ne diffuse pas |
| ③ | **le valideur** | il contrôle, vérifie qu'il n'y a **pas d'erreur**, puis **valide** | le contrôle qualité — c'est le moment le plus sérieux de la chaîne |
| ④ | **le secrétariat** | le résultat validé lui est transmis, il **imprime et scelle** | la remise au patient |

**Ce que cette description nous dit vraiment** : ce laboratoire **a déjà** un outil, et il tient précisément
les trois choses qu'un logiciel de laboratoire doit tenir — **l'accès restreint, la validation, la trace**.
Ils ne sont pas dans le vide. Ils sont **équipés**.

Et ça change tout, parce que ça veut dire que la phrase de King — « un logiciel qui leur permet de réduire
les erreurs dans les résultats » — décrit **ce qu'ils ont déjà**, pas ce qu'ils demandent.

---

## 3 · Le vide, et il est béant : **qu'est-ce qu'elle a demandé ?**

King rapporte deux choses d'elle :

1. **« elle n'était pas vraiment intéressée par le site »** — c'est un refus, et il est net ;
2. **« elle pensait qu'on avait plus à offrir »** — c'est une **ouverture**, pas une commande.

Puis elle a décrit **son** logiciel. On ne sait donc pas si elle :

- **(a)** veut qu'on **construise quelque chose comme ça** — un logiciel de validation de résultats, en mieux
  ou en moins cher que le leur ;
- **(b)** nous **expliquait que la partie numérique est déjà faite**, pour justifier le refus du site (« on
  n'a pas besoin d'une vitrine, on a déjà des outils ») ;
- **(c)** veut quelque chose **à côté** de leur logiciel — la remise du résultat au patient, la file
  d'attente, les rendez-vous, l'envoi des résultats par WhatsApp, les prélèvements à domicile…

**Ces trois lectures mènent à trois métiers différents, et deux d'entre eux ne sont pas les nôtres.** Écrire
une ligne de code avant de savoir laquelle est la bonne, c'est refaire l'erreur du site : construire une
belle chose que personne n'a demandée.

**La première question à lui poser n'est donc pas technique. C'est : « quels mots a-t-elle employés pour
dire ce qu'elle voulait ? »** S'il n'y en a pas eu — si elle a seulement décrit ce qu'ils ont — alors le
travail de la prochaine séance est de **qualifier**, pas de construire.

---

## 4 · Ce qui serait faisable — en trois zones, et il ne faut pas les mélanger

### Zone A — **le tour de contrôle du résultat** (sûre, utile, peu coûteuse)

Un outil **à côté** de leur logiciel, qui garde la trace de la chaîne : tel technicien a saisi à telle heure,
tel supérieur a ouvert avec son code à telle heure, tel valideur a validé à telle heure, le secrétariat a
reçu à telle heure. Un état, un journal, une alerte quand un résultat attend depuis trop longtemps.

**Ce qu'on ne fait pas dans la zone A :** on ne lit pas le contenu médical, on ne l'interprète pas, on ne
décide rien. On **constate** qu'un humain a validé. La phrase, à écrire sur le papier le jour où on vend ça :
**« le logiciel ne vérifie pas un résultat — il garde la trace de qui l'a vérifié. »**

Ce que ça vaut pour eux : le jour où un dossier est introuvable, où un résultat est resté trois heures sur
le bureau, ou qu'un inspecteur demande qui a validé quoi — la réponse existe, horodatée.

### Zone B — **la double saisie** (la douleur à qualifier, et la seule qui rapporte gros)

C'est la brique la plus intéressante de la description : **le technicien retape**. Il a le résultat sous les
yeux — souvent imprimé par un automate — et il le **recopie** dans le logiciel. C'est là que naissent les
erreurs de transcription, et c'est probablement ce que veut dire « réduire les erreurs ».

**Mais ça ne se fait que si les automates parlent.** Il faut savoir quels analyseurs ils ont et s'ils
sortent un **fichier** (port série, USB, export, HL7…) — ou si tout passe par du papier. Si les machines
produisent un fichier, la saisie manuelle disparaît et **la zone B devient la vraie vente**. Si tout est sur
papier, l'idée est morte et il vaut mieux le dire tout de suite que le découvrir à mi-parcours.

### Zone C — **à ne pas faire** (et à dire)

- **Un logiciel de laboratoire complet** (dossier patient, hébergement des résultats, historique médical) :
  c'est un autre métier, avec des obligations qui ne sont pas les nôtres ;
- **tout ce qui touche au contenu médical** : notre outil ne dit jamais « ce résultat est juste » ;
- **remplacer leur logiciel existant** : on se met **à côté**, jamais à la place. Casser un outil de
  laboratoire en service, c'est du sabotage, même involontaire ;
- **stocker des données de santé identifiantes** sans convention écrite. Le principe qui avait gagné pour
  l'essayage — *aucune photo ne quitte le téléphone* — s'écrit ici : **aucun résultat ne quitte leur
  machine**. Si nos outils n'en ont pas besoin, ils n'en gardent pas.

---

## 5 · Le risque qu'on ne peut pas ignorer

Un laboratoire d'analyses médicales, c'est **un service de santé**. Trois choses, à tenir du premier jour :

1. **La responsabilité ne se partage pas.** Si une erreur passe, ce n'est pas notre logiciel qui la valide —
   c'est un humain, avec son code. Notre trace protège **sa** décision, elle ne la remplace jamais. Toute
   interface qui donnerait l'impression du contraire est un défaut, pas une fonctionnalité.
2. **La confidentialité est réelle et elle est de leur côté.** Les résultats appartiennent aux patients et
   au laboratoire. Nous n'en détenons aucun. Si un jour il faut en manipuler, ce sera **écrit**, et jamais
   « en attendant ».
3. **Nous ne promettons pas « moins d'erreurs ».** On promet **une chaîne traçable** et, si les automates
   parlent, **une saisie en moins**. Le taux d'erreur est une conséquence, pas une garantie — et personne
   n'a le droit de la garantir à la place d'un biologiste.

---

## 6 · Les questions, dans l'ordre (et aucune ne porte sur le prix)

| # | Question | Ce qu'elle décide |
|---|---|---|
| 1 | **Quels mots avez-vous employés, quand vous avez dit que nous avions « plus à offrir » ?** | Est-ce qu'on qualifie, ou est-ce qu'on construit ? C'est la seule question qui compte aujourd'hui. |
| 2 | **Le logiciel que vous utilisez, qu'est-ce qui vous manque dedans ?** (Et : qui l'a fait, qui le maintient ?) | Un outil qu'on ne remplace pas se vend par ce qui lui manque. |
| 3 | **Les résultats arrivent d'où ?** De vos automates (lesquels ?), et sortent-ils un fichier ? | Décide la zone B : la fin de la double saisie, ou rien. |
| 4 | **Combien de résultats par jour, combien de techniciens, combien de valideurs, combien au secrétariat ?** | Décide la taille du travail — et si ce qui se vend vaut ce qu'on va dépenser. |
| 5 | **Qui décide, dans le laboratoire ?** Elle, ou un directeur qui n'était pas là ? | Un besoin qualifié avec quelqu'un qui ne signe pas est une conversation, pas un projet. |
| 6 | **Après le scellage, le résultat va où ?** Remis en main propre, envoyé, scanné ? | C'est là que se trouve le service suivant, celui que personne n'a encore proposé. |

**Ce qu'on ne dit pas encore :** ni prix, ni délai, ni « on peut faire ça ». Le 25/09, on a tenu cette règle
avec Univers. Elle vaut ici, et pour la même raison : **rien n'a été promis sur place, et c'est ce qui nous
laisse libres de proposer la bonne chose.**

---

## 7 · La règle de travail, la même qu'ailleurs

- **Un pilote, jamais un développement gratuit.** On construit **une** brique utile, dans **un** laboratoire,
  payée — assez petite pour être finie, assez vraie pour être montrée ailleurs.
- **Un produit, pas une commande sur mesure.** La campagne contient **beaucoup de laboratoires** (les labos
  de Douala sont dans nos fichiers depuis le 18/09). Le jour où une brique tient pour UNI-LABO, elle se
  revend — exactement comme l'outil d'essayage pour les opticiens. **Deux clients qui demandent la même
  chose, c'est un produit ; un client qui demande une chose, c'est une prestation.**
- **Une seule chose à la fois.** Univers a une preuve montrée (la planche d'essayage) ; on finit ce
  prototype-là avant d'ouvrir un deuxième chantier. Ici, on **qualifie**.

---

## 8 · Une conséquence immédiate, et elle coûte zéro

**Le redéploiement d'UNI-LABO n'est plus urgent.** Le formulaire de réservation manque sur la page en ligne
(`uni-labo.vercel.app`) : c'était l'action bloquante du 25/09, parce que la page devait correspondre à ce qui
a été vendu. **Puisqu'elle ne veut pas du site, on ne dépense plus une action dessus avant de savoir ce
qu'elle veut.** La page n'est pas perdue : comme celle d'Univers, elle peut devenir **la maison de la
nouvelle chose** — c'est-à-dire qu'on la redéploiera **le jour où il y aura quelque chose à y mettre**.

---

*Écrit par AMK le 27/09/2026. Sources : le message de King (rapport du rendez-vous du 25/09 à 13 h) et
`clients/uni-labo/AUDIT-2026-09-23.md`. Aucun fait n'a été ajouté à ce que King a rapporté.*
