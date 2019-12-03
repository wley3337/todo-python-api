from db.db_connection import DBConnection
from lists import lists_model
import os
# safe query construction cursor.execute("SELECT admin FROM users WHERE username = %s'", (username, ));

os.environ["FLASK_ENV"] = "TEST"


class User:
    def __init__(self, first_name,
                 last_name, username,
                 password_digest):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_digest = password_digest

    def save(self):
        print(os.environ["FLASK_ENV"])
        # now needs logic to:
        # check if a user with that username already exists
        # save if does not
        # return false
        if hasattr(self, 'id'):
            return True
        else:
            return False

    def to_json(self):
        if self.id is None:
            return False
        return get_user_by_id(self.id)

    def save_to_db(self):
        db = DBConnection()
        db.cur.execute(
            """
            INSERT INTO users(first_name, last_name, username, password_digest, created_at, updated_at) VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) 
            RETURNING row_to_json(users) 
            
            """, (self.first_name, self.last_name, self.username, self.password_digest))
        db.con.commit()
        new_user = db.cur.fetchone()[0]
        # print("commit return: ", commit_return)
        self.id = new_user["id"]
        db.close()


def all_users():
    """Gets all users from DB"""
    db = DBConnection()
    db.cur.execute(
        """
        SELECT row_to_json(u)
            FROM( SELECT id, first_name, last_name, username FROM users)
        u
        """
    )
    db_all_users = db.cur.fetchall()
    db.close()
    all_users = []
    for user in db_all_users:
        all_users.append(serialize_user(user[0]))
    return all_users


def get_user_by_id(id):
    """Gets a user by existing user id"""
    db = DBConnection()
    db.cur.execute(
        """
        SELECT row_to_json(u) 
            FROM( SELECT id, first_name, last_name, username FROM users WHERE id = %s)
        u
        """, (id,))
    user = db.cur.fetchone()
    db.close()
    if user is None:
        return None
    return serialize_user(user[0])


def get_user_by_username(username):
    """Gets a user by username"""
    db = DBConnection()
    db.cur.execute(
        """
        SELECT row_to_json(u) 
            FROM( SELECT * FROM users WHERE username = %s LIMIT 1)
        u
        """, (username,))
    user = db.cur.fetchone()
    db.close()
    if user is None:
        return None
    return user[0]


def serialize_user(user):
    """Serializes a JSON user object for ToDo Rails Frontend"""
    user_id = user["id"]
    user_lists = lists_model.get_users_lists_by_user_id(user_id)
    return {"firstName": user["first_name"], "lastName": user["last_name"], "username": user["username"], "lists": user_lists}
