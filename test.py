import fablab.database as database
engine = database.Engine()
engine.clear()
engine.populate_tables()

con = engine.connect()
test = con.get_reservation(1)
println(test)