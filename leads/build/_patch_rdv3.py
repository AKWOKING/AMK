import pathlib

p = pathlib.Path("leads/build/crm.py")
t = p.read_text(encoding="utf-8")

i = t.index('    dict(slug="uni-labo-bonamoussadi"')
end = t.index('→ parked."),', i) + len('→ parked."),')

NEW = '''    dict(slug="uni-labo-bonamoussadi", org="UNI-LABO",
         city="Douala (Bonamoussadi, Carrefour Etoo)", language="FR/EN",
         org_type="lab", wa_number="696 13 98 19", wa_verified="yes",
         contact_channel="WhatsApp", source="directory",
         source_detail="Remote-Sweep section C - Lun-Ven 07h-19h, Sam 07h-13h",
         contacted="Yes", reply="YES 19/09 20:20 - demande de RENDEZ-VOUS",
         demo="Yes", last_send_state="sent", follow_ups_sent="0",
         stage="offer", reply_type="human",
         notes="DEMANDE DE RENDEZ-VOUS - LE PLUS FORT SIGNAL DE LA CAMPAGNE. "
               "Le 19/09 a 20:20, UNI-LABO a ecrit, mot pour mot : « Bsr. Peut on prendre un rendez vous "
               "pour vendredi pour que vous nous presentez vos services? » "
               "Ce n est plus « je vous reviens » : c est une INVITATION. Premier prospect de la "
               "campagne qui demande a nous voir. RENDEZ-VOUS = VENDREDI 25/09. "
               "ATTENTION : LE SITE EST DEJA CONSTRUIT ET EN LIGNE (https://uni-labo.vercel.app) - "
               "la presentation des services se fera donc sur LEUR PROPRE site, ouvert sur un telephone. "
               "C est une seance de CLOTURE, pas un premier contact. Prix a poser : 100 000 FCFA, 50/50. "
               "Ce qui rend ce lead unique : il avait ecrit « Bsr » le 18/09 a 20:57, nous avons envoye "
               "le lien a 21:47 puis 22:05, et il est revenu DE LUI-MEME 24 h plus tard. "
               "Message 1 envoye le 18/09 a 18:41 (2 coches)."),'''

t = t[:i] + NEW + t[end:]
p.write_text(t, encoding="utf-8")
print("entree UNI-LABO remplacee en entier")
