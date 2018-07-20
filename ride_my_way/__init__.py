from flask import Flask
from ride_my_way.models.models import DatabaseConnection


app = Flask(__name__)  # Initialising a flask application

"""creating an instance of the DatabaseConnections table
   used o execute run methods in the models.py
"""
database_connection = DatabaseConnection()

# This is placed here to prevent circular imports
from ride_my_way.views import users, rides, ride_requests
