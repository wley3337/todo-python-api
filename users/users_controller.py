import os
import json
from flask import request
from flask_restful import Resource
from functools import wraps
import jwcrypto
from jwcrypto import jwt, jwk
from users import users_model
from util.jwt_handler import auth_decorator, make_encrypted_token


class UsersController(Resource):
    def get(self):
        user = users_model.all_users()
        return {"success": True, "users": user}, 200


# >>> from jwcrypto import jwt, jwk
# >>> k = {"k": "Wal4ZHCBsml0Al_Y8faoNTKsXCkw8eefKXYFuwTBOpA", "kty": "oct"}
# >>> key = jwk.JWK(**k)
# >>> e = token (unicode)
# >>> ET = jwt.JWT(key=key, jwt=e)
# >>> ST = jwt.JWT(key=key, jwt=ET.claims)
# >>> ST.claims
# u'{"info":"I\'m a signed token"}'

class UsersAutoLogin(Resource):
    method_decorators = [auth_decorator]

    def get(self, user_id):
        """
        user_id is passed from the auth_decorator on successful decoe of token. If not returns an error message that the user is not found.
        """
        user = users_model.get_user_by_id(user_id)
        if user is None:
            return {"success": False, "errors": {"messages": ["User not found"]}}, 200
        return {"success": True, "user": user}, 200
