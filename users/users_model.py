import os
from config.db.db_connection import DBConnection
from lists import lists_model

# os.environ["FLASK_gitENV"] = "TEST"


class User:
    """
    A User requires:
        first_name, last_name, username, password_digest (this should be a bcrypt generated digest)
    """

    def __init__(self, first_name,
                 last_name, username,
                 password_digest):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_digest = password_digest
        self.errors = {"messages": []}
        self.status_code = 200

    def save(self):
        """
        Checks to see if a username already exists in the database. 
            If it does it returns false and adds:
                self.errors["messages"].append("Username is already taken")
                self.status_code = 409
            If no user exists with username it returns true and sets self.status_code to 201
            If there is a DB error it returns false and adds:
                self.errors["messages"].append("DataBase Error, Please try again")
                self.status_code = 500
        """
        # check if a user with that username already exists
        if self.user_name_taken():
            self.errors["messages"].append("Username is already taken")
            self.status_code = 409
            return False
        # save if does not
        self.save_to_db()
        # if save successful
        if hasattr(self, 'id'):
            self.status_code = 201
            return True
        # if save is unsuccessful
        else:
            self.errors["messages"].append("DataBase Error, Please try again")
            self.status_code = 500
            return False

    def to_json(self):
        """
        Serializes a User obj, returns False if no user id
        """
        if self.id is None:
            return False
        return get_user_by_id(self.id)

    def save_to_db(self):
        """
        Saves User object to DB
        """
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

    def user_name_taken(self):
        """
        Checks DB for existing username returns True if a user exists with that username or False if not
        """
        db = DBConnection()
        db.cur.execute(
            """ SELECT * FROM users WHERE username = %s LIMIT 1""", (
                self.username,)
        )
        existing_user = db.cur.fetchone()
        print("username taken: ", existing_user)
        if existing_user is None:
            return False
        return True


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
