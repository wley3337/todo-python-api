import os
import psycopg2


class DBConnection:
    def __init__(self):
        self.user = os.environ["DB_USER"]
        self.password = os.environ["DB_PASSWORD"]
        self.host = os.environ["DB_HOST"]
        self.port = os.environ["DB_PORT"]
        self.connect()

    def connect(self):
        if os.environ["FLASK_ENV"] == "TEST":
            print("TEST DB")
            try:
                self.con = psycopg2.connect(
                    dbname=os.environ["DB_DATABASE_TEST"]
                )
            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
        if os.environ["FLASK_ENV"] == "DEV":
            print("DEV DB")
            try:
                self.con = psycopg2.connect(
                    dbname=os.environ["DB_DATABASE_DEV"]
                )
            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
        if os.environ["FLASK_ENV"] == "PROD":
            print("PROD DB")
            try:
                self.con = psycopg2.connect(
                    dbname=os.environ["DB_DATABASE_PROD"]
                )
            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
        self.cur = self.con.cursor()

    def close(self):
        self.con.close()
        self.cur.close()
