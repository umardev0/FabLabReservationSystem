import fablab.database as database
engine = database.Engine()
con = engine.connect()
con.check_foreign_keys_status()
#message = con.get_machine("machine-1")
#print(message)
messages = con.create_reservation(1, 1, 151943330 , 151945330, 1)


print(messages)