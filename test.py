import fablab.database as database
engine = database.Engine()
con = engine.connect()
con.check_foreign_keys_status()
#message = con.get_machine("machine-1")
#print(message)
messages = con.create_user("neqddw", "33333",None, None, None, 1, 1)

print(messages)