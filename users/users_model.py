from db import db_connection
from lists import lists_model
# safe query construction cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));


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
    db.cur.execute("""SELECT id, first_name, last_name, username FROM users""")
    db_all_users = db.cur.fetchall()
    db.close()
    all_users = []
    for user in db_all_users:
        all_users.append(serialize_user(user))
    return all_users


def get_user_by_id(id):
    db = db_connection.DBConnection()
    # returns tuple
    db.cur.execute(
        """SELECT id, first_name, last_name, username FROM users WHERE id = %s""", (id,))
    user = db.cur.fetchone()
    db.close()
    if user is None:
        return None
    return serialize_user(user)


def serialize_user(user):
    user_id = user[0]
    user_lists = lists_model.get_users_lists_by_user_id(user_id)
    return {"firstName": user[1], "lastName": user[2], "username": user[3], "lists": user_lists}
