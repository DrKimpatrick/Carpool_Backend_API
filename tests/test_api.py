from ride_my_way import views
import unittest
import json

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
        # self.app.testing = True

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
            "email": "dr.kimpatrick@gmail.com",
            "username": "kimpatrick_2",
            "phone_number": "078127364",
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

        self.ride_400 = {"origin_400": "Busabala",
                         "destination_400": "Kampala",
                         "meet_point": "Ndeeba",
                         "contribution": 6000,
                         "free_spots": 9,
                         "start_date": "21st/06/2018",
                         "finish_date": "1st/06/2018",
                         "terms": "terms"}

    def tearDown(self):
        pass

    def test_create_user_1(self):
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Account successfully created"})

    def test_create_user_2(self):
        """ Has the same username with the created user above """

        # Username is unique, therefore an error message is raised here
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Username already taken, try another"}
                         )
        self.assertEqual(response.json['message'],
                         "Username already taken, try another"
                         )
