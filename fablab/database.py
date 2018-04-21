'''
Created on 22.02.2018

Provides the database API to access the FabLab database.

@author: PWP20_2018
We reuse the code of Ivan and Mika in Programmable Web Project exercise _ University of Oulu



------------------------------------------------------IMPORTANT: SEARCH #PWP20_2018 FOR REQUIRED MODIFICATION PART----------------------------------------------------
'''

from datetime import datetime
import time, sqlite3, re, os
#Default paths for .db and .sql files to create and populate the database.
DEFAULT_DB_PATH = 'db/fablab.db'
DEFAULT_SCHEMA = "db/fablab_schema_dump.sql"
DEFAULT_DATA_DUMP = "db/fablab_data_dump.sql"


class Engine(object):
    '''
    Abstraction of the database.

    It includes tools to create, configure,
    populate and connect to the sqlite file. You can access the Connection
    instance, and hence, to the database interface itself using the method
    :py:meth:`connection`.

    :Example:

    >>> engine = Engine()
    >>> con = engine.connect()

    :param db_path: The path of the database file (always with respect to the
        calling script. If not specified, the Engine will use the file located
        at *db/fablab.db*. We will create the database from .sql file.

    '''
    def __init__(self, db_path=None):
        '''
        '''

        super(Engine, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH

    def connect(self):
        '''
        Creates a connection to the database.

        :return: A Connection instance
        :rtype: Connection

        '''
        return Connection(self.db_path)

    def remove_database(self):
        '''
        Removes the database file from the filesystem.

        '''
        if os.path.exists(self.db_path):
            #THIS REMOVES THE DATABASE STRUCTURE
            os.remove(self.db_path)

    def clear(self):
        '''
        Purge the database removing all records from the tables. However,
        it keeps the database schema (meaning the table structure)

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        #THIS KEEPS THE SCHEMA AND REMOVE VALUES
        con = sqlite3.connect(self.db_path)
        #Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM users")
            cur.execute("DELETE FROM machinetypes")
            cur.execute("DELETE FROM messages")
            #NOTE since we have ON DELETE CASCADE BOTH IN messages AND reservations AND
            #machines, WE DO NOT HAVE TO WORRY TO CLEAR THOSE TABLES.

    #METHODS TO CREATE AND POPULATE A DATABASE USING DIFFERENT SCRIPTS
    def create_tables(self, schema=None):
        '''
        Create programmatically the tables from a schema file.

        :param schema: path to the .sql schema file. If this parmeter is
            None, then *db/fablab_schema_dump.sql* is utilized.

        '''
        con = sqlite3.connect(self.db_path)
        if schema is None:
            schema = DEFAULT_SCHEMA
        try:
            with open(schema, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()

    def populate_tables(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.

        :param dump:  path to the .sql dump file. If this parmeter is
            None, then *db/forum_data_dump.sql* is utilized.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        con = sqlite3.connect(self.db_path)
        #Activate foreing keys support
        cur = con.cursor()
        cur.execute(keys_on)
        #Populate database from dump
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        try:
            with open (dump, encoding="utf-8") as f:
                sql = f.read()
                cur = con.cursor()
                cur.executescript(sql)
        finally:
            con.close()




class Connection(object):
    '''
    API to access the Forum database.

    The sqlite3 connection instance is accessible to all the methods of this
    class through the :py:attr:`self.con` attribute.

    An instance of this class should not be instantiated directly using the
    constructor. Instead use the :py:meth:`Engine.connect`.

    Use the method :py:meth:`close` in order to close a connection.
    A :py:class:`Connection` **MUST** always be closed once when it is not going to be
    utilized anymore in order to release internal locks.

    :param db_path: Location of the database file.
    :type dbpath: str
     def isclosed(self):

        #return: ``True`` if connection has already being closed.

        return self._isclosed
    '''
    def __init__(self, db_path):
        super(Connection, self).__init__()
        self.con = sqlite3.connect(db_path)
        self._isclosed = False



    def close(self):
        '''
        Closes the database connection, commiting all changes.

        '''
        if self.con and not self._isclosed:
            self.con.commit()
            self.con.close()
            self._isclosed = True 

    #FOREIGN KEY STATUS
    def check_foreign_keys_status(self):
        '''
        Check if the foreign keys has been activated.

        :return: ``True`` if  foreign_keys is activated and ``False`` otherwise.
        :raises sqlite3.Error: when a sqlite3 error happen. In this case the
            connection is closed.

        '''
        try:
            #Create a cursor to receive the database values
            cur = self.con.cursor()
            #Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            #We know we retrieve just one record: use fetchone()
            data = cur.fetchone()
            is_activated = data == (1,)
            print("Foreign Keys status: %s" % 'ON' if is_activated else 'OFF')
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            self.close()
            raise excp
        return is_activated

    def set_foreign_keys_support(self):
        '''
        Activate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        try:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            #execute the pragma command, ON
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    def unset_foreign_keys_support(self):
        '''
        Deactivate the support for foreign keys.

        :return: ``True`` if operation succeed and ``False`` otherwise.

        '''
        keys_on = 'PRAGMA foreign_keys = OFF'
        try:
            #Get the cursor object.
            #It allows to execute SQL code and traverse the result set
            cur = self.con.cursor()
            #execute the pragma command, OFF
            cur.execute(keys_on)
            return True
        except sqlite3.Error as excp:
            print("Error %s:" % excp.args[0])
            return False

    #HELPERS
    #Here the helpers that transform database rows into dictionary. They work
    #similarly to ORM

    #Helpers for machine
    def _create_machine_object(self, row):
        '''
        It takes a :py:class:`sqlite3.Row` and transform it into a dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary containing the following keys:

            * ``machineID``: id of the machine (int)
            * ``machinename``: machine's name
            * ``typeID``: type of the machine (int & FK - machinetypes table)
            * ``tutorial``: link to a HTML file that has tutorial for this machine (text)
            * ``createdAt, updatedAt``: UNIX timestamp (long integer) that specifies when
              the machine was created or updated.
            * ``createdBy & updatedBy``: The userID owner or modifier.

            Note that all values in the returned dictionary are string unless
            otherwise stated.

            Structure of an object:
                    machine = {'machineID': message_id, 'machinename': machine_name,
                   'typeID': machine_type_id, 'tutorial': machine_tutorial,
                   'createdAt': machine_created_at, 'updatedAt': machine_updated_at,
                   'createdBy': machine_created_by, 'updateBy': machine_updated_by}

        '''
        machine_id = 'machine-' + str(row['machineID'])
        machine_name = row['machinename']
        machine_type_id = row['typeID']
        machine_tutorial = row['tutorial']
        machine_created_at = row['createdAt']
        machine_updated_at = row['updatedAt']
        machine_created_by = row['createdBy']
        machine_updated_by = row['updatedBy']
        machine = {'machineID': machine_id, 'machinename': machine_name,
                   'typeID': machine_type_id, 'tutorial': machine_tutorial,
                   'createdAt': machine_created_at, 'updatedAt': machine_updated_at,
                   'createdBy': machine_created_by, 'updatedBy': machine_updated_by}
        return machine

    def _create_machine_list_object(self, row):
        '''
        Same as :py:meth:`_create_machine_object`. However, the resulting
        dictionary is targeted to build machines in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys `machine-`machineID``, ``machinename``,
            ``typeID`` and ``tutorial``.
        Structure of an object:
                machine = {'machineID': machine_id, 'machinename': machine_name,
                'typeID': machine_type_id, 'tutorial': machine_tutorial}
        '''
        machine_id = 'machine-' + str(row['machineID'])
        machine_name = row['machinename']
        machine_type_id = row['typeID']
        machine_tutorial = row['tutorial']
        machine = {'machineID': machine_id, 'machinename': machine_name,
                   'typeID': machine_type_id, 'tutorial': machine_tutorial}
        return machine

    #Helpers for users
    def _create_user_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

               {'userID': user_id,
               'username': user_name,
               'password': user_password,
               'email': user_email,
               'mobile': user_mobile,
               'website': user_website,
               'isAdmin': user_isAdmin,
               'createdAt': user_createdAt,
               'updatedAt': user_updatedAt}


            where:

            * ``userID``: unique ID
            * ``username``: nickname of the user
            * ``password``: password
            * ``email``: current email of the user.
            * ``mobile``: string showing the user's phone number. Can be None.
            * ``website``: url with the user's personal page. Can be None
            * ``isAdmin``: role of user
            * ``createdAt``: UNIX timestamp
            * ``updatedAt``: UNIX timestamp
            Note that all values are string if they are not otherwise indicated.

        '''
        user_id = row['userID']
        user_name = row['username']
        user_password = row['password']
        user_email = row['email']
        user_mobile = row['mobile']
        user_website = row['website']
        user_isAdmin = str(row['isAdmin'])
        user_createdAt = row['createdAt']
        user_updatedAt = row['updatedAt']
        return {'userID': user_id,
               'username': user_name,
               'password': user_password,
               'email': user_email,
               'mobile': user_mobile,
               'website': user_website,
               'isAdmin': user_isAdmin,
               'createdAt': user_createdAt,
               'updatedAt': user_updatedAt}

    def _create_user_list_object(self, row):
        '''
        Same as :py:meth:`_create_machine_list_object`. However, the resulting
        dictionary is targeted to build users in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys ``userID`` and
            ``username``

        '''
        return {'userID': row['userID'], 'username': row['username']}

    #Helpers for type
    def _create_type_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

               {'typeID': row['typeID'],
               'typeName': row['typeName'],
               'pastProject': row['pastProject'],
               'createdAt': row['createdAt'],
               'updatedAt': row['updatedAt'],
               'createdBy': row['createdBy'],
               'updatedBy': row['updatedBy']}


            where:

            * ``typeID``: unique ID
            * ``typeName``: name of the type
            * ``pastProject``: text contains location of HTML that contains previous projects using this type
            * ``createdAt & updatedAt``: UNIX timestamp
            * ``createdBy & updatedBy``: userID
            Note that all values are string if they are not otherwise indicated.

        '''

        return {'typeID': row['typeID'],
               'typeName': row['typeName'],
               'typeFullname': row['typeFullname'],
               'pastProject': row['pastProject'],
               'createdAt': row['createdAt'],
               'updatedAt': row['updatedAt'],
               'createdBy': row['createdBy'],
               'updatedBy': row['updatedBy']}

    def _create_type_list_object(self, row):
        '''
        Same as :py:meth:`_create_machine_list_object`. However, the resulting
        dictionary is targeted to build users in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys ``typeID`` and
            ``typeName``

        '''
        return {'typeID': row['typeID'], 'typeName': row['typeName'], 'typeFullname': row['typeFullname']}

    #Helpers for message
    def _create_message_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

               {'messageID': 'msg-' + str(row['messageID']),
               'fromUserID': row['fromUserID'],
               'toUserID': row['toUserID'],
               'content': row['content'],
               'createdAt': row['createdAt']}


            where:

            * ``messageID``: id of the message
            * ``fromUserID & toUserID``: sender and receiver
            * ``content``: message's content
            * ``createdAt``: UNIX timestamp
            Note that all values are string if they are not otherwise indicated.

        '''

        return {'messageID': 'msg-' + str(row['messageID']),
               'fromUserID': row['fromUserID'],
               'toUserID': row['toUserID'],
               'content': row['content'],
               'createdAt': row['createdAt']}

    def _create_message_list_object(self, row):
        '''
        Same as :py:meth:`_create_machine_list_object`. However, the resulting
        dictionary is targeted to build users in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys ``messageID`` and
            ``createdAt``

        '''
        return {'messageID': 'msg-' + str(row['messageID']), 'createdAt': row['createdAt']}

    #Helpers for reservation
    def _create_reservation_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the following format:

            .. code-block:: javascript

               {'reservationID': row['reservationID'],
               'userID': row['userID'],
               'machineID': 'machine-' + str(row['machineID']),
               'startTime': row['startTime'],
               'endTime': row['endTime'],
               'isActive': row['isActive'],
               'createdAt': row['createdAt'],
               'createdBy': row['createdBy'],
               'updatedAt': row['updatedAt'],
               'updatedBy': row['updatedBy']}


            where:

            * ``reservationID``: id of the reservation
            * ``userID``: user who reserved the machin
            * ``machineID``: machine that is reserved
            * ``startTime & endTime``: UNIX timestamp
            * ``createdAt``: machine that is reserved
            * ``isActive``: status of reservation
            * ``createdAt & updatedAt``: UNIX timestamp
            * ``createdBy & updatedBy``: userID

            Note that all values are string if they are not otherwise indicated.

        '''

        return {'reservationID': row['reservationID'],
               'userID': row['userID'],
               'machineID': 'machine-' + str(row['machineID']),
               'startTime': row['startTime'],
               'endTime': row['endTime'],
               'isActive': row['isActive'],
               'createdAt': row['createdAt'],
               'createdBy': row['createdBy'],
               'updatedAt': row['updatedAt'],
               'updatedBy': row['updatedBy']}

    def _create_reservation_list_object(self, row):
        '''
        Same as :py:meth:`_create_machine_list_object`. However, the resulting
        dictionary is targeted to build users in a list.

        :param row: The row obtained from the database.
        :type row: sqlite3.Row
        :return: a dictionary with the keys ``messageID`` and
            ``createdAt``

        '''
        return {'reservationID': row['reservationID'], 'userID': row['userID'],
               'machineID': 'machine-' + str(row['machineID']),
               'startTime': row['startTime'],
               'endTime': row['endTime'],
               'isActive': row['isActive']}

    #API ITSELF
    #Message Table API.
    def get_message(self, messageid):
        '''
        Extracts a message from the database.

        :param messageid: The id of the message. Note that messageid is a
            string with format ``msg-\d{1,3}``.
        :return: A dictionary with the format provided in
            :py:meth:`_create_message_object` or None if the message with target
            id does not exist.
        :raises ValueError: when ``messageid`` is not well formed

        '''
        #Extracts the int which is the id for a message in the database
        match = re.match(r'msg-(\d{1,3})', messageid)
        if match is None:
            raise ValueError("The messageid is malformed")
        messageid = int(match.group(1))
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM messages WHERE messageID = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (messageid,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_message_object(row)

    def get_messages(self, fromUserID=None, number_of_messages=-1,
                     before=-1, after=-1):
        '''
        Return a list of all the messages in the database filtered by the
        conditions provided in the parameters.

        :param fromUserID: default None. Search messages of a user with the given
            fromUserID. If this parameter is None, it returns the messages of
            any user in the system.
        :type fromUserID: int
        :param number_of_messages: default -1. Sets the maximum number of
            messages returning in the list. If set to -1, there is no limit.
        :type number_of_messages: int
        :param before: All timestamps > ``before`` (UNIX timestamp) are removed.
            If set to -1, this condition is not applied.
        :type before: long
        :param after: All timestamps < ``after`` (UNIX timestamp) are removed.
            If set to -1, this condition is not applied.
        :type after: long

        :return: A list of messages. Each message is a dictionary containing
            the following keys:

            * ``messageid``: string with the format msg-\d{1,3}.Id of the
                message.
            * ``fromUserID` & `toUserID``: userID of the message's sender and receiver.
            * ``content``: string containing the title of the message.
            * ``timestamp``: UNIX timestamp (long int) that specifies when the
                message was created.

            Note that all values in the returned dictionary are string unless
            otherwise stated.

        :raises ValueError: if ``before`` or ``after`` are not valid UNIX
            timestamps

        '''
        #Create the SQL Statement build the string depending on the existence
        #of fromUserID, numbero_of_messages, before and after arguments.
        query = 'SELECT * FROM messages'
          #fromUserID restriction
        if fromUserID is not None or before != -1 or after != -1:
            query += ' WHERE'
        if fromUserID is not None:
            query += " fromUserID = '%d'" % fromUserID
          #Before restriction
        if before != -1:
            if fromUserID is not None:
                query += ' AND'
            query += " createdAt < %s" % str(before)
          #After restriction
        if after != -1:
            if nickname is not None or before != -1:
                query += ' AND'
            query += " createdAt > %s" % str(after)
          #Order of results
        query += ' ORDER BY createdAt DESC'
          #Limit the number of resulst return
        if number_of_messages > -1:
            query += ' LIMIT ' + str(number_of_messages)
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        messages = []
        for row in rows:
            message = self._create_message_list_object(row)
            messages.append(message)
        return messages

    def delete_message(self, messageid):
        '''
        Delete the message with id given as parameter.

        :param str messageid: id of the message to remove.Note that messageid
            is a string with format ``msg-\d{1,3}``
        :return: True if the message has been deleted, False otherwise
        :raises ValueError: if the messageId has a wrong format.

        '''
        #Extracts the int which is the id for a message in the database
        match = re.match(r'msg-(\d{1,3})', messageid)
        if match is None:
            raise ValueError("The messageid is malformed")
        messageid = int(match.group(1))
        #Create the SQL statment
        stmnt = 'DELETE FROM messages WHERE messageID = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (messageid,)
        try:
            cur.execute(stmnt, pvalue)
            #Commit the message
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def create_message(self, content, fromUserID,
                       toUserID):
        '''
        Create a new message with the data provided as arguments.

        :param str content: the message's content
        :param int fromUserID: the userID of the person who create this message
        :param int toUserID: the userID of the person who receive this message
        :return: the id of the created message or None if the message was not
            found. Note that the returned value is a string with the format msg-\d{1,3}.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Extracts the int which is the id for a message in the database

        #Create the SQL statement for inserting the data
        stmnt = 'INSERT INTO messages (fromUserID,toUserID,content, \
                 createdAt) \
                 VALUES(?,?,?,?)'
          #Variables for the statement.
          #user_id is obtained from first statement.
        timestamp = time.mktime(datetime.now().timetuple())
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (fromUserID, toUserID, content, timestamp)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        lid = cur.lastrowid
        #Return the id in
        return 'msg-' + str(lid) if lid is not None else None

    #MACHINE API
    def get_machine(self, machineID):
        '''
        Extracts a machine from the database.

        :param machineID: The id of the machine. Note that machineid is a
            string with format ``machine-\d{1,3}``.
        :return: A dictionary with the format provided in
            :py:meth:`_create_machine_object` or None if the machine with target
            id does not exist.
        :raises ValueError: when ``machineID`` is not well formed

        '''
        #Extracts the int which is the id for a machine in the database
        match = re.match(r'machine-(\d{1,3})', machineID)
        if match is None:
            raise ValueError("The machineID is malformed")
        machineID = int(match.group(1))
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM machines WHERE machineID = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (machineID,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_machine_object(row)

    def contains_machine(self, machineID):
        '''
        Checks if a machine is in the database.

        :param str machineID: Id of the machine to search. Note that machineID
            is a string with the format machine-\d{1,3}.
        :return: True if the machine is in the database. False otherwise.

        '''
        return self.get_machine(machineID) is not None

    def contains_type(self, typeID):
        '''
        Checks if a machine is in the database.

        :param str machineID: Id of the machine to search. Note that machineID
            is a string with the format machine-\d{1,3}.
        :return: True if the machine is in the database. False otherwise.

        '''
        return self.get_type(typeID) is not None

    def get_machines(self, typeName=None):
        '''
        Return a list of all the machines in the database filtered by the
        conditions provided in the parameters.

        :param typeID: default None. Search machines with type TypeID

        :return: A list of machines. Each machines is a dictionary containing
            the following keys:

            * ``machineID``: string with the format machine-\d{1,3}.Id of the
                machine.
            * ``machinename``: name of the machine.
            * ``typeID``: type of the machine.
            * ``tutorial``: a HTML link store the tutorial how to use the machine
            * ``createdAt & updatedAt``: UNIX timestamp (long int) that specifies when the
                machine was created or updated.
            * ``createdBy & updatedBy``: UserID


            Note that all values in the returned dictionary are string unless
            otherwise stated.

        :raises ValueError: if ``typeName`` are not found

        '''
        #Create the SQL Statement build the string depending on the existence
        #of fromUserID, numbero_of_messages, before and after arguments.
        #SQL Statement to query machinetypes
        query = 'SELECT typeID FROM machinetypes'
        #SQL Statement to query machines
        stmnt = 'SELECT * FROM machines'
        if typeName is not None:
            query += " WHERE typeName = '%s' " % typeName
            self.con.row_factory = sqlite3.Row
            cur = self.con.cursor()
            cur.execute(query)
            row = cur.fetchone()
            if row is None:
                return None
            typeID = row["typeID"]
            if typeID is not None:
                stmnt += " WHERE typeID = " +  str(typeID)
            #Activate foreign key support
            self.set_foreign_keys_support()
            #Cursor and row initialization
            self.con.row_factory = sqlite3.Row
            cur = self.con.cursor()
            cur.execute(stmnt)
            rows = cur.fetchall()
            if rows is None:
                return None
            machines = []
            for machine in rows:
                machine = self._create_machine_list_object(machine)
                machines.append(machine)
                #Limit the number of resulst return
            return machines


        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(stmnt)
        rows = cur.fetchall()
        if rows is None:
            return None
        machines = []
        for machine in rows:
            machine = self._create_machine_list_object(machine)
            machines.append(machine)
            #Limit the number of resulst return

        return machines

    def delete_machine(self, machineID):
        '''
        Delete the machine with id given as parameter.

        :param str machineID: id of the message to remove.Note that messageid
            is a string with format ``machine-\d{1,3}``
        :return: True if the machine has been deleted, False otherwise
        :raises ValueError: if the machineID has a wrong format.

        '''
        #Extracts the int which is the id for a message in the database
        match = re.match(r'machine-(\d{1,3})', machineID)
        if match is None:
            raise ValueError("The machineID is malformed")
        machineID = int(match.group(1))

        #Create the SQL statment
        stmnt = 'DELETE FROM machines WHERE machineID = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (machineID,)
        try:
            cur.execute(stmnt, pvalue)
            #Commit the message
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def modify_machine(self, machineID, machinename, typeID, tutorial, updatedBy = '0'):
        '''
        Modify the name, the type and the tutorial of the machine with id
        ``machineID``

        :param str machinename: name of the machine
        :param int typeID: machine's type ID
        :param str tutorial: the tutorial HTML link
        :param str updatedBy: ID of the user who updated this machine. Default value is 0 - SQLAdmin
        :return: the id of the edited machine or None if the machine was
              not found. The id of the machine has the format ``machine-\d{1,3}``,
              where \d{1,3} is the id of the machine in the database.
        :raises ValueError: if the machineID has a wrong format.

        '''
        #Extracts the int which is the id for a machine in the database
        match = re.match(r'machine-(\d{1,3})', machineID)
        if match is None:
            raise ValueError("The machineID is malformed")
        machineID = int(match.group(1))

        #Create the SQL statment
        stmnt = 'UPDATE machines SET machinename=:machinename , typeID=:typeID, tutorial=:tutorial, updatedBy=:updatedBy,\
                  updatedAt=:updatedAt WHERE machineID =:machineID'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        timestamp = time.mktime(datetime.now().timetuple())

        pvalue = {"machineID": machineID,
                  "machinename": machinename,
                  "typeID": typeID,
                  "tutorial": tutorial,
                  "updatedAt":timestamp,
                  "updatedBy":updatedBy}
        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        else:
            if cur.rowcount < 1:
                return None
        return 'machine-%s' % machineID

    def create_machine(self, machinename, typeID, tutorial, createdBy='0'):
        '''
        Create a new machine with the data provided as arguments.

        :param str machinename: the machine's content
        :param int typeID: the type of the machine
        :param string tutorial: HTML link for tutorial
        :param int createdBy: the userID of the person who receive this message. Default value is 0, SQLAdmin
        :return: the id of the created machine or None if the machine was not
            found. Note that the returned value is a string with the format msg-\d{1,3}.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Extracts the int which is the id for a message in the database


        #Create the SQL statement for inserting the data
        stmnt = 'INSERT INTO machines (machinename, typeID, tutorial, \
                 createdBy, createdAt) \
                 VALUES(?,?,?,?,?)'
          #Variables for the statement.
          #user_id is obtained from first statement.
        timestamp = time.mktime(datetime.now().timetuple())
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (machinename, typeID, tutorial, createdBy,timestamp)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        lid = cur.lastrowid
        #Return the id in
        return 'machine-' + str(lid) if lid is not None else None



    #TYPE API
    def get_type(self, typeID):
        '''
        Extracts a machine type from the database.

        :param typeName: name of the Type
        :return: A dictionary with the format provided in
            :py:meth:`_create_message_object` or None if the message with target
            id does not exist.
        :raises ValueError: when ``machineID`` is not well formed

        '''
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM machinetypes WHERE typeID = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (typeID,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_type_object(row)

    def get_types(self):
        '''
        Return a list of all the types in the database filtered by the
        conditions provided in the parameters.


        :return: A list of types.
            * ``typeID``: typeID of the machine
            * ``typeName``: name of the type.

            Note that all values in the returned dictionary are string unless
            otherwise stated.


        '''
        #Create the SQL Statement build the string depending on the existence
        #of fromUserID, numbero_of_messages, before and after arguments.
        #SQL Statement to query machinetypes
        query = 'SELECT * FROM machinetypes'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if rows is None:
            return None
        types = []
        for type in rows:
            type = self._create_type_list_object(type)
            types.append(type)
            #Limit the number of resulst return

        return types

    def delete_type(self, typeID):
        '''
        Delete the typeID with id given as parameter.

        :param str machineID: id of the message to remove.Note that messageid
            is a string with format ``machine-\d{1,3}``
        :return: True if the machine has been deleted, False otherwise
        :raises ValueError: if the machineID has a wrong format.

        '''
        #Create the SQL statment
        stmnt = 'DELETE FROM machinetypes WHERE typeID = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (typeID,)
        try:
            cur.execute(stmnt, pvalue)
            #Commit the message
            self.con.commit()
        except sqlite3.Error as e:
            print("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def modify_type(self, typeID, typeName, typeFullname, pastProject, updatedBy= '0'):
        '''
        Modify the name, the past project of the type with id
        ``typeID``

        :param str typeName: short name of the type
        :param str typeFullname: full name of the type
        :param int typeID: machine's type ID
        :param str pastProject: the previous projects HTML link
        :return: the id of the edited type or None if the type was
              not found.
        :raises ValueError: if the machineID has a wrong format.

        '''
        #Extracts the int which is the id for a machine in the database
        #Create the SQL statment
        stmnt = 'UPDATE machinetypes SET typeName=:typeName , typeFullname=:typeFullname, pastProject=:pastProject, updatedAt=:timestamp, updatedBy=:updatedBy \
                 WHERE typeID =:typeID'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        timestamp = time.mktime(datetime.now().timetuple())

        #Execute main SQL Statement
        pvalue = {"typeID": typeID,
                  "typeName": typeName,
                  "typeFullname": typeFullname,
                  "pastProject": pastProject,
                  "timestamp":timestamp,
                  "updatedBy":updatedBy}
        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        else:
            if cur.rowcount < 1:
                return None
        return typeID

    def create_type(self, typeName, typeFullname, pastProject, createdBy='0'):
        '''
        Create a new machine type with the data provided as arguments.

        :param str typeName: short name of the type
        :param str typeFullname: full name of the type
        :param int typeID: the type of the machine
        :param string pastProject: HTML link for past projects
        :param int createdBy: the userID of the person who receive this message. Default value is 0, SQLAdmin
        :return: the id of the created machine type or None if the machine was not
            found.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Extracts the int which is the id for a message in the database


        #Create the SQL statement for inserting the data
        stmnt = 'INSERT INTO machinetypes (typeName, typeFullname, pastProject, createdAt, \
                 createdBy) \
                 VALUES(?,?,?,?,?)'
          #Variables for the statement.
          #user_id is obtained from first statement.
        timestamp = time.mktime(datetime.now().timetuple())
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (typeName, typeFullname, pastProject, timestamp, createdBy)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        lid = cur.lastrowid
        #Return the id in
        return str(lid) if lid is not None else None

    # RESERVATION API
    def get_reservation_list(self, userID = None, machineID = None, startTime=-1, endTime=-1):
        #Create the SQL Statement build the string depending on the existence
        #of userID, machineID, startTime and endTime arguments.

        if machineID is not None:
            match = re.match(r'machine-(\d{1,3})', machineID)
            if match is None:
                raise ValueError("The machineID is malformed")
            machineID = int(match.group(1))

        query = 'SELECT * FROM reservations'
          #userID restriction
        if userID is not None or machineID is not None or startTime != -1 or endTime != -1:
            query += ' WHERE'
        if userID is not None:
            query += " userID = " + str(userID)
        if machineID is not None:
            if userID is not None:
                query += ' AND '
            query += " machineID = " + str(machineID)

        #startTime restriction
        if startTime != -1:
            if userID is not None or machineID is not None:
                query += ' AND'
            query += " startTime > %s" % str(startTime)
          #endTime restriction
        if endTime != -1:
            if userID is not None or machineID is not None or startTime != -1:
                query += ' AND'
            query += " endTime < %s" % str(endTime)
          #Order of results
        query += ' ORDER BY startTime DESC'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        reservations = []
        for row in rows:
            reservation = self._create_reservation_list_object(row)
            reservations.append(reservation)
        return reservations

    def get_active_reservation_list(self, active = 1, userID = None, machineID = None, startTime=-1, endTime=-1):
        #Create the SQL Statement build the string depending on the existence
        #of userID, machineID, startTime and endTime arguments.
        if machineID is not None:
            match = re.match(r'machine-(\d{1,3})', machineID)
            if match is None:
                raise ValueError("The machineID is malformed")
            machineID = int(match.group(1))

        query = 'SELECT * FROM reservations'

        if active == 1:
            query += ' WHERE isActive = 1'
        else:
            query += ' WHERE isActive = 0'

        #userID restriction
        if userID is not None or machineID is not None or startTime != -1 or endTime != -1:
            query += ' AND'
        if userID is not None:
            query += " userID = " + str(userID)
        if machineID is not None:
            if userID is not None:
                query += ' AND'
            query += " machineID = " + str(machineID)

        #startTime restriction
        if startTime != -1:
            if userID is not None or machineID is not None:
                query += ' AND'
            query += " startTime > %s" % str(startTime)
          #endTime restriction
        if endTime != -1:
            if nickname is not None or machineID is not None or startTime != -1:
                query += ' AND'
            query += " endTime < %s" % str(endTime)
          #Order of results
        query += ' ORDER BY startTime DESC'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Get results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Build the return object
        reservations = []
        for row in rows:
            reservation = self._create_reservation_list_object(row)
            reservations.append(reservation)
        return reservations

    def get_reservation (self, reservationID):
        '''
        Extracts a specific reservation from the database.

        :param reservationID: ID of reservation
        :return: A dictionary with the format provided in
            :py:meth:`_create_reservation_object` or None if the reservation with target
            id does not exist.
        '''

        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the SQL Query
        query = 'SELECT * FROM reservations WHERE reservationID = ?'
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = (reservationID,)
        cur.execute(query, pvalue)
        #Process the response.
        #Just one row is expected
        row = cur.fetchone()
        if row is None:
            return None
        #Build the return object
        return self._create_reservation_object(row)

    def modify_reservation (self, reservationID, startTime, endTime, updatedBy = '0'):
        '''
        Modify the startTime and endTime of the reservation

        :param int reservationID: ID of the reservation
        :param int startTime & endTime: UNIX time stamp
        :param int updatedBy: userID of user
        :return: the id of the edited reservation or None if the type was
              not found.

        '''
        if isinstance(reservationID, int) == False:
            raise ValueError("The reservationID is malformed")

        #Extracts the int which is the id for a machine in the database
        #Create the SQL statment
        stmnt = 'UPDATE reservations SET startTime=:startTime , endTime=:endTime  \
                 WHERE reservationID =:reservationID'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        pvalue = {"startTime": startTime,
                  "endTime": endTime,
                  "reservationID": reservationID}
        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        else:
            if cur.rowcount < 1:
                return None
        return reservationID

    def contains_reservation(self, reservationID):
        '''
        Checks if a reservation is in the database.

        :param str reservationID: Id of the reservation to search. Note that reservationID is an integer.
        :return: True if the reservation is in the database. False otherwise.
        '''
        return self.get_reservation(reservationID) is not None

    def disable_reservation (self, reservationID, updatedBy = '0'):
        '''
        Modify the reservation's isActive state

        :param int reservationID: ID of the reservation
        :param int updatedBy: userID of user
        :return: the id of the edited reservation or None if the type was
              not found.

        '''
        #Extracts the int which is the id for a machine in the database
        #Create the SQL statment
        stmnt = 'UPDATE reservations SET isActive = 0 , updatedBy =:updatedBy , updatedAt =:updatedAt \
                 WHERE reservationID =:reservationID'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        timestamp = time.mktime(datetime.now().timetuple())

        pvalue = {"updatedBy": updatedBy,
                  "reservationID": reservationID,
				  "updatedAt": timestamp}
        try:
            cur.execute(stmnt, pvalue)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        else:
            if cur.rowcount < 1:
                return None
        return reservationID

    def delete_oldest_reservations (self, limit = 500):
        stmnt = 'DELETE FROM reservations WHERE reservationID IN (SELECT reservationID FROM reservations ORDER BY reservationID ASC LIMIT '
        stmnt += str(limit) + ')'
        cur = self.con.cursor()
        try:
            cur.execute(stmnt)
            self.con.commit()
        except sqlite3.Error as e:
            print ("Error %s:" % (e.args[0]))
        return bool(cur.rowcount)

    def create_reservation(self, userID, machineID, startTime=None, endTime=None, createdBy = '0'):
        '''
        Create a new reservation with the data provided as arguments.

        :param str typeName: the machine's content
        :param int typeID: the type of the machine
        :param string pastProject: HTML link for past projects
        :param int createdBy: the userID of the person who receive this message. Default value is 0, SQLAdmin
        :return: the id of the created machine type or None if the machine was not
            found.

        :raises ForumDatabaseError: if the database could not be modified.

        '''
        #Extracts the int which is the id for a message in the database


        #Create the SQL statement for inserting the data
        stmnt = 'INSERT INTO reservations (userID, machineID, startTime, \
                 endTime, createdBy, createdAt) \
                 VALUES(?,?,?,?,?,?)'
          #Variables for the statement.
          #user_id is obtained from first statement.
        timestamp = time.mktime(datetime.now().timetuple())
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        pvalue = (userID, machineID, startTime, endTime,createdBy,timestamp)
        #Execute the statement
        cur.execute(stmnt, pvalue)
        self.con.commit()
        #Extract the id of the added message
        lid = cur.lastrowid
        #Return the id in
        return str(lid) if lid is not None else None


    #ACCESSING THE USERS tables
    def get_users(self):
        '''
        Extracts all users in the database.

        :return: list of Users of the database. Each user is a dictionary
            that contains two keys: ``userName``(str) and ``userID``
            (int). None is returned if the database
            has no users.

        '''
        #Create the SQL Statements
          #SQL Statement for retrieving the users
        query = 'SELECT * FROM users'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Create the cursor
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute main SQL Statement
        cur.execute(query)
        #Process the results
        rows = cur.fetchall()
        if rows is None:
            return None
        #Process the response.
        users = []
        for row in rows:
            users.append(self._create_user_list_object(row))
        return users

    def get_user(self, username):
        '''
        Extracts all the information of a user.

        :param str username: The username of the user to search for.
        :return: dictionary with the format provided in the method:
            :py:meth:`_create_user_object`

        '''
        #Create the SQL Statements
        #SQL Statement for retrieving the user information
        query = 'SELECT * FROM users \
                  WHERE username = ? '
        #Variable to be used in the second query.
        user_id = None
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute SQL Statement to retrieve the id given a nickname
        pvalue = (username,)
        #execute the statement
        cur.execute(query, pvalue)
        #Process the response. Only one posible row is expected.
        row = cur.fetchone()
        if row is None:
            return None
        return self._create_user_object(row)

    def create_user(self, username, password, email = None, mobile = None, website = None, isAdmin='0', createdBy='0'):
        '''
        Create a new user with username, password and other information.

        :param str username: The username of the user.
        :param str password: The password of the user.
        :param str email: The email of the user.
        :param str mobile: The mobile of the user.
        :param str website: The website of the user.
        :param integer isAdmin: 0: user, 1: admin.
        :param integer createdBy: userID of user who created this user, or blank.
        :return: userID:

        '''
        #Create the SQL Statements
        #SQL Statement for retrieving the user information
        stmnt = 'INSERT INTO users (username, password, email, \
                 mobile, website, isAdmin, createdBy, createdAt) \
                 VALUES(?,?,?,?,?,?,?,?)'
        timestamp = time.mktime(datetime.now().timetuple())
        #Variable to be used in the second query.
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute SQL Statement to retrieve the id given a username
        pvalue = (username,password,email, mobile, website, isAdmin, createdBy, timestamp)
        #execute the statement
        cur.execute(stmnt, pvalue)
        #Process the response. Only one posible row is expected.
        self.con.commit()
        #Extract the id of the added message
        lid = cur.lastrowid
        #Return the id in
        return lid if lid is not None else None

    def delete_user(self, username):
        '''
        Remove all user information of the user with the nickname passed in as
        argument.

        :param str nickname: The nickname of the user to remove.

        :return: True if the user is deleted, False otherwise.

        '''
        #Create the SQL Statements
          #SQL Statement for deleting the user information
        query = 'DELETE FROM users WHERE username = ?'
        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to delete
        pvalue = (username,)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that it has been deleted
        if cur.rowcount < 1:
            return False
        return True

    def modify_user(self, username, password, email = None, mobile= None, website = None, updatedBy = '0'):
        '''
        Modify the information of a user.

        :param str username: The nickname of the user to modify
        :param str password: The password of the user to modify
        :param str email: The email of the user to modify
        :param str mobile: The mobile of the user to modify
        :param str website: The website of the user to modify
        :param integer updatedBy: The username of the user who modify this user


            Note that all values are string if they are not otherwise indicated.

        :return: the username of the modified user or None if the
            ``username`` passed as parameter is not  in the database.

        '''
                #Create the SQL Statements
          #SQL Statement to update the user_profile table
        query = 'UPDATE users SET password = ?,email = ?, \
                                           mobile = ?,website = ?, \
                                           updatedAt = ?, updatedBy = ? \
                                           WHERE username = ?'
        #temporal variables
        user_id = None

        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to extract the id associated to a nickname
        #execute the main statement
        timestamp = time.mktime(datetime.now().timetuple())
        pvalue = (password, email, mobile, website, timestamp,
                updatedBy, username)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that I have modified the user
        if cur.rowcount < 1:
            return None
        return username

    def change_role_user(self, username, isAdmin='0', updatedBy='0'):
        '''
        Change user role of user in the database.

        :param str username: The username of the user to modify
        :param integer isAdmin: 0:normal user or 1: admin
        :param integer updatedBy: The userID of the user who modify this user

        :return: the username of the modified user or None if the
            username passed as parameter is not  in the database.

        '''
        #Create the SQL Statements
          #SQL Statement for extracting the userid given a username
        query = 'UPDATE users SET isAdmin = ?,updatedBy = ?, \
                                           updatedAt = ? WHERE username = ?'
        #temporal variables

        #Activate foreign key support
        self.set_foreign_keys_support()
        #Cursor and row initialization
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        #Execute the statement to extract the id associated to a username
        #execute the main statement
        timestamp = time.mktime(datetime.now().timetuple())
        pvalue = (isAdmin, updatedBy, timestamp, username)
        cur.execute(query, pvalue)
        self.con.commit()
        #Check that I have modified the user
        if cur.rowcount < 1:
            return None
        return username
