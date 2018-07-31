from flask import jsonify
import psycopg2
from ride_my_way.models import DatabaseConnection


class Rides(DatabaseConnection):
    def create_ride(self, new_ride):
        """ Creates ride offer in the database
            The driver_id which is a foreign key is gotten from
            the current_user instance in the token_required()
            decorator as id
        """
        try:
            sql = "INSERT INTO carpool_rides(driver_id, " \
                  "origin, " \
                  "meet_point, " \
                  "contribution, " \
                  "free_spots, start_date, " \
                  "finish_date, destination, terms) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(
                sql,
                (new_ride['driver_id'], new_ride['origin'],
                 new_ride['meet_point'], new_ride['contribution'],
                 new_ride['free_spots'], new_ride['start_date'],
                 new_ride['finish_date'], new_ride['destination'],
                 new_ride['terms'])
            )
        except psycopg2.Error as err:
            return str(err)
        return jsonify({"message": "Ride create successfully"}), 201

    def get_rides(self):
        """ Returns a list of all ride offers available """

        sql = "SELECT origin, meet_point, contribution, free_spots, " \
              "start_date, finish_date, id, destination FROM carpool_rides"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        rides_list = []
        for ride in result:
            ride_info_dict = {}
            ride_info_dict['origin'] = ride[0]
            ride_info_dict['meet_point'] = ride[1]
            ride_info_dict['contribution'] = ride[2]
            ride_info_dict['free_spots'] = ride[3]
            ride_info_dict['start_date'] = ride[4]
            ride_info_dict['finish_date'] = ride[5]
            ride_info_dict['ride_id'] = ride[6]
            ride_info_dict['destination'] = ride[7]

            rides_list.append(ride_info_dict)
        return jsonify({"Rides": rides_list}), 200

    def rides_given(self, driver_id):
        """ Returns a list of rides given by the User(Driver)"""
        try:
            sql = "SELECT origin, meet_point, contribution, free_spots, " \
                  "start_date, finish_date, id, destination FROM carpool_rides WHERE " \
                  "driver_id=%s" % driver_id
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            return jsonify({"message": "Some thing went wrong"}), 500

        rides_list = []
        for ride in result:
            ride_info = {}
            ride_info['origin'] = ride[0]
            ride_info['meet_point'] = ride[1]
            ride_info['contribution'] = ride[2]
            ride_info['free_spots'] = ride[3]
            ride_info['start_date'] = ride[4]
            ride_info['finish_date'] = ride[5]
            ride_info['ride_id'] = ride[6]
            ride_info['destination'] = ride[7]

            rides_list.append(ride_info)
        return rides_list

    def rides_taken(self, passenger_id):
        """ Returns a list of rides given by the User(Driver)"""
        try:
            sql = "SELECT ride_id FROM carpool_ride_request WHERE passenger_id={} AND accepted='accepted'".format(passenger_id)
            self.cursor.execute(sql)
            all_ride_ids = self.cursor.fetchall()
        except:
            return jsonify({"message": "Some thing went wrong"}), 500

        try:
            sql = "SELECT origin, meet_point, contribution, free_spots, " \
                  "start_date, finish_date, id, destination FROM carpool_rides "
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            return jsonify({"message": "Some thing went wrong"}), 500

        taken_rides_list = []
        for ride in result:
            for ride_id in all_ride_ids:
                if ride[6] == ride_id[0]:
                    taken_ride_info = {}
                    taken_ride_info['origin'] = ride[0]
                    taken_ride_info['meet_point'] = ride[1]
                    taken_ride_info['contribution'] = ride[2]
                    taken_ride_info['free_spots'] = ride[3]
                    taken_ride_info['start_date'] = ride[4]
                    taken_ride_info['finish_date'] = ride[5]
                    taken_ride_info['ride_id'] = ride[6]
                    taken_ride_info['destination'] = ride[7]

                    taken_rides_list.append(taken_ride_info)
        return taken_rides_list

    def get_user_info(self, user_id):
        """ Gets the info of the user with the user_id provided"""

        sql = "SELECT username, phone_number, gender, email " \
              "FROM carpool_users WHERE id=%s" % user_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        user = {}  # holds user information
        for user_info in result:
            user['username'] = user_info[0]
            user['gender'] = user_info[2]
            user['phone number'] = user_info[1]
            user['email'] = user_info[3]
        return user

    def ride_details(self, ride_id):
        """ Returns the details of a ride offer with the ride_id provided
            Also contains the driver information
        """

        sql = "SELECT origin, meet_point, contribution, free_spots, start_date, " \
              "finish_date, driver_id, destination FROM carpool_rides WHERE id=%s" % ride_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return jsonify(
                {"message": "The ride offer with ride_id {} does not exist".format(ride_id)}
            ), 404

        ride_info_detail = {}
        for info in result:
            # driver information to be returned with rides details
            driver_id = info[6]
            driver_info = self.get_user_info(driver_id)
            ride_info_detail['Driver details'] = driver_info

            ride_info_detail['origin'] = info[0]
            ride_info_detail['meet_point'] = info[1]
            ride_info_detail['contribution'] = info[2]
            ride_info_detail['free_spots'] = info[3]
            ride_info_detail['start_date'] = info[4]
            ride_info_detail['finish_date'] = info[5]
            ride_info_detail['destination'] = info[7]

        return jsonify({"Ride details": ride_info_detail})

    def delete_ride(self, current_user, ride_id):
        """ Deletes the ride """
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
            # check for the presence of that ride id
            sql = "DELETE FROM carpool_rides WHERE id={} AND driver_id={}" \
                .format(ride_id, current_user)
            self.cursor.execute(sql)
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        return jsonify(
            {"message":
             "You have successfully deleted a ride with ride_id {}".format(ride_id)})

    # edit_ride = {}
    def edit_ride(self, edit_ride):
        """ Deletes the ride """
        try:
            # check for the presence of that ride id
            sql = "SELECT * FROM carpool_rides WHERE id={} AND driver_id={}" \
                .format(edit_ride['ride_id'], edit_ride['current_user'])
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except psycopg2.Error as err:
            return jsonify({"message": str(err)}), 500

        if not result:
            return jsonify(
                {"message":
                 "You don't have a ride with ride_id ({}), recheck the info and try again"
                 .format(edit_ride['ride_id'])}
            ), 404

        try:
            # check for the presence of that ride id
            sql = "UPDATE carpool_rides " \
                  "SET origin='{}', meet_point='{}', " \
                  "contribution='{}', free_spots='{}', " \
                  "start_date='{}', finish_date='{}', " \
                  "terms='{}' WHERE id={} AND driver_id={}" \
                .format(edit_ride['origin'], edit_ride['meet_point'],
                        edit_ride['contribution'], edit_ride['free_spots'],
                        edit_ride['start_date'], edit_ride['finish_date'],
                        edit_ride['terms'], edit_ride['ride_id'],
                        edit_ride['current_user'])
            self.cursor.execute(sql)
        except psycopg2.Error as err:
            return jsonify({"message": str(err) + " " + " Update"}), 500

        return jsonify(
            {"message":
             "You have successfully edited a ride with ride_id {}".format(edit_ride['ride_id'])})

