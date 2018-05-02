"""
Reservations and Reservation Resources testing includes the testing of 
[methods(GET,POST,PUT AND DELETE) associated with the resources 
and status codes (200,204,400,404)].
@authors: PWP-20
Code of Ivan and Mika provided in Programmable Web Project exercise _ University of Oulu
is been utilized for the implementation.
@author: ivan sanchez
@author: mika oja
"""
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

    #Add new reservation 
    reservation_1_request = {
      "userID" : "4",
      "machineID" : "2",
      "startTime" : "151943330",
      "endTime" : "151941330"
    }
    #Missing user 
    reservation_2_request = {
      "machineID" : "2",
      "startTime" : "151943330",
      "endTime" : "151941330"
    }
    #Missing machine type
    reservation_3_request = {
      "userID" : "4",
      "startTime" : "151943330",
      "endTime" : "151941330"
      
    }

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


    def test_add_reservation(self):
        """
        Test POST adding new reservation to the database.returns correct status codes
        """
        print("("+self.test_add_reservation.__name__+")", self.test_add_reservation.__doc__)

        resp = self.client.post(resources.api.url_for(resources.Reservations),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.reservation_1_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)

    def test_add_reservation_incorrect_format(self):
        """
        Test POST with incorrect format and return status code 400 (adding new reservations with error of JSON _ missing userID and machineID ).
        """
        print("(" + self.test_add_reservation_incorrect_format.__name__ + ")", self.test_add_reservation_incorrect_format.__doc__)

        #Missing user ID in request body json 
        resp = self.client.post(resources.api.url_for(resources.Reservations),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.reservation_2_request)
                                )
        self.assertTrue(resp.status_code == 400)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["resource_url"], self.url)
        error = data["@error"]
        self.assertIn("@message", error)
        self.assertEqual(error["@message"], "Wrong request format")

        #Missing machine ID in request body json
        resp = self.client.post(resources.api.url_for(resources.Reservations),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.reservation_3_request)
                                )
        self.assertTrue(resp.status_code == 400)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["resource_url"], self.url)
        error = data["@error"]
        self.assertIn("@message", error)
        self.assertEqual(error["@message"], "Wrong request format")

    def test_add_reservation_wrong_media(self):
        """
        Test POST adding reservation with a media different than json
        """
        print("(" + self.test_add_reservation_wrong_media.__name__ + ")",
              self.test_add_reservation_wrong_media.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Reservations),
                                headers={"Content-Type": "text"},
                                data=self.reservation_1_request.__str__()
                                )
        self.assertTrue(resp.status_code == 415)


class ReservationTestCase (ResourcesAPITestCase):

    #ATTENTION: json.loads return unicode
    reservation_req_1 = {
      "reservationID" : "12",
      "updatedBy" : "0"
    }
    reservation_mod_req_1 = {
      "updatedBy" : "0"
    }
    reservation_wrong_format = {
     "userID" : "4",
     "machineID" : "2",
    }

    url_main = "/fablab/api/users/"

    def setUp(self):
        super(ReservationTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Reservation,
                                         reservationID="1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.Reservation,
                                               reservationID="100",
                                               _external=False)
        self.url_wrong_format = resources.api.url_for(resources.Reservation,
                                         reservationID="",
                                         _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/fablab/api/reservations/1/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Reservation)
    def test_wrong_url(self):
        """
        Checks that GET reservation return correct status code if given a
        wrong url
        """
        print("("+self.test_wrong_url.__name__+")", self.test_wrong_url.__doc__)
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_reservation(self):
        """
        Checks that GET reservation return correct status code and data format
        """
        print("("+self.test_get_reservation.__name__+")", self.test_get_reservation.__doc__)
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data.decode("utf-8"))


            controls = data["@controls"]
            self.assertIn("self", controls)
            self.assertIn("profile", controls)
            self.assertIn("collection", controls)
            self.assertIn("edit", controls)
            self.assertIn("fablab:users-all", controls)
            
            edit_ctrl = controls["edit"]
            self.assertIn("title", edit_ctrl)
            self.assertIn("href", edit_ctrl)
            self.assertEqual(edit_ctrl["href"], self.url)
            self.assertIn("encoding", edit_ctrl)
            self.assertEqual(edit_ctrl["encoding"], "json")        
            self.assertIn("method", edit_ctrl)
            self.assertEqual(edit_ctrl["method"], "PUT")
            self.assertIn("schema", edit_ctrl)
        
            schema_data = edit_ctrl["schema"]
            self.assertIn("type", schema_data)
            self.assertIn("properties", schema_data)
            self.assertIn("required", schema_data)
            
            props = schema_data["properties"]
            self.assertIn("reservationID", props)
            self.assertIn("updatedBy", props)
            
            
            req = schema_data["required"]
            self.assertIn("reservationID", props)
            self.assertIn("updatedBy", props)
            
            users_all_ctrl = controls["fablab:users-all"]
            self.assertIn("title", users_all_ctrl)
            self.assertIn("href", users_all_ctrl)
            self.assertEqual(users_all_ctrl["href"], self.url_main)
            
            #Check rest attributes
            self.assertIn("userID", data)
            self.assertIn("machineID", data)
            self.assertIn("startTime", data)
            self.assertIn("endTime", data)
            self.assertIn("isActive", data)
            self.assertIn("createdAt", data)
            self.assertIn("createdBy", data)
            self.assertIn("updatedBy", data)
    
    def test_get_reservation_mimetype(self):
        """
        Checks that GET reservation return correct status code and data format
        """
        print("("+self.test_get_reservation_mimetype.__name__+")", self.test_get_reservation_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_RESERVATION_PROFILE))


    def test_modify_unexisting_reservation(self):
        """
        Test PUT with non existing reservation return correct status code 404 (Try to modify an unexisting reservation)
        """
        print("("+self.test_modify_unexisting_reservation.__name__+")", self.test_modify_unexisting_reservation.__doc__)

        #Check that I receive status code 404
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.reservation_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)
    def test_modify_existing_reservation(self):
        """
        Test PUT with existing reservation return correct status code 204 (Try to modify a existing reservation)
        """
        print("("+self.test_modify_existing_reservation.__name__+")", self.test_modify_existing_reservation.__doc__)

        #Check that I receive status code 204
        resp = self.client.put(self.url,
                                data=json.dumps(self.reservation_mod_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

    def test_modify_reservation_wrong_format(self):
        """
        Test PUT with wrong format return correct status code 400 (Try to modify a reservation in wrong format missing updatedBy)
        """
        print("("+self.test_modify_reservation_wrong_format.__name__+")", self.test_modify_reservation_wrong_format.__doc__)

        #Check that I receive status code 400
        resp = self.client.put(self.url,
                                data=json.dumps(self.reservation_wrong_format),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 400)

        
if __name__ == '__main__':
    print('Start running tests')
    unittest.main()