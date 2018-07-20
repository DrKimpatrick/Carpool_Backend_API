from flask import request, jsonify


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

