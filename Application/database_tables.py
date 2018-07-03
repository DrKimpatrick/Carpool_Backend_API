"""{"name":"kimanje patrick 3", "email": "dr.kimpatrick@gmail.com", "username": "patrick_8000",
"phone_number": 888, "bio": "this is kim", "gender": "Male", "password": "Kp15712Kp"
}
{"origin": "kampala", "destination": "Masaka", "meetpoint": "Ndeeba", "contribution": 5000,
        "free_spots": 4, "start_date": "21st/06/2018", "finish_date": "1st/06/2018", "terms":"terms", "rideId": 1000
    }"""

tables_list = [
    {
        "carpool_users": """

                         CREATE TABLE IF NOT EXISTS carpool_users(
                         id serial PRIMARY KEY, 
                         name VARCHAR (100), 
                         username VARCHAR (100) UNIQUE NOT NULL ,
                         email VARCHAR (100) UNIQUE NOT NULL ,
                         phone_number VARCHAR (10) UNIQUE ,
                         bio VARCHAR (1000), 
                         gender VARCHAR (10),
                         password VARCHAR (1000))
                         
                      """
    }
    ,
    {
        "carpool_rides": """

                         CREATE TABLE IF NOT EXISTS carpool_rides(
                         id serial PRIMARY KEY,
                         
                         driver_id INTEGER NOT NULL ,
                         FOREIGN KEY(driver_id) REFERENCES carpool_users(id) ON DELETE CASCADE,
                         origin VARCHAR (100) NOT NULL ,
                         meet_point VARCHAR NOT NULL ,
                         contribution INTEGER DEFAULT 0,
                         free_spots INTEGER NOT NULL ,
                         start_date VARCHAR (12),
                         finish_date VARCHAR (12),
                         terms VARCHAR (1000)
                         )
                            
                         """
    },
    {
        "carpool_ride_requests": """
                                 CREATE TABLE IF NOT EXISTS carpool_ride_request(
                                 id serial PRIMARY KEY,
                                 
                                 ride_id INTEGER NOT NULL ,
                                 FOREIGN KEY (ride_id) 
                                 REFERENCES carpool_rides(id) ON DELETE CASCADE,
                                 
                                 passenger_id INTEGER NOT NULL ,
                                 FOREIGN KEY(passenger_id) REFERENCES carpool_users(id) ON DELETE CASCADE ,
                                 accepted BOOLEAN DEFAULT FALSE ) 
                                 
                                 """
    }
]
