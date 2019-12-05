from flask import request
from flask_restful import Resource
from users.users_model import User
from util.jwt_handler import make_encrypted_token
import bcrypt


class CreateUserAccount(Resource):
    def post(self):
        """
        Create user route. 
            Request Body should have:
                first_name, last_name, username, password
            Success returns:
                {"success": True, "route": "create_user_accout", "user": new_user.to_json(), "token": token}, new_user.status_code
            Failure returns:
               return {"success": False, "route": "create_user_accout", "errors": new_user.errors}, new_user.status_code
        """
        r_body = request.get_json()
        first_name = r_body["user"]["first_name"]
        last_name = r_body["user"]["last_name"]
        username = r_body["user"]["username"]
        password = r_body["user"]["password"]
        password_digest = create_password_digest(password).decode("utf-8")
        new_user = User(first_name, last_name, username, password_digest)
        if new_user.save():
            token = make_encrypted_token({"user_id": new_user.id})
            return {"success": True, "route": "create_user_accout", "user": new_user.to_json(), "token": token}, new_user.status_code
        else:
            return {"success": False, "route": "create_user_accout", "errors": new_user.errors}, new_user.status_code


def create_password_digest(password):
    """
    Given a password it creates a bcrypt password digest with 12 rounds of salt/work. It converts password to 'utf-8' before encryption
    """
    u_pass = password.encode('utf-8')
    return bcrypt.hashpw(u_pass, bcrypt.gensalt(rounds=12))
