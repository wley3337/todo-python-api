from db import db_connection

"""Query Strings"""
# safe query construction cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));

q_all_users = """SELECT id, first_name, last_name, username FROM users"""


class User:
    def __init__(self, first_name,
                 last_name, username,
                 password_digest):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_digest = password_digest


def all_users():
    """Gets all users from DB"""
    db = db_connection.DBConnection()
    db.cur.execute(q_all_users)
    all_users = db.cur.fetchall()
    db.close()
    return all_users
