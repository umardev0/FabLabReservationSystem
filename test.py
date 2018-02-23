import fablab.database as database
engine = database.Engine()
con = engine.connect()
con.check_foreign_keys_status()
#message = con.get_machine("machine-1")
#print(message)
con.modify_machine("machine-2","test_moddified",1,None)
messages = con.get_machines()

con.create_machine("AAA", 1, "NONE", 2)
machine = con.get_machines()
print(machine)