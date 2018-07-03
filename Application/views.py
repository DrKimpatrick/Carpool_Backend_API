from flask import Flask, request, jsonify
from Application.models import DatabaseConnection
app = Flask(__name__)

# creating an instance of the DatabaseConnections table
database_connection = DatabaseConnection()


@app.route('/api/v1/users/signup', methods=['POST'])
def create_user():
    """ Creating a user. users_list = [{"username":"", "name":""}]"""

    if (not request.json or
            "name" not in request.json or
            "email" not in request.json or
            "username" not in request.json or
            "phone_number" not in request.json or
            "bio" not in request.json or
            "gender" not in request.json or
            "password" not in request.json):

        return jsonify(
            {"error": "You have either missed out some info or used wrong keys"}
        ), 400

    name = request.json["name"]
    email = request.json['email']
    username = request.json['username']
    phone_number = request.json['phone_number']
    bio = request.json['bio']
    gender = request.json['gender']
    password = request.json['password']

    result = database_connection.signup(name, email, username, phone_number, bio, gender, password)

    return jsonify({"Users": result})

    # result = database_connection.get_username("kim")
    # return jsonify({"user": result})


@app.route('/api/v1/users/login', methods=['POST'])
def login():
    """ The function confirms the presence of user. It does not login the user """

    if (not request.json or
            "email" not in request.json or
            "password" not in request.json):
        return jsonify(
            {"error": "You have either missed out some info or used wrong keys"}
        ), 400

    email = request.json['email']
    password = request.json['password']

    # sign_in now
    result = database_connection.sign_in(email, password)
    return jsonify({"message": result})


@app.route('/api/v1/users', methods=['GET'])
def list_of_users():
    """ Get all users"""
    result = database_connection.get_all_users()
    return jsonify({"Users": result})




