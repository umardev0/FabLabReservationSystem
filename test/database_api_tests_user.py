'''
Database interface for checking the tables been created correctly.
@authors: PWP-20
Code of Ivan and Mika provided in Programmable Web Project exercise _ University of Oulu
is been utilized. 

'''

import unittest, sqlite3
import fablab.database as database


#Path to the database file, different from the deployment db
DB_PATH = 'db/fablab_test.db'
ENGINE = database.Engine()


#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
USER1_USERNAME = 'user1'
USER1_ID = 1
USER1 = {'userID': USER1_ID ,
         'username': USER1_USERNAME,'passwrod': 23459,
		 'email':'adcd@gmail.com','mobile': '012345678',
         'isAdmin': 1,'createdAt': 1362015937,
         'UpdatedAt': 1362015937, 'createdBy':  2, 
         'updatedBy`': 2 
         }
USER1 = {'userID': USER1_ID ,
         'username': USER1_USERNAME,'passwrod': 23459,
		 'email':'efcj@gmail.com','mobile': '012345678',
         'isAdmin': 1,'createdAt': 1362015937,
         'UpdatedAt': 1362015937, 'createdBy': 'New York', 
         'updatedBy`': 2
         }
USER2_USERNAME = 'user2'
USER2_ID = 5
USER1 = {'userID': USER2_ID ,
          'username': USER1_USERNAME,'passwrod': 23459,
		  'email':'adcd@gmail.com', 'mobile': '012345678',
          'isAdmin': 1, 'createdAt': 1362015937,
          'UpdatedAt': 1362015937, 'createdBy':  2, 
          'updatedBy`': 2 
         }
NEW_USER_USERNAME = 'user10'
NEW_USER = {'username': NEW_USER_USERNAME,
			'passwrod': 23459,
			'email':'adcd@gmail.com','mobile': '012345678',
			'isAdmin': 1,'createdAt': 1362015937,
			'UpdatedAt': 1362015937, 'createdBy':  2, 
			'updatedBy`': 2 
         }
USER_WRONG_USERNAME = 'user11'
INITIAL_SIZE = 10



class UserDBAPITestCase(unittest.TestCase):
    connection = ENGINE.connect()
    '''
    Test cases for the Users related methods.
    '''
    #INITIATION AND TEARDOWN METHODS
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
          self.connection = ENGINE.connect() #problem

        except Exception as e: 
        #For instance if there is an error while populating the tables
          ENGINE.clear()


    def tearDown(self):
        '''
        Close underlying connection and remove all records from database
        '''
		
        self.connection.close()
        ENGINE.clear()

    def test_users_table_created(self):
        '''
        Checks that the table initially contains 1 users (check
        forum_data_dump.sql). 
        '''
        print('('+self.test_users_table_created.__name__+')', \
              self.test_users_table_created.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM users'
        #Connects to the database.
        con = self.connection.con
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query1)
            users = cur.fetchall()
            #Assert
            self.assertEqual(len(users), INITIAL_SIZE)
           

    def test_create_user_object(self):
        '''
        Check that the method create_user_object works and two dictionaries have the same values
        for the first database row. 
        '''
        print('('+self.test_create_user_object.__name__+')', \
              self.test_create_user_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT users.* FROM users'
        #Get the sqlite3 con from the Connection instance
        con = self.connection.con
        #I am doing operations after with, so I must explicitly close the
        # the connection to be sure that no locks are kepts. The with, close
        # the connection when it has gone out of scope
        #try:
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
    #finally:
        #    con.close()
        #Test the method
        user = self.connection._create_user_object(row)
        self.assertDictEquals(user, USER1)

    def test_get_user(self):
        '''
        Test get_user with id user1 and user2
        '''
        print('('+self.test_get_user.__name__+')', \
              self.test_get_user.__doc__)

        #Test with an existing user
        user1 = self.connection.get_user(USER1_USERNAME)
        self.assertDictEquals(user1, USER1)
        user2 = self.connection.get_user(USER2_USERNAME)
        self.assertDictEquals(user2, USER2)

    def test_get_user_noexistingid(self):
        '''
        Test get_user with  msg-20 (no-existing)
        '''
        print('('+self.test_get_user_noexistingid.__name__+')', \
              self.test_get_user_noexistingid.__doc__)

        #Test with an existing user
        user = self.connection.get_user(USER_WRONG_USERNAME)
        self.assertIsNone(user)

    def test_get_users(self):
        '''
        Test that get_users work correctly and extract required user info
        '''
        print('('+self.test_get_users.__name__+')', \
              self.test_get_users.__doc__)
        users = self.connection.get_users()
        #Check that the size is correct
        self.assertEqual(len(users), INITIAL_SIZE)
        #Iterate through users and check if the users with USER1_ID and
        #USER2_ID are correct:
        for user in users:
            if user['username'] == USER1_USERNAME:
                self.assertDictEqual(user, USER1)
            elif user['username'] == USER2_USERNAME:
                self.assertDictEqual(user, USER2)

    def test_delete_user(self):
        '''
        Test that the user1 is deleted
        '''
        print('('+self.test_delete_user.__name__+')', \
              self.test_delete_user.__doc__)
        resp = self.connection.delete_user(USER1_USERNAME)
        self.assertTrue(resp)
        #Check that the users has been really deleted thorough a get
        resp2 = self.connection.get_user(USER1_USERNAME)
        self.assertIsNone(resp2)
        

    def test_delete_user_noexistingnickname(self):
        '''
        Test delete_user with  user11 (no-existing)
        '''
        print('('+self.test_delete_user_noexistingnickname.__name__+')', \
              self.test_delete_user_noexistingnickname.__doc__)
        #Test with an existing user
        resp = self.connection.delete_user(USER_WRONG_USERNAME)
        self.assertFalse(resp)


    def test_not_contains_user(self):
        '''
        Check if the database does not contain users with id user11
        '''
        print('('+self.test_contains_user.__name__+')', \
              self.test_contains_user.__doc__)
        self.assertFalse(self.connection.contains_user(USER_WRONG_USERNAME))

    def test_contains_user(self):
        '''
        Check if the database contains users with username user1 and user2
        '''
        print('('+self.test_contains_user.__name__+')', \
              self.test_contains_user.__doc__)
        self.assertTrue(self.connection.contains_user(USER1_USERNAME))
        self.assertTrue(self.connection.contains_user(USER2_USERNAME))

   

if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
