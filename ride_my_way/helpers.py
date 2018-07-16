import re  # # here i import the module that implements regular expressions
from functools import wraps
from flask import request, jsonify
import jwt
from ride_my_way.models import DatabaseConnection

"""creating an instance of the DatabaseConnections table
   used o execute run methods in the models.py
"""
database_connection = DatabaseConnection()


""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


def token_required(f):
    """ Restricts access to only logged in i.e users with the right token """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({"message": "Token missing"}), 401


        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
            database_connection.cursor.execute(sql)
            current_user = database_connection.cursor.fetchone()
        except Exception as ex:
            return jsonify({"message": str(ex)}), 401

        return f(current_user, *args, **kwargs)
    return decorated


# here is my function for checking valid email address
def test_email(email):
    # message returned when email is invalid
    wrong_email = "{} is not a valid email".format(email)

    # verifying the submitted email

    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    email = re.match(pattern, email)  # returns none if no match
    if not email:
        return jsonify({"message": wrong_email}), 400


# here is my function for checking valid
def test_phone_number(phone_number):
    wrong_phone_number = "{} is not a valid phone number".format(phone_number)
    pattern = r"^(\+?\d{1,4}[\s-])?(?!0+\s+,?$)\d{10}\s*,?$"
    phone_number = re.match(pattern, phone_number)
    if not phone_number:
        return jsonify({"message": wrong_phone_number}), 400


# here is a function for checking a valid password
def test_password(password):
    wrong_password = "Password should be alphanumeric and at least 6 characters long"
    pattern = r"^(?=.*\d)(?=.*[a-z])[a-zA-Z0-9]{6,999}$"
    password = re.match(pattern, password)
    if not password:
        return jsonify({"message": wrong_password}), 400
