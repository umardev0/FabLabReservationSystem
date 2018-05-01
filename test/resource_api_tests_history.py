"""
History Resource testing includes the testing of
[methods(GET) associated with the resource
and status codes (200,404)]
@authors: PWP-20
Code of Ivan and Mika provided in Programmable Web Project exercise _ University of Oulu
is been utilized for the implementation.
@author: ivan sanchez
@author: mika oja
"""
import unittest, copy
import json

import flask

import fablab.resources as resources
import fablab.database as database

DB_PATH = "db/fablab_test.db"
ENGINE = database.Engine(DB_PATH)

MASONJSON = "application/vnd.mason+json"
JSON = "application/json"
HAL = "application/hal+json"
FABLAB_USER_PROFILE = "/profiles/user-profile/"
FABLAB_MACHINE_TYPE_PROFILE = "/profiles/machine-type-profile/"
FABLAB_MACHINE_PROFILE = "/profiles/machine-profile/"
FABLAB_RESERVATION_PROFILE = "/profiles/reservation-profile/"
FABLAB_HISTORY_PROFILE = "/profiles/history-profile/"
ERROR_PROFILE = "/profiles/error-profile"
ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

#Tell Flask that I am running it in testing mode.
resources.app.config["TESTING"] = True
#Necessary for correct translation in url_for
resources.app.config["SERVER_NAME"] = "localhost:5000"

#Database Engine utilized in our testing
resources.app.config.update({"Engine": ENGINE})


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

class HistoryTestCase (ResourcesAPITestCase):


    def setUp(self):
        super(HistoryTestCase, self).setUp()
        self.url1= resources.api.url_for(resources.History, machineID="machine-1",
                                         _external=False)
        self.reservation1_count = 4
        
        self.url2 = self.url1+"?after=151943329"
        self.reservation2_count = 2
        self.url3 = self.url1+"?before=151943329"
        self.reservation3_count = 3
        self.url4 = self.url1+"?before=151943329&after=151943330"
        self.reservation4_count = 1

        self.url_wrong= resources.api.url_for(resources.History, machineID="machine-20",
                                         _external=False)


    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        url = "/fablab/api/machines/machine-1/history/"
        with resources.app.test_request_context(url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.History)
    def test_wrong_url(self):
        """
        Checks that GET history return correct status code(404) if given a
        wrong url
        """
        print("("+self.test_wrong_url.__name__+")", self.test_wrong_url.__doc__)
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_history(self):
        """
        Checks that GET history of machine reservations return correct status code(200) and data format
        """
        print("("+self.test_get_history.__name__+")", self.test_get_history.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url1)
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
        self.assertEqual(controls["self"]["href"], self.url1)

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

        #Check that add-reservation control is correct
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
        self.assertEqual(len(items), self.reservation1_count)
        for item in items:
            self.assertIn("reservationID", item)
            self.assertIn("userID", item)
            self.assertIn("machineID", item)
            self.assertIn("startTime", item)
            self.assertIn("endTime", item)
            self.assertIn("isActive", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.Reservation, reservationID=item["reservationID"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_RESERVATION_PROFILE)
            
    def test_get_history_mimetype(self):
        """
        Checks that GET history of machine reservations return correct status code(200) and data format
        """
        print("("+self.test_get_history_mimetype.__name__+")", self.test_get_history_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_HISTORY_PROFILE))

    def test_get_history_before(self):
        """
        Checks that GET history of machine reservations with before parameter(time_stamp) return correct status code(200) and data format
        """
        print("("+self.test_get_history_before.__name__+")", self.test_get_history_before.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url2)
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
        self.assertEqual(controls["self"]["href"], self.url1)

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

        #Check that add-reservation control is correct
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
        self.assertEqual(len(items), self.reservation2_count)
        for item in items:
            self.assertIn("reservationID", item)
            self.assertIn("userID", item)
            self.assertIn("machineID", item)
            self.assertIn("startTime", item)
            self.assertIn("endTime", item)
            self.assertIn("isActive", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.Reservation, reservationID=item["reservationID"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_RESERVATION_PROFILE)

    def test_get_history_after(self):
        """
        Checks that GET history of machine reservations with after parameter(time_stamp) return correct status code(200) and data format
        """
        print("("+self.test_get_history_after.__name__+")", self.test_get_history_after.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url3)
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
        self.assertEqual(controls["self"]["href"], self.url1)

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

        #Check that add-reservation control is correct
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
        self.assertEqual(len(items), self.reservation3_count)
        for item in items:
            self.assertIn("reservationID", item)
            self.assertIn("userID", item)
            self.assertIn("machineID", item)
            self.assertIn("startTime", item)
            self.assertIn("endTime", item)
            self.assertIn("isActive", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.Reservation, reservationID=item["reservationID"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_RESERVATION_PROFILE)

    def test_get_history_before_after(self):
        """
        Checks that GET history of machine reservations with before and after parameter(time_stamp) return correct status code(200) and data format
        """
        print("("+self.test_get_history_before_after.__name__+")", self.test_get_history_before_after.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url4)
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
        self.assertEqual(controls["self"]["href"], self.url1)

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

        #Check that add-reservation control is correct
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
        self.assertEqual(len(items), self.reservation4_count)
        for item in items:
            self.assertIn("reservationID", item)
            self.assertIn("userID", item)
            self.assertIn("machineID", item)
            self.assertIn("startTime", item)
            self.assertIn("endTime", item)
            self.assertIn("isActive", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.Reservation, reservationID=item["reservationID"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_RESERVATION_PROFILE)


if __name__ == "__main__":
    print("Start running tests")
    unittest.main()