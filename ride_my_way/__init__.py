from flask import Flask
from ride_my_way.models import DbClass

app = Flask(__name__)  # Initialising a flask application

"""creating an instance of the DatabaseConnections table
   used o execute run methods in the models.py
"""

database_connection = DbClass()

# This is placed here to prevent circular imports
from ride_my_way.views import users, rides, ride_requests
