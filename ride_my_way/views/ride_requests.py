from ride_my_way import app, database_connection
from flask import jsonify, request
from ride_my_way.views.views_helpers import token_required
from ride_my_way.views.ride_requests_helper import reaction_status


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

    # Call a helper function to dictate a storage value
    # provide status to be stored in the db
    new_status = reaction_status(status)

    result = database_connection.respond_to_request(current_user[0], request_id, new_status)
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

