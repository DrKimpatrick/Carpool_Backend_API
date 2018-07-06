from ride_my_way.models import DatabaseConnection
from ride_my_way.views import app

if __name__ == '__main__':
    database_connection = DatabaseConnection()

    database_connection.create_tables()
    app.run(debug=True)

