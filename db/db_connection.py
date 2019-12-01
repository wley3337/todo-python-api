# >>> import psycopg2

# # Connect to an existing database
# >>> conn = psycopg2.connect("dbname=test user=postgres")

# # Open a cursor to perform database operations
# >>> cur = conn.cursor()

# # Execute a command: this creates a new table
# >>> cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# # Pass data to fill a query placeholders and let Psycopg perform
# # the correct conversion (no more SQL injections!)
# >>> cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
# ...      (100, "abc'def"))

# # Query the database and obtain data as Python objects
# >>> cur.execute("SELECT * FROM test;")
# >>> cur.fetchone()
# (1, 100, "abc'def")

# # Make the changes to the database persistent
# >>> conn.commit()

# # Close communication with the database
# >>> cur.close()
# >>> conn.close()
import os 
import psycopg2


class DBConnection:
    def __init__(self, env="DEV"):
        self.env = env
        self.user = os.environ["DB_USER"] 
        self.password = os.environ["DB_PASSWORD"]
        self.host = os.environ["DB_HOST"]
        self.port = os.environ["DB_PORT"]
        self.connect()


    def connect(self):
        if self.env == "TEST":
            try:
                self.con = psycopg2.connect(
                   dbname = os.environ["DB_DATABASE_TEST"]
                )
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
        if self.env == "DEV":
            try:
                self.con = psycopg2.connect(
                    dbname = os.environ["DB_DATABASE_DEV"]
                )
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
        if self.env == "PROD":
            try:
                self.con = psycopg2.connect(
                    dbname = os.environ["DB_DATABASE_PROD"]
                )
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error) 
        self.cur = self.con.cursor()

    def close(self):
        self.con.close()
        self.cur.close()


