from ride_my_way import views
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
        self.cur = views.database_connection
        views.database_connection.create_tables()

        # --------***** Creating users ********------------------

        # second user instance
        self.user_1 = {
            "name": "patrick",
            "email": "dr.kimpatrick@gmail.com",
            "username": "kimpatrick",
            "phone_number": "078127364",
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

    def test_create_user_1(self):
        """ Creating a user | supply right data
            expect a success
        """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

    def test_create_user_same_username(self):
        """ Creating another user with the same username """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # Creating another user with the same username, email and password
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)
        self.assertEqual(response.json,
                         {'message': 'Username already taken, try another'})

    def test_create_user_3(self):
        """ Second user instance | all expected to work fine """
        response_2 = self.app.post("{}auth/signup".format(BASE_URL),
                                   data=json.dumps(self.user_2),
                                   content_type=content_type)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.json,
                         {"message": "Account successfully created"})  # length=2

    def test_create_user_4(self):
        """ Wrong and missing user fields | Should raise and error message """
        response_3 = self.app.post("{}auth/signup".format(BASE_URL),
                                   data=json.dumps(self.user_3),
                                   content_type=content_type)

        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_3.json,
                         {"message": "You have either missed out some info or used wrong keys"})

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

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.json, {'message': 'Email or password is incorrect'})

    def test_login_2(self):
        """ create a user and login with with username which
            does not exist
         """

        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Email or password is incorrect'})

    def test_login_3(self):
        """ Lets creates a user and then login expect a success """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

    def test_create_ride_1(self):
        """ Lets create a ride offer here, first create account login and create ride
            Supply right ride data expect a success message
        """

        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

    # Lets try creating a ride but supply wrong data
    def test_create_ride_2(self):
        """ Supply wrong data when creating a ride by the logged in user"""
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']

        # supply information with wrong keys and missing parameters
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_400),
                                 headers={'Authorization': self.token}, content_type=content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'You have either missed out some info or used wrong keys'})

    # Lets try creating a ride but supply wrong data
    def test_create_ride_wrong(self):
        """ Supply wrong data when creating a ride by the logged in user
            with contribution as a string
        """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']

        # supply information with wrong keys and missing parameters
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_wrong_contribution),
                                 headers={'Authorization': self.token}, content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'contribution should be integer'})

    def test_available_ride(self):
        """ Create a user , login and then create a ride """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json['Rides']), 2)

    def test_driver_rides(self):
        """ Create a user , login and then create a ride """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()



        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}this/user/rides'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json["{}'s ride offers".format(self.current_user[2])]), 2)

    def test_get_single_ride_1(self):
        """ Create a user , login and then create a ride
            Supply wrong url input
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides/<ride_id>'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {'message': 'Input should be integer'})

    def test_get_single_ride_2(self):
        """ Create a user , login and then create a ride
            Supply wrong url input
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides/<ride_id>'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # check for the number of rides present
        response = self.app.get('{}rides/4'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "The ride offer with ride_id {} does not exist".format(4)})

    def test_request_for_ride_1(self):
        """ Create a user , login and then create a ride
            Ride id which does not exist
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        """ Creating another user """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_2),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}rides/1/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {'message': 'Your request has been successfully sent and pending approval'})

    def test_request_for_ride_2(self):
        """ Create a user , login and then create a ride
            Ride id which does not exist
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        # supply right information
        response = self.app.post('{}users/rides'.format(BASE_URL),
                                 data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride create successfully"})

        """ Creating another user """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_2),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}rides/19/requests'.format(BASE_URL),
                                 # data=json.dumps(self.ride_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "Ride_id ({}) does not exist".format(19)})

    def tearDown(self):
        sql_requests = "DROP TABLE IF EXISTS carpool_ride_request"
        sql_ride = "DROP TABLE IF EXISTS carpool_rides"
        sql = "DROP TABLE IF EXISTS carpool_users"

        sql_list = [sql_requests, sql_ride, sql]
        for sql in sql_list:
            self.cur.cursor.execute(sql)




