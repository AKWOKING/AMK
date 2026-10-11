# VAGUE 2026-10-12 — LISTE VÉRIFIÉE (opticiens froids) · 11/10 au soir

**Mandat (King, 11/10) :** vérifier chaque opticien **froid** de la vague. **Bali est hors vague — non
vérifié ici.** Tout prospect marqué **unverified** n'envoie pas lundi. Trié par statut :
confirmé → divergent → unverified.

**Sources primaires, relues ce soir (11/10) via `fetch_page` :**
- Annuaire ONOC par région (LITTORAL) : `https://onocameroun.com/annuaire-des-opticiens-par-region/`
  — c'est la source qui **gagne** (ruling 11/10 : « l'annuaire gagne »).
- « Liste des inscrits au tableau » : `https://onocameroun.com/liste-de-tous-les-opticiens-inscrits-au-tableau/`
  — source du **second numéro** sur les lignes divergentes (capture 11/10, `sales/LISTE-OPTICIENS-2026-10.md`).

**Note méthode :** le `curl` du bac à sable est bloqué sur `onocameroun.com` (HTTP 000) ; la lecture
passe par l'outil de page. Les quartiers **ne figurent pas dans l'annuaire** — ils sont repris de nos
journaux de recherche quand ils y sont, sinon marqués **NON SOURCÉ** (ne pas personnaliser).

---

## STATUT : CONFIRMÉ (annuaire = fichier, et « inscrits » concorde) — envoi lundi OK

| Opticien (M./Mme + nom) | Cabinet (exact) | Quartier | N° ONOC (insc. · arrêté) | Téléphone | Source | Divergence |
|---|---|---|---|---|---|---|
| M. Siméon Djeumo Feunou | **Horizon optique** | Akwa *(DoualaTour)* | 032 · En cours (#100) | 677 44 74 17 | annuaire #100 · quartier `Send-BATCH-2026-09-24-Opticiens-2.md` | ✅ aucune |
| M. Jean Dury Makongo | **Planète Optique** | NON SOURCÉ | 35 · En cours (#121) | 699 85 58 35 | annuaire #121 | ✅ aucune |
| Mme Hélène Manfo épse Jounda | **Maff Optique Sarl** | Bonadibong *(repère de quartier)* | 70 · 6676 (#123) | 699 93 19 56 | annuaire #123 · quartier `Activity-Log.md` / ayilaa.com | ✅ aucune |
| M. Armstrong Tuambi Nzikang | **Lumumba OpticMedical** *(remplaçant)* | ⚠️ Makepe ↔ Bonamoussadi — **conflit interne, ne pas personnaliser** | 054/2018 · 6677 (#144) | 670 59 79 96 | annuaire #144 · conflit `Activity-Log.md` 3889 vs 3987 | ✅ ONOC OK · quartier en conflit |

## STATUT : DIVERGENT (annuaire = fichier, mais « inscrits » diffère) — envoi lundi sur le n° ANNUAIRE ; si WhatsApp ne livre pas / ne répond pas, tester le second n° AVANT de classer (jamais 2ᵉ envoi même numéro)

| Opticien (M./Mme + nom) | Cabinet (exact) | Quartier | N° ONOC (insc. · arrêté) | Téléphone (annuaire) | 2ᵉ n° (« inscrits ») | Écart |
|---|---|---|---|---|---|---|
| Mme Hermine Boudzap Zoyem | **Faby Optique** | NON SOURCÉ | 118/2017 · 0082 (#99) | 692 08 00 55 | 672 55 21 37 | numéro **+** année (2017 vs 2021) **+** orthographe (Boudzap vs Bouzap) |
| Mme Pierrette Lotie Elise Lipoth | **JiredOptic Med** | NON SOURCÉ | 116 · 0060 (#120) | 696 26 50 31 | 695 62 66 32 | numéro |
| Mme Honorine Judith Makouo Kamokwe | **KamaïsOptic** | Bonanjo *(Activity-Log)* | 112 · 1394 (#122) | 690 57 82 27 | 699 57 82 27 | préfixe 690 vs 699 |
| M. Jean Zobo | **Centrale Optique** | NON SOURCÉ | 044/2020 · En cours (#145) | 693 96 89 56 | 699 59 82 86 | numéro **+** nom (Zobo vs Zogo) |

## STATUT : UNVERIFIED — **aucun**

Aucun des 8 (7 froids + 1 remplaçant) n'est sans ligne ONOC. **Personne n'est bloqué pour lundi** sur ce
critère. (Bali, hors vague, serait « unverified » : aucune ligne « L'Opticien Bali SARL » dans
l'annuaire — son n° 670 27 60 65 y figure sous « Optic-Swiss Sarl » #107.)

---

## Règles de sortie (standing)

- **L'annuaire gagne** : le numéro d'envoi est celui de l'annuaire (# colonne Téléphone).
- Divergent ≠ bloqué : envoi sur l'annuaire ; **second numéro seulement si silence / non-livraison**,
  jamais un deuxième envoi sur le même numéro (règle 02/10).
- Quartier **NON SOURCÉ** → King **ne personnalise pas** [quartier] pour ce prospect (le gabarit tient
  sans). Quartier en conflit (Lumumba) → ne pas personnaliser tant que non résolu.
- Ne jamais mentionner l'inscription à l'Ordre dans l'opener sans source pour CE cabinet
  (`content/strategy/RULE-CREDENTIAL-CLAIMS.md`).
