"""
Machine and Machines Resources testing includes the testing of 
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
initial_types = 7


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

class MachinesTestCase (ResourcesAPITestCase):

    #new machine 
    machine_new_request = {
      "machinename" : "new_machine",
      "typeID" : "1",
      "tutorial" : "www.google.com"
    }   

    #wrong machine request format
    machine_incorrect_format_request = {
      "machinename" : "new_machine",
      "tutorial" : "www.google.com",
    }   

    url = "/fablab/api/machines/"

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Machines)
    def test_get_machines(self):
        """
        Checks that GET machines return correct status code and data format
        """
        print("("+self.test_get_machines.__name__+")", self.test_get_machines.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("machines"))
        self.assertEqual(resp.status_code, 200)
        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))
        
        #Check controls
        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("fablab:add-machine", controls)
        self.assertIn("fablab:machinetypes-all", controls)

        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)

        # Check that machinetypes-all control is correct
        machines_all = controls["fablab:machinetypes-all"]
        self.assertIn("title", machines_all)
        self.assertIn("href", machines_all)
        self.assertEqual(machines_all["href"], "/fablab/api/machinetypes/")

        #Check that add-machine control is correct
        add_type = controls["fablab:add-machine"]
        self.assertIn("title", add_type)
        self.assertIn("href", add_type)
        self.assertEqual(add_type["href"], "/fablab/api/machines/")
        self.assertIn("encoding", add_type)
        self.assertEqual(add_type["encoding"], "json")        
        self.assertIn("method", add_type)
        self.assertEqual(add_type["method"], "POST")
        self.assertIn("schemaUrl", add_type)

        #Check that items are correct.
        items = data["items"]
        self.assertEqual(len(items), initial_types)
        for item in items:
            self.assertIn("machineID", item)
            self.assertIn("machinename", item)
            self.assertIn("typeID", item)
            self.assertIn("tutorial", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.Machine, machineID=item["machineID"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_MACHINE_PROFILE)
    def test_get_machines_mimetype(self):
        """
        Checks that GET machines return correct status code and data format
        """
        print("("+self.test_get_machines_mimetype.__name__+")", self.test_get_machines_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("machines"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_MACHINE_PROFILE))   
    def test_add_machine(self):
        """
        Test POST adding new machine to the database.returns correct status codes
        """
        print("("+self.test_add_machine.__name__+")", self.test_add_machine.__doc__)

        resp = self.client.post(resources.api.url_for(resources.Machines),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.machine_new_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        self.assertTrue(resp.status_code == 200)

    def test_add_machine_incorrect_format(self):
        """
        Test POST with incorrect format and return status code 400 (adding new machine with incorrect format of JSON _ missing typeID.)
        """
        print("("+self.test_add_machine_incorrect_format.__name__+")", self.test_add_machine_incorrect_format.__doc__)

        resp = self.client.post(resources.api.url_for(resources.Machines),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.machine_incorrect_format_request)
                               )
        self.assertTrue(resp.status_code == 400)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["resource_url"], self.url)
       
        error = data["@error"]
        self.assertIn("@message", error)
        self.assertEqual(error["@message"], "Wrong request format")

    def test_add_machine_wrong_media(self):
        """
        Test POST adding machine with a media different than json
        """
        print("("+self.test_add_machine_wrong_media.__name__+")", self.test_add_machine_wrong_media.__doc__)
        resp = self.client.post(resources.api.url_for(resources.Machines),
                                headers={"Content-Type": "text"},
                                data=self.machine_new_request.__str__()
                               )
        self.assertTrue(resp.status_code == 415)


class MachineTestCase (ResourcesAPITestCase):

    #ATTENTION: json.loads return unicode
    machine_req_1 = {
        "machinename" : "new_machine",
        "typeID" : "1",
        "tutorial" : "www.google.com",
        "createdBy": 0
    }

    machine_moq_req_1 = {
        "machinename" : "new_machine",
        "typeID" : "2",
        "tutorial" : "www.google.com",
        "updatedBy": 1
    }
    machine_wrong_req_1 = {
        "typeID" : "1",
        "tutorial" : "www.google.com",
        "updatedBy": 1
    }

    url_main = "/fablab/api/machines/"

    def setUp(self):
        super(MachineTestCase, self).setUp()
        self.url = resources.api.url_for(resources.Machine,
                                         machineID="machine-1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.Machine,
                                               machineID="machine-100",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/fablab/api/machines/1/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Machine)

    def test_wrong_url(self):
        """
        Checks that GET machine return correct status code if given a
        wrong URL
        """
        print("("+self.test_wrong_url.__name__+")", self.test_wrong_url.__doc__)
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_get_machine(self):
        """
        Checks that GET machine return correct status code and data format
        """
        print("("+self.test_get_machine.__name__+")", self.test_get_machine.__doc__)
        with resources.app.test_client() as client:
            resp = client.get(self.url)
            self.assertEqual(resp.status_code, 200)
            data = json.loads(resp.data.decode("utf-8"))


            controls = data["@controls"]
            self.assertIn("self", controls)
            self.assertIn("profile", controls)
            self.assertIn("collection", controls)
            self.assertIn("edit", controls)
            self.assertIn("delete", controls)
            self.assertIn("fablab:history-reservations",controls)
            self.assertIn("fablab:machines-all", controls)
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
            self.assertIn("machinename", props)
            
            req = schema_data["required"]
            
            history_reservations_ctrl = controls["fablab:history-reservations"]
            self.assertIn("title", history_reservations_ctrl)
            self.assertIn("href", history_reservations_ctrl)

            machines_all_ctrl = controls["fablab:machines-all"]
            self.assertIn("title", machines_all_ctrl)
            self.assertIn("href", machines_all_ctrl)
            self.assertEqual(machines_all_ctrl["href"], self.url_main)
            
            users_all_ctrl = controls["fablab:users-all"]
            self.assertIn("title", users_all_ctrl)
            self.assertIn("href", users_all_ctrl)
            
            #Check rest attributes
            self.assertIn("machinename", data)
            self.assertIn("typeID", data)
            self.assertIn("tutorial", data)
            self.assertIn("createdAt", data)
            self.assertIn("createdBy", data)
            self.assertIn("updatedAt", data)
            self.assertIn("updatedBy", data)

    def test_get_machine_mimetype(self):
        """
        Checks that GET machine return correct status code and data format
        """
        print("("+self.test_get_machine_mimetype.__name__+")", self.test_get_machine_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_MACHINE_PROFILE))

    def test_modify_unexisting_machine(self):
        """
        Test PUT with non existing machine return correct status code 404(Try to modify an unexisting machine)
        """
        print("("+self.test_modify_unexisting_machine.__name__+")", self.test_modify_unexisting_machine.__doc__)

        #Check that I receive status code 404
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.machine_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    def test_modify_machine(self):
        """
        Test PUT with existing machine return correct status code 204 (Try to modify an existing machine)
        """
        print("("+self.test_modify_machine.__name__+")", self.test_modify_machine.__doc__)

        #Check that I receive status code 204
        resp = self.client.put(self.url,
                                data=json.dumps(self.machine_moq_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

    def test_modify_machine_wrong_format(self):
        """
        Test PUT with wrong format return correct status code 400 (Try to modify a modify machine in wrong format missing machinename) 
        """
        print("("+self.test_modify_machine_wrong_format.__name__+")", self.test_modify_machine_wrong_format.__doc__)

        #Check that I receive status code 400
        resp = self.client.put(self.url,
                                data=json.dumps(self.machine_wrong_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 400)
        
    def test_delete_unexisting_machine(self):
        """
        Test DELETE with non existing machine return correct status code 404 (Try to delete an unexisting machine)
        """
        print("("+self.test_delete_unexisting_machine.__name__+")", self.test_delete_unexisting_machine.__doc__)

        #Check that I receive status code 404
        resp = self.client.delete(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_delete_machine(self):
        """
        Test DELETE with  existing machine return correct status code 204 (Try to delete a existing machine)
        """
        print("("+self.test_delete_machine.__name__+")", self.test_delete_machine.__doc__)

        #Check that I receive status code 204
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)


if __name__ == "__main__":
    print("Start running tests")
    unittest.main()
