import psycopg2
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash
from Application.database_tables import tables_list
import jwt

from datetime import datetime, timedelta

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 5000


class DatabaseConnection(object):
    def __init__(self):
        """ Initialising a database connection """
        try:
            # establishing a server connection
            self.connection = psycopg2.connect(dbname="Ride_my_way_2", user="postgres", password="Kp15712Kp", host="localhost")
            self.connection.autocommit = True

            # activate connection cursor
            self.cursor = self.connection.cursor()
        except psycopg2.Error as err:
            pprint(err)

    def create_tables(self):
        """ Create database tables from the database_tables.py file """
        for table_info in tables_list:
            for table_name in table_info:
                self.cursor.execute(table_info[table_name])

    # username, email and phone_number are unique
    def should_be_unique(self, username, email, phone_number):
        """ Ensures username, email and phone_number are unique"""

        select_query = "SELECT username, email, phone_number FROM carpool_users"
        self.cursor.execute(select_query)
        row = self.cursor.fetchall()
        for result in row:
            if result[0] == username:
                return "Username already taken, try another"
            if result[1] == email:
                return "User account with that email already exists"
            if result[2] == phone_number:
                return "User account with that phone number already exists"

    def signup(self, name, email, username, phone_number, bio, gender, password):

        # Check if they are unique
        if self.should_be_unique(username, email, phone_number):
            return self.should_be_unique(username, email, phone_number)

        # hashing the password
        hashed_password = generate_password_hash(password, method="sha256")

        try:
            sql = "INSERT INTO carpool_users(name, email, username, phone_number, bio, gender, password) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (name, email, username, phone_number, bio, gender, hashed_password))
        except psycopg2.Error as err:
            return str(err)
        return "Account successfully created"

    def sign_in(self, username, password):
        select_query = "SELECT username, password, id FROM carpool_users"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        for user_info in result:
            if user_info[0] == username and check_password_hash(user_info[1], password):
                payload = {
                    'id': user_info[2],
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
                token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                return token.decode('UTF-8')

        else:
            return "Email or password is incorrect"

    def get_all_users(self):
        select_query = "SELECT name, username, email, phone_number, bio, gender FROM carpool_users"
        self.cursor.execute(select_query)
        results = self.cursor.fetchall()

        # list of all users
        user_list = []

        for user in results:

            user_info = {}
            user_info['name'] = user[0]
            user_info['username'] = user[1]
            user_info['email'] = user[2]
            user_info['phone_number'] = user[3]
            user_info['bio'] = user[4]
            user_info['gender'] = user[5]

            user_list.append(user_info)

        return user_list

    def create_ride(self, driver_id, origin, meet_point, contribution, free_spots, start_date, finish_date):
        try:
            sql = "INSERT INTO carpool_rides(driver_id, " \
                                             "origin, " \
                                             "meet_point, " \
                                             "contribution, " \
                                             "free_spots, start_date, " \
                                             "finish_date) " \
                                             "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (driver_id, origin, meet_point, contribution, free_spots, start_date, finish_date))
        except psycopg2.Error as err:
            return str(err)
        return "Ride create successfully"

    def get_rides(self):
        sql = "SELECT origin, meet_point, contribution, free_spots, start_date, finish_date FROM carpool_rides"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        rides_list = []
        for ride in result:

            ride_info = {}
            ride_info['origin'] = ride[0]
            ride_info['meet_point'] = ride[1]
            ride_info['contribution'] = ride[2]
            ride_info['free_spots'] = ride[3]
            ride_info['start_date'] = ride[4]
            ride_info['finish_date'] = ride[5]

            rides_list.append(ride_info)
        return rides_list

    def rides_given(self, driver_id):
        """ Retrieves the rides given by the User (Driver)"""
        sql = "SELECT origin, meet_point, contribution, free_spots, start_date, finish_date FROM carpool_rides WHERE driver_id=%s" % (driver_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        rides_list = []
        for ride in result:
            ride_info = {}
            ride_info['origin'] = ride[0]
            ride_info['meet_point'] = ride[1]
            ride_info['contribution'] = ride[2]
            ride_info['free_spots'] = ride[3]
            ride_info['start_date'] = ride[4]
            ride_info['finish_date'] = ride[5]

            rides_list.append(ride_info)
        return rides_list



