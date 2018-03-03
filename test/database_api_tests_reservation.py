import sqlite3, unittest
from fablab import database


#Path to the database file, different from the deployment db
DB_PATH = 'db/fablab_test_api.db'
ENGINE = database.Engine()


RES1_ID = 1
RES1 = {'reservationID': 1,'userID': 1, 'machineID': 1,
'startTime': 151943330, 'endTime': 151945330,
'isActive': 1,'createdAt': 1519475698, 'createdBy': 1,
'updatedAt': None, 'updatedBy': None}

RES2_ID = 2
RES2 = {'reservationID': 2,'userID': 1, 'machineID': 2,
'startTime': 151943330, 'endTime': 151944330,
'isActive': 1,'createdAt': 1519473698, 'createdBy': 1,
'updatedAt': None, 'updatedBy': None}

RES1_MODIFIED = {'reservationID': 1, 'startTime': 151942220,
'endTime': 151943330}

WRONG_resID = 20
INITIAL_SIZE = 10

class ReservationDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Reservations related methods.
    '''

    #Creates a Connection instance to use the API

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
        Checks that the table initially contains 10 reservations
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
        values for the first database row.
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
        reservation['machineID'] = 1
        self.assertDictContainsSubset(reservation, RES1)

    def test_get_reservation(self):
        '''
        Test get_reservation with id 1 and 2
        '''
        print('('+self.test_get_reservation.__name__+')', \
              self.test_get_reservation.__doc__)
        #Test with an existing reservation
        reservation = self.connection.get_reservation(RES1_ID)
        RES1['machineID'] = 'machine-1'
        self.assertDictContainsSubset(reservation, RES1)
        reservation = self.connection.get_reservation(RES2_ID)
        RES2['machineID'] = 'machine-2'
        self.assertDictContainsSubset(reservation, RES2)

    def test_get_reservation_malformedid(self):
        '''
        Test get_reservation with id rese-1 (malformed)
        '''
        print('('+self.test_get_reservation_malformedid.__name__+')', \
              self.test_get_reservation_malformedid.__doc__)
        #Test with an existing reservation
        with self.assertRaises(ValueError):
            self.connection.get_reservation('rese-1')

    def test_get_reservation_noexistingid(self):
        '''
        Test get_reservation with id 20 (non-existing)
        '''
        print('('+self.test_get_reservation_noexistingid.__name__+')',\
              self.test_get_reservation_noexistingid.__doc__)
        #Test with an existing reservation
        reservation = self.connection.get_reservation(WRONG_resID)
        self.assertIsNone(reservation)

    def test_get_reservation_list(self):
        '''
        Test that get_reservation_list work correctly
        '''
        print('('+self.test_get_reservation_list.__name__+')', self.test_get_reservation_list.__doc__)
        reservations = self.connection.get_reservation_list()
        #Check that the size is correct
        self.assertEqual(len(reservations), INITIAL_SIZE)
        #Iterate through reservations and check if the reservations with RES1_ID and RES2_ID are correct:
        for reservation in reservations:
            if reservation['reservationID'] == RES1_ID:
                self.assertEqual(len(reservation), 6)
                RES1['machineID'] = 'machine-1'
                self.assertDictContainsSubset(reservation, RES1)
            elif reservation['reservationID'] == RES2_ID:
                self.assertEqual(len(reservation), 6)
                RES2['machineID'] = 'machine-2'
                self.assertDictContainsSubset(reservation, RES2)

    def test_get_reservations_specific_user(self):
        '''
        Get all reservations of user with id 1. Check that their ids are 2,6,10.
        '''
        #reservations of user 1 for machine 2 are 2,6,10
        print('('+self.test_get_reservations_specific_user.__name__+')', \
              self.test_get_reservations_specific_user.__doc__)
        reservations = self.connection.get_reservation_list(1,'machine-2')
        self.assertEqual(len(reservations), 3)
        #reservations id are 2,6,10
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (2,6,10))
            self.assertNotIn(reservation['reservationID'], (1, 3, 4, 5))

    def test_get_reservations_specific_machine(self):
        '''
        Get all reservations of machine with id 2. Check that their ids are 2, 10.
        '''
        #reservations of user 1 for machine 2 are 2,6,10
        print('('+self.test_get_reservations_specific_machine.__name__+')', \
              self.test_get_reservations_specific_machine.__doc__)
        reservations = self.connection.get_reservation_list(None,'machine-2')
        self.assertEqual(len(reservations), 3)
        #reservations id are 2 and 10
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (2,6,10))
            self.assertNotIn(reservation['reservationID'], (1, 3, 4, 5))

    def test_get_reservations_specific_start_time(self):
        '''
        Get all reservations starting after 151911000. Check that their ids are 1-10.
        '''
        #all reservations starting after 151911000
        print('('+self.test_get_reservations_specific_start_time.__name__+')', \
              self.test_get_reservations_specific_start_time.__doc__)
        reservations = self.connection.get_reservation_list(None, None, 151911000)
        self.assertEqual(len(reservations), 10)
        #reservations id are 1-10
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (1,2,3,4,5,6,7,8,9,10))

    def test_get_reservations_specific_end_time(self):
        '''
        Get all reservations ending before 151912005. Check that their ids are 9, 10.
        '''
        #reservations ending before 151912005 are 9 and 10
        print('('+self.test_get_reservations_specific_end_time.__name__+')', \
              self.test_get_reservations_specific_end_time.__doc__)
        reservations = self.connection.get_reservation_list(None, None, -1, 151912005)
        self.assertEqual(len(reservations), 2)
        #reservations id are 9 and 10
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (9, 10))
            self.assertNotIn(reservation['reservationID'], (1,2,3,4,5))

    def test_get_reservations_start_end_time(self):
        '''
        Get all reservations starting after 151911000 & ending before 151912005. Check that their ids are 9, 10.
        '''
        #reservations starting after 151911000 & ending before 151912005 are 9 and 10
        print('('+self.test_get_reservations_start_end_time.__name__+')', \
              self.test_get_reservations_start_end_time.__doc__)
        reservations = self.connection.get_reservation_list(None, None, 151911000, 151912005)
        self.assertEqual(len(reservations), 2)
        #reservations id are 9 and 10
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (9, 10))
            self.assertNotIn(reservation['reservationID'], (1,2,3,4,5))

    def test_get_active_reservations(self):
        '''
        Get all active reservations. Check that their ids are 1,2,3,4,5,6,9,10.
        '''
        #active reservations are 1,2,3,4,5,6,9,10
        print('('+self.test_get_active_reservations.__name__+')', \
              self.test_get_active_reservations.__doc__)
        reservations = self.connection.get_active_reservation_list()
        self.assertEqual(len(reservations), 8)
        #reservations id are 1,2,3,4,5,6,9,10
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (1,2,3,4,5,6,9,10))
            self.assertNotIn(reservation['reservationID'], (7,8))

    def test_get_inactive_reservations(self):
        '''
        Get all inactive reservations. Check that their ids are 7,8.
        '''
        #inactive reservations are 7,8
        print('('+self.test_get_inactive_reservations.__name__+')', \
              self.test_get_inactive_reservations.__doc__)
        reservations = self.connection.get_active_reservation_list(0)
        self.assertEqual(len(reservations), 2)
        #reservations id are 7,8
        for reservation in reservations:
            self.assertIn(reservation['reservationID'], (7,8))
            self.assertNotIn(reservation['reservationID'], (1,2,3,4,5,6,9,10))

    def test_disable_reservation(self):
        '''
        Set reservation 1's isActive state to 0 (inActive) and test if
        has been changed
        '''
        print('('+self.test_disable_reservation.__name__+')', \
              self.test_disable_reservation.__doc__)
        reservations = self.connection.disable_reservation(1)
        self.assertEqual(reservations, 1)

        #Check that the reservations has been really disabled through a get
        resp = self.connection.get_active_reservation_list(0)
        self.assertEqual(len(resp), 3)
        #reservations id are 7,8
        for reser in resp:
            self.assertIn(reser['reservationID'], (1,7,8))
            self.assertNotIn(reser['reservationID'], (2,3,4,5,6,9,10))

    def test_delete_reservation(self):
        '''
        Test that oldest 5 reservations are deleted
        '''
        print('('+self.test_delete_reservation.__name__+')', \
              self.test_delete_reservation.__doc__)
        resp = self.connection.delete_oldest_reservations(5)
        self.assertTrue(resp)
        #Check that the reservation has been really deleted throug a get
        resp2 = self.connection.get_reservation(RES1_ID)
        self.assertIsNone(resp2)

    # def test_delete_reservation_malformedid(self):
    #     '''
    #     Test that trying to delete reservation wit id ='1' raises an error
    #     '''
    #     print('('+self.test_delete_reservation_malformedid.__name__+')', \
    #           self.test_delete_reservation_malformedid.__doc__)
    #     #Test with an existing reservation
    #     with self.assertRaises(ValueError):
    #         self.connection.delete_reservation('1')
    #
    # def test_delete_reservation_noexistingid(self):
    #     '''
    #     Test delete_reservation with  reservation-10 (no-existing)
    #     '''
    #     print('('+self.test_delete_reservation_noexistingid.__name__+')', \
    #           self.test_delete_reservation_noexistingid.__doc__)
    #     #Test with an existing reservation
    #     resp = self.connection.delete_reservation(WRONG_resID)
    #     self.assertFalse(resp)

    def test_modify_reservation(self):
        '''
        Test that the reservation with id 1 is modifed
        '''
        print('('+self.test_modify_reservation.__name__+')', \
              self.test_modify_reservation.__doc__)
        resp = self.connection.modify_reservation(RES1_ID, 151942220, 151943330)
        self.assertEqual(resp, RES1_ID)
        #Check that the reservations has been really modified through a get
        resp2 = self.connection.get_reservation(RES1_ID)
        self.assertDictContainsSubset(RES1_MODIFIED, resp2)

    def test_modify_reservation_malformedid(self):
        '''
        Test that trying to modify reservation wit id ='1' (malformed id) raises an error
        '''
        print('('+self.test_modify_reservation_malformedid.__name__+')',\
              self.test_modify_reservation_malformedid.__doc__)
        #Test with an existing reservation
        with self.assertRaises(ValueError):
            self.connection.modify_reservation('1', 151942220, 151943330)

    def test_modify_reservation_noexistingid(self):
        '''
        Test modify_reservation with 20 (non-existing)
        '''
        print('('+self.test_modify_reservation_noexistingid.__name__+')',\
              self.test_modify_reservation_noexistingid.__doc__)
        #Test with an existing reservation
        resp = self.connection.modify_reservation(WRONG_resID, 151942220, 151943330)
        self.assertIsNone(resp)

    def test_create_reservation(self):
        '''
        Test that a new reservation can be created
        '''
        print('('+self.test_create_reservation.__name__+')',\
              self.test_create_reservation.__doc__)
        reservationid = self.connection.create_reservation(5, 5)
        self.assertIsNotNone(reservationid)
        #Get the expected created reservation
        new_reservation = {}
        new_reservation['userID'] = 5
        new_reservation['machineID'] = 'machine-5'
        #Check that the reservations has been really created through a get
        resp2 = self.connection.get_reservation(11)
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
        Check if the database does not contain reservation with id 20 (non-existing)

        '''
        print('('+self.test_contains_reservation.__name__+')', \
              self.test_contains_reservation.__doc__)
        self.assertFalse(self.connection.contains_reservation(WRONG_resID))

    def test_contains_reservation(self):
        '''
        Check if the database contains reservations with id 1 and 2
        '''
        print('('+self.test_contains_reservation.__name__+')', \
              self.test_contains_reservation.__doc__)
        self.assertTrue(self.connection.contains_reservation(RES1_ID))
        self.assertTrue(self.connection.contains_reservation(RES2_ID))

if __name__ == '__main__':
    print('Start running reservation tests')
    unittest.main()
