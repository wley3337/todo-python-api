from flask_restful import Resource

from users import users_model


class UsersController(Resource):
    def get(self):
        user = users_model.all_users()
        return {"success": True, "users": user}, 200


class UsersAutoLogin(Resource):
    def get(self):
        return {"route": "users-auto-login"}
