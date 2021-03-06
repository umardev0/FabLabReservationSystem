import json

from urllib.parse import unquote

from flask import Flask, request, Response, g, _request_ctx_stack, redirect, send_from_directory
from flask_restful import Resource, Api, abort
from werkzeug.exceptions import NotFound,  UnsupportedMediaType

from fablab.utils import RegexConverter
from fablab import database

#Constants for hypermedia formats and profiles
MASON = "application/vnd.mason+json"
JSON = "application/json"
FABLAB_USER_PROFILE = "/profiles/user-profile/"
FABLAB_MACHINE_TYPE_PROFILE = "/profiles/machine-type-profile/"
FABLAB_MACHINE_PROFILE = "/profiles/machine-profile/"
FABLAB_RESERVATION_PROFILE = "/profiles/reservation-profile/"
FABLAB_HISTORY_PROFILE = "/profiles/history-profile/"
ERROR_PROFILE = "/profiles/error-profile"

ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

# Fill these in
#Fill with the correct Apiary url"
STUDENT_APIARY_PROJECT = "https://fablabreservationapi.docs.apiary.io"
APIARY_PROFILES_URL = STUDENT_APIARY_PROJECT+"/#reference/profiles/"
APIARY_RELS_URL = STUDENT_APIARY_PROJECT+"/#reference/link-relations/"

USER_SCHEMA_URL = "/fablab/schema/user/"
LINK_RELATIONS_URL = "/fablab/link-relations/"

#Define the application and the api
app = Flask(__name__, static_folder="static", static_url_path="/.")
app.debug = True
# Set the database Engine. In order to modify the database file (e.g. for
# testing) provide the database path   app.config to modify the
#database to be used (for instance for testing)
app.config.update({"Engine": database.Engine()})
#Start the RESTful API.
api = Api(app)

# These two classes below are how we make producing the resource representation
# JSON documents manageable and resilient to errors. As noted, our mediatype is
# Mason. Similar solutions can easily be implemented for other mediatypes.

class MasonObject(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs

class FablabObject(MasonObject):
    """
    A convenience subclass of MasonObject that defines a bunch of shorthand
    methods for inserting application specific objects into the document. This
    class is particularly useful for adding control objects that are largely
    context independent, and defining them in the resource methods would add a
    lot of noise to our code - not to mention making inconsistencies much more
    likely!

    In the forum code this object should always be used for root document as
    well as any items in a collection type resource.
    """

    def __init__(self, **kwargs):
        """
        Calls dictionary init method with any received keyword arguments. Adds
        the controls key afterwards because hypermedia without controls is not
        hypermedia.
        """

        super(FablabObject, self).__init__(**kwargs)
        self["@controls"] = {}

    def add_control_endpoints(self, endpointsList):
        """
        Adds endpoints to an object
        """
        endpoints = []
        for item in endpointsList:
            if item == 'Machines':
                endpoints.append({"endpointUrl": api.url_for(Machines),"title": item})
            elif item == 'MachineTypes':
                endpoints.append({"endpointUrl": api.url_for(MachineTypes),"title": item})
            elif item == 'Reservations':
                endpoints.append({"endpointUrl": api.url_for(Reservations),"title": item})

        self["@controls"]["endpoints"] = endpoints

    def add_control_users_schema(self):
        """
        Adds the users schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/users/",
            "title": "users schema"
        }

    def add_control_user_schema(self):
        """
        Adds the user schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/user/",
            "title": "user schema"
        }

    def add_control_machines_schema(self):
        """
        Adds the machines schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/machines/",
            "title": "machines schema"
        }

    def add_control_machine_schema(self):
        """
        Adds the machine schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/machine/",
            "title": "machine schema"
        }

    def add_control_machinetypes_schema(self):
        """
        Adds the machinetypes schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/machinetypes/",
            "title": "machinetypes schema"
        }

    def add_control_machinetype_schema(self):
        """
        Adds the machinetype schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/machinetype/",
            "title": "machinetype schema"
        }

    def add_control_reservations_schema(self):
        """
        Adds the reservations schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/reservations/",
            "title": "reservations schema"
        }

    def add_control_reservation_schema(self):
        """
        Adds the reservation schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/reservation/",
            "title": "reservation schema"
        }

    def add_control_history_schema(self):
        """
        Adds the history schema link to an object
        """

        self["@controls"]["schema"] = {
            "schemaUrl": "/fablab/schema/history/",
            "title": "history schema"
        }

    def add_control_machinetypes_all(self):
        """
        Adds the machine type-all link to an object. Intended for the document object.
        """

        self["@controls"]["fablab:machinetypes-all"] = {
            "href": api.url_for(MachineTypes),
            "title": "All machine type"
        }

    def add_control_users_all(self):
        """
        This adds the users-all link to an object. Intended for the document object.
        """

        self["@controls"]["fablab:users-all"] = {
            "href": api.url_for(Users),
            "title": "List users"
        }

    def add_control_machines_all(self):
        """
        This adds the users-all link to an object. Intended for the document object.
        """

        self["@controls"]["fablab:machines-all"] = {
            "href": api.url_for(Machines),
            "title": "List machines"
        }

    def add_control_reservations_all(self):
        """
        This adds the users-all link to an object. Intended for the document object.
        """

        self["@controls"]["fablab:reservations-all"] = {
            "href": api.url_for(Reservations),
            "title": "List reservations"
        }

    def add_control_add_user(self):
        """
        This adds the add-user control to an object. Intended ffor the
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["@controls"]["add"] = {
            "href": api.url_for(Users),
            "title": "Create user",
            "encoding": "json",
            "method": "POST",
            "schemaUrl": "/fablab/schema/add_user/"
        }

    def add_control_add_machinetype(self):
        """
        This adds the add-user control to an object. Intended ffor the
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["@controls"]["add"] = {
            "href": api.url_for(MachineTypes),
            "title": "Create machine type",
            "encoding": "json",
            "method": "POST",
            "schemaUrl": "/fablab/schema/add_machinetype/"
        }

    def add_control_add_machine(self):
        """
        This adds the add-user control to an object. Intended ffor the
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["@controls"]["add"] = {
            "href": api.url_for(Machines),
            "title": "Create machine",
            "encoding": "json",
            "method": "POST",
            "schemaUrl": "/fablab/schema/add_machine/"
        }

    def add_control_add_reservation(self):
        """
        This adds the add-user control to an object. Intended ffor the
        document object. Instead of adding a schema dictionary we are pointing
        to a schema url instead for two reasons: 1) to demonstrate both options;
        2) the user schema is relatively large.
        """

        self["@controls"]["add"] = {
            "href": api.url_for(Reservations),
            "title": "Create reservation",
            "encoding": "json",
            "method": "POST",
            "schemaUrl": "/fablab/schema/add_reservation/"
        }

    def add_control_edit_user(self, username):
        """
        Adds a the edit control to a message object. For the schema we need
        the one that's intended for editing (it has editor instead of author).

        : param str msgid: message id in the msg-N form
        """

        self["@controls"]["edit"] = {
            "href": api.url_for(User, username=username),
            "title": "Edit this user",
            "encoding": "json",
            "method": "PUT",
            "schema": self._user_schema()
        }

    def add_control_delete_user(self, username):
        """
        Adds the delete control to an object. This is intended for any
        object that represents a user.

        : param str username: The username of the user to remove
        """

        self["@controls"]["forum:delete"] = {
            "href": api.url_for(User, username=username),
            "title": "Delete this user",
            "method": "DELETE"
        }

    def add_control_edit_machinetype(self, typeID):
        """
        Adds a the edit control to a message object. For the schema we need
        the one that's intended for editing (it has editor instead of author).

        : param str msgid: message id in the msg-N form
        """

        self["@controls"]["edit"] = {
            "href": api.url_for(MachineType, typeID=typeID),
            "title": "Edit this machine type",
            "encoding": "json",
            "method": "PUT",
            "schema": self._machine_type_schema()
        }

    def add_control_edit_machine(self, machineID):
        """
        Adds a the edit control to a message object. For the schema we need
        the one that's intended for editing (it has editor instead of author).

        : param str msgid: message id in the msg-N form
        """

        self["@controls"]["edit"] = {
            "href": api.url_for(Machine, machineID=machineID),
            "title": "Edit this machine",
            "encoding": "json",
            "method": "PUT",
            "schema": self._machine_schema()
        }

    def add_control_edit_reservation(self, reservationID):
        """
        Adds a the edit control to a message object. For the schema we need
        the one that's intended for editing (it has editor instead of author).

        : param str msgid: message id in the msg-N form
        """

        self["@controls"]["edit"] = {
            "href": api.url_for(Reservation, reservationID=reservationID),
            "title": "Edit this reservation",
            "encoding": "json",
            "method": "PUT",
            "schema": self._reservation_schema()
        }

    def add_control_delete_machinetype(self, typeID):
        """
        Adds the delete control to an object. This is intended for any
        object that represents a user.

        : param str username: The username of the user to remove
        """

        self["@controls"]["delete"] = {
            "href": api.url_for(MachineType, typeID=typeID),
            "title": "Delete this machine type",
            "method": "DELETE"
        }

    def add_control_delete_machine(self, machineID):
        """
        Adds the delete control to an object. This is intended for any
        object that represents a user.

        : param str username: The username of the user to remove
        """

        self["@controls"]["delete"] = {
            "href": api.url_for(Machine, machineID=machineID),
            "title": "Delete this machine",
            "method": "DELETE"
        }

    def add_control_machine_history(self, machineID):
        """
        This adds the reservations history control to a machine which defines a href
        template for making queries. In Mason query parameters are defined with
        a schema just like forms.

        : param str machineID: machineID of the machine
        """

        self["@controls"]["fablab:history-reservations"] = {
            "href": api.url_for(History, machineID=machineID).rstrip("/") + "{?length,before,after,active}",
            "title": "Reservation history",
            "isHrefTemplate": True,
            "schema": self._history_schema()
        }

    def _user_schema(self):
        """
        Creates a schema dictionary for editing public profiles of users.

        :rtype:: dict
        """

        schema = {
            "type": "object",
            "properties": {},
            "required": ["username", "password"]
        }

        props = schema["properties"]
        props["password"] = {
            "description": "User's new password",
            "title": "password",
            "type": "string"
        }
        props["email"] = {
            "description": "User's new email",
            "title": "email",
            "type": "string"
        }
        props["mobile"] = {
            "description": "User's new mobile",
            "title": "mobile",
            "type": "string"
        }
        props["website"] = {
            "description": "User's new website",
            "title": "website",
            "type": "string"
        }
        props["updatedBy"] = {
            "description": "User who updated this record ",
            "title": "updatedBy",
            "type": "integer"
        }

        return schema

    def _machine_type_schema(self):
        """
        Creates a schema dictionary for messages. If we're editing a message
        the editor field should be set. If the message is new, the author field
        should be set instead. This is controlled by the edit flag.

        This schema can also be accessed from the urls /forum/schema/edit-msg/ and
        /forum/schema/add-msg/.

        : param bool edit: is this schema for an edit form
        : rtype:: dict
        """

        schema = {
            "type": "object",
            "properties": {},
            "required": ["typeName", "typeFullname","pastProject"]
        }

        props = schema["properties"]
        props["typeName"] = {
            "title": "Type Name",
            "description": "The type of machine",
            "type": "string"
        }
        props["typeFullname"] = {
            "title": "Type Full Name",
            "description": "The full name of machine type",
            "type": "string"
        }
        props["pastProject"] = {
            "title": "Past Projects",
            "description": "Previous projects made by this type",
            "type": "string"
        }
        props["updatedBy"] = {
            "title": "Updated By",
            "description": "UserID whom modified the type",
            "type": "integer"
        }

        return schema

    def _machine_schema(self):
        """
        Creates a schema dictionary for messages. If we're editing a message
        the editor field should be set. If the message is new, the author field
        should be set instead. This is controlled by the edit flag.

        This schema can also be accessed from the urls /forum/schema/edit-msg/ and
        /forum/schema/add-msg/.

        : param bool edit: is this schema for an edit form
        : rtype:: dict
        """

        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        props = schema["properties"]
        props["machinename"] = {
            "title": "Machine Name",
            "description": "The model of machine",
            "type": "string"
        }
        return schema

    def _reservation_schema(self):
        """
        Creates a schema dictionary for messages. If we're editing a message
        the editor field should be set. If the message is new, the author field
        should be set instead. This is controlled by the edit flag.

        This schema can also be accessed from the urls /forum/schema/edit-msg/ and
        /forum/schema/add-msg/.

        : param bool edit: is this schema for an edit form
        : rtype:: dict
        """

        schema = {
            "type": "object",
            "properties": {},
            "required": ["reservationID","updatedBy"]
        }

        props = schema["properties"]
        props["reservationID"] = {
            "title": "Reservation ID",
            "description": "The ID of reservation to be disable",
            "type": "integer"
        }
        props["updatedBy"] = {
            "title": "Updated By",
            "description": "UserID whom disable the reservation",
            "type": "integer"
        }
        return schema

    def _history_schema(self):
        """
        Creates a schema dicionary for the reservations history query parameters.

        This schema can also be accessed from /forum/schema/history-query/

        :rtype:: dict
        """

        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }

        props = schema["properties"]
        props["length"] = {
            "description": "Maximum number of reservations returned",
            "type": "integer"
        }
        props["before"] = {
            "description": "Find reservations before (timestamp as seconds)",
            "type": "integer"
        }
        props["after"] = {
            "description": "Find reservations after (timestamp as seconds)",
            "type": "integer"
        }
        props["active"] = {
            "description": "Find reservations based on active state. 1 for active, 0 for inactive, default -1 for all",
            "type": "integer"
        }

        return schema

#ERROR HANDLERS

def create_error_response(status_code, title, message=None):
    """
    Creates a: py: class:`flask.Response` instance when sending back an
    HTTP error response

    : param integer status_code: The HTTP status code of the response
    : param str title: A short description of the problem
    : param message: A long description of the problem
    : rtype:: py: class:`flask.Response`
    """

    resource_url = None
    #We need to access the context in order to access the request.path
    ctx = _request_ctx_stack.top
    if ctx is not None:
        resource_url = request.path
    envelope = MasonObject(resource_url=resource_url)
    envelope.add_error(title, message)

    return Response(json.dumps(envelope), status_code, mimetype=MASON+";"+ERROR_PROFILE)

@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found",
                                 "This resource url does not exit")

@app.errorhandler(400)
def resource_not_found(error):
    return create_error_response(400, "Malformed input format",
                                 "The format of the input is incorrect")

@app.errorhandler(415)
def unknown_error(error):
    return create_error_response(415, "Unsupported media type",
                    "Use a JSOn compatible format")

@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error",
                    "The system has failed. Please, contact the administrator")

@app.before_request
def connect_db():
    """
    Creates a database connection before the request is proccessed.

    The connection is stored in the application context variable flask.g .
    Hence it is accessible from the request object.
    """

    g.con = app.config["Engine"].connect()

#HOOKS
@app.teardown_request
def close_connection(exc):
    """
    Closes the database connection
    Check if the connection is created. It migth be exception appear before
    the connection is created.
    """

    if hasattr(g, "con"):
        g.con.close()

#Define the resources
class MachineTypes(Resource):
    """
    Resource MachineTypes implementation
    """

    def get(self):
        """
        Get all machine types.

        INPUT parameters:
          None

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: Machine Type Profile
          /profiles/machine_type_profile

        """

        types_db = g.con.get_types()

        envelope = FablabObject()
        envelope.add_namespace("fablab", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(MachineTypes))
        envelope.add_control_add_machinetype()
        envelope.add_control_machines_all()
        envelope.add_control_machinetypes_schema()
        envelope.add_control_endpoints(['MachineTypes', 'Machines'])

        items = envelope["items"] = []

        for type in types_db:
            item = FablabObject(id=type["typeID"], typeName=type["typeName"], typeFullname=type["typeFullname"])
            item.add_control("self", href=api.url_for(MachineType, typeID=type["typeID"]))
            item.add_control("profile", href=FABLAB_MACHINE_TYPE_PROFILE)
            items.append(item)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_MACHINE_TYPE_PROFILE)

    def post(self):
        """
        Adds a new machine type.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: Machine Type Profile
          /profiles/machine_type_profile


        The body should be a JSON document that matches the schema for new messages
        If author is not there consider it  "Anonymous".

        RESPONSE STATUS CODE:
         * Returns 201 if the new machine type has been added correctly.
           The Location header contains the path of the new new machine type
         * Returns 400 if the new machine type is not well formed or the entity body is
           empty.
         * Returns 415 if the format of the response is not json
         * Returns 500 if the new machine type could not be added to database.

        """

        #Extract the request body. In general would be request.data
        #Since the request is JSON I use request.get_json
        #get_json returns a python dictionary after serializing the request body
        #get_json returns None if the body of the request is not formatted
        # using JSON. We use force=True since the input media type is not
        # application/json.

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")
        request_body = request.get_json(force=True)
         #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            typeName = request_body["typeName"]
            typeFullname = request_body["typeFullname"]
            pastProject = request_body.get("pastProject", "")
            createdBy = request_body.get("createdBy", "")

        except KeyError:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include message title and body")
        #Create the new machine type and build the response code"
        newType = g.con.create_type(typeName, typeFullname, pastProject, createdBy)
        if not newType:
            return create_error_response(500, "Problem with the database",
                                         "Cannot access the database")

        #Create the Location header with the id of the new machine type created
        url = api.url_for(MachineTypes)

        #RENDER
        #Return the response
        return Response(json.dumps({"id":str(newType)}),status=201, headers={"Location": url})

class MachineType(Resource):

    def get(self, typeID):
        """
        Get name and information of a specific Machine Type.

        Returns status code 404 if the typeID does not exist in the database.

        INPUT PARAMETER
       : param str typeID: The id of the Machine Type to be retrieved from the
            system

        RESPONSE ENTITY BODY:
         * Media type: application/vnd.mason+json:
             https://github.com/JornWildt/Mason
         * Profile: Machine Type Profile
          /profiles/machine_type_profile

        RESPONSE STATUS CODE
         * Return status code 200 if everything OK.
         * Return status code 404 if the Machine Type was not found in the database.

        """

        #PEFORM OPERATIONS INITIAL CHECKS
        #Get the type from db
        message_db = g.con.get_type(typeID)
        if not message_db:
            abort(404, message="There is no type with id %s" % typeID,
                       resource_type="MachineType",
                       resource_url=request.path,
                       resource_id=typeID)

        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = FablabObject(
            typeID=message_db["typeID"],
            typeName=message_db["typeName"],
            typeFullname=message_db["typeFullname"],
            pastProject=message_db["pastProject"],
            createdAt=message_db["createdAt"],
            updatedAt=message_db["updatedAt"],
            createdBy=message_db["createdBy"],
            updatedBy=message_db["updatedBy"]
        )

        envelope.add_namespace("fablab", LINK_RELATIONS_URL)
        envelope.add_namespace("atom-thread", ATOM_THREAD_PROFILE)

        envelope.add_control_machines_all()
        envelope.add_control_users_all()
        envelope.add_control_edit_machinetype(typeID)
        envelope.add_control_delete_machinetype(typeID)
        envelope.add_control_users_all()
        envelope.add_control("profile", href=FABLAB_MACHINE_TYPE_PROFILE)
        envelope.add_control("collection", href=api.url_for(MachineTypes))
        envelope.add_control("self", href=api.url_for(MachineType, typeID=typeID))
        envelope.add_control_machinetype_schema()

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_MACHINE_TYPE_PROFILE)


    def delete(self, typeID):
        """
        Deletes a Machine Type from the FabLab API.

        INPUT PARAMETERS:
       : param str typeID: The id of the Machine Type to be deleted

        RESPONSE STATUS CODE
         * Returns 204 if the Machine Type was deleted
         * Returns 404 if the typeID is not associated to any message.
        """

        #PERFORM DELETE OPERATIONS
        if g.con.delete_type(typeID):
            return "", 204
        else:
            #Send error message
            return create_error_response(404, "Unknown type",
                                         "There is no a type with name %s" % typeID
                                        )

    def put(self, typeID):
        """
        Modifies information of specific Machine Type.

        INPUT PARAMETERS:
       : param str typeiD: The id of the Machine Type to be modified

        REQUEST ENTITY BODY:
        * Media type: JSON

         * Profile: Machine Type Profile
          /profiles/machine_type_profile

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: Machine Type Profile
          /profiles/machine_type_profile

        The body should be a JSON document that matches the schema for editing messages
        If author is not there consider it  "Anonymous".

        OUTPUT:
         * Returns 204 if the Machine Type is modified correctly
         * Returns 400 if the body of the request is not well formed or it is
           empty.
         * Returns 404 if there is no Machine Type with typeID
         * Returns 415 if the input is not JSON.
         * Returns 500 if the database cannot be modified

        """

        #CHECK THAT TYPE EXISTS
        if not g.con.contains_type(typeID):
            return create_error_response(404, "Type not found",
                                         "There is no type with ID %s" % typeID
                                        )

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")
        request_body = request.get_json(force=True)
         #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            typeName = request_body["typeName"]
            typeFullname = request_body["typeFullname"]
            pastProject = request_body.get("pastProject", "")
            updatedBy = request_body.get("updatedBy", "")

        except KeyError:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include typeName and typeFullname")
        else:
            #Modify the Machine Type in the database
            if not g.con.modify_type(typeID, typeName, typeFullname, pastProject, updatedBy):
                return create_error_response(500, "Internal error",
                                         "Type information for %s cannot be updated" % typeName
                                        )
            return "", 204

class Reservations(Resource):
    """
    Resource Reservations implementation
    """

    def get(self):
        """
        Get all Reservations.

        INPUT parameters:
          None

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: FabLab Reservation
          /profiles/reservation_profile

        """

        #Extract reservations from database
        reservation_db = g.con.get_reservation_list()

        envelope = FablabObject()
        envelope.add_namespace("fablab", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(Reservations))
        envelope.add_control_add_reservation()
        envelope.add_control_machines_all()
        envelope.add_control_users_all()
        envelope.add_control_reservations_schema()
        envelope.add_control_endpoints(['Reservations', 'Machines'])

        items = envelope["items"] = []

        for type in reservation_db:
            item = FablabObject(reservationID=type["reservationID"], userID=type["userID"], machineID=type["machineID"])
            item.add_control("self", href=api.url_for(Reservation, reservationID=type["reservationID"]))
            item.add_control("profile", href=FABLAB_RESERVATION_PROFILE)
            items.append(item)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_RESERVATION_PROFILE)

    def post(self):
        """
        Adds a new Reservation.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: FabLab Reservation
          /profiles/reservation_profile


        The body should be a JSON document that matches the schema for new Reservation

        RESPONSE STATUS CODE:
         * Returns 201 if the Reservation has been added correctly.
           The Location header contains the path of the new Reservation
         * Returns 400 if the Reservation is not well formed or the entity body is
           empty.
         * Returns 415 if the format of the response is not json
         * Returns 500 if the Reservation could not be added to database.

        """

        #Extract the request body. In general would be request.data
        #Since the request is JSON I use request.get_json
        #get_json returns a python dictionary after serializing the request body
        #get_json returns None if the body of the request is not formatted
        # using JSON. We use force=True since the input media type is not
        # application/json.

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")
        request_body = request.get_json(force=True)
         #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            userID = request_body["userID"]
            machineID = request_body["machineID"]
            startTime = request_body["startTime"]
            endTime = request_body["endTime"]

        except KeyError:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Please recheck your request")
        #Create the new message and build the response code"
        newType = g.con.create_reservation(userID, machineID, startTime, endTime, userID)
        if not newType:
            return create_error_response(500, "Problem with the database",
                                         "Cannot access the database")

        #Create the Location header with the id of the message created
        url = api.url_for(Reservation, reservationID=newType)

        #RENDER
        #Return the response
        return Response(json.dumps({"id":str(newType)}),status=201, headers={"Location": url})

class Reservation(Resource):

    def get(self, reservationID):
        """
        Get name and information of a specific Reservation.

        Returns status code 404 if the reservationID does not exist in the database.

        INPUT PARAMETER
       : param str typeID: The id of the Machine Type to be retrieved from the
            system

        RESPONSE ENTITY BODY:
         * Media type: application/vnd.mason+json:
             https://github.com/JornWildt/Mason
         * Profile: FabLab Reservation
          /profiles/reservation_profile

        RESPONSE STATUS CODE
         * Return status code 200 if everything OK.
         * Return status code 404 if the Reservation was not found in the database.

        """

        #PEFORM OPERATIONS INITIAL CHECKS
        #Get the message from db
        message_db = g.con.get_reservation(reservationID)
        if not message_db:
            abort(404, message="There is no Reservation with id %s" % reservationID,
                       resource_type="Reservation",
                       resource_url=request.path,
                       resource_id=reservationID)

        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = FablabObject(
            userID=message_db["userID"],
            machineID=message_db["machineID"],
            startTime=message_db["startTime"],
            endTime=message_db["endTime"],
            isActive=message_db["isActive"],
            createdAt=message_db["createdAt"],
            updatedAt=message_db["updatedAt"],
            createdBy=message_db["createdBy"],
            updatedBy=message_db["updatedBy"]
        )

        envelope.add_namespace("fablab", LINK_RELATIONS_URL)
        envelope.add_namespace("atom-thread", ATOM_THREAD_PROFILE)
#---DANIEL : NEED TO ADD SOME LINK FOR USER & MACHINE HERE---
        envelope.add_control_edit_reservation(reservationID)
        envelope.add_control_users_all()
        envelope.add_control("profile", href=FABLAB_RESERVATION_PROFILE)
        envelope.add_control("collection", href=api.url_for(Reservations))
        envelope.add_control("self", href=api.url_for(Reservation, reservationID=reservationID))
        envelope.add_control_reservation_schema()

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_RESERVATION_PROFILE)


    def put(self, reservationID):
        """
        Disable the reservation.

        INPUT PARAMETERS:
       : param str reservationID: The id of the reservation to be disable

        REQUEST ENTITY BODY:
        * Media type: JSON

         * Profile: FabLab Reservation
          /profiles/reservation_profile

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: FabLab Reservation
          /profiles/reservation_profile

        OUTPUT:
         * Returns 204 if the Reservation is modified correctly
         * Returns 400 if the body of the request is not well formed or it is
           empty.
         * Returns 404 if there is no Reservation with reservationID
         * Returns 415 if the input is not JSON.
         * Returns 500 if the database cannot be modified

        """

        #CHECK THAT RESERVATION EXISTS
        if not g.con.contains_reservation(reservationID):
            return create_error_response(404, "Type not found",
                                         "There is no reservation with ID %s" % reservationID
                                        )

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")
        request_body = request.get_json(force=True)
         #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed

        try:
            updatedBy = request_body["updatedBy"]

        except KeyError:
            #This is launched if either title or body does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include a userID only")

        else:
            #Modify the message in the database
            if not g.con.disable_reservation(reservationID, updatedBy):
                return create_error_response(500, "Internal error",
                                         "Reservation %s cannot be disable" % reservationID
                                        )
            return "", 204


class Users(Resource):

    def get(self):
        """
        Gets a list of all the users in the database.

        It returns always status code 200.

        RESPONSE ENTITITY BODY:

         OUTPUT:
            * Media type: application/vnd.mason+json
                https://github.com/JornWildt/Mason
            * Profile: Fablab_User
                /profiles/user-profile

        Link relations used in items:

        Semantic descriptions used in items: username and UserID

        Link relations used in links: add_user, reservations_all, machines_all

        Semantic descriptors used in template: userID, username, email, mobile, website, isAdmin

        NOTE:
         * The attributes match one-to-one with column names in the
           database.
        """
        #PERFORM OPERATIONS
        #Create the users list
        users_db = g.con.get_users()

        #FILTER AND GENERATE THE RESPONSE
       #Create the envelope
        envelope = FablabObject()

        envelope.add_namespace("fablab", LINK_RELATIONS_URL)

        envelope.add_control_add_user()
        envelope.add_control_reservations_all()
        envelope.add_control_machines_all()
        envelope.add_control("self", href=api.url_for(Users))
        envelope.add_control_users_schema()
        envelope.add_control_endpoints(['Machines', 'MachineTypes', 'Reservations'])

        items = envelope["items"] = []

        for user in users_db:
            item = FablabObject(
                username=user["username"],
                userID=user["userID"]
            )
            item.add_control("self", href=api.url_for(User, username=user["username"]))
            item.add_control("profile", href=FABLAB_USER_PROFILE)
            items.append(item)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_USER_PROFILE)

    def post(self):
        """
        Adds a new user in the database.

        REQUEST ENTITY BODY:
         * Media type: JSON
         * Profile: Fablab_User


        Semantic descriptors used in template: username(mandatory),
        password(mandatory), email(optional),mobile(optional),
        website(optional), isAdmin(optional), createdBy(optional).

        RESPONSE STATUS CODE:
         * Returns 201 + the url of the new resource in the Location header
         * Return 409 Conflict if there is another user with the same username
         * Return 400 if the body is not well formed
         * Return 415 if it receives a media type != application/json

        NOTE:
         * The attributes match one-to-one with column names in the
           database.

        NOTE:
        The: py: method:`Connection.create_user()` receives as a parameter a
        dictionary with the following format.
        {"username":"", "password":"", "email":"", "mobile":"",
        "website":"", "isAdmin":"", "createdBy":""}

        """

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
        #Get the request body and serialize it to object
        #We should check that the format of the request body is correct. Check
        #That mandatory attributes are there.

        # pick up username so we can check for conflicts
        try:
            username = request_body["username"]
        except KeyError:
            return create_error_response(400, "Wrong request format", "User's username was missing from the request")

        #Conflict if user already exist
        if g.con.contains_user(username):
            return create_error_response(409, "Wrong username",
                                         "There is already a user with same"
                                         "username:%s." % username)

        # pick up rest of the mandatory fields
        try:
            password = request_body["password"]
            email = request_body.get("email", "")
            mobile = request_body.get("mobile", "")
            website = request_body.get("website", "")
            isAdmin = request_body.get("isAdmin", "")
            createdBy = request_body.get("createdBy", "")
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")

        try:
            id = g.con.create_user(username, password, email, mobile, website, createdBy)
        except ValueError:
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include all"
                                         " mandatory properties"
                                        )

        #CREATE RESPONSE AND RENDER
        return Response(json.dumps({"id":str(username)}), status=201,
            headers={"Location": api.url_for(User, username=username)})

class User(Resource):
    """
    User Resource.
    """

    def get(self, username):
        """
        Get basic information of a user:

        INPUT PARAMETER:
       : param str username: Username of the required user.

        OUTPUT:
         * Return 200 if the username exists.
         * Return 404 if the username is not stored in the system.

        RESPONSE ENTITY BODY:

        * Media type recommended: application/vnd.mason+json
        * Profile recommended: application/vnd.mason+json

        Link relations used:

        Semantic descriptors used: username and userID

        NOTE:
        The: py: method:`Connection.get_user()` returns a dictionary with the
        the following format.

        {'userID': user_id,
        'username': user_name,
        'password': user_password,
        'email': user_email,
        'mobile': user_mobile,
        'website': user_website,
        'isAdmin': user_isAdmin,
        'createdAt': user_createdAt,
        'updatedAt': user_updatedAt}
        """

        #PERFORM OPERATIONS
        user_db = g.con.get_user(username)
        if not user_db:
            return create_error_response(404, "Unknown user",
                                         "There is no a user with username %s"
                                         % username)
        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = FablabObject(
            username=username,
            userID= user_db["userID"],
            password= user_db["password"],
            email = user_db["email"],
            mobile = user_db["mobile"],
            website = user_db["website"],
            isAdmin = user_db["isAdmin"],
            createdAt = user_db["createdAt"],
            updatedAt = user_db["updatedAt"],
            createdBy = user_db["createdBy"],
            updatedBy = user_db["updatedBy"]
        )

        envelope.add_namespace("fablab", LINK_RELATIONS_URL)
        envelope.add_control("self", href=api.url_for(User, username=username))
        envelope.add_control("profile", href=FABLAB_USER_PROFILE)
        envelope.add_control_delete_user(username)
        envelope.add_control_edit_user(username)
        envelope.add_control_user_schema()

        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_USER_PROFILE)

    def delete(self, username):
        """
        Delete a user in the system.

       : param str username: Username of the required user.

        RESPONSE STATUS CODE:
         * If the user is deleted returns 204.
         * If the username does not exist return 404
        """

        #PEROFRM OPERATIONS
        #Try to delete the user. If it could not be deleted, the database
        #returns None.
        if g.con.delete_user(username):
            #RENDER RESPONSE
            return '', 204
        else:
            #GENERATE ERROR RESPONSE
            return create_error_response(404, "Unknown user",
                                         "There is no a user with username %s"
                                         % username)

    def put(self, username):
        """
        Modify a user.

        REQUEST ENTITY BODY:
        * Media type: JSON

        NOTE:
        The: py: method:`Connection.modify_user()` receives as a parameter a
        dictionary with the following format.
        {"username":"", "password":"", "email":"", "mobile":"",
        "website":"", "isAdmin":"", "updatedBy":""}

        """

        if not g.con.contains_user(username):
            return create_error_response(404, "Unknown user", "There is no user with username {}".format(username))

        request_body = request.get_json()
        if not request_body:
            return create_error_response(415, "Unsupported Media Type", "Use a JSON compatible format")

        try:
            password = request_body["password"]
            email = request_body.get("email", "")
            mobile = request_body.get("mobile", "")
            website = request_body.get("website", "")
            isAdmin = request_body.get("isAdmin", "")
            updatedBy = request_body.get("updatedBy", "")
        except KeyError:
            return create_error_response(400, "Wrong request format", "Be sure to include all mandatory properties")

        if not g.con.modify_user(username, password, email, mobile, website, isAdmin, updatedBy):
            return create_error_response(404, "Unknown user", "There is no user with username {}".format(username))

        return "", 204

class Machines(Resource):
    """
    Resource Machines implementation
    """

    def get(self):
        """
        Get all machines.

        INPUT parameters:
          None

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: Machine Profile
          /profiles/machine_profile

        """

        machines_db = g.con.get_machines()

        envelope = FablabObject()
        envelope.add_namespace("fablab", LINK_RELATIONS_URL)

        envelope.add_control("self", href=api.url_for(Machines))
        envelope.add_control_add_machine()
        envelope.add_control_machinetypes_all()
        envelope.add_control_machines_schema()
        envelope.add_control_endpoints(['Machines', 'MachineTypes'])

        items = envelope["items"] = []

        for machine in machines_db:
            item = FablabObject(
                machineID=machine["machineID"],
                machinename=machine["machinename"],
                typeID=machine["typeID"],
                tutorial=machine["tutorial"]
            )
            item.add_control("self", href=api.url_for(Machine, machineID=machine["machineID"]))
            item.add_control("profile", href=FABLAB_MACHINE_PROFILE)
            items.append(item)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_MACHINE_PROFILE)

    def post(self):
        """
        Adds a new machine.

        REQUEST ENTITY BODY:
         * Media type: JSON:
         * Profile: Machine Profile
          /profiles/machine_profile


        The body should be a JSON document that matches the schema for new machine
        If createdBy is not there consider it  "0" i.e Admin.

        RESPONSE STATUS CODE:
         * Returns 201 if the new machine has been added correctly.
           The Location header contains the path of the new machine
         * Returns 400 if the new machine is not well formed or the entity body is empty.
         * Returns 415 if the format of the response is not json
         * Returns 500 if the new machine could not be added to database.

         {"machinename":"", "typeID":"", "tutorial":"", "createdBy":""}

        """

        #Extract the request body. In general would be request.data
        #Since the request is JSON I use request.get_json
        #get_json returns a python dictionary after serializing the request body
        #get_json returns None if the body of the request is not formatted
        # using JSON. We use force=True since the input media type is not
        # application/json.

        if JSON != request.headers.get("Content-Type", ""):
            abort(415)
        #PARSE THE REQUEST:
        request_body = request.get_json(force=True)
        if not request_body:
            return create_error_response(415, "Unsupported Media Type",
                                         "Use a JSON compatible format",
                                         )
         #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            machinename = request_body["machinename"]
            typeID = request_body["typeID"]
            tutorial = request_body["tutorial"]
            createdBy = request_body.get("createdBy", "")

        except KeyError:
            #This is launched if machinename, typeID or tutorial does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include machinename, typeID and tutorial")
        #Create the new machine and build the response code"
        newMachine = g.con.create_machine(machinename, typeID, tutorial, createdBy)
        if not newMachine:
            return create_error_response(500, "Problem with the database",
                                         "Cannot access the database")

        #Create the Location header with the id of the new machine created
        url = api.url_for(Machines)

        #RENDER
        #Return the response
        return Response(json.dumps({"id":str(newMachine)}),status=201, headers={"Location": url})

class Machine(Resource):
    def get(self, machineID):
        """
        Get name and information of a specific Machine.

        Returns status code 404 if the machineID does not exist in the database.

        INPUT PARAMETER
       : param str typeID: The id of the Machine Type to be retrieved from the system

        RESPONSE ENTITY BODY:
         * Media type: application/vnd.mason+json:
             https://github.com/JornWildt/Mason
         * Profile: Machine Profile
          /profiles/machine_profile

        RESPONSE STATUS CODE
         * Return status code 200 if everything OK.
         * Return status code 404 if the Machine was not found in the database.

        """

        #PEFORM OPERATIONS INITIAL CHECKS
        #Get the machine from db
        machine_db = g.con.get_machine(machineID)
        if not machine_db:
            abort(404, message="There is no machine with id %s" % machineID,
                       resource_type="Machine",
                       resource_url=request.path,
                       resource_id=machineID)

        #FILTER AND GENERATE RESPONSE
        #Create the envelope:
        envelope = FablabObject(
            machineID=machine_db["machineID"],
            machinename=machine_db["machinename"],
            typeID=machine_db["typeID"],
            tutorial=machine_db["tutorial"],
            createdAt=machine_db["createdAt"],
            createdBy=machine_db["createdBy"],
            updatedAt=machine_db["updatedAt"],
            updatedBy=machine_db["updatedBy"]
        )

        envelope.add_namespace("fablab", LINK_RELATIONS_URL)
        envelope.add_namespace("atom-thread", ATOM_THREAD_PROFILE)

        envelope.add_control_edit_machine(machineID)
        envelope.add_control_delete_machine(machineID)
        envelope.add_control_machine_history(machineID)
        envelope.add_control_machines_all()
        envelope.add_control_users_all()
        envelope.add_control("profile", href=FABLAB_MACHINE_PROFILE)
        envelope.add_control("collection", href=api.url_for(Machines))
        envelope.add_control("self", href=api.url_for(Machine, machineID=machineID))
        envelope.add_control_machine_schema()

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_MACHINE_PROFILE)


    def delete(self, machineID):
        """
        Deletes a Machine from the FabLab API.

        INPUT PARAMETERS:
       : param str machineID: The id of the Machine to be deleted

        RESPONSE STATUS CODE
         * Returns 204 if the Machine was deleted
         * Returns 404 if the machineID is not associated to any machine.
        """

        #PERFORM DELETE OPERATIONS
        if g.con.delete_machine(machineID):
            return "", 204
        else:
            #Send error message
            return create_error_response(404, "Unknown id",
                                         "There is no a machine with id %s" % machineID
                                        )

    def put(self, machineID):
        """
        Modifies information of specific Machine.

        INPUT PARAMETERS:
       : param str machineID: The id of the Machine to be modified

        REQUEST ENTITY BODY:
        * Media type: JSON

         * Profile: Machine Profile
          /profiles/machine_profile

        RESPONSE ENTITY BODY:
        * Media type: Mason
          https://github.com/JornWildt/Mason
         * Profile: Machine Profile
          /profiles/machine_profile

        The body should be a JSON document that matches the schema for editing machines
        If editor is not there consider it  "0" i.e. Admin.

        OUTPUT:
         * Returns 204 if the Machine is modified correctly
         * Returns 400 if the body of the request is not well formed or it is
           empty.
         * Returns 404 if there is no Machine with machineID
         * Returns 415 if the input is not JSON.
         * Returns 500 if the database cannot be modified

        """

        #CHECK THAT MACHINE EXISTS
        if not g.con.contains_machine(machineID):
            return create_error_response(404, "Machine not found",
                                         "There is no machine with ID %s" % machineID
                                        )

        if JSON != request.headers.get("Content-Type",""):
            return create_error_response(415, "UnsupportedMediaType",
                                         "Use a JSON compatible format")
        request_body = request.get_json(force=True)
         #It throws a BadRequest exception, and hence a 400 code if the JSON is
        #not wellformed
        try:
            machinename = request_body["machinename"]
            typeID = request_body["typeID"]
            tutorial = request_body["tutorial"]
            updatedBy = request_body.get("updatedBy", "")

        except KeyError:
            #This is launched if machinename, typeID or tutorial does not exist or if
            # the template.data array does not exist.
            return create_error_response(400, "Wrong request format",
                                         "Be sure you include machinename, typeID and tutorial")
        else:
            #Modify the Machine in the database
            if not g.con.modify_machine(machineID, machinename, typeID, tutorial, updatedBy):
                return create_error_response(500, "Internal error",
                                         "Machine information for %s cannot be updated" % machinename
                                        )
            return "", 204

class History(Resource):
    def get (self, machineID):
        """
            This method returns a list of reservations for a particular machine

            INPUT:
            The query parameters are:
             * length: the number of reservations to return
             * after: the reservations returned must have been modified after
                      the time provided in this parameter.
                      Time is UNIX timestamp
             * before: the reservations returned must have been modified before the
                       time provided in this parameter. Time is UNIX timestamp
            * active: returns reservations according to active status

            RESPONSE STATUS CODE:
             * Returns 200 if the list can be generated and it is not empty
             * Returns 404 if no reservations meets the requirement

            RESPONSE ENTITY BODY:
            * Media type recommended: application/vnd.mason+json
            * Profile recommended: FABLAB_HISTORY_PROFILE
                /profiles/history-profile

            Link relations used in items: None

            Semantic descriptions used in items: headline

            Link relations used in links: messages-all, author

            Semantic descriptors used in queries: after, before, length, active
        """

        #INTIAL CHECKING
        #Extract query parameters
        parameters = request.args
        length = int(parameters.get('length', -1))
        before = int(parameters.get('before', -1))
        after = int(parameters.get('after', -1))
        active = int(parameters.get('after', -1))
        #PERFORM OPERATIONS
        #Get the messages. This method return None if there is
        #not user with nickname = nickname
        # results_db = g.con.get_reservation_list(machineID, length, before, after, active)
        results_db = g.con.get_reservation_list(None, machineID, before, after)
        if results_db is None or not results_db:
            return create_error_response(404, "Empty list",
                                         "Cannot find any reservations with the"
                                         " provided restrictions")
        envelope = FablabObject()

        envelope.add_namespace("fablab", LINK_RELATIONS_URL)
        envelope.add_control("self", href=api.url_for(History, machineID=machineID))
        envelope.add_control_add_reservation()
        envelope.add_control_machines_all()
        envelope.add_control_users_all()
        envelope.add_control_history_schema()

        items = envelope["items"] = []

        for result in results_db:
            item = FablabObject(
                reservationID=result['reservationID'],
                userID=result["userID"],
                machineID=result["machineID"],
                startTime=result["startTime"],
                endTime=result["endTime"],
                isActive=result["isActive"]
            )
            item.add_control("self", href=api.url_for(Reservation, reservationID=result["reservationID"]))
            item.add_control("profile", href=FABLAB_RESERVATION_PROFILE)
            items.append(item)

        #RENDER
        return Response(json.dumps(envelope), 200, mimetype=MASON+";" + FABLAB_HISTORY_PROFILE)
        #return None

#Add the Regex Converter so we can use regex expressions when we define the
#routes
app.url_map.converters["regex"] = RegexConverter

#Define the routes

api.add_resource(MachineTypes, "/fablab/api/machinetypes/",
                 endpoint="machinetypes")
api.add_resource(MachineType, "/fablab/api/machinetypes/<typeID>/",
                 endpoint="machinetype")
api.add_resource(Reservations, "/fablab/api/reservations/",
                 endpoint="reservations")
api.add_resource(Reservation, "/fablab/api/reservations/<reservationID>/",
                 endpoint="reservation")
api.add_resource(Users, "/fablab/api/users/",
                 endpoint="users")
api.add_resource(User, "/fablab/api/users/<username>/",
                 endpoint="user")
api.add_resource(Machines, "/fablab/api/machines/",
                 endpoint="machines")
api.add_resource(Machine, "/fablab/api/machines/<machineID>/",
                 endpoint="machine")
api.add_resource(History, "/fablab/api/machines/<machineID>/history/",
                 endpoint="history")

#Redirect profile
@app.route("/profiles/<profile_name>/")
def redirect_to_profile(profile_name):
    return redirect(APIARY_PROFILES_URL + profile_name)

@app.route("/fablab/link-relations/")
def redirect_to_rels():
    return redirect(APIARY_RELS_URL )

#Send our schema file(s)
@app.route("/fablab/schema/<schema_name>/")
def send_json_schema(schema_name):
    #return send_from_directory("static/schema", "{}.json".format(schema_name))
    return send_from_directory(app.static_folder, "schema/{}.json".format(schema_name))


#Start the application
#DATABASE SHOULD HAVE BEEN POPULATED PREVIOUSLY
if __name__ == '__main__':
    #Debug true activates automatic code reloading and improved error messages
    app.run(debug=True)
