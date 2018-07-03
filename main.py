import psycopg2


def connect_db():
    try:
        conn = psycopg2.connect(dbname="Carpool", user="postgres", password="Kp15712Kp", host="localhost")

        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(name VARCHAR (50) NOT NULL )")

    except psycopg2.Error as error:
        return error

    conn.commit()
    return conn


if __name__ == '__main__':
    conn = connect_db()
    print(conn)