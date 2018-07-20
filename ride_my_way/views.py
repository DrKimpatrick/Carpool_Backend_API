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


# check that all input fields are available
def check_ride_fields():
    """ Ensure that all fields are available
        and wrong keys are not provided

        It is a helper function that is called in
        create ride and edit ride | all provide the same fields
    """
    if (not request.json or
            "terms" not in request.json or
            "finish_date" not in request.json or
            "start_date" not in request.json or
            "free_spots" not in request.json or
            "contribution" not in request.json or
            'origin' not in request.json or
            'destination' not in request.json or
            "meet_point" not in request.json):

        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400


# get ride fields
def generate_ride_field_dict():
    """ Keep all the ride info in the dictionary
        Is input for check_ride_field_type helper func
    """
    origin = request.json['origin']
    destination = request.json['destination']
    meet_point = request.json['meet_point']
    contribution = request.json['contribution']
    free_spots = request.json['free_spots']
    start_date = request.json['start_date']
    finish_date = request.json['finish_date']
    terms = request.json['terms']

    ride_fields = {"origin": origin, "destination": destination,
                   "meet_point": meet_point, "contribution": contribution,
                   "free_spots": free_spots, "start_date": start_date,
                   "finish_date": finish_date, "terms": terms
                   }

    return ride_fields


# check ride field types
def check_ride_field_type(ride_fields):
    """ Checks the type of the ride field inputs
        Take in the the ride fields as a dictionary
    """

    if not isinstance(ride_fields['terms'], str):
        return jsonify({"message": "terms should be string"}), 400

    if not isinstance(ride_fields['start_date'], str):
        return jsonify({"message": "Start date should be string"}), 400

    if not isinstance(ride_fields['finish_date'], str):
        return jsonify({"message": "Finish date should be string"}), 400

    if not isinstance(ride_fields['free_spots'], int):
        return jsonify({"message": "Free spots should be integer"}), 400

    if not isinstance(ride_fields['origin'], str):
        return jsonify({"message": "Origin should be string"}), 400

    if not isinstance(ride_fields['destination'], str):
        return jsonify({"message": "Destination should be string"}), 400

    if not isinstance(ride_fields['meet_point'], str):
        return jsonify({"message": "meet_point should be string"}), 400

    if not isinstance(ride_fields['contribution'], (int, float, complex)):
        return jsonify({"message": "contribution should be integer"}), 400


@app.route('/api/v1/users/rides', methods=['POST'])
@token_required
def create_ride(current_user):
    """ Creating a ride offer """

    # check that there are no missed out info or used wrong keys
    if check_ride_fields():
        return check_ride_fields()

    # keep all the ride fields in a dictionary
    ride_fields = generate_ride_field_dict()

    # Checking for errors linked to the input type
    if check_ride_field_type(ride_fields):
        return check_ride_field_type(ride_fields)

    new_ride = {"driver_id": current_user[0],
                "origin": ride_fields['origin'],
                "meet_point": ride_fields['meet_point'],
                "contribution": ride_fields['contribution'],
                "free_spots": ride_fields['free_spots'],
                "start_date": ride_fields['start_date'],
                "finish_date": ride_fields['finish_date']}
    result = database_connection.create_ride(new_ride)
    return result


@app.route('/api/v1/rides', methods=['GET'])
@token_required
def available_ride(current_user):
    """ Retrieves all the available ride offers """
    result = database_connection.get_rides()
    return result


@app.route('/api/v1/this/user/rides', methods=['GET'])
@token_required
def driver_rides(current_user):
    """ Retrieves all the available ride offers """
    result = database_connection.rides_given(current_user[0])
    return jsonify({"{}'s ride offers".format(current_user[2]): result})


@app.route('/api/v1/rides/<ride_id>', methods=['GET'])
@token_required
def get_single_ride(current_user, ride_id):
    """ Retrieve a single ride by providing the ride_id """
    try:
        ride_id = int(ride_id)
    except:
        return jsonify({"message": "Input should be integer"}), 400

    if not isinstance(ride_id, int):
        return jsonify({"message": "Input should integer"}), 400
    else:
        result = database_connection.ride_details(ride_id)
        return result


@app.route('/api/v1/rides/<ride_id>/requests', methods=['POST'])
@token_required
def request_for_ride(current_user, ride_id):
    """ Passenger can request for a ride by providing the ride_id"""
    try:
        ride_id = int(ride_id)
    except ValueError as exc:
        return jsonify(
            {"message": "ride_id should be of type integer"}
        ), 400
    result = database_connection.request_ride(current_user[0], ride_id)
    return result


@app.route('/api/v1/users/rides/<ride_id>/requests', methods=['GET'])
@token_required
def requests_to_this_ride(current_user, ride_id):
    """ Retrieves all ride requests for that ride offer with id passed in """
    try:
        ride_id = int(ride_id)
    except ValueError as exc:
        return jsonify(
            {"message": "ride_id should be of type integer"}
        ), 400
    if not isinstance(ride_id, int):
        return jsonify({"message": "ride_id should be of type integer"}), 400

    result = database_connection.requests_to_this_ride(current_user[0], ride_id)
    return result


@app.route('/api/v1/users/rides/<request_id>/reaction', methods=['PUT'])
@token_required
def reaction_to_ride_request(current_user, request_id):
    """ Driver accepts or rejects a ride request """
    try:
        request_id = int(request_id)
    except ValueError as exc:
        return jsonify(
            {"message": "request_id should be of type integer"}
        ), 400
    if not isinstance(request_id, int):
        return jsonify({"message": "request_id should be of type integer"}), 400

    if not request.json or 'reaction' not in request.json:
        return jsonify(
            {
                "message":
                "Input should be of type dictionary where key is 'reaction' and"
                " value 'reject' or 'accept' or 'pending' set back to default"
            }
        ), 400

    status = request.json['reaction']
    # changing the status of a request
    if status == 'reject':
        status = 'rejected'
    if status == 'accept':
        status = 'accepted'
    if status == 'pending':
        status = 'pending'

    result = database_connection.respond_to_request(current_user[0], request_id, status)
    return result


@app.route('/api/v1/users/rides/<ride_id>/delete', methods=['DELETE'])
@token_required
def delete_ride_offer(current_user, ride_id):
    """ Deletes the ride with id provided """
    try:
        ride_id = int(ride_id)
    except:
        return jsonify({"message": "Input should be integer"}), 400

    if not isinstance(ride_id, int):
        return jsonify({"message": "Input should integer"}), 400

    # call the delete_ride func to delete a ride
    result = database_connection.delete_ride(current_user[0], ride_id)
    return result


@app.route('/api/v1/users/rides/<ride_id>/edit', methods=['PUT'])
@token_required
def edit_ride_offer(current_user, ride_id):
    """ Deletes the ride with id provided """

    # check that there are no missed out info or used wrong keys
    if check_ride_fields():
        return check_ride_fields()

    # keep all the ride fields in a dictionary
    ride_fields = generate_ride_field_dict()

    # Checking for errors linked to the input type
    if check_ride_field_type(ride_fields):
        return check_ride_field_type(ride_fields)

    edit_ride = {"current_user": current_user[0],
                 "ride_id": ride_id,
                 "origin": ride_fields['origin'],
                 "meet_point": ride_fields['meet_point'],
                 "contribution": ride_fields['contribution'],
                 "free_spots": ride_fields['free_spots'],
                 "start_date": ride_fields['start_date'],
                 "finish_date": ride_fields['finish_date'],
                 "terms": ride_fields['terms']}
    result = database_connection.edit_ride(edit_ride)
    return result


@app.route('/api/v1/rides/<request_id>/requests/cancel', methods=['DELETE'])
@token_required
def cancel_request(current_user, request_id):
    """ Passenger can cancel a ride request to a ride """
    try:
        request_id = int(request_id)
    except ValueError as err:
        return jsonify(
            {"message": "request_id should be of type integer"}
        ), 400
    result = database_connection.delete_request(current_user[0], request_id)
    return result



