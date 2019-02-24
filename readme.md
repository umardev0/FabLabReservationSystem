# PWP20 - FabLab reservation API
In this implementation, we(Umar, Daniel, Sofeem and Murad) followed the example code from Programable web project by Ivan and Mika, University of Oulu

The database is generated from SQLite (https://www.sqlite.org/index.html)

There are two ways to setup and populate the database:

1. Run SQL scripts in /db/*dump.sql 

2. Run API function create_tables and populate_tables

To run the tests of database:

1. Go to the root of the repository

2. To test methods associated to the tables run the following code:
```python
python -m test.TEST_MODULE_NAME
```

For example:
To test methods associated to the machine table run the following code
```python
python -m test.database_api_tests_message
```
To test methods associated to the user table run the following code:
```python
python -m test.database_api_tests_user
```
3. If you want to avoid that one test case is executed, you have to  decorate the corresponding method with the decorator:
```python
@unittest.skip("write reason of skip")
```
4. If you want to run just one test method isolated from the rest you can use the following code: 
```python
python -m unittest test.YOUR_TEST_MODULE.YOUR_TEST_CLASS.YOUR_TEST_METHOD
```
# Database functions:
class Engine(object):

    def __init__(self, db_path=None):


    def connect(self):


    def remove_database(self):


    def clear(self):

    #METHODS TO CREATE AND POPULATE A DATABASE USING SQL FILES
    def create_tables(self, schema=None):

    def populate_tables(self, dump=None):
 

class Connection(object):
    
    def __init__(self, db_path):


    def isclosed(self):


    def close(self):


    #FOREIGN KEY STATUS
    def check_foreign_keys_status(self):

    def set_foreign_keys_support(self):

    def unset_foreign_keys_support(self):

    #HELPERS
    #Here the helpers that transform database rows into dictionary. They work
    #similarly to ORM

    #Helpers for machine
    def _create_machine_object(self, row):

    def _create_machine_list_object(self, row):


    #Helpers for users
    def _create_user_object(self, row):

    def _create_user_list_object(self, row):


    #Helpers for type
    def _create_type_object(self, row):
        
    def _create_type_list_object(self, row):

        
    #Helpers for message
    def _create_message_object(self, row):

    def _create_message_list_object(self, row):
       
    def _create_reservation_list_object(self, row):

    def get_messages(self, fromUserID=None, number_of_messages=-1,

    def delete_message(self, messageid):

    def create_message(self, content, fromUserID,
                       toUserID):

    def create_user(self, username, password, email = None, mobile = None, website = None, isAdmin='0', createdBy='0'):

    #API ITSELF
    #Message Table API.
    def get_message(self, messageid):

    def get_messages(self, fromUserID=None, number_of_messages=-1,

    def delete_message(self, messageid):

    def create_message(self, content, fromUserID,        


    #MACHINE API
    def get_machine(self, machineID):
        
    def get_machines(self, typeName=None):
        
    def delete_machine(self, machineID):

    def modify_machine(self, machineID, machinename, typeID, tutorial, updatedBy = '0'):

    def create_machine(self, machinename, typeID, tutorial, createdBy='0'):
         

    #TYPE API
    def get_type(self, typeName):

    def get_types(self):

    def delete_type(self, typeName):
        
    def modify_type(self, typeID, typeName, pastProject, updatedBy= '0'):
       
    def create_type(self, typeName, pastProject, createdBy='0'):
        

    # RESERVATION API
    def get_reservation_list(self, userID = None, machineID = None, startTime=-1, endTime=-1):

    def get_active_reservation_list(self, userID = None, machineID = None, startTime=-1, endTime=-1):
        
    def get_reservation (self, reservationID):
        
    def modify_reservation (self, reservationID, startTime, endTime, updatedBy = '0'):
                
    def disable_reservation (self, reservationID, updatedBy = '0'):
            
    def delete_500_oldest_reservations (self):
        
    def create_reservation(self, userID, machineID, startTime=None, endTime=None, createdBy = '0'):
        

        
    #ACCESSING THE USERS tables
    def get_users(self):
        
    def get_user(self, username):

    def create_user(self, username, password, email = None, mobile = None, website = None, isAdmin='0', createdBy='0'):
        
    def delete_user(self, nickname):

    def modify_user(self, username, password, email = None, mobile= None, website = None, updatedBy = '0'):

    def change_role_user(self, username, isAdmin='0', updatedBy='0'):
  
# 
