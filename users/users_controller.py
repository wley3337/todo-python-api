from flask_restful import Resource

from users import users_model


class UsersController(Resource):
    def get(self):
        user = users_model.all_users()
        return {"success": True, "users": user}, 200


class UsersAutoLogin(Resource):
    def get(self):
        user = users_model.get_user_by_id(1)
        if user is None:
            return {"success": False, "errors": {"messages": ["User not found"]}}, 204
        return {"success": True, "user": user}, 200
