import os
from flask_restful import Resource 

from db import db_connection

class UsersController(Resource):
    def get(self):
        db = db_connection.DBConnection()
        db.cur.execute("""SELECT id, first_name, last_name, username FROM users""")
        all_users = db.cur.fetchall()
        print(all_users)
        db.close()
        return {"success": True, "users": all_users }, 200

