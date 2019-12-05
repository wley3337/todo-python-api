import os
import json
from flask import request
from flask_restful import Resource
from users import users_model
from util.jwt_handler import auth_decorator


class UsersController(Resource):
    def get(self):
        """
        Returns all users with IDs
        """
        user = users_model.all_users()
        return {"success": True, "users": user}, 200


class UsersAutoLogin(Resource):
    method_decorators = [auth_decorator]

    def get(self, user_id):
        """
        user_id is passed from the auth_decorator on successful decoding of JWT token. If not returns an error message that the user is not found.
        """
        user = users_model.get_user_by_id(user_id)
        if user is None:
            return {"success": False, "errors": {"messages": ["User not found"]}}, 200
        return {"success": True, "user": user}, 200
