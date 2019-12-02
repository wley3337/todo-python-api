from flask_restful import Resource


class CreateUserAccount(Resource):
    def post(self):
        return {"success": True, "route": "create_user_accout"}
