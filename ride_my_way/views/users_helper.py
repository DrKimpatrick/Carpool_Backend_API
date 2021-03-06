from flask import request, jsonify
import re  # here I import the module that implements regular expressions


# here is my function for checking valid email address
def check_email(email):
    # message returned when email is invalid
    wrong_email = "{} is not a valid email".format(email)

    # verifying the submitted email

    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    email = re.match(pattern, email)  # returns none if no match
    if not email:
        return jsonify({"message": wrong_email}), 400


# here is my function for checking valid
def check_phone_number(phone_number):
    wrong_phone_number = "{} is not a valid phone number".format(phone_number)
    pattern = r"^(\+?\d{1,4}[\s-])?(?!0+\s+,?$)\d{10}\s*,?$"
    phone_number = re.match(pattern, phone_number)
    if not phone_number:
        return jsonify({"message": wrong_phone_number}), 400


# here is a function for checking a valid password
def check_password(password):
    wrong_password = "Password should be alphanumeric and at least 6 characters long"
    pattern = r"^(?=.*\d)(?=.*[a-z])[a-zA-Z0-9]{6,999}$"
    password = re.match(pattern, password)
    if not password:
        return jsonify({"message": wrong_password}), 400


# check that the format in which the field data is presented is valid
def check_user_field_type(user_field_dict):
    """ Checks the type of the ride field inputs
        Take in the the ride fields as a dictionary
    """

    # check email
    if check_email(user_field_dict['email']):
        return check_email(user_field_dict['email'])

    # check phone number
    if check_phone_number(user_field_dict['phone_number']):
        return check_phone_number(user_field_dict['phone_number'])

    # check password
    if check_password(user_field_dict['password']):
        return check_password(user_field_dict['password'])


# check that all input fields are available
def check_user_fields():
    """ Ensure that all fields are available
        and wrong keys are not provided

        It is a helper function that is called in
        create_user and edit user | all provide the same fields
    """
    if (not request.json or
            "name" not in request.json or
            "email" not in request.json or
            "username" not in request.json or
            "phone_number" not in request.json or
            "bio" not in request.json or
            "gender" not in request.json or
            "password" not in request.json):

        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400


# get user fields
def generate_user_field_dict():
    """ Keep all the user info in the dictionary
        Is input for check_user_field_type helper func
    """
    name = request.json["name"]
    email = request.json['email']
    username = request.json['username']
    phone_number = request.json['phone_number']
    bio = request.json['bio']
    gender = request.json['gender']
    password = request.json['password']

    user_fields = {"name": name,
                   "email": email,
                   "username": username,
                   "phone_number": phone_number,
                   "bio": bio,
                   "gender": gender,
                   "password": password
                   }

    return user_fields


# get user fields
def generate_edit_user_fields_as_dict():
    """ Keep all the user info in the dictionary
        Is input for check_user_field_type helper func
    """
    name = request.json['name']
    email = request.json['email']
    username = request.json['username']
    phone_number = request.json['phone_number']
    bio = request.json['bio']
    gender = request.json['gender']

    user_fields = {"name": name,
                   "email": email,
                   "username": username,
                   "phone_number": phone_number,
                   "bio": bio,
                   "gender": gender,

                   }

    return user_fields


# check that all input fields are available
def check_user_edit_fields():
    """ Ensure that all fields are available
        and wrong keys are not provided

        It is a helper function that is called in
        create_user and edit user | all provide the same fields
    """
    if (not request.json or
            "name" not in request.json or
            "email" not in request.json or
            "username" not in request.json or
            "phone_number" not in request.json or
            "bio" not in request.json or
            "gender" not in request.json):

        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400


# check that the format in which the field data is presented is valid
def check_user_edit_field_type(user_field_dict):
    """ Checks the type of the ride field inputs
        Take in the the ride fields as a dictionary
    """

    # check email
    if check_email(user_field_dict['email']):
        return check_email(user_field_dict['email'])

    # check phone number
    if check_phone_number(user_field_dict['phone_number']):
        return check_phone_number(user_field_dict['phone_number'])

