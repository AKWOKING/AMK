import pathlib

p = pathlib.Path("leads/build/crm.py")
t = p.read_text(encoding="utf-8")

OLD = '"labiomed-deido":              ("lu", "19:32", "Lu. Maquette déjà prête."),'
NEW = ('"labiomed-deido":              ("lu", "19:32",\n'
       '                                    "***A REPONDU Oui a 19:43 - 11 minutes apres notre message. '
       'PREMIER OUI DE LA CAMPAGNE.*** Apercu + texte envoyes 20:02 SANS le prix (decision de King : '
       'le prix va avec un lien). Demo complete construite : hosting/previews/labiomed/ - a deployer '
       'puis envoyer avec le prix (100 000 FCFA, 50/50)."),')

assert OLD in t, "ligne labiomed introuvable"
t = t.replace(OLD, NEW, 1)

# un lead qui a dit OUI est une réponse en attente : on le note dans le CRM
OLD2 = 'def _apply_envois(out: list) -> None:\n    by = {r.get("slug"): r for r in out}'
NEW2 = ('def _apply_envois(out: list) -> None:\n'
        '    by = {r.get("slug"): r for r in out}\n'
        '    # un « Oui » est une reponse HUMAINE : on la pose AVANT la boucle generique,\n'
        '    # sinon le tuple de ENVOIS_1909_SOIR la remettrait a « none ».\n'
        '    _oui = by.get("labiomed-deido")\n'
        '    if _oui is not None:\n'
        '        _oui["Reply"] = "YES 19/09 19:43 - \\"Oui\\" (verbatim). PREMIER OUI DE LA CAMPAGNE."\n'
        '        _oui["reply_type"] = "human"')
assert OLD2 in t
t = t.replace(OLD2, NEW2, 1)

# ne pas ecraser le "Oui" avec "none"
OLD3 = '        r["reply_type"] = "auto" if etat == "auto-reponse" else "none"'
NEW3 = ('        if not str(r.get("Reply", "")).strip().lower().startswith("yes"):\n'
        '            r["reply_type"] = "auto" if etat == "auto-reponse" else "none"')
assert OLD3 in t
t = t.replace(OLD3, NEW3, 1)

p.write_text(t, encoding="utf-8")
print("CRM : le Oui de Labiomed est enregistre")
