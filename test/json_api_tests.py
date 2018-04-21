"""
Created on 26.01.2013
Modified on 05.02.2017
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
ERROR_PROFILE = "/profiles/error-profile"
ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

#Tell Flask that I am running it in testing mode.
resources.app.config["TESTING"] = True
#Necessary for correct translation in url_for
resources.app.config["SERVER_NAME"] = "localhost:5000"

#Database Engine utilized in our testing
resources.app.config.update({"Engine": ENGINE})

#Other database parameters.
initial_types = 5
initial_reservations = 5


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

class MachineTypesTestCase (ResourcesAPITestCase):

    #Anonymous user
    machine_type_new_request = {
      "typeName" : "new_test_type",
      "typeFullname" : "new full name type",
      "pastProject" : "http://www.fablab.oulu.fi/",
      "createdBy" : "1"
    }   

    #Existing user
    machine_type_error_request = {
      "typeFullname" : "new full name type",
      "pastProject" : "http://www.fablab.oulu.fi/"
    }   

    #Non exsiting user
    message_3_request = {
      "typeName" : "new_test_type",
      "typeFullname" : "new full name type",
      "pastProject" : "http://www.fablab.oulu.fi/",
      "createdBy" : "1"
    }   

    #Missing the headline
    message_4_wrong = {
        "articleBody": "Do you know any good online hypermedia course?",
        "author": "Onethatwashere"
    }

    #Missing the articleBody
    message_5_wrong = {
        "articleBody": "Do you know any good online hypermedia course?",
        "author": "Onethatwashere"
    }

    url = "/fablab/api/machinetypes/"

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.MachineTypes)

    def test_get_machinetypes(self):
        """
        Checks that GET Messages return correct status code and data format
        """
        print("("+self.test_get_machinetypes.__name__+")", self.test_get_machinetypes.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("machinetypes"))
        self.assertEqual(resp.status_code, 200)
        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))
        
        #Check controls
        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("fablab:add-machinetype", controls)
        self.assertIn("fablab:machines-all", controls)

        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        # Check that users-all control is correct
        users_ctrl = controls["fablab:machines-all"]
        self.assertIn("title", users_ctrl)
        self.assertIn("href", users_ctrl)
        self.assertEqual(users_ctrl["href"], "/fablab/api/machines/")

        #Check that add-message control is correct
        msg_ctrl = controls["fablab:add-machinetype"]
        self.assertIn("title", msg_ctrl)
        self.assertIn("href", msg_ctrl)
        self.assertEqual(msg_ctrl["href"], "/fablab/api/machinetypes/")
        self.assertIn("encoding", msg_ctrl)
        self.assertEqual(msg_ctrl["encoding"], "json")        
        self.assertIn("method", msg_ctrl)
        self.assertEqual(msg_ctrl["method"], "POST")
        self.assertIn("schemaUrl", msg_ctrl)

        #Check that items are correct.
        items = data["items"]
        self.assertEqual(len(items), initial_types)
        for item in items:
            self.assertIn("id", item)
            self.assertIn("typeName", item)
            self.assertIn("typeFullname", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.MachineType, typeID=item["id"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_MACHINE_TYPE_PROFILE)

    def test_get_machine_types_mimetype(self):
        """
        Checks that GET machine types return correct status code and data format
        """
        print("("+self.test_get_machine_types_mimetype.__name__+")", self.test_get_machine_types_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("machinetypes"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_MACHINE_TYPE_PROFILE))   

    def test_add_machine_type(self):
        """
        Test adding new type to the database.
        """
        print("("+self.test_add_machine_type.__name__+")", self.test_add_machine_type.__doc__)

        resp = self.client.post(resources.api.url_for(resources.MachineTypes),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.machine_type_new_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)

    def test_add_machine_type_error(self):
        """
        Test adding new type with error of JSON _ missing typeName.
        """
        print("("+self.test_add_machine_type_error.__name__+")", self.test_add_machine_type_error.__doc__)

        resp = self.client.post(resources.api.url_for(resources.MachineTypes),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.machine_type_error_request)
                               )
        self.assertTrue(resp.status_code == 400)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["resource_url"], self.url)
       
        error = data["@error"]
        self.assertIn("@message", error)
        self.assertEqual(error["@message"], "Wrong request format")

    def test_add_machine_type_wrong_media(self):
        """
        Test adding machine type with a media different than json
        """
        print("("+self.test_add_machine_type_wrong_media.__name__+")", self.test_add_machine_type_wrong_media.__doc__)
        resp = self.client.post(resources.api.url_for(resources.MachineTypes),
                                headers={"Content-Type": "text"},
                                data=self.machine_type_new_request.__str__()
                               )
        self.assertTrue(resp.status_code == 415)

                          
if __name__ == "__main__":
    print("Start running tests")
    unittest.main()
