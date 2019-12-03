from flask import request
from flask_restful import Resource
from users.users_model import User
import bcrypt


class CreateUserAccount(Resource):
    def post(self):
        r_body = request.get_json()
        first_name = r_body["user"]["first_name"]
        last_name = r_body["user"]["last_name"]
        username = r_body["user"]["username"]
        password = r_body["user"]["password"]
        password_digest = create_password_digest(password).decode("utf-8")
        new_user = User(first_name, last_name, username, password_digest)
        if new_user.save():
            return {"success": True, "route": "create_user_accout", "user": new_user.to_json()}
        else:
            return {"success": False, "route": "create_user_accout", "errors": {"messages": ["Username is already taken"]}}, 500


def create_password_digest(password):
    u_pass = password.encode('utf-8')
    return bcrypt.hashpw(u_pass, bcrypt.gensalt(rounds=12))
