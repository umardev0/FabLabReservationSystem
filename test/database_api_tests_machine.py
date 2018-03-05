import sqlite3, unittest
from fablab import database


#Path to the database file, different from the deployment db
DB_PATH = 'db/fablab_test_api.db'
ENGINE = database.Engine()


MACHINE1_ID = 'machine-1'
MACHINE1 = {'machineID': 1, 'machinename': 'Stratasys 380mc',
'typeID': 1, 'tutorial': 'www.google.com',
'createdAt': 1519472221, 'updatedAt': None,
'createdBy': 0, 'updatedBy': None}

MACHINE2_ID = 'machine-2'
MACHINE2 = {'machineID': 2, 'machinename': 'Formlabs Form 2',
'typeID': 1, 'tutorial': 'www.google.com',
'createdAt': 1519472221, 'updatedAt': 1519472221,
'createdBy': 0, 'updatedBy': 1}

MACHINE1_MODIFIED = {'machineID': 1, 'machinename': 'Roland mod',
'typeID': 5, 'tutorial': 'www.yahoo.com'}

WRONG_machineID = 'machine-10'
INITIAL_SIZE = 7

class MachineDBAPITestCase(unittest.TestCase):
    '''
    Test cases for the Machines related methods.
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

    def test_machines_table_created(self):
        '''
        Checks that the table initially contains 5 machines (check
        fablab_data_dump.sql). NOTE: Do not use Connection instance but
        call directly SQL.
        '''
        print('('+self.test_machines_table_created.__name__+')', \
                  self.test_machines_table_created.__doc__)
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

    def test_create_machine_object(self):
        '''
        Check that the method _create_machine_object works return adequate
        values for the first database row. NOTE: Do not use Connection instance
        to extract data from database but call directly SQL.
        '''
        print('('+self.test_create_machine_object.__name__+')', \
              self.test_create_machine_object.__doc__)
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM machines WHERE machineID = 1'
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
        machine = self.connection._create_machine_object(row)
        machine['machineID'] = 1
        self.assertDictContainsSubset(machine, MACHINE1)

    def test_get_machine(self):
        '''
        Test get_machine with id 1 and 2
        '''
        print('('+self.test_get_machine.__name__+')', \
              self.test_get_machine.__doc__)
        #Test with an existing machine
        machine = self.connection.get_machine(MACHINE1_ID)
        MACHINE1['machineID'] = 'machine-1'
        self.assertDictContainsSubset(machine, MACHINE1)
        machine = self.connection.get_machine(MACHINE2_ID)
        MACHINE2['machineID'] = 'machine-2'
        self.assertDictContainsSubset(machine, MACHINE2)

    def test_get_machine_malformedid(self):
        '''
        Test get_machine with id mach-1 (malformed)
        '''
        print('('+self.test_get_machine_malformedid.__name__+')', \
              self.test_get_machine_malformedid.__doc__)
        #Test with an existing machine
        with self.assertRaises(ValueError):
            self.connection.get_machine('mach-1')

    def test_get_machine_noexistingid(self):
        '''
        Test get_machine with id 10 (non-existing)
        '''
        print('('+self.test_get_machine_noexistingid.__name__+')',\
              self.test_get_machine_noexistingid.__doc__)
        #Test with an existing machine
        machine = self.connection.get_machine(WRONG_machineID)
        self.assertIsNone(machine)

    def test_get_machines(self):
        '''
        Test that get_machines work correctly
        '''
        print('('+self.test_get_machines.__name__+')', self.test_get_machines.__doc__)
        machines = self.connection.get_machines()
        #Check that the size is correct
        self.assertEqual(len(machines), INITIAL_SIZE)
        #Iterate through machines and check if the machines with MACHINE1_ID and MACHINE2_ID are correct:
        for machine in machines:
            if machine['machineID'] == MACHINE1_ID:
                self.assertEqual(len(machine), 4)
                MACHINE1['machineID'] = 'machine-1'
                self.assertDictContainsSubset(machine, MACHINE1)
            elif machine['machineID'] == MACHINE2_ID:
                self.assertEqual(len(machine), 4)
                MACHINE2['machineID'] = 'machine-2'
                self.assertDictContainsSubset(machine, MACHINE2)

    def test_get_machines_specific_type(self):
        '''
        Get all machines of type Stratasys. Check that their ids are 1 and 2.
        '''
        #machines of type '3d_printers' are 1 and 2
        print('('+self.test_get_machines_specific_type.__name__+')', \
              self.test_get_machines_specific_type.__doc__)
        machines = self.connection.get_machines(typeName='3d_printers')
        self.assertEqual(len(machines), 2)
        #machines id are 1 and 7
        for machine in machines:
            self.assertIn(machine['machineID'], ('machine-1', 'machine-2'))
            self.assertNotIn(machine['machineID'], ('machine-3', 'machine-4',
                                                    'machine-5', 'machine-6'))

    def test_delete_machine(self):
        '''
        Test that the machine with id machine-1 is deleted
        '''
        print('('+self.test_delete_machine.__name__+')', \
              self.test_delete_machine.__doc__)
        resp = self.connection.delete_machine(MACHINE1_ID)
        self.assertTrue(resp)
        #Check that the machine has been really deleted throug a get
        resp2 = self.connection.get_machine(MACHINE1_ID)
        self.assertIsNone(resp2)

    def test_delete_machine_malformedid(self):
        '''
        Test that trying to delete machine with id ='1' (malformed) raises an error
        '''
        print('('+self.test_delete_machine_malformedid.__name__+')', \
              self.test_delete_machine_malformedid.__doc__)
        #Test with an existing machine
        with self.assertRaises(ValueError):
            self.connection.delete_machine('1')

    def test_delete_machine_noexistingid(self):
        '''
        Test delete_machine with id machine-10 (non-existing)
        '''
        print('('+self.test_delete_machine_noexistingid.__name__+')', \
              self.test_delete_machine_noexistingid.__doc__)
        #Test with an existing machine
        resp = self.connection.delete_machine(WRONG_machineID)
        self.assertFalse(resp)

    def test_modify_machine(self):
        '''
        Test that the machine with id machine-1 is modifed
        '''
        print('('+self.test_modify_machine.__name__+')', \
              self.test_modify_machine.__doc__)
        resp = self.connection.modify_machine(MACHINE1_ID, 'Roland mod',
                                              "5", "www.yahoo.com")
        self.assertEqual(resp, MACHINE1_ID)
        #Check that the machines has been really modified through a get
        resp2 = self.connection.get_machine(MACHINE1_ID)
        MACHINE1_MODIFIED['machineID'] = 'machine-1'
        self.assertDictContainsSubset(MACHINE1_MODIFIED, resp2)

    def test_modify_machine_malformedid(self):
        '''
        Test that trying to modify machine with id ='1' (malformed) raises an error
        '''
        print('('+self.test_modify_machine_malformedid.__name__+')',\
              self.test_modify_machine_malformedid.__doc__)
        #Test with an existing machine
        with self.assertRaises(ValueError):
            self.connection.modify_machine('1', 'Roland CAMM-1 GS-24',
                                                  "5", "www.yahoo.com")

    def test_modify_machine_noexistingid(self):
        '''
        Test modify_machine with id machine-10 (non-existing)
        '''
        print('('+self.test_modify_machine_noexistingid.__name__+')',\
              self.test_modify_machine_noexistingid.__doc__)
        #Test with an existing machine
        resp = self.connection.modify_machine(WRONG_machineID, 'Roland CAMM-1 GS-24',
                                              "5", "www.yahoo.com")
        self.assertIsNone(resp)

    def test_create_machine(self):
        '''
        Test that a new machine can be created
        '''
        print('('+self.test_create_machine.__name__+')',\
              self.test_create_machine.__doc__)
        machineid = self.connection.create_machine('Roland', "5", "www.gmail.com")
        self.assertIsNotNone(machineid)
        #Get the expected created machine
        new_machine = {}
        new_machine['machinename'] = 'Roland'
        new_machine['typeID'] = 5
        new_machine['tutorial'] = 'www.gmail.com'
        #Check that the machines has been really created through a get
        resp2 = self.connection.get_machine('machine-8')
        self.assertDictContainsSubset(new_machine, resp2)
        #CHECK NOW NOT REGISTERED USER
        # machineid = self.connection.create_machine("new title", "new body",
        #                                            "anonymous_User")
        # self.assertIsNotNone(machineid)
        # #Get the expected modified machine
        # new_machine = {}
        # new_machine['title'] = 'new title'
        # new_machine['body'] = 'new body'
        # new_machine['sender'] = 'anonymous_User'
        # #Check that the machines has been really modified through a get
        # resp2 = self.connection.get_machine(machineid)
        # self.assertDictContainsSubset(new_machine, resp2)

    def test_not_contains_machine(self):
        '''
        Check if the database does not contain machine with id machine-10

        '''
        print('('+self.test_contains_machine.__name__+')', \
              self.test_contains_machine.__doc__)
        self.assertFalse(self.connection.contains_machine(WRONG_machineID))

    def test_contains_machine(self):
        '''
        Check if the database contains machines with id machine-1 and machine-2

        '''
        print('('+self.test_contains_machine.__name__+')', \
              self.test_contains_machine.__doc__)
        self.assertTrue(self.connection.contains_machine(MACHINE1_ID))
        self.assertTrue(self.connection.contains_machine(MACHINE2_ID))

if __name__ == '__main__':
    print('Start running machine tests')
    unittest.main()
