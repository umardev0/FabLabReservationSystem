import fablab.database as database
engine = database.Engine()
con = engine.connect()
con.check_foreign_keys_status()
#message = con.get_machine("machine-1")
#print(message)
con.modify_machine("machine-1","test_moddified",1,"",2)
messages = con.get_user('dana')

print(messages)