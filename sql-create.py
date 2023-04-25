"""
Creates tables in the database for the CloudFlare plugin

Run independantly of the main plugin, to create the table in the database

Modules:
    3rd Party: pyodbc, sys
    Custom: None

Classes:

    CloudFlareHandler
        Handle webhooks from Cloudflare
        Generate messages for Teams

Functions

    None

Exceptions:

    None

Misc Variables:

    LOCATION : str
        The location of the config file

Limitations/Requirements:
    No SQL logging at this time

Author:
    Luke Robertson - April 2023
"""


import pyodbc
import sys
import yaml


def connect(server, db):
    '''
    Connect to an SQL server

    Parameters:
        server : str
            The server to connect to
        db : str
            The database to connect to

    Raises:
        pyodbc.DataError
            If there is a data error
        pyodbc.OperationalError
            Operational error, such as bad credentials
        pyodbc.IntegrityError
            Integrity error
        pyodbc.InternalError
            A server error
        pyodbc.ProgrammingError
            Errors in the code, such as typos
        pyodbc.NotSupportedError
            The SQL command is not supported on this server
        pyodbc.Error
            Some generic error

    Returns:
        conn, cursor : tuple
            The connection object and the SQL cursor
    '''

    # Connect to the server and database
    try:
        conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=%s;'
            'Database=%s;'
            'Trusted_Connection=yes;'
            % (server, db))

    except pyodbc.DataError as e:
        print("A data error has occurred")
        print(e)
        return False

    except pyodbc.OperationalError as e:
        print("An operational error has occurred while \
            connecting to the database")
        print("Make sure the specified server is correct, \
            and that you have permissions")

        # Parse the error code and message
        error = str(e).split(",", 1)[1].split(";")[0].split("[")
        code = error[1].replace("] ", "")
        message = error[4].split("]")[1].split(".")[0]

        # Print the error, and end the script
        print(f"Error code: {code}\n{message}")
        return False

    except pyodbc.IntegrityError as e:
        print("An Integrity error has occurred")
        print(e)
        return False

    except pyodbc.InternalError as e:
        print("An internal error has occurred")
        print(e)
        return False

    except pyodbc.ProgrammingError as e:
        print("A programming error has occurred")
        print("Check that the database name is correct, \
            and that the database exists")

        # Parse the error code and message
        error = str(e).split(",", 1)[1].split(";")[0].split("[")
        code = error[1].replace("] ", "")
        message = error[4].split("]")[1].split(".")[0]

        # Print the error, and end the script
        print(f"Error code: {code}\n{message}")
        return False

    except pyodbc.NotSupportedError as e:
        print("A 'not supported' error has occurred")
        print(e)
        return False

    except pyodbc.Error as e:
        print("A generic error has occurred")
        print(e)
        return False

    # If the connection was successful, create a cursor
    cursor = conn.cursor()

    # Return the connection and the cursor as a tuple
    return conn, cursor


def close(connector):
    '''
    Close a connection to the SQL server

    Parameters:
        connector : pyodbc object
            An object representing the connection to the DB

    Raises:
        None


    Returns:
        None
    '''

    connector[1].close()
    connector[0].close()


def create_table(table, fields, connector):
    '''
    Create an SQL table

    Parameters:
        table : str
            The table name
        fields : dict
            The column names and type
        connector : pyodbc object
            An object representing the connection to the DB

    Raises:
        Exception
            If there was a problem executing the SQL command
        Exception
            If there was a problem committing the SQL changes


    Returns:
        False : Boolean
            If there's a problem
    '''

    # Build a valid SQL 'CREATE TABLE' command
    sql_string = (f'CREATE TABLE {table} (')
    for field in fields:
        sql_string += field + ' ' + fields[field] + ','
    sql_string += ')'

    # Attempt to connect to the SQL server
    try:
        connector[1].execute(sql_string)

    # If there's a problem, print errors and quit
    except Exception as e:
        print("SQL execution error")
        error = str(e).split(",", 1)[1].split(";")[0].split("[")
        code = error[1].replace("] ", "")
        message = error[4].split("]")[1].split(".")[0]

        print(code, message)

        if code == str(42000):
            print("Programming error. \
                Check that there are no typos in the SQL syntax")
        return False

    # Commit the SQL changes
    try:
        connector[0].commit()

    # Handle errors
    except Exception as e:
        print("SQL commit error")
        print(e)
        return False


# Create the tables
if __name__ == '__main__':
    print("...")
    '''
    Create SQL entries fields
    '''

    TABLE_NAME = 'cloudflare_events'
    CONFIG_FILE = '../../../chatbot/config.yaml'

    print("Running script...")

    # Open the YAML file, and store in the 'config' variable
    with open(CONFIG_FILE) as config:
        try:
            config = yaml.load(config, Loader=yaml.FullLoader)
        except yaml.YAMLError as err:
            print('Error parsing config file, exiting')
            print(err)
            sys.exit()

    # Get the DB server and name from global config
    SQL_SERVER = config['global']['db_server']
    DATABASE = config['global']['db_name']

    # Connect to the DB
    print("Connecting to the database...")
    sql_connector = connect(SQL_SERVER, DATABASE)
    if sql_connector:
        print("Connected to the database")
    else:
        print("Failed to connect")
        sys.exit()

    # Create a dictionary of fields we want to create
    fields = {
        'id': 'int IDENTITY(1,1) PRIMARY KEY not null',
        'type': 'text null',
        'pool': 'text null',
        'service': 'text null',
        'health': 'text null',
        'reason': 'text null',
        'logdate': 'date not null',
        'logtime': 'time not null',
        'source': 'binary(4) not null',
    }

    # Create the table
    print("Creating table...")
    create_table(TABLE_NAME, fields, sql_connector)

    # Cleanup
    print("Closing SQL connection...")
    close(sql_connector)
    print("Done")
