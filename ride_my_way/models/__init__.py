import psycopg2
from ride_my_way.models.database_tables import tables_list
import os

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 9000


class DatabaseConnection(object):
    """

    Creates database connection and tables
    Has methods associated with database objects like
    users, rides and ride requests
    The methods are called from the views.py file

    """

    def __init__(self):
        """ Initialising a database connection """
        if os.getenv('APP_SETTINGS') == "testing":
            self.dbname = "test_db"
        elif os.getenv('APP_SETTINGS') == 'development':
            self.dbname = "ride_my_way"
        else:
            self.dbname = 'dc3n9hdb7ngcus'

        if os.getenv('APP_SETTINGS') == 'testing' or os.getenv('APP_SETTINGS') == 'development':

            try:
                # establishing a server connection
                self.connection = psycopg2.connect(dbname="{}".format(self.dbname),
                                                user="postgres",
                                                password="Kp15712Kp",
                                                host="localhost"
                                                )
                self.connection.autocommit = True

                # activate connection cursor
                self.cursor = self.connection.cursor()
            except psycopg2.Error as err:
                # bug in returning under the __init__
                print("Can not establish a database connection")
        else:
            try:
                # establishing a server connection
                self.connection = psycopg2.connect(dbname="{}".format(self.dbname),
                                                user="hiyjfbbmaysfxe",
                                                password="629bd500da19e2929cb8b5bf5a975497776acdb19129036f91c19291bf614e0c",
                                                host="ec2-54-225-249-161.compute-1.amazonaws.com"
                                                )
                self.connection.autocommit = True

                # activate connection cursor
                self.cursor = self.connection.cursor()
            except psycopg2.Error as err:
                # bug in returning under the __init__
                print("Can not establish a database connection")

    def create_tables(self):
        """ Create database tables from the database_tables.py file """
        for table_info in tables_list:
            for table_name in table_info:
                self.cursor.execute(table_info[table_name])

# This is placed here to prevent circular imports
# remember these imported classes inherit from DatabaseConnection
from ride_my_way.models.users import Users
from ride_my_way.models.rides import Rides
from ride_my_way.models.ride_requests import RideRequests


class DbClass(Users, Rides, RideRequests):
    """ This class brings together all the classes that inherit
        from the DatabaseConnection class
    """

    def just(self):
        # This is does ensures that this class is not empty
        pass
