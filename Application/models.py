import psycopg2
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash

from Application.database_tables import tables_list


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

    def sign_in(self, email, password):
        select_query = "SELECT email, password FROM carpool_users"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall()

        for user_info in result:
            if user_info[0] == email and check_password_hash(user_info[1], password):
                return "Your are logged in"

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




