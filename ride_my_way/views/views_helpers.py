from functools import wraps
from flask import request, jsonify
import jwt
from ride_my_way import database_connection


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

