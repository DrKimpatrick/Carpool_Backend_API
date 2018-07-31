from ride_my_way import app, database_connection
from flask import jsonify
from ride_my_way.views.views_helpers import token_required
from ride_my_way.views.rides_helper import (check_ride_field_type,
                                            check_ride_fields,
                                            generate_ride_field_dict)


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
                "finish_date": ride_fields['finish_date'],
                "destination": ride_fields['destination'],
                "terms": ride_fields['terms']}
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
    """ Retrieves all ride offers for the current user """
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


