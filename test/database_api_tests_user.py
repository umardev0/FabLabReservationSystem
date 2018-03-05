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
ENGINE = database.Engine(DB_PATH)


#CONSTANTS DEFINING DIFFERENT USERS AND USER PROPERTIES
USER_ADMIN_ID = 0
USER_ADMIN_USERNAME = 'admin'
USERAdmin = {'userID': USER_ADMIN_ID ,
         'username': USER_ADMIN_USERNAME , 'password':'adminpassword',
         'email':'admin@fablab.oulu.fi', 'mobile': '0414868685',
         'website': 'https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space',
         'isAdmin': '1','createdAt': 1519472330,
         'updatedAt': None
         }
USERAdmin_listobject = {'userID': USER_ADMIN_ID ,
                        'username': USER_ADMIN_USERNAME}
USER1_USERNAME = 'user1'
USER1_ID = 1


USER1 = {'userID': USER1_ID ,
         'username': USER1_USERNAME,
         'password': 'user1password',
         'email':'user1@fablab.oulu.fi',
         'mobile': '0414868688',
         'website': 'https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space',
         'isAdmin': '1',
         'createdAt': 1519472333,
         'updatedAt': 1519474333 
         }
USER1_listobject = {'userID': USER1_ID ,
                    'username': USER1_USERNAME}
M_USER1= {'userID': USER1_ID ,
          'username': USER1_USERNAME,'password': 'muser1password',
         'email': 'muser1@fablab.oulu.fi','mobile': '12345678',
         'website': 'https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space',
         'isAdmin': '1',
         'createdAt': 1519472333,
         'updatedAt': 1519474333}
USER2_USERNAME = 'user2'
USER2_ID = 2
USER2 = {'userID': USER2_ID ,
         'username': USER2_USERNAME,
         'password': 'user2password',
         'email':'user2@fablab.oulu.fi', 
         'mobile': '0414868688',
         'website': 'https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space',
         'isAdmin': '0', 
         'createdAt': 1519473318,
         'updatedAt': None
        }
USER2_listobject = {'userID': USER2_ID ,
                    'username': USER2_USERNAME}
NEW_USER_USERNAME = 'user10'
NEW_USERID = 10
NEW_USER = {'userID': NEW_USERID ,
            'username': NEW_USER_USERNAME, 'password': 'user10password',
            'email':'user10@fablab.oulu.fi','mobile': '012345678',
            'website': 'https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space',
            'isAdmin': '0', 'createdBy': 1, 
            }
USER_WRONG_USERNAME = 'user11'
INITIAL_SIZE = 10



class UserDBAPITestCase(unittest.TestCase):

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
        Checks that the table initially contains 10 users (check
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
        Check that the method create_user_object correctly, Checks whether the two dictionaries of user object 
        have the same values 
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
        
        #Test the method
        user = self.connection._create_user_object(row)
        #Test the method with correct user data dictionary 
        self.assertDictEqual(user, USERAdmin )

    def test_create_user(self):
        '''
         Check that the method creates user correctly 
        '''
        print('('+self.test_create_user.__name__+')', \
              self.test_create_user.__doc__)
        userid = self.connection.create_user(NEW_USER_USERNAME,'user10password','user10@fablab.oulu.fi','012345678','https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space','0','0')
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
            #Extrac the last row id
            row = cur.lastrowid
         #test the method with newly added userid
        self.assertEqual(row,userid)

    def test_create_users_list_object(self):
        '''
        Check the method that user list object is created correctly
        Checks whether list object dictionaries have the same values
        '''
        print('('+self.test_create_users_list_object.__name__+')', \
              self.test_create_users_list_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT users.* FROM users'
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
            #Extrac the row
            row = cur.fetchone()

        #Test the method
        user = self.connection._create_user_list_object(row)
        #Test the method with correct user list object data dictionary  
        self.assertDictEqual(user, USERAdmin_listobject )
    def test_get_user(self):
        '''
        Test get_user with user name user1_username and user2_username,
        whether the method get_user getting the users correctly
        '''
        print('('+self.test_get_user.__name__+')', \
              self.test_get_user.__doc__)

        #Test with an existing user
        user1 = self.connection.get_user(USER1_USERNAME)
        self.assertDictEqual(user1, USER1)
        user2 = self.connection.get_user(USER2_USERNAME)
        self.assertDictEqual(user2, USER2)

    def test_get_user_noexistingusername(self):
        '''
        Test get_user with (no-existing) user_name
        '''
        print('('+self.test_get_user_noexistingusername.__name__+')', \
              self.test_get_user_noexistingusername.__doc__)

        #Test with an non-existing user_name
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
        #Iterate through users and check if the users with USER1_USERNAME and
        #USER2_USERNAME are extract correctly:
        for user in users:
            if user['username'] == USER1_USERNAME:
                self.assertDictEqual(user,USER1_listobject)
            elif user['username'] == USER2_USERNAME:
                self.assertDictEqual(user, USER2_listobject)
    def test_get_users_nonexistingusername(self):
        '''
        Test get_users work correctly and do not extract the non-existing user name
        '''
        print('('+self.test_get_users_nonexistingusername.__name__+')', \
              self.test_get_users_nonexistingusername.__doc__)
        users = self.connection.get_users()
        #Check that the size is correct
        self.assertEqual(len(users), INITIAL_SIZE)
        #Iterate through users and check  the users and try to find the user name that do not exist
        #check if response in None:
        for user in users:
            if user['username'] == USER_WRONG_USERNAME:
                resp = user['username']

                self.assertIsNone(resp)
    def test_delete_user(self):
        '''
        Test that the user2 is deleted
        '''
        print('('+self.test_delete_user.__name__+')', \
              self.test_delete_user.__doc__)
        #check the user deleted correctly and delete user method working correctly
        resp = self.connection.delete_user(USER2_USERNAME)
        self.assertTrue(resp)
        #Check that the users has been really deleted thorough a get
        resp2 = self.connection.get_user(USER2_USERNAME)
        self.assertIsNone(resp2)

    def test_delete_user_noexistingusername(self):
        '''
        Test delete_user with  user11 (no-existing user-name)
        '''
        print('('+self.test_delete_user_noexistingusername.__name__+')', \
              self.test_delete_user_noexistingusername.__doc__)
        #Test with an non-existing user-name, 
        resp = self.connection.delete_user(USER_WRONG_USERNAME)
        #Confirm whether the delete user is deleting the wrong user
        self.assertFalse(resp)

    def test_changerole_user(self):
        '''
        Check if the role of user with username user1 is changing 
        '''
        print('('+self.test_changerole_user.__name__+')', \
              self.test_changerole_user.__doc__)
              
        #Change user role with method
        user = self.connection.change_role_user(USER1_USERNAME,0,0)
        #test the role is changed 
        userobj = self.connection.get_user(user)
        self.assertEqual(userobj['isAdmin'],'0')

    def test_changerole_nonexistingusername(self):
        '''
        Check if the role of user method with nonexistingusername user11 
        '''
        print('('+self.test_changerole_nonexistingusername.__name__+')', \
              self.test_changerole_nonexistingusername.__doc__)
              
        #test the role is changed for nonexisting username
        resp = self.connection.change_role_user(USER_WRONG_USERNAME,0,0)
        self.assertIsNone(resp)

    def test_modify_user(self):
        '''
        Test that the user user1 is modifying correctly
        '''
        print('('+self.test_modify_user.__name__+')', \
              self.test_modify_user.__doc__)
        #Get the modified user
        user = self.connection.modify_user(USER1_USERNAME,'muser1password','muser1@fablab.oulu.fi','12345678','https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space','0')
        self.assertEqual(user, USER1_USERNAME)
        #Check that the users has been really modified through a get
        resp2 = self.connection.get_user(user)
        
        #Check the expected values
        
        self.assertEqual(M_USER1['password'], resp2['password'])
        self.assertEqual(M_USER1['email'], resp2['email'])
        self.assertEqual(M_USER1['mobile'], resp2['mobile'])
        self.assertEqual(M_USER1['email'], resp2['email'])
        self.assertEqual(M_USER1['website'], resp2['website'])

    def test_modify_user_noexistingusername(self):
        '''
        Test modify_user with  user11(no-existing)
        '''
        print('('+self.test_modify_user_noexistingusername.__name__+')', \
              self.test_modify_user_noexistingusername.__doc__)
        #Test with an non-existing user name
        resp = self.connection.modify_user(USER_WRONG_USERNAME,'muser1password','muser1@fablab.oulu.fi','12345678','https://wiki.oulu.fi/display/FLOWS/Fab+Lab+Oulu+Wiki+Space','0' )
        self.assertIsNone(resp)

if __name__ == '__main__':
    print('Start running user tests')
    unittest.main()
