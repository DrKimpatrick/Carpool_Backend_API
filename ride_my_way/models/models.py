import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from ride_my_way.database_tables import tables_list  # has the sql for table creation
import jwt
from flask import jsonify
import os

from datetime import datetime, timedelta

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
        else:
            self.dbname = "Ride_my_way_2"

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

    def create_tables(self):
        """ Create database tables from the database_tables.py file """
        for table_info in tables_list:
            for table_name in table_info:
                self.cursor.execute(table_info[table_name])

    def should_be_unique(self,
                         username,
                         email,
                         phone_number
                         ):
        """ Is a helper function that is called by other functions
            to ensure username and phone_number are unique
        """

        select_query = "SELECT username, email, phone_number FROM carpool_users"
        self.cursor.execute(select_query)
        row = self.cursor.fetchall()
        for result in row:
            if result[0] == username:
                return jsonify(
                    {"message": "Username already taken, try another"}), 406
            if result[1] == email:
                return jsonify(
                    {"message": "User account with that email already exists"}), 406
            if result[2] == phone_number:
                return jsonify(
                    {"message": "User account with that phone number already exists"}), 406

    # new_user = {}
    def signup(self, new_user):

        # Check if username, email and phone_number don't exist
        if self.should_be_unique(new_user['username'], new_user['email'], new_user['phone_number']):
            return self.should_be_unique(new_user['username'], new_user['email'], new_user['phone_number'])

        # hashing the password
        hashed_password = generate_password_hash(new_user['password'], method="sha256")

        # inserting user info into the carpool_users table
        try:
            sql = "INSERT INTO carpool_users(name, email, username, " \
                  "phone_number, bio, gender, password) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql,
                                (new_user['name'], new_user['email'], new_user['username'], new_user['phone_number'],
                                 new_user['bio'], new_user['gender'], hashed_password)
                                )
        except Exception as err:
            return jsonify({"message": "{}".format(str(err))}), 406
        return jsonify({"message": "Account successfully created"}), 201

    def sign_in(self, username, password):
        """ A sign a web token to current user if username and password match """
        try:
            # query the user table for the username and password
            select_query = "SELECT username, password, id FROM carpool_users"
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
        except Exception as err:
            return str(err)

        # assigning a web token if info right
        for user_info in result:
            if user_info[0] == username and check_password_hash(user_info[1], password):
                payload = {
                    'id': user_info[2],
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
                token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                return jsonify({"Token": token.decode('UTF-8')}), 200

        else:
            return jsonify({"message": "Email or password is incorrect"}), 404

    def get_all_users(self):
        """ Returns a list of all users in the database """

        select_query = "SELECT name, username, email, phone_number, " \
                       "bio, gender FROM carpool_users"
        self.cursor.execute(select_query)
        results = self.cursor.fetchall()

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

    # new_ride = {}
    def create_ride(self, new_ride):
        """ Creates ride offer in the database
            The driver_id which is a foreign key is gotten from
            the current_user instance in the token_required()
            decorator as id
        """
        try:
            sql = "INSERT INTO carpool_rides(driver_id, " \
                                             "origin, " \
                                             "meet_point, " \
                                             "contribution, " \
                                             "free_spots, start_date, " \
                                             "finish_date) " \
                                             "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(
                                sql,
                                (new_ride['driver_id'], new_ride['origin'],
                                 new_ride['meet_point'], new_ride['contribution'],
                                 new_ride['free_spots'], new_ride['start_date'],
                                 new_ride['finish_date'])
                                )
        except psycopg2.Error as err:
            return str(err)
        return jsonify({"message": "Ride create successfully"}), 201

    def get_rides(self):
        """ Returns a list of all ride offers available """

        sql = "SELECT origin, meet_point, contribution, free_spots, " \
              "start_date, finish_date, id FROM carpool_rides"
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
            ride_info['ride_id'] = ride[6]

            rides_list.append(ride_info)
        return jsonify({"Rides": rides_list}), 200

    def rides_given(self, driver_id):
        """ Returns a list of rides given by the User(Driver)"""
        try:
            sql = "SELECT origin, meet_point, contribution, free_spots, " \
                  "start_date, finish_date, id FROM carpool_rides WHERE " \
                  "driver_id=%s" % driver_id
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            return jsonify({"message": "Some thing went wrong"}), 500

        rides_list = []
        for ride in result:
            ride_info = {}
            ride_info['origin'] = ride[0]
            ride_info['meet_point'] = ride[1]
            ride_info['contribution'] = ride[2]
            ride_info['free_spots'] = ride[3]
            ride_info['start_date'] = ride[4]
            ride_info['finish_date'] = ride[5]
            ride_info['ride_id'] = ride[6]

            rides_list.append(ride_info)
        return rides_list

    def get_user_info(self, user_id):
        """ Gets the info of the user with the user_id provided"""

        sql = "SELECT username, phone_number, gender " \
              "FROM carpool_users WHERE id=%s" % user_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        user = {}  # holds user information
        for user_info in result:
            user['username'] = user_info[0]
            user['gender'] = user_info[2]
            user['phone number'] = user_info[1]
        return user

    def ride_details(self, ride_id):
        """ Returns the details of a ride offer with the ride_id provided
            Also contains the driver information
        """

        sql = "SELECT origin, meet_point, contribution, free_spots, start_date, " \
              "finish_date, driver_id FROM carpool_rides WHERE id=%s" % ride_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return jsonify(
                {"message": "The ride offer with ride_id {} does not exist".format(ride_id)}
            ), 404

        ride_info = {}
        for info in result:
            # driver information to be returned with rides details
            driver_id = info[6]
            driver_info = self.get_user_info(driver_id)
            ride_info['Driver details'] = driver_info

            ride_info['origin'] = info[0]
            ride_info['meet_point'] = info[1]
            ride_info['contribution'] = info[2]
            ride_info['free_spots'] = info[3]
            ride_info['start_date'] = info[4]
            ride_info['finish_date'] = info[5]

        return jsonify({"Ride details": ride_info})

    def request_ride(self, current_user, ride_id):
        """ Post a request for a ride by providing the ride id"""

        # ensure that user does not make more requests to the same ride
        try:
            sql = "SELECT ride_id, passenger_id FROM carpool_ride_request"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for request_info in result:
                if request_info[0] == ride_id and request_info[1] == current_user:
                    return jsonify(
                        {"message": "You already made a request to that ride"}
                    ), 406
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        # check to see whether the current user is the author of that ride
        # Current user should not make a request to the ride he/she created
        try:
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}".format(ride_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": "Ride_id ({}) does not exist".format(ride_id)}), 404

        if result:
            return jsonify(
                {"message":
                 "Your can not make a ride request to a ride you created"}
            ), 406

        # Now make a request to a ride offer
        try:
            sql = "INSERT INTO carpool_ride_request(ride_id, passenger_id)" \
                  " VALUES(%s, %s)"
            self.cursor.execute(sql, (ride_id, current_user))
        except psycopg2.Error as err:
            return jsonify({"message": "Ride_id ({}) does not exist".format(ride_id)}), 404
        return jsonify(
            {"message":
             "Your request has been successfully sent and pending approval"}
        ), 200

    def all_requests(self):
        """ Retrieves all ride requests"""
        sql = "SELECT * FROM carpool_ride_request"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def requests_to_this_ride(self,
                              current_user,
                              ride_id
                              ):
        """ Retrieves all ride requests for that ride offer
            Only if the current user is the author of the ride offer
        """

        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}"\
                .format(ride_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride with ride_id ({}), recheck the info and try again"
                 .format(ride_id)}
            ), 404

        try:
            # fetching data from the ride requests table where ride_id is
            sql = "SELECT id, passenger_id, accepted FROM  " \
                  "carpool_ride_request WHERE ride_id=%s" % ride_id
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "No requests made to ride with ride_id ({})".format(ride_id)}
            ), 404

        requests_list = []
        for r_request in result:
            request_info = {}
            request_info['request id'] = r_request[0]
            request_info['request status'] = r_request[2]

            # getting the passenger information
            passenger_id = r_request[1]
            passenger_info = self.get_user_info(passenger_id)
            request_info['passenger details'] = passenger_info
            requests_list.append(request_info)

        return jsonify({"Ride requests": requests_list}), 200

    def respond_to_request(self,
                           current_user,
                           request_id,
                           status
                           ):
        """ Driver accepts or rejects a ride request in reaction to a request """

        # check for the presence of that request id
        sql = "SELECT ride_id FROM carpool_ride_request WHERE id={}"\
              .format(request_id)
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        if not result:
            return jsonify(
                {
                    "message": "No request with id ({})".format(request_id)
                }
            ), 404

        # getting the ride_id to the ride where the request is made
        # result is of length one
        ride_id = result[0][-1]

        # ensure that the current user actually created that ride
        sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}"\
              .format(ride_id, current_user)

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if not result:
            return jsonify(
                {
                 "message":
                 "Sorry, you can only react to a ride request for the ride you created"
                }
            ), 406
        sql = "UPDATE carpool_ride_request SET accepted='{}' WHERE id={}"\
              .format(status, request_id)

        self.cursor.execute(sql)

        return jsonify({"message": "Ride request successfully {}".format(status)}), 200

    def delete_ride(self, current_user, ride_id):
        """ Deletes the ride """
        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}"\
                .format(ride_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride with ride_id ({}), recheck the info and try again"
                 .format(ride_id)}
            ), 404

        try:
            # check for the presence of that ride id
            sql = "DELETE FROM carpool_rides WHERE id={} AND driver_id={}"\
                .format(ride_id, current_user)
            self.cursor.execute(sql)
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        return jsonify(
            {"message":
             "You have successfully deleted a ride with ride_id {}".format(ride_id)})

    # edit_ride = {}
    def edit_ride(self, edit_ride):
        """ Deletes the ride """
        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}"\
                .format(edit_ride['ride_id'], edit_ride['current_user'])
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride with ride_id ({}), recheck the info and try again"
                 .format(edit_ride['ride_id'])}
            ), 404

        try:
            # check for the presence of that ride id
            sql = "UPDATE carpool_rides " \
                  "SET origin='{}', meet_point='{}', " \
                  "contribution='{}', free_spots='{}', " \
                  "start_date='{}', finish_date='{}', " \
                  "terms='{}' WHERE id={} AND driver_id={}"\
                .format(edit_ride['origin'], edit_ride['meet_point'],
                        edit_ride['contribution'], edit_ride['free_spots'],
                        edit_ride['start_date'], edit_ride['finish_date'],
                        edit_ride['terms'], edit_ride['ride_id'],
                        edit_ride['current_user'])
            self.cursor.execute(sql)
        except psycopg2.Error as err:
            return jsonify({"message": str(err) + " " + " Update"}), 500

        return jsonify(
            {"message":
             "You have successfully edited a ride with ride_id {}".format(edit_ride['ride_id'])})

    def delete_request(self,
                       current_user,
                       request_id
                       ):
        """ Driver accepts or rejects a ride request in reaction to a request """

        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_ride_request WHERE id={} AND passenger_id={}"\
                .format(request_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride request with request_id ({}), "
                 "recheck the info and try again"
                 .format(request_id)}
            ), 404

        try:
            # check for the presence of that ride id
            sql = "DELETE FROM carpool_ride_request WHERE id={} AND passenger_id={}"\
                .format(request_id, current_user)
            self.cursor.execute(sql)
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        return jsonify(
            {"message":
             "You have successfully deleted a ride request with request_id {}".format(request_id)})