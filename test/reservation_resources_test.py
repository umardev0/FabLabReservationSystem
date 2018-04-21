import unittest, copy
import json

import flask

from fablab import database
from fablab import resources

DB_PATH = 'db/fablab_test.db'
ENGINE = database.Engine(DB_PATH)

MASONJSON = "application/vnd.mason+json"
JSON = "application/json"
HAL = "application/hal+json"
FABLAB_RESERVATION_PROFILE = "/profiles/reservation-profile/"
ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

#Tell Flask that I am running it in testing mode.
resources.app.config["TESTING"] = True
#Necessary for correct translation in url_for
resources.app.config["SERVER_NAME"] = "localhost:5000"

#Database Engine utilized in our testing
resources.app.config.update({"Engine": ENGINE})

#Other database parameters.
initial_reservations = 10


class ResourcesAPITestCase(unittest.TestCase):
    #INITIATION AND TEARDOWN METHODS
    @classmethod
    def setUpClass(cls):
        """ Creates the database structure. Removes first any preexisting
            database file
        """
        print("Testing ", cls.__name__)
        ENGINE.remove_database()
        
        ENGINE.create_tables()

    @classmethod
    def tearDownClass(cls):
        """Remove the testing database"""
        print("Testing ENDED for ", cls.__name__)
        ENGINE.remove_database()

    def setUp(self):
        """
        Populates the database
        """
        #This method load the initial values from forum_data_dump.sql
        ENGINE.populate_tables()
        #Activate app_context for using url_for
        self.app_context = resources.app.app_context()
        self.app_context.push()
        #Create a test client
        self.client = resources.app.test_client()

    def tearDown(self):
        """
        Remove all records from database
        """
        ENGINE.clear()
        self.app_context.pop()
		
class ReservationsTestCase (ResourcesAPITestCase):

    url = "/fablab/api/reservations/"

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() should work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Reservations)
          
    def test_get_reservations(self):
        """
        Checks that GET Reservations return correct status code and data format
        """
        print("("+self.test_get_reservations.__name__+")", self.test_get_reservations.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("reservations"))
        self.assertEqual(resp.status_code, 200)

        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))

        #Check controls
        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("fablab:add-reservation", controls)
        self.assertIn("fablab:machines-all", controls)
        self.assertIn("fablab:users-all", controls)
        
        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        # Check that machines-all control is correct
        machines_ctrl = controls["fablab:machines-all"]
        self.assertIn("title", machines_ctrl)
        self.assertIn("href", machines_ctrl)
        self.assertEqual(machines_ctrl["href"], "/fablab/api/machines/")
        
        # Check that users-all control is correct
        users_ctrl = controls["fablab:users-all"]
        self.assertIn("title", users_ctrl)
        self.assertIn("href", users_ctrl)
        self.assertEqual(users_ctrl["href"], "/fablab/api/users/")

        #Check that add-machinetype control is correct
        add_type = controls["fablab:add-reservation"]
        self.assertIn("title", add_type)
        self.assertIn("href", add_type)
        self.assertEqual(add_type["href"], "/fablab/api/reservations/")
        self.assertIn("encoding", add_type)
        self.assertEqual(add_type["encoding"], "json")        
        self.assertIn("method", add_type)
        self.assertEqual(add_type["method"], "POST")
        self.assertIn("schemaUrl", add_type)
        
        #Check that items are correct.
        items = data["items"]
        self.assertEqual(len(items), initial_reservations)
        for item in items:
            self.assertIn("reservationID", item)
            self.assertIn("userID", item)
            self.assertIn("machineID", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.Reservation, reservationID=item["reservationID"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_RESERVATION_PROFILE)
            
    def test_get_reservations_mimetype(self):
        """
        Checks that GET reservations return correct status code and data format
        """
        print("("+self.test_get_reservations_mimetype.__name__+")", self.test_get_reservations_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("reservations"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_RESERVATION_PROFILE)) 

       


if __name__ == '__main__':
    print('Start running tests')
    unittest.main()