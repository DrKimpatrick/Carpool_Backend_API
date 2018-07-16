from ride_my_way import helpers, views
import unittest
import json
import jwt

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

BASE_URL = '/api/v1/'
content_type = 'application/json'


class TestRideMyWay(unittest.TestCase):
    """
                ========== Revision Notes ===========
                response.json = {"key": "value"}
                if key = User and Value = [{}]
                response.json['User'] = [{}]

                The key depends on the returned json "key"
                return jsonify("message": "some message")
                return jsonify("error": "some message")
                """

    def setUp(self):
        # views.app.config['TESTING'] = True
        self.app = views.app.test_client()
        self.cur = helpers.database_connection
        helpers.database_connection.create_tables()

        # --------***** Creating users ********------------------

        # second user instance
        self.user_1 = {
            "name": "patrick",
            "email": "dr.kimpatrick@gmail.com",
            "username": "kimpatrick",
            "phone_number": "0781273641",
            "bio": "This is patrick, mum's last born",
            "gender": "Male",
            "password": "Kp15712Kp"
        }

        # second user instance
        self.user_2 = {
            "name": "patrick",
            "email": "dr.kimpatrickw@gmail.com",
            "username": "kimpatrick_2",
            "phone_number": "0781273640",
            "bio": "This is patrick, mum's last born",
            "gender": "Male",
            "password": "Kp15712Kp"
        }

        # wrong and missing parameters
        self.user_3 = {
            "name_3": "patrick",
            "email": "dr.kimpatrick@gmail.com",
            "username_3": "kimpatrick_3",
            "bio": "This is patrick, mum's last born",
            "gender_3": "Male",
            "password": "Kp15712Kp"
        }

        # ---------------- Testing the user login --------------------

        # This user exists
        self.login_user_1 = {
            "username": "kimpatrick",
            "password": "Kp15712Kp"
        }
        # This user does not exist
        self.login_user_2 = {
            "username": "kimpatrick_2",
            "password": "Kp15712Kp"
        }

        # This user does not exist
        self.login_user_404 = {
            "username": "kimpatrick_404",
            "password": "Kp15712Kp"
        }

        # Bad request 400 | wrong inputs (keys)
        self.login_user_400 = {
            "username_400": "kimpatrick_400",
            "password": "Kp15712Kp"
        }

        # ----------------- Create ride offers ---------------------

        self.ride_1 = {"origin": "kampala",
                       "destination": "Masaka",
                       "meet_point": "Ndeeba",
                       "contribution": 5000,
                       "free_spots": 4,
                       "start_date": "21st/06/2018",
                       "finish_date": "1st/06/2018",
                       "terms": "terms"}

        self.ride_2 = {"origin": "Busabala",
                       "destination": "Kampala",
                       "meet_point": "Ndeeba",
                       "contribution": 6000,
                       "free_spots": 5,
                       "start_date": "21st/06/2018",
                       "finish_date": "1st/06/2018",
                       "terms": "terms"}
        self.ride_wrong_contribution = {"origin": "Busabala",
                                        "destination": "Kampala",
                                        "meet_point": "Ndeeba",
                                        "contribution": '6000',
                                        "free_spots": 5,
                                        "start_date": "21st/06/2018",
                                        "finish_date": "1st/06/2018",
                                        "terms": "terms"}

        self.ride_400 = {"origin_400": "Busabala",
                         "destination_400": "Kampala",
                         "meet_point": "Ndeeba",
                         "contribution": 6000,
                         "free_spots": 9,
                         "start_date": "21st/06/2018",
                         "finish_date": "1st/06/2018",
                         "terms": "terms"}

        # *********** Reject or accept ride request *****************
        self.reject_request = {"reaction": "reject"}
        self.accept_request = {"reaction": "accept"}
        self.pend_request = {"reaction": "pending"}
        self.reaction_400 = {"reaction_400": "400"}

    # ********** get_current user *******************************
    """ Helper func that gets the current user info """
    def get_current_user(self, token):

        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        return_current_user = self.cur.cursor.fetchone()
        return return_current_user

    # ********** Test whether the endpoints are protected **************

    def test_list_of_users_protected(self):
        """ Confirm list_of_users endpoint is protected
            It lists all users in the application
        """
        response = self.app.get('{}users'.format(BASE_URL),
                                content_type=content_type)
        self.assertEqual(response.json, {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_create_ride_protected(self):
        """ Confirm list_of_users endpoint is protected
            It lists all users in the application
        """
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 content_type=content_type)
        self.assertEqual(response.json, {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_available_ride_protected(self):
        """ Confirm available_ride endpoint is protected
            It lists all ride offers in the application
        """
        response = self.app.get('{}rides'.format(BASE_URL),
                                content_type=content_type)
        self.assertEqual(response.json,
                         {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_driver_rides_protected(self):
        """ Confirm driver_ride endpoint is protected
            It lists all ride given by the current driver
        """
        response = self.app.get('{}this/user/rides'.format(BASE_URL),
                                content_type=content_type)
        self.assertEqual(response.json,
                         {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_get_single_ride_protected(self):
        """ Confirm get_single_ride endpoint is protected
            Lists the details of a single ride by passing in the id
        """
        response = self.app.post('{}rides/1/requests'.format(BASE_URL),
                                 content_type=content_type)
        self.assertEqual(response.json, {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_request_for_ride_protected(self):
        """ Confirm request_for_ride endpoint is protected
            Enables a passenger to request for a ride offer
        """
        response = self.app.post('{}rides/<ride_id>/requests'.format(BASE_URL),
                                 content_type=content_type)
        self.assertEqual(response.json, {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_requests_to_this_ride_protected(self):
        """ Confirm requests_to_this_ride endpoint is protected
            Enables the driver to view a list of ride requests made
            to the ride with id he/she passes in
        """
        response = self.app.get('{}users/rides/1/requests'.format(BASE_URL),
                                content_type=content_type)
        self.assertEqual(response.json,
                         {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    def test_reaction_to_ride_request_protected(self):
        """ Confirm reaction_to_ride_request endpoint is protected
            Enables the driver to to accept or reject a ride
            request
        """
        response = self.app.put('{}users/rides/2/reaction'.format(BASE_URL),
                                content_type=content_type)
        self.assertEqual(response.json,
                         {"message": "Token missing"})
        self.assertEqual(response.status_code, 401)

    # ************** Test Signup *******************************************

    def test_create_user_1(self):
            """ Creating a user | supply right data
                expect a success
            """
            response = self.app.post("{}auth/signup".format(BASE_URL),
                                     data=json.dumps(self.user_1),
                                     content_type=content_type)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json,
                             {"message": "Account successfully created"})

    def test_create_user_same_username(self):
        """ Creating another user with the same username """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})
        self.assertEqual(response.status_code, 201)

        # Creating another user with the same username, email and password
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)
        self.assertEqual(response.json,
                         {'message': 'Username already taken, try another'})
        self.assertEqual(response.status_code, 406)

    def test_create_user_3(self):
        """ Second user instance | all expected to work fine """
        response_2 = self.app.post("{}auth/signup".format(BASE_URL),
                                   data=json.dumps(self.user_2),
                                   content_type=content_type)
        self.assertEqual(response_2.status_code, 201)
        self.assertEqual(response_2.json,
                         {"message": "Account successfully created"})

    def test_create_user_4(self):
        """ Wrong and missing user fields | Should raise and error message """
        response_3 = self.app.post("{}auth/signup".format(BASE_URL),
                                   data=json.dumps(self.user_3),
                                   content_type=content_type)

        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_3.json,
                         {"message":
                          "You have either missed out some "
                          "info or used wrong keys"})
        self.assertEqual(response_3.status_code, 400)

    # ************************* Test Login **********************************

    def test_login_1(self):
        # ---- for bad request ---------------------------
        """ Supply wrong data e.g missing fields"""
        response_400 = self.app.post("{}auth/login".format(BASE_URL),
                                     data=json.dumps(self.login_user_400),
                                     content_type=content_type)
        self.assertEqual(response_400.status_code, 400)

    def test_login_account(self):
        """ Right data but account does not exist """
        response_1 = self.app.post("{}auth/login".format(BASE_URL),
                                   data=json.dumps(self.login_user_1),
                                   content_type=content_type)

        self.assertEqual(response_1.status_code, 404)
        self.assertEqual(response_1.json,
                         {'message': 'Email or password is incorrect'})

    def test_login_2(self):
        """ create a user and login with with username which
            does not exist
         """

        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {'message': 'Email or password is incorrect'})

    def test_login_3(self):
        """ Lets creates a user and then login expect a success """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

    # ****************** Test create ride ********************************

    def test_create_ride_1(self):
        """ Lets create a ride offer here, first create account
            login and create ride
            Supply right ride data expect a success message
        """

        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

    # Lets try creating a ride but supply wrong data
    def test_create_ride_2(self):
        """ Supply wrong data when creating a ride by the logged in user"""
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply information with wrong keys and missing parameters
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_400),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {'message':
                          'You have either missed out '
                          'some info or used wrong keys'})

    # Lets try creating a ride but supply wrong data
    def test_create_ride_wrong(self):
        """ Supply wrong data when creating a ride by the logged in user
            with contribution as a string
        """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply information with wrong keys and missing parameters
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_wrong_contribution),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.json,
                         {'message': 'contribution should be integer'})
        self.assertEqual(response.status_code, 400)

    # ************ Test available rides **********************************

    def test_available_ride(self):
        """ Create a user , login and then create a ride """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json['Rides']), 2)

    # ************* Test driver rides *******************************

    def test_driver_rides(self):
        """ Create a user , login and then create a ride """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # implement a helper func for getting the current_use info e.g id
        self.current_user = self.get_current_user(self.token)

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}this/user/rides'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json["{}'s ride offers".
                             format(self.current_user[2])]), 2)

    # *********** Test get single ride by id ***************************

    def test_get_single_ride_1(self):
        """ Create a user , login and then create a ride
            Supply wrong url input
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides/<ride_id>'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.json,
                         {'message': 'Input should be integer'})
        self.assertEqual(response.status_code, 400)

    def test_get_single_ride_2(self):
        """ Create a user , login and then create a ride
            Supply wrong url input
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides/<ride_id>'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json), 1)

    def test_get_single_ride_3(self):
        """ Create a user , login and then create a ride
            Ride id which does not exist
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides/4'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)

        self.assertEqual(response.json,
                         {"message":
                          "The ride offer with ride_id {} does not exist"
                          .format(4)})
        self.assertEqual(response.status_code, 404)

    # *********** Test request to join ride *****************************

    def test_request_for_ride_1(self):
        """ Making a request to a ride
            Signup a user
            login the user
            Let the user create two ride offers

            create another user, let the user login
            let current login request for a ride
            supply ride id that exists

         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Create a ride offer 1st"""
        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        """ Create second ride offer 2nd"""
        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        """ Creating another user who will request to join a ride"""
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_2),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        """ Login the user who is going to request for a ride """
        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Now let the user request for the first ride id=1"""
        # supply right information
        response = self.app.post('{}rides/1/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.json,
                         {'message':
                          'Your request has been successfully '
                          'sent and pending approval'})
        self.assertEqual(response.status_code, 200)

    def test_request_for_ride_2(self):
        """ Create a user , login and then create a ride
            Fetch ride details for a ride that does not exist
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        """ Creating another user """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_2),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        # supply right information
        response = self.app.post('{}rides/19/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {"message": "Ride_id ({}) does not exist"
                          .format(19)})

    # current user request to join a ride he/she has created
    def test_request_for_ride_3(self):
        """ Making a request to a ride
            Signup a user
            login the user
            Let the user create two ride offers

            create another user, let the user login
            let current login request for a ride
            he/she has created

         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Create a ride offer 1st"""
        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        """ 
            Now let the current user request to join a 
            ride he/she has created
        """
        # supply right information
        response = self.app.post('{}rides/1/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json,
                         {'message':
                          'Your can not make a ride request to '
                          'a ride you created'})

    def test_requests_to_this_ride_1(self):
        """ View requests to a ride
            Signup a user
            login the user
            Let the user create two ride offers

            create another user, let the user login
            let current login request for a ride
            supply ride id that exists

         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Create a ride offer 1st"""
        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # ----------------------------------------------------------------------
        """ Creating another user who will request to join a ride"""
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_2),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        """ Login the user who is going to request for a ride """
        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Now let the user request for the first ride id=1"""
        # supply right information
        response = self.app.post('{}rides/1/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'message':
                          'Your request has been successfully sent '
                          'and pending approval'
                          })

        # ----------------------------------------------------------------
        """ Let the other first user login and view 
            requests made to the ride he/she
            created 
        """
        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ View requests made to the ride offer """
        # supply right information
        response = self.app.get('{}users/rides/1/requests'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json['Ride requests']), 1)

        # supply right information
        response = self.app.get('{}users/rides/2/requests'.format(BASE_URL),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,
                         {"message":
                          "You don't have a ride with ride_id ({}), "
                          "recheck the info and try again"
                          .format(2)}), 404

    def test_reaction_to_ride_request(self):
        """ Accept or Reject ride requests
            Signup a user
            login the user
            Let the user create two ride offers

            create another user, let the user login
            let current login request for a ride

            Let the driver accept or reject a ride request

         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Create a ride offer 1st"""
        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Ride create successfully"})

        # ---------------------------------------------------------------------------------
        """ Creating another user who will request to join a ride"""
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_2),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        """ Login the user who is going to request for a ride """
        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ Now let the user request for the first ride id=1"""
        # supply right information
        response = self.app.post('{}rides/1/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token},
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {'message':
                          'Your request has been successfully sent and '
                          'pending approval'})

        # let the passenger try to accept or reject the request he/she
        # has created (expect an error because is not acceptable)
        response = self.app.put('{}users/rides/1/reaction'.format(BASE_URL),
                                data=json.dumps(self.reject_request),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json, {
                 "message":
                 "Sorry, you can only react to a ride request "
                 "for the ride you created"
                })

        # ----------------------------------------------------------------
        """ Let the other first user login and view 
        requests made to the ride he/she
        created """
        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Token']

        """ View requests made to the ride offer """
        # supply right information
        response = self.app.put('{}users/rides/1/reaction'.format(BASE_URL),
                                data=json.dumps(self.reject_request),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Ride request successfully {}"
                          .format("rejected")})

        # supply wrong key | remember right key is 'reaction'
        response = self.app.put('{}users/rides/1/reaction'.format(BASE_URL),
                                data=json.dumps(self.reaction_400),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
                "message":
                "Input should be of type dictionary where key is "
                "'reaction' and value 'reject' or 'accept' or 'pending' "
                "set back to default"
            })

        # supply request id that does not exist
        response = self.app.put('{}users/rides/2/reaction'.format(BASE_URL),
                                data=json.dumps(self.reject_request),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'No request with id (2)'})

        # supply string as request id
        response = self.app.put('{}users/rides/kim/reaction'.format(BASE_URL),
                                data=json.dumps(self.reject_request),
                                headers={'Authorization': self.token},
                                content_type=content_type)
        self.assertEqual(response.json,
                         {"message": "request_id should be of type integer"})
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        sql_requests = "DROP TABLE IF EXISTS carpool_ride_request"
        sql_ride = "DROP TABLE IF EXISTS carpool_rides"
        sql = "DROP TABLE IF EXISTS carpool_users"

        sql_list = [sql_requests, sql_ride, sql]
        for sql in sql_list:
            self.cur.cursor.execute(sql)




