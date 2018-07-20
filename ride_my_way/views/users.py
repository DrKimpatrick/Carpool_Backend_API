from flask import Flask, request, jsonify
from ride_my_way.views_helpers import (token_required,
                                       check_user_field_type,
                                       check_user_fields,
                                       generate_user_field_dict,
                                       database_connection)

app = Flask(__name__)  # Initialising a flask application


@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    """ Creating a user account
        calls the signup() func in models.py
    """
    # check that there are no missed out info or used wrong keys
    if check_user_fields():
        return check_user_fields()

    # keep all the user fields in a dictionary
    user_fields = generate_user_field_dict()

    # check that information is not invalid
    if check_user_field_type(user_fields):
        return check_user_field_type(user_fields)

    new_user = {'name': user_fields['name'],
                "email": user_fields['email'],
                "username": user_fields['username'],
                "phone_number": user_fields['phone_number'],
                "bio": user_fields['bio'],
                "gender": user_fields['gender'],
                "password": user_fields['password']}

    result = database_connection.signup(new_user)

    return result


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """ The function confirms the presence of user.
        It login s in the user by providing a web token
    """

    if (not request.json or
            "username" not in request.json or
            "password" not in request.json):
        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400

    username = request.json['username']
    password = request.json['password']

    # sign_in now
    result = database_connection.sign_in(username, password)
    return result


@app.route('/api/v1/users', methods=['GET'])
@token_required
def list_of_users(current_user):
    """ Get all users"""
    result = database_connection.get_all_users()
    return jsonify({"Users": result})

