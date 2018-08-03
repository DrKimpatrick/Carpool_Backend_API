from flask import jsonify
import psycopg2
from ride_my_way.models import DatabaseConnection


class RideRequests(DatabaseConnection):
    def request_ride(self, current_user, ride_id):
        """ Post a request for a ride by providing the ride id"""

        # ensure that user does not make more requests to the same ride
        try:
            sql = "SELECT ride_id, passenger_id FROM carpool_ride_request"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for request_info in result:
                if request_info[0] == ride_id and request_info[1] == current_user:
                    return jsonify(
                        {"message": "You already made a request to that ride"}
                    ), 406
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        # check to see whether the current user is the author of that ride
        # Current user should not make a request to the ride he/she created
        try:
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}".format(ride_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": "Ride_id ({}) does not exist".format(ride_id)}), 404

        if result:
            return jsonify(
                {"message":
                 "Your can not make a ride request to a ride you created"}
            ), 406

        # Now make a request to a ride offer
        try:
            sql = "INSERT INTO carpool_ride_request(ride_id, passenger_id)" \
                  " VALUES(%s, %s)"
            self.cursor.execute(sql, (ride_id, current_user))
        except psycopg2.Error as err:
            return jsonify({"message": "Ride_id ({}) does not exist".format(ride_id)}), 404
        return jsonify(
            {"message":
             "Your request has been successfully sent and pending approval"}
        ), 200

    def all_requests(self):
        """ Retrieves all ride requests"""
        sql = "SELECT * FROM carpool_ride_request"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def requests_to_this_ride(self,
                              current_user,
                              ride_id
                              ):
        """ Retrieves all ride requests for that ride offer
            Only if the current user is the author of the ride offer
        """

        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}" \
                .format(ride_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride with ride_id ({}), recheck the info and try again"
                 .format(ride_id)}
            ), 404

        try:
            # fetching data from the ride requests table where ride_id is
            sql = "SELECT id, passenger_id, accepted FROM  " \
                  "carpool_ride_request WHERE ride_id=%s" % ride_id
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "No requests made to ride with ride_id ({})".format(ride_id)}
            ), 404

        requests_list = []
        for r_request in result:
            request_info = {}
            request_info['request_id'] = r_request[0]
            request_info['request_status'] = r_request[2]

            # getting the passenger information
            passenger_id = r_request[1]
            passenger_info = self.get_user_info(passenger_id)
            request_info['passenger_details'] = passenger_info
            requests_list.append(request_info)

        return jsonify({"Ride_requests": requests_list}), 200

    def respond_to_request(self,
                           current_user,
                           request_id,
                           status
                           ):
        """ Driver accepts or rejects a ride request in reaction to a request """

        # check for the presence of that request id
        sql = "SELECT ride_id FROM carpool_ride_request WHERE id={}" \
            .format(request_id)
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        if not result:
            return jsonify(
                {
                    "message": "No request with id ({})".format(request_id)
                }
            ), 404

        # getting the ride_id to the ride where the request is made
        # result is of length one
        ride_id = result[0][-1]

        # ensure that the current user actually created that ride
        sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}" \
            .format(ride_id, current_user)

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if not result:
            return jsonify(
                {
                    "message":
                        "Sorry, you can only react to a ride request for the ride you created"
                }
            ), 406
        sql = "UPDATE carpool_ride_request SET accepted='{}' WHERE id={}" \
            .format(status, request_id)

        self.cursor.execute(sql)

        return jsonify({"message": "Ride request successfully {}".format(status)}), 200

    def delete_request(self,
                       current_user,
                       request_id
                       ):
        """ Driver accepts or rejects a ride request in reaction to a request """

        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_ride_request WHERE id={} AND passenger_id={}" \
                .format(request_id, current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride request with request_id ({}), "
                 "recheck the info and try again"
                 .format(request_id)}
            ), 404

        try:
            # check for the presence of that ride id
            sql = "DELETE FROM carpool_ride_request WHERE id={} AND passenger_id={}" \
                .format(request_id, current_user)
            self.cursor.execute(sql)
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        return jsonify(
            {"message":
             "You have successfully deleted a ride request with request_id {}".format(request_id)}), 200

    def show_all_my_requests(self, current_user):
        """ Driver accepts or rejects a ride request in reaction to a request """

        try:
            # check for the presence of that ride id
            sql = "SELECT id, ride_id, accepted FROM carpool_ride_request WHERE passenger_id={}" \
                .format(current_user)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify({"message": "You have not made any ride requests"}), 404

        request_list = []
        for request_info in result:
            req_info = {}
            req_info['request_id'] = request_info[0]
            req_info['ride_id'] = request_info[1]
            req_info['request_status'] = request_info[2]

            try:
                sql = "SELECT origin, destination, meet_point, contribution, start_date, " \
                      "finish_date , driver_id FROM carpool_rides WHERE id={}".format(request_info[1])

                self.cursor.execute(sql)
                ride_result = self.cursor.fetchone()
            except psycopg2.Error as err:
                return jsonify({"message": str(err)}), 500

            req_info['origin'] = ride_result[0]
            req_info['destination'] = ride_result[1]
            req_info['meet_point'] = ride_result[2]
            req_info['contribution'] = ride_result[3]
            req_info['start_date'] = ride_result[4]
            req_info['finish_date'] = ride_result[5]
            req_info['driver_id'] = ride_result[6]

            try:
                sql = "SELECT username FROM carpool_users WHERE id={}".format(ride_result[6])
                self.cursor.execute(sql)
                user_result = self.cursor.fetchone()
            except psycopg2.Error as err:
                return jsonify({"message": str(err)}), 500
            req_info['username'] = user_result[0]

            request_list.append(req_info)

        return jsonify({"Ride_requests": request_list}), 200
