import jwt
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from ride_my_way.models import DatabaseConnection


""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 9000


class Users(DatabaseConnection):
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

    def sign_in(self, username_or_email, password):
        """ A sign a web token to current user if username and password match
            sign in with a username or email
        """
        try:
            # query the user table for the username and password
            select_query = "SELECT username, password, id, email FROM carpool_users"
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
        except Exception as err:
            return str(err)

        # assigning a web token if info right
        for user_info in result:
            if (user_info[0] == username_or_email and check_password_hash(user_info[1], password)  # username
                  or user_info[3] == username_or_email and check_password_hash(user_info[1], password)):  # email
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

    def get_user_info_users(self, user_id):
        """ Gets the info of the user with the user_id provided"""

        sql = "SELECT username, phone_number, gender, email, bio " \
              "FROM carpool_users WHERE id=%s" % user_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        user = {}  # holds user information
        for user_info in result:
            user['username'] = user_info[0]
            user['phone_number'] = user_info[1]
            user['gender'] = user_info[2]
            user['email'] = user_info[3]
            user['bio'] = user_info[4]

        return jsonify({"User_info": user})
