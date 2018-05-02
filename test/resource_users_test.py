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
initial_users = 10


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
        
        
class UsersTestCase(ResourcesAPITestCase):
    
    #new user request
    user_new_request = {
      "username" : "John",
      "password" : "123456",
      "email"    : "john@fablab.com",
      "mobile"   : "34567889",
      "website"  : "test_get_users_nonexistingusername",
      "isAdmin"  : "new full name type",
      "createdBy": "0"
    }  
    
    #Missing user name
    user_error_request = {
      "password" : "123456",
      "email"    : "john@fablab.com",
      "mobile"   : "34567889",
      "website"  : "test_get_users_nonexistingusername",
      "isAdmin"  : "new full name type",
      "createdBy": "0"
    } 

      

    url = "/fablab/api/users/"
    
    
    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        #NOTE: self.shortDescription() shuould work.
        print("("+self.test_url.__name__+")", self.test_url.__doc__, end=' ')
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.Users)
            
    def test_get_users(self):
        
        """
        Checks that GET types return correct status code and data format
        """
        print('('+self.test_get_users.__name__+')', \
              self.test_get_users.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("users"))
        self.assertEqual(resp.status_code, 200)
        # Check that I receive a collection and adequate href
        data = json.loads(resp.data.decode("utf-8"))

     #Check controls
        controls = data["@controls"]
        self.assertIn("self", controls)
        self.assertIn("fablab:add-user", controls)
        self.assertIn("fablab:reservations-all", controls)
        self.assertIn("fablab:machines-all", controls)
        
        self.assertIn("href", controls["self"])
        self.assertEqual(controls["self"]["href"], self.url)
        
    # Check that add-user control is correct
        add_user = controls["fablab:add-user"]
        self.assertIn("title", add_user)
        self.assertIn("href", add_user)
        self.assertEqual(add_user["href"], "/fablab/api/users/")
        self.assertIn("encoding", add_user)
        self.assertEqual(add_user["encoding"], "json")        
        self.assertIn("method", add_user)
        self.assertEqual(add_user["method"], "POST")
        self.assertIn("schemaUrl", add_user)
        
    
    
    # Check that reservations-all control is correct
        reservations_all = controls["fablab:reservations-all"]
        self.assertIn("title", reservations_all)
        self.assertIn("href", reservations_all)
        self.assertEqual(reservations_all["href"], "/fablab/api/reservations/")
    
    # Check that machines-all control is correct
        machines_all = controls["fablab:machines-all"]
        self.assertIn("title", machines_all)
        self.assertIn("href", machines_all)
        self.assertEqual(machines_all["href"], "/fablab/api/machines/")
        
        
        
    #Check that items are correct.
        items = data["items"]
        self.assertEqual(len(items), initial_users)
        for item in items:
            self.assertIn("username", item)
            self.assertIn("userID", item)
            self.assertIn("@controls", item)
            self.assertIn("self", item["@controls"])
            self.assertIn("href", item["@controls"]["self"])
            self.assertEqual(item["@controls"]["self"]["href"], resources.api.url_for(resources.User, username=item["username"], _external=False))
            self.assertIn("profile", item["@controls"])
            self.assertEqual(item["@controls"]["profile"]["href"], FABLAB_USER_PROFILE)
            
            
    def test_get_users_mimetype(self):
        """
        Checks that GET users return correct status code and data format
        """
        print("("+self.test_get_users_mimetype.__name__+")", self.test_get_users_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(flask.url_for("users"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_USER_PROFILE)) 
  
    def test_add_user(self):
        """
        Test adding new type to the database.
        """
        print("("+self.test_add_user.__name__+")", self.test_add_user.__doc__)

        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_new_request)
                               )
        self.assertTrue(resp.status_code == 201)
        url = resp.headers.get("Location")
        self.assertIsNotNone(url)
        resp = self.client.get(url)
        """
        self.assertTrue(resp.status_code == 200) 
        """

    def test_add_user_error(self):
        """
        Test adding new type with error of JSON _ missing typeName.
        """
        print("("+self.test_add_user_error.__name__+")", self.test_add_user_error.__doc__)

        resp = self.client.post(resources.api.url_for(resources.Users),
                                headers={"Content-Type": JSON},
                                data=json.dumps(self.user_error_request )
                               )
        self.assertTrue(resp.status_code == 400)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual(data["resource_url"], self.url)
       
        error = data["@error"]
        self.assertIn("@message", error)
        self.assertEqual(error["@message"], "Wrong request format")
        
        
        
        
    
class UserTestCase (ResourcesAPITestCase):

    #ATTENTION: json.loads return unicode
    user_req_1 = {
        
      "username" : "Axel",
      "password" : "123456",
      "email"    : "john@fablab.com",
      "mobile"   : "34567889",
      "website"  : "test_get_users_nonexistingusername",
      "isAdmin"  : "new full name type",
      "updatedBy": "0"
    }

    user_moq_req_1 = {
        
      "username" : "Axel",
      "password" : "123456",
      "email"    : "john@fablab.com",
      "mobile"   : "34567889",
      "website"  : "test_get_users_nonexistingusername",
      "isAdmin"  : "new full name type",
      "updatedBy": "0"
    }

    user_wrong_req_1 = {
      
      "email"    : "john@fablab.com",
      "mobile"   : "34567889",
      "website"  : "test_get_users_nonexistingusername",
      "isAdmin"  : "new full name type",
      "updatedBy": "0"
    }

    url_main = "/fablab/api/users/"
    
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.url = resources.api.url_for(resources.User,
                                         username="user1",
                                         _external=False)
        self.url_wrong = resources.api.url_for(resources.User,
                                               username="user100",
                                               _external=False)
        self.url_modify = resources.api.url_for(resources.User,
                                         username="user9",
                                         _external=False)

    def test_url(self):
        """
        Checks that the URL points to the right resource
        """
        _url = "/fablab/api/users/1/"
        
        print("("+self.test_url.__name__+")", self.test_url.__doc__)
        with resources.app.test_request_context(_url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEqual(view_point, resources.User)

    def test_wrong_url(self):
        """
        Checks that GET type return correct status code if given a
        wrong type
        """
        print("("+self.test_wrong_url.__name__+")", self.test_wrong_url.__doc__)
        resp = self.client.get(self.url_wrong)
        self.assertEqual(resp.status_code, 404)

                 
    def test_get_users_mimetype(self):
        """
        Checks that GET users return correct status code and data format
        """
        print("("+self.test_get_users_mimetype.__name__+")", self.test_get_users_mimetype.__doc__)

        #Check that I receive status code 200
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("Content-Type",None),
                          "{};{}".format(MASONJSON, FABLAB_USER_PROFILE)) 
    
    
    def test_modify_unexisting_machine_type(self):
        """
        Try to modify an unexisting type
        """
        print("("+self.test_modify_unexisting_machine_type.__name__+")", self.test_modify_unexisting_machine_type.__doc__)

        #Check that I receive status code 404
        resp = self.client.put(self.url_wrong,
                                data=json.dumps(self.user_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 404)

    def test_modify_machine_type(self):
        """
        Try to modify a created type
        """
        print("("+self.test_modify_machine_type.__name__+")", self.test_modify_machine_type.__doc__)

        #Check that I receive status code 204
        resp = self.client.put(self.url_modify,
                                data=json.dumps(self.user_moq_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 204)

    def test_modify_machine_type_wrong_format(self):
        """
        Try to modify a created type in wrong format
        """
        print("("+self.test_modify_machine_type_wrong_format.__name__+")", self.test_modify_machine_type_wrong_format.__doc__)

        #Check that I receive status code 400
        resp = self.client.put(self.url,
                                data=json.dumps(self.user_wrong_req_1),
                                headers={"Content-Type": JSON})
        self.assertEqual(resp.status_code, 400)   
      
    
    def test_delete_user(self):
        """
        Try to delete a created type
        """
        print("("+self.test_delete_user.__name__+")", self.test_delete_user.__doc__)

        #Check that I receive status code 204
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)
        
        
if __name__ == "__main__":
    print("Start running tests")
    unittest.main()
          
            
            
            
            
    