from ride_my_way import app, database_connection

if __name__ == '__main__':
    database_connection.create_tables()
    app.run(debug=True)

