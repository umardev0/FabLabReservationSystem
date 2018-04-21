import fablab.database as database
engine = database.Engine()
engine.create_tables()
engine.populate_tables()

con = engine.connect()
test = con.get_reservation(1)
print(test)