import psycopg2
from pprint import pprint


class DatabaseConnection(object):
    def __init__(self):
        try:
            # establishing a server connection
            self.connection = psycopg2.connect(dbname="Carpool", user="postgres", password="Kp15712Kp", host="localhost")
            self.connection.autocommit = True

            # storing a cursor object
            self.cursor = self.connection.cursor()  # activate connection cursor
        except psycopg2.Error as err:
            pprint(err)

    def create_tables(self):
        create_table_command = "CREATE TABLE IF NOT EXISTS pet(id serial PRIMARY KEY, " \
                               "name VARCHAR (100), age INTEGER NOT NULL )"
        self.cursor.execute(create_table_command)

        company = """CREATE TABLE IF NOT EXISTS COMPANY(
           ID serial PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           AGE            INT     NOT NULL,
           ADDRESS        CHAR(50),
           SALARY         REAL,
           JOIN_DATE	  DATE
        );"""

        self.cursor.execute(company)

    def insert_new_record(self):
        insert_command = "INSERT INTO pet(name, age) VALUES ('dog', 12), ('cat', 89)"
        pprint(insert_command)
        self.cursor.\
            execute(insert_command)

        company = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE) VALUES (9, 'Paul', 32, 'California', 20000.00,'2001-07-13');"
        # self.cursor.execute(company)

    def select_record(self):
        record = "SELECT * FROM pet WHERE name='dog'"

        self.cursor.execute(record)
        row = self.cursor.fetchall()
        # pprint(row)

        compay = "SELECT  AGE, NAME,SALARY, JOIN_DATE, ADDRESS FROM company"
        self.cursor.execute(compay)

        row = self.cursor.fetchall()
        info = {"name": "", "age": " ", "salary": "", "join_date": ""}
        info_list = []
        for item in row:
            info['age'] = item[0]
            info['name'] = item[1]
            info['salary'] = item[2]
            info['join_date'] = item[3]

            info_list.append(info)

        pprint(info_list)


if __name__ == '__main__':
    # database connection create table
    database_connection = DatabaseConnection()
    database_connection.create_tables()

    # create new record
    database_connection.insert_new_record()

    # select query
    database_connection.select_record()






