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

    #Anonymous type
    machine_type_new_request = {
      "typeName" : "new_test_type",
      "typeFullname" : "new full name type",
      "pastProject" : "http://www.fablab.oulu.fi/",
      "createdBy" : "1"
    }   

    #Existing type
    machine_type_error_request = {
      "typeFullname" : "new full name type",
      "pastProject" : "http://www.fablab.oulu.fi/"
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
        Checks that GET types return correct status code and data format
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
        machines_all = controls["fablab:machines-all"]
        self.assertIn("title", machines_all)
        self.assertIn("href", machines_all)
        self.assertEqual(machines_all["href"], "/fablab/api/machines/")

        #Check that add-message control is correct
        add_type = controls["fablab:add-machinetype"]
        self.assertIn("title", add_type)
        self.assertIn("href", add_type)
        self.assertEqual(add_type["href"], "/fablab/api/machinetypes/")
        self.assertIn("encoding", add_type)
        self.assertEqual(add_type["encoding"], "json")        
        self.assertIn("method", add_type)
        self.assertEqual(add_type["method"], "POST")
        self.assertIn("schemaUrl", add_type)

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


class MachineTypeTestCase (ResourcesAPITestCase):

    #ATTENTION: json.loads return unicode
    type_req_1 = {
        "typeName": "3d_printers",
        "typeFullname": "New 3D Printers",
        "pastProject": "http://www.oulu.fi/fablab/projects",
        "updatedBy": 1
    }

    type_moq_req_1 = {
        "typeFullname": "New 3D Printers",
        "pastProject": "http://www.oulu.fi/fablab/projects",
        "updatedBy": 1
    }

    type_wrong_req_1 = {
        "typeFullname": "New 3D Printers",
        "pastProject": "http://www.oulu.fi/fablab/projects",
        "updatedBy": 1
    }

    url_main = "/fablab/api/machines/"
    def setUp(self):
        super(MachineTypeTestCase, self).setUp()
        self.url = resources.api.url_for(resources.MachineType,
                                         typeID="1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.MachineType,
                                               typeID="100",
                                               _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        _url = "/fablab/api/machinetypes/1/"
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.MachineType)

    def test_wrong_url(self):
        """
        Checks that GET type return correct status code if given a
        wrong type
        """
        print("("+self.test_wrong_url.__name__+")", self.test_wrong_url.__doc__)
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)


    def test_get_machine_type(self):
        """
        Checks that GET type return correct status code and data format
        """
        print("("+self.test_get_machine_type.__name__+")", self.test_get_machine_type.__doc__)
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
            
            reply_ctrl = controls["fablab:machines-all"]
            self.assertIn("title", reply_ctrl)
            self.assertIn("href", reply_ctrl)
            self.assertEqual(reply_ctrl["href"], self.url_main)
            
            #Check rest attributes
            self.assertIn("typeID", data)
            self.assertIn("typeName", data)
            self.assertIn("typeFullname", data)
            self.assertIn("pastProject", data)

    def test_get_machine_type_mimetype(self):
        """
        Checks that GET type return correct status code and data format
        """
        print("("+self.test_get_machine_type_mimetype.__name__+")", self.test_get_machine_type_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_MACHINE_TYPE_PROFILE))

    def test_modify_unexisting_machine_type(self):
        """
        Try to modify an unexisting type
        """
        print("("+self.test_modify_unexisting_machine_type.__name__+")", self.test_modify_unexisting_machine_type.__doc__)

        #Check that I receive status code 404
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.type_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    def test_modify_machine_type(self):
        """
        Try to modify a created type
        """
        print("("+self.test_modify_machine_type.__name__+")", self.test_modify_machine_type.__doc__)

        #Check that I receive status code 204
        resp = self.client.put(self.url,
                                data=json.dumps(self.type_moq_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

    def test_modify_machine_type_wrong_format(self):
        """
        Try to modify a created type in wrong format
        """
        print("("+self.test_modify_machine_type_wrong_format.__name__+")", self.test_modify_machine_type_wrong_format.__doc__)

        #Check that I receive status code 204
        resp = self.client.put(self.url,
                                data=json.dumps(self.type_wrong_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 400)
        
    def test_delete_unexisting_machine_type(self):
        """
        Try to delete an unexisting type
        """
        print("("+self.test_delete_unexisting_machine_type.__name__+")", self.test_delete_unexisting_machine_type.__doc__)

        #Check that I receive status code 204
        resp = self.client.delete(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

    def test_delete_machine_type(self):
        """
        Try to delete a created type
        """
        print("("+self.test_delete_machine_type.__name__+")", self.test_delete_machine_type.__doc__)

        #Check that I receive status code 204
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)

if __name__ == "__main__":
    print("Start running tests")
    unittest.main()
