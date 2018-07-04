from flask import Flask, request, jsonify
from Application.models import DatabaseConnection
from functools import wraps
import jwt

app = Flask(__name__)

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

# creating an instance of the DatabaseConnections table
database_connection = DatabaseConnection()


def token_required(f):
    """ Restricts access to only users with the right token """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({"message": "Token missing"})


        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
            database_connection.cursor.execute(sql)
            current_user = database_connection.cursor.fetchone()
        except Exception as ex:
            return jsonify({"message": str(ex)})

        return f(current_user, *args, **kwargs)
    return decorated


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
            "username" not in request.json or
            "password" not in request.json):
        return jsonify(
            {"error": "You have either missed out some info or used wrong keys"}
        ), 400

    username = request.json['username']
    password = request.json['password']

    # sign_in now
    result = database_connection.sign_in(username, password)
    return jsonify({"message": result})


@app.route('/api/v1/users', methods=['GET'])
@token_required
def list_of_users(current_user):
    """ Get all users"""
    result = database_connection.get_all_users()
    return jsonify({"Users": result})


@app.route('/api/v1/rides', methods=['POST'])
@token_required
def create_ride(current_user):
    """ Creating a ride offer """

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
            {"error": "You have either missed out some info or used wrong keys"}
        ), 400

    origin = request.json['origin']
    destination = request.json['destination']
    meet_point = request.json['meet_point']
    contribution = request.json['contribution']
    free_spots = request.json['free_spots']
    start_date = request.json['start_date']
    finish_date = request.json['finish_date']
    terms = request.json['terms']

    # Checking for errors

    if not isinstance(terms, str):
        return jsonify({"error": "terms should be string"})

    if not isinstance(start_date, str):
        return jsonify({"error": "Start date should be string"})

    if not isinstance(finish_date, str):
        return jsonify({"error": "Finish date should be string"})

    if not isinstance(free_spots, int):
        return jsonify({"error": "Free spots should be integer"})

    if not isinstance(origin, str):
        return jsonify({"error": "Origin should be string"})

    if not isinstance(destination, str):
        return jsonify({"error": "Destination should be string"})

    if not isinstance(meet_point, str):
        return jsonify({"error": "meet_point should be string"})

    if not isinstance(contribution, (int, float, complex)):
        return jsonify({"error": "ride_id should be integer"})

    result = database_connection.create_ride(current_user[0], origin, meet_point, contribution, free_spots, start_date, finish_date)
    return jsonify({"message": result})


@app.route('/api/v1/rides', methods=['GET'])
@token_required
def available_ride(current_user):
    """ Retrieves all the available ride offers """
    result = database_connection.get_rides()
    return jsonify({"Rides": result})


@app.route('/api/v1/user/rides', methods=['GET'])
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
        return jsonify({"message": "Input should be integer"})

    if not isinstance(ride_id, int):
        return jsonify({"message": "Input should integer"})
    else:
        result = database_connection.ride_details(ride_id)
        return jsonify({"Result": result})


@app.route('/api/v1/rides/<ride_id>/requests', methods=['POST'])
@token_required
def request_for_ride(current_user, ride_id):
    """ Passenger can request for a ride by providing the ride_id"""
    try:
        ride_id = int(ride_id)
    except ValueError as exc:
        return jsonify(
            {"error": "ride_id should be of type integer. {}".format(str(exc))}
        )
    result = database_connection.request_ride(current_user[0], ride_id)
    return result


@app.route('/api/v1/user/rides/<ride_id>/requests', methods=['GET'])
@token_required
def requests_to_this_ride(current_user, ride_id):
    """ Retrieves all ride requests for that ride offer with id passed in """
    if isinstance(ride_id, int):
        return jsonify({"message": "Input should be integer"})
    result = database_connection.requests_to_this_ride(current_user[0], ride_id)
    return result






