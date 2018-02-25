'''
Database interface for checking the tables are been creating correctly.
@authors: PWP-20
Code of Ivan and Mika provided in Programmable Web Project exercise _ University of Oulu
is been utilized. 

'''

import sqlite3, unittest, collections

from fablab import database

#Path to the test database file, It is different from the deployment db
DB_PATH = 'db/forum_test.db'
ENGINE = database.Engine(DB_PATH)

INITIAL_SIZE = 1

class TestCaseCreatedTables(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ''' Creates the database structure. Removes first any preexisting
            database file
        '''
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        '''Remove the testing database'''
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        '''
        Populates the database
        '''
        try:
          #This method load the initial values from forum_data_dump.sql
          ENGINE.populate_tables()
          #Creates a Connection instance to use the API
          self.connection = ENGINE.connect()
        except Exception as e: 
        #For instance if there is an error while populating the tables
          ENGINE.clear()

    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
        self.connection.close()
        ENGINE.clear()

    def test_machine_table_schema(self):
        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('machines'))

            # collect names in a list
            result = c.fetchall()
            attributenames = [tup[1] for tup in result]
            attributetypes = [tup[2] for tup in result]
            names=['machineID','machinename','typeID','tutorial','createdAt','updatedAt','createdBy','updatedBy']
            types=['INTEGER','TEXT','INTEGER','TEXT','INTEGER','INTEGER','INTEGER']  
            self.assertEquals(names, names)    
            self.assertEquals(types, types) 

            #foreign key to check, whether they are correctly set
   
            foreign_keys =[('machinetypes','typeID','typeID')]
            c.execute('PRAGMA FOREIGN_KEY_LIST({})'.format('messages'))
            result = c.fetchall()
            result_filtered = [(tup[2],tup[3],tup[4]) for tup in result]
            for tup in result_filtered:
                self.assertIn(tup,foreign_keys)
  
    def test_machine_table_created(self):
        '''
        Checks that the table initially contains 1 machines (check
        forum_data_dump.sql). 
        
        '''
        print('('+self.test_machine_table_created.__name__+')', \
                  self.test_machine_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM machines'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            machines = cur.fetchall()
            #Assert
            self.assertEqual(len(machines), INITIAL_SIZE)

    
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)	

    def test_machinetypes_table_schema(self):
         
         con = self.connection.con
         with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('machinetypes'))

            # collect names in a list
            result = c.fetchall()
            attributenames = [tup[1] for tup in result]
            attributetypes = [tup[2] for tup in result]
            names=['typeID','typeName','typeFullname','pastProject','createdAt','updatedAt','createdBy','updatedBy']
            types=['INTEGER','TEXT','TEXT','TEXT','INTEGER','INTEGER','INTEGER','INTEGER']  
            self.assertEquals(names, names)    
            self.assertEquals(types, types) 
  
  
    def test_machinetypes_table_created(self):
        '''
        Checks that the table initially contains 1 machine type (check
        forum_data_dump.sql). 
        '''
        print('('+self.test_user_table_created.__name__+')', \
                  self.test_user_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM machinetypes'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)

    def test_user_table_schema(self):
        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('users'))

            # collect names in a list
            result = c.fetchall()
            attributenames = [tup[1] for tup in result]
            attributetypes = [tup[2] for tup in result]
            names=['userID','username','password','email','mobile','website','isAdmin','createdAt','createdAt','createdBy','updatedBy']
            types=['INTEGER','TEXT','NUMERIC','TEXT','TEXT','TEXT','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER']  
            self.assertEquals(names, names)    
            self.assertEquals(types, types) 

           

  
    def test_user_table_created(self):
        '''
        Checks that the table initially contains 1 user (check
        forum_data_dump.sql). 
        
        '''
        print('('+self.test_user_table_created.__name__+')', \
                  self.test_user_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()



    def test_messages_table_schema(self):

        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('messages'))

            # collect names in a list
            result = c.fetchall()
            names = [tup[1] for tup in result]
            types = [tup[2] for tup in result]
            attributenames=['messageID','fromUserID','toUserID','content','createdAt']
            attributetypes=['INTEGER','INTEGER','INTEGER','TEXT','INTEGER']  
            self.assertEquals(names, names)    
            self.assertEquals(types, types) 

           # add foreign key check
            foreign_keys =[('users','fromUserID','userID'),('users','toUserID','userID')]
            c.execute('PRAGMA FOREIGN_KEY_LIST({})'.format('messages'))
            result = c.fetchall()
            result_filtered = [(tup[2],tup[3],tup[4]) for tup in result]
            for tup in result_filtered:
                self.assertIn(tup,foreign_keys)
  
    def test_messages_table_created(self):
        '''
        Checks that the table initially contains 1 messages (check
        forum_data_dump.sql). 
        
        '''
        print('('+self.test_user_table_created.__name__+')', \
                  self.test_user_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)	

    def test_reservation_table_schema(self):
        con = self.connection.con
        with con:
            c = con.cursor()

            # Retrieve column information
            # Every column will be represented by a tuple with the following attributes:
            # (id, name, type, notnull, default_value, primary_key)
            c.execute('PRAGMA TABLE_INFO({})'.format('reservations'))

            # collect names in a list
            result = c.fetchall()
            attributenames = [tup[1] for tup in result]
            attributetypes = [tup[2] for tup in result]
            names=['reservationID','userID','machineID','startTime','endTime','isActive','createdAt','createdAt','createdBy','updatedBy']
            types=['INTEGER','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER','INTEGER']  
            self.assertEquals(names, names)    
            self.assertEquals(types, types) 

           # add foreign key check
            foreign_keys =[('machines','machineID','machineID'),('users','userID','userID')]
            c.execute('PRAGMA FOREIGN_KEY_LIST({})'.format('messages'))
            result = c.fetchall()
            result_filtered = [(tup[2],tup[3],tup[4]) for tup in result]
            for tup in result_filtered:
                self.assertIn(tup,foreign_keys)
  
    def test_reservation_table_created(self):
        '''
        Checks that the table initially contains 1 reservations (check
        forum_data_dump.sql). 
        
        '''
        print('('+self.test_user_table_created.__name__+')', \
                  self.test_user_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM reservations'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            resevre = cur.fetchall()
            #Assert
            self.assertEqual(len(resevre), INITIAL_SIZE)

    def connection(self)
           return self.DB_PATH	
    
    

if __name__ == '__main__':
    print('Start running database tests')
    unittest.main();


