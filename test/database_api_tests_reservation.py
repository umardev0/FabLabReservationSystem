import sqlite3, unittest
from fablab import database


#Path to the database file, different from the deployment db
DB_PATH = 'db/fablab_test.db'
ENGINE = database.Engine(DB_PATH)
ENGINE.remove_database()
ENGINE.create_tables()
ENGINE.populate_tables()


RESERVATION1_ID = 'reservation-001'
RESERVATION1 = {'reservationID': 1, 'reservationname': 'Stratasys 380mc',
'typeID': 1, 'tutorial': 'www.google.com',
'createdAt': 1519472221, 'updatedAt': None,
'createdBy': 0, 'updateBy': None}

RESERVATION2_ID = 'reservation-002'
RESERVATION2 = {'reservationID': 2, 'reservationname': 'Formlabs Form 2',
'typeID': 1, 'tutorial': 'www.google.com',
'createdAt': 1519472221, 'updatedAt': 1519472221,
'createdBy': 0, 'updateBy': 1}

RESERVATION1_MODIFIED = {'reservationID': 1, 'reservationname': 'Roland CAMM-1 GS-25',
'typeID': 5, 'tutorial': 'www.yahoo.com'}

WRONG_reservationID = 'reservation-10'
INITIAL_SIZE = 7

class MachineDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Machines related methods.
    '''

    #Creates a Connection instance to use the API
    connection = ENGINE.connect()

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
            #This method load the initial values from fablab_data_dump.sql
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

    def test_reservations_table_created(self):
        '''
        Checks that the table initially contains 5 reservations (check
        fablab_data_dump.sql). NOTE: Do not use Connection instance but
        call directly SQL.
        '''
        print('('+self.test_reservations_table_created.__name__+')', \
                  self.test_reservations_table_created.__doc__)
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
            reservations = cur.fetchall()
            #Assert
            self.assertEqual(len(reservations), INITIAL_SIZE)

    def test_create_reservation_object(self):
        '''
        Check that the method _create_reservation_object works return adequate
        values for the first database row. NOTE: Do not use Connection instace
        to extract data from database but call directly SQL.
        '''
        print('('+self.test_create_reservation_object.__name__+')', \
              self.test_create_reservation_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM reservations WHERE reservationID = 1'
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
        reservation = self.connection._create_reservation_object(row)
        self.assertDictContainsSubset(reservation, RESERVATION1)

    def test_get_reservation(self):
        '''
        Test get_reservation with id 1 and 2
        '''
        print('('+self.test_get_reservation.__name__+')', \
              self.test_get_reservation.__doc__)
        #Test with an existing reservation
        reservation = self.connection.get_reservation(RESERVATION1_ID)
        self.assertDictContainsSubset(reservation, RESERVATION1)
        reservation = self.connection.get_reservation(RESERVATION2_ID)
        self.assertDictContainsSubset(reservation, RESERVATION2)

    def test_get_reservation_malformedid(self):
        '''
        Test get_reservation with id mach-1 (malformed)
        '''
        print('('+self.test_get_reservation_malformedid.__name__+')', \
              self.test_get_reservation_malformedid.__doc__)
        #Test with an existing reservation
        with self.assertRaises(ValueError):
            self.connection.get_reservation('mach-1')

    def test_get_reservation_noexistingid(self):
        '''
        Test get_reservation with id 10 (no-existing)
        '''
        print('('+self.test_get_reservation_noexistingid.__name__+')',\
              self.test_get_reservation_noexistingid.__doc__)
        #Test with an existing reservation
        reservation = self.connection.get_reservation(WRONG_reservationID)
        self.assertIsNone(reservation)

    def test_get_reservations(self):
        '''
        Test that get_reservations work correctly
        '''
        print('('+self.test_get_reservations.__name__+')', self.test_get_reservations.__doc__)
        reservations = self.connection.get_reservations()
        #Check that the size is correct
        self.assertEqual(len(reservations), INITIAL_SIZE)
        #Iterate through reservations and check if the reservations with RESERVATION1_ID and RESERVATION2_ID are correct:
        for reservation in reservations:
            if reservation['reservationID'] == RESERVATION1_ID:
                self.assertEqual(len(reservation), 4)
                self.assertDictContainsSubset(reservation, RESERVATION1)
            elif reservation['reservationID'] == RESERVATION2_ID:
                self.assertEqual(len(reservation), 4)
                self.assertDictContainsSubset(reservation, RESERVATION2)

    def test_get_reservations_specific_type(self):
        '''
        Get all reservations of type Stratasys. Check that their ids are 1 and 2.
        '''
        #reservations of type '3d_printers' are 1 and 2
        print('('+self.test_get_reservations_specific_user.__name__+')', \
              self.test_get_reservations_specific_user.__doc__)
        reservations = self.connection.get_reservations(typeName='3d_printers')
        self.assertEqual(len(reservations), 2)
        #reservations id are 1 and 7
        for reservation in reservations:
            self.assertIn(reservation['reservationid'], ('reservation-1', 'reservation-2'))
            self.assertNotIn(reservation['reservationid'], ('reservation-3', 'reservation-4',
                                                    'reservation-5', 'reservation-6'))

    def test_delete_reservation(self):
        '''
        Test that the reservation reservation-1 is deleted
        '''
        print('('+self.test_delete_reservation.__name__+')', \
              self.test_delete_reservation.__doc__)
        resp = self.connection.delete_reservation(RESERVATION1_ID)
        self.assertTrue(resp)
        #Check that the reservation has been really deleted throug a get
        resp2 = self.connection.get_reservation(RESERVATION1_ID)
        self.assertIsNone(resp2)

    def test_delete_reservation_malformedid(self):
        '''
        Test that trying to delete reservation wit id ='1' raises an error
        '''
        print('('+self.test_delete_reservation_malformedid.__name__+')', \
              self.test_delete_reservation_malformedid.__doc__)
        #Test with an existing reservation
        with self.assertRaises(ValueError):
            self.connection.delete_reservation('1')

    def test_delete_reservation_noexistingid(self):
        '''
        Test delete_reservation with  reservation-10 (no-existing)
        '''
        print('('+self.test_delete_reservation_noexistingid.__name__+')', \
              self.test_delete_reservation_noexistingid.__doc__)
        #Test with an existing reservation
        resp = self.connection.delete_reservation(WRONG_reservationID)
        self.assertFalse(resp)

    def test_modify_reservation(self):
        '''
        Test that the reservation reservation-1 is modifed
        '''
        print('('+self.test_modify_reservation.__name__+')', \
              self.test_modify_reservation.__doc__)
        resp = self.connection.modify_reservation(RESERVATION1_ID, 'Roland CAMM-1 GS-24',
                                              "5", "www.yahoo.com")
        self.assertEqual(resp, RESERVATION1_ID)
        #Check that the reservations has been really modified through a get
        resp2 = self.connection.get_reservation(RESERVATION1_ID)
        self.assertDictContainsSubset(resp2, RESERVATION1_MODIFIED)

    def test_modify_reservation_malformedid(self):
        '''
        Test that trying to modify reservation wit id ='1' raises an error
        '''
        print('('+self.test_modify_reservation_malformedid.__name__+')',\
              self.test_modify_reservation_malformedid.__doc__)
        #Test with an existing reservation
        with self.assertRaises(ValueError):
            self.connection.modify_reservation('1', 'Roland CAMM-1 GS-24',
                                                  "5", "www.yahoo.com")

    def test_modify_reservation_noexistingid(self):
        '''
        Test modify_reservation with  reservation-10 (no-existing)
        '''
        print('('+self.test_modify_reservation_noexistingid.__name__+')',\
              self.test_modify_reservation_noexistingid.__doc__)
        #Test with an existing reservation
        resp = self.connection.modify_reservation(WRONG_reservationID, 'Roland CAMM-1 GS-24',
                                              "5", "www.yahoo.com")
        self.assertIsNone(resp)

    def test_create_reservation(self):
        '''
        Test that a new reservation can be created
        '''
        print('('+self.test_create_reservation.__name__+')',\
              self.test_create_reservation.__doc__)
        reservationid = self.connection.create_reservation('Roland', "5", "www.gmail.com")
        self.assertIsNotNone(reservationid)
        #Get the expected created reservation
        new_reservation = {}
        new_reservation['reservationname'] = 'Roland CAMM-1 GS-24'
        new_reservation['typeID'] = '5'
        new_reservation['tutorial'] = 'www.gmail.com'
        #Check that the reservations has been really created through a get
        resp2 = self.connection.get_reservation('reservation-8')
        self.assertDictContainsSubset(new_reservation, resp2)
        #CHECK NOW NOT REGISTERED USER
        # reservationid = self.connection.create_reservation("new title", "new body",
        #                                            "anonymous_User")
        # self.assertIsNotNone(reservationid)
        # #Get the expected modified reservation
        # new_reservation = {}
        # new_reservation['title'] = 'new title'
        # new_reservation['body'] = 'new body'
        # new_reservation['sender'] = 'anonymous_User'
        # #Check that the reservations has been really modified through a get
        # resp2 = self.connection.get_reservation(reservationid)
        # self.assertDictContainsSubset(new_reservation, resp2)

    def test_not_contains_reservation(self):
        '''
        Check if the database does not contain reservation with id reservation-10

        '''
        print('('+self.test_contains_reservation.__name__+')', \
              self.test_contains_reservation.__doc__)
        self.assertFalse(self.connection.contains_reservation(WRONG_reservationID))

    def test_contains_reservation(self):
        '''
        Check if the database contains reservations with id reservation-1 and reservation-2

        '''
        print('('+self.test_contains_reservation.__name__+')', \
              self.test_contains_reservation.__doc__)
        self.assertTrue(self.connection.contains_reservation(RESERVATION1_ID))
        self.assertTrue(self.connection.contains_reservation(RESERVATION2_ID))

if __name__ == '__main__':
    print('Start running reservation tests')
    unittest.main()
