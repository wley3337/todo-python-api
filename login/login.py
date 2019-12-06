import os
from flask import request
from flask_restful import Resource
import bcrypt
from users import users_model
from util.jwt_handler import make_encrypted_token


class Login(Resource):
    def post(self):
        r_body = request.get_json()
        print(r_body)
        username = r_body["user"]["username"]
        password = r_body["user"]["password"]
        user = users_model.get_user_by_username(username)
        if user is None:
            return {"success": False, "errors": {"messages": ["Wrong username or password"]}}
        elif user["password_digest"] and check_password(password, user["password_digest"]):
            auth_user = users_model.get_user_by_id(user["id"])
            token = make_encrypted_token({"user_id": user["id"]})
            print("authUser: ", auth_user)
            return {"success": True, "user": auth_user, "token": token}
        else:
            return {"success": False, "errors": {"messages": ["Wrong username or password"]}}


def check_password(password, password_digest):
    u_pass = password.encode('utf-8')
    u_pass_digest = password_digest.encode('utf-8')
    if bcrypt.checkpw(u_pass, u_pass_digest):
        print("BCrypt passed")
        return True
    else:
        print("BCrypt Failed")
        return False


# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
